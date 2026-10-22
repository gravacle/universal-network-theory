"""Tests for l2_root_records_writer_c3v001 (Claude3, D031). Real producers: two fresh P2 captures and Codex1's stage-a writer.
Synthetic: the freeze record, the pinned spec/tool files, the call roots (all inside WORK). No launch, no science.
usage: python3 -I -B test_l2_root_records_writer_c3v001.py WORK   (WORK must not exist)"""
import hashlib, json, os, subprocess, sys, time, types
from datetime import datetime, timezone, timedelta
from pathlib import Path
HERE = Path(__file__).resolve().parent; TOOL = HERE / 'l2_root_records_writer_c3v001.py'
CX1 = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/external_importer_cx1')
P2 = CX1 / 'runtime_distribution_capture_cx1v004.py'; STAGEA = CX1 / 'speculative_register_writer_cx1v001.py'
PY = sys.executable; WORK = Path(sys.argv[1]); os.mkdir(WORK)
results = []
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def pin(p): return {'path': str(p), 'sha256': sha(p)}
def put(p, obj): Path(p).write_text(json.dumps(obj, indent=2, sort_keys=True) + '\n'); return pin(p)
def check(name, ok, detail=''):
    results.append({'id': name, 'pass': bool(ok), 'detail': str(detail)[:300]})
def run(args, tool=TOOL):
    r = subprocess.run([PY, '-I', '-B', str(tool)] + args, capture_output=True, text=True, env={'PATH': '/usr/bin:/bin', 'HOME': os.environ.get('HOME', '/tmp')})
    try: out = json.loads(r.stdout.strip().splitlines()[-1])
    except Exception: out = {'raw': r.stdout + r.stderr}
    return r.returncode, out
def capture(p):
    r = subprocess.run([PY, '-I', '-B', str(P2), '--output', str(p)], capture_output=True, text=True, env={'PATH': '/usr/bin:/bin', 'HOME': os.environ.get('HOME', '/tmp')})
    assert r.returncode == 0, r.stderr; return pin(p)
iso = lambda t: t.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
# --- fixtures
fz = WORK / 'FREEZE.json'; frz = put(fz, {'schema': 'CX1_IMPORTER_FREEZE_V001', 'utc': iso(datetime.now(timezone.utc) - timedelta(seconds=5)),
          'policy': pin(CX1 / 'IMPORTER_POLICY_CX1V007_F2.json'), 'entry': pin(CX1 / 'importer_entry_cx1v001.py')})
time.sleep(1.1)
dcap = capture(WORK / 'DIRECT_CAPTURE.json')
OUT_ROOT = WORK / 'OUTPUT_ROOT'; OUT_ROOT.mkdir()
tools = {n: put(WORK / (n + '.json'), {'synthetic': n}) for n in ('launcher', 'guard', 'binder', 'dbp')}
entries = []
for row in (28, 29, 30, 31, 300, 301, 302):
    key = hashlib.sha256(('key%d' % row).encode()).hexdigest()
    spec = put(WORK / ('SPEC_R%d.json' % row), {'synthetic_spec': row})
    entries.append({'row': row, 'key': key, 'spec': spec, 'call_root': str(OUT_ROOT / ('DDO154_JACOBIAN_R%d_%s_A1' % (row, key[:16]))), 'attempt': 1,
                    'launcher': tools['launcher'], 'guard': tools['guard'], 'binder': tools['binder'], 'dbp': tools['dbp'], 'runtime_capture': dcap})
meta = put(WORK / 'REGISTER_META.json', {'schema': 'SPECULATIVE_REGISTER_L2_V001', 'entries': entries})
r = subprocess.run([PY, '-I', '-B', str(STAGEA), '--input', meta['path'], '--input-sha256', meta['sha256'], '--output', str(WORK / 'REGISTER.json')], capture_output=True, text=True)
check('stagea_writer_publishes_register', r.returncode == 0, r.stdout + r.stderr); reg = pin(WORK / 'REGISTER.json')
base = ['--register', reg['path'], '--register-sha256', reg['sha256'], '--freeze', frz['path'], '--freeze-sha256', frz['sha256']]
# --- positive: direct-launch
rc, o = run(['direct-launch'] + base + ['--direct-capture', dcap['path'], '--direct-capture-sha256', dcap['sha256'], '--out', str(WORK / 'LAUNCH.json')])
check('P1_direct_launch_written', rc == 0 and o.get('written', {}).get('path') == str(WORK / 'LAUNCH.json'), o)
lch = pin(WORK / 'LAUNCH.json'); L = json.loads(Path(lch['path']).read_text())
check('P1_launch_record_fields', set(L) == {'schema', 'utc', 'register', 'runtime_capture', 'interpreter', 'freeze'} and L['register'] == reg and L['runtime_capture'] == dcap and L['freeze'] == frz, L)
time.sleep(1.1)
ccap = capture(WORK / 'CAMPAIGN_CAPTURE.json')
ctx = {'config_sha256': 'a' * 64, 'cache_id': 'b' * 64, 'gate_digest': 'c' * 64}
cargs = ['--config-sha256', ctx['config_sha256'], '--cache-id', ctx['cache_id'], '--gate-digest', ctx['gate_digest']]
bargs = base + ['--direct-launch', lch['path'], '--direct-launch-sha256', lch['sha256'], '--campaign-capture', ccap['path'], '--campaign-capture-sha256', ccap['sha256']] + cargs
rc, o = run(['binding'] + bargs + ['--out', str(WORK / 'BINDING.json')])
check('P2_binding_written', rc == 0, o); bnd = pin(WORK / 'BINDING.json')
# --- independent consumer check: the importer's own join (registered_runtime_cx1v005), loaded by path from CX1
sys.path.insert(0, str(CX1))
import snapshot_cx1v001 as SN, registered_runtime_cx1v005 as RR
dcap_rec = json.loads(Path(dcap['path']).read_text())
policy = {'campaign_capture': ccap, 'producer': dcap_rec['producer'], 'driver': {'path': dcap_rec['driver']['path'] if 'path' in dcap_rec['driver'] else dcap_rec['driver']['realpath'], 'sha256': dcap_rec['driver']['sha256']},
          'monitor': {'path': dcap_rec['monitor']['path'] if 'path' in dcap_rec['monitor'] else dcap_rec['monitor']['realpath'], 'sha256': dcap_rec['monitor']['sha256']},
          'output_root': str(OUT_ROOT), 'freeze': frz, 'direct_launch': lch}
try:
    res = RR.check_registered_runtime(SN.Snapshot(), register_pin=reg, binding_pin=bnd, context=ctx, key=entries[3]['key'], spec_pin=entries[3]['spec'], runtime_policy=policy)
    check('P3_importer_join_accepts_records', res.get('registered') is True and res.get('launch_checks', {}).get('launch_association_verified') is True, res.get('comparison'))
except BaseException as e:
    check('P3_importer_join_accepts_records', False, '%s: %s' % (type(e).__name__, e))
# --- MUST_FAIL
def mf(name, args, code):
    rc, o = run(args); check(name, rc == 2 and code in str(o.get('refused', '')), o)
mf('F1_register_sha_mismatch', ['direct-launch', '--register', reg['path'], '--register-sha256', '0' * 64] + base[4:] + ['--direct-capture', dcap['path'], '--direct-capture-sha256', dcap['sha256'], '--out', str(WORK / 'X1.json')], 'SHA_MISMATCH:register')
bad_frz = put(WORK / 'FREEZE_BAD.json', {'schema': 'WRONG', 'utc': '2026-10-22T00:00:00Z', 'policy': frz, 'entry': frz})
mf('F2_freeze_schema', ['direct-launch', '--register', reg['path'], '--register-sha256', reg['sha256'], '--freeze', bad_frz['path'], '--freeze-sha256', bad_frz['sha256'], '--direct-capture', dcap['path'], '--direct-capture-sha256', dcap['sha256'], '--out', str(WORK / 'X2.json')], 'FREEZE_SCHEMA')
mf('F3_direct_capture_not_registered', ['direct-launch'] + base + ['--direct-capture', ccap['path'], '--direct-capture-sha256', ccap['sha256'], '--out', str(WORK / 'X3.json')], 'DIRECT_CAPTURE_NOT_THE_REGISTERED_ONE')
late = put(WORK / 'FREEZE_LATE.json', {'schema': 'CX1_IMPORTER_FREEZE_V001', 'utc': iso(datetime.now(timezone.utc) + timedelta(hours=1)), 'policy': frz, 'entry': frz})
mf('F4_capture_before_freeze', ['direct-launch', '--register', reg['path'], '--register-sha256', reg['sha256'], '--freeze', late['path'], '--freeze-sha256', late['sha256'], '--direct-capture', dcap['path'], '--direct-capture-sha256', dcap['sha256'], '--out', str(WORK / 'X4.json')], 'CAPTURE_BEFORE_FREEZE')
e2 = json.loads(json.dumps(entries)); e2[6]['runtime_capture'] = ccap
m2 = put(WORK / 'REGISTER_META2.json', {'schema': 'SPECULATIVE_REGISTER_L2_V001', 'entries': e2})
subprocess.run([PY, '-I', '-B', str(STAGEA), '--input', m2['path'], '--input-sha256', m2['sha256'], '--output', str(WORK / 'REGISTER2.json')], capture_output=True); reg2 = pin(WORK / 'REGISTER2.json')
mf('F5_register_two_captures', ['direct-launch', '--register', reg2['path'], '--register-sha256', reg2['sha256']] + base[4:] + ['--direct-capture', dcap['path'], '--direct-capture-sha256', dcap['sha256'], '--out', str(WORK / 'X5.json')], 'REGISTER_ONE_DIRECT_CAPTURE')
mf('F6_out_exists', ['direct-launch'] + base + ['--direct-capture', dcap['path'], '--direct-capture-sha256', dcap['sha256'], '--out', lch['path']], 'OUT_MUST_BE_NEW')
mf('F7_out_relative', ['direct-launch'] + base + ['--direct-capture', dcap['path'], '--direct-capture-sha256', dcap['sha256'], '--out', 'rel.json'], 'OUT_ABSOLUTE_NORMALIZED')
mf('F8_context_form', ['binding'] + bargs[:-6] + ['--config-sha256', 'xyz', '--cache-id', ctx['cache_id'], '--gate-digest', ctx['gate_digest'], '--out', str(WORK / 'X8.json')], 'CONTEXT_FORM')
crec = json.loads(Path(ccap['path']).read_text()); crec['interpreter'] = dict(crec['interpreter'], sha256='e' * 64); cbad = put(WORK / 'CAMPAIGN_INTERP_BAD.json', crec)
mf('F9_campaign_runtime_differs', ['binding'] + base + ['--direct-launch', lch['path'], '--direct-launch-sha256', lch['sha256'], '--campaign-capture', cbad['path'], '--campaign-capture-sha256', cbad['sha256']] + cargs + ['--out', str(WORK / 'X9.json')], 'RUNTIME_DIRECT_CAMPAIGN_DIFFER')
lbad_obj = dict(L, register=reg2); lbad = put(WORK / 'LAUNCH_BAD.json', lbad_obj)
mf('F10_launch_record_wrong_register', ['binding'] + base + ['--direct-launch', lbad['path'], '--direct-launch-sha256', lbad['sha256'], '--campaign-capture', ccap['path'], '--campaign-capture-sha256', ccap['sha256']] + cargs + ['--out', str(WORK / 'X10.json')], 'CONSUMER_REFUSED')
prec = json.loads(Path(ccap['path']).read_text()); prec['producer'] = {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/external_importer_cx1/runtime_capture_entry_cx1v003.py', 'sha256': 'c58aff70' + '0' * 56}; pbad = put(WORK / 'CAMPAIGN_P1.json', prec)
mf('F11_capture_not_P2', ['binding'] + base + ['--direct-launch', lch['path'], '--direct-launch-sha256', lch['sha256'], '--campaign-capture', pbad['path'], '--campaign-capture-sha256', pbad['sha256']] + cargs + ['--out', str(WORK / 'X11.json')], 'CAPTURE_PRODUCER')
r = subprocess.run([PY, str(TOOL), 'direct-launch'] + base + ['--direct-capture', dcap['path'], '--direct-capture-sha256', dcap['sha256'], '--out', str(WORK / 'X12.json')], capture_output=True, text=True)
check('F12_requires_isolated', r.returncode == 2 and 'RUN_WITH_-I_-B' in r.stdout, r.stdout)
check('no_refused_output_written', not any((WORK / ('X%d.json' % i)).exists() for i in range(1, 13)))
# --- mutants: each removes one guard; the named MUST_FAIL must then stop refusing
src = TOOL.read_text()
MUT = {'M1_no_one_capture': ("need(len(caps) == 1, 'REGISTER_ONE_DIRECT_CAPTURE')", 'pass', 'F5'),
       'M2_no_producer': ("need(rec.get('producer') == P2_PRODUCER, 'CAPTURE_PRODUCER_NOT_P2:' + label)", 'pass', 'F11'),
       'M3_no_compare': ("R.compare(direct, campaign)", 'pass', 'F9'),
       'M4_no_freeze_window': ("need(parse_utc(frz['utc'], 'freeze') < parse_utc(rec.get('captured_utc'), label), 'CAPTURE_BEFORE_FREEZE:' + label)", 'pass', 'F4')}
killed = {}
for name, (old, new, target) in MUT.items():
    assert src.count(old) == 1, name
    mp = HERE / ('.mut_%s.py' % name) if False else WORK / ('%s.py' % name); mp.write_text(src.replace(old, new))
    if target == 'F5': args = ['direct-launch', '--register', reg2['path'], '--register-sha256', reg2['sha256']] + base[4:] + ['--direct-capture', dcap['path'], '--direct-capture-sha256', dcap['sha256'], '--out', str(WORK / ('%s_out.json' % name))]
    elif target == 'F4': args = ['direct-launch', '--register', reg['path'], '--register-sha256', reg['sha256'], '--freeze', late['path'], '--freeze-sha256', late['sha256'], '--direct-capture', dcap['path'], '--direct-capture-sha256', dcap['sha256'], '--out', str(WORK / ('%s_out.json' % name))]
    elif target == 'F11': args = ['binding'] + base + ['--direct-launch', lch['path'], '--direct-launch-sha256', lch['sha256'], '--campaign-capture', pbad['path'], '--campaign-capture-sha256', pbad['sha256']] + cargs + ['--out', str(WORK / ('%s_out.json' % name))]
    else: args = ['binding'] + base + ['--direct-launch', lch['path'], '--direct-launch-sha256', lch['sha256'], '--campaign-capture', cbad['path'], '--campaign-capture-sha256', cbad['sha256']] + cargs + ['--out', str(WORK / ('%s_out.json' % name))]
    rc, o = run(args, tool=mp)
    killed[name] = not (rc == 2 and 'REGISTER_ONE_DIRECT_CAPTURE' in str(o) or rc == 2 and target != 'F5' and ('CAPTURE_PRODUCER_NOT_P2' in str(o) if target == 'F11' else 'RUNTIME_DIRECT_CAMPAIGN_DIFFER' in str(o) if target == 'F9' else 'CAPTURE_BEFORE_FREEZE' in str(o)))
check('mutants_all_killed', all(killed.values()), killed)
rec = {'schema': 'TEST_L2_ROOT_RECORDS_WRITER_C3V001', 'tool': pin(TOOL), 'n': len(results), 'passed': sum(r['pass'] for r in results), 'results': results, 'mutants': killed}
(WORK / 'TEST_RECORD.json').write_text(json.dumps(rec, indent=1, sort_keys=True) + '\n')
print(json.dumps({'n': rec['n'], 'passed': rec['passed'], 'failed': [r['id'] for r in results if not r['pass']], 'mutants': killed}))
