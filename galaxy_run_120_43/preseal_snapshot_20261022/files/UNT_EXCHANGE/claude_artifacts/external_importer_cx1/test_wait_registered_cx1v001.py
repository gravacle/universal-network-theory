"""Wait orchestration only: authenticated-observer and clock doubles, real fixture flock."""
import fcntl,os,types,tempfile,json,hashlib
from pathlib import Path
from wait_registered_cx1v001 import wait_registered
from snapshot_cx1v001 import Refusal
root=Path(__file__).resolve().parent
case=Path(tempfile.mkdtemp(prefix='wait_',dir=root/'inert_fixtures'))
fd=os.open(case/'ORCHESTRATOR.lock',os.O_CREAT|os.O_EXCL|os.O_RDWR,0o600);fcntl.flock(fd,fcntl.LOCK_EX)
lock=types.SimpleNamespace(held=True,_fd=fd,path=case/'ORCHESTRATOR.lock')
base=dict(natural_plan_committed=True,registered=True,identity_bound=True,runtime_environment_bound=True,envelope_valid=True,direct_state='RUNNING')
passed=[]
def run(obs,limit=None,pause=lambda:None):
 it=iter(obs)
 return wait_registered(lock=lock,work_dir=case,observe=lambda:next(it),pause=pause,max_polls=limit or len(obs))
try:
 valid=dict(base,direct_state='TERMINAL',outcome='COMPLETED_VALID',acceptance='ACCEPTED')
 r=run([base,dict(valid,acceptance='PENDING'),valid]);assert r['trace']==['WAIT_EXTERNAL','WAIT_ACCEPTANCE','VALIDATE_EXACT_IMPORT'];passed.append('running to acceptance pending to exact validation')
 for outcome in ('CAP_UNCOUNTED','INFRA_UNCOUNTED'):
  assert run([base,dict(base,direct_state='TERMINAL',outcome=outcome)])['action']=='NORMAL_CAMPAIGN_UNCOUNTED_FALLBACK';passed.append(outcome+' fallback only after terminal observation')
 assert run([base,base])['action']=='HOLD_POLL_LIMIT';passed.append('poll exhaustion holds without fallback')
 assert run([dict(base,direct_state='UNKNOWN')])['action']=='HOLD_UNKNOWN_EXTERNAL_STATE';passed.append('unknown liveness holds')
 assert run([dict(base,direct_state='TERMINAL',outcome='COMPLETED_INVALID')])['action']=='RETAIN_SPECULATIVE_INVALID_FOR_ROOT';passed.append('speculative invalid retained for root')
 assert run([dict(valid,acceptance='FAILED')])['action']=='RETAIN_FAILED_ACCEPTANCE_FOR_ROOT';passed.append('failed acceptance retained for root')
 try:run([dict(base,registered=False)])
 except Refusal:passed.append('registration disappearance refuses')
 else:raise AssertionError('disappeared accepted')
 try:run([base,valid],pause=lambda:setattr(lock,'held',False))
 except Refusal:passed.append('lost lock during wait refuses before another observation')
 else:raise AssertionError('lost lock accepted')
 lock.held=True
finally:fcntl.flock(fd,fcntl.LOCK_UN);os.close(fd)
r=dict(status='PASS',blocking_count=0,scope=__doc__,tested=passed,untested=['Authenticated observer construction','Actual waiting or external run polling','Executor integration and fallback launch'],pins=[dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in [Path(__file__),root/'wait_registered_cx1v001.py',root/'inflight_policy_cx1v001.py']])
p=case/'TEST_REPORT.json'
with p.open('x') as f:json.dump(r,f,indent=2);f.write('\n')
print(p)
