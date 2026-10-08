"""Saved-input inner-to-outer galaxy test. No execution until root freezes/releases."""
import os
import sys
sys.dont_write_bytecode = True
for key in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS',
            'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[key] = '1'
import hashlib
import json
import math
from pathlib import Path
import resource
import tempfile
import time
import numpy as np
import halo_profile_fitter_v001 as old

ROOT = Path(__file__).resolve().parent
STEM = 'GALAXY_RADIAL_TRANSFER_V001'
SOURCE = ROOT/'SPARC_EFFECTIVE_TRANSFER_V001_RESULT.json'
OLD_FREEZE = ROOT/'SPARC_EFFECTIVE_TRANSFER_V001_FROZEN.json'
HELPER = ROOT/'halo_profile_fitter_v001.py'
EXPECTED = {SOURCE: 'f8502c04a3f17655172b2f589b48d1eebaa7c46bb64ad9950fd10d34ceb23aa9',
    OLD_FREEZE: 'a3cf6c736a647877eb6a2daba06b5f481e00b5c63f8b23b3d831b8d31bada549',
    HELPER: 'e8bc0d90c68fd81a5a78525870c19f4d97b3e1bf8bebb1820fa40b4098201df1'}
CONV = 1e6/3.085677581491367e19
FIXED = ('baryons', 'inherited_calibrated', 'rar_calibrated')
HALOS = ('NFW', 'ISO')
GRIDS = (257, 513)
DEADLINE = math.inf


def encoded(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def digest(obj):
    return hashlib.sha256(encoded(obj)).hexdigest()


def publish(path, obj):
    data = encoded(obj)+b'\n'
    with tempfile.NamedTemporaryFile(dir=path.parent, prefix=path.name+'.partial.', delete=False) as f:
        temporary = Path(f.name)
        f.write(data)
        f.flush()
        os.fsync(f.fileno())
    try:
        os.link(temporary, path)
    finally:
        temporary.unlink()


def budget():
    if time.perf_counter() >= DEADLINE:
        raise TimeoutError('55-second invocation budget; resume missing galaxy')


def check(items, name, value, gate):
    items.append(dict(name=name, error=float(value), gate=gate,
                      passed=bool(math.isfinite(value) and value <= gate)))


def relative(a, b, floor=1.):
    a, b = np.asarray(a), np.asarray(b)
    return float(np.max(abs(a-b))/max(floor, float(np.max(abs(b)))))


def inputs():
    if any(sha(p) != h for p, h in EXPECTED.items()):
        raise RuntimeError('Changed pinned source/helper')
    saved = json.loads(SOURCE.read_text())
    original = json.loads(OLD_FREEZE.read_text())
    assert saved['status'] == 'COMPLETE_DESCRIPTIVE_EFFECTIVE_TRANSFER'
    assert saved['frozen_sha256'] == sha(OLD_FREEZE)
    assert all(c['passed'] for c in saved['controls'])
    grouped = {}
    for row in saved['central']['predictions']:
        if row['role'] == 'evaluation':
            grouped.setdefault(row['name'], []).append(row)
    groups = [(name, sorted(rows, key=lambda r: (r['R_kpc'], r['source_line'])))
              for name, rows in sorted(grouped.items())]
    assert len(groups) == 100
    calibration = sorted(g['name'] for g in saved['central']['galaxies'] if g['role'] == 'calibration')
    assert len(calibration) == 51
    census = [dict(index=i, name=name, n=len(rows), n_inner=len(rows)//2,
                   eligible=len(rows) >= 6, rows_sha256=digest(rows))
              for i, (name, rows) in enumerate(groups)]
    files = {p.name: sha(p) for p in (Path(__file__), ROOT/(STEM+'.md'), *EXPECTED)}
    return saved, original, groups, dict(files=files, census=census,
        previous_calibration_galaxies=calibration, a0_si=saved['a0_si'], inherited_r=original['r'],
        inherited_excluded_rows=original['excluded_rows'], inherited_central_invalid=saved['central']['invalid'])


def grid_shapes(model, r, logscale, pivot):
    logx = np.log(r/pivot)[None, :]-np.asarray(logscale)[:, None]
    logf = old._log_kernel_and_slope(model, logx)[0]
    logpivot = old._log_kernel_and_slope(model, -np.asarray(logscale))[0]
    return np.exp(logf-logpivot[:, None])


def amplitudes(shapes, b, v):
    shapes = np.atleast_2d(shapes)
    if not np.all(np.isfinite(shapes)) or np.any(shapes <= 0):
        raise ValueError('Invalid halo shape')
    zero_gradient = np.sum(shapes*(1-v/np.sqrt(b)), axis=1)
    lower = np.zeros(len(shapes))
    upper = np.max(v*v/shapes, axis=1)
    boundary = zero_gradient >= 0
    upper[boundary] = 0.
    for _ in range(96):
        budget()
        mid = (lower+upper)/2
        gradient = np.sum(shapes*(1-v/np.sqrt(b+mid[:, None]*shapes)), axis=1)
        lower = np.where((gradient < 0) & ~boundary, mid, lower)
        upper = np.where(gradient >= 0, mid, upper)
    amp = (lower+upper)/2
    loss = np.sum((np.sqrt(b+amp[:, None]*shapes)-v)**2, axis=1)
    return amp, loss


def profile(model, r, b, v, count):
    """Only inner arrays accepted. No outer kinematics/pivot can enter."""
    budget()
    pivot = float(np.median(r))
    grid = np.linspace(-20., 20., count)
    shapes = grid_shapes(model, r, grid, pivot)
    amps, losses = amplitudes(shapes, b, v)
    candidates, controls = [], []

    def scalar(t):
        budget()
        result = old.optimize_amplitude(old.shape(model, r, t, pivot), b, v, np.ones(len(r)))
        return result['amplitude'], result['sse']

    def keep(t, kind, **extra):
        amp, loss = scalar(t)
        candidates.append(dict(kind=kind, logscale=float(t) if math.isfinite(t) else None,
            scale_kpc=pivot*math.exp(t) if math.isfinite(t) else None,
            amplitude=amp, inner_sse=loss, amplitude_boundary=amp == 0., **extra))

    for index in (0, count//2, count-1):
        a, j = scalar(grid[index])
        check(controls, f'vector_scalar_A_{index}', relative(amps[index], a), 1e-10)
        check(controls, f'vector_scalar_J_{index}', relative(losses[index], j), 1e-10)
        check(controls, f'vector_shape_{index}', relative(shapes[index], old.shape(model, r, grid[index], pivot)), 1e-12)
    keep(-20., 'finite_lower_boundary')
    keep(20., 'finite_upper_boundary')
    keep(-math.inf, 'zero_scale_limit')
    keep(math.inf, 'infinite_scale_limit')
    zero_plateau = bool(np.all(amps == 0) and all(c['amplitude'] == 0 for c in candidates))
    if zero_plateau:
        candidates = [dict(kind='zero_amplitude_scale_unidentified', logscale=None,
                           scale_kpc=None, amplitude=0., inner_sse=float(np.sum((np.sqrt(b)-v)**2)),
                           amplitude_boundary=True)]
    else:
        keep(float(grid[int(np.argmin(losses))]), 'lowest_sampled_grid')
        ratio = (math.sqrt(5)-1)/2
        indices = np.flatnonzero((losses[1:-1] < losses[:-2]) & (losses[1:-1] < losses[2:]))+1
        if len(indices):
            left, right = grid[indices-1].copy(), grid[indices+1].copy()
            brackets = np.column_stack((left, right))
            c, d = right-ratio*(right-left), left+ratio*(right-left)
            objective = lambda t: amplitudes(grid_shapes(model, r, t, pivot), b, v)[1]
            fc, fd = objective(c), objective(d)
            for _ in range(80):
                choose_left = fc <= fd
                next_left, next_right = np.where(choose_left, left, c), np.where(choose_left, d, right)
                next_c = np.where(choose_left, next_right-ratio*(next_right-next_left), d)
                next_d = np.where(choose_left, c, next_left+ratio*(next_right-next_left))
                new_loss = objective(np.where(choose_left, next_c, next_d))
                fc, fd = np.where(choose_left, new_loss, fd), np.where(choose_left, fc, new_loss)
                left, right, c, d = next_left, next_right, next_c, next_d
            for j, i in enumerate(indices):
                choices = (float(grid[i]), float(left[j]), float(right[j]), float(c[j]), float(d[j]), float((left[j]+right[j])/2))
                trial = min(choices, key=lambda t: scalar(t)[1])
                keep(trial, 'strict_sampled_local_minimum', grid_index=int(i), initial_bracket=brackets[j].tolist(),
                     final_bracket=[float(left[j]), float(right[j])], golden_iterations=80)
    selected = dict(min(candidates, key=lambda c: c['inner_sse']))
    selected['scale_unidentified_at_zero_amplitude'] = selected['amplitude'] == 0.
    return dict(model=model, grid_count=count, pivot_kpc=pivot, selected=selected,
        candidates=candidates, grid=dict(logscale=grid.tolist(), amplitude=amps.tolist(), inner_sse=losses.tolist()),
        zero_amplitude_plateau=zero_plateau, controls=controls)


def predict(fitted, r, b):
    selected = fitted['selected']
    if selected['amplitude'] == 0:
        return np.sqrt(b)
    t = selected['logscale']
    if t is None:
        t = -math.inf if selected['kind'] == 'zero_scale_limit' else math.inf
    return np.sqrt(b+selected['amplitude']*old.shape(fitted['model'], r, t, fitted['pivot_kpc']))


def fit_split(model, r, b, v, count):
    n = len(r)//2
    return profile(model, r[:n], b[:n], v[:n], count)


def synthetic_tests():
    checks = []
    nodes, weights = np.polynomial.legendre.leggauss(128)
    z, weights = (nodes+1)/2, weights/2
    for model in HALOS:
        for x in (1e-6, .05, .125, 1., 10.):
            actual, slope = old._log_kernel_and_slope(model, np.array([math.log(x)]))
            y = x*z
            positive_integral = float(weights@(y/(1+y)**2 if model == 'NFW' else y*y/(1+y*y)))
            check(checks, f'{model}_mass_{x}', abs(math.exp(actual[0])/positive_integral-1), 2e-11)
            step = 1e-5
            plus = old._log_kernel_and_slope(model, np.array([math.log(x)+step]))[0][0]
            minus = old._log_kernel_and_slope(model, np.array([math.log(x)-step]))[0][0]
            check(checks, f'{model}_slope_{x}', abs((plus-minus)/(2*step)-slope[0]), 2e-8)
        r = np.geomspace(.1, 30., 24)
        b, n = 200+15*r, len(r)//2
        pivot, amplitude, t = float(np.median(r[:n])), 2500., .4
        v = np.sqrt(b+amplitude*old.shape(model, r, t, pivot))
        for sign in (-math.inf, math.inf):
            exponent = (-1 if sign < 0 else 1) if model == 'NFW' else (0 if sign < 0 else 2)
            check(checks, f'{model}_limit_{sign}', relative(old.shape(model, r, sign, pivot), (r/pivot)**exponent), 1e-12)
        check(checks, model+'_pivot', abs(old.shape(model, pivot, t, pivot)-1), 1e-12)
        a, _ = amplitudes(old.shape(model, r[:n], t, pivot), b[:n], v[:n])
        check(checks, model+'_amplitude_recovery', abs(a[0]/amplitude-1), 1e-11)
        fitted = fit_split(model, r, b, v, 257)
        check(checks, model+'_synthetic_sse', fitted['selected']['inner_sse'], 1e-8)
        check(checks, model+'_synthetic_amplitude', abs(fitted['selected']['amplitude']/amplitude-1), 1e-4)
        check(checks, model+'_synthetic_scale', abs(fitted['selected']['logscale']-t), 1e-4)
        changed = v.copy()
        changed[n:] *= 100+np.arange(len(v)-n)
        mutated = fit_split(model, r, b, changed, 257)
        check(checks, model+'_outer_velocity_leakage', 0. if digest(fitted) == digest(mutated) else 1., 0.)
        zero = fit_split(model, r, b, .9*np.sqrt(b), 257)
        check(checks, model+'_zero_plateau', 0. if zero['zero_amplitude_plateau'] and len(zero['candidates']) == 1 else 1., 0.)
        checks.extend(fitted['controls']+mutated['controls']+zero['controls'])
    return checks


def metrics(pred, r, observed, errors, n):
    residual = pred-observed
    logs = 2*np.log10(pred/observed)
    return dict(prediction_kms=pred.tolist(), residual_kms=residual.tolist(),
        residual_dex=logs.tolist(), quoted_error_residual=(residual/errors).tolist(),
        gpred_si=(CONV*pred*pred/r).tolist(),
        inner=dict(velocity_mse=float(np.mean(residual[:n]**2)), logg_mse=float(np.mean(logs[:n]**2))),
        outer=dict(velocity_mse=float(np.mean(residual[n:]**2)), logg_mse=float(np.mean(logs[n:]**2))))


def one_galaxy(index, name, rows, freeze_hash, out):
    start = time.perf_counter()
    out.update(index=index, name=name, rows=rows, rows_sha256=digest(rows), freeze_sha256=freeze_hash,
               n=len(rows), n_inner=len(rows)//2, controls=[], halo_fits={}, fixed={})
    if len(rows) < 6:
        return out | dict(status='EXCLUDED_LT6', reason='Fewer than six saved valid rows', seconds=time.perf_counter()-start)
    r, v, ev, gb, go = (np.asarray([row[key] for row in rows]) for key in
                       ('R_kpc', 'vobs_kms', 'evobs_kms', 'gbar_si', 'gobs_si'))
    if any(np.any(~np.isfinite(a)) or np.any(a <= 0) for a in (r, v, ev, gb, go)):
        raise ValueError('Saved positive finite row premise failed; no clipping')
    b, n = gb*r/CONV, len(r)//2
    out.update(inner_indices=list(range(n)), outer_indices=list(range(n, len(r))),
               split_radius_tied=bool(r[n-1] == r[n]), pivot_inner_kpc=float(np.median(r[:n])))
    check(out['controls'], 'gobs_saved_identity', float(np.max(abs(CONV*v*v/r/go-1))), 1e-12)
    changed = v.copy()
    changed[n:] *= 100+np.arange(len(v)-n)
    fitting_input = lambda vv: dict(r=r[:n].tolist(), b2=b[:n].tolist(), v=vv[:n].tolist())
    out['inner_input_sha256'] = digest(fitting_input(v))
    check(out['controls'], 'outer_mutation_inner_input_identity',
          0. if digest(fitting_input(changed)) == out['inner_input_sha256'] else 1., 0.)
    for model in FIXED:
        gp = np.asarray([row['gpred_si'][model] for row in rows])
        out['fixed'][model] = metrics(np.sqrt(gp*r/CONV), r, v, ev, n)
        saved_log = np.asarray([row['residual_dex'][model] for row in rows])
        check(out['controls'], model+'_saved_residual', relative(out['fixed'][model]['residual_dex'], saved_log), 1e-12)
    for model in HALOS:
        fits = [fit_split(model, r, b, v, count) for count in GRIDS]
        predictions = [predict(fitted, r, b) for fitted in fits]
        for fitted, pred in zip(fits, predictions):
            out['controls'].extend(fitted['controls'])
            reconstructed = float(np.sum((pred[:n]-v[:n])**2))
            check(out['controls'], f'{model}_{fitted["grid_count"]}_objective',
                  relative(reconstructed, fitted['selected']['inner_sse']), 1e-10)
            fitted['readout'] = metrics(pred, r, v, ev, n)
        check(out['controls'], model+'_grid_objective',
              relative(fits[0]['selected']['inner_sse'], fits[1]['selected']['inner_sse']), 1e-6)
        check(out['controls'], model+'_outer_prediction_refinement', relative(predictions[0][n:], predictions[1][n:]), 1e-5)
        out['halo_fits'][model] = fits
    out['paired_outer_differences'] = {}
    network = out['fixed']['inherited_calibrated']['outer']
    for label, item in out['fixed'].items():
        if label != 'inherited_calibrated':
            out['paired_outer_differences']['network_minus_'+label] = {k: network[k]-item['outer'][k] for k in network}
    for label, fits in out['halo_fits'].items():
        for fitted in fits:
            out['paired_outer_differences'][f'network_minus_{label}_{fitted["grid_count"]}'] = {
                k: network[k]-fitted['readout']['outer'][k] for k in network}
    return out | dict(status='QUALIFIED' if all(c['passed'] for c in out['controls']) else 'UNRESOLVED_CONTROLS',
                      seconds=time.perf_counter()-start)


def aggregate(receipts, freeze, case_hashes):
    eligible = [r for r in receipts if r['n'] >= 6]
    summaries, boundaries = {}, {}
    for label in FIXED:
        items = [r['fixed'].get(label) for r in eligible]
        summaries[label] = ({key: float(np.mean([x['outer'][key] for x in items]))
                            for key in ('velocity_mse', 'logg_mse')} if all(x is not None for x in items) else None)
    for model in HALOS:
        for j, count in enumerate(GRIDS):
            items = [r['halo_fits'].get(model, [None, None])[j] for r in eligible]
            key = f'{model}_{count}'
            summaries[key] = ({q: float(np.mean([x['readout']['outer'][q] for x in items]))
                               for q in ('velocity_mse', 'logg_mse')} if all(x is not None for x in items) else None)
            if all(x is not None for x in items):
                boundaries[key] = dict(galaxies=len(items), amplitude_zero=sum(x['selected']['amplitude_boundary'] for x in items),
                    scale_unidentified=sum(x['selected']['scale_unidentified_at_zero_amplitude'] for x in items),
                    selected_kinds={kind: sum(x['selected']['kind'] == kind for x in items)
                                    for kind in sorted({x['selected']['kind'] for x in items})})
    return dict(status='QUALIFIED_COMPLETE_CENSUS' if all(r['status'] in ('QUALIFIED', 'EXCLUDED_LT6') for r in receipts)
                else 'UNRESOLVED_COMPLETE_CENSUS', freeze=freeze, case_sha256=case_hashes,
        census=len(receipts), eligible=len(eligible), excluded=[dict(name=r['name'], reason=r['reason']) for r in receipts if r['n'] < 6],
        outcomes=[dict(index=r['index'], name=r['name'], status=r['status']) for r in receipts],
        outer_galaxy_balanced_MSE=summaries, boundary_frequencies=boundaries,
        paired_per_galaxy=[dict(name=r['name'], differences=r.get('paired_outer_differences')) for r in eligible],
        numerical_failures={r['name']: [c for c in r['controls'] if not c['passed']] for r in eligible if r['status'] != 'QUALIFIED'},
        summed_case_seconds=sum(r.get('seconds', 0.) for r in receipts),
        interpretation='Exposed radial development test. Unresolved aggregate entries are diagnostic, not qualified predictions.')


def main():
    global DEADLINE
    started = time.perf_counter()
    DEADLINE = started+55
    saved, original, groups, freeze = inputs()
    frozen_path = ROOT/(STEM+'_FROZEN.json')
    if sys.argv[1:] == ['freeze']:
        publish(frozen_path, freeze)
        print(json.dumps(dict(status='FROZEN', path=str(frozen_path), sha256=sha(frozen_path), census=len(groups))))
        return
    if sys.argv[1:] not in ([], ['run'], ['tests']):
        raise ValueError('Use freeze, tests, or run/default')
    if json.loads(frozen_path.read_text()) != freeze:
        raise RuntimeError('Freeze differs')
    freeze_hash = sha(frozen_path)
    testpath = ROOT/(STEM+'_TESTS.json')
    if not testpath.exists():
        controls = synthetic_tests()
        publish(testpath, dict(freeze_sha256=freeze_hash, controls=controls,
                              passed=all(c['passed'] for c in controls), seconds=time.perf_counter()-started))
    tests = json.loads(testpath.read_text())
    if tests['freeze_sha256'] != freeze_hash or not tests['passed'] or not all(c['passed'] for c in tests['controls']):
        raise RuntimeError('Synthetic qualification failed or mismatched; receipt preserved')
    if sys.argv[1:] == ['tests']:
        print(json.dumps(dict(status='TESTS_PASSED', sha256=sha(testpath), checks=len(tests['controls']))))
        return
    target = ROOT/(STEM+'_RESULT.json')
    if target.exists() or target.is_symlink():
        raise FileExistsError(target)
    directory = ROOT/(STEM+'_CASES')
    directory.mkdir(exist_ok=True)
    completed, paused = [], None
    for i, (name, rows) in enumerate(groups):
        path = directory/f'galaxy_{i:03d}.json'
        if path.exists() or path.is_symlink():
            prior = json.loads(path.read_text())
            if prior['freeze_sha256'] != freeze_hash or prior['rows_sha256'] != digest(rows) or prior['name'] != name or prior['index'] != i:
                raise RuntimeError('Existing galaxy receipt identity differs')
            continue
        try:
            budget()
            partial = {}
            result = one_galaxy(i, name, rows, freeze_hash, partial)
        except TimeoutError:
            paused = dict(index=i, name=name)
            break
        except Exception as exc:
            result = partial or dict(index=i, name=name, n=len(rows), rows=rows, rows_sha256=digest(rows),
                                     freeze_sha256=freeze_hash, controls=[], fixed={}, halo_fits={})
            result.update(status='ERROR', reason=f'{type(exc).__name__}: {exc}')
        publish(path, result)
        completed.append(dict(index=i, name=name, status=result['status']))
    paths = [directory/f'galaxy_{i:03d}.json' for i in range(100)]
    if all(p.exists() for p in paths):
        receipts = [json.loads(p.read_text()) for p in paths]
        result = aggregate(receipts, freeze, {p.name: sha(p) for p in paths})
        result.update(synthetic_tests_sha256=sha(testpath), last_invocation_seconds=time.perf_counter()-started,
                      peak_self_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
        publish(target, result)
        print(json.dumps(dict(status=result['status'], path=str(target), sha256=sha(target),
            eligible=result['eligible'], outer_galaxy_balanced_MSE=result['outer_galaxy_balanced_MSE'],
            boundary_frequencies=result['boundary_frequencies'], seconds=time.perf_counter()-started)))
    else:
        print(json.dumps(dict(status='PARTIAL_RESUMABLE', completed_this_invocation=completed,
            completed_census=sum(p.exists() for p in paths), paused_before_completion=paused,
            seconds=time.perf_counter()-started, next_command='same script run; no source changes')))


if __name__ == '__main__':
    main()
