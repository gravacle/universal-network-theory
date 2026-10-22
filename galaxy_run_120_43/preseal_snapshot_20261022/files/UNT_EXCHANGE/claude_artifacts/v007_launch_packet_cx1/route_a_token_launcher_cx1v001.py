"""Root-only post-seal launcher. Imported tests never spawn. Max3 route-A tokens, detached monitors.
PLAN --seal PATH --seal-sha SHA --execute-root-only [--worker]. No retries or resumes.
"""
import argparse,hashlib,json,os,signal,subprocess,sys,time
from pathlib import Path
HERE=Path(__file__).parent

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def ra_finished(path):
 p=Path(path)
 if not p.exists():return False
 data=p.read_bytes().splitlines(keepends=True)
 for line in data:
  if not line.endswith(b'\n'):continue # partial writer line never releases token
  row=json.loads(line)
  if row.get('stage')=='route_a' and row.get('event')=='finished':return True
 return False

def available(active):return max(0,3-sum(not x['route_a_finished'] for x in active))
def verify_pin(ref):
 if sha(ref['path'])!=ref['sha256']:raise ValueError('INPUT_PIN_MISMATCH '+ref['path'])
def validate(plan):
 for key in ('driver','monitor','launcher','guard'):verify_pin(plan[key])
 if plan['launcher']['path']!=str(Path(__file__).resolve()):raise ValueError('WRONG_LAUNCHER')
 if len(plan['calls'])!=10 or len({x['case'] for x in plan['calls']})!=10:raise ValueError('TEN_DISTINCT_CASES_REQUIRED')
 for x in plan['calls']:
  verify_pin(x['spec'])
  for p in (x['outdir'],x['receipt'],x['receipt']+'.launch.json',x['monitor_log']):
   if os.path.lexists(p):raise ValueError('EXISTING_OUTPUT '+p)

def worker(plan):
 pending=list(plan['calls']);active=[];completed=[];blocked=[]
 while pending or active:
  for x in list(active):
   try:x['route_a_finished']=ra_finished(Path(x['outdir'])/'progress.jsonl')
   except Exception as e:blocked.append('PROGRESS_DEFECT '+x['case']+': '+str(e))
   rc=x['proc'].poll()
   if rc is not None:
    rp=Path(x['receipt'])
    rec=json.loads(rp.read_bytes()) if rp.exists() else {}
    good=rc==0 and rec.get('status')=='FINISHED' and x['route_a_finished']
    if not good:blocked.append('CALL_FAILED_OR_MISSING_ROUTE_A_FINISH '+x['case'])
    completed.append({'case':x['case'],'monitor_exit':rc,'receipt_status':rec.get('status'),'passed':good});active.remove(x)
  if blocked:pending=[] # no new starts; existing detached monitors retain caps
  while pending and available(active)>0:
   x=dict(pending.pop(0));log=open(x['monitor_log'],'xb')
   args=x['monitor_argv']
   x['proc']=subprocess.Popen(['/usr/bin/nohup']+args,stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,start_new_session=True,env={**os.environ,'OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1','MKL_NUM_THREADS':'1','VECLIB_MAXIMUM_THREADS':'1'})
   log.close();x['route_a_finished']=False;active.append(x);print(json.dumps({'event':'monitor_started','case':x['case'],'monitor_pid':x['proc'].pid}),flush=True)
   time.sleep(3)
  if active:time.sleep(5)
 print(json.dumps({'event':'launcher_finished','completed':completed,'blockers':blocked}),flush=True)
 return 1 if blocked else 0

def main():
 ap=argparse.ArgumentParser();ap.add_argument('plan');ap.add_argument('--seal',required=True);ap.add_argument('--seal-sha',required=True);ap.add_argument('--execute-root-only',action='store_true',required=True);ap.add_argument('--worker',action='store_true');a=ap.parse_args()
 plan=json.loads(Path(a.plan).read_bytes());validate(plan)
 sys.path.insert(0,str(HERE));import producer_guard_cx1v004 as guard
 guard.validate_seal(a.seal,a.seal_sha) # remains fail-closed until registered frozen pin successor
 if a.worker:return worker(plan)
 logpath=plan['launcher_log'];log=open(logpath,'xb')
 args=[sys.executable,'-I','-B',str(Path(__file__).resolve()),a.plan,'--seal',a.seal,'--seal-sha',a.seal_sha,'--execute-root-only','--worker']
 proc=subprocess.Popen(['/usr/bin/nohup']+args,stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,start_new_session=True);log.close()
 print(json.dumps({'detached_launcher_pid':proc.pid,'log':logpath}));return 0
if __name__=='__main__':raise SystemExit(main())
