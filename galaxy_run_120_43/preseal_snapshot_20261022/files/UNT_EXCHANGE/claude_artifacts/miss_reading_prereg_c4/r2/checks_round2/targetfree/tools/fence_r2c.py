# R2-C lens (target-free and tools) audit-hook fence. Import and call install() first.
# Refuses: any open (read or write) whose path string contains a target-like or protected term; any write outside this
# lens folder; deletes, renames, process creation, network, truncate, links, chmod; listdir/scandir of refused paths.
# String-based on purpose: it never calls realpath on a read path, so it never stats a protected location.
import os, sys

LENS = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/miss_reading_prereg_c4/r2/checks_round2/targetfree'
DENY = ('rotmod', 'vobs', 'v_obs', 'massmodels', 'mass_models', 'sparc', 'lelli', 'begeman', 'rotcur', 'rotation_curve',
        'kmax_a2f10_c5h_run_v001', '/uvt_', 'runs_ext', 'c5h_run')
REFUSE_EVENTS = ('os.remove', 'os.rename', 'os.rmdir', 'shutil.rmtree', 'shutil.move', 'subprocess.Popen', 'os.system',
                 'os.exec', 'os.posix_spawn', 'os.spawn', 'os.fork', 'os.forkpty', 'pty.spawn', 'socket.connect',
                 'socket.getaddrinfo', 'socket.bind', 'os.truncate', 'os.symlink', 'os.link', 'os.chmod', 'os.chown',
                 'os.utime', 'urllib.Request', 'ctypes.dlopen')
_installed = []


def _p(x):
    if isinstance(x, int) or x is None:
        return None
    return os.fsdecode(x) if isinstance(x, bytes) else str(x)


def _deny(p):
    low = p.lower()
    return any(w in low for w in DENY)


def _hook(event, args):
    if event == 'open':
        p = _p(args[0])
        if p is None:
            return
        if _deny(p):
            raise PermissionError('fence_r2c: refused open of protected/target-like path: %s' % p)
        mode = args[1] if len(args) > 1 and isinstance(args[1], str) else 'r'
        flags = args[2] if len(args) > 2 and isinstance(args[2], int) else 0
        writing = any(c in mode for c in 'wax+') or bool(flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_APPEND | os.O_TRUNC))
        if writing:
            ap = os.path.abspath(p)
            if not ap.startswith(LENS + os.sep):
                raise PermissionError('fence_r2c: write outside the lens folder refused: %s' % p)
    elif event in ('os.listdir', 'os.scandir'):
        p = _p(args[0]) if args else None
        if p and _deny(p):
            raise PermissionError('fence_r2c: refused listing of %s' % p)
    elif event == 'os.mkdir':
        p = _p(args[0])
        if p and not os.path.abspath(p).startswith(LENS + os.sep):
            raise PermissionError('fence_r2c: mkdir outside the lens folder refused: %s' % p)
    elif event in REFUSE_EVENTS:
        raise PermissionError('fence_r2c: refused event %s' % event)


def install():
    if not _installed:
        sys.addaudithook(_hook)
        _installed.append(True)
