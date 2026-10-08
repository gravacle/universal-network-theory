# Smooth-release current coefficients without a metric solve V001

2026-09-29. Additive analytical certificate; the accepted closed-release
proof and all saved states remain unchanged. This bounds initial Taylor
coefficients, not a finite-time solution or a galaxy outcome.

Use the source D, exact constrained conformal metric psi, compactness U,
and A=4piG D/psi^6 of `SMOOTH_DISK_CLOSED_RELEASE_ORACLES_V001.md`
(SHA256 `5f5f2985167b47751aeceb78b823fb327aa58074b58e18a6d8856cd32bc7f7aa`).
Here D is SI rest mass per coordinate volume and spatial derivatives below
use physical Euclidean coordinates; c is the speed of light.

## 1. A global derivative certificate

Direct differentiation of the positive source gives

    Dmax=M(a+3b)/[4pi b(a+b)^3],

attained at the origin. At fixed zeta, differentiation with respect to R^2
has numerator -3aR^2/2-3(a+5zeta)(a+zeta)^2/2. At R=0 the remaining
factor (a+3zeta)/[zeta^3(a+zeta)^3] decreases with zeta. These prove the
maximum, rather than inferring it from a finite witness grid.

The exact positive Green representation, and psi>=1, imply

    |grad psi(x)| <= G/(2c^2) integral D(y)/|x-y|^2 d^3y
                  <= G/(2c^2) [4pi Dmax ell+M/ell^2].

Choosing ell0=[M/(2pi Dmax)]^(1/3) yields the global bound

    Bpsi=3piG Dmax ell0/c^2,       |grad psi|<=Bpsi.        (1)

This uses the exact total coordinate rest mass M; no numerical integral or
uncontrolled differentiation of a sup-norm estimate is involved.

## 2. Initial current coefficients

The physical orthonormal gradient of A is

    grad_hat A=4piG[psi^-8 grad D-6D psi^-9 grad psi].

Since 1<=psi<=1+U, 1-psi^-n<=nU. Thus

    |grad_hat A-4piG grad D|
       <=4piG[8U |grad D|+6D Bpsi] = Egrad.               (2)

Using the exact Laplacian identity in the parent proof gives independently

    |Delta_gamma A-4piG Delta D|
      <=4piG[10U |Delta D|+10Bpsi |grad D|
                         +30D Bpsi^2+12piG D^2/c^2]
       = Elap.                                           (3)

All omitted inverse powers of psi only reduce these positive upper bounds.
The term containing D^2 has its required factor c^-2. Egrad has units
s^-2 m^-1 and Elap has units s^-2 m^-2.

For the same initial hard state c_s^2=c^2 c_I^2, the cubic physical velocity
coefficient and normalized quartic canonical-current coefficient therefore
obey

    v_hat/tau^3 = -c_s^2 (4piG grad D)/6 + error,
    |error| <= c_s^2 Egrad/6;

    [(P-P0)/P0]/tau^4 = c_s^2 (4piG Delta D)/24 + error,
    |error| <= c_s^2 Elap/24.                             (4)

These expressions mean the Taylor coefficients at tau=0. They do not divide
a finite-time result by tau or assert a remainder bound. The velocity error
is a Euclidean norm bound in the initial orthonormal frame. The current
coefficient is signed; its interval must not be clipped when it spans zero.

The actual density-focusing coefficient is independently bracketed by
4piG D/(1+u)^6<=A<=4piG D. Thus a first certificate can expose both volume
focusing and delayed pressure transport using exact constrained-state
bounds, without solving a new orbit or reconstructing psi. A later finite
release must still solve/evolve the constraints, matter, current and clock.

## 3. State and interpretation

The first four old R=128/8192, b/a=1/8 or 1/16 examples are retained method
controls, not newly qualified joint cosmological candidates. Geometry need
be evaluated only once per thickness. The same identities can subsequently
be mapped to every authenticated inferred state by saved-state arithmetic,
without choosing a successful state or repeating the geometry calculation.
