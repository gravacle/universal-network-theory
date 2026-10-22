# Lens B (target-free and blinding): review of the miss-reading prereg r2, round 1

- **Lens:** B, target-free and blinding. Dispatch 0585 (`9003633293ff1db7d5153cabc338fd058cc199d834976b05543b7603b9433abd`), checked under 0592. Refute by default.
- **Reviewer:** a Claude4 helper lane. It wrote only in this folder. It did not edit the object.
- **Object:** `claude_artifacts/miss_reading_prereg_c4/r2/round1/`. All 10 entries of HASHES_R2.txt match `shasum -a 256` (checked 2026-10-18T18:48Z, rechecked 19:15Z). The values below are pasted from shasum output:
  - `6437ea33432f50971eef81e549a8e5789d0bd892efaf2d0f423ce4c933f30143` PREREG_MISS_READING_R2.md
  - `b105b55d7f80c5868d936f577ce81e92992999440f5cd85a06decbc62650d24b` CLAUSE_SOURCE_MAP_R2.md
  - `1d7af792f9b115fc7882254b694d82299217c3ab846d7d26d591f45a5c5eaf7f` ROOT_ITEMS_R2.md
  - `c81b5a7a579476480a085681ebd6eb8aa445e38b6a7abe2284dba3716b0c2832` NUMBER_PROVENANCE_R2.json
  - `aab683236116bc3562df86f3b9542a54eec3446c44a8f0e5569ff2b305d2180b` TARGET_FREE_CHECK_R2.json
  - `2a8202b823beb5cd0bc03c9e1e2b0377d9de59410a698c8d185f39739d66bc41` TARGET_FREE_MUTATION_TEST_R2.json
  - `6c1919a900d56fcb7438015db6a6be1d1d28fd07ee17a9bee6e1e007c0045b9b` INDEX_R2.md
  - `85457a43c654aa13b49fa528b786a615e99a51eaa29b4ba42687a2c0f3396cc7` tools/check_target_free_c4v001.py
  - `fc403648a57b3f0ee30b164e2cde48e3c1889bfee33938c8b23a93c1fd88ea11` tools/test_check_target_free_c4v001.py
  - `8c0d9fc2fb962f3e72de9e6a7a03cc11aa38efccd59981713fbcc0008b32576a` tools/make_miss_reading_c4v002.py
- **V005 read at review:** `0753f2d8dc437592a4ad70140f309c774837cb07e9c04e2c213c4421eeb8e87e`, read at 18:52:12Z and unchanged at 19:15:11Z. A copy is in `snapshots/V005_AT_REVIEW.md`. It holds A47–A91, while r2 was assembled on `17cb4fd4…` (last entry A89). V004 `487d4449…` and V003 `5bef6552…` match.
- **No target was opened.** No path containing rotmod, Vobs, MassModels or SPARC was opened. No NGC3198 data table, C5H run or `UVT_*` file was read, listed or stat'ed. Nothing was launched. All test data is synthetic. Python was run with `-I -B`, so no pycache was written into the object.

## Verdict: PASS_WITH_FINDINGS (0 BLOCKING, 8 SHOULD_FIX, 4 NOTE)

**What holds:**
- On its actual bytes, the r2 text is target-free. No r2 text file names an NGC3198 observed or target velocity, a target-bearing file or a target data source. That covers the prereg, map, root items, INDEX, provenance, check JSON, mutation JSON and HASHES.
- Every number in the text traces to a target-free source (§B below).
- Zone membership is fixed by query id, from the target-free slots query block.
- The reference member, the envelope membership, the cut rows and the gap rows are all fixed by target-free rules (v003g REFERENCE_RULE, SELECTION_RULE, A60).
- No rule needs target information before the score step.

**What does not hold:**
1. The blinding is incomplete against the one channel that the target-free check cannot see. That channel is public knowledge of the observed NGC3198 curve, which root's own A41 cites as "NGC3198's flat outer curve", combined with step-5 predictions that will exist before the planned seal.
2. Several reading rules still leave discretion at the score step.
3. The target-free check proves much less than INDEX_R2 says. 37 of 38 adversarial target-like mutations pass it.
4. T5 passes when a later V005 entry amends a cited ruling, and it passes now, although A90 (NGC K32 N-tests complete) postdates r2.
5. The TRUNCATION_SHAPE_RESIDUAL flag rule (M-7) cannot be executed on the actual N-test record: it stores a point, not an interval.

## A. Findings (most severe first)

### B-1 SHOULD_FIX: the seal and all root rulings can come after the NGC predictions exist

**Where:** PREREG C-Status "Seal" (L12); C-9 residual-risk rows (L369–372); ROOT_ITEMS M-6.

**Quotes:**
- r2 L12: "Root seals this text before any NGC3198 target is opened (A60; 0585), by registering its sha256 in a root entry (root item M-6)."
- r2 L369: "They are fixed now, before targets. Root may change them only before the seal (M-3)."

**Defect.** The only timing constraint is "before any target is opened". The program has scheduled the rulings and the seal "in the freeze step":
- A60, V005 L513: "Root rules on them and seals the prereg **before targets are opened**, in the freeze step."
- The freeze runs after step 5 has saved every member's raw forward result (RUNBOOK_V001 L9, step 1).

So all twelve root items could be ruled while the 43 NGC predictions are readable. These are the tiers (M-1 a/b/c), the zone cuts (M-2 a/b), the thresholds (M-3), the DT-S0G rule (M-9), the twin rule (M-10) and the radial support (M-7). The observed NGC3198 curve is public knowledge in rough form, and root's own decisions use it:
- V004 L747 (A41): "Static present-mass gravity cannot supply NGC3198's flat outer curve";
- V004 L685 (A39).

A rule chosen with the predictions in view can therefore be tuned to the outcome without any target file being opened. The target-free check (T1–T6) cannot detect this.

**Evidence.**
- Step 5 has not launched yet. 0594 L3: "Step 5 launches after the V007 adoption (step 3) and the DDO recalibration (step 4)". A8/A11: NGC route A failed at iteration 0 and was not relaunched. So no NGC prediction exists now, and the fix is still available.
- A prediction-blind freeze is feasible. RUNBOOK steps 2, 4 and 7 use only finiteness, cut records and projections, never predicted speeds.
- Program precedent:
  - A47 I3 (V005 L24): "Before the seal, the gate functions run on C5H only as validity/admissibility booleans and reason codes, with no row value printed or written."
  - A15 (V004 L28): "written before any NGC3198 target is opened and before calibration."

**Fix.**
- C-Status and M-6 should read: "Root rules M-1…M-12 and seals this text before any step-5 NGC route-A/B output value (prediction, band or envelope) is produced or read. Until the seal, step-5 outputs are read validity-only (A47 I3 pattern). The seal entry attests that no NGC prediction value was read before the rulings."
- If root cannot meet this, every M item is adopted exactly as written in this text, with no option switching, and the deviation is disclosed in the report header.

### B-2 SHOULD_FIX: the TSR flag rule cannot be executed on the record of record, so the flag set is undefined

**Where:** PREREG C-1.4 (L126); C-9 L371; ROOT_ITEMS M-7 (L136–141).

**Quotes:**
- r2 L126: "A row carries the flag if and only if the root-pinned flag record of root item M-7 lists it."
- M-7 L138–140: "the radial support [r_lo, r_hi], exactly as stored in that record … A query q is flagged if and only if r_lo ≤ R_q ≤ r_hi."
- M-7 L141: "The record is registered with the rosters (RUNBOOK_V001 step 4)".

**Defect.** The record of record does not store an interval:
- The production K32 compare, `ngc_ntest_eval_cx/out/K32_COMPARE_COMPLETE_V001.json` (`6f095f64…`; Codex1 0056; A90), stores `failing_TRUNCATION_SHAPE_rings[0].radial_support = {"kind": "sampled_ring", "R_kpc": 10.540847190215317}`.
- "Exactly as stored", the rule therefore flags no row. P10 can never hold, and R-TSR is vacuous.
- Any interval someone later chooses changes the flagged set. The rule places that choice at RUNBOOK step 4, after step-5 predictions exist (see B-1).

**Evidence** (`runs/TSR_FLAG_SET_BY_DEFINITION.json`; N1 record `8867c376…`). The neighbouring N-test rings are 9.9018 and 10.9117 kpc; Q25 is at 10.04 kpc and Q26 at 11.04 kpc.

| support definition | interval (kpc) | rows flagged |
|---|---|---|
| point, as stored | — | none |
| midpoints to the neighbouring rings | [10.2213, 10.7263] | none |
| neighbouring rings | [9.9018, 10.9117] | Q25 |
| two rings each side | [9.0001, 11.6560] | Q24, Q25, Q26 |
| ±0.5 kpc | [10.0408, 11.0408] | Q26 only (Q25 misses by 0.0008 kpc) |

**Fix.**
1. In r3, fix the support rule from the target-free ring list.
2. Compute the flagged query ids now and list them by id in C-1.4, as was done for the zones.
3. State the arithmetic: R_q from Rad_text in kpc, a closed interval, no metre conversion. (The RUNBOOK metre rule can differ at one-ulp neighbours.)
4. The flag record then becomes a pure lookup, fixed at the seal.

### B-3 SHOULD_FIX: discretion after the predictions exist has reading consequences, and C-9 claims it is closed

**Where:** PREREG C-3.1 DT-S0G (L188); C-9 (L364); C-4 (L218, L225, L228, L243); P9 (L206).

**Quotes:**
- r2 L188: "It is evaluated only if its runs finish before the freeze and root adopts an evaluated slots/module successor".
- r2 L364: "Evaluating STAGE0_GRID_OUTER only if it helps | It is evaluated only before the freeze, or it reads NOT_EVALUATED_BEFORE_FREEZE (A65.2)."
- r2 L243: "INVALID rows are excluded from N_v(Z), from m(Z), and from every pattern except P0 and P9."

**Defect, STAGE0 adoption.** Adopting an evaluated STAGE0 is a root act. RUNBOOK L5: "root must approve a new slots/module-pin successor before it can be admitted as evaluated". That act comes after the headline and STAGE0 predictions exist. So "only before the freeze" does not close "only if it helps".

**Defect, root-listed gates.** RUNBOOK steps 3–4 approve gates after step 1 has saved the forward results. A gate on OUTER rows leaves the headline unchanged, because INVALID still counts as a miss. It does change the readings:
- gating some OUTER rows changes m(OUTER), miss-dominance and S(OUTER), so P1, P1g or P2 can disappear;
- gating all of them turns P1 with R-MF "TESTED-NEGATIVE" (L195) into P9 with "E2 reads NOT_TESTABLE" (L206).

**Fix.**
- (a) STAGE0 is EVALUATED if and only if every registered STAGE0 member run has a FINISHED receipt before the freeze manifest is written. Root decides on receipts and validity booleans only, without reading any prediction value, and records the decision with the receipt times.
- (b) INVALID rows from root-listed gates registered after any step-5 output exists still score as INVALID_AS_MISS (0518). They are reported as GATE_AFTER_PREDICTIONS, and P9 or the E2 NOT_TESTABLE reading may not rest on them. Built-in reasons (QUERY_INSIDE_INNERMOST_NODE, cut and gap rows) are unaffected, since they are mechanical.
- (c) Until (a) and (b) are adopted, move the C-9 row to the residual risks.

### B-4 SHOULD_FIX: reading statuses at the score step are not mechanical, so the report format can be steered

**Where:** PREREG C-3 (L168–169); C-3.2 against-column (L200–205); C-8 item 5 (L340); ROOT_ITEMS M-12.

**Quotes:**
- L168: "The 43-row score can make a reading **consistent** or **inconsistent**."
- L169: "A reading whose deciding test has not run stays OPEN, whatever the score shows."
- L340: "each with the status consistent, inconsistent or OPEN".
- L200: "ORIGINAL_K shows the same excess (against R-GRID)".
- L201: "**R-ML:** the DT-T1a M/L variants do not move the inner rows by the miss."
- L202: "An onset radius inconsistent with k* … is reported, as a comparison only." This sits in the against column.
- L203: "a DT-GEO evaluation removing the offset (not available before the freeze)".
- L205: "ORIGINAL_K and the A17 C3 grid record agree".

**Defect.**
- R-UT1, R-HIST and R-REACH have no deciding test that has run. When P1 holds, L168 makes them "consistent" and L169 makes them "OPEN", but C-8 allows one status. The classifier picks one after seeing the targets.
- "Same excess", "move … by the miss", "onset radius" and "agree" are undefined, and they are applied after target access.
- R-ML's against-condition needs ML-variant predictions. ML_3p6_0.4 and 0.6 are NOT_EVALUATED_BEFORE_FREEZE (§6.2), and DT-T1a varies only f★ (A16.3, V004 L62; A10, V003 L41–44). So the condition invites a post-target evaluation.
- P6 likewise invites a post-freeze geometry evaluation that "removes the offset". That is a fit to targets, contrary to I-2 and C-5.4.
- No precedence is given when a consistent-condition and an against-condition both hold.
- M-12, the sealed classifier, is only a recommendation.

**Fix.**
1. Report two fields per reading:
   - score relation (consistent, inconsistent or not applicable), mechanical from the table;
   - test status (OPEN; TESTED-NEGATIVE for R-MF only).
2. Precedence: any registered against-condition that holds makes the reading inconsistent.
3. Define each against-condition, for example "the ORIGINAL_K twin satisfies P2" and "the ORIGINAL_K twin satisfies P8, and the A17 C3 record passes C3".
4. Mark the R-ML and P6 DT-GEO against-conditions NOT_AVAILABLE, with this sentence: "Any alternative or geometry evaluated after the freeze is EXPLORATORY (post-score) and changes no status."
5. Define P5's onset radius or remove it from the against column.
6. Make M-12 binding.

### B-5 SHOULD_FIX: there is no "first score is final" rule, root rulings after targets are unconstrained, and later deciding tests may reuse the opened rows

**Where:** PREREG I-7 (L64); C-1.1 fail-closed (L93); C-3 (L168); ROOT_ITEMS M-8.

**Quotes:**
- L64: "If root authorizes scoring a FREEZE_INCOMPLETE manifest, the classification is still made and reported in full."
- L93: "Root then rules before any reading is reported. The score stands as computed."
- L168: "Support comes only from that reading's own deciding test, run under its own pre-registration."

**Defect.**
- Nothing says that a later complete freeze, or a re-score after a FREEZE_INCOMPLETE score, is post-score. The completion steps, such as budgets, members and sensitivity, would then be chosen with targets seen.
- The RUNBOOK rule "No roster, cut or reference may be chosen after targets are seen" (RUNBOOK L26) is not restated in the text.
- After CLASSIFICATION_INPUT_DEFECT, root rules with the score output in hand, and the content of that ruling is unconstrained. Choosing another member, for instance, is not excluded.
- A deciding test pre-registered after NGC targets are open can re-score the same 43 rows and "support" a reading. DT-UT1's continuation rule, for example, is only "chosen by root before any galaxy use" (0521 via A65 L1275).

**Fix.**
- Add to I-7: "This text classifies the first successful score_after_freeze on NGC3198 targets. Any later freeze, re-registration or re-score after target access is EXPLORATORY (post-score)."
- Limit post-defect rulings to a field map that preserves values, or to NOT_AVAILABLE for the affected rows.
- Add to C-3: "A deciding test registered after NGC3198 target access can support a reading only through data not opened when its prereg was sealed. A re-score of these 43 rows under such a test is EXPLORATORY for this text."

### B-6 SHOULD_FIX: T5's per-entry V005 pins pass on changed rulings; M-6 covers only V006; the "no change" list is stale

**Where:** PREREG C-11 (L417, L433); ROOT_ITEMS M-6 item 3 (L122); check tool T5.

**Quotes:**
- L433: "The following entries were read with no change to this text: A61, A67–A69, A71–A80 and A83–A89."
- M-6 L122: "Any V006 entry made before target access that touches the reading needs either a revision of this text or an explicit no-change note".

**Defect.** Root amends rulings through later entries:
- A53 L241: "This amends A52.3";
- A88 L943: "amends A79 NEW-61";
- A73 L805: "Correction to A62".

A later entry leaves the cited section's bytes unchanged, so T5 still passes.

**Evidence** (`runs/T5_V005_AMENDMENT_RESULTS.json`; probe `tools_lensb/t5_v005_amendment_lensb.py`):
- These pass T5: a new entry inserted where root inserts entries, amending A81 RI-23 (E01); text inside the uncited A90 that withdraws A66.2 (E02); headings `## A81a:` and `## A66 amendment` (E07, E08).
- These fail, as they should: in-place edits, duplicate headings and appends at end of file (E03–E06, E09).
- Live case: the current V005 (`0753f2d8`) holds A90, which touches the reading:
  - V005 L913–918: "NGC K32 N-tests (Codex1 0056): N_FAIL_N1 … LO_NGC_K32_CERT_V001 (07745bbf) … Open for step 5: the LO I1-T precondition … NOT_RUN";
  - T5 still passes, with only a note (`runs/CHECK_RERUN_AT_REVIEW.json`).
- A81 RI-26 (L1062) covers "Any entry after A81", but M-6 drops the later-V005 case.

**Fix.**
1. T5 lists every `## A…` heading in the current file, in any suffix form, and fails on any entry that is not in the cited, read-no-change or revised lists.
2. M-6 item 3 covers every V005 entry after the last one read (now A90 and A91) as well as V006.
3. r3 cites A90 for the formal N-test reading and the step-5 LO I1-T root item, or records it as no change.
4. At the seal, check against the frozen V005 copy by whole-file sha.

### B-7 SHOULD_FIX: T4 has broad false negatives, and INDEX_R2's "Proved … Every number in it has a target-free source" over-claims

**Where:** INDEX_R2 L21–23; check tool `numeric_tokens` (L67–75) and T4 (L189–203).

**Quotes:**
- INDEX L21: "**Proved (by construction, from bytes):** the text names no target file, data source, velocity value or target symbol value (T1–T3)."
- INDEX L22: "Every number in it has a target-free source (T4)."

**Defect.**
- T4 checks token *values*, not *occurrences*. A listed value may appear anywhere, and all ten single digits 0–9 are listed.
- Categories are self-declared, and `uses` is never checked.
- Only the prereg is scanned. ROOT_ITEMS and the map are not, although root may rule their text into r3.
- Several stripping rules hide numbers: 8-or-more-digit runs (HEX), `§`, glued identifiers, and code spans (K-1).

**Evidence** (`runs/ADVERSARIAL_RESULTS.json`; harness `tools_lensb/adversarial_check_lensb.py`). 37 of 38 mutations PASS. All values are non-physical sentinels:
- "The quoted value v_q of NGC3198-Q43 is 778." (A01)
- "The quoted σ_q of every OUTER row is below 93.6." (A02)
- "778 km s−1" with U+2212 (A03)
- "1.48e5 m/s" (A07)
- "9​8​7 km s−1" (B01)
- "9\*\*8\*\*7" (B02)
- "⁹⁸⁷ km/s" (B03)
- "1.48×10³ km/s" (B04)
- number words (B05)
- "Q43/987.6" and "Q43_987" (B06, B07)
- "98760000 cm/s" (B08)
- "§987.6" (B09)
- a number added to ROOT_ITEMS or to the map (B15, B16)
- a self-declared `MODEL_DIAGNOSTIC` entry (B17)

Only the control fails: "v_q(Q43) = 987.6" (B13a).

**Consequences of K-1 beyond its description:**
- the same class of hole exists outside code spans (B06–B09);
- putting the symbol in a code span defeats T3 ("`v_q` = 778", B11).

On the actual r2 bytes nothing is hidden. Every digit-bearing code span is a file name, an identifier or an elided sha, and every `§` is a real section. So the PASS on r2 itself stands.

**Fix.**
1. Scan every text file.
2. Bind each listed number to its occurrences, by clause tag, and require each occurrence's tag in `uses`.
3. Fail on non-ASCII digits, on Cf and zero-width characters, soft hyphens, U+2212 next to a digit, digit runs split by markup, and number words.
4. Strip only 64-hex shas and the elided-sha pattern.
5. Verify each non-radius number by locating it in the cited entry's section bytes, as `runs/PROVENANCE_LOCATE.json` does by hand.
6. Change the INDEX wording to "checked against a deny-list and a listed-value inventory".

### B-8 SHOULD_FIX: T1, T2 and T3 are narrow deny-lists that miss target paths, data sources, units and symbol forms

**Where:** check tool L14–15 (FORBIDDEN, FORBIDDEN_EXT), L63–64 (VEL, SYM), L173–182 (three files only).

**Quote:** L14: "FORBIDDEN = ('rotmod', 'vobs', 'v_obs', 'massmodels', 'sparc', 'lelli', 'begeman')"

**Evidence** (`runs/ADVERSARIAL_RESULTS.json`). All of the following PASS:

T1:
- `…/data/NGC3198_observed_curve.txt` (C01)
- `…/NGC3198_OBSERVED_VELOCITIES.json` (C02)
- NGC3198.data and NGC3198.dat_v2 (C03, C04)
- .tsv, .xlsx and .fts (C05)
- "THINGS curve of de Blok et al." and "van Albada" (C06)
- ＳＰＡＲＣ in fullwidth (C07)
- rot­mod with a soft hyphen (C08)
- "Mass Models" and "Mass_Models" (C09)
- "rotmod" inside the provenance JSON, which T1 does not scan (C10)
- "V obs" and "v-obs" (C11)
- the C5H and UVT_ run names (C12)

T2:
- km s−1, km·s⁻¹, km∕s, kilometres per second, m/s and cm/s (A03–A07, B08)

T3:
- `v_q` = …, v\_q = …, v_q(Q43) = …, v_q ≃ …, and "v_q of … is …" (A01, B11–B14)

**Fix.**
- NFKC-normalize and strip Cf characters before matching.
- Treat as forbidden any NGC3198-named path, or any data-like extension, that is not on an allow-list of pinned target-free files.
- Extend the source names: THINGS, de Blok, van Albada, plus the existing seven.
- Run T2 and T3 on the normalized text, for any relation (=, ≈, ≃, ~, "is", "of") within a few characters of a number, and any velocity unit including m/s and cm/s.
- Also scan the provenance JSON and the INDEX.

### B-9 NOTE: the audit hook only partly blocks, and it never ran for the bundled PASS

**Where:** check tool `_hook` (L20–35), `main` (L266); generator L75; test L61.

**Quote:** tool header L9: "An audit hook refuses any open whose path contains a forbidden term, and any write other than --out."

**Evidence.**
- `runs/HOOK_PROBE_RESULTS.json`:
  - Refused: deny-listed opens and write-mode opens.
  - Allowed under the installed hook:
    - `os.truncate` (a canary in this folder went from 17 to 0 bytes);
    - mkdir, symlink, hard link and chmod;
    - exec, posix_spawn and fork;
    - listdir and scandir of a deny-listed directory;
    - C5H and UVT_ paths;
    - fullwidth spellings.
  - An open through an innocently named symlink reached the OS. The hook does not resolve realpath.
- `runs/HOOK_PROBE_PART3.json` and grep: `sys.addaudithook` is called only in `main` (L266). The generator (L75) and the mutation test (L61) call `T.run()` unhooked, so `TARGET_FREE_CHECK_R2.json` was produced without the hook.
- A hooked CLI rerun reproduces it, apart from the V005 note (`runs/CHECK_RERUN_AT_REVIEW.json`).
- T5 accepts a section-11 pin of a synthetic file named `SYNTH_NGC3198_OBSERVED_VELOCITY_TABLE_NOT_DATA.json` as target-free (D01).

**Fix.**
- Install the hook inside `run()`, with the output allow-list.
- Refuse truncate, mkdir, link, symlink, chmod, utime, exec, spawn, fork, and listdir or scandir of deny-listed paths.
- Test the resolved realpath.
- Add c5h, uvt_ and kmax_a2f10_c5h_run to the deny-list.
- Say in INDEX that the bundled result came from the unhooked path.

### B-10 NOTE: provenance mis-citations, and "uses" claims that are not true

**Where:** NUMBER_PROVENANCE_R2.json entries "0.03", "0.51", "0519", "0521" and "0523"; PREREG C-3.2 P3/P4 (L201).

**Quotes:**
- provenance: "DDO154 stellar share about 0.03 (V001 3, A21/E1)" and "NGC3198 stellar share about 0.51 (V001 3, A21/E1)";
- "0519": "FROM_CODEX/0519 (section 11 pins it)".

**Evidence** (`runs/PROVENANCE_LOCATE.json`):
- 0.03 and 0.51 occur only in V003 A10 L44: "DDO154 has a stellar fraction of about 0.03 and NGC3198 about 0.51". They do not occur in A21 (V004 L176–197) or A15 E1 (V004 L30–35). A10 calls f★ target-free, so there is no target problem.
- Section 11 pins only 0518, 0522, 0524, 0531, 0535, 0545, 0546, 0548 and 0585.

**Fix.**
- Cite A10 (V003 `5bef6552`) for 0.03 and 0.51, in the provenance and at L201.
- Change the uses for 0519, 0521 and 0523 to "named as withdrawn by 0524 (pinned)".

### B-11 NOTE: the mutation test's sentinels are realistic NGC3198-magnitude velocities, one bound to an OUTER row

**Where:** `tools/test_check_target_free_c4v001.py` L40–45.

**Quote:** "'The quoted value is 150.2 km/s.'", "'Here v_q = 151 for Q40.'", "'A quantity of 147.3 appears here.'"

**Defect.**
- These synthetic values sit at the publicly known flat-rotation level of this galaxy, the same public knowledge A41 relies on, and one is attached to a real OUTER id (Q40 is 38.19 kpc).
- A sealed bundle should carry nothing that reads as a plausible target value.
- No reviewer can check closeness without opening targets.

**Fix:** use non-physical sentinels, for example 987.6 km/s, v_q = 9876, and a fake id such as Q99.

### B-12 NOTE: the "Flat" disclaimer refers to nothing in r2, and the P1 "expected" label rests on A41's observed-curve wording

**Where:** PREREG C-1.3 L119; C-3.2 P1 row (L195).

**Quote:** L119: "\"Flat\" is the registered name of the outer region. It asserts nothing about the observed curve shape."

**Evidence.**
- r2's zones are INNER, TRANSITION and OUTER. The name came from V001 L63 ("OUTER (outer flat region)"), which r2 removed.
- P1 is labelled "(expected: A15 E2, A41)". A41 (V004 L747) asserts "NGC3198's flat outer curve".

**Fix:** delete L119, or replace it with: "P1's 'expected' label rests on A15 E2 and A41. A41's reference to the observed flat outer curve is literature knowledge, not a target read, and no classification rule uses it."

## B. Number provenance (task item 2): each value located in its source (`runs/PROVENANCE_LOCATE.json`)

| values | category | located in |
|---|---|---|
| 0.32, 9.04, 10.04, 28.16, 30.08, 44.08 | QUERY_RADIUS | slots V003 `query_block.rows[].Rad_text` for Q01, Q24, Q25, Q35, Q36 and Q43 (T4 also checks these). 44.08 also appears in A15 E2 (V004 L38). |
| 24, 11, 8, 43 | ROW_COUNT | slots: zone counts recomputed from Rad_text with cuts 10.0 and 30.0 give 24/11/8; n = 43; STAGE0 outer_rows = 8 |
| 10, 10.0, 30, 30.0 | RULE_CONSTANT | A15 E1 L31 ("R ≲ 10 kpc"), E2 L38 ("about 30–44.08 kpc"); A65.3 L1237 (R ≥ 30 kpc); v003g `_alternative_score_scope` (`>= 30.0`) |
| 13.8, 72, 12.545, 15.18, 69, 75 | GEOMETRY_REGISTERED | A16.1 V004 L56–57; A23 V004 L230 |
| 4.04, 66 | GEOMETRY_REGISTERED | A13 V003 L111; A23 V004 L224, L230 |
| 0.5, ±20 | BARYON_MODEL_REGISTERED | A10 V003 L36, L44 |
| 0.4, 0.6 | BARYON_MODEL_REGISTERED | A16.3 V004 L62 |
| 0.03, 0.51 | BARYON_MODEL_REGISTERED | A10 V003 L44 only; mis-cited (B-10) |
| 1.48, 95, 778, 1.1, 1.90, 0.11, 3.551 | MODEL_DIAGNOSTIC | A63 V005 L585, L591 |
| 0.477, 0.483, 93.6, 1.899, 0.106, 15.6, 0.451 | MODEL_DIAGNOSTIC | A65 V005 L1224–1228 |
| 15, 10.54, 1.0148, 1.1–3.7, K = 2 | MODEL_DIAGNOSTIC | A66 V005 L624–628; A64 L605; also A90 L915 |
| 16, 32, 64, 91 | NUMERICS_RULING | A60 L502; A64 L610–616 |
| 96, 128, [2, 91], θ/20 | NUMERICS_RULING | A60 L502; A81 RI-22 and RI-23 (L1058–1059) |
| L = 4, L ≥ 6 | NUMERICS_RULING | A15 E3 L44, L48; A63 L588 |

All of these are model-side or registered values with a target-free source. None is a velocity. The radii and the 13.8 Mpc distance come from the program's target-free query manifest and slots. Per the slots provenance note, the distance was checked against the data headers; that is a registered geometry, not a velocity, and r2 inherits the program's ruling.

## C. Tested (artifacts in this folder)

| artifact | what it is |
|---|---|
| `runs/CHECK_RERUN_AT_REVIEW.json` | the check CLI with its hook, on round1: PASS; identical to the bundle apart from the T5 note about V005 |
| `runs/MUTATION_RERUN_AT_REVIEW.json` | the object's mutation test: 14/14 |
| `tools_lensb/adversarial_check_lensb.py` → `runs/ADVERSARIAL_RESULTS.json` | 38 adversarial cases; 37 false negatives |
| `tools_lensb/t5_v005_amendment_lensb.py` → `runs/T5_V005_AMENDMENT_RESULTS.json` | 10 V005 variants |
| `tools_lensb/hook_probe_lensb.py` → `runs/HOOK_PROBE_RESULTS.json`, `runs/HOOK_PROBE_PART3.json` | the audit-hook probes |
| `tools_lensb/provenance_locate_lensb.py` → `runs/PROVENANCE_LOCATE.json` | each provenance number located in its sources |
| `runs/TSR_FLAG_SET_BY_DEFINITION.json` | TSR flag sets under candidate support definitions |

**Naming sweep of all 11 r2 files:**
- The text files hold no target term, no data-like extension and no number word used as a quantity.
- The only non-ASCII character in the prereg is U+2212, used in formulas.
- The tools contain the deny-list names and the synthetic sentinels of B-11.

## D. Outside this lens (for the other lenses; no finding here)

- I-6 (L56): "only N_PASS is an input to route A/B" conflicts with the A66.2 exception given one bullet earlier. 0606 item 6 already lists this.
- Codex1 0032 (`3e8c9fc9…`, 14:50Z) reports GQ_NGC at M_s 96 passing on [2, 91] ("M_s96 holds; no128 proposal needed"). r2 I-6 still states the M_s 96/128 condition without citing that record.
