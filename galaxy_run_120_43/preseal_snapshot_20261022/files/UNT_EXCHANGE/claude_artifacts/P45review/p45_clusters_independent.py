#!/usr/bin/env python3
"""Independent (Claude) re-derivation of the P45 order-h^6 uniform diagonal claim.

Written from scratch; imports nothing from lanes/ or the UNT folder.

Model on a flip cluster C (set of m edges, adjacency given, frozen ice signs
sigma_e = 1 - 2 n_e):
  D(S) = sum_{e in S} (A + alpha*sigma_e) + 2Ud * sum_{adjacent e<f in S} sigma_e sigma_f,
  A = 2 Ud,  V = -h sum_{e in C} X_e.
D(S) is the exact excess of Ud*sum_v (d_v-2)^2 + mu*sum_e n_e over the ice
reference when the edges in S are flipped (derived in the review notes):
  sum_v (sum_{e in S, e ~ v} sigma_e)^2 = 2|S| + 2 sum_{adjacent pairs} sigma_e sigma_f.

Two INDEPENDENT exact methods for the lowest-branch energy series of a cluster:
  (M1) Feshbach / Brillouin-Wigner self-consistent series:
       E = -<0|V (D_Q + QVQ - E)^{-1} V|0>, solved as a truncated power series.
  (M2) Rayleigh-Schroedinger recursion in intermediate normalisation.
Connected weights by inclusion-exclusion over all sub-supports.
"""
from fractions import Fraction as F
from itertools import product, combinations
import json, sys

ORD = 7  # keep h^0..h^6


# ---------------- truncated power series in h (exact) ----------------
def s_zero():
    return [F(0)] * ORD


def s_add(a, b):
    return [x + y for x, y in zip(a, b)]


def s_sub(a, b):
    return [x - y for x, y in zip(a, b)]


def s_scale(a, c):
    return [x * c for x in a]


def s_mul(a, b):
    out = [F(0)] * ORD
    for i, x in enumerate(a):
        if x == 0:
            continue
        for j in range(ORD - i):
            if b[j]:
                out[i + j] += x * b[j]
    return out


def s_shift(a, k=1):  # multiply by h^k
    return [F(0)] * k + a[:ORD - k]


# ---------------- cluster energies ----------------
def make_D(signs, adj, Ud, alpha):
    m = len(signs)
    A = 2 * Ud
    D = []
    for S in range(1 << m):
        val = sum((A + alpha * signs[i]) for i in range(m) if S >> i & 1)
        val += sum(2 * Ud * signs[i] * signs[j] for (i, j) in adj if (S >> i & 1) and (S >> j & 1))
        D.append(F(val))
    for S in range(1, 1 << m):
        if D[S] <= 0:
            raise ValueError("nonpositive denominator %s for S=%d" % (D[S], S))
    return D


def energy_feshbach(signs, adj, Ud, alpha):
    """Method M1. Returns list E[0..6] of h^k coefficients."""
    m = len(signs)
    D = make_D(signs, adj, F(Ud), F(alpha))
    nQ = (1 << m)
    # v = Q X |0>  (order h^0 vector over Q states)
    v = {S: s_zero() for S in range(1, nQ)}
    for i in range(m):
        v[1 << i] = s_add(v[1 << i], [F(1)] + [F(0)] * (ORD - 1))
    E = s_zero()
    for outer in range(6):
        # solve (D + QVQ - E) w = v as series, QVQ = -h QXQ.
        # w = D^{-1} [ v + h QXQ w + E w ]
        w = {S: s_zero() for S in range(1, nQ)}
        for inner in range(8):
            new = {}
            for S in range(1, nQ):
                acc = list(v[S])
                hop = s_zero()
                for i in range(m):
                    T = S ^ (1 << i)
                    if T != 0:
                        hop = s_add(hop, w[T])
                acc = s_add(acc, s_shift(hop, 1))
                acc = s_add(acc, s_mul(E, w[S]))
                new[S] = s_scale(acc, 1 / D[S])
            w = new
        # E = -<0|V w V..>: V|0> = -h X|0>, <0|V = -h <0|X ; E = -(h^2) <X0| w >
        tot = s_zero()
        for i in range(m):
            tot = s_add(tot, w[1 << i])
        E = s_scale(s_shift(tot, 2), F(-1))
    return E


def energy_rs(signs, adj, Ud, alpha):
    """Method M2: RS recursion, intermediate normalisation."""
    m = len(signs)
    D = make_D(signs, adj, F(Ud), F(alpha))
    nQ = 1 << m
    c = [[F(0)] * nQ for _ in range(ORD)]
    c[0][0] = F(1)
    E = [F(0)] * ORD
    for n in range(1, ORD):
        # E_n = <0|V|psi_{n-1}> = -sum_i c_{n-1}(e_i)
        E[n] = -sum(c[n - 1][1 << i] for i in range(m))
        for S in range(1, nQ):
            val = sum(c[n - 1][S ^ (1 << i)] for i in range(m))
            val += sum(E[k] * c[n - k][S] for k in range(1, n))
            c[n][S] = val / D[S]
    return E


def sub_support(signs, adj, idx):
    pos = {o: k for k, o in enumerate(idx)}
    return [signs[i] for i in idx], [(pos[i], pos[j]) for (i, j) in adj if i in pos and j in pos]


_cache = {}


def cluster_energy(signs, adj, Ud, alpha, method="fesh"):
    key = (tuple(signs), tuple(sorted(adj)), F(Ud), F(alpha), method)
    if key not in _cache:
        fn = energy_feshbach if method == "fesh" else energy_rs
        _cache[key] = fn(list(signs), list(adj), Ud, alpha)
    return _cache[key]


def connected_weight(signs, adj, Ud, alpha, method="fesh"):
    """Inclusion-exclusion: w(C) = sum_{B subset C} (-1)^{|C|-|B|} e(B)."""
    m = len(signs)
    w = s_zero()
    for r in range(1, m + 1):
        for idx in combinations(range(m), r):
            ss, aa = sub_support(signs, adj, idx)
            e = cluster_energy(ss, aa, Ud, alpha, method)
            sign = (-1) ** (m - r)
            w = s_add(w, s_scale(e, F(sign)))
    return w


def per_vertex(Ud, alpha, method="fesh"):
    """Uniform per-vertex scalar using the d=2 count identities (to be cross-checked
    by direct enumeration on a real graph in p45_graph_check.py)."""
    terms = []
    for s in (1, -1):
        terms.append(("edge", (s,), F(1), connected_weight([s], [], Ud, alpha, method)))
    for sg, mult in (((1, 1), 1), ((1, -1), 4), ((-1, -1), 1)):
        terms.append(("pair", sg, F(mult), connected_weight(list(sg), [(0, 1)], Ud, alpha, method)))
    for sg in ((1, 1, -1), (1, -1, -1)):
        terms.append(("star", sg, F(2), connected_weight(list(sg), [(0, 1), (0, 2), (1, 2)], Ud, alpha, method)))
    for s in (1, -1):
        for u in (1, -1):
            for v in (1, -1):
                mult = (1 if u == s else 2) * (1 if v == s else 2)
                terms.append(("path", (u, s, v), F(mult),
                              connected_weight([u, s, v], [(0, 1), (1, 2)], Ud, alpha, method)))
    total = s_zero()
    for _, _, mult, w in terms:
        total = s_add(total, s_scale(w, mult))
    return total, terms


# ---------------- hexagon ring amplitude T(x) ----------------
def T_ring(x):
    """T(x) = (2Ud)^5 * sum over 720 orderings of prod_{k=1..5} 1/D(S_k),
    alternating hexagon, D/(2Ud) = #arcs(S) + x*(n_plus - n_minus)."""
    from itertools import permutations
    x = F(x)
    sig = [1, -1, 1, -1, 1, -1]

    def Dn(S):
        size = len(S)
        adjp = sum(1 for k in range(6) if k in S and (k + 1) % 6 in S)
        return size - adjp + x * sum(sig[k] for k in S)  # = (|S|A + a*sum sig - 2Ud*adj)/(2Ud)

    tot = F(0)
    for p in permutations(range(6)):
        prod = F(1)
        S = set()
        for k in range(5):
            S.add(p[k])
            prod /= Dn(S)
        tot += prod
    return tot


def frac_str(x):
    return "%d/%d" % (x.numerator, x.denominator)


if __name__ == "__main__":
    out = {}
    # ---- calibration: single edge closed form ----
    for (Ud, alpha) in ((1, 0), (1, F(1, 5)), (1, F(1, 4)), (2, F(-1, 3))):
        for s in (1, -1):
            e = cluster_energy([s], [], Ud, alpha)
            Dv = 2 * F(Ud) + F(alpha) * s
            exp = [0, 0, -1 / Dv, 0, 1 / Dv ** 3, 0, -2 / Dv ** 5]
            assert e == [F(q) for q in exp], (Ud, alpha, s, e)
    print("single-edge series e2=-1/D, e4=1/D^3, e6=-2/D^5: OK (both signs, 4 parameter points)")

    # ---- method agreement M1 vs M2 on every support type and pattern ----
    shapes = {
        "edge": [], "pair": [(0, 1)], "star": [(0, 1), (0, 2), (1, 2)], "path": [(0, 1), (1, 2)],
        "disc2": [], "disc_pair_edge": [(0, 1)], "disc3": [],
    }
    nchk = 0
    for alpha in (F(0), F(1, 5), F(-1, 5), F(3, 7)):
        for name, adj in shapes.items():
            m = 1 if name == "edge" else (2 if name in ("pair", "disc2") else 3)
            for sg in product((1, -1), repeat=m):
                a = cluster_energy(list(sg), adj, 1, alpha, "fesh")
                b = cluster_energy(list(sg), adj, 1, alpha, "rs")
                assert a == b, (name, sg, alpha)
                nchk += 1
    print("Feshbach-series vs RS-recursion cluster energies agree exactly on", nchk, "clusters")

    # ---- disconnected supports cancel ----
    for alpha in (F(0), F(1, 5), F(3, 7)):
        for sg in product((1, -1), repeat=3):
            assert connected_weight(list(sg), [], 1, alpha) == s_zero()
            assert connected_weight(list(sg), [(0, 1)], 1, alpha) == s_zero()
        for sg in product((1, -1), repeat=2):
            assert connected_weight(list(sg), [], 1, alpha) == s_zero()
    print("disconnected supports (2 disjoint, pair+edge, 3 disjoint): connected weight == 0 at all orders")

    # ---- odd orders vanish; 3-edge weights start at h^6 ----
    for alpha in (F(0), F(1, 5)):
        for name, adj in (("star", shapes["star"]), ("path", shapes["path"])):
            for sg in product((1, -1), repeat=3):
                w = connected_weight(list(sg), adj, 1, alpha)
                assert w[1] == w[2] == w[3] == w[4] == w[5] == 0, (name, sg, w)
        for sg in product((1, -1), repeat=2):
            w = connected_weight(list(sg), [(0, 1)], 1, alpha)
            assert w[1] == w[2] == w[3] == w[5] == 0
    print("3-edge connected weights vanish below h^6; pair weights vanish below h^4: OK")

    # ---- per-vertex constants ----
    res = {}
    for (Ud, alpha) in ((1, F(0)), (1, F(1, 5)), (1, F(-1, 5)), (1, F(1, 4)), (1, F(-1, 4)),
                        (2, F(0)), (1, F(1, 8)), (1, F(-1, 8))):
        tot, terms = per_vertex(Ud, alpha)
        tot_rs, _ = per_vertex(Ud, alpha, "rs")
        assert tot == tot_rs
        key = "Ud=%s,alpha=%s" % (Ud, alpha)
        res[key] = {"c%d/N" % k: frac_str(tot[k]) for k in (1, 2, 3, 4, 5, 6)}
        res[key]["c6/N_float"] = float(tot[6])
        res[key]["terms_h6"] = {"%s%s x%s" % (n, sg, mult): frac_str(w[6]) for (n, sg, mult, w) in terms}
        res[key]["terms_h4"] = {"%s%s x%s" % (n, sg, mult): frac_str(w[4]) for (n, sg, mult, w) in terms if w[4]}
        print(key, " c2/N =", tot[2], " c4/N =", tot[4], " c6/N =", tot[6], "=", float(tot[6]))
    out["per_vertex"] = res

    # ---- evenness in alpha and Ud scaling ----
    for a in (F(1, 5), F(1, 4), F(1, 8)):
        assert per_vertex(1, a)[0] == per_vertex(1, -a)[0]
    t1 = per_vertex(1, F(0))[0]
    t2 = per_vertex(2, F(0))[0]
    assert t2[2] == t1[2] / 2 and t2[4] == t1[4] / 8 and t2[6] == t1[6] / 32
    print("c_k(alpha) even in alpha; Ud scaling c2~1/Ud, c4~1/Ud^3, c6~1/Ud^5: OK")

    # ---- ring amplitude ----
    T0 = T_ring(0)
    T1 = T_ring(F(1, 10))
    T8 = T_ring(F(1, 16))
    T8m = T_ring(F(-1, 16))
    print("T(0) =", T0, " T(1/10) =", T1, "=", float(T1), " T(1/16)=T(-1/16):", T8 == T8m)
    out["T"] = {"T(0)": frac_str(T0), "T(1/10)": frac_str(T1), "T(1/10)_float": float(T1),
                "T(1/10)/T(0)": float(T1 / T0)}
    with open("/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/P45review/clusters_output.json", "w") as fh:
        json.dump(out, fh, indent=1)
    print("wrote clusters_output.json")
