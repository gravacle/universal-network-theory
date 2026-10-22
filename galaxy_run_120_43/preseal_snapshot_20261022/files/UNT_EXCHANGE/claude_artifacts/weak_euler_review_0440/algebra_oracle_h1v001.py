import sys; sys.dont_write_bytecode=True; sys.path.append('/Users/bgm/Library/Python/3.9/lib/python/site-packages'); import numpy as np
# ---------------------------------------------------------------------------
# algebra_oracle_h1v001.py -- Claude4 review lane (dispatch 0440, amended by
# 0441), local helper H1 (algebra, complex signs, vertical shear).
# REVIEW FIXTURE ONLY. Not a project module, makes no physics decision.
#
# Independent closed-form oracle for the UNSCALED weak Euler matrix A and
# forcing vector b of the pinned root contract
#   UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CODEX1/
#   ADDITIONAL_CLAUDE_WEAK_EULER_TASKS_V001.json
#   SHA256 5c30449de636b1f3da751d07ad90caafe964ed19444b0648df8fd9726ade9ebe
# built from the closed forms derived in ALGEBRA_SIGN_H1_V001.md (same
# directory), NOT by chaining VR/VP/VZ -> AR/AP/AZ and NOT by forming E or PM:
#
#   pointwise inertial matrix, rows/columns ordered (R, phi, z), Om = Omega:
#     M_p = [[-m^2 Om^2 + 2 R Om Om_R,  -2 i m Om^2,  2 R Om Om_z],
#            [ 2 i m Om^2,              -m^2 Om^2,    0          ],
#            [ 0,                        0,          -m^2 Om^2   ]]
#   A_inertial = m^2 part + m^1 part + m^0 part (see inertial_* below);
#   pressure/density part expanded into five X^H diag(d) Y terms with
#   Y in {G, U_R, U_z}.
#
# The first line only makes numpy importable under `python3 -I -B`.
# numpy only. No solve, inverse, pseudoinverse, least squares, SVD, eigen-
# decomposition, clipping or materialized diagonal/identity matrices.
# einsum(optimize=False) is used for clarity on SMALL fixtures only.
# ---------------------------------------------------------------------------

_REAL_VECTORS = ('R', 'rho', 'P', 'K_R', 'K_z', 'P_R', 'P_z',
                 'Omega', 'Omega_R', 'Omega_z', 'volume_weights')
_POSITIVE = ('R', 'rho', 'P', 'volume_weights')
_MAPS = ('U_R', 'U_phi', 'U_z', 'divU', 'G')
_FORCING = ('f_R', 'f_phi', 'f_z')


def _real_vector(name, x):
    a = np.asarray(x)
    if a.dtype.kind not in 'fiu':
        raise ValueError(name + ': real numeric array required (complex/bool/object rejected)')
    if a.ndim != 1 or a.shape[0] < 1:
        raise ValueError(name + ': 1-D array (npoints,) required')
    a = a.astype(float)  # copy; caller array is never modified
    if not np.isfinite(a).all():
        raise ValueError(name + ': nonfinite entries')
    return a


def _complex_array(name, x, ndim):
    a = np.asarray(x)
    if a.dtype.kind not in 'fiuc':
        raise ValueError(name + ': numeric array required (bool/object rejected)')
    if a.ndim != ndim:
        raise ValueError(name + ': %d-D array required' % ndim)
    a = a.astype(complex)  # copy
    if not np.isfinite(a).all():
        raise ValueError(name + ': nonfinite entries')
    return a


def _check_m(m):
    if type(m) is not int or not 1 <= m <= 6:
        raise ValueError('m must be a Python int in 1..6 (bool excluded)')
    return m


def _check_gamma(gamma):
    if isinstance(gamma, (bool, np.bool_)) or not isinstance(gamma, (int, float, np.integer, np.floating)):
        raise ValueError('gamma must be a real scalar')
    g = float(gamma)
    if not np.isfinite(g):
        raise ValueError('gamma must be finite')
    return g


def _prepare(kw):
    out = {}
    for name in _REAL_VECTORS:
        out[name] = _real_vector(name, kw[name])
    n = out['R'].shape[0]
    for name in _REAL_VECTORS:
        if out[name].shape != (n,):
            raise ValueError(name + ': shape must equal (npoints,) = (%d,)' % n)
    for name in _POSITIVE:
        if not np.all(out[name] > 0):
            raise ValueError(name + ': strictly positive entries required')
    k = None
    for name in _MAPS:
        a = _complex_array(name, kw[name], 2)
        if a.shape[0] != n:
            raise ValueError(name + ': first dimension must be npoints = %d' % n)
        if k is None:
            k = a.shape[1]
        if a.shape != (n, k) or k < 1:
            raise ValueError(name + ': shape must be (npoints, nfree) consistent across maps')
        out[name] = a
    for name in _FORCING:
        a = _complex_array(name, kw[name], 1)
        if a.shape != (n,):
            raise ValueError(name + ': shape must be (npoints,)')
        out[name] = a
    return out


def _form(X, d, Y):
    """X^H diag(d) Y computed as sum_i conj(X[i,j]) * d[i] * Y[i,k]; no diagonal matrix."""
    return np.einsum('ij,i,ik->jk', np.conj(X), d, Y, optimize=False)


def _vform(X, v):
    """X^H v computed as sum_i conj(X[i,j]) * v[i]."""
    return np.einsum('ij,i->j', np.conj(X), v, optimize=False)


def pointwise_inertial_matrix(*, R, Omega, Omega_R, Omega_z, m):
    """Closed-form M_p, shape (npoints, 3, 3), rows/cols (R, phi, z):
    (AR, AP, AZ)^T = M_p (U_R, U_phi, U_z)^T pointwise."""
    R = _real_vector('R', R)
    Om = _real_vector('Omega', Omega)
    OmR = _real_vector('Omega_R', Omega_R)
    Omz = _real_vector('Omega_z', Omega_z)
    m = _check_m(m)
    n = R.shape[0]
    if Om.shape != (n,) or OmR.shape != (n,) or Omz.shape != (n,):
        raise ValueError('vector shapes must agree')
    O2 = Om * Om
    M = np.zeros((n, 3, 3), dtype=complex)
    M[:, 0, 0] = -(m * m) * O2 + 2.0 * R * Om * OmR
    M[:, 0, 1] = -2j * m * O2
    M[:, 0, 2] = 2.0 * R * Om * Omz
    M[:, 1, 0] = 2j * m * O2
    M[:, 1, 1] = -(m * m) * O2
    M[:, 2, 2] = -(m * m) * O2
    return M


def oracle_parts(*, R, rho, P, K_R, K_z, P_R, P_z, Omega, Omega_R, Omega_z,
                 volume_weights, U_R, U_phi, U_z, divU, G, f_R, f_phi, f_z, m, gamma):
    """Unscaled A split into its closed-form parts, plus unscaled b."""
    a = _prepare(dict(R=R, rho=rho, P=P, K_R=K_R, K_z=K_z, P_R=P_R, P_z=P_z,
                      Omega=Omega, Omega_R=Omega_R, Omega_z=Omega_z,
                      volume_weights=volume_weights, U_R=U_R, U_phi=U_phi, U_z=U_z,
                      divU=divU, G=G, f_R=f_R, f_phi=f_phi, f_z=f_z))
    m = _check_m(m)
    g = _check_gamma(gamma)
    w = a['volume_weights']
    r = a['rho']
    Rr = a['R']
    Om = a['Omega']
    XR, XP, XZ = a['U_R'], a['U_phi'], a['U_z']
    s2 = w * r * Om * Om  # w rho Omega^2
    # m^2 part: -m^2 Omega^2 times the identity in (R, phi, z); Hermitian, <= 0.
    inertial_m2 = -(m * m) * (_form(XR, s2, XR) + _form(XP, s2, XP) + _form(XZ, s2, XZ))
    # m^1 part: Coriolis coupling 2 i m Omega^2 (e_phi e_R^T - e_R e_phi^T); Hermitian.
    inertial_m1 = 2j * m * (_form(XP, s2, XR) - _form(XR, s2, XP))
    # m^0 part: R d_R(Omega^2) e_R e_R^T + R d_z(Omega^2) e_R e_z^T.
    # The second (vertical shear) term has no e_z e_R^T partner: non-Hermitian
    # whenever Omega_z != 0.
    inertial_m0_radial = _form(XR, 2.0 * w * r * Rr * Om * a['Omega_R'], XR)
    inertial_m0_vertical_shear = _form(XR, 2.0 * w * r * Rr * Om * a['Omega_z'], XZ)
    # Pressure/density part, PM and E expanded (Y in {G, U_R, U_z}):
    #  - divU^H diag(w gamma P/rho) G
    #  + divU^H diag(w rho^gamma K_R) U_R + divU^H diag(w rho^gamma K_z) U_z
    #  - U_R^H diag(w P_R/rho) G - U_z^H diag(w P_z/rho) G
    rg = r ** g
    pressure_density = (-_form(a['divU'], w * g * a['P'] / r, a['G'])
                        + _form(a['divU'], w * rg * a['K_R'], XR)
                        + _form(a['divU'], w * rg * a['K_z'], XZ)
                        - _form(XR, w * a['P_R'] / r, a['G'])
                        - _form(XZ, w * a['P_z'] / r, a['G']))
    inertial = inertial_m2 + inertial_m1 + inertial_m0_radial + inertial_m0_vertical_shear
    A = inertial + pressure_density
    b = -(_vform(XR, w * r * a['f_R']) + _vform(XP, w * r * a['f_phi']) + _vform(XZ, w * r * a['f_z']))
    return dict(A=A, b=b, inertial=inertial, inertial_m2=inertial_m2, inertial_m1=inertial_m1,
                inertial_m0_radial=inertial_m0_radial,
                inertial_m0_vertical_shear=inertial_m0_vertical_shear,
                pressure_density=pressure_density)


def oracle_A_b(*, R, rho, P, K_R, K_z, P_R, P_z, Omega, Omega_R, Omega_z,
               volume_weights, U_R, U_phi, U_z, divU, G, f_R, f_phi, f_z, m, gamma):
    """Return (A_unscaled, b_unscaled) from the closed forms. Divide both by the
    supplied normalization_scale to compare with a scaled implementation."""
    parts = oracle_parts(R=R, rho=rho, P=P, K_R=K_R, K_z=K_z, P_R=P_R, P_z=P_z,
                         Omega=Omega, Omega_R=Omega_R, Omega_z=Omega_z,
                         volume_weights=volume_weights, U_R=U_R, U_phi=U_phi, U_z=U_z,
                         divU=divU, G=G, f_R=f_R, f_phi=f_phi, f_z=f_z, m=m, gamma=gamma)
    return parts['A'], parts['b']
