# verify_targetfree_2 audit-hook fence. Import and call install() before anything else.
# Refuses: any open (read or write) whose path string contains a target-like or protected term; any write, mkdir or
# listing outside the rules below; deletes, renames, process creation, network, truncate, links, chmod.
# String-based on purpose: it never calls realpath on a read path, so it never stats a protected location.
import os, sys

MINE = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/miss_reading_prereg_c4/r2/checks_round2/verify_targetfree_2'
DENY = ('rotmod', 'vobs', 'v_obs', 'massmodels', 'mass_models', 'sparc', 'lelli', 'begeman', 'rotcur', 'rotation_curve',
        'kmax_a2f10_c5h_run_v001', '/uvt_', 'runs_ext', 'c5h_run')
REFUSE = ('os.remove', 'os.rename', 'os.rmdir', 'shutil.rmtree', 'shutil.move', 'subprocess.Popen', 'os.system', 'os.exec',
          'os.posix_spawn', 'os.spawn', 'os.fork', 'os.forkpty', 'pty.spawn', 'socket.connect', 'socket.getaddrinfo',
          'socket.bind', 'os.truncate', 'os.symlink', 'os.link', 'os.chmod', 'os.chown', 'os.utime', 'urllib.Request',
          'ctypes.dlopen')
_on = []


def _s(x):
    if isinstance(x, int) or x is None:
        return None
    return os.fsdecode(x) if isinstance(x, bytes) else str(x)


def _bad(p):
    return any(w in p.lower() for w in DENY)


def _mine(p):
    return os.path.abspath(p).startswith(MINE + os.sep)


def _hook(event, args):
    if event == 'open':
        p = _s(args[0])
        if p is None:
            return
        if _bad(p):
            raise PermissionError('fence_vtf2: refused open of %s' % p)
        mode = args[1] if len(args) > 1 and isinstance(args[1], str) else 'r'
        flags = args[2] if len(args) > 2 and isinstance(args[2], int) else 0
        w = any(c in mode for c in 'wax+') or bool(flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_APPEND | os.O_TRUNC))
        if w and not _mine(p):
            raise PermissionError('fence_vtf2: write outside my folder refused: %s' % p)
    elif event in ('os.listdir', 'os.scandir'):
        p = _s(args[0]) if args else None
        if p and _bad(p):
            raise PermissionError('fence_vtf2: refused listing of %s' % p)
    elif event == 'os.mkdir':
        p = _s(args[0])
        if p and not _mine(p):
            raise PermissionError('fence_vtf2: mkdir outside my folder refused: %s' % p)
    elif event in REFUSE:
        raise PermissionError('fence_vtf2: refused event %s' % event)


def install():
    if not _on:
        sys.addaudithook(_hook)
        _on.append(True)
