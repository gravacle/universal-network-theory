"""qinf_dependence_c2: how the short-wavelength lapse symbol Q(k)=T(k) k^2 c^4/(4 pi G) depends on the
calibration coordinates (s, gamma/Eref, ell_F) and on the coefficient grid. SYMBOL EVALUATIONS ONLY:
no route-A/forward run, no velocities, no targets, no result.json of KMAX_/D7R/V005-V008/DECIDING runs.

Evaluators (both from long_wavelength_response_c2/tools/lwr_common_v001.py, which loads the NGC run's
IDENTITY-pinned cardinal / complex-binding v002 / static-EH v002 modules by sha256):
  T_module : pinned modules node by node (reference)
  Binder.T_vec : batched transcription, validated here against T_module and against the audit's
                 T1_symbol_Q.npz (lapse_integration_audit_c2/m0_and_box) at the anchor.
Qinf definition = audit T5 (t5_isolated_continuum_kernel_v001.py L23): median of Q over cube nodes 1<=|k|<2 /kpc.
Analytic large-k limit: Qinf_pred = -[pinv(E_hat)]_nn * c^4/(4 pi G gamma_eff), E_hat = static EH density
kernel per (gamma k^2) (static v002 L168-206); gamma_eff = s * (gamma/Eref) * Eref_base (spec mapping).
"""
import hashlib, json, math, sys, time
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parents[1]
OUT = HERE/'out'
LWR = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/long_wavelength_response_c2')
AUD = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/lapse_integration_audit_c2/m0_and_box')
sys.path.insert(0, str(LWR/'tools'))
import lwr_common_v001 as L  # noqa: E402

UPC = L.UPC
C, G = L.C, L.G
KPC = L.KPC
PINS = {
    'lwr_common': (LWR/'tools/lwr_common_v001.py', None),
    'inventory_npz': (LWR/'out/GRID_INVENTORY_V001.npz', '1833cca4b27edafde5e1d27f511b5bc7843f5447eb4d0faebbdeeb98b790d20d'),
    'A2_npz': (UPC/'CLAUDE2/CRITICAL_PATH_EVALUATION_2026-10-17_V001/sampler_eval/CANDIDATE_4CHAIN_POOLED_GRID_V001.npz',
               '2e3a36d888ef8a89c9a2b6073ca6123656c31317c995962c11f34d434eca6ff7'),
    'gate_npz': (UPC/'CLAUDE2/BIRTHK_PILOT_EVALUATION_2026-10-17_V001/out/gate_coeff_grids.npz',
                 '63686db8f7c0239f9c8366113350d4c674e65003595f06a2902e7f821c4eb79b'),
    'worm_npz': (UPC/'CLAUDE2/WORM_PILOT_EVALUATION_2026-10-17_V001/out/coefficients.npz',
                 '032e6410d654389f4faacd7825117e021b12365a3b4d6fefc1ddd0ebe5ca4ea7'),
    'V004_npz': (UPC/'CODEX1/PROVISIONAL_L4_COEFFICIENT_FREEZE_V001/coefficients.npz',
                 'fe5a2f065dec8f120c573eeeb6edc0a24a945d2a0fd70e3f29a66cb986e53e4f'),
    'seed_scan_result': (UPC/'CLAUDE2/runs/A2_SEED_SCAN_G2_RUN_V001/result.json', None),
    'coordinate_spec_V001': (Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calibration_orchestrator_c2/DDO154_CALIBRATION_COORDINATE_SPEC_V001.json'),
                             'fdeb5eb9b69b302c3b7eca21ed772184da56e26224fa4f8b08c8a2b0534106f8'),
    'coordinate_addendum_V004': (Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calibration_orchestrator_c2/v004/COORDINATE_SPEC_ADDENDUM_V004.json'), None),
    'audit_T1_symbol': (AUD/'out/T1_symbol_Q.npz', None),
    'audit_T5': (AUD/'out/T5_ISOLATED_CONTINUUM_KERNEL_V001.json', None),
}
pins = {}
for k, (p, want) in PINS.items():
    h = L.sha(p)
    if want is not None and h != want:
        raise SystemExit('PIN MISMATCH '+k)
    pins[k] = dict(path=str(p), sha256=h)
for k, m in L.MODS.items():
    if k.startswith('fourier_arguments.'):
        pins['module:'+k] = dict(path=m['path'], sha256=L.sha(m['path']))
rep = dict(schema='QINF_DEPENDENCE_V001', pins=pins, anchor_check=L.ANCHOR_CHECK)
assert all(L.ANCHOR_CHECK[k] for k in ('Eref_seed_equals_s_times_unscaled', 'gamma_seed_equals_s_times_unscaled', 'ell_equal'))

# ---------- grids (inventory npz, cross-checked against the pinned source npz arrays) ----------
inv = np.load(PINS['inventory_npz'][0])
src = {}
with np.load(PINS['A2_npz'][0]) as z:
    src['A2_pooled'] = (z['source_hessian_grid'].copy(), z['background_C'].copy(), z['background_mu'].copy())
with np.load(PINS['V004_npz'][0]) as z:
    src['V004_pooled'] = (z['source_hessian_grid'].copy(), z['background_C'].copy(), z['background_mu'].copy())
with np.load(PINS['worm_npz'][0]) as z:
    src['worm_pooled'] = (z['worm_pooled_grid'].copy(), None, None)
with np.load(PINS['gate_npz'][0]) as z:
    src['birthk_pooled'] = (z['birthk_pooled_grid'].copy(), None, None)
grids = {}; gcheck = {}
for name in ('A2_pooled', 'V004_pooled', 'worm_pooled', 'birthk_pooled'):
    g = inv[name+'__grid']; Cb = inv[name+'__Cbar']; mu = inv[name+'__mubar']
    sg, sC, smu = src[name]
    gcheck[name] = dict(grid_equal_pinned_source=bool(np.array_equal(g, sg)),
                        background_equal_pinned_source=(None if sC is None else bool(np.array_equal(Cb, sC) and np.array_equal(mu, smu))),
                        background_source=('pinned npz' if sC is not None else 'long_wavelength_response_c2 t1 rebuild from blocks JSON (moments of chain means)'),
                        grid_array_sha256=hashlib.sha256(np.ascontiguousarray(g).tobytes()).hexdigest(),
                        h_NN_k0=float(g[0, 0, 0, 0, 0].real), Cbar_diag=np.diag(Cb).tolist())
    assert gcheck[name]['grid_equal_pinned_source']
    grids[name] = (g, Cb, mu)
rep['grids'] = gcheck

# ---------- calibration points (values read from the pinned files) ----------
scan = json.loads(PINS['seed_scan_result'][0].read_text())
spec = json.loads(PINS['coordinate_spec_V001'][0].read_text())['box_justification']
EB = scan['base']['Eref_J']
assert EB == L.ANCHOR_UNSCALED['Eref_J'] and scan['base']['ell_F_m'] == L.ANCHOR_UNSCALED['ell_F_m']
cand = {float(c['factor']): c['candidate_seed'] for c in scan['candidates']}
s0 = L.ANCHOR_UNSCALED['common_scale_s']; ge0 = L.ANCHOR_UNSCALED['gamma']/EB; ell0 = L.ANCHOR_UNSCALED['ell_F_m']
assert cand[10.0]['scale_s'] == s0 and abs(cand[10.0]['gamma_over_Eref']/ge0-1) < 1e-15
P = [('anchor_F10', 'A2_pooled', s0, ge0, ell0)]
for f in (1.0, 3.0, 30.0, 100.0):
    P.append(('seedscan_F%g' % f, 'A2_pooled', cand[f]['scale_s'], cand[f]['gamma_over_Eref'], ell0))
P.append(('GE_box_lo@s0', 'A2_pooled', s0, spec['gamma_over_Eref']['box'][0], ell0))
P.append(('GE_box_hi@s0', 'A2_pooled', s0, spec['gamma_over_Eref']['box'][1], ell0))
P.append(('s_box_lo', 'A2_pooled', spec['common_scale_s']['box'][0], ge0, ell0))
P.append(('s_box_hi', 'A2_pooled', spec['common_scale_s']['box'][1], ge0, ell0))
P.append(('ellF_box_lo', 'A2_pooled', s0, ge0, spec['ell_F_m']['box'][0]))
P.append(('ellF_box_hi', 'A2_pooled', s0, ge0, spec['ell_F_m']['box'][1]))
for gname in ('V004_pooled', 'worm_pooled', 'birthk_pooled'):
    P.append(('grid_'+gname, gname, s0, ge0, ell0))

# ---------- analytic EH constant: pinv(E_hat)_nn and the null space's lapse component ----------
def ehat(Cb, khat):
    root = L.root_C(Cb)
    b = L.stat.static_eh_block(Cbar=Cb, k_registered=root@khat, ell_F=1.0, coordinate_cell_measure=.25,
                               real_mode_square_sum=1., gamma=1.0, symmetry_tolerance=1e-10)
    return b['kernel']/b['physical_mode_volume'], b['physical_k']

dirs = {k: np.asarray(v, float)/np.linalg.norm(v) for k, v in L.DIRS.items()}
ehc = {}
for gname, (g, Cb, mu) in grids.items():
    vals = []; nulln = []; ranks = []
    for dn, d in dirs.items():
        E, kp = ehat(Cb, d)
        assert abs(np.dot(kp, kp)-1) < 1e-12
        U, sv, Vt = np.linalg.svd(E)
        r = int(np.sum(sv > 1e-10*sv[0])); ranks.append(r)
        nulln.append(float(np.max(np.abs(Vt[r:, 0]))))
        vals.append(float(np.linalg.pinv(E, rcond=1e-10)[0, 0]))
    ehc[gname] = dict(pinv_Ehat_nn_min=min(vals), pinv_Ehat_nn_max=max(vals), rank_Ehat=sorted(set(ranks)),
                      max_abs_lapse_component_of_null_vectors=max(nulln))
rep['EH_constant'] = ehc
PN = ehc['A2_pooled']['pinv_Ehat_nn_min']
GAMMA_GR = C**4/(16*np.pi*G)
rep['gamma_GR_c4_over_16piG'] = GAMMA_GR

# ---------- cube shell nodes for the T5 Qinf definition ----------
ax, _ = L.axis_nodes()
X, Y, Z = np.meshgrid(ax, ax, ax, indexing='ij')
waves = np.stack([X.ravel(), Y.ravel(), Z.ravel()], axis=1)
kk = np.linalg.norm(waves, axis=1)*KPC
t1 = np.load(PINS['audit_T1_symbol'][0])
assert np.allclose(t1['k_inverse_kpc'], kk, rtol=0, atol=1e-15)
shell = (kk >= 1) & (kk < 2)
ws = waves[shell]
QN = lambda T, kv: (T*np.sum(kv*kv, axis=1)*C**4/(4*np.pi*G))
T5 = json.loads(PINS['audit_T5'][0].read_text())
rep['audit_Qinf_T5'] = T5['Qinf']
rep['audit_Qinf_recomputed_from_T1_npz'] = float(np.median(t1['Q'][shell]))
rep['shell_nodes'] = int(shell.sum())

KS = [0.3, 1.0, 2.0, 10.0, 100.0, 1000.0]
rows = []
for name, gname, s, ge, ell in P:
    t0 = time.time()
    g, Cb, mu = grids[gname]
    Eeff = s*EB; geff = s*ge*EB
    B = L.Binder(g, Cb, mu, Eref=Eeff, ell=ell, gam=geff)
    Qs = QN(B.T_vec(ws), ws)
    row = dict(point=name, grid=gname, s=s, gamma_over_Eref=ge, ell_F_m=ell, Eref_eff_J=Eeff, gamma_eff=geff,
               Qinf_T5def=float(np.median(Qs.real)), Q_shell_1_2_min=float(Qs.real.min()), Q_shell_1_2_max=float(Qs.real.max()),
               Q_shell_imag_over_real_max=float(np.max(np.abs(Qs.imag)/np.abs(Qs.real))),
               Qinf_pred=float(-ehc[gname]['pinv_Ehat_nn_min']*C**4/(4*np.pi*G*geff)))
    row['Qinf_T5def_times_gamma_eff_over_gammaGR'] = row['Qinf_T5def']*geff/GAMMA_GR
    if name == 'anchor_F10':
        row['validation_vs_audit_T1_Q_max_rel'] = float(np.max(np.abs(Qs.real-t1['Q'][shell])/np.abs(t1['Q'][shell])))
    lines = {}
    for kval in KS:
        kv = np.stack([d*kval/KPC for d in dirs.values()])
        T, cond = B.T_vec(kv, want_cond=True)
        q = QN(T, kv).real
        lines[str(kval)] = dict(Q_dir_mean=float(q.mean()), Q_dir_min=float(q.min()), Q_dir_max=float(q.max()),
                                Q_over_pred_mean=float(q.mean()/row['Qinf_pred']), min_cond_inv=float(cond.min()))
    row['Q_lines_13dirs'] = lines
    # reference path: pinned modules at three directions, k=1 /kpc (singular-floor checks in solve_symbol apply)
    ref = []
    for dn in ('z', 'x', '111'):
        kv = dirs[dn]*1.0/KPC
        Tm, _, _ = L.T_module(kv, g, Cb, mu, Eref=Eeff, ell=ell, gam=geff)
        Tb = B.T_vec(kv[None, :])[0]
        ref.append(abs(Tm-Tb)/abs(Tm))
    row['module_vs_batched_max_rel_k1'] = float(max(ref))
    row['seconds'] = round(time.time()-t0, 1)
    rows.append(row)
    print('%-14s %-13s s=%.4g GE=%.4g ell=%.4g geff=%.4e Qinf=%.6f pred=%.6f Q(.3)=%.4f Q(1)=%.4f Q(2)=%.4f Q(100)=%.5f ref=%.1e %.0fs' % (
        name, gname, s, ge, ell, geff, row['Qinf_T5def'], row['Qinf_pred'], lines['0.3']['Q_dir_mean'], lines['1.0']['Q_dir_mean'],
        lines['2.0']['Q_dir_mean'], lines['100.0']['Q_dir_mean'], row['module_vs_batched_max_rel_k1'], row['seconds']), flush=True)
rep['points'] = rows
an = rows[0]
rep['exact_s_scaling_check'] = {r['point']: dict(Qinf_times_s_over_anchor=r['Qinf_T5def']*r['s']/(an['Qinf_T5def']*an['s']),
                                                 **{('Q%s_times_s_over_anchor' % k): r['Q_lines_13dirs'][k]['Q_dir_mean']*r['s']/(an['Q_lines_13dirs'][k]['Q_dir_mean']*an['s'])
                                                    for k in ('0.3', '1.0', '2.0')})
                                for r in rows if r['point'] in ('s_box_lo', 's_box_hi')}
rep['Qinf_gamma_eff_over_gammaGR'] = {r['point']: r['Qinf_T5def_times_gamma_eff_over_gammaGR'] for r in rows}
OUT.mkdir(exist_ok=True)
(OUT/'QINF_EVAL_V001.json').write_text(json.dumps(rep, indent=1, allow_nan=False))
print(json.dumps(dict(EH=ehc, audit=rep['audit_Qinf_T5'], recomputed=rep['audit_Qinf_recomputed_from_T1_npz'],
                      s_check=rep['exact_s_scaling_check']), indent=1))
