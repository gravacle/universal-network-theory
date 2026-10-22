"""Extension check: is the h^8 diagonal also configuration independent (tree-support argument)?
PG(2,3) incidence graph, exact Fractions, whole-graph RS through h^8. Also counts elementary
8-cycles in the diamond lattice (prim L=5 torus: no winding cycles shorter than 10).
Claude, P45 review."""
import sys, json, random, time
from fractions import Fraction as F
sys.path.insert(0, "/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/P45review")
from graphs import pg23_incidence, diamond_primitive, euler_ice, loop_update, cycles_of_length, girth
from brute_rs import rs_energy
nv, edges, _ = pg23_incidence()
rng = random.Random(23)
n = euler_ice(nv, edges)
confs = []
for c in range(5):
    for _ in range(rng.randrange(1, 50)):
        loop_update(nv, edges, n, rng)
    confs.append(list(n))
for a in (F(0), F(1, 4)):
    vals = []
    for nc in confs:
        t = time.time()
        E = rs_energy(edges, nc, F(1), [a] * len(edges), 8)
        vals.append(E)
        print(json.dumps(dict(alpha=str(a), E8_per_V=str(E[8] / nv), E6_per_V=str(E[6] / nv),
                              odd7=str(E[7]), secs=round(time.time() - t, 1))), flush=True)
    print(f"alpha={a}: h^8 diagonal identical over {len(vals)} states: {all(v[8] == vals[0][8] for v in vals)}", flush=True)
nv5, e5, _ = diamond_primitive(5)
print("prim5 girth", girth(nv5, e5), "V", nv5)
c8 = cycles_of_length(nv5, e5, 8)
c6 = cycles_of_length(nv5, e5, 6)
print("prim5 elementary 6-cycles", len(c6), "8-cycles", len(c8), "per vertex 8-cycles", F(len(c8), nv5))
