"""Are elementary 8-cycles of diamond flippable in typical ice states? (prim L=5 torus). Claude."""
import sys, random
sys.path.insert(0, "/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/P45review")
from graphs import diamond_primitive, euler_ice, loop_update, cycles_of_length
nv, edges, _ = diamond_primitive(5)
c6 = cycles_of_length(nv, edges, 6); c8 = cycles_of_length(nv, edges, 8)
rng = random.Random(9); n = euler_ice(nv, edges)
def flippable(cyc, n):
    out = 0
    for C in cyc:
        dv = {}
        for e in C:
            for v in edges[e]:
                dv[v] = dv.get(v, 0) + n[e]
        out += all(x == 1 for x in dv.values())
    return out
for t in range(4):
    for _ in range(400):
        loop_update(nv, edges, n, rng)
    print(f"state {t}: flippable hexagons {flippable(c6, n)}/{len(c6)}, flippable 8-cycles {flippable(c8, n)}/{len(c8)}")
