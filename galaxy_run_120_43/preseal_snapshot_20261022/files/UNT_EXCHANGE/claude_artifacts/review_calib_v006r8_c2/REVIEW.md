# REVIEW: Codex2 v006r8 (0554 / FROM_CODEX2 0435), Claude2-lane delta review, own fixtures

**VERDICT: PASS_WITH_FINDINGS.** 0 BLOCKING, 1 SHOULD_FIX (pre-existing in r7, not a regression), 3 NOTE.
TESTED: 76/76 of my own probes behave as 0554 requires. Synthetic fixtures only. No launch. The r5 driver was loaded only for `normalize_spec`. The audit hook recorded zero blocked attempts.

## Object

| File | sha256 (from bytes) |
|---|---|
| wrapper `calibration_orchestrator_cx2v006r8_v004.py` | 1ddbe6da… |
| core `calibration_core_cx2v006r8_v003.py` | 603ab460… |
| sensitivity `sensitivity_policy_cx2v006r8_v002.py` | 8fb06600… |
| config `RUN_CONFIG_DDO154_CX2V006R8_P128_MS128.json` | 4d2d19a2… |
| `REGISTERED_ANCHOR_CX2V006R8.json` | 7693959c… |
| anchor template `CALL_A2_ANCHOR_F10_C2V001.json` | a93c95b9… |
| coefficients `CANDIDATE_4CHAIN_POOLED_GRID_V001.npz` | 2e3a36d8… |

The manifests verify from bytes: `HASHES.txt` (25/25), `HASHES_FINAL_CX2V006R8.txt` (90/90), and the r7 operations and sensitivity manifests (15/15 and 24/24). No r7 artifact changed.

## (1) Re-anchor bound to the registered A2F10 anchor: PASS (TESTED)

`check_deciding` (core L135–143) requires two things of the `reanchor` row:
- its spec `physical` and `coefficients` equal the registered objects exactly;
- its result, receipt and spec sha equal `config.anchor`.

`registered_anchor()` (L83–102) re-derives the registration from bytes every time it runs:
- the template is checked against the registration;
- the coordinate file's `trial_point.anchor_spec` is checked against the template;
- `config.anchor` is checked for registered_point, physical, coefficients and driver, with `use` false.

In every near-miss below, `config.anchor` was rebound to the bad run, so only the registration could catch it. Each one refuses:
- **Seed coordinate.** The log/exp engine-seed θ refuses (N1). It differs at about 1e-15 in s, ell_F and gamma.
- **Distance.** D = 4.0400001 and 4.04 ± 1 ulp refuse (N2–N4).
- **Physical fields.** A one-ulp change in each of the six physical fields refuses (N5.0–N5.5). The driver also refuses any inclination other than 66.
- **Extra key.** An extra physical key refuses (N6).
- **Coefficients.** All of these refuse (C1–C4):
  - a real distinct coefficient file (sha d270a8e8);
  - a byte-identical copy at another path;
  - a `/./` path alias;
  - the right path with a wrong sha.
- **Other D = 4.04 workers-8 runs.** These refuse with REANCHOR_ROW_CONFIG_ANCHOR_PIN_MISMATCH:
  - a second fresh run at the exact registered point (S1);
  - the workers_8 run relabelled as the reanchor (S2);
  - a substitute row inside an actual `Context` (X3).
- **Other headline θ.** Another headline θ refuses on registration even when the config is rebound to it (S3).
- **Duplicates.** Duplicate reanchor rows refuse (S4), and so does the same run in both rows (S5).
- **Swapped or rebound pins.** All of these refuse (W1–W12):
  - each `config.anchor` field swapped to the workers_8 run;
  - receipts swapped between rows, with the config consistent with the swap (the receipt's spec pin differs) or unchanged;
  - results swapped;
  - a byte copy of the result at another path;
  - a row `spec_sha256` that differs from its pin;
  - each pending null field;
  - the shipped config.
- **Registration tampering.** All of these refuse (T1–T10):
  - registered_point sha;
  - a path alias;
  - physical 4.0400001 or a one-ulp change;
  - coefficient sha;
  - driver sha;
  - `use` true or missing;
  - physical removed;
  - no anchor at all.
- **Context binding.** Actual `Context` construction and the inherited `fresh_gates` bind the instance's anchor (X1, X2). A tampered `config.anchor` refuses at construction (X4). The ContextVar is restored afterwards (X5).

## (2) Review authorized by file sha, not by name: PASS (TESTED)

- The reviewer-name denylist is removed (R17).
- `registered_review` requires two things:
  - the review pin verifies from bytes;
  - the sha is in `REGISTERED_DISTINCT_REVIEW_SHA256`, which ships as an empty frozenset (R1–R3).
- I registered one review in memory only. Each of these refuses (R5–R9):
  - a one-space reviewer rename with its own correct pin;
  - a rename to "Codex2";
  - a renamed file that claims the registered sha;
  - an extra pin key;
  - a relative path.
- Through the full `sensitivity_gate` at the registered D = 4.1115:
  - a renamed review refuses on its sha, before A68 (R10);
  - a registered review still refuses on A68 (R11);
  - with A68 flipped in memory, a registered review whose `distance_hex` is wrong refuses on DISTINCT_REVIEW_BINDING (R13).
- The headline D = 4.04 stays ungated (R15).
- `compute_pair` refuses on A68 before it reads any plan or run (R16).

## (3) Changes against v006r7: PASS_WITH_NOTE (TESTED, `DIFF_R7_R8_*.json`)

Source changes:
- **Wrapper (8 lines):** the core and sensitivity pins and one message.
- **Core (58 lines):** `registered_anchor`, the ContextVar, the reanchor block, the `Context.__init__` and `fresh_gates` binding, and the adoption-policy path moved to `../v006r7` with the same sha.
- **Sensitivity (19 lines):** the review allowlist, the denylist removal, the A68 blocks, and `HERE` moved to `../v006r7` with the same pinned plan and comparator.

Config changes:
- the new `anchor` fields;
- `notes`;
- `tail_readiness.sensitivity_comparator_status`;
- the work_dir moved to an R8 path.

Nothing else changed. See N-3.

## (4) config.anchor is target-free: PASS (TESTED)

- **Keys.** The keys are use, result, receipt, spec_sha256 (all pending or null, with use false), driver_sha256, registered_point, physical and coefficients.
- **Content.**
  - No NGC, target or observed-velocity terms appear.
  - physical equals the registration, which equals the template, as exact objects.
- **Source chain.**
  - The template is DDO154 and contains no NGC key.
  - The coordinate registration declares `ngc3198_access: NONE`.
- All pins verify from bytes (F1–F8).

## Findings

- **V8-F1, SHOULD_FIX** (low urgency; due before TAIL_DECIDING evidence is pinned; pre-existing in r7). The numerics of both deciding rows are checked only by `validate_block`; they are not compared with `config.numerics.block`. TESTED (O2): a reanchor with any one of these changes passes, once `config.anchor` points at it:
  - picard passes 2 instead of 6;
  - route_a max_iterations 8 instead of 32;
  - uv_tail quadrature order 4 instead of 8.

  So the gate accepts a re-anchor at reduced numerics if root pins one. **Fix:** require each row's spec numerics to equal the config block, with eps/lo_certificate excluded as in `point_identity`.
- **N-1, NOTE.** The re-anchor must be launched from the template's physical values. A mapper-built anchor θ (log/exp, about 1e-15 off) refuses (N1). This is the intended behaviour, and the launch must follow it.
- **N-2, NOTE.** Distinctness is now root's act at registration: registered bytes naming "Codex2" are not refused (R14). Registering a review needs a sensitivity-policy successor plus a wrapper re-pin. A config entry alone is not enough. That is stricter than 0554's wording.
- **N-3, NOTE.** 0554 did not request the A68 fail-closed blocks (`compute_pair` and `sensitivity_gate`) or the `sensitivity_comparator_status` key. Both are disclosed in BUILD and 0435, both are restrictive, and both are consistent with the A68 ruling.

**UNTESTED:**
- actual TAIL_REANCHOR and deciding outputs;
- Codex2's 131 parent controls (not re-run);
- scientific certificates;
- the comparator successor.

## Artifacts

- `tools/common_c2r8.py`, `tools/test_r8_c2.py` and `tools/diff_r7_r8_c2.py`.
- `run_20261018T151705Z_90239/RESULTS.json` (76/76).
- `run_20261018T151647Z_88396/`: an aborted first attempt. Its fixture builder crashed on the driver's inclination refusal, so it holds partial fixtures only and no results. It is kept, not deleted.
- `DIFF_R7_R8_*.json`.
- `HASHES.txt`.
