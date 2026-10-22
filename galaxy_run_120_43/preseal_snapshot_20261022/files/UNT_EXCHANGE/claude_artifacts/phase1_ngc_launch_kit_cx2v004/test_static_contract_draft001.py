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
raw_parent=(HERE.parent/'phase1_ngc_launch_kit_cx2v003/phase1_ngc_launch_cx2v003.py').read_bytes()
assert hashlib.sha256(raw_parent).hexdigest()=='af0210715f658c43f73f37a5e6e733f7a48dc374caa1b8af5a0defe3987854d7'
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
names={'hash_bytes','error_text','exclusive','Suite','process_cases'}
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
assert 'def process_cases' in text
exec(compile(text,str(TEST)+':core_prefix','exec'),globals())
suite=Suite.__new__(Suite); suite.module=M; suite.tool_path=CORE; suite.tool_sha=hashlib.sha256(core).hexdigest(); suite.rows=[]; suite.interfaces={}; suite.refusals={}; suite.current_case='setup'; suite.root=WORK
process_cases(suite)
parent_source=raw_parent.decode()
current_source=raw.decode()
parent_tree=ast.parse(parent_source);current_tree=ast.parse(current_source)
def definition(source,tree,name):
    node=next(n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name==name)
    return ast.get_source_segment(source,node)
for name in ['path_rules','guard_read','guard_record','read_record','read_pin','monitor_receipt']:
    suite.case('GUARD_UNCHANGED_'+name,lambda n=name:suite.eq(definition(parent_source,parent_tree,n),definition(current_source,current_tree,n)))
def launch_order():
    n=next(n for n in current_tree.body if isinstance(n,ast.FunctionDef) and n.name=='launch')
    calls=[x for x in ast.walk(n) if isinstance(x,ast.Call)]
    line=lambda name:next(x.lineno for x in calls if isinstance(x.func,ast.Name) and x.func.id==name)
    commit=line('write_launch_commit')
    monitor=next(x.lineno for x in ast.walk(n) if isinstance(x,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='proc' for t in x.targets))
    assert line('run_dry')<line('register_call')<commit<monitor
    assignment=next(x for x in ast.walk(n) if isinstance(x,ast.Assign) and isinstance(x.value,ast.Call) and isinstance(x.value.func,ast.Name) and x.value.func.id=='write_launch_commit')
    assert ast.unparse(assignment.targets[0])=='(plan, plan_pin)'
    return True
suite.case('launch_final_commit_after_dry_before_monitor',launch_order)
for name in ['sampler','launch_resume','saved_residual_plan']:
    source=definition(current_source,current_tree,name)
    required='observe_launch_commit(' if name=='sampler' else 'read_launch_commit('
    suite.case('FINAL_PLAN_CONSUMER_'+name,lambda source=source,required=required:suite.eq(required in source,True))

record=dict(date_u=date,scope='TESTED saved synthetic process rows and static control-flow/unchanged-guard proof; actual launches UNTESTED',parent_sha256=hashlib.sha256(raw).hexdigest(),parent_test_sha256=hashlib.sha256(test).hexdigest(),component_sha256=hashlib.sha256(core).hexdigest(),cases=suite.rows,n_cases=len(suite.rows),n_pass=sum(r['status']=='PASS' for r in suite.rows))
with (WORK/'TEST_RECORD.json').open('xb') as f:f.write((json.dumps(record,sort_keys=True,indent=2)+'\n').encode())
for r in suite.rows:
 if r['status']!='PASS':print(json.dumps(r))
print('%d/%d PASS'%(record['n_pass'],record['n_cases']))
raise SystemExit(0 if record['n_pass']==record['n_cases'] else 1)
