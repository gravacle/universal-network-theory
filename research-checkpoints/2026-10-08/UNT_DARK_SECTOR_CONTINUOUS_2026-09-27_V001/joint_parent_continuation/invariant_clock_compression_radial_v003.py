"""Even-radius inward compression kernel; source only, no execution or IO.

V001's log-radius polynomial is not exact for regular T0=T00+T2*R**2
at the first midpoint cells. Those cells keep finite radius ratios under
refinement, allowing an O(h_grid) chi_R artifact there. This version uses
the SAME differential equation and supplied outer boundary, but a cubic
interpolant in R**2. No center clamp, filter, clipping or physical change.

On each interval y=(R**2-ri**2)/(rnext**2-ri**2). Its inward exponential
moments are evaluated by convergent analytic series with positive terms,
not quadrature or subtraction of nearly equal exponential moments. This
also handles the a=2*j resonances without a special physical prescription.
Long log intervals are composed from fixed h<=1 analytic intervals using
positive binomial coefficients. Moment caching depends only on the grid
and cT, never the state or result. These are floating-point formulas, not
a certified roundoff bound; independent qualification remains required.

kernel(r,T0,outerchi,cT) returns (chi,chi_R), as V001. The unchanged binary
coupledradial_rhs is re-exported explicitly; V002's separate Decimal oracle
and every prior source/result remain intact. This file has no driver.
"""

import math
from functools import lru_cache

from invariant_clock_compression_radial_v001 import (
    _finite, _log_ratio, coupledradial_rhs,
)

__all__ = ["kernel", "coupledradial_rhs"]
SERIES_RELATIVE_STOP = 2.0**-55


def _positive_unit_moment(n, x):
    """Integral_0^1 exp(-x*u)*u**n du by a positive analytic series.

    exp(-x)*sum_j x**j*n!/(n+j+1)! is used only for x<=512,
    so neither its largest term nor exp(-x) over/underflows. No alternating
    subtraction is needed. The recurrence tail is stopped only once its
    term ratio is below one half and its term is below the declared scale.
    """
    if x < 0 or x > 512:
        raise ValueError("positive unit-moment series requires 0<=x<=512")
    term = 1.0/(n+1)
    terms = [term]
    for j in range(1, 2049):
        ratio = x/(n+j+1)
        term *= ratio
        terms.append(term)
        total = math.fsum(terms)
        if ratio <= .5 and term <= SERIES_RELATIVE_STOP*total:
            return math.exp(-x)*total
    raise ArithmeticError("positive unit-moment series failed to converge")


@lru_cache(maxsize=8192)
def _small_interval_moments(h, rate, degree):
    """Exact-series moments on 0<h<=1, with positive coefficient recurrence.

    For z=2h, let a[n,j]=j!*S(n,j)*z**(n-j)/n!, where S are Stirling
    numbers of the second kind. Then
      a[n+1,j]=(j*z*a[n,j]+j*a[n,j-1])/(n+1),
      I_j=h*(z/expm1(z))**j*sum_n a[n,j]*E_n(rate*h).
    All retained summands are nonnegative. E_n uses a positive series near
    its recurrence's ill-conditioned region; its upward recurrence is
    used only with n<=x/2 and x>64, where it is contractive.
    """
    if not 0 < h <= 1 or not 0 <= degree <= 3:
        raise ValueError("invalid small-interval moment arguments")
    x, z = rate*h, 2*h
    En = -math.expm1(-x)/x if x else 1.0
    if degree == 0:
        return (h*En,)
    scale = z/math.expm1(z)
    coefficients = [1.0] + [0.0]*degree
    sums = [[En]] + [[] for _ in range(degree)]
    endpoint = math.exp(-x)
    for n in range(1, 257):
        coefficients = [0.0] + [
            j*(z*coefficients[j]+coefficients[j-1])/n
            for j in range(1, degree+1)]
        if x <= 64 or n > x/2:
            # With n<=256, the second branch implies x<512.
            En = _positive_unit_moment(n, x)
        else:
            En = (n*En-endpoint)/x
        if not math.isfinite(En) or En < 0:
            raise ArithmeticError("invalid nonnegative analytic moment")
        increments = [coefficients[j]*En for j in range(1, degree+1)]
        for j, increment in enumerate(increments, 1):
            sums[j].append(increment)
        if n >= degree+12 and all(
                increment <= SERIES_RELATIVE_STOP*math.fsum(sums[j])
                for j, increment in enumerate(increments, 1)):
            values = tuple(h*scale**j*math.fsum(sums[j]) for j in range(degree+1))
            if not all(math.isfinite(v) and v >= 0 for v in values):
                raise ArithmeticError("nonfinite analytic interval moment")
            return values
    raise ArithmeticError("even-radius exponential moment series failed to converge")


@lru_cache(maxsize=8192)
def _interval_moments(h, rate, degree):
    """Integral exp(-rate*t)*[expm1(2t)/expm1(2h)]**k, k=0..degree."""
    if h <= 1:
        return _small_interval_moments(h, rate, degree)
    count = math.ceil(h)
    width = h/count
    small = _small_interval_moments(width, rate, degree)
    denominator = -math.expm1(-2*h)
    pieces = [[] for _ in range(degree+1)]
    for i in range(count):
        t0, t1 = i*width, (i+1)*width
        decay = math.exp(-rate*t0)
        if decay == 0:
            break
        # y_h(t0+s)=b0+b1*y_width(s); both coefficients are in [0,1].
        # This form does not overflow even when exp(2*h) would overflow.
        b0 = math.exp(-2*(h-t0))*(-math.expm1(-2*t0))/denominator
        b1 = math.exp(-2*(h-t1))*(-math.expm1(-2*width))/denominator
        for k in range(degree+1):
            value = math.fsum(math.comb(k, j)*b0**(k-j)*b1**j*small[j]
                              for j in range(k+1))
            pieces[k].append(decay*value)
    values = tuple(math.fsum(v) for v in pieces)
    if not all(math.isfinite(v) and v >= 0 for v in values):
        raise ArithmeticError("nonfinite composed interval moment")
    return values


def _even_interval_polynomial(r, values, i):
    """Cubic/lower interpolant in local even coordinate y, p[0]=T0[i].

    Four consecutive existing nodes contain the interval when available.
    All coordinates depend on R**2, so the implicit extension is even at
    the origin. Subtract the left value before divided differences; this
    makes constant T0 exact. No new central datum or derivative is fitted.
    """
    count = min(4, len(r))
    start = max(0, min(i-1, len(r)-count))
    scale = max(r[start:start+count])
    left, right = r[i], r[i+1]
    denominator = ((right-left)/scale)*(right/scale+left/scale)
    if denominator <= 0 or not math.isfinite(denominator):
        raise ArithmeticError("unrepresentable even interpolation interval")
    nodes = [((r[j]-left)/scale)*(r[j]/scale+left/scale)/denominator
             for j in range(start, start+count)]
    divided = [values[j]-values[i] for j in range(start, start+count)]
    for order in range(1, count):
        for j in range(count-1, order-1, -1):
            span = nodes[j]-nodes[j-order]
            if span <= 0 or not math.isfinite(span):
                raise ArithmeticError("unrepresentable even interpolation nodes")
            divided[j] = (divided[j]-divided[j-1])/span
    polynomial = [divided[-1]]
    for j in range(count-2, -1, -1):
        product = [0.0]*(len(polynomial)+1)
        for k, coefficient in enumerate(polynomial):
            product[k] = math.fsum([product[k], -nodes[j]*coefficient])
            product[k+1] = math.fsum([product[k+1], coefficient])
        product[0] = math.fsum([product[0], divided[j]])
        polynomial = product
    polynomial[0] = values[i]
    if not all(math.isfinite(v) for v in polynomial):
        raise ArithmeticError("nonfinite even interpolation coefficients")
    return polynomial


def kernel(r, T0, outerchi, cT):
    """Solve chi-cT*R*chi_R/2=-cT*T0 inward on strictly positive radii.

    No R=0 floor. The caller owns outerchi. In each interval T0's declared
    representation is cubic or lower in R**2. The equilibrium offset
    chi+cT*T0 is carried independently to avoid subtracting rounded large
    equilibrium values to recover a small derivative. Returned chi_R is
    from that offset, not a finite difference of returned rounded chi.
    """
    radii = [_finite(v, "radius") for v in r]
    values = [_finite(v, "T0") for v in T0]
    outerchi, cT = _finite(outerchi, "outerchi"), _finite(cT, "cT")
    if not radii or len(radii) != len(values):
        raise ValueError("r and T0 must have the same nonzero length")
    if any(v <= 0 for v in radii) or any(b <= a for a, b in zip(radii, radii[1:])):
        raise ValueError("radii must be positive and strictly increasing")
    if cT <= 0 or not math.isfinite(2/cT):
        raise ValueError("cT>0 with representable 2/cT required")
    rate = 2/cT
    chi, offsets = [0.0]*len(radii), [0.0]*len(radii)
    chi[-1] = outerchi
    offsets[-1] = math.fsum([outerchi, cT*values[-1]])
    for i in range(len(radii)-2, -1, -1):
        h = _log_ratio(radii[i+1], radii[i])
        polynomial = _even_interval_polynomial(radii, values, i)
        moments = _interval_moments(h, rate, len(polynomial)-1)
        decay = math.exp(-rate*h)
        outer_offset = math.fsum([offsets[i+1], cT*(values[i]-values[i+1])])
        offsets[i] = math.fsum([decay*outer_offset]
                               + [-2*polynomial[k]*moments[k]
                                  for k in range(1, len(polynomial))])
        chi[i] = math.fsum([-cT*values[i], offsets[i]])
    chi_R = [rate*offset/radius for offset, radius in zip(offsets, radii)]
    if not all(math.isfinite(v) for v in chi+chi_R):
        raise ArithmeticError("nonfinite even-radius kernel result")
    return chi, chi_R
