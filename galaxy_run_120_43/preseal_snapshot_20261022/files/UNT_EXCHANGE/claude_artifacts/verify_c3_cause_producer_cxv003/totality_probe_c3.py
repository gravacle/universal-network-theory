"""Claude3 totality probe for the A252 cause producer (0848 item 2; cw8 v003-N1, A282).
For every honest FAILED-class receipt (monitor CHILD_FAILED, a positive non-signal exit, no stop_reason, and
driver_status FAILED, FAILED_AT_STAGE or ROUTE_A_NO_FIXED_POINT), classify() must return a row (never raise),
and the row must pass the roster builder's cause-binding checks (roster_builder_c2v007_cx3cw8v003 L4690-4710):
bound receipt == the receipt sha, bound spec == the spec sha, bound driver == the driver sha, status == the
monitor's driver_status, and a bound result equal to the result sha when present.
usage: python3 -I -B totality_probe_c3.py PRODUCER_PATH WORK_DIR [OUTCOME ...]   (WORK_DIR must not exist)
Synthetic only: no run tree, no real receipt, no launch."""
import hashlib, importlib.util, itertools, json, os, sys
from pathlib import Path
prod, work = Path(sys.argv[1]), Path(sys.argv[2])
outcomes = sys.argv[3:] or ['NONCONVERGENCE', 'ITERATION_BUDGET_EXHAUSTED', 'FAILED_SOURCE_PREPARATION', '<absent>', '<None>', 'UNKNOWN_X']
os.mkdir(work)
s = importlib.util.spec_from_file_location('producer_under_test', prod); m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
n = 0
def put(obj, suffix='.json'):
    global n
    n += 1; p = work / ('%04d%s' % (n, suffix)); raw = obj if isinstance(obj, bytes) else json.dumps(obj).encode()
    with p.open('xb') as f: f.write(raw)
    return str(p), hashlib.sha256(raw).hexdigest()
source = b"try:\n pass\nexcept RouteANoFixedPoint:\n status = 'ROUTE_A_NO_FIXED_POINT'\noutcome = 'ITERATION_BUDGET_EXHAUSTED'\n"
driver = put(source, '.py'); spec = 'a' * 64
sites = m.sites(Path(driver[0]).read_bytes())
vocab = {driver[1]: {'complete': True, 'modules': [{'path': driver[0], 'sha256': driver[1],
         'sites': [dict(x, token=t, model_outcome=True) for t, rows in sites.items() for x in rows]}]}}
STAGES = {'route_ok': [{'name': '01_route_a', 'exit_code': 0}],
          'route_ok_plus_failed_stage': [{'name': '01_route_a', 'exit_code': 0}, {'name': '02_post', 'exit_code': 1}],
          'no_stage_records': [],
          'route_signal_killed': [{'name': '01_route_a', 'exit_code': 137}]}
rows, problems = [], []
for lane, status, outcome, stage_key, exit_code, with_finish in itertools.product(
        ('DDO', 'NGC_no_attestation', 'NGC_attested'), ('FAILED', 'FAILED_AT_STAGE', 'ROUTE_A_NO_FIXED_POINT'),
        outcomes, STAGES, (1, 3), (True, False)):
    res = {'status': status, 'stage_records': STAGES[stage_key]}
    if outcome != '<absent>':
        res['route_a_outcome'] = {'outcome': None if outcome == '<None>' else outcome}
    rp = put(res)
    mon = {'status': 'CHILD_FAILED', 'driver_status': status, 'exit_code': exit_code, 'stop_reason': None,
           'result': {'path': rp[0], 'sha256': rp[1]}, 'pins': {'spec': {'sha256': spec}, 'driver': {'path': driver[0], 'sha256': driver[1]}}}
    rec = put(mon)
    fin = put({'status': status, 'result_path': rp[0], 'result_sha256': rp[1]})[0] if with_finish else str(work / 'absent_finish.json')
    drivers = {driver[1]: 'DDO' if lane == 'DDO' else 'NGC'}
    att = put({'status': 'POST_SEAL_ATTESTED', 'authority': 'Claude2', 'receipt_sha256': rec[1], 'spec_sha256': spec,
               'driver_sha256': driver[1]}) if lane == 'NGC_attested' else None
    case = dict(lane=lane, status=status, outcome=outcome, stages=stage_key, exit_code=exit_code, finish=with_finish)
    try:
        row = m.classify(rec, fin, att, drivers=drivers, vocabularies=vocab)
    except BaseException as e:
        problems.append(dict(case, problem='RAISED ' + type(e).__name__)); continue
    b = row.get('bound_shas', {}) if isinstance(row, dict) else {}
    bad = []
    if not isinstance(row, dict) or type(row.get('model_outcome')) is not bool or not isinstance(row.get('model_outcome_reason'), str): bad.append('ROW_FORM')
    if b.get('receipt') != rec[1]: bad.append('RECEIPT_BINDING')
    if b.get('spec') != spec or b.get('driver') != driver[1]: bad.append('SPEC_DRIVER_BINDING')
    if row.get('status') != status: bad.append('STATUS_BINDING')
    if b.get('result') is not None and b.get('result') != rp[1]: bad.append('RESULT_BINDING')
    counted = row.get('model_outcome') is True
    if counted and outcome not in ('ITERATION_BUDGET_EXHAUSTED',) and status == 'ROUTE_A_NO_FIXED_POINT' and outcome in ('<absent>', '<None>', 'UNKNOWN_X'):
        bad.append('UNKNOWN_OUTCOME_COUNTED')
    if bad: problems.append(dict(case, problem=bad, reason=row.get('model_outcome_reason')))
    rows.append(dict(case, model_outcome=row.get('model_outcome'), reason=row.get('model_outcome_reason')))
summary = {'producer': {'path': str(prod), 'sha256': hashlib.sha256(prod.read_bytes()).hexdigest()}, 'cases': len(rows) + sum(1 for p in problems if str(p.get('problem', '')).startswith('RAISED')),
           'rows': len(rows), 'problems': len(problems), 'counted_rows': sum(1 for r in rows if r['model_outcome']),
           'reasons': sorted({r['reason'] for r in rows}), 'first_problems': problems[:12]}
with open(work / 'TOTALITY_SUMMARY.json', 'x') as f: f.write(json.dumps(summary, indent=1, sort_keys=True) + '\n')
with open(work / 'TOTALITY_ROWS.json', 'x') as f: f.write(json.dumps(rows, indent=1, sort_keys=True) + '\n')
print(json.dumps({k: summary[k] for k in ('cases', 'rows', 'problems', 'counted_rows', 'reasons')}))
