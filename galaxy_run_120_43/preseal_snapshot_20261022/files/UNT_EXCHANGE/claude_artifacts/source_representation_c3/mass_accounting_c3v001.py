"""0494 step 1-2: total masses (k->0 limit and direct sums) of every DDO154 source representation at the A2 F10 anchor
(C4 V005 prefix + C4R3), and of the registered mass model. Read-only; numpy only; target-free; writes one JSON (x)."""
import hashlib, json, math, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
UPC = '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13'
PRE = UPC + '/CLAUDE2/runs/KMAX_A2F10_C4_V005_RUN_V001'; R3 = UPC + '/CLAUDE2/runs/KMAX_A2F10_C4R3_D7R3_RUN_V001'
CK = PRE + '/stages/01_route_a/checkpoint'
F = {'ref': UPC + '/CODEX1/GALAXY_RADIAL_SOURCE_REFERENCE_V001.json', 'old_gas': CK + '/blobs/1a8b5b819e7df9f1618aa70e0868c6fbbaf0b60f4efae2562a97beb5d9bdc96a.npy',
     'fixed_stars': CK + '/blobs/9185b69daebbf99e37d940e3040e0add20f76d5a48fc212b9096d1988cc12380.npy', 'g4': CK + '/blobs/2505e12ce30c4805d6d809102e33df7747ef6a0a402a3897e69a6c9258cdbe06.npy',
     'body_arrays': PRE + '/stages/03_body/body/body_arrays.npz', 'body_cfg': PRE + '/inputs/galaxy_config_body.json',
     'unit': R3 + '/stages/01_offset/offset/unit_response.npz', 'src_offset': R3 + '/stages/01_offset/offset/source_offset.npz'}
def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 22), b''): h.update(b)
    return h.hexdigest()
pins = {k: {'path': p, 'sha256': sha(p)} for k, p in F.items()}
for k in ('old_gas', 'fixed_stars', 'g4'): assert pins[k]['sha256'] == os.path.basename(F[k])[:-4], k
C = 299792458.0; MSUN = 1.98847e30; KPC = 3.085677581491367e19
out = {'schema': 'MASS_ACCOUNTING_C3V001', 'pins': pins}
# ---- registered reference model (target-free)
ref = json.load(open(F['ref'])); d = ref['galaxies']['DDO154']; out['ref_keys'] = {k: (list(v.keys()) if isinstance(v, dict) else str(v)[:120]) for k, v in d.items()}
gas = d['HI_plus_He']; st = d['stellar_reference']
e = [float(x) for x in gas['s_edges_kpc2']]; m = [float(x) for x in gas['annular_means_Msun_pc2']]
M_gas_ref = sum(mm * math.pi * (b - a) * 1e6 for a, b, mm in zip(e, e[1:], m))
rad = [float(x) for x in st['radius_kpc']]; sig = [float(x) for x in st['surface_density_Msun_pc2']]; rd = float(st['outer_scale_kpc'])
out['ref_meta'] = {k: v for k, v in d.items() if not isinstance(v, (dict, list))}
out['ref_gas_meta'] = {k: v for k, v in gas.items() if not isinstance(v, list)}; out['ref_star_meta'] = {k: v for k, v in st.items() if not isinstance(v, list)}
out['ref_gas_mass_Msun_annular_sum'] = M_gas_ref
# ---- route-A stored sources and G4 effective source at the smallest |k|
with np.load(F['unit']) as z: k = z['wavevectors'].copy(); U0 = z['weighted_responses'][:, 0, 0].copy()
og = np.load(F['old_gas'])[:, 0, 0]; fs = np.load(F['fixed_stars'])[:, 0, 0]; g4 = np.load(F['g4'])[:, 0, 0]
with np.load(F['src_offset']) as z: body = z['new_body_fourier_J'][:, 0, 0].copy(); delta = z['delta_source_fourier_J'][:, 0, 0].copy()
kn = np.linalg.norm(k, axis=1); i0 = int(np.argmin(kn)); s = g4 / U0
def Msun(fJ): return float(-(fJ.real) / C ** 2 / MSUN)
out['k_min_inverse_kpc'] = float(kn[i0] * KPC)
out['k0_masses_Msun'] = {'routeA_old_gas': Msun(og[i0]), 'routeA_fixed_stars': Msun(fs[i0]), 'routeA_old_gas_plus_stars': Msun(og[i0] + fs[i0]),
                         'routeA_G4_effective_source_s': Msun(s[i0]), 'routeB_new_body': Msun(body[i0]), 'offset_delta': Msun(delta[i0]), 'body_minus_delta_fG4': Msun(body[i0] - delta[i0])}
out['k0_ratios'] = {'s_over_oldgas_plus_stars': float((s[i0] / (og[i0] + fs[i0])).real), 's_over_body_minus_delta': float((s[i0] / (body[i0] - delta[i0])).real),
                    'body_minus_delta_over_oldgas_plus_stars': float(((body[i0] - delta[i0]) / (og[i0] + fs[i0])).real), 'body_over_oldgas_plus_stars': float((body[i0] / (og[i0] + fs[i0])).real)}
# is G4 the response to (old_gas + fixed_stars) at all k?
r = s / (og + fs); big = np.abs(og + fs) > 1e-3 * np.max(np.abs(og + fs))
out['s_over_routeA_stored_all_k'] = {'median': float(np.median(r[big].real)), 'q01_q99': np.quantile(r[big].real, [0.01, 0.99]).tolist()}
r2 = (body - delta) / (og + fs)
out['fG4_over_routeA_stored_all_k'] = {'median': float(np.median(r2[big].real)), 'q01_q99': np.quantile(r2[big].real, [0.01, 0.99]).tolist(), 'max_abs_rel_diff': float(np.max(np.abs((body - delta) - (og + fs))) / np.max(np.abs(og + fs)))}
# ---- route-B body arrays: direct sums
with np.load(F['body_arrays']) as z:
    Sig = z['Sigma_kg_m2'].copy(); Rn = z['radial_nodes_m'].copy(); RdR = z['radial_RdR_weights_m2'].copy(); J = z['base_integrated_source_J'][..., 0, 0].copy(); rho0 = z['rho0'].copy(); vw = z['volume_weights_m3'].copy()
out['body_direct'] = {'gas_mass_2pi_Sigma_RdR_Msun': float(2 * math.pi * np.sum(Sig * RdR) / MSUN), 'base_integrated_source_mass_Msun': float(-np.sum(J) / C ** 2 / MSUN),
                      'rho0_volume_mass_Msun': float(np.sum(rho0 * vw) / MSUN), 'radial_nodes_kpc_range': [float(Rn.min() / KPC), float(Rn.max() / KPC)], 'n_radial': int(len(Rn))}
cfg = json.load(open(F['body_cfg'])); out['body_cfg_excerpt'] = json.dumps(cfg)[:1500]
with open(os.path.join(HERE, 'MASS_ACCOUNTING_C3V001.json'), 'x') as fh: json.dump(out, fh, indent=1, default=str)
print(json.dumps({k: out[k] for k in ('ref_meta', 'ref_gas_meta', 'ref_star_meta', 'ref_gas_mass_Msun_annular_sum', 'k_min_inverse_kpc', 'k0_masses_Msun', 'k0_ratios', 's_over_routeA_stored_all_k', 'fG4_over_routeA_stored_all_k', 'body_direct')}, indent=1, default=str))
print('body cfg:', out['body_cfg_excerpt'][:1200])
