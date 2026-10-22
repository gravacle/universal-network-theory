"""Independent final launcher control tests. All processes, sleeps and signals inert."""
import builtins,contextlib,copy,hashlib,io,json,os,signal,types
from pathlib import Path
from unittest.mock import patch
R=Path(__file__).resolve().parent;I=R.parent/'impl';OUT=R/'LIFETIME_INDEPENDENT_V001';OUT.mkdir();checks=[];pins={}
def cite(p):b=Path(p).read_bytes();pins[str(p)]=hashlib.sha256(b).hexdigest();return b
def load(p,name):m=types.ModuleType(name);m.__file__=str(p);exec(compile(cite(p),str(p),'exec'),m.__dict__);return m
def check(name,fn,exception=None):
 try:v=fn();ok=exception is None and v is not False;detail=repr(v)[:200]
 except BaseException as e:ok=exception is not None and exception in str(e);detail=type(e).__name__+': '+str(e)
 checks.append({'name':name,'passed':ok,'detail':detail})
L=load(I/'step4_launcher_cx1v007.py','lifetime_final');cite(I/'step4_guard_cx1v006.py')
d=OUT/'boot';d.mkdir();p=d/'step4_launcher_cx1v007.py'
with p.open('xb') as f:f.write(cite(I/p.name))
with (d/'step4_guard_cx1v006.py').open('xb') as f:f.write(b'import builtins\nbuiltins._final_boot_sentinel.append(1)\n')
with patch.object(builtins,'_final_boot_sentinel',[],create=True) as sent:
 check('final launcher hash before guard execution',lambda:load(p,'wrong_final_boot'),'GUARD_BOOTSTRAP_HASH_MISMATCH')
 check('final launcher never executes wrong guard',lambda:sent==[])
F=I/'tests/SYNTH_V006';base=json.loads(cite(F/'001plan.json'))
# Two monitors are active before each fault; observe state until both become terminal.
for scenario in ('keyboard','systemexit','runtimeerror','sigint','sigterm','sighup','assertion_loss','restore_spawn_failure','restore_dead','repeated_poll_error'):
 d=OUT/scenario;d.mkdir();plan=copy.deepcopy(base);plan['launcher_log']=str(d/'launcher.log');Path(plan['launcher_log']).touch(exist_ok=False)
 plan['calls']=[copy.deepcopy(base['calls'][0]) for _ in range(4)]
 for idx,c in enumerate(plan['calls']):c.update(case='INERT_'+str(idx),outdir=str(d/('out_'+str(idx))),receipt=str(d/('receipt_'+str(idx))),monitor_log=str(d/('monitor_'+str(idx))))
 trace=[];state={'tick':0,'closed':False,'assertions':0,'interrupted':False,'monitor_serial':0};monitors=[];handlers={};spawned=[];captured=io.StringIO()
 class Assertion:
  def __init__(self,n):self.n=n
  def poll(self):
   if scenario in ('assertion_loss','restore_spawn_failure','restore_dead') and state['tick']>=2:
    return 1 if self.n==1 or scenario=='restore_dead' else None
   return None
 class Monitor:
  def __init__(self,n):self.n=n;self.polls=0;self.terminal=False
  def poll(self):
   assert not state['closed'],'MONITOR_POLLED_AFTER_LOCK_RELEASE';self.polls+=1;trace.append(('poll',self.n,self.polls))
   if scenario=='repeated_poll_error' and 2<=state['tick']<17:raise RuntimeError('owned intermittent poll fault')
   if state['tick']>=22+self.n:self.terminal=True;trace.append(('terminal',self.n));return 0
   return None
 def popen(argv,**kw):
  assert not state['closed'];spawned.append((list(argv),kw))
  if '-w' in argv:
   state['assertions']+=1;trace.append(('assertion',state['assertions']))
   if scenario=='restore_spawn_failure' and state['assertions']>1:raise OSError('owned restore failure')
   return Assertion(state['assertions'])
  state['monitor_serial']+=1;p=Monitor(state['monitor_serial']);monitors.append(p);trace.append(('monitor',p.n));return p
 def sleep(seconds):
  assert seconds==60 and not state['closed'];state['tick']+=1;trace.append(('sleep',state['tick']))
  assert state['tick']<=35,'UNBOUNDED_INERT_LOOP'
  if state['tick']==2 and not state['interrupted']:
   state['interrupted']=True
   if scenario=='keyboard':raise KeyboardInterrupt('owned interrupt')
   if scenario=='systemexit':raise SystemExit('owned interrupt')
   if scenario=='runtimeerror':raise RuntimeError('owned error')
   if scenario in ('sigint','sigterm','sighup'):handlers[{'sigint':signal.SIGINT,'sigterm':signal.SIGTERM,'sighup':signal.SIGHUP}[scenario]](999,None)
 def close(fd):
  assert fd==8765 and all(p.terminal for p in monitors),'LOCK_RELEASE_BEFORE_MONITORS_TERMINAL';state['closed']=True;trace.append(('closed',fd))
 def sig(s,h):old=handlers.get(s);handlers[s]=h;return old
 def validate(*a,**k):trace.append(('validate',));return plan,{}
 def qos():trace.append(('qos',));assert any(x[0]=='validate' for x in trace)
 with patch.object(L.G,'validate',validate),patch.object(L,'runtime_settings',lambda:None),patch.object(L,'normal_qos',qos),patch.object(L,'acquire_lock',lambda:8765),patch.object(L.subprocess,'Popen',popen),patch.object(L,'memory_free',lambda:80),patch.object(L,'first_iteration',lambda p:True),patch.object(L,'route_a_finished',lambda p:False),patch.object(L.G,'raw',return_value=b'{"status":"FINISHED"}'),patch.object(L.time,'sleep',sleep),patch.object(L.os,'close',close),patch.object(L.signal,'signal',sig),contextlib.redirect_stdout(captured):
  check('drain returns failure '+scenario,lambda:L.worker({'owned':'ref'})==1)
 check('two active monitors, no pending admission '+scenario,lambda:len(monitors)==2)
 check('lock closes only after both terminal '+scenario,lambda:state['closed'] and all(p.terminal for p in monitors) and trace[-1]==('closed',8765))
 check('drain polling has bounded cadence '+scenario,lambda:22<=state['tick']<=26 and len([x for x in trace if x[0]=='sleep'])==state['tick'])
 check('monitor lifetime wrapper and lock inherited '+scenario,lambda:all(argv[:2]==['/usr/bin/caffeinate','-i'] and argv[2:5]==[L.PYTHON,'-I','-B'] and kw['pass_fds']==(8765,) for argv,kw in spawned if '-w' not in argv))
 records=[json.loads(x) for x in captured.getvalue().splitlines()];final=records[-1]
 check('bounded deduplicated failure records '+scenario,lambda:final['event']=='step4_finished' and 1<=len(final['failures'])<=3 and len({(x['reason'],x['case']) for x in final['failures']})==len(final['failures']))
 check('only bounded assertion restoration '+scenario,lambda:state['assertions']==(2 if scenario in ('assertion_loss','restore_spawn_failure','restore_dead') else 1))
 check('handlers restored '+scenario,lambda:all(handlers[x] is None for x in (signal.SIGINT,signal.SIGTERM,signal.SIGHUP)))
 with (d/'TRACE.json').open('x') as f:json.dump({'trace':trace,'final':final},f)
# Actual main/worker guard call ordering; all subprocess interfaces hostile spies.
for entry in ('main','worker'):
 attempts=[]
 def badvalidate(*a,**k):raise L.G.Refusal('INERT_GUARD_REFUSAL')
 def process(*a,**k):attempts.append(a);raise AssertionError('SUBPROCESS_BEFORE_GUARD')
 with patch.object(L.G,'validate',badvalidate),patch.object(L.G,'pin',return_value={'owned':'ref'}),patch.object(L.subprocess,'Popen',process),patch.object(L.subprocess,'run',process),patch.object(L.sys,'argv',['launcher','/owned/plan','--execute-root-only']):
  check('guard refusal precedes subprocess '+entry,lambda:getattr(L,entry)(*([{'owned':'ref'}] if entry=='worker' else [])),'INERT_GUARD_REFUSAL')
 check('no subprocess attempted on refusal '+entry,lambda:attempts==[])
# Verify exact executable and PID form, positive and fail-closed return semantics.
seen=[]
def run(argv,**kw):seen.append((argv,kw));return types.SimpleNamespace(returncode=0)
with patch.object(L.subprocess,'run',run),patch.object(L.os,'getpid',return_value=12345):
 check('normal QoS accepts zero',lambda:L.normal_qos() is None)
check('normal QoS exact platform argv',lambda:seen[0][0]==['/usr/sbin/taskpolicy','-B','-p','12345'] and seen[0][1]['timeout']==10)
with patch.object(L.subprocess,'run',return_value=types.SimpleNamespace(returncode=64)):
 check('normal QoS refuses nonzero',lambda:L.normal_qos(),'NORMAL_QOS_RESET_FAILED')
cite(__file__)
report={'status':'TESTED','scope':'Final v007 Python lifecycle controls only; all processes, signals and sleeps mocked. Two active monitors drain over 22+ mocked minutes per scenario.','checks':checks,'passed':sum(x['passed'] for x in checks),'total':len(checks),'citations':pins,'limitations':['Native OS signals/SIGKILL not tested here.','Actual caffeinate fd/assertion/exit behavior not inferred from mocked argv.','Actual scientific monitor never executed.']}
with (OUT/'RESULTS.json').open('x') as f:json.dump(report,f,indent=2)
print(json.dumps({'passed':report['passed'],'total':report['total'],'failed':[x for x in checks if not x['passed']],'results_sha256':hashlib.sha256((OUT/'RESULTS.json').read_bytes()).hexdigest()}))
raise SystemExit(0 if report['passed']==report['total'] else 1)
