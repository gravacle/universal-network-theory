"""Synthetic launcher tests. Admission mocked separately from root-admission tests; every Popen mocked."""
import copy,contextlib,hashlib,importlib.util,io,json,sys
from pathlib import Path
R=Path(__file__).parent;src=R/'route_a_token_launcher_cx1v006.py'
s=importlib.util.spec_from_file_location('launchtest',src);M=importlib.util.module_from_spec(s);s.loader.exec_module(M)
D=R/'TOKEN_LAUNCHER_0559_SYNTH_V001';D.mkdir();M.G.admission=lambda *a,**k:{'label':'SYNTHETIC_TEST_AUTHORITY_MOCK'};M.G.REGISTERED=(D/'registered_fake',);M.G.stamp=lambda rec,*a,**k:dict(rec,root_admission={'SYNTHETIC_MOCK':True})
def pin(p):return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def put(p,text):
 with p.open('x') as f:f.write(text)
 return p
checks=[]
def check(name,fn,typ=None):
 try:v=fn();ok=typ is None and v is not False
 except Exception as e:ok=typ is not None and isinstance(e,typ)
 checks.append({'name':name,'passed':ok})
def plan_for(d):
 d.mkdir();driver=put(d/'driver.py','# synthetic\n');monitor=put(d/'monitor.py','# synthetic\n')
 p={'route_a_admission':{'max_active':6,'minimum_free_percent':25,'poll_seconds':60,'source':'/usr/bin/memory_pressure','ramp':'previous_first_completed_route_a_iteration','first_case_exception':'C4T-KHI'},'driver':pin(driver),'monitor':pin(monitor),'launcher':pin(src),'guard':pin(Path(M.G.__file__)),'launcher_log':str(d/'launcher.log'),'calls':[]}
 for i in range(10):
  sp=put(d/f'spec{i}.json','{}');x={'case':'C4T-KHI' if i==0 else str(i),'spec':pin(sp),'outdir':str(d/f'run{i}'),'receipt':str(d/f'receipt{i}.json'),'monitor_log':str(d/f'monitor{i}.log'),'wall_cap_hours_proposed':14,'rss_cap_bytes_proposed':28*2**30,'output_cap_bytes_proposed':96*2**30};x['monitor_argv']=M.monitor_argv(p,x);p['calls'].append(x)
 return p
p=plan_for(D/'binding');check('complete_binding',lambda:M.validate(p))
for index in (3,5,7,9,11,13,15,17,19):
 q=copy.deepcopy(p);q['calls'][0]['monitor_argv'][index]='TAMPERED';check('argv_tamper_'+str(index),lambda q=q:M.validate(q),ValueError)
marked=D/'marked_copy';marked.mkdir();put(marked/'start.json',json.dumps({'call_spec_sha256':M.G.C5H_SPEC}))
q=copy.deepcopy(p);q['calls'][0]['outdir']=str(marked/'new_child');check('marked_outdir_refused',lambda:M.validate(q),PermissionError)
put(Path(p['launcher_log']),'synthetic log\n');check('worker_existing_own_log_allowed',lambda:M.validate(p,worker_mode=True));check('parent_existing_log_refused',lambda:M.validate(p),ValueError)
bad=copy.deepcopy(p);bad['driver']['sha256']='0'*64
check('public_worker_validates_first',lambda:M.worker(bad),ValueError)
for mode in ('success','ordinary','rss','low_memory'):
 plan=plan_for(D/mode);clock=[0.];procs=[];peak=[0];overlap=[0]
 class Proc:
  def __init__(self,args):
   self.out=Path(args[args.index('--outdir')+1]);self.receipt=Path(args[args.index('--receipt')+1]);self.out.mkdir();self.start=clock[0];self.pid=100+len(procs);self.fail=mode in ('ordinary','rss') and not procs;self.a=self.start+(1000 if self.fail else 10);self.end=self.start+(1 if self.fail else 100)
  def poll(self):return (1 if self.fail else 0) if clock[0]>=self.end else None
 def tick(seconds):
  clock[0]+=seconds
  for x in procs:
   pp=x.out/'progress.jsonl'
   if clock[0]>=x.a and not pp.exists():
    put(pp,'{"stage":"route_a","event":"finished"}\n')
    ip=x.out/'stages'/'01_route_a'/'attempt_000'/'progress.jsonl';ip.parent.mkdir(parents=True);put(ip,'{"stage":"iteration_completed","iteration":0}\n')
   if x.poll() is not None and not x.receipt.exists():put(x.receipt,json.dumps({'status':('STOPPED_RSS_CAP' if mode=='rss' else 'CHILD_FAILED') if x.fail else 'FINISHED','exit_code':1 if x.fail else 0}))
 def fake_popen(args,**kw):
  assert kw['start_new_session'] is True and args[0]=='/usr/bin/nohup'
  x=Proc(args);procs.append(x);live=[z for z in procs if z.poll() is None];peak[0]=max(peak[0],sum(clock[0]<z.a for z in live));overlap[0]=max(overlap[0],len(live));return x
 M.time.sleep=tick;M.subprocess.Popen=fake_popen;M.memory_free_percent=lambda:24 if mode=='low_memory' and clock[0]<120 else 25
 with contextlib.redirect_stdout(io.StringIO()):rc=M.worker(plan)
 expected_count=1 if mode in ('rss','ordinary') else 10;expected_rc=0 if mode in ('success','low_memory') else 1
 checks.append({'name':'simulation_'+mode,'max_route_a':peak[0],'max_monitors':overlap[0],'starts':len(procs),'exit':rc,'passed':peak[0]<=6 and len(procs)==expected_count and rc==expected_rc})
partial=put(D/'partial.jsonl','{"stage":"route_a","event":"finished"}');check('partial_no_release',lambda:not M.ra_finished(partial))
for i,(line,want) in enumerate([('{"stage":"iteration_completed","iteration":0}\n',True),('{"stage":"iteration_completed","iteration":0}',False),('{"stage":"iteration_completed","iteration":true}\n',False),('{"stage":"iteration_completed","iteration":-1}\n',False),('bad\n',False)]):
 pp=put(D/f'iteration{i}.jsonl',line);check('iteration_event_'+str(i),lambda pp=pp,want=want:M.first_iteration_completed(pp)==want)
with (R/'TOKEN_LAUNCHER_0559_TESTS_V001.json').open('x') as f:json.dump({'label':'TESTED synthetic only; admission and Popen mocked; no real monitor launched','launcher':pin(src),'tests':checks},f,indent=1)
print(sum(x['passed'] for x in checks),len(checks));assert all(x['passed'] for x in checks)
