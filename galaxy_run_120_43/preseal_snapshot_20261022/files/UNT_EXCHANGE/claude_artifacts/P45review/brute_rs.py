"""Brute-force Rayleigh-Schroedinger energy of one ice state through h^6 on a WHOLE graph.
Independent of any cluster/inclusion-exclusion argument: all flip subsets (connected or
not) up to Hamming distance 3 are kept, all folded (renormalization) terms E^(k) psi^(n-k)
are kept. H0 = Ud*sum_v (d_v-2)^2 + sum_e alpha_e*n_e ; V = -h sum_e X_e.
Exact Fractions. Claude, P45 review. No Codex code imported.
"""
from fractions import Fraction as F


def popcount(x):
    return bin(x).count("1")


def make_D(edges, n, adj, Ud, alpha_e):
    """Exact excitation energy of flipping edge set S (bitmask) from ice state n.
    Computed directly from vertex degrees (NOT from the pairwise formula), so it also
    tests the pairwise D(S) formula used in the P45 text."""
    def D(mask):
        dv = {}
        lin = F(0)
        m = mask
        while m:
            low = m & -m
            e = low.bit_length() - 1
            m ^= low
            s = 1 - 2 * n[e]
            u, v = edges[e]
            dv[u] = dv.get(u, 0) + s
            dv[v] = dv.get(v, 0) + s
            lin += alpha_e[e] * s
        return Ud * sum(x * x for x in dv.values()) + lin
    return D


def rs_energy(edges, n, Ud, alpha_e, order=6):
    """Return [E0..E_order] (coefficients of h^k) of the ice state n, non-degenerate RS
    with intermediate normalization. Valid because no other ice state lies within
    Hamming distance 3 when girth >= 4 (checked separately)."""
    adj = None
    D = make_D(edges, n, adj, Ud, alpha_e)
    ne = len(edges)
    Dcache = {}

    def Dm(mask):
        x = Dcache.get(mask)
        if x is None:
            x = D(mask)
            if x <= 0:
                raise ValueError("nonpositive denominator")
            Dcache[mask] = x
        return x
    E = [F(0)] * (order + 1)
    psi = [dict() for _ in range(order + 1)]
    psi[0][0] = F(1)
    for k in range(1, order + 1):
        # E^(k) = <0|V|psi^(k-1)> = -sum_e psi^(k-1)(e)
        E[k] = -sum((psi[k - 1].get(1 << e, F(0)) for e in range(ne)), F(0))
        if k == order:
            break
        bound = min(k, order - k)
        acc = {}
        for S, val in psi[k - 1].items():
            if not val:
                continue
            size = popcount(S)
            if size + 1 <= bound:
                for e in range(ne):
                    T = S ^ (1 << e)
                    if T:
                        acc[T] = acc.get(T, F(0)) + val
            else:
                m = S
                while m:
                    low = m & -m
                    m ^= low
                    T = S ^ low
                    if T and popcount(T) <= bound:
                        acc[T] = acc.get(T, F(0)) + val
        # folded terms E^(j) psi^(k-j)(S), S != 0
        for j in range(1, k):
            if E[j]:
                for S, val in psi[k - j].items():
                    if S and popcount(S) <= bound:
                        acc[S] = acc.get(S, F(0)) + E[j] * val
        psi[k] = {S: v / Dm(S) for S, v in acc.items() if v}
    return E
