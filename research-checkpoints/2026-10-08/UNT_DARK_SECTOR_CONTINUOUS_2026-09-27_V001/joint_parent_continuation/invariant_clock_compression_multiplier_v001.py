"""Polar lapse/compression multipliers for the proposed -cTheta*Theta**2 term.

Source-only reusable equations: no driver import, execution, IO, integration,
clipping, source fitting, or boundary-condition selection. The caller supplies
one fixed primitive state and its independently qualified radial derivative.
``derivative(values, parity)`` returns d(values)/dR on the same grid; parity is
the string "even" or "odd" about the regular center. This module supplies no
finite-difference stencil. All evaluation points must have R > 0; a center
point requires a separate analytic limit, not division by a numerical floor.

Pr0 is REQUIRED: the original field radial pressure PLUS ordinary PrB, before
the compression stress. Its raw lapse coefficient is retained, so the radial
Hamiltonian constraint is not silently substituted into the multiplier solve.
The optional on-Hamiltonian coefficient is reported only as a diagnostic.

M=pi_phi/(2*A*R**2); P_b=A**2*j_b=sum(nu_i*p_i)/(2*R**2).
rhoB, PrB, PtB use the same action-density units as the field stresses. Their
momentum update is that of conserved collisionless ordinary matter, including
orbital support; an externally clamped density is not this source model.

The constitutive inputs must be from the SAME branch: m=K_X, d=K_XX,
q=sqrt(X**2+w**2), Q=c*q+sigma*w, p=sigma*q+c*w, e=(Z-C*p)/KB,
D=C*(e-(1+j)*p), Jcur=c*D-(m/X)*w, and jt=d[j(p**2)*p]/dp.
The original action has C=2-KB. Partial derivatives below retain 1+C/KB
explicitly rather than relying on a rounded equality to 2/KB.

Return chi_dot/N and N_R/N. The exact cancellation of (chi_dot)_R leaves a
pointwise positive-denominator branch and one lapse normalization, NOT a
second independent radial boundary condition for chi_dot. The caller still
owns the state chi constraint, physical outer matching, scalar charge flux,
ordinary matter evolution, radial Einstein constraint and boundary work.
"""

import numpy as np


class MultiplierBranchError(ValueError):
    """A declared positive branch failed; diagnostics retain the failed value."""

    def __init__(self, message, diagnostics):
        super().__init__(message)
        self.diagnostics = diagnostics


def _arrays(**values):
    names = tuple(values)
    arrays = []
    for name in names:
        if np.iscomplexobj(values[name]):
            raise ValueError(name + " must be real")
        value = np.asarray(values[name], dtype=float)
        if value.size == 0 or not np.all(np.isfinite(value)):
            raise ValueError(name + " must be nonempty and finite")
        arrays.append(value)
    return dict(zip(names, np.broadcast_arrays(*arrays)))


def _constant(name, value, positive=True):
    if np.iscomplexobj(value) or np.ndim(value) != 0:
        raise ValueError(name + " must be a real scalar")
    value = float(value)
    if not np.isfinite(value) or (positive and value <= 0):
        raise ValueError(name + " must be finite and positive")
    return value


def constitutive_partials(*, sigma, w, X, m, d, q, Q, D, jt, KB, C):
    """Analytic fixed-(M,sigma,w,Z) inverse/acceleration derivatives.

    These are evaluated at supplied consistent primitive values; no inverse
    is solved here. A nonpositive Schur is rejected BEFORE any division by it.
    """
    KB = _constant("KB", KB)
    C = _constant("C", C)
    g = _arrays(sigma=sigma, w=w, X=X, m=m, d=d, q=q, Q=Q, D=D, jt=jt)
    sigma, w, X, m, d, q, Q, D, jt = (g[k] for k in g)
    if np.any(X <= 0) or np.any(q <= 0) or np.any(d <= 0) or np.any(m < 0):
        raise ValueError("positive-X, positive-q, positive-d, nonnegative-m branch required")
    c = np.sqrt(1 + sigma*sigma)
    eta = C/KB
    slope = C*(1 + C/KB + jt)
    kinetic = d*(q/X)**2
    schur = kinetic - m*w*w/X**3 - sigma*sigma*slope
    diag = dict(Schur=schur, Schur_over_kinetic=schur/kinetic)
    if not np.all(np.isfinite(schur)) or np.any(schur <= 0):
        raise MultiplierBranchError("nonpositive or nonfinite scalar Schur", diag)
    q_M = 1/schur
    q_Z = -sigma*eta/schur
    q_w = (q*w*(d-m/X)/X**2 + sigma*c*slope)/schur
    q_sigma = (-D + sigma*slope*Q/c)/schur
    out = dict(Schur=schur, Schur_over_kinetic=schur/kinetic,
               q_M=q_M, q_Z=q_Z, q_w=q_w, q_sigma=q_sigma,
               e_M=-eta*sigma/schur, e_w=-eta*(c+sigma*q_w),
               e_sigma=-eta*(Q/c+sigma*q_sigma),
               e_Z=1/KB + eta*eta*sigma*sigma/schur)
    if any(not np.all(np.isfinite(value)) for value in out.values()):
        raise MultiplierBranchError("nonfinite constitutive partial", out)
    return out


def t0_partials(*, R, A, sigma, sigma_R, w, M, P_b, e, divZ):
    """T0 and explicit partials, treating e, divZ, sigma_R as independent."""
    g = _arrays(R=R, A=A, sigma=sigma, sigma_R=sigma_R, w=w, M=M,
                P_b=P_b, e=e, divZ=divZ)
    R, A, sigma, sigma_R, w, M, P_b, e, divZ = (g[k] for k in g)
    if np.any(R <= 0) or np.any(A <= 0):
        raise ValueError("R>0 and A>0 required; use separate analytic center limit")
    c = np.sqrt(1 + sigma*sigma)
    value = (-R*sigma*divZ/(2*c) + R*A*M*w/(2*c) - R*P_b/(2*A*c)
             + sigma*e/c + sigma_R/(A*c*c) + 2*sigma/(A*R))
    return dict(value=value,
        A=R*M*w/(2*c)+R*P_b/(2*A*A*c)-sigma_R/(A*A*c*c)-2*sigma/(A*A*R),
        sigma=(-R*divZ/(2*c**3)-R*A*M*w*sigma/(2*c**3)
               +R*P_b*sigma/(2*A*c**3)+e/c**3
               -2*sigma*sigma_R/(A*c**4)+2/(A*R)),
        w=R*A*M/(2*c), M=R*A*w/(2*c), P_b=-R/(2*A*c),
        e=sigma/c, divZ=-R*sigma/(2*c), sigma_R=1/(A*c*c))


def multipliers(*, R, A, Ar, sigma, sigma_R, w, M, Z, divZ,
                X, m, d, q, Q, p, e, D, Jcur, jt,
                rhoB, PrB, PtB, P_b, Pr0, chi, chi_R,
                KB, C, cTheta, derivative, q_R=None):
    """Return the exact local multiplier coefficients and their diagnostics.

    q_R should normally be supplied from a cancellation-safe q-minus-reference
    field. The fallback differentiates q-q.flat[0]; it cannot recover small
    spatial features already lost when q itself was rounded, and is labeled.
    Raw input consistency and state-constraint residuals are returned without
    fitting tolerances or modifying the state. Nonpositive scalar Schur or
    multiplier denominator raises MultiplierBranchError with diagnostics.
    """
    KB = _constant("KB", KB)
    C = _constant("C", C)
    cTheta = _constant("cTheta", cTheta)
    if not callable(derivative):
        raise ValueError("a qualified radial derivative callback is required")
    g = _arrays(R=R, A=A, Ar=Ar, sigma=sigma, sigma_R=sigma_R,
                w=w, M=M, Z=Z, divZ=divZ, X=X, m=m, d=d, q=q, Q=Q,
                p=p, e=e, D=D, Jcur=Jcur, jt=jt, rhoB=rhoB, PrB=PrB,
                PtB=PtB, P_b=P_b, Pr0=Pr0, chi=chi, chi_R=chi_R)
    (R, A, Ar, sigma, sigma_R, w, M, Z, divZ, X, m, d, q, Q,
     p, e, D, Jcur, jt, rhoB, PrB, PtB, P_b, Pr0, chi, chi_R) = (g[k] for k in g)
    if np.any(R <= 0) or np.any(A <= 0):
        raise ValueError("R>0 and A>0 required; center is an analytic limit")
    shape = R.shape

    def dr(value, parity):
        result = derivative(value, parity)
        if np.iscomplexobj(result):
            raise ValueError("radial derivative returned complex values")
        result = np.asarray(result, dtype=float)
        if result.shape != shape or not np.all(np.isfinite(result)):
            raise ValueError("radial derivative must return finite same-shape values")
        return result

    if q_R is None:
        q_R = dr(q-q.flat[0], "even")
        q_derivative_source = "constant_subtracted_fallback"
    else:
        if np.iscomplexobj(q_R):
            raise ValueError("q_R must be real")
        q_R = np.broadcast_to(np.asarray(q_R, dtype=float), shape)
        if not np.all(np.isfinite(q_R)):
            raise ValueError("q_R must be finite")
        q_derivative_source = "supplied"
    c = np.sqrt(1 + sigma*sigma)
    c_R = sigma*sigma_R/c
    partials = constitutive_partials(sigma=sigma, w=w, X=X, m=m, d=d,
                                    q=q, Q=Q, D=D, jt=jt, KB=KB, C=C)

    # P_b is independent of rhoB, PrB, PtB; it is never set to zero implicitly.
    j_old = sigma*divZ/A - M*w + P_b/(A*A)
    a0 = -R*(A*j_old+c*chi_R)/2
    s0 = e-c_R/A-sigma*a0
    s1 = -c/A
    s1_R = -c_R/A+c*Ar/(A*A)
    w0 = q_R/A-w*a0
    w1 = q/A
    m0 = -(dr(Jcur, "odd")+2*Jcur/R)/A-M*a0
    m1 = -Jcur/A
    z0 = Q*D/c-sigma*divZ/(A*c)-chi_R/A
    p0 = -A*(dr(PrB, "even")+2*(PrB-PtB)/R)
    p1 = -A*(rhoB+PrB)
    e0 = (partials["e_sigma"]*s0+partials["e_w"]*w0
          +partials["e_M"]*m0+partials["e_Z"]*z0)
    e1 = (partials["e_sigma"]*s1+partials["e_w"]*w1
          +partials["e_M"]*m1)
    tp = t0_partials(R=R, A=A, sigma=sigma, sigma_R=sigma_R,
                     w=w, M=M, P_b=P_b, e=e, divZ=divZ)
    b0 = (tp["A"]*A*a0+tp["sigma"]*s0+tp["w"]*w0+tp["M"]*m0
          +tp["P_b"]*p0+tp["e"]*e0
          +tp["divZ"]*(dr(z0, "odd")+2*z0/R)
          +tp["sigma_R"]*dr(s0, "odd"))
    b1 = (tp["sigma"]*s1+tp["w"]*w1+tp["M"]*m1+tp["P_b"]*p1
          +tp["e"]*e1+tp["divZ"]*z0+tp["sigma_R"]*(s0+s1_R))
    b2 = -1/(A*A*c)
    a_tau = sigma*sigma*(1-partials["e_Z"])/(c*c)+R*sigma*sigma_R/(2*c**4)
    b_tau = R*sigma*sigma/(2*c*c)

    # Raw polar lapse: Pr0 includes original field pressure AND PrB only.
    L0 = ((A-1)*(A+1)/(2*R)
          +A*A*R*(Pr0+sigma*chi_R/A+chi*chi/(2*cTheta))/2)
    L0_R = dr(L0, "odd")
    Ltau = A*A*R/(2*c)
    Ltau_R = A*A/(2*c)+A*Ar*R/c-A*A*R*sigma*sigma_R/(2*c**3)
    numerator = cTheta*(b2*(L0_R+L0*L0)+b1*L0+b0)
    denominator = 1+cTheta*(a_tau-b2*(L0*Ltau+Ltau_R)-b1*Ltau)
    coefficients = dict(a0=a0, s0=s0, s1=s1, w0=w0, w1=w1,
                        m0=m0, m1=m1, z0=z0, p0=p0, p1=p1,
                        e0=e0, e1=e1, b0=b0, b1=b1, b2=b2,
                        a_tau=a_tau, b_tau=b_tau,
                        L0=L0, L0_R=L0_R, Ltau=Ltau, Ltau_R=Ltau_R)
    if (not np.all(np.isfinite(denominator)) or np.any(denominator <= 0)
            or not np.all(np.isfinite(numerator))):
        raise MultiplierBranchError(
            "nonpositive/nonfinite compression denominator or nonfinite numerator",
            dict(denominator=denominator, numerator=numerator,
                 scalar_Schur=partials["Schur"], coefficients=coefficients))
    chi_dot_over_N = -numerator/denominator
    lapse_gradient = L0-Ltau*chi_dot_over_N
    if not np.all(np.isfinite(chi_dot_over_N)) or not np.all(np.isfinite(lapse_gradient)):
        raise MultiplierBranchError("nonfinite multiplier", dict(
            denominator=denominator, numerator=numerator,
            chi_dot_over_N=chi_dot_over_N, lapse_gradient=lapse_gradient))

    # This alternative is diagnostic ONLY; it uses the radial Hamiltonian.
    W = (rhoB+PrB+M*q-sigma*Q*D/c-w*Jcur
         +(c+sigma*sigma/c)*divZ/A)
    L0_on_hamiltonian = -Ar/A+A*A*R*W/2+A*R*sigma*chi_R
    diagnostics = dict(
        q_derivative_source=q_derivative_source,
        minimum_scalar_Schur=float(np.min(partials["Schur"])),
        minimum_scalar_Schur_fraction=float(np.min(partials["Schur_over_kinetic"])),
        minimum_multiplier_denominator=float(np.min(denominator)),
        regular_center_denominator_limit=1+1.5*cTheta,
        state_chi_constraint=chi-cTheta*R*chi_R/2+cTheta*tp["value"],
        chi_dot_radial_derivative_coefficient=(
            -cTheta*R/2+cTheta*b_tau-cTheta*b2*Ltau),
        multiplier_algebra_residual=denominator*chi_dot_over_N+numerator,
        L0_on_hamiltonian=L0_on_hamiltonian,
        raw_minus_on_hamiltonian_L0=L0-L0_on_hamiltonian,
        q_norm_residual=q*q-X*X-w*w,
        Q_residual=Q-c*q-sigma*w,
        p_residual=p-sigma*q-c*w,
        source_Z_residual=Z-KB*e-C*p,
        scalar_momentum_residual=M-m*q/X-sigma*D,
        scalar_current_residual=Jcur-c*D+(m/X)*w,
        action_coefficient_residual=C+KB-2)
    return dict(chi_dot_over_N=chi_dot_over_N, lapse_gradient=lapse_gradient,
                denominator=denominator, numerator=numerator,
                coefficients=coefficients, constitutive_partials=partials,
                T0_partials=tp, diagnostics=diagnostics)
