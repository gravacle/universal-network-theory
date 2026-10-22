# LENS SLOTS_RECORD: what root's seal run seals (Claude4 delta of Claude3's SELECTED c3v010, A115 scope)

Helper of UNT lane Claude4, lens SLOTS_RECORD. Work 2026-10-19T06:23Z to about 06:58Z (`date -u`; the PARTIAL.md log in this folder has the stamps).
Every Python step ran through the fence (`tools/run_fenced_c4st2.py` fe904509, `tools/fence_c4v002.py` c993d34c). In all three runs the fence summary read selftest 8/8, probes 15/15 and blocked_after_selftest [].
Nothing was launched: no seal or dry-run script, no driver, solver or monitor, no tool 4 build, and no tools 1, 2, 3 or 5 run (tool 3's run() loads the compare, so it was never called).
No protected path was opened or listed: the NGC3198 target data, runs_ext, the C5H run, `UVT_*` trees and UNT_INTERNAL_RUNS were all left alone.

## Verdict: BLOCKING_FINDINGS. 1 blocking (SR-1, class (b)) and 6 notes

Every slot value and every pin in the dry-run SEAL_RECORDs checks out from bytes as the object of record. No superseded object is pinned anywhere in them. The manual disclosures are V006 byte for byte, the I4 handling (A114, A117, A121) is correct, and the pin graph has no cycle. The one blocking finding is a stale step-8 input: the record carries the wrong gate verdicts for two pre-seal NO_RUN gates.

## Objects (sha256 from bytes, this session)
| object | path (short) | sha256 |
|---|---|---|
| SELECTED c3v010 | seal_assembly_c3/SELECTED_SEAL_PRESTAGE_C3SA_c3v010.json | 1f62deb4abe3375a02a63a1b803e2aa4c49a4b2ad997d399a618869ef240e161 |
| seal script c3v026 | seal_assembly_c3/ROOT_SEAL_STEPS_c3v026.sh | b43cc38be5f19c473167d8d57211c54d336d09d58fcfd66f5ca8187ad033c464 |
| slot draft c3v007 | seal_assembly_c3/c3v010_prestage/SLOT_VALUES_DRAFT_c3v007.json | 184ff5cbc01eb2683ace5cee8fbee1e82b38d7d6ac152726713501c1ddc83729 |
| previous draft c3v003 (c3v009 SELECTED) | seal_assembly_c3/SLOT_VALUES_DRAFT_c3v003.json | e12292a27e58aacdebfde5dfc4d1a3f7ccb0c5b3ca4b756ef2a6d8468a5311c5 |
| step-8 gates manifest (tuple role gates_manifest_draft; script L258) | seal_assembly_c3/MANIFEST_GATES_ONLY_DRAFT_C3SA.json | e5967bb9901fda39703553c5c02b4d11a580ef8456f6c0b7d315ee4c750f09da |
| dry-run SEAL_RECORD pass A / pass B | dry_run_20261019T060546Z/pass{A,B}/scratch_ctrl/V007_SEAL_ASSEMBLY/SEAL_RECORD_V007.json | 6649052d63d7be10f6b8465c75e095fae7932161b77a1582a9c0ae8aac44c78b / e661b6ff25351159250533cd92452c5ce03c924fddcad7b2ddd93148cb5b272d |
| root rulings V006 addendum (as read) | CLAUDE2/ROOT_DECISIONS_..._V006_ADDENDUM.md | f3b2c9190bcf9414dda989954c96a4b8c91e6555eb33abf3b46592adc22490af |
| closed V005 (open path now; = the bytes step 1 freezes) | CLAUDE2/ROOT_DECISIONS_..._V005_ADDENDUM.md (143081 bytes) | c01b3c51e34501d77e474594cc0b4be72c6e068c7f58a595055316313a8d4bb1 |

## 1. The slot draft c3v007 (TESTED: out/SLOTS_RECORD_ANALYSIS_C4SR_V001.json part A)
The draft has 23 pin leaves.

**18 filled slots.** Each one hashes from bytes to its pin, and each one is the object of record:
- **driver:** `driver_r5/galaxy_m0_forward_c2v010.py` b5cc62af (r6, A96).
- **driver_check_record:** `driver_r5/check/CHECK.md` 89a6de88 (A111 P3; the prefix and the path are in the V006 addendum text).
- **compare_reviewed_source:** r14 f3f9ba7e = SELECTED_R14_CX1V002.selected_source (A116.1, A117).
- **identity_comparator:** c2v007r2 052da0fe.
- **identity_gate_records:** Z2 83e7b067, Z2_OFF_RO1 3b9ad402 and B0prime_RERUN e33af53d (A92).
- **launch_packet.build:** BUILD_V007 94bc05a5.
- **certificates:**
  - EPS 598c8fa3, LO 1c384f76, GQ 5a1b39f8, DOUBLING ea48ac2b and LO_NGC 33bc2190 (r6 named candidates);
  - EPS_NGC 1d5eef1b and I1T_NGC 3ae7981a (A107, A111 P4).
- **producer_registry:** V012 4b8a3c35 (A121; 0665 table).
- **admission_entry:** launcher v007 861bba68 and guard v008 294cb776.

Each expected value comes from r6's named_candidates bytes or from the SELECTED pins. Where a ruling states an 8-hex prefix, the check also confirmed that the prefix appears in the ruling text and that the sha begins with it.

**Scalars.** driver_branch is r5, ngc_gas_M_s is 96 (r6 certificates rule) and cache_directory_r6_only is NOT_APPLICABLE_R5 (r6 value).

**5 PENDING slots.** Each output path is absent now:
- frozen_addendum;
- driver_build_record;
- launch_packet.bound_plan;
- launch_packet.bound_command;
- cascade_map_r5_addendum.

The frozen path equals r6 `seal_slots.frozen_addendum.path_to_be`. Step 1 fills it with the sha that r6's rule states, c01b3c51, and the open V005 file still has those bytes (143081). The cascade slot is filled from root's P7 input, 86c89730, which is also the prefix in 0664. The four documented output paths equal the script's FROZEN, DRIVER_BUILD_RECORD, BOUND_PLAN and BOUND_COMMAND strings, so the step-0 check DRAFT_PATHS_MUST_MATCH=1 passes at attempt 1 (string check, TESTED).

**Change from the c3v009 draft c3v003.** The key order is identical, and exactly two slots (4 leaves) changed. Hashing every draft in the chain attributes each step:

| draft | change | ruling |
|---|---|---|
| c3v003 → c3v004 723a36d1 | compare_reviewed_source PENDING(r13) → r14 f3f9ba7e | A114, A116, A117 |
| c3v004 → c3v005 d6924860 | producer_registry V009 → V010 b8435877 | A113 RI-33, A114 |
| c3v005 → c3v006 f542e394 | V010 → V011 512a7171 | A119 |
| c3v006 → c3v007 184ff5cb | V011 → V012 4b8a3c35 | A121, 0665 |

Nothing else changed.

**Objects that are not slots.** Prereg r6, disclosures V006, the custody record, the key map, COMPLETE, P5 and SELECTED_R14 enter through the script's pins and the env block. Section 2 checks each one where it lands in the record.

**Pin graph (part E).** The graph has 60 nodes: the tuple, the inputs, the r6 and r14 files, the registry, the I4 files and the dry-run outputs.
- It has 355 "X contains Y's full sha" edges and **0 cycles**.
- No object mentions, by an 8-hex prefix only, an object that pins it back in full.
- Neither the sealed prereg nor the SEAL_RECORD's inputs pin the sealed compare; only the record, the config and the summary do.
- V006 names the script by role and does not pin it (A112), while the script pins V006.
- The sealed compare pins the sealed prereg, which pins the reviewed r14. The r3-era prereg/compare cycle is absent.

## 2. The dry-run seal records (TESTED: part C/D; GATES_MANIFEST_VS_REGISTRY_C4SR_V001.json)
- **Files of record.** All 16 dry_run_of_record files match their listed sha and bytes (`shasum -c`). Claude3's HASHES_C3SA_c3v009.txt (479b57b3) also verifies for all 170 dry-run-folder lines. Its 2 NGC3198-named scratch FROZEN lines list c01b3c51, which equals shasum of both copies; this lens does not open those files in Python.
- **Pins.** Record A has 42 {path, sha256} pins and record B has 41. All verify from bytes, except the scratch FROZEN copy, which was hashed by shasum (c01b3c51). Its schema is UNT_V007_SEAL_RECORD_C4V004.
- **Objects of record.** All 33 checks are true in both passes:
  - compare_reviewed_source is r14, and the sealed compare is r14 plus the 5 A82 pins;
  - producer_registry is V012;
  - text_of_record is r6 d28c95f5 (SELECTED_R6 7200acd9 files.text_of_record);
  - case_block is 76309ae3 (r6 binding_inputs, SELECTED_R6);
  - addendum_at_text_of_record is the r6 read copy, c01b3c51;
  - frozen_addendum.sha256 is c01b3c51;
  - raw_successor_custody is 9ca16b4f, and its quoted body equals the file;
  - key_equivalence_map is 72a21888, and its quoted [] equals the case block's map;
  - new_item_dispositions is 68164144, and its quoted 19 items equal COMPLETE.items;
  - cascade_map_r5_addendum is 86c89730;
  - later_entry_dispositions: pass A carries P5 6a3fa535 (scratch copy with the same sha; content and raw_text equal the root file), and pass B is NOT_SUPPLIED_NONE_REQUIRED by its S23 substitution;
  - certificates, the identity records, the identity comparator, BUILD_V007, and the launcher and guard all equal the draft;
  - ngc_gas_M_s is 96, ddo 128, r5, parallel8;
  - the B2 record 915fbcda is registered as V012 gate_records.B2;
  - no cache_directory key appears.
- **Superseded objects.** The superseded set has 41 objects, all hashed from bytes:
  - r13 f5adfd11, SELECTED_R13, IMPL r13, SELECTED_R14_CX1V001 dc74949d, IMPL_R14 (pre-CX1V002) and r10 to r12;
  - registries V007 to V011 and their r14 validations;
  - disclosures V001 to V005 and V003_DRAFT;
  - I4 c3v001 4d6263f6 and c3v002 2a315da2;
  - the pre-COMPLETE NEW-item lists, converter v001, the v003 seal tools, BUILD_V005 and V006, guard v007 and launcher v006;
  - slot drafts c3v003 to c3v006, scripts c3v020 and c3v025, and SELECTED c3v009.

  **No superseded sha is pinned** in either record (0 of 42 and 0 of 41). They appear only as text; see N-3.
- **Manual disclosures.**
  - `manual_disclosures.pin` is {V006 path, 8dc28480}.
  - `raw_text`, encoded as UTF-8, is the V006 bytes, and `content` equals the parsed V006, deep and in order.
  - `e_r6_1_text` equals SELECTED_R6 basis.erratum_E_R6_1.
  - The record has 19 C-08 rows and these 11 root rows: A100_B2_SANITY, A101_B2_DOC_ERRATUM, A105_E_OPS5, A107_P12, A111_P3_P4, A106_2_SRR13_CHECK_SPLIT, E_R6_2, A113_ROOT_ITEMS_R6, A114_A117_I4_AFTER_SEAL, A118_CUSTODY_FORM and E_A118_1.
  - The dry run's STEP_11_DISCLOSURES_VERBATIM reads PASS (verbatim true).
- **I4 (A114, A117, A119, A121).**
  - V012 `producers.I4` is exactly [c3v003 707395ba], and that file's bytes match.
  - V012 `gate_records.I4` is PRODUCED_AFTER_THE_SEAL.
  - r14 GATE_RECORD_AFTER_SEAL_ALLOWED (L341, read by AST) contains I4.
  - No V012 pin carries c3v001 or c3v002; they appear only in V012's note.
  - V006's A114 row names in full: c3v003, V012, r14, SELECTED_R14_CX1V002, IMPL r14, and the N1 spec C2T_N1_SPEC_DRAFT_C3V001.json 8ae6e2db (= its bytes). The SEAL_RECORD therefore pins the N1 spec through raw_text, as A117 requires.
  - I4 reads MISSING in E-SEAL1, which is expected for an after-seal gate.
- **Sealed prereg and compare.** The sealed prereg is r6 with 0 leaf differences outside `seal_slots.<k>.value`, and its 9 values equal SLOTS_FINAL. The sealed compare differs from r14 on exactly L172, L188, L294, L305 and L336:
  - PIN_ADDENDUM_V005 is c01b3c51;
  - V007_PREREG_SHA256 is the sealed prereg's sha;
  - PIN_V010_R5_CHECK is CHECK.md 89a6de88;
  - PIN_DRIVER_BUILD_RECORD is the driver build record;
  - PIN_PRODUCER_REGISTRY is V012.

  PIN_REVIEW_V009 and PRODUCTION_K_BIG_A55 are already set in r14 (r6 SRR[2]). SLOTS_FINAL differs from the draft only in the 5 PENDING slots.
- **Pass A against pass B.** They differ only by the passA/passB scratch paths and the shas derived from them (the bound plan and command, the sealed prereg and compare, and e_seal1) and by S23. The driver build record is byte-identical in both passes (25b4ff69), so its bytes do not depend on its path, and the real run gets the same bytes.
- **r6 seal_record_requirements [0] to [13].** Each has its field in record A. The exception is [0]'s RO1 replay output (SR-1).
- **Real-run D-10.** Tool 1 compares `resolve()` of the FROZEN path with `path_to_be`; the dry run relaxed this through the shim (S16 and S16b). The CLAUDE2 control path and v007_launch_packet_cx1/P128 resolve to their literal spellings (`pwd -P`; no symlinked component), so the equality holds at the real path with no allowance.

## 3. Seal tools v004 on the dry run (TESTED: out/TOOL4_CHECKS_C4SR_V001.json, 24/24 as expected)
The tools were loaded from their verified bytes, by role from SELECTED_SEAL_TOOLS_V004_C4V001 593c59fa: seal_common 101a3aeb, tools 1, 2 and 3, and tool 4 9787cf58.

**What they accept:**
- **Tool 4 `check_admission_config` (B8):** PASS on both pairs. Each pair is the dry run's config and record with only frozen_addendum.path moved from the scratch NGC3198-named copy, which this lens does not open, to the CTRL path of the closed V005 (the same bytes, c01b3c51). The config's seal pin follows the variant (1 occurrence; only that key changed). The dry run's own STEP_12_TOOL4_ADMISSION on the exact pair also reads PASS.
- **`manual_disclosures_codes(V006)`:** PASS (19 C-08 rows and 11 root disclosures; e_r6_1_text = E_R6_1). `manual_disclosures_form_codes` on both records' content gives no failure. `manual_disclosures_record(V006)` equals each record's block.
- **`key_map_codes`:** [] with no failure.
- **`new_items_codes(COMPLETE, r14)`:** no failure, and the result equals the record's 19 quoted items.
- **`custody_codes(custody, b5cc62af)`:** no failure (6 evidence pins from bytes), and the result equals the record's quoted body.
- **`later_entry_dispositions`:** on root's P5 at its CTRL path, the content and raw_text equal record A's.
- **`b6_codes`:** no failure on both passes' gates_only and validity_only_C5H outputs (step 9 is the published stub).

**What they refuse (controls):**

| input | code |
|---|---|
| config A with record B | ADMISSION_CONFIG_SEAL_NOT_THE_RECORD, ADMISSION_CONFIG_PREREG_COMPARE |
| a v003-schema record | ADMISSION_SEAL_RECORD_SCHEMA |
| the V006 path with V005's sha | MANUAL_DISCLOSURES_PIN_MISMATCH |
| a non-empty case-block map | KEY_MAP_NOT_THE_CASE_BLOCK_MAP |
| the r13 sha as the reviewed source | NEW_ITEMS_IMPL_NOT_THE_REVIEWED_SOURCE |
| a non-driver sha | CUSTODY_DRIVER_NOT_THE_SLOT |

**Informative:** tool 4 alone accepts the superseded V005 on form. Supersession is enforced by the script: the V006 constant pin plus DISCLOSURES_SUPERSEDED_SHAS in step 0.

## 4. Findings

### SR-1. BLOCKING, class (b) (also reachable on the honest real run, (a)). TESTED for the manifest, registry, validation and dry-run bodies; FORMAL for the script, helper and compare reading
**The step-8 gates-only manifest that c3v026 pins omits the two pre-seal NO_RUN gate records that registry V012 registers.** As a result, the SEAL_RECORD's E-SEAL1 would read B0_RO1 and B0_N3 as MISSING.

**The stale manifest.**
- `MANIFEST_GATES_ONLY_DRAFT_C3SA.json` (e5967bb9) is the script's `MANIFEST_GATES` (L258) and the tuple's gates_manifest_draft.
- It was written at 2026-10-18T21:31:51Z against registry V009 (Claude3's PARTIAL.md) and is "unchanged since c3v009" (README c3v010).
- Its note says "every registered pre-seal gate record of registry V009 by path ... null = not built (B0_N3, B0_RO1, I4: fail closed)".
- It sets `"B0_RO1": null` and `"B0_N3": null`.

**What the registry of record holds.**
- A113 RI-33 rules that B0_N3 and B0_RO1 are built before the seal.
- V012, the sealed registry, registers their records by sha: B0_RO1 `ri33_c3/b0_ro1/B0_RO1_RECORD_C3V001.json` 332452b7a9e63b1bc2cb24a2875f0f281e89c4332571d24825a87dcf52a466ae and B0_N3 `ri33_c3/b0_n3/B0_N3_RECORD_C3V001.json` dd1dd912580ac478e36246c226aecd5e809b2459effe35a84eac66681a42012b. Both verify from bytes, both read verdict PASS, and their producers are pinned in V012.
- VALIDATE_R14_C3V012 (a7c80f8e, pinned in the SELECTED) evaluates all 15 pre-seal records PASS on r14, these two included.
- The manifest names 13 of those 15. Each of the 13 records hashes to a sha that V012 registers. The 2 nulls are exactly B0_N3 and B0_RO1.

**The effect.**
- The helper's `check-manifest` (gates-root) and `gates-only` pass the manifest to the sealed compare unchanged.
- r14's `evaluate_gate` returns MISSING for a null path. The dry run shows this in both passes: GATES_ONLY.json, carried verbatim into the SEAL_RECORD's e_seal1 and e_seal1_text, reads `B0_RO1: MISSING (GATE_RECORD_MISSING:B0_RO1)` and `B0_N3: MISSING`.
- The real step 8 uses the same gate block. The stand-in (S10) differs only in identity_runs.

**Why it is class (b).**
- B0_RO1 and B0_N3 are r14 NO_RUN_GATES. They are in r6 gates_before_any_T_result. r14's next step for a missing required gate reads "produce the record ... (RA13: gates on real records before the seal)".
- r6 seal_record_requirements[0] (A46 RA13) requires the compare's gate functions to run before the seal on "the identity-gate records and the RO1 replay", with "their output goes into the seal record (E-SEAL1)". r6 run_list.replays names it the "B0_RO1 replay (RA5 b)".
- The SEAL_RECORD would therefore fail to seal a required element, the RO1-replay gate output. It would also permanently state MISSING for two NO_RUN gates on genuine PASS records.
- In root mode g_B0_RO1 also cross-checks the record's part_a identity-run result shas, so step 8 is the only sealed-mode check of that record before the seal.
- No forged input is involved: root running c3v026 as selected, on the real inputs, produces this record.

**Refutation attempts (none holds).**
- (i) Step 8 does not use another manifest: the script's step 8 reads $MANIFEST_GATES, and the dry run substitutes it only by S10.
- (ii) Nothing fills a null gate from the registry: the helper does not augment the manifest, and evaluate_gate returns MISSING on a None path (dry-run bodies, both passes).
- (iii) The omission is not ruled or documented: V006 A107 to A121, dispatches 0659 to 0665, the README c3v010 and the SELECTED have no such ruling.
- (iv) Neither gate needs a T result (A113), and neither touches C5H; the step-8 fence still refuses the C5H run.
- (v) The final T reading can still evaluate the two gates if root's reading manifest names their records. The CASES_MANIFEST_TEMPLATE df4cad82 has an empty gates block, so the final reading is not decided by this. The sealed E-SEAL1, however, cannot be corrected after the seal.

**Smallest fix (root's ruling):**
1. A successor manifest that equals e5967bb9 except that B0_RO1 and B0_N3 carry the two record paths above.
2. Script c3v027, with only MANIFEST_GATES and its sha moved.
3. A dry run (expect RECORD_DEFECT or crossref codes for B0_RO1 there, because identity_runs is empty in the dry run).
4. Optionally, C-03 extended to "every V012 pre-seal gate_records entry evaluated, status PASS".

The alternative is a root ruling that E-SEAL1 may show MISSING for these two gates, carried as a disclosure row.

The verdicts in sealed mode (root mode, with the identity runs) are expected to be PASS per VALIDATE_R14_C3V012. That is not TESTED here, because it needs the `UVT_*` identity-run trees.

### Notes (A115: none blocks)
- **N-1 (NOTE, TESTED text).** V006 E_R6_2 says the I4 producer "is registered in V010". The A113_ROOT_ITEMS_R6 row says the B0_N3 and B0_RO1 records are "registered in V010". Both are historically true but stale against V012.
  - The A114 row in the same sealed file names V012 4b8a3c35 and c3v003 707395ba in full.
  - The sealed compare's PIN_PRODUCER_REGISTRY is V012.
  - No physics reading reads this text.
- **N-2 (NOTE, FORMAL).** The comment at r14 L332-333 still lists I4 among the gates "registered by record sha", while L341 puts I4 in GATE_RECORD_AFTER_SEAL_ALLOWED. The code governs. The sealed compare carries the comment unchanged, as the r14 reviews of record accepted it.
- **N-3 (NOTE, TESTED).** Superseded shas appear in the record only as text, each as a historical citation or as supersession:
  - r6's entry table: A104's "compare r13 (f5adfd11, SELECTED_R13 10acd098)", r12 4bd7b262, V008 f189cd3f and V009 32ddadcb;
  - E_R6_1 (IMPL r13 274f7049);
  - E_R6_2 (r13);
  - the A114 row (V011 512a7171, c3v002 2a315da2, c3v001 4d6263f6);
  - NEW-73's evidence (the full IMPL r13 sha).

  The pinned inputs' own notes cite superseded files as well:
  - the key map cites r13 f5adfd11;
  - COMPLETE cites disclosures V002 and V003_DRAFT as its C-08 id index. That index is harmless: the ids are identical and in the same order in V002, V006 and COMPLETE (19, all ADOPTED; TESTED).

  E_R6_2 and `sealed_status_authority` govern all of these.
- **N-4 (NOTE).** B8 was re-run on variant pairs only, because this lens does not open the scratch FROZEN copy with its NGC3198 name; see section 3. In the real run the FROZEN copy sits at the CTRL `path_to_be`, which both the fence rule (b) and the tools accept.
- **N-5 (NOTE).** The SELECTED's dry-run line "no stand-in" refers to the B7 and env inputs. S10 (the gates-manifest stand-in, identity_runs emptied) and S15 (the step-9 stub) remain by design. Because the stand-in copies the draft's gate block, the dry run reproduces SR-1 rather than hiding it.
- **N-6 (NOTE).** Pass B's later_entry_dispositions is NOT_SUPPLIED_NONE_REQUIRED (S23, no file to the tools). The real run uses pass A's form, and tool 4 rebuilt that form equal to record A from root's P5 at its CTRL path (TESTED).

## Not checked here
- The real E-SEAL1 bodies (step 8 on the `UVT_*` identity runs, and step 9 on C5H). They need protected paths, and the dry run stubs or stands in for them by design.
- Tool 4 build, tool 5, and tools 1 to 3 on the dry-run inputs. They load (exec) the compare and need the dry-run shim's D-10 patch.

## Rule incidents
1. One write outside the lens folder. A `grep > file` redirect, used as `shasum -c` input, created the session scratchpad file `/private/tmp/claude-501/-Users-bgm-Research-UNT-EXCHANGE/d3eba6e0-d470-48a9-b17d-717c88261d09/scratchpad/dry_lines.txt`.
   - It holds 170 lines of Claude3's hash list; sha256 0c43a7a4acdf8143b765e117970d061454ef99c78b37fe44796cefd360e8fff5.
   - It was not deleted, under the no-delete rule. No protected content is in it.
2. The three scripts were created with the Write tool, and two of them were edited in place with the Edit tool before their first run. They are this lens's own files. No output or evidence file was overwritten, and every output was created with open(p, 'x') or set -C.
3. Python ran only through the fenced runner. The mandated runner's own start-up probes read one `uvt_*.py` source module and the V004/V005 addenda, by its design.

## Files written (this folder, sha256 from bytes; PARTIAL.md is append-only, so its final sha is in the structured output)
- scripts/slots_record_c4sr_v001.py 83218a7c5f3cafbda323d3b4f9487a259c15d1eacd1b0dbd1dd83b0c353ab64f
- scripts/tool4_checks_c4sr_v001.py cc514ed5e93aaa03b465f1ed32c437c2256d272c50b21910f14b8038bde97c4f
- scripts/gates_manifest_vs_registry_c4sr_v001.py 0eda3e2bf441f0dae9cf392ca5d3cd567936f953770b3f4c480082fada47b28e
- out/SLOTS_RECORD_ANALYSIS_C4SR_V001.json 3fb26609260e408712cb6219c336fb10a20cde1cfeac462596193c9469b1b459
- out/TOOL4_CHECKS_C4SR_V001.json ba9db712c9558e0b37dfc0775e443dba7f8e1216c8db5441d209a72fee76c34c
- out/GATES_MANIFEST_VS_REGISTRY_C4SR_V001.json dd292455effc669f7d6cf8018143f63aaede190c703f7e325b347416ebfc58d1
- out/VARIANT_passA_SEAL_RECORD_FROZEN_PATH_CTRL.json 94a42ad844aa04488d789d12973d872ae129d3f2c12e2ac69d2ba8ce05b0f8b0
- out/VARIANT_passA_ROOT_SEAL_ADMISSION.json 0a171156e7764c90262cea11d25d0257bb13555d2c2df361286f112f4035ce68
- out/VARIANT_passB_SEAL_RECORD_FROZEN_PATH_CTRL.json 0a04d6cc693b0083ae65df25e7864f69684fa38508a750ed286005ae9717c743
- out/VARIANT_passB_ROOT_SEAL_ADMISSION.json 1cd5ab0dbee929310ea148c3e61343118129e185df1fa76078fba0d3137a7b14
- out/VARIANT_passA_SEAL_RECORD_SCHEMA_C4V003_CONTROL.json 59841f7ad64301b48ed8f9748ebf5d2b1a52b799cfda65ecf89fb3bc512a254c
- out/RUN_slots_record_c4sr_v001.stdout.txt 820f7571eeed18953f2aaa98093edd6c0ef0309e5668e374ebe524e27692e5b4; .stderr.txt a9167cb7385abdc6e838d6bd64e7bf75f20efc8dc68d04d25959b14f14bab223
- out/RUN_tool4_checks_c4sr_v001.stdout.txt 6b06060f3bd6e0b1f15e7b98fab0d7aff69421150a0eb0962759b19c3e38d8b1; .stderr.txt a9167cb7385abdc6e838d6bd64e7bf75f20efc8dc68d04d25959b14f14bab223
- out/RUN_gates_manifest_vs_registry_c4sr_v001.stdout.txt 7196ded3cc6e2d12672c67e5496f61546db882a4f0d532ec0b9cb32e455b41ce; .stderr.txt a9167cb7385abdc6e838d6bd64e7bf75f20efc8dc68d04d25959b14f14bab223
