"""P3b: missing launch root through the real Context and the entry CLI."""
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
REAL_SELECT = M.select_workers
M.SyntheticSystem.utc = lambda self: NOW
M.SyntheticSystem.processes = lambda self: []
N.load_tool = lambda: M
def run(fn, argv):
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            rc = fn(argv)
    finally:
        M.select_workers = REAL_SELECT
    return rc, buf.getvalue().strip()
OUT = {}
for label, sub in (('missing_root', 'never_created_root'),):
    f = make_context(missing_license=True)
    cfg = dict(M.read_pin(f.config)); cfg['p112_launch_root'] = str(f.root / sub)
    cp = put(f.root / 'CONFIG_MISSING_ROOT.json', cfg)
    args = ['--config', cp['path'], '--config-sha256', cp['sha256'], '--synthetic-pins', f.synthetic['path'], '--synthetic-pins-sha256', f.synthetic['sha256']]
    rc0, o0 = run(M.cli, ['select-workers'] + args)
    d_out = f.root / 'diag_outside.json'
    rc1, o1 = run(N.cli, ['select-workers', '--refusal-record', str(d_out)] + args)
    d_at = f.root / sub
    rc2, o2 = run(N.cli, ['select-workers', '--refusal-record', str(d_at)] + args)
    OUT[label] = dict(unchanged=(rc0, o0[:160]), entry_outside=(rc1, o1[:160]), record_outside=(json.loads(d_out.read_text())['refusal_code'] if d_out.exists() else None),
                      entry_dest_is_missing_root=(rc2, o2[:160]), root_created=(f.root / sub).exists())
print(json.dumps(OUT, indent=1))
