"""Checker guard: run SCRIPT as __main__; refuse process creation and any write outside this check/ dir. usage: chk_guard.py LOG SCRIPT args"""
import json, os, runpy, sys
ROOT = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/kmax_prereg_v005_c2/extension_c5c6/v006_r1/check/'
den, wr = [], set()
def hook(ev, a):
    if ev in ('subprocess.Popen', 'os.system', 'os.posix_spawn', 'os.fork', 'os.forkpty') or ev.startswith(('os.exec', 'os.spawn')):
        den.append(ev); raise PermissionError('chk_guard: ' + ev)
    if ev == 'open' and isinstance(a[0], (str, bytes, os.PathLike)):
        p = os.path.abspath(os.fsdecode(a[0])); m, f = a[1], a[2]
        w = (isinstance(m, str) and any(c in m for c in 'wax+')) or (isinstance(f, int) and f & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_APPEND | os.O_TRUNC))
        if w:
            if not p.startswith(ROOT): den.append('write ' + p); raise PermissionError('chk_guard write ' + p)
            wr.add(p)
    if ev in ('os.mkdir', 'os.rename', 'os.remove', 'os.rmdir', 'os.unlink', 'os.replace') and isinstance(a[0], (str, bytes, os.PathLike)):
        p = os.path.abspath(os.fsdecode(a[0]))
        if not p.startswith(ROOT): den.append(ev + ' ' + p); raise PermissionError('chk_guard ' + ev + ' ' + p)
log = sys.argv[1]; sys.argv = sys.argv[2:]
sys.addaudithook(hook)
code = 0
try:
    runpy.run_path(sys.argv[0], run_name='__main__')
except SystemExit as e:
    code = e.code if isinstance(e.code, int) else (0 if e.code is None else 1)
except BaseException as e:
    code = 'EXC %s: %s' % (type(e).__name__, e)
open(log, 'w').write(json.dumps({'exit': code, 'denied': den, 'writes': sorted(wr)}, indent=1))
sys.exit(code if isinstance(code, int) else 1)
