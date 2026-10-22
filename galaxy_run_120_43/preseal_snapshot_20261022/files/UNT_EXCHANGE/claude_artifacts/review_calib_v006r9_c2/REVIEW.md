# REVIEW: Codex2 v006r9 (0557 / FROM_CODEX2 0439), Claude2-lane delta review, own fixtures

**VERDICT: PASS_WITH_FINDINGS.** 0 BLOCKING, 0 SHOULD_FIX, 3 NOTE. V8-F1 is closed.
TESTED: 140/140 of my own probes behave as 0557 requires. Synthetic fixtures only. No launch. The r5 driver was loaded only for `normalize_spec`. The audit hook recorded zero blocked attempts.

## Object

| File | sha256 (from bytes) |
|---|---|
| wrapper `v006r9/calibration_orchestrator_cx2v006r9.py` | 24abe3bc… |
| core `v006r9/calibration_core_cx2v006r9.py` | a595c5c0… |
| sensitivity `v006r8/sensitivity_policy_cx2v006r8_v002.py` (reused) | 8fb06600… |
| config `v006r9/RUN_CONFIG_DDO154_CX2V006R9_P128_MS128.json` | 721c7230… |
| `v006r8/REGISTERED_ANCHOR_CX2V006R8.json` | 7693959c… |

Each matches the 0439 packet. The following manifests verify from bytes:
- r9 `HASHES_FINAL_CX2V006R9.txt` (272/272);
- r9 independent `HASHES_CX2V001.txt` (133/133);
- r8 `HASHES.txt` (25/25) and `HASHES_FINAL_CX2V006R8.txt` (90/90).

Every file in the r9 directory is listed in its manifest. No r8 file was modified after the r9 build started.

## (1) Deciding-row numerics bound to config.numerics.block: PASS (TESTED)

The mechanism, in core L105–148:
- `deciding_numerics_identity` deep-copies the block, then pops exactly `uv_tail.eps_certificate` and `uv_tail.lo_certificate`.
- `check_deciding` compares `canonical()` bytes of each row's raw spec numerics with the bound config block. It does this for both rows. The check runs after `validate_block` and before the reanchor, result, receipt and normalizer checks.
- `Context.__init__` and `fresh_gates` bind a copy of `cfg.numerics.block` in a second ContextVar, and reset it in `finally`.

**Positive controls.**
- P1–P3: the exact config numerics on both rows pass, in either row order, and also with the block supplied as a JSON round-trip copy.
- P4–P6: a certificate-only change gives identical identity bytes and does not mutate its input. The gate does not refuse it on the binding. With pins to my own fixture files, the gate passes (see N-1).

**Every case was tested three ways.**
- **ra:** the reanchor deviates and `config.anchor` is rebound to it, so only the binding can catch it.
- **w8:** the workers_8 row deviates and the reanchor is exact.
- **rev:** both rows are exact and the config block deviates, which isolates the binding from `validate_block`.

**The prior O2 probes now refuse.** picard.passes 2, route_a.max_iterations 8 and uv_tail.quadrature.order 4 each refuse ra, w8 and rev with `DECIDING_NUMERICS_NOT_CONFIG_BLOCK`. Replayed through the r8 core, the same evidence passes, which reproduces V8-F1.

**I added 31 new deviations (D01–D31).** All refuse ra, w8 and rev:
- **Gas and outer box:** uv_tail.gas.M_s 64 (D01) and K_big 64.0 (D02).
- **Workers:** top-level block.column_workers 2→1 and 2→4 (D03, D04), and route_a.column_workers 8→4 (D05).
- **Brackets:**
  - rfs_factors, le_first_factors and le_next_factors (D06–D08);
  - removing the column-71 rfs override (D09);
  - one column's A32 hull edge +0.5 (D10);
  - brackets.mode (D11).
- **Picard:** the picard bound speed_change_bound_km_s 0.01→0.1 (D12), observe_every_pass (D13), and removing the bound (D29).
- **Route A:** max_iterations 32→64 (D14). An increase also refuses, because the check is equality, not a floor.
- **Quadrature:** w_perp and w_z maxima (D15, D16).
- **Composite grid:** panel_orders, an interior break, and the scope string (D17–D19).
- **Tail settings:** jet_order, domain z_src, the stars tail_rule, and the asymptote (D20–D23).
- **Number representation:** K_big 128.0→128 (D24; `validate_block`'s `==` lets it through), picard.passes 6→6.0 (D25), and lambda_scale 1.0→1 (D26).
- **Extra keys:** numerics.c2r9_extra (D27), picard.max_passes (D28), and a certificate slot moved to the top level of numerics (D30).
- **Compound:** a certificate-only change plus picard.passes 5. The exclusion does not mask the real change (D31).

**Which check refuses.**
- **B1:** every deviation outside `validate_block`'s coverage refuses on `DECIDING_NUMERICS_NOT_CONFIG_BLOCK` itself, on both rows, not incidentally.
- `validate_block` catches D01, D02, D05 and D10 first. Each of those still refuses on the binding in the rev direction.
- **Counterfactual:** the r8 core accepted 40 of the 68 deviated-row cases, including all of O2, D03/04, D06–09, D12/13, D15/16, D19–21, D24, D26, D29 and D31. The r9 core refuses all 68.

**Certificate keys and fail-closed cases.**
- K1 and K2: if both certificate keys, or only eps, are absent, the identity exclusion does not admit the spec. The actual driver's normalization refuses it (strict uv_tail keys).
- U1–U4: a direct call with no numerics context or argument fails closed with `DECIDING_CONFIG_NUMERICS_BLOCK_REQUIRED`. So do the malformed blocks `{}`, `{'uv_tail':'x'}` and `[]`.

**Actual `Context` behaviour.**
- X1: exact rows pass.
- X2 and X3: a reduced-numerics reanchor refuses at construction and at the inherited `fresh_gates`.
- X5: exact rows under a changed config block refuse (cross-config).
- X6: refreshing contexts A, then C, then A shows no leak between them.
- X7: if a running context's config block is mutated to picard 2, `fresh_gates` refuses deciding on the binding, and numerics_verdict flags the changed block.
- X8: an exception inside the inherited init restores both ContextVars.
- X9: a block without uv_tail refuses before binding.

## (2) Nothing else changed vs v006r8: PASS (TESTED, `DIFF_R8_R9_*.json`)

**Sources.**
- **Wrapper (6 lines):** the core pin; the sensitivity load path moved to `../v006r8`, with the same sha; one message.
- **Core (36 lines):** the identity function, the ContextVar, the comparison, and the two binding blocks. No other line differs.
- The static-dry script changes only its labels and paths.

**Config.**
- These four paths change:
  - `notes`;
  - the new `tail_readiness.deciding_numerics_rule`;
  - `work_dir`;
  - `work_dir_identity.resolved` (both renamed R8→R9).
- `numerics` is canonically identical to r8, and so is `anchor`.

## (3) r8 protections still hold: PASS (TESTED, spot-check of 14)

These all still refuse or hold:
- Q1, r8 N1: the log/exp seed coordinate.
- Q2, r8 N3: D = 4.04 + 1 ulp.
- Q3, r8 C2: a byte-identical coefficient copy at another path.
- Q4, r8 S1: a second exact-point fresh run.
- Q5, r8 S2: the workers_8 run relabelled as the reanchor.
- Q6, r8 W4: swapped receipts with the anchor made consistent.
- Q7, r8 T2: a registered_point path alias.
- Q8, r8 W12: the shipped pending anchor.
- Q9, r8 X4: a tampered `config.anchor` at `Context` construction.
- Q10: the review allowlist is still an empty frozenset.
- Q11: `compute_pair` still refuses on A68.
- Q12: the sensitivity module is the r8 file at 8fb06600, and A68 is false.
- Q13: the headline D = 4.04 is still ungated.
- Q14: both ContextVars are None after all the work.

## Findings

- **N-1, NOTE: certificate slots in the deciding rows are unconstrained by `check_deciding`.** This is TESTED:
  - P6: pins to two arbitrary JSON files of my own pass the full gate.
  - K3: the `NONE_TEST_ONLY` sentinel on both rows passes too, given a forged COMPLETED result.

  This is what 0557's exclusion says. From the driver source, run mode refuses the PENDING sentinel, and it refuses TEST_ONLY when any stage domain is non-empty. Neither driver refusal was run here (UNTESTED). Certificate admission remains the open `POINT_CERTIFICATE_SCIENTIFIC_APPROVAL_PENDING` blocker. Once a certificate registry exists, the deciding rows' certificate pins could be bound to it.
- **N-2, NOTE: the binding follows the current config.** X4: a config block with picard bound 0.1 plus matching rows passes the deciding gate. numerics_verdict stays not ok on `V007_SEALED_ADOPT_TAIL_PENDING`. So the guard against a reduced config block itself is the V007 ADOPT / block_source gate, which is pending and was not exercised here. This is by design.
- **N-3, NOTE: two cosmetic leftovers.**
  - The config key `tail_readiness.deciding_numerics_rule` is declarative only; no code reads it.
  - The wrapper docstring still reads "v006 r8 (0554)".

**UNTESTED:**
- actual TAIL_REANCHOR and deciding runs;
- the driver's run-mode certificate refusals;
- the V007 ADOPT gate;
- scientific certificates;
- the comparator successor;
- Codex2's 34, 41 and 131 controls (not re-run).

## Artifacts

- `tools/common_c2r9.py`, `tools/test_r9_c2.py` and `tools/diff_r8_r9_c2.py`.
- `run_20261018T153113Z_23770/RESULTS.json` (140/140, including deviation classes and the r8 counterfactual).
- `DIFF_R8_R9_20261018T153203Z.json`.
- `HASHES.txt`.
