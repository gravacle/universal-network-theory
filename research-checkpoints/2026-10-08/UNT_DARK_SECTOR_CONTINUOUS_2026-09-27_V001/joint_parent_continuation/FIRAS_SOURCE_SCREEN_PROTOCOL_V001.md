# FIRAS source-strength residual-space screen V001

2026-09-29. Prospective, before scoring. Source `firas_source_screen_v001.py`;
root alone freezes/runs it. No production run by the author, no installation,
new raw-data retrieval, native dynamics or new radiation propagation.

## Input and statistical meaning

The owned NASA product is `firas_inputs_v001/firas_monopole_spec_v1.txt`,
SHA256 `df793c3dca09ebfa7dbc5aa0ec1951daa8884431bc30eff28a710d7516cf50fa`.
All 43 ordered rows are retained. The retrieval receipt and manually transcribed
primary covariance metadata are also frozen. The latter records the complete
43-lag Q sequence, independently checkable against
[Fixsen et al. 1996, section 3.3](https://arxiv.org/html/astro-ph/9605054#S3.SS3).

Use only column3 residuals, column4 uncertainties and column5 Galactic-template
shape in inference. Column2 is a constructed 2.725K blackbody plus those same
residuals, in different units; it is **not another independent observed vector**.
Its reconstruction discrepancy is descriptive only because the product rounds
frequencies and intensities. [NASA product documentation](https://lambda.gsfc.nasa.gov/product/cobe/firas_monopole_spect.html).

The covariance is C_ij=sigma_i sigma_j Q[abs(i-j)], in (kJy/sr)^2. Integer channel
index, not differences of rounded frequencies, determines lag. Cholesky must
succeed; no diagonal approximation, covariance rescaling by fitted chi2, added
independent calibration variance or hidden covariance repair is allowed.

The primary Table4 is already temperature/foreground-subtracted, and its stated
foreground model used a roughly9K modified blackbody. The compact product lacks
the original fit coefficients, calibration nuisance covariance and complete
nonlinear foreground likelihood. This is therefore an exposed, rounded,
calibration/foreground-conditioned **residual-space linear GLS screen**, not
reanalysis of raw interferograms or reproduction of every FIRAS systematic.
For a fixed nuisance tangent span A, projecting a prior subtraction inside A
does not change the tested orthogonal component. An unknown subtraction outside
A, especially nonlinear dust-temperature changes, need not cancel. The retained
alternatives below expose that dependence; their spread is not a proved bound
on all missing systematics. No blanket source-class/UNT exclusion follows.
The reported `nominal_design_degrees_of_freedom` is43 minus the current design
rank, not a reconstructed sampling degree count. The original subtraction-induced
degrees of freedom and residual covariance are not independently reconstructed.

## Fixed complete census and freedoms

Evaluate both reference derivative temperatures 2.725K (NASA reconstruction)
and2.728K (1996 analysis), without selecting by fit. These are reference-coordinate
sensitivity choices, not two independent data sets. Always profile an unrestricted
temperature correction dB/dT. Preserve three nuisance alternatives:

1. nu^2 B_nu(9K) with unrestricted amplitude;
2. that shape plus its9K temperature derivative, a local tangent envelope;
3. the product's actual column5 Galactic-pole template with unrestricted amplitude.

The two9K shapes share a normalization giving the amplitude template a peak of
1000kJy/sr. The derivative coefficient has units K times that amplitude; without
the removed foreground amplitude it is not an independently measured dust
temperature. Temperature coefficients likewise correct a residual baseline,
not a newly absolute-calibrated CMB temperature. No independent grey calibration
gain, arbitrary frequency offsets or per-channel nuisance is fitted. The
calibration accuracy remains inherited from FIRAS, not refitted away.

For each of these six reference/nuisance combinations retain one baseline and
15 one-source fits, hence6 baselines plus90 source rows. Do not fit source families
together or choose the best bath ratio. With B=B_nu(T), G=T dB/dT:

    mu:                 S_mu=-G/x,
    y:                  S_y=G[x coth(x/2)-4],
    inverse tangent:    S_inv=G,
    grey exchange:      S_grey(r)=B_nu(rT)-B,
    pure emission:      S_emit(r)=B_nu(rT).

The fixed positive r values are {.5,.9,1,1.1,4/3,2}. They are explicitly
declared sensitivity examples, not fitted temperatures or a native bath
prediction. The12 grey/emission templates plus mu,y,tangent give15 rows.
The grey source at r=1 is identically zero. The inverse-constructed source is
exactly degenerate with temperature. These twelve rows across six nuisance
choices must remain unidentifiable with null amplitude/error, not false finite
bounds, successful predicted blackbodies or outcomes to delete.

Physical ordinary frequency is nu_Hz=100*c*nu_cm^-1. Use exact SI h,kB,c and
1kJy=1e-23 W m^-2 Hz^-1; B_nu=2h nu^3 f/c^2. No wavenumber-density Jacobian is
applied to a product tabulated in Jy per Hz. These physical photon conventions
are adopted, not supplied by the native finite clock model.

## Strength and likelihood calculation

At each row fit y=A b+epsilon S with known C. Whiten with C=L L^T, scale design
columns for conditioning, solve least squares and retain the full coefficient
covariance. With Q spanning whitened nuisance columns, S_perp=(1-QQ^T)L^-1 S:

    epsilon_hat=(S_perp dot y_perp)/|S_perp|^2,
    sigma_epsilon=1/|S_perp|,
    chi2(epsilon)=chi2_min+(epsilon-epsilon_hat)^2/sigma_epsilon^2.

Rank degeneracy is declared if ||S_perp||/||L^-1 S||<=2e-12 (zero template also
degenerate). Other unexpected rank loss stops execution and retains failure.
Numerical COMPLETE means this census and controls completed, not an observational
acceptance of any source.

Report the signed estimate and nominal two-sided profile band at
Delta chi2=3.841458820694124. For physical grey/emission epsilon>=0, also retain
the interval measured from the constrained optimum max(0,epsilon_hat):

    radius=sqrt(max(-epsilon_hat,0)^2+DeltaChi2*sigma^2),
    interval=[max(0,epsilon_hat-radius), max(0,epsilon_hat+radius)].

These are nominal Gaussian profile ranges conditional on the supplied covariance
and nuisance span, **not** coverage-certified95% limits including systematics.
Negative unconstrained estimates are retained. For a frozen-temperature grey
bath the exact mixture solution uses epsilon=1-exp(-tau) in [0,1]; its interval
intersection with that domain is reported separately. General evolving
temperature, opacity and expansion histories are not inferred from this mixture.

The spectral shapes are exact instantaneous derivatives of the previously
declared collision laws. For small exposures epsilon~integral kappa dt (grey)
or integral j dt (emission), the associated energy/number changes relative to
the initial photon bath are epsilon(r^4-1), epsilon(r^3-1), or epsilon r^4,
epsilon r^3, respectively. These signed quantities at the reported upper
strength and the maximum fractional change across the43 channels are retained.
They are not a cosmological fraction supplied since an inferred production
epoch. The inverse tangent has no monopole strength bound after temperature
profiling; energy debit, T(z) and angular/polarization opacity remain separate
tests. The pure-emission r=4/3 moment equality does not imply spectral tangency.

The exact nonlinear temperature correction beyond dB/dT at the fitted nuisance
coefficient is reported as a whitened norm for source rows, not an outcome-fitted
threshold or proof that a finite evolving-source history has been solved.

## Reference and numerical controls

Published mu/y estimates, statistical/systematic errors and headline limits are
stored as descriptive context from primary Table2/sections6.2–6.3. Compare
separate mu/y fits with the published estimates and statistical errors, but impose
no numerical agreement gate. The compact product/reference-template choices
cannot exactly replay the authors' Galactic-cut/calibration analysis. In
particular do not add the published y systematic as a universal extra noise term
for unrelated network templates or call this a renewed full FIRAS likelihood.

Before interpreting fitted strengths retain these prospective checks:

- exact channel/covariance symmetry/diagonal and Cholesky reconstruction;
- whitening identity and SVD least squares versus independent normal equations;
- projected amplitude and profile chi2 versus full-design fit;
- exact synthetic coefficient recovery on every identifiable design;
- simultaneous reversal of data/design and both covariance axes;
- Planck tangent against centered derivative/Richardson at relative steps
  1e-3 and5e-4;
- factored grey photon/energy moment defect and the pure-emission4/3 moment
  identity, plus exact tangent/r=1 degeneracy and all-census counts.

Identity tolerance2e-12; normalized linear-algebra tolerance2e-9; Planck
derivative tolerance2e-8. All are fixed before scoring. They are arithmetic
controls, not target-selection/chi2 acceptance rules. Every row retains its
template, fit model and residual; full covariance and raw table are saved once.
No clipping, dropped high-frequency rows, fit-quality source selection or silent
increase in precision/tolerance is permitted.

## Execution and custody

`freeze` reads/hash-checks the input corpus and emits its source/protocol/config
manifest to stdout. Root publishes it as FIRAS_SOURCE_SCREEN_V001_FROZEN.json.
`run` authenticates that parsed manifest and emits a payload-hashed wrapper only
to stdout. Scientific exceptions retain partial rows/checks and traceback as
FAILED_EXECUTION; there is no package installation, output-file write, subprocess,
network operation or producer import. NumPy is the only nonstandard dependency,
threads fixed to1. The43-channel matrices and96 small fits are bounded, modest
memory work; root remains the sole numerical producer. Keep exposed-data and
shared primary calibration provenance in any integrated report.
