# DRYPLANS_C4V001: step-4 dry plans (dispatch 0587, part 2)

**Who:** a Claude4 helper. The work ran from 18:27:40Z to about 19:15Z on 2026-10-18 (`date -u`).

**What was done:** plan-only work. Nothing was launched, and no stage, solver, campaign or project calculation ran.

**What was not read:** C5H, any `UVT_*` object and any NGC3198 target. No runs_ext path was opened, listed or stat-ed.

**Evidence labels:**
- **TESTED** means it was observed in a fenced plan-only process in this folder.
- **FORMAL** means it was read from code or bytes.
- **UNTESTED** covers everything else.

**JSON of record:** `DRYPLANS_C4V002.json`, which holds one record per spec per driver.
- `DRYPLANS_C4V001.json` (e301bafd…) holds identical records.
- V001 is superseded only for one field, `r6_ready_to_run`. Its pointer named runner v001, which calls the harness diff v001. Runner v002 calls diff v002.

## 1. Result

**All 34 dry plans are PLANNED (TESTED).**
- They cover 32 distinct spec files, each dry-planned under its driver:
  - 30 tail-ON calibration specs under driver r5 (b5cc62af…);
  - 2 deciding-(iii) spec files, each planned twice, once under r5 and once under v009-GEO (237ef3d4…).
- Every plan ran in its own fenced process with `taskpolicy -b` and these results:
  - exit 0 and `executed_stages` 0;
  - no binding blocker, unexplained refusal, pin problem, scipy import or stage-admission refusal;
  - the r4 `plan_checks` (0ecb7605) were all true.
- The fence refused nothing in any process. Nothing under runs_ext, no `UVT_*` object, no C5H path and no target-word path was opened.

**The per-spec blockers total 93, after classification:**

| Class | Count |
|---|---|
| V007_ADOPTION_PIN | 30 |
| OTHER_ROOT_ITEM | 63 |
| DEFECT | 0 |
| HARNESS | 0 |

Three harness problems were found and fixed before the records of record were made (section 9).

**Launch-path view.** These are the blockers that stop a given run from launching. Post-run registrations are counted separately.

| Group | Runs | Blockers |
|---|---|---|
| Launch-ready apart from V007 pins | `TAIL_REANCHOR` | V007 pins only |
| Launch-ready apart from V007 pins | `DECIDING_III_{HIGH,LOW}_{R5,V009GEO}` (4 runs) | None at all. These four need **nothing** from V007. |
| Not reachable today | `HEADLINE_TRIAL` and the 8 `HEADLINE_CORNER_*` (the A32 box probes) | The root decision on per-point certificates: CERTIFICATE_POLICY_PENDING (section 4) |
| Not reachable today | `CAMPAIGN_W1_SEED` | The same decision, plus every campaign gate (section 5) |
| Not reachable today | `WORKERS_8` | No registered spec. Reusing a headline corner run resolves this (section 8). |
| Not reachable today | 16 `SENS_CORNER_*` and 2 `SENS_DISTANCE_*` | deciding-(iii) evidence, a review registration and an A68 comparator successor, all needed per D |

**r6 dry plans: DEFERRED. The r6 BUILD has not landed (section 3).** A ready-to-run r6 script is built and self-tested.

**Cross-lane DEFECT (FORMAL).** Section 6 has the details.
- Prereg r4 (e3b6b5b2) has no `binding_inputs.case_block`.
- The sealed-mode compare (r11 a5d10cb1, r12 73031283) refuses CASE_BLOCK_ABSENT without it.
- The calibration adoption policy also needs that binding.

## 2. Sources, pinned from bytes in this session

| Object | Path (abbreviated) | sha256 |
|---|---|---|
| Orchestrator v006r9 | `calib_tail_readiness_cx2/v006r9/calibration_orchestrator_cx2v006r9.py` | 24abe3bc4f6ee0e3c5d7c89502062cf99464573b35bc5b53c33c14ef2ae888af |
| Core v006r9 | `.../v006r9/calibration_core_cx2v006r9.py` | a595c5c0929fc0a8313bcdff3b79241f1e3ba8f77dc3749adc06b2a982b43605 |
| Config | `.../v006r9/RUN_CONFIG_DDO154_CX2V006R9_P128_MS128.json` | 721c7230f3f3efde6f8406f13a52995ae321248829ab1ee64a2f522ad5582b8e |
| v006r9 BUILD.md / TYPED_BLOCKERS | `.../v006r9/` | 29bcf9b6… / 1198bdef… |
| Static check (Codex2) | `.../v006r9/check_static_dry_cx2v006r9.py` | 8de49717aa9df12aead3f3a809debf2d342a779dddbd27a5f31278de0a65d1e6 |
| Saved static results (Codex2) | `.../v006r9/STATIC_DRY_RESULTS_CX2V006R9.json` | b50cf7cf56e9409959c88a5b621b688ae3d721e52da76723a22e8a609cd89964 |
| Sensitivity policy r8 v002 | `.../v006r8/sensitivity_policy_cx2v006r8_v002.py` | 8fb0660077d56ddc787ac67386f8def72e6f5a04fd14e44eb20ed9facf19de4f |
| Registered anchor | `.../v006r8/REGISTERED_ANCHOR_CX2V006R8.json` | 7693959ceca48581a06c1ca439c02bd80fd2ecfb158073270e3d2dc614ea79c3 |
| Adoption policy r7 | `.../v006r7/adoption_policy_cx2v006r7.py` | 7c726fa2ad3f3e0fbcfcf36353901f970cde1eff3f76321327e5a8a5fbc29b1d |
| Deciding-(iii) pair plan | `.../v006r7/DECIDING_III_PAIR_PLAN_CX2V006R7_V002.json` | cb42a5a3bf8e26d0aa2a3a4c35784c2301fde7ff6c60170da7536ba8cfd95656 |
| Parent v005 orchestrator | `calibration_orchestrator_c2/v005/calibration_orchestrator_c2v005.py` | c75a889ff4646a816329756124a19532cbc166d26f47ce2ea5147b71c2cf7c4d |
| Driver r5 | `tail_scheme_impl_c2/driver_r5/galaxy_m0_forward_c2v010.py` | b5cc62afb7814b4f337a012a1ffd1f1e677f398ac18a1f8297c7ff49ae5374c6 |
| Driver r5 BUILD.md | `tail_scheme_impl_c2/driver_r5/BUILD.md` | 0c18831261435a7e04401ccba31fb6bbe1a01809505055036d876c13c5e364b2 |
| Driver v009-GEO | `stage_successor_gal_c2v005/driver/galaxy_m0_forward_c2v009.py` | 237ef3d41daf4d99b0aafed3e90b27b095a741a9f66ea06ea34f3e44876d47bb |
| Anchor template | `CLAUDE2/specs/CALL_A2_ANCHOR_F10_C2V001.json` | a93c95b95c1f112b7293ffd598371335227cb93d7334981be33e368c6cd9f52b |
| Coordinate registration | `calib_tail_readiness_cx2/DDO154_COORDINATES_CX2V006.json` | 50e7288e4697c8c8bca0544a4b81b5b15462c10efaed2d437530b95d8a80951f |
| V007 C4T spec, TEMPLATE / FILLED | `v007_launch_packet_cx1/P128/specs/C4T_P128_MS128_R5_CX1V004.{TEMPLATE,FILLED}.json` | 13cfe988… / de6d7d77d053d9c983f15eca11468fe8520d025ff2ad1f643b2a517a915b1738 |
| A70 slot records | EPS_CERT_V006 / LO_CERT_V004_MS128 | 598c8fa34dc85113aa99dd3722f6b37f6625149995d7365c8cbd1b796f830192 / 1c384f763e663d85414f25ef8c02b4291efd88b63353a77961f2e88aca2e204a |
| V007 prereg of record r4 | `v007_final_prereg_c4/r4/KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R4.json` | e3b6b5b2ba265f54d15381f358913dd3ea931761aaa649c98a7583f58f1b7cf8 |
| Compare r11 (frozen) / r12 (as of 18:52Z) | `v007_compare_c2/r11/…_r11.py`, `r12/…_r12.py` | a5d10cb1a213931713b9712da0781042d8e02ed5c1e81cda21b97c33b0559c8a / 73031283e9159fd4846a3eeadee88f1d0931245f78eba725f9179b450884e974 |
| Dispatch 0587 | `FROM_CODEX/0587_…` | fe54bb9f0a8ef38bffb888d1ecd7bcdee8f876984f6db2539e59ad2a50283f61 |
| Open addendum V005 | as read | d03e75b7… (110,415 B, 18:30Z); 0753f2d8dc437592a4ad70140f309c774837cb07e9c04e2c213c4421eeb8e87e (120,185 B, 19:11Z; it adds A86–A91, none of which changes these plans) |
| Fence used (v002) | `tools/fence_c4v002.py` | 18510e3ae2a8fb84536059dff86057e2ef2eee23c05bf1fc419056cf41656762 |
| Fence copied (v001) | `tools/fence_c4v001.py` | f813c43099cfdadd3a779e395d223887d0df7cd8c8a8eb67b3a73de86eb699f0 |

## 3. r6: DEFERRED, BUILD not landed (TESTED from bytes)

**The decision.** This was checked at 18:30:51Z, 18:48:45Z, 18:58:24Z, 19:09:44Z and 19:10:48Z.
- `tail_scheme_impl_c2/driver_r6/` holds a driver file (24c9f54c58d69ba3374e619ac9bb873087dc243e122ee11db0f8f6a5b3972ed2), `CASCADE_MAP_R6.json` (cd903ade…), and the folders `specs/`, `gates/`, `out/` and `module/`.
- It has **no BUILD.md, no HASHES manifest and no build record.** Every file's mtime is 16:08–16:16Z.
- This matches A83, "stopped at its BUILD", and A89: r6 is adopted only if it causes no seal delay. If V007 seals on r5, r6 may serve steps 4–5 later, after its own identity gates.
- So **no dry plan was run under r6.**

**The ready-to-run r6 dry plan.** The pieces are:
- the runner `tools/run_r6_dryplans_c4v002.zsh`;
- the per-spec tool `tools/dryplan_one_r6_c4v001.py`;
- the diff `tools/diff_r6_r5_c4v002.py`.

**What it does once the BUILD lands:**
1. It refuses unless `driver_r6/BUILD.md` and a `driver_r6/HASHES*.txt` both name the r6 driver sha in full, and the driver bytes hash to that sha.
2. It dry-plans every r5-driver step-4 spec under r6, each in its own fenced process, in two variants:
   - (a) the spec as-is;
   - (b) the R6TC variant, which is the spec plus `numerics.uv_tail.table_cache` set to root's registered calibration cache block (A72, A81 RI-24).
3. It diffs every plan against its r5 plan, applying the r6 declared cascade map. The expected results are:
   - (a) `IDENTICAL_UNDER_MAP`;
   - (b) `ONLY_A72_CACHE_FIELDS`, meaning cache mode and directory, plus the label and call-spec pins.

**Evidence that the tooling behaves (TESTED):**
- **Real-mode attempt.** The runner printed `DEFERRED: r6 BUILD not landed …` and exited 2 (`r6_prep_v001/REAL_MODE_ATTEMPT_V002_STDOUT.txt`). The per-spec tool wrote verdict `DEFERRED_R6_BUILD_NOT_LANDED` and exited 2 (`r6_prep_v001/deferred_probe/`).
- **Stand-in self-test on the r5 driver** (not an r6 plan; diff in identity mode):
  - all 32 r5-driver specs read `plain:IDENTICAL_UNDER_MAP`;
  - all 30 R6TC variants are refused by r5 with `UV_TAIL_CONFIG_INVALID uv_tail keys must be exactly [...] got [... 'table_cache']`. So an A72 cache spec cannot run on r5.
- **Negative control.** A record of HEADLINE_TRIAL put in place of TAIL_REANCHOR reads 3 unexpected leaves. A record of SENS DHI put in place of SENS DLO reads 86. Either way the diff refuses (`r6_prep_v001/negctl_v001/`).

## 4. Spec list (my own derivation from v006r9, its config and generators)

**TAIL_REANCHOR (1)** (core L84–103 and L149–157; 0557 N-1)
- **Spec:** the registered A2F10 template physical with the config `numerics.block`, fresh, at D = 4.04.
- **Cross-check (TESTED):** equal to Codex2's r9 `ANCHOR_SPEC.json` except the label.
- **Spec sha:** 5fc6f0bd…

**WORKERS_8 (1)** (core L129–191)
- **Spec:** the candidate at the anchor point. No registered spec exists.
- **Spec sha:** 686ad07f…

**HEADLINE_CORNER (9)** (v005 `probe_points` L2041–2053 and `capability_probe` L2055–2113)
- **Spec:** `trial` plus the 2³ corners at D = 4.04, built by `ctx.mapper.build`. These are the exact launch bytes, with slots still pending.
- **Cross-check (TESTED):** the 8 corners equal the v006r7 `dryplans_v001` HEADLINE specs except the label, and the `trial` physical equals the registered anchor exactly.
- **Spec shas:** trial c5ede3c7…; 000 f3c72d95…; 100 28011f30…; 010 77c54de5…; 110 ef8b7d4c…; 001 850c8e22…; 101 478ae40f…; 011 4c8bb2bc…; 111 36e0ffdb…

**SENS_CORNER (16)** (0533 B4-1; static check L27–32)
- **Spec:** the template plus the block, with s, γ/E_ref and ℓ_F at the box corners and D at the box edges 3.9810717055349722 and 4.111497211045223.
- **Cross-check (TESTED):** each equals the v006r7 SENSITIVITY spec except the label, and their D hex values equal the pair-plan keys.
- **Spec shas:** listed in `specs_v001/SPEC_INVENTORY_C4V001.json`.

**SENS_DISTANCE (2)** (static check L33–34)
- **Spec:** the anchor template at D lower and D upper.
- **Cross-check (TESTED):** equal to the v006r7 DISTANCE specs except the label.
- **Spec shas:** e020397c… and 49bce3b5…

**CAMPAIGN_W1 (1)** (v005 Context L1786–1788; plan_only)
- **Spec:** the engine seed call, mapper-built.
- **Cross-check (TESTED):** the orchestrator's own `plan` gives a next wave of exactly this one call, with sha 3958aed3…, equal to `ctx.seed_spec_sha256`. Its physical differs from the anchor at about 1e-15 relative, the log/exp seed.
- **Spec sha:** 3958aed31353…

**DECIDING_III (4 runs, 2 spec files)** (pair plan cb42a5a3, 0540 F3)
- **Spec:** the registered tail-OFF calls, HIGH cf3f0086… and LOW 3f8a4c04…. Each file is the same bytes for both drivers.
- **Cross-check (TESTED):** the plans equal Codex2's r7 `sensitivity_tests_v001` dry plans, with 0 differing leaves.
- **Spec shas:** cf3f0086… and 3f8a4c04…

`specs_v001/specs/` holds every generated spec (exclusive create). The inventory is `specs_v001/SPEC_INVENTORY_C4V001.json` (362bb571…).

## 5. Blocker classification (per spec)

| Code | Class | Specs | On launch path? | Filled by / owner |
|---|---|---|---|---|
| PENDING_UV_TAIL_CERTIFICATE (driver run mode BLOCKED) | **V007_ADOPTION_PIN** | 30 tail-ON | yes | See below the table. |
| CERTIFICATE_POLICY_PENDING | OTHER_ROOT_ITEM | 30 tail-ON | See the second note below the table. | Root registers the registry, the policy review and the approved producers (TYPED_BLOCKERS r9: POINT_CERTIFICATE_SCIENTIFIC_APPROVAL_PENDING). |
| CONFIG_ANCHOR_TAIL_REANCHOR_PENDING | OTHER_ROOT_ITEM | TAIL_REANCHOR | no (post-run) | Root writes the result, receipt and spec sha into a new config version. |
| WORKERS_8_SPEC_NOT_REGISTERED | OTHER_ROOT_ITEM | WORKERS_8 | yes (pre-launch choice) | Root picks the run. Recommendation: a headline corner run (FORMAL, core L129–191), which needs no extra launch. |
| CAPABILITY_EVIDENCE_PENDING | OTHER_ROOT_ITEM | 9 headline | no (post-run) | Root registers the A32 run-mode box evidence from the 9 runs. |
| SENSITIVITY_DECIDING_III_REQUIRED (`prelaunch_check` refuses, TESTED) | OTHER_ROOT_ITEM | 18 SENS | yes | Per D: the pair runs, then checker evidence, a distinct review sha registered in a sensitivity-policy successor, and an A68-reviewed comparator successor. |
| COMPARATOR_A68_SUCCESSOR_REQUIRED (`compute_pair` refuses before any run read, TESTED) | OTHER_ROOT_ITEM | 4 deciding-(iii) | no (post-run evidence) | Same successor as above. The pair runs plan with zero blockers. |

**How the V007 adoption fills PENDING_UV_TAIL_CERTIFICATE (TESTED):**
1. The r9 block equals the C4T TEMPLATE numerics exactly. It differs from the C4T FILLED numerics only in `eps_certificate` and `lo_certificate`.
2. The adoption check requires block == adopted C4T numerics (adoption_policy L102–103; adoption_world S4). So adoption fills the block's slots with the sealed C4T slots: today EPS_CERT_V006 and LO_CERT_V004_MS128.
3. Every spec inherits them. After the fill, 30 of 30 specs normalize with 0 pending (post_adoption_probe).
4. FILL_PROBE dry plans with these pins have zero blockers on 30 of 30 specs.

**Where CERTIFICATE_POLICY_PENDING sits on each launch path:**
- **TAIL_REANCHOR and WORKERS_8:** not on the launch path, because `check_deciding` ignores the slots (r9 review N-1).
- **The 9 headline runs:** a pre-launch decision. Registry slots replace the slots in the mapper bytes that capability evidence binds.
- **CAMPAIGN_W1:** a campaign gate.
- **SENS:** scientific, because an anchor certificate pass is not a box pass (CERTIFICATE_ANALYSIS_CX2V001).

**Campaign-level gates.** This is the orchestrator's own `plan`, TESTED: status OK, next wave 1 call, `gates_ok` false.

| Gate | Reason now | Class |
|---|---|---|
| numerics_verdict | V007_SEALED_ADOPT_TAIL_PENDING | **V007_ADOPTION_PIN**. The V007 record must supply `verdict_artifact`, `block_source`, `compare`, `sealed_prereg` and `adopted_result`, and the block slots take the sealed C4T slots. |
| numerics_verdict, seal allowlist | `APPROVED_V007_SEALS = frozenset()` | The tuple is a **V007_ADOPTION_PIN**: compare sha, sealed prereg sha, frozen addendum sha, report schema, report sha. **But the fill mechanism is an OTHER_ROOT_ITEM.** The tuple can only enter through an immutable reviewed policy successor, which forces a new core (it pins the policy by sha) and a new orchestrator (it pins the core). That is a reviewed v006r10 cascade **after** the seal. adoption_world S1 refuses only on this; S2 passes with the tuple in an in-memory allowlist (TESTED on look-alikes). |
| adoption_regeneration | ADOPTION_DERIVATION_NOT_PINNED | OTHER_ROOT_ITEM (root writes the C4-6 derivation). Its V007-fed fields are V007 pins: verdict, compare and prereg shas, the C4T case and spec, and the C4T receipts. The rest are root items: base and seed spec shas from the **post-adoption** config, capability evidence, timing model, caps above measured use, disk guard, certificate registry. |
| deciding_test | evidence pending | OTHER_ROOT_ITEM. Register the rows `reanchor` and `workers_8` after their runs. |
| driver_capability | A32 run-mode box evidence pending | OTHER_ROOT_ITEM (the 9 headline runs) |
| certificate_policy | CERTIFICATE_POLICY_PENDING | OTHER_ROOT_ITEM |
| u_i_carrier | U_I_CARRIER_ROOT_TO_SET | OTHER_ROOT_ITEM (root signs `declared_by` and `basis`) |

**The adoption world** (TESTED, look-alike V007 records, the real policy bytes and the real C4T FILLED as `block_source`):

| Scenario | Result |
|---|---|
| S1: every V007 input supplied | refuses only on `V007_SEAL_NOT_IN_REVIEWED_ALLOWLIST` |
| S2: tuple allowlisted | ok |
| S3: prereg without `binding_inputs.case_block` | `V007_CASE_BLOCK_NOT_BOUND_BY_SEALED_PREREG` |
| S4: block slots still PENDING | `V007_BLOCK_DIFFERS_FROM_ADOPTED_C4T` |
| S5: deciding (ii) not verified | `V007_ROUTE_A_WORKERS_NOT_DECIDING_VERIFIED`. The deciding rows must be registered first. |
| S6: r6-driver C4T | `V007_C4T_DRIVER_OR_TAIL_MISMATCH` and `V007_C4T_SPEC_OR_DRIVER_NOT_BOUND` |
| S7: a None row in the carried uncertainty | `V007_CARRIED_UNCERTAINTY_REQUIRED`. Compare r11 L4781 can emit None rows; that this happens on an ADOPT_TAIL report is UNTESTED. |

## 6. Cross-lane findings (not step-4 code; they gate step 4 through V007)

**1. DEFECT: V007_PREREG_BINDING_INPUTS_CASE_BLOCK_ABSENT.** This is FORMAL from bytes, with its consequence TESTED on look-alikes.

What the bytes show:
- In sealed mode, compare r11 (L5689–5697) and r12 (L5692–5700) take the case block **only** from `prereg.binding_inputs.case_block`. Otherwise they refuse `CASE_BLOCK_ABSENT` in every mode, including `--gates-only` and `--validity-only`.
- Prereg r4's `binding_inputs` keys are: c5h_spec, gate_b3_final, identity_specs, qinf_evaluator, review_v009_orig, ro1_role_table, ro1_role_table_r5_pins, spec_set, successors, v006_r1_sealed. There is no `case_block`.
- SEAL_CHECKLIST_R4 B4 fills only `seal_slots`.
- No production V007 case-block file (schema `UNT_KMAX_TAIL_V007_CASE_BLOCK_C2V003`) exists in `v007_launch_packet_cx1/`, `v007_final_prereg_c4/` or `driver_r5/`. The only ones found are review fixtures.
- The calibration adoption policy reads the same binding (S3).

**Unless the sealed prereg carries `binding_inputs.case_block`, the sealed compare cannot read ADOPT_TAIL and step 4 can never be admitted.** This matters directly for the 0602 seal rehearsal (prereg r4 is Claude4's object).

Reproduction:
- `python3 -I -B -c "import json;print(sorted(json.load(open('<prereg r4>'))['binding_inputs']))"`
- `sed -n 5685,5700p <compare r11>`
- `adoption_world_v001/ADOPTION_WORLD_C4V001.json` S3.

**2. OTHER_ROOT_ITEM, conditional on A72/A89 choosing r6: ORCHESTRATOR_V006R9_R5_ONLY.**

v006r9 hard-requires r5 (FORMAL: core DRIVER_SHA; wrapper L47–48). An r6-sealed V007 would fail three ways:
- The adoption refuses (S6, TESTED).
- r5 refuses `uv_tail.table_cache` (TESTED, 30 of 30 R6TC variants).
- Exact block equality would carry the cache field into the calibration block.

What is needed is an orchestrator successor retargeted to r6, a registered calibration cache rule (RI-24) and its review. Under A89's no-delay rule V007 most likely seals on r5, and then this item is moot for step 4 unless root later rules r6 for steps 4–5.

## 7. Cross-checks (TESTED)

- **Codex2's static/dry check.** It was run as a path-only fenced copy (`tools/check_static_dry_cx2v006r9_C4PATHCOPY.py`, efc4c7ff…; exactly 4 path replacements plus a fence prologue).
  - It gives 131 of 131, the same check names and verdicts as Codex2's saved result.
  - `ANCHOR_SPEC.json` is byte-identical.
  - The anchor dry report is identical apart from `/call_spec`, the spec file path.
- **Codex2's earlier plans.** Against the v006r7 `dryplans_v001` reports (26 specs) and the r9 ANCHOR_DRY report, my plans differ only in `/call_spec`, `/call_spec_sha256` and `/normalized_spec/label`, using the derived-digest rule.
- **Deciding-(iii) plans.** All 4 match the v006r7 `sensitivity_tests_v001` plans with 0 differing leaves.
- **TAIL_REANCHOR against HEADLINE_TRIAL.** Their driver plans differ only in `call_spec`, `call_spec_sha256` and the label (negative-control record).

## 8. Observations for parts 1, 3 and 4 (FORMAL from code; not tested against real results)

- **One run can be both TAIL_REANCHOR and the capability `trial` probe.**
  - Facts: the `trial` probe point's physical is bitwise the registered anchor (TESTED), and the two plans differ only in the label (TESTED).
  - `check_deciding` needs the reanchor row's physical and coefficients equal to the registration, a fresh call, config numerics apart from the slots, and the spec sha pinned in `config.anchor`.
  - `capability_probe` needs the mapper-built spec sha.
  - So root can launch the **mapper-built trial bytes** as TAIL_REANCHOR and set `config.anchor.spec_sha256` to them. One run then serves both purposes.
  - 0557 N-1 is respected, because these are the template's physical values; only the label differs.
- **`workers_8` can be any one of the 8 headline corner runs.** It needs a distinct result, DDO154 at D = 4.04, a fresh call, config numerics, and normalized workers = 8. So the deciding rows need **no** run beyond the 9 probe runs.
- **The 4 deciding-(iii) runs depend on nothing from V007.** They are tail-OFF, run on r5 and v009-GEO, and plan with zero blockers. They can launch before the seal, CPU permitting. Only their evidence step waits on the A68 successor.
- **The spec bytes change after adoption.** For example, TAIL_REANCHOR 924851c4…, HEADLINE_TRIAL 7d9a8d47… and the seed 854e1291… (`post_adoption_probe_v001/`). These are PROVISIONAL: they hold only if the sealed C4T slots are exactly the A70 records and no per-point registry overrides them.
  - The C4-6 adoption derivation's `seed_spec_sha256` and `base_spec_sha256` must come from the post-adoption config.
  - The capability evidence must bind the post-adoption mapper bytes.
- **Config caps are as shipped:** per call 28,800 s wall, 64 GiB RSS, 12 GiB output; disk guard 12 GiB per call with a 20 GiB reserve. `production_caps_status` reads UNTESTED_REGENERATE_FROM_TAIL_TIMING. No wall-time figure is claimed here.

## 9. Harness issues (all fixed) and disclosures

- **H1.** fence v001 refused the r5 driver's own code file `…/uvt_route_b_binding_c2v001_r5.py`, because its rule was a casefolded `uvt_` prefix (`probe_v001/`).
  - fence v002 admits only a lowercase last-component `uvt_*.py` code file outside runs_ext.
  - It is also stricter than v001: casefolded runs_ext matching, plus refusing `listdir`/`scandir`/`glob` on runs_ext, `UVT_*` and C5H.
  - Its selftest passes 15 of 15. No runs_ext read is relaxed.
- **H2.** diff v001 had no derived-digest rule. Per-call files under the report dir embed that directory, so their digests differ between runs. The result was 32 of 32 false UNEXPECTED on the stand-in. diff v002 fixes this (32 of 32 identical) and passes the negative control.
- **H3.** The per-spec tool first typed PENDING_UV_TAIL_CERTIFICATE as OTHER_ROOT_ITEM. The final class, V007_ADOPTION_PIN, is set in the aggregator after the TESTED block-versus-C4T comparison. Both values are kept in each record, as `class_in_tool_record` and `class`.
- **H4.** The first probe run died on a `__file__` NameError before it produced any record.
- **Harness adaptation (as in Codex2's check).** Each orchestrator Context uses a local config copy whose `work_dir` is an uncreated directory here, with volume null. Only `work_dir`, `work_dir_identity` and `work_dir_volume` change; `cache_id`, the base spec and every spec are unaffected.
  - `platform.platform` is replaced with a static string so that no `uname` subprocess is spawned.
  - The disk forecast in my plan therefore reads the internal volume, not External1.
- **Disclosure: the interpreter.** Early read-only JSON inspections and three small in-folder file patches used `/usr/bin/python3` (Xcode 3.9.6) instead of the pinned runtime. No driver or orchestrator was imported in those. Everything that imports a driver or the orchestrator used the pinned runtime with `-I -B` under the fence.
- **Disclosure: reads outside the code.** Context construction opens the DDO154 calibration observation region (`CODEX1/DDO154_CALIBRATION_OBSERVATION_REGION_V001.json`), as Codex2's checks do. The r5 dry run reads the M_T monitor pin `CLAUDE2/runs/A2_ANCHOR_F10_RUN_V001/result.json` (v_ref speeds of a forward-model output). Both are logged per record. Neither is runs_ext, `UVT_*`, C5H or an NGC3198 target.

## 10. UNTESTED

- Scientific validity of any certificate.
- Real deciding, capability or adoption evidence. Every adoption test here uses look-alikes.
- Run-mode behaviour beyond the planning simulation.
- Any r6 plan (deferred).
- Whether root accepts reusing the trial or corner runs for the deciding rows.
- Wall time.

## 11. Reproduce (every command fenced, from this folder)

Set the environment for every command:
`OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1`

Use this interpreter as `PY`:
`/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -I -B`

1. Specs: `PY tools/make_step4_specs_c4v001.py <new dir>`
2. Jobs: `PY tools/list_jobs_c4v001.py specs_v001/SPEC_INVENTORY_C4V001.json <jobs.txt> r5,v009geo`, then `zsh tools/run_dryplans_c4v001.zsh <jobs.txt> <new root> <log>`. Each job is one process of `tools/dryplan_one_c4v001.py`.
3. Orchestrator plan: `PY tools/orch_plan_c4v001.py <new dir>`
4. Codex2 static copy: `PY tools/make_static_copy_c4v001.py <py> <dir>`, then run that copy.
5. Probes: `PY tools/post_adoption_probe_c4v001.py <dir>` and `PY tools/adoption_world_c4v001.py <dir>`
6. r6, after its BUILD lands: `zsh tools/run_r6_dryplans_c4v002.zsh <r6 sha> <cache block json> <its sha> <driver_r6/CASCADE_MAP from the BUILD> <its sha> <new root>`
7. Aggregate: `PY tools/aggregate_c4v002.py <out json>`

## 12. Files

**Records:**
- `DRYPLANS_C4V002.json` (record of record);
- `DRYPLANS_C4V001.json` (superseded only for the r6 runner pointer);
- this file;
- `HASHES.txt` (sha256 of every file in this folder except itself);
- `PARTIAL.md`.

**Run folders:**
- `specs_v001/`
- `r5_run_v001/`, with 34 records and `RUN_LOG.txt`
- `orch_plan_v001/`
- `static_copy_v001/`
- `post_adoption_probe_v001/`
- `adoption_world_v001/`
- `r6_prep_v001/`
- `probe_v001/` and `probe_v002/`
- `aggregate_test_v001/`, with the aggregator's test outputs (not records)
- `tools/`
