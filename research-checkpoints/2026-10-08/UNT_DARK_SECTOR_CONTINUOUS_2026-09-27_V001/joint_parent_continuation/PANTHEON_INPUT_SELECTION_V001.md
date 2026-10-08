# Pantheon+ input selection and exposure

2026-09-29. Select the official Pantheon+ SN-only distance product and full
statistical-plus-systematic covariance at repository commit
c447f0fea703fcd0fff57de5000947b5ca81286b, verified using the public GitHub commit
endpoint. No data score or cosmological fit is performed by this selection.

The source README and SN-only reference likelihood were read. They specify
zHD>0.01, standardized m_b_corr, and a full covariance submatrix in unchanged
row order. Multiple light curves of one SN must not be deduplicated: their
correlations are part of the supplied covariance. The theory uses zHD in
the radial integral and the distinct (1+zHEL) factor in luminosity distance.
No Cepheid distance substitution or MU_SH0ES absolute calibration is selected.
One common magnitude offset will be profiled; diagonal plotted errors are
not an acceptable substitute for the supplied covariance.

This is NOT an independent blind validation set. The existing reference
Omega_m=0.334 and its alternatives already derive from a Pantheon+ standard-
model inference; their use is explicitly noted in cosmology_closure_arithmetic.py.
The same-state raw-observable test is useful, but neither the inherited
Omega_m prior nor an inferred SN H0 may be counted again as separate data.
The present commit/selection is metadata-driven, not selected for a favorable
new likelihood result. A genuinely unused comparison remains separately open.

The four source files will be fetched individually by
fetch_pantheon_reference_v001.py and saved as reversible compressed ASCII
input receipts via the normal file-edit tool. Decoding must reproduce their
original byte lengths and SHA256 values before scientific reading. No source
is installed or executed; the published likelihood is a read-only reference.
The network fetch helper writes only stdout, and its digest is in each receipt.
No clone, repository synchronization or credential transfer is involved.

Primary references:
- https://github.com/PantheonPlusSH0ES/DataRelease
- https://arxiv.org/abs/2202.04077

Before scoring, freeze a separate source/protocol covering full-covariance
qualification, normalization/reference reproduction, finite-pressure distance
precision, shared-model/comparator inputs and retained per-row residuals.
This input acquisition is not completion of the supernova or joint test.
