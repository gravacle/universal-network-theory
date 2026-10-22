# Claude4 r6 refute helper (r6_check): run SCRIPT under the in-process fence and log every open.
# usage: python3 -I -B run_fenced_r6chk.py FENCE.py FENCE_SHA256 OPENLOG.json SCRIPT [args]
# - The fence (a byte copy of r6/tools/fence_c4v002.py, 53078e39, placed in r6_check/tools so that its review root is r6_check)
#   is installed FIRST, after its bytes are checked against FENCE_SHA256.
# - Its selftest() and selftest_v002() are NOT run: their probes realpath (lstat) paths under the CLAUDE2 runs_ext link and
#   UVT_/C5H-named synthetic paths. Instead five probes that touch no protected path must each be refused (process creation x2,
#   a socket connect, a write outside r6_check, a delete inside r6_check), else nothing runs.
# - A second audit hook records every open (path, write flag) and every os.listdir/os.scandir path. At exit the runner writes
#   OPENLOG.json by exclusive create (inside r6_check; the fence refuses anything else) with the distinct paths, and flags any
#   path in a protected class (runs_ext, a UVT_ component, the C5H run name, target words, NGC3198 data other than the root
#   decision addenda and .py sources). The fence's BLOCKED entries after the probes are reported too.
import hashlib, importlib.util, json, os, runpy, sys

fence_path, fence_sha, openlog, script = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
raw = open(fence_path, 'rb').read()
if hashlib.sha256(raw).hexdigest() != fence_sha:
    print('RUN_FENCED_REFUSED: fence sha mismatch', file=sys.stderr)
    sys.exit(3)
spec = importlib.util.spec_from_file_location('fence_c4_active', fence_path)
F = importlib.util.module_from_spec(spec)
spec.loader.exec_module(F)

OPENS = []
LISTS = []


def _rec(event, args):
    if event == 'open':
        p = args[0] if args else None
        if isinstance(p, (str, bytes, os.PathLike)):
            try:
                p = os.fsdecode(os.fspath(p))
            except Exception:
                return
            mode = args[1] if len(args) > 1 else None
            flags = args[2] if len(args) > 2 else None
            OPENS.append((os.path.abspath(p), F._writing(mode, flags)))
    elif event in ('os.listdir', 'os.scandir'):
        p = args[0] if args else None
        if isinstance(p, (str, bytes, os.PathLike)):
            try:
                LISTS.append(os.path.abspath(os.fsdecode(os.fspath(p))))
            except Exception:
                pass


sys.addaudithook(_rec)


def probes():
    import subprocess, socket
    trials = [
        ('popen', lambda: subprocess.Popen(['/usr/bin/true'])),
        ('os_system', lambda: os.system('true')),
        ('socket_connect', lambda: socket.socket().connect(('127.0.0.1', 9))),
        ('write_outside_r6_check', lambda: open('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/x_r6chk_fence_probe_should_not_exist.txt', 'x')),
        ('delete', lambda: os.remove(os.path.join(F.REVIEW, 'nonexistent_r6chk_probe'))),
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


def protected_class(p):
    low = p.casefold()
    comps = low.split(os.sep)
    if 'runs_ext' in comps:
        return 'runs_ext'
    if any(x.startswith('uvt_') for x in comps[:-1]) or (comps[-1].startswith('uvt_') and not comps[-1].endswith('.py')):
        return 'UVT component'
    if 'kmax_a2f10_c5h_run_v001' in low:
        return 'C5H name'
    if any(w in low for w in F.TARGET_WORDS):
        return 'target word'
    if ('ngc3198' in low or 'ngc_3198' in low) and not low.endswith('.py'):
        base = os.path.basename(p)
        import fnmatch
        if fnmatch.fnmatchcase(base, F.ADDENDUM_GLOB):
            return None
        return 'NGC3198 name'
    return None


st = probes()
ok = len(st) == 5 and all(v for _, v in st)
if not ok:
    print('RUN_FENCED_REFUSED: probes %s' % (st,), file=sys.stderr)
    sys.exit(3)
n0 = len(F.BLOCKED)
n_open0 = len(OPENS)
n_list0 = len(LISTS)
summary = {'fence': os.path.basename(fence_path), 'fence_sha256': fence_sha, 'review_root': F.REVIEW,
           'probes': '%d/%d' % (sum(1 for _, v in st if v), len(st)), 'selftests_not_run': 'selftest() and selftest_v002() (see header)'}
sys.argv = [script] + sys.argv[5:]
rc = 0
try:
    runpy.run_path(script, run_name='__main__')
except SystemExit as exc:
    rc = exc.code if isinstance(exc.code, int) else (0 if exc.code is None else 1)
    if not isinstance(exc.code, int) and exc.code is not None:
        print('SystemExit: %s' % (exc.code,), file=sys.stderr)
finally:
    opens = OPENS[n_open0:]
    lists = LISTS[n_list0:]
    distinct = sorted(set(p for p, _ in opens))
    writes = sorted(set(p for p, w in opens if w))
    flagged = sorted(set((p, protected_class(p)) for p in distinct + sorted(set(lists)) if protected_class(p)))
    summary['blocked_after_probes'] = [list(x) for x in F.BLOCKED[n0:]]
    summary['rc'] = rc
    summary['opens_distinct'] = len(distinct)
    summary['write_opens_distinct'] = writes
    summary['listdirs_distinct'] = sorted(set(lists))
    summary['protected_class_paths'] = [list(x) for x in flagged]
    rec = dict(summary, opened_paths=distinct)
    try:
        with open(openlog, 'x') as fh:
            json.dump(rec, fh, indent=1)
    except Exception as e:
        summary['openlog_error'] = '%s: %s' % (type(e).__name__, e)
    print('FENCE_R6CHK_SUMMARY ' + json.dumps({k: v for k, v in summary.items() if k not in ('listdirs_distinct',)}), file=sys.stderr)
sys.exit(rc)
