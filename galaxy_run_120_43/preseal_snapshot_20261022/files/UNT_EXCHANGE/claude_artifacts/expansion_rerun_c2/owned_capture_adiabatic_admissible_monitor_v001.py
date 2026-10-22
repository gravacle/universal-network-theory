"""Root-only bounded capture-adiabatic continuation on the admissible pooled same-target capture,
with the terminal estimator-convexity gate; no refit or physical acceptance. Derived from
owned_capture_adiabatic_resume_monitor_v001.py (bbc4f900): worker path/pin, caps, scope and
terminal-status readout changed; sampling/kill logic unchanged."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import time

LANE = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/expansion_rerun_c2')
WORKER = LANE / 'owned_capture_adiabatic_admissible_root_v001.py'
GATE = LANE / 'expansion_convexity_gate_v001.py'
PINS = {WORKER: 'be2998c2d8fbc220ed6e9a914e272c671d953e2112a01d58d260e21c4eae17af',
        GATE: 'c425936134f93d04f9c8a4fcd3c1f65be7fbac821798502dac975ba654c3d16d'}
PYTHON = '/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'


def checked(path, expected):
    import re
    if not re.fullmatch('[0-9a-f]{64}',expected):raise ValueError('Exact SHA256 required')
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    if h.hexdigest()!=expected:raise ValueError('Pin mismatch: '+str(path))


def output_size(out):
    return sum(p.stat().st_size for p in out.rglob('*') if p.is_file())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for key in ('diagnostic-review','diagnostic-review-sha256','outdir'):
        parser.add_argument('--'+key,required=True)
    args=parser.parse_args()
    for path,pin in PINS.items():checked(path,pin)
    checked(args.diagnostic_review,args.diagnostic_review_sha256)
    limits={'wall_seconds':7200,'rss_bytes':2*1024**3,'output_bytes':512*1024**2,'BLAS_threads':1}
    subprocess.run(['/bin/ps', '-p', str(os.getpid()), '-o', 'rss='],
                   check=True, capture_output=True, text=True, timeout=2)
    out = Path(args.outdir).resolve()
    out.mkdir(exist_ok=False)
    command=[PYTHON,'-I','-B',str(WORKER),'--outdir',str(out/'continuation')]
    env = dict(os.environ)
    for name in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
                 'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'BLIS_NUM_THREADS'):
        env[name] = '1'
    record = dict(utc=datetime.now(timezone.utc).isoformat(), status='STARTING',
                  command=command, limits=limits,
                  pins={str(p): s for p, s in PINS.items()},
                  diagnostic_review={'path':args.diagnostic_review,'sha256':args.diagnostic_review_sha256},
                  scope='Capture-adiabatic continuation from tau=0 on the pooled admission+cycle+worm same-target capture with reviewed V003 RHS, thermal branch sign guard and terminal estimator-convexity gate. Same stepper/RHS/step-control law/physical seed as CAPTURE_ADIABATIC_EXACT_RESUME_RUN_V001; failed mixing retained, no DE acceptance.',
                  monitor_semantics='Sampled RSS/output and final checks, not OS hard quotas.', samples=[])
    with (out / 'stdout.txt').open('x') as stdout, (out / 'stderr.txt').open('x') as stderr:
        started = time.monotonic()
        child = subprocess.Popen(command, stdout=stdout, stderr=stderr, env=env)
        record['child_pid'] = child.pid
        (out / 'launch.json').write_text(json.dumps(record, indent=2) + '\n')
        print(json.dumps({'child_pid': child.pid, 'output': str(out)}), flush=True)
        reason = None
        while child.poll() is None:
            elapsed = time.monotonic() - started
            try:
                ps = subprocess.run(['/bin/ps', '-p', str(child.pid), '-o', 'rss='],
                                    capture_output=True, text=True, timeout=2)
                if ps.returncode != 0 or not ps.stdout.strip():
                    if child.poll() is not None:
                        break
                    raise RuntimeError('No live-child RSS')
                rss = int(ps.stdout.strip()) * 1024
                if rss <= 0:
                    raise RuntimeError('Nonpositive live-child RSS')
                combined = rss + resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
                size = output_size(out)
                record['samples'].append(dict(elapsed_seconds=elapsed,
                                              combined_rss_bytes=combined, output_bytes=size))
                if elapsed >= limits['wall_seconds']:
                    reason = 'WALL_CAP'
                elif combined > limits['rss_bytes']:
                    reason = 'MEMORY_CAP'
                elif size > limits['output_bytes']:
                    reason = 'OUTPUT_CAP'
            except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired) as exc:
                if child.poll() is not None:
                    break
                reason = 'MONITOR_UNAVAILABLE: ' + repr(exc)
            if reason:
                if child.poll() is None:
                    child.kill()
                break
            time.sleep(0.1)
        rc = child.wait()
        elapsed = time.monotonic() - started
        combined_peak = (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
                         + resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
        size = output_size(out)
        record.update(status='FINISHED' if rc == 0 else 'FAILED_OR_INCOMPLETE',
                      exit_code=rc, stop_reason=reason, elapsed_seconds=elapsed,
                      conservative_combined_peak_bytes=combined_peak, final_output_bytes=size,
                      within_wall_cap=elapsed <= limits['wall_seconds'],
                      within_memory_cap=combined_peak <= limits['rss_bytes'],
                      within_output_cap=size <= limits['output_bytes'])
        if not all(record[k] for k in ('within_wall_cap', 'within_memory_cap', 'within_output_cap')):
            record['status'] = 'RESOURCE_LIMIT_EXCEEDED'
        finish = out / 'continuation/trajectory/finish.json'
        violation = out / 'continuation/convexity_violation.json'
        initial_failure = out / 'continuation/initial_root_failure.json'
        if finish.is_file():
            raw = finish.read_bytes()
            record['scientific_status'] = json.loads(raw)['status']
            record['finish_sha256'] = hashlib.sha256(raw).hexdigest()
        elif initial_failure.is_file():
            raw = initial_failure.read_bytes()
            record['scientific_status'] = json.loads(raw)['status']
            record['initial_root_failure_sha256'] = hashlib.sha256(raw).hexdigest()
        else:
            record['scientific_status'] = 'NO_COMPLETE_DIAGNOSTIC_RECEIPT'
        if violation.is_file():
            raw = violation.read_bytes()
            record['scientific_status'] = 'ESTIMATOR_CONVEXITY_VIOLATION'
            record['convexity_violation_sha256'] = hashlib.sha256(raw).hexdigest()
        (out / 'receipt.json').write_text(json.dumps(record, indent=2) + '\n')
        print(json.dumps({k: v for k, v in record.items() if k not in ('samples', 'command')}), flush=True)


if __name__ == '__main__':
    main()
