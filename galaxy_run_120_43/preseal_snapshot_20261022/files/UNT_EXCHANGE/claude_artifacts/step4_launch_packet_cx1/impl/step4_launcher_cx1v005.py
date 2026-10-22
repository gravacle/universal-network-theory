"""Root-only step-4 direct batches. No automatic retry; no raw campaign fallback."""
import argparse, fcntl, importlib.util, json, os, re, subprocess, sys, time
from pathlib import Path
HERE=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('_step4_guard',HERE/'step4_guard_cx1v005.py')
G=importlib.util.module_from_spec(sp);sp.loader.exec_module(G)
PYTHON='/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
BLAS={k:'1' for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS')}
LOCK=HERE.parent/'STEP4_MACHINE_LOCK_V001'
def monitor_argv(plan,call):
    return [PYTHON,'-I','-B',plan['monitor']['path'],'--driver',call['driver']['path'],'--driver-sha256',call['driver']['sha256'],'--spec',call['spec']['path'],'--outdir',call['outdir'],'--receipt',call['receipt'],'--wall-cap-s',str(call['wall_cap_s']),'--rss-cap-bytes',str(call['rss_cap_bytes']),'--output-cap-bytes',str(call['output_cap_bytes']),'--poll-s','2.0']
def read_progress(path):
    p=G.safe_path(str(path))
    if not p.is_file():return []
    rows=[]
    for b in p.read_bytes().splitlines(keepends=True):
        if not b.endswith(b'\n'):continue
        r=G.decode(b);G.require(isinstance(r,dict),'MALFORMED_PROGRESS');rows.append(r)
    return rows
def first_iteration(path):
    return any(r.get('stage')=='iteration_completed' and type(r.get('iteration')) is int and r['iteration']>=0 for r in read_progress(path))
def route_a_finished(path):
    return any(r.get('stage')=='route_a' and r.get('event')=='finished' for r in read_progress(path))
def memory_free():
    try:
        s=subprocess.check_output(['/usr/bin/memory_pressure'],text=True,stderr=subprocess.STDOUT,timeout=10)
        m=re.findall(r'^System-wide memory free percentage:\s*(\d+)%\s*$',s,re.M)
        return int(m[0]) if len(m)==1 and 0<=int(m[0])<=100 else None
    except Exception:return None
def decision(*,active_route_a,free,previous_iteration,first,max_active):
    return type(active_route_a) is int and 0<=active_route_a<max_active and type(free) is int and 25<=free<=100 and (first or previous_iteration is True)
def systemic(receipt,rc):
    if not isinstance(receipt,dict) or not receipt:return 'MISSING_OR_MALFORMED_RECEIPT'
    s=str(receipt.get('status',''));d=str(receipt.get('driver_status',''))
    if s in ('STOPPED_RSS_CAP','STOPPED_OUTPUT_CAP'):return s
    if receipt.get('exit_code') in (-9,137):return 'POSSIBLE_MEMORY_PRESSURE_KILL'
    if rc==2 or 'REFUSED' in s or 'REFUSED' in d:return 'SETUP_REFUSAL'
    return None
def runtime_settings():
    G.require(os.getpriority(os.PRIO_PROCESS,0)>=10,'NICE_10_REQUIRED')
    G.require(all(os.environ.get(k)=='1' for k in BLAS),'SINGLE_THREAD_BLAS_REQUIRED')
def acquire_lock():
    # A persistent empty inode plus flock: never delete, truncate or rewrite it.
    G.require(not LOCK.is_symlink(),'LOCK_SYMLINK_REFUSED')
    try:fd=os.open(LOCK,os.O_CREAT|os.O_EXCL|os.O_RDONLY,0o600)
    except FileExistsError:fd=os.open(LOCK,os.O_RDONLY)
    try:fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
    except BaseException:os.close(fd);raise G.Refusal('ANOTHER_STEP4_BATCH_ACTIVE')
    return fd

def worker(plan_ref):
    plan,cfg=G.validate(plan_ref,__file__,check_outputs=False)
    runtime_settings()
    G.require(Path(plan['launcher_log']).is_file() and not Path(plan['launcher_log']).is_symlink(),'WORKER_LAUNCHER_LOG_REQUIRED')
    for c in plan['calls']:
        for q in (c['outdir'],c['receipt'],c['receipt']+'.launch.json',c['monitor_log']):G.require(not os.path.lexists(q),'WORKER_EXISTING_CALL_OUTPUT')
    lock=acquire_lock()
    assertion=None;active=[];pending=list(plan['calls']);previous=None;failures=[];finished=[]
    try:
        # Admission precedes even the non-scientific assertion process.
        G.validate(plan_ref,__file__,check_outputs=False)
        assertion=subprocess.Popen(['/usr/bin/caffeinate','-i','-w',str(os.getpid())],stdin=subprocess.DEVNULL,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        G.require(assertion.poll() is None,'SLEEP_ASSERTION_FAILED')
        while pending or active:
            try:
                G.require(assertion.poll() is None,'SLEEP_ASSERTION_LOST')
                G.validate(plan_ref,__file__,check_outputs=False)
                runtime_settings()
            except Exception as e:
                failures.append({'reason':'ADMISSION_REVOKED','detail':str(e)});pending=[]
            for item in list(active):
                c=item['call']
                try:item['route_a_finished']=route_a_finished(Path(c['outdir'])/'progress.jsonl')
                except Exception as e:
                    failures.append({'case':c['case'],'reason':'MALFORMED_PROGRESS','detail':str(e)});pending=[]
                rc=item['proc'].poll()
                if rc is None:continue
                try:receipt=G.decode(G.raw(c['receipt']))
                except Exception:receipt={}
                reason=systemic(receipt,rc)
                if reason:failures.append({'case':c['case'],'reason':reason});pending=[]
                ok=rc==0 and receipt.get('status')=='FINISHED' and item['route_a_finished']
                finished.append({'case':c['case'],'passed':ok,'monitor_exit':rc,'receipt_status':receipt.get('status')})
                item['terminal']=True;active.remove(item)
            if pending:
                try:
                    prev_ok=previous is None or first_iteration(Path(previous['call']['outdir'])/'stages/01_route_a/attempt_000/progress.jsonl')
                    count=sum(not item['route_a_finished'] for item in active)
                    free=memory_free()
                    go=decision(active_route_a=count,free=free,previous_iteration=prev_ok,first=previous is None,max_active=plan['route_a_admission']['max_active'])
                    print(json.dumps({'event':'step4_admission_decision','case':pending[0]['case'],'free_percent':free,'active_route_a':count,'previous_first_iteration':prev_ok,'admitted':go}),flush=True)
                    if previous is not None and previous.get('terminal') and not prev_ok:raise G.Refusal('PREDECESSOR_ENDED_BEFORE_FIRST_ITERATION')
                    if go:
                        c=pending[0]
                        # Reverify all scientific gates and pins immediately before each start.
                        G.validate(plan_ref,__file__,check_outputs=False)
                        for p in (c['outdir'],c['receipt'],c['receipt']+'.launch.json',c['monitor_log']):G.require(not os.path.lexists(p),'OUTPUT_APPEARED_BEFORE_START')
                        G.require(assertion.poll() is None,'SLEEP_ASSERTION_LOST')
                        with open(c['monitor_log'],'xb') as log:
                            proc=subprocess.Popen(['/usr/bin/taskpolicy','-B']+monitor_argv(plan,c),stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,start_new_session=True,env={**os.environ,**BLAS})
                        item={'call':c,'proc':proc,'route_a_finished':False,'terminal':False}
                        active.append(item);previous=item;pending.pop(0)
                except Exception as e:
                    failures.append({'reason':'START_OR_RAMP_REFUSAL','detail':str(e)});pending=[]
            if pending or active:time.sleep(60)
        print(json.dumps({'event':'step4_finished','finished':finished,'failures':failures,'retry':'NONE'}),flush=True)
        return 1 if failures or not all(x['passed'] for x in finished) else 0
    finally:
        # Do not kill existing scientific monitors. The assertion follows this worker PID.
        os.close(lock)

def main():
    p=argparse.ArgumentParser();p.add_argument('plan');p.add_argument('--execute-root-only',required=True,action='store_true');p.add_argument('--worker',action='store_true');a=p.parse_args()
    ref=G.pin(a.plan);plan,cfg=G.validate(ref,__file__,check_outputs=not a.worker);runtime_settings()
    if a.worker:return worker(ref)
    G.require(not os.path.lexists(plan['launcher_log']),'EXISTING_LAUNCHER_LOG')
    # Guard passed before the first Popen. The detached child guards again.
    with open(plan['launcher_log'],'xb') as log:
        proc=subprocess.Popen(['/usr/bin/nohup','/usr/bin/taskpolicy','-B',PYTHON,'-I','-B',__file__,a.plan,'--execute-root-only','--worker'],stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,start_new_session=True,env={**os.environ,**BLAS})
    print(json.dumps({'detached_worker_pid':proc.pid,'launcher_log':plan['launcher_log'],'admission_sha256':os.environ['UNT_STEP4_ADMISSION_SHA256']}));return 0
if __name__=='__main__':raise SystemExit(main())
