# LENS_SCRIPT: Claude4 delta of SELECTED c3v010, lens SCRIPT (ROOT_SEAL_STEPS_c3v026.sh read as TEXT, never run)

Helper of UNT lane Claude4. Scope A115 (2026-10-19). Lens started 2026-10-19T06:23:00Z; this report written 2026-10-19T06:53:07Z (`date -u`).

## Objects (sha256 from bytes, this lens)
- SELECTED_SEAL_PRESTAGE_C3SA_c3v010.json `1f62deb4abe3375a02a63a1b803e2aa4c49a4b2ad997d399a618869ef240e161` (listed in HASHES_C3SA_c3v009.txt `479b57b3914291dba903d0c027f5fa1ca47e9702d66e36ad649e6c4fb9add8d2`).
- ROOT_SEAL_STEPS_c3v026.sh `b43cc38be5f19c473167d8d57211c54d336d09d58fcfd66f5ca8187ad033c464` (88509 bytes, 824 lines; equals SELECTED selected_tuple.script).
- Predecessors: c3v025 `22746e2182cbf948cc234c61d12a812473b864607b0a6f45f3e21ab961fd24a0`, c3v020 `36058df84bb2088970be442bc64445a4c6939b45df3e9cb3294cedef62c65ac0`.
- README_SEAL_ASSEMBLY_C3_c3v010.md `a43c36a717932fda1a72bba74f1879a039731b6a175f0d733835f4d9cd3aa22f` (= SELECTED evidence.readme). Slot draft c3v007 `184ff5cbc01eb2683ace5cee8fbee1e82b38d7d6ac152726713501c1ddc83729`. Helper c3v019 `91b15dc688a2c28e1b5362d9568a80f92431938eb5e2807367b2327a37290cbf`, runner `2b040e94a2b74eae981485288471376b86be0784a0a50b59093312c4fd87bf73`, fence `9c62ad4902c895f0aeeba3a78976b5944146ee0de153989dbc79470528dd2863`.

## Verdict: BLOCKING_FINDINGS (1 blocking, 7 NOTEs)

### SCRIPT-B1 (BLOCKING, class (b); also reachable under (a)): the step-8 E-SEAL1 run omits the two pre-seal NO_RUN gate records B0_RO1 and B0_N3, so the SEAL_RECORD would carry them as MISSING
- **What.** c3v026 L258 pins the step-8 manifest `MANIFEST_GATES_ONLY_DRAFT_C3SA.json` `e5967bb9901fda39703553c5c02b4d11a580ef8456f6c0b7d315ee4c750f09da` (mtime 2026-10-18T21:31:42Z). It is the registry-V009 draft. Its own note reads: "every registered pre-seal gate record of registry V009 by path ... null = not built (B0_N3, B0_RO1, I4: fail closed)". In it, `gates.B0_RO1` and `gates.B0_N3` are null.
- **Why that is now wrong.** The registry of record V012 `4b8a3c35ca9a140bdb9e132f564d2163704e915aa67840c71c36fea551cafafa` (c3v026 L298) registers both as PRE-SEAL gate records: sha lists, not PRODUCED_AFTER_THE_SEAL.
  - B0_RO1 is `ri33_c3/b0_ro1/B0_RO1_RECORD_C3V001.json` `332452b7a9e63b1bc2cb24a2875f0f281e89c4332571d24825a87dcf52a466ae`.
  - B0_N3 is `ri33_c3/b0_n3/B0_N3_RECORD_C3V001.json` `dd1dd912580ac478e36246c226aecd5e809b2459effe35a84eac66681a42012b`.
  - Both bytes are registered, and both read PASS under r14 in Claude3's VALIDATE_R14_C3V012_CASEBLOCK_OF_RECORD `a7c80f8e87456577a1f111b4b82488305bff0af9d5f7868080749d3a8858a155`.
  - A113 RI-33 rules them "built before the seal". The registry V010 lineage added them.
  - They are 2 of the 15 V012 pre-seal gates, and the manifest names the other 13. Each of those 13 records' bytes is registered in V012 (TESTED).
- **What root's selected run does** (no forged input).
  - Step 8 (L679-694) runs `check-manifest --mode gates-root` and then `gates-only --mode root` on that manifest.
  - In r14, `read_gates` (L5528) evaluates ALL_GATES, and `evaluate_gate` (L3790) gives `status MISSING, codes [GATE_RECORD_MISSING:<g>]` for a null path.
  - B0_RO1 and B0_N3 are in r14 NO_RUN_GATES (L419).
  - Nothing in the script refuses a MISSING status:
    - check-manifest skips null gates;
    - C-03 `gates-provenance` (helper L1692) checks only the 8 slotted gates (EPS, LO, GQ, DOUBLING, LO_NGC, B1, B1_OFF, B0prime_RERUN), and the slot draft has no B0_RO1 or B0_N3 slot (TESTED);
    - tool 4 v004 `b6_codes` (L135-175) checks the schema, blinding, test_mode, script sha, route mode and number tokens, never a status.
  - Tool 4 then embeds the GATES_ONLY text verbatim as `e_seal1_text.gates_only` and pins it as `e_seal1.gates_only` (tool 4 L539-540).
  - The sealed SEAL_RECORD would therefore state that the sealed compare's pre-seal gate check found B0_RO1 and B0_N3 MISSING, although their genuine records exist, are registered in the sealed registry, and pass.
- **What the text of record requires.**
  - r6 `seal_record_requirements[0]`: "Before the seal the compare's gate and admissibility functions run on the real input records (... the identity-gate records and the RO1 replay); their output goes into the seal record (E-SEAL1)".
  - r6 `run_list.replays` names "B0_RO1 replay (RA5 b)".
  - r6 `gates_before_any_T_result` lists both B0_RO1 and B0_N3.
  - r14's own next-step text (L4542) is "produce the %s record before the T-tests are read (RA13: gates on real records before the seal)".
- **Evidence that this is what happens** (TESTED on bytes: Claude3's dry run of record, both passes, sealed mode).
  - The pass-A SEAL_RECORD `6649052d63d7be10f6b8465c75e095fae7932161b77a1582a9c0ae8aac44c78b` and the pass-B SEAL_RECORD `e661b6ff25351159250533cd92452c5ce03c924fddcad7b2ddd93148cb5b272d` (both equal to the SELECTED's dry_run_of_record listing) contain `e_seal1_text.gates_only`. Its schema is `UNT_KMAX_TAIL_COMPARISON_C2V007_R11_GATES_ONLY` and `test_mode` is false.
  - In that body, `gates.B0_RO1 = {status MISSING, codes [GATE_RECORD_MISSING:B0_RO1], record_sha256 null}`, and the same holds for B0_N3. B0 reads PASS.
  - The dry run's stand-in manifest `44ad5b099ef80e33627e8180b8f29cb2df1eee7666d963c73d549e9803cfc7c9` has a `gates` object identical to e5967bb9's (jq equality). It differs only in having 0 identity_runs, against 3 in the real manifest. A null gate path is MISSING whatever the identity runs are (evaluate_gate returns before reading anything), so the real ROOT-mode run gives the same two MISSING verdicts. That last step is FORMAL.
- **Class.**
  - (b) applies: a sealed gate verdict that differs from the verdict on the genuine records (MISSING instead of the PASS the registered records give), for two NO_RUN gates, and a required E-SEAL1 element (r6 srr[0], the RO1 replay) that would not be sealed. This is "failing to seal a required one".
  - (a) also applies: it happens with the selected script, the selected env block and the real inputs, with no forged or malformed input.
  - Refutation attempts that failed:
    - no other step evaluates these records before the seal;
    - the slot draft has no slot for them;
    - the registry pin binds their shas, but not their gate evaluation;
    - no root ruling found (A107-A121, 0657-0665) keeps them out of E-SEAL1.
  - Root may still rule it a disclosure-only matter. The post-run full compare reads the gates again, provided its own manifest names these records. That is root's call; under the brief's definitions it is BLOCKING.
- **Remedy (for Claude3 and root).**
  1. Write a gates manifest that also names the two records of record.
  2. Repin MANIFEST_GATES in a new script, then rerun the dry run and the suites.
  3. Optionally (NOTE N5), add a check that every V012 pre-seal gate reads PASS in GATES_ONLY.
- **Corroboration.** Unselected objects appeared during this review, and I did not review them:
  - `MANIFEST_GATES_ONLY_C3SA_c3v002.json` `46dc53104d518edc9b00e77c0b4995df3e4871999c7264926dad186726ed62ca` (mtime 2026-10-19T06:44:23Z) equals e5967bb9 except that `B0_RO1` and `B0_N3` now name the two ri33_c3 records. Its note still says "registry V009".
  - `ROOT_SEAL_STEPS_c3v027.sh` `239a51c34439b9510155762db8ba02709f1a478b3601de371799ec78591df02f` (about 06:46Z) differs from c3v026, in non-comment lines, only in that MANIFEST_GATES pin.
  - `c3v011_prestage/` and `dry_run_20261019T064733Z/` are also new.
  - Claude3 appears to have found the same gap. SELECTED c3v010, as selected, still carries it.

## Task 1: diff c3v025 -> c3v026 (11 hunks, all attributed)
| # | c3v025 L -> c3v026 L | change | attribution |
| --- | --- | --- | --- |
| H1 | 2 -> 2 | header file name | comment |
| H2 | 5 -> 5-15 | new c3v026 supersession paragraph: V012 (I4 c3v003 707395ba), V006, P7/P8/P9 recorded | comment (0663, 0665, A121) |
| H3 | 168-169 -> 178-179 | P table, P7 "env (owner TBD)" -> "env (A121: CX3V001)"; P8 "env (root)" -> "env (A121: External1)" | comment (A121) |
| H4 | 183-185 -> 193-195 | P14 V011 -> V012 4b8a3c35 (VALIDATE a7c80f8e, draft c3v007); P15 V005 -> V006 8dc28480 | comment (0665, A121) |
| H5 | 217-220 -> 227-231 | input-list comments P7 86c89730, P8 External1, P10 300 (0659), P9 (A121) | comment (A121, 0659) |
| H6 | 246 -> 257 | DRAFT c3v006 f542e394 -> c3v007 184ff5cb; the draft diff is producer_registry path+sha only, V011 -> V012 (TESTED: raw diff) | functional: registry V012 (0663/0665/A121) |
| H7 | 262-266 -> 273-277 | DISCLOSURES V005 b1a7b3d5 -> V006 8dc28480; DISCLOSURES_SUPERSEDED_SHAS += V005 b1a7b3d5; comment names c3v003 and V012 | functional (0665/A121) |
| H8 | 284-286 -> 295-298 | REGISTRY V011 512a7171 -> V012 4b8a3c35 (+ comment) | functional (0663/0665/A121) |
| H9 | 418 -> 430 | step-0 refusal text "A112: V002" -> "root 0665: V006" | message text |
| H10 | 779 -> 791 | summary root_next C-08 string: "root V003, A116" -> "root V006, 0665" | SEAL_ASSEMBLY_SUMMARY text only |
| H11 | 790 -> 802 | summary manual_disclosures label "V003 per A116" -> "V006 per root 0665" | SEAL_ASSEMBLY_SUMMARY text only |

Result:
- 7 non-comment lines changed: DRAFT, DISCLOSURES, SUPERSEDED, REGISTRY, the refusal text and 2 summary strings. This matches the README's claim.
- No hunk is unexplained.
- The I4 producer c3v002 -> c3v003 is named only in comments (L6-L9, L274, L295-297). The script reaches the I4 producer only through the V012 pin, which is correct.
- The env-block expectations P7, P8 and P9 are comments only. REQUIRED_ACK (L340) is unchanged and equals A121's string exactly (TESTED).

## Task 2: c3v020 (SELECTED c3v009's script) -> c3v026, functional changes (non-comment diff)
| change | lines in c3v026 | tie |
| --- | --- | --- |
| compare r13 -> r14: COMPARE_R13_SHA -> COMPARE_R14_SHA f3f9ba7e (L333, L431); COMPARE_SUPERSEDED_SHAS += r13 f5adfd11 (L332); new COMPARE_R14_SELECTION_SHA 6b650ece check (L334, L432); IMPL_R14 2ba6d12e pinned (L269, L465) and the selection must name it as `implementation` (L480-482) | as listed | A114 (0651), A116 (0654: slot value r14, IMPL r14), A117 (compare of record); README "c3v021, pre-stage (A114/A116)" |
| draft c3v003 e12292a2 -> c3v007 184ff5cb; step 0 requires draft compare_reviewed_source = the reviewed compare (L501-502); step 3a no longer fills COMPARE_REVIEWED_SOURCE at run time | L257, L501-502, L615-621 | A116, Claude4 0133 (README c3v021) |
| registry V009 32ddadcb -> V012 4b8a3c35 | L298 | A113 RI-33 + A114.2 (V010: B0_N3, B0_RO1, I4), A119 (0660/0661: V011), A121 (0663/0665: V012) |
| disclosures V002 a0284ece -> V006 8dc28480; superseded V001 -> V001..V005 | L276-277 | 0658 (V003, A116), 0661 (V004, A119), 0662 (V005, A120), 0665 (V006, A121) |
| B7 inputs become constants: NEW-item COMPLETE 68164144 and custody 9ca16b4f; env UNT_SEAL_NEW_ITEM_LIST_* / UNT_SEAL_SUCCESSOR_CUSTODY_* removed from `need` and refused if set; PENDING guards; step-0 and step-10 pins; tool 4 --new-item-list / --successor-custody | L301-302, L413-416, L424-426, L468-469, L722-723, L732-733 | A118 (COMPLETE; custody Option A), root 0658 (pin in c3v010), 0659 (custody written), A119; README c3v022 |
| env inputs P2, P5-P10: names unchanged; values only in the SELECTED block (P2 r14; P5 6a3fa535; P6 72a21888; P7 86c89730; P8 External1; P9 ack; P10 300) | comments; REQUIRED_ACK L340 unchanged | A113 (P5 entries [], RI-30 key map, P10 300), 0659 table, A121 (P7, P8, P9) |
| step 3b C-04 with the A107 exclusions: code unchanged since c3v012; it now loads r14's loader against V012 through the two pins above | L626-633, L336-337 | A107 (exclusions), A114/A116 (r14), A121 (V012) |
| tool 4 v004 wiring: unchanged since c3v020 except the inputs above (B7 constants, V006) | L729-734 | A110, A112 (593c59fa), 0658/0659, 0665 |
| summary strings (C-08 root_next names IMPL r14 and V006; manual_disclosures label V006) | L791, L802 | A116.3, 0665 |

- No functional change was found that cannot be tied to a ruling or dispatch.
- One required consequence of the registry change was not carried: the step-8 manifest (SCRIPT-B1).
- The SELECTED's `root_messages_read` lists 0659, 0661, 0662, 0663, 0664 and 0665. 0658 is cited in the script and the README. 0651, 0654, 0657 and 0660 are reached only through the V006 addendum rulings (A114, A116, A118, A119).

## Task 3: every sha constant against bytes; the step-0 seal-tools role check
- **Fenced script.** `check_script_c3v026_c4v002.py`, sha `e958d738137ed1c684f5fa6607b3d93be55d24b43fe158363fb6b5117e950506`.
  - It parses the script text: every top-level `X=`/`X_SHA=` pair with `$A`, `$CTRL`, `$PKT`, `$C3`, `$TD` and `$SFX=""` expanded, plus the C04_EXCLUSIONS and TOOL_PINS arrays.
  - It hashes the named files after a pure-string protected-path test.
  - Its output is `CHECK_SCRIPT_C3V026_C4V002.json`, sha `d3bc16a8821507d2728db05c8aec7b0bd070cdeed3190fd0b543e06746cc18b9`.
- **Pin results.** 48 path/sha constants checked; 0 mismatches; 0 symlink or missing components (an lstat walk of every prefix).
  - HELPER, FENCE, RUNNER, DRAFT and MANIFEST_GATES.
  - PREREG_TOR, R6_SELECTED, CASE_BLOCK, IMPL_R13, IMPL_R14 and DISCLOSURES.
  - DRIVER, BINDER, TEMPLATE, BUILD, ALLOWLIST, PRODUCER_INDEX, GUARD and LAUNCHER.
  - REGISTRY, B7_NEW_ITEM_LIST, B7_SUCCESSOR_CUSTODY, IDREC_Z2/Z2OFF/B0P, B0_RECORD and B2_RECORD.
  - V003_SELECTED, V004_SELECTED, the 6 tools, V003_README, V004_README and DRIVER_CHECK_RECORD.
  - C04_EXCLUSIONS (2) and TOOL_PINS (6).
  - PY: the realpath of the pinned interpreter, `python3.12`, hashes to `8506f337a83611246ffcff62d6e96c6d2269e5db48508ca3ac2553d56c962aee` = PY_REAL_SHA.
  - OPEN_V005: `c01b3c51e34501d77e474594cc0b4be72c6e068c7f58a595055316313a8d4bb1`, 143081 bytes = V005_FINAL_SHA and V005_FINAL_BYTES.
  - C04_EXCLUSIONS equals the helper's own C04_A107_EXCLUSIONS constant (ast-parsed, not executed).
  - The env-block files (r14, SELECTED_R14_CX1V002, P5, key map, P7) match their env shas with no symlink component. COMPARE_R14_SHA and COMPARE_R14_SELECTION_SHA equal them.
- **Superseded lists.**
  - DISCLOSURES_SUPERSEDED_SHAS equals the bytes of V001..V005, in order. The V006 pin is not in it.
  - COMPARE_SUPERSEDED_SHAS = r12_cx3v002 4bd7b262, r11 a5d10cb1, r10 e801adc4 and r13 f5adfd11, each matched to its round file. r14 is not in it. See NOTE N3.
- **Skipped (protected), never touched.**
  - UNT_SEAL_C5H_RUN_DIR: compared as a string only.
  - INTERNAL_OUTPUT_ROOT `/Users/bgm/Research/UNT_INTERNAL_RUNS/V007_STEP2_R5_BUILD_V007`.
- **Step-0 seal-tools role check (L454-459), TESTED.** The 10 role pins equal `SELECTED_SEAL_TOOLS_V004_C4V001.json` `593c59faf39074b14579f927ae17c5aeda1f7450ee4a9f264f96a1f2c7b195e0` files.<role> exactly, path and sha, and the schema is equal:
  - seal_common 101a3aeb;
  - tool_1 a56f8d79, tool_2 c2c5dfc5, tool_3 316973a1, tool_4 9787cf58, tool_5 e5bedffe;
  - readme_v003_run_order 86012117, readme_v004_delta cec2bfc9;
  - selected_r6 7200acd9;
  - selected_v003_superseded_for_the_seal cf7e5b2f.
  - The V004 role `root_manual_disclosures_file` (V001, superseded) is correctly not used.
- **r6 role check (L437, L442-445), TESTED.** text_of_record d28c95f5, addendum_at_text_of_record c01b3c51, case_block 76309ae3, impl_of_record_r13 274f7049 and closed_v005_live c01b3c51 all equal SELECTED_R6 files.<role>.
  - The addendum_at_text_of_record pin is derived by `tor_table_bytes` from the TOR's byte_copy. That value has a trailing note after a space, which `${bc%% *}` strips, and the derived path is inside r6/.
  - The TOR binds the case block.
  - V006 `e_r6_1_text` equals r6 `basis.erratum_E_R6_1`, and V006 has exactly the 5 keys.

## Task 4: A115 (a) and (b); what each step checks and seals
| step (lines) | checks | writes / seals | real-run-only exposure, verdict |
| --- | --- | --- | --- |
| 0 (404-519) | seal dir absent; PY sha; utf8, (3,12), -B; helper+runner shas; PENDING scans; `need` 13 vars; 8 stale vars refused; ack; GiB digits; compare/disclosures not superseded; r14 + selection shas; C5H suffix; P5 under $CTRL/V007_SEAL_ASSEMBLY_INPUTS; check-tor; r6 roles; case-block binding; check-disclosures V006; V004 roles; 33 pins + 6 tool pins; selection names r14 + IMPL r14; draft pins (driver, registry, build, launcher/guard, identity records, check record, compare slot, C04 pins, attempt-1 documented output paths); outputs absent; output root check | nothing | TESTED here: all conditions, including the real-run-only `DRAFT_PATHS_MUST_MATCH=1` paths (the dry run set them to 0), outputs absent (FROZEN, SEAL_DIR, BOUND_PLAN, BOUND_COMMAND, CONFIG), env names (13 need = 13 block vars; 8 refused = do_not_set; no other UNT_SEAL_* referenced but UNT_SEAL_ATTEMPT). Output root: protected, FORMAL (helper L1311-1383 accepts an existing real UNT_INTERNAL_RUNS parent; free at a same-volume proxy 397.94 GiB >= 300) |
| 1 (522-534) | open V005 = c01b3c51 and 143081 bytes | FROZEN exclusive copy at $CTRL/..._V005_ADDENDUM_FROZEN.md (= r6 path_to_be, TESTED) | OK |
| 2 (537-556) | dispositions object (P5); tool 1 with --expect-frozen-sha and --addendum-at-text-of-record; rehash | logs | tool 1 D-10 (dry run used --allow-open-copy): path_to_be = FROZEN and CTRL realpath = literal (TESTED) -> passes FORMAL |
| 2a (559-574) | tool 5; check-driver-build-record (fenced) | DRIVER_BUILD_RECORD exclusive | OK (dry run) |
| 3 (577-609) | 41 template outputs fresh; output root create; binder; C-05/C-06 bound-check | output root (new, empty); BOUND_PLAN, BOUND_COMMAND in $PKT/P128 | 41 unique strings under the root (TESTED, strings only); P128 a real dir, outputs absent (TESTED) |
| 3a (612-623) | fill from draft c3v007 + runtime FROZEN, DBR, BOUND_*, CASCADE (P7) | SLOTS_FINAL | OK |
| 3b (626-633) | C-04: r14 loader, V012, A107 exclusions | log | OK (echo text stale, N1) |
| 4, 4a, 5, 5a (635-676) | sealed prereg = r6 + slots; C-02; tool 3; sealed compare (5 pins); tool 2 | SEALED_PREREG, SEALED_COMPARE | OK (dry run; the real tool 3/4 runs use the pinned runner, not the dry-run shim) |
| 8 (679-694) | check-manifest gates-root (identity_runs = the 3 identity records' run.path, TESTED equal, all /Volumes/External1 spellings; gate paths pass the no-follow walk, TESTED); gates-only ROOT mode (fence ROOT self-test expectation consistent by reading fence L78-106 against helper L577-578); C-03 | GATES_ONLY.json = E-SEAL1 gates | **SCRIPT-B1**. The identity-run trees (runs_ext) were not checkable for symlinks (N6) |
| 9 (697-713) | make-c5h-manifest + check-manifest c5h: P8 an exact member of the sealed compare's C5H_REGISTERED_RUN_DIRS (TESTED with the helper's _module_strings rule re-implemented; r14 L256-258, 2 entries; same in the dry-run sealed compare); runner runs the sealed compare --validity-only --case C5H | C5H manifest, VALIDITY_ONLY.json | Never executed by any dry run (S15 stub). FORMAL: r14 sealed validity-only reads cases.C5H as given; the C5H interlock and identity stats run only in test-mode full mode (L1830, L1851, L2108, L5739, L5745). CLI flags match the helper sub() table |
| 10 (716-737) | C-02; tool 4 v004 (B6 outputs, B7 constants, key map, V006) | candidate record | OK |
| 11 (740-752) | SEAL_RECORD sha = tool 4 stderr; R-02 V006 verbatim | SEAL_RECORD (exclusive) | OK |
| 12 (755-769) | make-config (W7-S1 15 rows; guard self-check; `config_is_guard_CONFIG` must be True); check-config-allowlist; tool 4 admission | ROOT_SEAL_ADMISSION_V001.json | guard v008 `CONFIG = Path(__file__).resolve().parent/'ROOT_SEAL_ADMISSION_V001.json'` resolves to the script's CONFIG (TESTED) -> True |
| 13, summary (772-804) | receipt; output root still empty | receipt, summary | OK |

- **(a) Refusal or wrong seal on the real inputs.**
  - SCRIPT-B1 is a wrong seal. It causes no refusal.
  - No other path was found:
    - no check expects an old sha;
    - the env-var names match the selected block exactly;
    - every file the real layout must hold exists with the pinned bytes and no symlink component;
    - every output is absent;
    - the guard CONFIG and the D-10 path_to_be equal the script strings;
    - P8 is an exact registered spelling.
  - Unverifiable residuals, all protected: see N6.
- **(b) Superseded or missing objects.**
  - No superseded compare, registry, disclosures, prereg or case block can be sealed. The compare is r14 by equality. The registry is V012 by pin plus the draft cross-check. Disclosures V001-V005 are refused. The prereg is r6 and the case block 76309ae3 by role.
  - Every required object is pinned, except the step-8 evaluation of B0_RO1 and B0_N3 (SCRIPT-B1).

## NOTEs (A115: none blocks)
- **N1. Stale run-log echoes and comments; text only.**
  - L627 step-3b echo: "through r13's own load_producer_registry against V009". The arguments are r14 and V012.
  - L636 step-4 echo: "sealed prereg = r5".
  - L453 comment "the disclosures pin is root's V002" and L746 comment "carries the V002 disclosures file". The pin is V006.
  - L199: "C-08 ... against the r13 IMPL of record". A116.3 moved it to r14, as the summary L791 says.
  - L625: the "STEP 4 (B4)" banner sits above step3b_c04.
  - L6: calls the c3v002 defects "A115 (a)". A121 classes D1 as (b) and D2/D3 as (a).
- **N2. Root 0659 wording against the selected block.** 0659 says to "Pin it ... as `UNT_SEAL_SUCCESSOR_CUSTODY_PATH` / `_SHA256`", while c3v026 refuses that env var (L425-426). The selected block and README tell root not to set it. If it is set, step 0 refuses before anything is written, which is safe.
- **N3. An r12 file outside the superseded list.** `kmax_tail_compare_c2v007_r12.py` (73031283) is not in COMPARE_SUPERSEDED_SHAS. This does not matter, because L431 requires r14 exactly.
- **N4. Free-space margin.** 397.94 GiB free on the Data volume (measured at /Users/bgm/Research/UNT_EXCHANGE) against the P10 floor of 300 GiB. The helper measures at the output root's parent. If live runs consume the margin, step 0 or step 3 refuses. That is a refusal, not a wrong seal.
- **N5. Hardening, optional.** No step requires every registered pre-seal gate to read PASS in GATES_ONLY: C-03 covers the 8 slotted gates only. Adding that check with the SCRIPT-B1 fix would make an omission like this one refuse instead of passing silently.
- **N6. Unverifiable residuals under the hard rules (protected).** Each is FORMAL by source reading:
  - step 0/3: V007_STEP2_R5_BUILD_V007 is absent and UNT_INTERNAL_RUNS is a real directory on the Data volume;
  - step 8 ROOT mode: the External1 identity-run trees and their side receipts have no symlinked ancestor and no symlink inside (A121 states no symlinked ancestor for the External1 spelling);
  - step 9: compare r14's own --validity-only read of the C5H run (Claude3's README NOTE).
- **N7. New unselected objects** (see SCRIPT-B1 Corroboration): manifest c3v002, c3v027, `c3v011_prestage/` and dry run 064733Z. Not reviewed. A new selection needs its own delta. The c3v002 manifest's note still says "registry V009", which is cosmetic.

## Tests (this lens)
- Diffs: c3v025->c3v026 has 11 hunks and 7 non-comment lines. c3v020->c3v026 non-comment hunks are as tabled. Slot draft c3v006->c3v007 raw diff is the producer_registry path and sha only.
- One fenced run of check_script_c3v026_c4v002.py; see the structured output for the full test list. Its `n_problems` is 1: MANIFEST_GATES, with B0_N3 and B0_RO1 not named.
- jq: the stand-in gates equal the real gates; both dry-run SEAL_RECORDs carry B0_RO1 and B0_N3 MISSING; the slot draft has no B0_RO1 or B0_N3 slot.

## Rules and fence
- **The fence run.** FENCE_C4ST2_SUMMARY: selftest 8/8, v002 exception probes 15/15, `blocked_after_selftest []`. This was the only Python run, through the fence; there were no python -c or heredoc probes.
- **Hard rules kept.**
  - Nothing was launched. The seal script, the dry-run scripts, the helper, the runner, the compare and tools 1-5 were read as text only.
  - The C5H dir, runs_ext, UNT_INTERNAL_RUNS, UVT_* and target data were never opened, listed or stat-ed. The P8 string and INTERNAL_OUTPUT_ROOT were classified by string and skipped.
  - Directories listed, each named and non-recursive:
    - the lens folder and its parent review folder;
    - seal_assembly_c3;
    - v007_compare_c2 and r10-r14;
    - producer_registry_c3/out and seal_assembly_c3/root_inputs;
    - ri33_c3/i4 and seal_b7_inputs_c4;
    - cascade_map_r5_addendum_cx3, v007_final_prereg_c4 and seal_tools_v004;
    - v007_launch_packet_cx1 and its P128;
    - dry_run_20261019T060546Z with fixtures/ and passA/scratch_ctrl/V007_SEAL_ASSEMBLY.
  - grep was used only on single named files. Writes went only to the lens folder, by exclusive create or append to the lens's own PARTIAL.md.
- **Incidents.** No rule incident. One `grep -o` on the r6 JSON failed with a ugrep complexity error and read nothing; jq was used instead.
