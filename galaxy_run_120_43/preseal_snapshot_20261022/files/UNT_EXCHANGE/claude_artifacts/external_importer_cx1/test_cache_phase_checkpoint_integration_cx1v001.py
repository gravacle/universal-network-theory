"""Inert integration of real cache verifier, phase callback, journal and checkpoint.
Original cache validator and authenticated resolver remain explicit test doubles.
"""
from pathlib import Path
import os,fcntl,tempfile,types,json,hashlib
from phase_journal_storage_cx1v001 import append,read
from cache_phase_checkpoint_adapter_cx1v001 import make_phase_use
from cache_verify_scope_cx1v003 import make_verifier
from snapshot_cx1v001 import Refusal
b=Path(__file__).parent;c=Path(tempfile.mkdtemp(prefix='cache_phase_integration_',dir=b/'inert_fixtures'));passed=[]
for name in ['provisional','final_pass','invalid_before','invalid_during','stale_during','original_raises','entry_mutation']:
 w=c/name;w.mkdir();d=w/'journal';d.mkdir()
 fd=os.open(w/'ORCHESTRATOR.lock',os.O_CREAT|os.O_EXCL|os.O_RDWR,0o600);fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
 lock=types.SimpleNamespace(held=True,_fd=fd,path=w/'ORCHESTRATOR.lock');ctx=types.SimpleNamespace(work_dir=w);self=types.SimpleNamespace(ctx=ctx)
 a=dict(directory=d,work_dir=w,lock=lock,phase_id='INERT');count=[0];calls=[];original_calls=[];binding={}
 def publish():
  j=read(**a);obj=dict(schema='CX1_PHASE_CHECKPOINT_V001',phase_id='INERT',directory=str(d),event_count=len(j['events']),head_sha256=j['head_sha256']);raw=json.dumps(obj).encode();p=w/('checkpoint_%d.json'%count[0]);count[0]+=1
  with p.open('xb') as f:f.write(raw)
  binding.update(checkpoint_pin=dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest()),directory=str(d),phase_id='INERT',import_id='i')
 def resolve(ctx,entry):calls.append(1);return dict(binding)
 def original(self,entry,stem):
  original_calls.append(1);assert hasattr(ctx,'_cx1_cache_snapshot')
  if name in ('invalid_during','stale_during'):
   append(**a,kind='FINAL_INVALIDATE',subject='')
   if name=='invalid_during':publish()
  if name=='original_raises':raise Refusal('INERT_ORIGINAL_FAILURE')
  if name=='entry_mutation':entry['changed']=True
  return 'INERT_VALIDATED'
 try:
  append(**a,kind='ADMIT',subject='i');append(**a,kind='CONSUME',subject='i')
  if name in ('final_pass','invalid_before'):append(**a,kind='FINAL_PASS' if name=='final_pass' else 'FINAL_INVALIDATE',subject='')
  publish();phase_use=make_phase_use(resolve=resolve,held_lock=lambda ctx:lock)
  verify=make_verifier(original,chain_modules=[],phase_use=phase_use,held_lock=lambda ctx:lock)
  try:result=verify(self,{'provenance':{'execution_origin':'DIRECT_EXTERNAL'}},'inert')
  except Refusal:result='REFUSED'
  assert result==('INERT_VALIDATED' if name in ('provisional','final_pass') else 'REFUSED'),(name,result)
  assert not hasattr(ctx,'_cx1_cache_snapshot'),name
  assert len(original_calls)==(0 if name=='invalid_before' else 1),name
  assert len(calls)==(1 if name in ('invalid_before','original_raises','entry_mutation') else 2),name
  if name in ('invalid_before','invalid_during','stale_during'):assert read(**a)['state']['freeze_campaign'] is True
  passed.append(name)
 finally:fcntl.flock(fd,fcntl.LOCK_UN);os.close(fd)
with (c/'TEST_REPORT.json').open('x') as f:json.dump(dict(tested=passed,untested=['Authenticated resolver','Real acceptance validator','Installed cache path','Campaign freeze enforcement'],scope='Real cache wrapper and checkpoint callback with inert validator and resolver; fresh before/after phase checks and snapshot cleanup'),f,indent=2)
print(c/'TEST_REPORT.json')
