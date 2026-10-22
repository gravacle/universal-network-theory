"""Sensitivity control for the brute-force harness: on a 4-regular graph WITH triangles
(circulant C_n(1,2)) three-edge supports include triangles whose sign-pattern counts are
configuration dependent, so the h^6 diagonal SHOULD vary while h^2,h^4 stay constant.
Also: Ud-scaling check of c6 and adjacent-word (single Record flip) diagonal scalar check.
Claude, P45 review."""
import sys, json, random
from fractions import Fraction as F
sys.path.insert(0, "/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/P45review")
from brute_rs import rs_energy
from graphs import incidence, pg23_incidence, euler_ice, loop_update, girth
from cluster_and_ring import per_vertex_formula

def circulant(n):
    E = set()
    for i in range(n):
        for d in (1, 2):
            a, b = i, (i + d) % n
            E.add((min(a, b), max(a, b)))
    return n, sorted(E)

def all_ice(nv, edges, limit=400):
    inc = incidence(nv, edges)
    deg = [0] * nv; rem = [4] * nv
    n = [0] * len(edges); out = []
    def bt(e):
        if len(out) >= limit: return
        if e == len(edges):
            if all(d == 2 for d in deg): out.append(list(n))
            return
        u, v = edges[e]
        for val in (0, 1):
            ok = True
            for w in (u, v):
                dnew = deg[w] + val; rnew = rem[w] - 1
                if dnew > 2 or dnew + rnew < 2: ok = False
            if not ok: continue
            n[e] = val
            for w in (u, v): deg[w] += val; rem[w] -= 1
            bt(e + 1)
            for w in (u, v): deg[w] -= val; rem[w] += 1
            n[e] = 0
    bt(0)
    return out

def triangle_patterns(nv, edges, n):
    es = {e: i for i, e in enumerate(edges)}
    pat = {}
    for a in range(nv):
        for b in range(a + 1, nv):
            for c in range(b + 1, nv):
                t = [(a, b), (a, c), (b, c)]
                if all(x in es for x in t):
                    k = sum(n[es[x]] for x in t)
                    pat[k] = pat.get(k, 0) + 1
    return pat

nv, edges = circulant(10)
print("C10(1,2): V", nv, "E", len(edges), "girth", girth(nv, edges))
ices = all_ice(nv, edges, limit=2000)
rng = random.Random(5)
sample = rng.sample(ices, 8)
rows = []
for n in sample:
    E = rs_energy(edges, n, F(1), [F(0)] * len(edges), 6)
    rows.append((str(E[2]), str(E[4]), str(E[6]), triangle_patterns(nv, edges, n)))
    print(json.dumps(dict(E2=str(E[2]), E4=str(E[4]), E6=str(E[6]), occupied_count_per_triangle=triangle_patterns(nv, edges, n))))
print("n_ice_found", len(ices), "distinct E2:", len({r[0] for r in rows}), "distinct E4:", len({r[1] for r in rows}), "distinct E6:", len({r[2] for r in rows}))

# Ud scaling of the per-vertex c6 at x=0
t1, _ = per_vertex_formula(F(1), F(0)); t2, _ = per_vertex_formula(F(2), F(0))
print("c6/N Ud=1:", t1[6], " Ud=2:", t2[6], " ratio:", t1[6] / t2[6], "(expect 32)")

# adjacent word: one vertex v0 with Record flipped -> its 4 incident edges get alpha' ; diagonal still scalar?
nv, edges, _ = pg23_incidence()
inc = incidence(nv, edges)
n = euler_ice(nv, edges)
vals = set()
for t in range(6):
    for _ in range(rng.randrange(1, 40)):
        loop_update(nv, edges, n, rng)
    al = [F(1, 4)] * len(edges)
    for e in inc[0]:
        al[e] = F(1, 4) - F(1, 8)
    E = rs_energy(edges, n, F(1), al, 6)
    vals.add((E[2], E[4], E[6]))
print("adjacent-word (one Record flip, alpha=1/4, lambda_R=1/8) diagonal through h^6 distinct values over 6 states:", len(vals))
v = list(vals)[0]
A = F(2); a = F(1, 4); ap = a - F(1, 8)
uni = rs_energy(edges, n, F(1), [a] * len(edges), 2)
print("E2(adjacent) - E2(uniform) =", v[0] - uni[2], " formula d2 =", -4 * A * (1 / (A * A - ap * ap) - 1 / (A * A - a * a)))
