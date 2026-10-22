# Delta r5 -> r6 (KMAX_TAIL_PREREG_V007_FINAL_DRAFT)

Each line is one recorded edit applied to r5 (3245899f) by make_v007_final_draft_c4v006_r2.py, with its trace to a ruling (A-entry) or a finding of the r5 check (F-; REPORT_R5CHK_C4V002 caea77aa). The item column is the r6 brief item: 1 the entry table, the closed V005 and the header; 2 the compare slot; 3 the launch packet; 4 the seal record requirements; 5 the F-11 fixes; 6 F-13; 7 the registry; 9 seal tools v003. Item 8 (the case block binding) changes nothing. Rows named SEAL_CHECKLIST_R6 are edits of the root checklist. Closed V005 addendum at generation: c01b3c51e34501d77e474594cc0b4be72c6e068c7f58a595055316313a8d4bb1, 143081 bytes (entries A47-A106; byte copy addendum_read/V005_ADDENDUM_READ_AT_R6_GENERATION.md).

| # | item | clause | kind | added sources | trace | why |
|---|---|---|---|---|---|---|
| 1 | 2 | `seal_slots.compare.rule` | rule rewritten | A102; A103; A104; Claude3 0092; Codex1 0076 | A102; A103; A104; A106.1; A81 RI-20; F-01; F-02 | the final round is r13 with its reviews of record (Claude3 0092, Codex1 0076); r12 superseded; F-02 (A106.1): a blocking item means a fix round, never a seal on that round, and r5's "or a ruling on the item" is removed; the sealed compare sets only the five A82 pins on r13 |
| 2 | 2 | `seal_slots.compare.named_candidates_verified_from_bytes` | candidates replaced |  | A102; A103; A104; F-01 | r13 (source, selection, FIELDS, IMPL, HASHES) and its two reviews of record, from bytes; r12 and its reviews kept as superseded (A102) |
| 3 | 2 | `outcome_branch_tests_required` | revised |  | A102; A104; F-01 | the final round named: r13 |
| 4 | 2 | `root_items.RI-28` | resolved | A102; A103; A104; Claude3 0092; Codex1 0076 | A102; A104; F-01 | the r12 A-B1 item: fix round r13 (A102), the compare of record (A104) |
| 5 | 1 | `not_v007_text_scope` | revised | A103 | A103; F-01 | A103: the step-5 NGC driver is cx3r008 (r5's scope-note sentence was false after A103) |
| 6 | 3 | `seal_slots.launch_packet.rule` | revised | A105; Claude4 0108 | A105; F-01 | BUILD_V007 delta 0108 (0 blocking) and A105's rulings W7-S1, RP-S1, RP-S2; BUILD_V007 stays bound (A105) |
| 7 | 3 | `seal_slots.launch_packet.pending_parts` | revised |  | A105; F-01 | the delta check is done (0108: 0 blocking) and BUILD_V007 stays bound (A105); the bound plan and command stay PENDING by design |
| 8 | 3 | `seal_slots.launch_packet.named_candidates_verified_from_bytes` | extended |  | A105; F-01 | the 0108 review pinned; BUILD_V007 re-verified from bytes at r6 generation (the r5-generation record is kept as written) |
| 9 | 3 | `root_items.RI-29` | resolved; the seal tool named as v003 | A105; Claude4 0108; A106.2 | A105; A106.2; F-01 | BUILD of record: delta 0108 PASS_WITH_FINDINGS, 0 blocking; it stays bound (A105); item 9: the recommendation names seal tools v003 |
| 10 | 4 | `seal_record_requirements[0]` | extended | A105 | A105; F-01 | E-OPS5 disclosed in the seal record's E-SEAL1 block (A105) |
| 11 | 4 | `seal_record_requirements[4]` | revised |  | A82; F-11 | F-11(c): the order of record names the driver BUILD record step that [8] and checklist B2a place before the sealed compare |
| 12 | 4 | `seal_record_requirements[13]` | new | A106.2; Claude4 0109; 0643 | A106.2 | A106.2: the seal record states which of C-02 to C-08 the seal script checked and which root checked by hand |
| 13 | 5 | `binding_inputs.case_block_rule` | revised | A104 | A104; F-11 | F-11(d): the line citation moves to r13, verified from bytes (r12 L5706 = r13 L5708) |
| 14 | 5 | `fixed_across_all_cases.validity_gates` | revised | A104 | A104; F-11 | F-11(d): r12 L5706 = r13 L5708, verified from bytes |
| 15 | 5 | `gates_before_any_T_result.after_seal_marker_policy` | revised | A104 | A104; F-11 | F-11(d): the citations move to r13 (L338 and L341 unchanged, verified from bytes) |
| 16 | 5 | `gates_before_any_T_result.B2` | revised |  | F-11; A94 | F-11(b): the clause separator before "A94:" |
| 17 | 5 | `root_items.RI-20` | status pointers added | A83; A86; A91; A96; A102; A103; A104 | A83; A102; A103; A104; F-11 | F-11(a): the RI-20 status names how A81 RI-20 was applied (the r4 "three recheck lenses" criterion was replaced, A83) |
| 18 | 5 | `root_items.RI-21` | status pointers added | A83; A92 | A83; F-11 | F-11(a): the RI-21 status names A83 (the r4 "own check" criterion was replaced) and A92 |
| 19 | 6 | `fixed_across_all_cases.production_tail.ngc_gas_M_s` | revised | r5 check F-13 | F-13; A81 RI-23 | F-13: root's checklist-A7 confirmation of the lane record is recorded in the SEAL_RECORD |
| 20 | 7 | `seal_slots.producer_registry.named_candidates_verified_from_bytes` | candidate named; V008 superseded | A106.1; Claude3 0092 | A101; A106.1; Claude3 0087 | C3V009 is the candidate (A101; Claude3 0087; A106.1), C3V008 superseded; V009 also passes on r13 (f14dd9a6); the slot rule is kept |
| 21 | 1 | `entries_after_A81.rows` | rows added |  | A99.3; A81 RI-26; A106.1; F-01 | rows for A102, A103, A104, A105, A106 (each revised here, naming its clauses), section sha256 from the closed bytes; the 20 r5 rows re-hash unchanged |
| 22 | 1 | `entries_after_A81.rule` | revised | A106.3 | A99.3; A106.3; F-01 | the table covers A82-A106; V005 closed at A106 (A106.3); later root rulings are V006 entries, not V005 entries |
| 23 | 1 | `entries_after_A81.addendum_read` | revised |  | A99.3; A106.3; A106.2; F-01 | the closed bytes: sha256, size and the r6 byte copy (the bytes seal tools v003 tool 1 takes as --addendum-at-text-of-record, C-01) |
| 24 | 1 | `seal_record_requirements[11]` | rewritten | A104; A106.2; A106.3; 0633; 0640; Claude4 0110 | A99.3; A104; A106.2; A106.3; F-01 | the table covers A82-A106; the frozen copy equals the closed bytes (A106.3); seal tools v003 tool 1 and its input (item 9); the D-05 rule (A104) |
| 25 | 1 | `root_items.RI-34` | resolved | A106.2; A106.3; 0633 | A106.3; A106.2; F-01 | A106.3: V005 closed at A106 and the table ends there; item 9: v003 refuses bare --covered-later names |
| 26 | 1 | `seal_slots.frozen_addendum.rule` | extended | A106.3 | A106.3 | A106.3: the frozen copy must equal the closed V005 bytes |
| 27 | 1 | `decision_pins_pending_at_seal.V005_addendum_frozen_copy.entries` | revised |  | A106.3; F-01 | the cited range A47-A106; the frozen copy must equal the closed bytes (A106.3) |
| 28 | 1 | `cites_by_name[0]` | revised |  | A106.3; F-01 | the cited range A47-A106; V005 closed (A106.3) |
| 29 | 1 | `root_items (order)` | reordered by r5's rule (open first, then by id) |  | A102; A104; A105; A106.3 | RI-28, RI-29 and RI-34 are resolved, so they move into the resolved group |
| 30 | 1 | `revision` | header |  | A106.1; F-01 | r5 -> r6 (A106.1 approves prereg r6) |
| 31 | 1 | `supersedes_draft` | header |  | A106.1; F-01 | the r5 pin replaces the r4 pin |
| 32 | 1 | `status` | header |  | A104; A105; A106.1; F-01 | r6 status line: A102-A106 integrated; V005 closed; r13; BUILD_V007 stays bound |
| 33 | 1 | `assembly` | header |  | A106.1; F-01 | r6 assembly: dispatch 0643, basis, base r5, the closed-bytes check, line checks, inputs from bytes; r5's inputs kept |
| 34 | 2 | `SEAL_CHECKLIST_R6 A1` | step rewritten |  | A102; A103; A104; F-11 | F-11(e): A1 names r13 and its reviews of record |
| 35 | 6 | `SEAL_CHECKLIST_R6 A7` | revised |  | F-13; A81 RI-23 | F-13: root's A7 confirmation of ngc_gas_M_s 96 is recorded in the SEAL_RECORD |
| 36 | 9 | `SEAL_CHECKLIST_R6 A8` | revised |  | A106.2; A87 | item 9: the seal tools named are v003 (A106.2 scope) |
| 37 | 3 | `SEAL_CHECKLIST_R6 A12` | revised |  | A105 | BUILD_V007 delta done; A105 |
| 38 | 5 | `SEAL_CHECKLIST_R6 B1` | step rewritten |  | A104; A106.2; A106.3; F-11 | F-11(e): B1 lists A82-A106 and requires the frozen copy to equal the closed bytes (A106.3); item 9: v003 tool 1 and its input |
| 39 | 5 | `SEAL_CHECKLIST_R6 B2a` | revised |  | A104; F-11 | F-11(d): B2a cites r13 (the function text is equal in r12 and r13, verified from bytes) |
| 40 | 3 | `SEAL_CHECKLIST_R6 B3` | revised |  | A105 | A105 RP-S1 |
| 41 | 4 | `SEAL_CHECKLIST_R6 B7` | revised |  | A105; A106.2; F-13 | the SEAL_RECORD carries E-OPS5 in E-SEAL1 (A105), root's A7 confirmation (F-13) and the C-02..C-08 statement (A106.2) |
| 42 | 3 | `SEAL_CHECKLIST_R6 B8` | revised |  | A105 | A105 W7-S1 |
| 43 | 3 | `SEAL_CHECKLIST_R6 C1` | revised |  | A105 | A105 RP-S2 |
| 44 | 2 | `SEAL_CHECKLIST_R6 SUPERSEDED` | revised |  | A102; A106.1; A101 | compare r12 (A102) and registry C3V008 superseded; "driver r6" kept apart from prereg r6; the r5 checklist superseded by this one (A106.1) |
| 45 | 1 | `SEAL_CHECKLIST_R6 header` | header |  | A99.3; F-01 | title r6 and the assembly time |
