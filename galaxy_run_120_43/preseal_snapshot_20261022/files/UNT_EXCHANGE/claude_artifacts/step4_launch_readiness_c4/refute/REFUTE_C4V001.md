# REFUTE_C4V001: adversarial check of the step-4 launch-readiness package (dispatch 0587)

**Who and when.** A Claude4 helper, refute-by-default lens. Work ran from 2026-10-18T20:08:59Z to 20:43Z (`date -u`). Coordinator: Claude2 (0587, A83, 0592, 0593, 0617).

**Object checked.** `claude_artifacts/step4_launch_readiness_c4/{inventory,dryplans,launch_order}/` as they stood at 20:12Z. Records of record, re-hashed here from bytes:

| File | sha256 |
|---|---|
| `inventory/INVENTORY_C4V001.json` | `eb359e0f902298b4d8d41e879b1ba85f852e4bf29d7d9d126a66dc239baee75b` |
| `inventory/INVENTORY_C4V001.md` | `cabdd70e7df0cedf47a76e4669c7b148bbe9dfb49a6a81f6890a873196cf61ec` |
| `inventory/ROOT_ITEMS_C4V001.json` | `a48ca79d0b0192dc842366d8c50e63a2bd3d9ff45c732e048d39f926eaa0da22` |
| `dryplans/DRYPLANS_C4V002.json` | `756d36ec5ecf15406fd52ddefcb9c57c4212f261cfc5a8fd24489cc7eb77d22d` |
| `dryplans/DRYPLANS_C4V001.md` | `1516c3c0a2c18b15778f78b95b965bfe75a3ca448d6595bd9d358dd21330ce8f` |
| `launch_order/LAUNCH_ORDER_C4V001.json` | `2b4dd6a0bdb0f541793a43f6b2091b586ffbed45532999b99103ae66b01bd6ab` |
| `launch_order/LAUNCH_ORDER_C4V001.md` | `c276c4d9e3c5552d26ae600eac01d97489aaf766daf2abf5e6fe69185a795938` |
| `launch_order/ROOT_ITEMS_FINAL_C4V001.md` | `5d83f0672f9b45fdae31772b2c29c5f786159aa960f0855cc1e258291353ee36` |

**Authority.** Root (Claude2) alone launches. Nothing here launches or authorizes anything. Every fix below is a RECOMMENDATION.

**Labels.** TESTED = recomputed here from bytes or observed in a fenced plan-only process in this folder. FORMAL = read from code or rulings, with file:line. UNTESTED = projections and future behaviour. Every wall-time, memory and disk figure below is UNTESTED unless marked otherwise.

## 1. Verdict: READY_WITH_CORRECTIONS

**What holds (TESTED).**
- The spec bytes, pins and dry plans reproduce.
- **11 of 34 dry plans (32%) were re-run** in fenced processes in this folder. They cover every run kind: TAIL_REANCHOR, WORKERS_8, the trial probe, two headline corners, SENS LO and HI corners, a distance plan, the campaign seed, deciding (iii) under r5 and deciding (iii) under v009-GEO.
  - Every one exits 0 with 0 executed stages.
  - Their DRYRUN reports equal the dry-plan lane's reports leaf for leaf. The only differences are report-directory paths and the digests derived from them, resolved recursively. 0 residual leaves.
- **622 pins over 413 paths** in the six JSON records re-hash with 0 mismatches.
- All three HASHES manifests verify.
- The structural finding R-C8 is confirmed from code.

**What does not hold.** Two items block the launch order as written:
- **F01:** a pre-seal launch of the deciding-(iii) runs, against 0587, 0610 item 4 and 0616.
- **F02:** the unguarded fallback, which 0620 removed.

There are also seven SHOULD_FIX items (F03-F09) and four NOTEs (F10-F13). The main SHOULD_FIX items are:
- a blocker misclassified as a V007 adoption pin on 27 of 30 specs;
- a ramp memory model below the reviewed 0538 model;
- missing certificate-production and disk-volume estimates.

All of these are documentary or ordering corrections. None needs new science.

## 2. Findings, most severe first

### F01 BLOCKING: the deciding-(iii) runs are ordered before the sealed ADOPT_TAIL, against the governing dispatches

- **Claim in the package.**
  - LAUNCH_ORDER md L33: "The 4 tail-OFF deciding-(iii) runs go first, before the seal, as 0540 F3 and A61 F3 allow."
  - Phase P2 at L147 launches them now.
  - L208: "The DIII plan has its own pre-seal admission."
  - Phase S1 at L149, and JSON L422, allows "DIII only, if still pending, at background priority" while step 2 runs.
  - INVENTORY md L112-115 mark them "may precede the seal". ROOT_ITEMS_FINAL R-D5 has "Launch before the seal".
- **Why it is refuted (FORMAL).**
  - 0587 (fe54bb9f) names "the deciding-(iii) per-D tail-OFF reruns" as step-4 runs. It then says: "Step 4 can only launch after a sealed V007 ADOPT_TAIL. Everything up to the launch can be ready before that."
  - 0616 (634bca4e, 19:58Z) specifies the step-4 launcher for exactly these runs, including the deciding-(iii) reruns. It requires a "post-adoption guard: it refuses unless a sealed V007 verdict reads ADOPT_TAIL, verified from bytes".
  - 0620 (037a2a61) lists the sealed ADOPT_TAIL as an admission control that must be enforced "before any process starts".
  - 0610 item 4 (29e72c1c) asks the cross-lineage reviewer to confirm "nothing launches before a sealed V007 ADOPT".
  - The rulings cited for the exception do not say "before the seal". 0540 F3 (801d47fd) says "Root launches them during calibration prep". A61 F3 (addendum 7f552858 L533) says "These are root launches during calibration prep." Per 0587, preparation stops at the launch.
- **Second problem (UNTESTED model, FORMAL rules).** Phase S1 lets 4 tail-OFF calls, each with 8 route-A workers, overlap the V007 step-2 ramp.
  - Neither launcher counts the other's route-A cases. V005 `available()` counts only its own cases (launcher 861bba68 L46-48). The package's R-D15 covers only campaign versus direct batch.
  - Background QoS lowers CPU priority, not memory.
  - Under the reviewed 0538 per-case model (helper C `caps_model.json` 4a5a0bd6), the six largest V007 cases in route A model at about 130 GiB: 29.0 + 25.9 + 4 × 18.79. That is why the V005 25%-free gate exists.
  - A tail-OFF DIII route A adds about 10.5 GiB each. Either the V007 gate holds T-cases back, which is a seal-path delay against A89's no-delay rule, or memory realizes after admission. Helper C C-0537-2 shows macOS `ps` RSS omits compressed pages, so per-call caps would not see it.
- **The move costs nothing.** In the package's own plan, the deciding-(iii) evidence gates only SENS, which runs after the campaign (L155, L321). Running deciding (iii) after T0 is therefore off the critical path.
- **Fix (RECOMMENDATION).**
  - Move the DIII batch after T0. For example, run it after the headline batch, or after FINAL_SUMMARY and before SENS, under the 0616 guard.
  - Alternatively, obtain an explicit root ruling for a pre-seal tail-OFF exception. Record it in the addendum, and carry a matching exception in the 0616 admission.
  - In either case, forbid any overlap with step 2.
  - Fix the same text in INVENTORY (L112-115, L149), ROOT_ITEMS_FINAL R-D5, and the LAUNCH_ORDER DAG and phases.

### F02 BLOCKING (already ruled): the unguarded zero-build fallback is still in the package

- **Present in bytes (TESTED, grep at 20:3xZ):**
  - LAUNCH_ORDER md L214-216: "Fallback with no build. The campaign_c2v005 CLI ... can run a direct batch";
  - JSON key `fallback_zero_build` at L547;
  - ROOT_ITEMS_FINAL R-B6, L146 ("or they use the zero-build fallback") and L149 ("Fallback until then: campaign_c2v005 CLI per batch").
- **Ruling (FORMAL).** 0620 (20:07Z), on Codex2 0494 (b633c98e): "That fallback is **removed** from step-4 readiness. Step 4 launches **only** through the guarded path." The raw CLI enforces none of these before process creation: the sealed ADOPT_TAIL, the step-4 admission, the PRELAUNCH, certificate and sensitivity checks, or the r5 allowlist.
- **Fix.** Delete the fallback from the md, the JSON and R-B6. Make R-B6 depend only on the 0616 packet: "if the guarded packet isn't ready when V007 adopts, step 4 waits for it".
- **Independent confirmation.** This finding is Codex2's (0494, BLOCKING). I confirmed it from bytes.

### F03 SHOULD_FIX: PENDING_UV_TAIL_CERTIFICATE is classified as a V007 adoption pin on all 30 tail-ON specs, but for 27 of them the slot is a per-point registry item (R-C1)

- **Claim.**
  - DRYPLANS md L34: 30 V007_ADOPTION_PIN.
  - L167-171: "adoption fills the block's slots ... Every spec inherits them ... FILL_PROBE dry plans with these pins have zero blockers on 30 of 30 specs."
  - TESTED tally from `DRYPLANS_C4V002.json`: all 30 records carry `class` V007_ADOPTION_PIN with `class_in_tool_record` OTHER_ROOT_ITEM. The aggregator (H3) overrode the per-spec tool.
- **Why it is refuted (FORMAL).**
  - The core `Mapper.build` (a595c5c0 L249-259) overwrites `eps_certificate`/`lo_certificate` from the registry record of the point.
  - The wrapper certificate check (24abe3bc L145-161) requires the bundle's `driver_certificate_bindings` to equal the spec slots. It requires the LO proof to cover all consumed states ("no anchor substitution", L160-161). The policy gate fixes `driver_slot_rule: POINT_EPS_AND_REVIEWED_PRELAUNCH_LO_ENVELOPE` (L74).
  - `PER_POINT_REQUIREMENTS_CX2V001.json` (8f690fc9) says: "LO: No anchor promotion." `CERTIFICATE_ANALYSIS_CX2V001.md` (4084bd59) says: "An anchor EPS or LO pass is not a box pass".
  - A73 (addendum L814) says: "certificate slots are left to the certificate registry; the block itself is guarded by the sealed V007 ADOPT."
- **What the code supports.**
  - The V007 adoption supplies the slot default at most for the 3 specs whose point identity equals C4T: TAIL_REANCHOR, the WORKERS_8 anchor repeat and HEADLINE_TRIAL, all point key 8ad6ca4e8678 (TESTED).
  - For the other 27, the slot is filled from the per-point registry, a root item: 8 headline corners, 16 SENS corners, 2 distance plans, and the campaign seed (6944e210, a distinct point about 1e-15 off).
  - The FILL_PROBE puts anchor records on corner specs, which the policy forbids. Its "30/30 zero blockers" is a driver-layer statement only. The driver checks only the certificate sha (driver b5cc62af L1076-1081; tail library 2026f2b6 L664-673). The probe says nothing about whether a corner can launch.
  - The per-spec tool's own text (dryplan_one_c4v001.py L259-266) already said this.
- **Fix.** Reclassify to at most 3 V007_ADOPTION_PIN and at least 90 OTHER_ROOT_ITEM. Map the 27 to R-C1. Reword DRYPLANS section 5 and section 1, and the R-A1 evidence line.

### F04 SHOULD_FIX: "launch-ready apart from V007 pins" contradicts the package's own admission design and 0620

- **Claim.**
  - DRYPLANS md L45: TAIL_REANCHOR is launch-ready apart from V007 pins. CERTIFICATE_POLICY_PENDING is "not on the launch path, because `check_deciding` ignores the slots".
  - L46: the 4 DIII runs need "None at all ... **nothing** from V007".
- **Why it is refuted (FORMAL).**
  - The launch order's own R-B6 admission requires "Per tail-ON call: a pinned root PRELAUNCH record (`prelaunch_check` PASS under C1)". With the registry pinned, `prelaunch_check` runs the certificate check (wrapper L178-180). An unregistered point refuses `CERTIFICATE_POINT_MISSING_OR_MISMATCHED` (L86-90), and this is TESTED by the launch lane's own registry probe.
  - 0620 makes the certificate check and the sealed ADOPT_TAIL admission controls for every step-4 process.
  - So R-C1 is on TAIL_REANCHOR's launch path, and the seal is on DIII's (see F01).
- **Fix.** State the launch path per run as: seal, then 0616 admission, then PRELAUNCH under C1, then registry entry. List the DIII prerequisites as: seal (F01), R-D5 caps and the 0616 packet.

### F05 SHOULD_FIX: the ramp's memory model is below the reviewed model that set the 0538 RSS minimums, so the "cap 3 keeps ≥ 25% free" rationale is not shown

- **Claim.** LAUNCH_ORDER md L234 and L239: route-A cap 3, modelled minimum free memory 31.1% (U), "sized from measured RSS (about 10.5 GB ... plus 0.40 GiB per worker)". The simulator sets `MEM_RA_TAIL_ON = 10.5 + 8 * 0.40` = 13.7 GiB (schedule_sim_c4v002.py L27), and that formula mixes GB and GiB.
- **Refutation.**
  - 0538 (acf2269a) adopts helper C's figures as the minimum RSS caps: 28 GiB for 96-node K128 cases, which is 1.5 × about 18.7 GiB.
  - Helper C's model (`caps_model.json` 4a5a0bd6, row C4T) gives `ship` **18.79 GiB**, against `episode` 14.03 and `build` 14.37. The ship term is the parent's 3S plus 8 workers × 3S of pickled TailState at every route-A iteration (FINDINGS_C ef575a8d L39-42; caps_model_c.py L57).
  - The package's own R-D8 recommends the 28 GiB caps, so it is internally inconsistent.
- **Recomputed with the package's own worst static configuration (UNTESTED, TESTED arithmetic).**
  - Cap 3 (3 calls in route A, 7 in route B at 4.3 GiB, plus 17 GiB background): 3 × 18.79 + 7 × 4.3 + 17 = 103.5 GiB, so **19.2% free**. That is below the 25% gate.
  - Cap 2: 2 × 18.79 + 8 × 4.3 + 17 = 89.0 GiB, so 30.5% free.
  - The real gate would throttle starts, so the 15.55 h U headline makespan is optimistic.
  - The background figure of 17 GiB rests on one reading at 19:32Z. The task text reports load about 36 at other times.
- **Fix.** Re-run the simulator with the 0538 per-case peaks. Either propose cap 2, or keep cap 3 with an explicit statement that the gate is expected to bind, and re-estimate the makespan. Keep the "raise later only on measured peaks" rule.

### F06 SHOULD_FIX: certificate-production compute is missing from the run inventory, the critical path and the "not modelled" list

- **Facts.**
  - R-C1 needs 28 prelaunch bundles before H2. Each needs a GQ record (one TESTED example: 37.13 s at C000, `GQ_P128_MS128_C000_R5_CX2V001.json` a785ccca). Each needs per-point EPS/ρ tables, which were "not executed" (BUILD_CERTIFICATES 48a14010), and an LO slot that needs a reviewed producer successor.
  - R-B5 needs post-state LO and GQ proofs for every consumed state of every completed campaign call before it can be cached (wrapper L95-118, L265-276). Some 120 calls ingest INFRA until then.
- **What the package does with them.** None of these jobs has a wall-time line. H1 and H3 say "not estimated". LAUNCH_ORDER section 5.5's "Not modelled" list omits them, and the campaign figure of 209.8 h E / 356.5 h U assumes zero acceptance time between waves.
- **Fix.** Add them as unestimated critical-path items (UNTESTED), with an owner and a timing basis. The inventory should also list them as root-launched or lane-run compute jobs.

### F07 SHOULD_FIX: there is no disk-volume estimate and no output location for the direct runs

- **Facts.**
  - Outputs are all kept: the principal's ~18:40Z ruling sets intermediate cleanup to NOT USED.
  - R-D8 proposes 96 GiB output caps for each direct tail-ON run.
  - Helper C's reviewed per-call output model for a 96-node K128 tail-ON call is 21.5 GiB typical and 57.7 GiB worst (caps_model.json).
  - The config's measured figure is 6.08 GB, for a tail-OFF anchor run (config `disk_guard`).
  - Free space by `df` at 20:2xZ (TESTED): External1 3.2 TiB, internal 458 GiB.
  - A99 V6-S2 (0621) puts the V007 step-2 outputs on the internal SSD.
- **Projection for 150 tail-ON step-4 calls (UNTESTED):** roughly 0.9 TB at the config figure, about 3.15 TiB typical, and about 8.45 TiB worst. The typical case alone about equals External1's free space.
- **What the package covers.** LAUNCH_ORDER and ROOT_ITEMS state no output path and no disk budget for the 35 direct runs. The only disk logic is the campaign's `disk_guard` and the ENOSPC-at-start halt.
- **Fix.** Add a disk plan: per-class output location, preferably External1 per the principal's ~18:20Z instruction; a batch disk guard for direct runs; and the D3 retention decision, which is still OPEN in the coordinate spec. Do this before H2.

### F08 SHOULD_FIX: the R-C8 cache-id prose is stale and does not match its own probe JSON

- ROOT_ITEMS_FINAL L214 and LAUNCH_ORDER md L364 say the cache id changes "4555ce79… → b3839787…", citing probe **v002**.
- Probe v002 (`REGISTRY_GROWTH_PROBE_C4V002.json` 4cfc6283) records NULL `878d612a…`, R0 `4f0521aa…` and R1 `b370470a…` (TESTED).
- 4555ce79 and b3839787 are probe **v001**'s values. They are the only 8-hex strings in LAUNCH_ORDER md that are found in no package pin (TESTED).
- The conclusion is unaffected; I confirm R-C8 from code below.
- **Fix.** Cite v002's values, as 0620 asks. Codex2 0494 and 0497 reported this independently.

### F09 SHOULD_FIX: published records were overwritten in place after a reviewer had pinned them, and the reviewed bytes are gone

- Codex2 0491 (20:02:10Z) pinned LAUNCH_ORDER json `056defdf…` and ROOT_ITEMS_FINAL md `218b5574…`.
- The builders then replaced both in place by "compare-and-swap" (`open(path,'w')`, build_launch_order_c4v001.py L344-349 and build_root_items_final_c4v001.py L246-252): 056defdf → facda76c → 2b4dd6a0, and 218b5574 → 3d9f70f3 → 5d83f067.
- No file in the package has any superseded sha (TESTED search). The inventory did the same with its first generation (25da7468/be5a5887, d197b0c3/ae2ce930).
- **Fix.** Restore exclusive-create versioning (`…_C4V002`) with the superseded bytes kept, so that a pinned review can be re-read.

### F10 NOTE: the r6 conclusion holds, but the dry-plan lane's supporting detail is wrong

- **The conclusion holds (TESTED 20:12Z).** `driver_r6/` has no BUILD*, HASHES* or SHA256* at depth ≤ 2. The driver is still 24c9f54c and the cascade map cd903ade. A96 (19:51Z) stops r6, and 0615 says "there is no r6 branch".
- **The detail is wrong.** DRYPLANS section 3 lists only specs/, gates/, out/ and module/, and says "Every file's mtime is 16:08–16:16Z". cascade/, logs/, tests/ and tools/ also exist. File mtimes run from 15:52:07Z (tools/profile_build_c2v001.py) through 16:55Z (logs/module_suite_V601.log). New files appeared at 19:47-19:49Z: tests/plumbing_r6, race_unit, tools/project_wall_c2v002 and out/PLUMBING_R6_V001.json.
- **The ready-to-run r6 tooling is moot.** Its R6TC variant assumes "root's registered calibration cache block (A72, A81 RI-24)". RI-24 governs V007 T-runs only and is moot (A96). No calibration cache rule exists, and caching for steps 4-5 is "decided later" with A85.1.

### F11 NOTE: wall-time labels

- **LAUNCH_ORDER section 5.2** presents three walls as "Measured completed runs": 2.88, 3.48 and 3.50 h.
  - They come from root's ruling text (A67 start 14:56Z; A92 ends), not from a log. Rule 9 asks for the log, or UNTESTED.
  - B0P_RERUN admitted its route A from a saved run (addendum L215), so it is not a full call.
  - The inference "so that projection is not optimistic" is unsupported.
- **INVENTORY md L53** gives "about 40 s each" for 28 GQ records. That extrapolates one 37.13 s record and is unlabelled.
- **ROOT_ITEMS_FINAL R-A5** labels the 8.74-8.77 h projection "(TESTED arithmetic)". The arithmetic is right (TESTED: TIMING_V003 keeps the I = 7 route-A baseline [1014.9, 1040.8] s inside its I = 32 total). The figure itself is UNTESTED.

### F12 NOTE: smaller gaps

- **PC-7 and the dual-use options.** PC-7 is OPEN in the coordinate spec (50e7288e): "repeat call at the anchor; outside the cache". The default 10-run batch already holds an anchor repeat: the fresh TAIL_REANCHOR plus HEADLINE_TRIAL, which differ only in `/label` (TESTED). DU-1, alone or with DU-2, removes it, so DU-1's saving (0.26 h E / 1.74 h U) is cancelled if PC-7 is required. R-D12 does not say this.
- **The Jacobian side points.** R-C8 itself says the Jacobian side points, like the seed, are fixed before any result. Wave 1 is the 1-call seed (TESTED in the dry plans' orchestrator plan), and WAVE_FIXTURE_V001 then shows a 3-call Jacobian wave. Pre-registering those 3 points with the 28 would let waves 1-2 run under v006r9 before R-C8 bites. R-C1 counts only 28.
- **R-D5's cap value is ambiguous.** It recommends 16 GiB RSS ("A52/A67 caps") but adds "24 GiB gives margin".
- **The orphan wait cap.** It is 29,400 s, the 8 h cap plus 600 s. R-A5 should raise it with the wall cap, or a resumed wave may return ORPHANS_STILL_RUNNING (v005 L2672-2707). This fails safe.
- **Newer rulings.** These postdate the package's last read: A97, A98, A99 (D-03: Claude4 builds the case block, and prereg r5 has been in progress since 20:21Z) and A100. R-A3 is now owned and in progress, not merely open. A99 V6-S2 moves step-2 outputs to the internal SSD (see F07).
- **A count inconsistency.** INVENTORY says "33 direct root runs before the campaign". The launch order puts SENS (18) after the campaign.

### F13 NOTE: the A82 no-write hazard covers all of step 4, not only the V007 compare

- The calibration adoption policy (7c726fa2 L56-59) reads `PIN_ADDENDUM_V005` from the sealed compare. It then re-reads that path from bytes against the frozen sha.
- It does this at every Context construction, and again at every pre-wave `fresh_gates` (v005 L1943-1947 recompute `numerics_verdict`).
- If the sealed compare cites the open V005 path rather than a `_FROZEN.md` copy, one root write to the open file after the freeze closes `numerics_verdict` for every later campaign wave. A99.6 confirmed the hazard live for the compare.
- **Fix.** R-D14 should say that the A82 rule must hold for the whole 9-16 day campaign, or that the sealed compare must cite the frozen copy.

## 3. Claims that survived refutation

- **Spec identity (TESTED).** These pairs differ only in `/label`:
  - TAIL_REANCHOR against Codex2's `ANCHOR_SPEC.json`;
  - HEADLINE_CORNER_010 and _111 against the v006r7 HEADLINE templates;
  - SENS C000_DLO and C111_DHI and DISTANCE_UPPER against the v006r7 templates;
  - TRIAL and WORKERS_8 against TAIL_REANCHOR.

  The trial physical and coefficients equal the registered anchor bitwise. The D hex values equal the pair-plan keys (0x1.fd93c1f526ddfp+1, 0x1.0722c532c2345p+2).
- **The orchestrator layer reproduces (TESTED).**
  - The cache id is 878d612a… in every tail-ON re-run, the same as the dry-plan lane's.
  - Point keys match.
  - The mapper rebuild matches the probe points and the seed (3958aed3…).
  - `prelaunch_check` PASSES at D = 4.04 and refuses SENSITIVITY_DECIDING_III_REQUIRED at both alternate D.
  - The deciding-(iii) `plan_pair` matches, `validate_tail_off` passes on the raw and normalized specs, and `compute_pair` refuses COMPARATOR_A68_SUCCESSOR_REQUIRED before any run read.
  - `gates_ok` is false, with the six gate reasons as reported.
- **R-C8 (FORMAL).**
  - The cache id includes the whole `tail_readiness` dict (wrapper L52-55).
  - `make_plan` calls `prelaunch_check` per call (v005 L3309).
  - With a registry pinned, an absent point refuses (wrapper L86-90, L178-180).
  - C4-2 holds one cache id per work dir (v005 L3094-3100).
  - The campaign therefore cannot admit engine-proposed points under v006r9.
- **The run inventory is complete against the code and rulings (FORMAL).** It covers:
  - the `probe_points` set (trial + 2³, v005 L2041-2053);
  - check_deciding's {reanchor, workers_8};
  - 8 × 2 SENS corners and 2 distance plans;
  - 2 × 2 deciding-(iii) runs;
  - the campaign;
  - post-S1.

  Dropping the KB064 templates is justified: A55 says "every tail-corrected case use[s] cylinder K_big = 128", and `validate_block` refuses K_big ≠ 128. That explains 0533's older "32 corners / 4 distance plans" count. The only omissions are the compute jobs in F06.
- **Other confirmations (FORMAL or TESTED).**
  - v006r9 accepts r5 only (core L25, L133-135; wrapper L47-48).
  - DU-2 satisfies `check_deciding` (core L114-197).
  - The V005 launcher facts hold: 10 cases, KHI first, `max_active` 6, 25% free, 60 s, first route-A iteration ramp (launcher 861bba68 L46-83, L153). Route A is the stage named `route_a`, at stage 01, in both drivers.
  - The TIMING_V003 inputs and the arithmetic in LAUNCH_ORDER section 5.1 reproduce from bytes (3e3fb600).
  - R-A3's absence holds: prereg r4 e3b6b5b2 `binding_inputs` has no `case_block`.
  - V7-SCHEMA: the frozen compare r12 (4bd7b262 L364) keeps `SCHEMA_REPORT = 'UNT_KMAX_TAIL_COMPARISON_C2V007_R11'`. That passes the adoption policy's prefix rule (L67). `PRODUCTION_K_BIG_A55 = 128.0` is present (L284).

## 4. Conduct audit of the three agents (reads, writes, fences)

- **Fence records (TESTED).** I aggregated every `blocked` / `fence_blocked` field in the package: 300 fields.
  - Exactly one is non-empty: the dry-plan lane's `probe_v001`. There the fence refused the driver's own code file `uvt_route_b_binding_c2v001_r5.py`, which was refused and not read; that refusal is H1.
  - `runs_ext_opens`: 0 non-empty out of 277.
  - `target_word_opens`: 0 out of 208.
  - No tool references a runs_ext, UVT_* or C5H path except to refuse it (grep).
- **Disclosed reads outside the code, none protected by the path rules:**
  - the DDO154 calibration observation region `CODEX1/DDO154_CALIBRATION_OBSERVATION_REGION_V001.json` (Context construction, by the dry-plan and launch lanes, as Codex2's checks do);
  - `CLAUDE2/runs/A2_ANCHOR_F10_RUN_V001/result.json` (the r5 dry run's M_T pin).

  The dry-plan lane's records keep only a count of outside opens (277 for TAIL_REANCHOR). My re-run of the same plan shows that those opens include the coefficients npz `CLAUDE2/CRITICAL_PATH_EVALUATION_2026-10-17_V001/sampler_eval/CANDIDATE_4CHAIN_POOLED_GRID_V001.npz` and seven CODEX1 DDO154 driver-input JSONs, among them `DDO154_MONOTONE_SOURCE_RECONSTRUCTION_RUN_V001/source.json` and `DDO154_STABLE_CACHED_COUPLED_TRIAL_SEED_V002.json`. They are opened by `cmd_dry_run`, not by Context construction. DRYPLANS section 9 does not list them. The launch lane's probe ran no driver dry run, and it logs only the observation region. Root may confirm that DDO154 calibration inputs fall inside "no target reads".
- **Writes (TESTED as far as bytes allow).**
  - No `*.pyc` was written under `claude_artifacts` outside the package after 18:25Z.
  - The tools write only by exclusive create inside their own folders, except the in-place overwrites in F09, which stay inside the package.
  - Stat calls cannot be audited by the fence: `os.stat` has no audit event. UNTESTED.
- **Rule deviations, disclosed by the lanes:**
  - the dry-plan lane used `/usr/bin/python3` (3.9.6) for JSON inspections and three in-folder patches, against rule 4;
  - the launch lane hit one zsh `echo ======` slip, against rule 6.

## 5. This check's own conduct

- **No launches.** Only plan-only modes ran (`cmd_dry_run` simulate, Context, `prelaunch_check`, `certificate_check`, `plan_pair`, `validate_tail_off` and a refused `compute_pair`). Each ran in its own process under `tools/fence_c4v002.py` (18510e3a), with `taskpolicy -b` and BLAS = 1.
  - `fence_c4v002.py` is a byte copy of the dry-plan lane's documented variant. Its selftest is 15/15 in this folder.
  - Its one relaxation over fence_c4v001 (f813c430) admits a lowercase `uvt_*.py` driver code file outside runs_ext. It also adds casefolded runs_ext matching and refuses listing runs_ext, UVT_* and C5H.
  - No runs_ext read was relaxed, so no further variant was needed.
- **Fence results.** BLOCKED was [] in all 12 re-run processes. Opens of runs_ext, target-word paths, C5H and NGC3198 data: 0.
- **Lowercase `uvt_` opens.** The only `uvt_` opens were driver code files under `driver_r5/cascade/`.
- **Other opens.** Context construction opened the DDO154 calibration observation region. The driver dry runs opened the coefficients npz, the CODEX1 DDO154 driver inputs and the A2F10 anchor result, as section 4 lists.
- **Disclosure.** One zsh `echo ===` slip of mine failed with "== not found" and had no other effect. Two harness bugs in my own leaf attribution were fixed by versioning: a relative path (V001/V002), then recursive derived digests (V003). The record of record is `reruns/LEAF_ATTRIBUTION_V003.json`.
- **Addendum read.** Read at 20:12:37Z as cf9bbf19 (130,524 B) and at 20:35:05Z as 7f552858 (134,891 B). Both snapshots are in this folder.

## 6. Files

| Path (in this folder) | What it is |
|---|---|
| `REFUTE_C4V001.md` | This report |
| `PARTIAL.md` | Work log |
| `tools/fence_c4v001.py`, `tools/fence_c4v002.py` | Fences (copies; shas above) |
| `tools/rerun_one_c4r001.py`, `tools/run_reruns_c4r001.zsh` | Independent re-run tool and runner |
| `tools/attribute_leaf_diffs_c4r001.py`, `tools/attribute_leaf_diffs_c4r002.py` | Leaf attribution (v002 recursive) |
| `tools/rehash_pins_c4r001.py`, `work_REHASH_C4R001.json` | Re-hash of 622 pins (0 mismatches) |
| `reruns/run_v001/*/RERUN_RECORD.json`, `reruns/RUN_LOG_V001.txt` | 11 re-run records |
| `reruns/LEAF_ATTRIBUTION_V003.json` | Attribution of record (V001/V002 kept, superseded) |
| `reruns/test_v001/` | First harness test (TAIL_REANCHOR), kept |
| `V005_ADDENDUM_snapshot_refute.md`, `V005_ADDENDUM_snapshot_refute_2.md` | Addendum snapshots |
| `HASHES.txt` | sha256 of every file here except itself |
