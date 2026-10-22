# REVIEW: NGC driver cx3r007 (Codex3), Claude4's distinct review for dispatch 0589

Claude4. Written 2026-10-18T19:25:08Z (`date -u` at write). There were two refute-by-default lenses run in parallel, strictness and parity, followed by one adversarial refuter per SHOULD_FIX finding. These were five helpers on Claude4's account. Nothing was launched, and no target, C5H or `UVT_*` run tree was read.

## VERDICT: PASS_WITH_FINDINGS. 0 BLOCKING, 3 SHOULD_FIX, 14 NOTE

- **Scope.** Exactly these bytes:
  - `ngc_launch_record_strictness_cx3/implementation/galaxy_m0_forward_c2v011_cx3v005_cx3r007_cx3v004.py`, `e4f5864aee796febf133aa03e2bf3236a9fc566971c5d2f0f5d3e2d6b226ea69`;
  - `plans/SPEC_REGISTRY_CX3R007_V001.json`, `cd30429c27ced0837dc383c00f78899a758fefeeaae2f6134e6aae7fcad18ea2`.
- **Baseline.** r006 `c2930e18eb2ba6f691dcaffffd56658143490ab366552cf90b27506a2357be49`, with registry `3c42ca07a4e2469bcb2be8b5a6ea69e3d696d8f5aca1b1ebadecd20242af90c1`.
- **Author report.** FROM_CODEX3/0611, `3f06e891bd5b7595a03e34b290aebf058ada091e81d7415abafdc88887802387`.
- **Pins.** Every pin was verified from bytes by every helper.

### The two claims in 0589

**1. Strictness: every r006 finding is now a typed refusal naming both paths, and no NGC launch-path parse is still last-wins.**
- **First half: CONFIRMED (TESTED).**
  - ST-SF1, ST-SF2/A71-RESID-1 and the producer start.json custody reads (both chains) each refuse with a typed NGC_JSON_DUPLICATE_KEY naming the file and both occurrence paths. Duplicates are caught at every depth, inside lists, and when keys differ only by escapes.
  - ST-N2 holds inside the record operation (6/6, including checkpoint A→B→A).
  - ST-N5 holds for rows.
  - IN-NGC-WIDEN-1 holds (15/15).
  - All 48 strict copies are installed.
- **Second half: REFUTED (TESTED).** Six NGC-route parse sites are still last-wins:
  - L5148, dry-run readiness (ST7-SF1);
  - L5066 and L5216, the grid-cut helper (ST7-SF2);
  - L792, the stage-child request (ST7-N5);
  - L9196 and L9210, spec routing (ST7-N6).
- **No admission on the registered run path.** None of these admits a duplicate there: all 8 registered specs are clean under a strict parse, and all have `ngc_outer_gas_cut` null. So nothing is BLOCKING.

**2. Parity: outside NGC, r007 is byte-identical to r006, and the registry pins e4f5864a for the same eight specs.**
- **CONFIRMED as scoped (TESTED and FORMAL).**
  - **Source.** r007 is r006's exact bytes plus an inserted block of 77 top-level statements, followed by the identical `__main__` guard.
  - **Dry plans.** 78 specs × 3 = 234 fenced processes (r006, r007, and r006 again as a determinism control). 442 of 442 emitted files match: 235 raw-equal, 207 equal after the closed substitutions (driver path and sha, output root), 0 residual.
  - **RO1.** 106,300 pairs have identical outputs and exceptions.
  - **Registry.** 8/8 cases are unchanged in order and spec, and 28/28 pins resolve from bytes.
- **The exception.** The 0581 wording "behaviour outside NGC must stay byte-identical" does not hold for one output class: run-mode failure diagnostics written to disk (PAR-TB-1).
- **Coverage limit (PAR-N-COV), disclosed.** My audit fence cut 37 of the 78 dry plans short:
  - 23 DDO V007/SUPERSEDED specs stopped at the `uvt_route_b_binding*_r5.py` pin check. My brief treated every `uvt_*` name as protected, which is stricter than the run-tree rule.
  - 14 NGC3198-named specs or configs were refused at their first open.

  Parity for those 37 rests on matched partial runs up to the stop, the FORMAL AST proof, and the earlier complete trees. A top-up with a fence narrowed to admit `uvt_*` source modules (never `runs_ext/UVT_*` trees) would make the 23 DDO specs TESTED end to end. It is available on request, at a few minutes of compute.

## SHOULD_FIX

| id | finding | refuter | fix |
|---|---|---|---|
| **ST7-SF1** | `cmd_dry_run` runs the ORIGINAL L5144 because the wrapper is entered inactive. Its post-dispatch `json.loads` of DRYRUN_REPORT.json (L5148) is last-wins, outside the record operation, and derives NGC_SOURCE_BUILD_READINESS.json. The strict copy (L8361) is unreachable. Probe: a duplicated report hid both blocker lists and gave readiness PENDING_CERTIFICATES. Mitigation: the driver wrote that report itself, and the 8 registered report/readiness pairs are duplicate-free (TESTED). | NOT REFUTED; reproduced; SHOULD_FIX | Enter `_ngc_selected_record_scope_cx3r007` in `cmd_dry_run` for NGC tail specs, as `cmd_run` does. Or parse the report strictly inside a record operation, in the NGC branch only. |
| **ST7-SF2** | Inside NGC, `normalize_spec` (L5066) and `final_rows_check` (L5216) read outer-gas-cut and route-B GL-node records through the imported grid-cut helper's last-wins `json.loads` (helper `5d037291…`), outside r007's byte custody. These records decide which rows are QUERY_BEYOND_OUTER_GAS_CUT or QUERY_OUTSIDE_RETAINED_SUPPORT. `final_rows_check` L5213–5218 also turns a typed Refusal into (False, None). Probe: a duplicated cut record returned its last values (20.0 / CERTIFIED_UNCONFINED, not 5.0 / NOT_CERTIFIED). Any NGC v011 spec that declares a cut reaches this path; the 8 registered specs do not. | NOT REFUTED; reproduced; SHOULD_FIX | In NGC contexts, read the cut and GL-node records through a strict snapshot with a sha check and equality with the helper result, as `_ngc_checkpoint_read_cx3r007` does. Re-raise Refusal in `final_rows_check`. |
| **PAR-TB-1** | Outside NGC, every traceback through the 49 wrapped globals (or `sha256_file`) gains one frame (`scoped` L6548 or `sha256_file` L6513), and the `__main__` guard frame moves. These tracebacks are written into r006-path `result.json` (whose sha enters finish.json) and stage `stderr.txt`. Status, valid, rows, reasons and exit codes are unchanged (TESTED: 6/6 wrapped probes add exactly one frame; the unwrapped control is equal). This independently re-derives Claude2's lead of the same name. | NOT REFUTED; reproduced. The refuter assesses NOTE, since only failure-diagnostic text differs. I keep SHOULD_FIX, because the 0581 byte-identity requirement is literally unmet. | **Recommended: a root ruling** admitting these closed traceback-text classes in failure diagnostics written to disk outside NGC. That takes about 5 minutes and needs no code change. The alternative is a zero-frame install (swap the globals on context entry) in r008. |

## NOTE (14)

**Strictness:**
- ST7-N1: the strict RO1 loader keeps a recursive unpack, giving an untyped RecursionError at a list depth of about 1000 or more.
- ST7-N2: ValueError (an int of more than 4300 digits) and UnicodeDecodeError are untyped in `_ngc_json_loads_cx3r007`.
- ST7-N3: malformed shapes outside the ST-N5 row scope stay untyped, and non-list column `failures` read as no failures.
- ST7-N4: A71 list-to-mapping residuals; `speeds_km_s` and `rad` are built last-wins from repeated query ids.
- ST7-N5: the stage-child request parse is last-wins.
- ST7-N6: the spec-routing parses are last-wins, and the dispatch re-reads the spec.
- ST7-N7: wrapper installation fails open under a different compile filename.
- ST7-N8: a checkpoint decode refuses repeated keys with an untyped CheckpointError.

**Parity:**
- PAR-N-DEPTH: each active wrapper uses one Python frame of recursion budget.
- PAR-N-REACH: 3 of the 48 strict variants can never run.
- PAR-N-COV: the fence coverage limit above.
- PAR-N-REG: registry r007 is a correct successor, but its scope line drops two r006 disclaimers.

**Harness (mine):**
- HARNESS-N1: `fence_c4v001` lstats a protected path's components before refusing the open. No protected path was ever attempted, so no stat of a protected path happened. A successor fence should refuse on the literal path before any filesystem call.

## Recommendation for root

- **Accept r007 for the 8 registered NGC fixture specs** in place of r006 (A80.2). Every finding is either outside their run path (ST7-SF2: cut null), mitigated on it (ST7-SF1: registered reports duplicate-free), or diagnostic-only (PAR-TB-1).
- **Before step 5:**
  - a small r008 closing ST7-SF1 and ST7-SF2, needed whenever a step-5 spec declares an outer-gas cut or readiness is relied on;
  - the PAR-TB-1 ruling.

  Step 5 is more than a day away (A80), so this costs no schedule.

## Files (sha256 from bytes)

| file | sha256 |
|---|---|
| `strictness/REVIEW_STRICTNESS_C4V001.md` | `38df18ab69330933bd6d795940349afa3ef33b2249a51cd20e2a6a90c74e43e9` |
| `strictness/RESULTS_STRICTNESS_C4V001.json` | `a982a54f48a872691496edf68214fa3fdae4cbac92d4226ac5e92e4007c0c52e` |
| `strictness/HASHES_STRICTNESS_C4V001.txt` | `5ff1097b9adf5a09d837d78681725887f1c150da45abd629985645e3f5633372` |
| `parity/REVIEW_PARITY_C4V001.md` | `85972ed182a185a611cfc9d6d60e60009ede0151ea64da63657b3dbc452508e9` |
| `parity/RESULTS_PARITY_C4V001.json` | `0ee4092cd1707c5f7aba8db0112c6ec685b3d7be0d4716ee9cf3ae84a6a640a0` |
| `parity/HASHES_PARITY_C4V001.txt` | `f7e03bb09ea94c4a10155875caf109a800d2f73ead511bb865003c58c4999505` |
| `verify/strictness_1/VERIFY.md` | `7b74b23ab7f97db28ef00e4770f98847c9091b8edd2ff3a587dbfc2977732118` |
| `verify/strictness_1/REVIEW_VERIFY_STRICTNESS_1_C4V001.md` | `7b74b23ab7f97db28ef00e4770f98847c9091b8edd2ff3a587dbfc2977732118` |
| `verify/strictness_2/VERIFY.md` | `4ecc7f05e4d44803c45d117b529a4288734f64625e1199dfa11797448036ae30` |
| `verify/parity_1/VERIFY.md` | `bb86dd4af0ad0d4450514ae9b1b239a00e4c7123d1bee81dfc89a1996786b71c` |
