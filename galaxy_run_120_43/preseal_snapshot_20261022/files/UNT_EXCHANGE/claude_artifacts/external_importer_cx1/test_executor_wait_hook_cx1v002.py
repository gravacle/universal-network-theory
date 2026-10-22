"""Real wait policy and lock checks; authenticated observer/admission/parent are doubles."""
import tempfile,types,fcntl,os,json,hashlib
from pathlib import Path
import executor_hook_cx1v004 as H
from snapshot_cx1v001 import Refusal
b=Path(__file__).resolve().parent;c=Path(tempfile.mkdtemp(prefix='wait_hook_',dir=b/'inert_fixtures'));(c/'waves').mkdir()
fd=os.open(c/'ORCHESTRATOR.lock',os.O_CREAT|os.O_EXCL|os.O_RDWR,0o600);fcntl.flock(fd,fcntl.LOCK_EX)
lock=types.SimpleNamespace(held=True,_fd=fd,path=c/'ORCHESTRATOR.lock')
base=types.ModuleType('inert_parent');calls=[]
base.run_campaign=lambda **kw:(calls.append('normal') or ([{'call_dir':'local'}],{}))
class Parent:
 def __init__(self):self.ctx=types.SimpleNamespace(work_dir=c,C=base)
 def execute(self,*args):return self.ctx.C.run_campaign()
class Scheduler:
 @staticmethod
 def run_campaign(_admitted_external,**kw):calls.append('import');return (list(_admitted_external.values()),{})
plan={'calls':[dict(key='k',spec_sha256='s',call_index=0)]}
common=dict(natural_plan_committed=True,registered=True,identity_bound=True,runtime_environment_bound=True,envelope_valid=True)
def state(direct_state,**kw):return dict(common,direct_state=direct_state,**kw)
scenarios=[('pending_to_valid',[state('RUNNING'),state('TERMINAL',outcome='COMPLETED_VALID',acceptance='ACCEPTED')],'import'),('cap',[state('TERMINAL',outcome='CAP_UNCOUNTED')],'normal'),('unknown',[state('UNKNOWN')],'refuse'),('poll_limit',[state('RUNNING')],'refuse'),('invalid',[state('TERMINAL',outcome='COMPLETED_INVALID')],'refuse')]
passed=[]
try:
 for index,(name,observations,expected) in enumerate(scenarios):
  wave=c/'waves'/('wave_%04d'%(index+1));wave.mkdir()
  with (wave/'WAVE_PLAN.json').open('x') as f:json.dump(plan,f)
  executor=H.make_executor_type(Parent,Scheduler)();executor._external_lock=lambda:lock
  executor._external_candidates=[dict(key='k',spec={'sha256':'s'},call_dir=str(c/'external'))]
  seen=[]
  def observe(candidate,call):
   seen.append(candidate['key']);return observations[min(len(seen)-1,len(observations)-1)]
  executor._external_observe=observe;executor._external_pause=lambda:None;executor._external_max_polls=2
  executor._validate=lambda candidate:{'receipt':{'receipt_sha256':'INERT'}}
  calls.clear()
  try:executor.execute(wave,plan,False,None)
  except Refusal:assert expected=='refuse' and not calls,name
  else:assert calls==[expected],(name,calls)
  assert executor.ctx.C is base
  passed.append(name)
 for index,mode in enumerate(['bad_wave_name','plan_mismatch','missing_plan']):
  wave=c/'waves'/('wave_BAD' if mode=='bad_wave_name' else 'wave_%04d'%(100+index));wave.mkdir()
  if mode!='missing_plan':
   with (wave/'WAVE_PLAN.json').open('x') as f:json.dump({'wrong':True} if mode=='plan_mismatch' else plan,f)
  calls.clear();seen.clear()
  try:executor.execute(wave,plan,False,None)
  except Refusal:assert not calls and not seen
  else:raise AssertionError(mode)
  passed.append(mode)
finally:fcntl.flock(fd,fcntl.LOCK_UN);os.close(fd)
r=dict(status='PASS',blocking_count=0,scope=__doc__,tested=passed,untested=['Authenticated live observer','Real parent/scheduler/cache integration','Actual sleeping or direct-call liveness','Envelope timing pending deputy'],pins=[dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in [Path(H.__file__),Path(__file__),b/'wait_registered_cx1v001.py',b/'inflight_policy_cx1v001.py']])
with (c/'TEST_REPORT.json').open('x') as f:json.dump(r,f,indent=2);f.write('\n')
print(c/'TEST_REPORT.json')
