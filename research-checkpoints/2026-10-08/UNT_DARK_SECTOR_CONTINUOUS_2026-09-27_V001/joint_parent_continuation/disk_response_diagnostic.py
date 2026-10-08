"""Authenticated, no-refit algebraic postprocessing; no PDE or physics worker."""
import os
for name in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS',
             'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[name] = '1'
import hashlib
import json
import math
import sys
import numpy as np
import disk_solver as law
import galaxy_density as density

ROOT = law.ROOT
FREEZE = ROOT / 'DISK_RESPONSE_DIAGNOSTIC_FROZEN.json'
RESULT = ROOT / 'DISK_RESPONSE_DIAGNOSTIC_RESULTS.json'
MODELS = ((True, True), (False, True), (True, False), (False, False))
JOBS = ((256, 255, False), (320, 1023, False), (512, 255, False), (512, 255, True))


def case_name(hi, h2, n, extent, newton):
    return f'galaxy_HI{int(hi)}_H2{int(h2)}_N{n}_L{extent}_Newton{int(newton)}'


def inv(value):
    return 0. if value == 0 else float(law.inverse(value))


def mu(value):
    return 0. if value == 0 else float(law.f(value)) / value


def vector_radial(radial_flux, vertical_flux):
    norm = math.hypot(radial_flux, vertical_flux)
    return 0. if norm == 0 else radial_flux / norm * inv(norm)


def reconstruct_vertical(radial, sheet_flux):
    if sheet_flux == 0:
        return 0.
    lo, hi = 0., 2 * (sheet_flux + abs(radial) + law.RATIO)
    assert mu(math.hypot(radial, hi)) * hi >= sheet_flux
    for _ in range(70):
        mid = (lo + hi) / 2
        if mu(math.hypot(radial, mid)) * mid < sheet_flux:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def main():
    source_names = ('DISK_RESPONSE_DIAGNOSTIC.md', 'disk_response_diagnostic.py',
                    'GALAXY_FIELD_FROZEN.json', 'disk_solver.py', 'galaxy_density.py',
                    'NGC3198_BARYON_INPUT.json',
                    '../joint_parent_dynamics/SHAPE_REFERENCE_RESULTS.json')
    sources = {name: law.sha(ROOT / name) for name in source_names}
    if sys.argv[1:] == ['freeze']:
        law.save_new(FREEZE, {'files': sources, 'mode': 'postprocessing_no_fit',
                             'models': MODELS, 'required_jobs_per_model': JOBS})
        return
    assert not sys.argv[1:] and json.loads(FREEZE.read_text())['files'] == sources
    galaxy_freeze = ROOT / 'GALAXY_FIELD_FROZEN.json'
    galaxy_hash = law.sha(galaxy_freeze)
    for name, digest in json.loads(galaxy_freeze.read_text())['files'].items():
        assert law.sha(ROOT / name) == digest
    # Require the complete predetermined queue; never select completed successes.
    paths = [ROOT / (case_name(hi, h2, *job) + '.json')
             for hi, h2 in MODELS for job in JOBS]
    assert all(path.is_file() for path in paths), 'Wait for all 16 original cases.'
    cases, input_hashes = {}, {}
    for path in paths:
        record = json.loads(path.read_text())
        p = record['payload']
        assert record['freeze_sha256'] == galaxy_hash
        assert record['payload_sha256'] == hashlib.sha256(law.encode(p)).hexdigest()
        assert p['case'] == path.stem == case_name(
            p['hi_tail'], p['h2_tail'], p['N'], p['extent'], p['newtonian'])
        assert all(p['checks'].values())
        input_hashes[path.name] = law.sha(path)
        # Do not retain the large potential matrices; no evolution is performed.
        cases[path.stem] = {key: p[key] for key in
                           ('comparison', 'component_masses_Msun', 'radii')}
        del p, record
    checks, models = [], []

    def check(label, discrepancy, scale=1., tolerance=1e-11):
        allowance = tolerance * max(1., abs(scale))
        checks.append({'name': label, 'absolute_error': float(discrepancy),
                       'allowance': float(allowance),
                       'passed': bool(discrepancy <= allowance)})

    for hi, h2 in MODELS:
        label = f'HI{int(hi)}_H2{int(h2)}'
        actual, newton, base, remote = [cases[case_name(hi, h2, *job)] for job in
            ((512, 255, False), (512, 255, True), (256, 255, False), (320, 1023, False))]
        assert actual['radii'] == newton['radii']
        assert actual['component_masses_Msun'] == newton['component_masses_Msun']
        profiles = density.profiles(hi, h2)
        masses = density.masses(profiles)
        total_mass = sum(masses.values())
        for name, mass in masses.items():
            check(label + '/mass/' + name,
                  abs(actual['component_masses_Msun'][name] - mass), mass, 1e-13)
        knots = np.unique(np.concatenate([p.r for p in profiles.values()]))
        hard_edges = [float(p.r[-1]) for p in profiles.values() if p.tail is None and p.s[-1] > 0]
        centers = np.array(actual['radii'])
        spacing = np.gradient(centers)
        rows = []
        assert len(actual['comparison']) == len(newton['comparison']) == len(base['comparison']) == len(remote['comparison']) == 43
        for index, (a_row, n_row, b_row, r_row) in enumerate(zip(
                actual['comparison'], newton['comparison'], base['comparison'], remote['comparison'])):
            assert all(a_row[key] == row[key] for key in ('R', 'velocity', 'error')
                       for row in (n_row, b_row, r_row))
            radius, x, n = a_row['R'], a_row['radial_force_a0'], n_row['radial_force_a0']
            assert radius > 0 and all(math.isfinite(value) for value in (x, n))
            sigma = sum(float(p.sigma(radius)) for p in profiles.values())
            b = 2 * math.pi * density.G_KPC_KMS2_MSUN * 1e6 * sigma / density.A0_KMS2_KPC
            z = reconstruct_vertical(x, b)
            s = math.hypot(x, z)
            coefficient = mu(s)
            solenoidal = coefficient * x - n
            vector = vector_radial(n, b)
            radial = math.copysign(inv(abs(n)), n) if n else 0.
            deep = math.copysign(math.sqrt(abs(n)), n) if n else 0.
            flat = math.sqrt(density.G_KPC_KMS2_MSUN * total_mass / density.A0_KMS2_KPC) / radius
            terms = {'remaining_field': x - vector, 'vertical_projection': vector - radial,
                     'law_shape_vs_deep': radial - deep, 'newtonian_disk_vs_monopole': deep - flat}
            factor = radius * density.A0_KMS2_KPC
            v2_terms = {name: value * factor for name, value in terms.items()}
            observed_v2 = a_row['velocity'] ** 2
            reference_residual = factor * flat - observed_v2
            check(f'{label}/{index}/sheet_jump', abs(coefficient * z - b), b)
            check(f'{label}/{index}/flux_inversion', abs(vector_radial(n + solenoidal, b) - x), x)
            check(f'{label}/{index}/force_decomposition', abs(sum(terms.values()) - (x - flat)), max(abs(x), abs(flat)))
            check(f'{label}/{index}/v2_decomposition',
                  abs(sum(v2_terms.values()) + reference_residual - (factor * x - observed_v2)),
                  max(abs(factor * x), observed_v2, abs(factor * flat)))
            local_spacing = float(np.interp(radius, centers, spacing))
            edge_distance = min((abs(radius - edge) for edge in hard_edges), default=None)
            diagnostics = {'true': x, 'vector_algebraic': vector, 'radial_algebraic': radial,
                           'radial_deep': deep, 'total_mass_flat_reference': flat}
            rows.append({'R_kpc': radius, 'observed_velocity_kms': a_row['velocity'],
                'observed_error_kms': a_row['error'], 'sigma_Msun_pc2': sigma,
                'newtonian_radial_a0': n, 'sheet_flux_a0': b, 'reconstructed_vertical_a0': z,
                'total_field_a0': s, 'mu': coefficient, 'radial_solenoidal_flux_a0': solenoidal,
                'diagnostic_radial_fields_a0': diagnostics, 'force_terms_a0': terms,
                'signed_v2_terms_kms2': v2_terms,
                'reference_residual_v2_kms2': reference_residual,
                'true_residual_v2_kms2': factor * x - observed_v2,
                'diagnostic_velocities_kms': {key: math.sqrt(factor * value) if value >= 0 else None
                                             for key, value in diagnostics.items()},
                'mesh_shift_a0': x - b_row['radial_force_a0'],
                'remote_domain_shift_a0': r_row['radial_force_a0'] - b_row['radial_force_a0'],
                'nearest_knot_distance_kpc': float(np.min(abs(knots - radius))),
                'nearest_hard_edge_distance_kpc': edge_distance,
                'local_radial_center_spacing_kpc': local_spacing,
                'within_two_spacings_of_hard_edge': edge_distance is not None and edge_distance <= 2 * local_spacing})
        summaries = {}
        for lower in (0., 2., 8.):
            selected = [row for row in rows if row['R_kpc'] >= lower]
            means = {key: float(np.mean([row['signed_v2_terms_kms2'][key] for row in selected]))
                     for key in rows[0]['signed_v2_terms_kms2']}
            maxima = {key: max(abs(row['signed_v2_terms_kms2'][key]) for row in selected)
                      for key in means}
            summaries[f'R_ge_{lower:g}_kpc'] = {'count': len(selected),
                'hard_edge_warning_count': sum(row['within_two_spacings_of_hard_edge'] for row in selected),
                'mean_signed_v2_terms_kms2': means, 'max_abs_v2_terms_kms2': maxima,
                'mean_reference_residual_v2_kms2': float(np.mean([row['reference_residual_v2_kms2'] for row in selected])),
                'mean_true_residual_v2_kms2': float(np.mean([row['true_residual_v2_kms2'] for row in selected]))}
        models.append({'model': label, 'component_masses_Msun': masses,
                       'rows': rows, 'summaries_descriptive_only': summaries})
    payload = {'status': 'COMPLETE' if all(item['passed'] for item in checks) else 'FAILED',
               'input_sha256': input_hashes, 'models': models, 'checks': checks,
               'mode': 'postprocessing_existing_fields_no_new_fit_or_PDE'}
    law.save_new(RESULT, {'freeze_sha256': law.sha(FREEZE),
                         'payload_sha256': hashlib.sha256(law.encode(payload)).hexdigest(),
                         'payload': payload})
    print(json.dumps({'status': payload['status'], 'models': len(models),
                      'rows': sum(len(model['rows']) for model in models), 'checks': len(checks)}))
    assert payload['status'] == 'COMPLETE'


if __name__ == '__main__':
    main()
