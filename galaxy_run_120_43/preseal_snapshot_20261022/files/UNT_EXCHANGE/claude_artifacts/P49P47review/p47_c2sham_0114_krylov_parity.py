"""Hidden-fragment probe beyond literal coordinate connectivity: is s1 in the cyclic
(Krylov) subspace K(s0)? Equivalent to: no eigenvalue at which s0 has BOTH U-even and
U-odd weight. Dense eigh of the U-even/U-odd blocks of the main coordinate fragment,
after the diagonal gauge that makes H real (phases 1). Manufactured parameters. Own code."""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from p47_c2sham_0114_model import params, U, sector_states, pc
from p47_c2sham_0114_sector_numeric import build, components, S0

P = params()
states = sector_states(); n = len(states)
idx, rows, cols, vals, closed = build(P, states)
th_k = np.angle(P['kappa'][0].c()); th_e = np.angle(P['epsilon_B'].c())
Ns = np.array([pc(s[5]) for s in states]); sec = np.array([s[0] for s in states])
W = np.exp(1j * (th_k * Ns + th_e * sec))
vg = np.conj(W[rows]) * vals * W[cols]
assert np.max(np.abs(vg.imag)) < 1e-14
vg = vg.real
roots = components(rows, cols, n)
i0 = idx[S0]; i1 = idx[U(S0)]
main = np.where(roots == roots[i0])[0]
pos = {int(k): i for i, k in enumerate(main)}
Uidx = np.array([idx[U(s)] for s in states])
# parity basis inside main fragment
even_vecs, odd_vecs, seen = [], [], set()
for k in main.tolist():
    if k in seen: continue
    u = int(Uidx[k]); seen.add(k); seen.add(u)
    if u == k:
        even_vecs.append(((k, 1.0),))
    else:
        r = 2 ** -0.5
        even_vecs.append(((k, r), (u, r))); odd_vecs.append(((k, r), (u, -r)))
m = len(main)
Hm = np.zeros((m, m))
for r_, c_, v in zip(rows.tolist(), cols.tolist(), vg.tolist()):
    if r_ in pos and c_ in pos:
        Hm[pos[r_], pos[c_]] += v
def basis_matrix(vecs):
    B = np.zeros((m, len(vecs)))
    for j, vv in enumerate(vecs):
        for k, a in vv: B[pos[k], j] = a
    return B
out = dict(main_fragment_size=m, n_even=len(even_vecs), n_odd=len(odd_vecs),
           symmetric_check=float(np.max(np.abs(Hm - Hm.T))))
s0v = np.zeros(m); s0v[pos[i0]] = 1.0
spec = {}
for name, vecs in (('even', even_vecs), ('odd', odd_vecs)):
    B = basis_matrix(vecs)
    Hb = B.T @ Hm @ B
    # parity block decoupling check
    E, V = np.linalg.eigh(Hb)
    c = V.T @ (B.T @ s0v)
    spec[name] = (E, np.abs(c) ** 2)
Bp = basis_matrix(even_vecs); Bm = basis_matrix(odd_vecs)
out['parity_blocks_decouple_maxabs'] = float(np.max(np.abs(Bp.T @ Hm @ Bm)))
tol_w = 1e-12
Ee, we = spec['even']; Eo, wo = spec['odd']
se = Ee[we > tol_w]; so = Eo[wo > tol_w]
out['even_supported_eigs'] = int(se.size); out['odd_supported_eigs'] = int(so.size)
out['weight_even'] = float(we.sum()); out['weight_odd'] = float(wo.sum())
# cluster supported eigenvalues within each parity (exact degeneracies) then cross-compare
d = np.min(np.abs(se[:, None] - so[None, :]))
out['min_cross_parity_gap_supported'] = float(d)
gaps = np.sort(np.abs(se[:, None] - so[None, :]).ravel())[:8]
out['smallest_8_cross_parity_gaps'] = [float(x) for x in gaps]
# within-parity exact-degeneracy spread (float resolution indicator)
de = np.diff(np.sort(se)); out['smallest_within_even_supported_spacings'] = [float(x) for x in np.sort(de)[:5]]
close = [(float(a), float(b)) for a in se for b in so if abs(a - b) < 1e-12]
out['cross_parity_coincidences_lt_1e-12'] = close[:20]
out['n_cross_coincidences'] = len(close)
# weight of rho_B in K(s0): (1 + ||P_K s1||^2)/2; with coincidences, at each shared E the
# s0 component a_e e_E + a_o o_E spans 1 dim; s1 component a_e e_E - a_o o_E.
if not close:
    out['TrP_K_rhoB'] = 'equal to 1 at float resolution: s1 in K(s0) (no supported cross-parity coincidence below 1e-12)'
if close:
    ws = []
    for a, b in close:
        pe = float(we[np.abs(Ee - a) < 1e-12].sum()); po = float(wo[np.abs(Eo - b) < 1e-12].sum())
        # in the 2D span, normalized s0 dir (sqrt(pe), sqrt(po)), s1 dir (sqrt(pe), -sqrt(po))
        ov = (pe - po) ** 2 / (pe + po)
        ws.append(dict(E=a, w_even=pe, w_odd=po, s1_overlap_in_K=ov, s1_missing=pe + po - ov))
    miss = sum(x['s1_missing'] for x in ws)
    out['s1_weight_outside_K_s0'] = miss
    out['TrP_K_rhoB'] = 1 - miss / 2
    out['coincidence_detail'] = ws[:10]
print(json.dumps(out, indent=1)[:4000])
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p47_c2sham_0114_krylov_parity_out.json'), 'w'), indent=1)
