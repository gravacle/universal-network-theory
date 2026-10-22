"""0541/0543: immutable root admission config, not argv authority. No config => refuse all producers.
Root alone writes ROOT_SEAL_ADMISSION_V001.json after seal. Every entry revalidates it from bytes.
Historical unguarded files cannot be disabled retroactively; only final allowlisted entry points are admitted.
"""
import functools,hashlib,inspect,json,os,re,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
CONFIG=HERE/'ROOT_SEAL_ADMISSION_V001.json'
AUTHORITY={'identity':'Claude2','role':'coordinator_and_single_scientific_launch_owner'}
C5H_NAME='KMAX_A2F10_C5H_RUN_V001'
C5H_SPEC='60b4613080055aedd92dbb649cdfa45675f64a4d133c7ba3e4fbb15b59c7704e'
BASE=Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2')
REGISTERED=(BASE/'runs_ext'/C5H_NAME,Path('/Volumes/External1/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs_ext')/C5H_NAME)
SEALED_COMPARE_REF=None

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def pin_check(ref):
 if not isinstance(ref,dict) or set(ref)!={'path','sha256'} or sha(ref['path'])!=ref['sha256']:raise ValueError('ROOT_ADMISSION_PIN_MISMATCH')
def admission(producer):
 global SEALED_COMPARE_REF
 if not CONFIG.is_file():raise PermissionError('ROOT_SEAL_ADMISSION_PENDING')
 raw=CONFIG.read_bytes();config_sha=hashlib.sha256(raw).hexdigest()
 expected=os.environ.get('UNT_ROOT_ADMISSION_SHA256','')
 if not re.fullmatch('[0-9a-f]{64}',expected):raise PermissionError('PUBLISHED_ADMISSION_SHA_REQUIRED')
 if config_sha!=expected:raise PermissionError('PUBLISHED_ADMISSION_SHA_MISMATCH')
 cfg=json.loads(raw)
 if cfg.get('schema')!='UNT_ROOT_SEAL_ADMISSION_CX1V001' or cfg.get('authority')!=AUTHORITY:raise PermissionError('ROOT_AUTHORITY_RECORD_REQUIRED')
 own=str(Path(producer).resolve());allow=cfg.get('producer_allowlist',{})
 if allow.get(own)!=sha(own) or allow.get(str(Path(__file__).resolve()))!=sha(__file__):raise PermissionError('PRODUCER_NOT_ON_FINAL_ALLOWLIST')
 for key in ('seal','prereg','compare','build'):pin_check(cfg[key])
 seal=json.loads(Path(cfg['seal']['path']).read_bytes())
 if seal.get('sealed_by')!=AUTHORITY:raise PermissionError('STRUCTURED_ROOT_SEAL_AUTHORITY_REQUIRED')
 if seal.get('prereg')!=cfg['prereg'] or seal.get('compare')!=cfg['compare']:raise PermissionError('SEALED_PREREG_COMPARE_BINDING')
 text=Path(cfg['build']['path']).read_text()
 for path,digest in allow.items():
  if Path(path).suffix!=".py" or sha(path)!=digest:raise PermissionError("ALLOWLIST_SOURCE_BYTES_CHANGED")
  if f'{digest}  {path}' not in text:raise PermissionError('BUILD_ALLOWLIST_MISMATCH')
 cfg['_verified_config_sha256']=config_sha
 SEALED_COMPARE_REF=cfg['compare'];return cfg

def provenance(producer):
 cfg=admission(producer)
 return {'config':{'path':str(CONFIG),'sha256':cfg['_verified_config_sha256']},'seal':dict(cfg['seal']),'compare':dict(cfg['compare'])}

def stamp(record,producer):
 if not isinstance(record,dict):raise ValueError('PRODUCER_RECORD_MUST_BE_OBJECT')
 return dict(record,root_admission=provenance(producer))

def check_entry_paths(fn,args,kwargs):
 seen=set()
 def visit(value,name='',depth=0):
  if depth>5:return
  if isinstance(value,os.PathLike):check_run_path(value,allow_registered=True);return
  if isinstance(value,str):
   if not value or value.startswith('--') or '\n' in value:return
   key=name.lower();candidate=('/' in value or '\\' in value or value.startswith('.') or key in {'run','path','p','out','outdir','root','mp','ck','cdir','source','filename'} or key.endswith(('_path','_dir','_file')))
   if candidate:check_run_path(value,allow_registered=True)
   return
  ident=id(value)
  if ident in seen:return
  seen.add(ident)
  if isinstance(value,dict):
   for k,v in value.items():visit(v,str(k),depth+1)
  elif isinstance(value,(tuple,list)):
   for v in value:visit(v,name,depth+1)
  else:
   attrs=getattr(value,'__dict__',{})
   for k in ('run','root','rot','field','src_rot','manifest','checkpoint','path'):
    if k in attrs:visit(attrs[k],k,depth+1)
 for name,value in inspect.signature(fn).bind_partial(*args,**kwargs).arguments.items():visit(value,name)
 if fn.__name__=='main':
  for value in sys.argv[1:]:visit(value,'path')

def guarded(fn):
 @functools.wraps(fn)
 def call(*a,**k):
  producer=fn.__globals__['__file__'];admission(producer);check_entry_paths(fn,a,k);result=fn(*a,**k)
  if isinstance(result,dict) and ('schema' in result or 'gate' in result):return stamp(result,producer)
  return result
 return call

def path_hit(path):
 p=Path(path);real=p.resolve();parts={x.casefold() for x in p.parts}|{x.casefold() for x in real.parts}
 if C5H_NAME.casefold() in parts:return True
 return any(real==x.resolve() or real.is_relative_to(x.resolve()) for x in REGISTERED)

def marker_hit(run):
 run=Path(run)
 if path_hit(run):return True
 for registered in REGISTERED:
  try:
   if run.is_dir() and registered.is_dir() and os.path.samefile(run,registered):return True
  except OSError:pass
 candidates=[(run/'start.json',('call_spec_sha256',)),(Path(str(run)+'.receipt.json.launch.json'),('pins','spec','sha256')),(run/'launch.json',('pins','spec','sha256'))]
 for p,keys in candidates:
  if path_hit(p):return True
  if not p.is_file():continue
  d=json.loads(p.read_bytes())
  for key in keys:d=d.get(key) if isinstance(d,dict) else None
  if d==C5H_SPEC:return True
 return False

def check_run_path(run,allow_registered=False):
 p=Path(run).absolute()
 if any(x.casefold().startswith('uvt_') for x in p.resolve().parts):raise PermissionError('UVT_RUN_FORBIDDEN')
 # An output anywhere under a copied/marked ancestor is also forbidden.
 real=p.resolve()
 for candidate in dict.fromkeys((p,*p.parents,real,*real.parents)):
  if marker_hit(candidate):
   if allow_registered and any(real==x.resolve() or real.is_relative_to(x.resolve()) for x in REGISTERED):return
   raise PermissionError('C5H_REGISTERED_OR_MARKED_COPY_REFUSED')

def authorize(argv,kind='run',producer=None):
 if '--seal' in argv or '--seal-sha' in argv:raise PermissionError('SEAL_AUTHORITY_MUST_NOT_COME_FROM_ARGV')
 cfg=admission(producer or argv[0])
 if kind=='run':
  if len(argv)<2:raise ValueError('RUN_ARGUMENT_REQUIRED')
  check_run_path(argv[1],allow_registered=True)
 return cfg
