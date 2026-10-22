# Claude3 seal-assembly builder (0626): in-process fence (c3v003: as c3v002 without the ctypes.dlopen refusal, which numpy's import-time
# probing trips harmlessly; c3v002 superseded fence_c3sa.py, whose self-test could touch real paths if the fence failed), armed BEFORE any foreign code executes. Read-only by default.
# Refuses (PermissionError, counted) every os.stat / os.lstat / os.readlink / os.access / open / os.listdir / os.scandir / chdir /
# link / symlink / rename / remove / rmdir / mkdir / subprocess / exec / spawn / fork / socket of a FORBIDDEN path or kind:
#   the registered C5H run name, any runs_ext path, any UVT_* component, /.vol, SPARC / NGC target spellings;
# every write (open with w/a/x/+, mkdir, rename, remove) outside the allowed write roots; every process start and network use.
import os, sys
FENCE = {'refused': 0, 'events': [], 'write_roots': (), 'armed': False}
_FORBID_SUBSTR = ('kmax_a2f10_c5h_run_v001', '/runs_ext', 'runs_ext/', '/uvt_', 'sparc', 'ngc3198_target', 'ngc_target', 'rotmod')
def _s(p):
    if isinstance(p, int):
        return None
    try:
        return os.fsdecode(p) if isinstance(p, (bytes, os.PathLike)) else str(p)
    except Exception:
        return None
def forbidden(p):
    s = _s(p)
    if s is None:
        return False
    sl = s.casefold()
    if sl.lstrip('/').startswith('.vol') or sl.startswith('//.vol'):
        return True
    return any(x in sl for x in _FORBID_SUBSTR)
def _refuse(kind, p):
    FENCE['refused'] += 1
    FENCE['events'].append((kind, (_s(p) or repr(p))[:200]))
    raise PermissionError('C3SA_FENCE_REFUSED %s %s' % (kind, (_s(p) or repr(p))[:160]))
def _in_write_roots(p):
    s = _s(p)
    if s is None:
        return False
    a = os.path.abspath(s)
    return any(a == r or a.startswith(r.rstrip('/') + '/') for r in FENCE['write_roots'])
_ostat, _olstat, _oreadlink, _oaccess = os.stat, os.lstat, os.readlink, os.access
def _stat(p, *a, **k):
    if forbidden(p): _refuse('stat', p)
    return _ostat(p, *a, **k)
def _lstat(p, *a, **k):
    if forbidden(p): _refuse('lstat', p)
    return _olstat(p, *a, **k)
def _readlink(p, *a, **k):
    if forbidden(p): _refuse('readlink', p)
    return _oreadlink(p, *a, **k)
def _access(p, *a, **k):
    if forbidden(p): _refuse('access', p)
    return _oaccess(p, *a, **k)
_PATH_EVENTS = ('open', 'os.listdir', 'os.scandir', 'os.chdir', 'os.link', 'os.symlink', 'os.rename', 'os.remove', 'os.rmdir',
                'os.mkdir', 'shutil.rmtree', 'os.truncate', 'os.utime', 'os.chmod', 'os.chown', 'shutil.copyfile', 'shutil.move')
_WRITE_EVENTS = ('os.link', 'os.symlink', 'os.rename', 'os.remove', 'os.rmdir', 'os.mkdir', 'shutil.rmtree', 'os.truncate',
                 'os.utime', 'os.chmod', 'os.chown', 'shutil.copyfile', 'shutil.move')
_PROC_EVENTS = ('subprocess.Popen', 'os.system', 'os.exec', 'os.posix_spawn', 'os.spawn', 'os.fork', 'os.forkpty', 'os.startfile',
                'socket.connect', 'socket.bind', 'socket.getaddrinfo', 'socket.sendto', 'urllib.Request', 'pty.spawn')
def _hook(ev, args):
    if not FENCE['armed']:
        return
    if ev in _PROC_EVENTS:
        _refuse(ev, args[0] if args else '')
    if ev in _PATH_EVENTS and args:
        p = args[0]
        if forbidden(p):
            _refuse(ev, p)
        if ev in _WRITE_EVENTS and not _in_write_roots(p):
            _refuse(ev + '(write outside roots)', p)
        if ev == 'open':
            mode = args[1] if len(args) > 1 else 'r'
            flags = args[2] if len(args) > 2 else 0
            w = (isinstance(mode, str) and any(c in mode for c in 'wax+')) or (isinstance(flags, int) and flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND))
            if w and not isinstance(p, int) and not _in_write_roots(p):
                _refuse('open-write(outside roots)', p)
def arm(write_roots=()):
    FENCE['write_roots'] = tuple(os.path.abspath(r) for r in write_roots)
    os.stat, os.lstat, os.readlink, os.access = _stat, _lstat, _readlink, _access
    if not FENCE.get('hooked'):
        sys.addaudithook(_hook)
        FENCE['hooked'] = True
    FENCE['armed'] = True
def selftest():
    """Every forbidden kind refuses before the syscall. Probes use nonexistent fake paths (/Users/c3sa_fake/...) or sys.audit()
    directly, so a probe that is NOT refused still touches nothing real. Returns (not_refused, n_refused); expected ([], 11)."""
    F = '/Users/c3sa_fake'
    probes = [('stat_c5h', lambda: os.stat(F + '/CLAUDE2/runs_ext/KMAX_A2F10_C5H_RUN_V001')),
              ('lstat_uvt', lambda: os.lstat(F + '/x/runs_ext/UVT_Z2_A2F10_R5_RUN_V001')),
              ('realpath_c5h', lambda: os.path.realpath(F + '/runs_ext/KMAX_A2F10_C5H_RUN_V001/result.json')),
              ('readlink_runs_ext', lambda: os.readlink(F + '/runs_ext')),
              ('access_uvt', lambda: os.access(F + '/UVT_A', os.R_OK)),
              ('open_vol_audit', lambda: sys.audit('open', '/.vol/1/2', 'rb', 0)),
              ('listdir_audit', lambda: sys.audit('os.listdir', F + '/CLAUDE2/runs_ext')),
              ('scandir_audit', lambda: sys.audit('os.scandir', F + '/runs_ext/UVT_A')),
              ('popen_audit', lambda: sys.audit('subprocess.Popen', '/nonexistent/c3sa_never', ['/nonexistent/c3sa_never'], None, None)),
              ('socket_audit', lambda: sys.audit('socket.connect', None, ('127.0.0.1', 9))),
              ('write_outside_audit', lambda: sys.audit('open', '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/C3SA_NEVER.txt', 'x', 0))]
    before = FENCE['refused']
    not_refused = []
    for name, fn in probes:
        try:
            fn()
            not_refused.append(name)
        except PermissionError:
            pass
        except Exception as e:
            not_refused.append('%s:%s' % (name, type(e).__name__))
    n = FENCE['refused'] - before
    FENCE['refused'] = before          # self-test refusals are not counted as run events
    FENCE['events'] = []
    return not_refused, n
