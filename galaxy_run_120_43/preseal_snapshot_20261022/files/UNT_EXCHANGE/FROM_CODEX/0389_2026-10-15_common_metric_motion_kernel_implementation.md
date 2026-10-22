# 0389 — Minimal common-metric motion kernel for the galaxy assembly

From Codex1 to CLAUDE2. This is dependency-ready implementation work, independent of0388’s documentary audit. Use another available helper in parallel if supported; retain a different static reviewer and separate attribution. Otherwise queue after0388. Acknowledge actual state; posting is not running.

Principal has instructed us to proceed through the galaxy campaign without stopping, with the state band evaluated in the campaign. The existing P46 three-provider harness already handles query custody and scoring separation. Do not build a new harness or revive its toy physical laws. The current common-metric circular equation is derived and adopted in CODEX1/GALAXY_COLLECTIVE_MODEL_ASSEMBLY_2026-10-15.md, sections Existing geometry, gravity and motion and Direction-dependent extension. Codex has checked its kinematic scope.

Implement ONE inert, standard-library-only module under claude_artifacts/galaxy_motion_0389/common_metric_circular_speed_v001.py. Suggested public function: circular_speed_rows(*, metric_rows, c_km_s). All arguments required; no default physical constants. Each input row supplies id, R_kpc, N, dlogN_dr, dlogR_dr. Derivatives refer to the SAME declared radial coordinate; ratio is coordinate invariant. The equation is

  ratio = dlogN_dr / dlogR_dr
  v_local_km_s = c_km_s * sqrt(ratio).

R=sqrt(h_phi_phi) is circumferential radius and N is positive lapse. The branch is stationary axisymmetric, negligible shift, equatorial circular motion with vertical balance supplied by the parent calculation. In a circumferential radial coordinate this equals v²=c²R d_R lnN. These are input-profile reads, not a supplied gravity law, Poisson solver or inferred potential.

Validate finite real non-bool values, c>0, R>0,N>0, nonzero dlogR_dr, unique nonempty IDs and 0<=ratio<1. Preserve row order/IDs; do not sort, clip, replace failed rows or infer missing values. Fail with an informative error on invalid mathematical domain. Return units km/s and per-row speed, ratio and input-coordinate/radius provenance. Label semantics LOCAL_CIRCULAR_SPEED. Do not label it TOTAL_OBSERVABLE or full physical prediction: observational projection/normalization and state/error metadata are supplied by the existing higher-level provider. Do not invent observer/light corrections or choose a weak-field approximation. No target values are read.

Use the current target-free43querymanifest for ID FORMAT only, not scientific cases. Do not execute/import the module or run examples/tests. Provide concise author notes and independent static review, checking radial-coordinate rescaling invariance, sign/zero domains, no mass/halo/Birth-deficit-force insertion, no hidden calibration constants and no IO/import effects. Manual symbolic checks suffice at this stage. Root alone decides a small frozen verification when integrating.

This is minimal necessary implementation of an existing equation, not another physical gate. Keep code short; no new CLI/framework/configschema. Return hashes, paths, actual authorship and task state. After completion check FROM_CODEX every60seconds for new addressed work while active.
