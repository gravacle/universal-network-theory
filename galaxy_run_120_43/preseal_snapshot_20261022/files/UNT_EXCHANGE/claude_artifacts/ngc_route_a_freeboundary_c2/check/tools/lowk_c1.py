"""CHECKER: (1) small-|k| scaling of the iteration-0 lapse amplitude A_0(k)=weighted_response/dk_weight;
(2) G80C cube quadrature error on an analytically known long-range kernel (Gaussian-smoothed point
mass, symbol 4*pi*exp(-k^2 a^2/2)/k^2 -> potential erf(r/(a sqrt2))/r), using the run's own node set.
Diagnostics only."""
import json, math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
import replay_c1 as C

OUT = Path(__file__).resolve().parent.parent/'out'
ctx = C.Ctx(); ni = ctx.caller['numerical_controls']; spec = ni['composite_grid_spec']; kpc = ni['kpc_m']
parts = []; wparts = []
for lo, hi, n in zip(spec['breaks_inverse_kpc'][:-1], spec['breaks_inverse_kpc'][1:], spec['panel_orders']):
    gx, gw = np.polynomial.legendre.leggauss(n)
    parts.append(((lo+hi)/2+(hi-lo)*gx/2)/kpc); wparts.append((hi-lo)*gw/(2*kpc))
ax = np.concatenate(parts); aw = np.concatenate(wparts)
waves = np.array([(x, y, z) for x in ax for y in ax for z in ax]); dkw = np.array([a*b*c for a in aw for b in aw for c in aw])
k = ctx.prepared['wavevectors']
rep = {'wavevectors_equal_rebuilt_G80C': bool(np.array_equal(k, waves))}
A = ctx.prepared['weighted_responses'][:, 0, 0]/dkw  # lapse component amplitude per unit d^3k
kk = np.linalg.norm(k, axis=1)*kpc
order = np.argsort(kk)
rows = []
for j in order[:40:4].tolist()+order[200:4000:400].tolist():
    rows.append({'|k|_inv_kpc': float(kk[j]), 'Re_A': float(A[j].real), 'Im_A': float(A[j].imag),
                 'Re_A_times_k2': float(A[j].real*kk[j]**2)})
rep['lowk_amplitude'] = rows
# total-weighted low-k content: contribution of |k|<0.03 shell to deltan at origin
for lo, hi in ((0, 0.01), (0, 0.03), (0.03, 0.1), (0.1, 0.3), (0.3, 2.1)):
    m = (kk >= lo) & (kk < hi)
    rep['delta_n_origin_shell_%g_%g' % (lo, hi)] = float((ctx.prepared['weighted_responses'][m, 0, 0].sum()/(2*math.pi)**3).real) if False else float(ctx.prepared['weighted_responses'][m, 0, 0].sum().real)
# (2) analytic test: f(k)=4pi exp(-k^2 a^2/2)/k^2 ; phi(r)=(2pi)^-3 int f e^{ikx} d^3k = erf(r/(a*sqrt2))/r
res = {}
kp = waves*kpc  # in 1/kpc
k2 = (kp**2).sum(1); w = dkw*kpc**3
for a in (5.0, 10.0, 20.0):
    f = 4*math.pi*np.exp(-k2*a*a/2)/k2*w/(2*math.pi)**3
    R = 52.655
    def quad(x, y, z):
        return float((f*np.cos(kp[:, 0]*x+kp[:, 1]*y+kp[:, 2]*z)).sum())
    def exact(x, y, z):
        r = math.sqrt(x*x+y*y+z*z); return math.erf(r/(a*math.sqrt(2)))/r
    out = {}
    for z in (0, 10, 30, 60, 95, 136.5, 272.97, 500, 1000):
        q = quad(R, 0, z); e = exact(R, 0, z)
        out[str(z)] = {'quad': q, 'exact': e, 'rel_err': (q-e)/e}
    # vertical differences relative to midplane, as the HI solver uses
    q0 = out['0']['quad']; e0 = out['0']['exact']
    for z in (10, 30, 60, 95, 136.5, 272.97):
        dq = out[str(z)]['quad']-q0; de = out[str(z)]['exact']-e0
        out[str(z)]['diff_quad'] = dq; out[str(z)]['diff_exact'] = de; out[str(z)]['diff_rel_err'] = (dq-de)/de
    res['a=%g' % a] = out
rep['analytic_point_mass_test_R52.655'] = res
(OUT/'LOWK_C1.json').write_text(json.dumps(rep, indent=1))
print(json.dumps(rep, indent=1))
