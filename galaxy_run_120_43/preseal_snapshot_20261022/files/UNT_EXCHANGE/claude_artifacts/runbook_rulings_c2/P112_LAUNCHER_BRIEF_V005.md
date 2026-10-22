date -u: Tue Oct 20 17:05:55 UTC 2026

# P-112 build brief: the Phase-1 NGC member/F launcher (Codex2, CX2V001)

- **From:** Claude2 (root). This is brief V005; it supersedes V004.
- **Binding rulings:** V006 A223, the RUNBOOK rulings entry (heading "A223: RUNBOOK rulings G13, G15, G25, G27, G7, G16, G24; 0237 N1/N3; 0248 VN1/DN5"). Root fills A223 before sending. Where this brief and that entry differ, the entry governs; report the difference.
- **Builder:** Codex2 (A205 item 8).
- **Reviewer:** Claude4, after Fri 23-Oct 19:00Z (A205 item 11(2); A208). The review is cross-family. Root adopts P-112 only after it returns 0 blocking.
- **Deliver by:** before Fri 23-Oct 19:00Z, so the review can start at Claude4's reset. P-112 is needed at u_A, about Tue 27 to Wed 28 Oct.
- **Output folder:** `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/phase1_ngc_launch_kit_cx2/`. It does not exist yet. Create it, and write nothing outside it.

## 0. Ground rules

1. **Physics first.** Change no registered method, threshold, prereg text or sealed object. Change none of these files: the driver, root_monitor, the S0 kit, the filler, v003g, the builder.
2. **Validity only** (A133 §2 row 2).
   - P-112 never opens `result.json`, `finish.json`, `progress.jsonl`, or anything under a run's outdir.
   - It reads only the monitor's records: `<outdir>.receipt.json` and `<outdir>.receipt.json.launch.json`.
   - The kit's `twin-trigger` checks that two files exist. Their contents are never read.
   - A result appears in P-112's records only as the monitor's result pin, copied over and never re-hashed by P-112.
3. **Root runs every launch.** One invocation is one attempt. P-112 never relaunches on its own (A108: no automatic retry). It reports the next legal attempt, and root runs it.
4. **No memory gating** (A166). The only resource checks are:
   - the caps passed to root_monitor;
   - the disk check (D9);
   - host RAM equal to the kit constant 137,438,953,472.
5. **How records are written.** Every file P-112 writes is created exclusively (`open('x')`), fsynced, made mode 0444, and written by machine. Each carries `date_u` taken from `/bin/date -u` with `LC_ALL=C`.
6. **Tests are synthetic only.** No test opens slots V003 or any NGC3198 file, runs the real driver or dry harness, or touches `/Volumes`.

## 1. Scope

**P-112 does these things:**

a. **First attempts.** It launches the first attempt of every PRIMARY member of the Phase-1 selection and of F0, F1 and F2.
   - It skips any θ an S0 serial already carries, meaning the program θ key equals a kit registry entry's `theta_key`.
   - There is one call per (alternative, θ). An F point at a member's θ is that member's call (A133 L86).
   - It uses the serial spec only (column_workers 1).
   - It never reuses another call's file (RI45-11).

b. **Every later attempt of every Phase-1 NGC call.** These are the rule-(c) reruns and the INFRA or MISLAUNCH retries. They cover:
   - P-112's own calls;
   - the S0 serials in the actual set;
   - the identity twin S0_SEED_CW8_TWIN, in twin mode (D3). P-112 never launches the twin's first attempt.

   **Carve-out (D6).** The kit keeps its own relaunches of an S0 call: the relaunch after a kit MISLAUNCH (kit order-check L737-791; MISLAUNCH record L1160) and the D7 relaunch at the same k after a monitor refusal. It keeps them until the call has a kit LAUNCH record, a P-112 attempt or a RESIDUAL_RETRY line for it (§10). Until then P-112 refuses to launch that call (KIT_RELAUNCH_OWNS).

c. **`close-attempt`** for every attempt, S0 kit attempts included.

d. **`assemble-registry`** and `assemble-registry --verify`, at step 4.

e. **`stop-outside-set`**, which root runs to stop S0 serials outside the actual set (D4).

f. **`record-monitor-refused`** (D7).

g. **`status`**, a read-only report: attempts and classes per call, the next legal attempt, an advisory terminal pre-check, MONITOR_ENDED_NO_RECEIPT for any attempt whose monitor ended without writing its receipt, MONITOR_STARTED_NO_LAUNCH_JSON for any attempt whose monitor left its receipt stdout or stderr but wrote no `.launch.json`, every RESIDUAL_RETRY line with the retry it admits, and each call's run of consecutive non-attempts (§10). With the run volume unmounted it reports RUN_VOLUME_NOT_MOUNTED in place of every residual and `absent` finding (§10).

**P-112 does not:**
- **Fill specs.** The filler opens the slots pin (filler L264, L292), so root runs `fill_step5_c2v001.py` on root's side, under root's blinding guard, as it did for S0. P-112 never runs or imports the filler; it checks root's fill directory.
- **Register NGC ρ points (A211 consequence 2, N3).** Point custody admits exactly the four registered S0 keys. Every Phase-1 member or F point outside S0 needs a root NGC ρ point registration before its acceptance. Root writes each one when u_A fixes the actual set. P-112 neither writes nor checks these registrations; acceptance is post-run and outside P-112.
- Produce certificates.
- Write call records. Root writes them (RUNBOOK L67).
- Write into the S0 kit's `launches/` directory.

## 2. Files you may open

Every sha below was computed from the file's bytes on 2026-10-20. P-112 checks every pin from bytes before use. `A` = `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/`.

| file | sha256 | use |
|---|---|---|
| `A/ngc_cx3r008_closure_cx3/implementation/galaxy_m0_forward_c2v011_cx3v005_cx3r008_cx3v001.py` | `577f8c94366ae8f99c5387b87397a83020f8186dc523b987d042103283346377` | Read it for the status set (strict clone L8989-9102: seven statuses; exit 0 only for COMPLETED and COMPLETED_INVALID, L9102) and for the run and _stage argv forms (L1825-1865). In production it is executed only by root_monitor. Never run it in a test. |
| `A/galaxy_m0_forward_c2_0466/root_monitor_c2v001.py` | `ba031c2340057d88ee399138cc645012a93aa7dc3eb7c9bba56d112c94a47107` | The receipt schema and keys (L133, L147, L177-199; utc_start and utc_end at L192) and the self-hash (L203-224). Tests may import it from verified bytes and call `run_monitored` on a synthetic driver in a scratch directory. |
| `A/s0_launch_kit_c2/s0_kit_c2v003a.py` | `fdc0ee6c833072b40991750f8df1122a1b51910986f01af3480a73cccfbed550` | Call `kill-target` and `twin-trigger` as subprocesses. Read ATTEMPT_RE (L123), the record schemas and names (L318-325, L395-423, L970-982, L1096-1173), register's same-spec reuse (L635-644) and the checks to port: fill-check L486, dry-verdict L566, ext1-check L651, watch-check L698, check_monitor_argv L826, launch_checks L992, wait_launch_record_parses L1026. Never call its plan-based subcommands for a non-S0 call. |
| `A/s0_launch_kit_c2/launch_s0_serial_root_c2v003a.sh` | `621263a21b813e8c71762cea57b0efc6ba36aecb1cf9023cc788f9133c3a96c2` | Read only (the launch order to mirror; the unique work directory, L121-127). |
| `A/s0_launch_kit_c2/launch_twin_root_c2v003a.sh` | `f199544db9fe40a4fedbe7647d52ad4bd8dacb13a9aa9c1b9ab4ad0198e7769f` | Read only (twin flow; `watch_pid`, L188-191). |
| `A/s0_launch_kit_c2/twin_kill_watch_c2v003a.sh` | `a3d70bec454691b6dcfcb8a9bbfe40d50b71cb85da564fc4ab803b55b02de925` | Run unchanged in twin mode. |
| `A/s0_launch_kit_c2/s0_prelaunch_record_c2v001.py` | `a10965b7a508f106e3d153632d2b1a39a427d9106fa2de3c9e09d92b85bcb59a` | Load from verified bytes. Call `parse_v006_pins` only. |
| `A/s0_launch_kit_c2/README_S0_LAUNCH_KIT_C2V003A.md` | `42978c3f938b1bf45a6a45b623e6f8ad25c5a333f8ecaef9a6cf657206f10b0e` | Read. |
| `A/step5_path_c2/tools/fill_step5_c2v001.py` | `ec417e76509427d8e942f52f02e9862a0277c90e3b92014c48b44a2efad61783` | Read only: the fill-receipt form and how spec values derive from θ (L291-298, L314). **Never run or import it.** |
| `A/step5_path_c2/tools/dry_one_c2v001.py` | `aac20dd3ca18bb609b37216f552aeb5a6b9f37147e17fc5501ea3c8d0842596b` | The dry harness. Production runs it as a subprocess; tests use a stand-in. |
| `A/step5_path_c2/tools/phase1_point_handoffs_c2v001.py` | `7d3b7c3c86204ca98b7fb87e39b11b544f3ee6069f8b34909e4c7810c00667cb` | Read: the F-point handoff UNT_STEP5_PHASE1_POINT_HANDOFF_C2V001. |
| `A/step5_path_c2/README_STEP5_PATH_C2V001.md` | `fba1a70a91f70b36b0f8035bb9ade5ec78bd8a44667954bd877c03d02c2eb1cd` | Read (L48: the spec label carries `theta_key=<program key>`). |
| `A/step5_path_c2/POLICY_C2V001.json` | `0c781a17548150831a7e10b8dd9d27897b856ab21398ee277fab3d2bbc4287e9` | Pin, and read its keys. Do not follow its `slots` pin. |
| `A/step5_path_c2/templates/TEMPLATE_A_K32_A2_HEADLINE_C2V001.json` | `68a19360d49f4dc547608ca8b2cec7116bed03b0f0cb947bb55e2aa1c61c13fb` | Serial template: the spec's structure and leaf paths. |
| `A/step5_path_c2/templates/TEMPLATE_A_K32_A2_HEADLINE_CW8_TWIN_C2V001.json` | `1aa662697fe259bd8c1bb9a4bda6170fdfabcc31e10a56a049a02c2f93961783` | Twin template: read only. |
| `A/sched_s45_c2/v003/CAPS_S45_C2V003.json` | `35f66b6a3152f985fe6edcbaeda2950e5b17e9f9f6026e5f6201052db1508f64` | Wall and output caps of record. |
| `A/tail_scheme_impl_c2/certificates_ngc_k32/gates/LO_NGC_K32_CERT_V001.json` | `07745bbf6d5c35d5a8568de7fc9e78b8c3bd8c3e371680dc8869c42a893c0382` | Custody pin; check the sha only (A136). |
| `A/phase1_c2/S0_RECORD_ROOT_V001/S0_C2V001.json` | `1be5ed709cdb49106652beb76baaafc1c257e760d8cda2c62c18ea6fb2e88143` | The S0 points and keys. |
| `A/phase1_c2/phase1_c2v003b.py` | `7d891ff7d81b0e9d103707d79c7a057cedc6dc1e893a0f4e9372a51d0b796dd4` | Read: the handoff (L628-707; L686-691 carry no θ or key), theta_of (L755-762), fdplan (L776-822). Do not run it. |
| `A/phase1_c2/README_PHASE1_C2V003B.md` | `cf3a4de73067529308c3f744261e641aa7f9d61b0b21e45338a60a22ad6ae3b0` | Read. |
| `A/calibration_orchestrator_c2/v005/calibration_orchestrator_c2v005.py` | `c75a889ff4646a816329756124a19532cbc166d26f47ce2ea5147b71c2cf7c4d` | `theta_key` (L523-529): load from verified bytes, or carry a verbatim copy proven equal on synthetic θ. |
| `A/runbook_v002_c2/roster_builder_c2v006.py` | `0cc731065d1f00e1549cb7b9442c901da0a35f48c8a03d67f14701f652ad0aa2` | Load from verified bytes. Production uses `canonical_bytes` and `theta_sha256` (L267-277). Tests use `_launch_registry`, `_receipt` and the rule-(c) logic (L581-787). Never call a function that loads v003g or the slots. |
| `A/runbook_v002_c2/RUNBOOK_V002_C2V006.md` | `e162db3e7bcaf348db2455aac9032ac8b0c57bb536ec97d043b6d9aad084349b` | Read §1 (L58-118) and §2 (L133-195). |
| `A/runbook_v002_c2/README_RUNBOOK_V002_C2V006.md` | `730bc14ce973f5eb61ff753541e31d0a9fa26d0f94acaf95b172ef7d26279b8f` | Read. |
| `A/runbook_v002_c2/interface_proof_c2v006.py`, `A/runbook_v002_c2/test_runbook_v002_c2v006.py` | `9b3772cfc6cfcb3a9f5d89497c9b855e17f3508e3474c1ca1c961f9520e6402d`, `88d79035bab8f78131a44d4f03cd209b85ca9245799d3e489441deee5d31268e` | Read, as patterns for the interface proof. |
| `A/freeze_score_readiness_cx3/v003g/prediction_freeze_c2v003g_cx3v001.py` | `48a1e48a5230fff346705c338da30a8ee53a8643193dbe4616c25e61eab3d405` | Check the sha, and grep field names only (`theta_engine`, `theta_ngc`, L2162-2163). **Never import or execute it** (it pins the slots). |
| `A/s0_launch_kit_c2/FREEZE_SPEC_OF_RECORD_C2V004.json` | `e2a7650e166a9230138ffd16453ac8fdabab41a8695169844940c4c061a894ec` | Spec of record: check the sha only. |
| Declared-list tools (§9) | listed in §9 | Check the sha only. Never run them. |
| `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/A133_TWO_PHASE_PROTOCOL_V001.md` | `cd92ef914a0d562f0392080ebf709b5fdb1d85ef7f7b4493ee143fe782cfac17` | Read §1.4, §2 and §3 (L77-111, L180-191, L201-222). |
| `A/miss_reading_prereg_c4/r3a_sc3/PREREG_MISS_READING_R3A.md` | `c64f65a357a0d3b44b362795fe7793576ba0ff6a71f1bafd2357573e2eb376c8` | Read L454 only (the first step-5 launch receipt). |
| V006: `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V006_ADDENDUM.md` | It grows; the sha was `6565c9737bf988abecff6d95453b0a114424d12e66440935b705505608eec26c` (285,659 B, through A221) at 17:08:48Z on 2026-10-20, unchanged since its 16:43:44Z write; root re-checks it when sending | **The named exception.** Read only these entries, by `## ` heading: A223 (the RUNBOOK rulings), A212, A211, A210, A208, A205 (items 6, 8 and 11(2)), A179, A172, A171, A166, A161, A148, A143 (D3), A141, A136, A135, A108. In production, P-112 reads it to parse pin lines. |

## 3. Files you must not open

- **Any path with a component containing `ngc3198`** (case-insensitive), except V006 at the entries above. This covers slots V003 (`d3859b42`) and any successor, NGC3198 target, observed-velocity and sigma files, `NGC3198_GEOMETRY_TRACE_C2V004.json`, and every file the driver or the filler pins (A205 item 6: also any NGC3198 file the code pins).
- `FREEZE_EXPECTED_INPUTS_C2V00*.json`, `DRYRUN_FREEZE_C2V004.json`, the K32 compare, N1 and node records, the program query manifest.
- **Run outputs:** anything inside any outdir, any `stages/` file (only existence, through the kit's twin-trigger), and every real run's `<outdir>.receipt.json.stdout.txt` and `<outdir>.receipt.json.stderr.txt` (existence checks only, §10). The work directory's `monitor.stdout.txt` and `monitor.stderr.txt` (P-112's or the kit's) may be hashed, never opened for content, and only when no `.launch.json` exists for that attempt (§10).
- `V007_POSTSEAL_RECORDS`, every `A_SIDE/` folder, classifier outputs, freeze manifests and scores.
- `~/.codex` (P-112 never reads it).
- **No network.**

## 4. Configuration (written by root and pinned on every call)

`--config <abs path> --config-sha256 <hex>`, schema `P112_CONFIG_CX2V001`, exact key set:

- **Paths and runtime:**
  - `python`: the kit's runtime `/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`.
  - `v006`: the V006 path. `v006_copy_dir`: an absolute directory outside every run tree (G24).
  - `run_volume`: a mount point, `/Volumes/External1` unless root names another (D9). `run_root`: one level under it, with the `NGC_` prefix.
  - `p112_launch_root`: an absolute, real, internal directory, not under `/Volumes`.
  - `s0`: `{launch_root, run_root}`, the kit's.
- **Constants:** `host_ram_bytes_expected` 137438953472.
- **Phase-1 pins**, each `{path, sha256}`:
  - `plan_output_primary`: the saved PLAN `evaluate_envelopes(budget=0)` PRIMARY output.
  - `plan_build_record`, `selection`, `fdplan` (FDPLAN_C2V001.json).
  - `spec_of_record`, which must be `e2a7650e…`.
  - `at0a_pass`.
- **Calls:**
  - `members`: `[{log_index, role, order, member_id, handoff pin, fill_dir, eps pin, gq pin}]`.
  - `f_points`: `[{label F0|F1|F2, handoff pin, fill_dir, eps pin, gq pin}]`.

P-112 applies the kit's `path_rules` (L290-297) and refuses any path with an `ngc3198` component in these: `run_root`, `p112_launch_root`, every `fill_dir`, outdir, receipt and spec, and every monitor argv element.

## 5. Names and layout

- **Call NAME** (V006 pin grammar `[A-Z0-9][A-Z0-9_]*`):
  - `P1_M<log_index:04d>` for members, `P1_F0`, `P1_F1` and `P1_F2` for F points;
  - for S0 calls, the kit name (`S0_SEED_SERIAL`, `S0_J0_SERIAL`, …, `S0_SEED_CW8_TWIN`).
- **Records in `p112_launch_root`:**
  - `registry/P112_<NAME>_CX2V001.json`;
  - `launches/P112_<NAME>_<LAUNCH|MISLAUNCH|MONITOR_REFUSED>_CX2V001_A<k>.json`. The `P112_` prefix can never match the kit's ATTEMPT_RE;
  - `work/<NAME>_A<k>_<YYYYMMDDTHHMMSSZ>_<pid>/`, one per invocation, created by exclusive `mkdir`, as the kit does (serial script L121-127). It holds the plan, checks, dry plan and monitor stdout/stderr. A relaunch at the same k gets a new work directory;
  - `twin_kill/`, where the kit's kill watch writes in twin mode;
  - `outside_set_stop/`;
  - `assembly/`.
- **On the run volume:**
  - outdir `<run_root>/NGC_P1_<NAME>_RUN_CX2V001_A<k>`;
  - the monitor writes `<outdir>.receipt.json`, `.receipt.json.launch.json`, `.receipt.json.stdout.txt` and `.receipt.json.stderr.txt`;
  - P-112 writes only `<outdir>.solo.json` and `<outdir>.attempt_receipt.json`. For S0 kit attempts, the attempt receipt goes beside the kit's outdir.

## 6. Preconditions for every launch (refuse, with a named code, otherwise)

1. **Launch condition (D8).**
   - V006 holds exactly one TOOL_PIN line named P112_LAUNCHER_CX2V001, `TOOL_PIN P112_LAUNCHER_CX2V001 <sha256 of this tool's bytes> <this tool's realpath>`, and its sha and realpath are this tool's own. It is the same line form as the kit's pins and sits under an entry heading. Root writes it only after Claude4's 0-blocking review.
   - **Grammar.** A TOOL_PIN line is a whole V006 line matching `^TOOL_PIN ([A-Z0-9][A-Z0-9_]*) ([0-9a-f]{64}) (/.*\S)$` (the kit's PIN_RE form, `a10965b7` L43), under an entry heading. Text that mentions TOOL_PIN inside a line is not a pin line; the rulings entry itself contains such text. A line that begins `TOOL_PIN P112_LAUNCHER_CX2V001` and does not match refuses TOOL_PIN_MISMATCH.
   - The version is part of the name. TOOL_PIN lines with any other name, such as a later `P112_LAUNCHER_CX2V002`, are ignored by this tool.
   - The kit's parser ignores `TOOL_PIN`, which is not one of its KINDS (`a10965b7` L41; KEYWORD_RE and PIN_RE at L42-43). Nor is `RESIDUAL_RETRY` (§10).
   - **The same gate applies to every subcommand that writes a record:** launch, close-attempt, assemble-registry (both modes), stop-outside-set and record-monitor-refused. Each refuses with TOOL_PIN_MISSING, TOOL_PIN_MISMATCH or TOOL_PIN_DUPLICATE. Dry mode and `status` work without the line.
2. **M-15 and the seed.** `<s0 launch_root>/M15_PRELAUNCH_RECORD_C2V001.json` exists with schema UNT_M15_PRELAUNCH_RECORD_C2V001. The kit's `launches/` holds a LAUNCH record of S0_SEED_SERIAL, found through ATTEMPT_RE (r3a L454).
3. **Pins.** AT-0a PASS, the selection, the PLAN output and fdplan verify from bytes. The PLAN output is value-free: every member has `evaluated` false.
4. **Handoff.**
   - Members: a phase1 v003b handoff, schema UNT_STEP5_ADMITTED_POINT_HANDOFF_CX3V001, with the member's certificate map (A135 item 10).
   - F points: the FDPLAN handoff UNT_STEP5_PHASE1_POINT_HANDOFF_C2V001.
   - V006 holds `HANDOFF_PIN <NAME>` and `SPEC_PIN <NAME>`, parsed by `parse_v006_pins` (RI45-09, RI45-13). The handoff and spec bytes equal those pins.
5. **Certificates.** The call's own EPS and GQ certificates, each with `point.key` equal to the call's program key (A148). P-112 reads only that field. LO `07745bbf` is checked as a custody pin.
6. **fill-check.** Port the kit's checks to the call's handoff type:
   - the fill receipt's schema, `launch_authorized` false, its handoff pin and theta_key, and no pending certificates;
   - leaf 1 in the serial spec;
   - EPS and LO pins in the spec;
   - the label `step5 A_K32_A2_HEADLINE theta_key=<key>`;
   - the pair differs only in the leaf.
7. **Dry plan.** A fresh dry plan with the real pins and the driver sha checked (RI45-13; A135 item 9). The verdict uses the kit's checks (L566-598), not the readiness label.
8. **watch-check** as the kit runs it (A172 N3).
9. **The θ checks** (§7).
10. **Disk (D9).** The run volume is mounted, not symlinked, and the outputs are absent. This mount check is also the one the rulings' G16 3 names (a missing volume is a stop, never a custody breach), and the one every residual, `absent` and RESIDUAL_RETRY decision waits for (§10, "Run volume first"). P-112 writes nothing under an unmounted path, in any subcommand. If `<outdir>.receipt.json.stdout.txt` or `.stderr.txt` exists for the planned attempt with no `.launch.json`, refuse MONITOR_STARTED_NO_LAUNCH_JSON (§10). Free bytes must be at least the attempt's output cap + 21,474,836,480:
    - serial first attempt: 167,503,724,544 (156 GiB);
    - serial OUTPUT_CAP rerun: 313,532,612,608 (292 GiB);
    - twin: 55,834,574,848 (52 GiB). The twin never has an OUTPUT_CAP rerun (§8).
11. **Host RAM.** `sysctl -n hw.memsize` equals 137,438,953,472.
12. **Reruns and retries only.** An attempt after a non-attempt LAUNCH or MISLAUNCH, or after an attempt named in an honoured RESIDUAL_RETRY line (§10), is a retry, even at k = 1, and these checks apply to it, not §6.13's:
    - every earlier LAUNCH or MISLAUNCH record of NAME has its attempt receipt, or is a non-attempt whose monitor receipt exists, or is named in a RESIDUAL_RETRY line that P-112 honours (§10). An earlier record whose monitor pid is gone with no monitor receipt, and no such line, refuses MONITOR_ENDED_NO_RECEIPT (§10);
    - after a RESIDUAL_RETRY line for attempt k, no live process runs attempt k's monitor command or its planned driver command (RESIDUAL_ATTEMPT_PROCESS_ALIVE, §10);
    - the next-attempt rule (§10) allows this attempt;
    - an S0 rerun uses the kit registry entry's spec bytes, which must equal V006 `SPEC_PIN <NAME>`;
    - a counted rerun, and a solo retry (§10), meets the solo condition (§9);
    - for an S0 call, the call has a kit LAUNCH record, a P-112 attempt or a RESIDUAL_RETRY line (§1b carve-out).
13. **First attempts only** (no LAUNCH or MISLAUNCH record of NAME exists, and no RESIDUAL_RETRY line names NAME):
    - the call's program key is in no kit registry entry;
    - no LAUNCH or MISLAUNCH record exists for NAME;
    - no registry entry exists for NAME, with one exception. After a monitor refusal at this k (D7), the existing entry is admitted if its spec sha, θ key and V006 pins equal this attempt's and the only records for NAME are MONITOR_REFUSED records at this k. P-112 then reports ALREADY_REGISTERED_SAME_SPEC and writes no new entry, as the kit's register does (L635-644). Any other existing entry refuses REGISTRY_ENTRY_EXISTS_FOR_ANOTHER_SPEC or ALREADY_LAUNCHED.

## 7. θ checks (closing the RUNBOOK 1b UNTESTED item)

**Members.** Match the PLAN member to the fdplan member and the handoff by (log_index, role, order) (IC-P1-MEMBERS, A171 L1592). Then:
1. Take θ from the handoff's `source_export_pin` at its `log_index` (`theta_natural`). Its key set equals the PLAN member's `theta_engine` key set, and every value has an identical `float.hex`. fdplan `members[].theta_hex` agrees, value for value.
2. `theta_key(PLAN theta_engine)` (orchestrator L523-529) equals the fdplan key, the fill receipt's `theta_key` and the spec label's `theta_key`.
3. Every spec value the filler derives from θ (filler L291-298) equals the same derivation from the PLAN `theta_engine`, by `float.hex`. That includes `gamma` as the IEEE product the filler computes.
4. The spec's `distance_Mpc` and `inclination_deg` equal three things, by `float.hex`:
   - the PLAN `theta_ngc` nuisance values;
   - the S0 seed serial spec's values (S0_SPECS_OK);
   - 13.8 and 72.0 (A171).
5. `theta_sha256 = sha256(canonical_bytes(theta_ngc))`, where `theta_ngc` is taken as parsed from the saved PLAN output and hashed with c2v006's `canonical_bytes`. Never recompute `theta_ngc` (c2v006 L276-277).

**F points.** fdplan `F[k]`: the key equals the handoff `point_key`, the fill receipt `theta_key` and the label key. The spec values match the `F[k]` `theta_hex` as in check 3, and the geometry passes check 4. `theta_sha256` is the point key (RUNBOOK L82).

**Mapping an S0 serial to a MEMBER** (assemble-registry, §14): the same checks 1-4 against the kit spec and the kit registry entry's `theta_key`.

Any mismatch refuses, naming the check and the coordinate. -0.0 and 0.0 differ.

## 8. Caps

| attempt | wall_cap_s | rss_cap_bytes | output_cap_bytes |
|---|---|---|---|
| serial, first (P-112 calls; S0 from the kit) | 610,324 | 137,438,953,472 (RAM) | 146,028,888,064 |
| serial, rule-(c) rerun | 1,220,648 (2 × first) | host RAM | 146,028,888,064 (OUTPUT_CAP rerun: 292,057,776,128) |
| twin, first (kit) | 22,752 | 1,511,828,488,192 (RAM × 11, A172 N4) | 34,359,738,368 |
| twin, rule-(c) rerun (D3) | 45,504 | 11 × host RAM | 34,359,738,368 |
| INFRA or MISLAUNCH retry | repeats the caps of the attempt it replaces | same | same |
| REFUSED or BLOCKED retry | repeats the caps of the attempt it replaces, in solo mode | same | same |

- The spec bytes are identical on every attempt of a call.
- "Doubled" is always 2 × the call's first attempt's wall cap.
- The twin never has an OUTPUT_CAP rerun: any STOPPED_* twin status is TWIN_PLANNED_STOP, which is terminal (§12).
- Check the wall and output values against CAPS_S45_C2V003, as the kit does (L363-367).

**Schedule risk (disclosed; this is registered rule (c), not a new rule).**
- A failing call normally needs two solo reruns at the doubled wall: up to 1,220,648 s each for a serial (an S0 serial included), and 45,504 s for the twin.
- Each serial rerun can add about 14 days to the start of Phase-1 step 4.
- Solo mode runs every counted rerun alone, so reruns of different calls do not overlap, and their delays add.

## 9. Process sampler, solo mode and the hold rule (G25 items 3-5; D5)

**Declared list.** A P-112 constant. Its canonical-JSON sha256 goes into every sample. Only a V006 entry can change it. A process counts if any argv element names one of these files, by realpath or by the sha256 of the named file (cache hashes by path, mtime and size):

| tool | path under `A/` | sha256 |
|---|---|---|
| driver, only with argv subcommand `run` or `_stage` | `ngc_cx3r008_closure_cx3/implementation/galaxy_m0_forward_c2v011_cx3v005_cx3r008_cx3v001.py` | `577f8c94366ae8f99c5387b87397a83020f8186dc523b987d042103283346377` |
| EPS point producer | `ngc_point_producer_c4/s0/build_c4v001/tools/eps_ngc_point_c4v002.py` | `8972822b5439e184297b4a5dbb552983ddb806804565ee1cc26691b680147235` |
| GQ binding producer | `ngc_point_producer_c4/s0/build_c4v001/tools/gq_binding_c4v002.py` | `f4ee064d9da414d9b98581ff6c1e374aab566950d9faf2e978342bc9a5dba0b1` |
| NGC ρ producer c3v003 | `s4rc1_c3/ngc_rho_c3v003/ngc_rho_producer_c3v003.py` | `d3d0f3ddda8be2e3d4b0e0732e5237a602cb3b1fb99d7921e8c10a886420a3c4` |
| NGC ρ stage c3v003 | `s4rc1_c3/ngc_rho_c3v003/ngc_rho_stage_c3v003.py` | `496d2a215145fb25aadbc4623b8930134cc2679cf1fe8097c65bf84cab450090` |
| NGC LO slot proof c3v003 | `s4rc1_c3/ngc_rho_c3v003/ngc_lo_slot_proof_c3v003.py` | `ada31d121871598aa0cd7db5137691502421c873cc75bdf331706501d3f3310a` |
| NGC acceptance handoff c2v005 (A211 stack of record) | `ngc_acceptance_c2/ngc_acceptance_handoff_c2v005.py` | `7077ad9337d48b444bb724b3d0dca531e615bbb09656fa00ba453bacf2e634b1` |
| NGC LO state adapter c2v003a (A211 stack of record) | `ngc_acceptance_c2/ngc_lo_state_adapter_c2v003a.py` | `9c4b6dfc591cfd5c372416beb936d5d903540e5fc41e4a327b428d7ba5001eb2` |
| NGC roster recipes c2v002 (A211 stack of record) | `ngc_acceptance_c2/ngc_roster_recipes_c2v002.py` | `c700f469314d73e90cd2498cdbea5b7f69fbbd9b61676468ea5e37356939978e` |
| NGC acceptance handoff c2v003a (kept: the stricter reading of D5) | `ngc_acceptance_c2/ngc_acceptance_handoff_c2v003a.py` | `7c54fd6fcc3defbc6728a35fd5125eb0d2fba23b735a38af6ac8de2094c04427` |
| values writer v004, cx2v002 (A212) | `values_writer_cx2/values_writer_c2v004_cx2v002.py` | `26319ecbfaf944c80c5df91a0c592899727e6ff9f5177404ebc49309bd906f0e` |
| carrier extractor cx3v005 | `step5_ngc_route_ab_readiness_cx3/carriers_0606_v001/tools/extract_carriers_cx3v005.py` | `50c7db5fbc2eb2cce17dcbb53ba1186bfdbc635a4098b0eb33ebd1402829732f` |
| carrier extractor c2v001 | `step5_path_c2/tools/extract_carriers_c2v001.py` | `8acd21c7b8c2c1d96038a6d1eee9cbf68c25e556ae4da59bea8b70f09c1c602a` |

An NGC tool not on the list (adopted after A212) joins this list only by a V006 entry. Until then, root's hold rule keeps it from starting during a solo attempt (below).

**Never counted:**
- root_monitor;
- the dry harness and the driver's `dry-run` subcommand (driver L4981);
- the sampler, P-112 itself and the kill watch;
- the attempt's own tree: the driver pid from `.launch.json` `child_pid` and all its descendants, by ppid closure at each poll. Before `.launch.json` exists, the monitor pid's descendants.

**The sampler** is a detached process with its pid in the LAUNCH record.
- It takes its first sample at least 1 s before P-112 starts the monitor. P-112 waits for that sample, then sleeps until at least 1 s has passed, then starts the monitor.
- It polls `ps -axww -o pid=,ppid=,pgid=,command=` every `poll_s` ≤ 10 s.
- It stops after the monitor pid is gone and the monitor receipt exists, and only after a final sample taken at least 1 s after the receipt exists.
- Sample times (first_utc, last_utc and each sample's utc) are UTC with microseconds. The monitor's utc_start and utc_end are whole seconds (root_monitor L43-44; utc_start is taken at L146, just before Popen).
- It also stops when the monitor exits without writing `.launch.json` (a monitor refusal, D7). In that case it writes nothing at the outdir path, so a relaunch at the same k finds `<outdir>.solo.json` absent.
- It also stops when the monitor pid is gone (§10's test) and no receipt has appeared 60 s later (MONITOR_ENDED_NO_RECEIPT, §10). It then writes nothing at the outdir path. The 60 s are counted only while the run volume passes the §6.10 mount check; while it is unmounted, the sampler keeps polling and decides nothing (§10, "Run volume first").
- At a normal end it writes `<outdir>.solo.json` with schema STEP5_SOLO_SAMPLE_CX2V001 and these keys: name, attempt, outdir, declared_list_sha256, poll_s, n_samples, first_utc, last_utc, monitor_start_utc, monitor_end_utc, largest_gap_s, complete, max_other_ngc_processes, nonzero_samples (utc, count, [pid, tool]), own_tree_root_pid, writer pin, date_u.
- close-attempt sets `other_ngc_processes_max` to null in each of these five cases (the same five as G25 item 4):
  1. the sampler died, or the file is absent;
  2. `complete` is false. `complete` is true if and only if every poll's `ps` call exited 0 and parsed, and the sampler ended by the normal-end rule (monitor gone, receipt exists, final sample at least 1 s after it);
  3. largest_gap_s > 2 × poll_s;
  4. floor(first_utc) is not earlier than the monitor receipt's utc_start: null unless floor(first_utc) < utc_start;
  5. floor(last_utc) is not later than the monitor receipt's utc_end: null unless floor(last_utc) > utc_end.

  floor() drops the fraction to the whole UTC second; utc_start and utc_end are parsed from `%Y-%m-%dT%H:%M:%SZ`. A first sample taken in the same second as the start, but before it, compares as later than the truncated utc_start. With the 1 s lead and the 1 s tail, cases 4 and 5 cannot fire on an honest attempt; without them, such an attempt would never count (a false null, costing another rerun of about 14 days).
- c2v007 recomputes the value from the pinned sample under the same five cases, with the same whole-second comparison, and refuses a receipt whose value differs. Compute it exactly this way.
- The count is a lower bound and is disclosed as one. The hold rule is the guarantee.

**Solo mode** applies to every rule-(c) rerun, every retry of a REFUSED or BLOCKED attempt, and any retry of a solo attempt.
- It refuses to start while any listed process is alive.
- While it runs, every other P-112 launch refuses (SOLO_RERUN_ACTIVE).
- The LAUNCH record carries `solo_mode` true and `counted_rerun` (true for a rule-(c) rerun, false for a retry), plus `rule_c_basis`, which pins the attempt receipts the attempt counts against. `counted_rerun` records how the attempt was launched; it never decides which two attempts form a pair (§10 item 2).
- Root's side of the hold rule is a root procedure. While a solo attempt runs, root starts no S0 kit call, twin or listed process, and no NGC tool not on the list (adopted after A212).

## 10. Attempts: numbering, ownership, the next legal attempt (D6, D7)

- **Numbering.** The next k = 1 + the largest k among the kit's LAUNCH or MISLAUNCH records for NAME (read through the kit's ATTEMPT_RE in `<s0 launch_root>/launches/`), P-112's LAUNCH or MISLAUNCH records for NAME, and the k of every RESIDUAL_RETRY line for NAME. For a call P-112 has launched once, P-112 owns every later attempt. Never write into the kit's `launches/`.
- **Kit carve-out.** For an S0 call with no kit LAUNCH record, no P-112 attempt and no RESIDUAL_RETRY line, the next attempt is the kit's (§1b). Report it as such and refuse to launch it.
- **Run volume first.** MONITOR_ENDED_NO_RECEIPT, MONITOR_STARTED_NO_LAUNCH_JSON, the D7 `absent` checks and the RESIDUAL_RETRY residual check are decided only after the §6.10 mount check passes (the run volume is mounted, not symlinked). With the run volume unmounted, `status` reports RUN_VOLUME_NOT_MOUNTED, and close-attempt, record-monitor-refused, assemble-registry and launch refuse RUN_VOLUME_NOT_MOUNTED (a stop, as in the rulings' G16 3) and write nothing. The sampler's 60 s wait (§9) is counted only while the volume is mounted. A receipt on an unmounted volume is not absent: after a host restart, a finished attempt whose receipt sits on the unmounted volume is never reported or refused as a residual.
- **MONITOR_REFUSED does not use up k.**
  - If the monitor exits without writing `.launch.json`, `record-monitor-refused` writes `MONITOR_REFUSED_ATTEMPT_RECORD_C2V001` by exclusive create to `launches/P112_<NAME>_MONITOR_REFUSED_CX2V001_A<k>.json`. Its exact key set is: schema, name, attempt (k), launcher (`P112_CX2V001`), writer {name `P112_LAUNCHER_CX2V001`, sha256 of this tool}, plan {path, sha256}, monitor_stdout and monitor_stderr {path, sha256} from the work directory, absent {outdir, receipt, launch_json, receipt_stdout, receipt_stderr}, date_u, rule. The five `absent` paths are `<outdir>`, `<outdir>.receipt.json`, `<outdir>.receipt.json.launch.json`, `<outdir>.receipt.json.stdout.txt` and `<outdir>.receipt.json.stderr.txt`.
  - **A monitor that started is not a refusal.** root_monitor creates `<receipt>.stdout.txt` and `.stderr.txt` by exclusive open (L143-144) after its refusal checks (L133), before Popen and before `.launch.json`. A monitor that dies there leaves both files, and a relaunch at the same k would fail on that open every time. If either file exists, the event is not a D7 refusal: `record-monitor-refused` refuses MONITOR_STARTED_NO_LAUNCH_JSON, writes nothing, and root rules (a driver may have started). It checks existence only; it never opens either file. A launch of that call at k refuses MONITOR_STARTED_NO_LAUNCH_JSON too (§6.10), until a RESIDUAL_RETRY line for it (below).
  - The work directory's `monitor.stdout.txt` and `monitor.stderr.txt` are hashed only when no `.launch.json` exists for the attempt.
  - For a kit call, root writes the same record by hand, at `<s0 launch_root>/monitor_refused/<NAME>_MONITOR_REFUSED_C2V003A_A<k>.json`, outside the kit's `launches/`, and only after that attempt's monitor pid has exited: the kit's scripts exit 5 after about 120 s without `.launch.json` even while the monitor is still alive (serial script L202-208; twin script L150-155). That record has launcher `KIT_C2V003A` and writer {name `ROOT`, sha256 null}, and it pins the kit work directory's `plan.json`, `monitor.stdout.txt` and `monitor.stderr.txt`. **P-112 accepts root-written records.** It checks the exact key set, the schema, the name and k, every pin from bytes, and, while no relaunch at the same k has started (no LAUNCH or MISLAUNCH record of (NAME, k), and neither `<outdir>.receipt.json.stdout.txt` nor `.stderr.txt` of k exists), that every `absent` path is still absent. Once the same-k relaunch has started, those paths belong to the relaunch and are not re-checked; the writer's check at date_u stands.
  - The relaunch reuses k once. For a P-112 call it reuses the same-spec registry entry (§6.13) and a new work directory. A second refusal at the same k cannot be recorded (exclusive create), so P-112 refuses with MONITOR_REFUSED_TWICE and root rules. This, MONITOR_STARTED_NO_LAUNCH_JSON and MONITOR_ENDED_NO_RECEIPT (below) are the rulings' three disclosed residuals. Root's ruling on the last two has one machine form, RESIDUAL_RETRY (below). MONITOR_REFUSED_TWICE writes no record, so the state on disk is the same as after the first refusal. P-112 cannot see an unrecorded second refusal and does not hold the call; it admits a further launch at k as it admitted the first relaunch (§6.13). Holding the call after MONITOR_REFUSED_TWICE is root's procedure (root runs every launch), and a third launch at k is made only on root's V006 ruling; no P-112 successor is needed for it.
  - Such an attempt is never an attempt of the call: it gets no attempt receipt, no call-record entry, and is listed in the assembly record.
- **Non-attempts** (G27 item 5: MONITOR_REFUSED; a LAUNCH or MISLAUNCH whose outdir does not exist at close; an off-spec LAUNCH or MISLAUNCH; an attempt named in an honoured RESIDUAL_RETRY line, which has no monitor receipt) do not separate an INFRA_REPEAT pair or a rule-(c) pair.
  - A LAUNCH with no outdir arises when the driver ends before its mkdir (driver L8994): a Refusal or OSError in cmd_run (L9208-9215) is not caught by main (L4971-4987), so the child exits 1 with no outdir and no finish (CHILD_FAILED|NONE|EXIT), and a signal there gives CHILD_FAILED|NONE|SIGNAL. The launch check reads only `.launch.json`, so it confirms, and the record is a LAUNCH.
  - Non-attempts carry no count limit, as INFRA retries carry none (A133 §3). `status` reports each call's run of consecutive non-attempts.
- **Monitor ended with no receipt (MONITOR_ENDED_NO_RECEIPT; the third residual).**
  - The case: a LAUNCH or MISLAUNCH record of attempt k exists, the monitor pid is gone, and `<outdir>.receipt.json` is absent, with the run volume mounted ("Run volume first", above). Causes: the host restarts or panics during a run of several days; the monitor is killed, P-112's own stop at the launch bound with `.launch.json` present included (§11.5); root_monitor's receipt write (`_write_x`, L199) fails because the run volume is lost or full (the receipt sits beside the outdir on that volume).
  - "Gone": no live process has the record's `monitor_pid` with a command line naming root_monitor and this attempt's `--receipt` path. A pid reused after a restart is not the monitor. Read the process table only.
  - `status` reports MONITOR_ENDED_NO_RECEIPT for the attempt. close-attempt refuses with this code and writes nothing. Every launch of that call refuses MONITOR_ENDED_NO_RECEIPT until a RESIDUAL_RETRY line for it (next bullet); any other ruling needs a P-112 successor. The sampler stops and writes nothing at the outdir path (§9).
  - No value is read. Nothing under the outdir is opened, nor `<outdir>.receipt.json.stdout.txt` or `.stderr.txt`. The call stays non-terminal, so step 4 waits, and root rules (rulings reading 19).
- **Root's ruling on a residual (RESIDUAL_RETRY).** Root's ruling on MONITOR_ENDED_NO_RECEIPT or MONITOR_STARTED_NO_LAUNCH_JSON has one machine form: a whole V006 line `RESIDUAL_RETRY <NAME> <k>` under the ruling entry. It is not a kit KINDS token, and it is parsed anchored, as TOOL_PIN (§6.1): the line matches `^RESIDUAL_RETRY ([A-Z0-9][A-Z0-9_]*) ([1-9][0-9]*)$` under an entry heading. Text that mentions RESIDUAL_RETRY inside a line is not such a line. A line that begins `RESIDUAL_RETRY ` and does not match refuses every launch (RESIDUAL_RETRY_MALFORMED). Duplicate lines for one (NAME, k) act as one.
  - With the line, attempt k of NAME is a non-attempt (G27 item 5) that uses its number. The next legal attempt is a retry at k+1 with attempt k's caps and solo mode, and no new registry entry (§6.12 applies, even at k = 1). That retry is P-112's, and the §1b carve-out ends for that call.
  - Attempt k's caps and solo mode are those in its LAUNCH or MISLAUNCH record. With no such record (MONITOR_STARTED_NO_LAUNCH_JSON), they are the caps and solo mode the next-legal-attempt rule gave attempt k, recomputed from the records before it.
  - P-112 launches it only when no live process runs attempt k's monitor command (root_monitor with `--receipt <outdir of k>.receipt.json`) or its planned driver command (`run --spec <spec> --outdir <outdir of k>`); otherwise it refuses RESIDUAL_ATTEMPT_PROCESS_ALIVE. Read the process table only. The outdir of k is the kit's (`run_name_for`, kit L318, L354-355, under s0.run_root) when attempt k was the kit's (no kit LAUNCH record, P-112 attempt or RESIDUAL_RETRY line before it, §1b), and P-112's (§5) otherwise. MONITOR_STARTED_NO_LAUNCH_JSON leaves no record naming its launcher, so this rule decides it.
  - P-112 honours the line only while attempt k of NAME is one of the two residuals: a LAUNCH or MISLAUNCH record of k whose monitor is gone (the test above) with no receipt; or no LAUNCH or MISLAUNCH record of k, `<outdir of k>.receipt.json.stdout.txt` or `.stderr.txt` present, and no `.launch.json`. Otherwise it refuses RESIDUAL_RETRY_NOT_RESIDUAL, so a line never turns an attempt that has a monitor receipt into a non-attempt. Existence checks only; neither file is opened.
  - Without the line, the call stays held. Any other ruling needs a P-112 successor.
  - Disclosed limit: S0_SEED_SERIAL before its first kit LAUNCH record. §6.2 refuses every P-112 launch until the kit holds a seed LAUNCH record, and the kit's order-check refuses every other S0 call (SEED_SERIAL_NOT_LAUNCHED_FIRST, kit L785-788). A residual there needs a successor of the kit or of P-112; P-112 reports it and refuses.
- **The next legal attempt,** from the call's LAUNCH and MISLAUNCH records, the closed attempts and the class map (§12). If any attempt of the call is MONITOR_ENDED_NO_RECEIPT or MONITOR_STARTED_NO_LAUNCH_JSON with no RESIDUAL_RETRY line for it, there is none: report it and refuse with that code. Otherwise the terminal conditions are checked first, in this order; the retry and rerun rules apply only if none holds:
  1. the last attempt is FINISHED, or PLANNED_STOP (twin only): the call is terminal. Refuse ATTEMPT_AFTER_TERMINAL.
  2. the last two attempts of the call (non-attempts excluded) form a rule-(c) pair, as c2v006 `_rule_c_problem` (L660-694) reads them; an attempt of any class between two failures separates them. Such a pair is terminal. A pair is identical raw status, FAILED, CAP or OUTPUT_CAP, identical spec, both samples 0, rerun RSS at RAM (twin: 11 × host RAM), rerun wall 2 × first, and for OUTPUT_CAP the output raised. Refuse ATTEMPT_AFTER_TERMINAL.
  3. the last two attempts of the call (non-attempts excluded) are both solo (solo mode, sample 0), with identical spec, identical caps and the identical raw status CHILD_FAILED|REFUSED, or CHILD_FAILED|BLOCKED: terminal, UNEVALUATED_INFRA_REPEAT (G13). Refuse ATTEMPT_AFTER_TERMINAL. Rule-(c) caps are not required, so a refusal on a first attempt becomes terminal after two solo retries.
  4. the last record is a non-attempt LAUNCH or MISLAUNCH, or the call's highest k is named in an honoured RESIDUAL_RETRY line: retry with that attempt's caps and solo mode (first-attempt caps if no attempt precedes it); no new registry entry. The retry takes the next k and is a retry, not a first attempt, even at k = 1 (§6.12).
  5. the last attempt reads CHILD_FAILED|REFUSED or CHILD_FAILED|BLOCKED: retry in solo mode with the caps of the attempt it replaces.
  6. the last attempt is any other INFRA (a MISLAUNCH that has a run directory included): retry with the caps and solo mode of the attempt it replaces.
  7. the last attempt is FAILED, CAP or OUTPUT_CAP: a rule-(c) rerun with solo mode and rerun caps (§8).
  - This logic is advisory. The builder decides terminality. Mirror c2v006 L643-787, with c2v007's changes:
    - attempt 0 needs only spec_sha256 and wall_cap_s (and output_cap_bytes for OUTPUT_CAP) unless it is counted;
    - the twin's RAM is × 11;
    - the INFRA_REPEAT pair is as defined above.
- **Twin mode (D3).** The spec is the kit's twin registry entry spec (`SPEC_PIN S0_SEED_CW8_TWIN`), leaf 8, at twin caps (§8).
  - Start the kit's kill watch unchanged: `--launch-root <p112_launch_root> --launch-json <receipt>.launch.json --outdir <outdir> --twin-spec-sha256 <sha> --mon-pid <monitor pid> --kill --max-wait-s <this attempt's wall cap>`.
  - Record its pid as `watch_pid` in the LAUNCH record.
  - The twin's `theta_sha256` and point_key are the seed key `968c915bece706ea1d6c0fa15357984884a87443e7c19eebd104230c9c961981`.
- **Outside-set stop (D4).** `stop-outside-set --name <S0 serial>` refuses unless:
  - the PLAN mapping shows the serial's key is neither a member's nor an F point's;
  - the kit's `kill-target`, given `--expect-leaf 1` and the monitor pid, verifies the target.

  It then sends TERM, and KILL after 15 s. It writes `S0_OUTSIDE_SET_STOP_RECORD_C2V001` to `p112_launch_root/outside_set_stop/` with these keys: name, attempt, the `.launch.json` pin, outdir, pgid, result, the PLAN and fdplan pins, the rule (A133 L103: kept, never read), date_u. It opens no output.

## 11. The launch itself

1. Run the preconditions. Create the invocation's work directory (§5) and write the plan (`UNT_P112_LAUNCH_PLAN_CX2V001`) there.
2. At first launch only, write the registry entry `UNT_P112_LAUNCH_REGISTRY_ENTRY_CX2V001` with these keys: name, kind (MEMBER or OTHER), alternative (PRIMARY or null), key (the v003g member_id, or F0-F2), point_key, theta_sha256, spec {path, sha256} (= the V006 SPEC_PIN), v006_spec_pin, v006_handoff_pin, handoff pin, PLAN output pin, fdplan pin, certificates {eps, gq, lo}, driver pin, fill_check pin, dry_verdict pin, theta_check pin, registered_at_attempt, config pin, date_u.
   - A relaunch at the same k after a monitor refusal reuses the existing same-spec entry (§6.13) and writes none.
   - An S0 rerun pins the kit's entry instead and writes none.
3. Start the sampler.
4. Exec the monitor in the A143 D3 form. Port `check_monitor_argv` (L826-876):
   ```
   PY -I -B <monitor> --driver <driver> --driver-sha256 <64 lowercase hex> --spec <abs> --outdir <abs>
     --receipt <outdir>.receipt.json --wall-cap-s <int> --rss-cap-bytes <int> --output-cap-bytes <int>
   ```
   Use absolute paths on the run volume, never through `runs_ext` (A141 L3). The outdir is new and absent. Run `nohup` with `caffeinate -i -w <monitor pid>`, as the kit does.
5. **Post-launch check.** Port `launch_checks` and `wait_launch_record_parses` (A172 N1: poll every 0.2 s, at most 300 s from the first poll). Check that the command, the driver, spec and monitor pins, the caps (the call's RSS rule), retries 0, and a launch utc after the M-15 record's epoch all match the plan.
   - On a mismatch, or a `.launch.json` that exists but does not parse by the bound: the kit's `kill-target`, TERM, KILL after 15 s, then wait up to 60 s for the monitor receipt. Write the MISLAUNCH record (A179 R2).
   - If no `.launch.json` appears and the monitor has exited: `record-monitor-refused`. It refuses MONITOR_STARTED_NO_LAUNCH_JSON if `<outdir>.receipt.json.stdout.txt` or `.stderr.txt` exists (§10).
   - If `.launch.json` is absent at the bound and the monitor pid is alive (verified by its command line naming root_monitor and this receipt), send TERM to the monitor pid, KILL after 15 s, and wait for it to exit. Then, if `.launch.json` exists, it is a MISLAUNCH (kill-target on its child_pid); otherwise the D7 rules apply (record-monitor-refused, or MONITOR_STARTED_NO_LAUNCH_JSON if the receipt stdout or stderr exists). kill-target runs without `--mon-pid` here: the monitor is gone, so the child's parent has changed and kill-target's parent check (kit L958-959) would refuse; it still checks the group leader, the exact command and the spec (kit L932-957). That MISLAUNCH has no monitor receipt, so the attempt is MONITOR_ENDED_NO_RECEIPT (§10).
6. **LAUNCH or MISLAUNCH record** (`UNT_P112_LAUNCH_RECORD_CX2V001` / `UNT_P112_MISLAUNCH_RECORD_CX2V001`):
   - the kit's keys (L1124-1165): name, attempt, outdir, receipt, launch_json {path, sha256, utc, child_pid}, spec, driver, monitor, caps, caps_basis, monitor_pid (kit L1132), m15_record, launch_check;
   - plus: host_ram_bytes, solo_mode, counted_rerun, rule_c_basis, the registry entry pin, sampler_pid, watch_pid (twin), the config pin, and the status-map sha.

## 12. raw_status and the status map (G13)

- **Composite.** `raw = <monitor status>|<driver_status or NONE>`. For CHILD_FAILED|NONE, append `|SIGNAL` if exit_code < 0, else `|EXIT`.
- **MISLAUNCH override.** Applies only if one MISLAUNCH record of this launcher binds this attempt: the same name, `attempt == k`, outdir and receipt, and, where present, `launch_json.sha256` equal to this `.launch.json` and `child_pid` equal to the monitor's.
- **TWIN_PLANNED_STOP override.** Applies only to S0_SEED_CW8_TWIN, when either:
  - a kill record exists in the launcher's `twin_kill/` with reason `ITERATION_0001_COMPLETED_AND_SIDECAR`, the same outdir and the same `launch_json.sha256`; or
  - the monitor status is `STOPPED_*`.
- **Precedence.** MISLAUNCH, then TWIN_PLANNED_STOP, then the composite.
- **The class map** is the 54-key exact-string dict of the RUNBOOK rulings entry (A223, G13). Carry it as a literal and assert its canonical-JSON sha256 (sort_keys, separators `(',', ':')`): `c36c37886aa67db763160681be99904c3ae9f22ebb51f3e841adadfa0e1cdb54`. A string not in it is UNMAPPED: P-112 reports it and the builder refuses. P-112 never maps it.
- **Builder receipt_keys.** Each role is the same-named top-level key, with status → `raw_status`.

## 13. close-attempt (G27; P-112 and S0 kit attempts)

**It writes nothing, and exits with a named code, unless all of these hold:**
- the TOOL_PIN gate (§6.1) passes;
- the run volume passes the §6.10 mount check; otherwise refuse RUN_VOLUME_NOT_MOUNTED (§10, "Run volume first");
- the monitor receipt exists and its self-hash verifies (root_monitor L203-212 logic, without re-hashing the result). If the monitor pid is gone and the receipt is absent, refuse MONITOR_ENDED_NO_RECEIPT (§10);
- exactly one LAUNCH or MISLAUNCH record of (NAME, k) exists in the launcher's `launches/`;
- for the twin, `watch_pid` is no longer a live kill-watch process;
- for P-112 attempts, `sampler_pid` has exited;
- for S0 attempts, the PLAN and fdplan mapping exists and verifies, and NAME is in the actual set or is the twin. An outside-set serial never gets a receipt;
- the outdir is a real directory, and the monitor spec sha equals the registry entry's and the V006 SPEC_PIN. Otherwise the attempt is not an attempt of the call, whether its record is a LAUNCH or a MISLAUNCH (G27 item 5): refuse NOT_AN_ATTEMPT, naming why. An attempt named in an honoured RESIDUAL_RETRY line has no monitor receipt and is never closed.
- host RAM: `sysctl` equals the LAUNCH record's `host_ram_bytes` (S0: the kit constant).

**It writes `<outdir>.attempt_receipt.json`**, schema STEP5_ATTEMPT_RECEIPT_C2V001, by exclusive create.
- **Top-level keys:**
  - raw_status; status_class (informational; c2v007 re-derives);
  - time_utc (the monitor's utc_end); launch_utc (`.launch.json` utc);
  - spec_sha256, theta_sha256, point_key;
  - rss_cap_bytes, wall_cap_s, output_cap_bytes (the monitor's caps); host_ram_bytes; other_ngc_processes_max (§9's five null cases; c2v007 recomputes it from the pinned sample);
  - call {name, kind, alternative, key}; attempt; run_dir;
  - solo_mode, counted_rerun;
  - run_volume_at_close {mount_point, mounted, free_bytes}. This is a disclosure only and never classifies (D2 reads infrastructure deaths literally).
- **pins:** monitor_receipt, launch_json, launch_record, registry_entry, solo_sample or null, stop_record or null, result (the monitor's result pin, copied and never opened) or null, status_map_sha256, config, writer.
- **date_u.**

**Then:** run the advisory terminal pre-check over the whole actual set. If this receipt completes the set, take the G24 cutoff copy:
- `cp -n` semantics (exclusive create; an existing same-sha file is accepted) of V006 to `<v006_copy_dir>/V006_CUTOFF_COPY_<sha256>.md`, then check its sha and byte count;
- write `STEP4_CUTOFF_RECORD_C2V001` with these keys: T, the pins of every terminal attempt receipt of the set, the copy {path, sha256, bytes}, the pre-check summary, date_u.
- **T is the latest time_utc over the set's terminal attempt receipts**, not this receipt's time_utc. Receipts are closed out of order: S0 receipts wait for the PLAN mapping.
- P-112 writes the cutoff record exactly once. Its pre-check is advisory: c2v007 re-derives the terminal set and T from the pinned receipts, uses its own T, and accepts the cutoff copy only if the record's date_u is at or after that T; otherwise it refuses GATE_CUTOFF_BEFORE_T. Root then records a successor cutoff record in V006, pinning the record it supersedes. That root record is the only second cutoff record allowed; P-112 never writes one.

**Custody copies.** Root, not P-112, takes the rulings' G16 custody copies of this attempt's result, monitor receipt and attempt receipt, if this attempt is terminal (rulings G16 3), once the receipt exists. P-112 takes none.

## 14. assemble-registry (G27; step 4)

- **Inputs:**
  - the config;
  - the kit entries `<s0 launch_root>/registry/<NAME>_C2V003A.json`;
  - P-112's entries;
  - the outside-set stop records;
  - the MONITOR_REFUSED records, P-112's and root's;
  - the RESIDUAL_RETRY lines in V006;
  - the attempt receipts (existence and pins only).
- **Calls in the set:**
  - every PLAN member: its P-112 entry, or the S0 entry whose kit `theta_key` equals the member's key, after the §7 checks on the kit spec;
  - F0-F2: a P-112 entry, or an S0 entry carrying that F point's key; omitted when the F point is a member's call;
  - S0_SEED_CW8_TWIN (OTHER);
  - S0 serials outside the set: excluded, each with its stop record.
- **Output:** `assembly/STEP5_LAUNCH_REGISTRY_PHASE1_CX2V001.json`, exactly `{schema: "STEP5_LAUNCH_REGISTRY_C2V003", phase: "PHASE_1", calls: [{alternative, kind, key, theta_sha256, spec_sha256}]}`. Calls are in a fixed order: members in PLAN order, then F0-F2, then the twin.
  - MEMBER: alternative PRIMARY, the v003g member_id, and the PLAN `theta_ngc` sha.
  - OTHER: alternative null, the label, and the point key.
- **Assembly record:** `STEP5_REGISTRY_ASSEMBLY_RECORD_CX2V001`. It pins every source, the PLAN output and fdplan, and V006's sha at assembly. It includes the §7 results for each S0-to-MEMBER mapping, the excluded serials, and the non-attempts (MONITOR_REFUSED; a LAUNCH or MISLAUNCH with no run directory or off-spec; each attempt named in an honoured RESIDUAL_RETRY line, with that line). A line that names an attempt with a monitor receipt is never honoured: assemble-registry refuses RESIDUAL_RETRY_NOT_RESIDUAL and writes nothing, and root rules. assemble-registry runs its residual and `absent` checks only with the run volume mounted (§10, "Run volume first").
- **`--verify`** rebuilds the STEP5 bytes from the pinned sources and byte-compares them. Root runs it before the FULL build.

## 15. Tests (synthetic only; a MUST_FAIL case for every refusal code)

**Theta, including one-ulp cases.** Use `math.nextafter`.
- **MUST_PASS:**
  - T01: an honest member and an honest F point.
  - T13: θ with 11 or more coordinates hashes stably through c2v006's `canonical_bytes`.
- **MUST_FAIL:**
  - T02: one ulp in one PLAN `theta_engine` coordinate.
  - T03: one ulp in the export `theta_natural`.
  - T04: one ulp in fdplan `theta_hex`.
  - T05: one ulp in a filled spec value, `gamma` included.
  - T06: one ulp in the spec `distance_Mpc`, and separately in `inclination_deg`.
  - T07: -0.0 against 0.0.
  - T08: a key set with an extra or a missing coordinate.
  - T09: (log_index, role, order) mismatched.
  - T10: the label key differs from the program key.
  - T11: one ulp in the kit S0 spec at assemble-registry.
  - T12: one ulp in `theta_ngc`. `theta_sha256` changes, `--verify` refuses, and c2v006 `_launch_registry` refuses LAUNCH_REGISTRY_THETA_MISMATCH.

**Status map.**
- S01 MUST_PASS: all 54 strings map as ruled; the count is 54; the dict sha is `c36c3788…`.
- S02 MUST_FAIL: an unknown driver status reads UNMAPPED.
- S03 MUST_PASS, precedence: a bound MISLAUNCH over STOPPED_WALL_CAP; a twin kill record over CHILD_FAILED|NONE|SIGNAL; STOPPED_RSS_CAP|RESULT_HASH_MISMATCH is CAP; a twin STOPPED_WALL_CAP with no kill record is TWIN_PLANNED_STOP; a serial STOPPED_WALL_CAP is CAP.
- S04 MUST_FAIL, bindings that must not apply: a MISLAUNCH record of attempt k-1; another outdir; another `launch_json` sha; a kill record with another reason or outdir.

**close-attempt.**
- C01 MUST_PASS: an honest P-112 attempt and an honest kit attempt (real-format receipts from `run_monitored` on a synthetic driver).
- C14 MUST_PASS: each of the five null cases of §9 gives `other_ngc_processes_max` null, and the receipt is still written.
- **MUST_FAIL, writing nothing:**
  - C02: no monitor receipt.
  - C03: no LAUNCH or MISLAUNCH record.
  - C04: both records exist.
  - C05: the twin's watch pid is alive.
  - C06: the sampler pid is alive.
  - C07: an S0 attempt before the PLAN mapping exists.
  - C08: an outside-set serial.
  - C09: the monitor spec differs from the registry spec.
  - C10: no outdir.
  - C11: a broken self-hash.
  - C12: a second close of the same attempt.
  - C13: host RAM differs.

**Cutoff.**
- G01 MUST_PASS: when the receipt that completes the set is not the one with the latest time_utc, the cutoff record's T is the latest time_utc over the set.
- G02 MUST_FAIL: P-112 writing a second cutoff record. (Root's single successor record on GATE_CUTOFF_BEFORE_T is outside P-112.)

**Sampler and solo mode.**
- P01 MUST_PASS: a byte copy of a listed tool under another path is counted, by sha; monitor, dry harness, `driver dry-run`, kill watch and the own tree are not counted. The values writer v004 and handoff c2v003a rows are counted.
- P02 MUST_FAIL: a gap > 2 × poll gives null.
- P03 MUST_FAIL: a killed sampler gives null.
- P04 MUST_FAIL: solo mode refuses with a listed process alive.
- P05 MUST_FAIL: a second launch refuses during a solo rerun, and during a solo REFUSED/BLOCKED retry.
- P06 MUST_FAIL: `complete` false, floor(first_utc) ≥ utc_start, and floor(last_utc) ≤ utc_end each give null.
- P07 MUST_PASS: when the monitor exits with no `.launch.json`, the sampler stops and writes nothing at `<outdir>.solo.json`.
- P08 MUST_FAIL: a first sample in the same whole second as utc_start, taken before the monitor started, gives null; so does a last sample in the same whole second as utc_end.
- P09 MUST_PASS: with the 1 s lead before the monitor starts and the 1 s tail after the receipt exists, the attempt is counted (`other_ngc_processes_max` is 0, not null), and recomputing it from the pinned sample gives the same value.

**Caps and disk.**
- K01 MUST_PASS: rerun caps for a serial and the twin; an INFRA retry repeats the replaced attempt's caps and solo mode; a REFUSED or BLOCKED retry repeats the caps in solo mode; a serial OUTPUT_CAP rerun doubles the output cap.
- K02 MUST_FAIL: free space of 292 GiB − 1 B refuses an OUTPUT_CAP serial rerun, and exactly 292 GiB passes.
- K03 MUST_FAIL: twin RSS at RAM.
- K04 MUST_FAIL: serial RSS at RAM × 11.
- K05 MUST_FAIL: a twin OUTPUT_CAP rerun (a twin STOPPED_OUTPUT_CAP is TWIN_PLANNED_STOP; refuse ATTEMPT_AFTER_TERMINAL).

**Numbering and ownership.**
- N01 MUST_PASS: kit A1 MISLAUNCH and A2 LAUNCH give P-112 k = 3.
- N02 MUST_PASS: the kit's ATTEMPT_RE, loaded from kit bytes, matches none of P-112's filenames, and the kit's `attempt_records` and `order-check` output on a synthetic kit launch root is unchanged after P-112 runs.
- N03 MUST_FAIL: any write path inside the kit's `launches/`.
- N04 MUST_PASS: MONITOR_REFUSED at k, then a relaunch at k. The existing same-spec registry entry is admitted (ALREADY_REGISTERED_SAME_SPEC) and no new entry is written; the two invocations use different work directories; the relaunch finds no `<outdir>.solo.json`.
- N05 MUST_FAIL: a second refusal at k (MONITOR_REFUSED_TWICE): `record-monitor-refused` refuses and writes nothing. MUST_PASS: P-112 does not hold the call; a further launch at k is admitted as the first relaunch was (holding it is root's procedure).
- N06 MUST_FAIL: a launch after a terminal attempt.
- N07 MUST_PASS: a first attempt reading CHILD_FAILED|REFUSED (not solo) gives a solo retry at the same caps; two solo retries with the same status make the call terminal, UNEVALUATED_INFRA_REPEAT, at [2, 3]; a third retry is refused with ATTEMPT_AFTER_TERMINAL. The same holds for BLOCKED.
- N08 MUST_FAIL (not terminal): REFUSED then BLOCKED; a pair with one non-solo attempt or a null sample; a pair with different caps; a pair separated by a MISLAUNCH attempt that has a run directory.
- N09 MUST_FAIL: a first attempt with an existing registry entry of another spec (REGISTRY_ENTRY_EXISTS_FOR_ANOTHER_SPEC), or with an existing entry and a LAUNCH or MISLAUNCH record for NAME.
- N10 MUST_PASS: a root-written kit MONITOR_REFUSED record is accepted. MUST_PASS: a root-written kit record at k = 1 is followed by a synthetic kit relaunch at k = 1 with a LAUNCH record and a receipt; `status` and `assemble-registry` accept the record and list the refusal as a non-attempt. MUST_FAIL: the same record with an extra key, a missing `receipt_stdout` or `receipt_stderr` key, a pin that does not match its bytes, or an `absent` path that exists while no relaunch at k has started. MUST_FAIL: with `<outdir>.receipt.json.stdout.txt` or `.stderr.txt` present and no `.launch.json` (a synthetic monitor that dies after root_monitor L143-144), `record-monitor-refused` refuses MONITOR_STARTED_NO_LAUNCH_JSON and writes nothing, and neither file is opened.
- N11 MUST_FAIL: P-112 launching an S0 call that has a kit MISLAUNCH and no kit LAUNCH record or P-112 attempt (KIT_RELAUNCH_OWNS). MUST_PASS: once the kit LAUNCH record exists, P-112 owns the rerun.
- N12 MUST_PASS: a P-112 first attempt at k = 1 ends in a MISLAUNCH stopped before the outdir existed. close-attempt refuses NOT_AN_ATTEMPT; the next legal attempt is a retry at k = 2 with first-attempt caps and the same solo mode, §6.12 admits it (the MISLAUNCH is a non-attempt whose monitor receipt exists), §6.13 does not apply, and no new registry entry is written. The same after a non-attempt MISLAUNCH of a solo rerun: the retry repeats its caps and solo mode.
- N13 MUST_PASS: a MISLAUNCH with no run directory does not separate an INFRA_REPEAT pair: solo REFUSED, a non-attempt MISLAUNCH, solo REFUSED (identical spec and caps) is terminal, UNEVALUATED_INFRA_REPEAT.
- N14 MUST_FAIL: a synthetic monitor is killed after `.launch.json`, so no receipt is written. The sampler exits and writes no `<outdir>.solo.json`; close-attempt refuses MONITOR_ENDED_NO_RECEIPT and writes nothing; `status` reports MONITOR_ENDED_NO_RECEIPT; the next launch of the call refuses MONITOR_ENDED_NO_RECEIPT; the audit hook (V03) shows that nothing under the outdir is opened. The same holds when the record's `monitor_pid` belongs to a live, unrelated process (a synthetic `sleep`): it does not count as the monitor. Then, MUST_PASS: with a `RESIDUAL_RETRY <NAME> <k>` line, the next legal attempt is a retry at k+1 with attempt k's caps and solo mode and no new registry entry. MUST_FAIL: that retry refuses RESIDUAL_ATTEMPT_PROCESS_ALIVE while a synthetic orphan runs the planned driver command (`run --spec <spec> --outdir <outdir of k>`), and is admitted once it exits. MUST_FAIL: a line naming an attempt that has a monitor receipt refuses RESIDUAL_RETRY_NOT_RESIDUAL. MUST_FAIL: a malformed line (`RESIDUAL_RETRY P1_M0001 01`) refuses RESIDUAL_RETRY_MALFORMED.
- N15 MUST_PASS: a call with k = 1 run beside another listed process (sample 1), FAILED X; k = 2, a solo rule-(c) rerun, FAILED X; k = 3, a rule-(c) rerun, INFRA; k = 4, a solo INFRA retry at rerun caps, FAILED X. It is not terminal: attempts 2 and 4 never form a pair (attempt 3 separates them), c2v006 `_rule_c_problem` reads RULE_C_INCOMPLETE on attempts 3 and 4, and the next legal attempt is a rule-(c) rerun at k = 5.
- N16 MUST_PASS: a kit call, S0_J0_SERIAL (the kit holds the seed's LAUNCH record), with MONITOR_STARTED_NO_LAUNCH_JSON at k = 1: no kit record, the receipt's stdout and stderr exist, no `.launch.json`. Without a line, the launch refuses MONITOR_STARTED_NO_LAUNCH_JSON. With `RESIDUAL_RETRY S0_J0_SERIAL 1`, the next legal attempt is a P-112 retry at k = 2 with the kit's first-attempt caps, not solo, on the kit registry entry's spec, with no new registry entry and no KIT_RELAUNCH_OWNS. The same holds for a kit MISLAUNCH at k = 1 whose monitor was stopped (no receipt). MUST_FAIL: the same for S0_SEED_SERIAL with no kit seed LAUNCH record refuses (§6.2).
- N17 MUST_PASS: a synthetic driver that exits 1 before creating its outdir at k = 1 and, separately, one killed by a signal there. Each gives a LAUNCH record; close-attempt refuses NOT_AN_ATTEMPT; the next legal attempt is a retry at k = 2 with first-attempt caps and the same solo mode, with no new registry entry (§6.13 does not apply; §6.12 admits it). The same holds for a kit LAUNCH at k = 1: P-112 owns the retry, with no KIT_RELAUNCH_OWNS.
- N18 MUST_PASS: a synthetic monitor still alive with no `.launch.json` at the launch bound. P-112 checks its command line (root_monitor and this receipt), sends TERM, KILL after 15 s, and waits for it to exit. (a) If `.launch.json` then exists, kill-target, run without `--mon-pid`, stops the synthetic driver, a MISLAUNCH record is written, and the attempt reads MONITOR_ENDED_NO_RECEIPT. (b) If not, and the receipt's stdout or stderr exists, `record-monitor-refused` refuses MONITOR_STARTED_NO_LAUNCH_JSON and writes nothing. (c) If neither exists, a MONITOR_REFUSED record is written. MUST_FAIL: a live pid whose command line does not name root_monitor and this receipt is not signalled. MUST_FAIL: with `.launch.json` absent and the monitor alive, no MISLAUNCH record is written before the monitor is stopped.
- N19 MUST_FAIL: with the synthetic run volume absent (the mount check injected; no test touches `/Volumes`), `status` and close-attempt report RUN_VOLUME_NOT_MOUNTED, not MONITOR_ENDED_NO_RECEIPT, for a finished attempt whose receipt sits on that volume; record-monitor-refused, assemble-registry and launch refuse RUN_VOLUME_NOT_MOUNTED and write nothing; the sampler does not stop on its 60 s rule. After the volume is restored, the attempt closes normally. assemble-registry refuses RESIDUAL_RETRY_NOT_RESIDUAL for a line that names an attempt with a receipt.

**Launch condition (D8).**
- L01 MUST_FAIL: no `TOOL_PIN P112_LAUNCHER_CX2V001` line.
- L02 MUST_FAIL: that line with another sha, or another realpath.
- L03 MUST_FAIL: two `TOOL_PIN P112_LAUNCHER_CX2V001` lines.
- L04 MUST_PASS: dry mode and `status` work without it.
- L05 MUST_PASS: an added `TOOL_PIN P112_LAUNCHER_CX2V002 …` line is ignored.
- L06 MUST_FAIL: close-attempt, assemble-registry, stop-outside-set and record-monitor-refused each refuse without the line, and write nothing.
- L07 MUST_PASS: a V006 that holds the rulings entry's text verbatim plus one valid `TOOL_PIN P112_LAUNCHER_CX2V001` line passes; the entry's mid-line mentions of TOOL_PIN and RESIDUAL_RETRY are not lines. MUST_FAIL: a line beginning `TOOL_PIN P112_LAUNCHER_CX2V001` that does not match the grammar (an upper-case sha, or a relative path) refuses TOOL_PIN_MISMATCH.

**Outside-set stop.**
- O01 MUST_FAIL: the target is in the set.
- O02 MUST_FAIL: kill-target refuses.
- O03 MUST_PASS: a synthetic outside-set process is stopped and recorded, and nothing is opened.

**Registry and interfaces.**
- R01 MUST_PASS: c2v006 `_launch_registry` (bytes `0cc73106`) accepts the assembled file.
- R02 MUST_PASS: c2v006 `_receipt` reads all nine roles from an attempt receipt. This test places the receipt inside run_dir; disclose that the true residence `<run_dir>.attempt_receipt.json` refuses RECEIPT_NOT_IN_RUN_DIR under c2v006 and needs c2v007, a root build.
- R03 MUST_FAIL: `--verify` after one changed byte.
- R04 MUST_PASS: an outside-set serial is excluded and listed.

**Paths and validity.**
- V01 MUST_FAIL: an `ngc3198` component in the run root, the fill_dir or an argv element.
- V02 MUST_FAIL: `runs_ext` spelling.
- V03 MUST_PASS: an audit hook (`sys.addaudithook` on `open`) shows P-112 never opens `result.json`, `finish.json`, `progress.jsonl` or anything under an outdir. A sentinel value in a synthetic `result.json` appears in no byte P-112 writes or prints.
- V04 MUST_FAIL: synthetic mode naming the real driver, the real monitor name, or `/Volumes`.

**Record runs.** Run the suite twice, as RUN1 and RUN2. The TEST_RECORD files must be byte-identical.

**Mutants.** Report at least these, killed:
- a wildcard map key;
- swapped precedence;
- an unbound MISLAUNCH;
- an ignored sampler gap;
- an undoubled rerun wall;
- twin RSS at RAM;
- numbering restarted at 1;
- θ compared with `==` instead of `float.hex` (T07);
- the disk check off by one;
- close-attempt writing before the PLAN mapping exists;
- the INFRA_REPEAT pair requiring rule-(c) caps (N07);
- T taken from the completing receipt (G01);
- the TOOL_PIN gate on launch only (L06);
- a REFUSED retry not in solo mode (K01);
- sample times compared without floor() (P08);
- a retry after a non-attempt MISLAUNCH treated as a first attempt (N12);
- a retry rule checked before the terminal conditions (N07);
- the rule-(c) pair taken over non-consecutive attempts (N15);
- a monitor that ended without a receipt left unreported, with the sampler still waiting (N14);
- a RESIDUAL_RETRY line honoured for an attempt that has a monitor receipt, or while the planned driver command still runs (N14);
- the k of a RESIDUAL_RETRY line left out of numbering (N16);
- a non-attempt LAUNCH (no run directory) treated as an attempt, or left with no next legal attempt (N17);
- kill-target given `--mon-pid` after the monitor was stopped (N18);
- a MISLAUNCH record written for an absent `.launch.json` while the monitor is alive (N18);
- TOOL_PIN or RESIDUAL_RETRY matched unanchored (L07);
- an `absent` path re-checked after the same-k relaunch started (N10);
- a residual or `absent` decision made with the run volume unmounted (N19);
- a RESIDUAL_RETRY line honoured at assemble-registry for an attempt that has a monitor receipt (N19).

## 16. Deliverables (in the output folder)

- `phase1_ngc_launch_cx2v001.py`, the tool, with the subcommands of §1.
- `README_PHASE1_NGC_LAUNCH_CX2V001.md`, with every claim labelled TESTED, FORMAL or UNTESTED, and a deciding test named for each UNTESTED claim.
- `test_phase1_ngc_launch_cx2v001.py`.
- `test_records_cx2v001/RUN1`, `test_records_cx2v001/RUN2`.
- `INTERFACE_PROOF_CX2V001.json`.
- `HASHES_CX2V001.txt`, with every sha computed from bytes.

Report to root through the exchange with the HASHES sha. Root forwards the build to Claude4.

**UNTESTED items to name, with their deciding tests:**
- the real driver statuses on a real attempt: the first real close-attempt;
- the PLAN `theta_engine` key set against the export and fdplan forms: the first θ check on the real PLAN output;
- the sampler on the production machine: the first P-112 attempt;
- the run volume's free space for 292 GiB: the launch check;
- a real kill watch run under `p112_launch_root`: the first twin rerun, if one ever happens;
- acceptance of a real root-written MONITOR_REFUSED record: the first kit monitor refusal, if one ever happens;
- MONITOR_ENDED_NO_RECEIPT after a real host restart or volume loss: the first such event, if one ever happens;
- a real monitor still alive with no `.launch.json` at the launch bound: the first such event, if one ever happens.
