"""Claude-authored independent check of P-37 claim (ii) (formal Gaussian Coulomb shear response).
Exact rational / exact polynomial arithmetic only (fractions). No Codex code imported or executed.

Model (declared, formal):  H = (U/2) sum e_T^2 + (K/2)(curl a)^2 + lam * (L h) . e ,  Gauss law k.e = 0 (no charges),
L h = (h23, h13, h12) on ten coordinates (00,01,02,03,11,22,33,12,13,23) (actual offdiagonal entries).
Optional declared diagonal-traceless block  b * T  on (11,22,33),  T = I - 11^T/3.
Ward generator (P-32 V003 s8.2): G_(mu nu),c = p_mu delta_(nu c) + p_nu delta_(mu c), static p = (0,k1,k2,k3).

Checks:
 A. closed form of K G (K = -chi_lin) and its exact reduction modulo k^2 (non-polynomiality = nonzero remainder)
 B. ranks / nullities / null-space content at random rational k; overlap of null space with gauge span
 C. joint local chart (h, e, phi) with Gauss multiplier phi: Schur complement = connected F_hh; the joint Ward
    system H [N; R] = 0 has NO solution (R any transformation of e, phi) whenever F_hh N != 0
 D. lawful Legendre chart (y = transverse polarization): Gamma_yy = U I2 (no nulls); Gamma_hh at fixed y = C;
    Moore-Penrose 'inverse' of chi_lin = (U/lam^2) L^T Pi L (same nullity 8) -- exact check
"""
from fractions import Fraction as F
import random, json, itertools, os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "claude_p37_ii_exact_ward_and_charts_results.json")
COORDS = ((0,0),(0,1),(0,2),(0,3),(1,1),(2,2),(3,3),(1,2),(1,3),(2,3))
LROW = {0: 9, 1: 8, 2: 7}          # e1 <-> h23, e2 <-> h13, e3 <-> h12

# ---------------- exact linear algebra ----------------
def zeros(n, m): return [[F(0)]*m for _ in range(n)]
def matmul(A, B): return [[sum((A[i][k]*B[k][j] for k in range(len(B))), F(0)) for j in range(len(B[0]))] for i in range(len(A))]
def T(A): return [list(r) for r in zip(*A)]
def rref(M):
    m = [r[:] for r in M]; piv = []; r = 0
    for c in range(len(m[0])):
        p = next((i for i in range(r, len(m)) if m[i][c] != 0), None)
        if p is None: continue
        m[r], m[p] = m[p], m[r]; v = m[r][c]; m[r] = [x/v for x in m[r]]
        for i in range(len(m)):
            if i != r and m[i][c] != 0:
                f = m[i][c]; m[i] = [x - f*y for x, y in zip(m[i], m[r])]
        piv.append(c); r += 1
        if r == len(m): break
    return m, piv
def rank(M): return len(rref(M)[1])
def nullspace(M):
    m, piv = rref(M); n = len(M[0]); free = [c for c in range(n) if c not in piv]; basis = []
    for f in free:
        v = [F(0)]*n; v[f] = F(1)
        for i, c in enumerate(piv): v[c] = -m[i][f]
        basis.append(v)
    return basis
def inv(M):
    n = len(M); A = [M[i][:] + [F(int(i == j)) for j in range(n)] for i in range(n)]
    R, piv = rref(A); assert piv[:n] == list(range(n)), "singular"
    return [r[n:] for r in R]

# ---------------- model blocks ----------------
def Lmat():
    L = zeros(3, 10)
    for i in range(3): L[i][LROW[i]] = F(1)
    return L
def Pi(k):
    k2 = sum(x*x for x in k); return [[F(int(i == j)) - k[i]*k[j]/k2 for j in range(3)] for i in range(3)]
def chi_lin(k, lam, U):
    L = Lmat(); return [[lam*lam/U*x for x in r] for r in matmul(matmul(T(L), Pi(k)), L)]
def chi_quad(b):
    C = zeros(10, 10)
    for i in range(3):
        for j in range(3): C[4+i][4+j] = b*(F(int(i == j)) - F(1, 3))
    return C
def G_static(k):
    p = [F(0)] + list(k)
    return [[p[mu]*F(int(nu == c)) + p[nu]*F(int(mu == c)) for c in range(4)] for mu, nu in COORDS]

# ---------------- exact polynomials in k1,k2,k3 (dict exponent->Fraction) ----------------
def padd(a, b, s=1):
    c = dict(a)
    for e, v in b.items(): c[e] = c.get(e, F(0)) + s*v
    return {e: v for e, v in c.items() if v != 0}
def pmul(a, b):
    c = {}
    for e1, v1 in a.items():
        for e2, v2 in b.items():
            e = tuple(x+y for x, y in zip(e1, e2)); c[e] = c.get(e, F(0)) + v1*v2
    return {e: v for e, v in c.items() if v != 0}
def var(i): e = [0, 0, 0]; e[i] = 1; return {tuple(e): F(1)}
def const(c): return {(0, 0, 0): F(c)} if c else {}
K2 = padd(padd(pmul(var(0), var(0)), pmul(var(1), var(1))), pmul(var(2), var(2)))
def reduce_mod_k2(p):
    """remainder of p modulo k1^2+k2^2+k3^2 (monic in k3): substitute k3^2 -> -(k1^2+k2^2) repeatedly"""
    p = dict(p)
    while True:
        hi = [e for e in p if e[2] >= 2]
        if not hi: return {e: v for e, v in p.items() if v != 0}
        e = hi[0]; v = p.pop(e)
        base = (e[0], e[1], e[2]-2)
        for sub, s in (((2, 0, 0), -1), ((0, 2, 0), -1)):
            ne = (base[0]+sub[0], base[1]+sub[1], base[2]); p[ne] = p.get(ne, F(0)) + s*v
        p = {x: y for x, y in p.items() if y != 0}
def pstr(p):
    if not p: return "0"
    return " + ".join(f"{v}*k1^{e[0]}k2^{e[1]}k3^{e[2]}" for e, v in sorted(p.items()))

results = {}

# ---------- A. symbolic Ward residue of K = -chi_lin (lam^2/U set to 1; it is an overall factor) ----------
# u(xi) = L G xi = (k2 xi3 + k3 xi2, k1 xi3 + k3 xi1, k1 xi2 + k2 xi1);  K G xi on rows (23,13,12) = -(u - k (k.u)/k^2)
# k^2 * residue = -(u k^2 - k (k.u))  ; polynomial part -u, nonpolynomial part k (k.u)/k^2
k = [var(0), var(1), var(2)]
resA = {}
for c in (1, 2, 3):                               # spatial gauge parameter xi = e_c
    xi = [const(int(c == j)) for j in (1, 2, 3)]
    u = [padd(pmul(k[1], xi[2]), pmul(k[2], xi[1])), padd(pmul(k[0], xi[2]), pmul(k[2], xi[0])), padd(pmul(k[0], xi[1]), pmul(k[1], xi[0]))]
    ku = {}
    for i in range(3): ku = padd(ku, pmul(k[i], u[i]))
    for i, rowname in zip(range(3), ("h23", "h13", "h12")):
        numer = padd(pmul(k[i], ku), pmul(u[i], K2), -1)     # k^2 * (K G)_row = k_i (k.u) - u_i k^2   [K=-chi, lam^2/U=1]
        rem = reduce_mod_k2(numer)
        resA[f"row {rowname}, xi=e{c}"] = dict(k2_times_residue=pstr(numer), remainder_mod_k2=pstr(rem),
                                              nonpolynomial=bool(rem))
results["A_symbolic_residue_rows_shear"] = resA
results["A_k_dot_LGxi"] = "k.(L G xi) = 2(k2 k3 xi1 + k1 k3 xi2 + k1 k2 xi3)  [bound-charge density created by a pure-gauge shear]"
# temporal gauge parameter xi = e0 at static p: G column has only h0i = k_i -> L G e0 = 0 -> zero residue
print("A. k^2*(K G) on shear rows, K=-chi_lin (lam^2/U=1); remainder mod k^2 nonzero => nonpolynomial:")
for key, v in resA.items(): print(f"   {key:18s} k2*res = {v['k2_times_residue']:40s} rem = {v['remainder_mod_k2']}")

# ---------- B. random rational k: exact closed-form agreement, ranks, null spaces ----------
rng = random.Random(20261012)
lam, U, b = F(7, 5), F(3, 11), F(5, 13)
statB = dict(cases=0, eq9_matches=0, nullity_lin=set(), nullity_lin_quad=set(),
             null_contains_temporal_trace_longshear=0, dim_null_cap_gauge=set(), ward_nonzero=0)
for _ in range(300):
    kk = [F(rng.randint(-9, 9), rng.randint(1, 5)) for _ in range(3)]
    if any(x == 0 for x in kk): continue
    k2 = sum(x*x for x in kk)
    Kl = [[-x for x in r] for r in chi_lin(kk, lam, U)]
    Kq = [[a - c for a, c in zip(r1, r2)] for r1, r2 in zip(Kl, chi_quad(b))]
    G = G_static(kk); W = matmul(Kl, G)
    statB["cases"] += 1
    if W[7][3] == 2*lam*lam/U*kk[0]*kk[1]*kk[2]/k2: statB["eq9_matches"] += 1
    if any(x != 0 for r in W for x in r): statB["ward_nonzero"] += 1
    statB["nullity_lin"].add(10 - rank(Kl)); statB["nullity_lin_quad"].add(10 - rank(Kq))
    # expected null vectors of Kq: h00, h01, h02, h03, trace (h11=h22=h33=1), longitudinal shear L^T k
    cand = []
    for a in range(4): v = [F(0)]*10; v[a] = F(1); cand.append(v)
    v = [F(0)]*10; v[4] = v[5] = v[6] = F(1); cand.append(v)
    v = [F(0)]*10; v[9], v[8], v[7] = kk[0], kk[1], kk[2]; cand.append(v)
    ok = all(all(x == 0 for x in matmul(Kq, [[y] for y in vv])[i]) for vv in cand for i in range(10))
    if ok and rank(cand) == 6: statB["null_contains_temporal_trace_longshear"] += 1
    # dimension of null(Kq) intersect range(G)
    Nb = nullspace(Kq); Gcols = T(G)
    dsum = rank(Nb + Gcols); statB["dim_null_cap_gauge"].add(len(Nb) + rank(Gcols) - dsum)
for key in ("nullity_lin", "nullity_lin_quad", "dim_null_cap_gauge"): statB[key] = sorted(statB[key])
results["B_random_rational_k"] = statB
print("B.", statB)

# ---------- C. joint local chart (h[10], e[3] unconstrained, phi[1] Gauss multiplier) ----------
# energy E = 1/2 h^T C h + U/2 |e|^2 + lam (L h).e + phi (k.e);  Hessian H (14x14), all entries polynomial in k
def joint(kk, Cm):
    L = Lmat(); H = zeros(14, 14)
    for i in range(10):
        for j in range(10): H[i][j] = Cm[i][j]
    for a in range(3):
        H[10+a][10+a] = U
        for j in range(10): H[10+a][j] = H[j][10+a] = lam*L[a][j]
        H[10+a][13] = H[13][10+a] = kk[a]
    return H
statC = dict(cases=0, schur_equals_C_minus_chi=0, joint_ward_unsolvable_spatial_xi=0, joint_ward_solvable_temporal_xi=0,
             required_Rphi_matches_minus_lam_kdotLN_over_k2=0)
for _ in range(60):
    kk = [F(rng.randint(-9, 9), rng.randint(1, 5)) for _ in range(3)]
    if any(x == 0 for x in kk): continue
    k2 = sum(x*x for x in kk)
    Cm = zeros(10, 10)                       # contact choice cycles: generic random / zero / completed square
    mode = statC["cases"] % 3
    if mode == 0:
        for i in range(10):
            for j in range(i, 10): Cm[i][j] = Cm[j][i] = F(rng.randint(-5, 5), rng.randint(1, 4))
    elif mode == 2:                          # C = (lam^2/U) L^T L : cancels the LOCAL part of chi_lin exactly
        Cm = [[lam*lam/U*x for x in r] for r in matmul(T(Lmat()), Lmat())]
    H = joint(kk, Cm); statC["cases"] += 1
    Hhh = [r[:10] for r in H[:10]]; Hhx = [r[10:] for r in H[:10]]; Hxx = [r[10:] for r in H[10:]]
    S = [[a - c for a, c in zip(r1, r2)] for r1, r2 in zip(Hhh, matmul(matmul(Hhx, inv(Hxx)), T(Hhx)))]
    target = [[a - c for a, c in zip(r1, r2)] for r1, r2 in zip(Cm, chi_lin(kk, lam, U))]
    if S == target: statC["schur_equals_C_minus_chi"] += 1
    G = G_static(kk)
    for c in range(4):
        N = [G[A][c] for A in range(10)]
        # unknowns R (4 = e1,e2,e3,phi):   H[:,10:] R = -H[:,:10] N   -> augmented rank test
        Ablk = [r[10:] for r in H]; rhs = [-sum(H[i][j]*N[j] for j in range(10)) for i in range(14)]
        solv = rank(Ablk) == rank([r + [v] for r, v in zip(Ablk, rhs)])
        FN = matmul(S, [[x] for x in N])
        if c == 0 and solv: statC["joint_ward_solvable_temporal_xi"] += 1
        if c == 0: statC.setdefault("temporal_solvable_by_contact_mode", {}).setdefault(["random","zero","completed_square"][mode], set()).add(solv)
        if c > 0: statC.setdefault("spatial_solvable_by_contact_mode", {}).setdefault(["random","zero","completed_square"][mode], set()).add(solv)
        if c > 0 and not solv and any(x[0] != 0 for x in FN): statC["joint_ward_unsolvable_spatial_xi"] += 1
        if c > 0:
            # with C chosen ad hoc to cancel F N exactly would require C N = chi N; check the forced R_phi
            LN = [N[LROW[i]] for i in range(3)]; kLN = sum(a*x for a, x in zip(kk, LN))
            # rows e: U R_e + k R_phi = -lam L N ; row phi: k.R_e = 0  =>  R_phi = -lam (k.LN)/k^2
            Rphi = -lam*kLN/k2; Re = [(-lam*LN[i] - kk[i]*Rphi)/U for i in range(3)]
            if sum(a*x for a, x in zip(kk, Re)) == 0: statC["required_Rphi_matches_minus_lam_kdotLN_over_k2"] += 1
for key in ("temporal_solvable_by_contact_mode", "spatial_solvable_by_contact_mode"):
    statC[key] = {m: sorted(v) for m, v in statC[key].items()}
results["C_joint_local_chart"] = statC
print("C.", statC)

# ---------- D. Legendre chart and Moore-Penrose comparison ----------
statD = dict(cases=0, pinv_equals_U_over_lam2_LtPiL=0, pinv_nullity=set(), Gamma_yy_eigs_positive=0)
for _ in range(40):
    kk = [F(rng.randint(-9, 9), rng.randint(1, 5)) for _ in range(3)]
    if any(x == 0 for x in kk): continue
    X = chi_lin(kk, lam, U)
    P = [[U/(lam*lam)*x for x in r] for r in matmul(matmul(T(Lmat()), Pi(kk)), Lmat())]
    XPX = matmul(matmul(X, P), X); PXP = matmul(matmul(P, X), P)
    sym1 = matmul(X, P); sym2 = matmul(P, X)
    mp = (XPX == X and PXP == P and sym1 == T(sym1) and sym2 == T(sym2))
    statD["cases"] += 1; statD["pinv_equals_U_over_lam2_LtPiL"] += int(mp); statD["pinv_nullity"].add(10 - rank(P))
    # transverse chart: y = E^T e, chi_yy = (1/U) I2  ->  Gamma_yy = U I2 (positive, no nulls) by construction;
    # verify on the shear block: chi restricted to range has eigenvalue lam^2/U twice (trace and rank)
    blk = [[X[i][j] for j in (9, 8, 7)] for i in (9, 8, 7)]
    tr = sum(blk[i][i] for i in range(3))
    if tr == 2*lam*lam/U and rank(blk) == 2: statD["Gamma_yy_eigs_positive"] += 1
statD["pinv_nullity"] = sorted(statD["pinv_nullity"])
results["D_legendre_and_pinv"] = statD
print("D.", statD)

with open(OUT, "w") as f: json.dump(results, f, indent=1, default=str)
print("wrote", OUT)
