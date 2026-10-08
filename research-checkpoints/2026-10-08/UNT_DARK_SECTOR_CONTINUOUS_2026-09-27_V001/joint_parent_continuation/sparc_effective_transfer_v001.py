"""One-worker, galaxy-grouped effective-response screen; not a disk PDE solve."""
import hashlib
import json
import math
from pathlib import Path
import resource
import time

import numpy as np
import disk_solver as law

ROOT = Path(__file__).resolve().parent
DATA = ROOT / 'external_ddo154_v001'
PREFIX = 'SPARC_EFFECTIVE_TRANSFER_V001'
KPC = 3.085677581491367e19
CONV = 1e6 / KPC
MODELS = ('baryons', 'inherited_fixed', 'inherited_calibrated', 'rar_calibrated')


def metadata():
    out = {}
    for line in (DATA / 'SPARC_Lelli2016c.mrt').read_text().splitlines():
        fields = line.split()
        if len(fields) != 19:
            continue
        try:
            int(fields[1])  # Hubble type: also rejects descriptive header lines.
            item = dict(name=fields[0], D=float(fields[2]), eD=float(fields[3]),
                        method=int(fields[4]), inc=float(fields[5]), einc=float(fields[6]),
                        rdisk=float(fields[11]), sb=float(fields[12]), quality=int(fields[17]))
        except ValueError:
            continue
        assert item['name'] not in out
        out[item['name']] = item
    assert len(out) == 175, len(out)
    return out


def load_data():
    meta = metadata()
    selected, excluded = {}, []
    for lineno, line in enumerate((DATA / 'SPARC_MassModels_Lelli2016c.mrt').read_text().splitlines(), 1):
        vals = line.split()
        if not vals or vals[0] not in meta:
            continue
        assert len(vals) == 10, (lineno, vals)
        name = vals[0]
        D, R, v, ev, vg, vd, vb, sbd, sbb = map(float, vals[1:])
        m = meta[name]
        bar2 = vg * abs(vg) + .5 * vd**2 + .7 * vb**2
        reasons = []
        if name in ('NGC3198', 'DDO154'):
            reasons.append('already_modeled')
        if m['quality'] > 2:
            reasons.append('quality_gt_2')
        if m['inc'] < 30:
            reasons.append('inclination_lt_30')
        if not all(math.isfinite(z) for z in (D, R, v, ev, vg, vd, vb, bar2)):
            reasons.append('nonfinite')
        if min(R, v, ev, bar2) <= 0:
            reasons.append('nonpositive_R_v_error_or_bar2')
        if reasons:
            excluded.append(dict(line=lineno, name=name, reasons=reasons))
            continue
        # Catalogue distances are rounded but should agree at displayed precision.
        assert abs(D - m['D']) <= .011, (name, D, m['D'])
        selected.setdefault(name, []).append([lineno, R, v, ev, vg, vd, vb])
    groups = []
    for name, rows in sorted(selected.items()):
        digest = hashlib.sha256(name.encode('utf8')).hexdigest()
        role = 'calibration' if int(digest, 16) % 3 == 0 else 'evaluation'
        groups.append(dict(meta=meta[name], role=role, name_hash=digest,
                           rows=np.asarray(rows, dtype=float)))
    return groups, excluded


def arrays(group, variant='central'):
    m, t = group['meta'], group['rows']
    R, v = t[:, 1].copy(), t[:, 2].copy()
    vg, vd, vb = t[:, 4], t[:, 5], t[:, 6]
    stars = 10**(.1 if variant == 'stellar_plus' else -.1) if variant.startswith('stellar_') else 1.
    bar2 = vg * np.abs(vg) + stars * (.5 * vd**2 + .7 * vb**2)
    if variant.startswith('distance_'):
        Dnew = m['D'] + (1 if variant.endswith('plus') else -1) * m['eD']
        if Dnew <= 0:
            return None, 'nonpositive_distance'
        scale = Dnew / m['D']
        R *= scale
        bar2 *= scale
    if variant.startswith('inclination_'):
        inew = m['inc'] + (1 if variant.endswith('plus') else -1) * m['einc']
        if not 0 < inew <= 90:
            return None, 'inclination_outside_0_90'
        v *= math.sin(math.radians(m['inc'])) / math.sin(math.radians(inew))
    if np.any(bar2 <= 0):
        return None, 'nonpositive_bar2_after_sensitivity'
    return dict(R=R, v=v, gbar=CONV * bar2 / R, gobs=CONV * v**2 / R), None


def prediction(gbar, model, a0):
    if model == 'baryons':
        return gbar.copy()
    if model.startswith('inherited'):
        return a0 * law.inverse(gbar / a0)
    assert model == 'rar_calibrated'
    return gbar / (-np.expm1(-np.sqrt(gbar / a0)))


def golden(fun, lo, hi):
    ratio = (math.sqrt(5) - 1) / 2
    c, d = hi - ratio * (hi - lo), lo + ratio * (hi - lo)
    fc, fd = fun(c), fun(d)
    for _ in range(70):
        if fc < fd:
            hi, d, fd = d, c, fc
            c = hi - ratio * (hi - lo)
            fc = fun(c)
        else:
            lo, c, fc = c, d, fd
            d = lo + ratio * (hi - lo)
            fd = fun(d)
    x = (lo + hi) / 2
    return dict(log10_a0=x, loss=fun(x))


def fit(gbar, gobs, weights, model, ngrid):
    def fun(x):
        res = np.log10(prediction(gbar, model, 10**x) / gobs)
        return float(np.sum(weights * res**2))
    grid = np.linspace(-12, -8, ngrid)
    losses = [fun(float(x)) for x in grid]
    candidates = [dict(log10_a0=-12., loss=losses[0]), dict(log10_a0=-8., loss=losses[-1])]
    for i in range(1, ngrid - 1):
        if losses[i] <= losses[i-1] and losses[i] <= losses[i+1]:
            candidates.append(golden(fun, float(grid[i-1]), float(grid[i+1])))
    best = min(candidates, key=lambda row: row['loss'])
    return dict(best=best, candidates=candidates, grid_log10=grid.tolist(), grid_loss=losses,
                boundary=best['log10_a0'] in (-12., -8.))


def check(controls, name, value, bound):
    controls.append(dict(name=name, value=float(value), bound=float(bound), passed=bool(value <= bound)))


def qualification():
    controls = []
    check(controls, 'inherited_r', abs(law.RATIO / 25.51664211557329 - 1), 1e-14)
    d = np.logspace(-8, 4, 61)
    x = law.inverse(d)
    check(controls, 'inverse_relative_residual', np.max(np.abs(law.f(x) / d - 1)), 1e-9)
    check(controls, 'positive_monotone', 0 if np.all(x > 0) and np.all(np.diff(x) > 0) else 1, 0)
    check(controls, 'low_asymptote', abs(float(law.f(1e-8)) / 1e-16 - 1), 1e-6)
    check(controls, 'high_asymptote', abs(float(law.f(1e8)) / 1e8 - 1), 1e-5)
    check(controls, 'signed_gas', abs((-2 * abs(-2) + .5 * 4**2 + .7 * 3**2) - 10.3), 1e-13)
    fake = dict(meta=dict(D=10., eD=2., inc=60., einc=5.),
                rows=np.array([[1., 2., 100., 5., -2., 40., 0.]]))
    a, _ = arrays(fake)
    b, _ = arrays(fake, 'distance_plus')
    check(controls, 'distance_gbar_invariance', np.max(np.abs(b['gbar'] / a['gbar'] - 1)), 1e-14)
    check(controls, 'distance_gobs_scaling', np.max(np.abs(b['gobs'] / a['gobs'] - 1/1.2)), 1e-14)
    b, _ = arrays(fake, 'inclination_plus')
    expected = (math.sin(math.radians(60)) / math.sin(math.radians(65)))**2
    check(controls, 'inclination_gobs_scaling', np.max(np.abs(b['gobs'] / a['gobs'] - expected)), 1e-14)
    for model in ('inherited_calibrated', 'rar_calibrated'):
        gb = np.logspace(-13, -8, 45)
        go = prediction(gb, model, 1.7e-10)
        f = fit(gb, go, np.ones(45)/45, model, 81)
        check(controls, model+'_synthetic_scale', abs(f['best']['log10_a0'] - math.log10(1.7e-10)), 1e-6)
        check(controls, model+'_synthetic_loss', f['best']['loss'], 1e-12)
    return controls


def score(groups, params, variant='central', save_rows=False):
    records, invalid, detailed = [], [], []
    for group in groups:
        a, reason = arrays(group, variant)
        name = group['meta']['name']
        if reason:
            invalid.append(dict(name=name, rows=len(group['rows']), reason=reason))
            continue
        row = dict(name=name, role=group['role'], rows=len(group['rows']), models={})
        row['meta'] = group['meta']
        predictions, residuals = {}, {}
        for model in MODELS:
            gp = prediction(a['gbar'], model, params[model])
            res = np.log10(gp / a['gobs'])
            vp = np.sqrt(gp * a['R'] / CONV)
            predictions[model], residuals[model] = gp, res
            row['models'][model] = dict(loss=float(np.mean(res**2)), bias_dex=float(np.mean(res)),
                                       velocity_mse=float(np.mean((vp-a['v'])**2)))
        records.append(row)
        if save_rows:
            for i, original in enumerate(group['rows']):
                detailed.append(dict(name=name, role=group['role'], source_line=int(original[0]),
                    R_kpc=float(a['R'][i]), vobs_kms=float(a['v'][i]), evobs_kms=float(original[3]),
                    gbar_si=float(a['gbar'][i]), gobs_si=float(a['gobs'][i]),
                    gpred_si={m: float(predictions[m][i]) for m in MODELS},
                    residual_dex={m: float(residuals[m][i]) for m in MODELS},
                    r_over_rdisk=float(a['R'][i]/group['meta']['rdisk']) if group['meta']['rdisk'] > 0 else None,
                    central_brightness=group['meta']['sb']))
    summary = {}
    for role in ('calibration', 'evaluation'):
        rg = [r for r in records if r['role'] == role]
        summary[role] = dict(galaxies=len(rg), rows=sum(r['rows'] for r in rg), models={})
        for model in MODELS:
            losses = [r['models'][model]['loss'] for r in rg]
            summary[role]['models'][model] = dict(galaxy_balanced_rms_dex=math.sqrt(float(np.mean(losses))),
                galaxy_balanced_bias_dex=float(np.mean([r['models'][model]['bias_dex'] for r in rg])),
                galaxy_balanced_velocity_rms_kms=math.sqrt(float(np.mean([r['models'][model]['velocity_mse'] for r in rg]))))
    return dict(summary=summary, galaxies=records, invalid=invalid, predictions=detailed)


def diagnostics(rows):
    out = {}
    ev = [r for r in rows if r['role'] == 'evaluation']
    definitions = dict(gbar_si=[0., 1e-11, 1e-10, math.inf],
                       r_over_rdisk=[0., 2., 4., math.inf],
                       central_brightness=[0., 100., 1000., math.inf])
    for key, edges in definitions.items():
        bins = []
        for lo, hi in zip(edges[:-1], edges[1:]):
            subset = [r for r in ev if r[key] is not None and lo <= r[key] < hi]
            byname = {}
            for r in subset:
                byname.setdefault(r['name'], []).append(r)
            stats = {}
            for model in MODELS:
                losses = [np.mean([r['residual_dex'][model]**2 for r in gr]) for gr in byname.values()]
                biases = [np.mean([r['residual_dex'][model] for r in gr]) for gr in byname.values()]
                stats[model] = dict(rms_dex=math.sqrt(float(np.mean(losses))) if losses else None,
                                    bias_dex=float(np.mean(biases)) if biases else None)
            bins.append(dict(lo=lo, hi=hi if math.isfinite(hi) else None,
                             galaxies=len(byname), rows=len(subset), models=stats))
        out[key] = bins
    return out


def bootstrap(records):
    ev = [r for r in records if r['role'] == 'evaluation']
    rng = np.random.default_rng(424027)
    indices = rng.integers(0, len(ev), size=(10000, len(ev)))
    out = {}
    for left, right in [('inherited_calibrated', 'baryons'), ('rar_calibrated', 'baryons'),
                        ('inherited_calibrated', 'rar_calibrated')]:
        delta = np.array([r['models'][left]['loss'] - r['models'][right]['loss'] for r in ev])
        means = np.mean(delta[indices], axis=1)
        out[left+'_minus_'+right] = dict(mean_loss_difference_dex2=float(np.mean(delta)),
             paired_percentiles_2p5_97p5=np.percentile(means, [2.5, 97.5]).tolist(),
             galaxies_left_better=int(np.sum(delta < 0)), galaxies=len(ev))
    return out


def main():
    started = time.perf_counter()
    result_path = ROOT / (PREFIX+'_RESULT.json')
    assert not result_path.exists(), 'Completed or failed receipt exists; do not rerun.'
    files = [Path(__file__), ROOT/(PREFIX+'.md'), ROOT/'disk_solver.py', law.SHAPE_PATH,
             DATA/'SPARC_Lelli2016c.mrt', DATA/'SPARC_MassModels_Lelli2016c.mrt']
    identities = {str(p.relative_to(ROOT.parent)): law.sha(p) for p in files}
    groups, excluded = load_data()
    split = [dict(name=g['meta']['name'], role=g['role'], name_sha256=g['name_hash'],
                  rows=len(g['rows'])) for g in groups]
    freeze = dict(files=identities, split=split, excluded_rows=excluded, r=law.RATIO,
                  disk_ml=.5, bulge_ml=.7, numpy_version=np.__version__)
    frozen_path = ROOT/(PREFIX+'_FROZEN.json')
    law.save_new(frozen_path, freeze)  # Membership and code frozen BEFORE calibration.
    controls = qualification()
    payload = dict(frozen_sha256=law.sha(frozen_path), controls=controls)
    if not all(c['passed'] for c in controls):
        payload['status'] = 'FAILED_PRE_OBSERVATION_NUMERICAL_CONTROL'
        law.save_new(result_path, payload)
        print(json.dumps(payload), flush=True)
        return
    train = [g for g in groups if g['role'] == 'calibration']
    aa = [arrays(g)[0] for g in train]
    gb = np.concatenate([a['gbar'] for a in aa])
    go = np.concatenate([a['gobs'] for a in aa])
    weights = np.concatenate([np.full(len(a['R']), 1/(len(train)*len(a['R']))) for a in aa])
    fits, params = {}, dict(baryons=0., inherited_fixed=1.2e-10)
    for model in ('inherited_calibrated', 'rar_calibrated'):
        coarse = fit(gb, go, weights, model, 81)
        fine = fit(gb, go, weights, model, 161)
        check(controls, model+'_grid_scale', abs(coarse['best']['log10_a0']-fine['best']['log10_a0']), 1e-6)
        check(controls, model+'_grid_loss', abs(coarse['best']['loss']-fine['best']['loss']), 1e-10)
        fits[model] = dict(coarse=coarse, fine=fine)
        params[model] = 10**fine['best']['log10_a0']
    # Inverse qualification on the actual prediction domain, including endpoint calibrations.
    variants = ('distance_minus', 'distance_plus', 'inclination_minus', 'inclination_plus',
                'stellar_minus', 'stellar_plus')
    qualification_arrays = [arrays(g, v)[0] for g in groups for v in ('central',) + variants]
    allgb = np.concatenate([a['gbar'] for a in qualification_arrays if a is not None])
    d = np.geomspace(float(np.min(allgb)/1e-8), float(np.max(allgb)/1e-12), 101)
    check(controls, 'actual_domain_inverse_relative_residual', np.max(np.abs(law.f(law.inverse(d))/d-1)), 1e-9)
    payload.update(fits=fits, a0_si=params, inverse_domain=[float(d[0]), float(d[-1])])
    if not all(c['passed'] for c in controls):
        payload['status'] = 'FAILED_CALIBRATION_NUMERICAL_CONTROL_NO_EVALUATION'
    else:
        central = score(groups, params, save_rows=True)
        sensitivities = {v: score(groups, params, v) for v in variants}
        payload.update(status='COMPLETE_DESCRIPTIVE_EFFECTIVE_TRANSFER', central=central,
                       sensitivities=sensitivities, paired_bootstrap=bootstrap(central['galaxies']),
                       diagnostic_bins=diagnostics(central['predictions']))
    payload.update(seconds=time.perf_counter()-started,
                   peak_self_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    law.save_new(result_path, payload)
    print(json.dumps(dict(status=payload['status'], controls_passed=sum(c['passed'] for c in controls),
        controls=len(controls), a0_si=params, summary=payload.get('central', {}).get('summary'),
        paired_bootstrap=payload.get('paired_bootstrap'), seconds=payload['seconds'],
        peak_self_rss_bytes=payload['peak_self_rss_bytes'], result_sha256=law.sha(result_path)), indent=2), flush=True)


if __name__ == '__main__':
    main()
