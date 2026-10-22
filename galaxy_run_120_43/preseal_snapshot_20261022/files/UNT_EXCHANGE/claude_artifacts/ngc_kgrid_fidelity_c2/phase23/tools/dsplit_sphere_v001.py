"""D-SPLIT input S_sph (prereg D_SPLIT_attribution_of_C1_failures): midplane lnN0 per acceptance ring on Gf with the
nodes |k| > 2/kpc dropped (sphere mask). Diagnostic input to D-SPLIT only; never a criterion, never adoption.
Arithmetic identical to compute/tools/sphere_info_v001.py (4f616b14): same mask expression, same metric point
(checker replay_c1 Ctx.lnN at z = 0 on the candidate iteration-0 operator with Ctx.prepared replaced by the masked
arrays). Differences: scope string names D-SPLIT (AGG_CHECK_V001 F5), the record carries grid and W of the full
operator (checked against the prereg candidate), writes under phase23/out/dsplit_sphere/, exclusive create.
Reads the operator from phase23/ops (H-OVR tier-2 preparation).
usage: dsplit_sphere_v001.py GRID LABEL RS RE
"""
import json, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_p23_v001 as P   # sha verification helpers and exclusive writer

def main():
    cid, label, rs, re_ = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
    rec = P.recorded()
    got = P.sha(P.CT/'kg_lib_v001.py')
    if rec.get('./tools/kg_lib_v001.py') != got:
        raise SystemExit('kg_lib sha mismatch')
    sys.path.insert(0, str(P.CT))
    import numpy as np
    import kg_lib_v001 as L
    L.OPS = P.P23/'ops'; L.OUT = P.P23/'out'
    if not L.threads_env_ok():
        raise SystemExit('single-thread BLAS env required')
    c = L.candidate(cid)
    if not c['isotropic_tensor']:
        raise SystemExit('D-SPLIT Gf must be an isotropic candidate')
    d = L.OUT/'dsplit_sphere'/('%s_%s' % (cid, label)); d.mkdir(parents=True, exist_ok=True)
    out = d/('rings_%03d_%03d.json' % (rs, re_))
    if out.exists():
        raise SystemExit('exists')
    C, S, ctx = L.ctx_with(cid, label)
    k = ctx.prepared['wavevectors']
    W = int(len(k))
    if W != c['wave_count_W']:
        raise SystemExit('W mismatch')
    keep = np.linalg.norm(k, axis=1)*C.KPC <= 2.0
    ctx.prepared = {'wavevectors': k[keep], 'weighted_responses': ctx.prepared['weighted_responses'][keep]}
    ctx._k = None
    cols = S.roster(ctx); t0 = time.process_time(); w0 = time.time()
    rows = []
    for o in range(rs, re_):
        rows.append({'ordinal': o, 'R_kpc': cols[32*o]['R_m']/C.KPC,
                     'lnN0': [ctx.lnN(cols[32*o+j]['R_m'], cols[32*o+j]['phi'], 0.0) for j in range(32)]})
    P.write_exclusive(out, {'grid': cid, 'label': label, 'kept_nodes': int(keep.sum()), 'W': W, 'rows': rows,
                            'cpu_s': time.process_time()-t0, 'wall_s': time.time()-w0,
                            'scope': 'D-SPLIT S_sph input (prereg D_SPLIT_attribution_of_C1_failures: Gf with nodes |k| > 2/kpc dropped); '
                                     'diagnostic only; never a criterion; never adoption'})
    print(cid, rs, re_, 'kept', int(keep.sum()))


if __name__ == '__main__':
    main()
