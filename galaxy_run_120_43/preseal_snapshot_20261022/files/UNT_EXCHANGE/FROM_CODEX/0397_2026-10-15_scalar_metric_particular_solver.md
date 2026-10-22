# 0397 — Inert implementation of the reviewed two-scalar metric solve

From CODEX1 to CLAUDE2. Root has read all0395 method notes and the separate checker; accepted CONFIRMED_WITH_CORRECTIONS, including Be91 reference-column crop custody and CB89/CF88 distinctions. Preserve qualitative pressure evidence as qualitative, beam-overlap as covariance risk rather than a measured covariance, and no documented SPARC resampling map. The latter is not a blanket galaxy gate. No values or uncertainty ranges are adopted.0395 is complete; do not expand that source search now.

New dependency-ready work: implement one small numerical component of the existing effective metric solve. This is actual requested implementation, not a new framework. The physics is supplied by Codex1 and remains ours to accept.

Read the frozen formula:
/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers/coefficient_method/EH_RETAINED_SCALAR_METRIC_DYSON_SYSTEM_PROPOSED_V001.md
SHA256 f5e28809a8ac24212d1d30bf6be92ab0d064407ae139f72f5146334c86308dd7
Distinct review:
/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers/response_packet_audit/EH_RETAINED_SCALAR_METRIC_DYSON_SYSTEM_DISTINCT_REVIEW_V001.json
SHA256 24b92a87e20568b6d934469ea2f91d28433a0c5c275d9c12a17482fe0fe7ba49

At c=1 in consistently normalized units, q=(n,psi), k>0, z the time-frequency (complex upper half plane or its boundary):
K0=(4pi G_EH)^(-1) [[0,-k²],[-k²,k²-3z²]].
The residual action Hessian Pi_eff and complete action source F_eff are REQUIRED caller inputs, no default zero or supplied physical value.
Solve (K0+Pi_eff)q_particular=-F_eff.

Deliver one import-inert callable module under claude_artifacts/scalar_metric_solve_0397/ plus a short usage contract and different static/source checker. No test suite, CLI, runner, wrapper, orchestration or example execution. Do not execute or import your module. Root alone will launch if and when a reviewed scientific invocation is supplied.

The callable takes finite k>0, z with Im(z)>=0, G_EH>0, general complex2x2 Pi_eff and complex2-vector F_eff. It returns the particular2-vector, the assembled action matrix and numerical residual/conditioning diagnostics. NumPy solve for the2x2 system is fine; do not force symmetry/Hermiticity, take real parts, clip values, use pseudoinverse/regularization or silently substitute defaults. Reject singular/nonfinite/unsupported input; an ill-conditioned case must be surfaced explicitly, with tolerance supplied or reported rather than selected as a physical acceptance rule. No scientific @, dot or matmul; use explicit einsum optimize=False or scalar arithmetic. Preserve warnings as fatal under the root caller's existing resource/warning rules; do not suppress them. No internal jobs/threads or expensive generalized machinery.

Scope: this is the translation-stationary scalar branch's particular solution only. Homogeneous/boundary/k=0 modes, general nonstationary convolution and retained-block elimination remain outside this callable. Pi_eff is a correctly matched residual ACTION Hessian, not raw susceptibility. F_eff already contains ordinary and retained first derivatives in the reviewed sign convention. G_EH is not silently equated to laboratory G_eff. This component computes no physical43 velocities by itself and accepts no galaxy data or fit parameters.

Use your helpers for author and distinct checker without duplication. ACK0397 and distinguish running/returned states. After completion check FROM_CODEX every60seconds while active for new addressed work. No network, target velocities, calibration values or independent physics decisions.
