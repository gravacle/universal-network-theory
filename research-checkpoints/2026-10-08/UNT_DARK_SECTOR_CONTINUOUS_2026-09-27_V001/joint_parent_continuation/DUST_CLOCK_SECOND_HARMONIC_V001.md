# Frozen regular second-harmonic source test

2026-10-05 UTC, before execution. Continue the SAME prepared modes, amplitude,
background, force law and one-form completion. Mean sector already checked
in DUST_CLOCK_MEAN_WORK_V002; nonanalytic odd harmonics remain their distinct
saved calculation. No new physical parameter, density or tolerance fit.

## Canonical constrained chart

For target p2=2p, f2=(1+ell^2p2^2)^-1, g2=f2^2p2^2, F=1+3beta/2,
A=3+2/beta, evolve z2,v2,pi2,P2. P is canonical rest weight, not proper
density; pi includes the cubic momentum term. With action sources below:

    E2=(pi2-Qdotz-A S_D)/(2A)-r v2,
    n2=[H(pi2-Qdotz)-2(p2^2+3r)z2+2rP2-Rn]/(2g2),
    D2=A E2+(2r/beta)v2+S_D/beta,
    zdot2=E2+Hn2, vdot2=n2+Vsrc,
    pidot2=-3Hpi2+2p2^2z2+2(p2^2+3r)n2+Rz,
    Pdot2=D2-p2^2v2+Psrc.

The lapse formula includes Qdotz but NOT a duplicate A S_D term. This follows
from varying the unreduced action and then using the full canonical momentum.
No time derivative of an interpolated forcing history is required.

## Direct action vertices, including reciprocal auxiliary response

Use proper spatial derivatives at each time (comoving phase is held fixed
when taking time derivatives). Write W=a U, D=partial_r W, b=B_x/a,
l=lambda_x/a. First order z=Z cos, n=N cos, v=V cos, P=Pstar cos,
W=p sigma sin, b=f1 partial_r n, l=f1^2 partial_r n. Zdot is evaluated as
HN+D/A-rV/F to avoid cancellation.

For zero first-order shear, the cubic density L3/(M^2a^3) is

    [T3+(3z-n)T2+(9z^2/2-3zn+n^2)T1
        +(9z^3/2-9z^2n/2+3zn^2-n^3)T0]/2
    +(n+z)z_r^2+2z n_r z_r-Lambda(9z^3/2+9nz^2/2)
    -2r[(n+P-2z)v_r^2/2+P W v_r]
    +(n+z)(b^2-2lb)+2zl n_r
    -2ell^2(n-z)l_r b_r+2ell^2 z_r(l_r b+l b_r),

where T0=-6FH^2, T1=-12FH zdot+4FH D,
T2=-6F zdot^2+12FH W z_r+4F zdot D-beta D^2,
T3=12F zdot W z_r-4F W z_r D.

Differentiate the spatial average with respect to a target-mode test field
and multiply by2 for cosine/sine normalization. z2,n2,v2,P2 tests use cos2;
include their spatial derivatives. The dotz2 test is independent cos2.
For S_D vary W by sin2/(2p), so D varies by cos2. Set Vsrc=-Q_P/(2r),
Psrc=Q_v/(2r). For the lapse test also vary b by f2 partial_r cos2 and l
by f2^2 partial_r cos2. Substituting the LINEAR stationary auxiliaries in
the effective cubic action in this way retains their second-order response;
omitting these variations would lose div(lambda2). The linear auxiliaries
do not depend on z, so the z test adds no corresponding auxiliary variation.

Eight phase points integrate these cubic vertices exactly up to roundoff;
repeat with16 as a control. Complex-step vertex evaluation uses1e-20 and
1e-25 for a cross-check. No fitted Fourier truncation or continuum solver.

## Initial constraints and observables

Extend the same zero-initial-clock-response preparation by choosing
P2=v2=n2=D2=E2=0 initially. Then the Hamiltonian determines

    z2_i=-3(p^2+3r)Zi^2/[4(4p^2+3r)],
    pi2_i=Qdotz_i=-(27/2)F H Zi^2.

These are a declared preparation, not a derived primordial state. P2=0 is
not zero proper density at this order. Initial source/lapse/shift constraints
must pass; do not set pi2=0 by hand.

Report preferred-chart z2,n2,P2,p2v2,D2/H and their magnitudes relative to
first-order peaks. Also report the regular second-order normal dust-density
cos2 coefficient P2-3z2+9Z^2/4-3Pstar Z/2-p^2V^2/4.
Do NOT call z2 or n2 Newtonian potentials or set Phi2=Psi2. Nonlinear gauge
conversion and observer optics remain required for that interpretation.

## Fixed controls

Reuse the qualified quintic interpolation of the existing65 linear snapshots.
Run RK4 at256,512,1024 steps, and compare33/65 source snapshots. One numerical
worker only. Checks: linear canonical chart vs exact original four-state
evolution <=2e-10 relative to absolute-term scale; mean action vertices vs
the separately checked mean formulas <=2e-10;8/16 phase and complex-step
refinement <=2e-10; analytic dust source and initial constraints <=2e-10.
512/1024 state/readout convergence <=2e-5;33/65 history refinement <=2e-4.
Compare each component against its interval peak, floor1e-30 in normalized
units. Quadratic correction/first-order peak <1% is the existing working
perturbative screen, not a rigorous remainder bound. Preserve every failure.

Restoring physical amplitude^2 is mandatory. The constitutive odd and regular
even corrections add at this order but their higher-order feedback is not
computed. A pass qualifies this second-order diagnostic, not Stage3 or UNT.
