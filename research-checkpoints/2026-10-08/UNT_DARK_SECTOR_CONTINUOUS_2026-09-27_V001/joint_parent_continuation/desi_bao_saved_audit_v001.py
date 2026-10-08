"""Independent saved-data arithmetic only: no distance integration or fitting search."""
import hashlib
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent


def encode(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def sha(path):
    path = path.resolve(strict=True)
    path.relative_to(ROOT)
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dot(a, b):
    return math.fsum(x*y for x, y in zip(a, b))


def solve(matrix, vector):
    """Independent partial-pivot Gaussian elimination; only 13 by 13."""
    n = len(vector)
    a = [list(row) + [v] for row, v in zip(matrix, vector)]
    for i in range(n):
        p = max(range(i, n), key=lambda k: abs(a[k][i]))
        a[i], a[p] = a[p], a[i]
        assert a[i][i] != 0
        for j in range(i+1, n):
            factor = a[j][i] / a[i][i]
            for k in range(i, n+1):
                a[j][k] -= factor*a[i][k]
    x = [0.]*n
    for i in range(n-1, -1, -1):
        x[i] = (a[i][-1]-math.fsum(a[i][j]*x[j] for j in range(i+1, n)))/a[i][i]
    return x


def main():
    files = {}
    def read(name):
        path = HERE/name
        files[name] = sha(path)
        return json.loads(path.read_text())
    frozen = read('DESI_BAO_SHAPE_V001_FROZEN.json')
    wrapper = read('DESI_BAO_SHAPE_V001_RESULTS.json')
    p = wrapper['payload']
    assert wrapper['freeze_sha256'] == files['DESI_BAO_SHAPE_V001_FROZEN.json']
    assert hashlib.sha256(encode(p)).hexdigest() == wrapper['payload_sha256']
    for name, expected in frozen['files'].items():
        assert sha(ROOT/name) == expected, name
    assert p['configuration'] == frozen['configuration']
    assert p['status'] == 'COMPLETE' and p['checks']['failed'] == 0
    assert p['checks']['total'] == 1160 and not p['checks']['failure_names']
    cfg = p['configuration']
    closure = read('COSMOLOGY_CLOSURE_ARITHMETIC.json')
    assert len(closure['rows']) == len(p['references']) == len(p['reference_metadata']) == 18
    mean_path = HERE/'desi_dr2_bao_external_v001/desi_gaussian_bao_ALL_GCcomb_mean.txt'
    cov_path = HERE/'desi_dr2_bao_external_v001/desi_gaussian_bao_ALL_GCcomb_cov.txt'
    raw = [line.split() for line in mean_path.read_text().splitlines()
           if line.strip() and not line.lstrip().startswith('#')]
    data = [dict(index=i, z=float(row[0]), quantity=row[2], value=float(row[1]))
            for i, row in enumerate(raw)]
    cov = [[float(x) for x in line.split()] for line in cov_path.read_text().splitlines()
           if line.strip() and not line.lstrip().startswith('#')]
    assert p['data']['order'] == data and p['data']['covariance'] == cov
    assert len(data) == len(cov) == 13 and all(len(row) == 13 for row in cov)
    assert [(r['z'], r['quantity']) for r in data] == [tuple(row) for row in frozen['expected_data_order']]
    y = [r['value'] for r in data]
    z = [r['z'] for r in data]
    labels = [r['quantity'] for r in data]
    checks, errors, fit_count = {}, {}, 0
    def close(category, actual, expected, tol=3e-11):
        if isinstance(actual, list):
            assert isinstance(expected, list) and len(actual) == len(expected)
            for a, b in zip(actual, expected):
                close(category, a, b, tol)
            return
        error = abs(actual-expected)
        scale = max(1., abs(actual), abs(expected))
        assert math.isfinite(error) and error <= tol*scale, (category, actual, expected)
        errors[category] = max(errors.get(category, 0.), error)
        checks[category] = checks.get(category, 0)+1
    lower = [[0.]*13 for _ in range(13)]
    for i in range(13):
        for j in range(i+1):
            value = cov[i][j]-dot(lower[i][:j], lower[j][:j])
            if i == j:
                assert value > 0
                lower[i][j] = math.sqrt(value)
            else:
                lower[i][j] = value/lower[j][j]
    def whiten(v):
        answer = []
        for i in range(13):
            answer.append((v[i]-dot(lower[i][:i], answer))/lower[i][i])
        return answer
    def audit_fit(fit, shape=None, observed=None):
        nonlocal fit_count
        obs = y if observed is None else observed
        assert len(fit['prediction']) == len(fit['residual']) == len(fit['whitened_residual']) == 13
        if shape is None:
            assert fit['A'] > 0
            shape = [x/fit['A'] for x in fit['prediction']]
        inv_d, inv_y = solve(cov, shape), solve(cov, obs)
        den, num = dot(shape, inv_d), dot(shape, inv_y)
        raw_a = num/den
        amplitude = max(0., raw_a)
        close('amplitude', fit['A'], amplitude)
        close('amplitude', fit['A_unconstrained'], raw_a)
        assert fit['boundary_active'] == (raw_a <= 0.)
        close('prediction', fit['prediction'], [amplitude*v for v in shape])
        residual = [v-w for v, w in zip(obs, fit['prediction'])]
        close('residual', fit['residual'], residual)
        close('whitened_residual', fit['whitened_residual'], whiten(residual))
        score = dot(residual, solve(cov, residual))
        close('covariance_score', fit['chi2'], score)
        close('hessian', fit['amplitude_hessian'], 2*den)
        gradient = 2*(fit['A']*den-num)
        close('gradient_scaled', fit['amplitude_gradient']/max(1., 2*num), gradient/max(1., 2*num))
        if fit['A'] > 0:
            close('acoustic_units', fit['H0_rd_km_s'], cfg['c_m_s']/1000/fit['A'])
        else:
            assert fit['H0_rd_km_s'] is None
        fit_count += 1
        return shape
    def audit_pairs(pairs, prediction):
        assert len(pairs) == 6
        for pair, pair_z in zip(pairs, sorted(set(z))[1:]):
            indices = [i for i, zz in enumerate(z) if zz == pair_z]
            im = next(i for i in indices if labels[i] == 'DM_over_rs')
            ih = next(i for i in indices if labels[i] == 'DH_over_rs')
            assert pair['z'] == pair_z and pair['original_indices_DM_DH'] == [im, ih]
            cc = [[cov[i][j] for j in [im, ih]] for i in [im, ih]]
            assert pair['covariance_DM_DH'] == cc
            close('AP_correlation', pair['correlation'], cc[0][1]/math.sqrt(cc[0][0]*cc[1][1]))
            grad = [1/y[ih], -y[im]/y[ih]**2]
            variance = sum(grad[i]*cc[i][j]*grad[j] for i in (0,1) for j in (0,1))
            close('AP_sigma', pair['AP_delta_method_sigma'], math.sqrt(variance))
            close('AP_ratio', pair['AP_observed'], y[im]/y[ih])
            close('AP_prediction', pair['AP_prediction'], prediction[im]/prediction[ih])
    groups = {}
    for index, (ref, result, old) in enumerate(zip(p['reference_metadata'], p['references'], closure['rows'])):
        assert ref['reference'] == result['reference'] == index
        assert ref['reference_input'] == old['reference_input'] and ref['bbn'] == old['bbn']
        assert ref['reference_case'] == old['reference_case']
        inp = old['reference_input']
        close('density', ref['Omega_m'], 1-inp['Omega_Lambda_ref'])
        close('density', ref['Omega_b'], old['bbn']['omega_b']/(inp['H0_km_s_Mpc']/100)**2)
        close('density', ref['Omega_exc'], old['reference_H0_missing_Omega'])
        close('density', ref['Omega_b']+ref['Omega_exc'], ref['Omega_m'])
        assert ref['Omega_Lambda'] == inp['Omega_Lambda_ref'] and ref['H0_km_s_Mpc'] == inp['H0_km_s_Mpc']
        groups.setdefault(ref['Omega_m'].hex(), []).append(index)
        audit_fit(result['fit'], result['shape'])
        audit_fit(result['precision_controls']['simpson2048_fit'])
        close('acoustic_units', result['conditional_rd_Mpc'], result['fit']['H0_rd_km_s']/ref['H0_km_s_Mpc'])
        contribution = [r*v for r, v in zip(result['fit']['residual'], solve(cov, result['fit']['residual']))]
        close('covariance_contributions', result['covariance_residual_contributions'], contribution)
        audit_pairs(result['pair_diagnostics'], result['fit']['prediction'])
        for i, label in enumerate(labels):
            if label == 'DH_over_rs':
                close('algebraic_DH', result['shape'][i], 1/math.sqrt(ref['Omega_m']*(1+z[i])**3+ref['Omega_Lambda']))
    assert list(groups.values()) == p['duplicate_shape_groups'] and len(groups) == 3
    profiles = p['comparator']['profiles']
    assert [row['grid_count'] for row in profiles] == [257, 513]
    for profile in profiles:
        n = profile['grid_count']
        xs, scores, amps = [profile[k] for k in ('grid_Omega_m', 'grid_chi2', 'grid_A')]
        assert len(xs) == len(scores) == len(amps) == n
        close('profile_grid', xs, [i/(n-1) for i in range(n)])
        local = [i for i in range(1,n-1) if scores[i] <= scores[i-1] and scores[i] <= scores[i+1]]
        assert local == profile['sampled_local_minimum_indices']
        candidates = profile['candidates']
        assert len(candidates) == len(local)+3
        assert [c['kind'] for c in candidates[:3]] == ['finite_left_endpoint','finite_right_endpoint','best_grid_point']
        assert [c['Omega_m'] for c in candidates[:2]] == [0.,1.]
        imin = min(range(n), key=lambda i: scores[i])
        assert candidates[2]['index'] == imin and candidates[2]['Omega_m'] == xs[imin]
        close('grid_candidate_score', candidates[2]['fit']['chi2'], scores[imin])
        for candidate, i in zip(candidates[3:], local):
            assert candidate['index'] == i and candidate['bracket'] == [xs[i-1],xs[i+1]]
            assert xs[i-1] <= candidate['Omega_m'] <= xs[i+1]
        best_index = min(range(len(candidates)), key=lambda i: (candidates[i]['fit']['chi2'],candidates[i]['Omega_m']))
        assert profile['best_candidate_index'] == best_index and profile['best'] == candidates[best_index]
        for candidate in candidates:
            shape = audit_fit(candidate['fit'])
            audit_fit(candidate['simpson_fit'])
            for i, label in enumerate(labels):
                if label == 'DH_over_rs':
                    close('algebraic_DH', shape[i], 1/math.sqrt(candidate['Omega_m']*(1+z[i])**3+1-candidate['Omega_m']))
    best = profiles[-1]['best']
    audit_pairs(best['pair_diagnostics'], best['fit']['prediction'])
    for result in p['references']:
        close('score_difference', result['chi2_minus_extra_shape_fit'], result['fit']['chi2']-best['fit']['chi2'])
    synthetic = p['synthetic_controls']['amplitude']
    synthetic_d = [v/cfg['synthetic_A'] for v in synthetic['prediction']]
    audit_fit(synthetic, synthetic_d, [cfg['synthetic_A']*v for v in synthetic_d])
    audit_fit(p['synthetic_controls']['nonpositive_boundary'], synthetic_d, [-v for v in synthetic_d])
    radiation = p['radiation_omission']['rows']
    assert len(radiation) == 108
    temperatures = [cfg['temperature_K']-cfg['temperature_error_K'],cfg['temperature_K'],cfg['temperature_K']+cfg['temperature_error_K']]
    expected_ids = [(i,t,n) for i in range(18) for t in temperatures for n in cfg['illustrative_Neff']]
    assert [(r['reference'],r['temperature_K'],r['illustrative_Neff']) for r in radiation] == expected_ids
    for row in radiation:
        ref = p['reference_metadata'][row['reference']]
        energy = 8*math.pi**5*cfg['boltzmann_J_K']**4*row['temperature_K']**4/(15*cfg['planck_h_J_s']**3*cfg['c_m_s']**3)
        h0 = ref['H0_km_s_Mpc']*1000/cfg['mpc_m']
        gamma = 8*math.pi*cfg['G_SI']*energy/(3*h0*h0*cfg['c_m_s']**2)
        wr = gamma*(1+7/8*(4/11)**(4/3)*row['illustrative_Neff'])
        close('radiation_density', row['Omega_gamma'], gamma)
        close('radiation_density', row['Omega_rad'], wr)
        close('radiation_H0', row['H_at_zero_over_inherited_H0'], math.sqrt(1+wr))
        q = [wr*(1+zz)**4/(ref['Omega_m']*(1+zz)**3+ref['Omega_Lambda']) for zz in z]
        hfrac = [math.sqrt(1+qq)-1 for qq in q]
        bound = 1-1/math.sqrt(1+max(q))
        close('radiation_H', row['H_fractional_increase'], hfrac)
        close('radiation_bound', row['all_z_H_increase_upper_bound'], max(hfrac))
        close('radiation_bound', row['all_z_distance_decrease_upper_bound'], bound)
        assert len(row['distance_fractional_decrease']) == 13
        for i, change in enumerate(row['distance_fractional_decrease']):
            assert -cfg['identity_tolerance'] <= change <= bound+cfg['identity_tolerance']
            if labels[i] == 'DH_over_rs':
                close('radiation_DH', change, 1-1/math.sqrt(1+q[i]))
    shape_summary = []
    for group in groups.values():
        ref, result = p['reference_metadata'][group[0]], p['references'][group[0]]
        shape_summary.append(dict(references=group, Omega_m=ref['Omega_m'], A=result['fit']['A'],
            chi2=result['fit']['chi2'], chi2_minus_free_shape=result['chi2_minus_extra_shape_fit'],
            conditional_rd_Mpc_range=[min(p['references'][i]['conditional_rd_Mpc'] for i in group),max(p['references'][i]['conditional_rd_Mpc'] for i in group)]))
    files[Path(__file__).name] = sha(Path(__file__))
    result = dict(status='COMPLETE_SAVED_ARITHMETIC_AUDIT', files=files,
        original_payload_sha256=wrapper['payload_sha256'], frozen_member_count=len(frozen['files']),
        census=dict(reference_rows=18, unique_shapes=3, observations=13, pair_diagnostics_per_curve=6,
            comparator_grids=[257,513], comparator_candidates=[len(x['candidates']) for x in profiles],
            radiation_rows=108, recombined_fit_records=fit_count),
        checks=checks, total_arithmetic_comparisons=sum(checks.values()),maximum_absolute_errors=errors,
        shape_groups=shape_summary,
        comparator=dict(Omega_m=best['Omega_m'], A=best['fit']['A'], chi2=best['fit']['chi2'],
            H0_rd_km_s=best['fit']['H0_rd_km_s'], selected_kind=best['kind'],
            grid_differences={key:abs(profiles[0]['best']['fit'][key]-best['fit'][key]) for key in ['A','chi2']}),
        radiation=dict(max_distance_fractional_decrease=max(max(r['distance_fractional_decrease']) for r in radiation),
            max_H_fractional_increase=max(max(r['H_fractional_increase']) for r in radiation),
            H_at_zero_over_inherited_H0_range=[min(r['H_at_zero_over_inherited_H0'] for r in radiation),max(r['H_at_zero_over_inherited_H0'] for r in radiation)]),
        producer=dict(check_count=p['checks']['total'],runtime_seconds=p['runtime_seconds'],peak_self_rss_bytes=p['peak_self_rss_bytes']),
        scope='Saved arithmetic and custody only. No producer import, distance integration, optimizer search or eigensolver. Comparator candidate shapes are reconstructed from their saved prediction/A; full grid scores are not independently recomputed. Radiation DM/DV integrals and quadrature convergence remain the original frozen producer evidence. No new observational acceptance threshold or significance calculation.')
    print(encode(dict(payload=result,payload_sha256=hashlib.sha256(encode(result)).hexdigest())).decode())


if __name__ == '__main__':
    main()
