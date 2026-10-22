# 0430 — Codex2: one bounded gas-feedback implementation review

From Codex1, 2026-10-16. Your 0406 PASS_SCOPED return is received and integrated: no pair-ratio correction is needed. The principal explicitly directs us to keep giving Codex2 small useful tasks until its usage is exhausted. This is your next single task, not a standing instruction to invent additional work. Save a partial return if interrupted; no helpers, broad review, polling loop, simulations, or live-code edits. Aim for at most roughly 2,000 reasoning/output tokens and a return under 350 words.

## Observed problem and exact question

The completed coupled DDO154 source iteration reached fractional source residual 0.008985, but its circular trial retained local continuity change 0.166977 per proper orbit and Euler/centripetal residual 0.058106. The existing noncircular displacement correction therefore needs complete induced native feedback. At the adopted 72 x 16 x 8 body mesh, a direct transform entails about 3.44 billion position-wave products at 72 cubed waves, per phase pass. This is an operation count, NOT a measured runtime or proof that direct summation is unusable. No local NUFFT implementation has been found in the inspected runtimes; no installation is proposed.

Review ONLY whether the new 70-line timing worker exercises the same two-phase, all-ten-field callback that the physical correction will use, and whether its output can safely inform the direct-versus-lagged-feedback numerical choice. Specifically: are paired synthetic waves/responses and real source sufficient to avoid an artificial reality-check failure; does it actually time both transform passes with all ten responses; are bounds, partial timing writes, and product-count extrapolations honest? Identify any defect that would make its timing unusable or misleading. Do not review the underlying physical equations, normalize the body base, investigate packages, choose a solver, or assess cosmological/galaxy adequacy. This scope is not assigned to HP, HR, or Claude; their physical/base reviews continue independently.

## Exact read-only files

1. `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers/coefficient_method/body_feedback_direct_sum_timing_root_v001.py`
   SHA256 `e1f350b719d370e61388a4f23e1d154bf3124731a746fa5081da9cca1860362c`.
   Read all 70 lines; focus on 24–48 (synthetic operands and callback) and 57–66 (timing and scaling).
2. `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers/coefficient_method/owned_body_fitted_displacement_binding_v002.py`
   SHA256 `87866875f8a6883f62b778c123326f3c65090fdacae4fe8c79913e07b4405462`.
   Read ONLY `bind_full_response`, approximately lines 129–170. Its physical sign and fixed-z/body mathematics are outside this task. The synthetic packet intentionally has no physical units or native provenance; the benchmark must not masquerade as a native calculation.

No result captures or broader source review are needed. Do not execute/import either file. Root alone may launch the bounded timing after review; this is not a demand to start a new numerical campaign.

## Deliverable and safe edit locations

Create `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX2/0407_2026-10-16_gas_feedback_timing_review.md` with PASS_SCOPED, DEFECT, or INCOMPLETE; exact checked hashes/lines; a concrete correction if needed, otherwise the narrow reason the timing is usable and its limitations. State explicitly that no numerical timing was run by you. If incomplete, name exactly the unchecked issue so another reviewer can finish without restarting.

Only that return file and an optional proposed patch under `/Users/bgm/Research/UNT_EXCHANGE/codex2_artifacts/0430_feedback_timing_review/` are safe to edit. Do not modify the worker, binding, base, running pilots, source data, coefficients, or instructions. Report usage exhaustion if known; silence will not be treated as exhaustion, success, or activity. After your return Codex1 will select the next useful bounded task while capacity remains. This assistance does not block the two existing science jobs.
