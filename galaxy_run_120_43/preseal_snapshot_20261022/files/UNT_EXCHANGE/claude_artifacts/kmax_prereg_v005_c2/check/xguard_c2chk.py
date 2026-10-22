"""Audit-hook guard (checker): run a python script with argv, refusing process creation, any write outside
ALLOW_WRITE, and any open of a V005-run or DDO154_ROUTE_B_C2V005_* path (read or write).
usage: python3 -I -B xguard_c2chk.py ALLOW_WRITE_DIR SCRIPT [ARGS...]
"""
import os
import runpy
import sys

ALLOW = os.path.realpath(sys.argv[1])
SCRIPT = sys.argv[2]
RUNS = '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs/'
DENIED = []


def forbidden_read(p):
    if not p.startswith(RUNS):
        return False
    rest = p[len(RUNS):]
    top = rest.split('/')[0]
    return ('_V005_RUN_V001' in top) or top.startswith('DDO154_ROUTE_B_C2V005_') or ('D7R1' in top)


def hook(ev, args):
    if ev in ('subprocess.Popen', 'os.system', 'os.exec', 'os.posix_spawn', 'os.spawn', 'os.fork', 'os.forkpty'):
        DENIED.append((ev, str(args)[:200]))
        raise PermissionError('xguard: process creation denied (%s)' % ev)
    if ev == 'open':
        path, mode, flags = args[0], args[1], args[2]
        if not isinstance(path, (str, bytes, os.PathLike)):
            return
        p = os.path.realpath(os.fsdecode(path))
        w = (mode is not None and any(c in str(mode) for c in 'wax+')) or (flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_APPEND | os.O_TRUNC))
        if forbidden_read(p):
            DENIED.append(('open-forbidden', p))
            raise PermissionError('xguard: forbidden path %s' % p)
        if w and not (p == ALLOW or p.startswith(ALLOW + os.sep)):
            DENIED.append(('write', p))
            raise PermissionError('xguard: write outside allow dir: %s' % p)
    if ev in ('os.mkdir', 'os.rename', 'os.remove', 'os.rmdir', 'shutil.rmtree', 'os.symlink', 'os.link', 'os.chmod', 'os.truncate'):
        p = os.path.realpath(os.fsdecode(args[0])) if args and isinstance(args[0], (str, bytes, os.PathLike)) else ''
        if not (p == ALLOW or p.startswith(ALLOW + os.sep)):
            DENIED.append((ev, p))
            raise PermissionError('xguard: %s outside allow dir: %s' % (ev, p))


sys.addaudithook(hook)
sys.argv = [SCRIPT] + sys.argv[3:]
try:
    runpy.run_path(SCRIPT, run_name='__main__')
except SystemExit as e:
    print('xguard: exit', e.code, 'denied', DENIED, file=sys.stderr)
    raise
print('xguard: denied', DENIED, file=sys.stderr)
