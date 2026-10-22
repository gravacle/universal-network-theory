# 0429 — Codex2: one independent sampler-ratio review

From Codex1 to Codex2, explicitly requested by the principal on 2026-10-16. This is a small, interruptible review for your remaining approximately 2% weekly usage. It is not a transfer of coordination or numerical-launch ownership. Do not do general UNT background review, spawn helpers, plan a campaign, or launch numerical sampling. One focused pass; aim for at most roughly 3,000 reasoning/output tokens and a return of at most 500 words. Stop after a definite finding. If usage runs low, save a partial finding immediately; silence is not a pass. Do not wait or poll after returning.

## Observed failure and why this check matters

The completed energy/time sampler obtained 512 measurements in each of two chains, but response mixing failed: record-coordinate R1 R-hat=2.01823; S11 descriptive effective sample sizes=4.43/4.92. Saved family counts changed 24/25 times for h, 240/241 for epsilon, and 4/7 for kappa; t and g were absent. These are measured activity counts, not proof of underproposal or a proof of physical rarity. A fixed-family proposal is now being tested with the same Hamiltonian and physical anchor. This review asks only whether its acceptance ratio preserves the intended measure. It does not ask you to establish mixing or to duplicate the running pilot.

## Exact question — deletion reciprocity only

For the V006 family-stratified pair kernel, is `_pair_delete` exactly reciprocal to `_pair_insert`, including the forward-family selection probability and the different event counts before/after deletion? Check specifically whether `r_x = r_f / 0.2` and the outer negation of the sum containing `log(k-1) - log(neligible)` give the correct deletion ratio, with r_f evaluated in the merged source dwell. Also check that an empty selected insertion family is a self-loop rather than resampled. Do not broaden into other kernels, numerical stability of time sampling, ergodicity or performance.

Proposal facts to verify against the small code slice:
- Fixed positive alpha_f=0.2 for the five disjoint families h,t,g,kappa,epsilon.
- Within a chosen family, q_a=alpha_f W_a/r_f(x); the actual reverse is unique, q_b=1.
- Insertion chooses uniformly among K+1 dwells of the pre-insertion K-event path.
- Deletion chooses uniformly among all N_elig eligible adjacent inverse pairs of its current path.
- Ordered excursion times have density exp[-(D_y-D_x)(t2-t1)]/Z(D_y-D_x,ell). The inherited log-Z routine is already reviewed; take its evaluated log Z as supplied.
- The expected insertion factor, if these facts are confirmed, is (p_D/p_I)*(K+1)/N_elig(X') * W_a W_b Z/(q_a q_b). Derive the deletion expression yourself, distinguishing K from the deletion function's current k. No extra family draw is made on deletion.

## Read only these code locations

1. `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers/coefficient_method/owned_collective_worldline_static_response_pairallk_v006.py`
   SHA256 `896cadbbe4059a77b33f370d643cfa7657c0e031d61d1aa46886e88eb4f576b7`.
   Read family definitions/selection near lines 21–115, insertion log ratio near 135–146, and `_pair_delete` lines 157–277. The file is small; no dependency walk is needed.
2. `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers/coefficient_method/owned_collective_worldline_static_response_pairallk_v004.py`
   SHA256 `7d0798923302bb36763c6b4f6212c944872b2b9c2f50021183d918a19dbd03c9`.
   Read only `_pair_log_ratio`, `_pair_eligible_positions`, `_pair_move`, lines 3316–3373. The old `_pair_log_ratio` docstring still describes uniform times; the executed code uses `_pair_log_Z` and energy cancellation. Judge executed code, and call out any misleading documentation separately from a ratio defect.

The observed-result files are supplied for provenance only; do not parse their large captures:
- `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CODEX1/OWNED_L4_ENERGY_TIME_ANCHOR_RUN_V001/result.json`
- `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CODEX1/ENERGY_TIME_RESPONSE_DIAGNOSTICS_RUN_V001/diagnostics/diagnostics.json`

## Required deliverable and safe edits

Write one short finding to:
`/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX2/0406_2026-10-16_family_pair_deletion_ratio_review.md`

Include:
1. Verdict: PASS_SCOPED, DEFECT, or INCOMPLETE.
2. A 3–6-line independent forward/reverse proposal derivation, with event counts defined.
3. Exact code line(s) confirming the expression or causing the defect.
4. If defective: the smallest correction or a concrete algebraic counterexample. If incomplete: exactly what was checked and what remains unchecked. No generic recommendations.

Safe to create/edit: the return file above and, only if needed, a proposed patch file under `/Users/bgm/Research/UNT_EXCHANGE/codex2_artifacts/0429_pair_ratio_review/`.
Do not modify any live sampler, recipe, monitor, result, source coefficient, or instruction file. The V006 pilot is already running; a defect should be reported promptly for Codex1 to assess, never hot-patched by this review. No simulations, duplicate pilot, empirical mixing test, or mandatory numerical fixture is requested. A short hand-worked marked-path counterexample is enough if relevant.

This extra independent review is not a new approval gate. Existing distinctly reviewed work continues. A partial return or account exhaustion does not invalidate completed artifacts and does not require a restart of the review.
