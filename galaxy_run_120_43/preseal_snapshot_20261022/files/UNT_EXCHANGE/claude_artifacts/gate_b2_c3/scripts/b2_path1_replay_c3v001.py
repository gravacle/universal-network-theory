"""Claude3 gate B2 (dispatch 0597), PATH 1 = the PRODUCTION static rows, by single-stage static replays on saved states.

R1 B2 (KMAX_TAIL_PREREG_V007_DRAFT_R1 c691cab6 L120): "static rows on saved C2R3/C3R3/C4R3 le3 (rotation_v005 uvt successor +
unchanged column mean; continuum_v001, O = cube 12)".  Design V002 sec 4.4 (L559-563).

For each saved R3 state (result shas = r11 PIN_R3):
  ROT_ON  the rotation-v005 uvt successor that driver v010 r5 pins (SCRIPTS_UVT['rotation_v005'] 8459ce3c, binding 1e27430c,
          library owned_uv_tail_lapse_v002 2026f2b6, roster 4366e3d6, Jn d6c55b55), run on the saved le3 rotation inputs
          (stages/19_le3_rotation/request.json argv) through the r5 driver's own single-stage shim (`_stage request.json`:
          module patches + stage globals + argv, then the stage main; NOT `run`/`dry-run`), tail ON with the uv_tail block
          below, the tail source rotation = the le2 rotation the le2 feedback transformed (--uv-tail-source-rotation-directory).
  CM_ON   the UNCHANGED gal_c2v005 column-mean v004 stage (driver r5 SCRIPTS['column_mean_v004'] ae78b012) on ROT_ON's output
          and the saved le3 columns -> the 12 rows.
uv_tail block: the registered production C4T P128 M_s 128 block (template 088902fb, numerics.uv_tail, read from bytes) with
exactly two declared changes: outer -> {shape cube, K_out_inverse_kpc 12.0} (B2's O) and the two certificate fields ->
NONE_TEST_ONLY (a static replay is not production admissible, R1 IA6; --uv-tail-admit-test-only).  Everything else as
registered: continuum_v001, gas lagrange3_s_gl4 M_s 128, stars max16_ceil_kdr_plus8 / t_panels_40a_phase1p5_gl12,
quadrature order 8 / w_perp 0.05 / w_z 0.02, domain R 14.2 / z_eval 35 / z_src 32 kpc, lambda 1.0, lapse_only, jet orders.
Galaxy configs (gal_c2v005, schema V005): C3R3/C4R3 = their saved le3 configs with the V005 schema; C2R3 ran the reviewed base
stage (no config): C3R3's config with C2R3's values for exactly the per-call fields the stage uses (others dropped).
Writes only under gate_b2_c3/ (exclusive create).  Every process: taskpolicy -b, single-thread BLAS, <= 3 at once.
Usage: python3 -I -B b2_path1_replay_c3v001.py [STATE ...]   (default C2R3 C3R3 C4R3)
"""
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

GATE = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/gate_b2_c3')
EX = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
ROOT = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13')
RUNS = ROOT / 'CLAUDE2/runs'
PY = '/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
R5 = EX / 'tail_scheme_impl_c2/driver_r5'
CAS = R5 / 'cascade/tail_scheme_impl_c2'
PINS = {
    'driver_r5': (R5 / 'galaxy_m0_forward_c2v010.py', 'b5cc62afb7814b4f337a012a1ffd1f1e677f398ac18a1f8297c7ff49ae5374c6'),
    'rotation_v005_uvt_r5': (CAS / 'route_b/stages/ddo_free_surface_rotation_root_v005_gal_c2v005_uvt_c2v001_r5.py',
                             '8459ce3cbccb47e3b59f7cf08f33ce8565efae9dd6df8d79d35aa27782b24601'),
    'uvt_binding_r5': (CAS / 'route_b/uvt_route_b_binding_c2v001_r5.py', '1e27430c12cc84195b7642fe925bc6f9916a55158ecc02c9fbff9b8564506329'),
    'uvt_lib_v002': (R5 / 'module/owned_uv_tail_lapse_v002.py', '2026f2b6e21eba661ef97a5a2b6a8b73d0f8a2d5c3b995611c705f3dc6746a54'),
    'uvt_roster': (EX / 'tail_scheme_impl_c2/module/uv_tail_source_roster_c2v001.py', '4366e3d6ca717b6f25a6799fa60b8ce05561a70d39662d7b1f08b75fc2171ad2'),
    'uvt_jn': (EX / 'tail_scheme_impl_c2/module/posix_libm_bessel_jn_provider_c2v001.py', 'd6c55b55c701a7172e6eaf86ef3f0fedb7f5b2de32d3dbeb06c1bbee471d3171'),
    'column_mean_v004': (EX / 'stage_successor_gal_c2v005/stages/ddo12_lower_entropy_column_mean_root_v004_gal_c2v005.py',
                         'ae78b012d079ceffd62af1dbc8c59c4aaf97cbc30e697eca8b58cd03fb732d38'),
    'schema_v005': (EX / 'stage_successor_gal_c2v005/schema/GALAXY_CONFIG_SCHEMA_V005.json', 'f9b8d48eca10e5c8f2299c23dc1ac69c60c9f87bc24486024e675f7927bc042a'),
    'colmean_binding': (ROOT / 'CODEX1/DDO154_COLUMN_MEAN_REFERENCE_BINDING_V001.json', 'f42c7c657cd9b8bcef6b88e980918ff2570b1fc0a5480784d8bf3b8bb2a3c600'),
    'template_C4T_P128_MS128': (EX / 'v007_launch_packet_cx1/P128/specs/C4T_P128_MS128_CX1V003.TEMPLATE.json',
                                '088902fb6498f06528f87eb460294095abcae2471b0932a935e9b43564b4e785'),
}
STATES = {'C2R3': ('KMAX_A2F10_C2R3_D7R3_RUN_V001', '1f6b32a4edd0dd28438536165bdb10e13c8125eb5ccafb60ceb17315eba8c169'),
          'C3R3': ('KMAX_A2F10_C3R3_D7R3_RUN_V001', 'c9c802f44854d4f41f9e119707235899aba75a8bd42e89c19983f9ca9b817674'),
          'C4R3': ('KMAX_A2F10_C4R3_D7R3_RUN_V001', 'aac01962dc7bf08a7486179bc5674af520f7ea38d73b004154cdd2ff25fa8dee')}
ROT_PER_CALL_USED = ('custody.seed_sha256', 'custody.checkpoint_identity_sha256', 'custody.offset_finish_sha256', 'route_a.accepted_iteration')
THREADS = ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS', 'BLIS_NUM_THREADS')
MAXP = 3


def sha_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 22), b''):
            h.update(b)
    return h.hexdigest()


def pin(name):
    p, s = PINS[name]
    if sha_file(p) != s:
        raise SystemExit('PIN MISMATCH %s %s' % (name, p))
    return str(p), s


def inside_gate(p):
    p = Path(p).resolve()
    if GATE.resolve() not in p.parents:
        raise SystemExit('refusing to write outside gate_b2_c3: %s' % p)
    return p


def write_x(path, obj):
    path = inside_gate(path); path.parent.mkdir(parents=True, exist_ok=True)
    raw = (json.dumps(obj, indent=1, allow_nan=False) + '\n').encode()
    with open(path, 'xb') as f:
        f.write(raw)
    return str(path), hashlib.sha256(raw).hexdigest()


def arg(argv, key):
    return argv[argv.index(key) + 1]


def set_arg(argv, key, value):
    a = list(argv); a[a.index(key) + 1] = str(value); return a


def schema_v005():
    p, s = pin('schema_v005')
    return {'name': 'UNT_ROUTE_B_GALAXY_CONFIG_SCHEMA_V005', 'path': p, 'sha256': s}


def uv_tail_config():
    tp, _ = pin('template_C4T_P128_MS128')
    blk = json.loads(Path(tp).read_text())['numerics']['uv_tail']
    want = {'outer': {'K_big_inverse_kpc': 128.0, 'shape': 'cylinder'}, 'source_rule': 'continuum_v001',
            'gas': {'M_s': 128, 'interp': 'lagrange3_s_gl4'}, 'quadrature': {'order': 8, 'w_perp_max_inverse_kpc': 0.05, 'w_z_max_inverse_kpc': 0.02}}
    for k, v in want.items():
        if blk[k] != v:
            raise SystemExit('template block is not the registered production block: ' + k)
    changed = {'outer': (blk['outer'], {'shape': 'cube', 'K_out_inverse_kpc': 12.0}),
               'eps_certificate': (blk['eps_certificate'], 'NONE_TEST_ONLY'), 'lo_certificate': (blk['lo_certificate'], 'NONE_TEST_ONLY')}
    out = dict(blk)
    for k, (_, v) in changed.items():
        out[k] = v
    return out, {k: {'registered': a, 'b2_replay': b} for k, (a, b) in changed.items()}


def env():
    e = {k: v for k, v in os.environ.items() if not k.startswith('PYTHON')}
    for k in THREADS:
        e[k] = '1'
    return e


def launch(run_dir, req):
    run_dir = inside_gate(run_dir); run_dir.mkdir(parents=True, exist_ok=False)
    dp, _ = pin('driver_r5')
    rp, rs = write_x(run_dir / 'request.json', req)
    fo = open(run_dir / 'stdout.txt', 'x'); fe = open(run_dir / 'stderr.txt', 'x')
    cmd = ['taskpolicy', '-b', PY, '-I', '-B', dp, '_stage', rp]
    pr = subprocess.Popen(cmd, stdout=fo, stderr=fe, env=env(), cwd=str(run_dir))
    return dict(proc=pr, fo=fo, fe=fe, t0=time.monotonic(), run_dir=str(run_dir), request=rp, request_sha256=rs, cmd=cmd)


def run_jobs(jobs, log):
    pending = list(jobs); running = {}; done = {}
    while pending or running:
        for job in list(pending):
            key, rd, req, deps = job
            if len(running) >= MAXP:
                break
            if all(d in done for d in deps):
                pending.remove(job)
                if any(done[d].get('exit_code') != 0 for d in deps):
                    done[key] = dict(run_dir=str(rd), exit_code=None, skipped='dependency failed'); continue
                r = req() if callable(req) else req
                running[key] = launch(rd, r); log('started', key)
        time.sleep(5)
        for key in list(running):
            j = running[key]
            if j['proc'].poll() is not None:
                code = j['proc'].wait(); j['fo'].close(); j['fe'].close(); running.pop(key)
                done[key] = dict(run_dir=j['run_dir'], request=j['request'], request_sha256=j['request_sha256'], exit_code=code,
                                 elapsed_seconds=time.monotonic() - j['t0'], cmd=j['cmd'])
                log('finished', key, code, '%.0fs' % done[key]['elapsed_seconds'])
    return done


def rotation_request(state, cfg_path, cfg_sha, fx):
    run, rsha = STATES[state]; rd0 = RUNS / run
    if sha_file(rd0 / 'result.json') != rsha:
        raise SystemExit('R3 result pin ' + state)
    rreq = json.loads((rd0 / 'stages/19_le3_rotation/request.json').read_text())
    fbreq = json.loads((rd0 / 'stages/17_le2_feedback/request.json').read_text())
    src_rot = arg(fbreq['argv'], '--rotation-directory')
    argv = list(rreq['argv'])
    if '--galaxy-config' in argv:
        gc = json.loads(Path(arg(argv, '--galaxy-config')).read_text())
        if sha_file(arg(argv, '--galaxy-config')) != arg(argv, '--galaxy-config-sha256'):
            raise SystemExit('saved galaxy config pin ' + state)
        sg = dict(rreq['stage_globals']); how = 'saved le3 rotation galaxy config, schema -> V005'
    else:
        c3 = json.loads((RUNS / STATES['C3R3'][0] / 'stages/19_le3_rotation/request.json').read_text())
        gc = json.loads(Path(arg(c3['argv'], '--galaxy-config')).read_text())
        patch = rreq['module_patches'][0]['set']; cp = Path(arg(argv, '--checkpoint-directory'))
        its = sorted(int(p.name[10:]) for p in cp.glob('iteration_*'))
        vals = {'custody.seed_sha256': patch['SEED_SHA'], 'custody.checkpoint_identity_sha256': patch['IDENTITY'],
                'custody.offset_finish_sha256': rreq['stage_globals']['OFFSET_SHA'], 'route_a.accepted_iteration': its[-1]}
        gc['fields'] = {k: v for k, v in gc['fields'].items() if v['status'] != 'PER_CALL' or k in ROT_PER_CALL_USED}
        for k, v in vals.items():
            gc['fields'][k] = {'value': v, 'status': 'PER_CALL'}
        sg = {}; how = ('C2R3 ran the reviewed base rotation v005 (no config): C3R3 le3 config, PER_CALL fields reduced to the four the '
                        'stage uses, set to C2R3 values %s; stage_globals OFFSET_SHA -> config custody.offset_finish_sha256' % json.dumps(vals))
    gc['schema'] = schema_v005()
    gp, gs = write_x(fx / ('b2c3_galaxy_config_rotation_v005_%s.json' % state), gc)
    argv = set_arg(argv, '--outdir', 'PLACEHOLDER')
    if '--galaxy-config' in argv:
        argv = set_arg(set_arg(argv, '--galaxy-config', gp), '--galaxy-config-sha256', gs)
    else:
        argv += ['--galaxy-config', gp, '--galaxy-config-sha256', gs]
    argv += ['--uv-tail-config', cfg_path, '--uv-tail-config-sha256', cfg_sha, '--uv-tail-admit-test-only',
             '--uv-tail-source-rotation-directory', src_rot]
    sp, ss = pin('rotation_v005_uvt_r5')
    req = dict(name='le3_rotation', kind='rotation_v005', script=sp, script_sha256=ss, argv=argv, stage_globals=sg,
               module_patches=rreq['module_patches'], mask=rreq.get('mask'))
    info = dict(saved_request=str(rd0 / 'stages/19_le3_rotation/request.json'), saved_request_sha256=sha_file(rd0 / 'stages/19_le3_rotation/request.json'),
                saved_script=[rreq['script'], rreq['script_sha256']], galaxy_config=dict(path=gp, sha256=gs, how=how), source_rotation=src_rot,
                saved_column_mean=str(rd0 / 'stages/20_le3_column_mean/observation'), columns=str(rd0 / 'stages/18_le3_columns_00/columns'))
    return req, info


def column_mean_request(state, rot_out, fx, cols):
    run, _ = STATES[state]; rd0 = RUNS / run
    creq = json.loads((rd0 / 'stages/20_le3_column_mean/request.json').read_text())
    if '--galaxy-config' in creq['argv']:
        cmc = json.loads(Path(creq['argv'][-2]).read_text())
        if sha_file(creq['argv'][-2]) != creq['argv'][-1]:
            raise SystemExit('saved column-mean config pin ' + state)
    else:
        c3 = json.loads((RUNS / STATES['C3R3'][0] / 'stages/20_le3_column_mean/request.json').read_text())
        cmc = json.loads(Path(c3['argv'][-2]).read_text())
        cmc['fields'] = {k: v for k, v in cmc['fields'].items() if v['status'] != 'PER_CALL' or k == 'custody.column_mean_input_pins'}
    cmc['schema'] = schema_v005()
    bp, bs = pin('colmean_binding'); rot = Path(rot_out); cols = Path(cols)
    cmc['fields']['custody.column_mean_input_pins'] = {'status': 'PER_CALL', 'value': [
        [bp, bs], [str(rot / 'start.json'), sha_file(rot / 'start.json')], [str(rot / 'finish.json'), sha_file(rot / 'finish.json')],
        [str(cols / 'start.json'), sha_file(cols / 'start.json')], [str(cols / 'finish.json'), sha_file(cols / 'finish.json')]]}
    sp, ss = pin('rotation_v005_uvt_r5')
    cmc['producer_pins'] = {'rotation_worker': {'path': sp, 'sha256': ss}}
    p, s = write_x(fx / ('b2c3_galaxy_config_column_mean_%s.json' % state), cmc)
    cp, cs = pin('column_mean_v004')
    odir = GATE / 'out/path1' / ('%s_CM_ON' % state) / 'observation'
    return dict(name='le3_column_mean', kind='column_mean_v004', script=cp, script_sha256=cs,
                argv=['--outdir', str(odir), '--galaxy-config', p, s], stage_globals={}, module_patches=[], mask=None)


def main():
    t0 = time.time()
    states = sys.argv[1:] or ['C2R3', 'C3R3', 'C4R3']
    pins = {k: dict(zip(('path', 'sha256'), pin(k))) for k in PINS}
    fx = GATE / 'fixtures'
    cfg, changes = uv_tail_config()
    cfg_path, cfg_sha = write_x(fx / 'b2c3_uv_tail_cube12_P128MS128_testonly.json', cfg)
    log_lines = []

    def log(*a):
        s = ' '.join(str(x) for x in a) + ' %.0fs' % (time.time() - t0); print(s, flush=True); log_lines.append(s)
    jobs = []; meta = {}
    for st in states:
        req, info = rotation_request(st, cfg_path, cfg_sha, fx)
        rd = GATE / 'out/path1' / ('%s_ROT_ON' % st)
        req['argv'] = set_arg(req['argv'], '--outdir', str(rd / 'rotation'))
        meta[st] = dict(info, rotation_outdir=str(rd / 'rotation'))
        jobs.append(('%s_ROT_ON' % st, rd, req, []))
    for st in states:
        jobs.append(('%s_CM_ON' % st, GATE / 'out/path1' / ('%s_CM_ON' % st),
                     (lambda st=st: column_mean_request(st, meta[st]['rotation_outdir'], fx, meta[st]['columns'])), ['%s_ROT_ON' % st]))
    done = run_jobs(jobs, log)
    rec = dict(schema='CLAUDE3_B2_PATH1_REPLAY_C3V001', producer={'path': str(Path(__file__).resolve()), 'sha256': sha_file(__file__)},
               pins=pins, uv_tail_config=dict(path=cfg_path, sha256=cfg_sha, block=cfg, declared_changes_from_registered=changes),
               states={}, jobs=done, log=log_lines, seconds=time.time() - t0)
    for st in states:
        r = dict(meta[st])
        cm = done.get('%s_CM_ON' % st, {})
        if cm.get('exit_code') == 0:
            res = json.loads((GATE / 'out/path1' / ('%s_CM_ON' % st) / 'observation/result.json').read_text())
            r['rows_km_s'] = [row['speed_km_s'] for row in res['prediction']['rows']]
            r['row_ids'] = [row['id'] for row in res['prediction']['rows']]
            r['column_mean_status'] = res['status']
            fin = json.loads((Path(meta[st]['rotation_outdir']) / 'finish.json').read_text())
            r['rotation_finish_sha256'] = sha_file(Path(meta[st]['rotation_outdir']) / 'finish.json')
            r['rotation_arrays_sha256'] = fin['arrays_sha256']
            u = fin.get('uv_tail', {})
            r['uv_tail'] = {k: u.get(k) for k in ('state_digest', 'empty', 'i1t', 'kept', 'outer', 'quadrature', 'config_sha256',
                                                  'production_admissible', 'test_only_admitted', 'lineage', 'diagnostics')}
            r['column_mean_result_sha256'] = sha_file(GATE / 'out/path1' / ('%s_CM_ON' % st) / 'observation/result.json')
        rec['states'][st] = r
    p, s = write_x(GATE / 'out' / ('B2_PATH1_REPLAY_%s_C3V001.json' % '_'.join(states)), rec)
    log('wrote', p, s)


if __name__ == '__main__':
    main()
