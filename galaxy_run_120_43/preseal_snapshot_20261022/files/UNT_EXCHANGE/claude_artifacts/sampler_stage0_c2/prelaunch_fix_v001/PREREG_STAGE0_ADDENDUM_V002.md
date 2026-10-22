# PREREG_STAGE0_ADDENDUM_V002: outcome mapping for edge cases, DRIFT_FLAG quoting, INCOMPLETE_n/8

Written 2026-10-18 UTC. Order of writing:
- after PREREG_STAGE0_V001 (`aee48b022bccc29196a3dddb632be4a2132d1ff8942fb4217938d6b70355ea1f`, sealed 01:05:50Z);
- after PREREG_STAGE0_ADDENDUM_V001 (`34e5dd29b1a0cd2abc048b869968f35a3f993e729a423ce20abcbadfa2931d69`, sealed 01:25:22Z);
- after check/CHECK_V001.md (`bb7aae1bc511822dfcac5eaaeca3fe6aa170b2a9adc2680831dd51e630cdbc9e`);
- **before any production stage-0 run**. At 01:49:15Z, `CLAUDE2/runs_ext/` on External1 had no STAGE0 entry.

The only sampler output that existed when this was written:
- the toy smoke chains (16 rows);
- the 150 s identity runs;
- the checker's toy RSS runs.

None of them carries information about any stage-0 outcome.

Frozen pins: V002 addendum `17c26616…` and V003 addendum `5bef6552…`. The V004 addendum is cited by name only.

## What this addendum does and does not do

The sealed prereg and ADDENDUM_V001 are unchanged. Every sealed condition, threshold and estimator stays exactly as written. This addendum does three things:
- It declares the outcome for cases where **no sealed §6 row's condition holds**, or where the sealed text leaves the mapping to code (CHECK_V001 C-2 G-1). It adds two classes, each with its own reading.
- It declares how an S0-PASS is quoted (CHECK_V001 C-2 G-2).
- It operationalizes the sealed INCOMPLETE_n/8 row for killed or crashed chains (CHECK_V001 C-3).

`prelaunch_fix_v001/analysis/stage0_analysis_v002.py` implements this. It is the only analysis that the launch pins V002 bind.

Status: DECLARED-PREMISE, for the mapping. Each case in B1–B3 is reachable by the v001 code paths that CHECK_V001 identified (FORMAL-RESULT, by reading `stage0_lib_v001.column_verdict` and the v001 `outcome()`).

## B0. Terms (DECLARED-PREMISE)

- **Assessed column.** Every column of §2 except the structural `exact_invariant` contacts.
- **blen.** blen = rows / 8 = 2048.
- **τ-leg failure (assessed).** For an assessed column, at least one of these holds:
  - its pooled-ACF τ̃ was estimated and blen < 5 τ̃ (τ̃ > 409.6);
  - some process's τ̂ was estimated and blen < 5 τ̂ / 2 (τ̂ > 819.2).
- **τ unassessable.** For an assessed column, τ̃ or at least one process's τ̂ could not be estimated. The causes are:
  - the series is constant in that process;
  - the column is constant in every process;
  - the Sokal window c = 5 never closed.
- **Stuck process.** A complete process with zero changed-path accepts in measurement (§2: "fails the rule").
- **Rhat = ∞.** Within-process variance is zero in every process, but the process means differ. The transcribed `_rhat` returns `failed, inf`.

## B1. Unassessable column (CHECK_V001 G-1)

These cases are declared:
- **Constant in every process at one value.** R-LIT is `unassessable`, as sealed. R-MA is `unassessable`.
- **Constant in some processes, varying in others.** R-LIT is `unassessable`, as sealed. The R-MA column verdict is reported as v001 computes it (`failed`, because the per-process guard τ̂ ≤ 819.2 cannot be evaluated). For the outcome, this column counts as **τ unassessable**. It does not count as an assessed τ-leg failure.
- **Sokal window not closed.** The column counts as **τ unassessable**.

**New class S0-UNASSESSABLE.** Its condition: no column has Rhat > 1.1 (including ∞), no process is stuck, the R-MA joint verdict is not `passed`, and **no assessed column has an assessed τ-leg failure**. In other words, the τ leg did not pass only because at least one τ could not be estimated.

- **P-96 reading.** There is no verdict on the τ leg. The Rhat leg passed. The τ leg is UNTESTED for the listed columns and processes (deciding test: an estimate of those columns' τ). The analysis lists every such column with its block or background location and the processes whose τ̂ is missing. Stage 1 is not proposable from this outcome alone. What follows is a root decision.
- **Grid reading.** As S0-FAIL-RHAT: a start-balanced, graph-ensemble sensitivity grid only, with the process-jackknife band, never a replacement. It is offered for the NGC outer rows if it is convexity-admissible.

**Unchanged.** If any assessed column has an assessed τ-leg failure, the sealed S0-FAIL-TAU condition ("R-MA τ leg fails") holds and S0-FAIL-TAU is registered, whatever the number of unassessable columns. That number is reported next to it.

## B2. Zero-accept (stuck) process

**New class S0-FAIL-STUCK.** Its condition: at least one complete process is stuck, and no column has Rhat > 1.1 (including ∞).

- **P-96 reading.** TESTED-NEGATIVE: not every process changed its path during measurement, so the §2 rule fails (sealed). The stuck processes are listed. Their τ is not estimated, so no length rescaling is derived from this outcome. Stage 1 is not proposable from it. Read it with §5 wiring and with A2 for the stuck processes.
- **Grid reading.** As S0-FAIL-RHAT.

**Unchanged.** If some column has Rhat > 1.1 (including ∞), the sealed S0-FAIL-RHAT condition holds and S0-FAIL-RHAT is registered. The stuck processes are listed next to it.

## B3. Rhat = ∞

Rhat = ∞ is Rhat > 1.1. It counts toward S0-FAIL-RHAT.

The v001 `outcome()` counted only finite Rhat values (`columns_rhat_gt_1.1`). It would have sent such a column to S0-FAIL-TAU. v002 adds a separate count, `columns_rhat_inf`, and leaves the v001 summary field unchanged.

## B4. Complete precedence (evaluated top to bottom; the first match registers)

| # | Class | Condition |
|---|---|---|
| 1 | INCOMPLETE_n/8 | fewer than 8 processes complete (sealed; operationalized in B6) |
| 2 | S0-PASS-LIT | R-LIT passes and census/U passes (sealed) |
| 3 | S0-PASS-MA | no Rhat > 1.1 (including ∞), R-MA passes, census/U passes (sealed) |
| 4 | S0-FAIL-RHAT | some column Rhat > 1.1, including ∞ (sealed; B3) |
| 5 | S0-FAIL-STUCK | some complete process stuck (B2) |
| 6 | S0-FAIL-TAU | R-MA not passed and at least one assessed τ-leg failure (sealed) |
| 7 | S0-UNASSESSABLE | R-MA not passed, no assessed τ-leg failure, at least one τ-unassessable column (B1) |
| 8 | S0-FAIL-CENSUS | census/U fails while the block rule passes (sealed) |

Rows 2–4, 6 and 8 are the sealed rows in the v001 order. Rows 5 and 7 are evaluated only where no sealed row's condition held before them, so neither new class captures a case that a sealed row covers.

## B5. Every S0-PASS is quoted with DRIFT_FLAG (CHECK_V001 G-2)

- ADDENDUM_V001 F3 holds: the sealed flat-quarter leg has power 0.00 against a 1.72 sd drift. A pass of that leg is therefore not evidence of stationarity.
- So any S0-PASS-LIT or S0-PASS-MA is quoted only together with DRIFT_FLAG (A3: FQ-WC fails in some (series, process) unit). It is written as `S0-PASS-… [DRIFT_FLAG=true|false]`, with the measured FQ-WC size at the flagged units' τ̂.
- The analysis writes this string to `outcome_quoted`. The class itself, and the rule, are unchanged.
- DRIFT_FLAG = true does not change the class. It means the pass does not establish stationarity.

## B6. INCOMPLETE_n/8 for killed or crashed chains (CHECK_V001 C-3)

A process is **complete** only if all of these hold:
- `result.json` exists, is non-empty, and parses as JSON;
- it carries `sampler_result` and `stage0_binding`;
- the binding matches its chain index, the starts manifest and the prereg sha;
- `status == "complete"`;
- its committed capture holds exactly `measurement_sweeps` rows.

Each failure is recorded per process as its reason, together with the monitor `receipt.json` `stop_reason` when one exists and parses. The reasons are:
- missing result;
- 0-byte result (a monitor kill on MEMORY_CAP, WALL_CAP or OUTPUT_CAP);
- partial or unparseable JSON;
- no `sampler_result` (worker exception);
- no binding;
- status;
- row count;
- unloadable capture.

A binding that is present but does not match is a provenance error, not an incomplete chain. It stops the analysis, as in v001.

With n < 8 complete processes:
- The outcome is INCOMPLETE_n/8, and there is no rule verdict (sealed).
- The n complete processes are analysed descriptively with the same code as the 8/8 case.
- Each section that cannot be computed at that n is recorded as `not_computed` with its reason. The analysis does not crash.
- Class labels inside the sections (memory, A1, A2, wiring, isotropy) are descriptive only. Their thresholds were set for 8 processes.
- The k = 0 lapse drift reading is not made.

## What is not claimed

- Nothing here sets or expects any outcome. Every class registers.
- No threshold, estimator, column set or sealed reading is changed.
