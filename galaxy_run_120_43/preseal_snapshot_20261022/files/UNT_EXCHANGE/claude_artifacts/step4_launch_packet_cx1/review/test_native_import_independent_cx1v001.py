"""Native source-only import and exact generated compile binding; never construct Context/campaign."""
import ast,hashlib,importlib.util,importlib.machinery,json,os,sys,types
from pathlib import Path
from unittest.mock import patch
R=Path(__file__).resolve().parent;I=R.parent/'impl';OUT=R/'NATIVE_IMPORT_INDEPENDENT_V001';OUT.mkdir();checks=[];pins={}
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):b=Path(p).read_bytes();pins[str(p)]=sha(b);return b
def check(name,fn,exception=None):
 try:v=fn();ok=exception is None and v is not False;detail=repr(v)[:200]
 except BaseException as e:ok=exception is not None and exception in str(e);detail=type(e).__name__+': '+str(e)
 checks.append({'name':name,'passed':ok,'detail':detail})
gp=I/'step4_guard_cx1v007.py';G=types.ModuleType('native_review_guard');G.__file__=str(gp);exec(compile(read(gp),str(gp),'exec'),G.__dict__)
base=I.parents[1]
paths=[base/x for x in ['calib_tail_readiness_cx2/v006r9/calibration_orchestrator_cx2v006r9.py','calib_tail_readiness_cx2/v006r9/calibration_core_cx2v006r9.py','calibration_orchestrator_c2/v005/calibration_orchestrator_c2v005.py','calib_tail_readiness_cx2/v006r8/sensitivity_policy_cx2v006r8_v002.py','calib_tail_readiness_cx2/certificates_per_point/certificate_guard_cx2v003.py']]
source_bytes={str(p):read(p) for p in paths};sources={p:sha(b) for p,b in source_bytes.items()};wrapper=paths[0];tree=ast.parse(source_bytes[str(wrapper)])
assignment=next(n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='_resolve_source' for t in n.targets));snippet=ast.literal_eval(assignment.value)
check('known generated fragment exact SHA',lambda:sha(snippet.encode())=='79e8936d96103b1540987a980b289b6d25e5e25941b02db647f7a833818da0e1')
check('native callsite exact compile filename',lambda:any(isinstance(n,ast.Expr) and ast.unparse(n)=="exec(compile(_resolve_source, __file__, 'exec'), O.__dict__)" for n in tree.body))
# Independent extra safety audit: native import may read only the five audited Research sources.
watch={'active':False};observed={'opens':[],'process_attempts':[],'protected_metadata_attempts':[]};original_get_code=importlib.machinery.SourceFileLoader.get_code
canonical_sources={str(Path(p).resolve()) for p in sources}
def lexical(p):
 if not isinstance(p,(str,bytes,os.PathLike)):return
 s=os.fsdecode(p)
 if any(x.casefold().startswith('uvt_') or x.casefold()=='kmax_a2f10_c5h_run_v001' or 'ngc3198' in x.casefold() for x in Path(s).parts):
  observed['protected_metadata_attempts'].append(s);raise AssertionError('PROTECTED_METADATA_PREVENTED')
def audit(event,args):
 if not watch['active']:return
 if event in ('subprocess.Popen','os.system','os.fork','os.posix_spawn','os.exec','socket.connect','socket.bind'):
  observed['process_attempts'].append(event);raise AssertionError('NATIVE_IMPORT_PROCESS_PREVENTED')
 if event=='open' and isinstance(args[0],(str,bytes,os.PathLike)):
  p=os.path.abspath(os.fsdecode(args[0]));lexical(p)
  if '/Research/' in p:
   observed['opens'].append(p)
   if p not in sources and p not in canonical_sources:raise AssertionError('UNEXPECTED_RESEARCH_READ')
sys.addaudithook(audit)
original_stat=os.stat;original_lstat=os.lstat;original_readlink=os.readlink
# These wrappers check lexically BEFORE delegating to real metadata operations.
def meta(original):
 def f(p,*a,**kw):lexical(p);return original(p,*a,**kw)
 return f
loaded={}
def import_native():
 m=G.load({'path':str(wrapper),'sha256':sources[str(wrapper)]},{'sources':sources},'independent_actual_native_wrapper');loaded['module']=m
 return m.Context.__module__=='independent_actual_native_wrapper' and callable(m.O.resolve) and m.O.resolve.__code__.co_filename==str(wrapper)
watch['active']=True
try:
 with patch.object(os,'stat',meta(original_stat)),patch.object(os,'lstat',meta(original_lstat)),patch.object(os,'readlink',meta(original_readlink)),G.fence(sources):
  check('actual complete native wrapper import',import_native)
finally:watch['active']=False
check('native import read only five audited sources',lambda:set(observed['opens'])<=set(sources)|canonical_sources and len(set(observed['opens']))==5)
check('native import no process attempt',lambda:observed['process_attempts']==[])
check('native import no protected metadata attempt',lambda:observed['protected_metadata_attempts']==[])
check('loader restored after native import',lambda:importlib.machinery.SourceFileLoader.get_code is original_get_code)
with G.fence(sources):
 check('exact generated snippet compile allowed',lambda:isinstance(compile(snippet,str(wrapper),'exec'),types.CodeType))
 check('one-byte generated change refuses',lambda:compile(snippet+'\n',str(wrapper),'exec'),'PREFLIGHT_COMPILE_HASH_MISMATCH')
with G.fence({str(wrapper):'0'*64}):
 check('generated snippet wrong owner pin refuses',lambda:compile(snippet,str(wrapper),'exec'),'PREFLIGHT_COMPILE_HASH_MISMATCH')
with G.fence({}):
 check('generated snippet unregistered owner refuses',lambda:compile(snippet,str(wrapper),'exec'),'PREFLIGHT_COMPILE_HASH_MISMATCH')
# Identical generated text under a different pinned owner is not admitted.
other=OUT/'other.py'
with other.open('xb') as f:f.write(b'VALUE=1\n')
with G.fence({str(other):sha(other.read_bytes())}):
 check('generated snippet unrelated owner refuses',lambda:compile(snippet,str(other),'exec'),'PREFLIGHT_COMPILE_HASH_MISMATCH')
# Fault inject owner-byte read at compile point; disk source is never changed.
real_read_bytes=Path.read_bytes;fresh={'reads':0}
def changed_owner(p):
 if str(p)==str(wrapper):fresh['reads']+=1;return source_bytes[str(wrapper)]+b'\n'
 return real_read_bytes(p)
with G.fence(sources),patch.object(Path,'read_bytes',changed_owner):
 check('generated compile rechecks actual owner bytes',lambda:compile(snippet,str(wrapper),'exec'),'PIN_BYTES_CHANGED')
check('fresh owner read actually reached',lambda:fresh['reads']>0)
# All registered paths must be protected, even outside /Research: virtual source read,
# real loader class. Bytes are injected at owned virtual filename; no filesystem write.
external='/private/tmp/independent_registered_source_no_file.py';good=b'VALUE="GOOD"\n';bad=b'VALUE="CHANGED"\n'
def injected(p):return good if str(p)==external else real_read_bytes(p)
def imported_external():
 sp=importlib.util.spec_from_file_location('owned_registered_external',external);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m.VALUE=='GOOD'
with G.fence({external:sha(good)}),patch.object(Path,'read_bytes',injected):
 check('registered outside Research real loader',imported_external)
 check('registered outside Research wrong compile rejects',lambda:compile(bad,external,'exec'),'PREFLIGHT_COMPILE_HASH_MISMATCH')
cache=importlib.util.cache_from_source(external)
with G.fence({external:sha(good)}):
 check('registered outside Research pyc read refuses',lambda:open(cache,'rb'),'UNPINNED_PREFLIGHT_SOURCE')
check('final loader restored',lambda:importlib.machinery.SourceFileLoader.get_code is original_get_code)
read(__file__)
report={'status':'TESTED','scope':'Actual five-source native wrapper import completed without Context/campaign construction or scientific methods. Exact generated-code custody controls and outside-Research registered-source loader.','checks':checks,'passed':sum(x['passed'] for x in checks),'total':len(checks),'observed':observed,'sources':sources,'sha256_from_bytes':pins,'limitations':['Production admission/adoption/certificates/sensitivity still UNTESTED.','No native Context or scientific monitor was constructed.','No scientific process, target data or actual protected path metadata access.']}
with (OUT/'RESULTS.json').open('x') as f:json.dump(report,f,indent=2)
print(json.dumps({'passed':report['passed'],'total':report['total'],'failures':[x for x in checks if not x['passed']],'results_sha256':sha((OUT/'RESULTS.json').read_bytes())}))
raise SystemExit(0 if report['passed']==report['total'] else 1)
