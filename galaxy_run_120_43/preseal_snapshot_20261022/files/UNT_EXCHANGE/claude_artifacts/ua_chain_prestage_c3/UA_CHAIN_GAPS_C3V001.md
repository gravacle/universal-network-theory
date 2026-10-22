# UA_CHAIN_GAPS_C3V001: what root must still rule or supply, and every step that cannot be written from adopted sources

This file goes with `UA_CHAIN_RUNBOOK_C3V001.md` (RB) and `UA_CHAIN_XREF_C3V001.md`. Source keys are as in RB.

**Bottom line:**
- **S8's first compute can start within minutes of u_A** (RB S8-01 to S8-05) once G-01, G-02 and G-03 are closed.
- **The S1 pair cannot.** It needs the row-32 chain first: about 4–6 h at E (AUDIT L70), plus the EPS lane latency. Its middle steps (S8-08 to S8-13) have no command lines in the named sources (G-10, G-11, G-12).
- **S9 can start within minutes** only if three things are ready at u_A:
  - the Phase-1 PLAN commands (G-20);
  - the forecast and cw8 spec producers (G-23, G-24);
  - Lane E, done earlier.

## A. Root rulings needed (before W3 acceptance unless marked)

| # | Item | Why | RB block |
|---|---|---|---|
| G-01 | **Confirm procedure A (`4da9ddb5`) as the operative row-32 procedure, with the c2v002c CLI names.** Procedure A names the c2v002a CLIs. The A272 checklist says c2v002c was adopted (A186, cited at [SCAN] L789; A186 not read here), and S1PATH L79–85 says the c2v002c CLIs are the c2v002a code with only the library pin changed. RB substitutes `s1_fill_c2v002c.py` and marks it DERIVED. | No named source shows the procedure's own standing. | S8-02, S8-12 |
| G-02 | **Name the adopted row-32 KS3 runner (path and sha).** AUDIT L269 cites "the row-32 KS3 runner `54595c2d`". From bytes (TESTED, 2026-10-21), `54595c2d68e6…` is `ks_k3_chain_c2/cp1_runner_c3v004_ks3_c2v001.py`. The A272 checklist scanned `ks_k3_chain_c2/cp1_runner_c3v004_ks3_c2v002.py`, which is **`da08d725ecf6…`**. Two versions exist, and no source read here says which one root adopted. The KS READMEs in that folder (`README_KS_K3_CHAIN_C2V001.md`, `README_KS_K3_GWAVE_C2V001{,a,b}.md`, not opened) probably do. | The CP-1 row-32 run cannot be pinned. | P4, S8-04 to S8-07 |
| G-04 | **Name row 32's EPS signer lane.** A202 makes Codex3 a root-approved signer lane but assigns rows 10–31 (A202 L2601–2603). Procedure A names Claude4 (PROCA L83–84). Claude4 is the bottleneck after Fri 19:00Z (A201 L2573). | It sets `--approved-signer-lane`. | P1, S8-07 |
| G-08 | **The S1 native PRELAUNCH path (possible blocker).** The A272 checklist flags, as not verified ([SCAN] L789), that `step4_prelaunch_c2v005.py` (bytes `117b3520`) pins guard011 and refuses any non-guard011 plan, while s1 `make_plan` writes only guard014 plans and needs a prelaunch record. The pair needs a native PRELAUNCH record for each child (PAIR L22). Root confirms the producer and its command. | Without it, no child plan can be made, so there is no pair. | P2-B4, S8-13 |
| G-22 | **The P-112 config schema value:** `P112_CONFIG_CX2V004` or `P112_CONFIG_CX3CW8V001`. Both are accepted ([CW8C] L7; [CW8L] L829). | It is a scope-identifying field of the immutable config. | S9-02 |
| G-18 | **The P-112 run root.** `run_root` must be `<run_volume>/NGC_*` ([CW8L] L851–852). Whether it must exist beforehand is "not determined" in the A272 checklist ([SCAN] L789). Whether it may equal the S0 run root is not stated. This helper cannot test `/Volumes`. | The config cannot be finalized without it. | S9-02 |
| P1.2 | **The V006 write-freeze window.** Fix it so it does not cover the row-32 pin entry (S8-03), the single CW8_LICENSE_PIN entry (E-05) or the S9 SPEC_PIN entries (S9-03). Basis: A201 L2569; AUDIT L152 suggests outside u_A ± 1 d. | A collision stalls S8 or S9 (AUDIT L33, L250). | P1 |
| (N7) | **C4T's later batch, if C3T ends non-systemically before its first iteration** (A284 L4965). Rule its path: the old single-call wrapper with C4T's child plan, or a new pair. Its command is G-15. | It is a contingency on S8's path. | S8-21 |

## B. Values root must supply at run time (PASTE)

**Before u_A:**
- `PASTE_P112_LAUNCH_ROOT`, `PASTE_V006_COPY_DIR`, `PASTE_CUSTODY_DIR`, `PASTE_CAUSE_RECORD_DIR`;
- the S1 folders: `PASTE_S1_FILL_DIR`, `PASTE_S1_PLAN_DIR`, `PASTE_S1_PRELAUNCH_DIR`, `PASTE_S1_RECORD_DIR`, `PASTE_S1_READING_DIR` (P3);
- `PASTE_REGISTRATION_PIN` (the S1 registration, path@sha);
- `PASTE_C4T_C1` (the campaign b1 C1);
- `PASTE_KS3_RUNNER` (G-02);
- `PASTE_HOLD_FILE` (P4).

**At u_A, for S8:**

| Step | Values |
|---|---|
| S8-01, S8-02 | `PASTE_UA_POINT_FILE`/`_SHA`; `PASTE_UA_CALL_SPEC`/`_SHA` (the u_A call's spec); `PASTE_CAMPAIGN_CONFIG`/`_SHA` |
| S8-03, S8-05 | `PASTE_THETA16`, `PASTE_KEY16`, `PASTE_POINT_KEY`, `PASTE_SPEC_SHA`, `PASTE_THETA_KEY`, the snapshot path and sha |
| S8-03 | `PASTE_ROW32_FILE` and its sha |
| S8-07 | `PASTE_EPS_REVIEW`/`_SHA`, `PASTE_SIGNER_LANE` |
| S8-15 | the C3T and C4T bound child admissions (path@sha); `PASTE_PAIR_SOURCE_REVIEW_PIN`; the pair launcher log name, which must be absent |
| S8-17 onward | `PASTE_ADMISSION_SHA`, `PASTE_BOUND_PLAN_SHA` (from S8-15b's shasum) |
| S8-P1 | `PASTE_S1_LAUNCH_CONFIG`, path and sha |

**For S9:**
- `PASTE_RUN_VOLUME`, `PASTE_RUN_ROOT_NAME`;
- the 8 scope values from S9-01;
- `PASTE_P112_CONFIG`/`_SHA`;
- the per-call SPEC_PIN names, shas and paths;
- `PASTE_FORECAST`/`_SHA` (fresh, ≤ 900 s).

**For Lane E:**
- `PASTE_COMPARATOR_RECORD`/`_SHA`;
- the two seed SPEC_PIN objects, copied from V006;
- `PASTE_LICENSE_PATH`/`_SHA`;
- `PASTE_DATE_U` (from `date -u`).

## C. Steps that cannot be written from the adopted sources this helper was allowed to open

| # | Step | What is missing | Where it probably is (not opened) |
|---|---|---|---|
| G-03 | **The row-32 row file** (V006 L1754). | Its format; how the KS3 runner receives it (a CLI flag, or a fixed path); and whether the V006 entry has a machine-read grammar. Procedure A's `plan`/`run` lines (PROCA L62, L71–74) predate the row file and carry no row-file argument. RB gives a prose template only (DERIVED-TEMPLATE). | The KS3 runner and KS chain README; the V006 KS-chain entry around L1716–1772 (only L1751–1757 read) |
| G-05 | **Codex3's scripted E1–E10 EPS check at K=3.** | Rows 10–31 are K=4 [4,182]. Row 32 is K=3: 179 shells [3,182] and a 10-shell ρ partition (PROCA L35–36; A160 L1342). Whether Codex3's checker and review writer accept K=3 is unknown. | Codex3's lane files |
| G-06 | **The S1 C1 freeze tool.** | It binds A240/A268's ordered six by digest (A240 L4102; A268 L4623). It is **unbuilt** per the A272 checklist ([SCAN] L789). | to be commissioned |
| G-07 | **The source-closure delta** (A240 L4101). | Its status after A268. It is decided only by the real DRY (S8-18). | Codex1's 0794 deliverables |
| G-09 | **How the KS3 scheduler is detached.** | Procedure A gives the foreground form. The scheduler runs for 40–90 min plus the ρ stages (PROCA L102). | the CP-1 run sheet (`75481f2b` per AUDIT L401) |
| G-10 | **Row 32's middle steps.** | Commands for ρ registration (PROCA L85), the G1 LO slot proof (L86), KS4 `bundle`/`registry` (L87) and KS4 `verify` with the S1 C1 (L88). The checklist gives only their folders ([SCAN] L626–629, L850). | the KS4 successor README `ks_k3_chain_successor_cx1/README_CX1V002.md`; the G1 tool's CLI |
| G-11 | **The S1 `fill` command.** | PROCA L91 elides the arguments ("fill ... --c3t-registry … --out-dir …"). The A272 checklist quotes the same elided form with the c2v002c name ([SCAN] L758), which supports G-01's substitution. | `s1_fill_c2v002c.py` CLI; S1 README C2V001 |
| G-12 | **The child plans, PRELAUNCH and binds.** | The exact `plan` form, including `--params` for DBP C2V004D (S1PATH L84, L196 say `--params` exists) and `--overlap` (PROCA L92); the PRELAUNCH005 command (G-08); and binder011's `bind` CLI for the children. The pair README's bind flags (PAIR L39–44) belong to a binder whose `bind` is AST-identical to binder011's (PAIR L13), but binder011's own `main` was not read. The A272 checklist quotes partial forms with the c2v002c names ([SCAN] L766, L774): `s1_fill_c2v002c.py plan --out PATH` (+ `PATH.s1.json`); PRELAUNCH005 `--output-dir`; `step4_bind_c2v011.py --plan-out/--admission-out/--command-out`; `s1_launch_root_c2v002c.py --launch --confirm SHA --record PATH`. **Children planned from C2V004B or C2V004C fail S8-16.** | `s1_fill_c2v002c.py`/lib CLI; `step4_bind_c2v011.py` CLI; the verdict-day sheet (its L151–152 binder lines, per [SCAN] L860) |
| G-13 | **The S1 launch config's full key set.** | The wrapper checks only `schema`, `campaign_state` and `step2_route_a_state` ([WRAP] L33–36). The lib's `SCHEMA_LAUNCH_CFG` object may require more. | `s1_path_lib_c2v002c.py` |
| G-14 | **The envelope START and END for the S1 pair.** | The A226 item-3 envelope over both children (A284 N10). The tool command is not in the named sources. Whether the envelope tool follows nested pins is UNTESTED ([VRES] N10). | `pinned_input_envelope_c2v003` (0843 L26) |
| G-15 | **The A284 N7 later-batch C4T launch command.** | See section A. | the old wrapper `s1_launch_root_c2v002c.py` CLI |
| G-20 | **The Phase-1 PLAN 1a/1b at u_A.** | It produces the 8 cw8 scope fields of the config (`plan_output_primary`, `plan_build_record`, `selection`, `fdplan`, `spec_of_record`, `at0a_pass`, `members`, `f_points`, [CW8L] L2992–2993). Their value forms come from the P112 parent contract ([P112C] L25: "All parent config fields remain"). | `runbook_v002_c2v007_cx2/RUNBOOK_V002_C2V007.md`; `runbook_rulings_c2/P112_LAUNCHER_BRIEF_V005.md` ([SCAN] L369, L374) |
| G-21 | **The verbatim P112 workflow lines:** `launch --dry`, `launch`, `close-attempt`, `assemble-registry`. | CW8C L43 defers them to "the existing P112 workflow". RB gives the CLI shape only ([CW8L] L2505–2523) and writes no launch command. | the same two files |
| G-23 | **The `_FULL_CW8` fill specs.** | Their producer. The spec must differ from the serial only by `column_workers` 1→8 ([CW8C] L16). | step-5 fill tooling |
| G-24 | **The cw8 forecast.** | No producer is named. Its keys are in [CW8C] L29–35, and it must be 0–900 s old at selection. Root writes it by hand. | none named |
| G-25 | **The cw8 license object.** | No adopted producer. RB gives the exact 8-key template (E-02). | none named |
| G-26 | **There is no non-committing license authentication.** | `cw8_authenticate` runs only inside `select-workers`, an admission decision. Any defect there durably selects serial ([CW8L] L3383–3400; `status` does not authenticate, L1787–1812). RB E-01, E-04 and E-06 are read-only pre-checks. A dry-authenticate helper would need a build and a review. | none |

## D. Hazards noticed (no ruling asked unless marked)

1. **V006 pin-grammar collisions.**
   - `cw8_root_license_pin` counts every V006 line that **starts** with `CW8_LICENSE_PIN`, even inside a code fence ([CW8L] L3009–3018).
   - The tool gate counts every line starting `TOOL_PIN P112_LAUNCHER_CX3CW8V003` (L364–385).
   - A quoted template in any V006 entry this helper did not read, A283–A290 and later included, would break selection (DUPLICATE → serial) or the gate (every launcher command refuses).
   - E-04 and the S9-03 count detect this. The row-32 entry template avoids these tokens at the start of any line.
2. **The license line must be bare.** It must not be a bullet or be indented, and it must have no trailing space.
   - A bulleted line is not seen at all: CW8_LICENSE_MISSING → serial.
   - A malformed line refuses: CW8_LICENSE_REGISTRATION_FORM → serial.
   - A non-A `## ` heading between the entry heading and the line also refuses ([CW8L] L3010–3016).
3. **The serial fallback is permanent per cohort.** select-workers before Lane E completes makes that cohort serial for good ([CW8C] L43, L55).
4. **The comparator record's location.** It must be outside both run roots and free of protected components (`ngc3198`, `stages`, `a_side`, …). Otherwise the launcher refuses to read it and selection falls to serial ([CW8L] L235–248).
5. **Walls.** The S1 children must be planned from DBP C2V004D (`5d3f4bb8`; A291 L5058). C2V004C stays the verdict-day object (A284 N8 L4967). S8-16 is the STOP check.
6. **Disk.** The pair batch needs both output caps plus 20 GiB free on External1 (PAIR L24). The review measured 193,273,528,320 B ([VRES] checked[4]). The guard checks this, and it is a refusal, not a crash.
7. **The campaign state.** The S8-P1 launch config attests the *current* campaign state, and the children's core-priority (overlap) must match it (PAIR L47; [WRAP] L40–41). If the campaign changes state between S8-13 and S8-20, the children must be re-planned.
8. **The binder's command file** (`S1_PAIR_EXECUTOR_COMMAND_V001.sh`) is never run (A284 N9). The pair wrapper is the only launch handoff.
9. **The dispatch's aim versus the physics of the chain.** "S8 and S9 start within minutes of u_A" holds for S8's row-32 CP-1 run, not for the S1 pair. The pair waits for the EPS review, ρ, slot, KS4, C1 freeze, fill, children and assembly. The wrapper itself returns within seconds of spawning the detached worker ([PLAUNCH] L158–160).
10. **The S1 C1 policy review (B1)** may bind content that exists only after row 32: the registry with row 32. If so, it cannot be fully pre-signed, and Codex3 should say what waits (AUDIT L126; A280 precedent).

## E. Scope disclosures (for the lead)

- **V006 was read by heading only:** A160, A201, A202, A240, A241, A268, A272, A274, A280, A281, A282, A284, A291.
  - The heading line numbers came from a grep for `^## ` that printed only line numbers for unlisted headings.
  - **Also read: V006 L1751–1757 only.** The dispatch names "the part at about L1754" as being inside A160. L1754 actually lies in the section that begins at L1716, not in A160 (L1323–1354). The narrow window was read because the dispatch names that line explicitly. Nothing else in that section was read. Lead: please confirm this was in scope.
- **Read beyond the dispatch's explicit file list, each by exact path:**

  | File | sha | How it was named | What was read |
  |---|---|---|---|
  | PROCA `s1_successors_c2/S1_C3T_CERT_EXTENSION_PROCEDURE_A.md` | `4da9ddb5` | the A272 checklist's S8 procedure-A source ([SCAN] L651 documents_scanned; findings L742–868) | all of it. It is the runbook for the row-32 CP-1 run and the S1 procedure-A steps the dispatch names |
  | P112C `phase1_ngc_launch_kit_cx2v004/README_CONTRACT_CX2V004_V001.md` | `78b77cbf` | the `P112_CONFIG_CX2V004` contract that CW8C L7 uses | 48 lines |
  | CW8P `cw8_phase1_cx3/CW8_SOURCE_PINS_CX3V001.json` | `3cd81174` | CW8C L65 | all of it |
  | `cp1_list_rho_slot_cx1/README_CX1V004.md` | `e0a9a874` | [SCAN] L226 documents_scanned | a grep for EPS-signing lines only. One header line matched, and it was not used |

- **Code read for CLI and schema only:**
  - the cw8 v003 launcher: CLI, config validation, license/forecast/lock/selection functions and path rules;
  - the pair wrapper v002: CLI and decision/record logic;
  - the pair launcher: `main` and the worker's admission and event lines;
  - the pair binder: `main` lines.
- **Listed, filtered to file names only:** `ks_k3_chain_c2/`, for `cp1_runner*` and `README*`, to find the KS3 runner behind G-02.
- **Hashed only, never opened:**
  - `ks_k3_chain_c2/{cp1_runner_c3v004_ks3_c2v001, cp1_runner_c3v004_ks3_c2v002, s4rc1_common_c3v004_ks3_c2v002, lo_slot_proof_c3v003_g1_c2v001, registry_assembler_c3v004_ks4_c2v002}.py`;
  - `ks_k3_chain_successor_cx1/{registry_assembler_ks4_cx1v002, s4rc1_common_ks3_cx1v002}.py`;
  - `step4_prelaunch_cx1/v005/step4_prelaunch_c2v005.py`;
  - the s1_successors_c2 CLIs, lib, guard014, launcher015 and binder011;
  - the DBP C2V004D instance.
- **Not opened:**
  - the dispatch's forbidden areas: `/Volumes`, run trees, run outputs, NGC3198 data, V007_POSTSEAL_RECORDS, `~/.codex`, C5H and UVT_* material;
  - V006 A290 and every unlisted V006 section.
- **Process deviation.** Three helper shell commands ran without the `taskpolicy -b` prefix. All were local writes or no-ops in this helper's own folders:
  - the heredoc `cat` that created RB;
  - a no-op `mkdir -p` of the scratch folder;
  - the `cat` that wrote the scratch verification script.
  
  Every other command carried the prefix.
