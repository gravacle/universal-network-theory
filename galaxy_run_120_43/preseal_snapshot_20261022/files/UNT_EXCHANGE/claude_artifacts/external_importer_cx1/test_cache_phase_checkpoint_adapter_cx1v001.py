from pathlib import Path
import tempfile,os,fcntl,types,json,hashlib
from phase_journal_storage_cx1v001 import append,read
from cache_phase_checkpoint_adapter_cx1v001 import make_phase_use
from snapshot_cx1v001 import Refusal
b=Path(__file__).parent;c=Path(tempfile.mkdtemp(prefix='cache_phase_checkpoint_',dir=b/'inert_fixtures'));w=c/'work';w.mkdir();d=w/'journal';d.mkdir()
fd=os.open(w/'ORCHESTRATOR.lock',os.O_CREAT|os.O_EXCL|os.O_RDWR,0o600);fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
lock=types.SimpleNamespace(held=True,_fd=fd,path=w/'ORCHESTRATOR.lock');ctx=types.SimpleNamespace(work_dir=w)
a=dict(directory=d,work_dir=w,lock=lock,phase_id='INERT');passed=[];pins=[];calls=[]
def checkpoint():
 j=read(**a);obj=dict(schema='CX1_PHASE_CHECKPOINT_V001',phase_id='INERT',directory=str(d),event_count=len(j['events']),head_sha256=j['head_sha256']);raw=json.dumps(obj).encode();p=c/('checkpoint_%d.json'%len(pins))
 with p.open('xb') as f:f.write(raw)
 pin=dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest());pins.append(pin);return pin
binding=dict(checkpoint_pin=checkpoint(),directory=str(d),phase_id='INERT',import_id='i')
def resolve(ctx,entry):calls.append(1);entry['mutated']=True;return dict(binding)
f=make_phase_use(resolve=resolve,held_lock=lambda ctx:lock)
def case(name,expected):
 entry={'key':'i'}
 try:got=f(ctx,entry)
 except Refusal:got='REFUSED'
 assert got==expected,(name,got);assert entry=={'key':'i'};passed.append(name)
try:
 case('unknown_import','REFUSED')
 append(**a,kind='ADMIT',subject='i');binding['checkpoint_pin']=checkpoint();case('provisional','PROVISIONAL_ENVELOPE')
 append(**a,kind='CONSUME',subject='i');case('stale_checkpoint','REFUSED')
 binding['checkpoint_pin']=checkpoint();case('fresh_after_consume','PROVISIONAL_ENVELOPE')
 append(**a,kind='FINAL_INVALIDATE',subject='');binding['checkpoint_pin']=checkpoint();case('fresh_invalidation','REFUSED')
 assert read(**a)['state']['freeze_campaign'] is True
 binding['import_id']='other';case('unknown_after_final','REFUSED');binding['import_id']='i'
 lock.held=False;case('unheld_lock','REFUSED');lock.held=True
 binding['extra']=True;case('extra_binding_field','REFUSED');binding.pop('extra')
 assert len(calls)==len(passed)
finally:fcntl.flock(fd,fcntl.LOCK_UN);os.close(fd)
with (c/'TEST_REPORT.json').open('x') as h:json.dump(dict(tested=passed,scope='Inert callback with real flock; resolver authentication, cache installation and freeze enforcement untested'),h,indent=2)
print(c/'TEST_REPORT.json')
