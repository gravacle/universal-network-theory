"""CHECKER: per-ring azimuthal spread of midplane lnN0 and of max vertical rise, from check/out sweep + completed
columns. Iteration-0 sources are analytic-azimuth axisymmetric (seed analytic_initial_azimuth=true, prep v001:288-296),
so any phi-variation is from the response/quadrature, not the source."""
import glob, json, sys, collections, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np, replay_c1 as C
H = Path(__file__).resolve().parent.parent
recs = {}
for f in glob.glob(str(H/'out/sweep_*_of_5.jsonl')):
    for l in open(f):
        r = json.loads(l); recs[r['i']] = r
ctx = C.Ctx(); import sweep_c1 as S
cols = S.roster(ctx)
out = {}
for ring0 in (0, 640, 1280, 1920, 2240, 2400, 2464, 2496, 2560, 2816, 3200, 3840, 4480, 4960):
    R = cols[ring0]['R_m']; v = [ctx.lnN(R, cols[ring0+j]['phi'], 0.0) for j in range(32)]
    out['%.3f' % (R/C.KPC)] = {'first_index': ring0, 'lnN0_mean': float(np.mean(v)), 'lnN0_min': float(min(v)), 'lnN0_max': float(max(v)),
                               'spread_over_threshold': float((max(v)-min(v))/C.threshold()),
                               'spread_over_abs_mean': float((max(v)-min(v))/abs(np.mean(v)))}
(H/'out/RING_PHI_C1.json').write_text(json.dumps(out, indent=1))
for k, v in out.items(): print(k, '%+.3e [%+.3e,%+.3e] spread/th=%.2f' % (v['lnN0_mean'], v['lnN0_min'], v['lnN0_max'], v['spread_over_threshold']))
