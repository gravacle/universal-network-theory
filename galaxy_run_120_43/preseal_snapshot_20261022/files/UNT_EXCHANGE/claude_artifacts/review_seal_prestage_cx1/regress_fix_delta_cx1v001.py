"""Prepared 0639 successor delta harness. Run only on a fresh byte-pinned review snapshot."""
import argparse,ast,hashlib,importlib.util,json,marshal,os,struct,subprocess,types
from pathlib import Path
sha=lambda b:hashlib.sha256(b).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--snapshot',required=True);ap.add_argument('--snapshot-sha',required=True);ap.add_argument('--outdir',required=True);a=ap.parse_args()
 raw=Path(a.snapshot).read_bytes();assert sha(raw)==a.snapshot_sha;manifest=json.loads(raw)
 row=next(x for x in manifest['inputs'] if Path(x['snapshot']).name=='helper.py');helper=Path(row['snapshot']);src=helper.read_bytes();assert sha(src)==row['sha256']
 out=Path(a.outdir);assert str(out).startswith('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/');out.mkdir()
 ns={'__name__':'inert_delta_helper_review','__file__':str(helper)};exec(compile(src,str(helper),'exec'),ns)
 checks=[]
 def ck(name,ok,detail=None):checks.append({'id':name,'passed':bool(ok),'detail':detail})
 # No actual protected object. Both link and target are new inert fixtures inside review output.
 prot=out/'KMAX_A2F10_C5H_RUN_V001';prot.mkdir();dummy=prot/'dummy.txt'
 with dummy.open('xb') as f:f.write(b'INERT ONLY\n')
 alias=out/'ordinary_alias';alias.symlink_to(prot,target_is_directory=True)
 original=os.lstat;hits=[]
 def spy(path,*args,**kwargs):
  if str(prot) in str(path):hits.append(str(path))
  return original(path,*args,**kwargs)
 os.lstat=spy
 try:
  try:ns['path_policy'](str(alias/'dummy.txt'),True,'inert metadata regression');outcome='ACCEPTED'
  except Exception as e:outcome=type(e).__name__
 finally:os.lstat=original
 ck('B1_alias_refuses',outcome!='ACCEPTED',outcome);ck('B1_zero_target_metadata_before_refusal',not hits,{'target_lstat_calls':len(hits)})
 # Source cache is a deliberately different synthetic program, exclusively written as a fresh fixture.
 fence=out/'synthetic_fence.py';source="MARKER='PINNED_SOURCE'\ndef arm(write_roots=()): pass\ndef selftest(): return (['realpath_c5h'],10)\n"
 with fence.open('x') as f:f.write(source)
 cache=Path(importlib.util.cache_from_source(str(fence)));cache.parent.mkdir();st=fence.stat()
 payload=importlib.util.MAGIC_NUMBER+struct.pack('<III',0,int(st.st_mtime),st.st_size)+marshal.dumps(compile(source.replace('PINNED_SOURCE','UNPINNED_BYTECODE'),str(fence),'exec'))
 with cache.open('xb') as f:f.write(payload)
 args=types.SimpleNamespace(fence=str(fence),fence_sha=sha(fence.read_bytes()))
 loaded=ns['_fence'](args,write_roots=(str(out),));ck('B2_executes_exact_pinned_source',loaded.MARKER=='PINNED_SOURCE',loaded.MARKER)
 try:ns['_fence'](types.SimpleNamespace(fence=str(fence),fence_sha='0'*64),write_roots=(str(out),));wrong='ACCEPTED'
 except Exception as e:wrong=type(e).__name__
 ck('B2_wrong_source_pin_refuses',wrong!='ACCEPTED',wrong)
 ck('priority_nice10',os.getpriority(os.PRIO_PROCESS,0)>=10)
 r={'date_u':subprocess.check_output(['/bin/date','-u'],text=True).strip(),'label':'TESTED_INERT_SUCCESSOR_DELTA','snapshot':{'path':a.snapshot,'sha256':a.snapshot_sha},'helper':row,'checks':checks,'passed':sum(x['passed'] for x in checks),'total':len(checks),'verdict':'PASS' if all(x['passed'] for x in checks) else 'FAIL','actual_protected_reads':False,'actual_target_reads':False,'scientific_processes_created':0}
 p=out/'RESULTS.json'
 with p.open('x') as f:json.dump(r,f,indent=2,sort_keys=True);f.write('\n')
 print(json.dumps({'passed':r['passed'],'total':r['total'],'verdict':r['verdict'],'path':str(p),'sha256':sha(p.read_bytes())}))
if __name__=='__main__':main()
