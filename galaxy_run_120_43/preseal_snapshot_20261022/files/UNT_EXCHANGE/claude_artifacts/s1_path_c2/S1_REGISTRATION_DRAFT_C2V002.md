# S1 transfer test at u_A: target-free registration (draft C2V002, for root entry in V006)

**Status.** DRAFT for root. Nothing here is in force until root enters this file in V006 by its sha256. It supersedes draft C2V001 (`1dc07ffb`) and applies both refutations of C2V001. The launch path and reader it names are built beside it in `claude_artifacts/s1_path_c2/` (README_S1_PATH_C2V001.md); nothing was launched.

**Written** 2026-10-19 (`date -u` 16:41:38Z at the last source read), before any campaign result, any V007 step-2 T value, any step-5 value and any NGC value existed or was read by this lane. No NGC3198 target or observed-velocity file was opened.

**Labels.** TESTED = read or computed from bytes in this session, or shown by a named synthetic test of the s1_path_c2 build (test ids such as L-F7 are in README_S1_PATH_C2V001.md). FORMAL = follows from registered text or code as read. UNTESTED = not checked; the deciding test is named. [D] = arithmetic on cited numbers. **CHOICE** = not forced by any text; §14 lists every CHOICE with its reason.

**Governing principle.** V005 A48, as quoted by C2V001 §0 from the frozen V005 addendum (`c01b3c51` L34; this lane did not open that file): "No ruling may make adoption easier than the text. Where the text is silent, the stricter-on-adoption reading is chosen." Here adoption means accepting the C4T calibration numerics for prediction at u_A. Where a choice only moves timing, A48 does not apply and the choice says so.

---

## 0. What changed from C2V001

Refuter A = the review that found 4 blocking items (B1 seed branch, B2 decidability, B3 INVALID next steps, B4 labels). Refuter B = the review that found 5 (B1 decidability, B2 timing, B3 at-anchor reading, B4 FAIL_TH2 label, B5 widening).

| Finding | Where fixed | How |
|---|---|---|
| A-B2, B-B1: TH-2 dropped "decidable" | §6, §8 | TH-2 is decidable per R6 L1231; new code UNDECIDABLE; R-PAIR next step; old "Decidability [D]" paragraph deleted |
| A-B1, B-B3: u_A can be the seed (the adoption point) | §3 seed branch, §8 | AT_ANCHOR branch, PASS_AT_ADOPTION_POINT, delta-u and leaf-ratio record, root item R-S1-1 |
| A-B3, B-B5: INVALID next steps imported D7 widening | §4, §7, §8 | next steps (i)-(iv) as amended for the tail era; recovery block wording deleted; T-case gates added to §7 |
| A-B4, B-B4: labels overclaimed; FAIL_TH2 contradicted §6 | §8 | PASS, PASS_AT_ADOPTION_POINT, FAIL_TH1 and FAIL_TH2 labels rewritten; untested items named |
| A-B4, B-N7: C2's A48 reasoning pointed the wrong way | §3, §14 C2 | C2 is FORMAL from A133 L202 and flagged to root under A48 |
| B-B2: timing later than the registered deadline | §12, §14 C1 | in force before T0, no later than H2; post-T0 edits are a new version labelled post-result |
| Notes A-N1 to A-N9, B-N1 to B-N11 | §0.1 | all accepted; two in part (reasons below) |

### 0.1 Notes

Accepted in full: A-N1 (§3), A-N2 (§7 SV7), A-N3 (§7 SV8), A-N4 (§5 reported, §13 item 12), A-N5 (§6), A-N6 (§8 S1-DIAG), A-N7 (§8, C21), A-N8 (§3), A-N9 and B-N11 (§15), B-N2 (§11 rule 4), B-N3 (§13 item 1), B-N4 (§13 item 3), B-N6 (built: the reader, §8), B-N7 (C2), B-N8 (§4: the filler refuses a base without `admit: {}`), B-N9 (built: the filler and the launch path re-derive the S1 physical leaves from the u_A theta bits), B-N10 (§5 reported).

Accepted in part:
- **B-N1 (re-pin V6 to `6ae3c5b6`).** V6 has moved on since: this draft read V6 at `8b8356c6` (990 lines, through A149). Every V6 line cited here is from `8b8356c6`; root re-pins at entry. The point of the note (re-pin) is kept; the sha it named is not.
- **B-N5 (use A133's 29.1 GB S1 term).** Used for the A133 root rule (§11 rule 2). The machine gate's own head reservation for an S1 call (11 + 20 + 5.79 = 36.79 GB, GATE L239-258) is the gate's, unchanged; this registration does not alter the gate.

Rejected: none.

## 1. Sources (sha256 from bytes, this session; TESTED)

`UNT_EXCHANGE` = `/Users/bgm/Research/UNT_EXCHANGE`; `CA` = `UNT_EXCHANGE/claude_artifacts`; `CTRL` = `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2`.

| Tag | File | sha256 |
|---|---|---|
| P5 | `CA/kmax_prereg_v005_c2/KMAX_MATRIX_PREREG_V005.json` | `dbddc02c4d793b44a12136fc4fc88b20c001865ddd4c89b1b70c57bc406bb174` |
| R6 | `CA/v007_final_prereg_c4/r6/KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R6.json` | `d28c95f56321f566b444c3e0bfbbe0ecdac564cbc03a8583ecd5f8d0ae40c0a9` |
| R11 | `CA/v007_compare_c2/r11/kmax_tail_compare_c2v007_r11.py` | `a5d10cb1a213931713b9712da0781042d8e02ed5c1e81cda21b97c33b0559c8a` |
| C5 | `CA/kmax_prereg_v005_c2/kmax_compare_c2v005.py` (cited by path in R11 L171) | `49404bc4b0d558c93113ed650802d9009f03be64c364f0d862213783389786f5` |
| CB | `CA/v007_final_prereg_c4/r5/case_block/CASE_BLOCK_V007_C4V001.json` | `76309ae39f23060cc662c4e218a41e1f95c56a26992402218a6198625f85ee71` |
| A133 | `CTRL/A133_TWO_PHASE_PROTOCOL_V001.md` | `cd92ef914a0d562f0392080ebf709b5fdb1d85ef7f7b4493ee143fe782cfac17` |
| V6 | `CTRL/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V006_ADDENDUM.md` (open file; 990 lines; through A149) | `8b8356c6101adc5ce078af2ddd44281207729a5136f4da157a2bcb62ca659bbf` |
| RI45 | `CA/root_items_step45_c4/ROOT_ITEMS_STEP45_V002.md` | `417de6fef408082695e4e3f68530351a0b71a7c1415d784a29199a8a9ec42ee8` |
| RFC | `CA/step4_launch_readiness_c4/launch_order/ROOT_ITEMS_FINAL_C4V004.md` | `97a762e1cf2c7eb76e7f77b4c708cfc5452dd5b72452b2bf86ffc9e369e6b704` |
| LO2 | `CA/step4_launch_readiness_c4/v002_work/order/LAUNCH_ORDER_C4V002.md` | `520270983a325b0efc7618713d3761cee9b145308e3cc227e5c17e1823363627` |
| INV | `CA/step4_launch_readiness_c4/inventory/INVENTORY_C4V001.json` | `eb359e0f902298b4d8d41e879b1ba85f852e4bf29d7d9d126a66dc239baee75b` |
| 0620 | `UNT_EXCHANGE/FROM_CODEX/0620_2026-10-18_claude4_codex1_step4_no_unguarded_fallback.md` | `037a2a61998d511e398f10f7e8c9203597a48e768bbf09d148ae209d94658e99` |
| DBP | `CA/sched_s45_c2/v003/DIRECT_BATCH_PARAMS_S45_C2V003A.json` | `4adc296bcb0ddcd154ec0dcea820908ac525d1d39ce00d633eecc4d0c95f87e7` |
| GATE | `CA/sched_s45_c2/v003/machine_gate_s45_c2v003.py` | `736a3438b0a3af41eb8d7b2c764f25ff0f9e18942320a4542a9893b6b419f811` |
| CFG | `CA/sched_s45_c2/v003/RUN_CONFIG_DDO154_CX2V006R9_S45_C2V003.json` | `d9241676c3b7b32bd3067a55bdfb7821ebc33a68adbdc011ab4e4c58b6e50a4d` |
| G11 | `CA/step4_launch_packet_cx1/impl/step4_guard_c2v011.py` | `eb97e303b968dc941e2059ada813be95340662253c327a7b9a9634bb8a2c8033` |
| L12 | `CA/step4_launch_packet_cx1/impl/step4_launcher_c2v012.py` | `59c00707ea8f3dc42fb2349bd806d42758119354954f878299d56bd21933f2a9` |
| B10 | `CA/step4_launch_packet_cx1/impl/step4_bind_c2v010.py` | `4d07dca36cc7bcf54e29c85f850d0efe7cbb6f8e472579393e23c70bf9920a30` |
| MON | `CA/galaxy_m0_forward_c2_0466/root_monitor_c2v001.py` (CFG monitor) | `ba031c2340057d88ee399138cc645012a93aa7dc3eb7c9bba56d112c94a47107` |
| DRV | `CA/tail_scheme_impl_c2/driver_r5/galaxy_m0_forward_c2v010.py` (hashed only) | `b5cc62afb7814b4f337a012a1ffd1f1e677f398ac18a1f8297c7ff49ae5374c6` |
| CORE | `CA/calib_tail_readiness_cx2/v006r10_c4/calibration_core_cx2v006r10_c4.py` | `dc895f8a993295b76a42b563893e990d2419432db78485dd387ddc232ff449d6` |
| WRP | `CA/calib_tail_readiness_cx2/v006r10_c4/calibration_orchestrator_cx2v006r10_c4_q5b1.py` | `7a6af535805399d49ec3f1c1cbe9e4911d98f6fae0ad50b69a0641214fcd5d4d` |
| ORC | `CA/calibration_orchestrator_c2/v005/calibration_orchestrator_c2v005.py` | `c75a889ff4646a816329756124a19532cbc166d26f47ce2ea5147b71c2cf7c4d` |
| COORD | `CA/calib_tail_readiness_cx2/DDO154_COORDINATES_CX2V006.json` (CFG L34) | `50e7288e4697c8c8bca0544a4b81b5b15462c10efaed2d437530b95d8a80951f` |
| TPL | `CTRL/specs/CALL_A2_ANCHOR_F10_C2V001.json` (COORD call_spec_mapping.template) | `a93c95b95c1f112b7293ffd598371335227cb93d7334981be33e368c6cd9f52b` |
| RAD | `.../CODEX1/DDO154_COLUMN_MEAN_REFERENCE_BINDING_V001.json` (R11 L242; `query_rows` id and radius only) | `f42c7c657cd9b8bcef6b88e980918ff2570b1fc0a5480784d8bf3b8bb2a3c600` |

**What the text gives S1 (TESTED from bytes).**
- P5 L720 is the only S1 text: "rerun the adopted shape at K=3 and K=4 at the calibrated point before prediction".
- R6 L2139: "S1 transfer across parameter space (V005 S1) unchanged". R11 L489-490 (ADOPT_TAIL next step): "cube K=4 tail-corrected (the C4T configuration) with u_i carried; V005 S1 transfer test at the calibrated point before prediction".
- V6 A142 (L734-744) puts "the S1 registration at u_A" in force by id (L736) and amends R-D15: S1 may overlap the campaign under the machine gate (L742). A133 L478 (V6) gives "the S1 template and launch path" to root workflows with Claude3 reviewing.

## 2. Scope

- S1 exists only if V007 reads ADOPT_TAIL (A133 L5). Otherwise there is no campaign and no S1.
- S1 tests whether the adopted calibration numerics (C4T) give a K3 to K4 increment at u_A within the registered bounds, where adoption itself was measured only at the anchor (P5 L720).
- It is target-free: DDO154 at u_A, DDO154 model speeds only.
- Transfer to every point other than u_A stays UNTESTED; the deciding test is the same pair at that point. In the seed branch (§3) transfer is UNTESTED everywhere.

## 3. Cases and the calibrated point

| Item | Registered | Basis |
|---|---|---|
| Cases | **S1_UA_C3T**: the C3T configuration (cube, tail-corrected, K = 3). **S1_UA_C4T**: the C4T configuration (K = 4). They replace `ROOT_NAMES_AT_REGISTRATION_K3/_K4` (DBP L155-168). | Cases P5 L720; shape and tail R11 L489; configurations CB `cases.C3T`, `cases.C4T`. Names: **CHOICE C5**. |
| Why tail-ON C3T/C4T (A-N1) | R11 L489 adopts "the C4T configuration", and V007 T1 is defined on C2T/C3T/C4T (R6 L1626). Tail-OFF C3/C4 would test numerics that were not adopted, which is not the stricter reading. TESTED from bytes: in CB, C3T and C4T `/numerics` differ only in `composite_grid_spec` (breaks to ±3 vs ±4, 84 vs 96 axis nodes, version); they share the same EPS_CERT_V006 / LO_CERT_V004 slots and `uv_tail_config_sha256` `6d5606ed`. | FORMAL |
| Calibrated point | **u_A** = the engine's `primary_anchor` at budget B_P1, in the order seed, most interior admitted entry, first admitted repair point, most interior pre-march global-design point (A133 L55-59). B_P1 is the number of forward calls before the first call whose family is outside {seed, jacobian, repair, gd_pre} (V6 L600). | FORMAL |
| Bits | S1 runs at u_A's exact theta bits: those of the Phase-1 record (A133 L62-65), equal to the campaign's cache entry (AT-0a). Every physical leaf of both S1 specs equals the Mapper formula of those bits (ORC L2186-2227: `common_scale_s`, `gamma = gamma_over_Eref * Eref_base_J`, `ell_F_m`, `distance_Mpc`), distance fixed at 4.04 Mpc (ORC L160). TESTED: the filler re-derives the leaves from the bits and refuses a one-ulp mismatch (F-F1); its formulas equal the extracted ORC Mapper.build, theta_key and diff_paths and the extracted CORE point_identity (F-P4). | FORMAL; base = the u_A call's own spec bytes is **CHOICE C4** |
| Both phases (C2) | One S1 at u_A serves both phases (A133 L202, in force by V6 L736). If AT-0b finds the Phase-2 primary anchor differs from u_A (A133 L253), S1 is not repeated there by this registration; AT-0b's outcome applies and the difference is disclosed. | FORMAL from A133 L202. Flagged to root under A48: one S1 at u_A is less strict than an S1 at each phase's prediction point. An S1 at a differing Phase-2 point would be a further requirement that must also pass, never a second chance. |
| **Seed branch (AT_ANCHOR)** | u_A is AT_ANCHOR iff its theta bits equal the coordinate spec's `trial_point.engine_seed_theta` on every coordinate, or every mapped physical leaf is within ANCHOR_ALIAS_RTOL = 1e-14 (ORC L155) of the P5 anchor block (P5 L429-436). The seed is item 1 of the primary_anchor order (A133 L55-56), and its physical leaves are the A2 F10 anchor where adoption was measured (P5 L720) up to rounding. TESTED: the seed's leaves differ from the anchor by at most 3.33e-15 relative, so a seed u_A reads AT_ANCHOR (F-P2). In this branch S1 tests reproduction at the adoption point, not transfer; the reading is still computed and still gates step-5 reads (§8). The campaign computes the seed as a real call, because tail-era numerics disable the anchor alias (COORD `call_spec_mapping.numerics`), so K4′ exists (FORMAL). | FORMAL; the AT_ANCHOR definition (bits or alias) is **CHOICE C23** |
| No u_A | On an engine terminal status or NO_IDENTIFIED_DIRECTION (A133 L69-73) there is no u_A; S1 reads NOT_RUN(NO_U_A). | FORMAL |
| K4′ | The campaign's own u_A call. If that call was relaunched under rule (c) (A133 L216), K4′ is the accepted attempt (A-N8). | **CHOICE C3** |

## 4. Per-call spec deltas from the campaign's u_A call

Base = the bytes of the campaign's own call spec at u_A (**CHOICE C4**). The filler checks the base before it builds anything (TESTED, F-F1 to F-F16): galaxy DDO154; `admit` present and `{}` (G11 L216; B-N8); the six theta-mapped physical leaves bitwise; inclination 66; `coefficients` equal to the P5 anchor coefficients pin (P5 V3 L712); label carries `theta <key16>`; numerics, minus the two certificate slots, equal to the campaign config's `numerics.block` (TESTED from bytes: CFG's block equals CB C4T `/numerics` except the certificate slots and the call-spec truncation form `{'shape':'cube'}`); composite grid = CB C4T, last break 4; brackets = the RA4 block (no recovery block exists in the tail era: R6 L1084, CORE Mapper L242); tail ON; both certificate slots are pins whose bytes verify.

| Path | S1_UA_C4T | S1_UA_C3T |
|---|---|---|
| `label` | `S1 transfer test C4T at u_A theta <key16>; base <base_sha8>` | the same with `C3T` |
| `physical`, `coefficients`, `galaxy`, `admit` | byte-equal to the u_A call | byte-equal to the u_A call |
| `numerics` except below | byte-equal to the u_A call | byte-equal to the u_A call |
| `numerics.composite_grid_spec` | unchanged (CB C4T) | CB C3T's block, bitwise |
| `numerics.uv_tail.eps_certificate` / `lo_certificate` | unchanged: `point_identity` excludes the label (CORE L233-238), so the registry returns the u_A point's own records | the records of `point_identity(S1_UA_C3T)`, which differs from u_A's because numerics are in the identity (§13 item 3) |
| driver | r5 `b5cc62af` | same |

TESTED (F-P1): the changed paths are exactly `label` for C4T, and `label`, `numerics.composite_grid_spec.*` and the two certificate slots for C3T; the C4T point key equals the base's; the C3T point key differs. Distinct labels are **CHOICE C5**; both calls compute route A fresh and admit nothing (**CHOICE C8**).

## 5. Statistic

- **Rows:** the 12 registered DDO154 rows (P5 `row_ids`). **tau_i = 0.25 sigma_i** (P5 L729): 0.4, 0.2, 0.175, 0.125, 0.1, 0.05, 0.05, 0.05, 0.075, 0.15, 0.175, 0.325 km/s (P5 L959).
- **Readout:** v_i is the call's own final-pass readout (A134 Q4, V6 L497 and L524), read through the compare-of-record functions (§8).
- **Records:** K3 = S1_UA_C3T, K4 = S1_UA_C4T, K4′ = the campaign's u_A call (§3).
- **Per row:** d_i = v_i(K4) − v_i(K3); d′_i = v_i(K4′) − v_i(K3).
- **Statistic of record:** Dhat_S1 = max over rows of max(|d_i|, |d′_i|)/tau_i: V005's Dhat (P5 L727) on the pair (3,4), V007's statistic (R6 L1059). Worse of the two K=4 records: **CHOICE C3**. Dhat for S1 at all: **CHOICE C6**.
- **Decidability inputs (for TH-2 only):** for a pair P = (a, b), E_i(P) = E_i(a) + E_i(b), where E_i(run) is the compare's Picard bound from the run's own pass rows (R6 L1218: A51 F2 uncapped, A54 S7, A56 N1, NEW-7, with its UNAVAILABLE cases); E^A_i(P) = E^A_i(a) + E^A_i(b), where E^A_i(run) is the last accepted route-A update's per-row effect (R6 L1278), taken from the run's route-A uv_tail record when its `probe_R_m` equals the registered row radii (R11 `check_uvt_record`), otherwise from an EA replay record bound to the run's result sha.
- **Reported, never gating:** Δ4_i = v_i(K4) − v_i(K4′) with a bitwise-equal flag (rerun determinism, UNTESTED anywhere so far); |d_i| in km/s and d_i/v_i (P5 L718); the anchor's own d34_i and u_i first term |v_i(C4T) − v_i(C3T)| from V007's compare of record beside |d_i| and |d′_i|, with |d_i|/u_i (A-N4, B-N10; **CHOICE C20**); max_i |v_i(S1_UA_CkT) − v_i(V007 CkT)|/tau_i for k = 3, 4 (A-B1). The anchor inputs are read only after T0 and only for this report.

## 6. Thresholds

| Id | Clause | Status |
|---|---|---|
| TH-1 | Dhat_S1 ≤ 1 | V005's first numeric clause of `shape_pass` (P5 L726), on the one pair S1 has. **Not subject to decidability** (R6 L1237, L1295). |
| TH-2 | For every row i and each pair P in {(K3, K4), (K3, K4′)}: \|Δv_i(P)\|/tau_i ≤ 1/2, **decidable**, no TINY exemption. Decidable means E_i(P) + E^A_i(P) ≤ tau_i/8 on every row (R6 L1231). E never widens a threshold (R6 L1261). | The form and number of V007 T1_H (R6 L1636, "every row, decidable; no TINY exemption"), applied where the text is silent: **CHOICE C7** |

**PASS needs TH-1 and TH-2 (both pairs decidable and within bound).** The operative per-row bound is tau_i/2: 0.2, 0.1, 0.0875, 0.0625, 0.05, 0.025, 0.025, 0.025, 0.0375, 0.075, 0.0875, 0.1625 km/s [D]. The decidability bound tau_i/8 is 0.05, 0.025, 0.021875, 0.015625, 0.0125, 0.00625 (rows 06-08), 0.009375, 0.01875, 0.021875, 0.040625 km/s [D].

**Why decidability is needed [D] (A-N5).** SV2 lets each call's final Picard pass move by up to 0.0125 km/s, so the difference of two calls can carry 0.025 km/s of Picard change alone, which is the whole TH-2 bound on rows 06-08. Only the decidability rule separates a measured increment from iteration noise.

**Why TH-2 is the stricter reading where the text is silent.** The clauses V005/V007 cannot apply without K=2 are the contraction clause (P5 L726), RA6 (R6 L1626) and T1_H (needs C6T). Applying TH-1 alone would present the computable part of T1 as T1, which A48 forbids. If the anchor's contraction transferred, the remainder beyond K=4 at u_A would be at most |d_i|; TH-2 holds it to tau_i/2, the stricter of the two registered remainder bounds (P5 L726 gives tau_i; T1_H gives tau_i/2). That contraction transfers is UNTESTED; deciding test: C2T at u_A (S1-DIAG).

**Stated now, before any number.** If V007's own anchor Dhat_T(3,4) lies in (1/2, 1], TH-2 is expected to read FAIL_TH2 at a u_A near the anchor although the anchor passed T1. That is a property of the stricter threshold; in the seed branch it follows from V007's own result and carries no transfer information.

**Alternatives not chosen:** (a) TH-1 alone: rejected under A48. (b) C2T at u_A with T1 literally: not chosen because the registered cases are K=3 and K=4 (P5 L720) and the booked runs are 2 (LO2 L89); kept as S1-DIAG. (c) |d_i(u_A)| ≤ |d34_i(anchor)| per row: rejected, because near the anchor it compares two nearly equal increments whose difference is set by E + E^A, not by transfer.

## 7. Validity gates (any failure reads INVALID, never FAIL)

S1 cases are V007 T-cases (R6 L1066, L1084, L1094). Every gate applies to K3, K4 and K4′ (SV-K4′), except where a row says otherwise. The reader computes every row marked "computed" (§8); rows marked "attested" are read from root-bound attestation records (§13 item 6).

| Gate | Requirement | Basis | How |
|---|---|---|---|
| SV0 | FINISHED monitor receipt (receipt `status`, MON L197); `driver_sha256` = r5; `call_spec_sha256` = the registered S1 spec (K3, K4) or the u_A call spec (K4′); the three result directories distinct; per launch, the spec sha registered and the driver sha checked (RI45-13, V6 L565) | FORMAL | computed |
| SV1 | status COMPLETED, `valid` true, exactly the 12 registered row ids with finite speeds; every pass row-set carries exactly the 12 ids (S9; otherwise RECORD_DEFECT); a pass recorded without rows makes E unavailable (B4) | P5 L710; R6 L1066 | computed (R11 `rows_codes`, `pass_rows_ids_code`, `pass_rows_gap`) |
| SV2 | final-pass `max_abs_change_km_s` present, ≤ 0.0125 km/s, and equal to the last pass-row increment | P5 L711, L732; R11 `v2_check` | computed |
| SV3 | normalized numerics minus the certificate slots equal CB's `/numerics` for that K (grid, truncation, picard, brackets, column_workers, route_a and the whole uv_tail content: S8; the key-equivalence map is `[]`, TESTED from CB); last break = K; physical leaves bitwise equal to u_A's; galaxy DDO154; coefficients and certificate slots equal the registered spec's; the route-A tail record's `config_sha256` = `6d5606ed`. P5 V3 binds physical leaves to the REGISTERED anchor block (P5 L712), which a non-seed u_A fails by construction; here they are re-bound to u_A's bits. A seed u_A matches the anchor within 1e-14 (ORC L155) but not necessarily bitwise (ORC L2217). Cross-run: K4′ differs from K4 only at `label`; K3 from K4 only at the §4 paths. | P5 V3, re-bound: **CHOICE C8**; R6 L1066 | computed |
| SV4 / SV5 | final field packet axis equals the registered grid axis bitwise, axis_nodes³ nodes; rows outside the mask exactly zero and the nonzero count equals the mask count | P5 L713-714 | computed (C5 `packet_checks`, pinned) |
| SV6 | no admitted route-A state (S1 admits nothing, so UVT_ADMISSION_MISMATCH cannot arise) | P5 L715; R6 L1094 | computed (`admit` empty) |
| SV7 | tail-era post-run acceptance with the same outcome every tail-ON direct call needs before any value is used: the EPS record of the call's own point (Q8, V6 L499), per-state LO acceptance with the registered ρ record in the LO slot (Q5, V6 L498; reading points L523-528; certificate `source_gas_M_s` = 128), and SRB-ROT ≤ tau_i/10 on the accepted state (Q10, V6 L501) | FORMAL for the LO route: Q5's "all 31 points" includes the 2 POST_S1 calls ([D] 11 + 18 + 2). **CHOICE C9** for the Q2/Q3 enforcement point, whose "29 tail-ON direct calls" (V6 L496) excludes POST_S1 (A-N2). | attested |
| RO1 | the RO1 record of each call checked against the case family's role table (R6 L1094) | FORMAL | attested |
| SV8 | no unruled flag. A flagged test that passes reads INVALID(FLAG_PENDING_RULING): next step "no adoption; root rules on the flag" (R11 L488). A flagged test that fails reads INVALID(UNDECIDABLE_FLAGGED): next step "rerun that case with seed source_rtol/10" (R6 L1777). Flags are evaluated per test (R6 AMB-04): TH-1 sees all three runs; each TH-2 pair sees its two. | R6 L1777, L1796; R11 L488 | computed (route-A uv_tail record) |

## 8. Reading, codes and effects

**Order (FORMAL from R6's outcome order, with A48 where it is silent).** NOT_RUN if any of the three runs has no receipt (or there is no u_A). Otherwise INVALID if any run fails a §7 gate. Otherwise, in this order: FAIL_TH1 (TH-1 fails, unflagged); FAIL_TH2 (a decidable pair fails, unflagged); INVALID(INCOMPLETE_RECORD) (a pair's E^A or E record is missing or defective); INVALID(UNDECIDABLE_FLAGGED); UNDECIDABLE (some pair undecidable, no decided failure); INVALID(FLAG_PENDING_RULING); PASS or PASS_AT_ADOPTION_POINT. A decided failure precedes a record gap because it is the reading less favourable to the model (A48). The reader refuses, and writes nothing, when an input record it needs is absent (an attestation, the fill record, the registration in V006); step-5 reads then stay held as for NOT_RUN.

| Code | When | Label | Step-5 effect | Next step |
|---|---|---|---|---|
| **PASS** | OFF_ANCHOR; TH-1 and TH-2 hold | TESTED-POSITIVE for the K3→K4 increment bound (TH-1, and TH-2 decidable) of the C4T numerics at u_A, at the recorded delta-u. UNTESTED at u_A: contraction (C2T), the K>4 remainder (C6T), K_big and tail implementation (T2/T3). UNTESTED at every other point, including the Phase-2 reference member unless its theta bits equal u_A's; deciding test: the S1 pair at that point. The Phase-2 publication carries this line. | Step-5 values may be read in both phases, subject to every other gate (r3a seal, M-12, A133 §2) | Prediction proceeds; the reading sha is cited in the freeze |
| **PASS_AT_ADOPTION_POINT** | AT_ANCHOR; TH-1 and TH-2 hold | TESTED-POSITIVE for reproduction of the K3→K4 increment at the adoption point. S1 transfer across parameter space is UNTESTED; deciding test: the S1 pair at the first prediction point whose theta bits differ from the anchor. | Phase-1 step-5 values may be read (the text's test has been run at the calibrated point); **Phase-2 step-5 reads stay held until root rules R-S1-1** (§12) | R-S1-1 |
| **FAIL_TH1** | TH-1 fails (decidability does not apply) | TESTED-NEGATIVE: V005's numeric clause Dhat ≤ 1 fails at u_A. Not a physics outcome. AT_ANCHOR: read as a reproduction defect. | Step-5 use stops in both phases: no step-5 value is read for any score and no new step-5 NGC launch is made; in-flight calls finish unread (as A133 L103); the campaign is not stopped by S1 (**CHOICE C12**) | S1-DIAG |
| **FAIL_TH2** | TH-1 holds; a decidable pair fails TH-2 | TESTED-NEGATIVE for the tau_i/2 bound only; transfer is UNTESTED until S1-DIAG. Not a physics outcome. AT_ANCHOR: it follows from V007's own anchor Dhat_T(3,4) and carries no transfer information. | as FAIL_TH1 | S1-DIAG |
| **UNDECIDABLE** | TH-1 holds; some pair is undecidable; no decided failure | UNTESTED | Step-5 values stay unread | R-PAIR once (R6 L1243), branch from the worst undecidable row, through a launch-path successor (§13 item 11). Still undecidable: UNDECIDABLE_AT_ITERATION_FLOOR, reads stay held, root rules. |
| **INVALID** | a §7 gate fails, or a record is incomplete | UNTESTED | Step-5 values stay unread (**CHOICE C11**) | per failing call: (i) monitor or cap stop: the identical spec in a fresh outdir with the cap raised (§10); (ii) bracket miss: BRACKET_HULL_MISS, whose next step is its own registration, with no D7 or W1 widening (R6 L1084; R11 RA4_NEXT L491); (iii) a named defect: "fix and rerun that case under V007 with thresholds unchanged" (R11 AMB16_NEXT L493); (iv) any other FAILED or REFUSED: one identical rerun, and a second identical failure is reported as a deterministic defect for review; SV7 failure: the call's A134 Q5 failure reading governs and root rules before any rerun; flags: SV8 above; INCOMPLETE_RECORD: produce the record (R11 L472). V005 V1(ii), V1(iii) and V3's C2′ path do not apply. |
| **NOT_RUN** | a run has no receipt; or NO_U_A | UNTESTED | Step-5 values stay unread; Phase-1 scoring waits (A133 L188) | launch when admitted (§9-§12) |

**Only PASS releases step-5 reads in both phases; PASS_AT_ADOPTION_POINT releases Phase-1 reads only.** FAIL, UNDECIDABLE, INVALID and NOT_RUN hold them. This is the A48 reading of RI45-04(b)'s "until S1's registered reading is recorded" (RI45 L111): recording a non-PASS code does not release reads (**CHOICE C11**).

**S1-DIAG (the next step on FAIL_TH1 or FAIL_TH2; CHOICE C13).**
1. Run C2T and C6T at u_A's theta bits with the §4 delta pattern (CB C2T, C6T), under a successor registration written before any of their values is read; read V007 T1 and T1_H literally (R6 L1626, L1636) on {C2T, C3T, C4T, C6T} at u_A.
2. NOT_CONVERGED_AT_U_A if T1 fails (next: V005 decision rule 3's K = 5, 6 route under a new prereg, P5 L694); TAIL_REMAINDER_AT_U_A if T1 holds and T1_H fails; INCREMENT_ONLY if both hold.
3. Only for INCREMENT_ONLY may root rule, in a new V6 entry written before any step-5 value is read, that step-5 use resumes. The ruling may not be easier than V007 T1 + T1_H at u_A (A48); the S1 FAIL stays on the record and in every publication.
4. S1-DIAG needs the four 0620 controls and its own launch path; as built, CORE L218-219 refuses every K ≠ 4 (TESTED for K = 3, L-F7).
5. **Seed branch (A-N6).** At a seed u_A, S1-DIAG's C2T and C6T reproduce V007's own anchor cases up to the < 1e-14 physical difference, so its class is fixed by V007's own result up to that rounding. Stated now.
6. **A FAIL before the Phase-1 score (A-N7).** Phase 1 is then not scored while step-5 use is stopped. If S1-DIAG later resumes step-5 use by a ruling written before any step-5 value is read, Phase 2 keeps its score-of-record status (A133 §3's EXPLORATORY trigger is a stop or change after the Phase-1 score, and no target information can have been read), with the FAIL and the resumption disclosed. **CHOICE C21.**

**The reading record** (written by exclusive create by the reviewed S1 reader, `s1_read_c2v001.py`; **CHOICE C19**) holds: the registration, V6, fill-record, spec, K4′ spec, compare and driver pins; the AST digests of every reused compare function; receipts and every gate code per run; per row v_i(K3), v_i(K4), v_i(K4′), d_i, d′_i, Δ4_i (bitwise flag), the tau ratios and d_i/v_i; per pair the E, E^A and (E + E^A)/tau rows, the decidability verdict and any R-PAIR branch; Dhat_S1; the code, sub-code, label, step-5 effect and next step; the flags; the branch record (AT_ANCHOR or OFF_ANCHOR, seed-bits and alias flags, u_A − u_seed per varying coordinate in the engine's u units, the delta from the trial point over the box half-width per coordinate and its maximum, and ln(leaf(u_A)/anchor leaf) for s, gamma, ell_F and distance); and, after T0, the §5 anchor comparisons. Root enters the record's sha in a V6 entry; that entry is the "S1 reading recorded" event (A133 L186; RI45 L111).

## 9. Launch path and the four 0620 controls (built; TESTED on synthetic inputs)

**Path.** S1 launches only through `s1_launch_root_c2v001.py` (this build; to be reviewed by Claude3 and named by root in V6, A133 L478), which runs the guarded step-4 packet (guard011 + launcher012, 0620 L11) for one POST_S1 call per batch. No raw CLI and no unguarded fallback (0620 L11). Outputs go to `/Volumes/External1/Research/UNT_STEP4_RUNS/V007_STEP4_DIRECT_V001/S1_UA_C{3,4}T_<key16>_A<n>` (V6 A124 L283; G11 L268), a fresh directory per call and attempt.

**Order; steps 1-4 run before any process (TESTED: no gate probe and no spawn on any S1-check or control refusal, L-F1 to L-F15 and L-F20 to L-F23; no spawn on any gate refusal, L-F16 to L-F19).**
1. S1 checks: the registration's sha appears in the pinned V6 bytes (S1_REGISTRATION_NOT_IN_FORCE; TESTED on synthetic bytes L-F11 and on the real C2V002/V6 bytes L-F12); launch config (campaign and step-2 route-A state); batch POST_S1 on guard011/launcher012; one call; driver r5; tail ON; the call's spec equals the filled spec, and a template replay from the fill record's pins reproduces its bytes exactly.
2. **Control 4, the r5 allowlist:** guard011 `spec_structure` (L215-223, TAIL_ON_R5_REQUIRED) and `admitted_source` of the driver (L111-112).
3. **Control 1, the sealed V007 ADOPT_TAIL:** guard011 `adoption` (L194-213) inside its fence: SEALED_ROOT_BINDING, SEALED_R5_BINDING, SEALED_ADOPT_TAIL_REQUIRED, REVIEWED_SEAL_TUPLE_PENDING. The adoption pin is the sealed compare's verdict report (V6 L562).
4. **Controls 2 and 3, the step-4 admission and PRELAUNCH/certificate/sensitivity:** guard011 `validate` (L310-362) with native preflight (L227-262) and the replay equality PRELAUNCH_REPLAY_MISMATCH (L352). The admission is root's published record (UNT_STEP4_ADMISSION_PATH/SHA256, as launcher012).
5. Machine gate v003 (§11), then A133's rule.
6. Launch mode only (`--launch --confirm <plan sha> --record PATH`): the pre-launch decision record by exclusive create, then launcher012 (`nice -n 10`, single-thread BLAS, `--execute-root-only`), which re-validates and detaches its worker (L12 L155-164).

**As built, three things stop S1 (FORMAL; each TESTED where marked):**
- **S1_UA_C3T cannot pass control 3.** CORE `validate_block` raises "kept K must be 4" (CORE L218-219), and the wrapper calls it in `certificate_check` (WRP L80) and `prelaunch_check` (WRP L203); ORC also refuses any undeclared normalized path (ORC L156, L2030-2038). TESTED: the extracted CORE clause refuses the C3T spec (F-P1, F-P6), and guard011's own `validate` refuses it on a synthetic admission at native preflight (L-F7). A reviewed core/wrapper successor must accept last break 3 and `numerics.composite_grid_spec` = CB C3T bitwise for S1_UA_C3T only and keep every other `validate_block` clause.
- **No overlap with the campaign.** guard011 L333 requires the admission to attest `campaign_inactive: true` and `step2_route_a_inactive: true`. A truthful attestation is impossible while the campaign runs, so A142's overlap needs a reviewed guard successor (B-N3). The S1 path refuses `campaign_state: ACTIVE` (S1_OVERLAP_NEEDS_GUARD_SUCCESSOR, TESTED L-F13) and any active step-2 route A (L-F22).
- **The S1_UA_C3T point certificates** (EPS record and ρ record for `point_identity(S1_UA_C3T)`, and its certificate-registry entry) do not exist (§13 item 3).

## 10. Caps (per call)

| Cap | Value | Basis |
|---|---|---|
| Wall | 100,800 s, **PROVISIONAL**: the DDO tail-ON constant in force at launch (A140 N4 successor, L3-08 in V6 L911), written into the admission | DBP L158, L163; **CHOICE C17** to follow the successor |
| RSS | 68,719,476,736 B (64 GiB) | DBP POST_S1 caps |
| Output | 85,899,345,920 B (80 GiB) | DBP POST_S1 caps; V6 L653, L906 |

- Caps are value-relevant (A133 L222): a cap stop reads INVALID pending a rerun with the identical spec in a fresh outdir, RSS at RAM (137,438,953,472 B, GATE L85) and the wall doubled (201,600 s [D]); A133 L218's form (**CHOICE C17**).
- **Disk, failing closed.** guard011's `disk_admission` (L299-308) uses the output caps: for a one-call POST_S1 batch, free ≥ 80 + 20 = 100 GiB at batch admission and before the start [D]. A147 L3-01 (V6 L905-911) keeps the campaign guard at the 80 GiB cap; volume planning is root's. Modelled S1 output 11.3 / 43.0 / 115.4 GiB (LO2 L406; UNTESTED).

## 11. Memory admission (built; TESTED on synthetic snapshots)

A142 puts S1 under the machine gate (V6 L742); A147 L3-02 (V6 L913-916) has root take the stricter of the A133 check and the gate. An S1 call starts only when all of these hold (**CHOICE C15**):

1. **Gate v003's own predicates**, called read-only from the pinned gate: `Gate.hold_check()` must read probe_ok and no twin hold (A140 N2; TESTED L-F16, L-F17); then, after the gate's 60 s warm-up, `Gate.decide(owned={}, head=class_from_spec_bytes(spec))` must admit (rules a-i, GATE L49-59). The S1 head is the gate's pooled DDO class: reservation 11 GB, spike 20 GB, growth 5.79 GB (TESTED: 36.79 GB on an empty machine, L-P1). [D]: beside one pooled route-A tree with counted footprint C, d1 needs C ≤ 20.41 GB; beside two, the route-A cap of 2 refuses. TESTED: refused with MEMORY_HARD at 92.58 GB beside one 30 GB route-A tree (L-F18).
2. **A133's root rule** (A133 L114-117): measured run footprint (the gate's own snapshot, the A130 metric) + 29.1 GB S1 term (A133 L123's 27 GB in consistent units; B-N5) + 29.1 GB campaign reserve (V6 L669) ≤ 103 GB. An unknown footprint refuses (TESTED L-F19). [D]: whenever every footprint is known, the gate's d2 (counted + 11 + 20 ≤ 72) already implies this rule (41 < 44.8 GB).
3. **launcher012's own ramp**: `memory_pressure` free ≥ 25 % (L12 L35-36; DBP route_a_admission, max_active 1).
4. **Concurrency and order (B-N2; CHOICE C14).** One S1 call per POST_S1 batch, so each S1 head meets the gate at its own start; launcher012's machine lock (L12 L52-59) then runs the two calls serially. If a reviewed overlap successor exists: start an S1 call only at the start of a single-call campaign wave or with no campaign head pending (A133 L346). The gate counts an S1 tree as pooled route A, so a campaign head can be refused while S1 is in route A; that contradicts A133 L124 ("never waits") and is disclosed whenever it happens. After FINAL_SUMMARY, S1 goes ahead of the step-5 queue (RI45 L254-255).

## 12. Timing and root items

| Moment | Rule | Basis |
|---|---|---|
| Registration in force | Entered in V6 by sha **before T0** (before the V007 compare of record is run or any step-2 T value is read), and in no case later than H2. If T0 comes first, this text is entered unchanged and the order is disclosed. Any edit after T0 is a new version labelled post-result. | A133 L184 (§2 row 0); V6 A142 L734-744; B-B2. **CHOICE C1** only for "before T0" |
| Earliest S1 start | when u_A is fixed (A133 L55-65); expected Tue 20 Oct 22:17 CDT (A133 L290, L301) | FORMAL |
| As built | S1 can start only with the campaign inactive (§9), so not before FINAL_SUMMARY, and S1_UA_C3T not at all until the core/wrapper successor and its certificates exist. Then the Phase-1 read deadline (Sat 24 Oct 09:00 CDT, A133 L186) cannot be met and Phase-1 scoring waits (A133 L188). | FORMAL |
| Duration | 5.20 h E / 8.76 h U per call (LO2 L309); serial (§11 rule 4) 10.40 h E / 17.52 h U [D, UNTESTED] | LO2 L309 |
| Reading recorded | before any Phase-1 NGC value is read (A133 L186) and before any step-5 output value is read (RI45 L111, option (b)) | FORMAL |

**Root items, each to be ruled before u_A is fixed (so no data can inform them):**
- **R-S1-1 (seed branch, A-B1/B-B3).** If u_A is AT_ANCHOR, does PASS_AT_ADOPTION_POINT release Phase-2 step-5 reads? Default registered here (A48): no; Phase-2 reads stay held. Recommended: register now S1-B, the same pair, statistic, thresholds and reading at the first Phase-2 member whose theta bits differ from the anchor (2 more calls). The alternative is to rule that PASS_AT_ADOPTION_POINT releases both phases under A133 L202 with the UNTESTED line published.
- **R-S1-2 (C2 under A48).** One S1 at u_A for both phases is root's choice (A133 L202), less strict than an S1 at each phase's prediction point. Root confirms it or registers the further S1.
- **R-S1-3 (successors on the Phase-1 critical path).** The guard successor for overlap and the core/wrapper successor for K = 3 (§9), each with its own MUST_FAIL tests, decide whether S1 can be read before Sat 24 Oct.

## 13. Open (UNTESTED unless marked)

1. **Overlap guard successor** (G11 L333). Deciding test: its own MUST_PASS (S1 admitted with the campaign active under the S1 overlap attestation) and MUST_FAIL (every other batch still needs `campaign_inactive: true`).
2. **K = 3 core/wrapper successor** (CORE L218-219; WRP L80, L203; ORC L156). TESTED as-built refusal (L-F7). Deciding test: the successor admits S1_UA_C3T and still refuses K = 2, 5, 6 and any other grid.
3. **S1_UA_C3T certificates.** EPS record and ρ record for `point_identity(S1_UA_C3T)` and a certificate-registry entry (WRP `certificate_check` looks up the registry by that digest). Whether the u_A point's EPS record (coverage [2, 91], V6 L944) already covers K = 3, and whether EPS enters v_i at all (A136: it is used numerically in `_eps_per_shell`, `field_bound`, `srb_rot`; B-N4), are UNTESTED. Deciding test: the C3T spec through the reviewed certificate check, and a synthetic check of `_eps_per_shell` against the speed rows.
4. **`sensitivity_gate` on a K = 3 spec** (G11 L251). Deciding test: the same synthetic preflight after item 2.
5. **E^A for S1.** The reader takes E^A from the route-A uv_tail record (`E_A_rows_km_s_accepted` with `probe_R_m` = the registered radii) or an EA replay record bound to the result sha; without either the pair reads INCOMPLETE_RECORD (TESTED R-F19). Deciding test: the first real S1 record carries `probe_R_m`.
6. **Attested gates (SV7, RO1).** The reader needs one `UNT_S1_GATE_ATTESTATION_C2V001` record per run and gate, bound to the result sha with producer and evidence pins (**CHOICE C22**). Adapters from acceptance_q2 v004 (V6 L849-857) and the RO1 role-table check to this record are unbuilt. Deciding test: both adapters on the first real S1 records.
7. **Compare of record r14** (`f3f9ba7e`, V6 A116-A117). The reader loads the compare named in its manifest and records an AST digest of every reused function; it was tested on r11 (`a5d10cb1`). Deciding test: the digests on r14 equal r11's, or the differences are reviewed. Separately, R6 L3 reads "NOT SEALED": the SEAL_RECORD (`a9646fe3`, V6 L302) is the authority on sealed status (V6 RI-35).
8. **Wall cap** PROVISIONAL until the A140 N4 successor.
9. **Rerun determinism of a tail-ON parallel8 DDO call.** The Δ4 report measures it at no cost.
10. **Contraction at u_A.** Deciding test: C2T at u_A (S1-DIAG).
11. **R-PAIR for S1 pairs** needs a launch-path successor (PICARD members admit their base's route A with column_workers 1, passes 12 and bound 0.0025; ROUTE_A members use seed_source_rtol_factor 0.1; R6 L1243) and a reader successor that reads the members. Until then UNDECIDABLE reads RPAIR_PENDING.
12. **u_i carried** (R11 L489). Whether the u_i used downstream should be the larger of the anchor's and u_A's |v(C4T) − v(C3T)|. Deciding test: read where r3a and step 5 consume u_i.
13. **The reader on real records.** Its input side follows R11 `read_run` and the driver's result layout (FORMAL). Deciding test, after T0: run the input side on V007's own step-2 C3T/C4T records; it must reproduce the compare of record's d34_i, E and E^A for that pair.
14. **Production disk admission** (guard011 `disk_admission` on External1) was not exercised (tests may not touch External1). Deciding test: root's dry plan at T0 on the real run root.

## 14. CHOICES (not forced by text)

| Id | Choice | Reason |
|---|---|---|
| C1 | In force before T0 | Stricter than "before the campaign result is read" (INV L4073) and blind to every T value; the registered deadline is H2 (A133 L184), which this does not move |
| C2 | (FORMAL now) one S1 at u_A for both phases | A133 L202, in force (V6 L736). Flagged under A48 as R-S1-2 |
| C3 | K4 is a fresh run; the statistic also takes K4′ (the accepted campaign u_A call); the worse of the two counts | Keeps the 2 booked runs; the max over both K=4 records is stricter, and turns a determinism check into a strictness term |
| C4 | The S1 specs are derived from the u_A call's own spec bytes | Bit-identity with the u_A call for every leaf the registration does not change |
| C5 | Case names S1_UA_C3T and S1_UA_C4T; a distinct label | Custody separation from the campaign record; the label is outside `point_identity` (CORE L233-238), so no certificate lookup changes |
| C6 | The statistic is V005 Dhat on the pair (3,4) | The only registered statistic computable from the two named cases (P5 L727; R6 L1059) |
| C7 | TH-2: every row ≤ tau_i/2, decidable, no TINY exemption | The T1_H form (R6 L1636) on the only remainder proxy at u_A; stricter where the text is silent |
| C8 | V3's physical binding re-bound to u_A's bits; V6 vacuous (no admission) | P5 V3 binds the anchor block, which fails every non-seed u_A by construction |
| C9 | SV7 applies to S1 | FORMAL for the LO route (Q5's 31 points); a choice for the Q2/Q3 enforcement point (29 calls, V6 L496) |
| C11 | Only PASS releases step-5 reads in both phases; PASS_AT_ADOPTION_POINT releases Phase 1 only | A48 reading of RI45 L111 |
| C12 | On FAIL: no new step-5 launch; in-flight calls finish unread; the campaign continues | "stops step-5 use" (RI45 L111) names step 5 only; kept outputs can be re-bound (A133 L203) |
| C13 | The FAIL next step is S1-DIAG | RI45 L111 needs a registered next step and none exists; it uses only registered tests |
| C14 | One S1 call per POST_S1 batch (serial); S1 ahead of the step-5 queue after FINAL_SUMMARY; with an overlap successor, start only at a single-call wave start or with no campaign head pending | Each S1 head meets the machine gate (A142); timing only, so A48 does not apply; costs about 5 h E against a 2-call batch |
| C15 | Memory: gate v003's hold_check and decide, then A133's rule with the 29.1 GB S1 term | The conjunction of every rule that claims S1 (A142; A147 L3-02) |
| C16 | Start windows after FINAL_SUMMARY or (with an overlap successor) at single-call waves; case order not fixed | A133 L346 gives single-call waves; order changes no value |
| C17 | The wall cap follows the successor constant; a cap-stop rerun uses RSS at RAM and doubles the wall | A133 L218's form; caps are value-relevant (A133 L222) |
| C19 | The reading is computed by the reviewed reader and recorded by exclusive create; root enters its sha in V6 | Makes "recorded" (A133 L186) a checkable event |
| C20 | The anchor comparisons and \|d_i\|/u_i are reported and never gate | A gate on them is undecidable near the anchor (§6 (c)) |
| C21 | After an S1 FAIL and an S1-DIAG resumption ruled before any step-5 value is read, Phase 2 keeps its score-of-record status, with disclosure | A133 §3's trigger is a stop or change after the Phase-1 score; no target information can have been read |
| C22 | SV7 and RO1 enter the reader as root-bound attestation records | Their producers exist outside this build; the reader binds each record to the result sha and verifies producer and evidence pins |
| C23 | AT_ANCHOR = seed bits equal, or every mapped leaf within 1e-14 of the anchor | Covers the seed and any other u_A at the adoption point up to rounding; the broader definition labels more readings as reproduction, which is the less favourable reading |

There is no C10 (flags now follow R6 AMB-04, FORMAL) and no C18.

## 15. Disclosures

- **Reads.** The prompt's named files and files cited by explicit path in them: C2V001, P5, R6, R11, C5 (R11 L171), CB (via `python3 -I -B`, C3T, C4T and the top-level keys only; C5H never accessed), A133, V6 (the only NGC3198-named file opened; read in parts, last at `8b8356c6`), RI45, LO2, INV, RFC (lines cited by C2V001), 0620, DBP, GATE, CFG, G11, L12, B10, MON (receipt fields), CORE, WRP, ORC, COORD (CFG L34), TPL (top-level keys and `admit`), RAD (`query_rows` id and radius only). DRV and the README of sched v003 were hashed, not read. A non-recursive `ls` was run on `s1_path_c2/` and on `step4_launch_packet_cx1/impl/`.
- **One print to disclose.** A structure listing of COORD printed the first 400 characters of its `ngc3198_nuisance_slots` block: NGC3198 distance and inclination placeholder boxes (model nuisance slots). No velocity or rotation-curve value was printed or read.
- **Not opened:** V5F (the A48 text is quoted from C2V001), run trees, External1, `~/.codex`, `c5h_hull_c2/`, `UVT_*`, `v003g/slots/`, any NGC3198 target file.
- **Commands.** Every grep was single-file; no recursive search. Python ran as `python3 -I -B` (the codex-runtime interpreter that launcher012 names, because `/usr/bin/python3` has no numpy); the synthetic suite peaked at about 240 MB RSS.
- **Writes and deviation.** This file and the s1_path_c2 build were composed and iterated in this session's private scratchpad (`/private/tmp/claude-501/...`), outside the UNT tree, then created in `s1_path_c2/` by exclusive create. That scratchpad work is a deviation from "write only inside s1_path_c2/"; it touched no UNT file.
- **C2V001's lane** reported that it opened V5F, an NGC3198-named file. Under this lane's rule that is a deviation; recorded here at A-N9/B-N11's request.
