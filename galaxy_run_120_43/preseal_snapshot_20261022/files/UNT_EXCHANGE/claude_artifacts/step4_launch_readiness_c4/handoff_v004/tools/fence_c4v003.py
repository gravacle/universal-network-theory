# Claude4 v003 (closes Claude3 0105 PR-SF3): in-process safety fence for the step-4 final-spec producer, its tests and the
# v003 builders. Successor of fence_c4v001.py (f813c43099cfdadd3a779e395d223887d0df7cd8c8a8eb67b3a73de86eb699f0).
# It is a Python audit hook (it cannot be removed once added). It raises PermissionError, so the operation never happens, on:
#  - any process creation (subprocess, os.system/exec/spawn/fork, pty), any os.kill, and any network use;
#  - any delete (os.remove/unlink/rmdir, shutil.rmtree) and any rename or move (os.rename/os.replace, shutil.move);
#  - any write, create, link, symlink, chmod or xattr change outside REVIEW (the parent of this file's folder);
#  - any open, listdir, scandir, chdir or glob of a PROTECTED path. The decision is taken on the LITERAL path first,
#    before any resolve or metadata probe (the class of 0625 item 1): the raw string and its lexical normal form are checked
#    with no filesystem access; then the path is resolved one component at a time, and every candidate and every symlink
#    target is checked lexically before it is probed (the rule of guard007 safe_path, 42bf0ce9 L32-53).
#    Protected names (casefold): any 'runs_ext' component and both CLAUDE2 runs_ext roots; any '.vol' component (the macOS
#    by-inode namespace); any UVT_* component; the C5H run name; the target words rotmod, vobs, massmodels, sparc; the NGC3198
#    aliases ngc3198, 'ngc 3198', ngc_3198, ngc-3198, ngc.3198, n3198, ugc5572, 'ugc 5572', ugc_5572, ugc-5572, ugc.5572;
#    the DDO154 observation aliases observation_region, obs_region, vrot, vel_obs, velobs, rotation_curve, rotcurve,
#    rot_curve, observed_rotation, observed_velocit, target_velocit; coefficient arrays (*.npz); '.codex' components.
#    One exception, copied from guard007 lexical_path (L28-29): the FINAL component may be a root-rulings file named
#    ROOT_DECISIONS_NGC3198_CONSTRUCTION_<suffix>.md (suffix [A-Za-z0-9_-]+ and itself free of every protected word).
#    Unlike v001 there is NO exemption inside REVIEW: a protected name is refused everywhere, look-alikes included.
# PROBE_LOG (only while TRACE[0] is True) records every lstat/readlink this fence performs, so a test can prove that no
# protected-named path was probed before its refusal.
import os
import re
import stat
import sys

VERSION = 'FENCE_C4V003'
REVIEW = os.path.realpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
RUNS_EXT = (
    '/Volumes/External1/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs_ext',
    '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs_ext',
)
TARGET_WORDS = ('rotmod', 'vobs', 'massmodels', 'sparc')
NGC_ALIASES = ('ngc3198', 'ngc 3198', 'ngc_3198', 'ngc-3198', 'ngc.3198', 'n3198',
               'ugc5572', 'ugc 5572', 'ugc_5572', 'ugc-5572', 'ugc.5572')
DDO_OBS_ALIASES = ('observation_region', 'obs_region', 'vrot', 'vel_obs', 'velobs', 'rotation_curve', 'rotcurve',
                   'rot_curve', 'observed_rotation', 'observed_velocit', 'target_velocit')
META_NAME = re.compile(r'ROOT_DECISIONS_NGC3198_CONSTRUCTION_([A-Za-z0-9_-]+)\.md')
PROCESS_EVENTS = {'subprocess.Popen', 'os.system', 'os.exec', 'os.posix_spawn', 'os.spawn', 'os.fork', 'os.forkpty',
                  'pty.spawn', 'os.startfile', 'os.kill', 'os.killpg', 'signal.pthread_kill'}
NET_EVENTS = {'socket.connect', 'socket.bind', 'socket.sendto', 'socket.sendmsg', 'socket.getaddrinfo',
              'socket.gethostbyname', 'socket.gethostbyaddr', 'urllib.Request', 'http.client.connect', 'ftplib.connect',
              'smtplib.connect', 'webbrowser.open'}
DELETE_EVENTS = {'os.remove', 'os.rmdir', 'shutil.rmtree'}
MOVE_EVENTS = {'os.rename', 'shutil.move'}
WRITE_PATH_EVENTS = {'os.mkdir': (0,), 'os.symlink': (1,), 'os.link': (1,), 'os.truncate': (0,),
                     'os.chmod': (0,), 'os.chown': (0,), 'os.utime': (0,), 'shutil.copyfile': (1,), 'shutil.copytree': (1,),
                     'os.chflags': (0,), 'os.lchflags': (0,), 'os.setxattr': (0,), 'os.removexattr': (0,)}
READ_PATH_EVENTS = {'os.listdir': 0, 'os.scandir': 0, 'os.chdir': 0, 'glob.glob': 0, 'os.link': 0, 'shutil.copyfile': 0,
                    'shutil.copytree': 0}
BLOCKED = []       # (event, detail) for every refused operation
TRACE = [False]
PROBE_LOG = []     # ('lstat'|'readlink', path) while TRACE[0]
_LSTAT = os.lstat
_READLINK = os.readlink


class FenceRefusal(PermissionError):
    pass


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


def protected_reason(path_str):
    """Lexical only: no filesystem access. Returns a reason string or None."""
    if not isinstance(path_str, str):
        return 'non-string path'
    low = path_str.casefold()
    if '\x00' in path_str:
        return 'NUL in path'
    comps = [c for c in path_str.split('/') if c]
    for r in RUNS_EXT:
        if _under(path_str, r) or _under(os.path.normpath(path_str), r):
            return 'real run tree'
    for c in comps:
        cl = c.casefold()
        if cl == 'runs_ext':
            return 'runs_ext tree'
        if cl == '.vol':
            return '/.vol by-inode path'
        if cl.startswith('uvt_'):
            return 'UVT component'
        if cl == '.codex':
            return '.codex component'
    if 'kmax_a2f10_c5h_run_v001' in low:
        return 'C5H name'
    for w in TARGET_WORDS:
        if w in low:
            return 'target word ' + w
    for w in DDO_OBS_ALIASES:
        if w in low:
            return 'DDO154 observation alias ' + w
    if low.endswith('.npz') or '.npz/' in low:
        return 'coefficient array (.npz)'
    for i, c in enumerate(comps):
        cl = c.casefold()
        hit = [w for w in NGC_ALIASES if w in cl]
        if not hit:
            continue
        m = META_NAME.fullmatch(c)
        if i == len(comps) - 1 and m is not None and not any(w in m.group(1).casefold() for w in NGC_ALIASES):
            continue                     # guard007 L28-29: a root-rulings file name as the final component only
        return 'NGC3198 alias ' + hit[0]
    return None


def _refuse(event, detail):
    BLOCKED.append((event, str(detail)))
    raise FenceRefusal('FENCE_C4V003: %s %s' % (event, detail))


def _check_literal(event, p):
    why = protected_reason(p)
    if why:
        _refuse('%s(%s)' % (event, why), p)


def safe_resolve(path, event='resolve'):
    """Literal checks first (raw string and lexical normal form, no filesystem access), then resolve one component at a
    time from the RAW components (so '..' is applied after the preceding links, as the kernel does), checking each
    candidate and each symlink target lexically before probing it. Returns the resolved absolute path."""
    raw = _s(path)
    if raw is None:
        _refuse(event + '(unsupported path type)', repr(path)[:80])
    _check_literal(event, raw)
    if not raw.startswith('/'):
        raw = os.path.join(os.getcwd(), raw)
        _check_literal(event, raw)
    _check_literal(event, os.path.normpath(raw))
    todo = [c for c in raw.split('/') if c]
    current = '/'
    links = 0
    while todo:
        part = todo.pop(0)
        if part == '.':
            continue
        if part == '..':
            current = os.path.dirname(current) or '/'
            continue
        cand = os.path.join(current, part)
        _check_literal(event, cand)
        if TRACE[0]:
            PROBE_LOG.append(('lstat', cand))
        try:
            st = _LSTAT(cand)
        except OSError:
            current = cand
            continue
        if stat.S_ISLNK(st.st_mode):
            links += 1
            if links > 40:
                _refuse(event + '(symlink loop)', cand)
            if TRACE[0]:
                PROBE_LOG.append(('readlink', cand))
            target = _READLINK(cand)
            _check_literal(event + ' symlink target', target)
            tpath = target if target.startswith('/') else os.path.join(current, target)
            _check_literal(event + ' symlink target', tpath)
            _check_literal(event + ' symlink target', os.path.normpath(tpath))
            if target.startswith('/'):
                current = '/'
            todo = [c for c in target.split('/') if c] + todo
        else:
            current = cand
    _check_literal(event, current)
    return current


def _writing(mode, flags):
    if isinstance(mode, str) and any(c in mode for c in 'wax+'):
        return True
    if isinstance(flags, int) and flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_APPEND | os.O_TRUNC):
        return True
    return False


def _write_target_inside(event, p):
    real = safe_resolve(p, event)
    parent = safe_resolve(os.path.dirname(real) or '/', event)
    if not (_under(real, REVIEW) and _under(parent, REVIEW)):
        _refuse(event + '(write outside REVIEW)', p)


def _hook(event, args):
    if event in PROCESS_EVENTS or event in NET_EVENTS:
        _refuse(event, args[:2] if isinstance(args, tuple) else args)
    if event in DELETE_EVENTS:
        _refuse(event, args[:1])
    if event in MOVE_EVENTS:
        _refuse(event, args[:2])
    if event in READ_PATH_EVENTS:
        i = READ_PATH_EVENTS[event]
        p = _s(args[i]) if isinstance(args, tuple) and len(args) > i else None
        if p is not None:
            safe_resolve(p, event)
    if event in WRITE_PATH_EVENTS:
        for i in WRITE_PATH_EVENTS[event]:
            p = _s(args[i]) if len(args) > i else None
            if p is not None:
                _write_target_inside(event, p)
        return
    if event == 'open':
        p = _s(args[0])
        if p is None:
            return
        safe_resolve(p, 'open')
        if _writing(args[1] if len(args) > 1 else None, args[2] if len(args) > 2 else None):
            _write_target_inside('open(write)', p)


sys.addaudithook(_hook)


def selftest():
    """Each forbidden class must raise FenceRefusal BEFORE any filesystem access to the protected path.
    Returns (name, refused, probes_of_protected_names)."""
    out = []
    import subprocess
    import socket
    here = REVIEW
    trials = [
        ('popen', lambda: subprocess.Popen(['/usr/bin/true'])),
        ('os_system', lambda: os.system('true')),
        ('socket_connect', lambda: socket.socket().connect(('127.0.0.1', 9))),
        ('write_outside', lambda: open('/private/tmp/claude4_fence_v003_probe_should_not_exist.txt', 'x')),
        ('delete', lambda: os.remove(os.path.join(here, 'nonexistent_probe'))),
        ('rename', lambda: os.rename(os.path.join(here, 'a_probe'), os.path.join(here, 'b_probe'))),
        ('read_runs_ext', lambda: open(RUNS_EXT[1] + '/probe_should_not_exist.json', 'rb')),
        ('read_runs_ext_component', lambda: open(os.path.join(here, 'runs_ext', 'x.json'), 'rb')),
        ('read_vol', lambda: open('/.vol/16777220/2', 'rb')),
        ('read_vol_relative', lambda: open('/private/../.vol/1/2', 'rb')),
        ('read_uvt', lambda: open('/Users/bgm/Research/UVT_probe_should_not_exist/x.json', 'rb')),
        ('read_c5h', lambda: open('/Users/bgm/Research/KMAX_A2F10_C5H_RUN_V001/x.json', 'rb')),
        ('read_rotmod', lambda: open(os.path.join(here, 'x_rotmod_probe.dat'), 'rb')),
        ('read_n3198', lambda: open(os.path.join(here, 'N3198_probe.json'), 'rb')),
        ('read_ugc5572', lambda: open(os.path.join(here, 'UGC5572_probe.json'), 'rb')),
        ('read_ngc_space', lambda: open(os.path.join(here, 'NGC 3198 probe.json'), 'rb')),
        ('read_ngc_dash', lambda: open(os.path.join(here, 'NGC-3198_probe.json'), 'rb')),
        ('read_ngc_py', lambda: open(os.path.join(here, 'ngc3198_probe.py'), 'rb')),
        ('read_ddo_vrot', lambda: open(os.path.join(here, 'DDO154_vrot_probe.json'), 'rb')),
        ('read_ddo_vel_obs', lambda: open(os.path.join(here, 'DDO154', 'vel_obs', 'x.json'), 'rb')),
        ('read_rotation_curve', lambda: open(os.path.join(here, 'DDO154_rotation_curve_probe.json'), 'rb')),
        ('read_target_velocities', lambda: open(os.path.join(here, 'target_velocities_probe.json'), 'rb')),
        ('read_observed_rotation', lambda: open(os.path.join(here, 'observed_rotation_velocities.json'), 'rb')),
        ('read_observation_region', lambda: open(os.path.join(here, 'DDO154_CALIBRATION_OBSERVATION_REGION_probe.json'), 'rb')),
        ('read_npz', lambda: open(os.path.join(here, 'x_probe.npz'), 'rb')),
        ('read_dotdot_hidden', lambda: open(os.path.join(here, 'rotmod', '..', 'innocent_probe.json'), 'rb')),
        ('listdir_uvt', lambda: os.listdir('/Users/bgm/Research/UVT_probe_should_not_exist')),
        ('meta_name_with_alias', lambda: open(os.path.join(here, 'ROOT_DECISIONS_NGC3198_CONSTRUCTION_UGC5572.md'), 'rb')),
        ('meta_name_as_directory', lambda: open(os.path.join(here, 'ROOT_DECISIONS_NGC3198_CONSTRUCTION_X.md', 'y.json'), 'rb')),
    ]
    for name, fn in trials:
        TRACE[0] = True
        n0 = len(PROBE_LOG)
        try:
            fn()
            out.append((name, False, []))
        except PermissionError as e:     # FenceRefusal of this or of another loaded copy of this fence (same bytes)
            probes = [p for _, p in PROBE_LOG[n0:] if protected_reason(p)]
            out.append((name, str(e).startswith('FENCE_C4V003'), probes))
        except Exception as e:
            out.append((name, False, ['%s: %s' % (type(e).__name__, e)]))
        finally:
            TRACE[0] = False
    return out
