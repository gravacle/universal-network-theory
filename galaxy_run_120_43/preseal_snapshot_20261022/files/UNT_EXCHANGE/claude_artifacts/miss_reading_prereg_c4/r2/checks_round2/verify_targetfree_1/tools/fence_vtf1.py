# Audit-hook fence for verify_targetfree_1. Refuses target-like or protected paths, writes outside this folder,
# and process, network, delete and rename events. Import it first.
import os, sys
_HERE = os.path.realpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
_BAD = ('rotmod', 'vobs', 'v_obs', 'massmodels', 'mass_models', 'sparc', 'kmax_a2f10_c5h_run_v001', 'uvt_', 'runs_ext')
def _hook(event, args):
    if event == 'open':
        path = args[0]
        if isinstance(path, int):
            return
        p = os.fsdecode(path) if isinstance(path, bytes) else str(path)
        low = p.lower()
        if any(w in low for w in _BAD):
            raise PermissionError('fence: refused path %s' % p)
        mode = args[1] if len(args) > 1 and isinstance(args[1], str) else 'r'
        flags = args[2] if len(args) > 2 and isinstance(args[2], int) else 0
        writing = any(c in mode for c in 'wax+') or (flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_APPEND | os.O_TRUNC))
        if writing:
            rp = os.path.realpath(p)
            if not (rp == _HERE or rp.startswith(_HERE + os.sep)):
                raise PermissionError('fence: write refused %s' % p)
    elif event in ('os.remove', 'os.unlink', 'os.rename', 'os.replace', 'os.rmdir', 'shutil.rmtree', 'subprocess.Popen',
                   'os.system', 'os.exec', 'os.posix_spawn', 'os.fork', 'os.forkpty', 'socket.connect', 'socket.getaddrinfo',
                   'socket.bind', 'os.symlink', 'os.link', 'os.truncate', 'os.chmod'):
        raise PermissionError('fence: refused event %s' % event)
sys.addaudithook(_hook)
