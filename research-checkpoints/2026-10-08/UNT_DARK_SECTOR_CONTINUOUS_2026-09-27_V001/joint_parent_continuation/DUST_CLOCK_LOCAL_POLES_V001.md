# Frozen test: physical scales of ordinary-source clock amplification

2026-10-05 UTC. Prospective, before execution. This is a local-in-time
linear pole diagnostic of EXACT_DUST_CLOCK_TRANSFER_V001, not a cosmological
trajectory, primordial initial state, finite-amplitude validity certificate
or observed structure fit. No historical transfer is rerun.

## Decision and fixed inputs

Determine whether the constant-trace clock merely adds a free wave, or
permits a distinct ordinary-source gravitational growth timescale and Weyl
response on finite spatial scales. Freeze beta=0.5 as a disclosed example,
not a selected best value; ell=100 pc, a0=1.0059833281731022e-10 m/s^2,
H_vac=50.3528974592 km/s/Mpc from the existing endpoint, and omega_b=0.02235
from the resident empirical alternative. No dark homogeneous dust.

Use Href=100 km/s/Mpc only as a unit. At a=0.1,0.3,1:
H^2/Href^2=(omega_b a^-3+(H_vac/Href)^2)/F,
r/Href^2=3 omega_b a^-3/2, F=1+3beta/2.
Radiation is omitted for this explicitly late dust-plus-endpoint diagnostic;
it is not a new radiation/recombination history. p/Href=c k/(a Href),
q=ell k/a, with c=299792.458 km/s and ell=0.0001 Mpc.

Inspect 221 fixed logarithmic comoving k points from 1e-5 to 1e6 Mpc^-1,
plus the three declared readouts k=.01,.1,1 Mpc^-1. This is an operator
spectrum, not a fitted wavenumber or a claim that every scale is physically
within the continuum model. Report the largest grid growth and adjacent
points; do not optimize beta, ell, background or thresholds.

## Algebra and interpretation

Freeze the exact four-state matrix at each epoch, retaining its actual
H,r,p. Let u=f^-2=1+2q^2+q^4, epsilon=u-1, A=3+2/beta. With pole s and
x=s(s+H), its characteristic equation is

    x^2+B x-C=0,
    B=3ur/A-r/F+epsilon p^2/A,
    C=(ur/A)(p^2+3r/F)>0.

Use a rationalized positive root for B>=0 to avoid subtraction cancellation.
The positive x branch implies a growing gravitational mode, not a scalar
ghost or proof of a material gradient instability. Its interpretation as
a local growth timescale is strongest when s/H is large and background
coefficients vary slowly relative to s. It is NOT an integrated growth law.

In the intermediate domain q<<1, p>>H and small vacuum stiffness,
x_plus approximately sqrt(r/A)p. At large q,p, x_plus tends to r: the
growth saturates to an ordinary finite Jeans scale rather than a UV divergence.
The other branch is the clock wave. Check these limits, not just a positive
eigenvalue returned by a black box.

Read out the growing eigenvector with Psi=-1, theta=Psi/s,
sigma=A[-s(s+H)+r/F]Psi/(p^2 s),
D=[s sigma-epsilon Psi]/u. Reconstruct n, Delta and the response ratio
-Psi/D relative to the instantaneous same ordinary-density potential.
These are ratios, not a prepared population or an independent mass halo.

## Controls frozen before execution

Compare the analytic four poles with direct 4x4 matrix eigenvalues for
beta=.1,.5,2; q=.001,.1,1,10; p=1,3,10; H=.4,r=.23. Permutation-match
scaled error tolerance 2e-9. These dimensionless algebra controls do not
pretend to be mutually consistent cosmological epochs. Characteristic
residual and eigenvector reconstruction tolerance 2e-10; high/low limits
2e-5. Zero ordinary density must reproduce the saved vacuum dispersion
to scaled 2e-12. All tolerances are numerical, not observational.

Report the leading-deep-field 1% spatial-sector amplitude screen

    |n|_screen=.01(1-f^2)/(2 f^3 c^2 p_physical/a0).

It comes from eta(B)f^2/(1-f^2), eta approximately 2|b|/a0,
b=f c^2 p_physical n. This is explicitly an ASYMPTOTIC spatial-Hessian
screen, not an exact nonlinear error bound or a full coupled transient
criterion. Matter/time terms can dominate the tiny free spatial restoring
term. Do not rule out finite-amplitude cosmology from this sufficient screen.
For small n, metric and density requirements remain separately necessary.

One small single-thread worker. Save failures unchanged. The result will
choose a physically relevant finite-amplitude follow-up, not certify the
model as a whole or launch an unrestricted CMB/expansion scan.
