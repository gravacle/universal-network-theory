"""Tests for schedule_ceiling_writer_c3v002 (Claude3, backlog #8; Claude4 0258 NOTEs S2-S4). Synthetic call bindings
and receipts in WORK only. The clock is injected by replacing the module's now_utc.
usage: python3 -I -B test_schedule_ceiling_writer_c3v002.py WORK   (WORK must not exist)"""
import hashlib, json, os, subprocess, sys, tempfile, types, argparse
from pathlib import Path
HERE = Path(__file__).resolve().parent; TOOL = HERE / 'schedule_ceiling_writer_c3v002.py'
WORK = Path(sys.argv[1]); os.mkdir(WORK); PY = sys.executable
results = []
def check(name, ok, detail=''): results.append({'id': name, 'pass': bool(ok), 'detail': str(detail)[:300]})
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def pin(p): return {'path': str(p), 'sha256': sha(p)}
def put(p, obj): Path(p).write_text(json.dumps(obj, indent=2, sort_keys=True) + '\n'); return pin(p)
def load(src_text=None, name='w'):
    raw = (src_text if src_text is not None else TOOL.read_text())
    m = types.ModuleType(name); m.__file__ = str(TOOL); exec(compile(raw, str(TOOL), 'exec'), m.__dict__); return m
def call_tool(m, clock, argv):
    m.now_utc = lambda: clock
    rb = m.load_rb()
    a = argparse.Namespace(**argv)
    try:
        out = m.cmd_register(rb, a) if argv['cmd'] == 'register' else m.cmd_close(rb, a)
        return 0, out
    except m.Refused as e:
        return 2, str(e)
def listing(d): return sorted(os.listdir(d))
W = load()
# --- registration (real clock is before the Phase-2 ceiling)
rc, o = call_tool(W, '2026-10-22T14:00:00Z', {'cmd': 'register', 'phase': 'PHASE_2', 'out': str(WORK / 'REGISTRATION_PHASE_2.json')})
check('T1_register_written', rc == 0, o); reg = pin(WORK / 'REGISTRATION_PHASE_2.json')
R = json.loads(Path(reg['path']).read_text())
check('T1_registration_fields', R == {'schema': 'SCHEDULE_CEILING_REGISTRATION_C2V001', 'phase': 'PHASE_2', 'deadline_utc': '2026-12-01T05:59:00Z', 'date_u': '2026-10-22T14:00:00Z'}, R)
check('T1_no_validation_dir_left', listing(WORK) == ['REGISTRATION_PHASE_2.json'], listing(WORK))
callb = put(WORK / 'CALL_A.json', {'alternative': 'ALT_A', 'kind': 'F_POINT', 'key': 'k' * 8, 'theta_sha256': 'a' * 64, 'spec_sha256': 'b' * 64})
rcp = WORK / 'RECEIPT_A.json'; rcp.write_text('{"synthetic_receipt": true}\n'); rcpin = pin(rcp)
# --- closures at/after the ceiling
rc, o = call_tool(W, '2026-12-01T06:00:00Z', {'cmd': 'close', 'phase': 'PHASE_2', 'registration': reg['path'], 'registration_sha256': reg['sha256'], 'call': callb['path'], 'call_sha256': callb['sha256'], 'last_receipt': rcpin['path'], 'last_receipt_sha256': rcpin['sha256'], 'no_last_receipt': False, 'out': str(WORK / 'CLOSURE_A.json')})
check('T2_close_with_receipt_written', rc == 0, o)
C = json.loads((WORK / 'CLOSURE_A.json').read_text())
check('T2_closure_fields', C['schema'] == 'SCHEDULE_CEILING_CLOSURE_C2V002' and C['call'] == json.loads(Path(callb['path']).read_text()) and C['last_receipt'] == {'path': os.path.realpath(rcpin['path']), 'sha256': rcpin['sha256']} and C['date_u'] == '2026-12-01T06:00:00Z', C)
callb2 = put(WORK / 'CALL_B.json', {'alternative': 'ALT_B', 'kind': 'F_POINT', 'key': 'm' * 8, 'theta_sha256': 'c' * 64, 'spec_sha256': 'd' * 64})
rc, o = call_tool(W, '2026-12-01T06:05:00Z', {'cmd': 'close', 'phase': 'PHASE_2', 'registration': reg['path'], 'registration_sha256': reg['sha256'], 'call': callb2['path'], 'call_sha256': callb2['sha256'], 'last_receipt': None, 'last_receipt_sha256': None, 'no_last_receipt': True, 'out': str(WORK / 'CLOSURE_B.json')})
check('T3_close_without_receipt_written', rc == 0 and json.loads((WORK / 'CLOSURE_B.json').read_text())['last_receipt'] is None, o)
# --- independent consumer run on the REAL files: a policy naming both closures
rb = W.load_rb()
pol = put(WORK / 'POLICY_PHASE_2.json', {'schema': 'INTERRUPTION_POLICY_C2V002', 'phase': 'PHASE_2', 'cause_producer': None, 'deadline_utc': '2026-12-01T05:59:00Z', 'deadline_registration': reg, 'attempts': [], 'closures': [pin(WORK / 'CLOSURE_A.json'), pin(WORK / 'CLOSURE_B.json')]})
try:
    res = rb.interruption_policy(pol, 'PHASE_2'); check('T4_consumer_accepts_both_closures', len(res['closures']) == 2, len(res['closures']))
except rb.Refused as e:
    check('T4_consumer_accepts_both_closures', False, e)
# --- MUST_FAIL (no output). base uses CALL_C, which has no closure anywhere.
def mf(name, clock, argv, code):
    rc, o = call_tool(W, clock, argv); check(name, rc == 2 and code in str(o) and not Path(argv['out']).exists(), o)
callc = put(WORK / 'CALL_C.json', {'alternative': 'ALT_C', 'kind': 'F_POINT', 'key': 'n' * 8, 'theta_sha256': 'e' * 64, 'spec_sha256': 'f' * 64})
base = {'cmd': 'close', 'phase': 'PHASE_2', 'registration': reg['path'], 'registration_sha256': reg['sha256'], 'call': callc['path'], 'call_sha256': callc['sha256'], 'last_receipt': None, 'last_receipt_sha256': None, 'no_last_receipt': True}
mf('F1_close_before_ceiling', '2026-11-30T23:00:00Z', dict(base, out=str(WORK / 'X1.json')), 'CLOSURE_BEFORE_CEILING')
mf('F2_register_after_ceiling', '2026-12-02T00:00:00Z', {'cmd': 'register', 'phase': 'PHASE_2', 'out': str(WORK / 'X2.json')}, 'REGISTRATION_AFTER_CEILING')
cx = put(WORK / 'CALL_EXTRA.json', {'alternative': 'A', 'kind': 'K', 'key': 'x', 'theta_sha256': 'a' * 64, 'spec_sha256': 'b' * 64, 'extra': 1})
mf('F3_call_extra_key', '2026-12-01T06:00:00Z', dict(base, call=cx['path'], call_sha256=cx['sha256'], out=str(WORK / 'X3.json')), 'CALL_KEYS')
mf('F4_registration_sha_mismatch', '2026-12-01T06:00:00Z', dict(base, registration_sha256='0' * 64, out=str(WORK / 'X4.json')), 'SHA_MISMATCH')
r1 = put(WORK / 'REGISTRATION_PHASE_1.json', {'schema': 'SCHEDULE_CEILING_REGISTRATION_C2V001', 'phase': 'PHASE_1', 'deadline_utc': '2026-11-06T05:59:00Z', 'date_u': '2026-10-22T14:00:00Z'})
mf('F5_wrong_phase_registration', '2026-12-01T06:00:00Z', dict(base, registration=r1['path'], registration_sha256=r1['sha256'], out=str(WORK / 'X5.json')), 'REGISTRATION_SCHEMA')
late = put(WORK / 'REGISTRATION_LATE.json', {'schema': 'SCHEDULE_CEILING_REGISTRATION_C2V001', 'phase': 'PHASE_2', 'deadline_utc': '2026-12-01T05:59:00Z', 'date_u': '2026-12-01T07:00:00Z'})
mf('F6_registration_dated_after_ceiling_consumer', '2026-12-01T08:00:00Z', dict(base, registration=late['path'], registration_sha256=late['sha256'], out=str(WORK / 'X6.json')), 'CONSUMER_REFUSED')
rc, o = call_tool(W, '2026-12-01T06:00:00Z', dict(base, out=str(WORK / 'CLOSURE_A.json'))); check('F7_out_exists', rc == 2 and 'OUT_MUST_BE_NEW' in str(o), o)
rc, o = call_tool(W, '2026-12-01T06:00:00Z', dict(base, out='rel.json')); check('F8_out_relative', rc == 2 and 'OUT_ABSOLUTE_NORMALIZED' in str(o), o)
r = subprocess.run([PY, '-I', '-B', str(TOOL), 'close', '--phase', 'PHASE_2', '--registration', reg['path'], '--registration-sha256', reg['sha256'], '--call', callb['path'], '--call-sha256', callb['sha256'], '--last-receipt', rcpin['path'], '--out', str(WORK / 'X9.json')], capture_output=True, text=True)
check('F9_cli_last_receipt_pin_pair', r.returncode == 2 and 'LAST_RECEIPT_PIN_PAIR' in r.stdout, r.stdout + r.stderr)
r = subprocess.run([PY, str(TOOL), 'register', '--phase', 'PHASE_2', '--out', str(WORK / 'X10.json')], capture_output=True, text=True)
check('F10_cli_requires_isolated', r.returncode == 2 and 'RUN_WITH_-I_-B' in r.stdout, r.stdout)
r = subprocess.run([PY, '-I', '-B', str(TOOL), 'close', '--phase', 'PHASE_2', '--registration', reg['path'], '--registration-sha256', reg['sha256'], '--call', callc['path'], '--call-sha256', callc['sha256'], '--no-last-receipt', '--out', str(WORK / 'X11.json')], capture_output=True, text=True)
check('F11_cli_real_clock_close_refused_before_ceiling', r.returncode == 2 and 'CLOSURE_BEFORE_CEILING' in r.stdout and not (WORK / 'X11.json').exists(), r.stdout)
# --- c3v002 S4: PHASE_1 out of scope (register and close)
mf('S4a_register_phase1_refused', '2026-10-22T14:00:00Z', {'cmd': 'register', 'phase': 'PHASE_1', 'out': str(WORK / 'X12.json')}, 'PHASE_OUT_OF_SCOPE')
mf('S4b_close_phase1_refused', '2026-11-06T06:00:00Z', dict(base, phase='PHASE_1', registration=r1['path'], registration_sha256=r1['sha256'], out=str(WORK / 'X13.json')), 'PHASE_OUT_OF_SCOPE')
# --- c3v002 S2: one closure per call in the records folder
s2a = dict(base, call=callb['path'], call_sha256=callb['sha256'], out=str(WORK / 'X14.json'))
mf('S2a_second_closure_same_call_refused', '2026-12-01T06:10:00Z', s2a, 'CLOSURE_ALREADY_IN_FOLDER:CLOSURE_A.json')
other = WORK / 'OTHER'; other.mkdir(); (other / 'NOTES.txt').write_text('not json, ignored\n')
put(other / 'CALL_X.json', {'alternative': 'ALT_A', 'kind': 'F_POINT', 'key': 'k' * 8, 'theta_sha256': 'a' * 64, 'spec_sha256': 'b' * 64})
rc, o = call_tool(W, '2026-12-01T06:10:00Z', dict(s2a, out=str(other / 'CLOSURE_A2.json')))
check('S2b_scan_is_per_folder_other_json_ignored', rc == 0, o)
pol2 = put(WORK / 'POLICY_DUP.json', {'schema': 'INTERRUPTION_POLICY_C2V002', 'phase': 'PHASE_2', 'cause_producer': None, 'deadline_utc': '2026-12-01T05:59:00Z', 'deadline_registration': reg, 'attempts': [], 'closures': [pin(WORK / 'CLOSURE_A.json'), pin(other / 'CLOSURE_A2.json')]})
try:
    rb.interruption_policy(pol2, 'PHASE_2'); check('S2c_consumer_backstop_refuses_both_named', False, 'accepted')
except rb.Refused as e:
    check('S2c_consumer_backstop_refuses_both_named', 'SCHEDULE_CEILING_DUPLICATE' in str(e), e)
for tag, setup, code in (('S2d_unreadable_json_refused', lambda d: (d / 'BROKEN.json').write_text('{'), 'FOLDER_JSON_UNREADABLE:BROKEN.json'),
                         ('S2e_symlinked_json_refused', lambda d: os.symlink(WORK / 'CLOSURE_A.json', d / 'LINK.json'), 'FOLDER_JSON_NOT_REGULAR:LINK.json'),
                         ('S2f_malformed_closure_refused', lambda d: put(d / 'C.json', {'schema': 'SCHEDULE_CEILING_CLOSURE_C2V002', 'phase': 'PHASE_2', 'call': {'alternative': 'x'}}), 'FOLDER_CLOSURE_MALFORMED:C.json')):
    d = WORK / tag; d.mkdir(); setup(d)
    mf(tag, '2026-12-01T06:10:00Z', dict(base, out=str(d / 'OUT.json')), code)
# --- c3v002 S3: validation copies never inside the records folder
S3 = WORK / 'S3'; S3.mkdir()
def instrument(m, fail_consumer=False, tmp_dir=None):
    made, seen = [], []
    real_mkdtemp = tempfile.mkdtemp
    def mk(prefix):
        p = real_mkdtemp(prefix=prefix, dir=tmp_dir); made.append(p); return p
    m.tempfile = types.SimpleNamespace(mkdtemp=mk)
    orig_load = m.load_rb
    def load_rb():
        r = orig_load(); inner = r.interruption_policy
        def wrapped(p, ph):
            seen.append(listing(S3))
            if fail_consumer:
                raise RuntimeError('simulated crash inside the consumer run')
            return inner(p, ph)
        r.interruption_policy = wrapped; return r
    m.load_rb = load_rb
    return made, seen
W3 = load(name='w3'); before = listing(S3)
made, seen = instrument(W3)
rc, o = call_tool(W3, '2026-10-22T14:00:00Z', {'cmd': 'register', 'phase': 'PHASE_2', 'out': str(S3 / 'REG.json')})
outside = all(not os.path.realpath(p).startswith(os.path.realpath(WORK) + os.sep) for p in made)
check('S3a_register_validation_dirs_outside_and_removed', rc == 0 and len(made) == 2 and outside and not any(os.path.lexists(p) for p in made), (o, made))
check('S3b_records_folder_unchanged_during_validation', seen == [before] and listing(S3) == ['REG.json'], (seen, listing(S3)))
regs3 = pin(S3 / 'REG.json')
W4 = load(name='w4'); made, seen = instrument(W4)
rc, o = call_tool(W4, '2026-12-01T06:00:00Z', dict(base, registration=regs3['path'], registration_sha256=regs3['sha256'], out=str(S3 / 'CLOSE.json')))
check('S3c_close_validation_dir_outside_and_removed', rc == 0 and len(made) == 1 and seen == [['REG.json']] and not os.path.lexists(made[0]), (o, made, seen))
W5 = load(name='w5'); made, seen = instrument(W5, fail_consumer=True)
try:
    call_tool(W5, '2026-12-01T06:00:00Z', dict(base, call=callb2['path'], call_sha256=callb2['sha256'], registration=regs3['path'], registration_sha256=regs3['sha256'], out=str(S3 / 'CRASH.json'))); crashed = False
except RuntimeError:
    crashed = True
check('S3d_crash_in_consumer_leaves_records_folder_clean', crashed and listing(S3) == ['CLOSE.json', 'REG.json'] and not any(os.path.lexists(p) for p in made), (crashed, listing(S3), made))
W6 = load(name='w6'); made, seen = instrument(W6, tmp_dir=str(S3))
rc, o = call_tool(W6, '2026-10-22T14:00:00Z', {'cmd': 'register', 'phase': 'PHASE_2', 'out': str(S3 / 'REG2.json')})
check('S3e_tmpdir_inside_records_folder_refused', rc == 2 and 'VALIDATION_DIR_IN_RECORDS_FOLDER' in str(o) and listing(S3) == ['CLOSE.json', 'REG.json'], (o, listing(S3)))
check('no_refused_output', not any((WORK / ('X%d.json' % i)).exists() for i in range(1, 15)))
# --- mutants: each removes one c3v002 guard (or the consumer run); a test above must then fail
src = TOOL.read_text()
def mutant(name, old, new, n=1):
    assert src.count(old) == n, name
    return load(src.replace(old, new), name)
killed = {}
MD = WORK / 'MUT'; MD.mkdir()
M = mutant('M1', "    res = validate_with_consumer(rb, a.phase, reg_pin, os.path.dirname(a.out), raw)\n    need(len(res['closures']) == 1, 'CONSUMER_CLOSURE_COUNT')\n", '')
rc, o = call_tool(M, '2026-12-01T08:00:00Z', dict(base, registration=late['path'], registration_sha256=late['sha256'], out=str(MD / 'M1.json'))); killed['M1_no_consumer_run_F6_passes'] = rc == 0
M = mutant('M2', "    folder_has_no_closure_for(rb, os.path.dirname(a.out), a.phase, call)\n", '')
rc, o = call_tool(M, '2026-12-01T06:10:00Z', dict(s2a, out=str(WORK / 'M2.json'))); killed['M2_no_duplicate_scan_S2a_passes'] = rc == 0
M = mutant('M3', " and a.phase in PHASES_IN_SCOPE, 'PHASE_OUT_OF_SCOPE')", ", 'PHASE_OUT_OF_SCOPE')", 2)
rc, o = call_tool(M, '2026-10-22T14:00:00Z', {'cmd': 'register', 'phase': 'PHASE_1', 'out': str(MD / 'M3.json')}); killed['M3_no_phase_scope_S4a_passes'] = rc == 0
M = mutant('M4', "    work = tempfile.mkdtemp(prefix='schedule_ceiling_validation_')\n    real, rec = os.path.realpath(work), os.path.realpath(records_dir)\n    if real == rec or real.startswith(rec + os.sep):\n        shutil.rmtree(work)\n        raise Refused('VALIDATION_DIR_IN_RECORDS_FOLDER')\n",
           "    work = tempfile.mkdtemp(prefix='.schedule_ceiling_validation_', dir=records_dir)\n")
S3m = WORK / 'S3M'; S3m.mkdir(); M.now_utc = lambda: '2026-10-22T14:00:00Z'
seen_m = []
orig = M.load_rb
def lr():
    r = orig(); inner = r.interruption_policy
    def w(p, ph): seen_m.append(listing(S3m)); return inner(p, ph)
    r.interruption_policy = w; return r
M.load_rb = lr
rc, o = call_tool(M, '2026-10-22T14:00:00Z', {'cmd': 'register', 'phase': 'PHASE_2', 'out': str(S3m / 'REG.json')})
killed['M4_validation_dir_in_records_folder_S3b_detects'] = rc == 0 and seen_m != [[]]
M = mutant('M5', "    if real == rec or real.startswith(rec + os.sep):\n        shutil.rmtree(work)\n        raise Refused('VALIDATION_DIR_IN_RECORDS_FOLDER')\n", '')
S3g = WORK / 'S3G'; S3g.mkdir()
real_mkdtemp = tempfile.mkdtemp
M.tempfile = types.SimpleNamespace(mkdtemp=lambda prefix: real_mkdtemp(prefix=prefix, dir=str(S3g)))
rc, o = call_tool(M, '2026-10-22T14:00:00Z', {'cmd': 'register', 'phase': 'PHASE_2', 'out': str(S3g / 'REG2.json')}); killed['M5_no_guard_S3e_passes'] = rc == 0
check('all_mutants_killed', all(killed.values()), killed)
rec = {'schema': 'TEST_SCHEDULE_CEILING_WRITER_C3V002', 'tool': pin(TOOL), 'consumer_sha256': W.RB_SHA, 'python': sys.version.split()[0],
       'n': len(results), 'passed': sum(x['pass'] for x in results), 'results': results, 'mutants': killed}
(WORK / 'TEST_RECORD.json').write_text(json.dumps(rec, indent=1, sort_keys=True) + '\n')
print(json.dumps({'n': rec['n'], 'passed': rec['passed'], 'failed': [x['id'] for x in results if not x['pass']], 'mutants': killed}))
