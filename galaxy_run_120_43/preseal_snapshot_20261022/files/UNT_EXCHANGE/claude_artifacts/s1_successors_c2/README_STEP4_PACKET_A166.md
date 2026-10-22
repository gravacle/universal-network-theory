# Step-4 packet A166 set (V006 A172): guard014, launcher015, S1 path lib c2v002b, DBP C2V004B

Written 2026-10-19T20:27:03Z (date -u). Claude2 root workflow item, V006 A172 "Commissioned: the step-4 packet A166 set".
Built only; nothing launched, nothing in force until root rules and Claude4 reviews. Every sha256 below is from bytes;
the full list is HASHES_G14.txt.

Bases (verified from bytes before the build): guard013 `593bebb6`, launcher014 `5d6af4a7`, lib c2v002a `f961839b`,
test_step4_guard_c2v013 `30324d80`, K=3 wrapper `e7f52461` (unchanged, still pinned by the lib), DBP C2V004 `7c3ceae5`.

## 1. step4_guard_c2v014.py `6efdca016416a919b25a1e23d46a415b75fe2b5e60145ba098f864730975165d`

guard013 with one change: the route-A rule binds only its non-memory fields.

- **Removed** (guard013 L372-373): `minimum_free_percent == 25`, `source == '/usr/bin/memory_pressure'`,
  `first_case_memory_exemption is False` (code FIRST_MEMORY_BYPASS_REFUSED is gone).
- **Kept** (guard014 L372-376): `max_active` integer 1..6 (ROUTE_A_CAP_REQUIRED), plan rule == root's rule
  (ROOT_RAMP_APPROVAL_REQUIRED), `poll_seconds == 60` and `ramp == previous_first_completed_route_a_iteration`
  (RAMP_RULE_REQUIRED).
- **poll_seconds is kept** because it is not memory-motivated. The packet interface (IMPLEMENTATION_INTERFACE_CX1V003.md
  L36) gives it as "one start per 60-second poll", and launcher015 L133 `time.sleep(60)` is the start and ramp cadence.
  The plan field is not read by the launcher; the guard binds the declared value to that constant.
- **Added** (L325-326, L376): `MEMORY_ADMISSION_FIELDS`. A rule that still carries any memory field is refused with
  MEMORY_ADMISSION_FIELD_REFUSED.
  - **Design: refuse, do not ignore.** launcher015 enforces no memory term, so a plan of record that states a 25 % ramp
    would misstate the start rule. A172 says the DBP drops the fields "as guard014 requires".
  - A C2V004-built plan or admission, including one from templates_v004, cannot be reused silently. It is refused
    (TESTED: G14-F25).
- **Unchanged**: every custody check, including core_priority_admission (guard013's, byte-identical), every refusal on
  every non-memory variant (TESTED: G14-P3, 26 variants, 19 refusing; G14-P6, 14 custody variants), and AST-identical
  top-level definitions except validate (G14-P0). guard013 checks no nice level, so there was nothing to drop.

## 2. step4_launcher_c2v015.py `cd987edd097323999847208d7b5fdfd93dadecb8a10beb6feaf91a0c53b68e0b`

launcher014 with its memory terms removed.

- **Removed**:
  - `memory_free` (launcher014 L31-36);
  - its call (L123);
  - the free term in `decision` (L37-38; now L32-33);
  - `free_percent` in the admission log (L125; now L118);
  - the NICE_10_REQUIRED line in runtime_settings (L47);
  - the now-unused `re` import (L4).
- **Re-pinned**: guard014, path and sha (L8-9).
- **Kept**:
  - max_active (`decision`);
  - the first-iteration ramp (L114) and the PREDECESSOR_ENDED_BEFORE_FIRST_ITERATION fail-fast (L119);
  - single-thread BLAS (runtime_settings L41-42; the BLAS env passed to the worker and monitor);
  - normal QoS (normal_qos), caffeinate (worker assertion and per-monitor);
  - the machine lock (launcher012's file);
  - the caps passed to the monitor (monitor_argv), drain-on-failure and `systemic`;
  - main, which is unchanged.
- **Diff scope (TESTED, L15-P1):** exactly 17 lines removed and 10 added. decision, memory_free, runtime_settings and
  worker are the only definitions that differ.

## 3. s1_path_lib_c2v002b.py `65d69cf48235cee25dbcab671d1f97bf393fa991338b5c249e7313f15b7576d4`

lib c2v002a, re-pinned to guard014 / launcher015 (closes E_A170_1).

- **Re-pinned** (PINS L74-75). The refusal is now S1_PACKET_NOT_GUARD014_LAUNCHER015 (L1144).
- **Removed** (v002a L1154-1210 and their helpers):
  - load_gate and the GATE pin;
  - the injected gate, `gkw`, `_overlap_gate` and `_overlap_sleep`;
  - the GUARD012_OVERLAP_GATE stage;
  - hold_check, the warm-up and decide;
  - the r5 route-A allowance against the gate cap;
  - the A133 rule and its constants;
  - memory_pressure (MEMORY_FREE_MIN_PERCENT, `_memory_free_percent`, MEMORY_PRESSURE_FREE_BELOW_25, the `memory_free`
    argument);
  - the `sleep` argument;
  - `/usr/bin/nice -n 10` in the launch argv (L1227-1228).
- **Kept: S1_CAMPAIGN_ROUTE_A_TREE_WHILE_ATTESTED_INACTIVE** (v002a L1198). It is now a process-table check (L1219-1224).
  - With the campaign attested INACTIVE, `_process_table` (L1040) runs `/bin/ps -ww -A -o pid=,command=`.
  - campaign_route_a_trees (L1075) keeps every root-monitor tree that matches all of:
    - its command line matches `root_monitor_c2v\d+\.py` and carries `--driver` (gate v003 L136 and L450);
    - its driver is r5, or its `--driver-sha256` cannot be parsed (fail closed);
    - its outdir is not this call's;
    - it is still in route A by route_a_done (gate v003 L392-410) on `<outdir>/progress.jsonl`. An unparsed outdir or
      an unreadable progress file counts as route A.
  - Any such tree refuses. A ps failure refuses with PROCESS_TABLE_UNREADABLE (stage CAMPAIGN_INACTIVE_CHECK).
  - Under ACTIVE (overlap) nothing is read. Only the gate allowance applied there, and it is removed.
  - Injecting `process_table` is a dry-mode seam only. Launch mode refuses it (LAUNCH_MODE_INJECTION_REFUSED, note 7).
- **Disclosed differences from the gate path. The membership is the same on well-formed logs.**
  - Phase is read only for r5 or unparsed trees. The gate read it for every tree, and only these trees decide.
  - A non-object JSON line in progress.jsonl is skipped. Gate v003 raised AttributeError there, so v002a refused with
    INTERNAL_ERROR.
  - The progress read has no lexical protected-path guard, as in the gate.
- **Record**: the decision record's `gate` entry is replaced by `campaign_route_a_trees`. The schema id is unchanged.
  `evaluated` text and docstrings now describe guard014 / launcher015.
- **Nothing else changes (TESTED, L-P0).**
  - Against v002a, every named top-level statement is AST-identical except MODULE, PINS and launch.
  - Removed and added are exactly the lists above.
  - PINS differ only in GUARD, LAUNCHER and the removed GATE. The imports are identical.

## 4. sched_s45_c2/v004b/DIRECT_BATCH_PARAMS_S45_C2V004B.json `e239d21e8f29e4711ec20c28c335bc25340fb8780253ceb1e57f037624e99205`

C2V004 with these changes (33 changed leaves; LEAF_DIFF_S45_C2V004B.json `6101382e`):

- each batch's route_a_admission is exactly {max_active, poll_seconds 60, ramp} (15 memory leaves dropped);
- DIII max_active is 4, its call count, with its max_active_basis.rule;
- packet_read names guard014 / launcher015 (the binder entry is unchanged; see R1);
- the texts are updated: scope, basis.max_active, packet_memory_check, still_root_rulings, supersedes, schema;
- note_a172 is added.

Every rss_cap_bytes is RAM 137438953472, and caps_per_case is unchanged (asserted). The other max_active values are
HEADLINE / SENS_LO / SENS_HI 3 and POST_S1 2. Every batch rule is admitted by guard014 and refused by guard013
(RAMP_RULE_REQUIRED) (TESTED, G14-P9).

The builder is `build_params_s45_c2v004b.py` `90c4a5d5`. It pins C2V004, guard014 and launcher015, and reads
MEMORY_ADMISSION_FIELDS and the line numbers from guard014's bytes.

## Tests (synthetic; scratch run dirs; no process started, no target read)

| Suite | Runs | Result |
|---|---|---|
| test_step4_guard_c2v014.py | test_runs/G14_RUN1, G14_RUN2 | 36/36 each (16 MUST_PASS, 20 MUST_FAIL); TEST_LOG identical |
| test_s1_path_c2v002b.py | test_runs/S1B_RUN1, S1B_RUN2 | 143/143 each (30 MUST_PASS, 113 MUST_FAIL) |

**test_step4_guard_c2v014.py**

- **Ported from guard013's 27:** every guard and launcher test that applies, retargeted to guard014 / launcher015.
  P3 and P6 now compare against guard013, and P5 shows guard013's memory refusals admitted by guard014.
- **New:**
  - G14-P8: HEADLINE with no memory fields is admitted.
  - G14-P9: the C2V004B rules.
  - G14-F25: free 25 is refused, and each memory field alone is refused.
  - L15-P3: memory_pressure unreadable.
    - launcher015 starts the first call. The audit hook records zero process creations, and no memory request is made.
    - Control: launcher014 asks for memory_pressure at every poll. The hook blocks each request, so it is never
      executed. It reads None and starts nothing.
  - L15-P4: the ramp waits for the predecessor's first iteration.
  - L15-F2: PREDECESSOR_ENDED_BEFORE_FIRST_ITERATION still fails fast.
  - L15-F3: max_active binds.
  - L15-P5: launcher014 and launcher015 behave identically on 8 non-memory worker scenarios (ramp, cap, predecessor
    ended, systemic receipt, disk start bound, admission revoked, signal drain, retained scientific failure).
  - L15-P6: runtime_settings without nice, read through an os proxy.
- **Harness seams:**
  - G.validate and G.disk_admission are stubbed (the real disk check stats External1).
  - The lock is a scratch file.
  - subprocess and time are shims.
  - An audit hook blocks every real process creation.

**test_s1_path_c2v002b.py**

- **Ported:** all v002a tests that apply, with their ids and codes. Plans come from make_plan on DBP C2V004B.
- **Converted:** the gate and memory MUST_FAILs L-F16, L-F18, L-F19, L-F28 and L-F30 become L-P6, which shows each of
  their inputs is now admitted. L-F17 becomes PROCESS_TABLE_UNREADABLE.
- **New:**
  - L-P0: diff scope.
  - L-P7: tree classification.
  - L-P8: dry mode admits INACTIVE and overlap plans on guard014 / launcher015. The audit hook shows gate v003 never
    opened, no process and no memory_pressure.
  - L-P9: the reader's argv (`subprocess.run` is a recording fake).
  - L-F37: fail-closed tree variants.
  - L-F38: guard013 / launcher014 and guard012 / launcher013 plans are refused.
- **Not ported:** W-P1, W-P2 and W-F1 to W-F5. They run the c2v002a CLI wrappers, which pin lib c2v002a (see R2).

**UNTESTED (deciding test named):**

- The live /bin/ps read on this machine. By rule, the tests never read the process table. Deciding test: one root dry
  run of the launch path with the campaign INACTIVE.
- A real launcher015 run with real monitors, as for every earlier launcher. Deciding test: the first batch.

## Root must rule

- **R1 Binder.** packet_read.binder `step4_bind_c2v010` (`4d07dca3`) still loads guard011.
  - It refuses any plan naming guard014 (LAUNCHER_GUARD_IDENTITY), and its command adds `nice -n 10`.
  - A direct batch on guard014 / launcher015 needs a binder successor that re-pins guard014 and drops nice. Not built:
    it is outside this item.
- **R2 CLI wrappers.** s1_launch_root, s1_fill and s1_read c2v002a pin lib `f961839b`, so lib c2v002b cannot be called
  from the CLI until c2v002b wrappers re-pin it. Not built.
- **R3 The lib's default DBP pin stays C2V003A** (`4adc296b`), as "no other change" requires.
  - make_plan without `--params` builds a plan that carries the memory fields and pre-A166 RSS caps. guard014 refuses
    that plan (fail closed).
  - Root passes `--params .../v004b/DIRECT_BATCH_PARAMS_S45_C2V004B.json@e239d21e...`, or rules a one-constant re-pin.
- **R4 Refuse versus ignore** for memory fields (section 1). Root confirms the refuse design. Plans and admissions from
  C2V004 or templates_v004 must take C2V004B's route_a_admission.
- **R5 Registration wording.** Registration C14 ("each S1 head passes the machine gate at its own start", quoted in
  make_plan's docstring, unchanged) now has no gate behind it. The campaign-window attestation and the INACTIVE
  process-table check remain.
- **R6 A140 N4.** A wall rebuild of C2V004 needs this A172 form re-derived from the new base. The builder pins
  `7c3ceae5`.
- **R7 sched v004a** (the max_concurrent 8 leaf, A172 "built first") is not part of this item and was not built here.
