# Claude4 r5 helper: run SCRIPT under the in-process fence. usage: python3 -I -B run_fenced_c4r5.py FENCE.py FENCE_SHA256 SCRIPT [args]
# The fence (audit hook, cannot be removed) is installed FIRST; its selftest must give 8/8 (and selftest_v002 17/17 for v002),
# else nothing runs. The BLOCKED entries added after the selftests are printed at the end (FENCE_C4R5_SUMMARY, stderr).
import hashlib, importlib.util, json, os, runpy, sys

fence_path, fence_sha, script = sys.argv[1], sys.argv[2], sys.argv[3]
raw = open(fence_path, 'rb').read()
if hashlib.sha256(raw).hexdigest() != fence_sha:
    print('RUN_FENCED_REFUSED: fence sha mismatch', file=sys.stderr)
    sys.exit(3)
spec = importlib.util.spec_from_file_location('fence_c4_active', fence_path)
F = importlib.util.module_from_spec(spec)
spec.loader.exec_module(F)
st = F.selftest()
ok1 = len(st) == 8 and all(v for _, v in st)
st2 = F.selftest_v002() if hasattr(F, 'selftest_v002') else []
ok2 = (not hasattr(F, 'selftest_v002')) or (len(st2) == 17 and all(v for _, v in st2))
if not (ok1 and ok2):
    print('RUN_FENCED_REFUSED: selftest %s %s' % (st, st2), file=sys.stderr)
    sys.exit(3)
n0 = len(F.BLOCKED)
summary = {'fence': os.path.basename(fence_path), 'fence_sha256': fence_sha, 'review_root': F.REVIEW,
           'selftest': '%d/%d' % (sum(1 for _, v in st if v), len(st)),
           'selftest_v002': ('%d/%d' % (sum(1 for _, v in st2 if v), len(st2))) if st2 else None}
sys.argv = [script] + sys.argv[4:]
rc = 0
try:
    runpy.run_path(script, run_name='__main__')
except SystemExit as exc:
    rc = exc.code if isinstance(exc.code, int) else (0 if exc.code is None else 1)
finally:
    summary['blocked_after_selftest'] = [list(x) for x in F.BLOCKED[n0:]]
    summary['rc'] = rc
    print('FENCE_C4R5_SUMMARY ' + json.dumps(summary), file=sys.stderr)
sys.exit(rc)
