# Builder for ROOT_ITEMS_STEP45_V002 (dispatch 0637, FIX stage). Helper of lane Claude4.
# V002 = the V001 builder (BUILDER_ROOT_ITEMS_STEP45_C4V001.py, 5ee49788) patched for the refuter's SF-1..SF-8
# (REFUTE_ROOT_ITEMS_STEP45.md, 0a75e6d8), the state that landed after the V001 build, and the NOTEs confirmed from bytes.
# Reads only the named source files (to re-hash them), writes only into the staging dir given on argv
# by exclusive create. Run: python3 -I -B build_root_items_step45_v002.py <staging_dir> <utc_stamp>
import hashlib, json, os, re, sys

STAGING = sys.argv[1]
STAMP = sys.argv[2]

X = "/Users/bgm/Research/UNT_EXCHANGE"
CA = X + "/claude_artifacts"
UC = "/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL"
ROOTDEC = UC + "/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2"

# key: (path, sha256 as read from bytes this session, volatile?, short name, note)
SOURCES = {
 "d0637": (X + "/FROM_CODEX/0637_2026-10-18_claude4_draft_step45_root_items.md", "e6163c64eaf2193e7730a1819ae0e1cea87420c8a4fa9ddb2678583e460ade01", False, "dispatch 0637", "authority for this task"),
 "cur_instr": (UC + "/CURRENT_INSTRUCTIONS.md", "59ada35ce59146c758374c88abeb3ed183f09217501d1f3c7a43463adacc6917", True, "CURRENT_INSTRUCTIONS.md", "program instructions"),
 "cx1_0074": (X + "/FROM_CODEX1/0074_2026-10-18_step4_step5_handoff_build_finished.md", "4a0236d1b4263bada8c9956b0e137df974515bdbbc7c84ec7d962c247b27a0e4", False, "Codex1 0074", ""),
 "cx1_0104": (X + "/FROM_CODEX1/0104_2026-10-18_handoff_successor_three_findings_addressed.md", "8fc9f57f33c96b38bf2281f83b4c3afb0caf85042cdbfdabebc428517064b5aa", False, "Codex1 0104", ""),
 "cx1_ri_v002": (CA + "/step4_step5_handoff_cx1/ROOT_ITEMS_CX1V002.json", "47c6f836adcb2334d0f6ec5b34a8791746852f9309c6ec2d7d61b9a2f9be180c", False, "ROOT_ITEMS_CX1V002.json", "the 8 handoff root items cited by 0074"),
 "cx1_ri_v003": (CA + "/step4_step5_handoff_cx1/ROOT_ITEMS_CX1V003.json", "98a45bbbaa7808f9636838dd9f8a1f7dea89a63176b5920e421f6e3c5467e503", False, "ROOT_ITEMS_CX1V003.json", "successor text cited by 0104"),
 "cx1_contract": (CA + "/step4_step5_handoff_cx1/HANDOFF_CONTRACT_CX1V002.md", "8eb0745989711999d7f63a3131908dff00ba144a59e1cdda95afa58abfa6cabc", False, "HANDOFF_CONTRACT_CX1V002.md", ""),
 "cx1_rules": (CA + "/step4_step5_handoff_cx1/rules/RULES_AUDIT_CX1V001.md", "7406996a81d32f60ae0c7959352d514b5315cc10ec74388afebb1dfa9b525646", False, "RULES_AUDIT_CX1V001.md", ""),
 "cx1_build1": (CA + "/step4_step5_handoff_cx1/BUILD_CX1V001.md", "c305a3b09a305c67d310631e4145213c4ee0dee563de714e0dab4d7e6dae0937", False, "BUILD_CX1V001.md", ""),
 "cx1_build2": (CA + "/step4_step5_handoff_cx1/BUILD_CX1V002.md", "bfdb19adeae95b2546f67fa2f593a4b4dfa258c2a6b317d4d4134675d4ca9761", False, "BUILD_CX1V002.md", "writer v010"),
 "cx1_semantic": (CA + "/step4_step5_handoff_cx1/semantic_delta_cx1v001/SEMANTIC_DELTA_CX1V001.md", "ba85f470a3e90fedd614bf16ed0bb0c5feb12a809d45d77505a1d3b6553ec905", False, "SEMANTIC_DELTA_CX1V001.md", ""),
 "cx3_0614": (X + "/FROM_CODEX3/0614_2026-10-18_dispatch0594_step5_readiness_finished.md", "9b6e50b561efa94f6f0c8ba7fab0df8906d0fc4d2f5608657170e0384ba424b8", False, "Codex3 0614", ""),
 "cx3_0618": (X + "/FROM_CODEX3/0618_2026-10-18_dispatch0606_carriers_finished.md", "8939c004e4bea1728eed610e4d98b98dffbe4333be1433c539feb16159de60a7", False, "Codex3 0618", ""),
 "cx3_ri_v002": (CA + "/step5_ngc_route_ab_readiness_cx3/ROOT_ITEMS_CX3V002.json", "3e9e31d41d673ebab357b82c365c551578302e9b95ddb705211b3cb1e5685471", False, "ROOT_ITEMS_CX3V002.json", "R1-R12"),
 "cx3_report": (CA + "/step5_ngc_route_ab_readiness_cx3/READINESS_REPORT_CX3V001.md", "c7c72d54293a133df4211805534849d2fe42fadf2ed5286ff7f3f0426e4c2782", False, "READINESS_REPORT_CX3V001.md", ""),
 "cx3_contract": (CA + "/step5_ngc_route_ab_readiness_cx3/HANDOFF_CONTRACT_CX3V002.md", "6ae6a0fc406df004e1aaeb425dd4ee3966c797b63f6d775bfb92d9a340b6dc7a", False, "HANDOFF_CONTRACT_CX3V002.md", "the consumer contract"),
 "cx3_policy": (CA + "/step5_ngc_route_ab_readiness_cx3/POLICY_CX3V001.json", "4f0d7d039fcee03fc9e2e1c74624919c77b14e19b101389124864219057e5bbf", False, "POLICY_CX3V001.json", "hashed"),
 "cx3_registry": (CA + "/step5_ngc_route_ab_readiness_cx3/STEP5_REGISTRY_CX3V002.json", "85b1e66aa56d38e455c86d20e9bf5a854e7e3d4a65d3e27adc5eb223b89cf59c", False, "STEP5_REGISTRY_CX3V002.json", "hashed"),
 "cx3_freeze_inputs": (CA + "/step5_ngc_route_ab_readiness_cx3/FREEZE_EXPECTED_INPUTS_CX3V002.json", "169df91f67ea73c7a0291b3fbc852c70777107753685191b95f97dacc9672253", False, "FREEZE_EXPECTED_INPUTS_CX3V002.json", ""),
 "cx3_order": (CA + "/step5_ngc_route_ab_readiness_cx3/LAUNCH_ORDER_CX3V002.md", "829a8cb66e2bffdfd215c1113028754a13a70ebf414d5b38a200b5914b8516c3", False, "LAUNCH_ORDER_CX3V002.md", ""),
 "cx3_carr_report": (CA + "/step5_ngc_route_ab_readiness_cx3/carriers_0606_v001/REPORT_CX3V001.md", "50f4278ec061583c2cf1ad6b558f8fb0b3759460c05bc5420af7739b6cdb53d2", False, "carriers REPORT_CX3V001.md", ""),
 "cx3_carr_decision": (CA + "/step5_ngc_route_ab_readiness_cx3/carriers_0606_v001/DECISION_CX3V001.json", "8762a1b57074a7ab7553bcb1805fd7fdd6d777925846bf96d79edca079f75f33", False, "carriers DECISION_CX3V001.json", ""),
 "cx3_carr_delta": (CA + "/step5_ngc_route_ab_readiness_cx3/carriers_0606_v001/READINESS_DELTA_CX3V001.json", "89aaa8f618f06732917b689782a51a9415130881a42124aceddc1e68fb9000e9", False, "carriers READINESS_DELTA_CX3V001.json", ""),
 "cx3_carr_contract": (CA + "/step5_ngc_route_ab_readiness_cx3/carriers_0606_v001/CARRIER_CONTRACT_CX3V001.json", "252ef9e1c2c139abbf6fd97d174444ea33cb7b615f96d592a1b09248928b0423", False, "CARRIER_CONTRACT_CX3V001.json", "hashed in V001; its A17_C3 role read at the fix stage"),
 "c3_0088": (X + "/FROM_CLAUDE3/0088_2026-10-18_step5-readiness-review-PASS_WITH_FINDINGS.md", "41907633ea0576adfac1f0eff3d9f5beb0d154c8d4d535d7a502d4c7a47b9f9c", False, "Claude3 0088", ""),
 "c3_review5": (CA + "/review_step5_readiness_c3/REVIEW_STEP5_READINESS_C3V001.md", "f32ead4a3e702a65b3f82fab69f1387db8afd4668263e2220d0cb829f16dcd36", False, "REVIEW_STEP5_READINESS_C3V001.md", "8 SHOULD_FIX, 15 missing ROOT_ITEMS"),
 "c3_s2": (CA + "/review_step5_readiness_c3/S2_carriers_evidence/FINDINGS_S2.md", "9fa773de6bf58abf6edf5feb8570ead722e227134f1d4492f37924a51289c4c2", False, "FINDINGS_S2.md", "Claude3 S2 lens"),
 "c3_s1": (CA + "/review_step5_readiness_c3/S1_filler/FINDINGS_S1.md", "a77e262858fe358a39580a2d9bf46e4024d65c56b9fd74e8be6435eadec4f82c", False, "FINDINGS_S1.md", "hashed only; cited through the review"),
 "c3_0094": (X + "/FROM_CLAUDE3/0094_2026-10-18_step4-handoff-review-PASS_WITH_FINDINGS-0-blocking.md", "e45fb60252d7fd9003d29a39db67c6f4ac2f6d005c7514f89c3048d4527beeb8", False, "Claude3 0094", ""),
 "c3_review4": (CA + "/review_step4_handoff_c3/REVIEW_STEP4_HANDOFF_C3V001.md", "77847250114c06755c551e89e57588b2d45c0abd778c2dfabcd04f6b0d289466", False, "REVIEW_STEP4_HANDOFF_C3V001.md", "6 SHOULD_FIX"),
 "c4_0104": (X + "/FROM_CLAUDE4/0104_2026-10-18_cx3r008_delta_PASS_WITH_FINDINGS.md", "57a8267851ab3fd7996d547617dafcadc19dd4cb04a0622170003cd21c86bea4", False, "Claude4 0104", ""),
 "c4_r8review": (CA + "/review_ngc_v011_cx3r008_c4/REVIEW_NGC_V011_CX3R008_C4V001.md", "7ff20c1ded13513e5c0f5a386be8aa17825625a7b5a83cd2513b0693e0ab5c42", False, "REVIEW_NGC_V011_CX3R008_C4V001.md", "cx3r008 delta of record"),
 "c4_index": (CA + "/step4_launch_readiness_c4/INDEX_STEP4_READINESS_C4V002.md", "e58603a1457e97da74ddf0b500e143db5e8cfe198a38aa28e4c657381890fc9d", False, "INDEX_STEP4_READINESS_C4V002.md", ""),
 "c4_ri_v004": (CA + "/step4_launch_readiness_c4/launch_order/ROOT_ITEMS_FINAL_C4V004.md", "97a762e1cf2c7eb76e7f77b4c708cfc5452dd5b72452b2bf86ffc9e369e6b704", False, "ROOT_ITEMS_FINAL_C4V004.md", "37 step-4 items"),
 "cx1_0080": (X + "/FROM_CODEX1/0080_2026-10-18_miss_reading_r3_preparation_two_shouldfix_pending.md", "f423415cd07a871241ed2842dcd4c21da5fcb2f5f9a0ac40dce136372f3a8a0a", False, "Codex1 0080", ""),
 "cx1_0082": (X + "/FROM_CODEX1/0082_2026-10-18_miss_reading_r3_function_slice_review_finished.md", "156aeb7c4cbb6da2ef2ea306c8e18054ba8a09dea147f63b7042fd3052882c31", False, "Codex1 0082", ""),
 "cx1_prov1": (CA + "/review_miss_reading_r3_cx1/PROVISIONAL_REVIEW_CX1V001.md", "6a99fdb90ddf25a15711092d88cea4a9704ed56bdf5bbe307f1e4e4997d985cd", False, "PROVISIONAL_REVIEW_CX1V001.md", ""),
 "cx1_prov2": (CA + "/review_miss_reading_r3_cx1/PROVISIONAL_REVIEW_CX1V002.md", "2196ec7c22a1b1ba71a32962ecec3f8b7d48877d79117af3fd6eac6d7182f110", False, "PROVISIONAL_REVIEW_CX1V002.md", ""),
 "r3_root_items": (CA + "/miss_reading_prereg_c4/r3_work/text_c4/ROOT_ITEMS_R3.md", "b33270fe9e07bbe3990cdeca6859daf08dd7d1e9836936befd2086d023edc4fb", True, "r3 draft ROOT_ITEMS_R3.md", "work draft, read 00:58:27Z; pending the final r3"),
 "r3_text": (CA + "/miss_reading_prereg_c4/r3_work/text_c4/PREREG_MISS_READING_R3.md", "fb40156a32d50809ad1b9d3e8e663468726c831f468b5192b05f01bbf3ed14c7", True, "r3 draft PREREG_MISS_READING_R3.md", "work draft, read 00:58:27Z; pending the final r3"),
 "r3_fixlog": (CA + "/miss_reading_prereg_c4/r3_work/fixlog_c4/PARTIAL.md", "a89b3e7f15e2c14d8b2f31dd469fc19e0065fd390903a481965f4a54cee2f320", True, "r3 fixlog PARTIAL.md", "work log, read 00:58:27Z (4da9a3eb), 01:33:32Z (e15ff4c7) and at the fix (a89b3e7f: 'Stage done', 01:42:42Z)"),
 "r3_dry": (CA + "/miss_reading_prereg_c4/r3_work/fixlog_c4/dry_after_fix/PREREG_MISS_READING_R3.md", "bdcf6aff2ff5020b141f9050cc6431e78c5cd26b0c54e157227dcd66986d12c2", True, "r3 fix-stage dry build PREREG", "rendered 01:27Z; grep of the C-9 row only"),
 "r3_confirm": (CA + "/miss_reading_prereg_c4/r3_work/fixlog_c4/CONFIRM_FINDINGS_FIX_1.json", "980558d12eb0c1f9430b73675670881708386b366598847543a6796ae4ca96f7", True, "r3 CONFIRM_FINDINGS_FIX_1.json", "work record"),
 "v005": (ROOTDEC + "/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md", "c01b3c51e34501d77e474594cc0b4be72c6e068c7f58a595055316313a8d4bb1", False, "V005 addendum (closed)", "rulings A47-A106; read in full"),
 "v006": (ROOTDEC + "/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V006_ADDENDUM.md", "b22bd18ae4c3142be54db0e965b2a2fff4264e787fa29963bd637b6ae2ddc6a4", True, "V006 addendum (open)", "A107-A112; read 00:55Z (7af42209), 01:33Z (43d4562b) and at the fix stage (b22bd18a: A112 inserted at 02:42Z); the three byte copies are in this folder"),
 "v006_copy": (CA + "/root_items_step45_c4/V006_ADDENDUM_COPY_AT_READ.md", "7af422093efd24d06ac6080c67f0114813071512cceab2c19d001d6eb04ba77c", False, "V006_ADDENDUM_COPY_AT_READ.md", "exclusive byte copy, 00:55:04Z (A107-A109)"),
 "v006_copy2": (CA + "/root_items_step45_c4/V006_ADDENDUM_COPY_AT_READ_2.md", "43d4562b4fce53cf7bc0ea101af2792b8669689cbbddf882882e1ac4a14cbb0c", False, "V006_ADDENDUM_COPY_AT_READ_2.md", "exclusive byte copy, 01:33:20Z (A107-A111)"),
 "v006_copy3": (CA + "/root_items_step45_c4/V006_ADDENDUM_COPY_AT_FIX.md", "b22bd18ae4c3142be54db0e965b2a2fff4264e787fa29963bd637b6ae2ddc6a4", False, "V006_ADDENDUM_COPY_AT_FIX.md", "exclusive byte copy, 02:44:13Z (A107-A112); diff against copy 2: one inserted section, A112"),
 "d0631": (X + "/FROM_CODEX/0631_2026-10-18_codex1_step4_to_step5_handoff_pipelining.md", "044628c989e72528e34525128003a3f8e6abe16de8a11550aa3dd51f9575e8be", False, "dispatch 0631", ""),
 "d0635": (X + "/FROM_CODEX/0635_2026-10-18_reassign_codex2_queue.md", "c6fd229feeef4c399198118d5c1465a1af9a5bff029f44865e1813b5eeec9758", False, "dispatch 0635", ""),
 "d0636": (X + "/FROM_CODEX/0636_2026-10-18_codex3_conserve_codex1_takes_prestage.md", "6b29ccf2ef10e7643975c79b232a98bd080968044acfedde7a18606aa0265621", False, "dispatch 0636", "fix rounds by a Claude lane or Codex1"),
 "d0638": (X + "/FROM_CODEX/0638_2026-10-18_codex1_takes_v003_codex3_reserve.md", "cc02bdbc54d5a33da07c3629772564d2538083412a790ddc9f841d37e9e54fcb", False, "dispatch 0638", "Codex3 in reserve"),
 "d0645": (X + "/FROM_CODEX/0645_2026-10-19_all_lanes_stall_reassignment_A109.md", "65df85f92b37fae6a5fbf5518fa6583ee00f0d8eef015902db14cc7637de0376", False, "dispatch 0645", ""),
 "d0617": (X + "/FROM_CODEX/0617_2026-10-18_all_lanes_multi_agent_concurrent_workstreams.md", "622f5cc99633a2433ce4fb7feebabb6580a468c6660f48377c7c8e48f6bd102d", False, "dispatch 0617", ""),
 "d0619": (X + "/FROM_CODEX/0619_2026-10-18_claude4_codex3_A98.md", "238858d12823a153b14dd980d2e2c0a4a71da5c320be054c1fe14832d667ee99", False, "dispatch 0619", "A98"),
 "d0620": (X + "/FROM_CODEX/0620_2026-10-18_claude4_codex1_step4_no_unguarded_fallback.md", "037a2a61998d511e398f10f7e8c9203597a48e768bbf09d148ae209d94658e99", False, "dispatch 0620", "step-4 launch path"),
 "d0616": (X + "/FROM_CODEX/0616_2026-10-18_codex1_step4_launch_packet.md", "634bca4ed8369143fba671ea0b922715ec7fb85354e28a0595b5c4c4cae454cc", False, "dispatch 0616", "hashed only; cited through the step-4 record"),
 "c3_0099": (X + "/FROM_CLAUDE3/0099_2026-10-19_ack-0115-step4-V002-and-producer-review-started.md", "05978918d7ebd93b37f6b3176733f6a2e1464f904a4a3fc5b858b2c0c46c1429", False, "Claude3 0099", ""),
 "c3_0101": (X + "/FROM_CLAUDE3/0101_2026-10-19_progress-step4-V002-review-running-v003-still-pending.md", "96f74de32aacd5a2baade269771fd2f52626a3d61b09ae82bb200a7457ff6c00", False, "Claude3 0101", ""),
 "cx1_0110": (X + "/FROM_CODEX1/0110_2026-10-18_ack_step4_spec_handoff_waiting_v003.md", "d0f7631fdb24f83be0af4bfeb8c683324536358d4ab3b141aa3d085af28e6df8", False, "Codex1 0110", ""),
 "c4_0107": (X + "/FROM_CLAUDE4/0107_2026-10-18_ack_0640_PV-D05-1_and_0637.md", "86858d336242f7bd9e7cc302399116f2831a06ad613ccb037e87850625f29d94", False, "Claude4 0107", ""),
 "c4_0114": (X + "/FROM_CLAUDE4/0114_2026-10-19_prereg_r6_SELECTED_7200acd9.md", "66767e269c175802e033dbc330b17c24d394eba4b2aad28902e3adeb71a18e3c", False, "Claude4 0114", ""),
 "c4_0115": (X + "/FROM_CLAUDE4/0115_2026-10-19_done_0587_step4_readiness_V002.md", "40a4ea6051e6b85d407eac7965f1363687199608c9794620472e383b6e94a1b7", False, "Claude4 0115", "hashed"),
 "c4_0118": (X + "/FROM_CLAUDE4/0118_2026-10-19_progress_seal_inputs_done_0637_r3_in_progress.md", "d400acb82ab79eae1c6a5155b861a9ff4fda6747cca2fedee0f80249a77bcfa8", False, "Claude4 0118", ""),
 "r6_selected": (CA + "/v007_final_prereg_c4/r6/SELECTED_R6_C4V001.json", "7200acd996755730573ad72d876ff632b8ef59bf86f2b0cf176ae3fceb4403b0", False, "SELECTED_R6_C4V001.json", "case_block entry read"),
 "r6_text": (CA + "/v007_final_prereg_c4/r6/KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R6.json", "d28c95f56321f566b444c3e0bfbbe0ecdac564cbc03a8583ecd5f8d0ae40c0a9", False, "KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R6.json", "binding_inputs.case_block read"),
 # ---- added in the FIX stage (V002); every sha read from bytes in this stage
 "refute": (CA + "/root_items_step45_c4_check/REFUTE_ROOT_ITEMS_STEP45.md", "0a75e6d86ecb57fd1a04dfafbd47ed17273ac4d015231032729bcb1499d9468d", False, "REFUTE_ROOT_ITEMS_STEP45.md", "the refuter stage of V001 (8 SHOULD_FIX, 13 NOTE)"),
 "v001_md": (CA + "/root_items_step45_c4/ROOT_ITEMS_STEP45_V001.md", "33d09696d105062f8a8dc0cd15256b412d2db6eeadd7d8e693a0489bbee07e46", False, "ROOT_ITEMS_STEP45_V001.md", "the version this one corrects; unchanged"),
 "v001_json": (CA + "/root_items_step45_c4/ROOT_ITEMS_STEP45_V001.json", "8a20c3342e2e3abe7a3560b07e4cfda5957aebbe044885e585373a3a5dc46fb2", False, "ROOT_ITEMS_STEP45_V001.json", "the version this one corrects; unchanged"),
 "c4_order_v002": (CA + "/step4_launch_readiness_c4/launch_order/LAUNCH_ORDER_C4V002.md", "520270983a325b0efc7618713d3761cee9b145308e3cc227e5c17e1823363627", False, "LAUNCH_ORDER_C4V002.md", "step-4 launch order of record; sections 4-6 read"),
 "c4_spec_handoff": (CA + "/step4_launch_readiness_c4/handoff/SPEC_HANDOFF_C4V002.md", "9f72489e0a67cb0931ca7b78939b53bef71f35cb3938c15e4f9e516c034055dd", False, "SPEC_HANDOFF_C4V002.md", "DIII lines read (section 3; L86, L203)"),
 "c3_0105": (X + "/FROM_CLAUDE3/0105_2026-10-19_step4-V002-and-producer-review-PASS_WITH_FINDINGS-0-blocking.md", "c0378a3228f8e6a7a5fcd173108d8b9a412572502c5ee5688a3ee60aab86e953", False, "Claude3 0105", "producer 8e835ce3 and package V002 review, born 01:19:16Z"),
 "c3_review_s4v2": (CA + "/review_step4_readiness_v002_c3/REVIEW_STEP4_READINESS_V002_C3V001.md", "1789c6b4d4a86e5b7bfe15b88653ab19b64abea3a4c8b9c577fe8c75984597c4", False, "REVIEW_STEP4_READINESS_V002_C3V001.md", "0 BLOCKING, 7 SHOULD_FIX"),
 "c3_pkg_partial": (CA + "/review_step4_readiness_v002_c3/PACKAGE/PARTIAL_FINDINGS_PACKAGE_V001.md", "f600c287c561b3ffe93cb6e5bea6eca5ac12c5dcf82c70af324c6adb058717bf", False, "PARTIAL_FINDINGS_PACKAGE_V001.md", "PKG-S1..S4 detail"),
 "c4_0119": (X + "/FROM_CLAUDE4/0119_2026-10-19_ack_claude3_0105_step4_fixes_started.md", "4ee6044ba9088612a968c87fa6117f3d20fc40e941f181f52bbf8782e1dacf69", False, "Claude4 0119", "producer v003 and package V003 started, 01:20:04Z"),
 "c4_0123": (X + "/FROM_CLAUDE4/0123_2026-10-19_progress_four_builds_running.md", "fd5fd8b69a42d17772e877c3795a81b6ddff611b32332bc1111a39da1dfcfd37", False, "Claude4 0123", "progress, 01:34:19Z"),
 "c4_v003_partial": (CA + "/step4_launch_readiness_c4/v003_work/PARTIAL.md", "831b9487579762dd6e2d02a939f845210d0472371b13fdd37ddcbeb10c15f7f7", True, "step-4 V003 build PARTIAL.md", "work log of the V003 build (03d68d2a at 02:09Z, c757b1cc at 02:24Z, 831b9487 at 02:50Z: 'BUILD stage complete')"),
 "c4_v005_builder": (CA + "/step4_launch_readiness_c4/v003_work/tools/build_root_items_final_c4v005.py", "8ee594df1fd9041d0a640e4381424262e95921bdb8c5315b1b63cd4aac0534d3", True, "build_root_items_final_c4v005.py", "the V005 builder; header read (R-B7, R-D18)"),
 "c4_v005_md": (CA + "/step4_launch_readiness_c4/v003_work/order/ROOT_ITEMS_FINAL_C4V005.md", "753e7e257985495acacd3f729f5aa1676875c4a7de1090f06f28324f768b199a", True, "ROOT_ITEMS_FINAL_C4V005.md (candidate)", "build-stage candidate, written 02:25:14Z; not reviewed or published; R-A1, R-B7, R-D17, R-D18 and the DIII step read"),
 "c4_producer_v003": (CA + "/step4_launch_readiness_c4/v003_work/tools/produce_final_step4_specs_c4v003.py", "28921808ae4dca50e4d572ca8febd8364e92346d9764cf2b911a938542b88f85", True, "produce_final_step4_specs_c4v003.py", "producer v003, hashed only (in build; delta check pending)"),
 "d0648": (X + "/FROM_CODEX/0648_2026-10-19_A112_v004_selected_disclosures_V002.md", "101f671fcd8e31ffd0702242f2bcd31c9f398005b5a9a9e1a2742abaf9bab216", False, "dispatch 0648", "seal-path wiring (A112); assigns no step-4 builder"),
 "cx1_iface3": (CA + "/step4_launch_packet_cx1/impl/IMPLEMENTATION_INTERFACE_CX1V003.md", "dc73cd94fa8cc539308c50b3fc1163b996e163d9699ef59cbf4dfb51039b382b", False, "IMPLEMENTATION_INTERFACE_CX1V003.md", "0616 packet interface; 'Plan and PRELAUNCH', DIII policy, max_active"),
 "cx1_guard7": (CA + "/step4_launch_packet_cx1/impl/step4_guard_cx1v007.py", "42bf0ce9dcd48f734299ace4f07cb92a15563e57a39f5ae40be451e481d1c3de", False, "step4_guard_cx1v007.py", "guard007; native_preflight L187-222, validate L224-275 read"),
 "cx1_launcher8": (CA + "/step4_launch_packet_cx1/impl/step4_launcher_cx1v008.py", "bf2d535fe8eb1a83a7e3c92751a5baeaf19bb7d3abef72bb3db964b8e36ba041", False, "step4_launcher_cx1v008.py", "grep only (no PRELAUNCH writer)"),
 "cx1_bind6": (CA + "/step4_launch_packet_cx1/impl/step4_bind_cx1v006.py", "3db8c72a36a1574ba0908da323effe49ded106aecc1c67f8a76152b6b54ad9cb", False, "step4_bind_cx1v006.py", "grep only (no PRELAUNCH writer)"),
 "cx1_runbook3": (CA + "/step4_launch_packet_cx1/RUNBOOK_CX1V003.md", "2eda3ebf6232480a9ac25341fa850c99e5dcb75cdf68b79ca785d3fbcf7330fb", False, "RUNBOOK_CX1V003.md", "steps 3-4 read"),
 "cx3_resource_plan": (CA + "/ngc_route_tail_readiness_cx3/ADMITTED_POINT_RESOURCE_PLAN_V001.json", "4de87df93a56a5d996e6ce0e5652e81e2142e1b8e154c9cb58a5c2b98832ef77", False, "ADMITTED_POINT_RESOURCE_PLAN_V001.json", "the only NGC resource plan (K15 era); read in full"),
 "cx3_ri_v001": (CA + "/step5_ngc_route_ab_readiness_cx3/ROOT_ITEMS_CX3V001.json", "446f340622bcc57b362fcb9109da6fcd3669cd60c17861b34f3c94da6f0e1167", False, "ROOT_ITEMS_CX3V001.json", "superseded by V002; compared record by record"),
 "r3f_prereg": (CA + "/miss_reading_prereg_c4/r3/PREREG_MISS_READING_R3.md", "b0fba984543c5c93fc4d25497c6e9e97f33662d3a98a63856b4933e4b1f47dd0", False, "r3 final PREREG_MISS_READING_R3.md", "the final r3 text (unsealed; named by SEAL CANDIDATE 0124); lines 242 and 598 read"),
 "r3f_root_items": (CA + "/miss_reading_prereg_c4/r3/ROOT_ITEMS_R3.md", "b33270fe9e07bbe3990cdeca6859daf08dd7d1e9836936befd2086d023edc4fb", False, "r3 final ROOT_ITEMS_R3.md", "byte-equal to the draft V001 read; M-3, M-13, M-14 re-read"),
 "r3f_index": (CA + "/miss_reading_prereg_c4/r3/INDEX_R3.md", "87b77c7ec1b66d741e02a6bde7cfa6b8f886f1ca729564df159eedfb39091c3f", False, "r3 final INDEX_R3.md", ""),
 "r3f_hashes": (CA + "/miss_reading_prereg_c4/r3/HASHES_R3.txt", "4c0e4cd1b8ab922b66fe31b9687441dadb7ab0498953362b28172da2d5152d57", False, "r3 final HASHES_R3.txt", ""),
 "r3f_checks": (CA + "/miss_reading_prereg_c4/r3/checks/INDEX_CHECKS_R3.md", "5d17ae7a874b652a844b7c6e112aff6ee4aa03c222ea4f1d4dc3880f6b71a19f", False, "r3 final checks/INDEX_CHECKS_R3.md", "pattern suite and closure table, added 02:07:41Z"),
 "c4_0124": (X + "/FROM_CLAUDE4/0124_2026-10-19_SEAL_CANDIDATE_miss_reading_prereg_r3.md", "73f5faab369abcd20dc7901811b0eae9d0cb8a9135c0df61b66f185d7b9c71b2", False, "Claude4 0124", "the first SEAL CANDIDATE post, 02:16:45Z"),
 "c4_0125": (X + "/FROM_CLAUDE4/0125_2026-10-19_miss_reading_r3_built_for_codex1_delta.md", "a58d1804234004676bfee1741ae36d758150f7a2a9b599d122bd913a7d8387f4", False, "Claude4 0125", "r3 built; CX1-MR3-P1 fix proposed, 02:19:34Z"),
 "cx1_0119": (X + "/FROM_CODEX1/0119_2026-10-18_miss_reading_r3_A98_delta_PASS_0.md", "ae2374c47fd4f71ca4e59321238daf3ec68d415e2a4719451e33a3aef468db3a", False, "Codex1 0119", "r3 A98.2 delta PASS, 0 blocking, 02:18:51Z"),
 "cx1_0120": (X + "/FROM_CODEX1/0120_2026-10-18_ack_0125_carry_MR3_P1_shouldfix.md", "27d2bd750f0161446c7474bbcaeab59edff9a937d85600a67ce0e470a2a0dfcf", False, "Codex1 0120", "CX1-MR3-P1 OPEN, CX1-MR3-P2 CLOSED, 02:20:47Z"),
 "cx1_r3delta": (CA + "/review_final_deltas_cx1/MISS_READING_R3_A98_DELTA_V001.json", "ee375b8dc6ddf17e9831b4b875112dcda87ebb2a239f9b77e6532e95955345b4", False, "MISS_READING_R3_A98_DELTA_V001.json", "Codex1's delta record; verdict PASS, blocking_count 0"),
}

def sha_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()

REHASH = {}
problems = []
for k, (p, s, vol, name, note) in SOURCES.items():
    if not re.fullmatch(r"[0-9a-f]{64}", s):
        problems.append("BAD_SHA_FORMAT " + k)
        continue
    cur = sha_file(p)
    REHASH[k] = cur
    if cur != s and not vol:
        problems.append("SHA_MISMATCH %s read %s now %s" % (k, s, cur))
if problems:
    print("REFUSED:", problems)
    sys.exit(2)

BLOCKS = ("BLOCKS_START", "BEFORE_FIRST_RESULT", "LATER", "DECIDED")

# ---------------------------------------------------------------- items
ITEMS = []
def item(**kw):
    ITEMS.append(kw)

# ===== Group 1: Codex1 0074 / 0104, the step-4 -> step-5 handoff (H1-H8) =====
G1 = "G1"
item(group=G1, key="exporter", step="4-5 handoff", blocks="BLOCKS_START", blocks_step="5", phase=6,
 title="The authentic native exporter and its verifier (the step-4 producer of every handoff)",
 blocks_note="Needed before the first real handoff, after step 4's FULL_FINAL_DECISION. It does not affect step 4's own start.",
 raised_by=["Codex1 H1_SCIENTIFIC_PRODUCER (ROOT_ITEMS_CX1V002; restated in V003)", "Codex1 H3 (its complete-roster custody part, V003)", "Codex1 H5 (the guarded plan/admission hashes)", "Codex1 0074 production blockers (1) and (3)", "Codex1 SEMANTIC_DELTA findings 2-4 (OPEN)", "Codex3 R1", "Claude3 0094 SF4; ADM-N7 (NOTE)"],
 issue="FORMAL: the guarded step-4 path has no authentic, target-free producer of admitted points (HANDOFF_CONTRACT_CX1V002, 'Proposed producer'; RULES_AUDIT_CX1V001 section 4: no per-point record callback; points are published only at finalise, after two deterministic replays). The native record (CALIBRATION_RUN_RECORD_C2V003) keeps them at run.exploration.admitted_points. The native verify_calibration_record (engine L3017-3108) checks canonical bytes, self-hash, fingerprint and registry chain, but does not reclassify predictions; the freeze module's _check_calibration_record (L2919-2980) re-derives the rectangles and reclassifies members (RULES_AUDIT, 'Native layout and verifier'). FORMAL (HANDOFF_CONTRACT_CX1V002 L15): the producer 'must independently retain and verify native record/registry custody, actual rectangle membership, complete deterministic replay, guarded plan/admission provenance, post-state acceptance and point-scoped certificate validity'. H5 (CX1V002 and V003) asks for 'guarded plan/admission hashes'; Codex1 0074 blocker (3) and BUILD_CX1V001 ('UNTESTED / open') name post-state acceptance. TESTED by Claude3 (0094 SF4): writer v008 checks only labels, the selected point's membership and claimed hashes, so a view that holds 1 point of a 3-point roster and is labelled final passes write_point; ADM-N7: the export lists one point under admitted_points.",
 options=["(a) A new reviewed exporter. It reads the native record and registry read-only; runs verify_calibration_record and the freeze module's reclassification unchanged; requires engine_status COMPLETE and engine_ok true (a registered BUDGET_EXHAUSTED record is not COMPLETE) and both deterministic replay results; verifies the guarded plan and admission provenance (the hashes of the root-published admission records and guarded plans under which each admitted point's call ran: H5), each admitted point's post-state acceptance (its per-call CERTIFICATE_ACCEPTANCE records: step-4 R-B5) and its point-scoped certificate validity (the certificates bound to that point, not another's: step-4 R-C1 and R-C8); rebuilds the complete admitted roster and compares it entry by entry (log_index, u, theta_natural) with the emitted final-decision view; then emits only those three fields, for every admitted point.",
          "(b) Root extracts the points by hand, with a checklist.",
          "(c) Freeze v003g becomes the producer, extended to emit the export."],
 recommendation="(a), covering all six obligations of the contract's producer boundary. Its tests include, all as MUST_FAIL: Codex1's named controls (a truncated roster, a relabelled final view, scope and replay mismatches, a forged or swapped record, a BUDGET_EXHAUSTED record); Claude3's 1-of-3 case; an admitted point whose post-state acceptance is missing or refused; and a guarded plan or admission hash that does not match the published one. It runs under the shared fence ({ref:fence}) and writes by exclusive create.",
 reasoning="The consumer contract copies entries from the actual native admitted_points under root custody (HANDOFF_CONTRACT_CX3V002). Labels, self-hashes, FINISHED monitors and PRELAUNCH permits do not show admission (RULES_AUDIT sections 1, 3 and 4; Claude3 0094: 219/219 admission cases as predicted). A point whose post-state certificates were refused, or whose call ran under another plan or admission, is not an admitted point of this calibration, so the exporter must check both and not only the roster. (b) puts custody on a manual step exactly where target-free provenance matters. (c) gives reviewed step-6 code (Claude4 0071 PASS) a new role and a new review. Calling the two native functions unchanged confines the new review to the comparison, the provenance checks and the emitter.",
 owner="Builder Codex1 (author of the writer, the producer contract V003 and the rules audit); distinct reviewer Claude3 (step-4 and handoff reviewer, A103 and 0635); Claude2 publishes its release-authority digest ({ref:authority}).",
 decided=None,
 sources=[("cx1_ri_v002", "H1_SCIENTIFIC_PRODUCER; H5_V007_NATIVE_CUSTODY"), ("cx1_ri_v003", "H1; H3; H5"), ("cx1_rules", "sections 1-4; 'Native layout and verifier'"), ("cx1_contract", "'Proposed producer and authority boundary' (L15)"), ("cx1_0074", "'UNTESTED / production blockers', items (1) and (3)"), ("cx1_build1", "'UNTESTED / open' (L13)"), ("cx1_semantic", "findings 2-4"), ("c3_review4", "SHOULD_FIX 4; NOTES, ADM-N7"), ("c4_ri_v004", "R-B5; R-C1; R-C8"), ("cx3_ri_v002", "R1"), ("cx3_contract", "source_export_pin paragraph")])

item(group=G1, key="coords", step="4-5 handoff", blocks="BLOCKS_START", blocks_step="5", phase=6,
 title="Step 4's three-parameter point against step 5's four-parameter filler",
 blocks_note="The selected filler refuses a genuine native point today.",
 raised_by=["Codex1 H2_NATIVE_COORDINATES (OPEN_BLOCKS_CURRENT_NATIVE_HANDOFF)", "Claude3 0094 CX-SF3 (NOTE)"],
 issue="TESTED by Codex1 (RULES_AUDIT, 'Independent interface blocker'; 9/9 synthetic controls): the step-4 config pins coordinate mode DDO154_DISTANCE_FIXED_AT_REGISTERED, so the headline varies three coordinates (common_scale_s, gamma_over_Eref, ell_F_m) and holds distance_Mpc at 4.04. The locked filler (fill_step5_cx3v003 2348974f, L90-120) uses the policy's engine_coordinates, in which distance_Mpc also varies (four entries), and refuses a three-entry u at VARYING_U_LENGTH. Padding a fourth entry would break the consumer's copied-native-u rule. FORMAL (Claude3 0094 CX-SF3): the shared coordinate file does not distinguish the two modes.",
 options=["(a) A reviewed filler and policy successor that accepts the native three-u fixed-distance mode. It binds the mode name and the exact coordinate-addendum and config identity, not only the shared coordinate file; keeps theta_natural as the mapping input; and validates distance_Mpc = 4.04 as fixed.",
          "(b) A reviewed explicit bridge that maps the three-u vector to four entries and records the mapping.",
          "(c) Run step 4 in the four-u, distance-varying mode."],
 recommendation="(a). MUST_FAIL controls: a four-u point under the three-u mode; a mode or addendum mismatch; distance_Mpc other than 4.04; a three-u point with an invented fourth entry.",
 reasoning="(a) keeps the native record's own coordinates. The filler already maps the physics from theta (gamma = gamma_over_Eref x Eref_base_J; the DDO distance never reaches the NGC geometry, which stays 13.8 Mpc and 72 degrees; HANDOFF_CONTRACT_CX3V002), so u serves validation only. (b) invents a coordinate the calibration never varied. (c) changes the step-4 design: the alternate distances are sensitivity cases, not the headline region (A57 B4-1; A61 F3).",
 owner="Builder Codex1, in the step-4 -> step-5 interface round ({ref:fence}); reviewer Claude3. Under 0636 fix rounds are built by a Claude lane or Codex1, not Codex3.",
 decided=None,
 sources=[("cx1_ri_v002", "H2_NATIVE_COORDINATES"), ("cx1_ri_v003", "H2"), ("cx1_rules", "'Independent interface blocker: 3-D native u versus 4-D filler u'"), ("c3_review4", "NOTES, CX-SF3"), ("cx3_contract", "physical-mapping paragraph"), ("v005", "A57 B4-1; A61 F3"), ("d0636", "last line")])

item(group=G1, key="timing", step="4-5 handoff", blocks="LATER", blocks_step="5", phase=10,
 title="Publication timing: wait for the full step-4 decision, or stream points",
 blocks_note="Under the recommendation, step 5 starts after FINAL_SUMMARY and the double replay, as already planned (step-4 R-D15). This item only decides whether step 5 could start earlier.",
 raised_by=["Codex1 H3_PUBLICATION_TIMING (WAIT_FOR_FULL_STEP4_DECISION)", "dispatch 0631 item 2", "step-4 R-D15"],
 issue="TESTED by Codex1 (RULES_AUDIT sections 2 and 4, and 'Stable membership does not freeze the selected region'): rectangle membership is pointwise and stays fixed for fixed identities, but the orchestrator publishes admitted_points only at finalise, after two complete cache-only replays. The freeze's representative members (hull extrema, centroid-nearest and interior members, the anchor) come from the whole admitted set, so they can change while the campaign runs.",
 options=["(a) WAIT_FOR_FULL_STEP4_DECISION, the current contract.",
          "(b) Commission now a reviewed incremental native admission producer, so that NGC runs can start at early points; the final roster, region and freeze still wait.",
          "(c) Keep (a) now, and decide (b) later from measured campaign timings."],
 recommendation="(c). (a) is the contract of record now. After campaign wave 3, when step-4 R-D7 has measured wave walls, root commissions (b) only if the remaining campaign is projected to last longer than building and reviewing (b) plus one integrated NGC point.",
 reasoning="Step 5 scores the freeze's representative members, which depend on the whole region, so NGC calls at early points may not be scored: compute is at risk, not rigour. (b) is a new custody contract on top of {ref:exporter}, which does not exist yet, and needs its own review. The campaign is modelled at 8.7 d E / 14.9 d U (UNTESTED; step-4 R-D7), so the saving could be large, and measured waves turn the choice into a decision on bytes. Overlap also competes with the campaign for memory (step-4 R-D15).",
 owner="Claude2.",
 decided=None,
 sources=[("cx1_ri_v002", "H3_PUBLICATION_TIMING"), ("cx1_rules", "sections 2 and 4; 'Stable membership does not freeze the selected region'"), ("d0631", "item 2"), ("c4_ri_v004", "R-D7; R-D15")])

item(group=G1, key="s1", step="4-5 handoff", blocks="BEFORE_FIRST_RESULT", blocks_step="5", phase=8,
 title="S4-POST-S1: the S1 transfer test before prediction",
 blocks_note="Its registration is step-4 R-C6 (close by BEFORE_CAMPAIGN). Under the recommended reading it must be read before any step-5 output value is read; under the strict reading (option a) it delays the step-5 start by about 5.42 h E / 8.97 h U (UNTESTED).",
 raised_by=["Codex1 H4_POST_S1 (EXISTING_REQUIREMENT_OPEN)", "step-4 R-C6", "RULES_AUDIT section 6"],
 issue="FORMAL (ROOT_ITEMS_FINAL_C4V004 R-C6): ADOPT_TAIL prescribes the 'V005 S1 transfer test at the calibrated point before prediction' (K = 3 and K = 4 at the calibrated point). For the tail scheme no spec, statistic, threshold or reading exists, and there is no admitted launch path: the 0616 packet does not cover it (RUNBOOK_CX1V003 step 1). Its 2 runs are projected at 5.42 h E / 8.97 h U (UNTESTED).",
 options=["(a) Strict: S1 runs and is read before the first step-5 NGC launch.",
          "(b) S1 runs right after FINAL_SUMMARY, alongside the first step-5 point. No step-5 output value is read (validity-only, as the miss-reading prereg already requires) until S1's registered reading is recorded; a failing S1 stops step-5 use under its registered next step.",
          "(c) Rule S1 not applicable to the tail scheme."],
 recommendation="Register S1 target-free now: its cases, the definition of 'the calibrated point' (fixed before any campaign result is read), the statistic, the thresholds (V005 S1's where they apply, stricter where the text is silent) and the reading. Give it a guarded template, or a path root names in a V006 entry, with all four 0620 controls enforced before any process. Adopt (b), and record it in V006 as root's reading of 'before prediction'.",
 reasoning="(b) keeps the blind order that matters (the reading is fixed first, and S1 is read before any step-5 value is), and it takes 5.42-8.97 h (UNTESTED) off the step-5 start. (a) is the literal alternative if root reads 'prediction' as the NGC run itself. (c) would make adoption easier than the V007 text, against the A48 principle.",
 owner="Claude2 (registration, ruling, launch); template builder Codex1 (the packet's builder); distinct reviewer Claude3.",
 decided=None,
 sources=[("cx1_ri_v002", "H4_POST_S1"), ("cx1_rules", "section 6"), ("c4_ri_v004", "R-C6"), ("d0620", "Ruling (the four controls)"), ("v005", "A48 governing principle")])

item(group=G1, key="v007rec", step="4-5 handoff", blocks="BLOCKS_START", blocks_step="5", phase=6,
 title="The authentic adopted V007 record behind v007_adoption_pin",
 blocks_note="The consumer requires the adopted record, and writer v008 pins a derived view instead.",
 raised_by=["Codex1 H5_V007_NATIVE_CUSTODY (V003 text)", "Codex1 SEMANTIC_DELTA finding 3 (OPEN)", "Claude3 0094 SF3; ADM-SF1 and CX-SF2 (NOTEs)", "Codex3 R1"],
 issue="FORMAL: the consumer's handoff field names the externally adopted V007 record ($ABSOLUTE_ADOPTED_V007_RECORD; HANDOFF_CONTRACT_CX3V002). Writer v008's checked_v007 returns a derived verdict VIEW (L137) and writes it into v007_adoption_pin (L212); the filler only byte-pins it (SEMANTIC_DELTA finding 3; Claude3 0094 SF3). Step 4 names the same verdict in its own config: C1 carries numerics.verdict_artifact (step-4 R-A1), and APPROVED_V007_SEALS carries the verdict sha (step-4 R-A2).",
 options=["(a) v007_adoption_pin is the sealed compare's verdict report itself: the same {path, sha256} that C1's numerics.verdict_artifact and the R-A2 seal tuple name, pinned by root in its V006 adoption entry. The writer verifies that equality, and the VIEW stays in the WRITER_RECEIPT as evidence only.",
          "(b) Keep the VIEW in the pin.",
          "(c) Pin the SEAL_RECORD instead."],
 recommendation="(a): one V007 record, with one sha, in steps 4 and 5.",
 reasoning="The consumer contract names the adopted record, and a self-describing view authenticates nothing (Claude3 0094 SF3; SEMANTIC_DELTA finding 3). Binding the pin to the artifact that the calibration gates read (R-A1, R-A2) makes the step-5 handoff and the step-4 adoption provably the same verdict. (c) pins the seal, not the adoption outcome.",
 owner="Claude2 names the record at T0, in a V006 entry; the writer binding is built by Codex1 (the {ref:exporter} round); reviewer Claude3.",
 decided=None,
 sources=[("cx1_ri_v003", "H5"), ("cx1_semantic", "finding 3"), ("c3_review4", "SHOULD_FIX 3; NOTES, ADM-SF1 and CX-SF2"), ("cx3_contract", "handoff paragraph"), ("c4_ri_v004", "R-A1; R-A2"), ("cx3_ri_v002", "R1")])

item(group=G1, key="certscope", step="5", blocks="BLOCKS_START", blocks_step="5", phase=7,
 title="NGC certificate scope at the step-4 admitted points",
 blocks_note="Per point, before that point's NGC launch. The producer should be built during step 4, so only compute remains after FINAL_SUMMARY.",
 raised_by=["Codex1 H6_CERTIFICATE_SCOPE (the scope half)", "Codex3 R4 and R5", "Claude3 0088 missing item 13", "Claude3 0094 CX-N1 (NOTE)"],
 issue="FORMAL: target-free NGC records exist and pass on saved states: EPS_CERT_NGC91_V001 1d5eef1b (CERTIFIED to 91 /kpc); LO_NGC_K32_CERT_V001 07745bbf (PASS on [2,91]; its (64,91] shell is a D-cap, Claude3 S2 N6); GQ_NGC_91_MS96 be148bab (PASS); I1T_NGC_T120L_V001 3ae7981a (iteration 0 only); and the K32 N-tests (N_FAIL_N1, with the route A/B gate OPEN under A66; A90). A101 closed the tail-domain star-transform convergence (TESTED PASS). The seal carries EPS_NGC and I1T_NGC (A107.1). None of them was computed at a step-4 admitted point. For DDO154 the sampled EPS over the calibration box reached 0.0125, against 6.42e-4 at the anchor, so calibration requires per-point certificates and refuses anchor substitution (V005, A65 section, Codex2 Lane A; A73). Claude3 0094 CX-N1: production cannot carry PENDING certificates, so no ADMITTED handoff exists until point-bound NGC certificates exist.",
 options=["(a) Reuse the saved-state NGC certificates for every step-5 point.",
          "(b) Keep the saved-state K32 / M_s 96 N-tests and GQ_NGC as the registered numerics gate for all points (on the premise that they are operator and geometry properties, which is UNTESTED: see the recommendation), and require per-point NGC EPS and LO certificates, plus I1-T at the point's own source and the reviewed validity replay for NGC91_K32_MS96 that H6 names, before each point's launch, failing closed, as for DDO154.",
          "(c) (b), plus N-test reruns at every point."],
 recommendation="(b). Build and review the NGC per-point producer now, on a synthetic or anchor point, and time it. Root rules in V006 that the saved-state K32 N-test reading, with its A66 consequence, applies at every step-5 point (Claude3's missing item 13), and records it as an assumption with its basis: the premise that the N-tests do not depend on the calibrated point is UNTESTED (no source tests it), and its basis is that the NGC operator, geometry and K_big are fixed (A64.2) and that the DDO precedent runs its convergence tests at saved states.",
 reasoning="GQ does not depend on mass (A48 AMB-12) and the NGC geometry is fixed, so GQ_NGC stands. EPS and LO depend on the point's source, as the DDO evidence shows, so (a) assumes an independence that the evidence contradicts. (c) re-tests operator numerics that the pre-target K_big rule already fixed (A64); the DDO structure (convergence tests at saved states, certificates per point) does not ask for it. (b) has exactly the DDO structure, so it is not easier than the precedent.",
 owner="Claude2 rules. Producer builder Claude3 or Claude4, as root assigns by capacity (the DDO per-point producers were Codex2's, now out of usage, A103); cross-lineage reviewer Codex1.",
 decided="In part: NGC K_big 32 (A64.2); NGC gas M_s 96 (A81 RI-23, with GQ_NGC_91_MS96 PASS); the N-test reading and gate (A66; A90); the star-transform convergence (A101); the seal's carriage of EPS_NGC and I1T_NGC (A107.1), with their slots pinned (A111 P4). Open: whether the certificates are per point.",
 sources=[("cx1_ri_v003", "H6"), ("cx3_ri_v002", "R4; R5"), ("cx3_report", "evidence paragraph"), ("c3_review5", "Missing ROOT_ITEMS 13"), ("c3_s2", "claim 2; N6; missing item 13"), ("c3_review4", "NOTES, CX-N1"), ("v005", "A48 AMB-12; A64; A65 section (Codex2 Lane A); A73; A81 RI-23; A90; A101"), ("v006", "A107.1; A111 P4")])

item(group=G1, key="content", step="4-5 handoff", blocks="BLOCKS_START", blocks_step="5", phase=6,
 title="Target-free content for every handed-off or carried artifact",
 blocks_note="Before the first real handoff.",
 raised_by=["Codex1 H6 (the content half); SEMANTIC_DELTA finding 2 (OPEN)", "Claude3 0094 SF2; CX-N4 (NOTE)", "Claude3 0088 SF6 (S2-SF4)"],
 issue="TESTED by Claude3: the writer's content screen is a key-name deny-list, so target-shaped rows under other keys (errV, vrot, v_rot, vcirc, RotationCurve, observations, sigma_obs, vel_km_s, rows, V) in a certificate artifact are pinned into the ADMITTED handoff, and the filler copies them into numerics.uv_tail (0094 SF2). The extractor carries opaque payloads verbatim, including target-row shapes and observed_velocity_km_s or vobs_km_s keys (0088 SF6). Freeze v003g already screens its own root documents (_scan_forbidden, _root_target_screen).",
 options=["(a) Extend the deny-lists.",
          "(b) An allow-list schema per artifact type (each real certificate or proof schema, the export, the handoff, each carrier): exact fields and types, validated on the same bytes that are pinned, with the v003g screen as a second layer.",
          "(c) Rely on root's sha pins."],
 recommendation="(b), in the shared module ({ref:fence}), used by the writer, the filler and the extractor. If an existing native proof cannot be handed off target-free, root selects a target-free representation with retained native custody before production (Codex1 H6, V003).",
 reasoning="No deny-list can enumerate target spellings, and Claude3 found ten that pass; an allow-list fails closed. (c) is the present state, in which safety rests on root never pinning a wrong file.",
 owner="Codex1 builds it with {ref:fence}; Claude3 reviews; Claude2 approves the schemas.",
 decided=None,
 sources=[("cx1_ri_v003", "H6"), ("cx1_semantic", "finding 2"), ("c3_review4", "SHOULD_FIX 2; NOTES, CX-N4"), ("c3_review5", "SHOULD_FIX 6"), ("c3_s2", "S2-SF4")])

item(group=G1, key="driver", step="5", blocks="BLOCKS_START", blocks_step="5", phase=6,
 title="The step-5 driver, and the policies that must follow it",
 blocks_note="No current filler, registry or carrier policy accepts the accepted driver.",
 raised_by=["Codex1 H7_DRIVER_CONSUMER_SELECTION (V003)", "Codex3 R3 (stale)", "Claude3 0088 SF3 and missing items 1-3", "Claude3 0094 CX-SF4 and ADM-N8 (NOTEs)", "A103"],
 issue="FORMAL: A93 accepted cx3r007 and retired the r006 registry; A103 accepted cx3r008 (577f8c94) as the step-5 NGC driver in its place, with its registry pinned from bytes before step 5. TESTED by Claude3 (0088 SF3): the selected filler and POLICY 4f0d7d03, STEP5_REGISTRY_CX3V002 (default r006_fallback), LAUNCH_ORDER_CX3V002 step 1, ROOT_ITEMS_CX3V002 R3 and the FREEZE_EXPECTED_INPUTS first_pass still name r006; no policy accepts cx3r008, and the extractor refuses an r008 result with DRIVER_CUSTODY. Writer v008 still accepts r006_fallback (Codex1 H7, V003).",
 options=["(a) Successors of the filler POLICY, the STEP5 registry, the carrier policy and the writer binding that accept only cx3r008 577f8c94, with its accepted review pin (REVIEW_NGC_V011_CX3R008_C4V001 7ff20c1d) and SPEC_REGISTRY_CX3R008_V002 2c3f421d, and refuse r006 and r007. The stale texts are replaced in the same round: LAUNCH_ORDER_CX3V002 step 1 ('choose r006 fallback unless Claude4's r007 review is accepted') by a successor or a root note citing A103; the FREEZE_EXPECTED_INPUTS first_pass input by the {ref:freezeinputs} successor; ROOT_ITEMS_CX3V002 R3 by this list ({ref:rilist}).",
          "(b) Run step 5 on cx3r007 under the existing policies."],
 recommendation="(a), in the step-4 -> step-5 interface round ({ref:fence}). Root pins the registry from bytes (A103), verifies the full driver sha from bytes before every NGC launch, and checks each result's driver_sha256 (A77.1 N8; A93).",
 reasoning="(b) contradicts A103. Every live r006 path is a fallback that A93 retired, and leaving one invites an automatic fallback (Codex1 H7).",
 owner="Codex1 builds; Claude3 reviews; Claude2 pins and verifies.",
 decided="The driver: A93 (r006 retired) and A103 (cx3r008 is the step-5 driver). Open: the policy successors.",
 sources=[("cx1_ri_v003", "H7"), ("cx3_ri_v002", "R3"), ("cx3_order", "step 1"), ("cx3_freeze_inputs", "first_pass.root_inputs"), ("c3_review5", "SHOULD_FIX 3; Missing ROOT_ITEMS 1-3"), ("c3_s2", "S2-SF3"), ("c3_review4", "NOTES, CX-SF4 and ADM-N8"), ("c4_r8review", "Object table"), ("v005", "A77.1; A93; A103")])

item(group=G1, key="authority", step="4-5 handoff", blocks="BLOCKS_START", blocks_step="5", phase=7,
 title="Release authority and receipt verification at every handoff",
 blocks_note="A root procedure, at the first handoff.",
 raised_by=["Codex1 H8_PUBLICATION_AND_REVIEW (V003)", "Claude3 0094 CX-SF1, CX-N2 and ADM-N6 (NOTEs)"],
 issue="FORMAL: the writer's printed digest is not an authority. Claude2 must publish the release-authority digest independently, verify the WRITER_RECEIPT bytes and bindings, and publish the verified receipt and handoff pins; root keeps the receipt, because custody is one-way.",
 options=["(a) Make H8 a step-5 RUNBOOK step.", "(b) Accept the writer's printed digest."],
 recommendation="(a). For each handoff root (1) publishes the authority digest in a V006 entry before the writer runs; (2) re-hashes the WRITER_RECEIPT and checks its authority and producer bindings, and its export and handoff pins against the emitted bytes; (3) publishes the verified receipt and handoff pins; (4) runs the filler with that handoff pin. launch_authorized stays false throughout. The per-handoff V006 entries then serve as the issuance record whose absence Claude3 notes (0094 ADM-N6).",
 reasoning="(b) lets an input authorize itself, which every review of this interface rejects (HANDOFF_CONTRACT_CX1V002; Claude3 0094 CX-SF1).",
 owner="Claude2.",
 decided=None,
 sources=[("cx1_ri_v003", "H8"), ("c3_review4", "NOTES, CX-SF1, CX-N2 and ADM-N6"), ("cx1_contract", "'Proposed producer and authority boundary'")])

item(group=G1, key="contract", step="4-5 handoff", blocks="BLOCKS_START", blocks_step="5", phase=6,
 title="Adopt the step-4 -> step-5 handoff contract",
 blocks_note="Adopting it now gives the successor builds a fixed target; it admits nothing.",
 raised_by=["Codex3 R2", "Codex1 0074 production blocker (4), 'root contract adoption'", "HANDOFF_CONTRACT_CX1V002 (writer side)", "HANDOFF_CONTRACT_CX3V002 (consumer side)"],
 issue="FORMAL: both contracts are proposals awaiting root adoption. TESTED by Claude3 (0094): the writer's handoff matches the filler's strict 10-field shape, the mock chain writer -> filler -> dry planner passes with 0 executed stages, and the handoff and export are structurally target-free.",
 options=["(a) Adopt the shape now in V006, and require {ref:exporter}, {ref:coords}, {ref:v007rec}, {ref:certscope}, {ref:content}, {ref:driver}, {ref:authority} and {ref:fence} before the first real handoff.",
          "(b) Adopt only the final successor versions.",
          "(c) Ask for a different contract."],
 recommendation="(a). Adopt: the 10-field handoff; the export with only log_index, u and theta_natural, for every admitted point (Claude3 0094 ADM-N7: the current export lists one); the externally published root digest as the only trust anchor ({ref:authority}); FULL_FINAL_DECISION timing ({ref:timing}); exclusive outputs; launch_authorized always false. Each successor re-pins the contract version it implements.",
 reasoning="The shape is TESTED compatible and target-free by construction. Fixing it now gives every successor one target without granting any admission. (b) delays the builds, and (c) has no supporting finding.",
 owner="Claude2.",
 decided=None,
 sources=[("cx3_ri_v002", "R2"), ("cx1_0074", "'UNTESTED / production blockers', item (4)"), ("cx1_contract", "whole"), ("cx3_contract", "whole"), ("c3_review4", "'What holds', Contract; NOTES, ADM-N7")])

# ===== Group 2: Codex3 0614 / 0618, step-5 readiness =====
G2 = "G2"
item(group=G2, key="custody", step="5", blocks="BLOCKS_START", blocks_step="5", phase=6,
 title="Per-point custody of run-produced inputs",
 blocks_note="A ruling only.",
 raised_by=["Codex3 R6", "Codex3 0618 rough edge (a refused geometry sensitivity)"],
 issue="FORMAL (ROOT_ITEMS_CX3V002 R6): at each actual point and grid, keep route-A convergence custody, the whole-radius cut decision or an explicit null, the mass-loss fraction, the rebuilt source and checkpoint, and the confinement checks; never reuse another point's or grid's cut; keep every 43-row failure, INVALID record and gate pin. A60: a query between the last retained route-B node and the pinned outer cut is INVALID (QUERY_OUTSIDE_RETAINED_SUPPORT), and the outer-cut INVALID set must equal {R_q >= first_unconfined_R} from the pinned cut record. A62 (F5): the freeze is two-pass: raw results, then cut records, then root's roster, then a replay.",
 options=["(a) Adopt R6 as the step-5 custody rule.", "(b) Allow a validated cut to be reused across points."],
 recommendation="(a), with Codex3's rule that a refused geometry sensitivity stays INVALID, never zero-width (0618 rough edges).",
 reasoning="The cut depends on the point's own confinement (A60), so a transplanted cut would make INVALID rows a free choice; the two-pass freeze needs every raw record (A62).",
 owner="Claude2 (root-only launches and custody).",
 decided="In part: A60 (gap rows, cut binding) and A62 (the two-pass freeze).",
 sources=[("cx3_ri_v002", "R6"), ("cx3_carr_delta", "other_rough_edges_not_changed"), ("v005", "A60; A62")])

item(group=G2, key="interface", step="5", blocks="BLOCKS_START", blocks_step="5", phase=6,
 title="One integrated interface per point, caps, first-point timing and one machine-wide schedule",
 blocks_note="Rulings: the interface and the first point's caps.",
 raised_by=["Codex3 R7", "LAUNCH_ORDER_CX3V002 steps 3-4", "step-4 R-D15"],
 issue="TESTED by Codex3 and confirmed by Claude3 (0088): the A and B templates normalize identically except for their label (12 semantic checks); both plan the integrated A -> B chain, so running both repeats the solve. UNTESTED: no NGC route-B runtime exists, and the only route-A projection is 15.07-25.07 h at one worker and 16 serial-column iterations, from an old basis and not a K32 bound. FORMAL (memory): no NGC K32 memory model exists. The only NGC resource plan, ADMITTED_POINT_RESOURCE_PLAN_V001 (4de87df9), is a K15 design estimate: its K15_tail_memory has cap_GiB_per_process 0.6 with status DESIGN_ESTIMATE_UNTESTED_ON_NGC_FIXED_POINT, its serial_peak_estimate_bytes_UNTESTED is 3,170,424,422.4, and its proposed caps are 5 GiB serial and 45 GiB for parallel8. It predates NGC K_big 32 (A64.2), and its 0.6 GiB per-process tail cap is the value of the tail module's memory guard before A55 raised that guard to 8 GiB. READINESS_REPORT_CX3V001 reports only dry-process RSS (at most 89,751,552 B). FORMAL (step-4 R-D15): after FINAL_SUMMARY, step 5 shares the machine with S4-POST-S1, DIII4 and the sensitivity batches.",
 options=["(a) One integrated interface per point and grid; the first headline point solo, under monitoring; caps for later points from its measurement; one machine-wide schedule.",
          "(b) Launch every selected point at once, with projected caps."],
 recommendation="(a). Use interface A: the two are equivalent (TESTED), and A carries no pending route-A sentinel. Before the first launch, name the memory model the first point's caps rest on, because none exists for NGC at K_big 32: either (i) commission a target-free K32/T120L memory estimate (the tail state at K_big 32 plus the route-A tree), from a lane Claude2 assigns (Codex1 ran the K32 N-test replays, A90; Codex3 is in reserve, 0638), and apply the A61 rule to it (an RSS cap of at least 1.5 x the modelled peak); or (ii) rule an explicit first-point cap with stated headroom over the K15-era figures, labelled UNTESTED. Either way the first point runs solo under monitoring, with no automatic retry, and later caps are re-derived from its measured RSS, wall and disk, which is the plan's own sequence ('Run first admitted point under root monitor; measure RSS/wall/disk ... Only then schedule within caps'). Schedule S4-POST-S1 first ({ref:s1}). Optional and UNTESTED: NGC route A at column_workers 8, only after a TESTED serial = parallel bitwise identity on the NGC operator and a reviewed template successor (the A47 I4 precedent; production BLAS stays single-thread, A95).",
 reasoning="No defensible bound for T_A + T_B exists until one point is measured. A cap set from a model of another regime is the E-OPS2 error class (A61: a launch plan and its sketched caps were sized from the peaks of runs that had admitted route A, for cases that compute it), so the model behind the first cap has to be named, even when it is only a stated headroom. (b) repeats that class for every point at once. One schedule keeps step 5 from crowding out S4-POST-S1, whose reading gates step-5 reading.",
 owner="Claude2 (rulings and the first launch); the memory estimate, if commissioned, by the lane Claude2 assigns.",
 decided=None,
 sources=[("cx3_ri_v002", "R7"), ("cx3_order", "steps 3-4; wall-time paragraph"), ("cx3_report", "wall-time and resource paragraphs"), ("cx3_resource_plan", "K15_tail_memory; serial_peak_estimate_bytes_UNTESTED; proposed_caps_require_Claude2_registration; admitted_point_sequence"), ("c3_review5", "'What holds', templates"), ("c4_ri_v004", "R-D15"), ("v005", "A47 I4; A55; A61; A64.2; A90; A95"), ("d0638", "Codex3 paragraph")])

item(group=G2, key="registry", step="5", blocks="BLOCKS_START", blocks_step="5", phase=7,
 title="Per-point launch registry, fresh dry plan and driver check",
 blocks_note="Per point, after its handoff.",
 raised_by=["Codex3 R4", "LAUNCH_ORDER_CX3V002 step 2", "READINESS_REPORT_CX3V001", "Claude3 0088 S2 N11", "A103"],
 issue="FORMAL: each real handoff needs a fresh dry plan and preflight on the concrete filled specs and the real certificate pins; synthetic dry success does not imply certificate acceptance (LAUNCH_ORDER_CX3V002 step 2; READINESS_REPORT). The registered NGC specs are the 8 dry-readiness fixture specs (A93 accepted cx3r007 'for the 8 registered NGC specs'; Claude3 S2 N11 on registry cd30429c), so filled step-5 specs are members of no current registry; A103 pins the cx3r008 registry from bytes before step 5.",
 options=["(a) Per point: fill the specs from the published handoff; choose one interface ({ref:interface}); register the chosen spec's sha in a root V006 entry or in a launch-registry successor that cx3r008 accepts; dry-plan it under cx3r008 with the real certificate pins (0 executed stages, no blockers); verify the driver sha from bytes; launch; check the result's driver_sha256.",
          "(b) Launch filled specs against the dry-readiness registry."],
 recommendation="(a).",
 reasoning="(b) runs specs that no launch registry names, while A77.1, A80.2 and A93 each name the registry that NGC route A/B launches from.",
 owner="Claude2 (root-only launch); the registry successor comes from the {ref:fence} round.",
 decided=None,
 sources=[("cx3_ri_v002", "R4"), ("cx3_order", "step 2"), ("cx3_report", "certificate paragraph"), ("cx3_contract", "certificate_pins paragraph"), ("c3_s2", "N11"), ("v005", "A77.1; A80.2; A93; A103")])

item(group=G2, key="freezeinputs", step="6", blocks="BEFORE_FIRST_RESULT", blocks_step="5", phase=8,
 title="Freeze v003g inputs: one complete list before any value is read",
 blocks_note="Fixed before any step-5 output value is read, as the title and the reasoning require. It also blocks step 6, because v003g refuses any missing input.",
 raised_by=["Codex3 R8", "Codex3 0618 READINESS_DELTA (the complete six-alternative and raw result, cut and gate registrations)", "Claude3 0088 S2 N9; SF3 (the stale r006 first_pass input)"],
 issue="FORMAL: v003g needs the evaluated ORIGINAL_K results, every representative member, the exact-theta sensitivity results, complete six-alternative rosters in declared order (the four NOT_EVALUATED ones explicit), all cut, gate, query and GL provenance, and the failed records. TESTED by Claude3 (S2 N9): FREEZE_EXPECTED_INPUTS_CX3V002 omits parameter_region (with bounds_semantics), observation_rule, the coordinate spec, the DDO154 observation-region file in input_files, the notes used by A16.1 and A13, and allow_incomplete; v003g has no field for the TSR flag record or the carriers.",
 options=["(a) A FREEZE_EXPECTED_INPUTS successor that lists every write_freeze_manifest input with its producing record and owner, with the TSR flag record and the carriers as pinned input files. It also drops the stale first_pass root input 'registered driver branch acceptance or r006 fallback' and names cx3r008 (A93; A103; Claude3 0088 SF3).",
          "(b) Assemble the inputs at freeze time from the RUNBOOK."],
 recommendation="(a), target-free and now, pinned before any step-5 output value is read; v003g unchanged.",
 reasoning="A complete list fixed before any step-5 value is read keeps every input a registered choice; (b) leaves the selection to a moment when values exist.",
 owner="Builder Codex1 (author of the steps 6-7 rehearsal) or Claude3; reviewer Claude4 (the v003g reviewer, 0071).",
 decided="In part: A62 (the two-pass freeze) and A70 (v003g ready).",
 sources=[("cx3_ri_v002", "R8"), ("cx3_freeze_inputs", "whole; first_pass.root_inputs"), ("cx3_carr_delta", "current_remaining_before_launch_or_freeze"), ("c3_review5", "SHOULD_FIX 3"), ("c3_s2", "N9"), ("v005", "A62; A70; A93; A103")])

item(group=G2, key="origk", step="5", blocks="BEFORE_FIRST_RESULT", blocks_step="5", phase=8,
 title="ORIGINAL_K: evaluate it, and define its spec pair",
 blocks_note="Rule before any step-5 output value is read; the ORIGINAL_K calls follow the headline members.",
 raised_by=["Codex3 R8 (FREEZE_EXPECTED_INPUTS, 'uncovered_required_evaluated_alternative')", "Claude3 0088 SF5 (S2-SF2) and missing item 9", "step-4 R-D13"],
 issue="FORMAL: slots V003 register ORIGINAL_K as EVALUATED_BEFORE_FREEZE: entropy_K_factor 1.0 instead of 64/121, at the same selected points, with 'DDO154 admission at K = 1 is not re-established' counted. The four readiness templates do not cover it. TESTED by Claude3 (S2-SF2): the carrier join compares only physical (without entropy) and coefficients, so different numerics, interface or source_slots still read AVAILABLE.",
 options=["(a) Evaluate it. The spec pair is the headline spec with only physical.entropy_K_factor (1.0) and the label changed: same numerics, source and interface. The carrier join compares the full normalized spec except those keys and route_a_inputs.",
          "(b) Record NOT_EVALUATED_BEFORE_FREEZE, before any step-5 output value is read. This needs a root-approved slots successor first: slots V003 register ORIGINAL_K as EVALUATED_BEFORE_FREEZE, and FREEZE_EXPECTED_INPUTS says root must supply its results and 'not silently omit it'.",
          "(c) Decide after the headline results."],
 recommendation="(a), run after the headline members and before the exact-theta sensitivity calls; (b), with its slots successor, only if root rules it blind, for compute.",
 reasoning="(a) is the registered plan and supplies the ORIGINAL_K half of the P8 report ({ref:m13}). (c) lets the alternative set depend on seen predictions.",
 owner="Claude2 rules; the spec-pair rule and the join fix go in the {ref:fence} round (Codex1; reviewer Claude3).",
 decided=None,
 sources=[("cx3_freeze_inputs", "uncovered_required_evaluated_alternative; exact_alternative_declarations"), ("c3_review5", "SHOULD_FIX 5; Missing ROOT_ITEMS 9"), ("c3_s2", "S2-SF2"), ("c4_ri_v004", "R-D13")])

item(group=G2, key="stage0", step="5", blocks="BEFORE_FIRST_RESULT", blocks_step="5", phase=8,
 title="The optional evaluated-STAGE0 successor",
 blocks_note="Soft: if it is not pinned before any step-5 output value is read, STAGE0 reads NOT_EVALUATED_BEFORE_FREEZE (NO_SEALED_SUCCESSOR). It never delays the headline (A65.2).",
 raised_by=["Codex3 R9", "0606 item 1", "Codex3 0618 rough edges", "r3 M-14 (step 6)"],
 issue="FORMAL: slots V003 register STAGE0_GRID_OUTER as NOT_EVALUATED_BEFORE_FREEZE, and v003g refuses an evaluated STAGE0 under them (Claude4 0071 N2); evaluation needs a root-approved immutable slots and module successor. STAGE0 runs at the same admitted points, with only the coefficient grid swapped to bdb9016c, after the headline and with spare compute; its OUTER score uses Q36-Q43 (A65). FORMAL (Claude4 0124): the first SEAL CANDIDATE names no STAGE0 successor, so under r3 M-14 STAGE0 reads NOT_EVALUATED_BEFORE_FREEZE (NO_SEALED_SUCCESSOR) unless the seal entry pins one or, under the Status fallback, the candidate that gives the pre-prediction versions names it.",
 options=["(a) Prepare the successor now. Its only change permits EVALUATED_BEFORE_FREEZE for STAGE0; scope, grid pin and headline:false stay as they are. Review it, pin it in the miss-reading seal entry, and let the r3 receipt rule fix the status mechanically.",
          "(b) Do not prepare it, so STAGE0 stays NOT_EVALUATED_BEFORE_FREEZE."],
 recommendation="(a).",
 reasoning="Without (a), STAGE0 cannot be evaluated even when its runs finish in time, and R-DRIFT keeps no deciding comparison. The r3 receipt rule (FINISHED receipts before RUNBOOK step 4, and a successor pinned before any value is read) leaves no post-prediction choice. The cost is one small target-free build and its review.",
 owner="Builder Codex1 or Claude3 (0636 excludes Codex3); reviewer Claude4, repeating its 0071 STAGE0 checks (r3 M-14); Claude2 pins it.",
 decided="In part: A65 (the registered alternative; after the headline; never delays it; NOT_EVALUATED fallback).",
 sources=[("cx3_ri_v002", "R9"), ("cx3_freeze_inputs", "STAGE0_GRID_OUTER declaration; stage0_status_transition"), ("cx3_carr_delta", "other_rough_edges_not_changed"), ("r3f_root_items", "M-14"), ("c4_0124", "STAGE0 line"), ("v005", "A65")])

item(group=G2, key="r6", step="4", blocks="LATER", blocks_step="4", phase=10,
 title="A cache or parallel-tail driver for steps 4-5",
 blocks_note="Nothing to rule for either start.",
 raised_by=["Codex3 R10", "step-4 R-B1"],
 issue="FORMAL: V007 seals on r5, and r6's partial bytes are unused; caching for steps 4-5 is decided later, with the A85.1 parallel-tail result (A96). v006r9 accepts only r5. A new driver for step 4 changes every registry point key (the driver sha is in the key) and needs its own identity gates and an orchestrator retarget (step-4 R-B1).",
 options=["(a) Step 4 on r5 and step 5 on cx3r008, as now.", "(b) Adopt a cache or parallel-tail successor for step 4 or step 5."],
 recommendation="(a) for both starts. Revisit (b) for step 5 only if a successor with TESTED bitwise identity, its own identity gates and its review is ready without delaying step 5 (the A89 no-delay rule, by analogy).",
 reasoning="A re-key at the step-4 start would void the 28 point keys that the certificate registry (S4-R-C1) fixes now, which is the costliest start item.",
 owner="Claude2.",
 decided="V007 on r5 (A96); step 4 on r5 (step-4 R-B1, by A96). Open: only a later step-5 optimization.",
 sources=[("cx3_ri_v002", "R10"), ("c4_ri_v004", "R-B1"), ("v005", "A85.1; A89; A96")])

item(group=G2, key="tsr", step="5", blocks="BEFORE_FIRST_RESULT", blocks_step="5", phase=8,
 title="The A66 radial-support mapping for the TRUNCATION_SHAPE_RESIDUAL flags",
 blocks_note="Ruled with the miss-reading seal, before any step-5 output value is read; the flag record must exist before the freeze (step 6).",
 raised_by=["Codex3 R12; Codex3 0618 TSR carrier", "Claude3 0088 missing items 7 and 14; S2 N7", "r3 M-7 (step 6)", "A66.2"],
 issue="FORMAL (r3 M-7 facts, from target-free records): the failing ring is ordinal 15 at R = 10.540847190215317 kpc, with S/theta = 1.01481832531416; its stored radial_support is a single sampled radius, which flags no row. The N1 ring radii equal the registered route-B GL4 nodes (ring 14 at 9.901811 kpc, ring 16 at 10.911722 kpc); the route-B value at node k depends only on ring k; and rows are piecewise-linear interpolants of the node values. The extractor holds all 43 flags null until root adopts a support record (0618).",
 options=["(i) Dependence: r_14 < R_q < r_16, which flags Q25 only.", "(ii) The stored point: no row.", "(iii) The ring's sampling cell: no row.", "(iv) The two bracketing query rows: Q25 and Q26."],
 recommendation="(i), with r3 M-7's support record (lower 9.901810628740723 kpc and upper 10.911721936765339 kpc, both exclusive; native_ring the compare's ordinal-15 record verbatim), in kpc at the registered 13.8 Mpc manifest radii (the frame Claude3 asked for; moot while geometry sensitivity is NOT_EVALUATED). Carry it as a separate root-pinned, target-free flag record listed among the freeze manifest's input files (Claude3's missing item 7; r3 M-7), screened by {ref:content}.",
 reasoning="(i) follows how a row's value is made, so no width is chosen. (ii) and (iii) empty the row-level disclosure that A66 requires, and (iv) flags a row that cannot depend on the ring. The flag is a disclosure, never INVALID (A66.2).",
 owner="Claude2 adopts and pins the support and flag records; Claude4 supplies them with r3; the extractor ({ref:carriers}) emits the 43 flags.",
 decided="A66 (a flag, not INVALID; a reading added). Open: the support mapping.",
 sources=[("cx3_ri_v002", "R12"), ("cx3_freeze_inputs", "a66_residual_disclosure"), ("cx3_carr_report", "TSR row"), ("c3_review5", "Missing ROOT_ITEMS 7 and 14"), ("c3_s2", "N7; N8"), ("r3f_root_items", "M-7"), ("v005", "A66")])

item(group=G2, key="carriers", step="5", blocks="BEFORE_FIRST_RESULT", blocks_step="5", phase=8,
 title="The carrier contract: adoption, authenticity and the freeze vehicle",
 blocks_note="Adopt it before carriers are extracted from real step-5 results.",
 raised_by=["Codex3 0618 (carrier_registration REQUIRED_FROM_ROOT)", "Claude3 0088 missing items 6 and 7; S2 SF1, SF2, SF4 and N2-N5"],
 issue="FORMAL, with Claude3's TESTED findings: CARRIER_CONTRACT_CX3V001 (252ef9e1) defines a strict request and three optional root-record schemas. Authenticity rests on the root request sha (S2 N5). The extractor's fence is lexical (S2 SF1), its ORIGINAL_K join is incomplete (S2 SF2), its payloads are unscreened (S2 SF4), point_key is free (S2 N2), the E1b readout is not bound to the headline alternative (S2 N3), and the N-test compare is not bound to K_big 32 and an OPEN gate (S2 N4).",
 options=["(a) Adopt the contract, with an extractor successor that closes S2 SF1, SF2, SF4 and N2-N4, a written authenticity rule (root request sha, producer pins, before-target attestation), and the carriers pinned as separate input files of the freeze manifest.",
          "(b) Adopt it as it is.", "(c) Drop the carriers."],
 recommendation="(a).",
 reasoning="(b) carries known gaps into the freeze; (c) loses the TSR disclosure that A66 requires.",
 owner="Claude2 adopts; the extractor successor goes in the {ref:fence} round (Codex1); reviewer Claude3.",
 decided=None,
 sources=[("cx3_carr_decision", "carrier_registration"), ("cx3_carr_report", "whole"), ("cx3_carr_contract", "hashed"), ("c3_review5", "Missing ROOT_ITEMS 6 and 7"), ("c3_s2", "S2-SF1, SF2, SF4; N2-N5")])

# ===== Group 3: Claude3 0088, step-5 readiness review =====
G3 = "G3"
item(group=G3, key="fence", step="4-5 handoff", blocks="BLOCKS_START", blocks_step="5", phase=6,
 title="One shared fence, I/O and screen module for the writer, the filler and the extractor",
 blocks_note="Before the first real handoff and the first carrier extraction.",
 raised_by=["Claude3 0088 SF1, SF2, SF4 and SF8 (with S1 N-6)", "Claude3 0094 SF1, SF5 and SF6 (it proposes one shared module); CX-N3 and ADM-N4 (NOTEs)", "Claude4 0104 PAR8-N6"],
 issue="TESTED by Claude3: the fences are lexical and narrow (NGC_3198, 'NGC 3198', N3198, UGC5572, DDO154, SPARC MassModels and /.vol spellings pass); resolve() runs before the refusal and touches protected metadata; files are read before their sha check; outputs follow dangling symlinks, '..' and symlinked parents; integers over 4300 digits, deep nesting, invalid bytes and 1e999 raise untyped tracebacks, though every case fails closed (Claude3 0094 CX-N3 and ADM-N4 note the same untyped errors on long integers in the writer's API). FORMAL (Codex1 0104; BUILD_CX1V002): writer v010 already refuses recognized target-path aliases before I/O, refuses output symlink and parent traversal with descriptor-relative exclusive creation, and refuses excessive nesting; Claude3's delta review of v010 is pending. FORMAL: the writer, the filler and the extractor parse only JSON (other inputs, such as the raw compare and addendum slots, are byte-pinned and not parsed: Claude3 0094 CX-N4), and the filler requires an integer, nonnegative selected log_index and finite, non-boolean u entries (HANDOFF_CONTRACT_CX3V002). PAR8-N6 (Claude4 0104): Codex3's dry-harness guard refuses target words only when the path contains ngc3198.",
 options=["(a) One module: refuse lexically first (aliases and catalogue terms); then open, fstat (S_ISREG, and nlink == 1 or an inode allow-list) and re-check the canonical path (F_GETPATH) before any read; refuse /.vol; bound every read (cap + 1); hash before parsing; confine outputs as writer v010 does; type every error; and carry the {ref:content} schema screen. JSON is parsed strictly, with no text fallback: the bytes must decode as strict UTF-8 with no BOM; a JSONDecodeError is a typed refusal; objects go through a duplicate-refusing object_pairs_hook (A71); integers go through a bounded parse_int inside that same parse (a literal over a digit cap is a typed refusal, otherwise int(), so integer fields such as log_index stay integers); parse_constant refuses NaN and Infinity, and parse_float refuses non-finite results such as 1e999; and nesting depth is capped before or during the parse, as writer v010 does. The module also covers any dry harness root uses for the per-point dry plans of {ref:registry} (PAR8-N6).",
          "(b) Patch each tool separately."],
 recommendation="(a), derived from writer v010's tested code. Each tool's own suite is re-run, and Claude3's probes become MUST_FAIL cases, together with a non-JSON input, an over-long integer literal, NaN, Infinity, 1e999, a duplicate key and an over-deep document. The same round carries {ref:coords}, {ref:driver}, {ref:origk}, {ref:carriers} and {ref:pointkey}.",
 reasoning="The same defect classes recur in three tools, and once more in the r12 A-B1 class (A102). One reviewed module closes them once, while per-tool patches drift. Target-freedom should not rest on root's pins alone. A71 and A102 give the principle (a duplicate refuses inside the parse, and no untyped ValueError path survives); A102's text fallback belongs to check_record_codes, whose legitimate text-format controls A90 keeps, and in a tool that parses only JSON a fallback would add an acceptance path for non-JSON bytes. parse_int=str would turn the filler's integer log_index into a string.",
 owner="Codex1 builds; Claude3 reviews, with its own probes as the regression suite.",
 decided=None,
 sources=[("c3_review5", "SHOULD_FIX 1, 2, 4 and 8"), ("c3_s2", "S2-SF1"), ("c3_s1", "hashed only"), ("c3_0094", "SHOULD_FIX 1, 5 and 6; 'For root'"), ("c3_review4", "SHOULD_FIX 1, 5 and 6; NOTES, CX-N3, ADM-N4 and CX-N4"), ("cx1_0104", "whole"), ("cx1_build2", "whole"), ("cx3_contract", "L11 (log_index and u rules)"), ("c4_r8review", "NOTES, PAR8-N6"), ("v005", "A71; A90; A102")])

item(group=G3, key="rilist", step="5", blocks="LATER", blocks_step="5", phase=10,
 title="A successor for ROOT_ITEMS_CX3V002",
 blocks_note="Documentary.",
 raised_by=["Claude3 0088 SF7 (S2-SF5)"],
 issue="FORMAL: ROOT_ITEMS_CX3V002 (18:56Z) predates A93, 0606 and A103, and its later open items sit only in READINESS_DELTA prose. Codex3 is in reserve (0638) and builds no fix rounds (0636).",
 options=["(a) Root adopts this document, after its refuter, as the step-5 root-item list.", "(b) Commission ROOT_ITEMS_CX3V003 from a lane."],
 recommendation="(a).",
 reasoning="This list carries all twelve R items and the fifteen missing ones, with their rulings and DECIDED markers; (b) would duplicate it.",
 owner="Claude2.",
 decided=None,
 sources=[("c3_review5", "SHOULD_FIX 7"), ("c3_s2", "S2-SF5"), ("d0636", "last line"), ("d0638", "Codex3 paragraph")])

item(group=G3, key="pointkey", step="5", blocks="BEFORE_FIRST_RESULT", blocks_step="5", phase=8,
 title="How point_key is derived and bound",
 blocks_note="Before carriers are extracted from real step-5 results.",
 raised_by=["Claude3 0088 missing item 8 (S2 N2)"],
 issue="TESTED by Claude3: point_key is a free root label in the carrier request, never joined to the call spec's physical point; the same rows were accepted under two keys.",
 options=["(a) point_key is the canonical point hash that the WRITER_RECEIPT records (HANDOFF_CONTRACT_CX1V002), and the extractor joins it to the call spec's physical point and to the handoff pin.", "(b) Keep a free label."],
 recommendation="(a).",
 reasoning="A free key lets one point's carriers be filed under another; deriving it from the receipt ties each carrier to the handoff that root published ({ref:authority}).",
 owner="The {ref:fence} round (Codex1); reviewer Claude3.",
 decided=None,
 sources=[("c3_s2", "N2; missing item 8"), ("cx1_contract", "WRITER_RECEIPT bullet")])

item(group=G3, key="bonly", step="5", blocks="LATER", blocks_step="5", phase=10,
 title="The optional B-only replay successor",
 blocks_note="Only needed if a saved route-A replay is wanted.",
 raised_by=["Claude3 0088 missing item 15", "LAUNCH_ORDER_CX3V002 step 3"],
 issue="FORMAL: a B-only replay of saved route-A custody needs a separately reviewed policy successor; the five native route_a_inputs fields are seed, attempt_directory, checkpoint_directory, identity_sha256 and result_sha256 (HANDOFF_CONTRACT_CX3V002).",
 options=["(a) Do not build it now; one integrated call per point ({ref:interface}).", "(b) Build it now."],
 recommendation="(a). Build it only if a saved route-A replay is later wanted.",
 reasoning="No current plan needs it.",
 owner="Claude2.",
 decided=None,
 sources=[("c3_s2", "missing item 15"), ("cx3_order", "step 3"), ("cx3_contract", "route_a_inputs paragraph")])

# ===== Group 5: Claude4 0104, cx3r008 =====
G5 = "G5"
item(group=G5, key="partb", step="5", blocks="BLOCKS_START", blocks_step="5", phase=6,
 title="PAR8-SF1: pin the one r008 traceback class that A98.1 does not list",
 blocks_note="Documentary: no code, driver-sha or registry change.",
 raised_by=["Claude4 0104 PAR8-SF1 = PT8-SF1 (both refuters reproduced it)", "Claude3 0088 missing item 1 (PAR-TB-1)", "Codex3 0618 (PAR-TB-1 is a prelaunch item)"],
 issue="TESTED by Claude4 (REVIEW_NGC_V011_CX3R008_C4V001): A98.1's r008 enumeration (disposition a9ae801f) omits the class at cmd_dry_run L5147, where r007's `if code==0 and rp.is_file():` becomes `if code==0 and (rp:=Path(report_dir)/'DRYRUN_REPORT.json').is_file():`, caret line included. It shows only in top-level dry-run stderr, and only if is_file() raises after the planner's own write (reproduced with a real EACCES); the exception class and text are identical. FORMAL: A98.1 says 'Any frame class specific to r008 is enumerated and pinned before closure; there is no blanket waiver', and dispatch 0619 (L15) says 'Pin any r008-specific frame class before closure'.",
 options=["(a) Root pins the class in a V006 entry: both source lines, the caret line and the scope (top-level dry-run stderr only; exception class and text identical), citing the review 7ff20c1d.",
          "(b) A one-entry successor of disposition a9ae801f, built by a Claude lane or Codex1 (0636) and delta-checked by Claude4.",
          "(c) Waive it."],
 recommendation="(a), written so that it pins the class as firmly as a disposition would: it quotes both source lines and the caret line verbatim, states the scope, is cited by its own section sha (V006 is an open file, so the entry is pinned by section, not by file), and names the record a later parity check reads (disposition a9ae801f together with this entry). It needs no builder (Codex3 is in reserve). The entry may also record that the inside-NGC frame classes (a)-(e) follow from ST7-SF1 and ST7-SF2 and lie outside PAR-TB scope (verify_closure_1, section 4). Batch it with root's other V006 entries: a V006 heading written before the miss-reading seal entry needs a row in r3's V006 table and a re-render ({ref:sealcand}). If root prefers a single record for every class, take (b), the review's own fix.",
 reasoning="(c) is a blanket waiver, which A98.1 forbids. The review's fix is (b), a disposition successor with no code change; (a) carries the same content, and A98.1's 'enumerated, byte-pinned' is met only if the entry is quoted verbatim and pinned by its section sha. The practical risk is nil, so the whole cost of (a) is one entry.",
 owner="Claude2.",
 decided="cx3r008 is accepted (A103) with this finding open; ST7-SF1 and ST7-SF2 are closed (TESTED, Claude4 0104).",
 sources=[("c4_r8review", "Findings, SHOULD_FIX PAR8-SF1"), ("c4_0104", "SHOULD_FIX"), ("c3_s2", "missing item 1"), ("cx3_carr_delta", "driver_delta.prelaunch_closures"), ("v005", "A98.1; A103"), ("d0619", "Codex3 paragraph")])

item(group=G5, key="st8n2", step="5", blocks="BEFORE_FIRST_RESULT", blocks_step="5", phase=8,
 title="ST8-N2: record r008's inside-NGC strictness changes as intended",
 blocks_note="Documentary.",
 raised_by=["Claude4 0104 ST8-N2"],
 issue="TESTED by Claude4: inside NGC, r008 turns some outcomes into typed refusals: NGC_JSON_DEPTH_REFUSED where an untyped RecursionError was raised before, and final_rows_check refusals in run mode, which become REFUSED (exit 3) instead of COMPLETED_INVALID (exit 0). None of the 8 registered NGC specs reaches them (Claude4 0104). Filled step-5 specs are new specs (Claude3 S2 N11), and whether they can reach them is UNTESTED.",
 options=["(a) Record them as intended in V006, and state how a REFUSED step-5 run enters the freeze: as a structured failure with its 43 rows kept, never dropped ({ref:custody}).", "(b) Leave them unrecorded."],
 recommendation="(a).",
 reasoning="A refusal and an INVALID completion are read differently downstream; fixing the reading before any step-5 result keeps it from being chosen afterwards.",
 owner="Claude2.",
 decided=None,
 sources=[("c4_r8review", "NOTES, ST8-N2"), ("c3_s2", "N11")])

item(group=G5, key="notes0104", step="5", blocks="LATER", blocks_step="5", phase=10,
 title="The other cx3r008 notes",
 blocks_note="No action before step 5.",
 raised_by=["Claude4 0104 ST8-N1, N3, N4 and N5; PAR8-N1 to N5"],
 issue="FORMAL: ST8-N1 (r007's last-wins readiness block is still live, reachable only through the ST7-N6 race together with a non-driver duplicate); ST8-N3 (the sha() helper is replaced module-wide, with identical digests on 407 files); ST8-N4 (route-A prep L191 still parses last-wins, on bytes the driver now refuses before launch); ST8-N5 (an erratum in the cx3r007 review's note count); and PAR8-N1 to N5. PAR8-N6 goes to {ref:fence}.",
 options=["(a) No action before step 5; carry ST8-N1 and ST8-N4 to the next driver successor, if one is built.", "(b) Commission a driver successor now."],
 recommendation="(a).",
 reasoning="Each is unreachable or documentary for the step-5 specs, while a successor would change the driver sha and cascade the registry and every review.",
 owner="Claude2.",
 decided=None,
 sources=[("c4_r8review", "NOTES, ST8-N1 and N3-N5; PAR8-N1 to N6")])

# ===== Group 6: step 4 (Claude4's package), start-blocking items in full =====
G6 = "G6"
item(group=G6, key="s4a3", fixed_id="S4-R-A3", step="4", blocks="BLOCKS_START", blocks_step="4", phase=1,
 title="The case-block binding in the sealed prereg",
 blocks_note="Closes at the seal (A108 step 1); nothing to rule.",
 raised_by=["ROOT_ITEMS_FINAL_C4V004 R-A3"],
 issue="TESTED here (strict JSON, from bytes, at 01:08Z): SELECTED_R6_C4V001 7200acd9 pins case_block CASE_BLOCK_V007_C4V001 76309ae3, and the r6 text of record d28c95f5 carries binding_inputs.case_block with that same path and sha. FORMAL: Codex1 0109 reads the r6 SELECTED file PASS, 0 blocking (as reported in Claude4 0118). The sealed compare refuses CASE_BLOCK_ABSENT without the binding.",
 options=["(a) Keep the binding through the seal and re-check it from bytes at assembly.", "(b) Re-open the case block."],
 recommendation="(a), inside the A108 seal steps.",
 reasoning="Nothing has changed the case block since A101.",
 owner="Claude2, at seal assembly.",
 decided="In progress: A106.1 approved r6, A107.3 records the provisional cross-check, and A108 sets the seal steps.",
 sources=[("c4_ri_v004", "R-A3"), ("r6_selected", "files.case_block"), ("r6_text", "binding_inputs.case_block"), ("c4_0118", "'Seal inputs: done'"), ("v005", "A101; A106.1"), ("v006", "A107.3; A108")])

item(group=G6, key="s4b6", fixed_id="S4-R-B6", step="4", blocks="BLOCKS_START", blocks_step="4", phase=2,
 title="The launch path of the 33 direct calls: the guarded packet",
 blocks_note="If the packet is not admitted when V007 adopts, step 4 waits (0620).",
 raised_by=["ROOT_ITEMS_FINAL_C4V004 R-B6"],
 issue="FORMAL: 0620 removed the zero-build fallback; the 33 direct calls (HEADLINE11, DIII4, SENS_LO9, SENS_HI9) launch only through Codex1's guarded packet (0616). Its successors landed (BUILD_CX1V002; Codex2 0515: PASS_WITH_FINDINGS, 0 blocking, in a bounded scope). Not yet admitted: the complete reviewed transitive source inventory (G7-SCOPE-1); the final root inputs (C1, policy, registry, certificates, sensitivity evidence, caps, output paths); Claude4's final specs; the PRELAUNCH records; root admission. No newer packet message existed at 00:06Z (INDEX section 4), and no Codex1 post from 0100 to 0120 mentions G7-SCOPE-1, a source inventory or a transitive closure (TESTED here, grep of those 21 named posts at 02:25Z).",
 options=["(a) Admit the packet once G7-SCOPE-1 and the final inputs close.", "(b) Any other path (removed by 0620)."],
 recommendation="(a). Codex1 builds the G7-SCOPE-1 inventory now, during step 2, and Claude3 reviews it (A103; 0635); the inventory covers the PRELAUNCH tool (S4-R-B4a) and the disk guard (S4-R-D17). Root then binds templates_v004 with the final specs (S4-R-A1), the caps and route-A cap (S4-R-D8), the output paths (S4-R-D17), the PRELAUNCH records (S4-R-B4a) and, for DIII4, the tail_off_policy (S4-R-B7).",
 reasoning="It is the only admitted path, and closing G7-SCOPE-1 during step 2 keeps it off the critical path.",
 owner="Codex1 (builder); Claude3 (review); Claude2 (admission).",
 decided="The path itself: 0620.",
 sources=[("c4_ri_v004", "R-B6"), ("c4_index", "section 4"), ("d0620", "Ruling"), ("v005", "A103"), ("d0635", "Claude3 row")])

item(group=G6, key="s4b4a", fixed_id="S4-R-B4a", step="4", blocks="BLOCKS_START", blocks_step="4", phase=2,
 title="The one-call PRELAUNCH check for the direct calls (the prelaunch part of R-B4)",
 blocks_note="Built and reviewed before T0, run at H1. The 0616 launcher refuses any call whose pinned PRELAUNCH record is not the exact replay of guard007's native_preflight, so HEADLINE11 cannot be admitted without it. No builder is assigned.",
 raised_by=["ROOT_ITEMS_FINAL_C4V004 R-B4 (its prelaunch-check part, split out here; its campaign entry is S4-R-B4b, by reference)", "LAUNCH_ORDER_C4V002 section 4.1 (L110) and H1 (L133)", "IMPLEMENTATION_INTERFACE_CX1V003 'Plan and PRELAUNCH'; RUNBOOK_CX1V003 step 4"],
 issue="FORMAL (ROOT_ITEMS_FINAL_C4V004 R-B4): 'Root also needs a one-call prelaunch check for standalone specs', and 'PRELAUNCH must include the actual certificate-policy and per-spec checks, because the r9 prelaunch function alone permits a null registry' (Codex1 0065). R-B4's Blocks line reads 'The campaign launch; the PRELAUNCH records the 0616 plans pin', its owner line 'builder any lane; distinct review', and R-B6's disposition binds 'the PRELAUNCH records (R-B4)'. LAUNCH_ORDER_C4V002 puts 'PRELAUNCH per spec on those bytes (R-B4)' on HEADLINE11's launch path (L110), and at H1 'Root runs PRELAUNCH on those exact bytes with the certificate-policy and per-spec checks (R-B4)' (L133). FORMAL (IMPLEMENTATION_INTERFACE_CX1V003; guard007 L187-222 and L266): the PRELAUNCH file is exactly the deterministic return of native_preflight(admission, call), which runs the native certificate_policy_gate, certificate_check(prelaunch) and sensitivity_gate for a tail-ON call and checks the DIII tail_off_policy for a tail-OFF call; root obtains it 'by a controlled in-process, read-only call after final inputs exist' and publishes it under a new name; the launcher's validation (guard007 validate) refuses unless each call's pinned PRELAUNCH equals a fresh native_preflight replay (PRELAUNCH_REPLAY_MISMATCH). RUNBOOK_CX1V003 step 4 says to generate PRELAUNCH through guarded native_preflight and publish it exclusively. TESTED here (grep of the three named files): binder v006 and launcher v008 contain no PRELAUNCH writer, and guard007 has no command-line entry, so the packet ships no tool for that call.",
 options=["(a) A small reviewed tool: under guard007's own fence, it calls guard007.native_preflight(admission candidate, call) unchanged for each call of a batch, in process and read-only, and writes each PRELAUNCH record by exclusive create under a new name, with a manifest of {case, spec, driver, prelaunch} pins for the binder. MUST_FAIL controls: a null registry or policy, an unregistered point, a PASS label in place of the native return, a changed spec byte, a wrong driver, and a DIII call without its tail_off_policy (S4-R-B7).",
          "(b) Root makes the in-process call by hand at H1, with a checklist.",
          "(c) Extend the binder to generate the PRELAUNCH records."],
 recommendation="(a), built and reviewed during step 2, so that at H1 it only runs. Builder: Codex1, the packet's author (the tool calls guard007's native_preflight unchanged); if Codex1 lacks capacity, Claude4 builds it and Codex1 reviews (A109). Distinct reviewer: Claude3 (A103; 0635). It joins the G7-SCOPE-1 source inventory (S4-R-B6). The campaign's own per-call prelaunch_check stays inside Orchestrator.run's gates (S4-R-B4b).",
 reasoning="The launcher accepts only the exact native replay, so the record cannot be typed by hand, and (b) puts an unreviewed step on the critical path of every direct batch. (c) changes the reviewed binder, in which Codex2's delta (0515) found 0 blocking. Calling native_preflight unchanged confines the new review to the wrapper, its fence and its exclusive writes. The record leaves the builder open ('any lane'), so without an assignment HEADLINE11 waits at H1.",
 owner="Builder unassigned (the record says 'any lane'): recommended Codex1, reviewer Claude3; Claude2 runs it at H1 and publishes the records.",
 decided="The launch path: 0620 (only the 0616 packet, for the 33 direct calls).",
 sources=[("c4_ri_v004", "R-B4; R-B6"), ("c4_order_v002", "section 4.1 (L110); section 4.2, H1 (L133); section 5.2"), ("cx1_iface3", "'Plan and PRELAUNCH'"), ("cx1_guard7", "L187-222; L266"), ("cx1_bind6", "grep"), ("cx1_launcher8", "grep"), ("cx1_runbook3", "steps 3-4"), ("d0620", "Ruling"), ("v006", "A109"), ("d0635", "Claude3 row")])

item(group=G6, key="s4c1", fixed_id="S4-R-C1", step="4", blocks="BLOCKS_START", blocks_step="4", phase=2,
 title="Per-point certificate admission and the registry (28 or 31 points)",
 blocks_note="PRELAUNCH under C1 refuses an unregistered point, TAIL_REANCHOR included. Today no builder is active for it.",
 raised_by=["ROOT_ITEMS_FINAL_C4V004 R-C1 (and R-C8 for the 31-point option)"],
 issue="FORMAL: the registry needs a prelaunch bundle per point: one GQ record, full EPS/rho tables and LO from a reviewed LO producer successor, because the current LO finish() is always UNAVAILABLE. The 28 point keys are fixed now by the C4T block (TESTED in the record), so CP-1 needs no V007 byte. The producers were Codex2's, and Codex2 is out of usage (A103), so no builder is active: no dispatch through 0648 (listed at 02:49Z; 0648 is seal-path wiring) assigns them. UNTESTED: GQ takes about 17.3 min serial for 28 points; EPS/rho and LO have no timing record.",
 options=["CP-1 window (a): phase P, before the seal.", "CP-1 window (b): during step 2 at background QoS, with root's memory attestation, never holding back a T-case.", "CP-1 window (c): after T0, as added time before H2.", "Points: 28, or 31 with the 3 Jacobian side points of wave 2."],
 recommendation="Assign now: the LO producer successor to Claude4 or Claude3 (root, by capacity; A109), with Codex1 as cross-lineage reviewer. Window (b): A108 seals now, so (a) is unlikely, and (c) puts unestimated compute on the critical path. 31 points, so that campaign waves 1-2 can run before the registry-growth design (R-C8) exists. Time the first bundle end to end.",
 reasoning="It is the only start blocker with no active builder, and its compute is unestimated.",
 owner="Claude2 (science review, registration, CP-1 operator); the builder and reviewer as above.",
 decided=None,
 sources=[("c4_ri_v004", "R-C1; R-C8"), ("c4_index", "section 5, 'Rulings the records ask root for'"), ("v005", "A72; A85.2; A95; A103"), ("v006", "A108; A109")])

item(group=G6, key="s4d1", fixed_id="S4-R-D1", step="4", blocks="BLOCKS_START", blocks_step="4", phase=2,
 title="The TAIL_REANCHOR source",
 blocks_note="A ruling.",
 raised_by=["ROOT_ITEMS_FINAL_C4V004 R-D1"],
 issue="FORMAL: the reanchor can be a fresh template run (default), DU-1 (the mapper-built trial spec) or DU-3 (the V007 C4T run); 0557 N-1 says it launches from the template's physical values. PC-7 needs two calls at the anchor point.",
 options=["(a) A fresh template run.", "(b) DU-1, by explicit ruling.", "(c) DU-3."],
 recommendation="(a).",
 reasoning="It is 0557 N-1's literal wording, and with HEADLINE11 it keeps PC-7 met.",
 owner="Claude2.",
 decided=None,
 sources=[("c4_ri_v004", "R-D1")])

item(group=G6, key="s4d2", fixed_id="S4-R-D2", step="4", blocks="BLOCKS_START", blocks_step="4", phase=2,
 title="Designate the workers_8 row",
 blocks_note="A ruling.",
 raised_by=["ROOT_ITEMS_FINAL_C4V004 R-D2"],
 issue="FORMAL: either the anchor repeat (WORKERS_8_CANDIDATE_ANCHOR in Codex1's HEADLINE template, which also serves PC-7) or one headline corner run (DU-2).",
 options=["(a) The anchor repeat (HEADLINE11).", "(b) DU-2: designate C000 before launch (HEADLINE10)."],
 recommendation="(a).",
 reasoning="DU-2 saves only 0.29 h E / 0.56 h U (UNTESTED) and needs its own root entry.",
 owner="Claude2.",
 decided=None,
 sources=[("c4_ri_v004", "R-D2")])

item(group=G6, key="s4d5", fixed_id="S4-R-D5", step="4", blocks="BLOCKS_START", blocks_step="4", phase=2,
 title="The deciding-(iii) pairs: caps and placement",
 blocks_note="A ruling; under the recommended placement it adds nothing to the calibration path.",
 raised_by=["ROOT_ITEMS_FINAL_C4V004 R-D5"],
 issue="FORMAL: 4 tail-OFF calls (2 D x {REFERENCE_V009GEO, NEW_R5}) that launch only after the sealed ADOPT_TAIL, through the 0616 guard, with no overlap with step 2 or the campaign; their only consumer is the sensitivity runs.",
 options=["(a) After FINAL_SUMMARY and before SENS.", "(b) Right after HEADLINE11, during H3 (adds up to 4.61 h E / 7.77 h U if H3 is shorter; UNTESTED)."],
 recommendation="(a), with caps of wall 43,200 s, RSS 16 GiB and output 96 GiB, recorded in V006.",
 reasoning="The record's caps meet the 1.5x rule against the tail-OFF route-A model (1.64x) and cover the 57.7 GiB worst-case output (UNTESTED model).",
 owner="Claude2.",
 decided=None,
 sources=[("c4_ri_v004", "R-D5")])

item(group=G6, key="s4d8", fixed_id="S4-R-D8", step="4", blocks="BLOCKS_START", blocks_step="4", phase=2,
 title="Caps for the direct tail-ON runs, and the route-A concurrency cap",
 blocks_note="The 0616 templates refuse null caps, and guard007 refuses a plan without a root-approved max_active (ROUTE_A_CAP_REQUIRED).",
 raised_by=["ROOT_ITEMS_FINAL_C4V004 R-D8", "INDEX_STEP4_READINESS_C4V002 section 5 (the route-A cap)", "LAUNCH_ORDER_C4V002 sections 6.4-6.5", "Claude3 0105 PKG-S3 (no root item carries the route-A cap ruling)"],
 issue="FORMAL: the 0616 templates leave caps null and refuse until root supplies positive integers, and guard007 requires a root-approved max_active, an integer from 1 to 6 (L243; IMPLEMENTATION_INTERFACE_CX1V003, 'Ramp and process boundary'). The V007 C4T plan caps are 19 h, 28 GiB and 96 GiB; helper C's modelled peak for this class is 18.79 GiB, so 28 GiB is 1.490x (TESTED arithmetic in the record). The record's default is those plan caps, taking 29 GiB 'if root wants the 1.5x margin over the model exactly' (R-D8). For the route-A cap, LAUNCH_ORDER_C4V002 section 6.4 recommends cap 3 for the 9- to 11-call batches (Codex1's proposal), or cap 2 if root wants modelled free memory at or above 25% after admission: the 25% gate is checked before each admission and reserves nothing for the call it admits, and under cap 3 HEADLINE11's modelled free memory after admission falls to 17.1%. Section 6.5: cap 2 keeps 25% after admission only while the post-route-A increment over the C4R3 tree peak (2.805 GiB) is at most 1.80 GiB (exactly 1.7972 GiB); with the rotation tail held through a column pair cap 2 gives 19.9% E / 24.1% U; and the rule at H1 is to read the C4T run's measured tree RSS after route A first, or else treat cap 2's property as unverified. TESTED here, as exact arithmetic on the same UNTESTED model (all 11 HEADLINE11 calls running, 17 GiB background, 128 GiB): the record's 17.1%, 28.6%, 19.9% (E) and 1.7972 GiB reproduce (17.09%, 28.57%, 19.89%, 1.7972 GiB); cap 3 keeps 25% only while the after-route-A term is at most 2.829 GiB (an increment of 0.024 GiB); and cap 1 keeps 25% while the increment is at most 3.216 GiB (a term of 6.021 GiB). No source models cap 1's wall time (UNTESTED).",
 options=["(a) The record's default: 19 h, 28 GiB and 96 GiB, with route-A cap 3 (Codex1's proposal; LAUNCH_ORDER_C4V002 section 6.4).",
          "(b) 19 h, 29 GiB and 96 GiB (A61's 1.5x margin), with the route-A cap read at H1 from the C4T record by the rule in the recommendation.",
          "(c) (b)'s RSS cap with route-A cap 3, accepting the modelled 17.1% dip after admission."],
 recommendation="(b). The RSS cap is 29 GiB. Root sets the route-A cap at H1 by this rule: (1) read the V007 C4T run's measured tree RSS after route A from its step-2 monitor record (the RSS record, not only the peak); (2) if the increment over 2.805 GiB is at most 1.80 GiB, cap 2; (3) if the increment is larger, or no after-route-A RSS record exists (cap 2's property is then unverified), cap 1, which keeps 25% up to an increment of 3.22 GiB at an unmodelled wall cost, unless root records in V006 that it accepts a modelled dip below 25% after admission, in which case cap 2; (4) if the increment exceeds 3.22 GiB, no cap keeps 25%, and root records that it accepts the dip or re-plans the batch; (5) cap 3 only if root records that it accepts the modelled 17.1% dip (option c). Both choices depart from the record's defaults (28 GiB; cap 3), and the V006 entry says so. The ROOT_ITEMS_FINAL_C4V005 candidate (in build) carries the route-A cap as its own item, R-D18, and recommends cap 3 with cap 2 as the 25% option and the same RSS precondition, which is this item's option (c) as the default: the two lists differ only in the default, and root picks one.",
 reasoning="A61 requires RSS caps of at least 1.5x the modelled peak: 1.5 x 18.79 = 28.19 GiB, so 28 GiB misses the rule by 0.19 GiB, and 29 GiB meets it (1.54x). The memory gate guards only the moment of admission (section 6.4), so only the route-A cap bounds free memory after it, and the record makes cap 2's 25% property conditional on the C4T measurement (section 6.5). The rule therefore reads that measurement first and has a branch for every outcome. Cap 3 keeps 25% only if the after-route-A term barely exceeds the 2.805 GiB tail-OFF peak, so in practice choosing it means accepting the dip.",
 owner="Claude2.",
 decided=None,
 sources=[("c4_ri_v004", "R-D8"), ("c4_index", "section 5 (the route-A cap)"), ("c4_order_v002", "sections 6.1-6.5"), ("cx1_iface3", "'Ramp and process boundary'"), ("cx1_guard7", "L243-246"), ("c3_review_s4v2", "SHOULD_FIX 7 (PKG-S3)"), ("c4_v005_md", "R-D18 (candidate)"), ("v005", "A61")])

item(group=G6, key="s4d9", fixed_id="S4-R-D9", step="4", blocks="BLOCKS_START", blocks_step="4", phase=2,
 title="The hull-miss contingency",
 blocks_note="A ruling, before a headline corner can miss.",
 raised_by=["ROOT_ITEMS_FINAL_C4V004 R-D9"],
 issue="FORMAL: v006 has no bracket recovery and the block must equal the C4T numerics, so a miss under the full hull is a hard stop (hull top margin about 2.5%; review r5).",
 options=["(a) Register the response now: record the miss, stop new launches of that theta, and root rules on a registration.", "(b) Decide when a miss happens."],
 recommendation="(a), never widening ad hoc.",
 reasoning="(b) would be a rule chosen after a result.",
 owner="Claude2.",
 decided=None,
 sources=[("c4_ri_v004", "R-D9")])

item(group=G6, key="s4d11", fixed_id="S4-R-D11", step="4", blocks="BLOCKS_START", blocks_step="4", phase=2,
 title="Operational settings for step 4",
 blocks_note="A ruling.",
 raised_by=["ROOT_ITEMS_FINAL_C4V004 R-D11"],
 issue="FORMAL: the record reads A85.2-4 (QoS, sleep assertion) as step-2 settings. A85.3 and A85.4 name step 2, while A85.2's background QoS for lanes' non-critical processes 'applies from the step-2 launch onward'. The 0616 packet carries normal QoS at root launch, single-thread BLAS and caffeinate -i -w <launcher pid>, and requires that no campaign and no step-2 route A is running; the campaign work dir is pinned on External1.",
 options=["(a) Apply the packet's settings to every direct batch, and the same QoS and sleep assertion to the campaign launcher; lanes use taskpolicy -b where allowed (A95); External1 stays mounted; a plan-mode run on C2 verifies the work dir and VolumeUUID before wave 1.", "(b) Rely on step 2's settings."],
 recommendation="(a).",
 reasoning="(b) leaves step 4 with no sleep assertion and no core priority.",
 owner="Claude2.",
 decided=None,
 sources=[("c4_ri_v004", "R-D11"), ("v005", "A85; A95")])

item(group=G6, key="s4d17", fixed_id="S4-R-D17", step="4", blocks="BLOCKS_START", blocks_step="4", phase=2,
 title="Disk plan and output placement for step 4",
 blocks_note="Output paths are mandatory template fields.",
 raised_by=["ROOT_ITEMS_FINAL_C4V004 R-D17", "Claude3 0105 PKG-S1 (A105.3 not folded in; the disk guard has no implementer)"],
 issue="FORMAL: every step-4 output is kept (the cleanup authorization is NOT USED). UNTESTED model: the 33 direct calls need about 709.5 GiB typical, and all step-4 calls about 3.25 TiB typical and 8.73 TiB worst. TESTED here (df -k): 420.6 GiB available on the internal volume and 3273.2 GiB on External1 at 01:08:08Z, and 418.1 GiB and 3273.2 GiB at 02:18:07Z. FORMAL (A105.3, RP-S2): step 2's outputs stay on the internal SSD (A85.3), about 250 GB expected against V011 caps that add up to 992 GiB, with a watchdog that alerts root below 80 GB free; so the direct calls cannot go there. FORMAL (Claude3 0105 PKG-S1, from its package lens): guard007 and launcher008 have no free-disk check (only memory_free and the per-call caps), so the disk guard this item recommends has no implementer.",
 options=["(a) External1 for HEADLINE11, DIII4, SENS_LO9, SENS_HI9 and S4-POST-S1, under one fresh step-4 run root with distinct per-call output directories; the campaign work dir as configured (External1).", "(b) The internal SSD (Codex1's template default), by explicit ruling and only for a class whose disk guard fits."],
 recommendation="(a). Disk guard per direct batch: at admission, free space on the output volume of at least calls x output cap + 20 GiB, and before each start at least one output cap + 20 GiB; refuse otherwise. Implementer: Codex1 adds both checks to the 0616 packet (the admission-time check in the guard, the per-start check in the launcher beside the memory gate, failing closed), reviewed by Claude3 with G7-SCOPE-1 (S4-R-B6); until that lands, root records a df reading of the output volume in each batch's admission record and does not admit a batch that fails the admission bound. Measure the headline outputs and re-project before the campaign, and rule D3 retention before the campaign, because the typical model (3.25 TiB) exceeds External1's free space (3.20 TiB). The ROOT_ITEMS_FINAL_C4V005 candidate (in build) names the same implementer, Codex1 with Claude3 reviewing, and adds an interim: an alert-only watchdog on the output volume at one output cap + 20 GiB, after which root applies A105.3's rule (relocate the unstarted calls or pause admission).",
 reasoning="The principal sends new large outputs to External1 (CURRENT_INSTRUCTIONS, about 18:20Z), and the internal SSD holds step 2 under A105.3. The launcher is the only component that sees each start, so the per-start check belongs there; a root reading at admission covers the batch until it does.",
 owner="Claude2 (ruling); Codex1 implements the disk guard in the packet; Claude3 reviews.",
 decided="In part: A105.3 (step-2 outputs stay on the internal SSD, with the 80 GB watchdog).",
 sources=[("c4_ri_v004", "R-D17"), ("c3_0105", "SHOULD_FIX 5 (PKG-S1)"), ("c3_pkg_partial", "PKG-S1"), ("c4_0119", "PKG-S1"), ("c4_v005_md", "R-D17 (candidate)"), ("v005", "A85.3; A105.3"), ("cur_instr", "'Principal: external drive External1 and lane credits'")])

item(group=G6, key="s4a1", fixed_id="S4-R-A1", step="4", blocks="BLOCKS_START", blocks_step="4", phase=3,
 title="C1 and the final step-4 specs at T0",
 blocks_note="At T0, right after the sealed ADOPT_TAIL.",
 raised_by=["ROOT_ITEMS_FINAL_C4V004 R-A1", "Claude3 0105 PR-SF1 to PR-SF5 (the producer review)"],
 issue="FORMAL: C1 carries numerics.{verdict_artifact, block_source, compare, sealed_prereg, adopted_result, source_results} and numerics.block := the sealed C4T call-spec numerics. The final specs are produced on C1 by Claude4's reviewed producer, never regenerated by root, and no PROVISIONAL file is a launch input. Status (FORMAL): Claude3's distinct review of producer 8e835ce3 (produce_final_step4_specs_c4v002.py) and package V002 is done (0105, 01:19:16Z): PASS_WITH_FINDINGS, 0 BLOCKING, 7 SHOULD_FIX. PR-SF1 is an escalation candidate: final mode accepts self-declared synthetic or unverified provenance and labels the output FINAL; it is not BLOCKING only because guard007's adoption() and certificate_check run under root's C1 at PRELAUNCH, a defence read from code, not executed, and root may escalate it. Claude4 0119 (01:20:04Z) started producer v003 (produce_final_step4_specs_c4v003.py), whose final mode must verify from bytes a sealed ADOPT_TAIL verdict, root's pinned C1, block_source tied to case block 76309ae3 and the registry read against its schema, and package V003 (ROOT_ITEMS_FINAL_C4V005 and a spec-handoff successor); Claude3 delta-checks it. TESTED (ls and sha256 at 02:50Z): producer v003 is produce_final_step4_specs_c4v003.py 28921808, and the V003 build wrote the ROOT_ITEMS_FINAL_C4V005 candidate (753e7e25) into its work folder; launch_order/ holds no V005. FORMAL (the V003 work log; the candidate's R-A1): the build stage completed at 02:39:38Z with nothing published; v003's final mode refuses unless the SEAL_RECORD, the verdict, the sealed prereg and compare, the frozen addendum, case block 76309ae3, block_source de6d7d77, the reviewed policy tuple and the registry chain all verify from bytes, and its tests read 148/148; Claude3's delta check is still to come. Codex1 0110 acknowledged the spec handoff.",
 options=["(a) The record's T0 procedure: root writes and announces C1 as {path, sha256}; Claude4 runs the reviewed producer and posts FINAL_SPECS_MANIFEST; optionally the 9 MAPPER_BUILD specs are rebuilt natively and must agree; root runs PRELAUNCH on those bytes (S4-R-B4a); the binder pins only the manifest pins.", "(b) Root regenerates the specs itself."],
 recommendation="(a), with producer v003 (28921808), not 8e835ce3: T0 uses v003 once Claude3's delta check reports 0 blocking with PR-SF1 closed (final mode refuses synthetic or unverified provenance). Root may escalate PR-SF1 to BLOCKING meanwhile; under either reading 8e835ce3 is not a T0 input. Prepare C1 now as a template that differs from r9 only in these fields, the block, and the R-C1, R-C2 and R-D8 fields.",
 reasoning="(a) is the reviewed path; (b) bypasses the producer review and the dual construction. PR-SF1's only defence is a guard check read from code, so the producer that labels specs FINAL should refuse unverified provenance itself.",
 owner="Claude2 (C1, PRELAUNCH, admission); Claude4 (the final specs and producer v003); Claude3 (the delta check of v003).",
 decided=None,
 sources=[("c4_ri_v004", "R-A1"), ("c4_index", "sections 4 and 5"), ("c3_0105", "whole"), ("c3_review_s4v2", "SHOULD_FIX 1-4; NOTES"), ("c4_0119", "whole"), ("c4_0123", "step-4 package row"), ("c4_v003_partial", "log to 02:40:24Z"), ("c4_v005_md", "R-A1 (candidate)"), ("c4_producer_v003", "hashed"), ("c3_0099", "whole"), ("c3_0101", "whole"), ("cx1_0110", "whole")])

item(group=G6, key="s4b7", fixed_id="S4-R-B7", step="4", blocks="LATER", blocks_step="4", phase=10,
 title="The DIII tail_off_policy that guard007 requires (not in ROOT_ITEMS_FINAL_C4V004)",
 blocks_note="Needed before DIII4's admission. Under the default placement (S4-R-D5 (a), after FINAL_SUMMARY) it delays nothing; under the H3 option (S4-R-D5 (b)) it is due before H3.",
 raised_by=["Claude3 0105 PKG-S2", "Claude4 0119 (a root item for it in package V003)", "ROOT_ITEMS_FINAL_C4V005 R-B7 (candidate in build)"],
 issue="FORMAL (IMPLEMENTATION_INTERFACE_CX1V003, 'Runtime authority and root input contract'; guard007 L214-221): DIII additionally needs a tail_off_policy: a root-authorized UNT_STEP4_DIII_POLICY_CX1V001 with status TESTED, verdict PASS and post_adoption_only true, whose cases bind the exact spec and driver of each DIII call. Only the native omitted-uv_tail schema is eligible, and certificate applicability is recorded as reviewed tail-OFF identity, not skipped through a null registry. SPEC_HANDOFF_C4V002 (L86): root's tail_off_policy must bind exactly the four DIII spec/driver pairs that the pair plan cb42a5a3 registers. TESTED here (grep): ROOT_ITEMS_FINAL_C4V004.md and LAUNCH_ORDER_C4V002.md carry 0 mentions of it, as Claude3 0105 PKG-S2 found. FORMAL (ROOT_ITEMS_FINAL_C4V005, a candidate in build): its R-B7 carries the same item with the four pins (DECIDING_III_HIGH_V009GEO and DECIDING_III_HIGH_R5 on spec cf3f0086, DECIDING_III_LOW_V009GEO and DECIDING_III_LOW_R5 on spec 3f8a4c04, with drivers 237ef3d4 and b5cc62af) and closes it by BEFORE_HEADLINE. FORMAL (guard007 L196-221): native_preflight reads the policy only on its tail-OFF branch, so HEADLINE11's admission does not need it, and it does not delay the step-4 start.",
 options=["(a) Draft the policy now, target-free (the four DIII specs and both drivers exist), have it reviewed, and let root authorize it by exclusive create before DIII4's admission.", "(b) Write it at DIII time."],
 recommendation="(a). Claude4 drafts it (it owns the specs), Claude3 reviews it (A103; 0635), and root authorizes and pins it before DIII4's admission, or before H3 if root picks the DIII-early option (S4-R-D5 (b)). The PRELAUNCH tool (S4-R-B4a) refuses a DIII call without it.",
 reasoning="It is a small, target-free document. Drafting it now keeps a root-authorized input off the DIII path, and under the default placement nothing waits on it.",
 owner="Claude4 drafts; Claude3 reviews; Claude2 authorizes.",
 decided="DIII runs only after the sealed ADOPT_TAIL: 0620 (the policy schema's post_adoption_only repeats it).",
 sources=[("cx1_iface3", "'Runtime authority and root input contract' (DIII tail_off_policy)"), ("cx1_guard7", "L214-221"), ("c4_spec_handoff", "L86; L203"), ("c3_0105", "SHOULD_FIX 6 (PKG-S2)"), ("c3_pkg_partial", "PKG-S2"), ("c4_0119", "PKG-S2"), ("c4_v005_md", "R-B7; 'Launch-path step added in V005: DIII (R-B7)'"), ("c4_ri_v004", "R-D5"), ("d0620", "Ruling")])

# ===== Group 7: step 6, the miss-reading prereg r3 =====
G7 = "G7"
PEND = ""
item(group=G7, key="sealcand", step="6", blocks="BEFORE_FIRST_RESULT", blocks_step="5", phase=8,
 title="Publish r3 as a SEAL CANDIDATE, and seal it before any step-5 output value is read",
 blocks_note="Before the first step-5 output read; it never delays step 5 (r3 Status). If it is missed, the fallback governs, and with no candidate the step-6 classification is EXPLORATORY.",
 raised_by=["r3 M-6 (timing and fallback)", "A98.2 (r3 ordered)", "A103 (Codex1 owns the r3 delta)", "Claude3 0088 missing item 11", "Claude4 0124 and 0125"],
 issue="FORMAL (final r3 b0fba984, Status [C-S]; r3 M-6): root rules M-1 to M-15 and seals the text with the M-12 classifier before anyone reads a step-5 output value, and until then step-5 outputs are read validity-only. If the timing fails, the text, the root items and the classifier all come from the last SEAL CANDIDATE post published before the first read; with no such post the whole classification is EXPLORATORY. TESTED (ls and sha256 at 02:13Z): the final r3 folder exists (born 01:56:31Z), with PREREG b0fba984 (unsealed, INDEX_R3) and ROOT_ITEMS_R3 b33270fe (byte-equal to the draft V001 read). FORMAL: Claude4 0124 (02:16:45Z) is the first SEAL CANDIDATE post: text b0fba984, ROOT_ITEMS b33270fe, 'classifier: none', no STAGE0 successor. Codex1's A98.2 delta (0119, record ee375b8d) reads PASS with 0 blocking in its scope (Codex2 0490's two findings), and 0120 carries one SHOULD_FIX, CX1-MR3-P1 ({ref:mr3p1}). Claude4 0125 plans one re-render, carrying that fix and any delta findings, with a new SEAL CANDIDATE post; until then 0124 stands. FORMAL (Claude4 0125, FB-3): V006 is open, and every V006 heading written before the seal entry needs a row in r3's V006 entry table and a re-render, hence a new candidate post; V006 entries are to be appended at the end only. TESTED here (sha256 and a diff of the byte copies): V006 became b22bd18a at 02:42:32Z by inserting A112 before the 'A108 continued' heading, after r3 and 0124 were rendered against 43d4562b, so the re-render must also add a row for A112.",
 options=["(a) Seal the next candidate: the re-render with the CX1-MR3-P1 fix and, if it is built in time, the M-12 classifier ({ref:m12}), before step 5 launches.", "(b) Seal later, but before the first step-5 output read.", "(c) Do not seal: the fallback takes the last candidate published before the first read (now 0124, 'classifier: none'), and the classifier is then labelled POST-PREDICTION (CLASSIFIER)."],
 recommendation="(a). The seal entry goes in V006 (A82; A106.3), names the rendered text's sha and the classifier's, and carries the rulings on M-1 to M-15 or cites them by id. Root batches the V006 entries that this list recommends before the seal into as few headings as possible, appended after the last heading, and tells Claude4 when they land, so that one re-render covers them and A112 (FB-3).",
 reasoning="(a) has days of runway, because step 5 follows step 4's FULL_FINAL_DECISION. (b) works, but leaves the classifier's status to timing. (c) gives up the pre-prediction classifier. Every V006 heading written before the seal costs a re-render and a new candidate post, so batching keeps the candidate stable.",
 owner="Claude4 (re-render and SEAL CANDIDATE posts); Codex1 (delta, A103); Claude2 (rulings and seal entry).",
 decided="The vehicle: V006 (A82; A106.3).",
 sources=[("r3f_prereg", "Status [C-S]"), ("r3f_root_items", "M-6"), ("r3f_index", "file table (unsealed)"), ("c4_0124", "whole"), ("c4_0125", "'Still open, for root at the seal' (FB-3)"), ("cx1_0119", "whole"), ("cx1_r3delta", "scope; verdict; blocking_count"), ("cx1_0120", "whole"), ("r3_fixlog", "whole"), ("v006_copy3", "diff against copy 2 (A112 inserted)"), ("v005", "A82; A98.2; A103; A106.3"), ("c3_s2", "missing item 11")])

item(group=G7, key="m12", step="6", blocks="BEFORE_FIRST_RESULT", blocks_step="5", phase=8,
 title="M-12: the classifier pair and its agreement record",
 blocks_note="Before the first step-5 output read, or the step-6 classifier is labelled POST-PREDICTION (CLASSIFIER).",
 raised_by=["r3 M-12", "Codex1 0082 (M-12 not built; agreement UNTESTED) and 0120", "Claude4 0124 ('classifier: none') and 0125", "Claude3 0088 missing item 11"],
 issue="FORMAL (r3 M-12; Claude4 0124 and 0125; Codex1 0082 and 0120): implementation A (Claude4) is not built, so the first SEAL CANDIDATE names no classifier, and Codex1's earlier B rehearsal and oracle are not an adopted r3 M-12 B implementation (0120); an exact implementation pair and its agreement review are still needed, and their agreement is UNTESTED. TESTED by Codex1 (0082): the old r2 rehearsal shows four adaptation gaps (null ratio, LATE behaviour, NEAR as a tier, half ties), which are cases for the pair, not defects of r3. FORMAL (r3 checks/INDEX_CHECKS_R3): the final r3 adds a pattern suite of the r3 rules on synthetic rows (all_ok true, run by the author's final stage), a check of the text, not the M-12 pair. Claude4 0125: implementation A can start at once if root says so, and it does not touch the V007 seal path.",
 options=["(a) The binding two-lineage pair with the shared suite that r3 M-12 lists.", "(b) A single classifier.", "(c) Hand classification."],
 recommendation="(a). Root tells Claude4 to start A now and Codex1 to bring B to r3 (A103; 0635), so that the pair passes its agreement suite and a SEAL CANDIDATE names A before the first step-5 output read. A is sealed with the text and the agreement record is pinned; root runs A on the real score; B never runs on real data.",
 reasoning="The classifier removes discretion at the one step that sees targets, and a two-lineage agreement turns ambiguous text into a fixable failure before the seal.",
 owner="Claude4 (A); Codex1 (B); Claude2 (the go-ahead and the pins).",
 decided=None,
 sources=[("r3f_root_items", "M-12"), ("c4_0124", "classifier line"), ("c4_0125", "M-12 line"), ("cx1_0120", "M-12 paragraph"), ("cx1_0082", "whole"), ("cx1_prov2", "whole"), ("r3f_checks", "the pattern suite"), ("c3_s2", "missing item 11")])

item(group=G7, key="mr3p1", step="6", blocks="BEFORE_FIRST_RESULT", blocks_step="5", phase=8,
 title="CX1-MR3-P1: the C-9 summary of the sign rule",
 blocks_note="A text fix in a re-render of r3, published as a new SEAL CANDIDATE before the seal. The final r3 folder was written by exclusive create and stays as it is.",
 raised_by=["Codex1 0080 and 0082, CX1-MR3-P1 (SHOULD_FIX, provisional)", "Codex1 0120 (carried as an OPEN SHOULD_FIX)", "Claude4 0125 (confirmed from bytes; fix proposed)"],
 issue="TESTED here (the final r3 b0fba984, at 02:13Z): C-2 (line 242) makes S(Z) UNDEFINED only when m(Z) is UNDEFINED, or when Z is miss-dominated and M(Z) − U(Z) < N_v(Z)/2, but the C-9 row 'Taking a zone's sign from its hits' (line 598) still says 'S(Z) is UNDEFINED unless the signed misses alone reach half of N_v(Z)'. The same row stands at line 598 of the draft fb40156a and of the fix-stage dry build bdcf6aff. An all-HIT zone is CENTERED under C-2 and UNDEFINED under C-9. FORMAL: Codex1 0120 carries it as an OPEN SHOULD_FIX and asks that the successor bytes be verified before closure. Claude4 0125 confirms it, notes that the §2 sentence 'A sign class is therefore never taken from hits…' is loose in the same way (CENTERED is a sign class), and proposes two sentences: the §9 row becomes 'A signed class (DEFICIT or EXCESS) needs a miss-dominated zone whose signed misses alone reach half of N_v(Z); in a miss-dominated zone where they do not, S(Z) is UNDEFINED (§2)', and the §2 sentence becomes 'A signed class (DEFICIT or EXCESS) is therefore never taken from hits, or from a minority of signed misses'.",
 options=["(a) Qualify the C-9 row by miss-domination, or cite C-2; Claude4 0125's two sentences do this and also tighten the §2 sentence.", "(b) Change C-2 to match C-9."],
 recommendation="(a), with Claude4 0125's two sentences; C-2 governs. The fix goes into one re-render, with any other delta findings, and a new SEAL CANDIDATE post (Claude4 0125), and Codex1 verifies the successor bytes before closing it (0120).",
 reasoning="(b) would change the reviewed algorithm through a summary line. The rule itself is unchanged, but the text sha changes, so the fix needs a re-render and a new candidate rather than an edit.",
 owner="Claude4 re-renders r3; Codex1 verifies the successor bytes.",
 decided=None,
 sources=[("cx1_prov1", "finding 1"), ("cx1_prov2", "finding 1"), ("cx1_0080", "whole"), ("cx1_0120", "whole"), ("c4_0125", "CX1-MR3-P1 paragraph"), ("r3f_prereg", "C-2, line 242; C-9 table, line 598"), ("r3_text", "C-9 table, line 598 (draft)"), ("r3_dry", "C-9 table, line 598")])

item(group=G7, key="mr3p2", step="6", blocks="BEFORE_FIRST_RESULT", blocks_step="5", phase=8,
 title="CX1-MR3-P2: the fallback must take one compatible tuple",
 blocks_note="CLOSED by Codex1 (0120): nothing to fix. Root adopts the selector with the seal.",
 raised_by=["Codex1 0080 and 0082, CX1-MR3-P2 (SHOULD_FIX, provisional)", "Codex1 0119 and 0120 (closed)"],
 issue="FORMAL (final r3 b0fba984, Status [C-S] and M-6): the fallback takes the text, the ROOT_ITEMS and the classifier (or 'classifier: none') together from one SEAL CANDIDATE post: the last one published before the first step-5 read, a candidate ruled FAIL before that read being withdrawn. With 'classifier: none' the classifier is built to the pre-prediction text, labelled POST-PREDICTION (CLASSIFIER), and must pass the M-12 suite; with no candidate the classification is EXPLORATORY. This disposes of Codex1's mixed-version case (r3 text with an r2 classifier). FORMAL: Codex1 0120 closes CX1-MR3-P2 ('CLOSED by the one-post fallback tuple and explicit classifier:none handling'), and its 0119 delta finds the same selector in Status and M-6.",
 options=["(a) Accept the one-post selector.", "(b) Select each component separately."],
 recommendation="(a).",
 reasoning="(b) is the defect Codex1 found, and the one-post selector closes it (Codex1 0120).",
 owner="Claude2 adopts it with the seal; Claude4 keeps the selector in every re-render.",
 decided=None,
 sources=[("cx1_prov1", "finding 2"), ("cx1_prov2", "finding 2"), ("cx1_0119", "SHOULD_FIX paragraph"), ("cx1_0120", "CX1-MR3-P2 line"), ("c4_0125", "CX1-MR3-P2 paragraph"), ("r3f_prereg", "Status [C-S], the fallback")])

item(group=G7, key="m3", step="6", blocks="BEFORE_FIRST_RESULT", blocks_step="5", phase=8,
 title="M-3: the §2 rule set, the sign-class rule (A or B) and the meaning of outer-row failure (alpha or gamma)",
 blocks_note="A root choice, ruled with the seal." + PEND,
 raised_by=["r3 M-3", "Codex1 0080 and 0082 (a root choice that neither review adopts); Codex1 0120", "Claude4 0125 (TXT-7: root rules M-3)"],
 issue="FORMAL (r3 M-3): M-3 first asks root to adopt the §2 rule set as written: miss-dominated M ≥ N_v/2 and hit-dominated H > N_v/2, so a tie goes to miss; U(Z), the unsigned MISS rows; the sign class; 'an UNDEFINED quantity makes a condition false', except the definedness tests of P14 and P15; the half-split trend, the even-count median, GROWING (P1g) and CROSSING (P11g); no vacuous patterns; OUTER_FAILURE as OUTER miss-dominated, equivalently exactly one of P1, P2, P11 or P14; the patterns P11 to P15; and P8 named NO_MISS_AMONG_VALID_ROWS. Two choices inside it are not forced. FORMAL (r3): (A) withholds S(Z) when Z is miss-dominated and M - U < N_v/2; (B) only when Z is miss-dominated and M - U < H. (alpha) reads outer-row failure as OUTER miss-dominated, and (gamma) as any failing OUTER row. TESTED by Codex1 on invented states: under (A), a LATE gate can turn P1 into P14 although a signed row remains. FORMAL (r3): with 2 of 8 OUTER rows missing, (gamma) reads TESTED-NEGATIVE and (alpha) reads NOT_NEGATIVE_AT_OUTER.",
 options=["The §2 rule set: adopt it as written, or ask for changes.", "(A) or (B).", "(alpha) or (gamma)."],
 recommendation="Adopt the §2 rule set as written, with (A) and (alpha), as r3 recommends.",
 reasoning="(A) never takes a sign class from a minority of the zone's rows, and its LATE dependence can only withhold a class, never create or switch one. (alpha) follows A15 E2 and E3, which state the outer expectation for the rows as a set, so a TESTED-NEGATIVE never rests on one row's sigma. (B) and (gamma) are sound alternatives if root prefers invariance under gate timing or a single-row trigger.",
 owner="Claude2.",
 decided=None,
 sources=[("r3f_root_items", "M-3"), ("cx1_prov1", "logical-controls table"), ("cx1_0080", "whole"), ("cx1_0120", "root-choices line"), ("c4_0125", "TXT-7")])

item(group=G7, key="m15", step="6", blocks="BEFORE_FIRST_RESULT", blocks_step="5", phase=8,
 title="M-15: the LATE-gate definition, and an all-LATE outer zone",
 blocks_note="A root choice, ruled with the seal. Under (a), a gate stays ON-TIME only if root pins it before the first step-5 launch receipt." + PEND,
 raised_by=["r3 M-15", "Codex1 0080 and 0082 (a root choice); Codex1 0120", "Claude4 0125 (TXT-7: root rules M-15)"],
 issue="FORMAL (r3): (a) a gate is ON-TIME if and only if its document's sha is pinned in a root entry stamped before the first step-5 launch receipt; (b) it is ON-TIME if registered before the first step-5 output value exists. (1) An OUTER zone whose non-INVALID rows are all LATE-gate rows reads P14 and TESTED-NEGATIVE with no OUTER prediction; (2) it reads NOT_TESTABLE. TESTED by Codex1 (bounded model): an all-gated OUTER zone moves from P9 / NOT_TESTABLE to P14 / TESTED-NEGATIVE when its gates become LATE.",
 options=["(a) or (b).", "(1) or (2)."],
 recommendation="(a) and (1), as r3 recommends. Root also pins every gate document it already knows in a V006 entry before the first step-5 launch; an entry in or after the miss-reading seal entry needs no re-render of r3 ({ref:sealcand}, FB-3).",
 reasoning="(a) is decidable from bytes (an entry's date -u against a launch receipt), while no record carries the time an output first existed, which (b) needs. (1) is stricter: a gate made after the predictions exist cannot turn TESTED-NEGATIVE into NOT_TESTABLE, and the E3 line prints the LATE count.",
 owner="Claude2.",
 decided=None,
 sources=[("r3f_root_items", "M-15"), ("cx1_prov1", "logical-controls table"), ("cx1_prov2", "focused results"), ("cx1_0120", "root-choices line"), ("c4_0125", "TXT-7; FB-3")])

item(group=G7, key="m11", step="6", blocks="BEFORE_FIRST_RESULT", blocks_step="5", phase=8,
 title="M-11: the E1(b) baryonic-Newtonian carrier",
 blocks_note="Ruled with the seal." + PEND,
 raised_by=["r3 M-11", "Claude3 0088 missing item 4", "Codex3 0618 (E1b UNAVAILABLE)"],
 issue="FORMAL: no target-free Newtonian reference producer exists; the inspected r007 producers emit none, and the extractor marks E1b UNAVAILABLE without one (0618). A15 E1's own deciding observable is reported in E1(a).",
 options=["(a) Report E1(b) as NOT_AVAILABLE.", "(b) Commission a target-free carrier, pinned before the freeze."],
 recommendation="(a), unless root wants (b) and an owner can build it in time.",
 reasoning="E1(b) is a comparison only and would be new computation on the step-6 path; E1(a) needs no new input.",
 owner="Claude2.",
 decided=None,
 sources=[("r3f_root_items", "M-11"), ("c3_s2", "missing item 4"), ("cx3_carr_report", "E1b row")])

item(group=G7, key="m13", step="6", blocks="BEFORE_FIRST_RESULT", blocks_step="5", phase=8,
 title="M-13: the T120L C3 record for the P8 report",
 blocks_note="Pinned in the seal entry." + PEND,
 raised_by=["r3 M-13", "Claude3 0088 missing item 5", "Codex3 0618 (P8 UNAVAILABLE)"],
 issue="FORMAL: if P8 holds, the report shows the in-use grid's C3 record beside ORIGINAL_K's twin classification. Round 1 named the A17 tier-1 C3 record, which belongs to grids not in use. The extractor carries the pair but reads UNAVAILABLE_NO_REGISTERED_AGREEMENT_PREDICATE (0618), and Claude3 asks for an agreement predicate. FORMAL (CARRIER_CONTRACT_CX3V001): the carrier contract's role for this record is A17_C3 (schema UNT_ROOT_A17_C3_REGISTRATION_CX3V001, 'Root-selected A17 radial-derivative k-grid fidelity record'), and Codex3 0618, its READINESS_DELTA ('M13 root-pinned A17 C3 record') and Claude3 0088 missing item 5 ('the A17-C3 record selection') also name an A17 C3 record, while r3 M-13 names A27's T120L C3 record.",
 options=["(a) Root names A27's T120L C3 record by path and sha in the seal entry, with no agreement predicate (a consistency disclosure only); without a pinned record that half reads NOT_AVAILABLE.", "(b) Also register an agreement predicate before the freeze."],
 recommendation="(a). The seal entry also states that the carrier contract's A17_C3 role carries A27's T120L C3 record, or root names a carrier-contract successor whose role matches ({ref:carriers}).",
 reasoning="The report never changes the headline or any status, so a predicate would add a threshold with no reading to serve. A record chosen after targets are opened could be chosen selectively, so it is pinned at the seal.",
 owner="Claude2.",
 decided=None,
 sources=[("r3f_root_items", "M-13"), ("c3_s2", "missing item 5"), ("cx3_carr_report", "P8/C3 row"), ("cx3_carr_contract", "optional_root_contracts.A17_C3"), ("cx3_carr_delta", "current_remaining_before_launch_or_freeze (M13)")])

item(group=G7, key="m8", step="6", blocks="BEFORE_FIRST_RESULT", blocks_step="5", phase=8,
 title="M-8: scoring a FREEZE_INCOMPLETE manifest",
 blocks_note="Fixed at the seal." + PEND,
 raised_by=["r3 M-8", "Claude3 0088 missing item 12"],
 issue="FORMAL: if the freeze ends FREEZE_INCOMPLETE, may it be scored? v003g needs allow_incomplete (Claude3 S2 N9).",
 options=["(a) Fix it at the seal: scored and classified in full, with every pattern, reading and zone summary, the E3 line and DT-S0G labelled PROVISIONAL (FREEZE_INCOMPLETE) with the incomplete_reasons; a different rule only if recorded before any step-5 output value is read.", "(b) Decide when it happens."],
 recommendation="(a).",
 reasoning="(b) decides at a moment when the predictions are readable.",
 owner="Claude2.",
 decided=None,
 sources=[("r3f_root_items", "M-8"), ("c3_s2", "missing item 12; N9")])

item(group=G7, key="m1", step="6", blocks="BEFORE_FIRST_RESULT", blocks_step="5", phase=8,
 title="M-1: tiers, and the NEAR flag",
 blocks_note="Ruled with the seal." + PEND,
 raised_by=["r3 M-1"],
 issue="FORMAL (r3): the tiers INVALID_AS_MISS, HIT and MISS come from frozen LADDER fields; NEAR is a flag on a MISS row whose valid envelope row meets the error bar, and it changes no count; it reads NOT_AVAILABLE where the envelope row is invalid.",
 options=["(a') NEAR as a flag (r3).", "(a) NEAR as a fourth tier (V001).", "(b) A sigma-multiple band.", "(c) No NEAR.", "(d) A member-level flag."],
 recommendation="(a').",
 reasoning="(a) was lenient and its gloss false (round 1); (b) adds a free number; (d) is sound if root prefers a member-level meaning, and it changes no count.",
 owner="Claude2.",
 decided=None,
 sources=[("r3f_root_items", "M-1")])

item(group=G7, key="m2", step="6", blocks="BEFORE_FIRST_RESULT", blocks_step="5", phase=8,
 title="M-2: zone cuts and membership",
 blocks_note="Ruled with the seal." + PEND,
 raised_by=["r3 M-2", "Claude3 0088 missing item 10"],
 issue="FORMAL: cuts at 10.0 and 30.0 kpc from A15's wording, and membership by id: INNER Q01-Q24, TRANSITION Q25-Q35, OUTER Q36-Q43. OUTER equals the STAGE0 scope, and E1b's INNER set depends on the table (Claude3 S2 N8).",
 options=["(a) Adopt the cuts and the id table.", "(b) A disc-scale cut."],
 recommendation="(a).",
 reasoning="The cuts are A15's own words, and fixing membership by id removes any argument about Q25 (10.04 kpc) and Q36 (30.08 kpc); (b) adds a stellar-model parameter.",
 owner="Claude2.",
 decided=None,
 sources=[("r3f_root_items", "M-2"), ("c3_s2", "missing item 10; N8")])

item(group=G7, key="m4", step="6", blocks="BEFORE_FIRST_RESULT", blocks_step="5", phase=8,
 title="M-4: deciding tests NOT SCHEDULED, the status tuple, and the deficit-type sign rule",
 blocks_note="Ruled with the seal." + PEND,
 raised_by=["r3 M-4"],
 issue="FORMAL (r3): DT-UT1, DT-BHD, DT-U12 and DT-TSR are registered NOT SCHEDULED; every reading is reported as a status tuple; and the A10 rule (with MINORITY_MISS), the A15 E3 rule and the deficit-type sign rule decide which readings are triggered and how.",
 options=["(i) R-UT1 and R-REACH are deficit-type; R-HIST, R-MF and R-DRIFT are sign-free.", "(ii) All five are sign-free."],
 recommendation="(i).",
 reasoning="R-UT1 and R-REACH explain missing long-range attraction, which can only lower the outer rotation, so calling them CONSISTENT with an outer excess would add an explanation their mechanism cannot give (the A48 principle). They stay reported and OPEN, as A15 E3 requires.",
 owner="Claude2.",
 decided=None,
 sources=[("r3f_root_items", "M-4")])

item(group=G7, key="m5", step="6", blocks="BEFORE_FIRST_RESULT", blocks_step="5", phase=8,
 title="M-5: score inputs and field names",
 blocks_note="Ruled with the seal." + PEND,
 raised_by=["r3 M-5"],
 issue="FORMAL (r3): the classification binds to freeze v003g (48a1e48a) and slots V003 (d3859b42), with the listed fields and carriers; a missing named field is a stop condition.",
 options=["(a) Bind as listed; any successor adopted before the freeze carries a reviewed field map.", "(b) Leave the field names to the classifier."],
 recommendation="(a).",
 reasoning="v003g is the reviewed freeze of record (Claude4 0071 PASS; A70).",
 owner="Claude2.",
 decided=None,
 sources=[("r3f_root_items", "M-5")])

item(group=G7, key="m6rest", step="6", blocks="BEFORE_FIRST_RESULT", blocks_step="5", phase=8,
 title="M-6: cited entries and the V005 and V006 entry tables",
 blocks_note="Ruled with the seal." + PEND,
 raised_by=["r3 M-6, items 2-5", "Claude4 0125 (FB-3)"],
 issue="FORMAL (r3): the seal check confirms the section sha of every cited V005 entry; every other V005 heading, and every V006 heading written before the seal entry, has a hand-written NO_CHANGE row read from the bytes; the frozen V005 sha is compared at the seal; and the check's currency verdict is read from its JSON. FORMAL (INDEX_R3; Claude4 0125, FB-3): r3 is current at V006 43d4562b, whose table holds its 6 headings; every new or edited V006 heading before the seal entry needs a row and a re-render, hence a new candidate post, and the seal entry and later entries lie outside the table. TESTED here: V006 is now b22bd18a, with A112 as a seventh heading, which the re-render must add.",
 options=["(a) Adopt it as r3 writes it.", "(b) Presence checks only."],
 recommendation="(a). Root appends V006 entries at the end only, and batches those it writes before the seal ({ref:sealcand}).",
 reasoning="Rounds 1 and 2 showed that presence alone attests nothing and that in-place edits went unseen; this is the A81 RI-26, A82 and A99 pattern.",
 owner="Claude2.",
 decided="V005 closed with A106 (c01b3c51), and later rulings go in V006 (A82; A106.3).",
 sources=[("r3f_root_items", "M-6, items 2-5"), ("r3f_index", "'V006 at assembly'"), ("c4_0125", "FB-3"), ("v006", "headings"), ("v005", "A81 RI-26; A82; A106.3")])

item(group=G7, key="m9", step="6", blocks="BEFORE_FIRST_RESULT", blocks_step="5", phase=8,
 title="M-9: the DT-S0G comparison rule",
 blocks_note="Ruled with the seal." + PEND,
 raised_by=["r3 M-9"],
 issue="FORMAL (r3): on the OUTER rows valid under both members, CONSISTENT if H_S > H_P; AGAINST if H_S <= H_P and the twin's median |r| is at least the reference member's; NOT_DECIDED otherwise. It never makes R-DRIFT supported.",
 options=["(a) As r3 writes it.", "(b) Round 1's sign-class rule."],
 recommendation="(a).",
 reasoning="It uses counts and medians only, with no new tolerance; (b) read AGAINST for a twin that shrank every residual.",
 owner="Claude2.",
 decided=None,
 sources=[("r3f_root_items", "M-9")])

item(group=G7, key="m10", step="6", blocks="BEFORE_FIRST_RESULT", blocks_step="5", phase=8,
 title="M-10: the twin rule for alternatives",
 blocks_note="Ruled with the seal." + PEND,
 raised_by=["r3 M-10"],
 issue="FORMAL (r3): the twin is the alternative's member with the reference member's log_index; TWIN_INVALID and TWIN_INPUT_DEFECT are defined; alternatives get no NEAR and no TSR flags.",
 options=["(a) As r3 writes it.", "(b) Score alternatives by envelope."],
 recommendation="(a).",
 reasoning="v003g guarantees that the twin exists; an alternative's NEAR would need a band step the freeze does not perform, and the N-tests ran on the PRIMARY operator.",
 owner="Claude2.",
 decided=None,
 sources=[("r3f_root_items", "M-10")])

# ---------------------------------------------------------------- ids and refs
ids = {}
n = 0
for it in ITEMS:
    if it.get("fixed_id"):
        ids[it["key"]] = it["fixed_id"]
    else:
        n += 1
        ids[it["key"]] = "RI45-%02d" % n
REF = re.compile(r"\{ref:([a-z0-9_]+)\}")
def resolve(s):
    def f(m):
        k = m.group(1)
        if k not in ids:
            raise SystemExit("UNRESOLVED_REF " + k)
        return ids[k]
    return REF.sub(f, s)

errs = []
seen = set()
for it in ITEMS:
    i = ids[it["key"]]
    if i in seen:
        errs.append("DUP_ID " + i)
    seen.add(i)
    for f in ("group", "key", "step", "blocks", "blocks_step", "phase", "title", "blocks_note", "raised_by", "issue", "options", "recommendation", "reasoning", "owner", "sources"):
        if f not in it:
            errs.append("MISSING %s %s" % (f, i))
    if it["blocks"] not in BLOCKS:
        errs.append("BAD_BLOCKS " + i)
    for (sk, sec) in it["sources"]:
        if sk not in SOURCES:
            errs.append("BAD_SOURCE %s %s" % (sk, i))
if errs:
    print("REFUSED:", errs)
    sys.exit(3)

def rendered(it):
    out = {}
    for k, v in it.items():
        if isinstance(v, str):
            out[k] = resolve(v)
        elif isinstance(v, list):
            out[k] = [resolve(x) if isinstance(x, str) else x for x in v]
        else:
            out[k] = v
    return out

R = [rendered(it) for it in ITEMS]
BYKEY = {it["key"]: r for it, r in zip(ITEMS, R)}

# ---------------------------------------------------------------- source maps per group (dedup)
def I(k):
    return ids[k]

MAPS = {
 "G1": [
  ("H1_SCIENTIFIC_PRODUCER", "OPEN", I("exporter")),
  ("H2_NATIVE_COORDINATES", "OPEN_BLOCKS_CURRENT_NATIVE_HANDOFF", I("coords")),
  ("H3_PUBLICATION_TIMING", "WAIT_FOR_FULL_STEP4_DECISION", I("timing") + " (timing); " + I("exporter") + " (complete-roster custody)"),
  ("H4_POST_S1", "EXISTING_REQUIREMENT_OPEN", I("s1") + " (= step-4 R-C6)"),
  ("H5_V007_NATIVE_CUSTODY", "OPEN", I("v007rec") + "; native custody and the guarded plan/admission hashes in " + I("exporter")),
  ("H6_CERTIFICATE_SCOPE", "OPEN", I("certscope") + " (scope); " + I("content") + " (content)"),
  ("H7_DRIVER_CONSUMER_SELECTION", "V002: OPEN_IF_SUCCESSOR_SELECTED; V003: OPEN_CURRENT_DRIVER_SELECTION_AND_POLICY_RECONCILIATION", I("driver") + " (driver DECIDED by A93 and A103; successors open)"),
  ("H8_PUBLICATION_AND_REVIEW", "V002: PENDING_EXTERNAL_REVIEW; V003: EXTERNAL_REVIEW_RECEIVED_PRODUCTION_CONTRACT_AND_CLOSURE_OPEN", I("authority")),
  ("0074 blocker (1): the authentic exporter and its distinct-reviewed verifier", "production blocker", I("exporter")),
  ("0074 blocker (2): the native three-u point against the selected four-u consumer", "production blocker", I("coords")),
  ("0074 blocker (3): the sealed V007 adoption, the complete native decision and custody, post-state acceptance, and NGC point EPS/LO evidence", "production blocker", I("v007rec") + " (adoption); " + I("exporter") + " (decision, custody, post-state acceptance); " + I("certscope") + " (NGC point certificates)"),
  ("0074 blocker (4): the existing S4-POST-S1, root contract adoption, the selected driver bindings", "production blocker", I("s1") + "; " + I("contract") + "; " + I("driver")),
 ],
 "G2": [
  ("R1 V007 adoption, admitted points, native custody, export", "UNRESOLVED_EXTERNAL_ADMISSION", I("exporter") + "; " + I("v007rec")),
  ("R2 adopt the handoff/export contract", "ROOT_CONTRACT_ADOPTION_REQUIRED", I("contract")),
  ("R3 r006 fallback until r007 is accepted", "REGISTERED_FALLBACK_AVAILABLE", "DECIDED: A93 (r007 accepted, r006 retired) and A103 (cx3r008 replaces r007); the stale wording is in " + I("driver")),
  ("R4 bind the available NGC records", "RECORDS_AVAILABLE_ROOT_BINDING_REQUIRED", I("certscope") + "; " + I("registry")),
  ("R5 keep K32 / M_s 96", "CURRENT_K32_NTEST_RECORDS_AVAILABLE", "DECIDED: A64.2 (K_big 32), A81 RI-23 (M_s 96; GQ_NGC_91_MS96 PASS), A90; see " + I("certscope")),
  ("R6 run-produced inputs per point", "RUN_PRODUCED_INPUTS", I("custody")),
  ("R7 resources and timing", "RESOURCE_AND_TIMING_UNKNOWN", I("interface")),
  ("R8 freeze input completeness", "FREEZE_INPUT_COMPLETENESS", I("freezeinputs") + "; " + I("origk")),
  ("R9 optional STAGE0 adoption", "OPTIONAL_STAGE0_ADOPTION", I("stage0")),
  ("R10 A89 no-delay rule for r6", "A89_NO_DELAY", "DECIDED: A89 and A96 (V007 on r5); the residual is " + I("r6")),
  ("R11 A90 iteration-0 I1T and the star-transform convergence", "A90_PRELAUNCH_ROOT_RULING_REQUIRED", "DECIDED: A101 (Codex1 0066, TESTED PASS); per-point I1-T is part of " + I("certscope")),
  ("R12 A66 radial-support mapping", "A66_DISCLOSURE_MAPPING_UNRESOLVED", I("tsr")),
  ("0618: TSR, E1b and P8 carriers; carrier registration", "REQUIRED_FROM_ROOT", I("tsr") + "; " + I("m11") + "; " + I("m13") + "; " + I("carriers")),
  ("0618: ST7-SF1, ST7-SF2, PAR-TB-1 before step 5", "prelaunch", "ST7-SF1 and ST7-SF2 closed (TESTED, Claude4 0104; cx3r008 accepted, A103); PAR-TB-1 is " + I("partb")),
  ("0618: complete six-alternative and raw result, cut and gate registrations", "remaining", I("freezeinputs")),
  ("0618 rough edges: the STAGE0 successor; M6/M12 adoption; the I6 wording; a refused geometry sensitivity", "not changed", I("stage0") + "; " + I("sealcand") + " and " + I("m12") + "; the I6 wording is fixed in the r3 text (0091, as 0618 reports); a refused geometry sensitivity stays INVALID, never zero-width, and " + I("custody") + " keeps every INVALID record"),
 ],
 "G3": [
  ("SF1 protected-path fences are lexical (filler, extractor)", "SHOULD_FIX", I("fence")),
  ("SF2 safe_path resolves before it refuses", "SHOULD_FIX", I("fence")),
  ("SF3 the A93 retirement of r006 is not propagated; no policy accepts cx3r008", "SHOULD_FIX", I("driver")),
  ("SF4 untyped tracebacks (digits, nesting, invalid bytes)", "SHOULD_FIX", I("fence")),
  ("SF5 the ORIGINAL_K join is incomplete", "SHOULD_FIX", I("origk")),
  ("SF6 carried payloads get no target-field screen", "SHOULD_FIX", I("content")),
  ("SF7 ROOT_ITEMS_CX3V002 is stale (15 items missing)", "SHOULD_FIX", I("rilist")),
  ("SF8 the filler has no output confinement", "SHOULD_FIX", I("fence")),
  ("Missing 1: A93 pre-step-5 fixes and the driver-sha check", "missing", I("partb") + "; ST7-SF1 and ST7-SF2 closed (Claude4 0104); the sha check is DECIDED (A77.1 N8; A93), applied in " + I("driver")),
  ("Missing 2: r007 or cx3r008, with matching successors", "missing", "Driver DECIDED (A103); successors in " + I("driver")),
  ("Missing 3: stale R3", "missing", "DECIDED (A93; A103)"),
  ("Missing 4: M-11, the E1b Newtonian carrier", "missing", I("m11")),
  ("Missing 5: M-13, the C3 pairing and an agreement predicate", "missing", I("m13")),
  ("Missing 6: adopt CARRIER_CONTRACT_CX3V001", "missing", I("carriers")),
  ("Missing 7: the freeze vehicle for carriers and the TSR flag record", "missing", I("carriers") + "; " + I("tsr")),
  ("Missing 8: point_key derivation and binding", "missing", I("pointkey")),
  ("Missing 9: the ORIGINAL_K pair at spec level", "missing", I("origk")),
  ("Missing 10: M-2 zone-table adoption", "missing", I("m2")),
  ("Missing 11: M-6, M-12 and prereg r3 with the I6 wording", "missing", I("sealcand") + "; " + I("m12") + "; " + I("m6rest") + "; the I6 wording is fixed in the r3 text (ROOT_ITEMS_R3, 0606 coverage table)"),
  ("Missing 12: M-8, the FREEZE_INCOMPLETE policy", "missing", I("m8")),
  ("Missing 13: the K32 N-test reading at the step-4 points", "missing", I("certscope")),
  ("Missing 14: the TSR support coordinate frame", "missing", I("tsr")),
  ("Missing 15: the optional B-only replay successor", "missing", I("bonly")),
 ],
 "G4": [
  ("SF1 the path fence is lexical and narrow", "SHOULD_FIX (writer v008)", I("fence") + "; writer v010 addresses it within its tested scope (Codex1 0104), and Claude3's delta review of v010 is pending"),
  ("SF2 the content screen is a key-name deny-list", "SHOULD_FIX", I("content") + " (OPEN)"),
  ("SF3 v007_adoption_pin is the verdict VIEW", "SHOULD_FIX", I("v007rec") + " (OPEN)"),
  ("SF4 WAIT_FOR_FULL_STEP4_DECISION is enforced by labels only", "SHOULD_FIX", I("exporter") + " (OPEN)"),
  ("SF5 no output confinement", "SHOULD_FIX", I("fence") + "; addressed in writer v010, Claude3's delta pending"),
  ("SF6 RecursionError escapes main()", "SHOULD_FIX", I("fence") + "; addressed in writer v010, Claude3's delta pending"),
  ("NOTE CX-SF1: the digest publisher is root", "NOTE", I("authority")),
  ("NOTE CX-SF2 and ADM-SF1: self-describing V007 views", "NOTE", I("v007rec")),
  ("NOTE CX-SF3: the coordinate mode is indistinguishable", "NOTE", I("coords")),
  ("NOTE CX-SF4 and ADM-N8: r006_fallback still accepted", "NOTE", I("driver")),
  ("NOTE CX-N1: no ADMITTED handoff without point-bound NGC certificates", "NOTE", I("certscope")),
  ("NOTE CX-N2: root keeps the WRITER_RECEIPT", "NOTE", I("authority")),
  ("NOTE CX-N4: raw compare and addendum slots are unscreened", "NOTE", I("content")),
  ("NOTE CX-N3 and ADM-N4: untyped API errors on long integers", "NOTE", I("fence") + " (the bounded integer parse)"),
  ("NOTE ADM-N6: no issuance registry", "NOTE", I("authority") + " (the per-handoff V006 entries)"),
  ("NOTE ADM-N7: the export lists one point under admitted_points", "NOTE", I("exporter") + "; " + I("contract") + " (every admitted point)"),
 ],
 "G5": [
  ("ST7-SF1 duplicate readiness report", "CLOSED (TESTED)", "DECIDED: cx3r008 accepted (A103)"),
  ("ST7-SF2 strict cut, GL and manifest records", "CLOSED (TESTED)", "DECIDED: cx3r008 accepted (A103)"),
  ("PAR8-SF1 = PT8-SF1 (PAR-TB-1 partly closed)", "SHOULD_FIX", I("partb") + " (must close before step 5)"),
  ("ST8-N2 inside-NGC strictness changes", "NOTE", I("st8n2")),
  ("ST8-N1, N3, N4, N5; PAR8-N1 to N5", "NOTE", I("notes0104")),
  ("PAR8-N6 the dry-harness guard", "NOTE", I("fence") + " (the module covers any dry harness root uses for the per-point dry plans of " + I("registry") + ")"),
 ],
}

# ---------------------------------------------------------------- step-4 index (by reference)
S4 = [
 ("R-A1", "AT_T0", "BLOCKS_START", "in full: S4-R-A1"),
 ("R-A2", "AT_T0", "BEFORE_FIRST_RESULT", "Seal tuple into APPROVED_V007_SEALS; gates numerics_verdict, hence the campaign, not the direct runs. No active builder (Codex2 out, A103)."),
 ("R-A3", "BEFORE_SEAL", "BLOCKS_START", "in full: S4-R-A3"),
 ("R-A4", "AFTER_HEADLINE", "BEFORE_FIRST_RESULT", "C4-6 adoption derivation, from the headline receipts; gates adoption_regeneration, hence campaign wave 1. Its target-free generator is written and reviewed before H3 (the record's disposition: 'write and review a target-free generator now'); the record names no builder."),
 ("R-A5", "AFTER_HEADLINE", "BEFORE_FIRST_RESULT", "Caps and the orphan wait regenerated from the measured C4T use; gates adoption_regeneration."),
 ("R-A6", "BEFORE_SEAL", "BEFORE_FIRST_RESULT", "Finite carried uncertainty in the ADOPT_TAIL report; gates numerics_verdict for the campaign only, so it can land in the R-B3 policy successor."),
 ("R-B1", "CLOSED_BY_RULING", "DECIDED", "Driver r5 for step 4 (A96)."),
 ("R-B2", "BEFORE_SENS", "LATER", "Deciding-(iii) comparator successor on c2v007r2. No active builder (A103)."),
 ("R-B3", "BEFORE_SEAL", "BEFORE_FIRST_RESULT", "One v006r10 cascade with a single delta review; gates the campaign. No active builder (A103)."),
 ("R-B4", "BEFORE_SEAL", "BEFORE_FIRST_RESULT", "Split here. Its prelaunch-check part is S4-R-B4a, in full (`BLOCKS_START`). This row, S4-R-B4b, is the campaign's own launch entry (run, resolve, reingest, status) and admission path, ruled in a V006 entry under 0620; until then the campaign waits. The record names no builder ('any lane')."),
 ("R-B5", "BEFORE_CAMPAIGN", "BEFORE_FIRST_RESULT", "Post-state certificate loop per campaign call (unestimated compute). No active operator (A103)."),
 ("R-B6", "BEFORE_HEADLINE", "BLOCKS_START", "in full: S4-R-B6"),
 ("R-C1", "BEFORE_HEADLINE", "BLOCKS_START", "in full: S4-R-C1"),
 ("R-C2", "AFTER_HEADLINE", "BEFORE_FIRST_RESULT", "u_i carrier declaration; gates u_i_carrier, hence the campaign."),
 ("R-C3", "BEFORE_CAMPAIGN", "BEFORE_FIRST_RESULT", "Tail-ON failure taxonomy and its judgment calls."),
 ("R-C4", "BEFORE_CAMPAIGN", "BEFORE_FIRST_RESULT", "MODEL_INVALID for tail-ON."),
 ("R-C5", "BEFORE_SENS", "LATER", "Distinct review per D of the deciding-(iii) evidence."),
 ("R-C6", "BEFORE_CAMPAIGN", "BEFORE_FIRST_RESULT", "S4-POST-S1 registration: see " + I("s1") + "."),
 ("R-C7", "BEFORE_SENS", "LATER", "Purpose, reading and schedule of the 18 sensitivity runs."),
 ("R-C8", "BEFORE_CAMPAIGN", "BEFORE_FIRST_RESULT", "Registry growth for campaign points; without it the campaign stops after its pre-registered points. No active builder (A103)."),
 ("R-D1", "BEFORE_HEADLINE", "BLOCKS_START", "in full: S4-R-D1"),
 ("R-D2", "BEFORE_HEADLINE", "BLOCKS_START", "in full: S4-R-D2"),
 ("R-D3", "AFTER_HEADLINE", "BEFORE_FIRST_RESULT", "Headline capability runs and evidence; gates driver_capability and adoption_regeneration."),
 ("R-D4", "AFTER_HEADLINE", "BEFORE_FIRST_RESULT", "deciding_test document and config.anchor; gates deciding_test and numerics_verdict."),
 ("R-D5", "BEFORE_HEADLINE", "BLOCKS_START", "in full: S4-R-D5"),
 ("R-D6", "BEFORE_SENS", "LATER", "Sensitivity launch conditions."),
 ("R-D7", "BEFORE_CAMPAIGN", "BEFORE_FIRST_RESULT", "Campaign scheduling (max_concurrent 6 recommended; UNTESTED model)."),
 ("R-D8", "BEFORE_HEADLINE", "BLOCKS_START", "in full: S4-R-D8"),
 ("R-D9", "BEFORE_HEADLINE", "BLOCKS_START", "in full: S4-R-D9"),
 ("R-D10", "BEFORE_CAMPAIGN", "BEFORE_FIRST_RESULT", "Engine seed computed afresh; its registry entry is part of S4-R-C1."),
 ("R-D11", "BEFORE_HEADLINE", "BLOCKS_START", "in full: S4-R-D11"),
 ("R-D12", "BEFORE_CAMPAIGN", "BEFORE_FIRST_RESULT", "Coordinate-spec preconditions still OPEN (PC-1, PC-5, PC-7, PC-9, D3)."),
 ("R-D13", "AFTER_CAMPAIGN", "LATER", "ORIGINAL_K evaluation: see " + I("origk") + "."),
 ("R-D14", "BEFORE_SEAL", "DECIDED", "V006 holds every later ruling and V005 is never written again (A82; A106.3; V006 opened 23:56Z). Residual: record the step-4 rulings in V006."),
 ("R-D15", "BEFORE_CAMPAIGN", "BEFORE_FIRST_RESULT", "One machine-wide schedule across launchers; also " + I("interface") + "."),
 ("R-D16", "BEFORE_CAMPAIGN", "BEFORE_FIRST_RESULT", "Per-D sensitivity registration in a sibling config, never edited mid-campaign."),
 ("R-D17", "BEFORE_HEADLINE", "BLOCKS_START", "in full: S4-R-D17"),
]
assert len(S4) == 37, len(S4)

RULINGS = [
 ("A60", "v005", "Gap rows INVALID (QUERY_OUTSIDE_RETAINED_SUPPORT) and the cut binding", [I("custody")]),
 ("A62", "v005", "Freeze procedure two-pass (F5)", [I("custody"), I("freezeinputs")]),
 ("A64.2", "v005", "NGC production K_big 32 after the formal N3", ["Codex3 R5", I("certscope")]),
 ("A65", "v005", "STAGE0_GRID_OUTER registered; after the headline; never delays it; NOT_EVALUATED fallback", [I("stage0")]),
 ("A66", "v005", "N_FAIL_N1 confined to TRUNCATION_SHAPE rings does not block route A/B; rows flagged as a disclosure", [I("tsr"), I("certscope")]),
 ("A77.1 (N8)", "v005", "Root verifies the full driver sha before each NGC launch and checks the result's driver_sha256", [I("driver"), I("registry")]),
 ("A81 RI-23", "v005", "NGC gas M_s 96 unless GQ_NGC at M_s 96 fails on [2,91]", ["Codex3 R5", I("certscope")]),
 ("A82; A106.3", "v005", "V005 closed; every later root ruling goes in V006", ["step-4 R-D14", I("sealcand"), I("m6rest")]),
 ("A89; A96", "v005", "V007 seals on r5; r6 deferred; caching for steps 4-5 decided later", ["Codex3 R10", "step-4 R-B1", I("r6")]),
 ("A90", "v005", "NGC K32 N-tests complete: N_FAIL_N1, gate OPEN under A66", [I("certscope")]),
 ("A93", "v005", "cx3r007 accepted; the r006 registry retired; driver sha checked before every NGC launch", ["Codex3 R3", I("driver")]),
 ("A98.1", "v005", "PAR-TB accepted narrowly; any r008-specific frame class pinned before closure", [I("partb")]),
 ("A98.2", "v005", "Miss-reading prereg r3 ordered", [I("sealcand")]),
 ("A101", "v005", "The A90 step-5 open item closed (star-transform convergence TESTED PASS)", ["Codex3 R11", I("certscope")]),
 ("A103", "v005", "Codex2 out; queue reassigned; cx3r008 accepted as the step-5 driver; registry pinned before step 5", [I("driver"), I("partb"), I("registry")]),
 ("A105.3", "v005", "Step-2 outputs stay on the internal SSD (about 250 GB expected; an 80 GB watchdog)", ["S4-R-D17"]),
 ("A107.1", "v006", "EPS_NGC and I1T_NGC are step-5 NGC certificates the seal carries", [I("certscope")]),
 ("A108", "v006", "Root proceeds from the seal to the step-2 launch", ["S4-R-A3"]),
 ("A111 P4", "v006", "The NGC certificate slots: EPS_NGC 1d5eef1b and I1T_NGC 3ae7981a, excluded from C-04", [I("certscope")]),
 ("A109", "v006", "Stalled work is reassigned automatically (owner fallbacks)", ["owners throughout"]),
 ("0620 (dispatch)", "d0620", "Step 4 launches only through the guarded packet, with the sealed ADOPT_TAIL, the step-4 admission, the PRELAUNCH, certificate and sensitivity checks and the r5 allowlist enforced before any process; no fallback", ["S4-R-B6", "S4-R-B4a", "S4-R-B7"]),
 ("0636 (dispatch)", "d0636", "Further fix rounds are built by a Claude lane or Codex1, not Codex3", ["owners throughout"]),
]

OWNER_SHORT = {
 "exporter": "Codex1 builds; Claude3 reviews", "coords": "Codex1 builds; Claude3 reviews", "timing": "Claude2",
 "s1": "Claude2; Codex1 template; Claude3 review", "v007rec": "Claude2 names it; Codex1 binds; Claude3 reviews",
 "certscope": "Claude2 rules; Claude3 or Claude4 builds; Codex1 reviews", "content": "Codex1 builds; Claude3 reviews",
 "driver": "Codex1 builds; Claude3 reviews; Claude2 pins", "authority": "Claude2", "contract": "Claude2",
 "custody": "Claude2", "interface": "Claude2 (names the memory model first)", "registry": "Claude2 (root launch)",
 "freezeinputs": "Codex1 or Claude3 builds; Claude4 reviews", "origk": "Claude2 rules; Codex1 builds the join",
 "stage0": "Codex1 or Claude3 builds; Claude4 reviews", "r6": "Claude2", "tsr": "Claude2 adopts; Claude4 supplies",
 "carriers": "Claude2 adopts; Codex1 builds; Claude3 reviews", "fence": "Codex1 builds; Claude3 reviews",
 "rilist": "Claude2", "pointkey": "Codex1 builds; Claude3 reviews", "bonly": "Claude2",
 "partb": "Claude2 (one V006 entry)", "st8n2": "Claude2 (one V006 entry)", "notes0104": "Claude2",
 "s4a3": "Claude2 at seal assembly", "s4b6": "Codex1 builds; Claude3 reviews; Claude2 admits",
 "s4b4a": "Builder unassigned (Codex1 recommended); Claude3 reviews; Claude2 runs it",
 "s4c1": "Claude2; LO successor Claude4 or Claude3; Codex1 reviews", "s4d1": "Claude2", "s4d2": "Claude2",
 "s4d5": "Claude2", "s4d8": "Claude2", "s4d9": "Claude2", "s4d11": "Claude2",
 "s4d17": "Claude2; Codex1 implements the disk guard; Claude3 reviews",
 "s4a1": "Claude2; Claude4 specs (producer v003); Claude3 delta check",
 "s4b7": "Claude4 drafts; Claude3 reviews; Claude2 authorizes",
 "sealcand": "Claude4 re-renders and posts; Codex1 delta; Claude2 seals", "m12": "Claude4 (A); Codex1 (B); Claude2 go-ahead and pins",
 "mr3p1": "Claude4 re-renders; Codex1 verifies", "mr3p2": "Claude2 adopts with the seal (closed, Codex1 0120)",
 "m3": "Claude2", "m15": "Claude2", "m11": "Claude2", "m13": "Claude2", "m8": "Claude2", "m1": "Claude2",
 "m2": "Claude2", "m4": "Claude2", "m5": "Claude2", "m6rest": "Claude2", "m9": "Claude2", "m10": "Claude2",
}
missing_short = [it["key"] for it in ITEMS if it["key"] not in OWNER_SHORT]
if missing_short:
    raise SystemExit("OWNER_SHORT_MISSING " + ",".join(missing_short))
S4_OWNER = {"R-A2": "Claude2; builder unassigned (A103)", "R-B3": "Claude2; builder unassigned (A103)",
            "R-B5": "Claude2; operator unassigned (A103)", "R-C8": "Claude2; builder unassigned (A103)",
            "R-C6": "Claude2 (see RI45-04)", "R-B4": "Claude2 (V006 ruling under 0620); entry builder unassigned ('any lane')",
            "R-A4": "Claude2 + distinct reviewer; generator builder unnamed", "R-A5": "Claude2 (record)",
            "R-C2": "Claude2 (record)", "R-D3": "Claude2 (root-only launch)", "R-D4": "Claude2 (record)"}
# SF-2: the five AFTER_HEADLINE items close at H3, from the headline receipts, before campaign wave 1
S4_PHASE = {"R-A4": 5, "R-A5": 5, "R-C2": 5, "R-D3": 5, "R-D4": 5}
# SF-1: the by-reference R-B4 row is the campaign part; its prelaunch part is S4-R-B4a, in full
S4_SUMMARY_ID = {"R-B4": "S4-R-B4b"}
S4_SUMMARY_TITLE = {
 "R-B4": "The campaign's own launch entry and admission path (the campaign part of R-B4), ruled in a V006 entry under 0620; until then the campaign waits. No builder named ('any lane').",
 "R-A4": "C4-6 adoption derivation from the headline receipts; gates adoption_regeneration. Its generator is written and reviewed before H3.",
}

PHASES = {
 1: "Now, at the seal (A108 step 1)",
 2: "During step 2, before T0",
 3: "At T0 (sealed ADOPT_TAIL), before HEADLINE11",
 4: "Before campaign wave 1 (by the end of HEADLINE11)",
 5: "At H3, from the headline receipts, before campaign wave 1",
 6: "During the campaign, before the first real handoff",
 7: "After FINAL_SUMMARY, before each point's NGC launch",
 8: "Before any step-5 output value is read",
 9: "Step 6, before the freeze",
 10: "Later (not a blocker)",
}

# ---------------------------------------------------------------- render markdown
def sp(k):
    p, s, vol, name, note = SOURCES[k]
    return name, s

def src_line(srcs):
    parts = []
    for (k, sec) in srcs:
        name, s = sp(k)
        parts.append("%s (`%s`) %s" % (name, s[:8], sec))
    return " · ".join(parts)

L = []
w = L.append
w("# ROOT_ITEMS_STEP45_V002: recommended root rulings for steps 4, 4->5, 5 and 6")
w("")
w("**Who and when.** A helper of lane Claude4 (coordinator Claude2), built %s (`date -u`). Fix stage of dispatch 0637 (`%s`). It corrects ROOT_ITEMS_STEP45_V001 (md `%s`, json `%s`, both unchanged) for the refuter's 8 SHOULD_FIX findings (REFUTE_ROOT_ITEMS_STEP45.md, `%s`), and it brings in the state that landed after V001 was built. Each change, and the reason for it, is in FIXLOG_V002.md in this folder; the short list is the section after the flags." % (STAMP, SOURCES["d0637"][1], SOURCES["v001_md"][1][:8], SOURCES["v001_json"][1][:8], SOURCES["refute"][1][:8]))
w("")
w("**Authority.** Root (Claude2) alone rules and launches. **Every recommended ruling below is a RECOMMENDATION** for root to approve or adjust during step 2. Nothing here launches, schedules or authorizes a run, and nothing here was adopted by writing it.")
w("")
w("**Labels.** TESTED = recomputed from bytes in this session, or by the named lane with its own test. FORMAL = read from a ruling, message, record or code, with the source named. UNTESTED = projections, models and future behaviour. RECOMMENDATION = a proposal for root.")
w("")
w("**Blocks legend.** `BLOCKS_START` = must close before the step's first launch, or the step starts late. `BEFORE_FIRST_RESULT` = the step can launch, but this must close before its first result is read or used (for step 4: before campaign wave 1; for step 5: before anyone reads a step-5 output value). `LATER` = can close later without delaying anything. `DECIDED` = a ruling already settled it (the entry is cited).")
w("")
w("**How to read it.** Each unique item has one id (RI45-nn, or S4-R-xx for the step-4 items listed in full). Items that two sources raise appear once; each group starts with a map from that source's own ids to the ids here. The summary table of every blocker, in launch order, is section 9; the flags below and section 9 are the short version.")
w("")
w("## Flags for root")
w("")
w("1. **Step 4 (T0 is about one step-2 run away; step 2 is projected at 10-16 h, UNTESTED, A89).** Twelve items block the start. Two have no assigned builder: S4-R-C1 (the LO producer successor and the certificate production were Codex2's, out of usage, A103, and no dispatch through 0648 reassigns them) and S4-R-B4a (the one-call PRELAUNCH tool that HEADLINE11's admission needs; the record says 'builder any lane'; Codex1 is recommended). S4-R-B6 still needs G7-SCOPE-1 from Codex1 and Claude3's review. S4-R-A1: Claude3's review of producer 8e835ce3 is done (0105: 0 BLOCKING, 7 SHOULD_FIX, PR-SF1 an escalation candidate), and T0 uses producer v003, in build (Claude4 0119), once Claude3's delta check finds PR-SF1 closed. S4-R-A3 closes at the seal. The other seven are rulings root can record in V006 now: S4-R-D1, D2, D5, D8 (RSS 29 GiB, and the route-A cap read at H1 from the C4T record), D9, D11 and D17 (External1, with Codex1 implementing the disk guard). The ROOT_ITEMS_FINAL_C4V005 candidate is built but not yet reviewed or published; once published it supersedes V004. It adds R-B7 (the DIII tail_off_policy, S4-R-B7 here, LATER for the start) and R-D18 (the route-A cap, which it defaults to 3, where S4-R-D8 here defaults to keeping 25% free). Five campaign gates close at H3 from the headline receipts, before wave 1 (section 9).")
w("2. **Step 5.** Four things do not exist yet: the native exporter (%s), the NGC per-point certificate producer (%s), consumer successors that accept the native three-u point and cx3r008 (%s, %s, in one round with %s), and a registered S4-POST-S1 (%s). There is also no NGC K_big 32 memory model for the first point's caps (%s). Step 5 follows step 4's FULL_FINAL_DECISION, so there are days of runway, but each needs an assigned builder and reviewer now. The complete freeze-input list (%s) is due before the first step-5 output value is read." % (I("exporter"), I("certscope"), I("coords"), I("driver"), I("fence"), I("s1"), I("interface"), I("freezeinputs")))
w("3. **Claude4 0104 (cx3r008).** Only PAR8-SF1 must close before step 5 (%s). The recommended close is one V006 entry that quotes the class verbatim and is pinned by its section sha; the review's own fix, a disposition successor, also closes it. ST8-N2 should be recorded as intended before the first step-5 result (%s). No other finding needs action." % (I("partb"), I("st8n2")))
w("4. **Step 6.** The final r3 exists (PREREG b0fba984, unsealed; TESTED), and Claude4 0124 is its first SEAL CANDIDATE post ('classifier: none'). Codex1's delta is in: PASS with 0 blocking (0119), CX1-MR3-P2 closed and CX1-MR3-P1 carried as one SHOULD_FIX (0120). Still open: CX1-MR3-P1, still at line 598 of the final text (TESTED), which Claude4 0125 fixes in one re-render with a new SEAL CANDIDATE (%s); the M-12 classifier pair, not built (%s); root's rulings on M-1 to M-15, with M-3 and M-15 the two choices that neither review adopts (%s, %s); and the seal (%s). Every V006 heading written before the miss-reading seal entry forces another re-render, so root should batch its V006 entries and append them at the end (FB-3); A112, added to V006 at 02:42Z, is already one more row for the re-render (TESTED)." % (I("mr3p1"), I("m12"), I("m3"), I("m15"), I("sealcand")))
w("5. **Already decided, not re-opened here:** the step-5 driver cx3r008 (A103); the A90 star-transform item (A101); NGC K_big 32 and M_s 96 (A64.2; A81 RI-23); r5 for step 4 (A96); V006 as the vehicle for every later ruling (A82; A106.3).")
w("6. **Owners.** Codex2 is out of usage (A103); Codex3 is in reserve and builds no fix rounds (0636; 0638). Every build here is recommended to Codex1, Claude3 or Claude4, each with a reviewer from another lane, and A109 reassigns any stalled work.")
w("")
CHANGES = [
 ("SF-1", "R-B4 is split. Its prelaunch-check part is a new start blocker listed in full (S4-R-B4a: the one-call PRELAUNCH tool, with no builder assigned; Codex1 recommended, Claude3 reviewing). Its campaign entry stays `BEFORE_FIRST_RESULT` (S4-R-B4b). Step 4 has 12 start items.", "flags 1; group 6; section 9"),
 ("SF-2", "R-A4, R-A5, R-C2, R-D3 and R-D4 gate campaign wave 1, so they are `BEFORE_FIRST_RESULT` (step 4), in a new section-9 block, 'At H3, from the headline receipts, before campaign wave 1'. R-A4's generator is built and reviewed before H3.", "group 6 table; section 9"),
 ("SF-3", "S4-R-A1 is current: Claude3's producer review is done (0105, 0 BLOCKING, 7 SHOULD_FIX), and T0 uses producer v003 after Claude3's delta check with PR-SF1 closed (root may escalate PR-SF1). New S4-R-B7 (the DIII tail_off_policy, `LATER`). S4-R-D17 names its disk-guard implementer and folds in A105.3. ROOT_ITEMS_FINAL_C4V005, now built as a candidate, is noted as V004's coming successor, and its R-B7, R-D17 and R-D18 are compared with the items here.", "flags 1; group 6"),
 ("SF-4", "RI45-01 (a) adds the guarded plan and admission provenance, post-state acceptance (step-4 R-B5) and point-scoped certificate validity, with MUST_FAIL controls for a missing or refused post-state acceptance and for a plan or admission hash mismatch. The group-1 map carries Codex1 0074's four production blockers.", "RI45-01; group-1 map"),
 ("SF-5", "S4-R-D8's route-A cap rule reads the C4T after-route-A RSS first and has a branch for each outcome: cap 2 up to an increment of 1.80 GiB; above it (or with no RSS record) cap 1, or a recorded acceptance of a dip; cap 3 only if root accepts the modelled 17.1% dip. Both departures from the record's defaults (28 GiB; cap 3) are stated.", "S4-R-D8"),
 ("SF-6", "RI45-14 is `BEFORE_FIRST_RESULT` (step 5) and still blocks step 6; its section-9 row moves to the step-5 read block, and its successor drops the stale r006 first_pass input.", "RI45-14; section 9"),
 ("SF-7", "RI45-20's JSON rule has no text fallback: a JSONDecodeError is a typed refusal, integers go through a bounded parse inside the duplicate-refusing hook, non-finite values refuse, and nesting depth is capped. A71 and A102 are cited for the principle only.", "RI45-20"),
 ("SF-8", "RI45-12 names the memory model behind the first NGC point's caps: either a commissioned target-free K32/T120L estimate, or an explicit first-point cap with stated headroom, labelled UNTESTED, run solo under monitoring with no automatic retry.", "RI45-12"),
 ("State (N-1)", "Step 6 moved after V001 was built: the final r3, SEAL CANDIDATE 0124, the build post 0125 and Codex1's delta (0119, 0120), and V006 gained A112. RI45-27 to RI45-30 are updated, RI45-29's fix now needs a re-render, RI45-30 is closed, the 'pending' marks are gone, RI45-16 notes that 0124 names no STAGE0 successor, and the V006/re-render interaction (FB-3) is carried in RI45-27, RI45-32 and RI45-40.", "flags 4; group 7; RI45-16; section 8"),
 ("NOTEs", "The refuter's notes N-2 to N-13 were each checked against the source bytes, and all are applied as small wording changes (FIXLOG_V002.md gives each one's reason). N-5 also re-flags RI45-27 and RI45-28 as `BEFORE_FIRST_RESULT` (step 5), matching RI45-14.", "RI45-06, 08, 09, 10, 11, 15, 20, 24, 27, 28, 31, 34; S4-R-D11; the maps of groups 1, 2, 4 and 5"),
]
w("## Changes from V001")
w("")
w("| finding | change | where |")
w("|---|---|---|")
for (a, b, c) in CHANGES:
    w("| %s | %s | %s |" % (a, b, c))
w("")

GROUP_TITLES = {
 "G1": ("1. Codex1 0074 and 0104: the step-4 -> step-5 handoff root items (H1-H8)", ["cx1_0074", "cx1_0104", "cx1_ri_v002", "cx1_ri_v003", "cx1_contract", "cx1_rules", "cx1_semantic", "cx1_build1", "cx1_build2"]),
 "G2": ("2. Codex3 0614 and 0618: the step-5 readiness root items", ["cx3_0614", "cx3_0618", "cx3_ri_v002", "cx3_ri_v001", "cx3_report", "cx3_contract", "cx3_freeze_inputs", "cx3_order", "cx3_carr_report", "cx3_carr_decision", "cx3_carr_delta", "cx3_resource_plan"]),
 "G3": ("3. Claude3 0088: the step-5 readiness review (8 SHOULD_FIX, 15 missing ROOT_ITEMS)", ["c3_0088", "c3_review5", "c3_s2"]),
 "G4": ("4. Claude3 0094: the step-4 -> step-5 handoff review (6 SHOULD_FIX)", ["c3_0094", "c3_review4"]),
 "G5": ("5. Claude4 0104: the cx3r008 delta, and what must close before step 5", ["c4_0104", "c4_r8review"]),
 "G6": ("6. Step 4: Claude4's readiness package, by reference", ["c4_index", "c4_ri_v004", "c4_order_v002", "c3_0105", "c3_review_s4v2", "c4_0119", "cx1_iface3", "cx1_guard7"]),
 "G7": ("7. Step 6: the miss-reading prereg r3 (final r3 and Codex1's delta landed; what is still open)", ["r3f_prereg", "r3f_root_items", "r3f_index", "r3f_checks", "c4_0124", "c4_0125", "cx1_0119", "cx1_0120", "cx1_r3delta", "cx1_0080", "cx1_0082", "cx1_prov1", "cx1_prov2", "r3_text", "r3_fixlog"]),
}

def render_item(r):
    i = ids[r["key"]]
    w("### %s. %s" % (i, r["title"]))
    w("")
    w("- **Step:** %s. **Blocks:** `%s` (step %s). %s" % (r["step"], r["blocks"], r["blocks_step"], r["blocks_note"]))
    w("- **Owner:** %s" % r["owner"])
    w("- **Raised by:** %s." % "; ".join(r["raised_by"]))
    w("- **Issue.** %s" % r["issue"])
    w("- **Options.**")
    for o in r["options"]:
        w("  - %s" % o)
    w("- **Recommended ruling (RECOMMENDATION).** %s" % r["recommendation"])
    w("- **Reasoning.** %s" % r["reasoning"])
    w("- **DECIDED:** %s" % (r["decided"] if r.get("decided") else "no ruling settles it."))
    w("- **Source:** %s." % src_line(r["sources"]))
    w("")

def render_map(g, head):
    w("| %s | status there | here |" % head)
    w("|---|---|---|")
    for (a, b, c) in MAPS[g]:
        w("| %s | %s | %s |" % (a, b, c))
    w("")

for g in ("G1", "G2", "G3", "G4", "G5", "G6", "G7"):
    title, sk = GROUP_TITLES[g]
    w("## " + title)
    w("")
    w("Sources: " + "; ".join("%s (`%s`)" % (SOURCES[k][3], SOURCES[k][1][:8]) for k in sk) + ".")
    w("")
    if g == "G1":
        w("Codex1 0074 cites ROOT_ITEMS_CX1V002 (8 items) and lists four production blockers. Codex1 0104 publishes the successor text ROOT_ITEMS_CX1V003 (same 8 ids, stricter wording, Claude3 0094 bound in) and writer v010, which addresses 0094 SF1, SF5 and SF6 within its tested scope; SF2, SF3 and SF4 stay OPEN (FORMAL, 0104). Both versions are mapped below; where their statuses differ, both are shown (TESTED, from the two JSON files).")
        w("")
        render_map(g, "Codex1 id")
    elif g == "G2":
        w("ROOT_ITEMS_CX3V002 (R1-R12) was written at 18:56Z, before A93, the 0606 carriers and A103 (FORMAL; Claude3 0088 SF7). The 0618 delta adds carrier and pre-launch items. The superseded ROOT_ITEMS_CX3V001 (`%s`) adds no item: 8 of its 10 records are identical to V002's, and its R4 and R5 are earlier wordings that V002 updates with the A90 evidence (TESTED here, record by record)." % SOURCES["cx3_ri_v001"][1][:8])
        w("")
        render_map(g, "Codex3 item")
    elif g == "G3":
        w("Claude3 rated every finding SHOULD_FIX refute-by-default and offered SF1 for escalation if a fence gap alone counts as a target read path; because both tools open only root-pinned files, this list keeps it SHOULD_FIX and folds it into one start-blocking build (RECOMMENDATION).")
        w("")
        render_map(g, "Claude3 0088 item")
    elif g == "G4":
        w("Every 0094 finding is a writer-side finding already carried by a group-1 or group-3 item, so this group adds no new id. Codex1 0104 reports v010 for SF1, SF5 and SF6, and Claude3's delta review of v010 is pending (FORMAL); closure is part of %s's review." % I("fence"))
        w("")
        render_map(g, "Claude3 0094 item")
    elif g == "G5":
        w("**Must any finding close before step 5?** Yes, one: **PAR8-SF1** (%s). A98.1 and dispatch 0619 require every r008-specific frame class to be pinned before closure, and this class is not pinned. It is documentary, with no code, driver-sha or registry change: the recommended close is one V006 entry that quotes the class verbatim and is pinned by its section sha, and the review's own fix, a disposition successor, would also close it. **ST8-N2** should be recorded as intended before the first step-5 result (%s). **Nothing else** needs action before step 5 (%s). A103 accepted cx3r008 with 0 blocking findings, and ST7-SF1 and ST7-SF2 are closed (TESTED, Claude4 0104)." % (I("partb"), I("st8n2"), I("notes0104")))
        w("")
        render_map(g, "Claude4 0104 finding")
    elif g == "G6":
        w("ROOT_ITEMS_FINAL_C4V004 holds 37 items; it is included here by reference. Its successor ROOT_ITEMS_FINAL_C4V005 (Claude4 0119) now exists as a build-stage candidate in `v003_work/order/` (md `%s`, written 02:25:14Z; TESTED, ls and sha256 at 02:50Z), not yet reviewed or published: launch_order/ holds no V005 file, and the V003 work log reads 'BUILD stage complete; nothing published or launched' at 02:39:38Z (FORMAL). Once published it supersedes V004. It keeps the 37 V004 ids, changes R-A1, R-A2, R-D14 and R-D17, and adds R-B7 (the DIII tail_off_policy) and R-D18 (the route-A cap) (FORMAL, its header). The 12 items that block step 4 from starting on time are listed in full below: the record's 11 that close by BEFORE_SEAL, BEFORE_HEADLINE or AT_T0 on the headline's launch path, and the prelaunch-check part of R-B4 (S4-R-B4a), split from its campaign entry (S4-R-B4b, by reference). S4-R-B7, the DIII tail_off_policy, is listed in full as well, because V004 does not carry it; it is `LATER`. The campaign prerequisites are `BEFORE_FIRST_RESULT` for step 4: they gate campaign wave 1, which follows HEADLINE11 (about 7.52 h E / 16.11 h U, UNTESTED) and H3. Five of them (R-A4, R-A5, R-C2, R-D3, R-D4) close at H3 from the headline receipts. Their dispositions stay as the record recommends." % SOURCES["c4_v005_md"][1][:8])
        w("")
        w("| id | close by (record) | blocks here | note |")
        w("|---|---|---|---|")
        for (a, b, c, d) in S4:
            w("| %s | %s | `%s` | %s |" % (a, b, c, d))
        w("")
        w("**No active builder after A103 (FORMAL):** R-A2, R-B2, R-B3, R-B5 and R-C8, plus R-C1's producer runs and LO successor (S4-R-C1). **Never assigned in the record (FORMAL):** R-B4's builds ('builder any lane': the PRELAUNCH tool S4-R-B4a and the campaign entry S4-R-B4b) and R-A4's generator (owner 'Claude2 + distinct reviewer'). The builds that block the start are R-C1's and S4-R-B4a's; the others gate the campaign, so they should be assigned within one headline batch of T0, and R-A4's generator in time for its review before H3 (RECOMMENDATION).")
        w("")
    elif g == "G7":
        w("**Status.** TESTED (ls and sha256 at 02:13Z): the final r3 folder `miss_reading_prereg_c4/r3/` exists (born 01:56:31Z), with PREREG `%s` (the text, unsealed, as INDEX_R3 says), ROOT_ITEMS_R3 `%s` (byte-equal to the draft that V001 read, so the M-items below carry over), INDEX_R3 `%s` and HASHES_R3 `%s`; its checks/ folder (02:07:41Z) adds a closure table and a pattern suite of the r3 rules (all_ok true, FORMAL from INDEX_CHECKS_R3). The fix stage ended 'Stage done' at 01:42:42Z (r3 fixlog). FORMAL: Claude4 0124 (02:16:45Z) is the first SEAL CANDIDATE post (that text and ROOT_ITEMS, 'classifier: none', no STAGE0 successor), and Claude4 0125 (02:19:34Z) reports the build and plans one re-render for CX1-MR3-P1. Codex1's A98.2 delta (0119, 02:18:51Z; record `%s`) reads PASS with 0 blocking in its scope, and 0120 (02:20:47Z) closes CX1-MR3-P2 and carries CX1-MR3-P1 as one SHOULD_FIX; M-12 agreement, the root choices M-3 and M-15, and actual seal readiness stay UNTESTED or pending. V001 marked this group pending the final r3 and Codex1's delta; both have landed, and **the items below are what is still open for step 6.** M-7 is %s and M-14 is %s." % (SOURCES["r3f_prereg"][1][:8], SOURCES["r3f_root_items"][1][:8], SOURCES["r3f_index"][1][:8], SOURCES["r3f_hashes"][1][:8], SOURCES["cx1_r3delta"][1][:8], I("tsr"), I("stage0")))
        w("")
    for r in R:
        if r["group"] == g:
            render_item(r)

w("## 8. Rulings applied (DECIDED, or deciding in part)")
w("")
w("V006 is open. It was read at 00:55Z (`7af42209`, A107-A109) and again at 01:33Z (`43d4562b`, adding A110, A111 and an 'A108 continued' heading). At the fix stage it changed once more: at 02:42:32Z (file time) it became `b22bd18a`, which is `43d4562b` plus one inserted section, A112 (seal tool 4 v004 SELECTED; the disclosures file V002; the R-02 check), placed before the 'A108 continued' heading (TESTED, diff of the byte copies). At this build it re-hashes to `%s`. All three byte copies are in this folder. A112 is a seal-path ruling and decides no step-4, step-5 or step-6 root item (FORMAL). A107-A111 are seal-path rulings (seal script, proceeding to the step-2 launch, stall reassignment, manual disclosures in the SEAL_RECORD, the driver check record and the NGC certificate slots). They decide no step-4, step-5 or step-6 root item beyond A107.1 and A111 P4 (NGC certificate carriage and slots), A108 (the seal steps) and A109 (the reassignment rule) (FORMAL). A105.3 is added in V002, because S4-R-D17 now folds it in." % REHASH["v006"])
w("")
w("| entry | file | what it settles | used in |")
w("|---|---|---|---|")
for (e, f, what, used) in RULINGS:
    w("| %s | %s (`%s`) | %s | %s |" % (e, SOURCES[f][3], SOURCES[f][1][:8], what, ", ".join(used)))
w("")

# ---------------------------------------------------------------- summary table in launch order
rows = []
for it, r in zip(ITEMS, R):
    if r["blocks"] in ("BLOCKS_START", "BEFORE_FIRST_RESULT"):
        rows.append((r["phase"], ITEMS.index(it), ids[r["key"]], dict(r, owner_short=OWNER_SHORT[r["key"]])))
for j, (a, b, c, d) in enumerate(S4):
    if c == "BEFORE_FIRST_RESULT":
        rows.append((S4_PHASE.get(a, 4), 1000 + j, S4_SUMMARY_ID.get(a, "S4-" + a), {"step": "4", "blocks": c, "title": S4_SUMMARY_TITLE.get(a, d), "owner": "Claude2, per ROOT_ITEMS_FINAL_C4V004", "owner_short": S4_OWNER.get(a, "Claude2 (record)"), "blocks_step": "4", "decided": None}))
rows.sort(key=lambda x: (x[0], x[1]))
rows = [(ph, i, r) for (ph, _o, i, r) in rows]
w("## 9. Summary: every blocker, in launch order")
w("")
w("Rows are ordered by the milestone each must close by, then by id. `LATER` and `DECIDED` items are left out. The step-4 rows marked by reference keep the record's disposition. S4-R-B4b is the campaign part of R-B4; its prelaunch part is S4-R-B4a.")
w("")
w("| # | must close by | id | step | blocks | item | owner |")
w("|---|---|---|---|---|---|---|")
SUMMARY = []
for k, (ph, i, r) in enumerate(rows, 1):
    t = r["title"]
    w("| %d | %s | %s | %s | `%s` (step %s) | %s | %s |" % (k, PHASES[ph], i, r["step"], r["blocks"], r["blocks_step"], t, r["owner_short"]))
    SUMMARY.append({"order": k, "must_close_by": PHASES[ph], "phase": ph, "id": i, "step": r["step"], "blocks": r["blocks"], "blocks_step": r["blocks_step"], "item": t, "owner": r["owner_short"]})
w("")

R3_FINAL = CA + "/miss_reading_prereg_c4/r3"
R3_EXISTS = os.path.isdir(R3_FINAL)
w("## 10. Sources (sha256 from bytes), conduct and limits")
w("")
w("Every source below was re-hashed from bytes by the builder at %s; a non-volatile mismatch would have refused the build. Volatile sources (open or in-progress files) are recorded as read and as now." % STAMP)
w("")
w("Paths are shortened: `UNT_EXCHANGE/` is `/Users/bgm/Research/UNT_EXCHANGE/` and `UNT_PROGRAM_CONTROL/` is `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/`; the JSON twin carries full paths.")
w("")
w("| source | path | sha256 as read | now | note |")
w("|---|---|---|---|---|")
for k, (p, s, vol, name, note) in SOURCES.items():
    now = REHASH[k]
    sp_ = p.replace("/Users/bgm/Research/UNT_EXCHANGE/", "UNT_EXCHANGE/").replace("/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/", "UNT_PROGRAM_CONTROL/")
    w("| %s | `%s` | `%s` | %s | %s |" % (name, sp_, s, "same" if now == s else ("`%s` (changed; volatile)" % now), note))
w("")
w("At build time the final r3 folder `%s` exists: **%s** (TESTED, isdir)." % (R3_FINAL, R3_EXISTS))
w("")
w("**Conduct.**")
w("- No launch; no driver, orchestrator, writer, filler, extractor, producer, guard, launcher, binder or compare was imported or run. No NGC3198 target or observed-velocity file, rotmod, Vobs, MassModels or SPARC file was opened. Nothing under runs_ext, KMAX_A2F10_C5H_RUN_V001 or any UVT_* path was read, listed or stat'ed. No network, delete, move or overwrite.")
w("- Reads, build stage (V001): the named sources above, in full where cited (FINDINGS_S1, POLICY_CX3V001, STEP5_REGISTRY_CX3V002, dispatch 0616 and Claude4 0115 hashed only). The V005 and V006 decisions files carry NGC3198 in their names; they are rulings, not target data. One grep over five named r3 work files and one over two named r3 PREREG files (no recursive search), sed reads of two sections of the r3 draft text, a tail of the r3 fixlog, and ls of named folders only. A strict-JSON read of the r6 SELECTED and r6 text files (case_block entries only). `df -k` on the internal volume and External1 (metadata).")
w("- Reads, fix stage (V002): the refuter's report and each source added above, by name. Strict-JSON reads (stdlib) of ROOT_ITEMS_CX1V002 and V003, ROOT_ITEMS_CX3V001 and V002, CARRIER_CONTRACT_CX3V001 (its A17_C3 role), READINESS_DELTA_CX3V001, FREEZE_EXPECTED_INPUTS_CX3V002 and Codex1's r3 delta record. Reads of named sections: guard007 L187-275; the V005 entries A55, A61, A64, A71, A85, A90, A98, A102 and A105; r3 M-3, M-13 and M-14; the final r3 PREREG at lines 242 and 598; LAUNCH_ORDER_C4V002 sections 1-6; the step-4 record in full. Greps of named files only (the guard, launcher and binder for PRELAUNCH; Codex1 posts 0100-0120 for G7-SCOPE-1; two step-4 record files for tail_off_policy; the V005 builder header), ls of named folders, stat birth times of the r3 folder and four lane posts, and `df -k` on two volumes (metadata). The step-4 V003 work files of another Claude4 helper (the V005 builder's header, the V005 candidate's R-A1, R-B7, R-D17, R-D18 and DIII step, the work log and the run record's stage field) were read and not changed. Posts that landed during this stage and concern the seal path were checked for step-4, step-5 or step-6 effects: dispatch 0648 in full (no step-4 builder assigned), Claude4 0126 by its head, and Claude3 0111-0114 and Codex1 0121 by name.")
w("- Writes: only in `claude_artifacts/root_items_step45_c4/`, by exclusive create. Build stage: the two V006 byte copies, PARTIAL.md (created once, then appended), the V001 pair, its builder and its HASHES file. Fix stage: PARTIAL_FIX_V002.md (created once, then appended), V006_ADDENDUM_COPY_AT_FIX.md (a byte copy of V006 at b22bd18a), these two files, FIXLOG_V002.md, BUILDER_ROOT_ITEMS_STEP45_C4V002.py and HASHES_ROOT_ITEMS_STEP45_V002.txt; no V001-stage file was changed. Both builders ran in the session scratchpad with `python3 -I -B` and single-thread BLAS variables.")
w("- Disclosures. Build stage: two shell slips with no effect on any file (a zsh `echo` of a separator beginning with `=` failed with 'not found'; an awk program with an escaped quote failed with a syntax error before printing). Fix stage: the scratchpad copy of the builder was edited in place (Edit tool, and one Python patch for the phase renumbering and the r3 source keys) before it ran, and the published builder is byte-equal to the copy that ran; one shell command failed before printing (a sed range built from a grep that matched two lines), with no effect on any file.")
w("- **Limits.** The step-4 V003 build and the r3 re-render are still moving; S4-R-A1, S4-R-B7, S4-R-D8, S4-R-D17 and group 7 describe them as of this build, and ROOT_ITEMS_FINAL_C4V005, once published, supersedes the step-4 record cited here. Lane-capacity readings behind the owner recommendations are FORMAL from dispatches (A103, 0636, 0638, A109) and may be stale. No item here is TESTED end to end: the TESTED marks cover only the facts so labelled.")
w("")

MD = "\n".join(L) + "\n"

# ---------------------------------------------------------------- json
J = {
 "schema": "UNT_ROOT_ITEMS_STEP45_C4V002",
 "date_u": STAMP,
 "author": "helper of lane Claude4 (fix stage)",
 "authority": {"dispatch": "0637", "path": SOURCES["d0637"][0], "sha256": SOURCES["d0637"][1]},
 "status": "RECOMMENDATIONS_FOR_ROOT_NOT_ADOPTED",
 "launch_authorized": False,
 "supersedes": {"md": {"path": SOURCES["v001_md"][0], "sha256": SOURCES["v001_md"][1]}, "json": {"path": SOURCES["v001_json"][0], "sha256": SOURCES["v001_json"][1]}, "note": "V001 stays unchanged"},
 "fix_round": {"refute": {"path": SOURCES["refute"][0], "sha256": SOURCES["refute"][1]}, "findings_fixed": ["SF-1", "SF-2", "SF-3", "SF-4", "SF-5", "SF-6", "SF-7", "SF-8"], "fixlog": "FIXLOG_V002.md (this folder)", "changes": [{"finding": a, "change": b, "where": c} for (a, b, c) in CHANGES]},
 "labels": {"TESTED": "recomputed from bytes in this session, or by the named lane with its own test", "FORMAL": "read from a ruling, message, record or code, with the source named", "UNTESTED": "projections, models and future behaviour", "RECOMMENDATION": "a proposal for root"},
 "blocks_legend": {"BLOCKS_START": "must close before the step's first launch", "BEFORE_FIRST_RESULT": "must close before the step's first result is read or used", "LATER": "can close later without delay", "DECIDED": "a ruling already settled it"},
 "sources": [{"key": k, "path": p, "sha256_read": s, "sha256_at_build": REHASH[k], "volatile": vol, "name": name, "note": note} for k, (p, s, vol, name, note) in SOURCES.items()],
 "groups": [{"group": g, "title": GROUP_TITLES[g][0], "source_keys": GROUP_TITLES[g][1], "source_item_map": [{"source_item": a, "status_there": b, "here": c} for (a, b, c) in MAPS.get(g, [])]} for g in ("G1", "G2", "G3", "G4", "G5", "G6", "G7")],
 "items": [],
 "step4_by_reference": [{"id": a, "close_by_record": b, "blocks_here": c, "note": d} for (a, b, c, d) in S4],
 "rulings": [{"entry": e, "file_key": f, "settles": what, "used_in": used} for (e, f, what, used) in RULINGS],
 "answer_0104_before_step5": {"must_close_before_step5": [I("partb")], "record_before_first_step5_result": [I("st8n2")], "no_action_before_step5": [I("notes0104")], "basis": "A98.1 ('Any frame class specific to r008 is enumerated and pinned before closure') and dispatch 0619", "recommended_close": "one V006 entry that quotes both source lines and the caret line verbatim, states the scope and is pinned by its section sha; the review's own fix, a disposition successor of a9ae801f, also closes it"},
 "step4_start_items": [r["fixed_id"] for r in R if r.get("fixed_id") and r["blocks"] == "BLOCKS_START"],
 "summary_blockers_in_launch_order": SUMMARY,
 "r3_final_folder_exists_at_build": R3_EXISTS,
 "r3_state_at_build": {"prereg": {"path": SOURCES["r3f_prereg"][0], "sha256": SOURCES["r3f_prereg"][1], "sealed": False}, "root_items": {"path": SOURCES["r3f_root_items"][0], "sha256": SOURCES["r3f_root_items"][1]}, "first_seal_candidate": {"post": SOURCES["c4_0124"][0], "sha256": SOURCES["c4_0124"][1], "classifier": "none"}, "codex1_delta": {"0119": "PASS, 0 blocking (A98.2 scope)", "0120": "CX1-MR3-P1 OPEN SHOULD_FIX; CX1-MR3-P2 CLOSED", "record": {"path": SOURCES["cx1_r3delta"][0], "sha256": SOURCES["cx1_r3delta"][1]}}, "planned": "one re-render with the CX1-MR3-P1 fix and a new SEAL CANDIDATE post (Claude4 0125)"},
}
for it, r in zip(ITEMS, R):
    J["items"].append({
     "id": ids[r["key"]], "key": r["key"], "group": r["group"], "title": r["title"], "step": r["step"],
     "blocks": r["blocks"], "blocks_step": r["blocks_step"], "blocks_note": r["blocks_note"], "launch_phase": r["phase"], "launch_phase_name": PHASES[r["phase"]],
     "raised_by": r["raised_by"], "issue": r["issue"], "options": r["options"],
     "recommendation": {"label": "RECOMMENDATION", "text": r["recommendation"], "reasoning": r["reasoning"]},
     "owner": r["owner"], "decided": r.get("decided"),
     "sources": [{"key": k, "file": SOURCES[k][0], "sha256": SOURCES[k][1], "section": sec} for (k, sec) in r["sources"]],
    })

def strict_dump(o):
    return json.dumps(o, indent=1, ensure_ascii=False, allow_nan=False, sort_keys=False) + "\n"

JS = strict_dump(J)
# self-check: the JSON parses strictly with no duplicate keys
def hook(pairs):
    d = {}
    for k, v in pairs:
        if k in d:
            raise SystemExit("DUPKEY " + k)
        d[k] = v
    return d
json.loads(JS, object_pairs_hook=hook)
if REF.search(MD) or REF.search(JS):
    raise SystemExit("UNRESOLVED_PLACEHOLDER_IN_OUTPUT")

os.makedirs(STAGING, exist_ok=True)
for name, data in (("ROOT_ITEMS_STEP45_V002.md", MD), ("ROOT_ITEMS_STEP45_V002.json", JS)):
    with open(os.path.join(STAGING, name), "x", encoding="utf-8") as f:
        f.write(data)
    print(name, hashlib.sha256(data.encode("utf-8")).hexdigest(), len(data.encode("utf-8")))
print("items", len(ITEMS), "summary_rows", len(SUMMARY), "ids", ", ".join(ids[it["key"]] for it in ITEMS))
changed = [k for k in SOURCES if REHASH[k] != SOURCES[k][1]]
print("volatile_changed", changed)
