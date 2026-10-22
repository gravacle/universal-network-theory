"""0541/0543 root-config-sealed token launcher. PLAN --execute-root-only [--worker].
No caller seal hash. Public functions guard on every call. Tests mock admission/process creation explicitly.
"""
import argparse,errno,hashlib,json,os,subprocess,sys,time
from pathlib import Path
HERE=Path(__file__).parent;sys.path.insert(0,str(HERE))
import producer_guard_cx1v005 as G
PYTHON='/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'

@G.guarded
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
@G.guarded
def ra_finished(path):
 p=Path(path)
 if not p.exists():return False
 for line in p.read_bytes().splitlines(keepends=True):
  if not line.endswith(b'\n'):continue
  row=json.loads(line)
  if row.get('stage')=='route_a' and row.get('event')=='finished':return True
 return False
@G.guarded
def available(active):return max(0,3-sum(not x['route_a_finished'] for x in active))
@G.guarded
def monitor_argv(plan,x):
 return [PYTHON,'-I','-B',plan['monitor']['path'],'--driver',plan['driver']['path'],'--driver-sha256',plan['driver']['sha256'],'--spec',x['spec']['path'],'--outdir',x['outdir'],'--receipt',x['receipt'],'--wall-cap-s',str(x['wall_cap_hours_proposed']*3600),'--rss-cap-bytes',str(x['rss_cap_bytes_proposed']),'--output-cap-bytes',str(x['output_cap_bytes_proposed']),'--poll-s','2.0']
@G.guarded
def validate(plan, worker_mode=False):
 for key in ('driver','monitor','launcher','guard'):
  ref=plan[key]
  if sha(ref['path'])!=ref['sha256']:raise ValueError('INPUT_PIN_MISMATCH '+key)
 if plan['launcher']['path']!=str(Path(__file__).resolve()) or plan['guard']['path']!=str(Path(G.__file__).resolve()):raise ValueError('WRONG_LAUNCHER_OR_GUARD')
 if len(plan['calls'])!=10 or len({x['case'] for x in plan['calls']})!=10:raise ValueError('TEN_DISTINCT_CASES_REQUIRED')
 seen=set()
 for x in plan['calls']:
  if sha(x['spec']['path'])!=x['spec']['sha256']:raise ValueError('SPEC_PIN_MISMATCH')
  if x['monitor_argv']!=monitor_argv(plan,x):raise ValueError('MONITOR_ARGV_BINDING')
  if any(type(x[k]) is not int or x[k]<=0 for k in ('wall_cap_hours_proposed','rss_cap_bytes_proposed','output_cap_bytes_proposed')):raise ValueError('CAP_TYPE')
  for p in (x['outdir'],x['receipt'],x['receipt']+'.launch.json',x['monitor_log']):
   G.check_run_path(p,allow_registered=False)
   if p in seen or os.path.lexists(p):raise ValueError('EXISTING_OR_DUPLICATE_OUTPUT')
   seen.add(p)
 G.check_run_path(plan['launcher_log'],allow_registered=False)
 if not worker_mode and os.path.lexists(plan['launcher_log']):raise ValueError('EXISTING_LAUNCHER_LOG')
 return True
@G.guarded
def systemic(rec,monitor_exit):
 status=str(rec.get('status',''));driver=str(rec.get('driver_status',''))
 if status in ('STOPPED_RSS_CAP','STOPPED_OUTPUT_CAP'):return status
 if rec.get('exit_code') in (-9,137):return 'POSSIBLE_MEMORY_PRESSURE_KILL'
 if monitor_exit==2 or 'REFUSED' in status or 'REFUSED' in driver:return 'REPEATING_SETUP_REFUSAL_REQUIRES_ROOT'
 if not rec:return 'MISSING_MONITOR_RECEIPT_REQUIRES_ROOT'
 return None
@G.guarded
def worker(plan):
 pending=list(plan['calls']);active=[];completed=[];systemic_failures=[];ordinary_failures=[]
 while pending or active:
  for x in list(active):
   try:x['route_a_finished']=ra_finished(Path(x['outdir'])/'progress.jsonl')
   except Exception:x['progress_defect']=True # retain token until monitor completion
   rc=x['proc'].poll()
   if rc is None:continue
   rp=Path(x['receipt'])
   try:rec=json.loads(rp.read_bytes()) if rp.exists() else {}
   except Exception:rec={}
   reason=systemic(rec,rc)
   if reason:systemic_failures.append({'case':x['case'],'reason':reason})
   good=rc==0 and rec.get('status')=='FINISHED' and x['route_a_finished'] and not x.get('progress_defect')
   if not good:ordinary_failures.append(x['case'])
   completed.append({'case':x['case'],'monitor_exit':rc,'receipt_status':rec.get('status'),'passed':good});active.remove(x)
  if systemic_failures:pending=[]
  while pending and available(active)>0:
   x=dict(pending.pop(0))
   try:
    log=open(x['monitor_log'],'xb')
    try:x['proc']=subprocess.Popen(['/usr/bin/nohup']+monitor_argv(plan,x),stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,start_new_session=True,env={**os.environ,'OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1','MKL_NUM_THREADS':'1','VECLIB_MAXIMUM_THREADS':'1'})
    finally:log.close()
   except OSError as e:
    systemic_failures.append({'case':x['case'],'reason':'DISK_GUARD' if e.errno in (errno.ENOSPC,errno.EDQUOT) else 'MONITOR_START_SETUP_REFUSAL'});pending=[];break
   x['route_a_finished']=False;active.append(x);print(json.dumps({'event':'monitor_started','case':x['case'],'monitor_pid':x['proc'].pid}),flush=True);time.sleep(3)
  if active:time.sleep(5)
 print(json.dumps({'event':'launcher_finished','completed':completed,'ordinary_failures':ordinary_failures,'systemic_failures':systemic_failures}),flush=True)
 return 1 if ordinary_failures or systemic_failures else 0
@G.guarded
def main():
 ap=argparse.ArgumentParser();ap.add_argument('plan');ap.add_argument('--execute-root-only',action='store_true',required=True);ap.add_argument('--worker',action='store_true');a=ap.parse_args()
 plan=json.loads(Path(a.plan).read_bytes());validate(plan,worker_mode=a.worker)
 if a.worker:return worker(plan)
 log=open(plan['launcher_log'],'xb');args=[PYTHON,'-I','-B',str(Path(__file__).resolve()),a.plan,'--execute-root-only','--worker']
 try:proc=subprocess.Popen(['/usr/bin/nohup']+args,stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
 finally:log.close()
 print(json.dumps({'detached_launcher_pid':proc.pid,'log':plan['launcher_log']}));return 0
if __name__=='__main__':raise SystemExit(main())
