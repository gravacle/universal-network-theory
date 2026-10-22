"""READ-ONLY verifier part 2 (not a run). Imports the v001 verifier's loaders by exec of its header only.

(a) All 2489 replayed columns (R, phi from the parallel replay's sweep shards; its default_95 ok flag is
    used only as a cross-check of my own evaluator): actual outcome reproduced?  Counterfactuals on the
    SAME quadrature/source for the 1808 failing columns: negative-T nodes zeroed; |k|<0.03 zeroed;
    |k|<0.1 replaced by 8.06*T_N; T=8.06*T_N everywhere.
(b) Quadrature fidelity with an ACTUAL-SHAPED isotropic symbol T_iso(|k|) = T along z (recomputed with
    the pinned modules), point mass at origin, vs a fine 1D radial integral.
"""
import json, math, sys
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
src = (HERE/'verify_lapse_v001.py').read_text()
head = src.split('# (1) independent recompute')[0]
exec(compile(head, 'verify_lapse_v001_header', 'exec'))   # loaders, arrays, T, kin, TN, W3 (own code)
OUT = Path(sys.argv[1])
A = np.array([[0., .5, .5], [.5, 0., .5], [.5, .5, 0.]])
with np.load('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/'
             'CRITICAL_PATH_EVALUATION_2026-10-17_V001/sampler_eval/CANDIDATE_4CHAIN_POOLED_GRID_V001.npz', allow_pickle=False) as z:
    grid = z['source_hessian_grid'].copy(); Cbar = z['background_C'].copy(); mubar = z['background_mu'].copy()
eig, vec = np.linalg.eigh(Cbar); root = np.einsum('ia,a,ja->ij', vec, np.sqrt(eig), vec, optimize=False)
def T_of(kv):
    kr = seed['ell_F_m']*np.einsum('ij,j->i', root, kv, optimize=False); kp = np.einsum('ji,j->i', A, kr, optimize=False)
    F = np.einsum('abc,abcij->ij', card.cardinal_weights(L=grid.shape[0], k_primitive=kp)['weights'], grid, optimize=False)
    b = cplx.bind_symbol(F_source_symbol=F, jbar=np.zeros(9), mubar=mubar, Cbar=Cbar, k_registered=kr, Eref=seed['Eref_J'], ell_F=seed['ell_F_m'],
                         gamma=seed['gamma'], static_binding_module=stat, relative_singular_floor=seed['relative_singular_floor'], hermitian_tolerance=seed['hermitian_tolerance'])
    ff = np.zeros((10, 1), complex); ff[0, 0] = 1.
    s = cplx.solve_symbol(bound=b, source_density_columns=ff, relative_singular_floor=seed['relative_singular_floor'],
                          full_residual_relative_tolerance=seed['solve_rtol'], full_residual_absolute_tolerance=seed['solve_atol'])
    return complex(s['fields'][0, 0]).real
Tr = T.real; neg = Tr < 0; fN = f[:, 0, 0]
kzu, grp = np.unique(k[:, 2], return_inverse=True)
def line_coeffs(amp, x, y):
    ph = np.exp(1j*(k[:, 0]*x+k[:, 1]*y))*amp
    return np.bincount(grp, ph.real, len(kzu))+1j*np.bincount(grp, ph.imag, len(kzu))
thr = math.log1p((5/3*11000.**2/(2/3))/C**2)
nst = 475; zs_plus = 0.2*kpc*np.arange(0, nst+1); zs = np.concatenate([zs_plus, -zs_plus[1:]])
E = np.exp(1j*np.outer(zs, kzu))
def outcome(L):
    lnN = np.log1p((E@L).real)
    lp = lnN[:nst+1]-lnN[0]; lm = np.concatenate([[0.], lnN[nst+1:]-lnN[0]])
    cp = np.flatnonzero(lp[1:] >= thr); cm = np.flatnonzero(lm[1:] >= thr)
    return (float((cp[0]+1)*0.2) if len(cp) else None, float((cm[0]+1)*0.2) if len(cm) else None)
variants = {
    'actual': wr[:, 0, 0],
    'negT_zeroed': np.where(neg, 0, wr[:, 0, 0]),
    'k_lt_0.03_zeroed': np.where(kin < 0.03, 0, wr[:, 0, 0]),
    'k_lt_0.1_set_8.06TN': np.where(kin < 0.1, W3*8.06*TN*fN, wr[:, 0, 0]),
    'all_8.06TN': W3*8.06*TN*fN,
}
rows = []
for p in sorted(Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_a_freeboundary_c2/replay/sweep').glob('shard_*_of_06.jsonl')):
    for line in p.read_text().splitlines():
        r = json.loads(line); rows.append(dict(ci=r['column_index'], R=r['R_kpc'], phi=r['phi'], az=r['azimuth'], mass=r['mass_kg'], ok_replay=r['default_95']['ok']))
rows.sort(key=lambda r: r['ci'])
agree = 0; tallies = {v: dict(confined_both=0, n=0, mass_confined=0.) for v in variants}
fail_rows = []
for r in rows:
    X, Y = r['R']*kpc*math.cos(r['phi']), r['R']*kpc*math.sin(r['phi'])
    o = outcome(line_coeffs(variants['actual'], X, Y))
    ok = o[0] is not None and o[1] is not None
    agree += int(ok == r['ok_replay'])
    if ok:
        continue
    rec = dict(ci=r['ci'], R=r['R'], az=r['az'], mass=r['mass'])
    for v, amp in variants.items():
        if v == 'actual':
            continue
        oo = outcome(line_coeffs(amp, X, Y)); okv = oo[0] is not None and oo[1] is not None
        tallies[v]['n'] += 1; tallies[v]['confined_both'] += int(okv); tallies[v]['mass_confined'] += r['mass']*okv
        rec[v] = oo
    fail_rows.append(rec)
res = dict(n_replayed=len(rows), my_ok_flag_agrees_with_replay=agree, n_fail_mine=len(fail_rows),
           fail_mass_kg=float(sum(r['mass'] for r in fail_rows)))
for v in tallies:
    if v != 'actual':
        tallies[v]['mass_fraction_of_failing_confined'] = tallies[v]['mass_confined']/res['fail_mass_kg']
res['counterfactual_tallies_on_failing_columns'] = {v: t for v, t in tallies.items() if v != 'actual'}
# azimuth pattern of failures
az = {}
for r in rows:
    pass
fr = {}
for r in fail_rows:
    fr.setdefault(r['az'], 0); fr[r['az']] += 1
tot = {}
for r in rows:
    tot.setdefault(r['az'], 0); tot[r['az']] += 1
res['fail_count_by_azimuth_index'] = {str(a): [fr.get(a, 0), tot[a]] for a in sorted(tot)}
still = [r for r in fail_rows if not (r['negT_zeroed'][0] is not None and r['negT_zeroed'][1] is not None)]
res['still_failing_with_negT_zeroed'] = dict(count=len(still), R_range=[min(r['R'] for r in still), max(r['R'] for r in still)] if still else None,
                                             by_az={str(a): sum(1 for r in still if r['az'] == a) for a in sorted(set(r['az'] for r in still))},
                                             head=still[:12])
still2 = [r for r in fail_rows if not (r['all_8.06TN'][0] is not None and r['all_8.06TN'][1] is not None)]
res['still_failing_with_all_8.06TN'] = dict(count=len(still2), head=still2[:12])

# (b) actual-shaped isotropic symbol quadrature test
kz1 = np.concatenate([np.geomspace(1e-4, 0.3, 300), np.linspace(0.3, 2.0, 200)[1:]])
Tz = np.array([T_of(np.array([0., 0., kk/kpc])) for kk in kz1])
Tiso = np.interp(np.log(kin), np.log(kz1), Tz)
M = 1.0e40; fpm = -M*C*C
res['Tiso_check'] = dict(T_at_1em4=float(Tz[0]), T_over_TN_at_2=float(Tz[-1]/(4*np.pi*G/(C**4*(2/kpc)**2))))
# fine 1D: dn(r) = 1/(2 pi^2 r) int_0^inf T(k) f k sin(k r) dk ; T beyond k=2 continued as T(2)*(2/k)^2
kf = np.linspace(1e-7, 2.0, 400001)/kpc
Tf = np.interp(np.log(np.maximum(kf*kpc, 1e-4)), np.log(kz1), Tz)
from math import pi
def exact_dn(r):
    integ = Tf*fpm*kf*np.sin(kf*r)
    main = np.trapezoid(integ, kf) if hasattr(np, 'trapezoid') else np.trapz(integ, kf)
    K = 2.0/kpc; Tk = Tz[-1]
    # tail: int_K^inf Tk K^2/k^2 * f * k sin(kr) dk = Tk K^2 f * int_K^inf sin(kr)/k dk = Tk K^2 f (pi/2 - Si(K r))
    x = K*r; t = np.linspace(0, x, 200001); si = np.trapezoid(np.sinc(t/np.pi), t) if hasattr(np, 'trapezoid') else np.trapz(np.sinc(t/np.pi), t)
    tail = Tk*K*K*fpm*(pi/2-si)
    return (main+tail)/(2*pi*pi*r)
pts = []
for (Rk, phik) in ((52.65530721571086, 7), (52.65530721571086, 0), (70., 0), (90., 7)):
    ph = 2*np.pi*phik/32; X, Y = Rk*kpc*math.cos(ph), Rk*kpc*math.sin(ph)
    Lq = line_coeffs(W3*Tiso*fpm, X, Y)
    for zk in (0., 1., 5., 10., 30., 60., 95.):
        q = float((np.exp(1j*kzu*zk*kpc)@Lq).real); ex = float(exact_dn(math.hypot(Rk, zk)*kpc))
        pts.append(dict(R_kpc=Rk, phi_index=phik, z_kpc=zk, quad=q, exact_1d=ex))
    base_q = pts[-7]['quad']; base_e = pts[-7]['exact_1d']
    for p in pts[-7:]:
        p['quad_rise'] = p['quad']-base_q; p['exact_rise'] = p['exact_1d']-base_e
res['actual_shaped_point_mass_quadrature_test'] = pts
OUT.write_text(json.dumps(res, indent=1, allow_nan=False, default=lambda o: None))
print(json.dumps({k: v for k, v in res.items() if k != 'actual_shaped_point_mass_quadrature_test'}, indent=1)[:6000])
for p in pts:
    print(p)
