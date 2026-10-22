# KMAX_TAIL_PREREG_V007: final draft r5 (UNSEALED)

FINAL DRAFT r5 (NOT SEALED). Assembled by Claude4 (dispatch 0621, A99) from r4 e3b6b5b2, integrating V005 A82-A101 through the entry table entries_after_A81 (each row revised here, or no change with the reason); open addendum observed 70a48f51e20311de82a37b13bee8cf18f7eaf9adbb976d957e50c5334e7c8c7e at assembly. Written before any V007 (tail-corrected) result exists; nothing was launched; C5H, UVT_* and targets were not read. binding_inputs.case_block pins CASE_BLOCK_V007_C4V001 (A99.2, A101). The launch-packet BUILD of record is BUILD_V007 (94bc05a5db1e6350b246c22e850ae62d95cd05ce21cdf5b329e3edded588a0de, filled from bytes; its Claude4 delta check and Claude2 adoption are pending, A99.1). Root fills the named seal slots and seals. Open root items: ROOT_ITEMS_R5.

**Assembly:** Claude4 r5 helper, single author, UTC 2026-10-18T21:00:35Z. Base: r4 `e3b6b5b2ba265f54d15381f358913dd3ea931761aaa649c98a7583f58f1b7cf8`. Dispatch 0621 `7ab78e6a0aa4c3d11d6c4dd9887ea2fc8b65e40a84bc75de387a319534b99504`.

The full clause text is in the JSON; `CLAUSE_SOURCE_MAP_R5.md` traces every clause; `DELTA_R4_R5.md` lists every edit with its trace; `ENTRY_TABLE_R5.md` is the A99.3 table; `SEAL_CHECKLIST_R5.md` and `ROOT_ITEMS_R5.md` are the root-facing lists.

## The case block (A99.2, A101)

- `binding_inputs.case_block`: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/r5/case_block/CASE_BLOCK_V007_C4V001.json` sha256 `76309ae39f23060cc662c4e218a41e1f95c56a26992402218a6198625f85ee71`.
- binding_inputs.case_block is the V007 case block of record, CASE_BLOCK_V007_C4V001 (schema UNT_KMAX_TAIL_V007_CASE_BLOCK_C2V003; built by Claude4 under A99.2; Codex2 0507: PASS, zero findings; A101). In sealed mode the compare reads the case block only from this key (r12 cx3v002 L5706) and refuses CASE_BLOCK_ABSENT without it (rehearsal D-03, R-03). For each of the ten T-cases it registers the /numerics, whole, of the driver v010 r5 dry run of its FILLED P128/M_s 128 spec (DRY_R5_MS128_V004 ff60cd6b over SPEC_REGISTRY_R5_MS128_CX1V004 c7023846, both byte-pinned in BUILD_V005), its grid and truncation, tail and ro1_required true, drivers_allowed [v010 r5 b5cc62af] and the pinned-library uv_tail_config_sha256, which equals the driver-side normalized sha of each dry run; and C5H as the registered call 60b46130 on v009-EXT 999331af, with nothing else registered. route_a_mode is parallel8 (A47 I4; A51). key_equivalence_map is []: no /numerics key of C4T-D5 outside composite_grid_spec and uv_tail differs from the C5H reference (A48 AMB-13). It reads valid under r12's own validate_case_block, in-process, both in memory and from the written bytes, and 22 must-refuse mutations refuse (TESTED; out/CASE_BLOCK_BUILD_C4V001 bcf560de). It is target-free spec metadata. The on-disk draft CASE_BLOCK_V007_DRAFT_C2V001 (6bf4ce5a) is not a V007 input: schema C2V002, retired labels C4T-K16/C4T-K64, v010 r3 drivers, K_big 32, gas M_s 64, PENDING tail shas, and a C4T-D5 entry marked not buildable.

## The launch-packet BUILD of record (A99.1)

- BUILD_V007 `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/BUILD_V007.md` sha256 `94bc05a5db1e6350b246c22e850ae62d95cd05ce21cdf5b329e3edded588a0de` (filled from bytes; 15 supported sources verified; template 1b406591 launches the case block's ten FILLED specs; Claude4 delta check and Claude2 adoption pending).

## Seal slots (root fills at seal assembly; never guessed)

- **frozen_addendum**: value `PENDING_ROOT_AT_SEAL_ASSEMBLY`. Root exclusively creates the immutable copy at seal assembly, after the last pre-seal entry; the seal check verifies that every A-entry this text cites is present in the frozen bytes; its path and sha go to the binder and into the SEAL_RECORD. The frozen addendum must not cite the sealed prereg's sha (draft shas may be cited), or the pins would cycle (RI-27). Once the frozen copy exists, root writes nothing more to the open V005 file; every later root entry goes in a V006 addendum (A82; A99.6: the hazard is live, because the compare cites the open path).  
  *Sources: 0576; 0574; RUNBOOK_V005 step 3; A78; A81 RI-26; A82 (RI-27); A99.6*
- **driver**: value `PENDING_ROOT_AT_SEAL_ASSEMBLY`. Path and full sha from bytes at seal; the SEAL_RECORD names it; the launcher refuses a plan whose driver differs (C4-S1, guard v008 / launcher v007); every identity run and every T-run carries driver_sha256 equal to it, and no T-run starts before the seal names it (A67 N1, extended to T-runs by A81 RI-24). The driver is v010 r5 (A96).  
  *Sources: A58 RI-01; A72; A67 N1; A78; 0574; A81 RI-24; A89; A96*
- **compare**: value `PENDING_ROOT_AT_SEAL_ASSEMBLY`. The final compare round is r12 cx3v002 (4bd7b262; selected by SELECTED_R12_CX3V001 91aa9747; FIELDS_R12_CX3V002 5cc95a06, IMPL ef0db32d, HASHES 3eb2912d; frozen 19:48:42Z; A96), whose scope is exactly A91.1-A91.3 (0459, 0462's should-fix, A88 SR_K; A91.4's RI-24 cache fields are moot, A96). V007 seals on the round whose delta reviews of record, Claude3's and Codex2's, each report 0 blocking (A81 RI-20 as applied by A83, A86, A91 and A96: the r11 workflow was stopped at its freeze before its three recheck lenses ran, and the reviews of record replaced them, A83; rehearsal R-02); if a review of record reports a blocking item, the slot waits for root's ruling (a fix round, or a ruling on the item). This slot holds that round's reviewed source, with its seal-time pin constants still unset (`None`; the bytes the reviews examined), path and sha. The sealed compare (V007_PREREG_SHA256 set to the sealed prereg sha, plus PIN_ADDENDUM_V005, PIN_DRIVER_BUILD_RECORD, PIN_V010_R5_CHECK and PIN_PRODUCER_REGISTRY) is created after the sealed prereg and is named only in the SEAL_RECORD; it may differ from the reviewed source only in those pin lines (A82: RI-27 ruled as drafted in r4).  
  *Sources: A79; A80; 0582; A75; A71; A58 RI-10; A81 RI-20; A82 (RI-27); compare r10 L150-166; A83; A86; A90; A91; A96*
- **identity_comparator**: value `PENDING_ROOT_AT_SEAL_ASSEMBLY`. The c2v007-lineage round whose check of record reports 0 blocking (A81 RI-21): c2v007r2 (run_identity_compare_c2v007.py 052da0fe, A92), after Codex2's delta check 0472 (PASS_WITH_FINDINGS, 0 blocking). Codex2's cross-lineage review is the c2v007 check of record: the c2v007 own-check workflow was stopped after the build froze and its outputs are leads only (A83; rehearsal R-02). c2v007r2 requires identity_sha256 and caller.sha256 present on both sides (A91). c2v004-c2v006 are superseded and not used at the seal.  
  *Sources: A68; A70; A74; A76; A81 RI-21; A83; A91; A92*
- **identity_gate_records**: value `PENDING_ROOT_AT_SEAL_ASSEMBLY`. Only the identity-comparator slot round's outputs on the identity runs of the driver in the driver slot (Z2, Z2_OFF_RO1, B0prime_RERUN), using the A59 replace-mode tokens derived from that driver, with the raw successor-custody check; each carries driver_sha256 = the driver slot (A81 RI-21, A67 N1). A92: the c2v007r2 records R5_V001.  
  *Sources: A59; A67 N1; A72.3; A74; A76; A81 RI-21; A92; A101*
- **launch_packet**: value `PENDING_ROOT_AT_SEAL_ASSEMBLY`. BUILD_V007 (A99.1: the V006 successor that closes V6-S1 (non-finite values refuse; records serialized before one exclusive write), V6-S2 (the RUNBOOK carries A85.2-4, and the r5 template's outputs go to the internal volume, not External1 runs_ext) and V6-S3 (15 supported sources); BUILD_V005 and BUILD_V006 are superseded as the BUILD of record), with the bound plan and command that the build-only binder writes from BUILD_V007's selected r5 template, the chosen driver and the frozen addendum (exclusive create). The binder runs after the addendum is frozen and the driver is chosen, and before the SEAL_RECORD is written; the SEAL_RECORD names the bound plan and command shas; root verifies both from bytes immediately before running the command. A validate()-level template-equality check is optional and not required (A81 RI-25). The template is unbound and PENDING by design. BUILD_V007's Claude4 delta check and Claude2's adoption are pending (A99.1).  
  *Sources: A78; 0576; 0577; 0574; Claude4 0079; A81 RI-25; A87; A88; A99.1*
- **certificates**: value `PENDING_ROOT_AT_SEAL_ASSEMBLY`. Root confirms each record of record at seal assembly. Every record that depends on M_s states its M_s (source_gas_M_s; the merged DOUBLING record states ddo_gas_M_s, the A73 merged-format and FIELDS_R12 DOUBLING field; rehearsal D-01, R-13), equal to the case block's registered gas.M_s, which must be 128 for DDO; an NGC record that states an M_s states 96, the NGC gas M_s (production_tail.ngc_gas_M_s; A81 RI-23 not triggered, Codex1 0032). LO_NGC is reported only in V007: the V007 LO_NGC slot takes LO_NGC_CERT_V002 (33bc2190), the LO_NGC record of record (A87); coverage to 91 gates the NGC N-test compare (step 5), not the V007 seal (A81 RI-23). DOUBLING is one merged record, registered before the seal (A81 RI-22): DOUBLING_MERGED_C3V001 (ea48ac2b, A87). GQ's record of record is GQ_CERT_V006 (5a1b39f8, A86).  
  *Sources: A70; A67 SF2; A68; A73; A64.2; A58 RI-03; A79 NEW-67; A81 RI-22; A81 RI-23; A86; A87; A90; R-13; Codex1 0032*
- **producer_registry**: value `PENDING_ROOT_AT_SEAL_ASSEMBLY`. Root-registered producer paths and shas and the gate-record shas of record (A67 N2); the compare hashes the producer bytes, not only the claimed sha (A69.1); every replay gate record is bound to it (A62.2); SR_K is registered by its producer pins with PRODUCED_AFTER_THE_SEAL (A88). The registry carries the c2v007r2 comparator, its tokens and the R5_V001 identity records (A92), the B3, B0, B0prime_DRY and B0_FA records (Claude4 0598), the B2 record of record C3V003 (A100, A101), BUILD_V007's post-seal producers (A99.5, V6-N4) and the B0_N3, B0_RO1 and I4 records once built (their empty slots fail closed). Pinned in the compare as PIN_PRODUCER_REGISTRY (A67).  
  *Sources: A62.2; A67 N2; A67 (seal-time pins); A69.1; A88; A92; A99.5; A100; A101; Claude3 0087*
- **cache_directory_r6_only**: value `NOT_APPLICABLE_R5`. Moot for V007: V007 seals on r5 (A96), so no cache directory is created or named; A81 RI-24 and the conditional cache slot are moot. Seal tool 3 requires the string NOT_APPLICABLE_R5 under r5.  
  *Sources: A72; A81 RI-24; A96*

## Entry table A82-A101 (A99.3)

| entry | decision | section sha256 |
|---|---|---|
| A82 | revised here | `8a45e4a9378e5c51...` |
| A83 | revised here | `b2c7417ffbde8f7c...` |
| A84 | no change | `598055296c7d18d5...` |
| A85 | no change | `8be593cf6eff91d2...` |
| A86 | revised here | `b3f451697f29bbc6...` |
| A87 | revised here | `3d479167fe3049db...` |
| A88 | revised here | `216fce8735405f20...` |
| A89 | revised here | `2e7844cc5145afee...` |
| A90 | revised here | `b1fce9a94cea5217...` |
| A91 | revised here | `7eb0f0a7093a7eee...` |
| A92 | revised here | `6d671c27db121106...` |
| A93 | revised here | `9474602df90fac58...` |
| A94 | revised here | `7ea61f90cd8feb93...` |
| A95 | no change | `435403e307b70701...` |
| A96 | revised here | `fed0c12f8eab596f...` |
| A97 | revised here | `a1734bcd393e4c16...` |
| A98 | no change | `181248d91db14377...` |
| A99 | revised here | `195fe36e8abf9976...` |
| A100 | revised here | `ff872d375e55bb31...` |
| A101 | revised here | `1a8babc42526e6af...` |

## Seal record requirements

- Before the seal the compare's gate and admissibility functions run on the real input records (the C5H receipt and result if present, the identity-gate records and the RO1 replay); their output goes into the seal record (E-SEAL1). *(A46 RA13)*
- Blinding: on C5H the gate functions run only as validity/admissibility booleans and reason codes, with no row value printed or written; the seal record states that no row value was shown. Record-controlled labels are redacted in blinded modes. *(A47 I3; A54 S6)*
- The compare pins at seal: V007_PREREG_SHA256 (this text once sealed), PIN_ADDENDUM_V005 (frozen V005 sha), PIN_REVIEW_V009 = the preserved original 3bce7c02, PRODUCTION_K_BIG_A55 = 128.0; its custody pins (PIN_RO1_CUSTODY, PIN_RO1_NODES_CUSTODY, the drivers_allowed I4 set) move to r5's re-pinned shas read from r5's BUILD record, verified from bytes. These seal-time pins (with PIN_DRIVER_BUILD_RECORD, PIN_V010_R5_CHECK and PIN_PRODUCER_REGISTRY) are the only lines in which the sealed compare may differ from the reviewed source of the final round; the prereg names the reviewed source, the SEAL_RECORD names the sealed compare (A82: RI-27 ruled as drafted in r4). *(0526; A53 (REVIEW_V009); A55; A56 (A55 follow-ups 1, 3); compare r5 NEW-26; A82 (RI-27); A82 (RI-27))*
- Key-equivalence map: every key v010 adds that differs from v009 numerics appears with its absent/default value and B0 evidence. *(A48 AMB-13)*
- Order of record (0561; A81 RI-19, the erratum to A72 H-01, whose "its sha goes in the seal record" is superseded). At seal assembly root exclusively creates, in this order: (1) the frozen copy of the V005 addendum, after the last pre-seal entry (A81 RI-26), after which root writes nothing more to the open V005 file and later entries go to a V006 addendum (A82; A99.6); (2) with the driver chosen (r5, A96; no cache directory, A81 RI-24 being moot), the bound plan and command written by the build-only binder (0576; A81 RI-25); (3) the sealed prereg text, this draft with every seal slot filled; (4) the sealed compare (A82); (5) the SEAL_RECORD, naming the sealed prereg sha (the first pin), the sealed compare, the driver, the frozen addendum, the bound plan and command shas; (6) the ROOT_SEAL_ADMISSION config, pinning the SEAL_RECORD's full sha; (7) a separate SEAL_ADMISSION_RECEIPT naming both, posted in a numbered root packet. The RUNBOOK verifies the published config sha before invoking any source; records embed the config, seal and compare shas. No file is edited after it is created. Root verifies the bound plan and command shas from bytes immediately before running the command. *(0561; 0576; A72 (H-01); A78; 0580; A81 RI-19; A81 RI-24; A81 RI-25; A81 RI-26; A82; A96; A99.6)*
- RI-10's adoption rule applies to every NEW item the final compare IMPL declares (adopted as text if stricter on adoption and gap-filling, rejected if looser); the IMPL lists each one with its disposition and its MUST_FAIL tests (A75), and the seal record quotes that list. *(A58 RI-10; A81 RI-20)*
- The raw successor-custody check of the Z2 run is recorded (A59). *(A59)*
- Disclosure E5-08: C5R3 ran the C5H driver and spec except for the label and fs overrides, so the C5R3 route-A fixtures the producers were tested on are very likely equal to C5H's route-A values, E^A included; they are not row values, and A47 I3 holds. *(A62 (E5-08))*
- Seal-time pins in the compare (A82): V007_PREREG_SHA256 (the sealed prereg), PIN_ADDENDUM_V005 (the frozen copy), PIN_DRIVER_BUILD_RECORD (the r5 driver BUILD record, schema UNT_V007_SEALED_DRIVER_BUILD_C2V001, which root exclusively creates at seal assembly before the sealed compare, equal to the compare's built-in r5 set with check_record = the driver check record of record; rehearsal D-06), PIN_V010_R5_CHECK (the r5 check record; r5 per A96), PIN_PRODUCER_REGISTRY; the custody pins follow the A77.2 role table read from the driver slot. *(A67 (seal-time pins); A72; A77.2; A82; A96)*
- CASCADE_MAP_R5_ADDENDUM (the immutable inventory addendum naming the unreachable pin-only successor) exists before the seal if the driver slot is r5. *(A69)*
- The root admission config names the BUILD_V007 launcher and guard sources exactly (A78 N2: the build check is a substring match), and its producer_allowlist names exactly BUILD_V007's 15 supported sources (A99.1; V6-S3). *(A78 N2; A99.1)*
- Any A-entry after A81 that touches this text needs a successor revision or an explicit no-change note in the seal record; the seal check verifies that every A-entry this text cites is present in the frozen bytes. The entry table entries_after_A81 lists every entry from A82 to the newest at r5 generation (A101) as revised here (with its clauses) or no change (with the reason), each with its section sha256 read from bytes, and the seal record quotes it (A99.3). At the freeze each row's section is re-hashed from the frozen bytes: a row whose section differs, and any entry after A101 without a row, needs a successor revision or an explicit seal-record note (A81 RI-26). *(A81 RI-26; A99.3)*
- The seal record repeats the B2 disclosure block of the B2 record of record (A100): the raw misses against ADV's saved rows (0.082 / 0.095 on le3 / 0.108 km/s), the gas-rule attribution, readings (i) and (ii) with P16 and m0, that ADV's saved C3R3 used le4, and the limit that B2 does not prove shared physical correctness; and A101's erratum for the record's two documentation should-fix items (C3V003-RI-1 attributes GL6/0.25 to 0622 in error; "<= 3.8e-11" should read approximately 3.83e-11). *(A100; A101)*

## Clauses changed in r5

- `binding_inputs.case_block` (new pin; trace A99.2, A101, D-03, GAP-03, R-03): the compare reads the case block in sealed mode only from binding_inputs.case_block {path, sha256} (r12 L5706)
- `binding_inputs.case_block_rule` (new; trace A99.2, A101, D-03, GAP-03, R-03): what the pinned case block is and how it was built
- `binding_inputs.gate_b3_record_A87 / gate_b3_rule` (new; trace A87, GAP-02 (A87 evidence), REFUTE DONE row): A87: the B3 record of record is the FIELDS-shape JSON; the Markdown is the human report
- `binding_inputs.successors` (rewritten; trace A96, GAP-19): V007 seals on r5 (A96)
- `binding_inputs.ro1_role_table` (revised; trace A96): r6 moot (A96)
- `binding_inputs.spec_set` (extended; trace A99.1, A99.2, D-02, D-03): case block and BUILD_V007 template bound to the same ten specs
- `fixed_across_all_cases.validity_gates` (extended; trace A99.2, D-03, R-03): where V3 finds the registered case block
- `fixed_across_all_cases.production_tail.gas` (extended; trace A81 RI-23, Codex1 0032, R-08): RI-23 condition evaluated from the GQ_NGC record
- `fixed_across_all_cases.production_tail.ngc_gas_M_s` (new; trace A81 RI-23, Codex1 0032, R-08): the value the tool-3 slot ngc_gas_M_s takes, with its ruling and evidence
- `fixed_across_all_cases.production_tail.memory_guard` (revised; trace A96): r6 moot
- `fixed_across_all_cases.production_tail.tail_table_cache` (rewritten; trace A89, A96, GAP-19): A96 applied A89/A72(c): r5, no cache
- `gates_before_any_T_result.B0prime_RERUN` (revised; trace A92, A96): r5 run compared by c2v007r2; r6 moot
- `gates_before_any_T_result.Z2_OFF_RO1` (revised; trace A92, A96): r5 run compared; r6 moot
- `gates_before_any_T_result.B1_Z2` (revised; trace A92, GAP-07): the comparator of record
- `gates_before_any_T_result.B2` (extended; trace A94, A97, A100, A101, R-15, GAP-15): B2 rulings A94/A97/A100/A101
- `gates_before_any_T_result.GQ` (revised; trace A86, GAP-02 (A86 evidence)): A86.1 GQ record of record
- `gates_before_any_T_result.DOUBLING` (extended; trace A87, A73, D-01, R-13, GAP-11): DOUBLING record of record and its M_s field
- `gates_before_any_T_result.LO_NGC` (extended; trace A87, A90, GAP-12): LO_NGC records named
- `gates_before_any_T_result.after_seal_marker_policy` (rewritten; trace A88, A99.5, GAP-20): SR_K joins the after-seal set
- `tests.SR_K` (revised; trace A88, GAP-20): A88: SR_K after the seal
- `run_list.DDO_gates` (rewritten; trace A92, A96, GAP-08): r5 identity runs done and compared
- `run_list.DDO_tests` (rewritten; trace A96, A99.1, A99.2, D-02): r5 only; BUILD_V007 template
- `run_list.replays` (extended; trace A88): SR_K after the seal
- `run_list.limits` (revised; trace A99.1, D-02, GAP-09, GAP-21): BUILD of record V007
- `run_list.cpu_hours_estimate_UNTESTED` (rewritten; trace A89): measured cost
- `scope_untested` (revised; trace A89, A96, A100): cache saving measured and moot; B2 limit
- `outcome_branch_tests_required` (revised; trace A96, GAP-06): the final round named
- `not_v007_text_scope` (revised; trace A93): registry named in the scope note
- `seal_record_requirements.2` (revised; trace A82): RI-27 ruled
- `seal_record_requirements[4]` (revised; trace A82, A96, A99.6, GAP-01): no write after the freeze; r5, no cache
- `seal_record_requirements[8]` (rewritten; trace A82, A96, D-06, GAP-04): the five pins; the driver BUILD record created at assembly
- `seal_record_requirements[10]` (rewritten; trace A99.1, D-02, GAP-09, GAP-21): BUILD_V007, 15 sources
- `seal_record_requirements[11]` (rewritten; trace A99.3, D-05, GAP-02, R-02): the entry table quoted; rows re-hashed at the freeze
- `seal_record_requirements[12]` (new; trace A100, A101, R-15): B2 disclosure in the seal record
- `seal_slots.frozen_addendum` (rule extended; trace A82, A99.6, GAP-01, D-10): no write after the freeze
- `seal_slots.driver` (branch fixed; trace A96, GAP-19): r5
- `seal_slots.compare` (rule rewritten; trace A83, A86, A90, A91, A96, R-02, GAP-06): the final round r12 and its reviews of record
- `seal_slots.identity_comparator` (rule rewritten; trace A83, A91, A92, R-02, GAP-07): c2v007r2, the check of record
- `seal_slots.identity_gate_records` (candidates named; trace A92, GAP-08): R5_V001 records of record
- `seal_slots.launch_packet` (rule rewritten; build bound; trace A99.1, D-02, GAP-09, GAP-21): BUILD_V007 is the BUILD of record (filled from bytes)
- `seal_slots.certificates` (rule rewritten; candidates named; trace A86, A87, A90, A81 RI-23, D-01, R-13, GAP-11, GAP-12): records of record; M_s field names
- `seal_slots.producer_registry` (rule rewritten; candidate named; trace A87, A88, A92, A99.5, A101, GAP-13): what the registry of record carries
- `seal_slots.cache_directory_r6_only` (value fixed by A96; trace A96): NOT_APPLICABLE_R5
- `root_items.RI-27, RI-24` (resolved; trace A82, A96): RI-27 ruled; RI-24 moot
- `root_items.RI-28..RI-37` (new; trace A81 RI-20, A99.1, R-10, R-09, GAP-18, GAP-14, A99.3, D-09, GAP-05, A88): open items at r5
- `entries_after_A81` (new; trace A99.3, D-05, GAP-02, R-02): the entry-by-entry table A82-A101
- `status / assembly / decision_pins_pending_at_seal / cites_by_name` (header; trace A99, A99.3): r5 header and cited range A47-A101

## Root items

RI-27 RESOLVED (A82); RI-24 moot (A96). OPEN: RI-28, RI-29, RI-30, RI-31, RI-32, RI-33, RI-34, RI-35, RI-36, RI-37 (see `ROOT_ITEMS_R5.md`).

