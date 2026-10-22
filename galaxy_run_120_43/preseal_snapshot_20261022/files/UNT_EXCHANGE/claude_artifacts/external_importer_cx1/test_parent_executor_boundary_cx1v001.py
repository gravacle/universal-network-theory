"""Actual executor hook, wait policy, callback, observer; inert parent only.
No scientific scheduler or parent implementation is loaded/executed.
"""
from pathlib import Path
import tempfile,json,hashlib,contextlib,io
b=Path(__file__).parent;out=Path(tempfile.mkdtemp(prefix='executor_observer_chain_',dir=b/'inert_fixtures'))
base=b/'test_natural_registered_observation_cx1v005.py';source=base.read_text();prefix=source[:source.index("try:\n got=observe(**a)")]
tail=r"""
from pinned_helper_loader_cx1v001 import prepare
policy=json.loads((b/'IMPORTER_POLICY_DRAFT_CX1V006.json').read_bytes())
assert hashlib.sha256((b/'pinned_helper_loader_cx1v001.py').read_bytes()).hexdigest()=='8be6c013c1710654c904b0d8f116dde3604cfbab76e48fb04e35ecc6438183f0'
private=prepare(policy['components'])
make_type=private('observation_executor_factory_cx1v002').make_type
Refusal=private('snapshot_cx1v001').Refusal
from executor_observer_adapter_cx1v001 import make_observer
calls=[]
# Extract only the three reviewed parent methods; no module initialization.
import ast
parent_path=b.parent/'calibration_orchestrator_c2/v005/calibration_orchestrator_c2v005.py'
parent_raw=parent_path.read_bytes()
assert hashlib.sha256(parent_raw).hexdigest()=='c75a889ff4646a816329756124a19532cbc166d26f47ce2ea5147b71c2cf7c4d'
tree=ast.parse(parent_raw);cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='CampaignExecutor')
methods=[n for n in cls.body if isinstance(n,ast.FunctionDef) and n.name in ('__init__','campaign_dict','execute')]
assert len(methods)==3
cls.body=methods;cls.decorator_list=[];cls.bases=[];cls.keywords=[]
namespace={'OrchestratorError':RuntimeError}
exec(compile(ast.fix_missing_locations(ast.Module(body=[cls],type_ignores=[])),str(parent_path),'exec'),namespace)
InertParent=namespace['CampaignExecutor']
ctx.cfg.update(per_call={k:v for k,v in caps.items() if k!='poll_s'},campaign_wall_cap_s=100,driver=ctx.driver)
ctx.max_concurrent=1;ctx.process_budget=1;ctx.stage_aware=False;ctx.python=PYTHON
scheduled=[]
def inert_scheduler(**kw):
 calls.append('scheduler boundary');scheduled.append(kw)
 assert kw['campaign']['calls']==[{'spec':plan['calls'][0]['spec']}]
 assert kw['campaign']['per_call']==ctx.cfg['per_call']
 assert kw['campaign']['driver']==ctx.driver and kw['python']==PYTHON
 assert kw['resume'] is False and kw['campaign_dir']==str(wd/'campaign')
 return dict(ok=True,calls=[],status='INERT_NO_PROCESS',launched=0)
ctx.C=types.SimpleNamespace(run_campaign=inert_scheduler)
E=make_type(InertParent,root_binding_pin=rb,expected_policy=root['policy'],expected_entry=root['entry'],theta_key=lambda theta:key,lock_for=lambda ex:lock,context_for=lambda ex:ctx,pause=lambda:None,max_polls=1)
ex=E(ctx)
assert not hasattr(ex,'_external_orch') and ex._external_context is ex.ctx
Bad=make_type(InertParent,root_binding_pin=rb,expected_policy=root['policy'],expected_entry=root['entry'],theta_key=lambda theta:key,lock_for=lambda ex:lock,context_for=lambda ex:types.SimpleNamespace(),pause=lambda:None,max_polls=1)
try:Bad(ctx)
except Refusal as exc:assert str(exc)=='FACTORY_CONTEXT_IDENTITY'
else:raise AssertionError('foreign context accepted')
try:ex._validate({})
except Refusal as exc:assert str(exc)=='VALID_ADMISSION_NOT_INSTALLED'
else:raise AssertionError('VALID admission unexpectedly enabled')

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
p=write('EXECUTOR_REPORT.json',dict(name=name,status='PASS',parent_calls=len(calls),refused=refused,scope='actual parent __init__/campaign_dict/execute; private factory; inert scheduler; resume=False'))
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
