"""Independent Claude check of packet P49-origin-0066 (FROM_CODEX2/0066).
Own code only; imports no Codex-authored module. Exact Fractions where feasible,
numpy only for random refutation probes and the toy written-count bound.
"""
import json, itertools, sys
from fractions import Fraction as F
import numpy as np

out = {}

# ---------- exact complex-rational helpers (pairs re,im) ----------
class C:
    __slots__ = ("r", "i")
    def __init__(s, r, i=0): s.r = F(r); s.i = F(i)
    def __add__(s, o): o = o if isinstance(o, C) else C(o); return C(s.r + o.r, s.i + o.i)
    __radd__ = __add__
    def __sub__(s, o): o = o if isinstance(o, C) else C(o); return C(s.r - o.r, s.i - o.i)
    def __mul__(s, o): o = o if isinstance(o, C) else C(o); return C(s.r*o.r - s.i*o.i, s.r*o.i + s.i*o.r)
    __rmul__ = __mul__
    def conj(s): return C(s.r, -s.i)
    def __eq__(s, o): o = o if isinstance(o, C) else C(o); return s.r == o.r and s.i == o.i
    def __repr__(s): return f"{s.r}{'+' if s.i>=0 else '-'}{abs(s.i)}i"

def cmat(a): return [[x if isinstance(x, C) else C(x) for x in r] for r in a]
def cmm(a, b):
    n, m, k = len(a), len(b[0]), len(b)
    return [[sum((a[i][l]*b[l][j] for l in range(k)), C(0)) for j in range(m)] for i in range(n)]
def cdag(a): return [[a[j][i].conj() for j in range(len(a))] for i in range(len(a[0]))]
def expect(A, v):  # <v|A|v> for (unnormalized) exact vector, returns real part / norm
    Av = [sum((A[i][j]*v[j] for j in range(len(v))), C(0)) for i in range(len(v))]
    num = sum((v[i].conj()*Av[i] for i in range(len(v))), C(0))
    den = sum((v[i].conj()*v[i] for i in range(len(v))), C(0))
    assert num.i == 0 and den.i == 0
    return num.r / den.r

def fr(x): return str(x)

# ---------- 1. Hadamard Cesaro control (own construction) ----------
vecs = [[F(x, 2) for x in r] for r in ((1,1,1,1),(1,-1,1,-1),(1,1,-1,-1),(1,-1,-1,1))]
outer = lambda u: [[x*y for y in u] for x in u]
def mm(a, b): return [[sum((a[i][k]*b[k][j] for k in range(len(b))), F(0)) for j in range(len(b[0]))] for i in range(len(a))]
def madd(a, b): return [[x+y for x, y in zip(r, s)] for r, s in zip(a, b)]
def zeros(n): return [[F(0)]*n for _ in range(n)]
def eye(n): return [[F(int(i == j)) for j in range(n)] for i in range(n)]
P = [outer(v) for v in vecs]
# orthogonal complete projectors
assert all(mm(P[i], P[j]) == (P[i] if i == j else zeros(4)) for i in range(4) for j in range(4))
S = zeros(4)
for p in P: S = madd(S, p)
assert S == eye(4)
words = ["00", "01", "10", "11"]
def cesaro(Pl, n, basis_word_index):
    effs = {}
    for w in range(len(words)):
        O = [[F(int(i == j and basis_word_index[i] == w)) for j in range(n)] for i in range(n)]
        e = zeros(n)
        for p in Pl: e = madd(e, mm(mm(p, O), p))
        effs[words[w]] = e
    return effs
had = cesaro(P, 4, [0, 1, 2, 3])
out["hadamard_cesaro_all_I_over_4"] = all(had[w] == [[F(1,4)*int(i == j) for j in range(4)] for i in range(4)] for w in words)

# Cesaro formula numeric sanity: long time average vs sum_E Pi_E O Pi_E (random real H, nondegenerate)
rng = np.random.default_rng(66)
A = rng.normal(size=(4, 4)); H = (A + A.T)/2
ev, U = np.linalg.eigh(H)
O = np.diag([0, 1, 0, 0.]).astype(complex)
Ebar = sum(np.outer(U[:, k], U[:, k]) @ O @ np.outer(U[:, k], U[:, k]) for k in range(4))
ts = np.linspace(0, 4000, 200001)
acc = np.zeros((4, 4), complex)
for t in ts[::50]:
    Ut = U @ np.diag(np.exp(-1j*ev*t)) @ U.T
    acc += Ut.conj().T @ O @ Ut
acc /= len(ts[::50])
out["cesaro_formula_numeric_maxdiff_T4000"] = float(np.max(np.abs(acc - Ebar)))

# ---------- 2. Fragmentation / frozen-word fixture ----------
Pf = [ [[F(int(i == j == 0)) for j in range(4)] for i in range(4)],
       [[F(int(i == j and i in (1, 2))) for j in range(4)] for i in range(4)],
       [[F(int(i == j == 3)) for j in range(4)] for i in range(4)] ]
frag = cesaro(Pf, 4, [0, 1, 2, 3])
def compress(E, idx): return [[E[i][j] for j in idx] for i in idx]
def scalar_check(a):
    d = len(a); c = sum((a[i][i] for i in range(d)), F(0))/d
    res = [[a[i][j] - (c if i == j else 0) for j in range(d)] for i in range(d)]
    return c, not any(x for r in res for x in r), res
def real_witnesses(a):
    d = len(a); vals = [a[i][i] for i in range(d)]
    for i in range(d):
        for j in range(i+1, d):
            for s in (-1, 1): vals.append((a[i][i] + a[j][j] + 2*s*a[i][j])/2)
    return vals
fr_rows = {w: scalar_check(compress(frag[w], [1, 2])) for w in words}
out["frozen_fixture_seed_dependent_on_01_10"] = not all(v[1] for v in fr_rows.values())
out["frozen_fixture_word01_spread"] = fr(max(real_witnesses(compress(frag["01"], [1, 2]))) - min(real_witnesses(compress(frag["01"], [1, 2]))))
# both seeds share energy 1 and written count 1 (same block)
out["frozen_fixture_seeds_same_energy_block"] = True

# ---------- 3. Correlated stipulated law ----------
law = {"00": F(1,2), "01": F(0), "10": F(0), "11": F(1,2)}
def stats(law):
    m0 = law["10"] + law["11"]; m1 = law["01"] + law["11"]
    cov = law["11"] - m0*m1
    fair = {w: F(1,4) for w in words}
    prod = {w: (m0 if w[0] == "1" else 1-m0)*(m1 if w[1] == "1" else 1-m1) for w in words}
    tv = lambda p, q: sum(abs(p[w]-q[w]) for w in words)/2
    return dict(q0=fr(m0), q1=fr(m1), cov=fr(cov), TV_fair=fr(tv(law, fair)), TV_same_marginal_iid=fr(tv(law, prod)))
out["correlated_control_stats"] = stats(law)
# biased iid universal law: what label would the 0066 three-way rule assign?
pb = F(1,4)
biased = {w: (pb if w[0]=="1" else 1-pb)*(pb if w[1]=="1" else 1-pb) for w in words}
def label_0066_rule(law):  # independent re-statement of the packet's labels (not imported)
    if all(v == F(1, len(law)) for v in law.values()): return "FAIR_COIN_EQUIVALENT"
    return "NONUNIFORM_COMMON_WORD_LAW"
out["biased_iid_law"] = {w: fr(v) for w, v in biased.items()}
out["biased_iid_stats"] = stats(biased)
out["label_correlated"] = label_0066_rule(law)
out["label_biased_iid"] = label_0066_rule(biased)
out["axis2_label_discriminates_correlated_vs_biased_iid"] = label_0066_rule(law) != label_0066_rule(biased)

# ---------- 4. Coherent-seed control ----------
plus = [[F(1,2), F(1,2)], [F(1,2), F(1,2)]]; minus = [[F(1,2), F(-1,2)], [F(-1,2), F(1,2)]]
out["coherent_control_basis_values"] = [fr(plus[0][0]), fr(plus[1][1])]
wv = real_witnesses(plus)
out["coherent_control_spread"] = fr(max(wv) - min(wv))
out["coherent_control_sum_identity"] = madd(plus, minus) == eye(2)

# ---------- 5. Fixed-time effects under REAL H are complex: real +/- witnesses blind ----------
# H = X (real symmetric). U(t)=exp(-iXt). At t=pi/4: U = (I - iX)/sqrt2, so E0 = U^dag |0><0| U
# exact: U^dag = (I + iX)/sqrt2 ; E0 = (1/2)(I+iX)|0><0|(I-iX)
I2 = cmat(eye(2)); X = cmat([[0, 1], [1, 0]])
iX = [[C(0, x.r) for x in r] for r in X]
Ud_unnorm = [[I2[i][j] + iX[i][j] for j in range(2)] for i in range(2)]   # (I+iX)
U_unnorm = cdag(Ud_unnorm)                                                  # (I-iX)
Pi0 = cmat([[1, 0], [0, 0]])
E0 = [[x*C(F(1,2)) for x in r] for r in cmm(cmm(Ud_unnorm, Pi0), U_unnorm)]
out["fixed_time_realH_E0_entries"] = [[repr(x) for x in r] for r in E0]
vals = {}
for name, v in {"|0>": [C(1), C(0)], "|1>": [C(0), C(1)], "|+>": [C(1), C(1)], "|->": [C(1), C(-1)],
                "|+i>": [C(1), C(0, 1)], "|-i>": [C(1), C(0, -1)]}.items():
    vals[name] = fr(expect(E0, v))
out["fixed_time_realH_word0_probabilities"] = vals
# general identity E(t)^* = E(-t) for real H: numeric probe
A = rng.normal(size=(5, 5)); H = (A + A.T)/2; ev, V = np.linalg.eigh(H)
Pi = np.diag([1, 0, 1, 0, 0.])
def Et(t):
    Ut = V @ np.diag(np.exp(-1j*ev*t)) @ V.T; return Ut.conj().T @ Pi @ Ut
out["realH_fixed_time_max_imag_part_t0.7"] = float(np.max(np.abs(Et(0.7).imag)))
out["realH_conj_E_t_equals_E_minus_t_maxdiff"] = float(np.max(np.abs(Et(0.7).conj() - Et(-0.7))))
Cb = sum(np.outer(V[:, k], V[:, k]) @ Pi @ np.outer(V[:, k], V[:, k]) for k in range(5))
out["realH_cesaro_max_imag_part"] = float(np.max(np.abs(np.imag(Cb.astype(complex)))))

# ---------- 6. Criterion: scalar compression <=> constant expectation (random refutation) ----------
fails = 0
for trial in range(2000):
    d = int(rng.integers(2, 6))
    Bm = rng.normal(size=(d, d)) + 1j*rng.normal(size=(d, d)); Bm = (Bm + Bm.conj().T)/2
    if trial % 2: Bm = np.eye(d)*rng.normal()  # scalar cases
    # spread over all pure states = lambda_max - lambda_min
    w = np.linalg.eigvalsh(Bm); spread = w[-1] - w[0]
    is_scalar = np.allclose(Bm, np.eye(d)*np.trace(Bm).real/d)
    if is_scalar != (spread < 1e-12): fails += 1
out["criterion_random_trials_2000_mismatches"] = fails
# imaginary off-diagonal invisible to real +/- and basis witnesses, visible to +/- i
Bm = np.array([[0.5, -0.5j], [0.5j, 0.5]])
real_w = [Bm[0, 0].real, Bm[1, 1].real] + [((Bm[0, 0] + Bm[1, 1] + s*2*Bm[0, 1].real)/2).real for s in (-1, 1)]
cplx_w = [((Bm[0, 0] + Bm[1, 1] + s*2*Bm[0, 1].imag)/2).real for s in (-1, 1)]
out["imag_offdiag_real_witness_spread"] = float(max(real_w) - min(real_w))
out["imag_offdiag_pm_i_witness_spread"] = float(max(cplx_w) - min(cplx_w))

# ---------- 7. Fixed-time dimension cap (strengthening) ----------
# claim: if V^dag E V = c I_d with E projector rank r and 0<c, then d<=r ; c<1 => d<=n-r.
viol = 0
for trial in range(3000):
    n = int(rng.integers(2, 7)); r = int(rng.integers(1, n)); d = int(rng.integers(1, n+1))
    Q, _ = np.linalg.qr(rng.normal(size=(n, n)) + 1j*rng.normal(size=(n, n)))
    E = Q[:, :r] @ Q[:, :r].conj().T
    Vv, _ = np.linalg.qr(rng.normal(size=(n, d)) + 1j*rng.normal(size=(n, d)))
    M = Vv.conj().T @ E @ Vv
    if np.allclose(M, np.eye(d)*np.trace(M).real/d, atol=1e-9) and (d > r and np.trace(M).real/d > 1e-9): viol += 1
out["dim_cap_random_violations"] = viol
# constructive: largest scalar-compression subspace for rank-r projector with c=1/2 has d=min(r,n-r)
n, r = 6, 2
E = np.diag([1, 1, 0, 0, 0, 0.])
Vv = np.zeros((6, 2)); Vv[0, 0] = Vv[2, 0] = Vv[1, 1] = Vv[3, 1] = 1/np.sqrt(2)
out["dim_cap_attained_d2_r2_c_half"] = bool(np.allclose(Vv.T @ E @ Vv, 0.5*np.eye(2)))

# ---------- 8. Energy conflation: subspace test reports dependence that is pure energy dependence ----------
# diagonal H = diag(0,1,1,2) on words 00,01,10,11; seeds S={00,01} have different energies.
Hd = [0, 1, 1, 2]
dep = {w: scalar_check(compress(frag[w], [0, 1]))[1] for w in words}
out["energy_conflation_subspace_test_universal_flags"] = dep
# energy-matched family inside S: all states with weight p on E=0, 1-p on E=1 -> identical Cesaro law
p = F(1,3)
lawA = {w: p*frag[w][0][0] + (1-p)*frag[w][1][1] for w in words}
out["energy_matched_family_law"] = {w: fr(v) for w, v in lawA.items()}
out["energy_matched_family_is_universal_by_construction"] = True
# energy-matching of a subspace itself is the same compression criterion on Pi_E
out["energy_projector_compressions_on_S_00_01"] = [scalar_check(compress(Pp, [0, 1]))[1] for Pp in Pf]

# ---------- 9. Written-count bound on a toy with Bind/admission/hopping ----------
# two sites; local factors p (2) x q (2) x cell (3:I,R,S); admission |S,p=1><R,p=0| x I_q
dl = 12
def loc(op_p=None, op_q=None, op_c=None):
    a = np.eye(2) if op_p is None else op_p; b = np.eye(2) if op_q is None else op_q; c = np.eye(3) if op_c is None else op_c
    return np.kron(np.kron(a, b), c)
def site(op, v): return np.kron(op, np.eye(dl)) if v == 0 else np.kron(np.eye(dl), op)
pn = np.diag([0, 1.]); qn = np.diag([0, 1.]); Xq = np.array([[0, 1], [1, 0.]]); Yq = np.array([[0, -1j], [1j, 0]])
sp = np.array([[0, 0], [1, 0.]])  # |1><0| carrier raise
Ap = loc(op_p=sp, op_c=np.array([[0, 0, 0], [0, 0, 0], [0, 1, 0.]]))  # |S,1><R,0|
PR = loc(op_c=np.diag([0, 1, 0.])); PS = loc(op_c=np.diag([0, 0, 1.]))
g, kap, t_h = 0.7, 0.9, 1.3
Hm = np.zeros((144, 144), complex)
for v in (0, 1):
    Hm += g*site(loc(op_p=pn, op_q=Xq), v)
    Hm += kap*(site(Ap, v) + site(Ap.conj().T, v))
    Hm += rng.normal()*site(loc(op_p=pn), v) + rng.normal()*site(loc(op_q=qn), v) + rng.normal()*site(PR, v) + rng.normal()*site(PS, v)
hop = np.kron(loc(op_p=sp), loc(op_p=sp.T))
Hm += -t_h*(hop + hop.conj().T)
Hm += 0.4*site(loc(op_p=pn), 0) @ site(loc(op_q=qn), 1)  # extra diagonal coupling
Nc = site(loc(op_p=pn), 0) + site(loc(op_p=pn), 1)
Nq = site(loc(op_q=qn), 0) + site(loc(op_q=qn), 1)
NR = site(PR, 0) + site(PR, 1)
Qop = Nc + NR
out["toy_H_Q_commutator_norm"] = float(np.max(np.abs(Hm @ Qop - Qop @ Hm)))
dNq = 1j*(Hm @ Nq - Nq @ Hm)
pY = site(loc(op_p=pn, op_q=Yq), 0) + site(loc(op_p=pn, op_q=Yq), 1)
out["toy_dNq_equals_minus_g_pY_maxdiff"] = float(np.max(np.abs(dNq - (-g)*pY)))
out["toy_min_eig_Nc_minus_pY"] = float(np.min(np.linalg.eigvalsh(Nc - pY)))
out["toy_min_eig_Nc_plus_pY"] = float(np.min(np.linalg.eigvalsh(Nc + pY)))
out["toy_min_eig_Q_minus_Nc"] = float(np.min(np.linalg.eigvalsh(Qop - Nc)))
ew, EV = np.linalg.eigh(Hm)
worst = -1e9
for trial in range(20):
    psi = rng.normal(size=144) + 1j*rng.normal(size=144)
    # project to sharp Q=2
    Qd = np.real(np.diag(Qop)); psi[Qd != 2] = 0; psi /= np.linalg.norm(psi)
    nq0 = np.real(psi.conj() @ Nq @ psi)
    c = EV.conj().T @ psi
    for tt in np.linspace(0, 10, 101):
        ph = EV @ (np.exp(-1j*ew*tt)*c)
        nq = np.real(ph.conj() @ Nq @ ph)
        worst = max(worst, abs(nq - nq0) - g*2*tt)
out["toy_bound_max_violation_(|dNq|-|g|Qt)"] = float(worst)

json.dump(out, open(sys.argv[1], "w"), indent=1, default=str)
print(json.dumps(out, indent=1, default=str))
