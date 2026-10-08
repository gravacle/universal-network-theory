# Pantheon+ same-state finite-pressure distance comparison

2026-09-29. Prospective source; root alone freezes/runs. No new mode,
cosmological ODE, absolute-distance calibration, state fit or observation
selection. The independent input/exposure decision is
PANTHEON_INPUT_SELECTION_V001.md. Exact receipt filenames/hashes are bound
in the worker's source snapshot before execution; no downloaded code runs.

## Data, conventions and counted freedom

Use all rows of the official PantheonPlusSH0ES/DataRelease distance vector
and STAT+SYS covariance at commit c447f0fea703fcd0fff57de5000947b5ca81286b.
Four individual reversible compressed-text receipts retain the original
vector, covariance, README and SN-only reference likelihood. Before parsing,
decode with a64MiB ceiling, recover the declared byte count and SHA256, check
the repository/commit/path/key and fetch-helper identity, and preserve both
the transport and raw-file hashes. The numerical code never executes the
downloaded likelihood. Its misleading introductory combined-SH0ES comment
does not override its actual SN-only implementation.

Paths are pantheon_inputs_v001/PANTHEON_{VECTOR,COVARIANCE,README,LIKELIHOOD}_V001_TRANSPORT.json.
The covariance receipt uses thirteen ordered data_parts: remove exactly the
single final LF from each, verify its declared character count, join in the
declared order, then decode/verify original bytes. Freeze every part, not only
the manifest. transport_sha256 is the fetch helper's SOURCE hash, not a hash
of compressed covariance bytes. The other three receipts have inline data.

The ONLY data mask is zHD>0.01, exactly as the published SN-only likelihood.
Use standardized m_b_corr; zHD in the radial integral; zHEL in the endpoint
factor. Preserve every selected light-curve row, including multiple surveys
of one SN and any calibrator row that satisfies the mask. Do not deduplicate,
clip residuals, remove an outlier, substitute MU_SH0ES or Cepheid distances,
or add the plotting diagonal errors/peculiar-velocity errors again. Subset
the FULL covariance with the identical original row indices in both axes.

For the unchanged flat background define dimensionless dM=integral dz/E(z),

    q_i=5 log10[(1+zHEL_i)dM(zHD_i)],
    m_model_i=q_i+Mcal,
    Mcal=(1^T C^-1[m_obs-q])/(1^T C^-1 1).                    (1)

This is ONE unrestricted common magnitude offset per conditional history.
The actual absolute magnitude would be
M=Mcal-25-5log10[c_km_s/Hcal_km_s_Mpc], conditional on the already supplied
Hcal; report this only as a dictionary/convention, not as a measured H0 or
new SH0ES calibration. The residual sign is model minus observation.
Save the quadratic score, derivative, curvature, and every signed residual
and whitened residual. The normalization/determinant is common to all rows
of this comparison, not an additional fitted covariance.

This is expressly NOT a blind/independent new validation. The inherited
Omega_m=.334 and alternative reference coefficients were informed by the
Pantheon+ standard-model inference. Do not multiply the old Omega_m posterior
or a Pantheon-inferred H0 into this raw-vector comparison, or count them as
extra independent observations. The complete light-curve product also carries
its standardization, selection-bias and fiducial peculiar-velocity assumptions.
The result tests this fixed forward map against those published products; it
does not reprocess the survey or prove their nuisance assumptions invariant.
No joint BBN+BAO+SN likelihood or significance is manufactured here.

## Same physical histories; efficient exact distance evaluation

Reuse ONLY the authenticated Kernel and Background definitions and read-only
input authentication from finite_pressure_bao_ruler_v001.py. Never call its
run/main, acoustic or observational profile producer. Its source and freeze
must authenticate, including the unchanged ordinary massless3.044 reference,
saved photon normalization, scalar action law, matched vacuum and Hcal
convention. No hidden switch to standard CDM or a^-4 hard energy.

Keep all67 inverse points x5 backgrounds=335 histories and all1,340 source
labels. Four soft copies have the same normalized homogeneous history,
verified again with saved s and cosmic coefficients; their galaxy constitutive
differences are not erased. The Delta=0 infinite-gap dust branch is retained.
Unsupported inherited state statuses remain explicit and are never fitted
into the physical domain. The same ordinary-radiation dust comparator is
calculated for each background with the same single magnitude-offset fit.
Do not refit Omega_m, omega_b,R, helium, temperature, covariance or source.

Sort UNIQUE selected zHD only for integration, then restore every original
row for scoring. With t=log(r/r1), the imported monotone action map gives
an endpoint bracket [2log(1+z),3log(1+z)]. A batched safeguarded Newton solve
uses its exact derivative lambda/3, an absolute log(A) target4e-15 and at most
64 iterations; unconverged endpoints are retained as numerical failures.
No interpolation of distances or equation of state. Integrate successive
positive endpoint intervals with Gauss16 (check Gauss8), angle128 (separate
angle64 comparison), and cumulatively add them. At three fixed witness
indices—minimum, middle and maximum unique redshift—cross-check the original
scalar64-bisection endpoint and independent global Gauss64 integral. Also
check the maximum-redshift integral using fresh Simpson512 nodes.

Distance batches contain at most64 redshift intervals. The source allows
one history at a time for distance formation and bounded multi-RHS covariance
operations. No335-fold covariance storage or factorization. Threads1 before
NumPy; no SciPy, pandas, CosmoSIS or other installation is needed.

## Prospective numerical qualification

- Declared raw total vector/covariance size is1701. The actual selected count,
  mask hash, original indices and row identifiers are retained, not guessed.
- Covariance finite/symmetric, positive diagonal and successful Cholesky;
  symmetry and reconstruction error <=2e-12 absolute. No eigenvalue floor,
  symmetrization, regularization or diagonal replacement.
- Exact synthetic triangular solutions, profile shift invariance and common
  offset recovery: relative2e-11; synthetic noiseless score<=1e-18.
- Vector/scalar endpoint and distance, interval8/16 and angle64/128, direct
  global quadrature and Simpson: relative2e-10. Offset/score refinement uses
  absolute2e-9 magnitude and2e-6 score. These are numerical controls only.
- Whitened/direct-precision offset agreement and projected score identity:
  normalized2e-10; profile stationary derivative normalized to the absolute
  contribution sum <=2e-11. Cholesky solve residual <=2e-10 normalized.
- Same-state A1 anchors w,cI2,omega/R,I/R^3 and four-copy shape agreement use
  the already declared2e-10 material tolerance.

Synthetic cosmologies before real scores include constant H and pure dust,
whose exact dM are z and2[1-(1+z)^(-1/2)]. A synthetic covariance with
off-diagonal entries checks the mask/indexing and profile formulas against a
small direct solve. Physical synthetic magnitudes generated from q plus a
known offset must recover that offset. Adding a constant to every q changes
the fitted offset oppositely and leaves residuals/score unchanged. The
zHD/zHEL luminosity convention is checked algebraically against the reference
angular-distance expression, not silently replaced by (1+zHD) twice.

No observed-success threshold, chi-square-tail probability, AIC/BIC or choice
of preferred state. Retain every failure and refinement. Shared-calibration
parameters and reference alternatives are not335 independently estimated
cosmologies or independent evidence replications.

## Publication and recovery

Freeze authenticates source/inputs only, not a fit. A benchmark uses the first
finite state in the saved row order with its comparator and all qualification
controls. It is explicitly a subset, not completion. The prospective
run-background0..4 modes each retain67 histories; all five are required for
the full census, or run computes all335. Root records actual time/self RSS;
no arbitrary deadline. There is no checkpoint overwrite or hidden file write.

The covariance is stored once in its original authenticated source receipt,
not repeated in outputs. Output includes selected observations/redshifts/row
mapping once. Complete residual and whitened-residual matrices may be stored
as reversible zlib/base64 little-endian float64 arrays with exact shape,
byte count and SHA256; every element must round-trip exactly before output.
This is lossless transport, not precision rounding or row deletion. Predicted
magnitudes are exactly reconstructible as m_obs+residual. Preserve per-history
scalars and all numerical checks in ordinary JSON, as well as full source
label and reference mappings. Root owns stdout publication and review.
