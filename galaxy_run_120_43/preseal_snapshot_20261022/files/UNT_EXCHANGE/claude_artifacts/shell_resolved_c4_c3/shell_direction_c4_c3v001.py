"""Direction split of the same C4R3 gravity-only ring indicator (extension of shell_resolved_c4_c3v001, same inputs):
(a) vertical slabs |kz| in (0,1],(1,2],(2,3],(3,4] with all kx,ky; (b) in-plane max(|kx|,|ky|) slabs with all kz;
(c) the cube shell (3,4] split into V (|kz|>3 only), P (in-plane >3 only), B (both). Same Newtonian reference.
Read-only; numpy only; writes one JSON (exclusive)."""
import hashlib, json, math, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
MAIN = os.path.join(HERE, 'SHELL_RESOLVED_C4_C3V001.json'); WANT = '6637bdea7c6f3b96c547883854959e6eaf77d1f516a4941d58e2ffd7e357fe5d'
if hashlib.sha256(open(MAIN, 'rb').read()).hexdigest() != WANT: raise SystemExit('pin')
M = json.load(open(MAIN)); P = {k: v['path'] for k, v in M['pins'].items()}
for k, v in M['pins'].items():
    if k in ('final_packet', 'source_offset', 'gas07', 'gas17', 'unit_response') and hashlib.sha256(open(v['path'], 'rb').read()).hexdigest() != v['sha256']: raise SystemExit('pin ' + k)
C = 299792458.0; G = 6.67430e-11; C2 = C * C; KPC = 3.085677581491367e19; QINF = M['validation']['Qinf']
ids = list(M['rows']); radii = np.array([M['rows'][i]['R_kpc'] for i in ids]) * KPC; tau = {i: M['rows'][i]['tau_km_s'] for i in ids}; v4 = {i: M['rows'][i]['v_C4_km_s'] for i in ids}
with np.load(P['final_packet']) as z: k = z['wavevectors'].copy(); x0 = z['weighted_responses'][:, 0, 0].copy()
with np.load(P['unit_response']) as z: dk = z['dk_weights'].copy()
with np.load(P['source_offset']) as z: body0 = z['new_body_fourier_J'][:, 0, 0].copy()
with np.load(P['gas07']) as z: oldgas0 = z['old_body_gas_fourier_J'][:, 0, 0].copy()
with np.load(P['gas17']) as z: g17 = z['new_gas_fourier_J'][:, 0, 0].copy()
f0 = body0 - oldgas0 + g17; kn = np.sqrt(np.sum(k * k, axis=1)); nN = dk / (2 * math.pi) ** 3 * 4 * math.pi * G / (C ** 4 * kn ** 2) * f0 * QINF
ax = np.unique(k[:, 0]); n = len(ax); ia = np.searchsorted(ax, k[:, 0]); ib = np.searchsorted(ax, k[:, 1]); flat = ia * n + ib
kz = np.abs(k[:, 2]) * KPC; kp = np.maximum(np.abs(k[:, 0]), np.abs(k[:, 1])) * KPC
def plane(amp, m):
    return (np.bincount(flat[m], weights=amp[m].real, minlength=n * n) + 1j * np.bincount(flat[m], weights=amp[m].imag, minlength=n * n)).reshape(n, n)
nphi = 32; ph = 2 * np.pi * np.arange(nphi) / nphi
EX = [[(np.exp(1j * ax * R * math.cos(t)), np.exp(1j * ax * R * math.sin(t)), t) for t in ph] for R in radii]
def ring(Pm):
    vals = np.zeros((len(radii), nphi)); gs = np.zeros((len(radii), nphi))
    for i in range(len(radii)):
        for j, (ex, ey, t) in enumerate(EX[i]):
            vals[i, j] = (ex @ Pm @ ey).real; gs[i, j] = ((1j * ax * ex) @ Pm @ ey * math.cos(t) + ex @ Pm @ (1j * ax * ey) * math.sin(t)).real
    return vals, gs
vA, _ = ring(plane(x0, np.ones(len(k), bool))); den = 1 + vA
def dv_tau(amp, m):
    _, gs = ring(plane(amp, m)); g0 = C2 * np.mean(gs / den, axis=1)
    return {i: float(radii[a] * g0[a] / (2 * v4[i] * 1e3) / 1e3 / tau[i]) for a, i in enumerate(ids)}
sl = [(0, 1), (1, 2), (2, 3), (3, 4)]
out = {'schema': 'SHELL_DIRECTION_C4_C3V001', 'main_sha256': WANT, 'vertical_slabs': {}, 'inplane_slabs': {}, 'cube34_split': {}}
for lo, hi in sl:
    m = (kz > lo) & (kz <= hi); out['vertical_slabs']['%d-%d' % (lo, hi)] = {'actual': dv_tau(x0, m), 'Qinf_newton': dv_tau(nN, m)}
    m = (kp > lo) & (kp <= hi); out['inplane_slabs']['%d-%d' % (lo, hi)] = {'actual': dv_tau(x0, m), 'Qinf_newton': dv_tau(nN, m)}
c34 = np.maximum(kp, kz)
for nm, m in (('V_kz_only', (kz > 3) & (kp <= 3)), ('P_inplane_only', (kp > 3) & (kz <= 3)), ('B_both', (kz > 3) & (kp > 3))):
    m = m & (c34 <= 4); out['cube34_split'][nm] = {'actual': dv_tau(x0, m), 'Qinf_newton': dv_tau(nN, m), 'n_nodes': int(m.sum())}
# source vertical form factor along kz at the smallest in-plane |k| nodes
small = (np.abs(k[:, 0]) == ax[ax > 0].min()) & (np.abs(k[:, 1]) == ax[ax > 0].min())
prof = sorted((float(a), float(b)) for a, b in zip(kz[small], np.abs(f0[small])))
out['source_kz_profile_at_min_kperp'] = prof
with open(os.path.join(HERE, 'SHELL_DIRECTION_C4_C3V001.json'), 'x') as fh: json.dump(out, fh, indent=1)
def line(d): return ' '.join('%+7.2f' % d[i] for i in ids)
print('rows                     ', ' '.join('%7s' % i[-2:] for i in ids))
for key in ('vertical_slabs', 'inplane_slabs'):
    for s, v in out[key].items(): print('%-8s %-5s actual   ' % (key[:8], s), line(v['actual'])); print('%-8s %-5s Qinf*N   ' % (key[:8], s), line(v['Qinf_newton']))
for s, v in out['cube34_split'].items(): print('cube34 %-15s act' % s, line(v['actual'])); print('cube34 %-15s QN ' % s, line(v['Qinf_newton']))
pz = {}
for a, b in prof: pz.setdefault(round(a, 6), []).append(b)
print('source |f0| vs |kz| (min kperp):', ' '.join('%.2f:%.3g' % (a, np.mean(b)) for a, b in sorted(pz.items()) if a > 0.5))
