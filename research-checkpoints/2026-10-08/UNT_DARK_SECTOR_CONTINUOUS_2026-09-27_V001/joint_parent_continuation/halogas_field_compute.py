"""Additive two-source/eight-case queue. Inert until explicit freeze or run."""
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
import galaxy_ring_oracle as ring
import halogas_density as source

ROOT = law.ROOT
SOURCE_DIR = ROOT/'halogas_source_candidate'
FREEZE = ROOT/'HALOGAS_FIELD_FROZEN.json'
QUALIFICATION = ROOT/'HALOGAS_FIELD_SOURCE_QUALIFICATION.json'
ORACLE = ROOT/'HALOGAS_FIELD_ORACLE.json'
RESULT = ROOT/'HALOGAS_FIELD_RESULTS.json'
JOBS = ((256, 255, False), (320, 1023, False), (512, 255, False), (512, 255, True))
WIDTHS = (40, 120)
CONTROL = 'ML36_CAL_HI1_H21_V001'


def identity(model, n, extent, newtonian):
    return f'{model}_N{n}_L{extent}_Newton{int(newtonian)}'


def authenticated(path, freeze_hash):
    record = json.loads(path.read_text())
    assert record['freeze_sha256'] == freeze_hash, path
    assert record['payload_sha256'] == hashlib.sha256(law.encode(record['payload'])).hexdigest(), path
    return record['payload']


def flat_seal(path):
    record = json.loads(path.read_text())
    payload = {key: value for key, value in record.items() if key != 'payload_sha256'}
    assert record['payload_sha256'] == hashlib.sha256(law.encode(payload)).hexdigest(), path
    return record


def publish(path, payload, freeze_hash):
    law.save_new(path, {'freeze_sha256': freeze_hash,
                       'payload_sha256': hashlib.sha256(law.encode(payload)).hexdigest(),
                       'payload': payload})


def inputs():
    """Read/authenticate existing inputs only; no new source/force computation."""
    files, visited = {}, set()

    def add(path, expected=None):
        path = path.resolve()
        digest = law.sha(path)
        if expected is not None:
            assert digest == expected, path
        files[os.path.relpath(path, ROOT)] = digest
        return path

    def manifest(path):
        path = add(path)
        if path in visited:
            return
        visited.add(path)
        record = json.loads(path.read_text())
        if 'payload_sha256' in record and 'payload' not in record:
            flat_seal(path)
        members = record.get('files', record.get('inputs_sha256'))
        assert isinstance(members, dict), path
        for name, digest in members.items():
            member = add(path.parent/name, digest)
            if member.name.endswith('_FROZEN.json'):
                manifest(member)

    for name in ('HALOGAS_FIELD_PROTOCOL.md', 'halogas_field_compute.py', 'halogas_density.py'):
        add(ROOT/name)
    add(SOURCE_DIR/'PLANAR_DENSITY_REPRESENTATION_PROPOSAL.md')
    add(SOURCE_DIR/'HALOGAS_SOURCE_TRACER_CONTEXT.md')
    manifest(SOURCE_DIR/'PLANAR_SOURCE_FROZEN.json')
    add(SOURCE_DIR/'PLANAR_SOURCE_RESULTS.json',
        '44b359abbcae5c0c61b26d3adc515a716fd6d45795fcecff3004189814230b2c')
    extraction = flat_seal(SOURCE_DIR/'PLANAR_SOURCE_RESULTS.json')
    prior = flat_seal(SOURCE_DIR/'PLANAR_SOURCE_FROZEN.json')
    assert extraction['freeze_sha256'] == law.sha(SOURCE_DIR/'PLANAR_SOURCE_FROZEN.json')
    assert extraction['inputs_sha256'] == prior['inputs_sha256']
    assert extraction['settings'] == prior['settings']
    assert extraction['status'] == 'COMPLETE' and all(row['passed'] for row in extraction['checks'])
    settings = extraction['settings']
    assert (settings['distance_pc'], settings['inclination_deg'], settings['pa_deg'],
            settings['helium_factor'], settings['HI_atoms_cm2_per_Msun_pc2']) == (13.8e6, 72., 215., 1.36, 1.25e20)
    manifest(ROOT/'STELLAR_CALIBRATION_FROZEN.json')
    calibration = json.loads((ROOT/'PHOTOMETRIC_SOURCE_COMPARISON.json').read_text())
    add(ROOT/'photometric_source_comparison.py', calibration['source_sha256'])
    for name, digest in calibration['input_sha256'].items():
        add(ROOT.parent/name, digest)
    multiplier = calibration['same_imaging_same_geometry_mass_conversion_ratio']
    expected = .5*(1e4*10**(.4*3.24)/280.9)/280
    assert multiplier == source.MULTIPLIER and abs(multiplier/expected-1) <= 2e-15
    control_hash = law.sha(ROOT/'STELLAR_CALIBRATION_FROZEN.json')
    old_hash = law.sha(ROOT/'GALAXY_FIELD_FROZEN.json')
    benchmark_hash = law.sha(ROOT/'STRETCHED_DISK_V002_FROZEN.json')
    # Nested qualified cases are authenticated, not just hashed as new opaque inputs.
    for name in list(files):
        if name.startswith('stretched_V002_') and name.endswith('.json'):
            payload = authenticated(ROOT/name, benchmark_hash)
            assert all(payload['checks'].values())
        elif name.startswith('galaxy_HI') and name.endswith('.json'):
            payload = authenticated(ROOT/name, old_hash)
            assert payload['case']+'.json' == name and all(payload['checks'].values())
    for result_name, freeze_name in (('RING_ORACLE_RESULTS.json', 'RING_ORACLE_FROZEN.json'),
                                    ('STELLAR_CALIBRATION_ORACLE.json', 'STELLAR_CALIBRATION_FROZEN.json'),
                                    ('STELLAR_CALIBRATION_RESULTS.json', 'STELLAR_CALIBRATION_FROZEN.json')):
        add(ROOT/result_name)
        payload = authenticated(ROOT/result_name, law.sha(ROOT/freeze_name))
        assert payload['status'] == 'COMPLETE'
        if 'checks' in payload:
            assert all(row['passed'] for row in payload['checks'])
    final_control = authenticated(ROOT/'STELLAR_CALIBRATION_RESULTS.json', control_hash)
    assert final_control['model'] == CONTROL
    assert final_control['oracle_sha256'] == law.sha(ROOT/'STELLAR_CALIBRATION_ORACLE.json')
    for job in JOBS:
        case = identity(CONTROL, *job)
        path = add(ROOT/(case+'.json'), final_control['case_files_sha256'][case+'.json'])
        p = authenticated(path, control_hash)
        assert p['case'] == case and p['model'] == CONTROL and p['stellar_multiplier'] == multiplier
        assert tuple(p[key] for key in ('N', 'extent', 'newtonian')) == job and all(p['checks'].values())
    return extraction, multiplier, dict(sorted(files.items()))


def qualification(extraction, multiplier):
    rows = [source.qualify(extraction, width, multiplier) for width in WIDTHS]
    same_support = rows[0]['support_kpc'] == rows[1]['support_kpc']
    mass_error = abs(rows[0]['included_retained_bare_HI_Msun']/rows[1]['included_retained_bare_HI_Msun']-1)
    checks = {'both_source_representations': all(row['status'] == 'COMPLETE' for row in rows),
              'same_complete_aperture': same_support, 'same_included_mass': mass_error <= 1e-13}
    return {'status': 'COMPLETE' if all(checks.values()) else 'FAILED', 'checks': checks,
            'models': rows, 'shared_mass_relative_error': mass_error}


def new_oracle(extraction, multiplier):
    started = time.perf_counter()
    checks, cases = [], []

    def check(name, error, tolerance):
        checks.append({'name': name, 'error': float(error), 'tolerance': float(tolerance),
                       'passed': bool(math.isfinite(error) and error <= tolerance)})

    for width in WIDTHS:
        model = source.MODELS[width]
        components = source.source(extraction, width, multiplier)
        masses, knots = density.masses(components), ring.source_knots(components)
        for radius in ring.RADII:
            distance = float(np.min(abs(knots-radius)))
            assert distance > 1e-10
            heights = [min(.2, distance/4)/2**i for i in range(3)]
            rows = []
            for height in heights:
                outputs = {str(order): ring.field(radius, height, components, order) for order in ring.ORDERS}
                for key in ('gR_kms2_per_kpc', 'potential_kms2'):
                    check(f'quadrature:{model}:{radius}:{height}:{key}',
                          ring.relative(outputs['48'][key], outputs['96'][key]), 1e-8)
                for name, piece in outputs['96']['components'].items():
                    check(f'mass:{model}:{radius}:{height}:{name}',
                          abs(piece['quadrature_mass_Msun']+piece['omitted_mass_Msun']-masses[name])/masses[name], 1e-9)
                rows.append({'z_kpc': height, 'orders': outputs})
            values = [row['orders']['96']['gR_kms2_per_kpc'] for row in rows]
            extrapolated = [2*values[i+1]-values[i] for i in (0, 1)]
            check(f'height:{model}:{radius}', ring.relative(extrapolated[0], extrapolated[1]), 1e-3)
            check(f'tail:{model}:{radius}', rows[-1]['orders']['96']['force_tail_bound_kms2_per_kpc']/max(1., abs(extrapolated[1])), 1e-10)
            cases.append({'model': model, 'width_arcsec': width, 'R_kpc': radius,
                          'component_masses_Msun': masses, 'heights': rows,
                          'nearest_knot_distance_kpc': distance,
                          'extrapolated_gR_kms2_per_kpc': extrapolated})
    return {'status': 'COMPLETE' if all(c['passed'] for c in checks) else 'FAILED',
            'checks': checks, 'cases': cases, 'role': 'fresh independent-of-FV Newtonian ring quadrature; no velocities',
            'seconds': time.perf_counter()-started,
            'peak_self_rss_bytes': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}


def run_case(width, n, extent, newtonian, extraction, multiplier, freeze_hash, oracle, qualified):
    started = time.perf_counter()
    model = source.MODELS[width]
    name = identity(model, n, extent, newtonian)
    components = source.source(extraction, width, multiplier)
    masses = density.masses(components)
    mass = sum(masses.values())
    q = density.G_KPC_KMS2_MSUN*mass/density.A0_KMS2_KPC
    geometry = edges, centers, _ = disk.mesh(n, extent)
    sr = np.sqrt(extent**2+centers**2)
    pr = disk.spherical_potential(sr, q, newtonian=newtonian)
    tangent = (q/sr**2 if newtonian else law.inverse(q/sr**2))*centers/sr
    bottom = density.bottom_flux(edges, components)
    boundary = (pr, pr.copy(), tangent, tangent, bottom)
    checkpoint = ROOT/(name+'.checkpoint.npz')
    history = None
    if checkpoint.exists():
        initial, history = inherited.load_checkpoint(checkpoint, name, freeze_hash, n)
        print(json.dumps({'resume_checkpoint': name, 'completed_outer': len(history)}), flush=True)
    else:
        rr, zz = np.meshgrid(centers, centers, indexing='ij')
        s = np.sqrt(rr*rr+(zz+5.)**2)
        initial = q*(1-1/s) if newtonian else math.sqrt(q)*np.log(s)
    phi, radial, history, ok = disk.solve(geometry, boundary, initial, newtonian,
            checkpoint=inherited.checkpoint_writer(checkpoint, name, freeze_hash), history_start=history)
    control_name = identity(CONTROL, n, extent, newtonian)
    control = authenticated(ROOT/(control_name+'.json'), law.sha(ROOT/'STELLAR_CALIBRATION_FROZEN.json'))
    obs = inherited.observations()
    radii = np.array([row['R'] for row in obs])
    sampled = np.interp(radii, centers, radial)
    comparisons = []
    assert len(obs) == len(control['comparison']) == 43
    for row, force, old in zip(obs, sampled, control['comparison']):
        assert all(row[key] == old[key] for key in ('R', 'velocity', 'error'))
        v2 = row['R']*density.A0_KMS2_KPC*float(force)
        velocity = math.sqrt(v2) if v2 >= 0 else None
        comparisons.append(dict(**row, radial_force_a0=float(force), velocity_squared=v2,
            prediction=velocity, residual=None if velocity is None else velocity-row['velocity'],
            control_radial_force_a0=old['radial_force_a0'], control_prediction=old['prediction'],
            signed_force_change_a0=float(force)-old['radial_force_a0'],
            signed_v2_change_kms2=v2-old['velocity_squared'],
            velocity_change_kms=None if velocity is None or old['prediction'] is None else velocity-old['prediction']))
    summaries = {}
    for lower in (0., 2., 8.):
        selected = [row for row in comparisons if row['R'] >= lower and row['residual'] is not None]
        residuals, errors = np.array([r['residual'] for r in selected]), np.array([r['error'] for r in selected])
        changes = [r['velocity_change_kms'] for r in selected if r['velocity_change_kms'] is not None]
        summaries[f'R_ge_{lower:g}_kpc'] = {
            'count': len(selected), 'omitted_negative_force_count': sum(r['R'] >= lower and r['residual'] is None for r in comparisons),
            'rms_kms': float(np.sqrt(np.mean(residuals**2))) if selected else None,
            'mean_residual_kms': float(np.mean(residuals)) if selected else None,
            'max_abs_residual_kms': float(np.max(abs(residuals))) if selected else None,
            'nominal_sum_squared_error_units': float(np.sum((residuals/errors)**2)) if selected else None,
            'mean_change_from_calibrated_control_kms': float(np.mean(changes)) if changes else None}
    flux_mass = float(np.sum(bottom))*density.A0_KMS2_KPC/density.G_KPC_KMS2_MSUN
    in_domain = sum(float(2*math.pi*1e6*p.integral(0., extent)) for p in components.values())
    mass_error = abs(flux_mass-in_domain)/in_domain
    source_error = max(abs(masses[key]/qualified['component_masses_Msun'][key]-1) for key in masses)
    checks = {'converged': bool(ok), 'source_mass': mass_error <= 1e-13,
              'qualified_source_identity': source_error <= 1e-13,
              'unchanged_stars_H2': all(abs(masses[key]/control['component_masses_Msun'][key]-1) <= 1e-13 for key in ('stars', 'H2_He')),
              'flux_balance': history[-1].get('flux_balance_error', math.inf) <= 2e-6,
              'unclipped': history[-1].get('clipped_faces', -1) == 0,
              'nonlinear_residual': history[-1].get('nonlinear_error', math.inf) <= 1e-9}
    numerical = {}
    if not newtonian and (extent == 1023 or n == 512):
        baseline = authenticated(ROOT/(identity(model, 256, 255, False)+'.json'), freeze_hash)
        assert all(baseline['checks'].values())
        previous = np.array([row['radial_force_a0'] for row in baseline['comparison']])
        chosen = radii >= 2.
        error = float(np.max(abs(sampled[chosen]-previous[chosen])/np.maximum(abs(sampled[chosen]), 1e-12)))
        label = 'remote_domain' if extent == 1023 else 'mesh_refinement'
        numerical[label+'_max_force_change'] = error
        checks[label] = error < .02
    ring_comparison = []
    if newtonian:
        for item in oracle['cases']:
            if item['model'] != model:
                continue
            radius, reference = item['R_kpc'], item['extrapolated_gR_kms2_per_kpc'][-1]
            value = float(np.interp(radius, centers, radial))*density.A0_KMS2_KPC
            height_error = abs(reference-item['extrapolated_gR_kms2_per_kpc'][0])
            last = item['heights'][-1]['orders']
            quad_error = abs(last['96']['gR_kms2_per_kpc']-last['48']['gR_kms2_per_kpc'])
            allowance = .02*max(1., abs(reference))+height_error+quad_error
            ring_comparison.append({'R_kpc': radius, 'grid_gR_kms2_per_kpc': value,
                'oracle_extrapolated_gR_kms2_per_kpc': reference,
                'oracle_extrapolation_difference': height_error, 'oracle_quadrature_difference': quad_error,
                'absolute_discrepancy': abs(value-reference), 'numerical_allowance': allowance,
                'passed': abs(value-reference) <= allowance})
        assert len(ring_comparison) == 5
        checks['independent_newtonian_force'] = all(row['passed'] for row in ring_comparison)
    payload = {'case': name, 'model': model, 'width_arcsec': width, 'stellar_multiplier': multiplier,
               'N': n, 'extent': extent, 'newtonian': newtonian,
               'component_masses_Msun': masses, 'total_mass_Msun': mass,
               'omitted_mass_beyond_boundary_Msun': mass-in_domain,
               'source_mass_relative_error': mass_error, 'qualified_source_relative_error': source_error,
               'checks': checks, 'history': history, 'numerical_comparison': numerical,
               'independent_newtonian_force_comparison': ring_comparison,
               'radii': centers.tolist(), 'radial_force_a0': radial.tolist(), 'phi': phi.tolist(),
               'comparison': comparisons, 'summaries_descriptive_only': summaries,
               'paired_calibrated_control_case': control_name,
               'seconds_this_invocation': time.perf_counter()-started,
               'peak_self_rss_bytes': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    publish(ROOT/(name+'.json'), payload, freeze_hash)
    print(json.dumps({'completed': name, 'checks': checks, 'seconds': payload['seconds_this_invocation'],
                      'descriptive_velocity_residuals': summaries}), flush=True)
    return payload


def main():
    assert sys.argv[1:] in ([], ['freeze'])
    extraction, multiplier, files = inputs()
    specification = {'files': files, 'models': {str(k): source.MODELS[k] for k in WIDTHS},
                     'jobs_per_source': [list(job) for job in JOBS], 'subpixels_per_axis': 8,
                     'stellar_multiplier': multiplier, 'helium_factor': source.HELIUM,
                     'r': law.RATIO, 'a0_kms2_kpc': density.A0_KMS2_KPC,
                     'oracle_radii_kpc': list(ring.RADII), 'oracle_orders': list(ring.ORDERS)}
    if sys.argv[1:] == ['freeze']:
        law.save_new(FREEZE, specification)
        return
    assert json.loads(FREEZE.read_text()) == specification
    freeze_hash = law.sha(FREEZE)
    if not QUALIFICATION.exists():
        publish(QUALIFICATION, qualification(extraction, multiplier), freeze_hash)
    qualified = authenticated(QUALIFICATION, freeze_hash)
    assert qualified['status'] == 'COMPLETE' and all(qualified['checks'].values()), 'Source failure preserved.'
    if not ORACLE.exists():
        publish(ORACLE, new_oracle(extraction, multiplier), freeze_hash)
    oracle = authenticated(ORACLE, freeze_hash)
    assert oracle['status'] == 'COMPLETE' and all(row['passed'] for row in oracle['checks']), 'Oracle failure preserved.'
    case_files = {}
    for width in WIDTHS:
        model = source.MODELS[width]
        qualification_row = next(row for row in qualified['models'] if row['model'] == model)
        for job in JOBS:
            name = identity(model, *job)
            path = ROOT/(name+'.json')
            result = authenticated(path, freeze_hash) if path.exists() else run_case(
                width, *job, extraction, multiplier, freeze_hash, oracle, qualification_row)
            assert result['case'] == name and result['model'] == model and result['width_arcsec'] == width
            assert result['stellar_multiplier'] == multiplier
            assert tuple(result[key] for key in ('N', 'extent', 'newtonian')) == job
            assert all(result['checks'].values()), 'Failed calculation preserved; diagnose before proceeding.'
            case_files[path.name] = law.sha(path)
            print(json.dumps({'verified_completed_case': name}), flush=True)
    final = {'status': 'COMPLETE', 'models': list(source.MODELS.values()),
             'case_files_sha256': case_files, 'oracle_sha256': law.sha(ORACLE),
             'source_qualification_sha256': law.sha(QUALIFICATION),
             'role': 'Two fixed-plane retained-HI source contrasts; no observational fit or native-gravity claim.'}
    if RESULT.exists():
        assert authenticated(RESULT, freeze_hash) == final
    else:
        publish(RESULT, final, freeze_hash)
    print(json.dumps({'status': 'COMPLETE', 'case_count': 8, 'models': final['models']}), flush=True)


if __name__ == '__main__':
    main()
