"""Tests for schedule_ceiling_writer_c3v001 (Claude3, backlog #8). Synthetic call bindings and receipts in WORK only.
The clock is injected by replacing the module's now_utc (closures can only be written at or after the ceiling).
usage: python3 -I -B test_schedule_ceiling_writer_c3v001.py WORK   (WORK must not exist)"""
import hashlib, json, os, subprocess, sys, types, argparse
from pathlib import Path
HERE = Path(__file__).resolve().parent; TOOL = HERE / 'schedule_ceiling_writer_c3v001.py'
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
W = load()
# --- registration (real clock is before the Phase-2 ceiling)
rc, o = call_tool(W, '2026-10-22T14:00:00Z', {'cmd': 'register', 'phase': 'PHASE_2', 'out': str(WORK / 'REGISTRATION_PHASE_2.json')})
check('T1_register_written', rc == 0, o); reg = pin(WORK / 'REGISTRATION_PHASE_2.json')
R = json.loads(Path(reg['path']).read_text())
check('T1_registration_fields', R == {'schema': 'SCHEDULE_CEILING_REGISTRATION_C2V001', 'phase': 'PHASE_2', 'deadline_utc': '2026-12-01T05:59:00Z', 'date_u': '2026-10-22T14:00:00Z'}, R)
check('T1_no_validation_dir_left', not any(p.name.startswith('.schedule_ceiling') for p in WORK.iterdir()))
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
# --- MUST_FAIL (no output)
def mf(name, clock, argv, code):
    rc, o = call_tool(W, clock, argv); check(name, rc == 2 and code in str(o) and not Path(argv['out']).exists(), o)
base = {'cmd': 'close', 'phase': 'PHASE_2', 'registration': reg['path'], 'registration_sha256': reg['sha256'], 'call': callb['path'], 'call_sha256': callb['sha256'], 'last_receipt': None, 'last_receipt_sha256': None, 'no_last_receipt': True}
mf('F1_close_before_ceiling', '2026-11-30T23:00:00Z', dict(base, out=str(WORK / 'X1.json')), 'CLOSURE_BEFORE_CEILING')
mf('F2_register_after_ceiling', '2026-12-02T00:00:00Z', {'cmd': 'register', 'phase': 'PHASE_2', 'out': str(WORK / 'X2.json')}, 'REGISTRATION_AFTER_CEILING')
cx = put(WORK / 'CALL_EXTRA.json', {'alternative': 'A', 'kind': 'K', 'key': 'x', 'theta_sha256': 'a' * 64, 'spec_sha256': 'b' * 64, 'extra': 1})
mf('F3_call_extra_key', '2026-12-01T06:00:00Z', dict(base, call=cx['path'], call_sha256=cx['sha256'], out=str(WORK / 'X3.json')), 'CALL_KEYS')
mf('F4_registration_sha_mismatch', '2026-12-01T06:00:00Z', dict(base, registration_sha256='0' * 64, out=str(WORK / 'X4.json')), 'SHA_MISMATCH')
r1 = put(WORK / 'REGISTRATION_PHASE_1.json', {'schema': 'SCHEDULE_CEILING_REGISTRATION_C2V001', 'phase': 'PHASE_1', 'deadline_utc': '2026-11-06T05:59:00Z', 'date_u': '2026-10-22T14:00:00Z'})
mf('F5_wrong_phase_registration', '2026-12-01T06:00:00Z', dict(base, registration=r1['path'], registration_sha256=r1['sha256'], out=str(WORK / 'X5.json')), 'REGISTRATION_SCHEMA')
late = put(WORK / 'REGISTRATION_LATE.json', {'schema': 'SCHEDULE_CEILING_REGISTRATION_C2V001', 'phase': 'PHASE_2', 'deadline_utc': '2026-12-01T05:59:00Z', 'date_u': '2026-12-01T07:00:00Z'})
mf('F6_registration_dated_after_ceiling_consumer', '2026-12-01T08:00:00Z', dict(base, registration=late['path'], registration_sha256=late['sha256'], out=str(WORK / 'X6.json')), 'CONSUMER_REFUSED')
mf('F7_out_exists', '2026-12-01T06:00:00Z', dict(base, out=str(WORK / 'CLOSURE_A.json')), 'OUT_MUST_BE_NEW') if False else None
rc, o = call_tool(W, '2026-12-01T06:00:00Z', dict(base, out=str(WORK / 'CLOSURE_A.json'))); check('F7_out_exists', rc == 2 and 'OUT_MUST_BE_NEW' in str(o), o)
rc, o = call_tool(W, '2026-12-01T06:00:00Z', dict(base, out='rel.json')); check('F8_out_relative', rc == 2 and 'OUT_ABSOLUTE_NORMALIZED' in str(o), o)
r = subprocess.run([PY, '-I', '-B', str(TOOL), 'close', '--phase', 'PHASE_2', '--registration', reg['path'], '--registration-sha256', reg['sha256'], '--call', callb['path'], '--call-sha256', callb['sha256'], '--last-receipt', rcpin['path'], '--out', str(WORK / 'X9.json')], capture_output=True, text=True)
check('F9_cli_last_receipt_pin_pair', r.returncode == 2 and 'LAST_RECEIPT_PIN_PAIR' in r.stdout, r.stdout + r.stderr)
r = subprocess.run([PY, str(TOOL), 'register', '--phase', 'PHASE_2', '--out', str(WORK / 'X10.json')], capture_output=True, text=True)
check('F10_cli_requires_isolated', r.returncode == 2 and 'RUN_WITH_-I_-B' in r.stdout, r.stdout)
r = subprocess.run([PY, '-I', '-B', str(TOOL), 'close', '--phase', 'PHASE_2', '--registration', reg['path'], '--registration-sha256', reg['sha256'], '--call', callb['path'], '--call-sha256', callb['sha256'], '--no-last-receipt', '--out', str(WORK / 'X11.json')], capture_output=True, text=True)
check('F11_cli_real_clock_close_refused_before_ceiling', r.returncode == 2 and 'CLOSURE_BEFORE_CEILING' in r.stdout and not (WORK / 'X11.json').exists(), r.stdout)
check('no_refused_output_or_validation_dir', not any((WORK / ('X%d.json' % i)).exists() for i in range(1, 12)) and not any(p.name.startswith('.schedule_ceiling') for p in WORK.iterdir()))
# --- mutant: drop the consumer run in close; F6 (only the consumer catches it) must then pass
src = TOOL.read_text(); old = "    res = validate_with_consumer(rb, a.phase, reg_pin, raw)\n    need(len(res['closures']) == 1, 'CONSUMER_CLOSURE_COUNT')\n"
assert src.count(old) == 1
M = load(src.replace(old, ''), 'mutant')
rc, o = call_tool(M, '2026-12-01T08:00:00Z', dict(base, registration=late['path'], registration_sha256=late['sha256'], out=str(WORK / 'M1_out.json')))
check('M1_mutant_without_consumer_killed', rc == 0, o)
rec = {'schema': 'TEST_SCHEDULE_CEILING_WRITER_C3V001', 'tool': pin(TOOL), 'n': len(results), 'passed': sum(x['pass'] for x in results), 'results': results}
(WORK / 'TEST_RECORD.json').write_text(json.dumps(rec, indent=1, sort_keys=True) + '\n')
print(json.dumps({'n': rec['n'], 'passed': rec['passed'], 'failed': [x['id'] for x in results if not x['pass']]}))
