"""POST-HOC robustness for CBAR_ANISOTROPY_C3V001 (not part of the registered verdict rule 61266bae).
Reads only CBAR_ANISOTROPY_C3V001.json (pinned) and the main script's functions are re-implemented here. numpy only."""
import hashlib, json, math, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); P = os.path.join(HERE, 'CBAR_ANISOTROPY_C3V001.json')
WANT = '6a183a1f7bc601b9167d75771e464b290b0b86b80c66105835dee64191ec620e'
if hashlib.sha256(open(P, 'rb').read()).hexdigest() != WANT: raise SystemExit('main result pin mismatch')
d = json.load(open(P)); E = d['estimates']; CH = d['chain_units']
C = {c: np.array(E[c]['C']) for c in CH}; RUNOF = {c: c.rsplit('_c', 1)[0] for c in CH}
def s_vec(M): return np.array([M[0, 0] - M[1, 1], 2 * M[0, 1]]) / (M[0, 0] + M[1, 1])
rng = np.random.default_rng(20261018)
def flip(X, N=200000, chunk=20000):
    X = np.asarray(X, float); n = len(X); obs = float(np.sum(X.mean(0) ** 2)); ge = 0
    for _ in range(N // chunk):
        sg = rng.choice((-1.0, 1.0), size=(chunk, n, X.shape[1])); ge += int(np.sum(np.sum((sg * X[None]).mean(1) ** 2, axis=1) >= obs - 1e-15))
    return {'stat': obs, 'p': (1 + ge) / (1 + N)}
def rayleigh(U):
    n = len(U); Rn = float(np.linalg.norm(U.sum(0))); return {'Rbar': Rn / n, 'p': min(1.0, math.exp(math.sqrt(1 + 4 * n + 4 * (n * n - Rn * Rn)) - (1 + 2 * n)))}
def binom2(k, n):
    tail = sum(math.comb(n, j) for j in range(max(k, n - k), n + 1)) / 2 ** n; return min(1.0, 2 * tail)
def suite(chains):
    S = np.array([s_vec(C[c]) for c in chains]); U = S / np.linalg.norm(S, axis=1)[:, None]
    runs = sorted(set(RUNOF[c] for c in chains)); SR = np.array([np.mean([s_vec(C[c]) for c in chains if RUNOF[c] == r], 0) for r in runs])
    neg_c = int(np.sum(S[:, 0] < 0)); neg_r = int(np.sum(SR[:, 0] < 0))
    return {'n_chains': len(chains), 'n_runs': len(runs), 'P_chain': flip(S), 'P_run': flip(SR), 'A_chain_rayleigh': rayleigh(U),
            'A_chain_flip': flip(U), 'sign_test_chain_Cxx_lt_Cyy': {'k': neg_c, 'n': len(chains), 'p_two_sided': binom2(neg_c, len(chains))},
            'sign_test_run_Cxx_lt_Cyy': {'k': neg_r, 'n': len(runs), 'p_two_sided': binom2(neg_r, len(runs))},
            'mean_s1_run': float(SR[:, 0].mean()), 'se_s1_run': float(SR[:, 0].std(ddof=1) / math.sqrt(len(runs)))}
out = {'label': 'POST_HOC_NOT_PART_OF_REGISTERED_RULE', 'main_result_sha256': WANT}
out['all_24'] = suite(CH)
out['excl_V004'] = suite([c for c in CH if not c.startswith('v004')])
out['excl_V004_and_NEAR_ENDPOINT'] = suite([c for c in CH if not c.startswith('v004') and not c.startswith('NEAR_ENDPOINT')])
runs = sorted(set(RUNOF.values())); per_run = {}
dif = []
for r in runs:
    cs = [c for c in CH if RUNOF[c] == r]; s = [s_vec(C[c]) for c in cs]; dif.append(s[0] - s[1])
    diag = np.mean([np.diag(C[c]) for c in cs], 0)
    per_run[r] = {'q_chains': [float(np.linalg.norm(v)) for v in s], 'axis_deg_chains': [E[c]['major_axis_deg_from_x'] for c in cs],
                  'mean_diag_xyz': diag.tolist(), 'largest_diag_axis': 'xyz'[int(np.argmax(diag))]}
dif = np.array(dif); sw = dif.std(0, ddof=1) / math.sqrt(2)
a2 = s_vec(np.array(E['A2_pooled']['C']))
out['per_run'] = per_run
out['largest_diag_axis_counts'] = {a: sum(1 for r in per_run.values() if r['largest_diag_axis'] == a) for a in 'xyz'}
out['within_run_noise_sd_per_chain_s'] = sw.tolist()
out['A2_pooled_s'] = a2.tolist(); out['A2_s1_z_vs_within_run_noise_4chain_mean'] = float(a2[0] / (sw[0] / 2))
sR = np.array([np.mean([s_vec(C[c]) for c in CH if RUNOF[c] == r], 0) for r in runs])
out['across_run_sd_of_run_mean_s'] = sR.std(0, ddof=1).tolist()
with open(os.path.join(HERE, 'CBAR_ANISOTROPY_POSTHOC_C3V001.json'), 'x') as fh: json.dump(out, fh, indent=1)
for k in ('all_24', 'excl_V004', 'excl_V004_and_NEAR_ENDPOINT'):
    t = out[k]; print(k, 'P_chain p=%.2g P_run p=%.2g A_rayl p=%.2g A_flip p=%.2g sign_chain %d/%d p=%.3g sign_run %d/%d p=%.3g mean_s1_run=%.4f+-%.4f' % (
        t['P_chain']['p'], t['P_run']['p'], t['A_chain_rayleigh']['p'], t['A_chain_flip']['p'], t['sign_test_chain_Cxx_lt_Cyy']['k'], t['n_chains'],
        t['sign_test_chain_Cxx_lt_Cyy']['p_two_sided'], t['sign_test_run_Cxx_lt_Cyy']['k'], t['n_runs'], t['sign_test_run_Cxx_lt_Cyy']['p_two_sided'], t['mean_s1_run'], t['se_s1_run']))
print('largest diag axis per run:', out['largest_diag_axis_counts']); print('within-run noise sd per chain (s1, s2):', sw.round(4).tolist(), ' across-run sd of run means:', np.round(out['across_run_sd_of_run_mean_s'], 4).tolist())
print('A2 pooled s:', a2.round(4).tolist(), ' z(s1) vs within-run noise for a 4-chain mean: %.2f' % out['A2_s1_z_vs_within_run_noise_4chain_mean'])
for r, v in per_run.items(): print('%-28s q=%s axis=%s diag=%s largest=%s' % (r, np.round(v['q_chains'], 4).tolist(), np.round(v['axis_deg_chains'], 1).tolist(), np.round(v['mean_diag_xyz'], 3).tolist(), v['largest_diag_axis']))
