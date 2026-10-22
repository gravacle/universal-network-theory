"""OS-level read audit of lookup validation plus full synthetic verifier replay."""
import hashlib
import json
import os
from pathlib import Path
import sys
import types

HERE = Path(__file__).resolve().parent
FIXTURE = HERE/'DIRECT_LOOKUP_TESTS_CX2V003'
OUT = HERE/'SNAPSHOT_AUDIT_CX2V001.json'
source = HERE/'direct_cert_lookup_cx2v002.py'
raw = source.read_bytes()
M = types.ModuleType('snapshot_audit_lookup')
M.__file__ = str(source)
exec(compile(raw, str(source), 'exec'), M.__dict__)
request_path = FIXTURE/'REQUEST.json'
request_bytes = request_path.read_bytes()
request = json.loads(request_bytes)
M.C1, M.GENESIS = request['c1'], request['genesis_registry']
custody = json.loads((FIXTURE/'BUNDLE_0.json').read_bytes())['custody']
reads = {}
active = True
def audit(event, args):
    if event.startswith(('subprocess.', 'socket.')) or event in (
        'os.system', 'os.fork', 'os.posix_spawn', 'os.rename', 'os.remove', 'os.rmdir'):
        raise RuntimeError('AUDIT_FENCE: '+event)
    if event != 'open' or not isinstance(args[0], (str, bytes)):
        return
    p = os.path.abspath(os.fsdecode(args[0]))
    if any(x in p.lower() for x in ('ngc3198', '/runs/', '/runs_ext/', '/.codex/', 'v007_postseal_records')):
        raise RuntimeError('AUDIT_PROTECTED_PATH: '+p)
    flags = args[2]
    writing = flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC)
    if writing:
        if active or p != str(OUT) or not flags & os.O_EXCL or os.path.lexists(p):
            raise RuntimeError('AUDIT_WRITE_REFUSED')
    elif active and p.startswith('/Users/bgm/Research/'):
        reads[p] = reads.get(p, 0) + 1
sys.addaudithook(audit)
class SyntheticSnapshot(M.Snapshot):
    def module(self, ref, name):
        obj = super().module(ref, name)
        if ref == M.ASSEMBLER:
            obj.A.real_custody_fn = lambda pin: lambda spec: custody
        return obj
s = SyntheticSnapshot()
prepared = M.validate(s, {'path': str(request_path), 'sha256': hashlib.sha256(request_bytes).hexdigest()})
M.replay(s, prepared)
active = False
duplicates = {p: n for p, n in reads.items() if n != 1}
untracked = sorted(set(reads) - set(s.counts))
missed = sorted(set(s.counts) - set(reads))
passed = not duplicates and not untracked and not missed
result = {'schema': 'DIRECT_SNAPSHOT_OS_AUDIT_CX2V001', 'status': 'TESTED', 'passed': passed,
          'physical_opens': reads, 'n_files': len(reads), 'duplicates': duplicates,
          'untracked': untracked, 'missed': missed, 'source': {'path': str(source),
          'sha256': hashlib.sha256(raw).hexdigest()},
          'scope': 'validate + native list verifier replay, synthetic custody. OS audit events, not internal counters.',
          'no_process_network_delete_rename': True}
payload = (json.dumps(result, indent=2, sort_keys=True)+'\n').encode()
with OUT.open('xb') as f:
    f.write(payload)
print(json.dumps({'passed': passed, 'n_files': len(reads),
                  'report': {'path': str(OUT), 'sha256': hashlib.sha256(payload).hexdigest()},
                  'duplicates': duplicates, 'untracked': untracked, 'missed': missed}))
raise SystemExit(0 if passed else 1)
