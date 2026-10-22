"""Pure inert D002 event projection tests; no real final check, cache or campaign writes."""
import copy,json,hashlib,tempfile
from pathlib import Path
from phase_invalidation_cx1v001 import project,require_use
from snapshot_cx1v001 import Refusal
b=Path(__file__).resolve().parent
phase='INERT_PHASE';events=[];passed=[]
def add(kind,subject=''):events.append(dict(seq=len(events),phase_id=phase,kind=kind,subject=subject))
def refuses(fn):
 try:fn()
 except Refusal:return
 raise AssertionError('expected refusal')
add('ADMIT','a');add('ADMIT','b');add('CONSUME','a')
original=copy.deepcopy(events)
assert require_use(events,phase,'b')=='PROVISIONAL_ENVELOPE';passed.append('pre-final explicitly provisional')
for kind in ['FINAL_INVALIDATE','FINAL_REFUSAL']:
 branch=copy.deepcopy(events)+[dict(seq=3,phase_id=phase,kind=kind,subject='')]
 state=project(branch,phase)
 assert set(state['imports'].values())=={'INVALIDATED_BY_ENVELOPE'} and state['freeze_campaign'] and state['root_escalation_required']
 for subject in ['a','b']:refuses(lambda:require_use(branch,phase,subject))
 for more in ['ADMIT','CONSUME','FINAL_PASS']:
  bad=branch+[dict(seq=4,phase_id=phase,kind=more,subject='a' if more!='FINAL_PASS' else '')]
  refuses(lambda:project(bad,phase))
 passed.append(kind+' invalidates all imports, freezes consumed campaign, refuses use and reopening')
assert events==original;passed.append('original admissions unchanged')
branch=copy.deepcopy(events)+[dict(seq=3,phase_id=phase,kind='FINAL_PASS',subject='')]
assert require_use(branch,phase,'a')=='ENVELOPE_FINAL_PASS';passed.append('final PASS preserves usable imports')
for field,value in [('seq',9),('phase_id','FOREIGN'),('kind','OTHER')]:
 bad=copy.deepcopy(events);bad[0][field]=value;refuses(lambda:project(bad,phase))
 passed.append(field+' mismatch refuses')
empty=[dict(seq=0,phase_id=phase,kind='FINAL_REFUSAL',subject='')]
s=project(empty,phase);assert s['refuse_further_use'] and not s['freeze_campaign'];passed.append('failed empty phase closes without claiming consumed campaign')
report=dict(status='PASS',blocking_count=0,tested=passed,untested=['Authenticated complete append-only event ingestion','Campaign lock and cache/consumer enforcement','Real final envelope check and escalation publication'],pins=[dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in [Path(__file__),b/'phase_invalidation_cx1v001.py']])
c=Path(tempfile.mkdtemp(prefix='phase_projection_',dir=b/'inert_fixtures'))
with (c/'TEST_REPORT.json').open('x') as f:json.dump(report,f,indent=2)
print(c/'TEST_REPORT.json')
