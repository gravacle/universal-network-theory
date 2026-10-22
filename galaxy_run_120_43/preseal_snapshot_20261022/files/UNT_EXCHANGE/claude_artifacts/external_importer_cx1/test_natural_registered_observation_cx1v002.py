"""Composition test: natural/register/runtime/invocation dependencies are doubles.
Actual Snapshot, interpreter byte association, terminal association and inflight policy.
"""
import tempfile,json,hashlib,types
from pathlib import Path
import natural_registered_observation_cx1v002 as m
from terminal_association_cx1v001 import SCHEMA
from inflight_policy_cx1v001 import decide
from snapshot_cx1v001 import Refusal
b=Path(__file__).parent;c=Path(tempfile.mkdtemp(prefix='observer_composition_',dir=b/'inert_fixtures'))
def write(n,o):
 p=c/n;p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('x') as f:json.dump(o,f)
 return dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
sp=write('spec.json',{'inert':1});driver=write('driver.json',{});monitor=write('monitor.json',{});plan=write('plan.json',{})
py=c/'fake_python';py.write_bytes(b'INERT NEVER EXECUTE');identity=dict(realpath=str(py),sha256=hashlib.sha256(py.read_bytes()).hexdigest());launch=write('launch.json',dict(interpreter=identity))
ctx=types.SimpleNamespace(work_dir=c,config_sha256='a'*64,cache_id='b'*64,gate_digest='c'*64,driver=driver,cfg={'monitor':monitor});caps=dict(wall_cap_s=10,rss_cap_bytes=20,output_cap_bytes=30,poll_s=2.0)
m.select=lambda *a,**k:dict(key='key',spec_sha256=sp['sha256'],mapped={'raw':Path(sp['path']).read_bytes()})
m.check_held_lock=lambda *a:None
passed=[]
for index,(status,code,expected) in enumerate([(None,0,'HOLD_UNKNOWN_EXTERNAL_STATE'),('FINISHED',0,'HOLD_UNCLASSIFIED_OUTCOME'),('CHILD_FAILED',1,'NORMAL_CAMPAIGN_UNCOUNTED_FALLBACK')]):
 d=c/str(index);entry=dict(key='key',spec=sp,call_root=str(d));reg=write(str(index)+'reg.json',dict(entries=[entry]))
 m.load=lambda *a,**k:dict(register_pin=reg,direct_plan_pin=plan,runtime_policy=dict(driver=driver,monitor=monitor,direct_launch=launch))
 m.check=lambda *a,**k:dict(registered=True,runtime={'entry':entry})
 m.bind_invocation=lambda *a,**k:dict(python=str(py),caps=caps)
 if status:
  pins=dict(spec=sp,driver=driver,monitor=monitor,python=str(py));cmd=[str(py),'-I','-B',driver['path'],'run','--spec',sp['path'],'--outdir',str(d/'out')]
  l=dict(schema=SCHEMA+'_LAUNCH',utc='2026-01-01T00:00:00Z',command=cmd,pins=pins,caps=caps,child_pid=1,retries_allowed=0)
  r=dict(schema=SCHEMA,utc_start=l['utc'],utc_end='2026-01-01T00:00:01Z',command=cmd,pins=pins,caps=caps,child_pid=1,retries=0,status=status,exit_code=code,stop_reason=None,result=None)
  r['receipt_sha256']=hashlib.sha256(json.dumps(r,sort_keys=True,separators=(',',':')).encode()).hexdigest()
  write(str(index)+'/RECEIPT.json',r);write(str(index)+'/RECEIPT.json.launch.json',l)
 args=dict(ctx=ctx,lock=None,wave=1,call_index=0,plan_pin=plan,theta_key=None,root_binding_pin=None,expected_policy=None,expected_entry=None)
 got=m.observe(**args);assert decide(**got)==expected;passed.append(expected)
# Failure before terminal observation must propagate; no fallback.
m.bind_invocation=lambda *a,**k:dict(python=str(py),caps=caps)
bad=write('bad_launch.json',dict(interpreter=dict(identity,sha256='0'*64)))
m.load=lambda *a,**k:dict(register_pin=reg,direct_plan_pin=plan,runtime_policy=dict(driver=driver,monitor=monitor,direct_launch=bad))
try:m.observe(**args)
except Refusal:passed.append('foreign interpreter refuses before terminal result')
else:raise AssertionError('foreign interpreter')
with (c/'TEST_REPORT.json').open('x') as f:json.dump(dict(tested=passed,scope=__doc__),f,indent=2)
print(c/'TEST_REPORT.json')
