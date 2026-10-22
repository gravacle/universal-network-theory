# REVIEW_STAGE_SUCCESSOR_V001: R-G remainder on stage_successor_gal_c2v005 (G1 verification, G2–G5, synthesis)

Reviewer: Claude2 workflow subagent (R-G remainder, reassigned by V004 addendum A38 §4). Written 2026-10-18T04:20Z (`date -u`).
Object: `claude_artifacts/stage_successor_gal_c2v005/` — driver v009-GEO `237ef3d41daf4d99b0aafed3e90b27b095a741a9f66ea06ea34f3e44876d47bb`, schema V005 `f9b8d48e…042a`, 11 gal_c2v005 stages, configs, `deciding/`. HASHES.txt `c01ce6ddddc7a960df964df67c1c09d35cb5b2eb1f15cfcd2c37834658d48944`.
Labels: DECLARED-PREMISE / HYPOTHESIS / FORMAL-RESULT / TESTED-POSITIVE / TESTED-NEGATIVE / UNTESTED. No GR answer is used anywhere; nothing here asserts what a D response must look like.

## Verdict

**PASS_WITH_FINDINGS — 0 BLOCKING, 2 SHOULD-FIX, 6 NOTE.**

- **G1 (Claude4 PASS) — CONFIRMED from bytes**, with an independent re-derivation of every load-bearing custody/minimality claim.
- **G2 — PASS (TESTED-POSITIVE).** Over an exhaustive 5610-case single-field battery, the only admission widened is DDO154 · PER_CALL · the 5 geometry fields; each lock alone restores gal_c2v004 behaviour exactly; no extra field, galaxy or member can be admitted by widening either lock alone.
- **G3 — PASS on everything executed; remainder UNTESTED.** The geometry producer is AST-identical v003c = v008 = v009-GEO. Deciding (i) re-compared independently: 232/232 arrays and 360/360 columns equal to the saved chain. Deciding (iii) re-compared independently: 234/234 arrays equal v009-GEO vs v003c through fs_columns_03, numeric leaves differ only in timing/pid. Rotation, feedback and column mean have **never executed at D ≠ 4.04** in either driver.
- **G4 — PASS (TESTED-POSITIVE).** NGC3198 configs differ only in `schema/generator/note`; every stage admits/refuses them identically after T; NGC dry-run reports equal after T except the +9 needle-line shift.
- **G5 — SHOULD-FIX carried into v010; deciding test DT-G5 specified below.**

Reading for root: v009-GEO is admissible at D = 4.04 (TESTED-POSITIVE). At D ≠ 4.04 it equals v003c bitwise as far as any call has run (TESTED-POSITIVE through fs_columns_03); use at D ≠ 4.04 stays gated by the A32 hull-bracket rerun, which DT-G5 step 1 is.

## Records read (sha256 from bytes)

| Record | sha256 | Note |
|---|---|---|
| V004 addendum (open) | `e2d9c4271011cce6…2672` (667 lines) | Its first 44110 bytes hash to `eade847c…0127` = Claude4's snapshot: **append-only since Claude4's read (TESTED)**. Sections used: A23 L221–250, A29 L438–460, A30 L462–479, A32 L518–553, A38 L632–667 |
| INTERFACE_GAL_C2V005.md | `28846580…335a` | |
| Claude4 G1 report / JSON | `c329be3e…bd4` / JSON pins that sha | 46/46 files of its §9 manifest verify from bytes |
| (i) result.json | `f33eb362f5311a76…` = finish | driver 237ef3d4, spec 4ac5527a |
| (iii) v009-GEO / v003c result.json | `77691e6c…` / `d887cab5…` = finish | spec 2029f26a |

## G1 — verification of Claude4's PASS (TESTED-POSITIVE)

Independent of Claude4's scripts (`scripts/g1_verify_v001.py` → `outputs/G1_VERIFY_V001.json`):
- HASHES.txt: 2918/2918 equal (`shasum -c`); the 1344 unlisted files are all under `check/`; no listed file is newer.
- All 11 stages: v005 = v004 outside the 4-line header and the shared admission block; the block is one text across all 11 (`31c7c55c…`, v004 `3c6dffba…`, matching Claude4). Inside the block the logic change is exactly SCHEMA/SCHEMA_NAME, the new PER_CALL_GEOMETRY constant, and the PER_CALL rule = old rule + one appended conjunct (string-checked); the other changed lines are inside the docstring.
- Driver hex64 literals v008 → v009-GEO: 15 removed / 15 added, all within {gal_c2v004 stage, schema V004, c2v006 config} → {gal_c2v005, V005, gal_c2v005 config}.
- All 17 registered diffs (16 in `diffs/` + `driver/DIFF_V008_V009.diff`) reproduce byte-for-byte with `diff -u`.
- Three-way merge (git merge-file --diff3, EXT 999331af / base v008 / GEO): exactly 1 conflict (docstring, L2–27). The output is byte-equal to Claude4's `MERGE_DIFF3_EXT_BASE_GEO.py` (`bcd9f848`). The EXT pin delta (+1) and the GEO pin delta (15) are disjoint.
- Not re-run by me (accepted from Claude4's byte-verified outputs; disclosed): generator re-runs, the AST 112/114 comparison, the EXT dry run `EXT_DRY_ROUTE_A.json` (`10e77f14`).

## G2 — stage admission logic

**FORMAL-RESULT.** The new refusal predicate is `old ∧ ¬(A ∧ B)`, where A = n ∈ PER_CALL_GEOMETRY[galaxy] (stage constant) and B = n ∈ schema.per_call_geometry[galaxy].fields (pinned schema). So refusals can only shrink, and only where A ∧ B holds. A is keyed by `cfg['galaxy']`, contains DDO154 only, and is a tuple with exact membership, so A is a hard upper bound on any widening. CONDITIONAL cannot route around this: DDO154 refuses every CONDITIONAL status, and NGC3198 has no A.

**TESTED-POSITIVE** (`scripts/g2_admission_battery_v001.py` → `outputs/g2/G2_ADMISSION_BATTERY_V001.json` `745214ae`). Method:
- Only the admission-block text from the pinned stage bytes is executed; no stage module runs.
- 5610 cases = 3 galaxy contexts (DDO154; NGC3198; NGC3198+GL10) × 34 fields × 11 statuses × 3–5 value kinds.
- Each case runs under v004 and under v005, and refusal texts are compared after T.

Results:
- **25 cases differ, all DDO154 · PER_CALL · the 5 fields.** In 20 of them v004 refuses and v005 admits, returning exactly the input value. In the other 5 the value is the literal sentinel `PER_CALL`: both versions refuse, and only the reason text changes (see N4).
- 0 crashes. Admissions: 233 under v004, 253 under v005.

Lock ablations, each compared with v004 over all 5610 cases:

| Variant | Cases differing from v004 |
|---|---|
| stage constant emptied | 0 |
| schema without `per_call_geometry` | 0 |
| schema lists 4 extra fields (incl. inclination, n_phi, distance_Mpc, n_columns) | 25 (the same 5 fields only) |
| schema declares NGC3198 with all fields | 25 (the same, DDO154 only) |
| constant gains 2 DDO fields + NGC entry, schema unchanged | 25 (the same) |
| schema `fields` as a string | 10 (a subset; substring semantics bounded by the constant) |

A combined DDO154 config (5 geometry fields PER_CALL, every other field the literal) is refused by v004 with exactly those 5 fields named, and admitted by v005.

**Driver-level admission (FORMAL).** Nothing is widened. The driver's own config loader requires V005 (c2v006 configs are now refused: a narrowing). `producer_pin` now excludes gal_c2v004 producers (a narrowing; INTERFACE UNTESTED-3 / Claude4 N9).

## G3 — per-call geometry semantics vs v003c `derive_geometry`

Code identity (`scripts/g3_semantics_v001.py` → `outputs/G3_SEMANTICS_V001.json` `445ccb8f`; TESTED-POSITIVE):
- `geometry_active`, `_pinned_json`, `derive_geometry`, `_write_bytes_x` and `geometry_inputs` are text- and AST-identical across v003c ed326130, v008 and v009-GEO. So are `GEOMETRY_PINS`, `PROFILE_NAME` and `KPC_M`.
- `geometry_config_fields` (new in v008) is identical in v008 and v009.

Deciding (i), D = 4.04 (`scripts/g3_recompare_i_v001.py` → `G3_RECOMPARE_I_V001.json` `a89a82e1`; TESTED-POSITIVE):
- This is my own comparator, stricter than the driver's: every array in dtype, shape and bytes; every column JSON on all numeric leaves; the saved map is read from the pinned driver text.
- 232/232 arrays equal (offset, fs/le1/le2/le3 rotation and feedback).
- 360/360 columns equal on all numeric leaves; the fs_columns_01 failure set is {5–9, 45–50}, as saved.
- le3 column-mean rows (12) equal.
- Agrees with A30 and with Claude4's G5 partial (958 arrays, wider scope).

Deciding (iii), D = 4.1115 (`g3_compare_iii_runs_v001.py` → `G3_COMPARE_III_RUNS_V001.json` `d6c7cd6a`; `g3_numeric_leaves_v001.py` → `9c42d685`; TESTED-POSITIVE):
- Identical file sets, apart from the v009-only configs/probes and the attempt token.
- 234/234 arrays byte-equal: route A 46, body 21, offset 27, columns 140.
- Every differing numeric leaf is `elapsed*`, `pid`, `started_unix_ns` or `ended_unix_ns`. The non-lineage string differences are only the delivery channel: v003c passes `COEFF_SHA/OFFSET_SHA/SOURCE_SHA` as stage globals, v009 passes them as config fields.
- The 4 per-call geometry inputs are equal after run-dir substitution. The profile is byte-identical (`177e2fd0`); the monotone source (06651697 vs b4200945) and the binding differ in raw sha only through the embedded run path.
- Both runs stop at `09_fs_rotation`, stage L224 "Missing complete72 successful columns".

Semantics at D for the stages that never ran:
- **rotation_v001 (TESTED-POSITIVE, run mode).** Its per-call config (monotone b4200945 PER_CALL, outer edge 14.351842439149376 PER_CALL) was admitted, and `check(SOURCE,…)` passed before L224. Rotation arithmetic at D: UNTESTED.
- **radial_truncation (TESTED-POSITIVE, in-process).** The function text from all 5 truncating stages, applied to the run's per-call profile and monotone edges (they are equal), gives J = 18 = last edge. That is the base expression `sqrt(edges[-1])`. outer/4.04-literal = 1.0176980198019803 = D/4.04.
- **column mean (TESTED-POSITIVE, in-process; never run).** Its own gal_c2v005 admission accepts the run's registered probe config at D (producer-pin extra check stubbed; disclosed), and `check_binding` PASSES against the per-call binding. The binding has distance 4.1115, source_profile = run profile, and query rows ×1.01769801980198.
- **Configs (TESTED-POSITIVE).** Every PER_CALL value in the run's stage configs equals `geometry_config_fields` re-evaluated on the run's own files.

## G4 — NGC3198 configs keep their semantics (TESTED-POSITIVE)

`scripts/g4_ngc_semantics_v001.py` → `G4_NGC_SEMANTICS_V001.json` `18231471`; `g4_explain_residue_v001.py` → `G4_RESIDUE_V001.json` `efa9accb`. No NGC data file was opened and no NGC value was printed; comparisons are by hash.

- **Configs.** For DDO154, NGC3198 and GL10, c2v006 → gal_c2v005 changes only the top-level keys `generator`, `note` and `schema`. `fields` (34), `galaxy`, `format` and `member` are canonical-equal.
- **Stage admission.** All 11 stages × 3 configs, v004 block on c2v006 vs v005 block on gal_c2v005, with each stage's own consumed constant: identical outcomes and identical refusal texts after T. All of them refuse the raw galaxy config, as expected, because the per-call slots are unfilled.
- **NGC dry-run reports.** NGC_A2F10_TEMPLATE, GL10_TEMPLATE and NGC_SEED, v008 vs v009, after T and after mapping the sha of each probe-config pair that is equal after T: the only JSON residue is `needle_lines` +9 in NGC_SEED (Claude4 N3, confirmed). The PLAN.txt residues are stage basenames gal_c2v004→gal_c2v005 and hex prefixes.
- **D = 14 Mpc.** Both NGC D=14 specs are refused ("UNSUPPORTED NGC geometry"). At stage level, NGC PER_CALL on the geometry fields is refused even when the schema declares NGC3198 (G2 ablation).

## G5 — the v010 merge hazard and its deciding test

### Facts

**TESTED-POSITIVE unless marked:**
- Prep v007 `ac905597`, v008 `bb05f974` and v009 `b4b27a1d` differ only at L130 (budgets 80/96/120).
- `C` is read inside the function at prep L63–64. Line 19 (`COEFFICIENT = C/…`) is bound at import, before any patch.
- The driver applies module patches by resolved path, after the module's code runs (v009:553–590). The same mechanism therefore serves v007, v008 and v009 (FORMAL).
- The registered C5 and C6 route-A requests (v009-EXT) already ran prep v009 + `LOCAL['prep']` + a module patch {COEFFICIENT, COEFFICIENT_SHA}. Only the key `C` would be new in the v010 combination.

**Reachability today:**
- v009-GEO at D ≠ 4.04: prep v007 (≤ 80 nodes) has executed (A2F10, 72 nodes). Prep v008 + C (81–96 nodes) is reachable and has never executed (FORMAL, v009:2168–2176).
- v009-EXT is BLOCKED at D ≠ 4.04 by the gal_c2v004 probe: FORMAL from G2, TESTED in Claude4's EXT dry run.
- v010 makes prep v009 + C (97–120 nodes, G5/G6) reachable, with no v003c reference because v003c's budget is 96 nodes.

**Observed in the records at review time (root has not registered it):**
- C6 at 4.04 (`runs_ext/KMAX_A2F10_C6R3_RUN_V001`) ended FAILED_AT_STAGE in route A: `NO_SUBLUMINAL_CIRCULAR_PRESSURE_BRANCH` (receipt `5d6507d7`, utc_end 04:10:25Z).
- C5 is still in progress.
- So no completed 4.04 chain exists yet on either G5/G6 grid.

**Comparator defects for any rerun** (verified from bytes `compare_distance_v009_v003c.py` L43/L81; first found by Claude4's G5 partial):
- The substring mask `'time'` hides the model output `prediction.columns[].streaming_first_moment_intensity_times_m_s`. The key is present in the (i) le3 column-mean record.
- `'utc'` masks every `*outcome*` key.
- `ended_unix_ns` is unmasked.

### DT-G5: the deciding test

This test is for root; nothing has been launched. Every call sets the six `*_NUM_THREADS` variables to 1 and uses the A32 hull bracket block: every fs entry is [1.5125e8, 3.17625e8], in rule mode via `fs_absolute_overrides`.

**Preconditions:**
- **P1.** v010 is written (GEO pins + EXT features + the F-A fix per A30), and its sha is cited. If N > 1 is used for route A, v010 also carries the V8c-F1 fix (A23).
- **P2.** v010 passes the dry-run identities of Claude4 N8:
  - against GEO, with the EXT features absent;
  - against EXT on the C5/C6 specs, after T;
  - the NGC seed, with needle-line normalisation.
- **P3.** Comparator v002 uses exact-key timing masks, masks `ended_unix_ns`, and never substring-masks model keys. Its fixture suite adds a 1-ulp change to `streaming_first_moment_intensity_times_m_s`, which must FAIL.

**Step 1 — completes deciding (iii), the A32 rerun; 72 nodes, prep v007.**
- Spec: a93c95b9 + D 4.1115 + the hull block. Run v010 and v003c.
- PASS: comparator v002 gives PASS_BITWISE_EQUAL_PER_CALL_OUTPUTS, including fs/rfs/le rotations, feedbacks and every column mean. This is the first execution at D of the rotation, feedback and column-mean stages.

**Step 2 — v010 against EXT at 4.04 on the Jacobian grid G (G5, or G6 once a 4.04 G6 chain completes); prep v009; the declared N.**
- Spec: the C5 (or C6) spec + the hull block, run under both v010 and v009-EXT.
- PASS: all arrays, speeds and column-mean rows are bitwise equal after T (stage lineage gal_c2v004 → gal_c2v005).

**Step 3 — the never-executed combination: G at D = 4.1115 (and 3.98107 if a central difference is declared).**
- There is no reference above 96 nodes, so PASS needs all of:
  - COMPLETED, with route A CONVERGED;
  - a request-diff on the run records against step 2 that shows only the declared geometry deltas: prep patch key `C`; PER_CALL geometry fields only to their consumers; the 4 geometry files;
  - those 4 files byte-equal (after <OUT>) to v010's step-1 files, since the geometry inputs are grid-independent;
  - radial_truncation J = last, and `check_binding` passes;
  - no stage refusal.
- The D response v(G, D) − v(G, 4.04) is recorded as a measurement and does not gate the test. Comparing it with step 1's 72-node response is a numerics diagnostic only (cf. Claude4 G3 F1, the fixed 1/kpc box). No threshold on its value or shape is prescribed.

**How to read a failure:**

| Failure | Reading |
|---|---|
| Step 1, GEOMETRY_INPUTS or SPEC | port defect |
| Step 1, only rotation/feedback/column-mean arrays | per-call delivery or stage-lineage defect at D |
| Step 2 | merge defect, independent of D |
| Step 3, an undeclared request delta | merge-interaction defect |
| Step 3, refusal, non-convergence or NUMERICS_LIMITED | TESTED-NEGATIVE for D ≠ 4.04 at G under v010 (a record, not a physics reading) |

**Until DT-G5 passes,** v010 should refuse D ≠ 4.04 above 80 nodes/axis, or above the node count step 3 has covered. That also closes the 81–96-node prep-v008 + C path that is open in v009-GEO today.

## Findings (most severe first)

| ID | Sev | Grade | Finding |
|---|---|---|---|
| S1 | SHOULD-FIX | FORMAL + TESTED (planning); run UNTESTED | v010 makes D ≠ 4.04 reachable on G5/G6 (prep v009 + C), and v009-GEO already reaches 81–96 nodes (prep v008 + C). Neither has executed. Deciding test: DT-G5; gate as above. Same as Claude4 G1 S1, plus the 81–96 sub-case and the C6 fact. |
| S2 | SHOULD-FIX | TESTED (code + record) | The (iii) comparator's substring timing mask hides a model output (`…intensity_times_m_s`) and every `*outcome*` key, and leaves `ended_unix_ns` unmasked. Fix it before the A32 rerun (DT-G5 P3). Credit: Claude4 G5 partial; verified here. |
| N1 | NOTE | TESTED | At D ≠ 4.04 rotation/feedback/column-mean arithmetic has never executed in either driver. Run mode stopped at fs_rotation L224, after its per-call admission and monotone pin check had passed. Column-mean admission and `check_binding` at D pass in-process. Deciding test: DT-G5 step 1. |
| N2 | NOTE | TESTED | Per-call admission is value-unconstrained: a float `1.5` is admitted for `source.profile`. Value checks rest on the consumers and on the driver. Consistency of D across stages is a driver property: one `derive_geometry` per call (FORMAL). No stage checks it; for example, the column mean does not compare binding.distance with the profile. |
| N3 | NOTE | TESTED | At D, non-consumer stage configs carry 4.04 literal geometry values, e.g. rotation_v001 `source.profile` = f5becd45 and reference `observation.binding` = f42c7c65. They are inert (unconsumed), but a config record shows mixed geometry. |
| N4 | NOTE | TESTED | For the 5 geometry fields, a PER_CALL whose value is the literal sentinel `PER_CALL` is still refused, with the text "(PER_CALL value)" in place of v004's "(PER_CALL status on a … field)". This is consistent with INTERFACE AN, which covers non-geometry fields only. |
| N5 | NOTE | TESTED | The lock types are lax but bounded. A string `fields` gives substring matching, capped by the constant. A malformed `per_call_geometry` would raise AttributeError rather than a refusal. Under the schema sha pin neither can be reached. |
| N6 | NOTE | TESTED | V004 addendum: append-only since Claude4's read (`eade847c` is a byte prefix of `e2d9c427`). Nothing in A33–A38 alters A23/A30/A32. |

The other Claude4 partial candidates were not re-verified here and are not adopted: G2-partial N6 (sentinel breadth) and N7 (D range). Claude4's G3 F1/F2 (k-box numerical component; tail-corrected numerics pinned to 4.04) are a separate review and are cited only as context for DT-G5 step 3.

## Disclosures

- **Writes.** Everything is under this directory, except 4 listing files that I wrote early to the session scratchpad (`ondisk.txt`, `listed.txt`, `v9.lst`, `v3.lst`). They are not deleted, per the no-deletion rule. `outputs/g2/cfg/` holds 30164 content-addressed synthetic battery configs, each written once.
- **No launches.** No driver dry run and no stage module execution took place. In-process work was limited to:
  - exec of the admission-block text and of the single functions `radial_truncation`, `check_binding`, `_posint` and `geometry_config_fields`, extracted from pinned bytes;
  - read-only `np.load(allow_pickle=False)` on the registered runs.
- **Run settings.** nice -n 10; at most 1 process at a time; the prescribed python with `-I -B`. One edit to my own `g1_verify_v001.py`, `g2_…`, and `g4_explain_residue_v001.py` during the work (a docstring-range fix, a guard on a non-ADMIT row, an output-path fix); the shas below are the final bytes.
- **NGC3198.** No NGC target or observation file was opened. NGC configs and plan reports were compared by hash only. `~/.codex` was not touched.
- **Reuse (all verified from bytes):** Claude4 G1 outputs (46-file manifest, all OK); the EXT dry-run result `10e77f14`; Claude4's V004 snapshot `eade847c`.

## Files (sha256 from bytes; relative to this directory)

```
6a153721945cb18df73d3b167df6295dd2435f6f9f72baa675f9020b02adc44a  scripts/g1_verify_v001.py
93d397603e64680277b4b7ddecab1419b90dbc327754419e77b7a210b4ef19c3  scripts/g2_admission_battery_v001.py
ed6dfb60d12f4ba849e012d3faa476e902e0c404c0bebd0cf47a222ef32c1e2f  scripts/g3_compare_iii_runs_v001.py
8b227bd0041096e9b579342404fb60c6434c1bb72592d5e0ab6acf80d21edede  scripts/g3_numeric_leaves_v001.py
ccc6b342d9fc840e728487c508dc91b3cdc56e27ae4487c07af476297ae9d3c6  scripts/g3_recompare_i_v001.py
9552e8e9b8221d140da1d2da193d91bce7b226bc9c50e7aacfb7c39bc6a2b774  scripts/g3_semantics_v001.py
f2cecfca47d26212e8384b5033511124ef986924df68bf31e359e7494f689050  scripts/g4_ngc_semantics_v001.py
5a12a4255cba61ed27c503d746eea6f835456f30fd0efea913978d5f34d3ae4c  scripts/g4_explain_residue_v001.py
8eb948164e762dca7d5c95cdb69a56fa7be3e96d10ec97af1d86cdafb0ba26e6  outputs/G1_VERIFY_V001.json
745214ae6083a94cb1ca13d215b9b2fb2e23c769af713e0aa65ab12cf724abd1  outputs/g2/G2_ADMISSION_BATTERY_V001.json
44ae16ffe713818778869d47851475a554c1485e64f5bd5da42ce0c87dd766ee  outputs/g2/schema_variant_extra.json
7bc51e5471273ee5448a67f86e20d3add48c5b163af0eb6204a99c67f734a5d2  outputs/g2/schema_variant_ngc.json
bd8ef6ce7befd4f8138d541c9f53c088589b668ff80a84d9c10e7d3fa05d8935  outputs/g2/schema_variant_no_pcg.json
50d37d889c3711b702813bbf057769c8edac219da620f694214c951a7d8601d8  outputs/g2/schema_variant_str.json
d6c7cd6ac9d1800451ece779e8cff842aa64314f8d4e4bfb6b9a2c4f0a10f104  outputs/G3_COMPARE_III_RUNS_V001.json
9c42d68504fb9f1a63fe563885c3144a7c7346ba90011a5c96190af45f341e27  outputs/G3_NUMERIC_LEAVES_V001.json
a89a82e166751a2df2947d4f3622de177139ff7c96ff4e6c2b16e04dd3979bef  outputs/G3_RECOMPARE_I_V001.json
445ccb8f1b9139d6bb3edc236e54c07f67c67d49fd9627aa16dc7f8910b4c5b0  outputs/G3_SEMANTICS_V001.json
1823147154b48ba979dd285c44861ed67441f76fcb545fb7ac7045a9030bdc21  outputs/G4_NGC_SEMANTICS_V001.json
1823147154b48ba979dd285c44861ed67441f76fcb545fb7ac7045a9030bdc21  outputs/G4_NGC_SEMANTICS_V001.rerun_for_residue.json
efa9accbef9dbb31734eec63a5127c3540834d545e9b7a202cf8cd46ff5eafc1  outputs/G4_RESIDUE_V001.json
bcd9f84816ae5fbf2e1c6f19c9797dd9fb7cb983ed2b5f962c62d4e6b83d18ff  work/merge/MERGE_EXT_BASE_GEO.py.txt
f8e4770106abb83df5e658e91edc5593198fe87f0600ee5d1946f22415902f28  work/merge/base_v008.py
999331afd604dd9829aa8f389f43cdb87603d03412d52ba09712226787f18db6  work/merge/ext_999331af.py
237ef3d41daf4d99b0aafed3e90b27b095a741a9f66ea06ea34f3e44876d47bb  work/merge/geo_237ef3d4.py
```
