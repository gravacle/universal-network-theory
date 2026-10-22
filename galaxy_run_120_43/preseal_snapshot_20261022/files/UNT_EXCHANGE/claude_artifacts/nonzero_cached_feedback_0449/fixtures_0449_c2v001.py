"""UNT 0449 independent analytic fixtures (fixture helper, c2v001).

Tests a supplied 0449 binding callable ("bind the accepted nonzero-density 0445
transform to the cached full ten-component response, then the linear lapse") on
SMALL SYNTHETIC ANALYTIC inputs only. No project packet, no .npz, no root worker,
no galaxy run, no target data.

Usage (root interpreter, isolated, single-thread BLAS):
  VECLIB_MAXIMUM_THREADS=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
  python3 -I -B fixtures_0449_c2v001.py --module PATH --function NAME --outdir DIR \
      [--adapter ADAPTER.py] [--only a,b,...]

The module is loaded by importlib from PATH after its sha256 is computed from
bytes and printed. The pinned 0445 contraction, the sibling J_n provider and the
fixed-xy line module are loaded only after their sha256 matches the 0449 pins.

Expectations are INDEPENDENT of the module and of the line module:
  J_m(x)        ascending series in decimal (exact binary x, 80 digits);
  deltaJ0(k)    the 0445 equation transcribed term by term with cmath;
  delta_prep    U[k,a,0] * deltaJ0(k) (U synthetic, per-component constants);
  field/jets    direct Python sums  sum_k A_k e^{i k.x},  i k_j (..),  -k_i k_j (..);
  lapse         Nb = 1 + Re n_base, dPhi = c^2 dn/Nb,
                grad = c^2 (grad dn/Nb - dn grad nb/Nb^2), log variant separately;
  gradient      4th-order central finite differences of the closed-form dPhi(x,y,z).

Adapter: the default adapter maps the module's keyword-only parameters by name
(see ALIASES) and reads outputs by key paths (see OUTPUT_PATHS). A different
interface can be bound with --adapter FILE defining make_kwargs(params, case) ->
dict and/or normalize(result, case) -> dict (keys as in _normalize below).
An unresolved parameter or output is reported as ADAPTER_UNRESOLVED, never PASS.

Tests (BINDING unless marked ADVISORY):
  a  one-wave and paired +-k sources: deltaJ0, delta_prepared (order, sign, every
     factor), complex full-ten fields and Cartesian jets, linear lapse, closed form
  b  linear dPhi gradient vs finite differences of the closed-form dPhi, plus the
     module's own dPhi differenced along R and z; linear never replaced by log
  c  Nb <= 0 rejected; Nb + dn <= 0 rejects the log difference (linear unaffected)
  d  partial / non-COMPLETE / forged 0445 results and a non-READY provider rejected
  e  imaginary remainder above caller tolerance rejected pointwise (incl. one that
     averages to zero over the 16 angles, one only in a non-lapse component and one
     only in the base), each with a passing control
  f  all 16 angles returned (uniform, offset and per-angle heights); anisotropic
     response that moves m=1 into m=3 slots preserved pointwise and in the DFT
  g  FloatingPointError under errstate('raise') and nonfinite under 'ignore'
     -> fail-closed dict, never raised (lane convention; retention reported ADVISORY)
  h  chunk invariance (ADVISORY)
  i  import inertness and lane AST scan (ADVISORY, informational)
  j  provenance echo, input immutability, accepted log variant values (ADVISORY)
"""
import argparse
import ast
import cmath
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
import sys
import time
import traceback

import numpy as np

# ---------------------------------------------------------------------------
# Pins (task 0449, sha256 b7e1cdc3cd4a45d6c4dd36136ff9f720c7a5362adc683560f4f0775dda675cc4)
# ---------------------------------------------------------------------------
_EX = '/Users/bgm/Research/UNT_EXCHANGE'
_FC = ('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/'
       'FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers')
PINS = {
    'task_0449': (_EX + '/FROM_CODEX/0449_2026-10-16_claude2_nonzero_cached_feedback_binding.md',
                  'b7e1cdc3cd4a45d6c4dd36136ff9f720c7a5362adc683560f4f0775dda675cc4'),
    'contraction_0445': (_EX + '/claude_artifacts/nonzero_density_fourier_0445/'
                         'nonzero_density_fourier_c2v001.py',
                         '255e09f4889b6ed470e3424d3a3c41f3a21c433f3095e04ea12af7a96bc5aaf4'),
    'provider_0445': (_EX + '/claude_artifacts/nonzero_density_fourier_0445/'
                      'posix_libm_bessel_jn_provider_c2v001.py',
                      '9ec3f1c9fb8afe1ffa4a2bb24df5daf4d2695aa51574984658cb753cfc304f67'),
    'line': (_FC + '/recovered_packet_audit/owned_fixed_xy_fourier_line_v002.py',
             '3a47419d88f24e5f6f0f1c2db1ea85cf4108057a3ddb94db608cd05e94822d18'),
}
LOADABLE = ('contraction_0445', 'provider_0445', 'line')

RTOL_VALUE = 1e-10       # closed-form comparisons, relative to max |expected| of the array
RTOL_FD = 1e-7           # finite-difference gradient comparisons
RTOL_CHUNK = 1e-13       # chunk invariance
TIGHT = 1e-11            # tight reality tolerance (atol and rtol) for real fields
LOOSE = 1e3              # permissive reality tolerance for intentionally complex one-wave fields
C_TEST = 3.7             # c: distinct from 1, 2pi and dk-like factors


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
    mods = {key: load_path(PINS[key][0], 'unt0449fx_' + key) for key in LOADABLE}
    return mods, seen


# ---------------------------------------------------------------------------
# Independent references
# ---------------------------------------------------------------------------
_MINUS_I = (1 + 0j, -1j, -1 + 0j, 1j)


def bessel_ref(m, x):
    """J_m(x), ascending series in decimal from the exact binary x (0 <= x <= 40)."""
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


def expected_deltaJ0(waves, R, z, w, rho, m, c):
    out = []
    for kx, ky, kz in waves:
        kp = math.hypot(kx, ky)
        al = math.atan2(ky, kx)
        s = 0j
        for Rq, zq, wq, rq in zip(R, z, w, rho):
            jm = bessel_ref(m, kp * Rq)
            bracket = rq * cmath.exp(1j * m * al) + rq.conjugate() * cmath.exp(-1j * m * al)
            s += wq * jm * cmath.exp(-1j * kz * zq) * bracket
        out.append(-(c * c) * (2 * math.pi) * _MINUS_I[m % 4] * s)
    return np.array(out, dtype=complex)


def direct_jets(waves, amps, x, y, z):
    """sum_k A_k e^{ik.x}, its Cartesian gradient and Hessian, per component (pure Python)."""
    nc = amps.shape[1]
    F = [0j] * nc
    G = [[0j] * 3 for _ in range(nc)]
    H = [[[0j] * 3 for _ in range(3)] for _ in range(nc)]
    for k, A in zip(waves, amps):
        e = cmath.exp(1j * (k[0] * x + k[1] * y + k[2] * z))
        for a in range(nc):
            t = complex(A[a]) * e
            if t == 0:
                continue
            F[a] += t
            for i in range(3):
                G[a][i] += 1j * k[i] * t
                for j in range(3):
                    H[a][i][j] += -k[i] * k[j] * t
    return np.array(F), np.array(G), np.array(H)


def points_of(R, phi, Z):
    """Cartesian points (nR, nphi, nz, 3) from radii, angles and heights (nR, nphi, nz)."""
    nR, nP, nZ = Z.shape
    P = np.empty((nR, nP, nZ, 3))
    for i in range(nR):
        for j in range(nP):
            for l in range(nZ):
                P[i, j, l] = (R[i] * math.cos(phi[j]), R[i] * math.sin(phi[j]), Z[i, j, l])
    return P


def field_grid(waves, amps, P):
    nR, nP, nZ, _ = P.shape
    nc = amps.shape[1]
    F = np.empty((nR, nP, nZ, nc), complex)
    G = np.empty((nR, nP, nZ, nc, 3), complex)
    H = np.empty((nR, nP, nZ, nc, 3, 3), complex)
    for idx in np.ndindex(nR, nP, nZ):
        F[idx], G[idx], H[idx] = direct_jets(waves, amps, *P[idx])
    return F, G, H


def lapse_expect(c, baseF, baseG, incF, incG):
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
    return dict(nb=nb, dn=dn, Nb=Nb, grad_nb=gnb, grad_dn=gdn, dphi=dphi, grad=grad,
                logphi=logphi, loggrad=loggrad)


def dphi_closed(c, waves, inc_amp0, base_amp0, x, y, z):
    """Closed-form linear dPhi at one point from the lapse-component amplitudes."""
    dn = 0j
    nb = 0j
    for k, a, b in zip(waves, inc_amp0, base_amp0):
        e = cmath.exp(1j * (k[0] * x + k[1] * y + k[2] * z))
        dn += a * e
        nb += b * e
    return c * c * dn.real / (1.0 + nb.real)


def fd_gradient(fun, p, h):
    g = np.empty(3)
    for i in range(3):
        def at(s):
            q = list(p)
            q[i] += s * h
            return fun(*q)
        g[i] = (-at(2) + 8 * at(1) - 8 * at(-1) + at(-2)) / (12 * h)
    return g


# ---------------------------------------------------------------------------
# Synthetic cases
# ---------------------------------------------------------------------------
S_UNIT = np.array([1.0, -0.6, 0.45, 0.3, -0.25, 0.2, 0.15, -0.12, 0.1, 0.08])
T_BASE = np.array([1.0, 0.5, -0.4, 0.3, 0.2, -0.2, 0.1, 0.1, -0.05, 0.05])
SRC3 = dict(R=[0.8, 1.5, 2.2], z=[-0.1, 0.2, 0.05], w=[0.3, 0.5, 0.4],
            rho=[0.7 + 0.2j, -0.3 + 0.5j, 0.1 - 0.4j])
SRC1 = dict(R=[1.3], z=[0.15], w=[0.45], rho=[0.6 - 0.35j])
EVAL_R = [1.7, 2.9]
EVAL_Z = [[-0.4, 0.05, 0.6], [-0.25, 0.3, 0.9]]
NPHI = 16


def roster(phi_offset=0.0, z_per_angle=0.0, R=None, Z=None):
    R = np.array(EVAL_R if R is None else R, float)
    Zr = np.array(EVAL_Z if Z is None else Z, float)
    phi = np.array([2 * math.pi * j / NPHI + phi_offset for j in range(NPHI)])
    Z3 = np.empty((len(R), NPHI, Zr.shape[1]))
    for j in range(NPHI):
        Z3[:, j, :] = Zr + z_per_angle * j
    return R, phi, Z3


def paired(ks):
    """Signed wave list: each k followed later by its exact negation (order mixed)."""
    ks = [np.array(k, float) for k in ks]
    pos = list(ks)
    neg = [-k for k in ks]
    order = []
    for i in range(len(ks)):
        order.append(pos[i] if i % 2 == 0 else neg[i])
    for i in range(len(ks)):
        order.append(neg[i] if i % 2 == 0 else pos[i])
    return np.array(order)


def scale_to(waves, row_amp, P, target):
    """Scale so that max over P of |sum_k row_amp_k e^{ik.x}| == target."""
    peak = 0.0
    for idx in np.ndindex(P.shape[:3]):
        x, y, z = P[idx]
        s = sum(a * cmath.exp(1j * (k[0] * x + k[1] * y + k[2] * z)) for k, a in zip(waves, row_amp))
        peak = max(peak, abs(s))
    return target / peak


def build_case(name, *, src, mode, waves, unit_rows, base_rows, inc_target, base_target,
               R, phi, Z, atol_inc, rtol_inc, atol_base, rtol_base, include_log=False,
               c=C_TEST, wave_chunk=2, position_chunk=2, expect=True, unit_override=None,
               base_override=None):
    """unit_rows (nk,) per-wave factor g_k; U[k,a,0] = sigma S_UNIT[a] g_k (unless override).
    base_rows (nk,) per-wave factor h_k; B[k,a,0] = tau T_BASE[a] h_k (unless override)."""
    waves = np.array(waves, float)
    P = points_of(R, phi, Z)
    dJ = expected_deltaJ0(waves, src['R'], src['z'], src['w'], src['rho'], mode, c) if expect \
        else None
    g = np.asarray(unit_rows, complex)
    h = np.asarray(base_rows, complex)
    if expect and inc_target is not None:
        sigma = scale_to(waves, g * dJ, P, inc_target)
    else:
        sigma = 1.0
    tau = scale_to(waves, h, P, base_target) if base_target else 0.0
    U = (sigma * S_UNIT[None, :] * g[:, None])[:, :, None].astype(complex)
    B = (tau * T_BASE[None, :] * h[:, None])[:, :, None].astype(complex)
    if unit_override is not None:
        U = unit_override(U, waves, sigma)
    if base_override is not None:
        B = base_override(B, waves, tau)
    case = dict(
        name=name, mode=mode, c=c, waves=waves,
        src_R=np.array(src['R'], float), src_z=np.array(src['z'], float),
        src_w=np.array(src['w'], float), src_rho=np.array(src['rho'], complex),
        unit=U, base=B, eval_R=R, eval_phi=phi, eval_Z=Z, points=P,
        atol_inc=atol_inc, rtol_inc=rtol_inc, atol_base=atol_base, rtol_base=rtol_base,
        include_log=include_log, wave_chunk=wave_chunk, position_chunk=position_chunk,
        provenance=dict(fixture='UNT0449 fixtures c2v001', case=name, synthetic=True,
                        nested=dict(tag='provenance-echo-' + name, n=7)),
        sigma=sigma, tau=tau)
    if expect:
        dprep = U * dJ[:, None, None]
        incF, incG, incH = field_grid(waves, dprep[:, :, 0], P)
        baseF, baseG, baseH = field_grid(waves, B[:, :, 0], P)
        ex = dict(deltaJ0=dJ, delta_prepared=dprep, inc_fields=incF, inc_gradient=incG,
                  inc_hessian=incH, base_fields=baseF, base_gradient=baseG, base_hessian=baseH)
        ex.update(lapse_expect(c, baseF, baseG, incF, incG))
        case['expected'] = ex
    return case


def case_one_wave(tight_inc=False, zero_base=False):
    k = [[0.9, -0.4, 0.7]]
    R, phi, Z = roster()
    return build_case('one_wave' + ('_tight' if tight_inc else '') + ('_zerobase' if zero_base else ''),
                      src=SRC1, mode=1, waves=k, unit_rows=[1.0], base_rows=[1.0],
                      inc_target=0.25, base_target=(None if zero_base else 0.3),
                      R=R, phi=phi, Z=Z,
                      atol_inc=(TIGHT if tight_inc else LOOSE), rtol_inc=(TIGHT if tight_inc else LOOSE),
                      atol_base=LOOSE, rtol_base=LOOSE)


PAIR_K = [[0.9, 0.4, 0.7], [-0.3, 1.1, -0.5], [0.0, 0.0, 0.8]]
# Hermitian per-pair factors: g for +k (as listed in PAIR_K), conj(g) for -k -> real fields,
# yet every wave row differs (wave-order, +-k swap and conjugation errors are visible).
PAIR_G = [1.0 * cmath.exp(0.4j), 0.7 * cmath.exp(-1.1j), 1.3 * cmath.exp(2.0j)]
PAIR_H = [1.0 * cmath.exp(-0.3j), 0.6 * cmath.exp(0.9j), 0.8 * cmath.exp(1.7j)]


def _herm_rows(waves, table):
    rows = []
    for k in waves:
        for i, b in enumerate(PAIR_K):
            b = np.array(b, float)
            if np.array_equal(k, b):
                rows.append(table[i])
                break
            if np.array_equal(k, -b):
                rows.append(table[i].conjugate())
                break
        else:
            raise ValueError('wave not in PAIR_K pairs')
    return rows


def case_paired(name='paired', mode=3, inc_target=0.25, base_target=0.3, include_log=False,
                phi_offset=0.0, z_per_angle=0.0, R=None, Z=None, wave_chunk=2, position_chunk=2,
                atol=TIGHT, rtol=TIGHT, base_sign=1.0):
    waves = paired(PAIR_K)
    R_, phi, Z_ = roster(phi_offset, z_per_angle, R, Z)
    return build_case(name, src=SRC3, mode=mode, waves=waves,
                      unit_rows=_herm_rows(waves, PAIR_G), base_rows=_herm_rows(waves, PAIR_H),
                      inc_target=inc_target, base_target=base_target, R=R_, phi=phi, Z=Z_,
                      atol_inc=atol, rtol_inc=rtol, atol_base=atol, rtol_base=rtol,
                      include_log=include_log, wave_chunk=wave_chunk, position_chunk=position_chunk,
                      base_override=(None if base_sign == 1.0 else (lambda B, w, t: base_sign * B)))


def ring_waves(kappa=0.9, kz=0.6, ndir=4):
    ks = []
    for j in range(ndir):
        a = math.pi * j / ndir
        ks.append([kappa * math.cos(a), kappa * math.sin(a), kz])
        ks.append([kappa * math.cos(a), kappa * math.sin(a), -kz])
    out = []
    for k in ks:
        out.append(np.array(k))
    for k in ks:
        out.append(-np.array(k))
    return np.array(out), ks


def case_anisotropic(beta):
    waves, ks = ring_waves()
    n = len(ks)
    g = []
    for idx in range(len(waves)):
        k = ks[idx % n]
        a = math.atan2(k[1], k[0])
        g.append(1.0 + beta * math.cos(2 * a))       # identical for k and -k (exact symmetry)
    h = [1.0 / (1 + (idx % n)) for idx in range(len(waves))]
    R, phi, Z = roster()
    return build_case('anisotropic_beta_%g' % beta, src=SRC3, mode=1, waves=waves,
                      unit_rows=g, base_rows=h, inc_target=0.25, base_target=0.3,
                      R=R, phi=phi, Z=Z, atol_inc=TIGHT, rtol_inc=TIGHT,
                      atol_base=TIGHT, rtol_base=TIGHT)


def case_xpair(name, eta_unit=0.0, eta_comp=0, eta_base=0.0):
    """Waves (+-kappa,0,0), kz = 0, mode 2 -> deltaJ0 real; U(+k) - U(-k) = 2 eta sigma S[a]
    in component eta_comp gives Im = 2 eta dJ sin(kappa x): odd in x, zero 16-angle mean."""
    waves = np.array([[0.9, 0.0, 0.0], [-0.9, -0.0, -0.0]])
    R, phi, Z = roster()

    def uo(U, w, sigma):
        U = U.copy()
        U[0, eta_comp, 0] += eta_unit * sigma * abs(S_UNIT[eta_comp])
        U[1, eta_comp, 0] -= eta_unit * sigma * abs(S_UNIT[eta_comp])
        return U

    def bo(B, w, tau):
        B = B.copy()
        B[0, 0, 0] += eta_base * tau
        B[1, 0, 0] -= eta_base * tau
        return B
    return build_case(name, src=SRC3, mode=2, waves=waves, unit_rows=[1.0, 1.0],
                      base_rows=[1.0, 1.0], inc_target=0.25, base_target=0.3, R=R, phi=phi,
                      Z=Z, atol_inc=TIGHT, rtol_inc=TIGHT, atol_base=TIGHT, rtol_base=TIGHT,
                      unit_override=uo, base_override=bo)


# ---------------------------------------------------------------------------
# Adapter
# ---------------------------------------------------------------------------
class AdapterUnresolved(Exception):
    pass


def provider_dict(mods, bessel=None, status='READY'):
    if bessel is None:
        made = mods['provider_0445'].create_jn_provider(
            library_policy='posix_find_library_m', expected_library_path=None,
            max_cache_entries=0)
        if made['status'] != 'READY':
            raise SystemExit('pinned J_n provider not READY: ' + str(made['finding']))
        return made
    return dict(status=status, bessel_jn=bessel, metadata=dict(provider='fixture double'),
                finding=None)


# canonical key -> accepted parameter names (case-sensitive exact match)
ALIASES = {
    'contraction': ('density_fourier', 'contraction', 'contraction_0445', 'density_contraction',
                    'nonzero_mode_density_fourier', 'source_contraction', 'fourier_contraction'),
    'provider_dict': ('jn_provider', 'provider', 'bessel_provider', 'jn_provider_result'),
    'provider_callable': ('bessel_jn', 'jn', 'bessel'),
    'result_0445': ('result_0445', 'contraction_result', 'density_fourier_result',
                    'deltaJ0_result', 'source_result'),
    'src_R': ('radius_m', 'source_radius_m', 'rho_radius_m'),
    'src_z': ('z_m', 'source_z_m', 'rho_z_m'),
    'src_w': ('weights_RdRdz_m3', 'source_weights_RdRdz_m3', 'RdRdz_m3', 'weights_m3'),
    'src_rho': ('rho_mode_kg_m3', 'rho_m_kg_m3', 'rho_m', 'rho_mode'),
    'mode': ('mode', 'm', 'azimuthal_mode'),
    'waves': ('k_physical_inverse_m', 'wavevectors', 'waves', 'k_physical'),
    'unit_packet': ('unit_response', 'unit_prepared', 'unit_packet'),
    'unit_array': ('weighted_unit_response', 'unit_weighted_responses', 'weighted_responses'),
    'base_packet': ('base_prepared', 'base_response', 'base_packet', 'f2_prepared'),
    'base_array': ('base_weighted_responses',),
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
    'atol_any': ('reality_atol',),
    'rtol_any': ('reality_rtol',),
    'wave_chunk': ('wave_chunk',),
    'position_chunk': ('position_chunk',),
    'include_log': ('include_log_difference', 'log_difference', 'finite_log_difference'),
    'provenance': ('provenance', 'supplied_provenance'),
}


def canonical_values(case, mods):
    pd = case.get('provider_override') or provider_dict(mods)
    contraction = case.get('contraction_override') or mods['contraction_0445'].nonzero_mode_density_fourier
    vals = dict(
        contraction=contraction, provider_dict=pd, provider_callable=pd['bessel_jn'],
        src_R=case['src_R'], src_z=case['src_z'], src_w=case['src_w'], src_rho=case['src_rho'],
        mode=case['mode'], waves=case['waves'],
        unit_packet=dict(wavevectors=case['waves'], weighted_responses=case['unit']),
        unit_array=case['unit'],
        base_packet=dict(wavevectors=case['waves'], weighted_responses=case['base']),
        base_array=case['base'],
        prepare_line=mods['line'].prepare_line, evaluate_line=mods['line'].evaluate_line,
        eval_R=case['eval_R'], eval_phi=case['eval_phi'], eval_Z=case['eval_Z'],
        c=case['c'], atol_base=case['atol_base'], rtol_base=case['rtol_base'],
        atol_inc=case['atol_inc'], rtol_inc=case['rtol_inc'],
        atol_any=min(case['atol_base'], case['atol_inc']),
        rtol_any=min(case['rtol_base'], case['rtol_inc']),
        wave_chunk=case['wave_chunk'], position_chunk=case['position_chunk'],
        include_log=case['include_log'], provenance=case['provenance'])
    return vals


def result_0445_for(case, vals):
    """Only for a dict-mode interface: the 0445 result the module would consume."""
    if 'result_0445_override' in case:
        return case['result_0445_override']
    pd = vals['provider_dict']
    if pd.get('status') != 'READY':
        return dict(status='INVALID_INPUT', complete=False, deltaJ0_J=None)
    return vals['contraction'](
        radius_m=case['src_R'], z_m=case['src_z'], weights_RdRdz_m3=case['src_w'],
        rho_mode_kg_m3=case['src_rho'], k_physical_inverse_m=case['waves'], c_m_s=case['c'],
        mode=case['mode'], bessel_jn=pd['bessel_jn'], wave_chunk=case['wave_chunk'],
        position_chunk=case['position_chunk'])


def default_make_kwargs(params, case, mods):
    vals = None
    out = {}
    for name, p in params.items():
        if p.kind not in (p.KEYWORD_ONLY, p.POSITIONAL_OR_KEYWORD):
            continue
        key = next((k for k, names in ALIASES.items() if name in names), None)
        if key is None:
            if p.default is not p.empty:
                continue
            raise AdapterUnresolved('parameter %r has no canonical mapping' % name)
        if vals is None:
            vals = canonical_values(case, mods)
        if key == 'eval_Z' and 'eval_Z_2d' in case.get('adapter_hints', ()):
            out[name] = case['eval_Z'][:, 0, :]
        elif key == 'result_0445':
            out[name] = result_0445_for(case, vals)
        else:
            out[name] = vals[key]
    return out


OUTPUT_PATHS = {
    'status': (('status',),),
    'complete': (('complete',),),
    'deltaJ0': (('deltaJ0_J',), ('deltaJ0',), ('source', 'deltaJ0_J')),
    'delta_prepared': (('delta_prepared', 'weighted_responses'), ('delta_prepared',),
                       ('increment_prepared', 'weighted_responses')),
    'delta_prepared_waves': (('delta_prepared', 'wavevectors'),),
    'base_fields': (('base_line', 'fields'), ('base', 'fields'), ('base_fields',)),
    'base_gradient': (('base_line', 'gradient'), ('base', 'gradient'), ('base_gradient',)),
    'base_hessian': (('base_line', 'hessian'), ('base', 'hessian'), ('base_hessian',)),
    'inc_fields': (('increment_line', 'fields'), ('increment', 'fields'), ('increment_fields',)),
    'inc_gradient': (('increment_line', 'gradient'), ('increment', 'gradient'),
                     ('increment_gradient',)),
    'inc_hessian': (('increment_line', 'hessian'), ('increment', 'hessian'),
                    ('increment_hessian',)),
    'nb': (('lapse', 'nb'), ('nb',)),
    'dn': (('lapse', 'dn'), ('dn',)),
    'Nb': (('lapse', 'Nb'), ('Nb',)),
    'dphi': (('linear', 'deltaPhi_m2_s2'), ('linear', 'deltaPhi'), ('linear_deltaPhi',)),
    'grad': (('linear', 'grad_deltaPhi_cartesian_m_s2'), ('linear', 'grad_deltaPhi_cartesian'),
             ('linear', 'grad_deltaPhi'), ('linear_grad_deltaPhi',)),
    'grad_cyl': (('linear', 'grad_deltaPhi_cylindrical_R_phi_z_m_s2'),),
    'logphi': (('log_difference', 'deltaPhi_m2_s2'), ('log_difference', 'deltaPhi'),
               ('log_deltaPhi',)),
    'loggrad': (('log_difference', 'grad_deltaPhi_cartesian_m_s2'),
                ('log_difference', 'grad_deltaPhi_cartesian'), ('log_grad_deltaPhi',)),
    'provenance': (('provenance',),),
    'retained': (('retained',),),
}


def _get_path(obj, path):
    for key in path:
        if not isinstance(obj, dict) or key not in obj:
            return None, False
        obj = obj[key]
    return obj, True


def default_normalize(result, case):
    out = {}
    if not isinstance(result, dict):
        raise AdapterUnresolved('result is not a dict: ' + type(result).__name__)
    for key, paths in OUTPUT_PATHS.items():
        out[key] = None
        for path in paths:
            val, ok = _get_path(result, path)
            if ok:
                out[key] = val
                out[key + '__path'] = '.'.join(path)
                break
    if out['status'] is None:
        raise AdapterUnresolved('no status key in result')
    return out


# ---------------------------------------------------------------------------
# Runner helpers
# ---------------------------------------------------------------------------
def grid_view(arr, case, tail_ndim):
    """Bring a module array to (nR, nphi, nz) + tail; None if impossible."""
    if arr is None:
        return None
    a = np.asarray(arr)
    nR, nP, nZ = case['eval_Z'].shape
    lead = a.shape[:a.ndim - tail_ndim] if tail_ndim else a.shape
    tail = a.shape[a.ndim - tail_ndim:] if tail_ndim else ()
    if lead == (nR, nP, nZ):
        return a
    if int(np.prod(lead)) == nR * nP * nZ and len(lead) == 1:
        return a.reshape((nR, nP, nZ) + tail)
    return None


def rel_err(got, exp):
    got = np.asarray(got)
    exp = np.asarray(exp)
    if got.shape != exp.shape:
        return None, 'shape %s != expected %s' % (got.shape, exp.shape)
    scale = float(np.max(np.abs(exp))) if exp.size else 0.0
    diff = np.abs(got - exp)
    if not np.all(np.isfinite(diff)):
        return math.inf, 'nonfinite difference'
    err = float(np.max(diff)) if diff.size else 0.0
    return (err / scale if scale > 0 else err), None


def check_value(checks, label, got, exp, rtol, tail_ndim=None, case=None):
    if got is None:
        checks.append(dict(check=label, ok=False, detail='MISSING in result'))
        return False
    if tail_ndim is not None:
        g = grid_view(got, case, tail_ndim)
        if g is None:
            checks.append(dict(check=label, ok=False,
                               detail='unexpected layout %s' % (np.asarray(got).shape,)))
            return False
        got = g
    err, why = rel_err(got, exp)
    ok = err is not None and err <= rtol
    checks.append(dict(check=label, ok=bool(ok), max_rel_err=err, rtol=rtol, detail=why))
    return ok


class Harness:
    def __init__(self, fn, mods, adapter):
        self.fn = fn
        self.mods = mods
        self.params = dict(inspect.signature(fn).parameters)
        self.make_kwargs = getattr(adapter, 'make_kwargs', None) if adapter else None
        self.normalize = getattr(adapter, 'normalize', None) if adapter else None
        self.calls = 0

    def has(self, canonical):
        return any(n in ALIASES[canonical] for n in self.params)

    def run(self, case, errstate='raise'):
        """-> (raw result or None, normalized or None, raised exception or None, seconds)."""
        if self.make_kwargs:
            kwargs = self.make_kwargs(self.params, case)
        else:
            kwargs = default_make_kwargs(self.params, case, self.mods)
        snapshot = {k: copy.deepcopy(v) for k, v in kwargs.items()
                    if isinstance(v, np.ndarray) or (isinstance(v, dict) and 'bessel_jn' not in v)}
        t0 = time.monotonic()
        raw = None
        exc = None
        self.calls += 1
        try:
            with np.errstate(all=errstate):
                raw = self.fn(**kwargs)
        except Exception as e:  # recorded; a raise is not a fail-closed dict
            exc = e
        dt = time.monotonic() - t0
        mutated = []
        for k, v in snapshot.items():
            if not _deep_equal(v, kwargs[k]):
                mutated.append(k)
        norm = None
        if raw is not None:
            norm = (self.normalize(raw, case) if self.normalize else default_normalize(raw, case))
        return raw, norm, exc, dt, mutated


def _deep_equal(a, b):
    if isinstance(a, np.ndarray):
        return isinstance(b, np.ndarray) and a.shape == b.shape and a.dtype == b.dtype and \
            bool(np.all((a == b) | (np.isnan(a) & np.isnan(b)) if a.dtype.kind in 'fc' else a == b))
    if isinstance(a, dict):
        return isinstance(b, dict) and a.keys() == b.keys() and all(_deep_equal(a[k], b[k]) for k in a)
    try:
        return bool(a == b)
    except Exception:
        return a is b


def is_complete(norm):
    return norm is not None and norm.get('status') == 'COMPLETE' and norm.get('complete') is True


def payload_absent(norm):
    """On rejection: no linear/log lapse and no delta_prepared exposed as a result."""
    if norm is None:
        return True
    return all(norm.get(k) is None for k in ('dphi', 'grad', 'logphi', 'loggrad', 'delta_prepared'))


def expect_complete_values(h, case, checks, *, lapse=True, log=None, jets=True):
    raw, norm, exc, dt, mutated = h.run(case)
    if exc is not None:
        checks.append(dict(check='call', ok=False, detail='raised %s: %s' % (type(exc).__name__, exc)))
        return None
    ok = is_complete(norm)
    checks.append(dict(check='status COMPLETE', ok=ok, detail=(None if ok else
                       '%s: %s' % (norm.get('status'), (raw or {}).get('reason')))))
    if not ok:
        return norm
    ex = case['expected']
    check_value(checks, 'deltaJ0 vs independent series', norm.get('deltaJ0'), ex['deltaJ0'], RTOL_VALUE)
    check_value(checks, 'delta_prepared = U*deltaJ0 (nk,10,1), signed order', norm.get('delta_prepared'),
                ex['delta_prepared'], RTOL_VALUE)
    dp = norm.get('delta_prepared')
    if dp is not None and np.asarray(dp).shape == ex['delta_prepared'].shape:
        got0 = np.asarray(dp)[:, 0, 0]
        nz = np.abs(ex['delta_prepared'][:, 0, 0]) > 0
        ratio = got0[nz] / ex['delta_prepared'][nz, 0, 0]
        checks.append(dict(check='factor diagnosis delta_prepared/expected (lapse column)', ok=bool(
            np.all(np.abs(ratio - 1) <= RTOL_VALUE)), ratio_min=complex(ratio[np.argmin(np.abs(ratio))]),
            ratio_max=complex(ratio[np.argmax(np.abs(ratio))]),
            suspects=_suspects(ratio, case['c'])))
        dw = norm.get('delta_prepared_waves')
        if dw is not None:
            checks.append(dict(check='delta_prepared wavevectors identical to input order',
                               ok=bool(np.array_equal(np.asarray(dw), case['waves']))))
        dj = norm.get('deltaJ0')
        if dj is not None:
            same = bool(np.array_equal(np.asarray(dp), case['unit'] * np.asarray(dj)[:, None, None]))
            checks.append(dict(check='delta_prepared bitwise == U * module deltaJ0[:,None,None] (once)',
                               ok=same))
    if jets:
        for key, tail in (('base_fields', 1), ('base_gradient', 2), ('base_hessian', 3),
                          ('inc_fields', 1), ('inc_gradient', 2), ('inc_hessian', 3)):
            check_value(checks, key + ' complex full-ten (all angles)', norm.get(key), ex[key],
                        RTOL_VALUE, tail, case)
    if lapse:
        for key, tail in (('nb', 0), ('dn', 0), ('Nb', 0)):
            if norm.get(key) is not None:
                check_value(checks, key, norm[key], ex[key], RTOL_VALUE, tail, case)
        check_value(checks, 'LINEAR dPhi = c^2 dn/Nb', norm.get('dphi'), ex['dphi'], RTOL_VALUE, 0, case)
        check_value(checks, 'LINEAR grad dPhi (Cartesian)', norm.get('grad'), ex['grad'], RTOL_VALUE, 1, case)
        g = grid_view(norm.get('dphi'), case, 0)
        if g is not None:
            dlog = rel_err(g, ex['logphi'])[0]
            checks.append(dict(check='linear dPhi is NOT the log variant', ok=bool(dlog > 1e-6),
                               rel_diff_to_log=dlog))
        if norm.get('grad_cyl') is not None:
            gc = grid_view(norm['grad_cyl'], case, 1)
            phi = case['eval_phi'][None, :, None]
            gx, gy, gz = ex['grad'][..., 0], ex['grad'][..., 1], ex['grad'][..., 2]
            cyl = np.stack((gx * np.cos(phi) + gy * np.sin(phi), -gx * np.sin(phi) + gy * np.cos(phi), gz), -1)
            check_value(checks, 'grad dPhi cylindrical (R,phi,z) from Cartesian', gc, cyl, RTOL_VALUE)
    if log is True:
        check_value(checks, 'LOG dPhi = c^2 log1p(dn/Nb) (separate label)', norm.get('logphi'),
                    ex['logphi'], RTOL_VALUE, 0, case)
        check_value(checks, 'LOG grad', norm.get('loggrad'), ex['loggrad'], RTOL_VALUE, 1, case)
    if log is False:
        checks.append(dict(check='no log difference when not requested',
                           ok=norm.get('logphi') is None and norm.get('loggrad') is None))
    if mutated:
        checks.append(dict(check='inputs not mutated', ok=False, detail=mutated))
    return norm


def _suspects(ratio, c):
    med = complex(np.median(ratio.real) + 1j * np.median(ratio.imag))
    cands = {'1 (correct)': 1, '-1 (extra minus)': -1, 'c^2': c * c, '1/c^2': 1 / (c * c),
             '-c^2': -c * c, '2pi': 2 * math.pi, '1/(2pi)': 1 / (2 * math.pi),
             '(2pi)^-3': (2 * math.pi) ** -3, 'i': 1j, '-i': -1j, 'conj-like': None}
    out = []
    for name, v in cands.items():
        if v is not None and abs(med - v) <= 1e-6 * max(1, abs(v)):
            out.append(name)
    return out or ['ratio %r matches no simple factor' % (med,)]


def expect_reject(h, case, checks, label, errstate='raise'):
    raw, norm, exc, dt, mutated = h.run(case, errstate=errstate)
    if exc is not None:
        checks.append(dict(check=label + ': rejected', ok=True,
                           detail='raised %s (rejected, but not a fail-closed dict)' % type(exc).__name__))
        checks.append(dict(check=label + ': fail-closed dict (lane convention)', ok=False,
                           detail='%s: %s' % (type(exc).__name__, exc)))
        return None
    rejected = not is_complete(norm)
    checks.append(dict(check=label + ': rejected (status not COMPLETE)', ok=rejected,
                       status=None if norm is None else norm.get('status'),
                       reason=(raw or {}).get('reason'), stage=(raw or {}).get('failure_stage')))
    checks.append(dict(check=label + ': no lapse/delta_prepared payload exposed', ok=payload_absent(norm)))
    return norm


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
def test_a(h):
    checks = []
    one = case_one_wave()
    # explicit scalar closed form for the one-wave/one-position source
    k = one['waves'][0]
    kp, al = math.hypot(k[0], k[1]), math.atan2(k[1], k[0])
    rq, Rq, zq, wq, m, c = SRC1['rho'][0], SRC1['R'][0], SRC1['z'][0], SRC1['w'][0], 1, C_TEST
    closed = -(c * c) * 2 * math.pi * (-1j) * wq * bessel_ref(m, kp * Rq) * cmath.exp(-1j * k[2] * zq) * \
        (rq * cmath.exp(1j * al) + rq.conjugate() * cmath.exp(-1j * al))
    checks.append(dict(check='fixture self-check: one-wave scalar closed form == generic sum',
                       ok=abs(closed - one['expected']['deltaJ0'][0]) <= 1e-14 * abs(closed)))
    P = one['points']
    e = np.exp(1j * (P[..., 0] * k[0] + P[..., 1] * k[1] + P[..., 2] * k[2]))
    inc0 = one['unit'][0, 0, 0] * closed * e
    checks.append(dict(check='fixture self-check: one-wave field = U0 dJ e^{ik.x}',
                       ok=rel_err(inc0, one['expected']['inc_fields'][..., 0])[0] <= 1e-13))
    sub = []
    expect_complete_values(h, one, sub)
    checks += [dict(c, check='one-wave: ' + c['check']) for c in sub]
    pc = case_paired()
    ex = pc['expected']
    herm = []
    nk = len(pc['waves'])
    for i in range(nk):
        j = next(j for j in range(nk) if np.array_equal(pc['waves'][j], -pc['waves'][i]))
        herm.append(abs(ex['deltaJ0'][j] - np.conj(ex['deltaJ0'][i])))
    checks.append(dict(check='fixture self-check: paired deltaJ0(-k) == conj deltaJ0(k)',
                       ok=max(herm) <= 1e-13 * np.max(np.abs(ex['deltaJ0']))))
    checks.append(dict(check='fixture self-check: paired fields real',
                       ok=float(np.max(np.abs(ex['inc_fields'].imag))) <= 1e-14 and
                       float(np.max(np.abs(ex['base_fields'].imag))) <= 1e-14))
    checks.append(dict(check='fixture self-check: k_perp = 0 pair has deltaJ0 == 0 exactly',
                       ok=bool(np.all(ex['deltaJ0'][np.hypot(pc['waves'][:, 0], pc['waves'][:, 1]) == 0] == 0))))
    sub = []
    expect_complete_values(h, pc, sub, log=False)
    checks += [dict(c, check='paired m=3: ' + c['check']) for c in sub]
    return checks


def test_b(h):
    checks = []
    pc = case_paired()
    raw, norm, exc, dt, _ = h.run(pc)
    if exc is not None or not is_complete(norm):
        return [dict(check='paired call COMPLETE', ok=False, detail=str(exc or (raw or {}).get('reason')))]
    ex = pc['expected']
    inc0 = ex['delta_prepared'][:, 0, 0]
    base0 = pc['base'][:, 0, 0]
    fun = lambda x, y, z: dphi_closed(pc['c'], pc['waves'], inc0, base0, x, y, z)
    P = pc['points']
    fd = np.empty(P.shape)
    for idx in np.ndindex(P.shape[:3]):
        fd[idx] = fd_gradient(fun, tuple(P[idx]), 1e-3)
    err_self = rel_err(ex['grad'], fd)[0]
    checks.append(dict(check='fixture self-check: analytic linear grad vs FD of closed-form dPhi',
                       ok=err_self <= RTOL_FD, max_rel_err=err_self))
    check_value(checks, 'module LINEAR grad dPhi vs FD of closed-form dPhi (all 96 points)',
                norm.get('grad'), fd, RTOL_FD, 1, pc)
    vals = np.array([fun(*P[idx]) for idx in np.ndindex(P.shape[:3])]).reshape(P.shape[:3])
    check_value(checks, 'module LINEAR dPhi vs closed-form dPhi(x,y,z)', norm.get('dphi'), vals,
                RTOL_VALUE, 0, pc)
    # the module's own dPhi differenced along R and z (stencil roster), compared with its gradient
    hstep = 2e-3
    R0, z0 = 2.1, 0.35
    Rs = [R0 + s * hstep for s in (-2, -1, 0, 1, 2)]
    Zs = [[z0 + s * hstep for s in (-3, -2, -1, 0, 1, 2, 3)] for _ in Rs]
    st = case_paired(name='paired_stencil', R=Rs, Z=Zs)
    raw2, n2, exc2, _, _ = h.run(st)
    if exc2 is not None or not is_complete(n2):
        checks.append(dict(check='stencil call COMPLETE', ok=False, detail=str(exc2 or (raw2 or {}).get('reason'))))
        return checks
    f = grid_view(n2.get('dphi'), st, 0)
    g = grid_view(n2.get('grad'), st, 1)
    if f is None or g is None:
        checks.append(dict(check='stencil outputs present', ok=False))
        return checks
    phi = st['eval_phi']
    dR = (-f[4, :, 3] + 8 * f[3, :, 3] - 8 * f[1, :, 3] + f[0, :, 3]) / (12 * hstep)
    dZ = (-f[2, :, 5] + 8 * f[2, :, 4] - 8 * f[2, :, 2] + f[2, :, 1]) / (12 * hstep)
    gR = g[2, :, 3, 0] * np.cos(phi) + g[2, :, 3, 1] * np.sin(phi)
    gZ = g[2, :, 3, 2]
    scale = float(np.max(np.abs(g[2, :, 3])))
    eR = float(np.max(np.abs(gR - dR))) / scale
    eZ = float(np.max(np.abs(gZ - dZ))) / scale
    checks.append(dict(check='module dPhi differenced along R == module radial grad (16 angles)',
                       ok=eR <= RTOL_FD, max_rel_err=eR))
    checks.append(dict(check='module dPhi differenced along z == module vertical grad (16 angles)',
                       ok=eZ <= RTOL_FD, max_rel_err=eZ))
    return checks


def test_c(h):
    checks = []
    c1 = case_paired(name='Nb_nonpositive', base_target=1.6, base_sign=-1.0)
    nbmin = float(np.min(c1['expected']['Nb']))
    checks.append(dict(check='fixture self-check: some Nb <= 0 and some > 0', ok=nbmin < 0 < float(
        np.max(c1['expected']['Nb'])), min_Nb=nbmin, points_Nb_le_0=int(np.sum(c1['expected']['Nb'] <= 0))))
    expect_reject(h, c1, checks, 'Nb <= 0 (linear)')
    c1b = case_paired(name='Nb_nonpositive_log', base_target=1.6, include_log=True, base_sign=-1.0)
    if h.has('include_log'):
        expect_reject(h, c1b, checks, 'Nb <= 0 (log requested)')
    c2 = case_paired(name='Nb_plus_dn_nonpositive', inc_target=2.0, base_target=0.2)
    ex = c2['expected']
    bad = (ex['Nb'] + ex['dn']) <= 0
    checks.append(dict(check='fixture self-check: Nb > 0 everywhere, Nb + dn <= 0 somewhere',
                       ok=bool(np.all(ex['Nb'] > 0) and np.any(bad)), points=int(np.sum(bad))))
    sub = []
    expect_complete_values(h, c2, sub, log=False)
    checks += [dict(s, check='Nb+dn<=0, log NOT requested -> linear still exact: ' + s['check']) for s in sub]
    if h.has('include_log'):
        c2l = case_paired(name='Nb_plus_dn_nonpositive_log', inc_target=2.0, base_target=0.2,
                          include_log=True)
        raw, norm, exc, dt, _ = h.run(c2l)
        if exc is not None:
            checks.append(dict(check='Nb+dn<=0 with log: fail-closed dict', ok=False, detail=repr(exc)))
        elif is_complete(norm):
            lp = grid_view(norm.get('logphi'), c2l, 0)
            finite_bad = lp is not None and bool(np.any(np.isfinite(lp[bad])))
            checks.append(dict(check='Nb+dn<=0 with log: no finite log value at offending points',
                               ok=not finite_bad))
            check_value(checks, 'Nb+dn<=0 with log: linear unaffected', norm.get('dphi'), ex['dphi'],
                        RTOL_VALUE, 0, c2l)
        else:
            checks.append(dict(check='Nb+dn<=0 with log requested: rejected (fail closed)', ok=True,
                               status=norm.get('status'), reason=(raw or {}).get('reason')))
            checks.append(dict(check='Nb+dn<=0 with log: no log/linear payload exposed as result',
                               ok=payload_absent(norm)))
        c3 = case_paired(name='log_ok', include_log=True)
        sub = []
        expect_complete_values(h, c3, sub, log=True)
        checks += [dict(s, check='log requested, Nb+dn>0: ' + s['check']) for s in sub]
    else:
        checks.append(dict(check='log difference control parameter', ok=True, na=True,
                           detail='module exposes no include_log parameter; log checks not applicable'))
    return checks


def _failing_provider(mods, fail_on_call):
    real = provider_dict(mods)['bessel_jn']
    state = dict(n=0)

    def bessel(n, x):
        state['n'] += 1
        if state['n'] >= fail_on_call:
            raise RuntimeError('fixture: provider fault injected at call %d' % state['n'])
        return real(n, x)
    return bessel


def test_d(h, mods):
    checks = []
    contraction = mods['contraction_0445'].nonzero_mode_density_fourier
    base = case_paired(wave_chunk=1, position_chunk=8)
    callable_mode = h.has('contraction')
    dict_mode = h.has('result_0445')
    if not (callable_mode or dict_mode):
        return [dict(check='0445 input parameter found', ok=False, detail='ADAPTER_UNRESOLVED')]
    # d1: real 0445 FAILED_CLOSED with retained partial chunk
    c = dict(base)
    bad = provider_dict(mods, _failing_provider(mods, 3))
    if callable_mode:
        c['provider_override'] = bad
    else:
        c['result_0445_override'] = contraction(
            radius_m=c['src_R'], z_m=c['src_z'], weights_RdRdz_m3=c['src_w'],
            rho_mode_kg_m3=c['src_rho'], k_physical_inverse_m=c['waves'], c_m_s=c['c'],
            mode=c['mode'], bessel_jn=bad['bessel_jn'], wave_chunk=1, position_chunk=8)
    expect_reject(h, c, checks, 'd1 real 0445 FAILED_CLOSED (partial chunks retained)')
    full = contraction(radius_m=base['src_R'], z_m=base['src_z'], weights_RdRdz_m3=base['src_w'],
                       rho_mode_kg_m3=base['src_rho'], k_physical_inverse_m=base['waves'],
                       c_m_s=base['c'], mode=base['mode'],
                       bessel_jn=provider_dict(mods)['bessel_jn'], wave_chunk=1, position_chunk=8)
    nan_row = full['deltaJ0_J'].copy()
    nan_row[2] = complex(math.nan, math.nan)
    forged = {
        'd2 status FAILED_CLOSED but full deltaJ0_J present': dict(full, status='FAILED_CLOSED', complete=False),
        'd3 status COMPLETE but complete False': dict(full, complete=False),
        'd4 COMPLETE with a NaN row (partial disguised)': dict(full, deltaJ0_J=nan_row),
        'd5 COMPLETE, deltaJ0_J None, retained present': dict(full, deltaJ0_J=None,
                                                              retained_deltaJ0_J=full['deltaJ0_J']),
        'd6 COMPLETE with nk-1 rows': dict(full, deltaJ0_J=full['deltaJ0_J'][:-1].copy()),
        'd7 status INTERRUPTED': dict(full, status='INTERRUPTED', complete=False),
    }
    for label, doc in forged.items():
        c = dict(base)
        if callable_mode:
            c['contraction_override'] = (lambda d: (lambda **kw: copy.deepcopy(d)))(doc)
        else:
            c['result_0445_override'] = copy.deepcopy(doc)
        expect_reject(h, c, checks, label)
    c = dict(base)
    c['src_rho'] = base['src_rho'].real.copy()
    expect_reject(h, c, checks, 'd11 0445 INVALID_INPUT (real-dtype rho_m)')
    other = contraction(radius_m=base['src_R'], z_m=base['src_z'], weights_RdRdz_m3=base['src_w'],
                        rho_mode_kg_m3=base['src_rho'], k_physical_inverse_m=base['waves'],
                        c_m_s=base['c'], mode=base['mode'] + 1,
                        bessel_jn=provider_dict(mods)['bessel_jn'], wave_chunk=1, position_chunk=8)
    c = dict(base)
    if callable_mode:
        c['contraction_override'] = (lambda d: (lambda **kw: copy.deepcopy(d)))(other)
    else:
        c['result_0445_override'] = copy.deepcopy(other)
    sub = []
    expect_reject(h, c, sub, 'd10 COMPLETE 0445 result for a different mode (hardening)')
    checks += [dict(s_, advisory=True) for s_ in sub]
    if h.has('provider_dict'):
        c = dict(base)
        c['provider_override'] = dict(status='LIBM_NOT_DISCOVERABLE', bessel_jn=None, metadata={},
                                      finding='fixture')
        expect_reject(h, c, checks, 'd8 provider status not READY')
        c = dict(base)
        c['provider_override'] = provider_dict(mods, provider_dict(mods)['bessel_jn'], status='PENDING')
        expect_reject(h, c, checks, 'd9 provider callable present but status PENDING')
    # control: same configuration with a healthy provider completes
    sub = []
    expect_complete_values(h, base, sub, jets=False)
    checks += [dict(s, check='control (healthy 0445, chunk 1x8): ' + s['check']) for s in sub]
    return checks


def test_e(h):
    checks = []
    e1 = case_one_wave(tight_inc=True, zero_base=True)
    imag = float(np.max(np.abs(e1['expected']['inc_fields'].imag)))
    checks.append(dict(check='e1 fixture: increment imaginary part far above tolerance', ok=imag > 1e3 * TIGHT,
                       max_abs_imag=imag))
    expect_reject(h, e1, checks, 'e1 one-wave increment, tight tolerance')
    e1c = case_one_wave(tight_inc=False, zero_base=True)
    sub = []
    expect_complete_values(h, e1c, sub)
    checks += [dict(s, check='e1 control (permissive tolerance): ' + s['check']) for s in sub]
    # e2: imaginary remainder odd in x -> exact zero mean over the 16-angle roster
    e2 = case_xpair('xpair_odd_imag', eta_unit=0.3, eta_comp=0)
    im = e2['expected']['inc_fields'][..., 0].imag
    mean_abs = float(np.max(np.abs(np.mean(im, axis=1))))
    checks.append(dict(check='e2 fixture: |Im dn| large pointwise, angular mean ~ 0',
                       ok=float(np.max(np.abs(im))) > 1e-3 and mean_abs <= 1e-15,
                       max_abs_imag=float(np.max(np.abs(im))), max_abs_angular_mean=mean_abs))
    expect_reject(h, e2, checks, 'e2 imaginary remainder averaging to zero over angles (not averaged)')
    sub = []
    expect_complete_values(h, case_xpair('xpair_control'), sub)
    checks += [dict(s, check='e2 control (eta = 0): ' + s['check']) for s in sub]
    # e3: imaginary only in non-lapse component 7
    e3 = case_xpair('xpair_comp7_imag', eta_unit=0.3, eta_comp=7)
    checks.append(dict(check='e3 fixture: lapse component real, component 7 not', ok=float(np.max(np.abs(
        e3['expected']['inc_fields'][..., 0].imag))) <= 1e-15 and float(np.max(np.abs(
            e3['expected']['inc_fields'][..., 7].imag))) > 1e-3))
    expect_reject(h, e3, checks, 'e3 imaginary only in field component 7 (full-ten check)')
    # e4: imaginary only in the base response
    e4 = case_xpair('xpair_base_imag', eta_base=0.3)
    checks.append(dict(check='e4 fixture: increment real, base lapse imaginary',
                       ok=float(np.max(np.abs(e4['expected']['inc_fields'].imag))) <= 1e-15 and
                       float(np.max(np.abs(e4['expected']['base_fields'][..., 0].imag))) > 1e-3))
    expect_reject(h, e4, checks, 'e4 imaginary only in base')
    return checks


def _dft_slots(arr):
    """16-point DFT over the angle axis (axis 1), numpy forward convention / N."""
    return np.fft.fft(arr, axis=1) / arr.shape[1]


def test_f(h):
    checks = []
    pc = case_paired(name='paired_angles')
    raw, norm, exc, dt, _ = h.run(pc)
    if exc is None and is_complete(norm):
        for key, tail in (('dphi', 0), ('grad', 1), ('inc_fields', 1)):
            g = norm.get(key)
            shape = None if g is None else np.asarray(g).shape
            checks.append(dict(check='%s angle axis has all 16 supplied angles' % key,
                               ok=g is not None and grid_view(g, pc, tail) is not None and
                               grid_view(g, pc, tail).shape[1] == NPHI, shape=shape))
    else:
        checks.append(dict(check='paired call COMPLETE', ok=False))
    off = case_paired(name='offset_angles_per_angle_z', phi_offset=0.13, z_per_angle=0.011)
    sub = []
    expect_complete_values(h, off, sub)
    checks += [dict(s, check='offset angles (+0.13 rad) and per-angle heights: ' + s['check']) for s in sub]
    iso = case_anisotropic(0.0)
    ani = case_anisotropic(0.6)
    s_iso = _dft_slots(iso['expected']['dn'])
    s_ani = _dft_slots(ani['expected']['dn'])
    peak_iso = float(np.max(np.abs(s_iso)))
    checks.append(dict(check='fixture self-check: isotropic ring keeps m=1 (slots 3,13 ~ 0)',
                       ok=float(np.max(np.abs(s_iso[:, [3, 13]]))) <= 1e-13 * peak_iso,
                       slot3_rel=float(np.max(np.abs(s_iso[:, [3, 13]]))) / peak_iso))
    frac = float(np.max(np.abs(s_ani[:, [3, 13]]))) / float(np.max(np.abs(s_ani)))
    checks.append(dict(check='fixture self-check: anisotropic response moves m=1 into slots 3,13',
                       ok=frac > 0.05, slot3_fraction=frac))
    sub = []
    n2 = expect_complete_values(h, ani, sub)
    checks += [dict(s, check='anisotropic mixing pointwise: ' + s['check']) for s in sub]
    if n2 is not None and is_complete(n2):
        dn = n2.get('dn')
        if dn is None and n2.get('inc_fields') is not None:
            dn = grid_view(n2['inc_fields'], ani, 1)[..., 0].real
        dn = grid_view(dn, ani, 0)
        if dn is not None:
            check_value(checks, 'anisotropic: all 16 DFT slots of module dn preserved (incl. 3,13)',
                        _dft_slots(dn), s_ani, RTOL_VALUE)
        dphi = grid_view(n2.get('dphi'), ani, 0)
        if dphi is not None:
            check_value(checks, 'anisotropic: all 16 DFT slots of module dPhi preserved',
                        _dft_slots(dphi), _dft_slots(ani['expected']['dphi']), RTOL_VALUE)
    return checks


def case_fpe():
    """c = 1e151 (c^2 = 1e302 finite) and |k| ~ 1e10: c^2 * grad dn overflows float64."""
    waves = paired([[7e9, 3e9, 5e9], [-2e9, 6e9, 1e9]])
    R, phi, Z = roster()
    c = build_case('fpe', src=SRC3, mode=1, waves=waves, unit_rows=[1.0] * 4, base_rows=[1.0] * 4,
                   inc_target=None, base_target=0.2, R=R, phi=phi, Z=Z, atol_inc=LOOSE,
                   rtol_inc=LOOSE, atol_base=LOOSE, rtol_base=LOOSE, c=1e151, expect=False)
    return c


def test_g(h, mods):
    checks = []
    c = case_fpe()
    pd = provider_dict(mods)
    res = mods['contraction_0445'].nonzero_mode_density_fourier(
        radius_m=c['src_R'], z_m=c['src_z'], weights_RdRdz_m3=c['src_w'], rho_mode_kg_m3=c['src_rho'],
        k_physical_inverse_m=c['waves'], c_m_s=c['c'], mode=1, bessel_jn=pd['bessel_jn'],
        wave_chunk=2, position_chunk=2)
    if res['status'] != 'COMPLETE':
        return [dict(check='fpe fixture 0445 COMPLETE', ok=False, detail=res.get('reason'))]
    dJ = res['deltaJ0_J']
    sigma = scale_to(c['waves'], dJ, c['points'], 0.3)
    c['unit'] = (sigma * S_UNIT[None, :] * np.ones(len(dJ))[:, None])[:, :, None].astype(complex)
    checks.append(dict(check='fpe fixture: unit response finite and normal', ok=bool(
        np.all(np.isfinite(c['unit'])) and np.min(np.abs(c['unit'])) > 2.3e-308), sigma=sigma))
    for mode in ('raise', 'ignore'):
        raw, norm, exc, dt, _ = h.run(c, errstate=mode)
        if exc is not None:
            checks.append(dict(check='errstate=%s: fail-closed dict (not raised)' % mode, ok=False,
                               detail='%s: %s' % (type(exc).__name__, exc)))
            continue
        checks.append(dict(check='errstate=%s: rejected' % mode, ok=not is_complete(norm),
                           status=norm.get('status'), stage=raw.get('failure_stage'),
                           exception_type=raw.get('exception_type'), reason=raw.get('reason')))
        checks.append(dict(check='errstate=%s: no lapse payload exposed' % mode, ok=payload_absent(norm)))
        ret = norm.get('retained')
        kept = sorted(k for k, v in ret.items() if v is not None) if isinstance(ret, dict) else None
        checks.append(dict(check='errstate=%s: retention reported (advisory)' % mode,
                           ok=bool(kept), advisory=True, retained_keys=kept))
    return checks


def test_h(h):
    checks = []
    a = case_paired(name='chunk_a', wave_chunk=1, position_chunk=1)
    b = case_paired(name='chunk_b', wave_chunk=5, position_chunk=3)
    outs = []
    for c in (a, b):
        raw, norm, exc, dt, _ = h.run(c)
        if exc is not None or not is_complete(norm):
            return [dict(check='chunk call COMPLETE', ok=False)]
        outs.append(norm)
    for key in ('deltaJ0', 'delta_prepared', 'inc_fields', 'dphi', 'grad'):
        if outs[0].get(key) is None:
            continue
        err = rel_err(np.asarray(outs[0][key]), np.asarray(outs[1][key]))[0]
        checks.append(dict(check='chunks (1,1) vs (5,3): %s' % key, ok=err is not None and err <= RTOL_CHUNK,
                           max_rel_diff=err))
    return checks


FORBIDDEN_ATTRS = {'dot', 'matmul', 'tensordot', 'vdot', 'inner', 'linalg', 'errstate', 'seterr',
                   'load', 'loadtxt', 'save', 'savez', 'fromfile', 'tofile', 'filterwarnings',
                   'simplefilter', 'catch_warnings', 'nan_to_num', 'clip', 'real_if_close'}
FORBIDDEN_NAMES = {'open', 'exec', 'eval', '__import__'}


def test_i(path, import_output):
    src = open(path, 'rb').read().decode('utf-8')
    tree = ast.parse(src)
    imports = set()
    bad = []
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
    return [dict(check='imports numpy + stdlib only', ok=not nonstd, imports=sorted(i for i in imports if i),
                 advisory=True, nonstd=nonstd),
            dict(check='no BLAS/IO/warning-suppression/clipping tokens', ok=not bad, advisory=True, hits=bad),
            dict(check='module top level: definitions/assignments only', ok=not top, advisory=True,
                 other_statements=top),
            dict(check='import printed nothing', ok=import_output == '', advisory=True,
                 output=import_output[:200])]


def test_j(h):
    checks = []
    pc = case_paired(name='provenance_echo')
    raw, norm, exc, dt, mutated = h.run(pc)
    if exc is not None or not is_complete(norm):
        return [dict(check='call COMPLETE', ok=False)]
    checks.append(dict(check='supplied provenance echoed unchanged', ok=_deep_equal(norm.get('provenance'),
                       pc['provenance']), advisory=True))
    checks.append(dict(check='caller arrays/packets unchanged after call', ok=not mutated, advisory=True,
                       mutated=mutated))
    inc = grid_view(norm.get('inc_fields'), pc, 1)
    if inc is not None:
        checks.append(dict(check='increment uses zero boundary (fields == pure wave sum)',
                           ok=rel_err(inc, pc['expected']['inc_fields'])[0] <= RTOL_VALUE, advisory=True))
    return checks


TESTS = 'abcdefghij'


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--module', required=True)
    ap.add_argument('--function', required=True)
    ap.add_argument('--outdir', required=True)
    ap.add_argument('--adapter', default=None)
    ap.add_argument('--only', default=TESTS)
    a = ap.parse_args()
    t0 = time.monotonic()
    mods, pins = load_pinned()
    msha = sha256_file(a.module)
    print('MODULE %s sha256 %s' % (a.module, msha), flush=True)
    print('FIXTURE %s sha256 %s' % (os.path.abspath(__file__), sha256_file(os.path.abspath(__file__))),
          flush=True)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
        module = load_path(a.module, 'unt0449fx_target')
    import_output = buf.getvalue()
    fn = getattr(module, a.function)
    adapter = load_path(a.adapter, 'unt0449fx_adapter') if a.adapter else None
    h = Harness(fn, mods, adapter)
    report = dict(module=a.module, module_sha256=msha, function=a.function,
                  fixture=os.path.abspath(__file__), fixture_sha256=sha256_file(os.path.abspath(__file__)),
                  pins=pins, interpreter=sys.executable, python=sys.version.split()[0],
                  numpy=np.__version__,
                  blas_env={k: os.environ.get(k) for k in ('VECLIB_MAXIMUM_THREADS', 'OPENBLAS_NUM_THREADS',
                                                          'OMP_NUM_THREADS')},
                  import_output=import_output, signature=str(inspect.signature(fn)), tests={})
    runners = dict(a=lambda: test_a(h), b=lambda: test_b(h), c=lambda: test_c(h),
                   d=lambda: test_d(h, mods), e=lambda: test_e(h), f=lambda: test_f(h),
                   g=lambda: test_g(h, mods), h=lambda: test_h(h), i=lambda: test_i(a.module, import_output),
                   j=lambda: test_j(h))
    binding = set('abcdefg')
    for key in a.only.split(',') if ',' in a.only else a.only:
        ts = time.monotonic()
        try:
            checks = runners[key]()
            verdict = 'PASS' if all(c['ok'] for c in checks if not c.get('advisory')) else 'FAIL'
        except AdapterUnresolved as exc:
            checks, verdict = [dict(check='adapter', ok=False, detail=str(exc))], 'ADAPTER_UNRESOLVED'
        except Exception as exc:
            checks = [dict(check='harness', ok=False, detail=traceback.format_exc())]
            verdict = 'ERROR'
        report['tests'][key] = dict(verdict=verdict, binding=key in binding, seconds=time.monotonic() - ts,
                                    checks=checks)
        nfail = sum(1 for c in checks if not c['ok'])
        print('TEST %s %-18s %s  (%d checks, %d not ok%s)' % (
            key, '[binding]' if key in binding else '[advisory]', verdict, len(checks), nfail,
            ', advisory items included' if key not in binding or any(c.get('advisory') for c in checks) else ''),
            flush=True)
        for c in checks:
            if not c['ok']:
                print('   not ok: %s %s' % (c['check'], {k: v for k, v in c.items() if k not in ('check', 'ok')}),
                      flush=True)
    report['calls'] = h.calls
    report['seconds'] = time.monotonic() - t0
    report['overall_binding'] = 'PASS' if all(report['tests'][k]['verdict'] == 'PASS'
                                              for k in report['tests'] if k in binding) else 'NOT_PASS'
    os.makedirs(a.outdir, exist_ok=True)
    out = os.path.join(a.outdir, 'fixtures_0449_result_%s.json' % msha[:16])
    with open(out, 'w') as handle:
        json.dump(report, handle, indent=1, default=_json_default)
    print('OVERALL_BINDING %s  calls=%d  %.2fs  report %s sha256 %s' % (
        report['overall_binding'], h.calls, report['seconds'], out, sha256_file(out)), flush=True)
    return 0 if report['overall_binding'] == 'PASS' else 1


def _json_default(o):
    if isinstance(o, complex):
        return [o.real, o.imag]
    if isinstance(o, np.generic):
        return o.item() if not isinstance(o, np.complexfloating) else [float(o.real), float(o.imag)]
    if isinstance(o, np.ndarray):
        return dict(ndarray_shape=list(o.shape), dtype=str(o.dtype))
    return repr(o)


if __name__ == '__main__':
    sys.exit(main())
