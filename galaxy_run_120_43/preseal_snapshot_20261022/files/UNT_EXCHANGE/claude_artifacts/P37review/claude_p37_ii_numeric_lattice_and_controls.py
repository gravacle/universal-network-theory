"""Claude-authored numerical checks for P-37 claim (ii). numpy only; no Codex code imported or executed.
 1. Diamond-lattice Gaussian Coulomb model (bond field E, ice/Gauss law at A and B sites, energy U_b/2 sum E^2):
    exact static response of the cell polarization e = sum_a sigma_a E_a  ->  (4/U_b) Pi_T(k) as k -> 0
    (U_e = U_b/4 per cell for |e|^2 normalisation), direction-dependent k->0 limit, and the lattice Ward witness
    ratio  (K G)_(12),xi=e3 / [2 lam^2 k1 k2 k3 /(U_e k^2)] -> 1.
 2. Quantum oscillator (one transverse photon mode): Kubo-Mori static susceptibility of e is 1/U at every beta,
    while the equal-time covariance is (1/2)sqrt(K/U)|k|-type (so covariance != static response).
 3. CR rotational family (a,b,c,d) least-squares fit to chi_lin at |k|=1: residual stays O(1).
 4. Linearized Einstein (Claude P-33 ward10 harness) + s*chi_lin: Ward violation and nullity vs s.
 5. Null-count control: hypothetical extra matchings (A1 trace e^2, T2 offdiagonal e_i e_j) give nullity 4 with
    null space = the four temporal coordinates, while the Ward residue persists (spurious 4-null pass).
"""
import numpy as np, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "P33"))
import ward10_crosscheck as w10            # Claude-authored P-33 harness
OUT = os.path.join(HERE, "claude_p37_ii_numeric_lattice_and_controls_results.json")
res = {}
SIG = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]], float)
IDX = [(0,0),(0,1),(0,2),(0,3),(1,1),(2,2),(3,3),(1,2),(1,3),(2,3)]
L = np.zeros((3, 10)); L[0, 9] = L[1, 8] = L[2, 7] = 1.0
def Pi(k): k = np.asarray(k, float); return np.eye(3) - np.outer(k, k)/(k@k)
def chi_lin(k, lam=1.0, U=1.0): return lam**2/U * L.T @ Pi(k) @ L
def G_static(k):
    p = np.r_[0.0, k]; return np.array([[p[m]*(n == c) + p[n]*(m == c) for c in range(4)] for m, n in IDX], float)

# ---------- 1. diamond lattice ----------
def lattice_chi(k, Ub=1.0, which="A"):
    k = np.asarray(k, float); ph = np.exp(1j*(SIG @ k)/8)        # bond-centre phases
    D = np.vstack([ph, np.conj(ph)])                                # Gauss law at A and at B (Bloch)
    P = np.eye(4) - np.linalg.pinv(D) @ D                          # projector on divergence-free bond space
    MA = (SIG.T * ph); MB = (SIG.T * np.conj(ph))
    M = MA if which == "A" else 0.5*(MA + MB)
    return (M @ P @ M.conj().T)/Ub
lat = {}
Ub = 1.0; Ue = Ub/4
for name, d in (("[1,2,3]", [1, 2, 3]), ("[3,-1,2]", [3, -1, 2]), ("[1,1,1]", [1, 1, 1]), ("[1,0.3,-0.7]", [1, .3, -.7])):
    d = np.array(d, float); d /= np.linalg.norm(d); rows = []
    for q in (0.4, 0.1, 0.025, 0.00625):
        k = q*d
        for which in ("A", "AB"):
            X = lattice_chi(k, Ub, which)
            dev = np.abs(X - Pi(k)/Ue).max()
            # lattice Ward witness: K = -lam^2 * L^T X L (lam=1); row h12 (index 7), xi = e3 (column 3)
            K = -(L.T @ X @ L); Wd = (K @ G_static(k))[7, 3]
            formula = 2*k[0]*k[1]*k[2]/(Ue*(k@k))
            rows.append(dict(q=q, which=which, max_abs_dev_from_Pi_over_Ue=float(dev),
                             ward_ratio=complex(Wd/formula) if abs(formula) > 1e-14 else None))
    lat[name] = rows
# k = 0 exactly on the lattice: three divergence-free modes (uniform flux sectors) -> chi = I/Ue (excluded mode)
X0 = lattice_chi([0, 0, 0], Ub, "A")
lat["k=0_exact"] = dict(chi_times_Ue=np.round((X0*Ue).real, 12).tolist(),
                        note="k=0 flux sector: full identity, not Pi_T; the k->0 limit is direction dependent")
res["1_diamond_lattice"] = lat

# ---------- 2. quantum oscillator: Kubo-Mori static susceptibility vs equal-time covariance ----------
def oscillator(U, Kk, beta, nmax=160):
    m = 1.0/U; Om = np.sqrt(U*Kk)
    a = np.diag(np.sqrt(np.arange(1, nmax)), 1)
    p = 1j*np.sqrt(m*Om/2)*(a.conj().T - a)
    E = Om*(np.arange(nmax) + 0.5); rho = np.exp(-beta*(E - E[0])); rho /= rho.sum()
    pm = np.abs(p)**2; KM = 0.0
    for i in range(nmax):
        for j in range(nmax):
            if i != j and pm[i, j] > 0: KM += pm[i, j]*(rho[i] - rho[j])/(E[j] - E[i])
    eqt = float(np.real(np.sum(rho*np.diag(p @ p))))
    return KM, eqt
osc = []
for (U, Kk, beta) in ((2.0, 0.5, 50.0), (2.0, 0.5, 1.0), (0.3, 3.0, 20.0), (0.3, 0.03, 200.0)):
    KM, eqt = oscillator(U, Kk, beta)
    osc.append(dict(U=U, K=Kk, beta=beta, kubo_mori_static=KM, one_over_U=1/U, equal_time_cov=eqt,
                    T0_equal_time_formula=0.5*np.sqrt(Kk/U)))
res["2_quantum_oscillator"] = osc

# ---------- 3. CR family fit ----------
def cr_basis(k):
    k = np.asarray(k, float); k2 = k@k; out = []
    def ten(c):
        t = np.zeros((4, 4))
        for (i, j), v in zip(IDX, c): t[i, j] = t[j, i] = v
        return t[1:, 1:]
    E = [ten(np.eye(10)[A]) for A in range(10)]
    def bil(f): return np.array([[f(E[A], E[B]) for B in range(10)] for A in range(10)])
    out.append(bil(lambda h, g: k2*np.sum(h*g)))
    out.append(bil(lambda h, g: k2*np.trace(h)*np.trace(g)))
    out.append(bil(lambda h, g: (h@k)@(g@k)))
    out.append(bil(lambda h, g: np.trace(h)*(k@g@k) + np.trace(g)*(k@h@k)))
    return out
rng = np.random.default_rng(5)
Arows, brows = [], []
for _ in range(40):
    k = rng.normal(size=3); k /= np.linalg.norm(k)
    B = cr_basis(k); Arows.append(np.stack([b.ravel() for b in B], 1)); brows.append(chi_lin(k).ravel())
A = np.vstack(Arows); bvec = np.concatenate(brows)
coef, *_ = np.linalg.lstsq(A, bvec, rcond=None)
res["3_CR_fit_unit_k"] = dict(best_abcd=coef.tolist(), relative_residual=float(np.linalg.norm(A@coef - bvec)/np.linalg.norm(bvec)))

# ---------- 4. Einstein (FP) + s*chi_lin ----------
ein = []
for s in (0.0, 1e-3, 1.0):
    worst = 0.0; nulls = set()
    for _ in range(50):
        k = rng.normal(size=3); p = np.r_[0.0, k]
        K = w10.K_coord(p) - s*chi_lin(k)
        R = K @ G_static(k); worst = max(worst, np.abs(R).max())
        sv = np.linalg.svd(K, compute_uv=False); nulls.add(int(np.sum(sv < 1e-9*sv.max())))
    ein.append(dict(s=s, max_static_ward_residual=float(worst), nullities=sorted(nulls)))
res["4_einstein_plus_chi_lin"] = ein

# ---------- 5. spurious exactly-4-null control ----------
ctl = []
for _ in range(20):
    k = rng.normal(size=3)
    K = -chi_lin(k)
    Tq = np.eye(3) - 1/3
    K[4:7, 4:7] -= 0.7*Tq                       # declared diagonal-traceless block (Codex)
    K[4:7, 4:7] -= 0.2*np.ones((3, 3))/3        # hypothetical A1 trace matching  tr j * e^2
    K[7:10, 7:10] -= 0.3*np.eye(3)              # hypothetical T2 offdiagonal quadratic matching
    sv = np.linalg.svd(K, compute_uv=False); null = int(np.sum(sv < 1e-9*sv.max()))
    _, _, Vt = np.linalg.svd(K); N = Vt[-null:].T
    temporal_frac = float(np.linalg.norm(N[:4])**2/null)
    Gs = G_static(k); Q, _ = np.linalg.qr(Gs)
    cap = int(np.sum(np.linalg.svd(N.T @ Q, compute_uv=False) > 1 - 1e-9))
    ctl.append(dict(nullity=null, null_space_weight_on_temporal=temporal_frac, dim_null_cap_gauge=cap,
                    ward_residual_max=float(np.abs(K @ Gs).max())))
res["5_spurious_4null_control"] = dict(nullities=sorted({c["nullity"] for c in ctl}),
    temporal_weight=sorted({round(c["null_space_weight_on_temporal"], 12) for c in ctl}),
    dim_null_cap_gauge=sorted({c["dim_null_cap_gauge"] for c in ctl}),
    min_ward_residual=min(c["ward_residual_max"] for c in ctl))

with open(OUT, "w") as f: json.dump(res, f, indent=1, default=str)
print(json.dumps(res, indent=1, default=str))
