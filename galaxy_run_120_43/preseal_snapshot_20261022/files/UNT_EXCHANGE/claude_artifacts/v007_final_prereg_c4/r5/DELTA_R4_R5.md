# Delta r4 -> r5 (KMAX_TAIL_PREREG_V007_FINAL_DRAFT)

Each line is one recorded edit applied to r4 (e3b6b5b2) by make_v007_final_draft_c4v005_p3.py, with its trace to a ruling (A-entry), a rehearsal defect (D-), gap (GAP-) or refuter correction (R-). Open V005 addendum at generation: 70a48f51e20311de82a37b13bee8cf18f7eaf9adbb976d957e50c5334e7c8c7e (entries A47-A101).

| # | clause | kind | added sources | trace | why |
|---|---|---|---|---|---|
| 1 | `binding_inputs.case_block` | new pin | A99.2; A101 | A99.2; A101; D-03; GAP-03; R-03 | the compare reads the case block in sealed mode only from binding_inputs.case_block {path, sha256} (r12 L5706) |
| 2 | `binding_inputs.case_block_rule` | new | A99.2; A101 | A99.2; A101; D-03; GAP-03; R-03 | what the pinned case block is and how it was built |
| 3 | `binding_inputs.gate_b3_record_A87 / gate_b3_rule` | new | A87; A101 | A87; GAP-02 (A87 evidence); REFUTE DONE row | A87: the B3 record of record is the FIELDS-shape JSON; the Markdown is the human report |
| 4 | `binding_inputs.successors` | rewritten | A96 | A96; GAP-19 | V007 seals on r5 (A96) |
| 5 | `binding_inputs.ro1_role_table` | revised | A96 | A96 | r6 moot (A96) |
| 6 | `binding_inputs.spec_set` | extended | A99.1; A99.2; A101 | A99.1; A99.2; D-02; D-03 | case block and BUILD_V007 template bound to the same ten specs |
| 7 | `fixed_across_all_cases.validity_gates` | extended | A99.2 | A99.2; D-03; R-03 | where V3 finds the registered case block |
| 8 | `fixed_across_all_cases.production_tail.gas` | extended | Codex1 0032 | A81 RI-23; Codex1 0032; R-08 | RI-23 condition evaluated from the GQ_NGC record |
| 9 | `fixed_across_all_cases.production_tail.ngc_gas_M_s` | new | A81 RI-23; Codex1 0032 | A81 RI-23; Codex1 0032; R-08 | the value the tool-3 slot ngc_gas_M_s takes, with its ruling and evidence |
| 10 | `fixed_across_all_cases.production_tail.memory_guard` | revised | A96 | A96 | r6 moot |
| 11 | `fixed_across_all_cases.production_tail.tail_table_cache` | rewritten | A89; A96 | A89; A96; GAP-19 | A96 applied A89/A72(c): r5, no cache |
| 12 | `gates_before_any_T_result.B0prime_RERUN` | revised | A92; A96 | A92; A96 | r5 run compared by c2v007r2; r6 moot |
| 13 | `gates_before_any_T_result.Z2_OFF_RO1` | revised | A92; A96 | A92; A96 | r5 run compared; r6 moot |
| 14 | `gates_before_any_T_result.B1_Z2` | revised | A92 | A92; GAP-07 | the comparator of record |
| 15 | `gates_before_any_T_result.B2` | extended | A94; A97; A100; A101 | A94; A97; A100; A101; R-15; GAP-15 | B2 rulings A94/A97/A100/A101 |
| 16 | `gates_before_any_T_result.GQ` | revised | A86 | A86; GAP-02 (A86 evidence) | A86.1 GQ record of record |
| 17 | `gates_before_any_T_result.DOUBLING` | extended | A87 | A87; A73; D-01; R-13; GAP-11 | DOUBLING record of record and its M_s field |
| 18 | `gates_before_any_T_result.LO_NGC` | extended | A87; A90 | A87; A90; GAP-12 | LO_NGC records named |
| 19 | `gates_before_any_T_result.after_seal_marker_policy` | rewritten | A88; A99.5 | A88; A99.5; GAP-20 | SR_K joins the after-seal set |
| 20 | `tests.SR_K` | revised | A88; A69 | A88; GAP-20 | A88: SR_K after the seal |
| 21 | `run_list.DDO_gates` | rewritten | A92; A96 | A92; A96; GAP-08 | r5 identity runs done and compared |
| 22 | `run_list.DDO_tests` | rewritten | A96; A99.1; A99.2 | A96; A99.1; A99.2; D-02 | r5 only; BUILD_V007 template |
| 23 | `run_list.replays` | extended | A88 | A88 | SR_K after the seal |
| 24 | `run_list.limits` | revised | A99.1 | A99.1; D-02; GAP-09; GAP-21 | BUILD of record V007 |
| 25 | `run_list.cpu_hours_estimate_UNTESTED` | rewritten | A89 | A89 | measured cost |
| 26 | `scope_untested` | revised |  | A89; A96; A100 | cache saving measured and moot; B2 limit |
| 27 | `outcome_branch_tests_required` | revised |  | A96; GAP-06 | the final round named |
| 28 | `not_v007_text_scope` | revised | A93 | A93 | registry named in the scope note |
| 29 | `seal_record_requirements[2]` | revised | A82 (RI-27) | A82 | RI-27 ruled |
| 30 | `seal_record_requirements[4]` | revised | A82; A96; A99.6 | A82; A96; A99.6; GAP-01 | no write after the freeze; r5, no cache |
| 31 | `seal_record_requirements[8]` | rewritten | A82; A96 | A82; A96; D-06; GAP-04 | the five pins; the driver BUILD record created at assembly |
| 32 | `seal_record_requirements[10]` | rewritten | A99.1 | A99.1; D-02; GAP-09; GAP-21 | BUILD_V007, 15 sources |
| 33 | `seal_record_requirements[11]` | rewritten | A99.3 | A99.3; D-05; GAP-02; R-02 | the entry table quoted; rows re-hashed at the freeze |
| 34 | `seal_record_requirements[12]` | new | A100; A101 | A100; A101; R-15 | B2 disclosure in the seal record |
| 35 | `seal_slots.frozen_addendum` | rule extended | A82 (RI-27); A99.6 | A82; A99.6; GAP-01; D-10 | no write after the freeze |
| 36 | `seal_slots.driver` | branch fixed | A89; A96 | A96; GAP-19 | r5 |
| 37 | `seal_slots.compare` | rule rewritten | A83; A86; A90; A91; A96 | A83; A86; A90; A91; A96; R-02; GAP-06 | the final round r12 and its reviews of record |
| 38 | `seal_slots.identity_comparator` | rule rewritten | A83; A91; A92 | A83; A91; A92; R-02; GAP-07 | c2v007r2, the check of record |
| 39 | `seal_slots.identity_gate_records` | candidates named | A92; A101 | A92; GAP-08 | R5_V001 records of record |
| 40 | `seal_slots.launch_packet` | rule rewritten; build bound | A87; A88; A99.1 | A99.1; D-02; GAP-09; GAP-21 | BUILD_V007 is the BUILD of record (filled from bytes) |
| 41 | `seal_slots.certificates` | rule rewritten; candidates named | A86; A87; A90; R-13; Codex1 0032 | A86; A87; A90; A81 RI-23; D-01; R-13; GAP-11; GAP-12 | records of record; M_s field names |
| 42 | `seal_slots.producer_registry` | rule rewritten; candidate named | A88; A92; A99.5; A100; A101 | A87; A88; A92; A99.5; A101; GAP-13 | what the registry of record carries |
| 43 | `seal_slots.cache_directory_r6_only` | value fixed by A96 | A96 | A96 | NOT_APPLICABLE_R5 |
| 44 | `root_items.RI-27, RI-24` | resolved | A82; A96 | A82; A96 | RI-27 ruled; RI-24 moot |
| 45 | `root_items.RI-28..RI-37` | new |  | A81 RI-20; A99.1; R-10; R-09; GAP-18; GAP-14; A99.3; D-09; GAP-05; A88 | open items at r5 |
| 46 | `entries_after_A81` | new | A81 RI-26; A99.3 | A99.3; D-05; GAP-02; R-02 | the entry-by-entry table A82-A101 |
| 47 | `status / assembly / decision_pins_pending_at_seal / cites_by_name` | header |  | A99; A99.3 | r5 header and cited range A47-A101 |
