"""Exclusive-file phase journal storage prerequisite, not authenticated ingestion.
Caller serializes every read/append with the actual parent work lock. Root event
provenance and consumer freeze enforcement are separate and remain unimplemented.
Partial files after a crash remain present and make reads refuse; never repaired here.
"""
import os,json,hashlib
from pathlib import Path
from snapshot_cx1v001 import Snapshot
from phase_invalidation_cx1v001 import project
from valid_admission_cx1v002 import check_held_lock
from request_guard_cx1v002 import require

def read(*,directory,work_dir,lock,phase_id):
 check_held_lock(lock,work_dir);d=Path(directory);w=Path(work_dir)
 require(d.is_absolute() and str(d.resolve())==str(d) and w in d.parents and d.is_dir(),'JOURNAL_DIRECTORY')
 files=sorted(d.iterdir());events=[];previous=None;s=Snapshot()
 for i,p in enumerate(files):
  require(p.name=='%08d.json'%i,'JOURNAL_SEQUENCE')
  raw=s.read(p);obj=s.document(dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest()))
  require(type(obj) is dict and set(obj)=={'schema','previous_sha256','event'} and obj['schema']=='CX1_PHASE_EVENT_FILE_V001','JOURNAL_SCHEMA')
  require(obj['previous_sha256']==previous,'JOURNAL_CHAIN')
  events.append(obj['event']);previous=hashlib.sha256(raw).hexdigest()
 state=project(events,phase_id);check_held_lock(lock,work_dir)
 return dict(events=events,head_sha256=previous,state=state,storage_only=True)

def append(*,directory,work_dir,lock,phase_id,kind,subject):
 current=read(directory=directory,work_dir=work_dir,lock=lock,phase_id=phase_id)
 event=dict(seq=len(current['events']),phase_id=phase_id,kind=kind,subject=subject)
 project(current['events']+[event],phase_id) # validate before creating any file
 obj=dict(schema='CX1_PHASE_EVENT_FILE_V001',previous_sha256=current['head_sha256'],event=event)
 raw=(json.dumps(obj,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
 p=Path(directory)/('%08d.json'%event['seq']);check_held_lock(lock,work_dir)
 with p.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
 fd=os.open(str(Path(directory)),os.O_RDONLY)
 try:os.fsync(fd)
 finally:os.close(fd)
 check_held_lock(lock,work_dir)
 return dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest())
