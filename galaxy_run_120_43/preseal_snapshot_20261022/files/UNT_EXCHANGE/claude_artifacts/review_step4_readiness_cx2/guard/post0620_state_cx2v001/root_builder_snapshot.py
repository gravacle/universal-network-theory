# Claude4 helper, dispatch 0587 part (4)/(e): the final merged root-item list for step 4.
# One data table -> work/ROOT_ITEMS_FINAL_C4V001.json and ROOT_ITEMS_FINAL_C4V001.md (exclusive create).
# Merges inventory/ROOT_ITEMS_C4V001.json (31 items) with every non-V007 blocker of dryplans/DRYPLANS_C4V002.json and the
# items found in this part. Every disposition is a RECOMMENDATION; root (Claude2) decides.
# Usage: python3 -I -B build_root_items_final_c4v001.py <out json> <out md>
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fence_c4v001 as F
import hashlib, json, datetime

LO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S4 = os.path.dirname(LO)
INV_RI = S4 + '/inventory/ROOT_ITEMS_C4V001.json'
DP = S4 + '/dryplans/DRYPLANS_C4V002.json'
SIM = LO + '/work/SCHEDULE_SIM_C4V002.json'
PRB = LO + '/work/registry_probe_v002/REGISTRY_GROWTH_PROBE_C4V002.json'
REC = LO + '/work/RECONCILE_C4V002.json'


def sha_file(p):
    with open(p, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


def load(p):
    with open(p, 'rb') as f:
        return json.loads(f.read())


# close_by phases (see LAUNCH_ORDER_C4V001.md section 3)
P_SEAL = 'BEFORE_SEAL'            # phase P: before the V007 seal (no V007 dependency)
P_T0 = 'AT_T0'                    # H1: right after the sealed ADOPT_TAIL, before the headline batch
P_H = 'BEFORE_HEADLINE'           # must exist before the headline batch launches (can close pre-seal)
P_H3 = 'AFTER_HEADLINE'           # H3: from the headline receipts, before the campaign
P_C = 'BEFORE_CAMPAIGN'
P_S = 'BEFORE_SENS'
P_Z = 'AFTER_CAMPAIGN'
P_DONE = 'CLOSED_BY_RULING'

ITEMS = [
    # ------------------------------------------------------------------ A
    dict(id='R-A1', group='A', title='Config successor C1 from the sealed ADOPT_TAIL', close_by=P_T0, owner='Claude2', v007='YES', src='inventory R-A1 + dryplans post_adoption_probe',
         what='Write numerics.{verdict_artifact, block_source, compare, sealed_prereg, adopted_result, source_results} and numerics.block := the sealed C4T call-spec numerics exactly (its eps/lo slots included).',
         blocks='Every tail-ON run (launch bytes are regenerated under C1) and the numerics_verdict gate.',
         evidence=['adoption policy 7c726fa2 L90-91 (block == C4T numerics); config 721c7230 fields null (TESTED, inventory)',
                   'dry plans post_adoption_probe: 30/30 specs normalize with 0 pending after the fill (TESTED there); provisional bytes TAIL_REANCHOR 924851c4, HEADLINE_TRIAL 7d9a8d47, seed 854e1291',
                   'registry probe v002 here reproduced the seed sha 854e129191b6b024d47b200a70df1d96098d27ef7628c6a727554929141e4bd9 with the A70 slot records (TESTED)'],
         rec='Prepare C1 now as a template differing from r9 only in these fields, the block and the R-C1/R-C2/R-D8 fields. At T0 fill it, check it by key diff, regenerate the launch bytes plan-only, and require that any point whose registry slots are the A70 records reproduces its dry-plan PROVISIONAL sha.', label='FORMAL / TESTED'),
    dict(id='R-A2', group='A', title='Seal tuple into APPROVED_V007_SEALS', close_by=P_T0, owner='Claude2 + distinct reviewer; builder Codex2', v007='YES', src='inventory R-A2 + dryplans campaign gate (seal allowlist)',
         what='The shipped allowlist is an empty frozenset; the tuple (compare sha, prereg sha, frozen addendum sha, report schema, verdict sha) enters only through an immutable policy successor, which forces core and wrapper successors.',
         blocks='numerics_verdict gate, hence the campaign. Not the direct runs.',
         evidence=['adoption policy 7c726fa2 L9-12; core a595c5c0 L200-203; wrapper 24abe3bc L27', 'dry plans adoption_world S1 refuses only on V007_SEAL_NOT_IN_REVIEWED_ALLOWLIST; S2 passes with the tuple in memory (TESTED there)'],
         rec='Build it inside the R-B3 cascade now with a one-line placeholder; at T0 insert the tuple and verify by line diff (the RI-27 pattern), so no full review sits after the seal.', label='TESTED / FORMAL'),
    dict(id='R-A3', group='A', title='Case-block binding in the sealed prereg (seal-blocking)', close_by=P_SEAL, owner='Claude2 at seal assembly; prereg author Claude4; compare owner Codex3', v007='MUST BE IN THE SEALED PREREG', src='inventory R-A3 + dryplans DEFECT (found independently by both)',
         what='Prereg r4 binding_inputs has no case_block. The sealed compare takes the case block only from there; the adoption policy reads the same binding.',
         blocks='The sealed V007 verdict itself, hence all of step 4.',
         evidence=['prereg r4 e3b6b5b2 key walk: no case_block (TESTED, inventory work/CASE_BLOCK_CHECK_C4V001.json)',
                   'compare r11 a5d10cb1 L5689-5697; frozen compare r12 4bd7b262 L5705-5714: sealed mode refuses CASE_BLOCK_ABSENT (FORMAL, read from bytes here at 2026-10-18T20:01:37Z)',
                   'adoption policy 7c726fa2 L74-77; dry plans adoption_world S3 V007_CASE_BLOCK_NOT_BOUND_BY_SEALED_PREREG (TESTED there)'],
         rec='Treat as blocking for the seal. Bind a registered, target-free case block through a prereg successor or an RI-26 seal note, and run r12 in sealed mode on it in the 0602 seal rehearsal.', label='TESTED (absence) / FORMAL (requirement)'),
    dict(id='R-A4', group='A', title='C4-6 adoption derivation', close_by=P_H3, owner='Claude2 + distinct reviewer', v007='PARTIAL', src='inventory R-A4 + dryplans campaign gate adoption_regeneration',
         what='Schema DDO154_CALIBRATION_ADOPTION_DERIVATION_C2V005 plus the wrapper tail bindings: verdict, adopted C4T case and spec, base and seed spec shas, capability evidence, timing model, monitor-verified receipts, caps above measured use, disk guard, registry.',
         blocks='adoption_regeneration gate, hence the campaign.',
         evidence=['v005 c75a889f L1828-1926; wrapper 24abe3bc L183-197 (needs driver_capability ok)', 'dry plans: base and seed shas must come from the post-adoption config (spec bytes change after adoption, TESTED there)'],
         rec='Write and review a target-free generator now; run it after the headline batch on C1 bytes; pin its output in C2.', label='FORMAL'),
    dict(id='R-A5', group='A', title='Caps regenerated from the measured C4T use', close_by=P_H3, owner='Claude2', v007='PARTIAL', src='inventory R-A5 + launch_order (TIMING_V003 under-count)',
         what='Config per-call caps are 8 h wall, 64 GiB RSS, 12 GiB output; C4-6 refuses caps that are not above the measured use.',
         blocks='adoption_regeneration; campaign calls that run past the wall cap would stop.',
         evidence=['config 721c7230 per_call / disk_guard (TESTED, inventory)',
                   'TIMING_V003 3e3fb600 keeps the I=7 route-A baseline in its I=32 total; scaled, the upper call is 8.74-8.77 h solo, above the 8 h cap (TESTED arithmetic, work/SCHEDULE_SIM_C4V002.json)',
                   'load ratios 1.69-2.99 (TIMING_V003 calibration rows)'],
         rec='Wall cap at least 2x the C4T measured elapsed and at least the upper projection times the measured load ratio; RSS at least 1.5x the C4T peak; output cap at least 1.5x the C4T output; disk_guard.per_call_bytes at least the output cap.', label='TESTED (values, arithmetic) / UNTESTED (fit)'),
    dict(id='R-A6', group='A', title='Finite carried uncertainty in the ADOPT_TAIL report', close_by=P_SEAL, owner='Codex3 (compare) + Claude2', v007='YES (the verdict carries it)', src='dryplans adoption_world S7 (new item)',
         what='The adoption refuses V007_CARRIED_UNCERTAINTY_REQUIRED if a carried_numerical_uncertainty_km_s row is None; compare r11 L4781 allows None rows.',
         blocks='numerics_verdict on an otherwise valid ADOPT_TAIL.',
         evidence=['dry plans adoption_world S7 (TESTED on look-alikes there)', 'compare r11 a5d10cb1 L4781 (FORMAL, cited by the dry plans)'],
         rec='Confirm in the seal rehearsal that an ADOPT_TAIL report always carries finite rows, or rule how a None row is read and put that rule in the R-B3 policy successor.', label='TESTED (look-alike) / UNTESTED (real report)'),
    # ------------------------------------------------------------------ B
    dict(id='R-B1', group='B', title='Driver of record: r5 (settled for V007 by A96)', close_by=P_DONE, owner='Claude2', v007='YES (driver slot)', src='inventory R-B1 + dryplans R6 DEFERRED + A96',
         what='A96 (19:51Z): V007 seals on v010 r5 b5cc62af; the r6 build was stopped and its bytes are unfinished and unused; caching for steps 4-5 is decided later with the A85.1 result.',
         blocks='Nothing now. v006r9 requires r5, so step 4 runs on r5.',
         evidence=['A96 in the open V005 addendum 991cc242 (snapshot 1952Z)', 'core a595c5c0 L25; wrapper 24abe3bc L47-48', 'driver_r6/ listing 19:37Z: no BUILD.md, no manifest (TESTED)'],
         rec='Run every step-4 call on r5. A cache or parallel-tail driver for steps 4-5 later needs its own identity gates, an orchestrator retarget successor, re-keyed registry points (the driver sha is in every point key) and a deciding-(iii) new side or a B0 transfer ruling. r6 dry plans stay DEFERRED (tooling ready in ../dryplans/tools).', label='TESTED / FORMAL'),
    dict(id='R-B2', group='B', title='Deciding-(iii) comparator successor on c2v007r2', close_by=P_SEAL, owner='Codex2 (sensitivity policy); Codex1 (c2v007r2 unchanged per 0611); cross-lineage reviewer', v007='NO', src='inventory R-B2 + dryplans COMPARATOR_A68_SUCCESSOR_REQUIRED + A92/0611',
         what='The pair plan and sensitivity policy pin the c2v004-derived comparator (FAIL, A68); compute_pair refuses while COMPARATOR_A68_REVIEWED is False and REGISTERED_DISTINCT_REVIEW_SHA256 is empty. Since A92, c2v007r2 (052da0fe) is the identity-comparator slot of record.',
         blocks='DIII evidence, hence the 18 sensitivity runs. Not the DIII launches.',
         evidence=['sensitivity policy 8fb06600 L19-40, L185-203; pair plan cb42a5a3', 'A92; 0611 (comparator source must not change); c2v007r2 052da0fe, BUILD_R2 d02e4637 (TESTED hashes)'],
         rec='One policy successor that re-pins the pair plan and policy to c2v007r2 through an r5 custody adapter outside the comparator (as the c2v004-r5 adapter did), with a validate_report for its schema; COMPARATOR_A68_REVIEWED set only after that adapter is reviewed. Confirm that the two-driver comparison (v009-GEO vs v010 r5) is in c2v007r2\'s supported scope.', label='TESTED (pins) / FORMAL'),
    dict(id='R-B3', group='B', title='One v006r10 cascade with a single delta review', close_by=P_SEAL, owner='Claude2; builder Codex2; distinct reviewer', v007='PARTIAL (tuple line)', src='inventory R-B3 + launch_order',
         what='Policy, core and wrapper successors carrying R-A2 (placeholder), R-B2, R-C8, R-B4 and R-A6 if needed. Every config change is a new cache id (C4-2).',
         blocks='The campaign gates.',
         evidence=['wrapper 24abe3bc L27-30 byte pins; v005 c75a889f C4-2 L59-63'],
         rec='Build it now, leaving only the tuple line for after the seal. Add a regression test: under the same config, r10 Mapper.build must give byte-identical specs to r9 for the 9 probe points and the seed (otherwise capability evidence and cached keys would not match).', label='FORMAL'),
    dict(id='R-B4', group='B', title='Launch entries', close_by=P_SEAL, owner='Claude2; builder any lane; distinct review', v007='NO', src='inventory R-B4 + dryplans campaign gates',
         what='v006r9 exposes plan and wave only; Orchestrator.run needs a session leader (launch_setsid_c2v005). Root also needs a one-call prelaunch check for standalone specs.',
         blocks='The campaign launch; the PRELAUNCH records the R-B6 plans pin.',
         evidence=['wrapper 24abe3bc L333-349; v005 c75a889f L3436-3444; setsid b978f402'],
         rec='Build a small reviewed entry (run --new-campaign, resolve retry, reingest, status, prelaunch-check that writes a pinned PRELAUNCH record per spec) that imports the r10 wrapper and runs under launch_setsid_c2v005.', label='FORMAL'),
    dict(id='R-B5', group='B', title='Post-state certificate loop per campaign call', close_by=P_C, owner='Claude2 + Codex2 (producers)', v007='NO', src='inventory R-B5',
         what='Each completed campaign call ingests INFRA CERTIFICATE_ACCEPTANCE_REFUSED until write_acceptance writes its handoff and the call is re-ingested.',
         blocks='Every campaign wave after a completed call.',
         evidence=['wrapper 24abe3bc L202-222, L265-276, L305-328; review r6 2d02874e (synthetic world, TESTED there)'],
         rec='Write the operating procedure, assign an operator lane and automate the producer runs per completed call so a wave never waits on a manual step.', label='FORMAL'),
    dict(id='R-B6', group='B', title='Step-4 direct-run launcher successor (V005 pattern)', close_by=P_H, owner='Claude2; builder Codex1 (author of the V005 packet); Claude4 delta check', v007='NO', src='launch_order (new item)',
         what='Launcher v007, guard v008 and the binder cannot be reused as bytes: 10 cases with C4T-KHI first (L72-83), the V007 seal admission with BUILD_V005\'s allowlist (guard L19-43), binder output only under the V007 packet (L18), route-A cap 6.',
         blocks='The DIII, headline, sensitivity and post-S1 launches (or they use the zero-build fallback).',
         evidence=['launcher 861bba68, guard 294cb776, binder f3e4e2be (FORMAL, read here)', 'ramp signal TESTED for step-4 specs: route A is stage 01 at stages/01_route_a/attempt_000 in every dry plan; solvers 7667025b L348 and aed4dd59 L304 emit iteration_completed'],
         rec='Build a successor with the LAUNCH_ORDER ramp (route-A cap 3, memory >= 25% free, first-iteration ramp, 60 s poll, one start per poll, V005 halts, no retry), a STEP4 root admission record and a binder that binds C1; delta-check it like V005 (ramp scenarios, admission forgeries, output guards). Fallback until then: campaign_c2v005 CLI per batch (no ramp, no memory gate, no C5H output guard).', label='FORMAL / RECOMMENDATION'),
    # ------------------------------------------------------------------ C
    dict(id='R-C1', group='C', title='Per-point certificate admission and the registry (28 points)', close_by=P_H, owner='Claude2 science review; Codex2 producers; distinct reviewer', v007='NO (keys depend on the block and driver)', src='inventory R-C1 + dryplans CERTIFICATE_POLICY_PENDING + reconcile RC-02/03',
         what='certificate_policy_review, approved_certificate_producers and a registry with prelaunch bundles; a reviewed LO producer successor (finish() always UNAVAILABLE); full EPS/rho tables; one GQ record per point. The pre-campaign points are 28: the 27 direct-run points plus the campaign seed 6944e210d071c17b502fd5188ea8967503dbf9bb1d5530b67d0b151da02b13cd.',
         blocks='Headline batch (the registry slots change the mapper bytes the capability evidence binds), sensitivity runs and the certificate_policy gate.',
         evidence=['config tail_readiness registry/policy null, producers [] (TESTED, inventory)', 'review bc211c3a N1, N3', 'reconcile RC-02/RC-03: 28 distinct dry-plan keys, the seed not in the inventory list (TESTED)', 'registry probe v002: registered slots change the spec bytes (TESTED)'],
         rec='Commission the LO successor and the cap review now; produce the 28 bundles under r5 before T0 so certificates never gate H2; freeze the registry before the CAP runs and never change its probe-point entries afterwards.', label='TESTED / FORMAL'),
    dict(id='R-C2', group='C', title='u_i carrier declaration', close_by=P_H3, owner='Claude2', v007='PARTIAL', src='inventory R-C2 + dryplans campaign gate u_i_carrier',
         what='The gate fails until root sets declared_by and basis; ADMISSION_RECTANGLES is not implemented; dropped from the r9 TYPED_BLOCKERS list.',
         blocks='u_i_carrier gate, hence the campaign.', evidence=['config u_i_carrier (TESTED, inventory); v005 c75a889f L1797-1826'],
         rec='FROZEN_BANDS_ONLY declared by Claude2 with the sealed verdict as basis, if the freeze successor carries it (UNTESTED); otherwise NOT_CARRIED_DECLARED with disclosure.', label='TESTED / UNTESTED'),
    dict(id='R-C3', group='C', title='Taxonomy approval and root judgment calls', close_by=P_C, owner='Claude2 + distinct reviewer', v007='NO', src='inventory R-C3',
         what='The tail-ON failure taxonomy is a candidate with judgment calls R10, R11, R13, R20/R21/R32, R22, R30; no route-A contraction test declared.',
         blocks='Halt classification in every campaign wave.', evidence=['taxonomy 0ad99c66; config route_a_contraction_test null (TESTED, inventory)'],
         rec='Commission the classification review now and rule the judgment calls before wave 1; keep the contraction test null unless a reviewed rule exists.', label='TESTED'),
    dict(id='R-C4', group='C', title='MODEL_INVALID for tail-ON', close_by=P_C, owner='Claude2 (later certified successor)', v007='NO', src='inventory R-C4 + r9 TYPED_BLOCKERS',
         what='resolve --decision invalid is disabled; a physically invalid theta halts the campaign with no cache record and a retry repeats it.',
         blocks='Campaign progress past an invalid point.', evidence=['wrapper 24abe3bc L95-118, L296-301'],
         rec='Decide before wave 1: accept halts if the headline probes all complete validly; otherwise commission a certified MODEL_INVALID rule, stricter where silent.', label='FORMAL'),
    dict(id='R-C5', group='C', title='Distinct review per D of the deciding-(iii) evidence', close_by=P_S, owner='Claude2 + a distinct-lane reviewer per D', v007='NO', src='inventory R-C5 + dryplans SENSITIVITY_DECIDING_III_REQUIRED',
         what='Each D needs its pair evidence, a distinct review, and root registration of the review sha and registry entry.',
         blocks='The 9 sensitivity runs at that D.', evidence=['sensitivity policy 8fb06600 L200-237; checker contract 47e23974'],
         rec='Assign a reviewer from a lane that did not produce the evidence; register the review sha in the R-B2 successor.', label='FORMAL'),
    dict(id='R-C6', group='C', title='Register the S1 transfer test (S4-POST-S1)', close_by=P_C, owner='Claude2', v007='YES (the next-step text)', src='inventory R-C6',
         what='ADOPT_TAIL prescribes "V005 S1 transfer test at the calibrated point before prediction" (K=3 and K=4 at the calibrated point). No spec, threshold or reading exists for the tail scheme.',
         blocks='Step 5 prediction. Wall about 5.4 h E / 9.0 h U for the 2 runs (UNTESTED).', evidence=['compare r11 a5d10cb1 L489-490; V005 prereg dbddc02c scope_untested S1'],
         rec='Register it target-free before the campaign result is read: cases, statistic, thresholds and reading.', label='TESTED (text)'),
    dict(id='R-C7', group='C', title='Purpose, reading and schedule of the 18 sensitivity runs', close_by=P_S, owner='Claude2', v007='NO', src='inventory R-C7',
         what='Nothing in step 4 consumes them; A23 ties them to bounding the D effect on NGC misses.',
         blocks='Their launch (recommended), and the freeze if A23 reads them.', evidence=['0533 B4-1; review r6 F3; A23 (V004 addendum 487d4449)'],
         rec='Register their reading before they run and schedule them after the campaign (default; 11.2 h E / 22.6 h U for all 18, UNTESTED), or defer them if no reading is registered.', label='FORMAL'),
    dict(id='R-C8', group='C', title='Campaign points outside the pre-registered set (registry growth)', close_by=P_C, owner='Claude2 rules the design; Codex2 builds; Claude-lineage review', v007='NO', src='launch_order (new item; neither list raised it)',
         what='With a registry pinned (the certificate_policy gate requires one), prelaunch_check refuses every point that is not already in it, and make_plan calls prelaunch_check for every call of a wave. Adding a point changes tail_readiness, hence the cache id, and C4-2 then refuses the work dir. The engine proposes most of its up to 120 points from earlier results, so they cannot be registered in advance.',
         blocks='The campaign after its pre-registered points. Only the seed and the Jacobian side points are fixed before any result (FORMAL reading of engine v003b: seed u, rel_step, box); every later point depends on earlier results.',
         evidence=['wrapper 24abe3bc L52-55 (cache id includes tail_readiness), L59-66, L86-90, L172-181; v005 c75a889f L3293-3309 (make_plan; prelaunch_check per call at L3309), L59-63 and L3094-3100 (C4-2)',
                   'registry probe v002 (fenced, plan-only, synthetic look-alikes): unregistered TAIL_REANCHOR, seed and an adaptive point all refuse CERTIFICATE_POINT_MISSING_OR_MISMATCHED; registering the seed changes the cache id 4555ce79... -> b3839787... (TESTED)'],
         rec='Rule the design before wave 1 and build it in R-B3. Preferred: an append-only, hash-chained registry ledger in the work dir whose genesis and policy (producers, guard, rules) are what the config and the cache id bind; each new point gets its prelaunch bundle from approved producers when its wave is planned, and the ledger entry is verified at plan, cache put and cache reuse. Alternative: a box-wide prelaunch envelope accepted by the science review (per-point acceptance kept).', label='TESTED (look-alike) / FORMAL (production)'),
    # ------------------------------------------------------------------ D
    dict(id='R-D1', group='D', title='TAIL_REANCHOR source', close_by=P_H, owner='Claude2', v007='PARTIAL (DU-3 uses the C4T run)', src='inventory R-D1 + dryplans section 8 + reconcile OP1',
         what='Fresh template run, DU-1 (the mapper-built trial spec, physical bitwise equal to the anchor) or DU-3 (the V007 C4T run). 0557 N-1 says the reanchor launches "from the template\'s physical values, not a mapper-built theta".',
         blocks='The deciding_test row reanchor and config.anchor.', evidence=['core a595c5c0 L149-157; 0557 16039954 N-1; reconcile RC-01 (one point key for RA, TRIAL and the anchor repeat, TESTED)'],
         rec='Default to a fresh template run (literal N-1). Use DU-1 only on an explicit ruling. The extra run costs +0.26 h E / +1.74 h U on the headline batch (10 against 9 runs, UNTESTED).', label='FORMAL / TESTED'),
    dict(id='R-D2', group='D', title='Designate the workers_8 row before launch', close_by=P_H, owner='Claude2', v007='NO', src='inventory R-D2 + dryplans WORKERS_8_SPEC_NOT_REGISTERED',
         what='Either one headline corner run (DU-2) or a repeat of the anchor with another label (the dry-plan candidate 686ad07f, which also serves PC-7).',
         blocks='The deciding_test document.', evidence=['core a595c5c0 L128-132, L189-191'],
         rec='Designate C000 (DU-2) in a root entry before launch; choose the anchor repeat only if root wants the PC-7 repeat now (adds one run).', label='FORMAL'),
    dict(id='R-D3', group='D', title='Headline capability runs and the capability evidence', close_by=P_H3, owner='Claude2 (root-only launch)', v007='PARTIAL', src='inventory R-D3 + dryplans CAPABILITY_EVIDENCE_PENDING',
         what='Nine runs (trial + 2^3 corners at D 4.04); the evidence document binds their mapper-built spec shas under the final config.',
         blocks='driver_capability and adoption_regeneration.', evidence=['core a595c5c0 L313-340; wrapper L194-195'],
         rec='Launch them in the headline batch right after C1 with the registry frozen; write the evidence only from monitor-verified receipts.', label='FORMAL'),
    dict(id='R-D4', group='D', title='deciding_test document and config.anchor', close_by=P_H3, owner='Claude2', v007='NO', src='inventory R-D4 + dryplans CONFIG_ANCHOR_TAIL_REANCHOR_PENDING',
         what='Two rows {reanchor, workers_8}; config.anchor {result, receipt, spec_sha256} from S4-RA.',
         blocks='deciding_test and numerics_verdict (check_numerics takes the verified workers count from check_deciding).', evidence=['core a595c5c0 L114-197; v005 c75a889f L1943-1947; dry plans adoption_world S5'],
         rec='Generate both from the receipts by script and self-check with check_deciding on a copy of the config before pinning.', label='FORMAL / TESTED'),
    dict(id='R-D5', group='D', title='Deciding-(iii) pairs: caps and launch window', close_by=P_SEAL, owner='Claude2 (root-only launch)', v007='NO', src='inventory R-D5 + launch_order',
         what='Caps are unspecified; the runs need nothing from V007 and plan with 0 blockers.',
         blocks='DIII evidence, hence the sensitivity runs.', evidence=['pair plan cb42a5a3; 0540 801d47fd F3 ("Root launches them during calibration prep"); A61 F3', 'dry plans: 0 blockers (TESTED there)'],
         rec='Use the A52/A67 identity-run caps (43,200 s, 16 GiB, 32 GiB); modelled route-A RSS is 10.5 GiB, so 1.5x is 15.75 GiB and 24 GiB gives margin. Launch before the seal when load permits (4.6 h E / 7.8 h U for the batch, UNTESTED), never at normal QoS inside the step-2 ramp. State the tail-OFF exception in the V006 addendum, because 0610 item 4 asks the cross-lineage reviewer to confirm nothing launches before a sealed ADOPT.', label='FORMAL / UNTESTED (caps)'),
    dict(id='R-D6', group='D', title='Sensitivity launch conditions', close_by=P_S, owner='Claude2 (root-only launch)', v007='PARTIAL', src='inventory R-D6 + dryplans SENSITIVITY_DECIDING_III_REQUIRED',
         what='Launch the 18 sensitivity runs only after their D is registered (R-C5) and their reading is registered (R-C7).',
         blocks='The sensitivity batch.', evidence=['sensitivity policy 8fb06600 L205-237'], rec='As R-C7.', label='FORMAL'),
    dict(id='R-D7', group='D', title='Campaign scheduling', close_by=P_C, owner='Claude2', v007='PARTIAL', src='inventory R-D7 + launch_order',
         what='Shipped: max_concurrent 1, process_budget 17 (hard maximum), stage-aware, 48 h per wave.',
         blocks='Campaign duration: 26.0 d E / 43.8 d U at max_concurrent 1 against 8.7 d / 14.9 d at 6 (UNTESTED).', evidence=['config 721c7230; v005 L171 PROCESS_BUDGET_MAX 17, L1724-1737; campaign d35d5d4a L186-230; work/SCHEDULE_SIM_C4V002.json'],
         rec='Set max_concurrent 6 (the nominal wave size) with budget 17 and stage-aware true; the 48 h wave cap then holds (max wave 10.4 h E / 17.5 h U). Option for root: a reviewed successor raising PROCESS_BUDGET_MAX to 24 (5.6 d E / 11.2 d U), which changes v005 and campaign_c2v005 pins.', label='FORMAL / UNTESTED'),
    dict(id='R-D8', group='D', title='Caps for the direct runs', close_by=P_H, owner='Claude2', v007='PARTIAL', src='inventory R-D8',
         what='The reanchor, workers_8, capability and sensitivity runs launch before the C4-6 caps exist.',
         blocks='Every direct tail-ON launch.', evidence=['V007 plan V010 26f1ebf9 C4T caps 19 h / 28 GiB / 96 GiB (proposals)', 'projected per-call walls in U: headline batch up to 9.5 h (18 cores) / 12.3 h (12 cores); 18-run sensitivity batch up to 12.0 h / 17.6 h; modelled route-A RSS 13.7 GiB (work/SCHEDULE_SIM_C4V002.json)'],
         rec='Use the V007 C4T plan caps (19 h, 28 GiB, 96 GiB) for the direct tail-ON runs, then the C4-6 caps for the campaign.', label='UNTESTED (fit)'),
    dict(id='R-D9', group='D', title='Hull-miss contingency', close_by=P_H, owner='Claude2', v007='NO', src='inventory R-D9',
         what='No bracket recovery in v006 and the block must equal the C4T numerics, so a miss under the full hull is a hard stop.',
         blocks='A corner or campaign point that misses.', evidence=['core a595c5c0 L240-243; review r5 8016cad0 (hull top margin about 2.5%, column 71 rfs 0.72%)'],
         rec='Register the response now: record the miss, stop new launches of that theta, rule on a registration; never widen ad hoc.', label='FORMAL'),
    dict(id='R-D10', group='D', title='Engine seed computed afresh', close_by=P_C, owner='Claude2', v007='NO', src='inventory R-D10 + reconcile RC-02',
         what='The anchor alias is disabled, so wave 1 is a fresh seed call about 1e-15 off the anchor (its own point key 6944e210...).',
         blocks='Wave 1 (needs its registry entry, R-C1).', evidence=['core a595c5c0 L101-102; v005 L1785-1788; dry plans orchestrator plan (TESTED there)'],
         rec='Accept the one extra call; register its point with the other 27.', label='FORMAL / TESTED'),
    dict(id='R-D11', group='D', title='Operational settings for step 4', close_by=P_H, owner='Claude2', v007='NO', src='inventory R-D11 + dryplans harness note',
         what='A85.2-4 (QoS, sleep assertion) cover step 2 only; the campaign work dir is pinned on External1; the dry plans and this part used an uncreated local work dir with volume null.',
         blocks='All step-4 launches (operations).', evidence=['A85; A95 (taskpolicy preferred, not required, for lanes); config work_dir_identity VolumeUUID 7752BF6F-EFA9-418D-AD80-29078B663078'],
         rec='Apply normal QoS and caffeinate -i -w <launcher pid> to step-4 root runs, ask lanes to use taskpolicy -b where allowed, keep External1 mounted and verify the real work dir and VolumeUUID with a plan-mode run on C2 before wave 1; keep every output.', label='TESTED (config) / FORMAL'),
    dict(id='R-D12', group='D', title='Coordinate-spec preconditions still OPEN', close_by=P_C, owner='Claude2', v007='PARTIAL (PC-1)', src='inventory R-D12',
         what='PC-1 (filled by the adoption), PC-5, PC-7 (FD noise floor by an anchor repeat), PC-9, D3, NGC slots, REVIEW.',
         blocks='The freeze (step 6) and possibly the campaign reading.', evidence=['coordinates 50e7288e preconditions_before_freeze'],
         rec='State which apply to step 4 (PC-7 can ride on the workers_8 anchor-repeat option) and which wait for step 6.', label='TESTED (text)'),
    dict(id='R-D13', group='D', title='ORIGINAL_K marked for evaluation before freeze', close_by=P_Z, owner='Claude2', v007='NO', src='inventory R-D13',
         what='The freeze writer refuses unless its evaluation is supplied or NOT_EVALUATED_BEFORE_FREEZE is recorded.',
         blocks='The freeze.', evidence=['coordinates 50e7288e discrete_alternatives.alternative_notes.ORIGINAL_K'],
         rec='Decide at the end of step 4 whether to evaluate it in step 5 or record NOT_EVALUATED_BEFORE_FREEZE.', label='TESTED (text) / UNTESTED (applicability)'),
    dict(id='R-D14', group='D', title='V006 addendum for the step-4 rulings', close_by=P_SEAL, owner='Claude2', v007='NO', src='inventory R-D14',
         what='A82: once the V005 file is frozen, every later root entry (steps 4-7) goes into a new V006 addendum.',
         blocks='Recording of every R-* ruling.', evidence=['A82 (open V005 addendum)'], rec='Record step-4 rulings in V005 until it freezes at seal assembly, then in V006 (A82); include the DIII tail-OFF exception (R-D5) and the R-D1/R-D2 designations.', label='TESTED'),
    dict(id='R-D15', group='D', title='One machine-wide schedule across launchers', close_by=P_C, owner='Claude2', v007='NO', src='launch_order (new item)',
         what='campaign_c2v005 and a direct-run launcher each account for their own processes only; run together they oversubscribe the 18 cores without either knowing.',
         blocks='Campaign and sensitivity timing.', evidence=['campaign d35d5d4a L186-230 (budget counts its own calls only); launcher 861bba68 available() counts its own cases only'],
         rec='Run one direct batch at a time and none while the campaign runs; if root wants overlap, lower the campaign process_budget explicitly for that period.', label='FORMAL / RECOMMENDATION'),
    dict(id='R-D16', group='D', title='Where the per-D sensitivity registration lives', close_by=P_C, owner='Claude2', v007='NO', src='launch_order (new item)',
         what='The per-D entries live in config.tail_readiness.sensitivity_deciding_iii, and tail_readiness is in the cache id; a change during the campaign forces a new work dir (C4-2).',
         blocks='Campaign continuity if the DIII evidence lands after wave 1.', evidence=['wrapper 24abe3bc L52-55; registry probe v002 (a tail_readiness change changes the cache id, TESTED)'],
         rec='Put the per-D entries into C2 only if they are final before the campaign starts; otherwise keep them in a sibling config used only for the standalone sensitivity prelaunch checks and never edit the campaign config mid-campaign.', label='TESTED / FORMAL'),
]


def main(out_json, out_md):
    utc = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    inv = load(INV_RI)
    dp = load(DP)
    inv_ids = [x['id'] for x in inv['items']]
    final_ids = [x['id'] for x in ITEMS]
    missing = [i for i in inv_ids if i not in final_ids]
    if missing or len(set(final_ids)) != len(final_ids):
        raise SystemExit('ITEM_SET_PROBLEM %s' % missing)
    codes = sorted({b['code'] for r in dp['records'] for b in r['blockers'] if b['class'] != 'V007_ADOPTION_PIN'})
    dp_map = {'CERTIFICATE_POLICY_PENDING': 'R-C1', 'CONFIG_ANCHOR_TAIL_REANCHOR_PENDING': 'R-D4', 'WORKERS_8_SPEC_NOT_REGISTERED': 'R-D2',
              'CAPABILITY_EVIDENCE_PENDING': 'R-D3', 'SENSITIVITY_DECIDING_III_REQUIRED': 'R-B2, R-C5, R-D5, R-D6',
              'COMPARATOR_A68_SUCCESSOR_REQUIRED': 'R-B2'}
    unmapped = [c for c in codes if c not in dp_map]
    gates = {g['gate']: g['class'] for g in dp['campaign_level_gates']}
    gate_map = {'numerics_verdict': 'R-A1 (V007 pins)', 'numerics_verdict / seal allowlist': 'R-A2, R-B3', 'adoption_regeneration': 'R-A4, R-A5',
                'deciding_test': 'R-D1, R-D2, R-D4', 'driver_capability': 'R-D3', 'certificate_policy': 'R-C1', 'u_i_carrier': 'R-C2'}
    cross = {f['code']: f['class'] for f in dp['cross_lane_findings']}
    cross_map = {'V007_PREREG_BINDING_INPUTS_CASE_BLOCK_ABSENT': 'R-A3', 'ORCHESTRATOR_V006R9_R5_ONLY_UNDER_AN_R6_SEAL': 'R-B1 (moot after A96)'}
    trace = {'inventory_items_all_carried': not missing, 'inventory_ids': inv_ids,
             'dryplan_non_v007_codes': {c: dp_map.get(c) for c in codes}, 'dryplan_codes_unmapped': unmapped,
             'dryplan_campaign_gates': {g: gate_map.get(g) for g in gates}, 'dryplan_cross_lane': {k: cross_map.get(k) for k in cross},
             'dryplan_other_problems': {'R6 BUILD not landed': 'R-B1', 'spec bytes change after adoption / registry': 'R-A1, R-A4, R-C1',
                                        'production work dir untested (uncreated local dir)': 'R-D11', 'ADOPT_TAIL None uncertainty rows (S7)': 'R-A6'},
             'new_items_this_part': [x['id'] for x in ITEMS if 'new item' in x['src']]}
    order = {P_SEAL: 0, P_H: 1, P_T0: 2, P_H3: 3, P_C: 4, P_S: 5, P_Z: 6, P_DONE: 7}
    delay_rank = ['R-A3', 'R-C8', 'R-C1', 'R-B3', 'R-B6', 'R-B4', 'R-B5', 'R-D7', 'R-A5', 'R-B2']
    doc = {'schema': 'STEP4_ROOT_ITEMS_FINAL_C4V001', 'utc': utc, 'n_items': len(ITEMS), 'items': ITEMS, 'traceability': trace,
           'most_likely_to_delay_step4_RECOMMENDATION': delay_rank,
           'close_by_legend': {P_SEAL: 'phase P, before the V007 seal (no V007 dependency)', P_H: 'before the headline batch (can close before the seal)',
                               P_T0: 'H1, right after the sealed ADOPT_TAIL', P_H3: 'H3, from the headline receipts', P_C: 'before campaign wave 1',
                               P_S: 'before the sensitivity batch', P_Z: 'after the campaign, before the freeze', P_DONE: 'closed by a ruling'},
           'inputs': {k: {'path': p, 'sha256': sha_file(p)} for k, p in (('inventory_root_items', INV_RI), ('dryplans', DP), ('schedule_sim', SIM), ('registry_probe', PRB), ('reconcile', REC))},
           'fence_blocked': F.BLOCKED, 'producer': {'path': os.path.abspath(__file__), 'sha256': sha_file(os.path.abspath(__file__))}}
    def opened(path):
        # exclusive create, or a compare-and-swap replace of my own earlier output (REPLACE_SHA=<old sha256>)
        if os.path.exists(path):
            want = os.environ.get('REPLACE_SHA_' + os.path.basename(path).replace('.', '_'))
            if not want or sha_file(path) != want:
                raise SystemExit('OUTPUT_EXISTS_WITHOUT_MATCHING_REPLACE_SHA ' + path)
            return open(path, 'w')
        return open(path, 'x')
    with opened(out_json) as f:
        json.dump(doc, f, indent=1, sort_keys=False, allow_nan=False)
        f.write('\n')
    jsha = sha_file(out_json)
    # ---- markdown
    L = []
    L.append('# Step-4 root items, final merged list (dispatch 0587, part 4)')
    L.append('')
    L.append('Claude4 helper, %s (`date -u` at generation). Machine-readable twin: `work/ROOT_ITEMS_FINAL_C4V001.json` (sha256 `%s`). '
             'Root (Claude2) alone decides and launches; every disposition below is a **RECOMMENDATION**. Labels: **TESTED** (recomputed from bytes or by a fenced plan-only probe), '
             '**FORMAL** (code or rulings, file:line cited), **UNTESTED** (projections, fit, future behaviour). Shas are shown as 8-hex prefixes of values computed from bytes; full values are in the JSON and in `work/SOURCE_PINS_C4V001.txt`.' % (utc, jsha))
    L.append('')
    L.append('**What was merged.** All 31 items of `../inventory/ROOT_ITEMS_C4V001.json` (a48ca79d) are carried under their ids; every non-V007 blocker of `../dryplans/DRYPLANS_C4V002.json` (756d36ec) maps to an item (traceability at the end); '
             'five items are new: R-A6 (from the dry plans\' adoption world S7), R-B6, R-C8, R-D15 and R-D16 (found in this part). Rulings newer than both lists are applied: A92 (c2v007r2 is the identity-comparator slot), '
             'A96 (V007 seals on r5; r6 unfinished and unused) and the frozen compare r12 (4bd7b262). %d items in all.' % len(ITEMS))
    L.append('')
    L.append('## Summary')
    L.append('')
    L.append('| id | item | close by | owner | filled by V007 | source |')
    L.append('|---|---|---|---|---|---|')
    for x in sorted(ITEMS, key=lambda y: (order[y['close_by']], y['id'])):
        L.append('| %s | %s | %s | %s | %s | %s |' % (x['id'], x['title'], x['close_by'], x['owner'], x['v007'], x['src']))
    L.append('')
    L.append('Close-by legend: ' + '; '.join('`%s` = %s' % (k, v) for k, v in doc['close_by_legend'].items()) + '.')
    L.append('')
    L.append('**Most likely to delay step 4 (RECOMMENDATION, from the dependency chain):** ' + ', '.join(delay_rank) + '. '
             'R-A3 can stop the V007 verdict itself. R-C8 stops the campaign after its pre-registered points. R-C1 and R-B6 gate the headline batch. R-B3/R-B4/R-B5 gate the campaign machinery. '
             'R-D7 sets the campaign length (8.7 d E / 14.9 d U at max_concurrent 6, against 26.0 / 43.8 d as shipped; UNTESTED).')
    L.append('')
    for grp, name in (('A', 'A. V007 adoption pins and the seal interface'), ('B', 'B. Driver, successors and launch machinery'),
                      ('C', 'C. Science and policy approvals'), ('D', 'D. Run decisions, root-only launches and operations')):
        L.append('## ' + name)
        L.append('')
        for x in [y for y in ITEMS if y['group'] == grp]:
            L.append('### %s: %s' % (x['id'], x['title']))
            L.append('- **What:** ' + x['what'])
            L.append('- **Blocks:** ' + x['blocks'])
            L.append('- **Close by:** `%s`. **Owner:** %s. **Filled by the V007 adoption:** %s.' % (x['close_by'], x['owner'], x['v007']))
            L.append('- **Evidence:** ' + '; '.join(x['evidence']) + '.')
            L.append('- **Recommended disposition (RECOMMENDATION):** ' + x['rec'])
            L.append('- **Label:** %s. **Source:** %s.' % (x['label'], x['src']))
            L.append('')
    L.append('## Traceability')
    L.append('')
    L.append('| from | code or item | final item |')
    L.append('|---|---|---|')
    for i in inv_ids:
        L.append('| inventory | %s | %s |' % (i, i))
    for c in codes:
        L.append('| dry plans (per spec) | %s | %s |' % (c, dp_map.get(c)))
    for g in gates:
        L.append('| dry plans (campaign gate) | %s | %s |' % (g, gate_map.get(g)))
    for k in cross:
        L.append('| dry plans (cross-lane) | %s | %s |' % (k, cross_map.get(k)))
    for k, v in trace['dryplan_other_problems'].items():
        L.append('| dry plans (problems) | %s | %s |' % (k, v))
    L.append('')
    L.append('Unmapped dry-plan codes: %s. Inventory items not carried: %s. Fence blocks in this generator: %s.' % (unmapped or 'none', missing or 'none', F.BLOCKED or 'none'))
    L.append('')
    with opened(out_md) as f:
        f.write('\n'.join(L))
    print(json.dumps({'json': out_json, 'json_sha256': jsha, 'md': out_md, 'md_sha256': sha_file(out_md), 'n': len(ITEMS),
                      'unmapped': unmapped, 'missing': missing, 'blocked': F.BLOCKED}, indent=1))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
