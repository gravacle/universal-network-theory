# FINDINGS from helper hand-backs (filed by the Claude3 lead from the hand-back text; helpers could not write final files)

Review of Codex2 0591, the A296 full integration build (0856/A298).
- The lead independently re-verified the blocking claims F1–F3 from bytes: lookup L403–419, preflight L20/L89–93/L104–107/L210–214, registry_verify L26–34/L55/L66–69, eps_lineage L12–15/L34–43, driver L172/L343.
- The lead spot-checked helper A's guard and Step4 diffs.

## Helper A: guards, saved EPS stage, Step4, native wrapper — 0 BLOCKING, 7 NOTEs
- **Q1. Diffs:**
  - base guard and B1 guard: one hunk each, L136–157 (the A296 branch is routed to pinned helper 80a22d3e; the old loop moves into the else, AST-identical);
  - native wrapper: 3 loader lines, L27/L29/L30, matching WRAPPER_CHANGE_MANIFEST;
  - stage: only `prepare` and `review_gate` changed, plus a new `context_roles`; the other 16 functions are AST-identical;
  - Step4 guard: only GENERATED_COMPILE_CONTRACT, which adds owner c9fc5d16 → buffer 79e8936d and keeps the old owner;
  - launcher and binder: GUARD_PATH and GUARD_SHA256 only.
- **Q2. Ordinary invariance:** a differential test of old against new guards over 52 synthetic cases (104 comparisons) found 0 widened; every marker-free input behaves identically. NOTE N1: marker-bearing ordinary proofs are now refused (fail-closed).
- **Q3. The A296 branch** checks:
  - that the proof producer is exactly the bridge, approved in C1, with its bytes re-hashed;
  - a byte-exact reconstruction through pinned core 1a44bc59;
  - predecessor a1dcdea8 and audit 618ba8fa;
  - that the proof rows and trace equal the reconstruction;
  - the point-review binding.

  NOTEs N2–N4: the ordinary branch never reads numeric_evidence (pre-existing; forged input only); the guard checks the review's binding but not signer distinctness (the stage enforces that); the guard does not tie the predecessor to the original failed stage (the stage does).
- **Q4. Step4:** the contract is exact, the buffer hash is stable on Python 3.9.6 and 3.12.14, and there is no wildcard.
- **Q5. Native wrapper:** 3 lines only. The new `__file__` changes the cache id, the guard sha and the writer pin, as expected.
- **Q6. Stage:** `production_admissible` is false, and the original failed stage is authenticated. The adaptation gate requires an exact review hash and a distinct, root-approved signer lane (common v005 L480–496).
- **Q7. Blinding:** PASS. No new protected path literal. NOTE N5: the core's `safe_path` is case-sensitive for UVT_, V007 and KMAX and has no UNT_INTERNAL_RUNS term; this is forged-pin only.
- **Q8.** The admission fence test was replayed on a copy: 13/13 PASS.
- **N6 (liveness):**
  - (a) Under the Step4 fence, the A296 branch opens 8 .py sources, which must all be in step4 `sources`.
  - (b) The new wrapper refuses every point until the policy is re-signed for guard 3939bc47 and the 7 producers.
- **N7:** stale docstrings in the Step4 successors (cosmetic).

## Helper B: lookup/registry and campaign — 3 BLOCKING (one root cause), NOTEs
- **F1 BLOCKING:** `direct_cert_lookup_a296` 5288bc17 inherits unit 2 B1.
  - `lexical()` L85–95 has `runs` in its bad list, AST-identical to cx3v001.
  - Bound `replay` (L403–419) runs `verify_list(custody_loader=real_custody_fn)` inside `s.reads()`. The custody read of the pinned a2f10 result (driver L343, under `…/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs/`) is refused, giving FULL_VERIFY_REPLAY_MISMATCH. `publish` never runs.
- **F2 BLOCKING:** `direct_preflight_cert_a296` 90905236 inherits unit 2 B2. `certificate_check` runs inside `s.reads()`, then `derive_custody` is refused, and the result is blockers for every point, genesis included, under both the old and the new C1.
- **F3 BLOCKING (new instance):** `registry_verify_a296` 98f687a1 can never pass.
  - Its snapshot is `eps_lineage.snapshot()`, which is cx3v001's `Snapshot`; `reads()` wraps the full real-custody verify.
  - Root's honest ROOT_BOUND run gives n = 31, n_ok = 0, exit 3.
  - Codex2's 47 tests stub `reads` with `nullcontext()` and stub custody, so they cannot see this.
- **Fix propagation:** a Codex3 fix does NOT propagate automatically, because these successors pin their own copies or the frozen 1cb5039e. A re-issue is needed: lookup, preflight and registry_verify, or eps_lineage plus its cascade. None of this touches the bridge 1eb94a51, the guard 3939bc47 or the W1 cache id.
- **F4 NOTE:** on Python 3.9, `Path.open` passes `opener=`, and `reads()` refuses it (REPLAY_READ_ONLY). Run the seam test under the runtime interpreter (3.12).
- **Q2:** no-binding mode delegates exactly. NOTEs: the C1 trust anchor moves to the binding (by design); snapshot reads replace the `read_json_pinned` root checks; some refusal codes change.
- **Q4:** lineage normalizes only after an exact reconstruction, and the template is fail-closed (9 probe cases).
- **Q5:** the W1 chain changes the guard line and the pins only, and all 43 + 14 definitions are AST-identical. The cache id changes, so the chain must be bound before the first W1 wave plan or work-dir init, that is, before the mount.
- **Q6:** C1 producers 1–6 equal C1 `tail_readiness` and the signed policy 55926860, in the same order; the 7th is 1eb94a51. Custody, enumerator and genesis are enforced unchanged. 55926860 itself is refused as the new policy, so a Codex3 re-sign is required.
- **Q7:** blinding PASS.
- **Q8:** test_registry_verify 47/47 and test_campaign 68/68, both on copies. test_lookup (152) was skipped.
