"""Actual executor hook, wait policy, callback, observer; inert parent only.
No scientific scheduler or parent implementation is loaded/executed.
"""
from pathlib import Path
import tempfile,json,hashlib,contextlib,io
b=Path(__file__).parent;out=Path(tempfile.mkdtemp(prefix='executor_observer_chain_',dir=b/'inert_fixtures'))
base=b/'test_natural_registered_observation_cx1v005.py';source=base.read_text();prefix=source[:source.index("try:\n got=observe(**a)")]
tail=r"""
from executor_hook_cx1v004 import make_executor_type
from executor_observer_adapter_cx1v001 import make_observer
calls=[]
class InertParent:
 def __init__(self):self.ctx=ctx
 def execute(self,*args):calls.append('parent fallback');return [],{'inert':True}
E=make_executor_type(InertParent,None);ex=E();ex._external_orch=ctx;ex._external_lock=lambda:lock
ex._external_candidates=[dict(key=key,spec=sp,call_dir=str(d))]
ex._external_observe=make_observer(ex,root_binding_pin=rb,expected_policy=root['policy'],expected_entry=root['entry'],theta_key=lambda theta:key)
ex._external_pause=lambda:(_ for _ in ()).throw(AssertionError('unexpected pause'));ex._external_max_polls=1
try:
 if status is not None:
  d.mkdir();pins=dict(spec=sp,driver=ctx.driver,monitor=monitor,python=PYTHON);cmd=[PYTHON,'-I','-B',ctx.driver['path'],'run','--spec',sp['path'],'--outdir',str(d/'out')]
  rcaps=dict(caps)
  if name=='foreign_caps':rcaps['wall_cap_s']=99
  side=dict(schema=SCHEMA+'_LAUNCH',utc='2026-10-21T12:30:00Z',command=cmd,pins=pins,caps=rcaps,child_pid=123,retries_allowed=0)
  receipt=dict(schema=SCHEMA,utc_start=side['utc'],utc_end='2026-10-21T12:31:00Z',command=cmd,pins=pins,caps=rcaps,child_pid=123,retries=0,status=status,exit_code=code,stop_reason=stop,result=None)
  receipt['receipt_sha256']=hashlib.sha256(json.dumps(receipt,sort_keys=True,separators=(',',':')).encode()).hexdigest()
  write(str(d.relative_to(c))+'/RECEIPT.json',receipt);write(str(d.relative_to(c))+'/RECEIPT.json.launch.json',side)
 try:ex.execute(wd,plan,False,None);refused=False
 except Refusal:refused=True
 assert refused != fallback,(name,refused)
 assert len(calls)==int(fallback),(name,calls)
finally:fcntl.flock(fd,fcntl.LOCK_UN);os.close(fd)
p=write('EXECUTOR_REPORT.json',dict(name=name,status='PASS',parent_calls=len(calls),refused=refused,scope='actual hook/wait/observer; inert parent'))
print(p['path'])
"""
variants=[('missing',None,0,None,False),('finished','FINISHED',0,None,False),('child_failure','CHILD_FAILED',1,None,True),('wall','STOPPED_WALL_CAP',-15,'WALL_CAP',True),('rss','STOPPED_RSS_CAP',-15,'RSS_CAP',True),('output','STOPPED_OUTPUT_CAP',-15,'OUTPUT_CAP',True),('foreign_caps','FINISHED',0,None,False)]
results=[]
for name,status,code,stop,fallback in variants:
 text=prefix+tail;p=out/(name+'.py')
 with p.open('x') as f:f.write(text)
 buf=io.StringIO()
 with contextlib.redirect_stdout(buf):exec(compile(text,str(p),'exec'),dict(__file__=str(base),__name__='__main__',name=name,status=status,code=code,stop=stop,fallback=fallback))
 rp=Path(buf.getvalue().strip().splitlines()[-1]);results.append(dict(result=json.loads(rp.read_bytes()),source=dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest()),report=dict(path=str(rp),sha256=hashlib.sha256(rp.read_bytes()).hexdigest())))
with (out/'TEST_REPORT.json').open('x') as f:json.dump(results,f,indent=2)
print(out/'TEST_REPORT.json')
