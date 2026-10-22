date -u: Mon Oct 19 19:41:30 UTC 2026

# README_RI45_14_C2V004: the RI45-14 list successor (V006 A163; Claude4 0223 B1, B2, N2, V-N1)

**From** the Claude2 root workflow `ri45-14-c2v004-and-slot-geometry`.
**List:** `FREEZE_EXPECTED_INPUTS_C2V004.json` (`54997f94…a3ce`). It supersedes C2V003 (`454dd3cc`, the A157 RI45_14_LIST_PIN).
**Status:** BUILT_NOT_PINNED. Claude4 does the delta re-review (A163). It authorizes nothing, launches nothing and reads no target.

## Result

**CHECK first (A163 L1406):** S0_SPECS_OK, FDPLAN_OK and FREEZE_SPEC_PLACEHOLDER (`NGC3198_GEOMETRY_TRACE_C2V004.json` `c1ac10f8`).
- The S0 geometry does not block the S0 launch.
- The placeholder use is confined to member selection: see `SLOT_GEOMETRY_FINDING_C2V004.md`. No phase1 successor is needed for correctness. A minimal hardening successor is described there and not built.

**B1, notes (A163 L1400).**
- **What the notes are.** `notes` is a deep copy of slots V003 `notes_block_for_manifest`, every key, plus `structural_assumptions["A18-ROOT-V004"]`.
- **The A18 entry.** It is `{section: A18, text_verbatim: V004 A18 L96-L121 from bytes, source: {path, sha256 487d4449, lines, section_sha256 30b69c45}}`.
- **The extra keys.** A13 is kept. A16.1 is now the A157 text (V006 L1275). Both are stored only.
- **Checks.** The notes pass `_check_slot_geometry` and `_headline_conditions` with the spec of record (TESTED: build check, K4, D-01, D-02, D-04). The C2V003 notes are refused (D-05), and so are notes without the A18 entry (D-06).

**B2, spec (A163 L1401).**
- **The recipe.** `spec_of_record` = `make_freeze_coordinate_spec(apply_coordinate_mode(CX2V006 coordinates + slots V003 ngc3198_slots, addendum coordinate_mode).coordinates).spec`.
- **Its sha.** It is embedded in the list and written as `FREEZE_SPEC_OF_RECORD_C2V004.json`. The file sha256, `e2a7650e…94ec`, equals the canonical sha recorded in the list. That file is the spec root saves at RUNBOOK step 1a/1b (the pass driver's `spec` input).
- **Engine part.** Its engine part (`54120a12…2e27`) equals three references (TESTED, K2):
  - the phase1 placeholder build;
  - orchestrator c2v005's own campaign derivation (`Context._apply_coordinate_mode` on CX2V006 `engine_coordinates`);
  - the orchestrator's V001 record check (L1663) with both slot sources.
- **"Same spec".** It is limited to the engine part. Members are identical under the two specs (D-09).
- **Precondition.** CX2V006's precondition NGC-slots is closed by slots V003. The V002/V005A pair is removed (A157).

**N2, interior_count = 5.**
- **Status.** ROOT_DECLARED_IN_V006 (A157 L1273; E_A157_1 at A163 L1408).
- **Binding sites, from bytes.** v003g L1245, L1557, L2734 and L3442; every phase1 version's handoff, fdplan and at1 sites; roster builders c2v001 and c2v005 (no interior_count; bound through `plan_outputs` and the pass driver's saved selection); RUNBOOK_V002 and RUNBOOK_V002_C2V005.
- **Checks IC-P1-HANDOFF, -FDPLAN, -MEMBERS, -FREEZE and IC-P2-SELECTION, -PLAN, -AT1, -FREEZE.** Each requires 5 and names the record field that shows it.

**V-N1, Phase-2 allow_incomplete (A163 L1415).**
- **The rule.** True if and only if a member of an evaluated alternative has `own_disposition` UNEVALUATED_CAP (rule f) or UNEVALUATED_STEP7_DISCREPANCY (rule b) in the replay plan of the last pass (the FULL REPLAY_PLAN, or its step-7 successor). That freeze is FREEZE_INCOMPLETE. Otherwise the value is False.
- **Tested.** D-02 (none: False, FREEZE_COMPLETE), D-03 (one, with False: refused A3) and D-04 (one: True, FREEZE_INCOMPLETE).

## Self-check and dry run

- **`SELFCHECK_RESULTS_C2V004.json`: 16 rows, all AS_EXPECTED.**
  - F-rows: the status rule. F-C4-01 PASS on the list; F-C4-02, -03, -04 and -07 MUST_FAIL; F-C4-05 and -06 controls.
  - K-rows: the contract. K-C4-01 PASS; K-C4-02 (C2V003 itself) and K-C4-03 to -08 (mutations) MUST_FAIL on the K-rows they name.
- **`DRYRUN_FREEZE_C2V004.json`: rows D-01 to D-10, all AS_EXPECTED.**
  - These are synthetic fixed-distance `write_freeze_manifest` runs through the pinned v003g, with the list's spec, notes, parameter_region and alternatives.
  - The engine run is synthetic, over the real CX2V006 engine coordinates: COMPLETE, 77 admitted, 12 members at interior_count 5, 3 identified directions.
  - The manifests it writes pass `verify_freeze_manifest`.

**Re-check** (each exits 0 on the list; the dry run needs a new scratch folder and a new output path):
```
PY=/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
$PY -I -B build/selfcheck_freeze_c2v004.py FREEZE_EXPECTED_INPUTS_C2V004.json
$PY -I -B build/selfcheck_contract_c2v004.py FREEZE_EXPECTED_INPUTS_C2V004.json
$PY -I -B build/dryrun_freeze_c2v004.py --list FREEZE_EXPECTED_INPUTS_C2V004.json --list-sha256 54997f946b85150ea76cf14485c26ccd5d67227d80ddb7c2aaa05011c887a3ce --c2v003 FREEZE_EXPECTED_INPUTS_C2V003.json --scratch <new dir> --out <new file>
```
The first two commands take the list's full path when run from outside the kit.

## Files (sha256 from bytes; the full list is in HASHES_C2V004.txt)

| File | sha256 |
|---|---|
| FREEZE_EXPECTED_INPUTS_C2V004.json | `54997f946b85150ea76cf14485c26ccd5d67227d80ddb7c2aaa05011c887a3ce` |
| FREEZE_SPEC_OF_RECORD_C2V004.json | `e2a7650e166a9230138ffd16453ac8fdabab41a8695169844940c4c061a894ec` |
| DIFF_FREEZE_EXPECTED_INPUTS_C2V003_TO_C2V004.json / .diff | `b40759a0…2269` / `b6569a51…6ca9` |
| SELFCHECK_RESULTS_C2V004.json | `bef69264f069ceb00745f24c41a0112a464ea9db66354c3d9cd8733c67c68459` |
| DRYRUN_FREEZE_C2V004.json | `54754395a57002103ca528d86ebd406546d9d2ad404d18318e1fbeffd43838d7` |
| SLOT_GEOMETRY_FINDING_C2V004.md | `60bb6145bd08a3dc22f56b482e2e6a83a60f222790d6d9e6c03de0a1ec900f97` |
| NGC3198_GEOMETRY_TRACE_C2V004.json (the CHECK) | `c1ac10f8f5e814c783d2d8f3f4f1a8a5e1d62eea5f8853f633a23b6fdf84383f` |
| build/build_freeze_inputs_c2v004.py | `cae960728c46cf85c75b8aa94b5c07bd4ced3930ddb1e6b25b10b28937988836` |
| build/selfcheck_freeze_c2v004.py | `03c3619a4a4d9472cebecc5dab105d40c5ecd9c7d6923a7f9ca867487cf6519a` |
| build/selfcheck_contract_c2v004.py | `0179295447207d992ea6a00c2295bb63632d8140d1f1f83d6f8b91d9465fd741` |
| build/dryrun_freeze_c2v004.py | `75b7842d10f178dfb00453d80d9e03ee0c207ea159beeb02a35e6a8ba6bf54b9` |

## Deviations and disclosures

1. **The status checker has a successor.**
   - The C2V003 checker (`1875c697`) refuses C2V004 at one leaf only: the verbatim slots sentence "The status of these slots under A16.1 is NOT_EVALUATED_BEFORE_FREEZE", which it binds to the list's `slots` pin.
   - B1 requires that text verbatim. So `selfcheck_freeze_c2v004.py` is the C2V003 rule with exactly one change: it does not read the notes value as claims. That subtree is checked byte for byte by K3 instead.
   - Row F-C4-00 records the predecessor's refusal at that leaf alone. F-C4-07 shows the same sentence outside the subtree is still refused.
2. **The dry run patches v003g in memory.**
   - Four root constants are patched (ROOT_SLOTS_PATH/SHA256 and REGISTERED_GL_NODES_PATH/SHA256) to synthetic files. This keeps v003g from opening the program slots file, the NGC3198 query manifest and the route-B config.
   - The synthetic engine run uses the CX2V006 engine parameters with the budget raised from 120 to 2000, so it completes. Phase 1's real exploration is BUDGET_EXHAUSTED, which only adds EXPLORATION_STATUS_BUDGET_EXHAUSTED.
   - Scratch outputs (synthetic manifests, record, world files) are in the session scratchpad: `…/scratchpad/c2v004_dryrun_final/`. Earlier trial builds are in the same scratchpad and are not of record.
3. **Not opened.** The DDO154 observation-region file was not opened. Its C2V003 pin is kept (`rederive_at_build.not_reread`).
4. **Slots V003.** Only `ngc3198_slots` and `notes_block_for_manifest` were read and used. They are written into the list as B1 and B2 require, and A141 found no velocity field in the file. No other slots key was printed.
5. **Read beyond A133-A161.**
   - V006 A163 is the commission. A164-A169 headings and A168-A169 were read: A168 L1519 binds a phase1 successor's sha into the classifiers, and A169 names roster builder c2v005 and RUNBOOK_V002_C2V005.
   - I also read those two files, in the named `runbook_v002_c2/` folder, at their A169 shas (653ced76, b34f294a), for the N2 sites.
6. **V006 grew during the build.** It is now `13fc80c2` at A169. The list records that sha and the line numbers it cites. Entries append below A157, so the cited lines are stable.
7. **Additions beyond the four items.**
   - code_files gains phase1_c2v003b (EXISTS_NOT_ADOPTED; the A163 CHECK and N2 cite it).
   - The s0 launch kit entry records A161's 8-hex adoption and keeps its full-sha rule.

**Open (not commissioned in A163; unchanged):** Claude4 0223 N4 (A16.4 wrapper check), N5 (null_direction_rule), N6 (query_manifest value annotation), N7, N8, N10 (other CX2V006 preconditions), N11, N12 and N13.
