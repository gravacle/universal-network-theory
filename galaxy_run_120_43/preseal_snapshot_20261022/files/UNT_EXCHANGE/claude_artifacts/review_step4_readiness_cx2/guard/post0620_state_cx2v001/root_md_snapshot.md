# Step-4 root items, final merged list (dispatch 0587, part 4)

Claude4 helper, 2026-10-18T20:06:50Z (`date -u` at generation). Machine-readable twin: `work/ROOT_ITEMS_FINAL_C4V001.json` (sha256 `100bec5960d26d2c40e405d017c4bb79b6a613674a0516af423476c0ccbfa707`). Root (Claude2) alone decides and launches; every disposition below is a **RECOMMENDATION**. Labels: **TESTED** (recomputed from bytes or by a fenced plan-only probe), **FORMAL** (code or rulings, file:line cited), **UNTESTED** (projections, fit, future behaviour). Shas are shown as 8-hex prefixes of values computed from bytes; full values are in the JSON and in `work/SOURCE_PINS_C4V001.txt`.

**What was merged.** All 31 items of `../inventory/ROOT_ITEMS_C4V001.json` (a48ca79d) are carried under their ids; every non-V007 blocker of `../dryplans/DRYPLANS_C4V002.json` (756d36ec) maps to an item (traceability at the end); five items are new: R-A6 (from the dry plans' adoption world S7), R-B6, R-C8, R-D15 and R-D16 (found in this part). Rulings newer than both lists are applied: A92 (c2v007r2 is the identity-comparator slot), A96 (V007 seals on r5; r6 unfinished and unused) and the frozen compare r12 (4bd7b262). 36 items in all.

## Summary

| id | item | close by | owner | filled by V007 | source |
|---|---|---|---|---|---|
| R-A3 | Case-block binding in the sealed prereg (seal-blocking) | BEFORE_SEAL | Claude2 at seal assembly; prereg author Claude4; compare owner Codex3 | MUST BE IN THE SEALED PREREG | inventory R-A3 + dryplans DEFECT (found independently by both) |
| R-A6 | Finite carried uncertainty in the ADOPT_TAIL report | BEFORE_SEAL | Codex3 (compare) + Claude2 | YES (the verdict carries it) | dryplans adoption_world S7 (new item) |
| R-B2 | Deciding-(iii) comparator successor on c2v007r2 | BEFORE_SEAL | Codex2 (sensitivity policy); Codex1 (c2v007r2 unchanged per 0611); cross-lineage reviewer | NO | inventory R-B2 + dryplans COMPARATOR_A68_SUCCESSOR_REQUIRED + A92/0611 |
| R-B3 | One v006r10 cascade with a single delta review | BEFORE_SEAL | Claude2; builder Codex2; distinct reviewer | PARTIAL (tuple line) | inventory R-B3 + launch_order |
| R-B4 | Launch entries | BEFORE_SEAL | Claude2; builder any lane; distinct review | NO | inventory R-B4 + dryplans campaign gates |
| R-D14 | V006 addendum for the step-4 rulings | BEFORE_SEAL | Claude2 | NO | inventory R-D14 |
| R-D5 | Deciding-(iii) pairs: caps and launch window | BEFORE_SEAL | Claude2 (root-only launch) | NO | inventory R-D5 + launch_order |
| R-B6 | Step-4 direct-run launcher successor (V005 pattern) | BEFORE_HEADLINE | Claude2; builder Codex1 (author of the V005 packet); Claude4 delta check | NO | launch_order (new item) |
| R-C1 | Per-point certificate admission and the registry (28 points) | BEFORE_HEADLINE | Claude2 science review; Codex2 producers; distinct reviewer | NO (keys depend on the block and driver) | inventory R-C1 + dryplans CERTIFICATE_POLICY_PENDING + reconcile RC-02/03 |
| R-D1 | TAIL_REANCHOR source | BEFORE_HEADLINE | Claude2 | PARTIAL (DU-3 uses the C4T run) | inventory R-D1 + dryplans section 8 + reconcile OP1 |
| R-D11 | Operational settings for step 4 | BEFORE_HEADLINE | Claude2 | NO | inventory R-D11 + dryplans harness note |
| R-D2 | Designate the workers_8 row before launch | BEFORE_HEADLINE | Claude2 | NO | inventory R-D2 + dryplans WORKERS_8_SPEC_NOT_REGISTERED |
| R-D8 | Caps for the direct runs | BEFORE_HEADLINE | Claude2 | PARTIAL | inventory R-D8 |
| R-D9 | Hull-miss contingency | BEFORE_HEADLINE | Claude2 | NO | inventory R-D9 |
| R-A1 | Config successor C1 from the sealed ADOPT_TAIL | AT_T0 | Claude2 | YES | inventory R-A1 + dryplans post_adoption_probe |
| R-A2 | Seal tuple into APPROVED_V007_SEALS | AT_T0 | Claude2 + distinct reviewer; builder Codex2 | YES | inventory R-A2 + dryplans campaign gate (seal allowlist) |
| R-A4 | C4-6 adoption derivation | AFTER_HEADLINE | Claude2 + distinct reviewer | PARTIAL | inventory R-A4 + dryplans campaign gate adoption_regeneration |
| R-A5 | Caps regenerated from the measured C4T use | AFTER_HEADLINE | Claude2 | PARTIAL | inventory R-A5 + launch_order (TIMING_V003 under-count) |
| R-C2 | u_i carrier declaration | AFTER_HEADLINE | Claude2 | PARTIAL | inventory R-C2 + dryplans campaign gate u_i_carrier |
| R-D3 | Headline capability runs and the capability evidence | AFTER_HEADLINE | Claude2 (root-only launch) | PARTIAL | inventory R-D3 + dryplans CAPABILITY_EVIDENCE_PENDING |
| R-D4 | deciding_test document and config.anchor | AFTER_HEADLINE | Claude2 | NO | inventory R-D4 + dryplans CONFIG_ANCHOR_TAIL_REANCHOR_PENDING |
| R-B5 | Post-state certificate loop per campaign call | BEFORE_CAMPAIGN | Claude2 + Codex2 (producers) | NO | inventory R-B5 |
| R-C3 | Taxonomy approval and root judgment calls | BEFORE_CAMPAIGN | Claude2 + distinct reviewer | NO | inventory R-C3 |
| R-C4 | MODEL_INVALID for tail-ON | BEFORE_CAMPAIGN | Claude2 (later certified successor) | NO | inventory R-C4 + r9 TYPED_BLOCKERS |
| R-C6 | Register the S1 transfer test (S4-POST-S1) | BEFORE_CAMPAIGN | Claude2 | YES (the next-step text) | inventory R-C6 |
| R-C8 | Campaign points outside the pre-registered set (registry growth) | BEFORE_CAMPAIGN | Claude2 rules the design; Codex2 builds; Claude-lineage review | NO | launch_order (new item; neither list raised it) |
| R-D10 | Engine seed computed afresh | BEFORE_CAMPAIGN | Claude2 | NO | inventory R-D10 + reconcile RC-02 |
| R-D12 | Coordinate-spec preconditions still OPEN | BEFORE_CAMPAIGN | Claude2 | PARTIAL (PC-1) | inventory R-D12 |
| R-D15 | One machine-wide schedule across launchers | BEFORE_CAMPAIGN | Claude2 | NO | launch_order (new item) |
| R-D16 | Where the per-D sensitivity registration lives | BEFORE_CAMPAIGN | Claude2 | NO | launch_order (new item) |
| R-D7 | Campaign scheduling | BEFORE_CAMPAIGN | Claude2 | PARTIAL | inventory R-D7 + launch_order |
| R-C5 | Distinct review per D of the deciding-(iii) evidence | BEFORE_SENS | Claude2 + a distinct-lane reviewer per D | NO | inventory R-C5 + dryplans SENSITIVITY_DECIDING_III_REQUIRED |
| R-C7 | Purpose, reading and schedule of the 18 sensitivity runs | BEFORE_SENS | Claude2 | NO | inventory R-C7 |
| R-D6 | Sensitivity launch conditions | BEFORE_SENS | Claude2 (root-only launch) | PARTIAL | inventory R-D6 + dryplans SENSITIVITY_DECIDING_III_REQUIRED |
| R-D13 | ORIGINAL_K marked for evaluation before freeze | AFTER_CAMPAIGN | Claude2 | NO | inventory R-D13 |
| R-B1 | Driver of record: r5 (settled for V007 by A96) | CLOSED_BY_RULING | Claude2 | YES (driver slot) | inventory R-B1 + dryplans R6 DEFERRED + A96 |

Close-by legend: `BEFORE_SEAL` = phase P, before the V007 seal (no V007 dependency); `BEFORE_HEADLINE` = before the headline batch (can close before the seal); `AT_T0` = H1, right after the sealed ADOPT_TAIL; `AFTER_HEADLINE` = H3, from the headline receipts; `BEFORE_CAMPAIGN` = before campaign wave 1; `BEFORE_SENS` = before the sensitivity batch; `AFTER_CAMPAIGN` = after the campaign, before the freeze; `CLOSED_BY_RULING` = closed by a ruling.

**Most likely to delay step 4 (RECOMMENDATION, from the dependency chain):** R-A3, R-C8, R-C1, R-B3, R-B6, R-B4, R-B5, R-D7, R-A5, R-B2. R-A3 can stop the V007 verdict itself. R-C8 stops the campaign after its pre-registered points. R-C1 and R-B6 gate the headline batch. R-B3/R-B4/R-B5 gate the campaign machinery. R-D7 sets the campaign length (8.7 d E / 14.9 d U at max_concurrent 6, against 26.0 / 43.8 d as shipped; UNTESTED).

## A. V007 adoption pins and the seal interface

### R-A1: Config successor C1 from the sealed ADOPT_TAIL
- **What:** Write numerics.{verdict_artifact, block_source, compare, sealed_prereg, adopted_result, source_results} and numerics.block := the sealed C4T call-spec numerics exactly (its eps/lo slots included).
- **Blocks:** Every tail-ON run (launch bytes are regenerated under C1) and the numerics_verdict gate.
- **Close by:** `AT_T0`. **Owner:** Claude2. **Filled by the V007 adoption:** YES.
- **Evidence:** adoption policy 7c726fa2 L90-91 (block == C4T numerics); config 721c7230 fields null (TESTED, inventory); dry plans post_adoption_probe: 30/30 specs normalize with 0 pending after the fill (TESTED there); provisional bytes TAIL_REANCHOR 924851c4, HEADLINE_TRIAL 7d9a8d47, seed 854e1291; registry probe v002 here reproduced the seed sha 854e129191b6b024d47b200a70df1d96098d27ef7628c6a727554929141e4bd9 with the A70 slot records (TESTED).
- **Recommended disposition (RECOMMENDATION):** Prepare C1 now as a template differing from r9 only in these fields, the block and the R-C1/R-C2/R-D8 fields. At T0 fill it, check it by key diff, regenerate the launch bytes plan-only, and require that any point whose registry slots are the A70 records reproduces its dry-plan PROVISIONAL sha.
- **Label:** FORMAL / TESTED. **Source:** inventory R-A1 + dryplans post_adoption_probe.

### R-A2: Seal tuple into APPROVED_V007_SEALS
- **What:** The shipped allowlist is an empty frozenset; the tuple (compare sha, prereg sha, frozen addendum sha, report schema, verdict sha) enters only through an immutable policy successor, which forces core and wrapper successors.
- **Blocks:** numerics_verdict gate, hence the campaign. Not the direct runs.
- **Close by:** `AT_T0`. **Owner:** Claude2 + distinct reviewer; builder Codex2. **Filled by the V007 adoption:** YES.
- **Evidence:** adoption policy 7c726fa2 L9-12; core a595c5c0 L200-203; wrapper 24abe3bc L27; dry plans adoption_world S1 refuses only on V007_SEAL_NOT_IN_REVIEWED_ALLOWLIST; S2 passes with the tuple in memory (TESTED there).
- **Recommended disposition (RECOMMENDATION):** Build it inside the R-B3 cascade now with a one-line placeholder; at T0 insert the tuple and verify by line diff (the RI-27 pattern), so no full review sits after the seal.
- **Label:** TESTED / FORMAL. **Source:** inventory R-A2 + dryplans campaign gate (seal allowlist).

### R-A3: Case-block binding in the sealed prereg (seal-blocking)
- **What:** Prereg r4 binding_inputs has no case_block. The sealed compare takes the case block only from there; the adoption policy reads the same binding.
- **Blocks:** The sealed V007 verdict itself, hence all of step 4.
- **Close by:** `BEFORE_SEAL`. **Owner:** Claude2 at seal assembly; prereg author Claude4; compare owner Codex3. **Filled by the V007 adoption:** MUST BE IN THE SEALED PREREG.
- **Evidence:** prereg r4 e3b6b5b2 key walk: no case_block (TESTED, inventory work/CASE_BLOCK_CHECK_C4V001.json); compare r11 a5d10cb1 L5689-5697; frozen compare r12 4bd7b262 L5705-5714: sealed mode refuses CASE_BLOCK_ABSENT (FORMAL, read from bytes here at 2026-10-18T20:01:37Z); adoption policy 7c726fa2 L74-77; dry plans adoption_world S3 V007_CASE_BLOCK_NOT_BOUND_BY_SEALED_PREREG (TESTED there).
- **Recommended disposition (RECOMMENDATION):** Treat as blocking for the seal. Bind a registered, target-free case block through a prereg successor or an RI-26 seal note, and run r12 in sealed mode on it in the 0602 seal rehearsal.
- **Label:** TESTED (absence) / FORMAL (requirement). **Source:** inventory R-A3 + dryplans DEFECT (found independently by both).

### R-A4: C4-6 adoption derivation
- **What:** Schema DDO154_CALIBRATION_ADOPTION_DERIVATION_C2V005 plus the wrapper tail bindings: verdict, adopted C4T case and spec, base and seed spec shas, capability evidence, timing model, monitor-verified receipts, caps above measured use, disk guard, registry.
- **Blocks:** adoption_regeneration gate, hence the campaign.
- **Close by:** `AFTER_HEADLINE`. **Owner:** Claude2 + distinct reviewer. **Filled by the V007 adoption:** PARTIAL.
- **Evidence:** v005 c75a889f L1828-1926; wrapper 24abe3bc L183-197 (needs driver_capability ok); dry plans: base and seed shas must come from the post-adoption config (spec bytes change after adoption, TESTED there).
- **Recommended disposition (RECOMMENDATION):** Write and review a target-free generator now; run it after the headline batch on C1 bytes; pin its output in C2.
- **Label:** FORMAL. **Source:** inventory R-A4 + dryplans campaign gate adoption_regeneration.

### R-A5: Caps regenerated from the measured C4T use
- **What:** Config per-call caps are 8 h wall, 64 GiB RSS, 12 GiB output; C4-6 refuses caps that are not above the measured use.
- **Blocks:** adoption_regeneration; campaign calls that run past the wall cap would stop.
- **Close by:** `AFTER_HEADLINE`. **Owner:** Claude2. **Filled by the V007 adoption:** PARTIAL.
- **Evidence:** config 721c7230 per_call / disk_guard (TESTED, inventory); TIMING_V003 3e3fb600 keeps the I=7 route-A baseline in its I=32 total; scaled, the upper call is 8.74-8.77 h solo, above the 8 h cap (TESTED arithmetic, work/SCHEDULE_SIM_C4V002.json); load ratios 1.69-2.99 (TIMING_V003 calibration rows).
- **Recommended disposition (RECOMMENDATION):** Wall cap at least 2x the C4T measured elapsed and at least the upper projection times the measured load ratio; RSS at least 1.5x the C4T peak; output cap at least 1.5x the C4T output; disk_guard.per_call_bytes at least the output cap.
- **Label:** TESTED (values, arithmetic) / UNTESTED (fit). **Source:** inventory R-A5 + launch_order (TIMING_V003 under-count).

### R-A6: Finite carried uncertainty in the ADOPT_TAIL report
- **What:** The adoption refuses V007_CARRIED_UNCERTAINTY_REQUIRED if a carried_numerical_uncertainty_km_s row is None; compare r11 L4781 allows None rows.
- **Blocks:** numerics_verdict on an otherwise valid ADOPT_TAIL.
- **Close by:** `BEFORE_SEAL`. **Owner:** Codex3 (compare) + Claude2. **Filled by the V007 adoption:** YES (the verdict carries it).
- **Evidence:** dry plans adoption_world S7 (TESTED on look-alikes there); compare r11 a5d10cb1 L4781 (FORMAL, cited by the dry plans).
- **Recommended disposition (RECOMMENDATION):** Confirm in the seal rehearsal that an ADOPT_TAIL report always carries finite rows, or rule how a None row is read and put that rule in the R-B3 policy successor.
- **Label:** TESTED (look-alike) / UNTESTED (real report). **Source:** dryplans adoption_world S7 (new item).

## B. Driver, successors and launch machinery

### R-B1: Driver of record: r5 (settled for V007 by A96)
- **What:** A96 (19:51Z): V007 seals on v010 r5 b5cc62af; the r6 build was stopped and its bytes are unfinished and unused; caching for steps 4-5 is decided later with the A85.1 result.
- **Blocks:** Nothing now. v006r9 requires r5, so step 4 runs on r5.
- **Close by:** `CLOSED_BY_RULING`. **Owner:** Claude2. **Filled by the V007 adoption:** YES (driver slot).
- **Evidence:** A96 in the open V005 addendum 991cc242 (snapshot 1952Z); core a595c5c0 L25; wrapper 24abe3bc L47-48; driver_r6/ listing 19:37Z: no BUILD.md, no manifest (TESTED).
- **Recommended disposition (RECOMMENDATION):** Run every step-4 call on r5. A cache or parallel-tail driver for steps 4-5 later needs its own identity gates, an orchestrator retarget successor, re-keyed registry points (the driver sha is in every point key) and a deciding-(iii) new side or a B0 transfer ruling. r6 dry plans stay DEFERRED (tooling ready in ../dryplans/tools).
- **Label:** TESTED / FORMAL. **Source:** inventory R-B1 + dryplans R6 DEFERRED + A96.

### R-B2: Deciding-(iii) comparator successor on c2v007r2
- **What:** The pair plan and sensitivity policy pin the c2v004-derived comparator (FAIL, A68); compute_pair refuses while COMPARATOR_A68_REVIEWED is False and REGISTERED_DISTINCT_REVIEW_SHA256 is empty. Since A92, c2v007r2 (052da0fe) is the identity-comparator slot of record.
- **Blocks:** DIII evidence, hence the 18 sensitivity runs. Not the DIII launches.
- **Close by:** `BEFORE_SEAL`. **Owner:** Codex2 (sensitivity policy); Codex1 (c2v007r2 unchanged per 0611); cross-lineage reviewer. **Filled by the V007 adoption:** NO.
- **Evidence:** sensitivity policy 8fb06600 L19-40, L185-203; pair plan cb42a5a3; A92; 0611 (comparator source must not change); c2v007r2 052da0fe, BUILD_R2 d02e4637 (TESTED hashes).
- **Recommended disposition (RECOMMENDATION):** One policy successor that re-pins the pair plan and policy to c2v007r2 through an r5 custody adapter outside the comparator (as the c2v004-r5 adapter did), with a validate_report for its schema; COMPARATOR_A68_REVIEWED set only after that adapter is reviewed. Confirm that the two-driver comparison (v009-GEO vs v010 r5) is in c2v007r2's supported scope.
- **Label:** TESTED (pins) / FORMAL. **Source:** inventory R-B2 + dryplans COMPARATOR_A68_SUCCESSOR_REQUIRED + A92/0611.

### R-B3: One v006r10 cascade with a single delta review
- **What:** Policy, core and wrapper successors carrying R-A2 (placeholder), R-B2, R-C8, R-B4 and R-A6 if needed. Every config change is a new cache id (C4-2).
- **Blocks:** The campaign gates.
- **Close by:** `BEFORE_SEAL`. **Owner:** Claude2; builder Codex2; distinct reviewer. **Filled by the V007 adoption:** PARTIAL (tuple line).
- **Evidence:** wrapper 24abe3bc L27-30 byte pins; v005 c75a889f C4-2 L59-63.
- **Recommended disposition (RECOMMENDATION):** Build it now, leaving only the tuple line for after the seal. Add a regression test: under the same config, r10 Mapper.build must give byte-identical specs to r9 for the 9 probe points and the seed (otherwise capability evidence and cached keys would not match).
- **Label:** FORMAL. **Source:** inventory R-B3 + launch_order.

### R-B4: Launch entries
- **What:** v006r9 exposes plan and wave only; Orchestrator.run needs a session leader (launch_setsid_c2v005). Root also needs a one-call prelaunch check for standalone specs.
- **Blocks:** The campaign launch; the PRELAUNCH records the R-B6 plans pin.
- **Close by:** `BEFORE_SEAL`. **Owner:** Claude2; builder any lane; distinct review. **Filled by the V007 adoption:** NO.
- **Evidence:** wrapper 24abe3bc L333-349; v005 c75a889f L3436-3444; setsid b978f402.
- **Recommended disposition (RECOMMENDATION):** Build a small reviewed entry (run --new-campaign, resolve retry, reingest, status, prelaunch-check that writes a pinned PRELAUNCH record per spec) that imports the r10 wrapper and runs under launch_setsid_c2v005.
- **Label:** FORMAL. **Source:** inventory R-B4 + dryplans campaign gates.

### R-B5: Post-state certificate loop per campaign call
- **What:** Each completed campaign call ingests INFRA CERTIFICATE_ACCEPTANCE_REFUSED until write_acceptance writes its handoff and the call is re-ingested.
- **Blocks:** Every campaign wave after a completed call.
- **Close by:** `BEFORE_CAMPAIGN`. **Owner:** Claude2 + Codex2 (producers). **Filled by the V007 adoption:** NO.
- **Evidence:** wrapper 24abe3bc L202-222, L265-276, L305-328; review r6 2d02874e (synthetic world, TESTED there).
- **Recommended disposition (RECOMMENDATION):** Write the operating procedure, assign an operator lane and automate the producer runs per completed call so a wave never waits on a manual step.
- **Label:** FORMAL. **Source:** inventory R-B5.

### R-B6: Step-4 direct-run launcher successor (V005 pattern)
- **What:** Launcher v007, guard v008 and the binder cannot be reused as bytes: 10 cases with C4T-KHI first (L72-83), the V007 seal admission with BUILD_V005's allowlist (guard L19-43), binder output only under the V007 packet (L18), route-A cap 6.
- **Blocks:** The DIII, headline, sensitivity and post-S1 launches (or they use the zero-build fallback).
- **Close by:** `BEFORE_HEADLINE`. **Owner:** Claude2; builder Codex1 (author of the V005 packet); Claude4 delta check. **Filled by the V007 adoption:** NO.
- **Evidence:** launcher 861bba68, guard 294cb776, binder f3e4e2be (FORMAL, read here); ramp signal TESTED for step-4 specs: route A is stage 01 at stages/01_route_a/attempt_000 in every dry plan; solvers 7667025b L348 and aed4dd59 L304 emit iteration_completed.
- **Recommended disposition (RECOMMENDATION):** Build a successor with the LAUNCH_ORDER ramp (route-A cap 3, memory >= 25% free, first-iteration ramp, 60 s poll, one start per poll, V005 halts, no retry), a STEP4 root admission record and a binder that binds C1; delta-check it like V005 (ramp scenarios, admission forgeries, output guards). Fallback until then: campaign_c2v005 CLI per batch (no ramp, no memory gate, no C5H output guard).
- **Label:** FORMAL / RECOMMENDATION. **Source:** launch_order (new item).

## C. Science and policy approvals

### R-C1: Per-point certificate admission and the registry (28 points)
- **What:** certificate_policy_review, approved_certificate_producers and a registry with prelaunch bundles; a reviewed LO producer successor (finish() always UNAVAILABLE); full EPS/rho tables; one GQ record per point. The pre-campaign points are 28: the 27 direct-run points plus the campaign seed 6944e210d071c17b502fd5188ea8967503dbf9bb1d5530b67d0b151da02b13cd.
- **Blocks:** Headline batch (the registry slots change the mapper bytes the capability evidence binds), sensitivity runs and the certificate_policy gate.
- **Close by:** `BEFORE_HEADLINE`. **Owner:** Claude2 science review; Codex2 producers; distinct reviewer. **Filled by the V007 adoption:** NO (keys depend on the block and driver).
- **Evidence:** config tail_readiness registry/policy null, producers [] (TESTED, inventory); review bc211c3a N1, N3; reconcile RC-02/RC-03: 28 distinct dry-plan keys, the seed not in the inventory list (TESTED); registry probe v002: registered slots change the spec bytes (TESTED).
- **Recommended disposition (RECOMMENDATION):** Commission the LO successor and the cap review now; produce the 28 bundles under r5 before T0 so certificates never gate H2; freeze the registry before the CAP runs and never change its probe-point entries afterwards.
- **Label:** TESTED / FORMAL. **Source:** inventory R-C1 + dryplans CERTIFICATE_POLICY_PENDING + reconcile RC-02/03.

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
- **What:** Each D needs its pair evidence, a distinct review, and root registration of the review sha and registry entry.
- **Blocks:** The 9 sensitivity runs at that D.
- **Close by:** `BEFORE_SENS`. **Owner:** Claude2 + a distinct-lane reviewer per D. **Filled by the V007 adoption:** NO.
- **Evidence:** sensitivity policy 8fb06600 L200-237; checker contract 47e23974.
- **Recommended disposition (RECOMMENDATION):** Assign a reviewer from a lane that did not produce the evidence; register the review sha in the R-B2 successor.
- **Label:** FORMAL. **Source:** inventory R-C5 + dryplans SENSITIVITY_DECIDING_III_REQUIRED.

### R-C6: Register the S1 transfer test (S4-POST-S1)
- **What:** ADOPT_TAIL prescribes "V005 S1 transfer test at the calibrated point before prediction" (K=3 and K=4 at the calibrated point). No spec, threshold or reading exists for the tail scheme.
- **Blocks:** Step 5 prediction. Wall about 5.4 h E / 9.0 h U for the 2 runs (UNTESTED).
- **Close by:** `BEFORE_CAMPAIGN`. **Owner:** Claude2. **Filled by the V007 adoption:** YES (the next-step text).
- **Evidence:** compare r11 a5d10cb1 L489-490; V005 prereg dbddc02c scope_untested S1.
- **Recommended disposition (RECOMMENDATION):** Register it target-free before the campaign result is read: cases, statistic, thresholds and reading.
- **Label:** TESTED (text). **Source:** inventory R-C6.

### R-C7: Purpose, reading and schedule of the 18 sensitivity runs
- **What:** Nothing in step 4 consumes them; A23 ties them to bounding the D effect on NGC misses.
- **Blocks:** Their launch (recommended), and the freeze if A23 reads them.
- **Close by:** `BEFORE_SENS`. **Owner:** Claude2. **Filled by the V007 adoption:** NO.
- **Evidence:** 0533 B4-1; review r6 F3; A23 (V004 addendum 487d4449).
- **Recommended disposition (RECOMMENDATION):** Register their reading before they run and schedule them after the campaign (default; 11.2 h E / 22.6 h U for all 18, UNTESTED), or defer them if no reading is registered.
- **Label:** FORMAL. **Source:** inventory R-C7.

### R-C8: Campaign points outside the pre-registered set (registry growth)
- **What:** With a registry pinned (the certificate_policy gate requires one), prelaunch_check refuses every point that is not already in it, and make_plan calls prelaunch_check for every call of a wave. Adding a point changes tail_readiness, hence the cache id, and C4-2 then refuses the work dir. The engine proposes most of its up to 120 points from earlier results, so they cannot be registered in advance.
- **Blocks:** The campaign after its pre-registered points. Only the seed and the Jacobian side points are fixed before any result (FORMAL reading of engine v003b: seed u, rel_step, box); every later point depends on earlier results.
- **Close by:** `BEFORE_CAMPAIGN`. **Owner:** Claude2 rules the design; Codex2 builds; Claude-lineage review. **Filled by the V007 adoption:** NO.
- **Evidence:** wrapper 24abe3bc L52-55 (cache id includes tail_readiness), L59-66, L86-90, L172-181; v005 c75a889f L3293-3309 (make_plan; prelaunch_check per call at L3309), L59-63 and L3094-3100 (C4-2); registry probe v002 (fenced, plan-only, synthetic look-alikes): unregistered TAIL_REANCHOR, seed and an adaptive point all refuse CERTIFICATE_POINT_MISSING_OR_MISMATCHED; registering the seed changes the cache id 4555ce79... -> b3839787... (TESTED).
- **Recommended disposition (RECOMMENDATION):** Rule the design before wave 1 and build it in R-B3. Preferred: an append-only, hash-chained registry ledger in the work dir whose genesis and policy (producers, guard, rules) are what the config and the cache id bind; each new point gets its prelaunch bundle from approved producers when its wave is planned, and the ledger entry is verified at plan, cache put and cache reuse. Alternative: a box-wide prelaunch envelope accepted by the science review (per-point acceptance kept).
- **Label:** TESTED (look-alike) / FORMAL (production). **Source:** launch_order (new item; neither list raised it).

## D. Run decisions, root-only launches and operations

### R-D1: TAIL_REANCHOR source
- **What:** Fresh template run, DU-1 (the mapper-built trial spec, physical bitwise equal to the anchor) or DU-3 (the V007 C4T run). 0557 N-1 says the reanchor launches "from the template's physical values, not a mapper-built theta".
- **Blocks:** The deciding_test row reanchor and config.anchor.
- **Close by:** `BEFORE_HEADLINE`. **Owner:** Claude2. **Filled by the V007 adoption:** PARTIAL (DU-3 uses the C4T run).
- **Evidence:** core a595c5c0 L149-157; 0557 16039954 N-1; reconcile RC-01 (one point key for RA, TRIAL and the anchor repeat, TESTED).
- **Recommended disposition (RECOMMENDATION):** Default to a fresh template run (literal N-1). Use DU-1 only on an explicit ruling. The extra run costs +0.26 h E / +1.74 h U on the headline batch (10 against 9 runs, UNTESTED).
- **Label:** FORMAL / TESTED. **Source:** inventory R-D1 + dryplans section 8 + reconcile OP1.

### R-D2: Designate the workers_8 row before launch
- **What:** Either one headline corner run (DU-2) or a repeat of the anchor with another label (the dry-plan candidate 686ad07f, which also serves PC-7).
- **Blocks:** The deciding_test document.
- **Close by:** `BEFORE_HEADLINE`. **Owner:** Claude2. **Filled by the V007 adoption:** NO.
- **Evidence:** core a595c5c0 L128-132, L189-191.
- **Recommended disposition (RECOMMENDATION):** Designate C000 (DU-2) in a root entry before launch; choose the anchor repeat only if root wants the PC-7 repeat now (adds one run).
- **Label:** FORMAL. **Source:** inventory R-D2 + dryplans WORKERS_8_SPEC_NOT_REGISTERED.

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

### R-D5: Deciding-(iii) pairs: caps and launch window
- **What:** Caps are unspecified; the runs need nothing from V007 and plan with 0 blockers.
- **Blocks:** DIII evidence, hence the sensitivity runs.
- **Close by:** `BEFORE_SEAL`. **Owner:** Claude2 (root-only launch). **Filled by the V007 adoption:** NO.
- **Evidence:** pair plan cb42a5a3; 0540 801d47fd F3 ("Root launches them during calibration prep"); A61 F3; dry plans: 0 blockers (TESTED there).
- **Recommended disposition (RECOMMENDATION):** Use the A52/A67 identity-run caps (43,200 s, 16 GiB, 32 GiB); modelled route-A RSS is 10.5 GiB, so 1.5x is 15.75 GiB and 24 GiB gives margin. Launch before the seal when load permits (4.6 h E / 7.8 h U for the batch, UNTESTED), never at normal QoS inside the step-2 ramp. State the tail-OFF exception in the V006 addendum, because 0610 item 4 asks the cross-lineage reviewer to confirm nothing launches before a sealed ADOPT.
- **Label:** FORMAL / UNTESTED (caps). **Source:** inventory R-D5 + launch_order.

### R-D6: Sensitivity launch conditions
- **What:** Launch the 18 sensitivity runs only after their D is registered (R-C5) and their reading is registered (R-C7).
- **Blocks:** The sensitivity batch.
- **Close by:** `BEFORE_SENS`. **Owner:** Claude2 (root-only launch). **Filled by the V007 adoption:** PARTIAL.
- **Evidence:** sensitivity policy 8fb06600 L205-237.
- **Recommended disposition (RECOMMENDATION):** As R-C7.
- **Label:** FORMAL. **Source:** inventory R-D6 + dryplans SENSITIVITY_DECIDING_III_REQUIRED.

### R-D7: Campaign scheduling
- **What:** Shipped: max_concurrent 1, process_budget 17 (hard maximum), stage-aware, 48 h per wave.
- **Blocks:** Campaign duration: 26.0 d E / 43.8 d U at max_concurrent 1 against 8.7 d / 14.9 d at 6 (UNTESTED).
- **Close by:** `BEFORE_CAMPAIGN`. **Owner:** Claude2. **Filled by the V007 adoption:** PARTIAL.
- **Evidence:** config 721c7230; v005 L171 PROCESS_BUDGET_MAX 17, L1724-1737; campaign d35d5d4a L186-230; work/SCHEDULE_SIM_C4V002.json.
- **Recommended disposition (RECOMMENDATION):** Set max_concurrent 6 (the nominal wave size) with budget 17 and stage-aware true; the 48 h wave cap then holds (max wave 10.4 h E / 17.5 h U). Option for root: a reviewed successor raising PROCESS_BUDGET_MAX to 24 (5.6 d E / 11.2 d U), which changes v005 and campaign_c2v005 pins.
- **Label:** FORMAL / UNTESTED. **Source:** inventory R-D7 + launch_order.

### R-D8: Caps for the direct runs
- **What:** The reanchor, workers_8, capability and sensitivity runs launch before the C4-6 caps exist.
- **Blocks:** Every direct tail-ON launch.
- **Close by:** `BEFORE_HEADLINE`. **Owner:** Claude2. **Filled by the V007 adoption:** PARTIAL.
- **Evidence:** V007 plan V010 26f1ebf9 C4T caps 19 h / 28 GiB / 96 GiB (proposals); projected per-call walls in U: headline batch up to 9.5 h (18 cores) / 12.3 h (12 cores); 18-run sensitivity batch up to 12.0 h / 17.6 h; modelled route-A RSS 13.7 GiB (work/SCHEDULE_SIM_C4V002.json).
- **Recommended disposition (RECOMMENDATION):** Use the V007 C4T plan caps (19 h, 28 GiB, 96 GiB) for the direct tail-ON runs, then the C4-6 caps for the campaign.
- **Label:** UNTESTED (fit). **Source:** inventory R-D8.

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
- **What:** A85.2-4 (QoS, sleep assertion) cover step 2 only; the campaign work dir is pinned on External1; the dry plans and this part used an uncreated local work dir with volume null.
- **Blocks:** All step-4 launches (operations).
- **Close by:** `BEFORE_HEADLINE`. **Owner:** Claude2. **Filled by the V007 adoption:** NO.
- **Evidence:** A85; A95 (taskpolicy preferred, not required, for lanes); config work_dir_identity VolumeUUID 7752BF6F-EFA9-418D-AD80-29078B663078.
- **Recommended disposition (RECOMMENDATION):** Apply normal QoS and caffeinate -i -w <launcher pid> to step-4 root runs, ask lanes to use taskpolicy -b where allowed, keep External1 mounted and verify the real work dir and VolumeUUID with a plan-mode run on C2 before wave 1; keep every output.
- **Label:** TESTED (config) / FORMAL. **Source:** inventory R-D11 + dryplans harness note.

### R-D12: Coordinate-spec preconditions still OPEN
- **What:** PC-1 (filled by the adoption), PC-5, PC-7 (FD noise floor by an anchor repeat), PC-9, D3, NGC slots, REVIEW.
- **Blocks:** The freeze (step 6) and possibly the campaign reading.
- **Close by:** `BEFORE_CAMPAIGN`. **Owner:** Claude2. **Filled by the V007 adoption:** PARTIAL (PC-1).
- **Evidence:** coordinates 50e7288e preconditions_before_freeze.
- **Recommended disposition (RECOMMENDATION):** State which apply to step 4 (PC-7 can ride on the workers_8 anchor-repeat option) and which wait for step 6.
- **Label:** TESTED (text). **Source:** inventory R-D12.

### R-D13: ORIGINAL_K marked for evaluation before freeze
- **What:** The freeze writer refuses unless its evaluation is supplied or NOT_EVALUATED_BEFORE_FREEZE is recorded.
- **Blocks:** The freeze.
- **Close by:** `AFTER_CAMPAIGN`. **Owner:** Claude2. **Filled by the V007 adoption:** NO.
- **Evidence:** coordinates 50e7288e discrete_alternatives.alternative_notes.ORIGINAL_K.
- **Recommended disposition (RECOMMENDATION):** Decide at the end of step 4 whether to evaluate it in step 5 or record NOT_EVALUATED_BEFORE_FREEZE.
- **Label:** TESTED (text) / UNTESTED (applicability). **Source:** inventory R-D13.

### R-D14: V006 addendum for the step-4 rulings
- **What:** A82: once the V005 file is frozen, every later root entry (steps 4-7) goes into a new V006 addendum.
- **Blocks:** Recording of every R-* ruling.
- **Close by:** `BEFORE_SEAL`. **Owner:** Claude2. **Filled by the V007 adoption:** NO.
- **Evidence:** A82 (open V005 addendum).
- **Recommended disposition (RECOMMENDATION):** Record step-4 rulings in V005 until it freezes at seal assembly, then in V006 (A82); include the DIII tail-OFF exception (R-D5) and the R-D1/R-D2 designations.
- **Label:** TESTED. **Source:** inventory R-D14.

### R-D15: One machine-wide schedule across launchers
- **What:** campaign_c2v005 and a direct-run launcher each account for their own processes only; run together they oversubscribe the 18 cores without either knowing.
- **Blocks:** Campaign and sensitivity timing.
- **Close by:** `BEFORE_CAMPAIGN`. **Owner:** Claude2. **Filled by the V007 adoption:** NO.
- **Evidence:** campaign d35d5d4a L186-230 (budget counts its own calls only); launcher 861bba68 available() counts its own cases only.
- **Recommended disposition (RECOMMENDATION):** Run one direct batch at a time and none while the campaign runs; if root wants overlap, lower the campaign process_budget explicitly for that period.
- **Label:** FORMAL / RECOMMENDATION. **Source:** launch_order (new item).

### R-D16: Where the per-D sensitivity registration lives
- **What:** The per-D entries live in config.tail_readiness.sensitivity_deciding_iii, and tail_readiness is in the cache id; a change during the campaign forces a new work dir (C4-2).
- **Blocks:** Campaign continuity if the DIII evidence lands after wave 1.
- **Close by:** `BEFORE_CAMPAIGN`. **Owner:** Claude2. **Filled by the V007 adoption:** NO.
- **Evidence:** wrapper 24abe3bc L52-55; registry probe v002 (a tail_readiness change changes the cache id, TESTED).
- **Recommended disposition (RECOMMENDATION):** Put the per-D entries into C2 only if they are final before the campaign starts; otherwise keep them in a sibling config used only for the standalone sensitivity prelaunch checks and never edit the campaign config mid-campaign.
- **Label:** TESTED / FORMAL. **Source:** launch_order (new item).

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
| dry plans (per spec) | CAPABILITY_EVIDENCE_PENDING | R-D3 |
| dry plans (per spec) | CERTIFICATE_POLICY_PENDING | R-C1 |
| dry plans (per spec) | COMPARATOR_A68_SUCCESSOR_REQUIRED | R-B2 |
| dry plans (per spec) | CONFIG_ANCHOR_TAIL_REANCHOR_PENDING | R-D4 |
| dry plans (per spec) | SENSITIVITY_DECIDING_III_REQUIRED | R-B2, R-C5, R-D5, R-D6 |
| dry plans (per spec) | WORKERS_8_SPEC_NOT_REGISTERED | R-D2 |
| dry plans (campaign gate) | numerics_verdict | R-A1 (V007 pins) |
| dry plans (campaign gate) | numerics_verdict / seal allowlist | R-A2, R-B3 |
| dry plans (campaign gate) | adoption_regeneration | R-A4, R-A5 |
| dry plans (campaign gate) | deciding_test | R-D1, R-D2, R-D4 |
| dry plans (campaign gate) | driver_capability | R-D3 |
| dry plans (campaign gate) | certificate_policy | R-C1 |
| dry plans (campaign gate) | u_i_carrier | R-C2 |
| dry plans (cross-lane) | V007_PREREG_BINDING_INPUTS_CASE_BLOCK_ABSENT | R-A3 |
| dry plans (cross-lane) | ORCHESTRATOR_V006R9_R5_ONLY_UNDER_AN_R6_SEAL | R-B1 (moot after A96) |
| dry plans (problems) | R6 BUILD not landed | R-B1 |
| dry plans (problems) | spec bytes change after adoption / registry | R-A1, R-A4, R-C1 |
| dry plans (problems) | production work dir untested (uncreated local dir) | R-D11 |
| dry plans (problems) | ADOPT_TAIL None uncertainty rows (S7) | R-A6 |

Unmapped dry-plan codes: none. Inventory items not carried: none. Fence blocks in this generator: none.
