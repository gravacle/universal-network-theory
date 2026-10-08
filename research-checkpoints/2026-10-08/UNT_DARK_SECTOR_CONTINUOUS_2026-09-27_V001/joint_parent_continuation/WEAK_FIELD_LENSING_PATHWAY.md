# Light bending from the same conditional metric/source law

2026-09-28. Analytical derivation and saved-field readiness check. No new
force solve, lensing-data fit, propagation or frozen-source edit.

## The answer at the disk calculation's order

For the specified stationary, weak-metric, aligned-clock branch, slow matter
and light respond to the same solved potential. Circular motion measures
`v_c^2=R*Phi_R(R,0)`; leading light bending measures the line integral of
`2*grad_perp Phi/c^2`. There is no independent leading lensing enhancement
or slip parameter to fit. This is a consequence of the explicitly adopted
relativistic interface, not of the nonrelativistic force law alone.

The full saved `phi[R,z]` fields are sufficient for a first postprocessing
test. Midplane circular speeds alone would not be sufficient. The minimum
new observable is the physical bending vector as a function of sky impact
position, retaining each source and boundary alternative.

## 1. Retain the actual adopted action

Use coordinates x0=ct, signature (-+++), minimal universal matter coupling,
and

    S=c^3/(16*pi*G) integral sqrt(-g)[R-2J(Y)] d^4x + S_m,
    u_mu=-partial_mu T/sqrt(-partial T squared),
    a_mu=u^nu nabla_nu u_mu,  Y=a_mu*a^mu,
    J_Y=mu(c^2*sqrt(Y))-1,  K_clock=0.

This is the known preferred-foliation framework, not a newly derived native
BS action. The action and weak-field construction are supplied by
[Blanchet and Marsat, sections II and IV](https://arxiv.org/pdf/1107.5264).
The current J uses the previously declared mechanical force and
`J(infinity)=0` matching; no extra term is added here. Its nonzero J(0)
sets the already discussed homogeneous background. Galaxy perturbations
must be matched to that background, not to an asserted globally flat vacuum.
Here J(infinity) means the high-acceleration Y limit, not spatial infinity;
the isolated large-radius field instead approaches low acceleration and J(0).

## 2. Why the leading scalar slip vanishes

Write the local scalar metric, after separating the homogeneous background,
as

    ds^2=-(1+2Phi/c^2)c^2 dt^2
          +(1-2Psi/c^2) d x^2 + higher-order scalar/vector/tensor terms.

Assume `|Phi|/c^2, |Psi|/c^2 <<1`, nonrelativistic ordinary stresses, a
quasistatic source, and the clock normal aligned with the stationary time
direction at the retained order. Then `a_i=partial_i Phi/c^2`.

The exact K=0 clock tensor already checked in `FULL_RESPONSE_PRESSURE.md`
is, in physical units,

    T_J^(mu nu)=c^4/(8*pi*G)
       [-J*g^(mu nu)+2f*a^mu*a^nu-2D*u^mu*u^nu],
    f=J_Y,  D=nabla_mu(f*a^mu).

Its lapse/density term contains two spatial derivatives of Phi and enters
the leading 00 equation. Its spatial anisotropy contains *two* acceleration
factors and enters one scalar post-Newtonian order later. In particular,
the leading local equations, with the background part subtracted, are

    Delta Psi + div[f*grad Phi] = 4*pi*G*rho_b,
    [delta_ij*Delta-partial_i partial_j](Phi-Psi)=0.          (1)

The trace of the second equation gives Delta(Phi-Psi)=0; substituting it
back gives a zero Hessian. The leading difference is therefore at most an
affine homogeneous term on a regular connected patch. The same background,
frame and boundary matching remove that freedom. Importantly, this argument
does not require setting the logarithmic galaxy potential to zero at infinity.
It yields

    Phi=Psi at metric order c^-2,
    div[mu(|grad Phi|)*grad Phi]=4*pi*G*rho_b.                (2)

This agrees with the cited weak-field result; equations (1)-(2) also show
directly which stress/order assumption supplies it. Small acceleration
relative to a0 is not the metric expansion parameter. One can retain the
full nonlinear mu while the dimensionless metric potentials remain small.

At the next scalar order, the clock anisotropic stress is nonzero:

    pi_ij[J]=f/(4*pi*G)
       [partial_i Phi partial_j Phi-delta_ij*|grad Phi|^2/3]
       + higher-order terms.                             (3)

It contributes at metric order c^-4, together with the ordinary kinetic
stresses and nonlinear Einstein terms. Calculating only (3) would not be a
complete post-Newtonian slip calculation. Rotational gravitomagnetic terms
also affect photon propagation at higher order than the scalar calculation
used here. The present disk fields do not contain those corrections.

The proper-slice averaged pressure identity in `FULL_RESPONSE_PRESSURE.md`
does not replace (1). Lensing is determined by the local metric and its
boundary conditions, not by inserting an averaged rho+3p into a halo formula.

## 3. What the clock and boundaries can change

Clock alignment is a physical branch selection, not something an arbitrary
time-dependent matter distribution guarantees. With the controlled
slow-motion expansion `T=t+sigma/c^2`, define

    Xi=Phi-sigma_dot+|grad sigma|^2/2.

At K=0 the leading lapse equation becomes
`Delta Phi+div[J_Y*grad Xi]=4*pi*G*rho_b`, with J_Y evaluated on
`|grad Xi|^2/c^4`; the clock has its own evolution equation. This follows
from the primary expansion in
[Blanchet and Skordis, section 3](https://arxiv.org/html/2404.06584v2),
specialized to K=0. Leading Phi=Psi can still hold while the actual Phi is
different from the stationary disk solution. Time-dependent clock effects
need not be a small correction to the modified force; see
[Flanagan's slow-motion analysis](https://arxiv.org/pdf/2302.14846).

For the selected stationary, zero-shift leading configuration with T=t,
the clock current equation is consistent: its remaining current is along
the time normal with time-independent coefficients. This verifies that the
selected branch exists; it does not show that formation or evolution selects
it. A clock state outside the assumed slow-motion hierarchy, relativistic
matter anisotropic stress, independently supplied metric perturbations,
or different cosmological/environmental matching requires solving the full
system before reusing (2).

The positive J0 background is negligible locally only in its actual scale
hierarchy. It affects large-distance metric matching and angular-diameter
distances. It is neither a new local lensing mass nor permission to extend
a static isolated logarithmic potential through the cosmological horizon.

## 4. Original photon and axisymmetric projection calculation

To first scalar order the null condition gives optical path index
`n_optical=1-(Phi+Psi)/c^2`. Variation of that path gives the physical
transverse ray-direction change

    Delta n_perp= -1/c^2 integral grad_perp(Phi+Psi) d ell.

Use the usual lens-equation convention in which the positive deflection
vector is the negative of this direction change:

    alpha_hat(b)=1/c^2 integral grad_perp(Phi+Psi) d ell
                =2/c^2 integral grad_perp Phi d ell.          (4)

For a centrally attractive potential its radial component points outward
in image-impact coordinates; the actual light ray bends inward. This fixes
the sign rather than changing the sign of a stored radial gradient.

Let X be sky distance along the projected major axis, Y along the minor
axis, and i the disk inclination. A straight unperturbed ray can be written
in disk coordinates as

    x_d=X,
    y_d=Y*cos(i)+ell*sin(i),
    z_d=-Y*sin(i)+ell*cos(i),
    R=sqrt(X^2+y_d^2).

An axisymmetric potential then gives

    partial_X Phi = Phi_R*X/R,
    partial_Y Phi = Phi_R*(y_d/R)*cos(i)-Phi_z*sin(i).         (5)

Use even reflection of Phi across the disk plane and odd reflection of
Phi_z. The axis value is its regular limit, not a division by zero. For a
face-on ray (i=0), the result reduces to

    alpha_hat_R(b)=4/c^2 integral_0^infinity Phi_R(b,z) dz.    (6)

For a thin lens at specified distances the observed reduced deflection is
`(D_LS/D_S)*alpha_hat`, and the lens equation is
`beta=theta-(D_LS/D_S)*alpha_hat(D_L*theta)`. Those distances and source
redshift are additional observational inputs; the physical bending (4)
does not require inventing them. A position angle only rotates (5) on the
sky, so principal-axis templates need no new angle fit.

One may define `rho_eff=Delta Phi/(4*pi*G)` as a geometric diagnostic. It
is not an independently supplied dark-matter distribution. Projecting it
into convergence is equivalent to (4) only if the longitudinal boundary
term is retained or vanishes:

    integral Delta_perp Phi d ell
       =4*pi*G*integral rho_eff d ell-[partial_ell Phi]_ends.

Applying mu to a projected baryonic density or to a Newtonian deflection
does not solve this nonlinear three-dimensional lens problem.

## 5. A distinctive far-field relation and the logarithmic boundary issue

For a finite isolated baryonic mass in the deep spherical regime,

    Phi_r=v_infinity^2/r,  v_infinity^4=G*M_b*a0.

Substitution into (4) gives the formal isolated asymptotic relation

    |alpha_hat|=2*pi*v_infinity^2/c^2,                       (7)

independent of impact magnitude within that ideal regime. Thus the same
asymptotic circular-speed amplitude fixes the bending amplitude; no separate
lensing halo normalization enters. A finite disk at finite radius must
instead use its actual field and (5), not impose (7).

The logarithmic Phi itself cannot be normalized to a finite value at spatial
infinity. Nevertheless its transverse-gradient integral converges: for a
deep monopole integrated only to `-Z<ell<Z`,

    alpha_inside=4*v_infinity^2/c^2 *atan(Z/b),
    alpha_formal_tail=2*pi*v_infinity^2/c^2-alpha_inside.

For Z much greater than b, that tail is approximately
`4*v_infinity^2*b/(c^2*Z)`. This is an exact diagnostic of the chosen deep
monopole continuation, not a bound on all possible environmental or
cosmological exteriors. Projected potential differences can be defined by
subtracting a reference impact before integration; the absolute divergent
projected potential is not an observable time delay.

Actual outer matching, external fields and the clock background can alter
the asymptotic region. The current finite-box spherical boundary is one
declared approximation, not a solved cosmological lens. Report its interior
and exterior bending separately and compare the already saved larger-domain
fields. The new observational prediction is conditional and falsifiable,
not a statement that a rotation-curve fit already validates lensing.

## 6. Saved fields make a small next calculation possible

Read-only source inspection verified the original 16 galaxy cases and four
stellar-calibration cases retain full cell-center potential arrays, radii,
N, box extent, source masses and custody links. One inspected N512 case has
a 512 by 512 array on the positive R,z quadrant. The normalization in
`galaxy_density.py` and the boundary/force construction is

    Phi[(km/s)^2]=A0_KMS2_KPC*phi_numeric,

where the numerical coordinates are kpc, and derivatives of phi are
accelerations in a0 units. Therefore line integration in kpc uses the factor
`2*A0_KMS2_KPC/c_kms^2`. Calling phi merely dimensionless without this
length convention would lose a scale factor.

`SAVED_POTENTIAL_LENSING_PROTOCOL.md` defines an inert all-source,
face-on/72-degree projection using those fields. Its continuous outer
completion, interpolation convention and numerical controls are explicit.
It changes neither the solved field nor the source/action and requires no
new lattice propagation. No lensing observable has been evaluated in this
analytical note.
