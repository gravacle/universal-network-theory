"""Claude3 backlog #6 review probe: run a G26 successor test as __main__ while every pre-existing path under /tmp and
/private/tmp (except this probe's own folder) behaves as ABSENT, as after a reboot. Python-level access only.
usage: $PY -I -B post_reboot_sim_c3.py TEST_PATH WORK"""
import errno, io, os, runpy, sys, builtins
test, work = sys.argv[1], sys.argv[2]
KEEP = os.path.dirname(os.path.abspath(__file__)) + '/'
DENY = ('/private/tmp/', '/tmp/')
HITS = []
def gone(p):
    if isinstance(p, int):
        return False
    try:
        s = os.fsdecode(p)
    except TypeError:
        return False
    s = s if s.startswith('/') else os.path.join(os.getcwd(), s)
    s2 = s if s.startswith('/private/') else '/private' + s
    if KEEP.startswith(s2.rstrip('/') + '/') or s2.startswith(KEEP):   # this probe's own folder and its ancestors stay
        return False
    return s.startswith(DENY)
def wrap(fn, name):
    def w(path, *a, **k):
        if gone(path):
            HITS.append((name, os.fsdecode(path)))
            raise FileNotFoundError(errno.ENOENT, 'SIMULATED_ABSENT_AFTER_REBOOT', os.fsdecode(path))
        return fn(path, *a, **k)
    return w
for name in ('stat', 'lstat', 'open', 'listdir', 'scandir', 'access', 'readlink'):
    setattr(os, name, wrap(getattr(os, name), 'os.' + name))
io.open = builtins.open = wrap(io.open, 'io.open')
sys.argv = [test, work]
try:
    runpy.run_path(test, run_name='__main__')
    status = 'COMPLETED'
except SystemExit as e:
    status = 'SystemExit %r' % (e.code,)
except BaseException as e:
    status = 'EXCEPTION %s: %s' % (type(e).__name__, str(e)[:300])
print('POST_REBOOT_SIM', status, 'denied_accesses=%d' % len(HITS), sorted(set(h[1] for h in HITS))[:40], file=sys.stderr)
