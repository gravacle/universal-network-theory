# A compact-dwarf test of the fixed-state 100-pc filter

2026-10-05 UTC. New empirical-facing necessary-condition test, not a rerun
of the Solar Gaussian certificate. The parent is the FIXED-STATE filtered
bounded-source action, not either unqualified variable-strain extension.
Inputs and gates below are specified before execution. This tests whether
the scale adopted to suppress compact-source anomalies also suppresses
the binding needed by a compact stellar system.

## Observable and deliberately limited comparison

[Simon et al.](https://arxiv.org/html/1007.4198) report Segue1 luminosity340
solar V-band luminosities, projected half-light radius29(+8,-5)pc and
substantial ellipticity. Their binary-corrected velocity dispersion is
3.7(+1.4,-1.1)km/s. The companion
[Martinez et al. analysis](https://arxiv.org/abs/1008.4585) models membership
and binaries jointly and obtains radius28(+5,-4)pc. These are not wholly
theory-free numbers, but the velocity inference does not require inserting
the published Newtonian dark-halo mass into our force calculation. That
mass is explicitly NOT an input.

A [2026 uniform reanalysis](https://arxiv.org/html/2602.10200v1) exists and
must be assessed separately: an archival reanalysis is not a new independent
galaxy. The initial calculation uses the older binary-marginalized number
only as a disclosed reference scale, not as a raw-data likelihood or a
Gaussian significance. No current claim rests on treating2.6km/s as a hard
confidence bound. The data were inspected while choosing this test, so this
is exposed development evidence, not a blind selection.

Model the total ordinary source and tracer by the SAME spherical Plummer
profile, rho=3M/(4pi a^3)(1+R^2/a^2)^(-5/2). This is an explicit idealization
of an elliptical galaxy, not a fit of the actual member positions. Let a=28pc
for the declared companion-profile benchmark and M=340,1020,3400 nominal
solar masses, i.e. stellar mass/light1,3,10 at the nominal luminosity. This
is a nuisance/design envelope, NOT a measured mass posterior or a complete
luminosity-uncertainty envelope. No unseen gas, black hole or material halo
is inserted. All source and tracer assumptions are counted.

Set a0=1.0059833281731022e-10m/s^2, r=25.51664211557329, ell=100pc, and test
uniform external accelerations e=.5a0 and1a0. These are stipulated external
field cases, not a fitted Milky Way halo or a certified field posterior.
They must not be presented as covering every possible orbital environment.
Ignore tides and time dependence only for this stationary necessary test.

## Nonlinear field bound for the entire Plummer source

Reuse the proved Wiener-ball framework of FILTERED_SOURCE_NONLINEAR_BOUND,
but derive the source input for Plummer rather than substituting a Gaussian.
Its normalized Fourier transform has the positive mixture representation

    rhohat(k)/M=t K1(t)=integral_0^infinity exp(-u-t^2/(4u)) du, t=ka.

Each term is a Gaussian with sigma^2=a^2/(2u). Applying the old positive
Gaussian bound and Jensen's inequality gives

    epsilon=||S g_N/e||_A
      <= GM/(pi ell^2 e)[ln(1+4ell^2/a^2)+exp(-1)].

Use the same declared ball r0=.01, modal ball s0=.02 and binomial bounds
Jmax,DJmax,Lw. Replace the old Solar-only minimum-root polarization bound
with a new monotone quadrature enclosure. On64 equally spaced s intervals,
the function eta_mode(s)=1/(1+t_s^2) increases withs, where
t_s+t_s^3=h_e/(gc s^2). Therefore

    P(h_e)/(Kb h_e)
      <= sum_j (s_j^2-s_(j-1)^2)/(1+t_(s_j)^2).

Use upper endpoints, not an unguarded fitted integral. A lower endpoint sum
provides an independent enclosure check; the s=0 limit is zero. The same
modal/binomial proof then gives LF. If the strict contraction and self-map
gates pass, the exact static branch within the stated Wiener ball obeys

    ||delta g||_infinity <= A=e LF epsilon/(1-LF).

This bounds the ENTIRE nonlinear anomalous force, with both filters retained.
It is not merely a linear approximation or the nonlinear remainder. No
global uniqueness outside the ball or time-dependent formation is proved.

## Convert force into a necessary stellar-velocity bound

Use the stationary integrated stress/Jeans equation with a vanishing outer
stress-flux term. Do not assume Plummer has finite moment of inertia:
its second radial moment diverges. The relevant first moment is finite,
<R>=2a, and the Newtonian virial integral is3pi GM/(32a). Consequently

    <v^2> <= 3pi GM/(32a)+2a A,
    sigma_LOS,global^2 <= <v^2>.

The second inequality allows arbitrary velocity anisotropy; no division by3
is taken to obtain a more favorable rejection. Motion is relative to the
bulk center. For a representative luminosity/mass-weighted cylindrical
aperture R_ap=67pc, positive velocity moments imply the conservative bound

    sigma_LOS,ap^2 <= <v^2>/F_ap,
    F_ap=R_ap^2/(R_ap^2+a^2).

This is not the likelihood of the actual spectroscopic selection. Mass
segregation, binary orbital velocities, membership, ellipticity, pressure
surface terms, mass loss, tides and a nonstationary phase require separate
analysis. The equilibrium assumption is not protected from challenge.

## Frozen arithmetic controls

One small run, six mass/external-field cases. Prospective checks: binomial
domain, mode self-map, modal contraction, outer contraction and outer
self-map; lower/upper polarization enclosure contains a separate256-node
quadrature within2e-10;64-bin upper bound decreases under128-bin refinement
within2e-12; cubic-root residual2e-12; Gaussian-mixture normalization2e-10;
Plummer first-moment and Newtonian virial integrals against their analytic
values at2e-9; aperture expression matches the projected Plummer integral
at2e-10. Unit controls use the exact IAU parsec and nominal solar GM.

If any certificate gate fails, retain that case as uncertified, not as an
observational failure or a bound. Do not retune the radius, mass, external
field, ball or numerical gates after output. Report the scalar and aperture
upper bounds, not best-fit dispersions or exclusion significances.

Root and handoff_plan_review_v005 independently checked the Plummer mixture,
Jensen step, monotone spectral enclosure, anomalous-force norm and integrated
virial coefficients before execution. This is an analytic review, not a
population/raw-data analysis or a replacement for the full Stage3 program.
