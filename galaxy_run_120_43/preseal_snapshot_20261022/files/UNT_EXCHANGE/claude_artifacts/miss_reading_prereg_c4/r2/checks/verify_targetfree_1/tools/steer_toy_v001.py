# steer_toy_v001.py - verify_targetfree_1 (B-1). SYNTHETIC, DIMENSIONLESS, NON-PHYSICAL toy.
# Purpose: show that, once predictions are visible, the outcome of each M-1 / M-3 option on the
# pattern P1 (OUTER_DEFICIT) becomes predictable from a rough "public" knowledge of the target shape,
# i.e. that an option chosen after step 5 can be chosen for its effect on the reading.
# No project data, no model, no target file. Every number below is a synthetic sentinel.
import json, sys
import numpy as np

OUT = sys.argv[1]
rng = np.random.default_rng(20261018)

# synthetic radii in "radius units" placed so the prereg's rule cuts 10 and 30 give 24/11/8 rows
R = np.concatenate([np.linspace(0.5, 9.5, 24), np.linspace(10.5, 28.5, 11), np.linspace(30.5, 44.5, 8)])
zone = np.where(R < 10.0, 0, np.where(R < 30.0, 1, 2))  # 0 INNER, 1 TRANSITION, 2 OUTER
shape = 1.0 - np.exp(-R / 2.0)          # synthetic "publicly known" flat-at-1 shape
SIG = 0.02                               # synthetic quoted error, dimensionless

def preds(d):
    # synthetic prediction: follows the shape, then falls below it by up to fraction d at the far edge
    return shape * (1.0 - d * np.clip((R - 10.0) / 34.0, 0.0, 1.0))

def patterns(p, lo, hi, v, near_opt, md_frac, s_thr):
    r = (p - v) / SIG
    hit = np.abs(r) <= 1.0
    if near_opt == 'a':
        near = (~hit) & (lo <= v + SIG) & (hi >= v - SIG)
    elif near_opt == 'b':
        near = (~hit) & (np.abs(r) > 1.0) & (np.abs(r) <= 2.0)
    else:
        near = np.zeros_like(hit)
    miss = (~hit) & (~near)
    out = {}
    for z in (0, 1, 2):
        sel = zone == z
        nv = int(sel.sum()); H = int(hit[sel].sum()); M = int(miss[sel].sum())
        m = float(np.median(r[sel]))
        S = 'DEFICIT' if m < -s_thr else ('EXCESS' if m > s_thr else 'CENTERED')
        out[z] = dict(nv=nv, H=H, M=M, m=m, S=S, md=(nv >= 1 and M >= md_frac * nv), hd=(nv >= 1 and H >= 0.5 * nv))
    P1 = out[2]['md'] and out[2]['S'] == 'DEFICIT'
    P5 = out[0]['hd'] and out[2]['md'] and out[1]['nv'] >= 1 and not out[1]['hd']
    P8 = int(miss.sum()) == 0
    return dict(P1=bool(P1), P5=bool(P5), P8=bool(P8))

OPTIONS = {
    'M1a_as_written': ('a', 0.5, 1.0),
    'M1b_sigma_multiple': ('b', 0.5, 1.0),
    'M1c_no_near': ('c', 0.5, 1.0),
    'M3_md_two_thirds': ('a', 2.0 / 3.0, 1.0),
    'M3_S_at_2': ('a', 0.5, 2.0),
}
NDRAW = 20000

def p1_rates(d, w, ndraw=NDRAW, prior_level=0.03):
    p = preds(d); lo = p * (1 - w); hi = p * (1 + w)
    counts = {k: 0 for k in OPTIONS}
    for _ in range(ndraw):
        g = rng.normal(0.0, prior_level)                 # rough public-knowledge uncertainty in level
        v = shape * (1.0 + g) + rng.normal(0.0, 0.01, R.size)
        for k, (no, mf, st) in OPTIONS.items():
            counts[k] += patterns(p, lo, hi, v, no, mf, st)['P1']
    return {k: counts[k] / ndraw for k in OPTIONS}

res = {'schema': 'VERIFY_TF1_STEER_TOY_V001', 'synthetic': True, 'units': 'dimensionless sentinels; not physical',
       'rows': {'INNER': int((zone == 0).sum()), 'TRANSITION': int((zone == 1).sum()), 'OUTER': int((zone == 2).sum())},
       'sigma': SIG, 'rough_knowledge_level_sd': 0.03, 'draws_per_case': NDRAW,
       'known_prediction_cases': {}, 'blind_case': {}}
# (1) the ruler has seen the predictions (one realised model behaviour per case)
for name, d, w in [('no_deficit', 0.0, 0.03), ('marginal_deficit', 0.06, 0.03), ('large_deficit', 0.30, 0.03),
                   ('marginal_deficit_wide_band', 0.06, 0.08)]:
    rates = p1_rates(d, w)
    res['known_prediction_cases'][name] = {'outer_deficit_fraction_d': d, 'band_half_width_w': w,
                                            'P_P1_by_option': rates,
                                            'max_minus_min': max(rates.values()) - min(rates.values())}
# (2) the ruler has NOT seen predictions: d and w drawn from a broad prior, one realised dataset per draw
nb = 4000; cnt = {k: 0 for k in OPTIONS}
for _ in range(nb):
    d = rng.uniform(0.0, 0.3); w = rng.uniform(0.01, 0.08)
    p = preds(d); lo = p * (1 - w); hi = p * (1 + w)
    g = rng.normal(0.0, 0.03); v = shape * (1.0 + g) + rng.normal(0.0, 0.01, R.size)
    for k, (no, mf, st) in OPTIONS.items():
        cnt[k] += patterns(p, lo, hi, v, no, mf, st)['P1']
res['blind_case'] = {'prior': 'd ~ U(0,0.3), w ~ U(0.01,0.08)', 'draws': nb,
                     'P_P1_by_option': {k: cnt[k] / nb for k in OPTIONS}}
res['reading'] = ('Known-prediction cases: in the marginal cases the P1 probability differs strongly between options, '
                  'so a ruler who has seen the predictions can pick an option for its effect on P1; in the no/large '
                  'deficit cases the options do not matter and can be picked at no cost. Blind case: the ruler only '
                  'knows prior averages.')
with open(OUT, 'x') as f:
    json.dump(res, f, indent=1, sort_keys=True)
print(json.dumps({k: v['P_P1_by_option'] for k, v in res['known_prediction_cases'].items()}, indent=1))
print(json.dumps(res['blind_case'], indent=1))
