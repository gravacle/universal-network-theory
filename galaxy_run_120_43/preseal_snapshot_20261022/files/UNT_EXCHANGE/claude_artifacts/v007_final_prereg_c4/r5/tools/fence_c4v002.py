# Claude4 0562/0565: in-process safety fence for every review tool here (Python audit hook; cannot be removed once added).
# It raises PermissionError, so the operation never happens, on:
#  - any process creation (subprocess, os.system/exec/spawn/fork, pty), any os.kill, and any network socket use;
#  - any delete (os.remove/unlink/rmdir, shutil.rmtree);
#  - any write, create, rename, link or chmod outside this review folder;
#  - any open, inside or outside this folder, of a real run tree (both CLAUDE2 runs_ext roots), a UVT_* component,
#    the C5H run name, or observed-velocity/target data (rotmod, Vobs, MassModels, SPARC, NGC3198 data).
#    The one exception is my own synthetic look-alikes, which live in this folder.
# Every open of a path inside LOOKALIKES is logged with a stack tag: is it the guard's own marker read, or a body read?
# v002 (Claude4 r5 helper; prereg r5 / V007 case block): ONLY two READ-ONLY exceptions are added; every other block is unchanged.
#  (a) uvt_*.py SOURCE modules outside every runs_ext tree: in both the literal and the real path the basename (casefolded)
#      starts 'uvt_' and ends '.py', no directory component starts 'uvt_', and no component is 'runs_ext';
#  (b) the root decision addenda CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V00*_ADDENDUM*.md (decision records,
#      not data; seal rehearsal D-11), literal and real path directly in the CLAUDE2 control folder. Scratch copies of them
#      inside this folder were already readable under v001's in-folder rule, so they need no change.
#  Both apply only to an open WITHOUT a write flag, and each lifts only its own rule: the real-run-tree, C5H-name and
#  target-word rules still apply to the same path. Writes outside this folder stay refused by the unchanged write rule.
import fnmatch, os, sys

REVIEW = os.path.realpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
LOOKALIKES = os.path.join(REVIEW, 'sandbox')
RUNS_EXT = (
    '/Volumes/External1/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs_ext',
    '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs_ext',
)
TARGET_WORDS = ('rotmod', 'vobs', 'massmodels', 'sparc')
CLAUDE2_CTRL = '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2'  # v002 (b)
_CLAUDE2_REAL = os.path.realpath(CLAUDE2_CTRL)                                                                              # v002 (b)
ADDENDUM_GLOB = 'ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V00*_ADDENDUM*.md'                                          # v002 (b)
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


def _uvt_source_exception(lit, real):
    """v002 (a): a uvt_*.py source module outside every runs_ext tree (applied to reads only)."""
    for p in (lit, real):
        comps = p.casefold().split(os.sep)
        if not (comps[-1].startswith('uvt_') and comps[-1].endswith('.py')):
            return False
        if any(x.startswith('uvt_') for x in comps[:-1]) or 'runs_ext' in comps:
            return False
    return True


def _addendum_exception(lit, real):
    """v002 (b): a root decision addendum directly in the CLAUDE2 control folder (applied to reads only)."""
    return (os.path.dirname(lit) in (CLAUDE2_CTRL, _CLAUDE2_REAL) and os.path.dirname(real) == _CLAUDE2_REAL
            and fnmatch.fnmatchcase(os.path.basename(lit), ADDENDUM_GLOB)
            and fnmatch.fnmatchcase(os.path.basename(real), ADDENDUM_GLOB))


def _forbidden_read(lit, real, writing=True):
    if any(_under(p, r) for p in (lit, real) for r in RUNS_EXT):
        return 'real run tree'
    if _under(real, REVIEW):
        return None  # my own synthetic look-alikes may carry protected-looking names
    ex_a = (not writing) and _uvt_source_exception(lit, real)        # v002 (a), read only
    ex_b = (not writing) and _addendum_exception(lit, real)          # v002 (b), read only
    for p in (lit, real):
        low = p.casefold()
        comps = low.split(os.sep)
        if any(x.startswith('uvt_') for x in (comps[:-1] if ex_a else comps)):
            return 'UVT component'
        if 'kmax_a2f10_c5h_run_v001' in low:
            return 'C5H name'
        if any(w in low for w in TARGET_WORDS):
            return 'target word'
        if ('ngc3198' in low or 'ngc_3198' in low) and not low.endswith('.py') and not ex_b:
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
        why = _forbidden_read(lit, real, _writing(args[1] if len(args) > 1 else None, args[2] if len(args) > 2 else None))
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


def selftest_v002():
    """v002: the two read-only exceptions, as path predicates only (no protected file is opened). Returns [(name, ok)]."""
    C2 = CLAUDE2_CTRL
    A = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/x_fence_probe_c4r5'
    ADD = C2 + '/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md'
    cases = [
        ('a_uvt_source_read_allowed', A + '/uvt_probe_should_not_exist.py', False, None),
        ('a_uvt_source_write_refused', A + '/uvt_probe_should_not_exist.py', True, 'UVT component'),
        ('a_uvt_dir_component_refused', A + '/UVT_probe_dir/uvt_probe.py', False, 'UVT component'),
        ('a_uvt_non_py_refused', A + '/uvt_probe.json', False, 'UVT component'),
        ('a_uvt_under_a_runs_ext_component_refused', A + '/runs_ext/uvt_probe.py', False, 'UVT component'),
        ('a_uvt_c5h_name_still_refused', A + '/kmax_a2f10_c5h_run_v001/uvt_probe.py', False, 'C5H name'),
        ('b_addendum_read_allowed', ADD, False, None),
        ('b_frozen_addendum_read_allowed', C2 + '/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM_FROZEN.md', False, None),
        ('b_v004_addendum_read_allowed', C2 + '/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V004_ADDENDUM.md', False, None),
        ('b_addendum_write_refused', ADD, True, 'NGC3198 data'),
        ('b_v001_decisions_not_an_addendum_refused', C2 + '/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V001.md', False, 'NGC3198 data'),
        ('b_addendum_name_in_subfolder_refused', C2 + '/specs/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md', False, 'NGC3198 data'),
        ('b_addendum_name_elsewhere_refused', A + '/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md', False, 'NGC3198 data'),
        ('b_addendum_json_refused', C2 + '/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.json', False, 'NGC3198 data'),
        ('b_target_word_still_refused', C2 + '/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM_rotmod.md', False, 'target word'),
        ('other_ngc3198_data_refused', A + '/NGC3198_probe_table.dat', False, 'NGC3198 data'),
        ('other_ngc3198_py_allowed_as_v001', A + '/ngc3198_probe_source.py', False, None),
    ]
    out = []
    for name, p, writing, want in cases:
        lit = os.path.abspath(p)
        real = os.path.realpath(lit)
        got = _forbidden_read(lit, real, writing)
        out.append((name, got == want))
    return out
