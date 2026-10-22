"""oracle_n1v001 -- Claude4 review lane, dispatch 0451, helper N1 (algebra/numerics).

Independent oracle for the annular-knot radial correction of root contract
ANNULAR_KNOT_RADIAL_CORRECTION_CHOICE_V001.json (sha256 58ffcbb8...).
Synthetic analytic fixtures only. Inert: numpy only, definitions only, no I/O.

Independence from the code under review:
  * natural cubic cardinal splines in the Hermite *slope* formulation
    (the pinned helper _spline_matrices uses second-derivative moments);
  * Legendre P_a and P'_a from the Bonnet and P'_{a+1}=P'_{a-1}+(2a+1)P_a
    recurrences (v001/c3v001 use legvander/legder);
  * closed-form 4-point Gauss-Legendre constants (c3v001 uses leggauss);
  * closed-form edge recovery plus an independent weights-only recovery.
The helicity construction follows the contract text (exponents, stacked
dimensionless norms, Braw=[.5T,.5T,0], SVD threshold, complete-QR nullspace);
nullspace='eigh' gives a different orthonormal basis of the same subspace so that
callers compare subspaces/products, never raw Z columns.
No solve, projection, symmetrization, ridge, clipping or physics.
"""
import numpy as np

EPS = float(np.finfo(np.float64).eps)
RECOMMENDED_EDGE_TOL_S = 64 * EPS          # ~1.42e-14, absolute, in s=(R/L)^2 units

_S65 = np.sqrt(6.0 / 5.0)
_X1 = np.sqrt(3.0 / 7.0 - 2.0 / 7.0 * _S65)
_X2 = np.sqrt(3.0 / 7.0 + 2.0 / 7.0 * _S65)
_S30 = np.sqrt(30.0)
GL4_X = np.array([-_X2, -_X1, _X1, _X2])                      # ascending
GL4_W = np.array([(18 - _S30) / 36, (18 + _S30) / 36, (18 + _S30) / 36, (18 - _S30) / 36])


def recover_annular_edges(*, radial_nodes_m, radial_RdR_weights_m2, outer_radius_m,
                          edge_tolerance_s, weight_tolerance_s):
    """Closed-form annulus recovery from ordered 4-point GL groups in s=(R/L)^2.

    Group k nodes s_{4k+i} = c_k + h_k X_i, R dR weights = (L^2/2) h_k W_i.
    c_k = mean of the 4 nodes; h_k = [X2(s3-s0)+X1(s2-s1)]/(2(X1^2+X2^2)) (least squares,
    X1^2+X2^2 = 6/7). Checks (absolute, s units): every node, adjacent edges, s0=0, s18=1,
    normalized weights 2w/L^2 against h_k W_i, and the independent cumulative-weight edges.
    Raises ValueError on any excess; never guesses. Returns knots [0, interior, 1].
    """
    R = np.asarray(radial_nodes_m, dtype=np.float64)
    wr = np.asarray(radial_RdR_weights_m2, dtype=np.float64)
    L = float(outer_radius_m)
    tol_s, tol_w = float(edge_tolerance_s), float(weight_tolerance_s)
    if not (np.isfinite(tol_s) and np.isfinite(tol_w) and tol_s >= 0 and tol_w >= 0):
        raise ValueError('explicit finite nonnegative tolerances required')
    if R.ndim != 1 or R.size % 4 or R.size < 8 or wr.shape != R.shape:
        raise ValueError('ordered 4-point groups required')
    if not (np.isfinite(L) and L > 0 and np.isfinite(R).all() and np.isfinite(wr).all()):
        raise ValueError('finite geometry required')
    if np.any(R <= 0) or np.any(R >= L) or np.any(np.diff(R) <= 0) or np.any(wr <= 0):
        raise ValueError('strictly interior increasing nodes and positive weights required')
    s = (R / L) ** 2
    g = s.reshape(-1, 4)
    c = g.mean(axis=1)
    h = (_X2 * (g[:, 3] - g[:, 0]) + _X1 * (g[:, 2] - g[:, 1])) / (2.0 * (_X1 * _X1 + _X2 * _X2))
    if np.any(h <= 0):
        raise ValueError('nonpositive recovered half-width')
    a, b = c - h, c + h
    what = 2.0 * wr / (L * L)                                   # s-measure weights, sum 1
    res = dict(
        node=float(np.max(np.abs(g - (c[:, None] + h[:, None] * GL4_X[None, :])))),
        adjacent=float(np.max(np.abs(b[:-1] - a[1:]))),
        s0=float(abs(a[0])),
        s_end=float(abs(b[-1] - 1.0)),
        weight=float(np.max(np.abs(what.reshape(-1, 4) - h[:, None] * GL4_W[None, :]))))
    knots = np.empty(g.shape[0] + 1)
    knots[0], knots[-1] = 0.0, 1.0
    knots[1:-1] = 0.5 * (b[:-1] + a[1:])
    edges_w = np.concatenate(([0.0], np.cumsum(what.reshape(-1, 4).sum(axis=1))))
    res['cumulative_weight_edges'] = float(np.max(np.abs(edges_w - knots)))
    bad = [k for k in ('node', 'adjacent', 's0', 's_end') if not res[k] <= tol_s]
    bad += [k for k in ('weight', 'cumulative_weight_edges') if not res[k] <= tol_w]
    if bad or np.any(np.diff(knots) <= 0):
        raise ValueError('annular GL-in-s recovery failed closed: ' +
                         ', '.join(f'{k}={res[k]:.3e}' for k in res) + f'; failing {bad}')
    return dict(knots=knots, s_nodes=s, centers=c, half_widths=h, s_weights=what,
                residuals=res, edge_tolerance_s=tol_s, weight_tolerance_s=tol_w)


def natural_cubic_cardinal(knots):
    """Natural cubic cardinal splines B_j (B_j(t_k)=delta_jk, B''=0 at both ends).

    Hermite slope form: slopes[k, j] = B_j'(t_k) solve the diagonally dominant system
    2m0+m1=3(y1-y0)/h0; m_{i-1}/h_{i-1}+2m_i(1/h_{i-1}+1/h_i)+m_{i+1}/h_i
    =3[(y_i-y_{i-1})/h_{i-1}^2+(y_{i+1}-y_i)/h_i^2]; m_{n-1}+2m_n=3(y_n-y_{n-1})/h_{n-1}.
    """
    t = np.asarray(knots, dtype=np.float64)
    if t.ndim != 1 or t.size < 3 or not np.isfinite(t).all() or np.any(np.diff(t) <= 0):
        raise ValueError('strictly increasing finite knots required')
    n = t.size - 1
    h = np.diff(t)
    A = np.zeros((n + 1, n + 1))
    Y = np.zeros((n + 1, n + 1))
    A[0, 0], A[0, 1] = 2.0, 1.0
    Y[0, 0], Y[0, 1] = -3.0 / h[0], 3.0 / h[0]
    for i in range(1, n):
        A[i, i - 1], A[i, i], A[i, i + 1] = 1.0 / h[i - 1], 2.0 * (1.0 / h[i - 1] + 1.0 / h[i]), 1.0 / h[i]
        Y[i, i - 1] = -3.0 / h[i - 1] ** 2
        Y[i, i] = 3.0 / h[i - 1] ** 2 - 3.0 / h[i] ** 2
        Y[i, i + 1] = 3.0 / h[i] ** 2
    A[n, n - 1], A[n, n] = 1.0, 2.0
    Y[n, n - 1], Y[n, n] = -3.0 / h[n - 1], 3.0 / h[n - 1]
    return dict(knots=t, widths=h, slopes=np.linalg.solve(A, Y))


def evaluate_cardinal(spline, at, *, allow_extrapolation=False):
    """Values V[q,j]=B_j(at_q) and s-derivatives D[q,j]. Exact unit rows at knots.

    Extrapolation (end cubic extended) only on explicit request; default raises.
    """
    t, h, M = spline['knots'], spline['widths'], spline['slopes']
    q = np.atleast_1d(np.asarray(at, dtype=np.float64))
    n = t.size - 1
    if not np.isfinite(q).all():
        raise ValueError('finite evaluation points required')
    if not allow_extrapolation and (np.any(q < t[0]) or np.any(q > t[-1])):
        raise ValueError('evaluation outside [t0, tn]: no extrapolation')
    k = np.clip(np.searchsorted(t, q, side='right') - 1, 0, n - 1)
    hk = h[k]
    u = (q - t[k]) / hk
    H00, H10 = (2 * u - 3) * u * u + 1, ((u - 2) * u + 1) * u
    H01, H11 = (3 - 2 * u) * u * u, (u - 1) * u * u
    dH00, dH10 = 6 * u * (u - 1), (3 * u - 1) * (u - 1)
    dH01, dH11 = 6 * u * (1 - u), u * (3 * u - 2)
    rows = np.arange(q.size)
    V = np.zeros((q.size, n + 1))
    D = np.zeros((q.size, n + 1))
    V[rows, k] += H00
    V[rows, k + 1] += H01
    V += (hk * H10)[:, None] * M[k, :] + (hk * H11)[:, None] * M[k + 1, :]
    D[rows, k] += dH00 / hk
    D[rows, k + 1] += dH01 / hk
    D += dH10[:, None] * M[k, :] + dH11[:, None] * M[k + 1, :]
    return V, D


def legendre(zeta, degree=7):
    """P_a(zeta), P'_a(zeta), a=0..degree, by recurrence (independent of legvander/legder)."""
    z = np.asarray(zeta, dtype=np.float64)
    P = np.empty(z.shape + (degree + 1,))
    dP = np.empty_like(P)
    P[..., 0], dP[..., 0] = 1.0, 0.0
    P[..., 1], dP[..., 1] = z, 1.0
    for a in range(1, degree):
        P[..., a + 1] = ((2 * a + 1) * z * P[..., a] - a * P[..., a - 1]) / (a + 1)
        dP[..., a + 1] = dP[..., a - 1] + (2 * a + 1) * P[..., a]
    return P, dP


def nodal_radial_derivative(*, radial_nodes_m, outer_radius_m):
    """v001 definition: d/dR of the natural cubic spline with knots at the nodes' s values."""
    R = np.asarray(radial_nodes_m, dtype=np.float64)
    L = float(outer_radius_m)
    s = (R / L) ** 2
    _, Ds = evaluate_cardinal(natural_cubic_cardinal(s), s)
    return (2 * R / L ** 2)[:, None] * Ds


def annular_scalar_maps(*, radial_nodes_m, radial_RdR_weights_m2, outer_radius_m, roots_m,
                        z_nodes_m, z_weights_m, edge_tolerance_s, weight_tolerance_s,
                        root_radial_derivatives_m=None, legendre_degree=7):
    """Contract scalar maps on annular knots: V=B_j P_a, d_R V, d_z V (rows i*nq+l, cols j*8+a).

    root_radial_derivatives_m: (nr,2) [lower_R, upper_R] to preserve (contract item 3); if None,
    they are recomputed with the v001 nodal-spline definition (oracle's own spline).
    """
    rec = recover_annular_edges(radial_nodes_m=radial_nodes_m, radial_RdR_weights_m2=radial_RdR_weights_m2,
                                outer_radius_m=outer_radius_m, edge_tolerance_s=edge_tolerance_s,
                                weight_tolerance_s=weight_tolerance_s)
    R = np.asarray(radial_nodes_m, dtype=np.float64)
    wr = np.asarray(radial_RdR_weights_m2, dtype=np.float64)
    L = float(outer_radius_m)
    roots = np.asarray(roots_m, dtype=np.float64)
    z = np.asarray(z_nodes_m, dtype=np.float64)
    wz = np.asarray(z_weights_m, dtype=np.float64)
    nr = R.size
    if roots.shape != (nr, 2) or z.ndim != 2 or z.shape[0] != nr or wz.shape != z.shape:
        raise ValueError('geometry shapes')
    center = (roots[:, 0] + roots[:, 1]) / 2
    height = (roots[:, 1] - roots[:, 0]) / 2
    if np.any(height <= 0):
        raise ValueError('positive half-heights required')
    zeta = (z - center[:, None]) / height[:, None]
    if root_radial_derivatives_m is None:
        DRn = nodal_radial_derivative(radial_nodes_m=R, outer_radius_m=L)
        cR, hR = DRn @ center, DRn @ height
        derivative_source = 'oracle recomputation of the v001 72-knot nodal-spline definition'
    else:
        rd = np.asarray(root_radial_derivatives_m, dtype=np.float64)
        if rd.shape != (nr, 2):
            raise ValueError('root radial derivatives (nr,2) required')
        cR, hR = (rd[:, 0] + rd[:, 1]) / 2, (rd[:, 1] - rd[:, 0]) / 2
        derivative_source = 'caller-supplied preserved root radial derivatives'
    sp = natural_cubic_cardinal(rec['knots'])
    Bv, Bs = evaluate_cardinal(sp, rec['s_nodes'])
    Bout, _ = evaluate_cardinal(sp, [1.0])
    BR = (2 * R / L ** 2)[:, None] * Bs
    P, dP = legendre(zeta, legendre_degree)
    nk, na, nq = Bv.shape[1], legendre_degree + 1, z.shape[1]
    slope = (cR[:, None] + zeta * hR[:, None]) / height[:, None]          # = -d zeta/dR at fixed z
    V = Bv[:, None, :, None] * P[:, :, None, :]
    VR = BR[:, None, :, None] * P[:, :, None, :] - Bv[:, None, :, None] * (dP * slope[:, :, None])[:, :, None, :]
    VZ = Bv[:, None, :, None] * (dP / height[:, None, None])[:, :, None, :]
    shape = (nr * nq, nk * na)
    arrays = dict(value=V.reshape(shape), partial_R=VR.reshape(shape), partial_z=VZ.reshape(shape),
                  outer_coefficient_trace=np.kron(Bout, np.eye(na)),
                  radial_value=Bv, radial_derivative=BR, radial_s_derivative=Bs,
                  weights_RdRdz=(wr[:, None] * wz).reshape(-1), zeta=zeta, roots_m=roots,
                  root_radial_derivatives=np.stack((cR - hR, cR + hR), axis=-1),
                  annular_edges_s=rec['knots'])
    return dict(arrays=arrays, trial_shape=[nk, na], quadrature_shape=[nr, nq], recovery=rec,
                spline=sp, center=center, height=height, center_R=cR, height_R=hR,
                derivative_source=derivative_source)


def regular_helicity_maps(*, value, partial_R, partial_z, outer_coefficient_trace, radial_nodes_m,
                          outer_radius_m, m, rank_relative_tolerance, rank_absolute_tolerance,
                          nullspace='qr'):
    """Contract helicity maps for any nscalar (152 annular; 576 reproduces v001 sizes)."""
    V = np.asarray(value, dtype=np.float64)
    VR = np.asarray(partial_R, dtype=np.float64)
    VZ = np.asarray(partial_z, dtype=np.float64)
    T = np.asarray(outer_coefficient_trace, dtype=np.float64)
    R = np.asarray(radial_nodes_m, dtype=np.float64)
    L = float(outer_radius_m)
    if type(m) is not int or not 1 <= m <= 6:
        raise ValueError('m in 1..6')
    n = V.shape[1]
    if VR.shape != V.shape or VZ.shape != V.shape or T.shape[1] != n or V.shape[0] % R.size:
        raise ValueError('scalar map shapes')
    rr = np.repeat(R, V.shape[0] // R.size)
    exps = (abs(m + 1), abs(m - 1), abs(m))
    f = [(rr / L) ** e for e in exps]
    vals = [fe[:, None] * V for fe in f]
    norms = np.concatenate((np.sqrt(0.5) * np.linalg.norm(vals[0], axis=0),
                            np.sqrt(0.5) * np.linalg.norm(vals[1], axis=0),
                            np.linalg.norm(vals[2], axis=0)))
    if not np.isfinite(norms).all() or np.any(norms <= 0):
        raise ValueError('zero/nonfinite column norm')
    Braw = np.hstack((0.5 * T, 0.5 * T, np.zeros_like(T)))
    Bn = Braw / norms[None, :]
    sv = np.linalg.svd(Bn, compute_uv=False)
    thr = float(rank_absolute_tolerance + rank_relative_tolerance * sv[0])
    common = dict(m=m, regularity_exponents=list(exps), column_norms=norms, hard_constraint_raw=Braw,
                  hard_constraint_normalized=Bn, hard_singular_values=sv, rank_threshold=thr)
    if sv[-1] <= thr:
        return dict(status='UNRESOLVED_OUTER_CONSTRAINT_RANK', **common)
    k = Bn.shape[0]
    if nullspace == 'qr':
        Q, _ = np.linalg.qr(Bn.T, mode='complete')
        Z = Q[:, k:]
    elif nullspace == 'eigh':
        # Different orthonormal basis of the same nullspace (LAPACK's wide SVD reuses the
        # Householder LQ and reproduces the QR basis bitwise, so it is no independent test).
        Z = np.linalg.eigh(Bn.T @ Bn)[1][:, :Bn.shape[1] - k]
    else:
        raise ValueError("nullspace must be 'qr' or 'eigh'")
    raw = Z / norms[:, None]
    plus, minus, vert = raw[:n], raw[n:2 * n], raw[2 * n:]

    def components(parts):
        p, q = parts[0] @ plus, parts[1] @ minus
        return (L / 2) * (p + q), (L / 2j) * (p - q), L * (parts[2] @ vert)

    out = dict(status='REGULAR_HELICITY_MAPS', **common, normalized_nullspace=Z, raw_coefficient_transform=raw,
               hard_nullspace_residual_norm=float(np.linalg.norm(Bn @ Z)))
    out['UR'], out['UP'], out['UZ'] = components(vals)
    out['partial_R_UR'], out['partial_R_UP'], out['partial_R_UZ'] = components(
        [fe[:, None] * VR + (e / rr)[:, None] * ve for e, fe, ve in zip(exps, f, vals)])
    out['partial_z_UR'], out['partial_z_UP'], out['partial_z_UZ'] = components([fe[:, None] * VZ for fe in f])
    out['divU'] = out['partial_R_UR'] + out['UR'] / rr[:, None] + 1j * m * out['UP'] / rr[:, None] + out['partial_z_UZ']
    return out


def scalar_basis_at(*, spline, R, z, outer_radius_m, center, height, legendre_degree=7):
    """V rows at arbitrary points (R, z) with caller-supplied center(R), height(R) (for FD checks)."""
    R = np.asarray(R, dtype=np.float64)
    L = float(outer_radius_m)
    Bv, _ = evaluate_cardinal(spline, (R / L) ** 2)
    P, _ = legendre((np.asarray(z, dtype=np.float64) - center) / height, legendre_degree)
    return (Bv[:, :, None] * P[:, None, :]).reshape(R.size, -1)


def helicity_fields_at(*, scalar_rows, R, outer_radius_m, m, raw_coefficient_transform):
    """U_R, U_phi, U_z rows (points x reduced) at arbitrary points from V rows and raw transform."""
    R = np.asarray(R, dtype=np.float64)
    L = float(outer_radius_m)
    n = scalar_rows.shape[1]
    raw = raw_coefficient_transform
    f = [(R / L) ** e for e in (abs(m + 1), abs(m - 1), abs(m))]
    p = (f[0][:, None] * scalar_rows) @ raw[:n]
    q = (f[1][:, None] * scalar_rows) @ raw[n:2 * n]
    return (L / 2) * (p + q), (L / 2j) * (p - q), L * ((f[2][:, None] * scalar_rows) @ raw[2 * n:])
