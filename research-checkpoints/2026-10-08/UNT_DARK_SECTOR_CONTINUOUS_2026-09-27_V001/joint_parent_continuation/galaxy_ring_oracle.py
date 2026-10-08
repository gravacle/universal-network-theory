"""Independent Newtonian ring quadrature; freeze/run only via main."""
import os
for _name in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS',
              'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[_name] = '1'
import hashlib
import json
import math
from pathlib import Path
import resource
import sys
import time
import uuid
import numpy as np
from numpy.polynomial.legendre import leggauss
import galaxy_density as density

ROOT = Path(__file__).resolve().parent
RADII = (2.7, 8.7, 20.7, 35.7, 43.7)
ORDERS = (48, 96)
G = density.G_KPC_KMS2_MSUN
QUADS = {n: leggauss(n) for n in (48, 96, 128, 256)}


def encoded(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save_new(path, obj):
    data = json.dumps(obj, indent=2, sort_keys=True, allow_nan=False)+'\n'
    temporary = path.with_name(path.name+'.pending-'+uuid.uuid4().hex)
    with temporary.open('x') as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    os.link(temporary, path)  # atomic publication; refuses an existing result
    temporary.unlink()


def relative(actual, reference):
    return abs(float(actual)-float(reference))/max(1., abs(float(reference)))


def elliptic(kprime):
    """K(k),E(k), using kprime=sqrt(1-k²) without near-ring subtraction."""
    b = np.asarray(kprime, dtype=float)
    assert np.all((b > 0)&(b <= 1+1e-14))
    b = np.minimum(b, 1.)
    a = np.ones_like(b)
    correction = (1-b)*(1+b)/2
    coefficient = 1.
    for _ in range(20):
        c = (a-b)/2
        correction += coefficient*c*c
        a, b = (a+b)/2, np.sqrt(a*b)
        coefficient *= 2
    first = math.pi/(2*a)
    return first, first*(1-correction)


def ring_kernels(radius, height, source_radius):
    """Geometric kernels multiplying G*a*Sigma(a) da; force is signed."""
    assert radius > 0 and height > 0
    a = np.asarray(source_radius, dtype=float)
    distance = np.sqrt((radius+a)**2+height*height)
    near2 = (radius-a)**2+height*height
    first, second = elliptic(np.sqrt(near2)/distance)
    potential = -4*first/distance
    radial = 2/(radius*distance)*(first-(a*a+height*height-radius*radius)/near2*second)
    return potential, radial


def radial_quadrature(radius, height, knots, cutoff, order):
    panels = np.unique(np.r_[0., np.asarray(knots), radius, cutoff])
    panels = panels[(panels >= 0)&(panels <= cutoff)]
    u = np.arcsinh((panels-radius)/height)
    nodes, weights = QUADS[order]
    mid, half = (u[1:]+u[:-1])/2, (u[1:]-u[:-1])/2
    mapped = mid[:, None]+half[:, None]*nodes
    a = radius+height*np.sinh(mapped)
    w = half[:, None]*weights*height*np.cosh(mapped)
    assert np.all(a >= -1e-10) and np.all(w > 0)
    return np.maximum(a, 0.).ravel(), w.ravel()


def source_knots(components):
    return np.unique(np.concatenate([p.r for p in components.values()]))


def source_cutoff(components):
    return max(float(p.r[-1]+(32*p.tail if p.tail is not None else 0))
               for p in components.values())


def field(radius, height, components, order=96):
    """Finite-height Newtonian field, not a pointwise nonlinear response."""
    cutoff = source_cutoff(components)
    assert 0 < radius < cutoff and height > 0
    a, w = radial_quadrature(radius, height, source_knots(components), cutoff, order)
    potential_kernel, force_kernel = ring_kernels(radius, height, a)
    pieces = {}
    for name, profile in components.items():
        shell = a*profile.sigma(a)*1e6*w
        omitted = float(2*math.pi*1e6*profile.integral(cutoff, np.inf))
        pieces[name] = {'potential_kms2': float(G*np.dot(shell, potential_kernel)),
                        'gR_kms2_per_kpc': float(G*np.dot(shell, force_kernel)),
                        'quadrature_mass_Msun': float(2*math.pi*np.sum(shell)),
                        'omitted_mass_Msun': omitted}
    omitted_total = sum(p['omitted_mass_Msun'] for p in pieces.values())
    return {'potential_kms2': sum(p['potential_kms2'] for p in pieces.values()),
            'gR_kms2_per_kpc': sum(p['gR_kms2_per_kpc'] for p in pieces.values()),
            'components': pieces, 'cutoff_kpc': cutoff,
            'force_tail_bound_kms2_per_kpc': G*omitted_total/(cutoff-radius)**2,
            'potential_tail_bound_kms2': G*omitted_total/(cutoff-radius)}


def surface_slope(radius, components):
    slope = 0.
    for p in components.values():
        assert np.all(abs(p.r-radius) > 1e-10)
        if radius > p.r[-1]:
            slope += -float(p.sigma(radius))/p.tail if p.tail is not None else 0.
        else:
            index = int(np.searchsorted(p.r, radius)-1)
            slope += (p.s[index+1]-p.s[index])/(p.r[index+1]-p.r[index])
    return float(slope)*1e6


def calculate():
    started = time.perf_counter()
    checks, elliptic_rows, ring_rows, kuzmin_rows, cases = [], [], [], [], []

    def check(name, error, tolerance):
        checks.append({'name': name, 'error': float(error), 'tolerance': float(tolerance),
                       'passed': bool(math.isfinite(float(error)) and error <= tolerance)})

    for k in (0., .2, .7, .99):
        kval, eval_ = elliptic(math.sqrt((1-k)*(1+k)))
        direct = {}
        for order in (128, 256):
            x, w = QUADS[order]
            theta, weights = (x+1)*math.pi/4, w*math.pi/4
            q = np.sqrt(1-k*k*np.sin(theta)**2)
            direct[order] = [float(np.dot(weights, 1/q)), float(np.dot(weights, q))]
        for i, value in enumerate((kval, eval_)):
            check(f'elliptic:{k}:{i}', relative(value, direct[256][i]), 1e-11)
            check(f'elliptic_quadrature:{k}:{i}', relative(direct[128][i], direct[256][i]), 1e-11)
        elliptic_rows.append({'k': k, 'AGM_K': float(kval), 'AGM_E': float(eval_), 'direct': direct})

    for radius, a, height in ((2.,1.,.4),(1.,2.,.4),(2.,2.,.4),(8.,3.,.5),(3.,8.,.5)):
        pk, fk = ring_kernels(radius, height, a)
        direct = {}
        for order in (128, 256):
            x, w = QUADS[order]
            theta, weights = (x+1)*math.pi/2, w*math.pi  # twice integral 0..pi
            separation = np.sqrt(radius*radius+a*a+height*height-2*radius*a*np.cos(theta))
            direct[order] = [float(np.dot(weights, -1/separation)),
                             float(np.dot(weights, (radius-a*np.cos(theta))/separation**3))]
        for i, value in enumerate((pk, fk)):
            check(f'ring:{radius}:{a}:{height}:{i}', relative(value, direct[256][i]), 2e-10)
            check(f'ring_quadrature:{radius}:{a}:{height}:{i}', relative(direct[128][i], direct[256][i]), 2e-10)
        if (radius, a) == (1., 2.):
            check('outward_exterior_ring', 0. if fk < 0 else 1., 0.)
        ring_rows.append({'R': radius, 'a': a, 'z': height,
                          'potential_kernel': float(pk), 'force_kernel': float(fk), 'direct': direct})

    cutoff = 1024.
    kuzmin_knots = [0.,.25,.5,1.,2.,4.,8.,16.,32.,64.,128.,256.,512.,cutoff]
    omitted = 1/math.sqrt(1+cutoff*cutoff)
    for radius, height in ((.7,.2),(1.3,.05),(3.7,.2),(8.3,.4)):
        outputs = {}
        for order in ORDERS:
            a, w = radial_quadrature(radius, height, kuzmin_knots, cutoff, order)
            shell = a/(2*math.pi*(1+a*a)**1.5)*w
            pk, fk = ring_kernels(radius, height, a)
            outputs[order] = {'potential': float(np.dot(shell, pk)),
                              'gR': float(np.dot(shell, fk)), 'mass': float(2*math.pi*np.sum(shell))}
        exact_p = -1/math.sqrt(radius*radius+(height+1)**2)
        exact_g = radius/(radius*radius+(height+1)**2)**1.5
        pb, gb = omitted/(cutoff-radius), omitted/(cutoff-radius)**2
        for key in ('potential', 'gR'):
            check(f'kuzmin_quadrature:{radius}:{key}', relative(outputs[48][key], outputs[96][key]), 1e-10)
        check(f'kuzmin_exact_force:{radius}', abs(outputs[96]['gR']-exact_g), gb+1e-10*max(1.,abs(exact_g)))
        check(f'kuzmin_exact_potential:{radius}', abs(outputs[96]['potential']-exact_p), pb+1e-10*max(1.,abs(exact_p)))
        check(f'kuzmin_mass:{radius}', abs(outputs[96]['mass']-(1-omitted)), 1e-10)
        kuzmin_rows.append({'R': radius, 'z': height, 'orders': outputs,
                            'exact_potential': exact_p, 'exact_gR': exact_g,
                            'force_tail_bound': gb, 'potential_tail_bound': pb, 'cutoff': cutoff})

    for hi_tail in (False, True):
        for h2_tail in (False, True):
            model = f'HI_{int(hi_tail)}_H2_{int(h2_tail)}'
            components = density.profiles(hi_tail, h2_tail)
            masses = density.masses(components)
            knots = source_knots(components)
            for radius in RADII:
                distance = float(np.min(abs(knots-radius)))
                assert distance > 1e-10
                heights = [min(.2, distance/4)/2**i for i in range(3)]
                rows = []
                for height in heights:
                    outputs = {order: field(radius, height, components, order) for order in ORDERS}
                    for key in ('gR_kms2_per_kpc', 'potential_kms2'):
                        check(f'galaxy_quadrature:{model}:{radius}:{height}:{key}',
                              relative(outputs[48][key], outputs[96][key]), 1e-8)
                    for name, piece in outputs[96]['components'].items():
                        check(f'galaxy_mass:{model}:{radius}:{height}:{name}',
                              abs(piece['quadrature_mass_Msun']+piece['omitted_mass_Msun']-masses[name])/masses[name], 1e-9)
                    rows.append({'z_kpc': height, 'orders': outputs})
                values = [row['orders'][96]['gR_kms2_per_kpc'] for row in rows]
                extrapolated = [2*values[i+1]-values[i] for i in (0, 1)]
                check(f'height_extrapolation:{model}:{radius}', relative(extrapolated[0], extrapolated[1]), 1e-3)
                check(f'galaxy_force_tail:{model}:{radius}', rows[-1]['orders'][96]['force_tail_bound_kms2_per_kpc']/max(1.,abs(extrapolated[1])), 1e-10)
                slope = 2*math.pi*G*surface_slope(radius, components)
                cases.append({'model': model, 'hi_tail': hi_tail, 'h2_tail': h2_tail,
                              'R_kpc': radius, 'component_masses_Msun': masses,
                              'total_mass_Msun': sum(masses.values()), 'heights': rows,
                              'extrapolated_gR_kms2_per_kpc': extrapolated,
                              'slope_corrected_gR_kms2_per_kpc': [v-slope*z for v,z in zip(values,heights)],
                              'predicted_dgR_dz_kms2_per_kpc2': slope})
    failed = [c for c in checks if not c['passed']]
    return {'status': 'COMPLETE' if not failed else 'FAILED_CHECKS',
            'checks': checks, 'failed_checks': failed, 'elliptic_controls': elliptic_rows,
            'ring_controls': ring_rows, 'kuzmin_controls': kuzmin_rows, 'cases': cases,
            'G_kpc_kms2_Msun': G, 'role': 'Newtonian modeled-source numerical qualification; no velocities',
            'seconds': time.perf_counter()-started,
            'peak_self_rss_bytes': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}


def source_hashes():
    names = ['RING_ORACLE_PROTOCOL.md', 'galaxy_ring_oracle.py', 'galaxy_density.py',
             'NGC3198_BARYON_INPUT.json', 'GALAXY_SOURCE_PREFLIGHT.md',
             'OUTER_GAS_INPUT_DECISION.md', 'begeman1989_original.pdf']
    ancestry = json.loads((ROOT/'NGC3198_BARYON_INPUT.json').read_text())['sources_sha256']
    for name, expected in ancestry.items():
        assert sha(ROOT/name) == expected, f'Input ancestor changed: {name}'
        names.append(name)
    return {name: sha(ROOT/name) for name in sorted(set(names))}


def main():
    freeze = ROOT/'RING_ORACLE_FROZEN.json'
    identity = {'files': source_hashes(), 'radii_kpc': list(RADII), 'orders': list(ORDERS),
                'models': [[a,b] for a in (False,True) for b in (False,True)]}
    if sys.argv[1:] == ['freeze']:
        save_new(freeze, identity)
        return
    assert not sys.argv[1:]
    assert json.loads(freeze.read_text()) == identity
    payload = calculate()
    save_new(ROOT/'RING_ORACLE_RESULTS.json', {'freeze_sha256': sha(freeze),
             'payload_sha256': hashlib.sha256(encoded(payload)).hexdigest(), 'payload': payload})
    print(json.dumps({'status': payload['status'], 'checks': len(payload['checks']),
                      'failed': len(payload['failed_checks']), 'cases': len(payload['cases']),
                      'seconds': payload['seconds'], 'peak_self_rss_bytes': payload['peak_self_rss_bytes']}))
    if payload['failed_checks']:
        raise SystemExit('Saved failed checks; do not retune or overwrite this result.')


if __name__ == '__main__':
    main()
