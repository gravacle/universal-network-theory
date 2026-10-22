# LENS_C4V001: Claude4 lens review of the RI45-14 list FREEZE_EXPECTED_INPUTS_C2V003

- **Object.** `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s0_launch_kit_c2/FREEZE_EXPECTED_INPUTS_C2V003.json`, sha256 `454dd3ccb6f9d1056981aa44b24237e12066c43ef8a37753606b783fa3383e9d` (TESTED from bytes). It is pinned in V006 A157 as `RI45_14_LIST_PIN` together with the three root fields A157 states (interior_count = 5, spec = CX2V006, notes.A16.1 text).
- **Reviewer.** Claude4 lens helper, distinct review, refute by default. Written 2026-10-19T18:39:45Z (date -u).
- **Severity basis (A115).** BLOCKING only if it is reachable from honest pinned producers on the real records. That means the freeze would consume a wrong, missing or target-bearing input, refuse an honest step-5 result, or change a tier, member set, reading or computed value, or the defect changes a physics reading. Everything else is NOTE.
- **Labels.** TESTED: run here, result shown. FORMAL: read from the cited bytes. Line numbers are those of the files at the shas below.

## 0. Verdict

**NOT READY AS THE LIST OF RECORD: 2 BLOCKING, 13 NOTE.**

What holds:
- Every pin I may open re-hashes to its recorded sha256: 39 MATCH and 0 mismatch, plus slots `d3859b42` MATCH (TESTED).
- The A157 GATE_PIN rows agree with the list and with GATE_DOCUMENT_PINS_V002.
- The alternatives equal slots V003 exactly.
- parameter_region equals the CX2V006 engine coordinates.
- Every diff in CX3V002 → C2V001 → C2V002 → C2V003 is reproduced and classified.

What fails is the list's value contract for two `write_freeze_manifest` inputs:
- **B1, notes.** The list maps `notes` to free-text keys `A13` and `A16.1`. v003g in coordinate mode `DDO154_DISTANCE_FIXED_AT_REGISTERED` never reads those keys. Instead it requires `notes.ngc3198_slot_sensitivity` and `notes.structural_assumptions`, the latter holding SA-BH-01, SA-REACH-01 and an A18 entry. The list names none of these.
- **B2, spec.** The list maps `spec` to the CX2V006 coordinate spec, which carries no NGC3198 slots. Its only NGC3198 values are placeholders marked "PLACEHOLDER VALUES, NOT NGC3198 INFORMATION". The list's own rule says select_representative_points and write_freeze_manifest "must receive the same spec", which ties the freeze to the phase1 selection spec, and that spec is built from those placeholders.

Followed as written, write_freeze_manifest refuses at the Phase-1 freeze. RI45-14 exists to prevent exactly this ("v003g refuses any missing input", ROOT_ITEMS_STEP45_V002 L275). Both repairs are target-free and can be made before any Phase-1 NGC value is read (section 8).

## 1. Bytes verified (sha256 from shasum, TESTED)

| File | sha256 | Agrees with |
|---|---|---|
| FREEZE_EXPECTED_INPUTS_C2V003.json | 454dd3ccb6f9d1056981aa44b24237e12066c43ef8a37753606b783fa3383e9d | HASHES_C2V003 L2; V006 L1269; SELFCHECK target |
| build/selfcheck_freeze_c2v003.py | 1875c6978db66d05ac73436f7d7ab26af72409e2485465abcf39c9c4255e3102 | HASHES_C2V003 L12; list self_check.checker |
| build/build_prelaunch_c2v003.py | 85b3e8d857c5b2c262aca7614be91264c173b1cc93ca4f2b96e6b43a3a840adf | HASHES_C2V003 L11 |
| HASHES_C2V003.txt | 060467a586d3b7b24daef090fb5d3de83388baf72bf428a6a23f97161dc2300e | (does not list itself) |
| SELFCHECK_RESULTS_C2V003.json | 5b44369226e370e27b319676e90937a72e5ba10b0d756376397d14f10f924d68 | HASHES_C2V003 L5 |
| PRELAUNCH_CHECKS_C2V003.json | cc5678c9d935eb16b4e22afc2fa78b60d84c2d711b946c746cf8983ce26de542 | HASHES_C2V003 L6 |
| README_PRELAUNCH_C2V003.md | db373981b6f5528a2d9e9247da93cd8a1d0112a373fcb6a81ab75848bf1c1617 | HASHES_C2V003 L10 |
| FREEZE_EXPECTED_INPUTS_C2V002.json / _C2V001.json | dc0d6ec7... / 5adce77a... (full values in HASHES_V002 L6 / HASHES L4) | the list's supersedes chain |
| FREEZE_EXPECTED_INPUTS_CX3V002.json (step5_ngc_route_ab_readiness_cx3/) | 169df91f67ea73c7a0291b3fbc852c70777107753685191b95f97dacc9672253 | supersedes chain; DIFF headers |
| DIFF CX3V002→C2V001 .diff/.json | 84dcf0d5... / 22c88ca0... | HASHES.txt L2-3 |
| DIFF C2V001→C2V002 .diff/.json | b1040194... / ac9ba652... | HASHES_V002 L2-3 |
| DIFF C2V002→C2V003 .diff/.json | e46d3499... / 8fe91139... | HASHES_C2V003 L4/L3 |
| A133_TWO_PHASE_PROTOCOL_V001.md | cd92ef914a0d562f0392080ebf709b5fdb1d85ef7f7b4493ee143fe782cfac17 | task brief; list interior_count.searched_sources |
| v003g prediction_freeze_c2v003g_cx3v001.py | 48a1e48a5230fff346705c338da30a8ee53a8643193dbe4616c25e61eab3d405 | list freeze_module; latest version folder is v003g (no v003h) |
| slots NGC3198_FREEZE_SLOTS_CX3V003.json | d3859b42390d75952b3f7942290fe1ae8b3044e4378dd4c92dbcfd2e7ee50969 | list L224 (RECORDED there, TESTED here); v003g ROOT_SLOTS_SHA256 L1583 |
| V006 addendum (now) | efcbd6a58b1175be7892d50cf896d8464b1771c4043631a6d8539aaf902cf018 (1299 lines) | list was built at 73663c84 (A155 highest); A156/A157 appended since |
| V004 addendum | 487d44498205e563c752e692b48bbb7288055591c72cfdcf5a75d849fef3d82b | read L62-69 and L226-230 only |

**Every other pinned path the list names** (code_files, input_files, referenced_not_input_files, coordinator_evidence) was screened, checked for symlinked ancestors by lstat only, then re-hashed (TESTED):
- 39 MATCH and 0 MISMATCH. This includes the driver `577f8c94`, phase1 v001/v002/v003/v003a, the filler, the handoff writer, root_monitor, the sched gate, the extractor, the TSR flag record, the carriers, the three M-7 pins, the A2 and STAGE0 grids, the 8 S0 EPS/GQ records, the four certificates, the S0 theta record, POLICY_C2V001, CX2V006 and its addendum, GATE_DOCUMENT_PINS_V002, RUNBOOK_V002, the roster builder and the coordinator evidence.
- The root_inputs review `7ff20c1d` also MATCHES.

**Skipped by rule:**
- the query manifest and the route-B config, both NGC3198-named;
- the DDO154 observation-region file, conservatively, because it is an observed-velocity table (calibration galaxy).

## 2. Task 1: what the list is, and how v003g consumes it

**Schema.** `UNT_STEP5_TO_FREEZE_INPUT_MAP_C2V003`. It has 35 top-level keys. The ones that carry content:
- the 17 `write_freeze_manifest_inputs` rows, one per keyword of v003g L3516-3518, in signature order; this is TESTED against the source;
- `code_files` (13), `input_files` (34) and `referenced_not_input_files` (4);
- the top pins: freeze module, query manifest, slots, route-B config and coordinator evidence;
- `interior_count`, `exact_alternative_declarations`, `first_pass`/`second_pass` and `launch_custody`;
- bookkeeping: `changes_*`, `open_items`, `labels`, `v006_at_build`, `rederive_at_build` and `self_check`.

**v003g does not read this list (TESTED).** No string in v003g names FREEZE_EXPECTED, INPUT_MAP or RI45. The list is a map that root follows by hand at RUNBOOK steps 6-7, and only some of its pins are checked against bytes:
- **Sha-checked inside v003g:**
  - the query manifest, against the hard pin `a2936517` (L54, L3594, via load_query_manifest);
  - the slots, against the hard pin `d3859b42` (L1582-1583);
  - the region file, against the run's region sha (L1170-1214, L3332);
  - the calibration record, by self-hash and fingerprint (L3279-3359).
- **Hashed as found:** every other code or input file is read by `_pin_files` (L3491-3506), which records whatever bytes are at the path at freeze time and compares them with nothing. The list's recorded sha256 values are therefore not enforced by the freeze (N8).

## 3. Task 2: against A133 section 1.4 L78, section 2 row 1, and RI45-14

**What A133 asks of the list.**
- **Section 1.4 L78:** "v003g select_representative_points runs on the B_P1 run, with interior_count taken from the RI45-14 list."
- **Section 2 row 1 (L185):** the RI45-14 list is fixed before the first Phase-1 NGC launch (Wed 21 Oct 17:00).
- **RI45-14 option (a) (ROOT_ITEMS L280):** "lists every write_freeze_manifest input with its producing record and owner". Its issue line (L278, Claude3 S2 N9) names what was missing: parameter_region, observation_rule, the coordinate spec, the region file, "the notes used by A16.1 and A13" and allow_incomplete.

**Present and right:**
- **parameter_region:** a dict with bounds_semantics (S11, L3574-3577). Its box equals the CX2V006 engine_coordinates exactly (TESTED, jq).
- **observation_rule:** an accepted type (L3578).
- **alternatives:** equal to slots V003 (TESTED, boolean equality; required by v003g L2485).
- **query_ids:** the 43 ids.
- **allow_incomplete:** True for Phase 1, False for Phase 2.
- **TSR flag record and carriers:** pinned in input_files, as RI45-14 asks.
- **Gate records and certificates:** pinned, and equal to A157's 15 GATE_PIN rows (TESTED: each (sha, path) pair is found once in input_files and in GATE_DOCUMENT_PINS_V002).
- **The rest:** ORIGINAL_K and sensitivity at budget 0 in Phase 1, and the cx3r008 root input.

**Missing or wrong:**
- **notes (B1).** "The notes used by A16.1 and A13" are, in v003g, `notes.ngc3198_slot_sensitivity` (A16.1/A16.4, L2941-3037) and `notes.structural_assumptions` with SA-BH-01, SA-REACH-01 and an A18 entry (A13 mode, L3040-3088). The list carries free-text `A13` and `A16.1` strings instead.
- **spec (B2).** No NGC3198 slot source is named, and the named spec carries placeholders.
- **Lesser gaps:**
  - null_direction_rule (N5);
  - the A16.4 wrapper check (N4);
  - Phase-2 rows (N7);
  - an annotated query_manifest value (N6);
  - concrete kit file paths (N13).

**Target-bearing or out of scope:**
- Nothing in the list's bytes is target-bearing: only query ids, model radii and node radii, model numerics, and no observed velocity or error.
- The NGC3198-named pins (query manifest a2936517, route-B config 64b6f1fa) cannot be checked from this lane. Only the query manifest is sha-enforced by v003g (N8).
- The DDO154 region file is calibration data and is allowed for its role.
- coordinator_evidence and launch_custody are not freeze inputs. They are harmless.

**Both phases.**
- Phase 1 is covered.
- Phase 2 is only partly covered. out_path, selection.exploration and the calibration-record input name only the Phase-1 registry and the B_P1 record (N7).
- interior_count is used in both phases (phase1 `agree` L1032 re-derives the Phase-2 members with the same CLI value). A157 should say that 5 binds both phases (N2).

## 4. Task 3: the self-check and its recorded results

**What `selfcheck_freeze_c2v003.py` checks.** It reads only the list's JSON. It refuses any string whose status word, bound to the nearest alias in its clause, differs from that item's structured status. It also refuses verbal absence or presence claims that contradict PENDING.

**What it leaves unchecked:**
- **Pins.** It opens no pinned file and recomputes no sha256.
- **Contract.** It checks no value against the v003g contract: key sets, required notes blocks, NGC slots, modes.
- **Kwarg rows.** KWARG_ITEMS (L35-36) omit spec, notes, selection, reference, sensitivity, query_ids, query_manifest and alternatives, so those rows' statuses are not even text-checked.
- **Lists of items.** A status after a list ("A, B, C STATUS") binds to C only. The checker discloses this.

**Recorded results.** SELFCHECK_RESULTS_C2V003 (`5b443692`) holds 12 rows, all AS_EXPECTED:
- F-C3-01 MUST_PASS on 454dd3cc;
- F-C3-02..08 and F-C3-10..12 MUST_FAIL, on C2V002, on the three put-back strings and on mutations;
- F-C3-09 a control.

The checker was not re-run here (no Python).

**Can a PASS on honest inputs hide a wrong pin? Yes.** A PASS certifies text-vs-status consistency only. It would PASS a wrong sha256, a missing input (B1, B2) or a wrong value.
- The builder's `rederive_at_build` (L160-188) is what re-hashed TESTED_FROM_BYTES pins at build. It recorded no changes, and my re-hash agrees.
- Nothing re-checks between the A157 pin and the freeze (N8).

## 5. Task 4: the three root fields

### interior_count = 5

**What it sets (FORMAL).**
- `_selection_plan` (L1111-1146) takes `_evenly_spaced_indices(len(remaining), interior_count)` (L481-489): min(5, remaining) evenly spaced admitted points by log_index, after the hull vertices, the anchor and the centroid-nearest point.
- The value is frozen as `admitted_region.selection_interior_count` (L1557). The verifier recomputes the plan from it (L2734) and the writer re-runs selection with it (L3442).
- A157's description of the rule (v003g L1245-1250) is accurate.

**Other code paths.**
- The phase1 tools take `--interior-count` with no default (v002 L1070, v003a L1297).
- They pass it to v003g selection for the handoff (v002 L583), the fdplan member calls (L697), and the Phase-2 member check in `agree` (L1032). They record it as `interior_count_RI45_14` (L626, L710).
- There is no other semantic use.
- Nothing binds the CLI value to A157's 5 (N2).

**"Changes no tier ... moves only compute and envelope breadth" is too strong (N1).**
- v003g's frozen headline is "the distribution (min/median/max) of the within-error counts of EVERY admitted representative member ... plus the within-error count of the REFERENCE MEMBER" (HEADLINE_RULE L79-84; score_after_freeze L4229-4255). n_members and the min/median/max counts therefore move with interior_count.
- The reference is the nearest VALID member (REFERENCE_RULE L85-88; L2213-2222). It is invariant only while the centroid-nearest member is valid. A cap that fires (A133 section 3 (f)) or any invalid member hands the reference, and so the 43 predictions (A133 L168), to the nearest valid selected member, and that member depends on interior_count.
- AT-1 runs over every valid Phase-2 PRIMARY member (A133 L257), so COVERED or SUPERSEDED can depend on it.
- More members also raise the Phase-2 FREEZE_INCOMPLETE risk.

The value is a legitimate CHOICE declared before any result, so this is not an integrity defect.

**Further notes on A157's text:**
- **Precedent.** "The only operational precedent" also misses root's own call-order toy, `root_call_order_toy_v003d.py` (`92e0b20d`) L200, which uses interior_count=6. The phase1 v003a tests use 0 and 6.
- **A142 item 3.** V006 L707 is about STAGE0 timing (the STAGE0 delay from the Phase-2 member count). A157 widens it to "Phase-2 step-5 duration".
- **Phase-1 call count.** A133 1.4's counts (4, or up to 7) assume B_P1 = 7. In the 22-call branch, 5 allows up to 12 members plus 3 F points.

### spec = CX2V006

**A135 item 7 (V006 L563, read):** "C1 is the tail-era CX2V006 lineage ... S0 is identical under V005A and CX2V006 (TESTED). AT-0a re-checks this at the Phase-1 freeze." A157 matches this.

**A157's claims check out (TESTED):**
- DDO154_COORDINATES_CX2V006 (`50e7288e`) and SPEC_V002 (`89e7d33e`) differ in raw bytes only at L1254-1255. Those lines are each file's own `freeze` pin: v003d `74e0d406` versus v003a `5ee3e5dc`.
- The coordinates, engine_coordinates, observation_region, engine_parameters, trial_point and units blocks are byte-equal.
- The two addenda differ only in `applies_to_coordinate_spec_sha256`. Both carry the coordinate_mode DDO154_DISTANCE_FIXED_AT_REGISTERED, with free coordinates [common_scale_s, gamma_over_Eref, ell_F_m] and distance_Mpc fixed at 4.04.
- So A157's "engine coordinates are byte-equal" is TESTED, and "S0 identical" follows, because the engine_parameters and trial_point blocks are equal.
- The list's input_files pin CX2V006 and its addendum, consistently.

**What remains:**
- **B2.** CX2V006 carries no NGC3198 slots: its 29 coordinates are 28 shared and 1 ddo154_nuisance. Its own `preconditions_before_freeze` lists "NGC-slots ... (NGC lane)" as OPEN.
- **N10.** Neither spec file pins v003g. A133 L55 and L196 still say "coordinate spec V002".

### notes.A16.1 (word for word against V004)

- **V004 L68:** "The manifest notes must state that the box-limited band rows are invalid by design (A16.1). The `evaluated: true` field then reads as "attempted and refused", not as a zero sensitivity."
- **V004 L228:** "**A16.1's stated reason is corrected.** It now reads: "the NGC3198 slots never enter calibration or member selection, and the members are evaluated at the registered geometry.""
- **A157 L1275:** "The box-limited band rows are invalid by design (A16.1): `evaluated: true` reads as attempted and refused, not as a zero sensitivity. The NGC3198 slots never enter calibration or member selection, and the members are evaluated at the registered geometry."
- **Sentence 1** is a faithful paraphrase of L68, not a copy. It drops "The manifest notes must state that" and "field then", changes a period to a colon, and drops the quotation marks around "attempted and refused".
- **Sentence 2** equals the L228 corrected reason verbatim except for the capital T.
- **Description.** A157's description ("L68 with its reason as corrected at L228") is accurate. The text is not word for word (N3).
- **Effect in v003g.** v003g never reads `notes['A16.1']`; it is stored only (L3778). The machine-checked A16.1/A16.4 statement is the slots block's `manifest_reading_note` (L2995-2998). See B1.

## 6. Task 5: the diffs

**Path sets.** I recomputed the leaf-path sets with jq. Objects are recursed and arrays treated as atoms.
- CX3V002→C2V001: 25 added, 0 removed, 7 changed.
- C2V001→C2V002: 7 added, 0 removed, 15 changed.
- C2V002→C2V003: 45 added, 1 removed (`interior_count/v006_at_build`), 16 changed.

All three equal the DIFF reports exactly (TESTED). The 18 keys claimed unchanged from CX3V002 are byte-equal in C2V003 (TESTED).

**Changes, classified.**

- **CX3V002→C2V001.**
  - Identity: schema, date and supersedes.
  - root_inputs: the r006 fallback is replaced by cx3r008 (driver 577f8c94, registry 2c3f421d, review 7ff20c1d), per RI45-08 (a) and RI45-14 (a).
  - a66 row_mapping: ROOT_UNRESOLVED becomes M-7 (i).
  - Phase-1 ORIGINAL_K is NOT_AVAILABLE.
  - Added: write_freeze_manifest_inputs (all 17 kwargs, filling the N9 omissions), code_files, input_files, referenced_not_input_files, interior_count, labels, open_items, launch_custody, saves and status.
  - Explained by changes_from_cx3v002. One exception: root_inputs[3] drops "NOT_RUN tail star convergence" from the A90 binding and adds A101. It is described only as "wording per RI45-14 (a)", which is a semantic narrowing (N12).
- **C2V001→C2V002.**
  - phase1_c2v003 goes from PENDING to EXISTS_NOT_ADOPTED (149ed4cb); phase1_c2v003a is added (385b287c); the sched v003 gate is added (736a3438).
  - The kit goes to PENDING_ROOT_ADOPTION.
  - The TSR flag record goes from PENDING to EXISTS_NOT_ADOPTED (61bd8a83), an erratum to C2V001.
  - GATE_DOCUMENT_PINS V001 (afa1df05) becomes V002 (5e688882).
  - RUNBOOK_V002 and the roster builder are split out as EXISTS_NOT_ADOPTED.
  - The S0 EPS/GQ owner text notes A148; the custody records name the C2V002 attempt records; labels are added.
  - Explained by C2V002's changes_from_c2v001, except three editorial edits (N12): the phase1_c2v002 rule text ("at v003 iff ..." becomes "at d64351ec unless the reviewed successor ..."), the replay-adapter why_pending ("not built" becomes "no source names a built file"), and "not produced yet" appended to two why_pending texts.
- **C2V002→C2V003.**
  - The changes_* lists are regenerated with statuses taken from the structured entries.
  - interior_count goes from PENDING_ROOT_FIXES to NO_REGISTERED_VALUE, with the sources it searched.
  - The kit candidates are taken from bytes; C2V002_HASHES goes from "WRITTEN_AFTER_THIS_FILE" to 24fb60dd.
  - Texts are regenerated: the TSR support record why_pending, the roster text and notes.A16.1.
  - Added: v006_at_build, rederive_at_build and self_check.
  - Changes otherwise: existence timestamps only.
  - All are explained by changes_from_c2v002, except that the regenerated open_items (status words filled, a new item 8) are not listed (N12).

**No change touches a pin's sha256 or a structured value without explanation.**

## 7. Findings

### B1 (BLOCKING): the notes row omits the v003g A13-mode notes contract

**Where.** List `write_freeze_manifest_inputs[kwarg=notes]` (L425-435) and A157 notes.A16.1 (V006 L1275).

**Defect.** The list's notes value is `{A13: <text>, A16.1: <text>}`. v003g reads neither key. In coordinate mode DDO154_DISTANCE_FIXED_AT_REGISTERED, which is forced, write_freeze_manifest needs two things and refuses without them:
- **The slot block (L2954-2960, L3682).** `notes.ngc3198_slot_sensitivity` must be present, with status, applies_to, declared_range equal to the spec's NGC slots, headline_geometry and manifest_reading_note.
- **The structural assumptions (L3054-3071).** `notes.structural_assumptions` must hold SA-BH-01 and SA-REACH-01, each with non-empty text_verbatim, and at least one entry with `section: 'A18'` and text_verbatim.

**Evidence.**
- **The mode is forced.** The list's parameter_region.mode (L278) and both addenda give the A13 mode. The freeze coordinates must bind to the run's (L3729-3732). phase1 freeze_spec applies the addendum mode (v002 L376).
- **Slots provide only part of it.** Slots V003 `notes_block_for_manifest` holds coefficient_grid_sensitivity, ngc3198_slot_sensitivity and structural_assumptions {SA-BH-01, SA-REACH-01, placement, source}, with no A18-section entry (structure only).
- **The review harness builds it the same way.** It sets notes = slots block plus a synthetic `A18-REVIEW-SYNTHETIC` entry, described as "not the root text" (review_v003g_cx3v001.py L143-146).
- **RI45-14 L278** names "the notes used by A16.1 and A13".

**Consequence.** Followed as written, the Phase-1 freeze refuses with "REFUSED (A16.1) ... requires notes.ngc3198_slot_sensitivity" and "REFUSED (A10/A12/A18)". That refuses honest step-5 results.

**Fix.** Make the notes value a deep copy of slots V003 (`d3859b42`) `notes_block_for_manifest`, then:
- add under structural_assumptions an entry `{section: 'A18', text_verbatim: <the root A18 in-plane anisotropy text of record>}`, and name that source file and its sha;
- optionally keep `A13` and `A16.1` as inert extra keys;
- add `raw_result_custody` if the RUNBOOK requires it (harness L904);
- record the result in a successor list or V006 entry before any Phase-1 NGC value is read, and dry-check it with a synthetic MODE_D_FIXED write_freeze_manifest that touches no NGC value.

### B2 (BLOCKING): the spec row names no NGC3198 slot source, and its named spec carries placeholders

**Where.** List `write_freeze_manifest_inputs[kwarg=spec]` (L334-357) and A157 spec = CX2V006 (V006 L1274).

**Defect.**
- v003g's `spec` must contain exactly one NGC3198 distance slot and one inclination slot (`_build_spec` L774-780).
- CX2V006's 29 coordinates are 28 shared and 1 ddo154_nuisance, with no ngc3198_nuisance slot.
- Its only NGC3198 values sit under `ngc3198_nuisance_slots.placeholder_for_engine_coordinate_derivation`, which it labels "PLACEHOLDER VALUES, NOT NGC3198 INFORMATION ... The real slots replace them at freeze", with status TO_BE_DECLARED_BY_THE_NGC3198_LANE_BEFORE_FREEZE.
- Its preconditions_before_freeze lists NGC-slots as OPEN.
- The pinned phase1 tools build their v003g spec from exactly those placeholders (phase1_c2v002 freeze_spec L372-380; v003a L420-428).
- The list's value_rule says select_representative_points and write_freeze_manifest "must receive the same spec".

**Evidence (TESTED by equality booleans only; no slot value shown).**
- Slots V003 `ngc3198_slots` have the same names and keys as the placeholders.
- But the distance box differs, and the inclination trial, box and reference_value all differ.
- The slots notes block's declared_range and headline_geometry match the real slots and not the placeholders.
- From the CX2V006 bytes: the placeholder inclination trial is 70.0.
- V004 L66 and L230 give the registered NGC3198 geometry as 13.8 Mpc and 72°.

**Consequence.**
- v003g passes the NGC3198 slots to forward_ngc at the spec's trial values (L1019-1026) and checks the slot block against the spec slots (L2978-2994).
- A freeze that follows the list's spec pointer and its "same spec" rule therefore carries placeholder NGC3198 geometry into every member's theta_ngc. It is refused by REFUSED (A16.1), or every member is left invalid by the forward's A16.4 geometry refusal.
- ROOT_CALL_ORDER_V003D L29 still says "NGC3198 slots V002", which is not v003g's slots V003.

**Fix.** State that

spec = make_freeze_coordinate_spec(coordinates = apply_coordinate_mode(coordinates = CX2V006.coordinates + slots V003 (`d3859b42`) ngc3198_slots, coordinate_mode = COORDINATE_ADDENDUM_CX2V006.coordinate_mode).coordinates).spec

and also:
- require its engine_coordinates to reproduce the campaign's, as phase1 freeze_spec already checks;
- restrict "same spec" to the engine coordinates, or re-run select_representative_points at the freeze with the real-slot spec. Selection is NGC-slot independent (L1284-1566), so the member set is unchanged;
- close CX2V006's NGC-slots precondition by citing slots V003.

### NOTES

- **N1.** A157's interior_count rationale is too strong (section 5). The member set enters the v003g headline distribution (L79-84, L4229-4255). It enters the reference choice when the centroid-nearest member is invalid (L85-88, L2213-2222), AT-1 (A133 L257), and the Phase-2 FREEZE_INCOMPLETE risk. The "only precedent" claim misses the toy's 6 (`92e0b20d` L200). "A142 item 3" (L707) concerns STAGE0 timing only. **Fix:** correct the wording. The choice itself stands.
- **N2.** The three A157 values are not in the pinned bytes. The list still reads NO_REGISTERED_VALUE/null, ROOT_RULES and PENDING_TEXT. Every phase1 command takes `--interior-count` by hand. **Fix:** add a checklist line: every phase1 receipt and plan has interior_count_RI45_14 == 5, and every manifest has admitted_region.selection_interior_count == 5, in both phases. Alternatively, a C2V004 list with the three fields filled.
- **N3.** The notes.A16.1 text is a paraphrase of V004 L68 plus the verbatim L228 reason, not a word-for-word copy (section 5). The key is inert in v003g.
- **N4.** A16.4's "Required check before ROOT_CALL_ORDER step 5" (V004 L67: real wrapper calls at D = 12.545 Mpc and at i = 69°, each valid=false with GEOMETRY_NOT_EXPOSED) is absent from the list. **Fix:** add the check and its saved records as a freeze precondition.
- **N5.** evaluate_sensitivity's `null_direction_rule` (L2383, L2279-2291) is frozen in the sensitivity block and fixes the Phase-2 sensitivity calls. It is not fixed by the list, RUNBOOK_V002, ROOT_CALL_ORDER_V003D or ROOT_ITEMS. The harness uses box_ends (L243, L899). **Fix:** fix it now. It is never a headline.
- **N6.** The query_manifest row's `value` (L402-407) carries an extra key `sha_status`. v003g L3585 refuses any key set other than {path, sha256, role}. The value_rule itself is right. **Fix:** strip the key or mark the value as annotated.
- **N7.** Phase-2 values are not stated: out_path (the Phase-2 registry root), selection.exploration (the campaign record's run at budget 120) and the Phase-2 calibration record. These are mechanical, but the list is "one complete list" (RI45-14).
- **N8.** v003g pins whatever bytes it finds (L3491-3506), and nothing compares them with the list's sha256 values after build. The route-B config pin 64b6f1fa has been re-hashed by no Claude lane, and v003g does not check it. **Fix:** add a root freeze step that compares manifest pins.code_files and pins.input_files with the list (refuse on mismatch), and have root re-hash the route-B config.
- **N9.** The self-check covers only text-vs-status consistency (section 4). Its PASS cannot detect a wrong pin, B1, B2 or a wrong value.
- **N10.** Provenance of the two spec files:
  - Neither pins v003g: V002 pins v003a 5ee3e5dc and CX2V006 pins v003d 74e0d406.
  - A133 L55 and L196 say "coordinate spec V002". Record that A157/A135.7 supersedes this wording (content-equal; v003g reads only the coordinates).
  - All 7 of CX2V006's preconditions_before_freeze read OPEN or PARTIAL in its bytes, and the list does not record their disposition.
  - A135.7's "AT-0a re-checks this at the Phase-1 freeze" is not carried by the list.
- **N11.** observation_rule.rule (L326) says "as v003g run_calibration_region applies them". run_calibration_region is the engine's function; v003g only names it in docstrings. **Fix:** a wording fix.
- **N12.** Minor unexplained diff edits (section 6). The only semantic one is the A90 clause narrowing in root_inputs[3]. **Fix:** confirm that A101 subsumes "NOT_RUN tail star convergence", or restore it.
- **N13.** The kit's code_files entry has a null path. A157 adopts "C2V002" by name, not by the HASHES_V002 sha `24fb60dd` that the list's ADOPTED_IN_V006 rule reads. v003g refuses non-path pins. **Fix:** name the concrete kit files at the freeze. The replay adapter is still PENDING.

## 8. Smallest repair (target-free; before any Phase-1 NGC value is read)

1. **notes (B1).** Set the notes row to: slots V003 `notes_block_for_manifest`, plus a root A18 structural-assumption entry (source pinned), plus the inert A13 and A16.1 texts.
2. **spec (B2).** Set the spec row to: CX2V006 coordinates plus slots V003 `ngc3198_slots`, via apply_coordinate_mode (CX2V006 addendum) and make_freeze_coordinate_spec, with engine coordinates equal to the campaign's. Restrict "same spec" to the engine part.
3. **Dry check.** Run a synthetic MODE_D_FIXED write_freeze_manifest dry run with these two constructions, before the Phase-1 freeze. No NGC value is needed.
4. **Notes N2, N4, N5 and N6.** Do these in the same entry: bind 5 for both phases, add the A16.4 check, fix null_direction_rule, and strip sha_status.

## 9. Conduct and rule incidents

**Opened (reads; greps of single named files):**
- CURRENT_INSTRUCTIONS.md (per CLAUDE.md);
- the kit files listed in section 1;
- CX3V002;
- A133 (sections 0-5);
- v003g;
- the review harness (`a435711b`);
- ROOT_CALL_ORDER_V003D and its toy (grep only);
- RUNBOOK_V002 (grep only);
- ROOT_ITEMS_STEP45_V002 (RI45-14);
- phase1_c2v002 and v003a (named lines);
- CX2V006, SPEC_V002 and both addenda;
- HARNESS_BUILD_V001.json.

**NGC3198-named files, only as permitted:**
- V006: A157 L1243-1280, A135 item 7 L563, A142 item 3 L707 (and L716, a sub-item 3, one line). Headings were located with awk printing line numbers only.
- V004: L62-69 and L226-230.
- slots: structure, plus the equality tests below.

**Not opened:**
- the rehearsal and the classifier;
- the query manifest, the route-B config and the DDO154 region file;
- V003 and V005;
- runs trees, runs_ext, C5H, UVT_* and UNT_INTERNAL_RUNS;
- External1.

**Discipline.**
- No Python and no recursive search. The non-recursive listings were the s0_launch_kit_c2 prefix globs and build/*, the freeze_score_readiness_cx3 v* glob, and the v003g folder, whose NGC3198 names were filtered out (count 0).
- No launches.
- Every program-file read was prefixed with taskpolicy -b.
- Writes went only to this folder, by exclusive create with noclobber; PARTIAL.md was append-only.

**Self-reported incidents:**
1. While checking the slots structure for an A18 entry, one jq call printed two `section` label strings ("A10", "A12 decision 2") from slots structural_assumptions. These are values, beyond pure key structure.
2. Equality-only jq tests read slots V003 values internally and displayed only booleans. They covered ngc3198_slots against the CX2V006 placeholders, the notes block declared_range and headline_geometry, and alternatives against the list. No slot value was displayed.
3. One shell loop used the variable name `path`, which clobbered zsh's PATH. That run printed only "command not found" errors and did nothing; it was re-run with other names.

## 10. Erratum (appended 2026-10-19T18:43:24Z, same author; nothing above is edited)

- **Re-hash count.** Sections 0 and 1 say "39 MATCH". The re-hash output holds 38 MATCH lines: 11 code files, 25 input files, 2 referenced files and the coordinator evidence. With slots `d3859b42`, that is 39 pins MATCH, and 0 MISMATCH in all cases.
- **"Byte-equal" in section 6.** "The 18 keys claimed unchanged from CX3V002 are byte-equal" means equal as canonical JSON (`jq -cS` hashes), not raw bytes.
- **Gate pins in section 3.** Each A157 (sha, path) pair is found exactly once in the list input_files and at least once in GATE_DOCUMENT_PINS_V002. The three M-7 pins appear twice there.
- **Correction to the first bullet** (appended 2026-10-19T18:43:41Z). The 38 MATCH lines are 11 code files, 24 input files, 2 referenced files and 1 coordinator evidence. Adding slots `d3859b42`, which is also an input file, gives 25 input files and 39 pins MATCH in all.
