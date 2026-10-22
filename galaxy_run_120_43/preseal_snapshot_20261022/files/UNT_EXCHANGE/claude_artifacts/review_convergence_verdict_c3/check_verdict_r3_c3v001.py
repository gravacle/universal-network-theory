"""Distinct check of the sealed KMAX convergence verdict on D7 R3 (Claude3, dispatch 0490).
Own implementation from the prereg text (dbddc02c); does not import or call kmax_compare_c2v005. Reads the 10 R3
result.json (authorized by 0490 after the verdict was registered) and their custody files. Writes one JSON (exclusive)."""
import hashlib, json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
P = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/kmax_prereg_v005_c2'
PIN = {'prereg': (P + '/KMAX_MATRIX_PREREG_V005.json', 'dbddc02c4d793b44a12136fc4fc88b20c001865ddd4c89b1b70c57bc406bb174'),
       'compare_script': (P + '/kmax_compare_c2v005.py', '49404bc4b0d558c93113ed650802d9009f03be64c364f0d862213783389786f5'),
       'cases_r3': (P + '/verdict_r3/CASES_R3.json', '0f5faca8a1310646dd78061b06242f84d25f64fba52aee35c9f83628c0f1b6ba'),
       'launch_r3': (P + '/d7_recovery_r3/LAUNCH_R3.json', '172725042203c971f6a6bf30df93c96caddb6d666554902eec57ce7d85b993c1'),
       'recovery_r3': (P + '/d7_recovery_r3/KMAX_D7_RECOVERY_R3.json', '7946b8575a2f95fb093c55e35bfffba48f4a8b5daf5e75d89132446b2b9c7453'),
       'comparison_json': (P + '/verdict_r3/COMPARE_R3_V001/KMAX_COMPARISON.json', '4ea21d902cfb4e8cd3b5aa61d29b8c3bbc05cab9a56c49f3af2913c32ae66433')}
KPC_M = 3.085677581491367e19
def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()
def canon(o): return json.dumps(o, sort_keys=True, separators=(',', ':'), allow_nan=False)
pins = {}
for k, (p, w) in PIN.items():
    h = sha(p)
    if h != w: raise SystemExit('PIN MISMATCH %s %s' % (k, h))
    pins[k] = {'path': p, 'sha256': h}
pre = json.load(open(PIN['prereg'][0])); cmap = json.load(open(PIN['cases_r3'][0])); L = json.load(open(PIN['launch_r3'][0]))
rec = json.load(open(PIN['recovery_r3'][0])); block = rec['brackets']
crit = pre['criterion']; ids = pre['row_ids']; tau = dict(zip(ids, pre['tau_km_s'])); sig = dict(zip(ids, pre['quoted_sigma_km_s']))
CD = {c['id']: c for c in pre['cases']}; anc = pre['anchor']; DRV = {k: v['sha256'] for k, v in pre['binding_inputs']['drivers'].items()}
SH2 = {v: k for k, v in DRV.items()}
F = []   # findings
out = {'schema': 'CHECK_VERDICT_R3_C3V001', 'pins': pins, 'anchor_keys': sorted(anc)}
# ---------------- tau as defined: 0.25 sigma
out['tau_equals_quarter_sigma'] = all(abs(tau[i] - 0.25 * sig[i]) < 1e-15 for i in ids)
# ---------------- 1. inputs
inp = {}
calls = {c['case']: c for c in L['calls']}
out['cases_file_keys_equal_registered'] = sorted(cmap) == sorted(CD)
out['launch_prereg_pin_ok'] = L['prereg']['sha256'] == PIN['prereg'][1] and L['R3']['sha256'] == PIN['recovery_r3'][1]
for cid in CD:
    cn = L['comparison_binding'][cid]; c = calls[cn]; rp = cmap[cid]; od = c['outdir']; e = {'call': cn}
    e['cases_path_is_call_outdir_result'] = rp == od + '/result.json'
    rc = json.load(open(c['receipt'])); ln = json.load(open(c['receipt'] + '.launch.json')); fin = json.load(open(od + '/finish.json'))
    r = json.load(open(rp)); rsha = sha(rp)
    e['receipt'] = {k: rc.get(k) for k in ('status', 'exit_code', 'driver_status', 'retries', 'stop_reason')}
    e['receipt_ok'] = rc.get('status') == 'FINISHED' and rc.get('exit_code') == 0 and rc.get('driver_status') == 'COMPLETED' and rc.get('retries') == 0
    e['launch_pins_ok'] = (ln['pins']['driver']['sha256'] == c['driver_sha256'] and ln['pins']['spec']['sha256'] == c['spec']['sha256']
                           and ln['pins']['spec']['path'] == c['spec']['path'])
    e['finish_ok'] = fin.get('status') == 'COMPLETED' and fin.get('valid') is True and fin.get('result_sha256') == rsha and fin.get('result_path') == rp
    e['result_driver_ok'] = r.get('driver_sha256') == c['driver_sha256'] == DRV[c['driver']]
    e['result_spec_ok'] = r.get('call_spec_sha256') == c['spec']['sha256'] == sha(c['spec']['path'])
    cs = od + '/inputs/call_spec.json'
    e['inputs_call_spec_ok'] = (sha(cs) == c['spec']['sha256']) if os.path.isfile(cs) else None
    e['result_sha256'] = rsha; e['driver'] = c['driver']
    e['all_ok'] = all(e[k] for k in ('cases_path_is_call_outdir_result', 'receipt_ok', 'launch_pins_ok', 'finish_ok', 'result_driver_ok', 'result_spec_ok')) and e['inputs_call_spec_ok'] is not False
    inp[cid] = e
out['inputs'] = inp
dt = pre['binding_inputs']['v005_deciding_test']; req = dt['required']
v5 = {'result_exists': os.path.isfile(dt['result_path'])}
if v5['result_exists']:
    dr = json.load(open(dt['result_path'])); dfin = json.load(open(dt['finish_path'])); drs = sha(dt['result_path'])
    v5.update(finish_binds_result=dfin.get('result_sha256') == drs, driver_ok=dr.get('driver_sha256') == req['driver_sha256'] == DRV['v005'],
              spec_ok=dr.get('call_spec_sha256') == req['call_spec_sha256'], verdict=(dr.get('deciding_test') or {}).get('verdict'),
              required_verdict=req['deciding_test.verdict'], launch_file_sha_ok=sha(dt['launch_file']['path']) == dt['launch_file']['sha256'])
    v5['admissible'] = bool(v5['finish_binds_result'] and v5['driver_ok'] and v5['spec_ok'] and v5['verdict'] == v5['required_verdict'])
out['v005_admissibility'] = v5
# recovery block: containment of anchor entries (widen only) and same non-override keys
ar, br = anc['brackets']['rule'], block['rule']
def contains(o, i): return isinstance(o, list) and len(o) == 2 and o[0] <= i[0] and i[1] <= o[1]
rb = {'mode_rule': block.get('mode') == 'rule', 'same_rule_keys': set(ar) == set(br),
      'non_override_keys_unchanged': all(canon(ar[k]) == canon(br[k]) for k in ar if not k.endswith('_overrides'))}
rb['anchor_entries_contained'] = all(contains(br[k].get(i), v) for k in ('fs_absolute_overrides', 'rfs_factor_overrides') for i, v in ar[k].items()) and \
    all(contains(br['le_factor_overrides'].get(ps, {}).get(i), v) for ps, t in ar['le_factor_overrides'].items() for i, v in t.items())
out['recovery_block'] = rb
# ---------------- 2. gates
def grid_def(gid):
    g = pre['grids'][gid]; cg = g.get('composite_grid_spec')
    return cg, (cg if cg else {'breaks_inverse_kpc': g['breaks_inverse_kpc'], 'panel_orders': g['panel_orders']})
def axis_m(spec):
    parts = []
    for lo, hi, n in zip(spec['breaks_inverse_kpc'][:-1], spec['breaks_inverse_kpc'][1:], spec['panel_orders']):
        x, _ = np.polynomial.legendre.leggauss(n); parts.append(((lo + hi) / 2 + (hi - lo) * x / 2) / KPC_M)
    return np.concatenate(parts)
def mask(k, shape, kmax_m):
    if shape == 'cube': return np.ones(len(k), bool)
    r = np.sqrt(k[:, 0] * k[:, 0] + k[:, 1] * k[:, 1] + k[:, 2] * k[:, 2]) if shape == 'sphere' else np.sqrt(k[:, 0] * k[:, 0] + k[:, 1] * k[:, 1])
    return r <= kmax_m
R, G = {}, {}
for cid, c in CD.items():
    r = json.load(open(cmap[cid])); R[cid] = r; g = {}
    rows = r.get('rows') or []; rid = [x['id'] for x in rows]; sp = {x['id']: x['speed_km_s'] for x in rows}
    g['V1'] = bool(r.get('status') == 'COMPLETED' and r.get('valid') is True and len(rid) == 12 and sorted(rid) == sorted(ids) and len(set(rid)) == 12
                   and all(isinstance(sp[i], (int, float)) and math.isfinite(sp[i]) for i in ids))
    sk = r.get('speeds_km_s'); g['rows_vs_speeds_field'] = (sk == [sp[i] for i in ids]) if isinstance(sk, list) else (canon(sk) == canon(sp) if isinstance(sk, dict) else None)
    ps = r.get('passes') or []; last = ps[-1] if ps else {}
    g['final_pass_is_last'] = r.get('final_pass') == last.get('pass'); g['last_change_km_s'] = last.get('max_abs_change_km_s')
    g['V2'] = bool(isinstance(g['last_change_km_s'], (int, float)) and g['last_change_km_s'] <= crit['tau_picard_km_s'])
    ns = r.get('normalized_spec') or {}; num = ns.get('numerics') or {}; pc = num.get('picard') or {}; tr = num.get('truncation') or {}
    cg, gspec = grid_def(c['grid']); mm = []
    if canon(num.get('composite_grid_spec')) != canon(cg): mm.append('grid')
    if not (tr.get('shape') == c['shape'] and tr.get('kmax_inverse_kpc') == c['kmax_inverse_kpc']): mm.append('truncation')
    if ns.get('galaxy') != 'DDO154': mm.append('galaxy=%r' % ns.get('galaxy'))
    if canon(ns.get('physical')) != canon(anc['physical']): mm.append('physical')
    if canon(ns.get('coefficients')) != canon(anc['coefficients']): mm.append('coefficients')
    if canon(num.get('brackets')) != canon(block): mm.append('brackets')
    if pc.get('speed_change_bound_km_s') != anc['picard']['speed_change_bound_km_s']: mm.append('picard_bound')
    if pc.get('observe_every_pass') != anc['picard']['observe_every_pass']: mm.append('picard_observe')
    npass = pc.get('passes'); g['picard_passes'] = npass
    if npass != anc['picard']['passes']:
        if not (cid == 'C2' and npass == c['bound_call']['picard_passes'] and g['last_change_km_s'] is not None and g['last_change_km_s'] <= anc['picard']['speed_change_bound_km_s']):
            mm.append('picard_passes')
        else: g['C2_picard_equivalence_used'] = True
    drv = SH2.get(r.get('driver_sha256')); g['driver'] = drv
    if drv not in c['drivers_allowed']: mm.append('driver')
    elif drv == 'v005' and not v5.get('admissible'): mm.append('V005_INADMISSIBLE')
    g['V3'] = not mm; g['V3_mismatch'] = mm
    fd = last.get('field'); pk = (json.load(open(fd + '/finish.json')).get('outputs') or {}).get('refreshed_prepared.npz') if fd and os.path.isfile(fd + '/finish.json') else None
    if pk and os.path.isfile(pk['path']) and sha(pk['path']) == pk['sha256']:
        with np.load(pk['path'], allow_pickle=False) as z: k = z['wavevectors'].copy(); w = z['weighted_responses'].copy()
        ax = axis_m(gspec); n = len(ax); uq = [np.unique(k[:, j]) for j in range(3)]
        g['V4'] = bool(len(k) == n ** 3 and all(len(u) == n and np.array_equal(u, ax) for u in uq)); g['axis_nodes'] = n
        g['V4_max_abs_axis_diff_m'] = float(max(np.max(np.abs(u - ax)) for u in uq)) if all(len(u) == n for u in uq) else None
        kk = c['kmax_inverse_kpc'] if c['kmax_inverse_kpc'] is not None else float(gspec['breaks_inverse_kpc'][-1])
        m = mask(k, c['shape'], kk / KPC_M); nz = np.any(w.reshape(len(w), -1) != 0, axis=1)
        gg = np.stack(np.meshgrid(ax, ax, ax, indexing='ij'), -1).reshape(-1, 3); exp_kept = int(np.count_nonzero(mask(gg, c['shape'], kk / KPC_M)))
        g.update(outside_rows_all_zero=bool(not np.any(nz[~m])), nonzero_rows=int(nz.sum()), mask_kept_expected=exp_kept, packet_sha256=pk['sha256'])
        g['V5'] = bool(g['outside_rows_all_zero'] and g['nonzero_rows'] == exp_kept)
        del k, w, gg, nz, m
    else:
        g['V4'] = g['V5'] = False; g['packet'] = 'missing or sha mismatch'
    if c['prefix'].startswith('admit:'):
        cube = c['prefix'].split(':')[1]; ia = (((r.get('identity') or {}).get('route_a') or {}).get('custody') or {}).get('identity_sha256')
        ib = (((json.load(open(cmap[cube])).get('identity') or {}).get('route_a') or {}).get('custody') or {}).get('identity_sha256')
        g['V6'] = bool(ia is not None and ia == ib and r.get('driver_sha256') == json.load(open(cmap[cube])).get('driver_sha256'))
    g['failed'] = [x for x in ('V1', 'V2', 'V3', 'V4', 'V5', 'V6') if x in g and not g[x]]; g['valid_all'] = not g['failed']
    G[cid] = g; print(cid, 'gates', {x: g[x] for x in ('V1', 'V2', 'V3', 'V4', 'V5', 'V6') if x in g}, g['V3_mismatch'], 'passes', npass, 'nz', g.get('nonzero_rows'), '/', g.get('mask_kept_expected'), flush=True)
out['gates'] = G
# ---------------- 3. statistics and decision (prereg order)
V = {cid: {x['id']: x['speed_km_s'] for x in R[cid]['rows']} for cid in CD}
def Dhat(a, b): return max(abs(V[b][i] - V[a][i]) / tau[i] for i in ids)
def D(a, b): return max(abs(V[b][i] - V[a][i]) for i in ids)
KEY = {('cube', 2): 'C2', ('cube', 3): 'C3', ('cube', 4): 'C4', ('sphere', 2): 'S2', ('sphere', 3): 'S3', ('sphere', 4): 'S4',
       ('cylinder', 2): 'Y2', ('cylinder', 3): 'Y3', ('cylinder', 4): 'Y4'}
for (A, K), cid in KEY.items(): assert CD[cid]['shape'] == A and CD[cid]['grid'] == 'G%d' % K
S = {}
for A in ('cube', 'sphere', 'cylinder'):
    d23, d34 = Dhat(KEY[(A, 2)], KEY[(A, 3)]), Dhat(KEY[(A, 3)], KEY[(A, 4)])
    argmax34 = max(ids, key=lambda i: abs(V[KEY[(A, 4)]][i] - V[KEY[(A, 3)]][i]) / tau[i])
    S[A] = {'Dhat_2_3': d23, 'Dhat_3_4': d34, 'q': d34 / d23, 'D_2_3_km_s': D(KEY[(A, 2)], KEY[(A, 3)]), 'D_3_4_km_s': D(KEY[(A, 3)], KEY[(A, 4)]),
            'argmax_row_3_4': argmax34, 'pass': bool(all(G[KEY[(A, K)]]['valid_all'] for K in (2, 3, 4)) and d34 <= 1.0 and d34 <= 0.5 * d23),
            'n_rows_3_4_over_tau': sum(abs(V[KEY[(A, 4)]][i] - V[KEY[(A, 3)]][i]) > tau[i] for i in ids)}
out['sequences'] = S
DR = Dhat('C2', 'R'); out['inner'] = {'Dhat_R': DR, 'D_R_km_s': D('C2', 'R'), 'pass': DR <= 1.0}
bad = sorted(cid for cid in CD if not G[cid]['valid_all'])
if bad: dec = {'outcome': 'INCOMPLETE', 'bad': bad}
elif DR > 1: dec = {'outcome': 'INNER_UNRESOLVED'}
elif not any(S[A]['pass'] for A in S):
    best = min(S, key=lambda A: S[A]['Dhat_3_4']); dec = {'outcome': 'NOT_CONVERGED', 'extend_shape': best}
else: dec = {'outcome': 'SOME_SHAPE_PASSES (rules 4-5 apply)'}
out['decision_own'] = dec
cmpj = json.load(open(PIN['comparison_json'][0])); cd = cmpj['decision']
agree = {'outcome': cd.get('outcome') == dec['outcome'], 'extend_shape': cd.get('extend_shape') == dec.get('extend_shape')}
for A in S:
    for k in ('Dhat_2_3', 'Dhat_3_4'): agree['%s_%s_absdiff' % (A, k)] = abs(cmpj['sequences'][A][k] - S[A][k])
agree['Dhat_R_absdiff'] = abs(cmpj['inner_control']['Dhat_R'] - DR)
agree['gates_equal'] = {cid: (cmpj['gates'][cid]['failed'] == G[cid]['failed']) for cid in CD}
agree['rows_equal'] = all(canon(cmpj['rows_km_s'][cid]) == canon(V[cid]) for cid in CD)
agree['compare_bracket_recovery_sha'] = (cmpj.get('bracket_recovery') or {}).get('sha256') == PIN['recovery_r3'][1]
agree['compare_v005_admissible'] = (cmpj.get('v005_admissibility') or {}).get('admissible')
agree['compare_prereg_sha'] = cmpj['prereg']['sha256'] == PIN['prereg'][1]; agree['compare_script_sha'] = cmpj['script_sha256'] == PIN['compare_script'][1]
agree['compare_test_mode'] = cmpj.get('test_mode'); agree['compare_cases_file_sha'] = cmpj['cases_file']['sha256'] == PIN['cases_r3'][1]
out['agreement_with_sealed_compare'] = agree
out['next_step_prereg_rule3'] = crit['decision_rule'][2]; out['next_step_compare'] = cd.get('next_step')
with open(os.path.join(HERE, 'CHECK_VERDICT_R3_C3V001.json'), 'x') as fh: json.dump(out, fh, indent=1, default=float)
print(json.dumps({k: out[k] for k in ('tau_equals_quarter_sigma', 'cases_file_keys_equal_registered', 'launch_prereg_pin_ok', 'v005_admissibility', 'recovery_block', 'sequences', 'inner', 'decision_own', 'agreement_with_sealed_compare')}, indent=1, default=float))
print('inputs all_ok:', {c: inp[c]['all_ok'] for c in inp})
