# Classifier B (lane Claude2), build c2v005: the A190 fix round

Claude2 subagent build, 2026-10-20T02:17:29Z (`date -u`). Root ruling V006 A190 on the c2v004 triage. Successor of `build_c2v004/` (`fe5bc96a`): its source files were copied, then changed only by new files; c2v004 is untouched.

**CLI (unchanged, A's interface):** `<codex python3> -I -B classifier_b_c2v005.py BUNDLE.json OUT.json` (OUT is created exclusively). Entry point `classify_bundle(bundle_path) -> bytes`. Stdlib only.

**Barrier (A190 ruling 1).** The producers' bytes are the contract for their records, so the builder read the producer modules and records below. The barrier stays in force against classifier A's code, suite and outputs: none was opened. A's printed forms for rulings 2 and 3 were taken only from the contract and README texts and the four `TRIAGE_c2v00*.json` descriptions.

## Producer bytes read (sha256 from bytes; read by line range and grep, never executed)

| file (under `claude_artifacts/`) | sha256 | what was read |
|---|---|---|
| `freeze_score_readiness_cx3/v003g/prediction_freeze_c2v003g_cx3v001.py` | `48a1e48a5230fff346705c338da30a8ee53a8643193dbe4616c25e61eab3d405` | `score_after_freeze` L4114-L4303 with `_ladder_row` L4011-L4031, `_score_members` L4034-L4052, `_alternative_score_scope` L4057-L4076, `_score_members_on_rows` L4078-L4089, `_band_rows` L4097-L4111; `_authorized_row_registration` L1788-L1798; `_invalid_registration_ok` L1919-L1934; `_registered_rows_ok` L1937-L1950; key sets L204-L231; manifest writer L3755-L3783 |
| `phase1_c2/phase1_c2v003b.py` | `7d891ff7d81b0e9d103707d79c7a057cedc6dc1e893a0f4e9372a51d0b796dd4` | MODULE L99, BAND_LABEL L114, the L1 record L942-L947, the AT1 record L1287-L1292 |
| `phase1_c2/phase1_c2v002.py` | `d64351ecc06c61e99e2d7253c5d4311617fc1f64d34d37523102ed32720a6754` | MODULE L48, BAND_LABEL L63, the L1 record L838-L843, the AT1 record L1043 |
| `stage0_successor_c2/prediction_freeze_c2v003g_stage0_c2v002.py` | `d260ee308a7f215176cab1fff51e94cb52c7fc6cdd64aa4da48c66f8091820f0` | its `score_after_freeze` alternatives L4829-L4855 (equal to v003g's) and `_alternative_score_scope` L4611-L4630 |
| `ngc_ntest_eval_cx/out/K32_COMPARE_COMPLETE_V001.json` | `6f095f64a1f1acc2ad2910af12f645e18acdf16fb62bfd936386a61c47ef30e9` | hashed; byte-copied into the real-bytes suite cases |

## Status

- **TESTED (own suite).** 327 synthetic target-free cases: 93 MUST_PASS, 234 MUST_FAIL, 1246 hand expectations.
  - Run twice (`suite/run1`, `suite/run2`): 327/327 in each. The two results files are byte-identical (`ed2e29d739125c1ff5e5d6f07f28f0b50b16e00aa0705d2ab894ccb53dc522c1`).
  - 0 schema errors under `OUTPUT_SCHEMA_C2V005_DERIVED.json`; pass-2 bytes equal pass-1 bytes, and CLI bytes equal the in-process unpatched bytes, on all 327.
  - Run as shipped (no seam): 16 cases on the real compare, d260ee30 and the bound tool values. Seam cases: 311; 299 show TSR_FLAG_TABLE_MISMATCH when run unpatched, 12 are refusals or NO_CLASSIFICATION.
  - Every stand-in producer record is in its producer's form (below), so the suite's honest bundles are honest-form bundles.
- **TESTED (discrimination, `work/discrim/DISCRIM_C2V005.json`).** c2v004 on the same bundles and seams fails 77 of the 80 new cases (B421, B425 and B436 are controls that hold in both) and 126 carried cases: the footprint of RC3, RC5, RC7 and RC8 on producer-form stand-ins.
- **UNTESTED:**
  - agreement with classifier A (the agreement run is next);
  - the seeded fuzz: `fuzz_c2v004.py` writes c2v004's stand-in forms and was not re-run;
  - any real manifest or score (M-12).

## The eight B_DEFECTs (producer line citations; classifier hunks)

**RC3 score alternatives[] entry form** (`check_alternatives`, L1253-L1299). From v003g L4273-L4299 (d260ee30 L4829-L4855): every entry other than the PRIMARY has role `NON_PRIMARY` (L4276; the A13 recorded alternative L4297); `scoring_scope` is written only on STAGE0_GRID_OUTER (L4277-L4279, `_alternative_score_scope` returns None elsewhere, L4059-L4060); `members` only on a scored evaluated entry (L4282-L4290), a note on an unscored one (L4291-L4293).
- A role that is not the string NON_PRIMARY (missing, null, ALTERNATIVE, ...) is a field defect.
- STAGE0's scoring_scope must be an object whose query_ids are Q36-Q43; its absence elsewhere is no defect.
- members is required (a list) only when scored is true.
- The failing fields are joined by a bare comma (ruling 2, RC3c).
- Cases B393-B400, B363, B364.

**RC4 prescore synthetic score, and DOWNSTREAM** (`prescore_score` L2649, `synthesize_score` L2676, `_syn_*` L2925-L2989). Built as `score_after_freeze` builds its output (L4190 query_ids, L4218-L4219, L4225-L4228, L4261-L4299), with a target-free stand-in pair (`SYN_PAIR`, L297) that no prescore output depends on.
- Rows by the producer's ladder (L4011-L4031) and registration rule (L4040-L4046): a non-null frozen registration makes INVALID_AS_MISS with the frozen reason; otherwise VALID, or UNEVALUATED_OR_REFUSED when row_valid is false or the speed is null. row_valid false alone never makes INVALID_AS_MISS.
- Envelope and sensitivity rows by `_band_rows` (L4097-L4111) from `pointwise_envelope[]` and `sensitivity.per_query[]` (both phases); the envelope label is the frozen rows' label (`_pointwise_envelope` L2072-L2086 writes one label on every row).
- Alternatives from `{primary, declared}` in the RC3 form; an evaluated one scored from `alternative_results[name].members` (STAGE0 on its scope rows, L4078-L4089); A13 recorded alternatives when `headline_conditions` is present (L3782-L3783, L4295-L4299).
- A read or operation that fails raises as the producer's does (KeyError, TypeError, IndexError, OverflowError for V-F3, StopIteration for L4228's `next()`): FIELD_DEFECT_OUTSIDE_ROWS `synthetic score could not be built from the frozen manifest: <class>`. The score is then read as missing (RC4D): `score output missing or malformed (None)`, and no detail that needs the score.
- c2v004's encodings are refused: an alternatives list or name-keyed object, lo_km_s/hi_km_s or query_id row keys, defaults for member_valid or row valid, a fixed envelope label.
- Cases B372-B383, B401-B409.

**RC5 frozen row_registration, with RL9** (`_reg_entries` L402, `reg_info` L418, `classify_row` L1138-L1200, `twin_registration` L1094). From L1788-L1798, L1919-L1934, L1937-L1950: a list aligned with query_ids; null for a valid row; for an INVALID row exactly `{status: INVALID, reason, registration}`, registration null for a built-in reason or the gate pin `{path, sha256}` for a gate reason.
- The gate of an INVALID_AS_MISS row is that pin's sha (lower-cased, V-F1), only when the entry is in the form and its reason equals the row's registered_reason.
- Any other entry is unreadable: the row reads `gate registration of an INVALID_AS_MISS row not readable from the frozen manifest`, and its reason is unknown (whole I_per_reason map blanked, RC14). PB-3's tolerant reader is withdrawn.
- A twin's registration (STAGE0 included) is read from the same 43-row list by query id (L4086-L4087). c2v004 read an 8-entry list for STAGE0.
- RL9 needs no change: a readable gate missing from the list still blanks only its own reason.
- Cases B361, B366, B367, B408, B410-B416.

**RC7 L1 band label and rows** (`band_column` L1605-L1647, `_l1_rows` L2991). From 7d891ff7 L942-L947 and d64351ec L838-L843: schema PHASE1_L1_C2V001, module the pinned tool's MODULE, label exactly `PHASE1_LINEARISED_ADMITTED_SET_PROJECTION_TRUNCATED_LOWER_BOUND_ON_SPREAD_NOT_A_TIER`, rows under `rows`. Anything else is L1_RECORD_DEFECT on all 43 rows, with no fd_noise_not_bounded entry. PB-7 (band_rows) is withdrawn. Cases B368, B417, B418.

**RC8 AT1 at0** (`parse_agree` L2309-L2312). From 7d891ff7 L1287 and d64351ec L1043: `at0` is the list of the two AT-0 outcomes in every outcome. Missing or not two strings: AGREE_RECORD_DEFECT, word OUTCOME (checked after the outcome value). Cases B422-B425.

**RL5B null-phase STAGE0 stop in prescore** (`prescore_output` L2634-L2642). The score-mode rule (c2v004 RL5) applies in prescore: a null phase reads the STAGE0 record, and a missing or malformed one prints the STAGE0 alternative's stop beside PHASE_MISMATCH. C4-3 is withdrawn. Cases B391, B426, B427.

## Ruling 2: the seal candidate's printed form (from the triage descriptions)

| item(s) | B's printed form now | hunk; cases |
|---|---|---|
| RC07, RC8, RC6 | presence and type checked separately; all `missing` messages first, then type messages, in field order; an absent score_status, within_error or status prints both | `row_messages` L1109; B428, B429 |
| RC08, RL2 | a row status outside VALID, INVALID, UNEVALUATED_OR_REFUSED is `status wrong type` | `row_messages`; B430 |
| RC12 (c2v001), RC10, RL5B | the null-phase STAGE0 stop (score mode since c2v004; prescore now) | B391, B427 |
| RC14 | an unreadable registration contributes no reason: the whole I_per_reason map is blanked | `classify_row`; B361 |
| RC06, RC5 (c2v002), RL6 | MEMBER_FINISHED for every finished-row failure (status, receipt time, step-4 start, before_step4; null only on the exception path); MEMBER_BEFORE_STEP4 only for an unfinished row with before_step4 set | `_stage0_facts` L1497-L1510; B365, B434-B436 |
| RC12 (c2v002), RL3 | a flag record that fails its exact keys prints only `flag record missing or malformed (%s)` | `check_tsr` L871-L876; B370 |
| RC13 | a freeze manifest that is not an object also prints `manifest reference_member / members unreadable` | `check_score` L988-L991; B431 |
| RC15 | L1 bytes not matching the pin read L1_SHA_MISMATCH; order: tool pin, load status, record form, header sha | `band_column`; B419-B421 |
| RC16 | a v002 failing entry with a category or flag outside v002's reads FAILING_KEYS_V002 | `_failing_word` L2374-L2378; B432 |
| RC2b, RC2R | candidate (i): (c) iff the schema differs or the TRUNCATION_SHAPE list is not a list of objects; else (d) unless one record with integer ordinal 15; (e) independently iff the other list is not exactly []; a non-object compare prints `compare unreadable (<status>)` | `check_tsr` L828-L852; B371, B384-B390, B433 |
| RC3c | bare comma | B398 |
| RC4b, RC4D | the score-missing detail after a failed synthesis | B372-B383 |

## Ruling 3: classifier A's printed form

- **Field-map partial rename** (c2v001 RC11, c2v002 RC9, c2v003 RL1; `apply_field_map` L561-L627). A role's renames run in order, each over its containers in document order. At the first container that already holds the target key, the rename is refused there and nothing further of that role is renamed. Other roles are unaffected. Cases B392 (B113's input: Q01-Q10 renamed; Q11 kept; Q12-Q43 `sigma_ratio missing`), B437.
- **Non-list `pins.input_files`** (c2v002 RC11, c2v003 RL4; `check_tsr` L855-L868). A string or an object is iterated as A iterates it and holds no pin, so every input-files requirement prints `not pinned`. A number, null or a missing key stays `manifest pins.input_files unreadable`. Cases B369, B438, B439.

## Choices, for the agreement triage

- **C5-1.** The synthetic score reads only the fields that build what the classifier reads. A field the scorer reads only for an output the classifier never reads (a member's role and evaluated, admitted_region, input_bindings, band_scope, coordinates, the sensitivity status, label, reference speed and max delta, member_evaluation) is not read. A manifest lacking one is not a synthesis failure in B.
- **C5-2.** Prescore attempts the synthesis on a manifest that did not load as an object. The construction's first read raises TypeError, so that detail and the score-missing detail print beside `freeze manifest missing or malformed`.
- **C5-3.** A scoring_scope on a non-STAGE0 entry is not checked (the texts and triage say only that its absence is no defect).
- **C5-4.** A readable gate pin has exactly the keys `{path, sha256}`, as v003g L1922 requires.
- **C5-5.** A malformed flag record keeps its own input-files requirement (the record's bytes' sha); only its field conditions are dropped.
- **C5-6.** B369 (B243's input) prints three `not pinned` details: the record's own and the two pins that carry their fixed shas. The c2v003 triage says A printed "two"; that count is UNTESTED here.
- **C5-7.** The suite's default ORIGINAL_K (EVALUATED_BEFORE_FREEZE) is scored with a fixed honest twin, as the producer writes every evaluated non-PRIMARY alternative. c2v004's unscored default was not a producer form.

PB-3, PB-7, PB-11 (as read), PB-17, C4-2 and C4-3 are withdrawn. The other c2v001-c2v004 choices are unchanged.

## Retired cases

45 in all (`RETIRED` in `suite/case_defs_c2v005_v8.py`, each with its reason and replacement). This round retires 30: B055, B113, B138, B145, B146, B161, B220, B221, B223, B243, B244, B266, B296-B300, B304-B306, B310, B311, B326, B331-B335, B337, B357. Their inputs are re-run, in the producer form where the input was not, as B360-B392.

## Files

| file | role |
|---|---|
| `classifier_b_c2v005.py` | the classifier (`cec5bfe9582899437aa715d78e1dfdb36089ebead04f840d4d68893b3d1251c7`), a byte copy of `work/drafts/cls_d10.py` |
| `kernels/*.py` | 16 byte copies (checked against KERNEL_PINS at every import) |
| `OUTPUT_SCHEMA_C2V005_DERIVED.json` | `tools/derive_schema_c2v005.py` (c2v004's derivation with the name c2v005) |
| `suite/suite_lib_c2v005.py`, `case_defs_c2v005_v8.py`, `run_suite_c2v005.py` | the producer-form generator, the 80 new cases with the RETIRED map, the runner (c2v004's with the c2v005 library) |
| `suite/run1/`, `suite/run2/`, `suite/SUITE_RESULTS_C2V005_RUN{1,2}.json` | the record runs |
| `suite/` (other `.py`) | byte copies from c2v004 |
| `work/patches/DIFF_cls_d09_to_cls_d10.diff`, `DIFF_suite_lib_c2v004_to_c2v005.diff` | the classifier and library changes (`cls_d09.py` is c2v004's classifier) |
| `work/discrim/DISCRIM_C2V005.json`, `dev_run_c2v005.py` | the discrimination check |
| `work/` (other files), `tools/` (other files) | byte copies from c2v004 |
| `tools/make_read_log_c2v005.py`, `tools/make_hashes_c2v005.py` | write READ_LOG.txt and HASHES_C2V005.txt |
| `READ_LOG.txt` | the c2v004 log and note carried verbatim, then this round's opens |
| `HASHES_C2V005.txt` | the sha256 of every file here except itself |

## Conduct (self-reported)

- Python ran only as `<codex python3> -I -B`. Drafts and dev runs were in the session scratchpad. Every file here was created exclusively (`cp -n`, `set -o noclobber`, open mode `x`); this README's line references were corrected in place before READ_LOG and HASHES were written. Nothing outside `build_c2v005/` was edited.
- No recursive search: `ls` of named folders, `grep`/`sed` of named files, all in READ_LOG.
- V006 was read through an awk filter printing A133, A154, A168, A173, A176 and A190 only.
- Not opened: classifier A's code, suite, outputs, regression, verify, work, tools, logs or audit files; the agreement records; any NGC3198 target, velocity, sigma or slots file.
