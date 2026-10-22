"""0494 / correction of 0043: residual of the C4R3 ring indicator against Qinf*T_N of the FULL represented source
f_total = fixed stars + latest gas + offset delta (identity total = U*f_total verified). Also the gas-vs-gas comparison of the
two routes (route-B body vs route-A stored gas) along kz and k_perp. Read-only; numpy only; one JSON (x)."""
import hashlib, json, math, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
MA = json.load(open(os.path.join(HERE, 'MASS_ACCOUNTING_C3V001.json'))); P = {k: v['path'] for k, v in MA['pins'].items()}
SH = json.load(open('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/shell_resolved_c4_c3/SHELL_RESOLVED_C4_C3V001.json'))
ST = os.path.dirname(os.path.dirname(os.path.dirname(SH['pins']['final_packet']['path'])))
def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 22), b''): h.update(b)
    return h.hexdigest()
for k in ('old_gas', 'fixed_stars', 'g4', 'unit', 'src_offset'): assert sha(P[k]) == MA['pins'][k]['sha256'], k
fin = SH['pins']['final_packet']['path']; g17p = ST + '/17_le2_feedback/feedback/gas_source_feedback.npz'
pins = {'final_packet': {'path': fin, 'sha256': sha(fin)}, 'gas17': {'path': g17p, 'sha256': sha(g17p)}, 'mass_accounting_json': sha(os.path.join(HERE, 'MASS_ACCOUNTING_C3V001.json'))}
with np.load(P['unit']) as z: k = z['wavevectors'].copy(); dk = z['dk_weights'].copy(); U0 = z['weighted_responses'][:, 0, 0].copy()
with np.load(fin) as z: act = z['weighted_responses'][:, 0, 0].copy()
with np.load(P['src_offset']) as z: body = z['new_body_fourier_J'][:, 0, 0].copy(); delta = z['delta_source_fourier_J'][:, 0, 0].copy()
with np.load(g17p) as z: g17 = z['new_gas_fourier_J'][:, 0, 0].copy()
og = np.load(P['old_gas'])[:, 0, 0]; fs = np.load(P['fixed_stars'])[:, 0, 0]
def rel(a, b): return float(np.max(np.abs(a - b)) / max(np.max(np.abs(a)), 1e-300))
ftot = fs + g17 + delta
ident = {'body_minus_delta_eq_old_gas': rel(og, body - delta), 'total_eq_U_ftot': rel(act, U0 * ftot)}
C = 299792458.0; G = 6.67430e-11; C2 = C * C; KPC = 3.085677581491367e19; QINF = SH['validation']['Qinf']
w = dk / (2 * math.pi) ** 3; kn = np.linalg.norm(k, axis=1); wTN = w * 4 * math.pi * G / (C ** 4 * kn ** 2)
parts = {'actual': act, 'Qinf_N_total': QINF * wTN * ftot, 'Qinf_N_stars': QINF * wTN * fs, 'Qinf_N_gas_plus_offset': QINF * wTN * (g17 + delta)}
parts['residual_vs_full_source'] = act - parts['Qinf_N_total']
ax = np.unique(k[:, 0]); n = len(ax); flat = np.searchsorted(ax, k[:, 0]) * n + np.searchsorted(ax, k[:, 1])
def plane(amp, m): return (np.bincount(flat[m], weights=amp[m].real, minlength=n * n) + 1j * np.bincount(flat[m], weights=amp[m].imag, minlength=n * n)).reshape(n, n)
ids = list(SH['rows']); radii = np.array([SH['rows'][i]['R_kpc'] for i in ids]) * KPC; tau = {i: SH['rows'][i]['tau_km_s'] for i in ids}; v4 = {i: SH['rows'][i]['v_C4_km_s'] for i in ids}
nphi = 32; ph = 2 * np.pi * np.arange(nphi) / nphi
EX = [[(np.exp(1j * ax * R * math.cos(t)), np.exp(1j * ax * R * math.sin(t)), t) for t in ph] for R in radii]
def ring(Pm):
    vals = np.zeros((len(radii), nphi)); gs = np.zeros((len(radii), nphi))
    for i in range(len(radii)):
        for j, (ex, ey, t) in enumerate(EX[i]):
            vals[i, j] = (ex @ Pm @ ey).real; gs[i, j] = ((1j * ax * ex) @ Pm @ ey * math.cos(t) + ex @ Pm @ (1j * ax * ey) * math.sin(t)).real
    return vals, gs
vA, _ = ring(plane(act, np.ones(len(k), bool))); den = 1 + vA
def dvt(amp, m):
    _, gs = ring(plane(amp, m)); g0 = C2 * np.mean(gs / den, axis=1)
    return [float(radii[a] * g0[a] / (2 * v4[i] * 1e3) / 1e3 / tau[i]) for a, i in enumerate(ids)]
kz = np.abs(k[:, 2]) * KPC; kp = np.maximum(np.abs(k[:, 0]), np.abs(k[:, 1])) * KPC; c34 = np.maximum(kp, kz)
regions = {'cube34_P_inplane_only': (kp > 3) & (kp <= 4) & (kz <= 3), 'cube34_V_kz_only': (kz > 3) & (kz <= 4) & (kp <= 3), 'cube34_all': (c34 > 3) & (c34 <= 4),
           'vslab_2_3': (kz > 2) & (kz <= 3), 'vslab_3_4': (kz > 3) & (kz <= 4), 'all_k': np.ones(len(k), bool)}
ring_parts = {rg: {pn: dvt(pa, m) for pn, pa in parts.items()} for rg, m in regions.items()}
# gas vs gas: route-B body vs route-A stored gas, along kz (min kperp) and kperp (min |kz|)
amin = ax[ax > 0].min(); kperp = np.hypot(k[:, 0], k[:, 1]) * KPC
lz = (np.abs(k[:, 0]) == amin) & (np.abs(k[:, 1]) == amin); lp = np.abs(k[:, 2]) == amin
gg = {'along_kz_at_min_kperp': sorted({round(float(a), 3): float((b).real) for a, b in zip(kz[lz], (body / og)[lz])}.items())[::8],
      'along_kperp_at_min_kz_binned': {}}
for lo, hi in ((0, 1), (1, 2), (2, 3), (3, 4), (4, 6)):
    m = lp & (kperp >= lo) & (kperp < hi) & (np.abs(og) > 1e-3 * np.max(np.abs(og)))
    rr = (body / og)[m].real; gg['along_kperp_at_min_kz_binned']['%d-%d' % (lo, hi)] = {'n': int(m.sum()), 'median': float(np.median(rr)), 'q10_q90': np.quantile(rr, [0.1, 0.9]).tolist()}
gg['offset_delta_k0_Msun'] = MA['k0_masses_Msun']['offset_delta']
out = {'schema': 'CORRECTED_SPLIT_C3V001', 'pins': pins, 'identities_rel_err': ident, 'rows': ids, 'ring_dv_over_tau': ring_parts, 'gas_body_over_routeA_gas': gg}
with open(os.path.join(HERE, 'CORRECTED_SPLIT_C3V001.json'), 'x') as fh: json.dump(out, fh, indent=1)
print(json.dumps(ident)); hdr = ' '.join('%6s' % i[-2:] for i in ids)
for rg, d in ring_parts.items():
    print('== %s %s' % (rg, hdr))
    for pn in ('actual', 'Qinf_N_total', 'Qinf_N_stars', 'Qinf_N_gas_plus_offset', 'residual_vs_full_source'): print('   %-24s' % pn, ' '.join('%+6.2f' % x for x in d[pn]))
print(json.dumps(gg, indent=1)[:2500])
