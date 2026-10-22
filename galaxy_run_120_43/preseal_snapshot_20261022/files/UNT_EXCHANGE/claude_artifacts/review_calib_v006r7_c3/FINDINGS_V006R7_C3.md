# FINDINGS_V006R7_C3: Claude3 delta check of Codex2's orchestrator v006r7 against review_calib_v006r6_c2 F1–F4 (0542 item 2)

## Object

`calib_tail_readiness_cx2/v006r7/HASHES_OPERATIONS_CX2V006R7.txt`: all 15 entries verify from bytes.

| File | sha256 (prefix) |
|---|---|
| wrapper | dfe4bf0e |
| core v002 | c022116d |
| adoption policy | 7c726fa2 |
| sensitivity policy v002 | f0d72561 |
| config | 6b19cd07 |
| BUILD_OPERATIONS | d2b09d7c |

Rulings checked against: 0540 (F1–F4; F3 as specified by root) and review_calib_v006r6_c2/REVIEW.md (2d02874e).

**Method.** Code reading only. Codex2's 18/18 operational controls were not re-run, and Codex2's own final static/dry run and independent review were still pending at BUILD's timestamp.

## Results

**F1: PASS, by code reading** (adoption policy L28–80).
- The seal tuple is now (compare sha, prereg sha, addendum sha, report schema, **verdict report sha**). A hand-written report has a different sha, so it fails V007_SEAL_NOT_IN_REVIEWED_ALLOWLIST.
- The allowlist stays empty.
- The function also checks:
  - ADOPT_TAIL with tests_read and test_mode false;
  - script sha equal to the compare sha;
  - the report schema;
  - the case block bound by the sealed prereg;
  - C4T tail-ON with the driver in drivers_allowed.

**F2: PASS_WITH_FINDINGS, by code reading** (core v002 L80–148). Implemented as 0540 asks:
- exactly two rows, named reanchor and workers_8;
- r5 driver;
- each spec pinned and fresh (admit {}), DDO154, D = 4.04;
- `validate_block` on both the raw and the normalized block;
- exact replay through the r5 normalizer;
- workers 8 read from the normalized spec;
- result COMPLETED and valid, bound to the spec;
- receipt reasons consumed (the A-01 fix);
- adjacent finish record COMPLETED and valid;
- distinct result shas.

`validate_block` enforces:
- continuum tail-ON, kept cube K = 4;
- K_big 128, gas M_s 128;
- λ = 1, lapse-only;
- workers 8, no ro1_workers flag;
- the full A32 hull on all 72 columns.

- **V7-F2a, SHOULD_FIX (low urgency; due before the TAIL_DECIDING_RUNS evidence is pinned).** The reanchor row is not bound to the anchor.
  - Only its *name* is checked. Its physical θ and coefficients are never compared with the calibration's anchor point, and its result is never compared with `config.anchor` once root fills it (today `anchor.use` is false and all fields are null).
  - So any fresh D = 4.04 workers-8 run can serve as the "re-anchor". The two rows differ only by label.
  - **Fix:** require the reanchor row's physical and coefficients to equal the registered anchor θ. Once TAIL_REANCHOR pins the anchor, also require its result to equal `config.anchor.result`.

**F3: PASS, with one NOTE, by code reading** (sensitivity policy v002 L194–230 and the pair plan).
- Headline D = 4.04 is ungated.
- Each alternate D needs its own `per_distance` entry, keyed by the exact float hex, with evidence and a review:
  - the evidence is TESTED and ok, with the pinned pair plan, matching distance, launch owner Claude2, tail_on false and test iii;
  - the comparator report is validated against the pair and the run roots, then **re-computed from the two runs**, and must equal its fresh computation (`compute_pair`);
  - the review is TESTED PASS and bound to the evidence, report, runs, plan and distance.
- The plan's masked keys are elapsed_seconds, ended_unix_ns, pid, started_unix_ns and utc.
- The plan's distances are 4.111497211045223 and 3.98107…
- A PASS unlocks only its own D.
- **V7-F3a, NOTE.** "Distinct reviewer" is a self-attested string checked against the denylist {Codex2, Codex2 build, CX2}; "codex2" or "Codex 2" would pass. This is low risk if root writes the `sensitivity_deciding_iii` registry entry itself. Binding the review file's sha in that root entry would make it explicit.

**F4: PASS, by code reading** (wrapper L296–301).
- `resolve(decision='invalid')` raises ROOT_INVALID_DISABLED_FOR_TAIL_ON at entry, before any lock, cache or resolution write.
- Retry still delegates to the inherited code.
- This is declared in BUILD, and `tail_readiness.root_invalid_resolution` is present in the config.

**Notes N1, N4 and N5** (BUILD; not re-run). CertificateRefusal is mapped to exit 3 at the run boundary, and the loaders execute the hashed bytes. Codex2's final static/dry run was still pending at BUILD's timestamp.

**Verdict:** PASS_WITH_FINDINGS (0 BLOCKING, 1 SHOULD_FIX, 1 NOTE). This is calibration-step work and does not block the V007 seal (0540).
