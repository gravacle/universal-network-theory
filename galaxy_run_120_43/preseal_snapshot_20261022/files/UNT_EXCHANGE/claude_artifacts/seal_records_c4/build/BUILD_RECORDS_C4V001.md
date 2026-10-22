# BUILD_RECORDS_C4V001: FIELDS_R11 records for B3 and the B0 family on driver v010 r5

Claude4 helper, `seal_records_c4/build`. Assignment: dispatch 0598 (`da395935443317525ed72a42ae0cd7880897dc04fbec84e11a0429169dd33466`), root A87. UTC 2026-10-18T19:15:26Z (`date -u`).

Rules kept: no launch and no computation run; records built only from existing outputs; every value copied or derived deterministically from pinned bytes; every input sha from bytes; writes only under `build/` (and temporary copies in the session scratchpad), each file by exclusive create, except the shell-captured stdout/stderr files of E4. The audit fence (`tools/fence_c4v001.py` `f813c43099cfdadd3a779e395d223887d0df7cd8c8a8eb67b3a73de86eb699f0`, write root `build/`) was installed first in every process that read program files after the survey. Labels: TESTED (checked from bytes or by running a reader), FORMAL (follows by argument from tested facts), UNTESTED. Two rule-2 breaches during the survey (E1, E3) and two process slips (E2, E4) are in the errors register (section 9).

## 1. Result

| gate | driver | status | record (build/records) | sha256 | r11 evaluate_gate, test registry | verdict field |
|---|---|---|---|---|---|---|
| B3 | none (saved C4R3; module v001) | BUILT | `B3_RECORD_C4V001.json` | `83c853b9261c5745a6ecaa79ca23790dbc9514656c3ca788478e65269111d5ce` | **PASS**, no codes | PASS |
| B0 | v010 r5 `b5cc62af` | BUILT | `B0_R5_RECORD_C4V001.json` | `c2cec35b1821a9868816405c8442ad20c831c0b4cbb599016593959f5b450c1b` | **PASS**, no codes | PASS_PLAN_IDENTICAL |
| B0prime_DRY | v010 r5 `b5cc62af` | BUILT | `B0prime_DRY_R5_RECORD_C4V001.json` | `7842d2a77f2c1b95119392f83ef5f4ada65f8532a59b46102b7f75f4d20c1a44` | **PASS**, no codes | PASS_DRY_IDENTICAL |
| B0_FA | v010 r5 `b5cc62af` | BUILT | `B0_FA_R5_RECORD_C4V001.json` | `888488cd236fb79d4f9462a64b37e809080a0e5ec6d40b4dac63375856bd9009` | **PASS**, no codes | PASS |
| B0_N3 | v010 r5 `b5cc62af` | NOT BUILT: missing run (section 6) | none | none | not read | none |
| B0_RO1 | v010 r5 `b5cc62af` | NOT BUILT: missing run (section 6) | none | none | not read | none |
| I4 | v010 r5 `b5cc62af` | NOT BUILT: missing run (section 6) | none | none | not read | none |
| all six, r6 | v010 r6 | NOT BUILT: r6 BUILD not landed (section 7) | none | none | not read | none |

Every built record reads **PASS** through the r11 compare's own gate reader (TESTED). The four records in `records/` are byte-identical to the first and only attempt, `attempts/ATTEMPT_V001/records/` (TESTED, `cmp`); no attempt failed.

## 2. How the records were read (r11)

- **Reader:** `evaluate_gate` of `v007_compare_c2/r11/kmax_tail_compare_c2v007_r11.py` (`a5d10cb1a213931713b9712da0781042d8e02ed5c1e81cda21b97c33b0559c8a`), loaded by path after its bytes were checked (`tools/check_records_c4v001.py` `0f258d800db1428def579a24377ad153f1186c41ab1d3d2a45b259ca488da026`).
- **Test registry:** `check/TEST_REGISTRY_C4V001.json` (`556e12b1a4b6517a15d73bd33f0e7ee2fd647486107a5535c46367f5d21ddf8e`) is a copy of Claude3's `PRODUCER_REGISTRY_C3V001.json` (`94d8a52806a5b414e4bc4b37cce990a4aab8e55e995e78805daf8f4f2ac3aca5`, not edited). It changes only the slots of the four built gates: `producers[gate]` is the record's producer pin (the builder, below) and `gate_records[gate]` is the record sha from bytes. It was loaded by the compare's own `load_producer_registry`, which hashes every registered producer file. It is not a root registration.
- **ctx:** `['producer_registry']` only. B3, B0, B0prime_DRY and B0_FA read no case block, run, C5H or H-07 input (FORMAL, from the gate functions `g_B3`, `g_B0`, `g_B0prime_DRY`, `g_B0_FA` and `evaluate_gate`), so no stand-in was needed and none was used.
- **Producer of every built record:** `tools/build_records_c4v001.py` (`139da4ce56a021df44bea70856863206bd10cfd0a7a7ff322bf9d9635dd9e66c`), as for Claude3's merged DOUBLING record. B0_FA also names `numbers_producer` = the r5 B0 tool `b0_r5_vs_r4_c2v001.py` (bound by bytes in r11). B3, B0 and B0prime_DRY name no `numbers_producer`, because their numbers come from more than one tool; all tools are in `sources`.

**Controls** (expected reading stated in the checker before it ran; all met, TESTED):

| control | expected | observed |
|---|---|---|
| no registry | RECORD_DEFECT, PRODUCER_REGISTRY_ABSENT_A62_2 | B0 RECORD_DEFECT, B0_FA RECORD_DEFECT, B0prime_DRY RECORD_DEFECT, B3 RECORD_DEFECT |
| Claude3 registry unmodified | RECORD_DEFECT, producer and record sha not registered | B0 RECORD_DEFECT, B0_FA RECORD_DEFECT, B0prime_DRY RECORD_DEFECT, B3 RECORD_DEFECT |
| GATE_B3_C4_V002.md (465cb3c3) read as the B3 record | RECORD_DEFECT GATE_RECORD_UNREADABLE | RECORD_DEFECT ['GATE_RECORD_UNREADABLE:B3:JSONDecodeError'] |
| mutation B0 (`CONTROL_B0_GEO_without_2029f26a.json`) | RECORD_DEFECT naming the clause | RECORD_DEFECT ['B0_GEO_SET_LACKS_2029f26a'] |
| mutation B0_FA (`CONTROL_B0_FA_A2_code_changed.json`) | RECORD_DEFECT naming the clause | RECORD_DEFECT ['VERDICT_PASS_CONTRADICTS_DATA:B0_FA', 'B0_FA_A2_NOT_REFUSED_CHECKPOINT_MISSING'] |
| mutation B3 (`CONTROL_B3_value_rel_2e-8.json`) | RECORD_DEFECT naming the clause | RECORD_DEFECT ['VERDICT_PASS_CONTRADICTS_DATA:B3', 'B3_cube_O8_value_rel'] |

## 3. B3 (`83c853b9261c5745a6ecaa79ca23790dbc9514656c3ca788478e65269111d5ce`)

- `independent_lane` = **Claude4**: the producing lane of `B3_COMPARE_V001.json` (schema `CLAUDE4_GATE_B3_COMPARE_V001`; folder `gate_b3_c4`; V002 report header). TESTED (schema read from bytes).
- `imports_tail_library` = **false**: `not independence.pass_` of B3_COMPARE_V001 (static imports of `b3_independent_v001.py`, banned [], the one dynamic import = FORWARD). Re-read from bytes here: the recorded static-import list equals the tool's AST imports; `b3_points_v001.py` imports ['b3_independent_v001', 'math', 'numpy']; FORWARD (`galaxy_baryonic_source_forward_v002.py` `e9be043b`) imports ['bisect', 'math']. TESTED.
- `state_result_sha256` = `aac01962dc7bf08a7486179bc5674af520f7ea38d73b004154cdd2ff25fa8dee`: B3_COMPARE `state.result_sha256`; equals the r11 compare `PIN_R3` C4R3 sha (regex on the compare bytes) and `result_sha256` of the four per-case independent outputs. TESTED.

| field | FIELDS rule | cube_O8 | cylinder_O8 | source checks (file) | label |
|---|---|---|---|---|---|
| value_rel | <= 1e-8 | 4.667719575018989e-15 | 4.8646393254252625e-15 | `cube8_E1_value` (B3_COMPARE); cylinder: the cyl8 counterparts | TESTED (copied) |
| gradient_rel | <= 1e-7 | 4.693897000618109e-15 | 3.13317428035482e-15 | `cube8_E1_gradient` (B3_COMPARE); cylinder: the cyl8 counterparts | TESTED (copied) |
| hessian_rel | <= 1e-6 | 4.342117563438904e-15 | 2.31867521372247e-15 | `cube8_E1_hessian` (B3_COMPARE); cylinder: the cyl8 counterparts | TESTED (copied) |
| lapse_pair_rel | <= 1e-8 | 7.655060103031141e-15 | 5.051740837941618e-15 | `cube8_E2_b0_vs_independent_t0` (B3_COMPARE), `cube8_E2_bd_vs_independent_tz_minus_t0` (B3_COMPARE); cylinder: the cyl8 counterparts | TESTED (max of 2 copied) |
| bd_z0_max_abs | == 0 | 0.0 | 0.0 | `cube8_E3_bd_z0_exact_zero_nonzero_count` (B3_COMPARE); cylinder: the cyl8 counterparts | TESTED indicator 0; value FORMAL (implication) |
| facade_midplane_ratio_max_abs | == 0 | 0.0 | 0.0 | `cube8_E5_facade_midplane_log_ratio_exact_zero` (B3_COMPARE); cylinder: the cyl8 counterparts | TESTED indicator 0; value FORMAL (implication) |
| angular_reads_rel | <= 1e-7 | 4.02386729633e-15 | 2.8234037451539267e-15 | `REF_cube8_tap_gradient_vs_independent_over_max_grad` (B3_TAP_REF_BODY), `BODY_cube8_tap_gradient_vs_independent_over_max_grad` (B3_TAP_REF_BODY); cylinder: the cyl8 counterparts | TESTED (max of 2 copied) |
| column_potential_rel | <= 1e-7 | 1.2017407367475428e-13 | 1.1874256726846666e-13 | `FSC_cube8_col00_potential_z_module_vs_independent_over_max_tail_potential_difference` (B3_TAP_FSC), `FSC_cube8_col30_potential_z_module_vs_independent_over_max_tail_potential_difference` (B3_TAP_FSC); cylinder: the cyl8 counterparts | TESTED (max of 2 copied) |
| imag_max_abs | == 0 | 0.0 | 0.0 | `cube8_E6_imaginary_part_unchanged_bitwise_and_real_jets` (B3_COMPARE); cylinder: the cyl8 counterparts | TESTED indicator 0; value FORMAL (implication) |
| doubling_rel | <= 1e-10 | 2.9873405280121455e-15 | 1.2367576946991918e-15 | `cube8_IND_doubling_value` (B3_COMPARE), `cube8_IND_doubling_gradient` (B3_COMPARE), `cube8_IND_doubling_hessian` (B3_COMPARE); cylinder: the cyl8 counterparts | TESTED (max of 3 copied) |
| hi_v003_L67_pass | true | true | true | `HI_v003_L67_68_condition_text` (B3_COMPARE); cylinder: the cyl8 counterparts | TESTED (copied check) |

Derivations (also in the record, `provenance`):

- **value_rel**: copied
- **gradient_rel**: copied
- **hessian_rel**: copied
- **lapse_pair_rel**: max over the two lapse-pair members b0 and bd (E2), each over max|t| (GATE_B3_C4_V002 rows lapse pair b0 / bd)
- **bd_z0_max_abs**: E3 counts the module bd(z=0) entries that are not +0.0 (pd[0] != 0.0 or signbit), over 72 radii x 16 azimuths (n 1152; b3_compare_v001.py); a count of 0.0 implies max|bd(z=0)| = 0.0 exactly
- **facade_midplane_ratio_max_abs**: E5 indicator: 0.0 iff the facade midplane log ratio at z = 0 is +0.0 on every one of the 8 lines (line v002, b3_compare_v001.py); 0.0 implies max|ratio| = 0.0 exactly
- **angular_reads_rel**: max over the reference and body TailBoundary-tap grad-t reads, each over max|grad t| (registered B3 item; GATE_B3_C4_V002 bold rows); the tap t reads are reported only (below)
- **column_potential_rel**: max over the fs-column potential(z) comparisons of columns 00 and 30, each over the max tail potential difference (registered B3 item; GATE_B3_C4_V002); V001 E7 was a proxy and is not used
- **imag_max_abs**: E6 indicator: 0.0 iff the tail jets are real float64 and the line evaluation imaginary part is bitwise unchanged by the tail (b3_compare_v001.py); 0.0 implies the tail imaginary contribution is 0.0 exactly
- **doubling_rel**: max over the independent-lane doubling self-convergence of value, gradient and Hessian
- **hi_v003_L67_pass**: the single HI v003 L67-68 condition-text check (one source file, the same for both outer cases; GATE_B3_C4_V002 "(same check)"): verdict PASS, value 0.0 -> true

Source files (sha256 from bytes):

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/gate_b3_c4/out/B3_COMPARE_V001.json` `773e4ae91f2a77782590264bb7b3a34c7c37d587fbf4ffb4b9a27cfcb2c7c5ae`: E1/E2/E3/E5/E6/doubling/HI/independence/state values
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/gate_b3_c4/out/B3_TAP_COMPARE_REF_BODY_V001.json` `054710321e7a82a890dd9478684925a46a9998318df1440d3281d7eb11516f8a`: reference and body tap grad-t reads (angular_reads_rel)
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/gate_b3_c4/out/B3_TAP_COMPARE_FSC_V001.json` `45f2e99f7586bf98d9f9cd3b5cdcd22cfc5a791274bae7f10e297be0278216e8`: fs-column potential(z) columns 00 and 30 (column_potential_rel)
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/gate_b3_c4/out/B3_IND_CUBE_V001.json` `56d245e44f1d193aa8d05501e8cb25d421a1bf1de9082d0f55dc1e72e1355c90`: per-case independent output (state, script)
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/gate_b3_c4/out/B3_IND_CYL_V001.json` `49fc08dcee3a9a1ff85ddd69277e9ceab9893e96a77f3c72d23214f818cb3a0a`: per-case independent output
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/gate_b3_c4/out/B3_IND_CUBE_DOUBLE_V001.json` `07abc58789237bd39e66630e16948a2aebcdcaefb25a31bce98d77e9634478aa`: per-case doubled independent output
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/gate_b3_c4/out/B3_IND_CYL_DOUBLE_V001.json` `a0e73c4bdf9c4f4841998bbde1ac13f0d623cbe34d041b60dfc578383b6c8ba9`: per-case doubled independent output
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/gate_b3_c4/tools/b3_compare_v001.py` `2b5be52c7d148b14bdcb75f4e41a5f27585940bf67bc77f5d876203a6c6479f1`: computing tool of B3_COMPARE (checks definitions)
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/gate_b3_c4/tools/b3_tap_compare_v001.py` `b104096b6d7624d0173ae44269e73a6438d4f3945835b4a7bae6bb870a1fa547`: computing tool of the tap compares
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/gate_b3_c4/tools/b3_independent_v001.py` `7464972d249d92865b5201f39ff0e6cabaa4ff6dedd82603f1e88bd43af7ccbd`: independent lane
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/gate_b3_c4/tools/b3_points_v001.py` `bd914043e706e1579f49aee853d71231ea6847a9c9e584dd8a3da043ea0e3792`: independent lane (points)
- `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers/recovered_packet_audit/galaxy_baryonic_source_forward_v002.py` `e9be043b46790e3493f4e427fb483a98a5665f004dfac287d5758afce0ac96ad`: the one dynamic import of the independent lane
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/gate_b3_c4/GATE_B3_C4_V002.md` `465cb3c3b105c8bea994259bcf347e86910e8a9ebbc502ba83ff617fa83ceacf`: human report: item mapping
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/gate_b3_c4/GATE_B3_C4_V001.md` `a336838aa2d533c5e417f584836dd3fa1dc51fe29ffb61c932f5f55d34f81ed1`: human report V001
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r11/kmax_tail_compare_c2v007_r11.py` `a5d10cb1a213931713b9712da0781042d8e02ed5c1e81cda21b97c33b0559c8a`: PIN_R3 C4R3 sha
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r11/FIELDS_R11.md` `c7f0dec6ff1ae45dc242c69686e88ad73089a39e1b582e73650e6e18a7368cc5`: field contract

Per-case independent outputs, each carrying result_sha256 = C4R3 and script_sha256 = `b3_independent_v001.py`: `B3_IND_CUBE` 56d245e44f1d193aa8d05501e8cb25d421a1bf1de9082d0f55dc1e72e1355c90, `B3_IND_CYL` 49fc08dcee3a9a1ff85ddd69277e9ceab9893e96a77f3c72d23214f818cb3a0a, `B3_IND_CUBE_DOUBLE` 07abc58789237bd39e66630e16948a2aebcdcaefb25a31bce98d77e9634478aa, `B3_IND_CYL_DOUBLE` a0e73c4bdf9c4f4841998bbde1ac13f0d623cbe34d041b60dfc578383b6c8ba9.

## 4. B0 (`c2cec35b1821a9868816405c8442ad20c831c0b4cbb599016593959f5b450c1b`), B0prime_DRY (`7842d2a77f2c1b95119392f83ef5f4ada65f8532a59b46102b7f75f4d20c1a44`): the chain r5 == r4 == v009

**B0-EMPTY counts, verified from bytes (TESTED).** `B0_R5_VS_R4_C2V001.json` (`e10e6a584ab49083f24bf4fbb7d94a32ccb667c1c1c7e0e3ff3943ca1061f929`): 80 specs, **64 counted, 64 PASS_PLAN_IDENTICAL, fail []**, **16 no evidence**. Every counted row has r4 and r5 exit 0, both report files non-empty (also by stat of the dry directories), identical files and no `differ`. Each no-evidence row has equal non-zero exits, equal terminal lines after T and empty reports. These counts match 0598, A87 and the r5 BUILD.

No evidence (B0-EMPTY), listed separately in the record: C2R3 (r4/r5 exit 1/1), C3R3 (r4/r5 exit 1/1), C4R3 (r4/r5 exit 1/1), FA_A1_NFP_EMPTY (r4/r5 exit 1/1), FA_A2_NFP_ABSENT (r4/r5 exit 1/1), FA_A4_CONV_EMPTY (r4/r5 exit 1/1), NEG_G5_ORDERS (r4/r5 exit 1/1), NEG_G7_132 (r4/r5 exit 1/1), NEG_MAXIT_0 (r4/r5 exit 1/1), NEG_MAXIT_33 (r4/r5 exit 1/1), NEG_MAXIT_ADMIT (r4/r5 exit 1/1), NEG_MAXIT_BOOL (r4/r5 exit 1/1), R4REG_NGC3198_T120L_TAIL_ITER0_NTEST_REQUEST_C2V001.TEMPLATE (r4/r5 exit 1/1; directory not listed: name class), RR3 (r4/r5 exit 1/1), S4R3 (r4/r5 exit 1/1), Y3R3 (r4/r5 exit 1/1).

**Why a chain.** FIELDS B0 (`maps/EXT`, `maps/GEO`, `spec_sets/{EXT,GEO,NGC}`) states plan identity against v009-EXT and v009-GEO. The compare uses it for that: GEO must hold 2029f26a and 4ac5527a, a key-equivalence map needs C5H 60b46130 in a set, and a C5H R-PAIR member spec must be in EXT. The r5 run proves r5 == r4 under the cascade map only. So each set is the r4 record's set (`GATE_B0.json` `580a86e2`, evidence `B0_PLAN_IDENTITY_C2V001.json` `19625e80`), kept only where the entry is counted and PASS_PLAN_IDENTICAL at **both** links. `maps/EXT` and `maps/GEO` carry both links. Each link is TESTED by its own run; the composition is FORMAL (transitivity of plan identity under the declared maps).

**B0-EMPTY at the r4 link (applied here from bytes, TESTED).** The r4 run recorded 50 comparisons, all PASS, before the ruling. Under the r5 tool's rule (exit 0 on both sides; DRYRUN_REPORT.json and DRYRUN_PLAN.txt regular and non-empty on both sides, by stat), **32 are counted** and 18 are no evidence: the 6 R3 KMAX specs against both parents and the 6 NEG specs against EXT. This is the restatement the B0-EMPTY ruling asked for.

| set | kept (counted at both links) | excluded |
|---|---|---|
| EXT | 19: A2F10 `a93c95b9`, A2F10_RA8 `6cb822bb`, ADMIT_PREFIX_C2V005 `4ac5527a`, ADMIT_ROUTE_A_C2V005 `a0c0f2aa`, PINNED_FULL_C2V001 `9542a413`, RULE_FULL_C2V001 `c92344bf`, DEC_II_N8 `4978ba17`, NGC_A2F10_TEMPLATE `bbb37ca6`, NGC_GL10_TEMPLATE `97eee390`, NGC_SEED_ROUTE_A_CONFIG `36262801`, C5_N8 `e45d172d`, C5_N1 `8e09a167`, C6_N8 `38612080`, C6_N1 `bf3a14a0`, C5_N8_M32 `09ff5a96`, C6_N8_M32 `8f28f5b6`, C5_N1_M32 `16774734`, C6_N1_M32 `d222348b`, C5H `60b46130` | 12: C2R3, C3R3, C4R3, S4R3, RR3, Y3R3, NEG_G5_ORDERS, NEG_G7_132, NEG_MAXIT_0, NEG_MAXIT_33, NEG_MAXIT_BOOL, NEG_MAXIT_ADMIT |
| GEO | 13: A2F10 `a93c95b9`, A2F10_RA8 `6cb822bb`, ADMIT_PREFIX_C2V005 `4ac5527a`, ADMIT_ROUTE_A_C2V005 `a0c0f2aa`, PINNED_FULL_C2V001 `9542a413`, RULE_FULL_C2V001 `c92344bf`, DEC_II_N8 `4978ba17`, NGC_A2F10_TEMPLATE `bbb37ca6`, NGC_GL10_TEMPLATE `97eee390`, NGC_SEED_ROUTE_A_CONFIG `36262801`, D3p98107 `c8290f65`, D4p07 `3a8328af`, D4p11150 `2029f26a` | 6: C2R3, C3R3, C4R3, S4R3, RR3, Y3R3 |
| NGC | 3: NGC_A2F10_TEMPLATE `bbb37ca6`, NGC_GL10_TEMPLATE `97eee390`, NGC_SEED_ROUTE_A_CONFIG `36262801` | 0: none |

GEO holds D4p11150 `2029f26a` and ADMIT_PREFIX_C2V005 `4ac5527a`; EXT holds C5H `60b46130` (TESTED). The 42 counted r5 rows outside the r4 standard set (the r4 V007 registry templates, Z2, Z2_OFF_RO1 and the P = 128 specs) have no v009 counterpart; they are listed in `b0_empty.r5_link.counted` and in no set.

| B0 field | value | source | label |
|---|---|---|---|
| maps/EXT, maps/GEO | link 1: r4 record maps (pairs 48 / 2, rule text copied), parent v009-EXT `999331af` / v009-GEO `237ef3d4`; link 2: cascade map `a7281e10` (103 substitution pairs), rule = r5 BUILD.md sec 4 "Declared map" line, copied | r4 GATE_B0.json, B0_PLAN_IDENTITY_C2V001.json, B0_R5_VS_R4_C2V001.json, BUILD.md | TESTED (copied, pins checked); composition FORMAL |
| spec_sets/{EXT,GEO,NGC} | 19 / 13 / 3 entries {label, sha256} | r4 record sets, filtered by both links | TESTED |
| verdict | PASS_PLAN_IDENTICAL | r5 summary.verdict_B0 and r4 summary.verdict_B0 both PASS_PLAN_IDENTICAL, no counted fail at either link, every set non-empty | TESTED |
| driver | v010 r5 `b5cc62afb7814b4f337a012a1ffd1f1e677f398ac18a1f8297c7ff49ae5374c6` | r5 run `r5` field = bytes of the driver | TESTED |

**B0prime_DRY** (R1 L3: the same dry runs as B0, every report file compared): `files_compared` = 67 relative paths, the union of the names present in the counted report directories of both links (read by name only, never opened). Each directory pair has the same name list and the count the runs recorded (TESTED). It includes `DRYRUN_REPORT.json` and `DRYRUN_PLAN.txt`. `spec_sets` are the B0 sets. Verdict PASS_DRY_IDENTICAL. Of the listed names, 55 sit in a forbidden name class: the `*_ngc3198_probe.json` planned-input configs of NGC_SEED_ROUTE_A_CONFIG. They were listed, never opened, and are named in `aux/BUILD_MANIFEST_C4V001.json`.

Sources of B0 and B0prime_DRY (sha256 from bytes):

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/out/B0_R5_RUN_V001/B0_R5_VS_R4_C2V001.json` `e10e6a584ab49083f24bf4fbb7d94a32ccb667c1c1c7e0e3ff3943ca1061f929`: link 2 (r4 -> r5) plan identity, B0-EMPTY counted / no-evidence rows
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/gates/b0_r5_vs_r4_c2v001.py` `857ccb8a49e11314c7534b1651bfd316b5eab156b2f26b8b148fea385ef4ce5c`: computing tool of link 2
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r4/out/GATE_RECORDS_R4_SCHEMA_C2V002/GATE_B0.json` `580a86e222d423b863ffddc08e071d05ec0ea7de9945324d156809ed22de659c`: link 1 maps and EXT/GEO/NGC classification
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r4/out/B0_RUN_V001/B0_PLAN_IDENTITY_C2V001.json` `19625e805785a9d5504b6c8cc7015934a3bc50487e542f041f691c33da835974`: link 1 per-spec exit codes, verdicts, file counts
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r4/gates/b0_plan_identity_c2v002.py` `b9aeb78e8a58ab369e923b4092cf504400633259843a7b129183333f7806cef3`: computing tool of link 1
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r4/gates/write_gate_records_v007_c2v003.py` `9e9b6bb34e8b45f8c32d0e170c56ecc5d1da95823a592ece049d0dac835447c9`: writer of the r4 records (precedent)
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/galaxy_m0_forward_c2v010.py` `b5cc62afb7814b4f337a012a1ffd1f1e677f398ac18a1f8297c7ff49ae5374c6`: sealed driver v010 r5
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r4/galaxy_m0_forward_c2v010.py` `b9ae92d5857951511437cf7632eb732c97b63592ed700e6810941c5f2d8d762b`: predecessor v010 r4
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/kmax_prereg_v005_c2/extension_c5c6/driver_v009/galaxy_m0_forward_c2v009.py` `999331afd604dd9829aa8f389f43cdb87603d03412d52ba09712226787f18db6`: parent v009-EXT
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/stage_successor_gal_c2v005/driver/galaxy_m0_forward_c2v009.py` `237ef3d41daf4d99b0aafed3e90b27b095a741a9f66ea06ea34f3e44876d47bb`: parent v009-GEO
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/CASCADE_MAP_R5_C2V001.json` `a7281e10a15c7f51eae8b5d5336648c1d0a7d04a8cf932b3860c9eba3636a880`: link 2 declared map
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/BUILD.md` `0c18831261435a7e04401ccba31fb6bbe1a01809505055036d876c13c5e364b2`: r5 BUILD (declared map text, sec 4)
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/specs/SPECS_P128_R5_C2V001.json` `8186a16fd001564ead4a4e43ec44be5db71c0d66b194a988c376817ad8d55683`: P128 specs of link 2
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r11/FIELDS_R11.md` `c7f0dec6ff1ae45dc242c69686e88ad73089a39e1b582e73650e6e18a7368cc5`: field contract
- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0598_2026-10-18_claude4_B3_json_and_B0_family_records.md` `da395935443317525ed72a42ae0cd7880897dc04fbec84e11a0429169dd33466`: assignment

## 5. B0_FA (`888488cd236fb79d4f9462a64b37e809080a0e5ec6d40b4dac63375856bd9009`)

| case | status | code | spec sha256 | r5 exit | source row | label |
|---|---|---|---|---|---|---|
| A1 | REFUSED | ROUTE_A_CHECKPOINT_MISSING | `688373516b8f08d2d59619b565e6b3c4dd7de14cb34e00697de83dc7e4122ee0` | 1 | `FA_A1_NFP_EMPTY` r5.stderr_tail | TESTED |
| A2 | REFUSED | ROUTE_A_CHECKPOINT_MISSING | `7d2db4b6c030fcd0bcd6ab1c0f17694214060c86dfe26cb5e1f2a878821e00dd` | 1 | `FA_A2_NFP_ABSENT` r5.stderr_tail | TESTED |
| A4 | REFUSED | ROUTE_A_CHECKPOINT_MISSING | `d67a89e4d67c5416f959f5b0f6ccc44e7e6bde90a41c658f01c32106507a44ce` | 1 | `FA_A4_CONV_EMPTY` r5.stderr_tail | TESTED |

Derivation: status/code from the r5 driver terminal line recorded by the r5 B0 run (rows FA_A1_NFP_EMPTY, FA_A2_NFP_ABSENT, FA_A4_CONV_EMPTY): re.match(r"(\w+): (\w+)") -> status REFUSED iff the first token is Refusal, code = the second token (the derivation of driver_r4/gates/write_gate_records_v007_c2v003.py); the r5 run executes the r5 driver in dry-run (simulate) mode; the refusal precedes any stage. Each spec sha equals the r4 B0_FA record's (`899a89e9`), and r4 and r5 end with the same terminal line after T. In the B0 count these three rows are no evidence (equal early failures); B0_FA reads the refusal itself.

## 6. Not built on r5: the exact runs each record needs

**B0_N3:** the RA8 static TailBoundary / TailState guard scan on the r5 tail-ON code: every construction and tail build site in the r5 driver and in the r5 cascade image of each file the r4 scan covered, each with its tail-OFF guard (the N3_SITES scan of write_gate_records_v007_c2v003.py, retargeted to the r5 paths and shas of CASCADE_MAP_R5_C2V001; the guard file RO1 worker c2v002 9f74d465 -> r5 fbe9ae79). No r5 N3 output exists.

Existing outputs (pinned, sha256 from bytes; not usable for the sealed driver): `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r4/out/GATE_RECORDS_R4_SCHEMA_C2V002/GATE_B0_N3.json` `8c3ce4dfa979fa66ae09750efd4c140bc53d41e66ce3981b6a8da3d35e88d92c` (r4 B0_N3 record (driver b9ae92d5)); `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r4/gates/write_gate_records_v007_c2v003.py` `9e9b6bb34e8b45f8c32d0e170c56ecc5d1da95823a592ece049d0dac835447c9` (r4 N3 scan producer).

r5 scan targets, mapped from the r4 scan through CASCADE_MAP_R5_C2V001 (shas from the r4 N3 record and the map; no file opened): ddo_composite_stable_cached_binding_v002_uvtail_ro1_c2v002.py `86af6198` -> `86af6198` (scanned); ddo_composite_stable_cached_root_worker_v002_uvtail_ro1_c2v002.py `9f74d465` -> `fbe9ae79` (guard_only); route_a_tail_manifest_c2v001.py `5e716092` -> `44b31a8b` (scanned); galaxy_m0_forward_c2v010.py `b9ae92d5` -> `b5cc62af` (scanned); route_a_tail_manifest_nodes_c2v001.py `9ec05805` -> `e003fcb5` (scanned); route_a_uv_tail_controller_nodes_c2v001.py `af93ee98` -> `e5a29a67` (scanned); uvt_route_b_binding_nodes_c2v001.py `493248a1` -> `1b5f3b4f` (scanned); route_a_uv_tail_controller_c2v001.py `51d32e7b` -> `c5bdd055` (scanned); uvt_route_b_binding_c2v001.py `7288a5d1` -> `1e27430c` (scanned).

**B0_RO1:** (a) the r5 identity runs Z2 (spec 2d5e79d0), Z2_OFF_RO1 (894e5b3a) and B0prime_RERUN (4ac5527a) on driver b5cc62af (root launches, A55 item 3; SEAL_CHECKLIST A5), read by a B0_RO1 producer for result.json sha256 and route_a_outcome.ro1.fired false; (b) the RA5 (b) replay on the C6 iteration-8 checkpoint through the r5 RO1 custody (workers fbe9ae79 / 869ce387, binding 86af6198): ROUTE_A_READOUT_NO_CIRCULAR_BRANCH at query 3, handed to route B; (c) the part (c) cases OTHER_EXCEPTION and REFUSAL_BEFORE_CONVERGENCE (expected = observed = CALL_FAILED) on the same custody. No B0_RO1 gate record exists for any driver.

Existing outputs (pinned, sha256 from bytes; not usable for the sealed driver): `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ro1_readout_c2/out/TEST_C6_REPLAY_C2V003.json` `55cdc6b551c9823eb3514ab9987fe5bd5e2b8f8c677c24896d2e3f574e7b95ba` (C6 replay on RO1 c2v001 workers fc698c3c / 867d2c87 and a v009 test vehicle); `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ro1_readout_c2/out/TEST_SYN_RO1_C2V001.json` `7cdda835d56ca729d97b277ac1b42e09636078c51c9c62590282f7ed63e0d447` (synthetic RO1 predicate tests); `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ro1_readout_c2/out/TEST_DRIVER_PATCH_C2V002.json` `5ab535450d58c3b3c6448af8499dc3e13d9af02bc91c4675245f04943b961de8` (RO1 driver patch on v009-EXT).

**I4:** the I4 run "I4 at production (C2T N8 against N1)" (CHECK_V001 sec 10, listed UNTESTED there) on driver v010 r5 b5cc62af with the tail ON: the same C2T spec at route_a.column_workers 8 and 1, compared bitwise outside custody (declared token list TOKENS_I4_SERIAL_PARALLEL), with the V8c-F1 fix confirmed on the r5 parallel worker. The only registered N1 pair is the r4 V007 registry C2T N8 / N1_FALLBACK templates (1348aed5 / 2cc67753, both plan-identical r5 vs r4 in the r5 B0 run); the P128 registry SPECS_P128_R5_C2V001 carries no N1 spec. The pair is root to fix. No I4 gate record exists for any driver.

Existing outputs (pinned, sha256 from bytes; not usable for the sealed driver): `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/check/CHECK_V001.md` `7eb2e136b227f23dc2be7903bfb9ebfb9edacbbffb16aa2e9ba1040144e3b176` (A51 final check: replay-level serial == parallel tail ON on driver v010 r3 4c14552f); `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver/launch_v002/TOKENS_I4_SERIAL_PARALLEL.json` `50d6af9443b0d95659690e16312a83a8ab4cf61c6a7a4275fb85d42ee7c4c5f4` (declared I4 custody token list (empty declared list)).

Earlier B0-family records found and pinned (none on r5): B0 `d46f67d7` (driver `474316c9`); B0prime_DRY `d9260859` (driver `474316c9`); B0_FA `ecb531a9` (driver `474316c9`); B0_N3 `c2c83dfd` (driver `474316c9`); B0 `bc618362` (driver `474316c9`); B0prime_DRY `6dfe24a8` (driver `474316c9`); B0_FA `17620675` (driver `474316c9`); B0_N3 `773b9b0e` (driver `474316c9`); B0 `255fdda1` (driver `474316c9`); B0prime_DRY `37b014a0` (driver `474316c9`); B0_FA `58d078f6` (driver `474316c9`); B0_N3 `9998916e` (driver `474316c9`); B0 `7849f03b` (driver `4c14552f`); B0prime_DRY `9fa17a86` (driver `4c14552f`); B0_FA `74e67ce7` (driver `4c14552f`); B0_N3 `88ffc60b` (driver `4c14552f`); B0 `e8c7c0fb` (driver `4c14552f`); B0prime_DRY `980f1ede` (driver `4c14552f`); B0_FA `72784f96` (driver `4c14552f`); B0_N3 `d8996faa` (driver `4c14552f`); B0 `e7d8e5b3` (driver `b9ae92d5`); B0prime_DRY `b54edde8` (driver `b9ae92d5`); B0_FA `280ee654` (driver `b9ae92d5`); B0_N3 `0bdf05a7` (driver `b9ae92d5`); B0 `580a86e2` (driver `b9ae92d5`); B0prime_DRY `70336ea4` (driver `b9ae92d5`); B0_FA `899a89e9` (driver `b9ae92d5`); B0_N3 `8c3ce4df` (driver `b9ae92d5`). Full paths and shas are in `aux/MISSING_RUNS_C4V001.json`.

## 7. r6

**r6: not built, BUILD not landed.** TESTED by listing at 18:53Z: `tail_scheme_impl_c2/driver_r6/` has no `BUILD.md` (the builder re-checked it: build_md_present = False; checked again for this report: False). The r6 outputs exist, but were not used: `out/B0_R6_RUN_V001/B0_R6_VS_R5_C2V001.json` `2afaf49a3280aff905d80b880d03bfd55943f80a1cbd0c43ee056cb1e53f83ba` (its stdout `6392d725`: set A 84 counted, 84 PASS_PLAN_IDENTICAL, 16 no evidence; set B 37 counted, 37 PASS), and the DRYRUN_P128_R6 runs V001 and V002. A83 says r6 is stopped at its BUILD. When the BUILD lands, this builder pattern applies with `driver_r6` inputs.

## 8. Observations (not record defects)

1. **B3 module version.** B3 tested tail module v001 `c28d4209`. The sealed r5 pins module v002 `2026f2b6`, which differs only in TAIL_MEMORY_CAP_BYTES (r5 BUILD.md sec 1; driver_r5/check (a)). The carry-over is FORMAL; B3 was not rerun on v002. The record's `note` declares it.
2. **No C5H R-PAIR member spec in the B0 EXT set.** No B0 output carries one, with or without projection_sha256 / declared_differences (A52.3, A53): neither the r5 run nor the r4 record (580a86e2). If a C5H R-PAIR member is ever named, r11 reads it invalid (C5H_RPAIR_MEMBER_SPEC_HAS_NO_B0_RECORD_AGAINST_V009_EXT_A52_3). FORMAL from case_validity; UNTESTED on a run.
3. **M_s 128 production specs.** The P = 128 rows of the r5 B0 run are Codex1 registry V002 (M_s 64; SPECS_P128_R5_C2V001). The registered production set (P128/M_s 128, c7023846, SEAL_CHECKLIST r4) has no r5-vs-r4 row in any output read here. driver_r5/check finding N2 says the same. B0 FIELDS sets do not need T-case specs. UNTESTED.
4. **Registry version.** A newer `PRODUCER_REGISTRY_C3V002.json` (`3b38c794`) sits beside the pinned C3V001. The test registry copies C3V001, as instructed.
5. **Checklist.** SEAL_CHECKLIST r4 item A6 (successor B0 tool and B0 record rerun, B0-EMPTY, on the chosen driver) is still PENDING there. These records are built from that rerun's output (the r5 B0 tool) and are root's to register.

## 9. Errors register

- **E1 (rule 2 breach, survey, about 18:38-18:41Z).** Two recursive `grep -rl --include=*.json` over all of claude_artifacts, looking for I4 / B0_RO1 outputs; the second was stopped early. grep opened every .json there, including 270 files in forbidden name classes: SPARC-named schema and audit files, synthetic look-alike `runs_ext/KMAX_A2F10_C5H_RUN_V001` trees and one `runs_ext/UVT_dummy` in review folders. Only matching file names were printed; no content was shown. Bounded, TESTED: grep (ugrep 7.8.4) follows no symlink under -r; all 366 multiply-linked inodes have every link inside claude_artifacts. So no real run tree (and not the registered C5H run) was reached. Correction: name-only searches from then on.
- **E2.** One PARTIAL.md append failed to parse in zsh (an apostrophe). Nothing ran; it was redone with a quoted heredoc.
- **E3 (conservative reading of rule 2).** An unfenced exploratory process hashed two tail-library source files named `uvt_route_b_binding_c2v001.py` and `uvt_route_b_binding_nodes_c2v001.py`. Only sha prefixes were printed. The fence later refused the same open in the builder's first scratch dry run (nothing written). The builder takes those shas from the r4 N3 record and the cascade map.
- **E4.** The stdout/stderr capture files of the attempt and final runs (`attempts/*.txt`, `aux_build.*.txt`, `check.*.txt`) were created by shell `>` redirection to new paths, not by `open(x)`. No existing file was overwritten: the paths were new. Later redirections use noclobber.
- **Scratch replica.** Before the builder and checker were committed into `build/tools`, they ran in a scratch copy in the session scratchpad, with a sha-verified fence copy whose write root was that copy. The first dry run was refused by the fence (E3); the second passed. The committed tool bytes equal the tested copies (TESTED).

## 10. Files

- `records/`: the four gate records (above).
- `check/`: `TEST_REGISTRY_C4V001.json`, `GATE_CHECK_C4V001.json` (every reading, the fields each gate read, controls), `controls/` (mutation copies, named CONTROL_*, with their own registry).
- `aux/`: `BUILD_MANIFEST_C4V001.json` (inputs and shas, outputs, builder, names listed but never opened) and `MISSING_RUNS_C4V001.json`.
- `attempts/ATTEMPT_V001/`: the first, passing attempt (records, aux, check).
- `tools/`: `fence_c4v001.py`, `build_records_c4v001.py`, `check_records_c4v001.py`, `make_report_c4v001.py`.
- `PARTIAL.md` (append-only log) and `HASHES.txt` (sha256 of every file written here).

