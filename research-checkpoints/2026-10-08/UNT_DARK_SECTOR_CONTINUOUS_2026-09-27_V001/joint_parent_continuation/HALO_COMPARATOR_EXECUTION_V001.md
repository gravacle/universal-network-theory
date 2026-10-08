# Prospective execution details for the same-source halo comparison

2026-09-29. Supplements HALO_COMPARATOR_PROPOSAL_V001.md before any new
observational fit. It changes neither the nine-source census nor its scoring.

The NumPy-only helper and wrapper are frozen with the proposal, this note,
the original fine-grid cases, their numerical receipts and source freezes.
The wrapper verifies canonical payloads and the actual files named in the
current input freezes before using the saved arrays. It does not execute
historical solvers, refit baryonic sources, or change their fields.

First run synthetic/numerical controls: compare both analytic mass profiles
with positive 128-node Gauss–Legendre integrals at x=1e-6,.05,.125,1,10;
test the logarithmic derivative by symmetric differences; verify normalized
exact limiting shapes and normalization at the pivot; check the zero-amplitude
boundary and recover two exact synthetic velocity profiles. Use relative
mass-profile tolerance 2e-11, derivative tolerance 2e-8, synthetic amplitude
and scale tolerance 1e-4 relative/absolute respectively, and synthetic SSE
below 1e-8. The synthetic profile uses 129 scale samples plus the declared
refinement and exact limits. These are numerical correctness criteria, not
observational acceptance thresholds.

Only after those controls pass, execute the 72 predeclared fits. Each of the
nine source variants has a separate result file containing eight fits. The
source's all-radius median is the fixed pivot for both fitting masks. Each
fit runs both 257 and 513 sample grids; their minimum objectives must agree
within 1e-6*max(1,J_fine). Selected amplitude-gradient checks use absolute
1e-8; score and curve reconstruction use 1e-8*max(1,abs(value)). These check
numerics only. There is no required improvement over the unchanged network
curve. A fit must not worsen its own zero-halo Newtonian control.

All observed rows, errors, baryonic squared speeds, network speeds and the
complete fitted halo/total speeds and signed residuals are retained, including
rows outside an optimized subset. Both equal-weight and quoted-error scores
are reported for all radii and R>=2; NGC3198 R>=8 is also summarized. Complete
candidate-minimum and boundary parameters are retained. Intermediate grid
arrays are summarized by their deterministic digest, census and extrema;
their full regeneration is specified by the frozen source and inputs. This
is not omission of a fitted outcome or a new choice of source convention.

One worker runs at a time with numerical threads fixed to one. Each completed
source is saved before the next begins. These small, independent saved-array
fits need no custom trajectory checkpoints; a interrupted source can rerun.
The workers print JSON and never write files themselves. Root saves their
unaltered stdout additively and independently reviews the final comparisons.
No observational likelihood ratio, evidence ratio or claim of Stage 2/3
completion is inferred from these descriptive comparisons.
