"""UNT 0441 (Claude2 lane) -- independent fixtures for project_density_map (0438 batched density-map extension).

FIXTURE HELPER ONLY. This script neither writes nor reviews the author's module; it loads a module from a file
path given on the command line and checks the named function against small manufactured inputs at the FULL
public shape (72 radii x 32 nodes x 8 coefficients; V/VR/VZ (2304, 576)). numpy only; synthetic data only; no
project data, no project runs, no I/O except an optional exclusive-create JSON report (--out).

Binding inputs: 0441 addendum sha256 a5cab71ad8a296760c5cab455c8b56a18fe61344e1189bc19d57a10b99cc5987 (Claude2
section) and parent 0438 sha256 83c963759f875285ce0b33148de1684318cbb81aa4658e1128bede3fe76a5c4c.

Equations under test (0441; '@' there is the mathematical product):
    M = V^H (W V)
    B = VR^H ((W rho) xi_R) - 1j*mode V^H ((W rho / R) xi_phi) + VZ^H ((W rho) xi_z)      column-wise
    M coefficients = B   (72 independent 8x8 blocks, multiple RHS, RHS columns in blocks of rhs_batch_size)
    G = V coefficients;  residual = M coefficients - B;  mass_j = sum_l W_l G[l, j] (complex, not forced to 0)

Sections
  C0  lane-convention scan (AST of the module text): no @ / dot / matmul / vdot / inner / tensordot / multi_dot /
      linalg.norm, every einsum has optimize=False, no errstate(...='ignore') / seterr / warnings 'ignore',
      no inv / pinv / lstsq / tensorinv / tensorsolve / matrix_power.
  C1  load (inert: no stdout) and signature (12 keyword-only required names, no defaults, no *args/**kwargs).
  C2  (1) independent dense reference (full 576x576 M and B assembled by einsum, dense solve; test only) on a
      synthetic block-diagonal V, modes 0..8, nfree in {1,3,7}, rhs_batch_size in {1,2,nfree,nfree+5}; plus
      solve-structure evidence from a numpy.linalg.solve spy: 72*ceil(nfree/bs) calls, each (8,8) x (8,k<=bs),
      each (block,batch) once, multiple RHS used, identical mass block across batches, no inv/pinv/lstsq;
      an einsum spy counts how often each 8x8 mass block is produced (must be exactly once per call).
  C3  (2) per-column equality with the vector function project_density (c2v002 if it and
      CHECK_0438_V002_DELTA.md exist, else c2v001), called column by column.
  C4  (3) modal sign / conjugation: analytic azimuthal case xi_phi = R (V A0) / rho gives coefficients exactly
      -1j*mode*A0 (a +1j variant must differ); mode 0 gives exact zero; +1j and conj(xi) reference variants
      differ from the module; B(1j xi) = 1j B(xi); mode scaling.
  C5  (4) failure prefixes: singular mass block k (one zeroed V column), injected LinAlgError at solve call N,
      finite-input overflow under the caller's default errstate and under errstate(all='raise'): no exception,
      fail-closed status, reported completed (block,batch) set == pairs actually solved (spy), no solve after
      the failure, retained coefficients == independent per-block reference. Injected KeyboardInterrupt: INFO
      if it propagates; if a result is returned, its status must be failed_closed* or contain "interrupt" and
      the same retention checks apply.
  C6  (5) malformed inputs rejected with ZERO solves (xi shape mismatch, real-dtype xi, nfree 0,
      rhs_batch_size 0/-1/bool/float/None/str, ...); missing/positional/extra arguments raise TypeError.
  C7  misc: batch-size invariance, inputs unmodified, finite data computes under errstate(all='raise'),
      module file unchanged after the run.

Result lines are PASS / FAIL / UNRESOLVED (a result key or format the fixture could not identify; supply
--keymap) / INFO. Exit 0 only when there is no FAIL and no UNRESOLVED.

Run (python3 -I -B; numpy is appended from the user site, see --numpy-site):
  /usr/bin/python3 -I -B fixtures_0438_map_c2v001.py <module_path> project_density_map \
      [--keymap '{"coefficients": "a", ...}' | --keymap keymap.json] [--out report.json] [--timeout 300]
      [--expect-sha256 HEX]
Keymap concepts: status_success, status_rejected_prefix, status_failed_prefix, coefficients, G, B, residual,
residual_block_norm, residual_column_norm, mass_integral, sv_min, sv_max, singular_values, cond, B_terms,
completed_pairs, completed_pairs_format (pairs|mask|batch_to_blocks|block_to_batches), retained_coefficients,
failed_block, failed_batch.
"""
import sys

sys.dont_write_bytecode = True  # never write __pycache__ next to the module under test

import argparse  # noqa: E402
import ast  # noqa: E402
import contextlib  # noqa: E402
import hashlib  # noqa: E402
import importlib.util  # noqa: E402
import inspect  # noqa: E402
import io  # noqa: E402
import json  # noqa: E402
import os  # noqa: E402
import signal  # noqa: E402
import time  # noqa: E402
import traceback  # noqa: E402
import warnings  # noqa: E402

DEFAULT_NUMPY_SITE = "/Users/bgm/Library/Python/3.9/lib/python/site-packages"
ARTIFACT_DIR = "/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/free_surface_density_projection_0438"
V001 = "free_surface_density_projection_c2v001.py"
V001_SHA = "b07fd00875e90e92c396b31103f3306dd8d85fbb1a10a44725f809a1553c6112"
V002 = "free_surface_density_projection_c2v002.py"
V002_GATE = "CHECK_0438_V002_DELTA.md"
FORBIDDEN_PREFIX = "/Users/bgm/Research/Universal Network Theory"

NB, NN, NC = 72, 32, 8
NROW, NCOL = NB * NN, NB * NC
EXPECTED_PARAMS = ("value", "partial_R", "partial_z", "weights", "radius", "rho", "xi_R", "xi_phi", "xi_z",
                   "mode", "provenance", "rhs_batch_size")
# 0441 lists 12 names for the map (the 11 vector names + rhs_batch_size).

TOL_REF = 1e-10      # module vs independent dense reference (coefficients, G, diagnostics)
TOL_B = 1e-12        # B vs reference
TOL_VEC = 1e-11      # map column j vs vector function
TOL_INV = 1e-13      # batch-size invariance
TOL_INTERNAL = 1e-12  # module self-consistency (G = V coef, residual, mass)

ALIASES = {
    "coefficients": ("coefficients", "coefficient_map", "coeffs", "a", "A", "a_map"),
    "G": ("G", "g", "G_map", "delta_rho", "delta_rho_map"),
    "B": ("B", "b", "B_map", "b_map", "rhs", "partial_B"),
    "residual": ("residual", "residuals", "residual_map", "direct_residual"),
    "residual_block_norm": ("residual_block_norm", "residual_block_norms", "residual_block_column_norm",
                            "residual_norm_per_block", "block_residual_norm", "residual_norm_block"),
    "residual_column_norm": ("residual_column_norm", "residual_column_norms", "residual_norm_per_column",
                             "column_residual_norm", "residual_col_norm", "residual_norm_column"),
    "mass_integral": ("mass_integral", "mass_integrals", "dot_W_G", "dot_W_delta_rho", "complex_mass_integral",
                      "mass_integral_per_column"),
    "sv_min": ("block_singular_value_min", "block_sv_min", "sv_min", "singular_value_min"),
    "sv_max": ("block_singular_value_max", "block_sv_max", "sv_max", "singular_value_max"),
    "singular_values": ("block_singular_values", "singular_values", "block_sv"),
    "cond": ("block_condition_number", "block_condition_numbers", "condition_number", "condition_numbers",
             "block_cond", "cond"),
    "B_terms": ("B_terms", "b_terms"),
    "completed_pairs": ("completed_block_batch", "completed_block_batch_indices", "completed_block_batch_pairs",
                        "completed_pairs", "completed_indices", "completed"),
    "retained_coefficients": ("solved_coefficients", "retained_coefficients", "partial_coefficients",
                              "coefficients_partial", "coefficients", "coefficient_map", "a"),
    "failed_block": ("failed_block",),
    "failed_batch": ("failed_batch",),
}

RESULTS = []
KEYMAP = {}
np = None
ORIG = {}


class FixtureTimeout(BaseException):
    pass


def rec(kind, tag, detail=""):
    RESULTS.append({"kind": kind, "tag": tag, "detail": detail})
    print("%-10s %s %s" % (kind, tag, detail), flush=True)


def chk(tag, cond, detail=""):
    rec("PASS" if cond else "FAIL", tag, detail)
    return bool(cond)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def g(x):
    return "%.3g" % x


# ----------------------------------------------------------------------------------------------------------------
# small numeric helpers (no BLAS in the fixture's own reference either: einsum(optimize=False) throughout)
# ----------------------------------------------------------------------------------------------------------------
def nrm(x):
    x = np.asarray(x)
    return float(np.sqrt(np.sum(np.abs(x) ** 2)))


def rel_cols(X, Y):
    X = np.asarray(X)
    Y = np.asarray(Y)
    if X.ndim == 1:
        X = X[:, None]
        Y = Y[:, None]
    num = np.sqrt(np.sum(np.abs(X - Y) ** 2, axis=0))
    den = np.sqrt(np.sum(np.abs(Y) ** 2, axis=0))
    den = np.where(den > 0, den, 1.0)
    return float(np.max(num / den)) if num.size else 0.0


def nbatches(nf, bs):
    return -(-nf // bs)


def batch_cols(t, nf, bs):
    return list(range(t * bs, min(nf, (t + 1) * bs)))


def blk(i):
    return slice(NC * i, NC * (i + 1))


# ----------------------------------------------------------------------------------------------------------------
# synthetic inputs at full public shape
# ----------------------------------------------------------------------------------------------------------------
def build_base(seed=20261016):
    rng = np.random.default_rng(seed)
    leg = np.polynomial.legendre
    x, wz = leg.leggauss(NN)
    P = leg.legvander(x, NC - 1)                     # (32, 8)
    D = np.zeros((NN, NC))
    for a in range(NC):
        c = np.zeros(NC)
        c[a] = 1.0
        D[:, a] = leg.legval(x, leg.legder(c))
    V4 = np.zeros((NB, NN, NB, NC))
    VZ4 = np.zeros((NB, NN, NB, NC))
    for i in range(NB):
        T = np.eye(NC) + 0.2 * np.triu(rng.standard_normal((NC, NC)), 1)
        V4[i, :, i, :] = np.einsum("la,ab->lb", P, T, optimize=False)
        VZ4[i, :, i, :] = 3.0 * np.einsum("la,ab->lb", D, T, optimize=False)
    V = V4.reshape(NROW, NCOL)
    VZ = VZ4.reshape(NROW, NCOL)
    # VZ need not be block diagonal: add sparse off-block entries
    rows = rng.integers(0, NROW, 600)
    cols = rng.integers(0, NCOL, 600)
    for r, c in zip(rows, cols):
        if c // NC != r // NN:
            VZ[r, c] += 0.01 * rng.standard_normal()
    VR = 0.3 * rng.standard_normal((NROW, NCOL))     # dense (spline-coupled in the source)
    Ri = 0.25 + 0.05 * np.arange(NB)
    wr = 0.04 + 0.01 * rng.random(NB)
    W = ((wr * Ri)[:, None] * wz[None, :]).reshape(-1)
    R = np.repeat(Ri, NN)
    rho = 0.5 + 1.5 * rng.random(NROW)
    return {"V": V, "VR": VR, "VZ": VZ, "W": W, "R": R, "rho": rho}


def make_xi(nf, seed):
    rng = np.random.default_rng(seed)
    return tuple(rng.standard_normal((NROW, nf)) + 1j * rng.standard_normal((NROW, nf)) for _ in range(3))


class Ref:
    """Independent dense reference: full M (576x576) and B by einsum, dense solve (test only)."""

    def __init__(self, base, V=None):
        self.base = base
        self.V = base["V"] if V is None else V
        W = base["W"]
        self.M = np.einsum("li,lj->ij", self.V.conj(), W[:, None] * self.V, optimize=False)
        self.Mb = np.stack([self.M[blk(i), blk(i)] for i in range(NB)])
        mask = np.zeros((NCOL, NCOL), bool)
        for i in range(NB):
            mask[blk(i), blk(i)] = True
        self.offblock_max = float(np.max(np.abs(self.M[~mask])))
        sv = np.stack([np.linalg.svd(self.Mb[i], compute_uv=False) for i in range(NB)])
        self.sv_min = sv.min(axis=1)
        self.sv_max = sv.max(axis=1)
        self.cond = np.array([self.sv_max[i] / self.sv_min[i] if self.sv_min[i] > 0 else np.inf
                              for i in range(NB)])

    def rhs(self, xR, xP, xZ, mode, sign=-1.0, conj_xi=False):
        b = self.base
        if conj_xi:
            xR, xP, xZ = xR.conj(), xP.conj(), xZ.conj()
        Wr = b["W"] * b["rho"]
        tr = np.einsum("li,lj->ij", b["VR"].conj(), Wr[:, None] * xR, optimize=False)
        ta = (sign * 1j * mode) * np.einsum("li,lj->ij", self.V.conj(), (Wr / b["R"])[:, None] * xP,
                                            optimize=False)
        tz = np.einsum("li,lj->ij", b["VZ"].conj(), Wr[:, None] * xZ, optimize=False)
        return tr + ta + tz, {"radial": tr, "azimuthal": ta, "vertical": tz}

    def solve_dense(self, B):
        return np.linalg.solve(self.M.astype(np.complex128), B)

    def G(self, coef):
        return np.einsum("ij,jk->ik", self.V, coef, optimize=False)

    def mass(self, G):
        return np.einsum("l,lk->k", self.base["W"], G, optimize=False)


def args_for(base, xi, mode, bs, prov="fixture-0441-synthetic", V=None):
    return dict(value=base["V"] if V is None else V, partial_R=base["VR"], partial_z=base["VZ"],
                weights=base["W"], radius=base["R"], rho=base["rho"], xi_R=xi[0], xi_phi=xi[1], xi_z=xi[2],
                mode=mode, provenance=prov, rhs_batch_size=bs)


# ----------------------------------------------------------------------------------------------------------------
# instrumentation: numpy.linalg.solve spy (+ traps for inv / pinv / lstsq / tensorinv / tensorsolve)
# ----------------------------------------------------------------------------------------------------------------
TRAPPED = ("inv", "pinv", "lstsq", "tensorinv", "tensorsolve", "matrix_power")


class Spy:
    def __init__(self, inject_at=None, inject_exc=None):
        self.calls = []
        self.trapped = []
        self.einsum_results = []
        self.inject_at = inject_at
        self.inject_exc = inject_exc

    def solve(self, a, b, *args, **kw):
        n = len(self.calls) + 1
        r = {"A": np.array(a, copy=True), "b": np.array(b, copy=True), "returned": False, "finite": False,
             "exc": None}
        self.calls.append(r)
        if self.inject_at == n:
            r["exc"] = "injected %s" % type(self.inject_exc).__name__
            raise self.inject_exc
        try:
            x = ORIG["solve"](a, b, *args, **kw)
        except BaseException as exc:
            r["exc"] = "%s: %s" % (type(exc).__name__, exc)
            raise
        r["returned"] = True
        r["finite"] = bool(np.all(np.isfinite(x)))
        return x

    def einsum(self, *args, **kw):
        r = ORIG["einsum"](*args, **kw)
        if isinstance(r, np.ndarray) and r.shape in ((NCOL, NCOL), (NB, NC, NC), (NC, NC)):
            self.einsum_results.append(np.array(r, copy=True))
        return r

    def trap(self, name):
        def f(*args, **kw):
            self.trapped.append(name)
            return ORIG[name](*args, **kw)
        return f


@contextlib.contextmanager
def instrument(module, spy):
    lin = np.linalg
    saved_mod = {}
    try:
        lin.solve = spy.solve
        np.einsum = spy.einsum
        for nm in TRAPPED:
            if nm in ORIG:
                setattr(lin, nm, spy.trap(nm))
        if module is not None:
            for k, v in list(vars(module).items()):
                if v is ORIG["solve"]:
                    saved_mod[k] = v
                    setattr(module, k, spy.solve)
                elif v is ORIG["einsum"]:
                    saved_mod[k] = v
                    setattr(module, k, spy.einsum)
                else:
                    for nm in TRAPPED:
                        if nm in ORIG and v is ORIG[nm]:
                            saved_mod[k] = v
                            setattr(module, k, spy.trap(nm))
        yield spy
    finally:
        lin.solve = ORIG["solve"]
        np.einsum = ORIG["einsum"]
        for nm in TRAPPED:
            if nm in ORIG:
                setattr(lin, nm, ORIG[nm])
        for k, v in saved_mod.items():
            setattr(module, k, v)


def call_map(fn, module, kwargs, spy=None, errstate=None, warn_error=False):
    spy = spy or Spy()
    out, exc = None, None
    with warnings.catch_warnings(record=True) as wl:
        warnings.simplefilter("error" if warn_error else "always")
        ctx = np.errstate(**errstate) if errstate else contextlib.nullcontext()
        try:
            with ctx, instrument(module, spy):
                out = fn(**kwargs)
        except FixtureTimeout:
            raise
        except BaseException as e:  # noqa: B902 -- the fixture must observe KeyboardInterrupt too
            exc = e
    return out, exc, [str(w.message) for w in wl], spy


# ----------------------------------------------------------------------------------------------------------------
# result-key resolution
# ----------------------------------------------------------------------------------------------------------------
def st_success():
    return KEYMAP.get("status_success", "computed")


def is_success(out):
    return isinstance(out, dict) and out.get("status") == st_success()


def is_rejected(out):
    return isinstance(out, dict) and isinstance(out.get("status"), str) and \
        out["status"].startswith(KEYMAP.get("status_rejected_prefix", "rejected"))


def is_failed_closed(out):
    return isinstance(out, dict) and isinstance(out.get("status"), str) and \
        out["status"].startswith(KEYMAP.get("status_failed_prefix", "failed_closed"))


def resolve(out, concept, valid):
    names = (KEYMAP[concept],) if concept in KEYMAP else ALIASES.get(concept, ())
    for k in names:
        if k in out and out[k] is not None:
            v = out[k]
            try:
                if valid(v):
                    return k, v
            except Exception:
                pass
    return None, None


def arr_shape(shape, kinds="fc"):
    def f(v):
        return isinstance(v, np.ndarray) and v.shape == shape and v.dtype.kind in kinds
    return f


def keys_summary(out):
    parts = []
    for k in sorted(out):
        v = out[k]
        if isinstance(v, np.ndarray):
            parts.append("%s:ndarray%s/%s" % (k, v.shape, v.dtype))
        elif isinstance(v, (list, tuple)):
            parts.append("%s:%s[%d]" % (k, type(v).__name__, len(v)))
        else:
            parts.append("%s:%s" % (k, type(v).__name__))
    return ", ".join(parts)


def unresolved(tag, concept, out):
    rec("UNRESOLVED", tag, "result key for '%s' not identified (supply --keymap); keys: %s"
        % (concept, keys_summary(out)))


def accept_keys(out):
    return [k for k in out if "accept" in str(k).lower()] if isinstance(out, dict) else []


def _int_like(x):
    return isinstance(x, (int, np.integer)) and not isinstance(x, (bool, np.bool_))


def normalize_pairs(out, n_batches):
    """Return (set of (block, batch), description) or (None, reason)."""
    fmt = KEYMAP.get("completed_pairs_format")
    if "completed_pairs" in KEYMAP:
        cands = [KEYMAP["completed_pairs"]]
    else:
        cands = list(ALIASES["completed_pairs"]) + sorted(
            k for k in out if "complet" in str(k).lower() and k not in ALIASES["completed_pairs"])
    for k in cands:
        if k not in out or out[k] is None:
            continue
        v = out[k]
        kl = str(k).lower()
        # explicit pairs: sequence of length-2 integer items (or empty)
        if fmt in (None, "pairs") and isinstance(v, (list, tuple, np.ndarray)) and not isinstance(v, dict):
            try:
                if len(v) == 0:
                    return set(), "%s (pairs, empty)" % k
                items = [tuple(p) for p in v]
                if all(len(p) == 2 and _int_like(p[0]) and _int_like(p[1]) for p in items):
                    return set((int(p[0]), int(p[1])) for p in items), "%s (pairs)" % k
                bad = [p for p in items if not (len(p) == 2 and _int_like(p[0]) and _int_like(p[1]))]
                if len(bad) < len(items):
                    return None, "%s holds %d non-integer pair entries, first %r" % (k, len(bad), bad[0])
            except TypeError:
                pass
        # boolean mask
        if fmt in (None, "mask") and isinstance(v, np.ndarray) and v.dtype == bool and v.ndim == 2:
            if v.shape == (NB, n_batches):
                return set((int(i), int(t)) for i, t in zip(*np.nonzero(v))), "%s (mask block x batch)" % k
            if v.shape == (n_batches, NB):
                return set((int(i), int(t)) for t, i in zip(*np.nonzero(v))), "%s (mask batch x block)" % k
        if isinstance(v, dict):
            f = fmt
            if f is None:
                if "by_batch" in kl or "per_batch" in kl:
                    f = "batch_to_blocks"
                elif "by_block" in kl or "per_block" in kl:
                    f = "block_to_batches"
            try:
                if f == "batch_to_blocks":
                    return set((int(i), int(t)) for t, bl in v.items() for i in bl), "%s (batch->blocks)" % k
                if f == "block_to_batches":
                    return set((int(i), int(t)) for i, bt in v.items() for t in bt), "%s (block->batches)" % k
            except (TypeError, ValueError):
                pass
    return None, "no interpretable completed (block,batch) record"


def retained_lookup(out, nf, bs):
    """Return (key, f) with f(i, t) -> (8, k) retained coefficients or None."""
    names = (KEYMAP["retained_coefficients"],) if "retained_coefficients" in KEYMAP \
        else ALIASES["retained_coefficients"]
    for k in names:
        v = out.get(k)
        if v is None:
            continue
        if isinstance(v, np.ndarray) and v.ndim == 2 and v.shape[1] == nf and v.shape[0] % NC == 0 \
                and v.shape[0] <= NCOL:
            K = v.shape[0] // NC

            def f(i, t, v=v, K=K):
                if i >= K:
                    return None
                return v[blk(i), batch_cols(t, nf, bs)]
            return k, f
        if isinstance(v, dict) and v:
            def f(i, t, v=v):
                x = v.get((i, t))
                if x is None:
                    return None
                x = np.asarray(x)
                return x[:, None] if x.ndim == 1 else x
            return k, f
    return None, None


# ----------------------------------------------------------------------------------------------------------------
# solve-call analysis
# ----------------------------------------------------------------------------------------------------------------
def match_block(A, Mb):
    if A.shape != (NC, NC) or not np.all(np.isfinite(A)):
        return None
    d = np.max(np.abs(Mb - A[None]), axis=(1, 2))
    sc = np.max(np.abs(Mb), axis=(1, 2))
    i = int(np.argmin(d / sc))
    return i if d[i] <= 1e-10 * sc[i] else None


def match_cols(b2, Bi):
    nf = Bi.shape[1]
    finB = np.all(np.isfinite(Bi), axis=0)
    sc = np.max(np.abs(np.where(np.isfinite(Bi), Bi, 0)), axis=0) + 1e-300
    cols = []
    for c in range(b2.shape[1]):
        v = b2[:, c]
        if np.all(np.isfinite(v)):
            cand = [j for j in range(nf) if finB[j] and np.max(np.abs(Bi[:, j] - v)) <= 1e-10 * sc[j]]
        else:
            cand = [j for j in range(nf) if not finB[j]]
        cols.append(cand[0] if len(cand) == 1 else None)
    return cols


def analyze_calls(spy, Mb, Bref, nf, bs):
    infos = []
    for c in spy.calls:
        A, b = c["A"], c["b"]
        b2 = b[:, None] if b.ndim == 1 else b
        info = {"A_shape": A.shape, "b_shape": b.shape, "block": None, "cols": None, "batch": None,
                "ok": c["returned"] and c["finite"], "exc": c["exc"]}
        info["block"] = match_block(A, Mb)
        if info["block"] is not None and b2.ndim == 2 and b2.shape[0] == NC:
            cols = match_cols(b2, Bref[blk(info["block"]), :])
            info["cols"] = cols
            if cols and None not in cols:
                t = cols[0] // bs
                if cols == batch_cols(t, nf, bs):
                    info["batch"] = t
        infos.append(info)
    return infos


def actually_completed(infos, nf, bs):
    solved = {}
    for inf in infos:
        if inf["ok"] and inf["block"] is not None and inf["cols"] and None not in inf["cols"]:
            solved.setdefault(inf["block"], set()).update(inf["cols"])
    done = set()
    for i, cs in solved.items():
        for t in range(nbatches(nf, bs)):
            if set(batch_cols(t, nf, bs)) <= cs:
                done.add((i, t))
    return done


def formation_counts(spy, M, Mb):
    """How many times each 8x8 mass block was produced by numpy.einsum during one call (full M, stacked
    (72,8,8) blocks, or single (8,8) blocks are recognised by value against the reference)."""
    cnt = np.zeros(NB, dtype=int)
    for r in spy.einsum_results:
        if not np.all(np.isfinite(r)):
            continue
        if r.shape == (NCOL, NCOL):
            if np.max(np.abs(r - M)) <= 1e-10 * np.max(np.abs(M)):
                cnt += 1
        elif r.shape == (NB, NC, NC):
            if np.max(np.abs(r - Mb)) <= 1e-10 * np.max(np.abs(Mb)):
                cnt += 1
        else:
            i = match_block(r, Mb)
            if i is not None:
                cnt[i] += 1
    return cnt


def structure_problems(spy, infos, nf, bs):
    T = nbatches(nf, bs)
    p = []
    if len(spy.calls) != NB * T:
        p.append("solve calls %d != 72*ceil(nfree/bs)=%d" % (len(spy.calls), NB * T))
    badshape = [k for k, inf in enumerate(infos)
                if inf["A_shape"] != (NC, NC) or not (inf["b_shape"] == (NC,) or (
                    len(inf["b_shape"]) == 2 and inf["b_shape"][0] == NC and 1 <= inf["b_shape"][1] <= bs))]
    if badshape:
        k = badshape[0]
        p.append("%d calls with shape other than (8,8)x(8,k<=%d); first A%s b%s"
                 % (len(badshape), bs, infos[k]["A_shape"], infos[k]["b_shape"]))
    pairs = [(inf["block"], inf["batch"]) for inf in infos]
    unm = sum(1 for q in pairs if q[0] is None or q[1] is None)
    if unm:
        p.append("%d calls not mapped to one (block, whole batch) of the reference" % unm)
    mp = [q for q in pairs if q[0] is not None and q[1] is not None]
    if len(set(mp)) != len(mp):
        p.append("duplicate (block,batch) solves")
    missing = set((i, t) for i in range(NB) for t in range(T)) - set(mp)
    if missing:
        p.append("%d (block,batch) pairs never solved" % len(missing))
    if bs >= 2 and nf >= 2 and not any(len(inf["b_shape"]) == 2 and inf["b_shape"][1] >= 2 for inf in infos):
        p.append("no multiple-RHS solve although rhs_batch_size>=2 and nfree>=2")
    first_A = {}
    for c, inf in zip(spy.calls, infos):
        i = inf["block"]
        if i is None:
            continue
        if i in first_A:
            if not (first_A[i].shape == c["A"].shape and np.array_equal(first_A[i], c["A"])):
                p.append("mass block %d differs between batches" % i)
                break
        else:
            first_A[i] = c["A"]
    if spy.trapped:
        p.append("forbidden linalg calls: %s" % sorted(set(spy.trapped)))
    return p


# ----------------------------------------------------------------------------------------------------------------
# sections
# ----------------------------------------------------------------------------------------------------------------
def c0_convention(src):
    tree = ast.parse(src)
    blas = ("dot", "matmul", "vdot", "inner", "tensordot", "multi_dot", "einsum_path")
    forb = ("inv", "pinv", "lstsq", "tensorinv", "tensorsolve", "matrix_power")
    found = {"matmul_op": [], "blas": [], "norm": [], "einsum_bad": [], "einsum_ok": 0, "errstate_ignore": [],
             "errstate_other": [], "seterr": [], "warn_ignore": [], "forbidden_linalg": [], "imports": set(),
             "isfinite": 0, "catch_warnings": []}
    for node in ast.walk(tree):
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.MatMult):
            found["matmul_op"].append(node.lineno)
        if isinstance(node, ast.AugAssign) and isinstance(node.op, ast.MatMult):
            found["matmul_op"].append(node.lineno)
        if isinstance(node, ast.Import):
            for a in node.names:
                found["imports"].add(a.name.split(".")[0])
        if isinstance(node, ast.ImportFrom) and node.module:
            found["imports"].add(node.module.split(".")[0])
            for a in node.names:
                if a.name in blas or a.name in forb:
                    found["blas" if a.name in blas else "forbidden_linalg"].append(node.lineno)
        if isinstance(node, ast.Call):
            fn = node.func
            name = fn.attr if isinstance(fn, ast.Attribute) else (fn.id if isinstance(fn, ast.Name) else None)
            if name in blas:
                found["blas"].append(node.lineno)
            elif name == "norm":
                found["norm"].append(node.lineno)
            elif name in forb:
                found["forbidden_linalg"].append(node.lineno)
            elif name == "einsum":
                opt = [kw for kw in node.keywords if kw.arg == "optimize"]
                if len(opt) == 1 and isinstance(opt[0].value, ast.Constant) and opt[0].value.value is False:
                    found["einsum_ok"] += 1
                else:
                    found["einsum_bad"].append(node.lineno)
            elif name == "errstate":
                vals = [kw.value.value for kw in node.keywords if isinstance(kw.value, ast.Constant)]
                (found["errstate_ignore"] if "ignore" in vals else found["errstate_other"]).append(node.lineno)
            elif name in ("seterr", "seterrcall"):
                found["seterr"].append(node.lineno)
            elif name in ("simplefilter", "filterwarnings"):
                a0 = node.args[0] if node.args else None
                if isinstance(a0, ast.Constant) and a0.value == "ignore":
                    found["warn_ignore"].append(node.lineno)
            elif name == "catch_warnings":
                found["catch_warnings"].append(node.lineno)
            elif name == "isfinite":
                found["isfinite"] += 1
    chk("C0.no_matmul_operator", not found["matmul_op"], "lines %s" % found["matmul_op"])
    chk("C0.no_blas_calls", not found["blas"], "dot/matmul/vdot/inner/tensordot/multi_dot lines %s" % found["blas"])
    chk("C0.no_linalg_norm", not found["norm"],
        "norm lines %s (numpy.linalg.norm uses BLAS dot internally; c2v002 precedent)" % found["norm"])
    chk("C0.einsum_optimize_False", not found["einsum_bad"] and found["einsum_ok"] > 0,
        "einsum ok=%d, without optimize=False at lines %s" % (found["einsum_ok"], found["einsum_bad"]))
    chk("C0.no_fp_suppression", not (found["errstate_ignore"] or found["seterr"] or found["warn_ignore"]),
        "errstate('ignore') %s, seterr %s, warnings-ignore %s"
        % (found["errstate_ignore"], found["seterr"], found["warn_ignore"]))
    chk("C0.no_inv_pinv_lstsq", not found["forbidden_linalg"], "lines %s" % found["forbidden_linalg"])
    rec("INFO", "C0.imports", "%s; errstate(non-ignore) lines %s; catch_warnings lines %s; isfinite calls %d"
        % (sorted(found["imports"]), found["errstate_other"], found["catch_warnings"], found["isfinite"]))


def c1_load(path, fname):
    before = set(sys.modules)
    buf_o, buf_e = io.StringIO(), io.StringIO()
    spec = importlib.util.spec_from_file_location("unt0441_map_under_test", path)
    mod = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(buf_o), contextlib.redirect_stderr(buf_e), \
            warnings.catch_warnings(record=True) as wl:
        warnings.simplefilter("always")
        spec.loader.exec_module(mod)
    new = sorted(m for m in set(sys.modules) - before if not m.startswith("numpy"))
    chk("C1.inert_import", buf_o.getvalue() == "" and buf_e.getvalue() == "" and not wl,
        "stdout %d chars, stderr %d chars, warnings %d" % (len(buf_o.getvalue()), len(buf_e.getvalue()), len(wl)))
    rec("INFO", "C1.new_non_numpy_modules_on_import", str(new))
    fn = getattr(mod, fname, None)
    if not chk("C1.function_present", callable(fn), fname):
        return mod, None
    sig = inspect.signature(fn)
    ps = list(sig.parameters.values())
    names = [p.name for p in ps]
    chk("C1.parameter_names", sorted(names) == sorted(EXPECTED_PARAMS), "got %s" % names)
    chk("C1.all_keyword_only_required",
        all(p.kind == p.KEYWORD_ONLY and p.default is p.empty for p in ps), str(sig))
    return mod, fn


def check_success_run(tag, out, exc, spy, ref, base, xi, mode, nf, bs, with_struct=True):
    """(1) module vs independent dense reference + structure evidence. Returns coefficient array or None."""
    if not chk(tag + ".status", exc is None and is_success(out),
               "exc=%r status=%r reason=%r" % (exc, out.get("status") if isinstance(out, dict) else None,
                                               out.get("reason") if isinstance(out, dict) else None)):
        return None
    Bref, terms = ref.rhs(*xi, mode)
    cref = ref.solve_dense(Bref)
    Gref = ref.G(cref)
    mref = ref.mass(Gref)
    kc, coef = resolve(out, "coefficients", arr_shape((NCOL, nf), "c"))
    kG, G = resolve(out, "G", arr_shape((NROW, nf), "c"))
    kB, B = resolve(out, "B", arr_shape((NCOL, nf), "c"))
    if coef is None:
        unresolved(tag + ".coefficients", "coefficients", out)
    else:
        chk(tag + ".coefficients_vs_dense", rel_cols(coef, cref) <= TOL_REF,
            "key=%s rel=%s" % (kc, g(rel_cols(coef, cref))))
    if G is None:
        unresolved(tag + ".G", "G", out)
    else:
        chk(tag + ".G_vs_dense", rel_cols(G, Gref) <= TOL_REF, "key=%s rel=%s" % (kG, g(rel_cols(G, Gref))))
        if coef is not None:
            gi = ref.G(coef)
            chk(tag + ".G_eq_V_coefficients", rel_cols(G, gi) <= TOL_INTERNAL, "rel=%s" % g(rel_cols(G, gi)))
    if B is None:
        unresolved(tag + ".B", "B", out)
    else:
        chk(tag + ".B_vs_dense", rel_cols(B, Bref) <= TOL_B, "key=%s rel=%s" % (kB, g(rel_cols(B, Bref))))
    kr, res = resolve(out, "residual", arr_shape((NCOL, nf), "c"))
    if res is None:
        unresolved(tag + ".residual", "residual", out)
    elif coef is not None and B is not None:
        direct = np.einsum("ij,jk->ik", ref.M, coef, optimize=False) - B
        scale = np.sqrt(np.sum(np.abs(B) ** 2, axis=0)) + 1e-300
        d = float(np.max(np.sqrt(np.sum(np.abs(res - direct) ** 2, axis=0)) / scale))
        small = float(np.max(np.sqrt(np.sum(np.abs(res) ** 2, axis=0)) / scale))
        chk(tag + ".residual_is_direct_M_coef_minus_B", d <= TOL_INTERNAL and small <= TOL_REF,
            "key=%s |res-(Mc-B)|/|B|=%s |res|/|B|=%s" % (kr, g(d), g(small)))
        # norms
        kbn, bn = resolve(out, "residual_block_norm", lambda v: isinstance(np.asarray(v), np.ndarray) and
                          np.asarray(v).shape in ((NB,), (NB, nf), (nf, NB)))
        kcn, cn = resolve(out, "residual_column_norm", lambda v: np.asarray(v).shape == (nf,))
        rb = np.sqrt(np.sum(np.abs(res.reshape(NB, NC, nf)) ** 2, axis=1))     # (72, nf)
        rc = np.sqrt(np.sum(np.abs(res) ** 2, axis=0))
        ok = True
        det = []
        if bn is None:
            unresolved(tag + ".residual_block_norm", "residual_block_norm", out)
        else:
            bn = np.asarray(bn, dtype=float)
            if bn.shape == (NB, nf):
                exp = rb
            elif bn.shape == (nf, NB) and nf != NB:
                exp = rb.T
            else:
                exp = np.sqrt(np.sum(rb ** 2, axis=1))
            e = float(np.max(np.abs(bn - exp))) / (float(np.max(exp)) + 1e-300)
            ok = ok and e <= 1e-8
            det.append("block %s shape%s rel=%s" % (kbn, bn.shape, g(e)))
        if cn is None:
            unresolved(tag + ".residual_column_norm", "residual_column_norm", out)
        else:
            cn = np.asarray(cn, dtype=float)
            e = float(np.max(np.abs(cn - rc))) / (float(np.max(rc)) + 1e-300)
            ok = ok and e <= 1e-8
            det.append("column %s rel=%s" % (kcn, g(e)))
        if bn is not None or cn is not None:
            chk(tag + ".residual_norms_consistent", ok, "; ".join(det))
    km, mass = resolve(out, "mass_integral", lambda v: np.asarray(v).shape == (nf,))
    if mass is None:
        unresolved(tag + ".mass_integral", "mass_integral", out)
    else:
        mass = np.asarray(mass)
        sc = np.einsum("l,lk->k", base["W"], np.abs(Gref), optimize=False) + 1e-300
        e_ref = float(np.max(np.abs(mass - mref) / sc))
        e_int = float(np.max(np.abs(mass - ref.mass(G)) / sc)) if G is not None else float("nan")
        chk(tag + ".mass_integral", np.iscomplexobj(mass) and e_ref <= TOL_REF and
            (G is None or e_int <= TOL_INTERNAL),
            "key=%s complex=%s vs ref %s vs W.G_module %s; |mass|/scale max %s (not forced to 0)"
            % (km, np.iscomplexobj(mass), g(e_ref), g(e_int), g(float(np.max(np.abs(mref) / sc)))))
    # block diagnostics
    ks1, smin = resolve(out, "sv_min", arr_shape((NB,), "f"))
    ks2, smax = resolve(out, "sv_max", arr_shape((NB,), "f"))
    if smin is None or smax is None:
        k3, svs = resolve(out, "singular_values", arr_shape((NB, NC), "f"))
        if svs is not None:
            smin, smax, ks1, ks2 = svs.min(axis=1), svs.max(axis=1), k3 + ".min", k3 + ".max"
    kcd, cond = resolve(out, "cond", arr_shape((NB,), "f"))
    if smin is None or smax is None:
        unresolved(tag + ".sv_range", "sv_min/sv_max", out)
    else:
        e = max(float(np.max(np.abs(smin - ref.sv_min) / ref.sv_min)),
                float(np.max(np.abs(smax - ref.sv_max) / ref.sv_max)))
        chk(tag + ".block_sv_range", e <= TOL_REF, "keys=%s,%s rel=%s" % (ks1, ks2, g(e)))
    if cond is None:
        unresolved(tag + ".cond", "cond", out)
    else:
        e = float(np.max(np.abs(cond - ref.cond) / ref.cond))
        chk(tag + ".block_condition_number", e <= TOL_REF, "key=%s rel=%s (range %s..%s)"
            % (kcd, g(e), g(float(ref.cond.min())), g(float(ref.cond.max()))))
    chk(tag + ".no_acceptance_key", not accept_keys(out), str(accept_keys(out)))
    if with_struct:
        infos = analyze_calls(spy, ref.Mb, Bref, nf, bs)
        probs = structure_problems(spy, infos, nf, bs)
        widths = sorted(set(inf["b_shape"][1] if len(inf["b_shape"]) == 2 else 1 for inf in infos))
        chk(tag + ".solve_structure", not probs,
            "calls=%d widths=%s %s" % (len(spy.calls), widths, "; ".join(probs)))
        cnt = formation_counts(spy, ref.M, ref.Mb)
        if int(cnt.sum()) == 0:
            rec("INFO", tag + ".mass_block_formation", "not observed through numpy.einsum (formation count "
                "unverifiable dynamically; identical-block evidence is in solve_structure)")
        else:
            chk(tag + ".mass_blocks_formed_once", bool(np.all(cnt == 1)),
                "einsum-observed formations per block: min %d max %d (%d einsum results recognised)"
                % (int(cnt.min()), int(cnt.max()), len(spy.einsum_results)))
    return coef


def c2_reference(fn, mod, base, ref):
    grid = []
    c = 0
    for nf in (1, 3, 7):
        for bs in sorted({1, 2, nf, nf + 5}):
            for m in ((2 * c) % 9, (2 * c + 1) % 9):
                grid.append((nf, bs, m))
            c += 1
    xis = {nf: make_xi(nf, 100 + nf) for nf in (1, 3, 7)}
    modes_seen = set()
    for nf, bs, m in grid:
        tag = "C2.nf%d.bs%d.m%d" % (nf, bs, m)
        out, exc, wl, spy = call_map(fn, mod, args_for(base, xis[nf], m, bs))
        check_success_run(tag, out, exc, spy, ref, base, xis[nf], m, nf, bs)
        if wl:
            rec("INFO", tag + ".warnings", "%d: %s" % (len(wl), wl[:2]))
        modes_seen.add(m)
    rec("INFO", "C2.coverage", "%d runs; modes %s; nfree {1,3,7}; rhs_batch_size {1,2,nfree,nfree+5}; "
        "reference M off-block max |.| = %s" % (len(grid), sorted(modes_seen), g(ref.offblock_max)))
    # batch-size invariance on one fixed input
    nf, m = 7, 6
    coefs = {}
    for bs in (1, 2, 7, 12):
        tag = "C7.invariance.nf7.m6.bs%d" % bs
        out, exc, wl, spy = call_map(fn, mod, args_for(base, xis[nf], m, bs))
        coefs[bs] = check_success_run(tag, out, exc, spy, ref, base, xis[nf], m, nf, bs)
    if all(coefs[b] is not None for b in coefs):
        e = max(rel_cols(coefs[b], coefs[7]) for b in coefs)
        bit = all(np.array_equal(coefs[b], coefs[7]) for b in coefs)
        chk("C7.batch_size_invariance", e <= TOL_INV, "max rel vs bs=7: %s; bitwise identical: %s" % (g(e), bit))
    return xis


def load_vector():
    p2 = os.path.join(ARTIFACT_DIR, V002)
    gate = os.path.join(ARTIFACT_DIR, V002_GATE)
    if os.path.exists(p2) and os.path.exists(gate):
        path, why = p2, "c2v002 and %s exist" % V002_GATE
    else:
        path, why = os.path.join(ARTIFACT_DIR, V001), "c2v001 (c2v002 present=%s, %s present=%s)" % (
            os.path.exists(p2), V002_GATE, os.path.exists(gate))
    h = sha256_file(path)
    if os.path.exists(gate):
        why += "; %s sha256 %s" % (V002_GATE, sha256_file(gate))
    rec("INFO", "C3.vector_module", "%s sha256 %s; %s" % (path, h, why))
    if path.endswith(V001):
        chk("C3.vector_c2v001_hash", h == V001_SHA, h)
    spec = importlib.util.spec_from_file_location("unt0438_vector_reference", path)
    vm = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(vm)
    return vm, path, h


def c3_vector(fn, mod, base, ref, xis):
    vm, vpath, vh = load_vector()
    cases = [(3, 2, 3), (1, 1, 0), (7, 7, 8), (7, 12, 5), (3, 1, 1)]
    for nf, bs, m in cases:
        tag = "C3.nf%d.bs%d.m%d" % (nf, bs, m)
        xi = xis[nf]
        out, exc, wl, spy = call_map(fn, mod, args_for(base, xi, m, bs))
        if not chk(tag + ".map_status", exc is None and is_success(out), "exc=%r" % exc):
            continue
        kc, coef = resolve(out, "coefficients", arr_shape((NCOL, nf), "c"))
        kG, G = resolve(out, "G", arr_shape((NROW, nf), "c"))
        kB, B = resolve(out, "B", arr_shape((NCOL, nf), "c"))
        kr, res = resolve(out, "residual", arr_shape((NCOL, nf), "c"))
        km, mass = resolve(out, "mass_integral", lambda v: np.asarray(v).shape == (nf,))
        kt, terms = resolve(out, "B_terms", lambda v: isinstance(v, dict))
        ks1, smin = resolve(out, "sv_min", arr_shape((NB,), "f"))
        ks2, smax = resolve(out, "sv_max", arr_shape((NB,), "f"))
        kcd, cond = resolve(out, "cond", arr_shape((NB,), "f"))
        worst = {"a": 0.0, "delta_rho": 0.0, "b": 0.0, "residual": 0.0, "dot_W": 0.0, "diag": 0.0, "terms": 0.0}
        bitwise = True
        vec_ok = True
        for j in range(nf):
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")  # fixture side only: c2v001's BLAS products may flag spuriously
                vo = vm.project_density(value=base["V"], partial_R=base["VR"], partial_z=base["VZ"],
                                        weights=base["W"], radius=base["R"], rho=base["rho"],
                                        xi_R=np.ascontiguousarray(xi[0][:, j]),
                                        xi_phi=np.ascontiguousarray(xi[1][:, j]),
                                        xi_z=np.ascontiguousarray(xi[2][:, j]), mode=m, provenance="fixture-0441")
            if vo.get("status") != "computed":
                vec_ok = False
                continue
            if coef is not None:
                worst["a"] = max(worst["a"], rel_cols(coef[:, j], vo["a"]))
                bitwise = bitwise and np.array_equal(coef[:, j], vo["a"])
            if G is not None:
                worst["delta_rho"] = max(worst["delta_rho"], rel_cols(G[:, j], vo["delta_rho"]))
            if B is not None:
                worst["b"] = max(worst["b"], rel_cols(B[:, j], vo["b"]))
            if res is not None:
                worst["residual"] = max(worst["residual"],
                                        nrm(res[:, j] - vo["residual"]) / (nrm(vo["b"]) + 1e-300))
            if mass is not None:
                sc = float(np.einsum("l,l->", base["W"], np.abs(vo["delta_rho"]), optimize=False)) + 1e-300
                worst["dot_W"] = max(worst["dot_W"], abs(complex(np.asarray(mass)[j]) - vo["dot_W_delta_rho"]) / sc)
            if terms is not None:
                for tk in ("radial", "azimuthal", "vertical"):
                    if tk in terms and isinstance(terms[tk], np.ndarray) and terms[tk].shape == (NCOL, nf):
                        worst["terms"] = max(worst["terms"], rel_cols(terms[tk][:, j], vo["b_terms"][tk])
                                             if nrm(vo["b_terms"][tk]) > 0 else nrm(terms[tk][:, j]))
            if smin is not None and smax is not None and cond is not None:
                worst["diag"] = max(worst["diag"],
                                    float(np.max(np.abs(smin - vo["block_singular_value_min"]) /
                                                 vo["block_singular_value_min"])),
                                    float(np.max(np.abs(smax - vo["block_singular_value_max"]) /
                                                 vo["block_singular_value_max"])),
                                    float(np.max(np.abs(cond - vo["block_condition_number"]) /
                                                 vo["block_condition_number"])))
        chk(tag + ".vector_calls_computed", vec_ok, "%d column calls" % nf)
        for key, concept, val in (("a", "coefficients", coef), ("delta_rho", "G", G), ("b", "B", B)):
            if val is None:
                unresolved(tag + "." + key, concept, out)
            else:
                chk(tag + ".%s_per_column" % key, worst[key] <= TOL_VEC, "max rel %s" % g(worst[key]))
        if res is None:
            unresolved(tag + ".residual", "residual", out)
        else:
            chk(tag + ".residual_per_column", worst["residual"] <= TOL_VEC,
                "max |r_map - r_vec|/|b| %s (both rounding-level)" % g(worst["residual"]))
        if mass is None:
            unresolved(tag + ".mass", "mass_integral", out)
        else:
            chk(tag + ".mass_vs_dot_W_delta_rho", worst["dot_W"] <= TOL_VEC, "max rel %s" % g(worst["dot_W"]))
        if smin is not None and smax is not None and cond is not None:
            chk(tag + ".block_diagnostics_vs_vector", worst["diag"] <= TOL_VEC, "max rel %s" % g(worst["diag"]))
        if terms is not None:
            chk(tag + ".B_terms_vs_vector_b_terms", worst["terms"] <= TOL_VEC, "max rel %s" % g(worst["terms"]))
        else:
            rec("INFO", tag + ".B_terms", "map exposes no B_terms dict (optional)")
        rec("INFO", tag + ".bitwise_coefficients_equal_vector", str(bitwise))


def c4_modal(fn, mod, base, ref):
    rng = np.random.default_rng(4411)
    nf, bs = 3, 2
    A0 = np.empty((NCOL, nf), complex)
    A0[:, 0] = rng.standard_normal(NCOL)
    A0[:, 1] = rng.standard_normal(NCOL)
    A0[:, 2] = rng.standard_normal(NCOL) + 1j * rng.standard_normal(NCOL)
    VA = np.einsum("ij,jk->ik", base["V"], A0, optimize=False)
    xP = base["R"][:, None] * VA / base["rho"][:, None]
    z = np.zeros((NROW, nf), complex)
    for m in (1, 3, 8):
        tag = "C4.analytic_azimuthal.m%d" % m
        out, exc, wl, spy = call_map(fn, mod, args_for(base, (z, xP, z), m, bs))
        if not chk(tag + ".status", exc is None and is_success(out), "exc=%r" % exc):
            continue
        kc, coef = resolve(out, "coefficients", arr_shape((NCOL, nf), "c"))
        if coef is None:
            unresolved(tag, "coefficients", out)
            continue
        e_minus = rel_cols(coef, -1j * m * A0)
        e_plus = rel_cols(coef, +1j * m * A0)
        chk(tag + ".coefficients_eq_minus_i_m_A0", e_minus <= TOL_REF,
            "rel to -1j*m*A0 %s; rel to +1j*m*A0 %s (must differ)" % (g(e_minus), g(e_plus)))
        chk(tag + ".plus_i_variant_differs", e_plus >= 1.0, "rel %s" % g(e_plus))
        kG, G = resolve(out, "G", arr_shape((NROW, nf), "c"))
        if G is not None:
            chk(tag + ".G_eq_minus_i_m_VA0", rel_cols(G, -1j * m * VA) <= TOL_REF, "rel %s" % g(rel_cols(G, -1j * m * VA)))
    out, exc, wl, spy = call_map(fn, mod, args_for(base, (z, xP, z), 0, bs))
    if chk("C4.analytic_azimuthal.m0.status", exc is None and is_success(out), "exc=%r" % exc):
        kc, coef = resolve(out, "coefficients", arr_shape((NCOL, nf), "c"))
        kB, B = resolve(out, "B", arr_shape((NCOL, nf), "c"))
        if coef is None:
            unresolved("C4.analytic_azimuthal.m0", "coefficients", out)
        else:
            chk("C4.analytic_azimuthal.m0.exact_zero", float(np.max(np.abs(coef))) == 0.0 and
                (B is None or float(np.max(np.abs(B))) == 0.0),
                "max|coef| %s max|B| %s" % (g(float(np.max(np.abs(coef)))),
                                             g(float(np.max(np.abs(B)))) if B is not None else "n/a"))
    # general case: +1j and conj(xi) variants differ; complex linearity; mode scaling
    xi = make_xi(nf, 777)
    m = 5
    Bm, termsm = ref.rhs(*xi, m)
    Bp, _ = ref.rhs(*xi, m, sign=+1.0)
    Bc, _ = ref.rhs(*xi, m, conj_xi=True)
    out, exc, wl, spy = call_map(fn, mod, args_for(base, xi, m, bs))
    out_i, exc_i, _, _ = call_map(fn, mod, args_for(base, tuple(1j * x for x in xi), m, bs))
    if chk("C4.general.m5.status", exc is None and is_success(out) and exc_i is None and is_success(out_i),
           "exc=%r/%r" % (exc, exc_i)):
        kB, B = resolve(out, "B", arr_shape((NCOL, nf), "c"))
        _, Bi = resolve(out_i, "B", arr_shape((NCOL, nf), "c"))
        if B is None or Bi is None:
            unresolved("C4.general.m5.B", "B", out)
        else:
            gap = nrm(Bp - Bm)
            chk("C4.general.m5.B_eq_minus_sign_reference", rel_cols(B, Bm) <= TOL_B,
                "rel %s" % g(rel_cols(B, Bm)))
            chk("C4.general.m5.plus_sign_variant_differs", nrm(B - Bp) >= 0.5 * gap,
                "|B-B(+1j)| %s vs |B(+1j)-B(-1j)| %s" % (g(nrm(B - Bp)), g(gap)))
            chk("C4.general.m5.conj_xi_variant_differs", nrm(B - Bc) >= 0.5 * nrm(Bc - Bm),
                "|B-B(conj xi)| %s vs gap %s" % (g(nrm(B - Bc)), g(nrm(Bc - Bm))))
            chk("C4.general.m5.complex_linear_B(1j xi)=1j B(xi)", rel_cols(Bi, 1j * B) <= TOL_B,
                "rel %s" % g(rel_cols(Bi, 1j * B)))
        kt, terms = resolve(out, "B_terms", lambda v: isinstance(v, dict))
        if terms is not None and isinstance(terms.get("azimuthal"), np.ndarray):
            chk("C4.general.m5.azimuthal_term", rel_cols(terms["azimuthal"], termsm["azimuthal"]) <= TOL_B,
                "key=%s rel %s" % (kt, g(rel_cols(terms["azimuthal"], termsm["azimuthal"]))))
        else:
            rec("INFO", "C4.general.m5.azimuthal_term", "no B_terms['azimuthal'] exposed (optional)")
    # mode scaling on azimuthal-only random xi_phi
    xr = make_xi(nf, 778)[1]
    o1, e1, _, _ = call_map(fn, mod, args_for(base, (z, xr, z), 1, bs))
    o4, e4, _, _ = call_map(fn, mod, args_for(base, (z, xr, z), 4, bs))
    if chk("C4.mode_scaling.status", e1 is None and e4 is None and is_success(o1) and is_success(o4)):
        _, c1 = resolve(o1, "coefficients", arr_shape((NCOL, nf), "c"))
        _, c4 = resolve(o4, "coefficients", arr_shape((NCOL, nf), "c"))
        if c1 is None or c4 is None:
            unresolved("C4.mode_scaling", "coefficients", o1)
        else:
            chk("C4.mode_scaling.coef(m=4)=4coef(m=1)", rel_cols(c4, 4 * c1) <= TOL_REF,
                "rel %s" % g(rel_cols(c4, 4 * c1)))


def check_failure(tag, out, exc, spy, Mb, Bref, nf, bs, singular_block=None, expect_exc=False):
    if expect_exc:
        if exc is not None:
            rec("INFO", tag + ".propagated", "%s propagated from the module (no result object to inspect); "
                "solve calls before it: %d" % (type(exc).__name__, len(spy.calls)))
            return
        rec("INFO", tag + ".caught", "module returned status=%r" % (out.get("status") if isinstance(out, dict)
                                                                    else type(out).__name__))
    else:
        if not chk(tag + ".no_exception", exc is None, "exc=%r" % (exc,)):
            return
    st = out.get("status") if isinstance(out, dict) else None
    ok_status = is_failed_closed(out) or (expect_exc and isinstance(st, str) and "interrupt" in st.lower())
    if not chk(tag + ".status_failed_closed", ok_status, "status=%r reason=%r"
               % (st, out.get("reason") if isinstance(out, dict) else None)):
        return
    chk(tag + ".no_acceptance_key", not accept_keys(out), str(accept_keys(out)))
    rec("INFO", tag + ".arrays_in_failure_result", ", ".join(
        "%s%s" % (k, v.shape) for k, v in sorted(out.items(), key=lambda kv: str(kv[0]))
        if isinstance(v, np.ndarray)))
    infos = analyze_calls(spy, Mb, Bref, nf, bs)
    actual = actually_completed(infos, nf, bs)
    bad_idx = [k for k, inf in enumerate(infos) if not inf["ok"]]
    if bad_idx:
        chk(tag + ".no_solve_after_failure", bad_idx[0] == len(infos) - 1,
            "first failing solve call %d of %d (%s)" % (bad_idx[0] + 1, len(infos), infos[bad_idx[0]]["exc"]))
        fail_pair = (infos[bad_idx[0]]["block"], infos[bad_idx[0]]["batch"])
    else:
        fail_pair = None
        rec("INFO", tag + ".no_failing_solve_call", "failure decided outside numpy.linalg.solve; %d solve calls"
            % len(infos))
    T = nbatches(nf, bs)
    comp, how = normalize_pairs(out, T)
    if comp is None:
        unresolved(tag + ".completed_pairs", "completed_pairs (%s)" % how, out)
        return
    chk(tag + ".completed_pairs_eq_actually_solved", comp == actual,
        "%s: reported %d, actually solved %d; reported-not-solved %s; solved-not-reported %s"
        % (how, len(comp), len(actual), sorted(comp - actual)[:4], sorted(actual - comp)[:4]))
    o1 = [(i, t) for i in range(NB) for t in range(T)]
    o2 = [(i, t) for t in range(T) for i in range(NB)]
    p1, p2 = comp == set(o1[:len(comp)]), comp == set(o2[:len(comp)])
    order = ("prefix of both block-major and batch-major order" if p1 and p2 else
             "block-major prefix" if p1 else "batch-major prefix" if p2 else "not a canonical prefix")
    rec("INFO", tag + ".completed_order", "%d of %d pairs; %s; failing pair %s" % (len(comp), NB * T, order,
                                                                                   fail_pair))
    if singular_block is not None:
        chk(tag + ".singular_block_not_completed", all(i != singular_block for i, t in comp),
            "block %d" % singular_block)
    for kk, pos in (("failed_block", 0), ("failed_batch", 1)):
        k, v = resolve(out, kk, lambda v: True)
        if k is not None and fail_pair is not None and fail_pair[pos] is not None:
            chk(tag + "." + kk, _int_like(v) and int(v) == fail_pair[pos], "reported %r, failing call %r"
                % (v, fail_pair[pos]))
        elif k is not None:
            rec("INFO", tag + "." + kk, "reported %r" % (v,))
    if comp:
        kr, look = retained_lookup(out, nf, bs)
        if look is None:
            unresolved(tag + ".retained_coefficients", "retained_coefficients", out)
        else:
            worst, missing = 0.0, 0
            for (i, t) in sorted(comp):
                cols = batch_cols(t, nf, bs)
                x = look(i, t)
                if x is None or not np.all(np.isfinite(x)):
                    missing += 1
                    continue
                xr = ORIG["solve"](Mb[i].astype(complex), Bref[blk(i), :][:, cols])
                worst = max(worst, rel_cols(x, xr))
            chk(tag + ".retained_coefficients_eq_reference", missing == 0 and worst <= TOL_REF,
                "key=%s pairs=%d missing/nonfinite=%d max rel %s" % (kr, len(comp), missing, g(worst)))
        kB, B = resolve(out, "B", arr_shape((NCOL, nf), "c"))
        done_t = sorted(set(t for _, t in comp))
        if B is not None:
            cols = [c for t in done_t for c in batch_cols(t, nf, bs)]
            chk(tag + ".retained_B_for_completed_batches", rel_cols(B[:, cols], Bref[:, cols]) <= TOL_B,
                "key=%s batches %s rel %s" % (kB, done_t, g(rel_cols(B[:, cols], Bref[:, cols]))))
        else:
            rec("INFO", tag + ".retained_B", "no B array retained in the failure result")
    else:
        rec("INFO", tag + ".retained", "no completed pairs (failure before any solve)")


def c5_failures(fn, mod, base, ref):
    # singular mass blocks
    for k, nf, bs, m in ((0, 3, 2, 2), (37, 3, 2, 2), (71, 7, 1, 7), (37, 7, 2, 4)):
        Vs = base["V"].copy()
        Vs[NN * k:NN * (k + 1), NC * k + 3] = 0.0
        rs = Ref(base, Vs)
        xi = make_xi(nf, 300 + k + nf)
        Bref, _ = rs.rhs(*xi, m)
        tag = "C5.singular_block%d.nf%d.bs%d" % (k, nf, bs)
        out, exc, wl, spy = call_map(fn, mod, args_for(base, xi, m, bs, V=Vs))
        check_failure(tag, out, exc, spy, rs.Mb, Bref, nf, bs, singular_block=k)
    # injected LinAlgError at solve call N
    nf, bs, m = 3, 2, 6
    xi = make_xi(nf, 500)
    Bref, _ = ref.rhs(*xi, m)
    total = NB * nbatches(nf, bs)
    for N in (1, 75, total):
        tag = "C5.injected_LinAlgError_call%d.nf%d.bs%d" % (N, nf, bs)
        spy = Spy(inject_at=N, inject_exc=np.linalg.LinAlgError("fixture-injected failure"))
        out, exc, wl, spy = call_map(fn, mod, args_for(base, xi, m, bs), spy=spy)
        check_failure(tag, out, exc, spy, ref.Mb, Bref, nf, bs)
    # finite-input overflow in (W*rho)*xi_z, column 2 (validation passes: every input finite)
    nf, bs, m, j = 3, 1, 3, 2
    xi = list(make_xi(nf, 600))
    rho = base["rho"].copy()
    r0 = NN * 40 + 5
    rho[r0] = 1e10
    xi[2] = xi[2].copy()
    xi[2][r0, j] = 1.7e308 + 1.7e308j
    b2 = dict(base)
    b2["rho"] = rho
    rref = Ref.__new__(Ref)
    rref.__dict__.update(ref.__dict__)
    rref.base = b2
    xi_ok = [x.copy() for x in xi]
    xi_ok[2][r0, j] = 0.0
    Bref, _ = rref.rhs(*xi_ok, m)
    Bref[:, j] = np.nan
    for label, es in (("default_errstate", None), ("errstate_raise", {"all": "raise"})):
        tag = "C5.overflow_%s.nf%d.bs%d" % (label, nf, bs)
        kw = args_for(base, tuple(xi), m, bs)
        kw["rho"] = rho
        out, exc, wl, spy = call_map(fn, mod, kw, errstate=es)
        check_failure(tag, out, exc, spy, ref.Mb, Bref, nf, bs)
        rec("INFO", tag + ".warnings", "%d recorded; status %r; fp key %r"
            % (len(wl), out.get("status") if isinstance(out, dict) else None,
               out.get("floating_point_exception") if isinstance(out, dict) else None))
    # injected KeyboardInterrupt (interruption): informative
    nf, bs, m = 3, 2, 6
    xi = make_xi(nf, 500)
    Bref, _ = ref.rhs(*xi, m)
    spy = Spy(inject_at=75, inject_exc=KeyboardInterrupt())
    out, exc, wl, spy = call_map(fn, mod, args_for(base, xi, m, bs), spy=spy)
    check_failure("C5.injected_KeyboardInterrupt_call75", out, exc, spy, ref.Mb, Bref, nf, bs, expect_exc=True)


def c6_malformed(fn, mod, base):
    nf, bs, m = 3, 2, 3
    xi = make_xi(nf, 900)
    good = args_for(base, xi, m, bs)
    cases = []

    def case(name, **over):
        kw = dict(good)
        kw.update(over)
        cases.append((name, kw))
    c = lambda shape: (np.ones(shape) + 1j * np.ones(shape))  # noqa: E731
    case("xi_phi_nfree_mismatch", xi_phi=c((NROW, 2)))
    case("xi_z_nfree_mismatch", xi_z=c((NROW, 4)))
    case("xi_R_rows_2303", xi_R=c((NROW - 1, nf)))
    case("xi_all_transposed", xi_R=xi[0].T.copy(), xi_phi=xi[1].T.copy(), xi_z=xi[2].T.copy())
    case("xi_all_1d_vectors", xi_R=xi[0][:, 0].copy(), xi_phi=xi[1][:, 0].copy(), xi_z=xi[2][:, 0].copy())
    case("xi_all_3d", xi_R=xi[0][:, :, None].copy(), xi_phi=xi[1][:, :, None].copy(), xi_z=xi[2][:, :, None].copy())
    case("xi_R_real_dtype", xi_R=xi[0].real.copy())
    case("xi_all_real_dtype", xi_R=xi[0].real.copy(), xi_phi=xi[1].real.copy(), xi_z=xi[2].real.copy())
    case("xi_phi_int_dtype", xi_phi=np.ones((NROW, nf), dtype=np.int64))
    case("xi_z_list", xi_z=xi[2].tolist())
    case("nfree_0", xi_R=c((NROW, 0)), xi_phi=c((NROW, 0)), xi_z=c((NROW, 0)))
    x = xi[1].copy()
    x[7, 1] = np.nan
    case("xi_phi_nan", xi_phi=x)
    x = xi[2].copy()
    x[100, 2] = complex(0, np.inf)
    case("xi_z_inf_imag", xi_z=x)
    for v, nm in ((0, "0"), (-1, "minus1"), (True, "True"), (False, "False"), (2.0, "float2.0"),
                  (np.float64(2.0), "npfloat2.0"), (None, "None"), ("2", "str2"), (np.bool_(True), "npbool")):
        case("rhs_batch_size_%s" % nm, rhs_batch_size=v)
    case("mode_True", mode=True)
    case("mode_9", mode=9)
    case("mode_minus1", mode=-1)
    case("mode_float", mode=2.0)
    case("provenance_empty", provenance="")
    case("provenance_blank", provenance="   ")
    case("provenance_None", provenance=None)
    Vb = base["V"].copy()
    Vb[31, 8] = 1e-3
    case("value_offblock_nonzero", value=Vb)
    case("value_complex", value=base["V"].astype(complex))
    w = base["W"].copy()
    w[10] = 0.0
    case("weights_zero_entry", weights=w)
    r = base["R"].copy()
    r[20] = -1.0
    case("radius_negative", radius=r)
    rh = base["rho"].copy()
    rh[30] = np.nan
    case("rho_nan", rho=rh)
    for name, kw in cases:
        out, exc, wl, spy = call_map(fn, mod, kw)
        chk("C6.reject.%s" % name, exc is None and is_rejected(out) and len(spy.calls) == 0 and not spy.trapped,
            "status=%r field=%r solves=%d exc=%r" % (out.get("status") if isinstance(out, dict) else None,
                                                     out.get("field") if isinstance(out, dict) else None,
                                                     len(spy.calls), exc))
    # TypeError on missing / positional / extra
    spy = Spy()
    kw = dict(good)
    del kw["rhs_batch_size"]
    for name, thunk in (("missing_rhs_batch_size", lambda: fn(**kw)),
                        ("positional", lambda: fn(*[good[p] for p in EXPECTED_PARAMS])),
                        ("extra_kwarg", lambda: fn(extra=1, **good))):
        raised = None
        with instrument(mod, spy):
            try:
                thunk()
            except TypeError as e:
                raised = e
            except Exception as e:  # noqa: BLE001
                raised = e
        chk("C6.typeerror.%s" % name, isinstance(raised, TypeError), repr(raised))
    chk("C6.typeerror.zero_solves", len(spy.calls) == 0, "solves=%d" % len(spy.calls))
    # informative acceptance cases
    for name, over in (("rhs_batch_size_np_int64", {"rhs_batch_size": np.int64(2)}),
                       ("rhs_batch_size_ndarray0d", {"rhs_batch_size": np.array(2)}),
                       ("xi_complex64", {"xi_R": xi[0].astype(np.complex64), "xi_phi": xi[1].astype(np.complex64),
                                         "xi_z": xi[2].astype(np.complex64)})):
        kw = dict(good)
        kw.update(over)
        out, exc, wl, spy = call_map(fn, mod, kw)
        rec("INFO", "C6.info.%s" % name, "status=%r exc=%r" % (out.get("status") if isinstance(out, dict) else None,
                                                              exc))


def c7_misc(fn, mod, base, ref):
    nf, bs, m = 3, 2, 7
    xi = make_xi(nf, 1200)
    kw = args_for(base, xi, m, bs)
    snap = {k: (v.copy() if isinstance(v, np.ndarray) else v) for k, v in kw.items()}
    o1, e1, _, _ = call_map(fn, mod, kw)
    o2, e2, _, _ = call_map(fn, mod, kw)
    unchanged = all(np.array_equal(kw[k], snap[k]) and kw[k].dtype == snap[k].dtype
                    if isinstance(snap[k], np.ndarray) else kw[k] == snap[k] for k in snap)
    chk("C7.inputs_unmodified", unchanged)
    if is_success(o1) and is_success(o2):
        _, c1 = resolve(o1, "coefficients", arr_shape((NCOL, nf), "c"))
        _, c2 = resolve(o2, "coefficients", arr_shape((NCOL, nf), "c"))
        if c1 is not None and c2 is not None:
            rec("INFO", "C7.deterministic_bitwise", str(np.array_equal(c1, c2)))
    out, exc, wl, spy = call_map(fn, mod, kw, errstate={"all": "raise"}, warn_error=True)
    chk("C7.finite_data_computes_under_errstate_raise_and_warnings_error", exc is None and is_success(out),
        "status=%r exc=%r reason=%r" % (out.get("status") if isinstance(out, dict) else None, exc,
                                        out.get("reason") if isinstance(out, dict) else None))
    if exc is None and is_success(out):
        check_success_run("C7.errstate_raise", out, exc, spy, ref, base, xi, m, nf, bs)


def main():
    ap = argparse.ArgumentParser(description="UNT 0441 fixtures for project_density_map")
    ap.add_argument("module_path")
    ap.add_argument("function_name")
    ap.add_argument("--keymap", default=None, help="JSON object or path to a .json file")
    ap.add_argument("--out", default=None, help="exclusive-create JSON report path")
    ap.add_argument("--timeout", type=int, default=300)
    ap.add_argument("--expect-sha256", default=None)
    ap.add_argument("--numpy-site", default=DEFAULT_NUMPY_SITE)
    ap.add_argument("--sections", default="C0,C1,C2,C3,C4,C5,C6,C7")
    a = ap.parse_args()
    global np, KEYMAP
    if a.numpy_site and a.numpy_site not in sys.path:
        sys.path.append(a.numpy_site)
    import numpy
    np = numpy
    ORIG["einsum"] = np.einsum
    for nm in ("solve",) + TRAPPED:
        if hasattr(np.linalg, nm):
            ORIG[nm] = getattr(np.linalg, nm)
    if a.keymap:
        txt = a.keymap
        if os.path.exists(txt):
            with open(txt) as f:
                txt = f.read()
        KEYMAP = json.loads(txt)
    if a.out:
        outp = os.path.realpath(a.out)
        if outp.startswith(FORBIDDEN_PREFIX):
            print("refusing to write under %s" % FORBIDDEN_PREFIX)
            return 2
    mpath = os.path.realpath(a.module_path)
    if mpath.startswith(FORBIDDEN_PREFIX):
        print("refusing to load a module under %s" % FORBIDDEN_PREFIX)
        return 2
    if not os.path.isfile(mpath):
        print("module file does not exist: %s" % mpath)
        return 2
    sec = set(s.strip() for s in a.sections.split(","))

    def on_alarm(signum, frame):
        raise FixtureTimeout("fixture timeout %ds" % a.timeout)
    signal.signal(signal.SIGALRM, on_alarm)
    signal.alarm(a.timeout)
    t0 = time.time()
    me = os.path.realpath(__file__)
    mh0 = sha256_file(mpath)
    rec("INFO", "S0.fixture", "%s sha256 %s" % (me, sha256_file(me)))
    rec("INFO", "S0.module_under_test", "%s sha256 %s function %s" % (mpath, mh0, a.function_name))
    rec("INFO", "S0.env", "python %s numpy %s isolated=%s dont_write_bytecode=%s keymap=%s"
        % (sys.version.split()[0], np.__version__, sys.flags.isolated, sys.dont_write_bytecode, KEYMAP))
    if a.expect_sha256:
        chk("S0.module_sha256_expected", mh0 == a.expect_sha256.lower(), "expected %s" % a.expect_sha256)
    timed_out = False
    try:
        with open(mpath) as f:
            src = f.read()
        if "C0" in sec:
            try:
                c0_convention(src)
            except Exception:
                rec("FAIL", "C0.crashed", traceback.format_exc(limit=3).replace("\n", " | "))
        mod, fn = c1_load(mpath, a.function_name)
        if fn is not None:
            base = build_base()
            ref = Ref(base)
            chk("S0.synthetic_V_block_diagonal_exact", ref.offblock_max == 0.0,
                "reference M off-block max %s; block cond range %s..%s"
                % (g(ref.offblock_max), g(float(ref.cond.min())), g(float(ref.cond.max()))))
            xis = None
            for name, f_ in (("C2", lambda: c2_reference(fn, mod, base, ref)),
                             ("C3", lambda: c3_vector(fn, mod, base, ref, xis or {n: make_xi(n, 100 + n)
                                                                                 for n in (1, 3, 7)})),
                             ("C4", lambda: c4_modal(fn, mod, base, ref)),
                             ("C5", lambda: c5_failures(fn, mod, base, ref)),
                             ("C6", lambda: c6_malformed(fn, mod, base)),
                             ("C7", lambda: c7_misc(fn, mod, base, ref))):
                if name not in sec:
                    continue
                ts = time.time()
                try:
                    r = f_()
                    if name == "C2":
                        xis = r
                except FixtureTimeout:
                    raise
                except Exception:
                    rec("FAIL", name + ".crashed", traceback.format_exc(limit=4).replace("\n", " | "))
                rec("INFO", name + ".elapsed_s", "%.1f" % (time.time() - ts))
    except FixtureTimeout as e:
        timed_out = True
        rec("FAIL", "S0.timeout", str(e))
    finally:
        signal.alarm(0)
    chk("S0.module_file_unchanged", sha256_file(mpath) == mh0, mpath)
    n = {k: sum(1 for r in RESULTS if r["kind"] == k) for k in ("PASS", "FAIL", "UNRESOLVED", "INFO")}
    verdict = "TIMEOUT" if timed_out else ("ALL_PASS" if n["FAIL"] == 0 and n["UNRESOLVED"] == 0 else
                                           ("HAS_FAIL" if n["FAIL"] else "HAS_UNRESOLVED"))
    print("SUMMARY pass=%d fail=%d unresolved=%d info=%d elapsed=%.1fs VERDICT=%s"
          % (n["PASS"], n["FAIL"], n["UNRESOLVED"], n["INFO"], time.time() - t0, verdict), flush=True)
    if a.out:
        with open(os.path.realpath(a.out), "x") as f:
            json.dump({"module": mpath, "module_sha256": mh0, "function": a.function_name, "counts": n,
                       "verdict": verdict, "results": RESULTS}, f, indent=1)
    return 0 if verdict == "ALL_PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
