#!/usr/bin/env python3
"""demo_pointwise_vs_weak_k1v001.py

Claude4 review lane, dispatch 0448, local helper K1 (algebra). Synthetic analytic
fixtures only: numpy and the standard library. No file is read or written, no project
module is imported, and no galaxy data, solve output, calibration or target value is
touched. Python 3.9-compatible syntax. Runs in about a second.

[1] -div(rho xi) against Gkin in cylindrical form, exp(+i m phi), with a 3-D Cartesian
    4th-order finite-difference reference, plus convention mutants.
[2] EOS provenance: PM(Gkin) with the provider-form gradients (L44-46, K_z = 0).
[3] Pointwise versus weak density in one vertical column: 32 Gauss-Legendre nodes,
    Legendre P0..P7 in the affine height coordinate (the 0438 vertical structure).
[4] Anti-Hermitian part of the 0439 A built with Gkin and provider-form gradients.

Exit status 0 if and only if every check meets its stated criterion.
"""
import sys

sys.dont_write_bytecode = True
if sys.version_info < (3, 12):
    sys.path.append('/Users/bgm/Library/Python/3.9/lib/python/site-packages')

import numpy as np
from numpy.polynomial import legendre as L
from numpy.polynomial import Polynomial as Poly

GAMMA = 5.0 / 3.0
FAILED = []


def check(name, ok, detail):
    print(('PASS ' if ok else 'FAIL ') + name + ': ' + detail)
    if not ok:
        FAILED.append(name)


def rel(a, b):
    return float(np.linalg.norm(a - b) / np.linalg.norm(b))


def cplx(rng, *shape):
    return rng.normal(size=shape) + 1j * rng.normal(size=shape)


def gkin(rho, rho_R, rho_z, U_R, U_z, divU):
    """Root contract equation, transcribed: maps are (npoints, nfree)."""
    return -rho[:, None] * divU - rho_R[:, None] * U_R - rho_z[:, None] * U_z


def provider_gradients(rho, P, K_R, P_R, P_z):
    """Provider L46 transcribed (gamma hard-coded 5/3 as there; K_z = 0 by L44)."""
    rho_R = (P_R - rho ** (5 / 3) * K_R) / ((5 / 3) * P / rho)
    rho_z = P_z / ((5 / 3) * P / rho)
    return rho_R, rho_z


# ---------------------------------------------------------------------------------------
# [1] cylindrical mass-advection identity
# ---------------------------------------------------------------------------------------
def section1(rng):
    print('\n[1] -div(rho xi) vs Gkin (exp(+i m phi)); reference = 3-D Cartesian 4th-order FD')
    c1, c2, c3 = 0.3 + 0.2j, -0.25 + 0.4j, 0.5 - 0.1j

    def rho_f(R, z):
        return np.exp(-0.4 * R + 0.3 * np.sin(z) - 0.5 * z * z + 0.2 * R * z)

    def xi(R, z):
        return (c1 * R * (1 + 0.5 * z) + 0.1 * R * R,
                c2 * (1 + 0.3 * R - 0.2 * z * z),
                c3 * (z + 0.3 * R * z * z) + 0.2j)

    def flux_cart(x, y, z, m):
        R = np.hypot(x, y)
        ph = np.arctan2(y, x)
        xR, xP, xZ = xi(R, z)
        e = rho_f(R, z) * np.exp(1j * m * ph)
        c, s = np.cos(ph), np.sin(ph)
        return e * (xR * c - xP * s), e * (xR * s + xP * c), e * xZ

    def div_fd(x, y, z, m, h=1e-3):
        total = 0
        for axis in range(3):
            acc = 0
            for k, cf in ((2, -1.0), (1, 8.0), (-1, -8.0), (-2, 1.0)):
                d = [0.0, 0.0, 0.0]
                d[axis] = k * h
                acc = acc + cf * flux_cart(x + d[0], y + d[1], z + d[2], m)[axis]
            total = total + acc / (12 * h)
        return total

    worst = 0.0
    mutant_min = {}
    for m in (1, 2, 3, 6):
        n = 16
        R = rng.uniform(0.6, 2.0, n)
        ph = rng.uniform(0, 2 * np.pi, n)
        z = rng.uniform(-0.6, 0.6, n)
        ref = -div_fd(R * np.cos(ph), R * np.sin(ph), z, m) * np.exp(-1j * m * ph)
        rho = rho_f(R, z)
        rho_R = rho * (-0.4 + 0.2 * z)
        rho_z = rho * (0.3 * np.cos(z) - z + 0.2 * R)
        xR, xP, xZ = xi(R, z)
        dR_xR = c1 * (1 + 0.5 * z) + 0.2 * R
        dz_xZ = c3 * (1 + 0.6 * R * z)
        divxi = dR_xR + xR / R + 1j * m * xP / R + dz_xZ      # helicity-L64 form
        G = gkin(rho, rho_R, rho_z, xR[:, None], xZ[:, None], divxi[:, None])[:, 0]
        worst = max(worst, rel(G, ref))
        mutants = {
            'phi term added a second time': G - rho * 1j * m * xP / R,
            'second xi_R/R term': G - rho * xR / R,
            'Lagrangian -rho div xi only': -rho * divxi,
            'exp(-i m phi) sign in divU': G + 2 * rho * 1j * m * xP / R,
            'advection sign flipped': -rho * divxi + rho_R * xR + rho_z * xZ,
        }
        for k, v in mutants.items():
            mutant_min[k] = min(mutant_min.get(k, np.inf), rel(v, ref))
    check('1a Gkin == -div(rho xi), m=1,2,3,6, 64 random points', worst < 1e-9,
          'max relative error %.1e (FD truncation/roundoff level)' % worst)
    for k, v in mutant_min.items():
        check('1b mutant detected: ' + k, v > 1e-2, 'min relative deviation %.2e' % v)


# ---------------------------------------------------------------------------------------
# [2] EOS provenance: PM(Gkin) reduction
# ---------------------------------------------------------------------------------------
def section2(rng):
    print('\n[2] PM(Gkin) with provider gradients vs -gamma P divU - P_R U_R - P_z U_z')
    n, k = 11, 4
    for eps in (0.0, 0.08):
        rho = rng.uniform(0.2, 3.0, n)
        K = rng.uniform(0.5, 2.0, n)
        P = K * rho ** GAMMA * (1 + eps * rng.uniform(-1, 1, n))
        K_R = K * rng.uniform(-1, 1, n)          # provider: K_R = K * logK_R
        K_z = np.zeros(n)                        # provider: fixed-K column law
        P_R, P_z = rng.normal(size=n), rng.normal(size=n)   # lagged relations: free numbers
        rho_R, rho_z = provider_gradients(rho, P, K_R, P_R, P_z)
        U_R, U_z, divU = cplx(rng, n, k), cplx(rng, n, k), cplx(rng, n, k)
        G = gkin(rho, rho_R, rho_z, U_R, U_z, divU)
        E = -K_R[:, None] * U_R - K_z[:, None] * U_z
        PM = (GAMMA * P / rho)[:, None] * G + rho[:, None] ** GAMMA * E
        target = -(GAMMA * P)[:, None] * divU - P_R[:, None] * U_R - P_z[:, None] * U_z
        eos = float(np.max(np.abs(P - K * rho ** GAMMA) / P))
        check('2a eps=%.2f identity PM(Gkin) == -gP divU - P_R U_R - P_z U_z' % eps,
              rel(PM, target) < 1e-13,
              'rel err %.1e; max |P-K rho^g|/P = %.1e' % (rel(PM, target), eos))
        rho_R_alt = (P_R - (P / K) * K_R) / ((5 / 3) * P / rho)  # EOS-implied variant via P/K
        PM_alt = (GAMMA * P / rho)[:, None] * gkin(rho, rho_R_alt, rho_z, U_R, U_z, divU) \
            + rho[:, None] ** GAMMA * E
        r_alt = rel(PM_alt, target)
        expect_alt = (r_alt < 1e-13) if eps == 0.0 else (r_alt > 1e-3)
        check('2b eps=%.2f contrast: (P/K)K_R gradient variant' % eps, expect_alt,
              'rel deviation %.1e (identity is specific to the provider rho^(5/3) K_R form)'
              % r_alt)
        coeff_gap = float(np.max(np.abs(GAMMA * P / rho - GAMMA * K * rho ** (GAMMA - 1))
                                 / (GAMMA * P / rho)))
        print('     eps=%.2f: max rel gap between PM coefficient gamma P/rho and EOS '
              'derivative gamma K rho^(g-1) = %.2e' % (eps, coeff_gap))


# ---------------------------------------------------------------------------------------
# [3] pointwise vs weak, one vertical column
# ---------------------------------------------------------------------------------------
def column(N=32, split=False, c=0.13, h=0.71):
    if split:   # illustrative two-panel 16+16 rule split at zeta=0 (actual split not inspected)
        x, wx = L.leggauss(N // 2)
        zeta = np.concatenate(((x - 1) / 2, (x + 1) / 2))
        om = np.concatenate((wx / 2, wx / 2))
    else:
        zeta, om = L.leggauss(N)
    V = L.legvander(zeta, 7)                                         # values, 0438 L23
    Vz = np.stack([L.legval(zeta, L.legder(np.eye(8)[a])) for a in range(8)], axis=-1) / h
    w = h * om                                                       # dz weights
    return dict(zeta=zeta, w=w, V=V, Vz=Vz, M=V.T @ (w[:, None] * V), h=h, c=c)


def compare(col, rho, rho_z, xz, dxz):
    V, Vz, w, M = col['V'], col['Vz'], col['w'], col['M']
    Gk = -rho * dxz - rho_z * xz                       # Gkin, vertical part
    b = Vz.T @ (w * rho * xz)                          # 0438 vertical b term
    Gp = V @ np.linalg.solve(M, b)                     # G_proj = V M^-1 b
    g = V.T @ (w * Gk)                                 # L2(W) functional of Gkin
    PiG = V @ np.linalg.solve(M, g)                    # W-projection of Gkin
    nW = lambda f: float(np.sqrt(np.sum(w * np.abs(f) ** 2)))
    d_in, d_out = Gp - PiG, PiG - Gk
    out = dict(Gk=Gk, Gp=Gp, b=b, g=g, nGk=nW(Gk), abs=nW(Gp - Gk),
               pyth=abs(nW(Gp - Gk) ** 2 - nW(d_in) ** 2 - nW(d_out) ** 2)
               / max(nW(Gp - Gk) ** 2, 1e-300),
               weak_by_construction=rel(V.T @ (w * Gp), b) if np.linalg.norm(b) > 0 else 0.0,
               d_in=d_in)
    if out['nGk'] > 0:
        out.update(rel=nW(Gp - Gk) / out['nGk'], rel_in=nW(d_in) / out['nGk'],
                   rel_out=nW(d_out) / out['nGk'])
    return out


def fields_poly(col, rho_p, xz_p, A=1.0, rho_z_scale=1.0):
    z, h = col['zeta'], col['h']
    return (rho_p(z), rho_z_scale * rho_p.deriv()(z) / h, A * xz_p(z), A * xz_p.deriv()(z) / h)


def fields_polytrope(col, xz_p, A=1.0):
    z, h = col['zeta'], col['h']
    s = 1 - z * z
    return s ** 1.5, -3 * z * np.sqrt(s) / h, A * xz_p(z), A * xz_p.deriv()(z) / h


def section3(rng):
    print('\n[3] one column: GL32, Legendre P0..P7 in affine zeta; rel = ||G_proj-Gkin||_W/||Gkin||_W')
    print('    split: G_proj-Gkin = d_in (in span: flux/quadrature/gradient-input) + d_out ((Pi-1)Gkin)')
    col = column()
    one_m_z2 = Poly([1, 0, -1])
    xz4 = Poly([0.3, 1.0, -0.5, 0.2, 0.1])
    xz6 = Poly([0.2, -0.4, 0.3, 0.5, -0.2, 0.1, 0.05])
    xz7 = Poly(L.leg2poly(np.eye(8)[7]))
    Amp = 7.75 * np.exp(0.7j)

    # A: zero flux, Gkin in span, quadrature exact
    for tag, xp in (('A1 rho=1-zeta^2, xi_z deg 4 (Gkin deg 5)', xz4),
                    ('A2 rho=1-zeta^2, xi_z deg 6 (Gkin deg 7, edge of span)', xz6)):
        r = compare(col, *fields_poly(col, one_m_z2, xp, A=Amp))
        check(tag, r['rel'] < 1e-12, 'rel %.1e' % r['rel'])
    r = compare(col, *fields_poly(col, one_m_z2, xz7, A=Amp))
    check('A3 rho=1-zeta^2, xi_z=P7 (Gkin deg 8: out of span only)',
          r['rel'] > 1e-3 and r['rel_in'] < 1e-12,
          'rel %.3e = out-of-span %.3e, in-span %.1e' % (r['rel'], r['rel_out'], r['rel_in']))

    # B: polynomial rho not vanishing at the surfaces -> dropped flux only
    for tag, rp in (('B1 rho=1-0.8 zeta^2 (rho_s=0.2)', Poly([1, 0, -0.8])),
                    ('B2 rho=1-zeta^2+0.05 (thin nonzero surface layer)', Poly([1.05, 0, -1]))):
        rho, rho_z, xz, dxz = fields_poly(col, rp, xz4, A=Amp)
        r = compare(col, rho, rho_z, xz, dxz)
        f_top, f_bot = rp(1.0) * Amp * xz4(1.0), rp(-1.0) * Amp * xz4(-1.0)
        jump = L.legvander(np.array([1.0]), 7)[0] * f_top - L.legvander(np.array([-1.0]), 7)[0] * f_bot
        pred = col['V'] @ np.linalg.solve(col['M'], jump)        # V M^-1 [psi rho xi_z]_bot^top
        mom0 = abs(r['g'][0] + (f_top - f_bot)) / abs(f_top - f_bot)  # P0 moment = -[rho xi_z]
        check(tag, rel(r['d_in'], pred) < 1e-12 and r['rel_out'] < 1e-12 and r['rel'] > 1e-2
              and mom0 < 1e-12,
              'rel %.3e; d_in equals flux-kernel prediction to %.1e; out-of-span %.1e; '
              'P0 moment sum_p w_p Gkin_p = -[rho xi_z]_bot^top to %.1e'
              % (r['rel'], rel(r['d_in'], pred), r['rel_out'], mom0))
    rho, rho_z, xz, dxz = fields_poly(col, Poly([1.0]), Poly([1.0]), A=Amp)
    r = compare(col, rho, rho_z, xz, dxz)
    print('     B3 rho=1, rigid xi_z: Gkin = 0 exactly (||Gkin||_W=%.1e), ||G_proj||_W/|rho xi_z| = %.2f'
          ' -> relative difference unbounded' % (r['nGk'], r['abs'] / abs(Amp)))

    # C: gamma=5/3 polytrope shape, zero flux, non-polynomial
    for tag, xp in (('C1 rho=(1-zeta^2)^1.5, rigid xi_z', Poly([1.0])),
                    ('C2 rho=(1-zeta^2)^1.5, xi_z ~ zeta', Poly([0, 1.0])),
                    ('C3 rho=(1-zeta^2)^1.5, xi_z ~ P7', xz7)):
        parts = []
        for N in (32, 64, 128):
            cN = column(N)
            parts.append(compare(cN, *fields_polytrope(cN, xp, A=Amp)))
        r1 = compare(col, *fields_polytrope(col, xp, A=1.0))
        check(tag, parts[0]['rel_out'] > 1e-3 and parts[0]['pyth'] < 1e-10
              and abs(parts[0]['rel'] - r1['rel']) < 1e-12 * max(1.0, r1['rel']),
              'N=32 rel %.3e (out-of-span %.3e, in-span quadrature %.1e); in-span at N=64/128: '
              '%.1e/%.1e; amplitude 1 vs 7.75e^{0.7i}: same rel' %
              (parts[0]['rel'], parts[0]['rel_out'], parts[0]['rel_in'],
               parts[1]['rel_in'], parts[2]['rel_in']))
        print('     %s: weak identity V^T W G_proj = b holds by construction (rel %.1e) although '
              'G_proj != Gkin pointwise' % (tag[:2], parts[0]['weak_by_construction']))
    cs = column(32, split=True)
    rs = compare(cs, *fields_polytrope(cs, Poly([1.0]), A=Amp))
    print('     C1 with illustrative split 16+16 panels at zeta=0: rel %.3e (out-of-span %.3e, '
          'in-span %.1e)' % (rs['rel'], rs['rel_out'], rs['rel_in']))

    # D: gradient-input inconsistency only (polynomial, zero flux, in span)
    for delta in (0.01, 0.1):
        r = compare(col, *fields_poly(col, one_m_z2, xz4, A=Amp, rho_z_scale=1 + delta))
        check('D rho_z supplied = (1+%.2f) d_z rho' % delta,
              r['rel'] > 1e-4 and r['rel_out'] < 1e-12,
              'rel %.3e, all in span (out-of-span %.1e)' % (r['rel'], r['rel_out']))

    # E: converse -- the weak functional is blind to W-orthogonal content
    q = cplx(rng, 32)
    rr = q - col['V'] @ np.linalg.solve(col['M'], col['V'].T @ (col['w'] * q))
    mom = float(np.max(np.abs(col['V'].T @ (col['w'] * rr))) / np.max(np.abs(col['V'].T @ (col['w'] * q))))
    nrm = float(np.sqrt(np.sum(col['w'] * np.abs(rr) ** 2) / np.sum(col['w'] * np.abs(q) ** 2)))
    check('E weak moments blind to (1-Pi) content', mom < 1e-13 and nrm > 0.3,
          'G and G+r share all 8 moments (rel %.1e) while ||r||_W/||q||_W = %.2f' % (mom, nrm))


# ---------------------------------------------------------------------------------------
# [4] Hermiticity diagnostic
# ---------------------------------------------------------------------------------------
def contract_A(R, rho, P, K_R, K_z, P_R, P_z, Om, Om_R, Om_z, w, U_R, U_P, U_z, divU, G, m, gamma):
    """0439 contract equations 0-8 transcribed (A unscaled)."""
    i = 1j
    E = -K_R[:, None] * U_R - K_z[:, None] * U_z
    PM = (gamma * P / rho)[:, None] * G + rho[:, None] ** gamma * E
    VR = i * m * Om[:, None] * U_R
    VP = -(R * Om_R)[:, None] * U_R + i * m * Om[:, None] * U_P - (R * Om_z)[:, None] * U_z
    VZ = i * m * Om[:, None] * U_z
    AR = i * m * Om[:, None] * VR - 2 * Om[:, None] * VP
    AP = i * m * Om[:, None] * VP + (2 * Om + R * Om_R)[:, None] * VR + (R * Om_z)[:, None] * VZ
    AZ = i * m * Om[:, None] * VZ

    def H(X, d, Y):
        return X.conj().T @ (d[:, None] * Y)
    return (H(U_R, w * rho, AR) + H(U_P, w * rho, AP) + H(U_z, w * rho, AZ)
            - H(divU, w, PM) - H(U_R, w * P_R / rho, G) - H(U_z, w * P_z / rho, G))


def section4(rng):
    print('\n[4] anti-Hermitian part of 0439 A with G = Gkin and provider gradients (K_z = 0)')
    n, k = 13, 5
    worst_pred, worst_tw, worst_tw_eps_exact, worst_kpred = 0.0, 0.0, 0.0, 0.0
    min_generic, min_kform_eps, max_kform_eps, min_mut = np.inf, np.inf, 0.0, {}
    for trial in range(24):
        m = int(rng.integers(1, 7))
        eps = 0.0 if trial % 2 == 0 else 0.05
        R = rng.uniform(0.3, 2.0, n)
        rho = rng.uniform(0.2, 3.0, n)
        K = rng.uniform(0.5, 2.0, n)
        P = K * rho ** GAMMA * (1 + eps * rng.uniform(-1, 1, n))
        K_R = K * rng.uniform(-1, 1, n)
        K_z = np.zeros(n)
        P_R, P_z = rng.normal(size=n), rng.normal(size=n)
        Om, Om_R = rng.uniform(0.5, 2.0, n), rng.normal(size=n)
        w = rng.uniform(0.1, 1.0, n)
        rho_R, rho_z = provider_gradients(rho, P, K_R, P_R, P_z)
        U_R, U_P, U_z, divU = (cplx(rng, n, k) for _ in range(4))
        G = gkin(rho, rho_R, rho_z, U_R, U_z, divU)
        tw_exact = -(rho ** (GAMMA - 1) * K_R * P_z / (GAMMA * P)) / (2 * R * Om)
        tw_kform = -((K_R / K) * P_z / (GAMMA * rho)) / (2 * R * Om)
        Om_z_rand = rng.normal(size=n)

        def antiH(Om_z, Gm):
            A = contract_A(R, rho, P, K_R, K_z, P_R, P_z, Om, Om_R, Om_z, w, U_R, U_P, U_z, divU,
                           Gm, m, GAMMA)
            return A, 0.5 * (A - A.conj().T)

        A, S = antiH(Om_z_rand, G)
        d_gen = w * (2 * rho * R * Om * Om_z_rand + (P_R * rho_z - P_z * rho_R) / rho)
        d_prov = w * rho * (R * 2 * Om * Om_z_rand + rho ** GAMMA * K_R * P_z / (P * GAMMA * rho))
        S_pred = 0.5 * (U_R.conj().T @ (d_prov[:, None] * U_z) - U_z.conj().T @ (d_prov[:, None] * U_R))
        worst_pred = max(worst_pred, rel(S, S_pred), rel(d_prov, d_gen))
        min_generic = min(min_generic, float(np.linalg.norm(S) / np.linalg.norm(A)))
        A, S = antiH(tw_exact, G)
        r = float(np.linalg.norm(S) / np.linalg.norm(A))
        if eps == 0.0:
            worst_tw = max(worst_tw, r)
            A2, S2 = antiH(tw_kform, G)
            worst_tw = max(worst_tw, float(np.linalg.norm(S2) / np.linalg.norm(A2)))
        else:
            worst_tw_eps_exact = max(worst_tw_eps_exact, r)
            A2, S2 = antiH(tw_kform, G)
            ratio = float(np.linalg.norm(S2) / np.linalg.norm(A2))
            min_kform_eps, max_kform_eps = min(min_kform_eps, ratio), max(max_kform_eps, ratio)
            eps_vec = (P - K * rho ** GAMMA) / P
            dK = -w * (K_R / K) * (P_z / GAMMA) * eps_vec      # predicted residual coefficient
            S2_pred = 0.5 * (U_R.conj().T @ (dK[:, None] * U_z) - U_z.conj().T @ (dK[:, None] * U_R))
            worst_kpred = max(worst_kpred, rel(S2, S2_pred))
            continue
        muts = {'Lagrangian G=-rho divU': -rho[:, None] * divU,
                'duplicate phi term in G': G - (rho * 1j * m / R)[:, None] * U_P,
                'G plus non-pointwise part': G + 0.05 * cplx(rng, n, k) * np.abs(G).mean()}
        for key, Gm in muts.items():
            A3, S3 = antiH(tw_exact, Gm)
            min_mut[key] = min(min_mut.get(key, np.inf), float(np.linalg.norm(S3) / np.linalg.norm(A3)))
    check('4a (A-A^H)/2 == 1/2[U_R^H D(d) U_z - h.c.], d = w rho[R d_z(Om^2) + rho^g K_R P_z/(g rho P)]',
          worst_pred < 1e-12, 'max rel err %.1e over 24 random cases (m=1..6)' % worst_pred)
    print('     generic random Omega_z: ||antiH||/||A|| >= %.2e' % min_generic)
    check('4b P=K rho^g, Omega_z at fixed-K thermal wind (both forms)', worst_tw < 1e-13,
          'max ||A-A^H||/(2||A||) = %.1e' % worst_tw)
    check('4c P!=K rho^g (eps 0.05), Omega_z from rho^g/P form', worst_tw_eps_exact < 1e-13,
          'max %.1e' % worst_tw_eps_exact)
    check('4d P!=K rho^g (eps 0.05), Omega_z from K_R/K form', worst_kpred < 1e-9,
          '||antiH||/||A|| in [%.1e, %.1e]; equals 1/2[U_R^H D(d_eps) U_z - h.c.], '
          'd_eps = -w (K_R/K)(P_z/gamma)(P-K rho^g)/P, to %.1e'
          % (min_kform_eps, max_kform_eps, worst_kpred))
    for key, v in min_mut.items():
        check('4e at thermal wind, mutant ' + key, v > 1e-8,
              'min ||antiH||/||A|| = %.1e (roundoff floor ~1e-16)' % v)


def main():
    rng = np.random.default_rng(448)
    print('numpy', np.__version__, '| python', sys.version.split()[0])
    section1(rng)
    section2(rng)
    section3(rng)
    section4(rng)
    print('\nRESULT:', 'ALL CHECKS PASS' if not FAILED else 'FAILED: ' + '; '.join(FAILED))
    return 0 if not FAILED else 1


if __name__ == '__main__':
    sys.exit(main())
