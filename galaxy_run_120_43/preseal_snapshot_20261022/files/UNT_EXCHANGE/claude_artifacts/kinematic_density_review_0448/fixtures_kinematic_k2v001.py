#!/usr/bin/env python3
"""K2 implementation-fixture harness, dispatch 0448 (Claude4 independent review lane, local helper K2).

Contract under test (root KINEMATIC_DENSITY_COMPARISON_CHOICE_V001.json,
SHA256 9e4c070e88bf431cac9e001958016f9ca022f8cdef2c0c4f039fb7cd1128e14d):
    Gkin = -rho[:,None]*divU - rho_R[:,None]*U_R - rho_z[:,None]*U_z
delta_rho = -div(rho xi), xi = U y, divU = partial_R UR + UR/R + i*m*UP/R + partial_z UZ
(azimuthal dependence exp(+i m phi)); no separate phi term may be added a second time.

The target is loaded by FILE PATH with importlib (never a package import); bytecode writing is off.
Modes
  --reference-run                target = kinematic_reference in reference_kinematic_k2v001.py (this
                                 directory); A2 baseline = vectorized contract literal; A5 mutants run.
  --module PATH --func NAME      target = NAME in file PATH; A2 baseline = the K2 loop reference; A4 scored.
  --interpreters PY1,PY2         re-run this harness under each interpreter (-I -B, single-thread env)
                                 and merge both runs into --out (children write JSON to stdout).
  --source-of-copy PATH          record sha256 and byte identity of the original that the target copies.
  --out JSON | -                 results file ('-' = stdout).
Groups: A1 analytic -div(rho xi) on nonconstant densities (incl. EOS-supplied gradients),
A2 reference comparison, A3 properties, A4 malformed-input probes, A5 mutation sensitivity.
Tiny analytic inputs only; no project data or project modules. Exit 0 iff every scored item passes.
"""
import sys
sys.dont_write_bytecode = True
if sys.version_info < (3, 12):
    sys.path.append('/Users/bgm/Library/Python/3.9/lib/python/site-packages')
import argparse
import contextlib
import functools
import hashlib
import importlib.util
import inspect
import json
import os
import platform
import subprocess
import warnings

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REF_PATH = os.path.join(HERE, 'reference_kinematic_k2v001.py')
REF_FUNC = 'kinematic_reference'
CONTRACT_PATH = ('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/'
                 'FIRST_CONSTRUCTION_REVIEW_2026-10-13/CODEX1/KINEMATIC_DENSITY_COMPARISON_CHOICE_V001.json')
CONTRACT_SHA256 = '9e4c070e88bf431cac9e001958016f9ca022f8cdef2c0c4f039fb7cd1128e14d'
PARAMS = ('rho', 'rho_R', 'rho_z', 'U_R', 'U_z', 'divU')
VECS = ('rho', 'rho_R', 'rho_z')
MAPS = ('U_R', 'U_z', 'divU')
C128 = np.complex128
EPS = float(np.finfo(np.float64).eps)
RTOL_A1 = 1e-12   # analytic product route vs target, relative to summed term magnitudes
RTOL_A2 = 1e-14   # target vs baseline, relative to |rho||divU|+|rho_R||U_R|+|rho_z||U_z|
RTOL_FD = 1e-8    # finite-difference cross-checks of the analytic fixtures (global relative)
CONTEXT = {'R': None, 'phi_part': None}   # read ONLY by R/phi-dependent mutants (A5)


# ------------------------------------------------------------------ utilities
def sha256_file(path):
    with open(path, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def load_function(path, name, tag):
    path = os.path.abspath(path)
    modname = 'k2v001_loaded_' + tag
    spec = importlib.util.spec_from_file_location(modname, path)
    if spec is None or spec.loader is None:
        raise ImportError('cannot create import spec for ' + path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[modname] = mod
    with contextlib.redirect_stdout(sys.stderr):
        spec.loader.exec_module(mod)
    return getattr(mod, name)


def J(x):
    """JSON-safe conversion (nan/inf become strings, complex becomes [re, im])."""
    if isinstance(x, dict):
        return dict((str(k), J(v)) for k, v in x.items())
    if isinstance(x, (list, tuple)):
        return [J(v) for v in x]
    if isinstance(x, (bool, np.bool_)):
        return bool(x)
    if isinstance(x, (int, np.integer)):
        return int(x)
    if isinstance(x, (float, np.floating)):
        v = float(x)
        if v != v:
            return 'nan'
        if v == float('inf'):
            return 'inf'
        if v == float('-inf'):
            return '-inf'
        return v
    if isinstance(x, (complex, np.complexfloating)):
        return [J(x.real), J(x.imag)]
    if isinstance(x, np.ndarray):
        return J(x.tolist())
    if x is None or isinstance(x, str):
        return x
    return repr(x)


def exc_desc(e):
    return {'type': type(e).__name__, 'message': str(e)[:500]}


def invoke(target, kwargs=None, args=()):
    kwargs = {} if kwargs is None else kwargs
    before = np.geterr()
    with warnings.catch_warnings(record=True) as wl:
        warnings.simplefilter('always')
        try:
            with contextlib.redirect_stdout(sys.stderr):
                out = target(*args, **kwargs)
            exc = None
        except KeyboardInterrupt:
            raise
        except BaseException as e:  # record every rejection, whatever its type
            out, exc = None, e
    after = np.geterr()
    changed = after != before
    if changed:
        np.seterr(**before)
    info = {'warnings': sorted(set(w.category.__name__ + ': ' + str(w.message)[:200] for w in wl)),
            'numpy_errstate_changed': changed}
    return out, exc, info


def fresh(kw):
    return dict((k, (np.array(v, copy=True) if isinstance(v, np.ndarray) else v)) for k, v in kw.items())


def out_problems(out, shape):
    if not isinstance(out, np.ndarray):
        return ['not an ndarray: ' + type(out).__name__]
    p = []
    if type(out) is not np.ndarray:
        p.append('ndarray subclass ' + type(out).__name__)
    if out.dtype != C128:
        p.append('dtype ' + str(out.dtype))
    if shape is not None and out.shape != tuple(shape):
        p.append('shape ' + str(out.shape) + ' != ' + str(tuple(shape)))
    if out.dtype.kind in 'fc' and not bool(np.all(np.isfinite(out))):
        p.append('nonfinite output')
    return p


def formula_scale(kw):
    r = np.abs(np.asarray(kw['rho'], dtype=np.float64))[:, None]
    a = np.abs(np.asarray(kw['rho_R'], dtype=np.float64))[:, None]
    b = np.abs(np.asarray(kw['rho_z'], dtype=np.float64))[:, None]
    return (r * np.abs(np.asarray(kw['divU'], dtype=C128)) + a * np.abs(np.asarray(kw['U_R'], dtype=C128))
            + b * np.abs(np.asarray(kw['U_z'], dtype=C128)))


def scaled_error(out, ref, scale):
    out = np.asarray(out, dtype=C128)
    ref = np.asarray(ref, dtype=C128)
    if out.shape != ref.shape or out.shape != np.shape(scale):
        return float('inf')
    err = np.abs(out - ref)
    if err.size == 0:
        return 0.0
    safe = np.where(scale > 0, scale, 1.0)
    rel = np.where(scale > 0, err / safe, np.where(err > 0, np.inf, 0.0))
    return float(np.max(rel))


def global_rel(a, b):
    a = np.asarray(a, dtype=C128)
    b = np.asarray(b, dtype=C128)
    den = max(float(np.max(np.abs(a))), float(np.max(np.abs(b))), 1e-300)
    return float(np.max(np.abs(a - b))) / den


def contract_literal(*, rho, rho_R, rho_z, U_R, U_z, divU):
    """Vectorized contract equation, verbatim (baseline for the reference self-run only)."""
    rho = np.asarray(rho, dtype=np.float64)
    rho_R = np.asarray(rho_R, dtype=np.float64)
    rho_z = np.asarray(rho_z, dtype=np.float64)
    U_R = np.asarray(U_R, dtype=C128)
    U_z = np.asarray(U_z, dtype=C128)
    divU = np.asarray(divU, dtype=C128)
    return -rho[:, None] * divU - rho_R[:, None] * U_R - rho_z[:, None] * U_z


class Rec(object):
    def __init__(self):
        self.items = []

    def add(self, cid, group, status, **detail):
        self.items.append({'id': cid, 'group': group, 'status': status, 'detail': J(detail)})


def check_output(rec, cid, group, target, kw, expected, scale, rtol, require_real=False, extra=None):
    out, exc, info = invoke(target, kwargs=fresh(kw))
    d = dict(extra or {})
    d.update(info)
    if exc is not None:
        rec.add(cid, group, 'fail', exception=exc_desc(exc), **d)
        return None
    shape = np.shape(kw['U_R'])
    probs = out_problems(out, shape)
    err = None
    if isinstance(out, np.ndarray) and out.shape == tuple(shape):
        err = scaled_error(out, expected, scale)
        d['output_sha256'] = hashlib.sha256(np.ascontiguousarray(out).tobytes()).hexdigest()
    ok = (not probs) and err is not None and err <= rtol
    if require_real and isinstance(out, np.ndarray) and out.dtype.kind == 'c':
        imag_zero = bool(np.all(out.imag == 0))
        d['imag_exactly_zero'] = imag_zero
        ok = ok and imag_zero
    rec.add(cid, group, 'pass' if ok else 'fail', max_scaled_error=err, tolerance=rtol, problems=probs, **d)
    return out


# ------------------------------------------------------------------ A1 analytic fixtures
def d4(f, x, h):
    """Fourth-order central first derivative."""
    return (-f(x + 2.0 * h) + 8.0 * f(x + h) - 8.0 * f(x - h) + f(x - 2.0 * h)) / (12.0 * h)


# Family G term: c * R**n * z**l * exp(-beta z^2 + i kappa R); a component is a list of terms.
def t_val(t, R, z):
    c, n, l, beta, kap = t
    return c * R ** n * z ** l * np.exp(-beta * z * z + 1j * kap * R)


def t_dR(t, R, z):
    c, n, l, beta, kap = t
    return c * z ** l * np.exp(-beta * z * z + 1j * kap * R) * (n * R ** (n - 1) + 1j * kap * R ** n)


def t_dz(t, R, z):
    c, n, l, beta, kap = t
    lead = l * z ** (l - 1) if l >= 1 else 0.0
    return c * R ** n * np.exp(-beta * z * z + 1j * kap * R) * (lead - 2.0 * beta * z ** (l + 1))


def c_val(C, R, z):
    return sum(t_val(t, R, z) for t in C)


def c_dR(C, R, z):
    return sum(t_dR(t, R, z) for t in C)


def c_dz(C, R, z):
    return sum(t_dz(t, R, z) for t in C)


def c_mul(A, B):
    return [(a[0] * b[0], a[1] + b[1], a[2] + b[2], a[3] + b[3], a[4] + b[4]) for a in A for b in B]


def c_mulR(A):
    return [(a[0], a[1] + 1, a[2], a[3], a[4]) for a in A]


def family_G(case_id, a, seed, npts=17, ncol=6):
    """rho = rho0 (1 + a R^2) exp(-z^2/h^2); xi components are sums of monomial-Gaussian terms."""
    rng = np.random.default_rng(seed)
    rho0, h = 1.3, 0.8
    ih2 = 1.0 / (h * h)
    R = rng.uniform(0.3, 2.0, npts)
    z = rng.uniform(-0.9, 0.9, npts)
    gz = np.exp(-z * z * ih2)
    rho = rho0 * (1.0 + a * R * R) * gz          # closed form
    rho_R = rho0 * 2.0 * a * R * gz              # hand-derived d/dR
    rho_z = -2.0 * z * ih2 * rho                 # hand-derived d/dz
    rho_comp = [(rho0, 0, 0, ih2, 0.0), (rho0 * a, 2, 0, ih2, 0.0)]

    def rho_f(RR, zz):
        return rho0 * (1.0 + a * RR * RR) * np.exp(-zz * zz * ih2)

    cols = []
    for k in range(ncol):
        m = k + 1
        cf = [complex(rng.normal(), rng.normal()) for _ in range(6)]
        be = [complex(0.3 + 0.6 * rng.random(), 0.4 * (rng.random() - 0.5)) for _ in range(3)]
        ka = [float(rng.uniform(-1.5, 1.5)) for _ in range(3)]
        xiR = [(cf[0], 1, 0, be[0], ka[0]), (cf[1], 2, 1, be[0], ka[0])]
        xiP = [(cf[2], 1, 0, be[1], ka[1]), (cf[3], 0.5, 2, be[1], ka[1])]
        xiZ = [(cf[4], 0, 1, be[2], ka[2]), (cf[5], 1.5, 0, be[2], ka[2])]
        UR, UP, UZ = c_val(xiR, R, z), c_val(xiP, R, z), c_val(xiZ, R, z)
        phi_part = 1j * m * UP / R
        divU = c_dR(xiR, R, z) + UR / R + phi_part + c_dz(xiZ, R, z)
        # product route: expand R*rho*xi_R and rho*xi_z into monomial-Gaussian terms, differentiate those
        PRc = c_mulR(c_mul(rho_comp, xiR))
        PZc = c_mul(rho_comp, xiZ)
        E = -(c_dR(PRc, R, z) / R + 1j * m * rho * UP / R + c_dz(PZc, R, z))
        S = (sum(np.abs(t_dR(t, R, z)) for t in PRc) / R + np.abs(m * rho * UP / R)
             + sum(np.abs(t_dz(t, R, z)) for t in PZc))
        cols.append(dict(m=m, UR=UR, UP=UP, UZ=UZ, divU=divU, phi_part=phi_part, E=E, S=S,
                         xiR_f=functools.partial(c_val, xiR), xiP_f=functools.partial(c_val, xiP),
                         xiZ_f=functools.partial(c_val, xiZ)))
    return assemble(case_id, 'G(a=%g)' % a, R, z, rho, rho_R, rho_z, rho_f, cols,
                    hz=1e-3 * np.ones_like(z), real_output=False)


class PCol(object):
    """Column for family P: xi_c(R, z) = amp_c R^n_c exp(i kap_c R) Poly_c(zeta), zeta = z/H(R)."""

    def __init__(self, amp, kap, npow, polys, H0, cH):
        self.amp, self.kap, self.npow, self.polys = amp, kap, npow, polys
        self.H0, self.cH = H0, cH

    def radial(self, i, RR):
        return self.amp[i] * RR ** self.npow[i] * np.exp(1j * self.kap[i] * RR)

    def comp(self, i, RR, zz):
        ze = zz / (self.H0 * (1.0 + self.cH * RR))
        return self.radial(i, RR) * np.polynomial.polynomial.polyval(ze, self.polys[i])


def family_P(case_id, seed, helicity=False, npts=17, ncol=6):
    """Polytrope-like column rho = rho0 exp(-R/Rd) (1 - zeta^2)^1.5, zeta = z/H(R), H = H0 (1 + cH R)."""
    PP = np.polynomial.polynomial
    rng = np.random.default_rng(seed)
    rho0, Rd, H0, cH = 2.0, 1.1, 0.35, 0.4
    Hp = H0 * cH
    R = rng.uniform(0.3, 2.0, npts)
    zeta = rng.uniform(-0.85, 0.85, npts)
    H = H0 * (1.0 + cH * R)
    z = zeta * H
    q = 1.0 - zeta * zeta
    rc = rho0 * np.exp(-R / Rd)
    rho = rc * q ** 1.5
    rho_R = -rc / Rd * q ** 1.5 + 3.0 * rc * q ** 0.5 * zeta * zeta * Hp / H   # hand-derived
    rho_z = -3.0 * rc * q ** 0.5 * zeta / H                                    # hand-derived

    def rho_f(RR, zz):
        ze = zz / (H0 * (1.0 + cH * RR))
        return rho0 * np.exp(-RR / Rd) * (1.0 - ze * ze) ** 1.5

    cols = []
    for k in range(ncol):
        m = k + 1
        if helicity:   # real xi_R, xi_z and purely imaginary xi_phi (root helicity-map structure)
            amp = [float(rng.normal()), 1j * float(rng.normal()), float(rng.normal())]
            kap = [0.0, 0.0, 0.0]
            polys = [rng.normal(size=4) for _ in range(3)]
        else:
            amp = [complex(rng.normal(), rng.normal()) for _ in range(3)]
            kap = [float(rng.uniform(-1.0, 1.0)) for _ in range(3)]
            polys = [rng.normal(size=4) + 1j * rng.normal(size=4) for _ in range(3)]
        npow = [1.0, 1.0, 0.5]
        col = PCol(amp, kap, npow, polys, H0, cH)
        PRv, PRd = PP.polyval(zeta, polys[0]), PP.polyval(zeta, PP.polyder(polys[0]))
        PZv, PZd = PP.polyval(zeta, polys[2]), PP.polyval(zeta, PP.polyder(polys[2]))
        A = col.radial(0, R)
        UR = A * PRv
        UP = col.radial(1, R) * PP.polyval(zeta, polys[1])
        Cz = col.radial(2, R)
        UZ = Cz * PZv
        dRxiR = A * (npow[0] / R + 1j * kap[0]) * PRv - A * PRd * zeta * Hp / H   # chain rule (R, zeta)
        dzxiZ = Cz * PZd / H
        phi_part = 1j * m * UP / R
        divU = dRxiR + UR / R + phi_part + dzxiZ
        # product route on the closed-form products, (R, zeta) chain rule; never uses rho_R, rho_z, divU
        aR = amp[0] * rho0 * R ** (npow[0] + 1.0) * np.exp((1j * kap[0] - 1.0 / Rd) * R)   # R rho_c A
        aRp = aR * ((npow[0] + 1.0) / R + 1j * kap[0] - 1.0 / Rd)
        Q = q ** 1.5 * PRv
        Qp = -3.0 * zeta * q ** 0.5 * PRv + q ** 1.5 * PRd
        dR_prod = aRp * Q - aR * Qp * zeta * Hp / H
        cz = amp[2] * rho0 * R ** npow[2] * np.exp((1j * kap[2] - 1.0 / Rd) * R)            # rho_c C
        Qzp = -3.0 * zeta * q ** 0.5 * PZv + q ** 1.5 * PZd
        dz_prod = cz * Qzp / H
        E = -(dR_prod / R + 1j * m * rho * UP / R + dz_prod)
        S = ((np.abs(aRp * Q) + np.abs(aR * Qp * zeta * Hp / H)) / R + np.abs(m * rho * UP / R)
             + np.abs(cz * Qzp / H))
        cols.append(dict(m=m, UR=UR, UP=UP, UZ=UZ, divU=divU, phi_part=phi_part, E=E, S=S,
                         xiR_f=functools.partial(col.comp, 0), xiP_f=functools.partial(col.comp, 1),
                         xiZ_f=functools.partial(col.comp, 2)))
    return assemble(case_id, 'P(polytrope-like column)', R, z, rho, rho_R, rho_z, rho_f, cols,
                    hz=1e-3 * H, real_output=helicity)


def cart_div_fd(rho_f, col, R, z, phi0, hz):
    """-div(rho xi e^{i m phi}) by Cartesian finite differences, divided by e^{i m phi0}."""
    m = col['m']
    x0, y0 = R * np.cos(phi0), R * np.sin(phi0)
    hxy = 2e-4 * R

    def field(xx, yy, zz):
        RR = np.hypot(xx, yy)
        ph = np.arctan2(yy, xx)
        e = np.exp(1j * m * ph)
        r = rho_f(RR, zz)
        fR, fP, fZ = col['xiR_f'](RR, zz), col['xiP_f'](RR, zz), col['xiZ_f'](RR, zz)
        return (r * (fR * np.cos(ph) - fP * np.sin(ph)) * e,
                r * (fR * np.sin(ph) + fP * np.cos(ph)) * e,
                r * fZ * e)

    dfx = d4(lambda xx: field(xx, y0, z)[0], x0, hxy)
    dfy = d4(lambda yy: field(x0, yy, z)[1], y0, hxy)
    dfz = d4(lambda zz: field(x0, y0, zz)[2], z, hz)
    return -(dfx + dfy + dfz) * np.exp(-1j * m * phi0)


def assemble(case_id, family, R, z, rho, rho_R, rho_z, rho_f, cols, hz, real_output):
    hR = 1e-3
    sc = {}
    sc['rho_R_vs_fd'] = global_rel(rho_R, d4(lambda RR: rho_f(RR, z), R, hR))
    sc['rho_z_vs_fd'] = global_rel(rho_z, d4(lambda zz: rho_f(R, zz), z, hz))
    worst = {'divU_vs_fd': 0.0, 'E_vs_cyl_fd': 0.0, 'E_vs_cart_fd_phi0.7': 0.0, 'E_vs_cart_fd_phi2.3': 0.0}
    for c in cols:
        dv_fd = (d4(lambda RR: c['xiR_f'](RR, z), R, hR) + c['UR'] / R + 1j * c['m'] * c['UP'] / R
                 + d4(lambda zz: c['xiZ_f'](R, zz), z, hz))
        e_fd = -(d4(lambda RR: RR * rho_f(RR, z) * c['xiR_f'](RR, z), R, hR) / R
                 + 1j * c['m'] * rho * c['UP'] / R
                 + d4(lambda zz: rho_f(R, zz) * c['xiZ_f'](R, zz), z, hz))
        worst['divU_vs_fd'] = max(worst['divU_vs_fd'], global_rel(c['divU'], dv_fd))
        worst['E_vs_cyl_fd'] = max(worst['E_vs_cyl_fd'], global_rel(c['E'], e_fd))
        worst['E_vs_cart_fd_phi0.7'] = max(worst['E_vs_cart_fd_phi0.7'],
                                           global_rel(c['E'], cart_div_fd(rho_f, c, R, z, 0.7, hz)))
        worst['E_vs_cart_fd_phi2.3'] = max(worst['E_vs_cart_fd_phi2.3'],
                                           global_rel(c['E'], cart_div_fd(rho_f, c, R, z, 2.3, hz)))
    sc.update(worst)
    st = lambda key: np.stack([c[key] for c in cols], axis=1)
    UR, UZ, divU = st('UR'), st('UZ'), st('divU')
    structure_exact = True
    if real_output:   # root structure: real U_R, U_z dtype; divU complex dtype with real values
        structure_exact = bool(np.all(UR.imag == 0) and np.all(UZ.imag == 0) and np.all(divU.imag == 0))
        UR, UZ, divU = UR.real.copy(), UZ.real.copy(), divU.real.astype(C128)
    inputs = dict(rho=rho, rho_R=rho_R, rho_z=rho_z, U_R=UR, U_z=UZ, divU=divU)
    E = st('E')
    scale = st('S') + formula_scale(inputs)
    E_identity = -(rho[:, None] * divU + rho_R[:, None] * UR + rho_z[:, None] * UZ)
    sc['identity_expansion_vs_product_route_scaled'] = scaled_error(E_identity, E, scale)
    return dict(id=case_id, family=family, npts=len(R), ncol=len(cols), m=[c['m'] for c in cols],
                inputs=inputs, expected=E, scale=scale, R=R, phi_part=st('phi_part'),
                real_output=real_output, structure_exact=structure_exact, selfcheck=sc)


def eos_case(P):
    """Gradients supplied through the provider's EOS relation (transcribed, provider lines 44-46)."""
    rho, rho_R, rho_z, R = P['inputs']['rho'], P['inputs']['rho_R'], P['inputs']['rho_z'], P['R']
    K0, sK, g = 0.7, 0.3, 5.0 / 3.0
    K = K0 * (1.0 + sK * R)
    logKR = sK / (1.0 + sK * R)
    Pr = K * rho ** g
    PR = K0 * sK * rho ** g + g * K * rho ** (g - 1.0) * rho_R    # true d/dR of K(R) rho^g
    Pz = g * K * rho ** (g - 1.0) * rho_z                          # true d/dz (K_z = 0)

    def eos(PR_, Pz_):
        KR = K * logKR
        return (PR_ - rho ** (5 / 3) * KR) / ((5 / 3) * Pr / rho), Pz_ / ((5 / 3) * Pr / rho)

    rR, rz = eos(PR, Pz)
    sR = (np.abs(PR) + np.abs(rho ** (5 / 3) * K * logKR)) / ((5 / 3) * Pr / rho)
    sz = np.abs(Pz) / ((5 / 3) * Pr / rho)
    roundtrip = max(float(np.max(np.abs(rR - rho_R) / sR)), float(np.max(np.abs(rz - rho_z) / sz)))
    rRl, rzl = eos(PR * (1.0 + 1e-3), Pz * (1.0 - 2e-3))           # lagged (non-derivative) pressure data
    base = P['inputs']
    true_kw = dict(base, rho_R=rR, rho_z=rz)
    lag_kw = dict(base, rho_R=rRl, rho_z=rzl)
    pred = -(rRl - rR)[:, None] * np.asarray(base['U_R'], C128) - (rzl - rz)[:, None] * np.asarray(base['U_z'], C128)
    return dict(true_kw=true_kw, lag_kw=lag_kw, pred_delta=pred, expected=P['expected'],
                scale_true=P['scale'] - formula_scale(base) + formula_scale(true_kw),
                scale_pair=formula_scale(true_kw) + formula_scale(lag_kw),
                roundtrip_scaled=roundtrip, R=P['R'], phi_part=P['phi_part'])


def build_A1():
    cases = [family_G('G+', 0.45, 44801), family_G('G-', -0.2, 44802),
             family_P('P', 44803), family_P('H', 44804, helicity=True)]
    return cases, eos_case(cases[2])


def a1_fixture_checks(rec, cases, eos):
    for c in cases:
        sc = c['selfcheck']
        fd_keys = ['rho_R_vs_fd', 'rho_z_vs_fd', 'divU_vs_fd', 'E_vs_cyl_fd', 'E_vs_cart_fd_phi0.7', 'E_vs_cart_fd_phi2.3']
        ok = all(sc[k] <= RTOL_FD for k in fd_keys) and sc['identity_expansion_vs_product_route_scaled'] <= RTOL_A1
        ok = ok and c['structure_exact']
        rec.add('A1-fixture-' + c['id'], 'A1-fixture', 'pass' if ok else 'fail', family=c['family'],
                npts=c['npts'], m=c['m'], fd_tolerance=RTOL_FD, identity_tolerance=RTOL_A1,
                root_structure_exact=c['structure_exact'], **sc)
    rec.add('A1-fixture-EOS-roundtrip', 'A1-fixture', 'pass' if eos['roundtrip_scaled'] <= RTOL_A1 else 'fail',
            max_scaled_error=eos['roundtrip_scaled'], tolerance=RTOL_A1,
            note='rho_R,rho_z rebuilt from consistent K(R) rho^(5/3) pressure via the transcribed provider relation')


def run_A1(target, rec, cases, eos):
    for c in cases:
        CONTEXT['R'], CONTEXT['phi_part'] = c['R'], c['phi_part']
        check_output(rec, 'A1-target-' + c['id'], 'A1', target, c['inputs'], c['expected'], c['scale'],
                     RTOL_A1, require_real=c['real_output'], extra={'family': c['family'], 'm': c['m']})
        CONTEXT['R'], CONTEXT['phi_part'] = None, None
    CONTEXT['R'], CONTEXT['phi_part'] = eos['R'], eos['phi_part']
    g_true = check_output(rec, 'A1-target-EOS-consistent', 'A1', target, eos['true_kw'], eos['expected'],
                          eos['scale_true'], RTOL_A1)
    g_lag, exc, info = invoke(target, kwargs=fresh(eos['lag_kw']))
    CONTEXT['R'], CONTEXT['phi_part'] = None, None
    want = eos['pred_delta'].shape
    if (g_true is None or exc is not None or not isinstance(g_lag, np.ndarray) or not isinstance(g_true, np.ndarray)
            or g_lag.shape != want or g_true.shape != want):
        rec.add('A1-target-EOS-lag-identity', 'A1', 'fail', exception=(exc_desc(exc) if exc else None),
                shapes=[list(np.shape(g_true)) if g_true is not None else None,
                        list(np.shape(g_lag)) if g_lag is not None else None, list(want)])
        return
    err = scaled_error(np.asarray(g_lag, C128) - np.asarray(g_true, C128), eos['pred_delta'], eos['scale_pair'])
    rec.add('A1-target-EOS-lag-identity', 'A1', 'pass' if err <= RTOL_A1 else 'fail', max_scaled_error=err,
            tolerance=RTOL_A1, claim='Gkin(lagged rho_R,rho_z) - Gkin(true) = -(d rho_R) U_R - (d rho_z) U_z')
    rec.add('A1-record-EOS-lag-deviation', 'A1', 'record',
            relative_departure_from_minus_div_rho_xi=global_rel(g_lag, eos['expected']),
            note='PR*(1+1e-3), Pz*(1-2e-3): Gkin equals -div(rho xi) only if supplied gradients are those of rho')


# ------------------------------------------------------------------ A2 reference comparison
def a2_inputs(seed, n, f, dyn=False):
    g = np.random.default_rng(seed)
    rho = np.exp(g.normal(size=n))
    rho_R = g.normal(size=n) * np.exp(g.normal(size=n))
    rho_z = g.normal(size=n) * np.exp(g.normal(size=n))
    maps = [g.normal(size=(n, f)) + 1j * g.normal(size=(n, f)) for _ in range(3)]
    if dyn:
        rho = rho * 10.0 ** g.integers(-3, 4, size=n)
        rho_R = rho_R * 10.0 ** g.integers(-3, 4, size=n)
        rho_z = rho_z * 10.0 ** g.integers(-3, 4, size=n)
        maps = [mp * 10.0 ** g.integers(-6, 7, size=(n, f)) for mp in maps]
    return dict(rho=rho, rho_R=rho_R, rho_z=rho_z, U_R=maps[0], U_z=maps[1], divU=maps[2])


def root_structured(seed, n, f):
    kw = a2_inputs(seed, n, f)
    g = np.random.default_rng(seed + 1000)
    kw['U_R'] = g.normal(size=(n, f))
    kw['U_z'] = g.normal(size=(n, f))
    kw['divU'] = g.normal(size=(n, f)).astype(C128)
    return kw


A2_CASES = [('rect_7x3', 4201, 7, 3, False), ('square_5x5', 4202, 5, 5, False),
            ('square_1x1', 4203, 1, 1, False), ('nfree1_9x1', 4204, 9, 1, False),
            ('npoints1_1x4', 4205, 1, 4, False), ('dynamic_range_8x6', 4206, 8, 6, True)]


def same_bits(a, b):
    return (isinstance(a, np.ndarray) and isinstance(b, np.ndarray) and a.dtype == b.dtype
            and a.shape == b.shape and np.ascontiguousarray(a).tobytes() == np.ascontiguousarray(b).tobytes())


def run_A2(target, rec, baseline, baseline_name):
    for name, seed, n, f, dyn in A2_CASES:
        kw = a2_inputs(seed, n, f, dyn)
        ref = baseline(**fresh(kw))
        check_output(rec, 'A2-' + name, 'A2', target, kw, ref, formula_scale(kw), RTOL_A2,
                     extra={'baseline': baseline_name})
    # root-structured: real-dtype U_R,U_z and real-valued complex divU; bitwise vs explicit complex128 cast
    kw = root_structured(4207, 6, 4)
    ref = baseline(**fresh(kw))
    out = check_output(rec, 'A2-root_structured_vs_baseline', 'A2', target, kw, ref, formula_scale(kw), RTOL_A2,
                       require_real=True, extra={'baseline': baseline_name})
    variants = [('U_R,U_z float64 vs complex128', dict(kw, U_R=kw['U_R'].astype(C128), U_z=kw['U_z'].astype(C128)), kw),
                ('divU float64 vs complex128', dict(kw, divU=kw['divU'].real.copy()), kw)]
    g = np.random.default_rng(4208)
    c64 = dict(a2_inputs(4208, 5, 3), **dict((k, (g.normal(size=(5, 3)) + 1j * g.normal(size=(5, 3))).astype(np.complex64)) for k in MAPS))
    variants.append(('maps complex64 vs complex128', c64, dict(c64, **dict((k, c64[k].astype(C128)) for k in MAPS))))
    f32 = dict(a2_inputs(4209, 5, 3), **dict((k, g.normal(size=(5, 3)).astype(np.float32)) for k in MAPS))
    variants.append(('maps float32 vs complex128', f32, dict(f32, **dict((k, f32[k].astype(C128)) for k in MAPS))))
    for label, kw_a, kw_b in variants:
        oa, ea, _ = invoke(target, kwargs=fresh(kw_a))
        ob, eb, _ = invoke(target, kwargs=fresh(kw_b))
        if ea is not None or eb is not None:
            rec.add('A2-lossless_cast: ' + label, 'A2', 'fail',
                    exception=[exc_desc(e) if e else None for e in (ea, eb)])
            continue
        bits = same_bits(oa, ob)
        val = bool(isinstance(oa, np.ndarray) and isinstance(ob, np.ndarray) and oa.shape == ob.shape
                   and np.array_equal(oa, ob))
        probs = out_problems(oa, np.shape(kw_a['U_R']))
        rec.add('A2-lossless_cast: ' + label, 'A2', 'pass' if (bits and not probs) else 'fail',
                bitwise_equal=bits, value_equal=val, problems=probs,
                note='values identical but bytes differ means signed-zero differences only' if (val and not bits) else '')


# ------------------------------------------------------------------ A3 properties
def run_A3(target, rec):
    G = 'A3'
    try:
        sig = inspect.signature(target)
        ps = list(sig.parameters.values())
        names = [p.name for p in ps]
        kinds = [p.kind.name for p in ps]
        defaults = [p.name for p in ps if p.default is not inspect.Parameter.empty]
        phi_like = [nm for nm in names if 'phi' in nm.lower() or nm in ('UP', 'U_P', 'm', 'R')]
        ok = (sorted(names) == sorted(PARAMS) and all(p.kind == inspect.Parameter.KEYWORD_ONLY for p in ps)
              and not defaults and not phi_like)
        rec.add('A3-signature', G, 'pass' if ok else 'fail', signature=str(sig), names=names, kinds=kinds,
                defaults=defaults, phi_or_R_or_m_parameters=phi_like,
                note='Gkin cannot depend on U_phi: no such input; the phi part enters only through divU')
    except (TypeError, ValueError) as e:
        rec.add('A3-signature', G, 'fail', exception=exc_desc(e))

    n, f = 6, 4
    X = a2_inputs(4301, n, f)
    Yv = a2_inputs(4302, n, f)
    Y = dict(X, **dict((k, Yv[k]) for k in MAPS))

    def call(kw, copy=True):
        out, exc, info = invoke(target, kwargs=(fresh(kw) if copy else dict(kw)))
        if exc is not None:
            raise RuntimeError('%s: %s' % (type(exc).__name__, str(exc)[:300]))
        if not isinstance(out, np.ndarray):
            raise RuntimeError('non-ndarray output ' + type(out).__name__)
        return out

    def guarded(cid, fn):
        try:
            fn()
        except Exception as e:  # any failure of a property check is a failed check, recorded
            rec.add(cid, G, 'fail', exception=exc_desc(e))

    def t_dtype_shape():
        o1 = call(X)
        o2 = call(root_structured(4303, n, f))
        p = out_problems(o1, (n, f)) + out_problems(o2, (n, f))
        rec.add('A3-output_complex128_shape_of_U_R', G, 'pass' if not p else 'fail', problems=p,
                c_contiguous=bool(o1.flags.c_contiguous))
    guarded('A3-output_complex128_shape_of_U_R', t_dtype_shape)

    def t_linear():
        a, b = 0.7 - 1.3j, -0.4 + 2.1j
        L = dict(X, **dict((k, a * X[k] + b * Y[k]) for k in MAPS))
        fx, fy, fl = call(X), call(Y), call(L)
        err = scaled_error(fl, a * fx + b * fy, abs(a) * formula_scale(X) + abs(b) * formula_scale(Y))
        rec.add('A3-linearity_in_maps', G, 'pass' if err <= 1e-13 else 'fail', max_scaled_error=err, tolerance=1e-13)
    guarded('A3-linearity_in_maps', t_linear)

    def t_pow2():
        fx = call(X)
        r1 = np.array_equal(call(dict(X, **dict((k, 8.0 * X[k]) for k in MAPS))), 8.0 * fx)
        r2 = np.array_equal(call(dict(X, **dict((k, X[k] * 2.0 ** -5) for k in MAPS))), fx * 2.0 ** -5)
        r3 = np.array_equal(call(dict(X, **dict((k, 2.0 * X[k]) for k in VECS))), 2.0 * fx)
        rec.add('A3-exact_power_of_two_homogeneity', G, 'pass' if (r1 and r2 and r3) else 'fail',
                maps_x8=r1, maps_x2m5=r2, vectors_x2=r3)
    guarded('A3-exact_power_of_two_homogeneity', t_pow2)

    def t_rot():
        fx = call(X)
        fi = call(dict(X, **dict((k, 1j * X[k]) for k in MAPS)))
        err = scaled_error(fi, 1j * fx, formula_scale(X))
        rec.add('A3-complex_rotation_equivariance', G, 'pass' if err <= 4 * EPS else 'fail', max_scaled_error=err,
                tolerance=4 * EPS, exactly_equal=bool(np.array_equal(fi, 1j * fx)),
                note='f(iX) = i f(X); a conjugating implementation gives -i f(X)')
    guarded('A3-complex_rotation_equivariance', t_rot)

    def t_cols():
        fx = call(X)
        Jc = [2, 0]
        sub = call(dict(X, **dict((k, X[k][:, Jc]) for k in MAPS)))
        ok1 = sub.shape == (n, len(Jc)) and np.array_equal(sub, fx[:, Jc])
        Pt = dict(X, **dict((k, X[k].copy()) for k in MAPS))
        for k in MAPS:
            Pt[k][:, 1] += (1.5 - 0.5j)
        fp = call(Pt)
        others = [0, 2, 3]
        ok2 = fp.shape == fx.shape and np.array_equal(fp[:, others], fx[:, others]) and not np.array_equal(fp[:, 1], fx[:, 1])
        rec.add('A3-column_independence', G, 'pass' if (ok1 and ok2) else 'fail', column_subset_exact=bool(ok1),
                perturb_one_column_changes_only_it=bool(ok2))
    guarded('A3-column_independence', t_cols)

    def t_rows():
        fx = call(X)
        I = [4, 1, 3]
        sub = call(dict((k, X[k][I]) for k in PARAMS))
        ok = sub.shape == (len(I), f) and np.array_equal(sub, fx[I])
        rec.add('A3-point_row_independence', G, 'pass' if ok else 'fail', row_subset_exact=bool(ok))
    guarded('A3-point_row_independence', t_rows)

    def t_mutation_alias():
        details = {}
        ok = True
        for label, kw in (('complex_maps', X), ('root_structured', root_structured(4304, n, f))):
            passed = fresh(kw)
            snap = dict((k, (v.dtype, v.shape, v.tobytes())) for k, v in passed.items())
            out, exc, info = invoke(target, kwargs=passed)
            if exc is not None:
                details[label] = {'exception': exc_desc(exc)}
                ok = False
                continue
            changed = [k for k, v in passed.items() if (v.dtype, v.shape, v.tobytes()) != snap[k]]
            aliased = [k for k, v in passed.items() if isinstance(out, np.ndarray) and np.shares_memory(out, v)]
            details[label] = {'inputs_changed': changed, 'output_aliases': aliased}
            ok = ok and not changed and not aliased
        rec.add('A3-no_input_mutation_no_aliasing', G, 'pass' if ok else 'fail', **details)
    guarded('A3-no_input_mutation_no_aliasing', t_mutation_alias)

    def t_readonly():
        fx = call(X)
        ro = fresh(X)
        for v in ro.values():
            v.setflags(write=False)
        out = call(ro, copy=False)   # the non-writeable arrays themselves are passed
        rec.add('A3-read_only_inputs_accepted', G, 'pass' if np.array_equal(out, fx) else 'fail',
                inputs_still_read_only=all(not v.flags.writeable for v in ro.values()))
    guarded('A3-read_only_inputs_accepted', t_readonly)

    def t_layout():
        fx = call(X)
        views = {}
        for k in MAPS:
            big = np.zeros((n, 2 * f), dtype=C128)
            big[:, ::2] = X[k]
            views[k] = big[:, ::2]
        for k in VECS:
            bigv = np.zeros(2 * n)
            bigv[::2] = X[k]
            views[k] = bigv[::2]
        strided = all(not views[k].flags.c_contiguous for k in PARAMS)
        o_view = call(views, copy=False)   # strided views passed as-is
        fort = dict(X, **dict((k, np.asfortranarray(X[k])) for k in MAPS))
        fortran = all(fort[k].flags.f_contiguous and not fort[k].flags.c_contiguous for k in MAPS)
        o_fort = call(fort, copy=False)
        ok = np.array_equal(o_view, fx) and np.array_equal(o_fort, fx) and strided and fortran
        rec.add('A3-noncontiguous_and_fortran_inputs', G, 'pass' if ok else 'fail',
                inputs_really_strided=strided, inputs_really_fortran=fortran,
                strided_views_equal=bool(np.array_equal(o_view, fx)), fortran_equal=bool(np.array_equal(o_fort, fx)))
    guarded('A3-noncontiguous_and_fortran_inputs', t_layout)

    def t_det():
        a, b = call(X), call(X)
        rec.add('A3-determinism', G, 'pass' if same_bits(a, b) else 'fail')
    guarded('A3-determinism', t_det)

    out, exc, info = invoke(target, kwargs=fresh(X))
    rec.add('A3-record-warnings_and_errstate_on_valid_call', G, 'record', **info)


# ------------------------------------------------------------------ A4 malformed-input probes
B_SIG = '0447: keyword-only signature kinematic_density_map(*, rho, rho_R, rho_z, U_R, U_z, divU); no hidden defaults'
B_PHI = 'contract: do not add a separate phi term a second time; 0447: no extra derivative or azimuth factor'
B_SHAPE = '0447: validate consistent shapes (vectors (n,), maps (n,nfree)); contract: output shape of U_R'
B_VFIN = '0447: finite real vectors'
B_VREAL = '0447: finite real vectors (nonzero imaginary part is not real)'
B_RPOS = '0447: positive rho'
B_GRAD = 'contract: rho_R, rho_z are supplied EOS/lagged derivatives; either sign is physical'
B_MFIN = '0447: finite real/complex maps'
B_MCAST = '0447: maps cast losslessly to complex128'
B_MDT = '0447: finite real/complex maps; object/string dtypes are neither'
B_OUT = 'contract: finite complex128 Gkin; 0447: reject nonfinite output'
B_SILENT = 'contract/0447 silent; either outcome defensible (recorded only)'


def a4_specs():
    n, f = 6, 3
    base = a2_inputs(4401, n, f)
    specs = []

    def cp():
        return dict((k, np.array(v, copy=True)) for k, v in base.items())

    def mod(**ch):
        d = cp()
        d.update(ch)
        return d

    def setv(name, idx, val):
        v = np.array(base[name], copy=True)
        v[idx] = val
        return v

    def add(pid, desc, expected, basis, kw, args=()):
        specs.append(dict(pid=pid, desc=desc, expected=expected, basis=basis, kw=kw, args=args))

    kw = cp(); del kw['divU']; add('P01', 'missing kwarg divU', 'reject', B_SIG, kw)
    kw = cp(); del kw['rho']; add('P02', 'missing kwarg rho', 'reject', B_SIG, kw)
    add('P03', 'all six arguments positional', 'reject', B_SIG, {}, tuple(base[k] for k in PARAMS))
    add('P04', 'extra kwarg U_phi', 'reject', B_PHI, mod(U_phi=1j * base['U_R']))
    add('P05', 'extra kwarg m=1', 'reject', B_PHI, mod(m=1))
    add('P06', 'rho length n+1', 'reject', B_SHAPE, mod(rho=np.append(base['rho'], 1.0)))
    add('P07', 'rho_R length n-1', 'reject', B_SHAPE, mod(rho_R=base['rho_R'][:-1].copy()))
    add('P08', 'rho_z length n+1', 'reject', B_SHAPE, mod(rho_z=np.append(base['rho_z'], 0.5)))
    add('P09', 'rho_R shape (1,) (broadcastable)', 'reject', B_SHAPE, mod(rho_R=np.array([0.3])))
    add('P10', 'rho 2-D (n,1)', 'reject', B_SHAPE, mod(rho=base['rho'][:, None].copy()))
    add('P11', 'rho_z 2-D (1,n)', 'reject', B_SHAPE, mod(rho_z=base['rho_z'][None, :].copy()))
    add('P12', 'rho 0-D', 'reject', B_SHAPE, mod(rho=np.array(1.2)))
    add('P13', 'rho contains nan', 'reject', B_VFIN, mod(rho=setv('rho', 2, np.nan)))
    add('P14', 'rho contains +inf', 'reject', B_VFIN, mod(rho=setv('rho', 2, np.inf)))
    add('P15', 'rho_R contains nan', 'reject', B_VFIN, mod(rho_R=setv('rho_R', 1, np.nan)))
    add('P16', 'rho_z contains -inf', 'reject', B_VFIN, mod(rho_z=setv('rho_z', 4, -np.inf)))
    add('P17', 'rho complex dtype, nonzero imag', 'reject', B_VREAL, mod(rho=base['rho'] + 0.1j))
    add('P18', 'rho_R complex dtype, nonzero imag', 'reject', B_VREAL, mod(rho_R=base['rho_R'] - 0.2j))
    add('P19', 'rho complex dtype, zero imag', 'record_only', B_SILENT, mod(rho=base['rho'].astype(C128)))
    add('P20', 'rho_z complex dtype, zero imag', 'record_only', B_SILENT, mod(rho_z=base['rho_z'].astype(C128)))
    add('P21', 'rho = +0.0 at one point', 'reject', B_RPOS, mod(rho=setv('rho', 1, 0.0)))
    add('P22', 'rho = -0.0 at one point', 'reject', B_RPOS, mod(rho=setv('rho', 1, -0.0)))
    add('P23', 'rho negative at one point', 'reject', B_RPOS, mod(rho=setv('rho', 3, -0.5)))
    add('P24', 'rho tiny positive 1e-300', 'accept', B_RPOS, mod(rho=setv('rho', 0, 1e-300)))
    add('P25', 'rho_R all negative', 'accept', B_GRAD, mod(rho_R=-np.abs(base['rho_R']) - 0.1))
    add('P26', 'rho_z all negative', 'accept', B_GRAD, mod(rho_z=-np.abs(base['rho_z']) - 0.1))
    add('P27', 'rho_R = rho_z = 0 (uniform density)', 'accept', B_GRAD, mod(rho_R=np.zeros(n), rho_z=np.zeros(n)))
    add('P28', 'rho int64 positive', 'record_only', B_SILENT, mod(rho=np.arange(1, n + 1, dtype=np.int64)))
    add('P29', 'rho float32', 'record_only', B_SILENT, mod(rho=base['rho'].astype(np.float32)))
    add('P30', 'rho bool (all True)', 'record_only', B_SILENT, mod(rho=np.ones(n, dtype=bool)))
    add('P31', 'rho object dtype', 'reject', B_VFIN + ' (object dtype is not a real dtype)',
        mod(rho=np.array(list(base['rho']), dtype=object)))
    add('P32', 'rho string dtype', 'reject', B_VFIN + ' (string dtype is not numeric)', mod(rho=base['rho'].astype(str)))
    add('P33', 'vectors as Python lists', 'record_only', B_SILENT,
        mod(rho=list(map(float, base['rho'])), rho_R=list(map(float, base['rho_R'])), rho_z=list(map(float, base['rho_z']))))
    add('P34', 'U_R npoints n+1', 'reject', B_SHAPE, mod(U_R=np.vstack([base['U_R'], base['U_R'][:1]])))
    add('P35', 'U_z npoints n-1', 'reject', B_SHAPE, mod(U_z=base['U_z'][:-1].copy()))
    add('P36', 'divU npoints n+1', 'reject', B_SHAPE, mod(divU=np.vstack([base['divU'], base['divU'][:1]])))
    add('P37', 'all maps npoints n+1 vs vectors n', 'reject', B_SHAPE,
        mod(**dict((k, np.vstack([base[k], base[k][:1]])) for k in MAPS)))
    add('P38', 'U_z nfree+1', 'reject', B_SHAPE, mod(U_z=np.hstack([base['U_z'], base['U_z'][:, :1]])))
    add('P39', 'divU nfree-1', 'reject', B_SHAPE, mod(divU=base['divU'][:, :-1].copy()))
    add('P40', 'U_z shape (n,1) (broadcastable)', 'reject', B_SHAPE, mod(U_z=base['U_z'][:, :1].copy()))
    add('P41', 'divU shape (1,nfree) (broadcastable)', 'reject', B_SHAPE, mod(divU=base['divU'][:1, :].copy()))
    add('P42', 'all maps 1-D length n', 'reject', B_SHAPE + ' (1-D maps would broadcast to (n,n))',
        mod(**dict((k, base[k][:, 0].copy()) for k in MAPS)))
    add('P43', 'U_R 1-D only', 'reject', B_SHAPE, mod(U_R=base['U_R'][:, 0].copy()))
    add('P44', 'all maps 3-D (n,nfree,1)', 'reject', B_SHAPE, mod(**dict((k, base[k][..., None].copy()) for k in MAPS)))
    add('P45', 'U_R contains nan', 'reject', B_MFIN, mod(U_R=setv('U_R', (2, 1), np.nan)))
    add('P46', 'U_z contains +inf', 'reject', B_MFIN, mod(U_z=setv('U_z', (0, 2), np.inf)))
    add('P47', 'divU nan in imaginary part only', 'reject', B_MFIN, mod(divU=setv('divU', (1, 2), complex(1.0, np.nan))))
    add('P48', 'divU inf in imaginary part', 'reject', B_MFIN, mod(divU=setv('divU', (3, 0), complex(0.5, np.inf))))
    add('P49', 'U_R bool dtype', 'record_only', B_SILENT + '; reject preferred (bool is not a real/complex dtype)',
        mod(U_R=(np.abs(base['U_R']) > 1.0)))
    add('P50', 'U_z object dtype', 'reject', B_MDT, mod(U_z=np.array(base['U_z'].tolist(), dtype=object)))
    add('P51', 'divU string dtype', 'reject', B_MDT, mod(divU=base['divU'].astype(str)))
    add('P52', 'U_R int64 small values', 'record_only', B_SILENT,
        mod(U_R=np.arange(n * f, dtype=np.int64).reshape(n, f) - 5))
    big = np.arange(n * f, dtype=np.int64).reshape(n, f)
    big[0, 0] = 2 ** 53 + 1
    add('P53', 'U_R int64 holding 2**53+1 (not exactly representable)', 'reject', B_MCAST, mod(U_R=big))
    add('P54', 'maps complex64', 'accept', B_MCAST, mod(**dict((k, base[k].astype(np.complex64)) for k in MAPS)))
    add('P55', 'maps float32 (real parts)', 'accept', B_MCAST, mod(**dict((k, base[k].real.astype(np.float32)) for k in MAPS)))
    add('P56', 'maps float16 (real parts)', 'accept', B_MCAST, mod(**dict((k, base[k].real.astype(np.float16)) for k in MAPS)))
    add('P57', 'root-structured: U_R,U_z float64; divU real-valued complex128', 'accept', B_MCAST,
        mod(U_R=base['U_R'].real.copy(), U_z=base['U_z'].real.copy(), divU=base['divU'].real.astype(C128)))
    add('P58', 'divU float64 dtype', 'accept', B_MCAST, mod(divU=base['divU'].real.copy()))
    add('P59', 'maps as nested Python lists', 'record_only', B_SILENT, mod(**dict((k, base[k].tolist()) for k in MAPS)))
    add('P60', 'maps longdouble (real parts); itemsize %d here' % np.dtype(np.longdouble).itemsize, 'record_only',
        B_SILENT, mod(**dict((k, base[k].real.astype(np.longdouble)) for k in MAPS)))
    add('P61', 'npoints = 0', 'record_only', B_SILENT,
        dict(rho=np.zeros(0), rho_R=np.zeros(0), rho_z=np.zeros(0), **dict((k, np.zeros((0, f), C128)) for k in MAPS)))
    add('P62', 'nfree = 0', 'record_only', B_SILENT, mod(**dict((k, np.zeros((n, 0), C128)) for k in MAPS)))
    kw = cp(); kw['rho'][0] = 1e200; kw['divU'][0, :] = 1e200
    add('P63', 'overflow in one product (1e200*1e200)', 'reject', B_OUT, kw)
    kw = cp(); kw['rho'][0] = 1.0; kw['divU'][0, :] = -1.5e308; kw['rho_R'][0] = 1.0; kw['U_R'][0, :] = -1.5e308
    kw['U_z'][0, :] = 0.0
    add('P64', 'overflow only in the sum of finite terms (1.5e308+1.5e308)', 'reject', B_OUT, kw)
    kw = cp(); kw['rho'][0] = 1e10; kw['divU'][0, :] = 1e300j
    add('P65', 'overflow in imaginary part only', 'reject', B_OUT, kw)
    kw = cp(); kw['rho'][0] = 1e150; kw['divU'][0, :] = 1e150
    add('P66', 'large finite product (1e150*1e150)', 'accept', B_OUT, kw)
    kw = cp(); kw['rho'][0] = 1e-300; kw['rho_R'][0] = 0.0; kw['rho_z'][0] = 0.0; kw['divU'][0, :] = 1e-20
    add('P67', 'subnormal output entries (1e-300*1e-20)', 'accept', B_OUT, kw)
    kw = cp(); kw['rho_R'][0] = np.inf; kw['U_R'][0, :] = 0.0
    add('P68', 'rho_R inf where U_R row is zero (inf*0)', 'reject', B_VFIN, kw)
    return specs


def run_A4(target, reference, scored):
    results = []
    for s in a4_specs():
        kw = dict((k, (np.array(v, copy=True) if isinstance(v, np.ndarray) else v)) for k, v in s['kw'].items())
        out, exc, info = invoke(target, kwargs=kw, args=s['args'])
        r = {'pid': s['pid'], 'desc': s['desc'], 'expected': s['expected'], 'basis': s['basis'],
             'accepted': exc is None, 'warnings': info['warnings']}
        if exc is not None:
            r['exception'] = exc_desc(exc)
        else:
            try:
                shape = np.shape(s['kw'].get('U_R'))
            except Exception:
                shape = None
            r['problems'] = out_problems(out, shape)
            try:
                with warnings.catch_warnings():
                    warnings.simplefilter('ignore')
                    with np.errstate(all='ignore'):
                        ref = reference(**dict((k, (np.array(v, copy=True) if isinstance(v, np.ndarray) else v))
                                               for k, v in s['kw'].items()))
                        r['value_vs_reference_scaled'] = scaled_error(out, ref, formula_scale(s['kw']))
            except Exception as e:
                r['value_vs_reference_scaled'] = None
                r['reference_note'] = 'reference not applicable: ' + type(e).__name__
        if not scored:
            r['verdict'] = 'record'
        elif s['expected'] == 'record_only':
            r['verdict'] = 'record'
        elif s['expected'] == 'reject':
            r['verdict'] = 'as_expected' if exc is not None else 'UNEXPECTED'
        else:
            good = (exc is None and not r['problems'] and r.get('value_vs_reference_scaled') is not None
                    and r['value_vs_reference_scaled'] <= RTOL_A2)
            r['verdict'] = 'as_expected' if good else 'UNEXPECTED'
        results.append(J(r))
    return results


# ------------------------------------------------------------------ A5 mutation sensitivity
def _ctx_R(n):
    R = CONTEXT.get('R')
    if R is not None and np.shape(R) == (n,):
        return R
    return np.linspace(0.6, 1.9, n)


def _ctx_phi(shape):
    p = CONTEXT.get('phi_part')
    if p is not None and np.shape(p) == tuple(shape):
        return p
    g = np.random.default_rng(97)
    return 1j * (g.normal(size=shape) + 1j * g.normal(size=shape))   # synthetic stand-in


def make_loop_mutant(kind):
    def mutant(*, rho, rho_R, rho_z, U_R, U_z, divU):
        r = np.asarray(rho, dtype=np.float64)
        a = np.asarray(rho_R, dtype=np.float64)
        b = np.asarray(rho_z, dtype=np.float64)
        ur = np.asarray(U_R, dtype=C128)
        uz = np.asarray(U_z, dtype=C128)
        dv = np.asarray(divU, dtype=C128)
        n, nf = ur.shape
        R = _ctx_R(n)
        ph = _ctx_phi((n, nf))
        out = np.empty((n, nf), dtype=C128)
        for i in range(n):
            ri, ai, bi, Ri = float(r[i]), float(a[i]), float(b[i]), float(R[i])
            for j in range(nf):
                d, u, w = complex(dv[i, j]), complex(ur[i, j]), complex(uz[i, j])
                if kind == 'conjugated_maps':
                    d, u, w = d.conjugate(), u.conjugate(), w.conjugate()
                t1, t2, t3 = (-ri) * d, ai * u, bi * w
                if kind == 'sign_term_rho_divU':
                    t1 = -t1
                elif kind == 'sign_term_rhoR_UR':
                    t2 = -t2
                elif kind == 'sign_term_rhoz_Uz':
                    t3 = -t3
                elif kind == 'missing_rho_on_divU':
                    t1 = -d
                elif kind == 'rhoR_rhoz_swapped':
                    t2, t3 = bi * u, ai * w
                elif kind == 'rhoR_used_for_Uz':
                    t3 = ai * w
                elif kind == 'rhoz_term_dropped':
                    t3 = 0j
                elif kind == 'extra_R_factor_on_rhoR_UR':
                    t2 = Ri * ai * u
                elif kind == 'extra_1_over_R_on_divU_term':
                    t1 = (-ri) * d / Ri
                val = t1 - t2 - t3
                if kind == 'duplicate_phi_term':
                    val = val - ri * complex(ph[i, j])
                elif kind == 'duplicate_UR_over_R_term':
                    val = val - ri * u / Ri
                out[i, j] = val
        if kind == 'real_part_only':
            out = out.real.astype(C128)
        elif kind == 'transposed_output':
            out = np.ascontiguousarray(out.T)
        elif kind == 'complex64_precision':
            out = out.astype(np.complex64).astype(C128)
        return out
    mutant.__name__ = 'mutant_' + kind
    return mutant


def mutant_no_column_broadcast(*, rho, rho_R, rho_z, U_R, U_z, divU):
    r = np.asarray(rho, dtype=np.float64)
    a = np.asarray(rho_R, dtype=np.float64)
    b = np.asarray(rho_z, dtype=np.float64)
    return -r * np.asarray(divU, dtype=C128) - a * np.asarray(U_R, dtype=C128) - b * np.asarray(U_z, dtype=C128)


def mutant_inplace_input(*, rho, rho_R, rho_z, U_R, U_z, divU):
    r = np.asarray(rho, dtype=np.float64)
    a = np.asarray(rho_R, dtype=np.float64)
    b = np.asarray(rho_z, dtype=np.float64)
    dv = divU                        # writes into the caller's array
    dv *= -r[:, None]
    dv -= a[:, None] * np.asarray(U_R, dtype=C128)
    dv -= b[:, None] * np.asarray(U_z, dtype=C128)
    return dv


MUTANTS = [
    ('M01', 'sign of -rho*divU flipped', make_loop_mutant('sign_term_rho_divU')),
    ('M02', 'sign of -rho_R*U_R flipped', make_loop_mutant('sign_term_rhoR_UR')),
    ('M03', 'sign of -rho_z*U_z flipped', make_loop_mutant('sign_term_rhoz_Uz')),
    ('M04', 'rho missing on divU term', make_loop_mutant('missing_rho_on_divU')),
    ('M05', 'rho_R and rho_z swapped', make_loop_mutant('rhoR_rhoz_swapped')),
    ('M06', 'duplicate phi term -rho*(i m U_phi/R) (A1: actual phi part; elsewhere synthetic)', make_loop_mutant('duplicate_phi_term')),
    ('M07', 'duplicate cylindrical term -rho*U_R/R', make_loop_mutant('duplicate_UR_over_R_term')),
    ('M08', 'extra R factor on rho_R*U_R', make_loop_mutant('extra_R_factor_on_rhoR_UR')),
    ('M09', 'extra 1/R factor on rho*divU', make_loop_mutant('extra_1_over_R_on_divU_term')),
    ('M10', 'conjugated maps', make_loop_mutant('conjugated_maps')),
    ('M11', 'vectors broadcast without [:,None]', mutant_no_column_broadcast),
    ('M12', 'real part only', make_loop_mutant('real_part_only')),
    ('M13', 'transposed output', make_loop_mutant('transposed_output')),
    ('M14', 'in-place write into divU input', mutant_inplace_input),
    ('M15', 'rho_R used for the U_z term', make_loop_mutant('rhoR_used_for_Uz')),
    ('M16', 'rho_z term dropped', make_loop_mutant('rhoz_term_dropped')),
    ('M17', 'complex64 precision', make_loop_mutant('complex64_precision')),
]


def run_A5(reference, cases, eos):
    table = []
    for mid, desc, fn in MUTANTS:
        r = Rec()
        run_A1(fn, r, cases, eos)
        run_A2(fn, r, reference, 'K2 loop reference')
        run_A3(fn, r)
        failed = [c['id'] for c in r.items if c['status'] == 'fail']
        table.append({'id': mid, 'mutation': desc, 'detected': bool(failed), 'n_failed_checks': len(failed),
                      'detected_by': failed[:12]})
    return table


# ------------------------------------------------------------------ driver
def summarize(rec, probes, mutations):
    passed = [c['id'] for c in rec.items if c['status'] == 'pass']
    failed = [c['id'] for c in rec.items if c['status'] == 'fail']
    record = [c['id'] for c in rec.items if c['status'] == 'record']
    passed += [p['pid'] for p in probes if p['verdict'] == 'as_expected']
    failed += [p['pid'] for p in probes if p['verdict'] == 'UNEXPECTED']
    record += [p['pid'] for p in probes if p['verdict'] == 'record']
    passed += [m['id'] for m in mutations if m['detected']]
    failed += [m['id'] + ' (undetected)' for m in mutations if not m['detected']]
    return {'passed': len(passed), 'failed': len(failed), 'record': len(record), 'failures': failed}


def single(args):
    reference = load_function(REF_PATH, REF_FUNC, 'reference')
    if args.reference_run:
        target, tpath, tfunc, mode = reference, REF_PATH, REF_FUNC, 'reference-run'
        baseline, bname = contract_literal, 'vectorized contract literal (harness inline)'
    else:
        tpath, tfunc, mode = os.path.abspath(args.module), args.func, 'module'
        target = load_function(tpath, tfunc, 'target')
        baseline, bname = reference, 'K2 loop reference'
    rec = Rec()
    cases, eos = build_A1()
    a1_fixture_checks(rec, cases, eos)
    run_A1(target, rec, cases, eos)
    run_A2(target, rec, baseline, bname)
    run_A3(target, rec)
    probes = run_A4(target, reference, scored=(mode == 'module'))
    mutations = run_A5(reference, cases, eos) if mode == 'reference-run' else []
    summary = summarize(rec, probes, mutations)
    meta = {'schema': 'k2v001_fixture_results', 'dispatch': '0448', 'role': 'Claude4 lane local helper K2 (implementation fixtures)',
            'mode': mode, 'label': args.label, 'python': sys.version.split()[0], 'executable': sys.executable,
            'numpy': np.__version__, 'machine': platform.machine(),
            'harness': {'path': os.path.abspath(__file__), 'sha256': sha256_file(os.path.abspath(__file__))},
            'reference': {'path': REF_PATH, 'sha256': sha256_file(REF_PATH), 'func': REF_FUNC},
            'target': {'path': tpath, 'sha256': sha256_file(tpath), 'func': tfunc},
            'a2_baseline': bname,
            'contract': {'path': CONTRACT_PATH, 'pinned_sha256': CONTRACT_SHA256,
                         'observed_sha256': (sha256_file(CONTRACT_PATH) if os.path.exists(CONTRACT_PATH) else None)},
            'tolerances': {'A1': RTOL_A1, 'A2': RTOL_A2, 'FD': RTOL_FD},
            'A4_scored': mode == 'module'}
    if args.source_of_copy:
        src = os.path.abspath(args.source_of_copy)
        with open(src, 'rb') as fa, open(tpath, 'rb') as fb:
            ident = fa.read() == fb.read()
        meta['source_of_copy'] = {'path': src, 'sha256': sha256_file(src), 'byte_identical_to_target': ident}
    result = dict(meta, summary=summary, checks=rec.items, probes=probes, mutations=mutations)
    write_json(args.out, result)
    return 0 if summary['failed'] == 0 else 1


def write_json(path, obj):
    text = json.dumps(J(obj), indent=1, allow_nan=False)
    if path == '-':
        sys.stdout.write(text + '\n')
        sys.stdout.flush()
    else:
        with open(path, 'w') as fh:
            fh.write(text + '\n')


def cross_compare(runs):
    keys = []
    for r in runs:
        res = r.get('result')
        if res is None:
            keys.append(None)
            continue
        keys.append({'checks': [(c['id'], c['status']) for c in res['checks']],
                     'probes': [(p['pid'], p['verdict'], p['accepted'], (p.get('exception') or {}).get('type'))
                                for p in res['probes']],
                     'mutations': [(m['id'], m['detected']) for m in res['mutations']],
                     'digests': [(c['id'], c['detail'].get('output_sha256')) for c in res['checks']
                                 if c['detail'].get('output_sha256')]})
    if len(keys) < 2 or any(k is None for k in keys):
        return {'compared': False}
    out = {'compared': True}
    for name in ('checks', 'probes', 'mutations', 'digests'):
        a, b = keys[0][name], keys[1][name]
        out[name + '_identical'] = a == b
        out[name + '_differences'] = [[x, y] for x, y in zip(a, b) if x != y][:20]
    return out


def multi(args):
    pys = [p.strip() for p in args.interpreters.split(',') if p.strip()]
    child = [os.path.abspath(__file__)]
    if args.reference_run:
        child.append('--reference-run')
    else:
        child += ['--module', os.path.abspath(args.module), '--func', args.func]
    if args.source_of_copy:
        child += ['--source-of-copy', os.path.abspath(args.source_of_copy)]
    env = dict(os.environ)
    env.update({'OMP_NUM_THREADS': '1', 'OPENBLAS_NUM_THREADS': '1', 'VECLIB_MAXIMUM_THREADS': '1'})
    runs, rc = [], 0
    for py in pys:
        cmd = [py, '-I', '-B'] + child + ['--out', '-', '--label', os.path.basename(py)]
        cp = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, timeout=900)
        entry = {'interpreter': py, 'command': cmd, 'returncode': cp.returncode,
                 'stderr_tail': cp.stderr.decode('utf-8', 'replace')[-3000:]}
        try:
            entry['result'] = json.loads(cp.stdout.decode('utf-8'))
        except ValueError as e:
            entry['result'] = None
            entry['parse_error'] = str(e)
            rc = 1
        if cp.returncode != 0:
            rc = 1
        runs.append(entry)
    merged = {'schema': 'k2v001_fixture_results_merged', 'dispatch': '0448',
              'harness_sha256': sha256_file(os.path.abspath(__file__)),
              'summaries': [{'interpreter': r['interpreter'], 'returncode': r['returncode'],
                             'python': (r['result'] or {}).get('python'), 'numpy': (r['result'] or {}).get('numpy'),
                             'summary': (r['result'] or {}).get('summary')} for r in runs],
              'cross_interpreter': cross_compare(runs), 'runs': runs}
    write_json(args.out, merged)
    return rc


def main(argv=None):
    ap = argparse.ArgumentParser(description='K2 fixtures for the 0448 kinematic density map review')
    ap.add_argument('--reference-run', action='store_true')
    ap.add_argument('--module')
    ap.add_argument('--func')
    ap.add_argument('--out', required=True)
    ap.add_argument('--interpreters')
    ap.add_argument('--source-of-copy')
    ap.add_argument('--label', default='')
    args = ap.parse_args(argv)
    if args.reference_run == bool(args.module):
        ap.error('give exactly one of --reference-run or --module PATH --func NAME')
    if args.module and not args.func:
        ap.error('--module requires --func')
    if args.interpreters:
        return multi(args)
    return single(args)


if __name__ == '__main__':
    sys.exit(main())
