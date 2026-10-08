# Exact hard-barotrope C provider and CLASS candidate interface

2026-09-29. Inert source implementation; no compilation, library import,
scientific evaluation or transfer run by its author. The provider implements
the exact zero-source constitutive integrals by qualified numerical
quadrature; "exact" identifies the action/EOS, not exact floating arithmetic.
It changes neither pinned CLASS nor the separately owned ordinary adapter.

## 1. Physical branch and input ownership

The explicitly adopted macroscopic action contains

    C beta [I sqrt(-partial theta squared) - e_R(I,0)] - C DeltaU,
    e_R from V(y)=R^2 y^2/2+y^4/4, m=kappa=u4=1.

On its homogeneous zero-polarization-current branch, a^3 I=I1,
rho_H=C beta e_R, p_H=C beta(I omega-e_R), omega=e_I, and
ca2=I e_II/omega. The Q=0 linear scalar metric interface is exactly the
barotropic fluid with these coefficients. This is the declared effective
current law, not a new claim of native rapid averaging, vector ensemble
formation, physical oscillator seconds, or arbitrary-Q equivalence. A
nonzero conserved polarization entropy requires its additional source and
is intentionally outside this provider. Ordinary matter, radiation,
anisotropic stress and the matched constant vacuum remain separate.

Inputs are the SAME retained single hard mode R,I1,e1 and its present
positive hard excitation density rho1, plus an explicit interval
0<a_min<=1<=a_max. I1/e1 are unweighted modal values; rho1 already includes
beta and the common physical energy normalization. Do not pass the total
weighted energy as e1 or multiply rho1 by beta again. No new abundance,
sound speed, time scale, gap or initial spectrum is selected here.

The finite constructor rejects I1=0 or e1=0. Positive ideal dust is a
separately named constructor/branch, not an underflow remedy or a small-w
cut. An absent hard component should not be constructed at all. Finite
objects never change to dust at a threshold.

Actual I1 drives inversion at every a. The reconstructed e_R(I1) must
agree with saved e1 within 2e-10 relative; otherwise initialization fails.
The accepted ratio is exposed as `reference_energy_relative_error`.
Density is normalized using the quadrature-consistent epsilon(I1), making
rho(1)=rho1 exact without changing I1, R or any orbit. This is at most the
declared numerical anchor correction, not a scientific energy refit.

## 2. Stable material formulas and derivatives

For r=b^2/R^2>0, theta in [0,pi/2], q=1+r(1+sin^2 theta)/2,

    epsilon=r/2+r^2/4, e=R^4 epsilon,
    f=(2/pi) r integral cos^2(theta) sqrt(q) dtheta, I=R^3 f,
    j=integral q^(-1/2) dtheta, Omega=omega/R=pi/(2j).

The target is log f=log I1-3 log R-3 log a. Work in log r so neither a^-3
nor R^4 is required in intermediate arithmetic. With normalized period
weight q^-1/2 and action weight cos^2(theta)sqrt(q), define

    t=r(1+sin^2 theta)/(2q), alpha=<t>_P, bta=<t>_A,
    M2=<sin^2 theta>_P, M4=<sin^4 theta>_P,
    w=r M4/(2+r), ca2=alpha/(2+bta).

Pressure is not computed as a subtraction of nearly equal I omega and e.
The trace fraction is likewise evaluated as

    (rho-3p)/rho=4 M2/(2+r),

not a subtraction near the quartic limit. The exact sum of this fraction
and 3w is checked to 2e-11. The separate virial check is
exp(log f+log Omega-log epsilon)=1+w, also to 2e-11 absolute.

Dots in the next line mean d/d ln(b), not time:

    alpha_dot=2<t(1-t)>_P-Var_P(t),
    bta_dot=2<t(1-t)>_A+Var_A(t),
    d ln(ca2)/d ln I=
      [alpha_dot/alpha-bta_dot/(2+bta)]/(2+bta).

Implementation uses 1-t=1/q and a second centered-variance pass, avoiding
subtraction of two moments near either limit. The background outputs are

    rho_ln=-3(rho+p),       p_ln=ca2 rho_ln,
    rho_lnln=9(rho+p)(1+ca2),
    w_ln=-3(1+w)(ca2-w),    ca2_ln=-3 d(ca2)/d ln I,
    dw/da=w_ln/a,
    integral_fld=log[rho(a)/rho1]=log[epsilon(a)/epsilon(1)].

For conformal LENGTH derivatives multiply each ln(a) derivative by
Hconf=a H_phys/c (CLASS's a*H). No native-SI frequency conversion is hidden
in `omega_over_R`. The exact sound speed here is c*sqrt(ca2) only under
the independently adopted fluid action.

Positive weights give 0<w,ca2<1/3 at finite positive action. Roundoff up to
64 DBL_EPSILON above 1/3 is allowed as a numerical identity allowance;
outputs are never clipped. The harmonic limits are w~3r/16,
ca2~3r/8 and ca2_ln~−3ca2; the quartic limits are w,ca2→1/3.

## 3. Bounded quadrature, inversion and API

Files: `unt_hard_barotrope_v001.h` and `.c`. C99 with libm; C++ linkage guards.
No I/O, process launch, heap allocation, mutable global cache or dependency
on CLASS headers. An initialized caller-owned context is immutable and
evaluations are reentrant. Initialization writes only that context.

Only GL orders 64 and 128 are supported: 64 primary, 128 independent
resolution. Nodes on [0,pi/2] are generated in initialization by Legendre
recurrence/Newton, max32 iterations/root, step tolerance 8 DBL_EPSILON;
weights must be positive and sum to pi/2 within 2e-13. Root refinement uses
the same formula, so resolution is not an independent integration method.
Independent Simpson/saved-orbit checks are specified below. Kahan sums are
used for all moments. This code has not yet been compiled or evaluated.

The exact inequalities

    r/2 <= f(r), r^(3/2)/(2sqrt(2)) <= f(r),
    f(r) <= r sqrt(1+r)/2

give log r_hi=min(log2+log i,log2+(2/3)log i). Taking r_lo=r_hi/4 is a
strict lower bracket (split i<=1 and i>=1). Tiny explicit roundoff margins
enlarge these brackets. Inversion uses safeguarded Newton with slope
d ln f/d ln r=1+bta/2, inside a checked bracket, max64 iterations.
Acceptance requires a log-action residual <=32 DBL_EPSILON*(1+|log i|),
not merely a narrow bracket. Arithmetic range is explicitly rejected rather
than extrapolated: log(DBL_MIN)+32 <= log r <= log(DBL_MAX)/2−32.

Public calls:

    unt_hard_init(ctx,order,R,I1,e1,rho1,a_min,a_max,error,error_size)
    unt_hard_init_dust(ctx,rho1,a_min,a_max,error,error_size)
    unt_hard_eval(ctx,a,out,error,error_size)
    unt_hard_stress(out,delta,theta,&delta_rho,&delta_p,&momentum)
    unt_hard_fluid_rhs(out,Hconf,k2,metric_continuity,metric_euler,
                       delta,theta,&delta_prime,&theta_prime)

All return an explicit status; caller must stop or retain failure, not
reuse partially written output. Dust reports NaN for undefined orbit
coordinates, so a JSON wrapper must encode those as null with its branch
label. Error messages are caller-buffered. a=0 and evaluation outside the
declared finite slice fail. There is no fictitious Big-Bang input state.

The stress helper supplies delta_p=ca2*delta_rho, momentum=(rho+p)*theta,
and no shear. The exact scalar RHS is

    delta' = -(1+w)(theta+metric_continuity)-3Hconf(ca2-w)delta,
    theta' = -Hconf(1-3ca2)theta+ca2*k^2*delta/(1+w)+metric_euler.

In Newtonian gauge metric_continuity=−3Psi', metric_euler=k^2 Phi.
These are caller-supplied metric variables, not a Phi=Psi assumption or a
new metric solver. The canceled rest-frame/gauge entropy term is exactly
zero only because cs2=ca2 for this Q=0 barotrope.

## 4. Required candidate CLASS integration sites: not yet patched

Pinned CLASS commit 64bbab707faf4de4779a9e04edd180fef18d98fa was inspected.
The independently owned ordinary adapter remains unmodified. A subsequent
separate derived tree/adapter must implement ALL of the following; linking
this provider alone is not a candidate CLASS calculation.

| Pinned site | Required candidate behavior |
|---|---|
| background.c:542–555, 658–748 | Supply this w,dw/da,integral and exact rho,p,dp/dln a. Either use exact rho directly throughout, or retain its integrated variable and verify it against the provider; never inconsistent copies. |
| background.c:1780, perturbations.c:818 | Replace the stock a=0 and early-negligible-fluid premises with the declared finite-slice branch checks. Merely disabling a guard is not initial-data implementation. |
| background.c:2240–2255,2660 | Seed the hard density with rho1 exp(integral); conservation derivative is −3(rho+p). |
| background.c:524–555,606–615 | For diagnostic matter/radiation splitting use rho−3p and 3p once, as for existing massive species; these are bookkeeping, not two independent fluids. |
| perturbations.c:5782–5947 | Replace the subdominant dark-energy attractor. Include the hard relativistic contribution in total radiation/enthalpy but not neutrino shear; use the already declared finite-slice constrained/regular preparation. Recompute fractions and normalization, including zeta and any expansion-series correction. |
| perturbations.c:7855–7863 | Use rho,p,ca2 for every hard stress component. No constant input cs2_fld and no independent entropy term; use_ppf=false. |
| perturbations.c:10785–10809 | Use the exact time-dependent ca2 in both density and velocity RHS; don't reconstruct a tiny ca2 by canceling w−w'/(3H(1+w)) when the direct provider exists. |
| perturbations.c:6222–6226,8677,8794,9591–9593 | Keep matching density/velocity gauge conversions, output sources and stress diagnostics. Use actual 1+w, not a dust substitution. |
| perturbations.c:7614–7798,7951–7960 | Stock matter-source sums omit fld. Explicitly define/implement baryon-only, hard, total excitation and comoving outputs; do not present stock delta_m as including this component. Nonlinear HALOFIT/etc. are not qualified for this model. |
| input.c:3260–3405 | Preserve the physical budget and new branch identity. Do not let a synchronous-gauge CDM floor insert extra matter. Use a suitable gauge/fix and no fake CDM. Input must not silently replace matched vacuum or hard density. |

PPF sites, tensor/vector initial data and unrelated dark-energy branches are
not used by this scalar candidate. This is a scalar transfer interface, not
a primordial-tensor or arbitrary-vorticity claim.

## 5. Physical normalization, initialization and atomic-history contract

Inherited physical coefficients often obey Omega_b+Omega_H+Omega_Lambda=1
in units of Hcal before separately adding ordinary radiation. If the same
physical radiation is then retained, put F=1+Omega_r (or, generally, the
actual sum of all present physical coefficients),

    H0_actual=Hcal sqrt(F), Omega_j,CLASS=Omega_j,saved/F,
    rho_H1,CLASS=Omega_H,saved*(Hcal/c)^2.

CLASS H0 uses inverse Mpc; its density is (8piG/3c^4) times physical energy
density in compatible length units. Vacuum has the same fixed physical
coefficient as before. This is a unit/budget mapping, not recalibration to
a desired H0, added CDM or altered ordinary photon temperature. Massive
ordinary species, if adopted, require their actual present contribution in
F instead of an assumed massless-radiation replacement.

At a finite a_i, name one shared initial covariance and the complete
ordinary/hard density, velocity, shear and polarization data. The prior
route's regular radiation-series preparation is one declared choice, not
native derivation or a proof of a=0. Its finite-a_i constraints and
zeta normalization must include this exact hard background. A mode's
starting time cannot fall below the provider's a_min; all evolution from
the shared slice must be retained. A test using the alternative constrained
two-column finite-slice data must preserve that different label.

Thermodynamics must use the SAME H(a), ordinary density, photon temperature,
helium and atomic assumptions. The bundled CLASS HYREC wrapper is not the
owned standalone FULL external-H calculation and explicitly refuses FULL.
The later candidate adapter must import a qualified matching FULL history
and its opacity/temperature derivatives, or implement an independently
reviewed external-H FULL bridge. No recombination equivalence follows
merely from changing the background or choosing the word HYREC. Conversely,
no unresolved native oscillator-to-seconds dictionary is imposed as a new
gate on the explicitly adopted exact macroscopic fluid current law.

## 6. Prospective root-owned material qualification (not executed)

Before any CLASS candidate output, root freezes these bytes and its small
test harness. Suggested compact fixed census: synthetic positive r1 values
1e-12,1e-6,1,1e6 with R=1,rho1=1; a=1,.1,.001, plus explicit ideal dust.
The independent reference I1 comes from composite Simpson1024/2048 of the
same endpoint-safe action, not from the provider itself. Compare GL64/128
rho,w,ca2,derivatives and saved same-state finite-gap anchor outputs, with
relative 2e-9 plus absolute 2e-13 for ratios/derivatives. Retain every failure.
This is an algorithm qualification set, not a new scientific state census.

Check conservation, trace/virial, analytic dust, and exact integral sign.
Use centered differences in ln(a) at steps1e-3 and5e-4 with Richardson
to check rho,p,w,ca2 derivatives (relative2e-6 plus absolute2e-11), only
inside the declared domain. Check source-free perturbation RHS identities
at both gauges' explicitly supplied metric factors; the helpers do not
generate those factors. Bad saved energy, a=0, outside-domain and zero-action
positive-density finite inputs must fail. Compilation warnings, buffer
errors and test failures must be reported without silently changing the
physics. These gates are prospective; no outcomes have been seen.

The implementation costs O(order*iterations) per evaluation, with bounded
small stack storage and no history. A later interpolation/cache is optional
performance work requiring its own derivative/conservation error receipt,
not a reason to substitute constant cs2. This provider is usable material
code now; candidate CLASS initialization/thermal integration remains work.

## 7. Source custody

Original derivation/implementation with primary software evidence from the
locally pinned official CLASS source. Mathematical/action sources:

* MACROSCOPIC_ALPHA_ONE_GALAXY_BVP_V001.md:
  64d98fff0681a81edce675049f6d72bb54c58b1d92f463f69fdd09dff8ed7bb3
* ALPHA_ONE_FLRW_ENTROPY_INTERFACE_V001.md:
  48b6ba835fb84d30182bfb2233d17e49ad2b4cd2cb7e5f10def2ff934d94911e
* PREPARED_ACTION_COMPRESSION_DERIVATION_V001.md:
  4e95a23d32367941948deb088e7f192b1f5269923d216c802586376d7d950d33
* HARD_MODE_COLD_HISTORY_CONSTRAINT_V001.md:
  c4f80c78a6af1fadb472bc6bef9d3fb54302cc9b00ef0ae728a149b70b0bf067
* FINITE_SLICE_CMB_PREPARATION_AND_BOLTZMANN_ROUTE_V001.md:
  7b9a4952f279d9a32b6a6d5de9338f01b50bd3cbd6a1eab8cced8bad5f593cd4
* CLASS_PINNED_IMPLEMENTATION_READINESS_V001.md:
  b2453b07f78d60fbe3678eff9b90891a6a36199a2b7052eed666ee798160daa9

Pinned upstream source hashes:

* source/background.c:
  b6c4d46883ecfe9eb0a28964a62e9ca6e8cad7a9f035349d497578ffd8438efd
* source/perturbations.c:
  07b9ab4e55ee3c26beed7af1cf57fb4e850c4c4cb041d84c67d3da7aed3f2e9a
* include/background.h:
  41de634f32fed7ce4af3386fe4eb67892bc6c37520b8c9a40155f6895e3bdb3c
* source/input.c:
  c5bead345df78eefa368de7d7f0585be0c8856ed58dbfbb61c1818f8041faa5e

No upstream, ordinary baseline, saved scientific state or sealed result was
modified. Source/header/protocol hashes belong in the later freeze receipt;
the protocol does not self-hash.
