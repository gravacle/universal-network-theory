# Galaxy source recipe and independent Newtonian check

2026-09-28. Analytical preflight of the parent's prospective four-profile
recipe. Read the retained baryon input and outer-H I decision. No field
worker, fitted parameter, new galaxy selection or observed-speed comparison.

## Source decision

Accept the following as an explicit **modeled, exposed development source**:

- Entire Begeman H I profile at D=13.8 Mpc, with helium factor 1.36 once.
  Keep its positive piecewise-linear radial interpolation. The measured
  angular endpoint corresponds to 46.16395871525 kpc.
- Entire Leroy stellar profile, flat from the origin to 0.3 kpc,
  piecewise-linear thereafter, and a continuous exponential beyond 15.1 kpc
  with endpoint density 2.5 solar masses/pc squared and scale 3.2 kpc.
- Leroy H2 profile with the analogous flat core and interpolation through
  6.4 kpc. Thereafter use either zero or the continuous endpoint exponential
  with density 1.2 and scale 2.7 kpc. Its tabulated gas densities already
  contain helium; do not multiply them again.
- Independently choose either zero H I beyond its endpoint or a continuous
  exponential with scale `ell_HI=Delta_R/log(.36/.14)`, where
  `Delta_R=0.5*4.014257279586958 kpc`. This is fixed from density samples,
  not from a rotation curve.

The resulting two-by-two alternatives are all retained. Their relative
agreement with velocities must not select which source is reported or
retroactively alter the tails. Stellar/H2 scale lengths are declared
published density-shape inputs, not a reason to enforce the inconsistent
table4 global mass as an equality. Keep the previous fixed constitutive
law, a0 and r; do not optimize a mass normalization.

The coplanar razor-thin construction flattens differently reduced warped
rings and discards vertical structure. It is a controlled approximation,
not a claim to have reconstructed the actual three-dimensional galaxy.
In particular, observed HI column mass must not receive an extra 15-percent
thick-gas component: thick gas is a redistribution of the observed total.

Hard endpoint truncation is mathematically permitted, but a nonzero surface
density jumping to zero produces a logarithmic razor-thin radial-field
singularity at the edge. This affects H2 at 6.4 kpc and HI at 46.164 kpc in
the truncated branches. Preserve these cases and their finite-grid effects;
do not evaluate a purported finite exact midplane force at the edge or
silently smooth it after seeing residuals. Continuous interpolation knots
can also reduce regularity, although they do not create that density-jump
singularity. No observed-speed success gate is appropriate here.

## Mass normalization is directly auditable

Use radius in kpc and tabulated Sigma in solar masses/pc squared. Every
surface-density integral therefore contains the factor `10^6`:

    M = 2*pi*10^6 * integral R*Sigma(R) dR.

For a linear segment from (ri,si) to (rj,sj), its exact contribution is

    Mseg = 2*pi*10^6 * (rj-ri)/6
           * [(2*ri+rj)*si + (ri+2*rj)*sj].

The flat-core contribution is `pi*10^6*Sigma0*R0^2`. For a continuous
exponential tail beginning at (Rt,St) with scale ell,

    Mtail = 2*pi*10^6*St*ell*(Rt+ell).

Thus four total masses follow by additive source accounting, not by the
spherical formula `RV^2/G`. The HI helium multiplier applies to both its
measured and tail terms. No interpolation should be renormalized to make
this integral equal a differently reduced catalogue total.

For an exponential cut numerically at B>Rt the omitted mass is exactly

    M_omitted(B) = 2*pi*10^6*St*ell*(B+ell)*exp(-(B-Rt)/ell).

This separates computational omission from the chosen physical tail model.

## Independent exact ring reduction

For this section use Sigma in solar masses/kpc squared, so it is the
tabulated value multiplied by 10^6. Let R>0 be the evaluation radius, a the
source-ring radius, and z>0 the evaluation height. Define

    D = sqrt((R+a)^2+z^2),  d2 = (R-a)^2+z^2,
    k = sqrt(4*R*a)/D,     kprime = sqrt(d2)/D.

Integrating the Newton kernel over azimuth gives

    Phi_N(R,z) = -4*G * integral_0^infinity a*Sigma(a)*K(k)/D da,

where `K(k)=integral_0^(pi/2) (1-k^2 sin^2(theta))^(-1/2) dtheta`.
Differentiate this expression at z>0, where differentiation under the
integral is regular. Using the defining-integral derivative of K yields

    gR_N(R,z) = (2*G/R) * integral_0^infinity a*Sigma(a)/D
                * [K(k) - (a^2+z^2-R^2)/d2 * E(k)] da.             (1)

Here `gR_N=partial_R Phi_N`: positive means inward physical acceleration,
whose vector component is `-gR_N`. An exterior ring can contribute a
negative gR_N. Never square an unsigned ring speed or clip negative ring
contributions. Equation (1) is derived from the same density without a
finite-volume discretization and does not invert the observed rotation curve.

Check normalization independently on the unintegrated ring:

    d(gR_N)/da = G*a*Sigma(a) * integral_0^(2*pi)
                 (R-a*cos(theta)) /
                 (R^2+a^2+z^2-2*R*a*cos(theta))^(3/2) dtheta.

A few nonsingular rings, including a>R, can compare this direct angular
quadrature with the elliptic expression. At R=0 use symmetry, gR_N=0,
rather than evaluating the apparent 1/R expression. In a complete analytic
benchmark, the Kuzmin density reproduces
`gR_N=GM*R/[R^2+(z+a_disk)^2]^(3/2)` for z>0.

## Fast evaluation without SciPy

The arithmetic-geometric mean evaluates the complete elliptic integrals.
Set `a0=1`, `b0=kprime`, `c0^2=1-kprime^2`; iterate

    anext=(a+b)/2, bnext=sqrt(a*b), cnext=(a-b)/2.
    K = pi/(2*AGM(1,kprime)),
    E = K*[1 - sum_(n=0)^infinity 2^(n-1)*cn^2].

These are the standard identities in
[NIST DLMF 19.8.5–6](https://dlmf.nist.gov/19.8#E5).
Use `kprime=sqrt(d2)/D` directly near a=R instead of subtracting k squared
from one. Its square can also initialize `c0^2=(1-kprime)*(1+kprime)`.
For an implementation, start the sum at `c0^2/2`, then add `cnext^2`,
`2*cnextnext^2`, and so on; this avoids a common factor-two indexing error.
Compare selected nonsingular K/E values against their defining angular
integrals before using this oracle. No additional package is required.

Split the a integration at all density knots, tail junctions and a=R.
For small z, the substitution

    a = R + z*sinh(u),  da = z*cosh(u) du

resolves the narrow near-ring structure while keeping a one-dimensional
quadrature. Apply it separately to the finite radial intervals, retaining
signed contributions. Prospectively compare two Gauss orders such as 48/96
per interval; do not mistake low quadrature order at fixed z for a physical
thin-disk effect. An omitted outer exponential mass beyond B>R gives the
conservative acceleration bound `G*M_omitted/(B-R)^2`. Sum that bound for
all omitted components, independently of cancellation in the desired force.

## Height limit and comparison to the field solver

Do not integrate equation (1) naively at z=0 across a=R: the thin-sheet
limit requires cancellation of the singular ring contributions. Instead,
at radii away from all profile knots and sharp endpoints, compute fixed
heights `z0,z0/2,z0/4` and retain their actual convergence. A source-only
choice is `z0=min(0.2 kpc, distance_to_nearest_knot/4)`. For example,
R=2.7,8.7,20.7,35.7,43.7 kpc are prospective density-independent force
checkpoints; if any coincides with an implementation's knot, move it by a
predeclared source-only rule before any force result.

The one-sided sheet condition gives

    partial_z Phi_N(R,0+) = 2*pi*G*Sigma(R),
    partial_z gR_N(R,0+) = 2*pi*G*Sigma'(R).

Consequently `2*gR_N(R,z/2)-gR_N(R,z)` cancels the leading height term.
Comparing the two successive extrapolants supplies a practical convergence
diagnostic; it is not a rigorous remainder bound at arbitrary z. The
additional check `gR_N(R,z)-2*pi*G*Sigma'(R)*z` tests the predicted leading
slope, without assigning a physical disk thickness to the regulator.

For a clean finite-volume Newtonian check set mu=1 and use this ring-derived
potential on its finite outer boundary. Otherwise an approximate boundary
error would be mixed with a discretization error. Compare the same density,
not the SPARC velocity-component templates, which have other reductions.
This Newtonian check cannot justify applying the nonlinear constitutive law
pointwise to a disk force; the nonlinear equation must still be solved.

With G expressed in `kpc*(km/s)^2/Msun`, equation (1) returns
`(km/s)^2/kpc`. Its conversion to m/s squared is multiplication by
`10^6/(3.085677581491367e19)`. Use the same explicit G and a0 constants in
both routes. Preserve the full 43-row observation comparison after source
freeze; the requested R>=2 and R>=8 summaries are descriptive, not evidence
for discarding other rows or selecting among the four source alternatives.
