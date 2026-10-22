#!/usr/bin/env python3
"""fixtures_n2v001.py -- N2 implementation fixtures, dispatch 0451 (Claude4 distinct review of 0450).

Synthetic analytic fixtures only: no project data, no project run, no field/parameter search.
Root contract ANNULAR_KNOT_RADIAL_CORRECTION_CHOICE_V001.json (sha 58ffcbb8...), scalar_design 1-6.
The pinned spline helper (owned_body_fitted_displacement_binding_v002.py, sha 87866875...) is loaded by
path for comparison only; only its _spline_matrices is called, on synthetic knots. The old scalar and
helicity modules are read as text (static-scan calibration) and never imported.
Independent expectation (not the helper, not another oracle): edge truth from the generator,
Thomas-solved natural cubic cardinal basis in power form, Bonnet Legendre recurrence, contract chain
rule, stacked dimensionless norms, exact true-outer xi_R rows, basis-free null-space projector.

  self-run : python3 -I -B fixtures_n2v001.py --self --out fixture_results_n2v001_self.json
  module   : python3 -I -B fixtures_n2v001.py --module PATH [--scalar-fn NAME] [--helicity-fn NAME]
             [--adapter PATH|c3v001] --out JSON
Adapter: 'c3v001' = built-in adapter for annular_knot_maps_c3v001.py (old_scalar_maps supplied by a
v001-convention input emulator written from the v001 text; caller tolerances 64*eps); or a .py file with any
of call_scalar(module, geom, ctx), call_helicity(module, scalar_result, geom, m, ctx),
normalize_scalar(result), normalize_helicity(result).
"""
import sys
sys.dont_write_bytecode = True
import argparse, ast, hashlib, importlib.util, inspect, json, os, platform, time, traceback
import numpy as np

REF = '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13'
HELPER_PATH = REF + '/helpers/coefficient_method/owned_body_fitted_displacement_binding_v002.py'
HELPER_SHA = '87866875f8a6883f62b778c123326f3c65090fdacae4fe8c79913e07b4405462'
OLD_SCALAR_PATH = REF + '/helpers/coefficient_method/owned_free_surface_32q8trial_maps_v001.py'
OLD_SCALAR_SHA = '3bd792bafcfc32f5e0ed9e7cc62bdfec67a3ec185bd80ce1981f90dbe30db943'
OLD_HEL_PATH = REF + '/helpers/coefficient_method/owned_32q8_regular_helicity_maps_v001.py'
OLD_HEL_SHA = '280149dc028260d865604948633bb8a1332c5ee01be916895c02df42e2b280c6'
CONTRACT_PATH = REF + '/CODEX1/ANNULAR_KNOT_RADIAL_CORRECTION_CHOICE_V001.json'
CONTRACT_SHA = '58ffcbb86cd6512bb02ddf384a593311d1a9483f73f0cd83633432a9f5ef073e'

NR, NZ, NA, NK, NL = 72, 32, 18, 19, 8          # radial nodes, z nodes, annuli, knots, Legendre 0..7
NT, NQ = NK*NL, NR*NZ                            # 152 trial columns, 2304 quadrature rows
NRED = 3*NT - NL                                 # 448 reduced coordinates
EPS = np.finfo(float).eps
GL4X, GL4W = np.polynomial.legendre.leggauss(4)
RANK_REL, RANK_ABS = 1e-12, 0.0                  # synthetic explicit hard-rank controls
TOL = dict(edge_abs=1e-13, map_rel=1e-12, trace_abs=1e-15, preserve_rel=1e-14, rootder_rel=1e-11,
           fd_rel=1e-6, fd_step_rel=1e-6, intrinsic_card_abs=1e-12, intrinsic_rel=1e-9,
           hard_residual=1e-13, ortho=1e-12, projector=1e-12, hel_map_rel=1e-11, norms_rel=1e-13,
           sv_rel=1e-12, outer_rel=1e-13, hel_fd_value_rel=1e-11)
HEL_MAPS = ('UR', 'UP', 'UZ', 'partial_R_UR', 'partial_R_UP', 'partial_R_UZ',
            'partial_z_UR', 'partial_z_UP', 'partial_z_UZ', 'divU')
REQ_SCALAR = ('value', 'partial_R', 'partial_z', 'weights_RdRdz', 'zeta', 'outer_coefficient_trace',
              'roots_m', 'root_radial_derivatives')
OPT_SCALAR = ('lower_surface_trace', 'upper_surface_trace', 'radial_derivative')
REQ_HEL = HEL_MAPS + ('status', 'raw_coefficient_transform', 'normalized_nullspace', 'hard_constraint_raw',
                      'column_norms', 'regularity_exponents')
OPT_HEL = ('hard_constraint_normalized', 'hard_singular_values', 'rank_threshold', 'inverse_column_norms',
           'hard_nullspace_residual', 'hard_nullspace_residual_norm', 'm', 'outer_radius_m')


# ----------------------------------------------------------------------------- utilities
def sha256_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def load_by_path(path, name, expect_sha=None):
    if expect_sha is not None and sha256_file(path) != expect_sha:
        raise RuntimeError('pin mismatch: ' + path)
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def relmax(a, b):
    a = np.asarray(a); b = np.asarray(b)
    if a.shape != b.shape:
        return float('inf')
    if a.size == 0:
        return 0.0
    scale = float(np.max(np.abs(b)))
    d = float(np.max(np.abs(a - b)))
    return d/scale if scale > 0 else d


def jsonable(x):
    if isinstance(x, dict):
        return {str(k): jsonable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [jsonable(v) for v in x]
    if isinstance(x, np.ndarray):
        return jsonable(x.tolist())
    if isinstance(x, (np.bool_,)):
        return bool(x)
    if isinstance(x, (np.integer,)):
        return int(x)
    if isinstance(x, (np.floating, float)):
        x = float(x)
        return x if np.isfinite(x) else repr(x)
    if isinstance(x, complex):
        return [x.real, x.imag]
    return x


class Report:
    def __init__(self):
        self.rows = []

    def add(self, group, check, ok, info=False, **metrics):
        row = dict(group=group, check=check, status='INFO' if info else ('PASS' if ok else 'FAIL'))
        for k, v in jsonable(metrics).items():
            row[('reported_' + k) if k in row else k] = v
        self.rows.append(row)

    def error(self, group, check, exc):
        self.rows.append(dict(group=group, check=check, status='ERROR',
                              error=(type(exc).__name__ + ': ' + str(exc))[:400]))

    def bad(self):
        return [r for r in self.rows if r['status'] in ('FAIL', 'ERROR')]

    def counts(self):
        out = {}
        for r in self.rows:
            out[r['status']] = out.get(r['status'], 0) + 1
        return out


# ----------------------------------------------------------------------------- independent expectation
def _thomas(sub, dia, sup, rhs):
    n = len(dia); cp = np.zeros(n); dp = np.zeros(rhs.shape)
    cp[0] = sup[0]/dia[0] if n > 1 else 0.0
    dp[0] = rhs[0]/dia[0]
    for i in range(1, n):
        den = dia[i] - sub[i]*cp[i-1]
        cp[i] = sup[i]/den if i < n-1 else 0.0
        dp[i] = (rhs[i] - sub[i]*dp[i-1])/den
    x = np.zeros(rhs.shape); x[-1] = dp[-1]
    for i in range(n-2, -1, -1):
        x[i] = dp[i] - cp[i]*x[i+1]
    return x


class Cardinal:
    """Own natural cubic cardinal basis on knots x: S_j(x_k)=delta_jk, S''=0 at both ends.
    Second derivatives from a Thomas tridiagonal solve; power-form evaluation (not the helper's form)."""

    def __init__(self, knots):
        x = np.asarray(knots, float); n = x.size; h = np.diff(x)
        if x.ndim != 1 or n < 3 or not np.all(h > 0):
            raise ValueError('strictly increasing knots required')
        m = n - 2; sub = np.zeros(m); dia = np.zeros(m); sup = np.zeros(m); rhs = np.zeros((m, n))
        for r in range(m):
            k = r + 1
            sub[r] = h[k-1]; dia[r] = 2*(h[k-1] + h[k]); sup[r] = h[k]
            rhs[r, k-1] = 6/h[k-1]; rhs[r, k] = -6/h[k-1] - 6/h[k]; rhs[r, k+1] = 6/h[k]
        M = np.zeros((n, n)); M[1:-1] = _thomas(sub, dia, sup, rhs)   # M[k, j] = S_j''(x_k)
        self.x, self.h, self.M, self.n = x, h, M, n

    def eval(self, q, d=0):
        q = np.atleast_1d(np.asarray(q, float))
        k = np.clip(np.searchsorted(self.x, q, side='right') - 1, 0, self.n - 2)
        t = (q - self.x[k])[:, None]; h = self.h[k][:, None]; Y = np.eye(self.n)
        y0, y1, M0, M1 = Y[k], Y[k+1], self.M[k], self.M[k+1]
        b = (y1 - y0)/h - h*(2*M0 + M1)/6
        if d == 0:
            out = y0 + b*t + M0*t*t/2 + (M1 - M0)*t**3/(6*h)
            hit = np.flatnonzero(q == self.x[-1])
            if hit.size:
                out[hit] = Y[-1]          # cardinal definition at the last knot
            return out
        if d == 1:
            return b + M0*t + (M1 - M0)*t*t/(2*h)
        if d == 2:
            return M0 + (M1 - M0)*t/h
        raise ValueError('d')


def legendre_own(x, deg=NL-1):
    """Bonnet recurrence P_n and P_n' (independent of numpy.polynomial.legendre)."""
    x = np.asarray(x, float)
    P = np.zeros(x.shape + (deg + 1,)); D = np.zeros_like(P)
    P[..., 0] = 1.0
    if deg >= 1:
        P[..., 1] = x; D[..., 1] = 1.0
    for n in range(1, deg):
        P[..., n+1] = ((2*n + 1)*x*P[..., n] - n*P[..., n-1])/(n + 1)
        D[..., n+1] = D[..., n-1] + (2*n + 1)*P[..., n]
    return P, D


SHAPES = {  # dimensionless center(s)/L and height(s)/L; h>0 and |c|<h on [0,1]
    'linear': (lambda s: 0.004 + 0.012*s, lambda s: 0.06 - 0.025*s),
    'smooth': (lambda s: 0.006*np.sin(2.3*s + 0.4) + 0.004*s*s,
               lambda s: 0.05 + 0.015*np.cos(1.7*s) - 0.012*s**3),
}


def nodes_from_intervals(lo, hi, L):
    lo = np.asarray(lo, float); hi = np.asarray(hi, float); c = (lo + hi)/2; h = (hi - lo)/2
    s = (c[:, None] + h[:, None]*GL4X[None, :]).reshape(-1)
    return dict(R=L*np.sqrt(s), wr=((L*L/2)*h[:, None]*GL4W[None, :]).reshape(-1), s_true=s)


def make_geometry(*, name, seed, L, shape, z_rule):
    """18 random annuli 0=s0<...<s18=1 in s=(R/L)^2; 4-point GL in s per annulus; R dR weights
    (L^2/2)(b-a)/2 W_i (sum L^2/2); roots from smooth center/height; 32 z nodes per column."""
    rng = np.random.default_rng(seed)
    w = rng.uniform(1.0, 3.0, NA); w = w/np.sum(w)
    edges = np.concatenate(([0.0], np.cumsum(w))); edges[-1] = 1.0
    nd = nodes_from_intervals(edges[:-1], edges[1:], L)
    cf, hf = SHAPES[shape]
    center = L*cf(nd['s_true']); height = L*hf(nd['s_true'])
    roots = np.stack((center - height, center + height), axis=1)
    if z_rule == 'split':                       # two 16-point GL panels split at random t_i
        x16, w16 = np.polynomial.legendre.leggauss(16); t = rng.uniform(-0.3, 0.3, NR)
        zeta = np.empty((NR, NZ)); wz = np.empty((NR, NZ))
        for i in range(NR):
            for p, (al, be) in enumerate(((-1.0, t[i]), (t[i], 1.0))):
                zeta[i, 16*p:16*p+16] = (al + be)/2 + (be - al)/2*x16
                wz[i, 16*p:16*p+16] = height[i]*(be - al)/2*w16
    else:                                       # plain 32-point GL
        x32, w32 = np.polynomial.legendre.leggauss(32)
        zeta = np.broadcast_to(x32, (NR, NZ)).copy(); wz = height[:, None]*w32[None, :]
    z = center[:, None] + height[:, None]*zeta
    return dict(name=name, seed=seed, L=float(L), shape=shape, z_rule=z_rule, edges=edges,
                R=nd['R'], wr=nd['wr'], s_true=nd['s_true'], roots=roots, z=z, wz=wz)


def probe_geometries(g):
    """Not-recoverable / malformed inputs; the scalar build must raise (fail closed)."""
    L, R, wr, e = g['L'], g['R'], g['wr'], g['edges']
    out = []

    def var(label, **kw):
        d = dict(g); d.update({k: v for k, v in kw.items() if k != 's_true'}); d['name'] = g['name'] + ':' + label
        out.append((label, d))
    R1 = R.copy(); R1[4*9+1] *= 1 + 1e-9; var('node_inner_rel1e-9', R=R1)
    R1 = R.copy(); R1[4*9+3] *= 1 + 1e-9; var('node_outer_rel1e-9', R=R1)
    w1 = wr.copy(); w1[4*9+2] *= 1 + 1e-9; var('weight_one_rel1e-9', wr=w1)
    w1 = wr.copy(); d = wr[4*9+2]*1e-9; w1[4*9+2] += d; w1[4*12+1] -= d
    var('weight_pair_sum_preserving_1e-9', wr=w1)
    e1 = e.copy(); e1[0] = 1e-9; var('s0_eq_1e-9', **nodes_from_intervals(e1[:-1], e1[1:], L))
    e1 = e.copy(); e1[-1] = 1 - 1e-9; var('s18_eq_1m1e-9', **nodes_from_intervals(e1[:-1], e1[1:], L))
    e1 = e - 1e-9; var('all_edges_shift_m1e-9_exact_measure', **nodes_from_intervals(e1[:-1], e1[1:], L))
    lo, hi = e[:-1].copy(), e[1:].copy(); hi[8] += 1e-7; lo[12] += 1e-7
    var('overlap_g8_gap_g12_1e-7_sum_preserving', **nodes_from_intervals(lo, hi, L))
    lo, hi = e[:-1].copy(), e[1:].copy(); hi[8] += 1e-7
    var('overlap_g8_1e-7', **nodes_from_intervals(lo, hi, L))
    idx = np.arange(NR); idx[20:24], idx[24:28] = np.arange(24, 28), np.arange(20, 24)
    var('unordered_swap_groups5_6', R=R[idx], wr=wr[idx])
    idx = np.arange(NR); idx[28:32] = idx[28:32][::-1]
    var('unordered_reverse_within_group7', R=R[idx], wr=wr[idx])
    Ra, Rb = L*np.sqrt(e[:-1]), L*np.sqrt(e[1:])
    Rn = ((Ra + Rb)/2)[:, None] + ((Rb - Ra)/2)[:, None]*GL4X[None, :]
    var('gl_in_R_not_in_s_exact_measure', R=Rn.reshape(-1), wr=(Rn*((Rb - Ra)/2)[:, None]*GL4W[None, :]).reshape(-1))
    var('outer_radius_mismatch_rel1e-9', L=L*(1 + 1e-9))
    var('nodes68_drop_last_group', R=R[:68], wr=wr[:68], roots=g['roots'][:68], z=g['z'][:68], wz=g['wz'][:68])
    return out


def expectation_scalar(g):
    """Independent expected scalar maps for contract items 1-4 (own spline, own Legendre)."""
    L, R, wr, roots, z, wz = g['L'], g['R'], g['wr'], g['roots'], g['z'], g['wz']
    s = (R/L)**2
    C = Cardinal(g['edges'])                                   # ground-truth edges from generator
    Bv = C.eval(s, 0); Bs = C.eval(s, 1); BR = (2*R/L**2)[:, None]*Bs
    center = 0.5*(roots[:, 0] + roots[:, 1]); height = 0.5*(roots[:, 1] - roots[:, 0])
    DRg = (2*R/L**2)[:, None]*Cardinal(s).eval(s, 1)           # old 72-node geometry convention
    cR, hR = DRg @ center, DRg @ height
    zeta = (z - center[:, None])/height[:, None]
    P, dP = legendre_own(zeta)
    chain = (cR[:, None] + zeta*hR[:, None])/height[:, None]
    V = np.einsum('ij,ila->ilja', Bv, P).reshape(NQ, NT)
    VR = (np.einsum('ij,ila->ilja', BR, P) - np.einsum('ij,ila->ilja', Bv, dP*chain[:, :, None])).reshape(NQ, NT)
    VZ = np.einsum('ij,ila->ilja', Bv, dP/height[:, None, None]).reshape(NQ, NT)
    e18 = np.zeros(NK); e18[-1] = 1.0
    return dict(V=V, VR=VR, VZ=VZ, Bv=Bv, Bs=Bs, BR=BR, DRg=DRg, cR=cR, hR=hR, center=center, height=height,
                zeta=zeta, T=np.kron(e18[None, :], np.eye(NL)), weights=(wr[:, None]*wz).reshape(-1),
                rootder=np.stack((cR - hR, cR + hR), axis=-1),
                lower=np.kron(Bv, ((-1.0)**np.arange(NL))[None, :]), upper=np.kron(Bv, np.ones((1, NL))),
                chain_term_rel=float(np.max(np.abs(np.einsum('ij,ila->ilja', Bv, dP*chain[:, :, None])))/np.max(np.abs(VR))))


def expected_helicity_raw(exp, g, m):
    """Independent pre-QR helicity maps: exponents |m+1|,|m-1|,|m|; d/dR (R/L)^e = e(R/L)^(e-1)/L;
    norms of literally stacked dimensionless (UR/L, UP/L, UZ/L) per raw unit coefficient;
    true-outer xi_R/L=(p+q)/2 at R=L with exact cardinal row e_18; projector onto null(B)."""
    L = g['L']; rr = np.repeat(g['R'], NZ)
    ex = (abs(m + 1), abs(m - 1), abs(m))
    pw = [(rr/L)**e for e in ex]
    dpw = [e*(rr/L)**(e - 1)/L if e > 0 else np.zeros_like(rr) for e in ex]
    vals = [p[:, None]*exp['V'] for p in pw]
    rad = [p[:, None]*exp['VR'] + dp[:, None]*exp['V'] for p, dp in zip(pw, dpw)]
    ver = [p[:, None]*exp['VZ'] for p in pw]
    norms = []
    for blk, v in enumerate(vals):
        if blk == 0:
            UR, UP, UZ = v/2, v/(2j), 0*v
        elif blk == 1:
            UR, UP, UZ = v/2, -v/(2j), 0*v
        else:
            UR, UP, UZ = 0*v, 0*v, v
        norms.append(np.sqrt(np.sum(np.abs(UR)**2 + np.abs(UP)**2 + np.abs(UZ)**2, axis=0)))
    norms = np.concatenate(norms)
    T = exp['T']
    Braw = np.concatenate((0.5*T, 0.5*T, np.zeros((NL, NT))), axis=1)
    B = Braw/norms[None, :]
    Pnull = np.eye(3*NT) - B.T @ np.linalg.solve(B @ B.T, B)
    return dict(exponents=list(ex), vals=vals, rad=rad, ver=ver, norms=norms, Braw=Braw, B=B, Pnull=Pnull,
                sv=np.linalg.svd(B, compute_uv=False))


def maps_from_transform(raw, Tm, L, m, rr):
    Pp, Mm, Vv = Tm[:NT], Tm[NT:2*NT], Tm[2*NT:]
    out = {}
    for prefix, parts in (('U', raw['vals']), ('partial_R_U', raw['rad']), ('partial_z_U', raw['ver'])):
        p = parts[0] @ Pp; q = parts[1] @ Mm
        out[prefix + 'R'] = (L/2)*(p + q); out[prefix + 'P'] = (L/(2j))*(p - q); out[prefix + 'Z'] = L*(parts[2] @ Vv)
    out['divU'] = out['partial_R_UR'] + out['UR']/rr[:, None] + 1j*m*out['UP']/rr[:, None] + out['partial_z_UZ']
    return out


class Analytic:
    """Analytic V(R,z)=B_j(s(R)) P_a((z-c(R))/h(R)) at arbitrary points. B: own cardinal spline on the
    generator edges. Geometry mode 'spline': natural cubic in s through the 72 node values (the preserved
    old convention, so its derivative at nodes equals the pinned root derivative); 'analytic': generator."""

    def __init__(self, g):
        self.g = g; self.L = g['L']; s = (g['R']/self.L)**2
        self.B = Cardinal(g['edges']); self.G = Cardinal(s)
        r = g['roots']; self.c = 0.5*(r[:, 0] + r[:, 1]); self.h = 0.5*(r[:, 1] - r[:, 0])

    def geom(self, Rq, mode):
        sq = (Rq/self.L)**2
        if mode == 'spline':
            W = self.G.eval(sq, 0); return W @ self.c, W @ self.h
        cf, hf = SHAPES[self.g['shape']]
        return self.L*cf(sq), self.L*hf(sq)

    def V(self, Rq, zq, mode='spline'):
        Bq = self.B.eval((Rq/self.L)**2, 0); c, h = self.geom(Rq, mode)
        P, _ = legendre_own((zq - c)/h)
        return np.einsum('nj,na->nja', Bq, P).reshape(len(Rq), -1)


# ----------------------------------------------------------------------------- reference implementation
def recover_edges_ref(s, wr, L, *, tol_s=64*EPS, tol_w=64*EPS, check_weights=True):
    s = np.asarray(s, float); wr = np.asarray(wr, float)
    if s.shape != (NR,) or wr.shape != (NR,) or np.any(np.diff(s) <= 0):
        raise ValueError('ordered 72 radial nodes required')
    G = s.reshape(NA, 4); c = G.mean(axis=1); h = (G @ GL4X)/np.dot(GL4X, GL4X)
    if np.any(h <= 0) or np.max(np.abs(c[:, None] + h[:, None]*GL4X[None, :] - G)) > tol_s:
        raise ValueError('not a four-point GL group in s')
    lo, hi = c - h, c + h
    if np.max(np.abs(hi[:-1] - lo[1:])) > tol_s:
        raise ValueError('adjacent annulus edges disagree')
    if abs(lo[0]) > tol_s or abs(hi[-1] - 1) > tol_s:
        raise ValueError('s0=0 / s18=1 not met')
    if check_weights:
        ew = (L*L/2)*(h[:, None]*GL4W[None, :]).reshape(-1)
        if np.max(np.abs(wr - ew)/ew) > tol_w:
            raise ValueError('R dR weights disagree')
    return np.concatenate(([0.0], 0.5*(hi[:-1] + lo[1:]), [1.0]))


def ref_scalar_build(*, radial_nodes_m, radial_RdR_weights_m2, radial_domain_m, roots_m, z_nodes_m,
                     z_weights_m, spline='own', helper=None, mutation=None):
    R = np.asarray(radial_nodes_m, float); wr = np.asarray(radial_RdR_weights_m2, float)
    roots = np.asarray(roots_m, float); z = np.asarray(z_nodes_m, float); wz = np.asarray(z_weights_m, float)
    lo, L = map(float, radial_domain_m)
    if R.shape != (NR,) or wr.shape != R.shape or roots.shape != (NR, 2) or z.shape != (NR, NZ) or wz.shape != z.shape:
        raise ValueError('72x32 geometry required')
    if lo != 0 or not L > R[-1] or R[0] <= 0 or np.any(wr <= 0) or np.any(wz <= 0):
        raise ValueError('full-domain positive quadrature required')
    if mutation == 'sorts_input':                 # 'guessing': silently reorder every column array
        o = np.argsort(R); R, wr, roots, z, wz = R[o], wr[o], roots[o], z[o], wz[o]
    if np.any(np.diff(R) <= 0):
        raise ValueError('ordered radial nodes required')
    s = (R/L)**2
    if mutation == 'knots_equal_nodes':
        knots = s
    else:
        knots = recover_edges_ref(s, wr, L, tol_s=1e-6 if mutation == 'edge_tol_loose' else 64*EPS,
                                  check_weights=mutation != 'no_weight_check')
    nk = knots.size
    if spline == 'helper':
        tr, Ds = helper._spline_matrices(knots, list(s) + [0.0, 1.0]); Bv, Bs, tout = tr[:NR], Ds[:NR], tr[-1]
        Dg = helper._spline_matrices(s, list(s) + [0.0, 1.0])[1][:NR]
    else:
        C = Cardinal(knots); Bv, Bs, tout = C.eval(s, 0), C.eval(s, 1), C.eval([1.0], 0)[0]
        Dg = Cardinal(s).eval(s, 1)
    if mutation == 'outer_trace_last_node':
        tout = Bv[-1]
    BR = Bs if mutation == 'missing_2R_over_L2' else (2*R/L**2)[:, None]*Bs
    center = np.mean(roots, axis=1); height = (roots[:, 1] - roots[:, 0])/2
    DRg = (2*R/L**2)[:, None]*Dg; cR, hR = DRg @ center, DRg @ height
    if mutation == 'root_derivs_zero':
        cR, hR = 0*cR, 0*hR
    zeta = (z - center[:, None])/height[:, None]
    P, dP = legendre_own(zeta)
    sign = 1.0 if mutation == 'zeta_chain_sign' else -1.0
    chain = (cR[:, None] + zeta*hR[:, None])/height[:, None]
    V = np.einsum('ij,ila->ilja', Bv, P).reshape(NQ, nk*NL)
    VR = (np.einsum('ij,ila->ilja', BR, P) + sign*np.einsum('ij,ila->ilja', Bv, dP*chain[:, :, None])).reshape(NQ, nk*NL)
    VZ = np.einsum('ij,ila->ilja', Bv, dP/height[:, None, None]).reshape(NQ, nk*NL)
    arrays = dict(value=V, partial_R=VR, partial_z=VZ, weights_RdRdz=(wr[:, None]*wz).reshape(-1), zeta=zeta,
                  outer_coefficient_trace=np.kron(np.asarray(tout)[None, :], np.eye(NL)),
                  lower_surface_trace=np.kron(Bv, ((-1.0)**np.arange(NL))[None, :]),
                  upper_surface_trace=np.kron(Bv, np.ones((1, NL))), radial_derivative=BR, roots_m=roots,
                  root_radial_derivatives=np.stack((cR - hR, cR + hR), axis=-1))
    return dict(arrays=arrays, trial_shape=[nk, NL], quadrature_shape=[NR, NZ], recovered_edges_s=knots)


def ref_helicity_build(*, scalar_maps, radial_nodes_m, outer_radius_m, m, rank_relative_tolerance,
                       rank_absolute_tolerance, mutation=None):
    if type(m) is not int or not 1 <= m <= 6:
        raise ValueError('modes 1..6 only')
    L = float(outer_radius_m); R = np.asarray(radial_nodes_m, float)
    nk, nd = scalar_maps['trial_shape']; ns = nk*nd
    a = scalar_maps['arrays']; V, VR, VZ, T = a['value'], a['partial_R'], a['partial_z'], a['outer_coefficient_trace']
    rr = np.repeat(R, NZ)
    ex = (abs(m - 1), abs(m + 1), abs(m)) if mutation == 'exponents_swapped' else (abs(m + 1), abs(m - 1), abs(m))
    f = [(rr/L)**e for e in ex]; vals = [fi[:, None]*V for fi in f]
    tw = 1.0 if mutation == 'norm_unhalved' else 0.5
    norms = np.concatenate([np.sqrt(tw*np.sum(vals[0]**2, axis=0)), np.sqrt(tw*np.sum(vals[1]**2, axis=0)),
                            np.sqrt(np.sum(vals[2]**2, axis=0))])
    inv = 1/norms
    Braw = np.concatenate((.5*T, .5*T, np.zeros_like(T)), axis=1)
    if mutation == 'lid_added':
        lid = np.concatenate([np.kron(np.eye(nk), np.ones((1, nd))), np.kron(np.eye(nk), ((-1.0)**np.arange(nd))[None, :])])
        Braw = np.concatenate((Braw, np.concatenate((np.zeros((2*nk, 2*ns)), lid), axis=1)))
    B = Braw*inv[None, :]
    sv = np.linalg.svd(B, compute_uv=False); thr = float(rank_absolute_tolerance + rank_relative_tolerance*sv[0])
    common = dict(m=m, hard_constraint_raw=Braw, hard_constraint_normalized=B, hard_singular_values=sv,
                  rank_threshold=thr, column_norms=norms, inverse_column_norms=inv, regularity_exponents=list(ex),
                  outer_radius_m=L)
    if sv[-1] <= thr:
        return dict(status='UNRESOLVED_OUTER_CONSTRAINT_RANK', **common)
    Q, _ = np.linalg.qr(B.T, mode='complete'); Z = Q[:, B.shape[0]:]
    rt = inv[:, None]*Z
    blocks = (slice(0, 576), slice(576, 1152), slice(1152, None)) if mutation == 'slice_576_left' else \
        (slice(0, ns), slice(ns, 2*ns), slice(2*ns, None))
    rt2 = rt
    if mutation == 'derivative_transform_differs':
        Qr, _ = np.linalg.qr(np.random.default_rng(7).standard_normal((Z.shape[1], Z.shape[1]))); rt2 = rt @ Qr
    maps = {}

    def transform(parts, prefix, t):
        p = parts[0] @ t[blocks[0]]; q = parts[1] @ t[blocks[1]]
        maps[prefix + 'R'] = (L/2)*(p + q); maps[prefix + 'P'] = (L/(2j))*(p - q); maps[prefix + 'Z'] = L*(parts[2] @ t[blocks[2]])
    transform(vals, 'U', rt)
    transform([fi[:, None]*VR + (e/rr)[:, None]*v for e, fi, v in zip(ex, f, vals)], 'partial_R_U', rt2)
    transform([fi[:, None]*VZ for fi in f], 'partial_z_U', rt2)
    div = maps['partial_R_UR'] + maps['UR']/rr[:, None] + (1j*m)*maps['UP']/rr[:, None] + maps['partial_z_UZ']
    hres = B @ Z
    return dict(status='REGULAR_HELICITY_MAPS', **common, **maps, divU=div, normalized_nullspace=Z,
                raw_coefficient_transform=rt, hard_nullspace_residual=hres,
                hard_nullspace_residual_norm=float(np.linalg.norm(hres)))


class RefImpl:
    def __init__(self, mutation=None, spline='own', helper=None):
        self.mutation, self.spline, self.helper = mutation, spline, helper
        self.name = 'reference(' + spline + ')' + ('' if mutation is None else ' mutation=' + mutation)

    def scalar(self, g):
        return ref_scalar_build(radial_nodes_m=g['R'], radial_RdR_weights_m2=g['wr'], radial_domain_m=(0.0, g['L']),
                                roots_m=g['roots'], z_nodes_m=g['z'], z_weights_m=g['wz'], spline=self.spline,
                                helper=self.helper, mutation=self.mutation)

    def helicity(self, sres, g, m, rank_relative_tolerance=RANK_REL, rank_absolute_tolerance=RANK_ABS):
        return ref_helicity_build(scalar_maps=sres, radial_nodes_m=g['R'], outer_radius_m=g['L'], m=m,
                                  rank_relative_tolerance=rank_relative_tolerance,
                                  rank_absolute_tolerance=rank_absolute_tolerance, mutation=self.mutation)


# ----------------------------------------------------------------------------- target-module adapter
class AdapterError(RuntimeError):
    pass


def v001_convention_old_maps(g, helper):
    """Adapter input emulator: the dict v001 build() returns (owned_free_surface_32q8trial_maps_v001.py
    L17-38), written from its text -- the v001 module is NOT imported -- with the pinned helper spline used
    exactly as v001 L19-21. No v001 input validation here, so malformed probes reach the target's checks."""
    R = np.asarray(g['R'], float); wr = np.asarray(g['wr'], float); roots = np.asarray(g['roots'], float)
    z = np.asarray(g['z'], float); wz = np.asarray(g['wz'], float); outer = float(g['L']); n = R.size
    center = np.mean(roots, axis=1); height = (roots[:, 1] - roots[:, 0])/2
    trace, Ds = helper._spline_matrices((R/outer)**2, list((R/outer)**2) + [0., 1.])
    DR = (2*R/outer**2)[:, None]*Ds[:n]
    center_R = np.einsum('ij,j->i', DR, center, optimize=False); height_R = np.einsum('ij,j->i', DR, height, optimize=False)
    zeta = (z - center[:, None])/height[:, None]
    P = np.polynomial.legendre.legvander(zeta, 7)
    dP = np.stack([np.polynomial.legendre.legval(zeta, np.polynomial.legendre.legder(np.eye(8)[a])) for a in range(8)], axis=-1)
    V = np.zeros((n, NZ, n, NL)); VR = np.zeros_like(V); VZ = np.zeros_like(V)
    for i in range(n):
        V[i, :, i, :] = P[i]
        VR[i] = np.einsum('j,la->lja', DR[i], P[i], optimize=False)
        VR[i, :, i, :] -= dP[i]*(center_R[i] + zeta[i, :, None]*height_R[i])/height[i]
        VZ[i, :, i, :] = dP[i]/height[i]
    arrays = dict(value=V.reshape(n*NZ, n*NL), partial_R=VR.reshape(n*NZ, n*NL), partial_z=VZ.reshape(n*NZ, n*NL),
                  weights_RdRdz=(wr[:, None]*wz).reshape(-1), zeta=zeta,
                  outer_coefficient_trace=np.kron(trace[-1][None, :], np.eye(NL)),
                  lower_surface_trace=np.kron(np.eye(n), ((-1.)**np.arange(NL))[None, :]),
                  upper_surface_trace=np.kron(np.eye(n), np.ones((1, NL))), radial_derivative=DR, roots_m=roots,
                  root_radial_derivatives=np.stack((center_R - height_R, center_R + height_R), axis=-1))
    return dict(arrays=arrays, trial_shape=[n, NL], quadrature_shape=[n, NZ])


class BuiltinC3v001Adapter:
    """Keyword API of annular_knot_maps_c3v001.py (INTERFACE_0450_V001.md). Caller tolerances: roundoff."""
    EDGE_TOL = 64*EPS
    WEIGHT_TOL = 64*EPS

    def old_maps(self, g, ctx):
        try:
            return v001_convention_old_maps(g, ctx['helper'])
        except Exception as exc:  # noqa: BLE001
            raise AdapterError('v001-convention input emulator failed: ' + type(exc).__name__ + ': ' + str(exc)[:120])

    def call_scalar(self, mod, g, ctx, old=None, **override):
        kw = dict(old_scalar_maps=self.old_maps(g, ctx) if old is None else old, old_scalar_map_sha256=OLD_SCALAR_SHA,
                  radial_nodes_m=g['R'], radial_RdR_weights_m2=g['wr'], outer_radius_m=g['L'],
                  binding_module=ctx['helper'], binding_module_sha256=HELPER_SHA,
                  edge_absolute_tolerance=self.EDGE_TOL, weight_relative_tolerance=self.WEIGHT_TOL)
        kw.update(override)
        return mod.build_annular_scalar_maps(**kw)

    def call_helicity(self, mod, sres, g, m, ctx):
        return mod.build_annular_regular_helicity_maps(
            scalar_maps=sres, radial_nodes_m=g['R'], outer_radius_m=g['L'], m=m,
            rank_relative_tolerance=ctx['rank_relative_tolerance'], rank_absolute_tolerance=ctx['rank_absolute_tolerance'])


def c3v001_custody_probes(rep, impl, g):
    """Target-specific: tampered/mismatched v001 custody inputs must raise (preserved geometry never guessed).
    The last probe is a v001-VALID packet (z-weight column sum 2h(1+5e-13), inside v001's rtol 1e-12)."""
    G = 'F-preserve'; ad = impl.adapter; ctx = impl.ctx
    base = ad.old_maps(g, ctx)

    def tampered(key, fn):
        o = dict(base); a = dict(base['arrays']); a[key] = fn(np.array(a[key], copy=True)); o['arrays'] = a
        return o

    def bump(a, idx, rel):
        a[idx] = a[idx]*(1 + rel); return a
    cases = [('root_radial_derivatives_1ulp', dict(old=tampered('root_radial_derivatives', lambda a: (a.__setitem__((5, 0), np.nextafter(a[5, 0], np.inf)), a)[1]))),
             ('value_block_entry_1ulp', dict(old=tampered('value', lambda a: (a.__setitem__((7*NZ + 3, 7*NL + 2), np.nextafter(a[7*NZ + 3, 7*NL + 2], np.inf)), a)[1]))),
             ('weights_RdRdz_entry_rel1e-9', dict(old=tampered('weights_RdRdz', lambda a: bump(a, 100, 1e-9)))),
             ('old_scalar_map_sha_wrong', dict(old_scalar_map_sha256='0'*64)),
             ('binding_sha_wrong', dict(binding_module_sha256='0'*64)),
             ('edge_tolerance_missing_None', dict(edge_absolute_tolerance=None))]
    for label, kw in cases:
        try:
            ad.call_scalar(impl.mod, g, ctx, **kw)
            rep.add(G, g['name'] + ':custody_failclosed:' + label, False, raised=False)
        except AdapterError as exc:
            rep.error(G, g['name'] + ':custody_failclosed:' + label, exc)
        except Exception as exc:  # noqa: BLE001
            rep.add(G, g['name'] + ':custody_failclosed:' + label, True, raised=(type(exc).__name__ + ': ' + str(exc))[:160])
    try:
        sres = ad.call_scalar(impl.mod, g, ctx)
        rep.add(G, g['name'] + ':module_edge_recovery_diagnostics', True, info=True,
                **{k: v for k, v in sres.get('edge_recovery', {}).items() if k not in ('gl_nodes', 'gl_weights')})
        R1 = g['R'].copy(); R1[40] = np.nextafter(R1[40], np.inf)
        for label, gg in (('helicity_R_differs_1ulp', dict(g, R=R1)), ('helicity_L_differs_rel1e-12', dict(g, L=g['L']*(1 + 1e-12)))):
            try:
                ad.call_helicity(impl.mod, sres, gg, 1, ctx)
                rep.add('F-helicity', g['name'] + ':input_mismatch_failclosed:' + label, False, raised=False)
            except Exception as exc:  # noqa: BLE001
                rep.add('F-helicity', g['name'] + ':input_mismatch_failclosed:' + label, True,
                        raised=(type(exc).__name__ + ': ' + str(exc))[:160])
    except Exception as exc:  # noqa: BLE001
        rep.error(G, g['name'] + ':module_edge_recovery_diagnostics', exc)
    g2 = dict(g); wz = g['wz'].copy(); wz[11] *= 1 + 5e-13; g2['wz'] = wz
    v001_ok = bool(np.allclose(np.sum(wz, axis=1), 2*(g['roots'][:, 1] - g['roots'][:, 0])/2, rtol=1e-12, atol=0))
    try:
        ad.call_scalar(impl.mod, g2, ctx)
        rep.add(G, g['name'] + ':v001_valid_zweight_sum_5e-13', True, info=True, v001_check_passes=v001_ok, raised=False)
    except Exception as exc:  # noqa: BLE001
        rep.add(G, g['name'] + ':v001_valid_zweight_sum_5e-13', True, info=True, v001_check_passes=v001_ok,
                raised=(type(exc).__name__ + ': ' + str(exc))[:160], weight_relative_tolerance_passed=ad.WEIGHT_TOL,
                note='weight_relative_tolerance also gates the 32-term column-sum custody check')


def bind_kwargs(fn, cand):
    kw = {}; missing = []
    for name, p in inspect.signature(fn).parameters.items():
        if p.kind in (p.VAR_POSITIONAL, p.VAR_KEYWORD):
            continue
        if name in cand:
            kw[name] = cand[name]
        elif p.default is p.empty:
            missing.append(name)
    if missing:
        raise AdapterError('unmapped required parameters ' + repr(missing) + '; supply --adapter')
    return kw


class TargetImpl:
    def __init__(self, path, scalar_fn, helicity_fn, adapter_path, helper):
        self.path = os.path.abspath(path); self.sha = sha256_file(self.path); self.helper = helper
        self.mod = load_by_path(self.path, 'n2_target_' + self.sha[:8])
        if adapter_path == 'c3v001':
            self.adapter = BuiltinC3v001Adapter()
        else:
            self.adapter = load_by_path(adapter_path, 'n2_adapter') if adapter_path else None
        fns = {k: v for k, v in vars(self.mod).items() if inspect.isfunction(v) and v.__module__ == self.mod.__name__}

        def pick(given, word):
            if given:
                return getattr(self.mod, given)
            c = [k for k in fns if word in k.lower() and not k.startswith('_')]
            return fns[c[0]] if len(c) == 1 else None
        self.sfn = pick(scalar_fn, 'scalar'); self.hfn = pick(helicity_fn, 'helicity')
        self.ctx = dict(helper=helper, helper_path=HELPER_PATH, module_sha256=self.sha, module_path=self.path,
                        rank_relative_tolerance=RANK_REL, rank_absolute_tolerance=RANK_ABS)
        self.name = 'target ' + os.path.basename(self.path) + ' sha ' + self.sha

    def _norm(self, hook, res):
        if self.adapter is not None and hasattr(self.adapter, hook):
            return getattr(self.adapter, hook)(res)
        return res

    def scalar(self, g):
        if self.adapter is not None and hasattr(self.adapter, 'call_scalar'):
            return self._norm('normalize_scalar', self.adapter.call_scalar(self.mod, g, self.ctx))
        if self.sfn is None:
            raise AdapterError('scalar function not identified; pass --scalar-fn')
        cand = dict(radial_nodes_m=g['R'], radial_RdR_weights_m2=g['wr'], radial_domain_m=(0.0, g['L']),
                    roots_m=g['roots'], z_nodes_m=g['z'], z_weights_m=g['wz'], outer_radius_m=g['L'],
                    binding_module=self.helper, spline_module=self.helper, spline_helper=self.helper,
                    binding_module_path=HELPER_PATH, spline_helper_path=HELPER_PATH, helper_path=HELPER_PATH)
        return self._norm('normalize_scalar', self.sfn(**bind_kwargs(self.sfn, cand)))

    def helicity(self, sres, g, m, rank_relative_tolerance=RANK_REL, rank_absolute_tolerance=RANK_ABS):
        if self.adapter is not None and hasattr(self.adapter, 'call_helicity'):
            ctx = dict(self.ctx, rank_relative_tolerance=rank_relative_tolerance,
                       rank_absolute_tolerance=rank_absolute_tolerance)
            return self._norm('normalize_helicity', self.adapter.call_helicity(self.mod, sres, g, m, ctx))
        if self.hfn is None:
            raise AdapterError('helicity function not identified; pass --helicity-fn')
        cand = dict(scalar_maps=sres, radial_nodes_m=g['R'], outer_radius_m=g['L'], m=m,
                    rank_relative_tolerance=rank_relative_tolerance, rank_absolute_tolerance=rank_absolute_tolerance,
                    scalar_map_sha256=self.sha)
        return self._norm('normalize_helicity', self.hfn(**bind_kwargs(self.hfn, cand)))


# ----------------------------------------------------------------------------- fixtures
def arrays_of(res):
    return res['arrays'] if isinstance(res, dict) and isinstance(res.get('arrays'), dict) else res


def find_edges(res, path=''):
    """Locate the recovered 19 edges anywhere in the result (key containing 'edge')."""
    if isinstance(res, dict):
        for k, v in res.items():
            if 'edge' in str(k).lower():
                try:
                    a = np.asarray(v, float)
                    if a.shape == (NK,):
                        return path + str(k), a
                except (TypeError, ValueError):
                    pass
        for k, v in res.items():
            if isinstance(v, dict):
                hit = find_edges(v, path + str(k) + '.')
                if hit[0] is not None:
                    return hit
    return None, None


def check_edges(rep, g, sres):
    G, n = 'F-edges', g['name']
    key, e = find_edges(sres)
    if e is None:
        rep.add(G, n + ':recovered_edges_returned', False, note='no 19-vector under a key containing "edge"')
        return
    err = float(np.max(np.abs(e - g['edges'])))
    rep.add(G, n + ':recovered_edges_vs_generator', err <= TOL['edge_abs'], key=key, max_abs_err=err, tol=TOL['edge_abs'])
    rep.add(G, n + ':s0_zero_s18_one', abs(e[0]) <= TOL['edge_abs'] and abs(e[-1] - 1) <= TOL['edge_abs'],
            s0=e[0], s18_minus_1=e[-1] - 1, bitwise_s0_0=bool(e[0] == 0.0), bitwise_s18_1=bool(e[-1] == 1.0))


def check_probes(rep, impl, g):
    e1 = g['edges'].copy(); e1[17] = 1 - 1e-3          # VALID geometry, last annulus width 1e-3 in s
    g1 = dict(g, name=g['name'] + ':valid_narrow_last_annulus_1e-3')
    g1.update({k: v for k, v in nodes_from_intervals(e1[:-1], e1[1:], g['L']).items() if k != 's_true'}); g1['edges'] = e1
    try:
        res = impl.scalar(g1); k, e = find_edges(res)
        diag = res.get('edge_recovery', {}) if isinstance(res, dict) else {}
        rep.add('F-edges', g['name'] + ':valid_narrow_annulus_1e-3', True, info=True, accepted=True,
                edge_err=float(np.max(np.abs(e - e1))) if e is not None else None,
                max_weight_relative_residual=diag.get('max_weight_relative_residual'))
    except Exception as exc:  # noqa: BLE001
        rep.add('F-edges', g['name'] + ':valid_narrow_annulus_1e-3', True, info=True, accepted=False,
                raised=(type(exc).__name__ + ': ' + str(exc))[:200],
                note='valid input refused at the roundoff tolerances passed; weight residual scales ~eps*s/ds')
    for label, bad in probe_geometries(g):
        try:
            impl.scalar(bad)
            rep.add('F-edges', g['name'] + ':failclosed:' + label, False, raised=False)
        except AdapterError as exc:
            rep.error('F-edges', g['name'] + ':failclosed:' + label, exc)
        except Exception as exc:  # noqa: BLE001 -- any refusal counts as fail-closed
            rep.add('F-edges', g['name'] + ':failclosed:' + label, True, raised=True,
                    exception=(type(exc).__name__ + ': ' + str(exc))[:200])


def check_scalar(rep, g, sres, exp):
    G, n = 'F-scalar', g['name']; a = arrays_of(sres)
    ts, qs = sres.get('trial_shape'), sres.get('quadrature_shape')
    rep.add(G, n + ':trial_shape_19x8', ts is not None and list(ts) == [NK, NL], trial_shape=ts)
    rep.add(G, n + ':quadrature_shape_72x32', qs is not None and list(qs) == [NR, NZ], quadrature_shape=qs)
    for key, ek in (('value', 'V'), ('partial_R', 'VR'), ('partial_z', 'VZ')):
        A = a.get(key)
        if A is None:
            rep.add(G, n + ':' + key + '_vs_expectation', False, missing=True); continue
        A = np.asarray(A); real = not np.iscomplexobj(A)
        err = relmax(A, exp[ek]) if A.shape == (NQ, NT) else float('inf')
        rep.add(G, n + ':' + key + '_2304x152_vs_expectation', A.shape == (NQ, NT) and real and err <= TOL['map_rel'],
                shape=list(A.shape), real=real, rel_err=err, tol=TOL['map_rel'])
    T = a.get('outer_coefficient_trace')
    if T is None:
        rep.add(G, n + ':outer_trace_exact_at_s1', False, missing=True)
    else:
        T = np.asarray(T); ok = T.shape == (NL, NT)
        err = float(np.max(np.abs(T - exp['T']))) if ok else float('inf')
        rep.add(G, n + ':outer_trace_exact_at_s1', ok and err <= TOL['trace_abs'], shape=list(T.shape), max_abs_err=err,
                bitwise_kron_e18_I8=bool(ok and np.array_equal(T, exp['T'])), tol=TOL['trace_abs'])
    for key, ek in (('lower_surface_trace', 'lower'), ('upper_surface_trace', 'upper')):
        A = a.get(key)
        if A is None:
            rep.add(G, n + ':' + key, False, info=True, note='absent'); continue
        A = np.asarray(A); nodes = relmax(A, exp[ek]) if A.shape == exp[ek].shape else float('inf')
        alt = np.kron(np.eye(NK), (((-1.0)**np.arange(NL)) if ek == 'lower' else np.ones(NL))[None, :])
        knots = relmax(A, alt) if A.shape == alt.shape else float('inf')
        rep.add(G, n + ':' + key + '_generalized', min(nodes, knots) <= TOL['map_rel'], shape=list(A.shape),
                rel_err_vs_kron_Bnodes=nodes, rel_err_vs_kron_I19=knots,
                note='72x152 = trace at radial nodes; 19x152 = per-knot coefficient trace')
    A = a.get('radial_value')
    if A is not None:
        A = np.asarray(A)
        rep.add(G, n + ':radial_value_B_72x19', A.shape == exp['Bv'].shape and relmax(A, exp['Bv']) <= TOL['map_rel'],
                shape=list(A.shape), rel_err=relmax(A, exp['Bv']))
    A = a.get('annular_edges_R_m')
    if A is not None:
        A = np.asarray(A, float); ref = g['L']*np.sqrt(g['edges'])
        rep.add(G, n + ':annular_edges_R_m', A.shape == ref.shape and relmax(A, ref) <= 1e-13, rel_err=relmax(A, ref))
    A = a.get('radial_derivative')
    if A is None:
        rep.add(G, n + ':radial_derivative', False, info=True, note='absent')
    else:
        A = np.asarray(A)
        e1 = relmax(A, exp['BR']) if A.shape == exp['BR'].shape else float('inf')
        e2 = relmax(A, exp['DRg']) if A.shape == exp['DRg'].shape else float('inf')
        rep.add(G, n + ':radial_derivative_generalized', min(e1, e2) <= TOL['map_rel'], shape=list(A.shape),
                rel_err_vs_trial_dBdR_72x19=e1, rel_err_vs_geometry_DR_72x72=e2)


def check_intrinsic(rep, g, sres):
    """From the module's own node values only: per-annulus cubic through its 4 GL nodes must be the
    natural cubic cardinal spline on the generator edges (delta at all 19 edges, C1/C2 across interior
    edges, S''=0 at s=0 and s=1) and its derivative must equal the module's dB/ds at the nodes."""
    G, n = 'F-scalar', g['name'] + ':intrinsic'; a = arrays_of(sres)
    V = np.asarray(a['value']); VR = np.asarray(a['partial_R'])
    if V.shape != (NQ, NT) or VR.shape != (NQ, NT):
        rep.add(G, n + '_natural_cardinal', False, note='shape'); return
    Bv = V.reshape(NR, NZ, NK, NL)[:, 0, :, 0]                  # P_0 = 1
    Bs = VR.reshape(NR, NZ, NK, NL)[:, 0, :, 0]/(2*g['R']/g['L']**2)[:, None]   # dP_0 = 0
    e = g['edges']; h = (e[1:] - e[:-1])/2; Vd = np.vander(GL4X, 4, increasing=True)
    val = np.zeros((NA, 2, NK)); d1 = np.zeros((NA, 2, NK)); d2 = np.zeros((NA, 2, NK)); dn = np.zeros((NR, NK))
    for k in range(NA):
        c = np.linalg.solve(Vd, Bv[4*k:4*k+4])
        for side, u in enumerate((-1.0, 1.0)):
            val[k, side] = c[0] + c[1]*u + c[2]*u*u + c[3]*u**3
            d1[k, side] = (c[1] + 2*c[2]*u + 3*c[3]*u*u)/h[k]
            d2[k, side] = (2*c[2] + 6*c[3]*u)/h[k]**2
        dn[4*k:4*k+4] = (c[1][None, :] + 2*c[2][None, :]*GL4X[:, None] + 3*c[3][None, :]*GL4X[:, None]**2)/h[k]
    I = np.eye(NK)
    card = max(float(np.max(np.abs(val[:, 0] - I[:-1]))), float(np.max(np.abs(val[:, 1] - I[1:]))))
    s1 = float(np.max(np.abs(d1))); s2 = float(np.max(np.abs(d2)))
    c1 = float(np.max(np.abs(d1[:-1, 1] - d1[1:, 0])))/s1; c2 = float(np.max(np.abs(d2[:-1, 1] - d2[1:, 0])))/s2
    nat = max(float(np.max(np.abs(d2[0, 0]))), float(np.max(np.abs(d2[-1, 1]))))/s2
    der = relmax(Bs, dn)
    ok = card <= TOL['intrinsic_card_abs'] and max(c1, c2, nat, der) <= TOL['intrinsic_rel']
    rep.add(G, n + '_natural_cubic_cardinal_from_nodes', ok, cardinal_abs=card, C1_rel=c1, C2_rel=c2,
            natural_end_rel=nat, node_derivative_rel=der, tol_card=TOL['intrinsic_card_abs'], tol_rel=TOL['intrinsic_rel'])


def check_preserve(rep, g, sres, exp, helper):
    G, n = 'F-preserve', g['name']; a = arrays_of(sres)
    r = a.get('roots_m')
    rep.add(G, n + ':roots_identical', r is not None and np.array_equal(np.asarray(r), g['roots']),
            present=r is not None)
    for key, ek in (('zeta', 'zeta'), ('weights_RdRdz', 'weights')):
        A = a.get(key)
        if A is None:
            rep.add(G, n + ':' + key, False, missing=True); continue
        A = np.asarray(A); err = relmax(A, exp[ek])
        rep.add(G, n + ':' + key + '_preserved', err <= TOL['preserve_rel'], shape=list(A.shape), rel_err=err,
                bitwise=bool(A.shape == exp[ek].shape and np.array_equal(A, exp[ek])), tol=TOL['preserve_rel'])
    A = a.get('root_radial_derivatives')
    if A is None:
        rep.add(G, n + ':root_radial_derivatives', False, missing=True); return
    A = np.asarray(A); err = relmax(A, exp['rootder'])
    hv = None
    if helper is not None:
        s = (g['R']/g['L'])**2; D = (2*g['R']/g['L']**2)[:, None]*helper._spline_matrices(s, list(s) + [0., 1.])[1][:NR]
        cR, hR = D @ exp['center'], D @ exp['height']; hv = relmax(A, np.stack((cR - hR, cR + hR), axis=-1))
    rep.add(G, n + ':root_radial_derivatives_old72_convention', err <= TOL['rootder_rel'], rel_err_vs_own=err,
            rel_err_vs_helper=hv, tol=TOL['rootder_rel'])


def check_chain(rep, g, sres, exp, an):
    G, n = 'F-chain', g['name']; a = arrays_of(sres)
    VR = np.asarray(a['partial_R']); VZ = np.asarray(a['partial_z'])
    if VR.shape != (NQ, NT) or VZ.shape != (NQ, NT):
        rep.add(G, n + ':fd', False, note='shape ' + str(VR.shape)); return
    Rq = np.repeat(g['R'], NZ); zq = g['z'].reshape(-1); hq = np.repeat(exp['height'], NZ)
    out = {}
    for f in (1.0, 0.5):
        d = TOL['fd_step_rel']*g['L']*f; dz = TOL['fd_step_rel']*hq*f
        fr = (an.V(Rq + d, zq) - an.V(Rq - d, zq))/(2*d)
        fz = (an.V(Rq, zq + dz) - an.V(Rq, zq - dz))/(2*dz[:, None])
        out[f] = (relmax(VR, fr), relmax(VZ, fz))
    rep.add(G, n + ':partial_R_V_vs_central_FD', out[1.0][0] <= TOL['fd_rel'], rel_err=out[1.0][0],
            rel_err_half_step=out[0.5][0], tol=TOL['fd_rel'], chain_term_share=exp['chain_term_rel'])
    rep.add(G, n + ':partial_z_V_vs_central_FD', out[1.0][1] <= TOL['fd_rel'], rel_err=out[1.0][1],
            rel_err_half_step=out[0.5][1], tol=TOL['fd_rel'])
    if g['shape'] != 'linear':
        d = TOL['fd_step_rel']*g['L']
        fr = (an.V(Rq + d, zq, 'analytic') - an.V(Rq - d, zq, 'analytic'))/(2*d)
        rep.add(G, n + ':partial_R_V_vs_FD_of_generator_geometry', True, info=True, rel_dev=relmax(VR, fr),
                note='nonzero by design: preserved old 72-node spline root derivatives approximate the analytic ones')


def check_helicity(rep, impl, g, sres, exp, m, an, fd=True):
    G, n = 'F-helicity', g['name'] + ':m' + str(m)
    try:
        H = impl.helicity(sres, g, m)
    except Exception as exc:  # noqa: BLE001
        rep.error(G, n + ':build', exc); return
    st = H.get('status')
    rep.add(G, n + ':status_regular', st == 'REGULAR_HELICITY_MAPS', status=st)
    if st != 'REGULAR_HELICITY_MAPS':
        return
    raw = expected_helicity_raw(exp, g, m); L = g['L']; rr = np.repeat(g['R'], NZ)
    missing = [k for k in REQ_HEL if k not in H]
    rep.add(G, n + ':required_names_present', not missing, missing=missing)
    ex = H.get('regularity_exponents')
    rep.add(G, n + ':regularity_exponents', ex is not None and list(ex) == raw['exponents'], got=ex, expected=raw['exponents'])
    dims = {k: list(np.shape(H[k])) for k in HEL_MAPS if k in H}
    rep.add(G, n + ':all_maps_2304x448', len(dims) == len(HEL_MAPS) and all(v == [NQ, NRED] for v in dims.values()), dims=dims)
    Tm = np.asarray(H.get('raw_coefficient_transform'))
    rep.add(G, n + ':raw_transform_456x448', Tm.shape == (3*NT, NRED), shape=list(Tm.shape))
    cn = H.get('column_norms')
    cerr = relmax(np.asarray(cn), raw['norms']) if cn is not None else float('inf')
    rep.add(G, n + ':column_norms_stacked_dimensionless', cerr <= TOL['norms_rel'], rel_err=cerr, tol=TOL['norms_rel'])
    Br = np.asarray(H.get('hard_constraint_raw')) if 'hard_constraint_raw' in H else np.zeros((0, 0))
    berr = relmax(Br, raw['Braw']) if Br.shape == raw['Braw'].shape else float('inf')
    lid = Br.ndim == 2 and Br.shape[1] == 3*NT and bool(np.any(Br[:, 2*NT:] != 0))
    rep.add(G, n + ':true_outer_8_rows_no_lid', Br.shape == (NL, 3*NT) and berr <= TOL['map_rel'] and not lid,
            shape=list(Br.shape), rel_err_vs_exact_outer=berr, vertical_block_nonzero=lid)
    sv = H.get('hard_singular_values')
    if sv is not None and np.size(sv) == NL:
        thr = H.get('rank_threshold'); svr = relmax(np.asarray(sv), raw['sv'])
        terr = abs(float(thr) - (RANK_ABS + RANK_REL*raw['sv'][0]))/(RANK_REL*raw['sv'][0]) if thr is not None else float('inf')
        rep.add(G, n + ':singular_values_and_threshold', svr <= TOL['sv_rel'] and terr <= 1e-9, sv_rel_err=svr,
                threshold_rel_err=terr, min_sv_over_threshold=float(raw['sv'][-1]/(RANK_ABS + RANK_REL*raw['sv'][0])))
    else:
        rep.add(G, n + ':singular_values_and_threshold', False, shape=list(np.shape(sv)) if sv is not None else None)
    if Tm.ndim != 2 or Tm.shape[0] != 3*NT:
        rep.add(G, n + ':shared_coordinates', False, note='transform rows != 456'); return
    Z = raw['norms'][:, None]*Tm
    ortho = float(np.max(np.abs(Z.T @ Z - np.eye(Z.shape[1]))))
    resid = float(np.max(np.abs(raw['B'] @ Z))); proj = float(np.max(np.abs(Z @ Z.T - raw['Pnull'])))
    rep.add(G, n + ':nullspace_orthonormal_BZ0_full_rank448', Z.shape[1] == NRED and ortho <= TOL['ortho']
            and resid <= TOL['hard_residual'] and proj <= TOL['projector'], columns=Z.shape[1], ortho=ortho,
            max_abs_BZ=resid, projector_err=proj)
    nz = H.get('normalized_nullspace')
    if nz is not None:
        zerr = relmax(np.asarray(nz), Z) if np.shape(nz) == Z.shape else float('inf')
        rep.add(G, n + ':normalized_nullspace_consistent_with_transform', zerr <= 1e-12, rel_err=zerr)
    outer = float(np.max(np.abs(raw['Braw'] @ Tm)))/(float(np.max(np.abs(raw['Braw'])))*float(np.max(np.abs(Tm))))
    rep.add(G, n + ':true_outer_xiR_zero_in_reduced_coordinates', outer <= TOL['outer_rel'], rel=outer)
    em = maps_from_transform(raw, Tm, L, m, rr)
    errs = {k: (relmax(np.asarray(H[k]), em[k]) if k in H else float('inf')) for k in HEL_MAPS}
    rep.add(G, n + ':all_maps_equal_raw_maps_at_ONE_shared_transform', max(errs.values()) <= TOL['hel_map_rel'],
            rel_errs=errs, tol=TOL['hel_map_rel'])
    if all(k in H for k in HEL_MAPS):
        own = np.asarray(H['partial_R_UR']) + np.asarray(H['UR'])/rr[:, None] + 1j*m*np.asarray(H['UP'])/rr[:, None] \
            + np.asarray(H['partial_z_UZ'])
        rep.add(G, n + ':divU_identity_from_returned_maps', relmax(np.asarray(H['divU']), own) <= TOL['hel_map_rel'],
                rel_err=relmax(np.asarray(H['divU']), own))
    del em
    if fd and all(k in H for k in HEL_MAPS):
        y = np.random.default_rng(1000 + m).standard_normal(Tm.shape[1]); c = Tm @ y
        cp, cm, cz = c[:NT], c[NT:2*NT], c[2*NT:]; e = raw['exponents']; zq = g['z'].reshape(-1)

        def fields(Rq, zz):
            Vq = an.V(Rq, zz); p = (Rq/L)**e[0]*(Vq @ cp); q = (Rq/L)**e[1]*(Vq @ cm)
            return (L/2)*(p + q), (L/(2j))*(p - q), L*(Rq/L)**e[2]*(Vq @ cz)
        d = TOL['fd_step_rel']*L; dz = TOL['fd_step_rel']*np.repeat(exp['height'], NZ)
        U0 = fields(rr, zq); Up, Um = fields(rr + d, zq), fields(rr - d, zq); Zp, Zm = fields(rr, zq + dz), fields(rr, zq - dz)
        dR = [(u - w)/(2*d) for u, w in zip(Up, Um)]; dZ = [(u - w)/(2*dz) for u, w in zip(Zp, Zm)]
        r = {}
        for i, comp in enumerate('RPZ'):
            r['U' + comp] = relmax(np.asarray(H['U' + comp]) @ y, U0[i])
            r['partial_R_U' + comp] = relmax(np.asarray(H['partial_R_U' + comp]) @ y, dR[i])
            r['partial_z_U' + comp] = relmax(np.asarray(H['partial_z_U' + comp]) @ y, dZ[i])
        r['divU'] = relmax(np.asarray(H['divU']) @ y, dR[0] + U0[0]/rr + 1j*m*U0[1]/rr + dZ[2])
        vok = max(r['UR'], r['UP'], r['UZ']) <= TOL['hel_fd_value_rel']
        dok = max(v for k, v in r.items() if k.startswith('partial') or k == 'divU') <= TOL['fd_rel']
        rep.add(G, n + ':physical_field_FD_product_rule_and_divergence', vok and dok, rel_errs=r)


def check_helicity_probes(rep, impl, g, sres):
    G, n = 'F-helicity', g['name']
    try:
        H = impl.helicity(sres, g, 1, rank_relative_tolerance=2.0, rank_absolute_tolerance=0.0)
        st = H.get('status') if isinstance(H, dict) else None
        rep.add(G, n + ':rank_threshold_failclosed_rel2', st != 'REGULAR_HELICITY_MAPS', status=st)
    except AdapterError as exc:
        rep.error(G, n + ':rank_threshold_failclosed_rel2', exc)
    except Exception as exc:  # noqa: BLE001
        rep.add(G, n + ':rank_threshold_failclosed_rel2', True, raised=(type(exc).__name__ + ': ' + str(exc))[:200])
    for mm in (0, 7):
        try:
            H = impl.helicity(sres, g, mm)
            rep.add(G, n + ':m' + str(mm) + '_outside_1_6', True, info=True, accepted=True,
                    status=H.get('status') if isinstance(H, dict) else None, note='old module rejects m outside 1..6')
        except Exception as exc:  # noqa: BLE001
            rep.add(G, n + ':m' + str(mm) + '_outside_1_6', True, info=True, accepted=False,
                    raised=(type(exc).__name__ + ': ' + str(exc))[:160])


def check_names(rep, g, sres):
    a = arrays_of(sres)
    miss = [k for k in REQ_SCALAR if k not in a]; opt = [k for k in OPT_SCALAR if k not in a]
    rep.add('F-names', g['name'] + ':scalar_required_names', not miss, missing=miss, optional_absent=opt,
            top_level_keys=sorted(map(str, sres.keys())) if isinstance(sres, dict) else None)
    prov = [k for k in (sres.keys() if isinstance(sres, dict) else []) if 'provenance' in str(k).lower()]
    rep.add('F-names', g['name'] + ':provenance_returned', bool(prov), info=True, keys=prov,
            content=jsonable({k: v for k, v in sres[prov[0]].items() if np.size(v) < 8}) if prov and isinstance(sres[prov[0]], dict) else None)
    callables = [k for k, v in (sres.items() if isinstance(sres, dict) else []) if callable(v)] + \
        [k for k, v in (a.items() if isinstance(a, dict) else []) if callable(v)]
    rep.add('F-noproj', g['name'] + ':no_callables_returned', not callables, callables=callables)


def run_suite(impl, geoms, *, ms=(1, 2, 3, 4, 5, 6), probes=True, helper=None, fd=True):
    rep = Report()
    for g in geoms:
        exp = expectation_scalar(g); an = Analytic(g)
        try:
            sres = impl.scalar(g)
        except Exception as exc:  # noqa: BLE001
            rep.error('F-edges', g['name'] + ':clean_geometry_accepted', exc); sres = None
        if sres is not None:
            rep.add('F-edges', g['name'] + ':clean_geometry_accepted', True)
            for fn, args in ((check_names, (rep, g, sres)), (check_edges, (rep, g, sres)),
                             (check_scalar, (rep, g, sres, exp)), (check_intrinsic, (rep, g, sres)),
                             (check_preserve, (rep, g, sres, exp, helper)), (check_chain, (rep, g, sres, exp, an))):
                try:
                    fn(*args)
                except Exception as exc:  # noqa: BLE001
                    rep.error(fn.__name__, g['name'], exc)
            for m in ms:
                try:
                    check_helicity(rep, impl, g, sres, exp, m, an, fd=fd)
                except Exception as exc:  # noqa: BLE001
                    rep.error('F-helicity', g['name'] + ':m' + str(m), exc)
            if probes:
                check_helicity_probes(rep, impl, g, sres)
            del sres
        if probes:
            check_probes(rep, impl, g)
    return rep


# ----------------------------------------------------------------------------- static scan (F-noproj)
SUSPECT_CALLS = {'solve', 'inv', 'pinv', 'lstsq', 'cholesky', 'cho_factor', 'cho_solve', 'lu_factor', 'lu_solve',
                 'eig', 'eigh', 'eigvals', 'eigvalsh', 'clip', 'tensorsolve', 'tensorinv'}
FLAG_TOKENS = ('rho', 'density', 'mass', 'ridge', 'clip', 'symmetri', 'regulariz', 'penal', 'tikhonov')


def static_scan(path=None, source=None):
    src = source if source is not None else open(path, encoding='utf-8').read()
    tree = ast.parse(src); parent = {}
    for node in ast.walk(tree):
        for ch in ast.iter_child_nodes(node):
            parent[ch] = node

    def enclosing(node):
        while node in parent:
            node = parent[node]
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                return node.name
        return '<module>'

    def dotted(f):
        parts = []
        while isinstance(f, ast.Attribute):
            parts.append(f.attr); f = f.value
        if isinstance(f, ast.Name):
            parts.append(f.id)
        return '.'.join(reversed(parts))
    calls, flags, toplevel, imports = [], [], [], []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            d = dotted(node.func); last = d.split('.')[-1] if d else ''
            if last in SUSPECT_CALLS or last in ('svd', 'qr'):
                fnm = enclosing(node)
                kind = 'expected' if last in ('svd', 'qr') else ('spline_internal' if last == 'solve' and 'spline' in fnm.lower() else 'flag')
                calls.append(dict(line=node.lineno, call=d, function=fnm, kind=kind))
        ident = None
        if isinstance(node, ast.Name):
            ident = node.id
        elif isinstance(node, ast.Attribute):
            ident = node.attr
        elif isinstance(node, ast.arg):
            ident = node.arg
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            ident = node.name
        if ident and any(t in ident.lower() for t in FLAG_TOKENS):
            flags.append(dict(line=getattr(node, 'lineno', None), identifier=ident, function=enclosing(node)))
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            imports.append(dict(line=node.lineno, names=[a.name for a in node.names],
                                module=getattr(node, 'module', None), function=enclosing(node)))
    for node in tree.body:
        ok = isinstance(node, (ast.Import, ast.ImportFrom, ast.FunctionDef, ast.ClassDef)) or \
            (isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str))
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            val = node.value
            ok = val is not None and all(isinstance(x, (ast.Constant, ast.Tuple, ast.List, ast.Dict, ast.Load,
                                                        ast.UnaryOp, ast.unaryop, ast.BinOp, ast.operator,
                                                        ast.Name, ast.Store))
                                         for x in ast.walk(val))
        if not ok:
            toplevel.append(dict(line=node.lineno, kind=type(node).__name__))
    public = [n.name for n in tree.body if isinstance(n, ast.FunctionDef) and not n.name.startswith('_')]
    flagged_calls = [c for c in calls if c['kind'] == 'flag']
    status = 'PASS' if not flagged_calls and not flags and not toplevel else ('FAIL' if flags or flagged_calls else 'REVIEW')
    return dict(status=status, public_functions=public, linalg_calls=calls, flagged_identifiers=flags,
                nonstatic_toplevel=toplevel, imports=imports)


BAD_SNIPPET = '''import numpy as np
def build(V, W, rho, xi):
    M = V.T @ (W[:, None]*V)
    return np.linalg.solve(M + 1e-12*np.eye(len(M)), V.T @ (W*rho*xi))
'''


# ----------------------------------------------------------------------------- self-run
def self_vs_helper(rep, helper, g):
    G, n = 'S-helper', g['name']; L, R = g['L'], g['R']; s = (R/L)**2; e = g['edges']
    C = Cardinal(e); tr, Ds = helper._spline_matrices(e, list(s) + [0.0, 1.0])
    rep.add(G, n + ':values_at_nodes_own_vs_helper', relmax(C.eval(s, 0), tr[:NR]) <= 1e-13, rel=relmax(C.eval(s, 0), tr[:NR]))
    rep.add(G, n + ':dBds_at_nodes_own_vs_helper', relmax(C.eval(s, 1), Ds[:NR]) <= 1e-13, rel=relmax(C.eval(s, 1), Ds[:NR]))
    e18 = np.eye(NK)[-1]
    rep.add(G, n + ':outer_row_s1', np.array_equal(tr[-1], e18) and np.array_equal(C.eval([1.0], 0)[0], e18),
            helper_bitwise=bool(np.array_equal(tr[-1], e18)), own_bitwise=bool(np.array_equal(C.eval([1.0], 0)[0], e18)))
    rep.add(G, n + ':axis_row_s0_is_e0', np.array_equal(tr[-2], np.eye(NK)[0]), helper_row_s0_max_abs_err=float(np.max(np.abs(tr[-2] - np.eye(NK)[0]))))
    ce = C.eval(e, 0); che = helper._spline_matrices(e, list(e))[0]
    rep.add(G, n + ':cardinality_at_19_knots', float(np.max(np.abs(ce - np.eye(NK)))) <= 1e-15 and float(np.max(np.abs(che - np.eye(NK)))) <= 1e-15,
            own=float(np.max(np.abs(ce - np.eye(NK)))), helper=float(np.max(np.abs(che - np.eye(NK)))))
    d2 = C.eval([0.0, 1.0], 2); m2 = float(np.max(np.abs(C.M)))
    rep.add(G, n + ':natural_ends_own', float(np.max(np.abs(d2))) <= 1e-12*m2, max_abs_S2_ends=float(np.max(np.abs(d2))),
            max_abs_S2_knots=m2)
    Dg_own = Cardinal(s).eval(s, 1); Dg_h = helper._spline_matrices(s, list(s) + [0.0, 1.0])[1][:NR]
    rep.add(G, n + ':old72_geometry_derivative_own_vs_helper', relmax(Dg_own, Dg_h) <= 1e-12, rel=relmax(Dg_own, Dg_h))
    ro, rh = RefImpl().scalar(g), RefImpl(spline='helper', helper=helper).scalar(g)
    d = {k: relmax(rh['arrays'][k], ro['arrays'][k]) for k in ('value', 'partial_R', 'partial_z', 'outer_coefficient_trace', 'root_radial_derivatives')}
    rep.add(G, n + ':reference_maps_own_spline_vs_helper_spline', max(d.values()) <= TOL['map_rel'], rel=d)
    em = v001_convention_old_maps(g, helper)['arrays']; ex = expectation_scalar(g)
    idx = np.arange(NR); blocks = em['value'].reshape(NR, NZ, NR, NL)[idx, :, idx, :]
    off = em['value'].reshape(NR, NZ, NR, NL).copy(); off[idx, :, idx, :] = 0
    rep.add(G, n + ':v001_input_emulator_vs_independent_expectation',
            np.array_equal(em['zeta'], ex['zeta']) and np.array_equal(em['weights_RdRdz'], ex['weights'])
            and relmax(em['root_radial_derivatives'], ex['rootder']) <= TOL['rootder_rel']
            and relmax(blocks, legendre_own(ex['zeta'])[0]) <= 1e-13 and not off.any(),
            zeta_bitwise=bool(np.array_equal(em['zeta'], ex['zeta'])),
            weights_bitwise=bool(np.array_equal(em['weights_RdRdz'], ex['weights'])),
            rootder_rel=relmax(em['root_radial_derivatives'], ex['rootder']),
            value_blocks_vs_bonnet=relmax(blocks, legendre_own(ex['zeta'])[0]), offdiag_zero=bool(not off.any()))
    gl = np.polynomial.legendre; zt = np.linspace(-1, 1, 41); P, D = legendre_own(zt)
    Pn = gl.legvander(zt, NL - 1); Dn = np.stack([gl.legval(zt, gl.legder(np.eye(NL)[a])) for a in range(NL)], axis=-1)
    rep.add(G, n + ':bonnet_legendre_vs_numpy', max(relmax(P, Pn), relmax(D, Dn)) <= 1e-13, rel=max(relmax(P, Pn), relmax(D, Dn)))


MUTATIONS = [
    ('knots_equal_nodes', 'old 72-node knots (trial 72x8, extrapolated outer trace)'),
    ('missing_2R_over_L2', 'dB/dR uses dB/ds (missing 2R/L^2)'),
    ('zeta_chain_sign', 'wrong sign of zeta chain term in partial_R V'),
    ('slice_576_left', 'helicity raw_transform sliced [:576],[576:1152],[1152:]'),
    ('lid_added', 'free-surface xi_z lid rows added to hard constraint'),
    ('derivative_transform_differs', 'derivative maps use a different raw_transform (T@Qrand)'),
    ('outer_trace_last_node', 'outer trace at last node s_71 instead of s=1'),
    ('root_derivs_zero', 'root radial derivatives dropped (flat geometry)'),
    ('exponents_swapped', 'regularity exponents |m-1|,|m+1| swapped'),
    ('norm_unhalved', 'transverse column norm without the 1/2 stacked factor'),
    ('edge_tol_loose', 'edge recovery tolerance 1e-6 (not roundoff)'),
    ('no_weight_check', 'edge recovery skips R dR weight verification'),
    ('sorts_input', 'edge recovery sorts unordered nodes instead of failing'),
]


def summarize(rep):
    groups = {}
    for r in rep.rows:
        g = groups.setdefault(r['group'], {}); g[r['status']] = g.get(r['status'], 0) + 1
    return groups


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--self', action='store_true'); ap.add_argument('--module'); ap.add_argument('--scalar-fn')
    ap.add_argument('--helicity-fn'); ap.add_argument('--adapter'); ap.add_argument('--out', required=True)
    ap.add_argument('--no-mutations', action='store_true')
    args = ap.parse_args()
    t0 = time.time()
    meta = dict(harness=os.path.abspath(__file__), harness_sha256=sha256_file(os.path.abspath(__file__)),
                python=sys.version.split()[0], numpy=np.__version__, platform=platform.platform(),
                argv=sys.argv, threads={k: os.environ.get(k) for k in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS')},
                contract_sha256_verified=sha256_file(CONTRACT_PATH) == CONTRACT_SHA,
                helper_sha256_verified=sha256_file(HELPER_PATH) == HELPER_SHA,
                old_scalar_sha256_verified=sha256_file(OLD_SCALAR_PATH) == OLD_SCALAR_SHA,
                old_helicity_sha256_verified=sha256_file(OLD_HEL_PATH) == OLD_HEL_SHA,
                tolerances=TOL, rank_controls=dict(relative=RANK_REL, absolute=RANK_ABS),
                scope='synthetic analytic geometry only; no project data or project run')
    helper = load_by_path(HELPER_PATH, 'n2_pinned_spline_helper', HELPER_SHA)
    geoms = [make_geometry(name='G1', seed=4511, L=3.0, shape='linear', z_rule='split'),
             make_geometry(name='G2', seed=4512, L=2.5e20, shape='smooth', z_rule='split'),
             make_geometry(name='G3', seed=4513, L=0.7, shape='smooth', z_rule='plain')]
    meta['geometries'] = [dict(name=g['name'], seed=g['seed'], L=g['L'], shape=g['shape'], z_rule=g['z_rule'],
                               edges=g['edges'], min_annulus_width=float(np.min(np.diff(g['edges'])))) for g in geoms]
    out = dict(meta=meta)
    if args.self:
        rep = Report()
        for g in geoms:
            self_vs_helper(rep, helper, g)
        out['expectation_vs_helper'] = rep.rows
        for label, impl in (('reference_own_spline', RefImpl()), ('reference_helper_spline', RefImpl(spline='helper', helper=helper))):
            r = run_suite(impl, geoms, helper=helper)
            out[label] = dict(counts=r.counts(), by_group=summarize(r), failures=r.bad(), rows=r.rows)
        scans = {'old_scalar_module_text': static_scan(OLD_SCALAR_PATH), 'old_helicity_module_text': static_scan(OLD_HEL_PATH),
                 'synthetic_density_projection_snippet': static_scan(source=BAD_SNIPPET)}
        out['static_scan_calibration'] = scans
        if not args.no_mutations:
            table = []
            for mu, desc in MUTATIONS:
                r = run_suite(RefImpl(mutation=mu), geoms[:1], ms=(1, 2, 6), helper=helper)
                bad = r.bad()
                table.append(dict(mutation=mu, description=desc, detected=bool(bad), n_failed=len(bad),
                                  groups=sorted({b['group'] for b in bad}), first_failures=[b['check'] for b in bad[:6]]))
            table.append(dict(mutation='static_scan:synthetic_density_projection', description='density projection with ridge',
                              detected=scans['synthetic_density_projection_snippet']['status'] == 'FAIL'))
            out['mutation_study'] = table
        clean = [out[k]['counts'] for k in ('reference_own_spline', 'reference_helper_spline')]
        out['verdict'] = dict(expectation_vs_helper_all_pass=all(r['status'] in ('PASS', 'INFO') for r in rep.rows),
                              reference_suites_no_fail=all(c.get('FAIL', 0) == 0 and c.get('ERROR', 0) == 0 for c in clean),
                              static_scan_calibration=[scans['old_scalar_module_text']['status'], scans['old_helicity_module_text']['status'],
                                                       scans['synthetic_density_projection_snippet']['status']],
                              all_mutations_detected=all(t['detected'] for t in out.get('mutation_study', [])))
    if args.module:
        impl = TargetImpl(args.module, args.scalar_fn, args.helicity_fn, args.adapter, helper)
        out['target'] = dict(path=impl.path, sha256=impl.sha, scalar_fn=getattr(impl.sfn, '__name__', None),
                             helicity_fn=getattr(impl.hfn, '__name__', None), adapter=args.adapter,
                             static_scan=static_scan(impl.path))
        r = run_suite(impl, geoms, helper=helper)
        if isinstance(impl.adapter, BuiltinC3v001Adapter):
            out['target']['caller_tolerances'] = dict(edge_absolute_tolerance=impl.adapter.EDGE_TOL,
                                                      weight_relative_tolerance=impl.adapter.WEIGHT_TOL)
            for g in geoms:
                try:
                    c3v001_custody_probes(r, impl, g)
                except Exception as exc:  # noqa: BLE001
                    r.error('F-preserve', g['name'] + ':custody_probes', exc)
        out['target'].update(counts=r.counts(), by_group=summarize(r), failures=r.bad(), rows=r.rows)
    out['meta']['seconds'] = round(time.time() - t0, 2)
    with open(args.out, 'w', encoding='utf-8') as f:
        json.dump(jsonable(out), f, indent=1)
    print(json.dumps(jsonable({k: v for k, v in out.items() if k in ('verdict',)}), indent=1))
    if 'target' in out:
        print(json.dumps(jsonable(dict(target_counts=out['target']['counts'], by_group=out['target']['by_group'],
                                       static=out['target']['static_scan']['status'])), indent=1))
    print('wrote', args.out, 'in', out['meta']['seconds'], 's')


if __name__ == '__main__':
    main()
