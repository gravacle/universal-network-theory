"""Root-only custody/resource wrapper; no solver import or scientific changes.

Only generated freezes/receipts are written, using the pinned no-overwrite
publisher. Every child invocation is a fresh private process group.
"""
import base64
import hashlib
import json
import os
from pathlib import Path
import runpy
import signal
import subprocess
import sys
import threading
import time
import traceback

sys.dont_write_bytecode = True
ROOT = Path('/Users/bgm/Documents/ChatGPT/Universal Network Theory')
J = ROOT/'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation'
THIS = J/'spherical_two_current_supervisor_v001.py'
PROTOCOL = J/'SPHERICAL_TWO_CURRENT_SUPERVISOR_PROTOCOL_V001.md'
SOURCE = J/'spherical_two_current_v001.py'
SCIENCE_FREEZE = J/'SPHERICAL_TWO_CURRENT_V001_FROZEN.json'
FREEZE = J/'SPHERICAL_TWO_CURRENT_SUPERVISOR_V001_FROZEN.json'
FREEZE_RUN = J/'SPHERICAL_TWO_CURRENT_V001_FREEZE_RUN.json'
FREEZE_INTENT = J/'SPHERICAL_TWO_CURRENT_V001_FREEZE_INTENT.json'
PUBLISHER = J/'run_scientific_case_v001.py'
PINS = {
    SOURCE.name:'0349740de7d0b4173f634eaf8fd52c7e5eb4ea9ea196f95a5b882024f6dd95df',
    'SPHERICAL_TWO_CURRENT_FINITE_R_DESIGN_V001.md':'4733e51a4bf5646861ec3123ab5799b3b3e5662faf8a449b8eb54f7cd4f661c1',
    'SPHERICAL_TWO_CURRENT_PROTOCOL_V001.md':'c124a0e0a361a33860ec4e0470b0380758405740bdb8b7d9f45783b0bf9a5ba2',
    'SPHERICAL_TWO_CURRENT_SCOPE_PREFLIGHT_V001.md':'275e9ef559918eee32de99f3b848fbad56bf5b7f07ace8d3f63298aca058f63b',
    PUBLISHER.name:'f4cf2cea4d4d42688616ee671f66b5717a0fb554f1ea4972783d9cc1b00071b8'}
CONFIG = dict(wall_seconds=180.,sampled_process_group_rss_bytes=1073741824,
              sample_seconds=.2,terminate_grace_seconds=3.,all_cases=12,
              require_successful_case_zero_for_later_cases=True)
ENV_KEYS = ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS',
            'VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')


def sha(raw): return hashlib.sha256(raw).hexdigest()
def enc(obj): return json.dumps(obj,sort_keys=True,separators=(',',':'),allow_nan=False).encode()


def helpers():
    if Path.cwd().resolve()!=ROOT or Path(__file__).resolve()!=THIS:
        raise RuntimeError('Wrong root/script context')
    for p in (PUBLISHER,*PUBLISHER.parents):
        if p==ROOT.parent: break
        if p.is_symlink(): raise RuntimeError('Linked publisher ancestry')
    if sha(PUBLISHER.read_bytes())!=PINS[PUBLISHER.name]: raise RuntimeError('Publisher changed')
    h=runpy.run_path(str(PUBLISHER),run_name='two_current_publication_helpers')
    return h['bound'],h['publish']


def absent(bound,*paths):
    for p in paths:
        bound(p)
        if p.exists() or p.is_symlink(): raise FileExistsError('No overwrite or automatic rerun: '+str(p))


def snapshot(bound):
    files={}
    for name,expected in PINS.items():
        p=bound(J/name);got=sha(p.read_bytes())
        if got!=expected: raise RuntimeError('Pinned input changed: '+name)
        files[str(p.relative_to(ROOT))]=got
    for p in (THIS,PROTOCOL): files[str(p.relative_to(ROOT))]=sha(bound(p).read_bytes())
    python=Path(sys.executable).resolve(strict=True)
    if not python.is_file(): raise RuntimeError('Python executable unavailable')
    return dict(schema='SPHERICAL_TWO_CURRENT_CONTROLLER_INPUTS_V001',files=files,
                configuration=CONFIG,python=dict(path=str(python),sha256=sha(python.read_bytes()),version=sys.version))


def authenticate_science_freeze(bound,raw):
    f=json.loads(raw)
    expected=[dict(case_index=i,gap=R,L=L,dx=dx,cells=round(L/dx)) for i,(R,L,dx) in
              enumerate((R,L,dx) for R in (128,8192) for L in (8.,16.) for dx in (1/16,1/32,1/64))]
    if not isinstance(f,dict) or f.get('cases')!=expected or not isinstance(f.get('files'),dict):
        raise RuntimeError('Producer freeze census/schema differs')
    for name,expected_sha in f['files'].items():
        rel=Path(name)
        if rel.is_absolute() or '..' in rel.parts: raise RuntimeError('Invalid freeze member')
        p=bound(ROOT/rel)
        if not p.is_file() or sha(p.read_bytes())!=expected_sha: raise RuntimeError('Frozen member differs: '+name)
    for name in (SOURCE.name,'SPHERICAL_TWO_CURRENT_FINITE_R_DESIGN_V001.md','SPHERICAL_TWO_CURRENT_PROTOCOL_V001.md'):
        if f['files'].get(str((J/name).relative_to(ROOT)))!=PINS[name]: raise RuntimeError('Unbound producer source')
    enc(f)  # Reject nonfinite parsed values, including nonstandard JSON constants.
    return f


def invoke(argv):
    env=os.environ.copy()
    for k in ('PYTHONPATH','PYTHONHOME','PYTHONSTARTUP','PYTHONINSPECT'): env.pop(k,None)
    env.update({k:'1' for k in ENV_KEYS});env.update(PYTHONDONTWRITEBYTECODE='1',LC_ALL='C')
    start=time.monotonic();p=None;out=err=b'';exception=None;reason=None;peak=0;errors=[]
    finished=threading.Event();thread=None
    def send(sig):
        if p is not None:
            try: os.killpg(p.pid,sig)
            except ProcessLookupError: pass
    def watch():
        nonlocal reason,peak
        while not finished.wait(CONFIG['sample_seconds']):
            if p.poll() is not None: return
            try:
                q=subprocess.run(['/bin/ps','-axo','pgid=,rss='],capture_output=True,timeout=2.,check=True)
                rss=sum(int(v[1])*1024 for line in q.stdout.splitlines() if len(v:=line.split())==2 and int(v[0])==p.pid)
                peak=max(peak,rss)
                if rss>CONFIG['sampled_process_group_rss_bytes']: reason='SAMPLED_PROCESS_GROUP_RSS_LIMIT'
            except Exception:
                errors.append(traceback.format_exc());reason='RESOURCE_MONITOR_FAILED'
            if time.monotonic()-start>=CONFIG['wall_seconds']: reason=reason or 'WALL_TIME_LIMIT'
            if reason:
                send(signal.SIGTERM)
                if not finished.wait(CONFIG['terminate_grace_seconds']): send(signal.SIGKILL)
                return
    try:
        p=subprocess.Popen(argv,cwd=ROOT,env=env,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE,start_new_session=True)
        thread=threading.Thread(target=watch,daemon=True);thread.start()
        out,err=p.communicate(timeout=CONFIG['wall_seconds'])
    except BaseException as exc:
        exception=traceback.format_exc()
        if isinstance(exc,subprocess.TimeoutExpired): reason=reason or 'WALL_TIME_LIMIT'
        send(signal.SIGTERM)
        if p is not None:
            try: out,err=p.communicate(timeout=CONFIG['terminate_grace_seconds'])
            except BaseException:
                send(signal.SIGKILL);out,err=p.communicate()
    finally:
        finished.set()
        if thread: thread.join(timeout=3.)
    rec=dict(argv=argv,cwd=str(ROOT),seconds=time.monotonic()-start,returncode=None if p is None else p.returncode,
             exception=exception,stop_reason=reason,sampled_process_group_peak_rss_bytes=peak,
             resource_monitor_errors=errors,stdout_base64=base64.b64encode(out).decode(),
             stderr_base64=base64.b64encode(err).decode(),stdout_sha256=sha(out),stderr_sha256=sha(err),
             stdout_bytes=len(out),stderr_bytes=len(err))
    return rec,out


def invocation_ok(r):
    return r['returncode']==0 and r['exception'] is None and r['stop_reason'] is None and not r['resource_monitor_errors']


def save(publish,path,payload,freeze_sha=None):
    raw=enc(dict(schema='SPHERICAL_TWO_CURRENT_CUSTODY_RECEIPT_V001',freeze_sha256=freeze_sha,
                 payload_sha256=sha(enc(payload)),payload=payload))+b'\n'
    publish(raw,path)
    if path.read_bytes()!=raw: raise RuntimeError('Published receipt bytes differ')
    return sha(raw)


def paths(index):
    base='SPHERICAL_TWO_CURRENT_V001_CASE_'+format(index,'03d')
    return J/(base+'_RUN.json'),J/(base+'.json')


def validate_case(raw,index,science_sha,f):
    w=json.loads(raw);p=w['payload'];enc(p)
    if w['freeze_sha256']!=science_sha or w['payload_sha256']!=sha(enc(p)) or p['case']!=f['cases'][index]:
        raise RuntimeError('Producer freeze/payload/case binding differs')
    if not isinstance(p['status'],str) or not isinstance(p['failures'],list): raise RuntimeError('Invalid producer status')
    complete=p['status']=='COMPLETE_FINITE_R_NUMERICAL_CASE' and not p['failures']
    return p,complete


def benchmark_gate(bound,freeze_sha,science_sha,f):
    receipt,rawpath=paths(0);w=json.loads(bound(receipt).read_bytes());p=w['payload']
    if w['freeze_sha256']!=freeze_sha or w['payload_sha256']!=sha(enc(p)) or p['status']!='CASE_COMPLETE':
        raise RuntimeError('Successful case-zero resource/science benchmark required')
    raw=bound(rawpath).read_bytes();_,complete=validate_case(raw,0,science_sha,f)
    if not complete or p['case_index']!=0 or p['invocation']['stdout_sha256']!=sha(raw) or not invocation_ok(p['invocation']):
        raise RuntimeError('Case-zero benchmark receipt/raw differs')


def main():
    bound,publish=helpers();s=snapshot(bound);args=sys.argv[1:]
    if args==['freeze']:
        absent(bound,FREEZE_INTENT,FREEZE_RUN,SCIENCE_FREEZE,FREEZE)
        argv=[s['python']['path'],'-B',str(SOURCE),'freeze']
        save(publish,FREEZE_INTENT,dict(status='INTENT_NO_RETRY',controller_inputs=s,argv=argv))
        r,raw=invoke(argv);error=None
        try:
            if not invocation_ok(r): raise RuntimeError('Custody-only freeze invocation failed')
            authenticate_science_freeze(bound,raw)
            if snapshot(bound)!=s: raise RuntimeError('Controller inputs changed during freeze')
        except BaseException: error=traceback.format_exc()
        p=dict(status='FREEZE_CAPTURE_COMPLETE' if error is None else 'FREEZE_FAILED_RETAINED',
               controller_inputs=s,invocation=r,validation_error=error)
        receipt_sha=save(publish,FREEZE_RUN,p)
        if error is None:
            publish(raw,SCIENCE_FREEZE)
            frozen=dict(controller_inputs=s,producer_freeze_sha256=sha(raw),freeze_invocation_receipt_sha256=receipt_sha)
            publish(enc(frozen)+b'\n',FREEZE)
        print(enc(dict(status=p['status'],receipt=str(FREEZE_RUN),sha256=receipt_sha,
                       producer_freeze_sha256=sha(raw) if error is None else None)).decode(),flush=True)
        return 0 if error is None else 2
    if len(args)!=2 or args[0]!='run-case' or not args[1].isdigit() or not 0<=int(args[1])<12:
        raise RuntimeError('Use freeze or run-case INDEX (0..11)')
    index=int(args[1]);fraw=bound(FREEZE).read_bytes();frozen=json.loads(fraw);freeze_sha=sha(fraw)
    if frozen['controller_inputs']!=s: raise RuntimeError('Controller freeze changed')
    fr=bound(FREEZE_RUN).read_bytes()
    if sha(fr)!=frozen['freeze_invocation_receipt_sha256']: raise RuntimeError('Freeze invocation receipt changed')
    rawfreeze=bound(SCIENCE_FREEZE).read_bytes();science_sha=sha(rawfreeze)
    if science_sha!=frozen['producer_freeze_sha256']: raise RuntimeError('Producer freeze changed')
    f=authenticate_science_freeze(bound,rawfreeze)
    receipt,rawpath=paths(index);intent=receipt.with_name(receipt.name.replace('_RUN.json','_INTENT.json'))
    absent(bound,intent,receipt,rawpath)
    if index: benchmark_gate(bound,freeze_sha,science_sha,f)
    argv=[s['python']['path'],'-B',str(SOURCE),'run-case',str(index)]
    save(publish,intent,dict(status='INTENT_NO_RETRY',case_index=index,case=f['cases'][index],
                            producer_freeze_sha256=science_sha,argv=argv),freeze_sha)
    r,raw=invoke(argv)
    error=None;science=None;complete=False
    try:
        science,complete=validate_case(raw,index,science_sha,f)
        authenticate_science_freeze(bound,rawfreeze)
        if snapshot(bound)!=s or bound(SCIENCE_FREEZE).read_bytes()!=rawfreeze or bound(FREEZE).read_bytes()!=fraw:
            raise RuntimeError('Inputs changed during invocation')
    except BaseException: error=traceback.format_exc();complete=False
    okay=complete and error is None and invocation_ok(r)
    payload=dict(status='CASE_COMPLETE' if okay else 'CASE_FAILED_RETAINED',case_index=index,case=f['cases'][index],
                 producer_freeze_sha256=science_sha,invocation=r,validation_error=error,
                 scientific_status=None if science is None else science['status'],
                 scientific_failures=None if science is None else science['failures'],
                 scientific_raw_output_qualified=error is None,raw_output_path=str(rawpath) if error is None else None)
    receipt_sha=save(publish,receipt,payload,freeze_sha)
    if error is None: publish(raw,rawpath)  # Valid failed science is retained too.
    print(enc(dict(status=payload['status'],case_index=index,receipt=str(receipt),receipt_sha256=receipt_sha,
                   raw_path=payload['raw_output_path'],raw_sha256=sha(raw),seconds=r['seconds'],
                   sampled_process_group_peak_rss_bytes=r['sampled_process_group_peak_rss_bytes'],
                   stop_reason=r['stop_reason'],scientific_status=payload['scientific_status'])).decode(),flush=True)
    return 0 if okay else 2


if __name__=='__main__': sys.exit(main())
