"""Pure planning arithmetic only; no running S0 state or scientific output read."""
import ast
import hashlib
import json
import subprocess
from pathlib import Path

H = Path(__file__).parent
source_path = H/'phase1_ngc_launch_cx3cw8v001.py'
raw = source_path.read_bytes()
assert hashlib.sha256(raw).hexdigest() == '04dfc429e335458494fa377f2f46e8d54adbe7e0f0b9a4c3b2121c6b0964f0c2'
tree = ast.parse(raw)
costs = ast.literal_eval(next(n.value for n in tree.body if isinstance(n, ast.Assign)
    and any(isinstance(t, ast.Name) and t.id=='CW8_COSTS' for t in n.targets)))
node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name=='cw8_schedule')
def need(ok, message):
    if not ok:
        raise ValueError(message)
ns = {'need': need}
exec(compile(ast.Module(body=[node], type_ignores=[]), '<pure cw8 schedule only>', 'exec'), ns)
schedule = ns['cw8_schedule']
rows = []
for n in (1, 2, 3):
    for free in (12, 15, 16, 18):
        scenarios = {}
        for scenario, cost in costs.items():
            barrier = max(0.0, cost['serial_h']-6.0)
            serial = max(barrier, schedule(n, free, 1, cost))
            full8 = max(barrier, schedule(n, free, 8, cost))
            scenarios[scenario] = {'assumed_existing_S0_remaining_h': barrier,
                'new_serial_branch_h': cost['serial_h'],
                'new_cw8_branch_h': schedule(n, free, 8, cost),
                'serial_makespan_from_pair_h': serial, 'cw8_makespan_from_pair_h': full8,
                'predicted_saving_h': serial-full8}
        rows.append({'new_not_started_calls': n, 'available_cores': free,
                     'choose_cw8': all(s['predicted_saving_h']>0 for s in scenarios.values()),
                     'scenarios': scenarios})
for n in (1, 2, 3):
    r = next(x for x in rows if x['new_not_started_calls']==n and x['available_cores']==18)
    assert abs(r['scenarios']['expectation']['predicted_saving_h']-(6.0 if n<=2 else 4.48))<1e-9
    assert abs(r['scenarios']['upper']['predicted_saving_h']-6.0)<1e-9
assert not next(x for x in rows if x['new_not_started_calls']==3 and x['available_cores']==12)['choose_cw8']
out = H/'S0_OPTION_EVIDENCE_CX3V001.json'
doc = {'date_u': subprocess.check_output(['/bin/date','-u'],text=True).strip(),
       'status': 'TESTED_ARITHMETIC_FORMAL_MODEL_NOT_MEASURED_SPEEDUP',
       'script': {'path': str(Path(__file__)), 'sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},
       'source': {'path': str(source_path), 'sha256': hashlib.sha256(raw).hexdigest()},
       'costs_h': costs, 'cases': rows,
       'assumptions': ['pair available at t=6 h',
          'existing S0 critical barrier started at t=0 with same uniform serial-call cost',
          'new call PLAN/certificates are already available at pair time',
          'root observes resource-feasible two-stage schedule; no CPU admission governor in selector',
          'unknown/unmodeled loads choose serial; no S0 restart'],
       'actual_S0_state_read': False, 'scientific_execution': 'NONE'}
with out.open('x') as f:
    json.dump(doc,f,indent=2,sort_keys=True);f.write('\n')
print(json.dumps({'path':str(out),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'cases':len(rows)}))
