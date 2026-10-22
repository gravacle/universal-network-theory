"""Claude-authored side check of P-37 eq. (9) and the 8/6 nullity counts (claim ii), exact rationals.
chi_lin = (lam^2/U) L^T Pi_T(k) L on the ten coordinates (00,01,02,03,11,22,33,12,13,23);
chi_quad = b * (delta_ij - 1/3) on (11,22,33). K = -(chi_lin + chi_quad).
Ward generator G_(mu nu),c = p_mu delta_nu c + p_nu delta_mu c, static p=(0,k).
"""
from fractions import Fraction as F
import random, json, sys

COORDS = ((0, 0), (0, 1), (0, 2), (0, 3), (1, 1), (2, 2), (3, 3), (1, 2), (1, 3), (2, 3))
SLOT = {0: 9, 1: 8, 2: 7}  # e1<->h23, e2<->h13, e3<->h12


def rank(M):
    m = [r[:] for r in M]; r = 0
    for c in range(len(m[0])):
        piv = next((i for i in range(r, len(m)) if m[i][c] != 0), None)
        if piv is None: continue
        m[r], m[piv] = m[piv], m[r]
        for i in range(len(m)):
            if i != r and m[i][c] != 0:
                f = m[i][c] / m[r][c]; m[i] = [x - f * y for x, y in zip(m[i], m[r])]
        r += 1
    return r


rng = random.Random(7)
res = dict(cases=0, eq9_ok=True, nullity_lin=set(), nullity_lin_quad=set())
for _ in range(200):
    k = [F(rng.randint(-6, 6), rng.randint(1, 4)) for _ in range(3)]
    if all(v == 0 for v in k): continue
    lam = F(rng.randint(1, 9), 4); U = F(rng.randint(1, 9), 5); b = F(rng.randint(1, 9), 3)
    k2 = sum(v * v for v in k)
    Pi = [[F(i == j) - k[i] * k[j] / k2 for j in range(3)] for i in range(3)]
    for bq in (F(0), b):
        chi = [[F(0)] * 10 for _ in range(10)]
        for i in range(3):
            for j in range(3):
                chi[SLOT[i]][SLOT[j]] = lam * lam / U * Pi[i][j]
                chi[4 + i][4 + j] = bq * (F(i == j) - F(1, 3))
        K = [[-x for x in r] for r in chi]
        p = [F(0)] + k
        G = [[p[mu] * F(nu == c) + p[nu] * F(mu == c) for c in range(4)] for mu, nu in COORDS]
        W = [[sum(K[r][s] * G[s][c] for s in range(10)) for c in range(4)] for r in range(10)]
        val = W[7][3]  # row h12, generator xi=e3
        res["eq9_ok"] &= (val == 2 * lam * lam * k[0] * k[1] * k[2] / (U * k2))
        (res["nullity_lin"] if bq == 0 else res["nullity_lin_quad"]).add(10 - rank(K))
    res["cases"] += 1
res["nullity_lin"] = sorted(res["nullity_lin"]); res["nullity_lin_quad"] = sorted(res["nullity_lin_quad"])
json.dump(res, open(sys.argv[1], "w") if len(sys.argv) > 1 else sys.stdout, indent=1)
print(res)
