# Step-4 root items, final merged list, V004 (dispatch 0587, V002 correction pass)

**Who and when.** A Claude4 helper, 2026-10-18T23:06:01Z (`date -u` at generation). Coordinator: Claude2.

**Authority.** Root (Claude2) alone decides and launches. Every disposition below is a **RECOMMENDATION**. Nothing here launches or authorizes a run.

**Labels.** **TESTED** = recomputed from bytes or observed in a fenced plan-only process. **FORMAL** = read from code or rulings, with file:line. **UNTESTED** = projections, fits and future behaviour. Shas are shown as 8-hex prefixes of values computed from bytes; the full values are in the JSON twin and in `work/SOURCE_PINS_C4V003.txt`.

**Records.** Machine-readable twin `ROOT_ITEMS_FINAL_C4V004.json` (sha256 `1cf25e8a72846c296005ef64af0da96b2fd7b86365f900fc56d4ef5d9577ffc7`). Projections are read from `SCHEDULE_SIM_C4V003.json` (`987801b258863e8be07497605c45e7112fcea5a9164f04e71b149852f7417150`); byte checks from `work/SOURCE_CHECKS_C4V002.json` (`74f2e026dd9c048e04f89490f39ddbfa81247f6287c0440d8483899386072347`) and `work/SOURCE_CHECKS_LATE_C4V002.json` (`e9a815cce8306fdfaeb56608baeaeac67b311cf64d52d0f6ccee31708fe31265`); the FIX pass byte checks from `../fixlog/work/FIX_SOURCE_CHECKS_C4FX001.json` (`ae83075cbfbffc233355ede1a0613d364de362423c24183666f8de52051a35c3`).

**What this is.** The successor of `../../launch_order/ROOT_ITEMS_FINAL_C4V001.md` for the V002 correction pass. All 36 V001 items are carried under their ids, and one item is new (R-D17). The V001 files are unchanged.

**Version note.** This V004 supersedes two in-pass versions, both kept unchanged:
- `ROOT_ITEMS_FINAL_C4V002.{md,json}` (`23eebe19`, `5f35f6f4`), written at 21:28Z. It had not read Codex1 0071/0072 or Codex2 0515 (21:00-21:03Z), so its R-B6 packet status was stale.
- `ROOT_ITEMS_FINAL_C4V003.{md,json}` (`9286a102`, `53fd5dda`), written at 21:45Z. It added A102 and the step-4 -> step-5 handoff (0631, Codex1 0074), but its owners predate A103 (21:43Z: Codex2 is out of usage).

**FIX pass.** This V004 and its JSON twin were regenerated in place at 2026-10-18T23:06:01Z by this builder, patched for the V002 refute findings RR01-RR04, P01, P03 and P04 (`../fixlog/FIXLOG.md`). The pre-fix bytes (md `e1a0d51b`, json `6c5b095d`), which the three V002 refuters pinned, are kept in `../fixlog/work/prefix/order/`. Changed: R-A1, R-A3, R-B4, R-B6, R-C1, R-C6, R-D14 and the traceability row; the rows marked "FIX pass" in the table below.

## Changes from V001

| item | change | source |
|---|---|---|
| R-B6 | Fallback removed; text replaced: launch only through the 0616 guarded packet, every control before any process; v005 FAIL (Codex2 0508), successors in progress (0069); step 4 waits if not ready. | 0620; F02; Codex2 0494/0508; Codex1 0068/0069 |
| R-D5 | DIII moved after T0 under the 0616 guard, no overlap with step 2 or the campaign; default before SENS, option during H3; one cap value each (wall 43,200 s, RSS 16 GiB, output 96 GiB). | F01; F12; Codex1 0065; F07 (output cap) |
| R-A3 | Status: owned (A99 D-03), case block 76309ae3 pinned in prereg r5 (A101); r5 landed for review (0103); closes at the seal. | A99; A101; Claude4 0101/0103; F12 |
| R-A5 | Orphan wait 29,400 s added; 8.74-8.77 h labelled an UNTESTED projection with TESTED arithmetic; output cap against the disk model. | F11; F12 |
| R-B4 | Campaign admission path stated (Orchestrator.run via the reviewed entry; never the raw CLI); PRELAUNCH must carry the certificate-policy and per-spec checks. | 0620; Codex1 0065; RUNBOOK_CX1V001 |
| R-B5 | Post-state acceptance compute labelled an unestimated critical-path item. | F06 |
| R-C1 | Certificate production compute (GQ timing basis, EPS/rho and LO unestimated); 31-point option; F03 slot source. | F06; F12; F03 |
| R-C8 | Cache ids corrected to probe v002 (878d612a, 4f0521aa, b370470a); Jacobian bridge option. | F08; 0620; F12 |
| R-D1 | PC-7 against DU-1 and DU-2 stated. | F12 |
| R-D2 | Default workers_8 row = the anchor repeat (Codex1 HEADLINE11 template); DU-2 option with its effect. | Codex1 0065/0068; task item 3 |
| R-D7 | Budget 48 successor marked not memory-feasible under the 0538 model; campaign model labelled an assumption. | F05; Codex2 0497 |
| R-D8 | Caps checked against the 0538 GiB model (28 GiB = 1.49x). | F05 |
| R-D14 | A82 no-write hazard extended to the whole campaign, or cite the _FROZEN.md copy. | F13; A99.6 |
| R-D15 | Packet runtime constraints and flock scope added. | Codex1 RUNBOOK_CX1V001 |
| R-D16 | Default is now the sibling config, since DIII runs after the campaign by default. | F01 |
| R-D17 | New item: disk plan, output placement, disk guard, D3. | F07 |
| R-B1, R-B2, R-C5, R-C6, R-C7, R-D6, R-D11, R-D12 | Wording aligned to the four batches, the post-T0 DIII and the packet (driver roles, templates, one batch at a time). R-B2 now closes before SENS, not before the seal, because the DIII evidence follows the campaign by default. | Codex1 0065/0068; F01 |
| R-B6 (V003 over the in-pass V002) | Packet status brought up to date: the successors landed (BUILD_CX1V002) and Codex2's delta reads 0 blocking; admission still waits for G7-SCOPE-1, the final root inputs and root admission. | Codex1 0071/0072; Codex2 0515 |
| R-A3, R-C6, R-D15 (V003 over the in-pass V002) | A102 (r13 for the compare slot); the step-4 -> step-5 handoff waits for the full step-4 decision, so step 5 joins the machine-wide schedule after FINAL_SUMMARY. | A102; dispatch 0631; Codex1 0074 |
| R-A2, R-B2, R-B3, R-B5, R-B6, R-C1, R-C8 (V004 over the in-pass V003) | Owners updated: Codex2 is out of usage, so root reassigns the builds that named it; further step-4 packet reviews go to Claude3. | A103 |
| R-A1 (FIX pass) | Evidence carries Part B's line: the 30/30 fill is a driver-layer statement, the seed (a distinct point) leaves the provisional list, and no PROVISIONAL file is a launch input. T0 procedure: root writes and announces C1; Claude4 runs the reviewed producer and posts the manifest; root runs PRELAUNCH on those exact bytes (optional dual construction); the binder pins only the manifest pins. Acceptance rule from Part C. | RR02; RR03; P01; F03 |
| R-A3 (FIX pass) | Status: bound in prereg r5, not published or sealed; publication-time binding check PASS (Codex2 0517); Claude4 0109: r5 F-01 blocking as written, r6 recommended and in build, the 76309ae3 binding kept; Codex3 now on seal tools v003 only. | P03; Claude4 0103/0109; Codex2 0517; 0636 |
| R-B4, R-B6, R-C6 (FIX pass) | R-B6 covers the 33 direct calls. The campaign and S4-POST-S1 have no admitted launch path until root rules R-B4 and R-C6 in a V006 entry under 0620. R-B4 adds the root-published admission record (all four 0620 controls). R-C6 drops "a root admission of the same strength". | RR01; 0620; RUNBOOK_CX1V003; templates_v004 |
| R-C1 (FIX pass) | Scope line carried: on the launch path of every tail-ON direct run, TAIL_REANCHOR included. The CP-1 window and operator are root's ruling: (a) phase P; (b) step 2 at background QoS with a memory attestation, never holding back a T-case; or (c) after T0. The point keys are already fixed by the C4T block. | RR04; P01; A72; A85.2; A95 |
| R-D14, traceability (FIX pass) | R-D14 lists the V006 entries for the R-B4/R-C6 launch paths and the CP-1 window. Traceability: the 3 anchor-point specs take the V007 adoption values through the R-C1 registry entry (A73). | RR01; RR02; RR04 |

**Disclosure (F09).** V001's `ROOT_ITEMS_FINAL_C4V001.md` was first written as `218b5574`, which Codex2 0491 pinned, and was then overwritten in place twice (218b5574 -> 3d9f70f3 -> 5d83f067); its JSON twin went fe1c02e7 -> b1849b64 -> 100bec59. The superseded bytes are not recoverable: no file in the V001 package carries any of those shas (TESTED, `work/SOURCE_CHECKS_C4V002.json`). This V002 is versioned by exclusive create; its generator has no replace path. The FIX pass rewrote this work candidate in place, as its brief allows, and kept the pre-fix bytes (see the FIX-pass note above).

## Summary

| id | item | close by | owner | filled by V007 | source |
|---|---|---|---|---|---|
| R-A3 | Case-block binding in the sealed prereg: owned, bound in prereg r5 (not yet sealed), closes at the seal | BEFORE_SEAL | Claude4 (case block, prereg r5 and its r6 successor; A99 D-03, 0109); Codex2 (checks done: 0507, 0517); Claude2 at seal assembly | MUST BE IN THE SEALED PREREG | inventory R-A3 + dryplans DEFECT + A99 D-03 + A101 + Claude4 0101/0103/0109 + Codex2 0517 |
| R-A6 | Finite carried uncertainty in the ADOPT_TAIL report | BEFORE_SEAL | Codex3 (compare) + Claude2 | YES (the verdict carries it) | dryplans adoption_world S7 (V001 new item) |
| R-B3 | One v006r10 cascade with a single delta review | BEFORE_SEAL | Claude2; builder: Codex2 was named but is out of usage (A103), so root reassigns; distinct reviewer | PARTIAL (tuple line) | inventory R-B3 + launch_order V001 |
| R-B4 | Launch entries, and the campaign's own admission path (none admitted yet) | BEFORE_SEAL | Claude2 (rules the path in V006, publishes the admission record); builder any lane; distinct review | NO | inventory R-B4 + dryplans campaign gates + Codex1 0065/RUNBOOK_CX1V001/V003 + 0620 |
| R-D14 | V006 addendum for the step-4 rulings, and the A82 no-write hazard for the whole campaign | BEFORE_SEAL | Claude2 | NO | inventory R-D14 + F13 + A99.6 |
| R-B6 | Launch path of the 33 direct calls: Codex1's guarded packet (0616) only, with no fallback | BEFORE_HEADLINE | Codex1 (builder, 0616); distinct review: Codex2 0515 (done), further step-4 packet reviews Claude3 (A103); Claude2 (root admission) | NO | launch_order V001 (new item) + 0620 + F02 + Codex2 0494/0508 + Codex1 0068/0069 |
| R-C1 | Per-point certificate admission and the registry (28 points, or 31), with its production compute | BEFORE_HEADLINE | Claude2 science review and registration; the producers were built by Codex2 (out of usage, A103), so root assigns the lane that runs them and builds the LO successor; distinct reviewer | NO (keys depend on the block and driver, both already fixed by the case block) | inventory R-C1 + dryplans CERTIFICATE_POLICY_PENDING + reconcile RC-02/03 + F03 + F06 + F12 |
| R-D1 | TAIL_REANCHOR source, and PC-7 against DU-1 | BEFORE_HEADLINE | Claude2 | PARTIAL (DU-3 uses the C4T run) | inventory R-D1 + dryplans section 8 + reconcile OP1 + F12 |
| R-D11 | Operational settings for step 4 | BEFORE_HEADLINE | Claude2 | NO | inventory R-D11 + dryplans harness note + Codex1 RUNBOOK_CX1V001 |
| R-D17 | Disk plan and output placement for step 4 (and D3 retention) | BEFORE_HEADLINE | Claude2 | NO | V002 new item (F07) |
| R-D2 | Designate the workers_8 row before launch | BEFORE_HEADLINE | Claude2 | NO | inventory R-D2 + dryplans WORKERS_8_SPEC_NOT_REGISTERED + Codex1 HEADLINE template |
| R-D5 | Deciding-(iii) pairs: caps and placement, after the sealed ADOPT_TAIL | BEFORE_HEADLINE | Claude2 (root-only launch) | NO (but its launch waits for the sealed ADOPT_TAIL) | inventory R-D5 + launch_order V001 + F01 + F12 + Codex1 0065 |
| R-D8 | Caps for the direct tail-ON runs | BEFORE_HEADLINE | Claude2 | PARTIAL | inventory R-D8 + V002 memory model |
| R-D9 | Hull-miss contingency | BEFORE_HEADLINE | Claude2 | NO | inventory R-D9 |
| R-A1 | Config successor C1 from the sealed ADOPT_TAIL, and the final specs produced on it | AT_T0 | Claude2 (C1, PRELAUNCH, admission); Claude4 (the final specs: 0616 "Claude4 owns the specs") | YES | inventory R-A1 + dryplans post_adoption_probe + INVENTORY_C4V002 root_item_lines_for_successor (R-A1) + SPEC_HANDOFF_C4V002 section 5 |
| R-A2 | Seal tuple into APPROVED_V007_SEALS | AT_T0 | Claude2 + distinct reviewer; builder: Codex2 was named but is out of usage (A103), so root reassigns | YES | inventory R-A2 + dryplans campaign gate (seal allowlist) |
| R-A4 | C4-6 adoption derivation | AFTER_HEADLINE | Claude2 + distinct reviewer | PARTIAL | inventory R-A4 + dryplans campaign gate adoption_regeneration |
| R-A5 | Caps and the orphan wait regenerated from the measured C4T use | AFTER_HEADLINE | Claude2 | PARTIAL | inventory R-A5 + launch_order V001 (TIMING_V003 under-count) + F11 + F12 (orphan wait) |
| R-C2 | u_i carrier declaration | AFTER_HEADLINE | Claude2 | PARTIAL | inventory R-C2 + dryplans campaign gate u_i_carrier |
| R-D3 | Headline capability runs and the capability evidence | AFTER_HEADLINE | Claude2 (root-only launch) | PARTIAL | inventory R-D3 + dryplans CAPABILITY_EVIDENCE_PENDING |
| R-D4 | deciding_test document and config.anchor | AFTER_HEADLINE | Claude2 | NO | inventory R-D4 + dryplans CONFIG_ANCHOR_TAIL_REANCHOR_PENDING |
| R-B5 | Post-state certificate loop per campaign call (compute on the critical path) | BEFORE_CAMPAIGN | Claude2; the producers were built by Codex2 (out of usage, A103); an operator lane root assigns | NO | inventory R-B5 + F06 |
| R-C3 | Taxonomy approval and root judgment calls | BEFORE_CAMPAIGN | Claude2 + distinct reviewer | NO | inventory R-C3 |
| R-C4 | MODEL_INVALID for tail-ON | BEFORE_CAMPAIGN | Claude2 (later certified successor) | NO | inventory R-C4 + r9 TYPED_BLOCKERS |
| R-C6 | Register the S1 transfer test (S4-POST-S1) | BEFORE_CAMPAIGN | Claude2 | YES (the next-step text) | inventory R-C6 + Codex1 0065/0068 |
| R-C8 | Campaign points outside the pre-registered set (registry growth) | BEFORE_CAMPAIGN | Claude2 rules the design; builder: Codex2 was named but is out of usage (A103), so root reassigns; Claude-lineage review | NO | launch_order V001 (new item) + F08 + 0620 + F12 (Jacobian option) |
| R-D10 | Engine seed computed afresh | BEFORE_CAMPAIGN | Claude2 | NO | inventory R-D10 + reconcile RC-02 |
| R-D12 | Coordinate-spec preconditions still OPEN | BEFORE_CAMPAIGN | Claude2 | PARTIAL (PC-1) | inventory R-D12 + F12 |
| R-D15 | One machine-wide schedule across launchers | BEFORE_CAMPAIGN | Claude2 | NO | launch_order V001 (new item) + Codex1 RUNBOOK_CX1V001 step 7 |
| R-D16 | Where the per-D sensitivity registration lives | BEFORE_CAMPAIGN | Claude2 | NO | launch_order V001 (new item) |
| R-D7 | Campaign scheduling | BEFORE_CAMPAIGN | Claude2 | PARTIAL | inventory R-D7 + launch_order V001 + V002 memory model |
| R-B2 | Deciding-(iii) comparator successor on c2v007r2 | BEFORE_SENS | policy successor: Codex2 was named but is out of usage (A103), so root reassigns; Codex1 (c2v007r2 unchanged per 0611); cross-lineage reviewer | NO | inventory R-B2 + dryplans COMPARATOR_A68_SUCCESSOR_REQUIRED + A92/0611 |
| R-C5 | Distinct review per D of the deciding-(iii) evidence | BEFORE_SENS | Claude2 + a distinct-lane reviewer per D | NO | inventory R-C5 + dryplans SENSITIVITY_DECIDING_III_REQUIRED |
| R-C7 | Purpose, reading and schedule of the 18 sensitivity runs | BEFORE_SENS | Claude2 | NO | inventory R-C7 + Codex1 templates |
| R-D6 | Sensitivity launch conditions | BEFORE_SENS | Claude2 (root-only launch) | PARTIAL | inventory R-D6 + dryplans SENSITIVITY_DECIDING_III_REQUIRED + Codex1 templates |
| R-D13 | ORIGINAL_K marked for evaluation before freeze | AFTER_CAMPAIGN | Claude2 | NO | inventory R-D13 |
| R-B1 | Driver of record: r5 (settled for V007 by A96) | CLOSED_BY_RULING | Claude2 | YES (driver slot) | inventory R-B1 + dryplans R6 DEFERRED + A96 |

Close-by legend: `BEFORE_SEAL` = phase P, before the V007 seal (no step-4 launch of any kind); `BEFORE_HEADLINE` = before the headline batch (can close before the seal); `AT_T0` = H1, right after the sealed ADOPT_TAIL; `AFTER_HEADLINE` = H3, from the headline receipts; `BEFORE_CAMPAIGN` = before campaign wave 1; `BEFORE_SENS` = before the sensitivity batches; `AFTER_CAMPAIGN` = after the campaign, before the freeze; `CLOSED_BY_RULING` = closed by a ruling.

**Most likely to delay step 4 (RECOMMENDATION, from the dependency chain):** R-B6, R-C1, R-C8, R-B3, R-B4, R-B5, R-D17, R-D7, R-A5, R-B2, R-A3.
- R-B6: the guarded packet is the only launch path for the 33 direct calls. Its successor delta reads 0 blocking, but G7-SCOPE-1, the final root inputs and root admission remain, and the direct batches wait for them. The campaign and S4-POST-S1 wait for root's V006 rulings (R-B4, R-C6).
- R-C1: 28 (or 31) bundles, with unestimated EPS/rho and LO production and the LO producer successor.
- R-C8: without it the campaign stops after its pre-registered points.
- R-B3, R-B4 and R-B5: the campaign machinery, including unestimated per-call acceptance compute.
- R-D17: output placement, the disk guard and D3.
- R-D7: the campaign length, 8.7 d E / 14.9 d U at max_concurrent 6 against 26.0 / 43.8 d as shipped (UNTESTED; 120 calls in 21 waves is an assumption).
- R-A3 is closing: the binding is in prereg r5 (TESTED; landed for review, 0103; publication-time binding check PASS, Codex2 0517). Claude4 0109 reads r5 F-01 blocking as written and recommends r6, which keeps the binding. It closes at the seal.
- A103: Codex2, the named builder of R-A2, R-B2, R-B3 and R-C8 and of the certificate producers, is out of usage. Until root reassigns them, those items have no active builder.

## A. V007 adoption pins and the seal interface

### R-A1: Config successor C1 from the sealed ADOPT_TAIL, and the final specs produced on it
- **What:** Write numerics.{verdict_artifact, block_source, compare, sealed_prereg, adopted_result, source_results} and numerics.block := the sealed C4T call-spec numerics exactly (its eps/lo slots included). Root writes C1 and announces it as {path, sha256}; the final step-4 specs are then produced on that C1 by Claude4 (procedure below), not regenerated by root.
- **Blocks:** Every tail-ON direct run (its final spec is produced on C1) and the numerics_verdict gate.
- **Close by:** `AT_T0`. **Owner:** Claude2 (C1, PRELAUNCH, admission); Claude4 (the final specs: 0616 "Claude4 owns the specs"). **Filled by the V007 adoption:** YES.
- **Evidence:** adoption policy 7c726fa2 L90-91 (block == C4T numerics); config 721c7230 numerics fields null and source_results [] (TESTED, inventory); the r5 C4T FILLED spec de6d7d77 equals the current block outside the two certificate slots (TESTED, V001 and Part B); dry plans post_adoption_probe: 30/30 specs normalize with 0 pending after the fill (TESTED there), a driver-layer statement only: the C4T (A70) slots it attaches are V007 values only for the anchor point identity 8ad6ca4e8678 (3 specs: TAIL_REANCHOR, WORKERS_8_CANDIDATE_ANCHOR, HEADLINE_TRIAL; TESTED, Part B checks S3); the other 27 take registry slots (R-C1), and the seed is a distinct point (6944e210), so it is not on this list (Part B line, INVENTORY_C4V002 root_item_lines_for_successor.R-A1_evidence, carried here in the FIX pass); no PROVISIONAL file is a launch input: Codex1 templates_v004 limitations, "provisional/dry files are not admitted scientific inputs"; the hand-built TAIL_REANCHOR (924851c4) and WORKERS_8 (23c13f75) PROVISIONAL labels end "not a launch spec", and HEADLINE_TRIAL (7d9a8d47) carries the native mapper label (TESTED, fixlog/work/FIX_SOURCE_CHECKS_C4FX001.json); Part C producer produce_final_step4_specs_c4v002.py 8e835ce3 (SPEC_HANDOFF_C4V002 section 5; no V001 tool can produce the final bytes): in its synthetic-C1 final mode the MAPPER_BUILD bytes equal the PROVISIONAL bytes 9/9 and the hand-built bytes equal them except /label 20/20 (TESTED there, producer_test_v002).
- **Recommended disposition (RECOMMENDATION):** Prepare C1 now as a template differing from r9 only in these fields, the block and the R-C1/R-C2/R-D8 fields. At T0: (1) root fills C1, checks it by key diff and announces it as {path, sha256}; (2) Claude4 runs the reviewed final-spec producer (produce_final_step4_specs_c4v002.py 8e835ce3, once its distinct review is done) on that C1 and posts FINAL_SPECS_MANIFEST {path, sha256} with its binder_pins (SPEC_HANDOFF_C4V002 section 5, steps 1-7); (3) if root agrees, the 9 MAPPER_BUILD specs are rebuilt with the native Mapper.build in a fenced plan-only process and published only if the 9 shas agree (dual construction, step 6); (4) root runs PRELAUNCH on those exact bytes (R-B4); (5) the binder pins only the manifest pins. Acceptance rule: a MAPPER_BUILD spec equals its PROVISIONAL sha only where its registry record carries the A70 slots, which can hold only at the anchor point (HEADLINE_TRIAL, 7d9a8d47); a hand-built spec equals its PROVISIONAL bytes except /label; no PROVISIONAL file is ever bound.
- **Label:** FORMAL / TESTED. **Source:** inventory R-A1 + dryplans post_adoption_probe + INVENTORY_C4V002 root_item_lines_for_successor (R-A1) + SPEC_HANDOFF_C4V002 section 5.

### R-A2: Seal tuple into APPROVED_V007_SEALS
- **What:** The shipped allowlist is an empty frozenset; the tuple (compare sha, prereg sha, frozen addendum sha, report schema, verdict sha) enters only through an immutable policy successor, which forces core and wrapper successors.
- **Blocks:** numerics_verdict gate, hence the campaign. Not the direct runs.
- **Close by:** `AT_T0`. **Owner:** Claude2 + distinct reviewer; builder: Codex2 was named but is out of usage (A103), so root reassigns. **Filled by the V007 adoption:** YES.
- **Evidence:** adoption policy 7c726fa2 L9-12; core a595c5c0 L200-203; wrapper 24abe3bc L27; dry plans adoption_world S1 refuses only on V007_SEAL_NOT_IN_REVIEWED_ALLOWLIST; S2 passes with the tuple in memory (TESTED there).
- **Recommended disposition (RECOMMENDATION):** Build it inside the R-B3 cascade now with a one-line placeholder; at T0 insert the tuple and verify by line diff (the RI-27 pattern), so no full review sits after the seal.
- **Label:** TESTED / FORMAL. **Source:** inventory R-A2 + dryplans campaign gate (seal allowlist).

### R-A3: Case-block binding in the sealed prereg: owned, bound in prereg r5 (not yet sealed), closes at the seal
- **What:** Prereg r4 had no binding_inputs.case_block, and the sealed compare refuses CASE_BLOCK_ABSENT without it. A99 D-03 made the fix owned: Claude4 builds the V007 case block, Codex2 checks it, and it is pinned as binding_inputs.case_block in prereg r5. A101 (20:48Z): CASE_BLOCK_V007_C4V001 76309ae3, Codex2 0507 PASS with zero findings, pinned in prereg r5. Prereg r5 landed for Codex3's review at 21:14:35Z (Claude4 0103), and its publication-time binding check passed (Codex2 0517, 21:03:06Z: 50/50). Status (FIX pass): bound in prereg r5, not published or sealed. Claude4's own r5 check (0109, 22:31:47Z) reads F-01 BLOCKING for sealing r5 as written, because A102-A105 postdate its text, and recommends prereg r6, which keeps the 76309ae3 binding; the r6 build started at 22:33:25Z (no r6 JSON yet). Codex3's r5 review (0628) was narrowed to the seal-tools v003 delta (0636; Codex3 0642). It closes at the seal.
- **Blocks:** The sealed V007 verdict, until the sealed prereg (r5, or r6 or another successor with the same binding) carries it.
- **Close by:** `BEFORE_SEAL`. **Owner:** Claude4 (case block, prereg r5 and its r6 successor; A99 D-03, 0109); Codex2 (checks done: 0507, 0517); Claude2 at seal assembly. **Filled by the V007 adoption:** MUST BE IN THE SEALED PREREG.
- **Evidence:** prereg r4 e3b6b5b2 key walk: no case_block (TESTED, inventory work/CASE_BLOCK_CHECK_C4V001.json); prereg r5 draft 3245899f: binding_inputs.case_block = {path v007_final_prereg_c4/r5/case_block/CASE_BLOCK_V007_C4V001.json, sha256 76309ae39f23060cc662c4e218a41e1f95c56a26992402218a6198625f85ee71} (TESTED from bytes, work/SOURCE_CHECKS_C4V002.json); case block bytes 76309ae3 (TESTED); A101 and Claude4 0101 (6bc848e2): validator r12 validate_case_block returns [] (TESTED there); Claude4 0103 (a81ecc0b): Codex2 binding check PASS 50/50 (cited, not re-read); compare r11 a5d10cb1 L5689-5697 and frozen compare r12 4bd7b262 L5705-5714: sealed mode refuses CASE_BLOCK_ABSENT (FORMAL, V001 read at 20:01:37Z); A102 (21:22Z): the compare slot takes r13 = r12 plus exactly the A-B1 fix, once Claude3 and Codex2 report 0 blocking; nothing else changes (addendum copy 27b62183, work/SOURCE_CHECKS_LATE_C4V001.json); FIX pass, TESTED from bytes (fixlog/work/FIX_SOURCE_CHECKS_C4FX001.json): r5 3245899f binds 76309ae3 and the case block names C4T FILLED de6d7d77; Codex2 0517 (97933e1a) PASS 50/50, closing the publication-time binding check; Claude4 0109 (d0b20717) F-01 BLOCKING for r5 as written, r6 recommended, the 76309ae3 binding stays; r6/PARTIAL.md (fb431ab6) build started 22:33:25Z; 0636 (6b29ccf2) and Codex3 0642 keep Codex3 on the seal-tools v003 delta only.
- **Recommended disposition (RECOMMENDATION):** No new step-4 action: keep this binding through the seal. If r5 is superseded before the seal (Claude4 0109 recommends r6), its successor must carry the same binding_inputs.case_block (76309ae3, or a reviewed successor block); re-check the sealed prereg's binding_inputs.case_block from bytes at seal assembly.
- **Label:** TESTED (binding in the r5 bytes) / FORMAL (requirement). **Source:** inventory R-A3 + dryplans DEFECT + A99 D-03 + A101 + Claude4 0101/0103/0109 + Codex2 0517.

### R-A4: C4-6 adoption derivation
- **What:** Schema DDO154_CALIBRATION_ADOPTION_DERIVATION_C2V005 plus the wrapper tail bindings: verdict, adopted C4T case and spec, base and seed spec shas, capability evidence, timing model, monitor-verified receipts, caps above measured use, disk guard, registry.
- **Blocks:** adoption_regeneration gate, hence the campaign.
- **Close by:** `AFTER_HEADLINE`. **Owner:** Claude2 + distinct reviewer. **Filled by the V007 adoption:** PARTIAL.
- **Evidence:** v005 c75a889f L1828-1926; wrapper 24abe3bc L183-197 (needs driver_capability ok); dry plans: base and seed shas must come from the post-adoption config (spec bytes change after adoption, TESTED there).
- **Recommended disposition (RECOMMENDATION):** Write and review a target-free generator now; run it after the headline batch on C1 bytes; pin its output in C2.
- **Label:** FORMAL. **Source:** inventory R-A4 + dryplans campaign gate adoption_regeneration.

### R-A5: Caps and the orphan wait regenerated from the measured C4T use
- **What:** Config per-call caps are 8 h wall, 64 GiB RSS and 12 GiB output; orphan_wait.cap_s is 29400 s (the 8 h cap plus 600 s). C4-6 refuses caps that are not above the measured use.
- **Blocks:** adoption_regeneration. Campaign calls that run past the wall cap stop. With a wall cap above 8 h, a resumed wave whose orphaned calls outlive the 29400 s wait returns ORPHANS_STILL_RUNNING (it fails safe, and root must resume again).
- **Close by:** `AFTER_HEADLINE`. **Owner:** Claude2. **Filled by the V007 adoption:** PARTIAL.
- **Evidence:** config 721c7230 per_call, disk_guard and orphan_wait (TESTED from bytes, work/SOURCE_CHECKS_C4V002.json); upper solo tail-ON call 8.74-8.77 h (8.75 h used): an UNTESTED projection; its arithmetic is TESTED (TIMING_V003 3e3fb600 keeps the I=7 route-A baseline in its I=32 total; scaling it adds 25 x [91.4, 95.1] s; SCHEDULE_SIM_C4V003 per_call); load ratios 1.69-2.99 (TIMING_V003 calibration rows, measured at load 20-60); v005 c75a889f L2672-2707: wait_orphans takes its cap from config orphan_wait.cap_s and returns ORPHANS_STILL_RUNNING past it (FORMAL); config output cap 12 GiB against helper C's 96-node model, 21.5 GiB typical and 57.7 GiB worst (caps_model.json 4a5a0bd6; UNTESTED model).
- **Recommended disposition (RECOMMENDATION):** Wall cap at least 2x the C4T measured elapsed and at least the upper projection times the measured load ratio; RSS at least 1.5x the C4T peak; output cap at least 1.5x the C4T output; disk_guard.per_call_bytes at least the output cap; and orphan_wait.cap_s at least the new wall cap plus the receipt grace and margin (keep the +600 s pattern), raised in the same config successor.
- **Label:** TESTED (values, arithmetic) / UNTESTED (fit). **Source:** inventory R-A5 + launch_order V001 (TIMING_V003 under-count) + F11 + F12 (orphan wait).

### R-A6: Finite carried uncertainty in the ADOPT_TAIL report
- **What:** The adoption refuses V007_CARRIED_UNCERTAINTY_REQUIRED if a carried_numerical_uncertainty_km_s row is None; compare r11 L4781 allows None rows.
- **Blocks:** numerics_verdict on an otherwise valid ADOPT_TAIL.
- **Close by:** `BEFORE_SEAL`. **Owner:** Codex3 (compare) + Claude2. **Filled by the V007 adoption:** YES (the verdict carries it).
- **Evidence:** dry plans adoption_world S7 (TESTED on look-alikes there); compare r11 a5d10cb1 L4781 (FORMAL, cited by the dry plans).
- **Recommended disposition (RECOMMENDATION):** Confirm in the seal rehearsal that an ADOPT_TAIL report always carries finite rows, or rule how a None row is read and put that rule in the R-B3 policy successor.
- **Label:** TESTED (look-alike) / UNTESTED (real report). **Source:** dryplans adoption_world S7 (V001 new item).

## B. Driver, successors and launch machinery

### R-B1: Driver of record: r5 (settled for V007 by A96)
- **What:** A96 (19:51Z): V007 seals on v010 r5 b5cc62af; the r6 build was stopped and its bytes are unfinished and unused; caching for steps 4-5 is decided later with the A85.1 result. Codex1 0065: DIII reference roles keep the pinned v009-GEO; every production and new role uses r5.
- **Blocks:** Nothing now. v006r9 requires r5, so step 4 runs on r5.
- **Close by:** `CLOSED_BY_RULING`. **Owner:** Claude2. **Filled by the V007 adoption:** YES (driver slot).
- **Evidence:** A96 in the open V005 addendum (copy 70a48f51 in this folder); core a595c5c0 L25; wrapper 24abe3bc L47-48; driver_r6/ listing 19:37Z: no BUILD.md, no manifest (TESTED, V001); Codex1 templates_v002: driver roles PRODUCTION_R5, NEW_R5 and REFERENCE_V009GEO (TESTED from bytes).
- **Recommended disposition (RECOMMENDATION):** Run every step-4 production and new-side call on r5, and the DIII reference side on the pinned v009-GEO. A cache or parallel-tail driver for steps 4-5 later needs its own identity gates, an orchestrator retarget successor, re-keyed registry points (the driver sha is in every point key) and a deciding-(iii) new side or a B0 transfer ruling.
- **Label:** TESTED / FORMAL. **Source:** inventory R-B1 + dryplans R6 DEFERRED + A96.

### R-B2: Deciding-(iii) comparator successor on c2v007r2
- **What:** The pair plan and sensitivity policy pin the c2v004-derived comparator (FAIL, A68); compute_pair refuses while COMPARATOR_A68_REVIEWED is False and REGISTERED_DISTINCT_REVIEW_SHA256 is empty. Since A92, c2v007r2 (052da0fe) is the identity-comparator slot of record.
- **Blocks:** DIII evidence, hence the 18 sensitivity runs. Not the DIII launches.
- **Close by:** `BEFORE_SENS`. **Owner:** policy successor: Codex2 was named but is out of usage (A103), so root reassigns; Codex1 (c2v007r2 unchanged per 0611); cross-lineage reviewer. **Filled by the V007 adoption:** NO.
- **Evidence:** sensitivity policy 8fb06600 L19-40, L185-203; pair plan cb42a5a3; A92; 0611 (comparator source must not change); c2v007r2 052da0fe, BUILD_R2 d02e4637 (TESTED hashes, V001).
- **Recommended disposition (RECOMMENDATION):** One policy successor that re-pins the pair plan and policy to c2v007r2 through an r5 custody adapter outside the comparator (as the c2v004-r5 adapter did), with a validate_report for its schema; COMPARATOR_A68_REVIEWED set only after that adapter is reviewed. Confirm that the two-driver comparison (v009-GEO vs v010 r5) is in c2v007r2's supported scope. It must land before the DIII evidence step, which by default follows the campaign (R-D5).
- **Label:** TESTED (pins) / FORMAL. **Source:** inventory R-B2 + dryplans COMPARATOR_A68_SUCCESSOR_REQUIRED + A92/0611.

### R-B3: One v006r10 cascade with a single delta review
- **What:** Policy, core and wrapper successors carrying R-A2 (placeholder), R-B2, R-C8, R-B4 and R-A6 if needed. Every config change is a new cache id (C4-2).
- **Blocks:** The campaign gates.
- **Close by:** `BEFORE_SEAL`. **Owner:** Claude2; builder: Codex2 was named but is out of usage (A103), so root reassigns; distinct reviewer. **Filled by the V007 adoption:** PARTIAL (tuple line).
- **Evidence:** wrapper 24abe3bc L27-30 byte pins; v005 c75a889f C4-2 L59-63.
- **Recommended disposition (RECOMMENDATION):** Build it now, leaving only the tuple line for after the seal. Add a regression test: under the same config, r10 Mapper.build must give byte-identical specs to r9 for the 9 probe points and the seed (otherwise capability evidence and cached keys would not match).
- **Label:** FORMAL. **Source:** inventory R-B3 + launch_order V001.

### R-B4: Launch entries, and the campaign's own admission path (none admitted yet)
- **What:** v006r9 exposes plan and wave only; Orchestrator.run needs a session leader (launch_setsid_c2v005). Root also needs a one-call prelaunch check for standalone specs. The 0616 guarded packet covers the 33 direct calls only: campaign execution and the unregistered S4-POST-S1 need their own admission (RUNBOOK_CX1V001/V003 step 1; template limitations). Codex1 0065: PRELAUNCH must include the actual certificate-policy and per-spec checks, because the r9 prelaunch function alone permits a null registry. Until root rules this entry and the campaign admission in a V006 entry under 0620 (R-D14), the campaign has no admitted launch path and waits. Orchestrator.run already refuses unless its gates pass and it runs as a session leader (v005 c75a889f L3436-3444; launch_setsid_c2v005 b978f402 only setsids and execs), so this is a gap of scope and wording, not an unguarded launch.
- **Blocks:** The campaign launch; the PRELAUNCH records the 0616 plans pin.
- **Close by:** `BEFORE_SEAL`. **Owner:** Claude2 (rules the path in V006, publishes the admission record); builder any lane; distinct review. **Filled by the V007 adoption:** NO.
- **Evidence:** wrapper 24abe3bc L333-349; v005 c75a889f L3436-3444; setsid b978f402; Codex1 0065 (6a676c7c) and RUNBOOK_CX1V001 (4d6107c7) step 1; templates_v002 limitations (TESTED from bytes); 0620 (037a2a61): no raw campaign CLI launch path; FIX pass, TESTED from bytes (fixlog/work/FIX_SOURCE_CHECKS_C4FX001.json): RUNBOOK_CX1V003 (2eda3ebf) step 1, "Campaign execution and unregistered post-calibration S1 require separate admission"; templates_v004 limitations, "Campaign launches and unregistered post-calibration S1 are outside this direct-run packet"; v005 run() L3436-3444 refuses unless gates_ok and a session leader; launch_setsid_c2v005 only setsids and execs.
- **Recommended disposition (RECOMMENDATION):** Build a small reviewed entry (run --new-campaign, resolve retry, reingest, status, and a prelaunch-check that writes a pinned PRELAUNCH record per spec with the certificate-policy and per-spec checks) that imports the r10 wrapper and runs under launch_setsid_c2v005. The campaign launches only through Orchestrator.run via this entry, with all four 0620 controls enforced before any process: the sealed ADOPT_TAIL (numerics_verdict over it); a root-published step-4 admission record for the campaign (the entry, C2, the work dir and the caps, by exclusive create, as for the 0616 packet); the PRELAUNCH and certificate checks (certificate_policy and prelaunch_check per call, with deciding_test, driver_capability, adoption_regeneration and u_i_carrier); and the r5 allowlist (v006r9 accepts only r5 b5cc62af). Add the 0616 core-priority and sleep-assertion steps; never use the raw campaign_c2v005 CLI. 0620 names only the 0616 packet as the step-4 launch path, so root rules this path in a V006 entry; until then the campaign waits.
- **Label:** FORMAL / RECOMMENDATION. **Source:** inventory R-B4 + dryplans campaign gates + Codex1 0065/RUNBOOK_CX1V001/V003 + 0620.

### R-B5: Post-state certificate loop per campaign call (compute on the critical path)
- **What:** Each completed campaign call ingests INFRA CERTIFICATE_ACCEPTANCE_REFUSED until write_acceptance writes its handoff and the call is re-ingested. That needs, per completed call, an LO proof for every consumed state and GQ_SIGNED for the signed states. The number of consumed states per call is known only after the call, and no producer timing exists for these proofs, so this compute is unestimated.
- **Blocks:** Every campaign wave after a completed call. The campaign projection (8.7 d E / 14.9 d U at max_concurrent 6, UNTESTED) assumes zero acceptance time between waves.
- **Close by:** `BEFORE_CAMPAIGN`. **Owner:** Claude2; the producers were built by Codex2 (out of usage, A103); an operator lane root assigns. **Filled by the V007 adoption:** NO.
- **Evidence:** wrapper 24abe3bc L95-118, L202-222, L265-276, L305-328; guard 5f1e49e6 L155-219; review r6 2d02874e (synthetic world, TESTED there).
- **Recommended disposition (RECOMMENDATION):** Write the operating procedure, assign an operator lane, automate the producer runs per completed call so a wave never waits on a manual step, and time the first acceptance (wave 1, the seed) to replace this unestimated item with a measured one.
- **Label:** FORMAL / UNTESTED (time). **Source:** inventory R-B5 + F06.

### R-B6: Launch path of the 33 direct calls: Codex1's guarded packet (0616) only, with no fallback
- **What:** The 33 direct calls (HEADLINE11, DIII4, SENS_LO9, SENS_HI9) launch only through Codex1's guarded packet (0616), with the sealed ADOPT_TAIL, the step-4 admission, the PRELAUNCH/certificate/sensitivity checks and the r5 allowlist enforced before any process (0620). The packet v005 (guard v005 11a31edd, launcher v005 f9e4888d, binder v004 7f7add85, direct adapter v001 eee61ac6) read FAIL with four blockers (Codex2 0508). Its successors (0069) have landed: BUILD_CX1V002 with guard v007 42bf0ce9, launcher v008 bf2d535f, binder v006 3db8c72a, the unchanged adapter v001 and templates_v004 (Codex1 0071), and Codex2's delta reads PASS_WITH_FINDINGS with 0 blocking in its bounded scope (Codex2 0515; Codex1 0072). The packet is still not admitted: the complete reviewed transitive source inventory (G7-SCOPE-1), the final root inputs (C1, policy, registry, certificates, sensitivity evidence, caps, output paths), Claude4's final specs (the reviewed producer's manifest on C1, R-A1) and root admission remain, and no launch approval is issued. If it is not admitted when V007 adopts, the direct batches wait. The zero-build fallback through the raw campaign CLI is removed (0620, Codex2 0494): it enforced none of those controls before creating a process. The campaign and S4-POST-S1 are outside the packet (RUNBOOK_CX1V003 step 1; templates_v004 limitations) and have no admitted launch path until root rules R-B4 and R-C6 in a V006 entry under 0620; they wait until then.
- **Blocks:** Every direct batch: HEADLINE11, DIII4, SENS_LO9 and SENS_HI9 (33 calls).
- **Close by:** `BEFORE_HEADLINE`. **Owner:** Codex1 (builder, 0616); distinct review: Codex2 0515 (done), further step-4 packet reviews Claude3 (A103); Claude2 (root admission). **Filled by the V007 adoption:** NO.
- **Evidence:** 0620 037a2a61 (ruling); Codex2 0494 b633c98e (the raw CLI checks only monitor/driver/spec hashes and its own process budget; TESTED from source there); Codex2 0508 dda0f7ba: TESTED FAIL for guard v005 / binder v004 / launcher v005 / adapter v001 (refusal ordering, guard bootstrap, late plan re-read, .pyc probe); Codex1 0069 54d90d6e: successors started; Codex1 0071 (BUILD_CX1V002 3a9c2a22): four blockers, four SHOULD_FIX items and NI-3 closed at local tested scope; Codex2 0515 (14175b29): PASS_WITH_FINDINGS, 0 blocking, G7-SCOPE-1 boundary, "No scientific launch or launch approval" (TESTED there; shas re-hashed here, work/SOURCE_CHECKS_LATE_C4V001.json); Codex1 0068 11e45132 and RUNBOOK_CX1V001 4d6107c7: four UNBOUND templates cover the 33 direct calls; every start, the first included, needs free memory >= 25%; the proposed route-A cap 3 awaits root admission; 0623 3cf31cd8: tail-ON specs use uv_tail.enabled = true with no mode field, the reviewed r5 schema; 30/30 dry-plan tail-ON specs carry it (TESTED spot check here; Part B owns the record).
- **Recommended disposition (RECOMMENDATION):** Codex2's delta of the successors reports 0 blocking (0515). Before admission, close G7-SCOPE-1 with the complete reviewed transitive source inventory, then bind the templates (templates_v004 equal templates_v002 in every field this list uses, TESTED) with Claude4's final specs, root-approved caps (R-D5, R-D8), output paths (R-D17) and the PRELAUNCH records (R-B4). If it is not admitted at T0, the direct batches wait; nothing else launches a direct step-4 call. The campaign (R-B4) and S4-POST-S1 (R-C6) launch only through a path root names in a V006 entry, with all four 0620 controls enforced before any process.
- **Label:** FORMAL (ruling) / TESTED (by Codex2: v005 FAIL, successor delta 0 blocking) / UNTESTED (production admission). **Source:** launch_order V001 (new item) + 0620 + F02 + Codex2 0494/0508 + Codex1 0068/0069.

## C. Science and policy approvals

### R-C1: Per-point certificate admission and the registry (28 points, or 31), with its production compute
- **What:** certificate_policy_review, approved_certificate_producers and a registry with prelaunch bundles; a reviewed LO producer successor (finish() always UNAVAILABLE); full EPS/rho tables; one GQ record per point. The pre-campaign points are 28: the 27 direct-run points plus the campaign seed 6944e210d071c17b502fd5188ea8967503dbf9bb1d5530b67d0b151da02b13cd. Option: 31, adding the 3 Jacobian side points of wave 2 (u = seed + 0.05 along each coordinate; fixed before any result), so waves 1-2 can run before R-C8 bites. For 27 of the 30 tail-ON specs the slots come from this registry, not from the V007 adoption; the 3 anchor-point specs (TAIL_REANCHOR, WORKERS_8, HEADLINE_TRIAL; key 8ad6ca4e8678) take the V007 adoption values only through this registry's entry for the anchor point (A73; F03). R-C1 is on the launch path of every tail-ON direct run, TAIL_REANCHOR included: PRELAUNCH under C1 refuses an unregistered point. Producing the bundles is compute on the critical path before H2: GQ about 17.3 min serial for 28 points (28 x 37.13 s, an UNTESTED extrapolation from one record); EPS/rho and LO have no timing record, so they are unestimated.
- **Blocks:** Headline batch (the registry slots change the mapper bytes the capability evidence binds), sensitivity runs and the certificate_policy gate.
- **Close by:** `BEFORE_HEADLINE`. **Owner:** Claude2 science review and registration; the producers were built by Codex2 (out of usage, A103), so root assigns the lane that runs them and builds the LO successor; distinct reviewer. **Filled by the V007 adoption:** NO (keys depend on the block and driver, both already fixed by the case block).
- **Evidence:** config tail_readiness registry/policy null, producers [] (TESTED, inventory); review bc211c3a N1 (LO finish() always UNAVAILABLE), N3; BUILD_CERTIFICATES 48a14010 L15: full per-point EPS/rho tables were not executed; GQ_P128_MS128_C000_R5_CX2V001.json a785ccca: seconds 37.1257 (TESTED from bytes; one record); reconcile RC-02/RC-03: 28 distinct dry-plan keys, the seed not in the inventory list (TESTED); registry probe v002: registered slots change the spec bytes (TESTED); WAVE_FIXTURE_V001 8d19fecc: wave 2 is a 3-call Jacobian wave at u = seed + 0.05 e_i (synthetic cache only; real directions UNTESTED); A73: certificate slots are left to the certificate registry; F03 (REFUTE_C4V001); the CP-1 window (FIX pass, FORMAL from the addendum copy 18fd9a83 in fixlog/): A72 (L780) admits a V007 T-case only while free memory is >= 25%; A85.2 (L1253) runs every lane's non-critical process under taskpolicy -b from the step-2 launch onward; A95 (L1086) makes taskpolicy -b preferred, not required, in lane work; point keys exclude the eps/lo slots (provisional keys equal dry keys) and the C4T FILLED spec de6d7d77 has the anchor key, so the 28 keys are fixed now by the C4T block that the case block 76309ae3 names (TESTED, Part B checks S3; fixlog/work/FIX_SOURCE_CHECKS_C4FX001.json).
- **Recommended disposition (RECOMMENDATION):** Commission the LO successor and the cap review now. Root rules the CP-1 window and its operator lane: (a) phase P, if CP-1 can finish before the seal; (b) during step 2, only at background QoS (A85.2; A95) with root's memory attestation, never holding back a T-case (A72); or (c) after T0, as added time before H2. The point keys are already fixed by the C4T block, so CP-1 needs no V007 byte; bundles made before T0 are spent if V007 does not adopt. Time the first bundle end to end so the estimate rests on bytes; freeze the registry before the CAP runs and never change its probe-point entries afterwards.
- **Label:** TESTED / FORMAL / UNTESTED (time). **Source:** inventory R-C1 + dryplans CERTIFICATE_POLICY_PENDING + reconcile RC-02/03 + F03 + F06 + F12.

### R-C2: u_i carrier declaration
- **What:** The gate fails until root sets declared_by and basis; ADMISSION_RECTANGLES is not implemented; dropped from the r9 TYPED_BLOCKERS list.
- **Blocks:** u_i_carrier gate, hence the campaign.
- **Close by:** `AFTER_HEADLINE`. **Owner:** Claude2. **Filled by the V007 adoption:** PARTIAL.
- **Evidence:** config u_i_carrier (TESTED, inventory); v005 c75a889f L1797-1826.
- **Recommended disposition (RECOMMENDATION):** FROZEN_BANDS_ONLY declared by Claude2 with the sealed verdict as basis, if the freeze successor carries it (UNTESTED); otherwise NOT_CARRIED_DECLARED with disclosure.
- **Label:** TESTED / UNTESTED. **Source:** inventory R-C2 + dryplans campaign gate u_i_carrier.

### R-C3: Taxonomy approval and root judgment calls
- **What:** The tail-ON failure taxonomy is a candidate with judgment calls R10, R11, R13, R20/R21/R32, R22, R30; no route-A contraction test declared.
- **Blocks:** Halt classification in every campaign wave.
- **Close by:** `BEFORE_CAMPAIGN`. **Owner:** Claude2 + distinct reviewer. **Filled by the V007 adoption:** NO.
- **Evidence:** taxonomy 0ad99c66; config route_a_contraction_test null (TESTED, inventory).
- **Recommended disposition (RECOMMENDATION):** Commission the classification review now and rule the judgment calls before wave 1; keep the contraction test null unless a reviewed rule exists.
- **Label:** TESTED. **Source:** inventory R-C3.

### R-C4: MODEL_INVALID for tail-ON
- **What:** resolve --decision invalid is disabled; a physically invalid theta halts the campaign with no cache record and a retry repeats it.
- **Blocks:** Campaign progress past an invalid point.
- **Close by:** `BEFORE_CAMPAIGN`. **Owner:** Claude2 (later certified successor). **Filled by the V007 adoption:** NO.
- **Evidence:** wrapper 24abe3bc L95-118, L296-301.
- **Recommended disposition (RECOMMENDATION):** Decide before wave 1: accept halts if the headline probes all complete validly; otherwise commission a certified MODEL_INVALID rule, stricter where silent.
- **Label:** FORMAL. **Source:** inventory R-C4 + r9 TYPED_BLOCKERS.

### R-C5: Distinct review per D of the deciding-(iii) evidence
- **What:** Each D needs its pair evidence (from DIII4, which runs after the sealed ADOPT_TAIL), a distinct review, and root registration of the review sha and registry entry.
- **Blocks:** The 9 sensitivity runs at that D.
- **Close by:** `BEFORE_SENS`. **Owner:** Claude2 + a distinct-lane reviewer per D. **Filled by the V007 adoption:** NO.
- **Evidence:** sensitivity policy 8fb06600 L200-237; checker contract 47e23974.
- **Recommended disposition (RECOMMENDATION):** Assign a reviewer from a lane that did not produce the evidence; register the review sha in the R-B2 successor. This review sits between DIII4 and SENS (unestimated); in the DIII-early option it runs during the campaign.
- **Label:** FORMAL. **Source:** inventory R-C5 + dryplans SENSITIVITY_DECIDING_III_REQUIRED.

### R-C6: Register the S1 transfer test (S4-POST-S1)
- **What:** ADOPT_TAIL prescribes "V005 S1 transfer test at the calibrated point before prediction" (K=3 and K=4 at the calibrated point). No spec, threshold or reading exists for the tail scheme. The 0616 packet has no template for it: unregistered post-calibration S1 is outside the direct packet and needs its own admission (RUNBOOK_CX1V001/V003 step 1). It has no admitted launch path yet.
- **Blocks:** Step 5 prediction. Wall 5.42 h E / 8.97 h U for the 2 runs (UNTESTED).
- **Close by:** `BEFORE_CAMPAIGN`. **Owner:** Claude2. **Filled by the V007 adoption:** YES (the next-step text).
- **Evidence:** compare r11 a5d10cb1 L489-490; V005 prereg dbddc02c scope_untested S1; Codex1 templates_v002 limitations (TESTED from bytes); RUNBOOK_CX1V003 2eda3ebf step 1 and templates_v004 limitations (TESTED, fixlog/work/FIX_SOURCE_CHECKS_C4FX001.json).
- **Recommended disposition (RECOMMENDATION):** Register it target-free before the campaign result is read: cases, statistic, thresholds and reading; then add a guarded template, or a path root names in a V006 entry, with all four 0620 controls enforced before any process (the sealed ADOPT_TAIL, a root-published admission record, PRELAUNCH with the certificate checks, the r5 allowlist). Until then S4-POST-S1 has no admitted launch path and waits. Codex1 0074 lists the existing S4-POST-S1 and root contract adoption among the step-4 -> step-5 handoff's production blockers.
- **Label:** TESTED (text). **Source:** inventory R-C6 + Codex1 0065/0068.

### R-C7: Purpose, reading and schedule of the 18 sensitivity runs
- **What:** Nothing in step 4 consumes them; A23 ties them to bounding the D effect on NGC misses. Codex1's templates split them into SENS_LO9 and SENS_HI9, one batch at a time.
- **Blocks:** Their launch (recommended), and the freeze if A23 reads them.
- **Close by:** `BEFORE_SENS`. **Owner:** Claude2. **Filled by the V007 adoption:** NO.
- **Evidence:** 0533 B4-1; review r6 F3; A23 (V004 addendum 487d4449); templates_v002: SENS_LO 9 calls, SENS_HI 9 calls (TESTED from bytes).
- **Recommended disposition (RECOMMENDATION):** Register their reading before they run and schedule them after the campaign and after DIII4 and its review (default: SENS_LO9 then SENS_HI9, 6.97 h E / 13.81 h U each, UNTESTED), or defer them if no reading is registered.
- **Label:** FORMAL. **Source:** inventory R-C7 + Codex1 templates.

### R-C8: Campaign points outside the pre-registered set (registry growth)
- **What:** With a registry pinned (the certificate_policy gate requires one), prelaunch_check refuses every point that is not already in it, and make_plan calls prelaunch_check for every call of a wave. Adding a point changes tail_readiness, hence the cache id, and C4-2 then refuses the work dir. The engine proposes most of its up to 120 points from earlier results, so they cannot be registered in advance.
- **Blocks:** The campaign after its pre-registered points. Only the seed and the 3 Jacobian side points are fixed before any result (FORMAL reading of engine v003b: seed u, rel_step 0.05, box); every later point depends on earlier results.
- **Close by:** `BEFORE_CAMPAIGN`. **Owner:** Claude2 rules the design; builder: Codex2 was named but is out of usage (A103), so root reassigns; Claude-lineage review. **Filled by the V007 adoption:** NO.
- **Evidence:** wrapper 24abe3bc L52-55 (cache id includes tail_readiness), L59-66, L86-90, L172-181; v005 c75a889f L3293-3309 (make_plan; prelaunch_check per call at L3309), L59-63 and L3094-3100 (C4-2); registry probe v002 (REGISTRY_GROWTH_PROBE_C4V002.json 4cfc6283; fenced, plan-only, synthetic look-alikes): unregistered TAIL_REANCHOR, seed and an adaptive point all refuse CERTIFICATE_POINT_MISSING_OR_MISMATCHED; the cache id is 878d612a... with no registry, 4f0521aa... with the empty registry and b370470a... once the seed is registered (TESTED; values re-read from bytes in work/SOURCE_CHECKS_C4V002.json).
- **Recommended disposition (RECOMMENDATION):** Rule the design before wave 1 and build it in R-B3. Preferred: an append-only, hash-chained registry ledger in the work dir whose genesis and policy (producers, guard, rules) are what the config and the cache id bind; each new point gets its prelaunch bundle from approved producers when its wave is planned, and the ledger entry is verified at plan, cache put and cache reuse. Alternative: a box-wide prelaunch envelope accepted by the science review (per-point acceptance kept). Bridge: pre-register the 3 Jacobian side points (31 points, R-C1), so waves 1-2 (4 calls, about two call walls) run before the mechanism must exist; the campaign still stops at wave 3 without it.
- **Label:** TESTED (look-alike) / FORMAL (production). **Source:** launch_order V001 (new item) + F08 + 0620 + F12 (Jacobian option).

## D. Run decisions, root-only launches and operations

### R-D1: TAIL_REANCHOR source, and PC-7 against DU-1
- **What:** Fresh template run (default), DU-1 (the mapper-built trial spec, physical bitwise equal to the anchor) or DU-3 (the V007 C4T run). 0557 N-1 says the reanchor launches "from the template's physical values, not a mapper-built theta". PC-7 (FD noise floor: a repeat call at the anchor, outside the cache; OPEN in the coordinate spec) needs two calls at the anchor point.
- **Blocks:** The deciding_test row reanchor and config.anchor; PC-7 if root wants it met in step 4.
- **Close by:** `BEFORE_HEADLINE`. **Owner:** Claude2. **Filled by the V007 adoption:** PARTIAL (DU-3 uses the C4T run).
- **Evidence:** core a595c5c0 L149-157; 0557 16039954 N-1; reconcile RC-01 (one point key for RA, TRIAL and the anchor repeat, TESTED); coordinate spec 50e7288e PC-7 OPEN (TESTED from bytes).
- **Recommended disposition (RECOMMENDATION):** Default to a fresh template run (literal N-1). Use DU-1 only on an explicit ruling. PC-7 count: the default HEADLINE11 has three anchor-point calls (TAIL_REANCHOR, the WORKERS_8 anchor repeat, HEADLINE_TRIAL); DU-1 alone or DU-2 alone (10 runs) keeps two; DU-1 + DU-2 (9 runs) keeps one, so an added anchor repeat is needed if PC-7 must be met in step 4, and that cancels the saving of 9 over 10 runs (0.26 h E / 1.74 h U, UNTESTED).
- **Label:** FORMAL / TESTED. **Source:** inventory R-D1 + dryplans section 8 + reconcile OP1 + F12.

### R-D2: Designate the workers_8 row before launch
- **What:** Either the anchor repeat with another label (the default in Codex1's HEADLINE template, WORKERS_8_CANDIDATE_ANCHOR; dry-plan candidate 686ad07f; it also serves PC-7) or one headline corner run (DU-2).
- **Blocks:** The deciding_test document.
- **Close by:** `BEFORE_HEADLINE`. **Owner:** Claude2. **Filled by the V007 adoption:** NO.
- **Evidence:** core a595c5c0 L128-132, L189-191; templates_v002 HEADLINE call 2 = WORKERS_8_CANDIDATE_ANCHOR (TESTED from bytes).
- **Recommended disposition (RECOMMENDATION):** Default: the anchor repeat (HEADLINE11, 7.52 h E / 16.11 h U). DU-2 (designate C000 in a root entry before launch) gives HEADLINE10 (7.23 h / 15.55 h), saving 0.29 h E / 0.56 h U (UNTESTED); PC-7 stays met through TAIL_REANCHOR and HEADLINE_TRIAL.
- **Label:** FORMAL. **Source:** inventory R-D2 + dryplans WORKERS_8_SPEC_NOT_REGISTERED + Codex1 HEADLINE template.

### R-D3: Headline capability runs and the capability evidence
- **What:** Nine runs (trial + 2^3 corners at D 4.04); the evidence document binds their mapper-built spec shas under the final config.
- **Blocks:** driver_capability and adoption_regeneration.
- **Close by:** `AFTER_HEADLINE`. **Owner:** Claude2 (root-only launch). **Filled by the V007 adoption:** PARTIAL.
- **Evidence:** core a595c5c0 L313-340; wrapper L194-195.
- **Recommended disposition (RECOMMENDATION):** Launch them in the headline batch right after C1 with the registry frozen; write the evidence only from monitor-verified receipts.
- **Label:** FORMAL. **Source:** inventory R-D3 + dryplans CAPABILITY_EVIDENCE_PENDING.

### R-D4: deciding_test document and config.anchor
- **What:** Two rows {reanchor, workers_8}; config.anchor {result, receipt, spec_sha256} from S4-RA.
- **Blocks:** deciding_test and numerics_verdict (check_numerics takes the verified workers count from check_deciding).
- **Close by:** `AFTER_HEADLINE`. **Owner:** Claude2. **Filled by the V007 adoption:** NO.
- **Evidence:** core a595c5c0 L114-197; v005 c75a889f L1943-1947; dry plans adoption_world S5.
- **Recommended disposition (RECOMMENDATION):** Generate both from the receipts by script and self-check with check_deciding on a copy of the config before pinning.
- **Label:** FORMAL / TESTED. **Source:** inventory R-D4 + dryplans CONFIG_ANCHOR_TAIL_REANCHOR_PENDING.

### R-D5: Deciding-(iii) pairs: caps and placement, after the sealed ADOPT_TAIL
- **What:** 4 tail-OFF calls (2 D x {REFERENCE_V009GEO 237ef3d4, NEW_R5 b5cc62af}); 96 nodes, route A at 8 workers, uv_tail null, admit {} (spec bytes 3f8a4c04 / cf3f0086, TESTED). They launch only after the sealed ADOPT_TAIL, through the 0616 guard, with no overlap with step 2 or the campaign (0587, 0616, 0620; Codex1 0065: "All batches, including DIII, require the sealed ADOPT_TAIL under 0620"). The V001 pre-seal window is withdrawn (F01).
- **Blocks:** DIII evidence, hence the 18 sensitivity runs, their only consumer.
- **Close by:** `BEFORE_HEADLINE`. **Owner:** Claude2 (root-only launch). **Filled by the V007 adoption:** NO (but its launch waits for the sealed ADOPT_TAIL).
- **Evidence:** pair plan cb42a5a3; 0540 801d47fd F3 and A61 F3 say "root launches them during calibration prep"; neither says before the seal (REFUTE F01); 0587 fe54bb9f, 0616 634bca4e, 0620 037a2a61; Codex1 0065 6a676c7c; RUNBOOK_CX1V001 step 1 ("No raw campaign fallback or pre-seal DIII exception"); dry plans: 0 blockers (TESTED there); DIII specs: total_axis_nodes 96, route_a column_workers 8 (TESTED from bytes, work/SOURCE_CHECKS_C4V002.json).
- **Recommended disposition (RECOMMENDATION):** Caps, one value each: wall 43,200 s (the A67 precedent; 1.82x the 6.61 h U-adjusted solo projection and 1.76x the 6.82 h longest modelled call in the batch, UNTESTED); RSS 16 GiB (1.64x helper C's 9.75 GiB tail-OFF route-A model, meeting the 0538 >= 1.5x rule); output 96 GiB (helper C's 96-node model is 21.5 GiB typical and 57.7 GiB worst; the A67 32 GiB was set for 72-node runs and sits below that worst case). Default placement: after FINAL_SUMMARY and before SENS, so it adds nothing to the calibration path (4.61 h E / 7.77 h U, UNTESTED). Option: right after HEADLINE11, during H3 and before the campaign, so its evidence and review run during the campaign; that adds up to the same 4.61 h / 7.77 h to the calibration path if H3 is shorter. Record the placement in the V006 addendum (R-D14).
- **Label:** FORMAL / UNTESTED (caps fit, walls). **Source:** inventory R-D5 + launch_order V001 + F01 + F12 + Codex1 0065.

### R-D6: Sensitivity launch conditions
- **What:** Launch the 18 sensitivity runs only after their D is registered (R-C5) and their reading is registered (R-C7), as two guarded batches (SENS_LO9, SENS_HI9), one at a time.
- **Blocks:** The sensitivity batches.
- **Close by:** `BEFORE_SENS`. **Owner:** Claude2 (root-only launch). **Filled by the V007 adoption:** PARTIAL.
- **Evidence:** sensitivity policy 8fb06600 L205-237; templates_v002 runtime_constraints.one_step4_batch_at_a_time true (TESTED from bytes).
- **Recommended disposition (RECOMMENDATION):** As R-C7.
- **Label:** FORMAL. **Source:** inventory R-D6 + dryplans SENSITIVITY_DECIDING_III_REQUIRED + Codex1 templates.

### R-D7: Campaign scheduling
- **What:** Shipped: max_concurrent 1, process_budget 17 (hard maximum), stage-aware, 48 h per wave.
- **Blocks:** Campaign duration: 26.0 d E / 43.8 d U at max_concurrent 1 against 8.7 d / 14.9 d at 6 (UNTESTED; the 120-call, 21-wave model is an assumption, not measured adaptive behaviour).
- **Close by:** `BEFORE_CAMPAIGN`. **Owner:** Claude2. **Filled by the V007 adoption:** PARTIAL.
- **Evidence:** config 721c7230; v005 L171 PROCESS_BUDGET_MAX 17, L1724-1737; campaign d35d5d4a L186-230; SCHEDULE_SIM_C4V003.json.
- **Recommended disposition (RECOMMENDATION):** Set max_concurrent 6 (the nominal wave size) with budget 17 and stage-aware true; the 48 h wave cap then holds (longest modelled wave 10.4 h E / 17.5 h U), and at most 2 calls are in route A (modelled free memory >= 57.4%). Option for root: a reviewed successor raising PROCESS_BUDGET_MAX to 24 (5.6 d E / 11.2 d U; 3 calls in route A, modelled free >= 42.7%), which changes the v005 and campaign_c2v005 pins. Budget 48 is not memory-feasible under the 0538 model: 6 calls in route A model -1.4% free, and campaign_c2v005 has no memory gate.
- **Label:** FORMAL / UNTESTED. **Source:** inventory R-D7 + launch_order V001 + V002 memory model.

### R-D8: Caps for the direct tail-ON runs
- **What:** The reanchor, workers_8, capability and sensitivity runs launch before the C4-6 caps exist; the 0616 templates leave caps null and refuse until root supplies positive integers.
- **Blocks:** Every direct tail-ON launch.
- **Close by:** `BEFORE_HEADLINE`. **Owner:** Claude2. **Filled by the V007 adoption:** PARTIAL.
- **Evidence:** V007 plan V010 26f1ebf9 C4T caps 19 h / 28 GiB / 96 GiB (proposals); 0538 minimum RSS cap for 96-node K128 cases: 28 GiB; helper C model peak for this case class 18.79 GiB (caps_model.json row C4T, ship term): 28 GiB is 1.490x it, and 1.5 x 18.79 = 28.185 GiB; modelled per-call walls in U: HEADLINE11 up to 9.87 h (18 cores) / 13.04 h (12 cores); SENS 9-call batch up to 9.36 h / 11.54 h (SCHEDULE_SIM_C4V003.json, UNTESTED).
- **Recommended disposition (RECOMMENDATION):** Use the V007 C4T plan caps (19 h, 28 GiB, 96 GiB) for the direct tail-ON runs, then the C4-6 caps for the campaign; take 29 GiB if root wants the 1.5x margin over the model exactly.
- **Label:** UNTESTED (fit). **Source:** inventory R-D8 + V002 memory model.

### R-D9: Hull-miss contingency
- **What:** No bracket recovery in v006 and the block must equal the C4T numerics, so a miss under the full hull is a hard stop.
- **Blocks:** A corner or campaign point that misses.
- **Close by:** `BEFORE_HEADLINE`. **Owner:** Claude2. **Filled by the V007 adoption:** NO.
- **Evidence:** core a595c5c0 L240-243; review r5 8016cad0 (hull top margin about 2.5%, column 71 rfs 0.72%).
- **Recommended disposition (RECOMMENDATION):** Register the response now: record the miss, stop new launches of that theta, rule on a registration; never widen ad hoc.
- **Label:** FORMAL. **Source:** inventory R-D9.

### R-D10: Engine seed computed afresh
- **What:** The anchor alias is disabled, so wave 1 is a fresh seed call about 1e-15 off the anchor (its own point key 6944e210...).
- **Blocks:** Wave 1 (needs its registry entry, R-C1).
- **Close by:** `BEFORE_CAMPAIGN`. **Owner:** Claude2. **Filled by the V007 adoption:** NO.
- **Evidence:** core a595c5c0 L101-102; v005 L1785-1788; dry plans orchestrator plan (TESTED there).
- **Recommended disposition (RECOMMENDATION):** Accept the one extra call; register its point with the other 27.
- **Label:** FORMAL / TESTED. **Source:** inventory R-D10 + reconcile RC-02.

### R-D11: Operational settings for step 4
- **What:** A85.2-4 (QoS, sleep assertion) cover step 2 only. The 0616 packet carries normal QoS at root launch, single-thread BLAS, caffeinate -i -w <launcher pid>, and requires campaign and step-2 route-A inactivity; the campaign work dir is pinned on External1; the dry plans used an uncreated local work dir with volume null.
- **Blocks:** All step-4 launches (operations).
- **Close by:** `BEFORE_HEADLINE`. **Owner:** Claude2. **Filled by the V007 adoption:** NO.
- **Evidence:** A85; A95 (taskpolicy preferred, not required, for lanes); config work_dir_identity VolumeUUID 7752BF6F-EFA9-418D-AD80-29078B663078; templates_v002 runtime_constraints (TESTED from bytes).
- **Recommended disposition (RECOMMENDATION):** Apply the packet's settings to every direct batch and the same QoS and sleep assertion to the campaign launcher; ask lanes to use taskpolicy -b where allowed; keep External1 mounted and verify the real work dir and VolumeUUID with a plan-mode run on C2 before wave 1; keep every output. Output placement is R-D17.
- **Label:** TESTED (config) / FORMAL. **Source:** inventory R-D11 + dryplans harness note + Codex1 RUNBOOK_CX1V001.

### R-D12: Coordinate-spec preconditions still OPEN
- **What:** PC-1 (filled by the adoption), PC-5, PC-7 (FD noise floor by an anchor repeat), PC-9, D3 (disk retention, see R-D17), NGC slots, REVIEW.
- **Blocks:** The freeze (step 6) and possibly the campaign reading.
- **Close by:** `BEFORE_CAMPAIGN`. **Owner:** Claude2. **Filled by the V007 adoption:** PARTIAL (PC-1).
- **Evidence:** coordinates 50e7288e preconditions_before_freeze (TESTED from bytes).
- **Recommended disposition (RECOMMENDATION):** State which apply to step 4 and which wait for step 6. PC-7 is met in step 4 by the default HEADLINE11 or by DU-1 alone or DU-2 alone; DU-1 + DU-2 needs an added anchor repeat (R-D1). D3 is ruled with the disk plan (R-D17).
- **Label:** TESTED (text). **Source:** inventory R-D12 + F12.

### R-D13: ORIGINAL_K marked for evaluation before freeze
- **What:** The freeze writer refuses unless its evaluation is supplied or NOT_EVALUATED_BEFORE_FREEZE is recorded.
- **Blocks:** The freeze.
- **Close by:** `AFTER_CAMPAIGN`. **Owner:** Claude2. **Filled by the V007 adoption:** NO.
- **Evidence:** coordinates 50e7288e discrete_alternatives.alternative_notes.ORIGINAL_K.
- **Recommended disposition (RECOMMENDATION):** Decide at the end of step 4 whether to evaluate it in step 5 or record NOT_EVALUATED_BEFORE_FREEZE.
- **Label:** TESTED (text) / UNTESTED (applicability). **Source:** inventory R-D13.

### R-D14: V006 addendum for the step-4 rulings, and the A82 no-write hazard for the whole campaign
- **What:** A82: once the V005 file is frozen, every later root entry (steps 4-7) goes into a new V006 addendum. The calibration adoption policy (7c726fa2 L56-59) reads PIN_ADDENDUM_V005 from the sealed compare and re-reads that path from bytes against the frozen sha, at every Context construction and every pre-wave fresh_gates (v005 L1943-1947 recompute numerics_verdict). If the sealed compare cites the open V005 path, one root write to it after the freeze closes numerics_verdict for every later campaign wave. A99.6 confirmed the hazard live for the compare.
- **Blocks:** Recording of every R-* ruling, and numerics_verdict for every campaign wave if the hazard is not held.
- **Close by:** `BEFORE_SEAL`. **Owner:** Claude2. **Filled by the V007 adoption:** NO.
- **Evidence:** A82 and A99.6 (addendum copy 70a48f51 in this folder); adoption policy 7c726fa2 L56-59 (O.read_pinned of the addendum path; FORMAL, read from bytes); v005 c75a889f L1943-1947 (fresh_gates; FORMAL, cited by F13).
- **Recommended disposition (RECOMMENDATION):** Hold the A82 no-write rule on the open V005 file for the whole campaign (8.7 d E / 14.9 d U modelled, UNTESTED) and up to step 4's last numerics_verdict read, or have the sealed compare (and through it the calibration adoption policy) cite the _FROZEN.md copy. Record step-4 rulings in V006 after the freeze: the DIII placement (R-D5), the R-D1/R-D2 designations, the route-A cap (R-D8), the disk plan (R-D17), the campaign and S4-POST-S1 launch paths (R-B4, R-C6, under 0620) and the CP-1 window (R-C1).
- **Label:** FORMAL. **Source:** inventory R-D14 + F13 + A99.6.

### R-D15: One machine-wide schedule across launchers
- **What:** campaign_c2v005 and a direct-run launcher each account for their own processes only. The 0616 packet requires campaign and step-2 route-A inactivity and holds a flock against other packet instances, not unrelated launchers; root attests machine-wide occupancy.
- **Blocks:** Campaign and sensitivity timing; memory headroom; the start of step 5.
- **Close by:** `BEFORE_CAMPAIGN`. **Owner:** Claude2. **Filled by the V007 adoption:** NO.
- **Evidence:** campaign d35d5d4a L186-230 (budget counts its own calls only); RUNBOOK_CX1V001 step 7; templates_v002 runtime_constraints (TESTED from bytes); dispatch 0631 (044628c9); Codex1 0074 (WAIT_FOR_FULL_STEP4_DECISION, TESTED text).
- **Recommended disposition (RECOMMENDATION):** Run one direct batch at a time and none while the campaign runs (DIII4 included); if root wants overlap, lower the campaign process_budget explicitly for that period and re-run the memory model. Step 5 (NGC route A/B) waits for the full step-4 decision under the current producers (dispatch 0631; Codex1 0074: WAIT_FOR_FULL_STEP4_DECISION), so its runs follow FINAL_SUMMARY and then share the machine with S4-POST-S1, DIII4 and SENS: put them in the same machine-wide schedule.
- **Label:** FORMAL / RECOMMENDATION. **Source:** launch_order V001 (new item) + Codex1 RUNBOOK_CX1V001 step 7.

### R-D16: Where the per-D sensitivity registration lives
- **What:** The per-D entries live in config.tail_readiness.sensitivity_deciding_iii, and tail_readiness is in the cache id; a change during the campaign forces a new work dir (C4-2).
- **Blocks:** Campaign continuity if the DIII evidence lands after wave 1 (always, in the default placement).
- **Close by:** `BEFORE_CAMPAIGN`. **Owner:** Claude2. **Filled by the V007 adoption:** NO.
- **Evidence:** wrapper 24abe3bc L52-55; registry probe v002 (a tail_readiness change changes the cache id, TESTED).
- **Recommended disposition (RECOMMENDATION):** Keep the per-D entries in a sibling config used only for the standalone sensitivity prelaunch checks; never edit the campaign config mid-campaign. Put them into C2 only in the DIII-early option and only if they are final before the campaign starts.
- **Label:** TESTED / FORMAL. **Source:** launch_order V001 (new item).

### R-D17: Disk plan and output placement for step 4 (and D3 retention)
- **What:** Every step-4 output is kept (the ~17:50Z intermediate-cleanup authorization is NOT USED, ~18:40Z). Per call: 5.66 GiB measured for a tail-OFF anchor call (config disk_guard.measured_per_call_bytes, TESTED from config bytes, not re-measured); 21.5 GiB typical and 57.7 GiB worst in helper C's 96-node model (UNTESTED). Projection for 155 calls (151 tail-ON + 4 tail-OFF; the 120-call campaign is an assumption): 877.8 GiB measured-based, 3332.5 GiB (3.25 TiB) typical, 8943.5 GiB (8.73 TiB) worst (UNTESTED). Free at 2026-10-18T21:27:39Z (TESTED, df -k, work/MACHINE_READINGS_C4V002.txt): internal 454.1 GiB, External1 3273.2 GiB (3.20 TiB). The 33 direct calls alone need 709.5 GiB typical, more than the internal SSD's free space.
- **Blocks:** Every direct batch (output paths are mandatory template fields) and the campaign (the D3 retention rule is needed before the volume nears External1's free space).
- **Close by:** `BEFORE_HEADLINE`. **Owner:** Claude2. **Filled by the V007 adoption:** NO.
- **Evidence:** principal ~18:20Z (CURRENT_INSTRUCTIONS): new large outputs go to External1, naming future calibration runs; config work_dir on External1, VolumeUUID 7752BF6F (TESTED from config bytes); A85.3 and A99 V6-S2: the V007 step-2 outputs go on the internal SSD (step 2 only); Codex1 templates_v002 runtime_constraints.root_selected_internal_ssd_outputs = true; RUNBOOK_CX1V001 step 6 ("root-selected internal-SSD placement"); caps_model.json C4T row out_typ_GiB 21.5, out_worst_GiB 57.7 (UNTESTED model); coordinate spec 50e7288e D3 "disk retention rule (root)" OPEN (TESTED from bytes).
- **Recommended disposition (RECOMMENDATION):** Rule per class before H2. Default: External1 for HEADLINE11, DIII4, SENS_LO9, SENS_HI9 and S4-POST-S1, under one fresh step-4 run root with distinct per-call outdirs, receipts and logs; the campaign work dir as in the config (External1). The internal SSD only by explicit ruling (Codex1's template default asks for it), and only for a class whose disk guard fits. Disk guard for every direct batch: at admission, free bytes on the output volume >= calls x output cap + 20 GiB (the config reserve), and before each start >= one output cap + 20 GiB, refusing otherwise; with 96 GiB caps that is 1076 GiB for HEADLINE11, 884 GiB per SENS batch, 404 GiB for DIII4 and 212 GiB for POST-S1. Rule D3 before the campaign: at the typical model the step-4 total (3.25 TiB) exceeds External1's free space (3.20 TiB).
- **Label:** TESTED (free space, config) / UNTESTED (volume model). **Source:** V002 new item (F07).

## Traceability

| from | code or item | final item |
|---|---|---|
| inventory | R-A1 | R-A1 |
| inventory | R-A2 | R-A2 |
| inventory | R-A3 | R-A3 |
| inventory | R-A4 | R-A4 |
| inventory | R-A5 | R-A5 |
| inventory | R-B1 | R-B1 |
| inventory | R-B2 | R-B2 |
| inventory | R-B3 | R-B3 |
| inventory | R-B4 | R-B4 |
| inventory | R-B5 | R-B5 |
| inventory | R-C1 | R-C1 |
| inventory | R-C2 | R-C2 |
| inventory | R-C3 | R-C3 |
| inventory | R-C4 | R-C4 |
| inventory | R-C5 | R-C5 |
| inventory | R-C6 | R-C6 |
| inventory | R-C7 | R-C7 |
| inventory | R-D1 | R-D1 |
| inventory | R-D2 | R-D2 |
| inventory | R-D3 | R-D3 |
| inventory | R-D4 | R-D4 |
| inventory | R-D5 | R-D5 |
| inventory | R-D6 | R-D6 |
| inventory | R-D7 | R-D7 |
| inventory | R-D8 | R-D8 |
| inventory | R-D9 | R-D9 |
| inventory | R-D10 | R-D10 |
| inventory | R-D11 | R-D11 |
| inventory | R-D12 | R-D12 |
| inventory | R-D13 | R-D13 |
| inventory | R-D14 | R-D14 |
| ROOT_ITEMS_FINAL V001 | R-A1 | R-A1 |
| ROOT_ITEMS_FINAL V001 | R-A2 | R-A2 |
| ROOT_ITEMS_FINAL V001 | R-A3 | R-A3 |
| ROOT_ITEMS_FINAL V001 | R-A4 | R-A4 |
| ROOT_ITEMS_FINAL V001 | R-A5 | R-A5 |
| ROOT_ITEMS_FINAL V001 | R-A6 | R-A6 |
| ROOT_ITEMS_FINAL V001 | R-B1 | R-B1 |
| ROOT_ITEMS_FINAL V001 | R-B2 | R-B2 |
| ROOT_ITEMS_FINAL V001 | R-B3 | R-B3 |
| ROOT_ITEMS_FINAL V001 | R-B4 | R-B4 |
| ROOT_ITEMS_FINAL V001 | R-B5 | R-B5 |
| ROOT_ITEMS_FINAL V001 | R-B6 | R-B6 |
| ROOT_ITEMS_FINAL V001 | R-C1 | R-C1 |
| ROOT_ITEMS_FINAL V001 | R-C2 | R-C2 |
| ROOT_ITEMS_FINAL V001 | R-C3 | R-C3 |
| ROOT_ITEMS_FINAL V001 | R-C4 | R-C4 |
| ROOT_ITEMS_FINAL V001 | R-C5 | R-C5 |
| ROOT_ITEMS_FINAL V001 | R-C6 | R-C6 |
| ROOT_ITEMS_FINAL V001 | R-C7 | R-C7 |
| ROOT_ITEMS_FINAL V001 | R-C8 | R-C8 |
| ROOT_ITEMS_FINAL V001 | R-D1 | R-D1 |
| ROOT_ITEMS_FINAL V001 | R-D2 | R-D2 |
| ROOT_ITEMS_FINAL V001 | R-D3 | R-D3 |
| ROOT_ITEMS_FINAL V001 | R-D4 | R-D4 |
| ROOT_ITEMS_FINAL V001 | R-D5 | R-D5 |
| ROOT_ITEMS_FINAL V001 | R-D6 | R-D6 |
| ROOT_ITEMS_FINAL V001 | R-D7 | R-D7 |
| ROOT_ITEMS_FINAL V001 | R-D8 | R-D8 |
| ROOT_ITEMS_FINAL V001 | R-D9 | R-D9 |
| ROOT_ITEMS_FINAL V001 | R-D10 | R-D10 |
| ROOT_ITEMS_FINAL V001 | R-D11 | R-D11 |
| ROOT_ITEMS_FINAL V001 | R-D12 | R-D12 |
| ROOT_ITEMS_FINAL V001 | R-D13 | R-D13 |
| ROOT_ITEMS_FINAL V001 | R-D14 | R-D14 |
| ROOT_ITEMS_FINAL V001 | R-D15 | R-D15 |
| ROOT_ITEMS_FINAL V001 | R-D16 | R-D16 |
| dry plans (per spec) | CAPABILITY_EVIDENCE_PENDING | R-D3 |
| dry plans (per spec) | CERTIFICATE_POLICY_PENDING | R-C1 |
| dry plans (per spec) | COMPARATOR_A68_SUCCESSOR_REQUIRED | R-B2 |
| dry plans (per spec) | CONFIG_ANCHOR_TAIL_REANCHOR_PENDING | R-D4 |
| dry plans (per spec) | SENSITIVITY_DECIDING_III_REQUIRED | R-B2, R-C5, R-D5, R-D6 |
| dry plans (per spec) | WORKERS_8_SPEC_NOT_REGISTERED | R-D2 |
| dry plans (per spec, re-read under F03) | PENDING_UV_TAIL_CERTIFICATE | R-C1 for the 27 non-anchor tail-ON specs; the 3 anchor-point specs take the V007 adoption values through the R-C1 registry entry (A73: slots are left to the certificate registry) |
| dry plans (campaign gate) | numerics_verdict | R-A1 (V007 pins) |
| dry plans (campaign gate) | numerics_verdict / seal allowlist | R-A2, R-B3 |
| dry plans (campaign gate) | adoption_regeneration | R-A4, R-A5 |
| dry plans (campaign gate) | deciding_test | R-D1, R-D2, R-D4 |
| dry plans (campaign gate) | driver_capability | R-D3 |
| dry plans (campaign gate) | certificate_policy | R-C1 |
| dry plans (campaign gate) | u_i_carrier | R-C2 |
| dry plans (cross-lane) | V007_PREREG_BINDING_INPUTS_CASE_BLOCK_ABSENT | R-A3 (closing: bound in prereg r5) |
| dry plans (cross-lane) | ORCHESTRATOR_V006R9_R5_ONLY_UNDER_AN_R6_SEAL | R-B1 (moot after A96) |
| dry plans (problems) | R6 BUILD not landed | R-B1 |
| dry plans (problems) | spec bytes change after adoption / registry | R-A1, R-A4, R-C1 |
| dry plans (problems) | production work dir untested (uncreated local dir) | R-D11, R-D17 |
| dry plans (problems) | ADOPT_TAIL None uncertainty rows (S7) | R-A6 |

Unmapped dry-plan codes: none. Inventory items not carried: none. V001 items not carried: none. Fence blocks in this generator: none.
