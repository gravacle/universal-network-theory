"""Checker probe: decision equivalence of the V006 draft compare (e6475f38 + prereg f90ab96c, synthetic max_iterations 16)
and the R1 compare (a7816746 + prereg 807fc5bf, synthetic max_iterations 32) over a grid of synthetic C5/C6 deltas, plus
targeted L1/L2/M1 probes.  Real R3 adapted records for C4/C3/C2/R (read-only).  Writes one JSON to argv[1] (must not exist)."""
import copy, importlib.util, json, sys, itertools
from pathlib import Path
L = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/kmax_prereg_v005_c2/extension_c5c6')
def load(p, n):
    s = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
D = load(L / 'prereg_v006/kmax_compare_ext_c2v006.py', 'draft')
R = load(L / 'v006_r1/prereg/kmax_compare_ext_c2v006_r1.py', 'r1')
preD = json.loads((L / 'prereg_v006/KMAX_MATRIX_PREREG_V006.json').read_text())
preR = json.loads((L / 'v006_r1/prereg/KMAX_MATRIX_PREREG_V006_R1.json').read_text())
bi = preR['binding_inputs']
pre5 = json.loads(Path(bi['prereg_v005']['path']).read_text())
C5M = R.load_pinned(bi['v005_compare']['path'], bi['v005_compare']['sha256'], 'c5m')
r3 = json.loads(Path(bi['r3_recovery']['path']).read_text())['brackets']
cases = {c['id']: c for c in preR['cases']}
real = {cid: C5M.adapt_result(cases[cid]['bound']['result']['path']) for cid in ('C4', 'C3', 'C2', 'R')}
ids = pre5['row_ids']; tau = dict(zip(ids, pre5['tau_km_s']))
v9 = bi['drivers']['v009']['sha256']
def synth(pre, cid, base, mult, maxit, workers=8):
    a = copy.deepcopy(real['C4'])
    a['rows'] = {i: base[i] + mult * tau[i] * (1 if k % 2 == 0 else -1) for k, i in enumerate(ids)}
    a['driver_sha256'] = v9
    a['grid_spec'] = pre['grids'][cases[cid]['grid']]['composite_grid_spec']
    ns = a['normalized_spec']; ns['numerics']['composite_grid_spec'] = a['grid_spec']
    ns['numerics']['route_a'] = {'column_workers': workers, 'max_iterations': maxit}; ns['admit'] = {}
    return a
def build(pre, d45, d56, maxit, workers=8):
    ad = dict(real)
    c5 = synth(pre, 'C5', real['C4']['rows'], d45, maxit, workers); c6 = synth(pre, 'C6', c5['rows'], d56, maxit, workers)
    ad['C5'], ad['C6'] = c5, c6
    return ad
pk = lambda ad: {c: {'V4': True, 'V5': True} for c in ad}
v7 = {c: {'V7': True} for c in ('C5', 'C6')}
ok9 = {'admissible': True, 'reason': 'synthetic'}
out = {'grid': [], 'probes': {}}
vals = [0.0, 0.3, 0.5, 0.8, 0.999999, 1.0000001, 1.5, 2.0, 4.0, 10.0]
neq = 0
for d45, d56 in itertools.product(vals, vals):
    adD = build(preD, d45, d56, 16); adR = build(preR, d45, d56, 32)
    eD = D.evaluate_ext(preD, pre5, C5M, adD, pk(adD), r3, ok9, v7)
    eR = R.evaluate_ext(preR, pre5, C5M, adR, pk(adR), r3, ok9, v7, {'admissible': True}, True)
    a = (eD['decision']['outcome'], eD['decision'].get('subtype')); b = (eR['decision']['outcome'], eR['decision'].get('subtype'))
    same_stats = json.dumps(eD.get('sequence', eD.get('pairs')), sort_keys=True, default=float) == json.dumps(eR.get('sequence', eR.get('pairs')), sort_keys=True, default=float)
    dD = {k: v for k, v in eD['decision'].items() if k not in ('rule',)}; dR = {k: v for k, v in eR['decision'].items() if k not in ('rule',)}
    full_eq = json.dumps(dD, sort_keys=True, default=float) == json.dumps(dR, sort_keys=True, default=float)
    if a != b or not full_eq: neq += 1
    out['grid'].append({'d45': d45, 'd56': d56, 'draft': a, 'r1': b, 'decision_dict_equal_excl_rule': full_eq})
out['grid_n'] = len(out['grid']); out['grid_not_equal'] = neq
out['evaluate_keys_draft'] = sorted(eD.keys()); out['evaluate_keys_r1'] = sorted(eR.keys())
# M1: 16 rejected under R1, 32 rejected under draft
adR16 = build(preR, 0.8, 0.3, 16); e = R.evaluate_ext(preR, pre5, C5M, adR16, pk(adR16), r3, ok9, v7, {'admissible': True}, True)
out['probes']['M1_r1_maxit16'] = [e['decision']['outcome'], e['gates']['C5']['V3_mismatch']]
adR33 = build(preR, 0.8, 0.3, 33); e = R.evaluate_ext(preR, pre5, C5M, adR33, pk(adR33), r3, ok9, v7, {'admissible': True}, True)
out['probes']['M1_r1_maxit33'] = [e['decision']['outcome'], e['gates']['C5']['V3_mismatch']]
adR4 = build(preR, 0.8, 0.3, 32, workers=4); e = R.evaluate_ext(preR, pre5, C5M, adR4, pk(adR4), r3, ok9, v7, {'admissible': True}, True)
out['probes']['M1_r1_workers4'] = [e['decision']['outcome'], e['gates']['C5']['V3_mismatch']]
# L1: C4 and R sha mutation under R3 and under R(n)
for cid in ('C4', 'R', 'C2'):
    for isr3 in (True, False):
        ad = build(preR, 0.8, 0.3, 32); ad[cid] = dict(ad[cid], result_sha256='0' * 64)
        e = R.evaluate_ext(preR, pre5, C5M, ad, pk(ad), r3, ok9, v7, {'admissible': True}, isr3)
        out['probes']['L1_%s_sha_mut_r3_%s' % (cid, isr3)] = [e['decision']['outcome'], e['gates'][cid]['failed'], e['gates'][cid]['V3_mismatch'][:1]]
# L1: C3 result placed in C4 slot under R3
ad = build(preR, 0.8, 0.3, 32); ad['C4'] = copy.deepcopy(real['C3'])
e = R.evaluate_ext(preR, pre5, C5M, ad, pk(ad), r3, ok9, v7, {'admissible': True}, True)
out['probes']['L1_C3_in_C4_slot'] = [e['decision']['outcome'], e['gates']['C4']['V3_mismatch']]
# L2: v005 inadmissible
ad = build(preR, 0.8, 0.3, 32)
e = R.evaluate_ext(preR, pre5, C5M, ad, pk(ad), r3, ok9, v7, {'admissible': False, 'reason': 'probe'}, True)
out['probes']['L2_v005_inadmissible'] = {c: e['gates'][c]['failed'] for c in ('C4', 'C3', 'C2', 'R', 'C5', 'C6')}
out['probes']['L2_v005_inadmissible_outcome'] = e['decision']['outcome']
out['probes']['L2_next_step_is_V005_text'] = e['decision']['next_step']['C4']['V3'] == pre5['amendment_v005']['driver']['inadmissible_next_step']
out['probes']['L2_v005_none'] = R.evaluate_ext(preR, pre5, C5M, ad, pk(ad), r3, ok9, v7, None, True)['decision']['outcome']
# L2: real execution
v5 = C5M.v005_admissibility(pre5); out['probes']['L2_real'] = {k: v5.get(k) for k in ('admissible', 'verdict', 'reason', 'result_sha256', 'finish_sha256')}
# L4
ad = build(preR, 0.8, 0.3, 32)
for k in ('primary_N8', 'alternate_N1'):
    ad['C5'] = dict(ad['C5'], result_path=cases['C5']['outdirs'][k]['outdir'] + '/result.json')
    e = R.evaluate_ext(preR, pre5, C5M, ad, pk(ad), r3, ok9, v7, {'admissible': True}, True)
    out['probes']['L4_' + k] = [e['gates']['C5']['registered_outdir'], e['decision']['outcome']]
symlink = '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs_ext/KMAX_A2F10_C5R3_RUN_V001/result.json'
ad['C5'] = dict(ad['C5'], result_path=symlink)
e = R.evaluate_ext(preR, pre5, C5M, ad, pk(ad), r3, ok9, v7, {'admissible': True}, True)
out['probes']['L4_via_symlink_path'] = [e['gates']['C5']['registered_outdir'], e['decision']['outcome']]
with open(sys.argv[1], 'x') as f:
    json.dump(out, f, indent=1, default=str); f.write('\n')
print(json.dumps({'grid_n': out['grid_n'], 'grid_not_equal': out['grid_not_equal'], 'keys_equal': out['evaluate_keys_draft'] == out['evaluate_keys_r1'], **out['probes']}, indent=1, default=str))
