# DESI DR2 expansion-shape census: prospective numerical protocol

2026-09-29. Fixed before predictions or scoring. Implements the root's
DESI_BAO_OUT_OF_CALIBRATION_PRESELECTION_V001.md without altering its parent,
reference alternatives, complete data vector or interpretation. Root is the
sole runner after independent preflight and source freeze.

## Candidate, inputs and complete census

Use all 18 rows of the authenticated COSMOLOGY_CLOSURE_ARITHMETIC.json:
Omega_b=omega_b/(H0/100)^2, Omega_exc=the retained missing-density coefficient,
Omega_m=Omega_b+Omega_exc=1-Omega_Lambda_ref. Verify that identity. Preserve
the original reference case, H0, acceleration-reference and BBN labels even
where the resulting expansion shapes duplicate. They are alternatives, not
18 independent observational tests or a posterior sample. The four soft
quadratures do not create extra expansion predictions.

The primary candidate is the declared ideal balanced/averaged hard limit,
E(z)^2=Omega_m(1+z)^3+1-Omega_m. Its state, clock, ordinary-matter and
finite-gap qualifications remain those of the reviewed hard-limit interface.
There is no coefficient fit to these new distances.

Read the COMPLETE 13 entries and 13-by-13 covariance from the pinned files
in desi_dr2_bao_external_v001. Match exactly their stated redshifts/labels;
the final z=2.33 pair is DH followed by DM. The covariance is never silently
reordered or diagonalized for scoring. Check finiteness, symmetry, positive
definiteness and Cholesky reconstruction. The README contains primary URLs,
commit and byte hashes; freeze it and both exact data files.

These are survey-inferred BAO distances with their template and covariance
assumptions, not raw photons or assumptions-free observables. Data are outside
the model calibration, but not fully blinded: the exposure history, including
the paper's displayed comparator score, remains in the README. That number
is NOT a numerical target or acceptance threshold.

## One exposed acoustic-scale nuisance and one comparator shape

Compute dM=integral_0^z dz/E, dH=1/E and dV=(z dM^2 dH)^(1/3). For each
reference analytically profile ONE common A=c/(H0 rd)>=0 across all 13 rows:

    A=max(0, d^T C^-1 y/(d^T C^-1 d)).

Use Cholesky-whitened dot products for production. Retain the unconstrained
value, active-boundary flag, derivative/Hessian, every predicted value and
signed residual, whitened residual, full quadratic score, and the diagnostic
conditional rd=c/(H0 A). A fitted rd is not a network acoustic-ruler prediction.
Covariance-weighted residual contributions can have either sign and are not
independent bin likelihoods.

For each anisotropic pair also report its original row indices, the DM/DH
covariance submatrix, correlation, observed AP=DM/DH, delta-method ratio error
and model ratio. Reordering a two-row DISPLAY to DM,DH does not alter the
primary vector. These ratios/errors are descriptive only; no Gaussian ratio
likelihood is used. An A=0 prediction makes its displayed AP ratio undefined.

The comparison family is the SAME flat dust-plus-vacuum formula, now with
Omega_m freely profiled over [0,1] as well as A. Independently retain the
uniform 257- and 513-point profiles, both finite endpoints, the best grid
point, and every sampled interior local-minimum bracket. Refine each such
bracket using 80 golden-section iterations, with no prior concentration or
branch selection by closeness to an exposed paper result. Save every candidate
and all profile arrays. Compare the selected minima between grids. This is
a converged numerical profile census, not an analytic proof of a global
minimum. The extra fitted shape is counted; raw score differences are not
a predictive-victory claim or a likelihood-ratio significance.

## Frozen numerical controls, not physical-success gates

Primary integrals use fixed 96-point Gauss-Legendre quadrature, checked against
48-point Gauss-Legendre. An independent composite Simpson calculation with
2048 equal subintervals checks every reference and every comparator candidate.
It uses its own nodes/weights, not an interpolation of the Gauss integral.

Prospective numerical tolerances:

* Gauss48/96 shape relative difference <=2e-12.
* Simpson/Gauss shape relative difference <=2e-11.
* Same-parameter network/comparator identity, exact endpoint controls,
  amplitude recovery/direct solve agreement: relative 2e-12.
* Cholesky reconstruction and covariance symmetry: absolute 2e-12.
* Method/direct quadratic-score differences: absolute 2e-8.
* Comparator grid-minimum differences: score <=2e-8, Omega_m <=1e-6,
  A relative <=1e-6. These do not impose a preferred Omega_m or score.

Exact endpoint controls are Omega_m=0: dM=z,dH=1,dV=z; Omega_m=1:
dM=2[1-(1+z)^(-1/2)], dH=(1+z)^(-3/2), with dV from its definition.
At synthetic Omega_m=.27, A=42, retain exact synthetic amplitude recovery
and zero residual (quadratic score <1e-18). A synthetic negative vector -d
must select A=0 with the correct nonnegative boundary derivative. For all
actual references independently compare the direct C solve with the whitened
amplitude and quadratic score. Separately compute the native-component
Omega_b/Omega_exc expansion and the same-Omega_m comparator to verify the
parameter identity rather than changing the physical shape.

Retain all coarse/method controls even if any numerical gate fails. No
observational pass/fail cutoff, significance, AIC/BIC or fitted source-state
selection is introduced. A technical revision after outcomes preserves the
failed version and evidence; it is not an opportunity to replace the model.

## Separate radiation-omission diagnostic, with measured input exposed

The primary frozen dust model and its score are unchanged. Quantify omission
using the measured temperature T=2.72548 +/- .00057 K from
[Fixsen2009](https://arxiv.org/abs/0911.1955v2). Evaluate the central temperature
and both quoted endpoints as sensitivity alternatives, not a new probability
integral. From the Planck integral use

    u_gamma=8 pi^5 k_B^4 T^4/(15 h_P^3 c^3),
    Omega_gamma=8 pi G u_gamma/(3 H0^2 c^2).

Use exact SI c=299792458, h_P=6.62607015e-34 and k_B=1.380649e-23, as
defined by [BIPM](https://www.bipm.org/en/measurement-units), and nominal
G=6.67430e-11 from [CODATA2022](https://physics.nist.gov/cuu/pdf/all.pdf).
G's uncertainty is not propagated; this is an omission diagnostic, not a
complete radiation-parameter inference.

Report photons only and the EXPLICIT illustrative all-massless factor
1+(7/8)(4/11)^(4/3) Neff with Neff=3.046. The definition and this historical
standard-decoupling example are given in
[Mangano et al.2005, equation2](https://arxiv.org/pdf/hep-ph/0506164).
This is not a current measured low-redshift neutrino density; finite neutrino
masses and any nonstandard photon source require their actual evolution.
The illustrative case is not a rigorous upper bound on arbitrary radiation.

Hold the calibrated PHYSICAL dust and vacuum coefficients fixed and calculate

    H_rad(z)^2/H0_inherited^2=E_dust(z)^2+Omega_rad(1+z)^4.

Therefore H_rad(0)/H0_inherited=sqrt(1+Omega_rad). State that change; do not
silently subtract radiation from the already matched vacuum to restore the
old H0. Compute only fractional changes to H and the 13 distance components,
with independent Simpson checks. Do NOT profile A or score this diagnostic.

For 0<=z<=2.33, q(z)=Omega_rad(1+z)^4/E_dust(z)^2 increases monotonically for
the retained nonnegative dust/vacuum coefficients. The rigorous all-interval
fractional distance-decrease bound is 1-1/sqrt(1+q(2.33)); the H increase is
bounded by sqrt(1+q(2.33))-1. Check the actual changes against these bounds.
This bounds the named ordinary-radiation omission only, not finite-hard-gap
pressure, clock instability, photon production or acoustic-template changes.

## Byte custody, execution and output

`desi_bao_shape_v001.py freeze` authenticates exact inputs and prints only a
JSON source/configuration snapshot. It does not calculate a prediction or
score. Root publishes that stdout as DESI_BAO_SHAPE_V001_FROZEN.json using
normal file tools. `run` refuses changed sources/configuration, then prints a
single JSON wrapper with payload and freeze hashes. Root publishes the result.
The worker never writes files, downloads, installs, launches child workers or
imports another numerical producer. NumPy and the Python standard library are
sufficient. No job deadline is imposed.

Freeze includes this code/protocol, preselection, reviewed physical interface,
paired-state note, external README/data and authenticated inherited reference
source/ancestors. All paths resolve inside the exact project root. Output
retains all18 reference records, both comparator profiles, complete covariance,
all six anisotropic-pair diagnostics, synthetic controls and all108 radiation
sensitivity rows. Output is bounded at1MiB; numerical status and every failure
name remain visible. A failed numerical check exits nonzero after printing
the complete result. There is no physical outcome encoded in COMPLETE.
