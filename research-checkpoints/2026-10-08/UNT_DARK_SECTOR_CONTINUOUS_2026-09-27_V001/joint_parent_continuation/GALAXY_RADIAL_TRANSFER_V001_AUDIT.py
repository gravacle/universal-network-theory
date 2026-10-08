"""Independent saved-array audit only: no producer/helper imports or fitting."""
import hashlib
import json
import math
import os
from pathlib import Path
import statistics
import tempfile
import time

J = Path(__file__).resolve().parent
STEM = 'GALAXY_RADIAL_TRANSFER_V001'
CONV = 1e6 / 3.085677581491367e19
FIXED = ('baryons', 'inherited_calibrated', 'rar_calibrated')
GRIDS = (257, 513)
checks = []


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def digest(v):
    return hashlib.sha256(json.dumps(v, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()).hexdigest()


def read(name):
    return json.loads((J / name).read_text())


def ck(name, passed):
    checks.append({'name': name, 'passed': bool(passed)})


def close(a, b, tol=2e-12):
    return math.isfinite(a) and math.isfinite(b) and abs(a-b) <= tol*max(1., abs(a), abs(b))


def eqarray(a, b):
    return len(a) == len(b) and all(close(x, y) for x, y in zip(a, b))


def mean(a):
    return math.fsum(a) / len(a)


def metrics(pred, rows, n):
    residual = [p-r['vobs_kms'] for p, r in zip(pred, rows)]
    logs = [2*math.log10(p/r['vobs_kms']) for p, r in zip(pred, rows)]
    return {'residual_kms': residual, 'residual_dex': logs,
        'quoted_error_residual': [v/r['evobs_kms'] for v, r in zip(residual, rows)],
        'gpred_si': [CONV*p*p/r['R_kpc'] for p, r in zip(pred, rows)],
        'inner': {'velocity_mse': mean([x*x for x in residual[:n]]), 'logg_mse': mean([x*x for x in logs[:n]])},
        'outer': {'velocity_mse': mean([x*x for x in residual[n:]]), 'logg_mse': mean([x*x for x in logs[n:]])}}


def audit_metric(label, saved, rows, n):
    pred = saved['prediction_kms']
    ck(label+'/positive_full_prediction', len(pred) == len(rows) and all(math.isfinite(x) and x > 0 for x in pred))
    got = metrics(pred, rows, n)
    for k in ('residual_kms', 'residual_dex', 'quoted_error_residual', 'gpred_si'):
        ck(label+'/'+k, eqarray(got[k], saved[k]))
    for side in ('inner', 'outer'):
        for k in ('velocity_mse', 'logg_mse'):
            ck(label+'/'+side+'/'+k, close(got[side][k], saved[side][k]))
    return got


def summary_pair(data, other):
    rows = []
    for r in data:
        n, o = r['metrics']['inherited_calibrated']['velocity_mse'], r['metrics'][other]['velocity_mse']
        d = n-o
        tol = 1e-10*max(1., n, o)
        rows.append({'name': r['name'], 'network_mse': n, 'other_mse': o, 'difference': d,
            'kind': r['kinds'].get(other), 'amplitude_zero': r['zero'].get(other),
            'outcome': 'tie' if abs(d) <= tol else ('network_win' if d < 0 else 'network_loss')})
    diffs = [r['difference'] for r in rows]
    gains = sorted(rows, key=lambda r: (r['difference'], r['name']))
    losses = sorted(rows, key=lambda r: (-r['difference'], r['name']))
    absolute = sorted(rows, key=lambda r: (-abs(r['difference']), r['name']))
    def subset(rr):
        return {'n': len(rr), 'network_mse': mean([r['network_mse'] for r in rr]),
            'other_mse': mean([r['other_mse'] for r in rr]),
            'paired_mean': mean([r['difference'] for r in rr]),
            'paired_median': statistics.median(r['difference'] for r in rr)} if rr else None
    out = {'wins': sum(r['outcome'] == 'network_win' for r in rows),
        'ties': sum(r['outcome'] == 'tie' for r in rows),
        'losses': sum(r['outcome'] == 'network_loss' for r in rows),
        'all': subset(rows), 'median_network_mse': statistics.median(r['network_mse'] for r in rows),
        'median_other_mse': statistics.median(r['other_mse'] for r in rows),
        'top5_network_gains': gains[:5], 'top5_network_losses': losses[:5],
        'top5_absolute_contributors': absolute[:5], 'per_galaxy': rows,
        'leave_out': {}}
    for k in (1, 5):
        for label, ordering in (('largest_network_gains', gains), ('largest_absolute_differences', absolute)):
            omitted = {r['name'] for r in ordering[:k]}
            out['leave_out'][f'{label}_{k}'] = {'omitted': sorted(omitted), **subset([r for r in rows if r['name'] not in omitted])}
    if other.startswith(('NFW_', 'ISO_')):
        boundary = {'finite_lower_boundary', 'finite_upper_boundary', 'zero_scale_limit', 'infinite_scale_limit', 'zero_amplitude_scale_unidentified'}
        out['boundary_strata'] = {label: subset([r for r in rows if (r['kind'] in boundary) == flag])
            for label, flag in (('selected_boundary_or_limit', True), ('selected_interior', False))}
        out['by_selected_kind'] = {kind: subset([r for r in rows if r['kind'] == kind]) for kind in sorted({r['kind'] for r in rows})}
        out['top5_gain_fraction_of_net_gain'] = math.fsum(r['difference'] for r in gains[:5])/math.fsum(diffs) if math.fsum(diffs) else None
    return out


def main():
    started = time.perf_counter()
    result = read(STEM+'_RESULT.json')
    freeze = read(STEM+'_FROZEN.json')
    tests = read(STEM+'_TESTS.json')
    source = read('SPARC_EFFECTIVE_TRANSFER_V001_RESULT.json')
    fh = sha(J/(STEM+'_FROZEN.json'))
    ck('result_hash', sha(J/(STEM+'_RESULT.json')) == '77883bc7e0da4ceaf1d623ba835be6dc3c0666dd0b56d0b00aa36e551247f7c0')
    ck('freeze_copy', result['freeze'] == freeze)
    for name, h in freeze['files'].items():
        ck('frozen_file/'+name, sha(J/name) == h)
    ck('synthetic_pin', result['synthetic_tests_sha256'] == sha(J/(STEM+'_TESTS.json')) and tests['freeze_sha256'] == fh)
    for i, c in enumerate(tests['controls']):
        ck('synthetic/'+str(i), c['passed'] == (math.isfinite(c['error']) and c['error'] <= c['gate']) and c['passed'])
    grouped = {}
    for row in source['central']['predictions']:
        if row['role'] == 'evaluation':
            grouped.setdefault(row['name'], []).append(row)
    groups = [(name, sorted(rows, key=lambda r: (r['R_kpc'], r['source_line']))) for name, rows in sorted(grouped.items())]
    ck('evaluation_count', len(groups) == 100)
    data, excluded, counts, control_count, tied_splits = [], [], {}, 0, []
    relative_velocity, galaxy_relative_means = [], []
    for i, (name, rows) in enumerate(groups):
        filename = f'galaxy_{i:03d}.json'
        path = J/(STEM+'_CASES')/filename
        receipt = json.loads(path.read_text())
        n, nr = len(rows)//2, len(rows)
        ck(name+'/case_hash', result['case_sha256'][filename] == sha(path))
        ck(name+'/provenance', receipt['rows'] == rows and receipt['rows_sha256'] == digest(rows) and receipt['freeze_sha256'] == fh)
        expected_census = {'index': i, 'name': name, 'n': nr, 'n_inner': n, 'eligible': nr >= 6, 'rows_sha256': digest(rows)}
        ck(name+'/census', freeze['census'][i] == expected_census and receipt['index'] == i and receipt['name'] == name and receipt['n'] == nr and receipt['n_inner'] == n)
        ck(name+'/outcome', result['outcomes'][i] == {'index': i, 'name': name, 'status': receipt['status']})
        if nr < 6:
            ck(name+'/exclusion', receipt['status'] == 'EXCLUDED_LT6')
            excluded.append({'name': name, 'n': nr, 'reason': receipt['reason']})
            continue
        ck(name+'/qualified', receipt['status'] == 'QUALIFIED')
        ck(name+'/mask', receipt['inner_indices'] == list(range(n)) and receipt['outer_indices'] == list(range(n, nr)))
        ck(name+'/pivot', receipt['pivot_inner_kpc'] == statistics.median(r['R_kpc'] for r in rows[:n]))
        if receipt['split_radius_tied']:
            tied_splits.append(name)
        for c in receipt['controls']:
            control_count += 1
            ck(name+'/control/'+c['name'], c['passed'] == (math.isfinite(c['error']) and c['error'] <= c['gate']) and c['passed'])
        inner_data = {'r': [r['R_kpc'] for r in rows[:n]], 'b2': [r['gbar_si']*r['R_kpc']/CONV for r in rows[:n]], 'v': [r['vobs_kms'] for r in rows[:n]]}
        ck(name+'/inner_input_hash', receipt['inner_input_sha256'] == digest(inner_data))
        entry = {'name': name, 'metrics': {}, 'kinds': {}, 'zero': {}, 'n_outer': nr-n}
        for label in FIXED:
            got = audit_metric(name+'/'+label, receipt['fixed'][label], rows, n)
            ck(name+'/'+label+'/frozen_prediction', eqarray(receipt['fixed'][label]['prediction_kms'], [math.sqrt(r['gpred_si'][label]*r['R_kpc']/CONV) for r in rows]))
            entry['metrics'][label] = got['outer']
        vr = receipt['fixed']['rar_calibrated']['prediction_kms'][n:]
        vn = receipt['fixed']['inherited_calibrated']['prediction_kms'][n:]
        frac = [a/b-1 for a, b in zip(vn, vr)]
        relative_velocity.extend(frac)
        galaxy_relative_means.append(mean(frac))
        for model in ('NFW', 'ISO'):
            for count, fit in zip(GRIDS, receipt['halo_fits'][model]):
                label = f'{model}_{count}'
                got = audit_metric(name+'/'+label, fit['readout'], rows, n)
                selected = fit['selected']
                ck(name+'/'+label+'/fit', fit['grid_count'] == count and fit['pivot_kpc'] == receipt['pivot_inner_kpc'] and selected['amplitude'] >= 0 and selected['inner_sse'] == min(c['inner_sse'] for c in fit['candidates']))
                ck(name+'/'+label+'/objective', close(n*got['inner']['velocity_mse'], selected['inner_sse']))
                entry['metrics'][label] = got['outer']
                entry['kinds'][label] = selected['kind']
                entry['zero'][label] = selected['amplitude'] == 0
                c = counts.setdefault(label, {'galaxies': 0, 'amplitude_zero': 0, 'scale_unidentified': 0, 'selected_kinds': {}})
                c['galaxies'] += 1
                c['amplitude_zero'] += selected['amplitude'] == 0
                c['scale_unidentified'] += selected['scale_unidentified_at_zero_amplitude']
                c['selected_kinds'][selected['kind']] = c['selected_kinds'].get(selected['kind'], 0)+1
        for key, difference in receipt['paired_outer_differences'].items():
            other = key.removeprefix('network_minus_')
            for metric in ('velocity_mse', 'logg_mse'):
                ck(name+'/'+key+'/'+metric, close(difference[metric], entry['metrics']['inherited_calibrated'][metric]-entry['metrics'][other][metric]))
        ck(name+'/aggregate_pair_copy', result['paired_per_galaxy'][len(data)] == {'name': name, 'differences': receipt['paired_outer_differences']})
        data.append(entry)
    ck('census_complete', len(data) == result['eligible'] == 94 and result['census'] == 100 and len(excluded) == 6)
    ck('exclusions_complete', result['excluded'] == [{k: r[k] for k in ('name', 'reason')} for r in excluded])
    ck('boundary_counts', counts == result['boundary_frequencies'])
    ck('complete_status', result['status'] == 'QUALIFIED_COMPLETE_CENSUS' and result['numerical_failures'] == {})
    aggregates = {label: {metric: mean([r['metrics'][label][metric] for r in data]) for metric in ('velocity_mse', 'logg_mse')} for label in data[0]['metrics']}
    for label, vals in aggregates.items():
        for metric, v in vals.items():
            ck('aggregate/'+label+'/'+metric, close(v, result['outer_galaxy_balanced_MSE'][label][metric]))
    robust = {other: summary_pair(data, other) for other in ('baryons', 'rar_calibrated', 'NFW_257', 'NFW_513', 'ISO_257', 'ISO_513')}
    output = {'status': 'SAVED_ARRAY_AUDIT_PASSED' if all(c['passed'] for c in checks) else 'SAVED_ARRAY_AUDIT_FAILED',
        'scope': 'Independent saved arithmetic only. No force, fit, producer or trajectory rerun. Robustness is posthoc descriptive, not new gates or blind validation.',
        'pins': {'audit_source': sha(Path(__file__)), 'result': sha(J/(STEM+'_RESULT.json')), 'freeze': fh, 'synthetic': sha(J/(STEM+'_TESTS.json'))},
        'checks': {'total': len(checks), 'passed': sum(c['passed'] for c in checks), 'failed': [c for c in checks if not c['passed']]},
        'saved_controls': {'synthetic': len(tests['controls']), 'eligible_galaxy': control_count},
        'census': 100, 'eligible': len(data), 'excluded': excluded, 'outer_rows': sum(r['n_outer'] for r in data),
        'tied_split_radii': tied_splits, 'aggregate': aggregates, 'boundary_counts': counts,
        'network_vs_RAR_outer_velocity_spread': {'denominator': 'RAR velocity; separately frozen calibrated a0 values',
            'rows': len(relative_velocity), 'median_absolute_fraction': statistics.median(map(abs, relative_velocity)),
            'maximum_absolute_fraction': max(map(abs, relative_velocity)),
            'median_signed_fraction': statistics.median(relative_velocity),
            'mean_signed_fraction_row_weighted': mean(relative_velocity),
            'mean_signed_fraction_galaxy_balanced': mean(galaxy_relative_means)},
        'posthoc_paired_velocity_robustness': robust, 'tie_rule': 'abs(network-other)<=1e-10*max(1,network,other)',
        'seconds': time.perf_counter()-started}
    target = J/(STEM+'_AUDIT.json')
    blob = (json.dumps(output, indent=2, allow_nan=False)+'\n').encode()
    with tempfile.NamedTemporaryFile(dir=J, prefix=target.name+'.partial.', delete=False) as f:
        temporary = Path(f.name)
        f.write(blob)
        f.flush()
        os.fsync(f.fileno())
    try:
        os.link(temporary, target)
    finally:
        temporary.unlink()
    small = {k: {x: v[x] for x in ('wins', 'ties', 'losses', 'all', 'leave_out')} for k, v in robust.items()}
    print(json.dumps({'status': output['status'], 'checks': output['checks'], 'controls': output['saved_controls'], 'aggregate': aggregates, 'boundaries': counts, 'robustness': small, 'sha256': sha(target), 'seconds': output['seconds']}))


if __name__ == '__main__':
    main()
