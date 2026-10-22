"""Independent 0625 boundary reproductions. No scientific subprocess or actual protected path probe."""
import ast,builtins,copy,hashlib,importlib,importlib.util,importlib.machinery,importlib._bootstrap_external,json,marshal,os,re,stat,sys,types
from pathlib import Path
from unittest.mock import patch
R=Path(__file__).resolve().parent;I=R.parent/'impl';OUT=R/'BOUNDARY_INDEPENDENT_V001';OUT.mkdir()
checks=[];citations={};events=[]
def digest(b):return hashlib.sha256(b).hexdigest()
def cite(p):
 p=Path(p);b=p.read_bytes();citations[str(p)]=digest(b);return b
def put(name,b):
 p=OUT/name;p.parent.mkdir(parents=True,exist_ok=True)
 if isinstance(b,str):b=b.encode()
 with p.open('xb') as f:f.write(b)
 return p
def check(name,fn,exception=None):
 try:
  v=fn();ok=exception is None and v is not False;detail=repr(v)[:240]
 except BaseException as e:ok=exception is not None and exception in str(e);detail=type(e).__name__+': '+str(e)
 checks.append({'name':name,'passed':ok,'detail':detail})
def module(path,name):
 data=cite(path);m=types.ModuleType(name);m.__file__=str(path);exec(compile(data,str(path),'exec'),m.__dict__);return m
G=module(I/'step4_guard_cx1v006.py','independent_guard');B=module(I/'step4_bind_cx1v005.py','independent_binder')
# Exact metadata ordering. All test paths are virtual; spies prevent any real probe.
for path in ('/virtual/UVT_DEMONSTRATION/result.json','/virtual/KMAX_A2F10_C5H_RUN_V001/result.json','/virtual/NGC3198_observed.csv','/virtual/uvt_lower/../safe'):
 probes=[]
 def forbidden(*a,**k):probes.append(repr(a));raise AssertionError('ANY_METADATA_BEFORE_LEXICAL_REJECTION')
 with patch.object(os,'lstat',forbidden),patch.object(os,'stat',forbidden),patch.object(os,'readlink',forbidden),patch.object(Path,'resolve',forbidden):
  check('lexical refusal '+path,lambda:G.safe_path(path),'PROTECTED_PATH_REFUSED')
 check('zero metadata '+path,lambda:probes==[])
for target in ('/virtual/UVT_DEMONSTRATION/child','../UVT_DEMONSTRATION/child','/virtual/KMAX_A2F10_C5H_RUN_V001/child','/virtual/NGC3198_observed.csv'):
 probes=[]
 def lstat(p):
  p=str(p);probes.append(('lstat',p));assert not any(x in p.casefold() for x in ('uvt_','ngc3198','kmax_a2f10_c5h_run_v001'))
  return types.SimpleNamespace(st_mode=stat.S_IFLNK if p=='/virtual/alias' else stat.S_IFDIR)
 def readlink(p):probes.append(('readlink',str(p)));assert str(p)=='/virtual/alias';return target
 with patch.object(os,'lstat',lstat),patch.object(os,'readlink',readlink),patch.object(Path,'resolve',side_effect=AssertionError('resolve used')):
  check('symlink refusal '+target,lambda:G.safe_path('/virtual/alias/result'),'PROTECTED_PATH_REFUSED')
 check('symlink stops at alias '+target,lambda:probes==[('lstat','/virtual'),('lstat','/virtual/alias'),('readlink','/virtual/alias')])
with patch.object(os,'lstat',return_value=types.SimpleNamespace(st_mode=stat.S_IFDIR)):
 check('frozen metadata exception only',lambda:str(G.safe_path('/virtual/ROOT_DECISIONS_NGC3198_CONSTRUCTION_V001.md')).endswith('.md'))
 check('metadata exception does not permit protected parent',lambda:G.safe_path('/virtual/NGC3198/ROOT_DECISIONS_NGC3198_CONSTRUCTION_V001.md'),'PROTECTED_PATH_REFUSED')
# Entire binder and launcher module bootstraps against an inert wrong adjacent guard.
for name in ('step4_bind_cx1v005.py','step4_launcher_cx1v006.py'):
 src=cite(I/name);d=OUT/('boot_'+name[:-3]);d.mkdir();p=d/name
 with p.open('xb') as f:f.write(src)
 with (d/'step4_guard_cx1v006.py').open('xb') as f:f.write(b'import builtins\nbuiltins._independent_sentinel.append("EXECUTED")\n')
 with patch.object(builtins,'_independent_sentinel',[],create=True) as sentinel:
  check('bootstrap hash before exec '+name,lambda:module(p,'inert_boot'),'GUARD_BOOTSTRAP_HASH_MISMATCH')
  check('no unchecked guard execution '+name,lambda:sentinel==[])
# Use complete synthetic fixture through actual validator, then late virtual rewrite.
F=I/'tests/SYNTH_V005';plan_path=F/'001plan.json';plan_bytes=cite(plan_path);plan=json.loads(plan_bytes)
cfg=json.loads(cite(F/'001admission.json'));cfg['plan']=None;candidate=put('candidate.json',json.dumps(cfg,sort_keys=True).encode())
original_raw=B.G.raw;original_validate=B.G.validate;trace=[];state={'validated':False}
changed=copy.deepcopy(plan);changed['calls'][0]['wall_cap_s']+=999;changed_bytes=json.dumps(changed,sort_keys=True).encode()
def raw(path):
 if str(path)==str(plan_path):trace.append(('read',state['validated']));return changed_bytes if state['validated'] else plan_bytes
 return original_raw(path)
def validate(ref,producer,**kw):
 trace.append(('validate_buffer',digest(kw['_plan_bytes'])));result=original_validate(ref,producer,**kw);state['validated']=True;return result
with patch.object(B.G,'raw',raw),patch.object(B.G,'validate',validate):
 check('binder actual full synthetic validation',lambda:B.bind(plan_path,candidate,OUT/'BOUND_PLAN.json',OUT/'BOUND_ADMISSION.json',OUT/'COMMAND.sh')['plan']['sha256']==digest(plan_bytes))
check('binder validated snapshot is emitted',lambda:(OUT/'BOUND_PLAN.json').read_bytes()==plan_bytes)
check('binder no late plan read',lambda:trace==[('read',False),('validate_buffer',digest(plan_bytes))])
probe=copy.deepcopy(cfg);probe['plan']={'path':str(plan_path),'sha256':digest(plan_bytes)}
check('guard rejects different snapshot',lambda:G.validate(probe['plan'],plan['launcher']['path'],_candidate_config=probe,_plan_bytes=changed_bytes),'PLAN_SNAPSHOT_HASH_MISMATCH')
# Exact native helper functions, AST extracted without campaign imports/constructor.
O=I.parents[1]/'calibration_orchestrator_c2/v005/calibration_orchestrator_c2v005.py';odata=cite(O)
names={'load_pinned_module','read_pinned','sha256_file','sha256_bytes'}
nodes=[n for n in ast.parse(odata).body if isinstance(n,ast.FunctionDef) and n.name in names]
assert {n.name for n in nodes}==names
native={'Path':Path,'hashlib':hashlib,'importlib':importlib,'OrchestratorError':ValueError,'re':re}
exec(compile(ast.Module(body=nodes,type_ignores=[]),str(O),'exec'),native)
old_get_code=importlib.machinery.SourceFileLoader.get_code
open_events=[];watch={'on':False}
def watcher(event,args):
 if watch['on'] and event=='open' and isinstance(args[0],(str,bytes,os.PathLike)):open_events.append(os.fsdecode(args[0]))
sys.addaudithook(watcher)
for cached in (False,True):
 p=put('loader_'+str(cached)+'.py','VALUE="VERIFIED_SOURCE"\n');ref={'path':str(p),'sha256':digest(p.read_bytes())}
 if cached:
  cache=Path(importlib.util.cache_from_source(str(p)));cache.parent.mkdir(exist_ok=True)
  payload=compile('VALUE="UNTRUSTED_CACHE"\n',str(p),'exec')
  st=p.stat();pyc=importlib.util.MAGIC_NUMBER+(0).to_bytes(4,'little')+int(st.st_mtime).to_bytes(4,'little')+st.st_size.to_bytes(4,'little')+marshal.dumps(payload)
  with cache.open('xb') as f:f.write(pyc)
  check('poison cache eligible without fence',lambda:native['load_pinned_module'](ref,'cache_baseline','inert').VALUE=='UNTRUSTED_CACHE')
 open_events.clear();watch['on']=True
 try:
  with G.fence({str(p):ref['sha256']}):
   check('actual native loader cache='+str(cached),lambda:native['load_pinned_module'](ref,'real_native_'+str(cached),'inert').VALUE=='VERIFIED_SOURCE')
 finally:watch['on']=False
 check('no cache open cache='+str(cached),lambda:not any(x.endswith('.pyc') for x in open_events))
 check('loader hook restored cache='+str(cached),lambda:importlib.machinery.SourceFileLoader.get_code is old_get_code)
 with G.fence({str(p):ref['sha256']}):
  check('direct altered compile buffer cache='+str(cached),lambda:compile(b'VALUE="ALTERED"\n',str(p),'exec'),'PREFLIGHT_COMPILE_HASH_MISMATCH')
 # Change the actual buffer at compile after production verify has returned.
 realcompile=builtins.compile;mutation={'hit':False}
 def mutate(source,filename,*a,**kw):
  if str(filename)==str(p) and isinstance(source,bytes):source=b'VALUE="LATE_CHANGED"\n';mutation['hit']=True
  return realcompile(source,filename,*a,**kw)
 with G.fence({str(p):ref['sha256']}),patch.object(builtins,'compile',mutate):
  check('native actual compile-time change cache='+str(cached),lambda:native['load_pinned_module'](ref,'mutation_'+str(cached),'inert'),'PREFLIGHT_COMPILE_HASH_MISMATCH')
 check('compile mutation seam reached cache='+str(cached),lambda:mutation['hit'])
 check('hook restored after compile refusal cache='+str(cached),lambda:importlib.machinery.SourceFileLoader.get_code is old_get_code)
# Real nested loader executes only listed sources; unlisted child refuses.
child=put('child.py','VALUE=17\n');childref={'path':str(child),'sha256':digest(child.read_bytes())}
parent=put('parent.py','import importlib.util\ns=importlib.util.spec_from_file_location("nested_owned",'+repr(str(child))+')\nm=importlib.util.module_from_spec(s)\ns.loader.exec_module(m)\nVALUE=m.VALUE\n');parentref={'path':str(parent),'sha256':digest(parent.read_bytes())}
with G.fence({str(child):childref['sha256'],str(parent):parentref['sha256']}):
 check('actual transitive listed loader',lambda:native['load_pinned_module'](parentref,'transitive_owned','inert').VALUE==17)
with G.fence({str(parent):parentref['sha256']}):
 check('actual transitive unlisted loader',lambda:native['load_pinned_module'](parentref,'transitive_unlisted','inert'),'UNPINNED_PREFLIGHT_SOURCE')
cite(__file__)
report={'status':'TESTED','scope':'Independent inert controls; actual native SourceFileLoader used; synthetic full binder validation; no scientific subprocess; no actual protected metadata access.','checks':checks,'passed':sum(c['passed'] for c in checks),'total':len(checks),'citations':citations,'limitations':['Production adoption/certificates not exercised.','Lifecycle separate.','Synthetic binder uses expressly mocked scientific providers from SYNTH_V005.']}
with (OUT/'RESULTS.json').open('x') as f:json.dump(report,f,indent=2)
print(json.dumps({'passed':report['passed'],'total':report['total'],'failures':[c for c in checks if not c['passed']],'results_sha256':digest((OUT/'RESULTS.json').read_bytes())}))
raise SystemExit(0 if report['passed']==report['total'] else 1)
