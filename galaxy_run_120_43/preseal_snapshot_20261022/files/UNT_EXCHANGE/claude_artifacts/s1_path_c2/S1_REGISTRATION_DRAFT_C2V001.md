# S1 transfer test at u_A: target-free registration (draft C2V001, for root entry in V006)

**Status.** DRAFT for root. Nothing here is in force until root enters it in V006 by id. It builds nothing and launches nothing.

**Written** 2026-10-19 ~15:51Z, before any campaign result, any V007 step-2 result, any step-5 value and any NGC value existed or was read. No NGC3198 target or observed-velocity file was opened.

**Labels.** TESTED = read or computed from bytes in this session. FORMAL = follows from registered text or code as read. UNTESTED = not checked; the deciding test is named. [D] = arithmetic on cited numbers. **CHOICE** = not forced by any text; the reason is given, and §14 lists every CHOICE.

**Governing principle.** V005 A48: "No ruling may make adoption easier than the text. Where the text is silent, the stricter-on-adoption reading is chosen." (V5F L34). Here "adoption" means accepting the C4T calibration numerics for prediction at u_A.

---

## 1. Sources (sha256 from bytes, this session)

| Tag | File | sha256 |
|---|---|---|
| P5 | `UNT_EXCHANGE/claude_artifacts/kmax_prereg_v005_c2/KMAX_MATRIX_PREREG_V005.json` | `dbddc02c4d793b44a12136fc4fc88b20c001865ddd4c89b1b70c57bc406bb174` |
| R6 | `UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/r6/KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R6.json` | `d28c95f56321f566b444c3e0bfbbe0ecdac564cbc03a8583ecd5f8d0ae40c0a9` |
| R11 | `UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r11/kmax_tail_compare_c2v007_r11.py` | `a5d10cb1a213931713b9712da0781042d8e02ed5c1e81cda21b97c33b0559c8a` |
| CB | `UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/r5/case_block/CASE_BLOCK_V007_C4V001.json` | `76309ae39f23060cc662c4e218a41e1f95c56a26992402218a6198625f85ee71` |
| A133 | `Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/A133_TWO_PHASE_PROTOCOL_V001.md` | `cd92ef914a0d562f0392080ebf709b5fdb1d85ef7f7b4493ee143fe782cfac17` |
| V6 | `.../CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V006_ADDENDUM.md` (open file; read through A145) | `92ab3b4a0a4b6d6016e5ecaf57a04b8a36aada7a8f9596581eee61aace414e24` |
| V5F | `.../CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM_FROZEN.md` | `c01b3c51e34501d77e474594cc0b4be72c6e068c7f58a595055316313a8d4bb1` |
| RI45 | `UNT_EXCHANGE/claude_artifacts/root_items_step45_c4/ROOT_ITEMS_STEP45_V002.md` | `417de6fef408082695e4e3f68530351a0b71a7c1415d784a29199a8a9ec42ee8` |
| RFC | `UNT_EXCHANGE/claude_artifacts/step4_launch_readiness_c4/launch_order/ROOT_ITEMS_FINAL_C4V004.md` | `97a762e1cf2c7eb76e7f77b4c708cfc5452dd5b72452b2bf86ffc9e369e6b704` |
| LO2 | `UNT_EXCHANGE/claude_artifacts/step4_launch_readiness_c4/v002_work/order/LAUNCH_ORDER_C4V002.md` | `520270983a325b0efc7618713d3761cee9b145308e3cc227e5c17e1823363627` |
| INV | `UNT_EXCHANGE/claude_artifacts/step4_launch_readiness_c4/inventory/INVENTORY_C4V001.json` | `eb359e0f902298b4d8d41e879b1ba85f852e4bf29d7d9d126a66dc239baee75b` |
| 0620 | `UNT_EXCHANGE/FROM_CODEX/0620_2026-10-18_claude4_codex1_step4_no_unguarded_fallback.md` | `037a2a61998d511e398f10f7e8c9203597a48e768bbf09d148ae209d94658e99` |
| DBP | `UNT_EXCHANGE/claude_artifacts/sched_s45_c2/v003/DIRECT_BATCH_PARAMS_S45_C2V003A.json` | `4adc296bcb0ddcd154ec0dcea820908ac525d1d39ce00d633eecc4d0c95f87e7` |
| GATE | `UNT_EXCHANGE/claude_artifacts/sched_s45_c2/v003/machine_gate_s45_c2v003.py` | `736a3438b0a3af41eb8d7b2c764f25ff0f9e18942320a4542a9893b6b419f811` |
| RDS | `UNT_EXCHANGE/claude_artifacts/sched_s45_c2/v003/README_SCHED_S45_C2V003.md` | `486d1d98d60557d1addf7cbf438f141f2001ad6acb94267b722da4abb760055e` |
| CFG | `UNT_EXCHANGE/claude_artifacts/sched_s45_c2/v003/RUN_CONFIG_DDO154_CX2V006R9_S45_C2V003.json` | `d9241676c3b7b32bd3067a55bdfb7821ebc33a68adbdc011ab4e4c58b6e50a4d` |
| G11 | `UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/impl/step4_guard_c2v011.py` | `eb97e303b968dc941e2059ada813be95340662253c327a7b9a9634bb8a2c8033` |
| CORE | `UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/v006r10_c4/calibration_core_cx2v006r10_c4.py` | `dc895f8a993295b76a42b563893e990d2419432db78485dd387ddc232ff449d6` |
| WRP | `UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/v006r10_c4/calibration_orchestrator_cx2v006r10_c4_q5b1.py` | `7a6af535805399d49ec3f1c1cbe9e4911d98f6fae0ad50b69a0641214fcd5d4d` |
| ORC | `UNT_EXCHANGE/claude_artifacts/calibration_orchestrator_c2/v005/calibration_orchestrator_c2v005.py` | `c75a889ff4646a816329756124a19532cbc166d26f47ce2ea5147b71c2cf7c4d` |

`UNT_EXCHANGE` = `/Users/bgm/Research/UNT_EXCHANGE`; `Universal Network Theory` = `/Users/bgm/Research/Universal Network Theory`. V6 is an open file. Its sha differs from the `ff3eeff0` an earlier reader saw. Every V6 line cited here is from `92ab3b4a`.

**What the text gives S1 (TESTED from bytes).**
- P5 L720 is the only S1 text: "rerun the adopted shape at K=3 and K=4 at the calibrated point before prediction". It names the cases, the shape and the point, and nothing else.
- R6 L2139 says "S1 ... (V005 S1) unchanged".
- R11 L489-490 (ADOPT_TAIL next step): "cube K=4 tail-corrected (the C4T configuration) with u_i carried; V005 S1 transfer test at the calibrated point before prediction".
- V6 A142 (L734-742) puts "the S1 registration at u_A" in force by id, and amends R-D15. No V6 entry from A107 to A145 gives S1's statistic, threshold, validity binding, reading or failure next step. That is TESTED by a single-file grep of V6 for `S1`, which hits only L283, L478, L736 and L742.

## 2. Scope

- S1 exists only if V007 reads ADOPT_TAIL. Otherwise there is no campaign and no S1 (A133 L5).
- S1 tests one thing: whether the adopted calibration numerics (C4T) transfer from the anchor, where adoption was measured (P5 L720), to the calibrated point u_A.
- It tests no other point: no step-5 member, no FD point and no Phase-2 estimate. A133 L202 and L380 call u_A "a choice, not a derivation". Transfer to every other point stays UNTESTED. The deciding test would be the same pair at that point, and none is registered.
- S1 is target-free. It runs DDO154 at u_A, and its reading uses DDO154 model speeds only.

## 3. Cases and the calibrated point

| Item | Registered | Basis |
|---|---|---|
| Cases | **S1_UA_C3T**: the C3T configuration, cube, tail-corrected, K = 3. **S1_UA_C4T**: the C4T configuration, K = 4. These two names replace `ROOT_NAMES_AT_REGISTRATION_K3/_K4` (DBP L155-168). | Cases from P5 L720; shape and tail from R11 L489; configurations from CB L394-438 (C3T) and L820-868 (C4T). Names: **CHOICE C5**. |
| Calibrated point | **u_A** = the engine's `primary_anchor` at budget B_P1, in the order seed, then most interior admitted entry, then first admitted repair point, then most interior pre-march global-design point (A133 L55-59). B_P1 is the number of forward calls before the first call whose family is outside {seed, jacobian, repair, gd_pre} (V6 L600, which generalizes A133 L61). B_P1 comes from the double byte-equal replay and is written to the Phase-1 registry (A133 L62-65). | FORMAL: A133 L55-65, V6 L600, V6 L736. |
| Bits | S1 runs at u_A's **exact theta bits**: those of the Phase-1 record (A133 L65), equal to the campaign's cache entry for u_A (AT-0a, A133 L248). Every physical leaf of both S1 specs is byte-equal to the campaign's own u_A call: `Mapper.build`, ORC L2216-2219 (`common_scale_s`, `gamma = gamma_over_Eref * Eref_base_J`, `ell_F_m`, `distance_Mpc`). Distance is fixed in mode `DDO154_DISTANCE_FIXED_AT_REGISTERED` (ORC L160). | FORMAL. Taking the bytes from the u_A call's own recorded spec is **CHOICE C4**. |
| Both phases | One S1 at u_A serves Phase 1 and Phase 2 (A133 L202). If AT-0b later finds that the Phase-2 primary anchor differs from u_A (A133 L254), S1 is **not** repeated at the Phase-2 anchor. AT-0b's own outcome applies, and the difference is disclosed. | **CHOICE C2**. |
| No u_A | On an engine terminal status or NO_IDENTIFIED_DIRECTION (A133 L70-73) there is no u_A. S1 reads NOT_RUN(NO_U_A). | FORMAL. |

## 4. Per-call spec deltas from the campaign's u_A call

Base = the spec bytes of the campaign's own call at u_A (**CHOICE C4**). Its numerics block is C1's, which is the sealed C4T call-spec numerics (CFG L63; the composite grid version at CFG L419 is `DIRECT_LAPSE_PANELS96_KMAX4_OUTER6_C2_0470_V001`).

| Path | S1_UA_C4T | S1_UA_C3T |
|---|---|---|
| `label` | `S1 transfer test C4T at u_A theta <theta_key[:16]>; base <base_sha8>` (same format as ORC L2220) | the same, with `C3T` |
| `physical.*`, `coefficients`, `galaxy` | byte-equal to the u_A call | byte-equal to the u_A call |
| `numerics`, except the paths below | byte-equal to the u_A call: brackets, including any recovery block (ORC L2221-2222), picard, route_a, truncation cube, the uv_tail config | byte-equal to the u_A call |
| `numerics.composite_grid_spec` | unchanged: C4T's (CB L828-868; 16 panels, 96 axis nodes, breaks to ±4) | C3T's registered block, bitwise (CB L402-438; 14 panels of order 6, 84 axis nodes (CB L437), breaks to ±3, version `DIRECT_LAPSE_PANELS84_KMAX3_OUTER6_C2_0470_V001` (CB L438)) |
| `numerics.uv_tail.eps_certificate` / `.lo_certificate` | unchanged. `point_identity` excludes the label and these two slots (CORE L233-238), so the registry lookup returns the u_A point's own certificates (FORMAL). | this state's own: the EPS record and the ρ record for `point_identity(S1_UA_C3T)`, which differs from u_A's because numerics are in the identity (CORE L237-238). Route: §9, control 3. |
| driver | r5 `b5cc62af...` (CFG L8; G11 L10; CB L816 and L1246) | same |

- **TESTED from bytes:** C3T and C4T in CB differ only in `grid` (G3/G4, CB L395/L821), `normalized_spec_equal./numerics.composite_grid_spec` and `note`. They share `uv_tail_config_sha256` `6d5606ed` (CB L814/L1244), `tail` true and `ro1_required` true (CB L812-813 / L1242-1243), and drivers_allowed = [r5] (CB L815-816 / L1245-1246). Case block `route_a_mode` is `parallel8`.
- **Label:** a distinct label is **CHOICE C5**. It gives custody separation from the campaign's u_A result. `label` is a declared changed path (ORC L156) and is not in `point_identity`, so it changes no certificate lookup (FORMAL). That it changes no computed value is UNTESTED; the deciding test is the K4/K4′ comparison in §5.
- **No admission:** both calls compute route A fresh and admit no saved state (**CHOICE C8**).

## 5. Statistic

- **Rows:** the 12 registered DDO154 rows (P5 L708 window 0.49-5.92 kpc; P5 L710).
- **Readout:** v_i is the call's own recorded readout (A134 Q4, V6 L497): the Picard-pass rows at call geometry, excluding the diagnostic route-A rows (V6 L524).
- **tau_i = 0.25 σ_i** (P5 L729). The values are P5 L960-971, in row order: 0.4, 0.2, 0.175, 0.125, 0.1, 0.05, 0.05, 0.05, 0.075, 0.15, 0.175, 0.325 km/s.
- **Records.**
  - K3 = S1_UA_C3T.
  - K4 = S1_UA_C4T.
  - K4′ = the campaign's own u_A call, read only after this registration is in force. **CHOICE C3.**
- **Per row:** d_i = v_i(K4) − v_i(K3) and d′_i = v_i(K4′) − v_i(K3), signed, in km/s.
- **Statistic of record:** Dhat_S1 = max over the 12 rows of max(|d_i|, |d′_i|) / tau_i. This is V005's Dhat (P5 L727) for the pair (3,4) at u_A, which V007 keeps as its statistic (R6 L1059-1060). Taking the worse of the two K=4 records is **CHOICE C3**. Applying Dhat to S1 at all is **CHOICE C6**.
- **Reported, never gating:**
  - Δ4_i = v_i(K4) − v_i(K4′), with a bitwise-equal flag. This is a free check of rerun determinism for tail-ON parallel8 DDO, which is UNTESTED in every source read here.
  - Absolute |d_i| in km/s (P5 L727), and d_i/v_i (P5 L718).
  - The anchor's own d34_i = v_i(C4T) − v_i(C3T) from the V007 compare of record, beside d_i. This is **CHOICE C20**.

## 6. Thresholds

| Id | Clause | Status |
|---|---|---|
| TH-1 | Dhat_S1 ≤ 1 | **V005's, where it applies:** the first numeric clause of `shape_pass` (P5 L726), on the one pair S1 has. |
| TH-2 | for **every** row i: max(\|d_i\|, \|d′_i\|) / tau_i ≤ 1/2, with no TINY exemption | **Stricter, where the text is silent (CHOICE C7).** It is the form and number of V007 T1_H: "per row ... /tau_i <= 1/2 every row ... no TINY exemption" (R6 L1636). |

**PASS needs TH-1 and TH-2.** TH-2 implies TH-1, so the operative per-row bound is tau_i/2. Per row that is 0.2, 0.1, 0.0875, 0.0625, 0.05, 0.025, 0.025, 0.025, 0.0375, 0.075, 0.0875 and 0.1625 km/s [D].

**Where the text is silent, and why TH-2 is the stricter reading:**
- The clauses V005 and V007 cannot apply without K=2 are:
  - the contraction clause Dhat(3,4) ≤ 0.5·Dhat(2,3) (P5 L726);
  - the RA6 per-row clause (R6 L1627);
  - T1_H, which needs C6T (R6 L1636).
- Without them, contraction at u_A cannot be measured.
- If the anchor's contraction (q ≤ 1/2, P5 L726) is assumed to transfer, the remainder beyond K=4 at u_A is at most |d_i|. TH-2 then holds that remainder to tau_i/2. That is the stricter of the two registered remainder bounds: P5 L726 gives tau_i, and T1_H gives tau_i/2.
- Applying TH-1 alone would present the computable part of T1 as if it were T1, which A48 forbids (V5F L34).
- **UNTESTED:** that contraction transfers to u_A. Deciding test: C2T at u_A, which is the S1-DIAG step in §8.

**Decidability [D].** The smallest bound, 0.025 km/s (rows 06-08, P5 L965-967), is 2.6 times the measured Picard floor of 0.0095 km/s (P5 L735) and 2 times tau_picard of 0.0125 km/s (P5 L732).

**Stated now, before any number exists.** If the anchor's own Dhat_T(3,4) lies in (1/2, 1], TH-2 is expected to read FAIL at a u_A near the anchor, even though the anchor passed T1. That is a property of the stricter threshold. It is pre-named as sub-code FAIL_TH2, not as a transfer defect.

**Alternatives not chosen:**
- **(a) TH-1 alone.** Rejected under A48.
- **(b) Add C2T at u_A and apply T1 literally.** Not chosen because root's task fixes the cases at K=3 and K=4. It would also be a third run outside the booked 2 (LO2 L89; RFC L249), with no launch path (§9). It is kept as the failure next step.
- **(c) A bound relative to the anchor, |d_i(u_A)| ≤ |d34_i(anchor)| per row.** Rejected. At u_A ≈ anchor it compares two nearly equal increments, each carrying Picard error up to 0.0125 km/s per call (P5 L732), so it would read FAIL about half the time with perfect transfer.

## 7. Validity gates (any failure gives INVALID, never FAIL)

| Gate | Requirement | Basis |
|---|---|---|
| SV0 | A FINISHED receipt; the spec sha registered per launched spec, with a driver sha check (RI45-13, V6 L565); the outdir is distinct and fresh under the step-4 run root (V6 L283) | FORMAL |
| SV1 | driver status COMPLETED, `valid` true, exactly the 12 registered row ids, all speeds finite | P5 V1 L710 |
| SV2 | final-pass `max_abs_change_km_s` present and ≤ tau_picard = 0.0125 km/s | P5 V2 L711, L732 |
| SV3 | The normalized spec equals the §4 registered S1 spec at every path. In particular `composite_grid_spec` equals CB C3T/C4T bitwise, truncation is cube, and the driver is r5. P5 V3 binds the physical leaves to "the REGISTERED anchor block" (P5 L712), which every u_A case would fail by construction. Here they are re-bound to the u_A call's physical bytes. | P5 V3 L712, re-bound: **CHOICE C8** |
| SV4 | the final field packet's wavevector axis equals the registered grid axis bitwise and holds axis_nodes^3 nodes | P5 V4 L713 |
| SV5 | rows outside the registered mask are exactly zero, and `nonzero_rows_in_packet` equals the mask count | P5 V5 L714 |
| SV6 | the call admitted no saved route-A state. P5 V6 (L715) is vacuous, because S1 admits nothing. | **CHOICE C8** |
| SV7 | The tail-era post-run acceptance that every tail-ON direct call must pass before any value is used, with the same outcome required: the EPS record of the call's own point (Q8, V6 L499), per-state LO acceptance (Q2/Q3/Q5, V6 L496-498, reading points L523-528), and SRB-ROT ≤ tau_i/10 on the accepted state (Q10, V6 L501). | FORMAL if Q5's "all 31 points" (V6 L498) counts S1. [D] 11 HEADLINE + 18 SENS + 2 POST_S1 = 31, matching RDS L27's "31 tail-ON direct-batch caps". Otherwise this is **CHOICE C9** (stricter). |
| SV8 | No unruled flag on either call. If a flag such as TAIL_SOURCE_UNDERCONVERGED is present and TH-1/TH-2 hold, the reading is INVALID(FLAG_PENDING_RULING) until root rules on the flag. If a flag is present and a threshold fails, the reading is INVALID(UNDECIDABLE_FLAGGED). | By analogy with AMB-04 and AMB-17 (V5F L38-39): **CHOICE C10** |
| SV-K4′ | K4′ passes SV1-SV8 as the campaign's own call | **CHOICE C3** |

## 8. Reading, codes and effects

**Order.** PASS and FAIL are decided only when both S1 calls and K4′ are valid (as AMB-17 requires, V5F L39). Otherwise the reading is INVALID if some finished call fails a gate, and NOT_RUN if some case has no FINISHED receipt.

| Code | When | Label | Step-5 effect | Registered next step |
|---|---|---|---|---|
| **PASS** | all valid; TH-1 and TH-2 hold | TESTED-POSITIVE: the numerics transfer at u_A only | Step-5 values may be read, subject to every other gate: r3a seal, M-12 and A133 §2 (A133 L186). | Prediction proceeds; the S1 record's sha is cited in the freeze. |
| **FAIL** | all valid; a threshold fails. FAIL_TH1 means Dhat_S1 > 1. FAIL_TH2 means TH-1 holds and TH-2 fails. | TESTED-NEGATIVE for the transfer of the C4T numerics to u_A. This is not a physics outcome. | **Step-5 use stops, in both phases** (RI45 L111): no step-5 value is read for any score, and no new step-5 NGC launch is made. In-flight step-5 calls run to a terminal receipt and are kept unread (as A133 L103 does). The campaign is not stopped by S1. **CHOICE C12** | **S1-DIAG** (**CHOICE C13**), below. |
| **INVALID** | a finished call or K4′ fails SV0-SV8 or SV-K4′ | UNTESTED | Step-5 values stay unread (validity-only). **CHOICE C11** | The failed gate's V005 next step (P5 L700-705). A monitor or cap stop reruns the identical spec in a fresh outdir with the cap raised (P5 L700(i)), as §10 sets out. INVALID_FINAL comes only after two identical deterministic non-INFRA failures (the form of A133 L217-218). Root then rules on the review that gate names. |
| **NOT_RUN** | some case has no FINISHED receipt. Sub-codes: NO_U_A, NO_LAUNCH_PATH, NOT_ADMITTED, IN_PROGRESS. | UNTESTED | Step-5 values stay unread. Phase-1 scoring waits (A133 L188). **CHOICE C11** | Build the S1 launch path and name it in V6 (§9), then launch when admitted (§11-12). |

**Only PASS releases step-5 reads.** FAIL, INVALID and NOT_RUN all hold them. This is the A48 reading of RI45-04(b)'s "until S1's registered reading is recorded" (RI45 L111): recording a non-PASS code does not release them (**CHOICE C11**).

**S1-DIAG (the next step on FAIL).**
1. Run C2T and C6T at u_A's theta bits, built with the same §4 delta pattern (CB C2T L5, C6T L1250; C6T grid version CB L1306). Read V007 T1 and T1_H literally (R6 L1627, L1636) on {C2T, C3T, C4T, C6T} at u_A, under a successor registration written before any of their values is read.
2. Classify the result:
   - **NOT_CONVERGED_AT_U_A** if T1 fails. Next step: V005 decision-rule 3's route of extending K to 5 and 6 /kpc (P5 L694), under a new prereg.
   - **TAIL_REMAINDER_AT_U_A** if T1 holds and T1_H fails.
   - **INCREMENT_ONLY** if both hold.
3. Only for INCREMENT_ONLY may root rule, in a new V6 entry written before any step-5 value is read, whether step-5 use resumes. That ruling may not be easier than V007 T1 + T1_H applied at u_A (A48), and the S1 FAIL stays on the record and in the published result.
4. S1-DIAG needs the four 0620 controls and its own launch path. CORE L218-219 refuses K ≠ 4.

**The reading record.** It is written by exclusive create by the reviewed S1 reader (**CHOICE C19**). It holds:
- the case and spec shas, the u_A theta key, the K4′ spec sha and the driver sha;
- receipts and the gate results SV0-SV8;
- per row: v_i(K3), v_i(K4), v_i(K4′), d_i, d′_i, Δ4_i and the ratios to tau_i;
- Dhat_S1, the code and sub-code, and any flags.

Root enters the record's sha in a V6 entry. That entry is the "S1 reading recorded" event for A133 L186 and RI45 L111.

## 9. Launch path and the four 0620 controls

**Path.**
- S1 launches only through the S1 template and launch path that A133 assigns (A133 L290). A133 L478 in V6 makes it a root workflow reviewed by Claude3, and it must then be named in a V6 entry.
- No raw CLI and no unguarded fallback may be used (0620 L11).
- Output goes to `/Volumes/External1/Research/UNT_STEP4_RUNS/V007_STEP4_DIRECT_V001/<distinct outdir per call and attempt>` (V6 L283; G11 L268).

**The four controls, all enforced before any process starts (0620 L5-11; RFC L252):**

1. **The sealed V007 ADOPT_TAIL** (0620 L6). The path refuses as G11 `adoption()` does (L194-215): `SEALED_R5_BINDING` (L199), `SEALED_ADOPT_TAIL_REQUIRED` (L200) and `REVIEWED_SEAL_TUPLE_PENDING` (L205). The adoption pin is the sealed compare's verdict report (V6 L562).
2. **The step-4 admission** (0620 L7). A root-published admission record covers batch POST_S1, as G11 `validate()` requires (L314, L316, L317; G11 accepts the batch at L334).
   - The record must **not** attest `campaign_inactive: true` while the campaign runs. G11 L333 requires that attestation, but V6 L742 lets S1 overlap the campaign.
   - The S1 path therefore replaces the L333 attestation with the S1 overlap admission in §11 (FORMAL conflict; resolved by the A142 ruling, V6 L742).
3. **PRELAUNCH, certificate and sensitivity checks** (0620 L8). These are G11 `native_preflight` (L227-261: `certificate_policy_gate` L249, `certificate_check(spec,'prelaunch')` L250, `sensitivity_gate` L251, `prelaunch_check` L252) and the replay equality `PRELAUNCH_REPLAY_MISMATCH` (L352). For S1_UA_C3T the path needs a reviewed successor, because:
   - core `validate_block` raises "kept K must be 4" (CORE L218-219), and the wrapper calls it in `certificate_check` (WRP L80) and in `prelaunch_check` (WRP L203);
   - `prelaunch_check` refuses any normalized path outside DECLARED_CHANGED_PATHS (ORC L156-157, L2030-2038).

   The successor must:
   - add `numerics.composite_grid_spec` as a declared changed path, for the C3T case only, equal to CB L402-438 bitwise;
   - accept last break 3 for that case only;
   - keep every other `validate_block` clause (CORE L213-231).

   The S1_UA_C3T EPS and ρ records come from CP-1-style per-point production for its own `point_identity` (V6 L499, L516-519).
4. **The r5 allowlist** (0620 L9): driver sha = `R5_SHA` (G11 L10), with `TAIL_ON_R5_REQUIRED` (G11 L220, L238), and CB drivers_allowed (L816, L1246).

**FORMAL, UNTESTED:** the as-built G11 cannot launch S1_UA_C3T. Deciding test: a synthetic C3T-at-u spec through G11 `native_preflight` with a synthetic config, `python3 -I -B`, expecting refusal at CORE L219.

## 10. Caps (per call)

| Cap | Value | Basis |
|---|---|---|
| Wall | 100,800 s. **PROVISIONAL**: the DDO tail-ON constant in force at launch, written into the admission record. | DBP L158, L163; RDS L27; re-derived from the step-2 receipts (V6 L652; RDS L104-108). Following the successor constant is **CHOICE C17**. |
| RSS | 68,719,476,736 B (64 GiB) | DBP L157, L162 (= CFG L489) |
| Output | 85,899,345,920 B (80 GiB) | DBP L156, L161; V6 L653 |

- **Caps are value-relevant** (A133 L222). A cap stop reads INVALID pending a rerun.
- **The rerun** uses the identical spec in a fresh outdir, with RSS at RAM (137,438,953,472 B, GATE L85) and the wall doubled (201,600 s [D]). This is A133 L218's step-5 form, applied to S1 (**CHOICE C17**).
- **Disk, failing closed** (V6 L288-289):
  - at admission, free space ≥ 2 × 80 + 20 = 180 GiB [D];
  - before each start, ≥ 80 + 20 = 100 GiB [D].

  LO2 L416's 212 GiB assumed 96 GiB caps, which the 80 GiB cap (V6 L653) supersedes. The modelled S1 output is 11.3, 43.0 or 115.4 GiB at 6.08 GB, typical and worst (LO2 L406). These are UNTESTED.

## 11. Memory admission

A142 makes the machine gate govern S1 (V6 L742: "under the machine gate (A143)"). Gate v003 has no S1-head predicate, only `--hold-check` and `--twin-start-check` (GATE L71, L812-830). An S1 call starts only when **all** of the following hold (**CHOICE C15**, the conjunction of every rule that claims S1):

1. **Gate v003's own head decision, for the S1 head**, using its DDO class from `class_from_numerics` (GATE L239-257). This is the full rule a-i (GATE L49-59), including:
   - d1 MEMORY_HARD ≤ hard_eff, with static hard 83 GB (GATE L95);
   - d2 MEMORY_KNEE ≤ knee_eff, with static knee 72 GB (GATE L93);
   - the route-A cap of 2, machine-wide (GATE L51, L88);
   - swap ≤ 8 GB (GATE L110).

   Because no such predicate exists, the S1 launch path must call the gate's pure decision function (GATE L504-509) read-only. This is a build, and UNTESTED.
2. **A133's root rule** (A133 L114-117): A130 measured run footprint + S1 term + campaign reserve ≤ 103 GB (75% of RAM).
   - The campaign reserve is 29.1 GB (V6 L669; this is A133 L117's 27 in consistent units).
   - The S1 term is 36.79 GB = 11.0 + 20.0 + 5.79 [D]: the gate's GENERIC class, as which the campaign's gate counts an r5 S1 tree (GATE L4-6, L97, L108, L109). It replaces A133 L123's "27 GB per S1 call", which is 29.1 GB in consistent units, because it is the larger of the two (**CHOICE C15**).
   - The rule therefore admits S1 only at a measured footprint ≤ 37.11 GB [D].
3. **`machine_gate_s45_c2v003.py --hold-check` exits 0** (DBP L355-366; RDS L24). An exit of 3 means the twin is in route A; 2 means the probe failed. Both hold.
4. **The packet's own check:** `memory_pressure` free ≥ 25% (DBP L182). DBP L383 notes that this check is blind.
5. **Concurrency:**
   - at most 1 S1 call while the campaign is active, so that the campaign plus S1 stays within the route-A cap of 2 and a campaign head is not refused because of S1 (A133 L51, L124);
   - at most 2 after FINAL_SUMMARY (DBP L181).

   **CHOICE C14.**
6. **Queue priority:** S1 heads go ahead of Phase-1 NGC launches, never ahead of the campaign (RI45 L254-255: "Schedule S4-POST-S1 first", because its reading gates step-5 reading). **CHOICE C14.**

**Consequence, stated now [D/UNTESTED].**
- Rule 2 admits S1 beside one C4T-class campaign call (23.2-27.1 GB measured, A133 L119) only when little else is running.
- With S0 NGC trees in flight (about 14 GB each modelled, A133 L123), S1 may wait. It may then reach NOT_RUN at the Phase-1 read deadline (Sat 24 Oct 09:00 CDT, A133 L186), in which case Phase-1 scoring waits (A133 L188).

## 12. Timing

| Moment | Rule | Basis |
|---|---|---|
| Registration in force | Before the **campaign's W1 launch**, which is stricter than "before the campaign result is read" (INV L4073). | **CHOICE C1**. RFC L250 (close by BEFORE_CAMPAIGN); A133 L184 (step-0 batch, before H2) |
| Earliest S1 start | When u_A is fixed by the B_P1 snapshot (A133 L55-65); expected Tue 20 Oct 22:17 CDT, low Tue 07:43, high Fri 23 Oct 07:39 (A133 L301). The launch path is needed by then (A133 L290). | FORMAL |
| Start windows | (i) during a campaign wave with a single DDO call (A133 L346), or (ii) when no campaign DDO call is in flight, including after FINAL_SUMMARY, where S1 is first in the post-campaign queue (LO2 L138, Z1). In both cases §11 must admit. | (i) FORMAL; adding (ii) is **CHOICE C16** |
| Case order | Not value-relevant. Whichever case is admissible first starts first. DBP L166-168 lists K3 before K4, but S1_UA_C4T has no certificate prerequisite. | **CHOICE C16** |
| Duration | 5.20 h E / 8.76 h U per call (LO2 L309). Run serially under §11 rule 5, that is 10.40 h E / 17.52 h U [D, UNTESTED]. | LO2 L309 |
| Reading recorded | Before any Phase-1 NGC value is read (A133 L186; deadline Sat 24 Oct 09:00 CDT) and before any step-5 output value is read (RI45 L111, option (b), adopted by V6 L736 through A133 L184). | FORMAL |
| Overlap | S1 may overlap the campaign under the machine gate (V6 L742). This supersedes DBP L383's "must not start while the campaign or the NGC loop has calls running" for S1 only. | FORMAL (A142 is the later ruling) |

## 13. Open for root (UNTESTED unless marked)

1. **The K=3 launch path.** Deciding test in §9.
2. **The S1_UA_C3T certificate route.** CORE L218-219 refuses K ≠ 4 in the wrapper's checks, and whether the EPS and ρ producers accept a K=3 kept grid is unknown. Deciding test: run both producers on a synthetic `point_identity` with the C3T block.
3. **Whether `sensitivity_gate` (G11 L251) passes a K=3 spec.** Deciding test: the same synthetic preflight.
4. **The S1 head predicate in gate v003.** It needs a build (§11 rule 1), with tests.
5. **The wall cap is PROVISIONAL** until the step-2 receipts re-derive it (V6 L652). Retention rule D3 is open (LO2 L417).
6. **The compare of record is r14** (`f3f9ba7e`; V6 A116-A117, L157-178). The ADOPT_TAIL text here was read from r11 (`a5d10cb1`) L489-490. Deciding test: read r14's `NEXT_STEP['ADOPT_TAIL']` from bytes once root names its path. Separately, R6 L3 reads "FINAL DRAFT r6 (NOT SEALED)". Deciding test: check that the SEAL_RECORD's prereg pin is `d28c95f5`.
7. **Determinism of a tail-ON parallel8 DDO rerun.** It is untested in these sources; R6 L1321's B0prime_RERUN is tail-OFF with route A admitted. The §5 Δ4 report measures it at no cost.
8. **Transfer of contraction to u_A** (§6). Deciding test: C2T at u_A (S1-DIAG).

## 14. CHOICES (not forced by text)

| Id | Choice | Reason |
|---|---|---|
| C1 | In force before campaign W1 launch | Stricter than "before the result is read" (INV L4073), and u_A can be the W1 seed (A133 L56); matches RFC L250 BEFORE_CAMPAIGN |
| C2 | "Calibrated point" = u_A for both phases; no S1 repeat at a different Phase-2 anchor | A133 L202 registers one S1 at u_A; a second S1 would be an unregistered second chance |
| C3 | K4 is a fresh run, and the statistic also takes K4′ (the campaign's u_A call), using the worse of the two | Keeps the 2 booked runs (LO2 L89); the max over both K=4 records is stricter (A48) and turns a determinism check into a strictness term instead of a new gate |
| C4 | S1 specs are derived from the u_A call's own recorded spec bytes | Bit-identity with the u_A call, including any bracket recovery, whatever config successors land after `march0` |
| C5 | Case names S1_UA_C3T and S1_UA_C4T; a distinct label | Custody separation from the campaign record; the label changes no certificate lookup (CORE L237-238) |
| C6 | The statistic is V005 Dhat on the pair (3,4) | The only registered statistic computable from the two named cases (P5 L727; R6 L1060); anything else would be a new knob |
| C7 | TH-2: every row ≤ tau_i/2, with no TINY exemption | Stricter where the text is silent (A48): it is the T1_H bound (R6 L1636), applied to the only remainder proxy at u_A |
| C8 | V3's physical binding re-bound to u_A's bytes; V6 vacuous (no admission) | P5 V3 binds the anchor block (L712), which fails every u_A case by construction; fresh route A avoids V6's admitted-state question |
| C9 | SV7 tail-era acceptance applies to S1 | FORMAL if Q5's 31 points include POST_S1 ([D] 11 + 18 + 2); stricter otherwise |
| C10 | A flag blocks PASS (INVALID(FLAG_PENDING_RULING) or INVALID(UNDECIDABLE_FLAGGED)) | AMB-04 and AMB-17 analogue (V5F L38-39) |
| C11 | Only PASS releases step-5 reads | A48 reading of RI45 L111; otherwise recording INVALID or NOT_RUN would release reads |
| C12 | On FAIL: no new step-5 launch; in-flight calls finish unread; the campaign continues | "stops step-5 use" (RI45 L111) names step 5 only; kept outputs stay available to re-bind (A133 L203) |
| C13 | The FAIL next step is S1-DIAG (C2T and C6T at u_A; V007 T1/T1_H literally) | RI45 L111 needs a registered next step and none exists; it uses only registered tests; any resumption is ruled in a new entry, under A48 |
| C14 | ≤ 1 S1 call while the campaign is active (≤ 2 after); S1 goes ahead of Phase-1 NGC launches | Route-A cap 2 machine-wide (GATE L51, L88) and campaign priority (A133 L124); RI45 L254-255 |
| C15 | Memory: the conjunction of gate v003's head decision, A133's rule with the 36.79 GB GENERIC term, hold-check and memory_pressure | Every rule that claims S1 is applied; the larger S1 model is the stricter one (V6 L669 units) |
| C16 | Start window (ii), when no campaign DDO call is in flight; the case order is not fixed | A133 L346 gives only (i); (ii) lets S1 run after FINAL_SUMMARY (LO2 L138); order changes no value |
| C17 | Wall cap follows the successor constant; a cap-stop rerun uses RSS at RAM and doubles the wall | A133 L218 form; caps are value-relevant (A133 L222) |
| C19 | The reading is computed by the reviewed S1 reader and recorded by exclusive create; root enters its sha in V6 | It makes "recorded" (A133 L186) a checkable event |
| C20 | The anchor's d34_i is reported beside d_i and never gates | A transfer diagnostic; a gate on it is undecidable near the anchor (§6 (c)) |

There is no C18. The disk numbers in §10 follow from the V6 L288-289 formula and the 80 GiB cap, so they are not a choice.

## 15. Disclosures

- **Reads.** Named files only: the source map's files plus files cited by explicit path inside them. G11 and the params path come from DBP L370-379 and V6 L631-636. WRP comes from V6 L623, and CORE from WRP L27. The orchestrator path comes from A133 L395. The C3T FILLED spec (CB L818) was sha-hashed only, never opened; its sha starts `212f4b36` and matches CB.
- **Commands.** One non-recursive `ls` of the named `sched_s45_c2/v003/`. Every grep was single-file. `python3 -I -B` was used only for read-only JSON parsing of CB. No test, solver, monitor or launcher ran.
- **Not opened:** run trees, External1, `~/.codex`, `c5h_hull_c2/`, `UVT_*`, `v003g/slots/`. CB contains a `C5H` key, which was neither opened nor printed. The NGC3198-named files opened are the V6 and V5F rulings only.
- **Writes.** This file, by exclusive create, in a new folder `claude_artifacts/s1_path_c2/`.
  - **Deviation:** the text was first composed in this session's private scratchpad (`/private/tmp/claude-501/...`), outside the UNT tree, and then copied byte-for-byte with an exclusive create.
  - Nothing else was written.
- **Inherited from an earlier reader** (it reported "Write nothing" and wrote nothing): the citations ORC L1786 (`to_natural`), WRP L308 (the tail certificate path) and the RUNBOOK_CX1V003 lines appear in its map. They are not used for any number here.
