"""Additive cubic-in-R^2 lensing repair; no execution or monkey-patching at import."""
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
import saved_potential_lensing as old

ROOT, EPS, FACTOR = old.ROOT, old.EPS, old.FACTOR
FREEZE = ROOT/'SAVED_POTENTIAL_LENSING_V002_FROZEN.json'
RESULT = ROOT/'SAVED_POTENTIAL_LENSING_V002_RESULTS.json'


def stencil(interval, node_count):
    start = np.clip(np.asarray(interval, dtype=int)-1, 0, node_count-4)
    return start[..., None]+np.arange(4)


def basis(squared_nodes, points):
    """Batched local-normalized four-node basis and derivatives with respect to s."""
    squared_nodes = np.asarray(squared_nodes, dtype=float)
    points = np.asarray(points, dtype=float)
    assert squared_nodes.ndim == points.ndim == 2 and squared_nodes.shape[1] == 4
    span = squared_nodes[:, -1]-squared_nodes[:, 0]
    assert np.all(span > 0)
    knots = (squared_nodes-squared_nodes[:, :1])/span[:, None]
    t = (points-squared_nodes[:, :1])/span[:, None]
    weights = np.ones(points.shape+(4,))
    derivative = np.zeros_like(weights)
    for j in range(4):
        others = [m for m in range(4) if m != j]
        for m in others:
            weights[:, :, j] *= (t-knots[:, m, None])/(knots[:, j, None]-knots[:, m, None])
        for a in others:
            term = np.ones_like(t)/(knots[:, j, None]-knots[:, a, None])
            for m in others:
                if m != a:
                    term *= (t-knots[:, m, None])/(knots[:, j, None]-knots[:, m, None])
            derivative[:, :, j] += term/span[:, None]
    return weights, derivative


def ray_geometry(x, y, inclination, nodes):
    ray = old.ray_geometry(x, y, inclination, nodes)
    radial = stencil(ray['ir'], len(nodes))
    ray['stencil'] = radial
    ray['corners'] = {(int(i), int(j+b)) for indices, j in zip(radial, ray['iz'])
                      for i in indices for b in (0, 1)}
    assert (0, 0) not in ray['corners'], 'Cubic stencil needs the undefined origin corner.'
    return ray


def integrate_correction(ray, nodes, residuals, order):
    x, y, si, ci = (ray[key] for key in ('X', 'Y', 'si', 'ci'))
    radial, iz = ray['stencil'], ray['iz']
    lower = np.array([[residuals[int(i), int(j)] for i in indices] for indices, j in zip(radial, iz)])
    upper = np.array([[residuals[int(i), int(j+1)] for i in indices] for indices, j in zip(radial, iz)])
    gx, gw = leggauss(order)
    half, mid = (ray['right']-ray['left'])/2, (ray['right']+ray['left'])/2
    ell, quadrature = mid[:, None]+half[:, None]*gx, half[:, None]*gw
    yd, zd = y*ci+ell*si, -y*si+ell*ci
    s, z = x*x+yd*yd, abs(zd)
    weights, derivative = basis(nodes[radial]**2, s)
    dz = (nodes[iz+1]-nodes[iz])[:, None]
    v = (z-nodes[iz, None])/dz
    assert np.all((v >= -1e-9)&(v <= 1+1e-9))
    low_s = np.sum(derivative*lower[:, None, :], axis=2)
    high_s = np.sum(derivative*upper[:, None, :], axis=2)
    derivative_s = (1-v)*low_s+v*high_s
    derivative_z = np.sum(weights*(upper-lower)[:, None, :], axis=2)/dz
    gradients = (2*x*derivative_s, 2*yd*ci*derivative_s-np.sign(zd)*si*derivative_z)
    scale_s = np.sum(abs(derivative)*(abs(1-v)[:, :, None]*abs(lower[:, None, :])
                                      +abs(v)[:, :, None]*abs(upper[:, None, :])), axis=2)
    scale_z = np.sum(abs(weights)*(abs(lower)+abs(upper))[:, None, :], axis=2)/dz
    scales = (2*abs(x)*scale_s, 2*abs(yd*ci)*scale_s+abs(si)*scale_z)
    return (np.array([math.fsum((quadrature*g).ravel()) for g in gradients]),
            np.array([math.fsum((quadrature*g).ravel()) for g in scales]))


def faceon_trapezoid(b, nodes, residuals):
    interval = int(np.searchsorted(nodes, b, side='right')-1)
    indices = stencil(np.array([interval]), len(nodes))
    _, derivative = basis(nodes[indices]**2, np.array([[b*b]]))
    derivative = derivative[0, 0]
    values = np.array([[residuals[int(i), j] for i in indices[0]] for j in range(len(nodes))])
    gradient = 2*b*np.sum(values*derivative, axis=1)
    scale = 2*b*np.sum(abs(values*derivative), axis=1)
    dz = np.diff(nodes)
    return float(math.fsum(dz*(gradient[1:]+gradient[:-1]))), float(math.fsum(dz*(scale[1:]+scale[:-1])))


def synthetic_controls():
    checks = []
    _, centers, _ = old.disk.mesh(12, 16.)
    nodes = np.r_[0., centers, 16.]
    length, squared = 16., 256.

    def check(name, error, tolerance):
        checks.append({'case': 'synthetic_cubic', 'name': name, 'error': float(error),
                       'tolerance': float(tolerance), 'passed': bool(math.isfinite(error) and error <= tolerance)})

    intervals = np.arange(len(nodes)-1)
    indices = stencil(intervals, len(nodes))
    points = nodes[:-1, None]**2+np.diff(nodes**2)[:, None]*np.array([.17, .43, .81])
    weights, derivative = basis(nodes[indices]**2, points)
    for p in range(4):
        for q in (0, 1):
            radial_values = (nodes[indices]**2/squared)**p
            low, high = radial_values*.2**q, radial_values*.8**q
            v = (.37-.2)/.6
            interpolation = np.sum(weights*((1-v)*low+v*high)[:, None, :], axis=2)
            ds = np.sum(derivative*((1-v)*low+v*high)[:, None, :], axis=2)*squared
            dz = np.sum(weights*(high-low)[:, None, :], axis=2)/.6
            exact = (points/squared)**p*.37**q
            exact_ds = np.zeros_like(points) if p == 0 else p*(points/squared)**(p-1)*.37**q
            exact_dz = np.zeros_like(points) if q == 0 else (points/squared)**p
            for name, value, target, scale in (
                    ('value', interpolation, exact, np.sum(abs(weights*((1-v)*low+v*high)[:, None, :]), axis=2)),
                    ('ds', ds, exact_ds, squared*np.sum(abs(derivative*((1-v)*low+v*high)[:, None, :]), axis=2)),
                    ('dz', dz, exact_dz, np.sum(abs(weights)*(abs(low)+abs(high))[:, None, :], axis=2)/.6)):
                check(f'monomial:{p}:{q}:{name}', float(np.max(abs(value-target))), 1024*EPS*max(1., float(np.max(scale))))
            for b in (2.7, 8.7):
                for label, x, y, inc in (('face', b, 0., 0.), ('major', b, 0., 72.), ('minor', 0., b, 72.)):
                    ray = ray_geometry(x, y, inc, nodes)
                    values = {(i, j): (nodes[i]**2/squared)**p*(nodes[j]/length)**q for i, j in ray['corners']}
                    four, scale4 = integrate_correction(ray, nodes, values, 4)
                    eight, scale8 = integrate_correction(ray, nodes, values, 8)
                    gx, gw = leggauss(8)
                    half, mid = (ray['right']-ray['left'])/2, (ray['right']+ray['left'])/2
                    ell, qw = mid[:, None]+half[:, None]*gx, half[:, None]*gw
                    yd, zd = y*ray['ci']+ell*ray['si'], -y*ray['si']+ell*ray['ci']
                    ss, zz = (x*x+yd*yd)/squared, abs(zd)/length
                    exact_s = np.zeros_like(ss) if p == 0 else p*ss**(p-1)*zz**q/squared
                    exact_z = np.zeros_like(ss) if q == 0 else ss**p/length
                    gradients = (2*x*exact_s, 2*yd*ray['ci']*exact_s-np.sign(zd)*ray['si']*exact_z)
                    direct = np.array([math.fsum((qw*g).ravel()) for g in gradients])
                    for axis in (0, 1):
                        tolerance = 4096*EPS*max(1., scale4[axis]+scale8[axis])
                        check(f'monomial_ray:{p}:{q}:{b}:{label}:4vs8:{axis}', abs(four[axis]-eight[axis]), tolerance)
                        check(f'monomial_ray:{p}:{q}:{b}:{label}:analytic:{axis}', abs(four[axis]-direct[axis]), tolerance)
    arbitrary = np.sin(np.arange(len(nodes)))
    for j in range(len(nodes)):
        interval = min(j, len(nodes)-2)
        ii = stencil(np.array([interval]), len(nodes))
        w, _ = basis(nodes[ii]**2, np.array([[nodes[j]**2]]))
        value = float(np.dot(w[0, 0], arbitrary[ii[0]]))
        scale = float(np.dot(abs(w[0, 0]), abs(arbitrary[ii[0]])))
        check(f'nodal:{j}', abs(value-arbitrary[j]), 1024*EPS*max(1., scale))
        if 0 < j < len(nodes)-1:
            left = stencil(np.array([j-1]), len(nodes))
            wl, _ = basis(nodes[left]**2, np.array([[nodes[j]**2]]))
            other = float(np.dot(wl[0, 0], arbitrary[left[0]]))
            check(f'stencil_continuity:{j}', abs(other-value), 1024*EPS*max(1., scale))
    ii = stencil(np.array([len(nodes)-2]), len(nodes))
    w, _ = basis(nodes[ii]**2, np.array([[nodes[-1]**2]]))
    arbitrary[-1] = 0.
    check('outer_radial_zero', abs(float(np.dot(w[0, 0], arbitrary[ii[0]]))), 1024*EPS)
    check('outer_height_zero', float(np.max(abs(np.sum(weights*np.zeros_like(nodes[indices])[:, None, :], axis=2)))), 1024*EPS)
    for label, radius in (('original_origin', nodes[1]/2), ('expanded_origin_dependency', (nodes[1]+nodes[2])/2)):
        refused = False
        try:
            ray_geometry(radius, 0., 0., nodes)
        except AssertionError as error:
            refused = 'origin' in str(error)
        check(label, 0. if refused else 1., 0.)
    return checks


def inputs():
    census, files = old.inputs()
    first_freeze = json.loads(old.FREEZE.read_text())
    assert first_freeze['files'] == files and first_freeze['case_census'] == census
    previous = old.authenticated(old.RESULT, old.law.sha(old.FREEZE))
    assert previous['status'] == 'FAILED_NUMERICAL_CONTROLS' and len(previous['cases']) == 20
    assert len(previous['failed_checks']) == 5
    assert all(row['name'].endswith(':newtonian_projected_mass') for row in previous['failed_checks'])
    assert [row['case'] for row in previous['cases']] == [row['case'] for row in census]
    for path in (old.FREEZE, old.RESULT, ROOT/'saved_potential_lensing_v002.py',
                 ROOT/'SAVED_POTENTIAL_LENSING_V002_METHOD.md'):
        files[os.path.relpath(path, ROOT)] = old.law.sha(path)
    return census, dict(sorted(files.items())), previous


def calculate_case(census, before, inherited_checks, checks):
    started = time.perf_counter()
    p = old.authenticated(ROOT/(census['case']+'.json'), old.law.sha(ROOT/census['freeze']))
    _, centers, _ = old.disk.mesh(p['N'], p['extent'])
    assert np.array_equal(centers, np.array(p['radii']))
    phi = np.array(p['phi'], dtype=float)
    assert phi.shape == (p['N'], p['N']) and np.all(np.isfinite(phi))
    nodes = np.r_[0., centers, p['extent']]
    q = old.density.G_KPC_KMS2_MSUN*sum(p['component_masses_Msun'].values())/old.density.A0_KMS2_KPC
    assert q == before['q_kpc2']
    rays, needed = [], set()
    for row in before['rays']:
        ray = ray_geometry(row['X_kpc'], row['Y_kpc'], row['inclination_deg'], nodes)
        mirror = ray_geometry(-row['X_kpc'], -row['Y_kpc'], row['inclination_deg'], nodes)
        assert [ray['lo'], ray['hi']] == row['box_entry_exit_kpc']
        rays.append((row, ray, mirror))
        needed.update(ray['corners'] | mirror['corners'])
    residual, reference_info = old.reference_nodes(phi, centers, p['extent'], q, p['newtonian'], needed)

    def check(name, error, tolerance):
        checks.append({'case': census['case'], 'name': name, 'error': float(error),
                       'tolerance': float(tolerance), 'passed': bool(math.isfinite(error) and error <= tolerance)})

    for check_row in inherited_checks:
        if check_row['case'] == census['case'] and any(marker in check_row['name'] for marker in
                (':sphere_quadrature:', ':sphere_whole_vs_pieces', ':analytic_newtonian:', ':analytic_deep:', ':physical_units_')):
            assert check_row['passed']
            checks.append({**check_row, 'inherited_unchanged_from': 'SAVED_POTENTIAL_LENSING_RESULTS.json'})
    check('spherical_reference_potential_64_128', reference_info['potential_64_128_max_scaled_difference'], 1e-9)
    rows = []
    for previous, ray, mirror in rays:
        label, b = previous['projection'], previous['R_kpc']
        tag = f'{label}:{b}'
        four, scale4 = integrate_correction(ray, nodes, residual[64], 4)
        eight, scale8 = integrate_correction(ray, nodes, residual[64], 8)
        reverse, scale_reverse = integrate_correction(mirror, nodes, residual[64], 4)
        doubled, _ = integrate_correction(ray, nodes, residual[128], 4)
        for axis in (0, 1):
            check(tag+f':exact_cubic_segment:{axis}', abs(four[axis]-eight[axis]), 4096*EPS*max(1., scale4[axis]+scale8[axis]))
            check(tag+f':parity:{axis}', abs(four[axis]+reverse[axis]), 4096*EPS*max(1., scale4[axis]+scale_reverse[axis]))
        cross = 0 if label == 'minor_72' else 1
        check(tag+':cross_axis', abs(four[cross]), 4096*EPS*max(1., scale4[cross]))
        trapezoid = None
        if label == 'face_on':
            trap, scale_trap = faceon_trapezoid(b, nodes, residual[64])
            check(tag+':faceon_trapezoid', abs(four[0]-trap), 4096*EPS*max(1., scale4[0]+scale_trap))
            trapezoid = {'raw_integral': trap, 'cancellation_scale': scale_trap}
        sphere = np.array(previous['spherical_orders_raw']['128']['whole'])
        reference_effect = doubled-four
        check(tag+':reference_potential_effect', float(np.max(abs(reference_effect))),
              1e-7*max(1., float(np.linalg.norm(sphere)), float(np.linalg.norm(four))))
        pieces = {key: np.array(value) for key, value in previous['pieces_rad'].items()}
        pieces['finite_box_correction'] = FACTOR*four
        total = np.array([math.fsum(piece[i] for piece in pieces.values()) for i in (0, 1)])
        raw_sum = (pieces['spherical_interior']+pieces['spherical_exterior'])/FACTOR+four
        check(tag+':angle_piece_closure', float(np.max(abs(total-FACTOR*raw_sum))),
              128*EPS*max(float(sum(np.sum(abs(value)) for value in pieces.values())), np.finfo(float).tiny))
        projected = None
        if previous['newtonian_projected_mass'] is not None:
            projected = dict(previous['newtonian_projected_mass'])
            projected['fractional_error'] = abs(total[0]/projected['exact_angle_rad']-1)
            assert projected['target'] == .01
            check(tag+':newtonian_projected_mass', projected['fractional_error'], .01)
        rows.append({**previous, 'method': 'V002 local cubic s / linear |z|',
            'segment_count': len(ray['left']), 'pieces_rad': {key: value.tolist() for key, value in pieces.items()},
            'total_rad': total.tolist(), 'total_arcsec': (old.ARCSEC*total).tolist(),
            'V001_total_rad': previous['total_rad'],
            'V002_minus_V001_rad': (total-np.array(previous['total_rad'])).tolist(),
            'spherical_parts_reused_from_authenticated_V001': True,
            'correction_raw_orders': {'four': four.tolist(), 'eight': eight.tolist(),
                                     'mirror_four': reverse.tolist(), 'doubled_reference_four': doubled.tolist()},
            'correction_cancellation_scale': scale4.tolist(),
            'reference_potential_effect_rad': (FACTOR*reference_effect).tolist(),
            'faceon_trapezoid': trapezoid, 'newtonian_projected_mass': projected})
    del phi
    return {**before, 'method': 'V002 local cubic s / linear |z|',
            'reference_nodes': reference_info, 'rays': rows, 'seconds': time.perf_counter()-started}


def main():
    assert sys.argv[1:] in ([], ['freeze'])
    census, files, previous = inputs()
    specification = {'files': files, 'case_census': census, 'method': 'local four-node cubic in s=R^2; linear |z|',
                     'radial_stencil_start': 'clip(interval-1,0,node_count-4)',
                     'segment_orders': [4, 8], 'reference_potential_orders': [64, 128],
                     'spherical_parts': 'exact authenticated V001 reuse', 'maximum_reference_batch': 512,
                     'synthetic_mesh': [12, 16.], 'synthetic_radii': [2.7, 8.7],
                     'physical_radii_kpc': list(old.RADII), 'unchanged_projected_mass_target': .01}
    if sys.argv[1:] == ['freeze']:
        old.law.save_new(FREEZE, specification)
        return
    assert json.loads(FREEZE.read_text()) == specification
    assert not RESULT.exists(), 'A V002 result already exists; never overwrite or silently repeat.'
    started = time.perf_counter()
    checks = synthetic_controls()
    # Preserve synthetic failures as a standalone final result without reading projections.
    cases = []
    if all(row['passed'] for row in checks):
        for item, before in zip(census, previous['cases']):
            cases.append(calculate_case(item, before, previous['checks'], checks))
            print(json.dumps({'completed_V002_lensing_case': item['case'], 'rays': 15,
                              'seconds': cases[-1]['seconds']}), flush=True)
    failures = [row for row in checks if not row['passed']]
    payload = {'status': 'COMPLETE' if not failures else 'FAILED_NUMERICAL_CONTROLS',
        'role': 'Post-failure interpolation repair; same conditional metric, fields, rays, exterior and targets.',
        'previous_result_sha256': old.law.sha(old.RESULT), 'cases': cases, 'checks': checks,
        'failed_checks': failures, 'comparisons': old.descriptive_comparisons(cases) if cases else {},
        'seconds': time.perf_counter()-started,
        'peak_self_rss_bytes': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    old.law.save_new(RESULT, {'freeze_sha256': old.law.sha(FREEZE),
        'payload_sha256': hashlib.sha256(old.law.encode(payload)).hexdigest(), 'payload': payload})
    print(json.dumps({'status': payload['status'], 'cases': len(cases), 'checks': len(checks),
                      'failures': len(failures), 'seconds': payload['seconds']}), flush=True)
    if failures:
        raise SystemExit('V002 failures preserved; no automatic method/tolerance change.')


if __name__ == '__main__':
    main()
