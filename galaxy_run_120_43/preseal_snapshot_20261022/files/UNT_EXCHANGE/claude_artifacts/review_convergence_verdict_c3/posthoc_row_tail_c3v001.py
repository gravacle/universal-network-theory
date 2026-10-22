"""POST HOC diagnostic (prereg tail_diagnostic semantics: reported, never adopted). Per-row contraction q_i = |d34_i|/|d23_i|
from the 10 R3 result.json rows; and a naive geometric projection of each row to (4,5) and (5,6). Not part of the check verdict."""
import hashlib, json, os
HERE = os.path.dirname(os.path.abspath(__file__)); P = os.path.join(HERE, 'CHECK_VERDICT_R3_C3V001.json')
if hashlib.sha256(open(P, 'rb').read()).hexdigest() != '86ca602c0b1c8e995d826bae1f285c1c5d7c7698c90d8a7699e546e56e267aef': raise SystemExit('pin')
pre = json.load(open('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/kmax_prereg_v005_c2/KMAX_MATRIX_PREREG_V005.json'))
cm = json.load(open('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/kmax_prereg_v005_c2/verdict_r3/CASES_R3.json'))
ids = pre['row_ids']; tau = dict(zip(ids, pre['tau_km_s']))
V = {c: {x['id']: x['speed_km_s'] for x in json.load(open(p))['rows']} for c, p in cm.items()}
out = {'label': 'POST_HOC_DIAGNOSTIC_NEVER_ADOPTED', 'check_json_sha256': '86ca602c0b1c8e995d826bae1f285c1c5d7c7698c90d8a7699e546e56e267aef', 'shapes': {}}
for A, (a, b, c) in {'cube': ('C2', 'C3', 'C4'), 'sphere': ('S2', 'S3', 'S4'), 'cylinder': ('Y2', 'Y3', 'Y4')}.items():
    rows = {}
    for i in ids:
        d23, d34 = V[b][i] - V[a][i], V[c][i] - V[b][i]; q = abs(d34) / abs(d23) if d23 else None
        rows[i] = {'d23_over_tau': d23 / tau[i], 'd34_over_tau': d34 / tau[i], 'q_i': q, 'same_sign': (d23 > 0) == (d34 > 0),
                   'proj_45_over_tau': (abs(d34) * q / tau[i]) if q is not None else None, 'proj_56_over_tau': (abs(d34) * q * q / tau[i]) if q is not None else None}
    qs = [r['q_i'] for r in rows.values() if r['q_i'] is not None]
    out['shapes'][A] = {'rows': rows, 'n_rows_q_gt_0p5': sum(q > 0.5 for q in qs), 'n_rows_q_ge_0p9': sum(q >= 0.9 for q in qs), 'n_rows_non_contracting_q_ge_1': sum(q >= 1 for q in qs),
                        'max_proj_45_over_tau': max(r['proj_45_over_tau'] for r in rows.values()), 'max_proj_56_over_tau': max(r['proj_56_over_tau'] for r in rows.values())}
with open(os.path.join(HERE, 'POSTHOC_ROW_TAIL_C3V001.json'), 'x') as fh: json.dump(out, fh, indent=1)
for A, s in out['shapes'].items():
    print(A, 'q>0.5: %d  q>=0.9: %d  q>=1: %d  naive max proj Dhat(4,5)=%.2f (5,6)=%.2f' % (s['n_rows_q_gt_0p5'], s['n_rows_q_ge_0p9'], s['n_rows_non_contracting_q_ge_1'], s['max_proj_45_over_tau'], s['max_proj_56_over_tau']))
    print('   ', ' '.join('%s:q=%.2f(d34/tau=%+.1f)' % (i[-2:], r['q_i'], r['d34_over_tau']) for i, r in s['rows'].items()))
