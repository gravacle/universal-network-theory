"""CX3V001 S1 pair launcher: one worker holds the unchanged machine lock for both calls. Runtime functions byte-for-byte AST-equal to launcher015."""
"""Root-only step-4 direct batches. No automatic retry; no raw campaign fallback."""
# c2v015 = launcher014 (5d6af4a7) with its memory terms removed (V006 A172): no memory_free / memory_pressure read, no
# free term in decision or in the admission log, no nice >= 10 requirement; the guard is guard014. The machine lock,
# max_active, the first-iteration ramp, single-thread BLAS, normal QoS, caffeinate and drain-on-failure are launcher014's.
import argparse, fcntl, hashlib, json, os, signal, subprocess, sys, time, types
from pathlib import Path
HERE=Path(__file__).resolve().parent
GUARD_PATH=HERE/'step4_guard_c2v014_s1pair_cx3v001.py'
GUARD_SHA256='1274a39a19a7d8540858b8f45be0b683e776fa4fc1386bec10871bb0342ac6cc'
GUARD_BYTES=GUARD_PATH.read_bytes()
if hashlib.sha256(GUARD_BYTES).hexdigest()!=GUARD_SHA256:
    raise PermissionError('GUARD_BOOTSTRAP_HASH_MISMATCH')
G=types.ModuleType('_step4_guard');G.__file__=str(GUARD_PATH)
exec(compile(GUARD_BYTES,str(GUARD_PATH),'exec'),G.__dict__)
PYTHON='/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
BLAS={k:'1' for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS')}
LOCK=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/STEP4_MACHINE_LOCK_V001')
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
def decision(*,active_route_a,previous_iteration,first,max_active):
    return type(active_route_a) is int and 0<=active_route_a<max_active and (first or previous_iteration is True)
def systemic(receipt,rc):
    if not isinstance(receipt,dict) or not receipt:return 'MISSING_OR_MALFORMED_RECEIPT'
    s=str(receipt.get('status',''));d=str(receipt.get('driver_status',''))
    if s in ('STOPPED_RSS_CAP','STOPPED_OUTPUT_CAP'):return s
    if receipt.get('exit_code') in (-9,137):return 'POSSIBLE_MEMORY_PRESSURE_KILL'
    if rc==2 or 'REFUSED' in s or 'REFUSED' in d:return 'SETUP_REFUSAL'
    return None
def runtime_settings():
    G.require(all(os.environ.get(k)=='1' for k in BLAS),'SINGLE_THREAD_BLAS_REQUIRED')
def normal_qos():
    # macOS -B is a PID operation, not a utility wrapper. Children inherit it.
    result=subprocess.run(['/usr/sbin/taskpolicy','-B','-p',str(os.getpid())],stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=10)
    G.require(result.returncode==0,'NORMAL_QOS_RESET_FAILED')

def acquire_lock():
    # A persistent empty inode plus flock: never delete, truncate or rewrite it.
    G.require(not LOCK.is_symlink(),'LOCK_SYMLINK_REFUSED')
    try:fd=os.open(LOCK,os.O_CREAT|os.O_EXCL|os.O_RDONLY,0o600)
    except FileExistsError:fd=os.open(LOCK,os.O_RDONLY)
    try:fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
    except BaseException:os.close(fd);raise G.Refusal('ANOTHER_STEP4_BATCH_ACTIVE')
    return fd

def worker(plan_ref):
    plan,cfg=G.validate(plan_ref,__file__,check_outputs=False,disk_batch=False)
    runtime_settings()
    G.require(Path(plan['launcher_log']).is_file() and not Path(plan['launcher_log']).is_symlink(),'WORKER_LAUNCHER_LOG_REQUIRED')
    for c in plan['calls']:
        for q in (c['outdir'],c['receipt'],c['receipt']+'.launch.json',c['monitor_log']):G.require(not os.path.lexists(q),'WORKER_EXISTING_CALL_OUTPUT')
    lock=acquire_lock();assertion=None;active=[];pending=list(plan['calls'])
    previous=None;failures=[];failure_keys=set();finished=[];draining=False
    stop={'signal':None};old_handlers={};restoration_attempted=False
    def note(reason,case=None,detail=None):
        key=(reason,case)
        if key not in failure_keys:
            failure_keys.add(key);failures.append({'reason':reason,'case':case,'detail':detail})
    def drain(reason,case=None,detail=None):
        nonlocal draining
        draining=True;pending.clear();note(reason,case,detail)
    def on_signal(number,frame):stop['signal']=number
    def sleep_process():
        return subprocess.Popen(['/usr/bin/caffeinate','-i','-w',str(os.getpid())],stdin=subprocess.DEVNULL,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    try:
        for sig in (signal.SIGINT,signal.SIGTERM,signal.SIGHUP):
            old_handlers[sig]=signal.signal(sig,on_signal)
        G.validate(plan_ref,__file__,check_outputs=False,disk_batch=False)
        normal_qos()
        assertion=sleep_process();G.require(assertion.poll() is None,'SLEEP_ASSERTION_FAILED')
        while pending or active:
            try:
                if stop['signal'] is not None:drain('WORKER_SIGNAL',detail=str(stop['signal']))
                if assertion.poll() is not None:
                    drain('SLEEP_ASSERTION_LOST')
                    # One bounded safety-only restoration. Each active monitor also
                    # owns a utility-lifetime assertion, independent of this worker.
                    if not restoration_attempted:
                        restoration_attempted=True
                        try:
                            assertion=sleep_process()
                            G.require(assertion.poll() is None,'SLEEP_ASSERTION_RESTORE_FAILED')
                        except BaseException as e:note('SLEEP_ASSERTION_RESTORE_FAILED',detail=str(e))
                if not draining:
                    try:G.validate(plan_ref,__file__,check_outputs=False,disk_batch=False);runtime_settings()
                    except Exception as e:drain('ADMISSION_REVOKED',detail=str(e))
                for item in list(active):
                    c=item['call']
                    try:item['route_a_finished']=route_a_finished(Path(c['outdir'])/'progress.jsonl')
                    except Exception as e:drain('MALFORMED_PROGRESS',c['case'],str(e))
                    try:rc=item['proc'].poll()
                    except BaseException as e:
                        drain('MONITOR_POLL_ERROR',c['case'],str(e));continue
                    if rc is None:continue
                    try:receipt=G.decode(G.raw(c['receipt']))
                    except Exception:receipt={}
                    reason=systemic(receipt,rc)
                    if reason:drain(reason,c['case'])
                    ok=rc==0 and receipt.get('status')=='FINISHED' and item['route_a_finished']
                    finished.append({'case':c['case'],'passed':ok,'monitor_exit':rc,'receipt_status':receipt.get('status')})
                    item['terminal']=True;active.remove(item)
                if pending and not draining:
                    prev_ok=previous is None or first_iteration(Path(previous['call']['outdir'])/'stages/01_route_a/attempt_000/progress.jsonl')
                    count=sum(not item['route_a_finished'] for item in active)
                    disk=G.disk_admission(plan,pending[0])
                    go=decision(active_route_a=count,previous_iteration=prev_ok,first=previous is None,max_active=plan['route_a_admission']['max_active'])
                    print(json.dumps({'event':'step4_admission_decision','case':pending[0]['case'],'active_route_a':count,'previous_first_iteration':prev_ok,'admitted':go}),flush=True)
                    if previous is not None and previous.get('terminal') and not prev_ok:raise G.Refusal('PREDECESSOR_ENDED_BEFORE_FIRST_ITERATION')
                    if go:
                        c=pending[0];G.validate(plan_ref,__file__,check_outputs=False,disk_batch=False)
                        G.disk_admission(plan,c)
                        for q in (c['outdir'],c['receipt'],c['receipt']+'.launch.json',c['monitor_log']):G.require(not os.path.lexists(q),'OUTPUT_APPEARED_BEFORE_START')
                        G.require(assertion.poll() is None,'SLEEP_ASSERTION_LOST')
                        if stop['signal'] is not None:drain('WORKER_SIGNAL',detail=str(stop['signal']))
                        else:
                            with open(c['monitor_log'],'xb') as log:
                                proc=subprocess.Popen(['/usr/bin/caffeinate','-i']+monitor_argv(plan,c),stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,start_new_session=True,env={**os.environ,**BLAS},pass_fds=(lock,))
                                # Register before log closure: an error closing or
                                # reporting the log cannot orphan an untracked monitor.
                                item={'call':c,'proc':proc,'route_a_finished':False,'terminal':False}
                                active.append(item);previous=item;pending.pop(0)
                if pending or active:time.sleep(60)
            except BaseException as e:
                drain('WORKER_INTERRUPTED_OR_ERROR',detail=type(e).__name__+': '+str(e))
                # Drain survives catchable interrupts. Retain active handles and the
                # lock, sleep with bounded cadence, and never admit another monitor.
                if active:
                    try:time.sleep(60)
                    except BaseException as again:note('DRAIN_INTERRUPTED',detail=type(again).__name__)
        print(json.dumps({'event':'step4_finished','finished':finished,'failures':failures,'retry':'NONE'}),flush=True)
        return 1 if failures or not all(x['passed'] for x in finished) else 0
    finally:
        for sig,old in old_handlers.items():signal.signal(sig,old)
        # Catchable errors cannot leave this block with active monitors; descriptors
        # are additionally inherited by each monitor's caffeinate lifetime owner.
        if active:raise RuntimeError('ACTIVE_MONITORS_RETAINED_LOCK_NOT_CLOSED')
        os.close(lock)

def main():
    p=argparse.ArgumentParser();p.add_argument('plan');p.add_argument('--execute-root-only',required=True,action='store_true');p.add_argument('--worker',action='store_true');a=p.parse_args()
    ref=G.pin(a.plan);plan,cfg=G.validate(ref,__file__,check_outputs=not a.worker);runtime_settings()
    if a.worker:return worker(ref)
    G.require(not os.path.lexists(plan['launcher_log']),'EXISTING_LAUNCHER_LOG')
    normal_qos()
    # Guard passed before the first Popen. The detached child guards again.
    with open(plan['launcher_log'],'xb') as log:
        proc=subprocess.Popen(['/usr/bin/nohup',PYTHON,'-I','-B',__file__,a.plan,'--execute-root-only','--worker'],stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,start_new_session=True,env={**os.environ,**BLAS})
    print(json.dumps({'detached_worker_pid':proc.pid,'launcher_log':plan['launcher_log'],'admission_sha256':os.environ['UNT_STEP4_ADMISSION_SHA256']}));return 0
if __name__=='__main__':raise SystemExit(main())
