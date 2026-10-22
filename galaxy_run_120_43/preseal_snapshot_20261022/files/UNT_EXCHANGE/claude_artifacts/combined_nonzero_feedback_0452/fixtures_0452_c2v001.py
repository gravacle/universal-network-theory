"""UNT 0452 independent analytic fixtures (fixture helper, c2v001).

Tests a supplied 0452 callable ("combine retained density harmonics m in 1..6 before ONE
cached full-ten field evaluation") on SMALL SYNTHETIC ANALYTIC inputs only. No project
packet, no .npz, no root worker, no galaxy run, no target data.

Usage (root interpreter, isolated, single-thread BLAS):
  VECLIB_MAXIMUM_THREADS=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
  python3 -I -B fixtures_0452_c2v001.py --module PATH --function NAME --outdir DIR \
      [--adapter ADAPTER.py] [--only 1,2,...]

The target module's sha256 is computed from bytes and printed BEFORE it is loaded by
importlib from PATH (and recomputed after the run). The pinned 0445 contraction, J_n
provider, v002 line module and the frozen 0449 module are loaded only after their
sha256 matches the 0452 pins; no 0449 file is written (python -B: no bytecode).

Expectations are INDEPENDENT of the module, of 0445 and of the line module:
  deltaJ0(k)   DIRECT azimuthal Fourier summation, NO Bessel function:
               rho_q(phi) = sum_m [rho_m(q) e^{im phi} + conj(rho_m(q)) e^{-im phi}] (real),
               deltaJ0(k) = -c^2 sum_q w_q e^{-i k_z z_q} (2pi/N) sum_n rho_q(phi_n)
                            e^{-i k_perp R_q cos(phi_n - alpha_k)}, N = 2048 nodes;
               the combined total is summed from the COMBINED real perturbation, per-mode
               values from each harmonic alone (fixture self-check: total = sum of modes,
               and per-mode = 0445 equation with a decimal-series J_m).
  delta_prep   U[k,a,0] * deltaJ0_total(k) (U synthetic, non-separable in (k, a)).
  field/jets   direct numpy elementwise sums  sum_k A_k e^{i k.x}, i k_j (..), -k_i k_j (..).
  lapse        Nb = 1 + Re n_base, LINEAR dPhi = c^2 dn/Nb,
               grad = c^2 (grad dn/Nb - dn grad nb/Nb^2); LOG variant separately.
  call counts  injected recorder wrappers around the 0445 callable, prepare_line and
               evaluate_line; every prepare_line packet column is classified as base /
               total increment / single-mode increment / other.

Adapter: parameters are mapped by name (ALIASES; an unmatched parameter whose name holds
'rho'/'mode'/'harmonic'/'coeff' is taken as the {m: rho_m} mapping) and outputs are
located by key search (normalize). A different interface can be bound with --adapter FILE
defining make_kwargs(params, case, values) -> dict and/or normalize(result, case) -> dict.
An unresolved parameter or output is reported, never PASS.

Tests (BINDING unless a check is marked advisory):
  1  two distinct harmonics (m=1, m=3) vs the direct azimuthal summation of the combined
     real perturbation: per-mode and total deltaJ0, delta_prepared, complex full-ten
     fields/jets (base and increment, all 16 angles), linear and separate log lapse;
     0445 called once per mode with the identical signed waves and roster
  2  cancellation: (a) m=1 + m=3 analytically cancelling through the real 0445 -> zero
     increment to roundoff; (b) exact: per-mode results that are exact negatives ->
     total, increment fields/jets, dn and dPhi exactly zero
  3  base and line geometry evaluated once: prepare_line/evaluate_line call counts and
     per-(R, phi) roles for 1, 2 and 6 modes; no per-mode line evaluation
  4  a partial / failed / forged / invalid / interrupted / overflowing mode rejects the
     total evaluation (no line call, no payload) and the per-mode results are retained
  5  anisotropic response mixing m=1,3 into |m|=5 slots retained across the 16 angles
  6  one-mode input reproduces the pinned 0449 module within roundoff (m = 1, 3, 6)
  7  metadata lists included and omitted modes; no nominal single-mode tag; empty,
     non-mapping, out-of-range, bool, float, str, duplicate keys and mismatched/real
     coefficient arrays rejected
  8  keyword-only signature with no defaults, every 0449 caller control present
  9  advisory: lane AST scan, import inertness, chunk invariance, provenance echo, input
     immutability
"""
import argparse
import ast
import cmath
import collections
import contextlib
import copy
import decimal
import hashlib
import importlib.util
import inspect
import io
import json
import math
import os
import re
import sys
import time
import traceback
from collections.abc import Mapping

import numpy as np

# ---------------------------------------------------------------------------
# Pins (task 0452, sha256 2cb7cc47429d14803a71cf0acb0ec57407c4aed414998e08ee71fac967efe3e3)
# ---------------------------------------------------------------------------
_EX = '/Users/bgm/Research/UNT_EXCHANGE'
_D49 = _EX + '/claude_artifacts/nonzero_cached_feedback_0449/'
_D45 = _EX + '/claude_artifacts/nonzero_density_fourier_0445/'
_FC = ('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/'
       'FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers')
PINS = {
    'task_0452': (_EX + '/FROM_CODEX/0452_2026-10-16_claude2_combined_nonzero_feedback.md',
                  '2cb7cc47429d14803a71cf0acb0ec57407c4aed414998e08ee71fac967efe3e3'),
    'module_0449': (_D49 + 'nonzero_cached_feedback_c2v001.py',
                    '1b4f129ff93698f951a537c1c59011fba93b75d70c6aa7c704a9992aa3f6bf95'),
    'interface_0449': (_D49 + 'INTERFACE_0449_V001.md',
                       '0c72f717640aefe6838938adaf67b8010a123bab0f29063a2de232cb3945ac77'),
    'review_0449': (_D49 + 'REVIEW_0449_V001.md',
                    '68327d2bc23cb2e7e76d861b4d5533f1f3a75fb0346f491bf23efb8238b9a274'),
    'fixtures_0449': (_D49 + 'fixtures_0449_c2v001.py',
                      'dff1ab5c39cc25cf052258dee2babde713acd0f682cb398c7316286099a78c25'),
    'contraction_0445': (_D45 + 'nonzero_density_fourier_c2v001.py',
                         '255e09f4889b6ed470e3424d3a3c41f3a21c433f3095e04ea12af7a96bc5aaf4'),
    'provider_0445': (_D45 + 'posix_libm_bessel_jn_provider_c2v001.py',
                      '9ec3f1c9fb8afe1ffa4a2bb24df5daf4d2695aa51574984658cb753cfc304f67'),
    'line': (_FC + '/recovered_packet_audit/owned_fixed_xy_fourier_line_v002.py',
             '3a47419d88f24e5f6f0f1c2db1ea85cf4108057a3ddb94db608cd05e94822d18'),
}
LOADABLE = ('module_0449', 'contraction_0445', 'provider_0445', 'line')

RTOL_VALUE = 1e-11       # direct-summation comparisons, relative to max |expected| of the array
RTOL_0449 = 1e-14        # one-mode reproduction of the pinned 0449 output
RTOL_SUM = 1.2e-16       # x M^2: total vs the module's own per-mode sum, any summation order
RTOL_CHUNK = 1e-13       # chunk invariance
CANCEL_REL = 1e-13       # analytic cancellation through 0445: residual / single-mode scale
TIGHT = 1e-11            # reality tolerance (atol and rtol) for real fields
C_TEST = 3.7             # c distinct from 1, 2pi and dk-like factors
NPHI = 16
N_AZ = 2048              # direct azimuthal summation nodes
ERRSTATE_DEFAULT = dict(all='raise')


def sha256_file(path):
    with open(path, 'rb') as handle:
        return hashlib.sha256(handle.read()).hexdigest()


def load_path(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_pinned():
    seen = {}
    for key, (path, pin) in PINS.items():
        got = sha256_file(path)
        seen[key] = dict(path=path, sha256=got, pin=pin, match=(got == pin))
        if got != pin:
            raise SystemExit('PIN MISMATCH %s: %s != %s (stop)' % (key, got, pin))
    mods = {key: load_path(PINS[key][0], 'unt0452fx_' + key) for key in LOADABLE}
    return mods, seen


# ---------------------------------------------------------------------------
# Independent references
# ---------------------------------------------------------------------------
_MINUS_I = (1 + 0j, -1j, -1 + 0j, 1j)


def bessel_ref(m, x):
    """J_m(x), ascending series in decimal from the exact binary x (0 <= x <= 40); used only
    for fixture self-checks and for choosing cancelling/overflowing coefficients."""
    if not (0.0 <= x <= 40.0):
        raise ValueError('reference Bessel range')
    if x == 0.0:
        return 1.0 if m == 0 else 0.0
    with decimal.localcontext() as ctx:
        ctx.prec = 80
        half = decimal.Decimal(x) / 2
        sq = half * half
        term = half ** m / math.factorial(m)
        total = term
        k = 0
        while True:
            k += 1
            term = -term * sq / (k * (k + m))
            total += term
            if k > x and abs(term) < decimal.Decimal(10) ** -70:
                break
        return float(total)


def bessel_formula_deltaJ0(waves, R, z, w, rho, m, c):
    """0445 equation transcribed term by term with cmath and the decimal J_m (self-check)."""
    out = []
    for kx, ky, kz in waves:
        kp = math.hypot(kx, ky)
        al = math.atan2(ky, kx)
        s = 0j
        for Rq, zq, wq, rq in zip(R, z, w, rho):
            bracket = rq * cmath.exp(1j * m * al) + rq.conjugate() * cmath.exp(-1j * m * al)
            s += wq * bessel_ref(m, kp * Rq) * cmath.exp(-1j * kz * zq) * bracket
        out.append(-(c * c) * (2 * math.pi) * _MINUS_I[m % 4] * s)
    return np.array(out, dtype=complex)


def direct_deltaJ0(waves, R, z, w, modes, c, nodes=N_AZ):
    """DIRECT azimuthal Fourier summation of the real perturbation built from ALL supplied
    harmonics together (no Bessel function, no (-i)^m):
      rho_q(phi) = sum_m 2 Re(rho_m(q) e^{i m phi});
      deltaJ0(k) = -c^2 sum_q w_q e^{-i kz z_q} (2pi/N) sum_n rho_q(phi_n) e^{-i(kx x_qn + ky y_qn)}."""
    R = np.asarray(R, float)
    z = np.asarray(z, float)
    w = np.asarray(w, float)
    phi = 2.0 * math.pi * np.arange(nodes) / nodes
    rho_phi = np.zeros((len(R), nodes))
    for m, coeff in modes.items():
        coeff = np.asarray(coeff, complex)
        rho_phi = rho_phi + 2.0 * np.real(coeff[:, None] * np.exp(1j * m * phi)[None, :])
    xq = R[:, None] * np.cos(phi)[None, :]
    yq = R[:, None] * np.sin(phi)[None, :]
    out = np.empty(len(waves), complex)
    for i, (kx, ky, kz) in enumerate(np.asarray(waves, float)):
        ring = np.sum(rho_phi * np.exp(-1j * (kx * xq + ky * yq)), axis=1) * (2.0 * math.pi / nodes)
        out[i] = -(c * c) * np.sum(w * np.exp(-1j * kz * z) * ring)
    return out


def field_grid(waves, amps, P):
    """sum_k A_k e^{ik.x}, Cartesian gradient and Hessian per component; elementwise numpy."""
    waves = np.asarray(waves, float)
    kx, ky, kz = waves[:, 0], waves[:, 1], waves[:, 2]
    ph = P[..., 0, None] * kx + P[..., 1, None] * ky + P[..., 2, None] * kz      # (...,nk)
    term = np.exp(1j * ph)[..., :, None] * amps                                    # (...,nk,10)
    F = np.sum(term, axis=-2)
    G = np.empty(F.shape + (3,), complex)
    H = np.empty(F.shape + (3, 3), complex)
    for i in range(3):
        G[..., i] = np.sum(term * (1j * waves[:, i])[:, None], axis=-2)
        for j in range(3):
            H[..., i, j] = np.sum(term * (-waves[:, i] * waves[:, j])[:, None], axis=-2)
    return F, G, H


def points_of(R, phi, Z):
    nR, nP, nZ = Z.shape
    P = np.empty((nR, nP, nZ, 3))
    for i in range(nR):
        for j in range(nP):
            for l in range(nZ):
                P[i, j, l] = (R[i] * math.cos(phi[j]), R[i] * math.sin(phi[j]), Z[i, j, l])
    return P


def lapse_expect(c, baseF, baseG, incF, incG, phi):
    nb = baseF[..., 0].real
    dn = incF[..., 0].real
    gnb = baseG[..., 0, :].real
    gdn = incG[..., 0, :].real
    Nb = 1.0 + nb
    with np.errstate(all='ignore'):
        dphi = c * c * dn / Nb
        grad = c * c * (gdn / Nb[..., None] - dn[..., None] * gnb / (Nb[..., None] ** 2))
        logphi = c * c * np.log1p(dn / Nb)
        loggrad = c * c * (Nb[..., None] * gdn - dn[..., None] * gnb) / (Nb * (Nb + dn))[..., None]
    cp = np.cos(phi)[None, :, None]
    sp = np.sin(phi)[None, :, None]
    cyl = np.stack((grad[..., 0] * cp + grad[..., 1] * sp, -grad[..., 0] * sp + grad[..., 1] * cp,
                    grad[..., 2]), -1)
    return dict(nb=nb, dn=dn, Nb=Nb, grad_nb=gnb, grad_dn=gdn, dphi=dphi, grad=grad, grad_cyl=cyl,
                logphi=logphi, loggrad=loggrad)


def peak_abs(waves, row, P):
    return float(np.max(np.abs(field_grid(waves, np.asarray(row, complex)[:, None], P)[0])))


# ---------------------------------------------------------------------------
# Synthetic cases
# ---------------------------------------------------------------------------
S_UNIT = np.array([1.0, -0.6, 0.45, 0.3, -0.25, 0.2, 0.15, -0.12, 0.1, 0.08])
T_BASE = np.array([1.0, 0.5, -0.4, 0.3, 0.2, -0.2, 0.1, 0.1, -0.05, 0.05])
SRC = dict(R=[0.8, 1.5, 2.2, 1.1], z=[-0.1, 0.2, 0.05, -0.3], w=[0.3, 0.5, 0.4, 0.35])
RHO = {
    1: [0.7 + 0.2j, -0.3 + 0.5j, 0.1 - 0.4j, 0.25 + 0.1j],
    2: [-0.2 + 0.35j, 0.4 - 0.1j, 0.15 + 0.25j, -0.3 - 0.2j],
    3: [0.2 - 0.6j, 0.45 + 0.15j, -0.35 - 0.2j, 0.1 + 0.3j],
    4: [0.3 + 0.1j, -0.15 - 0.45j, 0.2 + 0.05j, 0.4 - 0.25j],
    5: [-0.5 + 0.2j, 0.1 + 0.3j, 0.35 - 0.15j, -0.05 + 0.4j],
    6: [0.15 + 0.5j, -0.4 + 0.2j, -0.1 - 0.3j, 0.3 + 0.05j],
}
BASE_K = [[0.9, 0.4, 0.7], [-0.3, 1.1, -0.5], [0.0, 0.0, 0.8], [0.6, -0.7, 0.0], [1.2, 0.2, -0.3]]
EVAL_R = [1.7, 2.9]
EVAL_Z = [[-0.4, 0.05, 0.6], [-0.25, 0.3, 0.9]]


def roster(z_per_angle=0.007):
    R = np.array(EVAL_R, float)
    Zr = np.array(EVAL_Z, float)
    phi = np.array([2 * math.pi * j / NPHI for j in range(NPHI)])
    Z3 = np.empty((len(R), NPHI, Zr.shape[1]))
    for j in range(NPHI):
        Z3[:, j, :] = Zr + z_per_angle * j
    return R, phi, Z3


def signed_waves(base_k):
    """Each k and its exact negation, sign mixed and in scrambled order."""
    ks = [np.array(k, float) for k in base_k]
    order = []
    for i, k in enumerate(ks):
        order.append((i, 1) if i % 2 == 0 else (i, -1))
    for i, k in enumerate(ks):
        order.append((i, -1) if i % 2 == 0 else (i, 1))
    order = order[1::2] + order[0::2]
    waves = np.array([s * ks[i] for i, s in order])
    return waves, order


def hermitian_rows(order, table, comp, phase_step):
    """(nk, 10) rows: +k_i -> scale[a] table[i] e^{i phase_step a (i+1)}, -k_i -> conjugate."""
    rows = np.empty((len(order), 10), complex)
    for r, (i, s) in enumerate(order):
        v = comp * table[i] * np.exp(1j * phase_step * np.arange(10) * (i + 1))
        rows[r] = v if s > 0 else np.conj(v)
    return rows


G_TAB = [1.0 * cmath.exp(0.4j), 0.7 * cmath.exp(-1.1j), 1.3 * cmath.exp(2.0j),
         0.9 * cmath.exp(0.6j), 0.5 * cmath.exp(-2.4j)]
H_TAB = [1.0 * cmath.exp(-0.3j), 0.6 * cmath.exp(0.9j), 0.8 * cmath.exp(1.7j),
         0.7 * cmath.exp(-0.8j), 0.4 * cmath.exp(2.2j)]


def finish_case(case, per_mode, total, inc_target, base_target, sigma_ref=None):
    """Scale unit/base, then compute every independent expectation."""
    waves, P = case['waves'], case['points']
    U0, B0 = case['unit_rows'], case['base_rows']
    ref = total if sigma_ref is None else sigma_ref
    pk = peak_abs(waves, U0[:, 0] * ref, P)
    sigma = inc_target / pk if (inc_target and pk > 0) else 1.0
    tau = base_target / peak_abs(waves, B0[:, 0], P) if base_target else 0.0
    U = (sigma * U0)[:, :, None]
    B = (tau * B0)[:, :, None]
    case.update(unit=U, base=B, sigma=sigma, tau=tau)
    dprep = U * total[:, None, None]
    incF, incG, incH = field_grid(waves, dprep[:, :, 0], P)
    baseF, baseG, baseH = field_grid(waves, B[:, :, 0], P)
    ex = dict(per_mode=per_mode, total=total, delta_prepared=dprep, inc_fields=incF,
              inc_gradient=incG, inc_hessian=incH, base_fields=baseF, base_gradient=baseG,
              base_hessian=baseH)
    ex.update(lapse_expect(case['c'], baseF, baseG, incF, incG, case['eval_phi']))
    case['expected'] = ex
    return case


def build_case(name, *, modes, base_k=BASE_K, src=SRC, c=C_TEST, inc_target=0.25, base_target=0.3,
               include_log=False, wave_chunk=2, position_chunk=3, z_per_angle=0.007,
               unit_rows=None, base_rows=None, expect=True, sigma_mode=None, atol=TIGHT,
               rtol=TIGHT):
    waves, order = signed_waves(base_k) if unit_rows is None else (np.asarray(base_k, float), None)
    R, phi, Z = roster(z_per_angle)
    P = points_of(R, phi, Z)
    modes = {m: np.asarray(v, complex) for m, v in modes.items()}
    case = dict(
        name=name, modes=modes, c=c, waves=waves, order=order,
        src_R=np.array(src['R'], float), src_z=np.array(src['z'], float),
        src_w=np.array(src['w'], float),
        unit_rows=(hermitian_rows(order, G_TAB, S_UNIT, 0.17) if unit_rows is None else unit_rows),
        base_rows=(hermitian_rows(order, H_TAB, T_BASE, -0.11) if base_rows is None else base_rows),
        eval_R=R, eval_phi=phi, eval_Z=Z, points=P, atol_inc=atol, rtol_inc=rtol,
        atol_base=atol, rtol_base=rtol, include_log=include_log, wave_chunk=wave_chunk,
        position_chunk=position_chunk,
        provenance=dict(fixture='UNT0452 fixtures c2v001', case=name, synthetic=True,
                        nested=dict(tag='provenance-echo-' + name, n=7)))
    if not expect:
        case.update(unit=(case['unit_rows'])[:, :, None], base=(0.3 * case['base_rows'])[:, :, None])
        return case
    per_mode = {m: direct_deltaJ0(waves, src['R'], src['z'], src['w'], {m: v}, c)
                for m, v in modes.items()}
    total = direct_deltaJ0(waves, src['R'], src['z'], src['w'], modes, c)
    sref = None if sigma_mode is None else per_mode[sigma_mode]
    return finish_case(case, per_mode, total, inc_target, base_target, sref)


# ---------------------------------------------------------------------------
# Recorder wrappers (call counting / role classification / fault injection)
# ---------------------------------------------------------------------------
class InjectedInterrupt(KeyboardInterrupt):
    """Fixture-injected interruption (distinguishable from a real Ctrl-C)."""


class Trace:
    def __init__(self, case, inject=None):
        self.case = case
        self.inject = inject or {}
        self.contraction_calls = []
        self.prepare = []
        self.evaluate = []
        self._lines = {}
        self._keep = []
        self.provider_callable = None
        ex = case.get('expected')
        self.ref = None
        if ex is not None:
            U = case['unit'][:, :, 0]
            per = {m: U * d[:, None] for m, d in ex['per_mode'].items()}
            tot = U * ex['total'][:, None]
            scale = max([float(np.max(np.abs(v))) for v in per.values()] + [float(np.max(np.abs(tot)))])
            self.ref = dict(base=case['base'][:, :, 0], total=tot, per=per, scale=scale)

    def classify(self, W):
        try:
            W = np.asarray(W)
        except Exception:
            return ['unreadable']
        if W.ndim != 3 or W.shape[:2] != (len(self.case['waves']), 10):
            return ['shape%s' % (W.shape,)]
        roles = []
        for s in range(W.shape[2]):
            col = W[:, :, s]
            if self.ref is None:
                roles.append('unclassified')
                continue
            if np.array_equal(col, self.ref['base']):
                roles.append('base')
                continue
            tol = 1e-11 * self.ref['scale']
            with np.errstate(all='ignore'):
                if float(np.max(np.abs(col - self.ref['total']))) <= tol:
                    roles.append('total')
                    continue
                hit = [m for m, v in self.ref['per'].items() if float(np.max(np.abs(col - v))) <= tol]
            roles.append('mode%d' % hit[0] if hit else 'other')
        return roles

    def wrap_contraction(self, inner):
        def contraction(**kw):
            rec = dict(keys=sorted(kw), bessel_jn=kw.get('bessel_jn'))
            for k in ('mode', 'wave_chunk', 'position_chunk', 'c_m_s'):
                rec[k] = kw.get(k)
            for k in ('radius_m', 'z_m', 'weights_RdRdz_m3', 'rho_mode_kg_m3', 'k_physical_inverse_m'):
                try:
                    rec[k] = np.array(kw.get(k), copy=True)
                except Exception:
                    rec[k] = None
            self.contraction_calls.append(rec)
            hook = self.inject.get('contraction')
            if hook is not None:
                return hook(inner, kw, len(self.contraction_calls))
            return inner(**kw)
        return contraction

    def wrap_prepare(self, inner):
        def prepare_line(**kw):
            prepared = kw.get('prepared')
            W = prepared.get('weighted_responses') if isinstance(prepared, Mapping) else None
            roles = self.classify(W)
            line = inner(**kw)
            self._lines[id(line)] = roles
            self._keep.append(line)
            self.prepare.append(dict(x=kw.get('x_m'), y=kw.get('y_m'), roles=roles))
            return line
        return prepare_line

    def wrap_evaluate(self, inner):
        def evaluate_line(**kw):
            roles = self._lines.get(id(kw.get('line')), ['unknown-line'])
            self.evaluate.append(dict(z=kw.get('z_m'), roles=roles))
            if self.inject.get('interrupt_evaluate') == len(self.evaluate):
                raise InjectedInterrupt('fixture interrupt at evaluate_line call %d' % len(self.evaluate))
            return inner(**kw)
        return evaluate_line

    def role_counts(self):
        prep = collections.Counter()
        ev = collections.Counter()
        for p in self.prepare:
            for r in p['roles']:
                prep[r] += 1
        for e in self.evaluate:
            for r in e['roles']:
                ev[r] += 1
        return dict(prepare_calls=len(self.prepare), evaluate_calls=len(self.evaluate),
                    prepare_columns=dict(prep), evaluate_columns=dict(ev))

    def per_point(self, role):
        R, phi = self.case['eval_R'], self.case['eval_phi']
        counts = np.zeros((len(R), len(phi)), int)
        stray = 0
        for p in self.prepare:
            if role not in p['roles']:
                continue
            hit = False
            for i in range(len(R)):
                for j in range(len(phi)):
                    if abs(p['x'] - R[i] * math.cos(phi[j])) <= 1e-12 * R[i] and \
                            abs(p['y'] - R[i] * math.sin(phi[j])) <= 1e-12 * R[i]:
                        counts[i, j] += 1
                        hit = True
            stray += 0 if hit else 1
        return counts, stray


# ---------------------------------------------------------------------------
# Adapter
# ---------------------------------------------------------------------------
class AdapterUnresolved(Exception):
    pass


def provider_dict(mods, bessel=None, status='READY'):
    if bessel is None:
        made = mods['provider_0445'].create_jn_provider(
            library_policy='posix_find_library_m', expected_library_path=None, max_cache_entries=0)
        if made['status'] != 'READY':
            raise SystemExit('pinned J_n provider not READY: ' + str(made['finding']))
        return made
    return dict(status=status, bessel_jn=bessel, metadata=dict(provider='fixture double'), finding=None)


ALIASES = {
    'contraction': ('density_fourier', 'contraction', 'contraction_0445', 'density_contraction',
                    'nonzero_mode_density_fourier', 'source_contraction', 'fourier_contraction'),
    'provider_dict': ('jn_provider', 'provider', 'bessel_provider', 'jn_provider_result'),
    'src_R': ('radius_m', 'source_radius_m', 'rho_radius_m'),
    'src_z': ('z_m', 'source_z_m', 'rho_z_m'),
    'src_w': ('weights_RdRdz_m3', 'source_weights_RdRdz_m3', 'RdRdz_m3', 'weights_m3'),
    'modes': ('rho_modes_kg_m3', 'rho_by_mode_kg_m3', 'rho_mode_map_kg_m3', 'mode_rho_kg_m3',
              'density_modes_kg_m3', 'rho_m_by_mode_kg_m3', 'rho_harmonics_kg_m3', 'modes',
              'rho_modes', 'density_modes', 'mode_coefficients', 'harmonics'),
    'waves': ('k_physical_inverse_m', 'wavevectors', 'waves', 'k_physical'),
    'unit_packet': ('unit_response', 'unit_prepared', 'unit_packet'),
    'base_packet': ('base_prepared', 'base_response', 'base_packet', 'f2_prepared'),
    'prepare_line': ('prepare_line',),
    'evaluate_line': ('evaluate_line',),
    'eval_R': ('eval_radius_m', 'evaluation_radius_m', 'eval_R_m', 'R_eval_m'),
    'eval_phi': ('eval_phi_rad', 'evaluation_phi_rad', 'eval_angles_rad', 'phi_rad', 'angles_rad'),
    'eval_Z': ('eval_z_m', 'evaluation_z_m', 'eval_heights_m', 'z_eval_m'),
    'c': ('c_m_s', 'c'),
    'atol_base': ('base_reality_atol',),
    'rtol_base': ('base_reality_rtol',),
    'atol_inc': ('increment_reality_atol',),
    'rtol_inc': ('increment_reality_rtol',),
    'wave_chunk': ('wave_chunk',),
    'position_chunk': ('position_chunk',),
    'include_log': ('include_log_difference', 'log_difference', 'finite_log_difference'),
    'provenance': ('provenance', 'supplied_provenance'),
}
CONTROLS_0449 = tuple(ALIASES)        # every canonical input must be an explicit parameter
_MODES_HINTS = ('rho', 'mode', 'harmonic', 'coeff')


def resolve_params(params):
    """-> {param_name: canonical} (raises AdapterUnresolved)."""
    out = {}
    for name, p in params.items():
        if p.kind not in (p.KEYWORD_ONLY, p.POSITIONAL_OR_KEYWORD):
            continue
        key = next((k for k, names in ALIASES.items() if name in names), None)
        if key is None and any(h in name.lower() for h in _MODES_HINTS) and 'modes' not in out.values():
            key = 'modes'
        if key is None:
            if p.default is not p.empty:
                continue
            raise AdapterUnresolved('parameter %r has no canonical mapping' % name)
        out[name] = key
    return out


def canonical_values(case, mods, trace):
    pd = case.get('provider_override') or provider_dict(mods)
    trace.provider_callable = pd.get('bessel_jn')
    contraction = case.get('contraction_override') or mods['contraction_0445'].nonzero_mode_density_fourier
    return dict(
        contraction=trace.wrap_contraction(contraction), provider_dict=pd,
        src_R=case['src_R'], src_z=case['src_z'], src_w=case['src_w'], modes=case['modes'],
        waves=case['waves'],
        unit_packet=dict(wavevectors=case['waves'], weighted_responses=case['unit']),
        base_packet=dict(wavevectors=case['waves'], weighted_responses=case['base']),
        prepare_line=trace.wrap_prepare(mods['line'].prepare_line),
        evaluate_line=trace.wrap_evaluate(mods['line'].evaluate_line),
        eval_R=case['eval_R'], eval_phi=case['eval_phi'], eval_Z=case['eval_Z'], c=case['c'],
        atol_base=case['atol_base'], rtol_base=case['rtol_base'], atol_inc=case['atol_inc'],
        rtol_inc=case['rtol_inc'], wave_chunk=case['wave_chunk'],
        position_chunk=case['position_chunk'], include_log=case['include_log'],
        provenance=case['provenance'])


def default_make_kwargs(params, case, values):
    return {name: values[key] for name, key in resolve_params(params).items()}


# ----- output location (key search; every resolved path is reported) -----
def _is_0445_result(d):
    return isinstance(d, Mapping) and 'counts' in d and isinstance(d.get('convention'), Mapping) \
        and 'equation' in d['convention']


def _mode_key(k):
    if isinstance(k, (bool, np.bool_)):
        return None
    if isinstance(k, (int, np.integer)) and 1 <= int(k) <= 6:
        return int(k)
    if isinstance(k, str):
        mm = re.fullmatch(r'(?:m|mode_?)?([1-6])', k)
        if mm:
            return int(mm.group(1))
    return None


def find_per_mode(obj, path=(), depth=0):
    """Every mapping {m: per-mode dict} (or list of per-mode dicts) inside the result."""
    found = []
    if depth > 5:
        return found
    if isinstance(obj, Mapping):
        keys = list(obj.keys())
        if keys and all(_mode_key(k) is not None for k in keys) and \
                all(isinstance(v, Mapping) or v is None for v in obj.values()) and \
                any(isinstance(v, Mapping) for v in obj.values()):
            found.append((path, {_mode_key(k): v for k, v in obj.items()}))
            return found
        if _is_0445_result(obj):
            return found
        for k, v in obj.items():
            found += find_per_mode(v, path + (k,), depth + 1)
    elif isinstance(obj, (list, tuple)) and obj and all(isinstance(v, Mapping) for v in obj):
        keyed = {}
        for v in obj:
            mk = _mode_key(v.get('mode', v.get('m')))
            if mk is None and _is_0445_result(v):
                mk = _mode_key((v.get('counts') or {}).get('mode'))
            if mk is None:
                return found
            keyed[mk] = v
        found.append((path, keyed))
    return found


def mode_info(entry):
    if not isinstance(entry, Mapping):
        return dict(status=None, status_0445=None, deltaJ0=None, retained=None, mask=None)
    r45 = entry if _is_0445_result(entry) else next(
        (v for v in entry.values() if _is_0445_result(v)), None)
    r45 = r45 or {}
    dj = entry.get('deltaJ0_J') if isinstance(entry.get('deltaJ0_J'), np.ndarray) else r45.get('deltaJ0_J')
    return dict(status=entry.get('status', r45.get('status')), status_0445=r45.get('status'),
                deltaJ0=dj, retained=r45.get('retained_deltaJ0_J'), mask=r45.get('retained_wave_mask'),
                failure_stage_0445=r45.get('failure_stage'))


def _walk(obj, path=(), depth=0, skip=()):
    yield path, obj
    if depth >= 6 or not isinstance(obj, Mapping) or _is_0445_result(obj):
        return
    for k, v in obj.items():
        p = path + (k,)
        if p in skip:
            continue
        yield from _walk(v, p, depth + 1, skip)


def _last(path):
    return str(path[-1]).lower() if path else ''


def _pick(cands, prefer):
    if not cands:
        return None, None
    cands.sort(key=lambda pv: (0 if any(t in '.'.join(map(str, pv[0])).lower() for t in prefer) else 1,
                               len(pv[0])))
    return cands[0]


def locate(region, nk, skip):
    """Payload items inside one region (top level without 'retained', or 'retained')."""
    out = {}
    tot, prep, base, inc, lapse, lin, log, mask = [], [], [], [], [], [], [], []
    for path, v in _walk(region, skip=skip):
        name = _last(path)
        if not path:
            continue
        if 'deltaj0' in name and isinstance(v, np.ndarray) and v.shape == (nk,):
            tot.append((path, v))
        elif 'deltaj0' in name and v is None:
            tot.append((path, None))
        if 'prepared' in name and 'base' not in name and 'unit' not in name:
            if isinstance(v, Mapping) and 'weighted_responses' in v:
                prep.append((path, v.get('weighted_responses')))
                out['delta_prepared_waves'] = v.get('wavevectors')
            elif isinstance(v, np.ndarray) or v is None:
                prep.append((path, v))
        if isinstance(v, Mapping) and {'fields', 'gradient', 'hessian'} <= set(v):
            (base if 'base' in name else inc).append((path, v))
        elif v is None and name.endswith('_line'):
            (base if 'base' in name else inc).append((path, None))
        if isinstance(v, Mapping) and 'dn' in v and ('Nb' in v or 'nb' in v):
            lapse.append((path, v))
        if isinstance(v, Mapping) and any('deltaphi' in str(k).lower() for k in v):
            (log if 'log' in name else lin).append((path, v))
        elif v is None and name in ('linear', 'log_difference', 'lapse'):
            {'linear': lin, 'log_difference': log, 'lapse': lapse}[name].append((path, None))
        if name == 'point_mask':
            mask.append((path, v))
    p, out['total'] = _pick(tot, ('total', 'sum', 'combined'))
    out['total__path'] = p
    out['total_candidates'] = ['.'.join(map(str, q)) for q, _ in tot]
    p, out['delta_prepared'] = _pick(prep, ('delta', 'total', 'increment'))
    out['delta_prepared__path'] = p
    for key, cands in (('base', base), ('inc', inc)):
        p, v = _pick(cands, ('base',) if key == 'base' else ('increment', 'total'))
        out[key + '__path'] = p
        for kind in ('fields', 'gradient', 'hessian'):
            out[key + '_' + kind] = v.get(kind) if isinstance(v, Mapping) else None
    p, v = _pick(lapse, ('lapse',))
    out['lapse__path'] = p
    for k in ('nb', 'dn', 'Nb'):
        out[k] = v.get(k) if isinstance(v, Mapping) else None
    for key, cands in (('lin', lin), ('log', log)):
        p, v = _pick(cands, ('linear',) if key == 'lin' else ('log',))
        out[key + '__path'] = p
        d = v if isinstance(v, Mapping) else {}
        out[key + '_label'] = d.get('label')
        out[key + '_dphi'] = next((d[k] for k in d if 'deltaphi' in str(k).lower() and 'grad' not in str(k).lower()), None)
        out[key + '_grad'] = next((d[k] for k in d if 'grad' in str(k).lower() and 'cart' in str(k).lower()),
                                  next((d[k] for k in d if 'grad' in str(k).lower() and 'cyl' not in str(k).lower()), None))
        out[key + '_grad_cyl'] = next((d[k] for k in d if 'cyl' in str(k).lower()), None)
    p, out['point_mask'] = _pick(mask, ('point_mask',))
    return out


def _int_list(v):
    if isinstance(v, np.ndarray):
        v = v.tolist()
    if isinstance(v, (list, tuple, set, frozenset)) and all(
            isinstance(x, (int, np.integer)) and not isinstance(x, (bool, np.bool_)) for x in v):
        return [int(x) for x in v]
    return None


def default_normalize(result, case):
    if not isinstance(result, Mapping):
        raise AdapterUnresolved('result is not a mapping: ' + type(result).__name__)
    nk = len(case['waves'])
    pm = find_per_mode(result)
    chosen = None
    for path, d in sorted(pm, key=lambda pd_: ('retained' in map(str, pd_[0]), len(pd_[0]))):
        chosen = (path, d)
        break
    skip = tuple(p for p, _ in pm)
    top_region = {k: v for k, v in result.items() if k != 'retained'}
    out = dict(status=result.get('status'), complete=result.get('complete'),
               per_mode=({m: mode_info(e) for m, e in chosen[1].items()} if chosen else None),
               per_mode__path=(chosen[0] if chosen else None),
               per_mode_paths_all=[p for p, _ in pm], provenance=result.get('provenance'),
               retained_raw=result.get('retained'))
    out.update(locate(top_region, nk, skip))
    ret = result.get('retained')
    if isinstance(ret, Mapping):
        rpm = find_per_mode(ret)
        out['retained_per_mode'] = ({m: mode_info(e) for m, e in rpm[0][1].items()} if rpm else None)
        rloc = locate(ret, nk, tuple(('retained',) + p for p, _ in rpm) + tuple(p for p, _ in rpm))
        out['retained_total'] = rloc['total']
        out['retained_point_mask'] = rloc['point_mask']
    else:
        out['retained_per_mode'] = None
        out['retained_total'] = None
        out['retained_point_mask'] = None
    inc_l, om_l = [], []
    for path, v in _walk(result):
        name = _last(path)
        lst = _int_list(v)
        if lst is None:
            continue
        if 'includ' in name:
            inc_l.append((path, lst))
        elif any(t in name for t in ('omit', 'omission', 'exclud', 'absent', 'missing')):
            om_l.append((path, lst))
    p, out['included'] = _pick(inc_l, ('mode',))
    out['included__path'] = p
    p, out['omitted'] = _pick(om_l, ('mode',))
    out['omitted__path'] = p
    # nominal single-mode tags: an int-valued 'mode'/'m' key outside per-mode results
    tags = []
    for path, v in _walk(result, skip=skip):
        if path and _last(path) in ('mode', 'm') and isinstance(v, (int, np.integer)) \
                and not isinstance(v, (bool, np.bool_)):
            tags.append('.'.join(map(str, path)))
    out['single_mode_tags'] = tags
    if out['status'] is None:
        raise AdapterUnresolved('no status key in result')
    return out


# ---------------------------------------------------------------------------
# Harness
# ---------------------------------------------------------------------------
class Harness:
    def __init__(self, fn, mods, adapter):
        self.fn = fn
        self.mods = mods
        self.params = dict(inspect.signature(fn).parameters)
        self.make_kwargs = getattr(adapter, 'make_kwargs', None) if adapter else None
        self.normalize = getattr(adapter, 'normalize', None) if adapter else None
        self.calls = 0

    def run(self, case, errstate=None, inject=None):
        """-> Run(raw, norm, exc, seconds, mutated, trace)."""
        trace = Trace(case, inject)
        values = canonical_values(case, self.mods, trace)
        kwargs = (self.make_kwargs(self.params, case, values) if self.make_kwargs
                  else default_make_kwargs(self.params, case, values))
        snapshot = {k: copy.deepcopy(v) for k, v in kwargs.items()
                    if isinstance(v, np.ndarray) or (isinstance(v, dict) and 'bessel_jn' not in v)}
        t0 = time.monotonic()
        raw = exc = None
        self.calls += 1
        try:
            with np.errstate(**(errstate or ERRSTATE_DEFAULT)):
                raw = self.fn(**kwargs)
        except InjectedInterrupt as e:
            exc = e
        except Exception as e:  # recorded; a raise is not a fail-closed dict
            exc = e
        dt = time.monotonic() - t0
        mutated = [k for k, v in snapshot.items() if not _deep_equal(v, kwargs[k])]
        norm = None
        if isinstance(raw, Mapping):
            norm = self.normalize(raw, case) if self.normalize else default_normalize(raw, case)
        return dict(raw=raw, norm=norm, exc=exc, seconds=dt, mutated=mutated, trace=trace)


def _deep_equal(a, b):
    if isinstance(a, np.ndarray):
        return isinstance(b, np.ndarray) and a.shape == b.shape and a.dtype == b.dtype and \
            bool(np.all((a == b) | (np.isnan(a) & np.isnan(b)) if a.dtype.kind in 'fc' else a == b))
    if isinstance(a, dict):
        return isinstance(b, Mapping) and set(a.keys()) == set(b.keys()) and \
            all(_deep_equal(a[k], b[k]) for k in a)
    try:
        return bool(a == b)
    except Exception:
        return a is b


def is_complete(norm):
    return norm is not None and norm.get('status') == 'COMPLETE' and norm.get('complete') is True


def payload_absent(norm):
    """On rejection: no total source, prepared increment, field increment or lapse exposed."""
    if norm is None:
        return True
    return all(norm.get(k) is None for k in ('total', 'delta_prepared', 'inc_fields', 'base_fields',
                                             'dn', 'lin_dphi', 'lin_grad', 'log_dphi', 'log_grad'))


def rel_err(got, exp):
    try:
        got = np.asarray(got)
        exp = np.asarray(exp)
    except Exception as e:
        return None, 'unreadable %r' % e
    if got.shape != exp.shape:
        return None, 'shape %s != expected %s' % (got.shape, exp.shape)
    if got.dtype == bool or exp.dtype == bool:
        return (0.0 if np.array_equal(got, exp) else math.inf), None
    scale = float(np.max(np.abs(exp))) if exp.size else 0.0
    with np.errstate(all='ignore'):
        diff = np.abs(got - exp)
    if not np.all(np.isfinite(diff)):
        return math.inf, 'nonfinite difference'
    err = float(np.max(diff)) if diff.size else 0.0
    return (err / scale if scale > 0 else err), None


def chk(checks, label, ok, **info):
    checks.append(dict(check=label, ok=bool(ok), **info))
    return bool(ok)


def check_value(checks, label, got, exp, rtol, advisory=False):
    if got is None:
        return chk(checks, label, False, detail='MISSING in result', advisory=advisory)
    err, why = rel_err(got, exp)
    return chk(checks, label, err is not None and err <= rtol, max_rel_err=err, rtol=rtol, detail=why,
               advisory=advisory)


def _suspects(ratio, c):
    med = complex(np.median(ratio.real) + 1j * np.median(ratio.imag))
    cands = {'1 (correct)': 1, '-1 (extra minus)': -1, 'c^2': c * c, '1/c^2': 1 / (c * c), '2pi': 2 * math.pi,
             '1/(2pi)': 1 / (2 * math.pi), '2': 2, '1/2': 0.5, 'i': 1j, '-i': -1j}
    out = [n for n, v in cands.items() if abs(med - v) <= 1e-6 * max(1, abs(v))]
    return out or ['median ratio %r matches no simple factor' % (med,)]


def status_line(run):
    raw = run['raw'] if isinstance(run['raw'], Mapping) else {}
    return dict(status=raw.get('status'), stage=raw.get('failure_stage'), reason=str(raw.get('reason'))[:300],
                exc=(None if run['exc'] is None else '%s: %s' % (type(run['exc']).__name__, run['exc'])))


def expect_complete(h, case, checks, prefix, *, log=None, contraction_check=True, line_check=True,
                    values=True, errstate=None):
    run = h.run(case, errstate=errstate)
    norm = run['norm']
    tag = lambda s: prefix + ': ' + s
    if run['exc'] is not None or not is_complete(norm):
        chk(checks, tag('status COMPLETE'), False, **status_line(run))
        return run
    chk(checks, tag('status COMPLETE'), True)
    ex = case['expected']
    modes = sorted(case['modes'])
    pm = norm.get('per_mode') or {}
    chk(checks, tag('per-mode results retained for exactly the included modes'),
        sorted(pm) == modes, got=sorted(pm), path=norm.get('per_mode__path'))
    if values:
        for m in modes:
            info = pm.get(m) or {}
            chk(checks, tag('per-mode m=%d 0445 status COMPLETE' % m), _st(info) == 'COMPLETE', got=_st(info))
            check_value(checks, tag('per-mode m=%d deltaJ0 vs direct azimuthal sum of that harmonic' % m),
                        info.get('deltaJ0'), ex['per_mode'][m], RTOL_VALUE)
        ok = check_value(checks, tag('TOTAL deltaJ0 vs direct azimuthal sum of the COMBINED real perturbation'),
                         norm.get('total'), ex['total'], RTOL_VALUE)
        if not ok and norm.get('total') is not None and np.asarray(norm['total']).shape == ex['total'].shape:
            nz = np.abs(ex['total']) > 1e-9 * np.max(np.abs(ex['total']))
            chk(checks, tag('factor diagnosis total/expected'), False,
                suspects=_suspects(np.asarray(norm['total'])[nz] / ex['total'][nz], case['c']))
        got_modes = [pm.get(m, {}).get('deltaJ0') for m in modes]
        if norm.get('total') is not None and all(isinstance(g, np.ndarray) for g in got_modes):
            tot = np.asarray(norm['total'])
            scale = max(float(np.max(np.abs(g))) for g in got_modes)
            with np.errstate(all='ignore'):
                folds = {}
                for name, seq in (('ascending', modes), ('descending', modes[::-1]),
                                  ('mapping order', list(case['modes']))):
                    acc = got_modes[modes.index(seq[0])].copy()
                    for m in seq[1:]:
                        acc = acc + got_modes[modes.index(m)]
                    folds[name] = acc
                err = float(np.max(np.abs(tot - folds['ascending']))) / scale if scale > 0 else \
                    float(np.max(np.abs(tot - folds['ascending'])))
            chk(checks, tag('TOTAL == sum of the module\'s own retained per-mode deltaJ0 (each once)'),
                err <= RTOL_SUM * len(modes) * len(modes), max_rel_err=err)
            chk(checks, tag('TOTAL bitwise equal to a left fold (order identified; advisory)'),
                any(np.array_equal(tot, f) for f in folds.values()), advisory=True,
                bitwise_orders=[n for n, f in folds.items() if np.array_equal(tot, f)])
        dp = norm.get('delta_prepared')
        check_value(checks, tag('delta_prepared = U * deltaJ0_total (nk,10,1), signed order'), dp,
                    ex['delta_prepared'], RTOL_VALUE)
        if dp is not None and norm.get('total') is not None:
            chk(checks, tag('delta_prepared bitwise == unit * module total[:,None,None] (single multiplication)'),
                np.array_equal(np.asarray(dp), case['unit'] * np.asarray(norm['total'])[:, None, None]))
        if norm.get('delta_prepared_waves') is not None:
            chk(checks, tag('delta_prepared wavevectors identical to the supplied signed order'),
                np.array_equal(np.asarray(norm['delta_prepared_waves']), case['waves']))
        for key in ('base_fields', 'base_gradient', 'base_hessian', 'inc_fields', 'inc_gradient', 'inc_hessian'):
            check_value(checks, tag(key + ' complex full-ten, all %d angles, vs direct sum' % NPHI),
                        norm.get(key), ex[key], RTOL_VALUE)
        for key in ('nb', 'dn', 'Nb'):
            if norm.get(key) is not None:
                check_value(checks, tag('lapse ' + key), norm[key], ex[key], RTOL_VALUE)
        check_value(checks, tag('LINEAR dPhi = c^2 dn/Nb'), norm.get('lin_dphi'), ex['dphi'], RTOL_VALUE)
        check_value(checks, tag('LINEAR grad dPhi (Cartesian)'), norm.get('lin_grad'), ex['grad'], RTOL_VALUE)
        if norm.get('lin_grad_cyl') is not None:
            check_value(checks, tag('LINEAR grad dPhi cylindrical (R,phi,z)'), norm['lin_grad_cyl'],
                        ex['grad_cyl'], RTOL_VALUE)
        if norm.get('lin_dphi') is not None:
            d = rel_err(norm['lin_dphi'], ex['logphi'])[0]
            chk(checks, tag('linear dPhi is NOT the log variant'), d is not None and d > 1e-6, rel_diff_to_log=d)
        if log is True:
            check_value(checks, tag('LOG dPhi = c^2 log1p(dn/Nb), separate dict'), norm.get('log_dphi'),
                        ex['logphi'], RTOL_VALUE)
            check_value(checks, tag('LOG grad'), norm.get('log_grad'), ex['loggrad'], RTOL_VALUE)
            chk(checks, tag('labels: linear and log dicts separately labelled (advisory)'),
                'LINEAR' in str(norm.get('lin_label')).upper() and 'LOG' in str(norm.get('log_label')).upper()
                and norm.get('lin__path') != norm.get('log__path'), advisory=True,
                lin_label=norm.get('lin_label'), log_label=norm.get('log_label'))
        if log is False:
            chk(checks, tag('no log difference when not requested'),
                norm.get('log_dphi') is None and norm.get('log_grad') is None)
        mask = norm.get('point_mask')
        if mask is not None:
            chk(checks, tag('point_mask all True over (nR, %d, nz)' % NPHI),
                np.asarray(mask).shape == case['eval_Z'].shape and bool(np.all(mask)))
    tr = run['trace']
    if contraction_check:
        calls = tr.contraction_calls
        chk(checks, tag('0445 called exactly once per included mode'),
            sorted(c['mode'] for c in calls if type(c['mode']) is int) == modes and len(calls) == len(modes),
            modes_called=[c['mode'] for c in calls])
        same = all(c['k_physical_inverse_m'] is not None and np.array_equal(c['k_physical_inverse_m'], case['waves'])
                   and np.array_equal(c['radius_m'], case['src_R']) and np.array_equal(c['z_m'], case['src_z'])
                   and np.array_equal(c['weights_RdRdz_m3'], case['src_w']) for c in calls)
        chk(checks, tag('every 0445 call: identical signed waves and common R, z, RdRdz roster'), same)
        rho_ok = all(type(c['mode']) is int and c['mode'] in case['modes'] and c['rho_mode_kg_m3'] is not None and
                     np.array_equal(c['rho_mode_kg_m3'], case['modes'][c['mode']]) for c in calls)
        chk(checks, tag('every 0445 call: rho_m of THAT mode, unscaled'), rho_ok)
        chk(checks, tag('every 0445 call: READY provider callable, caller chunks and c passed through'),
            all(c['bessel_jn'] is tr.provider_callable and c['wave_chunk'] == case['wave_chunk'] and
                c['position_chunk'] == case['position_chunk'] and c['c_m_s'] == case['c'] for c in calls))
    if line_check:
        line_once_checks(checks, tag, case, tr)
    if run['mutated']:
        chk(checks, tag('inputs not mutated'), False, mutated=run['mutated'], advisory=True)
    return run


def line_once_checks(checks, tag, case, tr):
    nR, nP, nZ = case['eval_Z'].shape
    rc = tr.role_counts()
    bcount, bstray = tr.per_point('base')
    tcount, tstray = tr.per_point('total')
    per_mode_cols = {k: v for k, v in rc['prepare_columns'].items() if k.startswith('mode')}
    chk(checks, tag('base prepared ONCE per (R_i, phi_j) at x=R cos phi, y=R sin phi'),
        bool(np.all(bcount == 1)) and bstray == 0, min=int(bcount.min()), max=int(bcount.max()), stray=bstray)
    chk(checks, tag('total increment prepared ONCE per (R_i, phi_j)'),
        bool(np.all(tcount == 1)) and tstray == 0, min=int(tcount.min()), max=int(tcount.max()), stray=tstray)
    chk(checks, tag('no single-mode or other increment packet prepared'),
        not per_mode_cols and rc['prepare_columns'].get('other', 0) == 0 and
        all(k in ('base', 'total') for k in rc['prepare_columns']), columns=rc['prepare_columns'])
    chk(checks, tag('evaluate_line: base and total each once per point (%d), nothing else' % (nR * nP * nZ)),
        rc['evaluate_columns'].get('base', 0) == nR * nP * nZ and
        rc['evaluate_columns'].get('total', 0) == nR * nP * nZ and
        all(k in ('base', 'total') for k in rc['evaluate_columns']), columns=rc['evaluate_columns'])
    return rc


def expect_reject(h, case, checks, label, *, errstate=None, inject=None, lines_zero=True):
    run = h.run(case, errstate=errstate, inject=inject)
    norm = run['norm']
    if run['exc'] is not None:
        chk(checks, label + ': fail-closed dict (not raised)', False,
            detail='%s: %s' % (type(run['exc']).__name__, run['exc']))
        return run
    chk(checks, label + ': rejected (status not COMPLETE)', not is_complete(norm), **status_line(run))
    chk(checks, label + ': no total/prepared/field/lapse payload exposed', payload_absent(norm))
    if lines_zero:
        rc = run['trace'].role_counts()
        chk(checks, label + ': total evaluation not started (0 line calls)',
            rc['prepare_calls'] == 0 and rc['evaluate_calls'] == 0,
            prepare=rc['prepare_calls'], evaluate=rc['evaluate_calls'])
    return run


def _st(info):
    info = info or {}
    return info.get('status_0445') or info.get('status')


def all_per_mode(norm):
    """Union of per-mode info found at top level and in 'retained' (retained wins if both)."""
    out = {}
    for src in ((norm or {}).get('per_mode'), (norm or {}).get('retained_per_mode')):
        if src:
            for m, v in src.items():
                if v and (v.get('status_0445') is not None or v.get('deltaJ0') is not None or m not in out):
                    out[m] = v
    return out


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
def test_1(h):
    checks = []
    # rho_3 = 8 RHO[3] so that both harmonics carry comparable deltaJ0 (J_3 << J_1 here)
    case = build_case('two_harmonics_m1_m3', modes={3: 8.0 * np.array(RHO[3]), 1: RHO[1]}, include_log=True)
    ex = case['expected']
    s = sum(ex['per_mode'].values())
    chk(checks, 'fixture self-check: direct combined total == sum of direct per-mode',
        rel_err(ex['total'], s)[0] <= 1e-13, max_rel_err=rel_err(ex['total'], s)[0])
    for m in (1, 3):
        bf = bessel_formula_deltaJ0(case['waves'], SRC['R'], SRC['z'], SRC['w'], case['modes'][m], m, case['c'])
        e = rel_err(ex['per_mode'][m], bf)[0]
        chk(checks, 'fixture self-check: m=%d direct azimuthal sum == 0445 equation (decimal J_m)' % m,
            e <= 1e-12, max_rel_err=e)
    chk(checks, 'fixture self-check: both harmonics contribute (each >= 20%% of total peak)',
        all(float(np.max(np.abs(ex['per_mode'][m]))) >= 0.2 * float(np.max(np.abs(ex['total']))) for m in (1, 3)))
    chk(checks, 'fixture self-check: fields real, Nb > 0, Nb + dn > 0',
        float(np.max(np.abs(ex['inc_fields'].imag))) <= 1e-14 and float(np.max(np.abs(ex['base_fields'].imag))) <= 1e-14
        and bool(np.all(ex['Nb'] > 0)) and bool(np.all(ex['Nb'] + ex['dn'] > 0)))
    kp0 = np.hypot(case['waves'][:, 0], case['waves'][:, 1]) == 0
    chk(checks, 'fixture self-check: k_perp = 0 pair present (exact zero rows)', bool(np.any(kp0)) and
        bool(np.all(np.abs(ex['total'][kp0]) <= 1e-15 * np.max(np.abs(ex['total'])))))
    r1 = expect_complete(h, case, checks, 'm{1,3} log requested', log=True)
    c2 = dict(case, include_log=False, name='two_harmonics_nolog')
    r2 = expect_complete(h, c2, checks, 'm{1,3} log NOT requested', log=False, values=True)
    if is_complete(r1['norm']) and is_complete(r2['norm']):
        chk(checks, 'linear result identical with and without the log request (advisory)',
            np.array_equal(np.asarray(r1['norm']['lin_dphi']), np.asarray(r2['norm']['lin_dphi'])), advisory=True)
    return checks


def test_2(h, mods):
    checks = []
    # (a) analytic cancellation through the real 0445: one transverse direction (kx, ky) =
    # (0.9, 0.4) with several k_z plus a k_perp = 0 pair; rho_3(q) real chosen so that
    # J_3(k_perp R_q) Re(rho_3 e^{3i alpha}) = J_1(k_perp R_q) Re(rho_1 e^{i alpha}) for every q.
    base_k = [[0.9, 0.4, 0.7], [0.9, 0.4, -0.5], [0.0, 0.0, 0.8], [0.9, 0.4, 0.3], [0.9, 0.4, 0.0]]
    kp = math.hypot(0.9, 0.4)
    al = math.atan2(0.4, 0.9)
    rho1 = np.array(RHO[1], complex)
    rho3 = np.array([bessel_ref(1, kp * Rq) * (r * cmath.exp(1j * al)).real /
                     (bessel_ref(3, kp * Rq) * math.cos(3 * al)) for Rq, r in zip(SRC['R'], rho1)], complex)
    case = build_case('cancel_m1_m3_real0445', modes={1: rho1, 3: rho3}, base_k=base_k, sigma_mode=1,
                      include_log=True)
    ex = case['expected']
    s1 = float(np.max(np.abs(ex['per_mode'][1])))
    resid = float(np.max(np.abs(ex['per_mode'][1] + ex['per_mode'][3]))) / s1
    chk(checks, '2a fixture self-check: direct per-mode contributions cancel (|d1+d3|/|d1|)',
        resid <= 1e-12 and float(np.max(np.abs(ex['total']))) / s1 <= 1e-12, residual=resid,
        combined_direct_rel=float(np.max(np.abs(ex['total']))) / s1)
    chk(checks, '2a fixture self-check: each mode alone gives a 0.25-peak increment', abs(
        peak_abs(case['waves'], case['unit'][:, 0, 0] * ex['per_mode'][1], case['points']) - 0.25) < 1e-12)
    run = h.run(case)
    norm = run['norm']
    if run['exc'] is not None or not is_complete(norm):
        chk(checks, '2a status COMPLETE', False, **status_line(run))
    else:
        chk(checks, '2a status COMPLETE', True)
        pm = norm.get('per_mode') or {}
        for m in (1, 3):
            check_value(checks, '2a per-mode m=%d deltaJ0 nonzero and retained (vs direct)' % m,
                        (pm.get(m) or {}).get('deltaJ0'), ex['per_mode'][m], RTOL_VALUE)
        tot = norm.get('total')
        rel = None if tot is None else float(np.max(np.abs(tot))) / s1
        chk(checks, '2a TOTAL deltaJ0 cancels to roundoff (|total| / |d1| <= %g)' % CANCEL_REL,
            rel is not None and rel <= CANCEL_REL, rel=rel)
        for key, lim in (('inc_fields', 0.25), ('inc_gradient', 0.25 * 1.5), ('inc_hessian', 0.25 * 2.5)):
            v = norm.get(key)
            r = None if v is None else float(np.max(np.abs(v))) / lim
            chk(checks, '2a %s zero to roundoff (rel. to the single-mode 0.25 scale)' % key,
                r is not None and r <= CANCEL_REL, rel=r)
        dp = norm.get('lin_dphi')
        r = None if dp is None else float(np.max(np.abs(dp))) / (case['c'] ** 2 * 0.25)
        chk(checks, '2a LINEAR dPhi zero to roundoff', r is not None and r <= CANCEL_REL, rel=r)
        check_value(checks, '2a base still evaluated once and exact (fields)', norm.get('base_fields'),
                    ex['base_fields'], RTOL_VALUE)
        line_once_checks(checks, lambda s: '2a ' + s, case, run['trace'])
    # (b) exact zero: a contraction double returns the real 0445 result of mode a for mode a and
    # its exact negation (labelled with mode b, every other field from the same COMPLETE dict) for b.
    a, b = 2, 5
    real = mods['contraction_0445'].nonzero_mode_density_fourier

    def double(**kw):
        if kw.get('mode') == b:
            r = real(**dict(kw, mode=a))
            r = dict(r, counts=dict(r['counts'], mode=b), deltaJ0_J=-r['deltaJ0_J'])
            return r
        return real(**kw)
    rho_a = np.array(RHO[a], complex)
    case_b = build_case('exact_cancel_double', modes={a: rho_a, b: rho_a.copy()}, include_log=True,
                        sigma_mode=a)
    dA = case_b['expected']['per_mode'][a]
    case_b = finish_case(case_b, {a: dA, b: -dA}, np.zeros_like(dA), 0.25, 0.3, sigma_ref=dA)
    case_b['contraction_override'] = double
    run = h.run(case_b)
    norm = run['norm']
    if run['exc'] is not None or not is_complete(norm):
        chk(checks, '2b exact-negative per-mode results: module rejected the double (advisory)', False,
            advisory=True, **status_line(run))
    else:
        zero_ok = {}
        for key in ('total', 'delta_prepared', 'inc_fields', 'inc_gradient', 'inc_hessian', 'dn',
                    'lin_dphi', 'lin_grad', 'log_dphi', 'log_grad'):
            v = norm.get(key)
            zero_ok[key] = (v is not None and bool(np.all(np.asarray(v) == 0)))
        chk(checks, '2b exact cancellation: total, delta_prepared, increment fields/jets, dn, linear and '
                    'log dPhi all EXACTLY zero', all(zero_ok.values()), detail=zero_ok)
        check_value(checks, '2b base still evaluated and exact', norm.get('base_fields'),
                    case_b['expected']['base_fields'], RTOL_VALUE)
        pm = norm.get('per_mode') or {}
        chk(checks, '2b both (nonzero) per-mode results retained',
            all(isinstance((pm.get(m) or {}).get('deltaJ0'), np.ndarray) and
                float(np.max(np.abs(pm[m]['deltaJ0']))) > 0 for m in (a, b)))
        line_once_checks(checks, lambda s: '2b ' + s, case_b, run['trace'])
    return checks


def test_3(h):
    checks = []
    counts = {}
    for name, modes in (('one m=4', {4: RHO[4]}), ('two m=2,6', {6: RHO[6], 2: RHO[2]}),
                        ('all six', {m: RHO[m] for m in (5, 1, 4, 2, 6, 3)})):
        case = build_case('line_once_' + name.replace(' ', '_').replace(',', '_').replace('=', ''),
                          modes=modes)
        run = expect_complete(h, case, checks, name, values=(name == 'all six'))
        tr = run['trace']
        counts[name] = tr.role_counts()
        nR, nP, nZ = case['eval_Z'].shape
        counts[name]['naive_per_mode_prepare_calls'] = 2 * len(modes) * nR * nP
    pc = [counts[n]['prepare_calls'] for n in counts]
    ec = [counts[n]['evaluate_calls'] for n in counts]
    chk(checks, 'prepare_line / evaluate_line call totals independent of the number of modes',
        len(set(pc)) == 1 and len(set(ec)) == 1, prepare=pc, evaluate=ec,
        naive_per_mode=[counts[n]['naive_per_mode_prepare_calls'] for n in counts])
    return checks


def _fail_provider(mods, mode_to_fail, on_call):
    real = provider_dict(mods)['bessel_jn']
    state = collections.Counter()

    def bessel(n, x):
        state[n] += 1
        if n == mode_to_fail and state[n] >= on_call:
            raise RuntimeError('fixture: provider fault for order %d at its call %d' % (n, state[n]))
        return real(n, x)
    return bessel


def test_4(h, mods):
    checks = []
    real = mods['contraction_0445'].nonzero_mode_density_fourier
    modes = {1: RHO[1], 3: RHO[3]}
    base = build_case('partial_base', modes=modes, wave_chunk=1, position_chunk=8)
    ex = base['expected']
    # 4a: the LAST mode (m=3) fails inside 0445 after one committed wave chunk
    c = dict(base, provider_override=provider_dict(mods, _fail_provider(mods, 3, 2)))
    run = expect_reject(h, c, checks, '4a m=3 0445 FAILED_CLOSED (partial)')
    pm = all_per_mode(run['norm'])
    i1, i3 = pm.get(1) or {}, pm.get(3) or {}
    chk(checks, '4a per-mode m=1 retained: COMPLETE', _st(i1) == 'COMPLETE', got=_st(i1))
    check_value(checks, '4a per-mode m=1 retained deltaJ0 vs direct', i1.get('deltaJ0'), ex['per_mode'][1], RTOL_VALUE)
    msk = i3.get('mask')
    chk(checks, '4a per-mode m=3 retained: FAILED_CLOSED with its partial wave mask',
        _st(i3) == 'FAILED_CLOSED' and msk is not None and
        bool(np.any(msk)) and not bool(np.all(msk)), got=_st(i3),
        mask=(None if msk is None else np.asarray(msk).tolist()))
    if msk is not None and i3.get('retained') is not None:
        r3 = np.asarray(i3['retained'])
        check_value(checks, '4a m=3 partial retained rows equal direct values (advisory)', r3[np.asarray(msk)],
                    ex['per_mode'][3][np.asarray(msk)], RTOL_VALUE, advisory=True)
    chk(checks, '4a no total formed from a partial mode (no total exposed)', (run['norm'] or {}).get('total') is None)
    # 4b: the FIRST mode fails
    c = dict(base, provider_override=provider_dict(mods, _fail_provider(mods, 1, 2)))
    run = expect_reject(h, c, checks, '4b m=1 0445 FAILED_CLOSED (first mode)')
    pm = all_per_mode(run['norm'])
    chk(checks, '4b per-mode m=1 retained: FAILED_CLOSED',
        _st(pm.get(1)) == 'FAILED_CLOSED', got=_st(pm.get(1)))
    chk(checks, '4b m=3 after the failing mode: computed or not (advisory, informational)', True, advisory=True,
        m3_status=_st(pm.get(3)),
        contraction_modes_called=[x['mode'] for x in run['trace'].contraction_calls])
    # 4c: forged per-mode results for m=3 (m=1 healthy)
    full3 = real(radius_m=base['src_R'], z_m=base['src_z'], weights_RdRdz_m3=base['src_w'],
                 rho_mode_kg_m3=base['modes'][3], k_physical_inverse_m=base['waves'], c_m_s=base['c'], mode=3,
                 bessel_jn=provider_dict(mods)['bessel_jn'], wave_chunk=1, position_chunk=8)
    nan_row = full3['deltaJ0_J'].copy()
    nan_row[3] = complex(math.nan, math.nan)
    short_mask = full3['retained_wave_mask'].copy()
    short_mask[2] = False
    forged = {
        '4c1 COMPLETE but complete False': dict(full3, complete=False),
        '4c2 COMPLETE with a NaN row': dict(full3, deltaJ0_J=nan_row),
        '4c3 COMPLETE labelled with another mode': dict(full3, counts=dict(full3['counts'], mode=2)),
        '4c4 COMPLETE with nk-1 rows': dict(full3, deltaJ0_J=full3['deltaJ0_J'][:-1].copy()),
        '4c5 status INTERRUPTED': dict(full3, status='INTERRUPTED', complete=False),
        '4c6 FAILED_CLOSED with full retained only': dict(full3, status='FAILED_CLOSED', complete=False,
                                                         deltaJ0_J=None, retained_deltaJ0_J=full3['deltaJ0_J']),
        '4c7 COMPLETE with an incomplete wave mask': dict(full3, retained_wave_mask=short_mask),
        '4c8 not a mapping': None,
        '4c9 0445 reports INVALID_INPUT for m=3': dict(status='INVALID_INPUT', complete=False, deltaJ0_J=None,
                                                       reason='fixture double', counts=dict(full3['counts'])),
    }
    for label, doc in forged.items():
        def hook(inner, kw, n, doc=doc):
            if kw.get('mode') == 3:
                return copy.deepcopy(doc)
            return inner(**kw)
        run = expect_reject(h, base, checks, label, inject=dict(contraction=hook))
        pm = all_per_mode(run['norm'])
        chk(checks, label + ': m=1 per-mode result retained (advisory)',
            _st(pm.get(1)) == 'COMPLETE', advisory=True)
    # 4d: 0445 INVALID_INPUT for one mode (real-dtype coefficients)
    c = dict(base, modes={1: RHO[1], 3: np.array(RHO[3], complex).real.copy()})
    run = expect_reject(h, c, checks, '4d m=3 real-dtype coefficients (0445 INVALID_INPUT or module validation)')
    # 4e: interruption inside the contraction of m=3
    def hook_int(inner, kw, n):
        if kw.get('mode') == 3:
            raise InjectedInterrupt('fixture interrupt in 0445 for m=3')
        return inner(**kw)
    run = h.run(base, inject=dict(contraction=hook_int))
    interrupt_checks(checks, '4e interrupt inside 0445 (m=3)', run, need_modes={1: 'COMPLETE'})
    # 4e2: interruption raised INSIDE the unchanged 0445 (provider, order 3, its 2nd call): 0445
    # attaches its own partial record and re-raises; the module must re-raise with its record
    real_jn = provider_dict(mods)['bessel_jn']
    state = collections.Counter()

    def jn_int(n, x):
        state[n] += 1
        if n == 3 and state[n] >= 2:
            raise InjectedInterrupt('fixture interrupt inside 0445 provider, order 3')
        return real_jn(n, x)
    c = dict(base, provider_override=provider_dict(mods, jn_int))
    run = h.run(c)
    n2 = interrupt_checks(checks, '4e2 interrupt inside 0445 provider (m=3)', run, need_modes={1: 'COMPLETE'})
    if n2 is not None:
        i3 = all_per_mode(n2).get(3) or {}
        chk(checks, '4e2 m=3 0445 INTERRUPTED record kept under its mode (advisory)', _st(i3) == 'INTERRUPTED',
            advisory=True, got=_st(i3))
    # 4f: interruption during the single total evaluation (7th evaluate_line call)
    run = h.run(base, inject=dict(interrupt_evaluate=7))
    att = interrupt_checks(checks, '4f interrupt at evaluate_line call 7', run, need_modes={1: 'COMPLETE', 3: 'COMPLETE'})
    if att is not None:
        n = att
        rm = n.get('retained_point_mask')
        chk(checks, '4f evaluated points retained (advisory)', rm is not None and 0 < int(np.count_nonzero(rm)) <
            rm.size, advisory=True, points=(None if rm is None else int(np.count_nonzero(rm))))
        chk(checks, '4f retained total deltaJ0 equals direct combined (advisory)', n.get('retained_total') is not None
            and rel_err(n['retained_total'], ex['total'])[0] <= RTOL_VALUE, advisory=True)
    # 4g: overflow in the summation itself (each per-mode deltaJ0 finite, ~1e308, same sign)
    c = case_overflow()
    for es in ('raise', 'ignore'):
        run = expect_reject(h, c, checks, '4g sum overflow, errstate=%s' % es, errstate=dict(all=es))
        pm = all_per_mode(run['norm'])
        chk(checks, '4g errstate=%s: both per-mode results retained COMPLETE and finite' % es,
            all(_st(pm.get(m)) == 'COMPLETE' and
                isinstance((pm.get(m) or {}).get('deltaJ0'), np.ndarray) and
                bool(np.all(np.isfinite(pm[m]['deltaJ0']))) for m in (1, 3)))
    return checks


def interrupt_checks(checks, label, run, need_modes):
    exc = run['exc']
    chk(checks, label + ': KeyboardInterrupt re-raised (not swallowed)', isinstance(exc, InjectedInterrupt),
        got=(None if exc is None else type(exc).__name__), status=(run['raw'] or {}).get('status')
        if isinstance(run['raw'], Mapping) else None)
    if not isinstance(exc, InjectedInterrupt):
        return None
    # the dependency 0445 attaches unt0445_retained_result itself; the module's own record is
    # any other unt<N>_retained_result attribute (0452 expected)
    names = [a for a in dir(exc) if re.fullmatch(r'unt\d+_retained_result', a)
             and a != 'unt0445_retained_result']
    att = getattr(exc, names[0]) if len(names) == 1 else None
    chk(checks, label + ': retained result attached, status INTERRUPTED', isinstance(att, Mapping) and
        att.get('status') == 'INTERRUPTED', attribute=names)
    if not isinstance(att, Mapping):
        return None
    n = default_normalize(att, run['trace'].case)
    pm = all_per_mode(n)
    chk(checks, label + ': per-mode results retained %s' % need_modes,
        all(_st(pm.get(m)) == st for m, st in need_modes.items()),
        got={m: _st(v) for m, v in pm.items()})
    chk(checks, label + ': no payload exposed at top level', payload_absent(n))
    return n


def case_overflow():
    """One ring point, waves +-(0.9, 0, 0); c = 1e151; rho_1 = a, rho_3 = -a J1/J3 (real) so that
    deltaJ0_1 == deltaJ0_3 ~ 1.0e308 each; their sum overflows float64."""
    c = 1e151
    R, w = 1.3, 0.45
    j1, j3 = bessel_ref(1, 0.9 * R), bessel_ref(3, 0.9 * R)
    a = 1.0e308 / (c * c * 2 * math.pi * w * j1 * 2)
    src = dict(R=[R], z=[0.0], w=[w])
    case = build_case('overflow_sum', modes={1: [complex(a, 0.0)], 3: [complex(-a * j1 / j3, 0.0)]},
                      base_k=[[0.9, 0.4, 0.0]], src=src, c=c, expect=False)
    waves = np.array([[0.9, 0.0, 0.0], [-0.9, 0.0, 0.0]])
    rows = np.ones((2, 10), complex) * S_UNIT
    case.update(waves=waves, unit=rows[:, :, None], base=(0.2 * rows)[:, :, None])
    return case


def ring_waves(ndir=12, kappa=0.9, kz=0.6):
    ks = []
    for j in range(ndir):
        a = math.pi * j / ndir
        ks.append([kappa * math.cos(a), kappa * math.sin(a), kz])
        ks.append([kappa * math.cos(a), kappa * math.sin(a), -kz])
    return np.array([np.array(k) for k in ks] + [-np.array(k) for k in ks]), ks


def case_anisotropic(beta):
    waves, ks = ring_waves()
    n = len(ks)
    g, hrow = [], []
    for idx in range(len(waves)):
        k = ks[idx % n]
        a = math.atan2(k[1], k[0])
        g.append(1.0 + beta * math.cos(2 * a))           # identical for k and -k
        hrow.append(1.0 / (1 + (idx % n)))
    U0 = np.array(g, complex)[:, None] * S_UNIT[None, :]
    B0 = np.array(hrow, complex)[:, None] * T_BASE[None, :]
    return build_case('anisotropic_beta_%g' % beta, modes={1: RHO[1], 3: 8.0 * np.array(RHO[3])}, base_k=waves,
                      unit_rows=U0, base_rows=B0, z_per_angle=0.0)


def _dft(arr):
    return np.fft.fft(arr, axis=1) / arr.shape[1]


def test_5(h):
    checks = []
    iso, ani = case_anisotropic(0.0), case_anisotropic(0.6)
    si, sa = _dft(iso['expected']['dn']), _dft(ani['expected']['dn'])
    marker = [5, 11]                     # |m| = 5: reachable only through the cos(2 alpha) response
    fi = float(np.max(np.abs(si[:, marker]))) / float(np.max(np.abs(si)))
    fa = float(np.max(np.abs(sa[:, marker]))) / float(np.max(np.abs(sa)))
    chk(checks, 'fixture self-check: isotropic response keeps |m|=5 slots empty', fi <= 1e-12, frac=fi)
    chk(checks, 'fixture self-check: anisotropic response moves m=3 into |m|=5 slots', fa > 5e-3, frac=fa)
    for case, label in ((iso, 'isotropic'), (ani, 'anisotropic')):
        run = expect_complete(h, case, checks, label + ' ring (48 waves, m=1,3)', line_check=False,
                              contraction_check=False)
        n = run['norm']
        if is_complete(n) and n.get('dn') is not None:
            dn = np.asarray(n['dn'])
            chk(checks, label + ': dn keeps all 16 supplied angles', dn.shape == case['eval_Z'].shape, shape=dn.shape)
            if dn.shape == case['eval_Z'].shape:
                check_value(checks, label + ': all 16 DFT slots of module dn == expected', _dft(dn),
                            _dft(case['expected']['dn']), RTOL_VALUE)
                if case is ani:
                    got = float(np.max(np.abs(_dft(dn)[:, marker]))) / float(np.max(np.abs(_dft(dn))))
                    chk(checks, 'anisotropic: |m|=5 content retained in the output (not projected to m=1,3)',
                        abs(got - fa) <= 1e-9 * max(fa, 1e-30) + 1e-14, frac=got, expected=fa)
            if n.get('lin_dphi') is not None and case is ani:
                check_value(checks, 'anisotropic: all 16 DFT slots of module LINEAR dPhi == expected',
                            _dft(np.asarray(n['lin_dphi'])), _dft(ani['expected']['dphi']), RTOL_VALUE)
    return checks


def run_0449(mods, case, mode, errstate=None):
    fn = mods['module_0449'].nonzero_cached_feedback
    with np.errstate(**(errstate or ERRSTATE_DEFAULT)):
        return fn(density_fourier=mods['contraction_0445'].nonzero_mode_density_fourier,
                  jn_provider=provider_dict(mods), radius_m=case['src_R'], z_m=case['src_z'],
                  weights_RdRdz_m3=case['src_w'], rho_mode_kg_m3=case['modes'][mode], mode=mode,
                  k_physical_inverse_m=case['waves'],
                  unit_response=dict(wavevectors=case['waves'], weighted_responses=case['unit']),
                  base_prepared=dict(wavevectors=case['waves'], weighted_responses=case['base']),
                  prepare_line=mods['line'].prepare_line, evaluate_line=mods['line'].evaluate_line,
                  eval_radius_m=case['eval_R'], eval_phi_rad=case['eval_phi'], eval_z_m=case['eval_Z'],
                  c_m_s=case['c'], base_reality_atol=case['atol_base'], base_reality_rtol=case['rtol_base'],
                  increment_reality_atol=case['atol_inc'], increment_reality_rtol=case['rtol_inc'],
                  wave_chunk=case['wave_chunk'], position_chunk=case['position_chunk'],
                  include_log_difference=case['include_log'], provenance=case['provenance'])


def test_6(h, mods):
    checks = []
    for m in (1, 3, 6):
        case = build_case('one_mode_vs_0449_m%d' % m, modes={m: RHO[m]}, include_log=True)
        ref = run_0449(mods, case, m)
        chk(checks, 'm=%d pinned 0449 COMPLETE on this fixture' % m, ref.get('status') == 'COMPLETE',
            reason=ref.get('reason'))
        run = h.run(case)
        n = run['norm']
        if run['exc'] is not None or not is_complete(n):
            chk(checks, 'm=%d module COMPLETE' % m, False, **status_line(run))
            continue
        pairs = [('total deltaJ0 vs 0449 deltaJ0_J', n.get('total'), ref['deltaJ0_J']),
                 ('per-mode deltaJ0 vs 0449 deltaJ0_J', ((n.get('per_mode') or {}).get(m) or {}).get('deltaJ0'),
                  ref['deltaJ0_J']),
                 ('delta_prepared', n.get('delta_prepared'), ref['delta_prepared']['weighted_responses'])]
        for kind in ('fields', 'gradient', 'hessian'):
            pairs.append(('base_line ' + kind, n.get('base_' + kind), ref['base_line'][kind]))
            pairs.append(('increment_line ' + kind, n.get('inc_' + kind), ref['increment_line'][kind]))
        for key in ('nb', 'dn', 'Nb'):
            pairs.append(('lapse ' + key, n.get(key), ref['lapse'][key]))
        pairs += [('LINEAR dPhi', n.get('lin_dphi'), ref['linear']['deltaPhi_m2_s2']),
                  ('LINEAR grad Cartesian', n.get('lin_grad'), ref['linear']['grad_deltaPhi_cartesian_m_s2']),
                  ('LINEAR grad cylindrical', n.get('lin_grad_cyl'),
                   ref['linear']['grad_deltaPhi_cylindrical_R_phi_z_m_s2']),
                  ('LOG dPhi', n.get('log_dphi'), ref['log_difference']['deltaPhi_m2_s2']),
                  ('LOG grad Cartesian', n.get('log_grad'), ref['log_difference']['grad_deltaPhi_cartesian_m_s2']),
                  ('point_mask', n.get('point_mask'), ref['point_mask'])]
        bitwise = []
        for label, got, want in pairs:
            check_value(checks, 'm=%d one-mode == 0449: %s' % (m, label), got, want, RTOL_0449)
            if got is not None and np.array_equal(np.asarray(got), np.asarray(want)):
                bitwise.append(label)
        chk(checks, 'm=%d one-mode == 0449 bitwise (advisory, informational)' % m, len(bitwise) == len(pairs),
            advisory=True, bitwise=len(bitwise), of=len(pairs),
            not_bitwise=[p[0] for p in pairs if p[0] not in bitwise])
        chk(checks, 'm=%d line call counts equal 0449 expectation (advisory)' % m,
            run['trace'].role_counts()['prepare_calls'] == ref['completeness']['line_prepare_calls'] and
            run['trace'].role_counts()['evaluate_calls'] == ref['completeness']['line_evaluate_calls'],
            advisory=True)
    # failure parity: Nb <= 0 -> both reject (stage advisory)
    case = build_case('parity_Nb_nonpositive', modes={2: RHO[2]}, base_target=1.6)
    case['base'] = -case['base']
    ref = run_0449(mods, case, 2)
    run = h.run(case)
    n = run['norm']
    chk(checks, 'parity: Nb <= 0 rejected by 0449 and by the module', ref.get('status') != 'COMPLETE' and
        run['exc'] is None and not is_complete(n), ref_stage=ref.get('failure_stage'), **status_line(run))
    chk(checks, 'parity: same failure stage (advisory)', isinstance(run['raw'], Mapping) and
        run['raw'].get('failure_stage') == ref.get('failure_stage'), advisory=True,
        ref=ref.get('failure_stage'), got=(run['raw'] or {}).get('failure_stage') if isinstance(run['raw'], Mapping) else None)
    return checks


class DupMapping(Mapping):
    """A Mapping whose iteration yields a key twice (duplicate mode keys)."""

    def __init__(self, items):
        self._items = list(items)

    def __getitem__(self, key):
        for k, v in self._items:
            if k == key and type(k) is type(key):
                return v
        raise KeyError(key)

    def __iter__(self):
        return iter([k for k, _ in self._items])

    def __len__(self):
        return len(self._items)


def test_7(h):
    checks = []
    for modes, inc, om in (({3: RHO[3], 1: RHO[1]}, [1, 3], [2, 4, 5, 6]),
                           ({5: RHO[5]}, [5], [1, 2, 3, 4, 6]),
                           ({m: RHO[m] for m in (6, 5, 4, 3, 2, 1)}, [1, 2, 3, 4, 5, 6], [])):
        case = build_case('metadata_%s' % '_'.join(map(str, sorted(modes))), modes=modes)
        run = h.run(case)
        n = run['norm']
        if run['exc'] is not None or not is_complete(n):
            chk(checks, 'metadata run %s COMPLETE' % sorted(modes), False, **status_line(run))
            continue
        chk(checks, 'included modes listed = %s' % inc, n.get('included') is not None and sorted(n['included']) == inc,
            got=n.get('included'), path=n.get('included__path'))
        chk(checks, 'omitted modes listed = %s (of 1..6)' % om, n.get('omitted') is not None and sorted(n['omitted']) == om,
            got=n.get('omitted'), path=n.get('omitted__path'))
        chk(checks, 'included order ascending (advisory, informational)', n.get('included') == inc, advisory=True,
            got=n.get('included'))
        chk(checks, 'no nominal single-mode tag on the combined result (int "mode" key outside per-mode results)',
            not n.get('single_mode_tags'), tags=n.get('single_mode_tags'))
    # failure dicts also carry the lists (advisory)
    base = build_case('reject_base', modes={1: RHO[1], 3: RHO[3]}, expect=True)
    bad = {
        'empty mapping {}': {},
        'non-mapping list of pairs': [(1, base['modes'][1])],
        'key 0': {0: base['modes'][1]},
        'key 7': {7: base['modes'][1]},
        'key -1': {-1: base['modes'][1]},
        'bool key True': {True: base['modes'][1]},
        'bool key False': {False: base['modes'][1]},
        'float key 1.0': {1.0: base['modes'][1]},
        'str key "1"': {'1': base['modes'][1]},
        'duplicate key (Mapping iterating 1, 3, 1)': DupMapping([(1, base['modes'][1]), (3, base['modes'][3]),
                                                                  (1, base['modes'][3])]),
        'mismatched coefficient length (m=3 has q-1)': {1: base['modes'][1], 3: base['modes'][3][:-1].copy()},
        'real-dtype coefficients (m=1)': {1: base['modes'][1].real.copy(), 3: base['modes'][3]},
        'None coefficients (m=3)': {1: base['modes'][1], 3: None},
        'mode 1 valid, key 8 invalid': {1: base['modes'][1], 8: base['modes'][3]},
    }
    key_level = ('empty', 'non-mapping', 'key 0', 'key 7', 'key -1', 'bool', 'float', 'str', 'duplicate', 'key 8')
    for label, modes in bad.items():
        c = dict(base, modes=modes)
        run = expect_reject(h, c, checks, 'reject ' + label)
        if any(t in label for t in key_level):
            raw = run['raw'] if isinstance(run['raw'], Mapping) else {}
            chk(checks, 'reject %s: INVALID_INPUT with no 0445 call (advisory)' % label,
                raw.get('status') == 'INVALID_INPUT' and not run['trace'].contraction_calls, advisory=True,
                status=raw.get('status'), contraction_calls=len(run['trace'].contraction_calls))
    c = dict(base, modes={np.int64(1): base['modes'][1]})
    run = h.run(c)
    chk(checks, 'numpy int64 key: behaviour recorded (advisory, informational)', True, advisory=True,
        **status_line(run))
    return checks


def test_8(h):
    checks = []
    params = h.params
    kinds = {n: p.kind for n, p in params.items()}
    chk(checks, 'all parameters keyword-only', all(k == inspect.Parameter.KEYWORD_ONLY for k in kinds.values()),
        non_kw=[n for n, k in kinds.items() if k != inspect.Parameter.KEYWORD_ONLY])
    chk(checks, 'no parameter has a default', all(p.default is p.empty for p in params.values()),
        with_default=[n for n, p in params.items() if p.default is not p.empty])
    try:
        mapping = resolve_params(params)
        missing = [c for c in CONTROLS_0449 if c not in mapping.values()]
        chk(checks, 'every 0449 caller control (+ the mode mapping) is an explicit parameter', not missing,
            missing=missing, mapping=mapping)
        extra = [n for n in params if n not in mapping]
        chk(checks, 'no unmapped extra parameter (advisory)', not extra, advisory=True, extra=extra)
    except AdapterUnresolved as exc:
        chk(checks, 'parameter mapping', False, detail=str(exc))
    case = build_case('signature_missing', modes={1: RHO[1]})
    trace = Trace(case)
    values = canonical_values(case, h.mods, trace)
    kwargs = h.make_kwargs(params, case, values) if h.make_kwargs else default_make_kwargs(params, case, values)
    for drop in ('include_log_difference', 'wave_chunk', 'increment_reality_atol', 'c_m_s'):
        if drop not in kwargs:
            continue
        kw = dict(kwargs)
        kw.pop(drop)
        try:
            h.fn(**kw)
            ok, why = False, 'no error'
        except TypeError as exc:
            ok, why = True, str(exc)
        chk(checks, 'missing %s raises TypeError (no default)' % drop, ok, detail=why[:200])
    return checks


FORBIDDEN_ATTRS = {'dot', 'matmul', 'tensordot', 'vdot', 'inner', 'linalg', 'errstate', 'seterr',
                   'load', 'loadtxt', 'save', 'savez', 'fromfile', 'tofile', 'filterwarnings',
                   'simplefilter', 'catch_warnings', 'nan_to_num', 'clip', 'real_if_close', 'fft', 'mean'}
FORBIDDEN_NAMES = {'open', 'exec', 'eval', '__import__', 'print'}


def test_9(h, path, import_output):
    checks = []
    src = open(path, 'rb').read().decode('utf-8')
    tree = ast.parse(src)
    imports, bad = set(), []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(a.name for a in node.names)
        elif isinstance(node, ast.ImportFrom):
            imports.add(node.module)
        elif isinstance(node, ast.Attribute) and node.attr in FORBIDDEN_ATTRS:
            bad.append('attr %s line %d' % (node.attr, node.lineno))
        elif isinstance(node, ast.Name) and node.id in FORBIDDEN_NAMES:
            bad.append('name %s line %d' % (node.id, node.lineno))
        elif isinstance(node, ast.BinOp) and isinstance(node.op, ast.MatMult):
            bad.append('@ line %d' % node.lineno)
        elif isinstance(node, ast.keyword) and node.arg == 'optimize':
            if not (isinstance(node.value, ast.Constant) and node.value.value is False):
                bad.append('einsum optimize not False line %d' % node.value.lineno)
    top = [type(n).__name__ for n in tree.body
           if not isinstance(n, (ast.Import, ast.ImportFrom, ast.FunctionDef, ast.ClassDef, ast.Assign))
           and not (isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant))]
    nonstd = sorted(m for m in imports if m and m.split('.')[0] not in sys.stdlib_module_names
                    and m.split('.')[0] != 'numpy')
    chk(checks, 'imports numpy + stdlib only', not nonstd, advisory=True, imports=sorted(i for i in imports if i))
    chk(checks, 'no BLAS/IO/warning-suppression/clipping/projection tokens', not bad, advisory=True, hits=bad)
    chk(checks, 'module top level: definitions/assignments only', not top, advisory=True, other=top)
    chk(checks, 'import printed nothing', import_output == '', advisory=True, output=import_output[:200])
    outs = []
    for wc, pc in ((1, 1), (5, 3)):
        case = build_case('chunk_%d_%d' % (wc, pc), modes={1: RHO[1], 3: RHO[3]}, wave_chunk=wc, position_chunk=pc)
        run = h.run(case)
        outs.append(run['norm'] if is_complete(run['norm']) else None)
    if all(outs):
        for key in ('total', 'delta_prepared', 'inc_fields', 'lin_dphi', 'lin_grad'):
            if outs[0].get(key) is not None:
                e = rel_err(outs[0][key], outs[1][key])[0]
                chk(checks, 'chunks (1,1) vs (5,3): %s' % key, e is not None and e <= RTOL_CHUNK, advisory=True,
                    max_rel_diff=e)
    else:
        chk(checks, 'chunk runs COMPLETE', False, advisory=True)
    case = build_case('provenance_echo', modes={1: RHO[1], 3: RHO[3]})
    run = h.run(case)
    n = run['norm']
    chk(checks, 'supplied provenance echoed unchanged', n is not None and _deep_equal(n.get('provenance'),
        case['provenance']), advisory=True)
    chk(checks, 'caller arrays, packets and the mode mapping unchanged after the call', not run['mutated'],
        advisory=True, mutated=run['mutated'])
    return checks


TESTS = '123456789'
BINDING = set('12345678')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--module', required=True)
    ap.add_argument('--function', required=True)
    ap.add_argument('--outdir', required=True)
    ap.add_argument('--adapter', default=None)
    ap.add_argument('--only', default=TESTS)
    a = ap.parse_args()
    t0 = time.monotonic()
    msha = sha256_file(a.module)
    print('MODULE %s sha256 %s' % (a.module, msha), flush=True)
    me = os.path.abspath(__file__)
    print('FIXTURE %s sha256 %s' % (me, sha256_file(me)), flush=True)
    mods, pins = load_pinned()
    for key, row in pins.items():
        print('PIN %-16s %s %s' % (key, row['sha256'], 'OK' if row['match'] else 'MISMATCH'), flush=True)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
        module = load_path(a.module, 'unt0452fx_target')
    import_output = buf.getvalue()
    fn = getattr(module, a.function)
    adapter = load_path(a.adapter, 'unt0452fx_adapter') if a.adapter else None
    h = Harness(fn, mods, adapter)
    report = dict(module=a.module, module_sha256_before=msha, function=a.function, fixture=me,
                  fixture_sha256=sha256_file(me), pins=pins, interpreter=sys.executable,
                  python=sys.version.split()[0], numpy=np.__version__,
                  blas_env={k: os.environ.get(k) for k in ('VECLIB_MAXIMUM_THREADS', 'OPENBLAS_NUM_THREADS',
                                                          'OMP_NUM_THREADS')},
                  errstate_default=ERRSTATE_DEFAULT, import_output=import_output,
                  signature=str(inspect.signature(fn)), tests={})
    runners = {'1': lambda: test_1(h), '2': lambda: test_2(h, mods), '3': lambda: test_3(h),
               '4': lambda: test_4(h, mods), '5': lambda: test_5(h), '6': lambda: test_6(h, mods),
               '7': lambda: test_7(h), '8': lambda: test_8(h), '9': lambda: test_9(h, a.module, import_output)}
    for key in [k for k in a.only.replace(',', '') if k in runners]:
        ts = time.monotonic()
        try:
            checks = runners[key]()
            verdict = 'PASS' if all(c['ok'] for c in checks if not c.get('advisory')) else 'FAIL'
        except AdapterUnresolved as exc:
            checks, verdict = [dict(check='adapter', ok=False, detail=str(exc))], 'ADAPTER_UNRESOLVED'
        except Exception:
            checks, verdict = [dict(check='harness', ok=False, detail=traceback.format_exc())], 'ERROR'
        binding = key in BINDING
        report['tests'][key] = dict(verdict=verdict, binding=binding, seconds=time.monotonic() - ts, checks=checks)
        nb = sum(1 for c in checks if not c['ok'] and not c.get('advisory'))
        na = sum(1 for c in checks if not c['ok'] and c.get('advisory'))
        print('TEST %s %-11s %-18s %3d checks, %d binding not ok, %d advisory not ok  (%.2fs)' % (
            key, '[binding]' if binding else '[advisory]', verdict, len(checks), nb, na,
            time.monotonic() - ts), flush=True)
        for c in checks:
            if not c['ok']:
                info = {k: v for k, v in c.items() if k not in ('check', 'ok')}
                print('   not ok%s: %s %s' % (' (advisory)' if c.get('advisory') else '', c['check'],
                                              str(info)[:600]), flush=True)
    report['calls'] = h.calls
    report['seconds'] = time.monotonic() - t0
    report['module_sha256_after'] = sha256_file(a.module)
    nbind = sum(len([c for c in report['tests'][k]['checks'] if not c.get('advisory')]) for k in report['tests']
                if k in BINDING)
    report['binding_checks'] = nbind
    report['overall_binding'] = 'PASS' if all(report['tests'][k]['verdict'] == 'PASS' for k in report['tests']
                                              if k in BINDING) and report['module_sha256_after'] == msha \
        else 'NOT_PASS'
    os.makedirs(a.outdir, exist_ok=True)
    out = os.path.join(a.outdir, 'fixtures_0452_result_%s.json' % msha[:16])
    with open(out, 'w') as handle:
        json.dump(report, handle, indent=1, default=_json_default)
    print('MODULE sha256 after run %s (%s)' % (report['module_sha256_after'],
                                               'unchanged' if report['module_sha256_after'] == msha else 'CHANGED'))
    print('OVERALL_BINDING %s  binding checks=%d  calls=%d  %.2fs  report %s sha256 %s' % (
        report['overall_binding'], nbind, h.calls, report['seconds'], out, sha256_file(out)), flush=True)
    return 0 if report['overall_binding'] == 'PASS' else 1


def _json_default(o):
    if isinstance(o, complex):
        return [o.real, o.imag]
    if isinstance(o, np.generic):
        return o.item() if not isinstance(o, np.complexfloating) else [float(o.real), float(o.imag)]
    if isinstance(o, np.ndarray):
        return dict(ndarray_shape=list(o.shape), dtype=str(o.dtype))
    if isinstance(o, (set, frozenset)):
        return sorted(o)
    return repr(o)


if __name__ == '__main__':
    sys.exit(main())
