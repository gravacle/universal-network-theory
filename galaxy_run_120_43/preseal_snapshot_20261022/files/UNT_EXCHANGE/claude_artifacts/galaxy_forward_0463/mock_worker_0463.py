#!/usr/bin/env python3
"""mock_worker_0463.py -- official mock worker for the 0463 campaign-runner fixtures.

Written from INTERFACE_0463_V001.md alone (independent fixture author), before any
module under test was read.  Standard library only.  Deterministic.

Command line (EXACTLY the real worker command line, verified from the interface):

  <python> -I -B mock_worker_0463.py --seed <seed.json> --seed-sha256 <hex>
      --solver <solver.py> --solver-sha256 <hex>
      --checkpoint-module <ckpt.py> --checkpoint-module-sha256 <hex>
      --outdir <dir> --checkpoint-directory <dir> --start-iteration <int> [--resume]

Behaviour:
  1. Verify the SHA256 (over bytes) of the seed, solver and checkpoint-module files
     against the given hex pins.  Any mismatch or unreadable file -> exit 2, nothing
     written under --outdir.
  2. Read the seed (JSON).  Read seed['mock'] = {'sleep_s': float,
     'mode': 'ok'|'exit_nonzero'|'hang'|'rss'|'output'|'nan'|'missing_result',
     'speeds': {id: float}}.  A missing/invalid mock block -> exit 4.
  3. Write <outdir>/start.json with an ISO-8601 UTC start timestamp (plus a float
     unix timestamp, pid, pgid, mode, sleep_s, argv, resume flag, start_iteration).
     Append a line to <outdir>/progress.jsonl.
  4. Act on the mode:
       ok             sleep sleep_s; write result.json deterministically from the seed
                      (see RESULT LAYOUT); write finish.json; exit 0
       exit_nonzero   sleep sleep_s; write finish.json (no result.json); exit 3
       hang           sleep 3600 s (never writes finish.json / result.json)
       rss            allocate ~300 MB, touch every page, hold for sleep_s, then
                      behave like 'ok' (result.json + finish.json; exit 0)
       output         write ~50 MB of bytes to <outdir>/bulk_output.bin, hold for
                      sleep_s, then behave like 'ok' (exit 0)
       nan            sleep sleep_s; write result.json with the FIRST speed (sorted id)
                      replaced by NaN (JSON token NaN); write finish.json; exit 0
       missing_result sleep sleep_s; write finish.json only (no result.json); exit 0

RESULT LAYOUT (result.json; deterministic: no timestamps, canonical key order):
  {'result': {'speeds_km_s': {id: float}, 'valid': true},
   'mock': {'mode': str, 'sleep_s': float},
   'schema': 'MOCK_RESULT_0463_V001',
   'seed_sha256': <hex of the seed bytes>,
   'start_iteration': int,
   'resume': bool}
  For mode 'nan' the layout is the same but one speed is NaN and the JSON is written
  with allow_nan=True (a reader must treat it as invalid).

Exit codes: 0 ok; 2 pin mismatch / unreadable pinned file (argparse usage errors also
exit 2); 3 requested by mode 'exit_nonzero'; 4 seed unreadable or mock block invalid.
"""
import argparse
import hashlib
import json
import math
import os
import sys
import time
from datetime import datetime, timezone

MODES = ('ok', 'exit_nonzero', 'hang', 'rss', 'output', 'nan', 'missing_result')
RSS_ALLOC_BYTES = 300 * 1024 * 1024
OUTPUT_BYTES = 50 * 1024 * 1024
OUTPUT_CHUNK = 1024 * 1024
HANG_SECONDS = 3600.0


def _sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        while True:
            chunk = fh.read(1 << 20)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def _now_iso():
    return datetime.now(timezone.utc).isoformat()


def _write_json(path, obj, allow_nan=False):
    data = json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=allow_nan)
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(data)
        fh.flush()
        os.fsync(fh.fileno())


def _append_progress(outdir, record):
    with open(os.path.join(outdir, 'progress.jsonl'), 'a', encoding='utf-8') as fh:
        fh.write(json.dumps(record, sort_keys=True, separators=(',', ':')) + '\n')


def _parse_args(argv):
    p = argparse.ArgumentParser(prog='mock_worker_0463.py', add_help=True)
    p.add_argument('--seed', required=True)
    p.add_argument('--seed-sha256', required=True)
    p.add_argument('--solver', required=True)
    p.add_argument('--solver-sha256', required=True)
    p.add_argument('--checkpoint-module', required=True)
    p.add_argument('--checkpoint-module-sha256', required=True)
    p.add_argument('--outdir', required=True)
    p.add_argument('--checkpoint-directory', required=True)
    p.add_argument('--start-iteration', required=True, type=int)
    p.add_argument('--resume', action='store_true')
    return p.parse_args(argv)


def _verify_pin(label, path, expected):
    try:
        actual = _sha256_file(path)
    except OSError as exc:
        sys.stderr.write('PIN_UNREADABLE %s %s: %s\n' % (label, path, exc))
        return False
    if actual != str(expected).strip().lower():
        sys.stderr.write('PIN_MISMATCH %s %s expected=%s actual=%s\n' % (label, path, expected, actual))
        return False
    return True


def _load_mock_block(seed_path):
    with open(seed_path, 'r', encoding='utf-8') as fh:
        seed = json.load(fh)
    if not isinstance(seed, dict) or not isinstance(seed.get('mock'), dict):
        raise ValueError('seed has no dict field "mock"')
    mock = seed['mock']
    mode = mock.get('mode')
    if mode not in MODES:
        raise ValueError('mock.mode %r not in %r' % (mode, MODES))
    sleep_s = mock.get('sleep_s')
    if not isinstance(sleep_s, (int, float)) or isinstance(sleep_s, bool) or not math.isfinite(float(sleep_s)) or sleep_s < 0:
        raise ValueError('mock.sleep_s must be a finite non-negative number')
    speeds = mock.get('speeds')
    if not isinstance(speeds, dict) or not speeds:
        raise ValueError('mock.speeds must be a non-empty dict')
    clean = {}
    for key in sorted(speeds):
        val = speeds[key]
        if not isinstance(key, str) or not isinstance(val, (int, float)) or isinstance(val, bool) or not math.isfinite(float(val)):
            raise ValueError('mock.speeds[%r] is not a finite float' % (key,))
        clean[key] = float(val)
    return mode, float(sleep_s), clean


def _result_object(mode, sleep_s, speeds, seed_sha256, start_iteration, resume):
    return {
        'schema': 'MOCK_RESULT_0463_V001',
        'result': {'speeds_km_s': dict(speeds), 'valid': True},
        'mock': {'mode': mode, 'sleep_s': sleep_s},
        'seed_sha256': seed_sha256,
        'start_iteration': int(start_iteration),
        'resume': bool(resume),
    }


def _sleep(seconds):
    end = time.monotonic() + max(0.0, float(seconds))
    while True:
        remaining = end - time.monotonic()
        if remaining <= 0:
            return
        time.sleep(min(remaining, 0.5))


def main(argv):
    args = _parse_args(argv)
    seed_path = os.path.abspath(args.seed)
    solver_path = os.path.abspath(args.solver)
    ckpt_path = os.path.abspath(args.checkpoint_module)
    outdir = os.path.abspath(args.outdir)
    ckpt_dir = os.path.abspath(args.checkpoint_directory)

    pins_ok = True
    pins_ok &= _verify_pin('seed', seed_path, args.seed_sha256)
    pins_ok &= _verify_pin('solver', solver_path, args.solver_sha256)
    pins_ok &= _verify_pin('checkpoint_module', ckpt_path, args.checkpoint_module_sha256)
    if not pins_ok:
        sys.stderr.flush()
        return 2
    seed_sha256 = str(args.seed_sha256).strip().lower()

    try:
        mode, sleep_s, speeds = _load_mock_block(seed_path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        sys.stderr.write('SEED_INVALID %s: %s\n' % (seed_path, exc))
        sys.stderr.flush()
        return 4

    os.makedirs(outdir, exist_ok=True)
    os.makedirs(ckpt_dir, exist_ok=True)

    t_start_unix = time.time()
    start_record = {
        'schema': 'MOCK_START_0463_V001',
        'started_utc': _now_iso(),
        'started_unix': t_start_unix,
        'pid': os.getpid(),
        'pgid': os.getpgid(0),
        'mode': mode,
        'sleep_s': sleep_s,
        'start_iteration': int(args.start_iteration),
        'resume': bool(args.resume),
        'seed_sha256': seed_sha256,
        'argv': list(argv),
    }
    _write_json(os.path.join(outdir, 'start.json'), start_record)
    _append_progress(outdir, {'phase': 'start', 'mode': mode, 'unix': t_start_unix})
    sys.stdout.write('mock_worker_0463 start mode=%s sleep_s=%s pid=%d\n' % (mode, sleep_s, os.getpid()))
    sys.stdout.flush()

    result_obj = _result_object(mode, sleep_s, speeds, seed_sha256, args.start_iteration, args.resume)
    holder = None  # keeps the RSS allocation alive

    if mode == 'hang':
        _append_progress(outdir, {'phase': 'hang', 'unix': time.time()})
        _sleep(HANG_SECONDS)
        # Not expected to be reached (the runner must kill the process group).
        _write_json(os.path.join(outdir, 'finish.json'), {
            'schema': 'MOCK_FINISH_0463_V001', 'finished_utc': _now_iso(), 'finished_unix': time.time(),
            'mode': mode, 'exit_code': 0, 'note': 'hang expired without being killed'})
        return 0

    if mode == 'rss':
        holder = bytearray(RSS_ALLOC_BYTES)
        for off in range(0, RSS_ALLOC_BYTES, 4096):  # touch every page so RSS really grows
            holder[off] = 1
        _append_progress(outdir, {'phase': 'rss_allocated', 'bytes': RSS_ALLOC_BYTES, 'unix': time.time()})
        _sleep(sleep_s)
    elif mode == 'output':
        bulk_path = os.path.join(outdir, 'bulk_output.bin')
        written = 0
        with open(bulk_path, 'wb') as fh:
            i = 0
            while written < OUTPUT_BYTES:
                fh.write(bytes([i % 256]) * OUTPUT_CHUNK)
                written += OUTPUT_CHUNK
                i += 1
            fh.flush()
            os.fsync(fh.fileno())
        _append_progress(outdir, {'phase': 'output_written', 'bytes': written, 'unix': time.time()})
        _sleep(sleep_s)
    else:
        _sleep(sleep_s)

    exit_code = 0
    if mode == 'exit_nonzero':
        exit_code = 3
    elif mode == 'nan':
        first_id = sorted(result_obj['result']['speeds_km_s'])[0]
        result_obj['result']['speeds_km_s'][first_id] = float('nan')
        _write_json(os.path.join(outdir, 'result.json'), result_obj, allow_nan=True)
    elif mode == 'missing_result':
        pass
    else:  # ok, rss, output
        _write_json(os.path.join(outdir, 'result.json'), result_obj)

    t_end = time.time()
    _append_progress(outdir, {'phase': 'finish', 'exit_code': exit_code, 'unix': t_end})
    _write_json(os.path.join(outdir, 'finish.json'), {
        'schema': 'MOCK_FINISH_0463_V001',
        'finished_utc': _now_iso(),
        'finished_unix': t_end,
        'mode': mode,
        'exit_code': exit_code,
        'result_json_written': mode in ('ok', 'rss', 'output', 'nan'),
        'wall_s': t_end - t_start_unix,
    })
    sys.stdout.write('mock_worker_0463 finish mode=%s exit_code=%d\n' % (mode, exit_code))
    sys.stdout.flush()
    del holder
    return exit_code


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
