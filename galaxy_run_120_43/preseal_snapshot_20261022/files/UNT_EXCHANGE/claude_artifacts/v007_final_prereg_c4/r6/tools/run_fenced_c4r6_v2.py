# Claude4 r6 helper: run SCRIPT under the in-process fence. usage: python3 -I -B run_fenced_c4r6_v2.py FENCE.py FENCE_SHA256 SCRIPT [args]
# v2 supersedes run_fenced_c4r6.py before any use (v1 was never run): v1 called the fence's selftest_v002(), whose path predicates
# realpath (lstat) synthetic probe paths that carry a UVT_ component and the C5H run name; v2 runs neither selftest.
# The fence (fence_c4v002, an audit hook that cannot be removed) is installed FIRST. Its selftest() and selftest_v002() are NOT run
# (selftest() realpaths probes under the CLAUDE2 runs_ext link and a UVT_ name; selftest_v002() realpaths UVT_- and C5H-named
# synthetic paths). Instead five probes that touch no protected path must each be refused by the fence (process creation x2, a
# socket connect, a write outside the r6 folder, a delete inside it), else nothing runs. The BLOCKED entries added after the probes
# are printed at the end (FENCE_C4R6_SUMMARY, stderr).
import hashlib, importlib.util, json, os, runpy, sys

fence_path, fence_sha, script = sys.argv[1], sys.argv[2], sys.argv[3]
raw = open(fence_path, 'rb').read()
if hashlib.sha256(raw).hexdigest() != fence_sha:
    print('RUN_FENCED_REFUSED: fence sha mismatch', file=sys.stderr)
    sys.exit(3)
spec = importlib.util.spec_from_file_location('fence_c4_active', fence_path)
F = importlib.util.module_from_spec(spec)
spec.loader.exec_module(F)


def probes():
    import subprocess, socket
    trials = [
        ('popen', lambda: subprocess.Popen(['/usr/bin/true'])),
        ('os_system', lambda: os.system('true')),
        ('socket_connect', lambda: socket.socket().connect(('127.0.0.1', 9))),
        ('write_outside_r6', lambda: open('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/x_c4r6_fence_probe_should_not_exist.txt', 'x')),
        ('delete', lambda: os.remove(os.path.join(F.REVIEW, 'nonexistent_c4r6_probe'))),
    ]
    out = []
    for name, fn in trials:
        try:
            fn()
            out.append((name, False))
        except PermissionError as e:
            out.append((name, str(e).startswith('FENCE_C4')))
        except Exception:
            out.append((name, False))
    return out


st = probes()
ok = len(st) == 5 and all(v for _, v in st)
if not ok:
    print('RUN_FENCED_REFUSED: probes %s' % (st,), file=sys.stderr)
    sys.exit(3)
n0 = len(F.BLOCKED)
summary = {'fence': os.path.basename(fence_path), 'fence_sha256': fence_sha, 'review_root': F.REVIEW,
           'probes': '%d/%d' % (sum(1 for _, v in st if v), len(st)), 'selftests_not_run': 'selftest() and selftest_v002() (see header)'}
sys.argv = [script] + sys.argv[4:]
rc = 0
try:
    runpy.run_path(script, run_name='__main__')
except SystemExit as exc:
    rc = exc.code if isinstance(exc.code, int) else (0 if exc.code is None else 1)
    if not isinstance(exc.code, int) and exc.code is not None:
        print('SystemExit: %s' % (exc.code,), file=sys.stderr)
finally:
    summary['blocked_after_probes'] = [list(x) for x in F.BLOCKED[n0:]]
    summary['rc'] = rc
    print('FENCE_C4R6_SUMMARY ' + json.dumps(summary), file=sys.stderr)
sys.exit(rc)
