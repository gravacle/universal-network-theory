"""INERT campaign launcher for galaxy_m0_forward driver calls (Claude2 lane, dispatch 0466, c2v001).

Each call spec runs through root_monitor_c2v001 (one monitor child process per call) in its own
fresh directory  CAMPAIGN/call_NNNN/{spec.json, out/, RECEIPT.json(+.launch/.stdout/.stderr)}.
Rules: at most max_concurrent calls at once (<=12, and max_concurrent*column_workers<=12);
fresh directories only; resumable by VERIFIED receipt (self-hash, spec and driver pins, result
hash from bytes): verified calls are skipped (RESUMED_OK / RESUMED_FAILED) and failed calls are
never rerun automatically; an existing call directory without a verifying receipt is
DIR_EXISTS_UNVERIFIED and is never touched; after the campaign wall cap no new call starts
(running calls finish under their own caps); results are returned in input order and written to
a new CAMPAIGN/campaign_summary_<utc>_<pid>_<ns>.json.

Campaign file (JSON):
 {"calls": [{"spec": {...call spec...}} | {"spec_path": P, "spec_sha256": H}, ...],
  "max_concurrent": N, "per_call": {"wall_cap_s": F, "rss_cap_bytes": N, "output_cap_bytes": N, "poll_s": F},
  "campaign_wall_cap_s": F, "driver": {"path": P, "sha256": H}, "monitor": {"path": P, "sha256": H}}
CLI:  campaign_c2v001.py --campaign FILE.json --campaign-dir DIR [--resume]
Importing this module does nothing.
"""
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

PY = '/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def _load_monitor(path, sha):
    import types
    raw = Path(path).read_bytes()
    if hashlib.sha256(raw).hexdigest() != sha:
        raise ValueError('monitor pin mismatch')
    m = types.ModuleType('c2v001_monitor')
    m.__file__ = str(path)
    exec(compile(raw, str(path), 'exec'), m.__dict__)
    return m


def _spec_bytes(call):
    if 'spec' in call:
        return (json.dumps(call['spec'], indent=1, sort_keys=True, allow_nan=False) + '\n').encode()
    raw = Path(call['spec_path']).read_bytes()
    if hashlib.sha256(raw).hexdigest() != call['spec_sha256']:
        raise ValueError('spec pin mismatch: %s' % call['spec_path'])
    return raw


def _record_from_receipt(i, cdir, rec, status):
    res = None
    rp = (rec.get('result') or {}).get('path')
    if rp and Path(rp).is_file():
        try:
            r = json.loads(Path(rp).read_text())
            res = {'valid': r.get('valid'), 'status': r.get('status'), 'speeds_km_s': r.get('speeds_km_s'), 'reasons': r.get('reasons')}
        except ValueError:
            res = None
    return {'index': i, 'call_dir': str(cdir), 'status': status, 'monitor_status': rec.get('status'),
            'stop_reason': rec.get('stop_reason'), 'exit_code': rec.get('exit_code'), 'driver_status': rec.get('driver_status'),
            'receipt_sha256': rec.get('receipt_sha256'), 'result': rec.get('result'), 'forward': res,
            'elapsed_seconds': rec.get('elapsed_seconds'), 'peak_rss_bytes': rec.get('peak_rss_bytes')}


def run_campaign(*, campaign, campaign_dir, resume=False, python=PY):
    cdir = Path(campaign_dir)
    reasons = []
    calls = campaign.get('calls')
    n = campaign.get('max_concurrent')
    pc = campaign.get('per_call', {})
    cap = campaign.get('campaign_wall_cap_s')
    drv, mon = campaign.get('driver', {}), campaign.get('monitor', {})
    if not isinstance(calls, list) or not calls:
        reasons.append('calls must be a non-empty list')
    if type(n) is not int or not 1 <= n <= 12:
        reasons.append('max_concurrent must be an int in 1..12')
    if not (isinstance(cap, (int, float)) and cap > 0):
        reasons.append('campaign_wall_cap_s must be > 0')
    for k in ('path', 'sha256'):
        if k not in drv or k not in mon:
            reasons.append('driver/monitor {path, sha256} required')
            break
    if cdir.exists() and not resume:
        reasons.append('campaign dir exists; pass resume=True to resume by verified receipt')
    specs = []
    if not reasons:
        try:
            monitor = _load_monitor(mon['path'], mon['sha256'])
            if sha256_file(drv['path']) != drv['sha256']:
                raise ValueError('driver pin mismatch')
            for c in calls:
                raw = _spec_bytes(c)
                workers = 1
                try:
                    workers = int(json.loads(raw).get('numerics', {}).get('column_workers', 1))
                except Exception:
                    pass
                specs.append((raw, hashlib.sha256(raw).hexdigest(), workers))
        except Exception as exc:
            reasons.append('%s: %s' % (type(exc).__name__, exc))
    if not reasons and n * max(w for _, _, w in specs) > 12:
        reasons.append('max_concurrent * column_workers exceeds 12 single-thread processes')
    if reasons:
        return {'ok': False, 'status': 'REFUSED', 'reasons': reasons, 'calls': []}
    cdir.mkdir(parents=True, exist_ok=True)
    records = [None] * len(specs)
    pending = []
    for i, (raw, ssha, _) in enumerate(specs):
        d = cdir / ('call_%04d' % i)
        if d.exists():
            rp = d / 'RECEIPT.json'
            v = monitor.verify_receipt(rp, spec_sha256=ssha, driver_sha256=drv['sha256']) if rp.is_file() else {'ok': False, 'reasons': ['no receipt']}
            if v['ok'] and (d / 'spec.json').is_file() and sha256_file(d / 'spec.json') == ssha:
                ok = v['receipt'].get('status') == 'FINISHED' and v['receipt'].get('driver_status') == 'COMPLETED'
                records[i] = _record_from_receipt(i, d, v['receipt'], 'RESUMED_OK' if ok else 'RESUMED_FAILED')
            else:
                records[i] = {'index': i, 'call_dir': str(d), 'status': 'DIR_EXISTS_UNVERIFIED', 'reasons': v['reasons']}
        else:
            pending.append(i)
    t0 = time.monotonic()
    running = {}
    max_seen = 0
    launched = 0
    while pending or running:
        while pending and len(running) < n and time.monotonic() - t0 < cap:
            i = pending.pop(0)
            raw, ssha, _ = specs[i]
            d = cdir / ('call_%04d' % i)
            d.mkdir(exist_ok=False)
            with open(d / 'spec.json', 'xb') as f:
                f.write(raw)
                f.flush()
                os.fsync(f.fileno())
            cmd = [python, '-I', '-B', mon['path'], '--driver', drv['path'], '--driver-sha256', drv['sha256'],
                   '--spec', str(d / 'spec.json'), '--outdir', str(d / 'out'), '--receipt', str(d / 'RECEIPT.json'),
                   '--wall-cap-s', repr(float(pc['wall_cap_s'])), '--rss-cap-bytes', str(int(pc['rss_cap_bytes'])),
                   '--output-cap-bytes', str(int(pc['output_cap_bytes'])), '--poll-s', repr(float(pc.get('poll_s', 1.0))),
                   '--python', python]
            env = {k: v for k, v in os.environ.items() if not k.startswith('PYTHON')}
            for k in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'BLIS_NUM_THREADS'):
                env[k] = '1'
            so = open(d / 'monitor.stdout.txt', 'x')
            se = open(d / 'monitor.stderr.txt', 'x')
            running[i] = (subprocess.Popen(cmd, stdout=so, stderr=se, env=env), so, se, d)
            launched += 1
            max_seen = max(max_seen, len(running))
        if pending and time.monotonic() - t0 >= cap and not running:
            break
        if pending and time.monotonic() - t0 >= cap:
            pass  # no new starts; wait for running calls
        done = [i for i, (p, _, _, _) in running.items() if p.poll() is not None]
        for i in done:
            p, so, se, d = running.pop(i)
            so.close()
            se.close()
            rp = d / 'RECEIPT.json'
            v = monitor.verify_receipt(rp, spec_sha256=specs[i][1], driver_sha256=drv['sha256']) if rp.is_file() else {'ok': False, 'reasons': ['monitor wrote no receipt'], 'receipt': None}
            if v['ok']:
                rec = v['receipt']
                ok = rec.get('status') == 'FINISHED' and rec.get('driver_status') == 'COMPLETED'
                records[i] = _record_from_receipt(i, d, rec, 'OK' if ok else 'FAILED')
            else:
                records[i] = {'index': i, 'call_dir': str(d), 'status': 'FAILED', 'reasons': v['reasons'], 'monitor_exit': p.returncode}
        if running:
            time.sleep(0.2)
    for i in pending:
        records[i] = {'index': i, 'status': 'NOT_STARTED', 'reason': 'campaign wall cap reached before start'}
    status = 'CAMPAIGN_CAP' if pending else 'COMPLETE'
    summary = {'ok': True, 'status': status, 'calls': records, 'launched': launched, 'max_concurrent_observed': max_seen,
               'n_ok': sum(1 for r in records if r['status'] in ('OK', 'RESUMED_OK')),
               'n_failed': sum(1 for r in records if r['status'] in ('FAILED', 'RESUMED_FAILED')),
               'n_resumed': sum(1 for r in records if r['status'].startswith('RESUMED')),
               'n_not_started': sum(1 for r in records if r['status'] == 'NOT_STARTED'),
               'n_unverified': sum(1 for r in records if r['status'] == 'DIR_EXISTS_UNVERIFIED'),
               'campaign_wall_used_s': time.monotonic() - t0, 'retries': 0}
    sp = cdir / ('campaign_summary_%s_%d_%d.json' % (time.strftime('%Y%m%dT%H%M%SZ', time.gmtime()), os.getpid(), time.time_ns()))
    with open(sp, 'x') as f:
        json.dump(summary, f, indent=1, allow_nan=False)
        f.write('\n')
    summary['summary_path'] = str(sp)
    return summary


def main(argv=None):
    import argparse
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--campaign', required=True)
    ap.add_argument('--campaign-dir', required=True)
    ap.add_argument('--resume', action='store_true')
    ap.add_argument('--python', default=PY)
    a = ap.parse_args(argv)
    out = run_campaign(campaign=json.loads(Path(a.campaign).read_text()), campaign_dir=a.campaign_dir, resume=a.resume, python=a.python)
    print(json.dumps({k: v for k, v in out.items() if k != 'calls'}, indent=1))
    return 0 if out['ok'] else 2


if __name__ == '__main__':
    sys.exit(main())
