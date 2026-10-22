"""INERT root monitor for ONE galaxy_m0_forward driver call (Claude2 lane, dispatch 0466, c2v001).

Runs  <python> -I -B <driver> run --spec SPEC --outdir OUTDIR  as a child in its own session
(process group), single-threaded BLAS env, and enforces:
  hard wall cap, sampled RSS cap (sum of rss over the child's whole process tree via ps),
  output-size cap (total bytes under OUTDIR), OUTDIR absent before start, no automatic retry.
Writes (exclusive create, fsync):  RECEIPT.launch.json at start, RECEIPT at end with command,
pins (driver and spec SHA256 from bytes), caps, exit code, elapsed, peak RSS, peak output bytes,
samples, stop reason, driver finish status and result.json SHA256, and a self-hash.

CLI:  root_monitor_c2v001.py --driver D --driver-sha256 H --spec S --outdir O --receipt R
        --wall-cap-s F --rss-cap-bytes N --output-cap-bytes N [--poll-s F] [--python P]
Importing this module does nothing.
"""
import hashlib
import json
import os
import signal
import subprocess
import sys
import time
from pathlib import Path

PY = '/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
RECEIPT_SCHEMA = 'UNT_GALAXY_M0_MONITOR_RECEIPT_C2V001'
THREAD_ENV = ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS',
              'VECLIB_MAXIMUM_THREADS', 'BLIS_NUM_THREADS')
MAX_SAMPLES = 20000


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False)


def utc():
    return time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())


def tree_rss_bytes(root_pid):
    """Sum of RSS (bytes) over root_pid and all descendants, from one `ps` snapshot."""
    try:
        out = subprocess.run(['ps', '-A', '-o', 'pid=,ppid=,rss='], capture_output=True, text=True, timeout=20).stdout
    except Exception:
        return None, []
    kids, rss = {}, {}
    for line in out.splitlines():
        parts = line.split()
        if len(parts) != 3:
            continue
        try:
            pid, ppid, kb = int(parts[0]), int(parts[1]), int(parts[2])
        except ValueError:
            continue
        rss[pid] = kb * 1024
        kids.setdefault(ppid, []).append(pid)
    if root_pid not in rss:
        return 0, []
    total, stack, members = 0, [root_pid], []
    while stack:
        p = stack.pop()
        if p in members:
            continue
        members.append(p)
        total += rss.get(p, 0)
        stack.extend(kids.get(p, []))
    return total, members


def dir_bytes(path):
    total = 0
    for root, dirs, files in os.walk(path):
        for name in files:
            try:
                total += os.lstat(os.path.join(root, name)).st_size
            except OSError:
                pass
    return total


def _write_x(path, obj):
    with open(path, 'x') as f:
        f.write(json.dumps(obj, indent=1, sort_keys=True, allow_nan=False) + '\n')
        f.flush()
        os.fsync(f.fileno())


def _kill_group(proc):
    try:
        os.killpg(proc.pid, signal.SIGTERM)
    except ProcessLookupError:
        return
    try:
        proc.wait(timeout=15)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        proc.wait()


def run_monitored(*, driver, driver_sha256, spec, outdir, receipt, wall_cap_s, rss_cap_bytes, output_cap_bytes,
                  poll_s=1.0, python=PY):
    """Returns the receipt dict (also written to `receipt`).  Refusals return {'status':'REFUSED'}
    without starting anything and without writing a receipt."""
    driver, spec, outdir, receipt = Path(driver), Path(spec), Path(outdir), Path(receipt)
    reasons = []
    if not (isinstance(wall_cap_s, (int, float)) and wall_cap_s > 0):
        reasons.append('wall cap must be > 0')
    for v, n in ((rss_cap_bytes, 'rss cap'), (output_cap_bytes, 'output cap')):
        if type(v) is not int or v <= 0:
            reasons.append(n + ' must be a positive int')
    if not (isinstance(poll_s, (int, float)) and 0 < poll_s <= 60):
        reasons.append('poll_s must be in (0,60]')
    if outdir.exists():
        reasons.append('outdir exists (must be absent): %s' % outdir)
    launch_path = receipt.with_name(receipt.name + '.launch.json')
    if receipt.exists() or launch_path.exists():
        reasons.append('receipt or launch record exists: %s' % receipt)
    if not driver.is_file() or sha256_file(driver) != driver_sha256:
        reasons.append('driver pin mismatch or missing: %s' % driver)
    if not spec.is_file():
        reasons.append('spec missing: %s' % spec)
    if reasons:
        return {'status': 'REFUSED', 'reasons': reasons}
    spec_sha = sha256_file(spec)
    receipt.parent.mkdir(parents=True, exist_ok=True)
    cmd = [python, '-I', '-B', str(driver), 'run', '--spec', str(spec), '--outdir', str(outdir)]
    env = {k: v for k, v in os.environ.items() if not k.startswith('PYTHON')}
    for k in THREAD_ENV:
        env[k] = '1'
    caps = {'wall_cap_s': wall_cap_s, 'rss_cap_bytes': rss_cap_bytes, 'output_cap_bytes': output_cap_bytes, 'poll_s': poll_s}
    pins = {'driver': {'path': str(driver), 'sha256': driver_sha256}, 'spec': {'path': str(spec), 'sha256': spec_sha},
            'python': python, 'monitor': {'path': str(Path(__file__).resolve()), 'sha256': sha256_file(__file__)}}
    so = open(receipt.with_name(receipt.name + '.stdout.txt'), 'x')
    se = open(receipt.with_name(receipt.name + '.stderr.txt'), 'x')
    t0 = time.monotonic()
    started = utc()
    proc = subprocess.Popen(cmd, stdout=so, stderr=se, env=env, start_new_session=True)
    _write_x(launch_path, {'schema': RECEIPT_SCHEMA + '_LAUNCH', 'utc': started, 'command': cmd, 'pins': pins, 'caps': caps,
                           'child_pid': proc.pid, 'retries_allowed': 0})
    samples, peak_rss, peak_out, stop = [], 0, 0, None
    while True:
        code = proc.poll()
        el = time.monotonic() - t0
        rss, members = tree_rss_bytes(proc.pid)
        outb = dir_bytes(outdir) if outdir.exists() else 0
        if rss is not None:
            peak_rss = max(peak_rss, rss)
        peak_out = max(peak_out, outb)
        if len(samples) < MAX_SAMPLES:
            samples.append([round(el, 3), rss, outb, len(members)])
        if code is not None:
            break
        if el > wall_cap_s:
            stop = 'WALL_CAP'
        elif rss is not None and rss > rss_cap_bytes:
            stop = 'RSS_CAP'
        elif outb > output_cap_bytes:
            stop = 'OUTPUT_CAP'
        if stop:
            _kill_group(proc)
            break
        time.sleep(poll_s)
    code = proc.wait()
    so.close()
    se.close()
    elapsed = time.monotonic() - t0
    finish = outdir / 'finish.json'
    res = outdir / 'result.json'
    driver_status = None
    if finish.is_file():
        try:
            driver_status = json.loads(finish.read_text()).get('status')
        except ValueError:
            driver_status = 'UNREADABLE_FINISH'
    result = {'path': str(res), 'sha256': sha256_file(res)} if res.is_file() else None
    if result is not None and finish.is_file():
        try:
            if json.loads(finish.read_text()).get('result_sha256') != result['sha256']:
                driver_status = 'RESULT_HASH_MISMATCH'
        except ValueError:
            pass
    rec = {'schema': RECEIPT_SCHEMA, 'utc_start': started, 'utc_end': utc(), 'command': cmd, 'pins': pins, 'caps': caps,
           'child_pid': proc.pid, 'exit_code': code, 'elapsed_seconds': elapsed, 'peak_rss_bytes': peak_rss,
           'peak_output_bytes': peak_out, 'final_output_bytes': dir_bytes(outdir) if outdir.exists() else 0,
           'n_samples': len(samples), 'samples': samples, 'stop_reason': stop, 'driver_status': driver_status,
           'result': result, 'retries': 0,
           'status': 'FINISHED' if (stop is None and code == 0) else ('STOPPED_' + stop if stop else 'CHILD_FAILED')}
    rec['receipt_sha256'] = hashlib.sha256(canonical(rec).encode()).hexdigest()
    _write_x(receipt, rec)
    return rec


def verify_receipt(path, *, spec_sha256=None, driver_sha256=None):
    """Self-hash, optional expected pins, and result.json hash re-verified from bytes."""
    reasons = []
    try:
        rec = json.loads(Path(path).read_text())
    except Exception as exc:
        return {'ok': False, 'reasons': ['unreadable receipt: %s' % exc], 'receipt': None}
    claimed = rec.pop('receipt_sha256', None)
    if claimed != hashlib.sha256(canonical(rec).encode()).hexdigest():
        reasons.append('receipt self-hash mismatch')
    rec['receipt_sha256'] = claimed
    if rec.get('schema') != RECEIPT_SCHEMA:
        reasons.append('schema mismatch')
    if spec_sha256 is not None and rec.get('pins', {}).get('spec', {}).get('sha256') != spec_sha256:
        reasons.append('spec pin differs')
    if driver_sha256 is not None and rec.get('pins', {}).get('driver', {}).get('sha256') != driver_sha256:
        reasons.append('driver pin differs')
    r = rec.get('result')
    if r is not None:
        if not Path(r['path']).is_file() or sha256_file(r['path']) != r['sha256']:
            reasons.append('result.json hash does not verify')
    return {'ok': not reasons, 'reasons': reasons, 'receipt': rec}


def main(argv=None):
    import argparse
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    for k in ('driver', 'driver-sha256', 'spec', 'outdir', 'receipt'):
        ap.add_argument('--' + k, required=True)
    ap.add_argument('--wall-cap-s', type=float, required=True)
    ap.add_argument('--rss-cap-bytes', type=int, required=True)
    ap.add_argument('--output-cap-bytes', type=int, required=True)
    ap.add_argument('--poll-s', type=float, default=1.0)
    ap.add_argument('--python', default=PY)
    a = ap.parse_args(argv)
    rec = run_monitored(driver=a.driver, driver_sha256=a.driver_sha256, spec=a.spec, outdir=a.outdir, receipt=a.receipt,
                        wall_cap_s=a.wall_cap_s, rss_cap_bytes=a.rss_cap_bytes, output_cap_bytes=a.output_cap_bytes,
                        poll_s=a.poll_s, python=a.python)
    summary = {k: rec.get(k) for k in ('status', 'reasons', 'exit_code', 'stop_reason', 'driver_status', 'elapsed_seconds',
                                       'peak_rss_bytes', 'result')}
    print(json.dumps(summary))
    return 2 if rec['status'] == 'REFUSED' else (0 if rec['status'] == 'FINISHED' else 1)


if __name__ == '__main__':
    sys.exit(main())
