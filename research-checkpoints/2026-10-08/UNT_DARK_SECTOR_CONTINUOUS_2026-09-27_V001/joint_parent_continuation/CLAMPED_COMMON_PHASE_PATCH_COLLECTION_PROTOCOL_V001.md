# Clamped patch collection: prospective saved-data protocol

2026-09-29. Inert collector only; no producer/material import, nonlinear solve,
orbit quadrature or scientific outcome inspection during authoring. Original
driver, material and freeze remain untouched. No new pass threshold or fitted
choice is introduced by this comparison.

## Complete and partial census

Default inputs are `CLAMPED_COMMON_PHASE_PATCH_V001_CASE_000.json` through
`_007.json`, each containing the raw producer stdout transport. Alternatively
the root supplies exactly eight ordered paths. Expected labels are the fixed
Cartesian product R=[128,8192], L=[1,2], N=[16,32], N varying fastest.
Each present case must authenticate its exact compressed/raw/payload hashes,
the shared producer freeze, full case configuration, label and seed census.

A missing case is explicitly MISSING. A prerequisite failure retains both
unstarted seeds; it is not fabricated into two numerical attempts. A completed
case must retain seed multipliers1 and2. Authentication/shape inconsistencies
are errors, never ignored rows. The collector freeze binds its code/protocol
and complete producer input lineage prospectively. Each invocation's receipt
additionally binds all actual result files then present; no future result hash
is invented in advance.

PARTIAL_CENSUS reports all missing case indices and every affected comparison.
COMPLETE_SAVED_COMPARISON means eight authenticated results are present, not
that they converged or describe a resolved physical solution. Separate flags
require all case controls passed, all16 seeds converged and all16 Jacobians
qualified. Missing/failed cases cannot make these flags true. No aggregate
success replaces the individual outcome/history and qualification fields.

## Comparisons fixed before outcomes

Retain all24 pair records:

- Eight grid pairs: N16 versus N32 at identical R,L and fixed seed.
- Eight clamp pairs: L1 versus L2 at identical R,N and fixed seed.
- Eight seed pairs: seed1 versus seed2 at identical R,L,N.

Differences are always second minus first. Fields are u and physical Phi,
radial and vertical gradients in dimensionless G and m/s², hard action I and
I/I_b, complete hard/soft delta(E+3Pi), total reaction and hard absolute energy
and pressure. Failed-but-retained iterates may be compared descriptively, with
their nonconverged status visible. Missing material fields are listed, not
silently reconstructed or substituted.

The first case's saved centres provide target points. Keep only the geometry-
defined centre rectangle covered by both source meshes. In particular the
larger-clamp grid may not cover the first small-box centre, so that edge strip
is explicitly omitted from interpolation, with retained indices and excluded
point count saved. This is fixed geometric support, not an outcome selection.
Use bilinear interpolation in the saved physical dimensionless x,z coordinates;
never extrapolate. Grid pairs use the coarse target grid. Seed pairs share a
mesh and are therefore direct at the centres.

Metrics are maximum absolute and signed differences, volume-weighted RMS
difference, symmetric relative RMS (dividing by the mean of the two RMS field
norms), and both fields' ranges/norms. Weights are the retained first-grid
annular cell volumes; this is a descriptive shared-point comparison, not a
conservative remap or a new global flux qualification. Exact zero norms yield
zero relative difference only when both fields are identically zero.

No grid-difference tolerance is imposed after viewing results. These metrics
and the saved cell-width/local-length ranges inform whether a further resolved
calculation is needed; the collector itself always sets
`numerical_resolution_certified=false`. Changed-L results compare different
externally clamped patches, not isolated-domain convergence or a selected
halo radius. Agreement of two seeds is not a uniqueness theorem.

## Execution and resource/progress boundaries

`freeze` emits the prospective collector snapshot; `run` verifies it and emits
one saved-comparison wrapper with its payload hash. Stdout only, bytecode
disabled, no output-file writes or subprocesses. Root publishes with
apply_patch. Loading/interpolating saved fields does not invoke the physical
producer or a new orbit calculation.

The already-running V001 physical producer retains its iteration history in
memory and only publishes it at completion; no durable intermediate recovery
is asserted. Preserve the existing root execution session and its eventual
exact stdout. Do not modify/instrument the frozen process or add a checkpoint
system for a small rerunnable job. If measured runtimes warrant visible
progress in subsequent cases, use a separately versioned additive reporting
wrapper/driver with flushed seed/iteration events and unchanged mathematics;
that would be a future change, not an alteration of V001 evidence.
