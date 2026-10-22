# run_fenced_r5chk.py -- run a target script in-process under fence_c4v002 (r5_check helper, Claude4).
# usage: python3 -I -B run_fenced_r5chk.py FENCE.py FENCE_SHA256 TARGET.py [target args ...]
# 1. refuses unless FENCE.py hashes to FENCE_SHA256 (from bytes);
# 2. loads the fence (its audit hook cannot be removed), runs selftest() (8 trials, each must be refused) and
#    selftest_v002() (path predicates, each must hold); refuses otherwise;
# 3. defence in depth OUTSIDE the fence file (stat and directory listing raise no 'open' event): os.stat / os.lstat are
#    wrapped, and a second audit hook covers os.listdir / os.scandir / os.walk / glob.glob; both refuse (PermissionError,
#    nothing touched) any path with the C5H run name, a runs_ext component, a /.vol alias, a uvt_ directory component or a
#    uvt_ non-.py file. Lexical checks only (no realpath inside the guard);
# 4. runs TARGET as __main__ with the given argv; prints one R5CHK_FENCE_SUMMARY JSON line at the end.
import sys, os, hashlib, importlib.util, json, runpy

fp, fsha, target = sys.argv[1], sys.argv[2], sys.argv[3]
targs = sys.argv[4:]
if hashlib.sha256(open(fp, 'rb').read()).hexdigest() != fsha:
    print('RUNNER_REFUSED: fence sha mismatch'); sys.exit(3)
spec = importlib.util.spec_from_file_location('fence_c4v002_r5chk', fp)
F = importlib.util.module_from_spec(spec)
spec.loader.exec_module(F)
st1 = F.selftest()
st2 = F.selftest_v002()
ok1 = len(st1) == 8 and all(r for _, r in st1)
ok2 = len(st2) > 0 and all(r for _, r in st2)
selftest_blocked = list(F.BLOCKED)
n0 = len(F.BLOCKED)
if not (ok1 and ok2):
    print('RUNNER_REFUSED: fence selftest', json.dumps({'selftest': st1, 'selftest_v002': st2})); sys.exit(3)

GUARD_REFUSED = []
def _bad(p):
    try:
        s = os.fsdecode(os.fspath(p))
    except TypeError:
        return None
    low = os.path.abspath(s).casefold()
    comps = low.split(os.sep)
    if 'kmax_a2f10_c5h_run_v001' in low:
        return 'C5H name'
    if 'runs_ext' in comps:
        return 'runs_ext component'
    if low == '/.vol' or low.startswith('/.vol/'):
        return '/.vol alias'
    if any(c.startswith('uvt_') for c in comps[:-1]):
        return 'uvt_ directory component'
    if comps[-1].startswith('uvt_') and not comps[-1].endswith('.py'):
        return 'uvt_ non-py file'
    return None
_real_stat, _real_lstat = os.stat, os.lstat
def _guarded(fn, name):
    def g(p, *a, **k):
        w = _bad(p)
        if w:
            GUARD_REFUSED.append((name, w, str(p)))
            raise PermissionError('R5CHK_STAT_GUARD: %s %s' % (name, w))
        return fn(p, *a, **k)
    return g
os.stat = _guarded(_real_stat, 'os.stat')
os.lstat = _guarded(_real_lstat, 'os.lstat')
LIST_EVENTS = {'os.listdir', 'os.scandir', 'os.walk', 'os.fwalk', 'glob.glob', 'glob.glob/2'}
def _list_hook(event, args):
    if event in LIST_EVENTS and args:
        p = args[0]
        if p is None:
            p = '.'
        w = _bad(p)
        if w:
            GUARD_REFUSED.append((event, w, str(p)))
            raise PermissionError('R5CHK_LIST_GUARD: %s %s' % (event, w))
sys.addaudithook(_list_hook)

sys.argv = [target] + targs
code = 0
try:
    runpy.run_path(target, run_name='__main__')
except SystemExit as e:
    code = e.code if isinstance(e.code, int) else (0 if e.code is None else 1)
summary = {'fence': {'path': fp, 'sha256': fsha}, 'selftest': '%d/%d' % (sum(1 for _, r in st1 if r), len(st1)),
           'selftest_v002': '%d/%d' % (sum(1 for _, r in st2 if r), len(st2)),
           'selftest_blocked_count': len(selftest_blocked),
           'blocked_after_selftests': F.BLOCKED[n0:], 'stat_list_guard_refused': GUARD_REFUSED, 'exit_code': code,
           'target': target}
print('R5CHK_FENCE_SUMMARY ' + json.dumps(summary))
sys.exit(code)
