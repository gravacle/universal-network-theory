# Delta r2 → r3 (KMAX_TAIL_PREREG_V007_FINAL_DRAFT)

Each line is one recorded edit applied to r2 (58a0b87d) by the r3 generator.

| # | clause | kind | added sources | why |
|---|---|---|---|---|
| 1 | `binding_inputs.successors` | rewritten | A69; A72.1; A72.3; A58 RI-01 | r4 pins superseded by r5 (A58 RI-01) and the A72 r5/r6 branch |
| 2 | `binding_inputs` | restructured | 0580 item 2 | r2 r4-era and pre-slot pins moved to binding_inputs_superseded_r2; root-at-seal values moved to seal_slots |
| 3 | `fixed_across_all_cases.production_tail.P` | rewritten | A58 RI-05; A62 (S4T note) | RI-05 ruled |
| 4 | `fixed_across_all_cases.production_tail.quadrature` | rewritten | A58 RI-03 | RI-03 ruled |
| 5 | `fixed_across_all_cases.production_tail.gas` | extended | A60; A64.2; A68 CHK-1; A75.8; A79 NEW-67; A80 | NGC K_big/M_s and the M_s binding |
| 6 | `fixed_across_all_cases.production_tail.memory_guard` | rewritten | A72.1 | driver-slot branch |
| 7 | `fixed_across_all_cases.production_tail.tail_table_cache` | new | A72; A72.3; A78 | new ruling A72 |
| 8 | `fixed_across_all_cases.brackets` | sources | A58 RI-05 | RA4 case list C4T-KLO/KHI ruled |
| 9 | `fixed_across_all_cases.route_a` | extended | A77 N7; A77.2 | A77.2 role table |
| 10 | `pairing_and_decidability_rule.noise_allowance` | rewritten | A58 RI-18 | RI-18 ruled: the q cap of 0.9 is removed (stricter) |
| 11 | `pairing_and_decidability_rule.if_not_decidable_R_PAIR` | extended | A69 (AMB-07); A77.2 | tie-break and role table |
| 12 | `gates_before_any_T_result.B1_Z2` | rewritten | A58 RI-11; A58 RI-12; A59; A67 N1; A73 SF2; A74; A76 | Z2 rulings A58-A76 |
| 13 | `gates_before_any_T_result.Z2_OFF_RO1` | rewritten | A67; A67 N1; A72.3; A74; A76 | comparator and driver slot |
| 14 | `gates_before_any_T_result.B0prime_RERUN` | extended | A67 N1; A72.3; A74 | comparator and driver slot |
| 15 | `gates_before_any_T_result.B0_RO1` | extended | A79.1 | A79 blocking item 1 |
| 16 | `gates_before_any_T_result.B0_N3` | extended | A79.1 | A79 blocking item 1 |
| 17 | `gates_before_any_T_result.EPS` | rewritten | A58 RI-17; A64.2; A67 N4; A68; A70 | coverage and record rulings |
| 18 | `gates_before_any_T_result.LO` | rewritten | A58 RI-06; A68 CHK-1; A69.2; A70; A71; A73 F2; A75 A01; A75.8; A79 NEW-67 | RI-06 partition and record rulings |
| 19 | `gates_before_any_T_result.GQ` | rewritten | A64.2; A67 SF1; A67 SF2; A68 CHK-1; A70; A75 A05; A75.6; A79.1; 0544 | GQ record rulings |
| 20 | `gates_before_any_T_result.DOUBLING` | rewritten | A58 RI-03; A73; A79 NEW-61; A79 NEW-67 | DOUBLING rulings |
| 21 | `gates_before_any_T_result.RB_FP` | extended | A62.1; A67 N3; A69.2 | shell coverage |
| 22 | `gates_before_any_T_result.HARMONIC` | extended | A79.1 | A79 blocking item 1 |
| 23 | `gates_before_any_T_result.LO_NGC` | extended | A64.2; A75 A01; A79.1; Codex1 0049 (state only) | NGC coverage |
| 24 | `gates_before_any_T_result.record_verdicts` | extended | A67 (order N1); A73 | record states |
| 25 | `gates_before_any_T_result.no_last_wins` | new | A71; A74; A75.1; A75.2; A75.3; A79.1; A79.4; A79.6 | new ruling A71 (systematic) |
| 26 | `gates_before_any_T_result.after_seal_marker_policy` | new | A79 NEW-61 (as corrected 17:16Z); A75.7 (corrected by A79); A67 N2; A62.2; A69 | A79 NEW-61 corrected |
| 27 | `gates_before_any_T_result.c5h_interlock` | new | A72 (H-07); A75.4; A79.3; A79.5; A79 NEW-64 | H-07 rulings |
| 28 | `gates_before_any_T_result.blinded_output` | new | A75.5; A79.2; A76 (SF-ARGV) | blinding rulings |
| 29 | `gates_before_any_T_result.certificate_ms_binding` | new | A68 CHK-1; A68 (records); A73 F2; A75.8; A79 NEW-67 | M_s binding |
| 30 | `tests.T1_S` | extended | A62 (S4T note); A58 RI-05 | S4T wording |
| 31 | `tests.SR_K` | extended | A62.2; A67 N2; A79 NEW-61 | SR_K record rulings |
| 32 | `decision_rule.ADOPT_TAIL_cube_K4_C4T` | extended | A71; 0580 | slots and no-last-wins |
| 33 | `outcomes_first_applicable.NO_RUN` | extended | A67 (order N1); A71 | record rulings |
| 34 | `outcomes_first_applicable.UNDECIDABLE_AT_ITERATION_FLOOR` | extended | A67 NEW-31 | NEW-31 accepted |
| 35 | `ngc3198_N_tests` | extended | A62; A64.1; A64.2; A64.3; A66 | NGC K_big 32 and N1 consequence |
| 36 | `run_list.DDO_gates` | rewritten | A67; A72.3; A74 | identity reruns |
| 37 | `run_list.DDO_tests` | rewritten | A70; A72.3; A78; 0576 | spec set and launch |
| 38 | `run_list.contingent` | extended | A68 | gates_v004 result |
| 39 | `run_list.replays` | extended | A73; A79 NEW-61 | record timing |
| 40 | `run_list.NGC` | rewritten | A64.2 | K_big 32 |
| 41 | `run_list.limits` | rewritten | A61; A62; A72 (ITEM3-R1); 0559; A78 N2 | launch rulings |
| 42 | `run_list.cpu_hours_estimate_UNTESTED` | rewritten | A58 RI-09; A61 | RI-09 ruled |
| 43 | `seal_record_requirements` | extended | 0561; 0576; A58 RI-10; A59; A62; A67; A69; A78 N2 | 7 requirements added |
