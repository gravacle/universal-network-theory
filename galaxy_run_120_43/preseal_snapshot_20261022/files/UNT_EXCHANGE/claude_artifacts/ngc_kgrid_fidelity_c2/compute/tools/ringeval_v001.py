"""Operator ring reads (prereg C1, C4, R2, R3; gate V3 ring part): lnN of the candidate iteration-0 operator at
every roster column of rings [RS, RE), heights z in {0, +10, -10, +20, -20, +30, -30} kpc.
Metric point = checker replay_c1 Ctx.metric_point (solver c2v001:129-158 transcription) with Ctx.prepared replaced
by the candidate operator; lnN = log(N) (replay_c1 Ctx.lnN). The iteration-0 source is analytic-azimuth axisymmetric.
usage: ringeval_v001.py GRID LABEL RS RE
"""
import json, math, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import kg_lib_v001 as L

ZK = (0.0, 10.0, -10.0, 20.0, -20.0, 30.0, -30.0)


def main():
    cid, label, rs, re_ = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
    if not L.threads_env_ok():
        raise SystemExit('single-thread BLAS env required')
    d = L.OUT/'rings'/('%s_%s' % (cid, label)); d.mkdir(parents=True, exist_ok=True)
    out = d/('rings_%03d_%03d.json' % (rs, re_))
    if out.exists():
        raise SystemExit('exists')
    C, S, ctx = L.ctx_with(cid, label)
    cols = S.roster(ctx)
    t0 = time.process_time(); w0 = time.time()
    rows = []
    for o in range(rs, re_):
        ring = {'ordinal': o, 'first_index': 32*o, 'R_kpc': cols[32*o]['R_m']/C.KPC, 'lnN': []}
        for j in range(32):
            col = cols[32*o+j]; R = col['R_m']; phi = col['phi']
            ring['lnN'].append([ctx.lnN(R, phi, 0.0 if z == 0 else z*C.KPC) for z in ZK])
        rows.append(ring)
    rec = {'grid': cid, 'label': label, 'rings': [rs, re_], 'z_kpc': list(ZK), 'rows': rows,
           'cpu_s': time.process_time()-t0, 'wall_s': time.time()-w0, 'n_lines': 32*(re_-rs)}
    L.write_json(out, rec)
    print(cid, label, rs, re_, 'cpu', rec['cpu_s'])


if __name__ == '__main__':
    main()
