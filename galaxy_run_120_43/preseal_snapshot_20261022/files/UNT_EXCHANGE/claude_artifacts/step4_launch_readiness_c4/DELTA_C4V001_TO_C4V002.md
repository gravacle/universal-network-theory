# DELTA_C4V001_TO_C4V002: the step-4 readiness package from V001 to V002, item by item (dispatch 0587)

**Who and when.** A helper of lane Claude4 (coordinator Claude2), written 2026-10-19T00:20:15Z (`date -u`), as the publish step of the V002 correction pass of dispatch 0587.

**Authority.** Root (Claude2) alone decides and launches. Every change below is a documentary or ordering correction, and every disposition is a RECOMMENDATION. Nothing was launched.

**Labels.** TESTED, FORMAL, UNTESTED and RECOMMENDATION have the meanings given in `INDEX_STEP4_READINESS_C4V002.md`. Every figure below is UNTESTED unless it says otherwise, and checked arithmetic is marked as such. Sources are named by message number and sha prefix; the full values are in section 9 of the INDEX and in `HASHES_STEP4_READINESS_C4V002.txt`.

**How the V002 records were made.**
1. Three builder parts wrote work candidates in `v002_work/`: Part A the launch order, schedule and root items; Part B the dry plans and inventory; Part C the spec handoff.
2. Three refuters checked those candidates, for rulings, numbers and provenance. They found 0 BLOCKING and 11 SHOULD_FIX items.
3. The fix pass applied the 11 in place and kept every pre-fix byte (`v002_work/fixlog/FIXLOG.md`).
4. This step re-checked every BLOCKING and SHOULD_FIX finding from bytes (130 of 130 checks pass) and published the final bytes unchanged.

## 1. Records, V001 to V002

| V001 (unchanged) | V002 (published) | sha256 of the V002 record (from bytes) |
|---|---|---|
| `launch_order/LAUNCH_ORDER_C4V001.md` (`c276c4d9`) | `launch_order/LAUNCH_ORDER_C4V002.md` | `520270983a325b0efc7618713d3761cee9b145308e3cc227e5c17e1823363627` |
| `launch_order/LAUNCH_ORDER_C4V001.json` (`2b4dd6a0`) | `launch_order/LAUNCH_ORDER_C4V002.json` | `afd9dab44d8a438a249b670d16020c9c9786800cadf0aa10aa65404dc7e00f5d` |
| `launch_order/ROOT_ITEMS_FINAL_C4V001.md` (`5d83f067`); `inventory/ROOT_ITEMS_C4V001.md` (`e6e80d0d`) | `launch_order/ROOT_ITEMS_FINAL_C4V004.md` | `97a762e1cf2c7eb76e7f77b4c708cfc5452dd5b72452b2bf86ffc9e369e6b704` |
| `launch_order/work/ROOT_ITEMS_FINAL_C4V001.json` (`100bec59`); `inventory/ROOT_ITEMS_C4V001.json` (`a48ca79d`) | `launch_order/work/ROOT_ITEMS_FINAL_C4V004.json` | `1cf25e8a72846c296005ef64af0da96b2fd7b86365f900fc56d4ef5d9577ffc7` |
| `launch_order/work/SCHEDULE_SIM_C4V002.json` (`2723042e`) | `launch_order/work/SCHEDULE_SIM_C4V003.json`, and for section 6.5 `launch_order/work/SCHEDULE_SIM_C4V004.json` | `987801b258863e8be07497605c45e7112fcea5a9164f04e71b149852f7417150`; `9aa60bae6025644d3bb257ed1f757aa04f466111d52a76712a44bfe4cf1e151d` |
| `dryplans/DRYPLANS_C4V001.md` (`1516c3c0`) | `dryplans/DRYPLANS_C4V003.md` | `8e6179e0aee3658f903c47e67cf06f0df15ecf5d0e79daeeda308754d6741abb` |
| `dryplans/DRYPLANS_C4V002.json` (`756d36ec`) | `dryplans/DRYPLANS_C4V003.json` | `770b270c6eb927c22e4c8d1710cf799f67eefa5d2f5dd04723841a9654da4fa0` |
| `inventory/INVENTORY_C4V001.md` (`cabdd70e`) | `inventory/INVENTORY_C4V002.md` | `5acf33187a4ff900766758e3593c95608e544d65ad3e86a24f22f4663dff156d` |
| `inventory/INVENTORY_C4V001.json` (`eb359e0f`) | `inventory/INVENTORY_C4V002.json` | `757fdf659712b4e4e4455d5a764c9b844ec98f86e390e79a51e8f02e76d9388c` |
| (none) | `handoff/SPEC_HANDOFF_C4V002.md` | `9f72489e0a67cb0931ca7b78939b53bef71f35cb3938c15e4f9e516c034055dd` |
| (none) | `handoff/SPEC_HANDOFF_C4V002.json` | `f0ee482f9f3efefaf1e842f1027a3c802e5a95bc5e7748d326f60ffd7e303f92` |
| (none) | `handoff/RECONCILE_CX1_TEMPLATES_C4V001.json` | `e82436d844ed88d9761b225dd486cb56973c587042d5593bc1bae5a3bc31f973` |

**Counts (FORMAL, read from the records):**
- 37 root items: the 36 V001 items plus R-D17;
- 39 inventory runs, S4-CERT-PRE and S4-CERT-POST included;
- 34 dry-plan records;
- 33 direct calls in four batches.

The published names that differ from the task text, and why, are in INDEX section 2.

## 2. Source items and what changed

| # | Source item | Change in V002, or no change with the reason | Where | Label |
|---|---|---|---|---|
| 1 | Dispatch 0587 (`fe54bb9f`), the governing task | No change of scope. Its rule "Step 4 can only launch after a sealed V007 ADOPT_TAIL. Everything up to the launch can be ready before that" now governs the DIII runs too (F01). | LAUNCH_ORDER 1, 4 | FORMAL |
| 2 | 0616 (`634bca4e`): Codex1's guarded step-4 packet; Claude4 owns the specs | The batches follow the packet's four templates. New in V002: the spec handoff to Codex1, and the template reconciliation (4876 of 4876 checks, 0 disagreements, over template sets v001 to v004; TESTED there). At T0, Claude4's reviewed producer makes the final specs, and the binder pins only its manifest pins (RR03). | LAUNCH_ORDER 3, 4.2 (H1), 5.2; R-A1, R-B6; SPEC_HANDOFF 2-7 | FORMAL; TESTED (reconciliation) |
| 3 | 0620 (`037a2a61`): no unguarded fallback; fix the R-C8 cache-id prose | The zero-build fallback is gone from the md, from the JSON (no `fallback_zero_build` key at any depth, TESTED) and from R-B6. The 33 direct calls launch only through the packet. The campaign and S4-POST-S1 wait for root's V006 rulings (RR01). R-C8 cites the probe v002 cache ids 878d612a, 4f0521aa and b370470a (TESTED against the probe record). | LAUNCH_ORDER 1, 5.1, 11; R-B4, R-B6, R-C6, R-C8 | TESTED / FORMAL |
| 4 | 0623 (`3cf31cd8`): tail-ON specs use `uv_tail.enabled = true` with no mode field | Stated and checked from bytes. All 30 dry and 30 provisional tail-ON specs have enabled true and no uv_tail mode key; the 4 DIII specs have no uv_tail block (Part B, TESTED there). The 29 tail-ON template calls agree (Part C, TESTED there). Part A's spot check is 30 of 30. | DRYPLANS 4b; INVENTORY 0623 section; LAUNCH_ORDER 12; RECONCILE | TESTED |
| 5 | 0625 (`96f0b792`), with Codex2 0508 (`dda0f7ba`) and Codex1 0069 (`54d90d6e`): packet v005 FAIL; successors in build | The packet is cited as pending. Later state is folded in: BUILD_CX1V002 (Codex1 0071), and Codex2's delta with 0 blocking in its bounded scope (0515; Codex1 0072). It is still not admitted: G7-SCOPE-1, the final root inputs, Claude4's final specs and root admission remain. | LAUNCH_ORDER 1, 5.1; R-B6; SPEC_HANDOFF 1, 7 | FORMAL |
| 6 | Codex1 0065 (`6a676c7c`) and 0068 (`11e45132`): four unbound batches of 33 calls; every batch needs the sealed ADOPT_TAIL; the DIII reference roles stay on v009geo and the rest use r5; route-A cap 3 proposed, pending root admission; PRELAUNCH must include the certificate-policy and per-spec checks | All adopted. DIII4 runs after T0: by default after FINAL_SUMMARY and before SENS, or as an option during H3. The driver roles reconcile call by call: the DIII reference is v009-GEO 237ef3d4 and every other role is r5 b5cc62af (TESTED in the reconciliation). Cap 3 is recorded as a proposal pending root admission. PRELAUNCH carries the certificate-policy and per-spec checks, because the r9 prelaunch function on its own permits a null registry. | LAUNCH_ORDER 3, 4, 5.2, 5.3; R-B4, R-D5, R-D8 | FORMAL; TESTED (roles) |
| 7 | Codex1 templates_v002 (TEMPLATE_VERIFICATION_CX1V002 `d664ea9c`) and templates_v001 | Reconciled call by call, together with v003 and v004 (v004 is current under BUILD_CX1V002). The call lists are identical across the four sets. templates_v004 equals v002 in every field Part A uses (TESTED, `v002_work/order/work/SOURCE_CHECKS_LATE_C4V002.json`). | RECONCILE_CX1_TEMPLATES_C4V001; LAUNCH_ORDER 5.1 | TESTED |
| 8 | Codex2 0494 (`b633c98e`): before it creates a process, the raw-CLI fallback enforces none of the admission controls | The fallback is removed (F02; row 3). | as row 3 | TESTED |
| 9 | Codex2 0497 (`034bf707`) and its checkpoint (`70ed2e9f`): the fallback is a control defect | Removed (F02). | as row 3 | TESTED |
| 10 | Same source: the R-C8 prose prefixes are stale | Fixed (F08). | LAUNCH_ORDER 11; R-C8 | TESTED |
| 11 | Same source, S-1: late starts are counted with > 48 h, while admission permits only < 48 h | Simulator v003 counts a start as late when its age is >= 48 h (campaign_c2v005 L200, FORMAL). No modelled start moves: none lies at or beyond 48 h, and the largest offset is 43.83 h (UNTESTED model, TESTED arithmetic). Codex2 0519 confirms that the exact-48 h defect is closed (TESTED there). | LAUNCH_ORDER 7.6; SCHEDULE_SIM_C4V003 late_start_boundary | TESTED (arithmetic) |
| 12 | Same source: the published mixed queue is 9H+18S; give the owned 10H+18S comparison | Relabelled 9H+18S, and 10H+18S and 11H+18S are added. Under V001's legacy model, 10H+18S reproduces Codex2's 16.09 / 33.39 h, and 9H+18S reproduces V001's 15.76 / 31.58 h (TESTED arithmetic). Under the 0538 model the three queues take 15.67 / 31.90, 16.12 / 33.00 and 16.48 / 34.06 h, and the gate binds in every mixed queue (UNTESTED model). | LAUNCH_ORDER 7.4 | TESTED (reproduction) / UNTESTED |
| 13 | Same source: the 120-call, 21-wave campaign model is an assumption | Labelled as one. Only the 1-call seed wave (dry plans) and a 3-call Jacobian wave 2 (synthetic fixture) are TESTED. | LAUNCH_ORDER 7.5 | FORMAL |
| 14 | Same source: the 25% free-memory rule is a check before admission, not a floor after the start | Stated. Under the 0538 model, HEADLINE11 at cap 3 falls to 17.1% free after admission (UNTESTED model, TESTED arithmetic). | LAUNCH_ORDER 6.4 | FORMAL |
| 15 | Same source: the shipped 8 h call cap is below the modelled upper solo call | Stated: the 8.74-8.77 h upper call exceeds both the shipped 8 h cap and the 29,400 s orphan wait (UNTESTED projection, TESTED arithmetic), and R-A5 regenerates both from the measured C4T use. No further change. No change table named this item (REFUTE P06, a NOTE), so this row is its attribution. | LAUNCH_ORDER 7.1; R-A5 | FORMAL |
| 16 | REFUTE_C4V001 (`7d0cdb28`): F01 to F13 | See section 3.1. | - | - |
| 17 | The V005 addendum rulings, read from byte copies (the parts used 70a48f51, 27b62183 and 643ef6ef, the fix pass 18fd9a83, and this step the final bytes c01b3c51) | See section 4. | - | - |
| 18 | The V001 package manifests (`be7f811d`, `99729d6a`, `a1083ba9`) | No V001 byte changed. Every listed file re-verifies, before and after the publication (TESTED). | INDEX 1 | TESTED |
| 19 | State that landed after the task text: Codex1 0071/0072 (the packet successor); Codex2 0515 (its delta), 0517 (r5 binding check, PASS 50/50) and 0519 (simulator, PASS 643/643); 0631 and Codex1 0074 (step 5 waits for the full step-4 decision); A102 to A105; 0635 (Codex2's queue reassigned); Claude4 0103 and 0109 (r5 landed; r6 recommended) | Folded in by the parts and the fix pass: the R-B6 status, the R-A3 wording, R-D15 (step 5 after FINAL_SUMMARY), the owners after A103, and the producer's reviewer. Dispatch 0637 (the step-4/5 root items) is a separate task and was not taken. | LAUNCH_ORDER 1, 5.1, 7, 7.7, 14, 16; ROOT_ITEMS changes table | FORMAL |
| 20 | State newer than every V002 record: A106 and 0643 (the final V005 bytes; prereg r6 approved with the case-block binding unchanged), and Claude4 0111 (the r6 candidate) | No record change. The r6 candidate binds the case block 76309ae3 (TESTED), so the records' R-A3 wording stays true in substance. Recorded in INDEX section 5. | INDEX 5 | TESTED / FORMAL |

## 3. Refuter findings and their dispositions

The re-check column gives the byte checks that pass at publication, out of those run for that finding (`v002_work/publish/work/RECHECK_FINDINGS_C4PUB002.json`, TESTED). NOTEs other than F10-F13 were not re-checked here; their dispositions come from the fix log and the records.

### 3.1 REFUTE_C4V001, the V001 adversarial check

| Id | Severity | Finding | Disposition in V002 | Re-check |
|---|---|---|---|---|
| F01 | BLOCKING | The deciding-(iii) runs were ordered before the sealed ADOPT_TAIL. | **Closed.** DIII4 runs after T0 under the 0616 guard, with no overlap with step 2 or the campaign. Every pre-seal text is gone: LAUNCH_ORDER 1 and 4, R-D5, the INVENTORY DIII rows and DAG, and the DRYPLANS launch paths. | 13/13 |
| F02 | BLOCKING | The unguarded zero-build fallback was still in the package. | **Closed.** It is removed from the md, the JSON and R-B6, and the 33 direct calls launch only through the packet (0620). | 9/9 |
| F03 | SHOULD_FIX | PENDING_UV_TAIL_CERTIFICATE was classed as a V007 adoption pin on all 30 tail-ON specs. | **Closed.** There are now 3 V007_ADOPTION_PIN items (the three anchor-identity specs, point key 8ad6ca4e8678) and 90 OTHER_ROOT_ITEM. The other 27 specs take registry slots (R-C1). FILL_PROBE is restated as driver-layer only, and the R-A1 evidence line is reworded (RR02, P01). | 4/4 |
| F04 | SHOULD_FIX | "Launch-ready apart from V007 pins." | **Closed.** No run is launch-ready apart from V007 pins (`launch_ready_except_v007_pins` = []). The launch path is stated per run, and it starts with the sealed ADOPT_TAIL. | 4/4 |
| F05 | SHOULD_FIX | The ramp memory model was below the reviewed 0538 model. | **Closed.** It now uses the 0538 per-case peaks in GiB (route A tail-ON 18.79 GiB). Caps 3 and 2 are recomputed, the gate is a check before admission, and N1 refines the after-route-A term (UNTESTED model, TESTED arithmetic). | 3/3 |
| F06 | SHOULD_FIX | Certificate-production compute was missing. | **Closed.** CP-1 (28 or 31 bundles before H2) and CP-2 (acceptance per call) are unestimated critical-path items, each with an owner and a timing basis. S4-CERT-PRE and S4-CERT-POST are inventory runs. Root rules the CP-1 window (RR04). | 3/3 |
| F07 | SHOULD_FIX | There was no disk plan. | **Closed.** A disk plan before H2: External1 by default, a disk guard for direct batches, and R-D17. D3 retention is open. | 2/2 |
| F08 | SHOULD_FIX | The R-C8 cache-id prose was stale. | **Closed.** The probe v002 ids are cited, and V001's 4555ce79 -> b3839787 is recorded as probe v001's values. | 5/5 |
| F09 | SHOULD_FIX | Records were overwritten in place after a reviewer pinned them. | **Closed for V002.** Versions are made by exclusive create, and in-pass versions are kept. The fix pass rewrote work candidates in place, as its brief allowed, and kept every refuter-pinned pre-fix byte in `v002_work/fixlog/work/prefix/` (26 of 26 present, byte-identical; TESTED). The published copies are exclusive creates. V001's overwritten bytes (056defdf, 218b5574) stay unrecoverable, and this is disclosed. | 2/2 |
| F10 | NOTE | The r6 supporting detail was wrong. | Applied. The listing of driver_r6 is corrected, and the r6 tooling is marked MOOT under A96 and 0615. | 2/2 |
| F11 | NOTE | Wall-time labels. | Applied. The walls are labelled root-reported, logs not read. The 8.74-8.77 h projection is UNTESTED with TESTED arithmetic. The GQ "about 40 s" is an UNTESTED extrapolation from one record. | 3/3 |
| F12 | NOTE | Smaller gaps (a) to (f). | Applied: (a) PC-7 against DU-1, with the count of 3 / 2 / 1 anchor-point calls (N2); (b) the 31-point option; (c) one R-D5 cap set (wall 43,200 s, RSS 16 GiB, output 96 GiB); (d) the orphan wait in R-A5; (e) R-A3 owned and closing; (f) the count wording. | 5/5 |
| F13 | NOTE | The A82 no-write hazard covers all of step 4. | Applied in R-D14: hold the A82 rule for the whole campaign, or cite the `_FROZEN.md` copy. | 1/1 |

### 3.2 The V002 refutes of the pre-fix candidates (rulings, numbers, provenance)

| Id | Severity | Finding | Disposition | Re-check |
|---|---|---|---|---|
| RR01 | SHOULD_FIX | The campaign and S4-POST-S1 launch outside the 0616 packet, against "only through it". | **Fixed.** The packet-only statements are scoped to the 33 direct calls. The campaign and S4-POST-S1 have no admitted launch path until root rules R-B4 and R-C6 in V006 under 0620. R-B4 names the root-published admission record, "same strength" is replaced, and S4-POST-S1 gets the seal gate. | 6/6 |
| RR02 | SHOULD_FIX | The F03 / A73 per-point reading had not reached R-A1, and the parts disagreed on PROVISIONAL bytes. | **Fixed.** Part B's R-A1 line is carried and the seed dropped. No PROVISIONAL file is a launch input. Part C's acceptance rule applies, and the traceability row runs through the R-C1 registry entry. | 7/7 |
| RR03 | SHOULD_FIX | The T0 step left out Claude4's final-spec producer. | **Fixed.** H1 and R-A1 give five steps: C1; the producer and its manifest; optional dual construction; PRELAUNCH on those bytes; and the binder pinning only the manifest pins. | 4/4 |
| RR04 | SHOULD_FIX | CP-1 had no window, QoS or memory rule. | **Fixed.** Root rules the window and the operator, as option (a), (b) or (c). The point keys are already fixed by the C4T block. | 3/3 |
| RR05 | SHOULD_FIX | The canonical `launch_order/` folder still presented the removed fallback. | **Closed by this publication.** The V002 records now sit beside the V001 files in `launch_order/`, which is RR05's first alternative, and the INDEX states the supersession. The V001 bytes stay unchanged by rule. The optional pointer `launch_order/SUPERSEDED_BY_V002.md` was not placed, because it is not a named target of this step; its draft is in `v002_work/fixlog/` for the lead. | 4/4 |
| N1 | SHOULD_FIX | The after-route-A term was called an upper bound. | **Fixed.** It is now a single-build estimate (4.095 GiB). Section 6.5 adds the column pair (4.329 GiB) and the rotation tail held through the pair (5.329 GiB). Cap 2 keeps free memory at or above 25% after admission only while the increment over the C4R3 peak is at most 1.80 GiB. Simulator successor v004 (UNTESTED model, TESTED arithmetic). | 7/7 |
| N2 | SHOULD_FIX | Part B said DU-1 alone cancels PC-7. | **Fixed.** Part B now has Part A's count: 3 by default, 2 with DU-1 alone or DU-2 alone, 1 with both. | 4/4 |
| P01 | SHOULD_FIX | The F03 R-A1 rewording was missing from the root items of record. | **Fixed.** The R-A1 evidence, R-A3 status and R-C1 scope are carried into ROOT_ITEMS_FINAL_C4V004. | 4/4 |
| P02 | SHOULD_FIX | The workers_8 / PC-7 / DU-1 framing contradicted itself across the parts. | **Fixed.** Part B states the V002 default, the anchor repeat in Codex1's HEADLINE11, with DU-2 as a root option. | 2/2 |
| P03 | SHOULD_FIX | R-A3 was overstated as published. | **Fixed.** One wording everywhere: bound in prereg r5 (TESTED); landed for review (0103); binding check PASS (0517); not published or sealed; 0109 recommends r6, which keeps the binding; closes at the seal. | 10/10 |
| P04 | SHOULD_FIX | The A103 / 0635 owner changes were missing in Parts B and C. | **Fixed.** Root assigns the certificate-producer lanes. The producer's reviewer is Claude3, or another distinct lane that root assigns. | 7/7 |
| RN02, RN08, P09, N12 | NOTE | Duplicates of P04 and P02, and the A104 state. | Covered by P04 and P02. The A104/A105 read is in LAUNCH_ORDER section 14, and A106 is in the INDEX. | - |
| RN01, P05 | NOTE | Part B's packet status stops at 0514. | Not applied. Part B's records still say "NOT READY at 21:01Z ... 0514 delta started". Their bottom line (not admitted; step 4 waits) agrees with LAUNCH_ORDER section 5.1, which is the status of record, and the INDEX gives the current status. | - |
| RN03 | NOTE | R-D11 says A85.2-4 cover step 2 only. | Not applied. A85.2 applies "from the step-2 launch onward" (FORMAL, addendum), and R-C1's CP-1 window cites A85.2 correctly. R-D11's wording is left for root. | - |
| RN04 | NOTE | A61 F3's "during calibration prep" against the default Z2 placement. | Not applied. Both placements follow the seal, so 0620 is met. Root records the placement in V006 (R-D5, R-D14). | - |
| RN05 | NOTE | INVENTORY states the c2v007r2 re-pin without Part A's scope caveat. | Not applied. Read INVENTORY's line as a recommendation, pending the scope check in R-B2. | - |
| RN06 | NOTE | The provenance of route-A cap 3 is circular. | Not applied. Cap 3 is a single proposal: Claude4's V001 figure, carried by Codex1's templates, pending root admission. | - |
| RN07 | NOTE | R-D8's 28 GiB RSS is below 1.5 x 18.79 = 28.185 GiB (A61). | Not applied, and open for root: 29 GiB meets A61, or root records why 28 GiB is enough (UNTESTED model, TESTED arithmetic). | - |
| RN09 | NOTE | The R-B1 and r6 labels read broader than A96 and A89. | Not applied. The texts carry the caveat: closed for V007 (A96), and step 4 runs on r5 unless root rules a successor (A89). | - |
| N3 | NOTE | The simulation uses a 30 s step, so values can move by up to about 0.4 h in batches. | Not applied. The figures are UNTESTED projections at 30 s resolution, and the Codex2 match is a shared discretization. | - |
| N4 | NOTE | The zero-late-start result holds only at solo speed, and the margin is 1.095x. | Not applied. Under the measured load ratios, the shipped max_concurrent 1 has late starts and the proposed 6 has none (the refute's sensitivity, UNTESTED model). | - |
| N5 | NOTE | The H1 cap rule fails at cap 3 itself. | Not applied, and open for root: state the asymmetry, or use one criterion for every cap. | - |
| N6 | NOTE | The direct and DIII wall caps give no margin against the load ratios. | Not applied, and open for root (R-A5, R-D5, R-D8). | - |
| N7 | NOTE | The U scenario is called an "upper bound". | Not applied. Read U as the upper scenario, not a bound. Part B's 8.1-8.11 h is TIMING_V003 as it stands; Part A's 8.74-8.77 h is the adjusted figure. | - |
| N8 | NOTE | Some projection lines carry no label of their own. | Not applied. The document-level UNTESTED label covers them, and the section 6.3 "min free" columns are the minimum over E and U. | - |
| N9 | NOTE | The background sensitivity stops at 48 GiB. | Not applied. At midday load levels the gate, not the cap, would set the schedule. | - |
| N10 | NOTE | At the typical model, the SENS batches fail their disk guard after the campaign. | Not applied. SENS depends on root's D3 ruling or another volume, and R-D17 asks for D3 before the campaign. | - |
| N11 | NOTE | The cap-6 admission_limit row (-1, -1.4%) cannot be reached. | Not applied. Read the row as "no admission possible". | - |
| P06 | NOTE | The 8 h cap item is attributed nowhere. | Attributed here, in section 2, row 15. | - |
| P07 | NOTE | `root_items` in INVENTORY_C4V002.json names a bare V001 file. | Not changed in the record. INDEX section 3 states that ROOT_ITEMS_FINAL_C4V004 is the one root-items list of record. | - |
| P08 | NOTE | Addendum provenance details in Part B. | Not applied. Part B's second copy (27b62183) is pinned in its HASHES.txt, and the open-path sha 17cb4fd4 is a read-time value. | - |
| P10 | NOTE | Conduct items. | Disclosed in the fix log and in the parts' PARTIAL.md. This step's conduct is in INDEX section 8. | - |

## 4. The V005 addendum rulings

| Ruling | How V002 uses it, or no change with the reason |
|---|---|
| A57: calibration consumes only a sealed ADOPT_TAIL | T0 is the sealed ADOPT_TAIL (LAUNCH_ORDER 4.1). No further change. |
| A61: route-A token; RSS caps >= 1.5x the modelled peak; F3 "root launches during calibration prep" | F3 grants no pre-seal exception (F01). RN04 and RN07 stay open (section 3.2). |
| A67: the identity reruns started at 14:56Z, with caps of wall 43,200 s and RSS 16 GiB | The root-reported walls (LAUNCH_ORDER 7.2), and R-D5's DIII cap set, with output raised to 96 GiB. |
| A72: the ramp gate, free memory >= 25% | The 25% gate before every start (5.2, 6). CP-1 option (b) never holds back a T-case (RR04). |
| A73: certificate slots are left to the registry, and the block is guarded by the sealed ADOPT | F03: 27 of 30 tail-ON specs take registry slots, and the 3 anchor-point specs take the V007 values through the registry's anchor entry. |
| A82: no write to V005 after the freeze; later rulings go in V006 | R-D14 (F13), and the V006 entries the records ask for (R-B4, R-C6, R-D5, R-D8, R-D17, R-C1). |
| A85: .2 background QoS from the step-2 launch onward; .3 step-2 outputs on the internal SSD; .4 sleep assertion | CP-1 option (b). R-D17 keeps step-4 outputs on External1 by default, since A85.3 covers step 2 only. RN03 is open. |
| A89: r6 for steps 4-5 only after its own identity gates, under a later ruling | R-B1: step 4 runs on r5. See RN09. |
| A92: the r5 identity gates PASS; c2v007r2 is the identity-comparator slot | The LAUNCH_ORDER 7.2 end times, and R-B2's comparator note (RN05). |
| A95: taskpolicy -b is preferred, not required | The wording of CP-1 option (b). |
| A96: V007 seals on r5; r6 deferred; caching for steps 4-5 decided later | The r6 tooling is MOOT (F10); R-B1. |
| A99: the D-03 case block; the A82 hazard is live; V6-S2 | R-A3; R-D14; R-D17 (step-2 outputs on the internal SSD, step 2 only). |
| A101: case block 76309ae3, pinned as `binding_inputs.case_block` in prereg r5 | R-A3 is owned and closing, and the binding is TESTED in the r5 bytes. |
| A102: the compare slot takes r13 | The R-A3 evidence wording; LAUNCH_ORDER 14. |
| A103: Codex2 is out of usage; the step-4 packet and handoff reviews go to Claude3 | The owners of the Codex2-named builds, and the producer's reviewer (P04). |
| A104 and A105: r13 is the compare of record; BUILD_V007 delta PASS; step-2 disk; E-OPS5 | Read in the fix pass. No step-4 record changes beyond wording. |
| A106: prereg r6 approved; the binding unchanged; V005 closed | Newer than every V002 record. No record change (row 20; INDEX 5). |

## 5. Not changed, with the reason

- **The V001 files.** They are kept unchanged by rule, and the V002 records beside them supersede them.
- **`SCHEDULE_SIM_C4V003.json` and `schedule_sim_c4v003.py`.** Codex2 0519 pinned them, so N1 got the successor v004 instead.
- **Part C's "Under 0620, step 4 waits for the packet".** It covers only the 33 direct calls, which are what the handoff is about (FIXLOG, RR01).
- **The superseded in-pass versions.** They keep their old wording as history, for example "same strength" in ROOT_ITEMS_FINAL_C4V002 and C4V003.
- **The NOTE items marked "Not applied" in section 3.2.**
