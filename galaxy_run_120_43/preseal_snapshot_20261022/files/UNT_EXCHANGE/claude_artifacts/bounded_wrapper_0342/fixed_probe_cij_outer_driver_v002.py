"""INERT outer driver V002 for the fixed-probe census wrapper V004 (tasks 0342/0343). Root runs it once, after review; no retry.

V002 changes vs V001 (custody only; science, caps, one attempt and unused result paths unchanged):
  - The wrapper is launched with start_new_session=True, so its PID is the KNOWN process group. Wrapper V004 keeps its
    one scientific producer and its /bin/ps monitor calls in that same group. No descendant scan, no PID handoff.
  - ONE cleanup routine runs after Popen on EVERY path: wrapper exit, timeout, and any exception (including
    KeyboardInterrupt, SystemExit and SIGTERM, which the driver converts to SystemExit). It SIGKILLs the known group
    even if the wrapper leader has already exited (a producer may remain in it), reaps the wrapper, then confirms the
    group is gone with killpg(pgid, 0) -> ProcessLookupError within GRACE. Kill/wait/permission/verification errors are
    recorded; cleanup is 'confirmed' only when the wrapper is reaped AND the group is verified gone. Unconfirmed cleanup
    fails the receipt and sets 'root_attention_required'.
  - SIGINT, SIGTERM and SIGHUP handlers NEVER raise: they only record the signal. The main path polls the wrapper in
    50 ms waits and, on a recorded signal, takes the same single cleanup path (trigger SIGNAL, recorded as a driver
    error). No signal can interrupt Popen's handle handoff, an except clause, or cleanup itself. A signal recorded
    before Popen prevents the launch. Residual: SIGKILL of the driver cannot be handled; the wrapper's own 10 s wall cap
    then still stops the producer, and the missing outer receipt is itself a failed launch.
  - 'wrapper_lifetime_seconds' (renamed from outer_elapsed_seconds) runs from just before Popen until the wrapper is
    observed exited (wait return, or reap inside cleanup). Cleanup verification, terminal-receipt reading/hashing and
    this receipt's construction and write follow that timestamp; it is NOT the total driver lifetime.

Acceptance (status COMPLETED_WITHIN_ENVELOPE) requires ALL of: no driver error; no timeout; wrapper exit 0;
wrapper lifetime <= 10 s; process-group cleanup confirmed; wrapper TERMINAL receipt COMPLETED with all predicates true;
primary pin matching; driver peak + inner conservative peak <= 256 MiB; inner total-created bound + driver capture
files + OUTER_MAX <= 32 MiB.
"""
from pathlib import Path
import datetime,hashlib,json,os,resource,signal,subprocess,sys,time
R=Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL')
C=R/'FIRST_CONSTRUCTION_REVIEW_2026-10-13'/'CODEX1'
WRAPPER=(C/'readiness_fixed_probe_cij_root_launch_wrapper_v004.py','0008c65a765771e70fa6acd6c30ccce880bcb722ecf3b18a02284d293591c370')
PREFIX='READINESS_FIXED_PROBE_CIJ_L4_L6'
PRIMARY=C/(PREFIX+'_ROOT_RECEIPT_V002.json');TERMINAL=C/(PREFIX+'_ROOT_TERMINAL_RECEIPT_V002.json')
OUT_STDOUT=C/(PREFIX+'_OUTER_DRIVER_STDOUT_V001.txt');OUT_STDERR=C/(PREFIX+'_OUTER_DRIVER_STDERR_V001.txt');OUTER=C/(PREFIX+'_OUTER_RECEIPT_V001.json')
WALL=10;MEMORY=256*1024*1024;OUTPUT=32*1024*1024;OUTER_MAX=64*1024;GRACE=1.0
SIG={'pending':None}
def _on_signal(signum,frame):
 SIG['pending']=SIG['pending'] or signum  # never raises; the main path polls this and runs the single cleanup
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for c in iter(lambda:f.read(1024*1024),b''):h.update(c)
 return h.hexdigest()
def peak():
 n=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
 return n if sys.platform=='darwin' else n*1024
def err(exc):return {'type':type(exc).__name__,'message':str(exc)[:200]}
def cleanup(proc,trigger,start):
 """Single cleanup path. Never raises; every failure is recorded and leaves 'confirmed' False."""
 c={'trigger':trigger,'process_group':proc.pid,'wrapper_already_exited':proc.returncode is not None,'kill_sent':False,'group_absent_at_kill':False,'errors':[]}
 try:os.killpg(proc.pid,signal.SIGKILL);c['kill_sent']=True
 except ProcessLookupError:c['group_absent_at_kill']=True
 except BaseException as exc:c['errors'].append({'step':'killpg_SIGKILL',**err(exc)})
 try:proc.wait(timeout=GRACE)
 except BaseException as exc:c['errors'].append({'step':'wait_wrapper',**err(exc)})
 c['wrapper_reaped']=proc.returncode is not None;c['wrapper_returncode']=proc.returncode
 c['observed_exit_seconds']=time.monotonic()-start
 c['group_gone']=False;deadline=time.monotonic()+GRACE
 while True:
  try:os.killpg(proc.pid,0)
  except ProcessLookupError:c['group_gone']=True;break
  except BaseException as exc:c['errors'].append({'step':'verify_group',**err(exc)});break
  if time.monotonic()>=deadline:c['errors'].append({'step':'verify_group','type':'GroupStillPresent','message':'process group still present after grace'});break
  time.sleep(.02)
 c['confirmed']=c['wrapper_reaped'] and c['group_gone']
 return c
def main():
 if len(sys.argv)!=3:raise SystemExit('usage: outer_driver <review_path> <review_sha256>')
 if not __debug__:raise SystemExit('Python optimization prohibited')
 if sha(WRAPPER[0])!=WRAPPER[1]:raise SystemExit('Wrapper pin changed')
 for p in [OUT_STDOUT,OUT_STDERR,OUTER,PRIMARY,TERMINAL]:
  if p.exists():raise SystemExit('Immutable path already exists: '+str(p))
 for s in (signal.SIGINT,signal.SIGTERM,signal.SIGHUP):signal.signal(s,_on_signal)
 env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None)
 cmd=[sys.executable,'-B',str(WRAPPER[0]),sys.argv[1],sys.argv[2]]
 rec={'kind':'OUTER_DRIVER_RECEIPT','driver_version':'V002','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command':cmd,'wrapper_pin':{'path':str(WRAPPER[0]),'sha256':WRAPPER[1]},'driver_pin':{'path':str(Path(__file__)),'sha256':sha(Path(__file__))},'wall_cap_seconds':WALL,'memory_cap_bytes':MEMORY,'output_cap_bytes':OUTPUT,'outer_receipt_max_bytes':OUTER_MAX,'grace_seconds':GRACE,'timeout':False,'retry':'none'}
 proc=None;trigger='WRAPPER_EXIT';lifetime=None;o=e=None
 start=time.monotonic()
 try:
  o=OUT_STDOUT.open('x');e=OUT_STDERR.open('x')
  if SIG['pending'] is None:proc=subprocess.Popen(cmd,stdin=subprocess.DEVNULL,stdout=o,stderr=e,start_new_session=True,env=env)
  while proc is not None and SIG['pending'] is None:
   try:proc.wait(timeout=.05);lifetime=time.monotonic()-start;break
   except subprocess.TimeoutExpired:
    if time.monotonic()-start>=WALL:rec['timeout']=True;trigger='TIMEOUT';break
 except BaseException as exc:
  rec['driver_error']=err(exc);trigger='DRIVER_EXCEPTION'
 if SIG['pending'] is not None and lifetime is None and trigger=='WRAPPER_EXIT':
  trigger='SIGNAL';rec['driver_error']={'type':'Signal','message':'signal '+str(SIG['pending'])+' received before wrapper exit'}
 if proc is not None:
  rec['cleanup']=cleanup(proc,trigger,start)
  if lifetime is None and rec['cleanup']['wrapper_reaped']:lifetime=rec['cleanup']['observed_exit_seconds']
 else:
  rec['cleanup']={'trigger':trigger,'confirmed':True,'note':'no wrapper process was created'}
 for f in (o,e):
  try:
   if f is not None:f.close()
  except BaseException as exc:rec.setdefault('capture_close_errors',[]).append(err(exc))
 if SIG['pending'] is not None:rec['signal_received']=SIG['pending']
 rec['wrapper_lifetime_seconds']=lifetime;rec['wrapper_exit_code']=None if proc is None else proc.returncode
 rec['root_attention_required']=not rec['cleanup']['confirmed']
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
 checks={'no_driver_error':'driver_error' not in rec,'no_timeout':not rec['timeout'],'wrapper_exit_zero':rec['wrapper_exit_code']==0,'wrapper_lifetime_within_cap':lifetime is not None and lifetime<=WALL,
  'process_group_cleanup_confirmed':rec['cleanup']['confirmed'] is True,
  'terminal_completed':rec['terminal_status']=='COMPLETED_WITHIN_ENVELOPE','terminal_predicates_all_true':bool(rec['terminal_predicates']) and all(rec['terminal_predicates'].values()),
  'primary_pin_matches':prim_ok,'memory_within_cap':inner is not None and drv+inner<=MEMORY,'output_within_cap':inner_bytes is not None and inner_bytes+cap_files+OUTER_MAX<=OUTPUT}
 rec['outer_predicates']=checks;rec['status']='COMPLETED_WITHIN_ENVELOPE' if all(checks.values()) else 'FAILED_OR_INCOMPLETE'
 rec['tail_scope']='wrapper_lifetime_seconds ends when the wrapper is observed exited. Group verification, terminal-receipt reading/hashing and this receipt construction/write (<= outer_receipt_max_bytes) follow it: not total driver lifetime; tail bounded in bytes, not wall time.'
 b=(json.dumps(rec,indent=2,allow_nan=False)+'\n').encode()
 if len(b)>OUTER_MAX:
  rec={'kind':'OUTER_DRIVER_RECEIPT','driver_version':'V002','status':'FAILED_OR_INCOMPLETE','reason':'OUTER_RECEIPT_OVERSIZE','wrapper_lifetime_seconds':lifetime,'cleanup_confirmed':rec['cleanup']['confirmed'],'root_attention_required':rec['root_attention_required']};b=(json.dumps(rec,indent=2)+'\n').encode()
 with OUTER.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
 print(json.dumps({'outer_receipt':str(OUTER),'status':rec['status'],'wrapper_lifetime_seconds':lifetime,'cleanup_confirmed':rec.get('cleanup',{}).get('confirmed',rec.get('cleanup_confirmed')),'root_attention_required':rec['root_attention_required']}))
 sys.exit(0 if rec['status']=='COMPLETED_WITHIN_ENVELOPE' else 1)
if __name__=='__main__':main()
