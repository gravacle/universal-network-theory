"""POST-HOC, descriptive: per-batch C̄ for the four A2 chains (admission, cycle) from their traces files
(8 batch means x 128 samples per chain). Not part of the registered rule. numpy only; writes one JSON (exclusive)."""
import hashlib, json, math, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
SE = '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/CRITICAL_PATH_EVALUATION_2026-10-17_V001/sampler_eval'
BG = [('background_cell_sum_whitened_R', 0), ('background_cell_sum_whitened_R', 1), ('background_cell_sum_whitened_R', 2),
      ('background_cell_sum_whitened_S', 0, 0), ('background_cell_sum_whitened_S', 1, 1), ('background_cell_sum_whitened_S', 2, 2),
      ('background_cell_sum_whitened_S', 1, 2), ('background_cell_sum_whitened_S', 0, 2), ('background_cell_sum_whitened_S', 0, 1)]
def C_from(vec9):
    a = np.asarray(vec9, float) / 64.0; mu = a[:3]; M = np.zeros((3, 3))
    for p, (i, j) in enumerate(((0, 0), (1, 1), (2, 2), (1, 2), (0, 2), (0, 1)), 3): M[i, j] = M[j, i] = a[p]
    return M - np.outer(mu, mu)
out = {'label': 'POST_HOC_DESCRIPTIVE', 'pins': {}, 'chains': {}}
for run in ('admission', 'cycle'):
    tp, bp = SE + '/%s_traces.json' % run, SE + '/%s_blocks.json' % run
    for p in (tp, bp): out['pins'][os.path.basename(p)] = hashlib.sha256(open(p, 'rb').read()).hexdigest()
    tr = json.load(open(tp)); bl = json.load(open(bp))['background']
    lab = {tuple(e['label']): e for e in tr['background']}
    for c in (0, 1):
        B = np.array([lab[k]['chain%d' % c]['batch_means_8x128'] for k in BG]).T          # (8, 9)
        full = np.asarray(bl['per_chain_means'][c], float)[[[tuple(l) for l in bl['labels']].index(k) for k in BG]]
        s1 = []; s2 = []
        for b in range(8):
            Cb = C_from(B[b]); s1.append(float((Cb[0, 0] - Cb[1, 1]) / (Cb[0, 0] + Cb[1, 1]))); s2.append(float(2 * Cb[0, 1] / (Cb[0, 0] + Cb[1, 1])))
        Cf = C_from(full); s1f = float((Cf[0, 0] - Cf[1, 1]) / (Cf[0, 0] + Cf[1, 1]))
        x = np.arange(8.0); slope = float(np.polyfit(x, s1, 1)[0])
        out['chains']['%s_c%d' % (run, c)] = {'batch_mean_avg_minus_chain_mean_max_abs': float(np.abs(B.mean(0) - full).max()),
            's1_per_batch': s1, 's2_per_batch': s2, 's1_full_chain': s1f, 's1_first_half_mean': float(np.mean(s1[:4])),
            's1_last_half_mean': float(np.mean(s1[4:])), 's1_slope_per_batch': slope, 'n_batches_s1_negative': int(sum(v < 0 for v in s1))}
with open(os.path.join(HERE, 'CBAR_BATCH_DRIFT_POSTHOC_C3V001.json'), 'x') as fh: json.dump(out, fh, indent=1)
for k, v in out['chains'].items():
    print('%-13s check=%.1e s1 batches=%s full=%.4f first=%.4f last=%.4f slope=%.4f neg=%d/8' % (k, v['batch_mean_avg_minus_chain_mean_max_abs'], np.round(v['s1_per_batch'], 3).tolist(), v['s1_full_chain'], v['s1_first_half_mean'], v['s1_last_half_mean'], v['s1_slope_per_batch'], v['n_batches_s1_negative']))
