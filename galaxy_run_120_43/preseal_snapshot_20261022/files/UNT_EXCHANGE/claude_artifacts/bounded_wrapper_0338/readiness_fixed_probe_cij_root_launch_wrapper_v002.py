"""Root-only one-shot exact census wrapper V002 (custody-accounting repair of V001). Scientific execution only after review.

Receipt hierarchy (V002):
  1. PRIMARY receipt (_ROOT_RECEIPT_V001.json): written once, exclusively. It holds every pin, sample and
     predicate, with status PROVISIONAL_<verdict>. It is NEVER the acceptance record.
  2. TERMINAL receipt (_ROOT_TERMINAL_RECEIPT_V001.json): small, exclusive, written last. It pins the primary
     receipt and records wall and peak-RSS measurements taken AFTER the primary receipt was written. Its
     'status' is the AUTHORITATIVE acceptance record.
  A missing terminal receipt, a missing primary receipt, or any accounting exception means FAILED_OR_INCOMPLETE.
  Both files are preserved if interrupted. Only the terminal receipt's own final write is outside measurement;
  its size is bounded by TERMINAL_MAX and reserved inside the output cap.
"""
from pathlib import Path
import datetime,hashlib,json,os,resource,signal,subprocess,sys,time
R=Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL')
B=R/'FIRST_CONSTRUCTION_REVIEW_2026-10-13';C=B/'CODEX1';HC=B/'helpers/coefficient_method'
PRODUCER=HC/'owned_loop_merger_fixed_probe_cij_census_v002.py'
PINS=[(PRODUCER,'ff22b23115f25e05b9079f74653aa2e3c37f76e135ca700ecd74694d4ff2ad75'),(HC/'OWNED_LOOP_MERGER_FIXED_PROBE_CIJ_CENSUS_PROSPECT_V001.md','9cc08d8f558c92993bca1b3dd75399f44061a8bb5a998a62e0c30b524dbbeb08'),(HC/'OWNED_LOOP_MERGER_CIJ_V002_CUSTODY_ADDENDUM_V001.md','40d1195d0bb3845a87bf334d8f25e31aa0d4131b89e605d315452484d8a16c83')]
WALL=10;MEMORY=256*1024*1024;OUTPUT=32*1024*1024
RECEIPT_RESERVE=1024*1024;TERMINAL_MAX=64*1024  # primary+terminal receipts are reserved inside OUTPUT
PRODUCER_OUTPUT_CAP=OUTPUT-RECEIPT_RESERVE
PREFIX='READINESS_FIXED_PROBE_CIJ_L4_L6'
output=C/(PREFIX+'_OUTPUT_V001.json');stdout=C/(PREFIX+'_STDOUT_V001.jsonl');stderr=C/(PREFIX+'_STDERR_V001.txt');receipt=C/(PREFIX+'_ROOT_RECEIPT_V001.json')
terminal=C/(PREFIX+'_ROOT_TERMINAL_RECEIPT_V001.json')
def pin(p):
 h=hashlib.sha256();n=0
 with p.open('rb') as f:
  for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk);n+=len(chunk)
 return {'path':str(p),'sha256':h.hexdigest(),'bytes':n}
def peak(who):
 n=resource.getrusage(who).ru_maxrss
 return n if sys.platform=='darwin' else n*1024
if len(sys.argv)!=3:raise RuntimeError('Need distinct prelaunch review path and exact hash')
if not __debug__:raise RuntimeError('Python optimization prohibited')
review=Path(sys.argv[1]);review_sha=sys.argv[2]
for p,h in PINS+[(review,review_sha)]:
 if pin(p)['sha256']!=h:raise RuntimeError('Input pin changed: '+str(p))
for p in [output,stdout,stderr,receipt,terminal]:
 if p.exists():raise RuntimeError('Immutable output already exists: '+str(p))
env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None)
cmd=[sys.executable,'-B',str(PRODUCER),'--output',str(output)]
record={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'wrapper_version':'V002','root_authorized_bounded_launch':True,'scientific_child_processes':1,'command':cmd,'inputs':[pin(p) for p,h in PINS+[(review,review_sha)]],'wrapper':pin(Path(__file__)),'wall_cap_seconds':WALL,'combined_resident_cap_bytes':MEMORY,'output_cap_bytes':OUTPUT,'receipt_reserve_bytes':RECEIPT_RESERVE,'producer_output_cap_bytes':PRODUCER_OUTPUT_CAP,'terminal_receipt_max_bytes':TERMINAL_MAX,'memory_enforcement':'Periodic combined RSS sampling and conservative postrun sum of wrapper/child peak RSS; not a kernel-enforced instantaneous RSS claim.','receipt_hierarchy':'PRIMARY receipt is provisional; TERMINAL receipt status is authoritative; missing terminal receipt = FAILED_OR_INCOMPLETE.','authoritative_record':str(terminal),'samples':[],'status':'STARTING'}
child=None;reason=None;start=time.monotonic()
def stop_child():
 if child is not None and child.poll() is None:
  try:os.killpg(child.pid,signal.SIGKILL)
  except ProcessLookupError:pass
  child.wait(timeout=1)
def output_size():return sum(p.stat().st_size for p in [output,stdout,stderr] if p.exists())
try:
 with stdout.open('x') as out,stderr.open('x') as err:
  child=subprocess.Popen(cmd,stdin=subprocess.DEVNULL,stdout=out,stderr=err,start_new_session=True,env=env)
  while child.poll() is None:
   elapsed=time.monotonic()-start
   if elapsed>=WALL:reason='WALL_CAP';stop_child();break
   if output_size()>PRODUCER_OUTPUT_CAP:reason='OUTPUT_CAP';stop_child();break
   ps=subprocess.run(['/bin/ps','-o','rss=','-p',str(os.getpid())+','+str(child.pid)],capture_output=True,text=True,timeout=min(.25,max(.001,WALL-elapsed)),check=True)
   rss=sum(int(x)*1024 for x in ps.stdout.split())
   record['samples'].append({'elapsed_seconds':time.monotonic()-start,'combined_rss_bytes':rss})
   if rss>MEMORY:reason='MEMORY_CAP';stop_child();break
   time.sleep(min(.02,max(0,WALL-(time.monotonic()-start))))
  child.wait(timeout=1)
 record['exit_code']=child.returncode
 if child.returncode==0 and reason is None and output.is_file() and output_size()<=PRODUCER_OUTPUT_CAP:
  data=json.loads(output.read_text())
  record['scientific_status']=data.get('status')
  record['completed_sizes']=[q.get('L') for q in data.get('cases',[]) if q.get('status')=='PASS_SCOPED']
  record['completed_arm_count']=sum(a.get('status')=='PASS_SCOPED' for q in data.get('cases',[]) for a in q.get('arms',{}).values())
  record['producer_errors']=data.get('errors')
  record['stdout_terminal_present']=any('"event": "TERMINAL"' in line and 'PASS_SCOPED' in line for line in stdout.read_text().splitlines())
  del data
except BaseException as exc:
 record['wrapper_error']={'type':type(exc).__name__,'message':str(exc)};reason=reason or 'WRAPPER_ERROR';stop_child()
primary_pin=None;primary_bytes_len=None
try:
 # Phase A: all substantial custody work (streaming output hashes, stderr check) BEFORE the final measurement.
 record['stop_reason']=reason
 record['outputs']=[pin(p) for p in [output,stdout,stderr] if p.exists()]
 record['output_bytes']=output_size();record['stderr_empty']=stderr.exists() and stderr.stat().st_size==0
 # Phase B: pre-receipt measurement, provisional verdict, primary receipt serialized in memory, then written exclusively.
 record['wall_seconds']=time.monotonic()-start
 record['wrapper_peak_rss_bytes']=peak(resource.RUSAGE_SELF);record['child_peak_rss_bytes']=peak(resource.RUSAGE_CHILDREN)
 record['conservative_combined_peak_bytes']=record['wrapper_peak_rss_bytes']+record['child_peak_rss_bytes']
 checks={'exit_zero':record.get('exit_code')==0,'no_stop_reason':reason is None,'no_wrapper_error':'wrapper_error' not in record,'wall_within_cap':record['wall_seconds']<=WALL,'memory_within_cap':record['conservative_combined_peak_bytes']<=MEMORY,'output_within_cap':record['output_bytes']<=PRODUCER_OUTPUT_CAP,'stderr_empty':record['stderr_empty'],'producer_pass':record.get('scientific_status')=='PASS_SCOPED','complete_sizes':record.get('completed_sizes')==[4,6],'complete_arms':record.get('completed_arm_count')==4,'no_producer_errors':record.get('producer_errors')==[],'terminal_present':record.get('stdout_terminal_present') is True}
 record['acceptance_predicates']=checks
 provisional='COMPLETED_WITHIN_ENVELOPE' if all(checks.values()) else 'FAILED_OR_INCOMPLETE'
 record['status']='PROVISIONAL_'+provisional
 primary_bytes=(json.dumps(record,indent=2,allow_nan=False)+'\n').encode()
 primary_bytes_len=len(primary_bytes)
 if primary_bytes_len+TERMINAL_MAX>RECEIPT_RESERVE:raise RuntimeError('Primary receipt exceeds reserved receipt budget')
 with receipt.open('xb') as f:f.write(primary_bytes);f.flush();os.fsync(f.fileno())
 primary_pin={'path':str(receipt),'sha256':hashlib.sha256(primary_bytes).hexdigest(),'bytes':primary_bytes_len}
except BaseException as exc:
 record['accounting_error']={'type':type(exc).__name__,'message':str(exc)}
# Phase C: post-receipt-write measurement; small exclusive TERMINAL receipt is the authoritative record.
post_wall=time.monotonic()-start
post_self=peak(resource.RUSAGE_SELF);post_child=peak(resource.RUSAGE_CHILDREN)
total_created=(record.get('output_bytes') or output_size())+(primary_bytes_len or 0)+TERMINAL_MAX
term_checks={'primary_receipt_written':primary_pin is not None,'no_accounting_error':'accounting_error' not in record,'provisional_pass':record.get('status')=='PROVISIONAL_COMPLETED_WITHIN_ENVELOPE','postwrite_wall_within_cap':post_wall<=WALL,'postwrite_memory_within_cap':post_self+post_child<=MEMORY,'total_created_bytes_within_output_cap':total_created<=OUTPUT}
terminal_record={'kind':'AUTHORITATIVE_TERMINAL_RECEIPT','wrapper_version':'V002','primary_receipt':primary_pin,'accounting_error':record.get('accounting_error'),'postwrite_wall_seconds':post_wall,'postwrite_wrapper_peak_rss_bytes':post_self,'postwrite_child_peak_rss_bytes':post_child,'postwrite_conservative_combined_peak_bytes':post_self+post_child,'total_created_bytes_upper_bound':total_created,'terminal_predicates':term_checks,'status':'COMPLETED_WITHIN_ENVELOPE' if all(term_checks.values()) else 'FAILED_OR_INCOMPLETE','note':'Only this receipt write itself is unmeasured; its size is capped by terminal_receipt_max_bytes and reserved within the output cap.'}
terminal_bytes=(json.dumps(terminal_record,indent=2,allow_nan=False)+'\n').encode()
if len(terminal_bytes)>TERMINAL_MAX:
 terminal_record={'kind':'AUTHORITATIVE_TERMINAL_RECEIPT','wrapper_version':'V002','status':'FAILED_OR_INCOMPLETE','reason':'TERMINAL_RECEIPT_OVERSIZE','primary_receipt':primary_pin}
 terminal_bytes=(json.dumps(terminal_record,indent=2,allow_nan=False)+'\n').encode()
with terminal.open('xb') as f:f.write(terminal_bytes);f.flush();os.fsync(f.fileno())
print(json.dumps({'terminal_receipt':pin(terminal),'primary_receipt':primary_pin,'status':terminal_record['status'],'postwrite_wall_seconds':terminal_record.get('postwrite_wall_seconds'),'postwrite_combined_peak_bytes':terminal_record.get('postwrite_conservative_combined_peak_bytes'),'acceptance_predicates':record.get('acceptance_predicates'),'terminal_predicates':terminal_record.get('terminal_predicates')},indent=2))
sys.exit(0 if terminal_record['status']=='COMPLETED_WITHIN_ENVELOPE' else 1)
