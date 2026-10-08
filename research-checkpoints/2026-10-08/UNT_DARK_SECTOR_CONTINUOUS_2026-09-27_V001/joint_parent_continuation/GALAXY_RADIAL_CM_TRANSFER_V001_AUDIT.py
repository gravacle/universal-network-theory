"""Independent saved c(M) arithmetic; no producer/helper imports or refitting."""
import hashlib
import json
import math
import os
from pathlib import Path
import statistics
import tempfile
import time

J = Path(__file__).resolve().parent
STEM = 'GALAXY_RADIAL_CM_TRANSFER_V001'
OLD = 'GALAXY_RADIAL_TRANSFER_V001'
KPC, MSUN, GSI = 3.085677581491367e19, 1.98847e30, 6.67430e-11
G, H, LITTLE_H, FB = GSI*MSUN/(KPC*1e6), .0671, .671, .0490/.3175
CONV = 1e6/KPC
SCENARIOS = {'central': 0., 'minus_0p11': -.11, 'plus_0p11': .11}
checks, maxima = [], {}


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def digest(v):
    return hashlib.sha256(json.dumps(v, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()).hexdigest()


def read(name):
    return json.loads((J/name).read_text())


def ck(name, passed):
    checks.append({'name': name, 'passed': bool(passed)})


def error(a, b):
    return abs(a-b)/max(1., abs(a), abs(b))


def numerical(name, category, a, b, gate=1e-10):
    if isinstance(a, list):
        value = max((error(x, y) for x, y in zip(a, b)), default=0.) if len(a) == len(b) else math.inf
    else:
        value = error(a, b)
    maxima[category] = max(maxima.get(category, 0.), value)
    ck(name, math.isfinite(value) and value <= gate)


def mean(a):
    return math.fsum(a)/len(a)


def mass_function(x):
    if x < .01:
        # m(x)=-ln(1-q)-q=sum(q^n/n,n>=2), q=x/(1+x).
        q, terms = x/(1+x), []
        power = q*q
        for n in range(2, 80):
            term = power/n
            terms.append(term)
            if term < terms[0]*1e-18:
                break
            power *= q
        return math.fsum(terms)
    return math.log1p(x)-x/(1+x)


def params(logmass, delta):
    mass = 10**logmass
    c = 10**(.905-.101*math.log10(mass*LITTLE_H/1e12)+delta)
    r200 = (G*mass/(100*H*H))**(1/3)
    return mass, c, r200


def prediction(logmass, delta, radii, b2):
    if logmass is None:
        return [math.sqrt(b) for b in b2]
    mass, c, r200 = params(logmass, delta)
    norm = G*(1-FB)*mass/mass_function(c)
    return [math.sqrt(b+norm*mass_function(r*c/r200)/r) for r, b in zip(radii, b2)]


def readout(pred, rows, n):
    res = [p-r['vobs_kms'] for p, r in zip(pred, rows)]
    dex = [2*math.log10(p/r['vobs_kms']) for p, r in zip(pred, rows)]
    return {'prediction_kms': pred, 'residual_kms': res, 'residual_dex': dex,
        'quoted_error_residual': [x/r['evobs_kms'] for x, r in zip(res, rows)],
        'gpred_si': [CONV*p*p/r['R_kpc'] for p, r in zip(pred, rows)],
        'inner': {'velocity_mse': mean([x*x for x in res[:n]]), 'logg_mse': mean([x*x for x in dex[:n]])},
        'outer': {'velocity_mse': mean([x*x for x in res[n:]]), 'logg_mse': mean([x*x for x in dex[n:]])}}


def pair_summary(rows):
    def summary(rr):
        return {'n': len(rr), 'network_mean': mean([r['network'] for r in rr]),
            'cm_mean': mean([r['cm'] for r in rr]), 'paired_mean': mean([r['difference'] for r in rr]),
            'paired_median': statistics.median(r['difference'] for r in rr)}
    gains = sorted(rows, key=lambda r: (r['difference'], r['name']))
    absolute = sorted(rows, key=lambda r: (-abs(r['difference']), r['name']))
    out = {'all': summary(rows), 'wins': sum(r['outcome'] == 'win' for r in rows),
        'ties': sum(r['outcome'] == 'tie' for r in rows), 'losses': sum(r['outcome'] == 'loss' for r in rows),
        'median_network': statistics.median(r['network'] for r in rows),
        'median_cm': statistics.median(r['cm'] for r in rows),
        'top5_gains': gains[:5], 'top5_losses': sorted(rows, key=lambda r: (-r['difference'], r['name']))[:5],
        'top5_absolute': absolute[:5], 'leave_out': {}, 'per_galaxy': rows}
    for k in (1, 5):
        for label, order in (('largest_gains', gains), ('largest_absolute', absolute)):
            omitted = {r['name'] for r in order[:k]}
            out['leave_out'][f'{label}_{k}'] = {'omitted': sorted(omitted), **summary([r for r in rows if r['name'] not in omitted])}
    return out


def main():
    started = time.perf_counter()
    result, freeze, tests = (read(STEM+s+'.json') for s in ('_RESULT', '_FROZEN', '_TESTS'))
    previous = read(OLD+'_RESULT.json')
    fh = sha(J/(STEM+'_FROZEN.json'))
    ck('result_pin', sha(J/(STEM+'_RESULT.json')) == '22e23d920de4df97361fa2e633b316dea36b2f76878c0f0334d9b85c55ae619a')
    ck('source_pin', sha(J/'galaxy_radial_cm_transfer_v001.py') == 'b12d2a4a320063edd05b578a85c4d97c32121509632ba4e969e20cb0694bbe2a')
    ck('freeze_pin', fh == '2243d06baef0a5f636739cdab980055f104ed98365e6a2e5749238e825cbe1e8')
    ck('freeze_copy', result['freeze'] == freeze)
    for name, h in freeze['files'].items():
        ck('file/'+name, sha(J/name) == h)
    ck('tests_pin', tests['freeze_sha256'] == fh and sha(J/(STEM+'_TESTS.json')) == result['synthetic_tests_sha256'])
    for i, c in enumerate(tests['controls']):
        ck('synthetic/'+str(i), c['passed'] and math.isfinite(c['error']) and c['error'] <= c['gate'])
    summaries, flags, paired, excluded, masses, references, controls = {}, {}, {}, [], {}, {}, 0
    for i in range(100):
        file = f'galaxy_{i:03d}.json'
        path, opath = J/(STEM+'_CASES')/file, J/(OLD+'_CASES')/file
        case, old = json.loads(path.read_text()), json.loads(opath.read_text())
        name, rows, n = old['name'], old['rows'], old['n_inner']
        ck(name+'/custody', sha(path) == result['case_sha256'][file] and sha(opath) == freeze['inherited_case_sha256'][file] == previous['case_sha256'][file] == case['inherited_case_sha256'])
        ck(name+'/identity', case['index'] == i and case['name'] == name and case['rows'] == rows and case['rows_sha256'] == digest(rows) == old['rows_sha256'] and case['freeze_sha256'] == fh and case['n'] == len(rows) and case['n_inner'] == n)
        census = {'index': i, 'name': name, 'n': len(rows), 'eligible': len(rows) >= 6, 'n_inner': n,
            'inner_indices': old.get('inner_indices'), 'outer_indices': old.get('outer_indices'),
            'rows_sha256': old['rows_sha256'], 'inherited_case_sha256': sha(opath)}
        ck(name+'/census', freeze['census'][i] == census)
        ck(name+'/outcome', result['outcomes'][i] == {'index': i, 'name': name, 'status': case['status']})
        if len(rows) < 6:
            ck(name+'/excluded', case['status'] == 'EXCLUDED_LT6')
            excluded.append({'name': name, 'reason': case['reason']})
            continue
        ck(name+'/qualified', case['status'] == 'QUALIFIED' and old['status'] == 'QUALIFIED')
        ck(name+'/masks', case['inner_indices'] == old['inner_indices'] == list(range(n)) and case['outer_indices'] == old['outer_indices'] == list(range(n, len(rows))))
        for c in case['controls']:
            controls += 1
            ck(name+'/control/'+c['name'], c['passed'] and math.isfinite(c['error']) and c['error'] <= c['gate'])
        rr = [r['R_kpc'] for r in rows]
        b2 = [r['gbar_si']*r['R_kpc']/CONV for r in rows]
        vv = [r['vobs_kms'] for r in rows]
        ck(name+'/inner_hash', digest({'radius': rr[:n], 'b2': b2[:n], 'observed': vv[:n]}) == case['inner_input_sha256'])
        expected_refs = dict(old['fixed'])
        for model, fits in old['halo_fits'].items():
            expected_refs.update({f'{model}_{f["grid_count"]}': f['readout'] for f in fits})
        ck(name+'/unchanged_references', case['references'] == expected_refs)
        for label, ref in case['references'].items():
            got = readout(ref['prediction_kms'], rows, n)
            for metric in ('velocity_mse', 'logg_mse'):
                numerical(name+'/ref/'+label+'/'+metric, 'reference_metrics', got['outer'][metric], ref['outer'][metric], 2e-12)
            references.setdefault(label, []).append(got['outer'])
        for scenario, delta in SCENARIOS.items():
            for count, fit in zip((257, 513), case['cm_fits'][scenario]):
                key = f'{scenario}_{count}'
                selected = fit['selected']
                logmass = selected['log10_mass_msun']
                ck(name+'/'+key+'/scenario', fit['delta_c'] == delta and fit['grid_count'] == count)
                if logmass is None:
                    ck(name+'/'+key+'/zero', selected['zero_halo'] and selected['mass_dmo_msun'] == 0 and selected['concentration'] is None and selected['r200_dmo_kpc'] is None)
                    mass, c, r200 = 0., None, None
                else:
                    mass, c, r200 = params(logmass, delta)
                    for field, val in (('mass_dmo_msun', mass), ('concentration', c), ('r200_dmo_kpc', r200), ('rs_kpc', r200/c)):
                        numerical(name+'/'+key+'/'+field, 'parameters', val, selected[field], 2e-12)
                    ck(name+'/'+key+'/low_mass', selected['concentration_extrapolated_low'] == (mass < 1e10/LITTLE_H))
                pred = prediction(logmass, delta, rr, b2)
                got = readout(pred, rows, n)
                for field in ('prediction_kms', 'residual_kms', 'residual_dex', 'quoted_error_residual', 'gpred_si'):
                    numerical(name+'/'+key+'/'+field, field, got[field], fit['readout'][field])
                for side in ('inner', 'outer'):
                    for metric in ('velocity_mse', 'logg_mse'):
                        numerical(name+'/'+key+'/'+side+'/'+metric, 'metrics', got[side][metric], fit['readout'][side][metric])
                numerical(name+'/'+key+'/inner_sse', 'selected_objective', n*got['inner']['velocity_mse'], selected['inner_sse'])
                # Recompute values at SAVED grid masses and candidates; never optimize.
                gridloss = []
                ck(name+'/'+key+'/grid_abscissae', len(fit['grid']['log10_mass_msun']) == count and all(error(t, 8+7*j/(count-1)) < 1e-14 for j, t in enumerate(fit['grid']['log10_mass_msun'])))
                for t in fit['grid']['log10_mass_msun']:
                    pp = prediction(t, delta, rr[:n], b2[:n])
                    gridloss.append(math.fsum((a-b)**2 for a, b in zip(pp, vv[:n])))
                numerical(name+'/'+key+'/grid_losses', 'all_saved_grid_losses', gridloss, fit['grid']['inner_sse'])
                for j, candidate in enumerate(fit['candidates']):
                    pp = prediction(candidate['log10_mass_msun'], delta, rr[:n], b2[:n])
                    loss = math.fsum((a-b)**2 for a, b in zip(pp, vv[:n]))
                    numerical(name+'/'+key+'/candidate/'+str(j), 'all_saved_candidate_losses', loss, candidate['inner_sse'])
                ck(name+'/'+key+'/selected_saved_minimum', selected['inner_sse'] == min(q['inner_sse'] for q in fit['candidates']))
                beyond = None if r200 is None else [j for j, r in enumerate(rr) if r > r200]
                outer_beyond = None if beyond is None else [j for j in beyond if j >= n]
                ck(name+'/'+key+'/domain', fit['rows_beyond_r200_dmo'] == beyond and fit['outer_rows_beyond_r200_dmo'] == outer_beyond and selected['finite_mass_boundary'] == (logmass in (8., 15.)))
                total = case['catalogue_total_baryon_mass_msun']
                budget = None if total is None else total > FB*mass
                ck(name+'/'+key+'/budget', fit['nominal_baryon_budget_exceeded'] is budget)
                flag = flags.setdefault(key, dict(galaxies=0, zero_halo=0, finite_mass_boundary=0, below_calibrated_mass=0, any_outer_beyond_r200=0, baryon_budget_assessed=0, baryon_budget_exceeded=0))
                flag['galaxies'] += 1
                flag['zero_halo'] += mass == 0
                flag['finite_mass_boundary'] += logmass in (8., 15.)
                flag['below_calibrated_mass'] += 0 < mass < 1e10/LITTLE_H
                flag['any_outer_beyond_r200'] += bool(outer_beyond)
                flag['baryon_budget_assessed'] += budget is not None
                flag['baryon_budget_exceeded'] += budget is True
                summaries.setdefault(key, []).append(got['outer'])
                masses.setdefault(key, []).append({'name': name, 'mass': mass, 'c': c, 'r200': r200, 'kind': selected['kind'], 'below_calibration': 0 < mass < 1e10/LITTLE_H, 'outer_beyond': outer_beyond, 'budget': budget})
                for label, ref in case['references'].items():
                    for metric in ('velocity_mse', 'logg_mse'):
                        numerical(name+'/'+key+'/pair/'+label+'/'+metric, 'saved_pairs', got['outer'][metric]-ref['outer'][metric], case['paired_outer_differences'][key][label][metric])
                network, cm = case['references']['inherited_calibrated']['outer']['velocity_mse'], got['outer']['velocity_mse']
                diff = network-cm
                tol = 1e-10*max(1., network, cm)
                paired.setdefault(key, []).append({'name': name, 'network': network, 'cm': cm, 'difference': diff,
                    'outcome': 'tie' if abs(diff) <= tol else ('win' if diff < 0 else 'loss'),
                    'kind': selected['kind'], 'mass': mass, 'below_calibration': 0 < mass < 1e10/LITTLE_H})
        ck(name+'/aggregate_pair_copy', result['paired_per_galaxy'][len(references['inherited_calibrated'])-1] == {'name': name, 'differences': case['paired_outer_differences']})
    aggregate = {k: {m: mean([r[m] for r in rows]) for m in ('velocity_mse', 'logg_mse')} for k, rows in summaries.items()}
    for key, val in aggregate.items():
        for metric, v in val.items():
            numerical('aggregate/'+key+'/'+metric, 'aggregate', v, result['outer_galaxy_balanced_MSE'][key][metric])
    ck('flags', flags == result['boundary_and_domain_frequencies'])
    ck('census_qualification', result['census'] == 100 and result['eligible'] == 94 and result['status'] == 'QUALIFIED_COMPLETE_CENSUS' and not result['numerical_failures'])
    ck('exclusions', len(excluded) == 6 and result['excluded'] == previous['excluded'] == excluded)
    ck('reference_aggregate_copy', result['inherited_reference_outer_galaxy_balanced_MSE'] == previous['outer_galaxy_balanced_MSE'])
    robust = {key: pair_summary(rows) for key, rows in paired.items()}
    output = {'status': 'SAVED_CM_AUDIT_PASSED' if all(c['passed'] for c in checks) else 'SAVED_CM_AUDIT_FAILED',
        'scope': 'Independent analytic NFW values at saved parameters/grid masses, no fitting or producer/helper import. Paired robustness is posthoc descriptive.',
        'pins': {'audit_source': sha(Path(__file__)), 'source': sha(J/'galaxy_radial_cm_transfer_v001.py'), 'result': sha(J/(STEM+'_RESULT.json')), 'freeze': fh, 'tests': sha(J/(STEM+'_TESTS.json'))},
        'checks': {'total': len(checks), 'passed': sum(c['passed'] for c in checks), 'failed': [c for c in checks if not c['passed']]},
        'maximum_scaled_errors': maxima, 'saved_controls': {'synthetic': len(tests['controls']), 'galaxy': controls},
        'census': 100, 'eligible': 94, 'excluded': excluded, 'aggregate': aggregate, 'flags': flags,
        'posthoc_paired_network_minus_CM': robust, 'domain_details': masses,
        'tie_rule': 'abs(network-CM)<=1e-10*max(1,network,CM)', 'seconds': time.perf_counter()-started}
    target = J/(STEM+'_AUDIT.json')
    with tempfile.NamedTemporaryFile(dir=J, prefix=target.name+'.partial.', delete=False) as f:
        temporary = Path(f.name)
        f.write((json.dumps(output, indent=2, allow_nan=False)+'\n').encode())
        f.flush()
        os.fsync(f.fileno())
    try:
        os.link(temporary, target)
    finally:
        temporary.unlink()
    compact = {key: {k: r[k] for k in ('all', 'wins', 'ties', 'losses', 'leave_out')} for key, r in robust.items() if key.endswith('_513')}
    print(json.dumps({'status': output['status'], 'checks': output['checks'], 'maxima': maxima, 'controls': output['saved_controls'], 'aggregate': aggregate, 'flags': flags, 'robustness': compact, 'seconds': output['seconds'], 'sha256': sha(target)}))


if __name__ == '__main__':
    main()
