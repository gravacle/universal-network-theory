from pathlib import Path
import tempfile,os,fcntl,types,json,hashlib
from phase_journal_storage_cx1v001 import read,append
from phase_invalidation_cx1v001 import require_use
from snapshot_cx1v001 import Refusal
b=Path(__file__).parent;c=Path(tempfile.mkdtemp(prefix='phase_journal_',dir=b/'inert_fixtures'));work=c/'work';work.mkdir();d=work/'journal';d.mkdir()
fd=os.open(work/'ORCHESTRATOR.lock',os.O_CREAT|os.O_EXCL|os.O_RDWR,0o600);fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB);lock=types.SimpleNamespace(held=True,_fd=fd,path=work/'ORCHESTRATOR.lock');args=dict(directory=d,work_dir=work,lock=lock,phase_id='INERT_PHASE');passed=[]
try:
 first=append(**args,kind='ADMIT',subject='import1');original=Path(first['path']).read_bytes()
 append(**args,kind='CONSUME',subject='import1');append(**args,kind='FINAL_INVALIDATE',subject='')
 got=read(**args);assert got['state']['freeze_campaign'] and got['state']['root_escalation_required'];assert Path(first['path']).read_bytes()==original
 passed.append('durable ordered invalidation preserves prior admission bytes')
 try:require_use(got['events'],'INERT_PHASE','import1')
 except Refusal:passed.append('invalidated use refuses')
 else:raise AssertionError('use')
 before=sorted(d.iterdir())
 try:append(**args,kind='FINAL_PASS',subject='')
 except Refusal:passed.append('duplicate final refuses before write')
 else:raise AssertionError('final')
 assert sorted(d.iterdir())==before
 for name,filename,data in [('partial','00000000.json',b'{'),('gap','00000001.json',b'{}'),('chain','00000000.json',json.dumps(dict(schema='CX1_PHASE_EVENT_FILE_V001',previous_sha256='0'*64,event=dict(seq=0,phase_id='INERT_PHASE',kind='ADMIT',subject='x'))).encode())]:
  bad=work/name;bad.mkdir()
  with (bad/filename).open('xb') as f:f.write(data)
  try:read(**dict(args,directory=bad))
  except Refusal:passed.append(name+' refuses')
  else:raise AssertionError(name)
 lock.held=False
 try:read(**args)
 except Refusal:passed.append('unheld lock refuses')
 else:raise AssertionError('lock')
finally:fcntl.flock(fd,fcntl.LOCK_UN);os.close(fd)
with (c/'TEST_REPORT.json').open('x') as f:json.dump(dict(tested=passed,scope='storage only; synthetic events, real held flock; no root provenance or freeze action'),f,indent=2)
print(c/'TEST_REPORT.json')
