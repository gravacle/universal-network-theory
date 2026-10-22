# PREREG_STAGE0_ADDENDUM_V003: root ruling on outcome precedence; complete-but-missing capture; run-dir arity and order

Written 2026-10-18 UTC. Order of writing:
- after PREREG_STAGE0_V001 (`aee48b022bccc29196a3dddb632be4a2132d1ff8942fb4217938d6b70355ea1f`, sealed 01:05:50Z);
- after PREREG_STAGE0_ADDENDUM_V001 (`34e5dd29b1a0cd2abc048b869968f35a3f993e729a423ce20abcbadfa2931d69`, sealed 01:25:22Z);
- after PREREG_STAGE0_ADDENDUM_V002 (`b3a4d23f9130dc2c1bf810883eea59eb4000522d192ba830e2b226a3091f7ae1`, sealed 01:50:05Z);
- after `prelaunch_fix_v001/check/CHECK_V001.md` (`812671b433fa7dcb39f7c293d33f45a1533af16b8b5d165de671066ca575a28a`), findings F-1, F-2, F-3;
- **before any production stage-0 run**. At 03:26:38Z, External1 `CLAUDE2/runs_ext/` had no STAGE0 entry. The seal file records a second check made at seal time.

No sampler output that carries information about any stage-0 outcome existed when this was written (only the toy smoke chains, the 150 s identity runs, the checker's toy runs, and synthetic test inputs).

## What this addendum does

It applies one root ruling, and fixes two code findings. No threshold, estimator, column set, sealed condition or sealed reading changes.

`prelaunch_fix_v002/analysis/stage0_analysis_v003.py` implements this addendum together with ADDENDUM_V002's surviving parts. It is the only analysis that launch pins V003 bind.

What stays in force from ADDENDUM_V002, unchanged: B0 (terms), B1 except its closing "Unchanged" sentence, B2's class definition and reading, B3, B5, and B6 (as extended by C2 below). **B4 is replaced in full by C1.**

## C0. Root ruling (DECLARED by root)

**Sealed §6 rows always take precedence.** An addendum class (S0-FAIL-STUCK, S0-UNASSESSABLE) registers only where no sealed §6 row's condition holds. When a sealed row registers, the addendum's quantities (stuck processes, τ-unassessable columns) are listed next to it. They do not change the sealed class or its sealed reading.

The sealed S0-FAIL-TAU condition "R-MA τ leg fails" keeps the B0 reading accepted in CHECK_V001 R-4: at least one assessed τ-leg failure.

## C1. Precedence (replaces ADDENDUM_V002 B4; evaluated top to bottom, the first match registers)

| # | Class | Condition | Source |
|---|---|---|---|
| 1 | INCOMPLETE_n/8 | fewer than 8 processes complete | sealed; operationalized in V002 B6 and C2 |
| 2 | S0-PASS-LIT | R-LIT joint passes and census/U passes | sealed |
| 3 | S0-PASS-MA | no column Rhat > 1.1 (including ∞), R-MA joint passes, census/U passes | sealed |
| 4 | S0-FAIL-RHAT | some column Rhat > 1.1, including ∞ | sealed; V002 B3 |
| 5 | S0-FAIL-TAU | no Rhat > 1.1 (including ∞), R-MA joint not passed, at least one assessed τ-leg failure (B0). This holds **whether or not any process is stuck and whatever the number of τ-unassessable columns** | sealed |
| 6 | S0-FAIL-CENSUS | census/U fails while the block rule passes (R-LIT joint or R-MA joint passed) | sealed |
| 7 | S0-FAIL-STUCK | at least one complete process is stuck | V002 B2; only after rows 1–6 |
| 8 | S0-UNASSESSABLE | R-MA joint not passed, at least one τ-unassessable column | V002 B1; only after rows 1–7 |
| 9 | ANALYSIS_ERROR_UNMAPPED | none of rows 1–8 | integrity case, below |

Rows 2–6 are the sealed rows in the v001 code order. Rows 7 and 8 come after every sealed row, so neither addendum class can register where a sealed row's condition holds.

**Row 9 is unreachable at 8 complete processes** (FORMAL-RESULT, by reading `stage0_lib_v001.column_verdict`, `rhat`, `sokal_tau`, `pooled_acf_tau` and `mixing()`):
- With a complete process stuck, row 7 matches.
- Otherwise a block's R-MA verdict fails or is unassessable only through a column whose Rhat failed or exceeded 1.1 (row 4), whose pooled τ̃ or some τ̂ failed the τ leg (row 5), or whose pooled τ̃ or some τ̂ could not be estimated (row 8).
- If R-MA passes and census/U passes, row 3 or row 2 matches; if R-MA passes and census/U fails, row 6 matches.

If row 9 is ever reached, the analysis still writes its JSON, with `outcome = ANALYSIS_ERROR_UNMAPPED` and no rule verdict. The case goes to root. It is not a stage-0 outcome.

**Differences from analysis v002 (exhaustive):**
- A stuck process together with an assessed τ-leg failure and no Rhat > 1.1: v002 registered S0-FAIL-STUCK. V003 registers S0-FAIL-TAU, with the stuck processes listed (CHECK_V001 F-1, probe P1).
- R-LIT joint passed, R-MA joint not passed with no assessed τ-leg failure (the pooled τ̃ could not be estimated), census/U failed: v002 registered S0-UNASSESSABLE. V003 registers the sealed S0-FAIL-CENSUS, since the block rule (R-LIT) passed.
- The residual of row 9: v002 registered S0-FAIL-TAU. V003 registers ANALYSIS_ERROR_UNMAPPED.

Every other combination of outcome inputs that `column_verdict` and `mixing()` can produce registers the same class in v002 and v003. The tests check this exhaustively over those inputs (test T6).

## C1a. Corrected sentences of ADDENDUM_V002

ADDENDUM_V002 B1's closing sentence ("Unchanged. If any assessed column has an assessed τ-leg failure, … S0-FAIL-TAU is registered, whatever the number of unassessable columns") was **false under its own B4**: with a stuck process, B4 row 5 registered S0-FAIL-STUCK first. ADDENDUM_V002 B4's closing sentence ("neither new class captures a case that a sealed row covers") was false for the same case.

Both are replaced by this sentence:

> If no column has Rhat > 1.1 (including ∞) and any assessed column has an assessed τ-leg failure, the sealed S0-FAIL-TAU condition holds and S0-FAIL-TAU is registered, whatever the number of τ-unassessable columns and whether or not any process is stuck. Both are reported next to it.

ADDENDUM_V002 B2's closing sentence (S0-FAIL-RHAT takes precedence over a stuck process) was true and stays.

## C1b. Readings when a sealed row registers alongside addendum quantities

- The sealed row's P-96 and grid readings register exactly as sealed (§6).
- The analysis lists the stuck processes and the τ-unassessable columns next to the class (`outcome_mapping_inputs`).
- A stuck process has no τ̂ estimate, so it contributes nothing to τ̃_max. The S0-FAIL-TAU length rescaling is computed from the assessed τ only, as the sealed row's estimator already does. This is a statement of what the code computes, not a new reading.

## C2. Complete status with a missing or unloadable capture (CHECK_V001 F-2; extends V002 B6)

V002 B6 lists "unloadable capture" as a not-complete reason, but analysis v002 reached that branch only for a status other than `complete`. With `status == "complete"` and no capture, v002 raised `KeyError: 'chain_id'`.

From V003, for a result that passes every other B6 check and reports `status == "complete"`, each of these makes the process **not complete**, with the reason recorded:
- loading `committed_capture` raises any exception (missing directory, no block files, an unreadable block, non-contiguous measurement ids);
- the capture holds no rows for chain 0.

These stay provenance or integrity errors that stop the analysis, as in v001 and v002:
- a binding that is present but does not match;
- a capture that holds a chain id other than 0;
- a background label order that differs from the pinned order.

## C3. Run-dir arity and order (CHECK_V001 F-3)

The stage-0 mode **refuses**, before reading any result and without writing any output, unless all of these hold:
- exactly 8 run directories are given;
- each exists and is a directory;
- the 8 resolved paths are pairwise distinct;
- the output prefix's `.json` and `_grids.npz` do not exist yet, and the prefix's parent directory exists;
- for position k (0..7), every chain index the directory itself declares equals k:
  - a directory name of the monitor form `STAGE0_L4_BIRTHK_C<j>_RUN_V<nnn>` declares j;
  - a `receipt.json` or `launch.json` that parses and carries an integer `chain` declares that integer.

A refusal exits non-zero. It registers no outcome, because no analysis was made.

The `stage0_binding` check of V002 B6 also stays: a present binding whose chain differs from k is a provenance error.

## What is not claimed

- Nothing here sets or expects any outcome. Every class registers.
- No threshold, estimator, column set, sealed condition or sealed reading is changed.
- Full-size memory and time of the analysis remain UNTESTED (deciding test: the production analysis run).
