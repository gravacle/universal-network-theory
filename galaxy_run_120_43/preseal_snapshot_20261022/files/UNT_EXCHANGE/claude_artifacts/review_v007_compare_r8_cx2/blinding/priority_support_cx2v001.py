"""Independent 0558 blinding probe. Fresh synthetic manifests; no production run input."""
import contextlib
import copy
import hashlib
import io
import json
import math
import os
import sys
import time
import types
from pathlib import Path
import numpy as np

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parents[1]/'v007_compare_c2/r8/kmax_tail_compare_c2v007_r8.py'
EXPECTED='bd51db152f700afd86c2156904a4998b4582deeac5c06d05def50b27b397e5c3'
BLOCKED=[];READS=set()
def audit(event,args):
    if event.startswith('socket.') or event in ('subprocess.Popen','os.system','os.posix_spawn','os.spawn','os.fork','os.exec'):
        BLOCKED.append(event);raise RuntimeError('Review forbids process/network')
    if event in ('os.remove','os.rmdir','os.rename','os.replace','shutil.rmtree'):
        BLOCKED.append(event);raise RuntimeError('Review forbids destructive mutation')
    if event=='open' and isinstance(args[0],(str,bytes,os.PathLike)):
        p=Path(os.fsdecode(args[0])).resolve();s=str(p);low=s.lower()
        if '/.codex/' in low or '/runs/' in low or '/runs_ext/' in low or 'kmax_a2f10_c5h_run_v001' in low:
            BLOCKED.append(s);raise RuntimeError('Review forbids production run/session read')
        if 'ngc3198' in low and any(x in low for x in ('observed','target','rotmod')):
            BLOCKED.append(s);raise RuntimeError('Review forbids NGC target read')
        flags=args[2];mode=args[1]
        writing=(isinstance(mode,str) and any(x in mode for x in 'wax+')) or isinstance(flags,int) and flags&(os.O_CREAT|os.O_TRUNC|os.O_RDWR|os.O_WRONLY|os.O_APPEND)
        if writing:
            if not p.is_relative_to(HERE.resolve()) or not flags&os.O_EXCL:
                BLOCKED.append(s);raise RuntimeError('Review writes exclusively in own directory')
        else:READS.add(s)
sys.addaudithook(audit)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def pin(p):return {'path':str(p),'sha256':sha(p)}
def write(p,obj):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
    raw=obj if isinstance(obj,bytes) else obj.encode() if isinstance(obj,str) else (json.dumps(obj,indent=2,sort_keys=True)+'\n').encode()
    with p.open('xb') as f:f.write(raw)
    return pin(p)
raw=SOURCE.read_bytes();assert hashlib.sha256(raw).hexdigest()==EXPECTED
M=types.ModuleType('_independent_compare_r8');M.__file__=str(SOURCE);sys.modules[M.__name__]=M
exec(compile(raw,str(SOURCE),'exec'),M.__dict__)
run=HERE/('run_'+time.strftime('%Y%m%dT%H%M%S',time.gmtime())+'_%s'%os.getpid());run.mkdir()
rows=[]
def check(name,ok,detail=None):rows.append({'name':name,'pass':bool(ok),'detail':detail})

