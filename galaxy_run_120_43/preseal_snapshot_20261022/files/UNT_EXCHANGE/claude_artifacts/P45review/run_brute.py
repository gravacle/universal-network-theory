"""Driver: brute-force h^2,h^4,h^6 diagonal energies of many ice states on real girth-6
4-regular graphs; check configuration independence and compare with an independent
per-vertex cluster formula. Claude, P45 review."""
import sys, time, random, json
from fractions import Fraction as F
sys.path.insert(0, "/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/P45review")
from graphs import (diamond_primitive, diamond_conventional, pg23_incidence, girth,
                    cycles_of_length, euler_ice, loop_update, check_ice)
from brute_rs import rs_energy


def flippable(hexes, edges, n, nv):
    cnt = 0
    for H in hexes:
        # alternating <=> every hexagon vertex has exactly one occupied hexagon edge
        dv = {}
        for e in H:
            for v in edges[e]:
                dv[v] = dv.get(v, 0) + n[e]
        if all(x == 1 for x in dv.values()):
            cnt += 1
    return cnt


def polarization(edges, dirs, n):
    if dirs is None:
        return None
    vec = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]
    P = [0, 0, 0]
    for e, d in enumerate(dirs):
        s = 2 * n[e] - 1
        for t in range(3):
            P[t] += s * vec[d][t]
    return tuple(P)


def main(which, alphas, nconf, seed, Ud=F(1)):
    if which == "prim3":
        nv, edges, dirs = diamond_primitive(3)
    elif which == "conv2":
        nv, edges, dirs = diamond_conventional(2)
    elif which == "pg23":
        nv, edges, dirs = pg23_incidence()
    else:
        raise SystemExit("unknown graph")
    g = girth(nv, edges)
    hexes = cycles_of_length(nv, edges, 6)
    print(f"graph={which} V={nv} E={len(edges)} girth={g} six_cycles={len(hexes)}", flush=True)
    rng = random.Random(seed)
    n = euler_ice(nv, edges)
    confs = []
    for c in range(nconf):
        steps = 0 if c == 0 else rng.randrange(1, 60)
        for _ in range(steps):
            loop_update(nv, edges, n, rng)
        check_ice(nv, edges, n)
        confs.append(list(n))
    out = []
    for a in alphas:
        alpha_e = [F(a)] * len(edges)
        vals = []
        for c, nc in enumerate(confs):
            t = time.time()
            E = rs_energy(edges, nc, Ud, alpha_e, 6)
            row = dict(conf=c, flippable_hex=flippable(hexes, edges, nc, nv),
                       polarization=polarization(edges, dirs, nc),
                       E2_per_V=str(E[2] / nv), E4_per_V=str(E[4] / nv), E6_per_V=str(E[6] / nv),
                       odd=[str(E[1]), str(E[3]), str(E[5])], secs=round(time.time() - t, 1))
            print(json.dumps(dict(alpha=str(a), **row)), flush=True)
            vals.append(E)
        same = all(v[k] == vals[0][k] for v in vals for k in (2, 4, 6))
        print(f"alpha={a}: all {len(vals)} configurations identical at h2,h4,h6 (exact Fractions): {same}", flush=True)
        out.append(dict(alpha=str(a), identical=same, E_per_V=[str(x / nv) for x in vals[0]]))
    return out


if __name__ == "__main__":
    which = sys.argv[1]
    alphas = [F(x) for x in sys.argv[2].split(",")]
    nconf = int(sys.argv[3])
    seed = int(sys.argv[4])
    res = main(which, alphas, nconf, seed)
    print("SUMMARY", json.dumps(res))
