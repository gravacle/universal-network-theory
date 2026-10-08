# Frozen-polarization Solar limit: independent saved-array audit

2026-10-04. **229/229 checks pass**, runtime 0.55 seconds. The audit reads all seven saved cases without importing a producer, solving an equation, repeating iterations, or fitting a parameter. Frozen inputs, inherited manufactured controls, all 15 new controls, primary receipt hashes, sensitivity identities, source arrays, units and qualification arithmetic agree. No frozen file was changed. The sole numerical slot was released immediately after the audit.

## Result and scope

The declared finite-radius extraction gives

    c2 = -0.08259037906990421,
    Q2 = -3(a0/rM)c2 = 2.170106621771691e-26 s^-2,
    rM = sqrt(GM/a0).

This is 0.522102682 times the earlier fully relaxed AQUAL prediction. The two declared external-field sensitivities give `1.956180857076367e-26` and `2.389272619054560e-26 s^-2`.

The sign is consistent with `delta Phi = -Q2 R^2 P2(cos theta)/3`. Against the adopted current Cassini/DE440 value `(1.6 +/- 1.8)e-27 s^-2`, the fixed-mean arithmetic residual is **11.16726**. The primary observational convention is [Park et al., Eq. 6 and abstract](https://arxiv.org/html/2602.17884v2).

This is not a posterior-marginalized significance. Galaxy acceleration-scale/source calibration, shape calibration and completion uncertainties were not marginalized. The two external-field cases are sensitivities, not a distribution or a refit. Uniform nonresponding polarization is an imposed changed state-response premise, not a native formed state or a demonstrated finite-response law. Nothing here establishes monotonic interpolation between frozen and relaxed limits.

## Independent contact and source checks

For `b = -bmag zhat`, the audit independently differentiates the fixed-state energy

    E(g) = |g|^2/2 - (b dot g)/sqrt(1+|g|^2/r_shape^2)

by complex-step differentiation and verifies the complete flux

    D = g - F b + F^3 g (b dot g)/r_shape^2.

The last term must not be discarded when polarization is frozen. The external polarization magnitude is separately checked against the positive mechanical equilibrium integral at 256/512-point quadrature. The reconstructed external Hessian coefficients are `Cperp=1.00262376180768`, `Cparallel=1.00780750904458`; the sufficient global ellipticity lower bound is `0.932134377337714`.

The saved spherical fields were converted to cylindrical Cartesian components, the complete polarization was calculated there, and the uniform external polarization was subtracted before rotating and projecting back. Legendre polynomials/derivatives were built by recurrence, not the producer's evaluation routines. This independently reproduces every stored Br and Theta modal array. The anisotropic outer Green normalization, regular inner boundary, SI conversion and all five primary qualification gates agree. Primary B/C, C/D and D/E differences remain `9.16718e-4`, `6.63088e-5` and `1.65007e-13`. C/D is a combined domain/spacing check, not an isolated boundary-error estimate.

## Finite extraction radius is understood, not forced to zero

The finest plateau variation is **0.00127215** (0.1272%), unlike the almost exactly harmonic relaxed-AQUAL inner field. A frozen contact source remains weakly non-harmonic at these radii.

Let `r` denote dimensionless radius and let the local regular dipole be `psi_1=c1 r+...`. At high central acceleration, the leading quadrupolar contact terms are

    Br_2 = (2/3) r_shape bmag (e-c1) r^4 + ...,
    Theta_2 = 4 r_shape bmag (e-c1) r^4 + ...,
    psi_2/r^2 = c0 + [r_shape bmag (e-c1)/3] r^3 + ... .

The continuum cubic coefficient is `14.7086724934`; the same coefficient through the actual fitted radial stencil is `14.6969921628`. Without fitting it, this accounts for the observed extraction-interval variation to **0.0644% of that small variation**. This is a descriptive asymptotic check, not a new acceptance gate.

The innermost saved coefficient is `c0 approximately -0.08259722183318`, giving `Q2 approximately 2.17028641905644e-26 s^-2`: only **0.008285% larger** than the predeclared median. The audit retains the original median as the qualified reported result. Neither finite extraction nor this contact correction materially changes the conditional comparison.

## Green, residual and flux checks

For the exponentially fitted l=2 recurrence, the source-derived inner coefficient is evaluated directly using

    c0_discrete = psi_2(r_N)/r_N^2 - sum_j W_j S_j,
    W_j = [1-exp(-5h(N-j))]/[(2 sinh(5h/2)/h^2) r_j^2].

No tridiagonal solve is repeated. Applying the same weights to the actual modal residual and retaining both boundary residuals gives an exact identity with finest error `8.43e-14`. The source-derived coefficient differs from the inner field by only `8.16e-9` relative; the weighted modal residual contributes about `-6.74e-10` to c0. The finest maximum scaled modal residual is `1.43e-8`.

A continuum finite-boundary Green integral, including the outer Dirichlet contribution and inner endpoint term, differs from the inner coefficient by **0.5154%, 0.1287%, 0.03216%** for A/B/C, and **0.03918%** for the enlarged-domain finest grid. This is consistent with second-order radial discretization. It is descriptive convergence evidence, not a rigorous infinite-domain error bound.

The finest complete-flux enclosed-mass diagnostic has maximum error `1.0671e-5`, and `4.4172e-6` within `0.05<r<10`. The same-domain A/B/C errors decrease by approximately four with each radial refinement. These flux/residual diagnostics are retained rather than described as exact conservation.

## Scientific conclusion

Under this specified uniform-polarization limit, freezing lowers the fixed central quadrupole by roughly half but **does not by itself produce the adopted measured Solar quadrupole** after retaining the bounded-source contact. The original relaxed-AQUAL result remains unchanged. This screens simple uniform freezing, not every finite spatial/time-dependent state, a dynamical transition, or all UNT. Any further state-response mechanism must supply its own physical formation, matching and energy/current accounting rather than treating this imposed limit as already realized.

Audit JSON: `SOLAR_FROZEN_POLARIZATION_V001_AUDIT.json`, SHA256 `982609fdd9d787e984063c5b5bf485a0b2c35c172f035c1d3c972892cafa94aa`. It pins all seven case receipts, source/protocol custody and the audit source. No additional numerical execution is needed for this report.
