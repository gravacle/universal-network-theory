"""Inert seal-helper boundary regressions. No comparator/real root script execution."""
import argparse,ast,hashlib,json,os,re,subprocess,types
from pathlib import Path

def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--snapshot',required=True);ap.add_argument('--snapshot-sha',required=True);ap.add_argument('--outdir',required=True);a=ap.parse_args()
 raw=Path(a.snapshot).read_bytes();assert sha(raw)==a.snapshot_sha;manifest=json.loads(raw)
 sources={}
 for ref in manifest['inputs']:
  p=Path(ref['snapshot']); b=p.read_bytes();assert sha(b)==ref['sha256'];sources[p.name]=b
 out=Path(a.outdir);assert str(out).startswith('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/');out.mkdir()
 # Only the copied helper is executed, with __name__ preventing its CLI. Its module-level statements are stdlib imports, definitions and literal constants.
 tree=ast.parse(sources['helper.py'])
 allowed=(ast.Import,ast.ImportFrom,ast.Assign,ast.FunctionDef,ast.ClassDef,ast.If)
 assert all(isinstance(n,allowed) for n in tree.body)
 ns={'__name__':'inert_seal_helper_review','__file__':str(out/'helper_snapshot_identity.py')}
 exec(compile(sources['helper.py'],'review_helper_snapshot','exec'),ns)
 Refuse=ns['Refuse']; checks=[]
 def ck(name,ok,detail=None):checks.append({'id':name,'passed':bool(ok),'detail':detail})
 def put(name,data):
  path=out/name;b=data.encode() if isinstance(data,str) else data
  with path.open('xb') as f:f.write(b)
  return path,sha(b)
 def refused(name,fn):
  try:fn();ck(name,False,'unexpected success')
  except Refuse as e:ck(name,True,str(e).split(':')[0])
  except Exception as e:ck(name,False,type(e).__name__+': '+str(e))
 dest=out/'exclusive.bin';res=ns['write_x'](str(dest),b'original inert data');ck('exclusive_new_write',res['sha256']==sha(b'original inert data'))
 refused('existing_output_refuses',lambda:ns['write_x'](str(dest),b'replacement'))
 ck('existing_output_bytes_preserved',dest.read_bytes()==b'original inert data')
 refused('missing_output_parent_refuses',lambda:ns['write_x'](str(out/'missing'/'new.bin'),b'new'))
 ck('missing_parent_not_created',not (out/'missing').exists())
 refused('wrong_source_pin_refuses_copy',lambda:ns['c_copy_x'](types.SimpleNamespace(src=str(dest),src_sha='0'*64,dst=str(out/'badcopy.bin'))))
 ck('wrong_pin_emits_no_output',not (out/'badcopy.bin').exists())
 correct=ns['c_copy_x'](types.SimpleNamespace(src=str(dest),src_sha=sha(dest.read_bytes()),dst=str(out/'copy.bin')))
 ck('copy_preserves_exact_verified_bytes',(out/'copy.bin').read_bytes()==dest.read_bytes())
 keys=ns['PREREG_SLOT_OF']; slot={k:{'path':'/Users/inert/'+k,'sha256':'1'*64} for k in set(keys.values())};slot['compare_reviewed_source']={}
 tor={'schema':'INERT_PREREG','outside':'must remain identical','seal_slots':{k:{'value':'PENDING','policy':'unchanged'} for k in keys}}
 tp,th=put('prereg.json',json.dumps(tor));sp,sh=put('slots.json',json.dumps(slot))
 output=out/'sealed_prereg.json';ns['c_sealed_prereg'](types.SimpleNamespace(text_of_record=str(tp),tor_sha=th,slots=str(sp),slots_sha=sh,out=str(output)))
 actual=json.loads(output.read_bytes());expected=json.loads(json.dumps(tor))
 for k,v in keys.items():expected['seal_slots'][k]['value']=slot[v]
 ck('prereg_only_slot_values_change',actual==expected)
 source='\n'.join(n+' = None' for n in ns['PIN_NAMES'])+'\nUNCHANGED = 17\n'
 cp,ch=put('inert_compare.py',source); slot['compare_reviewed_source']={'path':str(cp),'sha256':ch};slot['driver_build_record']={'path':'/Users/inert/build.json','sha256':'2'*64};slot['driver_check_record']={'path':'/Users/inert/check.json','sha256':'3'*64}
 sp2,sh2=put('slots_compare.json',json.dumps(slot));coutput=out/'sealed_inert_compare.py'
 args=types.SimpleNamespace(reviewed=str(cp),reviewed_sha=ch,slots=str(sp2),slots_sha=sh2,sealed_prereg=str(output),sealed_prereg_sha=sha(output.read_bytes()),out=str(coutput))
 ns['c_sealed_compare'](args)
 before=source.splitlines();after=coutput.read_text().splitlines();ck('exact_five_pin_lines_changed',[i for i,(x,y) in enumerate(zip(before,after)) if x!=y]==list(range(5)) and len(before)==len(after))
 badsource=source+'\ndef mutate():\n global V007_PREREG_SHA256\n V007_PREREG_SHA256 = "bad"\n';bp,bh=put('inert_rebind.py',badsource)
 slot['compare_reviewed_source']={'path':str(bp),'sha256':bh};sp3,sh3=put('slots_rebind.json',json.dumps(slot));badout=out/'sealed_rebind.py'
 refused('global_pin_rebind_refuses',lambda:ns['c_sealed_compare'](types.SimpleNamespace(reviewed=str(bp),reviewed_sha=bh,slots=str(sp3),slots_sha=sh3,sealed_prereg=str(output),sealed_prereg_sha=sha(output.read_bytes()),out=str(badout))))
 ck('rebind_emits_no_output',not badout.exists())
 # Extract exact run_h wrapper, but substitute H with an inert status function. No real root-script function executes.
 script=sources['script.sh'].decode();line=next(x for x in script.splitlines() if x.startswith('run_h() {'))
 for case,code,existing in [('failure',2,False),('noclobber',0,True)]:
  casepath=out/case;casepath.mkdir();logs=casepath/'logs';logs.mkdir()
  if existing:
   with (logs/'FIRST.json').open('xb') as f:f.write(b'original log')
  shell='set -Eeuo pipefail\nset -o noclobber\nSTEP=inert\nexec 3>&2\ntrap \'echo "STOPPED ${STEP}" >&3\' ERR\nLOGS="$1"\nH() { return '+str(code)+'; }\n'+line+'\nrun_h FIRST noop\nprintf ran > "$2"\n'
  scriptpath,scriptsha=put(case+'/inert_wrapper.sh',shell);nextfile=casepath/'AFTER';r=subprocess.run(['/bin/bash',str(scriptpath),str(logs),str(nextfile)],capture_output=True,text=True)
  ck(case+'_stops_first_failure',r.returncode!=0 and not nextfile.exists(),{'returncode':r.returncode,'stderr':r.stderr[:350]})
  ck(case+'_stop_trap_visible','STOPPED' in r.stderr)
  if existing:ck('noclobber_original_log_preserved',(logs/'FIRST.json').read_bytes()==b'original log')
 ck('priority_nice10',os.getpriority(os.PRIO_PROCESS,0)>=10,os.getpriority(os.PRIO_PROCESS,0))
 result={'date_u':subprocess.check_output(['/bin/date','-u'],text=True).strip(),'label':'TESTED_INERT_BOUNDARY_REGRESSIONS','scope':'Provisional snapshot only; 0639 alias and bytecode regressions intentionally not repeated here. No actual protected/target content or real root script execution.','snapshot':{'path':a.snapshot,'sha256':a.snapshot_sha},'harness':{'path':__file__,'sha256':sha(Path(__file__).read_bytes())},'checks':checks,'passed':sum(c['passed'] for c in checks),'total':len(checks),'verdict':'PASS' if all(c['passed'] for c in checks) else 'FAIL','scientific_processes_created':0}
 p=out/'RESULTS.json'
 with p.open('x') as f:json.dump(result,f,indent=2,sort_keys=True);f.write('\n')
 print(json.dumps({'passed':result['passed'],'total':result['total'],'verdict':result['verdict'],'result_sha256':sha(p.read_bytes()),'path':str(p)}))
if __name__=='__main__':main()
