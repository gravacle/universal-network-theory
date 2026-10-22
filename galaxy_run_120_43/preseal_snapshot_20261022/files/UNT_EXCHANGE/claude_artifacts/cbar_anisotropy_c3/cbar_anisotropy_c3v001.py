"""C̄ in-plane anisotropy across every available L=4 coefficient estimate (Claude3, dispatch 0487).
Decision rule: PLAN_CBAR_ANISOTROPY_C3V001.md (61266bae), registered before this ran. numpy only; read-only on
every input; writes only CBAR_ANISOTROPY_C3V001.json next to this file (exclusive create). Opens no result.json."""
import hashlib, itertools, json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
UPC = '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13'
SE = UPC + '/CLAUDE2/CRITICAL_PATH_EVALUATION_2026-10-17_V001/sampler_eval'
LWR = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/long_wavelength_response_c2'
PLAN_SHA = '61266baef52fe9e2f5c54a7248d68cb09926acc2d6fccf3cfbeee8623003a4fd'
SRC = {'admission_blocks': (SE + '/admission_blocks.json', None), 'cycle_blocks': (SE + '/cycle_blocks.json', None),
       'v004_blocks': (SE + '/v004_blocks.json', None),
       'worm_blocks': (UPC + '/CLAUDE2/WORM_PILOT_EVALUATION_2026-10-17_V001/out/worm_blocks.json', None),
       'birthk_blocks': (UPC + '/CLAUDE2/BIRTHK_PILOT_EVALUATION_2026-10-17_V001/out/birthk_blocks.json', None),
       'A2_npz': (SE + '/CANDIDATE_4CHAIN_POOLED_GRID_V001.npz', '2e3a36d888ef8a89c9a2b6073ca6123656c31317c995962c11f34d434eca6ff7'),
       'V004_npz': (UPC + '/CODEX1/PROVISIONAL_L4_COEFFICIENT_FREEZE_V001/coefficients.npz', 'fe5a2f065dec8f120c573eeeb6edc0a24a945d2a0fd70e3f29a66cb986e53e4f'),
       'grid_inventory_npz': (LWR + '/out/GRID_INVENTORY_V001.npz', '1833cca4b27edafde5e1d27f511b5bc7843f5447eb4d0faebbdeeb98b790d20d'),
       'chk_e_npz': (LWR + '/check/out/CHK_E_OTHER_RUNS_V001.npz', '153d4ad051e8a0548ad8008c423043c98ab41f977b2950ab2945e92abd84495a'),
       'chk_e_json': (LWR + '/check/out/CHK_E_OTHER_RUNS_V001.json', '381942364adeee722019a0534c915bee5f4779919638d9ad3e55e8ff94a9afea'),
       'plan': (HERE + '/PLAN_CBAR_ANISOTROPY_C3V001.md', PLAN_SHA)}
def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as fh:
        for b in iter(lambda: fh.read(1 << 20), b''): h.update(b)
    return h.hexdigest()
pins = {}
for k, (p, want) in SRC.items():
    h = sha(p)
    if want is not None and h != want: raise SystemExit('PIN MISMATCH ' + k)
    pins[k] = {'path': p, 'sha256': h}
BG = [('background_cell_sum_whitened_R', 0), ('background_cell_sum_whitened_R', 1), ('background_cell_sum_whitened_R', 2),
      ('background_cell_sum_whitened_S', 0, 0), ('background_cell_sum_whitened_S', 1, 1), ('background_cell_sum_whitened_S', 2, 2),
      ('background_cell_sum_whitened_S', 1, 2), ('background_cell_sum_whitened_S', 0, 2), ('background_cell_sum_whitened_S', 0, 1)]
def moments(raw, labels, cells=64):
    labels = [tuple(l) for l in labels]; a = np.asarray(raw, float)[[labels.index(k) for k in BG]] / cells
    mu = a[:3]; M = np.zeros((3, 3))
    for p, (i, j) in enumerate(((0, 0), (1, 1), (2, 2), (1, 2), (0, 2), (0, 1)), 3): M[i, j] = M[j, i] = a[p]
    return M - np.outer(mu, mu)
# ---- 10 chains from the five blocks JSON (own rebuild) ----
raw, labels = {}, {}
for run in ('admission', 'cycle', 'worm', 'birthk', 'v004'):
    d = json.load(open(SRC[run + '_blocks'][0])); labels[run] = d['background']['labels']
    pcm = d['background']['per_chain_means']; assert len(pcm) == 2, run
    for c in (0, 1): raw[(run, c)] = np.asarray(pcm[c], float)
    del d
def C_of(chains):
    run0 = chains[0][0]; assert all(labels[r] == labels[run0] for r, _ in chains)
    return moments(np.mean([raw[c] for c in chains], axis=0), labels[run0])
chainC = {}
for (run, c) in raw: chainC['%s_c%d' % (run, c)] = C_of([(run, c)])
A2C = [('admission', 0), ('admission', 1), ('cycle', 0), ('cycle', 1)]
est = {}
def add(name, C, chains, src, independent=True): est[name] = {'C': np.asarray(C, float), 'chains': chains, 'source': src, 'independent_estimate': independent}
add('A2_pooled', C_of(A2C), ['admission_c0', 'admission_c1', 'cycle_c0', 'cycle_c1'], 'rebuilt from blocks JSON (mean of 4 chain means)')
for r, c in A2C: add('%s_c%d' % (r, c), chainC['%s_c%d' % (r, c)], ['%s_c%d' % (r, c)], 'blocks JSON chain')
add('six_chain', C_of(A2C + [('worm', 0), ('worm', 1)]), ['A2 x4', 'worm_c0', 'worm_c1'], 'rebuilt; overlaps A2', False)
add('eight_chain', C_of(A2C + [('worm', 0), ('worm', 1), ('birthk', 0), ('birthk', 1)]), ['A2 x4', 'worm x2', 'birthk x2'], 'rebuilt; overlaps A2', False)
for r in ('birthk', 'worm'):
    add('%s_pooled' % r, C_of([(r, 0), (r, 1)]), ['%s_c0' % r, '%s_c1' % r], 'rebuilt from blocks JSON')
    for c in (0, 1): add('%s_c%d' % (r, c), chainC['%s_c%d' % (r, c)], ['%s_c%d' % (r, c)], 'blocks JSON chain')
add('V004_pooled', C_of([('v004', 0), ('v004', 1)]), ['v004_c0', 'v004_c1'], 'rebuilt from blocks JSON')
for c in (0, 1): add('v004_c%d' % c, chainC['v004_c%d' % c], ['v004_c%d' % c], 'blocks JSON chain')
val = {}
with np.load(SRC['A2_npz'][0]) as z: val['A2_rebuilt_vs_npz_background_C_max_abs'] = float(np.abs(est['A2_pooled']['C'] - z['background_C']).max())
with np.load(SRC['V004_npz'][0]) as z: val['V004_rebuilt_vs_npz_background_C_max_abs'] = float(np.abs(est['V004_pooled']['C'] - z['background_C']).max())
with np.load(SRC['grid_inventory_npz'][0]) as z:
    val['own_rebuild_vs_GRID_INVENTORY_Cbar_max_abs'] = max(float(np.abs(est[n]['C'] - z[n + '__Cbar']).max()) for n in est)
    val['GRID_INVENTORY_estimates_matched'] = sorted(n for n in est if n + '__Cbar' in z.files)
# ---- 21 CODEX1 estimates from the checker's extraction ----
RUNS = ['OWNED_L4_BIRTH_RESIDENCE_RUN_V001', 'OWNED_L4_CURRENT_GRAPH_BIRTH_RUN_V001', 'OWNED_L4_CURRENT_GRAPH_LONG_RUN_V001',
        'OWNED_L4_ENERGY_TIME_ANCHOR_RUN_V001', 'OWNED_L4_FAMILY_PAIR_ANCHOR_RUN_V001', 'OWNED_L4_HEX_FAMILY_PAIR_ANCHOR_RUN_V002',
        'OWNED_L4_NEAR_ENDPOINT_CAPTURE_RUN_V001']
chkj = json.load(open(SRC['chk_e_json'][0]))
with np.load(SRC['chk_e_npz'][0]) as z:
    Z = {k: z[k].copy() for k in z.files if k.endswith('__C')}
dup = max(float(np.abs(Z['OWNED_L4_RAW_REWEIGHT_CAPTURE_RUN_V001__c%d__C' % c] - chainC['v004_c%d' % c]).max()) for c in (0, 1))
val['RAW_REWEIGHT_chain_C_vs_v004_chain_C_max_abs'] = dup
eigdiff = 0.0
for run in RUNS:
    short = run.replace('OWNED_L4_', '').replace('_RUN', '')
    for e in ('pooled', 'c0', 'c1'):
        C = Z['%s__%s__C' % (run, e)]
        eigdiff = max(eigdiff, float(np.abs(np.linalg.eigvalsh(C) - np.asarray(chkj[run]['estimates'][e]['Cbar_eigs'])).max()))
        add('%s_%s' % (short, e), C, (['%s_c0' % short, '%s_c1' % short] if e == 'pooled' else ['%s_%s' % (short, e)]), 'CHK_E npz (checker extraction)')
        if e != 'pooled': chainC['%s_%s' % (short, e)] = C
val['CHK_E_npz_eigs_vs_CHK_E_json_Cbar_eigs_max_abs'] = eigdiff
# ---- per-estimate table ----
def describe(C):
    B = C[:2, :2]; lo, hi = np.linalg.eigvalsh(B); w, V = np.linalg.eigh(B); maj = V[:, 1]
    th = math.degrees(math.atan2(maj[1], maj[0])) % 180.0
    tr3 = float(np.trace(C) / 3.0)
    return {'C': C.tolist(), 'eigs_full': np.linalg.eigvalsh(C).tolist(), 'inplane_eigs': [float(lo), float(hi)],
            'inplane_anisotropy_q': float((hi - lo) / (hi + lo)), 'major_axis_deg_from_x': th,
            'Cxx': float(C[0, 0]), 'Cyy': float(C[1, 1]), 'Czz': float(C[2, 2]), 'Cxy': float(C[0, 1]), 'Cxz': float(C[0, 2]), 'Cyz': float(C[1, 2]),
            'cubic_group_average_tr_over_3': tr3, 'inplane_D4_average': float((C[0, 0] + C[1, 1]) / 2),
            'rel_traceless_frobenius': float(np.linalg.norm(C - tr3 * np.eye(3)) / tr3)}
table = {n: dict(describe(e['C']), chains=e['chains'], source=e['source'], independent_estimate=e['independent_estimate']) for n, e in est.items()}
# ---- tests ----
rng = np.random.default_rng(20261017)
def s_vec(C): return np.array([C[0, 0] - C[1, 1], 2 * C[0, 1]]) / (C[0, 0] + C[1, 1])
def flip_test(X, N=200000, chunk=20000):
    X = np.asarray(X, float); n = len(X); obs = float(np.sum(X.mean(0) ** 2)); ge = 0
    for _ in range(N // chunk):
        sg = rng.choice((-1.0, 1.0), size=(chunk, n, X.shape[1]))
        ge += int(np.sum(np.sum((sg * X[None]).mean(1) ** 2, axis=1) >= obs - 1e-15))
    return obs, (1 + ge) / (1 + N)
def comp_test(x, N=200000, chunk=20000):
    x = np.asarray(x, float); n = len(x); obs = abs(float(x.mean())); ge = 0
    for _ in range(N // chunk):
        sg = rng.choice((-1.0, 1.0), size=(chunk, n)); ge += int(np.sum(np.abs((sg * x[None]).mean(1)) >= obs - 1e-15))
    return obs, (1 + ge) / (1 + N)
def rayleigh(U):
    n = len(U); Rn = float(np.linalg.norm(U.sum(0))); Rbar = Rn / n
    p = math.exp(math.sqrt(1 + 4 * n + 4 * (n * n - Rn * Rn)) - (1 + 2 * n))  # Zar (1999) approximation
    return Rbar, min(1.0, p)
SP = [np.array(P, float) * np.array(sg, float)[:, None] for P in (np.eye(3)[list(q)] for q in itertools.permutations(range(3)))
      for sg in itertools.product((-1, 1), repeat=3)]
assert len(SP) == 48
def oh_test(Cs, N=100000, chunk=10000):
    T = np.array([[R @ (C / (np.trace(C) / 3)) @ R.T - np.eye(3) for R in SP] for C in Cs])  # (n,48,3,3)
    n = len(Cs); obs = float(np.sum(T[:, 0].mean(0) ** 2)); ge = 0
    for _ in range(N // chunk):
        idx = rng.integers(0, 48, size=(chunk, n)); M = T[np.arange(n)[None, :], idx].mean(1)
        ge += int(np.sum(np.sum(M ** 2, axis=(1, 2)) >= obs - 1e-15))
    return obs, (1 + ge) / (1 + N)
CH = sorted(chainC); RUNOF = {c: c.rsplit('_c', 1)[0] for c in CH}; RUNSET = sorted(set(RUNOF.values()))
def suite(chains):
    S = np.array([s_vec(chainC[c]) for c in chains]); U = S / np.linalg.norm(S, axis=1)[:, None]
    runs = sorted(set(RUNOF[c] for c in chains)); SR = np.array([np.mean([s_vec(chainC[c]) for c in chains if RUNOF[c] == r], axis=0) for r in runs])
    UR = SR / np.linalg.norm(SR, axis=1)[:, None]
    out = {'n_chains': len(chains), 'n_runs': len(runs)}
    out['P_chain_level'] = dict(zip(('stat_mean_s_sq', 'p'), flip_test(S))); out['mean_s_chain'] = S.mean(0).tolist()
    out['A_chain_level_rayleigh'] = dict(zip(('Rbar', 'p'), rayleigh(U))); out['A_chain_level_flip'] = dict(zip(('stat', 'p'), flip_test(U)))
    out['P_run_level'] = dict(zip(('stat_mean_s_sq', 'p'), flip_test(SR))); out['A_run_level_rayleigh'] = dict(zip(('Rbar', 'p'), rayleigh(UR)))
    out['component_Cxx_eq_Cyy'] = dict(zip(('abs_mean', 'p'), comp_test(S[:, 0]))); out['component_Cxy_eq_0'] = dict(zip(('abs_mean', 'p'), comp_test(S[:, 1])))
    out['Oh_full_cubic'] = dict(zip(('stat', 'p'), oh_test([chainC[c] for c in chains])))
    q = np.linalg.norm(S, axis=1)
    out['per_chain_q'] = {'mean': float(q.mean()), 'sd': float(q.std(ddof=1)), 'min': float(q.min()), 'max': float(q.max())}
    out['s_component_sd'] = S.std(0, ddof=1).tolist(); out['expected_abs_mean_s_noise_n4'] = float(np.sqrt(np.sum(S.var(0, ddof=1)) / 4))
    return out
tests = {'all_24_chains': suite(CH), 'excluding_NEAR_ENDPOINT': suite([c for c in CH if not c.startswith('NEAR_ENDPOINT')])}
# within-A2 exact enumeration (component sign flips over its 4 chains: 4^4 = 256 patterns)
SA = np.array([s_vec(chainC[c]) for c in ('admission_c0', 'admission_c1', 'cycle_c0', 'cycle_c1')]); obs = float(np.sum(SA.mean(0) ** 2))
pats = list(itertools.product((-1.0, 1.0), repeat=8)); vals = [float(np.sum((np.array(p).reshape(4, 2) * SA).mean(0) ** 2)) for p in pats]
tests['within_A2_exact'] = {'stat': obs, 'p': sum(v >= obs - 1e-15 for v in vals) / len(vals), 'chain_s': SA.tolist(),
                            'A2_pooled_s': s_vec(est['A2_pooled']['C']).tolist()}
def verdict(t):
    P, A, PR = t['P_chain_level']['p'], max(t['A_chain_level_rayleigh']['p'], t['A_chain_level_flip']['p']), t['P_run_level']['p']
    if P < 0.01 and A < 0.01 and PR < 0.01: return 'anisotropy systematic across estimates'
    if P >= 0.05 and min(t['A_chain_level_rayleigh']['p'], t['A_chain_level_flip']['p']) >= 0.05 and PR >= 0.05: return 'anisotropy consistent with estimator noise'
    return 'INCONCLUSIVE at L=4'
for k in ('all_24_chains', 'excluding_NEAR_ENDPOINT'): tests[k]['verdict_by_registered_rule'] = verdict(tests[k])
spread = {}
for key in ('inplane_eigs',):
    lo = np.array([table[n]['inplane_eigs'][0] for n in table]); hi = np.array([table[n]['inplane_eigs'][1] for n in table])
    q = np.array([table[n]['inplane_anisotropy_q'] for n in table])
    spread = {'n_estimates': len(table), 'lambda_lo': [float(lo.min()), float(lo.max())], 'lambda_hi': [float(hi.min()), float(hi.max())],
              'q_range': [float(q.min()), float(q.max())], 'q_median': float(np.median(q))}
res = {'schema': 'CBAR_ANISOTROPY_C3V001', 'plan_sha256': PLAN_SHA, 'pins': pins, 'validation': val, 'estimates': table,
       'chain_units': CH, 'run_units': RUNSET, 'spread_across_estimates': spread, 'tests': tests,
       'info_only_symmetrized_A2': {'cubic_group_average_tr_over_3': table['A2_pooled']['cubic_group_average_tr_over_3'],
                                    'inplane_D4_average': table['A2_pooled']['inplane_D4_average'], 'note': 'information only; not proposed for adoption (0487)'}}
out = os.path.join(HERE, 'CBAR_ANISOTROPY_C3V001.json')
with open(out, 'x') as fh: json.dump(res, fh, indent=1)
print(json.dumps(val, indent=1)); print(json.dumps(spread))
for n in table: t = table[n]; print('%-28s lo=%.4f hi=%.4f q=%.4f axis=%6.1f  diag=%s  offd=(%.4f,%.4f,%.4f) tr/3=%.4f' % (n, *t['inplane_eigs'], t['inplane_anisotropy_q'], t['major_axis_deg_from_x'], np.round([t['Cxx'], t['Cyy'], t['Czz']], 4).tolist(), t['Cxy'], t['Cxz'], t['Cyz'], t['cubic_group_average_tr_over_3']))
print(json.dumps(tests, indent=1, default=float))
