# Direct AQUAL external-field quadrupole — prospective V001

2026-10-04. New conditional, non-galaxy prediction. This tests the universal
conservative AQUAL completion of the frozen relaxed network force law, not all
possible network theories. It does not substitute QUMOND for AQUAL.

## Frozen physical assumptions and inputs

Use the already calibrated a0=1.0059833281731022e-10 m/s² and inherited shape
r=25.51664211557329 without adjustment. The analytic law is that of disk_solver.py.
One spherical Sun, GM=1.32712440018e20 m³/s², in a constant external field directed
along the polar axis. Independently measured external acceleration 2.32e-10 m/s²
is primary; 2.16 and 2.48e-10 are separately reported sensitivity cases, not fits.
This uniform-field, stationary, single-source boundary is an adopted approximation.
No solar or galaxy nuisance fitting, and no physical response-time claim.

External-field context: https://academic.oup.com/mnras/article/530/2/1781/7641422 .
Direct nonlinear precedent: https://arxiv.org/html/1010.1349v2 .
Observation: https://arxiv.org/html/2602.17884v2 gives Q2=(1.6±1.8)e-27 s^-2,
jointly estimated with DE440 ephemeris parameters. The older overlapping estimate
is not a second independent datum. Do not transfer that paper's QUMOND-specific
planetary correction or interpolation-family exclusions directly to this law.

## Equations and numerical design

rM=sqrt(GM/a0), r=R/rM, t=ln r, u=cos(theta). In units a0 rM write
phi=-1/r-e r u+psi, e=gext/a0. Separate the analytic large Newtonian and external
terms so the tiny regular quadrupole is not obtained by subtracting potentials.
Solve div(mu(|grad phi|) grad phi)=0 outside the Sun. Equivalently
Delta psi=div B, B=(1-mu)grad phi. All Legendre modes 0 through L are retained,
including odd modes. Angular projection uses Gauss–Legendre quadrature.

psi_l,tt+psi_l,t-l(l+1)psi_l = r(Br_l,t+2Br_l+Theta_l),
Theta_l=(2l+1)/2 integral sqrt(1-u²) Btheta P_l' du.
An exponentially fitted three-diagonal radial operator preserves r^l and
r^(-l-1) homogeneous solutions exactly. Source and potential derivatives are
second-order in log radius. Picard updates are underrelaxed by 0.5.

Inner regular boundary psi_0=exp(-l h)psi_1; outer boundary is the independently
derived external-field linear Green asymptote
psi=[1-1/(mu_e sqrt(1+L_e(1-u²)))]/r, L_e=d ln mu/d ln g at e.
Both are finite-domain approximations, requiring domain checks.
Extract c2=median(psi_2/r²) on r=0.003..0.02 and Q2=-3 a0 c2/rM.
The exact complete-domain Green identity provides an additional diagnostic;
the finite-domain integral is NOT automatically an independent exact result.

## Locked run budget and qualification, before physical results

Controls: stable deficit agrees with original flux to absolute 3e-13 on a
logarithmic range; angular orthogonality 1e-12; zero-deficit Newton solve 1e-12;
manufactured l=0..3 forced solutions at 97/193/385 radial points must converge
at least 2.5-fold per doubling and reach <0.003 relative max error. Homogeneous
mode solve error <1e-9. Check linear equation residual <1e-10 scaled.

Physical census (nr, L, angular order, inner radius, outer radius):
A=(193,16,48,1e-4,64); B=(385,24,72,1e-4,64);
C=(769,40,120,1e-4,64); D=(769,40,120,5e-5,128);
E=(769,48,144,5e-5,128). Primary external field runs all five.
The two external-field sensitivity values run E only if primary qualifies.
Each case starts from zero psi, at most 240 Picard iterations and 50 seconds;
checkpoint each completed case, no parallel workers. Convergence requires
max update <1e-8 scaled by max(1,max|psi|) for three consecutive iterations,
and final fixed-point defect <3e-8 on the same scale. A numerical failure at
the cancellation saddle is not a physical exclusion.

To report a usable physical Q2: every primary case must converge; plateau
max deviation <0.01 scaled by max(|c2|,1e-5); B/C radial+angular change, C/D
domain change, and D/E angular change each <0.05 on max(|c2_E|,1e-5).
Report all values, not only best resolution. Numerical differences define
a diagnostic envelope, not a rigorous error bound. The Green integral and
mode-tail amplitude are retained descriptively, never used to relax these gates.
No threshold is chosen after results. Conditional Gaussian standardized
residual against Cassini is descriptive (not full model evidence), and is
withheld if qualification fails. No source-law retuning from this observation.

## Next decision

Qualified agreement means cross-scale survival only. Qualified discrepancy
constrains this universal static completion; retain the galaxy success and
investigate a physically specified environment/scale-dependent completion,
counting every new freedom. Unqualified computation needs a diagnosed
numerical alternative, not a fabricated scientific conclusion. Full shared
expansion, growth, merger, early-universe, both CMB tracks, native formation
and independent final synthesis remain open regardless of this test.
