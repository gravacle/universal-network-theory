"""Audit-hook guard for the V006 R1 dry runs / smoke / tests: a copy of extension_c5c6/tools/guard_c2ext.py (itself adapted
from driver_v008_c2/tests/guard_c2v008.py) with the write root narrowed to v006_r1/.
Usage: python3 -I -B guard_r1.py LOG.json SCRIPT.py [args...]
Runs SCRIPT as __main__ with these refusals (PermissionError, recorded in LOG.json):
  * any process creation (subprocess.Popen, os.system, os.exec*, os.spawn*, os.posix_spawn, os.fork*): no launch possible;
  * any open for writing, mkdir, rename, remove, chmod, unlink outside ALLOWED_WRITE_ROOT (this lane folder);
  * any write under CLAUDE2/runs or CLAUDE2/runs_ext (also via the External1 real path);
  * any open of a velocity-like basename (rotmod, .dat, velocit, vobs) or of an NGC3198 path naming targets/observed.
Reads of saved run outputs are allowed (the R3 verdict is registered).  LOG.json: script, argv, exit, denied, writes,
every path opened for reading.
"""
import json
import os
import runpy
import sys

ALLOWED_WRITE_ROOT = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/kmax_prereg_v005_c2/extension_c5c6/v006_r1/'
NO_WRITE_ROOTS = ('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs',
                  '/Volumes/External1/')
VELOCITY_HINTS = ('rotmod', '.dat', 'velocit', 'vobs')
PROC = ('subprocess.Popen', 'os.system', 'os.exec', 'os.spawn', 'os.posix_spawn', 'os.fork', 'os.forkpty')
MUT = ('os.mkdir', 'os.rename', 'os.remove', 'os.rmdir', 'os.chmod', 'shutil.rmtree', 'os.unlink', 'os.replace', 'os.truncate')
denied, writes, opened = [], {}, set()


def _write_mode(mode, flags):
    if isinstance(mode, str):
        return any(c in mode for c in 'wax+')
    if isinstance(flags, int):
        return bool(flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_APPEND | os.O_TRUNC))
    return False


def _p(x):
    return os.path.abspath(os.fsdecode(x)) if isinstance(x, (str, bytes, os.PathLike)) else None


def _velocity(p):
    b = os.path.basename(p).lower()
    if any(h in b for h in VELOCITY_HINTS):
        return True
    return 'NGC3198' in p and any(t in p.lower() for t in ('target', 'observed_v', 'vobs'))


def hook(event, args):
    if event in PROC:
        denied.append([event, repr(args)[:300]])
        raise PermissionError('guard_r1: %s refused' % event)
    if event == 'open':
        p = _p(args[0])
        if p is None:
            return
        w = _write_mode(args[1], args[2])
        if _velocity(p):
            denied.append([event, p])
            raise PermissionError('guard_r1: velocity-like path refused: ' + p)
        if w:
            if not p.startswith(ALLOWED_WRITE_ROOT) or any(p.startswith(r) for r in NO_WRITE_ROOTS):
                denied.append([event + ':write', p])
                raise PermissionError('guard_r1: write outside the lane refused: ' + p)
            writes[p] = writes.get(p, 0) + 1
        else:
            opened.add(p)
    if event in MUT:
        p = _p(args[0]) or repr(args[0])
        if not str(p).startswith(ALLOWED_WRITE_ROOT):
            denied.append([event, p])
            raise PermissionError('guard_r1: %s outside the lane refused: %s' % (event, p))
        writes['%s %s' % (event, p)] = writes.get('%s %s' % (event, p), 0) + 1


def main():
    log, script = os.path.abspath(sys.argv[1]), sys.argv[2]
    if not log.startswith(ALLOWED_WRITE_ROOT):
        raise SystemExit('log must be inside the lane')
    sys.argv = [script] + sys.argv[3:]
    sys.addaudithook(hook)
    code = 0
    try:
        runpy.run_path(script, run_name='__main__')
    except SystemExit as exc:
        code = exc.code if isinstance(exc.code, int) else (0 if exc.code is None else 1)
    except BaseException as exc:
        import traceback
        code = 'EXCEPTION %s: %s' % (type(exc).__name__, exc)
        traceback.print_exc()
    rec = {'script': script, 'argv': sys.argv[1:], 'exit': code, 'denied': denied, 'writes': writes,
           'opened_read': sorted(opened), 'velocity_like_paths_opened': [p for p in opened if _velocity(p)]}
    with open(log, 'x') as f:
        json.dump(rec, f, indent=1)
    print(json.dumps({'exit': code, 'denied': denied, 'n_writes': len(writes), 'n_opened': len(opened)}))
    return code


if __name__ == '__main__':
    _c = main()
    sys.exit(_c if isinstance(_c, int) else 1)
