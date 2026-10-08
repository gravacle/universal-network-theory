# Population test of the existing effective response

2026-10-04. Prospective computational protocol, before new population residuals
or calibration. This implements the user's choice to retain measured inputs,
permit universal calibration, and test a different physical interpretation.
It is a bounded empirical screen, not a new microscopic consistency queue.

## Model and claim

Let gbar=(Vgas*abs(Vgas)+.5*Vdisk^2+.7*Vbul^2)/R, converted to SI.
Use the exact inherited scalar flux f from disk_solver.py and adopt

    gpred = a0 * inverse_f(gbar/a0).

The scalar flux comes from the existing conditional relaxed quartic-mode
construction. Applying its inverse directly to the radial baryonic reference
acceleration of a disk is an ADDITIONAL empirical closure. It is not the
axisymmetric nonlinear field solution, the evolved K(X)/cTheta state, or a
native UNT derivation. No lensing or expansion prediction follows from this
scalar closure alone. Its fixed asymptotic BTFR is not new independent evidence.

Fit only a0 universally. Hold r=gs/a0 at the inherited value recorded by
disk_solver.py (approximately25.5166421). This is another calibrated physical
input, originally selected using cosmology, not a derived constant. The two
stellar M/L conventions are imported, not individually fitted. Gas includes
helium1.33 already; negative gas forces keep their signs. The ordinary-matter
component velocities are Newtonian reference calculations from the photometry
and gas data, not directly measured accelerations or an assumption about total
gravity. Distance, geometry, circular-motion and tracer assumptions remain.

Comparators on exactly the same rows: gpred=gbar; and the empirical RAR
gpred=gbar/[-expm1(-sqrt(gbar/a0))], with its OWN one-parameter calibration.
Also retain the inherited effective law at a0=1.2e-10 SI without a new fit.
RAR was developed on this archive: it is an informed empirical benchmark,
not a previously unexposed competitor. No fitted-halo or full LambdaCDM
predictive comparison is claimed by these three/four curves.

## Selection and exposure

Use the two resident SPARC MRT files in external_ddo154_v001. Select Q<=2
and inclination>=30deg from the sample metadata. Exclude NGC3198 and DDO154
from calibration/evaluation because already modeled in this program. All
other finite rows with R,Vobs,eVobs,gbar strictly positive are retained;
record every exclusion and its reason. No 10% velocity-error or radius cut.

Assign whole galaxies by SHA256(UTF8 galaxy identifier), interpreted as a
big-endian integer: remainder0 modulo3 is calibration, remainder1/2 evaluation.
No radii from one galaxy cross the split. The archive is public and previously
resident/exposed; this is a prospective in-program split, NOT blind new data
or an independent rediscovery of the RAR. No alternative split is selected
after scoring. All objects/rows and memberships are saved.

## Fit, score and uncertainty limits

Fit log10(a0) in[-12,-8] by minimizing the mean across calibration galaxies
of their mean squared log10(gpred/gobs), where gobs=Vobs^2/R. Each galaxy has
equal total weight. Use81- and161-point grids, refine EVERY sampled interior
minimum by golden-section search, and retain both endpoints. Compare refined
best log10(a0) to1e-6 and loss to1e-10. Boundary minima are reported, not hidden.
This is an empirical loss, not a likelihood or an errors-in-variables fit.

Freeze both fitted constants before evaluation. Primary descriptive score:
sqrt(mean_g mean_r log10(gpred/gobs)^2), in dex. Retain velocity RMS, per-galaxy
losses/biases and every baseline prediction. Compare inherited-shape and RAR
losses, and each against baryons-only, with paired galaxy resampling:10000
replicates, fixed seed424027; report percentile2.5/97.5 intervals. These are
conditional descriptive sampling intervals, not discovery significance,
complete systematic uncertainty, a posterior, or proof of population superiority.
Shared distance-method/group errors are not independent across all galaxies.

Record residuals by predeclared gbar bins[0,1e-11,1e-10,infinity], R/Rdisk
bins[0,2,4,infinity], and stellar disk central brightness bins[0,100,1000,
infinity] in solar luminosities/pc2. These are diagnostics, not new fit targets.
No new surface-density coefficient, local a0 or galaxy-specific history is fit.

Without refitting, repeat scores under each of six separate input sensitivities:
all distances shifted by their own quoted +/-error, inclinations shifted by
their own quoted +/-error, and both stellar M/L values multiplied by10^(+/-.1).
Distance rescaling uses R proportional D, baryonic V^2 proportional D, hence
gbar invariant and gobs proportional1/D. Inclination sensitivity uses
Vobs_new=Vobs_old*sin(i_old)/sin(i_new) only: source deprojection cannot be
reconstructed from these tables and is explicitly held fixed. Therefore it
is a kinematic sensitivity, not full inclination marginalization. Reject and
list nonphysical transformed inputs; compare models on identical valid rows.
These deliberately coherent shifts are stress tests, not confidence bounds
or optimal nuisance adjustments. Quoted random velocity errors, galaxy-specific
stellar variation, gas geometry, distance correlations and covariance remain
unmodeled in the primary loss. No reduced-chi-square or Bayes factor is claimed.

## Numerical qualification and decision

Before observations are fitted, check the inherited f(inverse_f(d)) on61
log-spaced d in[1e-8,1e4], relative error<=1e-9, positivity and monotonicity;
check low/high asymptotes at x=1e-8/1e8 within1e-6/1e-5 respectively. Synthetic
one-scale data must recover log10(a0) within1e-6, and score<=1e-12. Qualify
signed source arithmetic and distance/inclination transformations directly.
Any failed qualification is retained and stops observational scoring. Do not
change thresholds to match outcomes. One small serial NumPy worker, no install.

Improvement over baryons-only establishes that this effective response captures
missing rotational support in this sample. Equal or worse performance than
RAR means it has not earned a distinctive empirical advantage over that
benchmark; even a conditional advantage would not alone establish UNT or beat
LambdaCDM. Large unaccounted residuals trigger source/closure diagnosis, not
post-hoc row rejection. The result should decide whether to invest next in
full disk geometry and independent-observable prediction, or first revise a
specific physical response assumption. Current formation failures remain.

Expansion, lensing, growth, mergers, BBN/recombination, CMB perturbations and
separate network thermal-origin tests remain required. Inflation is a potential
later unification target, not an accomplishment inferred from this galaxy test.

Primary data/method references: [SPARC](https://arxiv.org/abs/1606.09251) and
[RAR](https://arxiv.org/abs/1609.05917). Their measured constraints are retained;
the causal interpretation and effective total response are what this test varies.
