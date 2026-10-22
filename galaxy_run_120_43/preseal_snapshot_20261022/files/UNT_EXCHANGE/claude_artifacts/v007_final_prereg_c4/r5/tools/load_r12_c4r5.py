# Claude4 r5 helper: load compare r12 cx3v002 (4bd7b262, selected by SELECTED_R12_CX3V001 91aa9747) in-process and UNMODIFIED,
# so its own validate_case_block can be called. Its bytes are verified first; it is exec'd under a module name that is not
# __main__ (main() never runs). Defence in depth (the fence is the primary guard, installed before this module):
#  - C5H_REGISTERED_RUN_DIRS is redirected to a stand-in path that is never created, so any code path that would stat the
#    registered C5H run reads 'identity unavailable' and refuses (A79.3) instead of touching it (validate_case_block does not
#    use it: FORMAL, from its code);
#  - os.stat / os.lstat refuse any path naming the registered C5H run, any runs_ext/UVT_* path and any /.vol path (stat raises
#    no audit event, so the fence cannot see it). GUARD['refused'] counts refusals (expected 0).
import hashlib, os, sys, types
from pathlib import Path

CMP = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r12/kmax_tail_compare_c2v007_r12_cx3v002.py'
CMP_SHA = '4bd7b262caae26f2de146cee803dd689a1f4e565cb67552f04e6d6b97188dd28'
HERE = Path(__file__).resolve().parent
STANDIN = HERE.parent / 'out' / 'C5H_REGISTERED_RUN_STANDIN_NEVER_CREATED'
GUARD = {'refused': 0, 'events': []}
_C5H = 'kmax_a2f10_c5h_run_v001'


def _forbidden_stat(p):
    if isinstance(p, int):
        return False
    try:
        s = os.fsdecode(p) if isinstance(p, bytes) else os.fspath(p)
    except TypeError:
        return False
    low = s.casefold()
    return (_C5H in low) or ('/runs_ext/uvt_' in low) or low.startswith('/.vol')


_ostat, _olstat = os.stat, os.lstat


def _stat(p, *a, **k):
    if _forbidden_stat(p):
        GUARD['refused'] += 1
        GUARD['events'].append(('stat', str(p)[:160]))
        raise PermissionError('LOAD_R12_C4R5_STAT_GUARD %s' % str(p)[:120])
    return _ostat(p, *a, **k)


def _lstat(p, *a, **k):
    if _forbidden_stat(p):
        GUARD['refused'] += 1
        GUARD['events'].append(('lstat', str(p)[:160]))
        raise PermissionError('LOAD_R12_C4R5_STAT_GUARD %s' % str(p)[:120])
    return _olstat(p, *a, **k)


os.stat, os.lstat = _stat, _lstat


def load():
    raw = Path(CMP).read_bytes()
    if hashlib.sha256(raw).hexdigest() != CMP_SHA:
        raise SystemExit('LOAD_R12_C4R5: compare bytes are not 4bd7b262')
    name = 'kmax_tail_compare_c2v007_r12_cx3v002_c4r5'
    if name in sys.modules:
        return sys.modules[name]
    m = types.ModuleType(name)
    m.__file__ = CMP
    sys.modules[name] = m
    exec(compile(raw.decode('utf-8'), CMP, 'exec'), m.__dict__)
    m.C5H_REGISTERED_RUN_DIRS = (str(STANDIN),)
    return m
