"""Independent saved-array audit. No producer import, inverse, fit or evolution."""
import os
for key in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS',
            'VECLIB_MAXIMUM_THREADS'):
    os.environ[key] = '1'
import hashlib
import json
import math
from pathlib import Path
import resource
import tempfile
import time
import numpy as np

ROOT = Path(__file__).resolve().parent
STEM = 'LINEAR_SOURCE_GALAXY_REFERENCE_V001'
PINS = {
    STEM + '_RESULT.json': '6bef7739471ce1ae5ed0714c3572693162fc2d3ac0780345ba43894ccef947fb',
    'linear_source_galaxy_reference_v001.py': '82dab5cc4970802524bf5e2fa511ecc0ba325d3a8923175733b80c34cfd3a4df',
    STEM + '.md': '399fa90b083afe9a014bc47e2e3d70c80f1c8ef5708edb205cb348b8d6f72801',
    'GALAXY_RADIAL_TRANSFER_V001_RESULT.json': '77883bc7e0da4ceaf1d623ba835be6dc3c0666dd0b56d0b00aa36e551247f7c0',
}
A0 = 1.0059833281731022e-10
PC = 149597870700.0 * 648000.0 / math.pi
CONV = 1e6 / (1000 * PC)
checks = []


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(name, condition):
    checks.append(dict(name=name, passed=bool(condition)))


def close(name, actual, expected, tolerance=1e-11, relative=False):
    a, b = np.asarray(actual, dtype=float), np.asarray(expected, dtype=float)
    if a.shape != b.shape:
        checks.append(dict(name=name, passed=False, reason='shape'))
        return
    denominator = np.maximum(abs(b), 1e-300) if relative else np.maximum(abs(b), 1.)
    err = float(np.max(abs(a-b)/denominator, initial=0.))
    checks.append(dict(name=name, error=err, tolerance=tolerance,
                       passed=bool(np.isfinite(err) and err <= tolerance)))


def positive_flux(x, order):
    """Independent cubic Newton root and positive angle integral; no B subtraction."""
    x = np.asarray(x)
    h = (8/(3*math.pi))*x
    t = np.minimum(h, np.cbrt(h))  # Both are upper bounds on the positive root.
    for _ in range(24):
        t -= (t*(1+t*t)-h)/(1+3*t*t)
    angle = np.arctan(1/t)
    nodes, weights = np.polynomial.legendre.leggauss(order)
    u = angle[:, None]*(nodes+1)/2
    sin2 = np.sin(u)**2
    integral = (angle/2)*np.sum(weights*2*sin2*(3-2*sin2), axis=1)
    return h*h*integral/(2*(8/(3*math.pi))), t*(1+t*t)/h-1


def readout(pred, obs, errors, outer):
    dv = pred-obs
    lg = 2*np.log10(pred/obs)
    metrics = dict(velocity_mse=math.fsum(float(v*v) for v in dv[outer])/len(outer),
                   logg_mse=math.fsum(float(v*v) for v in lg[outer])/len(outer))
    arrays = dict(prediction_kms=pred, residual_kms=dv, residual_dex=lg,
                  quoted_error_residual=dv/errors)
    return metrics, arrays


def main():
    started = time.perf_counter()
    target = ROOT/(STEM+'_AUDIT.json')
    if target.exists() or target.is_symlink():
        raise FileExistsError(target)
    custody = {name: sha(ROOT/name) for name in PINS}
    for name, value in PINS.items():
        check('pin:'+name, custody[name] == value)
    if not all(c['passed'] for c in checks):
        raise ValueError('Custody failed before arithmetic')
    data = json.loads((ROOT/(STEM+'_RESULT.json')).read_text())
    prior = json.loads((ROOT/'GALAXY_RADIAL_TRANSFER_V001_RESULT.json').read_text())
    for name, value in data['custody'].items():
        check('result_custody:'+name, sha(ROOT/name) == value)
    controls = data['controls']
    check('producer_control_count', len(controls) == 1228)
    check('producer_control_names_unique', len({c['name'] for c in controls}) == 1228)
    for c in controls:
        check('producer_control:'+c['name'], c['passed'] is True and
              math.isfinite(c['error']) and 0 <= c['error'] <= c['limit'])
    check('qualified_status', data['status'] == 'QUALIFIED_LOCAL_REFERENCE_ONLY'
          and data['all_controls_pass'] is True)
    check('unchanged_a0', data['inputs']['a0_si'] == A0 ==
          prior['freeze']['a0_si']['inherited_calibrated'])
    check('no_new_fits', data['inputs']['per_galaxy_fits'] == 0 == data['inputs']['new_global_fits'])
    new = {c['name']: c for c in data['cases']}
    check('new_unique_census', len(new) == len(data['cases']) == 94)
    check('prior_census', prior['status'] == 'QUALIFIED_COMPLETE_CENSUS' and
          prior['census'] == 100 and prior['eligible'] == 94 and len(prior['case_sha256']) == 100)
    excluded = []
    summaries = []
    all_new_x, all_d = [], []
    outer_count = row_count = 0
    for filename, expected_sha in sorted(prior['case_sha256'].items()):
        path = ROOT/'GALAXY_RADIAL_TRANSFER_V001_CASES'/filename
        check('case_pin:'+filename, sha(path) == expected_sha)
        case = json.loads(path.read_text())
        name = case['name']
        if case['n'] < 6:
            excluded.append(dict(name=name, reason=case['reason'], n=case['n'], case_sha256=expected_sha))
            check(name+':absent', name not in new)
            continue
        check(name+':qualified', case['status'] == 'QUALIFIED' and all(c['passed'] for c in case['controls']))
        saved = new[name]
        rows, n = case['rows'], case['n']
        check(name+':hash', saved['case_sha256'] == expected_sha)
        check(name+':masks', case['n_inner'] == n//2 and case['inner_indices'] == list(range(n//2))
              and case['outer_indices'] == saved['outer_indices'] == list(range(n//2, n)))
        check(name+':source_lines', saved['source_lines'] == [r['source_line'] for r in rows])
        radius, obs, error, gb, go = (np.array([r[k] for r in rows]) for k in
                                    ('R_kpc','vobs_kms','evobs_kms','gbar_si','gobs_si'))
        check(name+':positive_saved_rows', len(rows) == n and all(np.all(np.isfinite(a) & (a>0))
              for a in (radius, obs, error, gb, go)) and np.all(np.diff(radius) >= 0))
        close(name+':radius', saved['R_kpc'], radius, 0)
        close(name+':gbar', saved['gbar_si'], gb, 0, True)
        close(name+':gobs_units', CONV*obs**2/radius, go, 1e-12, True)
        gp = np.array(saved['gpred_si'])
        all_new_x.extend(gp/A0)
        all_d.extend(gb/A0)
        pred = np.sqrt(gp*radius/CONV)
        outer = np.array(saved['outer_indices'])
        metrics, arrays = readout(pred, obs, error, outer)
        for label, values in arrays.items():
            close(name+':new:'+label, values, saved['new_local_reference'][label])
        for metric, value in metrics.items():
            close(name+':new:'+metric, value, saved['new_local_reference']['outer'][metric])
        references = dict(case['fixed'])
        for halo in ('NFW','ISO'):
            for fit in case['halo_fits'][halo]:
                references[halo+'_'+str(fit['grid_count'])] = fit['readout']
        scores = {}
        for label, read in references.items():
            score, arrays = readout(np.array(read['prediction_kms']), obs, error, outer)
            scores[label] = score
            for key, values in arrays.items():
                close(name+':reference:'+label+':'+key, values, read[key])
            for metric, value in score.items():
                close(name+':reference:'+label+':'+metric, value, read['outer'][metric])
                if label in saved['paired_outer_differences']:
                    close(name+':paired:'+label+':'+metric, metrics[metric]-value,
                          saved['paired_outer_differences'][label][metric])
        summaries.append(dict(name=name, new=metrics, references=scores))
        row_count += n
        outer_count += len(outer)
    check('exact_exclusions', excluded == data['excluded'] and len(excluded) == 6)
    check('prior_exclusions', [{k: e[k] for k in ('name','reason')} for e in excluded] == prior['excluded'])
    close('outer_rows', outer_count, 981, 0)
    x, d = np.array(all_new_x), np.array(all_d)
    f64, cubic64 = positive_flux(x, 64)
    f96, cubic96 = positive_flux(x, 96)
    close('independent_cubic_root', cubic96, np.zeros_like(x), 2e-14)
    close('independent_positive_flux_inverse', f96, d, 1e-11, True)
    close('independent_quadrature_refinement', f64, f96, 1e-11, True)
    aggregate = {m: math.fsum(c['new'][m] for c in summaries)/94 for m in ('velocity_mse','logg_mse')}
    for m, value in aggregate.items():
        close('aggregate:new:'+m, value, data['new_galaxy_balanced_outer_MSE'][m])
    for label in summaries[0]['references']:
        for m in aggregate:
            value = math.fsum(c['references'][label][m] for c in summaries)/94
            close('aggregate:'+label+':'+m, value, data['saved_reference_outer_MSE'][label][m])
            close('prior_aggregate:'+label+':'+m, value, prior['outer_galaxy_balanced_MSE'][label][m])
    beta = 32/(9*math.pi**2)
    mcrit = A0*(100*PC)**2/(beta*1.32712440018e20)
    close('beta', beta, data['separate_spherical_asymptotic']['beta'], 1e-14, True)
    close('Mcrit', mcrit, data['separate_spherical_asymptotic']['Mcrit_Msun'], 1e-14, True)
    check('asymptotic_not_scored', data['separate_spherical_asymptotic']['scored_against_disk_rows'] is False)
    out = dict(status='PASS' if all(c['passed'] for c in checks) else 'FAIL',
               custody=custody, audit_source_sha256=sha(Path(__file__)),
               producer_controls=dict(total=len(controls), passed=sum(c['passed'] for c in controls)),
               audit_controls=dict(total=len(checks), passed=sum(c['passed'] for c in checks)),
               controls=checks, galaxies=94, excluded=excluded, full_rows=row_count, outer_rows=outer_count,
               new_galaxy_balanced_outer_MSE=aggregate, beta=beta, Mcrit_Msun=mcrit,
               paired_mean_velocity_difference={label: math.fsum(c['new']['velocity_mse']-
                   c['references'][label]['velocity_mse'] for c in summaries)/94
                   for label in summaries[0]['references']},
               per_galaxy=summaries,
               scope='Saved local algebraic reference only. No inverse/producer/fit rerun; no finite-ell disk or asymptotic/existence qualification.',
               elapsed_seconds=time.perf_counter()-started,
               peak_rss_native=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    fd, temporary = tempfile.mkstemp(prefix=target.name+'.', suffix='.tmp', dir=ROOT)
    try:
        with os.fdopen(fd, 'w') as stream:
            json.dump(out, stream, indent=2, allow_nan=False)
            stream.write('\n')
            stream.flush()
            os.fsync(stream.fileno())
        os.link(temporary, target)
    finally:
        os.unlink(temporary)
    print(json.dumps({k: out[k] for k in ('status','producer_controls','audit_controls','galaxies',
                                         'full_rows','outer_rows','elapsed_seconds')}))
    print(json.dumps(dict(result_sha256=sha(target), aggregate=aggregate,
                          paired_mean_velocity_difference=out['paired_mean_velocity_difference'])))
    return 0 if out['status'] == 'PASS' else 2


if __name__ == '__main__':
    raise SystemExit(main())
