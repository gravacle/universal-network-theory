# Frozen mean-work test on the saved ordinary-source transient

2026-10-05 UTC, written before execution. Same fixed physical inputs,
amplitude1e-8 and window as DUST_CLOCK_SHORT_TRANSIENT_V001. Reuse its saved
finest linear histories, not the incomplete nonlinear run status as proof
of full validity. No galaxy, cosmological or observational fit is performed.

## Complete regular quadratic mean projection

Use the action and conventions of PLANAR_CLOCK_STRESS_AND_DUST_V001.
Here F=1+3beta/2, r=rhobar/(2M^2), Hdot=-r/F, Lambda=3F H^2-2r,
p=k/a, f=(1+ell^2p^2)^-1, and the first-order cosine amplitudes are

    Z=-Psi+H sigma, N=f^-2(Psi+D), V=theta+sigma, S=p^2 sigma.

Dot denotes preferred background time, not log a. Define

    T0=-6F H^2,
    T1=-12F H Zdot+4F H S,
    T2bar=-3F Zdot^2-6F H S Z+2F Zdot S-beta S^2/2.

The coordinate-mean lapse constraint is

    6F H zdot0+6r z0+C=0,
    C=p^2 Z^2/2-9Lambda Z^2/4
      -[T2bar+(3Z-2N)T1/2+(9Z^2/4-3ZN+3N^2/2)T0]/2
      -f^2p^2N^2/2-rp^2V^2/2.

The independent spatial-volume equation is

    6F(zddot0+3H zdot0)=Qdot_d+3H Q_d-Q_z,
    Q_d=[-6F S Z+(3Z-N)(-12F Zdot+4F S)/2
         -12F H(9Z^2/4-3ZN/2+N^2/2)]/2,
    Q_z=[3T2bar+(9Z-3N)T1/2
         +(27Z^2/4-9ZN/2+3N^2/2)T0]/2
         +p^2(Z^2/2+NZ)-Lambda(27Z^2/4+9NZ/2)
         +(5f^2-4f^3)p^2N^2/2+rp^2V^2.

Their on-shell quadratic work identity is

    Cdot+3HC+H(Qdot_d+3H Q_d-Q_z)=0.

Retain the homogeneous shear momentum m=6chidot0-(3Z-N)S:

    mdot+3H m=J,
    J=-p^2(2Z^2+4NZ)+2p^2N^2 f^2(1-2f)+2rp^2V^2.

Two internal analysts derived/checked the action contributions independently.
Numerical evaluation will check conservation rather than presume that the
agreement of formulas is a proof of their implementation.

## Initial state and readouts

Mean lapse n0=0 fixes domain time; no lapse history is fitted. Preserve
canonical mean P2=0. Fix the initial proper volume by z0=-3Zi^2/4,
chi0=chidot0=0 for this zero-initial-shift preparation. Initial zdot0 follows
the Hamiltonian constraint. Independently evolve the spatial-volume
equation with those same initial values. This fixes no new density species.

Report domain log-volume scale correction L=z0+3Z^2/4, delta H=Ldot,
delta q=-Lddot/H^2+2Hdot Ldot/H^3, and chi0/chidot0. Domain-volume q is
NOT observer-inferred acceleration: that requires the saved same-metric
null-ray and observer-clock calculation. Do not use a sign of delta q as
proof of an accelerating universe. The complete2k response remains open.

## Bounded computation and criteria

Use the finest existing65 linear snapshots at k=.01,.1,1. Reconstruct their
four-state vector exactly from the recorded physical readouts. Cubic Hermite
interpolation uses endpoint slopes from the exact linear equations. Compare
the65-snapshot interpolation with its33-snapshot subset; do not rerun the
completed constitutive harmonic sums or alter their criteria.

Integrate the mean constraint, shear and independent volume equation with
RK4 at256,512,1024 steps over log(a/ai)=.05. Controls fixed in advance:

- Algebraic work identity and dust kinetic/lapse-work identity normalized
  by sums of absolute constituent terms: <=2e-10.
- Complex-step derivative vs centered directional derivative on nonzero
  source samples: <=2e-5; finite-difference step1e-5 in Href time units.
- Linear interpolation differential defect normalized to its local linear
  terms: <=2e-5 away from the interval endpoints.
-512-to1024 mean state convergence, each component relative to its interval
  peak: <=2e-5.
-33-to65 snapshot refinement of mean state/readouts: <=2e-4.
- Independently integrated volume state/velocity versus mean Hamiltonian
  state/velocity: <=2e-4 relative to separate interval peaks.

Zero/near-zero comparisons use a1e-30 floor in amplitude-normalized units;
zero-amplitude null response is an additional exact control. Store actual
physical answers with amplitude^2 restored. Failed criteria remain failures
and are preserved before any motivated refinement. No outcome threshold
is chosen for acceleration or shear; this is a diagnostic, not a fit.
