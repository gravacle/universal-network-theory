"""s0_kit_c2v003.py -- the checks and custody records behind the S0 launch scripts (s0_launch_kit_c2, C2V003).

It launches nothing: it never starts root_monitor or the NGC driver, and it never reads a run's result.  The shell
scripts (launch_s0_serial_root_c2v003.sh, launch_twin_root_c2v003.sh, twin_kill_watch_c2v003.sh) call one subcommand per
step and act only on exit 0.  Exit codes: 0 pass, 3 refused (launch-check: stop the launch), 4 written with an
order/consistency flag, 1 'not yet' (twin-trigger) or 'child not alive' (kill-target), 2 usage.  Every file it writes is
created exclusively ('x') and fsynced.

C2V003 (successor of C2V002; V006 A166, the principal's direction to stop micromanaging the Mac's resources): no memory
gating.  The sched v003 admission (ngc_admission class, gate decide, the A133 103 GB rule), the gate --hold-check /
--twin-start-check calls, the A147 L3-03 kind check and the twin's wave-state attestation are removed; nothing here reads
the machine's memory.  The per-call RSS cap is physical RAM (137,438,953,472 B) for the serial and the twin; the wall
and output caps are unchanged.  The twin may start any time after the seed serial's LAUNCH record.  Kept: M-15 first,
seed first, fill / dry plan / registry / custody checks, absolute External1 paths, the disk check, the relaunch path and
the twin's kill watch after iteration 1.  The post-launch check is now the launch record (<receipt>.launch.json)
against the plan; a launch whose record does not match is stopped as a procedural mis-launch and relaunched as attempt
k+1 in the same launch root under the same M-15 record.

Subcommands (see each function's docstring):
  validate        args + every pin from bytes -> plan (shell assignments or JSON); writes nothing (except --emit json --out)
  fill-check      the filled serial/twin specs against the role's handoff, certificates and V006 SPEC_PIN
  dry-verdict     the fresh cx3r008 dry plan: blocker lists, not the readiness label (RI45-13 item 7)
  register        the per-point launch registry entry (exclusive create)
  ext1-check      External1 mount, path spelling, absent outputs, free space >= output cap + 20 GiB
  step2-check     step 2's last receipt exists (A135.5)
  watch-check     the V006 WATCH_PIN watch script verifies and is running (A135.5; the watch is passive, A166)
  order-check     after the M-15 step: seed serial first, one confirmed launch per name, attempt k+1 only after a
                  recorded mis-launch of attempt k whose monitor receipt exists (M-15; r3a L454)
  freeze-check    V006 unchanged since the M-15 record while no launch receipt exists yet
  record-epoch    the M-15 record's date -u epoch second
  monitor-argv    validates the exact root_monitor argv the script will exec (D3 form) and prints it shell-quoted
  launch-check    the post-launch check: <receipt>.launch.json against the plan (command, pins, caps, retries, M-15 order)
  launch-record   writes the attempt's record (exclusive create): LAUNCH (launch check confirmed) or MISLAUNCH (stopped)
  twin-trigger    A141 L4: iteration_0001/COMPLETED.json and uv_tail_sidecar/iteration_0001.json both exist
  kill-target     verifies a launched driver process group (spec sha, leaf, group leader, command, parent) before a kill
  kill-record     writes the twin's planned-stop kill record (exclusive create)
"""
import argparse
import calendar
import hashlib
import json
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
RECORD_WRITER = ('s0_prelaunch_record_c2v001.py', 'a10965b7a508f106e3d153632d2b1a39a427d9106fa2de3c9e09d92b85bcb59a')     # the C2V001 writer, unchanged
GATE_PINS = ('GATE_DOCUMENT_PINS_V002.json', '5e688882451824931f964e610cf17597d82ee0eb246fb0dce528ec0c6e148042')
PY = '/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
A = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/'
UNTPC = '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/'
GiB = 1 << 30
VTAG = 'C2V003'
ROLES = ('seed', 'j0', 'j1', 'j2')
ROLE_NAME = {'seed': 'SEED', 'j0': 'J0', 'j1': 'J1', 'j2': 'J2'}
S0_ROLE = {'seed': 'seed', 'j0': 'jacobian_first_attempt_0', 'j1': 'jacobian_first_attempt_1', 'j2': 'jacobian_first_attempt_2'}
KEYS = {'seed': '968c915bece706ea1d6c0fa15357984884a87443e7c19eebd104230c9c961981',
        'j0': '3d7785669b549d6f9b9e0df65a3ad71de00c0da26a974c77ccb258856000fa60',
        'j1': 'ab7bf95317b37652282ac7da86931816955ce8a781279b79e1d5258689c3970c',
        'j2': '4b9b4ec88eb2d94ce2c8eeb52e2f7c5b5b7f96bdb5d4df52b9077ba06401f6a2'}
RAM_BYTES = 137438953472                          # V006 A166: per-call RSS cap = physical RAM (128 GiB)
CAPS = {'serial': {'wall_cap_s': 610324, 'rss_cap_bytes': RAM_BYTES, 'output_cap_bytes': 146028888064},
        'twin': {'wall_cap_s': 22752, 'rss_cap_bytes': RAM_BYTES, 'output_cap_bytes': 34359738368}}
CAPS_FROM_FILE = ('wall_cap_s', 'output_cap_bytes')   # checked against CAPS_S45_C2V003; the RSS cap is A166's, not the file's
EXPECTED_LEAF = {'serial': 1, 'twin': 8}
MAX_ATTEMPT = 99
DISK_RESERVE_BYTES = 20 * GiB                     # per-start check: one output cap + 20 GiB (kept; A166 keeps the disk guard)
SERIAL_FILE, TWIN_FILE = 'CALL_A_K32_A2_HEADLINE_C2V001.json', 'CALL_A_K32_A2_HEADLINE_CW8_TWIN_C2V001.json'
FILL_RECEIPT = 'FILL_RECEIPT_C2V001.json'
LEAF = ('numerics', 'route_a', 'column_workers')
LAUNCH_SCHEMA = 'UNT_GALAXY_M0_MONITOR_RECEIPT_C2V001_LAUNCH'
HEX64 = re.compile(r'^[0-9a-f]{64}$')
ATTEMPT_RE = re.compile(r'^(?P<name>S0_(?:SEED|J0|J1|J2)_SERIAL|S0_SEED_CW8_TWIN)_(?P<kind>LAUNCH|MISLAUNCH)_C2V003_'
                        r'A(?P<k>[1-9][0-9]?)\.json$')
RECORD_SCHEMA = {'LAUNCH': 'UNT_S0_LAUNCH_RECORD_C2V003', 'MISLAUNCH': 'UNT_S0_MISLAUNCH_RECORD_C2V003'}
LAUNCH_RULE = ('V006 A166: no gate reading and no memory admission; after each launch the launch record '
               '(<receipt>.launch.json) must match the plan (command, driver/spec/monitor pins, caps with RSS = RAM, '
               'retries 0, launch after the M-15 record); otherwise the launch is stopped as a procedural mis-launch')
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
SYNTHETIC_KEYS = ('schema', 'v006', 'driver', 'monitor', 'filler', 'dry_harness', 's0_record', 'policy',
                  'acceptance', 'lo', 'gq_gate', 'eps', 'gq', 'gate_pins', 'external1_root', 'python',
                  'external1_require_mount', 'free_bytes_override')


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


def fsync_dir(path):
    dfd = os.open(str(path), os.O_RDONLY)
    try:
        os.fsync(dfd)
    finally:
        os.close(dfd)


def write_x_bytes(path, b, mode=0o444):
    path = Path(path)
    fd = os.open(str(path), os.O_WRONLY | os.O_CREAT | os.O_EXCL, mode)
    try:
        os.write(fd, b)
        os.fsync(fd)
    finally:
        os.close(fd)
    fsync_dir(path.parent)
    return sha_bytes(b)


def write_x(path, obj):
    return write_x_bytes(path, (json.dumps(obj, indent=1, sort_keys=True, allow_nan=False, default=str) + '\n').encode())


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


def pin_of(path):
    return {'path': str(path), 'sha256': sha_file(path)}


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
    need(type(sp) is dict and set(sp) == set(SYNTHETIC_KEYS) and sp['schema'] == 'S0_LAUNCH_KIT_SYNTHETIC_PINS_C2V003',
         'SYNTHETIC_PINS_KEYS')
    # a synthetic run can never reach the real monitor or the real driver
    for k in ('driver', 'monitor'):
        need(sp[k]['sha256'] != REAL[k]['sha256'] and os.path.realpath(sp[k]['path']) != os.path.realpath(REAL[k]['path']),
             'SYNTHETIC_PINS_NAME_THE_REAL_%s' % k.upper())
    need(Path(sp['monitor']['path']).name != Path(REAL['monitor']['path']).name and
         not re.search(r'root_monitor_c2v\d+\.py', sp['monitor']['path']), 'SYNTHETIC_MONITOR_NAME_MATCHES_GATE_PATTERN')
    return sp, True, {'path': a.synthetic_pins, 'sha256': a.synthetic_pins_sha256}


def run_name_for(call, nm, k):
    base = 'NGC_P1_S0_%s_SERIAL_RUN' % nm if call == 'serial' else 'NGC_P1_S0_SEED_CW8_TWIN_RUN'
    return '%s_%s_A%d' % (base, VTAG, k)


def record_name(reg_name, kind, k):
    return '%s_%s_%s_A%d.json' % (reg_name, kind, VTAG, k)


def build_plan(a):
    need(a.role in ROLES, 'ROLE must be seed|j0|j1|j2')
    need(a.call in ('serial', 'twin'), 'CALL')
    need(a.mode in ('dry', 'launch'), 'MODE')
    need(not (a.call == 'twin' and a.role != 'seed'), 'TWIN_IS_AT_THE_SEED_ONLY')
    need(re.fullmatch(r'[1-9][0-9]?', str(a.attempt or '')) is not None, 'ATTEMPT must be an integer 1..%d' % MAX_ATTEMPT)
    k = int(a.attempt)
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
    run_name = run_name_for(a.call, nm, k)
    outdir = rr + '/' + run_name
    receipt = outdir + '.receipt.json'
    reg_name = 'S0_%s_SERIAL' % nm if a.call == 'serial' else 'S0_SEED_CW8_TWIN'
    # every pin from bytes
    for key in ('driver', 'monitor', 'filler', 'dry_harness', 's0_record', 'policy', 'acceptance', 'lo', 'gq_gate', 'gate_pins'):
        verify_pin(pins[key], key)
    verify_pin(pins['eps'][a.role], 'eps_' + a.role)
    verify_pin(pins['gq'][a.role], 'gq_' + a.role)
    caps = verify_pin(REAL['caps'], 'caps')
    cj = strict_json(Path(caps['path']).read_bytes(), 'caps')
    need({c: cj['ngc_s0_call_of_record'][c] for c in CAPS_FROM_FILE} == {c: CAPS['serial'][c] for c in CAPS_FROM_FILE} and
         {c: cj['ngc_identity_twin'][c] for c in CAPS_FROM_FILE} == {c: CAPS['twin'][c] for c in CAPS_FROM_FILE},
         'CAPS_FILE_WALL_OR_OUTPUT_DIFFERS_FROM_KIT_CAPS')
    need(all(type(CAPS[c]['rss_cap_bytes']) is int and CAPS[c]['rss_cap_bytes'] == RAM_BYTES for c in CAPS),
         'RSS_CAP_NOT_RAM (V006 A166: the RSS cap is physical RAM, %d B)' % RAM_BYTES)
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
    launches_dir = lrp / 'launches'
    prev = None
    if k > 1:
        prev_out = rr + '/' + run_name_for(a.call, nm, k - 1)
        prev = {'attempt': k - 1, 'mislaunch_record': str(launches_dir / record_name(reg_name, 'MISLAUNCH', k - 1)),
                'outdir': prev_out, 'receipt': prev_out + '.receipt.json'}
    plan = {
        'schema': 'S0_LAUNCH_PLAN_C2V003', 'mode': a.mode, 'call': a.call, 'role': a.role, 'attempt': k,
        'synthetic': synthetic, 'synthetic_pins': sp_pin, 'python': pins['python'],
        'kit': {'dir': str(KIT_DIR), 'helper': {'path': str(Path(__file__).resolve()), 'sha256': sha_file(__file__)},
                'record_writer': {'path': str(KIT_DIR / RECORD_WRITER[0]), 'sha256': RECORD_WRITER[1]}, 'gate_pins': gp},
        'pins': {key: pins[key] for key in ('driver', 'monitor', 'filler', 'dry_harness', 's0_record', 'policy', 'acceptance',
                                            'lo', 'gq_gate')},
        'eps': pins['eps'][a.role], 'gq_binding': pins['gq'][a.role], 'caps_file': caps, 'caps': CAPS[a.call],
        'caps_basis': {'wall_cap_s': 'CAPS_S45_C2V003 (A135 item 3; A141 L1)', 'output_cap_bytes': 'CAPS_S45_C2V003 (A140 N3)',
                       'rss_cap_bytes': 'V006 A166: physical RAM %d B' % RAM_BYTES},
        'theta_key': KEYS[a.role],
        'expected': {'leaf': EXPECTED_LEAF[a.call], 'rule': LAUNCH_RULE},
        'names': {'handoff_pin': 'S0_' + nm, 'spec_pin': reg_name, 'serial_spec_pin': 'S0_%s_SERIAL' % nm,
                  'run_name': run_name, 'first_call': 'S0_SEED_SERIAL'},
        'launch_root': lr,
        'paths': {'record': str(lrp / 'M15_PRELAUNCH_RECORD_C2V001.json'),
                  'registry': str(lrp / 'registry' / ('%s_%s.json' % (reg_name, VTAG))),
                  'launch_record': str(launches_dir / record_name(reg_name, 'LAUNCH', k)),
                  'mislaunch_record': str(launches_dir / record_name(reg_name, 'MISLAUNCH', k)),
                  'seed_registry': str(lrp / 'registry' / ('S0_SEED_SERIAL_%s.json' % VTAG)),
                  'launches_dir': str(launches_dir), 'kill_dir': str(lrp / 'twin_kill')},
        'previous_attempt': prev,
        'ext1_root': ext1, 'run_root': rr, 'outdir': outdir, 'receipt': receipt, 'launch_json': receipt + '.launch.json',
        'v006': {'path': v006, 'sha256_at_validate': sha_bytes(vraw)},
        'v006_pins': {'handoff': hand, 'spec': spec_pin, 'serial_spec': serial_pin, 'watch': watch},
        'synthetic_extras': ({key: pins[key] for key in ('external1_require_mount', 'free_bytes_override')}
                             if synthetic else None),
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
          'PLAN_ATTEMPT': str(plan['attempt']), 'PLAN_V006': plan['v006']['path'], 'PLAN_DRIVER': plan['pins']['driver']['path'],
          'PLAN_DRIVER_SHA': plan['pins']['driver']['sha256'], 'PLAN_MONITOR': plan['pins']['monitor']['path'],
          'PLAN_MONITOR_SHA': plan['pins']['monitor']['sha256'], 'PLAN_FILLER': plan['pins']['filler']['path'],
          'PLAN_FILLER_SHA': plan['pins']['filler']['sha256'], 'PLAN_DRY': plan['pins']['dry_harness']['path'],
          'PLAN_DRY_SHA': plan['pins']['dry_harness']['sha256'], 'PLAN_GATE_PINS': plan['kit']['gate_pins']['path'],
          'PLAN_GATE_PINS_SHA': plan['kit']['gate_pins']['sha256'], 'PLAN_RECORD': plan['paths']['record'],
          'PLAN_REGISTRY': plan['paths']['registry'], 'PLAN_LAUNCH_RECORD': plan['paths']['launch_record'],
          'PLAN_MISLAUNCH_RECORD': plan['paths']['mislaunch_record'],
          'PLAN_SEED_REGISTRY': plan['paths']['seed_registry'], 'PLAN_LAUNCHES_DIR': plan['paths']['launches_dir'],
          'PLAN_OUTDIR': plan['outdir'], 'PLAN_RECEIPT': plan['receipt'], 'PLAN_LAUNCH_JSON': plan['launch_json'],
          'PLAN_EXT1': plan['ext1_root'], 'PLAN_WALL': str(plan['caps']['wall_cap_s']), 'PLAN_RSS': str(plan['caps']['rss_cap_bytes']),
          'PLAN_OUTCAP': str(plan['caps']['output_cap_bytes']), 'PLAN_THETA_KEY': plan['theta_key'],
          'PLAN_EXPECTED_LEAF': str(plan['expected']['leaf']),
          'PLAN_FIRST_CALL': plan['names']['first_call'], 'PLAN_HANDOFF': hand.get('path', ''),
          'PLAN_HANDOFF_SHA': hand.get('sha256', ''), 'PLAN_SPEC_PIN_SHA': spec.get('sha256', ''),
          'PLAN_RUN_NAME': plan['names']['run_name']}
    for key, v in kv.items():
        print('%s=%s' % (key, shlex.quote(v)))
    return 0


def load_plan(path):
    raw = Path(path).read_bytes()
    plan = strict_json(raw, 'plan')
    need(plan.get('schema') == 'S0_LAUNCH_PLAN_C2V003', 'PLAN_SCHEMA')
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
    out = {'schema': 'S0_FILL_CHECK_C2V003', 'ok': not bad, 'failed': bad, 'checks': checks, 'date_u': date_u(),
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
    out = {'schema': 'S0_DRY_VERDICT_C2V003', 'ok': not bad, 'failed': bad, 'checks': checks, 'date_u': date_u(),
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


def attempt_records(plan, name=None):
    """The attempt records in <launch root>/launches (LAUNCH | MISLAUNCH, attempt k), optionally of one name."""
    d = Path(plan['paths']['launches_dir'])
    out = []
    if d.is_dir():
        for p in sorted(d.iterdir()):
            m = ATTEMPT_RE.match(p.name)
            if m and (name is None or m.group('name') == name):
                out.append({'path': str(p), 'name': m.group('name'), 'kind': m.group('kind'), 'attempt': int(m.group('k'))})
    return out


def cmd_register(a):
    """The per-point launch registry entry (RI45-13 (a); A135 item 9), exclusive create in launch mode.  One entry per name;
    a relaunch (attempt k > 1) or a retry after a refusal reuses it only for the same spec bytes and V006 pins."""
    plan = load_plan(a.plan)
    fc = strict_json(Path(a.fill_check).read_bytes(), 'fill check')
    dv = strict_json(Path(a.dry_verdict).read_bytes(), 'dry verdict')
    need(fc['ok'] and dv['ok'], 'FILL_OR_DRY_NOT_OK')
    need(dv['spec']['sha256'] == fc['launch_spec']['sha256'], 'DRY_PLAN_OF_ANOTHER_SPEC')
    entry = {'schema': 'UNT_S0_LAUNCH_REGISTRY_ENTRY_C2V003', 'name': plan['names']['spec_pin'], 'role': plan['role'],
             'call': plan['call'], 'theta_key': plan['theta_key'], 'spec': fc['launch_spec'],
             'v006_spec_pin': fc['v006_spec_pin'], 'v006_handoff_pin': fc['v006_handoff_pin'],
             'pair': {'serial': fc['serial'], 'twin': fc['twin']}, 'fill_dir': fc['fill_dir'], 'fill_receipt': fc['fill_receipt'],
             'certificates': fc['certificates'], 's0_record': plan['pins']['s0_record'], 'driver': plan['pins']['driver'],
             'fill_check': {'path': a.fill_check, 'sha256': sha_file(a.fill_check)},
             'dry_verdict': {'path': a.dry_verdict, 'sha256': sha_file(a.dry_verdict)}, 'dry_log': dv['log'],
             'registered_at_attempt': plan['attempt'],
             'rule': 'RI45-13 (a): fresh dry plan with the real certificate pins, spec sha registered (V006 SPEC_PIN), driver '
                     'sha checked before launch', 'date_u': date_u(), 'synthetic': plan['synthetic']}
    if plan['mode'] != 'launch':
        print(json.dumps({'status': 'DRY_NOT_REGISTERED', 'would_write': plan['paths']['registry'], 'entry': entry}))
        return 0
    Path(plan['paths']['registry']).parent.mkdir(exist_ok=True)
    launched = [r for r in attempt_records(plan, plan['names']['spec_pin']) if r['kind'] == 'LAUNCH']
    need(not launched, 'ALREADY_LAUNCHED %s' % [r['path'] for r in launched])
    if os.path.lexists(plan['paths']['registry']):
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
        reasons.append('DISK_FREE %s < %d (output cap + 20 GiB, per-start check)' % (free, need_bytes))
    out = {'schema': 'S0_EXT1_CHECK_C2V003', 'ok': not reasons, 'reasons': reasons, 'free_bytes': free,
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
    out = {'schema': 'S0_STEP2_CHECK_C2V003', 'ok': ok, 'receipt': p, 'sha256': sha_file(p) if ok else None,
           'date_u': date_u(), 'role': plan['role']}
    if a.out:
        write_x(a.out, out)
    print(json.dumps({'ok': ok, 'receipt': p}))
    return 0 if ok else 3


def cmd_watch_check(a):
    """A135.5: the V006 WATCH_PIN MEMORY_WATCH script verifies from bytes and a process running it exists (ps).
    The watch is passive (alerts only, A166); this checks only that it runs, never what it reads."""
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
    out = {'schema': 'S0_WATCH_CHECK_C2V003', 'ok': not reasons, 'reasons': reasons, 'watch_pin': w,
           'running_processes': running[:5], 'date_u': date_u()}
    if a.out:
        write_x(a.out, out)
    print(json.dumps({'ok': out['ok'], 'reasons': reasons}))
    return 0 if out['ok'] else 3


def launches(plan):
    d = Path(plan['paths']['launches_dir'])
    return sorted(str(p) for p in d.iterdir()) if d.is_dir() else []


def read_record(plan):
    raw = Path(plan['paths']['record']).read_bytes()
    rec = strict_json(raw, 'M-15 record')
    need(rec.get('schema') == 'UNT_M15_PRELAUNCH_RECORD_C2V001', 'M15_RECORD_SCHEMA')
    return rec, sha_bytes(raw)


def cmd_order_check(a):
    """After the M-15 step (the shell script refuses earlier when the record is absent and this is not the seed serial's
    first attempt, or when launch records exist without it):
      - the record exists; no confirmed launch (LAUNCH record) of this name exists in any attempt;
      - attempt k has no record yet, and no later attempt has one;
      - attempt k > 1 (the relaunch path): attempt k-1 ended in a MISLAUNCH record of this name, written under the same
        M-15 record (sha), and its monitor receipt exists (that monitor and its driver have ended); no record refuses (a
        run failure is root's ruling, A50/A108, not this relaunch path);
      - every call other than the seed serial needs a confirmed seed serial launch (M-15; r3a L454); the twin also needs
        the seed registry entry, and nothing else: it may start any time after the seed's LAUNCH record (A166)."""
    plan = load_plan(a.plan)
    P = plan['paths']
    name, k = plan['names']['spec_pin'], plan['attempt']
    rec_exists = os.path.lexists(P['record'])
    mine = attempt_records(plan, name)
    reasons = []
    if not rec_exists:
        reasons.append('M15_RECORD_MISSING')
    launched = [r['path'] for r in mine if r['kind'] == 'LAUNCH']
    if launched:
        reasons.append('ALREADY_LAUNCHED %s' % launched)
    later = [r['path'] for r in mine if r['attempt'] >= k]
    if later:
        reasons.append('ATTEMPT_%d_OR_LATER_ALREADY_RECORDED %s' % (k, later))
    prev_info = None
    if k > 1:
        prev = [r for r in mine if r['attempt'] == k - 1]
        if not prev:
            reasons.append('NO_RECORD_OF_ATTEMPT_%d (a relaunch follows a recorded mis-launch of the previous attempt)' % (k - 1))
        elif prev[0]['kind'] != 'MISLAUNCH' or len(prev) != 1:
            reasons.append('ATTEMPT_%d_IS_NOT_A_RECORDED_MISLAUNCH (%s): the relaunch follows a procedural '
                           'mis-launch only; any other ending is root\'s ruling (A50; A108)' % (k - 1, [r['kind'] for r in prev]))
        else:
            m = strict_json(Path(prev[0]['path']).read_bytes(), 'mis-launch record')
            pa = plan['previous_attempt']
            ok_form = (m.get('schema') == RECORD_SCHEMA['MISLAUNCH'] and m.get('name') == name and m.get('attempt') == k - 1
                       and m.get('outdir') == pa['outdir'] and m.get('receipt') == pa['receipt'])
            if not ok_form:
                reasons.append('MISLAUNCH_RECORD_FORM %s' % prev[0]['path'])
            if rec_exists:
                _, rsha = read_record(plan)
                if (m.get('m15_record') or {}).get('sha256') != rsha:
                    reasons.append('MISLAUNCH_RECORD_UNDER_ANOTHER_M15_RECORD')
            if not os.path.lexists(pa['receipt']):
                reasons.append('PREVIOUS_ATTEMPT_MONITOR_RECEIPT_MISSING %s (its monitor has not ended; stop it first)'
                               % pa['receipt'])
            prev_info = {'record': prev[0]['path'], 'sha256': sha_file(prev[0]['path']),
                         'reason': m.get('launch_verdict_reason')}
    if not (plan['call'] == 'serial' and plan['role'] == 'seed'):
        seed = [r for r in attempt_records(plan, 'S0_SEED_SERIAL') if r['kind'] == 'LAUNCH']
        if not seed:
            reasons.append('SEED_SERIAL_NOT_LAUNCHED_FIRST')
    if plan['call'] == 'twin' and not os.path.lexists(P['seed_registry']):
        reasons.append('SEED_SERIAL_NOT_REGISTERED')
    print(json.dumps({'ok': not reasons, 'reasons': reasons, 'record_exists': rec_exists, 'attempt': k,
                      'attempt_records': [r['path'] for r in mine], 'previous_mislaunch': prev_info}))
    return 0 if not reasons else 3


def cmd_freeze_check(a):
    """While no launch receipt exists in this launch root (no attempt record yet: the first launch), V006 must be
    byte-identical to the V006 the M-15 record logged (path and sha256): the write freeze lasts from the record to the
    first receipt.  After a mis-launch the freeze is over (root records the mis-launch in V006)."""
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
    """A143 D3 / A147 L3-03 form: PY -I -B <monitor> then exactly the eight flags in order, each with one value (never the
    '=' forms); --driver-sha256 64 lowercase hex equal to the pin; --spec absolute; --outdir absolute under External1
    (never runs_ext); receipt = outdir + '.receipt.json'; caps equal to the call's caps of record."""
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
    """Before a kill (the twin's planned stop, or a mis-launch stop): the launch record's child is alive, leads its own
    process group, runs exactly the launch record's command, its parent is --mon-pid (when given), and the command's spec
    is the launched one (sha256 from bytes and numerics.route_a.column_workers = --expect-leaf).  stdout: the pgid (exit 0);
    exit 1: the child is not alive (nothing to stop); exit 3: refused.  The verification JSON goes to stderr."""
    lj = strict_json(Path(a.launch_json).read_bytes(), 'launch json')
    reasons = []
    pid = lj.get('child_pid')
    cmd = lj.get('command')
    spec = ((lj.get('pins') or {}).get('spec') or {})
    alive = None
    if type(pid) is not int or pid <= 1 or not isinstance(cmd, list):
        reasons.append('LAUNCH_JSON_FORM')
    else:
        if spec.get('sha256') != a.spec_sha256:
            reasons.append('LAUNCH_SPEC_IS_NOT_THE_LAUNCHED_SPEC')
        try:
            sb = Path(spec.get('path')).read_bytes()
            if sha_bytes(sb) != a.spec_sha256 or dig(strict_json(sb, 'launched spec'), LEAF) != a.expect_leaf:
                reasons.append('SPEC_BYTES_OR_LEAF')
        except (OSError, TypeError, Refusal):
            reasons.append('SPEC_UNREADABLE')
        pg = ps_field(pid, 'pgid')
        alive = bool(pg)
        if not pg:
            reasons.append('CHILD_NOT_ALIVE')
        else:
            if int(pg) != pid:
                reasons.append('CHILD_NOT_A_GROUP_LEADER')
            if ps_field(pid, 'command') != ' '.join(cmd):
                reasons.append('CHILD_COMMAND_DIFFERS (pid reuse?)')
            if a.mon_pid is not None and ps_field(pid, 'ppid') != str(a.mon_pid):
                reasons.append('CHILD_PARENT_IS_NOT_THE_MONITOR %s' % a.mon_pid)
    print(json.dumps({'ok': not reasons, 'reasons': reasons, 'pgid': pid, 'alive': alive, 'mon_pid': a.mon_pid,
                      'expect_leaf': a.expect_leaf}), file=sys.stderr)
    if alive is False:
        return 1
    if reasons:
        return 3
    print(pid)
    return 0


def cmd_kill_record(a):
    lr = Path(a.launch_root)
    d = lr / 'twin_kill'
    d.mkdir(exist_ok=True)
    rec = {'schema': 'UNT_S0_TWIN_KILL_RECORD_C2V003', 'date_u': date_u(), 'reason': a.reason, 'pgid': a.pgid,
           'result': a.result, 'launch_json': {'path': a.launch_json, 'sha256': sha_file(a.launch_json)},
           'outdir': a.outdir, 'rule': 'A141 L4: the planned twin stop after iteration 1 COMPLETED + sidecar record; not a '
                                       'failure (A135 item 3; A133 section 3(c)); the twin is never a member'}
    p = d / ('TWIN_KILL_RECORD_%s_%s.json' % (a.reason, os.path.basename(a.outdir.rstrip('/'))))
    h = write_x(p, rec)
    print(json.dumps({'status': 'WRITTEN', 'path': str(p), 'sha256': h}))
    return 0


# ------------------------------------------------------------------------------------------------------------- records
def caps_equal(caps, want):
    try:
        return isinstance(caps, dict) and all(float(caps.get(c, -1)) == float(v) for c, v in want.items())
    except (TypeError, ValueError):
        return False


def launch_checks(plan, rec, spec, spec_sha256):
    """The launch record root_monitor wrote (<receipt>.launch.json) against the plan -> (checks, raw bytes, dict, utc epoch).
    The checks are C2V002's launch-record checks, unchanged, plus 'launch_json_parseable'; an unreadable or unparseable
    launch record fails that check and never passes."""
    try:
        raw = Path(plan['launch_json']).read_bytes()
        lj = strict_json(raw, 'launch json')
        need(type(lj) is dict, 'LAUNCH_JSON_NOT_AN_OBJECT')
    except (OSError, Refusal):
        return {'launch_json_parseable': False}, None, {}, None
    expected_cmd = [plan['python'], '-I', '-B', plan['pins']['driver']['path'], 'run', '--spec', spec, '--outdir', plan['outdir']]
    pins = lj.get('pins') if isinstance(lj.get('pins'), dict) else {}
    try:
        launch_epoch = parse_iso(lj.get('utc'))
    except (TypeError, ValueError):
        launch_epoch = None
    checks = {
        'launch_json_parseable': True,
        'schema': lj.get('schema') == LAUNCH_SCHEMA,
        'command_is_planned': lj.get('command') == expected_cmd,
        'driver_pin': pins.get('driver') == {'path': plan['pins']['driver']['path'], 'sha256': plan['pins']['driver']['sha256']},
        'spec_pin': pins.get('spec') == {'path': spec, 'sha256': spec_sha256},
        'monitor_sha': isinstance(pins.get('monitor'), dict) and
        pins['monitor'].get('sha256') == plan['pins']['monitor']['sha256'],
        'caps': caps_equal(lj.get('caps'), plan['caps']),
        'retries_0': lj.get('retries_allowed') == 0,
        'child_pid': type(lj.get('child_pid')) is int,
        'm15_record_precedes_this_launch': launch_epoch is not None and launch_epoch > int(rec['date_u_epoch_s']),
    }
    return checks, raw, lj, launch_epoch


def cmd_launch_check(a):
    """The post-launch check (C2V003).  V006 A166 removed the A147 L3-03 gate reading; what is read now is the launch
    record root_monitor wrote: once <receipt>.launch.json exists, its command, driver/spec/monitor pins, caps (RSS = RAM),
    retries 0, child pid and launch time (after the M-15 record) must equal the plan's.  CONFIRMED -> exit 0.  Anything
    else, including an unreadable launch record or an error here, -> MISLAUNCH, exit 3 (fail closed: the script stops the
    launch at once).  The verdict goes to --out by exclusive create.  Nothing here reads the machine's memory or a gate."""
    plan = load_plan(a.plan)
    plan_sha = sha_file(a.plan)
    need(a.mon_pid > 1, 'LAUNCH_CHECK_ARGS')
    lj_pin, rsha, err = None, None, None
    try:
        rec, rsha = read_record(plan)
        checks, raw, lj, _ = launch_checks(plan, rec, a.spec, a.spec_sha256)
        if raw is not None:
            lj_pin = {'path': plan['launch_json'], 'sha256': sha_bytes(raw), 'child_pid': lj.get('child_pid')}
        failed = sorted(c for c, v in checks.items() if not v)
    except Exception as e:                                             # fail closed
        checks, failed, err = {}, ['LAUNCH_CHECK_ERROR'], '%s: %s' % (type(e).__name__, e)
    verdict = 'MISLAUNCH' if failed else 'CONFIRMED'
    reason = 'LAUNCH_RECORD_MATCHES_PLAN' if not failed else 'LAUNCH_RECORD_DIFFERS_FROM_PLAN %s%s' % (
        failed, (' (%s)' % err) if err else '')
    out = {'schema': 'S0_LAUNCH_VERDICT_C2V003', 'verdict': verdict, 'reason': reason, 'failed': failed, 'checks': checks,
           'mon_pid': a.mon_pid, 'call': plan['call'], 'role': plan['role'], 'attempt': plan['attempt'],
           'launch_json': lj_pin, 'm15_record_sha256': rsha, 'plan': {'path': a.plan, 'sha256': plan_sha},
           'spec': {'path': a.spec, 'sha256': a.spec_sha256}, 'caps_expected': plan['caps'], 'rule': plan['expected']['rule'],
           'date_u': date_u(), 'synthetic': plan['synthetic']}
    write_x(a.out, out)
    print(json.dumps({'verdict': verdict, 'reason': reason}))
    return 0 if verdict == 'CONFIRMED' else 3


def cmd_launch_record(a):
    """After the monitor wrote <receipt>.launch.json and launch-check ran: write this attempt's record ('x'):
      LAUNCH     the launch verdict is CONFIRMED for this monitor pid, this plan and these launch-record bytes (required);
      MISLAUNCH  the launch was stopped (procedural mis-launch, not a scientific failure); carries the launch verdict, the
                 kill-target verification, the stop result and the monitor receipt when it exists; names the relaunch.
    One record per attempt.  First record in the launch root: the launch utc must be later than the M-15 record's date -u
    second, and V006 is re-hashed (a change is flagged)."""
    plan = load_plan(a.plan)
    rec, rsha = read_record(plan)
    name, k = plan['names']['spec_pin'], plan['attempt']
    already = [r['path'] for r in attempt_records(plan, name) if r['attempt'] == k]
    need(not already, 'ATTEMPT_ALREADY_RECORDED %s' % already)
    lv, lv_pin = None, None
    if a.launch_verdict and os.path.lexists(a.launch_verdict):
        lv = strict_json(Path(a.launch_verdict).read_bytes(), 'launch verdict')
        lv_pin = pin_of(a.launch_verdict)
    checks, lj_raw, lj, launch_epoch = launch_checks(plan, rec, a.spec, a.spec_sha256)
    if a.outcome == 'LAUNCH':
        need(lv is not None and lv.get('schema') == 'S0_LAUNCH_VERDICT_C2V003' and lv.get('verdict') == 'CONFIRMED' and
             lv.get('mon_pid') == a.mon_pid and (lv.get('plan') or {}).get('sha256') == sha_file(a.plan) and
             lj_raw is not None and (lv.get('launch_json') or {}).get('sha256') == sha_bytes(lj_raw),
             'A LAUNCH RECORD NEEDS A CONFIRMED LAUNCH VERDICT FOR THIS MONITOR PID, PLAN AND LAUNCH RECORD')
    first = not launches(plan)
    flags = []
    v006_now = sha_file(plan['v006']['path'])
    if first and v006_now != rec['v006']['sha256']:
        flags.append('V006_CHANGED_BETWEEN_RECORD_AND_THIS_CHECK')
    bad = sorted(c for c, v in checks.items() if not v)
    out = {'schema': RECORD_SCHEMA[a.outcome], 'outcome': a.outcome, 'name': name, 'role': plan['role'], 'call': plan['call'],
           'attempt': k, 'first_record_in_launch_root': first, 'checks': checks, 'failed': bad, 'flags': flags,
           'm15_record': {'path': plan['paths']['record'], 'sha256': rsha, 'date_u': rec['date_u'],
                          'date_u_epoch_s': rec['date_u_epoch_s'], 'v006_sha256': rec['v006']['sha256']},
           'launch_json': {'path': plan['launch_json'], 'sha256': sha_bytes(lj_raw) if lj_raw is not None else None,
                           'utc': lj.get('utc'), 'utc_epoch_s': launch_epoch, 'child_pid': lj.get('child_pid')},
           'v006_sha256_now': v006_now, 'spec': {'path': a.spec, 'sha256': a.spec_sha256},
           'driver': plan['pins']['driver'], 'monitor': plan['pins']['monitor'], 'outdir': plan['outdir'],
           'receipt': plan['receipt'], 'caps': plan['caps'], 'caps_basis': plan['caps_basis'], 'monitor_pid': a.mon_pid,
           'watch_pid': a.watch_pid,
           'launch_check': {'verdict_file': lv_pin, 'verdict': (lv or {}).get('verdict'), 'reason': (lv or {}).get('reason'),
                            'failed': (lv or {}).get('failed'), 'rule': plan['expected']['rule']},
           'launch_verdict_reason': (lv or {}).get('reason') if lv else 'LAUNCH_CHECK_DID_NOT_RETURN_A_VERDICT',
           'work_files': {Path(p).name: {'path': p, 'sha256': sha_file(p)} for p in sorted(str(x) for x in Path(a.work).iterdir())
                          if Path(p).is_file() and Path(p).name not in ('mislaunch_record.out',)},
           'registry': {'path': plan['paths']['registry'], 'sha256': sha_file(plan['paths']['registry'])},
           'plan': {'path': a.plan, 'sha256': sha_file(a.plan)},
           'kit': plan['kit'], 'synthetic': plan['synthetic'], 'date_u': date_u(),
           'reads': 'validity-only until r3a and the M-12 classifier are sealed (A133 section 2 row 2); after every result '
                    'check result driver_sha256 = 577f8c94 (A77.1 N8)'}
    if a.outcome == 'MISLAUNCH':
        kt = None
        if a.kill_target_out and os.path.lexists(a.kill_target_out):
            try:
                kt = json.loads(Path(a.kill_target_out).read_text().strip().splitlines()[-1])
            except (ValueError, IndexError):
                kt = {'unparseable': True}
        rcpt = plan['receipt']
        out.update({
            'classification': 'PROCEDURAL_MISLAUNCH: the launch was stopped because its launch record (<receipt>.launch.json) '
                              'did not match the plan (%s); not a scientific failure; its outputs are never read' % (
                                  (lv or {}).get('failed'),),
            'stop': {'result': a.stop_result, 'pgid': a.pgid, 'kill_target': kt,
                     'kill_target_file': pin_of(a.kill_target_out) if a.kill_target_out and os.path.lexists(a.kill_target_out) else None},
            'monitor_receipt': ({'path': rcpt, 'exists': True, 'sha256': sha_file(rcpt)} if os.path.lexists(rcpt)
                                else {'path': rcpt, 'exists': False}),
            'relaunch': {'attempt': k + 1, 'launch_root': plan['launch_root'], 'm15_record': {'path': plan['paths']['record'],
                                                                                            'sha256': rsha},
                         'outdir': plan['run_root'] + '/' + run_name_for(plan['call'], ROLE_NAME[plan['role']], k + 1),
                         'how': 'the same script with --attempt %d in this launch root (order-check admits it once this '
                                'attempt\'s monitor receipt exists)' % (k + 1),
                         'root_note': 'root records this mis-launch in V006; V006 is no longer write-frozen'}})
    Path(plan['paths']['launches_dir']).mkdir(exist_ok=True)
    path = plan['paths'][{'LAUNCH': 'launch_record', 'MISLAUNCH': 'mislaunch_record'}[a.outcome]]
    h = write_x(path, out)
    print(json.dumps({'status': '%s_RECORD_WRITTEN' % a.outcome, 'path': path, 'sha256': h, 'failed': bad, 'flags': flags}))
    if a.outcome != 'LAUNCH':
        return 0
    return 3 if bad else (4 if flags else 0)


# ------------------------------------------------------------------------------------------------------------- main
def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    v = sub.add_parser('validate')
    for k in ('role', 'call', 'mode', 'launch-root', 'run-root'):
        v.add_argument('--' + k, required=True)
    v.add_argument('--attempt', default='1')
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
    lc = sub.add_parser('launch-check')
    for k in ('plan', 'spec', 'spec-sha256', 'out'):
        lc.add_argument('--' + k, required=True)
    lc.add_argument('--mon-pid', type=int, required=True)
    lr = sub.add_parser('launch-record')
    for k in ('plan', 'work', 'spec', 'spec-sha256'):
        lr.add_argument('--' + k, required=True)
    lr.add_argument('--outcome', choices=('LAUNCH', 'MISLAUNCH'), required=True)
    lr.add_argument('--mon-pid', type=int, required=True)
    lr.add_argument('--launch-verdict')
    lr.add_argument('--watch-pid', type=int)
    lr.add_argument('--stop-result', choices=('KILLED_TERM', 'KILLED_KILL', 'ALREADY_ENDED', 'NOT_KILLED_TARGET_REFUSED'))
    lr.add_argument('--kill-target-out')
    lr.add_argument('--pgid', type=int)
    t = sub.add_parser('twin-trigger')
    t.add_argument('--outdir', required=True)
    k_ = sub.add_parser('kill-target')
    k_.add_argument('--launch-json', required=True)
    k_.add_argument('--spec-sha256', required=True)
    k_.add_argument('--expect-leaf', type=int, required=True)
    k_.add_argument('--mon-pid', type=int)
    kr = sub.add_parser('kill-record')
    for x in ('launch-root', 'launch-json', 'outdir', 'result', 'reason'):
        kr.add_argument('--' + x, required=True)
    kr.add_argument('--pgid', type=int, required=True)
    a = ap.parse_args(argv)
    if a.cmd == 'launch-record' and a.outcome == 'MISLAUNCH' and not a.stop_result:
        ap.error('--outcome MISLAUNCH needs --stop-result')
    fn = {'validate': cmd_validate, 'fill-check': cmd_fill_check, 'dry-verdict': cmd_dry_verdict, 'register': cmd_register,
          'ext1-check': cmd_ext1_check,
          'step2-check': cmd_step2_check, 'watch-check': cmd_watch_check, 'order-check': cmd_order_check,
          'freeze-check': cmd_freeze_check, 'record-epoch': cmd_record_epoch, 'monitor-argv': cmd_monitor_argv,
          'launch-check': cmd_launch_check, 'launch-record': cmd_launch_record, 'twin-trigger': cmd_twin_trigger,
          'kill-target': cmd_kill_target, 'kill-record': cmd_kill_record}[a.cmd]
    try:
        return fn(a)
    except (Refusal, OSError, KeyError, TypeError, ValueError) as e:
        print(json.dumps({'status': 'REFUSED', 'step': a.cmd, 'reason': '%s: %s' % (type(e).__name__, e)}))
        return 3


if __name__ == '__main__':
    sys.exit(main())
