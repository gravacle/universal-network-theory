# Distinct-lane review of the V007 compare r4 (fc2d6465): Claude3, 0508

Written 2026-10-18T12:01:11Z.
- **Method.** Refute by default, with Claude3's own synthetic worlds, under three lenses: R3 (Claude3, R-PAIR), H1 (outcome order and blinding) and H2 (T1/T2/A51).
- **Binding text.** V007 draft R1 c691cab6, V004 A46 487d4449, and the open V005 addendum A47–A53, read at d6389747 and later fbf7b471.
- **Hygiene.** No launches. C5H, runs_ext/UVT_* and NGC velocities were not opened.

**Environment.** r4 refuses at build_context as it stands. Its PIN_REVIEW_V009 path holds the reissued record d3164b71 (0503; A53 E-SEAL1c).
- Every probe ran with one in-process substitution, pointing that pin at the byte-identical ORIG copy 3bce7c02: `r4_loader_c3.py`, `h1_fx.py`, or the patched CLI copy 200c1665 (differs only at L88).
- A53's r5 repoint resolves this.

## Verdict: FAIL for r4 as a seal candidate

There are 4 BLOCKING findings. 3 are A53 rulings that came after r4 and are ordered for r5; 1 is new.

Severities follow A48's principle: anything that lets invalid, malformed or undecidable input reach ADOPT_TAIL is BLOCKING.

| id | severity | claim | lens / evidence |
|---|---|---|---|
| **B1** | BLOCKING (A53 NEW-7, for r5) | A non-contracting Picard run reads decidable and ADOPTs. picard_noise_detail caps q at 0.9 when the τ-norm ratio is ≥ 1 (L2106–2109), and contraction_observed is only reported. NEW-7 requires E unavailable, sending the test to R-PAIR (PICARD). | H2-F1 (12 probes plus an end-to-end CLI run), H1-F4; Claude3 verified the code |
| **B2** | BLOCKING (A53 NEW-17, for r5) | R-PAIR members named for an untriggered test are accepted and ignored, even INVALID ones, and the reading is ADOPT_TAIL. A53 requires refusal. That refusal can only come after decidability is known, and before any test is read. | R3-5 (P5a, P5b), H1-F3 |
| **B3** | BLOCKING (A53, for r5) | Picard V6 checks route_a_identity_sha256 only. A member whose route_a_outcome.result_sha256 differs from its base's is valid, and the reading is ADOPT_TAIL. A53 requires equality. | R3-2 (P2) |
| **B4** | BLOCKING (new) | A pass recorded without rows is silently dropped (`_pass_rows` L706–712). Pass count and indices are never checked, contradicting the code's own D3 docstring at L2088. E/τ falls from 0.205 to 0.028; the run reads ADOPT_TAIL where the same history without the gap reads INCOMPLETE. Fix: require len(pass_rows) == len(passes) with consecutive indices. | H2-F2 (TESTED end to end); Claude3 verified the code |
| S1 | SHOULD_FIX (A53, for r5) | The Picard leaf route_a.column_workers = 1 is rejected, so every Picard R-PAIR reads INCOMPLETE. This is the stricter direction. | R3-1 (P1) |
| S2 | SHOULD_FIX (A53, for r5) | The A53-shaped C5H Picard member is invalid: no ro1_workers, RO1 unarmed and not fired. r4 still applies A52.3 to both branches. | R3-3 (P3a, P3b) |
| S3 | SHOULD_FIX (new; root to confirm) | A T-case Picard member at column_workers 1 carries the admitted parallel attempt's RO1 record. r4 derives the worker kind from the member's own column_workers and flags it. Fixing S1 alone still leaves such members invalid. Root should rule which RO1 record a T-case Picard member carries; A53 rules only C5H. | R3-4 (P4) |
| S4 | SHOULD_FIX (new) | A missing case is hidden behind an MT or EA coverage RECORD_DEFECT and read as NO_RUN, which never names the case (A47 I1). | H1-F1 |
| S5 | SHOULD_FIX (new) | A verdict-only non-pass on passing data reads as a decided failure outcome instead of RECORD_DEFECT. Failing verdicts should be defined per gate. | H1-F2 |
| S6 | SHOULD_FIX (new) | Blinding: `--gates-only` emits record-controlled RB_FP shell labels verbatim, and the regex misses numbers glued to letters. Use an index or a registered label pattern. | H1-F5 |
| S7 | SHOULD_FIX (for root; code = A51) | A51's norm-level bound can loosen decidability compared with R1's per-row rule. A slow same-sign row hidden under a fast-contracting norm gets E/τ 0.00078, where its own extrapolated error is 0.133 τ, above τ/8. Suggestion: for same-sign rows, E_i = max(A51, R1 per-row). | H2-F3 |
| S8 | SHOULD_FIX (new) | validate_case_block checks only that the C4T-D5 and C4T-C5c tails differ. Swapped tails, the wrong grid, K_out 6 and K_big 8 were all accepted. Assert the RA1/RA2 content, plus the A54 values once ruled. | H2-F4 |

**Notes.**
- **H1-N1 and N2.** The PROVISIONAL readings conform; they are for root.
- **H1-N3.** The C5H interlock does not read the result's own spec sha.
- **H1-N4 and N5.** These cover what the blinded modes read and the limits of the regex backstop.
- **H2-N1.** Boundaries round-tripped through floating point can land 1 ulp over.
- **H2-N2.** The A47 G5 blind spot is caught by T1_H.

## Passed (refutation attempts that failed)

**Focus 1, outcome order.**
- The A50 group order holds, and every adjacent group-2 pair reads the earlier outcome.
- PROVISIONAL marking and non-marking hold. AMB-04 flag routing holds.
- AMB-17: each pending step alone reads INCOMPLETE. Every required gate MISSING (21) reads INCOMPLETE, and every gate's malformed verdict (25) reads NO_RUN.
- H1: 94 of 95 probes behaved as the text requires; the miss is S4.

**Focus 2.**
- **T1 plus RA6 per-row and TINY.** 18 edge cases and 4000 fuzz draws gave 0 mismatches against H2's own implementation, including exact boundaries, 1-ulp variants and NaN/inf.
- **T2 and T2c.** Inclusive boundaries hold, and a missing member reads INCOMPLETE.
- **T2I.** The 1e-12 threshold holds; an unrecorded value is never read as a pass.
- **A50 S1** is enforced at case-block, run and spec level.

**Focus 3, R-PAIR.**
- The branch comes from the rule (AMB-07; E unavailable gives PICARD), and a manifest naming the other branch reads INCOMPLETE.
- Alias invalidates both labels.
- Member leaves must be byte-equal. Cross-branch leaves are rejected. NEW-16 is enforced.
- Clean worlds resolve on both branches.

**Focus 4.**
- The A51 formula, NEW-7 aside, gave 0 mismatches over 13 histories and 3000 fuzz draws.
- E only gates decidability and never passes a threshold.

**Focus 5, blinding.**
- 851 planted sentinels produced 0 hits on stdout, stderr and files in `--validity-only` (C5H, C4T-D5, all 11 cases) and `--gates-only`, except S6.
- The positive control in full mode gave 14 hits.

## Next

The r5 delta will be reviewed against B1–B4 and S1–S8 when `r5/` lands.

**Files.**
- `R3_rpair/FINDINGS_R3_RPAIR.md`
- `H1_order_blinding/FINDINGS_H1_FINAL.md`
- `H2_T1_T2_A51/FINDINGS_H2.md` and `.json`
- the scripts and outputs under each lens directory
- `r4_loader_c3.py`
- sha256 values in `HASHES_REVIEW_V007_R4_C3V001.txt`
