"""INERT campaign launcher for galaxy_m0_forward driver calls (Claude2 lane calibration_orchestrator_c2/v005, c2v005).
c2v005 = campaign_c2v003 (be462862) with exactly two changes (Claude4 R-B C4-4 and the C4-1 read class):
  * every monitor is started with start_new_session=True: its own session and process group, so a signal sent to the
    launching process group (the orchestrator's) never reaches a monitor; each monitor keeps enforcing its wall, RSS and
    output caps on its driver (which the monitor already runs in a session of its own) and writes its receipt;
  * _record_from_receipt also treats an OSError on the result read as an unreadable result (forward None).
Everything else (call directories, monitor command, budget rule, resume rules, record vocabulary, summary) is c2v003.
c2v003 docstring follows.

INERT campaign launcher for galaxy_m0_forward driver calls (Claude2 lane calibration_orchestrator_c2/v003, c2v003).
Successor of campaign_c2v001 (71274ceb, galaxy_m0_forward_c2_0466): identical call directories, monitor command,
resume-by-verified-receipt rules, record vocabulary (OK / FAILED / RESUMED_OK / RESUMED_FAILED / DIR_EXISTS_UNVERIFIED /
NOT_STARTED) and summary file; the only change is how many calls may run at once.

c2v001 rule (replaced): max_concurrent <= 12 and max_concurrent x column_workers <= 12.
c2v003 rule: a DECLARED process budget B (1..17 = 6 performance + 12 efficiency cores, one left for the orchestrator and
the system) and max_concurrent calls (1..B).  Each call has a weight = busy single-thread processes:
  peak  = max(numerics.route_a.column_workers, numerics.column_workers)   while route A may still be running
          (numerics.column_workers alone when the spec admits route A instead of computing it);
  after = numerics.column_workers                                        once route A has finished.
A pending call starts only if (sum of the current weights of the running calls) + its peak <= B and fewer than
max_concurrent calls run (FIFO: the head of the queue is never skipped).  stage_aware=true: a running call's weight drops
from peak to after when ITS OWN driver progress log (<call>/out/progress.jsonl, written by the driver at every stage start
and finish) shows route A finished (an event {stage: route_a, event: finished}) or any later stage started; any read
problem keeps the peak (conservative).  stage_aware=false: peak for the whole call.  Weights never increase during a call
(peak >= after), so the accounted sum is an upper bound of the busy processes at every instant.
Idle parents (monitor, driver, the stage parent of a route-A pool) are not counted: they sleep or poll.

Campaign file (JSON):
 {"calls": [{"spec": {...}} | {"spec_path": P, "spec_sha256": H}, ...], "max_concurrent": N, "process_budget": B,
  "stage_aware": bool, "per_call": {"wall_cap_s", "rss_cap_bytes", "output_cap_bytes", "poll_s"},
  "campaign_wall_cap_s": F, "driver": {"path", "sha256"}, "monitor": {"path", "sha256"}}
CLI:  campaign_c2v005.py --campaign FILE.json --campaign-dir DIR [--resume]
Importing this module does nothing.
"""
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

MODULE_NAME = 'campaign_c2v005'
PROCESS_BUDGET_MAX = 17
PY = '/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
THREAD_ENV = ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS',
              'BLIS_NUM_THREADS')


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
    m = types.ModuleType('c2v005_monitor')
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


def spec_weights(raw):
    """(peak, after) busy processes of one call, from the spec bytes (see module docstring)."""
    spec = json.loads(raw)
    num = spec.get('numerics') or {}
    cw = num.get('column_workers', 1)
    ra = (num.get('route_a') or {}).get('column_workers', 1)
    if type(cw) is not int or cw < 1 or type(ra) is not int or ra < 1:
        raise ValueError('numerics.column_workers / numerics.route_a.column_workers must be positive ints')
    admitted = (spec.get('admit') or {}).get('route_a') is not None
    after = cw
    return (after if admitted else max(ra, after)), after


def route_a_done(call_dir):
    """True only when the driver's own progress log of this call shows route A finished or a later stage started."""
    p = Path(call_dir) / 'out' / 'progress.jsonl'
    try:
        raw = p.read_bytes()
    except OSError:
        return False
    for ln in raw.split(b'\n'):
        if not ln.strip():
            continue
        try:
            d = json.loads(ln.decode('utf-8'))
        except (ValueError, UnicodeDecodeError):
            continue                                            # a line being written
        st, ev = d.get('stage'), d.get('event')
        if st == 'route_a' and ev == 'finished':
            return True
        if isinstance(st, str) and st != 'route_a' and ev == 'started':
            return True
    return False


def _record_from_receipt(i, cdir, rec, status):
    res = None
    rp = (rec.get('result') or {}).get('path')
    if rp and Path(rp).is_file():
        try:
            r = json.loads(Path(rp).read_text())
            res = {'valid': r.get('valid'), 'status': r.get('status'), 'speeds_km_s': r.get('speeds_km_s'), 'reasons': r.get('reasons')}
        except (OSError, ValueError, AttributeError):          # c2v005: unreadable / unparseable / not an object
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
    budget = campaign.get('process_budget')
    stage_aware = campaign.get('stage_aware', False)
    pc = campaign.get('per_call', {})
    cap = campaign.get('campaign_wall_cap_s')
    drv, mon = campaign.get('driver', {}), campaign.get('monitor', {})
    if not isinstance(calls, list) or not calls:
        reasons.append('calls must be a non-empty list')
    if type(budget) is not int or not 1 <= budget <= PROCESS_BUDGET_MAX:
        reasons.append('process_budget must be an int in 1..%d' % PROCESS_BUDGET_MAX)
    if type(n) is not int or not 1 <= n <= PROCESS_BUDGET_MAX or (type(budget) is int and n > budget):
        reasons.append('max_concurrent must be an int in 1..process_budget')
    if type(stage_aware) is not bool:
        reasons.append('stage_aware must be a bool')
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
                peak, after = spec_weights(raw)
                specs.append((raw, hashlib.sha256(raw).hexdigest(), peak, after))
        except Exception as exc:
            reasons.append('%s: %s' % (type(exc).__name__, exc))
    if not reasons and max(s[2] for s in specs) > budget:
        reasons.append('a call needs %d processes > process_budget %d' % (max(s[2] for s in specs), budget))
    if reasons:
        return {'ok': False, 'status': 'REFUSED', 'reasons': reasons, 'calls': []}
    cdir.mkdir(parents=True, exist_ok=True)
    records = [None] * len(specs)
    pending = []
    for i, (raw, ssha, _, _) in enumerate(specs):
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
    max_weight = 0
    launched = 0
    weight_log = []

    def weight(i):
        _, _, peak, after = specs[i]
        if stage_aware and route_a_done(running[i][3]):
            return after
        return peak

    while pending or running:
        while pending and len(running) < n and time.monotonic() - t0 < cap:
            cur = sum(weight(j) for j in running)
            i = pending[0]
            if cur + specs[i][2] > budget:
                break                                           # FIFO: wait until the head fits
            pending.pop(0)
            raw, ssha, _, _ = specs[i]
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
            for k in THREAD_ENV:
                env[k] = '1'
            so = open(d / 'monitor.stdout.txt', 'x')
            se = open(d / 'monitor.stderr.txt', 'x')
            # c2v005 (C4-4): the monitor runs in its own session, outside the launcher's process group
            running[i] = (subprocess.Popen(cmd, stdout=so, stderr=se, env=env, start_new_session=True), so, se, d)
            launched += 1
            max_seen = max(max_seen, len(running))
            w = sum(weight(j) for j in running)
            max_weight = max(max_weight, w)
            weight_log.append({'t': round(time.monotonic() - t0, 3), 'event': 'start', 'call': i, 'accounted': w})
        if pending and time.monotonic() - t0 >= cap and not running:
            break
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
            weight_log.append({'t': round(time.monotonic() - t0, 3), 'event': 'finish', 'call': i,
                               'accounted': sum(weight(j) for j in running)})
        if running:
            time.sleep(0.2)
    for i in pending:
        records[i] = {'index': i, 'status': 'NOT_STARTED', 'reason': 'campaign wall cap reached before start'}
    status = 'CAMPAIGN_CAP' if pending else 'COMPLETE'
    summary = {'ok': True, 'status': status, 'calls': records, 'launched': launched, 'max_concurrent_observed': max_seen,
               'process_budget': budget, 'stage_aware': stage_aware, 'max_accounted_processes': max_weight,
               'call_weights': [{'peak': s[2], 'after_route_a': s[3]} for s in specs], 'weight_log': weight_log,
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
