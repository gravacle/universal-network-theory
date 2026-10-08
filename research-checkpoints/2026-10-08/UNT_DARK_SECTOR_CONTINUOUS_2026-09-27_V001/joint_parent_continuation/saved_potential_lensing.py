"""Conditional lensing from twenty saved fields; no PDE or import-time run."""
import os
import sys
sys.dont_write_bytecode = True
for name in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS',
             'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[name] = '1'
import hashlib
import json
import math
import resource
import time
import numpy as np
from numpy.polynomial.legendre import leggauss
import disk_solver as law
import axisymmetric_disk_v002 as disk
import galaxy_density as density
import galaxy_field_compute as inherited

ROOT = law.ROOT
FREEZE = ROOT/'SAVED_POTENTIAL_LENSING_FROZEN.json'
RESULT = ROOT/'SAVED_POTENTIAL_LENSING_RESULTS.json'
RADII = (2.7, 8.7, 20.7, 35.7, 43.7)
JOBS = ((256, 255, False), (320, 1023, False), (512, 255, False), (512, 255, True))
CONTROL = 'ML36_CAL_HI1_H21_V001'
SPEED = 299792.458
FACTOR = 2*density.A0_KMS2_KPC/SPEED**2
ARCSEC = 180*3600/math.pi
EPS = np.finfo(float).eps


def authenticated(path, freeze_hash):
    record = json.loads(path.read_text())
    assert record['freeze_sha256'] == freeze_hash, path
    assert record['payload_sha256'] == hashlib.sha256(law.encode(record['payload'])).hexdigest(), path
    return record['payload']


def inputs():
    files, visited = {}, set()

    def add(path, expected=None):
        path = path.resolve()
        digest = law.sha(path)
        assert expected is None or digest == expected, path
        files[os.path.relpath(path, ROOT)] = digest
        return path

    def manifest(path):
        path = add(path)
        if path in visited:
            return
        visited.add(path)
        record = json.loads(path.read_text())
        for name, digest in record['files'].items():
            member = add(path.parent/name, digest)
            if member.name.endswith('_FROZEN.json'):
                manifest(member)

    for name in ('saved_potential_lensing.py', 'LENSING_NUMERICAL_CONTROLS.md',
                 'SAVED_POTENTIAL_LENSING_PROTOCOL.md', 'WEAK_FIELD_LENSING_PATHWAY.md',
                 'FULL_RESPONSE_PRESSURE.md'):
        add(ROOT/name)
    manifest(ROOT/'STELLAR_CALIBRATION_FROZEN.json')
    census = []
    for hi, h2 in ((True, True), (False, True), (True, False), (False, False)):
        for n, extent, newtonian in JOBS:
            census.append({'case': inherited.case_name(hi, h2, n, extent, newtonian),
                'freeze': 'GALAXY_FIELD_FROZEN.json', 'source': f'HI{int(hi)}_H2{int(h2)}',
                'hi_tail': hi, 'h2_tail': h2, 'stellar_multiplier': 1.,
                'N': n, 'extent': extent, 'newtonian': newtonian})
    control_final = authenticated(add(ROOT/'STELLAR_CALIBRATION_RESULTS.json'),
                                  law.sha(ROOT/'STELLAR_CALIBRATION_FROZEN.json'))
    assert control_final['status'] == 'COMPLETE' and control_final['model'] == CONTROL
    for n, extent, newtonian in JOBS:
        case = f'{CONTROL}_N{n}_L{extent}_Newton{int(newtonian)}'
        add(ROOT/(case+'.json'), control_final['case_files_sha256'][case+'.json'])
        census.append({'case': case, 'freeze': 'STELLAR_CALIBRATION_FROZEN.json', 'source': CONTROL,
            'hi_tail': True, 'h2_tail': True, 'stellar_multiplier': control_final['stellar_multiplier'],
            'N': n, 'extent': extent, 'newtonian': newtonian})
    assert len(census) == 20 and control_final['stellar_multiplier'] == 1.2567828155112788
    for row in census:
        path = add(ROOT/(row['case']+'.json'))
        p = authenticated(path, law.sha(ROOT/row['freeze']))
        assert p['case'] == row['case'] and all(p['checks'].values())
        assert all(p[key] == row[key] for key in ('N', 'extent', 'newtonian'))
        if row['source'] == CONTROL:
            assert p['model'] == CONTROL and p['stellar_multiplier'] == row['stellar_multiplier']
        else:
            assert (p['hi_tail'], p['h2_tail']) == (row['hi_tail'], row['h2_tail'])
    # Authenticate inherited numerical qualifications, not only opaque file hashes.
    for name in list(files):
        if name.startswith('stretched_V002_') and name.endswith('.json'):
            p = authenticated(ROOT/name, law.sha(ROOT/'STRETCHED_DISK_V002_FROZEN.json'))
            assert all(p['checks'].values())
    return census, dict(sorted(files.items()))


def ray_geometry(x, y, inclination, nodes):
    si = 0. if inclination == 0 else math.sin(math.radians(inclination))
    ci = 1. if inclination == 0 else math.cos(math.radians(inclination))
    extent = float(nodes[-1])
    assert 0 < math.hypot(x, y) < extent and ci > 0
    lo, hi = (-extent+y*si)/ci, (extent+y*si)/ci
    if si > 0:
        radial = math.sqrt(extent**2-x*x)
        lo, hi = max(lo, (-radial-y*ci)/si), min(hi, (radial-y*ci)/si)
    assert lo < hi
    crossings = [lo, hi]
    for z in nodes:
        crossings.extend(((z+y*si)/ci, (-z+y*si)/ci))
    if si > 0:
        for radius in nodes:
            if radius >= abs(x):
                root = math.sqrt(max(0., radius*radius-x*x))
                crossings.extend(((root-y*ci)/si, (-root-y*ci)/si))
    tolerance = 64*EPS*max(1., abs(lo), abs(hi))
    cuts = [lo]
    for value in sorted(v for v in crossings if lo < v < hi):
        if value-cuts[-1] > tolerance and hi-value > tolerance:
            cuts.append(value)
    cuts.append(hi)
    left, right = np.array(cuts[:-1]), np.array(cuts[1:])
    mid = (left+right)/2
    yd, zd = y*ci+mid*si, -y*si+mid*ci
    ir = np.searchsorted(nodes, np.hypot(x, yd), side='right')-1
    iz = np.searchsorted(nodes, abs(zd), side='right')-1
    assert np.all((ir >= 0)&(ir < len(nodes)-1)&(iz >= 0)&(iz < len(nodes)-1))
    assert not np.any((ir == 0)&(iz == 0)), 'Ray needs the deliberately undefined origin corner.'
    corners = {(int(i+a), int(j+b)) for i, j in zip(ir, iz) for a in (0, 1) for b in (0, 1)}
    return {'X': x, 'Y': y, 'inclination': inclination, 'si': si, 'ci': ci,
            'lo': lo, 'hi': hi, 'left': left, 'right': right, 'ir': ir, 'iz': iz, 'corners': corners}


def reference_nodes(phi, centers, extent, q, newtonian, needed):
    """Evaluate only positive-center dependencies, never a dense mesh×quadrature."""
    nodes = np.r_[0., centers, extent]
    outer, physical = len(nodes)-1, set()

    def dependencies(i, j):
        if i == outer or j == outer:
            return
        assert (i, j) != (0, 0)
        if i == 0:
            dependencies(1, j)
            dependencies(2, j)
        elif j == 0:
            dependencies(i, 1)
            dependencies(i, 2)
        else:
            physical.add((i, j))

    for i, j in needed:
        dependencies(i, j)
    keys = sorted(physical)
    radii = np.array([math.hypot(nodes[i], nodes[j]) for i, j in keys])
    references, residuals = {}, {}
    for order in (64, 128):
        values = np.concatenate([disk.spherical_potential(radii[a:a+512], q, order=order, newtonian=newtonian)
                                 for a in range(0, len(radii), 512)])
        references[order] = values
        cache = {key: float(phi[key[0]-1, key[1]-1]-value) for key, value in zip(keys, values)}

        def residual(i, j):
            if (i, j) in cache:
                return cache[i, j]
            if i == outer or j == outer:
                value = 0.
            elif i == 0:
                assert j != 0
                a, b = nodes[1]**2, nodes[2]**2
                value = residual(1, j)-a*(residual(2, j)-residual(1, j))/(b-a)
            elif j == 0:
                value = residual(i, 1)-nodes[1]*(residual(i, 2)-residual(i, 1))/(nodes[2]-nodes[1])
            else:
                raise AssertionError('Unplanned reference node')
            cache[i, j] = value
            return value

        residuals[order] = {key: residual(*key) for key in needed}
    relative = abs(references[64]-references[128])/np.maximum(1., abs(references[128]))
    worst = int(np.argmax(relative))
    return residuals, {'positive_saved_center_count': len(keys), 'requested_corner_count': len(needed),
                      'maximum_batch_size': min(512, len(keys)),
                      'potential_64_128_max_scaled_difference': float(relative[worst]),
                      'worst_node_indices': list(keys[worst]), 'worst_radius_kpc': float(radii[worst])}


def integrate_correction(ray, nodes, residuals, order):
    x, y, si, ci = (ray[key] for key in ('X', 'Y', 'si', 'ci'))
    ir, iz = ray['ir'], ray['iz']
    values = np.array([[residuals[int(i+a), int(j+b)] for a, b in ((0, 0), (1, 0), (0, 1), (1, 1))]
                       for i, j in zip(ir, iz)])
    v00, v10, v01, v11 = (values[:, i, None] for i in range(4))
    gx, gw = leggauss(order)
    half, mid = (ray['right']-ray['left'])/2, (ray['right']+ray['left'])/2
    ell = mid[:, None]+half[:, None]*gx
    weights = half[:, None]*gw
    yd, zd = y*ci+ell*si, -y*si+ell*ci
    s, z = x*x+yd*yd, abs(zd)
    ds, dz = (nodes[ir+1]**2-nodes[ir]**2)[:, None], (nodes[iz+1]-nodes[iz])[:, None]
    u, v = (s-nodes[ir, None]**2)/ds, (z-nodes[iz, None])/dz
    assert np.all((u >= -1e-9)&(u <= 1+1e-9)&(v >= -1e-9)&(v <= 1+1e-9))
    derivative_s = ((v10-v00)*(1-v)+(v11-v01)*v)/ds
    derivative_z = ((v01-v00)*(1-u)+(v11-v10)*u)/dz
    sky = (2*x*derivative_s,
           2*yd*ci*derivative_s-np.sign(zd)*si*derivative_z)
    scale_s = ((abs(v10)+abs(v00))*abs(1-v)+(abs(v11)+abs(v01))*abs(v))/ds
    scale_z = ((abs(v01)+abs(v00))*abs(1-u)+(abs(v11)+abs(v10))*abs(u))/dz
    scales = (2*abs(x)*scale_s, 2*abs(yd*ci)*scale_s+abs(si)*scale_z)
    return (np.array([math.fsum((weights*value).ravel()) for value in sky]),
            np.array([math.fsum((weights*value).ravel()) for value in scales]))


def faceon_trapezoid(b, nodes, residuals):
    i = int(np.searchsorted(nodes, b, side='right')-1)
    ds = nodes[i+1]**2-nodes[i]**2
    low = np.array([residuals[i, j] for j in range(len(nodes))])
    high = np.array([residuals[i+1, j] for j in range(len(nodes))])
    derivative = 2*b*(high-low)/ds
    scale = 2*b*(abs(high)+abs(low))/ds
    widths = np.diff(nodes)
    return float(math.fsum(widths*(derivative[1:]+derivative[:-1]))), float(math.fsum(widths*(scale[1:]+scale[:-1])))


def angular_scalar(q, b, left, right, order, kind):
    gx, gw = leggauss(order)
    theta = (left+right)/2+(right-left)*gx/2
    weights = (right-left)*gw/2
    cosine = np.cos(theta)
    radius = b/cosine
    if kind == 'candidate':
        integrand = law.inverse(q/radius**2)/cosine
        endpoint = math.sqrt(q)/b
    elif kind == 'newtonian':
        integrand, endpoint = (q/radius**2)/cosine, 0.
    else:
        assert kind == 'deep'
        integrand, endpoint = (math.sqrt(q)/radius)/cosine, 0.
    offset = endpoint*(right-left)
    residual = weights*(integrand-endpoint)
    return math.fsum([offset, *residual]), abs(offset)+math.fsum(abs(residual))


def spherical_parts(ray, q, order, kind):
    b = math.hypot(ray['X'], ray['Y'])
    a, z = math.atan(ray['lo']/b), math.atan(ray['hi']/b)
    vector = np.array([ray['X'], ray['Y']])
    scalar, scale = {}, {}
    intervals = {'whole': (-math.pi/2, math.pi/2), 'interior': (a, z),
                 'left': (-math.pi/2, a), 'right': (z, math.pi/2)}
    for key, (lo, hi) in intervals.items():
        scalar[key], scale[key] = angular_scalar(q, b, lo, hi, order, kind)
    scalar['exterior'] = math.fsum((scalar['left'], scalar['right']))
    scale['exterior'] = scale['left']+scale['right']
    return ({key: vector*value for key, value in scalar.items()},
            {key: b*value for key, value in scale.items()}, scalar, (a, z))


def calculate_case(census, checks):
    started = time.perf_counter()
    p = authenticated(ROOT/(census['case']+'.json'), law.sha(ROOT/census['freeze']))
    _, centers, _ = disk.mesh(p['N'], p['extent'])
    assert np.array_equal(centers, np.array(p['radii']))
    phi = np.array(p['phi'], dtype=float)
    assert phi.shape == (p['N'], p['N']) and np.all(np.isfinite(phi))
    nodes = np.r_[0., centers, p['extent']]
    mass = sum(p['component_masses_Msun'].values())
    q = density.G_KPC_KMS2_MSUN*mass/density.A0_KMS2_KPC
    rays, needed = [], set()
    for b in RADII:
        for label, x, y, inclination in (('face_on', b, 0., 0.), ('major_72', b, 0., 72.), ('minor_72', 0., b, 72.)):
            positive = ray_geometry(x, y, inclination, nodes)
            negative = ray_geometry(-x, -y, inclination, nodes)
            rays.append((b, label, positive, negative))
            needed.update(positive['corners'] | negative['corners'])
    residual, reference_info = reference_nodes(phi, centers, p['extent'], q, p['newtonian'], needed)

    def check(label, error, tolerance, **extra):
        checks.append({'case': census['case'], 'name': label, 'error': float(error),
                       'tolerance': float(tolerance), 'passed': bool(math.isfinite(error) and error <= tolerance), **extra})

    check('spherical_reference_potential_64_128', reference_info['potential_64_128_max_scaled_difference'], 1e-9)
    components = density.profiles(census['hi_tail'], census['h2_tail'])
    stars = components['stars']
    components['stars'] = density.Profile(stars.r.copy(), census['stellar_multiplier']*stars.s, stars.tail)
    reconstructed_masses = density.masses(components)
    assert all(abs(reconstructed_masses[key]/p['component_masses_Msun'][key]-1) <= 1e-13 for key in reconstructed_masses)
    rows = []
    for b, label, ray, mirror in rays:
        tag = f'{label}:{b}'
        two, scale_two = integrate_correction(ray, nodes, residual[64], 2)
        four, scale_four = integrate_correction(ray, nodes, residual[64], 4)
        reverse, scale_reverse = integrate_correction(mirror, nodes, residual[64], 2)
        doubled, _ = integrate_correction(ray, nodes, residual[128], 2)
        for axis in (0, 1):
            check(tag+f':exact_segment:{axis}', abs(two[axis]-four[axis]), 4096*EPS*max(1., scale_two[axis]+scale_four[axis]))
            check(tag+f':parity:{axis}', abs(two[axis]+reverse[axis]), 4096*EPS*max(1., scale_two[axis]+scale_reverse[axis]))
        cross = 0 if label == 'minor_72' else 1
        check(tag+':cross_axis', abs(two[cross]), 4096*EPS*max(1., scale_two[cross]))
        trapezoid = None
        if label == 'face_on':
            trap, scale_trap = faceon_trapezoid(b, nodes, residual[64])
            check(tag+':faceon_trapezoid', abs(two[0]-trap), 4096*EPS*max(1., scale_two[0]+scale_trap))
            trapezoid = {'raw_integral': trap, 'cancellation_scale': scale_trap}
        kind = 'newtonian' if p['newtonian'] else 'candidate'
        spheres = {order: spherical_parts(ray, q, order, kind) for order in (64, 128)}
        sphere, sphere_scale, _, angles = spheres[128]
        for part in ('whole', 'interior', 'exterior'):
            denominator = max(1., float(np.linalg.norm(sphere['whole'])), sphere_scale[part])
            check(tag+':sphere_quadrature:'+part, float(np.max(abs(spheres[64][0][part]-sphere[part]))), 1e-8*denominator)
        decomposition = sphere['interior']+sphere['exterior']
        check(tag+':sphere_whole_vs_pieces', float(np.max(abs(sphere['whole']-decomposition))),
              1e-8*max(1., float(np.linalg.norm(sphere['whole'])), sphere_scale['interior']+sphere_scale['exterior']))
        reference_effect = doubled-two
        check(tag+':reference_potential_effect', float(np.max(abs(reference_effect))),
              1e-7*max(1., float(np.linalg.norm(sphere['whole'])), float(np.linalg.norm(two))))
        # Direct quadrature of exact radial fields, not the candidate flux inverse.
        analytic_controls = {}
        for exact_kind in ('newtonian', 'deep'):
            theta_a, theta_z = angles
            full = 2*q/b**2 if exact_kind == 'newtonian' else math.pi*math.sqrt(q)/b
            inside = q/b**2*(math.sin(theta_z)-math.sin(theta_a)) if exact_kind == 'newtonian' else math.sqrt(q)/b*(theta_z-theta_a)
            exact = {'whole': full, 'interior': inside, 'exterior': full-inside}
            reports = {}
            for order in (64, 128):
                _, scales, scalars, _ = spherical_parts(ray, q, order, exact_kind)
                reports[str(order)] = {key: scalars[key] for key in exact}
                for part in exact:
                    check(tag+f':analytic_{exact_kind}:{order}:{part}', abs(scalars[part]-exact[part]),
                          512*EPS*max(1., abs(exact[part]), scales[part]/b))
            physical = FACTOR*b*full
            expected = 4*density.G_KPC_KMS2_MSUN*mass/(SPEED**2*b) if exact_kind == 'newtonian' else 2*math.pi*math.sqrt(density.G_KPC_KMS2_MSUN*mass*density.A0_KMS2_KPC)/SPEED**2
            check(tag+':physical_units_'+exact_kind, abs(physical-expected), 128*EPS*max(abs(expected), np.finfo(float).tiny))
            analytic_controls[exact_kind] = {'exact_scalar_integrals': exact, 'quadratures': reports, 'exact_whole_angle_rad': expected}
        pieces = {'spherical_interior': FACTOR*sphere['interior'],
                  'finite_box_correction': FACTOR*two, 'spherical_exterior': FACTOR*sphere['exterior']}
        total = np.array([math.fsum(piece[i] for piece in pieces.values()) for i in (0, 1)])
        check(tag+':angle_piece_closure', float(np.max(abs(total-FACTOR*(decomposition+two)))),
              128*EPS*max(float(sum(np.sum(abs(v)) for v in pieces.values())), np.finfo(float).tiny))
        projected = None
        if p['newtonian'] and label == 'face_on':
            enclosed = sum(float(2*math.pi*1e6*profile.integral(0., b)) for profile in components.values())
            expected = 4*density.G_KPC_KMS2_MSUN*enclosed/(SPEED**2*b)
            error = abs(total[0]/expected-1)
            check(tag+':newtonian_projected_mass', error, .01)
            projected = {'enclosed_baryonic_mass_Msun': enclosed, 'exact_angle_rad': expected,
                         'fractional_error': error, 'target': .01,
                         'scope': 'Combined interpolation/finite-box completion accuracy; not a data fit.'}
        rows.append({'R_kpc': b, 'projection': label, 'X_kpc': ray['X'], 'Y_kpc': ray['Y'],
            'inclination_deg': ray['inclination'], 'box_entry_exit_kpc': [ray['lo'], ray['hi']],
            'segment_count': len(ray['left']), 'pieces_rad': {k: v.tolist() for k, v in pieces.items()},
            'total_rad': total.tolist(), 'total_arcsec': (ARCSEC*total).tolist(),
            'whole_spherical_rad': (FACTOR*sphere['whole']).tolist(),
            'spherical_orders_raw': {str(order): {k: v.tolist() for k, v in spheres[order][0].items()} for order in (64, 128)},
            'correction_raw_orders': {'two': two.tolist(), 'four': four.tolist(), 'mirror_two': reverse.tolist(),
                                     'doubled_reference_two': doubled.tolist()},
            'correction_cancellation_scale': scale_two.tolist(),
            'reference_potential_effect_rad': (FACTOR*reference_effect).tolist(),
            'faceon_trapezoid': trapezoid, 'analytic_monopole_controls': analytic_controls,
            'newtonian_projected_mass': projected})
    del phi
    return {**census, 'total_mass_Msun': mass, 'q_kpc2': q, 'reference_nodes': reference_info,
            'rays': rows, 'seconds': time.perf_counter()-started}


def descriptive_comparisons(cases):
    by_case = {row['case']: row for row in cases}
    numerical, calibration = [], []
    for row in cases:
        if not row['newtonian'] and (row['N'] == 512 or row['extent'] == 1023):
            baseline = next(c for c in cases if c['source'] == row['source'] and (c['N'], c['extent'], c['newtonian']) == (256, 255, False))
            for current, old in zip(row['rays'], baseline['rays']):
                assert (current['R_kpc'], current['projection']) == (old['R_kpc'], old['projection'])
                change = np.array(current['total_rad'])-old['total_rad']
                numerical.append({'case': row['case'], 'baseline': baseline['case'],
                    'R_kpc': current['R_kpc'], 'projection': current['projection'],
                    'difference_rad': change.tolist(), 'fractional_vector_change': float(np.linalg.norm(change)/max(np.linalg.norm(current['total_rad']), np.finfo(float).tiny))})
        if row['source'] == CONTROL:
            original = by_case[inherited.case_name(True, True, row['N'], row['extent'], row['newtonian'])]
            for current, old in zip(row['rays'], original['rays']):
                assert (current['R_kpc'], current['projection']) == (old['R_kpc'], old['projection'])
                calibration.append({'case': row['case'], 'original': original['case'],
                    'R_kpc': current['R_kpc'], 'projection': current['projection'],
                    'difference_rad': (np.array(current['total_rad'])-old['total_rad']).tolist()})
    return {'mesh_and_domain_descriptive_only': numerical, 'fixed_stellar_calibration_changes': calibration}


def main():
    assert sys.argv[1:] in ([], ['freeze'])
    census, files = inputs()
    specification = {'files': files, 'case_census': census, 'radii_kpc': list(RADII),
                     'projections': ['face_on', 'major_72', 'minor_72'],
                     'c_kms': SPEED, 'r': law.RATIO, 'a0_kms2_kpc': density.A0_KMS2_KPC,
                     'reference_potential_orders': [64, 128], 'angular_orders': [64, 128],
                     'segment_orders': [2, 4], 'maximum_reference_batch': 512}
    if sys.argv[1:] == ['freeze']:
        law.save_new(FREEZE, specification)
        return
    assert json.loads(FREEZE.read_text()) == specification
    started = time.perf_counter()
    checks, cases = [], []
    for case in census:
        cases.append(calculate_case(case, checks))
        print(json.dumps({'completed_lensing_case': case['case'], 'rays': 15,
                          'seconds': cases[-1]['seconds']}), flush=True)
    failures = [row for row in checks if not row['passed']]
    payload = {'status': 'COMPLETE' if not failures else 'FAILED_NUMERICAL_CONTROLS',
        'role': 'Conditional aligned-clock weak-field physical bending; no observed lens fit or new PDE.',
        'cases': cases, 'checks': checks, 'failed_checks': failures,
        'comparisons': descriptive_comparisons(cases), 'seconds': time.perf_counter()-started,
        'peak_self_rss_bytes': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    law.save_new(RESULT, {'freeze_sha256': law.sha(FREEZE),
        'payload_sha256': hashlib.sha256(law.encode(payload)).hexdigest(), 'payload': payload})
    print(json.dumps({'status': payload['status'], 'cases': len(cases), 'rays': sum(len(c['rays']) for c in cases),
                      'checks': len(checks), 'failures': len(failures), 'seconds': payload['seconds']}), flush=True)
    if failures:
        raise SystemExit('All numerical failures preserved; no automatic retuning or overwrite.')


if __name__ == '__main__':
    main()
