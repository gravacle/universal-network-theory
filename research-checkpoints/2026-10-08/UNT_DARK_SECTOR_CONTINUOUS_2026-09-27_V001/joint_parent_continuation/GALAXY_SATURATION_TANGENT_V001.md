# Galaxy leverage on the shared expansion scale

2026-10-03. Prospective diagnostic, not a new galaxy fit. The purpose is to
test whether the existing NGC3198 fields have measurable leverage on the
universal saturation ratio r independently of cosmology. A very weak
derivative is a useful physical result: these curves would not supply the
claimed expansion prediction even with other source inputs held fixed.

Reuse the frozen HALOGAS40/120 fields, density, observation radii and
errors without alteration. All observations are exposed development data.
The single tangent is at the inherited r=25.51664211557329, with a0,
baryonic source, distance and inclination fixed. It is not a likelihood
interval or a global fit, and says nothing about whether another r fits
better. Releasing source nuisances can only reduce local independent
information relative to this fixed-source, diagonal-error diagnostic.

For the actual discrete residual R(phi,p), p=ln r, solve

    J chi = -R_p,   J=partial R/partial phi.

Differentiate the complete face law, including interpolated transverse
gradients and outer potential/tangent boundaries. The prescribed baryon
bottom flux has zero p derivative. Use the existing logarithmic boundary
quadrature (64 nodes); the inverse-force derivative is -f_p/f_g.
The physical source equation and its numerical mesh are not changed.

The discrete Jacobian need not be symmetric. Use a small NumPy flexible
GMRES with the positive normal-gradient face matrix as an iterative
preconditioner. SciPy is absent in the existing runtime; do not install it.
Inner diagonal-preconditioned CG is only a numerical preconditioner, not
the scientific tangent operator. Freeze inner tolerance1e-2/cap2000,
outer restart20/cap200 iterations and true residual1e-8 relative to R_p.
Stop with an unresolved result if these limits fail. One case runs at a
time. No nonlinear parameter sweep or new observational sample is opened.

Before interpreting a solve, require: original residual/readout reproduced
within1e-11/1e-10 scaled error; independent complete-residual centered
directional checks at steps1e-4 and5e-5 within1e-5 relative error; boundary
quadrature derivative64/128 within1e-7 relative error. Complex-step
derivatives of the parameterized analytic flux are checked against centered
differences, not accepted solely because a solver converges.

Also solve J d=-R for the saved base-field defect. Keep the saved phi
untouched. Compare its velocity correction to the tangent velocity vector
(max norms; flag above1%). This is not by itself a sensitivity-error bound:
recompute J and R_p at phi+d and report the residual of the SAME chi there.
Require that shifted tangent residual <=1e-3 for diagnostic qualification.

Start with the saved 40-arcsec N256/L255 case. If controls pass, continue
serially with N512/L255 and N320/L1023, then the 120-arcsec representation
when useful. Require derivative-specific mesh/domain max-norm changes <=5%
for a qualified fixed-source leverage statement. Failure is unresolved
derivative convergence, not permission to change the threshold. The two
gas representations are correlated source choices, not independent galaxies.

Report dv/dln r at the 43 inherited radii and
I=sum[(dv/dln r)/sigma_v]^2, with 1/sqrt(I) only a local fixed-source
curvature scale. Do not call it a confidence interval. Report the linear
velocity change for delta ln r=ln(33.31908967768237/25.51664211557329)
ONLY as a local forecast for the newly derived expansion-bound displacement;
its finite-change accuracy is untested. A scientific constraint on r needs
nuisance projection, nonlinear range checks and an explicit likelihood.

Preserve every attempt and numerical failure. If this inherited galaxy
law has inadequate leverage, do not continue a low-field parameter sweep;
choose a predeclared high-field or environmental observable, or derive an
additional universal relation from a specified network mechanism.
