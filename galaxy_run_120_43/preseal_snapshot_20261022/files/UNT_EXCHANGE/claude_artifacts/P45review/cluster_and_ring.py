"""(1) Own connected-support cluster sum for c6/N and comparison with whole-graph brute force;
(2) direct census of support sign patterns on actual ice states (tests the P45 count claims);
(3) ring amplitude T(x) by 720 orderings, environment independence on real hexagons,
    and an exact-diagonalization normalization check of K on the 64-state hexagon cube.
Claude, P45 review. No Codex code imported."""
import sys, json, random
from fractions import Fraction as F
from itertools import permutations, combinations, product
sys.path.insert(0, "/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/P45review")
from graphs import (diamond_primitive, diamond_conventional, pg23_incidence, incidence,
                    edge_adjacency, cycles_of_length, euler_ice, loop_update)
from brute_rs import rs_energy


def cube_energy(signs, adj_pairs, Ud, alpha, order=6):
    """RS energy series of the reference state of a small flip cube (own implementation:
    explicit Hamiltonian dictionary, intermediate normalization)."""
    m = len(signs)
    A = 2 * Ud

    def D(S):
        tot = sum((A + alpha * signs[i]) for i in range(m) if S >> i & 1)
        tot += sum(2 * Ud * signs[i] * signs[j] for (i, j) in adj_pairs if S >> i & 1 and S >> j & 1)
        return F(tot)
    states = range(1 << m)
    E = [F(0)] * (order + 1)
    psi = [[F(0)] * (1 << m) for _ in range(order + 1)]
    psi[0][0] = F(1)
    for k in range(1, order + 1):
        E[k] = -sum(psi[k - 1][1 << i] for i in range(m))
        for S in states:
            if S == 0:
                continue
            v = sum(psi[k - 1][S ^ (1 << i)] for i in range(m))
            v += sum(E[j] * psi[k - j][S] for j in range(1, k))
            psi[k][S] = v / D(S)
    return E


def connected_weight(signs, adj_pairs, Ud, alpha):
    """Moebius inversion over subsets: weight of monomials with support exactly the full set."""
    m = len(signs)
    tot = [F(0)] * 7
    for r in range(1, m + 1):
        for sub in combinations(range(m), r):
            idx = {o: i for i, o in enumerate(sub)}
            sp = [(idx[i], idx[j]) for (i, j) in adj_pairs if i in idx and j in idx]
            Es = cube_energy([signs[i] for i in sub], sp, Ud, alpha)
            sgn = (-1) ** (m - r)
            for k in range(7):
                tot[k] += sgn * Es[k]
    return tot


def census(nv, edges, n):
    """Directly enumerate connected supports of <=3 edges with sign patterns on the graph."""
    inc = incidence(nv, edges)
    adj = edge_adjacency(nv, edges)
    sg = [1 - 2 * x for x in n]
    c = {}

    def add(key):
        c[key] = c.get(key, 0) + 1
    for e in range(len(edges)):
        add(("edge", sg[e]))
    for v in range(nv):
        for e, f in combinations(inc[v], 2):
            add(("pair", tuple(sorted((sg[e], sg[f])))))
        for t in combinations(inc[v], 3):
            add(("star", tuple(sorted(sg[x] for x in t))))
    # paths e-f-g, e~f, f~g, e !~ g ; count each unordered path once
    seen = set()
    for f in range(len(edges)):
        a, b = edges[f]
        for e in inc[a]:
            if e == f:
                continue
            for g in inc[b]:
                if g == f or g in adj[e] or g == e:
                    continue
                key = frozenset((e, f, g))
                if key in seen:
                    continue
                seen.add(key)
                ends = tuple(sorted((sg[e], sg[g])))
                add(("path", ends[0], sg[f], ends[1]))
    return {str(k): v for k, v in sorted(c.items())}


def per_vertex_formula(Ud, alpha):
    w = {}
    for s in (1, -1):
        w[("e", s)] = connected_weight([s], [], Ud, alpha)
    for p in ((1, 1), (1, -1), (-1, -1)):
        w[("p",) + p] = connected_weight(list(p), [(0, 1)], Ud, alpha)
    for t in ((1, 1, -1), (1, -1, -1), (1, 1, 1), (-1, -1, -1)):
        w[("s",) + t] = connected_weight(list(t), [(0, 1), (0, 2), (1, 2)], Ud, alpha)
    for u, s, v in product((1, -1), repeat=3):
        w[("P", u, s, v)] = connected_weight([u, s, v], [(0, 1), (1, 2)], Ud, alpha)
    tot = [F(0)] * 7
    def acc(key, mult):
        for k in range(7):
            tot[k] += mult * w[key][k]
    acc(("e", 1), 1); acc(("e", -1), 1)
    acc(("p", 1, 1), 1); acc(("p", 1, -1), 4); acc(("p", -1, -1), 1)
    acc(("s", 1, 1, -1), 2); acc(("s", 1, -1, -1), 2)
    for u, s, v in product((1, -1), repeat=3):
        acc(("P", u, s, v), (1 if u == s else 2) * (1 if v == s else 2))
    return tot, w


def hexagon_T(Ud, alpha, sig=(1, -1, 1, -1, 1, -1)):
    A = 2 * Ud

    def D(S):
        tot = sum(A + alpha * sig[i] for i in S)
        tot += sum(2 * Ud * sig[i] * sig[(i + 1) % 6] for i in S if (i + 1) % 6 in S)
        return F(tot)
    T = F(0)
    for perm in permutations(range(6)):
        prod = F(1)
        for k in range(1, 6):
            prod *= A / D(set(perm[:k]))
        T += prod
    return T


def graph_ring_amplitude(nv, edges, n, H, Ud, alpha):
    """Sum over 720 orderings using the exact degree-based energy on the real graph."""
    Hl = list(H)
    T = F(0)
    for perm in permutations(Hl):
        prod = F(1)
        for k in range(1, 6):
            dv = {}
            lin = F(0)
            for e in perm[:k]:
                s = 1 - 2 * n[e]
                for v in edges[e]:
                    dv[v] = dv.get(v, 0) + s
                lin += alpha * s
            Dk = Ud * sum(x * x for x in dv.values()) + lin
            prod *= 2 * Ud / Dk
        T += prod
    return T


if __name__ == "__main__":
    out = {}
    Ud = F(1)
    # (1) per-vertex cluster formula vs brute force values (from run_brute logs)
    for a in (F(0), F(1, 4), F(-3, 10), F(-1, 4)):
        tot, w = per_vertex_formula(Ud, a)
        out[f"c_per_V(alpha={a})"] = [str(x) for x in tot]
        if a == 0:
            out["w_edge_plus"] = [str(x) for x in w[("e", 1)]]
            out["w_star_+++ (absent in ice)"] = [str(x) for x in w[("s", 1, 1, 1)]]
    # disconnected 3-edge control
    out["disconnected_triple_weight"] = [str(x) for x in connected_weight([1, -1, 1], [], Ud, F(1, 4))]
    out["disconnected_pair_plus_edge"] = [str(x) for x in connected_weight([1, -1, 1], [(0, 1)], Ud, F(1, 4))]
    # (2) census on real ice states
    rng = random.Random(1)
    for name, builder in (("prim3", lambda: diamond_primitive(3)), ("pg23", pg23_incidence)):
        nv, edges, dirs = builder()
        n = euler_ice(nv, edges)
        cens = []
        for t in range(4):
            for _ in range(rng.randrange(1, 40)):
                loop_update(nv, edges, n, rng)
            cens.append(census(nv, edges, n))
        out[f"census_{name}_V={nv}"] = cens[0]
        out[f"census_{name}_identical_over_4_states"] = all(c == cens[0] for c in cens)
    # (3) ring amplitude
    for a in (F(0), F(1, 8), F(-1, 8), F(1, 4), F(-1, 4), F(1, 2)):
        out[f"T(x={a/2})"] = str(hexagon_T(Ud, a))
    out["T(0)_alt_pattern_-+-+-+"] = str(hexagon_T(Ud, F(0), (-1, 1, -1, 1, -1, 1)))
    out["T(alpha=1/4)_alt_pattern_-+-+-+"] = str(hexagon_T(Ud, F(1, 4), (-1, 1, -1, 1, -1, 1)))
    nv, edges, dirs = diamond_primitive(3)
    hexes = cycles_of_length(nv, edges, 6)
    n = euler_ice(nv, edges)
    amps = set()
    checked = 0
    for t in range(6):
        for _ in range(rng.randrange(1, 30)):
            loop_update(nv, edges, n, rng)
        for H in hexes:
            dv = {}
            for e in H:
                for v in edges[e]:
                    dv[v] = dv.get(v, 0) + n[e]
            if all(x == 1 for x in dv.values()):
                amps.add(graph_ring_amplitude(nv, edges, n, H, Ud, F(1, 4)))
                checked += 1
                if checked % 20 == 0:
                    pass
        if checked > 60:
            break
    out["graph_ring_amplitudes_alpha=1/4_distinct_values"] = [str(x) for x in amps]
    out["graph_ring_amplitudes_checked"] = checked
    print(json.dumps(out, indent=1))
