"""Actual import-only native closure plus exact generated/source-alias custody controls.
No Context is instantiated, no data/configuration is loaded, no process starts.
"""
import ast,builtins,hashlib,importlib.util,importlib.machinery,json,keyword,os,sys,types
from pathlib import Path
from unittest.mock import patch
I=Path(__file__).resolve().parent.parent;OUT=I/'tests/NATIVE_IMPORT_V001';OUT.mkdir()
sp=importlib.util.spec_from_file_location('nativeG',I/'step4_guard_cx1v007.py');G=importlib.util.module_from_spec(sp);sp.loader.exec_module(G)
ART=I.parents[1]
refs={
 'calib_tail_readiness_cx2/v006r9/calibration_orchestrator_cx2v006r9.py':'24abe3bc4f6ee0e3c5d7c89502062cf99464573b35bc5b53c33c14ef2ae888af',
 'calib_tail_readiness_cx2/v006r9/calibration_core_cx2v006r9.py':'a595c5c0929fc0a8313bcdff3b79241f1e3ba8f77dc3749adc06b2a982b43605',
 'calibration_orchestrator_c2/v005/calibration_orchestrator_c2v005.py':'c75a889ff4646a816329756124a19532cbc166d26f47ce2ea5147b71c2cf7c4d',
 'calib_tail_readiness_cx2/v006r8/sensitivity_policy_cx2v006r8_v002.py':'8fb0660077d56ddc787ac67386f8def72e6f5a04fd14e44eb20ed9facf19de4f',
 'calib_tail_readiness_cx2/certificates_per_point/certificate_guard_cx2v003.py':'5f1e49e689a859c003b137c45c07f887423443ef2c726182616b41bf290c9c2f'}
sources={str(ART/k):v for k,v in refs.items()};wrapper=next(iter(sources));owner=sources[wrapper]
checks=[]
def check(name,fn,err=None):
 try:v=fn();ok=err is None and v is not False;detail=repr(v)[:160]
 except BaseException as e:ok=err is not None and err in str(e);detail=type(e).__name__+': '+str(e)
 checks.append({'name':name,'passed':ok,'detail':detail})
for path,h in sources.items():check('native_pin_'+Path(path).name,lambda path=path,h=h:hashlib.sha256(G.raw(path)).hexdigest()==h)
wrapper_bytes=G.verify({'path':wrapper,'sha256':owner});tree=ast.parse(wrapper_bytes)
assign=next(n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='_resolve_source' for t in n.targets))
snippet=ast.literal_eval(assign.value)
check('reviewed_literal_digest',lambda:G.GENERATED_COMPILE_CONTRACT=={owner:frozenset({hashlib.sha256(snippet.encode()).hexdigest()})})
check('exact_generated_call_site',lambda:sum(1 for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='compile' and len(n.args)==3 and isinstance(n.args[0],ast.Name) and n.args[0].id=='_resolve_source' and isinstance(n.args[1],ast.Name) and n.args[1].id=='__file__' and isinstance(n.args[2],ast.Constant) and n.args[2].value=='exec')==1)
# Independent audit adds a data-deny boundary on all Research reads, not merely
# source suffixes. It records any attempted scientific process separately.
watch={'active':False,'reads':set(),'processes':0,'unlisted_reads':0}
def watch_import(event,args):
 if not watch['active']:return
 if event in ('subprocess.Popen','os.system','os.fork','os.forkpty','os.posix_spawn','os.exec','socket.connect','socket.bind'):
  watch['processes']+=1;raise AssertionError('NO_PROCESS_OR_NETWORK')
 if event=='open' and isinstance(args[0],(str,bytes,os.PathLike)):
  p=str(G.safe_path(os.path.abspath(os.fsdecode(args[0]))))
  if '/Research/' in p:
   if p not in sources:watch['unlisted_reads']+=1;raise AssertionError('UNLISTED_RESEARCH_DATA')
   watch['reads'].add(p)
sys.addaudithook(watch_import)
result={}
def import_actual():
 watch['active']=True
 try:
  with G.fence(sources):result['module']=G.load({'path':wrapper,'sha256':owner},{'sources':sources},'_builder_actual_native_wrapper')
 finally:watch['active']=False
 return isinstance(result['module'],types.ModuleType)
check('actual_native_wrapper_import',import_actual)
check('all_five_sources_read',lambda:watch['reads']==set(sources))
check('no_unlisted_research_data',lambda:watch['unlisted_reads']==0)
check('zero_process_or_network',lambda:watch['processes']==0)
check('native_generated_function_installed',lambda:result['module'].O.CampaignExecutor.resolve.__code__.co_filename==wrapper)
with G.fence(sources):
 check('exact_generated_buffer_accepted',lambda:isinstance(compile(snippet,wrapper,'exec'),types.CodeType))
 check('changed_generated_buffer_refused',lambda:compile(snippet+'\n# changed\n',wrapper,'exec'),'PREFLIGHT_COMPILE_HASH_MISMATCH')
 other=next(p for p in sources if p!=wrapper)
 check('wrong_owner_refused',lambda:compile(snippet,other,'exec'),'PREFLIGHT_COMPILE_HASH_MISMATCH')
 original=G.raw;reads=[]
 def changed_owner(path):
  if str(path)==wrapper:reads.append(str(path));return wrapper_bytes+b'\n# late source mutation\n'
  return original(path)
 with patch.object(G,'raw',changed_owner):check('fresh_owner_bytes_required',lambda:compile(snippet,wrapper,'exec'),'PIN_BYTES_CHANGED')
 check('owner_rechecked_at_use',lambda:reads==[wrapper])
with G.fence({}):check('unregistered_owner_refused',lambda:compile(snippet,wrapper,'exec'),'PREFLIGHT_COMPILE_HASH_MISMATCH')
# A real runtime stdlib source is outside Research. Pin it read-only, force the
# original loader to fail if called, and prove the exact source override operates.
external=Path(keyword.__file__);external_ref=G.pin(external)
check('outside_research_fixture',lambda:'/Research/' not in str(external))
def real_loader(path,name):
 sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
def forbidden_loader(*args):raise AssertionError('CACHED_LOADER_CALLED')
with patch.object(importlib.machinery.SourceFileLoader,'get_code',forbidden_loader):
 with G.fence({external_ref['path']:external_ref['sha256']}):
  check('outside_registered_real_loader',lambda:real_loader(external,'_owned_keyword').iskeyword('while'))
  check('outside_changed_compile_refused',lambda:compile(b'VALUE="unverified"\n',str(external),'exec'),'PREFLIGHT_COMPILE_HASH_MISMATCH')
  cache=importlib.util.cache_from_source(str(external))
  check('outside_registered_cache_open_refused',lambda:open(cache,'rb'),'UNPINNED_PREFLIGHT_SOURCE')
  check('outside_registered_legacy_cache_refused',lambda:open(str(external)+'c','rb'),'UNPINNED_PREFLIGHT_SOURCE')
check('loader_restored',lambda:importlib.machinery.SourceFileLoader.get_code.__name__=='get_code')
# Immutable owned aliases exercise canonical source membership exactly as legacy
# Research symlinks do, with no relaxed protected-path allowance.
owned=OUT/'owned_source.py'
with owned.open('x') as f:f.write('VALUE="owned verified alias"\n')
alias=OUT/'owned_alias.py';alias.symlink_to(owned.name);h=G.sha(owned)
with G.fence({str(alias):h}):
 check('alias_registered_source_loader',lambda:real_loader(alias,'_owned_alias').VALUE=='owned verified alias')
 check('alias_canonical_map',lambda:G.FENCE_SOURCES=={str(owned):h})
 check('alias_changed_compile_refused',lambda:compile(b'VALUE="changed"\n',str(alias),'exec'),'PREFLIGHT_COMPILE_HASH_MISMATCH')
def conflict():
 with G.fence({str(alias):h,str(owned):'0'*64}):return False
check('alias_conflicting_hash_refused',conflict,'ALIASED_SOURCE_HASH_CONFLICT')
probes=[]
def no_probe(*args,**kw):probes.append(args);raise AssertionError('METADATA_PROBE')
def forbidden_mapping():
 with G.fence({'/private/tmp/UVT_virtual_block/source.py':'0'*64}):return False
with patch.object(os,'lstat',no_probe),patch.object(os,'readlink',no_probe):check('mapping_lexical_refusal',forbidden_mapping,'PROTECTED_PATH_REFUSED')
check('mapping_zero_protected_probes',lambda:probes==[])
report={'status':'TESTED','passed':sum(x['passed'] for x in checks),'total':len(checks),'checks':checks,'native_sources':sources,'implementation':G.pin(I/'step4_guard_cx1v007.py'),'scientific_processes':0,'native_context_constructed':False,'production_adoption_certificate_sensitivity':'UNTESTED'}
with (OUT/'RESULTS.json').open('x') as f:json.dump(report,f,sort_keys=True,indent=2)
print(json.dumps({'passed':report['passed'],'total':report['total'],'failed':[x for x in checks if not x['passed']]}))
raise SystemExit(0 if report['passed']==report['total'] else 1)
