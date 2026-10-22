"""Order-8 ring amplitude T8(x) on an alternating 8-cycle (exists in diamond: 3 elementary
8-cycles per vertex). K8 = h^8 T8(x)/(2Ud)^7. Compare x-dependence with T6.
Also confirms the 5 PG(2,3) states used in run_order8.py were distinct. Claude, P45 review."""
import sys, random
from fractions import Fraction as F
from itertools import permutations
sys.path.insert(0, "/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/P45review")
from graphs import pg23_incidence, euler_ice, loop_update, cycles_of_length

def ringT(L, Ud, alpha):
    A = 2 * Ud
    sig = [1 if i % 2 == 0 else -1 for i in range(L)]
    T = F(0)
    for perm in permutations(range(L)):
        S = set(); prod = F(1)
        for k in range(L - 1):
            S.add(perm[k])
            D = sum(A + alpha * sig[i] for i in S) + sum(2 * Ud * sig[i] * sig[(i + 1) % L] for i in S if (i + 1) % L in S)
            prod *= A / D
        T += prod
    return T
res = {}
for a in (F(0), F(1, 4), F(-1, 4), F(1, 2)):
    t6 = ringT(6, F(1), a); t8 = ringT(8, F(1), a)
    res[str(a / 2)] = (t6, t8, t8 / t6)
    print(f"x={a/2}: T6={t6} ({float(t6):.6f})  T8={t8} ({float(t8):.6f})  T8/T6={float(t8/t6):.6f}")
x0, x1 = "0", "1/8"
print("ratio of (T8/T6) between x=1/8 and x=0:", float(res[x1][2] / res[x0][2]))
nv, edges, _ = pg23_incidence()
rng = random.Random(23)
n = euler_ice(nv, edges)
hexes = cycles_of_length(nv, edges, 6)
confs = []
for c in range(5):
    for _ in range(rng.randrange(1, 50)):
        loop_update(nv, edges, n, rng)
    confs.append(tuple(n))
def flip(nc):
    cnt = 0
    for H in hexes:
        dv = {}
        for e in H:
            for v in edges[e]:
                dv[v] = dv.get(v, 0) + nc[e]
        cnt += all(x == 1 for x in dv.values())
    return cnt
print("order-8 PG(2,3) states distinct:", len(set(confs)), "of", len(confs), "flippable hexagon counts:", [flip(c) for c in confs])
