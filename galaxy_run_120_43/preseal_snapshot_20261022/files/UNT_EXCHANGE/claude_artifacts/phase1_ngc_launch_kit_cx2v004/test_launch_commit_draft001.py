"""Saved synthetic launch-plan custody; no monitor, sampler, or driver starts."""
import copy
import hashlib
import json
import os
from pathlib import Path
import sys
import types

HERE = Path(__file__).resolve().parent
FILES = [
    (HERE.parent / 'phase1_ngc_launch_kit_cx2v003/phase1_ngc_launch_cx2v003.py',
     'af0210715f658c43f73f37a5e6e733f7a48dc374caa1b8af5a0defe3987854d7'),
    (HERE / 'policy_core_draft002.py',
     'b59ab990007482153b3b3be2f35bea68675eefe0fb497d133dbbc057c862e0ce'),
    (HERE / 'launch_commit_draft002.py',
     '8c1f552be71155122c73779b0c7fdba11c35009c982871aed26424d56ed5e26e'),
]
M = types.ModuleType('p112_commit_tests')
M.__file__ = str(FILES[0][0])
for path, digest in FILES:
    raw = path.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == digest
    exec(compile(raw, str(path), 'exec'), M.__dict__)
WORK = Path(sys.argv[1]).resolve()
WORK.mkdir()
READS = []


def audit(event, args):
    if event in ('os.rename', 'os.remove', 'os.rmdir'):
        raise AssertionError('IMMUTABILITY_FENCE: ' + event)
    if event == 'subprocess.Popen' and args[1] != ['/bin/date', '-u']:
        raise AssertionError('PROCESS_FENCE')
    if event != 'open' or not isinstance(args[0], (str, bytes, os.PathLike)):
        return
    path = os.path.realpath(os.fsdecode(args[0]))
    if not path.startswith(str(WORK) + os.sep):
        raise AssertionError('READ_FENCE: ' + path)
    flags = args[2]
    writing = isinstance(flags, int) and bool(flags & (os.O_WRONLY | os.O_RDWR))
    if writing and os.path.lexists(path):
        raise AssertionError('IMMUTABILITY_FENCE: existing-file write')
    if not writing:
        READS.append(path)


sys.addaudithook(audit)
CASES = []
N = 0


class Context:
    cfg = {'phase1_ceiling_utc': '2026-11-06T05:59:00Z',
           'phase2_ceiling_utc': '2026-12-01T05:59:00Z'}
    config_pin = {'path': '/synthetic/config.json', 'sha256': 'c' * 64}
    pins = {'driver': {'path': '/synthetic/driver.py', 'sha256': 'd' * 64},
            'monitor': {'path': '/synthetic/monitor.py', 'sha256': 'e' * 64}}

    def gate(self):
        return {'synthetic_gate': True}

    def write(self, path, obj):
        return M.write_x(path, dict(obj, observations=M.observation_report()))


def fixture():
    global N
    N += 1
    work = WORK / ('case_%03d' % N)
    work.mkdir()
    ctx = Context()
    spec = {'path': '/synthetic/spec.json', 'sha256': 'f' * 64}
    now = '2026-11-01T00:00:00Z'
    caps = {'wall_cap_s': M.remaining_wall(ctx.cfg['phase2_ceiling_utc'], now),
            'rss_cap_bytes': M.RAM, 'output_cap_bytes': 1000}
    plan = {
        'schema': 'UNT_P112_LAUNCH_PLAN_CX2V001', 'name': 'P1_M0001', 'attempt': 1,
        'config': ctx.config_pin, 'work': str(work), 'spec': spec, 'pins': ctx.pins,
        'outdir': '/synthetic/call', 'caps': caps, 'caps_basis': {'rule': 'bootstrap'},
        'invocation_utc': now, 'date_u': M.date_u(), 'solo_mode': True,
        'monitor_argv': M.monitor_command(ctx.pins, spec, '/synthetic/call', caps),
    }
    pin = ctx.write(str(work / 'plan.json'), plan)
    return ctx, work, plan, pin


def case(name, fn, expected=None):
    CASES.append((name, fn, expected))


def complete():
    ctx, work, plan, pin = fixture()
    final, final_pin = M.write_launch_commit(ctx, plan, pin, work, '2026-11-01T00:02:00Z')
    assert final['caps']['wall_cap_s'] == plan['caps']['wall_cap_s'] - 120
    assert final['caps']['rss_cap_bytes'] == plan['caps']['rss_cap_bytes']
    assert final['spec'] == plan['spec']
    with (work / 'LAUNCH_COMMIT.json').open('rb') as f:
        commit = M.strict_json(f.read())
    return ctx, work, plan, pin, final, final_pin, commit


case('fresh_wall_after_preparation', lambda: complete())
case('resumable_committed_plan', lambda: (
    lambda x: M.read_launch_commit(x[0], x[2], x[3], x[1]) == (x[4], x[5]))(complete()))
case('sampler_observes_same_commit', lambda: (
    lambda x: M.observe_launch_commit(x[0], x[2], x[3], x[1]) == (x[4], x[5]))(complete()))
case('commit_cannot_overwrite', lambda: (
    lambda x: M.write_launch_commit(x[0], x[2], x[3], x[1], '2026-11-01T00:03:00Z'))(complete()),
    'LAUNCH_COMMIT_EXISTS')
case('bootstrap_pin_mismatch', lambda: (
    lambda c,w,p,pin: M.write_launch_commit(c,p,dict(pin,sha256='0'*64),w,'2026-11-01T00:02:00Z'))(*fixture()),
    'LAUNCH_BOOTSTRAP_BYTES')
case('bootstrap_data_mismatch', lambda: (
    lambda c,w,p,pin: M.write_launch_commit(c,dict(p,attempt=2),pin,w,'2026-11-01T00:02:00Z'))(*fixture()),
    'LAUNCH_BOOTSTRAP_BYTES')
case('clock_backward', lambda: (
    lambda c,w,p,pin: M.write_launch_commit(c,p,pin,w,'2026-10-31T23:59:00Z'))(*fixture()),
    'LAUNCH_CLOCK_MOVED_BACKWARD')
case('phase1_admission_closed', lambda: (
    lambda c,w,p,pin: M.write_launch_commit(c,p,pin,w,c.cfg['phase1_ceiling_utc']))(*fixture()),
    'UNEVALUATED_SCHEDULE_CEILING')


def altered(change):
    c,w,p,pin,final,fpin,commit = complete()
    final = copy.deepcopy(final)
    change(final)
    return M._commit_plan_check(c,p,pin,commit,final,fpin,w)


case('committed_spec_cannot_change', lambda:
     altered(lambda d: d.update(spec={'path':'/synthetic/other.json','sha256':'a'*64})),
     'LAUNCH_COMMIT_FIXED_FIELDS')
case('committed_output_cap_cannot_change', lambda:
     altered(lambda d: d['caps'].update(output_cap_bytes=2000)), 'LAUNCH_COMMIT_MACHINE_CAPS')
case('committed_wall_must_be_remaining', lambda:
     altered(lambda d: d['caps'].update(wall_cap_s=d['caps']['wall_cap_s']+1)), 'LAUNCH_COMMIT_WALL')
case('committed_argv_must_match', lambda:
     altered(lambda d: d['monitor_argv'].append('--unregistered')), 'LAUNCH_COMMIT_ARGV')
case('phase1_is_never_stop', lambda:
     altered(lambda d: d['caps_basis'].update(phase1_requests_stop=True)), 'LAUNCH_COMMIT_CEILINGS')


def outside_pin():
    c,w,p,pin,final,fpin,commit = complete()
    commit['launch_plan']['path'] = '/never_open/NGC3198_forbidden.json'
    return M.read_launch_commit(c,p,pin,w,snapshot=commit)


case('outside_pin_refused_before_read', outside_pin, 'LAUNCH_COMMIT_RESIDENCE')


def partial():
    c,w,p,pin = fixture()
    M.write_x_bytes(w / 'LAUNCH_COMMIT.json', b'{')
    return M.observe_launch_commit(c,p,pin,w) is None


case('partial_commit_poll_not_a_final_snapshot', partial)


def single_read():
    c,w,p,pin = fixture()
    before = len(READS)
    @M.read_scope
    def command():
        final, fpin = M.write_launch_commit(c,p,pin,w,'2026-11-01T00:02:00Z')
        assert M.read_launch_commit(c,p,pin,w) == (final,fpin)
    command()
    paths = READS[before:]
    return bool(paths) and len(paths) == len(set(paths))


case('A226_commit_buffers_single_read', single_read)
results = []
for name, fn, expected in CASES:
    observed, passed = 'RETURNED', False
    try:
        value = fn()
        passed = expected is None and value is not False
    except M.Refusal as exc:
        observed, passed = exc.code, exc.code == expected
    row = {'id':name,'expected':expected,'observed':observed,'verdict':'PASS' if passed else 'FAIL'}
    results.append(row)
    if not passed:
        print(json.dumps(row))
record = {'scope':'synthetic saved plans; public launch/sampler/resume wiring UNTESTED',
          'sources':[{'path':str(p),'sha256':s} for p,s in FILES],
          'n_cases':len(results),'n_pass':sum(r['verdict']=='PASS' for r in results),'cases':results}
M.write_x(WORK / 'TEST_RECORD.json', record)
print('%d/%d PASS' % (record['n_pass'],record['n_cases']))
raise SystemExit(0 if record['n_pass']==record['n_cases'] else 1)
