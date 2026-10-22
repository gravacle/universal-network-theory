#!/usr/bin/env python3
"""Direct graph-level checks of the P45 h^6 uniform-diagonal claim (Claude, independent).

Graph: incidence graph of PG(2,3) (26 vertices, 52 edges, 4-regular, girth 6).
For several ice configurations (2-factors) with DIFFERENT flippable-hexagon counts:
  (a) direct exact RS recursion on the full graph (all states with <=3 flipped edges),
      no cluster decomposition, no counting identity used;
  (b) direct enumeration of every edge subset of size <=3 with its own adjacency and
      signs, summing exact inclusion-exclusion weights;
  (c) float Lanczos ED of H0+V on the <=3-flip truncated space (non-perturbative),
      comparing configurations and the residual against the exact c2,c4,c6.
Only my own module p45_clusters_independent is imported.
"""
import sys, json, random, time
from fractions import Fraction as F
from itertools import combinations, product
import numpy as np

sys.path.insert(0, "/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/P45review")
import p45_clusters_independent as cl

OUT = "/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/P45review/"


# ---------------- PG(2,3) incidence graph ----------------
def pg23():
    pts = []
    for v in product(range(3), repeat=3):
        if v == (0, 0, 0):
            continue
        # normalise: first nonzero coordinate = 1
        for c in v:
            if c:
                inv = 1 if c == 1 else 2
                break
        w = tuple((inv * x) % 3 for x in v)
        if w not in pts:
            pts.append(w)
    assert len(pts) == 13
    edges = []
    for i, p in enumerate(pts):
        for j, l in enumerate(pts):
            if sum(a * b for a, b in zip(p, l)) % 3 == 0:
                edges.append((i, 13 + j))
    return 26, edges


def octahedron():
    n = 6
    edges = [(i, j) for i in range(6) for j in range(i + 1, 6) if not (j == i + 1 and i % 2 == 0)]
    return n, edges


def girth(n, edges):
    adj = [[] for _ in range(n)]
    for k, (a, b) in enumerate(edges):
        adj[a].append(b)
        adj[b].append(a)
    best = 10 ** 9
    for s in range(n):
        dist = [-1] * n
        par = [-1] * n
        dist[s] = 0
        q = [s]
        for u in q:
            for w in adj[u]:
                if dist[w] < 0:
                    dist[w] = dist[u] + 1
                    par[w] = u
                    q.append(w)
                elif par[u] != w:
                    best = min(best, dist[u] + dist[w] + 1)
    return best


def edge_adjacency(edges):
    m = len(edges)
    inc = {}
    for k, (a, b) in enumerate(edges):
        inc.setdefault(a, []).append(k)
        inc.setdefault(b, []).append(k)
    nb = [set() for _ in range(m)]
    for v, ks in inc.items():
        for x in ks:
            for y in ks:
                if x != y:
                    nb[x].add(y)
    return inc, nb


def all_two_factors(n, edges, inc, limit=None):
    """Exhaustive backtracking enumeration of 2-factors (ice configurations)."""
    m = len(edges)
    occ = [None] * m
    deg_occ = [0] * n
    deg_und = [len(inc[v]) for v in range(n)]
    sols = []

    def feasible(v):
        return deg_occ[v] <= 2 and deg_occ[v] + deg_und[v] >= 2

    def rec(k):
        if limit and len(sols) >= limit:
            return
        if k == m:
            if all(d == 2 for d in deg_occ):
                sols.append(tuple(occ))
            return
        a, b = edges[k]
        for val in (1, 0):
            occ[k] = val
            deg_und[a] -= 1
            deg_und[b] -= 1
            deg_occ[a] += val
            deg_occ[b] += val
            if feasible(a) and feasible(b):
                rec(k + 1)
            deg_occ[a] -= val
            deg_occ[b] -= val
            deg_und[a] += 1
            deg_und[b] += 1
        occ[k] = None

    rec(0)
    return sols


def six_cycles(n, edges):
    idx = {}
    for k, (a, b) in enumerate(edges):
        idx[(a, b)] = k
        idx[(b, a)] = k
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    found = {}

    def dfs(path):
        if len(path) == 6:
            if path[0] in adj[path[-1]]:
                es = [idx[(path[i], path[(i + 1) % 6])] for i in range(6)]
                found.setdefault(tuple(sorted(es)), es)
            return
        for w in adj[path[-1]]:
            if w not in path and w > path[0]:
                dfs(path + [w])

    for s in range(n):
        dfs([s])
    return list(found.values())


def flippable_count(occ, hexes):
    c = 0
    for h in hexes:
        s = [occ[e] for e in h]
        if all(s[i] != s[(i + 1) % 6] for i in range(6)):
            c += 1
    return c


def cycle_structure(n, edges, occ):
    adj = [[] for _ in range(n)]
    for k, (a, b) in enumerate(edges):
        if occ[k]:
            adj[a].append(b)
            adj[b].append(a)
    seen = [False] * n
    lens = []
    for s in range(n):
        if not seen[s]:
            L = 0
            st = [s]
            seen[s] = True
            while st:
                u = st.pop()
                L += 1
                for w in adj[u]:
                    if not seen[w]:
                        seen[w] = True
                        st.append(w)
            lens.append(L)
    return sorted(lens)


# ---------------- (a) direct exact RS on full graph ----------------
def direct_rs(edges, nb, occ, Ud, alpha, maxflip=3):
    Ud, alpha = F(Ud), F(alpha)
    A = 2 * Ud
    m = len(edges)
    sig = [1 - 2 * o for o in occ]

    def D(S):
        val = sum(A + alpha * sig[e] for e in S)
        for i, e in enumerate(S):
            for f in S[i + 1:]:
                if f in nb[e]:
                    val += 2 * Ud * sig[e] * sig[f]
        return val

    states = [()]
    for r in range(1, maxflip + 1):
        states += list(combinations(range(m), r))
    Dv = {S: D(S) for S in states}
    for S in states[1:]:
        assert Dv[S] > 0
    # c[n] dict: state -> coeff, only nonzero entries
    c = [dict() for _ in range(7)]
    c[0][()] = F(1)
    E = [F(0)] * 7
    for n in range(1, 7):
        E[n] = -sum(c[n - 1].get((e,), F(0)) for e in range(m))
        if n == 6:
            break
        acc = {}
        # hop contributions: [ -V psi_{n-1} ](S) = sum_{e} c_{n-1}(S xor e)
        for T, val in c[n - 1].items():
            Tl = list(T)
            for e in range(m):
                if e in T:
                    S = tuple(x for x in Tl if x != e)
                else:
                    if len(T) >= maxflip:
                        continue
                    S = tuple(sorted(Tl + [e]))
                if S == ():
                    continue
                acc[S] = acc.get(S, F(0)) + val
        for k in range(1, n):
            if E[k]:
                for S, val in c[n - k].items():
                    if S != ():
                        acc[S] = acc.get(S, F(0)) + E[k] * val
        c[n] = {S: v / Dv[S] for S, v in acc.items() if v != 0}
    return E


# ---------------- (b) direct subset enumeration of cluster weights ----------------
def subset_sum(edges, nb, occ, Ud, alpha, maxsize=3):
    m = len(edges)
    sig = [1 - 2 * o for o in occ]
    tot = cl.s_zero()
    census = {}
    for r in range(1, maxsize + 1):
        for C in combinations(range(m), r):
            adj = [(i, j) for i in range(r) for j in range(i + 1, r) if C[j] in nb[C[i]]]
            signs = [sig[e] for e in C]
            # classify (for the census) - connected?
            w = cl.connected_weight(signs, adj, Ud, alpha)
            if any(w):
                key = (r, len(adj), tuple(sorted(signs)))
                census[key] = census.get(key, 0) + 1
                tot = cl.s_add(tot, w)
    return tot, census


# ---------------- (c) float Lanczos on truncated space ----------------
def build_trunc(edges, nb, occ, Ud, alpha, maxflip=3):
    m = len(edges)
    sig = [1 - 2 * o for o in occ]
    A = 2.0 * Ud
    states = [()]
    for r in range(1, maxflip + 1):
        states += list(combinations(range(m), r))
    index = {S: i for i, S in enumerate(states)}
    Dv = np.zeros(len(states))
    rows, cols = [], []
    for i, S in enumerate(states):
        val = sum(A + alpha * sig[e] for e in S)
        for a_, e in enumerate(S):
            for f in S[a_ + 1:]:
                if f in nb[e]:
                    val += 2.0 * Ud * sig[e] * sig[f]
        Dv[i] = val
        for e in S:  # remove e -> neighbour
            T = tuple(x for x in S if x != e)
            j = index[T]
            rows += [i, j]
            cols += [j, i]
    return Dv, np.array(rows), np.array(cols)


def lanczos_ground(Dv, rows, cols, h, nit=200):
    n = len(Dv)

    def mv(x):
        return Dv * x - h * np.bincount(rows, weights=x[cols], minlength=n)

    rng = np.random.default_rng(1)
    v = np.zeros(n)
    v[0] = 1.0
    v += 1e-3 * rng.standard_normal(n)
    v /= np.linalg.norm(v)
    V = [v]
    al, be = [], []
    w = mv(v)
    a = v @ w
    w = w - a * v
    al.append(a)
    for k in range(1, nit):
        b = np.linalg.norm(w)
        if b < 1e-14:
            break
        v = w / b
        for u in V:  # full reorthogonalisation
            v -= (u @ v) * u
        v /= np.linalg.norm(v)
        V.append(v)
        be.append(b)
        w = mv(v) - b * V[-2]
        a = v @ w
        w = w - a * v
        al.append(a)
    T = np.diag(al) + np.diag(be, 1) + np.diag(be, -1)
    return np.linalg.eigvalsh(T)[0]


def main():
    t0 = time.time()
    report = {}
    n, edges = pg23()
    m = len(edges)
    inc, nb = edge_adjacency(edges)
    degs = sorted(set(len(inc[v]) for v in range(n)))
    g = girth(n, edges)
    print("PG(2,3) incidence graph: n=%d m=%d degrees=%s girth=%d" % (n, m, degs, g))
    assert degs == [4] and g == 6
    hexes = six_cycles(n, edges)
    print("number of 6-cycles:", len(hexes))
    sols = all_two_factors(n, edges, inc)
    print("number of ice configurations (2-factors), exhaustive:", len(sols))
    # flippable counts distribution
    dist = {}
    for s in sols:
        k = flippable_count(s, hexes)
        dist[k] = dist.get(k, 0) + 1
    print("flippable-hexagon count distribution {count: #configs}:", dict(sorted(dist.items())))
    report["graph"] = dict(n=n, m=m, girth=g, n_hexagons=len(hexes), n_ice=len(sols),
                           flippable_distribution={str(k): v for k, v in sorted(dist.items())})
    # pick configs spanning min..max flippable count with differing cycle structures
    bykey = {}
    for s in sols:
        k = (flippable_count(s, hexes), tuple(cycle_structure(n, edges, s)))
        bykey.setdefault(k, s)
    keys = sorted(bykey)
    print("distinct (flippable, cycle-structure) classes:", len(keys))
    chosen = []
    # extremes + a spread
    pick = [keys[0], keys[-1]] + keys[1:-1:max(1, (len(keys) - 2) // 4)][:4]
    for k in pick:
        chosen.append((k, bykey[k]))
    report["configs"] = []
    exact = {}
    for (Ud, alpha) in ((1, F(0)), (1, F(1, 5))):
        tot, _ = cl.per_vertex(Ud, alpha)
        exact[(Ud, alpha)] = tot
    for (k, occ) in chosen:
        row = dict(flippable=k[0], cycles=list(k[1]))
        assert all(sum(occ[e] for e in inc[v]) == 2 for v in range(n))
        for (Ud, alpha) in ((1, F(0)), (1, F(1, 5))):
            E = direct_rs(edges, nb, occ, Ud, alpha)
            S, census = subset_sum(edges, nb, occ, Ud, alpha)
            pred = [x * n for x in exact[(Ud, alpha)]]
            okA = (E[2] == pred[2] and E[4] == pred[4] and E[6] == pred[6] and E[1] == E[3] == E[5] == 0)
            okB = (S[2] == E[2] and S[4] == E[4] and S[6] == E[6])
            tag = "x=%s" % (alpha / 2)
            row[tag] = dict(E2=str(E[2]), E4=str(E[4]), E6=str(E[6]), E6_float=float(E[6]),
                            direct_equals_26_times_per_vertex=okA, subset_sum_equals_direct=okB,
                            connected_support_census={"size%d_adj%d_signs%s" % kk: v for kk, v in sorted(census.items())})
            print("config flippable=%d cycles=%s %s: E2=%s E4=%s E6=%s (%.15f)  direct==N*c: %s  subsets==direct: %s"
                  % (k[0], list(k[1]), tag, E[2], E[4], E[6], float(E[6]), okA, okB))
            assert okA and okB
        report["configs"].append(row)
    print("exact part done in %.1fs" % (time.time() - t0))

    # ---------------- float ED ----------------
    hs = [0.05, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5]
    report["ED"] = {}
    for (Ud, alpha) in ((1.0, 0.0), (1.0, 0.2)):
        tot = exact[(1, F(alpha).limit_denominator(100))]
        c2, c4, c6 = (float(tot[2]) * n, float(tot[4]) * n, float(tot[6]) * n)
        tab = []
        Es = {}
        for ci, (k, occ) in enumerate(chosen):
            Dv, rows, cols = build_trunc(edges, nb, occ, Ud, alpha)
            Es[ci] = [lanczos_ground(Dv, rows, cols, h) for h in hs]
        for hi, h in enumerate(hs):
            vals = [Es[ci][hi] for ci in Es]
            pert = c2 * h ** 2 + c4 * h ** 4 + c6 * h ** 6
            resid = vals[0] - pert
            spread = max(vals) - min(vals)
            tab.append(dict(h=h, E_config0=vals[0], spread_over_configs=spread,
                            resid_vs_c2c4c6=resid, resid_over_h8=resid / h ** 8,
                            resid_without_c6_over_h6=(vals[0] - c2 * h ** 2 - c4 * h ** 4) / h ** 6))
            print("x=%.2f h=%.2f E=%.15f spread=%.3e resid=%.3e resid/h^8=%.5f (E-c2-c4)/h^6=%.8f (exact c6=%.8f)"
                  % (alpha / 2, h, vals[0], spread, resid, resid / h ** 8,
                     (vals[0] - c2 * h ** 2 - c4 * h ** 4) / h ** 6, c6))
        report["ED"]["x=%.2f" % (alpha / 2)] = dict(N_c6=c6, table=tab)
    with open(OUT + "graph_check_output.json", "w") as fh:
        json.dump(report, fh, indent=1)
    print("wrote graph_check_output.json; total %.1fs" % (time.time() - t0))


if __name__ == "__main__":
    main()
