"""Read-only checkpoint prerequisite. Caller independently authenticates the pin.
No checkpoint production, event provenance, adoption, or freeze enforcement.
"""
from pathlib import Path
from snapshot_cx1v001 import Snapshot
from request_guard_cx1v002 import require
from phase_journal_storage_cx1v001 import read
from valid_admission_cx1v002 import check_held_lock

def check(*,checkpoint_pin,directory,work_dir,lock,phase_id):
 check_held_lock(lock,work_dir)
 obj=Snapshot().document(checkpoint_pin)
 require(type(obj) is dict and set(obj)=={'schema','phase_id','directory','event_count','head_sha256'},'CHECKPOINT_SCHEMA')
 require(obj['schema']=='CX1_PHASE_CHECKPOINT_V001' and obj['phase_id']==phase_id and obj['directory']==str(Path(directory)),'CHECKPOINT_ASSOCIATION')
 n=obj['event_count'];h=obj['head_sha256']
 require(type(n) is int and n>=0,'CHECKPOINT_COUNT')
 require((n==0 and h is None) or (n>0 and type(h) is str and len(h)==64 and all(c in '0123456789abcdef' for c in h)),'CHECKPOINT_HEAD')
 current=read(directory=directory,work_dir=work_dir,lock=lock,phase_id=phase_id)
 require(len(current['events'])==n and current['head_sha256']==h,'CHECKPOINT_JOURNAL_MISMATCH')
 Snapshot().pin(checkpoint_pin);check_held_lock(lock,work_dir)
 return dict(journal=current,checkpoint=checkpoint_pin,prerequisites_only=True)
