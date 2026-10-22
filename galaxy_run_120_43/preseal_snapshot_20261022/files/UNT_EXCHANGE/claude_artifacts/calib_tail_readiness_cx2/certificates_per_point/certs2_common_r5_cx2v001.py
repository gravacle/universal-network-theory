"""Shared helpers for certificates_v002 (tail_scheme_impl_c2/certificates_v002).  READ-ONLY on every input; writes only
under certificates_v002/ (exclusive create).  numpy only.

Reuses, read-only and pinned by sha, the certificates_v001 helper library certs_common_c2v001.py (1946a394): symbol route
(QINF evaluator f58de0dc reproduced bitwise), saved R3 states, I1-T on DDO states, tail-module loading, direction sets.
Its write_new() refuses any path outside certificates_v001, so this module carries its own write_new().

ENVELOPE (A52 ruling 5; CERTIFICATES_V001 sec 1 'deciding next step'):  in the batched symbol transcription
lwr_common_v001.Binder.F_of the coefficient block is F(k) = sum_abc w_a(t_0) w_b(t_1) w_c(t_2) grid[a,b,c] with
t = remainder(kp, 2 pi), kp = ell_F (k @ root(Cbar)^T) @ A_BRAVAIS, and w the L=4 Fejer weights (nonnegative, sum 1):
F is a convex combination of the 64 grid blocks indexed by a point t of the cardinal torus T^3.  The EH block depends on k
itself.  The envelope symbol q_env(k, t) = 4 gamma |k|^2 x_0 with F(t) in place of F(k) therefore contains the actual
symbol as the special case t = t(k):  sup over (direction, |k| in shell, t in T^3) of |1 - q_env| >= sup over the actual
shell of |1 - q|.  env_q() below is Binder.T_vec's arithmetic with t supplied; env_q(k, t(k)) == q_of(k) is TESTED bitwise
(tools/eps_cert_c2v005.py self-test)."""
import hashlib
import json
import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
CERT2 = HERE
import importlib.util
V001_TOOLS = HERE
V001_COMMON_PATH = HERE/'certs_common_r5_cx2v001.py'
V001_COMMON_SHA = 'c75aaa5a197efe7bde1014269d74aa37810ccce6f95b7eec1078352f09ffb3b7'
_common_raw=V001_COMMON_PATH.read_bytes()
if hashlib.sha256(_common_raw).hexdigest()!=V001_COMMON_SHA:raise ValueError('r5 common pin mismatch')
_ccspec=importlib.util.spec_from_file_location('cx2_r5_common_for_envelope',V001_COMMON_PATH)
CC=importlib.util.module_from_spec(_ccspec);sys.modules[_ccspec.name]=CC
exec(compile(_common_raw,str(V001_COMMON_PATH),'exec'),CC.__dict__)

V001 = CC.CERT
V001_RECORDS = {
    'EPS_CERT_V004': (V001 / 'gates/EPS_CERT_V004.json', 'de0dcefd8b0426bb88935cba5ba7aa1cbbd118f89f092957a051979775be2c04'),
    'EPS_CERT_K128_V004': (V001 / 'gates/EPS_CERT_K128_V004.json', '260d550394c5e663b6ed9524a71f4359859c330017e0c50ff6639560b6b3b5e3'),
    'LO_CERT_V001': (V001 / 'gates/LO_CERT_V001.json', '311cb01d79a864ba1db5c6f55fba5d3c8d3ab4efb7997664df005ca21dbde736'),
    'LO_CERT_K128_V001': (V001 / 'gates/LO_CERT_K128_V001.json', 'd92bf1349c9f223fa4edf2fcd1df1e43fc5ac2ae193e81afe9eba98a6d176d0b'),
    'LO_NGC_CERT_V001': (V001 / 'gates/LO_NGC_CERT_V001.json', '5ec9414890ad41e0c62af1b9b8b80cef533516e41d71a08517417a29ea97b36b'),
    'GQ_CERT_V001': (V001 / 'gates/GQ_CERT_V001.json', '5c71e28ef5e33d3383ae205ceb10f3d4e3a863234bd62363c7b019547c416cfc'),
    'CHECK_V001': (V001 / 'check/CHECK.md', 'a89b16d8'),
}
GATE_SCHEMA = CC.GATE_SCHEMA


def v001_record(name):
    p, want = V001_RECORDS[name]
    got = CC.sha(p)
    if not got.startswith(want):
        raise SystemExit('v001 record pin ' + name)
    return json.loads(p.read_text()), {'path': str(p), 'sha256': got}


def write_new(path, obj):
    path = Path(path)
    if CERT2 not in path.resolve().parents:
        raise SystemExit('refusing to write outside certificates_v002: %s' % path)
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = (json.dumps(obj, indent=1, allow_nan=False, sort_keys=False) + '\n').encode()
    with open(path, 'xb') as f:
        f.write(raw)
    return hashlib.sha256(raw).hexdigest()


def decisions():
    return {'frozen_pinned': CC.pin('addendum_v004_frozen'),
            'open_cited_by_name': CC.ADDENDUM_V005_CITED + ' (A48, A50, A51, A52 rulings 4-5)'}


# ------------------------------------------------------------------ envelope symbol
class Envelope:
    """q_env(k, t): Binder.T_vec arithmetic (lwr_common_v001 L110-161) with the cardinal-torus point t supplied."""

    def __init__(self, L, B):
        self.B = B; self.A = np.asarray(L.A_BRAVAIS, float)
        self.a = np.arange(B.L, dtype=float)
        self.gv = 2 * np.pi * self.a / B.L

    def t_of(self, kv_m):
        """The actual torus point of k (Binder.F_of L111-113)."""
        kr = self.B.ell * (np.atleast_2d(kv_m) @ self.B.root.T)
        return np.remainder(kr @ self.A, 2 * np.pi)

    def F_t(self, t):
        t = np.atleast_2d(np.asarray(t, float))
        a = self.a; gv = self.gv; B = self.B
        ph = np.exp(1j * a[None, None, :, None] * (t[:, :, None, None] - gv[None, None, None, :]))
        sums = ph.sum(axis=2)
        one = (sums.real ** 2 + sums.imag ** 2) / (B.L * B.L)
        return np.einsum('na,nb,nc,abcij->nij', one[:, 0], one[:, 1], one[:, 2], B.grid, optimize=True)

    def native(self, t, chunk=20000):
        t = np.atleast_2d(t); out = np.empty((len(t), 10, 10), complex)
        for lo in range(0, len(t), chunk):
            out[lo:lo + chunk] = self.B.native_from_F(self.F_t(t[lo:lo + chunk]))
        return out

    def eh_dir(self, nhat, k_ref_m):
        """EH block at |k| = k_ref_m along each unit direction (quadratic in k: eh(c k) = c^2 eh(k))."""
        kv = np.atleast_2d(nhat) * k_ref_m
        kr = self.B.ell * (kv @ self.B.root.T)
        return self.B.eh(kr)

    def q(self, kv_m, t):
        """Exact path: q_env for paired rows of kv_m (1/m) and t."""
        B = self.B
        kv = np.atleast_2d(np.asarray(kv_m, float)); t = np.atleast_2d(t)
        kr = B.ell * (kv @ B.root.T)
        tot = B.native_from_F(self.F_t(t)) + B.eh(kr)
        e0 = np.zeros((len(kv), 10, 1), complex); e0[:, 0, 0] = 1.0
        x = np.linalg.solve(tot / B.volume, -e0)
        return 4.0 * B.gam * np.sum(kv * kv, axis=1) * x[:, 0, 0]

    def dev_grid(self, Nt, Ed, ks_m, k_ref_m):
        """|1 - q_env| on the product (t-grid natives Nt [nt,10,10]) x (direction EH blocks Ed at k_ref [nd,10,10]) x ks:
        returns array [nk, nd, nt] (broadcast arithmetic; scale s = (k/k_ref)^2 on the EH block)."""
        B = self.B
        out = np.empty((len(ks_m), Ed.shape[0], Nt.shape[0]))
        e0 = np.zeros((10, 1), complex); e0[0, 0] = 1.0
        for ik, k in enumerate(ks_m):
            s = (k / k_ref_m) ** 2
            for d0 in range(0, Ed.shape[0], max(1, 40000 // Nt.shape[0])):
                d1 = min(Ed.shape[0], d0 + max(1, 40000 // Nt.shape[0]))
                tot = (Nt[None, :, :, :] + s * Ed[d0:d1, None, :, :]) / B.volume
                x = np.linalg.solve(tot.reshape(-1, 10, 10), np.broadcast_to(-e0, (tot.shape[0] * tot.shape[1], 10, 1)))
                q = 4.0 * B.gam * k * k * x[:, 0, 0]
                out[ik, d0:d1] = np.abs(1.0 - q).reshape(d1 - d0, Nt.shape[0])
        return out


def fib_sphere(n):
    i = np.arange(n) + 0.5
    z = 1 - 2 * i / n; r = np.sqrt(1 - z * z); th = math.pi * (3 - math.sqrt(5)) * i
    return np.stack([r * np.cos(th), r * np.sin(th), z], axis=1)


def fib_hemi(n):
    """n directions on the upper hemisphere (the envelope is even in the direction: EH is quadratic in k and t is free)."""
    i = np.arange(n) + 0.5
    z = 1 - i / n; r = np.sqrt(1 - z * z); th = math.pi * (3 - math.sqrt(5)) * i
    return np.stack([r * np.cos(th), r * np.sin(th), z], axis=1)


def torus_grid_v(m):
    """m^3 torus points 2 pi j / m (vertices 0 and, for even m, pi included)."""
    g = 2 * np.pi * np.arange(m) / m
    return np.stack(np.meshgrid(g, g, g, indexing='ij'), axis=-1).reshape(-1, 3)


# ------------------------------------------------------------------ envelope: full response, global grid, local refinement
def env_full(E, kv_m, t):
    """All 10 fields x = -K^-1 e_n with F(t) (Binder arithmetic; x[0] = T)."""
    B = E.B
    kv = np.atleast_2d(np.asarray(kv_m, float)); t = np.atleast_2d(t)
    kr = B.ell * (kv @ B.root.T)
    tot = B.native_from_F(E.F_t(t)) + B.eh(kr)
    e0 = np.zeros((len(kv), 10, 1), complex); e0[:, 0, 0] = 1.0
    return np.linalg.solve(tot / B.volume, -e0)[:, :, 0]


def tangent_basis(n):
    n = np.atleast_2d(n) / np.linalg.norm(np.atleast_2d(n), axis=1)[:, None]
    a = np.where(np.abs(n[:, :1]) < 0.9, np.array([[1.0, 0, 0]]), np.array([[0, 1.0, 0]]))
    e1 = a - np.sum(a * n, axis=1)[:, None] * n; e1 /= np.linalg.norm(e1, axis=1)[:, None]
    e2 = np.cross(n, e1)
    return n, e1, e2


def refine(f, p0, sig0, clip01, rng, M=48, max_it=120, tol=1e-7, grow=1.3):
    """Batched adaptive random pattern search (maximization) from S starts.  f(start_index_array, params[n,P]) -> values[n].
    clip01: indices of params clipped to [0,1].  A step is accepted only if it raises the value; the step scale halves on a
    failed iteration and grows on success; stops when every scale < tol x its initial value or after max_it iterations."""
    p = np.array(p0, float); S, P = p.shape
    fv = f(np.arange(S), p)
    sig = np.tile(np.asarray(sig0, float), (S, 1)); sig_init = sig.copy()
    it = 0
    for it in range(1, max_it + 1):
        cand = p[:, None, :] + sig[:, None, :] * rng.standard_normal((S, M, P))
        if clip01:
            cand[:, :, clip01] = np.clip(cand[:, :, clip01], 0.0, 1.0)
        sidx = np.repeat(np.arange(S), M)
        fc = f(sidx, cand.reshape(-1, P)).reshape(S, M)
        j = np.argmax(fc, axis=1); best = fc[np.arange(S), j]
        up = best > fv
        p[up] = cand[np.arange(S), j][up]; fv[up] = best[up]
        sig[~up] *= 0.5; sig[up] = np.minimum(sig[up] * grow, sig_init[up])
        if np.all(sig < tol * sig_init):
            break
    return p, fv, it


def distinct_top(vals, keys, n, min_sep):
    """Indices of the n largest vals whose keys (rows) are pairwise >= min_sep apart (max-abs)."""
    order = np.argsort(vals)[::-1]; out = []
    for i in order:
        if all(np.max(np.abs(keys[i] - keys[j])) >= min_sep for j in out):
            out.append(int(i))
        if len(out) == n:
            break
    return out


def torus_wrap_diff(a, b):
    d = np.abs(np.remainder(a - b + np.pi, 2 * np.pi) - np.pi)
    return d
