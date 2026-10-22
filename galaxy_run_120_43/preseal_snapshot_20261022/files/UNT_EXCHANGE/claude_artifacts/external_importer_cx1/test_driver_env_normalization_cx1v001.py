"""Execute only extracted environment expressions, never launcher functions."""
import ast, hashlib, json, types, tempfile
from pathlib import Path
A=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
paths=[A/'calibration_orchestrator_c2/v005/campaign_c2v005.py',A/'s1_successors_c2/step4_launcher_c2v015.py',A/'galaxy_m0_forward_c2_0466/root_monitor_c2v001.py']
expected=['d35d5d4a62e6e5b632eb10c59bf4c82c2b1d744f6ceba609399c02baa5ecfeb2',None,'ba031c2340057d88ee399138cc645012a93aa7dc3eb7c9bba56d112c94a47107']
trees=[];pins=[]
for p,h in zip(paths,expected):
 raw=p.read_bytes();sha=hashlib.sha256(raw).hexdigest();assert h is None or sha==h
 trees.append(ast.parse(raw));pins.append({'path':str(p),'sha256':sha})
def globals_for(t):
 out={}
 for n in t.body:
  if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id in ('THREAD_ENV','PY','PYTHON','BLAS') for x in n.targets):
   exec(compile(ast.Module(body=[n],type_ignores=[]),'inert_constants','exec'),out)
 return out
cg,dg,mg=map(globals_for,trees)
def normalizer(t,g):
 assignments=[n for n in ast.walk(t) if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id=='env' for x in n.targets)]
 loops=[n for n in ast.walk(t) if isinstance(n,ast.For) and isinstance(n.iter,ast.Name) and n.iter.id=='THREAD_ENV']
 assert len(assignments)==len(loops)==1
 code=compile(ast.fix_missing_locations(ast.Module(body=[assignments[0],loops[0]],type_ignores=[])),'inert_env','exec')
 def apply(e):
  ns={**g,'os':types.SimpleNamespace(environ=dict(e))};exec(code,ns);return ns['env']
 return apply
campaign=normalizer(trees[0],cg);monitor=normalizer(trees[2],mg)
assert cg['PY']==dg['PYTHON']==mg['PY']
for i in range(128):
 env={'PATH':'/inert/bin','KEEP':'value'+str(i),'PYTHONPATH':'inert','PYTHONOTHER':'inert'}
 for j,k in enumerate(mg['THREAD_ENV']):
  if i & (1<<j):env[k]=str(j+2)
 direct=monitor({**env,**dg['BLAS']});via_campaign=monitor(campaign(env))
 assert direct==via_campaign and direct['KEEP']==env['KEEP']
 assert all(direct[k]=='1' for k in mg['THREAD_ENV'])
 assert not any(k.startswith('PYTHON') for k in direct)
# Different inherited non-PYTHON values remain observable: do not claim full equivalence.
assert monitor({'OTHER':'a'})!=monitor({'OTHER':'b'})
b=Path(tempfile.mkdtemp(prefix='env_',dir=Path(__file__).parent/'inert_fixtures'))
r={'status':'PASS','blocking_count':0,'scope':'Extracted environment transformations only','tested':['128 equal-base environment cases','default interpreter strings equal','non-PYTHON base differences preserved'],'pins':pins,'untested':['Actual process/runtime binary identity','Different inherited environments','Full launcher or monitor execution']}
p=b/'TEST_REPORT.json';p.write_text(json.dumps(r,indent=2)+'\n');print(p)
