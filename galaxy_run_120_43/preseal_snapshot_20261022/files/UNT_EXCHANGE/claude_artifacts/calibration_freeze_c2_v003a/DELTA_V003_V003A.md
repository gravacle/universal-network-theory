# DELTA_V003_V003A: the calibration engine and prediction freeze, v003 to v003a

Claude2 lane. UTC 2026-10-17. Physical status: not_assessed.

Scope: CHECK_V001 (`calibration_freeze_c2_v003/check/CHECK_V001.md`) line defects **X1** and **X2** only. Nothing else in the modules changed. Everything below is synthetic: no project forward, no NGC3198 velocity, no network, single thread. Runtime: codex python 3.12.14 `-I -B`, numpy 2.3.5. The only real file opened is the target-free NGC3198 query manifest (`a2936517…`, ids only), by the v003 checker fixtures exactly as in CHECK_V001.

Line numbers are v003a lines. Mechanical diffs: `DIFF_ENGINE_c2v003_to_c2v003a.diff` (8 hunks, +61/−6) and `DIFF_FREEZE_c2v003_to_c2v003a.diff` (12 hunks, +237/−66).

| File | v003 sha256 | v003a sha256 | v003a lines |
|---|---|---|---|
| engine | `ec509648…51fcc7` | `193841fa1f1d078f7fc981fdba78cf3d736b50ee17e019f0cf94aae94e3a63a6` | 2992 |
| freeze | `f670d14b…5e8028` | `5ee3e5dce72c77870903ce378e146fb86f7288ab2a403deb39796e348ee0f9b8` | 3145 |

Identity: `MODULE_NAME` follows the new file names (`calibration_region_engine_c2v003a`, `prediction_freeze_c2v003a`); the engine `PREDECESSOR` names v003. The schemas (`FREEZE_MANIFEST_C2V003`, `CALIBRATION_RUN_RECORD_C2V003`, `EXPLORATION_FINGERPRINT_C2V003`) are unchanged.

## 1. X1 (P34-14 depth): the four listed fixes

| # | Fix | v003 location | v003a lines | Change |
|---|---|---|---|---|
| 1 | Rectangles from the pinned region file **bytes**, never the run dict | freeze `_region_of` L971–984; reclassification L1125–1130 | constants 104–111; `_region_from_bytes` 989–1033; `_region_of` 1036–1059; select 1161–1164, reclassification 1200 | <ul><li>`select_representative_points` takes only `region.path` and `region.sha256` from the run. It reads the file (regular file, non-blocking), checks its sha256 **before parsing**, and re-derives the 12 ids and `[low, high]` with the engine's validation (12 rows, unique ids, every row field finite, σ > 0, low < observed < high, top fields present).</li><li>Every admitted point is reclassified against those rectangles. The run dict's `rectangles` and `row_ids` are never read.</li><li>An ok region without a path, or bytes that do not hash to the named sha, refuses. A run without an ok region keeps v003's layout-B NOTE, and the writer refuses it.</li></ul> |
| 1 | Writer and verifier reclassify every **member** from bytes | writer L2469–2496; verifier L2645–2655 | `_check_calibration_record` 2353–2433; writer 2632–2667; verifier 2816–2834 | <ul><li>The writer and the verifier re-derive the rectangles from the **pinned** region file (the `input_files` pin whose sha equals `observation_region_sha256`).</li><li>They reclassify every admitted point of the pinned calibration record from its recorded DDO154 prediction.</li><li>Every member (`log_index`, `u`) of the primary and of each alternative must be a recorded admitted point with identical `u`.</li></ul> |
| 2 | Calibration record pin **mandatory** | writer L2473–2494 (optional); `_validate_input_bindings` L2268–2274 (`if cr is not None`); verifier L2647 | writer 2639–2654; `_validate_input_bindings` 2342–2350; verifier 2816–2834 | <ul><li>Exactly one `CALIBRATION_RUN_RECORD_C2V003` pin is required in `input_files`.</li><li>`input_bindings.calibration_record = None` fails the structure check, which the writer and the verifier share, so a re-hashed manifest without it is refused.</li><li>`calibration_record_bound` is therefore always True on a written manifest.</li></ul> |
| 2 | Engine **recomputes** the fingerprint (record) | `write_calibration_record` L2826 copied `run['exploration_fingerprint']` | `_run_fingerprint` 2748–2765; `write_calibration_record` 2826–2836, 2866 | <ul><li>The fingerprint is recomputed from `run.exploration.admitted_points` and `run.region.sha256`, and the record stores the recomputed value.</li><li>**Choice:** a run whose reported fingerprint is not None and differs from the recomputed one is refused (it was edited after the engine returned).</li><li>A run without an exploration (INPUT_INVALID, SEED_INVALID, …) is still recorded, with fingerprint None.</li></ul> |
| 2 | Engine **recomputes** the fingerprint (verify) | `verify_calibration_record` L2877–2934 (no recomputation) | 2948–2962 | <ul><li>The fingerprint is recomputed from the recorded run content and must equal the stored `exploration_fingerprint`.</li><li>`region_sha256` must equal the recorded `run.region.sha256`.</li><li>New output field: `exploration_fingerprint_recomputed`.</li></ul> |
| 2 | Freeze checks: the pinned record's **recomputed** fingerprint equals the run's | writer compared the record's *stored* field | `_check_calibration_record` 2353–2433 (writer 2660, verifier 2831) | <ul><li>Checks the schema and the self-hash (`record_sha256` over the canonical body).</li><li>Recomputes the fingerprint from the record's run content. It must equal the record's stored value **and** the selection's `calibration_fingerprint` (recomputed by `select_representative_points` from the run's admitted points).</li><li>The record's region sha must equal the pinned region file's.</li></ul> |
| 3 | Empty or missing `hull_box` **refused** | freeze L1158 (`and hull_box`: `{}` and None skipped) | 1229–1251 | `hull_box` must be a non-empty dict; otherwise `REFUSED (S8/X1)`. The S8 well-formedness and range checks are unchanged. |

**What still passes, by design.** A fully consistent forgery passes: root writes a forged region file, records the forged run, and pins both. It is self-consistent, and the module cannot tell it from an honest run on another region. Only two things distinguish it:
- the region pin sha in the manifest, which is not the program DDO154 region `13c16a63…`;
- the externally logged `record_file_sha256`.

This is the same class as CHECK_V001's last untested row. Probe OBS-X1.6 records it.

## 2. X2: correction to DELTA_V002_V003.md line 52 (S10 evidence)

DELTA_V002_V003.md stays unchanged (read-only). Its S10 evidence cell is corrected here.

**False statement (v003 DELTA line 52):** "P2 `M-*.never_raises` PASS in v002 and v003".

**Correct statement.** `M-eng.never_raises` and `M-frz.never_raises` **FAIL** in Claude4's B2 P2 suites (`p2_original` and `p2_adapted`), for both v003 and the v002 baseline:
- v003 record run: `final/regression/b2_claude4/out/v003_20261017T143333Z_55543`. P2 results sha `54800302…8494` (original) and `1ce15f3b…1e47` (adapted).
- v002 baseline: `out_v002_baseline/v002_20261017T142337Z_42500`.

The cause is TypeErrors from v001-signature calls:
- `run_calibration_region` is missing `global_design_count`;
- `evaluate_envelopes` is missing `spec`.

This is by design under X0: a call that does not match the keyword-only signature still raises TypeError. The P2 rows are therefore **not** evidence for S10.

The S10 evidence is:
- v003 self-test S10.1–S10.4 and S8.2;
- checker B-S10a/b/c (CHECK_V001: notes 5000 deep, cyclic list/dict, inf/nan `hull_box` key and ndarray fields all give ok=False without raising).

All of these PASS on v003a as well (§3).

## 3. Re-runs on the v003a bytes (`193841fa…`, `5ee3e5dc…`)

| Suite | Result | Notes |
|---|---|---|
| v003 self-test (`regression/v003_selftest/selftest_v003_ON_V003A.py`) | **64/64 PASS** | <ul><li>The only adaptation is **AD-1** (diff `DIFF_selftest_v003_to_ON_V003A.diff`, plus the two module paths). RUN1 is recorded once in its own registry (`calibration_record_base_AD1.json`) and pinned wherever v003 pinned [REGION, QM]: the default `write()` inputs and D3.1.</li><li>The P34-16 registry and its line-count check are untouched.</li><li>D3.2–D3.5, P34-16.3/.4 and A4 are unchanged.</li></ul> |
| v003 checker fixtures `fixtures_check_c2v003.py` (`e6afeb56…`, read-only) via `regression/checker_v003/run_checker_on_v003a.py` | **52/52 PASS**; X-P34-14d FAIL→**PASS** | <ul><li>The wrapper writes a path-only copy. `PATH_WRAPPER.diff` has 3 lines: FINAL, ENG_PATH and FRZ_PATH. The plan copy sha is `b3a04968…`.</li><li>Pass/fail by id against the record run `144757Z_60608`: **only X-P34-14d changed**. `select_representative_points` now refuses the forged run: "log_index 9 … S01 = 104.33 outside the closed rectangle [97.99, 102.01]".</li><li>Detail differences, after normalising hashes and paths, are only wall seconds, manifest hashes, and B-D10 `n_calls` 631→529. The 102 calls were X-P34-14d's two v003 freezes, which are no longer reached; 529 equals CHECK_V001's blind-only count.</li></ul> |
| `root_call_order_toy_v003a.py` (path-only diff from `root_call_order_toy.py`) | engine COMPLETE (28 admitted); FREEZE_COMPLETE; 10 members; verify, registration and registry chain ok; `calibration_record_bound: true`; member counts 0/0/43, reference 0 | Run `root_call_order_runs/run_20261017T145907Z_67194`. The toy already pinned the record, so it did not need to change. |
| X1 probes (author's own, not blind; `regression/x1_probes/x1_probes_v003a.py`) | **19/19 PASS** (18 checks + OBS-X1.6) | <ul><li>Widened dict rectangles alone change nothing (the selection is byte-identical).</li><li>Refused: a dict sha the file does not hash to; a missing path; a forged region file named by the run (with the honest record pinned, and with both regions pinned); a missing record pin; a re-hashed manifest with a None record binding.</li><li>Recompute-not-copy: a tampered reported fingerprint refuses; a forged run with fingerprint None is recorded with the recomputed value; an edited, self-re-hashed record fails verify; a relabelled record of other content is refused.</li><li>A record with one member's prediction moved outside the true rectangle is refused by member reclassification.</li><li>A missing or empty `hull_box` refuses.</li></ul> Two earlier probe runs are kept under `runs/superseded_*`: a fixture error of mine (the forger's `hull_box` was not updated), and the run before OBS-X1.6 was added. |

## 4. Documents not changed (read-only), now stale on one point

- `final/DELTA_V002_V003.md` line 59 (P34-16, "Choice: pinning the record is recommended …, not required"). Superseded: in v003a the pin is required.
- `final/ROOT_CALL_ORDER.md`, steps 1b and 5. The documented order already pins the record, so the call order is unchanged. In v003a, step 5 refuses without it.

## 5. Untested

These are unchanged from CHECK_V001:
- the real forwards and the real 15-coordinate spec;
- the real DDO154 region file (`13c16a63…`) through the new byte re-derivation. The validation mirrors the engine's loader, but only synthetic region files were used;
- FIFO pins;
- LAPACK builds other than Accelerate arm64;
- `WALL_LIMIT` trips;
- registration timing (D8);
- a fully consistent forgery (§1; recorded as OBS-X1.6, not prevented).
