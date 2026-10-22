"""TIMING V003 of single UV-tail builds with the r5 module successor (owned_uv_tail_lapse_v002, cap 8 GiB), gas M_s 128,
production quadrature (the C4T-KHI_P128_MS128_R5 uv_tail block, outer K_big varied), on the saved C4R3-lineage states.
READ-ONLY on every input; writes only under kbig_timing_v003/out (exclusive create).  Not a T statistic; no route-A or
route-B RUN is launched; no target data is read.

Successor of kbig_proxy_v002/tools/kbig_build_timing_c2v002.py (83b9735e): the SAME input readers are imported from it
(route_a_inputs, eval_costs; pinned by bytes) and the SAME build call is made; changes only:
  * library = driver_r5/module/owned_uv_tail_lapse_v002.py (2026f2b6; differs from v001 c28d4209 only in
    TAIL_MEMORY_CAP_BYTES 0.6 GiB -> 8 GiB), roster + provider = the pinned module/ files (identical bytes in driver_r5/module);
  * gas M_s = 128 (the P128 MS128 specs);
  * KINDS: route_a (cold + in-process warm, as v002), route_b_rot (le_rotation own-roster build, 72 radii, cold + an
    in-process second build with a fresh roster on the same StarsProfile = measured 'warm' route-B), route_b_cols (the
    rfs/le columns own-roster build of one 36-column run = rfs_columns_00 shape, radii = radial nodes 0..35).
  * MODE 'st' (production env: every BLAS thread var = 1, as the driver's single_thread_env forces) or 'mt' (NON-PRODUCTION:
    BLAS thread vars unset, Accelerate default threading) -- 'mt' measures one parallel option the driver does not allow.
  * the normalized config is checked field-by-field against the C4T-KHI R5 spec uv_tail block (only outer K_big and the
    two certificate fields may differ; certificates are the TEST_ONLY sentinel = identical arithmetic).
Usage: python3 -I -B kbig_build_timing_c2v003.py KIND KBIG MODE   -> out/TIMING_<KIND>_KB<KBIG>_MS128_<MODE>_V003.json"""
import hashlib
import importlib.util
import json
import os
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / 'out'
X = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
V002_TOOLS = X / 'tail_scheme_impl_c2/kbig_proxy_v002/tools'
V002_TOOL = (V002_TOOLS / 'kbig_build_timing_c2v002.py', '83b9735ec2cb05ee435bf7325d265b4d45dbc22160f7549bac6b60a66a05d5a1')
KP2 = (V002_TOOLS / 'kp2_common_c2v001.py', '5deaeb97f05b1b62e5d1a88ba911f2c01cfc3d055b571625e877cdbed424abbc')
LIB_V002 = (X / 'tail_scheme_impl_c2/driver_r5/module/owned_uv_tail_lapse_v002.py', '2026f2b6e21eba661ef97a5a2b6a8b73d0f8a2d5c3b995611c705f3dc6746a54')
SPEC_KHI = (X / 'v007_launch_packet_cx1/P128/specs/C4T-KHI_P128_MS128_R5_CX1V004.TEMPLATE.json',
            'd01399860e79d47502611f643b36d29e683ba5e3191bea604179e99e63f00508')
THREAD_ENV = ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS')


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 22), b''):
            h.update(b)
    return h.hexdigest()


def load(path_sha, name):
    p, want = path_sha
    if sha(p) != want:
        raise SystemExit('PIN MISMATCH ' + str(p))
    spec = importlib.util.spec_from_file_location(name, str(p))
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m
    spec.loader.exec_module(m)
    return m


def write_new(path, obj):
    path = Path(path)
    if OUT.resolve() not in path.resolve().parents:
        raise SystemExit('refusing to write outside kbig_timing_v003/out: %s' % path)
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = (json.dumps(obj, indent=1, allow_nan=False) + '\n').encode()
    with open(path, 'xb') as f:
        f.write(raw)
    return hashlib.sha256(raw).hexdigest()


def spec_check(U, cfg, Kb):
    raw = json.loads(Path(SPEC_KHI[0]).read_text())['numerics']['uv_tail']
    if sha(SPEC_KHI[0]) != SPEC_KHI[1]:
        raise SystemExit('spec pin')
    raw = dict(raw, outer={'shape': 'cylinder', 'K_big_inverse_kpc': float(Kb)},
               eps_certificate=U.TEST_ONLY_CERT, lo_certificate=U.TEST_ONLY_CERT)
    ref = U.normalize_config(raw)
    diff = sorted(k for k in set(ref) | set(cfg) if k != 'sha256' and ref.get(k) != cfg.get(k))
    if diff:
        raise SystemExit('config differs from the KHI spec uv_tail block: %s' % diff)
    return dict(equal_to_spec_block_with_outer_and_test_only_certs=True, spec=dict(path=str(SPEC_KHI[0]), sha256=SPEC_KHI[1]),
                config_sha256=cfg['sha256'], spec_normalized_sha256=ref['sha256'])


def main():
    kind = sys.argv[1]; Kb = float(sys.argv[2]); mode = sys.argv[3]
    if mode == 'st':
        bad = [k for k in THREAD_ENV if os.environ.get(k) != '1']
        if bad:
            raise SystemExit('st mode needs single-thread env: %s' % bad)
    elif mode == 'mt':
        bad = [k for k in THREAD_ENV if k in os.environ]
        if bad:
            raise SystemExit('mt mode needs thread env unset: %s' % bad)
    else:
        raise SystemExit('MODE st|mt')
    t_all = time.time()
    sys.path.insert(0, str(V002_TOOLS))
    K2 = load(KP2, 'kp2_common_c2v001')
    T2 = load(V002_TOOL, 'kbig_build_timing_c2v002')     # defines CC (certs_common, pinned) + the v002 readers; main() not run
    CC = T2.CC
    _, RS, PV = CC.uvt_modules()                           # roster 4366e3d6, provider d6c55b55 (pinned in certs_common)
    U = load(LIB_V002, 'uvt_lapse_v002')
    jn = PV.create_provider()
    prof = json.loads(Path(CC.pin('profile')['path']).read_text())
    case = CC.SavedR3('C4R3')
    units = dict(kpc_m=case.ni['kpc_m'], solar_mass_kg=case.ni['solar_mass_kg'])
    s_edges = prof['galaxies']['DDO154']['HI_plus_He']['s_edges_kpc2']
    stars = RS.stars_registered(prof, 'DDO154', units=units)
    cfg = CC.uvt_config(U, K_big=Kb, M_s=128)
    chk = spec_check(U, cfg, Kb)
    M_s = cfg['gas']['M_s']
    if kind == 'route_a':
        n_iter = 6
        A = T2.route_a_inputs(U, RS, PV, case, prof, n_iter)
        kept = U.kept_region('route_a', None, case.K / U.KPC_M)
        mk = lambda: RS.roster_route_a(stars, A['init'], A['elements'], A['relaxation'], s_edges_kpc2=s_edges,
                                       kpc_m=units['kpc_m'], M_s=M_s, c_m_s=CC.C)
        radii = A['eval_radii']; i1t = A['i1t']; stage = 'route_a'; order = cfg['jet_order']['route_a']
        info = dict(n_iter_elements=n_iter, n_elements=A['n_elements'], n_columns=A['n_columns'], relaxation=A['relaxation'],
                    eval_radii_rule='v002 RECONSTRUCTED rule (unique column R + probes + stencil)')
        warm_label = 'in-process rebuild, same StarsProfile and k array (the controller complete_iteration path)'
    elif kind in ('route_b_rot', 'route_b_cols'):
        i1t = CC.i1t_on_state(RS, PV, case, prof, s_edges, units, jn)
        arr = case.source_rotation_arrays()
        mk = lambda: RS.roster_rotation(arr, stars, s_edges_kpc2=s_edges, kpc_m=units['kpc_m'], M_s=M_s)
        allR = np.asarray(arr['radial_nodes_m'], float)
        if kind == 'route_b_rot':
            radii = allR; stage = 'le_rotation'
        else:
            radii = allR[:36]; stage = 'le_columns'
        kept = U.kept_region(stage, {'shape': 'cube', 'kmax_inverse_kpc': None}, case.K / U.KPC_M)
        order = cfg['jet_order']['route_b']
        info = dict(source_rotation=str(case.src_rot), n_radial_nodes=int(len(allR)),
                    radii_rule='all 72 radial nodes (le_rotation)' if kind == 'route_b_rot' else
                    'radial nodes 0..35 = rfs_columns_00 of a 2-run split (base radial_nodes_m[ids]; RECONSTRUCTED from the rotation arrays)')
        warm_label = ('in-process second build, fresh roster on the same StarsProfile (stars radial transform cache hit); '
                      'production route-B stages are separate processes, so this is NOT what a stage does today')
    else:
        raise SystemExit('KIND route_a|route_b_rot|route_b_cols')
    t0 = time.time(); roster = mk(); t_roster = time.time() - t0
    g = U._grid(kept, cfg['outer'], cfg['quadrature'], cfg['domain']['R_eval_max_kpc'])
    rss0 = K2.peak_rss_bytes(); c0 = K2.cpu_seconds(); t0 = time.time()
    status = 'BUILT'; refusal = None; rec = {}; warm = None; ev = None
    try:
        st = U.build(config=cfg, kept=kept, roster=roster, gamma_eff=case.gamma, c_m_s=CC.C, eval_radii_m=radii, jn_provider=jn,
                     i1t=i1t, stage_kind=stage)
        rec = dict(memory_estimate_bytes=st.record['memory_estimate_bytes'], quadrature={k: st.record['quadrature'][k] for k in ('N_perp', 'N_z_plus')},
                   rank=st.record['rank'], n_eval_radii=st.record['n_eval_radii'], build_seconds_module=st.diagnostics.get('build_seconds'),
                   state_digest=st.digest, stars_certificates=st.record.get('stars_certificates'))
    except ValueError as exc:
        status = 'REFUSED'; refusal = str(exc)
    wall = time.time() - t0; cpu = K2.cpu_seconds() - c0; rss1 = K2.peak_rss_bytes()
    if status == 'BUILT':
        ev = T2.eval_costs(st, np.unique(radii), order, U.KPC_M)
        del st
        roster2 = mk()
        c1 = K2.cpu_seconds(); t1 = time.time()
        st2 = U.build(config=cfg, kept=kept, roster=roster2, gamma_eff=case.gamma, c_m_s=CC.C, eval_radii_m=radii, jn_provider=jn,
                      i1t=i1t, stage_kind=stage)
        warm = dict(build_wall_seconds=round(time.time() - t1, 2), build_cpu_seconds=round(K2.cpu_seconds() - c1, 2),
                    state_digest_equal_cold=bool(st2.digest == rec['state_digest']), label=warm_label)
    out = dict(schema='UVT_KBIG_BUILD_TIMING_C2V003', label='timing of single r5-module tail builds; not a T statistic',
               producer=K2.producer(__file__), v002_tool=dict(path=str(V002_TOOL[0]), sha256=V002_TOOL[1]),
               library=dict(path=str(LIB_V002[0]), sha256=sha(LIB_V002[0]), cap_bytes=U.TAIL_MEMORY_CAP_BYTES),
               kind=kind, stage_kind=stage, mode=mode, K_big_inverse_kpc=Kb, K_inverse_kpc=case.K, M_s=M_s, spec_check=chk,
               status=status, refusal=refusal, cold_build_wall_seconds=round(wall, 2), cold_build_cpu_seconds=round(cpu, 2),
               warm_build=warm, roster_seconds=round(t_roster, 2), peak_rss_bytes_before_build=rss0,
               peak_rss_bytes_after_cold_build=rss1, peak_rss_bytes_end=K2.peak_rss_bytes(), n_eval_radii=int(len(np.unique(radii))),
               grid=dict(N_perp=int(len(g['kp'])), N_z_plus=int(len(g['kz']))), record=rec, evaluation=ev, i1t=i1t, info=info,
               total_seconds=round(time.time() - t_all, 1), env={k: os.environ.get(k) for k in THREAD_ENV},
               load_note='machine shared with other single-thread jobs (load average ~16-20 on 18 cores at launch); wall under that load',
               pins={k: CC.pin(k) for k in ('uvt_roster', 'uvt_jn', 'profile', 'row_binding', 'prereg_v005')})
    p = OUT / ('TIMING_%s_KB%04d_MS128_%s_V003.json' % (kind, int(Kb), mode))
    h = write_new(p, out)
    print(kind, Kb, mode, status, refusal, 'cold %.1fs cpu %.1fs' % (wall, cpu), 'warm', None if warm is None else warm['build_wall_seconds'],
          'rss %.2f GiB' % (K2.peak_rss_bytes() / 2 ** 30), 'radii', out['n_eval_radii'], h[:8], flush=True)


if __name__ == '__main__':
    main()
