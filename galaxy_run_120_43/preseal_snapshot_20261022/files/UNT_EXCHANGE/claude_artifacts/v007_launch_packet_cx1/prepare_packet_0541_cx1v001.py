"""Prepare generator successor after0541/0543. Does not invoke generator or any launch."""
import ast
from pathlib import Path
R=Path(__file__).parent;s=(R/'make_launch_packet_cx1v006.py').read_text()
s=s.replace('route_a_token_launcher_cx1v001.py','route_a_token_launcher_cx1v004.py').replace('producer_guard_cx1v004.py','producer_guard_cx1v006.py')
s=s.replace('TOKEN_COST_PREVIEW_V004','TOKEN_COST_PREVIEW_V005').replace('LAUNCH_PLAN_V004','LAUNCH_PLAN_V005').replace('CASES_MANIFEST_TEMPLATE_V004','CASES_MANIFEST_TEMPLATE_V005').replace('LAUNCH_COMMAND_V004','LAUNCH_COMMAND_V005').replace('_MS128_CX1_RUN_V004','_MS128_CX1_RUN_V005').replace('_CX1_LAUNCHER_V004','_CX1_LAUNCHER_V005')
s=s.replace(' --seal "$SEAL_PATH" --seal-sha "$SEAL_SHA256" --execute-root-only',' --execute-root-only')
s=s.replace('Set exact sealed path/hash.','Root admission config must pin the actual seal; no argv seal authority.')
s=s.replace('Any failed receipt, missing required routeA finish or malformed progress stops new starts; existing monitors finish under caps','Ordinary case failures continue; new starts halt only on systemic memory/disk/setup failures or absent monitor receipt; root decides relaunches')
s=s.replace('# 2x contention planning multiplier, then2x margin over that scenario for cutoff.','#0538 wall cutoff about2x solo scenario; concurrency uses progress tokens.')
s=s.replace(" print('UNTESTED concurrent projection hours'", " print('UNTESTED token-schedule projection hours'")
needle=" if preview:write(R/'P128/TOKEN_COST_PREVIEW_V005.json',o)"
insert=""" worker_file=R/'R5_WORKER_SHA256_0541_V001.txt';worker_pins=[]
 for line in worker_file.read_text().splitlines():
  digest,path=line.split('  ',1);ref=pin(Path(path))
  if ref['sha256']!=digest:raise ValueError('R5_WORKER_BYTES_CHANGED')
  worker_pins.append(ref)
 o['runtime_worker_pin_file']=pin(worker_file);o['runtime_worker_pins']=worker_pins
"""
assert needle in s;s=s.replace(needle,insert+needle)
ast.parse(s)
with (R/'make_launch_packet_cx1v007.py').open('x') as f:f.write(s)
print('generator7 prepared; not executed')
