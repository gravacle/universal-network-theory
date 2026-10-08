"""50-digit arithmetic oracle for the generic coupled radial constraints.

V001 is preserved.  Its inward kernel is re-exported unchanged; only the
algebraic coupledradial_rhs below uses Decimal arithmetic.  This module has
no data access, integration, source fitting, boundary selection, or driver.
It is NOT a decision to use Decimal in the physical evolution solver.

Inputs may be Decimal, decimal text, Python float, or Python int.  Conversion
is exact: a float contributes its exact binary value, not a rounded decimal
rendering.  Arithmetic then uses a local 50-digit, round-half-even context.
The caller remains responsible for input consistency.  Higher precision
cannot reconstruct correlations already destroyed by independently rounding
A, chi, stress, or other inputs.  Return values have the same float-valued
dictionary interface as V001 and therefore undergo final float rounding.
"""

from decimal import Decimal, InvalidOperation, ROUND_HALF_EVEN, localcontext
import math

from invariant_clock_compression_radial_v001 import kernel

__all__ = ["kernel", "coupledradial_rhs"]
DECIMAL_PRECISION = 50


def _decimal_exact(value, name):
    """Convert supported scalar inputs without pre-rounding to context."""
    if isinstance(value, bool):
        raise TypeError(name + " must be a numeric scalar, not bool")
    if isinstance(value, Decimal):
        result = value
    elif isinstance(value, float):
        result = Decimal.from_float(value)
    elif isinstance(value, (str, int)):
        try:
            result = Decimal(value)
        except (InvalidOperation, ValueError) as error:
            raise ValueError(name + " must be valid finite decimal text or a number") from error
    else:
        raise TypeError(name + " must be Decimal, decimal text, Python float, or Python int")
    if not result.is_finite():
        raise ValueError(name + " must be finite")
    return result


def coupledradial_rhs(R, A, chi, rho0, j0, u, ur, e, cT):
    """Evaluate the same R > 0 coupled constraints as V001 at precision 50.

    rho0 and j0 are old-sector normal stresses, including ordinary matter,
    without auxiliary chi stress.  u is the covariant radial vector field;
    ur is its radial derivative.  sigma=u/A and c=sqrt(1+sigma**2).

      A_R - A**2*R*sigma*chi_R/2 = F_A,
      sigma*A_R/(A**2*c**2) + R*chi_R/2 = chi/cT + T_star.

    Return float entries A_R, chi_R, determinant, sigma, c, F_A, T_star.
    The determinant is R*(1+sigma**2/c**2)/2 > 0.  At the regular center
    use the analytic limits separately, never substitute a radius floor:

      A=1+rho_total(0)*R**2/6+O(R**4),
      chi(0)=-3*cT*sigma_R(0),
      rho_total(0)=rho0(0)-chi(0)**2/(2*cT).

    This RHS is not an outward shooting prescription.  Regular-center mass
    and caller-owned outer chi data remain distinct boundary conditions.
    """
    names = ("R", "A", "chi", "rho0", "j0", "u", "ur", "e", "cT")
    values = tuple(_decimal_exact(value, name) for value, name in
                   zip((R, A, chi, rho0, j0, u, ur, e, cT), names))
    R, A, chi, rho0, j0, u, ur, e, cT = values
    if R <= 0 or A <= 0 or cT <= 0:
        raise ValueError("R, A, and cT must be positive; use center limits separately")

    with localcontext() as context:
        context.prec = DECIMAL_PRECISION
        context.rounding = ROUND_HALF_EVEN
        one = Decimal(1)
        two = Decimal(2)
        sigma = u / A
        c = (one + sigma * sigma).sqrt()
        Ac2 = (A * c) ** 2
        F_A = (A * (one - A) * (one + A) / (two * R)
               + A**3 * R * (rho0 - chi**2 / (two * cT)) / two)
        T_star = (-R * A * j0 / (two * c) + sigma * e / c
                  + ur / Ac2 + two * sigma / (A * R))
        determinant = (R / two) * (one + (sigma / c) ** 2)
        chi_R = (chi / cT + T_star - sigma * F_A / Ac2) / determinant
        A_R = F_A + A**2 * R * sigma * chi_R / two
        decimal_result = dict(A_R=A_R, chi_R=chi_R, determinant=determinant,
                              sigma=sigma, c=c, F_A=F_A, T_star=T_star)
        if not all(value.is_finite() for value in decimal_result.values()):
            raise ArithmeticError("nonfinite Decimal coupled radial RHS")
        result = {name: float(value) for name, value in decimal_result.items()}
    if not all(math.isfinite(value) for value in result.values()):
        raise ArithmeticError("coupled radial RHS is not representable as finite floats")
    return result
