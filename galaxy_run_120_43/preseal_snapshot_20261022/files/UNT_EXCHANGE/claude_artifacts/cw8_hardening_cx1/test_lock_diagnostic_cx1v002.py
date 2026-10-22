"""D034 inert lock and destination controls, plus prohibited-choice mutant."""
from pathlib import Path
import hashlib, types, sys, io, contextlib
ENTRY = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cw8_hardening_cx1/select_workers_diagnostic_cx1v001.py')
assert hashlib.sha256(ENTRY.read_bytes()).hexdigest() == '5a93c37122e416e0d2230ec25be256ec10d913536479f3f1d4de7e6c44ed6eaa'
N = types.ModuleType('diagnostic_entry')
N.__file__ = str(ENTRY)
exec(compile(ENTRY.read_bytes(), str(ENTRY), 'exec'), N.__dict__)
FIXTURE = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cw8_phase1_cx3/test_selector_cx3v003.py')
assert hashlib.sha256(FIXTURE.read_bytes()).hexdigest() == '39fa111c3e5e29f8fcd33f3d6e749da565fb51d2f542efb12e3f9994695af14b'
source = FIXTURE.read_text().split('\ncase("missing_license_automatic_serial"')[0]
__file__ = str(FIXTURE)
exec(compile(source, str(FIXTURE), 'exec'), globals())
ALLOWED.add(str(ENTRY))
ENTRY_RAW = ENTRY.read_text()
REPORT = []
NCOUNT = 0

def fresh(kind):
    global NCOUNT
    NCOUNT += 1
    parent = WORK / ('lock_case_%03d' % NCOUNT); parent.mkdir()
    root = parent / 'launch'
    if kind != 'ROOT': root.mkdir()
    if kind == 'FILE': (root / '.worker_choices.lock').mkdir()
    return types.SimpleNamespace(cfg={'p112_launch_root': str(root)}, config_pin={'path': str(parent / 'inert-config.json'), 'sha256': '0'*64}, system=types.SimpleNamespace(utc=lambda: NOW)), parent

def body(ctx, forecast):
    raise AssertionError('Lock-refused body must not execute')

selector = M.cw8_choice_lock(body)

def invoke(kind, destination=None, mutant=False):
    ctx, parent = fresh(kind)
    dest = parent / 'diagnostic.json'
    if destination == 'existing': put(dest, {'sentinel': True})
    elif destination == 'choice':
        folder = parent / 'worker_choices'; folder.mkdir(); dest = folder / 'diagnostic.json'
    elif destination == 'relative': dest = 'relative.json'
    elif destination == 'unnormalized': dest = str(parent) + '/./diagnostic.json'
    elif destination == 'missing_parent': dest = parent / 'missing' / 'diagnostic.json'
    elif destination == 'missing_root': dest = Path(ctx.cfg['p112_launch_root']) / 'diagnostic.json'
    original_os = M.os
    if kind == 'IDENTITY':
        realstat = original_os.stat
        def fake_stat(path, *args, **kwargs):
            st = realstat(path, *args, **kwargs)
            if str(path).endswith('/.worker_choices.lock') and kwargs.get('follow_symlinks') is False:
                return types.SimpleNamespace(st_dev=st.st_dev, st_ino=st.st_ino+1)
            return st
        M.os = types.SimpleNamespace(**{key:getattr(original_os,key) for key in dir(original_os)})
        M.os.stat = fake_stat
    selected = selector
    original_entry = N.select_with_refusal
    if mutant:
        segment = ast.get_source_segment(ENTRY_RAW, next(n for n in ast.parse(ENTRY_RAW).body if isinstance(n, ast.FunctionDef) and n.name == 'select_with_refusal'))
        needle = '        raise  # Preserve the original lock refusal; diagnostic is not selection.'
        assert segment.count(needle) == 1
        injected = "        choice_dir = Path(ctx.cfg['p112_launch_root']) / 'worker_choices'\n        choice_dir.mkdir()\n        with (choice_dir / 'CHOICE_MUTANT.json').open('x') as out: out.write('{}')\n" + needle
        exec(compile(segment.replace(needle, injected), '<entry unauthorized choice mutant>', 'exec'), N.__dict__)
    caught = None
    try:
        N.select_with_refusal(M, selected, ctx, refusal_record=str(dest))
    except M.Refusal as exc: caught = exc
    finally:
        M.os = original_os
        N.select_with_refusal = original_entry
    assert caught is not None
    choices = list((Path(ctx.cfg['p112_launch_root']) / 'worker_choices').glob('CHOICE_*.json'))
    if destination:
        expected = {'existing':'CW8_REFUSAL_RECORD_EXISTS', 'choice':'CW8_REFUSAL_RECORD_CHOICE_DIRECTORY', 'relative':'CW8_REFUSAL_RECORD_PATH', 'unnormalized':'CW8_REFUSAL_RECORD_PATH', 'missing_parent':'CW8_REFUSAL_RECORD_PARENT', 'missing_root':'CW8_REFUSAL_RECORD_PARENT'}[destination]
        assert caught.code == expected, caught.code
        if destination == 'existing': assert json.loads(Path(dest).read_text()) == {'sentinel':True}
        else: assert not Path(dest).exists()
    else:
        assert caught.code == 'CW8_CHOICE_LOCK_' + kind
        record = json.loads(dest.read_text())
        assert set(record) == {'schema','utc','refusal_code','refusal_text','launch_root','lock_path','config_pin','tool_pin','worker_choices_written'}
        assert record['schema'] == 'CW8_LOCK_REFUSAL_RECORD_V001'
        assert record['refusal_code'] == caught.code and record['refusal_text'] == str(caught)
        assert record['worker_choices_written'] is False
        assert record['tool_pin'] == {'path':str(ENTRY), 'sha256': hashlib.sha256(ENTRY.read_bytes()).hexdigest()}
        assert record['config_pin'] == ctx.config_pin
        assert len(list(parent.glob('diagnostic*.json'))) == 1
    if mutant:
        try:
            assert not choices, 'lock refusal must never write a choice'
        except AssertionError:
            pass  # The identical no-choice oracle rejects the mutated entry.
        else:
            raise AssertionError('unauthorized-choice mutant survived')
    else:
        assert not choices
    REPORT.append(dict(case=kind, destination=destination, mutant_detected=mutant, status='PASS', code=caught.code))

for kind in ('ROOT','FILE','IDENTITY'): invoke(kind)
for destination in ('existing','choice','relative','unnormalized','missing_parent','missing_root'): invoke('ROOT', destination)
invoke('FILE', mutant=True)
# Full Context and unchanged production CLI: success does not create a diagnostic.
f = make_context(missing_license=True)
M.SyntheticSystem.utc = lambda self: NOW
M.SyntheticSystem.processes = lambda self: []
N.load_tool = lambda: M
out = io.StringIO()
dest = f.root / 'unused-diagnostic.json'
with contextlib.redirect_stdout(out):
    rc = N.cli(['select-workers', '--refusal-record', str(dest), '--config', f.config['path'], '--config-sha256', f.config['sha256'], '--synthetic-pins', f.synthetic['path'], '--synthetic-pins-sha256', f.synthetic['sha256']])
result = json.loads(out.getvalue())
assert rc == 0 and result['status'] == 'SELECTED' and result['column_workers'] == 1, result
assert not dest.exists()
REPORT.append(dict(case='real_Context_CLI_success_no_diagnostic', status='PASS'))
report = dict(schema='CW8_N3_DIAGNOSTIC_TEST_CX1V002', checks=REPORT, scientific_launches=0)
put(WORK / 'REPORT.json', report)
print(json.dumps(report, sort_keys=True))
