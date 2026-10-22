"""Shell-resolved high-k contribution to the 12 DDO154 rows on the C4R3 (G4 cube, K=4) final field packet (Claude3, 0491).
Gravity-only ring indicator (the compare's definition: g_R = c^2 dR(dN)/(1+dN), midplane, 32 azimuths, m=0), split exactly by
|k| shells and by max-norm (cube) shells: each shell's dN gradient over the FULL field's (1+dN). Newtonian reference: the same
ring machinery on Qinf * T_N(k) * f0(k) * dk/(2pi)^3 with the represented total source f0 (body - body gas + latest gas,
component 0) from the run's own stage files. Read-only; numpy only; writes one JSON (exclusive). Does not open uv_tail_study_c2."""
import hashlib, json, math, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
RUN = '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs/KMAX_A2F10_C4R3_D7R3_RUN_V001'
ST = RUN + '/stages'
F = {'final_packet': ST + '/17_le2_feedback/feedback/refreshed_prepared.npz', 'unit_response': ST + '/01_offset/offset/unit_response.npz',
     'source_offset': ST + '/01_offset/offset/source_offset.npz', 'gas07': ST + '/07_fs_feedback/feedback/gas_source_feedback.npz',
     'gas13': ST + '/13_le1_feedback/feedback/gas_source_feedback.npz', 'gas17': ST + '/17_le2_feedback/feedback/gas_source_feedback.npz',
     'result': RUN + '/result.json', 'prereg': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/kmax_prereg_v005_c2/KMAX_MATRIX_PREREG_V005.json',
     'compare': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/kmax_prereg_v005_c2/verdict_r3/COMPARE_R3_V001/KMAX_COMPARISON.json',
     'C3_result': RUN.replace('C4R3', 'C3R3') + '/result.json'}
WANT = {'prereg': 'dbddc02c4d793b44a12136fc4fc88b20c001865ddd4c89b1b70c57bc406bb174', 'compare': '4ea21d902cfb4e8cd3b5aa61d29b8c3bbc05cab9a56c49f3af2913c32ae66433'}
def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 22), b''): h.update(b)
    return h.hexdigest()
pins = {k: {'path': p, 'sha256': sha(p)} for k, p in F.items()}
for k, w in WANT.items():
    if pins[k]['sha256'] != w: raise SystemExit('PIN ' + k)
res = json.load(open(F['result'])); fin17 = json.load(open(ST + '/17_le2_feedback/feedback/finish.json'))
assert res['passes'][-1]['field'] == ST + '/17_le2_feedback/feedback' and fin17['outputs']['refreshed_prepared.npz']['sha256'] == pins['final_packet']['sha256']
pre = json.load(open(F['prereg'])); ids = pre['row_ids']; tau = dict(zip(ids, pre['tau_km_s']))
rb = pre['binding_inputs']['row_binding']; assert sha(rb['path']) == rb['sha256']
qrows = json.load(open(rb['path']))['query_rows']; assert [q['id'] for q in qrows] == ids; radii = np.array([q['radius_m'] for q in qrows])
v4 = {x['id']: x['speed_km_s'] for x in res['rows']}; v3 = {x['id']: x['speed_km_s'] for x in json.load(open(F['C3_result']))['rows']}
C = 299792458.0; G = 6.67430e-11; C2 = C * C; KPC = 3.085677581491367e19
GAMMA_EFF = 2.9863917119177204e41; QINF = C ** 4 / (16 * math.pi * G * GAMMA_EFF)
with np.load(F['final_packet']) as z: k = z['wavevectors'].copy(); x0 = z['weighted_responses'][:, 0, 0].copy()
with np.load(F['unit_response']) as z: assert np.array_equal(z['wavevectors'], k); dk = z['dk_weights'].copy()
with np.load(F['source_offset']) as z: body0 = z['new_body_fourier_J'][:, 0, 0].copy()
with np.load(F['gas07']) as z: oldgas0 = z['old_body_gas_fourier_J'][:, 0, 0].copy(); g07 = z['new_gas_fourier_J'][:, 0, 0].copy()
with np.load(F['gas13']) as z: p13 = z['previous_current_gas_fourier_J'][:, 0, 0].copy(); g13 = z['new_gas_fourier_J'][:, 0, 0].copy()
with np.load(F['gas17']) as z: p17 = z['previous_current_gas_fourier_J'][:, 0, 0].copy(); g17 = z['new_gas_fourier_J'][:, 0, 0].copy(); d17 = z['delta_gas_fourier_J'][:, 0, 0].copy()
chain = {'prev13_eq_new07': bool(np.array_equal(p13, g07)), 'prev17_eq_new13': bool(np.array_equal(p17, g13)), 'delta17_eq_new17_minus_prev17_maxabs': float(np.max(np.abs(d17 - (g17 - p17))))}
f0 = body0 - oldgas0 + g17
w = dk / (2 * math.pi) ** 3; kn = np.sqrt(np.sum(k * k, axis=1)); knk = kn * KPC
TN = 4 * math.pi * G / (C ** 4 * kn ** 2); nN = w * TN * f0          # Newtonian weighted lapse amplitude of the represented source
# ---- per-node / per-shell symbol check: actual lapse over Newtonian of the same source
sph = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 7)]
mx = np.max(np.abs(k), axis=1) * KPC
cub = [(0, 1), (1, 2), (2, 3), (3, 4)]
def in_sh(lo, hi, arr): return (arr >= lo) & (arr < hi) if hi < 7 else (arr >= lo)
symb = {}
for lo, hi in sph:
    m = in_sh(lo, hi, knk); a, n = x0[m], nN[m]
    big = np.abs(n) >= np.quantile(np.abs(n), 0.5)
    ls = complex(np.vdot(n, a) / np.vdot(n, n))
    symb['%g-%g' % (lo, hi)] = {'n_nodes': int(m.sum()), 'ls_ratio_actual_over_newton': [ls.real, ls.imag], 'ls_over_Qinf': ls.real / QINF,
                                'median_ratio_top_half': float(np.median((a[big] / n[big]).real)), 'q25_q75': np.quantile((a[big] / n[big]).real, [0.25, 0.75]).tolist()}
# ---- ring decomposition (separable: midplane points, sum over kz first)
ax = np.unique(k[:, 0]); assert np.array_equal(ax, np.unique(k[:, 1])); n = len(ax)
ia = np.searchsorted(ax, k[:, 0]); ib = np.searchsorted(ax, k[:, 1]); flat = ia * n + ib
def plane(amp, m):
    re = np.bincount(flat[m], weights=amp[m].real, minlength=n * n); im = np.bincount(flat[m], weights=amp[m].imag, minlength=n * n)
    return (re + 1j * im).reshape(n, n)
shells = [('sph_%g-%g' % s, in_sh(s[0], s[1], knk)) for s in sph] + [('cub_%g-%g' % s, (mx > s[0]) & (mx <= s[1])) for s in cub]
allm = np.ones(len(k), bool)
PA = {nm: plane(x0, m) for nm, m in shells}; PA['all'] = plane(x0, allm)
PN = {nm: plane(nN * QINF, m) for nm, m in shells}; PN['all'] = plane(nN * QINF, allm)
nphi = 32; ph = 2 * np.pi * np.arange(nphi) / nphi
def ring(P, denom=None):
    g0 = np.zeros(len(radii)); vals = np.zeros((len(radii), nphi))
    gs = np.zeros((len(radii), nphi))
    for i, R in enumerate(radii):
        for j, t in enumerate(ph):
            ex = np.exp(1j * ax * R * math.cos(t)); ey = np.exp(1j * ax * R * math.sin(t))
            val = ex @ P @ ey; gx = (1j * ax * ex) @ P @ ey; gy = ex @ P @ (1j * ax * ey)
            vals[i, j] = val.real; gs[i, j] = (gx * math.cos(t) + gy * math.sin(t)).real
    return vals, gs
vA, gA = ring(PA['all']); den = 1 + vA
def g0_of(P): _, gs = ring(P); return C2 * np.mean(gs / den, axis=1)
G0A = {nm: g0_of(P) for nm, P in PA.items()}; G0N = {nm: g0_of(P) for nm, P in PN.items()}
cmpj = json.load(open(F['compare'])); fdC4 = [r['g0_m_s2'] for r in cmpj['field_diagnostic']['C4']['rows']]
val = {'g0_all_vs_compare_ring_C4_max_rel': float(np.max(np.abs(G0A['all'] - np.array(fdC4)) / np.abs(np.array(fdC4)))),
       'sum_sph_shells_vs_all_max_rel': float(np.max(np.abs(sum(G0A[nm] for nm, _ in shells[:5]) - G0A['all']) / np.abs(G0A['all']))),
       'sum_cub_shells_vs_all_max_rel': float(np.max(np.abs(sum(G0A[nm] for nm, _ in shells[5:]) - G0A['all']) / np.abs(G0A['all']))),
       'max_imag_over_real_dN': None, 'source_chain': chain, 'Qinf': QINF}
rows = {}
for i, rid in enumerate(ids):
    R = radii[i]; vr = v4[rid] * 1e3
    def dv(g): return R * g / (2 * vr) / 1e3     # linearized share of the row speed, km/s
    e = {'R_kpc': R / KPC, 'v_C4_km_s': v4[rid], 'd34_observed_km_s': v4[rid] - v3[rid], 'tau_km_s': tau[rid]}
    for nm, _ in shells:
        e[nm] = {'g0_actual_m_s2': float(G0A[nm][i]), 'dv_actual_km_s': float(dv(G0A[nm][i])), 'dv_over_tau': float(dv(G0A[nm][i]) / tau[rid]),
                 'g0_Qinf_newton_m_s2': float(G0N[nm][i]), 'ratio_actual_over_Qinf_newton': float(G0A[nm][i] / G0N[nm][i]) if G0N[nm][i] != 0 else None}
    sq = [abs(e['sph_%g-%g' % s]['dv_actual_km_s']) for s in sph[:4]]
    e['sph_decay_ratios_12_23_34'] = [sq[1] / sq[0], sq[2] / sq[1], sq[3] / sq[2]]
    e['sph_monotone_decay'] = bool(sq[0] > sq[1] > sq[2] > sq[3])
    e['shell34_over_tau'] = e['sph_3-4']['dv_over_tau']; e['cub34_over_tau'] = e['cub_3-4']['dv_over_tau']
    e['cub34_dv_over_observed_d34'] = e['cub_3-4']['dv_actual_km_s'] / e['d34_observed_km_s']
    rows[rid] = e
out = {'schema': 'SHELL_RESOLVED_C4_C3V001', 'pins': pins, 'validation': val, 'symbol_check_per_sph_shell': symb, 'rows': rows,
       'constants': {'c': C, 'G': G, 'kpc_m': KPC, 'gamma_eff': GAMMA_EFF}, 'scope': 'gravity-only ring indicator at fixed final field; linear shell split; diagnostic, no launch'}
with open(os.path.join(HERE, 'SHELL_RESOLVED_C4_C3V001.json'), 'x') as fh: json.dump(out, fh, indent=1)
print(json.dumps(val, indent=1)); print(json.dumps(symb, indent=1))
print('row    R    v4    d34obs | dv/tau per sph shell [0-1 1-2 2-3 3-4 >4] | cub(3,4] dv/tau | ratio to Qinf*Newton [1-2 2-3 3-4 >4] | decay 12,23,34')
for rid, e in rows.items():
    print('%s %5.2f %6.2f %+6.3f | %s | %+7.2f | %s | %s' % (rid[-2:], e['R_kpc'], e['v_C4_km_s'], e['d34_observed_km_s'],
          ' '.join('%+8.2f' % e['sph_%g-%g' % s]['dv_over_tau'] for s in sph), e['cub34_over_tau'],
          ' '.join('%6.3f' % e['sph_%g-%g' % s]['ratio_actual_over_Qinf_newton'] for s in sph[1:]), ' '.join('%.2f' % x for x in e['sph_decay_ratios_12_23_34'])))
