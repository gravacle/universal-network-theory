"""s0_kit_c2v001.py -- the checks and custody records behind the S0 launch scripts (s0_launch_kit_c2, C2V001).

It launches nothing: it never starts root_monitor or the NGC driver, and it never reads a run's result.  The shell
scripts (launch_s0_serial_root_c2v001.sh, launch_twin_root_c2v001.sh, twin_kill_watch_c2v001.sh) call one subcommand per
step and act only on exit 0.  Exit codes: 0 pass, 3 refused, 4 written with an order/consistency flag, 1 'not yet'
(twin-trigger only), 2 usage.  Every file it writes is created exclusively ('x') and fsynced.

Subcommands (see each function's docstring):
  validate        args + every pin from bytes -> plan (shell assignments or JSON); writes nothing (except --emit json --out)
  fill-check      the filled serial/twin specs against the role's handoff, certificates and V006 SPEC_PIN
  dry-verdict     the fresh cx3r008 dry plan: blocker lists, not the readiness label (RI45-13 item 7)
  register        the per-point launch registry entry (exclusive create)
  admission       sched v003 NGC serial admission (pinned ngc_admission class + pinned gate decide) + the A133 memory rule
  gate-cli        synthetic-only emulation of machine_gate --hold-check / --twin-start-check (injected snapshot)
  ext1-check      External1 mount, path spelling, absent outputs, free space >= 136 GiB + 20 GiB (A143 D1)
  step2-check     step 2's last receipt exists (A135.5)
  watch-check     the V006 WATCH_PIN watch script verifies and is running (A135.5)
  order-check     after the M-15 step: seed serial first, one launch per registry name (A143 D2; r3a L454)
  freeze-check    V006 unchanged since the M-15 record while no launch receipt exists yet
  record-epoch    the M-15 record's date -u epoch second
  monitor-argv    validates the exact root_monitor argv the script will exec (D3 form) and prints it shell-quoted
  wave-state      root's wave/direct-batch attestation for the twin (A143 D2/D3)
  launch-record   checks <receipt>.launch.json against the plan and writes the launch record (exclusive create)
  twin-trigger    A141 L4: iteration_0001/COMPLETED.json and uv_tail_sidecar/iteration_0001.json both exist
  kill-target     verifies the twin's driver process group before a kill
  kill-record     writes the twin kill record (exclusive create)
"""
import argparse
import calendar
import hashlib
import json
import math
import os
import re
import shlex
import shutil
import subprocess
import sys
import time
import types
from pathlib import Path

KIT_DIR = Path(__file__).resolve().parent
RECORD_WRITER = ('s0_prelaunch_record_c2v001.py', 'a10965b7a508f106e3d153632d2b1a39a427d9106fa2de3c9e09d92b85bcb59a')
GATE_PINS = ('GATE_DOCUMENT_PINS_V001.json', 'afa1df05bf6329997adccf160dc6fd56534c59b914332c264c79512df1e7ce36')
PY = '/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
A = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/'
UNTPC = '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/'
GiB = 1 << 30
ROLES = ('seed', 'j0', 'j1', 'j2')
ROLE_NAME = {'seed': 'SEED', 'j0': 'J0', 'j1': 'J1', 'j2': 'J2'}
S0_ROLE = {'seed': 'seed', 'j0': 'jacobian_first_attempt_0', 'j1': 'jacobian_first_attempt_1', 'j2': 'jacobian_first_attempt_2'}
KEYS = {'seed': '968c915bece706ea1d6c0fa15357984884a87443e7c19eebd104230c9c961981',
        'j0': '3d7785669b549d6f9b9e0df65a3ad71de00c0da26a974c77ccb258856000fa60',
        'j1': 'ab7bf95317b37652282ac7da86931816955ce8a781279b79e1d5258689c3970c',
        'j2': '4b9b4ec88eb2d94ce2c8eeb52e2f7c5b5b7f96bdb5d4df52b9077ba06401f6a2'}
CAPS = {'serial': {'wall_cap_s': 610324, 'rss_cap_bytes': 34359738368, 'output_cap_bytes': 146028888064},
        'twin': {'wall_cap_s': 22752, 'rss_cap_bytes': 92341796864, 'output_cap_bytes': 34359738368}}
DISK_RESERVE_BYTES = 20 * GiB                     # A143 D1 per-start check: one output cap + 20 GiB
A133_LIMIT_GB, A133_SERIAL_PEAK_GB, A133_CAMPAIGN_RESERVE_GB = 103.0, 20.11, 29.1   # A133 section 1.4 in A141 L2 units
SERIAL_FILE, TWIN_FILE = 'CALL_A_K32_A2_HEADLINE_C2V001.json', 'CALL_A_K32_A2_HEADLINE_CW8_TWIN_C2V001.json'
FILL_RECEIPT = 'FILL_RECEIPT_C2V001.json'
LEAF = ('numerics', 'route_a', 'column_workers')
LAUNCH_SCHEMA = 'UNT_GALAXY_M0_MONITOR_RECEIPT_C2V001_LAUNCH'
HEX64 = re.compile(r'^[0-9a-f]{64}$')
P0 = A + 'ngc_point_producer_c4/s0/build_c4v001/out/'
REAL = {
    'v006': UNTPC + 'CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V006_ADDENDUM.md',
    'driver': {'path': A + 'ngc_cx3r008_closure_cx3/implementation/galaxy_m0_forward_c2v011_cx3v005_cx3r008_cx3v001.py',
               'sha256': '577f8c94366ae8f99c5387b87397a83020f8186dc523b987d042103283346377'},
    'monitor': {'path': A + 'galaxy_m0_forward_c2_0466/root_monitor_c2v001.py',
                'sha256': 'ba031c2340057d88ee399138cc645012a93aa7dc3eb7c9bba56d112c94a47107'},
    'filler': {'path': A + 'step5_path_c2/tools/fill_step5_c2v001.py',
               'sha256': 'ec417e76509427d8e942f52f02e9862a0277c90e3b92014c48b44a2efad61783'},
    'dry_harness': {'path': A + 'step5_path_c2/tools/dry_one_c2v001.py',
                    'sha256': 'aac20dd3ca18bb609b37216f552aeb5a6b9f37147e17fc5501ea3c8d0842596b'},
    'ngc_admission': {'path': A + 'sched_s45_c2/v003/ngc_admission_s45_c2v003.py',
                      'sha256': 'bdb44eeb807fd860a7f382526fba4b6c256ccffb29c6c6b4d129b4b6c14925f3'},
    'gate': {'path': A + 'sched_s45_c2/v003/machine_gate_s45_c2v003.py',
             'sha256': '736a3438b0a3af41eb8d7b2c764f25ff0f9e18942320a4542a9893b6b419f811'},
    'caps': {'path': A + 'sched_s45_c2/v003/CAPS_S45_C2V003.json',
             'sha256': '35f66b6a3152f985fe6edcbaeda2950e5b17e9f9f6026e5f6201052db1508f64'},
    's0_record': {'path': A + 'phase1_c2/S0_RECORD_ROOT_V001/S0_C2V001.json',
                  'sha256': '1be5ed709cdb49106652beb76baaafc1c257e760d8cda2c62c18ea6fb2e88143'},
    'policy': {'path': A + 'step5_path_c2/POLICY_C2V001.json',
               'sha256': '0c781a17548150831a7e10b8dd9d27897b856ab21398ee277fab3d2bbc4287e9'},
    'acceptance': {'path': A + 'review_ngc_v011_cx3r008_c4/REVIEW_NGC_V011_CX3R008_C4V001.md',
                   'sha256': '7ff20c1ded13513e5c0f5a386be8aa17825625a7b5a83cd2513b0693e0ab5c42'},
    'lo': {'path': A + 'tail_scheme_impl_c2/certificates_ngc_k32/gates/LO_NGC_K32_CERT_V001.json',
           'sha256': '07745bbf6d5c35d5a8568de7fc9e78b8c3bd8c3e371680dc8869c42a893c0382'},
    'gq_gate': {'path': A + 'ngc_ntest_eval_cx/out/GQ_NGC_91_MS96_V001.json',
                'sha256': 'be148bab4d80ef412d55d2011cac2e3a1d44725a0ba21a4d2bf43c7ffbdc1a76'},
    'eps': {'seed': {'path': P0 + 'S0_POINT_EPS_968c915bece706ea_C4V002_s0seed.json',
                     'sha256': 'efdc430a561ae936d860f85ec050f22a10f17c03aad7ad17fc2150744dcde563'},
            'j0': {'path': P0 + 'S0_POINT_EPS_3d7785669b549d6f_C4V002_s0j0.json',
                   'sha256': '8270b6b3eb9daddd01e32f7c6cc0fd143afd6b751ff9ced310ac92ca365586da'},
            'j1': {'path': P0 + 'S0_POINT_EPS_ab7bf95317b37652_C4V002_s0j1.json',
                   'sha256': 'bfac8f57233e904aed30f68594645b5b9c97697e47ce088e9d18e7a8fe4aff1e'},
            'j2': {'path': P0 + 'S0_POINT_EPS_4b9b4ec88eb2d94c_C4V002_s0j2.json',
                   'sha256': '5dd9900a7db31003cb1b1054c156f6ac73b062375bae3a423990e782a2ccfdfc'}},
    'gq': {'seed': {'path': P0 + 'S0_GQ_BINDING_968c915bece706ea_C4V002_gqseedA.json',
                    'sha256': '903a7d6c88804bb99175ec78927184f210fa1fb07c32c985c294ef0546d0b979'},
           'j0': {'path': P0 + 'S0_GQ_BINDING_3d7785669b549d6f_C4V002_gqj0A.json',
                  'sha256': 'cc6113ce39adaa3b24154848d099fec693aec15b91f09c3f9ca74299448d5f27'},
           'j1': {'path': P0 + 'S0_GQ_BINDING_ab7bf95317b37652_C4V002_gqj1A.json',
                  'sha256': '4fc1d744f2d0cb38a08d086aa8c20603bbd3b43c7c27a9a0d0d83665091402ca'},
           'j2': {'path': P0 + 'S0_GQ_BINDING_4b9b4ec88eb2d94c_C4V002_gqj2A.json',
                  'sha256': '934c0a4774b9153e7fbe25d72c743eff529079644f3fdc03ab060dc25833f3e0'}},
    'gate_pins': {'path': str(KIT_DIR / GATE_PINS[0]), 'sha256': GATE_PINS[1]},
    'external1_root': '/Volumes/External1',
    'python': PY,
}
SYNTHETIC_KEYS = ('schema', 'v006', 'driver', 'monitor', 'filler', 'dry_harness', 'ngc_admission', 'gate', 's0_record', 'policy',
                  'acceptance', 'lo', 'gq_gate', 'eps', 'gq', 'gate_pins', 'external1_root', 'python',
                  'external1_require_mount', 'free_bytes_override', 'snapshot', 'snapshot_after_twin')


class Refusal(ValueError):
    pass


def need(ok, why):
    if not ok:
        raise Refusal(why)


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for blk in iter(lambda: f.read(1 << 20), b''):
            h.update(blk)
    return h.hexdigest()


def date_u():
    r = subprocess.run(['/bin/date', '-u'], capture_output=True, text=True, env={'LC_ALL': 'C', 'PATH': '/usr/bin:/bin'},
                       timeout=10)
    return r.stdout.rstrip('\n')


def write_x(path, obj):
    path = Path(path)
    b = (json.dumps(obj, indent=1, sort_keys=True, allow_nan=False, default=str) + '\n').encode()
    fd = os.open(str(path), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o444)
    try:
        os.write(fd, b)
        os.fsync(fd)
    finally:
        os.close(fd)
    dfd = os.open(str(path.parent), os.O_RDONLY)
    try:
        os.fsync(dfd)
    finally:
        os.close(dfd)
    return sha_bytes(b)


def strict_json(b, what):
    def pairs(ps):
        d = {}
        for k, v in ps:
            need(k not in d, 'DUPLICATE_JSON_KEY %s %s' % (what, k))
            d[k] = v
        return d

    def bad(c):
        raise Refusal('NONFINITE_JSON %s %s' % (what, c))
    try:
        return json.loads(b, object_pairs_hook=pairs, parse_constant=bad)
    except (ValueError, UnicodeDecodeError) as e:
        raise Refusal('UNPARSEABLE_JSON %s (%s)' % (what, type(e).__name__)) from None


def is_pin(x):
    return type(x) is dict and set(x) == {'path', 'sha256'} and isinstance(x['path'], str) and \
        isinstance(x['sha256'], str) and bool(HEX64.match(x['sha256']))


def verify_pin(pin, what):
    need(is_pin(pin), 'PIN_FORM %s' % what)
    need(os.path.isabs(pin['path']), 'PIN_PATH_NOT_ABSOLUTE %s' % what)
    try:
        h = sha_file(pin['path'])
    except OSError as e:
        raise Refusal('PIN_FILE_UNREADABLE %s %s (%s)' % (what, pin['path'], type(e).__name__)) from None
    need(h == pin['sha256'], 'PIN_SHA_MISMATCH %s: expected %s, bytes %s' % (what, pin['sha256'], h))
    return pin


def load_module(pin, name):
    raw = Path(pin['path']).read_bytes()
    need(sha_bytes(raw) == pin['sha256'], 'MODULE_PIN_MISMATCH %s' % name)
    m = types.ModuleType(name)
    m.__file__ = pin['path']
    exec(compile(raw, pin['path'], 'exec'), m.__dict__)
    return m


def record_writer():
    return load_module({'path': str(KIT_DIR / RECORD_WRITER[0]), 'sha256': RECORD_WRITER[1]}, 's0_prelaunch_record_c2v001')


def dig(obj, keys):
    for k in keys:
        need(isinstance(obj, dict) and k in obj, 'MISSING_KEY %s' % '.'.join(keys))
        obj = obj[k]
    return obj


def canon(o):
    return json.dumps(o, sort_keys=True, separators=(',', ':'), allow_nan=False)


# ------------------------------------------------------------------------------------------------------------- plan
def path_rules(p, what):
    """No runs_ext link spelling, no uvt_ component, no UNT_INTERNAL_RUNS, no C5H marker, no ngc3198 component."""
    parts = [x for x in p.split('/') if x]
    low = p.lower()
    need('runs_ext' not in parts, '%s_SPELLED_THROUGH_RUNS_EXT' % what)
    need(not any(x.lower().startswith('uvt_') for x in parts), '%s_UVT_COMPONENT' % what)
    need('unt_internal_runs' not in low and 'kmax_a2f10_c5h' not in low, '%s_PROTECTED_TREE' % what)


def resolve_pins(a):
    if not a.synthetic_pins:
        need(not a.synthetic_pins_sha256, 'SYNTHETIC_SHA_WITHOUT_FILE')
        return dict(REAL), False, None
    need(os.path.isabs(a.synthetic_pins) and a.synthetic_pins_sha256, 'SYNTHETIC_PINS_FORM')
    raw = Path(a.synthetic_pins).read_bytes()
    need(sha_bytes(raw) == a.synthetic_pins_sha256, 'SYNTHETIC_PINS_SHA_MISMATCH')
    sp = strict_json(raw, 'synthetic pins')
    need(type(sp) is dict and set(sp) == set(SYNTHETIC_KEYS) and sp['schema'] == 'S0_LAUNCH_KIT_SYNTHETIC_PINS_C2V001',
         'SYNTHETIC_PINS_KEYS')
    # a synthetic run can never reach the real monitor or the real driver
    for k in ('driver', 'monitor'):
        need(sp[k]['sha256'] != REAL[k]['sha256'] and os.path.realpath(sp[k]['path']) != os.path.realpath(REAL[k]['path']),
             'SYNTHETIC_PINS_NAME_THE_REAL_%s' % k.upper())
    need(Path(sp['monitor']['path']).name != Path(REAL['monitor']['path']).name and
         not re.search(r'root_monitor_c2v\d+\.py', sp['monitor']['path']), 'SYNTHETIC_MONITOR_NAME_MATCHES_GATE_PATTERN')
    return sp, True, {'path': a.synthetic_pins, 'sha256': a.synthetic_pins_sha256}


def build_plan(a):
    need(a.role in ROLES, 'ROLE must be seed|j0|j1|j2')
    need(a.call in ('serial', 'twin'), 'CALL')
    need(a.mode in ('dry', 'launch'), 'MODE')
    need(not (a.call == 'twin' and a.role != 'seed'), 'TWIN_IS_AT_THE_SEED_ONLY')
    pins, synthetic, sp_pin = resolve_pins(a)
    ext1 = pins['external1_root']
    if synthetic and a.mode == 'launch':
        need(os.path.realpath(ext1) != os.path.realpath(REAL['external1_root']) and not ext1.startswith('/Volumes/'),
             'SYNTHETIC_LAUNCH_MUST_NOT_USE_EXTERNAL1')
    lr = a.launch_root
    need(isinstance(lr, str) and os.path.isabs(lr), 'LAUNCH_ROOT_NOT_ABSOLUTE')
    need(os.path.normpath(lr) == lr and Path(lr).is_dir() and os.path.realpath(lr) == lr, 'LAUNCH_ROOT_NOT_A_REAL_DIRECTORY')
    need(not lr.startswith('/Volumes/'), 'LAUNCH_ROOT_ON_AN_EXTERNAL_VOLUME')
    path_rules(lr, 'LAUNCH_ROOT')
    rr = a.run_root
    need(isinstance(rr, str) and os.path.isabs(rr), 'RUN_ROOT_NOT_ABSOLUTE')
    need(os.path.normpath(rr) == rr, 'RUN_ROOT_NOT_NORMAL')
    path_rules(rr, 'RUN_ROOT')
    need(rr.startswith(ext1.rstrip('/') + '/') and os.path.dirname(rr) == ext1.rstrip('/'),
         'RUN_ROOT_NOT_ONE_LEVEL_UNDER_%s' % ext1)
    rname = os.path.basename(rr)
    need(re.match(r'^NGC_[A-Za-z0-9_.-]+$', rname) is not None, 'RUN_ROOT_NAME_MUST_START_NGC_')
    need('ngc3198' not in rname.lower(), 'RUN_ROOT_NAME_HAS_NGC3198')
    nm = ROLE_NAME[a.role]
    run_name = 'NGC_P1_S0_%s_SERIAL_RUN_C2V001' % nm if a.call == 'serial' else 'NGC_P1_S0_SEED_CW8_TWIN_RUN_C2V001'
    outdir = rr + '/' + run_name
    receipt = outdir + '.receipt.json'
    reg_name = 'S0_%s_SERIAL' % nm if a.call == 'serial' else 'S0_SEED_CW8_TWIN'
    # every pin from bytes
    for k in ('driver', 'monitor', 'filler', 'dry_harness', 'ngc_admission', 'gate', 's0_record', 'policy', 'acceptance', 'lo',
              'gq_gate', 'gate_pins'):
        verify_pin(pins[k], k)
    verify_pin(pins['eps'][a.role], 'eps_' + a.role)
    verify_pin(pins['gq'][a.role], 'gq_' + a.role)
    caps = verify_pin(REAL['caps'], 'caps')
    cj = strict_json(Path(caps['path']).read_bytes(), 'caps')
    need({k: cj['ngc_s0_call_of_record'][k] for k in CAPS['serial']} == CAPS['serial'] and
         {k: cj['ngc_identity_twin'][k] for k in CAPS['twin']} == CAPS['twin'], 'CAPS_FILE_DIFFERS_FROM_KIT_CAPS')
    s0 = strict_json(Path(pins['s0_record']['path']).read_bytes(), 's0 record')
    pts = [p for p in s0.get('points') or [] if p.get('role') == S0_ROLE[a.role]]
    need(len(pts) == 1 and pts[0].get('key') == KEYS[a.role], 'S0_RECORD_HAS_NO_POINT_%s_WITH_KEY' % a.role)
    need(os.path.isabs(pins['python']) and Path(pins['python']).is_file(), 'PYTHON_MISSING')
    rw = record_writer()
    gp = verify_pin({'path': pins['gate_pins']['path'], 'sha256': pins['gate_pins']['sha256']}, 'gate_pins')
    v006 = pins['v006']
    need(os.path.isabs(v006), 'V006_NOT_ABSOLUTE')
    vraw = Path(v006).read_bytes()
    try:
        parsed = rw.parse_v006_pins(vraw)
    except rw.Refusal as e:
        raise Refusal('V006_PIN_LINES: %s' % e) from None
    P = parsed['pins']
    hand = P['HANDOFF_PIN'].get('S0_' + nm)
    spec_pin = P['SPEC_PIN'].get(reg_name)
    serial_pin = P['SPEC_PIN'].get('S0_%s_SERIAL' % nm)
    watch = P['WATCH_PIN'].get('MEMORY_WATCH')
    lrp = Path(lr)
    plan = {
        'schema': 'S0_LAUNCH_PLAN_C2V001', 'mode': a.mode, 'call': a.call, 'role': a.role, 'synthetic': synthetic,
        'synthetic_pins': sp_pin, 'python': pins['python'],
        'kit': {'dir': str(KIT_DIR), 'helper': {'path': str(Path(__file__).resolve()), 'sha256': sha_file(__file__)},
                'record_writer': {'path': str(KIT_DIR / RECORD_WRITER[0]), 'sha256': RECORD_WRITER[1]}, 'gate_pins': gp},
        'pins': {k: pins[k] for k in ('driver', 'monitor', 'filler', 'dry_harness', 'ngc_admission', 'gate', 's0_record',
                                      'policy', 'acceptance', 'lo', 'gq_gate')},
        'eps': pins['eps'][a.role], 'gq_binding': pins['gq'][a.role], 'caps_file': caps, 'caps': CAPS[a.call],
        'theta_key': KEYS[a.role],
        'names': {'handoff_pin': 'S0_' + nm, 'spec_pin': reg_name, 'serial_spec_pin': 'S0_%s_SERIAL' % nm,
                  'run_name': run_name, 'first_call': 'S0_SEED_SERIAL'},
        'launch_root': lr,
        'paths': {'record': str(lrp / 'M15_PRELAUNCH_RECORD_C2V001.json'),
                  'registry': str(lrp / 'registry' / ('%s_C2V001.json' % reg_name)),
                  'launch_record': str(lrp / 'launches' / ('%s_LAUNCH_C2V001.json' % reg_name)),
                  'seed_registry': str(lrp / 'registry' / 'S0_SEED_SERIAL_C2V001.json'),
                  'seed_launch_record': str(lrp / 'launches' / 'S0_SEED_SERIAL_LAUNCH_C2V001.json'),
                  'launches_dir': str(lrp / 'launches'), 'kill_dir': str(lrp / 'twin_kill')},
        'ext1_root': ext1, 'run_root': rr, 'outdir': outdir, 'receipt': receipt, 'launch_json': receipt + '.launch.json',
        'v006': {'path': v006, 'sha256_at_validate': sha_bytes(vraw)},
        'v006_pins': {'handoff': hand, 'spec': spec_pin, 'serial_spec': serial_pin, 'watch': watch},
        'synthetic_extras': ({k: pins[k] for k in ('external1_require_mount', 'free_bytes_override', 'snapshot',
                                                   'snapshot_after_twin')} if synthetic else None),
    }
    if a.mode == 'launch':
        need(hand is not None, 'V006_HAS_NO_HANDOFF_PIN %s (RI45-09)' % plan['names']['handoff_pin'])
        need(spec_pin is not None, 'V006_HAS_NO_SPEC_PIN %s (RI45-13)' % reg_name)
        need(watch is not None, 'V006_HAS_NO_WATCH_PIN MEMORY_WATCH (A135.5)')
    return plan


def cmd_validate(a):
    plan = build_plan(a)
    if a.emit == 'json':
        need(a.out, 'OUT_REQUIRED')
        h = write_x(a.out, plan)
        print(json.dumps({'status': 'PLAN_WRITTEN', 'path': a.out, 'sha256': h}))
        return 0
    hand = plan['v006_pins']['handoff'] or {}
    spec = plan['v006_pins']['spec'] or {}
    kv = {'PLAN_PY': plan['python'], 'PLAN_ROLE': plan['role'], 'PLAN_CALL': plan['call'], 'PLAN_SYNTHETIC': '1' if plan['synthetic'] else '0',
          'PLAN_V006': plan['v006']['path'], 'PLAN_DRIVER': plan['pins']['driver']['path'],
          'PLAN_DRIVER_SHA': plan['pins']['driver']['sha256'], 'PLAN_MONITOR': plan['pins']['monitor']['path'],
          'PLAN_MONITOR_SHA': plan['pins']['monitor']['sha256'], 'PLAN_FILLER': plan['pins']['filler']['path'],
          'PLAN_FILLER_SHA': plan['pins']['filler']['sha256'], 'PLAN_DRY': plan['pins']['dry_harness']['path'],
          'PLAN_DRY_SHA': plan['pins']['dry_harness']['sha256'], 'PLAN_GATE': plan['pins']['gate']['path'],
          'PLAN_GATE_SHA': plan['pins']['gate']['sha256'], 'PLAN_GATE_PINS': plan['kit']['gate_pins']['path'],
          'PLAN_GATE_PINS_SHA': plan['kit']['gate_pins']['sha256'], 'PLAN_RECORD': plan['paths']['record'],
          'PLAN_REGISTRY': plan['paths']['registry'], 'PLAN_LAUNCH_RECORD': plan['paths']['launch_record'],
          'PLAN_SEED_REGISTRY': plan['paths']['seed_registry'], 'PLAN_LAUNCHES_DIR': plan['paths']['launches_dir'],
          'PLAN_OUTDIR': plan['outdir'], 'PLAN_RECEIPT': plan['receipt'], 'PLAN_LAUNCH_JSON': plan['launch_json'],
          'PLAN_EXT1': plan['ext1_root'], 'PLAN_WALL': str(plan['caps']['wall_cap_s']), 'PLAN_RSS': str(plan['caps']['rss_cap_bytes']),
          'PLAN_OUTCAP': str(plan['caps']['output_cap_bytes']), 'PLAN_THETA_KEY': plan['theta_key'],
          'PLAN_FIRST_CALL': plan['names']['first_call'], 'PLAN_HANDOFF': hand.get('path', ''),
          'PLAN_HANDOFF_SHA': hand.get('sha256', ''), 'PLAN_SPEC_PIN_SHA': spec.get('sha256', ''),
          'PLAN_RUN_NAME': plan['names']['run_name']}
    for k, v in kv.items():
        print('%s=%s' % (k, shlex.quote(v)))
    return 0


def load_plan(path):
    raw = Path(path).read_bytes()
    plan = strict_json(raw, 'plan')
    need(plan.get('schema') == 'S0_LAUNCH_PLAN_C2V001', 'PLAN_SCHEMA')
    return plan


# ------------------------------------------------------------------------------------------------------------- fill
def strip_leaf(spec):
    s = json.loads(json.dumps(spec))
    node = s
    for k in LEAF[:-1]:
        node = node[k]
    v = node.pop(LEAF[-1])
    return s, v


def cmd_fill_check(a):
    """The filled specs against the role: handoff = the V006 HANDOFF_PIN (RI45-09) naming this theta key, the S0 record,
    the role's per-point EPS and LO 07745bbf; serial leaf 1, twin leaf 8, equal elsewhere; the launched spec's sha equal to
    its V006 SPEC_PIN (launch: required; dry: PENDING when absent, refused when it differs)."""
    plan = load_plan(a.plan)
    d = Path(a.fill_dir)
    need(d.is_absolute() and d.is_dir(), 'FILL_DIR')
    hp = plan['v006_pins']['handoff']
    need(hp is not None, 'NO_V006_HANDOFF_PIN')
    hb = Path(hp['path']).read_bytes()
    need(sha_bytes(hb) == hp['sha256'], 'HANDOFF_BYTES_DIFFER_FROM_V006_PIN')
    h = strict_json(hb, 'handoff')
    want_certs = {'eps_certificate': plan['eps'], 'lo_certificate': plan['pins']['lo']}
    checks = {
        'handoff_schema': h.get('schema') == 'UNT_STEP5_PHASE1_POINT_HANDOFF_C2V001',
        'handoff_mode': h.get('mode') == 'PHASE1_POINT',
        'handoff_point_key': h.get('point_key') == plan['theta_key'],
        'handoff_source_is_s0_record': h.get('source_pin') == plan['pins']['s0_record'],
        'handoff_certificates': h.get('certificate_pins') == want_certs,
        'handoff_driver_branch': h.get('driver_branch') == 'cx3r008',
        'handoff_root_admission': h.get('root_admission') == 'A133_PHASE1_POINT_THETA_FIXED_TARGET_FREE',
        'handoff_policy': h.get('policy_pin') == plan['pins']['policy'],
        'handoff_acceptance': h.get('driver_acceptance_pin') == plan['pins']['acceptance'],
        'handoff_v007_pin_form': is_pin(h.get('v007_adoption_pin')),
    }
    files = {}
    for n in (SERIAL_FILE, TWIN_FILE, FILL_RECEIPT):
        b = (d / n).read_bytes()
        files[n] = (b, strict_json(b, n))
    rc = files[FILL_RECEIPT][1]
    checks.update({
        'receipt_schema': rc.get('schema') == 'UNT_STEP5_FILLED_SPECS_C2V001',
        'receipt_not_authorizing': rc.get('launch_authorized') is False,
        'receipt_handoff_pin': rc.get('handoff_pin') == {'path': hp['path'], 'sha256': hp['sha256']},
        'receipt_theta_key': rc.get('theta_key') == plan['theta_key'],
        'receipt_no_pending_certificates': rc.get('pending_certificates') == [],
    })
    ser, tw = files[SERIAL_FILE][1], files[TWIN_FILE][1]
    label = 'step5 A_K32_A2_HEADLINE theta_key=%s' % plan['theta_key']
    for tag, s, cw in (('serial', ser, 1), ('twin', tw, 8)):
        try:
            checks[tag + '_leaf'] = dig(s, LEAF) == cw and type(dig(s, LEAF)) is int
            checks[tag + '_eps_certificate'] = dig(s, ('numerics', 'uv_tail', 'eps_certificate')) == plan['eps']
            checks[tag + '_lo_certificate'] = dig(s, ('numerics', 'uv_tail', 'lo_certificate')) == plan['pins']['lo']
            checks[tag + '_label'] = s.get('label') == label
        except Refusal:
            checks[tag + '_structure'] = False
    try:
        checks['pair_differs_only_in_leaf'] = canon(strip_leaf(ser)[0]) == canon(strip_leaf(tw)[0])
    except (KeyError, TypeError):
        checks['pair_differs_only_in_leaf'] = False
    shas = {n: sha_bytes(files[n][0]) for n in files}
    launch_file = SERIAL_FILE if plan['call'] == 'serial' else TWIN_FILE
    pin = plan['v006_pins']['spec']
    if pin is None:
        spec_status = 'PENDING_V006_SPEC_PIN'
        checks['spec_pin_present'] = plan['mode'] == 'dry'
    else:
        spec_status = 'MATCHES_V006' if pin['sha256'] == shas[launch_file] else 'DIFFERS_FROM_V006'
        checks['spec_sha_equals_v006_spec_pin'] = pin['sha256'] == shas[launch_file]
    if plan['call'] == 'twin':
        sp = plan['v006_pins']['serial_spec']
        checks['serial_of_same_fill_registered'] = (sp is not None and sp['sha256'] == shas[SERIAL_FILE]) or \
            (sp is None and plan['mode'] == 'dry')
    bad = sorted(k for k, v in checks.items() if not v)
    out = {'schema': 'S0_FILL_CHECK_C2V001', 'ok': not bad, 'failed': bad, 'checks': checks, 'date_u': date_u(),
           'fill_dir': str(d), 'serial': {'path': str(d / SERIAL_FILE), 'sha256': shas[SERIAL_FILE]},
           'twin': {'path': str(d / TWIN_FILE), 'sha256': shas[TWIN_FILE]},
           'fill_receipt': {'path': str(d / FILL_RECEIPT), 'sha256': shas[FILL_RECEIPT]},
           'launch_spec': {'path': str(d / launch_file), 'sha256': shas[launch_file]},
           'spec_pin_status': spec_status, 'v006_spec_pin': pin, 'v006_handoff_pin': hp,
           'certificates': {'eps': plan['eps'], 'lo': plan['pins']['lo'], 'gq_binding': plan['gq_binding'],
                            'gq_gate': plan['pins']['gq_gate']}}
    if a.out:
        write_x(a.out, out)
    print(json.dumps({k: out[k] for k in ('ok', 'failed', 'launch_spec', 'spec_pin_status')}))
    return 0 if out['ok'] else 3


# ------------------------------------------------------------------------------------------------------------- dry plan
def cmd_dry_verdict(a):
    """RI45-13 item 7: read the blocker lists, not the label.  Required: harness exit 0, no fence denial, Ctx simulate only,
    0 executed stages, binding_blockers [], source_build_blockers [], future dependencies only PENDING_ROUTE_A_OUTPUTS,
    planned_route_a true, and the log's driver/spec shas equal to the plan's."""
    plan = load_plan(a.plan)
    log = strict_json(Path(a.log).read_bytes(), 'dry log')
    rd = Path(a.report_dir)
    rdy = strict_json((rd / 'NGC_SOURCE_BUILD_READINESS.json').read_bytes(), 'readiness')
    deps = sorted({b.get('class') for b in rdy.get('future_stage_dependencies') or []})
    checks = {
        'harness_exit_0': log.get('exit') == 0,
        'no_fence_denial': log.get('blocked') == [],
        'ctx_simulate_only': bool(log.get('ctx_modes')) and set(log.get('ctx_modes')) == {'simulate'},
        'driver_sha': log.get('driver_sha256') == plan['pins']['driver']['sha256'],
        'spec_sha': log.get('spec_sha256') == a.spec_sha256 and sha_file(a.spec) == a.spec_sha256,
        'executed_stages_0': rdy.get('executed_stages') == 0,
        'binding_blockers_empty': rdy.get('binding_blockers') == [],
        'source_build_blockers_empty': rdy.get('source_build_blockers') == [],
        'future_deps_only_pending_route_a': set(deps) <= {'PENDING_ROUTE_A_OUTPUTS'},
        'planned_route_a': rdy.get('planned_route_a') is True,
    }
    bad = sorted(k for k, v in checks.items() if not v)
    out = {'schema': 'S0_DRY_VERDICT_C2V001', 'ok': not bad, 'failed': bad, 'checks': checks, 'date_u': date_u(),
           'log': {'path': a.log, 'sha256': sha_file(a.log)},
           'readiness': {'path': str(rd / 'NGC_SOURCE_BUILD_READINESS.json'),
                         'sha256': sha_file(rd / 'NGC_SOURCE_BUILD_READINESS.json')},
           'source_build_blockers': [b.get('class') for b in rdy.get('source_build_blockers') or []],
           'binding_blockers': rdy.get('binding_blockers'), 'future_stage_dependencies': deps,
           'readiness_label_ignored': rdy.get('readiness'), 'spec': {'path': a.spec, 'sha256': a.spec_sha256}}
    if a.out:
        write_x(a.out, out)
    print(json.dumps({k: out[k] for k in ('ok', 'failed', 'source_build_blockers', 'future_stage_dependencies')}))
    return 0 if out['ok'] else 3


def cmd_register(a):
    """The per-point launch registry entry (RI45-13 (a); A135 item 9), exclusive create in launch mode."""
    plan = load_plan(a.plan)
    fc = strict_json(Path(a.fill_check).read_bytes(), 'fill check')
    dv = strict_json(Path(a.dry_verdict).read_bytes(), 'dry verdict')
    need(fc['ok'] and dv['ok'], 'FILL_OR_DRY_NOT_OK')
    need(dv['spec']['sha256'] == fc['launch_spec']['sha256'], 'DRY_PLAN_OF_ANOTHER_SPEC')
    entry = {'schema': 'UNT_S0_LAUNCH_REGISTRY_ENTRY_C2V001', 'name': plan['names']['spec_pin'], 'role': plan['role'],
             'call': plan['call'], 'theta_key': plan['theta_key'], 'spec': fc['launch_spec'],
             'v006_spec_pin': fc['v006_spec_pin'], 'v006_handoff_pin': fc['v006_handoff_pin'],
             'pair': {'serial': fc['serial'], 'twin': fc['twin']}, 'fill_dir': fc['fill_dir'], 'fill_receipt': fc['fill_receipt'],
             'certificates': fc['certificates'], 's0_record': plan['pins']['s0_record'], 'driver': plan['pins']['driver'],
             'fill_check': {'path': a.fill_check, 'sha256': sha_file(a.fill_check)},
             'dry_verdict': {'path': a.dry_verdict, 'sha256': sha_file(a.dry_verdict)}, 'dry_log': dv['log'],
             'rule': 'RI45-13 (a): fresh dry plan with the real certificate pins, spec sha registered (V006 SPEC_PIN), driver '
                     'sha checked before launch', 'date_u': date_u(), 'synthetic': plan['synthetic']}
    if plan['mode'] != 'launch':
        print(json.dumps({'status': 'DRY_NOT_REGISTERED', 'would_write': plan['paths']['registry'], 'entry': entry}))
        return 0
    Path(plan['paths']['registry']).parent.mkdir(exist_ok=True)
    need(not os.path.lexists(plan['paths']['launch_record']), 'ALREADY_LAUNCHED %s' % plan['paths']['launch_record'])
    if os.path.lexists(plan['paths']['registry']):
        # a retry after a refusal at a later step (e.g. admission): the entry is never rewritten; it must name the same
        # spec bytes, theta and V006 pins, else refuse
        old = strict_json(Path(plan['paths']['registry']).read_bytes(), 'registry entry')
        same = (old.get('spec', {}).get('sha256') == entry['spec']['sha256'] and old.get('theta_key') == entry['theta_key']
                and old.get('v006_spec_pin') == entry['v006_spec_pin'] and old.get('v006_handoff_pin') == entry['v006_handoff_pin'])
        need(same, 'REGISTRY_ENTRY_EXISTS_FOR_ANOTHER_SPEC %s' % plan['paths']['registry'])
        print(json.dumps({'status': 'ALREADY_REGISTERED_SAME_SPEC', 'path': plan['paths']['registry'],
                          'sha256': sha_file(plan['paths']['registry'])}))
        return 0
    h = write_x(plan['paths']['registry'], entry)
    print(json.dumps({'status': 'REGISTERED', 'path': plan['paths']['registry'], 'sha256': h}))
    return 0


# ------------------------------------------------------------------------------------------------------------- gate
class FakeClock:
    def __init__(self):
        self.t = 1000.0

    def __call__(self):
        return self.t


def synthetic_snapshot(plan, key):
    ex = plan['synthetic_extras']
    need(plan['synthetic'] and ex and ex.get(key), 'SYNTHETIC_SNAPSHOT_ONLY')
    snap = strict_json(Path(ex[key]).read_bytes(), 'snapshot')
    snap['procs_cpu'] = {int(k): v for k, v in (snap.get('procs_cpu') or {}).items()}
    for r in snap.get('runs') or []:
        r['cpu_s'] = {int(k): v for k, v in (r.get('cpu_s') or {}).items()}
    return snap


def load_gate(plan):
    NA = load_module(plan['pins']['ngc_admission'], 'ngc_admission_s45_c2v003')
    need(NA.GATE_SHA256 == plan['pins']['gate']['sha256'] and os.path.realpath(NA.GATE_PATH) ==
         os.path.realpath(plan['pins']['gate']['path']), 'NGC_ADMISSION_GATE_PIN_DIFFERS')
    G = NA._load_pinned(NA.GATE_PATH, NA.GATE_SHA256, 's45_machine_gate_ngc')
    return NA, G


def make_gate(plan, G, snapshot_key, params=None):
    if plan['synthetic']:
        snap = synthetic_snapshot(plan, snapshot_key)
        clock = FakeClock()
        return G.Gate(params=params, probe_fn=lambda: snap, clock=clock), clock
    return G.Gate(params=params), None


def warm(gate, clock):
    gate.sample(force=True)
    if clock is not None:
        clock.t += gate.P['warmup_s'] + 1.0
    else:
        time.sleep(gate.P['warmup_s'])
    gate.sample(force=True)


def a133_memory_ok(live_runs_gb):
    """A133 section 1.4 in A141 L2 units: measured run footprint + 20.11 GB + 29.1 GB <= 103 GB (footprint <= 53.79 GB)."""
    return isinstance(live_runs_gb, (int, float)) and math.isfinite(live_runs_gb) and \
        live_runs_gb + A133_SERIAL_PEAK_GB + A133_CAMPAIGN_RESERVE_GB <= A133_LIMIT_GB + 1e-9


def cmd_admission(a):
    """sched v003 admission of one NGC serial call: ngc_admission_s45_c2v003's own wave-1 class (family NGC_SERIAL), its
    class/gate consistency checks, then the pinned gate's decide() on a warmed sample (spacing 600 s as the loop uses),
    plus the A133 memory rule.  Disk is ext1-check's.  Reads ps/top/sysctl/vm_stat through the gate (real mode)."""
    plan = load_plan(a.plan)
    need(plan['call'] == 'serial', 'ADMISSION_IS_FOR_THE_SERIAL_CALL (the twin uses --twin-start-check)')
    NA, G = load_gate(plan)
    raw = Path(a.spec).read_bytes()
    need(sha_bytes(raw) == a.spec_sha256, 'SPEC_SHA')
    cw = NA.spec_route_a_workers(raw)
    reasons = []
    if cw != 1:
        reasons.append('SPEC_NOT_SERIAL column_workers=%r' % (cw,))
    why_class = NA.class_matches_gate(G)
    if why_class:
        reasons.append('CLASS_MISMATCH: %s' % why_class)
    c1 = NA.PARAMS['class_wave1']
    head = NA.ngc_class(G, c1['res_route_a_gb'], c1['spike_gb'], NA.PARAMS)
    never = G.never_admissible(head, G.PARAMS)
    if never:
        reasons.append('NEVER_ADMISSIBLE: %s' % never)
    gate, clock = make_gate(plan, G, 'snapshot', params={'spacing_s': NA.PARAMS['spacing_s']})
    warm(gate, clock)
    d = gate.decide(owned={}, head=head, n_running=0, max_concurrent=NA.PARAMS['max_concurrent'], last_own_start=None)
    reasons += ['GATE_' + r for r in d['reasons']]
    mem_ok = a133_memory_ok(d.get('live_runs_gb'))
    if not mem_ok:
        reasons.append('A133_MEMORY: live run footprint %.2f GB + %.2f + %.2f > %.1f GB' % (
            d.get('live_runs_gb') or float('nan'), A133_SERIAL_PEAK_GB, A133_CAMPAIGN_RESERVE_GB, A133_LIMIT_GB))
    out = {'schema': 'S0_ADMISSION_C2V001', 'admit': not reasons, 'reasons': reasons, 'date_u': date_u(),
           'head': head, 'gate_decision': d, 'a133_memory_ok': mem_ok,
           'ngc_admission': plan['pins']['ngc_admission'], 'gate': plan['pins']['gate'], 'synthetic': plan['synthetic'],
           'spec': {'path': a.spec, 'sha256': a.spec_sha256},
           'note': 'ngc_admission_s45_c2v003 is an admission LOOP that launches; this check uses its class and the pinned gate '
                   'only, and root launches through root_monitor directly (its wave-1 wall cap 576,000 s differs from the '
                   'S0 cap 610,324 s).'}
    if a.out:
        write_x(a.out, out)
    print(json.dumps({'admit': out['admit'], 'reasons': reasons, 'live_runs_gb': d.get('live_runs_gb'),
                      'mem_after_admit_gb': d.get('mem_after_admit_gb')}))
    return 0 if out['admit'] else 3


def cmd_gate_cli(a):
    """Synthetic-only emulation of machine_gate_s45_c2v003 main(): --hold-check (0 clear, 3 hold, 2 probe failed) and
    --twin-start-check (0 admit, 3 refuse), on the pinned gate code with an injected snapshot."""
    plan = load_plan(a.plan)
    need(plan['synthetic'], 'GATE_CLI_EMULATION_IS_SYNTHETIC_ONLY: root runs the pinned gate CLI itself')
    _, G = load_gate(plan)
    gate, clock = make_gate(plan, G, a.snapshot_key)
    if a.which == 'hold':
        d = gate.hold_check()
        print(json.dumps({k: d[k] for k in ('hold', 'twins', 'probe_ok')}))
        return 2 if not d['probe_ok'] else (3 if d['hold'] else 0)
    warm(gate, clock)
    d = gate.twin_start()
    print(json.dumps({'admit': d['admit'], 'reasons': d['reasons']}))
    return 0 if d['admit'] else 3


# ------------------------------------------------------------------------------------------------------------- checks
def cmd_ext1_check(a):
    """External1 mounted (synthetic: a directory), no symlinked ancestor, the outputs absent, free >= cap + 20 GiB."""
    plan = load_plan(a.plan)
    ext1, rr = plan['ext1_root'], plan['run_root']
    ex = plan['synthetic_extras'] or {}
    reasons = []
    if plan['synthetic'] and ex.get('external1_require_mount') is False:
        if not Path(ext1).is_dir():
            reasons.append('EXTERNAL1_NOT_A_DIRECTORY')
    elif not os.path.ismount(ext1):
        reasons.append('EXTERNAL1_NOT_MOUNTED')
    if os.path.realpath(ext1) != ext1:
        reasons.append('EXTERNAL1_SYMLINKED')
    if os.path.lexists(rr) and (not Path(rr).is_dir() or os.path.realpath(rr) != rr):
        reasons.append('RUN_ROOT_NOT_A_REAL_DIRECTORY')
    for p in (plan['outdir'], plan['receipt'], plan['launch_json'], plan['receipt'] + '.stdout.txt',
              plan['receipt'] + '.stderr.txt'):
        if os.path.lexists(p):
            reasons.append('OUTPUT_EXISTS %s' % p)
    free = None
    if Path(ext1).is_dir():
        free = ex.get('free_bytes_override') if plan['synthetic'] and ex.get('free_bytes_override') is not None else \
            shutil.disk_usage(ext1).free
    need_bytes = plan['caps']['output_cap_bytes'] + DISK_RESERVE_BYTES
    if free is None or free < need_bytes:
        reasons.append('DISK_FREE %s < %d (output cap + 20 GiB, A143 D1)' % (free, need_bytes))
    out = {'schema': 'S0_EXT1_CHECK_C2V001', 'ok': not reasons, 'reasons': reasons, 'free_bytes': free,
           'required_bytes': need_bytes, 'outdir': plan['outdir'], 'receipt': plan['receipt'], 'date_u': date_u()}
    if a.out:
        write_x(a.out, out)
    print(json.dumps({'ok': out['ok'], 'reasons': reasons, 'free_bytes': free}))
    return 0 if out['ok'] else 3


def cmd_step2_check(a):
    """A135.5: step 2's last receipt exists (named by root); its sha256 is logged, its content is not interpreted."""
    plan = load_plan(a.plan)
    p = a.receipt
    ok = isinstance(p, str) and os.path.isabs(p) and Path(p).is_file()
    out = {'schema': 'S0_STEP2_CHECK_C2V001', 'ok': ok, 'receipt': p, 'sha256': sha_file(p) if ok else None,
           'date_u': date_u(), 'role': plan['role']}
    if a.out:
        write_x(a.out, out)
    print(json.dumps({'ok': ok, 'receipt': p}))
    return 0 if ok else 3


def cmd_watch_check(a):
    """A135.5: the V006 WATCH_PIN MEMORY_WATCH script verifies from bytes and a process running it exists (ps)."""
    plan = load_plan(a.plan)
    w = plan['v006_pins']['watch']
    reasons = []
    running = []
    if w is None:
        reasons.append('V006_HAS_NO_WATCH_PIN')
    else:
        try:
            if sha_file(w['path']) != w['sha256']:
                reasons.append('WATCH_SCRIPT_SHA_MISMATCH')
        except OSError:
            reasons.append('WATCH_SCRIPT_MISSING')
        ps = subprocess.run(['/bin/ps', '-ww', '-A', '-o', 'pid=,command='], capture_output=True, text=True, timeout=30).stdout
        running = [ln.strip() for ln in ps.splitlines() if w['path'] in ln]
        if not running:
            reasons.append('WATCH_NOT_RUNNING')
    out = {'schema': 'S0_WATCH_CHECK_C2V001', 'ok': not reasons, 'reasons': reasons, 'watch_pin': w,
           'running_processes': running[:5], 'date_u': date_u()}
    if a.out:
        write_x(a.out, out)
    print(json.dumps({'ok': out['ok'], 'reasons': reasons}))
    return 0 if out['ok'] else 3


def launches(plan):
    d = Path(plan['paths']['launches_dir'])
    return sorted(str(p) for p in d.iterdir()) if d.is_dir() else []


def cmd_order_check(a):
    """After the M-15 step (the shell script refuses earlier when the record is absent and this is not the seed serial,
    or when launch records exist without it): the record exists, seed serial first (A143 D2; r3a L454), one launch per
    name, and the twin only after the seed serial's launch record.  (A registry entry may exist from a refused attempt;
    register accepts it only for the same spec.)"""
    plan = load_plan(a.plan)
    P = plan['paths']
    rec, L = os.path.lexists(P['record']), launches(plan)
    reasons = []
    if not rec:
        reasons.append('M15_RECORD_MISSING')
    if os.path.lexists(P['launch_record']):
        reasons.append('LAUNCH_RECORD_EXISTS %s' % P['launch_record'])
    if not (plan['call'] == 'serial' and plan['role'] == 'seed') and not os.path.lexists(P['seed_launch_record']):
        reasons.append('SEED_SERIAL_NOT_LAUNCHED_FIRST')
    if plan['call'] == 'twin' and not os.path.lexists(P['seed_registry']):
        reasons.append('SEED_SERIAL_NOT_REGISTERED')
    print(json.dumps({'ok': not reasons, 'reasons': reasons, 'record_exists': rec, 'launches': L}))
    return 0 if not reasons else 3


def read_record(plan):
    raw = Path(plan['paths']['record']).read_bytes()
    rec = strict_json(raw, 'M-15 record')
    need(rec.get('schema') == 'UNT_M15_PRELAUNCH_RECORD_C2V001', 'M15_RECORD_SCHEMA')
    return rec, sha_bytes(raw)


def cmd_freeze_check(a):
    """While no launch record exists (the first launch), V006 must be byte-identical to the V006 the M-15 record logged
    (path and sha256): the write freeze lasts from the record to the first receipt."""
    plan = load_plan(a.plan)
    rec, rsha = read_record(plan)
    L = launches(plan)
    now = sha_file(plan['v006']['path'])
    reasons = []
    if not L:
        if rec['v006']['path'] != plan['v006']['path']:
            reasons.append('V006_PATH_DIFFERS_FROM_RECORD')
        if rec['v006']['sha256'] != now:
            reasons.append('V006_CHANGED_SINCE_RECORD (record %s, now %s)' % (rec['v006']['sha256'], now))
    print(json.dumps({'ok': not reasons, 'reasons': reasons, 'freeze_open': not L, 'record_sha256': rsha,
                      'record_v006_sha256': rec['v006']['sha256'], 'v006_sha256_now': now}))
    return 0 if not reasons else 3


def cmd_record_epoch(a):
    plan = load_plan(a.plan)
    rec, _ = read_record(plan)
    print(int(rec['date_u_epoch_s']))
    return 0


# ------------------------------------------------------------------------------------------------------------- argv
FLAGS = ('--driver', '--driver-sha256', '--spec', '--outdir', '--receipt', '--wall-cap-s', '--rss-cap-bytes', '--output-cap-bytes')


def check_monitor_argv(argv, plan):
    """A143 D3 form: PY -I -B <monitor> then exactly the eight flags in order, each with one value; --driver-sha256 64
    lowercase hex equal to the pin; --spec absolute; --outdir absolute under External1 (never runs_ext); receipt =
    outdir + '.receipt.json'; caps equal to the call's caps of record."""
    r = []
    if len(argv) != 4 + 2 * len(FLAGS):
        return ['ARGV_LENGTH %d' % len(argv)]
    if argv[0] != plan['python'] or argv[1:3] != ['-I', '-B']:
        r.append('INTERPRETER_FORM')
    if argv[3] != plan['pins']['monitor']['path']:
        r.append('MONITOR_PATH')
    kv = {}
    for i, f in enumerate(FLAGS):
        k, v = argv[4 + 2 * i], argv[5 + 2 * i]
        if k != f:
            r.append('FLAG_ORDER %s != %s' % (k, f))
        kv[f] = v
    if r:
        return r
    if kv['--driver'] != plan['pins']['driver']['path']:
        r.append('DRIVER_PATH')
    if not HEX64.match(kv['--driver-sha256']) or kv['--driver-sha256'] != plan['pins']['driver']['sha256']:
        r.append('DRIVER_SHA256_FORM (exactly 64 lowercase hex equal to the pin)')
    s = kv['--spec']
    if not os.path.isabs(s) or os.path.normpath(s) != s:
        r.append('SPEC_NOT_ABSOLUTE')
    o = kv['--outdir']
    try:
        path_rules(o, 'OUTDIR')
    except Refusal as e:
        r.append(str(e))
    ext1 = plan['ext1_root'].rstrip('/')
    if not os.path.isabs(o) or os.path.normpath(o) != o or not o.startswith(ext1 + '/'):
        r.append('OUTDIR_NOT_ABSOLUTE_UNDER_%s' % ext1)
    if o != plan['outdir']:
        r.append('OUTDIR_NOT_THE_PLANNED_STRING')
    if not os.path.basename(o).startswith('NGC_') or 'ngc3198' in o.lower():
        r.append('OUTDIR_NAME')
    if kv['--receipt'] != o + '.receipt.json':
        r.append('RECEIPT_FORM')
    caps = plan['caps']
    for f, k in (('--wall-cap-s', 'wall_cap_s'), ('--rss-cap-bytes', 'rss_cap_bytes'), ('--output-cap-bytes', 'output_cap_bytes')):
        if kv[f] != str(caps[k]):
            r.append('CAP %s %s != %s' % (f, kv[f], caps[k]))
    return r


def cmd_monitor_argv(a):
    plan = load_plan(a.plan)
    argv = list(a.argv)
    if argv and argv[0] == '--':
        argv = argv[1:]
    r = check_monitor_argv(argv, plan)
    if r:
        print(json.dumps({'ok': False, 'reasons': r}))
        return 3
    print(' '.join(shlex.quote(x) for x in argv))
    return 0


# ------------------------------------------------------------------------------------------------------------- twin
def parse_iso(s):
    return calendar.timegm(time.strptime(s, '%Y-%m-%dT%H:%M:%SZ'))


def cmd_wave_state(a):
    """Root's attestation for the twin start (A143 D2/D3; A140 N2): ROOT_WAVE_STATE_C2V001 with wave_in_progress false,
    direct_batch_pending false, utc no older than 600 s (and not in the future by more than 60 s)."""
    reasons = []
    try:
        w = strict_json(Path(a.file).read_bytes(), 'wave state')
    except (OSError, Refusal) as e:
        print(json.dumps({'ok': False, 'reasons': ['WAVE_STATE_UNREADABLE %s' % e]}))
        return 3
    if not (type(w) is dict and set(w) == {'schema', 'wave_in_progress', 'direct_batch_pending', 'utc', 'written_by'} and
            w['schema'] == 'ROOT_WAVE_STATE_C2V001' and type(w['wave_in_progress']) is bool and
            type(w['direct_batch_pending']) is bool):
        reasons.append('WAVE_STATE_FORM')
    else:
        if w['wave_in_progress']:
            reasons.append('MID_WAVE')
        if w['direct_batch_pending']:
            reasons.append('DIRECT_BATCH_PENDING')
        try:
            age = time.time() - parse_iso(w['utc'])
            if age > 600 or age < -60:
                reasons.append('WAVE_STATE_STALE age_s=%.0f' % age)
        except (ValueError, TypeError):
            reasons.append('WAVE_STATE_UTC_FORM')
    out = {'ok': not reasons, 'reasons': reasons, 'file': a.file, 'sha256': sha_file(a.file)}
    if a.out:
        write_x(a.out, dict(out, schema='S0_WAVE_STATE_CHECK_C2V001', date_u=date_u()))
    print(json.dumps(out))
    return 0 if not reasons else 3


def find_stage(outdir):
    st = Path(outdir) / 'stages'
    if not st.is_dir():
        return None, 0
    names = [d for d in sorted(os.listdir(st)) if re.fullmatch(r'[0-9]{2}_route_a', d)]
    return (st / names[0] if len(names) == 1 else None), len(names)


def cmd_twin_trigger(a):
    """A141 L4: the twin's planned stop once iteration 1 is COMPLETED and its sidecar iteration record exists.  Existence
    only: stages/NN_route_a/checkpoint/iteration_0001/COMPLETED.json and stages/NN_route_a/uv_tail_sidecar/iteration_0001.json
    (records are published atomically; the comparator verifies their integrity later).  No content is read."""
    need(os.path.isabs(a.outdir), 'OUTDIR_NOT_ABSOLUTE')
    stage, n = find_stage(a.outdir)
    if n > 1:
        print(json.dumps({'met': False, 'error': 'MORE_THAN_ONE_ROUTE_A_STAGE', 'n': n}))
        return 3
    if stage is None:
        print(json.dumps({'met': False, 'completed': False, 'sidecar': False, 'stage': None}))
        return 1
    c = (stage / 'checkpoint' / 'iteration_0001' / 'COMPLETED.json').is_file()
    s = (stage / 'uv_tail_sidecar' / 'iteration_0001.json').is_file()
    print(json.dumps({'met': c and s, 'completed': c, 'sidecar': s, 'stage': str(stage)}))
    return 0 if (c and s) else 1


def ps_field(pid, field):
    r = subprocess.run(['/bin/ps', '-ww', '-o', '%s=' % field, '-p', str(pid)], capture_output=True, text=True, timeout=20)
    return r.stdout.strip() if r.returncode == 0 else None


def cmd_kill_target(a):
    """Before a twin kill: the launch record's child is alive, leads its own process group, runs exactly the launch
    record's command, and that command's spec is the registered twin (sha and column_workers 8)."""
    lj = strict_json(Path(a.launch_json).read_bytes(), 'launch json')
    reasons = []
    pid = lj.get('child_pid')
    cmd = lj.get('command')
    spec = ((lj.get('pins') or {}).get('spec') or {})
    if type(pid) is not int or pid <= 1 or not isinstance(cmd, list):
        reasons.append('LAUNCH_JSON_FORM')
    else:
        if spec.get('sha256') != a.twin_spec_sha256:
            reasons.append('LAUNCH_SPEC_IS_NOT_THE_TWIN')
        try:
            sb = Path(spec.get('path')).read_bytes()
            if sha_bytes(sb) != a.twin_spec_sha256 or dig(strict_json(sb, 'twin spec'), LEAF) != 8:
                reasons.append('TWIN_SPEC_BYTES_OR_LEAF')
        except (OSError, TypeError, Refusal):
            reasons.append('TWIN_SPEC_UNREADABLE')
        pg = ps_field(pid, 'pgid')
        if not pg:
            reasons.append('CHILD_NOT_ALIVE')
        else:
            if int(pg) != pid:
                reasons.append('CHILD_NOT_A_GROUP_LEADER')
            if ps_field(pid, 'command') != ' '.join(cmd):
                reasons.append('CHILD_COMMAND_DIFFERS (pid reuse?)')
    print(json.dumps({'ok': not reasons, 'reasons': reasons, 'pgid': pid}), file=sys.stderr)
    if reasons:
        return 3
    print(pid)
    return 0


def cmd_kill_record(a):
    lr = Path(a.launch_root)
    d = lr / 'twin_kill'
    d.mkdir(exist_ok=True)
    rec = {'schema': 'UNT_S0_TWIN_KILL_RECORD_C2V001', 'date_u': date_u(), 'reason': a.reason, 'pgid': a.pgid,
           'result': a.result, 'launch_json': {'path': a.launch_json, 'sha256': sha_file(a.launch_json)},
           'outdir': a.outdir, 'rule': 'A141 L4: the planned twin stop after iteration 1 COMPLETED + sidecar record; not a '
                                       'failure (A135 item 3; A133 section 3(c)); the twin is never a member'}
    p = d / ('TWIN_KILL_RECORD_%s_C2V001.json' % a.reason)
    h = write_x(p, rec)
    print(json.dumps({'status': 'WRITTEN', 'path': str(p), 'sha256': h}))
    return 0


# ------------------------------------------------------------------------------------------------------------- launch record
def cmd_launch_record(a):
    """After the monitor wrote <receipt>.launch.json: check it against the plan and write the launch record ('x').
    First launch (no other launch record): launch utc epoch must be > the M-15 record's date -u epoch, and V006 is
    re-hashed (a change is flagged: the order of a V006 write against the receipt is not decidable from bytes)."""
    plan = load_plan(a.plan)
    rec, rsha = read_record(plan)
    lj_raw = Path(plan['launch_json']).read_bytes()
    lj = strict_json(lj_raw, 'launch json')
    first = not launches(plan)
    expected_cmd = [plan['python'], '-I', '-B', plan['pins']['driver']['path'], 'run', '--spec', a.spec, '--outdir', plan['outdir']]
    caps = lj.get('caps') or {}
    try:
        launch_epoch = parse_iso(lj.get('utc'))
    except (TypeError, ValueError):
        launch_epoch = None
    checks = {
        'schema': lj.get('schema') == LAUNCH_SCHEMA,
        'command_is_planned': lj.get('command') == expected_cmd,
        'driver_pin': (lj.get('pins') or {}).get('driver') == {'path': plan['pins']['driver']['path'],
                                                                'sha256': plan['pins']['driver']['sha256']},
        'spec_pin': (lj.get('pins') or {}).get('spec') == {'path': a.spec, 'sha256': a.spec_sha256},
        'monitor_sha': ((lj.get('pins') or {}).get('monitor') or {}).get('sha256') == plan['pins']['monitor']['sha256'],
        'caps': all(float(caps.get(k, -1)) == float(v) for k, v in plan['caps'].items()),
        'retries_0': lj.get('retries_allowed') == 0,
        'child_pid': type(lj.get('child_pid')) is int,
    }
    flags = []
    v006_now = sha_file(plan['v006']['path'])
    if first:
        checks['m15_record_precedes_first_launch'] = launch_epoch is not None and launch_epoch > int(rec['date_u_epoch_s'])
        if v006_now != rec['v006']['sha256']:
            flags.append('V006_CHANGED_BETWEEN_RECORD_AND_THIS_CHECK')
    bad = sorted(k for k, v in checks.items() if not v)
    out = {'schema': 'UNT_S0_LAUNCH_RECORD_C2V001', 'name': plan['names']['spec_pin'], 'role': plan['role'],
           'call': plan['call'], 'first_launch': first, 'checks': checks, 'failed': bad, 'flags': flags,
           'm15_record': {'path': plan['paths']['record'], 'sha256': rsha, 'date_u': rec['date_u'],
                          'date_u_epoch_s': rec['date_u_epoch_s'], 'v006_sha256': rec['v006']['sha256']},
           'launch_json': {'path': plan['launch_json'], 'sha256': sha_bytes(lj_raw), 'utc': lj.get('utc'),
                           'utc_epoch_s': launch_epoch, 'child_pid': lj.get('child_pid')},
           'v006_sha256_now': v006_now, 'spec': {'path': a.spec, 'sha256': a.spec_sha256},
           'driver': plan['pins']['driver'], 'monitor': plan['pins']['monitor'], 'outdir': plan['outdir'],
           'receipt': plan['receipt'], 'caps': plan['caps'], 'monitor_pid': a.mon_pid, 'hold_check_exit': a.hold_exit,
           'hold_confirmed': a.hold_confirmed, 'watch_pid': a.watch_pid,
           'work_files': {Path(p).name: {'path': p, 'sha256': sha_file(p)} for p in sorted(str(x) for x in Path(a.work).iterdir())
                          if Path(p).is_file()},
           'registry': {'path': plan['paths']['registry'], 'sha256': sha_file(plan['paths']['registry'])},
           'kit': plan['kit'], 'synthetic': plan['synthetic'], 'date_u': date_u(),
           'reads': 'validity-only until r3a and the M-12 classifier are sealed (A133 section 2 row 2); after every result '
                    'check result driver_sha256 = 577f8c94 (A77.1 N8)'}
    Path(plan['paths']['launches_dir']).mkdir(exist_ok=True)
    h = write_x(plan['paths']['launch_record'], out)
    print(json.dumps({'status': 'LAUNCH_RECORD_WRITTEN', 'path': plan['paths']['launch_record'], 'sha256': h, 'failed': bad,
                      'flags': flags}))
    return 3 if bad else (4 if flags else 0)


# ------------------------------------------------------------------------------------------------------------- main
def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    v = sub.add_parser('validate')
    for k in ('role', 'call', 'mode', 'launch-root', 'run-root'):
        v.add_argument('--' + k, required=True)
    v.add_argument('--synthetic-pins')
    v.add_argument('--synthetic-pins-sha256')
    v.add_argument('--emit', choices=('shell', 'json'), default='shell')
    v.add_argument('--out')
    f = sub.add_parser('fill-check')
    f.add_argument('--plan', required=True)
    f.add_argument('--fill-dir', required=True)
    f.add_argument('--out')
    d = sub.add_parser('dry-verdict')
    for k in ('plan', 'spec', 'spec-sha256', 'log', 'report-dir'):
        d.add_argument('--' + k, required=True)
    d.add_argument('--out')
    r = sub.add_parser('register')
    for k in ('plan', 'fill-check', 'dry-verdict'):
        r.add_argument('--' + k, required=True)
    ad = sub.add_parser('admission')
    for k in ('plan', 'spec', 'spec-sha256'):
        ad.add_argument('--' + k, required=True)
    ad.add_argument('--out')
    g = sub.add_parser('gate-cli')
    g.add_argument('--plan', required=True)
    g.add_argument('--which', choices=('hold', 'twin-start'), required=True)
    g.add_argument('--snapshot-key', choices=('snapshot', 'snapshot_after_twin'), default='snapshot')
    for name in ('ext1-check', 'watch-check', 'freeze-check', 'record-epoch'):
        s = sub.add_parser(name)
        s.add_argument('--plan', required=True)
        s.add_argument('--out')
    s2 = sub.add_parser('step2-check')
    s2.add_argument('--plan', required=True)
    s2.add_argument('--receipt', required=True)
    s2.add_argument('--out')
    o = sub.add_parser('order-check')
    o.add_argument('--plan', required=True)
    m = sub.add_parser('monitor-argv')
    m.add_argument('--plan', required=True)
    m.add_argument('argv', nargs=argparse.REMAINDER)
    w = sub.add_parser('wave-state')
    w.add_argument('--file', required=True)
    w.add_argument('--out')
    lr = sub.add_parser('launch-record')
    for k in ('plan', 'work', 'spec', 'spec-sha256'):
        lr.add_argument('--' + k, required=True)
    lr.add_argument('--mon-pid', type=int, required=True)
    lr.add_argument('--hold-exit', type=int, required=True)
    lr.add_argument('--hold-confirmed', choices=('yes', 'no', 'n/a'), default='n/a')
    lr.add_argument('--watch-pid', type=int)
    t = sub.add_parser('twin-trigger')
    t.add_argument('--outdir', required=True)
    k = sub.add_parser('kill-target')
    k.add_argument('--launch-json', required=True)
    k.add_argument('--twin-spec-sha256', required=True)
    kr = sub.add_parser('kill-record')
    for x in ('launch-root', 'launch-json', 'outdir', 'result', 'reason'):
        kr.add_argument('--' + x, required=True)
    kr.add_argument('--pgid', type=int, required=True)
    a = ap.parse_args(argv)
    fn = {'validate': cmd_validate, 'fill-check': cmd_fill_check, 'dry-verdict': cmd_dry_verdict, 'register': cmd_register,
          'admission': cmd_admission, 'gate-cli': cmd_gate_cli, 'ext1-check': cmd_ext1_check, 'step2-check': cmd_step2_check,
          'watch-check': cmd_watch_check, 'order-check': cmd_order_check, 'freeze-check': cmd_freeze_check,
          'record-epoch': cmd_record_epoch, 'monitor-argv': cmd_monitor_argv, 'wave-state': cmd_wave_state,
          'launch-record': cmd_launch_record, 'twin-trigger': cmd_twin_trigger, 'kill-target': cmd_kill_target,
          'kill-record': cmd_kill_record}[a.cmd]
    try:
        return fn(a)
    except (Refusal, OSError, KeyError, TypeError, ValueError) as e:
        print(json.dumps({'status': 'REFUSED', 'step': a.cmd, 'reason': '%s: %s' % (type(e).__name__, e)}))
        return 3


if __name__ == '__main__':
    sys.exit(main())
