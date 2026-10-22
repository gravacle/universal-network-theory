import ast,copy,hashlib,importlib.util,json,marshal,os,struct,subprocess,sys,types
from pathlib import Path
sha=lambda b:hashlib.sha256(b).hexdigest()
base=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1');out=base/'runner003_controls_v001';out.mkdir();guarded=out/'guarded';guarded.mkdir();external=out/'guarded_sibling';external.mkdir()
p=base/'selected_runner003_snapshot_v001/runner.py';src=p.read_bytes();assert sha(src)=='2b040e94a2b74eae981485288471376b86be0784a0a50b59093312c4fd87bf73'
op=base/'provisional_snapshot_v002/run_pinned_c3sa_c3v002.py';old=op.read_bytes();assert sha(old)=='b57e4859c498bf57e05706dcd83d89db0f14102c33aec7359580c155d924861c'
ns={'__name__':'inert_runner003_review','__file__':str(p)};exec(compile(src,str(p),'exec'),ns)
fixtures=[]
def put(path,buf):
 b=buf.encode() if isinstance(buf,str) else buf
 with path.open('xb') as f:f.write(b)
 fixtures.append({'path':str(path),'sha256':sha(b)});return path,sha(b)
def stale_cache(path,source):
 cache=Path(importlib.util.cache_from_source(str(path)));cache.parent.mkdir(exist_ok=True);st=path.stat();b=importlib.util.MAGIC_NUMBER+struct.pack('<III',0,int(st.st_mtime),st.st_size)+marshal.dumps(compile(source,str(path),'exec'));put(cache,b)
checks=[]
def ck(name,ok,detail=None):checks.append({'id':name,'passed':bool(ok),'detail':detail})
def run(args):
 modules=set(sys.modules);meta=list(sys.meta_path);argv=list(sys.argv);paths=list(sys.path)
 try:return {'return':ns['run'](args)}
 except Exception as e:return {'exception':type(e).__name__,'message':str(e)}
 finally:
  sys.meta_path[:]=meta;sys.argv[:]=argv;sys.path[:]=paths
  for n in list(set(sys.modules)-modules):
   if n.startswith('unt_review_'):del sys.modules[n]
def main_args(path,h):return ['--main',str(path)+'='+h,'--call','main','--']
def refused(r):return r.get('exception')=='ImportError' and r.get('message','').startswith('UNPINNED_SIBLING_IMPORT_REFUSED')
# Exact package-form regression from runner002: payload would return41 if the import executed.
pkg=guarded/'unt_review_package';pkg.mkdir();put(pkg/'__init__.py','MARKER=41\n')
mp,mh=put(guarded/'main_unpinned_package.py',"import sys\nsys.path.insert(0,"+repr(str(guarded))+")\nimport unt_review_package\ndef main(args): return unt_review_package.MARKER\n")
r=run(main_args(mp,mh));ck('N1_exact_sibling_package_refuses',refused(r),r)
# Namespace package has no __init__.py and spec.origin=None; search locations must carry the guard.
nsp=guarded/'unt_review_namespace';nsp.mkdir();put(nsp/'leaf.py','MARKER=43\n')
mp,mh=put(guarded/'main_unpinned_namespace.py',"import sys\nsys.path.insert(0,"+repr(str(guarded))+")\nimport unt_review_namespace.leaf\ndef main(args): return unt_review_namespace.leaf.MARKER\n")
r=run(main_args(mp,mh));ck('namespace_sibling_package_refuses',refused(r),r)
common,ch=put(guarded/'unt_review_common.py',"MARKER='PINNED_SOURCE'\n");stale_cache(common,"MARKER='UNPINNED_BYTECODE'\n")
mp,mh=put(guarded/'main_pinned.py',"import unt_review_common\ndef main(args): return 0 if unt_review_common.MARKER=='PINNED_SOURCE' else 17\n")
r=run(['--module','unt_review_common='+str(common)+'='+ch]+main_args(mp,mh));ck('pinned_sibling_source_overrides_stale_pyc',r=={'return':0},r)
put(guarded/'unt_review_unpinned.py','MARKER=37\n');mp,mh=put(guarded/'main_unpinned_flat.py',"import sys\nsys.path.insert(0,"+repr(str(guarded))+")\nimport unt_review_unpinned\ndef main(args): return unt_review_unpinned.MARKER\n")
r=run(main_args(mp,mh));ck('flat_unpinned_sibling_refuses',refused(r),r)
# Shares a string prefix with the guarded directory but is not a descendant.
put(external/'unt_review_external.py','MARKER=29\n');mp,mh=put(guarded/'main_external.py',"import sys\nsys.path.insert(0,"+repr(str(external))+")\nimport unt_review_external\ndef main(args): return unt_review_external.MARKER\n")
r=run(main_args(mp,mh));ck('safe_external_sibling_prefix_import_allowed',r=={'return':29},r)
mp,mh=put(guarded/'main_stdlib.py','import calendar\ndef main(args): return calendar.Calendar().firstweekday\n');was_loaded='calendar' in sys.modules;r=run(main_args(mp,mh));ck('stdlib_import_allowed',r=={'return':0} and not was_loaded,{'result':r,'calendar_preloaded':was_loaded})
ck('priority_nice10',os.getpriority(os.PRIO_PROCESS,0)>=10)
# Exact AST delta: removing find_spec from both modules leaves identical syntax trees.
def strip_find(raw):
 t=ast.parse(raw)
 for n in t.body:
  if isinstance(n,ast.ClassDef) and n.name=='UnpinnedSiblingGuard':n.body=[x for x in n.body if not(isinstance(x,ast.FunctionDef) and x.name=='find_spec')]
 return ast.dump(t,include_attributes=False)
ck('only_find_spec_AST_changes',strip_find(old)==strip_find(src))
result={'date_u':subprocess.check_output(['/bin/date','-u'],text=True).strip(),'label':'TESTED_SELECTED_RUNNER003_N1_DELTA','source':{'path':str(p),'sha256':sha(src)},'previous_source':{'path':str(op),'sha256':sha(old)},'harness':{'path':__file__,'sha256':sha(Path(__file__).read_bytes())},'checks':checks,'passed':sum(x['passed'] for x in checks),'total':len(checks),'fixtures':fixtures,'scope':'N1 changed method only. Exact pinned source buffers and inert payloads. No real script/comparator/scientific execution, protected metadata or network. Does not certify arbitrary concurrent filesystem mutation or every Python import mechanism.'}
rp=out/'RESULTS.json'
with rp.open('x') as f:json.dump(result,f,indent=2,sort_keys=True);f.write('\n')
print(json.dumps({'path':str(rp),'sha256':sha(rp.read_bytes()),'passed':result['passed'],'total':result['total'],'failures':[x for x in checks if not x['passed']]}))
