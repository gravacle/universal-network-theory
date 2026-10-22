import hashlib,importlib.util,json,marshal,os,struct,subprocess,sys,types
from pathlib import Path
sha=lambda b:hashlib.sha256(b).hexdigest()
base=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1');out=base/'runner002_controls_v001';out.mkdir()
p=base/'provisional_snapshot_v002/run_pinned_c3sa_c3v002.py';src=p.read_bytes();assert sha(src)=='b57e4859c498bf57e05706dcd83d89db0f14102c33aec7359580c155d924861c'
ns={'__name__':'inert_runner_review','__file__':str(p)};exec(compile(src,str(p),'exec'),ns)
def put(name,buf):
 p=out/name;b=buf.encode() if isinstance(buf,str) else buf
 with p.open('xb') as f:f.write(b)
 return p,sha(b)
def stale_cache(p,source):
 cache=Path(importlib.util.cache_from_source(str(p)));cache.parent.mkdir(exist_ok=True);st=p.stat()
 b=importlib.util.MAGIC_NUMBER+struct.pack('<III',0,int(st.st_mtime),st.st_size)+marshal.dumps(compile(source,str(p),'exec'))
 with cache.open('xb') as f:f.write(b)
 return {'path':str(cache),'sha256':sha(b)}
checks=[]
def ck(name,ok,detail=None):checks.append({'id':name,'passed':bool(ok),'detail':detail})
def run(args):
 old_modules=set(sys.modules);old_meta=list(sys.meta_path);old_argv=list(sys.argv);old_path=list(sys.path)
 try:return {'return':ns['run'](args)}
 except Exception as e:return {'exception':type(e).__name__,'message':str(e)}
 finally:
  sys.meta_path[:]=old_meta;sys.argv[:]=old_argv;sys.path[:]=old_path
  for n in list(set(sys.modules)-old_modules):
   if n.startswith('unt_review_'):del sys.modules[n]
common,ch=put('unt_review_common.py',"MARKER='PINNED_SOURCE'\n")
main,mh=put('main_pinned.py',"import unt_review_common\ndef main(args): return 0 if unt_review_common.MARKER=='PINNED_SOURCE' else 17\n")
cache=stale_cache(common,"MARKER='UNPINNED_BYTECODE'\n")
args=['--module','unt_review_common='+str(common)+'='+ch,'--main',str(main)+'='+mh,'--call','main','--']
r=run(args);ck('pinned_sibling_uses_exact_source_despite_stale_pyc',r=={'return':0},r)
bad=list(args);bad[1]='unt_review_common='+str(common)+'='+'0'*64;r=run(bad);ck('wrong_module_pin_typed_refusal',r.get('exception')=='Refuse' and r.get('message','').startswith('PIN_BYTES_MISMATCH'),r)
badmain=list(args);badmain[3]=str(main)+'='+'0'*64;r=run(badmain);ck('wrong_main_pin_typed_refusal',r.get('exception')=='Refuse' and r.get('message','').startswith('PIN_BYTES_MISMATCH'),r)
flat,flath=put('unt_review_unpinned.py','MARKER=37\n');fm,fmh=put('main_unpinned_flat.py',"import sys\nsys.path.insert(0,"+repr(str(out))+")\nimport unt_review_unpinned\ndef main(args): return unt_review_unpinned.MARKER\n")
r=run(['--main',str(fm)+'='+fmh,'--call','main','--']);ck('unpinned_flat_sibling_refuses',r.get('exception')=='ImportError' and r.get('message','').startswith('UNPINNED_SIBLING_IMPORT_REFUSED'),r)
pkg=out/'unt_review_package';pkg.mkdir();pkgfile,pgh=put('unt_review_package/__init__.py','MARKER=41\n');pm,pmh=put('main_unpinned_package.py',"import sys\nsys.path.insert(0,"+repr(str(out))+")\nimport unt_review_package\ndef main(args): return unt_review_package.MARKER\n")
r=run(['--main',str(pm)+'='+pmh,'--call','main','--']);ck('unpinned_sibling_package_refuses',r.get('exception')=='ImportError' and r.get('message','').startswith('UNPINNED_SIBLING_IMPORT_REFUSED'),r)
ck('priority_nice10',os.getpriority(os.PRIO_PROCESS,0)>=10)
result={'date_u':subprocess.check_output(['/bin/date','-u'],text=True).strip(),'label':'TESTED_UNSELECTED_RUNNER002_INERT_DELTA','source':{'path':str(p),'sha256':sha(src)},'harness':{'path':__file__,'sha256':sha(Path(__file__).read_bytes())},'checks':checks,'passed':sum(x['passed'] for x in checks),'total':len(checks),'stale_fixture':cache,'scope':'New runner only; all code payloads inert newly created fixtures. Package test targets blanket sibling-import guard claim, not a claim that current tool imports or live sources changed. No real tool/comparator/root script or protected content.'}
rp=out/'RESULTS.json'
with rp.open('x') as f:json.dump(result,f,indent=2,sort_keys=True);f.write('\n')
print(json.dumps({'path':str(rp),'sha256':sha(rp.read_bytes()),'passed':result['passed'],'total':result['total'],'failed':[x for x in checks if not x['passed']]}))
