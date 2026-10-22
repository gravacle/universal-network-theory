"""INFO diagnostic (NOT the prereg D-SPLIT, never a criterion): midplane lnN0 per ring on a tier-1 operator with the
nodes |k| > 2/kpc dropped (sphere mask of the D-SPLIT definition, applied here to a tier-1 grid because D-SPLIT's
Gf = finest evaluated isotropic grids requires tier-2, which is blocked). Same metric point as ringeval_v001.
usage: sphere_info_v001.py GRID LABEL RS RE
"""
import json, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
import kg_lib_v001 as L


def main():
    cid, label, rs, re_ = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
    if not L.threads_env_ok():
        raise SystemExit('single-thread BLAS env required')
    d = L.OUT/'sphere_info'/('%s_%s' % (cid, label)); d.mkdir(parents=True, exist_ok=True)
    out = d/('rings_%03d_%03d.json' % (rs, re_))
    if out.exists():
        raise SystemExit('exists')
    C, S, ctx = L.ctx_with(cid, label)
    k = ctx.prepared['wavevectors']; keep = np.linalg.norm(k, axis=1)*C.KPC <= 2.0
    ctx.prepared = {'wavevectors': k[keep], 'weighted_responses': ctx.prepared['weighted_responses'][keep]}
    ctx._k = None
    cols = S.roster(ctx); t0 = time.process_time()
    rows = []
    for o in range(rs, re_):
        rows.append({'ordinal': o, 'R_kpc': cols[32*o]['R_m']/C.KPC,
                     'lnN0': [ctx.lnN(cols[32*o+j]['R_m'], cols[32*o+j]['phi'], 0.0) for j in range(32)]})
    L.write_json(out, {'grid': cid, 'label': label, 'kept_nodes': int(keep.sum()), 'W': int(len(keep)), 'rows': rows,
                       'cpu_s': time.process_time()-t0, 'scope': 'INFO only; not D-SPLIT; not a criterion'})
    print(cid, rs, re_, 'kept', int(keep.sum()))


if __name__ == '__main__':
    main()
