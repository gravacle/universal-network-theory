"""Run B's own suite; redirect its hash-only original compare to byte-identical permitted suite-case bytes."""
import argparse,hashlib,json,os,runpy,subprocess,sys
from pathlib import Path
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--work',required=True);a=ap.parse_args()
 root=Path(__file__).resolve().parent;work=Path(a.work).resolve();work.mkdir(parents=True,exist_ok=False)
 art=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts');b=art/'classifier_b_c2/build_c2v005'
 copy=b/'suite/run1/B340/compare.json';want='6f095f64a1f1acc2ad2910af12f645e18acdf16fb62bfd936386a61c47ef30e9'
 assert hashlib.sha256(copy.read_bytes()).hexdigest()==want
 sources=set();refused=[]
 def guard(event,args):
  if event=='open':
   path,mode,flags=args
   if not isinstance(path,(str,bytes,os.PathLike)):return
   p=Path(os.fsdecode(path)).resolve()
   write=isinstance(flags,int) and bool(flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND))
   if write:
    if not p.is_relative_to(work):raise PermissionError('WRITE_OUTSIDE_OWN_WORK')
   elif str(p).startswith('/Users/bgm/Research/'):
    if p.is_relative_to(work) or p.is_relative_to(b) or p==Path(__file__).resolve():pass
    elif p==art/'stage0_successor_c2/prediction_freeze_c2v003g_stage0_c2v002.py':pass
    else:refused.append(str(p));raise PermissionError('OUTSIDE_CLASSIFIER_REVIEW_SCOPE')
    if p.suffix=='.py':sources.add(str(p))
  elif event in ('os.remove','os.rename','os.rmdir'):raise PermissionError('NO_DELETION_OR_RENAME')
 sys.addaudithook(guard)
 sys.path.insert(0,str(b/'suite'))
 import suite_lib_c2v005 as lib
 lib.REAL_COMPARE_PATH=str(copy)
 sys.argv=[str(b/'suite/run_suite_c2v005.py'),'--classifier',str(b/'classifier_b_c2v005.py'),
 '--schema',str(b/'OUTPUT_SCHEMA_C2V005_DERIVED.json'),'--defs',str(b/'suite/case_defs_c2v005_v8.py'),
 '--cases',str(work/'cases'),'--results',str(work/'SUITE_RESULTS_CX2V001.json'),'--python',sys.executable]
 code=0
 try:runpy.run_path(sys.argv[0],run_name='__main__')
 except SystemExit as ex:code=ex.code or 0
 except Exception as ex:
  code=1;print(type(ex).__name__,str(ex));raise
 finally:
  audit={'date_u':subprocess.check_output(['/bin/date','-u'],text=True).strip(),'label':'TESTED','exit_code':code,
  'compare_copy':{'path':str(copy),'sha256':want},'refused_opens':refused,
  'code_reads':[{'path':p,'sha256':hashlib.sha256(Path(p).read_bytes()).hexdigest()} for p in sorted(sources)],
  'scope':'parent guard; child B CLIs consume only newly generated target-free cases and pinned B kernels'}
  with (work/'READ_LOG_CX2V001.json').open('x') as f:json.dump(audit,f,indent=2);f.write('\n')
 return code
if __name__=='__main__':sys.exit(main())
