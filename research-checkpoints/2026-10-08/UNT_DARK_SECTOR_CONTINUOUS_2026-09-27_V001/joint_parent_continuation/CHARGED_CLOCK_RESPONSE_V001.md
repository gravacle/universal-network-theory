# Charged clock response to conserved ordinary matter

2026-10-03. Prospective specification, before execution. This is the next
physical prediction test of the existing bounded-clock action, not a new
microscopic consistency project. It tests its time-dependent gravitational
response on a declared expanding background. It cannot alone test the
nonlinear MOND force or establish observational superiority.

## Fixed model and preparation

Use exactly the action and bounded pressure in
BOUNDED_CLOCK_ACTION_AND_RESULT_V001.md. No radial halo, phase or vector
profile is fitted. Adopt KB=1, lambda_s=1, eps=1e-6 and Q0/H0=1. The
existing unit calibration implies Gcos/GN=1/4. Set H0=73.6 km/s/Mpc,
a0=1.2e-10 m/s^2, Omega_A=0.7 and the ordinary baryon density
8 pi GN rho_b0/(3 H0^2)=0.05, hence Omega_b_cos=0.0125. Fix the conserved
clock charge by rho_clock_excess0/(3 H0^2/(8 pi Gcos))=0.2875. This
enforces flat H(a=1)=H0. These are exposed DEVELOPMENT inputs, not an
observational fit or a derived abundance. The same seven constants/state
numbers and adopted functions remain counted. Six scalar initial amplitudes
per nonzero Fourier mode remain additional preparation freedoms.

Evolve one mode K=k c/H0=30000 from a=0.01 to 1. Its present 1/k is about
136 kpc, while its full wavelength is about 853 kpc. There is no radiation,
baryon pressure, gas cooling or virialization in this first linear test.
It is not a CMB calculation or a model of a formed galaxy. All material
density and velocity perturbations evolve by their conservation equations.

The primary source preparation is a zero-mean ordinary baryon mode of
initial density amplitude 1e-5, initially at rest. All clock/vector
perturbation amplitudes initially vanish; constraints set the metric.
This is declared baryon isocurvature, not a native primordial prediction.
Also propagate all six independent constrained initial columns to expose
mode dependence, and one declared adiabatic development comparison:
F=delta_b=1e-5, theta_clock=theta_b, chi=Z=0, with Phi_dot=0 initially.
Neither preparation is selected after seeing its response.

## Complete linear equations

Use x=ln a, h=H/H0, Q=Qphysical/H0, velocities V=H0 theta,
alpha=H0 alpha_physical, and density units 3H0^2/(8 pi Gcos).
Rb=Omega_b_cos a^-3, W=(rho_clock+P_clock) in these units,
F=delta rho_clock/W, s=c_ad^2, kappa2=K^2/a^2, C=2-KB.
Phi is the dimensionless metric potential, with Psi=Phi.

    chi=Q(V+alpha), E=(Z-C chi)/KB
    deltaP=s[W F+kappa2 Z/3]
    Phi'=-Phi+3(W V+Rb Vb)/(2h)
    delta_b'=3 Phi'-kappa2 Vb/h
    Vb'=Phi/h
    F'=3 Phi'-kappa2 V/h-s kappa2 Z/W
    V'=3s V+(Phi+deltaP/W)/h
    Z'=-Z+3W chi/(Qh)+CQ(E-chi)/h
    alpha'=(E-Phi)/h

The propagated Einstein constraint is

    CH=2 kappa2 Phi+3(W F+Rb delta_b)+9h(W V+Rb Vb)=0,
    CH'=-3 CH.

Background: a^3 K_Q is conserved, Q'/Q=-3s,
W'/W=-3(1+s), h'=-3(Rb+W)/(2h). The full pressure, rather than a
constant sound-speed approximation, determines all coefficients.
F normalization is used only on this strictly positive-charge interval.

As independent action controls reconstruct U=WF+kappa2 Z/3 and check

    U'=-3(1+s)U+3W Phi'+CQ kappa2(E-chi)/(3h)+W kappa2 alpha/h;
    Phi_ddot+4h Phi_dot+(2h_dot+3h^2)Phi=3 deltaP/2,

with dots in H0 time units. Two source-only reviewers independently checked
the metric signs and current closure, using the original action and the
[primary relativistic benchmark](https://arxiv.org/html/2007.00082v3).
The new spatial J begins cubically in perturbations and does not supply
the MOND response in this linear calculation.

## Comparisons and numerical gates

Compare with conserved baryons plus pressureless matter and a constant
vacuum term, with the SAME Gcos, Omega_b_cos, 0.2875 extra matter and
0.7 vacuum normalization, scale and preparations. This matches the
calibrated expansion budget rather than declaring one model superior by
parameter naming. It is not a full conventional best fit or unused data.

Use a single NumPy worker and fourth-order two-stage Gauss collocation.
Compare 512, 1024 and 2048 uniform ln(a) steps at shared checkpoints.
Keep all initial columns; do not infer full ghost freedom from bounded
finite-time responses. If resolution fails, preserve it and use further
doubling under the SAME gates. Do not change physical inputs to pass.

Gates fixed before execution: relative matrix-identity residual <=1e-10;
EdS analytic-control relative error <=1e-7 at 2048 steps; normalized
Einstein-constraint residual <=1e-6; normalized maximum checkpoint
trajectory difference between 1024 and 2048 <=1e-4. Normalize each
column/component difference by max over the fine trajectory of that
component, with a floor 1e-10 times the column's largest component.
Include a separate absolute difference for near-zero components.

Report the actual dropped Z time term, not just k/(aH): on a>=0.1 compute
the L2 norm of Zdot divided by the root sum of squared retained terms
HZ, K_Q chi and CQ(E-chi). A value <=0.1 is a prospective approximation
accuracy screen, NOT an observational acceptance threshold. Also report
the actual clock-rate perturbation gamma/Q=deltaP/W and the rate that
would be incorrectly inferred by freezing the phase (gamma/Q=-Phi).

For both specified 1e-5 preparations, report maxima of |delta_b|, |F|,
metric and peculiar velocities, the two bounded-rate margins, and
|gamma|/min(Q-Q0,Qmax-Q). Also bound nonlinear spatial corrections via
|k chi/a|/[(1+lambda_s)a0/c^2]. If a ratio exceeds 0.1, mark that
preparation outside the conservative linear window rather than treating
its finite-amplitude extrapolation as a physical solution. The infinitesimal
transfer operator can still be reported. An inferred smaller allowed
amplitude is a validity bound, not a retuned successful test.

## Decision and continuation

The test decides whether this specified conserved-source response is
well behaved and whether freezing its time/current terms is justified.
A successful run supplies a dynamical outer-response building block,
not a fitted galaxy boundary or a halo-free observational victory.
If the frozen approximation fails, use the retained response in the next
nonlinear matching calculation. If the candidate response itself fails,
retain the failure and identify the affected premise before any revision.
Native formation, abundance economy and all eleven Stage 3 lanes remain
open. Continue immediately to the consequential next physical test.
