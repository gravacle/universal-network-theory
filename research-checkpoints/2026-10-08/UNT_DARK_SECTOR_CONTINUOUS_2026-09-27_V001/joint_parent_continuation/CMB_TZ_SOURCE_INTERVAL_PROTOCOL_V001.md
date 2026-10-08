# Temperature redshift constraints on continuous photon production

This prospective calculation translates published temperature intervals into
constraints on the already derived continuous-source equation. It adds an
observational test of net photon production that can remain invisible to the
mean blackbody spectrum. It does not assume a Big Bang or inflation, reconstruct
raw molecular spectra, or combine overlapping published measurements.

## Physical assumptions and exact endpoint identities

Adopt the photon and metric interface in CMB_CONTINUOUS_SOURCE_ANALYSIS_V001.md:
ordinary redshift, two-polarization massless photons, homogeneous temperature,
and an exactly Planckian distribution maintained over the tested interval.
The earlier derivation gives u=Tdot/T+H, Q=4u rho and S=3u n. For emission time
t_z and today t_0, with a_0=1 and a_z=1/(1+z), integration yields

    L(z)=integral[t_z,t_0] u dt=ln[T0*(1+z)/T(z)],
    F_E=1-exp(-4L)=1-[T(z)/(T0*(1+z))]^4,
    F_N=1-exp(-3L)=1-[T(z)/(T0*(1+z))]^3.

F_E is the fraction of present photon energy added after redshifting the
initial contribution to today; F_N uses comoving photon number. Neither counts
gross absorption and replacement events. Negative values mean net removal
under this interface and are retained. If Q>=0 throughout the interval, the
allowed range is intersected with L>=0, not silently clipped into a detection.
If that intersection is empty it is reported empty. A homogeneous constant
physical temperature would instead give L=ln(1+z), F_E=1-(1+z)^-4.

For a constant-beta comparison T=T0*(1+z)^(1-beta), u=beta H and
L=beta ln(1+z). This ansatz is an adopted source history, not a native prediction.
An arbitrary beta(z) is not constrained pointwise by a constant-beta fit.

## Sources and statistical scope

The fixed input JSON transcribes source summaries, not raw independent
likelihood data. [Fixsen 2009](https://arxiv.org/abs/0911.1955) supplies the
combined present temperature 2.72548 +/-0.00057 K. This is not an additional
independent spectrum dataset beside the existing FIRAS screen.

[Muller et al.](https://arxiv.org/abs/1212.5456) report 5.08 +/-0.10 K from
non-LTE molecular excitation. [Kotani et al.](https://arxiv.org/html/2509.20760v1)
report 5.13 +/-0.06 K from HCN excitation toward the same absorber. The latter
uses CMB-dominated LTE, neglects collisions, treats covering factor and time
variability, and corrects column-density inhomogeneity. Its weighted channel
estimate is conditional on these choices; no full posterior is supplied here.
Both measurements are kept separately because the common object and systematic
effects preclude assuming independence. Kotani's full text gives the actual
absorber redshift 0.88582; its rounded 0.89 display value is not used as an
exact physical redshift. The rounded-redshift change is reported diagnostically.

[Riechers et al.](https://arxiv.org/abs/2202.00693) give a 16.4–30.2 K one-sigma
range at z=6.34 conditional on water excitation and starburst radiation
modeling. This asymmetric interval is propagated as given, not replaced by a
Gaussian. [Saro et al.](https://arxiv.org/abs/1312.2462) constrain constant beta
to 0.017 with -0.028/+0.030 quoted errors for 158 SPT clusters. Their SPT-only
summary is translated separately at the reported endpoint z=1.35; the tighter
combined-literature value is not double-counted.

All three temperature intervals and the beta interval are fixed before this
new numerical translation. The calculation makes no new fit and defines no
observational pass threshold. Source data are now exposed and cannot later be
called unused predictions. Report both fixed-central-T0 intervals and the
range over the rectangular reported-T0-error interval. A rectangle of marginal
intervals has no asserted joint 68-percent coverage. No two-sigma extrapolation
or likelihood product is licensed by these summaries.

## Numerical unit and review

The stdout-only stdlib worker has freeze and run modes. Freeze binds input
JSON, this protocol, source script and the prior analytical identities. Root
publishes its exact output before run. Every observed input and covariance
limitation stays in the result. Ordered extrema follow analytically from L
increasing with T0 and decreasing with Tz. Fixed identity tolerance is 2e-14
absolute for logarithm/power round trips, a numerical control only. Analytic
zero-source and half-energy synthetic checks are retained, not physical cases.
The independent review must check signs, endpoint order, measurement overlap,
coverage disclaimers and the distinction between net injection and turnover.

These constraints apply only to the adopted photon interface and measurement
interpretations. They do not reject early network generation, balanced
maintenance, inhomogeneous source constructions, or modified atomic/photon
laws without their own observational derivation. A surviving source still
owes its native rates, energy and momentum debit, spatial correlations,
polarization, and a shared expansion history. This is not Stage 3 completion.
