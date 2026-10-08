# Pantheon+ finite-pressure comparison: independent preflight V001

2026-09-29. Full source/protocol read. No producer was imported or executed,
no distance/score calculated, and no data or source changed by this reviewer.

Accepted current source identities:

- `pantheon_finite_pressure_v001.py`:
  `02b27f41f2cb0072e5d3b2418f3633b78338554fdea206046dc20e9c3197a350`.
- `PANTHEON_FINITE_PRESSURE_PROTOCOL_V001.md`:
  `561f024fc1f31992c911a3edff5f1776f565fbc274eaefbe523a8aa42af21f87`.
- Imported, authenticated expansion definitions:
  `finite_pressure_bao_ruler_v001.py`,
  `b59ab0f88e39234929eb6fa4d0a53bba0b1bf4dc4fbd9891b704b5cd89e19bf1`.

The source, complete protocol and input-selection note were read, together
with the imported authentication, Kernel and Background definitions. The
locally retained official README and SN-only likelihood receipts were decoded
as text and read; the downloaded code was NOT executed.

## Verified mathematical and data conventions

The mask zHD>0.01, standardized m_b_corr, full STAT+SYS covariance submatrix
in identical original row order, and separate zHEL luminosity endpoint agree
with the retained official implementation. Repeated light-curve rows are
preserved. There is no Cepheid-distance substitution, MU_SH0ES calibration,
diagonal-error fitting, extra peculiar-velocity variance or residual clipping.

For C=L L^T, forward substitution correctly computes L^-1 residuals. The
precision-one vector is L^-T L^-1 1. The profiled magnitude offset

    Mcal=(1^T C^-1 [m_obs-q])/(1^T C^-1 1)

has the correct sign, unrestricted domain, derivative and positive curvature.
The projection-score identity uses its cancellation-aware comparison scale;
the primary score is the stable squared norm of the whitened final residual.
Full-covariance SPD/reconstruction and solve controls retain off-diagonal
terms without regularization. The covariance determinant is common, not a
hidden fitted term. The reported absolute-M dictionary consistently uses
Hcal, while H(0)/Hcal is separately reported after ordinary radiation is added.

The action-endpoint map has d ln A/dt=lambda/3 and bracket
2 ln A<=t<=3 ln A. The safeguarded Newton derivative and scalar-bisection
crosscheck agree. Unique-redshift integration is restored to every original
row before scoring. Independent interval8/16, angle64/128, whole-interval
Gauss64 and Simpson512 checks are declared before outcomes. Constant-H and
pure-dust endpoint controls use the correct exact distances and preserve the
distinct zHD/zHEL convention.

## Census, numerical scope and interpretation

All67 inverse points times5 backgrounds are retained. Four soft copies are
verified to share the homogeneous history but keep all1,340 original labels;
their galaxy response is not asserted equal. Infinite-gap dust and unsupported
states retain explicit labels. One offset is profiled per conditional history;
no matter fraction, gap, state, baryon density, covariance or H0 is refitted.
The same-background dust comparator receives the same covariance and freedom.

The fixed numerical tolerances are method controls, not desired physical
outcomes. Complete residual and whitened-residual arrays are losslessly
transported, rather than rounded or trimmed. Benchmark and per-background
runs are explicitly incomplete subsets until the whole census is collected.
No best-state selection, tail-probability declaration or new observational
threshold is inserted. Inherited Pantheon exposure is acknowledged; this is
not an independent blind validation or a joint BBN+BAO+SN likelihood.

No load-bearing defect or required correction was found. This is a preflight
acceptance of the specified computation, not an assertion of a numerical or
observational result before root's frozen execution.
