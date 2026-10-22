"""BH-D step 2: exact multivariate Taylor coefficients of <psi(T)|O|psi(T)> for H = sum_j x_j G_j.

PREREG_BHD_STEP2_V001.md (sha256 2563b31c...). Same estimator as step 1 (bhd_step1_coeffs.Cluster):
  v[mu] = coefficient of x^mu in H^|mu| psi0  (integer vectors; G_j integer, real symmetric),
  [x^sigma] <O>(T=1) = sum_{mu+nu=sigma} i^|nu| (-i)^|mu| <v_nu|O|v_mu> / (|mu|! |nu|!).
Exact arithmetic by residues modulo primes p < 2^25 and Chinese-remainder reconstruction. The number of
primes is fixed from a rigorous magnitude bound (|v| <= A elementwise, A from the same recursion with
|G_j|; |<v_nu|O|v_mu>| <= ||A_nu|| ||A_mu|| for any partial-permutation O), plus ONE redundant prime: the
reconstruction from the others must agree with it, else the run aborts.
Generators are given as lists of partial permutations (dst, src, val): (G v)[dst] += val * v[src].
"""
from fractions import Fraction as Fr
from itertools import product
from math import comb, factorial, log2, ceil
import numpy as np

PBITS = 25


def _is_prime(n):
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True


def primes_below(limit, k):
    out = []
    n = limit - 1
    while len(out) < k:
        if _is_prime(n):
            out.append(n)
        n -= 1
    return out


PRIMES = primes_below(1 << PBITS, 64)


def crt(residues, primes):
    x, M = 0, 1
    for r, p in zip(residues, primes):
        # solve x + M*t = r mod p
        t = ((int(r) - x) * pow(M, -1, p)) % p
        x += M * t
        M *= p
    if x > M // 2:
        x -= M
    return x


class Block:
    def __init__(self, dim, gens, psi0, sigmas, label=''):
        """gens: list (one per variable) of lists of (dst, src, val) int arrays; psi0: basis index;
        sigmas: list of needed monomial exponent tuples (same length as gens)."""
        self.dim, self.gens, self.label = dim, gens, label
        nv = len(gens)
        self.sigmas = sorted(set(tuple(s) for s in sigmas), key=lambda s: (sum(s), s))
        down = set()
        for s in self.sigmas:
            for mu in product(*[range(x + 1) for x in s]):
                down.add(mu)
        self.monos = sorted(down, key=lambda s: (sum(s), s))
        self.pos = {mu: i for i, mu in enumerate(self.monos)}
        nm = len(self.monos)
        # ---- rigorous float bound A >= |v|
        A = np.zeros((nm, dim))
        A[0, psi0] = 1.0
        for i, mu in enumerate(self.monos[1:], 1):
            acc = np.zeros(dim)
            for j in range(nv):
                if mu[j] == 0:
                    continue
                prev = list(mu); prev[j] -= 1
                src = A[self.pos[tuple(prev)]]
                for (d, s, val) in gens[j]:
                    acc[d] += np.abs(val) * src[s]  # d is injective within one partial permutation
            A[i] = acc * (1 + 1e-12)
        norms = np.sqrt((A * A).sum(axis=1)) * (1 + 1e-9)
        # ---- pair tables (op-independent)
        mu_i, nu_i, sg_i, ph_i, wt = [], [], [], [], []
        lbound = 0.0
        for si, s in enumerate(self.sigmas):
            n = sum(s)
            B = 0.0
            for mu in product(*[range(x + 1) for x in s]):
                nu = tuple(a - b for a, b in zip(s, mu))
                k, l = sum(mu), sum(nu)
                mu_i.append(self.pos[mu]); nu_i.append(self.pos[nu]); sg_i.append(si)
                ph_i.append((l + 3 * k) % 4); wt.append(comb(n, k))
                B += comb(n, k) * norms[self.pos[mu]] * norms[self.pos[nu]]
            if B > 0:
                lbound = max(lbound, log2(B))
        self.log2_bound = lbound
        need = ceil((lbound + 2) / (PBITS - 1)) + 1  # +1 redundant
        self.primes = PRIMES[:max(2, need)]
        self.mu_i, self.nu_i, self.sg_i = map(lambda x: np.array(x, dtype=np.int64), (mu_i, nu_i, sg_i))
        self.ph_i = np.array(ph_i, dtype=np.int64)
        self.wt = wt
        self.npairs = len(wt)
        # ---- residue vectors
        P = np.array(self.primes, dtype=np.int64)[:, None]
        self.V = []
        for p in self.primes:
            V = np.zeros((nm, dim), dtype=np.int64)
            V[0, psi0] = 1
            for i, mu in enumerate(self.monos[1:], 1):
                acc = np.zeros(dim, dtype=np.int64)
                for j in range(nv):
                    if mu[j] == 0:
                        continue
                    prev = list(mu); prev[j] -= 1
                    src = V[self.pos[tuple(prev)]]
                    for (d, s, val) in gens[j]:
                        acc[d] += val * src[s]
                V[i] = acc % p
            self.V.append(V)
        self.wt_mod = [np.array([w % p for w in wt], dtype=np.int64) for p in self.primes]
        self._cache = {}

    def expect_tgt(self, tgt, key=None, chunk=2048):
        """tgt[s] = image basis index of s under O (or -1). Returns {sigma: (Fr re, Fr im)}."""
        if key is not None and key in self._cache:
            return self._cache[key]
        src = np.nonzero(tgt >= 0)[0]
        ns = len(self.sigmas)
        res = []
        for V, p, wm in zip(self.V, self.primes, self.wt_mod):
            OV = np.zeros_like(V)
            OV[:, tgt[src]] = V[:, src]
            acc = np.zeros(ns * 4, dtype=np.int64)
            for c0 in range(0, self.npairs, chunk):
                sl = slice(c0, c0 + chunk)
                d = (V[self.nu_i[sl]] * OV[self.mu_i[sl]]).sum(axis=1) % p  # < 2^50 * dim < 2^63
                w = (d * wm[sl]) % p
                np.add.at(acc, self.sg_i[sl] * 4 + self.ph_i[sl], w)
                acc %= p
            re = (acc[0::4] - acc[2::4]) % p
            im = (acc[1::4] - acc[3::4]) % p
            res.append((re, im))
        out = {}
        pr = self.primes
        for si, s in enumerate(self.sigmas):
            vals = []
            for part in (0, 1):
                rs = [int(res[k][part][si]) for k in range(len(pr))]
                x = crt(rs[:-1], pr[:-1])
                if x % pr[-1] != rs[-1]:
                    raise RuntimeError('CRT redundancy check failed: bound or arithmetic error')
                vals.append(x)
            if vals[0] or vals[1]:
                n = sum(s)
                out[s] = (Fr(vals[0], factorial(n)), Fr(vals[1], factorial(n)))
        if key is not None:
            self._cache[key] = out
        return out
