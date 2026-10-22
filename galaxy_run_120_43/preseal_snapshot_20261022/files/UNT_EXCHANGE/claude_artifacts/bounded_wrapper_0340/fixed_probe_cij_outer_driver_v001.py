"""INERT outer driver for the fixed-probe census wrapper V003 (task 0340). Root runs it once, after review; no retry loop.

Measures the WHOLE wrapper subprocess from start to exit with time.monotonic (timeout 10 s) and writes ONE exclusive
outer receipt. Acceptance (status COMPLETED_WITHIN_ENVELOPE) requires ALL of:
  wrapper exit 0; no timeout or kill; outer elapsed <= 10 s;
  the wrapper's TERMINAL receipt exists, parses, has status COMPLETED_WITHIN_ENVELOPE and all terminal predicates true;
  the primary receipt's bytes match the pin recorded in the terminal receipt;
  driver self peak + wrapper conservative combined peak <= 256 MiB;
  wrapper total-created upper bound + driver capture files + OUTER_MAX <= 32 MiB.
On timeout: wrapper descendants (and their process groups) are snapshotted with /bin/ps BEFORE the wrapper is signalled.
The driver sends SIGTERM to the wrapper (V003 then kills the scientific child group), waits <= 1 s, then SIGKILLs the
wrapper group and every snapshotted descendant group, so no detached work remains.
Tail scope: only this outer receipt's construction and write (<= OUTER_MAX bytes) follow the final measurement.
"""
from pathlib import Path
import datetime,hashlib,json,os,resource,signal,subprocess,sys,time
R=Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL')
C=R/'FIRST_CONSTRUCTION_REVIEW_2026-10-13'/'CODEX1'
WRAPPER=(C/'readiness_fixed_probe_cij_root_launch_wrapper_v003.py','c3fc987a35cb045bbc9ea73082e512f302040627e7d24a80ca3b71832344cdfd')
PREFIX='READINESS_FIXED_PROBE_CIJ_L4_L6'
PRIMARY=C/(PREFIX+'_ROOT_RECEIPT_V002.json');TERMINAL=C/(PREFIX+'_ROOT_TERMINAL_RECEIPT_V002.json')
OUT_STDOUT=C/(PREFIX+'_OUTER_DRIVER_STDOUT_V001.txt');OUT_STDERR=C/(PREFIX+'_OUTER_DRIVER_STDERR_V001.txt');OUTER=C/(PREFIX+'_OUTER_RECEIPT_V001.json')
WALL=10;MEMORY=256*1024*1024;OUTPUT=32*1024*1024;OUTER_MAX=64*1024;GRACE=1.0;PS='/bin/ps'
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for c in iter(lambda:f.read(1024*1024),b''):h.update(c)
 return h.hexdigest()
def peak():
 n=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
 return n if sys.platform=='darwin' else n*1024
def descendants(root_pid):
 out=subprocess.run([PS,'-A','-o','pid=,ppid=,pgid='],capture_output=True,text=True,timeout=1,check=True).stdout
 rows=[tuple(int(x) for x in l.split()) for l in out.splitlines() if l.strip()]
 kids={root_pid};changed=True
 while changed:
  changed=False
  for pid,ppid,pg in rows:
   if ppid in kids and pid not in kids:kids.add(pid);changed=True
 return sorted({pg for pid,ppid,pg in rows if pid in kids})
def main():
 if len(sys.argv)!=3:raise SystemExit('usage: outer_driver <review_path> <review_sha256>')
 if not __debug__:raise SystemExit('Python optimization prohibited')
 if sha(WRAPPER[0])!=WRAPPER[1]:raise SystemExit('Wrapper pin changed')
 for p in [OUT_STDOUT,OUT_STDERR,OUTER,PRIMARY,TERMINAL]:
  if p.exists():raise SystemExit('Immutable path already exists: '+str(p))
 env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None)
 cmd=[sys.executable,'-B',str(WRAPPER[0]),sys.argv[1],sys.argv[2]]
 rec={'kind':'OUTER_DRIVER_RECEIPT','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command':cmd,'wrapper_pin':{'path':str(WRAPPER[0]),'sha256':WRAPPER[1]},'driver_pin':{'path':str(Path(__file__)),'sha256':sha(Path(__file__))},'wall_cap_seconds':WALL,'memory_cap_bytes':MEMORY,'output_cap_bytes':OUTPUT,'outer_receipt_max_bytes':OUTER_MAX,'timeout':False,'killed_groups':[],'retry':'none'}
 start=time.monotonic();proc=None
 try:
  with OUT_STDOUT.open('x') as o,OUT_STDERR.open('x') as e:
   proc=subprocess.Popen(cmd,stdin=subprocess.DEVNULL,stdout=o,stderr=e,start_new_session=True,env=env)
   try:proc.wait(timeout=WALL)
   except subprocess.TimeoutExpired:
    rec['timeout']=True
    try:groups=descendants(proc.pid)
    except BaseException as exc:groups=[proc.pid];rec['descendant_scan_error']=type(exc).__name__
    try:os.kill(proc.pid,signal.SIGTERM)
    except ProcessLookupError:pass
    try:proc.wait(timeout=GRACE)
    except subprocess.TimeoutExpired:pass
    for g in set(groups)|{proc.pid}:
     try:os.killpg(g,signal.SIGKILL);rec['killed_groups'].append(g)
     except (ProcessLookupError,PermissionError):pass
    proc.wait(timeout=2)
 except BaseException as exc:
  rec['driver_error']={'type':type(exc).__name__,'message':str(exc)[:300]}
 elapsed=time.monotonic()-start
 rec['outer_elapsed_seconds']=elapsed;rec['wrapper_exit_code']=None if proc is None else proc.returncode
 term=None;prim_ok=False
 try:
  term=json.loads(TERMINAL.read_text()) if TERMINAL.exists() else None
  pp=(term or {}).get('primary_receipt') or {}
  prim_ok=bool(pp) and PRIMARY.exists() and sha(PRIMARY)==pp.get('sha256')
 except BaseException as exc:rec['terminal_read_error']=type(exc).__name__
 rec['terminal_status']=(term or {}).get('status');rec['terminal_predicates']=(term or {}).get('terminal_predicates')
 drv=peak();inner=(term or {}).get('postwrite_conservative_combined_peak_bytes')
 cap_files=sum(p.stat().st_size for p in [OUT_STDOUT,OUT_STDERR] if p.exists())
 inner_bytes=(term or {}).get('total_created_bytes_upper_bound')
 rec.update({'driver_peak_rss_bytes':drv,'inner_conservative_peak_bytes':inner,'driver_capture_bytes':cap_files,'inner_total_created_upper_bound':inner_bytes})
 checks={'no_driver_error':'driver_error' not in rec,'no_timeout':not rec['timeout'],'wrapper_exit_zero':rec['wrapper_exit_code']==0,'outer_elapsed_within_cap':elapsed<=WALL,
  'terminal_completed':rec['terminal_status']=='COMPLETED_WITHIN_ENVELOPE','terminal_predicates_all_true':bool(rec['terminal_predicates']) and all(rec['terminal_predicates'].values()),
  'primary_pin_matches':prim_ok,'memory_within_cap':inner is not None and drv+inner<=MEMORY,'output_within_cap':inner_bytes is not None and inner_bytes+cap_files+OUTER_MAX<=OUTPUT}
 rec['outer_predicates']=checks;rec['status']='COMPLETED_WITHIN_ENVELOPE' if all(checks.values()) else 'FAILED_OR_INCOMPLETE'
 rec['tail_scope']='This receipt construction/write (<= outer_receipt_max_bytes) follows the final measurement; bounded in bytes, not wall time.'
 b=(json.dumps(rec,indent=2,allow_nan=False)+'\n').encode()
 if len(b)>OUTER_MAX:
  rec={'kind':'OUTER_DRIVER_RECEIPT','status':'FAILED_OR_INCOMPLETE','reason':'OUTER_RECEIPT_OVERSIZE','outer_elapsed_seconds':elapsed};b=(json.dumps(rec,indent=2)+'\n').encode()
 with OUTER.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
 print(json.dumps({'outer_receipt':str(OUTER),'status':rec['status'],'outer_elapsed_seconds':elapsed}))
 sys.exit(0 if rec['status']=='COMPLETED_WITHIN_ENVELOPE' else 1)
if __name__=='__main__':main()
