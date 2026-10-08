"""Run one pinned scientific case and atomically publish its generated receipt.

This is a scientific-output/checkpoint controller, not a source editor.
Unchanged producers still emit stdout; publication never replaces a file.
"""
import contextlib
import hashlib
import io
import json
import os
from pathlib import Path
import runpy
import sys
import tempfile
import time
import traceback
import uuid

sys.dont_write_bytecode = True
for variable in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
                 'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[variable] = '1'
HERE = Path(__file__).resolve().parent
ROOT = Path('/Users/bgm/Documents/ChatGPT/Universal Network Theory')
LANES = {
    'hyrec': ('hyrec_inputs_v001/hyrec_full_supervisor_v002.py',
        '7884b0d55beb131b285753ec4144f3d5851b9f6a5235d0af18d026ad359fde13',
        'hyrec_inputs_v001/HYREC_FULL_SUPERVISOR_V002_FROZEN.json',
        'f8a820ca14e389e48f17b22813cdc7caf4bbeaf70e34f4491e392f507536b20d',
        'hyrec_inputs_v001/HYREC_FULL_CASE_{index:03d}_V002.json'),
    'growth': ('finite_slice_growth_transfer_reuse_v002.py',
        'ff54437b25d3420ad0fc7ba2ac54e950457689265ff899847f8e8ca2b594e062',
        'FINITE_SLICE_GROWTH_TRANSFER_V002_FROZEN.json',
        'cd6f2fff3089b07c681895cb610b1e674446ae42fcf80c3a3ee412d31e1db238',
        'FINITE_SLICE_GROWTH_TRANSFER_V002_CASE_{index:03d}.json')}


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def bound(path):
    path.relative_to(ROOT)
    current = ROOT
    if current.is_symlink():
        raise RuntimeError('Project root is a link')
    for part in path.relative_to(ROOT).parts:
        current = current / part
        if current.is_symlink():
            raise RuntimeError('Linked path refused: '+str(current))
    if path.parent.resolve(strict=True) != path.parent:
        raise RuntimeError('Publication ancestry differs')
    return path


def publish(raw, destination):
    """fsync contents, atomic no-overwrite link, then fsync directory."""
    bound(destination)
    if destination.exists() or destination.is_symlink():
        raise FileExistsError('Existing receipt will never be overwritten')
    descriptor, name = tempfile.mkstemp(prefix=destination.name+'.pending.', dir=destination.parent)
    pending = Path(name)
    # A failed publication leaves this exact generated pending file for review.
    with os.fdopen(descriptor, 'wb') as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    bound(destination)
    os.link(pending, destination)  # EEXIST refuses even a concurrent writer.
    directory_fd = os.open(destination.parent, os.O_RDONLY)
    try:
        os.fsync(directory_fd)
    finally:
        os.close(directory_fd)
    pending.unlink()  # Only our exact redundant temporary; final bytes remain.


def main():
    if len(sys.argv) != 3 or sys.argv[1] not in LANES or not sys.argv[2].isdigit():
        raise RuntimeError('Use hyrec|growth and one case index')
    lane, index = sys.argv[1], int(sys.argv[2])
    if not 0 <= index < 335 or Path.cwd().resolve() != ROOT or HERE != ROOT/'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation':
        raise RuntimeError('Wrong case or project context')
    source_name, source_sha, freeze_name, freeze_sha, pattern = LANES[lane]
    source, frozen = bound(HERE/source_name), bound(HERE/freeze_name)
    if sha(source.read_bytes()) != source_sha or sha(frozen.read_bytes()) != freeze_sha:
        raise RuntimeError('Pinned scientific source/freeze changed')
    destination = bound(HERE/pattern.format(index=index))
    if destination.exists() or destination.is_symlink():
        raise FileExistsError('Case already has a receipt; no producer executed')
    started = time.perf_counter()
    buffer = io.StringIO()
    exit_code = 0
    failure = None
    sys.argv = [str(source), 'run-case', str(index)]
    try:
        with contextlib.redirect_stdout(buffer):
            try:
                runpy.run_path(str(source), run_name='__main__')
            except SystemExit as stopped:
                exit_code = stopped.code or 0
                if type(exit_code) is not int:
                    raise RuntimeError('Noninteger producer exit')
        raw = buffer.getvalue().encode('utf-8')
        wrap = json.loads(raw)
        payload = wrap['payload']
        encoded = json.dumps(payload, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()
        if wrap['freeze_sha256'] != freeze_sha or wrap['payload_sha256'] != sha(encoded):
            raise RuntimeError('Produced wrapper custody differs')
        if not isinstance(payload['status'], str) or not isinstance(payload['failures'], list):
            raise RuntimeError('Malformed scientific status')
        produced_index = payload.get('result', {}).get('case_index') if lane == 'hyrec' else payload.get('case_index')
        if type(produced_index) is not int or produced_index != index:
            raise RuntimeError('Produced case identity differs from requested destination')
    except BaseException:
        failure = dict(status='EXECUTION_OR_OUTPUT_VALIDATION_FAILED', lane=lane, case_index=index,
            source_sha256=source_sha, freeze_sha256=freeze_sha, captured_stdout=buffer.getvalue(),
            traceback=traceback.format_exc(), producer_exit_code=exit_code)
        raw = (json.dumps(failure, sort_keys=True, separators=(',', ':'), allow_nan=False)+'\n').encode()
        destination = destination.with_name(destination.name+'.attempt-'+uuid.uuid4().hex+'.json')
    publish(raw, destination)
    if sha(destination.read_bytes()) != sha(raw):
        raise RuntimeError('Published bytes differ')
    payload = failure if failure is not None else payload
    summary = dict(lane=lane, case_index=index, path=str(destination), sha256=sha(raw),
        bytes=len(raw), status=payload['status'], failures=payload.get('failures'),
        producer_exit_code=exit_code, controller_seconds=time.perf_counter()-started,
        source_sha256=source_sha, freeze_sha256=freeze_sha,
        publisher_sha256=sha(Path(__file__).read_bytes()),
        publication='atomic no-overwrite; durable generated scientific output')
    if lane == 'hyrec' and failure is None:
        r = payload['result']
        summary.update(precision_ruler_interval_qualified=r.get('precision_ruler_interval_qualified'),
                       drag=r.get('drag', {}).get('half'))
    print(json.dumps(summary, sort_keys=True, separators=(',', ':'), allow_nan=False), flush=True)
    return 2 if failure is not None else exit_code


if __name__ == '__main__':
    sys.exit(main())
