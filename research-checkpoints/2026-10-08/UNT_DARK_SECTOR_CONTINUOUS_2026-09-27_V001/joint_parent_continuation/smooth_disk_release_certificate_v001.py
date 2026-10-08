"""Inert exact-bound release certificate. Root alone executes; stdout only."""
import sys
sys.dont_write_bytecode = True
import base64
import hashlib
import json
import math
from pathlib import Path
import resource
import time
import zlib

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
FREEZE = HERE / 'SMOOTH_DISK_RELEASE_CERTIFICATE_V001_FROZEN.json'
CONFIG = dict(spectrum_index=1, reference=0, gaps=[128, 8192],
    thickness_over_a=[1/8, 1/16], radial_witnesses=[0., .5, 1., 2.],
    vertical_witnesses=[0., .25, .5, 1.], a_kpc=3.2,
    parsec_m=3.085677581491367e16, c_m_s=299792458.,
    G_m3_kg_s2=6.67430e-11, beta=.005,
    fd_steps=[2**-10, 2**-11], arithmetic_tolerance=2e-11,
    fd_tolerance=1e-6, far_radius_over_a=1024.,
    far_angles=[0., math.pi/4, math.pi/2], expected_cases=4,
    expected_readouts=64)


def encode(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'),
                      allow_nan=False).encode()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inputs():
    files, seen = {}, set()

    def add(path, expected=None):
        path = path.resolve(strict=True)
        path.relative_to(ROOT)
        actual = sha(path)
        if expected is not None and actual != expected:
            raise RuntimeError('Changed input: ' + str(path))
        files[str(path.relative_to(ROOT))] = actual
        return path

    def manifest(path):
        path = add(path)
        if path in seen:
            return
        seen.add(path)
        for name, digest in json.loads(path.read_text())['files'].items():
            raw = Path(name)
            options = [raw] if raw.is_absolute() else [ROOT/raw, path.parent/raw]
            matches = {p.resolve() for p in options
                       if p.resolve().is_relative_to(ROOT) and p.is_file()}
            if len(matches) != 1:
                raise RuntimeError('Ambiguous ancestor: ' + name)
            child = add(matches.pop(), digest)
            if child.name.endswith('_FROZEN.json'):
                manifest(child)

    t = json.loads(add(HERE/'FINITE_GAP_SHARED_SCREEN_V002_TRANSPORT.json',
        '11d5898717488b1ab3fb75e3294e55e5674f2b3f2d623f15cc9bb2e9a54c4db4').read_text())
    inflater = zlib.decompressobj()
    raw = inflater.decompress(base64.b64decode(t['data'], validate=True)) + inflater.flush()
    if not inflater.eof or inflater.unused_data or inflater.unconsumed_tail:
        raise RuntimeError('Invalid saved transport')
    if len(raw) != t['raw_bytes'] or hashlib.sha256(raw).hexdigest() != t['raw_sha256']:
        raise RuntimeError('Changed saved payload')
    wrapper = json.loads(raw)
    old = wrapper['payload']
    ancestor = HERE/'FINITE_GAP_SHARED_SCREEN_V002_FROZEN.json'
    manifest(ancestor)
    if (wrapper['freeze_sha256'] != sha(ancestor) or
        wrapper['payload_sha256'] != hashlib.sha256(encode(old)).hexdigest()):
        raise RuntimeError('Invalid saved wrapper')
    if old['status'] != 'COMPLETE' or old['failures']:
        raise RuntimeError('Unqualified saved source')
    path = add(HERE/'GLOBAL_GAP_LIMIT_CALIBRATION_V001_RESULTS.json',
        '11e7c8e7d9119ef02177904e462e1959e5d554eed245000f8609530b5b64b628')
    global_wrapper = json.loads(path.read_text())
    global_data = global_wrapper['payload']
    if global_data['status'] != 'COMPLETE' or global_data['failures']:
        raise RuntimeError('Unqualified reference source')
    manifest(HERE/'GLOBAL_GAP_LIMIT_CALIBRATION_V001_FROZEN.json')
    if global_wrapper['payload_sha256'] != hashlib.sha256(encode(global_data)).hexdigest():
        raise RuntimeError('Changed reference wrapper')
    if global_wrapper['freeze_sha256'] != sha(HERE/'GLOBAL_GAP_LIMIT_CALIBRATION_V001_FROZEN.json'):
        raise RuntimeError('Changed reference freeze')
    for name, digest in [
        ('SMOOTH_DISK_CLOSED_RELEASE_ORACLES_V001.md',
         '5f5f2985167b47751aeceb78b823fb327aa58074b58e18a6d8856cd32bc7f7aa'),
        ('SMOOTH_RELEASE_CURRENT_BOUND_ADDENDUM_V001.md', None),
        ('SMOOTH_DISK_RELEASE_CERTIFICATE_PROTOCOL_V001.md', None),
        (Path(__file__).name, None)]:
        add(HERE/name, digest)
    selected = [row for row in old['rows']
                if row['spectrum_index'] == CONFIG['spectrum_index']
                and row['reference'] == CONFIG['reference']
                and row['R'] in CONFIG['gaps']]
    if len(selected) != 2 or {row['R'] for row in selected} != set(CONFIG['gaps']):
        raise RuntimeError('Changed selected state census')
    return selected, global_data, dict(configuration=CONFIG, files=files)


class Jet:
    """Two-coordinate value/gradient/Hessian arithmetic, not a field solve."""
    def __init__(self, value, gradient=(0., 0.), hessian=((0., 0.), (0., 0.))):
        self.v = float(value)
        self.g = tuple(gradient)
        self.h = tuple(tuple(row) for row in hessian)

    @staticmethod
    def cast(value):
        return value if isinstance(value, Jet) else Jet(value)

    def __add__(self, other):
        other = Jet.cast(other)
        return Jet(self.v+other.v, [self.g[i]+other.g[i] for i in range(2)],
                   [[self.h[i][j]+other.h[i][j] for j in range(2)] for i in range(2)])
    __radd__ = __add__

    def __neg__(self):
        return self * -1.

    def __sub__(self, other):
        return self + -Jet.cast(other)

    def __rsub__(self, other):
        return Jet.cast(other) + -self

    def __mul__(self, other):
        other = Jet.cast(other)
        return Jet(self.v*other.v,
            [self.g[i]*other.v+self.v*other.g[i] for i in range(2)],
            [[self.h[i][j]*other.v+self.v*other.h[i][j]
              +self.g[i]*other.g[j]+self.g[j]*other.g[i]
              for j in range(2)] for i in range(2)])
    __rmul__ = __mul__

    def __pow__(self, power):
        # All noninteger powers in the source have strictly positive bases.
        v = self.v**power
        d1 = power*self.v**(power-1) if power else 0.
        d2 = power*(power-1)*self.v**(power-2) if power not in (0, 1) else 0.
        return Jet(v, [d1*g for g in self.g],
                   [[d1*self.h[i][j]+d2*self.g[i]*self.g[j]
                     for j in range(2)] for i in range(2)])

    def __truediv__(self, other):
        return self * Jet.cast(other)**-1

    def __rtruediv__(self, other):
        return Jet.cast(other) * self**-1


def source(x, z, b):
    """Dimensionless potential phi/(GM/a), density D/(M/a^3)."""
    zz = (z*z+b*b)**.5
    aa = 1+zz
    dd2 = x*x+aa*aa
    potential = -dd2**-.5
    density = (b*b/(4*math.pi)) * (x*x+(1+3*zz)*aa*aa)/(zz**3*dd2**2.5)
    return potential, density


def analytic_potential(x, z, b):
    zz = math.sqrt(z*z+b*b)
    aa = 1+zz
    d2 = x*x+aa*aa
    d = math.sqrt(d2)
    w = [x, 0., aa*z/zz]
    diagonal = [1., 1., 1+b*b/zz**3]
    gradient = [w[0]/d**3, w[2]/d**3]
    hessian = [[(diagonal[i] if i == j else 0.)/d**3
                -3*w[i]*w[j]/d**5 for j in range(3)] for i in range(3)]
    return -1/d, gradient, hessian


def fd4(function, x, z, step):
    center = function(x, z)
    gradient, diagonal = [], []
    for direction in (0, 1):
        values = []
        for offset in (-2, -1, 1, 2):
            values.append(function(x+offset*step*(direction == 0),
                                   z+offset*step*(direction == 1)))
        fm2, fm1, fp1, fp2 = values
        gradient.append((fm2-8*fm1+8*fp1-fp2)/(12*step))
        diagonal.append((-fm2+16*fm1-30*center+16*fp1-fp2)/(12*step*step))
    offsets, weights = (-2, -1, 1, 2), (1., -8., 8., -1.)
    mixed = math.fsum(wi*wj*function(x+oi*step, z+oj*step)
        for oi, wi in zip(offsets, weights) for oj, wj in zip(offsets, weights))/(144*step*step)
    return gradient, [[diagonal[0], mixed], [mixed, diagonal[1]]]


def run(selected, global_data):
    start = time.perf_counter()
    failures, count, worst = [], 0, {}

    def check(name, actual, expected, scale=1., tolerance=None):
        nonlocal count
        count += 1
        tolerance = CONFIG['arithmetic_tolerance'] if tolerance is None else tolerance
        denom = max(abs(actual), abs(expected), abs(scale), 1e-300)
        error = abs(actual-expected)/denom
        worst[name] = max(worst.get(name, 0.), error)
        if not math.isfinite(error) or error > tolerance:
            failures.append(dict(check=name, actual=actual, expected=expected,
                                 scale=denom, error=error, tolerance=tolerance))

    def require(name, condition):
        check(name, float(bool(condition)), 1.)

    # Independent elementary polynomial and fractional-chain-rule checks.
    xj, zj = Jet(2., (1., 0.)), Jet(3., (0., 1.))
    poly = xj*xj*zj+zj**3
    check('jet_value', poly.v, 39.)
    for i, expected in enumerate((12., 31.)):
        check('jet_gradient', poly.g[i], expected)
    for i, row in enumerate(((6., 4.), (4., 18.))):
        for j, expected in enumerate(row):
            check('jet_hessian', poly.h[i][j], expected)
    reciprocal = ((xj*xj+zj*zj)**.5)**-2
    check('jet_fractional_value', reciprocal.v, 1/13)
    for i, value in enumerate((2., 3.)):
        check('jet_fractional_gradient', reciprocal.g[i], -2*value/13**2)
        for j, value2 in enumerate((2., 3.)):
            check('jet_fractional_hessian', reciprocal.h[i][j],
                  8*value*value2/13**3-(2/13**2 if i == j else 0.))

    geometries = []
    for b in CONFIG['thickness_over_a']:
        points, far = [], []
        dmax = (1+3*b)/(4*math.pi*b*(1+b)**3)
        bound = 1/(b*(1+b)**2)
        for x in CONFIG['radial_witnesses']:
            for z in CONFIG['vertical_witnesses']:
                pj, dj = source(Jet(x, (1., 0.)), Jet(z, (0., 1.)), b)
                pv, grad, hess = analytic_potential(x, z, b)
                check('potential_value', pj.v, pv)
                for i, index in enumerate((0, 2)):
                    check('potential_gradient', pj.g[i], grad[i])
                    for j, index2 in enumerate((0, 2)):
                        check('potential_hessian', pj.h[i][j], hess[index][index2], bound)
                lap = dj.h[0][0]+dj.h[1][1]+(dj.g[0]/x if x else dj.h[0][0])
                trace = math.fsum(hess[i][i] for i in range(3))
                check('source_poisson', trace, 4*math.pi*dj.v, bound)
                check('cylindrical_hessian', hess[1][1], grad[0]/x if x else pj.h[0][0])
                require('source_positive', dj.v > 0)
                require('density_max_bound', dj.v <= dmax*(1+2e-14))
                eig_center = (hess[0][0]+hess[2][2])/2
                eig_radius = math.hypot((hess[0][0]-hess[2][2])/2, hess[0][2])
                norm = max(abs(eig_center-eig_radius), abs(eig_center+eig_radius), abs(hess[1][1]))
                require('tidal_global_bound', norm <= bound*(1+2e-14))
                fd_rows = []
                for step in CONFIG['fd_steps']:
                    for which, jet in enumerate((pj, dj)):
                        fg, fh = fd4(lambda xx, zz: source(xx, zz, b)[which], x, z, step)
                        gs = 1. if which == 0 else dmax/b
                        hs = bound if which == 0 else dmax/(b*b)
                        ge = max(abs(fg[i]-jet.g[i])/max(gs, abs(jet.g[i])) for i in range(2))
                        he = max(abs(fh[i][j]-jet.h[i][j])/max(hs, abs(jet.h[i][j]))
                                 for i in range(2) for j in range(2))
                        check('fd_gradient', ge, 0., 1., CONFIG['fd_tolerance'])
                        check('fd_hessian', he, 0., 1., CONFIG['fd_tolerance'])
                        fd_rows.append(dict(field=['potential', 'density'][which], step=step,
                            gradient=fg, hessian=fh, gradient_scaled_error=ge,
                            hessian_scaled_error=he, gradient_scale=gs, hessian_scale=hs))
                points.append(dict(x=x, z=z, potential=pv, potential_gradient=grad,
                    potential_hessian=hess, density=dj.v, density_gradient=list(dj.g),
                    density_hessian=[list(row) for row in dj.h], density_laplacian=lap,
                    potential_laplacian=trace, tidal_norm=norm, fd=fd_rows))
        check('central_density', points[0]['density'], dmax)
        check('central_vertical_curvature', points[0]['potential_hessian'][2][2], bound)
        radius = CONFIG['far_radius_over_a']
        for angle in CONFIG['far_angles']:
            x, z = radius*math.cos(angle), radius*math.sin(angle)
            _, gradient, _ = analytic_potential(x, z, b)
            flux = radius*(x*gradient[0]+z*gradient[1])
            lower, upper = (radius/(radius+1+b))**3, 1+1/radius
            require('asymptotic_mass_flux_bound', lower <= flux <= upper)
            far.append(dict(radius=radius, angle=angle, normalized_radial_flux=flux,
                            lower=lower, upper=upper))
        geometries.append(dict(b_over_a=b, density_max=dmax, tidal_bound=bound,
            asymptotic_mass_coefficient=1., finite_radius_mass_flux_controls=far, points=points))

    c, G = CONFIG['c_m_s'], CONFIG['G_m3_kg_s2']
    a = CONFIG['a_kpc']*1000*CONFIG['parsec_m']
    ref = global_data['references'][CONFIG['reference']]
    spec = global_data['spectra'][CONFIG['spectrum_index']]['spectrum']
    kb = math.fsum(spec['weights'])+CONFIG['beta']
    cases = []
    for state in selected:
        gs = state['gstar']
        ci = state['I']*state['eII']/state['omega']
        check('same_state_sound_speed', ci, state['cI2'], 1e-300)
        check('same_state_action_pressure', CONFIG['beta']*state['I']*state['omega'],
              state['E']+state['pressure'])
        check('same_state_pressure_ratio', state['pressure']/state['E'], state['w'], 1e-300)
        check('same_state_vacuum', state['DeltaU'],
              state['E']*ref['Omega_Lambda']/ref['Omega_exc'])
        require('causal_intrinsic_sound', 0 < ci < 1/3)
        cs2 = c*c*ci
        stress_scale = gs*gs/(4*math.pi*G*kb)
        rho_h = stress_scale*state['E']/(c*c)
        pressure_h = stress_scale*state['pressure']
        vacuum_energy = stress_scale*state['DeltaU']
        GM, mass = gs*a*a, gs*a*a/G
        check('cosmic_excitation_normalization', rho_h,
              3*ref['H0_s_inverse']**2*ref['Omega_exc']/(8*math.pi*G), 1e-300)
        check('cosmic_vacuum_normalization', vacuum_energy/(c*c),
              3*ref['H0_s_inverse']**2*ref['Omega_Lambda']/(8*math.pi*G), 1e-300)
        for gi, geometry in enumerate(geometries):
            bb = geometry['b_over_a']
            b = a*bb
            U = GM/(2*c*c*(a+b))
            dmax = mass/a**3*geometry['density_max']
            ell0 = (mass/(2*math.pi*dmax))**(1/3)
            Bpsi = 3*math.pi*G*dmax*ell0/(c*c)
            check('gradient_split_stationarity', mass/ell0**2,
                  2*math.pi*dmax*ell0, 1e-300)
            require('contraction_domain', 0 < U < 1)
            tide = GM/a**3*geometry['tidal_bound']
            output_points = []
            for point in geometry['points']:
                D = mass/a**3*point['density']
                dgrad = [mass/a**4*v for v in point['density_gradient']]
                dnorm = math.hypot(*dgrad)
                dlap = mass/a**5*point['density_laplacian']
                potential = GM/a*point['potential']
                u = -potential/(2*c*c)
                psi_lo, psi_hi = 1+u/(1+U), 1+u
                require('metric_bracket_order', 1 <= psi_lo <= psi_hi <= 1+U*(1+2e-14))
                Af = 4*math.pi*G*D
                Alo, Ahi = Af/psi_hi**6, Af
                Agrad = [4*math.pi*G*v for v in dgrad]
                Alap = 4*math.pi*G*dlap
                grad_error = 4*math.pi*G*(8*U*dnorm+6*D*Bpsi)
                lap_error = 4*math.pi*G*(10*U*abs(dlap)+10*Bpsi*dnorm
                             +30*D*Bpsi*Bpsi+12*math.pi*G*D*D/(c*c))
                v3 = [-cs2*v/6 for v in Agrad]
                v3_error = cs2*grad_error/6
                current4 = cs2*Alap/24
                current4_error = cs2*lap_error/24
                density2 = [rho_h*(1+state['w'])*bound/2 for bound in (Alo, Ahi)]
                pressure2 = [cs2*v for v in density2]
                # Exact Hamiltonian residual for the explicit first iterate, not zero.
                lap_psi1 = -2*math.pi*G*D/(c*c)
                constraint_rhs = 2*math.pi*G*D/(c*c*psi_hi)
                defect = -lap_psi1-constraint_rhs
                stable_defect = 2*math.pi*G*D/(c*c)*u/(1+u)
                check('first_iterate_constraint_residual', defect, stable_defect,
                      2*math.pi*G*D/(c*c))
                check('same_state_pressure_jet', pressure2[1], cs2*density2[1], 1e-300)
                output_points.append(dict(x=point['x'], z=point['z'], D_kg_m3=D,
                    potential_m2_s2=potential,
                    potential_gradient_m_s2=[GM/a**2*v for v in point['potential_gradient']],
                    potential_hessian_s2=[[GM/a**3*v for v in row] for row in point['potential_hessian']],
                    psi_lower=psi_lo, psi_upper=psi_hi,
                    focusing_s2_interval=[Alo, Ahi], fractional_density_tau2_interval=[Alo/2, Ahi/2],
                    hard_density_tau2_kg_m3_s2_interval=density2,
                    hard_pressure_tau2_Pa_s2_interval=pressure2,
                    focusing_gradient_flat_s2_m1=Agrad,
                    focusing_gradient_error_bound_s2_m1=grad_error,
                    focusing_laplacian_flat_s2_m2=Alap,
                    focusing_laplacian_error_bound_s2_m2=lap_error,
                    orthonormal_velocity_tau3_m_s4_leading=v3,
                    orthonormal_velocity_tau3_norm_error_m_s4=v3_error,
                    canonical_current_tau4_s4_leading=current4,
                    canonical_current_tau4_s4_interval=[current4-current4_error, current4+current4_error],
                    first_metric_iterate_constraint_residual_m2=stable_defect))
            cases.append(dict(gap=state['R'], geometry_index=gi,
                role='old retained method control; not newly qualified joint candidate',
                source_state={key: state[key] for key in ('I','omega','eII','E','pressure','w','cI2','gstar','S','DeltaU')},
                Kb=kb, hard_weight=CONFIG['beta'], a_m=a, b_m=b, GM_m3_s2=GM,
                rest_mass_kg=mass, hard_mass_density_kg_m3=rho_h,
                hard_pressure_Pa=pressure_h, vacuum_energy_J_m3=vacuum_energy,
                background_H_s_inverse=ref['H0_s_inverse'], intrinsic_cs2_m2_s2=cs2,
                compactness_U=U, contraction_factor_upper=U,
                first_metric_iterate_uniform_error_upper=U*U,
                Dmax_kg_m3=dmax, green_split_radius_m=ell0,
                metric_gradient_bound_m_inverse=Bpsi,
                frozen_source_tidal_bound_s2=tide,
                frozen_source_rest_caustic_sufficient_seconds=math.acosh(2)/math.sqrt(tide),
                frozen_source_central_vertical_caustic_seconds=math.pi/(2*math.sqrt(tide)),
                actual_interval_caustic_status='not evaluated; initial bound is not an interval bound',
                momentum_constraint='exactly zero by CMC/comoving initial data',
                points=output_points))
    check('point_mass_vacuum_tau4_coefficient', ((-2)**2+1+1)/12, .5)
    check('case_census', len(cases), CONFIG['expected_cases'])
    check('readout_census', sum(len(case['points']) for case in cases), CONFIG['expected_readouts'])
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform == 'darwin' else 1024)
    return dict(status='COMPLETE' if not failures else 'FAILED_CHECKS', configuration=CONFIG,
        checks=count, failures=failures, worst_scaled_errors=worst,
        reference=ref, geometries=geometries, cases=cases,
        scope='Exact initial constraint/jet bounds only; no reconstructed metric, finite-time evolution, orbit, halo fit or abundance requalification.',
        derivative_method='Analytical two-variable chain-rule jets; independent fourth-order finite differences at both fixed steps.',
        mass_normalization='Exact asymptotic Poisson flux; finite-radius flux bounds retained as controls, not a truncated mass integral.',
        elapsed_seconds=time.perf_counter()-start, peak_bytes=peak)


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ('freeze', 'run'):
        raise RuntimeError('Usage: smooth_disk_release_certificate_v001.py freeze|run')
    selected, global_data, snapshot = inputs()
    if sys.argv[1] == 'freeze':
        print(encode(snapshot).decode())
        return
    if json.loads(FREEZE.read_text()) != snapshot:
        raise RuntimeError('Freeze differs from current sources')
    payload = run(selected, global_data)
    print(encode(dict(payload=payload, payload_sha256=hashlib.sha256(encode(payload)).hexdigest(),
                      freeze_sha256=sha(FREEZE))).decode())


if __name__ == '__main__':
    main()
