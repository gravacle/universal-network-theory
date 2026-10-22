"""Claude2-lane review helpers for Codex2 v006r8 (0554/0435). No launches, no network, no deletion.

Audit hook: refuses subprocess/socket/exec/spawn, any delete/rename, any write outside this
review directory (writes must be exclusive-create), and reads of the forbidden paths.
"""
import hashlib
import json
import os
import sys
import types
from pathlib import Path

ART = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
R8 = ART / 'calib_tail_readiness_cx2/v006r8'
R7 = ART / 'calib_tail_readiness_cx2/v006r7'
OUT = ART / 'review_calib_v006r8_c2'
BLOCKED = []

WRAPPER_SHA = '1ddbe6da1b34e84a9a419a0c72e2933a74cd3021cbdb68c91f5691193b9ce488'


def _audit(event, args):
    if event.startswith('socket.') or event in (
            'subprocess.Popen', 'os.system', 'os.posix_spawn', 'os.spawn', 'os.fork',
            'os.forkpty', 'os.exec', 'pty.spawn', 'os.kill'):
        BLOCKED.append(event)
        raise RuntimeError('C2R8 review forbids launch/network: ' + event)
    if event in ('os.remove', 'os.unlink', 'os.rmdir', 'os.rename', 'os.replace',
                 'shutil.rmtree', 'os.truncate'):
        BLOCKED.append(event)
        raise RuntimeError('C2R8 review forbids delete/move: ' + event)
    if event == 'open' and args and isinstance(args[0], (str, bytes, os.PathLike)):
        p = Path(os.fsdecode(args[0])).resolve()
        low = str(p).lower()
        if ('kmax_a2f10_c5h_run_v001' in low or '/runs_ext/uvt_' in low or '/.codex/' in low):
            BLOCKED.append('read ' + str(p))
            raise RuntimeError('C2R8 forbidden read: ' + str(p))
        if 'ngc3198' in low and any(x in low for x in ('observed', 'target', 'rotmod', 'velocit')):
            BLOCKED.append('read ' + str(p))
            raise RuntimeError('C2R8 forbidden NGC target read: ' + str(p))
        mode = args[1] if len(args) > 1 else 'r'
        flags = args[2] if len(args) > 2 else 0
        writing = (isinstance(mode, str) and any(c in mode for c in 'wax+')) or (
            isinstance(flags, int) and flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND))
        if writing:
            if not p.is_relative_to(OUT.resolve()):
                BLOCKED.append('write ' + str(p))
                raise RuntimeError('C2R8 write outside review dir: ' + str(p))
            if isinstance(mode, str) and 'x' not in mode and not (isinstance(flags, int) and flags & os.O_EXCL):
                BLOCKED.append('nonexclusive ' + str(p))
                raise RuntimeError('C2R8 requires exclusive create: ' + str(p))


sys.addaudithook(_audit)


def sha_bytes(raw):
    return hashlib.sha256(raw).hexdigest()


def sha_file(path):
    return sha_bytes(Path(path).read_bytes())


def pin(path):
    return {'path': str(path), 'sha256': sha_file(path)}


def write_x(path, data):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(data, bytes):
        raw = data
    elif isinstance(data, str):
        raw = data.encode()
    else:
        raw = json.dumps(data, sort_keys=True, indent=1, allow_nan=False).encode()
    with open(p, 'xb') as f:
        f.write(raw)
    return pin(p)


def load_pinned(path, name, expected):
    raw = Path(path).read_bytes()
    if sha_bytes(raw) != expected:
        raise ValueError('source pin mismatch: %s' % path)
    m = types.ModuleType(name)
    m.__file__ = str(path)
    sys.modules[name] = m
    exec(compile(raw, str(path), 'exec'), m.__dict__)
    return m


def make_receipt(mon_schema, spec_sha, driver_sha, result_pin):
    """Own receipt construction from the monitor's documented verify contract (self-hash over canonical)."""
    body = {'schema': mon_schema, 'status': 'FINISHED', 'driver_status': 'COMPLETED',
            'pins': {'spec': {'sha256': spec_sha}, 'driver': {'sha256': driver_sha}},
            'result': result_pin, 'retries': 0, 'exit_code': 0, 'stop_reason': None,
            'c2r8_fixture': True}
    canon = json.dumps(body, sort_keys=True, separators=(',', ':'), allow_nan=False)
    body['receipt_sha256'] = hashlib.sha256(canon.encode()).hexdigest()
    return body


class Ledger:
    def __init__(self):
        self.rows = []

    def check(self, cid, name, ok, observed=None):
        self.rows.append({'id': cid, 'name': name, 'pass': bool(ok), 'observed': observed})
        print(('PASS ' if ok else 'FAIL ') + cid + ' ' + name, flush=True)

    def summary(self):
        return {'passed': sum(r['pass'] for r in self.rows), 'total': len(self.rows),
                'failed': [r['id'] for r in self.rows if not r['pass']], 'blocked_attempts': list(BLOCKED)}
