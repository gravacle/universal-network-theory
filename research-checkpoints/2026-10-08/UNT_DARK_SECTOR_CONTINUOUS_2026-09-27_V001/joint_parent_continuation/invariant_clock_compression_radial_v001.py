"""Pure radial-constraint helpers; no data access, producer imports, or main.

The caller supplies cT and the outer chi boundary value.  Nothing here selects
that boundary, fits a parameter, propagates a source, or certifies roundoff.
kernel uses degree <= 3 interpolation of T0 in log(r), without limiting or
clipping.  Its interval integrals are analytic exponential moments, not
numerical quadrature.  The coupled helper evaluates the exact two radial
constraints at R > 0; it does not solve the boundary-value problem.
"""

import math

__all__ = ["kernel", "coupledradial_rhs"]


def _finite(value, name):
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(name + " must be finite")
    return value


def _log_ratio(numerator, denominator):
    """Preserve adjacent-node separation without overflowing a large ratio."""
    difference = numerator - denominator
    if abs(difference) <= 0.5 * denominator:
        return math.log1p(difference / denominator)
    return math.log(numerator) - math.log(denominator)


def _weighted_moments(h, rate, degree):
    """Return exp(-rate*h), and h*integral_0^1 exp(-rate*h*u)*u^k du.

    For rate*h <= 1 the convergent power series avoids recurrence
    cancellation.  Otherwise integration-by-parts recurrence is stable for
    the supported degrees 0..3.  W0 uses expm1 and 1/rate, not h/(rate*h),
    so even overflow of the product rate*h has the correct limiting form.
    """
    x = rate * h
    decay = math.exp(-x)
    if x <= 1.0:
        weights = []
        for k in range(degree + 1):
            term = 1.0 / (k + 1)
            terms = [term]
            for n in range(1, 65):
                term *= (-x / n) * ((k + n) / (k + n + 1))
                terms.append(term)
                if abs(term) <= 2.0**-54 * abs(math.fsum(terms)):
                    break
            else:
                raise ArithmeticError("exponential-moment series did not converge")
            weights.append(h * math.fsum(terms))
        return decay, weights
    weights = [-math.expm1(-x) / rate]
    for k in range(1, degree + 1):
        weights.append((k * weights[-1] - h * decay) / x)
    return decay, weights


def _interval_polynomial(r, values, i, h):
    """Power coefficients on u=log(r/r[i])/h, with p[0]=values[i].

    Four consecutive nodes containing the interval are used when available:
    one left neighbor and one right neighbor, shifted at the boundaries.
    Fewer than four input nodes give the unique lower-degree interpolant.
    Subtracting the interval's left value makes constant inputs exact.
    """
    count = min(4, len(r))
    start = max(0, min(i - 1, len(r) - count))
    nodes = [_log_ratio(r[j], r[i]) / h
             for j in range(start, start + count)]
    divided = [values[j] - values[i]
               for j in range(start, start + count)]
    for order in range(1, count):
        for j in range(count - 1, order - 1, -1):
            divided[j] = ((divided[j] - divided[j - 1])
                          / (nodes[j] - nodes[j - order]))
    polynomial = [divided[-1]]
    for j in range(count - 2, -1, -1):
        product = [0.0] * (len(polynomial) + 1)
        for k, coefficient in enumerate(polynomial):
            product[k] = math.fsum([product[k], -nodes[j] * coefficient])
            product[k + 1] = math.fsum([product[k + 1], coefficient])
        product[0] = math.fsum([product[0], divided[j]])
        polynomial = product
    polynomial[0] = values[i]
    if not all(math.isfinite(v) for v in polynomial):
        raise ArithmeticError("nonfinite interpolation coefficients")
    return polynomial


def kernel(r, T0, outerchi, cT):
    """Solve chi - cT*r*chi_R/2 = -cT*T0 inward on positive nodes.

    Parameters are finite sequences r, T0 of equal nonzero length, a finite
    outerchi at r[-1], and finite cT > 0 with representable 2/cT.  Radii
    must be strictly increasing; r=0 is deliberately excluded.

    Return (chi, chi_R), both Python lists at the supplied nodes.  chi_R is
    obtained analytically from the ODE, not by differencing the result.
    The equilibrium offset chi+cT*T0 is propagated separately, preserving
    small ODE derivatives next to a large constant equilibrium term.  Thus
    last-bit subtraction of the returned rounded chi is not a superior
    derivative oracle.  Cubic interpolation can overshoot; no positivity,
    monotonicity, outer matching, or physical acceptance is imposed here.
    """
    radii = [_finite(v, "radius") for v in r]
    values = [_finite(v, "T0") for v in T0]
    if not radii or len(radii) != len(values):
        raise ValueError("r and T0 must have the same nonzero length")
    if any(v <= 0 for v in radii):
        raise ValueError("all radii must be positive")
    if any(right <= left for left, right in zip(radii, radii[1:])):
        raise ValueError("radii must be strictly increasing")
    cT = _finite(cT, "cT")
    outerchi = _finite(outerchi, "outerchi")
    if cT <= 0:
        raise ValueError("cT must be positive")
    rate = 2.0 / cT
    if not math.isfinite(rate):
        raise ValueError("2/cT must be representable")
    chi = [0.0] * len(radii)
    offsets = [0.0] * len(radii)
    chi[-1] = outerchi
    offsets[-1] = math.fsum([outerchi, cT * values[-1]])
    for i in range(len(radii) - 2, -1, -1):
        h = _log_ratio(radii[i + 1], radii[i])
        polynomial = _interval_polynomial(radii, values, i, h)
        decay, weights = _weighted_moments(h, rate, len(polynomial) - 1)
        outer_offset = math.fsum([offsets[i + 1],
                                  cT * (values[i] - values[i + 1])])
        offsets[i] = math.fsum(
            [decay * outer_offset]
            + [-2.0 * polynomial[k] * weights[k]
               for k in range(1, len(polynomial))])
        chi[i] = math.fsum([-cT * values[i], offsets[i]])
    chi_R = [rate * offset / radius
             for offset, radius in zip(offsets, radii)]
    if not all(math.isfinite(v) for v in chi + chi_R):
        raise ArithmeticError("nonfinite kernel result")
    return chi, chi_R


def coupledradial_rhs(R, A, chi, rho0, j0, u, ur, e, cT):
    """Evaluate the coupled Hamiltonian/compression constraint at R > 0.

    rho0 and j0 are OLD-sector normal stresses, including ordinary matter,
    evaluated on the caller's canonical state.  They must not already
    include auxiliary chi stress.  u is the covariant radial vector
    component, ur its radial derivative, sigma=u/A, c=sqrt(1+sigma**2).

    Equations:
      A_R - A**2*R*sigma*chi_R/2 = F_A,
      sigma*A_R/(A**2*c**2) + R*chi_R/2 = chi/cT + T_star.

    Return a dict with A_R, chi_R, determinant, sigma, c, F_A, T_star.
    This is an algebraic RHS, not an outward chi shooting prescription.

    Center limits, NOT evaluated by passing R=0:
      A=1+rho_total(0)*R**2/6+O(R**4),
      chi(0)=-3*cT*sigma_R(0),
      rho_total(0)=rho0(0)-chi(0)**2/(2*cT).
    A regular-center mass condition and a supplied outer chi condition are
    needed.  The homogeneous chi mode R**(2/cT) can itself be regular;
    regularity alone is not an outer-boundary selection rule.
    """
    names = ("R", "A", "chi", "rho0", "j0", "u", "ur", "e", "cT")
    R, A, chi, rho0, j0, u, ur, e, cT = (
        _finite(v, name) for v, name in
        zip((R, A, chi, rho0, j0, u, ur, e, cT), names))
    if R <= 0 or A <= 0 or cT <= 0:
        raise ValueError("R, A, and cT must be positive; use center limits separately")
    sigma = u / A
    c = math.hypot(1.0, sigma)
    Ac2 = (A * c) ** 2
    F_A = math.fsum([A * (1.0 - A) * (1.0 + A) / (2.0 * R),
                    A**3 * R * (rho0 - chi**2 / (2.0 * cT)) / 2.0])
    T_star = math.fsum([-R * A * j0 / (2.0 * c), sigma * e / c,
                       ur / Ac2, 2.0 * sigma / (A * R)])
    determinant = (R / 2.0) * (1.0 + (sigma / c) ** 2)
    chi_R = math.fsum([chi / cT, T_star, -sigma * F_A / Ac2]) / determinant
    A_R = math.fsum([F_A, A**2 * R * sigma * chi_R / 2.0])
    result = dict(A_R=A_R, chi_R=chi_R, determinant=determinant,
                  sigma=sigma, c=c, F_A=F_A, T_star=T_star)
    if not all(math.isfinite(v) for v in result.values()):
        raise ArithmeticError("nonfinite coupled radial RHS")
    return result
