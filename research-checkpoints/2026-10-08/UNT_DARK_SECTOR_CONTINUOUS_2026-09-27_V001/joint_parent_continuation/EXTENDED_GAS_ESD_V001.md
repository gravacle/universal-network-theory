# Forward extended-gas control for the lensing contrast

2026-10-04. Pre-execution sensitivity specification; the target data and
their contrasts are already exposed. This is not a new predictive fit or
an assertion that the assumed gas has been observed. It tests one concrete
ordinary-matter alternative before attributing the contrast to a different
network coupling. Keep the inherited galaxy-calibrated a0 and shape fixed.

Use the already published isothermal hot-gas benchmark with R_h=100 kpc
and M_hot/Mstar in {0,1}, alongside the same cold-gas estimator. Consider
nominal Mstar in {1e10,10^10.5,1e11} solar masses. These are sensitivity
anchors, NOT estimated catalogue means or a mass prior. For each type split,
run high-type stellar shifts {0,.167} dex (colour) or {0,.141} dex (Sersic),
crossed with both hot-gas choices. Low type has zero shift and zero hot gas
in those four differential cases. Also include equal nominal gas on BOTH
types with zero stellar shift as a zero-contrast/absolute-response control.
The stellar offsets use the study's illustrative method-plus-selection
estimates, not measured corrections. No best mass or case is selected.
There are three explicit physical benchmark choices: nominal stellar mass,
differential stellar scale and differential gas fraction; none is a native
prediction or a fitted global force parameter. The density shape, gas radius
and type assignment are additional adopted assumptions.
[Primary source, sections 4.3, 5.2 and 5.4](https://arxiv.org/html/2106.11677v1).

At each of the same seven primary gbar coordinates, hold fixed

    M_nom=S_nom[1+10^(6.63-.69 log10 S_nom)],
    R=sqrt(G M_nom/gbar).

For the high-type true stellar mass S=10^delta S_nom, recompute the cold-gas
estimator, set M_c=S(1+f_cold(S)) and M_h=f_hot S, then use

    M(r)=M_c+M_h min(r/R_h,1), m(r)=dln M/dln r,
    g_N=G M(r)/r^2, f(g/a0)=g_N/a0.

Changing R with the true shifted mass would incorrectly cancel the catalogue
bias being tested. The conditional stationary Phi=Psi spherical projection
is evaluated directly, not by an SIS conversion:

    DeltaSigma(R)=1/(2pi G) integral_0^(pi/2)
      cos(theta) [g+(2-m)g_N dg/dg_N] dtheta,
    r=R sec(theta), dg/dg_N=1/f'(g/a0).

Split the quadrature at theta_h=acos(R/R_h) when R<R_h; the mass slope jumps
there. The density truncation is part of this benchmark, not a fitted cutoff.
For Newton gravity the gas-only answer is independently analytic:

    Mh/(pi Rh R^2)[Rh-sqrt(Rh^2-R^2)+(R/2)acos(R/Rh)]  (R<Rh),
    Mh/(pi R^2)                                      (R>=Rh).

Add Mc/(pi R^2) for its compact source. Verify this at radii .01,.1,.3,.8,
.99,1,1.01,2,10 times Rh to relative 1e-8, zero-gas recovery against the
existing compact projection to 1e-8, and 64/128-node split quadrature to
1e-7. Check positive fields/slopes and matched zero-contrast recovery.
Failing controls are preserved before data scores; do not loosen tolerances.

For each of all 30 cases, report predicted low/high ESD and their difference,
the fixed paired 14-bin Q and contrast 7-bin Q with the saved full covariance,
and all seven physical R. Explicitly flag R<30 kpc (compact source questionable)
and R>300 kpc (isolation caution). Keep fixed seven-bin scores so selection
does not change with the result; flagged cases are not equal-quality tests.
No optimizer, sigma conversion, fitted gas profile, data rebinning or union
of overlapping colour/Sersic evidence. Unknown stacking weights, mass scatter,
stellar calibration and external field/environment prevent a likelihood claim.

Independent source review accepted the projection and Newton formula before
execution and required the fixed-nominal-R and radial-validity cautions above.
One small numerical worker; no new download or installation.
