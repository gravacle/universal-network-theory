"""Static synthetic policy tests. No fixture, monitor, or driver is launched."""
import copy
import hashlib
import json
import os
from pathlib import Path
import sys
import types

HERE = Path(__file__).resolve().parent
BASE = HERE.parent / 'phase1_ngc_launch_kit_cx2v003/phase1_ngc_launch_cx2v003.py'
CORE = HERE / 'policy_core_draft002.py'
base = BASE.read_bytes()
core = CORE.read_bytes()
assert hashlib.sha256(base).hexdigest() == 'af0210715f658c43f73f37a5e6e733f7a48dc374caa1b8af5a0defe3987854d7'
assert hashlib.sha256(core).hexdigest() == 'b59ab990007482153b3b3be2f35bea68675eefe0fb497d133dbbc057c862e0ce'
M = types.ModuleType('p112_pure_policy')
M.__file__ = str(BASE)
exec(compile(base, str(BASE), 'exec'), M.__dict__)
exec(compile(core, str(CORE), 'exec'), M.__dict__)
WORK = Path(sys.argv[1]).resolve()
WORK.mkdir()


def audit(event, args):
    if event in ('os.rename', 'os.remove', 'os.rmdir', 'subprocess.Popen'):
        raise AssertionError('IMMUTABILITY_PROCESS_FENCE: ' + event)
    if event == 'open' and isinstance(args[0], (str, bytes, os.PathLike)):
        path = os.path.realpath(os.fsdecode(args[0]))
        if not path.startswith(str(WORK) + os.sep):
            raise AssertionError('READ_FENCE: ' + path)
        flags = args[2]
        if isinstance(flags, int) and flags & (os.O_WRONLY | os.O_RDWR) and os.path.lexists(path):
            raise AssertionError('IMMUTABILITY_FENCE')


sys.addaudithook(audit)
P1 = '2026-11-06T05:59:00Z'
P2 = '2026-12-01T05:59:00Z'
NOW = '2026-11-01T00:00:00Z'
NAME = 'P1_M0001'
CASES = []


def case(name, fn, expected=None):
    CASES.append((name, fn, expected))


def receipt(k=1, cls='FAILED', raw='CHILD_FAILED|FAILED', **changes):
    r = {
        'attempt': k, 'status_class': cls, 'raw_status': raw,
        'spec_sha256': 'a' * 64, 'solo_mode': True, 'other_ngc_processes_max': 0,
        'rss_cap_bytes': M.RAM, 'host_ram_bytes': M.RAM, 'wall_cap_s': 17,
        'output_cap_bytes': 1000, 'time_utc': '2026-10-31T00:00:%02dZ' % (k % 60),
        'pins': {'stop_record': None},
    }
    r.update(changes)
    r['receipt_pin'] = {'path': '/synthetic/receipt_%d.json' % k, 'sha256': M.sha(M.canonical(r))}
    return r


def causes(rows, **changes):
    out = {}
    for r in rows:
        proof = {
            'driver_sha256': 'b' * 64, 'spec_sha256': r['spec_sha256'], 'stage': 'route_a',
            'status': r['raw_status'].split('|', 1)[1], 'failure_code': 'ITERATION_BUDGET_EXHAUSTED',
            'clean': True, 'iteration_budget': 10, 'registered_iteration_budget': 10,
            'signal': None, 'exception_type': None,
            'source_pins': [{'path': '/synthetic/proof.json', 'sha256': 'c' * 64}],
        }
        proof.update(changes)
        p = r['receipt_pin']
        out[(p['path'], p['sha256'])] = proof
    return out


def next_for(rows, *, name=NAME, **kw):
    records = [{'attempt': r['attempt'], 'origin': 'P112', 'outcome': 'LAUNCH'} for r in rows]
    options = dict(phase_ceiling_utc=P1, monitor_ceiling_utc=P2, now_utc=NOW)
    options.update(kw)
    return M.next_attempt(name, records, rows, set(), **options)


pair = [receipt(), receipt(2)]
case('model_pair_needs_external_authenticated_map', lambda: M.terminal_prefix(pair, NAME) is None)
case('clean_budget_pair_counts', lambda:
     M.terminal_prefix(pair, NAME, causes(pair))['disposition'] == 'RULE_C_INVALID')
case('explicit_route_a_pair_counts', lambda:
     M.terminal_prefix(pair, NAME, causes(pair, failure_code='ROUTE_A_NO_FIXED_POINT')) is not None)
for key, value in [('clean', False), ('signal', -9), ('exception_type', 'OSError'),
                   ('failure_code', 'FAILED_SOURCE_PREPARATION'), ('failure_code', 'ValueError'),
                   ('iteration_budget', 11), ('registered_iteration_budget', None),
                   ('source_pins', []), ('driver_sha256', 'wrong'), ('stage', ''),
                   ('spec_sha256', 'd' * 64)]:
    case('uncounted_' + key + '_' + str(value), lambda k=key, v=value:
         M.terminal_prefix(pair, NAME, causes(pair, **{k: v})) is None)
case('one_failure_never_counts', lambda:
     M.terminal_prefix(pair[:1], NAME, causes(pair[:1])) is None)
case('pair_stage_must_match', lambda: M.terminal_prefix(pair, NAME, {
    **causes(pair[:1]), **causes(pair[1:], stage='different')}) is None)
case('pair_code_must_match', lambda: M.terminal_prefix(pair, NAME, {
    **causes(pair[:1]), **causes(pair[1:], failure_code='ROUTE_A_NO_FIXED_POINT')}) is None)
case('pair_driver_must_match', lambda: M.terminal_prefix(pair, NAME, {
    **causes(pair[:1]), **causes(pair[1:], driver_sha256='d' * 64)}) is None)
for key, value in [('solo_mode', False), ('other_ngc_processes_max', 1),
                   ('other_ngc_processes_max', None), ('other_ngc_processes_max', True),
                   ('rss_cap_bytes', M.RAM - 1)]:
    rows = [pair[0], receipt(2, **{key: value})]
    case('pair_evidence_' + key + '_' + str(value), lambda r=rows:
         M.terminal_prefix(r, NAME, causes(r)) is None)
for cls, raw in [('CAP', 'STOPPED_WALL_CAP|NONE'), ('CAP', 'STOPPED_RSS_CAP|NONE'),
                 ('OUTPUT_CAP', 'STOPPED_OUTPUT_CAP|NONE'), ('INFRA', 'CHILD_FAILED|NONE|SIGNAL')]:
    rows = [receipt(k, cls, raw) for k in (1, 2, 3, 4)]
    case('never_terminal_' + raw, lambda r=rows: M.terminal_prefix(r, NAME) is None)
    case('retry_solo_' + raw, lambda r=rows: next_for(r)['solo_mode'] is True)
case('no_doubled_wall_condition', lambda:
     M.terminal_prefix(pair, NAME, causes(pair))['counted_attempts'] == [0, 1])
case('unauthenticated_repeated_solo_held', lambda: next_for(pair), 'HELD_FOR_CAUSE')
case('unauthenticated_single_retried', lambda: next_for(pair[:1])['attempt'] == 2)
case('positive_model_pair_blocks_retry', lambda:
     next_for(pair, authenticated_causes=causes(pair)), 'ATTEMPT_AFTER_TERMINAL')
case('known_nonmodel_cause_allows_retry', lambda:
     next_for(pair, authenticated_causes={
         (r['receipt_pin']['path'], r['receipt_pin']['sha256']): None for r in pair
     })['attempt'] == 3)
for status in ('REFUSED', 'BLOCKED'):
    rows = [receipt(k, 'INFRA', 'CHILD_FAILED|' + status) for k in (1, 2)]
    case('held_for_fix_' + status, lambda r=rows: next_for(r), 'HELD_FOR_FIX')
    case('explicit_fix_release_' + status, lambda r=rows:
         next_for(r, root_hold_release=True)['solo_mode'])
outcaps = [receipt(1, 'OUTPUT_CAP', 'STOPPED_OUTPUT_CAP|NONE', output_cap_bytes=1000),
           receipt(2, 'OUTPUT_CAP', 'STOPPED_OUTPUT_CAP|NONE', output_cap_bytes=2000),
           receipt(3, 'OUTPUT_CAP', 'STOPPED_OUTPUT_CAP|NONE', output_cap_bytes=4000)]
case('output_doubles_previous_not_first', lambda: next_for(outcaps)['caps']['output_cap_bytes'] == 8000)
case('no_attempt_number_limit', lambda:
     next_for([receipt(1000000, 'CAP', 'STOPPED_RSS_CAP|NONE')])['attempt'] == 1000001)
case('wall_uses_phase2_remaining', lambda:
     next_for(pair[:1])['caps']['wall_cap_s'] == int(M.timestamp(P2) - M.timestamp(NOW)))
case('phase1_no_new_phase1_admission_after_boundary', lambda:
     next_for(pair[:1], now_utc=P1), 'UNEVALUATED_SCHEDULE_CEILING')
case('missing_monitor_deadline_refuses', lambda:
     next_for(pair[:1], monitor_ceiling_utc=None), 'MONITOR_PHASE2_CEILING_REQUIRED')
twin = [receipt(1, 'CAP', 'STOPPED_RSS_CAP|NONE')]
case('twin_retry_ram_times_11', lambda:
     next_for(twin, name=M.TWIN)['caps']['rss_cap_bytes'] == 11 * M.RAM)
case('twin_planned_stop_requires_evidence', lambda:
     M.terminal_prefix([receipt(1, 'PLANNED_STOP', 'TWIN_PLANNED_STOP')], M.TWIN),
     'TWIN_STOP_NOT_BOUND')
stop = receipt(1, 'PLANNED_STOP', 'TWIN_PLANNED_STOP',
               pins={'stop_record': {'path': '/synthetic/watch.json', 'sha256': 'f' * 64}})
case('twin_planned_stop_with_bound_evidence', lambda:
     M.terminal_prefix([stop], M.TWIN)['disposition'] == 'PLANNED_STOP')
case('phase1_ceiling_does_not_request_stop', lambda:
     M.phase_disposition([], NAME, P1, P1) == {
         'status': 'UNEVALUATED_SCHEDULE_CEILING', 'terminal': None,
         'continues_for_next_phase': True, 'stop_requested': False})
late = [receipt(1, 'FINISHED', 'FINISHED|COMPLETED', time_utc='2026-11-07T00:00:00Z')]
case('after_phase1_completion_not_retroactive', lambda:
     M.phase_disposition(late, NAME, P1, '2026-11-08T00:00:00Z')['status']
     == 'UNEVALUATED_SCHEDULE_CEILING')
case('after_phase1_completion_available_phase2', lambda:
     M.phase_disposition(late, NAME, P2, '2026-11-08T00:00:00Z')['status'] == 'TERMINAL')
case('held_cause_status_before_boundary', lambda:
     M.phase_disposition(pair, NAME, P1, NOW)['status'] == 'HELD_FOR_CAUSE')
case('held_cause_at_boundary_incomplete', lambda:
     M.phase_disposition(pair, NAME, P1, P1)['status'] == 'UNEVALUATED_SCHEDULE_CEILING')

results = []
for name, fn, expected in CASES:
    observed, passed = 'RETURNED', False
    try:
        result = fn()
        passed = expected is None and result is not False
    except M.Refusal as exc:
        observed, passed = exc.code, exc.code == expected
    row = {'id': name, 'expected': expected, 'observed': observed, 'verdict': 'PASS' if passed else 'FAIL'}
    results.append(row)
    if not passed:
        print(json.dumps(row))
record = {
    'scope': 'TESTED pure synthetic policy; authentication adapter and public tool UNTESTED',
    'parent_sha256': hashlib.sha256(base).hexdigest(), 'component_sha256': hashlib.sha256(core).hexdigest(),
    'n_cases': len(results), 'n_pass': sum(r['verdict'] == 'PASS' for r in results), 'cases': results,
}
with (WORK / 'TEST_RECORD.json').open('xb') as f:
    f.write((json.dumps(record, indent=2, sort_keys=True) + '\n').encode())
print('%d/%d PASS' % (record['n_pass'], record['n_cases']))
raise SystemExit(0 if record['n_pass'] == record['n_cases'] else 1)
