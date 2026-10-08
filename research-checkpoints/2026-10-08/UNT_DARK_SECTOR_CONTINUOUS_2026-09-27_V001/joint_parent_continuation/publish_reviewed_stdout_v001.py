"""Fixed-job stdout custody; no scientific changes or overwritten receipts."""
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
HARD = 'hard_barotrope_qualification_v001.py'
HARD_SHA = '4a8a0b7260b970aa4aa11b682e4b3377f96ad0b7dd0d47ce6d0735db888fc8d6'
BAO = 'hyrec_inputs_v001/hyrec_bao_interval_v001.py'
BAO_SHA = 'c35a24011a92462d725824eff0a96bdfca7ae11a5935e462a5dce3f7ce85fdb3'
BAO_SNAPSHOT = 'hyrec_inputs_v001/HYREC_BAO_INTERVAL_V001_PARTIAL_002_FROZEN.json'
HARD_FREEZE = 'HARD_BAROTROPE_QUALIFICATION_V001_FROZEN.json'
JOBS = {
    'bao-freeze': (BAO, BAO_SHA, ['freeze'], BAO_SNAPSHOT, None),
    'bao-collect': (BAO, BAO_SHA, ['collect', str(HERE / BAO_SNAPSHOT)],
                    'hyrec_inputs_v001/HYREC_BAO_INTERVAL_V001_PARTIAL_002.json', BAO_SNAPSHOT),
    'hard-freeze': (HARD, HARD_SHA, ['freeze'], HARD_FREEZE, None),
    'hard-build': (HARD, HARD_SHA, ['build'], 'HARD_BAROTROPE_QUALIFICATION_V001_BUILD.json', HARD_FREEZE),
    'hard-benchmark': (HARD, HARD_SHA, ['benchmark'], 'HARD_BAROTROPE_QUALIFICATION_V001_BENCHMARK.json', HARD_FREEZE),
    'hard-run': (HARD, HARD_SHA, ['run'], 'HARD_BAROTROPE_QUALIFICATION_V001_RESULTS.json', HARD_FREEZE),
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
    return 2 if failure else code


if __name__ == '__main__':
    sys.exit(main())
