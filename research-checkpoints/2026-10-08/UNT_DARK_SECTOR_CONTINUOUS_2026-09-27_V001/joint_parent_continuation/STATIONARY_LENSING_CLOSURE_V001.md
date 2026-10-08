# The same static solution must predict motion and light bending

2026-09-29. Analytical consequence of the explicitly adopted covariant parent
and its conditional radial-scalar equilibrium. This is not an observational
lensing test or a derivation of that parent from native BS dynamics. It gives
a cheap Stage-3 consistency target for any subsequent static solution.
Photons and test bodies are assumed to couple minimally to this same metric,
with null and timelike geodesics respectively. This explicit physical
dictionary is not yet derived from native carrier/photon calculations.

## Exact geometry, without a separate lensing profile

Use c=1, M²=(8 pi G)^-1, areal radius r, and a static spherical region

    ds²=-N(r)² dt²+dr²/f(r)+r² dOmega²,
    f=1-2G m(r)/r,    nu=N'/N.

Here m includes the total density of the chosen static solution, including
any vacuum term; no second cosmological constant is inserted into f. Where
these coordinates are regular, the independent Einstein equations are

    m'=4 pi r² rho,
    nu=G[m+4 pi r³ p_r]/[r² f].                         (1)

Anisotropic stress obeys

    p_r'=-(rho+p_r)nu+2(p_t-p_r)/r.                     (2)

The shared-state closure already supplies, with its original C and DeltaU,

    rho_mode=C[E+DeltaU+a F+(r²F)' sqrt(f)/r²],
    p_r,mode=C[Pi-DeltaU-a F],
    p_t,mode=C[Pi-DeltaU],
    a=sqrt(f) nu,  F=Bbar h'(a),  N omega_j=mu_j.        (3)

Ordinary matter stress must be included as well. These are the same fields
used in (1), not a second fitted mass or an independently adjustable light
coupling. Equation (2) is already an exact identity for (3) on the specified
averaged branch, with the angular pressure term retained.

The speed of an allowed circular timelike geodesic, measured by a local
static observer, is exactly

    v_circ²=r nu.                                      (4)

Existence requires 0<r nu<1; stability is an additional condition, not
guaranteed by this formula. Actual disk kinematics need their own geometry;
this spherical relation is not a replacement for a disk solution.

## Null propagation uses both metric functions

For a future-directed equatorial null ray, E_gamma=N² tdot>0 and
L_gamma=r² phidot are constants. Dots here denote affine derivatives, and
take the unsigned impact parameter b=|L_gamma|/E_gamma>=0. Direct
substitution in ds²=0 gives

    rdot²=f E_gamma² [N^-2-b²/r²],
    |dphi/dr|= b/[r² sqrt(f) sqrt(N^-2-b²/r²)],
    |dt/dr|=1/[N sqrt(f) sqrt(1-b² N²/r²)].             (5)

The turning point satisfies b=r_min/N(r_min). These integrals between the
actual source/observer boundaries determine angular transfer and travel time.
A local static observer measures the unsigned angular sine sin(alpha)=b N/r.
For a fixed static observer, elapsed proper time is N_obs times the coordinate
time interval. Coordinate b changes
under constant time normalization with N, but the local angle does not.

If the whole exterior is genuinely asymptotically flat with N->1 and f->1,
one can form the usual total deflection by integrating the angular expression
from r_min to infinity twice and subtracting pi. The present positive-vacuum
candidate is NOT globally asymptotically flat. Its finite cosmological
matching and observer geometry must be supplied instead; using the
infinite-flat formula there would be an uncontrolled extra assumption.

## A weak-field diagnostic that exposes the pressure prediction

In a weak static region, introduce isotropic spatial coordinates and write

    ds²=-(1+2Phi)dt²+(1-2Psi)(dvarrho²+varrho²dOmega²).

To first metric order the areal-to-isotropic change gives
Psi'=G m/r², while (1) gives Phi'=G[m+4 pi r³p_r]/r².
Primes here may be identified with areal derivatives only to that order.
Thus the local dynamical and lensing-potential mass diagnostics are

    M_dyn=r² Phi'/G=m+4 pi r³ p_r,
    M_lens=r²(Phi'+Psi')/(2G)=m+2 pi r³ p_r,
    M_dyn-M_lens=2 pi r³ p_r.                            (6)

M_lens is a local three-dimensional potential diagnostic. A measured lensing
mass is a line-of-sight projection using (5) or the controlled weak-lensing
integral; it is not simply the value of (6) at an image radius. For a system
embedded in a background, compare localized perturbations after consistent
background/matching subtraction. One cannot discard DeltaU in the action
while keeping its fitted expansion, or insert total vacuum pressure into a
background-subtracted observed mass formula without the same subtraction.

Equation (6) shows the testable connection: the SAME state fixes Pi, Bbar,
and hence radial pressure, so rotation and lensing are not independently
adjustable. Small local pressure contributions can give near equality;
appreciable radial pressure produces a definite difference that must be
calculated, not assumed away. The scalar coupling term -C aF is anisotropic
and must be included along with the excitation pressure and ordinary stress.

## What this closes and the next use

This specifies a conditional observable map once an admissible static
solution exists. It does not supply that solution, stability, a vector
ensemble's formation, physical clock calibration, or a measured galaxy fit.
Its equations are derived directly from the adopted metric action and
geodesics; no new phenomenological lensing function is introduced.

The next static solver should output N,f,rho,p_r,p_t together, check (1)-(3),
and evaluate both timelike and finite-boundary null readouts. A model that
fits a rotation curve but fails its resulting lensing signal would then
fail a real linked test rather than merely receive another fitted profile.
