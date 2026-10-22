import tempfile,json,hashlib,copy
from pathlib import Path
from snapshot_cx1v001 import Snapshot,Refusal
from terminal_association_cx1v001 import SCHEMA
from terminal_snapshot_cx1v001 import observe
from inflight_policy_cx1v001 import decide
root=Path(__file__).resolve().parent;case=Path(tempfile.mkdtemp(prefix='terminal_',dir=root/'inert_fixtures'))
def write(p,d):
 p.parent.mkdir(parents=True,exist_ok=True)
 raw=json.dumps(d,sort_keys=True,separators=(',',':')).encode()
 with p.open('xb') as f:f.write(raw)
 return dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest())
spec=write(case/'spec.json',{'inert':1});driver=write(case/'driver.json',{'inert':2});monitor=write(case/'monitor.json',{'inert':3})
caps=dict(wall_cap_s=10,rss_cap_bytes=100,output_cap_bytes=100,poll_s=1)
passed=[];serial=0
def run(status='FINISHED',code=0,stop=None,mutate=lambda r,l:None):
 global serial
 serial+=1;d=case/str(serial);out=str(d/'out');python='/inert/python'
 pins=dict(spec=spec,driver=driver,monitor=monitor,python=python)
 cmd=[python,'-I','-B',driver['path'],'run','--spec',spec['path'],'--outdir',out]
 l=dict(schema=SCHEMA+'_LAUNCH',utc='2026-01-01T00:00:00Z',command=cmd,pins=pins,caps=caps,child_pid=123,retries_allowed=0)
 r=dict(schema=SCHEMA,utc_start=l['utc'],utc_end='2026-01-01T00:00:01Z',command=cmd,pins=pins,caps=caps,child_pid=123,retries=0,status=status,exit_code=code,stop_reason=stop,result=None)
 mutate(r,l)
 r['receipt_sha256']=hashlib.sha256(json.dumps(r,sort_keys=True,separators=(',',':')).encode()).hexdigest()
 rp=write(d/'RECEIPT.json',r);lp=write(d/'RECEIPT.json.launch.json',l)
 snap=Snapshot();result=observe(snap,call_root=str(d),spec=spec,driver=driver,monitor=monitor,python=python,caps=caps)
 assert all(n==1 for n in snap.read_counts.values())
 return result
assert run()['outcome'] is None;passed.append('finished does not assert VALID')
assert run('CHILD_FAILED',1)['outcome']=='INFRA_UNCOUNTED';passed.append('child failure uncounted')
for stop in ('WALL_CAP','RSS_CAP','OUTPUT_CAP'):
 assert run('STOPPED_'+stop,-15,stop)['outcome']=='CAP_UNCOUNTED';passed.append(stop)
for name,mutate in [('foreign pid',lambda r,l:l.update(child_pid=999)),('foreign start',lambda r,l:l.update(utc='2025-01-01T00:00:00Z')),('retries',lambda r,l:r.update(retries=1)),('finished nonzero',lambda r,l:r.update(exit_code=1)),('unknown status',lambda r,l:r.update(status='RUNNING')),('result outside root',lambda r,l:r.update(result=spec)),('foreign command',lambda r,l:l.update(command=['foreign']))]:
 try:run(mutate=mutate)
 except Refusal:passed.append(name)
 else:raise AssertionError(name)
missing=observe(Snapshot(),call_root=str(case/'MISSING'),spec=spec,driver=driver,monitor=monitor,python='/inert/python',caps=caps)
assert missing['direct_state']=='UNKNOWN' and decide(natural_plan_committed=True,registered=True,identity_bound=True,runtime_environment_bound=True,envelope_valid=True,**missing)=='HOLD_UNKNOWN_EXTERNAL_STATE'
passed.append('missing receipt holds, never permits fallback')
r=dict(status='PASS',blocking_count=0,scope='Terminal association prerequisites; all evidence inert',tested=passed,untested=['Runtime/environment/root register authentication','Real monitor-produced records or process liveness','Executor wait/fallback integration'],pins=[dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in [Path(__file__),root/'terminal_association_cx1v001.py',root/'terminal_snapshot_cx1v001.py']])
p=case/'TEST_REPORT.json';write(p,r);print(p)
