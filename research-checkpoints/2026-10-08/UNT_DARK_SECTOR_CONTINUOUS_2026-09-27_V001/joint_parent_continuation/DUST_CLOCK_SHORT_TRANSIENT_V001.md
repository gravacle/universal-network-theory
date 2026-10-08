# Frozen short source transient and first nonlinear correction

2026-10-05 UTC. Prospective protocol after the local-pole diagnostic; this
is a new finite-time calculation, not repetition of an old transfer.
Root and endpoint_equations_check derived the forced harmonics independently.
One small numerical worker, no fitted quantities or amplitude reduction.

Use the exact constant-trace dust four-state action and the SAME inputs as
DUST_CLOCK_LOCAL_POLES_V001, beta=.5, ell100pc, omega_b=.02235 and inherited
endpoint. Three fixed comoving modes k=.01,.1,1 Mpc^-1, starting a_i=.1,
ending ln(a/a_i)=.05. Radiation remains deliberately omitted in this late
diagnostic; its roughly 1.9% density contribution at a_i is not a bound on
the transfer error. No full cosmology or primordial-state claim.

Initial ordinary comoving contrast is Delta_i=1e-8, theta_i=sigma_i=0,
D_i=r_i Delta_i/p_i^2, Psi_i=-D_i. Thus n_i=0 and the instantaneous
comoving Poisson clock contribution is zero. This is a prepared ordinary
source at rest, NOT a native formed or growing adiabatic initial condition.

## What is actually computed

First evolve the exact linear four-state system in ln a. In parallel evolve
the leading acceleration-constitutive correction, initially zero, driven by
that linear solution. For n1=N(t) cos(kx), F(b)=b-b|b|/a0+O(b^3/a0^2),
the correction at odd harmonic m satisfies

    y2_m_dot=L_m y2_m+e_sigma delta n_m,
    delta n_m=(f1^2/fm)(c^2 p1/a0)
                [8/(pi m^2(4-m^2))] N|N|.

L_m is the SAME linear dust/clock operator at p_m=m p1; no independent
harmonic population is supplied. Keep odd harmonics through 15,31,63 for
refinement. Do not truncate to the fundamental or extrapolate a first
correction into a full nonlinear evolution. This estimates only the
constitutive nonlinearity; dust advection and complete metric/filter stresses
are distinct omitted terms. At this retained scalar order Phi=Psi; its
nonlinear-stress correction has not yet been established.

Use RK4 on 2048,4096,8192 equal log-a steps, store 65 common samples.
State amplitudes are divided by the FIXED Delta_i for conditioning, not a
physical amplitude change. Compare final and common-time readouts of Psi,
Delta, n, p theta and p sigma. No pointwise division at sinusoid nodes.
Correction amplitude is the sum of absolute harmonic coefficients divided
by the largest corresponding linear amplitude over the interval.

## Fixed numerical controls and physical screens

- Check the matrix formulation against the four-state component RHS to
  scaled 2e-12 at declared test states and three epochs.
- Compare analytic |sin|sin odd coefficients with 32768-point periodic
  quadrature to relative 2e-7 through m63. This is independent of evolution.
- Finest versus middle time-grid readouts: normalized linear difference
  <=2e-5; correction readouts relative to their own peak amplitude <=5e-3.
- m31 versus m63 summed correction amplitudes must differ by <=.02 relative
  to the m63 correction amplitude. Preserve an unresolved harmonic tail as
  a failed qualification, not zero error.

Separately report, without retuning, whether over the whole short interval:
|Delta| and |delta_N| stay below .01; metric |Psi|,|n|,|zeta|,|Hv| below1e-4;
physical velocity/tilt p|theta| and p|sigma| below1e-3; peak |b|/a0 below1e-3;
and the estimated constitutive correction in each readout below1%.
These are declared working screens, not rigorous remainder/observational
criteria. Also report the conservative spatial-Hessian and omitted-stress
power-counting ratios. A screen failure does not exclude the full nonlinear
model. No new length, beta, cosmological component or tolerance may be fitted
after results. Save partial/failed attempts separately if needed.

The scientific decision is whether this prepared ordinary source has a
controlled short-time amplified optical response in the declared expansion,
or whether full nonlinear/metric dynamics are already indispensable. A
zero-mean first-order mode cannot establish averaged cosmic acceleration.
