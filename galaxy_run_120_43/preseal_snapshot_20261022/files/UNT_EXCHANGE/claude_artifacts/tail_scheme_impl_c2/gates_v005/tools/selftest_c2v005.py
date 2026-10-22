"""Self-test of run_identity_compare_c2v005 (and the gates_v005 token tool and fill tool c2v002).  Claude2 gates_v005.

Part T  tokens: the derived replace-mode sets vs the z2_v002 append set (4cbe46ed): the 16 appended (path, sha) successor pairs
        equal the replaced NEW sides; the replaced base forms are absent; the RO1 and other 26 entries are unchanged.
Part C  the gates_v004 check lane's canaries (check/scripts/canaries_c2v004_cl001.py 9ff721e0), PORTED, for each driver r4 / r5:
        the same 29 MUST_FAIL and 10 MUST_PASS cases with the same mutations, with stage directories looked up by name (the
        checker's literal 'stages/02_reference' cannot hold in a Z2 tree that carries the driver's manifest stage), plus the
        checker's 6 probes (F08, Q01-Q05), which c2v005 must now FAIL.  Base trees: the checker's own bases (selftest C2 copies of
        Codex3's baselines), rebuilt driver-faithful in each case's own directory (build_tree): real pinned stage scripts (v008 reference side, the selected
        driver's new side), result.json driver_sha256, and for Z2 the driver's tail shape (inputs uv_tail files, the
        route_a_tail_manifest stage, the tail argv blocks, the uv_tail record, the RO1 worker of the driver, the declared tail
        pins in the attempt start.json and the checkpoint IDENTITY).  Tokens: the derived replace-mode Z2 set of the driver;
        B0P: none.  Each case mutates its own copy; the comparator runs as a subprocess (python3 -I -B).
Part N  own cases (B1, B2, S1-S3, A59, A67 N1, rules, pins, ledger, progress, static pins), r4 and r5.
Part F  fill tool c2v002: guard unit tests on a scratch registered directory; CLI refusals on the registered C5H name (string
        and symlink-target markers: nothing under the C5H directory is stat-ed); N2 type-exact T1; regression: the gates_v004
        stand-ins S1/S2 re-filled byte-identical to c9a6d5cf / d9e715e2.
Synthetic trees only, except Part F's read-only regression (finished runs UVT_Z2_A2F10_RUN_V001 and the C2V008 deciding run).
  python3 -I -B selftest_c2v005.py OUTDIR
"""
import copy
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np

PY = '/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
G5 = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v005')
G4 = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v004')
CMP = G5 / 'run_identity_compare_c2v005.py'
FILL = G5 / 'tools/fill_picard_member_c2v002.py'
CHECK_BASE = (G4 / 'out/SELFTEST_C2V004_V002/C/C2_declared_drivers')
CHECKER = (G4 / 'check/scripts/canaries_c2v004_cl001.py', '9ff721e0')
APPEND_Z2 = (Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_identity_gates_c2/z2_v002/TOKENS_Z2_C2V004.json'),
             '4cbe46edc6795916aa98cebfdd05ca154d707a1425cbb5f9753fcf0e1ca209bc')
V008 = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/driver_v008_c2/galaxy_m0_forward_c2v008.py',
        'f8e4770106abb83df5e658e91edc5593198fe87f0600ee5d1946f22415902f28')
EXT = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/kmax_prereg_v005_c2/extension_c5c6/driver_v009/galaxy_m0_forward_c2v009.py',
       '999331afd604dd9829aa8f389f43cdb87603d03412d52ba09712226787f18db6')
T = 'NONE_TEST_ONLY'


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def rj(p):
    return json.loads(Path(p).read_text())


def wj(p, o, indent=2, sort_keys=False):
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    if p.exists() or p.is_symlink():
        p.unlink()  # only ever inside this lane's OUTDIR copies
    p.write_text(json.dumps(o, indent=indent, sort_keys=sort_keys))


def wnpy(p, a):
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    if p.exists():
        p.unlink()
    with open(p, 'xb') as f:
        np.save(f, a, allow_pickle=False)


def load_mod(path, name):
    s = importlib.util.spec_from_file_location(name, str(path))
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


def sdir(run, name):
    hits = [d for d in sorted((Path(run) / 'stages').iterdir()) if d.is_dir() and d.name[3:] == name]
    if len(hits) != 1:
        raise RuntimeError('stage %s in %s: %d' % (name, run, len(hits)))
    return hits[0]


def req(run, name='reference'):
    return sdir(run, name) / 'request.json'


def fin(run):
    return sdir(run, 'reference') / 'reference/finish.json'


# ---------------------------------------------------------------- driver-faithful base trees
def write_identity(cm, p, add_pins):
    body = cm._read(str(p), 'identity')
    caller = cm.decode(body['identity']['caller']['record'])
    caller = dict(caller)
    cp = dict(caller['code_pins'])
    cp.update(add_pins)
    caller['code_pins'] = cp
    body['identity']['caller'] = {'sha256': cm.digest(caller), 'record': cm.encode(caller)}
    body.pop('payload_sha256', None)
    body['payload_sha256'] = cm._sha(cm._canonical(body))
    p.unlink()
    p.write_bytes(cm._canonical(body) + b'\n')
    cm._read(str(p), 'identity')


def build_tree(gate, base, dkey, c5, drv, t8, cm):
    """Build the driver-faithful REF/NEW pair for `gate` directly in `base` (paths inside the files are this tree's own)."""
    D = c5.DRIVERS[dkey]
    if gate == 'B0P_RERUN':
        return build_b0p(base, D, drv)
    return build_z2(base, D, dkey, drv, t8, cm)


def build_b0p(b, D, drv):
    shutil.copytree(CHECK_BASE / 'CANARY_B0P_RERUN_00_baseline' / 'REF', b / 'REF')
    shutil.copytree(CHECK_BASE / 'CANARY_B0P_RERUN_00_baseline' / 'NEW', b / 'NEW')
    for run, dsha in ((b / 'REF', V008[1]), (b / 'NEW', D[1])):
        q = rj(req(run)); q['script'], q['script_sha256'] = str(drv.SCRIPTS['reference'][0]), drv.SCRIPTS['reference'][1]; wj(req(run), q)
        r = rj(run / 'result.json'); r['driver_sha256'] = dsha; wj(run / 'result.json', r)
    s = rj(b / 'NEW/start.json'); s['driver'], s['driver_sha256'] = D; wj(b / 'NEW/start.json', s)
    return b


def build_z2(z, D, dkey, drv, t8, cm):
    shutil.copytree(CHECK_BASE / 'CANARY_Z2_00_baseline' / 'REF', z / 'REF')
    shutil.copytree(CHECK_BASE / 'CANARY_Z2_00_baseline' / 'NEW', z / 'NEW')
    R, N = (z / 'REF').resolve(), (z / 'NEW').resolve()
    for run in (R, N):
        wj(run / 'inputs/seed_c2v001.json', {'synthetic_seed': True, 'source_rtol': 0.01})
    os.rename(N / 'stages/02_reference', N / 'stages/03_reference')
    wj(N / 'inputs/uv_tail_config.json', {'synthetic_uv_tail_config': True})
    wj(N / 'inputs/uv_tail_route_a_request.json', {'schema': 'UNT_UV_TAIL_ROUTE_A_REQUEST_C2V001', 'synthetic': True})
    man = N / 'stages/02_route_a_tail_manifest/manifest/ROUTE_A_TAIL_MANIFEST.json'
    wj(man, {'synthetic_manifest': True})
    cfg, rq = N / 'inputs/uv_tail_config.json', N / 'inputs/uv_tail_route_a_request.json'

    def ra_argv(run):
        return ['--seed', str(run / 'inputs/seed_c2v001.json'), '--seed-sha256', sha(run / 'inputs/seed_c2v001.json'),
                '--outdir', str(run / 'stages/01_route_a/attempt_000'), '--checkpoint-directory', str(run / 'stages/01_route_a/checkpoint'),
                '--column-workers', '8']
    ra_block = ['--uv-tail-config', str(rq), '--uv-tail-config-sha256', sha(rq), '--eps-certificate', T, '--eps-certificate-sha256', T,
                '--lo-certificate', T, '--lo-certificate-sha256', T, '--uv-tail-sidecar-directory', str(N / 'stages/01_route_a/uv_tail_sidecar')]
    q = rj(R / 'stages/01_route_a/request.json'); q['argv'] = ra_argv(R); wj(R / 'stages/01_route_a/request.json', q)
    wp = drv.RO1_ROUTE_A['worker_parallel']
    q = rj(N / 'stages/01_route_a/request.json'); q['argv'] = ra_argv(N) + ra_block
    q['script'], q['script_sha256'] = str(wp[0]), wp[1]
    wj(N / 'stages/01_route_a/request.json', q)
    mw = drv.AUX_UVT['manifest_writer']
    margv = ['--seed', str(N / 'inputs/seed_c2v001.json'), '--seed-sha256', sha(N / 'inputs/seed_c2v001.json'),
             '--attempt-directory', str(N / 'stages/01_route_a/attempt_000'), '--checkpoint-directory', str(N / 'stages/01_route_a/checkpoint'),
             '--checkpoint-module', str(drv.AUX['checkpoint_module'][0]), '--checkpoint-module-sha256', drv.AUX['checkpoint_module'][1],
             '--uv-tail-request', str(rq), '--uv-tail-request-sha256', sha(rq), '--outdir', str(N / 'stages/02_route_a_tail_manifest/manifest')]
    wj(N / 'stages/02_route_a_tail_manifest/request.json', {'name': 'route_a_tail_manifest', 'kind': 'route_a_tail_manifest', 'script': str(mw[0]),
                                                           'script_sha256': mw[1], 'argv': margv})
    ref_block = ['--uv-tail-config', str(cfg), '--uv-tail-config-sha256', sha(cfg), '--uv-tail-admit-test-only',
                 '--route-a-tail-manifest', str(man), '--route-a-tail-manifest-sha256', sha(man)]
    q = rj(req(R)); q['script'], q['script_sha256'] = str(t8['SCRIPTS']['reference'][0]), t8['SCRIPTS']['reference'][1]; wj(req(R), q)
    q = rj(req(N)); q['script'], q['script_sha256'] = str(drv.SCRIPTS_UVT['reference'][0]), drv.SCRIPTS_UVT['reference'][1]
    q['argv'] = q['argv'] + ref_block; wj(req(N), q)
    tail_pins = {str(Path(p).resolve()): s for p, s in (drv.AUX_UVT['controller'], drv.UVT_LIB['lib'], drv.UVT_LIB['roster'], drv.UVT_LIB['provider'])}
    tail_pins[str(rq)] = sha(rq)
    st = rj(N / 'stages/01_route_a/attempt_000/start.json')
    st['worker_pin'] = wp[1]
    st['input_pins'] = {str(Path(drv.RO1_ROUTE_A['binding'][0]).resolve()): drv.RO1_ROUTE_A['binding'][1],
                        str(Path(drv.AUX_UVT['facade'][0]).resolve()): drv.AUX_UVT['facade'][1], **tail_pins}
    wj(N / 'stages/01_route_a/attempt_000/start.json', st)
    write_identity(cm, N / 'stages/01_route_a/checkpoint/IDENTITY.json', tail_pins)
    r = rj(R / 'result.json'); r['driver_sha256'] = V008[1]; r['route_a_outcome'].pop('ro1', None); wj(R / 'result.json', r)
    r = rj(N / 'result.json'); r['driver_sha256'] = D[1]
    r['route_a_outcome']['ro1'] = {'rule': 'RO1', 'armed': True, 'fired': False, 'events': [], 'worker_sha256': wp[1],
                                   'binding_sha256': drv.RO1_ROUTE_A['binding'][1]}
    r['uv_tail'] = {'enabled': True, 'config': {'path': str(cfg), 'sha256': sha(cfg)}, 'request': {'path': str(rq), 'sha256': sha(rq)},
                    'manifest': {'path': str(man), 'sha256': sha(man)}, 'admissibility': 'test_only', 'test_only_flag': ['--uv-tail-admit-test-only'],
                    'certificates': {'eps_certificate': [T, T], 'lo_certificate': [T, T]}, 'route_a_argv': ra_block[:-2], 'truncation_argv': None}
    wj(N / 'result.json', r)
    s = rj(N / 'start.json'); s['driver'], s['driver_sha256'] = D; wj(N / 'start.json', s)
    return z


# ---------------------------------------------------------------- cases
def cases(dkey, drv, t8, te, c5, tokdir):
    D = c5.DRIVERS[dkey]
    other = 'r5' if dkey == 'r4' else 'r4'
    Z, B = 'Z2', 'B0P_RERUN'
    cs = []

    def add(tag, gate, expect, mut=None, must_fail=(), note='', driver=None):
        cs.append(dict(tag=tag, gate=gate, expect=expect, mut=mut, must_fail=must_fail, note=note, driver=driver or dkey))

    # ======== the checker's canaries (ported)
    add('P00_baseline_B0P', B, 'MUST_PASS')
    add('P00_baseline_Z2', Z, 'MUST_PASS')
    add('F01_extra_toplevel_txt', B, 'MUST_FAIL', lambda r, n, d: (n / 'notes.txt').write_bytes(b'x\n') and None, ('INVENTORY',))
    add('F02_extra_route_a_attempt_json', Z, 'MUST_FAIL', lambda r, n, d: wj(sdir(n, 'route_a') / 'attempt_000/extra.json', {'x': 1}), ('INVENTORY',))
    add('F03_extra_inputs_file', B, 'MUST_FAIL', lambda r, n, d: wj(n / 'inputs/extra_config.json', {'x': 1}), ('INVENTORY',))

    def dup_tampered(r, n, d):
        src = sdir(n, 'reference')
        shutil.copytree(src, n / 'stages/09_reference')
        o = rj(src / 'reference/finish.json'); o['metric'] = 999.0; wj(src / 'reference/finish.json', o)
    add('F04_duplicate_stage_number_tampered', B, 'MUST_FAIL', dup_tampered, ('STAGE_SET', 'INVENTORY'), 'B1')
    add('F05_duplicate_stage_number_extra_copy', B, 'MUST_FAIL', lambda r, n, d: shutil.copytree(sdir(n, 'reference'), n / 'stages/09_reference') and None,
        ('STAGE_SET', 'INVENTORY'), 'B1')

    def blob(r, n, d):
        b = sdir(n, 'route_a') / 'checkpoint/blobs/0000.npy'
        raw = bytearray(b.read_bytes()); raw[-1] ^= 1
        b.unlink(); b.write_bytes(bytes(raw))
    add('F06_route_a_blob_npy_last_bit', Z, 'MUST_FAIL', blob, ('RA_BLOBS',))
    add('F07_stage_npy_1ulp', B, 'MUST_FAIL', lambda r, n, d: [wnpy(sdir(r, 'reference') / 'reference/field.npy', np.array([1.0, 2.0])),
                                                             wnpy(sdir(n, 'reference') / 'reference/field.npy', np.array([1.0, np.nextafter(2.0, 3.0)]))], ('STAGES',))
    add('F08_route_a_attempt_arrays_npy_changed', Z, 'MUST_FAIL', lambda r, n, d: [
        wnpy(sdir(r, 'route_a') / 'attempt_000/arrays/000001_extra.npy', np.array([1.0])),
        wnpy(sdir(n, 'route_a') / 'attempt_000/arrays/000001_extra.npy', np.array([2.0]))], ('FILES_ROUTE_A',), 'checker probe; S3')
    add('F09_stage_argv_value', B, 'MUST_FAIL', lambda r, n, d: wj(req(n), dict(rj(req(n)), argv=['--tolerance', '0.010'])), ('REQUEST',))
    add('F10_route_a_argv_column_workers', Z, 'MUST_FAIL',
        lambda r, n, d: wj(req(n, 'route_a'), dict(rj(req(n, 'route_a')), argv=['--column-workers', '8', '--max-iterations', '5'])), ('REQUEST',))

    def dup_flag(r, n, d):
        q = rj(req(n, 'route_a'))
        q['argv'] = q['argv'] + ['--uv-tail-sidecar-directory', '/elsewhere/uv_tail_sidecar', '--uv-tail-sidecar-directory',
                                 str(sdir(n, 'route_a') / 'uv_tail_sidecar')]
        wj(req(n, 'route_a'), q)
    add('F11_route_a_declared_flag_twice_first_outside_run', Z, 'MUST_FAIL', dup_flag, ('REQUEST',), 'S1')

    def flag_wrong_kind(r, n, d):
        q = rj(req(n)); q['argv'] = q['argv'] + ['--uv-tail-source-rotation-directory', str(sdir(n, 'reference') / 'x')]; wj(req(n), q)
    add('F12_Z2_rotation_dir_flag_on_reference_stage', Z, 'MUST_FAIL', flag_wrong_kind, ('REQUEST',), 'S2')

    def fs_feedback(r, n, d, flag):
        for run, num, scr in ((r, '03', t8['SCRIPTS']['feedback_v002']), (n, '04', drv.SCRIPTS['feedback_v002'])):
            dst = run / 'stages' / ('%s_fs_feedback' % num)
            shutil.copytree(sdir(run, 'reference'), dst)
            q = rj(dst / 'request.json')
            q['kind'] = 'feedback_v002'; q['script'], q['script_sha256'] = str(scr[0]), scr[1]; q['argv'] = ['--tolerance', '0.01']
            wj(dst / 'request.json', q)
        if flag:
            q = rj(req(n, 'fs_feedback')); q['argv'] = q['argv'] + ['--uv-tail-admit-test-only']; wj(req(n, 'fs_feedback'), q)
    add('F13_Z2_tail_flag_on_non_UVT_kind_stage', Z, 'MUST_FAIL', lambda r, n, d: fs_feedback(r, n, d, True), ('REQUEST',), 'S2')

    def sz_stage(r, n, d):
        for run, v in ((r, 0.0), (n, -0.0)):
            o = rj(fin(run)); o['nested']['probe'] = v; wj(fin(run), o)
    add('F14_stage_json_signed_zero', B, 'MUST_FAIL', sz_stage, ('STAGES',))

    def res_set(run, fn):
        o = rj(run / 'result.json'); fn(o); wj(run / 'result.json', o)
    add('F15_result_rows_signed_zero', B, 'MUST_FAIL', lambda r, n, d: [res_set(r, lambda o: o['rows'][0].__setitem__('speed_km_s', 0.0)),
                                                                       res_set(n, lambda o: o['rows'][0].__setitem__('speed_km_s', -0.0))], ('RESULT',))
    add('F16_result_unlisted_key_signed_zero', B, 'MUST_FAIL', lambda r, n, d: [res_set(r, lambda o: o.__setitem__('residual_diagnostics', {'max_abs_residual': 0.0})),
                                                                               res_set(n, lambda o: o.__setitem__('residual_diagnostics', {'max_abs_residual': -0.0}))], ('RESULT',), 'B2')

    def sz_ckpt(r, n, d):
        for run, v in ((r, 0.0), (n, -0.0)):
            p = sdir(run, 'route_a') / 'checkpoint/iteration_0000/COMPLETED.json'; o = rj(p); o['residual'] = v; wj(p, o)
    add('F17_checkpoint_record_signed_zero', Z, 'MUST_FAIL', sz_ckpt, ('RA_RECORDS',))
    add('F18_stage_json_float_to_int', B, 'MUST_FAIL', lambda r, n, d: wj(fin(n), dict(rj(fin(n)), metric=2)), ('STAGES',))
    add('F19_result_rows_float_to_int', B, 'MUST_FAIL', lambda r, n, d: res_set(n, lambda o: o['rows'][0].__setitem__('speed_km_s', 1)), ('RESULT',))

    def f20(o, v):
        o['picard_bound_met'] = True; o['residual_diagnostics'] = {'n_rows': v}
    add('F20_result_unlisted_key_float_to_int', B, 'MUST_FAIL', lambda r, n, d: [res_set(r, lambda o: f20(o, 1.0)), res_set(n, lambda o: f20(o, 1))], ('RESULT',), 'B2')

    def f21(o, v):
        o['accepted_for_calibration'] = v; o['picard_bound_met'] = v
    add('F21_result_unlisted_verdict_keys_flipped', B, 'MUST_FAIL', lambda r, n, d: [res_set(r, lambda o: f21(o, True)), res_set(n, lambda o: f21(o, False))], ('RESULT',), 'B2')
    add('F22_result_pass_unlisted_key_bool_to_int', B, 'MUST_FAIL', lambda r, n, d: [res_set(r, lambda o: o['passes'][0].__setitem__('rotation_positive', True)),
                                                                                    res_set(n, lambda o: o['passes'][0].__setitem__('rotation_positive', 1))], ('RESULT',), 'B2')

    def f23(o):
        o['route_a_outcome']['classification'] = 'NOT_CONVERGED'; o['route_a_outcome']['result_sha256'] = 'e' * 64
    add('F23_result_route_a_outcome_changed', Z, 'MUST_FAIL', lambda r, n, d: res_set(n, f23), ('RESULT',), 'B2')

    def smuggle(r, n, d):
        a, b = rj(req(r)), rj(req(n))
        b['script'], b['script_sha256'] = '/x/evil_reference.py', 'c' * 64
        wj(req(n), b)
        t = d / 'TOKENS_SMUGGLE.json'
        wj(t, {'declared': [[a['script'], b['script'], '<S_PATH>'], [a['script_sha256'], b['script_sha256'], '<S_SHA>']]})
        return {'tokens': t}
    add('F24_script_swap_hidden_by_declared_token', B, 'MUST_FAIL', smuggle, ('AUTO_CUSTODY',))

    def swap(run, scr):
        q = rj(req(run)); q['script'], q['script_sha256'] = str(scr[0]), scr[1]; wj(req(run), q)
    add('F25_swap_to_driver_entry_of_other_kind', Z, 'MUST_FAIL', lambda r, n, d: swap(n, drv.SCRIPTS_UVT['body']), ('AUTO_CUSTODY',))
    add('F26_Z2_reference_swap_to_plain_base_not_uvt', Z, 'MUST_FAIL', lambda r, n, d: swap(n, drv.SCRIPTS['reference']), ('AUTO_CUSTODY', 'SCRIPT_CUSTODY'), 'A59')
    add('F27_route_a_swap_to_nodes_worker', Z, 'MUST_FAIL', lambda r, n, d: wj(req(n, 'route_a'), dict(rj(req(n, 'route_a')), script=str(drv.NODES_ROUTE_A['worker_parallel'][0]),
                                                                                                   script_sha256=drv.NODES_ROUTE_A['worker_parallel'][1])), ('AUTO_CUSTODY',))
    add('F28_new_driver_is_declared_reference_driver_not_pinned', B, 'MUST_FAIL', lambda r, n, d: wj(n / 'start.json', dict(rj(n / 'start.json'), driver=EXT[0], driver_sha256=EXT[1])),
        ('AUTO_CUSTODY', 'NEW_DRIVER_PIN'))

    def undecl_ref_driver(r, n, d):
        wj(r / 'start.json', dict(rj(r / 'start.json'), driver='/x/galaxy_m0_forward_c2v008.py', driver_sha256='a' * 64))
        t = d / 'TOKENS_DRV.json'
        wj(t, {'declared': [['/x/galaxy_m0_forward_c2v008.py', D[0], '<D>'], ['a' * 64, D[1], '<DS>']]})
        return {'tokens': t}
    add('F29_undeclared_ref_driver_hidden_by_declared_token', B, 'MUST_FAIL', undecl_ref_driver, ('AUTO_CUSTODY',))

    def solver_swap(r, n, d):
        a, b = rj(req(r, 'route_a')), rj(req(n, 'route_a'))
        a['argv'] = a['argv'] + ['--solver', str(t8['PARALLEL_ROUTE_A']['solver'][0]), '--solver-sha256', t8['PARALLEL_ROUTE_A']['solver'][1]]
        b['argv'] = b['argv'] + ['--solver', 'X' + str(te['PARALLEL_ROUTE_A']['solver'][0]), '--solver-sha256', 'f' * 64]
        wj(req(r, 'route_a'), a); wj(req(n, 'route_a'), b)
    add('F30_route_a_solver_swap_not_in_driver_map', Z, 'MUST_FAIL', solver_swap, ('AUTO_CUSTODY',))
    add('Q01_inputs_json_content_changed', B, 'MUST_FAIL', lambda r, n, d: [wj(r / 'inputs/seed_c2v001.json', {'source_rtol': 0.01}),
                                                                           wj(n / 'inputs/seed_c2v001.json', {'source_rtol': 0.5})], ('FILES_INPUTS',), 'checker probe; S3')

    def q02(r, n, d):
        for run, v in ((r, 0.01), (n, 0.5)):
            wj(run / 'inputs/seed_c2v001.json', {'source_rtol': v})
            q = rj(req(run)); q['argv'] = q['argv'] + ['--seed', str(run / 'inputs/seed_c2v001.json'), '--seed-sha256', sha(run / 'inputs/seed_c2v001.json')]
            wj(req(run), q)
    add('Q02_inputs_change_referenced_by_sha_in_request', B, 'MUST_FAIL', q02, ('FILES_INPUTS',), 'checker probe; S3')
    add('Q03_toplevel_finish_changed', B, 'MUST_FAIL', lambda r, n, d: [wj(r / 'finish.json', {'status': 'COMPLETED', 'result_sha256': 'a' * 64}),
                                                                       wj(n / 'finish.json', {'status': 'FAILED', 'result_sha256': 'b' * 64})], ('FILES_TOP',), 'checker probe; S3')
    add('Q04_route_a_attempt_result_changed', Z, 'MUST_FAIL', lambda r, n, d: [
        wj(sdir(r, 'route_a') / 'attempt_000/result.json', {'outcome': 'CONVERGED_FINITE_FIXED_POINT', 'speeds': [1.0]}),
        wj(sdir(n, 'route_a') / 'attempt_000/result.json', {'outcome': 'NOT_CONVERGED', 'speeds': [9.0]})], ('FILES_ROUTE_A',), 'checker probe; S3')

    def strip_block(r, n, d):
        q = rj(req(n)); q['argv'] = rj(req(r))['argv']; wj(req(n), q)
    add('Q05_Z2_uvt_stage_without_any_tail_flag', Z, 'MUST_FAIL', strip_block, ('REQUEST',), 'checker probe; S2 (required)')
    add('P01_stage_json_reformatted_key_order', B, 'MUST_PASS', lambda r, n, d: wj(fin(n), dict(reversed(list(rj(fin(n)).items()))), indent=None))

    def recompress(r, n, d):
        p = sdir(n, 'reference') / 'reference/arrays.npz'
        with np.load(p, allow_pickle=False) as f:
            arrs = {k: np.array(f[k]) for k in f.files}
        p.unlink()
        with open(p, 'xb') as f:
            np.savez_compressed(f, **arrs)
    add('P02_npz_recompressed_same_arrays', B, 'MUST_PASS', recompress)
    add('P03_stage_renumbered', B, 'MUST_PASS', lambda r, n, d: sdir(n, 'reference').rename(n / 'stages/05_reference'))

    def masked(r, n, d):
        for run, v in ((r, 1.0), (n, 2.0)):
            o = rj(fin(run)); o['elapsed_seconds'] = v; o['utc'] = 'T%s' % v; wj(fin(run), o)
    add('P04_masked_keys_differ', B, 'MUST_PASS', masked)

    def nan_both(r, n, d):
        for run in (r, n):
            o = rj(fin(run)); o['nested']['nan_probe'] = float('nan'); wj(fin(run), o)
    add('P05_nan_equal_both_sides', B, 'MUST_PASS', nan_both)
    add('P06_Z2_reference_swap_v008_to_driver_uvt_declared', Z, 'MUST_PASS', lambda r, n, d: [swap(r, t8['SCRIPTS']['reference']), swap(n, drv.SCRIPTS_UVT['reference'])])

    def ref_on_driver(r, n, d):
        wj(r / 'start.json', dict(rj(r / 'start.json'), driver=D[0], driver_sha256=D[1]))
        res_set(r, lambda o: o.__setitem__('driver_sha256', D[1]))
        swap(r, drv.SCRIPTS['reference'])
        base = rj(tokdir / ('TOKENS_Z2_REPLACE_%s_C2V005.json' % dkey.upper()))
        t = d / 'TOKENS_P07.json'
        wj(t, {'declared': [[str(drv.SCRIPTS['reference'][0]), str(drv.SCRIPTS_UVT['reference'][0]), '<P07_PATH>'],
                            [drv.SCRIPTS['reference'][1], drv.SCRIPTS_UVT['reference'][1], '<P07_SHA>']] + base['declared']})
        return {'tokens': t}
    add('P07_Z2_reference_run_on_the_driver_itself', Z, 'MUST_PASS', ref_on_driver,
        note='the driver is a REFERENCE_DRIVER; route A PARALLEL worker -> RO1 worker_parallel; reference base -> successor declared')
    add('P08_Z2_declared_sidecar_file', Z, 'MUST_PASS', lambda r, n, d: wj(sdir(n, 'route_a') / 'uv_tail_sidecar/iteration_0000.json', {'x': 1}))
    add('P09_Z2_fs_feedback_stage_without_tail_flags', Z, 'MUST_PASS', lambda r, n, d: fs_feedback(r, n, d, False), note='S2 control')

    # ======== own cases
    def append_tokens(d, kinds=('reference',)):
        base = rj(tokdir / ('TOKENS_Z2_REPLACE_%s_C2V005.json' % dkey.upper()))['declared']
        app = rj(APPEND_Z2[0])['declared'][:50] if dkey == 'r4' else None
        extra = []
        for k in kinds:
            for t in base:
                if t[1] == str(drv.SCRIPTS_UVT[k][0]):
                    extra.append([t[0], str(drv.SCRIPTS[k][0]), t[2]])
                if t[1] == drv.SCRIPTS_UVT[k][1]:
                    extra.append([t[0], drv.SCRIPTS[k][1], t[2]])
        p = d / 'TOKENS_APPEND.json'
        wj(p, {'declared': base + extra})
        return {'tokens': p}
    add('N01_A59_append_mode_tokens_refused', Z, 'MUST_FAIL', lambda r, n, d: append_tokens(d), ('TOKENS_POLICY',), 'A59')

    def f1_hole(r, n, d):
        swap(n, drv.SCRIPTS['reference'])
        return append_tokens(d)
    add('N02_A59_F1_hole_base_ran_under_append_tokens', Z, 'MUST_FAIL', f1_hole, ('TOKENS_POLICY', 'SCRIPT_CUSTODY', 'AUTO_CUSTODY'), 'A59 F1')

    def off_succ(r, n, d):
        t = d / 'TOKENS_OFF_SUCC.json'
        wj(t, {'declared': [['x', str(drv.SCRIPTS_UVT['body'][0]), '<X>']]})
        return {'tokens': t}
    add('N03_tail_off_token_to_successor', B, 'MUST_FAIL', off_succ, ('TOKENS_POLICY',))
    add('N04_unnumbered_stage_dir', B, 'MUST_FAIL', lambda r, n, d: shutil.copytree(sdir(n, 'reference'), n / 'stages/reference_extra') and None, ('STAGE_SET', 'INVENTORY'), 'B1')

    def dup_number(r, n, d):
        shutil.copytree(sdir(r, 'reference'), r / 'stages/03_body')
        shutil.copytree(sdir(n, 'reference'), n / 'stages/02_body')
    add('N05_duplicate_stage_number_distinct_names', B, 'MUST_FAIL', dup_number, ('STAGE_SET',), 'B1')

    def order(r, n, d):
        shutil.copytree(sdir(r, 'reference'), r / 'stages/03_body')
        os.rename(sdir(n, 'reference'), n / 'stages/03_reference')
        shutil.copytree(n / 'stages/03_reference', n / 'stages/02_body')
    add('N06_stage_order_swapped', B, 'MUST_FAIL', order, ('STAGE_SET',), 'B1')
    add('N07_symlink_in_new', B, 'MUST_FAIL', lambda r, n, d: os.symlink('finish.json', sdir(n, 'reference') / 'reference/link.json'), ('INVENTORY',))
    add('N08_Z2_manifest_stage_missing', Z, 'MUST_FAIL', lambda r, n, d: shutil.rmtree(sdir(n, 'route_a_tail_manifest')), ('STAGE_SET', 'MANIFEST_STAGE'))

    def man_after(r, n, d):
        os.rename(sdir(n, 'route_a_tail_manifest'), n / 'stages/04_route_a_tail_manifest')
    add('N09_Z2_manifest_stage_not_after_route_a', Z, 'MUST_FAIL', man_after, ('STAGE_SET',))
    add('N10_Z2_manifest_wrong_script', Z, 'MUST_FAIL', lambda r, n, d: wj(req(n, 'route_a_tail_manifest'), dict(rj(req(n, 'route_a_tail_manifest')),
                                                                                                         script=str(drv.SCRIPTS_UVT['body'][0]), script_sha256=drv.SCRIPTS_UVT['body'][1])),
        ('MANIFEST_STAGE', 'SCRIPT_CUSTODY'))
    add('N11_Z2_truncation_flag_on_reference', Z, 'MUST_FAIL', lambda r, n, d: wj(req(n), dict(rj(req(n)), argv=rj(req(n))['argv'] + ['--uv-tail-truncation', '{}'])), ('REQUEST',), 'S2')

    def wrong_sha(r, n, d):
        q = rj(req(n)); a = q['argv']; i = a.index('--uv-tail-config-sha256'); a[i + 1] = sha(n / 'inputs/uv_tail_route_a_request.json'); wj(req(n), q)
    add('N12_Z2_config_sha_of_another_file', Z, 'MUST_FAIL', wrong_sha, ('REQUEST',), 'S2 values')

    def no_test_only(r, n, d):
        q = rj(req(n)); q['argv'].remove('--uv-tail-admit-test-only'); wj(req(n), q)
    add('N13_Z2_test_only_flag_missing', Z, 'MUST_FAIL', no_test_only, ('REQUEST',), 'S2')

    def stage_records(r, n, d, bad):
        for run in (r, n):
            recs = []
            for st in sorted((run / 'stages').iterdir()):
                q = rj(st / 'request.json')
                q['name'] = st.name[3:]  # driver requests carry their name (L1821); the synthetic ones did not
                wj(st / 'request.json', q)
                recs.append(dict(q, name=st.name[3:], executed=True, exit_code=0, request_path=str(st / 'request.json'),
                                 request_sha256=sha(st / 'request.json'), stage_dir=str(st), elapsed_seconds=1.0))
            res_set(run, lambda o: o.__setitem__('stage_records', recs))
        if bad:
            res_set(n, lambda o: o['stage_records'][0].__setitem__('argv', ['--tolerance', '0.5']))
    add('N14_stage_record_differs_from_own_request', B, 'MUST_FAIL', lambda r, n, d: stage_records(r, n, d, True), ('STAGE_RECORDS',), 'B2')
    add('N15_stage_records_consistent', B, 'MUST_PASS', lambda r, n, d: stage_records(r, n, d, False))
    add('N16_checkpoint_lock_differs', Z, 'MUST_FAIL', lambda r, n, d: [(sdir(r, 'route_a') / 'checkpoint/checkpoint.lock').write_bytes(b''),
                                                                       (sdir(n, 'route_a') / 'checkpoint/checkpoint.lock').write_bytes(b'x')], ('FILES_ROUTE_A',), 'S3')
    add('N17_attempt_finish_differs', Z, 'MUST_FAIL', lambda r, n, d: [wj(sdir(r, 'route_a') / 'attempt_000/finish.json', {'status': 'RETURNED_ACTUAL_RESULT'}),
                                                                      wj(sdir(n, 'route_a') / 'attempt_000/finish.json', {'status': 'FAILED'})], ('FILES_ROUTE_A',), 'S3')

    def att_pin(r, n, d, side):
        p = sdir(n if side == 'new' else r, 'route_a') / 'attempt_000/start.json'
        o = rj(p); o['input_pins']['/x/undeclared.py'] = 'd' * 64; wj(p, o)
    add('N18_attempt_undeclared_new_only_pin', Z, 'MUST_FAIL', lambda r, n, d: att_pin(r, n, d, 'new'), ('FILES_ROUTE_A',), 'S3 pins')
    add('N19_attempt_reference_only_pin', Z, 'MUST_FAIL', lambda r, n, d: att_pin(r, n, d, 'ref'), ('FILES_ROUTE_A',), 'S3 pins')

    def call_spec(r, n, d, leaf):
        for run, lab, v in ((r, 'REF LABEL', 1), (n, 'NEW LABEL', 2 if leaf else 1)):
            wj(run / 'inputs/call_spec.json', {'label': lab, 'numerics': {'x': v}})
    add('N20_call_spec_label_only_differs', B, 'MUST_PASS', lambda r, n, d: call_spec(r, n, d, False), note='declared MASK /label')
    add('N21_call_spec_leaf_differs', B, 'MUST_FAIL', lambda r, n, d: call_spec(r, n, d, True), ('FILES_INPUTS',))

    def ledger(r, n, d, same):
        for run, tok in ((r, '01792270475919883000-66829-703fbf7e'), (n, '01792317277062886000-23453-17301d17')):
            a = sdir(run, 'route_a') / 'checkpoint/attempts'
            wj(a / ('%s.start.json' % tok), {'attempt': tok, 'pid': 1, 'kind': 'start'})
            wj(a / ('%s.end.json' % tok), {'attempt': tok, 'kind': 'end', 'status': 'OK' if (same or run == r) else 'KILLED'})
            res_set(run, lambda o: o.setdefault('identity', {}).__setitem__('attempt_link', {'attempt': tok, 'end_record': str(a / ('%s.end.json' % tok))}))
    add('N22_attempt_tokens_differ_content_equal', Z, 'MUST_PASS', lambda r, n, d: ledger(r, n, d, True), note='ledger tokens paired')
    add('N23_attempt_ledger_content_differs', Z, 'MUST_FAIL', lambda r, n, d: ledger(r, n, d, False), ('ATTEMPT_LEDGER',))

    def progress(r, n, d, bad):
        for run, e in ((r, 1.0), (n, 2.0)):
            (run / 'progress.jsonl').write_text(json.dumps({'stage': 'reference', 'event': 'started'}) + '\n' +
                                                json.dumps({'stage': 'reference', 'event': 'finished', 'exit_code': 1 if (bad and run == n) else 0, 'elapsed': e}) + '\n')
    add('N24_progress_elapsed_only_differs', B, 'MUST_PASS', lambda r, n, d: progress(r, n, d, False))
    add('N25_progress_event_differs', B, 'MUST_FAIL', lambda r, n, d: progress(r, n, d, True), ('FILES_TOP',))

    def static(r, n, d, kind):
        good = str(drv.SCRIPTS['reference'][0])
        sr_, sn_ = rj(r / 'start.json'), rj(n / 'start.json')
        sr_['static_pins'], sn_['static_pins'] = {}, {}
        if kind == 'good':
            sn_['static_pins'][good] = drv.SCRIPTS['reference'][1]
        elif kind == 'bogus':
            sn_['static_pins'][good] = 'f' * 64
        else:
            sr_['static_pins'][good] = drv.SCRIPTS['reference'][1]
        wj(r / 'start.json', sr_); wj(n / 'start.json', sn_)
    add('N26_static_pin_new_only_verified_from_bytes', B, 'MUST_PASS', lambda r, n, d: static(r, n, d, 'good'))
    add('N27_static_pin_new_only_bogus_sha', B, 'MUST_FAIL', lambda r, n, d: static(r, n, d, 'bogus'), ('FILES_TOP',))
    add('N28_static_pin_reference_only', B, 'MUST_FAIL', lambda r, n, d: static(r, n, d, 'refonly'), ('FILES_TOP',))
    add('N29_result_driver_sha_not_pinned', B, 'MUST_FAIL', lambda r, n, d: res_set(n, lambda o: o.__setitem__('driver_sha256', EXT[1])), ('NEW_DRIVER_PIN',), 'A67 N1')

    def impl(r, n, d, newkind):
        res_set(r, lambda o: o.setdefault('identity', {}).setdefault('route_a', {}).__setitem__('implementation', {'kind': 'PARALLEL_C2V001'}))
        res_set(n, lambda o: o.setdefault('identity', {}).setdefault('route_a', {}).__setitem__('implementation', {'kind': newkind}))
    add('N30_Z2_impl_kind_wrong_pair', Z, 'MUST_FAIL', lambda r, n, d: impl(r, n, d, 'TAIL_OFF_RO1_PARALLEL_C2V010R4'), ('RESULT',), 'declared PAIR')
    add('N31_Z2_impl_kind_declared_pair', Z, 'MUST_PASS', lambda r, n, d: impl(r, n, d, 'UVTAIL_RO1_PARALLEL_C2V001'))

    def ro1_mismatch(r, n, d):
        def f(o):
            b = copy.deepcopy(o['route_a_outcome']['ro1']); b['fired'] = True
            o.setdefault('identity', {}).setdefault('route_a', {})['outcome'] = {'ro1': b}
        res_set(n, f)
    add('N32_Z2_identity_ro1_differs_from_outcome_ro1', Z, 'MUST_FAIL', ro1_mismatch, ('RESULT',))
    add('N33_Z2_uv_tail_record_not_test_only', Z, 'MUST_FAIL', lambda r, n, d: res_set(n, lambda o: o['uv_tail'].__setitem__('admissibility', 'production')), ('UV_TAIL_RECORD',))
    add('N34_B0P_ro1_armed', B, 'MUST_FAIL', lambda r, n, d: res_set(n, lambda o: o['route_a_outcome']['ro1'].__setitem__('armed', True)), ('RO1',))
    add('N35_Z2_baseline_compared_under_the_other_driver', Z, 'MUST_FAIL', None, ('NEW_DRIVER_PIN',), 'A67 N1', driver=other)
    add('N36_inputs_file_renamed', B, 'MUST_FAIL', lambda r, n, d: [wj(r / 'inputs/a.json', {'x': 1}), wj(n / 'inputs/b.json', {'x': 1})], ('INVENTORY',))
    add('N37_stage_dir_renamed', B, 'MUST_FAIL', lambda r, n, d: sdir(n, 'reference').rename(n / 'stages/02_reference2'), ('STAGE_SET', 'INVENTORY'))
    return cs


def run_cases(out, dkey, build, cs, tokdir):
    rows = []
    for c in cs:
        d = out / ('CASES_' + dkey) / c['tag']
        build(c['gate'], d)
        ref, new = (d / 'REF').resolve(), (d / 'NEW').resolve()
        tok = tokdir / ('TOKENS_Z2_REPLACE_%s_C2V005.json' % c['driver'].upper() if c['gate'] == 'Z2' else 'TOKENS_B0P_RERUN_C2V005.json')
        if c['gate'] == 'Z2' and c['driver'] != dkey:
            tok = tokdir / ('TOKENS_Z2_REPLACE_%s_C2V005.json' % dkey.upper())
        if c['mut'] is not None:
            r = c['mut'](ref, new, d)
            if isinstance(r, dict) and 'tokens' in r:
                tok = r['tokens']
        p = subprocess.run([PY, '-I', '-B', str(CMP), '--gate', c['gate'], '--driver', c['driver'], '--reference', str(ref), '--new', str(new),
                            '--tokens', str(tok), '--out', str(d / 'REPORT.json')], capture_output=True, text=True)
        if (d / 'REPORT.json').is_file():
            rep = rj(d / 'REPORT.json')
            verdict, failing = rep['verdict'], rep['failing']
        else:
            verdict, failing = 'REFUSED', [p.stderr.strip().splitlines()[-1][:300] if p.stderr.strip() else '']
        if c['expect'] == 'MUST_FAIL':
            ok = verdict == 'FAIL' and set(c['must_fail']) <= set(failing)
        else:
            ok = verdict == 'PASS_BITWISE_EQUAL'
        rows.append({'case': c['tag'], 'gate': c['gate'], 'driver': c['driver'], 'expect': c['expect'], 'must_fail': list(c['must_fail']),
                     'verdict': verdict, 'failing': failing, 'ok': ok, 'note': c['note']})
        print('%-6s %s %-56s %-9s %-18s %s' % ('ok' if ok else 'BREACH', dkey, c['tag'], c['expect'], verdict, failing), flush=True)
    return rows


# ---------------------------------------------------------------- part T
def part_tokens(tokdir):
    res = {}
    app = rj(APPEND_Z2[0])['declared']
    if sha(APPEND_Z2[0]) != APPEND_Z2[1]:
        raise SystemExit('append tokens pin')
    rep4 = rj(tokdir / 'TOKENS_Z2_REPLACE_R4_C2V005.json')['declared']
    c3 = rj('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v003/tokens/TOKENS_Z2_C2V003.json')['declared']
    appended = [tuple(t) for t in app[50:]]
    changed = [(tuple(a), tuple(b)) for a, b in zip(c3, rep4) if a != b]
    res['r4_appended_16_subset_of_replace'] = set(appended) <= {tuple(t) for t in rep4}
    res['r4_replace_changes_24_entries_new_side_only'] = len(changed) == 24 and all(a[0] == b[0] and a[2] == b[2] for a, b in changed)
    res['r4_replace_path_sha_changes_equal_appended'] = {b for a, b in changed if not b[1].endswith('.py') or b[1].startswith('/')} == set(appended)
    res['r4_unchanged_26'] = sum(1 for a, b in zip(c3, rep4) if a == b) == 26
    rep5 = rj(tokdir / 'TOKENS_Z2_REPLACE_R5_C2V005.json')['declared']
    ch5 = [(a, b) for a, b in zip(c3, rep5) if a != b]
    res['r5_replace_changes_24_entries_same_positions_as_r4'] = [i for i, (a, b) in enumerate(zip(c3, rep5)) if a != b] == [i for i, (a, b) in enumerate(zip(c3, rep4)) if a != b]
    res['r5_successors_are_r5_cascade_paths_or_shas'] = all(('driver_r5/cascade' in b[1]) or (len(b[1]) == 64) or b[1].endswith('_r5.py') for a, b in ch5)
    res['off_ro1_r4_r5_equal_c2v003'] = rj(tokdir / 'TOKENS_Z2_OFF_RO1_R4_C2V005.json')['declared'] == c3 == rj(tokdir / 'TOKENS_Z2_OFF_RO1_R5_C2V005.json')['declared']
    return res


# ---------------------------------------------------------------- part F
def part_fill(out):
    fm = load_mod(FILL, 'fill_c2v002_selftest')
    rows = []

    def row(tag, ok, det):
        rows.append({'case': tag, 'ok': bool(ok), 'detail': det})
        print('%-6s F %-60s %s' % ('ok' if ok else 'BREACH', tag, str(det)[:140]), flush=True)
    sc = (out / 'FILL').resolve()
    reg = sc / 'runs_ext/REGISTERED_RUN_V001'
    (reg / 'inputs').mkdir(parents=True)
    (sc / 'elsewhere').mkdir()
    os.symlink(str(reg / 'nonexistent_probe'), sc / 'elsewhere/link_abs')
    os.symlink('../runs_ext/REGISTERED_RUN_V001', sc / 'elsewhere/link_rel')
    os.symlink('link_rel', sc / 'elsewhere/link_chain')
    (sc / 'clean_run').mkdir()
    (sc / 'KMAX_A2F10_C5H_COPY').mkdir()
    for tag, path, want_refused in (('G1_direct_inside_registered', reg, True), ('G2_symlink_abs_to_nonexistent_inside', sc / 'elsewhere/link_abs', True),
                                    ('G3_symlink_relative_into_registered', sc / 'elsewhere/link_rel', True),
                                    ('G4_symlink_chain_into_registered', sc / 'elsewhere/link_chain', True),
                                    ('G5_dotdot_into_registered', sc / 'elsewhere/../runs_ext/./REGISTERED_RUN_V001/inputs', True),
                                    ('G6_case_variant_inside', Path(str(reg).replace('REGISTERED', 'registered')), True),
                                    ('G7_marker_name_elsewhere', sc / 'KMAX_A2F10_C5H_COPY', True),
                                    ('G8_clean_path', sc / 'clean_run', False)):
        real, why = fm.guarded_resolve(str(path), registered=str(reg))
        row(tag, (why is not None) == want_refused, {'path': str(path), 'refused': why, 'resolved': real})
    # CLI on the real registered name (string marker; nothing under it is stat-ed), and a scratch symlink whose target names it
    os.symlink(fm.C5H_REGISTERED + '/nonexistent_probe', sc / 'elsewhere/link_real_c5h')
    for tag, base in (('G9_cli_registered_c5h_path_string', fm.C5H_REGISTERED), ('G10_cli_symlink_target_names_c5h', str(sc / 'elsewhere/link_real_c5h'))):
        p = subprocess.run([PY, '-I', '-B', str(FILL), '--member-template', '/nonexistent', '--member-sha', 'x', '--base-template', '/nonexistent',
                            '--base-sha', 'x', '--base-run', base, '--out', str(sc / ('%s.json' % tag))], capture_output=True, text=True)
        msg = (p.stderr.strip().splitlines() or [''])[-1]
        row(tag, p.returncode != 0 and 'REFUSED: base run guard' in msg and 'MARKER' in msg and not (sc / ('%s.json' % tag)).exists(), msg[:200])
    # N2 type-exact T1 on a real registered member (C4T@RPAIR:T1_H/PICARD) and its base
    mk = load_mod(fm.MAKER[0], 'mk_selftest')
    regj = rj(G4 / 'specs/RPAIR_C2V002/SPECS_RPAIR_C2V002.json')
    m = next(s for s in regj['specs'] if s['key'] == 'C4T@RPAIR:T1_H/PICARD')
    mt, bt = rj(m['file']), rj(m['base']['path'])
    row('T1_real_member_passes', fm.t1_check(mk, bt, mt)[0], m['sha256'][:8])
    for tag, ptr, v in (('T1_column_workers_True_refused', ('numerics', 'route_a', 'column_workers'), True),
                        ('T1_column_workers_1.0_refused', ('numerics', 'route_a', 'column_workers'), 1.0),
                        ('T1_passes_12.0_refused', ('numerics', 'picard', 'passes'), 12.0),
                        ('T1_bound_as_str_refused', ('numerics', 'picard', 'speed_change_bound_km_s'), '0.0025')):
        x = copy.deepcopy(mt)
        o = x
        for k in ptr[:-1]:
            o = o[k]
        o[ptr[-1]] = v
        row(tag, not fm.t1_check(mk, bt, x)[0], {'leaf': '/'.join(ptr), 'value': repr(v)})
    # regression: the gates_v004 stand-ins re-filled byte-identically
    for s, want in (('S1_TAILON', 'c9a6d5cf08aa62c6c3ae2fb2ba99a75dacde13761d8b666abad6d5e2284623f0'),
                    ('S2_TAILOFF', 'd9e715e2dd5b8b2b65f6e2160a73ad4736bbe619c6515723d7d3da67eeeb9fe7')):
        fr = rj(G4 / ('specs/STANDIN_V002/STANDIN_%s_PICARD.FILLED.json.FILL_RECORD.json' % s))
        o = sc / ('REFILL_%s.json' % s)
        p = subprocess.run([PY, '-I', '-B', str(FILL), '--member-template', fr['member_template'][0], '--member-sha', fr['member_template'][1],
                            '--base-template', fr['base_template'][0], '--base-sha', fr['base_template'][1], '--base-run', fr['base_run'],
                            '--out', str(o)], capture_output=True, text=True)
        got = sha(o) if o.is_file() else None
        row('R_refill_%s_byte_identical' % s, got == want, {'sha256': got, 'expected': want, 'rc': p.returncode, 'err': p.stderr[-200:]})
    return rows


def main():
    out = Path(sys.argv[1]).resolve()
    out.mkdir(parents=True, exist_ok=False)
    tokdir = G5 / 'tokens'
    c5 = load_mod(CMP, 'c5_selftest')
    cm = c5.load_cm()
    t8, te = c5.driver_tables(V008[0]), c5.driver_tables(EXT[0])
    if sha(V008[0]) != V008[1] or sha(EXT[0]) != EXT[1]:
        raise SystemExit('reference driver pins')
    rep = {'schema': 'SELFTEST_C2V005', 'script': [str(Path(__file__).resolve()), sha(__file__)], 'comparator': [str(CMP), sha(CMP)],
           'fill_tool': [str(FILL), sha(FILL)], 'check_base_trees': str(CHECK_BASE), 'ported_from': list(CHECKER),
           'tokens': {p.name: sha(p) for p in sorted(tokdir.glob('*.json'))}, 'parts': {}}
    rep['parts']['T_tokens'] = part_tokens(tokdir)
    print('T', json.dumps(rep['parts']['T_tokens']), flush=True)
    allrows = []
    for dkey in ('r4', 'r5'):
        c5.DRIVER[:] = list(c5.DRIVERS[dkey])
        drv = c5.load_driver()
        build = (lambda gate, dst, dkey=dkey, drv=drv: build_tree(gate, dst, dkey, c5, drv, t8, cm))
        allrows += run_cases(out, dkey, build, cases(dkey, drv, t8, te, c5, tokdir), tokdir)
    rep['parts']['C_N_cases'] = allrows
    rep['parts']['F_fill'] = part_fill(out)
    ported = [r for r in allrows if r['case'][:1] in 'FPQ']
    own = [r for r in allrows if r['case'][:1] == 'N']
    rep['summary'] = {
        'tokens': all(rep['parts']['T_tokens'].values()),
        'ported_checker_must_fail_29': {d: [sum(1 for r in ported if r['driver'] == d and r['expect'] == 'MUST_FAIL' and r['case'][:1] == 'F' and r['case'] != 'F08_route_a_attempt_arrays_npy_changed' and r['ok']),
                                            sum(1 for r in ported if r['driver'] == d and r['expect'] == 'MUST_FAIL' and r['case'][:1] == 'F' and r['case'] != 'F08_route_a_attempt_arrays_npy_changed')] for d in ('r4', 'r5')},
        'ported_checker_must_pass_10': {d: [sum(1 for r in ported if r['driver'] == d and r['case'][:3] in ('P00', 'P01', 'P02', 'P03', 'P04', 'P05', 'P06', 'P07', 'P08') and r['ok']),
                                            sum(1 for r in ported if r['driver'] == d and r['case'][:3] in ('P00', 'P01', 'P02', 'P03', 'P04', 'P05', 'P06', 'P07', 'P08'))] for d in ('r4', 'r5')},
        'checker_probes_now_must_fail_6': {d: [sum(1 for r in ported if r['driver'] == d and (r['case'][:1] == 'Q' or r['case'].startswith('F08')) and r['ok']),
                                               sum(1 for r in ported if r['driver'] == d and (r['case'][:1] == 'Q' or r['case'].startswith('F08')))] for d in ('r4', 'r5')},
        'own_cases': {d: [sum(1 for r in allrows if r['driver'] == d and (r['case'][:1] == 'N' or r['case'].startswith('P09')) and r['ok']),
                          sum(1 for r in allrows if r['driver'] == d and (r['case'][:1] == 'N' or r['case'].startswith('P09')))] for d in ('r4', 'r5')},
        'fill': [sum(1 for r in rep['parts']['F_fill'] if r['ok']), len(rep['parts']['F_fill'])],
        'breaches': [(r['driver'], r['case']) for r in allrows if not r['ok']] + [('fill', r['case']) for r in rep['parts']['F_fill'] if not r['ok']],
    }
    rep['summary']['all_ok'] = rep['summary']['tokens'] and not rep['summary']['breaches']
    with open(out / 'SELFTEST_C2V005.json', 'x') as f:
        json.dump(rep, f, indent=1, default=str)
    print(json.dumps(rep['summary'], indent=1))


if __name__ == '__main__':
    main()
