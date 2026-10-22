"""Second dry-run set: c2v008 vs c2v009 on COMPUTE-mode test specs at the <=96-node registered grids (G3, G4, GR; serial and
N=8 route A), so the full route-A request (prep v008 LOCAL injection, seed, argv) and every planned stage are compared.
The test specs are the R3 specs with admit -> {} (and route_a for the N=8 variant) only; written to specs/test/.
Usage: python3 -I -B run_dry_byteid2_c2ext.py OUT_DIR   (same guard, env, nice and <=4 concurrency as run_dry_c2ext.py)."""
import json
import os
import subprocess
import sys
import time
from pathlib import Path

PY = '/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
EX = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
HERE = EX / 'kmax_prereg_v005_c2/extension_c5c6'
GUARD = HERE / 'tools/guard_c2ext.py'
DRV = {'v008': EX / 'driver_v008_c2/galaxy_m0_forward_c2v008.py', 'v009': HERE / 'driver_v009/galaxy_m0_forward_c2v009.py'}
R3S = EX / 'kmax_prereg_v005_c2/d7_recovery_r3/specs_d7r3'
SRC = {'C3COMP_G3': ('CALL_KMAX_C3R3_A2F10_D7R3_C2V005.json', None), 'C4COMP_G4': ('CALL_KMAX_C4R3_A2F10_D7R3_C2V005.json', None),
       'C4COMP_N8_G4': ('CALL_KMAX_C4R3_A2F10_D7R3_C2V005.json', {'column_workers': 8}),
       'RRCOMP_GR': ('CALL_KMAX_RR3_A2F10_D7R3_C2V005.json', None)}


def main():
    out = Path(sys.argv[1]).resolve()
    (out / 'dry').mkdir(parents=True, exist_ok=True)
    (out / 'logs').mkdir(exist_ok=True)
    (HERE / 'specs/test').mkdir(exist_ok=True)
    jobs = []
    for k, (fn, ra) in SRC.items():
        s = json.loads((R3S / fn).read_text())
        s['admit'] = {}
        if ra is not None:
            s['numerics']['route_a'] = ra
        s['label'] = 'TEST ONLY (dry run, c2v008 vs c2v009 byte identity): %s with admit {}%s' % (fn, '' if ra is None else ' and numerics.route_a %s' % json.dumps(ra))
        p = HERE / 'specs/test' / ('TEST_%s.json' % k)
        if not p.exists():
            with open(p, 'x') as f:
                f.write(json.dumps(s, indent=1, sort_keys=True) + '\n')
        for v in ('v008', 'v009'):
            jobs.append(('%s_%s' % (v, k), v, p))
    env = {k: v for k, v in os.environ.items() if not k.startswith('PYTHON')}
    for k in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'BLIS_NUM_THREADS'):
        env[k] = '1'
    os.nice(10)
    pending, running, done = list(jobs), [], []
    while pending or running:
        while pending and len(running) < 4:
            name, v, s = pending.pop(0)
            so = open(out / 'logs' / (name + '.stdout.txt'), 'x')
            se = open(out / 'logs' / (name + '.stderr.txt'), 'x')
            cmd = [PY, '-I', '-B', str(GUARD), str(out / 'logs' / (name + '.guard.json')), str(DRV[v]), 'dry-run', '--spec', str(s),
                   '--report-dir', str(out / 'dry' / name)]
            running.append((name, v, s, subprocess.Popen(cmd, stdout=so, stderr=se, env=env, cwd=str(out)), time.time(), so, se))
        time.sleep(0.5)
        for r in list(running):
            name, v, s, p, t, so, se = r
            if p.poll() is not None:
                so.close(); se.close(); running.remove(r)
                rec = {'name': name, 'driver': v, 'spec': str(s), 'expect': 'expect_ok', 'exit': p.returncode, 'seconds': round(time.time() - t, 2)}
                done.append(rec)
                print(json.dumps(rec), flush=True)
    with open(out / 'DRY_JOBS_BYTEID2.json', 'x') as f:
        json.dump({'jobs': done}, f, indent=1)


if __name__ == '__main__':
    main()
