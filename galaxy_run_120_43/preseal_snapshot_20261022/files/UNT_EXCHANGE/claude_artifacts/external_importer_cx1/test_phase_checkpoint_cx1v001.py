from pathlib import Path
import tempfile,os,fcntl,types,json,hashlib
from phase_journal_storage_cx1v001 import append,read
from phase_checkpoint_cx1v001 import check
from snapshot_cx1v001 import Refusal
b=Path(__file__).parent;c=Path(tempfile.mkdtemp(prefix='phase_checkpoint_',dir=b/'inert_fixtures'));w=c/'work';w.mkdir();d=w/'journal';d.mkdir()
fd=os.open(w/'ORCHESTRATOR.lock',os.O_CREAT|os.O_EXCL|os.O_RDWR,0o600);fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
lock=types.SimpleNamespace(held=True,_fd=fd,path=w/'ORCHESTRATOR.lock');args=dict(directory=d,work_dir=w,lock=lock,phase_id='INERT_PHASE');passed=[]
def pin(name,obj):
 p=c/(name+'.json');raw=json.dumps(obj,sort_keys=True).encode()
 with p.open('xb') as f:f.write(raw)
 return dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest())
def cp(directory,count,head):return dict(schema='CX1_PHASE_CHECKPOINT_V001',phase_id='INERT_PHASE',directory=str(directory),event_count=count,head_sha256=head)
def case(name,obj,expect,**changes):
 p=pin(name,obj)
 try:check(checkpoint_pin=p,**dict(args,**changes))
 except Refusal:
  assert not expect,name
 else:assert expect,name
 passed.append(name)
try:
 case('empty',cp(d,0,None),True)
 first=append(**args,kind='ADMIT',subject='import1')
 one=cp(d,1,first['sha256']);case('exact',one,True)
 append(**args,kind='CONSUME',subject='import1')
 two=cp(d,2,read(**args)['head_sha256']);case('current',two,True)
 case('stale_checkpoint',one,False)
 short=w/'prefix_copy';short.mkdir()
 with (short/'00000000.json').open('xb') as f:f.write(Path(first['path']).read_bytes())
 case('missing_suffix',dict(two,directory=str(short)),False,directory=short)
 case('wrong_phase',dict(two,phase_id='OTHER'),False)
 case('wrong_directory',dict(two,directory=str(short)),False)
 case('wrong_head',dict(two,head_sha256='0'*64),False)
 case('boolean_count',dict(two,event_count=True),False)
 case('extra_field',dict(two,extra=True),False)
 lock.held=False;case('unheld_lock',two,False)
finally:fcntl.flock(fd,fcntl.LOCK_UN);os.close(fd)
with (c/'TEST_REPORT.json').open('x') as f:json.dump(dict(tested=passed,scope='Synthetic checkpoints and journal; actual held flock; no authenticated root or freeze integration'),f,indent=2)
print(c/'TEST_REPORT.json')
