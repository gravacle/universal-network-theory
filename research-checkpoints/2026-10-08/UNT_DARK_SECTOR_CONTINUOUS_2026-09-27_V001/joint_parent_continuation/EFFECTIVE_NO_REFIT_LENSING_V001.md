# No-refit cross-probe check: published weak-lensing accelerations

2026-10-04. Follow the completed SPARC effective screen with a different probe,
without refitting its acceleration scale. This is a conditional comparison
to a published reduced data product, not a raw-shear likelihood or blind test.
The table and authors' qualitative conclusion were read before this protocol;
no numerical score has yet been calculated and no parameter is selected here.

## Observable bridge

The inherited WEAK_FIELD_LENSING_PATHWAY.md derives leading Phi=Psi for the
adopted stationary weak-metric, aligned-clock, minimally coupled branch. The
extra empirical disk closure used in the population screen is not needed in
an isolated spherical exterior: its underlying flux law there obeys
f(g/a0)=G*Mb(<r)/(r^2*a0). Transfer that SAME law and calibrated scale, not
the unsolved K(X)/compression state, to the ideal spherical weak-lensing limit.

For equal weak metric potentials, light deflection satisfies

    alpha(R) = (2/c^2) integral g(sqrt(R^2+z^2))*R/sqrt(R^2+z^2) dz.

Equivalently define a geometric diagnostic density through
rho_eff=[d(r^2*g)/dr]/(4*pi*G*r^2). This is a representation of the metric,
not new freely fitted matter. GR-like thin-lens deprojection then recovers
this same g. In particular for circular projected symmetry,

    DeltaSigma = c^2/(8*pi*G) * [alpha/R - d(alpha)/dR].

The deep isolated limit g=sqrt(G*Mb*a0)/r gives
alpha=2*pi*sqrt(G*Mb*a0)/c^2 and
DeltaSigma=sqrt(G*Mb*a0)/(4*G*R); the Newtonian point-mass limit gives
DeltaSigma=Mb/(pi*R^2). These checks fix the normalization/sign. The deep-limit
formula is NOT substituted for finite-radius predictions below; use the
complete inherited scalar inverse at each published gbar.

Conditional Phi=Psi and branch/geometry assumptions are essential. A scalar
rotation law alone would not predict this light bending. Background matching,
external fields, source geometry, current conservation and state formation
remain unestablished for a complete shared cosmology.

## Data and frozen comparison

Use all15 rows of Table1 of Mistele et al., arXiv:2310.15248v2:
https://arxiv.org/html/2310.15248v2 . Record the table numbers in the source
script, checked against the primary publication. The paper reports SI log10
accelerations, not values to be multiplied again by h70. Its distances use
H0=73 and flat FLRW Omega_m=.2793. Thus this comparison inherits a cosmological
distance reduction; it cannot establish an alternative expansion history.

The authors deproject lensing ESD, adopt stellar/gas estimates and spherical
symmetry, and assess exterior extrapolation. Their Table1 statistical and
interpolation/extrapolation errors omit an additional approximately.1dex
vertical stellar-mass systematic. Bin covariance and raw source-lens weights
are unavailable in this table. Do not treat all errors or bins as independent.
The .1dex vertical mass band is the authors' translation of approximately
.2dex mass uncertainty through the deep-regime square root, not an additional
independent error to combine with the horizontal mass sensitivity below.
Their stellar-population convention is chosen to be consistent with SPARC:
this is a different observable with shared nuisance assumptions, not a wholly
independent calibration of ordinary matter.

Predict the table using a0=1.0059833281731022e-10 for the inherited shape and
a0=1.0022739170327795e-10 for RAR, exactly as fitted on51 SPARC calibration
galaxies. Also predict g=gbar. No lensing amplitude, slip, stellar mass,
background, external-field or interpolation-shape parameter is fitted.
Authenticate the SPARC receipt and law sources before calculation.

Report every residual, equal-bin RMS and mean log residual. The primary
interpretive subset has log10(gbar)>=-13, the paper's conservative isolation
warning boundary; retain and report the remaining rows as a flagged extended
comparison, not discarded failures. This is a source-motivated choice after
table exposure, not a preregistered blind sample. Do not quote chi-square,
independent-bin significance or model-selection evidence from this table.

Show predictions under fixed horizontal shifts of gbar by+/-.2dex, solely
as coherent mass-scale sensitivities, NOT fitted shifts or uncertainty
marginalization. Save the local-curve variation over+/-.125dex in gbar as a
bin-width diagnostic; it is not a reconstruction of the actual stacking
weights or observational errors. The table may not suffice for a precise
bin-averaged forward model. Retain published statistical/systematic numbers
without converting them into a newly calibrated tolerance.

This calculation may show consistency, tension, or an effectively identical
prediction to RAR. None establishes an advantage over all dark-matter models.
Any next actual lensing likelihood should project the model to published ESD
or shear, use the real covariance, consistent mass distributions and geometry,
and keep galaxy-calibrated parameters fixed. Do not fit a favorable lensing
normalization then call it a cross-probe prediction.

Primary references: [Mistele et al.](https://arxiv.org/abs/2310.15248),
[KiDS data release](https://kids.strw.leidenuniv.nl/sciencedata.php), and
[Brouwer release documentation](https://kids.strw.leidenuniv.nl/sci_data/brouwer2021_rar_README.txt).
The corresponding older ESD release is available; no raw-shear work or large
download is needed for this first15-point descriptive check.

Execution note: the first launch stopped at Python parsing, before any science,
because both the table label and table numbers used the keyword `table` in one
dictionary constructor. The label key was corrected to `table_label`; no
input, criterion, prediction or result changed and no receipt existed yet.
