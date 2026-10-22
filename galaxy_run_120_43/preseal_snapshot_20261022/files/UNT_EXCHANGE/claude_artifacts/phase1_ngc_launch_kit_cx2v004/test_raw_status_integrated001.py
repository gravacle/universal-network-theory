"""Saved synthetic status and custody probes; no subprocess fixture launches."""
import ast, copy, hashlib, json, os, subprocess, sys, traceback, types
from pathlib import Path
HERE=Path(__file__).resolve().parent
BASE=HERE/'phase1_ngc_launch_cx2v004_draft003.py'
TEST=HERE.parent/'phase1_ngc_launch_kit_cx2v003/test_phase1_ngc_launch_cx2v003.py'
CORE=HERE/'raw_status_draft001.py'
raw=BASE.read_bytes(); test=TEST.read_bytes(); core=CORE.read_bytes()
assert hashlib.sha256(raw).hexdigest()=='8cec1b56fc682f638fee57329eefc9b3cddfa47959d175e7095fc0c5fe0342c9'
assert hashlib.sha256(test).hexdigest()=='a3cdbdc661b69bd8830ea0b0f68e02674b5319064c7fb8c7060928d971c73f49'
assert hashlib.sha256(core).hexdigest()=='48664e268c3ecc15158d946b21a6bb1e361931c4ed99df9b220be3a7f652398d'
M=types.ModuleType('raw_probe'); M.__file__=str(BASE)
exec(compile(raw,str(BASE),'exec'),M.__dict__); exec(compile(core,str(CORE),'exec'),M.__dict__)
date=subprocess.check_output(['/bin/date','-u'],env=dict(os.environ,LC_ALL='C'),text=True).strip()
WORK=Path(sys.argv[1]).resolve(); WORK.mkdir()
def audit(event,args):
 if event in ('os.rename','os.remove','os.rmdir','subprocess.Popen'): raise AssertionError('IMMUTABILITY_PROCESS_FENCE '+event)
 if event=='open' and isinstance(args[0],(str,bytes,os.PathLike)):
  p=os.path.realpath(os.fsdecode(args[0])); flags=args[2]
  if not p.startswith(str(WORK)+os.sep): raise AssertionError('READ_FENCE '+p)
  if isinstance(flags,int) and flags&(os.O_WRONLY|os.O_RDWR) and os.path.lexists(p): raise AssertionError('IMMUTABILITY_FENCE')
sys.addaudithook(audit)
tree=ast.parse(test)
names={'hash_bytes','error_text','exclusive','Suite','core_cases'}
selected=[]
for n in tree.body:
 if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name in names:
  if n.name=='core_cases':
   n.body=n.body[:next(i for i,x in enumerate(n.body) if isinstance(x,ast.FunctionDef) and x.name=='receipt')]
  selected.append(n)
text=ast.unparse(ast.Module(body=selected,type_ignores=[]))
text=text.replace('CX2V004', 'CX2V005').replace('CX2V003', 'CX2V004')
text=text.replace('stop = {\'reason\':',"stop = {'schema':'UNT_S0_TWIN_KILL_RECORD_C2V003A','pgid':123,'result':'KILLED_TERM','date_u':'synthetic date', 'reason':")
text=text.replace("M.raw_status(cap_rec, **tb), ('TWIN_PLANNED_STOP', 'PLANNED_STOP')", "M.raw_status(cap_rec, **tb), ('STOPPED_WALL_CAP|FAILED', 'CAP')")
assert "'pgid':123" in text
exec(compile(text,str(TEST)+':core_prefix','exec'),globals())
suite=Suite.__new__(Suite); suite.module=M; suite.tool_path=CORE; suite.tool_sha=hashlib.sha256(core).hexdigest(); suite.rows=[]; suite.interfaces={}; suite.refusals={}; suite.current_case='setup'; suite.root=WORK
core_cases(suite)
bind=dict(name=M.TWIN,attempt=1,outdir='/synthetic/run',receipt='/synthetic/run.receipt.json',launch_pin={'path':'/synthetic/launch.json','sha256':'a'*64},child_pid=100)
stop=dict(schema='UNT_S0_TWIN_KILL_RECORD_C2V003A',reason='ITERATION_0001_COMPLETED_AND_SIDECAR',outdir=bind['outdir'],launch_json=bind['launch_pin'],pgid=100,result='KILLED_TERM',date_u=date)
rec=dict(status='CHILD_FAILED',driver_status=None,exit_code=-15)
for key,value in [('schema','wrong'),('pgid',True),('pgid',101),('result','NOT_KILLED'),('date_u',''),('launch_json',{'path':'/other','sha256':'a'*64})]:
 suite.case('BOUND_'+key+'_'+str(value),lambda k=key,v=value: suite.refuses('TWIN_STOP_NOT_BOUND',lambda:M.raw_status(rec,**bind,stop=dict(stop,**{k:v}))))
for status,cls in [('STOPPED_WALL_CAP','CAP'),('STOPPED_RSS_CAP','CAP'),('STOPPED_OUTPUT_CAP','OUTPUT_CAP')]:
 suite.case('TWIN_'+status,lambda s=status,c=cls:suite.eq(M.raw_status(dict(rec,status=s),**bind),(s+'|NONE',c)))
suite.case('TWIN_signal_without_watch',lambda:suite.eq(M.raw_status(rec,**bind),('CHILD_FAILED|NONE|SIGNAL','INFRA')))
suite.case('TWIN_valid_KILL',lambda:suite.eq(M.raw_status(rec,**bind,stop=dict(stop,result='KILLED_KILL')),('TWIN_PLANNED_STOP','PLANNED_STOP')))
original=M.raw_status
mutants=[('missing_pid_check',"type(stop.get('pgid')) is int and stop['pgid'] == child_pid",'True',dict(stop,pgid=101)),('missing_result_check',"stop.get('result') in ('KILLED_TERM', 'KILLED_KILL')",'True',dict(stop,result='NOT_KILLED')),('missing_launch_binding',"stop.get('launch_json') == launch_pin",'True',dict(stop,launch_json={'path':'/other','sha256':'a'*64}))]
for label,a,b,bad in mutants:
 changed=core.decode(); assert changed.count(a)==1; changed=changed.replace(a,b)
 exec(compile(changed,str(CORE)+':'+label,'exec'),M.__dict__)
 def probe(bad=bad):
  try: suite.refuses('TWIN_STOP_NOT_BOUND',lambda:M.raw_status(rec,**bind,stop=bad))
  except AssertionError: return
  raise AssertionError('MUTANT_SURVIVED')
 suite.case('MUTANT_'+label,probe); M.raw_status=original
record=dict(date_u=date,scope='TESTED saved synthetic status/core prefix; public launcher UNTESTED',parent_sha256=hashlib.sha256(raw).hexdigest(),parent_test_sha256=hashlib.sha256(test).hexdigest(),component_sha256=hashlib.sha256(core).hexdigest(),cases=suite.rows,n_cases=len(suite.rows),n_pass=sum(r['status']=='PASS' for r in suite.rows))
with (WORK/'TEST_RECORD.json').open('xb') as f:f.write((json.dumps(record,sort_keys=True,indent=2)+'\n').encode())
for r in suite.rows:
 if r['status']!='PASS':print(json.dumps(r))
print('%d/%d PASS'%(record['n_pass'],record['n_cases']))
raise SystemExit(0 if record['n_pass']==record['n_cases'] else 1)
