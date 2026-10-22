"""Hook control flow only. Admission and scheduler are explicit test doubles."""
import fcntl,os,types,hashlib,json
from pathlib import Path
from datetime import datetime,timezone
import executor_hook_cx1v002 as H
root=Path(__file__).resolve().parent
case=root/'inert_fixtures'/datetime.now(timezone.utc).strftime('hook_%Y%m%dT%H%M%S%f');case.mkdir(parents=True,exist_ok=False)
fd=os.open(case/'ORCHESTRATOR.lock',os.O_CREAT|os.O_EXCL|os.O_RDWR,0o600);fcntl.flock(fd,fcntl.LOCK_EX)
lock=types.SimpleNamespace(held=True,_fd=fd,path=case/'ORCHESTRATOR.lock')
base=types.ModuleType('_spy_campaign')
base.run_campaign=lambda **kw:([{'index':i,'status':'OK','call_dir':'local'} for i in range(2)],{'normal':True})
class Parent:
 def __init__(self):self.ctx=types.SimpleNamespace(work_dir=case,C=base)
 def execute(self,wd,plan,resume,log):return self.ctx.C.run_campaign()
 def classify(self,c,r):return ('PARENT',None,None,{})
class Scheduler:
 @staticmethod
 def run_campaign(_admitted_external,**kw):
  return ([_admitted_external.get(i,{'index':i,'status':'OK','call_dir':'local'}) for i in range(2)],{'normal':True})
T=H.make_executor_type(Parent,Scheduler);e=T();e._external_lock=lambda:lock
plan={'calls':[{'key':'k0','spec_sha256':'s0','call_index':0},{'key':'k1','spec_sha256':'s1','call_index':1}]}
e._external_candidates=[{'key':'k0','spec':{'sha256':'s0'},'call_dir':str(case/'direct')}, {'key':'UNREQUESTED','spec':{'sha256':'sx'},'call_dir':'NEVER_OPEN'}]
validated=[]
def validate(candidate):
 validated.append(candidate['key']);return {'receipt':{'receipt_sha256':'r'},'classification':'VALID','failure_class':None,'forward':{},'provenance':{'call_dir':candidate['call_dir']}}
e._validate=validate
passed=[]
try:
 records,meta=e.execute(case/'wave',plan,False,None)
 assert validated==['k0'] and records[0]['execution_origin']=='DIRECT_EXTERNAL' and records[1]['call_dir']=='local'
 assert meta['external_call_indices']==[0] and e.ctx.C is base
 passed.append('mixed selected indices and proxy restoration')
 assert e.classify(plan['calls'][0],records[0])[0]=='VALID' and validated==['k0','k0']
 passed.append('fresh admission at ingest')
 assert e.classify(plan['calls'][1],records[1])[0]=='PARENT';passed.append('normal classifier retained')
 e._external_candidates=[];r,m=e.execute(case/'wave2',plan,False,None)
 assert m=={'normal':True} and all(x['call_dir']=='local' for x in r);passed.append('no match uses parent')
 e._external_candidates=[{'key':'k0','spec':{'sha256':'wrong'},'call_dir':'NEVER_OPEN'}]
 r,m=e.execute(case/'wave3',plan,False,None);assert m=={'normal':True};passed.append('different spec falls back without admission')
 e._external_candidates=[{'key':'k0','spec':{'sha256':'s0'},'call_dir':str(case/'direct')}]*2
 try:e.execute(case/'duplicate',plan,False,None)
 except H.Refusal as ex:assert 'AMBIGUOUS_EXTERNAL_CANDIDATE' in str(ex)
 else:raise AssertionError('duplicate accepted')
 passed.append('duplicate candidate refuses')
 e._external_candidates=e._external_candidates[:1]
 local=case/'already'/'campaign'/'call_0000';local.mkdir(parents=True)
 before=len(validated);r,m=e.execute(case/'already',plan,False,None)
 assert len(validated)==before and m=={'normal':True}
 passed.append('existing local execution is not substituted')
 saved=Scheduler.run_campaign
 def fail(**kw):raise RuntimeError('INERT scheduler failure')
 Scheduler.run_campaign=fail
 try:e.execute(case/'failure',plan,False,None)
 except RuntimeError as ex:assert str(ex)=='INERT scheduler failure'
 else:raise AssertionError('failure swallowed')
 assert e.ctx.C is base;Scheduler.run_campaign=saved
 passed.append('scheduler failure restores original private context')
 lock.held=False
 try:e.execute(case/'unheld',plan,False,None)
 except H.Refusal as ex:assert 'WORK_LOCK_REQUIRED' in str(ex)
 else:raise AssertionError('unheld accepted')
 lock.held=True;passed.append('unheld lock refuses before dispatch')
finally:fcntl.flock(fd,fcntl.LOCK_UN);os.close(fd)
report={'status':'PASS','blocking_count':0,'scope':'executor hook control-flow only','tested':passed,'untested':['real parent execution','real admission through hook','cache integration','whole engine'], 'pins':[{'path':str(f),'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for f in [Path(H.__file__),Path(__file__)]]}
with (case/'TEST_REPORT.json').open('x') as f:json.dump(report,f,indent=2);f.write('\n')
print(case/'TEST_REPORT.json')
