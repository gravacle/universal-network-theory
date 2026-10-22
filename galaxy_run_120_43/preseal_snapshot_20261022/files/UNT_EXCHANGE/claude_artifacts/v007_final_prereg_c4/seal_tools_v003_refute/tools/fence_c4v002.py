# Claude4 0562/0565: in-process safety fence for every review tool here (Python audit hook; cannot be removed once added).
# It raises PermissionError, so the operation never happens, on:
#  - any process creation (subprocess, os.system/exec/spawn/fork, pty), any os.kill, and any network socket use;
#  - any delete (os.remove/unlink/rmdir, shutil.rmtree);
#  - any write, create, rename, link or chmod outside this review folder;
#  - any open, inside or outside this folder, of a real run tree (both CLAUDE2 runs_ext roots), a UVT_* component,
#    the C5H run name, or observed-velocity/target data (rotmod, Vobs, MassModels, SPARC, NGC3198 data).
#    The one exception is my own synthetic look-alikes, which live in this folder.
# Every open of a path inside LOOKALIKES is logged with a stack tag: is it the guard's own marker read, or a body read?
# v002 (Claude4 seal tools v002, task rule 5): the ONLY change from fence_c4v001 (f813c430) is two READ-ONLY exceptions
# to the open rules (writes outside this folder stay refused for every path):
#  (a) a uvt_*.py SOURCE module (basename starts with lowercase 'uvt_' and ends with '.py'; no directory component starts
#      with uvt_, any case) outside both runs_ext roots; a .pyc, a UVT_* directory or anything under runs_ext stays refused;
#  (b) the root decision files CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V00*_ADDENDUM*.md (directory exactly the
#      CLAUDE2 control folder, literal and resolved path both), which are decision records, not data (rehearsal D-11).
#      Scratch copies of them inside this folder were already readable (this folder is exempt), unchanged.
import fnmatch, os, sys

REVIEW = os.path.realpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
LOOKALIKES = os.path.join(REVIEW, 'sandbox')
RUNS_EXT = (
    '/Volumes/External1/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs_ext',
    '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs_ext',
)
TARGET_WORDS = ('rotmod', 'vobs', 'massmodels', 'sparc')
CTRL_C2 = '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2'   # v002 (b)
CTRL_C2_DIRS = (CTRL_C2, os.path.realpath(CTRL_C2))                                                                         # v002 (b)
ROOT_DECISION_GLOB = 'ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V00*_ADDENDUM*.md'                                    # v002 (b)
PROCESS_EVENTS = {'subprocess.Popen', 'os.system', 'os.exec', 'os.posix_spawn', 'os.spawn', 'os.fork', 'os.forkpty',
                  'pty.spawn', 'os.startfile', 'os.kill', 'os.killpg', 'signal.pthread_kill'}
NET_EVENTS = {'socket.connect', 'socket.bind', 'socket.sendto', 'socket.sendmsg', 'socket.getaddrinfo',
              'socket.gethostbyname', 'urllib.Request', 'http.client.connect', 'ftplib.connect', 'smtplib.connect'}
DELETE_EVENTS = {'os.remove', 'os.rmdir', 'shutil.rmtree'}
WRITE_PATH_EVENTS = {'os.mkdir': (0,), 'os.rename': (0, 1), 'os.symlink': (1,), 'os.link': (1,), 'os.truncate': (0,),
                     'os.chmod': (0,), 'os.chown': (0,), 'os.utime': (0,), 'shutil.copyfile': (1,), 'shutil.copytree': (1,),
                     'shutil.move': (0, 1), 'os.chflags': (0,), 'os.lchflags': (0,), 'os.setxattr': (0,), 'os.removexattr': (0,)}
OPEN_LOG = []      # (path, writing, tag) for every open whose real or literal path is inside LOOKALIKES
BLOCKED = []       # (event, detail) for every refused operation
_GUARD_FILE = os.path.realpath('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/producer_guard_cx1v007.py')


def _s(x):
    if x is None or isinstance(x, int):
        return None
    if isinstance(x, bytes):
        return os.fsdecode(x)
    try:
        return os.fspath(x)
    except TypeError:
        return None


def _under(p, root):
    return p == root or p.startswith(root + os.sep)


def _uvt_source_module(p):
    """v002 (a): True only for <dirs>/uvt_*.py where the basename starts with lowercase 'uvt_' and ends with '.py' and no
    directory component starts with uvt_ (any case).  The runs_ext test in _forbidden_read runs first and is unchanged."""
    parts = p.split(os.sep)
    base = parts[-1]
    if not (base.startswith('uvt_') and base.endswith('.py')):
        return False
    return not any(x.casefold().startswith('uvt_') for x in parts[:-1])


def _root_decision_addendum(p):
    """v002 (b): True only for CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V00*_ADDENDUM*.md (exact folder)."""
    d, b = os.path.split(p)
    return d in CTRL_C2_DIRS and fnmatch.fnmatchcase(b, ROOT_DECISION_GLOB)


def _forbidden_read(lit, real):
    if any(_under(p, r) for p in (lit, real) for r in RUNS_EXT):
        return 'real run tree'
    if _under(real, REVIEW):
        return None  # my own synthetic look-alikes may carry protected-looking names
    for p in (lit, real):
        low = p.casefold()
        if any(x.startswith('uvt_') for x in low.split(os.sep)) and not _uvt_source_module(p):   # v002 (a)
            return 'UVT component'
        if 'kmax_a2f10_c5h_run_v001' in low:
            return 'C5H name'
        if any(w in low for w in TARGET_WORDS):
            return 'target word'
        if ('ngc3198' in low or 'ngc_3198' in low) and not low.endswith('.py') and not _root_decision_addendum(p):   # v002 (b)
            return 'NGC3198 data'
    return None


def _writing(mode, flags):
    if isinstance(mode, str) and any(c in mode for c in 'wax+'):
        return True
    if isinstance(flags, int) and flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_APPEND | os.O_TRUNC):
        return True
    return False


def _tag():
    f = sys._getframe(2)
    while f is not None:
        if f.f_code.co_name == 'marker_hit' and os.path.realpath(f.f_code.co_filename) == _GUARD_FILE:
            return 'guard_marker_read'
        f = f.f_back
    return 'body_or_other'


def _refuse(event, detail):
    BLOCKED.append((event, str(detail)))
    raise PermissionError('FENCE_C4: %s %s' % (event, detail))


def _hook(event, args):
    if event in PROCESS_EVENTS:
        _refuse(event, args[:2] if isinstance(args, tuple) else args)
    if event in NET_EVENTS:
        _refuse(event, args[:2] if isinstance(args, tuple) else args)
    if event in DELETE_EVENTS:
        _refuse(event, args[:1])
    if event in WRITE_PATH_EVENTS:
        for i in WRITE_PATH_EVENTS[event]:
            p = _s(args[i]) if len(args) > i else None
            if p is None:
                continue
            ap = os.path.abspath(p)
            real = os.path.join(os.path.realpath(os.path.dirname(ap)), os.path.basename(ap))
            if not _under(real, REVIEW):
                _refuse(event, p)
        return
    if event == 'open':
        p = _s(args[0])
        if p is None:
            return
        lit = os.path.abspath(p)
        real = os.path.realpath(lit)
        why = _forbidden_read(lit, real)
        if why:
            _refuse('open(%s)' % why, p)
        if _writing(args[1] if len(args) > 1 else None, args[2] if len(args) > 2 else None):
            parent_real = os.path.join(os.path.realpath(os.path.dirname(lit)), os.path.basename(lit))
            if not (_under(real, REVIEW) and _under(parent_real, REVIEW)):
                _refuse('open(write outside review)', p)
        if _under(real, LOOKALIKES) or _under(lit, LOOKALIKES):
            OPEN_LOG.append((real, _writing(args[1] if len(args) > 1 else None, args[2] if len(args) > 2 else None), _tag()))


sys.addaudithook(_hook)


def selftest():
    """Each forbidden class must raise; returns the list of (name, refused)."""
    out = []
    import subprocess, socket
    trials = [
        ('popen', lambda: subprocess.Popen(['/usr/bin/true'])),
        ('os_system', lambda: os.system('true')),
        ('socket_connect', lambda: socket.socket().connect(('127.0.0.1', 9))),
        ('write_outside', lambda: open('/private/tmp/claude4_fence_probe_should_not_exist.txt', 'x')),
        ('read_runs_ext', lambda: open(RUNS_EXT[1] + '/probe_should_not_exist.json', 'rb')),
        ('read_uvt', lambda: open('/Users/bgm/Research/UVT_probe_should_not_exist/x.json', 'rb')),
        ('read_target', lambda: open('/Users/bgm/Research/x_rotmod_probe_should_not_exist.dat', 'rb')),
        ('delete', lambda: os.remove(os.path.join(REVIEW, 'nonexistent_probe'))),
    ]
    for name, fn in trials:
        try:
            fn()
            out.append((name, False))
        except PermissionError as e:
            out.append((name, str(e).startswith('FENCE_C4')))
        except Exception:
            out.append((name, False))
    return out
