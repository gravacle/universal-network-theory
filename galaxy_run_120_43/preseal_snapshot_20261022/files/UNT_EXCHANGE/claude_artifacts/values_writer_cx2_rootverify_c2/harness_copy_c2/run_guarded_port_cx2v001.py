"""Run the port with a parent-process research-data guard and dependency hashes."""
import argparse,hashlib,json,os,runpy,subprocess,sys
from pathlib import Path
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--tests',required=True);ap.add_argument('--module',required=True);ap.add_argument('--work',required=True);a=ap.parse_args()
 root=Path(__file__).resolve().parent;work=Path(a.work).resolve();reads=set();refused=[]
 def guard(event,args):
  if event=='open':
   path,mode,flags=args
   if not isinstance(path,(str,bytes,os.PathLike)):return
   p=Path(os.fsdecode(path)).resolve()
   write=(isinstance(flags,int) and bool(flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND)))
   if write:
    if not p.is_relative_to(work):raise PermissionError('WRITE_OUTSIDE_OWN_SYNTHETIC_WORK')
   elif str(p).startswith('/Users/bgm/Research/'):
    if 'ngc3198' in p.name.lower():refused.append(str(p));raise PermissionError('NGC3198_NAMED_PATH')
    if p.is_relative_to(root):return
    if p.suffix=='.py':reads.add(str(p));return
    refused.append(str(p));raise PermissionError('REAL_RESEARCH_DATA_REFUSED')
  elif event in ('os.remove','os.rename','os.rmdir'):
   for value in args[:2] if event=='os.rename' else args[:1]:
    if isinstance(value,(str,bytes,os.PathLike)) and not Path(os.fsdecode(value)).resolve().is_relative_to(work):
     raise PermissionError('MUTATION_OUTSIDE_OWN_SYNTHETIC_WORK')
 sys.addaudithook(guard)
 sys.argv=[a.tests,'--module',a.module,'--work',str(work)]
 code=0
 try:runpy.run_path(a.tests,run_name='__main__')
 except SystemExit as e:code=e.code or 0
 # All of these are code reads authorized by 0773, never data-pointer traversal.
 pins=[{'path':p,'sha256':hashlib.sha256(Path(p).read_bytes()).hexdigest()} for p in sorted(reads)]
 d={'date_u':subprocess.check_output(['/bin/date','-u'],text=True).strip(),'label':'TESTED','loaded_code':pins,
    'refused_opens':refused,'exit_code':code,'guard_scope':'parent process; child writer CLIs use the port synthetic ruling and manifest and the same pinned library/row code',
    'wrapper_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
 with (work/'DEPENDENCY_READ_LOG_CX2V001.json').open('x') as f:json.dump(d,f,indent=2);f.write('\n')
 return code
if __name__=='__main__':sys.exit(main())
