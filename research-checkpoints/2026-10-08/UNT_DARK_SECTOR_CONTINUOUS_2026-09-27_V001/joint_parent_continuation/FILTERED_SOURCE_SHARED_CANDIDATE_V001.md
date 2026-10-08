# Averaged source response with the finite vacuum endpoint retained

2026-10-04. A new, provisional effective hypothesis after V009's geometric
coupling screen. It changes where spatial averaging acts: on the complete
gravitational input before its nonlinear response, rather than only on the
response coordinates. Its purpose is to test whether short-scale screening
can coexist with the earlier finite force-to-vacuum endpoint relation.
Neither UNT superiority nor an observationally viable cosmology is asserted.

## Precisely what changes

In flat static space define the self-adjoint Yukawa averaging operator

    S_ell=(1-ell^2 laplacian)^(-1),  b=S_ell g,  g=grad Phi,
    h(b)=b/sqrt(1+|b|^2/gs^2).

Use isolated perturbations about a specified constant external field. S acts
componentwise in this static definition. The proposed relaxed energy is

    E=integral [ |g|^2/(8 pi G) + C(U(b)+DeltaU) + rho_b Phi ] d^3x,
    C=1/(4 pi G Kb),
    U(b)=min_y integral nu[V0(y)-kappa delta h(b).y],
    V0=kappa delta^2 |y|^2/2+u4 |y|^4/4,
    nu=A delta on (0,Lambda), Kb=kappa A Lambda^2/2.

This is a NONLOCAL STATIC effective action, not yet a causal network
evolution law. The kernel, its physical length, equilibrium state, source
map and covariant realization are assumptions. No heavy simulation is
justified before testing the elementary consequences below. The earlier
linear-source gradient candidate and all its successes/failures remain
separate. This candidate does not silently inherit its numerical results.

Restore the earlier bounded source ratio r=gs/a0=25.51664211557329 and use
the later frozen galaxy acceleration a0=1.0059833281731022e-10 m/s^2.
Ell=100 pc is inherited as a disclosed development choice, not a new fit.
There are three numerical physical inputs a0, r and ell in the static law,
in addition to adopted functional choices and the unresolved dynamical
inertia/state/covariant content. G is an ordinary calibration. The ratio r
was originally chosen using an expansion reference; it is NOT a blind
galaxy-derived prediction of vacuum energy.

## Field equation and why averaging the source differs

Let P(h)=integral nu kappa delta y(h). The envelope derivative is
grad_b U=-(D_b h)^T P. Static variation gives

    div D=4 pi G rho_b,
    D=g-S_ell F(b),   F(b)=(D_b h)^T P(h(b))/Kb.

The OUTER S is required by self-adjoint variation. Omitting it changes the
model and would lose the energy/work relation. Even a uniformly held
polarization retains the complete source derivative, but it is now averaged
before entering the short-scale gravitational equation. This is why the old
failed held-polarization Solar result is not this candidate's prediction.

Around constant external e define local relaxed flux D_local(b)=b-F(b),
epsilon_local=partial D_local/partial b and Q=I-epsilon_local. Fourier
linearization gives, with q=k ell,

    epsilon(k)=I-f(q)^2 Q, f(q)=1/(1+q^2).

This is a convex combination of I and epsilon_local, so a strictly positive
local Hessian implies a positive static Fourier Hessian. It does not prove
causal stability of an unprovided time-dependent completion. At large k the
extra response falls as k^-4. The regular point-source potential correction
has a finite central Hessian, unlike an assumed unresolved cusp.

## New bounded Solar calculation before any fit

Keep the previously exposed primary external acceleration 2.32e-10 m/s^2,
GM_sun=1.32712440018e20 m^3/s^2 and ell100pc. They are illustrative physical
inputs for a constant-background LINEARIZED prediction, not a new ephemeris
likelihood. No Gaussian source bound from the other parent is inherited.

For u=cos(theta), d(u)=Q_perp+(Q_parallel-Q_perp)u^2<1. The exact radial
Fourier integral is

    integral_0^infinity q^2 d/[(1+q^2)^2-d] dq
      =pi d/[2 sqrt(2+2 sqrt(1-d))].

It also holds for negative d. With the convention
delta Phi=-Q2[(e_hat.x)^2-|x|^2/3]/2 for the traceless quadratic part,

    Q2=Cq GM/ell^3,
    Cq=-1/2 integral_-1^1 P2(u) d(u)/sqrt(2+2 sqrt(1-d(u))) du.

The isotropic quadratic correction is not silently discarded; record the
Laplacian coefficient as well. A constant-field Fourier solution also gives
the conservative bound ON ITS OWN FILTERED INPUT perturbation

    |delta b_linear| <= GM/(2ell^2) [1+dmax/(pi epsilon_min)],
    epsilon_min=min(1,lambda_min(epsilon_local)),
    dmax=max |lambda(Q)|.

This follows by splitting the explicitly filtered Newton field from the
absolutely integrable extra Fourier response. It is a self-consistency scale
for linearization, NOT a nonlinear solution/error certificate. The full
filtered field, not the large unfiltered Solar surface acceleration, is the
argument of h. Small input excursion is encouraging but insufficient to
certify the measured Solar result.

Before execution: evaluate modal/angular pairs (64,64), (128,128), (256,256),
(128,256), (256,128). Require positive local eigenvalues; their relative
refinement and Cq changes against (256,256) must be <1e-6. Do not fit ell or
the external field. Check the radial integral with independent 256-node
mapped quadrature for d=-.5,.2,.8,.98 to scaled 2e-9; check the modal static
force against the inherited closed-form force and its derivative to 2e-6;
check zero-Q and isotropic-Q quadrupoles to 2e-12. No criterion is a claimed
Solar observational acceptance threshold. Preserve failures as output.

## What is shared with homogeneous expansion and what is not

The averaging operator preserves every constant field. It therefore leaves
the earlier uniform-source endpoint DIFFERENCE unchanged:

    DeltaU=-U(|b|->infinity)=integral_0^gs P(h) dh,
    Q_b(r)=DeltaU/(Kb a0^2).

The limit is b->infinity, with h->gs; evaluating U(b=gs) is not that limit.
IF the already explicit physical matching condition U(infinity)+DeltaU=0
is imposed, its common-metric homogeneous vacuum scale is

    H_vac^2=2 DeltaU/(3 Kb c^2).

This is a physical absolute-energy postulate, not an irrelevant choice of
zero. Retaining it restores a conditional force/endpoint link without
introducing another independently adjustable vacuum amplitude. It does not
derive that postulate from UNT. The old r calibration used H0=73.6 km/s/Mpc,
Omega_Lambda=.666 and a0=1.2e-10 m/s^2. At the later galaxy a0, the vacuum
scale changes in direct proportion to a0. Report the rescaled SAVED result,
not a new fit, and do not present H_vac as the present total Hubble rate.

Homogeneous unexcited modes plus this offset do NOT supply missing
matter-era expansion/growth or CMB peaks. An arbitrary additional mode
abundance would still be another budget. The previously failed shared
backgrounds remain failures. Static ell averaging by itself cannot repair
their homogeneous history.

## Decision and evidence ceiling

Root and endpoint_equations_check independently derived the filtered
variation, Fourier coefficient and point-source linear input bound before
execution. The reviewer confirms that constant-field endpoint preservation
is exact for this declared filter, but neither dynamic locality nor energy
normalization is thereby derived.

A qualified small quadrupole would justify checking the SAME filtered
source law on an actual galaxy and its optical metric; it would not earn
a Solar likelihood pass or joint cosmological success. If it fails this
small test, preserve that failure before changing any kernel or parameter.
After this calculation, the highest-value shared-model question remains
an actual homogeneous evolution/metric law with ordinary radiation and a
source-selected state, followed by a prediction not used in its calibration.

## Executed linear result

All 29 fixed controls pass; the new calculation took 0.0521 s internally.
The external local eigenvalues are .678798882264952 and .864799179375393.
The dimensionless Cq=.0133029565427473, giving
Q2_linear=6.00908255800142e-38 s^-2 at 100 pc. The isotropic Laplacian is
6.08204485735650e-37 s^-2. Maximum reported quadrupole refinement change is
5.28e-13 relative, well inside the predeclared 1e-6 gate. The linear filtered
input bound is 8.01886520995148e-18 m/s^2, or 3.4564e-8 of the external field.
These are not a nonlinear or ephemeris result.

The unchanged, previously matched endpoint rescales to H_vac=50.3528974592
km/s/Mpc at the later galaxy a0. This is not H_today and is not independent
confirmation: the ratio r used a prior expansion calibration. An actual
ordinary-matter/radiation background history remains necessary.

Result SHA256:
d25a8aaedef6f51afb246c7a720b3c3fe02089a64d3a1dddf6a723b1675ba015.
The saved JSON contains source, inherited-input and pre-result-note hashes.
No numerical worker remains live. The next test is a nonlinear finite-source
bound using the same action, not a retuned length or another linear solver.
