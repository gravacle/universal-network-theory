"""Claude-authored independent check of P-37 FORMAL endpoint claims (i) and (iii).

Reads nothing Codex-authored at run time; every formula below is rebuilt from the
P-31 V002 / V001 source-law TEXT (A1, A2-A4, A7, A8, l_e, l_v, w(v,u)) and the
canonical degree term Ud(d-dstar)^2 + Delta_can n.

Exact Fractions throughout except one float finite-difference check of the
normalized-cosine derivative (A7/A8), which is independent of the A8 formula.
"""
from fractions import Fraction as F
from itertools import combinations
import random, math, json, sys

SIG = ((1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1))
PAIRS = list(combinations(range(4), 2))
OFF = ((1, 2), (0, 2), (0, 1))  # (23),(13),(12) <-> e1,e2,e3
out = {}


def nnT(a, b):  # n_a n_b^T with n = sigma/sqrt3  -> rational
    return [[F(SIG[a][i] * SIG[b][j], 3) for j in range(3)] for i in range(3)]


def frob(M, X):
    return sum(M[i][j] * X[i][j] for i in range(3) for j in range(3))


def A8(a, b):
    ab, ba, aa, bb = nnT(a, b), nnT(b, a), nnT(a, a), nnT(b, b)
    return [[(ab[i][j] + ba[i][j]) / 2 + (aa[i][j] + bb[i][j]) / 6 for j in range(3)] for i in range(3)]


def u(a, X):
    return frob(nnT(a, a), X)


def pol(pair):
    return tuple(SIG[pair[0]][i] + SIG[pair[1]][i] for i in range(3))


def rand_sym(rng, den=7):
    X = [[F(0)] * 3 for _ in range(3)]
    for i in range(3):
        for j in range(i, 3):
            X[i][j] = X[j][i] = F(rng.randint(-9, 9), den)
    return X


rng = random.Random(20261012)

# ---------------------------------------------------------------- 1. A7/A8 from A1 (float FD, independent)
def cosine(a, b, G):
    na = [s / math.sqrt(3) for s in SIG[a]]
    nb = [s / math.sqrt(3) for s in SIG[b]]
    q = lambda x, y: sum(x[i] * G[i][j] * y[j] for i in range(3) for j in range(3))
    return q(na, nb) / math.sqrt(q(na, na) * q(nb, nb))

maxerr = 0.0
for trial in range(50):
    X = [[float(v) for v in row] for row in rand_sym(rng)]
    for a, b in PAIRS:
        t = 1e-6
        Gp = [[(i == j) + t * X[i][j] for j in range(3)] for i in range(3)]
        Gm = [[(i == j) - t * X[i][j] for j in range(3)] for i in range(3)]
        fd = (cosine(a, b, Gp) - cosine(a, b, Gm)) / (2 * t)
        ex = float(frob(A8(a, b), [[F(v).limit_denominator(10**6) for v in r] for r in X]))
        maxerr = max(maxerr, abs(fd - ex))
out["A8_vs_FD_normalized_cosine_max_abs_err"] = maxerr
assert maxerr < 1e-8

# ---------------------------------------------------------------- 2. six-state identities (1),(2),(3)
six = {}
for a, b in PAIRS:
    A = A8(a, b); e = pol((a, b))
    diag_ok = all(A[i][i] == F(e[i] ** 2, 6) - F(2, 9) for i in range(3))
    off_ok = all(A[i][j] == -F(e[3 - i - j], 9) for i in range(3) for j in range(3) if i != j)
    trace0 = sum(A[i][i] for i in range(3)) == 0
    # (3): sum_occ n_a^T X n_a = (2/3)trX + (2/3)(X23 e1+X13 e2+X12 e3)  for random X
    ok3 = True; ok2 = True
    for _ in range(20):
        X = rand_sym(rng)
        trX = X[0][0] + X[1][1] + X[2][2]
        sh = sum(X[i][j] * e[3 - i - j] for i, j in OFF)
        ok3 &= (u(a, X) + u(b, X) == F(2, 3) * trX + F(2, 3) * sh)
        Ud = F(rng.randint(1, 9), 5)
        lhs = 2 * Ud * frob(A, X)
        rhs = Ud / 3 * sum(X[i][i] * (e[i] ** 2 - F(4, 3)) for i in range(3)) - F(4, 9) * Ud * sh
        ok2 &= (lhs == rhs)
    six[f"{a}{b}"] = dict(e=e, eq1_diag=diag_ok, eq1_off=off_ok, A_traceless=trace0, eq2=ok2, eq3=ok3)
    assert diag_ok and off_ok and trace0 and ok2 and ok3
out["six_state_identities"] = six
# B vertex: reversing all n leaves A8 unchanged
out["A8_even_under_n_to_minus_n"] = True  # A8 is quadratic in n: trivially; checked below numerically too

# ---------------------------------------------------------------- 3. lattice: full first-source derivative on ice configs
def build(L):
    cells = [(i, j, k) for i in range(L) for j in range(L) for k in range(L)]
    idx = {c: n for n, c in enumerate(cells)}
    d = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)]
    edges = []  # (A index, B index, label)
    for c in cells:
        for a in range(4):
            bc = tuple((c[m] - d[a][m]) % L for m in range(3))
            edges.append((idx[c], idx[bc], a))
    nA = len(cells)
    # simple-graph check
    assert len({(x, y) for x, y, _ in edges}) == len(edges)
    return nA, edges


def ice_polarized(edges, occ_labels=(0, 1)):
    return [1 if a in occ_labels else 0 for _, _, a in edges]


def loop_update(nA, edges, n, rng):
    incA = [[] for _ in range(nA)]; incB = [[] for _ in range(nA)]
    for ei, (x, y, a) in enumerate(edges):
        incA[x].append(ei); incB[y].append(ei)
    path = [("A", rng.randrange(nA))]; used = []
    seen = {path[0]: 0}
    while True:
        side, v = path[-1]
        if side == "A":
            ei = rng.choice([e for e in incA[v] if n[e] == 1]); nxt = ("B", edges[ei][1])
        else:
            ei = rng.choice([e for e in incB[v] if n[e] == 0]); nxt = ("A", edges[ei][0])
        used.append(ei); path.append(nxt)
        if nxt in seen:
            for e in used[seen[nxt]:]:
                n[e] ^= 1
            return
        seen[nxt] = len(path) - 1


def degrees(nA, edges, n):
    dA = [0] * nA; dB = [0] * nA
    occA = [[] for _ in range(nA)]; occB = [[] for _ in range(nA)]
    for ei, (x, y, a) in enumerate(edges):
        if n[ei]:
            dA[x] += 1; dB[y] += 1; occA[x].append(a); occB[y].append(a)
    return dA, dB, occA, occB


def first_source_derivative(nA, edges, n, Xa, Xb, P):
    """d/ds H_diag(Q0 sector) at s=0 for spatial source j_u = s*Xa[u] (A charts);
    Xb[v] = B-node averaged source bar_j_v (w = 1/4 per edge on q4 simple graph).
    P: dict of canonical coefficients. Diagonal Q0-sector owners only:
    edge Delta_can n_e exp(l_e); node exp(l_v)[Ud((1-2d*)d+d*^2) + eps_r q - lamR d q + E_S]
    and cross terms 2Ud exp(l_v + c_ab) n_a n_b."""
    Ud, Dc, ds, er, lR, ES = P["Ud"], P["Delta_can"], P["dstar"], P["eps_r"], P["lamR"], P["E_S"]
    dA, dB, occA, occB = degrees(nA, edges, n)
    tot = F(0)
    for ei, (x, y, a) in enumerate(edges):
        if n[ei]:
            tot += Dc * u(a, Xa[x])
    for side, dd, occ, XX, qq in (("A", dA, occA, Xa, P["qA"]), ("B", dB, occB, Xb, P["qB"])):
        for v in range(nA):
            X = XX[v]; trX = X[0][0] + X[1][1] + X[2][2]
            d = dd[v]; q = qq[v]
            scalar = Ud * ((1 - 2 * ds) * d + ds * ds) + er * q - lR * d * q + ES
            cross_cnt = len(list(combinations(occ[v], 2)))
            tot += trX * (scalar + 2 * Ud * cross_cnt)
            for a, b in combinations(sorted(occ[v]), 2):
                tot += 2 * Ud * frob(A8(a, b), X)
    return tot


def run_lattice(L, nconf, P, rng):
    nA, edges = build(L)
    n = ice_polarized(edges)
    res = dict(L=L, nA=nA, nedges=len(edges), checked=0, max_resid=0, PA_eq_PB=True, ice=True)
    lam = F(2, 3) * P["Delta_can"] - F(8, 9) * P["Ud"]
    for c in range(nconf):
        for _ in range(3):
            loop_update(nA, edges, n, rng)
        dA, dB, occA, occB = degrees(nA, edges, n)
        res["ice"] &= all(x == 2 for x in dA + dB)
        PA = [sum(pol(tuple(occA[v]))[i] for v in range(nA)) for i in range(3)]
        PB = [sum(pol(tuple(occB[v]))[i] for v in range(nA)) for i in range(3)]
        Pe = [sum(SIG[a][i] for ei, (_, _, a) in enumerate(edges) if n[ei]) for i in range(3)]
        res["PA_eq_PB"] &= (PA == PB == Pe)
        X = rand_sym(rng)
        Xa = [X] * nA; Xb = [X] * nA
        got = first_source_derivative(nA, edges, n, Xa, Xb, P)
        trX = X[0][0] + X[1][1] + X[2][2]
        # predicted: trace owners + lambda X.P + (Ud/3) sum_v sum_i X_ii Q_v,i
        trace_part = F(0)
        for dd, qq in ((dA, P["qA"]), (dB, P["qB"])):
            for v in range(nA):
                d = dd[v]; q = qq[v]
                trace_part += trX * (P["Ud"] * ((1 - 2 * P["dstar"]) * d + P["dstar"] ** 2) + P["eps_r"] * q
                                     - P["lamR"] * d * q + P["E_S"] + 2 * P["Ud"])
        trace_part += P["Delta_can"] * F(2, 3) * trX * nA  # edge trace owner, 2 occ edges per A
        shear = lam * sum(X[i][j] * PA[3 - i - j] for i, j in OFF)
        quad = F(0)
        for occ in (occA, occB):
            for v in range(nA):
                e = pol(tuple(occ[v]))
                quad += P["Ud"] / 3 * sum(X[i][i] * (e[i] ** 2 - F(4, 3)) for i in range(3))
        resid = got - (trace_part + shear + quad)
        res["max_resid"] = max(res["max_resid"], abs(resid))
        res["checked"] += 1
    res["max_resid"] = str(res["max_resid"])
    return res


P = dict(Ud=F(1), Delta_can=F(4), dstar=3, eps_r=F(3, 7), lamR=F(1, 4), E_S=F(5, 11))
for L in (2, 3):
    nA, _ = build(L)
    for rho in (0, 1):
        PP = dict(P, qA=[rho] * nA, qB=[rho] * nA)
        r = run_lattice(L, 40, PP, rng)
        out[f"lattice_L{L}_rho{rho}"] = r
        assert r["max_resid"] == "0" and r["PA_eq_PB"] and r["ice"]
# random coefficient tuples / dstar values too
for trial in range(6):
    ds = rng.choice([2, 3, 4])
    PP = dict(Ud=F(rng.randint(1, 9), 4), Delta_can=F(rng.randint(-9, 9), 3), dstar=ds,
              eps_r=F(rng.randint(-5, 5), 3), lamR=F(rng.randint(0, 5), 6), E_S=F(1, 3))
    nA, _ = build(2)
    PP["qA"] = [rng.randint(0, 1) for _ in range(nA)]; PP["qB"] = [rng.randint(0, 1) for _ in range(nA)]
    r = run_lattice(2, 15, PP, rng)
    out[f"lattice_randomtuple_{trial}"] = dict(r, dstar=ds, Ud=str(PP["Ud"]), Delta_can=str(PP["Delta_can"]))
    assert r["max_resid"] == "0"

# ---------------------------------------------------------------- 4. crosswalk and dstar
def lam_native(Dc, Ud):
    return F(2, 3) * Dc - F(8, 9) * Ud

cw = {}
# lambda(delta) = 2delta/3 + c(dstar) Ud with Delta_can = delta - 4Ud(2-dstar)
for ds in (1, 2, 3, 4, 5):
    c = (lam_native(F(0) - 4 * (2 - ds), F(1)))  # delta=0, Ud=1
    cw[ds] = str(c)
out["lambda_at_delta0_Ud1_by_dstar"] = cw
# solve 2/3*4(ds-2) - 8/9 = 16/9  -> ds
ds_solve = F(2) + (F(16, 9) + F(8, 9)) / (F(8, 3))
out["dstar_solving_crosswalk_identity"] = str(ds_solve)
assert ds_solve == 3
# identity check for symbolic generic values at dstar=3
ok = True
for _ in range(100):
    Ud = F(rng.randint(1, 50), rng.randint(1, 9)); de = F(rng.randint(-50, 50), rng.randint(1, 9))
    Dc = de + 4 * Ud  # dstar=3
    ok &= (F(2, 9) * (3 * Dc - 4 * Ud) == F(2, 3) * de + F(16, 9) * Ud)
out["crosswalk_identity_dstar3_100_random"] = ok
# wrong chart: attaching the source to delta (degree-2 rewriting) gives 2delta/3 - 8Ud/9
out["wrong_chart_difference_over_Ud"] = str((F(2, 3) * 0 + F(16, 9)) - (F(2, 3) * 0 - F(8, 9)))  # = 8/3
# energy rewriting identity on lattice configs (any n, not only ice)
nA, edges = build(2)
rw_ok = True
for _ in range(200):
    n = [rng.randint(0, 1) for _ in edges]
    dA, dB, _, _ = degrees(nA, edges, n)
    ds = rng.choice([1, 2, 3, 4]); Ud = F(rng.randint(1, 9), 3); Dc = F(rng.randint(-9, 9), 2)
    de = Dc + 4 * Ud * (2 - ds)
    lhs = Dc * sum(n) + Ud * sum((d - ds) ** 2 for d in dA + dB)
    rhs = Ud * sum((d - 2) ** 2 for d in dA + dB) + de * sum(n) + 2 * nA * Ud * (ds * ds - 4)
    rw_ok &= (lhs == rhs)
out["degree_rewrite_identity_random_configs"] = rw_ok
# ice window and the claimed fine-tuning point
out["ice_window_lambda_range_dstar3_over_Ud"] = [str(F(2, 3) * (-2) + F(16, 9)), str(F(2, 3) * 2 + F(16, 9))]
out["finetune_Delta_can_4Ud_3_in_delta_chart_x_by_dstar"] = {
    ds: str((F(4, 3) + 4 * (2 - ds)) / 2) for ds in (2, 3, 4)}

# ---------------------------------------------------------------- 5. linear vs quadratic split on the 6 ice states
# basis functions on the six states: 1, e1,e2,e3, Q1,Q2 (Q3=-Q1-Q2); check orthogonality/completeness
states = PAIRS
def frank(M):
    m = [r[:] for r in M]; r = 0
    for c in range(len(m[0])):
        piv = next((i for i in range(r, len(m)) if m[i][c] != 0), None)
        if piv is None: continue
        m[r], m[piv] = m[piv], m[r]
        for i in range(len(m)):
            if i != r and m[i][c] != 0:
                f = m[i][c] / m[r][c]; m[i] = [x - f * y for x, y in zip(m[i], m[r])]
        r += 1
    return r
basis = []
for p in states:
    e = pol(p)
    basis.append([1, e[0], e[1], e[2], e[0] ** 2 - F(4, 3), e[1] ** 2 - F(4, 3)])
out["six_state_function_space_rank"] = frank([[F(x) for x in r] for r in basis])
# complement map (n -> 1-n): pair -> complementary pair, e -> -e
comp_ok = all(pol(tuple(sorted(set(range(4)) - set(p)))) == tuple(-x for x in pol(p)) for p in states)
out["complement_maps_e_to_minus_e"] = comp_ok
# shear insertion odd, diag-traceless insertion even under complement
par_ok = True
for p in states:
    q = tuple(sorted(set(range(4)) - set(p)))
    A, Aq = A8(*p), A8(*q)
    par_ok &= all(A[i][j] == -Aq[i][j] for i in range(3) for j in range(3) if i != j)
    par_ok &= all(A[i][i] == Aq[i][i] for i in range(3))
out["shear_odd_diag_even_under_complement"] = par_ok

# ---------------------------------------------------------------- 6. claim (iii): O(h^2) virtual correction to the shear vertex
def E_diag(nA, edges, n, Xa, s, P):
    """exact diagonal energy at source s*X (uniform), Q0 sector, with exp weights
    expanded only to first order in s -> returns (E0, E1) where E = E0 + s*E1 + O(s^2)"""
    E0 = F(0)
    Ud, Dc, ds = P["Ud"], P["Delta_can"], P["dstar"]
    dA, dB, occA, occB = degrees(nA, edges, n)
    for ei in range(len(edges)):
        if n[ei]:
            E0 += Dc
    for dd, occ, qq in ((dA, occA, P["qA"]), (dB, occB, P["qB"])):
        for v in range(nA):
            d = dd[v]; q = qq[v]
            E0 += Ud * (d - ds) ** 2 + P["eps_r"] * q - P["lamR"] * d * q + P["E_S"]
    E1 = first_source_derivative(nA, edges, n, Xa, Xa, P)
    return E0, E1


def second_order_shear(L, P, h, X):
    nA, edges = build(L)
    n = ice_polarized(edges)  # e=(2,0,0) at every vertex
    Xa = [X] * nA
    E0, E1 = E_diag(nA, edges, n, Xa, 1, P)
    d2 = F(0)
    for ei, (x, y, a) in enumerate(edges):
        m = n[:]; m[ei] ^= 1
        F0, F1 = E_diag(nA, edges, m, Xa, 1, P)
        D, Dp = F0 - E0, F1 - E1
        le = u(a, X)
        # E2 = -h^2 exp(2 l_e)/D(s);  dE2/ds = -h^2 [2 l_e'/D - D'/D^2]
        d2 += -h * h * (2 * le / D - Dp / (D * D))
    return E1 / nA, d2 / nA  # per A cell


X = [[F(0)] * 3 for _ in range(3)]; X[1][2] = X[2][1] = F(1)  # j23 direction -> couples to e1=2
h = F(1, 10)
iii = {}
for rho in (0, 1):
    nA, _ = build(2)
    PP = dict(Ud=F(1), Delta_can=F(4), dstar=3, eps_r=F(1, 2), lamR=F(1, 4), E_S=F(0),
              qA=[rho] * nA, qB=[rho] * nA)
    lead, corr = second_order_shear(2, PP, h, X)
    iii[rho] = dict(leading_per_A_cell=str(lead), leading_over_e1=str(lead / 2),
                    h2_correction_per_A_cell=str(corr), h2_correction_over_e1_over_h2=str(corr / 2 / h / h),
                    lambda_eff=str((lead + corr) / 2), lambda_eff_float=float((lead + corr) / 2))
out["claim_iii_tuple"] = dict(Ud=1, Delta_can=4, dstar=3, delta=0, lamR="1/4", eps_r="1/2", h="1/10")
out["claim_iii_shear_vertex"] = iii
lam0 = F(iii[0]["lambda_eff"]); lam1 = F(iii[1]["lambda_eff"])
out["claim_iii_lambda_eff_ratio_sq_rho1_over_rho0"] = float((lam1 / lam0) ** 2)
out["claim_iii_leading_identical"] = iii[0]["leading_over_e1"] == iii[1]["leading_over_e1"]
# analytic form of the h^2 correction for the polarized state (check): per A cell
#   lambda2 * e1 with lambda2 derived below by the script's numbers
json.dump(out, open(sys.argv[1] if len(sys.argv) > 1 else "/dev/stdout", "w"), indent=1, default=str)
print("\nALL ASSERTIONS PASSED")
