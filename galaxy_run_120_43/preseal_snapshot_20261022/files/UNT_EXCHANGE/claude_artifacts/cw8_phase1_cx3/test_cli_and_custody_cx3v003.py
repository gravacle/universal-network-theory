"""Additional metadata-only CLI and adverse custody controls. No process launch."""
import contextlib
import io
from pathlib import Path

HERE = Path(__file__).parent
fixture_path = HERE/'test_selector_cx3v003.py'
source = fixture_path.read_text().split('\ncase("missing_license_automatic_serial"')[0]
exec(compile(source, str(fixture_path)+':definitions', 'exec'), globals())
builder = HERE/'roster_builder_c2v007_cx3cw8v003.py'
ALLOWED.add(str(builder))
braw = builder.read_bytes()
assert hashlib.sha256(braw).hexdigest() == 'f710334b6f5ec2663fbebd826c7b326ebf7ff9eb600e751584de4f518a4e0b11'
B = types.ModuleType('cw8_cli_consumer')
B.__file__ = str(builder)
exec(compile(braw, str(builder), 'exec'), B.__dict__)
# Explicit synthetic clock/process-list seam; the parser, Context and selector
# execute unchanged, and the outer fixture audit prohibits subprocesses.
M.SyntheticSystem.utc = lambda self: NOW
M.SyntheticSystem.processes = lambda self: []


def cli_case(missing=False, extra=(), expected_code=None, omit_forecast=False):
    f = make_context(missing_license=missing)
    fp = None if omit_forecast else forecast(f)
    args = ['select-workers', '--config', f.config['path'], '--config-sha256', f.config['sha256'],
            '--synthetic-pins', f.synthetic['path'], '--synthetic-pins-sha256', f.synthetic['sha256']]
    if fp is not None:
        args += ['--forecast', fp['path'], '--forecast-sha256', fp['sha256']]
    args += list(extra)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = M.cli(args)
    result = json.loads(buf.getvalue())
    if expected_code is None:
        assert rc == 0 and result['status'] == 'SELECTED', result
        assert result['column_workers'] == (1 if missing or omit_forecast else 8), result
        choice = M.read_pin(result['choice'])
        assert choice['prediction']['reason'] == result['reason']
    else:
        assert rc == 2 and result['code'] == expected_code, result
    return True


case('metadata_cli_selects_authorized_full_cw8', cli_case)
case('metadata_cli_missing_license_durable_serial_fallback', lambda: cli_case(missing=True))
case('metadata_cli_no_forecast_durable_serial_fallback', lambda: cli_case(omit_forecast=True))
for name, extra, expected in (
    ('name', ('--name', 'P1_M0001'), 'CW8_SELECT_ARGUMENTS'),
    ('attempt', ('--attempt', '1'), 'CW8_SELECT_ARGUMENTS'),
    ('dry', ('--dry',), 'DRY_COMMAND'),
    ('resume', ('--resume',), 'RESUME_COMMAND'),
    ('verify', ('--verify',), 'VERIFY_COMMAND')):
    case('metadata_cli_refuses_'+name, lambda ex=extra, code=expected: cli_case(extra=ex, expected_code=code))


def custody_case(kind):
    f = make_context()
    choice, _ = choose(f)
    call = f.ctx.call('P1_M0001')
    role = M.cw8_role(call)
    entry = {'name': call['name'], 'schema': 'UNT_P112_LAUNCH_REGISTRY_ENTRY_CX2V001',
             'worker_role': role, 'spec': call['spec']}
    doc = {'worker_role': copy.deepcopy(role)}
    record = {'worker_role': copy.deepcopy(role), 'watch_pid': None}
    if kind == 'old_serial_entry':
        entry.pop('worker_role')
    elif kind == 'old_serial_raw_spec':
        entry['spec'] = call['serial_spec']
    elif kind == 'twin_role':
        entry['worker_role'] = dict(role, kind='IDENTITY_TWIN')
    elif kind == 'twin_watcher':
        record['watch_pid'] = 123
    elif kind == 'closed_receipt_role':
        doc['worker_role'] = dict(role, column_workers=1)
    elif kind == 'record_choice':
        record['worker_role'] = dict(role, choice=None)
    elif kind == 'unauthorized':
        entry['worker_role'] = dict(role, choice=None)
        doc['worker_role'] = copy.deepcopy(entry['worker_role'])
        record['worker_role'] = copy.deepcopy(entry['worker_role'])
    expected = {'old_serial_entry': 'CW8_ROLE_CUSTODY', 'old_serial_raw_spec': 'CW8_SPEC_LEAF',
                'twin_role': 'CW8_ROLE_CUSTODY', 'twin_watcher': 'CW8_FULL_CALL_TWIN_WATCHER',
                'closed_receipt_role': 'CW8_ROLE_CUSTODY', 'record_choice': 'CW8_ROLE_CUSTODY',
                'unauthorized': 'CW8_FULL_CALL_UNAUTHORIZED'}[kind]
    try:
        B.command_snapshot(B._cw8_receipt_workers)(doc, entry, None, record, 'synthetic adverse custody')
    except B.Refused as exc:
        assert exc.code == expected, (exc.code, expected)
    else:
        raise AssertionError('adverse custody accepted: '+kind)
    return True


for kind in ('old_serial_entry', 'old_serial_raw_spec', 'twin_role', 'twin_watcher',
             'closed_receipt_role', 'record_choice', 'unauthorized'):
    case('consumer_refuses_'+kind, lambda k=kind: custody_case(k))

report = {'date_u': DATE, 'status': 'TESTED', 'scope': __doc__, 'cases': RESULTS,
          'passed': sum(r['status']=='PASS' for r in RESULTS),
          'failed': sum(r['status']!='PASS' for r in RESULTS),
          'launcher': {'path': str(TOOL), 'sha256': TOOL_SHA},
          'builder': {'path': str(builder), 'sha256': hashlib.sha256(braw).hexdigest()},
          'test': {'path': str(Path(__file__)), 'sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},
          'seams': ['inert source pins and SyntheticSystem', 'synthetic clock and empty process list'],
          'scientific_execution': 'NONE'}
pin = put(WORK/'EVIDENCE.json', report)
print(json.dumps({'passed': report['passed'], 'failed': report['failed'], 'evidence': pin,
                  'failures': [r for r in RESULTS if r['status']!='PASS']}))
sys.exit(bool(report['failed']))
