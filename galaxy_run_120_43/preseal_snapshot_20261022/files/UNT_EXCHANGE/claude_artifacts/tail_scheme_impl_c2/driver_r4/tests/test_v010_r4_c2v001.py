"""r4 suite (Claude2 tail_scheme_impl_c2/driver_r4; successor of driver/tests/test_v010_c2v001.py): groups A-I of c2v001 on driver
c2v010 r4 (A2 now: nodes_v001 with an ext grid normalizes, without one refused; H2 extended to the r4 tables and the declared
tail-OFF RO1 opt-in), plus J nodes_v001 planning, K RO1 c2v002 (CHECK F1, hunk 6), L tail OFF on the RO1 workers (A50 items
11-12), M probe radii (A50 item 13), N the F4 reference successor.
Tests of driver c2v010 and the route-A tail manifest writer (Claude2 tail_scheme_impl_c2/driver).  No stage is launched:
subprocess.Popen is replaced by a refusing stub for the whole process, every driver call is simulate (Ctx('simulate')) except
the one run-mode refusal test (B2), which must end BLOCKED before any stage; reviewed files are read only.
Groups: A normalization; B tail planning rules; C stage wiring on the saved DDO154 chain (simulate); D producer whitelist;
E admission rules on saved records; F manifest writer on the route-A lane's synthetic converged sidecar + the real route-B
binding consumer; G NGC K16 plan; H static guards (RA8 / B0_N3); I RO1 / AMB-14 presence.
Usage: python3 -I -B test_v010_c2v001.py V010_PATH V010_SHA OUTDIR RESULT_JSON"""
import copy
import hashlib
import json
import os
import re
import subprocess
import sys
import types
from pathlib import Path

LAUNCHES = []


class _NoLaunch:
    def __init__(self, *a, **k):
        LAUNCHES.append(a[0] if a else k.get('args'))
        raise RuntimeError('LAUNCH_FORBIDDEN_IN_TEST')


import platform  # noqa: E402
platform.platform(); platform.machine()  # warm platform's cached uname()/processor() (it shells out once) before the stub
subprocess.Popen = _NoLaunch  # every stage launch path of the driver goes through subprocess.Popen

EX = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
DRV = EX / 'tail_scheme_impl_c2/driver'
C2 = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2')
EXT = (EX / 'kmax_prereg_v005_c2/extension_c5c6/driver_v009/galaxy_m0_forward_c2v009.py', '999331afd604dd9829aa8f389f43cdb87603d03412d52ba09712226787f18db6')
WRITER = DRV / 'route_a_tail_manifest_c2v001.py'
ROWS = []


def rec(test, ok, **info):
    ROWS.append(dict(test=test, ok=bool(ok), **info))
    print(json.dumps(ROWS[-1], default=str)[:600], flush=True)


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def load_mod(path, want, name):
    raw = Path(path).read_bytes()
    if want is not None and hashlib.sha256(raw).hexdigest() != want:
        raise SystemExit('pin ' + str(path))
    m = types.ModuleType(name)
    m.__file__ = str(path)
    sys.modules[name] = m
    exec(compile(raw, str(path), 'exec'), m.__dict__)
    return m


def expect_refusal(fn, needle, *exc_names):
    try:
        fn()
    except Exception as exc:  # noqa: BLE001
        names = [c.__name__ for c in type(exc).__mro__]
        return (needle in str(exc)) and (not exc_names or any(n in names for n in exc_names)), '%s: %s' % (type(exc).__name__, str(exc)[:300])
    return False, 'NO_EXCEPTION'


def main():
    v010_path, v010_sha, out, result = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3]), Path(sys.argv[4])
    out.mkdir(parents=True, exist_ok=False)
    v = load_mod(v010_path, v010_sha, 'v010_under_test')
    e = load_mod(*EXT, 'v009ext_under_test')
    specs = json.loads((EX / 'tail_scheme_impl_c2/driver_r4/specs/SPECS_V007_C2V002_R1.json').read_text())
    by = {Path(r['file']).name: r for r in specs['specs']}
    z2 = json.loads(Path(by['CALL_UVT_Z2_A2F10_EMPTY_DOMAIN_N8_C2V010.json']['file']).read_text())
    c4t = json.loads(Path(by['CALL_KMAX_TAIL_C4T_A2F10_HULL_N8_M32_C2V010.TEMPLATE.json']['file']).read_text())
    lib = v.uvt_library()

    # ------------------------------------------------------------------ A normalization
    s = copy.deepcopy(z2); s['numerics']['uv_tail']['enabled'] = False
    ok, msg = expect_refusal(lambda: v.normalize_spec(s), 'enabled must be true', 'Refusal'); rec('A1_enabled_false_refused', ok, msg=msg)
    s = copy.deepcopy(c4t); s['numerics']['uv_tail']['source_rule'] = {'rule': 'nodes_v001', 'ext_grid': None}
    ok, msg = expect_refusal(lambda: v.normalize_spec(s), 'UV_TAIL_NODES_V001_EXT_GRID_INVALID', 'Refusal'); rec('A2_r4_nodes_v001_without_ext_grid_refused', ok, msg=msg)
    s = copy.deepcopy(c4t); s['numerics']['uv_tail']['extra'] = 1
    ok, msg = expect_refusal(lambda: v.normalize_spec(s), 'UV_TAIL_CONFIG_INVALID', 'Refusal'); rec('A3_unknown_config_key_refused', ok, msg=msg)
    s = copy.deepcopy(c4t); s['numerics']['uv_tail']['stars'] = {'segment_rule': 'max16_ceil_kdr_plus8', 'tail_nodes': 256}
    ok, msg = expect_refusal(lambda: v.normalize_spec(s), 'UV_TAIL_CONFIG_INVALID', 'Refusal'); rec('A4_V002_stars_key_refused', ok, msg=msg)
    ngc = json.loads((EX / 'ngc_f10_c2/route_b_v006/specs/CALL_NGC3198_ROUTE_B_A2F10_TEMPLATE_C2V006.json').read_text())
    ngc['numerics']['uv_tail'] = copy.deepcopy(c4t['numerics']['uv_tail'])
    ok, msg = expect_refusal(lambda: v.normalize_spec(ngc), 'unknown keys', 'Refusal'); rec('A5_ngc_route_b_with_tail_refused', ok, msg=msg)
    base = json.loads((EX / 'driver_v008_c2/deciding/CALL_A2_ANCHOR_F10_ROUTE_A_PARALLEL_N8_C2V008.json').read_text())
    rec('A6_tail_off_normalization_equals_v009_EXT', v.canonical(v.normalize_spec(base)) == e.canonical(e.normalize_spec(base)))
    nz_raw = v.normalize_spec(z2)['numerics']['uv_tail']
    nz = v.uvt_info(nz_raw)
    want_sha = lib.normalize_config(z2['numerics']['uv_tail'])['sha256']
    rec('A7_z2_normalized_uv_tail_is_the_library_config_and_planning_record', nz_raw == json.loads(v.canonical(z2['numerics']['uv_tail']))
        and lib.normalize_config(nz_raw)['sha256'] == want_sha and nz['config_sha256'] == want_sha and nz['pending_certificates'] == []
        and nz['test_only_certificates'] == ['eps_certificate', 'lo_certificate'], record=nz)
    nc = v.uvt_info(v.normalize_spec(c4t)['numerics']['uv_tail'])
    rec('A8_template_pending_certificates', nc['config_sha256'] is None and nc['pending_certificates'] == ['eps_certificate', 'lo_certificate'])
    s = copy.deepcopy(base); s['numerics']['uv_tail'] = None
    ok, msg = expect_refusal(lambda: v.normalize_spec(s), 'must be an object', 'Refusal'); rec('A9_null_block_refused', ok, msg=msg)

    # ------------------------------------------------------------------ B planning rules
    s = copy.deepcopy(c4t)
    s['numerics']['uv_tail']['eps_certificate'] = s['numerics']['uv_tail']['lo_certificate'] = 'NONE_TEST_ONLY'
    ns = v.normalize_spec(s)
    ok, msg = expect_refusal(lambda: v.execute_chain(v.Ctx('simulate', ns, out / 'B1_sim')), 'UVT_TEST_ONLY_REQUIRES_EMPTY_DOMAIN', 'Refusal')
    rec('B1_test_only_certificates_with_nonempty_domain_refused', ok, msg=msg)
    n0 = len(LAUNCHES)
    ns = v.normalize_spec(c4t)
    ctx = v.Ctx('run', ns, out / 'B2_run')
    (out / 'B2_run').mkdir()
    ok, msg = expect_refusal(lambda: v.execute_chain(ctx), 'PENDING_UV_TAIL_CERTIFICATE', 'Blocked')
    stages_made = (out / 'B2_run' / 'stages').exists()
    rec('B2_run_mode_pending_certificate_BLOCKED_before_any_stage', ok and len(LAUNCHES) == n0 and not stages_made and not ctx.records,
        msg=msg, launches=len(LAUNCHES) - n0, stage_dir_created=stages_made)
    fake = out / 'FAKE_CERTIFICATE_TEST_ONLY_NOT_A_GATE_OUTPUT.json'
    fake.write_text(json.dumps({'note': 'TEST ONLY: exercises the filled-certificate planning path; not an EPS/LO certificate'}))
    s = copy.deepcopy(c4t)
    s['numerics']['uv_tail']['eps_certificate'] = s['numerics']['uv_tail']['lo_certificate'] = {'path': str(fake), 'sha256': sha(fake)}
    ns = v.normalize_spec(s)
    ctx = v.Ctx('simulate', ns, out / 'B3_sim')
    info, _ = v.execute_chain(ctx)
    u = info['uv_tail']
    req = json.loads(Path(u['request']['path']).read_text())
    cfg_raw = json.loads(Path(u['config']['path']).read_text())
    mon = req['monitor']
    v5 = json.loads(v.UVT_MONITOR_PINS['prereg_v005'][0].read_text())
    am = v._argv_map(ctx.records[0]['argv'])
    rec('B3_filled_planning_writes_config_and_request',
        u['config']['written'] and sha(u['config']['path']) == u['config']['sha256'] and sha(u['request']['path']) == u['request']['sha256']
        and lib.normalize_config(cfg_raw)['sha256'] == v.uvt_info(ns['numerics']['uv_tail'])['config_sha256']
        and set(req) == {'schema', 'uv_tail', 'admissibility', 'monitor'} and req['admissibility'] == 'production'
        and len(mon['probe_R_m']) == 12 and len(mon['v_ref_km_s']) == 12 and mon['tau_km_s'] == [float(t) for t in v5['tau_km_s']]
        and len(mon['probe_phi_rad']) == 8 and mon['threshold'] == 0.25
        and am.get('--eps-certificate') == str(fake) and am.get('--eps-certificate-sha256') == sha(fake)
        and am.get('--uv-tail-config-sha256') == u['request']['sha256'],
        kept=u['kept_regions']['route_a']['kept'], admissibility=u['admissibility'])
    ctl_mod = load_mod(v.AUX_UVT['controller'][0], v.AUX_UVT['controller'][1], 'route_a_uv_tail_controller_c2v001')
    try:
        nrq = ctl_mod.normalize_request(req, ctl_mod.load_libraries()['lib'])
        rec('B4_route_a_request_accepted_by_the_controller', nrq['sha256'] and nrq['uv_tail']['sha256'] == v.uvt_info(ns['numerics']['uv_tail'])['config_sha256'],
            request_sha256=nrq['sha256'])
    except Exception as exc:  # noqa: BLE001
        rec('B4_route_a_request_accepted_by_the_controller', False, msg=str(exc))

    # ------------------------------------------------------------------ C wiring on the saved chain (simulate, route A planned)
    sv = {k: x for k, x in v.GALAXIES['DDO154']['saved_runs'].items() if k != 'route_a'}
    a2 = json.loads((C2 / 'specs/CALL_A2_ANCHOR_F10_C2V001.json').read_text())
    for tag, trunc in (('cube', {'shape': 'cube'}), ('sphere', {'shape': 'sphere', 'kmax_inverse_kpc': 2.0})):
        s = copy.deepcopy(a2)
        s['numerics']['truncation'] = trunc
        s['numerics']['uv_tail'] = copy.deepcopy(c4t['numerics']['uv_tail'])
        s['numerics']['uv_tail']['eps_certificate'] = s['numerics']['uv_tail']['lo_certificate'] = {'path': str(fake), 'sha256': sha(fake)}
        ns = v.normalize_spec(s)
        # sphere: the saved offset is a cube offset (its mask check would rightly fail), so the offset is planned, not taken as saved
        ctx = v.Ctx('simulate', ns, out / ('C_%s' % tag), saved_runs=sv if tag == 'cube' else {k: x for k, x in sv.items() if k != 'offset'})
        info, final = v.execute_chain(ctx)
        recs = [r for r in ctx.records if r.get('argv')]
        names = [r['name'] for r in recs]
        srcrot = {r['name']: v._argv_map(r['argv']).get('--uv-tail-source-rotation-directory') for r in recs
                  if r['kind'] in ('columns_v003', 'columns_v005', 'rotation_v005')}
        want = {}
        for r in recs:
            if r['kind'] == 'columns_v003':
                want[r['name']] = str(sv['fs_rotation'])
            elif r['kind'] in ('columns_v005', 'rotation_v005'):
                p = int(r['name'][2])
                want[r['name']] = str(sv['fs_rotation']) if p == 1 else str(sv['le%d_rotation' % (p - 1)])
        tr_ok = all((('--uv-tail-truncation' in v._argv_map(r['argv'])) == (tag == 'sphere'))
                    for r in recs if r['kind'] in v.UVT_TAIL_KINDS and v.UVT_BINDING_KIND[r['kind']] not in ('reference', 'body'))
        tr_val = {v._argv_map(r['argv']).get('--uv-tail-truncation') for r in recs if r['kind'] in v.UVT_TAIL_KINDS} - {None}
        scripts_ok = all(r['script_sha256'] == (v.SCRIPTS_UVT.get(r['kind']) or v.SCRIPTS.get(r['kind']) or (None, r['script_sha256']))[1]
                         for r in recs if r['kind'] not in ('route_a', 'route_a_tail_manifest'))
        man_ok = all('--route-a-tail-manifest' in v._argv_map(r['argv']) for r in recs if r['kind'] in ('reference', 'body', 'offset'))
        fb_ok = all(not any(str(x).startswith('--uv-tail') for x in r['argv']) for r in recs if r['kind'] in ('feedback_v002', 'feedback_v004', 'column_mean_v004'))
        rv = {p['stage']: p['run_mode_value'] for p in info['producer_identity']}
        prod_ok = all(rv[st] == v.SCRIPTS_UVT[k][1] for st, k in (('fs_rotation', 'columns_v001'), ('fs_feedback', 'rotation_v001'))) \
            and all(p['run_mode_value'] == v.SCRIPTS_UVT['rotation_v005'][1] for p in info['producer_identity'] if p['stage'].endswith('_column_mean'))
        rec('C1_%s_saved_chain_wiring' % tag, srcrot == want and tr_ok and scripts_ok and man_ok and fb_ok and prod_ok and len(srcrot) >= 7
            and (tag == 'cube' or tr_val == {'{"kmax_inverse_kpc":2.0,"shape":"sphere"}'}),
            stages=names, source_rotation=srcrot, truncation_values=sorted(tr_val), producers_run_mode=rv,
            final_pass=None if final is None else final['pass'])

    # ------------------------------------------------------------------ D producer whitelist
    us = v.SCRIPTS_UVT['columns_v001'][1]
    ok, msg = expect_refusal(lambda: v.producer_pin('columns_v001', us), 'neither the successor nor its reviewed base', 'Refusal')
    rec('D1_tail_off_refuses_uvt_producer', ok, msg=msg)
    rec('D2_tail_on_admits_uvt_producer', v.producer_pin('columns_v001', us, v.SCRIPTS_UVT)['sha256'] == us
        and v.rotation_producer_pin(v.SCRIPTS_UVT['rotation_v005'][1], v.SCRIPTS_UVT)['sha256'] == v.SCRIPTS_UVT['rotation_v005'][1])

    # ------------------------------------------------------------------ E admission rules on saved records
    cp = C2 / 'runs/A2_ANCHOR_F10_RUN_V001/stages/01_route_a/checkpoint'
    rec('E1_tail_off_admits_v009_checkpoint', v.uvt_route_a_identity_check(cp, None) is None)
    ok, msg = expect_refusal(lambda: v.uvt_route_a_identity_check(cp, '0' * 64), 'UVT_ADMISSION_MISMATCH', 'Refusal')
    rec('E2_tail_on_refuses_tail_off_checkpoint', ok, msg=msg)
    rs = C2 / 'runs/A2_ANCHOR_F10_RUN_V001/stages/02_reference/reference/start.json'
    rec('E3_tail_off_admits_saved_reference', v.uvt_admitted_record_check(rs, None, 'reference') is None)
    ok, msg = expect_refusal(lambda: v.uvt_admitted_record_check(rs, {'config_sha256': '0' * 64}, 'reference'), 'UVT_ADMISSION_MISMATCH', 'Refusal')
    rec('E4_tail_on_refuses_tail_off_reference', ok, msg=msg)
    fake_rec = out / 'E_fake_start.json'
    fake_rec.write_text(json.dumps({'uv_tail': {'enabled': True, 'config_sha256': '1' * 64, 'state_digest': '2' * 64}}))
    ok, msg = expect_refusal(lambda: v.uvt_admitted_record_check(fake_rec, None, 'reference'), 'UVT_ADMISSION_MISMATCH', 'Refusal')
    rec('E5_tail_off_refuses_tail_on_record', ok and v.uvt_admitted_record_check(fake_rec, {'config_sha256': '1' * 64}, 'reference')['config_sha256'] == '1' * 64, msg=msg)

    # ------------------------------------------------------------------ F manifest writer (synthetic converged sidecar) + route-B consumer
    sys.path.insert(0, str(EX / 'tail_scheme_impl_c2/route_a/tests'))
    import uvt_common_c2v001 as U  # noqa: E402  (route-A lane test helpers, read-only)
    W = load_mod(WRITER, sha(WRITER), 'uvt_manifest_writer_under_test')
    mods = U.modules()
    _, meta = U.syn_build(mods)
    req = U.syn_request()
    ctl = U.syn_controller(mods, meta, request=req, sidecar=None)
    run = EX / 'tail_scheme_impl_c2/route_a/out/runs/SYN_TAIL_ON'
    sc, ck = run / 'on1_converged_serial_sidecar', run / 'on1_converged_serial_ck'
    fin = json.loads((sc / 'finish_000.json').read_text())
    att = out / 'F_attempt'
    att.mkdir()
    uv = dict(fin['record'], sidecar={'directory': str(sc), 'finish': {'path': str(sc / 'finish_000.json'), 'sha256': sha(sc / 'finish_000.json')},
                                      'files': fin['files']})
    (att / 'result.json').write_text(json.dumps({'result': {'uv_tail': uv}}))
    (att / 'finish.json').write_text(json.dumps({'status': 'RETURNED_ACTUAL_RESULT', 'result_sha256': sha(att / 'result.json')}))
    try:
        rp, rsha, uvr = W.attempt_tail_record(att, ctl.request['sha256'])
        rec('F1_attempt_tail_record_custody', uvr['accepted_iteration'] == 1, accepted=uvr['accepted_iteration'])
    except Exception as exc:  # noqa: BLE001
        rec('F1_attempt_tail_record_custody', False, msg=str(exc)); uvr = fin['record']
    ok, msg = expect_refusal(lambda: W.attempt_tail_record(att, '0' * 64), 'UV_TAIL_MANIFEST_REQUEST_MISMATCH')
    rec('F2_request_mismatch_refused', ok, msg=msg)
    cm = mods['checkpoint']
    ident = cm._read(str(ck / 'IDENTITY.json'), 'identity')
    n = uvr['accepted_iteration']
    start = cm._read(str(ck / ('iteration_%04d' % n) / 'START.json'), 'iteration_start')
    gas = cm._get(str(ck), start['gas_fourier_J'])
    sid = json.loads((sc / 'SIDECAR_IDENTITY.json').read_text())['identity']
    want = dict(ctl.static_identity, relaxation=float(sid['relaxation']), checkpoint_identity_sha256=ident['identity_sha256'])
    rec('F3_controller_static_identity_equals_sidecar', json.loads(W._canon(want)) == sid)
    records, elements = W.sidecar_elements(sc, n)
    st = W.rebuild_state(ctl, sidecar_identity=sid, elements=elements, n=n, gas=gas)
    rec('F4_rebuilt_state_digest_equals_sidecar_and_result', st.digest == records[n]['state_digest'] == uvr['boundary_state_digest_at_return']
        == uvr['iterations'][-1]['state_digest'], digest=st.digest, empty=st.empty)
    ok, msg = expect_refusal(lambda: W.rebuild_state(U.syn_controller(mods, meta, request=req, sidecar=None),
                                                     sidecar_identity=dict(sid, relaxation=0.25), elements=elements, n=n, gas=gas),
                             'UV_TAIL_SOURCE_MISMATCH')
    rec('F5_wrong_relaxation_refused_by_I1T_before_any_state', ok, msg=msg)
    ok, msg = expect_refusal(lambda: W.rebuild_state(U.syn_controller(mods, meta, request=req, sidecar=None), sidecar_identity=sid,
                                                     elements=elements[:-1] + [dict(elements[-1], integrated_J=elements[-1]['integrated_J'] * 1.001)],
                                                     n=n, gas=gas), 'UV_TAIL_SOURCE_MISMATCH')
    rec('F5b_perturbed_element_roster_refused_by_I1T', ok, msg=msg)
    mrec = W.write_outputs(out / 'F_manifest', controller=ctl, state=st, n=n, identity_sha256=ident['identity_sha256'],
                           start_payload_sha256=start['payload_sha256'], provenance={'test': 'synthetic on1_converged_serial'})
    rb = load_mod(v.AUX_UVT['route_b_binding'][0], v.AUX_UVT['route_b_binding'][1], 'uvt_route_b_binding_under_test')
    cfg = rb._load('lib').normalize_config(req['uv_tail'])
    args = types.SimpleNamespace(route_a_tail_manifest=mrec['manifest'], route_a_tail_manifest_sha256=mrec['manifest_sha256'],
                                 uv_tail_admit_test_only=True, uv_tail_tap=0, outdir=str(out / 'F_manifest'))
    b = rb.Binding(args, 'reference', cfg, cfg['sha256'])
    b._modules()
    kept = b.lib.kept_region('reference', None, 2.0 / U.KPC)
    try:
        man, st2, mref = b._manifest(ident['identity_sha256'], n, start, kept)
        roster, synthetic = b._manifest_gas_roster(man, {'kpc_m': U.KPC})
        rec('F6_route_b_binding_accepts_the_manifest', st2.digest == st.digest and not synthetic and roster.gas.M_s == cfg['gas']['M_s'],
            manifest=mrec)
    except Exception as exc:  # noqa: BLE001
        rec('F6_route_b_binding_accepts_the_manifest', False, msg='%s: %s' % (type(exc).__name__, exc))
    ok, msg = expect_refusal(lambda: b._manifest(ident['identity_sha256'], n + 1, start, kept), 'UV_TAIL_ROUTE_A_MANIFEST_MISMATCH')
    rec('F7_binding_refuses_wrong_iteration', ok, msg=msg)
    tm = json.loads(Path(mrec['manifest']).read_text())
    tm['state']['digest'] = '0' * 64
    tp = out / 'F_tampered_manifest.json'
    tp.write_text(json.dumps(tm))
    b2 = rb.Binding(types.SimpleNamespace(route_a_tail_manifest=str(tp), route_a_tail_manifest_sha256=sha(tp), uv_tail_admit_test_only=True,
                                          uv_tail_tap=0, outdir=str(out)), 'reference', cfg, cfg['sha256'])
    b2._modules()
    ok, msg = expect_refusal(lambda: b2._manifest(ident['identity_sha256'], n, start, kept), 'UV_TAIL_STATE_DIGEST_MISMATCH')
    rec('F8_binding_refuses_tampered_state_digest', ok, msg=msg)

    # ------------------------------------------------------------------ G NGC K16 (plan only)
    ngs = json.loads((EX / 'galaxy_m0_forward_c2_0466/specs/CALL_NGC3198_SEED_C2V002.json').read_text())
    ngs['numerics']['uv_tail'] = {'enabled': True, 'outer': {'shape': 'cylinder', 'K_big_inverse_kpc': 16.0}, 'source_rule': 'continuum_v001',
                                  'gas': {'interp': 'lagrange3_s_gl4', 'M_s': 96},
                                  'stars': {'segment_rule': 'max16_ceil_kdr_plus8', 'tail_rule': 't_panels_40a_phase1p5_gl12'},
                                  'quadrature': {'order': 8, 'w_perp_max_inverse_kpc': 0.005, 'w_z_max_inverse_kpc': 0.007},
                                  'domain': {'R_eval_max_kpc': 136.5, 'z_eval_max_kpc': 105.0, 'z_src_max_kpc': 95.0},
                                  'asymptote': 'EH_exact_minus_quarter', 'lapse_only': True, 'jet_order': {'route_a': 1, 'route_b': 2, 'ngc_eval': 1},
                                  'lambda_scale': 1.0, 'eps_certificate': 'PENDING_UV_TAIL_CERTIFICATE', 'lo_certificate': 'PENDING_UV_TAIL_CERTIFICATE'}
    sp = out / 'G_ngc_seed_with_tail.json'
    sp.write_text(json.dumps(ngs))
    code = v.cmd_dry_run(str(sp), str(out / 'G_ngc_dry'))
    rep = json.loads((out / 'G_ngc_dry/DRYRUN_REPORT.json').read_text())
    p0 = rep['stage_plan'][0]
    rec('G1_ngc_tail_plans_v002_lineage_RO1_worker_and_lineage_swap', code == 0 and p0['script_sha256'] == v.NGC_CODE_UVT['worker'][1]
        and 'ngc_code_lineage_swap' in p0 and p0['ngc_code_lineage_swap']['evidence'][1] == v.NGC_CODE_UVT['lineage_evidence'][1]
        and p0['status'].startswith('PLANNED_BLOCKED'), worker=p0['script'], status=p0['status'])

    # ------------------------------------------------------------------ H static guards (RA8 / B0_N3)
    text = v010_path.read_text()
    rec('H1_driver_never_constructs_a_TailBoundary_or_TailState', 'TailBoundary(' not in text and 'TailState(' not in text and '.build(' not in text)
    lines = text.splitlines()
    i0 = next(i for i, l in enumerate(lines) if l.startswith('def execute_chain(ctx):'))
    i1 = next(i for i in range(i0 + 1, len(lines)) if lines[i].startswith('def '))
    bad = []
    tok = re.compile(r'SCRIPTS_UVT|AUX_UVT|RO1_ROUTE_A|NODES_ROUTE_A|uvt_act\[|uvx\[|uvt_plan\(|uvt_route_a_identity_check\(|uvt_admitted_record_check\(|ro1_off_request\(')
    for i in range(i0, i1):
        l = lines[i]
        if not tok.search(l) or l.strip().startswith('#'):
            continue
        # declared tail-OFF statements (they read records and never fire on v009 outputs): the admission rule UVT_ADMISSION_MISMATCH
        if ('uvt_extra = SCRIPTS_UVT if uvt is not None else None' in l or ("uvt_admitted_record_check(" in l and 'uvt, ' in l)
                or "uvt_extra = uvt_act['scripts'] if uvt is not None else None" in l  # r4: the active-table select (declared, no effect)
                or (l.strip() == 'uvt_route_a_identity_check(cp, None)' and lines[i - 1].strip() == 'if uvt is None:  # C2V010 (u): a tail-OFF call never admits a tail-ON route A (never fires on v009 checkpoints)')):
            continue
        ind = len(l) - len(l.lstrip())
        ok = False
        for j in range(i - 1, i0, -1):
            h = lines[j]
            hi = len(h) - len(h.lstrip())
            if h.strip() and hi < ind:
                hs = h.strip()
                if ('uvt is not None' in hs or 'uvx is not None' in hs or hs.startswith('def uvt_argv') or hs.startswith("elif uvt['config_sha256']")
                        or hs.startswith('if ro1_off:')):  # r4 R5: the declared tail-OFF RO1 opt-in (absent key -> never true)
                    ok = True
                elif hs == 'else:' and any("elif uvt['config_sha256']" in lines[k] for k in range(max(i0, j - 3), j)):
                    ok = True
                elif hs.startswith('if uvt is not None') or hs.startswith('if uvt is None'):
                    ok = 'not None' in hs
                if ok or hi == 4:
                    break
                ind = hi
        if not ok:
            bad.append((i + 1, l.strip()[:120]))
    rec('H2_every_tail_on_statement_in_execute_chain_is_guarded', not bad, unguarded=bad[:10])
    rec('H3_stage_launch_only_through_run_stages', text.count('subprocess.Popen(') == 1)

    # ------------------------------------------------------------------ I RO1 / AMB-14
    ra = {'column_workers': 8, 'max_iterations': 32, 'seed_source_rtol_factor': 0.1}
    ok_ext, msg_ext = expect_refusal(lambda: e.normalize_route_a_numerics(ra), 'unknown keys', 'Refusal')
    rec('I1_seed_source_rtol_factor_v010_only (AMB-14, via the RO1 hunks)', v.normalize_route_a_numerics(ra)['seed_source_rtol_factor'] == 0.1 and ok_ext)
    rec('I2_ro1_functions_present', hasattr(v, 'ro1_outcome') and v.RO1_CODE == 'ROUTE_A_READOUT_NO_CIRCULAR_BRANCH')
    att0 = C2 / 'runs/A2_ANCHOR_F10_RUN_V001/stages/01_route_a/attempt_000'
    ra0 = json.loads((att0 / 'result.json').read_text())
    rv, re_ = v.route_a_outcome_record(ra0, att0 / 'result.json'), e.route_a_outcome_record(ra0, att0 / 'result.json')
    ro1 = rv.pop('ro1', None)
    rec('I3_tail_off_outcome_record = v009-EXT + ro1 non-armed (AMB-15 declared key)', rv == re_ and ro1 == {
        'rule': 'RO1', 'fired': False, 'events': [], 'armed': False, 'worker_sha256': None, 'binding_sha256': None}, ro1=ro1)
    # ================================================================== r4 groups (driver_r4)
    R4 = EX / 'tail_scheme_impl_c2/driver_r4'
    NB = json.loads((EX / 'tail_scheme_impl_c2/nodes_v001/BUILD_NODES_SUCCESSORS_C2V001.json').read_text())
    d5 = json.loads(Path(by['CALL_KMAX_TAIL_C4T_D5_A2F10_HULL_N8_M32_C2V010R4.TEMPLATE.json']['file']).read_text())
    z2off_ro1 = json.loads(Path(by['CALL_UVT_Z2_OFF_RO1_A2F10_N8_C2V010R4.json']['file']).read_text())
    # ------------------------------------------------------------------ J nodes_v001
    nd5 = v.normalize_spec(d5)
    rec('J1_C4TD5_nodes_v001_normalizes', nd5['numerics']['uv_tail'] == json.loads(v.canonical(d5['numerics']['uv_tail'])) and v.uvt_is_nodes(nd5['numerics']['uv_tail']))
    ngn = copy.deepcopy(ngs); ngn['numerics']['uv_tail']['source_rule'] = copy.deepcopy(d5['numerics']['uv_tail']['source_rule'])
    ok, msg = expect_refusal(lambda: v.normalize_spec(ngn), 'UV_TAIL_NODES_V001_DDO154_ONLY', 'Refusal'); rec('J1b_ngc_nodes_v001_refused', ok, msg=msg)
    s = copy.deepcopy(d5)
    s['numerics']['uv_tail']['eps_certificate'] = s['numerics']['uv_tail']['lo_certificate'] = {'path': str(fake), 'sha256': sha(fake)}
    ns = v.normalize_spec(s)
    ctx = v.Ctx('simulate', ns, out / 'J2_nodes_sim')
    info, _ = v.execute_chain(ctx)
    u = info['uv_tail']
    recs = [r for r in ctx.records if r.get('argv')]
    ra_req = ctx.records[0]
    mw = [r for r in ctx.records if r.get('kind') == 'route_a_tail_manifest']
    tail_scripts = {r['kind']: r['script_sha256'] for r in recs if r['kind'] in v.UVT_TAIL_KINDS}
    req = json.loads(Path(u['request']['path']).read_text())
    rec('J2_nodes_plan_uses_the_nodes_tables', u['source_rule'] == 'nodes_v001' and ra_req['script_sha256'] == v.NODES_ROUTE_A['worker_parallel'][1]
        and v._argv_map(ra_req['argv']).get('--solver-sha256') == v.AUX_UVT['solver_parallel'][1]
        and mw and mw[0]['script_sha256'] == v.AUX_UVT_NODES['manifest_writer'][1]
        and all(tail_scripts[k] == v.SCRIPTS_UVT_NODES[k][1] for k in tail_scripts) and len(tail_scripts) >= 4
        and u['nodes_ext_context']['n_ext_nodes'] == 108 ** 3 - 96 ** 3 and all(x['kept']['shape'] == 'cube' for x in u['kept_regions'].values())
        and not u['domain_empty_all_stages'] and info['route_a']['implementation']['kind'] == 'UVTAIL_NODES_RO1_PARALLEL_C2V001'
        and u['monitor_probe_R_m'] == req['monitor']['probe_R_m'] and len(u['monitor_probe_R_m']) == 12
        and u['code']['route_a_controller'][1] == v.AUX_UVT_NODES['controller'][1],
        tail_scripts=tail_scripts, ext=u['nodes_ext_context']['n_ext_nodes'], kind=info['route_a']['implementation']['kind'])
    s3 = copy.deepcopy(s); s3['numerics']['truncation'] = {'shape': 'sphere', 'kmax_inverse_kpc': 4.0}
    ok, msg = expect_refusal(lambda: v.execute_chain(v.Ctx('simulate', v.normalize_spec(s3), out / 'J3_sim')), 'UV_TAIL_NODES_V001_REQUIRES_CUBE_KEPT', 'Refusal')
    rec('J3_nodes_with_sphere_truncation_refused', ok, msg=msg)
    s4 = copy.deepcopy(s); g = s4['numerics']['uv_tail']['source_rule']['ext_grid']; g['panel_orders'] = [6, 6] + [8] + [6] * 12 + [8] + [6, 6]; g['total_axis_nodes'] = sum(g['panel_orders'])
    ok, msg = expect_refusal(lambda: v.execute_chain(v.Ctx('simulate', v.normalize_spec(s4), out / 'J4_sim')), 'UV_TAIL_NODES_V001_EXT_GRID_INVALID', 'Refusal')
    rec('J4_nodes_ext_not_a_supergrid_refused_at_planning', ok, msg=msg)
    s5 = copy.deepcopy(d5); s5['numerics']['uv_tail']['source_rule']['ext_grid'] = None
    ok, msg = expect_refusal(lambda: v.normalize_spec(s5), 'UV_TAIL_NODES_V001_EXT_GRID_INVALID', 'Refusal'); rec('J4b_nodes_ext_null_refused', ok, msg=msg)
    nctl = load_mod(v.AUX_UVT_NODES['controller'][0], v.AUX_UVT_NODES['controller'][1], 'route_a_uv_tail_controller_nodes_c2v001')
    try:
        nrq = nctl.normalize_request(req, nctl.load_libraries()['lib'])
        rec('J5_nodes_request_accepted_by_the_nodes_controller', nrq['uv_tail']['sha256'] == v.uvt_info(ns['numerics']['uv_tail'])['config_sha256'])
    except Exception as exc:  # noqa: BLE001
        rec('J5_nodes_request_accepted_by_the_nodes_controller', False, msg=str(exc))
    rec('J6_binding_blockers_and_pins_clean', v.uvt_binding_blockers(True) == [] and v.uvt_binding_blockers(False) == []
        and len(v.uvt_static_pins(True)) > len(v.uvt_static_pins(False)), nodes_blockers=v.uvt_binding_blockers(True))
    # ------------------------------------------------------------------ K RO1 c2v002 (CHECK F1)
    want = {'worker': '9f74d4652dbbc237f2d38951440a9a95875251fb2cd286499b404a0cf35a8ad1', 'worker_parallel': 'd676ecb2c05e8017a4ffbde74a01e7a7ec1a4290149baa6cbfe62435bb573d97',
            'ngc_worker': '6559ff6a364adbd5d23c04378b74e8fb6adfb8681b52f20451bc8582dce3a593', 'ngc_worker_parallel': '4065fe58e9f5c6734c15ab193de95c69392d477eff8d26c0e6254d49483f2292',
            'binding': '86af6198045ee6995daa7b57e78570643ddbd9edcc0eba42e2fdc816897ca885', 'ngc_binding': '52dc4065da6b0307d1a37bb63bf22921edd08709a763b0ed5a114e8c2b0f2226'}
    rec('K1_RO1_pins_are_c2v002', {k: x[1] for k, x in v.RO1_ROUTE_A.items()} == want and all(sha(x[0]) == x[1] for x in v.RO1_ROUTE_A.values()))
    rec('K2_RO1_messages_A49', v.RO1_MESSAGES == ('NO_SUBLUMINAL_CIRCULAR_PRESSURE_BRANCH', 'DEGENERATE_RADIAL_EULER: zero exact denominator; no unique speed',
                                                  'NON_TIMELIKE_COLUMN') and 'DEGENERATE_RADIAL_EULER: zero exact denominator; no unique speed' in text)
    veh = (EX / 'ro1_readout_c2/driver_patch/c2v002/galaxy_m0_forward_c2v009_ro1_TESTVEHICLE_c2v002.py').read_text()

    def func(src, name):
        ls = src.splitlines(True); i = next(k for k, l in enumerate(ls) if l.startswith('def %s(' % name))
        j = next(k for k in range(i + 1, len(ls)) if ls[k].startswith('def ') or ls[k].startswith('class '))
        return ''.join(ls[i:j])
    fr, fv = func(text, 'ro1_outcome'), func(veh, 'ro1_outcome')
    armed_v = "    armed = bool(bind) and worker in {RO1_ROUTE_A[k][1] for k in ('worker', 'worker_parallel', 'ngc_worker', 'ngc_worker_parallel')}\n"
    armed_r = ("    armed = bool(bind) and worker in ({RO1_ROUTE_A[k][1] for k in ('worker', 'worker_parallel', 'ngc_worker', 'ngc_worker_parallel')}\n"
               "                                      | {NODES_ROUTE_A[k][1] for k in ('worker', 'worker_parallel')})  # C2V010 r4: + the nodes RO1 workers\n")
    rec('K3_RO1_functions_equal_vehicle_c2v002', func(text, 'ngc_read_route_a_result') == func(veh, 'ngc_read_route_a_result')
        and func(text, 'route_a_outcome_record') == func(veh, 'route_a_outcome_record') and fr == fv.replace(armed_v, armed_r) and fv.count(armed_v) == 1)
    syn = EX / 'ro1_readout_c2/out/c2v002/runs/SYN_V002/workers'
    man = out / 'K4_SYNTHETIC_NGC43_MANIFEST.json'
    man.write_text(json.dumps({'scope': 'SYNTHETIC 43-row manifest (RO1 DP7 form); not NGC3198 data', 'rows': [{'query_id': 'SYNQ%02d' % i, 'Rad_text': 'SYN'} for i in range(43)]}))
    k4 = {}
    for tag in ('ngc_serial_ro1_real_nosub', 'ngc_parallel_ro1_real_degenerate'):
        p = syn / tag / 'attempt/result.json'
        got = {}
        for lab, m in (('v009_EXT', e), ('r4', v)):
            try:
                got[lab] = {'returned': m.ngc_read_route_a_result(str(p), str(p.parent / 'finish.json'), manifest_path=str(man))}
            except Exception as exc:  # noqa: BLE001
                got[lab] = {'raised': '%s: %s' % (type(exc).__name__, str(exc)[:120])}
        pr = got['r4'].get('returned') or {}
        k4[tag] = dict(v009_ext=got['v009_EXT'].get('raised', 'returned'), r4_rows=pr.get('rows', 'n/a'), r4_valid=pr.get('valid'),
                       r4_ro1_fired=(pr.get('ro1') or {}).get('fired'), r4_armed=(pr.get('ro1') or {}).get('armed'))
    rec('K4_hunk6_ngc_reader_RO1_aware', all(x['v009_ext'].startswith('TypeError') and x['r4_rows'] is None and x['r4_valid'] is False
                                             and x['r4_ro1_fired'] is True and x['r4_armed'] is True for x in k4.values()), cases=k4)
    # ------------------------------------------------------------------ L tail OFF on the RO1 workers (A50 items 11-12)
    nz = v.normalize_spec(z2off_ro1)
    base_n = v.normalize_spec(base)
    ok_abs = v.canonical(v.normalize_spec(base)) == e.canonical(e.normalize_spec(base))
    neg = {}
    for lab, mut, needle in (('false', lambda q: q['numerics']['route_a'].update(ro1_workers=False), 'must be true'),
                             ('with_tail', lambda q: q['numerics'].update(uv_tail=copy.deepcopy(z2['numerics']['uv_tail'])), 'is for tail-OFF calls'),
                             ('with_admitted_route_a', None, 'requires route A to be computed')):
        q = copy.deepcopy(z2off_ro1)
        if mut is not None:
            mut(q)
        else:
            q = json.loads((EX / 'ngc_route_impl_c2/binding/specs/CALL_REPRO_PINNED_ADMIT_PREFIX_C2V005.json').read_text())
            q['numerics']['route_a'] = {'ro1_workers': True}
        neg[lab] = expect_refusal(lambda: v.normalize_spec(q), needle, 'Refusal')
    rec('L1_ro1_workers_normalization', nz['numerics']['route_a'] == {'column_workers': 8, 'ro1_workers': True} and ok_abs and 'ro1_workers' not in base_n['numerics']['route_a']
        and all(x[0] for x in neg.values()), negatives={k: x[1] for k, x in neg.items()})
    ctx = v.Ctx('simulate', nz, out / 'L2_ro1_off_sim')
    info, _ = v.execute_chain(ctx)
    ra_req = ctx.records[0]; am = v._argv_map(ra_req['argv'])
    offreq = json.loads(Path(am['--uv-tail-config']).read_text())
    others = [r for r in ctx.records[1:] if r.get('argv')]
    rec('L2_ro1_off_plan', ra_req['script_sha256'] == v.RO1_ROUTE_A['worker_parallel'][1] and am.get('--solver-sha256') == v.PARALLEL_ROUTE_A['solver'][1]
        and offreq['uv_tail']['enabled'] is False and am.get('--eps-certificate') == 'NONE_TEST_ONLY' and sha(am['--uv-tail-config']) == am.get('--uv-tail-config-sha256')
        and 'uv_tail' not in info and info['route_a']['implementation']['kind'] == 'TAIL_OFF_RO1_PARALLEL_C2V010R4'
        and all(r['script_sha256'] == v.SCRIPTS[r['kind']][1] and not any(str(x).startswith('--uv-tail') for x in r['argv']) for r in others)
        and v.ro1_off_blockers() == [] and str(v.RO1_ROUTE_A['binding'][0]) in v.all_static_pins(nz), stages=[r['name'] for r in ctx.records])
    # synthetic attempts: armed set
    k5 = {}
    for lab, wsha in (('ro1_parallel', v.RO1_ROUTE_A['worker_parallel'][1]), ('nodes_parallel', v.NODES_ROUTE_A['worker_parallel'][1]),
                      ('v009_parallel', v.PARALLEL_ROUTE_A['worker'][1])):
        d = out / ('L3_attempt_' + lab); d.mkdir()
        (d / 'start.json').write_text(json.dumps({'worker_pin': wsha}))
        rr = {'input_pins': {str(Path(v.RO1_ROUTE_A['binding'][0]).resolve()): v.RO1_ROUTE_A['binding'][1]}}
        blk, fired = v.ro1_outcome(rr, {}, d / 'result.json', True)
        k5[lab] = (blk['armed'], fired)
    rec('L3_ro1_armed_set', k5 == {'ro1_parallel': (True, False), 'nodes_parallel': (True, False), 'v009_parallel': (False, False)}, cases=k5)
    # ------------------------------------------------------------------ M probe radii in the route-A tail record (A50 item 13; code reading + plan)
    rec('M1_probe_R_m_copied_into_route_a_record', "uvx['route_a_record'].update(probe_R_m=list(uvx['monitor_probe_R_m'])" in text
        and 'monitor_probe_R_m' in u, note='TESTED at plan level (J2); the copy into result.uv_tail.route_a_record runs only on a returned route A (UNTESTED here)')
    # ------------------------------------------------------------------ N F4 reference successor
    f4 = NB['continuum_reference_f4']
    rec('N1_F4_reference_successor_planned', v.SCRIPTS_UVT['reference'][1] == f4['sha256'] and sha(v.SCRIPTS_UVT['reference'][0]) == f4['sha256']
        and v.SCRIPTS_UVT_NODES['reference'][1] == NB['stages']['reference']['sha256'])
    rec('Z_no_launch_attempted', not LAUNCHES, launches=LAUNCHES)
    res = {'schema': 'TEST_V010_R4_C2V001', 'driver': [str(v010_path), v010_sha], 'writer': [str(WRITER), sha(WRITER)],
           'tests': ROWS, 'passed': sum(r['ok'] for r in ROWS), 'failed': [r['test'] for r in ROWS if not r['ok']]}
    with open(result, 'x') as f:
        json.dump(res, f, indent=1, default=str)
    print(json.dumps({'passed': res['passed'], 'total': len(ROWS), 'failed': res['failed']}))


if __name__ == '__main__':
    main()
