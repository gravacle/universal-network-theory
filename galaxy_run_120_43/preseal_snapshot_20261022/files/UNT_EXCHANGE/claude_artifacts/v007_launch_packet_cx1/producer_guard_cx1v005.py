"""0541/0543: immutable root admission config, not argv authority. No config => refuse all producers.
Root alone writes ROOT_SEAL_ADMISSION_V001.json after seal. Every entry revalidates it from bytes.
Historical unguarded files cannot be disabled retroactively; only final allowlisted entry points are admitted.
"""
import functools,hashlib,json,os,sys
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
 cfg=json.loads(CONFIG.read_bytes())
 if cfg.get('schema')!='UNT_ROOT_SEAL_ADMISSION_CX1V001' or cfg.get('authority')!=AUTHORITY:raise PermissionError('ROOT_AUTHORITY_RECORD_REQUIRED')
 own=str(Path(producer).resolve());allow=cfg.get('producer_allowlist',{})
 if allow.get(own)!=sha(own) or allow.get(str(Path(__file__).resolve()))!=sha(__file__):raise PermissionError('PRODUCER_NOT_ON_FINAL_ALLOWLIST')
 for key in ('seal','prereg','compare','build'):pin_check(cfg[key])
 seal=json.loads(Path(cfg['seal']['path']).read_bytes())
 if seal.get('sealed_by')!=AUTHORITY:raise PermissionError('STRUCTURED_ROOT_SEAL_AUTHORITY_REQUIRED')
 if seal.get('prereg')!=cfg['prereg'] or seal.get('compare')!=cfg['compare']:raise PermissionError('SEALED_PREREG_COMPARE_BINDING')
 text=Path(cfg['build']['path']).read_text()
 for path,digest in allow.items():
  if f'{digest}  {path}' not in text:raise PermissionError('BUILD_ALLOWLIST_MISMATCH')
 SEALED_COMPARE_REF=cfg['compare'];return cfg

def guarded(fn):
 @functools.wraps(fn)
 def call(*a,**k):admission(fn.__globals__['__file__']);return fn(*a,**k)
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
 p=Path(run)
 if any(x.casefold().startswith('uvt_') for x in p.resolve().parts):raise PermissionError('UVT_RUN_FORBIDDEN')
 # An output anywhere under a copied/marked ancestor is also forbidden.
 for candidate in (p,*p.parents):
  if marker_hit(candidate):
   if allow_registered and path_hit(p):return
   raise PermissionError('C5H_REGISTERED_OR_MARKED_COPY_REFUSED')

def authorize(argv,kind='run',producer=None):
 if '--seal' in argv or '--seal-sha' in argv:raise PermissionError('SEAL_AUTHORITY_MUST_NOT_COME_FROM_ARGV')
 cfg=admission(producer or argv[0])
 if kind=='run':
  if len(argv)<2:raise ValueError('RUN_ARGUMENT_REQUIRED')
  check_run_path(argv[1],allow_registered=True)
 return cfg
