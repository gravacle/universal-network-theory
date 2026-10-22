"""Claude3 independent probes of the D034 entry through the REAL Context and the unchanged CLI (backlog #5 review).
usage: $PY -I -B probe_n3_cli_c3.py WORK   (WORK must not exist)"""
from pathlib import Path
import hashlib, types, sys, io, contextlib, json, os
ENTRY = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cw8_hardening_cx1/select_workers_diagnostic_cx1v001.py')
assert hashlib.sha256(ENTRY.read_bytes()).hexdigest() == '5a93c37122e416e0d2230ec25be256ec10d913536479f3f1d4de7e6c44ed6eaa'
N = types.ModuleType('diagnostic_entry'); N.__file__ = str(ENTRY)
exec(compile(ENTRY.read_bytes(), str(ENTRY), 'exec'), N.__dict__)
FIXTURE = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cw8_phase1_cx3/test_selector_cx3v003.py')
assert hashlib.sha256(FIXTURE.read_bytes()).hexdigest() == '39fa111c3e5e29f8fcd33f3d6e749da565fb51d2f542efb12e3f9994695af14b'
source = FIXTURE.read_text().split('\ncase("missing_license_automatic_serial"')[0]
__file__ = str(FIXTURE)
exec(compile(source, str(FIXTURE), 'exec'), globals())
ALLOWED.add(str(ENTRY))
OUT = {}
REAL_SELECT = M.select_workers
def run(fn, argv):
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            try:
                rc = fn(argv)
            except SystemExit as e:
                rc = ('SystemExit', e.code)
    finally:
        M.select_workers = REAL_SELECT          # N.cli patches the shared module; production runs it once per process
    return rc, buf.getvalue()
def base_args(f):
    return ['--config', f.config['path'], '--config-sha256', f.config['sha256'], '--synthetic-pins', f.synthetic['path'], '--synthetic-pins-sha256', f.synthetic['sha256']]
M.SyntheticSystem.utc = lambda self: NOW
M.SyntheticSystem.processes = lambda self: []
N.load_tool = lambda: M
def ctx_of(f):
    system = M.SyntheticSystem(M.read_pin(f.synthetic)['system']); system.processes = lambda: []; system.utc = lambda: NOW
    return M.Context(f.config, system=system, synthetic_pins=f.overrides)
def choices(f):
    d = Path(ctx_of(f).cfg['p112_launch_root']) / 'worker_choices'
    return sorted(p.name for p in d.glob('*')) if d.exists() else None
# P1: FILE lock refusal through the unchanged CLI, then through the entry with --refusal-record, on the same fixture
f = make_context(missing_license=True); root = Path(ctx_of(f).cfg['p112_launch_root'])
(root / '.worker_choices.lock').mkdir()
rc0, out0 = run(M.cli, ['select-workers'] + base_args(f))
dest = f.root / 'diag_P1.json'
rc1, out1 = run(N.cli, ['select-workers', '--refusal-record', str(dest)] + base_args(f))
rec = json.loads(dest.read_text()) if dest.exists() else None
cp = ctx_of(f).config_pin
OUT['P1_file_lock_cli'] = dict(unchanged_rc=rc0, entry_rc=rc1, stdout_identical=(out0 == out1), unchanged_stdout=out0.strip()[:200],
    record_written=rec is not None, record_keys_ok=(rec is not None and set(rec) == {'schema','utc','refusal_code','refusal_text','launch_root','lock_path','config_pin','tool_pin','worker_choices_written'}),
    record_code=(rec or {}).get('refusal_code'), record_config_pin_equals_real_ctx=(rec or {}).get('config_pin') == cp, real_ctx_config_pin=cp,
    record_lock_path_ok=(rec or {}).get('lock_path') == str(root / '.worker_choices.lock'), record_mode=oct(os.stat(dest).st_mode & 0o777) if dest.exists() else None,
    worker_choices_after=choices(f))
# P2: IDENTITY lock refusal through the entry CLI (inode substitution simulated as in the author's test)
f2 = make_context(missing_license=True); root2 = Path(ctx_of(f2).cfg['p112_launch_root'])
original_os = M.os; realstat = original_os.stat
def fake_stat(path, *a, **k):
    st = realstat(path, *a, **k)
    if str(path).endswith('/.worker_choices.lock') and k.get('follow_symlinks') is False:
        return types.SimpleNamespace(st_dev=st.st_dev, st_ino=st.st_ino + 1)
    return st
M.os = types.SimpleNamespace(**{k: getattr(original_os, k) for k in dir(original_os)}); M.os.stat = fake_stat
dest2 = f2.root / 'diag_P2.json'
try:
    rc2, out2 = run(N.cli, ['select-workers', '--refusal-record', str(dest2)] + base_args(f2))
finally:
    M.os = original_os
rec2 = json.loads(dest2.read_text()) if dest2.exists() else None
OUT['P2_identity_lock_cli'] = dict(entry_rc=rc2, stdout=out2.strip()[:160], record_code=(rec2 or {}).get('refusal_code'), worker_choices_after=choices(f2))
# P3: ROOT lock refusal: launch root is a symlink to a real folder (realpath differs)
f3 = make_context(missing_license=True)
cfg3 = dict(M.read_pin(f3.config)); real_root = Path(cfg3['p112_launch_root'])
link = f3.root / 'launch_root_link'; os.symlink(real_root, link); cfg3['p112_launch_root'] = str(link)
c3pin = put(f3.root / 'CONFIG_ROOTLINK.json', cfg3)
f3b = types.SimpleNamespace(config=c3pin, synthetic=f3.synthetic, overrides=f3.overrides, root=f3.root)
dest3 = f3.root / 'diag_P3.json'
rc3a, out3a = run(M.cli, ['select-workers'] + base_args(f3b))
rc3, out3 = run(N.cli, ['select-workers', '--refusal-record', str(dest3)] + base_args(f3b))
OUT['P3_root_symlink_cli'] = dict(unchanged_rc=rc3a, unchanged_stdout=out3a.strip()[:200], entry_rc=rc3, stdout_identical=(out3a == out3), record_written=dest3.exists(),
    record_code=(json.loads(dest3.read_text()).get('refusal_code') if dest3.exists() else None))
# P4: destination checks before selection on an otherwise-successful fixture: existing file; under the real worker_choices; inside the root but elsewhere
f4 = make_context(missing_license=True); root4 = Path(ctx_of(f4).cfg['p112_launch_root'])
ex = f4.root / 'exists.json'; put(ex, {'sentinel': True})
rc4a, out4a = run(N.cli, ['select-workers', '--refusal-record', str(ex)] + base_args(f4))
wc = root4 / 'worker_choices'; wc.mkdir()
rc4b, out4b = run(N.cli, ['select-workers', '--refusal-record', str(wc / 'd.json')] + base_args(f4))
OUT['P4_destination_refusals_before_selection'] = dict(existing_rc=rc4a, existing_code=json.loads(out4a)['code'] if out4a.strip().startswith('{') else out4a[:120],
    choice_dir_rc=rc4b, choice_dir_code=json.loads(out4b)['code'] if out4b.strip().startswith('{') else out4b[:120], worker_choices_after=choices(f4))
# P5: success without --refusal-record equals the unchanged CLI in shape (two fresh fixtures)
fa = make_context(missing_license=True); fb = make_context(missing_license=True)
ra, oa = run(M.cli, ['select-workers'] + base_args(fa)); rb_, ob = run(N.cli, ['select-workers'] + base_args(fb))
ja, jb = json.loads(oa), json.loads(ob)
OUT['P5_success_shape_equal'] = dict(unchanged_rc=ra, entry_rc=rb_, keys_equal=sorted(ja) == sorted(jb), status=(ja['status'], jb['status']), workers=(ja['column_workers'], jb['column_workers']), reason=(ja['reason'], jb['reason']))
# P6: argument order: command not first
fc = make_context(missing_license=True)
rc6, out6 = run(N.cli, base_args(fc) + ['select-workers', '--refusal-record', str(fc.root / 'd6.json')])
OUT['P6_command_not_first'] = dict(rc=rc6, stdout=out6.strip()[:160])
# P7: tool pin: a one-byte-altered copy refuses at load
alt = WORK / 'altered_tool.py'
raw = Path(M.__file__).read_bytes(); put(alt, raw.replace(b'"""', b'""" ', 1), raw=True)
N2 = types.ModuleType('entry2'); N2.__file__ = str(ENTRY); exec(compile(ENTRY.read_bytes(), str(ENTRY), 'exec'), N2.__dict__)
N2.TOOL = alt
try:
    N2.load_tool(); OUT['P7_tool_pin'] = 'LOADED (bad)'
except ValueError as e:
    OUT['P7_tool_pin'] = 'REFUSED ' + str(e)
OUT['P7b_real_tool_loads'] = hashlib.sha256(N2.TOOL.read_bytes()).hexdigest()[:8] if False else None
print(json.dumps(OUT, indent=1, sort_keys=True, default=str))
