#!/usr/bin/env python3
"""Float RS on the full PG(2,3) incidence graph through h^10 (beyond the claim; Claude).

RS recursion on the space of states with <= K flipped edges relative to an ice config.
K=5 makes E_2..E_10 exact (an order-2k diagonal word never has more than k edges flipped
at once; no other ice state lies within 5 flips since girth = 6). Compares configurations
spanning the full range of flippable-hexagon counts. Purpose: test the stronger statement
that, on 4-regular girth>=6 graphs at uniform alpha, the diagonal is configuration
independent through h^10 (all supports of <=5 edges are trees whose signed embedding
counts are fixed by the 2+/2- vertex rule), so the first possible configuration-dependent
diagonal term is h^12.
"""
import sys, json, time
from itertools import combinations
from math import comb
import numpy as np

sys.path.insert(0, "/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/P45review")
import p45_graph_check as g

OUT = "/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/P45review/"


def build(m, adjmat, sig, Ud, alpha, K):
    A = 2.0 * Ud
    offsets = [0]
    combos = [np.zeros((1, 0), dtype=np.int64)]
    for r in range(1, K + 1):
        arr = np.array(list(combinations(range(m), r)), dtype=np.int64)
        combos.append(arr)
    sizes = [len(c) for c in combos]
    for r in range(1, K + 1):
        offsets.append(offsets[-1] + sizes[r - 1])
    ntot = offsets[-1] + sizes[-1]
    binom = np.array([[comb(n, k) for k in range(K + 2)] for n in range(m + 1)], dtype=np.int64)

    def colex(arr):  # arr sorted rows
        r = arr.shape[1]
        rank = np.zeros(arr.shape[0], dtype=np.int64)
        for i in range(r):
            rank += binom[arr[:, i], i + 1]
        return rank

    D = np.zeros(ntot)
    pos = [None] * (K + 1)
    pos[0] = np.array([0])
    down_from, down_to = [], []
    for r in range(1, K + 1):
        arr = combos[r]
        p = offsets[r] + colex(arr)
        pos[r] = p
        s = sig[arr]
        val = (A + alpha * s).sum(axis=1)
        for i in range(r):
            for j in range(i + 1, r):
                val += 2.0 * Ud * s[:, i] * s[:, j] * adjmat[arr[:, i], arr[:, j]]
        D[p] = val
        for j in range(r):
            sub = np.delete(arr, j, axis=1)
            q = offsets[r - 1] + (colex(sub) if r > 1 else np.zeros(len(arr), dtype=np.int64))
            down_from.append(p)
            down_to.append(q)
    down_from = np.concatenate(down_from)
    down_to = np.concatenate(down_to)
    single = offsets[1] + np.arange(m)  # colex rank of (e,) is e
    return D, down_from, down_to, single, ntot


def rs_float(D, df, dt, single, ntot, order=10):
    c = [np.zeros(ntot)]
    c[0][0] = 1.0
    E = [0.0] * (order + 1)
    invD = np.zeros(ntot)
    invD[1:] = 1.0 / D[1:]
    for n in range(1, order + 1):
        E[n] = -c[n - 1][single].sum()
        if n == order:
            break
        x = c[n - 1]
        y = np.bincount(df, weights=x[dt], minlength=ntot) + np.bincount(dt, weights=x[df], minlength=ntot)
        for k in range(1, n):
            if E[k] != 0.0:
                y += E[k] * c[n - k]
        y[0] = 0.0
        c.append(y * invD)
    return E


def main():
    t0 = time.time()
    n, edges = g.pg23()
    m = len(edges)
    inc, nb = g.edge_adjacency(edges)
    adjmat = np.zeros((m, m))
    for e in range(m):
        for f in nb[e]:
            adjmat[e, f] = 1.0
    hexes = g.six_cycles(n, edges)
    sols = g.all_two_factors(n, edges, inc)
    bykey = {}
    for s in sols:
        k = (g.flippable_count(s, hexes), tuple(g.cycle_structure(n, edges, s)))
        bykey.setdefault(k, s)
    keys = sorted(bykey)
    pick = [keys[0], keys[len(keys) // 3], keys[2 * len(keys) // 3], keys[-1]]
    res = {}
    for alpha in (0.0, 0.2):
        rows = []
        for kk in pick:
            sig = np.array([1 - 2 * o for o in bykey[kk]], dtype=float)
            D, df, dt, single, ntot = build(m, adjmat, sig, 1.0, alpha, 5)
            E = rs_float(D, df, dt, single, ntot, 10)
            rows.append(dict(config=[kk[0], list(kk[1])], E=E))
            print("x=%.2f flippable=%d cycles=%s  E2=%.15g E4=%.15g E6=%.15g E8=%.15g E10=%.15g  (dim %d, %.0fs)"
                  % (alpha / 2, kk[0], list(kk[1]), E[2], E[4], E[6], E[8], E[10], ntot, time.time() - t0))
        for k in (2, 4, 6, 8, 10):
            vals = [r["E"][k] for r in rows]
            print("   order %2d: max-min over configs = %.3e  (value %.12g)" % (k, max(vals) - min(vals), vals[0]))
        res["x=%.2f" % (alpha / 2)] = rows
    with open(OUT + "higher_order_float_output.json", "w") as fh:
        json.dump(res, fh, indent=1)


if __name__ == "__main__":
    main()
