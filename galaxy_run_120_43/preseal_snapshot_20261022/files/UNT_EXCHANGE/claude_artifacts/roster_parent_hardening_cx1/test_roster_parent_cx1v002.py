"""Backlog7: actual CLI parent preflight with ledger-producing test seams."""
import contextlib, hashlib, io, json, os, sys, types, datetime, re, stat, math, _strptime
from pathlib import Path
SOURCE = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/roster_parent_hardening_cx1/roster_builder_cw8_parent_cx1v001.py')
EXPECTED = 'c8c38ee43307efb13a8bb7e91ee2203cb9f15dd8ab393c133b65b580f6797ed5'
raw = SOURCE.read_bytes()
assert hashlib.sha256(raw).hexdigest() == EXPECTED
WORK = Path(sys.argv[1]).resolve(); WORK.mkdir()

def audit(event, args):
    if event.startswith('socket.') or event in ('subprocess.Popen','os.system','os.rename','os.remove','os.rmdir','os.kill'):
        raise AssertionError('FENCE:' + event)
    if event == 'open' and isinstance(args[0], (str,bytes,os.PathLike)):
        p = Path(os.path.realpath(os.fsdecode(args[0])))
        assert p == WORK or WORK in p.parents, ('READ_WRITE_FENCE', str(p))
        if args[2] & (os.O_WRONLY | os.O_RDWR): assert not os.path.lexists(p), 'NO_OVERWRITE'
sys.addaudithook(audit)
results = []
index = 0
for command in ('step7','custody'):
 for scenario in ('missing_parent','parent_is_file','valid_parent','relative_valid_parent','missing_parent_mutant'):
    index += 1
    root = WORK / ('case_%02d' % index); root.mkdir()
    candidate = raw.decode()
    guard = "            if not os.path.isdir(os.path.dirname(os.path.abspath(args['--out-dir']))):\n                raise Refused('OUT_DIR_PARENT_MISSING', args['--out-dir'])\n"
    assert candidate.count(guard) == 2
    if scenario == 'missing_parent_mutant': candidate = candidate.replace(guard, '')
    M = types.ModuleType('roster_tested'); M.__file__ = str(SOURCE)
    exec(compile(candidate, str(SOURCE), 'exec'), M.__dict__)
    parent = root / 'parent'
    if scenario in ('valid_parent','relative_valid_parent'): parent.mkdir()
    elif scenario == 'parent_is_file':
        with parent.open('x') as f: f.write('inert')
    destination = str(parent / 'out')
    if scenario == 'relative_valid_parent': destination = os.path.relpath(destination)
    doc = {'schema': 'STEP7_INPUT_C2V003' if command == 'step7' else 'CUSTODY_INPUT_C2V007', 'build_record':{}, 'replay_plan':{}}
    if command == 'step7': doc.update(pass_one={}, pass_k={})
    M._cmd_input = lambda *args: (doc,None)
    entered = []
    ledger = root / 'LEDGER_TEST_SEAM.json'
    def operation(*args):
        entered.append(True)
        with ledger.open('x') as f: f.write('{}')
        return {'status':'NO_NEW_DISCREPANCY','seq':1}, b'{}\n', b'{}\n'
    M.step7_run = operation; M.custody_run = operation
    stdout, stderr = io.StringIO(), io.StringIO()
    error = None
    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        try: rc = M.main([command,'--input',str(root/'inert-input.json'),'--input-sha256','0'*64,'--out-dir',destination])
        except OSError as exc: rc=None;error=type(exc).__name__
    if scenario == 'missing_parent_mutant':
        assert entered and ledger.exists() and error == 'FileNotFoundError'
        try: assert not entered and not ledger.exists()
        except AssertionError: pass
        else: raise AssertionError('parent guard mutant survived')
    elif scenario in ('missing_parent','parent_is_file'):
        assert rc == 2 and json.loads(stderr.getvalue())['refused'] == 'OUT_DIR_PARENT_MISSING', stderr.getvalue()
        assert not entered and not ledger.exists() and not Path(destination).exists()
    else:
        assert rc == 0 and entered and ledger.exists(), (rc,stderr.getvalue())
        expected = 'STEP7_RESULT.json' if command == 'step7' else 'CUSTODY_RESULT.json'
        assert (Path(destination)/expected).read_bytes() == b'{}\n'
    results.append({'command':command,'scenario':scenario,'status':'PASS','ledger_entered':bool(entered),'mutant_detected':scenario.endswith('_mutant')})
report={'schema':'ROSTER_PARENT_PREFLIGHT_TEST_CX1V001','source':{'path':str(SOURCE),'sha256':EXPECTED},'checks':results,'test_seams':['_cmd_input supplies structurally valid inert input','step7_run/custody_run write a sentinel ledger; no scientific data'], 'scientific_launches':0}
with (WORK/'REPORT.json').open('x') as f:json.dump(report,f,sort_keys=True,indent=2);f.write('\n')
print(json.dumps(report,sort_keys=True))
