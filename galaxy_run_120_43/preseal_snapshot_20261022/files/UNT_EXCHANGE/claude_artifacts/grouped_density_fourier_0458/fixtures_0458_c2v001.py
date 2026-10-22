#!/usr/bin/env python3
"""UNT 0458 independent fixtures, c2v001 (fixture-author role; SYNTHETIC inputs only).

Usage (root interpreter, isolated, single-thread BLAS env):
  VECLIB_MAXIMUM_THREADS=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -I -B fixtures_0458_c2v001.py --module PATH [--interface PATH] [--only T05,T13]
                                        [--quick] [--json-out NEW_PATH] [--api-map JSON]

What it does
  * prints the sha256 of the module under test (computed from the bytes it executes),
    verifies the pinned 0445 contraction and Jn provider from bytes, and loads all three by
    importlib from those verified bytes (no project data, NPZ or root worker);
  * discovers the public prepare / evaluate / 0445-keyword adapter entry points named in
    INTERFACE_0458_V001.md (prepare_geometry, evaluate_mode, bind_0445_adapter for the
    frozen v001 API) and maps canonical fixture calls onto them in a THIN ADAPTER LAYER
    (class Api); --api-map can override names without editing this file;
  * oracles: (i) an independent direct sum written from the 0445 equation (per wave and q,
    cmath.exp, math.fsum of real/imaginary parts, both branch sums kept separately) and
    (ii) the pinned original 0445 contraction run on the same synthetic inputs;
  * tests T01..T22 (see TESTS): inert import, lane AST scan, signatures, exact grouping
    counts, equivalence m=1..6, zero rho, real- but not complex-linearity, branch isolation,
    zero-k_perp guard and provider faults, duplicates/holes/permutations, every q once,
    A/B/A refresh, stale identity, cache tamper and changed convention, errstate/overflow
    retention, memory-entry caps (exact boundary by bisection, before allocation), no dense
    nq*nk table, interruption retention, unmutated inputs, adapter contract vs 0445,
    provenance, chunk invariance.
Comparisons are normalized per wave by |c^2 2pi| * SUM_q |w_q J_m| 2|rho_q| (the absolute
term scale of the finite sum); where that scale is exactly 0 the values must be exactly 0.
Writes nothing except the optional --json-out summary (exclusive create). Exit 1 on any
FAIL/ERROR. Floating-point state: tests set np.errstate locally where stated.
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
import time
import tracemalloc
import traceback
from collections.abc import Mapping

import numpy as np

PIN_0445 = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/nonzero_density_fourier_0445/'
            'nonzero_density_fourier_c2v001.py',
            '255e09f4889b6ed470e3424d3a3c41f3a21c433f3095e04ea12af7a96bc5aaf4')
PIN_PROVIDER = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/nonzero_density_fourier_0445/'
                'posix_libm_bessel_jn_provider_c2v001.py',
                '9ec3f1c9fb8afe1ffa4a2bb24df5daf4d2695aa51574984658cb753cfc304f67')
DEFAULT_INTERFACE = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/grouped_density_fourier_0458/'
                     'INTERFACE_0458_V001.md')
KEYWORDS_0445 = ('radius_m', 'z_m', 'weights_RdRdz_m3', 'rho_mode_kg_m3', 'k_physical_inverse_m',
                 'c_m_s', 'mode', 'bessel_jn', 'wave_chunk', 'position_chunk')
TOL = 1e-13          # normalized agreement bound for module vs either oracle
SENSITIVE = 1e-6     # a wrong law must differ from the module by at least this (normalized)
UNIT = (complex(1.0, 0.0), complex(0.0, -1.0), complex(-1.0, 0.0), complex(0.0, 1.0))  # (-i)^m

RESULTS = []
CTX = {}


# =========================================================================== bookkeeping

def record(tid, name, level, detail):
    RESULTS.append(dict(id=tid, name=name, result=level, detail=detail))
    print('[%s] %-4s %s :: %s' % (level, tid, name, detail), flush=True)


def check(tid, name, ok, detail, warn=False):
    record(tid, name, 'PASS' if ok else ('WARN' if warn else 'FAIL'), detail)
    return ok


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def load_from_bytes(path, expected, name):
    data = open(path, 'rb').read()
    digest = sha256_bytes(data)
    if expected is not None and digest != expected:
        raise SystemExit('PIN MISMATCH %s: %s != %s' % (path, digest, expected))
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    exec(compile(data, path, 'exec'), module.__dict__)
    return module, digest, data


# =========================================================================== oracle (i)

def direct_oracle(waves, R, z, w, rho, c, m, jn, law='0445'):
    """Independent direct finite sum from the 0445 equation, per wave and per q.

    deltaJ_m(k) = -c^2 2pi (-i)^m SUM_q w_q J_m(kperp R_q) exp(-i kz z_q)
                  [rho_q exp(+i m alpha) + conj(rho_q) exp(-i m alpha)]
    kperp = np.hypot(kx, ky), alpha = np.arctan2(ky, kx) on the signed inputs.
    law != '0445' gives deliberately WRONG variants used only to prove sensitivity.
    Returns dict(total, plus, minus, scale) of (nk,) arrays.
    """
    waves = np.asarray(waves, dtype=np.float64)
    R = np.asarray(R, dtype=np.float64)
    z = np.asarray(z, dtype=np.float64)
    w = np.asarray(w, dtype=np.float64)
    rho = np.asarray(rho, dtype=np.complex128)
    pref = -(c * c) * (2.0 * math.pi)
    unit = UNIT[m % 4] if law != 'plus_i_power' else UNIT[(-m) % 4]
    if law == 'extra2':
        pref = 2.0 * pref
    nk = waves.shape[0]
    total = np.empty(nk, dtype=np.complex128)
    plus = np.empty(nk, dtype=np.complex128)
    minus = np.empty(nk, dtype=np.complex128)
    scale = np.empty(nk, dtype=np.float64)
    for k in range(nk):
        kx, ky, kz = float(waves[k, 0]), float(waves[k, 1]), float(waves[k, 2])
        kperp = float(np.hypot(kx, ky))
        alpha = float(np.arctan2(ky, kx))
        if law == 'alpha_swapped':
            alpha = float(np.arctan2(kx, ky))
        J = np.asarray(jn(m, np.array([kperp * float(r) for r in R], dtype=np.float64)))
        ep = cmath.exp(1j * (m * alpha))
        em = cmath.exp(-1j * (m * alpha))
        pr, pi_, mr, mi, sc = [], [], [], [], []
        for q in range(R.shape[0]):
            phase = kz * float(z[q])
            vert = cmath.exp(-1j * phase)
            vert_minus = cmath.exp(1j * phase) if law == 'conj_vertical_minus' else vert
            b = float(w[q]) * float(J[q])
            r = complex(rho[q])
            rm = r if law == 'no_conj_minus' else r.conjugate()
            if law == 'drop_minus':
                rm = 0j
            a = b * vert * r
            d = b * vert_minus * rm
            pr.append(a.real); pi_.append(a.imag); mr.append(d.real); mi.append(d.imag)
            sc.append(abs(b) * 2.0 * abs(r))
        P = complex(math.fsum(pr), math.fsum(pi_))
        M = complex(math.fsum(mr), math.fsum(mi))
        plus[k] = pref * (unit * (P * ep))
        minus[k] = pref * (unit * (M * em))
        tp, tm = P * ep, M * em
        total[k] = pref * (unit * complex(math.fsum([tp.real, tm.real]), math.fsum([tp.imag, tm.imag])))
        scale[k] = abs(pref) * math.fsum(sc)
    return dict(total=total, plus=plus, minus=minus, scale=scale)


def nerr(a, b, scale):
    """max |a-b| / scale; inf if scale==0 somewhere and a or b is not exactly 0 there."""
    a = np.asarray(a, dtype=np.complex128)
    b = np.asarray(b, dtype=np.complex128)
    scale = np.asarray(scale, dtype=np.float64)
    zero = scale == 0.0
    if np.any(zero & ((a != 0) | (b != 0))):
        return math.inf
    if not np.any(~zero):
        return 0.0
    return float(np.max(np.abs(a[~zero] - b[~zero]) / scale[~zero]))


# =========================================================================== oracle (ii)

def run_0445(case, rho, m, c=None, jn=None, wave_chunk=5, position_chunk=7):
    return CTX['m0445'].nonzero_mode_density_fourier(
        radius_m=case['R'], z_m=case['z'], weights_RdRdz_m3=case['w'], rho_mode_kg_m3=rho,
        k_physical_inverse_m=case['waves'], c_m_s=case['c'] if c is None else c, mode=m,
        bessel_jn=CTX['jn'] if jn is None else jn, wave_chunk=wave_chunk,
        position_chunk=position_chunk)


# =========================================================================== synthetic cases

def case_irregular():
    """Signed irregular waves with duplicates/holes/zero-kperp; R groups with free z, w."""
    groups = [
        (0.37, [(0.2, 0.010), (-0.0, 0.011), (1.9, 0.012)]),
        (float(np.nextafter(0.37, 1.0)), [(0.2, 0.020)]),           # 1-ulp distinct radius
        (1.1, [(-0.5, 0.013), (0.0, 0.017), (0.2, 0.019), (0.2, 0.023)]),
        (2.9, [(1.3, 0.031), (-2.1, 0.029)]),
        (5.03, [(0.7, 0.05)]),
        (0.81, [(-1.7, 0.007), (3.3, 0.0071), (-0.25, 0.0093), (0.6, 0.0101)]),
        (3.75, [(0.2, 0.041), (-0.5, 0.043), (1.3, 0.047), (0.05, 0.039), (-0.0, 0.037)]),
        (7.2, [(2.5, 0.061), (-2.5, 0.067)]),
        (1.1, [(0.2, 0.019)]),                                       # exact duplicate q
    ]
    rows = [(r, zz, ww) for r, members in groups for zz, ww in members]
    perm = [13, 2, 19, 7, 0, 22, 11, 5, 16, 1, 9, 20, 3, 14, 8, 21, 6, 17, 12, 4, 18, 10, 15]
    assert sorted(perm) == list(range(len(rows)))
    rows = [rows[i] for i in perm]
    R = np.array([r for r, _, _ in rows])
    z = np.array([zz for _, zz, _ in rows])
    w = np.array([ww for _, _, ww in rows])
    half_up = float(np.nextafter(0.5, 1.0))
    waves = np.array([
        [3., 4., 0.5], [4., 3., 0.5], [-3., -4., -0.5], [-3., 4., 0.5], [3., -4., 0.5],
        [5., 0., 0.5], [0., 5., 0.5], [-5., -0.0, 0.5], [-5., 0.0, 0.5], [0., -5., -0.5],
        [0., 0., 1.0], [-0.0, 0.0, 0.5], [0.0, -0.0, -0.5], [-0.0, -0.0, 0.0], [0., 0., -0.0],
        [1.1, -2.3, 0.0], [-1.1, 2.3, -0.0], [2.3, -1.1, 0.0],
        [3., 4., 0.5], [3., 4., 0.5],                                 # exact duplicates
        [0.7, 0.2, 2.2], [0.2, 0.7, -1.3], [-0.7, -0.2, -2.2],
        [0.3, 0.4, 0.5], [0.5, 0.0, half_up],                         # kz 1 ulp apart
        [1e-3, 2e-3, 0.5], [6.1, -0.4, 3.7], [-2.2, 1.9, -3.7], [12.5, 0.0, 0.25],
        [-6.1, 0.4, -3.7], [0.0, 0.0, 3.7], [1.7, 1.7, -1.3], [-1.7, -1.7, 1.3],
        [4., 3., -0.5], [-4., -3., 0.5], [2.3, -1.1, 0.0],
    ], dtype=np.float64)
    return dict(name='irregular', R=R, z=z, w=w, waves=waves, c=2.0,
                chunks=dict(position_chunk=5, perp_chunk=3, cell_chunk=2))


def case_random(seed=458, nk_base=150, nk_dup=30, nq=240, n_r=12):
    rng = np.random.default_rng(seed)
    lattice = rng.integers(-4, 5, size=(nk_base, 3)).astype(np.float64)
    lattice *= np.array([0.37, 0.37, 0.29])
    dups = lattice[rng.integers(0, nk_base, size=nk_dup)]
    extra = np.array([[0.0, 0.0, 0.29], [-0.0, 0.0, -0.58], [0.37, -0.0, 0.0]])
    waves = np.concatenate([lattice, dups, extra])
    waves = waves[rng.permutation(waves.shape[0])]
    r_unique = np.sort(rng.uniform(0.1, 9.0, size=n_r))
    R = r_unique[rng.integers(0, n_r, size=nq)]
    z_choices = np.concatenate([np.linspace(-3.0, 3.0, 25), rng.uniform(-4, 4, size=10)])
    z = z_choices[rng.integers(0, z_choices.shape[0], size=nq)]
    w = rng.uniform(0.001, 0.05, size=nq)
    return dict(name='random', R=R, z=z, w=w, waves=waves, c=3.0,
                chunks=dict(position_chunk=37, perp_chunk=4, cell_chunk=3))


def case_wide(nq=8000, nk=1000, n_r=40, n_z=50, seed=4580):
    """Large nq*nk (dense table would be nq*nk*16 B) with few unique groups."""
    rng = np.random.default_rng(seed)
    grid = np.arange(-3, 4) * 0.5
    kx = grid[rng.integers(0, 7, size=nk)]
    ky = grid[rng.integers(0, 7, size=nk)]
    kz = (np.arange(8) - 3.5)[rng.integers(0, 8, size=nk)] * 0.21
    waves = np.stack([kx, ky, kz], axis=1)
    r_unique = rng.uniform(0.2, 6.0, size=n_r)
    z_unique = rng.uniform(-2.0, 2.0, size=n_z)
    R = r_unique[rng.integers(0, n_r, size=nq)]
    z = z_unique[rng.integers(0, n_z, size=nq)]
    w = rng.uniform(0.001, 0.02, size=nq)
    return dict(name='wide', R=R, z=z, w=w, waves=waves, c=1.5,
                chunks=dict(position_chunk=2000, perp_chunk=4, cell_chunk=8))


def rho_random(n, seed):
    rng = np.random.default_rng(seed)
    return (rng.normal(size=n) + 1j * rng.normal(size=n)).astype(np.complex128)


def group_counts(case):
    """Independent grouping counts (exact float64 equality, as np.unique)."""
    waves = case['waves']
    kperp = np.hypot(waves[:, 0], waves[:, 1])
    kz = waves[:, 2]
    cells = set(zip(kz.tolist(), kperp.tolist()))       # -0.0 == 0.0 as Python floats
    cells_bits = set(zip([v.tobytes() for v in kz], [v.tobytes() for v in kperp]))
    per_kz = {}
    for zb, pb in cells_bits:
        per_kz.setdefault(zb, set()).add(pb)
    return dict(nk=int(waves.shape[0]), nq=int(case['R'].shape[0]),
                n_kz_unique=int(np.unique(kz).shape[0]),
                n_kz_unique_bitwise=len({v.tobytes() for v in kz}),
                n_perp_unique=int(np.unique(kperp).shape[0]),
                n_R_unique=int(np.unique(case['R']).shape[0]),
                filled_cells=len(cells), n_cells_bitwise=len(cells_bits),
                max_cells_per_kz_bitwise=max(len(v) for v in per_kz.values()))


# =========================================================================== THIN ADAPTER LAYER
# Canonical fixture calls -> the frozen 0458 entry points discovered from INTERFACE_0458_V001.md:
#   api.prepare(case, modes, limits=None, jn=None, controls=None) -> prepare result dict
#   api.geometry(prep_result) -> bound geometry record
#   api.evaluate(geometry, case, rho, m, c=None, jn=None, wave_chunk=, position_chunk=) -> dict
#   api.adapter(geometry, case, rho, m, ...) -> dict through the 0445-keyword adapter
#   api.adapter_call(geometry, kwargs_0445) -> dict
# Supported adapter shapes: (a) a binder f(*, geometry) returning a callable with exactly
# the 0445 keywords, (b) a function with the 0445 keywords plus one geometry keyword.

CANDIDATES = dict(
    radius=('radius_m',), z=('z_m',), weights=('weights_RdRdz_m3',),
    waves=('k_physical_inverse_m', 'wavevectors'),
    modes=('modes', 'mode_set', 'bound_modes'), rho=('rho_mode_kg_m3',), mode=('mode',),
    c=('c_m_s',), geometry=('geometry', 'bound_geometry', 'prepared_geometry'),
    provider=('jn_provider', 'bessel_jn_provider', 'provider', 'bessel_jn'))
API_MAP = {}
DEFAULT_CONTROLS = dict(position_chunk=64, perp_chunk=8, cell_chunk=16)
GENEROUS = 10 ** 12

# Exact memory-entry formulas per prepare limit keyword, transcribed from the frozen
# INTERFACE (prepare_geometry docstring / scaling()): g holds the fixture's INDEPENDENT
# counts plus the prepare controls.  T16 also measures every threshold by bisection.
FORMULA_NAMES = ('nq', 'nk', 'n_kz_unique', 'n_perp_unique', 'n_R_unique', 'n_modes', 'n_cells',
                 'max_cells_per_kz', 'position_chunk', 'perp_chunk', 'cell_chunk')
LIMIT_FORMULA_TEXT = {
    'max_vertical_entries': 'n_kz_unique * nq',
    'max_bessel_entries': 'n_modes * n_perp_unique * n_R_unique',
    'max_angular_entries': 'n_modes * nk',
    'max_work_entries': '4 * nq + 2 * n_R_unique * n_kz_unique + 2 * n_cells + nk',
    'max_block_entries': ('max(min(position_chunk, nq) * n_kz_unique, '
                          'min(perp_chunk, n_perp_unique) * n_R_unique, '
                          'min(cell_chunk, max_cells_per_kz) * n_R_unique)'),
}


def safe_formula(text):
    """Integer arithmetic (+ - * //, min, max) over FORMULA_NAMES only; no eval."""
    tree = ast.parse(text, mode='eval')
    for node in ast.walk(tree):
        ok = isinstance(node, (ast.Expression, ast.BinOp, ast.Add, ast.Sub, ast.Mult,
                               ast.FloorDiv, ast.Load, ast.UnaryOp, ast.USub, ast.Call, ast.Name,
                               ast.Constant))
        if isinstance(node, ast.Name) and node.id not in FORMULA_NAMES + ('min', 'max'):
            ok = False
        if isinstance(node, ast.Constant) and type(node.value) is not int:
            ok = False
        if isinstance(node, ast.Call) and not (isinstance(node.func, ast.Name)
                                               and node.func.id in ('min', 'max')):
            ok = False
        if not ok:
            raise ValueError('formula %r uses a disallowed construct' % text)

    def value(node, g):
        if isinstance(node, ast.Expression):
            return value(node.body, g)
        if isinstance(node, ast.Constant):
            return node.value
        if isinstance(node, ast.Name):
            return g[node.id]
        if isinstance(node, ast.UnaryOp):
            return -value(node.operand, g)
        if isinstance(node, ast.Call):
            args = [value(a, g) for a in node.args]
            return min(args) if node.func.id == 'min' else max(args)
        a, b = value(node.left, g), value(node.right, g)
        return {ast.Add: a + b, ast.Sub: a - b, ast.Mult: a * b,
                ast.FloorDiv: a // b if b else None}[type(node.op)]
    return lambda g: value(tree, g)


def _pick(params, role, fn_role=None):
    mapped = API_MAP.get('param_map', {}).get(fn_role or '', {}).get(role)
    if mapped is not None:
        return mapped if mapped in params else None
    for name in CANDIDATES[role]:
        if name in params:
            return name
    return None


class Api:
    """Thin adapter layer (the only module-shape-specific code in this fixture)."""

    out_key = 'deltaJ0_J'
    retained_pairs = (('retained_deltaJ0_J', 'retained_wave_mask'),)
    retained_keys = ('retained_deltaJ0_J', 'retained_wave_mask')

    def __init__(self, prepare_fn, evaluate_fn, binder_fn, adapter_fn, provider, interrupt_attrs,
                 geometry_key):
        self.prepare_fn, self.evaluate_fn = prepare_fn, evaluate_fn
        self.binder_fn, self.adapter_fn = binder_fn, adapter_fn
        self.provider = provider
        self.interrupt_attrs = interrupt_attrs
        self.geometry_key = geometry_key
        self.p_prepare = list(inspect.signature(prepare_fn).parameters)
        self.p_evaluate = list(inspect.signature(evaluate_fn).parameters)
        self.limit_names = [p for p in self.p_prepare if p.startswith('max_') or 'limit' in p]
        self.control_names = [p for p in self.p_prepare if 'chunk' in p]
        self.evaluate_0445_shaped = set(KEYWORDS_0445) <= set(self.p_evaluate)
        self.evaluate_takes_inputs = bool(_pick(self.p_evaluate, 'radius', 'evaluate'))
        if adapter_fn is not None:
            self.adapter_geometry_name = [p for p in inspect.signature(adapter_fn).parameters
                                          if p not in KEYWORDS_0445][0]
        self._bound = []

    def describe(self):
        return ('prepare=%s%s controls=%s limits=%s | evaluate=%s%s (0445-shaped=%s) | adapter=%s '
                '| geometry_key=%r | interrupt_attrs=%s'
                % (self.prepare_fn.__name__, tuple(self.p_prepare), self.control_names,
                   self.limit_names, self.evaluate_fn.__name__, tuple(self.p_evaluate),
                   self.evaluate_0445_shaped,
                   ('binder %s(*, geometry) -> 0445-keyword callable' % self.binder_fn.__name__)
                   if self.binder_fn else ('%s(+%s)' % (self.adapter_fn.__name__,
                                                        self.adapter_geometry_name)),
                   self.geometry_key, self.interrupt_attrs))

    # ---------------------------------------------------------------- provider plumbing
    def provider_dict(self, jn):
        if jn is None or jn is self.provider['bessel_jn']:
            return self.provider
        forged = dict(self.provider)
        forged['bessel_jn'] = jn
        return forged

    def jn_for(self, geometry):
        for bound_geometry, jn in reversed(self._bound):
            if bound_geometry is geometry:
                return jn
        return self.provider['bessel_jn']

    # ---------------------------------------------------------------- calls
    def controls_for(self, case, controls=None):
        merged = dict(DEFAULT_CONTROLS, **case.get('chunks', {}))
        merged.update(controls or {})
        return {name: merged[name] for name in self.control_names}

    def generous_limits(self, case, modes):
        return {name: GENEROUS for name in self.limit_names}

    def formula_counts(self, case, modes, controls=None):
        g = group_counts(case)
        out = dict(nq=g['nq'], nk=g['nk'], n_kz_unique=g['n_kz_unique_bitwise'],
                   n_perp_unique=g['n_perp_unique'], n_R_unique=g['n_R_unique'],
                   n_modes=len(modes), n_cells=g['n_cells_bitwise'],
                   max_cells_per_kz=g['max_cells_per_kz_bitwise'])
        out.update(self.controls_for(case, controls))
        return out

    def required_limits(self, case, modes, controls=None):
        g = self.formula_counts(case, modes, controls)
        return {name: int(LIMIT_FORMULAS[name](g)) for name in self.limit_names
                if name in LIMIT_FORMULAS}

    def empirical_threshold(self, case, modes, name, hi=GENEROUS):
        def accepted(value):
            limits = self.generous_limits(case, modes)
            limits[name] = value
            return is_complete(self.prepare(case, modes, limits=limits))
        if not accepted(hi):
            return None
        lo = 0
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if accepted(mid):
                hi = mid
            else:
                lo = mid
        return hi

    def prepare(self, case, modes, limits=None, jn=None, controls=None):
        p = self.p_prepare
        kw = {_pick(p, 'radius', 'prepare'): case['R'], _pick(p, 'z', 'prepare'): case['z'],
              _pick(p, 'weights', 'prepare'): case['w'], _pick(p, 'waves', 'prepare'): case['waves'],
              _pick(p, 'modes', 'prepare'): tuple(modes)}
        pname = _pick(p, 'provider', 'prepare')
        kw[pname] = self.provider_dict(jn) if 'provider' in pname else \
            (jn or self.provider['bessel_jn'])
        kw.update(self.controls_for(case, controls))
        kw.update(limits if limits is not None else self.generous_limits(case, modes))
        missing = [x for x in p if x not in kw]
        if missing:
            raise TypeError('fixture API layer cannot fill prepare params %s' % missing)
        result = self.prepare_fn(**kw)
        if is_complete(result):
            self._bound.append((self.geometry(result), jn or self.provider['bessel_jn']))
        return result

    def geometry(self, result):
        return result.get(self.geometry_key) if isinstance(result, Mapping) else None

    def counts(self, result):
        geometry = self.geometry(result)
        out = {}
        for source in (result.get('counts'),
                       geometry.get('counts') if isinstance(geometry, Mapping) else None):
            if isinstance(source, Mapping):
                for key, value in source.items():
                    out.setdefault(API_MAP.get('counts_map', {}).get(key, key), value)
        return out

    def kwargs_0445(self, geometry, case, rho, m, c=None, jn=None, wave_chunk=5, position_chunk=7):
        return dict(radius_m=case['R'], z_m=case['z'], weights_RdRdz_m3=case['w'],
                    rho_mode_kg_m3=rho, k_physical_inverse_m=case['waves'],
                    c_m_s=case['c'] if c is None else c, mode=m,
                    bessel_jn=self.jn_for(geometry) if jn is None else jn,
                    wave_chunk=wave_chunk, position_chunk=position_chunk)

    def evaluate(self, geometry, case, rho, m, c=None, jn=None, wave_chunk=5, position_chunk=7):
        p = self.p_evaluate
        if self.evaluate_0445_shaped:
            kw = self.kwargs_0445(geometry, case, rho, m, c, jn, wave_chunk, position_chunk)
        else:
            kw = {_pick(p, 'rho', 'evaluate'): rho, _pick(p, 'mode', 'evaluate'): m}
            if _pick(p, 'c', 'evaluate'):
                kw[_pick(p, 'c', 'evaluate')] = case['c'] if c is None else c
        kw[_pick(p, 'geometry', 'evaluate')] = geometry
        missing = [x for x in p if x not in kw]
        if missing:
            raise TypeError('fixture API layer cannot fill evaluate params %s' % missing)
        return self.evaluate_fn(**kw)

    def bind(self, geometry):
        """Binder style: (binding dict, callable or None)."""
        binding = self.binder_fn(geometry=geometry)
        fn = None
        if isinstance(binding, Mapping):
            fn = binding.get('density_fourier')
            if fn is None:
                fns = [v for v in binding.values() if callable(v)]
                fn = fns[0] if len(fns) == 1 else None
        return binding, fn

    def adapter_call(self, geometry, kwargs):
        if self.binder_fn is not None:
            binding, fn = self.bind(geometry)
            if fn is None:
                return binding
            return fn(**kwargs)
        return self.adapter_fn(**dict(kwargs, **{self.adapter_geometry_name: geometry}))

    def adapter(self, geometry, case, rho, m, c=None, jn=None, wave_chunk=5, position_chunk=7):
        return self.adapter_call(geometry, self.kwargs_0445(geometry, case, rho, m, c, jn,
                                                            wave_chunk, position_chunk))


LIMIT_FORMULAS = {}


def discover_entry_points(module, interface_text):
    names = re.findall(r'\b([A-Za-z_][A-Za-z0-9_]*)\s*\(\s*\*', interface_text)
    names += re.findall(r'def\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(', interface_text)
    names += re.findall(r'`([A-Za-z_][A-Za-z0-9_]*)`', interface_text)
    names += re.findall(r'`([A-Za-z_][A-Za-z0-9_]*)\(', interface_text)
    funcs = []
    for name in dict.fromkeys(names):
        obj = getattr(module, name, None)
        if not name.startswith('_') and inspect.isfunction(obj) and \
                obj.__module__ == module.__name__:
            funcs.append(name)
    prepare = [n for n in funcs if 'prepare' in n]
    evaluate = [n for n in funcs if 'evaluat' in n]
    binder = [n for n in funcs if ('bind' in n or 'adapter' in n) and n not in prepare + evaluate
              and set(inspect.signature(getattr(module, n)).parameters) == {'geometry'}]
    adapter = [n for n in funcs if n not in prepare + evaluate + binder and
               set(KEYWORDS_0445) < set(inspect.signature(getattr(module, n)).parameters)]
    return dict(all=funcs, prepare=prepare, evaluate=evaluate, binder=binder, adapter=adapter)


def build_api(module, interface_text, provider, prov):
    found = discover_entry_points(module, interface_text)
    print('INTERFACE-named public functions: %s' % found)
    for role in ('prepare', 'evaluate', 'binder', 'adapter'):
        if API_MAP.get(role):
            found[role] = [API_MAP[role]]
            print('API-MAP override: %s -> %s' % (role, API_MAP[role]))
    for role in ('prepare', 'evaluate'):
        if len(found[role]) != 1:
            raise SystemExit('cannot uniquely discover %s entry point: %s (use --api-map)'
                             % (role, found[role]))
    if len(found['binder']) + len(found['adapter']) != 1:
        raise SystemExit('cannot uniquely discover the 0445-keyword adapter: binder %s adapter %s'
                         % (found['binder'], found['adapter']))
    texts = dict(LIMIT_FORMULA_TEXT, **API_MAP.get('limit_formulas', {}))
    for name, text in texts.items():
        LIMIT_FORMULAS[name] = safe_formula(text)
    attrs = sorted(set(re.findall(r'(unt\d{4}\w*retained\w*)', interface_text)))
    own = [a for a in attrs if a.startswith('unt0458')] or attrs
    interrupt_attrs = dict(evaluate=own, prepare=own, adapter=attrs)
    interrupt_attrs.update(API_MAP.get('interrupt_attrs', {}))
    api = Api(getattr(module, found['prepare'][0]), getattr(module, found['evaluate'][0]),
              getattr(module, found['binder'][0]) if found['binder'] else None,
              getattr(module, found['adapter'][0]) if found['adapter'] else None,
              provider, interrupt_attrs, API_MAP.get('geometry_key', 'geometry'))
    unknown = [n for n in api.limit_names if n not in LIMIT_FORMULAS]
    if unknown:
        print('NOTE: no transcribed formula for limits %s (T16 measures thresholds)' % unknown)
    return api


# =========================================================================== helpers for tests

def out_of(result):
    return result.get(CTX['api'].out_key) if isinstance(result, Mapping) else None


def is_complete(result):
    return isinstance(result, Mapping) and result.get('status') == 'COMPLETE' \
        and result.get('complete') is True


def snapshot(*arrays):
    return [(None if a is None else (np.asarray(a).tobytes(), np.asarray(a).dtype.str,
                                     np.asarray(a).shape,
                                     bool(np.asarray(a).flags.writeable)))
            for a in arrays]


def walk_arrays(obj, path='geometry', seen=None, depth=0):
    """Yield (path, ndarray) for every ndarray reachable through Mappings/sequences/attrs."""
    if seen is None:
        seen = set()
    if id(obj) in seen or depth > 6:
        return
    seen.add(id(obj))
    if isinstance(obj, np.ndarray):
        yield path, obj
        return
    if isinstance(obj, Mapping):
        for key in list(obj.keys()):
            yield from walk_arrays(obj[key], '%s[%r]' % (path, key), seen, depth + 1)
    elif isinstance(obj, (list, tuple)):
        for i, item in enumerate(obj):
            yield from walk_arrays(item, '%s[%d]' % (path, i), seen, depth + 1)
    elif hasattr(obj, '__dict__') and not callable(obj):
        for key, value in vars(obj).items():
            yield from walk_arrays(value, '%s.%s' % (path, key), seen, depth + 1)


def geometry_fingerprint(geometry):
    h = hashlib.sha256()
    for path, array in walk_arrays(geometry):
        h.update(path.encode())
        h.update(np.ascontiguousarray(array).tobytes())
    return h.hexdigest()


class Tracer:
    """Raise KeyboardInterrupt at the n-th 'line' event inside the module under test."""

    def __init__(self, filename, n):
        self.filename, self.n, self.count, self.line, self.stack = filename, n, 0, None, ()

    def _local(self, frame, event, arg):
        if event == 'line':
            self.count += 1
            if self.count == self.n:
                self.line = frame.f_lineno
                lines, f = [], frame
                while f is not None:
                    if f.f_code.co_filename == self.filename:
                        lines.append(f.f_lineno)
                    f = f.f_back
                self.stack = tuple(lines)          # module-file lines, innermost first
                raise KeyboardInterrupt('fixture interrupt at module line %d' % frame.f_lineno)
        return self._local

    def __call__(self, frame, event, arg):
        if frame.f_code.co_filename == self.filename:
            return self._local
        return None


def protected_lines(source):
    """Lines inside a try body that has an `except BaseException` handler, excluding pure
    FORWARDING handlers (those that read an existing record with getattr): an interrupt that
    reaches a forwarder with no inner record legitimately has none (as in 0445 validation).
    """
    lines = set()
    for node in ast.walk(ast.parse(source)):
        if not isinstance(node, ast.Try) or not node.body:
            continue
        for handler in node.handlers:
            t = handler.type
            names = ['BaseException'] if t is None else \
                [t.id] if isinstance(t, ast.Name) else \
                [e.id for e in t.elts if isinstance(e, ast.Name)] if isinstance(t, ast.Tuple) else []
            if 'BaseException' not in names:
                continue
            calls = [c for c in ast.walk(handler) if isinstance(c, ast.Call)]
            callee = [c.func.id if isinstance(c.func, ast.Name) else getattr(c.func, 'attr', '')
                      for c in calls]
            if 'getattr' not in callee:
                lines.update(range(node.body[0].lineno, node.body[-1].end_lineno + 1))
    return lines


# =========================================================================== static tests

INERT_PROBE = r'''
import ast, importlib.util, json, sys, time
path = sys.argv[1]
data = open(path, 'rb').read()
tree = ast.parse(data)
names = set()
for node in tree.body:
    if isinstance(node, ast.Import):
        names.update(a.name for a in node.names)
    elif isinstance(node, ast.ImportFrom) and node.module and not node.level:
        names.add(node.module)
for name in sorted(names):
    __import__(name)
code = compile(data, path, 'exec')
spec = importlib.util.spec_from_file_location('probe0458', path)
module = importlib.util.module_from_spec(spec)
events = []
WATCH = ('open', 'os.', 'subprocess.', 'socket.', 'ctypes.', 'shutil.', 'urllib', 'http',
         'sqlite3', 'glob.', 'pathlib', 'tempfile', 'mmap', 'fcntl', 'signal.')
def hook(event, args):
    if event in ('exec', 'compile', 'import', 'object.__setattr__', 'object.__getattr__',
                 'sys._getframe', 'builtins.id', 'object.__delattr__'):
        return
    if event.startswith(WATCH):
        events.append([event, repr(args)[:160]])
sys.addaudithook(hook)
t0 = time.perf_counter()
exec(code, module.__dict__)
seconds = time.perf_counter() - t0
import numpy as np
arrays = sorted((k, int(v.size)) for k, v in module.__dict__.items() if isinstance(v, np.ndarray))
print(json.dumps(dict(events=events, seconds=seconds, arrays=arrays,
                      public=sorted(k for k in module.__dict__ if not k.startswith('_')))))
'''


def t01_inert_import():
    proc = subprocess.run([sys.executable, '-I', '-B', '-c', INERT_PROBE, CTX['module_path']],
                          capture_output=True, text=True, timeout=120, env=dict(os.environ))
    if proc.returncode != 0:
        return check('T01', 'inert import', False, 'probe failed: ' + proc.stderr[-400:])
    info = json.loads(proc.stdout.strip().splitlines()[-1])
    big = [a for a in info['arrays'] if a[1] > 64]
    ok = not info['events'] and not big and info['seconds'] < 1.0
    return check('T01', 'inert import (subprocess, audit hook after pre-importing deps)', ok,
                 'audit events during module exec=%s; module-level ndarrays=%s; exec %.4fs'
                 % (info['events'][:5], info['arrays'], info['seconds']))


BLAS = {'dot', 'matmul', 'vdot', 'inner', 'tensordot', 'einsum_path', 'multi_dot', 'kron'}
NOWARN = {'seterr', 'errstate', 'filterwarnings', 'simplefilter', 'catch_warnings',
          'suppress_warnings', 'resetwarnings', 'seterrcall'}
FILEIO = {'save', 'savez', 'savez_compressed', 'load', 'loadtxt', 'savetxt', 'genfromtxt',
          'fromfile', 'tofile', 'memmap', 'read_bytes', 'write_bytes', 'read_text', 'write_text'}
APPROX = {'interp', 'vectorize', 'polyfit', 'fft', 'ifft', 'rfft', 'irfft', 'fftn', 'ifftn',
          'rfftn', 'irfftn', 'solve', 'lstsq', 'inv', 'pinv', 'round', 'around', 'isclose',
          'allclose'}
CTOR_OK = {'MappingProxyType', 'dict', 'tuple', 'frozenset', 'set', 'complex', 'float', 'int',
           'str', 'list', 'object', 'namedtuple', 'compile'}


def t02_lane_ast():
    source = CTX['module_source']
    tree = ast.parse(source)
    fails, warns, info = [], [], []
    stdlib = set(getattr(sys, 'stdlib_module_names', ())) | {'__future__'}
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            names = [a.name for a in node.names] if isinstance(node, ast.Import) else \
                ([node.module] if node.module else [])
            for name in names:
                top = name.split('.')[0]
                if top != 'numpy' and top not in stdlib:
                    fails.append('L%d import %s (not numpy/stdlib)' % (node.lineno, name))
                if top in ('warnings', 'pickle', 'shelve', 'io', 'pathlib', 'tempfile',
                           'subprocess', 'socket', 'threading', 'multiprocessing', 'ctypes'):
                    warns.append('L%d imports %s' % (node.lineno, name))
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.MatMult):
            fails.append('L%d @ operator' % node.lineno)
        if isinstance(node, ast.Attribute) and node.attr == 'linalg':
            fails.append('L%d linalg' % node.lineno)
        if isinstance(node, ast.Call):
            f = node.func
            name = f.attr if isinstance(f, ast.Attribute) else (f.id if isinstance(f, ast.Name) else '')
            if name in BLAS:
                fails.append('L%d BLAS-type call %s' % (node.lineno, name))
            if name in NOWARN:
                fails.append('L%d warning/errstate control %s' % (node.lineno, name))
            if name in FILEIO or (isinstance(f, ast.Name) and name in ('open', 'exec', 'eval',
                                                                           'input', '__import__')):
                fails.append('L%d I/O or dynamic call %s' % (node.lineno, name))
            if name in APPROX:
                if isinstance(f, ast.Name) and name == 'round':
                    warns.append('L%d builtin round' % node.lineno)
                else:
                    fails.append('L%d approximation/solver/tolerance call %s' % (node.lineno, name))
            if isinstance(f, ast.Name) and name == 'print':
                warns.append('L%d print' % node.lineno)
            if name == 'einsum':
                opt = [k for k in node.keywords if k.arg == 'optimize']
                if not opt or not (isinstance(opt[0].value, ast.Constant) and opt[0].value.value is False):
                    fails.append('L%d einsum without optimize=False' % node.lineno)
            if name == 'real' or name == 'imag':
                info.append('L%d np.%s(...)' % (node.lineno, name))
        if isinstance(node, ast.Attribute) and node.attr in ('real', 'imag') \
                and isinstance(node.ctx, ast.Load):
            info.append('L%d .%s' % (node.lineno, node.attr))
    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom, ast.FunctionDef, ast.ClassDef)):
            continue
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant):
            continue
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            for sub in ast.walk(node):
                if isinstance(sub, ast.Call):
                    f = sub.func
                    name = f.attr if isinstance(f, ast.Attribute) else getattr(f, 'id', '?')
                    if name not in CTOR_OK:
                        warns.append('L%d top-level call %s in constant' % (node.lineno, name))
            continue
        fails.append('L%d top-level statement %s' % (node.lineno, type(node).__name__))
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and not node.name.startswith('_'):
            a = node.args
            if a.posonlyargs or a.args or a.vararg or a.kwarg:
                fails.append('public %s: non keyword-only parameters' % node.name)
            if any(d is not None for d in a.kw_defaults):
                fails.append('public %s: keyword defaults present' % node.name)
    check('T02', 'lane AST scan (numpy+stdlib, no BLAS/@, einsum optimize=False, no warning '
          'control, no I/O, keyword-only no defaults, definitions-only top level)',
          not fails, 'fails=%s warns=%s' % (fails, warns))
    record('T02b', '.real/.imag reads (for reviewer: complex data must be preserved)', 'INFO',
           '%d occurrences: %s' % (len(info), info[:40]))


def t03_signatures():
    api = CTX['api']
    problems = []
    fns = [('prepare', api.prepare_fn), ('evaluate', api.evaluate_fn)]
    fns.append(('binder', api.binder_fn) if api.binder_fn else ('adapter', api.adapter_fn))
    for role, fn in fns:
        for p in inspect.signature(fn).parameters.values():
            if p.kind is not inspect.Parameter.KEYWORD_ONLY:
                problems.append('%s.%s kind %s' % (role, p.name, p.kind))
            if p.default is not inspect.Parameter.empty:
                problems.append('%s.%s has default' % (role, p.name))
        try:
            fn()
            problems.append('%s() with no args did not raise' % role)
        except TypeError:
            pass
    case = case_irregular()
    geometry, _ = prepared(case)
    if api.binder_fn is not None:
        binding, closure = api.bind(geometry)
        if not (isinstance(binding, Mapping) and binding.get('status') == 'READY' and callable(closure)):
            problems.append('binder did not return READY + callable: %r' % (
                binding.get('status') if isinstance(binding, Mapping) else binding,))
        else:
            params = inspect.signature(closure).parameters
            if set(params) != set(KEYWORDS_0445):
                problems.append('adapter callable params %s != 0445 keywords' % sorted(params))
            for p in params.values():
                if p.kind is not inspect.Parameter.KEYWORD_ONLY or \
                        p.default is not inspect.Parameter.empty:
                    problems.append('adapter callable %s not keyword-only/no-default' % p.name)
        for bogus_name, bogus in (('None', None), ('empty dict', {}), ('prepare result', _)):
            b = api.binder_fn(geometry=bogus)
            if isinstance(b, Mapping) and b.get('status') == 'READY':
                problems.append('binder accepted %s' % bogus_name)
        shape = 'binder %s(*, geometry) -> callable(*, %s)' % (api.binder_fn.__name__,
                                                               ', '.join(KEYWORDS_0445))
    else:
        params = set(inspect.signature(api.adapter_fn).parameters)
        extra = sorted(params - set(KEYWORDS_0445))
        if not set(KEYWORDS_0445) <= params or len(extra) != 1:
            problems.append('adapter params: missing %s extra %s' % (
                sorted(set(KEYWORDS_0445) - params), extra))
        shape = '%s(0445 keywords + %s)' % (api.adapter_fn.__name__, extra)
    check('T03', 'entry points discovered from INTERFACE; keyword-only, no defaults; adapter keeps '
          'the exact 0445 keyword contract with a bound geometry', not problems,
          'prepare=%s evaluate=%s adapter=%s; problems=%s'
          % (api.prepare_fn.__name__, api.evaluate_fn.__name__, shape, problems))


# =========================================================================== numerical tests

def prepared(case, modes=(1, 2, 3, 4, 5, 6), **kw):
    api = CTX['api']
    result = api.prepare(case, modes, **kw)
    if not is_complete(result):
        raise AssertionError('prepare not COMPLETE: %s %s' % (result.get('status'),
                                                              result.get('reason')))
    return api.geometry(result), result


def t04_grouping_counts():
    api = CTX['api']
    problems, details = [], []
    for case in (case_irregular(), case_random()):
        g = group_counts(case)
        _, prep = prepared(case)
        got = api.counts(prep)
        for key in ('nk', 'nq', 'n_perp_unique', 'n_R_unique'):
            if got.get(key) != g[key]:
                problems.append('%s %s: module %r expected %r' % (case['name'], key, got.get(key), g[key]))
        kz_ok = got.get('n_kz_unique') in (g['n_kz_unique'], g['n_kz_unique_bitwise'])
        if not kz_ok:
            problems.append('%s n_kz_unique module %r expected %r (value) or %r (bitwise)' % (
                case['name'], got.get('n_kz_unique'), g['n_kz_unique'], g['n_kz_unique_bitwise']))
        kz_mode = ('bitwise (+0/-0 separate)' if got.get('n_kz_unique') == g['n_kz_unique_bitwise']
                   != g['n_kz_unique'] else 'value-equal' if got.get('n_kz_unique') == g['n_kz_unique']
                   else '?')
        cells = got.get('n_cells')
        if cells is not None and cells not in (g['filled_cells'], g['n_cells_bitwise']):
            problems.append('%s n_cells module %r expected %r/%r' % (
                case['name'], cells, g['filled_cells'], g['n_cells_bitwise']))
        details.append('%s independent=%s module(nk,nq,kz,perp,R,cells)=%s kz grouping %s' % (
            case['name'], g, tuple(got.get(k) for k in ('nk', 'nq', 'n_kz_unique', 'n_perp_unique',
                                                        'n_R_unique', 'n_cells')), kz_mode))
        if g['filled_cells'] >= g['n_kz_unique'] * g['n_perp_unique']:
            problems.append('%s synthetic design has no holes' % case['name'])
    check('T04', 'exact grouping counts (computed hypot / signed kz / R exact-equal; 1-ulp R and kz '
          'stay distinct; holes present)', not problems, '; '.join(details + problems))


def t05_equivalence():
    api = CTX['api']
    worst = dict(oracle=0.0, o0445=0.0, oracle_vs_0445=0.0, adapter_vs_0445=0.0)
    problems = []
    runs = 0
    for case in (case_irregular(), case_random()):
        geometry, _ = prepared(case)
        nq = case['R'].shape[0]
        nk = case['waves'].shape[0]
        perp_zero = np.hypot(case['waves'][:, 0], case['waves'][:, 1]) == 0.0
        for m in range(1, 7):
            base = rho_random(nq, 100 + m)
            variants = dict(complex=base, real=base.real.astype(np.complex128),
                            imag=(1j * base.imag).astype(np.complex128),
                            complex64=base.astype(np.complex64))
            for label, rho in variants.items():
                with np.errstate(all='raise'):
                    got = api.evaluate(geometry, case, rho, m)
                    ref = run_0445(case, rho, m)
                    ada = api.adapter(geometry, case, rho, m)
                runs += 1
                if not is_complete(got) or not is_complete(ref) or not is_complete(ada):
                    problems.append('%s m=%d %s statuses %s/%s/%s' % (
                        case['name'], m, label, got.get('status'), ref.get('status'),
                        ada.get('status')))
                    continue
                value = out_of(got)
                if not (isinstance(value, np.ndarray) and value.dtype == np.complex128
                        and value.shape == (nk,)):
                    problems.append('%s m=%d %s output not complex128 (nk,)' % (case['name'], m, label))
                    continue
                orc = direct_oracle(case['waves'], case['R'], case['z'], case['w'],
                                    np.asarray(rho, np.complex128), case['c'], m, CTX['jn'])
                e1 = nerr(value, orc['total'], orc['scale'])
                e2 = nerr(value, ref['deltaJ0_J'], orc['scale'])
                e3 = nerr(ref['deltaJ0_J'], orc['total'], orc['scale'])
                e4 = nerr(ada['deltaJ0_J'], ref['deltaJ0_J'], orc['scale'])
                for key, e in zip(('oracle', 'o0445', 'oracle_vs_0445', 'adapter_vs_0445'),
                                  (e1, e2, e3, e4)):
                    worst[key] = max(worst[key], e)
                if max(e1, e2, e4) > TOL:
                    problems.append('%s m=%d %s errs %.3g %.3g %.3g' % (case['name'], m, label,
                                                                        e1, e2, e4))
                if np.any(value[perp_zero] != 0.0):
                    problems.append('%s m=%d %s kperp=0 not exactly 0' % (case['name'], m, label))
                if label == 'complex' and not np.any(value.imag != 0.0):
                    problems.append('%s m=%d complex output has no imaginary part' % (case['name'], m))
    check('T05', 'module == direct oracle == pinned 0445 (irregular + random cases, m=1..6, '
          'complex/real/imag/complex64 rho, errstate raise; adapter included)', not problems,
          'runs=%d worst normalized: module-vs-oracle %.3g, module-vs-0445 %.3g, '
          '0445-vs-oracle %.3g, adapter-vs-0445 %.3g; tol %.0e; %s'
          % (runs, worst['oracle'], worst['o0445'], worst['oracle_vs_0445'],
             worst['adapter_vs_0445'], TOL, problems[:6]))


def t06_zero_rho():
    api = CTX['api']
    problems = []
    for case in (case_irregular(), case_random()):
        geometry, _ = prepared(case)
        zero = np.zeros(case['R'].shape[0], dtype=np.complex128)
        for m in range(1, 7):
            got = api.evaluate(geometry, case, zero, m)
            ref = run_0445(case, zero, m)
            if not is_complete(got):
                problems.append('%s m=%d status %s' % (case['name'], m, got.get('status')))
                continue
            if np.any(out_of(got) != 0.0) or np.any(ref['deltaJ0_J'] != 0.0):
                problems.append('%s m=%d nonzero output for zero rho' % (case['name'], m))
    check('T06', 'zero rho -> exactly zero (module and 0445), all modes', not problems,
          '; '.join(problems) or 'all exact zeros')


def t07_real_linear_not_complex_linear():
    api = CTX['api']
    case = case_irregular()
    geometry, _ = prepared(case)
    nq = case['R'].shape[0]
    problems, rows = [], []
    theta = 0.9
    rot = complex(math.cos(theta), math.sin(theta))
    for m in range(1, 7):
        r1, r2 = rho_random(nq, 7 * m), rho_random(nq, 7 * m + 1)
        a, b = 0.7, -1.3
        F = lambda rho: out_of(api.evaluate(geometry, case, rho, m))
        orc = direct_oracle(case['waves'], case['R'], case['z'], case['w'], r1, case['c'], m,
                            CTX['jn'])
        scale = orc['scale']
        lin = nerr(F(a * r1 + b * r2), a * F(r1) + b * F(r2), scale)
        rotated = F(rot * r1)
        orc_rot = direct_oracle(case['waves'], case['R'], case['z'], case['w'], rot * r1,
                                case['c'], m, CTX['jn'])
        match_rot = nerr(rotated, orc_rot['total'], scale)
        ref_rot = run_0445(case, rot * r1, m)['deltaJ0_J']
        match_rot_0445 = nerr(rotated, ref_rot, scale)
        nonlin = nerr(rotated, rot * F(r1), scale)
        times_i = nerr(F(1j * r1), 1j * F(r1), scale)
        rows.append('m=%d real-lin %.2g rot-vs-oracle %.2g rot-vs-0445 %.2g |F(e^it r)-e^it F(r)| '
                    '%.3g |F(ir)-iF(r)| %.3g' % (m, lin, match_rot, match_rot_0445, nonlin, times_i))
        if lin > TOL or match_rot > TOL or match_rot_0445 > TOL:
            problems.append('m=%d agreement' % m)
        if not (nonlin > 1e-3 and times_i > 1e-3):
            problems.append('m=%d operator looks complex-linear' % m)
    check('T07', 'full operator REAL-linear but NOT complex-linear; module matches oracle and 0445 '
          'for each rotated source', not problems, ' | '.join(rows) + ' ' + str(problems))


def t08_branches():
    api = CTX['api']
    problems, rows = [], []
    for case in (case_irregular(), case_random()):
        geometry, _ = prepared(case)
        nq = case['R'].shape[0]
        waves = case['waves']
        alpha = np.arctan2(waves[:, 1], waves[:, 0])
        for m in range(1, 7):
            rho = rho_random(nq, 31 * m)
            F = lambda r: out_of(api.evaluate(geometry, case, r, m))
            f, fi = F(rho), F(1j * rho)
            plus = (f - 1j * fi) / 2.0          # isolates the rho e^{+im alpha} branch
            minus = (f + 1j * fi) / 2.0         # isolates the conj(rho) e^{-im alpha} branch
            orc = direct_oracle(waves, case['R'], case['z'], case['w'], rho, case['c'], m, CTX['jn'])
            ep = nerr(plus, orc['plus'], orc['scale'])
            em = nerr(minus, orc['minus'], orc['scale'])
            # closed forms: real s -> 2 s cos(m alpha); imaginary i s -> -2 s sin(m alpha),
            # each times pref*(-i)^m*SUM_q w J E s (taken from the oracle's plus branch / e^{im a})
            s = rho.real.astype(np.complex128)
            fr, fs = F(s), F(1j * s)
            orc_s = direct_oracle(waves, case['R'], case['z'], case['w'], s, case['c'], m, CTX['jn'])
            base = orc_s['plus'] / np.exp(1j * m * alpha)
            e_cos = nerr(fr, 2.0 * np.cos(m * alpha) * base, orc_s['scale'])
            e_sin = nerr(fs, -2.0 * np.sin(m * alpha) * base, orc_s['scale'])
            # Hermitian pair consequence F(-k) = conj F(k) where -k is in the roster
            key = {tuple(row): i for i, row in enumerate(waves.tolist())}
            pairs = [(i, key[tuple((-waves[i]).tolist())]) for i in range(waves.shape[0])
                     if tuple((-waves[i]).tolist()) in key]
            eh = max([abs(f[j] - np.conj(f[i])) / max(orc['scale'][i], 1e-300)
                      for i, j in pairs if orc['scale'][i] > 0] or [0.0])
            ref_f = run_0445(case, rho, m)['deltaJ0_J']
            hb_mod = sum(1 for i, j in pairs if f[j] == np.conj(f[i]) and orc['scale'][i] > 0)
            hb_ref = sum(1 for i, j in pairs if ref_f[j] == np.conj(ref_f[i]) and orc['scale'][i] > 0)
            # bitwise-Hermitian pair counts are reported only (INFO): exact equality also
            # arises by chance from arithmetic order, so it is not a symmetry-use detector.
            # sensitivity: wrong laws differ from the module
            sens = {}
            laws = ['conj_vertical_minus', 'no_conj_minus', 'extra2', 'drop_minus',
                    'alpha_swapped']
            if m % 2:
                laws.append('plus_i_power')     # (+i)^m == (-i)^m for even m: not a wrong law
            for law in laws:
                wrong = direct_oracle(waves, case['R'], case['z'], case['w'], rho, case['c'], m,
                                      CTX['jn'], law=law)
                sens[law] = nerr(f, wrong['total'], orc['scale'])
            rows.append('%s m=%d plus %.2g minus %.2g cos %.2g sin %.2g herm(%d pairs) %.2g '
                        'bitwise-herm module/0445 %d/%d min-wrong-law %.2g'
                        % (case['name'], m, ep, em, e_cos, e_sin, len(pairs), eh, hb_mod, hb_ref,
                           min(sens.values())))
            if max(ep, em, e_cos, e_sin) > TOL or eh > 1e-12:
                problems.append('%s m=%d branch mismatch' % (case['name'], m))
            if min(sens.values()) < SENSITIVE:
                problems.append('%s m=%d insensitive to %s' % (
                    case['name'], m, min(sens, key=sens.get)))
    check('T08', 'negative/conjugate branch: single-branch isolation via F(rho) -/+ i F(i rho), '
          'real/imag closed forms, Hermitian pairs, wrong-law sensitivity', not problems,
          ' | '.join(rows[:12]) + ' ... ' + str(problems))


def _bad_providers():
    jn = CTX['jn']

    def j0_substitute(n, x):
        return jn(0, x)

    def tiny_at_zero(n, x):
        v = np.array(jn(n, x), dtype=np.float64)
        v[np.asarray(x) == 0.0] = 1e-300
        return v

    def float32(n, x):
        return np.asarray(jn(n, x)).astype(np.float32)

    def wrong_shape(n, x):
        return np.asarray(jn(n, x)).reshape(-1)[:-1] if np.asarray(x).size > 1 else np.zeros(2)

    def nan_value(n, x):
        v = np.array(jn(n, x), dtype=np.float64)
        v.reshape(-1)[-1] = math.nan
        return v

    def above_one(n, x):
        v = np.array(jn(n, x), dtype=np.float64)
        v.reshape(-1)[-1] = 1.5
        return v

    def complex_out(n, x):
        return np.asarray(jn(n, x)).astype(np.complex128)

    def raises(n, x):
        raise RuntimeError('fixture provider failure')

    return dict(j0_substitute=j0_substitute, tiny_at_zero=tiny_at_zero, float32=float32,
                wrong_shape=wrong_shape, nan_value=nan_value, above_one=above_one,
                complex_out=complex_out, raises=raises)


def t09_zero_kperp_guard():
    api = CTX['api']
    case = case_irregular()
    waves = case['waves']
    perp_zero = np.hypot(waves[:, 0], waves[:, 1]) == 0.0
    geometry, _ = prepared(case)
    problems, rows = [], []
    for m in range(1, 7):
        rho = rho_random(case['R'].shape[0], 900 + m)
        value = out_of(api.evaluate(geometry, case, rho, m))
        ref = run_0445(case, rho, m)['deltaJ0_J']
        if np.any(value[perp_zero] != 0.0) or np.any(ref[perp_zero] != 0.0):
            problems.append('m=%d kperp=0 output not exactly 0' % m)
    rows.append('kperp=0 waves (signed zeros incl.) = %d, exact 0 for m=1..6' % int(perp_zero.sum()))
    for name, bad in _bad_providers().items():
        rho = rho_random(case['R'].shape[0], 77)
        ref = run_0445(case, rho, 2, jn=bad)
        try:
            prep = api.prepare(case, (1, 2, 3, 4, 5, 6), jn=bad)
        except Exception as exc:  # the module must not raise
            problems.append('%s: prepare raised %s' % (name, type(exc).__name__))
            continue
        status = '%s@%s' % (prep.get('status'), prep.get('failure_stage'))
        if is_complete(prep):
            got = api.evaluate(api.geometry(prep), case, rho, 2)
            status = 'prepare COMPLETE, evaluate %s@%s' % (got.get('status'), got.get('failure_stage'))
            problems.append('%s: provider fault not caught at the provider stage (0445: %s@%s)'
                            % (name, ref.get('status'), ref.get('failure_stage')))
            if is_complete(got):
                problems.append('%s accepted' % name)
        elif (prep.get('status'), prep.get('failure_stage')) != (ref.get('status'),
                                                                 ref.get('failure_stage')):
            problems.append('%s: module %s vs 0445 %s@%s' % (name, status, ref.get('status'),
                                                             ref.get('failure_stage')))
        rows.append('%s: module %s / 0445 %s@%s' % (name, status, ref.get('status'),
                                                    ref.get('failure_stage')))
        if ref.get('status') == 'COMPLETE':
            problems.append('%s: 0445 accepted (fixture design error)' % name)
    check('T09', 'exact-zero kperp guard identical to 0445 (exact zeros; J0-substituting / '
          'nonzero-at-0 / float32 / shape / NaN / |J|>1 / complex / raising providers fail closed)',
          not problems, '; '.join(rows + problems))


def t10_duplicates_holes_permutation():
    api = CTX['api']
    problems, rows = [], []
    case = case_irregular()
    geometry, _ = prepared(case)
    waves = case['waves']
    m = 5
    rho = rho_random(case['R'].shape[0], 1234)
    base = out_of(api.evaluate(geometry, case, rho, m))
    dup_groups = {}
    for i, row in enumerate(waves.tolist()):
        dup_groups.setdefault(np.asarray(row, dtype=np.float64).tobytes(), []).append(i)
    dups = [g for g in dup_groups.values() if len(g) > 1]
    for g in dups:
        if len({base[i].tobytes() for i in g}) != 1:
            problems.append('duplicate rows %s not bitwise equal' % g)
    rows.append('duplicate wave groups %s bitwise-equal outputs' % dups)
    perm = np.random.default_rng(5).permutation(waves.shape[0])
    pcase = dict(case, waves=waves[perm].copy())
    pgeom, _ = prepared(pcase)
    pval = out_of(api.evaluate(pgeom, pcase, rho, m))
    orc = direct_oracle(waves, case['R'], case['z'], case['w'], rho, case['c'], m, CTX['jn'])
    e_wave = nerr(pval, base[perm], orc['scale'][perm])
    rows.append('wave permutation: normalized %.2g, bitwise %s'
                % (e_wave, bool(np.array_equal(pval, base[perm]))))
    qperm = np.random.default_rng(6).permutation(case['R'].shape[0])
    qcase = dict(case, R=case['R'][qperm].copy(), z=case['z'][qperm].copy(), w=case['w'][qperm].copy())
    qgeom, _ = prepared(qcase)
    qval = out_of(api.evaluate(qgeom, qcase, rho[qperm], m))
    e_pos = nerr(qval, base, orc['scale'])
    rows.append('position permutation: normalized %.2g, bitwise %s'
                % (e_pos, bool(np.array_equal(qval, base))))
    counts = group_counts(case)
    rows.append('holes: filled cells %d of n_kz*n_perp = %d' % (
        counts['filled_cells'], counts['n_kz_unique'] * counts['n_perp_unique']))
    if e_wave > TOL or e_pos > TOL:
        problems.append('permutation changed result beyond roundoff')
    check('T10', 'duplicates retained (bitwise equal), holes retained, original wave order; '
          'wave/position permutation equivariance', not problems, '; '.join(rows + problems))


def t11_each_q_once():
    api = CTX['api']
    case = case_irregular()
    geometry, _ = prepared(case)
    nq = case['R'].shape[0]
    problems = []
    worst = 0.0
    for m in (1, 3, 6):
        total = np.zeros(case['waves'].shape[0], dtype=np.complex128)
        full_rho = np.zeros(nq, dtype=np.complex128)
        for q in range(nq):
            rho = np.zeros(nq, dtype=np.complex128)
            rho[q] = complex(0.6 + 0.01 * q, -0.8 + 0.02 * q)
            full_rho[q] = rho[q]
            value = out_of(api.evaluate(geometry, case, rho, m))
            orc = direct_oracle(case['waves'], case['R'], case['z'], case['w'], rho, case['c'], m,
                                CTX['jn'])
            e = nerr(value, orc['total'], orc['scale'])
            worst = max(worst, e)
            if e > TOL:
                problems.append('m=%d q=%d (R=%r z=%r w=%r) err %.3g' % (
                    m, q, case['R'][q], case['z'][q], case['w'][q], e))
            total = total + value
        full = out_of(api.evaluate(geometry, case, full_rho, m))
        orc = direct_oracle(case['waves'], case['R'], case['z'], case['w'], full_rho, case['c'], m,
                            CTX['jn'])
        e = nerr(full, total, orc['scale'] * 4)
        worst = max(worst, e)
        if e > TOL:
            problems.append('m=%d sum of single-q sources differs %.3g' % (m, e))
    check('T11', 'every q included exactly once (single-q sources incl. exact duplicate q, 1-ulp R, '
          'z=-0.0, each vs oracle; superposition)', not problems,
          'worst normalized %.3g over %d single-q runs; %s' % (worst, 3 * nq, problems[:5]))


def t12_refresh_aba():
    api = CTX['api']
    case = case_random()
    geometry, _ = prepared(case)
    before = geometry_fingerprint(geometry)
    nq = case['R'].shape[0]
    problems, rows = [], []
    A = {m: rho_random(nq, 500 + m) for m in range(1, 7)}
    B = {m: rho_random(nq, 600 + m) for m in range(1, 7)}
    first = {m: out_of(api.evaluate(geometry, case, A[m], m)).copy() for m in range(1, 7)}
    second = {m: out_of(api.evaluate(geometry, case, B[m], m)).copy() for m in (6, 2, 4, 1, 5, 3)}
    third = {m: out_of(api.evaluate(geometry, case, A[m], m)).copy() for m in (3, 1, 6, 2, 5, 4)}
    for m in range(1, 7):
        if first[m].tobytes() != third[m].tobytes():
            problems.append('m=%d A not bitwise reproduced after B' % m)
        if np.array_equal(first[m], second[m]):
            problems.append('m=%d B equals A' % m)
    fresh, _ = prepared(case)
    for m in range(1, 7):
        fb = out_of(api.evaluate(fresh, case, B[m], m))
        if fb.tobytes() != second[m].tobytes():
            problems.append('m=%d B on reused geometry != B on fresh geometry (bitwise)' % m)
    a1 = out_of(api.adapter(geometry, case, A[2], 2)).copy()
    out_of(api.adapter(geometry, case, B[2], 2))
    a2 = out_of(api.adapter(geometry, case, A[2], 2))
    if a1.tobytes() != a2.tobytes() or a1.tobytes() != first[2].tobytes():
        rows.append('adapter A/B/A bitwise %s, adapter==evaluate bitwise %s' % (
            a1.tobytes() == a2.tobytes(), a1.tobytes() == first[2].tobytes()))
        if a1.tobytes() != a2.tobytes():
            problems.append('adapter A/B/A not bitwise')
    after = geometry_fingerprint(geometry)
    if before != after:
        problems.append('geometry arrays changed by evaluation')
    rows.append('A/B/A bitwise for m=1..6 (interleaved order), B reused == B fresh bitwise, '
                'geometry fingerprint unchanged=%s' % (before == after))
    check('T12', 'source refresh A/B/A on one bound geometry (bitwise A reproduction; no rho-'
          'dependent state)', not problems, '; '.join(rows + problems))


def _perturb(array, index, how='ulp'):
    out = np.array(array, dtype=np.float64, copy=True)
    flat = out.reshape(-1)
    if how == 'ulp':
        flat[index] = np.nextafter(flat[index], math.inf)
    elif how == 'negzero':
        flat[index] = -flat[index]
    return out


def t13_stale_geometry():
    api = CTX['api']
    case = case_irregular()
    geometry, _ = prepared(case)
    rho = rho_random(case['R'].shape[0], 4242)
    m = 2
    waves = case['waves']
    ky_zero = [i for i in range(waves.shape[0]) if waves[i, 1] == 0.0 and waves[i, 0] < 0.0][0]
    z_negzero = [i for i in range(case['z'].shape[0]) if case['z'][i] == 0.0][0]
    swap = case['waves'].copy()
    swap[[0, 1]] = swap[[1, 0]]
    rswap = np.arange(case['R'].shape[0])
    rswap[[0, 1]] = rswap[[1, 0]]
    variants = dict(
        waves_ulp=dict(waves=_perturb(waves, 3 * 5 + 2)),
        waves_kx_ulp=dict(waves=_perturb(waves, 3 * 20 + 0)),
        waves_row_swap=dict(waves=swap),
        waves_signed_zero_ky=dict(waves=_perturb(waves, 3 * ky_zero + 1, 'negzero')),
        waves_dropped_row=dict(waves=waves[:-1].copy()),
        R_ulp=dict(R=_perturb(case['R'], 4)),
        R_order=dict(R=case['R'][rswap].copy(), z=case['z'][rswap].copy(), w=case['w'][rswap].copy()),
        z_ulp=dict(z=_perturb(case['z'], 7)),
        z_signed_zero=dict(z=_perturb(case['z'], z_negzero, 'negzero')),
        w_ulp=dict(w=_perturb(case['w'], 9)),
    )
    problems, rows = [], []
    for name, change in variants.items():
        bad = dict(case, **change)
        rho_b = rho if bad['R'].shape == case['R'].shape else rho[:bad['R'].shape[0]]
        statuses = []
        if api.evaluate_takes_inputs:
            r = api.evaluate(geometry, bad, rho_b, m)
            statuses.append('evaluate=%s' % r.get('status'))
            if is_complete(r):
                problems.append('evaluate accepted stale %s' % name)
        r = api.adapter(geometry, bad, rho_b, m)
        statuses.append('adapter=%s' % r.get('status'))
        if is_complete(r):
            problems.append('adapter accepted stale %s' % name)
        rows.append('%s: %s' % (name, ','.join(statuses)))
    # mode outside the bound set
    sub, _ = prepared(case, modes=(2, 5))
    r = api.evaluate(sub, case, rho, 3)
    r2 = api.adapter(sub, case, rho, 3)
    rows.append('mode 3 on geometry(2,5): evaluate=%s adapter=%s' % (r.get('status'), r2.get('status')))
    if is_complete(r) or is_complete(r2):
        problems.append('mode outside bound set accepted')
    ok_sub = api.evaluate(sub, case, rho, 5)
    if not is_complete(ok_sub):
        problems.append('bound mode 5 rejected on geometry(2,5)')
    # provider identity: a different callable with identical values
    def same_values(n, x, _jn=CTX['jn']):
        return _jn(n, x)
    r = api.adapter(geometry, case, rho, m, jn=same_values)
    r2 = api.evaluate(geometry, case, rho, m, jn=same_values)
    rows.append('different provider callable: adapter %s evaluate %s' % (r.get('status'),
                                                                        r2.get('status')))
    if is_complete(r) or is_complete(r2):
        problems.append('a different provider callable was accepted')
    other = CTX['prov'].create_jn_provider(library_policy=CTX['prov'].LIBRARY_POLICY_FIND_LIBRARY_M,
                                           expected_library_path=None, max_cache_entries=8)
    r3 = api.evaluate(geometry, case, rho, m, jn=other['bessel_jn'])
    rows.append('second READY provider instance: evaluate %s' % r3.get('status'))
    if is_complete(r3):
        problems.append('second provider instance accepted')
    # c is a per-call scalar (not geometry); report what happens
    rc = api.adapter(geometry, case, rho, m, c=case['c'] * 2)
    rows.append('adapter with different c: %s (c is a per-call prefactor input)' % rc.get('status'))
    check('T13', 'stale geometry rejection (waves/R/z/w changed by 1 ulp, order, signed zero, '
          'dropped row; mode outside bound set; different provider identity)', not problems,
          '; '.join(rows + problems))


def _tamper_array(array):
    try:
        array.flags.writeable = True
    except ValueError:
        return False
    flat = array.reshape(-1)
    if array.size == 0:
        return False
    i = array.size // 2
    kind = array.dtype.kind
    if kind == 'b':
        flat[i] = not flat[i]
    elif kind in 'iu':
        flat[i] = flat[i] + 1 if flat[i] + 1 < np.iinfo(array.dtype).max else flat[i] - 1
    elif kind == 'f':
        flat[i] = flat[i] * 1.5 + 0.25
    elif kind == 'c':
        flat[i] = flat[i] * (1.5 + 0.5j) + 0.25
    else:
        return False
    return True


def t14_cache_tamper():
    api = CTX['api']
    case = case_irregular()
    rho = rho_random(case['R'].shape[0], 99)
    m = 4
    geometry0, _ = prepared(case)
    clean = out_of(api.evaluate(geometry0, case, rho, m)).copy()
    paths = [p for p, _ in walk_arrays(geometry0)]
    rows, problems, warns = [], [], []
    for target in paths:
        geometry, _ = prepared(case)
        pre_bound = api.bind(geometry)[1] if api.binder_fn is not None else None
        arrays = dict(walk_arrays(geometry))
        array = arrays[target]
        if not _tamper_array(array):
            rows.append('%s prevented(read-only base)' % target)
            continue
        try:
            r_eval = api.evaluate(geometry, case, rho, m)
            r_adapt = api.adapter(geometry, case, rho, m)
            r_pre = pre_bound(**api.kwargs_0445(geometry, case, rho, m)) if pre_bound else {}
        except Exception as exc:
            problems.append('%s: raised %s' % (target, type(exc).__name__))
            continue
        tag = '%s eval=%s adapter=%s bound-before-tamper=%s' % (
            target, r_eval.get('status'), r_adapt.get('status'), r_pre.get('status'))
        for r in (r_eval, r_adapt, r_pre):
            if is_complete(r):
                if out_of(r).tobytes() == clean.tobytes():
                    warns.append(tag + ' (undetected, output unchanged)')
                else:
                    problems.append(tag + ' (undetected, OUTPUT CHANGED)')
                break
        rows.append(tag)
    # scalar / string fields of a Mapping geometry, via forged copies
    forged_rows = []
    if isinstance(geometry0, Mapping):
        plain = dict(geometry0)
        r = api.evaluate(plain, case, rho, m)
        forged_rows.append('unchanged plain-dict copy: %s' % r.get('status'))
        for key, value in geometry0.items():
            if isinstance(value, np.ndarray):
                continue
            if isinstance(value, str):
                new = value + 'X'
            elif isinstance(value, bool):
                new = not value
            elif isinstance(value, int):
                new = value + 1
            elif isinstance(value, float):
                new = value * 1.5 + 1.0
            elif isinstance(value, tuple):
                new = tuple(value) + (7,)
            elif isinstance(value, Mapping):
                new = dict(value)
                new['__fixture_tamper__'] = 1
            else:
                continue
            forged = dict(geometry0)
            forged[key] = new
            if type(geometry0) is not dict:
                try:
                    forged = type(geometry0)(forged)
                except Exception:
                    pass
            r = api.evaluate(forged, case, rho, m)
            tag = 'field %r -> %s' % (key, r.get('status'))
            if is_complete(r):
                if out_of(r).tobytes() == clean.tobytes():
                    warns.append(tag + ' (undetected, output unchanged)')
                else:
                    problems.append(tag + ' (undetected, OUTPUT CHANGED)')
            forged_rows.append(tag)
    module = CTX['module']
    if hasattr(module, 'CONVENTION') and isinstance(module.CONVENTION, Mapping):
        other, _, _ = load_from_bytes(CTX['module_path'], CTX['module_sha'],
                                      'fixture0458_second_convention')
        other.CONVENTION = type(module.CONVENTION)(dict(module.CONVENTION,
                                                        fixture_variant='changed convention'))
        ev_other = getattr(other, api.evaluate_fn.__name__)
        kw = dict(api.kwargs_0445(geometry0, case, rho, m), geometry=geometry0)
        r = ev_other(**kw)
        forged_rows.append('geometry from this convention evaluated by a changed-convention '
                           'instance -> %s' % r.get('status'))
        if is_complete(r):
            problems.append('changed CONVENTION accepted a geometry prepared under the old one')
    for bogus_name, bogus in (('None', None), ('empty dict', {}), ('list', [1, 2])):
        r = api.evaluate(bogus, case, rho, m)
        forged_rows.append('%s -> %s' % (bogus_name, r.get('status')))
        if is_complete(r):
            problems.append('bogus geometry %s accepted' % bogus_name)
    level = 'FAIL' if problems else ('WARN' if warns else 'PASS')
    record('T14', 'cache tamper rejection (every reachable geometry array modified in place; '
           'scalar/convention/provider fields forged; bogus geometry)', level,
           'arrays: %s | fields: %s | warns: %s | problems: %s' % (rows, forged_rows, warns, problems))


def t15_errstate_overflow():
    api = CTX['api']
    problems, rows = [], []
    case = case_irregular()
    nq = case['R'].shape[0]
    big_rho = np.full(nq, 1e306 + 1e306j, dtype=np.complex128)
    huge_rho = np.full(nq, 1.5e308 + 0j, dtype=np.complex128)
    scenarios = [
        ('prefactor overflow (rho 1e306, c 1e3)', case, big_rho, 1e3),
        ('inner overflow (rho 1.5e308)', case, huge_rho, case['c']),
        ('c^2 2pi overflow (c 1e154)', case, rho_random(nq, 3), 1e154),
    ]
    geometry, _ = prepared(case)
    for mode_name in ('raise', 'ignore'):
        for label, cs, rho, c in scenarios:
            with np.errstate(all=mode_name):
                ref = run_0445(cs, rho, 3, c=c)
                try:
                    got = api.evaluate(geometry, cs, rho, 3, c=c)
                    ada = api.adapter(geometry, cs, rho, 3, c=c)
                except Exception as exc:
                    problems.append('%s/%s raised %s' % (mode_name, label, type(exc).__name__))
                    continue
            rows.append('%s/%s: module %s(%s) adapter %s / 0445 %s(%s)' % (
                mode_name, label, got.get('status'), got.get('exception_type'), ada.get('status'),
                ref.get('status'), ref.get('exception_type')))
            if is_complete(got) or is_complete(ada):
                problems.append('%s/%s completed' % (mode_name, label))
            if got.get('status') != ref.get('status') or ada.get('status') != ref.get('status'):
                problems.append('%s/%s status parity' % (mode_name, label))
            missing = [k for k in api.retained_keys if got.get(k) is None and
                       not isinstance(got.get('retained'), Mapping)]
            if got.get('status') == 'FAILED_CLOSED' and missing:
                problems.append('%s/%s no retention keys %s' % (mode_name, label, missing))
    # overflow inside one later R group only (w*rho finite, group sum not): documented
    # FAILED_CLOSED at the grouped-sum stage with earlier R groups retained
    R_s = np.array([0.5, 0.5, 2.0, 2.0, 2.0, 3.0])
    sc = dict(name='scatter', R=R_s, z=np.array([0.1, 0.2, 0.3, 0.3, 0.3, 0.4]),
              w=np.array([0.5, 0.5, 1.0, 1.0, 1.0, 0.5]),
              waves=np.array([[1.0, 0.5, 0.0], [0.3, -0.7, 0.2]]), c=1.0)
    rho_s = np.array([1.0, 1.0, 1.5e308, 1.5e308, 1.5e308, 1.0], dtype=np.complex128)
    gs, _ = prepared(sc)
    for mode_name in ('raise', 'ignore'):
        with np.errstate(all=mode_name):
            got = api.evaluate(gs, sc, rho_s, 2, position_chunk=1)   # one R group per batch
            ref = run_0445(sc, rho_s, 2)
        work = got.get('retained_work') or {}
        mask = work.get('r_group_mask') if isinstance(work, Mapping) else None
        rows.append('%s/grouped-sum overflow: module %s@%s r_group_mask %s / 0445 %s@%s' % (
            mode_name, got.get('status'), got.get('failure_stage'),
            None if mask is None else np.asarray(mask).tolist(), ref.get('status'),
            ref.get('failure_stage')))
        if is_complete(got) or got.get('status') != ref.get('status'):
            problems.append('%s/grouped-sum overflow status' % mode_name)
        if got.get('failure_stage') != 'scatter' or mask is None or not np.any(mask) \
                or np.all(mask):
            problems.append('%s/grouped-sum overflow not failed at its stage with partial V '
                            'retained (INTERFACE: scatter)' % mode_name)
    geo_scenarios = [
        ('kz*z overflow', dict(case, waves=np.array([[1.0, 0.0, 1e200], [0.0, 2.0, 0.5]]),
                               z=np.full(nq, 1e200))),
        ('kperp*R overflow', dict(case, waves=np.array([[1e200, 0.0, 0.5], [0.0, 2.0, 0.5]]),
                                  R=np.full(nq, 1e200))),
        ('hypot overflow', dict(case, waves=np.array([[1.5e308, 1.5e308, 0.5], [0.0, 2.0, 0.5]]))),
    ]
    for mode_name in ('raise', 'ignore'):
        for label, cs in geo_scenarios:
            with np.errstate(all=mode_name):
                ref = run_0445(cs, rho_random(nq, 5), 3)
                try:
                    prep = api.prepare(cs, (3,))
                except Exception as exc:
                    problems.append('%s/%s prepare raised %s' % (mode_name, label, type(exc).__name__))
                    continue
                status = prep.get('status')
                if is_complete(prep):
                    got = api.evaluate(api.geometry(prep), cs, rho_random(nq, 5), 3)
                    status = 'prepare COMPLETE then evaluate %s' % got.get('status')
                    if is_complete(got):
                        problems.append('%s/%s completed' % (mode_name, label))
            rows.append('%s/%s: module %s(%s) / 0445 %s(%s)' % (
                mode_name, label, status, prep.get('exception_type'), ref.get('status'),
                ref.get('exception_type')))
    with np.errstate(all='warn'):
        import warnings
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter('always')
            got = api.evaluate(geometry, case, big_rho, 3, c=1e3)
        rows.append('warn: status %s, %d RuntimeWarning(s) surfaced to caller' % (
            got.get('status'), sum(issubclass(w.category, RuntimeWarning) for w in caught)))
        if is_complete(got):
            problems.append('warn mode completed')
    check('T15', 'finite/overflow under caller errstate raise/ignore/warn -> FAILED_CLOSED with '
          'retention; status parity with 0445; geometry-stage overflow fails closed', not problems,
          '; '.join(rows + problems))


class CountingProvider:
    def __init__(self, jn):
        self.jn, self.calls, self.elements = jn, 0, 0

    def __call__(self, n, x):
        self.calls += 1
        self.elements += int(np.asarray(x).size)
        return self.jn(n, x)


def t16_memory_caps():
    api = CTX['api']
    problems, rows = [], []
    case = case_irregular()
    modes = (1, 2, 3, 4, 5, 6)
    g = dict(group_counts(case), n_modes=len(modes))
    transcribed = api.required_limits(case, modes)
    empirical = {name: api.empirical_threshold(case, modes, name) for name in api.limit_names}
    shapes = dict(nq=g['nq'], nk=g['nk'], kz_q=g['n_kz_unique'] * g['nq'],
                  kz_R=g['n_kz_unique'] * g['n_R_unique'], kz_perp=g['n_kz_unique'] * g['n_perp_unique'],
                  perp_R=g['n_perp_unique'] * g['n_R_unique'],
                  modes_perp_R=g['n_modes'] * g['n_perp_unique'] * g['n_R_unique'],
                  modes_nk=g['n_modes'] * g['nk'])
    rows.append('limits %s; INTERFACE-transcribed %s; empirical thresholds %s; group sizes %s'
                % (api.limit_names, transcribed, empirical, shapes))
    if not api.limit_names:
        problems.append('no memory-entry limit parameters on prepare')
    for name in api.limit_names:
        if empirical[name] is None:
            problems.append('%s: generous value rejected' % name)
        elif name in transcribed and transcribed[name] != empirical[name]:
            problems.append('%s: INTERFACE formula %d != empirical threshold %d'
                            % (name, transcribed[name], empirical[name]))
        elif name not in transcribed:
            rows.append('%s: no transcribed formula (empirical only)' % name)
    exact = {name: empirical[name] for name in api.limit_names if empirical[name] is not None}
    ok = api.prepare(case, modes, limits=exact)
    rows.append('at exact limits: %s' % ok.get('status'))
    if not is_complete(ok):
        problems.append('exact limits rejected: %s' % ok.get('reason'))
    for name in exact:
        lower = dict(exact)
        lower[name] = exact[name] - 1
        if lower[name] < 1:
            lower[name] = 0
        counter = CountingProvider(CTX['jn'])
        r = api.prepare(case, modes, limits=lower, jn=counter)
        rows.append('%s-1: %s stage=%s provider_calls=%d' % (name, r.get('status'),
                                                             r.get('failure_stage'), counter.calls))
        if is_complete(r) or api.geometry(r) is not None:
            problems.append('%s-1 accepted' % name)
        if counter.calls:
            problems.append('%s-1: provider evaluated before the cap check' % name)
    # evaluation wave block: min(wave_chunk, nk) <= max_block_entries (checked at evaluate)
    small_controls = dict(position_chunk=1, perp_chunk=1, cell_chunk=1)
    small = api.required_limits(case, modes, small_controls)
    if 'max_block_entries' in small and small['max_block_entries'] < case['waves'].shape[0]:
        bl = small['max_block_entries']
        prep_small = api.prepare(case, modes, limits=small, controls=small_controls)
        gs = api.geometry(prep_small)
        rho = rho_random(case['R'].shape[0], 1616)
        at = api.evaluate(gs, case, rho, 2, wave_chunk=bl) if gs is not None else {}
        over = api.evaluate(gs, case, rho, 2, wave_chunk=bl + 1) if gs is not None else {}
        rows.append('controls %s exact limits %s: prepare %s; evaluate wave_chunk=%d %s, =%d %s@%s'
                    % (small_controls, small, prep_small.get('status'), bl, at.get('status'), bl + 1,
                       over.get('status'), over.get('failure_stage')))
        if not (is_complete(prep_small) and is_complete(at)) or is_complete(over):
            problems.append('evaluation wave-block limit not enforced at the exact boundary')
    # before-allocation evidence: would-be E alone = n_kz_unique * nq * 16 B
    rng = np.random.default_rng(16)
    nq, nk = 120_000, 400
    big = dict(name='capbig', R=rng.uniform(0.5, 5.0, size=nq).round(1),
               z=rng.uniform(-3, 3, size=nq), w=rng.uniform(0.001, 0.01, size=nq),
               waves=np.stack([rng.integers(-3, 4, nk) * 0.5, rng.integers(-3, 4, nk) * 0.5,
                               rng.integers(-40, 41, nk) * 0.11], axis=1), c=1.0)
    g = group_counts(big)
    would = g['n_kz_unique'] * nq * 16
    tiny = {name: 1 for name in exact}
    counter = CountingProvider(CTX['jn'])
    tracemalloc.start()
    tracemalloc.reset_peak()
    r = api.prepare(big, modes, limits=tiny, jn=counter)
    peak = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()
    rows.append('big case %s: tiny limits -> %s, traced peak %.1f MB vs would-be E %.1f MB, '
                'provider calls %d' % (g, r.get('status'), peak / 1e6, would / 1e6, counter.calls))
    if is_complete(r) or peak > 0.25 * would or counter.calls:
        problems.append('cap rejection not before allocation')
    got = api.counts(r)
    reported = {k: got.get(k) for k in ('n_kz_unique', 'n_perp_unique', 'n_R_unique', 'n_cells')}
    expect = dict(n_kz_unique=g['n_kz_unique_bitwise'], n_perp_unique=g['n_perp_unique'],
                  n_R_unique=g['n_R_unique'], n_cells=g['n_cells_bitwise'])
    rows.append('cap-failure counts reported %s (independent %s); stage %s' % (
        reported, expect, r.get('failure_stage')))
    if reported != expect:
        problems.append('cap failure does not report the group sizes root needs')
    check('T16', 'memory-entry caps: exact limits accepted, each limit-1 rejected fail-closed with '
          'no provider call; traced peak << would-be cache', not problems, '; '.join(rows + problems))


def _scale_vectorized(case, rho, m, chunk=100):
    pref = abs(-(case['c'] ** 2) * 2 * math.pi)
    waves = case['waves']
    kperp = np.hypot(waves[:, 0], waves[:, 1])
    weight = np.abs(case['w']) * 2.0 * np.abs(rho)
    out = np.empty(waves.shape[0])
    for a in range(0, waves.shape[0], chunk):
        J = CTX['jn'](m, kperp[a:a + chunk, None] * case['R'][None, :])
        out[a:a + chunk] = pref * np.einsum('kq,q->k', np.abs(J), weight, optimize=False)
    return out


def t17_no_dense_table():
    api = CTX['api']
    case = case_wide()
    g = group_counts(case)
    dense = g['nq'] * g['nk'] * 16
    rho = rho_random(g['nq'], 17)
    tracemalloc.start()
    tracemalloc.reset_peak()
    t0 = time.perf_counter()
    prep = api.prepare(case, (4,))
    t_prep = time.perf_counter() - t0
    peak_prep = tracemalloc.get_traced_memory()[1]
    tracemalloc.reset_peak()
    geometry = api.geometry(prep)
    t0 = time.perf_counter()
    got = api.evaluate(geometry, case, rho, 4)
    t_eval = time.perf_counter() - t0
    peak_eval = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()
    t0 = time.perf_counter()
    ref = run_0445(case, rho, 4, wave_chunk=50, position_chunk=4000)
    t_ref = time.perf_counter() - t0
    scale = _scale_vectorized(case, rho, 4)
    e = nerr(out_of(got), ref['deltaJ0_J'], scale)
    ok = is_complete(got) and e <= TOL and max(peak_prep, peak_eval) < 0.25 * dense
    check('T17', 'no dense nq*nk table (traced peaks vs nq*nk*16 B) and agreement with 0445 on a '
          'wide case', ok,
          'counts %s; dense would be %.0f MB; traced peak prepare %.1f MB, evaluate %.1f MB; '
          'normalized vs 0445 %.3g; synthetic timing (no performance promise) prepare %.3fs '
          'evaluate %.3fs, 0445 %.3fs' % (g, dense / 1e6, peak_prep / 1e6, peak_eval / 1e6, e,
                                          t_prep, t_eval, t_ref))


def _interrupt_sweep(call, attr_names, protected, label, reference=None):
    """Interrupt `call` at successive line events; return rows and problems."""
    rows, problems = [], []
    n = 1
    seen_complete = False
    steps = 0
    while not seen_complete and steps < 60:
        steps += 1
        tracer = Tracer(CTX['module_path'], n)
        sys.settrace(tracer)
        try:
            result = call()
            seen_complete = True
        except KeyboardInterrupt as exc:
            sys.settrace(None)
            attached = {name: getattr(exc, name) for name in dir(exc)
                        if name.startswith('unt') and name.endswith('retained_result')}
            documented = [a for a in attr_names if a in attached]
            line = tracer.line
            inside = any(l in protected for l in tracer.stack)   # some module frame in a try
            line = '%d<%s' % (line, ','.join(str(l) for l in tracer.stack[1:]))
            record_ = attached[documented[0]] if documented else None
            status = record_.get('status') if isinstance(record_, Mapping) else None
            rows.append('n=%d L%s %s attrs=%s status=%s' % (n, line, 'protected' if inside else
                                                            'unprotected', sorted(attached), status))
            if inside:
                if not documented:
                    problems.append('%s n=%d L%s: no documented retained attribute' % (label, n, line))
                elif not isinstance(record_, Mapping) or record_.get('complete') is not False \
                        or record_.get('status') == 'COMPLETE':
                    problems.append('%s n=%d: retained record malformed' % (label, n))
                elif reference is not None:
                    problems.extend(reference(record_, n))
        finally:
            sys.settrace(None)
        n = int(n * 1.6) + 1
    if not seen_complete:
        problems.append('%s: sweep never reached completion' % label)
    return rows, problems


def t18_interruption():
    api = CTX['api']
    case = case_irregular()
    geometry, _ = prepared(case)
    rho = rho_random(case['R'].shape[0], 18)
    full = out_of(api.evaluate(geometry, case, rho, 3)).copy()
    protected = protected_lines(CTX['module_source'])

    def consistent(record_, n):
        out = []
        for key_value, key_mask in api.retained_pairs:
            value, mask = record_.get(key_value), record_.get(key_mask)
            if value is None and isinstance(record_.get('retained'), Mapping):
                value = record_['retained'].get(key_value)
                mask = record_['retained'].get(key_mask)
            if isinstance(value, np.ndarray) and isinstance(mask, np.ndarray) \
                    and value.shape == full.shape and mask.shape == full.shape:
                if np.any(mask) and not np.array_equal(value[mask], full[mask]):
                    out.append('n=%d retained masked values differ from COMPLETE values' % n)
        return out

    rows_e, prob_e = _interrupt_sweep(lambda: api.evaluate(geometry, case, rho, 3),
                                      api.interrupt_attrs['evaluate'], protected, 'evaluate',
                                      consistent)
    after = out_of(api.evaluate(geometry, case, rho, 3))
    if after.tobytes() != full.tobytes():
        prob_e.append('geometry not reusable bitwise after interrupted evaluations')
    rows_p, prob_p = _interrupt_sweep(lambda: api.prepare(case, (1, 2, 3, 4, 5, 6)),
                                      api.interrupt_attrs['prepare'], protected, 'prepare')
    if api.binder_fn is not None:   # bind untraced; the adapter contract is the bound callable
        closure = api.bind(geometry)[1]
        adapter_call = lambda: closure(**api.kwargs_0445(geometry, case, rho, 3))
    else:
        adapter_call = lambda: api.adapter(geometry, case, rho, 3)
    rows_a, prob_a = _interrupt_sweep(adapter_call, api.interrupt_attrs['adapter'], protected,
                                      'adapter', consistent)
    adapter_names = set()
    for row in rows_a:
        adapter_names.update(re.findall(r"'(unt\w+)'", row))
    same_object = []
    for n in (60, 150, 400):
        tracer = Tracer(CTX['module_path'], n)
        sys.settrace(tracer)
        try:
            adapter_call()
        except KeyboardInterrupt as exc:
            a, b = getattr(exc, 'unt0458_retained_result', None), getattr(exc, 'unt0445_retained_result', None)
            if a is not None or b is not None:
                same_object.append((n, a is b))
        finally:
            sys.settrace(None)
    if any(not ok for _, ok in same_object):
        prob_a.append('adapter unt0445/unt0458 records not the same object: %s' % same_object)
    note = ('adapter interruption attribute(s) %s (same object: %s); 0452 consumer reads '
            'unt0445_retained_result' % (sorted(adapter_names), same_object))
    problems = prob_e + prob_p + prob_a
    check('T18', 'interruption: KeyboardInterrupt re-raised with the documented retained result '
          '(status not COMPLETE, complete False, masked partial values == COMPLETE values); '
          'geometry reusable afterwards', not problems,
          'evaluate %d interrupts; prepare %d; adapter %d; %s; problems=%s; sample=%s'
          % (len(rows_e), len(rows_p), len(rows_a), note, problems[:6],
             (rows_e[:3] + rows_e[-3:] + rows_p[-2:] + rows_a[-2:])))
    bare = sorted({row.split()[1] for row in rows_e + rows_p + rows_a
                   if 'unprotected attrs=[]' in row})
    record('T18c', 'interrupt points that carry no record (outside a record-creating handler: '
           'validation before the guarded block, or result packaging after it, as in 0445)', 'INFO',
           'module lines (innermost<callers) %s' % bare)
    if 'unt0445_retained_result' not in adapter_names:
        documented = 'unt0445_retained_result' in api.interrupt_attrs['adapter']
        record('T18b', 'adapter interruption attribute vs 0452 consumer',
               'FAIL' if documented else 'WARN',
               'adapter attaches %s; 0452 retains an in-flight mode record only via '
               'unt0445_retained_result (documented in INTERFACE: %s)'
               % (sorted(adapter_names), documented))
    else:
        record('T18b', 'adapter interruption attribute vs 0452 consumer', 'PASS',
               'adapter attaches unt0445_retained_result (0452-compatible)')


def t19_inputs_unmutated():
    api = CTX['api']
    case = case_irregular()
    rho = rho_random(case['R'].shape[0], 19)
    arrays = [case['R'], case['z'], case['w'], case['waves'], rho]
    before = snapshot(*arrays)
    prep = api.prepare(case, (1, 2, 3, 4, 5, 6))
    geometry = api.geometry(prep)
    api.evaluate(geometry, case, rho, 2)
    api.adapter(geometry, case, rho, 2)
    with np.errstate(all='ignore'):
        api.evaluate(geometry, case, np.full_like(rho, 1e306 + 1e306j), 2, c=1e3)
    after = snapshot(*arrays)
    problems = [] if before == after else ['inputs mutated']
    ro = {k: (np.array(v, copy=True) if isinstance(v, np.ndarray) else v) for k, v in case.items()}
    for v in ro.values():
        if isinstance(v, np.ndarray):
            v.flags.writeable = False
    rho_ro = rho.copy()
    rho_ro.flags.writeable = False
    r1 = api.prepare(ro, (2,))
    r2 = api.evaluate(api.geometry(r1), ro, rho_ro, 2) if is_complete(r1) else {}
    r3 = api.adapter(api.geometry(r1), ro, rho_ro, 2) if is_complete(r1) else {}
    if not (is_complete(r1) and is_complete(r2) and is_complete(r3)):
        problems.append('read-only inputs rejected')
    lists = dict(case, R=case['R'].tolist(), z=case['z'].tolist(), w=case['w'].tolist(),
                 waves=case['waves'].tolist())
    r4 = api.adapter(geometry, lists, rho, 2)
    r5 = CTX['m0445'].nonzero_mode_density_fourier(
        radius_m=lists['R'], z_m=lists['z'], weights_RdRdz_m3=lists['w'], rho_mode_kg_m3=rho,
        k_physical_inverse_m=lists['waves'], c_m_s=2.0, mode=2, bessel_jn=CTX['jn'],
        wave_chunk=4, position_chunk=4)
    note = 'list inputs: adapter %s / 0445 %s' % (r4.get('status'), r5.get('status'))
    out_ro = out_of(r2) if is_complete(r2) else None
    if out_ro is not None and not out_ro.flags.writeable:
        note += '; output read-only'
    check('T19', 'inputs unmutated (prepare/evaluate/adapter/failure path); read-only inputs '
          'accepted', not problems, '; '.join(problems) + note)


def gate_0449_0452(result, nk, m):
    """Replica of the 0449/0452 consumer gate on a 0445-style result."""
    if not isinstance(result, Mapping) or result.get('status') != 'COMPLETE' \
            or result.get('complete') is not True:
        return 'not COMPLETE'
    counts = result.get('counts') or {}
    mask = np.asarray(result.get('retained_wave_mask'))
    if counts.get('waves') != nk or counts.get('mode') != m or mask.shape != (nk,) \
            or not np.all(mask):
        return 'counts/mode/mask'
    value = result.get('deltaJ0_J')
    if not isinstance(value, np.ndarray) or value.dtype != np.complex128 or value.shape != (nk,):
        return 'deltaJ0_J dtype/shape'
    if not np.all(np.isfinite(value)):
        return 'nonfinite'
    return None


def t20_adapter_contract():
    api = CTX['api']
    case = case_irregular()
    geometry, _ = prepared(case)
    nq = case['R'].shape[0]
    nk = case['waves'].shape[0]
    rho = rho_random(nq, 20)
    problems, rows = [], []
    for m in range(1, 7):
        ada = api.adapter(geometry, case, rho, m)
        gate = gate_0449_0452(ada, nk, m)
        if gate:
            problems.append('m=%d consumer gate failed: %s' % (m, gate))
    ref = run_0445(case, rho, 2)
    ada = api.adapter(geometry, case, rho, 2)
    miss = sorted(set(ref) - set(ada))
    rows.append('COMPLETE keys missing vs 0445: %s; extra: %s' % (miss, sorted(set(ada) - set(ref))))
    if miss:
        problems.append('COMPLETE result lacks 0445 keys %s' % miss)
    for sub in ('counts', 'chunking'):
        if isinstance(ref.get(sub), Mapping):
            lack = sorted(set(ref[sub]) - set(ada.get(sub) or {}))
            if lack:
                rows.append('%s subkeys missing vs 0445: %s' % (sub, lack))
    base = dict(radius_m=case['R'], z_m=case['z'], weights_RdRdz_m3=case['w'],
                rho_mode_kg_m3=rho, k_physical_inverse_m=case['waves'], c_m_s=case['c'], mode=2,
                bessel_jn=CTX['jn'], wave_chunk=5, position_chunk=7)
    float128 = getattr(np, 'float128', None)
    battery = dict(
        mode_0=dict(mode=0), mode_7=dict(mode=7), mode_true=dict(mode=True),
        mode_np_int=dict(mode=np.int64(2)), mode_float=dict(mode=2.0),
        wave_chunk_0=dict(wave_chunk=0), wave_chunk_bool=dict(wave_chunk=True),
        wave_chunk_float=dict(wave_chunk=5.0), position_chunk_0=dict(position_chunk=0),
        position_chunk_neg=dict(position_chunk=-1),
        jn_not_callable=dict(bessel_jn=None), c_bool=dict(c_m_s=True), c_zero=dict(c_m_s=0.0),
        c_negative=dict(c_m_s=-2.0), c_inf=dict(c_m_s=math.inf), c_nan=dict(c_m_s=math.nan),
        c_square_inf=dict(c_m_s=1e200), c_str=dict(c_m_s='2'),
        R_zero=dict(radius_m=np.where(np.arange(nq) == 3, 0.0, case['R'])),
        R_negative=dict(radius_m=-case['R']), R_nan=dict(radius_m=np.where(np.arange(nq) == 1,
                                                                           math.nan, case['R'])),
        R_2d=dict(radius_m=case['R'][None, :]), R_complex=dict(radius_m=case['R'] + 0j),
        z_short=dict(z_m=case['z'][:-1]), w_zero=dict(weights_RdRdz_m3=0.0 * case['w']),
        w_negative=dict(weights_RdRdz_m3=-case['w']), rho_real=dict(rho_mode_kg_m3=rho.real),
        rho_short=dict(rho_mode_kg_m3=rho[:-1]), rho_nan=dict(
            rho_mode_kg_m3=np.where(np.arange(nq) == 2, complex(math.nan, 0), rho)),
        rho_2d=dict(rho_mode_kg_m3=rho[None, :]), rho_int=dict(rho_mode_kg_m3=np.arange(nq)),
        waves_2col=dict(k_physical_inverse_m=case['waves'][:, :2]),
        waves_1d=dict(k_physical_inverse_m=case['waves'][0]),
        waves_empty=dict(k_physical_inverse_m=np.zeros((0, 3))),
        waves_nan=dict(k_physical_inverse_m=np.where(np.arange(nk)[:, None] == 4, math.nan,
                                                     case['waves'])),
        waves_complex=dict(k_physical_inverse_m=case['waves'] + 0j),
    )
    if float128 is not None:
        battery['R_float128'] = dict(radius_m=case['R'].astype(float128))
        battery['rho_clongdouble'] = dict(rho_mode_kg_m3=rho.astype(np.clongdouble))
    mismatch = []
    for name, change in battery.items():
        kwargs = dict(base, **change)
        r0 = CTX['m0445'].nonzero_mode_density_fourier(**kwargs)
        try:
            r1 = api.adapter_call(geometry, kwargs)
        except Exception as exc:
            mismatch.append('%s raised %s' % (name, type(exc).__name__))
            continue
        if r1.get('status') != r0.get('status'):
            mismatch.append('%s: adapter %s vs 0445 %s' % (name, r1.get('status'), r0.get('status')))
        if r1.get('status') == r0.get('status') == 'INVALID_INPUT':
            lack = sorted(set(r0) - set(r1))
            if lack:
                mismatch.append('%s INVALID_INPUT keys missing %s' % (name, lack))
    rows.append('INVALID_INPUT parity battery: %d cases, mismatches %s' % (len(battery), mismatch))
    if mismatch:
        problems.append('battery mismatches')
    with np.errstate(all='ignore'):
        r0 = run_0445(case, rho, 2, c=1e154)
        r1 = api.adapter(geometry, case, rho, 2, c=1e154)
    lack = sorted(set(r0) - set(r1))
    rows.append('FAILED_CLOSED: adapter %s / 0445 %s; keys missing %s; retained_wave_mask %s' % (
        r1.get('status'), r0.get('status'), lack, type(r1.get('retained_wave_mask')).__name__))
    if r1.get('status') != r0.get('status') or lack:
        problems.append('FAILED_CLOSED parity/keys')
    if api.binder_fn is not None:
        closure = api.bind(geometry)[1]
        try:
            closure(**dict(base, geometry=geometry))
            problems.append('adapter callable accepted an extra geometry keyword')
        except TypeError:
            pass
        try:
            closure(**{k: v for k, v in base.items() if k != 'position_chunk'})
            problems.append('adapter callable accepted a missing 0445 keyword')
        except TypeError:
            pass
    else:
        try:
            api.adapter_fn(**dict(base))
            problems.append('adapter without geometry did not raise TypeError')
        except TypeError:
            pass
    check('T20', 'adapter preserves 0445 keyword contract and result keys (0449/0452 consumer gate, '
          'INVALID_INPUT/FAILED_CLOSED parity battery)', not problems, '; '.join(rows + problems))


def _hex_strings(obj, path='result', depth=0, out=None):
    if out is None:
        out = {}
    if depth > 5:
        return out
    if isinstance(obj, str) and re.fullmatch(r'[0-9a-f]{64}', obj):
        out[path] = obj
    elif isinstance(obj, Mapping):
        for key, value in obj.items():
            _hex_strings(value, '%s.%s' % (path, key), depth + 1, out)
    elif isinstance(obj, (list, tuple)):
        for i, value in enumerate(obj):
            _hex_strings(value, '%s[%d]' % (path, i), depth + 1, out)
    return out


def _keys_like(obj, words, path='result', depth=0, out=None):
    if out is None:
        out = []
    if isinstance(obj, Mapping) and depth < 4:
        for key, value in obj.items():
            if any(w in str(key).lower() for w in words):
                out.append('%s.%s' % (path, key))
            _keys_like(value, words, '%s.%s' % (path, key), depth + 1, out)
    return out


def t21_provenance():
    api = CTX['api']
    case = case_irregular()
    geometry, prep = prepared(case)
    nq = case['R'].shape[0]
    a, b = rho_random(nq, 2101), rho_random(nq, 2102)
    ra1 = api.evaluate(geometry, case, a, 2)
    rb = api.evaluate(geometry, case, b, 2)
    ra2 = api.evaluate(geometry, case, a, 2)
    constants = set()
    for value in vars(CTX['module']).values():
        constants |= set(_hex_strings(value, 'const').values())
    geo_hex = (set(_hex_strings(geometry, 'geometry').values()) |
               set(_hex_strings({k: v for k, v in prep.items() if k != api.geometry_key},
                                'prep').values())) - constants
    h1, hb, h2 = _hex_strings(ra1), _hex_strings(rb), _hex_strings(ra2)
    geometry_bound = sorted(p for p, v in h1.items() if v in geo_hex)
    source_bound = sorted(p for p, v in h1.items() if p in hb and hb[p] != v and h2.get(p) == v)
    timing = _keys_like(ra1, ('time', 'timing', 'second', 'elapsed', 'duration'))
    counts = _keys_like(ra1, ('count',))
    problems = []
    if not geometry_bound:
        problems.append('no geometry digest echoed in the evaluation result')
    if not source_bound:
        problems.append('no source digest (stable for A, changed for B)')
    if not counts:
        problems.append('no counts')
    if not timing:
        problems.append('no timing')
    check('T21', 'output provenance: geometry identity echoed, source identity stable A/A and '
          'changed for B; counts/timing present', not problems,
          'geometry-bound digests %s; source-bound digests %s; timing keys %s; counts keys %s; %s'
          % (geometry_bound, source_bound, timing[:6], counts[:4], problems))


def t22_chunk_invariance_and_provider_calls():
    api = CTX['api']
    case = case_random()
    nq = case['R'].shape[0]
    rho = rho_random(nq, 2201)
    problems, rows = [], []
    counter = CountingProvider(CTX['jn'])
    prep = api.prepare(case, (1, 2, 3, 4, 5, 6), jn=counter)
    geometry = api.geometry(prep)
    calls_after_prepare = counter.calls
    base = {m: out_of(api.evaluate(geometry, case, rho, m)).copy() for m in range(1, 7)}
    if counter.calls != calls_after_prepare:
        problems.append('provider called during evaluation (%d calls)' % (counter.calls -
                                                                          calls_after_prepare))
    rows.append('provider calls: prepare %d (elements %d), evaluation +%d' % (
        calls_after_prepare, counter.elements, counter.calls - calls_after_prepare))
    orc_scale = {m: direct_oracle(case['waves'], case['R'], case['z'], case['w'], rho, case['c'], m,
                                  CTX['jn'])['scale'] for m in (1, 4)}
    bitwise_eval, bitwise_prep = [], []
    for wc, pc in ((1, 1), (3, 1000), (1000, 2), (183, 240)):
        for m in (1, 4):
            v = out_of(api.evaluate(geometry, case, rho, m, wave_chunk=wc, position_chunk=pc))
            if v is None or nerr(v, base[m], orc_scale[m]) > TOL:
                problems.append('evaluate chunks (%d,%d) m=%d changed result' % (wc, pc, m))
            else:
                bitwise_eval.append(v.tobytes() == base[m].tobytes())
    for controls in (dict(position_chunk=1, perp_chunk=1, cell_chunk=1),
                     dict(position_chunk=1000, perp_chunk=1000, cell_chunk=1000),
                     dict(position_chunk=17, perp_chunk=2, cell_chunk=3)):
        p2 = api.prepare(case, (1, 4), controls=controls)
        g2 = api.geometry(p2)
        for m in (1, 4):
            v = out_of(api.evaluate(g2, case, rho, m)) if g2 is not None else None
            if v is None or nerr(v, base[m], orc_scale[m]) > TOL:
                problems.append('prepare controls %s m=%d changed result' % (controls, m))
            else:
                bitwise_prep.append(v.tobytes() == base[m].tobytes())
    rows.append('evaluate chunk variants bitwise-equal %d/%d; prepare control variants (and mode '
                'subset (1,4)) bitwise-equal %d/%d (bitwise observed, not required)'
                % (sum(bitwise_eval), len(bitwise_eval), sum(bitwise_prep), len(bitwise_prep)))
    check('T22', 'chunk/control invariance (evaluate wave/position chunks, prepare position/perp/'
          'cell chunks, mode subset) within roundoff; provider not called during evaluation',
          not problems, '; '.join(rows + problems))


# =========================================================================== runner

TESTS = [
    ('T01', t01_inert_import), ('T02', t02_lane_ast), ('T03', t03_signatures),
    ('T04', t04_grouping_counts), ('T05', t05_equivalence), ('T06', t06_zero_rho),
    ('T07', t07_real_linear_not_complex_linear), ('T08', t08_branches),
    ('T09', t09_zero_kperp_guard), ('T10', t10_duplicates_holes_permutation),
    ('T11', t11_each_q_once), ('T12', t12_refresh_aba), ('T13', t13_stale_geometry),
    ('T14', t14_cache_tamper), ('T15', t15_errstate_overflow), ('T16', t16_memory_caps),
    ('T17', t17_no_dense_table), ('T18', t18_interruption), ('T19', t19_inputs_unmutated),
    ('T20', t20_adapter_contract), ('T21', t21_provenance),
    ('T22', t22_chunk_invariance_and_provider_calls),
]
QUICK_SKIP = {'T01', 'T17'}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    parser.add_argument('--module', required=True)
    parser.add_argument('--interface', default=DEFAULT_INTERFACE)
    parser.add_argument('--only', default='')
    parser.add_argument('--quick', action='store_true')
    parser.add_argument('--json-out', default='')
    parser.add_argument('--api-map', default='',
                        help='JSON thin-adapter overrides: prepare/evaluate/adapter names, '
                             'param_map {fn: {role: kw}}, geometry_key, counts_map, '
                             'limit_formulas, interrupt_attrs')
    args = parser.parse_args(argv)
    print('python %s numpy %s; env VECLIB=%s OPENBLAS=%s OMP=%s MKL=%s; flags isolated=%s '
          'dont_write_bytecode=%s' % (
              sys.version.split()[0], np.__version__, os.environ.get('VECLIB_MAXIMUM_THREADS'),
              os.environ.get('OPENBLAS_NUM_THREADS'), os.environ.get('OMP_NUM_THREADS'),
              os.environ.get('MKL_NUM_THREADS'), sys.flags.isolated, sys.dont_write_bytecode))
    fixture_sha = sha256_bytes(open(os.path.abspath(__file__), 'rb').read())
    print('fixture sha256 %s' % fixture_sha)
    m0445, _, _ = load_from_bytes(PIN_0445[0], PIN_0445[1], 'fixture0458_pinned_0445')
    prov, _, _ = load_from_bytes(PIN_PROVIDER[0], PIN_PROVIDER[1], 'fixture0458_pinned_provider')
    print('pinned 0445 sha256 %s OK; provider sha256 %s OK' % (PIN_0445[1], PIN_PROVIDER[1]))
    provider = prov.create_jn_provider(library_policy=prov.LIBRARY_POLICY_FIND_LIBRARY_M,
                                       expected_library_path=None, max_cache_entries=0)
    if provider.get('status') != prov.READY:
        raise SystemExit('provider not READY: %s' % provider.get('finding'))
    module_path = os.path.abspath(args.module)
    module, module_sha, module_bytes = load_from_bytes(module_path, None, 'fixture0458_under_test')
    print('module under test %s sha256 %s' % (module_path, module_sha))
    if args.api_map:
        API_MAP.update(json.load(open(args.api_map, 'r', encoding='utf-8')))
        print('api-map %s: %s' % (args.api_map, API_MAP))
    interface_text = open(args.interface, 'r', encoding='utf-8').read()
    interface_sha = sha256_bytes(interface_text.encode('utf-8'))
    print('interface %s sha256 %s' % (args.interface, interface_sha))
    CTX.update(m0445=m0445, prov=prov, provider=provider, jn=provider['bessel_jn'],
               module=module, module_path=module_path, module_source=module_bytes.decode('utf-8'),
               module_sha=module_sha)
    CTX['api'] = build_api(module, interface_text, provider, prov)
    print('API layer: %s' % CTX['api'].describe())
    only = {s.strip() for s in args.only.split(',') if s.strip()}
    t_start = time.perf_counter()
    for tid, fn in TESTS:
        if only and tid not in only:
            continue
        if args.quick and tid in QUICK_SKIP:
            continue
        t0 = time.perf_counter()
        try:
            fn()
        except Exception as exc:
            record(tid, fn.__name__, 'ERROR', '%s: %s | %s' % (
                type(exc).__name__, exc, traceback.format_exc().strip().splitlines()[-3:]))
        finally:
            sys.settrace(None)
        print('      (%s %.2fs)' % (tid, time.perf_counter() - t0), flush=True)
    tally = {}
    for r in RESULTS:
        tally[r['result']] = tally.get(r['result'], 0) + 1
    print('SUMMARY %s total %.1fs module_sha256 %s' % (tally, time.perf_counter() - t_start,
                                                         module_sha))
    if args.json_out:
        with open(args.json_out, 'x', encoding='utf-8') as handle:
            json.dump(dict(module=module_path, module_sha256=module_sha, fixture_sha256=fixture_sha,
                           interface_sha256=interface_sha, results=RESULTS, tally=tally), handle,
                      indent=1, default=str)
    bad = tally.get('FAIL', 0) + tally.get('ERROR', 0)
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
