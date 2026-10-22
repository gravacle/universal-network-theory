#!/usr/bin/env python3
"""Supplementary checks (Claude, independent).
 1. ED on the <=3-flip truncated space at SMALL h with Richardson extrapolation in h^2:
    recovers the exact N*c6 (the truncation adds large non-extensive h^8 terms, which is
    why the h>=0.05 table in graph_check_output.json cannot be read for c6).
 2. Positive control (girth 3, octahedron K_{2,2,2}): two ice configs (two triangles vs a
    Hamiltonian hexagon) DO differ at h^6 through triangle supports -> the pipeline detects
    configuration dependence when the counting identity's hypothesis (no short cycles) fails.
 3. Direct exact RS (no cluster decomposition) on one representative of EVERY
    (flippable-count, cycle-structure) class of PG(2,3) ice configurations, x=0 and x=1/10.
"""
import sys, json, time
from fractions import Fraction as F
import numpy as np

sys.path.insert(0, "/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/P45review")
import p45_clusters_independent as cl
import p45_graph_check as g

OUT = "/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/P45review/"
np.seterr(all="ignore")


def main():
    rep = {}
    t0 = time.time()
    n, edges = g.pg23()
    inc, nb = g.edge_adjacency(edges)
    hexes = g.six_cycles(n, edges)
    sols = g.all_two_factors(n, edges, inc)
    bykey = {}
    for s in sols:
        k = (g.flippable_count(s, hexes), tuple(g.cycle_structure(n, edges, s)))
        bykey.setdefault(k, s)
    keys = sorted(bykey)

    # ---- 1. small-h ED + Richardson ----
    rep["ED_small_h"] = {}
    for alpha in (0.0, 0.2):
        tot = cl.per_vertex(1, F(alpha).limit_denominator(100))[0]
        c2, c4, c6 = (float(tot[k]) * n for k in (2, 4, 6))
        rows_out = []
        for kk in (keys[0], keys[-1]):
            occ = bykey[kk]
            Dv, rows, cols = g.build_trunc(edges, nb, occ, 1.0, alpha)
            hs = [0.004, 0.008, 0.016]
            r = []
            for h in hs:
                E = g.lanczos_ground(Dv, rows, cols, h, nit=80)
                r.append((E - c2 * h * h - c4 * h ** 4) / h ** 6)
            # Richardson in h^2 (ratios 4): remove h^2 and h^4 corrections
            r1 = [(4 * r[0] - r[1]) / 3, (4 * r[1] - r[2]) / 3]
            r2 = (16 * r1[0] - r1[1]) / 15
            rows_out.append(dict(config=[kk[0], list(kk[1])], raw=r, richardson=r2, exact_Nc6=c6))
            print("ED x=%.2f config %s: (E-c2h2-c4h4)/h^6 at h=%s -> %s ; Richardson %.6f ; exact N*c6 %.6f"
                  % (alpha / 2, kk, hs, ["%.5f" % v for v in r], r2, c6))
        rep["ED_small_h"]["x=%.2f" % (alpha / 2)] = rows_out

    # ---- 2. positive control: octahedron ----
    no, eo = g.octahedron()
    inco, nbo = g.edge_adjacency(eo)
    print("octahedron: n=%d m=%d girth=%d" % (no, len(eo), g.girth(no, eo)))
    solso = g.all_two_factors(no, eo, inco)
    classes = {}
    for s in solso:
        classes.setdefault(tuple(g.cycle_structure(no, eo, s)), s)
    rep["octahedron"] = {"n_ice": len(solso)}
    for alpha in (F(0), F(1, 5)):
        vals = {}
        for cs, occ in classes.items():
            E = g.direct_rs(eo, nbo, occ, 1, alpha)
            S, census = g.subset_sum(eo, nbo, occ, 1, alpha)
            assert S[2] == E[2] and S[4] == E[4] and S[6] == E[6]
            vals[str(list(cs))] = dict(E2=str(E[2]), E4=str(E[4]), E6=str(E[6]), E6f=float(E[6]))
            print("  octa x=%s cycles=%s E2=%s E4=%s E6=%s (%.10f)" % (alpha / 2, list(cs), E[2], E[4], E[6], float(E[6])))
        rep["octahedron"]["x=%s" % (alpha / 2)] = vals

    # ---- 3. all classes of PG(2,3) ----
    rep["all_classes"] = []
    ref = {a: [x * n for x in cl.per_vertex(1, a)[0]] for a in (F(0), F(1, 5))}
    for kk in keys:
        occ = bykey[kk]
        row = dict(flippable=kk[0], cycles=list(kk[1]))
        for a in (F(0), F(1, 5)):
            E = g.direct_rs(edges, nb, occ, 1, a)
            ok = E[2] == ref[a][2] and E[4] == ref[a][4] and E[6] == ref[a][6]
            row["x=%s" % (a / 2)] = dict(E6=str(E[6]), equals_N_c6=ok)
            assert ok, (kk, a)
        rep["all_classes"].append(row)
        print("class flippable=%d cycles=%s: direct E2,E4,E6 == N*(c2,c4,c6) at x=0 and x=1/10" % (kk[0], list(kk[1])))
    print("all %d classes identical. %.1fs" % (len(keys), time.time() - t0))
    with open(OUT + "supplement_output.json", "w") as fh:
        json.dump(rep, fh, indent=1)


if __name__ == "__main__":
    main()
