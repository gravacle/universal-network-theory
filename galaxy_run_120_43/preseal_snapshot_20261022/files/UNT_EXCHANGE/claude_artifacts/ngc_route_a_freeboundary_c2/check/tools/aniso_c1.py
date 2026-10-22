"""CHECKER: grid-induced azimuthal variation of an isotropic analytic kernel (exact field is phi-independent)
on the run's own G80C nodes; vertical difference [phi(R,phi,z)-phi(R,phi,0)] at z=30 kpc vs phi. Diagnostics only."""
import json, math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np, replay_c1 as C
ctx = C.Ctx(); kp = ctx.prepared['wavevectors']*C.KPC
spec = ctx.caller['numerical_controls']['composite_grid_spec']; kpc = ctx.caller['numerical_controls']['kpc_m']
aw = np.concatenate([(hi-lo)*np.polynomial.legendre.leggauss(n)[1]/2 for lo, hi, n in
                     zip(spec['breaks_inverse_kpc'][:-1], spec['breaks_inverse_kpc'][1:], spec['panel_orders'])])
w = np.einsum('i,j,k->ijk', aw, aw, aw).ravel()
k2 = (kp**2).sum(1); out = {}
for a in (3.0, 5.0, 10.0):
    f = 4*math.pi*np.exp(-k2*a*a/2)/k2*w/(2*math.pi)**3
    for R in (20.0, 46.0, 52.655, 80.0, 120.0):
        rows = []
        for j in range(9):
            phi = 2*math.pi*j/32
            x, y = R*math.cos(phi), R*math.sin(phi)
            q0 = float((f*np.cos(kp[:, 0]*x+kp[:, 1]*y)).sum()); q30 = float((f*np.cos(kp[:, 0]*x+kp[:, 1]*y+kp[:, 2]*30)).sum())
            rows.append(q30-q0)
        r0 = math.sqrt(R*R); r30 = math.sqrt(R*R+900)
        ex = math.erf(r30/(a*math.sqrt(2)))/r30-math.erf(r0/(a*math.sqrt(2)))/r0
        rows = np.array(rows)
        out['a=%g R=%g' % (a, R)] = {'exact_diff': ex, 'quad_min': float(rows.min()), 'quad_max': float(rows.max()),
                                     'phi_spread_over_exact': float((rows.max()-rows.min())/abs(ex)),
                                     'max_abs_rel_err': float(np.max(np.abs(rows-ex))/abs(ex))}
(Path(__file__).resolve().parent.parent/'out'/'ANISO_C1.json').write_text(json.dumps(out, indent=1))
for k, v in out.items(): print(k, '%.3e spread/exact=%.4f maxrelerr=%.4f' % (v['exact_diff'], v['phi_spread_over_exact'], v['max_abs_rel_err']))
