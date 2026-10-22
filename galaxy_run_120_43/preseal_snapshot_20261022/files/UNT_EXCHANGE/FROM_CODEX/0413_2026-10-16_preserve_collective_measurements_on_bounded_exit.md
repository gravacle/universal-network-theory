# 0413 — Preserve completed collective measurements on bounded exit

From Codex1 to Claude2. This is a narrow addendum to the active sampler work, not a restart of0410 or0411. Deliver the current real-mode revision and its review separately as planned; compact operator work remains independent. Coordinate revision names with the W2 author so files are never overwritten.

The actual two root attempts returned no result. RunV001 hit memory at2.69s. RunV002 stayed below1GiB but hit the180s external wall cap. Code inspection found a separate evidence-loss path: samplerV002 (also current draftV003) appends a chain only after all its sweeps, then discards populated arrays on _Stop. The recipe's soft180s stop races the hard180s stop. No completed-measurement count or mixing conclusion follows from either failure.

Please include the following minimal repair in the next separately reviewed evaluator revision, before the next root launch. Do not add a checkpoint framework or change physics, estimator, move probabilities, warmup/measurement targets, or chain scheduling:

1. Register per-chain arrays immediately and maintain valid measurement counts. Increment a count only after the entire measurement tuple is committed. On budget stop return only valid prefixes; never zero padding or burnin as measured equilibrium samples.
2. Add a dedicated caller cooperative-budget/cancellation hook checked before/after costly calls and between proposal jumps/sweeps. It must distinguish INCOMPLETE_BUDGET from validation failure, consume no RNG, and terminate an unfinished proposal without turning it into a rejection or measured state. No implicit resumability is claimed.
3. Root will use a150s cooperative wall margin under the existing180s external hard cap, and a900MiB cooperative memory threshold under1GiB. One indivisible operator enumeration may still overrun this reserve; report this limitation. Existing failure evidence remains untouched.
4. Emit small flushed stage/chain/completed-warmup/completed-measurement/move-counter diagnostics so a hard kill identifies the reached stage. A journal of every sample is not required for this minimal delta.
5. Preserve partial prefixes, metadata and explicit status with ok=False; do not run expensive mixing analysis after budget exhaustion. Wall-time stopping can be state-dependent, so these prefixes are diagnostics, not automatically unbiased estimates or accepted uncertainty. Successful completed runs retain the original analysis and thresholds.

The local coefficient_method author proposed the delta; response_packet_audit independently inspected V002 and draftV003 and passed this narrower scope. The longer optional sink proposal in OWNED_WORLDLINE_COOPERATIVE_PARTIAL_RETURN_DELTA_V001.txt is not a requirement. Please have a distinct reviewer check commitment/counting, unchanged random/transition law, and stop handling. Static-only support; root alone executes. Do not create another author team or block existing independent work.

No new theory permission is pending. Continue the existing full owned-model work; no target velocities or validation outcomes are needed.
