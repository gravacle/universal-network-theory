"""Run exact pinned synthetic-suite bytes with an inherited audit and 8-GiB RSS watchdog.
The only behavioral substitution preserves redundant hard-linked .tmp names instead of unlinking them.
Child Python invocations are instrumented too; scientific driver subprocesses are refused.
"""
import ast,hashlib,json,os,resource,runpy,subprocess,sys,time
from pathlib import Path
H=Path(__file__).parent;ART=H.parent;PY='/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
SELF=str(Path(__file__).absolute());AUD=H/'suite_audits_cx3v001'
SOURCES={str(ART/'h3_campaign_path_c2/tests/test_h3_campaign_path_c2v002.py'):'6705c949b504aac4cfd994710c0beea8abd2775ef347ede2dff986035f2caa1d',str(ART/'h3_campaign_path_c2/tests/test_campaign_cert_c2v004.py'):'52d0420206718a73e92ec89779deebe49ea90bf367cd8db798cf68e427be748e',str(ART/'galaxy_m0_forward_c2_0466/root_monitor_c2v001.py'):'ba031c2340057d88ee399138cc645012a93aa7dc3eb7c9bba56d112c94a47107'}
MOCK_SHA='374c508e83a6c6a8714be0e4cf25c08fe6d8325671603decdd36c75f5165f57c'
def sha(b):return hashlib.sha256(b).hexdigest()
def allowed_script(s):
 p=Path(s).absolute();b=p.read_bytes()
 if str(p) in SOURCES:return sha(b)==SOURCES[str(p)]
 return p.is_relative_to(H) and sha(b)==MOCK_SHA
script=str(Path(sys.argv[1]).absolute());args=sys.argv[2:]
if not allowed_script(script):raise PermissionError('unapproved executable script '+script)
AUD.mkdir(exist_ok=True)
audit_fh=(AUD/('AUDIT_%d.json'%os.getpid())).open('x')
# macOS sandbox rejects setrlimit with ValueError; monitor each instrumented process's actual RSS.
import threading
def watch_rss():
 while True:
  if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss >= 8<<30:os._exit(91)
  time.sleep(0.2)
threading.Thread(target=watch_rss,daemon=True).start()
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS'):os.environ[k]='1'
reads=set();denied=[];preserved=[];subcalls=[];active=True
origPopen=subprocess.Popen
class Popen(origPopen):
 def __init__(self,argv,*a,**kw):
  if not isinstance(argv,(list,tuple)):raise PermissionError('shell command refused')
  argv=list(argv)
  if argv[0]==PY:
   i=next((i for i,v in enumerate(argv[1:],1) if not str(v).startswith('-')),None)
   if i is None or not allowed_script(argv[i]):raise PermissionError('unapproved Python child '+repr(argv[:5]))
   subcalls.append({'script':argv[i],'sha256':sha(Path(argv[i]).read_bytes())})
   argv=[PY,'-I','-B',SELF,argv[i],*argv[i+1:]]
  elif Path(argv[0]).name!='ps':raise PermissionError('non-Python/ps subprocess refused')
  super().__init__(argv,*a,**kw)
subprocess.Popen=Popen
orig_unlink=os.unlink
def preserve_tmp(path,*a,**kw):
 p=Path(path).absolute()
 if p.is_relative_to(H) and p.name.startswith('.') and p.name.endswith('.tmp') and p.is_file() and p.stat().st_nlink>=2:
  preserved.append(str(p));return None
 raise PermissionError('delete refused '+str(p))
os.unlink=preserve_tmp;os.remove=preserve_tmp

def audit(e,args):
 if not active:return
 if (e.startswith('socket.') and e!='socket.gethostname') or e in ('os.system','os.fork','os.posix_spawn','os.rename','os.rmdir','os.remove','os.symlink'):raise PermissionError(e)
 if e=='open' and isinstance(args[0],(str,bytes,os.PathLike)):
  p=Path(os.fsdecode(args[0])).absolute();s=str(p);mode,flags=args[1:]
  w=(isinstance(mode,str) and any(c in mode for c in 'wax+')) or isinstance(flags,int) and flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND)
  if w and not p.is_relative_to(H) and not s.startswith('/dev/'):
   denied.append(['write',s]);raise PermissionError('write outside own scratch')
  if not w and not p.is_relative_to(H):
   forbidden=('ngc3198' in s.lower() or '/runs_ext/' in s or '/runs/' in s or '/.codex/' in s or '/.codex-alt/' in s or '/V007_SEAL_ASSEMBLY/' in s or '/V007_POSTSEAL_RECORDS/' in s or '/cp1_run_' in s or '/W1_RUN_SHEET/evidence/' in s or ('target' in p.name.lower() and p.suffix!='.py'))
   if forbidden:denied.append(['read',s]);raise PermissionError('forbidden path '+s)
  if not w and p.is_file() and (p.suffix in ('.py','.json','.md','.txt') or p.name=='spec.json') and not p.is_relative_to(Path(sys.base_prefix)):reads.add(s)
sys.addaudithook(audit)
code=0;error=None;started=time.monotonic();sys.argv=[script,*args]
try:runpy.run_path(script,run_name='__main__')
except SystemExit as e:code=e.code if isinstance(e.code,int) else (0 if e.code is None else 1)
except BaseException as e:error=repr(e);code=1;raise
finally:
 active=False
 foreign=[]
 for s in sorted(reads):
  p=Path(s)
  if not p.is_relative_to(H) and p.is_file():foreign.append({'path':s,'sha256':sha(p.read_bytes())})
 out={'script':{'path':script,'sha256':sha(Path(script).read_bytes())},'argv':args,'status':code,'error':error,'foreign_read_pins':foreign,'denied':denied,'subprocesses':subcalls,'preserved_redundant_tmp_names':preserved,'rss_watchdog_limit_bytes':8<<30,'kernel_address_space_limit_set':False,'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'seconds':time.monotonic()-started}
 json.dump(out,audit_fh,indent=1,sort_keys=True);audit_fh.write('\n');audit_fh.close()
sys.exit(code)
