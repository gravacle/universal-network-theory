"""Guarded dry runs (simulate mode; no stage executed) for the kmax extension lane.
Usage: python3 -I -B run_dry_c2ext.py OUT_DIR   (OUT_DIR/dry and OUT_DIR/logs; targets must not exist)
Each job: python3 -I -B guard_c2ext.py LOG driver dry-run --spec S --report-dir R; nice 10, single-thread BLAS env,
<= 4 concurrent.  Jobs: (A) C5/C6 N8/N1 under c2v009; (B) c2v008 vs c2v009 on registered <=96-node specs (byte-identity);
(C) negative specs under c2v009 (must be refused) and the C5 spec under c2v008 (must be refused).  Writes DRY_JOBS.json."""
import json
import os
import subprocess
import sys
import time
from pathlib import Path

PY = '/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
EX = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
HERE = EX / 'kmax_prereg_v005_c2/extension_c5c6'
CL2 = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2')
GUARD = HERE / 'tools/guard_c2ext.py'
DRV = {'v008': EX / 'driver_v008_c2/galaxy_m0_forward_c2v008.py', 'v009': HERE / 'driver_v009/galaxy_m0_forward_c2v009.py'}
R3S = EX / 'kmax_prereg_v005_c2/d7_recovery_r3/specs_d7r3'
EXT = {k: HERE / 'specs' / ('CALL_KMAX_%sR3_A2F10_EXT_%s_M16_C2V009.json' % tuple(k.split('_'))) for k in ('C5_N8', 'C5_N1', 'C6_N8', 'C6_N1')}  # build 2: the M16 specs
BYTE_ID = {
    'A2F10_G2': CL2 / 'specs/CALL_A2_ANCHOR_F10_C2V001.json',
    'DECIDING_II_N8_G2': EX / 'driver_v008_c2/deciding/CALL_A2_ANCHOR_F10_ROUTE_A_PARALLEL_N8_C2V008.json',
    'ADMIT_PREFIX_G2': EX / 'ngc_route_impl_c2/binding/specs/CALL_REPRO_PINNED_ADMIT_PREFIX_C2V005.json',
    'C3R3_G3': R3S / 'CALL_KMAX_C3R3_A2F10_D7R3_C2V005.json',
    'C4R3_G4': R3S / 'CALL_KMAX_C4R3_A2F10_D7R3_C2V005.json',
    'RR3_GR': R3S / 'CALL_KMAX_RR3_A2F10_D7R3_C2V005.json',
    'S4R3_G4': R3S / 'CALL_KMAX_S4R3_A2F10_D7R3_C2V005.json',
    'Y3R3_G3': R3S / 'CALL_KMAX_Y3R3_A2F10_D7R3_C2V005.json',
}
NEG = HERE / 'specs/negative_b2'  # build 2 set (specs/negative = build-1 set, superseded)


def make_negatives():
    """Negative specs (each one leaf away from C5_N8 or C4R3), written once."""
    NEG.mkdir(exist_ok=True)
    c5 = json.loads(EXT['C5_N8'].read_text())
    c4 = json.loads((R3S / 'CALL_KMAX_C4R3_A2F10_D7R3_C2V005.json').read_text())
    out = {}

    def put(name, s):
        p = NEG / ('NEG_%s.json' % name)
        if not p.exists():
            with open(p, 'x') as f:
                f.write(json.dumps(s, indent=1, sort_keys=True) + '\n')
        out[name] = p
    s = json.loads(json.dumps(c5)); s['numerics']['composite_grid_spec']['panel_orders'] = [6] * 8 + [8, 4] + [6] * 8
    put('G5_ORDERS_NOT_DECLARED', s)
    s = json.loads(json.dumps(c5)); g = s['numerics']['composite_grid_spec']
    g['breaks_inverse_kpc'] = [-7, -6, -5, -4, -3] + g['breaks_inverse_kpc'][3:-3] + [3, 4, 5, 6, 7]; g['panel_orders'] = [6] * 22; g['total_axis_nodes'] = 132
    put('G7_132_NODES', s)
    s = json.loads(json.dumps(c5)); s['numerics']['route_a']['max_iterations'] = 0
    put('MAXIT_0', s)
    s = json.loads(json.dumps(c5)); s['numerics']['route_a']['max_iterations'] = 33
    put('MAXIT_33', s)
    s = json.loads(json.dumps(c5)); s['numerics']['route_a']['max_iterations'] = True
    put('MAXIT_BOOL', s)
    ap = json.loads(BYTE_ID['ADMIT_PREFIX_G2'].read_text())
    s = json.loads(json.dumps(ap)); s['numerics']['route_a'] = {'max_iterations': 8}
    put('POS_MAXIT8_ADMIT_PREFIX', s)   # = base seed value: seed reused, admission passes, plan as ADMIT_PREFIX_G2
    s = json.loads(json.dumps(ap)); s['numerics']['route_a'] = {'max_iterations': 9}
    put('MAXIT9_ADMIT_PREFIX', s)       # changes the seed: the admitted checkpoint's seed check must BLOCK
    return out


def main():
    out = Path(sys.argv[1]).resolve()
    (out / 'dry').mkdir(parents=True, exist_ok=True)
    (out / 'logs').mkdir(exist_ok=True)
    neg = make_negatives()
    jobs = []
    for k, s in EXT.items():
        jobs.append(('v009_' + k, 'v009', s, 'expect_ok'))
    for k, s in BYTE_ID.items():
        for v in ('v008', 'v009'):
            jobs.append(('%s_%s' % (v, k), v, s, 'expect_ok'))
    for k, s in neg.items():
        jobs.append(('v009_NEG_' + k, 'v009', s, 'expect_ok' if k.startswith('POS_') else 'expect_refused'))
    jobs.append(('v008_C5_N8', 'v008', EXT['C5_N8'], 'expect_refused'))
    env = {k: v for k, v in os.environ.items() if not k.startswith('PYTHON')}
    for k in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'BLIS_NUM_THREADS'):
        env[k] = '1'
    os.nice(10)
    pending, running, done = list(jobs), [], []
    while pending or running:
        while pending and len(running) < 4:
            name, v, s, exp = pending.pop(0)
            rd = out / 'dry' / name
            so = open(out / 'logs' / (name + '.stdout.txt'), 'x')
            se = open(out / 'logs' / (name + '.stderr.txt'), 'x')
            cmd = [PY, '-I', '-B', str(GUARD), str(out / 'logs' / (name + '.guard.json')), str(DRV[v]), 'dry-run', '--spec', str(s), '--report-dir', str(rd)]
            running.append((name, v, s, exp, subprocess.Popen(cmd, stdout=so, stderr=se, env=env, cwd=str(out)), time.time(), so, se))
        time.sleep(0.5)
        for r in list(running):
            name, v, s, exp, p, t, so, se = r
            if p.poll() is not None:
                so.close(); se.close()
                running.remove(r)
                rec = {'name': name, 'driver': v, 'spec': str(s), 'expect': exp, 'exit': p.returncode, 'seconds': round(time.time() - t, 2)}
                done.append(rec)
                print(json.dumps(rec), flush=True)
    with open(out / 'DRY_JOBS.json', 'x') as f:
        json.dump({'jobs': done, 'drivers': {k: str(v) for k, v in DRV.items()}}, f, indent=1)


if __name__ == '__main__':
    main()
