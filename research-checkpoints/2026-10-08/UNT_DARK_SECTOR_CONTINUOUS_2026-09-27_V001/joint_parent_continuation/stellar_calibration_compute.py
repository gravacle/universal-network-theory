"""One fixed source-calibration comparison; immutable helpers, additive custody."""
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
import disk_solver as law
import axisymmetric_disk_v002 as disk
import galaxy_density as density
import galaxy_field_compute as inherited
import disk_response_diagnostic as response

ROOT = law.ROOT
MODEL = 'ML36_CAL_HI1_H21_V001'
FREEZE = ROOT / 'STELLAR_CALIBRATION_FROZEN.json'
ORACLE = ROOT / 'STELLAR_CALIBRATION_ORACLE.json'
RESULT = ROOT / 'STELLAR_CALIBRATION_RESULTS.json'
JOBS = ((256, 255, False), (320, 1023, False), (512, 255, False), (512, 255, True))


def identity(n, extent, newtonian):
    return f'{MODEL}_N{n}_L{extent}_Newton{int(newtonian)}'


def authenticated(path, freeze_hash):
    record = json.loads(path.read_text())
    assert record['freeze_sha256'] == freeze_hash
    assert record['payload_sha256'] == hashlib.sha256(law.encode(record['payload'])).hexdigest()
    return record['payload']


def publish(path, payload, freeze_hash):
    law.save_new(path, {'freeze_sha256': freeze_hash,
                       'payload_sha256': hashlib.sha256(law.encode(payload)).hexdigest(),
                       'payload': payload})


def inputs():
    """Validate complete original queue and nested source custody without a solve."""
    names = {'STELLAR_CALIBRATION_PROTOCOL.md', 'STELLAR_CALIBRATION_TEST_DESIGN.md',
             'stellar_calibration_compute.py', 'PHOTOMETRIC_SOURCE_COMPARISON.json',
             'PHOTOMETRIC_SOURCE_COMPARISON.md', 'photometric_source_comparison.py',
             'DISK_RESPONSE_DIAGNOSTIC.md', 'disk_response_diagnostic.py'}
    freezes = ('GALAXY_FIELD_FROZEN.json', 'STRETCHED_DISK_V002_FROZEN.json',
               'RING_ORACLE_FROZEN.json')
    for name in freezes:
        names.add(name)
        for member, digest in json.loads((ROOT / name).read_text())['files'].items():
            assert law.sha(ROOT / member) == digest, member
            names.add(member)
    calibration = json.loads((ROOT / 'PHOTOMETRIC_SOURCE_COMPARISON.json').read_text())
    assert calibration['source_sha256'] == law.sha(ROOT / 'photometric_source_comparison.py')
    for name, digest in calibration['input_sha256'].items():
        path = ROOT.parent / name
        assert law.sha(path) == digest
        names.add(os.path.relpath(path, ROOT))
    multiplier = calibration['same_imaging_same_geometry_mass_conversion_ratio']
    expected = .5 * (1e4 * 10**(.4 * 3.24) / 280.9) / 280
    assert multiplier == 1.2567828155112788 and abs(multiplier / expected - 1) <= 2e-15
    old_hash = law.sha(ROOT / 'GALAXY_FIELD_FROZEN.json')
    for hi, h2 in ((True, True), (False, True), (True, False), (False, False)):
        for n, extent, newtonian in JOBS:
            name = inherited.case_name(hi, h2, n, extent, newtonian)
            path = ROOT / (name + '.json')
            p = authenticated(path, old_hash)
            assert p['case'] == name and all(p['checks'].values())
            assert (p['hi_tail'], p['h2_tail'], p['N'], p['extent'], p['newtonian']) == (hi, h2, n, extent, newtonian)
            names.add(path.name)
    for name in sorted(names):
        if name.startswith('stretched_V002_') and name.endswith('.json'):
            p = authenticated(ROOT / name, law.sha(ROOT / 'STRETCHED_DISK_V002_FROZEN.json'))
            assert all(p['checks'].values())
    ring = authenticated(ROOT / 'RING_ORACLE_RESULTS.json', law.sha(ROOT / 'RING_ORACLE_FROZEN.json'))
    assert ring['status'] == 'COMPLETE' and all(row['passed'] for row in ring['checks'])
    return multiplier, {name: law.sha(ROOT / name) for name in sorted(names)}, ring


def source(multiplier):
    components = density.profiles(True, True)
    p = components['stars']
    components['stars'] = density.Profile(p.r.copy(), multiplier * p.s, p.tail)
    return components


def recombine_oracle(ring, multiplier):
    """Linear combination of saved component quadratures; no new quadrature."""
    checks, cases = [], []

    def check(name, error, tolerance):
        checks.append({'name': name, 'error': float(error), 'tolerance': float(tolerance),
                       'passed': bool(math.isfinite(error) and error <= tolerance)})

    for old in ring['cases']:
        if not (old['hi_tail'] and old['h2_tail']):
            continue
        radius, rows = old['R_kpc'], []
        masses = dict(old['component_masses_Msun'])
        masses['stars'] *= multiplier
        for entry in old['heights']:
            orders = {}
            for order in ('48', '96'):
                original = entry['orders'][order]
                pieces = {name: {key: value * (multiplier if name == 'stars' else 1.)
                                 for key, value in piece.items()}
                          for name, piece in original['components'].items()}
                omitted = sum(piece['omitted_mass_Msun'] for piece in pieces.values())
                cutoff = original['cutoff_kpc']
                orders[order] = {'gR_kms2_per_kpc': sum(p['gR_kms2_per_kpc'] for p in pieces.values()),
                    'potential_kms2': sum(p['potential_kms2'] for p in pieces.values()),
                    'components': pieces, 'cutoff_kpc': cutoff,
                    'force_tail_bound_kms2_per_kpc': density.G_KPC_KMS2_MSUN * omitted / (cutoff - radius)**2,
                    'potential_tail_bound_kms2': density.G_KPC_KMS2_MSUN * omitted / (cutoff - radius)}
            for key in ('gR_kms2_per_kpc', 'potential_kms2'):
                check(f'{radius}/{entry["z_kpc"]}/{key}',
                      abs(orders['48'][key] - orders['96'][key]) / max(1., abs(orders['96'][key])), 1e-8)
            for name, piece in orders['96']['components'].items():
                check(f'{radius}/{entry["z_kpc"]}/mass/{name}',
                      abs(piece['quadrature_mass_Msun'] + piece['omitted_mass_Msun'] - masses[name]) / masses[name], 1e-9)
            rows.append({'z_kpc': entry['z_kpc'], 'orders': orders})
        values = [row['orders']['96']['gR_kms2_per_kpc'] for row in rows]
        extrapolated = [2 * values[j + 1] - values[j] for j in (0, 1)]
        check(f'{radius}/height', abs(extrapolated[1] - extrapolated[0]) / max(1., abs(extrapolated[1])), 1e-3)
        check(f'{radius}/tail', rows[-1]['orders']['96']['force_tail_bound_kms2_per_kpc'] / max(1., abs(extrapolated[1])), 1e-10)
        cases.append({'R_kpc': radius, 'component_masses_Msun': masses, 'heights': rows,
                      'extrapolated_gR_kms2_per_kpc': extrapolated})
    assert [row['R_kpc'] for row in cases] == [2.7, 8.7, 20.7, 35.7, 43.7]
    return {'status': 'COMPLETE' if all(row['passed'] for row in checks) else 'FAILED',
            'model': MODEL, 'stellar_multiplier': multiplier, 'cases': cases, 'checks': checks,
            'role': 'component-linear recombination of qualified independent-of-FV ring oracle'}


def run_case(n, extent, newtonian, multiplier, freeze_hash, oracle):
    started = time.perf_counter()
    name = identity(n, extent, newtonian)
    components = source(multiplier)
    masses = density.masses(components)
    old_masses = density.masses(density.profiles(True, True))
    scaling_error = max(abs(masses[key] / (mass * (multiplier if key == 'stars' else 1.)) - 1)
                        for key, mass in old_masses.items())
    mass = sum(masses.values())
    q = density.G_KPC_KMS2_MSUN * mass / density.A0_KMS2_KPC
    geometry = edges, centers, width = disk.mesh(n, extent)
    sr = np.sqrt(extent**2 + centers**2)
    pr = disk.spherical_potential(sr, q, newtonian=newtonian)
    tangent = (q / sr**2 if newtonian else law.inverse(q / sr**2)) * centers / sr
    bottom = density.bottom_flux(edges, components)
    boundary = (pr, pr.copy(), tangent, tangent, bottom)
    checkpoint = ROOT / (name + '.checkpoint.npz')
    history = None
    if checkpoint.exists():
        initial, history = inherited.load_checkpoint(checkpoint, name, freeze_hash, n)
        print(json.dumps({'resume_checkpoint': name, 'completed_outer': len(history)}), flush=True)
    else:
        rr, zz = np.meshgrid(centers, centers, indexing='ij')
        s = np.sqrt(rr**2 + (zz + 5.)**2)
        initial = q * (1 - 1 / s) if newtonian else math.sqrt(q) * np.log(s)
    phi, radial, history, ok = disk.solve(geometry, boundary, initial, newtonian,
        checkpoint=inherited.checkpoint_writer(checkpoint, name, freeze_hash), history_start=history)
    old_name = inherited.case_name(True, True, n, extent, newtonian)
    old = authenticated(ROOT / (old_name + '.json'), law.sha(ROOT / 'GALAXY_FIELD_FROZEN.json'))
    obs = inherited.observations()
    assert len(old['comparison']) == len(obs) == 43
    radii = np.array([row['R'] for row in obs])
    sampled = np.interp(radii, centers, radial)
    comparison = []
    for row, force, prior in zip(obs, sampled, old['comparison']):
        assert all(row[key] == prior[key] for key in ('R', 'velocity', 'error'))
        v2 = row['R'] * density.A0_KMS2_KPC * float(force)
        speed = math.sqrt(v2) if v2 >= 0 else None
        comparison.append(dict(**row, radial_force_a0=float(force), velocity_squared=v2,
            prediction=speed, residual=None if speed is None else speed - row['velocity'],
            old_radial_force_a0=prior['radial_force_a0'], old_prediction=prior['prediction'],
            old_residual=prior['residual'], force_change_a0=float(force) - prior['radial_force_a0'],
            velocity_squared_change=v2 - prior['velocity_squared'],
            velocity_change=None if speed is None or prior['prediction'] is None else speed - prior['prediction']))
    summaries = {}
    for lower in (0., 2., 8.):
        selected = [row for row in comparison if row['R'] >= lower and row['residual'] is not None]
        residuals = np.array([row['residual'] for row in selected])
        errors = np.array([row['error'] for row in selected])
        paired = [row['velocity_change'] for row in selected if row['velocity_change'] is not None]
        summaries[f'R_ge_{lower:g}_kpc'] = {'count': len(selected),
            'omitted_negative_force_count': sum(row['R'] >= lower and row['residual'] is None for row in comparison),
            'rms_kms': float(np.sqrt(np.mean(residuals**2))) if selected else None,
            'mean_residual_kms': float(np.mean(residuals)) if selected else None,
            'max_abs_residual_kms': float(np.max(abs(residuals))) if selected else None,
            'nominal_sum_squared_error_units': float(np.sum((residuals / errors)**2)) if selected else None,
            'paired_real_velocity_count': len(paired),
            'mean_velocity_change_kms': float(np.mean(paired)) if paired else None}
    flux_mass = float(np.sum(bottom)) * density.A0_KMS2_KPC / density.G_KPC_KMS2_MSUN
    in_domain = sum(float(2 * math.pi * 1e6 * p.integral(0., extent)) for p in components.values())
    mass_error = abs(flux_mass - in_domain) / in_domain
    checks = {'converged': bool(ok), 'source_mass': mass_error <= 1e-13,
        'source_scaling': scaling_error <= 1e-13,
        'flux_balance': history[-1].get('flux_balance_error', math.inf) <= 2e-6,
        'unclipped': history[-1].get('clipped_faces', -1) == 0,
        'nonlinear_residual': history[-1].get('nonlinear_error', math.inf) <= 1e-9}
    numerical_comparison = {}
    if not newtonian and (extent == 1023 or n == 512):
        baseline = authenticated(ROOT / (identity(256, 255, False) + '.json'), freeze_hash)
        assert all(baseline['checks'].values())
        original = np.array([row['radial_force_a0'] for row in baseline['comparison']])
        selected = radii >= 2.
        difference = float(np.max(abs(sampled[selected] - original[selected]) / np.maximum(abs(sampled[selected]), 1e-12)))
        label = 'remote_domain' if extent == 1023 else 'mesh_refinement'
        numerical_comparison[label + '_max_force_change'] = difference
        checks[label] = difference < .02
    ring_comparison = []
    if newtonian:
        for item in oracle['cases']:
            radius = item['R_kpc']
            reference = item['extrapolated_gR_kms2_per_kpc'][-1]
            numerical = float(np.interp(radius, centers, radial)) * density.A0_KMS2_KPC
            height_delta = abs(reference - item['extrapolated_gR_kms2_per_kpc'][0])
            orders = item['heights'][-1]['orders']
            quad_delta = abs(orders['96']['gR_kms2_per_kpc'] - orders['48']['gR_kms2_per_kpc'])
            allowance = .02 * max(1., abs(reference)) + height_delta + quad_delta
            error = abs(numerical - reference)
            ring_comparison.append({'R_kpc': radius, 'grid_gR_kms2_per_kpc': numerical,
                'oracle_extrapolated_gR_kms2_per_kpc': reference,
                'oracle_extrapolation_difference': height_delta, 'oracle_quadrature_difference': quad_delta,
                'absolute_discrepancy': error, 'numerical_allowance': allowance, 'passed': error <= allowance})
        checks['independent_newtonian_force'] = len(ring_comparison) == 5 and all(row['passed'] for row in ring_comparison)
    payload = {'case': name, 'model': MODEL, 'stellar_multiplier': multiplier, 'hi_tail': True, 'h2_tail': True,
        'N': n, 'extent': extent, 'newtonian': newtonian, 'component_masses_Msun': masses,
        'omitted_mass_beyond_boundary_Msun': mass - in_domain,
        'source_mass_relative_error': mass_error, 'source_scaling_relative_error': scaling_error,
        'checks': checks, 'history': history, 'numerical_comparison': numerical_comparison,
        'independent_newtonian_force_comparison': ring_comparison,
        'radii': centers.tolist(), 'radial_force_a0': radial.tolist(), 'phi': phi.tolist(),
        'comparison': comparison, 'summaries_descriptive_only': summaries,
        'original_same_grid_case': old_name, 'seconds_this_invocation': time.perf_counter() - started,
        'peak_self_rss_bytes': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    publish(ROOT / (name + '.json'), payload, freeze_hash)
    print(json.dumps({'completed': name, 'checks': checks, 'seconds': payload['seconds_this_invocation'],
                      'descriptive_velocity_residuals': summaries}), flush=True)
    return payload


def matched_diagnostic(multiplier, freeze_hash):
    actual = authenticated(ROOT / (identity(512, 255, False) + '.json'), freeze_hash)
    newton = authenticated(ROOT / (identity(512, 255, True) + '.json'), freeze_hash)
    assert actual['radii'] == newton['radii'] and actual['component_masses_Msun'] == newton['component_masses_Msun']
    components = source(multiplier)
    total_mass = sum(actual['component_masses_Msun'].values())
    rows, checks = [], []
    centers = np.array(actual['radii'])
    knots = np.unique(np.concatenate([p.r for p in components.values()]))
    for a, n in zip(actual['comparison'], newton['comparison']):
        radius, x, nr = a['R'], a['radial_force_a0'], n['radial_force_a0']
        assert all(a[key] == n[key] for key in ('R', 'velocity', 'error'))
        sigma = sum(float(p.sigma(radius)) for p in components.values())
        b = 2 * math.pi * density.G_KPC_KMS2_MSUN * 1e6 * sigma / density.A0_KMS2_KPC
        z = response.reconstruct_vertical(x, b)
        mu = response.mu(math.hypot(x, z))
        solenoidal = mu * x - nr
        vector = response.vector_radial(nr, b)
        radial = math.copysign(response.inv(abs(nr)), nr) if nr else 0.
        deep = math.copysign(math.sqrt(abs(nr)), nr) if nr else 0.
        flat = math.sqrt(density.G_KPC_KMS2_MSUN * total_mass / density.A0_KMS2_KPC) / radius
        terms = {'remaining_field': x - vector, 'vertical_projection': vector - radial,
                 'law_shape_vs_deep': radial - deep, 'newtonian_disk_vs_monopole': deep - flat}
        factor = radius * density.A0_KMS2_KPC
        v2_terms = {key: value * factor for key, value in terms.items()}
        reference_residual = factor * flat - a['velocity']**2
        errors = {'sheet_jump': (abs(mu * z - b), max(1., abs(b))),
            'flux_inversion': (abs(response.vector_radial(nr + solenoidal, b) - x), max(1., abs(x))),
            'force_decomposition': (abs(sum(terms.values()) - x + flat), max(1., abs(x), abs(flat))),
            'v2_decomposition': (abs(sum(v2_terms.values()) + reference_residual - a['velocity_squared'] + a['velocity']**2),
                                  max(1., abs(a['velocity_squared']), a['velocity']**2, abs(factor * flat)))}
        for key, (error, scale) in errors.items():
            checks.append({'name': f'{radius}/{key}', 'error': error, 'tolerance': 1e-11 * scale,
                           'passed': bool(error <= 1e-11 * scale)})
        rows.append({'R_kpc': radius, 'true_radial_a0': x, 'newtonian_radial_a0': nr,
            'sigma_Msun_pc2': sigma, 'sheet_flux_a0': b, 'reconstructed_vertical_a0': z,
            'mu': mu, 'radial_solenoidal_flux_a0': solenoidal,
            'force_terms_a0': terms, 'signed_v2_terms_kms2': v2_terms,
            'reference_residual_v2_kms2': reference_residual,
            'true_residual_v2_kms2': a['velocity_squared'] - a['velocity']**2,
            'nearest_knot_distance_kpc': float(np.min(abs(knots - radius))),
            'local_radial_center_spacing_kpc': float(np.interp(radius, centers, np.gradient(centers))),
            'hard_edge_warning': False})  # All three profiles have continuous exponential tails.
    assert len(rows) == 43
    return {'status': 'COMPLETE' if all(c['passed'] for c in checks) else 'FAILED',
            'role': 'same-source same-domain sheet reconstruction and signed bookkeeping',
            'rows': rows, 'checks': checks}


def main():
    assert sys.argv[1:] in ([], ['freeze'])
    multiplier, files, ring = inputs()
    specification = {'files': files, 'model': MODEL, 'stellar_multiplier': multiplier,
                     'jobs': [list(job) for job in JOBS], 'r': law.RATIO,
                     'a0_kms2_kpc': density.A0_KMS2_KPC}
    if sys.argv[1:] == ['freeze']:
        law.save_new(FREEZE, specification)
        return
    assert json.loads(FREEZE.read_text()) == specification
    freeze_hash = law.sha(FREEZE)
    if ORACLE.exists():
        oracle = authenticated(ORACLE, freeze_hash)
    else:
        oracle = recombine_oracle(ring, multiplier)
        publish(ORACLE, oracle, freeze_hash)
    assert oracle['model'] == MODEL and oracle['stellar_multiplier'] == multiplier
    assert oracle['status'] == 'COMPLETE' and all(row['passed'] for row in oracle['checks'])
    case_files = {}
    for job in JOBS:
        name = identity(*job)
        path = ROOT / (name + '.json')
        result = authenticated(path, freeze_hash) if path.exists() else run_case(*job, multiplier, freeze_hash, oracle)
        assert result['case'] == name and result['model'] == MODEL and result['stellar_multiplier'] == multiplier
        assert tuple(result[key] for key in ('N', 'extent', 'newtonian')) == job
        assert all(result['checks'].values()), 'Failed calculation retained; diagnose before proceeding.'
        case_files[path.name] = law.sha(path)
        print(json.dumps({'verified_completed_case': name}), flush=True)
    if RESULT.exists():
        final = authenticated(RESULT, freeze_hash)
        assert final['case_files_sha256'] == case_files
        assert final['oracle_sha256'] == law.sha(ORACLE)
    else:
        diagnostic = matched_diagnostic(multiplier, freeze_hash)
        final = {'status': diagnostic['status'], 'model': MODEL, 'stellar_multiplier': multiplier,
                 'case_files_sha256': case_files, 'oracle_sha256': law.sha(ORACLE),
                 'matched_diagnostic': diagnostic}
        publish(RESULT, final, freeze_hash)
    assert final['status'] == 'COMPLETE'
    print(json.dumps({'status': final['status'], 'case_count': 4, 'matched_rows': 43,
                      'model': MODEL}), flush=True)


if __name__ == '__main__':
    main()
