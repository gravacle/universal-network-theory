"""Claude3 gate B2 (dispatch 0597), PATH 1b = the PRODUCTION library in-process, per source component (sanity / diagnostics).

Not the gate quantity (the gate's production rows are PATH 1: the rotation-v005 uvt successor + column mean stage replays).
This loads the production tail library exactly as the r5 route-B binding pins it (owned_uv_tail_lapse_v002 2026f2b6, roster
4366e3d6, Jn d6c55b55) and rebuilds the le_rotation tail state of each saved le3 state in-process with the binding's own
recipe (uvt_route_b_binding_c2v001_r5 L425-473: stars_registered + roster_rotation of the le2 rotation the le2 feedback
transformed, M_s from the config; I1-T = stars GL4 rings prep_analytic_j0 + feedback rings vs fixed + new gas at 4096 seeded
nodes; kept = kept_region('le_rotation', None, grid K)), with the SAME uv_tail config file PATH 1 used.  Outputs:
  * the rebuilt full-roster state digest (must equal PATH 1's stage record state_digest: same tail state);
  * rows through the LINEAR static channel (Omega^2 -> Omega^2 + sum_l w rho/h c^2 <t_R>_16 / (A R); the rotation law is
    linear in pr, the stage's 1/(1+f0+t) factor is O(1e-8)) for: full roster, stars-only roster, gas-only roster;
  * the z = 0, 12-row-radius static proxy dv_i = R_i c^2 <d_R t>_16(R_i, 0) / (2 v_i) (certificates_v001 sec 4 / DOUBLING
    definition) for the full roster.
Rows: the pinned observation adapter exactly as column mean v004 L208-227.  Writes only under gate_b2_c3/out/path1b.
Usage: python3 -I -B b2_path1b_module_components_c3v001.py STATE
"""
import hashlib
import importlib.util
import json
import math
import os
import sys
import time
from pathlib import Path

import numpy as np

GATE = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/gate_b2_c3')
EX = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
ROOT = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13')
RUNS = ROOT / 'CLAUDE2/runs'
HR = ROOT / 'helpers/recovered_packet_audit'
R5 = EX / 'tail_scheme_impl_c2/driver_r5'
PINS = {
    'uvt_lib_v002': (R5 / 'module/owned_uv_tail_lapse_v002.py', '2026f2b6e21eba661ef97a5a2b6a8b73d0f8a2d5c3b995611c705f3dc6746a54'),
    'uvt_roster': (EX / 'tail_scheme_impl_c2/module/uv_tail_source_roster_c2v001.py', '4366e3d6ca717b6f25a6799fa60b8ce05561a70d39662d7b1f08b75fc2171ad2'),
    'uvt_jn': (EX / 'tail_scheme_impl_c2/module/posix_libm_bessel_jn_provider_c2v001.py', 'd6c55b55c701a7172e6eaf86ef3f0fedb7f5b2de32d3dbeb06c1bbee471d3171'),
    'profile': (ROOT / 'CODEX1/GALAXY_RADIAL_SOURCE_REFERENCE_V001.json', 'f5becd4586264ef156b021812d440e884f518c61dc9953e41a4fb1494218c60b'),
    'binding': (ROOT / 'CODEX1/DDO154_COLUMN_MEAN_REFERENCE_BINDING_V001.json', 'f42c7c657cd9b8bcef6b88e980918ff2570b1fc0a5480784d8bf3b8bb2a3c600'),
    'observation': (HR / 'galaxy_hi_observation_forward_v001.py', '8e30897e875a619b132ba07e93459333cfd9302bbe2fc98d9a2ff0a2ec6d815d'),
    'adapter': (HR / 'owned_column_mean_streaming_observation_v002.py', '6790e28eb6631c0144f2efda26071a5933f47f7bda7d0c15d3b81e3581cc548c'),
}
STATES = {'C2R3': ('KMAX_A2F10_C2R3_D7R3_RUN_V001', '1f6b32a4edd0dd28438536165bdb10e13c8125eb5ccafb60ceb17315eba8c169'),
          'C3R3': ('KMAX_A2F10_C3R3_D7R3_RUN_V001', 'c9c802f44854d4f41f9e119707235899aba75a8bd42e89c19983f9ca9b817674'),
          'C4R3': ('KMAX_A2F10_C4R3_D7R3_RUN_V001', 'aac01962dc7bf08a7486179bc5674af520f7ea38d73b004154cdd2ff25fa8dee')}
CFG = GATE / 'fixtures/b2c3_uv_tail_cube12_P128MS128_testonly.json'
THREADS = ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS')


def sha_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 22), b''):
            h.update(b)
    return h.hexdigest()


def load(name):
    p, s = PINS[name]
    if sha_file(p) != s:
        raise SystemExit('PIN MISMATCH ' + str(p))
    spec = importlib.util.spec_from_file_location('b2c3_p1b_' + name, str(p)); m = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = m; spec.loader.exec_module(m)
    return m


def write_new(path, obj):
    path = Path(path).resolve()
    if GATE.resolve() not in path.parents:
        raise SystemExit('refusing to write outside gate_b2_c3')
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = (json.dumps(obj, indent=1, allow_nan=False) + '\n').encode()
    with open(path, 'xb') as f:
        f.write(raw)
    return hashlib.sha256(raw).hexdigest()


def arg(argv, key):
    return argv[argv.index(key) + 1]


def main():
    bad = [k for k in THREADS if os.environ.get(k) != '1']
    if bad:
        raise SystemExit('single-thread BLAS env required')
    t0 = time.time(); sid = sys.argv[1]; run, rsha = STATES[sid]; rd0 = RUNS / run
    if sha_file(rd0 / 'result.json') != rsha:
        raise SystemExit('R3 result sha')
    U = load('uvt_lib_v002'); RS = load('uvt_roster'); PV = load('uvt_jn'); jn = PV.create_provider()
    obs = load('observation'); adapter = load('adapter')
    res = json.loads((rd0 / 'result.json').read_text())
    gamma = float(res['identity']['route_a']['custody']['physical']['gamma'])
    rreq = json.loads((rd0 / 'stages/19_le3_rotation/request.json').read_text()); a = rreq['argv']
    ni = json.loads(Path(arg(a, '--seed')).read_text())['numerical_inputs']
    fd = Path(arg(a, '--feedback-directory')); ff = json.loads((fd / 'finish.json').read_text()); fs = json.loads((fd / 'start.json').read_text())
    cp = Path(arg(a, '--checkpoint-directory'))
    src_dir = Path(arg(json.loads((rd0 / 'stages/17_le2_feedback/request.json').read_text())['argv'], '--rotation-directory'))
    if sha_file(src_dir / 'finish.json') != fs['rotation_finish_sha256']:
        raise SystemExit('source rotation')
    sfin = json.loads((src_dir / 'finish.json').read_text())
    if sha_file(sfin['arrays_path']) != sfin['arrays_sha256']:
        raise SystemExit('source arrays sha')
    with np.load(sfin['arrays_path'], allow_pickle=False) as f:
        sarr = {k: f[k].copy() for k in ('rho0', 'volume_weights_m3', 'radial_nodes_m', 'z')}
    prof = json.loads(Path(PINS['profile'][0]).read_text())
    if sha_file(PINS['profile'][0]) != PINS['profile'][1]:
        raise SystemExit('profile pin')
    units = dict(kpc_m=float(ni['kpc_m']), solar_mass_kg=float(ni['solar_mass_kg'])); c = 299792458.0
    s_edges = prof['galaxies']['DDO154']['HI_plus_He']['s_edges_kpc2']
    raw = CFG.read_bytes(); cfg = U.normalize_config(json.loads(raw))
    stars = RS.stars_registered(prof, 'DDO154', units=units)
    ros = RS.roster_rotation(sarr, stars, s_edges_kpc2=s_edges, kpc_m=units['kpc_m'], M_s=cfg['gas']['M_s'])
    # I1-T (binding L425-470 recipe)
    with np.load(ff['outputs']['refreshed_prepared.npz']['path'], allow_pickle=False) as f:
        waves = f['wavevectors'].copy()
    idx = np.sort(np.random.default_rng(20261018).choice(len(waves), min(4096, len(waves)), replace=False)); wv = waves[idx]
    its = sorted(p for p in cp.glob('iteration_*'))
    start = json.loads((its[-1] / 'START.json').read_text())
    fx = start['fixed_source_fourier_J']
    if sha_file(cp / fx['blob']) != fx['file_sha256']:
        raise SystemExit('fixed source blob')
    fixed = np.load(cp / fx['blob'], allow_pickle=False)[:, 0, 0][idx]
    rings = RS.stars_gl4_rings(prof, 'DDO154', kpc_m=units['kpc_m'], solar_mass_kg=units['solar_mass_kg'], gauss_order=ni['source_gauss_order'])
    starT = RS.packet_transform(rings, wv, 'prep_analytic_j0', c_m_s=c, j0=jn.j0)
    m = np.sum(sarr['volume_weights_m3'] * sarr['rho0'], axis=1)
    gasT = RS.packet_transform(dict(R=np.repeat(sarr['radial_nodes_m'], sarr['z'].shape[2]), z=sarr['z'][:, 0, :].reshape(-1), m=m.reshape(-1)),
                               wv, 'feedback_ring_j0_v004', c_m_s=c, j0=jn.j0)
    fb = ff['outputs']['gas_source_feedback.npz']
    with np.load(fb['path'], allow_pickle=False) as f:
        newgas = f['new_gas_fourier_J'][:, 0, 0][idx].copy()
    i1t = RS.check_represented(starT + gasT, fixed + newgas, 'stars prep_analytic_j0 + gas feedback_ring_j0', rtol=1e-12)
    i1t = dict(i1t, nodes=int(len(idx)), seed=20261018)
    br = [float(x) for x in ni['composite_grid_spec']['breaks_inverse_kpc']]; K_m = br[-1] / float(ni['kpc_m'])
    kept = U.kept_region('le_rotation', None, K_m)
    # evaluation geometry: saved le3 rotation + columns
    rfin = json.loads((rd0 / 'stages/19_le3_rotation/rotation/finish.json').read_text())
    with np.load(rfin['arrays_path'], allow_pickle=False) as f:
        rot = {k: f[k].copy() for k in ('radial_nodes_m', 'z', 'rho0', 'enthalpy', 'rotation_Omega_squared')}
    cfin = json.loads((rd0 / 'stages/18_le3_columns_00/columns/finish.json').read_text())
    cols = {it['index']: json.loads(Path(it['path']).read_text()) for it in cfin['completed']}; cols = [cols[i] for i in range(len(cols))]
    binding = json.loads(Path(PINS['binding'][0]).read_text())
    cm = json.loads((rd0 / 'stages/20_le3_column_mean/observation/result.json').read_text())
    rows_saved = np.array([r['speed_km_s'] for r in cm['prediction']['rows']], float)
    R = rot['radial_nodes_m']; zf = rot['z'][:, 0, :]; Rrow = np.array([q['radius_m'] for q in binding['query_rows']], float)
    phis = 2 * math.pi * np.arange(16) / 16
    w_rho_h = np.array([cc['weights_m'] for cc in cols]) * rot['rho0'][:, 0, :] / rot['enthalpy'][:, 0, :]; A = np.sum(w_rho_h, axis=1)

    def rows_for(dpr):
        om2 = rot['rotation_Omega_squared'] + (np.sum(w_rho_h * dpr, axis=1) / A / R)[:, None]
        wts = [(np.asarray(cc['weights_m'], float) * rot['rho0'][i, 0] * binding['HI_to_HI_plus_He_mass_ratio']).tolist() for i, cc in enumerate(cols)]
        pk = adapter.evaluate(observation_module=obs, radial_nodes_m=R, query_ids=[q['id'] for q in binding['query_rows']],
                              query_radii_m=[q['radius_m'] for q in binding['query_rows']], v_phi_m_s=R[:, None] * np.sqrt(om2),
                              emissivity_path_weights=wts, physical_inclination_rad=binding['physical_inclination_rad'],
                              released_inclination_rad=binding['released_inclination_rad'], approximation_provenance=binding['observation_rule'],
                              tracer_provenance=binding['tracer_rule'], source_status='CLAUDE3_B2_PATH1B', motion_status='CLAUDE3_B2_PATH1B',
                              nonaxisymmetric_residual_provenance='Claude3 B2 path 1b')
        return np.array([r['speed_km_s'] for r in pk['rows']], float)
    out = dict(schema='CLAUDE3_B2_PATH1B_MODULE_COMPONENTS_C3V001', producer={'path': str(Path(__file__).resolve()), 'sha256': sha_file(__file__)},
               state=sid, state_result_sha256=rsha, config=dict(path=str(CFG), file_sha256=hashlib.sha256(raw).hexdigest(), config_sha256=cfg['sha256']),
               pins={k: dict(path=str(p), sha256=s) for k, (p, s) in PINS.items()}, i1t=i1t, kept=kept, gamma_eff=gamma,
               rows_saved_le3_km_s=rows_saved.tolist(), components={})
    zero = rows_for(np.zeros(zf.shape))
    out['zero_correction_rows_equal_saved_bitwise'] = bool(zero.tobytes() == rows_saved.tobytes())
    for name, roster, radii in (('full_cols', ros, R), ('stars_only_cols', RS.Roster(stars=stars, gas=None, provenance={'b2c3': 'stars only'}), R),
                                ('gas_only_cols', RS.Roster(stars=None, gas=ros.gas, provenance={'b2c3': 'gas only'}), R),
                                ('full_rows_z0', ros, Rrow)):
        t1 = time.time()
        st = U.build(config=cfg, kept=kept, roster=roster, gamma_eff=gamma, c_m_s=c, eval_radii_m=radii, jn_provider=jn, i1t=i1t, stage_kind='le_rotation')
        rec = dict(state_digest=st.digest, empty=st.empty, quadrature={k: st.record['quadrature'].get(k) for k in ('order', 'N_perp', 'N_z_plus', 'phase_perp_rad', 'phase_z_rad')},
                   production_admissible=st.record.get('production_admissible'), build_seconds=time.time() - t1)
        if name.endswith('_cols'):
            dpr = np.empty(zf.shape); tv = np.empty(zf.shape)
            for i in range(len(R)):
                J = st.cyl_jets(float(R[i]), phis, zf[i], 1)
                dpr[i] = c * c * np.mean(J['fR'], axis=0); tv[i] = np.mean(J['f'], axis=0)
            r = rows_for(dpr)
            rec.update(rows_km_s=r.tolist(), delta_rows_km_s=(r - rows_saved).tolist(), c2_mean_dRt_absmax=float(np.max(np.abs(dpr))),
                       t_mean_absmax=float(np.max(np.abs(tv))))
            if name == 'full_cols':
                out['full_dpr_linear'] = dpr.tolist(); out['full_t_mean'] = tv.tolist()
        else:
            fR = np.empty((len(Rrow), 16))
            for i in range(len(Rrow)):
                fR[i] = st.cyl_jets(float(Rrow[i]), phis, np.array([0.0]), 1)['fR'][:, 0]
            dv = Rrow * c * c * fR.mean(axis=1) / (2 * rows_saved * 1e3) / 1e3
            rec.update(z0_proxy_dv_km_s=dv.tolist(), dRt_mean_per_m=fR.mean(axis=1).tolist(),
                       definition='dv_i = R_i c^2 <d_R t>_16(R_i, z=0) / (2 v_i), v_i = saved le3 row speed')
        out['components'][name] = rec
        print(sid, name, 'digest', st.digest[:12], '%.0fs' % (time.time() - t1), np.round(rec.get('delta_rows_km_s', rec.get('z0_proxy_dv_km_s')), 6).tolist(), flush=True)
    out['seconds'] = time.time() - t0
    h = write_new(GATE / 'out/path1b' / ('P1B_%s_C3V001.json' % sid), out)
    print(sid, 'written', h[:12], '%.0fs' % (time.time() - t0), flush=True)


if __name__ == '__main__':
    main()
