"""Fixed spherical-shadow stdout custody; no scientific changes or overwritten receipts."""
import contextlib
import hashlib
import io
import json
from pathlib import Path
import runpy
import sys
import traceback
import uuid

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = Path('/Users/bgm/Documents/ChatGPT/Universal Network Theory')
PUBLISHER = HERE / 'run_scientific_case_v001.py'
PUBLISHER_SHA = 'f4cf2cea4d4d42688616ee671f66b5717a0fb554f1ea4972783d9cc1b00071b8'
SOURCE = 'spherical_dust_shadow_v001.py'
SOURCE_SHA = 'ba928eafe25c870ea872027389ecff1a45425f6f3ea613562e65d67bd9c853ed'
FREEZE = 'SPHERICAL_DUST_SHADOW_V001_FROZEN.json'
JOBS = {
    'freeze': (SOURCE, SOURCE_SHA, ['freeze'], FREEZE, None),
    'run': (SOURCE, SOURCE_SHA, ['run'], 'SPHERICAL_DUST_SHADOW_V001_RESULTS.json', FREEZE),
}


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in JOBS:
        raise RuntimeError('Select exactly one fixed reviewed job')
    if Path.cwd().resolve() != ROOT or HERE != ROOT / 'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation':
        raise RuntimeError('Wrong project context')
    if PUBLISHER.is_symlink() or digest(PUBLISHER.read_bytes()) != PUBLISHER_SHA:
        raise RuntimeError('Publisher identity changed')
    helpers = runpy.run_path(str(PUBLISHER), run_name='custody_helpers')
    bound, publish = helpers['bound'], helpers['publish']
    job = sys.argv[1]
    source_name, source_sha, args, output_name, freeze_name = JOBS[job]
    source, destination = bound(HERE / source_name), bound(HERE / output_name)
    if digest(source.read_bytes()) != source_sha:
        raise RuntimeError('Reviewed source differs')
    if destination.exists() or destination.is_symlink():
        raise FileExistsError('Receipt already exists; no job executed')
    buffer = io.StringIO()
    code = 0
    failure = None
    sys.argv = [str(source), *args]
    try:
        with contextlib.redirect_stdout(buffer):
            try:
                runpy.run_path(str(source), run_name='__main__')
            except SystemExit as stopped:
                code = stopped.code or 0
                if type(code) is not int:
                    raise RuntimeError('Noninteger producer exit')
        raw = buffer.getvalue().encode('utf-8')
        packet = json.loads(raw)
        if not isinstance(packet, dict):
            raise RuntimeError('Expected JSON object')
        json.dumps(packet, allow_nan=False)
        if freeze_name is not None:
            payload = packet['payload']
            encoded = json.dumps(payload, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()
            if packet['payload_sha256'] != digest(encoded) or packet['freeze_sha256'] != digest(bound(HERE / freeze_name).read_bytes()):
                raise RuntimeError('Produced wrapper custody differs')
            if not isinstance(payload['status'], str):
                raise RuntimeError('Missing scientific status')
    except BaseException:
        failure = dict(status='CAPTURE_OR_VALIDATION_FAILED', job=job, captured_stdout=buffer.getvalue(),
                       traceback=traceback.format_exc(), source_sha256=source_sha, producer_exit_code=code)
        raw = (json.dumps(failure, sort_keys=True, separators=(',', ':'), allow_nan=False) + '\n').encode()
        destination = destination.with_name(destination.name + '.attempt-' + uuid.uuid4().hex + '.json')
    publish(raw, destination)
    if digest(destination.read_bytes()) != digest(raw):
        raise RuntimeError('Published bytes differ')
    print(json.dumps(dict(job=job, path=str(destination), bytes=len(raw), sha256=digest(raw),
                          status=failure['status'] if failure else packet.get('payload', {}).get('status', 'SNAPSHOT_SAVED'),
                          producer_exit_code=code, source_sha256=source_sha,
                          controller_sha256=digest(Path(__file__).read_bytes())), sort_keys=True), flush=True)
    return 2 if failure or (freeze_name is not None and packet['payload'].get('failures')) else code


if __name__ == '__main__':
    sys.exit(main())
