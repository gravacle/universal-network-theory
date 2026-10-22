"""Direct inert reproductions of0625; ordinary OS helper only, no scientific work."""
import ast,builtins,copy,fcntl,hashlib,importlib.util,importlib.machinery,importlib._bootstrap_external,json,os,select,signal,subprocess,sys,types
from pathlib import Path
from unittest.mock import patch
I=Path(__file__).resolve().parent.parent;OUT=I/'tests/FIX0625_V003';OUT.mkdir()
def load(path,name):
 sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
L=load(I/'step4_launcher_cx1v008.py','fixL');G=L.G;B=load(I/'step4_bind_cx1v006.py','fixB')
checks=[]
def check(name,fn,err=None):
 try:v=fn();ok=err is None and v is not False;detail=repr(v)[:140]
 except BaseException as e:ok=err is not None and err in str(e);detail=type(e).__name__+': '+str(e)
 checks.append({'name':name,'passed':ok,'detail':detail})
def put(name,content):
 p=OUT/name;b=content.encode() if isinstance(content,str) else json.dumps(content,sort_keys=True).encode()
 with p.open('xb') as f:f.write(b)
 return p
# Lexically protected paths: all metadata operations are hostile mocks, no real path.
for name in ('UVT_SYNTH','KMAX_A2F10_C5H_RUN_V001','NGC3198_observed.csv'):
 with patch.object(G.os,'lstat',side_effect=AssertionError('METADATA_TOUCHED')) as st,patch.object(Path,'resolve',side_effect=AssertionError('RESOLVE_TOUCHED')):
  check('lexical_zero_metadata_'+name,lambda name=name:G.safe_path('/OWNED/'+name),'PROTECTED_PATH_REFUSED')
  check('zero_lstat_'+name,lambda:st.call_count==0)
# A virtual symlink leads to a virtual forbidden path; no real protected metadata.
probes=[]
def lstat(p):
 s=str(p);probes.append(s)
 if 'UVT_SYNTH' in s:raise AssertionError('PROTECTED_TARGET_PROBED')
 return types.SimpleNamespace(st_mode=0o120777 if s=='/OWNED/link' else 0o040755)
with patch.object(G.os,'lstat',lstat),patch.object(G.os,'readlink',return_value='/OWNED/UVT_SYNTH/child'):
 check('symlink_target_refused_before_probe',lambda:G.safe_path('/OWNED/link/result.json'),'PROTECTED_PATH_REFUSED')
 check('symlink_probes_only_lexically_safe',lambda:probes==['/OWNED','/OWNED/link'])
# Execute entire real launcher and binder bootstrap against wrong adjacent guard.
for file in ('step4_launcher_cx1v008.py','step4_bind_cx1v006.py'):
 d=OUT/file.replace('.py','');d.mkdir();guard=d/'step4_guard_cx1v007.py';sentinel=d/'UNVERIFIED_SENTINEL'
 with guard.open('x') as f:f.write('open('+repr(str(sentinel))+',"x").write("bad")\n')
 src=I/file
 with (d/file).open('xb') as f:f.write(src.read_bytes())
 check('bootstrap_'+file,lambda d=d,file=file:load(d/file,'inert_boot_'+file.replace('.','_')),'GUARD_BOOTSTRAP_HASH_MISMATCH')
 check('bootstrap_no_unverified_exec_'+file,lambda sentinel=sentinel:not sentinel.exists())
# Binder snapshots once; inject a changing late-read source and inspect publication.
base=I/'tests/SYNTH_V007';plan=G.decode((base/'001plan.json').read_bytes());cfg=G.decode((base/'001admission.json').read_bytes());cfg['plan']=None
candidate=put('CANDIDATE.json',cfg);original=(base/'001plan.json').read_bytes();reads=[]
raw=B.G.raw
def changing(path):
 if str(path)==str(base/'001plan.json'):
  reads.append(str(path));return original if len(reads)==1 else b'{"FORGED_LATE_BYTES":true}'
 return raw(path)
with patch.object(B.G,'raw',changing):
 check('binder_snapshot_success',lambda:B.bind(base/'001plan.json',candidate,OUT/'BOUND_PLAN.json',OUT/'BOUND_ADMISSION.json',OUT/'ROOT_COMMAND.sh')['plan']['sha256']==hashlib.sha256(original).hexdigest())
check('binder_plan_read_once',lambda:len(reads)==1)
check('binder_emits_validated_buffer',lambda:(OUT/'BOUND_PLAN.json').read_bytes()==original)
# Native exact SourceFileLoader function, AST-only extraction (no native imports).
orch=I.parents[1]/'calibration_orchestrator_c2/v005/calibration_orchestrator_c2v005.py'
node=next(n for n in ast.parse(orch.read_bytes()).body if isinstance(n,ast.FunctionDef) and n.name=='load_pinned_module')
env={'read_pinned':lambda p,label:G.verify(p),'importlib':importlib,'sha256_file':G.sha,'OrchestratorError':G.Refusal}
exec(compile(ast.Module(body=[node],type_ignores=[]),str(orch),'exec'),env)
for cached in (False,True):
 path=put('custody_'+str(cached)+'.py','VALUE="SOURCE_VERIFIED"\n');ref=G.pin(path)
 if cached:
  cache=Path(importlib.util.cache_from_source(str(path)));cache.parent.mkdir(exist_ok=True)
  code=compile('VALUE="STALE_CACHE"\n',str(path),'exec')
  data=importlib._bootstrap_external._code_to_timestamp_pyc(code,int(path.stat().st_mtime),path.stat().st_size)
  with cache.open('xb') as f:f.write(data)
 opens=[];realopen=builtins.open
 # Fence is the production path; cache bytes exist and would be eligible under a
 # standard loader. New get_code goes directly through hash-then-compile.
 with G.fence({str(path):ref['sha256']}):
  check('native_loader_cache_'+str(cached),lambda ref=ref,cached=cached:env['load_pinned_module'](ref,'owned_native_'+str(cached),'custody').VALUE=='SOURCE_VERIFIED')
 # compile audit validates the actual buffer, even after an earlier good prehash.
 with G.fence({str(path):ref['sha256']}):
  check('late_changed_compile_'+str(cached),lambda path=path:exec(compile(b'VALUE="CHANGED_AFTER_PREHASH"\n',str(path),'exec'),{}),'PREFLIGHT_COMPILE_HASH_MISMATCH')
check('SourceFileLoader_restored',lambda:importlib.machinery.SourceFileLoader.get_code.__name__=='get_code')
# Lifecycle fault cases: no actual scientific/monitor process is created.
for scenario in ('keyboard','systemexit','exception','signalterm','lost_assertion','restore_fail','poll_error'):
 d=OUT/('life_'+scenario);d.mkdir();p=copy.deepcopy(plan);p['launcher_log']=str(d/'launcher.log');Path(p['launcher_log']).touch(exist_ok=False)
 p['calls']=[copy.deepcopy(plan['calls'][0]),copy.deepcopy(plan['calls'][0])]
 for idx,c in enumerate(p['calls']):c.update(case='CASE'+str(idx),outdir=str(d/('run'+str(idx))),receipt=str(d/('rec'+str(idx))),monitor_log=str(d/('log'+str(idx))))
 events=[];spawned=[];ticks=[0];assertions=[0];interrupted=[False];handlers={}
 class Proc:
  pid=1234
  def __init__(self,kind):self.kind=kind;self.n=0
  def poll(self):
   self.n+=1
   if self.kind=='assertion':return 1 if scenario in ('lost_assertion','restore_fail') and ticks[0]>=1 else None
   if scenario=='poll_error' and self.n==1:raise RuntimeError('poll fault')
   return None if self.n<3 else 0
 def spawn(argv,**kw):
  spawned.append((argv,kw))
  if '-w' in argv:
   assertions[0]+=1
   if scenario=='restore_fail' and assertions[0]>1:raise OSError('restore denied')
   return Proc('assertion')
  events.append('monitor_start');return Proc('monitor')
 def snooze(n):
  ticks[0]+=1;events.append('sleep_lock_retained')
  if not interrupted[0]:
   interrupted[0]=True
   if scenario=='keyboard':raise KeyboardInterrupt()
   if scenario=='systemexit':raise SystemExit(3)
   if scenario=='exception':raise RuntimeError('ordinary fault')
   if scenario=='signalterm':handlers[signal.SIGTERM](signal.SIGTERM,None)
 def sig(s,h):old=handlers.get(s);handlers[s]=h;return old
 def close(fd):events.append('lock_closed')
 with patch.object(L.G,'validate',return_value=(p,{})),patch.object(L,'runtime_settings',lambda:None),patch.object(L,'normal_qos',lambda:None),patch.object(L,'acquire_lock',lambda:9876),patch.object(L.subprocess,'Popen',spawn),patch.object(L,'memory_free',lambda:80),patch.object(L,'route_a_finished',lambda p:False),patch.object(L,'first_iteration',lambda p:False),patch.object(L.time,'sleep',snooze),patch.object(L.os,'close',close),patch.object(L.signal,'signal',sig),patch.object(L.G,'raw',return_value=b'{"status":"FINISHED"}'):
  check('lifecycle_'+scenario,lambda:L.worker({'synthetic':'ref'})==1)
 monitor=[x for x in spawned if '-w' not in x[0]]
 check('no_second_monitor_'+scenario,lambda:len(monitor)==1)
 check('lock_retained_until_terminal_'+scenario,lambda:events[-1]=='lock_closed' and events.count('lock_closed')==1 and events.count('sleep_lock_retained')>=2)
 check('independent_lifetime_owner_'+scenario,lambda:monitor[0][0][:2]==['/usr/bin/caffeinate','-i'] and monitor[0][1]['pass_fds']==(9876,))
 if scenario in ('lost_assertion','restore_fail'):check('bounded_restore_'+scenario,lambda:assertions[0]==2)
# Ordinary inert OS helper verifies actual caffeinate/taskpolicy pass-through FD
# and exit behavior. It reads one inherited fd and stdin, prints one line, exits7.
lockpath=OUT/'OS_LOCK';fd=os.open(lockpath,os.O_CREAT|os.O_EXCL|os.O_RDONLY,0o600);fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
cmd=['/usr/bin/caffeinate','-i',sys.executable,'-I','-B','-c','import os,sys,subprocess;r=subprocess.run(["/usr/sbin/taskpolicy","-B","-p",str(os.getpid())],capture_output=True);assert r.returncode==0,r.stderr;os.fstat(int(sys.argv[1]));print("FD_READY",flush=True);sys.stdin.readline();raise SystemExit(7)',str(fd)]
proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,start_new_session=True,pass_fds=(fd,))
try:
 ready=select.select([proc.stdout],[],[],10)[0];line=proc.stdout.readline().strip() if ready else ''
 check('OS_wrapper_retains_inherited_fd',lambda:line=='FD_READY')
 os.close(fd);fd=None
 other=os.open(lockpath,os.O_RDONLY)
 try:check('OS_monitor_lifetime_lock_survives_parent_close',lambda:fcntl.flock(other,fcntl.LOCK_EX|fcntl.LOCK_NB),'Resource temporarily unavailable')
 finally:os.close(other)
 proc.stdin.write('finish\n');proc.stdin.flush();rc=proc.wait(timeout=10)
 check('OS_wrapper_forwards_exit7',lambda:rc==7)
finally:
 if fd is not None:os.close(fd)
 if proc.stdin:proc.stdin.close()
 if proc.poll() is None:proc.wait(timeout=10)
result={'label':'TESTED direct0625inertcontrols; ordinaryOShelper only; scientificprocesses0; fullscientificproductionUNTESTED','checks':checks,'passed':sum(x['passed'] for x in checks),'total':len(checks),'scientific_processes_created':0,'ordinary_os_helpers':1,'sources':[G.pin(x) for x in (I/'step4_guard_cx1v007.py',I/'step4_launcher_cx1v008.py',I/'step4_bind_cx1v006.py',Path(__file__))]}
with (OUT/'RESULTS.json').open('x') as f:json.dump(result,f,indent=2,allow_nan=False)
print(json.dumps({'passed':result['passed'],'total':result['total'],'failed':[x for x in checks if not x['passed']]}))
raise SystemExit(0 if result['passed']==result['total'] else 1)
