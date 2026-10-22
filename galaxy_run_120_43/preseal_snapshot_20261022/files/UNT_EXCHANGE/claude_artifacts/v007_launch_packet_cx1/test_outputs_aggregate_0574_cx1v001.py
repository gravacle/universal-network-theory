"""0574 output and aggregate must-fail tests. Synthetic admission only; no solver/process calls."""
import ast,copy,hashlib,importlib.util,json,runpy,sys,types
from pathlib import Path
R=Path(__file__).parent;sys.path.insert(0,str(R))
import producer_guard_cx1v008 as G
D=R/'OUTPUT_AGGREGATE_0574_SYNTH_V001';D.mkdir();checks=[]
def put(p,o):
 with p.open('x') as f:f.write(o if isinstance(o,str) else json.dumps(o))
 return p
def pin(p):return {'path':str(p),'sha256':hashlib.sha256(Path(p).read_bytes()).hexdigest()}
def check(name,fn,refuse=False):
 try:v=fn();ok=not refuse and v is not False
 except PermissionError:ok=refuse
 except Exception as e:ok=False;print(name,type(e).__name__,str(e))
 checks.append({'name':name,'passed':ok})
reg=json.loads((R/'GUARDED_SUCCESSORS_0574_V001.json').read_bytes())['files']
compare=put(D/'compare.py','# synthetic compare, EA path uses no functions\n')
G.CONFIG=D/'synthetic_config.json';G.REGISTERED=(D/'registered_fake',);G.REGISTERED[0].mkdir()
cfg={'_verified_config_sha256':'1'*64,'seal':{'path':str(D/'seal'),'sha256':'2'*64},'compare':pin(compare),'producer_allowlist':{x['path']:x['sha256'] for x in reg}}
G.admission=lambda *a,**k:cfg;G.SEALED_COMPARE_REF=cfg['compare']
marked=D/'marked';marked.mkdir();put(marked/'start.json',{'call_spec_sha256':G.C5H_SPEC})
uvt=D/'UVT_SYNTHETIC';uvt.mkdir();alias=D/'alias';alias.symlink_to(marked,target_is_directory=True)
paths=[marked/'out.json',uvt/'out.json',G.REGISTERED[0]/'out.json',alias/'out.json']
# Execute each actual source output-check expression, and prove it immediately precedes every exclusive write.
for ref in reg:
 tree=ast.parse(Path(ref['path']).read_bytes());count=0
 for node in ast.walk(tree):
  for field,seq in ast.iter_fields(node):
   if not isinstance(seq,list):continue
   for i,n in enumerate(seq):
    if not isinstance(n,ast.With):continue
    c=n.items[0].context_expr
    if not isinstance(c,ast.Call) or not isinstance(c.func,ast.Name) or c.func.id!='open' or len(c.args)<2 or not isinstance(c.args[1],ast.Constant) or c.args[1].value!='x':continue
    prev=seq[i-1];assert isinstance(prev,ast.Expr) and isinstance(prev.value,ast.Call) and prev.value.func.attr=='check_run_path' and ast.dump(prev.value.args[0])==ast.dump(c.args[0]) and prev.value.keywords[0].arg=='allow_registered' and prev.value.keywords[0].value.value is False
    code=compile(ast.fix_missing_locations(ast.Module(body=[prev],type_ignores=[])),ref['path'],'exec');count+=1
    for j,p in enumerate(paths):check(Path(ref['path']).stem+'_output_'+str(count)+'_'+str(j),lambda p=p,code=code:exec(code,{'_root_guard':G,'out':str(p),'a':types.SimpleNamespace(out=str(p))}),True)
 if count:checks.append({'name':Path(ref['path']).stem+'_all_exclusive_writes_checked','passed':True,'writes':count})
# Real dm4 CLI reproductions, with a wholly synthetic run and real file-exclusive output logic.
run=D/'run';run.mkdir();put(run/'result.json',{})
for j,p in enumerate(paths):
 sys.argv=['dm4',str(run),'SYNTHETIC',str(p)]
 check('real_dm4_cli_forbidden_output_'+str(j),lambda:runpy.run_path(str(R/'dm4_report_cx1v008.py'),run_name='__main__'),True)
 assert not p.exists()
# Real aggregate main: forged/unstamped/unadmitted producer inputs must refuse before output.
spec=importlib.util.spec_from_file_location('aggtest',R/'aggregate_records_cx1v008.py');M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
base={'schema':'SYNTHETIC','producer':pin(R/'ea_replay_cx1v012.py'),'per_case':{'C5H':{'label':'SYNTHETIC'}}};base=G.stamp(base,__file__)
for label,mutate in [('unstamped',lambda x:x.pop('root_admission')),('forged_config',lambda x:x['root_admission']['config'].update(sha256='9'*64)),('forged_seal',lambda x:x['root_admission']['seal'].update(sha256='9'*64)),('forged_compare',lambda x:x['root_admission']['compare'].update(sha256='9'*64)),('no_producer',lambda x:x.pop('producer')),('forged_producer',lambda x:x['producer'].update(sha256='9'*64)),('unadmitted_producer',lambda x:x.update(producer=pin(compare))),('valid',lambda x:None)]:
 obj=copy.deepcopy(base);mutate(obj);p=put(D/(label+'.json'),obj);mp=put(D/(label+'_manifest.json'),{'C5H':pin(p)});out=D/(label+'_aggregate.json');sys.argv=['aggregate','EA',str(mp),str(out)]
 check('real_aggregate_'+label,M.main,label!='valid');assert out.exists()==(label=='valid')
 if label=='valid':assert json.loads(out.read_bytes())['root_admission']==G.provenance(__file__)
with (R/'OUTPUT_AGGREGATE_0574_TESTS_V001.json').open('x') as f:json.dump({'label':'TESTED synthetic admission only; actual dm4 CLI and aggregate main; every writer check expression exercised; no numerical replay','tests':checks},f,indent=1)
print(sum(x['passed'] for x in checks),len(checks));assert all(x['passed'] for x in checks)
