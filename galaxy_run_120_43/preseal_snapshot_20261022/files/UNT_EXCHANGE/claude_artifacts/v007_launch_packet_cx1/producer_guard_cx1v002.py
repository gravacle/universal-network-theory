"""Fail-closed producer admission. Before sealing, only the three named saved fixtures may be entry runs.
After sealing, --seal PATH --seal-sha SHA binds the root seal and its sealed compare constants from AST (never executes it).
Audit protection follows symlinks before any C5H/UVT file open. This is an execution interlock, not a scientific certificate.
"""
import ast,hashlib,json,os,sys
from pathlib import Path
ROOT=Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2')
FIXTURES={str((ROOT/p).resolve()) for p in ('runs/KMAX_A2F10_C4R3_D7R3_RUN_V001','runs_ext/KMAX_A2F10_C5R3_RUN_V001','runs_ext/KMAX_A2F10_C6R3_RUN_V001')}
SEALED=False

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def validate_seal(path,want):
    if sha(path)!=want:raise ValueError('SEAL_PIN_MISMATCH')
    seal=json.loads(Path(path).read_bytes())
    if seal.get('sealed_by')!='Claude2 (root)':raise ValueError('ROOT_SEAL_REQUIRED')
    for name in ('prereg','compare'):
        ref=seal[name]
        if sha(ref['path'])!=ref['sha256']:raise ValueError('SEALED_'+name.upper()+'_PIN_MISMATCH')
    tree=ast.parse(Path(seal['compare']['path']).read_bytes());vals={}
    for node in tree.body:
        if isinstance(node,ast.Assign):
            for t in node.targets:
                if isinstance(t,ast.Name) and t.id in ('V007_PREREG_SHA256','PIN_ADDENDUM_V005'):
                    vals[t.id]=ast.literal_eval(node.value)
    if vals.get('V007_PREREG_SHA256')!=seal['prereg']['sha256'] or not isinstance(vals.get('PIN_ADDENDUM_V005'),str) or len(vals['PIN_ADDENDUM_V005'])!=64:
        raise ValueError('COMPARE_NOT_SEALED_V007')
    return seal

def check_path(path,sealed=False):
    if not isinstance(path,(str,bytes,os.PathLike)):return
    p=str(Path(os.fsdecode(path)).resolve())
    if '/runs_ext/UVT_' in p:raise PermissionError('UVT_RUN_READ_FORBIDDEN')
    if '/KMAX_A2F10_C5H_RUN_V001/' in p or p.endswith('/KMAX_A2F10_C5H_RUN_V001'):
        if not sealed:raise PermissionError('C5H_REQUIRES_VERIFIED_V007_SEAL')

def authorize(argv,kind='run'):
    global SEALED
    SEALED=False
    args=list(argv)
    if '--seal' in args or '--seal-sha' in args:
        if '--seal' not in args or '--seal-sha' not in args:raise ValueError('SEAL_PATH_AND_SHA_REQUIRED')
        i=args.index('--seal');sp=args[i+1];del args[i:i+2];i=args.index('--seal-sha');ss=args[i+1];del args[i:i+2]
        validate_seal(sp,ss);SEALED=True
    if not SEALED:
        if kind=='cid':
            if len(args)<2 or args[1]!='C4':raise PermissionError('PRESEAL_SR_ONLY_C4R3_FIXTURE')
        elif kind=='records':
            raise PermissionError('PRODUCTION_AGGREGATION_REQUIRES_SEAL')
        elif len(args)<2 or str(Path(args[1]).resolve()) not in FIXTURES:
            raise PermissionError('PRESEAL_ONLY_NAMED_C4R3_C5R3_C6R3_FIXTURES')
    sys.argv[:]=args
    def audit(event,values):
        if event=='open':check_path(values[0],SEALED)
    sys.addaudithook(audit)
    return {'sealed':SEALED,'mode':'postseal' if SEALED else 'fixture'}
