"""UNT 0455 independent synthetic fixtures for the exact scalar-force evaluator (c2v001).

Fixture author only: this file neither writes nor reviews the module. It tests a
supplied module on SMALL SYNTHETIC inputs only. No project packet, no .npz, no
root worker, no project run, no file I/O except the JSON result in --outdir.

Usage (root interpreter, isolated, single-thread BLAS):
  VECLIB_MAXIMUM_THREADS=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -I -B fixtures_0455_c2v001.py --module PATH [--interface PATH] --outdir DIR \
      [--only T01,T02,...]

The module sha256 is computed from bytes and printed, then the module is loaded by
importlib. Public entry points are discovered from the INTERFACE file (identifiers
written as `name(` there that are public callables of the module) and bound by the
THIN ADAPTER below; nothing else in this file depends on the module's API.

ORACLE (independent of the module): a DIRECT finite sum over every supplied wave
and every supplied point, no grouping, no symmetry:
    dn(p)        = sum_q a_q exp(i (kx_q x_p + ky_q y_p + kz_q z_p))
    grad_dn(p)_j = sum_q (i k_qj) a_q exp(i k_q . x_p)
cross-checked against a pure-Python cmath double loop and against central finite
differences of the oracle itself (derivative sign convention).
Lapse (independent transcription of the 0449 linear convention):
    Nb = 1 + Re n_b,  dPhi = c^2 Re dn / Nb,
    grad dPhi = c^2 (Re grad_dn / Nb - Re dn Re grad n_b / Nb^2).
Tolerances: |module - oracle| <= REL * sum_q |a_q| (field) and
REL * sum_q |k_qj| |a_q| (gradient component j): a regrouping-roundoff bound, far
below any omitted, duplicated, reflected, sign-flipped or re-weighted term.

Adapter: InterfaceAdapter binds INTERFACE_0455_V001.md (prepare_geometry, bind_base,
exact_finite_sum, admit_scalar_force, exact_scalar_force). AssumedAdapter is the
pre-INTERFACE guess, kept only for the fixture's own mock self-test. An unresolved
API stops with ADAPTER_UNRESOLVED, never PASS.

Tests (BINDING unless marked advisory in the output):
  T00 oracle self-check: numpy direct sum == cmath loop; oracle gradient == FD (sign)
  T01 irregular anisotropic signed waves with holes, columns: scalar + 3 gradients
  T02 reordered waves      T03 exact duplicates summed; one-ulp near-duplicate kept;
      reported exact group counts      T04 sparse (mostly-hole) dense grid; single wave
  T05 nonuniform z per column, off-column points, repeated point, one point
  T06 per-component (i kx, i ky, i kz) signs; module grad == FD of module dn
  T07 complex linearity/scaling on the raw path; imaginary part retained (no .real)
  T08 linear lapse quotient + gradient vs independent computation (unit and 1e19 m
      scales); FD of module deltaPhi; c^2 exactly once; complex dn/grad retained
  T09 nonreal base/increment field/gradient rejected above, accepted below tolerance
  T10 gradient reality check scales with the supplied length, field check does not; rtol
  T11 N_b <= 0 / nonfinite rejected      T12 point/wave identity mismatch (ulp,
      reorder, drop) rejected or oracle-exact, never stale
  T13 amplitudes and base refreshed per call; in-place buffer mutation; geometry reuse
      across sources; caller mutation after prepare does not leak
  T14 dense-entry limit (below/at) and block limit (below/at) fail closed
  T15 column/point chunk invariance (advisory)      T16 caller inputs unmutated
  T17 FloatingPointError (errstate raise) and nonfinite inputs -> fail-closed dict
  T18 no Hessian array; INTERFACE says none evaluated
  T19 inert import; lane AST scan and keyword-only/no-default signatures (advisory)
  T20 synthetic signed 72^3 lattice (5184 pairs x 72 kz, no data): limit + oracle
  T21 two-stage path bitwise == one-call path; raw-result/base identity and integrity
      guards; retention on failure and 2-D point shapes (advisory)
"""
import argparse
import ast
import cmath
import hashlib
import importlib.util
import inspect
import json
import math
import os
import re
import subprocess
import sys
import tempfile
import time
import traceback

import numpy as np

REL = 1e-11            # regrouping roundoff bound, relative to the absolute-sum scale
REL_CHUNK = 1e-13      # chunk invariance
REL_FD = 1e-6          # finite-difference derivative checks
C_TEST = 3.7           # c: distinct from 1, 2, 2pi
TIGHT = 1e-9           # reality atol for intentionally real (Hermitian) synthetic fields

TASK_0455 = ('/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/'
             '0455_2026-10-16_claude2_exact_scalar_force_acceleration.md',
             'b467a0c0c6e2fe3498a44ebdecca110776528dde7b4304d204cd42e64c67062c')


def sha256_file(path):
    with open(path, 'rb') as handle:
        return hashlib.sha256(handle.read()).hexdigest()


def load_path(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# ---------------------------------------------------------------------------
# Synthetic data (fixture-owned; deterministic seeds)
# ---------------------------------------------------------------------------
KX = np.array([-2.71, -1.37, -0.413, 0.0, 0.77, 1.93, 3.07])
KY = np.array([-1.9, -0.23, 0.0, 0.61, 2.44])
KZ = np.array([-3.3, -1.1, -0.29, 0.0, 0.53, 2.2])


def make_waves(seed, *, fraction=0.4, extra_unique=4, duplicates=6, hermitian=False, kscale=1.0):
    """Irregular, anisotropic, signed waves: a random SUBSET of an uneven Cartesian
    product (holes), plus waves sharing nothing, plus exact duplicate rows with
    different amplitudes; rows permuted. Hermitian=True appends -k with conj(a)."""
    rng = np.random.default_rng(seed)
    grid = np.array([(a, b, c) for a in KX for b in KY for c in KZ])
    keep = rng.random(len(grid)) < fraction
    keep[0] = True
    waves = grid[keep]
    extra = rng.uniform(-4.0, 4.0, size=(extra_unique, 3))
    waves = np.concatenate([waves, extra])
    dup = waves[rng.choice(len(waves), size=duplicates, replace=False)]
    waves = np.concatenate([waves, dup])
    amps = rng.uniform(0.3, 1.5, len(waves)) * np.exp(1j * rng.uniform(-np.pi, np.pi, len(waves)))
    if hermitian:
        waves = np.concatenate([waves, -waves])
        amps = np.concatenate([amps, np.conj(amps)])
    perm = rng.permutation(len(waves))
    waves = np.ascontiguousarray(waves[perm] * kscale)
    amps = np.ascontiguousarray(amps[perm])
    return waves, amps


def make_points(seed, *, xscale=1.0, z_zero=False):
    """Exact-(x,y) columns with NONUNIFORM, unequal-length z lists, points not on any
    shared column, one exactly repeated point; order shuffled so columns interleave."""
    rng = np.random.default_rng(seed)
    cols = rng.uniform(-2.0, 2.0, size=(6, 2))
    lengths = [1, 2, 3, 5, 4, 7]
    pts = []
    for (cx, cy), n in zip(cols, lengths):
        zs = np.sort(rng.uniform(-1.5, 1.5, n)) if not z_zero else np.zeros(n)
        for zv in zs:
            pts.append((cx, cy, zv))
    for _ in range(5):
        pts.append(tuple(rng.uniform(-2.0, 2.0, 3)) if not z_zero
                   else tuple(list(rng.uniform(-2.0, 2.0, 2)) + [0.0]))
    pts.append(pts[3])
    pts = np.array(pts)
    if z_zero:
        pts[:, 2] = 0.0
    pts = pts[rng.permutation(len(pts))] * xscale
    return (np.ascontiguousarray(pts[:, 0]), np.ascontiguousarray(pts[:, 1]),
            np.ascontiguousarray(pts[:, 2]))


def base_field(x, y, z, *, inv=1.0, imag=0.0):
    """Analytic real base n_b and its exact Cartesian gradient (|n_b| <= 0.35)."""
    p = (0.7 * inv, -0.3 * inv, 0.45 * inv)
    q = (0.4 * inv, 0.9 * inv)
    t1 = p[0] * x + p[1] * y + p[2] * z + 0.3
    t2 = q[0] * y - q[1] * z
    nb = 0.2 * np.sin(t1) + 0.15 * np.cos(t2)
    g = np.empty((len(x), 3))
    g[:, 0] = 0.2 * np.cos(t1) * p[0]
    g[:, 1] = 0.2 * np.cos(t1) * p[1] - 0.15 * np.sin(t2) * q[0]
    g[:, 2] = 0.2 * np.cos(t1) * p[2] + 0.15 * np.sin(t2) * q[1]
    return nb.astype(complex) + 1j * imag, g.astype(complex)


# ---------------------------------------------------------------------------
# Oracle (independent direct finite sum)
# ---------------------------------------------------------------------------
def oracle(k, a, x, y, z):
    theta = (x[:, None] * k[None, :, 0] + y[:, None] * k[None, :, 1] + z[:, None] * k[None, :, 2])
    terms = np.exp(1j * theta) * a[None, :]
    dn = terms.sum(axis=1)
    grad = np.empty((len(x), 3), dtype=complex)
    for j in range(3):
        grad[:, j] = (terms * (1j * k[None, :, j])).sum(axis=1)
    return dn, grad


def oracle_loop(k, a, x, y, z):
    dn = []
    grad = []
    for p in range(len(x)):
        s = 0j
        g = [0j, 0j, 0j]
        for q in range(len(k)):
            e = cmath.exp(1j * (float(k[q, 0]) * float(x[p]) + float(k[q, 1]) * float(y[p])
                                + float(k[q, 2]) * float(z[p]))) * complex(a[q])
            s += e
            for j in range(3):
                g[j] += 1j * float(k[q, j]) * e
        dn.append(s)
        grad.append(g)
    return np.array(dn), np.array(grad)


def scales(k, a):
    fs = float(np.sum(np.abs(a)))
    gs = np.array([float(np.sum(np.abs(k[:, j]) * np.abs(a))) for j in range(3)])
    return fs, gs


def lapse_expected(dn, gdn, nb, gnb, c):
    Nb = 1.0 + nb.real
    dphi = c * c * dn.real / Nb
    gd = c * c * (gdn.real / Nb[:, None] - dn.real[:, None] * gnb.real / (Nb[:, None] ** 2))
    return Nb, dphi, gd


def err_field(got, exp, fs):
    return float(np.max(np.abs(np.asarray(got) - exp))) / fs


def err_grad(got, exp, gs):
    got = np.asarray(got)
    return max(float(np.max(np.abs(got[:, j] - exp[:, j]))) / gs[j] for j in range(3) if gs[j] > 0)


# ---------------------------------------------------------------------------
# THIN ADAPTER (the only module-API-dependent layer)
# ---------------------------------------------------------------------------
class Outcome(object):
    def __init__(self, ok, out=None, result=None, exc=None):
        self.ok, self.out, self.result, self.exc = ok, out, result, exc

    def describe(self):
        if self.exc is not None:
            return 'EXCEPTION %s: %s' % (type(self.exc).__name__, self.exc)
        if isinstance(self.result, dict):
            return 'status=%r reason=%r' % (self.result.get('status'),
                                            self.result.get('reason', self.result.get('failure')))
        return 'result type %s' % type(self.result).__name__


def vs(o):
    """COMPLETE, or REJECTED[status: short reason] so a rejection is seen to be for the tested cause."""
    if o.ok:
        return 'COMPLETE'
    if o.exc is not None:
        return 'REJECTED[exception %s: %s]' % (type(o.exc).__name__, str(o.exc)[:90])
    r = o.result if isinstance(o.result, dict) else {}
    return 'REJECTED[%s: %s]' % (r.get('status'), str(r.get('reason'))[:90])


def find_key(obj, names, depth=0):
    """First value whose key equals one of names (in order), searched breadth-first."""
    if depth > 4 or not isinstance(obj, dict):
        return None
    for n in names:
        if n in obj and obj[n] is not None:
            return obj[n]
    for v in obj.values():
        if isinstance(v, dict):
            got = find_key(v, names, depth + 1)
            if got is not None:
                return got
    return None


class Adapter(object):
    """Binds canonical calls to the module. Filled in from the INTERFACE file."""

    notes = []

    def __init__(self, module, interface_text):
        self.m = module
        self.interface_text = interface_text
        self.discovered = discover(module, interface_text)

    def complete(self, result):
        return isinstance(result, dict) and result.get('status') == 'COMPLETE'

    def prepare(self, k, x, y, z, *, limit=None, chunk=None):
        raise NotImplementedError

    def raw(self, geom, k, x, y, z, a):
        raise NotImplementedError

    def admit(self, geom, k, x, y, z, a, nb, gnb, c, length, tol, *, base_points=None, base_geom=None):
        raise NotImplementedError

    def required_dense(self, k):
        """Fixture-side dense size: unique exact (kx,ky) pairs x unique exact kz."""
        pairs = len({(float(u), float(v)) for u, v in k[:, :2]})
        kz = len({float(w) for w in k[:, 2]})
        return pairs, kz


def discover(module, text):
    names = []
    for match in re.finditer(r'`?([A-Za-z][A-Za-z0-9_]*)\s*\(', text):
        n = match.group(1)
        if n not in names and not n.startswith('_') and callable(getattr(module, n, None)):
            if inspect.isfunction(getattr(module, n)) or inspect.isclass(getattr(module, n)):
                names.append(n)
    return names


class AssumedAdapter(Adapter):
    """Assumed API (used only until the INTERFACE is read): prepare_geometry, raw_finite_sum,
    bind_base, evaluate_force; limit in dense S entries; chunk in columns."""

    def describe(self):
        return 'AssumedAdapter(prepare_geometry, raw_finite_sum, bind_base, evaluate_force)'

    def limit_for(self, k, factor):
        pairs, nkz = self.required_dense(k)
        need = pairs * nkz
        if factor == 'below':
            return need - 1
        if factor == 'exact':
            return need
        return int(math.ceil(need * factor))

    def chunk_values(self):
        return (1, 2, 3, 7, 1000)

    def reported_groups(self, g):
        geom = g.out
        if isinstance(geom, dict) and 'n_pairs' in geom and 'n_kz' in geom:
            return (geom['n_pairs'], geom['n_kz'])
        return None

    def prepare(self, k, x, y, z, *, limit=None, chunk=None):
        r = call(self.m.prepare_geometry, dict(wavevectors=k, x_m=x, y_m=y, z_m=z,
                                               max_dense_entries=limit, column_chunk=chunk))
        if isinstance(r, Outcome):
            return r
        return Outcome(self.complete(r), r.get('geometry') if isinstance(r, dict) else None, r)

    def raw(self, geom, k, x, y, z, a):
        r = call(self.m.raw_finite_sum, dict(geometry=geom, wavevectors=k, x_m=x, y_m=y, z_m=z, amplitudes=a))
        if isinstance(r, Outcome):
            return r
        out = dict(dn=find_key(r, ['dn_complex']), grad_dn=find_key(r, ['grad_dn_complex']))
        return Outcome(self.complete(r), out, r)

    def admit(self, geom, k, x, y, z, a, nb, gnb, c, length, tol, *, base_points=None, base_geom=None):
        bp = base_points if base_points is not None else (x, y, z)
        bg = base_geom if base_geom is not None else geom
        b = call(self.m.bind_base, dict(geometry=bg, x_m=bp[0], y_m=bp[1], z_m=bp[2], n_b=nb, grad_n_b=gnb))
        if isinstance(b, Outcome):
            return b
        if not self.complete(b):
            return Outcome(False, None, b)
        r = call(self.m.evaluate_force, dict(geometry=geom, base=b['base'], wavevectors=k, x_m=x, y_m=y, z_m=z,
                                             amplitudes=a, c_m_s=c, length_scale_m=length,
                                             base_reality_atol=tol['base_atol'], base_reality_rtol=tol['base_rtol'],
                                             increment_reality_atol=tol['inc_atol'],
                                             increment_reality_rtol=tol['inc_rtol']))
        if isinstance(r, Outcome):
            return r
        out = dict(dn=find_key(r, ['dn_complex']), grad_dn=find_key(r, ['grad_dn_complex']),
                   dphi=find_key(r, ['deltaPhi_m2_s2']), gdphi=find_key(r, ['grad_deltaPhi_cartesian_m_s2']),
                   Nb=find_key(r, ['Nb']))
        return Outcome(self.complete(r), out, r)


class InterfaceAdapter(AssumedAdapter):
    """Bound from INTERFACE_0455_V001.md (c2v001): prepare_geometry(wavevectors, x_m, y_m, z_m,
    max_dense_entries, max_block_entries, column_chunk, point_chunk); bind_base(n_base,
    grad_n_base, x_m, y_m, z_m); exact_finite_sum(geometry, wavevectors, amplitudes, x_m, y_m,
    z_m); admit_scalar_force(finite_sum, base, c_m_s, gradient_length_scale_m, 4 tolerances);
    exact_scalar_force(geometry, base, wavevectors, amplitudes, x_m, y_m, z_m, c_m_s,
    gradient_length_scale_m, 4 tolerances). Fixture limit = max_dense_entries; the block
    limit is passed generously (10**8) except in T14 where it is tested on its own."""

    REQUIRED = ('prepare_geometry', 'bind_base', 'exact_finite_sum', 'admit_scalar_force',
                'exact_scalar_force')

    def describe(self):
        return 'InterfaceAdapter(%s)' % ', '.join(self.REQUIRED)

    def reported_groups(self, g):
        counts = g.result.get('counts') if isinstance(g.result, dict) else None
        if counts and 'transverse_pairs_count' in counts and 'kz_count' in counts:
            return (counts['transverse_pairs_count'], counts['kz_count'])
        return None

    def prepare(self, k, x, y, z, *, limit=None, chunk=None, block=10 ** 8, point_chunk=None):
        pc = point_chunk if point_chunk is not None else max(1, 2 * int(chunk) - 1)
        r = call(self.m.prepare_geometry, dict(wavevectors=k, x_m=x, y_m=y, z_m=z, max_dense_entries=limit,
                                               max_block_entries=block, column_chunk=chunk, point_chunk=pc))
        if isinstance(r, Outcome):
            return r
        return Outcome(self.complete(r), r.get('geometry') if isinstance(r, dict) else None, r)

    def raw(self, geom, k, x, y, z, a):
        r = call(self.m.exact_finite_sum, dict(geometry=geom, wavevectors=k, amplitudes=a, x_m=x, y_m=y, z_m=z))
        if isinstance(r, Outcome):
            return r
        out = dict(dn=r.get('dn_complex'), grad_dn=r.get('grad_dn_complex'))
        return Outcome(self.complete(r), out, r)

    def bind(self, nb, gnb, pts):
        b = call(self.m.bind_base, dict(n_base=nb, grad_n_base=gnb, x_m=pts[0], y_m=pts[1], z_m=pts[2]))
        if isinstance(b, Outcome):
            return b
        return Outcome(self.complete(b), b.get('base'), b)

    @staticmethod
    def _tol(tol):
        return dict(base_reality_atol=tol['base_atol'], base_reality_rtol=tol['base_rtol'],
                    increment_reality_atol=tol['inc_atol'], increment_reality_rtol=tol['inc_rtol'])

    @staticmethod
    def _admitted(r):
        return dict(dn=r.get('dn_complex'), grad_dn=r.get('grad_dn_complex'), dphi=r.get('deltaPhi_m2_s2'),
                    gdphi=r.get('grad_deltaPhi_cartesian_m_s2'), Nb=r.get('Nb'))

    def admit(self, geom, k, x, y, z, a, nb, gnb, c, length, tol, *, base_points=None, base_geom=None):
        b = self.bind(nb, gnb, base_points if base_points is not None else (x, y, z))
        if not b.ok:
            return b
        kw = dict(geometry=geom, base=b.out, wavevectors=k, amplitudes=a, x_m=x, y_m=y, z_m=z, c_m_s=c,
                  gradient_length_scale_m=length)
        kw.update(self._tol(tol))
        r = call(self.m.exact_scalar_force, kw)
        if isinstance(r, Outcome):
            return r
        return Outcome(self.complete(r), self._admitted(r), r)

    def admit_two_stage(self, finite_sum_result, base_out, c, length, tol):
        kw = dict(finite_sum=finite_sum_result, base=base_out, c_m_s=c, gradient_length_scale_m=length)
        kw.update(self._tol(tol))
        r = call(self.m.admit_scalar_force, kw)
        if isinstance(r, Outcome):
            return r
        return Outcome(self.complete(r), self._admitted(r), r)


def make_adapter(module, text):
    names = discover(module, text)
    if all(n in names for n in InterfaceAdapter.REQUIRED):
        return InterfaceAdapter(module, text)
    if all(n in names for n in ('prepare_geometry', 'raw_finite_sum', 'bind_base', 'evaluate_force')):
        return AssumedAdapter(module, text)
    raise SystemExit('ADAPTER_UNRESOLVED: INTERFACE entry points %s' % names)


def call(fn, kwargs):
    try:
        result = fn(**kwargs)
    except Exception as exc:  # recorded, not swallowed silently
        return Outcome(False, None, None, exc)
    return result


# ---------------------------------------------------------------------------
# Test harness
# ---------------------------------------------------------------------------
RESULTS = []


def record(tid, name, verdict, detail, binding=True):
    RESULTS.append(dict(id=tid, name=name, verdict=verdict, binding=binding, detail=detail))
    print('%-5s %-8s %s :: %s' % (tid, verdict, name, detail if isinstance(detail, str)
                                  else json.dumps(detail, default=str)[:400]))
    sys.stdout.flush()


def check(tid, name, cond, detail, binding=True):
    record(tid, name, 'PASS' if cond else 'FAIL', detail, binding)
    return cond


def run_test(tid, fn, *args):
    try:
        fn(*args)
    except Exception:
        record(tid, fn.__name__, 'ERROR', traceback.format_exc()[-1500:])


def snapshot(*arrays):
    return [(hashlib.sha256(np.ascontiguousarray(a).tobytes()).hexdigest(), a.dtype.str, a.shape,
             bool(a.flags.writeable)) for a in arrays]


def generous_limit(A, k):
    return A.limit_for(k, 1000)


def tolset(base_atol=TIGHT, base_rtol=0.0, inc_atol=TIGHT, inc_rtol=0.0):
    return dict(base_atol=base_atol, base_rtol=base_rtol, inc_atol=inc_atol, inc_rtol=inc_rtol)


def compare_raw(A, geom, k, a, x, y, z, label):
    o = A.raw(geom, k, x, y, z, a)
    if not o.ok:
        return False, '%s: raw not COMPLETE: %s' % (label, o.describe())
    dn_o, gd_o = oracle(k, a, x, y, z)
    fs, gs = scales(k, a)
    ef = err_field(o.out['dn'], dn_o, fs)
    eg = err_grad(o.out['grad_dn'], gd_o, gs)
    return (ef <= REL and eg <= REL), '%s: field err %.2e, grad err %.2e (rel to abs-sum)' % (label, ef, eg)


# --- T00 oracle self-checks (no module) ------------------------------------
def t00_oracle(A):
    k, a = make_waves(11, fraction=0.15, extra_unique=2, duplicates=2)
    x, y, z = make_points(12)
    d1, g1 = oracle(k, a, x, y, z)
    d2, g2 = oracle_loop(k, a, x, y, z)
    fs, gs = scales(k, a)
    e = max(err_field(d1, d2, fs), err_grad(g1, g2, gs))
    h = 1e-4
    fd = np.empty((len(x), 3), dtype=complex)
    for j in range(3):
        sh = [np.zeros(len(x)) for _ in range(3)]
        vals = []
        for s in (-2, -1, 1, 2):
            sh[j] = np.full(len(x), s * h)
            vals.append(oracle(k, a, x + sh[0], y + sh[1], z + sh[2])[0])
        fd[:, j] = (vals[0] - 8 * vals[1] + 8 * vals[2] - vals[3]) / (12 * h)
    efd = err_grad(fd, g1, gs)
    check('T00', 'oracle numpy == cmath loop; oracle gradient == FD of oracle (sign convention)',
          e <= 1e-13 and efd <= REL_FD, 'loop err %.2e, FD err %.2e' % (e, efd))


# --- T01 direct sum, irregular signed anisotropic waves, holes, columns ----
def t01_direct(A):
    k, a = make_waves(21)
    x, y, z = make_points(22)
    pairs, nkz = A.required_dense(k)
    g = A.prepare(k, x, y, z, limit=A.limit_for(k, 4), chunk=3)
    if not check('T01', 'prepare COMPLETE (irregular waves, %d waves, %d pairs x %d kz, holes %d)'
                 % (len(k), pairs, nkz, pairs * nkz - len({tuple(r) for r in k})),
                 g.ok, g.describe()):
        return
    ok, msg = compare_raw(A, g.out, k, a, x, y, z, 'raw vs direct oracle')
    check('T01', 'scalar + all three gradient components vs direct finite sum', ok, msg)


# --- T02 reordered waves -----------------------------------------------------
def t02_reorder(A):
    k, a = make_waves(31)
    x, y, z = make_points(32)
    perm = np.random.default_rng(33).permutation(len(k))
    k2, a2 = np.ascontiguousarray(k[perm]), np.ascontiguousarray(a[perm])
    g1 = A.prepare(k, x, y, z, limit=A.limit_for(k, 4), chunk=4)
    g2 = A.prepare(k2, x, y, z, limit=A.limit_for(k2, 4), chunk=4)
    o1, o2 = A.raw(g1.out, k, x, y, z, a), A.raw(g2.out, k2, x, y, z, a2)
    if not check('T02', 'reordered waves both COMPLETE', o1.ok and o2.ok,
                 o1.describe() + ' | ' + o2.describe()):
        return
    fs, gs = scales(k, a)
    d, gd = oracle(k, a, x, y, z)
    e = max(err_field(o2.out['dn'], d, fs), err_grad(o2.out['grad_dn'], gd, gs),
            err_field(o1.out['dn'], o2.out['dn'], fs), err_grad(o1.out['grad_dn'], o2.out['grad_dn'], gs))
    check('T02', 'reordered waves == oracle == original order', e <= REL, 'max err %.2e' % e)


# --- T03 exact duplicate waves -------------------------------------------------
def t03_duplicates(A):
    k, a = make_waves(41, duplicates=0)
    x, y, z = make_points(42)
    # three exact copies of row 0 and two of row 5 with distinct complex amplitudes
    k2 = np.concatenate([k, k[[0, 0, 0, 5, 5]]])
    a2 = np.concatenate([a, np.array([0.4 - 0.9j, -1.1 + 0.2j, 0.05j, 2.0, -0.7 - 0.7j])])
    merged = a.copy()
    merged[0] += 0.4 - 0.9j - 1.1 + 0.2j + 0.05j
    merged[5] += 2.0 - 0.7 - 0.7j
    g = A.prepare(k2, x, y, z, limit=A.limit_for(k2, 4), chunk=5)
    o = A.raw(g.out, k2, x, y, z, a2) if g.ok else g
    if not check('T03', 'duplicates COMPLETE', o.ok, o.describe()):
        return
    fs, gs = scales(k2, a2)
    d1, g1 = oracle(k2, a2, x, y, z)
    d2, g2 = oracle(k, merged, x, y, z)
    e1 = max(err_field(o.out['dn'], d1, fs), err_grad(o.out['grad_dn'], g1, gs))
    e2 = max(err_field(o.out['dn'], d2, fs), err_grad(o.out['grad_dn'], g2, gs))
    check('T03', 'exact duplicate waves summed (== direct sum over all rows == merged amplitudes)',
          e1 <= REL and e2 <= REL, 'vs all-rows %.2e, vs merged %.2e' % (e1, e2))
    # a NEAR duplicate (one ulp in kz) is a different wave: compare to oracle, not merged
    k3 = np.concatenate([k, k[[2]]])
    k3[-1, 2] = np.nextafter(k3[-1, 2], np.inf) if k3[-1, 2] != 0 else 1e-300
    a3 = np.concatenate([a, np.array([0.8 + 0.3j])])
    g3 = A.prepare(k3, x, y, z, limit=A.limit_for(k3, 4), chunk=5)
    ok, msg = compare_raw(A, g3.out, k3, a3, x, y, z, 'one-ulp near-duplicate') if g3.ok else (False, g3.describe())
    check('T03', 'one-ulp near-duplicate kz kept as its own exact group, oracle agrees', ok, msg)
    pairs, nkz = A.required_dense(k3)
    rep = A.reported_groups(g3)
    if rep is not None:
        check('T03', 'reported exact groups == fixture count (no binning)', tuple(rep) == (pairs, nkz),
              'module %r fixture %r' % (rep, (pairs, nkz)))


# --- T04 holes: sparse subset, pathological missing combinations -----------
def t04_holes(A):
    rng = np.random.default_rng(51)
    # diagonal-only set: every (kx,ky) pair appears with exactly ONE kz -> dense S mostly holes
    n = 9
    kx = rng.uniform(-3, 3, n)
    ky = rng.uniform(-3, 3, n)
    kz = rng.uniform(-3, 3, n)
    k = np.stack([kx, ky, kz], axis=1)
    k = np.concatenate([k, np.stack([kx[:3], ky[:3], kz[3:6]], axis=1)])
    a = rng.uniform(0.3, 1.5, len(k)) * np.exp(1j * rng.uniform(-3, 3, len(k)))
    x, y, z = make_points(52)
    g = A.prepare(k, x, y, z, limit=A.limit_for(k, 2), chunk=2)
    pairs, nkz = A.required_dense(k)
    ok, msg = compare_raw(A, g.out, k, a, x, y, z, 'holes %d/%d filled' % (len(k), pairs * nkz)) if g.ok \
        else (False, g.describe())
    check('T04', 'missing Cartesian combinations contribute nothing (sparse dense S)', ok, msg)
    # single wave
    k1, a1 = np.array([[0.37, -1.9, 2.6]]), np.array([0.6 - 1.2j])
    g1 = A.prepare(k1, x, y, z, limit=A.limit_for(k1, 2), chunk=1)
    ok, msg = compare_raw(A, g1.out, k1, a1, x, y, z, 'single wave') if g1.ok else (False, g1.describe())
    check('T04', 'single-wave case', ok, msg)


# --- T05 points: nonuniform z, off-column points, single point --------------
def t05_points(A):
    k, a = make_waves(61)
    x, y, z = make_points(62)
    ok, msg = True, []
    for label, (xx, yy, zz) in (('shuffled columns + off-column + repeated point', (x, y, z)),
                                ('one point', (x[:1], y[:1], z[:1])),
                                ('one column, irregular z', (np.full(9, 0.731), np.full(9, -1.27),
                                                             np.array([-1.4, -1.39, -0.2, 0.0, 0.001,
                                                                       0.5, 0.51, 1.2, 1.45]))),
                                ('all distinct columns', (x + np.arange(len(x)) * 1e-3, y, z))):
        g = A.prepare(k, xx, yy, zz, limit=A.limit_for(k, 4), chunk=2)
        if not g.ok:
            ok = False
            msg.append('%s: prepare %s' % (label, g.describe()))
            continue
        good, m = compare_raw(A, g.out, k, a, xx, yy, zz, label)
        ok = ok and good
        msg.append(m)
    check('T05', 'nonuniform z per column / points not on columns / single point', ok, ' ; '.join(msg))


# --- T06 derivative components and signs ------------------------------------
def t06_signs(A):
    x, y, z = make_points(72)
    k = np.array([[1.3, -0.4, 2.1]])
    a = np.array([0.9 + 0.35j])
    g = A.prepare(k, x, y, z, limit=A.limit_for(k, 2), chunk=3)
    o = A.raw(g.out, k, x, y, z, a) if g.ok else g
    if not check('T06', 'single-wave raw COMPLETE', o.ok, o.describe()):
        return
    e = a[0] * np.exp(1j * (1.3 * x - 0.4 * y + 2.1 * z))
    expect = np.stack([1j * 1.3 * e, -1j * 0.4 * e, 1j * 2.1 * e], axis=1)
    errs = [float(np.max(np.abs(np.asarray(o.out['grad_dn'])[:, j] - expect[:, j]))) for j in range(3)]
    check('T06', 'grad = (i kx, i ky, i kz) a e^{ik.x} per component (signs, order)',
          max(errs) <= 1e-12, 'per-component max err %s' % ['%.1e' % v for v in errs])
    # module's own FD along each axis (independent of both formulae)
    kk, aa = make_waves(73)
    gg = A.prepare(kk, x, y, z, limit=A.limit_for(kk, 4), chunk=3)
    base = A.raw(gg.out, kk, x, y, z, aa)
    h = 1e-4
    fd = np.empty((len(x), 3), dtype=complex)
    for j in range(3):
        vals = []
        for s in (-2, -1, 1, 2):
            sh = [x, y, z]
            sh = [c + (s * h if i == j else 0.0) for i, c in enumerate(sh)]
            gs_ = A.prepare(kk, sh[0], sh[1], sh[2], limit=A.limit_for(kk, 4), chunk=3)
            vals.append(np.asarray(A.raw(gs_.out, kk, sh[0], sh[1], sh[2], aa).out['dn']))
        fd[:, j] = (vals[0] - 8 * vals[1] + 8 * vals[2] - vals[3]) / (12 * h)
    fs, gsc = scales(kk, aa)
    efd = err_grad(fd, np.asarray(base.out['grad_dn']), gsc)
    check('T06', 'module grad_dn == 4th-order FD of module dn along x, y, z', efd <= REL_FD,
          'FD err %.2e' % efd)


# --- T07 linearity / scaling with complex coefficients ----------------------
def t07_linear(A):
    k, a1 = make_waves(81)
    rng = np.random.default_rng(82)
    a2 = rng.normal(size=len(k)) + 1j * rng.normal(size=len(k))
    x, y, z = make_points(83)
    g = A.prepare(k, x, y, z, limit=A.limit_for(k, 4), chunk=4)
    al, be = 0.7 - 2.3j, -1.6 + 0.4j
    o1, o2 = A.raw(g.out, k, x, y, z, a1), A.raw(g.out, k, x, y, z, a2)
    o3 = A.raw(g.out, k, x, y, z, al * a1 + be * a2)
    o4 = A.raw(g.out, k, x, y, z, (2.0 ** 40) * 1j * a1)
    if not check('T07', 'raw COMPLETE x4', all(o.ok for o in (o1, o2, o3, o4)),
                 ' | '.join(o.describe() for o in (o1, o2, o3, o4))):
        return
    fs, gs = scales(k, np.abs(al * a1) + np.abs(be * a2))
    lin_f = al * np.asarray(o1.out['dn']) + be * np.asarray(o2.out['dn'])
    lin_g = al * np.asarray(o1.out['grad_dn']) + be * np.asarray(o2.out['grad_dn'])
    e = max(err_field(o3.out['dn'], lin_f, fs), err_grad(o3.out['grad_dn'], lin_g, gs))
    d3, gd3 = oracle(k, al * a1 + be * a2, x, y, z)
    eo = max(err_field(o3.out['dn'], d3, fs), err_grad(o3.out['grad_dn'], gd3, gs))
    fs4, gs4 = scales(k, (2.0 ** 40) * a1)
    e4 = max(err_field(o4.out['dn'], (2.0 ** 40) * 1j * np.asarray(o1.out['dn']), fs4),
             err_grad(o4.out['grad_dn'], (2.0 ** 40) * 1j * np.asarray(o1.out['grad_dn']), gs4))
    check('T07', 'raw(al a1 + be a2) == al raw(a1) + be raw(a2) == oracle; complex scaling 2^40 i',
          max(e, eo, e4) <= REL, 'linearity %.2e oracle %.2e scaling %.2e' % (e, eo, e4))
    # raw keeps the complex value: no .real, no reflection, no factor 2, no c^2
    d1, _ = oracle(k, a1, x, y, z)
    im = float(np.max(np.abs(np.asarray(o1.out['dn']).imag - d1.imag)))
    check('T07', 'raw path retains the imaginary part of a non-Hermitian sum (no .real / reflection)',
          im <= REL * scales(k, a1)[0] and float(np.max(np.abs(d1.imag))) > 0.1,
          'imag err %.2e, oracle max |Im| %.2f' % (im, float(np.max(np.abs(d1.imag)))))


# --- T08 linear lapse quotient ------------------------------------------------
def t08_lapse(A, xscale=1.0):
    inv = 1.0 / xscale
    k, a = make_waves(91, hermitian=True, kscale=inv)
    a = a * 0.05
    x, y, z = make_points(92, xscale=xscale)
    nb, gnb = base_field(x, y, z, inv=inv)
    g = A.prepare(k, x, y, z, limit=A.limit_for(k, 4), chunk=3)
    L = 0.5 * xscale
    o = A.admit(g.out, k, x, y, z, a, nb, gnb, C_TEST, L, tolset()) if g.ok else g
    tag = 'xscale %.0e' % xscale
    if not check('T08', 'admitted COMPLETE on a real (Hermitian) increment, %s' % tag, o.ok, o.describe()):
        return
    dn, gdn = oracle(k, a, x, y, z)
    Nb, dphi, gd = lapse_expected(dn, gdn, nb, gnb, C_TEST)
    fs, gs = scales(k, a)
    c2 = C_TEST * C_TEST
    tol_d = 10 * REL * c2 * fs / float(np.min(Nb))
    tol_g = 10 * REL * c2 * (float(np.max(gs)) / float(np.min(Nb))
                             + fs * float(np.max(np.abs(gnb))) / float(np.min(Nb)) ** 2)
    ed = float(np.max(np.abs(np.asarray(o.out['dphi']) - dphi)))
    eg = float(np.max(np.abs(np.asarray(o.out['gdphi']) - gd)))
    check('T08', 'deltaPhi = c^2 Re dn/Nb and grad formula vs independent computation, %s' % tag,
          ed <= tol_d and eg <= tol_g, 'dPhi err %.2e (tol %.1e), grad err %.2e (tol %.1e)'
          % (ed, tol_d, eg, tol_g))
    ef = max(err_field(o.out['dn'], dn, fs), err_grad(o.out['grad_dn'], gdn, gs))
    cplx = np.iscomplexobj(np.asarray(o.out['dn'])) and np.iscomplexobj(np.asarray(o.out['grad_dn']))
    check('T08', 'admitted output retains complex dn and grad_dn == oracle, %s' % tag,
          cplx and ef <= REL, 'complex dtype %s, err %.2e' % (cplx, ef))
    if o.out.get('Nb') is not None:
        eN = float(np.max(np.abs(np.asarray(o.out['Nb']) - Nb)))
        check('T08', 'reported Nb == 1 + Re n_b, %s' % tag, eN <= 1e-15, 'err %.1e' % eN, binding=False)
    if xscale != 1.0:
        return
    # independent quotient-rule check: FD of the module's own admitted deltaPhi
    h = 1e-4
    fd = np.empty((len(x), 3))
    for j in range(3):
        vals = []
        for s in (-2, -1, 1, 2):
            sh = [c + (s * h if i == j else 0.0) for i, c in enumerate((x, y, z))]
            nbs, gnbs = base_field(*sh)
            gsh = A.prepare(k, sh[0], sh[1], sh[2], limit=A.limit_for(k, 4), chunk=3)
            vals.append(np.asarray(A.admit(gsh.out, k, sh[0], sh[1], sh[2], a, nbs, gnbs, C_TEST, L,
                                           tolset()).out['dphi']))
        fd[:, j] = (vals[0] - 8 * vals[1] + 8 * vals[2] - vals[3]) / (12 * h)
    sc = float(np.max(np.abs(gd)))
    efd = float(np.max(np.abs(fd - np.asarray(o.out['gdphi'])))) / sc
    check('T08', 'module grad deltaPhi == 4th-order FD of module deltaPhi (quotient rule, signs)',
          efd <= REL_FD, 'FD err %.2e rel' % efd)
    # c appears exactly as c^2 once: c -> 2c multiplies by 4
    o2 = A.admit(g.out, k, x, y, z, a, nb, gnb, 2 * C_TEST, L, tolset())
    r = float(np.max(np.abs(np.asarray(o2.out['dphi']) - 4 * np.asarray(o.out['dphi'])))) / \
        float(np.max(np.abs(np.asarray(o.out['dphi']))))
    check('T08', 'c^2 enters once (2c -> 4x deltaPhi)', o2.ok and r <= 1e-14, 'rel diff %.1e' % r)


def t08b_units(A):
    t08_lapse(A, xscale=3.0857e19)


# --- T09 reality failures, each with a passing control ------------------------
def _real_case(A, seed, z_zero=False):
    k, a = make_waves(seed, hermitian=True, fraction=0.2, extra_unique=2, duplicates=2)
    a = a * 0.05
    x, y, z = make_points(seed + 1, z_zero=z_zero)
    nb, gnb = base_field(x, y, z)
    g = A.prepare(k, x, y, z, limit=A.limit_for(k, 4), chunk=3)
    return k, a, x, y, z, nb, gnb, g


def t09_reality(A):
    k, a, x, y, z, nb, gnb, g = _real_case(A, 101)
    L, at = 1.0, 1e-8
    cases = []
    p = 7
    for label, mod in (
            ('base field', lambda nb_, gnb_, a_, f: (nb_ + _spike(len(nb_), p, 1j * f * at), gnb_, a_)),
            ('base gradient', lambda nb_, gnb_, a_, f: (nb_, _spike3(len(nb_), p, 1, 1j * f * at / L) + gnb_, a_)),
            ('increment field', lambda nb_, gnb_, a_, f: (nb_, gnb_, None))):
        cases.append((label, mod))
    out = []
    allok = True
    for label, mod in cases[:2]:
        for f, want in ((0.5, True), (2.0, False)):
            nb2, gnb2, _ = mod(nb, gnb, a, f)
            o = A.admit(g.out, k, x, y, z, a, nb2, gnb2, C_TEST, L, tolset(base_atol=at, inc_atol=at))
            good = (o.ok == want)
            allok = allok and good
            out.append('%s x%.1f -> %s%s' % (label, f, vs(o),
                                              '' if good else ' (WRONG: %s)' % o.describe()))
    # increment field: a k=0 wave with amplitude i*f*at -> Im dn = f*at everywhere, gradient untouched
    for f, want in ((0.5, True), (2.0, False)):
        k2 = np.concatenate([k, np.zeros((1, 3))])
        a2 = np.concatenate([a, np.array([1j * f * at])])
        g2 = A.prepare(k2, x, y, z, limit=A.limit_for(k2, 4), chunk=3)
        o = A.admit(g2.out, k2, x, y, z, a2, nb, gnb, C_TEST, L, tolset(base_atol=at, inc_atol=at))
        good = (o.ok == want)
        allok = allok and good
        out.append('increment field x%.1f -> %s%s' % (f, vs(o),
                                                      '' if good else ' (WRONG: %s)' % o.describe()))
    # increment gradient: wave (0,0,kappa), real amplitude beta, all points at z=0:
    # field += beta (real), grad_z += i kappa beta (pure imaginary); L*kappa*beta vs atol
    k, a, x, y, z, nb, gnb, _ = _real_case(A, 111, z_zero=True)
    kappa = 1.7
    for f, want in ((0.5, True), (2.0, False)):
        beta = f * at / (L * kappa)
        k2 = np.concatenate([k, np.array([[0.0, 0.0, kappa]])])
        a2 = np.concatenate([a, np.array([beta + 0j])])
        g2 = A.prepare(k2, x, y, z, limit=A.limit_for(k2, 4), chunk=3)
        o = A.admit(g2.out, k2, x, y, z, a2, nb, gnb, C_TEST, L, tolset(base_atol=at, inc_atol=at))
        good = (o.ok == want)
        allok = allok and good
        out.append('increment gradient x%.1f -> %s%s' % (f, vs(o),
                                                         '' if good else ' (WRONG: %s)' % o.describe()))
    check('T09', 'nonreal base/increment field/gradient rejected above tolerance, accepted below',
          allok, ' ; '.join(out))


def _spike(n, p, v):
    s = np.zeros(n, dtype=complex)
    s[p] = v
    return s


def _spike3(n, p, j, v):
    s = np.zeros((n, 3), dtype=complex)
    s[p, j] = v
    return s


# --- T10 gradient tolerance scales with the supplied length -------------------
def t10_length(A):
    k, a, x, y, z, nb, gnb, g = _real_case(A, 121)
    at, eps = 1e-8, 1e-6          # base gradient Im = eps [1/m]; scaled Im = L*eps
    gnb2 = gnb + _spike3(len(x), 4, 2, 1j * eps)
    out = []
    allok = True
    for L, want in ((1e-3, True), (1.0, False)):
        o = A.admit(g.out, k, x, y, z, a, nb, gnb2, C_TEST, L, tolset(base_atol=at, inc_atol=at))
        good = o.ok == want
        allok = allok and good
        out.append('base grad, L=%g -> %s%s' % (L, vs(o),
                                               '' if good else ' (WRONG %s)' % o.describe()))
    # field checks must NOT scale with L: Im n_b = 0.5 atol passes at any L; 2 atol fails at any L
    for f, L, want in ((0.5, 1e6, True), (2.0, 1e-6, False)):
        o = A.admit(g.out, k, x, y, z, a, nb + _spike(len(x), 4, 1j * f * at), gnb, C_TEST, L,
                    tolset(base_atol=at, inc_atol=at))
        good = o.ok == want
        allok = allok and good
        out.append('base field x%.1f, L=%g -> %s%s' % (f, L, vs(o),
                                                       '' if good else ' (WRONG %s)' % o.describe()))
    # rtol: Im = 0.5 * rtol * |Re| passes with atol=0
    o = A.admit(g.out, k, x, y, z, a, nb + 1j * 0.5e-6 * np.abs(nb.real), gnb, C_TEST, 1.0,
                tolset(base_atol=0.0, base_rtol=1e-6, inc_atol=TIGHT))
    allok = allok and o.ok
    out.append('base field Im=0.5 rtol|Re| atol=0 -> %s' % ('COMPLETE' if o.ok else 'REJECTED (WRONG)'))
    check('T10', 'gradient reality tolerance scales with supplied length; field check does not; rtol honoured',
          allok, ' ; '.join(out))


# --- T11 Nb <= 0 --------------------------------------------------------------
def t11_nb(A):
    k, a, x, y, z, nb, gnb, g = _real_case(A, 131)
    out, allok = [], True
    for v, want in ((-0.999, True), (-1.0, False), (-1.25, False), (float('nan'), False),
                    (float('-inf'), False)):
        nb2 = nb.copy()
        nb2[5] = v
        o = A.admit(g.out, k, x, y, z, a, nb2, gnb, C_TEST, 1.0, tolset())
        good = o.ok == want
        allok = allok and good
        out.append('n_b=%r -> %s%s' % (v, vs(o),
                                       '' if good else ' (WRONG %s)' % o.describe()))
    check('T11', 'N_b = 1 + Re n_b <= 0 or nonfinite rejected; N_b > 0 accepted', allok, ' ; '.join(out))


# --- T12 cached-point / wave identity mismatch -----------------------------------
def t12_identity(A):
    k, a, x, y, z, nb, gnb, g = _real_case(A, 141)
    out, allok = [], True
    x2 = x.copy()
    x2[3] = np.nextafter(x2[3], np.inf)
    z2 = z.copy()
    z2[0] = np.nextafter(z2[0], -np.inf)
    perm = np.arange(len(x))[::-1].copy()
    for label, pts in (('one x ulp', (x2, y, z)), ('one z ulp', (x, y, z2)),
                       ('points reversed', (x[perm], y[perm], z[perm])),
                       ('one point dropped', (x[:-1], y[:-1], z[:-1]))):
        o = A.admit(g.out, k, x, y, z, a, nb[:len(pts[0])], gnb[:len(pts[0])], C_TEST, 1.0, tolset(),
                    base_points=pts)
        good = not o.ok
        allok = allok and good
        out.append('base bound to %s -> %s' % (label, vs(o) if not o.ok else 'COMPLETE (WRONG)'))
    # base bound (validly) under a geometry for P', then used with the geometry for P
    for label, pts in (('one x ulp', (x2, y, z)), ('one z ulp', (x, y, z2))):
        go = A.prepare(k, pts[0], pts[1], pts[2], limit=A.limit_for(k, 4), chunk=3)
        o = A.admit(g.out, k, x, y, z, a, nb, gnb, C_TEST, 1.0, tolset(), base_points=pts, base_geom=go.out)
        good = go.ok and not o.ok
        allok = allok and good
        out.append("base bound under geometry for P' (%s), used with geometry for P -> %s"
                   % (label, vs(o) if not o.ok else 'COMPLETE (WRONG)'))
    for label, kk in (('one kx ulp', _ulp(k, 0)), ('waves reordered', k[::-1].copy()), ('one wave dropped', k[:-1])):
        o = A.raw(g.out, kk, x, y, z, a[:len(kk)])
        good = (not o.ok) or _agrees(o, kk, a[:len(kk)], x, y, z)
        allok = allok and good
        out.append('geometry for K, waves %s -> %s' % (label, vs(o) if not o.ok else
                                                       ('COMPLETE (== oracle for supplied waves)' if good
                                                        else 'COMPLETE STALE (WRONG)')))
    for label, pts in (('one x ulp', (x2, y, z)), ('points reversed', (x[perm], y[perm], z[perm]))):
        o = A.raw(g.out, k, pts[0], pts[1], pts[2], a)
        good = (not o.ok) or _agrees(o, k, a, *pts)
        allok = allok and good
        out.append('geometry for P, points %s -> %s' % (label, vs(o) if not o.ok else
                                                        ('COMPLETE (== oracle)' if good else 'COMPLETE STALE (WRONG)')))
    check('T12', 'cached base / geometry identity mismatch rejected (never stale reuse)', allok, ' ; '.join(out))


def _ulp(k, j):
    k2 = k.copy()
    k2[1, j] = np.nextafter(k2[1, j], np.inf)
    return k2


def _agrees(o, k, a, x, y, z):
    d, gd = oracle(k, a, x, y, z)
    fs, gs = scales(k, a)
    return err_field(o.out['dn'], d, fs) <= REL and err_grad(o.out['grad_dn'], gd, gs) <= REL


# --- T13 source change refresh; geometry reuse ----------------------------------
def t13_refresh(A):
    k, a, x, y, z, nb, gnb, g = _real_case(A, 151)
    rng = np.random.default_rng(152)
    out, allok = [], True
    seq = [a, a * (-0.3 + 0.1j), rng.normal(size=len(k)) + 1j * rng.normal(size=len(k)), a]
    for i, aa in enumerate(seq):
        o = A.raw(g.out, k, x, y, z, aa)
        good = o.ok and _agrees(o, k, aa, x, y, z)
        allok = allok and good
        out.append('raw #%d %s' % (i, 'oracle' if good else 'WRONG ' + o.describe()))
    # in-place mutation of the SAME caller array object between calls (no id()-based caching)
    buf = a.copy()
    o1 = A.admit(g.out, k, x, y, z, buf, nb, gnb, C_TEST, 1.0, tolset())
    buf *= 2.0
    o2 = A.admit(g.out, k, x, y, z, buf, nb, gnb, C_TEST, 1.0, tolset())
    r = float(np.max(np.abs(np.asarray(o2.out['dphi']) - 2 * np.asarray(o1.out['dphi'])))) / \
        float(np.max(np.abs(np.asarray(o1.out['dphi']))))
    good = o1.ok and o2.ok and r <= 1e-13
    allok = allok and good
    out.append('same amplitude buffer mutated in place x2 -> deltaPhi x2 rel %.1e' % r)
    # base refresh: new base on same points -> new quotient
    nb3 = nb * 0.5
    gnb3 = gnb * 0.5
    o3 = A.admit(g.out, k, x, y, z, buf, nb3, gnb3, C_TEST, 1.0, tolset())
    dn, gdn = oracle(k, buf, x, y, z)
    _, dphi3, gd3 = lapse_expected(dn, gdn, nb3, gnb3, C_TEST)
    e3 = float(np.max(np.abs(np.asarray(o3.out['dphi']) - dphi3))) / float(np.max(np.abs(dphi3)))
    good = o3.ok and e3 <= 1e-10
    allok = allok and good
    out.append('base changed -> refreshed quotient err %.1e' % e3)
    # caller mutation of the arrays used at prepare time must not leak into the geometry
    kc, xc, yc, zc = k.copy(), x.copy(), y.copy(), z.copy()
    gc = A.prepare(kc, xc, yc, zc, limit=A.limit_for(kc, 4), chunk=3)
    kc[:, 0] += 0.5
    xc += 0.25
    o4 = A.raw(gc.out, k, x, y, z, a)
    good = o4.ok and _agrees(o4, k, a, x, y, z)
    allok = allok and good
    out.append('caller arrays mutated after prepare -> geometry %s' % ('unaffected' if good else
                                                                       'AFFECTED/REJECTED ' + o4.describe()))
    check('T13', 'amplitudes / base refreshed per call; geometry reuse across sources == oracle', allok,
          ' ; '.join(out))


# --- T14 dense-grouping limit -------------------------------------------------------
def t14_limit(A):
    k, a = make_waves(161)
    x, y, z = make_points(162)
    pairs, nkz = A.required_dense(k)
    out, allok = [], True
    for label, lim, want in (('far below', A.limit_for(k, 0.25), False),
                             ('just below', A.limit_for(k, 'below'), False),
                             ('exactly at', A.limit_for(k, 'exact'), True),
                             ('generous', A.limit_for(k, 8), True)):
        if lim is None:
            continue
        g = A.prepare(k, x, y, z, limit=lim, chunk=3)
        good = g.ok == want
        allok = allok and good
        out.append('%s (%r) -> %s%s' % (label, lim, vs(g),
                                        '' if good else ' (WRONG %s)' % g.describe()))
    check('T14', 'dense grouping %d pairs x %d kz rejected over the caller limit' % (pairs, nkz), allok,
          ' ; '.join(out))
    if isinstance(A, InterfaceAdapter):
        # block limit: cb = min(column_chunk, columns), pb = min(point_chunk, points);
        # need max(cb*n_pairs, 4*cb*n_kz, pb*n_kz) <= max_block_entries (INTERFACE)
        ncol = len({(float(u), float(v)) for u, v in zip(x, y)})
        cb, pb = min(3, ncol), min(5, len(x))
        need = max(cb * pairs, 4 * cb * nkz, pb * nkz)
        out2, ok2 = [], True
        for label, blk, want in (('just below', need - 1, False), ('exact', need, True)):
            g = A.prepare(k, x, y, z, limit=A.limit_for(k, 8), chunk=3, block=blk, point_chunk=5)
            good = g.ok == want
            ok2 = ok2 and good
            out2.append('%s (%d) -> %s%s' % (label, blk, vs(g),
                                             '' if good else ' (WRONG %s)' % g.describe()))
            if g.ok:
                good, m = compare_raw(A, g.out, k, a, x, y, z, 'at block limit')
                ok2 = ok2 and good
                out2.append(m)
        check('T14', 'block limit max(cb*n_pairs, 4*cb*n_kz, pb*n_kz) = %d enforced before allocation' % need,
              ok2, ' ; '.join(out2))


# --- T15 chunk invariance -------------------------------------------------------------
def t15_chunk(A):
    k, a = make_waves(171)
    x, y, z = make_points(172)
    res = []
    for ch in A.chunk_values():
        g = A.prepare(k, x, y, z, limit=A.limit_for(k, 4), chunk=ch)
        if isinstance(A, InterfaceAdapter):
            for pc in (1, 4, 1000):
                g2 = A.prepare(k, x, y, z, limit=A.limit_for(k, 4), chunk=ch, point_chunk=pc)
                o2 = A.raw(g2.out, k, x, y, z, a) if g2.ok else g2
                res.append(('c%d/p%d' % (ch, pc), o2))
        o = A.raw(g.out, k, x, y, z, a) if g.ok else g
        res.append((ch, o))
    ok = all(o.ok for _, o in res)
    fs, gs = scales(k, a)
    e = 0.0
    if ok:
        for _, o in res[1:]:
            e = max(e, err_field(o.out['dn'], res[0][1].out['dn'], fs),
                    err_grad(o.out['grad_dn'], res[0][1].out['grad_dn'], gs))
    check('T15', 'column-chunk invariance %s' % [c for c, _ in res], ok and e <= REL_CHUNK,
          'max diff %.2e' % e, binding=False)


# --- T16 caller inputs unmutated --------------------------------------------------------
def t16_immutable(A):
    k, a, x, y, z, nb, gnb, _ = _real_case(A, 181)
    nb = nb + 1j * 1e-12 * np.cos(x)             # sub-tolerance imaginary parts a module must not touch
    gnb = gnb + 1j * 1e-12 * np.sin(y)[:, None]
    arrays = [k, a, x, y, z, nb, gnb]
    before = snapshot(*arrays)
    g = A.prepare(k, x, y, z, limit=A.limit_for(k, 4), chunk=3)
    A.raw(g.out, k, x, y, z, a)
    A.admit(g.out, k, x, y, z, a, nb, gnb, C_TEST, 1.0, tolset())
    nb_bad = nb.copy()
    nb_bad[0] = -3.0
    bb = snapshot(nb_bad)
    A.admit(g.out, k, x, y, z, a, nb_bad, gnb, C_TEST, 1.0, tolset())
    after = snapshot(*arrays)
    check('T16', 'caller inputs unmutated (bytes, dtype, shape, writeable) incl. on failure',
          before == after and bb == snapshot(nb_bad), 'equal=%s' % (before == after))


# --- T17 floating-point errors -> fail closed ---------------------------------------------
def t17_fpe(A):
    k = np.array([[0.5, 0.25, -1.0], [0.5, 0.25, -1.0], [1.0, 0.0, 0.0]])
    a = np.array([1e308 + 0j, 1e308 + 0j, 1.0 + 0j])     # duplicate scatter overflows
    x, y, z = make_points(191)
    out, allok = [], True
    for mode in ('raise', 'ignore'):
        with np.errstate(all=mode):
            try:
                g = A.prepare(k, x, y, z, limit=A.limit_for(k, 4), chunk=3)
                o = A.raw(g.out, k, x, y, z, a) if g.ok else g
            except FloatingPointError as exc:
                o = Outcome(False, None, None, exc)
                out.append('errstate %s -> FloatingPointError ESCAPED (WRONG)' % mode)
                allok = False
                continue
        good = (not o.ok) and o.exc is None
        allok = allok and good
        out.append('errstate %s -> %s' % (mode, ('fail-closed dict ' + vs(o)) if good else o.describe()))
    for label, kk, aa, xx in (('nan wave', np.array([[np.nan, 0.0, 0.0]]), np.array([1.0 + 0j]), x),
                              ('inf amplitude', np.array([[1.0, 0.0, 0.0]]), np.array([np.inf + 0j]), x),
                              ('nan point', np.array([[1.0, 0.0, 0.0]]), np.array([1.0 + 0j]),
                               np.concatenate([[np.nan], x[1:]]))):
        with np.errstate(all='ignore'):
            g = A.prepare(kk, xx, y, z, limit=A.limit_for(kk, 4), chunk=3)
            o = A.raw(g.out, kk, xx, y, z, aa) if g.ok else g
        good = not o.ok
        allok = allok and good
        out.append('%s -> %s' % (label, vs(o)
                                 if good else 'COMPLETE (WRONG)'))
    check('T17', 'FloatingPointError / nonfinite inputs fail closed', allok, ' ; '.join(out))


# --- T18 no Hessian claimed ---------------------------------------------------------------
def t18_hessian(A):
    k, a, x, y, z, nb, gnb, g = _real_case(A, 201)
    o = A.admit(g.out, k, x, y, z, a, nb, gnb, C_TEST, 1.0, tolset())
    bad = []

    def walk(obj, path):
        if isinstance(obj, dict):
            for key, v in obj.items():
                if 'hess' in str(key).lower() and isinstance(v, np.ndarray):
                    bad.append(path + '/' + str(key))
                walk(v, path + '/' + str(key))
    walk(o.result if isinstance(o.result, dict) else {}, '')
    text = A.interface_text.lower()
    stated = 'hessian' in text and any(w in text for w in ('no hessian', 'not evaluated', 'none evaluated',
                                                          'hessian: none', 'no hessian is'))
    check('T18', 'no Hessian array returned; INTERFACE states none evaluated', o.ok and not bad and stated,
          'hessian arrays %s; interface statement found %s' % (bad, stated))


# --- T19 import inertness and lane scan ----------------------------------------------------
def t19_inert(A, module_path):
    with tempfile.TemporaryDirectory() as d:
        code = ('import importlib.util,sys\n'
                'spec=importlib.util.spec_from_file_location("m0455",sys.argv[1])\n'
                'm=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)\n')
        env = dict(os.environ)
        proc = subprocess.run([sys.executable, '-I', '-B', '-c', code, module_path], cwd=d,
                              capture_output=True, text=True, timeout=60, env=env)
        created = os.listdir(d)
    check('T19', 'import is inert (no output, no files, exit 0)',
          proc.returncode == 0 and not proc.stdout and not proc.stderr and not created,
          'rc=%d stdout=%r stderr=%r files=%r' % (proc.returncode, proc.stdout[:200], proc.stderr[:200], created))
    with open(module_path, 'r') as handle:
        tree = ast.parse(handle.read())
    top_bad = [type(n).__name__ for n in tree.body
               if not isinstance(n, (ast.Import, ast.ImportFrom, ast.FunctionDef, ast.ClassDef,
                                     ast.Assign, ast.AnnAssign))
               and not (isinstance(n, ast.Expr) and isinstance(getattr(n, 'value', None), ast.Constant))]
    issues = []
    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.MatMult):
            issues.append('@ at line %d' % node.lineno)
        if isinstance(node, ast.Attribute) and node.attr in ('dot', 'matmul', 'vdot', 'inner', 'tensordot',
                                                              'seterr', 'filterwarnings', 'simplefilter',
                                                              'load', 'save', 'savez'):
            issues.append('.%s at line %d' % (node.attr, node.lineno))
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'open':
            issues.append('open() at line %d' % node.lineno)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == 'einsum':
            kws = {kw.arg: kw.value for kw in node.keywords}
            if not (isinstance(kws.get('optimize'), ast.Constant) and kws['optimize'].value is False):
                issues.append('einsum without optimize=False at line %d' % node.lineno)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == 'errstate':
            issues.append('errstate at line %d' % node.lineno)
        if isinstance(node, ast.Import):
            imports.update(al.name.split('.')[0] for al in node.names)
        if isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module.split('.')[0])
    nonstd = sorted(i for i in imports if i != 'numpy' and i not in sys.stdlib_module_names)
    check('T19', 'lane scan: definitions-only top level, numpy+stdlib, no BLAS products, einsum optimize=False, '
          'no warning suppression / I/O', not top_bad and not issues and not nonstd,
          'top-level non-def %s; issues %s; non-stdlib imports %s' % (top_bad, issues, nonstd), binding=False)
    sigs = {}
    for name in A.discovered:
        fn = getattr(A.m, name)
        if inspect.isfunction(fn):
            ps = inspect.signature(fn).parameters.values()
            sigs[name] = [p.name for p in ps if p.kind != p.KEYWORD_ONLY or p.default is not p.empty]
    check('T19', 'public entry points keyword-only, no defaults', all(not v for v in sigs.values()),
          'violations %s' % sigs, binding=False)


# --- T20 actual-shape synthetic lattice: 72^3 signed waves = 5184 pairs x 72 kz ----------
def t20_lattice(A):
    n = np.arange(-36, 36, dtype=float)
    dk = 2.0 * np.pi / 7.3e20                        # synthetic box, physical 1/m scale
    gx, gy, gz = np.meshgrid(n * dk, n * dk * 1.0000001, n * dk * 0.9999999, indexing='ij')
    k = np.ascontiguousarray(np.stack([gx.ravel(), gy.ravel(), gz.ravel()], axis=1))
    rng = np.random.default_rng(211)
    a = (rng.normal(size=len(k)) + 1j * rng.normal(size=len(k))) * 1e-3
    x = np.array([1.1e20, 1.1e20, -2.3e20, 0.4e20])
    y = np.array([-0.7e20, -0.7e20, 0.9e20, 2.2e20])
    z = np.array([0.05e20, -0.31e20, 0.12e20, 0.0])
    pairs, nkz = A.required_dense(k)
    out, allok = ['fixture count %d pairs x %d kz' % (pairs, nkz)], (pairs, nkz) == (5184, 72)
    t0 = time.time()
    g0 = A.prepare(k, x, y, z, limit=A.limit_for(k, 'below'), chunk=2)
    allok = allok and not g0.ok
    out.append('limit just below -> %s (%.2fs)' % (vs(g0) if not g0.ok else 'COMPLETE (WRONG)', time.time() - t0))
    t0 = time.time()
    g = A.prepare(k, x, y, z, limit=A.limit_for(k, 'exact'), chunk=2)
    o = A.raw(g.out, k, x, y, z, a) if g.ok else g
    t1 = time.time() - t0
    if o.ok:
        d, gd = oracle(k, a, x, y, z)
        fs, gs = scales(k, a)
        ef, eg = err_field(o.out['dn'], d, fs), err_grad(o.out['grad_dn'], gd, gs)
        allok = allok and ef <= REL and eg <= REL
        out.append('limit exact -> COMPLETE (%.2fs), field err %.2e, grad err %.2e' % (t1, ef, eg))
    else:
        allok = False
        out.append('limit exact -> %s' % o.describe())
    rep = A.reported_groups(g) if g.ok else None
    if rep is not None:
        allok = allok and tuple(rep) == (5184, 72)
        out.append('module reports %r' % (tuple(rep),))
    check('T20', 'synthetic 72^3 signed lattice (no data): 5184 x 72 grouping, limit, oracle on 4 points',
          allok, ' ; '.join(out))


# --- T21 API-specific: two-stage path (raw result -> admission) and identity of the raw result -----
def t21_two_stage(A):
    if not isinstance(A, InterfaceAdapter):
        record('T21', 'two-stage path', 'SKIP', 'adapter has no two-stage entry point', binding=False)
        return
    k, a, x, y, z, nb, gnb, g = _real_case(A, 221)
    b = A.bind(nb, gnb, (x, y, z))
    fs = A.raw(g.out, k, x, y, z, a)
    one = A.admit(g.out, k, x, y, z, a, nb, gnb, C_TEST, 1.0, tolset())
    two = A.admit_two_stage(fs.result, b.out, C_TEST, 1.0, tolset())
    same = one.ok and two.ok and all(np.array_equal(np.asarray(one.out[key]), np.asarray(two.out[key]))
                                     for key in ('dn', 'grad_dn', 'dphi', 'gdphi'))
    check('T21', 'admit_scalar_force(exact_finite_sum(...)) == exact_scalar_force(...) bitwise', same,
          '%s | %s' % (one.describe(), two.describe()))
    out, allok = [], True
    x2 = x.copy()
    x2[2] = np.nextafter(x2[2], np.inf)
    b2 = A.bind(nb, gnb, (x2, y, z))
    o = A.admit_two_stage(fs.result, b2.out, C_TEST, 1.0, tolset())
    allok = allok and b2.ok and not o.ok
    out.append('finite sum on P, base bound to P (one x ulp) -> %s' % (vs(o) if not o.ok else 'COMPLETE (WRONG)'))
    forged = dict(fs.result)
    dn_f = np.array(fs.result['dn_complex'], copy=True)
    dn_f[0] += 1.0
    forged['dn_complex'] = dn_f
    o = A.admit_two_stage(forged, b.out, C_TEST, 1.0, tolset())
    allok = allok and not o.ok
    out.append('finite-sum dict with altered dn -> %s' % (vs(o) if not o.ok else 'COMPLETE (WRONG)'))
    partial = dict(fs.result)
    partial['status'] = 'FAILED_CLOSED'
    o = A.admit_two_stage(partial, b.out, C_TEST, 1.0, tolset())
    allok = allok and not o.ok
    out.append('non-COMPLETE finite sum -> %s' % (vs(o) if not o.ok else 'COMPLETE (WRONG)'))
    forged_b = dict(b.out)
    nb_f = np.array(b.out['n_base_complex'], copy=True) if 'n_base_complex' in b.out else None
    if nb_f is not None:
        nb_f[0] += 0.1
        forged_b['n_base_complex'] = nb_f
        o = A.admit_two_stage(fs.result, forged_b, C_TEST, 1.0, tolset())
        allok = allok and not o.ok
        out.append('bound base with altered n_b -> %s' % (vs(o) if not o.ok else 'COMPLETE (WRONG)'))
    check('T21', 'raw finite-sum result and bound base are identity/integrity-checked at admission', allok,
          ' ; '.join(out))
    # retention on failure (advisory)
    nb_bad = nb.copy()
    nb_bad[3] = -2.0
    o = A.admit(g.out, k, x, y, z, a, nb_bad, gnb, C_TEST, 1.0, tolset())
    ret = o.result.get('retained') if isinstance(o.result, dict) else None
    has = isinstance(ret, dict) and ret.get('dn_complex') is not None
    check('T21', 'failure (Nb<=0) returns FAILED_CLOSED with retained complex dn/grad_dn', (not o.ok) and has,
          '%s; retained keys %s' % (o.describe(), sorted(ret) if isinstance(ret, dict) else ret), binding=False)
    # multi-dimensional point shape (INTERFACE: any ndim >= 1)
    k2, a2 = make_waves(222)
    xs, ys, zs = make_points(223)
    n = (len(xs) // 3) * 3
    X, Y, Z = (v[:n].reshape(3, n // 3).copy() for v in (xs, ys, zs))
    g2 = A.prepare(k2, X, Y, Z, limit=A.limit_for(k2, 4), chunk=2)
    o2 = A.raw(g2.out, k2, X, Y, Z, a2) if g2.ok else g2
    ok2 = o2.ok and np.shape(o2.out['dn']) == (3, n // 3) and np.shape(o2.out['grad_dn']) == (3, n // 3, 3)
    if ok2:
        d, gd = oracle(k2, a2, X.ravel(), Y.ravel(), Z.ravel())
        f_s, g_s = scales(k2, a2)
        e = max(err_field(np.asarray(o2.out['dn']).ravel(), d, f_s),
                err_grad(np.asarray(o2.out['grad_dn']).reshape(-1, 3), gd, g_s))
        ok2 = e <= REL
    check('T21', '2-D point shape preserved and == oracle', ok2, o2.describe(), binding=False)


# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--module', required=True)
    ap.add_argument('--interface')
    ap.add_argument('--outdir', required=True)
    ap.add_argument('--only')
    args = ap.parse_args()
    module_path = os.path.abspath(args.module)
    iface = args.interface or os.path.join(os.path.dirname(module_path), 'INTERFACE_0455_V001.md')
    msha = sha256_file(module_path)
    isha = sha256_file(iface)
    fsha = sha256_file(os.path.abspath(__file__))
    tsha = sha256_file(TASK_0455[0])
    print('module    %s  %s' % (msha, module_path))
    print('interface %s  %s' % (isha, iface))
    print('fixtures  %s  %s' % (fsha, os.path.abspath(__file__)))
    print('task0455  %s  match=%s' % (tsha, tsha == TASK_0455[1]))
    if tsha != TASK_0455[1]:
        raise SystemExit('task pin mismatch: stop')
    with open(iface, 'r') as handle:
        itext = handle.read()
    module = load_path(module_path, 'unt0455_module_under_test')
    A = make_adapter(module, itext)
    print('discovered entry points from INTERFACE: %s' % A.discovered)
    print('adapter: %s' % A.describe())
    tests = [('T00', t00_oracle, (A,)), ('T01', t01_direct, (A,)), ('T02', t02_reorder, (A,)),
             ('T03', t03_duplicates, (A,)), ('T04', t04_holes, (A,)), ('T05', t05_points, (A,)),
             ('T06', t06_signs, (A,)), ('T07', t07_linear, (A,)), ('T08', t08_lapse, (A,)),
             ('T08', t08b_units, (A,)), ('T09', t09_reality, (A,)), ('T10', t10_length, (A,)),
             ('T11', t11_nb, (A,)), ('T12', t12_identity, (A,)), ('T13', t13_refresh, (A,)),
             ('T14', t14_limit, (A,)), ('T15', t15_chunk, (A,)), ('T16', t16_immutable, (A,)),
             ('T17', t17_fpe, (A,)), ('T18', t18_hessian, (A,)), ('T19', t19_inert, (A, module_path)), ('T20', t20_lattice, (A,)), ('T21', t21_two_stage, (A,))]
    only = set(args.only.split(',')) if args.only else None
    t0 = time.time()
    for tid, fn, fargs in tests:
        if only and tid not in only:
            continue
        run_test(tid, fn, *fargs)
    elapsed = time.time() - t0
    binding = [r for r in RESULTS if r['binding']]
    summary = dict(module=module_path, module_sha256=msha, interface=iface, interface_sha256=isha,
                   fixtures_sha256=fsha, task_sha256=tsha, adapter=A.describe(), discovered=A.discovered,
                   binding_pass=sum(r['verdict'] == 'PASS' for r in binding),
                   binding_total=len(binding),
                   advisory_pass=sum(r['verdict'] == 'PASS' for r in RESULTS if not r['binding']),
                   advisory_total=sum(1 for r in RESULTS if not r['binding']),
                   elapsed_s=round(elapsed, 3), numpy=np.__version__, python=sys.version.split()[0],
                   results=RESULTS)
    os.makedirs(args.outdir, exist_ok=True)
    path = os.path.join(args.outdir, 'fixtures_0455_result_%s.json' % msha[:16])
    with open(path, 'w') as handle:
        json.dump(summary, handle, indent=1, default=str)
    print('BINDING %d/%d PASS; ADVISORY %d/%d PASS; %.2fs; result %s'
          % (summary['binding_pass'], summary['binding_total'], summary['advisory_pass'],
             summary['advisory_total'], elapsed, path))
    return 0 if summary['binding_pass'] == summary['binding_total'] else 1


if __name__ == '__main__':
    sys.exit(main())
