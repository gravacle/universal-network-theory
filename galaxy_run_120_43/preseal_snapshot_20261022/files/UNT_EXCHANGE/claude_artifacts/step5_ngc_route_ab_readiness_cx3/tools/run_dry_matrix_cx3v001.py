"""Eight isolated cmd_dry_run calls; this harness has no scientific command path."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import datetime
import hashlib
import json
import os
import subprocess
import sys

D = Path(__file__).resolve().parent.parent
PYTHON = '/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
policy = json.loads((D / 'POLICY_CX3V001.json').read_bytes())
assert hashlib.sha256((D / 'POLICY_CX3V001.json').read_bytes()).hexdigest() == '4f0d7d039fcee03fc9e2e1c74624919c77b14e19b101389124864219057e5bbf'
env = dict(os.environ, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1', VECLIB_MAXIMUM_THREADS='1')
jobs = []
for branch, rec in policy['drivers'].items():
    for spec in sorted((D / 'synthetic/filled_v001').glob('CALL_*.json')):
        jobs.append((branch, rec, spec))


def one(job):
    branch, rec, spec = job
    ident = branch + '__' + spec.stem
    dest = D / 'dry' / ident
    dest.mkdir(exist_ok=False)
    driver = rec['driver']
    args = [PYTHON, '-I', '-B', str(D / 'tools/dry_one_step5_cx3v001.py'),
            driver['path'], driver['sha256'], str(spec), hashlib.sha256(spec.read_bytes()).hexdigest(),
            str(dest / 'report'), str(dest / 'LOG_CX3V001.json')]
    completed = subprocess.run(args, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    with (dest / 'HARNESS_RETURN_CX3V001.json').open('x') as f:
        json.dump({'returncode': completed.returncode, 'stdout': completed.stdout, 'stderr': completed.stderr, 'argv': args}, f, indent=2)
        f.write('\n')
    if completed.returncode:
        return {'id': ident, 'harness_return': completed.returncode, 'passed': False}
    log = json.loads((dest / 'LOG_CX3V001.json').read_bytes())
    report = json.loads((dest / 'report/DRYRUN_REPORT.json').read_bytes())
    classes = sorted(report['remaining_refusals']['by_class'])
    result = {'id': ident, 'driver_pin': driver, 'spec_sha256': hashlib.sha256(spec.read_bytes()).hexdigest(),
              'log_pin': {'path': str(dest / 'LOG_CX3V001.json'), 'sha256': hashlib.sha256((dest / 'LOG_CX3V001.json').read_bytes()).hexdigest()},
              'report_pin': {'path': str(dest / 'report/DRYRUN_REPORT.json'), 'sha256': hashlib.sha256((dest / 'report/DRYRUN_REPORT.json').read_bytes()).hexdigest()},
              'executed_stages': report['executed_stages'], 'binding_blockers': report['binding_blockers'],
              'unexplained_refusals': report['remaining_refusals']['unexplained'],
              'static_refusals': report['remaining_refusals']['static'], 'remaining_classes': classes,
              'planned_route_a': report['normalized_spec'].get('_ngc_produces_route_a'),
              'plan_exit': log['exit'], 'elapsed_s': log['elapsed_s'], 'peak_rss_bytes': log['peak_rss_bytes'],
              'memory_limit_note': log['memory_limit_note'], 'audit_blocks': log['blocked'],
              'stages_planned': report['summary']['stages_planned'], 'pin_problems': report['summary']['pin_problems']}
    result['passed'] = (result['executed_stages'] == 0 and not result['binding_blockers'] and not result['unexplained_refusals'] and
                        not result['static_refusals'] and not result['audit_blocks'] and not result['pin_problems'] and
                        set(classes) <= {'PENDING_ROUTE_A_OUTPUTS', 'PENDING_UV_TAIL_CERTIFICATE'} and
                        log['exception'] is None and log['exit'] == 0 and result['planned_route_a'] is True and result['peak_rss_bytes'] < 8 * 1024**3)
    return result


with ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(one, jobs))
out = {'schema': 'UNT_STEP5_DRY_MATRIX_CX3V001', 'date_u': datetime.datetime.now(datetime.timezone.utc).strftime('%a %b %d %H:%M:%S UTC %Y'),
       'status': 'TESTED_PASS' if all(r['passed'] for r in results) else 'TESTED_FAIL', 'plans': len(results), 'results': results,
       'scope': 'Synthetic point dry planning only; no stage execution, physical admission, certificate acceptance or scientific timing.'}
with (D / 'DRY_MATRIX_CX3V001.json').open('x') as f:
    json.dump(out, f, indent=2, sort_keys=True); f.write('\n')
print(json.dumps({'status': out['status'], 'plans': len(results), 'passing': sum(r['passed'] for r in results)}))
sys.exit(0 if all(r['passed'] for r in results) else 1)
