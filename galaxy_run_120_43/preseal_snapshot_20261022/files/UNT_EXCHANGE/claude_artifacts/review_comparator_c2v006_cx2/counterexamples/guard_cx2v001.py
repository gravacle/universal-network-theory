import os,sys
from pathlib import Path
ALLOWED=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v006_cx2/counterexamples').resolve()
AUDIT_BLOCKED=[]
def _audit(ev,args):
 if ev.startswith('socket.') or ev in ('subprocess.Popen','os.system','os.posix_spawn','os.spawn','os.fork','os.exec','pty.spawn'):
  AUDIT_BLOCKED.append(ev);raise RuntimeError('NO_PROCESS_NETWORK')
 if ev in ('os.remove','os.rmdir','os.rename','os.replace','shutil.rmtree'):
  AUDIT_BLOCKED.append(ev);raise RuntimeError('NO_DESTRUCTIVE_WRITES')
 if ev=='open' and isinstance(args[0],(str,bytes,os.PathLike)):
  p=Path(os.fsdecode(args[0])).resolve();s=str(p).lower();mode=args[1];flags=args[2]
  if '/runs/' in s or '/runs_ext/' in s or '/.codex/' in s or 'kmax_a2f10_c5h_run_v001' in s or '/gates_v006/out/' in s or '/gates_v006/records/' in s or ('ngc3198' in s and any(x in s for x in ('target','observed','rotmod'))):
   AUDIT_BLOCKED.append(str(p));raise RuntimeError('PROHIBITED_READ')
  writing=(isinstance(mode,str) and any(x in mode for x in 'wax+')) or (isinstance(flags,int) and flags&(os.O_CREAT|os.O_TRUNC|os.O_WRONLY|os.O_RDWR|os.O_APPEND))
  if writing and (not p.is_relative_to(ALLOWED) or not flags&os.O_EXCL):
   AUDIT_BLOCKED.append(str(p));raise RuntimeError('ONLY_NEW_OWN_FILES')
sys.addaudithook(_audit)
