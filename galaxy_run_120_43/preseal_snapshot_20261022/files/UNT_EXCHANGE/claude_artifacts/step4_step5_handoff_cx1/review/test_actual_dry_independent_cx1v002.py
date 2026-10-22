"""Independent actual Codex3 dry helper, with pre-metadata lexical/symlink barrier."""
import hashlib,json,os,runpy,stat,sys,types
from pathlib import Path
R=Path(__file__).parent;OUT=R/'DRY_INDEPENDENT_V002';OUT.mkdir()
WPATH=R.parent/'impl/write_step4_step5_handoff_cx1v008.py'
W=types.ModuleType('writer_metadata_guard');W.__file__=str(WPATH);exec(compile(WPATH.read_bytes(),str(WPATH),'exec'),W.__dict__)
rec=json.loads((R/'CONTROLS_INDEPENDENT_V003/RESULTS.json').read_bytes())
driver=rec['driver_selection']['driver'];spec=Path(rec['filled_directory'])/'CALL_A_K32_A2_HEADLINE_CX3V001.json';specsha=hashlib.sha256(spec.read_bytes()).hexdigest()
helper=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step5_ngc_route_ab_readiness_cx3/tools/dry_one_step5_cx3v001.py');helper_bytes=helper.read_bytes()
original={k:getattr(os,k) for k in ('stat','lstat','readlink')}
metadata_calls=0
# Resolve components using captured metadata primitives. Check each textual path
# and link destination before asking the OS about that destination.
def checked_path(value):
 if isinstance(value,int):return value
 p=W.lexical(os.path.abspath(os.fsdecode(value)));todo=list(p.parts[1:]);cur=Path('/');links=0
 while todo:
  x=todo.pop(0)
  if x in ('','.'):continue
  if x=='..':cur=cur.parent;continue
  c=W.lexical(str(cur/x))
  try:info=original['lstat'](c)
  except (FileNotFoundError,NotADirectoryError):cur=c;continue
  if stat.S_ISLNK(info.st_mode):
   links+=1
   if links>40:raise RuntimeError('INDEPENDENT_SYMLINK_LOOP')
   t=original['readlink'](c);W.lexical(str(Path(t) if os.path.isabs(t) else cur/t))
   if os.path.isabs(t):cur=Path('/');parts=list(Path(t).parts[1:])
   else:parts=list(Path(t).parts)
   todo=parts+todo
  else:cur=c
 return str(W.lexical(str(cur)))
def guarded_stat(value,*a,**kw):
 global metadata_calls
 metadata_calls+=1;checked_path(value);return original['stat'](value,*a,**kw)
def guarded_lstat(value,*a,**kw):
 global metadata_calls
 metadata_calls+=1;W.lexical(os.path.abspath(os.fsdecode(value)));return original['lstat'](value,*a,**kw)
def guarded_readlink(value,*a,**kw):
 global metadata_calls
 metadata_calls+=1;W.lexical(os.path.abspath(os.fsdecode(value)));t=original['readlink'](value,*a,**kw);W.lexical(str(Path(t) if os.path.isabs(t) else Path(value).parent/t));return t
os.stat=guarded_stat;os.lstat=guarded_lstat;os.readlink=guarded_readlink
# Verify the boundary rejects virtual protected values before any original call.
probes=[];saved=original.copy()
try:
 for k in original:original[k]=lambda *a,**kw:probes.append(a) or (_ for _ in ()).throw(AssertionError('PROBE'))
 for value in ('/virtual/UVT_NEVER/a','/virtual/KMAX_A2F10_C5H_RUN_V001/a','/virtual/NGC3198_observed_velocities.json'):
  try:os.stat(value)
  except W.Refusal:pass
  else:raise AssertionError('missing metadata refusal')
 assert not probes
finally:original.update(saved)
# Independent process and write barrier is installed before running the helper.
def audit(event,args):
 if event.startswith(('socket.','subprocess.')) or event in ('os.system','os.posix_spawn','os.fork','os.forkpty','os.exec','os.kill','os.killpg'):raise RuntimeError('INDEPENDENT_PROCESS_OR_NETWORK_DENIED')
 if event=='open' and args and isinstance(args[0],(str,bytes,os.PathLike)):checked_path(args[0])
sys.addaudithook(audit)
sys.argv=[str(helper),driver['path'],driver['sha256'],str(spec),specsha,str(OUT/'report'),str(OUT/'LOG_CX1V001.json')]
# Execute exactly the helper bytes just inspected and pinned, without a second read.
ns={'__name__':'__main__','__file__':str(helper)};exec(compile(helper_bytes,str(helper),'exec'),ns)
log=json.loads((OUT/'LOG_CX1V001.json').read_bytes())
print(json.dumps({'exit':log['exit'],'exception':log['exception'],'ctx_modes':log['ctx_modes'],'blocked':log['blocked'],'metadata_calls':metadata_calls,'log_sha256':hashlib.sha256((OUT/'LOG_CX1V001.json').read_bytes()).hexdigest(),'helper_sha256':hashlib.sha256(helper_bytes).hexdigest(),'spec_sha256':specsha}))
raise SystemExit(0 if log['exit']==0 and log['ctx_modes']==['simulate'] and not log['blocked'] else 1)
