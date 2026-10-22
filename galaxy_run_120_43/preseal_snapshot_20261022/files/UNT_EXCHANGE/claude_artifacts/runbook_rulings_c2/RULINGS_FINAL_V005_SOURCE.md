## @ANUM@: RUNBOOK rulings G13, G15, G25, G27, G7, G16, G24; 0237 N1/N3; 0248 VN1/DN5 (@T@)

**Why.** P-112, the Phase-1 NGC member/F launcher, starts on these rulings (A205 item 8). Its other precondition, the P-117 record, is met (A210). The S0 launch needs the receipt status map named before its first launch (RUNBOOK L140), so this entry stands before the S0 M-15 record. No ruling here changes a registered method, threshold, prereg text or sealed object, except the disclosed pre-result registrations under A133 §3 (L201): DN5, UNEVALUATED_INFRA_REPEAT and UNEVALUATED_CUSTODY_BREACH. Where a ruling reads registered text, it is listed under "Disclosed readings". This is the RUNBOOK rulings entry A210 item 2 names; A211 to the entry before this one were written before it.

**Source.** Root workflow wf_16e496bf: a drafter and two refutation lenses (physics/blinding: 8 AMEND, 5 HOLDS; implementation: 9 AMEND, 3 HOLDS). Every AMEND fix is applied; where the lenses differ, the stricter or more explicit one is taken (root decisions D1-D15). Two fixes are not taken:
- both lenses proposed moving some infrastructure deaths out of FAILED; D2 reads them literally instead (G13);
- lens 1's G13 fix 3 (the twin reading TWIN_NOT_USED, with the kit retrying INFRA twin attempts) is replaced by D3's twin mode (G25 item 8).

Root workflow wf_bbfb82d5 then checked the synthesis against the sources and found 15 defects. Each is fixed in this entry. A second check of that version found 10 more (the custody successor's form, the custody-copy timing, the sampler's time comparison, the cutoff's T, a non-attempt MISLAUNCH, D7's edge cases, the next-attempt order, and stale citations, lineage and stamp). Each is fixed here too. A third check found 4 more (a monitor that ends without writing its receipt, the brief's reading of the rule-(c) pair, V006 entry spans that go stale before insertion, and the brief's custody-copy scope), and each is fixed here as well. A fourth check found 5 more (no machine form for root's ruling on a residual, a LAUNCH with no run directory, a monitor still alive with no .launch.json at the launch bound, the TOOL_PIN line's grammar, and the undefined sample flag `complete`), and each is fixed here as well. A fifth check found 7 more (a root-written MONITOR_REFUSED record that fails its own acceptance after the same-k relaunch, residual checks run with no mount check, a hold after a second monitor refusal that nothing enforces, an absent `.launch.json` caught by the mismatch rule, NGC tools adopted after A212 and before this entry, a stale V006 citation, and small text fixes), and each is fixed here as well.

**Read.** RUNBOOK_V002_C2V006 `e162db3e`; builder c2v006 `0cc73106`; root_monitor_c2v001 `ba031c23`; driver cx3r008 `577f8c94` on its live path (cmd_run L9208 → _ngc_v011_dispatch L9194 → strict clone L8989-9102); S0 kit C2V003A `fdc0ee6c`, serial script `621263a2`, twin script `f199544d`, kill watch `a3d70bec`, record writer `a10965b7`; phase1 v003b `7d891ff7`; orchestrator c2v005 `c75a889f`; filler `ec417e76`; A133 `cd92ef91`; r3a sc3 `c64f65a3`; V006 `6565c973` (285,659 B, through A221; last written at 16:43:44Z by its modification time, and unchanged at 16:45:14Z, 16:58:10Z, 16:59:21Z and 17:08:48Z; it was `339458c5`, 284,051 B, through A220, at 16:43:13Z). A205-A219 read by heading at 15:57:53Z, A220 at 16:43:13Z, and A221 at 16:59:21Z. V006 ends with an unnumbered, unstamped heading, `## A108 continued`, after A221; it was read by heading only, and its content is not checked here. At insertion, root reads by heading every entry added after A221, and that heading, confirms that none changes a ruling here, and updates the V006 sha and these spans. A210 (phase1 v003b), A211 (the NGC acceptance stack and N3) and A212 (values writer v004) are used below; A213-A221 change no ruling here. By heading, A220 is the S4-R-A1 fix (apply_h3_fields_c2v004; failed at A221), and A221 records Codex1 0162's FAIL of it and commissions a c2v005 successor. The tools built or adopted at A213-A221 are not NGC launch-path tools: registry_assembler_c3v005 is the S4-R-C1 calibration certificate registry and offline verifier, and apply_h3_fields_c2v004 applies the H3 fields to a DDO154 calibration RUN_CONFIG (from their paths and docstrings).

Not opened, except as disclosed next: any NGC3198 target, observed-velocity, sigma or slots file; run outputs; V007_POSTSEAL_RECORDS; ~/.codex.

Disclosure from the fixer round: a sha search ran `shasum` over the JSON files up to depth 4 under claude_artifacts before it was stopped. It may have read the bytes of NGC3198-named files, slots V003 among them. It printed four sha lines and no file content. The four were ROOT_TSR_FLAG_RECORD_V001, the two carrier policies and the K32 compare.

**Finding (TESTED on synthetic records shaped like the real ones).** Builder c2v006 cannot build from the real Phase-1 records:
- root_monitor nests the spec sha and caps and writes no θ, host RAM or solo value. c2v006 reads top-level keys only, so every receipt refuses RECEIPT_CALL_BINDING_MISSING, a FINISHED one included.
- The monitor receipt is the sibling `<outdir>.receipt.json`. c2v006 requires it inside run_dir, so it refuses RECEIPT_NOT_IN_RUN_DIR.
- The kit's M-15 record UNT_M15_PRELAUNCH_RECORD_C2V001 refuses INPUT_KEY_MISSING.

The S0 kit's records stay the records of record. A post-run attempt receipt (G27) and builder c2v007 adapt to them. The S0 kit needs no change.

### G13: the call set, the Phase-2 sensitivity registration, the status map

**Question.** RUNBOOK L402-405: which calls step 4 waits for; how Phase-2 sensitivity entries are registered; the one status map per receipt producer.

**Ruling.**
1. **The Phase-1 call set** (A133 L77-90):
   - the PRIMARY members, kind MEMBER;
   - F0, F1 and F2, kind OTHER. An F point at a member's exact θ is that member's call (A133 L86);
   - the identity twin S0_SEED_CW8_TWIN, kind OTHER. Its planned stop is its terminal.
   - An S0 serial whose θ is neither a member's nor an F point's is outside the set. It is not registered and never read, and step 4 does not wait for it. Root stops it as soon as the set is fixed at u_A (G25 item 7).
   - Step 4 begins when every call of the set has a terminal attempt receipt (A133 L210).
2. **The Phase-2 sensitivity registration** is RUNBOOK §3 2c, with two exceptions:
   - an entry at an (alternative, θ) that already has any registered call is that call. It is registered as SENSITIVITY with that call's spec sha and a call record identical to that call's, and it is not relaunched;
   - an A16.4 entry (VN1) is never launched or registered.
3. **The status map** for root_monitor_c2v001, read through the attempt receipt (G27).
   - **Raw status** = `<monitor status>|<driver_status or NONE>`, both taken from the monitor receipt. CHILD_FAILED with no driver status gains `|SIGNAL` (exit_code < 0) or `|EXIT` (otherwise).
   - **Overrides, in this order:** MISLAUNCH, then TWIN_PLANNED_STOP, then the composite string.
     - MISLAUNCH applies only for a MISLAUNCH record bound to this attempt: the same name, attempt k, outdir and receipt, and, where the record carries them, the same .launch.json sha and child_pid.
     - TWIN_PLANNED_STOP applies only to S0_SEED_CW8_TWIN, for a kill record bound to this attempt (reason ITERATION_0001_COMPLETED_AND_SIDECAR, the same outdir, the same .launch.json sha) or for any STOPPED_* monitor status (A141 L4).
     - MONITOR_REFUSED is the launch-side status of a monitor that refused and wrote nothing (D7; G27 item 5).
   - **One exact-string dict, 54 keys, no wildcards.** A STOPPED_<cap> monitor status wins over every driver-side value.
     ```
     FINISHED      FINISHED|COMPLETED  FINISHED|COMPLETED_INVALID
     FAILED        CHILD_FAILED|FAILED  CHILD_FAILED|FAILED_AT_STAGE  CHILD_FAILED|ROUTE_A_NO_FIXED_POINT
                   CHILD_FAILED|NONE|EXIT
     CAP           STOPPED_WALL_CAP|COMPLETED  STOPPED_WALL_CAP|COMPLETED_INVALID  STOPPED_WALL_CAP|FAILED
                   STOPPED_WALL_CAP|FAILED_AT_STAGE  STOPPED_WALL_CAP|ROUTE_A_NO_FIXED_POINT  STOPPED_WALL_CAP|REFUSED
                   STOPPED_WALL_CAP|BLOCKED  STOPPED_WALL_CAP|UNREADABLE_FINISH  STOPPED_WALL_CAP|RESULT_HASH_MISMATCH
                   STOPPED_WALL_CAP|NONE
                   STOPPED_RSS_CAP|COMPLETED  STOPPED_RSS_CAP|COMPLETED_INVALID  STOPPED_RSS_CAP|FAILED
                   STOPPED_RSS_CAP|FAILED_AT_STAGE  STOPPED_RSS_CAP|ROUTE_A_NO_FIXED_POINT  STOPPED_RSS_CAP|REFUSED
                   STOPPED_RSS_CAP|BLOCKED  STOPPED_RSS_CAP|UNREADABLE_FINISH  STOPPED_RSS_CAP|RESULT_HASH_MISMATCH
                   STOPPED_RSS_CAP|NONE
     OUTPUT_CAP    STOPPED_OUTPUT_CAP|COMPLETED  STOPPED_OUTPUT_CAP|COMPLETED_INVALID  STOPPED_OUTPUT_CAP|FAILED
                   STOPPED_OUTPUT_CAP|FAILED_AT_STAGE  STOPPED_OUTPUT_CAP|ROUTE_A_NO_FIXED_POINT  STOPPED_OUTPUT_CAP|REFUSED
                   STOPPED_OUTPUT_CAP|BLOCKED  STOPPED_OUTPUT_CAP|UNREADABLE_FINISH  STOPPED_OUTPUT_CAP|RESULT_HASH_MISMATCH
                   STOPPED_OUTPUT_CAP|NONE
     INFRA         CHILD_FAILED|REFUSED  CHILD_FAILED|BLOCKED  CHILD_FAILED|NONE|SIGNAL  CHILD_FAILED|UNREADABLE_FINISH
                   CHILD_FAILED|RESULT_HASH_MISMATCH  CHILD_FAILED|COMPLETED  CHILD_FAILED|COMPLETED_INVALID
                   FINISHED|NONE  FINISHED|UNREADABLE_FINISH  FINISHED|RESULT_HASH_MISMATCH  FINISHED|FAILED
                   FINISHED|FAILED_AT_STAGE  FINISHED|ROUTE_A_NO_FIXED_POINT  FINISHED|REFUSED  FINISHED|BLOCKED
                   MISLAUNCH  MONITOR_REFUSED
     PLANNED_STOP  TWIN_PLANNED_STOP
     ```
   - The dict as canonical JSON (`{string: class}`, sort_keys, separators `(',', ':')`, 2,052 bytes) has sha256 `c36c37886aa67db763160681be99904c3ae9f22ebb51f3e841adadfa0e1cdb54`. P-112 and c2v007 carry it and assert this sha. Root passes it as `receipt_status_classes`.
   - Any other string is unmapped: the builder refuses RECEIPT_STATUS_UNMAPPED, and root rules it. The driver's live path writes only seven statuses (L9002-9102), so this cannot arise from the pinned driver.
   - **Infrastructure deaths are read literally (D2).** Some infrastructure deaths surface as FAILED: a signalled stage gives FAILED_AT_STAGE (Ctx.run_stages L1864), a caught OSError or MemoryError (a full disk, or a lost volume, when the monitor's receipt is still written; otherwise MONITOR_ENDED_NO_RECEIPT) gives FAILED, and a failed result write gives NONE|EXIT. All three read FAILED. A lost or full run volume can also stop root_monitor writing the receipt itself (`_write_x`, L199; the receipt sits beside the outdir on that volume). That attempt has no status: it is MONITOR_ENDED_NO_RECEIPT, a residual (below). The guard is rule (c) itself: a solo rerun at the doubled wall first, and two identical counted solo failures before a member is invalid.
   - **Repeated deterministic refusals.**
     - An attempt that reads CHILD_FAILED|REFUSED or CHILD_FAILED|BLOCKED is retried in solo mode (G25 item 5), at the caps of the attempt it replaces.
     - Two consecutive attempts of the call that are both solo (solo mode, and other_ngc_processes_max = 0), with identical spec, identical caps and the identical raw status CHILD_FAILED|REFUSED, or CHILD_FAILED|BLOCKED, are terminal with disposition UNEVALUATED_INFRA_REPEAT: FREEZE_INCOMPLETE, never MEMBER_INVALID. Non-attempts (G27 item 5) do not separate the two.
     - A refusal on a first attempt therefore becomes terminal after at most two solo retries.
     - Every other INFRA string is retried with no count limit and no deadline (A133 §3).
     - The status map leaves no judgment point open. Three residuals remain, and all three go to root (disclosed reading 19). Two are D7's: a second monitor refusal at the same attempt number, and a monitor that started but wrote no .launch.json (MONITOR_STARTED_NO_LAUNCH_JSON). The third is MONITOR_ENDED_NO_RECEIPT: the monitor pid is gone and the receipt is absent (process rulings). Each is decided only with the run volume mounted (process rulings, "Run volume first"). No value is read in any of them, and the outdir is never opened. Root's ruling on MONITOR_STARTED_NO_LAUNCH_JSON or MONITOR_ENDED_NO_RECEIPT has one machine form, the RESIDUAL_RETRY line (process rulings).
   - **Cost (the draft's "one rerun" corrected).** A counted pair can start at attempt 1 only if attempt 1 was sampled solo with no other process. No S0 first attempt has a sample, and P-112 first attempts run beside other calls. So a failing call normally needs two solo reruns at the doubled wall, up to 1,220,648 s each for a serial (see Schedule risk).

**Evidence.** A133 `cd92ef91` L77-90, L103, L107-111, L201, L210-211, L216-219; RUNBOOK L94, L140, L163, L258, L402-405; driver `577f8c94` L9002-9102 (exit 0 only for COMPLETED and COMPLETED_INVALID, L9102), L1858-1864; root_monitor `ba031c23` L133 (a refusal writes nothing), L147, L177-197; kit `fdc0ee6c` L970-982 (kill record), L1096-1173 (MISLAUNCH record); twin script `f199544d` L188-191 (watch_pid); A141 L4; c2v006 L581-601, L1052-1055, L1111-1116, L1133-1136; probe (TESTED): a `STOPPED_WALL_CAP|*` key leaves `STOPPED_WALL_CAP|NONE` unmapped.

**Implements.** P-112: raw status, the bindings and the map in close-attempt; the solo retry of REFUSED and BLOCKED attempts; assemble-registry builds the set. c2v007: re-derives the raw status (G27) and adds the UNEVALUATED_INFRA_REPEAT pair as defined above. Root: passes the dict. S0 kit: no change.

**Blocks.** The S0 first launch (the map must be in V006 before the M-15 record); P-112's start; Phase-1 step 4.

### G25: rule-(c) evidence

**Question.** RUNBOOK L415: the receipt keys for the evidence roles, and four readings of A133 §3(c).

**Ruling.**
1. **Keys.** Each of the nine roles is the same-named top-level key of the attempt receipt (G27), written by machine:
   - status = `raw_status`;
   - time_utc = the monitor's utc_end;
   - spec_sha256 = the monitor's pins.spec.sha256;
   - rss_cap_bytes, wall_cap_s and output_cap_bytes = the monitor's caps;
   - theta_sha256 (G27);
   - host_ram_bytes = `sysctl -n hw.memsize`, read at launch and again at close. For S0 kit attempts it is the kit constant 137,438,953,472, checked against sysctl at close;
   - other_ngc_processes_max = the attempt's process sample (item 4). It is null when no valid sample exists, and an attempt with a null sample can never be a counted attempt.
2. **The four readings.**
   1. Confirmed: "with no other NGC process running" applies to both counted failures (A133 L217-218).
   2. Confirmed: "at RAM" means equal to host_ram_bytes. For the identity twin, "at RAM" means 11 × host_ram_bytes, its A172 N4 cap (D3). If A177 R1 ever raises a serial's cap to RAM × n, root re-rules this reading before that call's rerun.
   3. Confirmed: "doubled" means exactly 2 × the call's first attempt's wall cap, on every counted rerun.
   4. Replaced: "identical" means the identical composite raw status (G13), not the monitor status alone.

   The pair is the one c2v006 reads, unchanged (`_rule_c_problem` L660-694; `_terminal` R1, L725-731): the last two attempts of the call, non-attempts excluded (G27 item 5). An attempt of any class between two failures separates them.
3. **"Other NGC process" (D5).** A process counts if its argv names a tool on a declared list, matched by realpath or by the sha256 of the named file:
   - the driver `577f8c94` with subcommand `run` or `_stage`;
   - the NGC point certificate producers: eps_ngc_point_c4v002 `8972822b`, gq_binding_c4v002 `f4ee064d`;
   - the NGC ρ c3v003 producer `d3d0f3dd`, stage `496d2a21` and slot proof `ada31d12`;
   - the NGC acceptance stack of record (A211): LO state adapter c2v003a `9c4b6dfc`, handoff c2v005 `7077ad93`, roster recipes c2v002 `c700f469`;
   - handoff c2v003a `7c54fd6f`, kept on the list as the stricter reading of D5;
   - values writer v004, cx2v002 `26319ecb` (A212);
   - the carrier extractors: cx3v005 `50c7db5f`, c2v001 `8acd21c7`.

   A211 names the stack's adapter as the LO state adapter c2v003a, which settles the ambiguity in A205 item 6. Not counted: root_monitor, the dry harness and the driver's `dry-run` subcommand (driver L4981), the sampler, the kill watch, and the attempt's own process tree. The list is a P-112 constant, and only a V006 entry can change it.
4. **Sampler coverage.** The sampler takes its first sample at least 1 s before P-112 starts the monitor, and a final sample at least 1 s after the monitor receipt exists. It polls at most every 10 s and records n_samples, poll_s and the largest gap. If the monitor pid is gone and no receipt has appeared 60 s later, it stops and writes nothing at the outdir path (MONITOR_ENDED_NO_RECEIPT). The 60 s are counted only while the run volume is mounted; while it is unmounted, the sampler keeps polling and decides nothing (process rulings, "Run volume first"). Sample times carry sub-second precision. The monitor's utc_start and utc_end are whole seconds (root_monitor L43-44), so the comparison is in whole seconds: floor() of a sample time against the receipt's value. other_ngc_processes_max is null in each of these five cases:
   1. the sampler died, or its sample file is absent;
   2. the sample's `complete` is false. `complete` is true if and only if every poll's `ps` call exited 0 and parsed, and the sampler ended by the normal-end rule (monitor gone, receipt exists, final sample at least 1 s after it);
   3. the largest gap exceeds 2 × poll_s;
   4. floor(first sample time) is not earlier than the monitor receipt's utc_start (null unless floor(first) < utc_start);
   5. floor(last sample time) is not later than the monitor receipt's utc_end (null unless floor(last) > utc_end).

   With the 1 s lead and the 1 s tail, cases 4 and 5 cannot fire on an honest attempt. Without them, a first sample in the same second as the start, but before it, would read "after", and the attempt would never count (a false null, costing a rerun of about 14 days). P-112 and c2v007 compare in exactly this way. Tests: a same-second first sample gives null (MUST_FAIL); with the 1 s lead, the attempt is counted (MUST_PASS).

   A ps poll can miss a short process, so the count is a lower bound; the guarantee is the hold rule (item 5).
5. **Hold rule.** A counted rerun, or a solo retry (G13), starts only when no listed process is alive. While it runs:
   - P-112 starts nothing;
   - root starts no S0 kit call, twin or other listed process;
   - root starts no NGC tool that is not on the list, whenever it was adopted (the list reflects adoptions through A212). Such a tool joins the list only by a V006 entry.
6. **Caps** (a process choice, A141 L1).
   - A rule-(c) rerun has identical spec bytes, RSS at RAM (twin: RAM × 11) and wall = 2 × the first attempt's: 1,220,648 s for a serial, 45,504 s for the twin.
   - An OUTPUT_CAP rerun also has output = 2 × the first attempt's. The identity twin never has one: any STOPPED_* twin status is TWIN_PLANNED_STOP, which is terminal.
   - An INFRA or MISLAUNCH retry repeats the caps and the solo mode of the attempt it replaces. A REFUSED or BLOCKED retry repeats the caps and always runs solo (G13).
7. **Outside-set S0 serials (D4).** Root stops each one as soon as the set is fixed at u_A. The stop runs the kill-target checks and writes a stop record by exclusive create. Outputs are kept and never read (A133 L103). After that, no outside-set serial can hold up a solo rerun.
8. **Ownership (D3, D6).**
   - P-112 owns the rule-(c) and INFRA reruns of every Phase-1 NGC call, the S0 serials and the identity twin included (a twin mode at the twin's caps). This supersedes A161 N3's on-demand kit successor.
   - **The kit's own relaunches stay with the kit.** For an S0 call, the kit relaunches after its own MISLAUNCH (order-check L737-791; MISLAUNCH record L1160), and the D7 relaunch at the same k after a monitor refusal also goes through the kit. The kit keeps both until the call has a LAUNCH record, a P-112 attempt or a RESIDUAL_RETRY line (process rulings).
   - Once P-112 launches any attempt of a call, every later attempt of that call is P-112's. Its attempt numbers continue after the kit's.
   - P-112 never writes into the kit's launches directory. It reads the kit's records there.

**Evidence.** root_monitor `ba031c23` L43-44 (whole-second utc), L140-149 (utc_start taken at L146, before Popen), L192-198; c2v006 L591-601, L643-694 (L677-680 always check attempt 0); kit `fdc0ee6c` L613-645 (register), L737-791 (order-check). Probes (TESTED):
- an S0 first attempt with no sample refuses RULE_C_EVIDENCE_MISSING;
- a call with a non-solo first attempt and two solo reruns at 2× wall reaches the terminal pair [1, 2];
- a twin pair at RAM × 11 refuses RULE_C_RERUN_CAPS under c2v006.

Also A133 L217-219, L222; A141 L1; A161 N3; A166; A172 N4; A177 R1; A211; A212; kit `fdc0ee6c` L83, L110-112.

**Implements.**
- P-112: the sampler, solo mode, the rerun path with twin mode, host RAM, the nine keys, and a stop-outside-set command for root.
- c2v007:
  - full evidence only on the counted pair. On attempt 0 it requires spec_sha256 and wall_cap_s (and output_cap_bytes for OUTPUT_CAP) unless attempt 0 is counted;
  - it checks rss_cap_bytes == 11 × host_ram_bytes for S0_SEED_CW8_TWIN only;
  - it recomputes other_ngc_processes_max from the pinned sample under item 4's five cases, with the whole-second comparison.
- Root: the hold rule, including the rule for NGC tools not on the list, and the outside-set stops.

**Blocks.** P-112's start. Until this is implemented, no call can be marked invalid or unevaluated, and a failed call stays non-terminal (RUNBOOK L415). Phase-1 step 4, if any call fails.

### G27: the launch registry and the receipt binding

**Question.** RUNBOOK L417: the registry's producer and schema; the θ value receipts carry; binding keys on every receipt.

**Ruling.**
1. **The registry.** STEP5_LAUNCH_REGISTRY_C2V003, exactly as c2v006 checks it (L136, L604-636). It is fed from per-call entries, each written by exclusive create at its call's first launch: the kit's UNT_S0_LAUNCH_REGISTRY_ENTRY_C2V003A, or P-112's own entry. At step 4, P-112 `assemble-registry` writes the STEP5 file and an assembly record that pins every source.
   - An S0 entry whose θ key is a PLAN member's becomes that MEMBER entry, matched by (log_index, role, order) (IC-P1-MEMBERS, A171 L1592). Before it maps one, assemble-registry checks three things and refuses on any mismatch (one-ulp MUST_FAIL tests):
     - O.theta_key(PLAN theta_engine) equals the kit's theta_key;
     - the kit spec's θ bits equal the PLAN theta_engine's float.hex;
     - the spec's NGC geometry equals the theta_ngc nuisance values.
   - The other S0 entries in the set become OTHER entries (F0-F2, S0_SEED_CW8_TWIN). Outside-set serials are left out and listed.
   - A verify mode rebuilds the STEP5 bytes from the pinned sources and byte-compares them. Root runs it before the FULL build.
2. **θ: two functions, both carried.**
   - The program θ key (orchestrator theta_key, L523-529) hashes a schema-wrapped engine θ.
   - The builder's theta_sha256 hashes v003g's canonical bytes of theta_ngc, which adds the NGC nuisances.
   - A MEMBER's theta_sha256 is hashed from the saved PLAN `evaluate_envelopes(budget=0)` PRIMARY output (spec of record `e2a7650e`) and is never recomputed.
   - An OTHER entry's theta_sha256 is its point key (RUNBOOK L82).
   - A member handoff carries no θ and no key (phase1 v003b L686-689). The θ comes through its source_export_pin at its log_index; the key comes through fdplan.
3. **The attempt receipt.** STEP5_ATTEMPT_RECEIPT_C2V001, at exactly `<outdir>.attempt_receipt.json`, by exclusive create, written by P-112 `close-attempt` (S0 kit attempts included).
   - It carries theta_sha256, spec_sha256 and point_key for every class.
   - It pins the monitor receipt, the .launch.json, the LAUNCH or MISLAUNCH record, the registry entry, the solo sample and any kill record. Its spec_sha256 must equal both the monitor's and the registry's.
   - close-attempt writes nothing until:
     - the run volume is mounted (otherwise it refuses RUN_VOLUME_NOT_MOUNTED; process rulings, "Run volume first");
     - the monitor receipt exists (if the monitor pid is gone without one, it refuses MONITOR_ENDED_NO_RECEIPT);
     - exactly one LAUNCH or MISLAUNCH record of this attempt exists;
     - for the twin, the kill-watch pid in the LAUNCH record has exited;
     - for an S0 attempt, the PLAN and fdplan mapping exists.
4. **c2v007 trusts nothing the receipt asserts.** It:
   - accepts the receipt only at realpath(run_dir) + `.attempt_receipt.json`;
   - verifies the pinned monitor receipt's self-hash (the verify_receipt logic);
   - re-derives raw_status from the monitor's status, driver_status and exit_code, plus the pinned, bound MISLAUNCH and kill records;
   - requires the receipt's caps, spec and time_utc to equal the monitor receipt's;
   - recomputes other_ngc_processes_max from the pinned sample under G25 item 4's five cases, taking the monitor's start and end from the monitor receipt's utc_start and utc_end and comparing in whole seconds (G25 item 4), and requires the receipt's value to equal it.

   Results and cut records stay inside run_dir. The run tree is never written after the run, except the G16 restore.
5. **Non-attempts.** Some attempts are not attempts of the call:
   - one with no run directory at close: MONITOR_REFUSED (D7), or a LAUNCH or MISLAUNCH whose outdir does not exist (the driver ended before its mkdir, driver L8994). A Refusal or OSError in cmd_run before that mkdir (L9208-9215) is not caught by main (L4971-4987), so the driver exits 1 with no outdir and no finish (CHILD_FAILED|NONE|EXIT); a signal there gives CHILD_FAILED|NONE|SIGNAL. The launch check reads only `.launch.json`, so such an attempt can carry a LAUNCH record;
   - a LAUNCH or MISLAUNCH with a spec other than the registered one;
   - an attempt named in a RESIDUAL_RETRY line while it has no monitor receipt (root's ruling on a residual; process rulings). It uses its number. A line never makes an attempt with a monitor receipt a non-attempt: assemble-registry and c2v007 refuse RESIDUAL_RETRY_NOT_RESIDUAL for such an attempt, and root rules.

   Each is recorded in V006 and in the assembly record and left out of the call record. A non-attempt does not separate an INFRA_REPEAT pair or a rule-(c) pair.
   - **After a non-attempt LAUNCH or MISLAUNCH** (the last record of the call is one): retry with its caps and solo mode (first-attempt caps if no attempt precedes it); no new registry entry. The record used its attempt number, so the retry takes the next k. It is a retry, not a first attempt, even at k = 1. The same holds after an attempt named in an honoured RESIDUAL_RETRY line (process rulings).
   - Non-attempts carry no count limit, as INFRA retries carry none (A133 §3). P-112 `status` reports each call's run of consecutive non-attempts, and root, who runs every launch, sees each one.

**Evidence.** c2v006 L136, L276-277, L604-636, L706-707, L716-717, L738-745, L1056; orchestrator `c75a889f` L523-529; v003g `48a1e48a` L1019-1025, L2162-2163, L2313-2335; phase1 `7d891ff7` L686-691, L776-822; kit `fdc0ee6c` L613-650 (the entry carries theta_key and spec only); root_monitor `ba031c23` L192 (utc_start, utc_end); step5_path README L48; A136 L584; A169 L1538; A171 L1590-1592. Probes (TESTED): c2v006 _launch_registry accepts an assembled STEP5 file; a receipt beside run_dir refuses RECEIPT_NOT_IN_RUN_DIR.

**Implements.** P-112: the entries, close-attempt, assemble-registry with its verify mode, and an interface proof against c2v006's bytes. c2v007: the receipt residence, the re-derivation and the sample recomputation. S0 kit: no change.

**Blocks.** P-112's start; every MEMBERS or FULL build (RUNBOOK L417); Phase-1 step 4.

### G15: the M-15 record and its V006 copy

**Question.** RUNBOOK L139, L407: the pre-launch record's path and format, and the V006 byte copy.

**Ruling.**
- The record of record is the kit's UNT_M15_PRELAUNCH_RECORD_C2V001 at `<S0 launch root>/M15_PRELAUNCH_RECORD_C2V001.json`. It is written by exclusive create as the seed serial's first action (A142 item 6; A161; A179). The RUNBOOK's proposed M15_PRE_LAUNCH_RECORD_C2V001 is withdrawn.
- c2v007 reads it by its exact keys:
  - v006_sha256 = `v006.sha256`;
  - the gate list = `gate_documents_pinned_in_v006[].sha256_from_bytes`;
  - date_u as written, which must parse to `date_u_epoch_s`.
- The m15 launch receipts are the .launch.json of every attempt of the seed serial and the twin, MISLAUNCH attempts, non-attempt LAUNCH or MISLAUNCH records, and attempts named in a RESIDUAL_RETRY line included (an attempt with no .launch.json adds none). Each is timed by its `utc` key, not by the call receipts' time_utc. c2v006 uses the earliest of them (L1380-1391).
- Root runs `cp -n` of V006 to `<S0 launch root>/M15_V006_COPY_<sha256>.md` before its first V006 write after the record, a mis-launch entry included. Root checks the copy's sha and byte count against v006.sha256 and v006.bytes, and logs the copy's sha in the entry that records the S0 launch.

**Evidence.** Record writer `a10965b7` L194-212; kit `fdc0ee6c` L418, L796-812; no copy step in `621263a2`, `f199544d` or `a10965b7`; c2v006 L126, L339-347, L1364-1391. Probes (TESTED): the kit record refuses INPUT_KEY_MISSING under c2v006; c2v006's parse_utc_ns parses the `date -u` form. A161 N2.

**Implements.** Root: the copy step. c2v007: the kit form. S0 kit: no change.

**Blocks.** The S0 launch procedure; the Phase-1 FULL build's m15 input. Without that input, every gate reads LATE (RUNBOOK L167).

### G7: the TSR support record

**Question.** RUNBOOK L398: whether UNT_ROOT_TSR_SUPPORT_CX3V001 exists, who writes it, and its point_key.

**Ruling.** It exists. Root writes it by machine projection (c2v007 `tsr-support`), and `tsr-check` verifies it.
- **Keys.** Exactly classifier A's nine:
  - schema UNT_ROOT_TSR_SUPPORT_CX3V001;
  - mode SAVED_TARGET_FREE;
  - target_free true and before_target_access true;
  - slots_pin, ntest_compare_pin, rings and point_key (below);
  - rule_id M7_I_DEPENDENCE_OPEN_INTERVAL_C2V001.
- **rings.** One entry, with exactly the keys {native_ring, lower_kpc, upper_kpc, lower_inclusive: false, upper_inclusive: false}. native_ring is the compare's ordinal-15 TRUNCATION_SHAPE ring, copied verbatim. The bounds are 9.901810628740723 and 10.911721936765339 (V001 content_when_written).
- **slots_pin.** Copied byte-canonically from the adopted carrier extractor's policy `slots` pin, with the same path spelling. Both candidate policies pin `freeze_score_readiness_cx3/v003g/slots/NGC3198_FREEZE_SLOTS_CX3V003.json` `d3859b42`; its content was not opened or shown; its bytes may have been hashed once (fixer-round disclosure):
  - POLICY_CX3V001 `311ceedd` (extractor cx3v005);
  - POLICY_CARRIERS_C2V001 `aa50c752` (extractor c2v001, step5_path).

  POLICY_C2V001 `0c781a17` pins the same slots.
  - **Open:** the extractor choice under A135 item 11. Root rules it before the record is due.
  - If the M-14 slots successor is pinned for Phase 2, slots_pin is ruled again then.
- **ntest_compare_pin.** The exact pin dict root passes as the compare in input_files (`6f095f64`), with the same spelling.
- **point_key.** Take D1's member id from the pass record of the ledger head the freeze uses. point_key is the fdplan members[].key of the member whose (log_index, role, order) matches that id.
- **Timing.** The record is written after step 7 reads NO_NEW_DISCREPANCY and before step 8, and it is input_files item 8. tsr-check asserts the slots and compare equalities.

**Evidence.** Classifier A `e92aa30e` L644-725 (L705-723); extractor `50c7db5f` L158-163, L213-221; the three policies' `slots` pins, read from their bytes (the slots file: its content was not opened or shown; its bytes may have been hashed once, fixer-round disclosure); ROOT_TSR_FLAG_RECORD_V001 `61bd8a83` pins.support_record; c2v006 L200-211; RUNBOOK L46, L116, L129, L286, L384; A177 L1846.

**Implements.** c2v007 (root build, reviewed by Codex1). Not S0, not P-112.

**Blocks.** The freeze's input_files item 8 and classifier A's bundle. Without the record, classifier A fires TSR_FLAG_TABLE_MISMATCH. The A135 item 11 extractor ruling comes first.

### G16: after a stop

**Question.** RUNBOOK L195, L358, L408: the remedy after a pre-target stop or after PASS_RESULT_CUSTODY_BREACH.

**Ruling.**
1. **Root's own preflight** (8a tsr-check and check-gate-list; 9-pre seal-check). Root records the stop code in V006. The only permitted remedies are:
   - re-run with corrected inputs, when what root passed was wrong;
   - re-produce a root-written target-free record with its registered producer, from unchanged pinned inputs;
   - restore a pinned object from a byte copy whose sha256 equals the pin.

   No roster, cut, member, reference, gate set, compare, N1 or node record, sealed object or registered text changes. If no remedy clears the stop, score_after_freeze is not called, and the phase is reported with the stop code, disclosed.
2. **The sealed classifier's synthetic pre-score run.** A stop there is r3a's CLASSIFICATION_INPUT_DEFECT and ends that phase's classification. Root adds no remedy.
3. **Custody (D10).** Root takes the `cp -n` custody copies of each terminal attempt's result, monitor receipt and attempt receipt when that attempt receipt is closed (sha-checked against the monitor's result pin), and of the cut records at step 3; in every case before pass one. Step 5 pins them. The custody directory is outside every run tree. (In the Phase-1 order 3 → 4 → 2, then 5 (RUNBOOK L159), pass one reads the registered results before step 5, so copies taken at step 5 would come too late for 3(a).)
   - 3(a) and 3(b) apply only with the run volume mounted (the P-112 §6.10 mount check). A missing volume is a stop, never a breach, and nothing is written under an unmounted path.
   - (a) On PASS_RESULT_CUSTODY_BREACH, root restores the file at its registered path from that copy, re-runs the pass and records the event. This restore is the single permitted write into a run tree, and it is recorded in V006.
   - (b) A call that meets both conditions reads UNEVALUATED_CUSTODY_BREACH (FREEZE_INCOMPLETE): (i) its registered result sha fails to verify from bytes, with the run volume mounted; (ii) no custody copy with that sha exists. It is never rebuilt, rerun or substituted. This is a pre-result registration under A133 §3 (L201), so no judgment point remains. The successor plan that records it is constrained:
     - it is machine-derived by c2v007, never written by root (A133 L215);
     - it is c2v006 `_apply_unevaluated` (L1809-1830) applied to exactly the calls that meet both conditions, with UNEVALUATED_CUSTODY_BREACH in place of UNEVALUATED_STEP7_DISCREPANCY (own_disposition and replay_index); nothing else changes. The function's other effects are therefore part of the successor: it lowers member_budget and re-runs `_effective`, so every later member reads UNEVALUATED_BY_ORDER_TRUNCATION (forced by v003g, RUNBOOK L112); in Phase 2 it resets the sensitivity block; it sets predecessor_sha256;
     - c2v007 ledgers it as a CUSTODY entry kind in the same hash chain (c2v006 L2042 and L2047 would read it BROKEN). The reader re-checks both conditions and re-derives it byte for byte (RUNBOOK §7a L217; K10, K11, K17). Anything else reads STEP7_LEDGER_BROKEN. With the run volume unmounted the reader stops; it never reads BROKEN or a breach for that reason.
     - MUST_FAIL: a successor that marks a call whose result still verifies reads STEP7_LEDGER_BROKEN.
     - MUST_FAIL: a custody successor that leaves member_budget unchanged where `_apply_unevaluated` lowers it reads STEP7_LEDGER_BROKEN.
     - Scope: `_apply_unevaluated` marks replay entries through their MEMBER keys only (L1818). Every Phase-1 replay entry is a member's (OTHER calls carry no alternative, L1225-1240), so the Phase-1 derivation is complete. A Phase-2 SENSITIVITY-only replay entry is not marked by it; that form is open (Open items), due before Phase-2 pass one.

**Evidence.** r3a `c64f65a3` L184-201, L691; RUNBOOK L112, L159, L195-197, L212-217, L339-358; c2v006 L1225-1240 (replay_index), L1601-1604 (the replay records RESULT_CUSTODY_BREACH), L1766-1768 (PASS_RESULT_CUSTODY_BREACH), L1809-1830 (`_apply_unevaluated`), L1995-2047 (STEP7_LEDGER_BROKEN; L2038-2047, the successor must be step 7's own change and needs NEW_UNEVALUATED); A133 L215; K10, K11, K17.

**Implements.** Root: the copies at receipt close and at step 3, the step-5 pins, the mount check before 3(a) or 3(b), and the restore. c2v007: the text, the 3(b) successor derivation, the CUSTODY ledger entry kind and the reader's re-check, TESTED on synthetic records with both MUST_FAIL cases above.

**Blocks.** Nothing now. The copies are needed from the first closed terminal attempt receipt and at step 3, before the first pass on real results; 3(a) and 3(b) before the first 8a or 9-pre check.

### G24: the Phase-1 gate cutoff

**Question.** RUNBOOK L414: the Phase-1 gate cutoff, proposed as the V006 at the step-4 start.

**Ruling (D11).**
- **T** is the latest time_utc over the terminal attempt receipts of the call set. Receipts are not closed in the order their attempts ended (S0 receipts wait for the PLAN mapping), so T is not the time_utc of the receipt that completes the set.
- **Copies before writes.** From the M-15 record until c2v007 accepts the cutoff record, root takes `cp -n` of V006, named by its sha (`V006_COPY_<sha256>.md` in the root copy directory), before every V006 write. The V006 at T is the copy taken before the first V006 write after T, or the machine cutoff copy when no write fell between T and it.
- **The cutoff copy is taken by machine.** P-112 close-attempt takes it when it writes the receipt that completes the call set by its advisory pre-check; otherwise root takes it at its first sight of that receipt. It is pinned as gate_cutoff, kind PHASE1_STEP4_START. P-112 writes the cutoff record once.
- **c2v007 decides T.** P-112's pre-check is advisory; the builder decides terminality. c2v007 re-derives the terminal set and T from the pinned receipts and uses its own T. It accepts the cutoff copy only if the cutoff record's date_u is at or after that T; otherwise it refuses GATE_CUTOFF_BEFORE_T. Root then writes a successor cutoff record, with c2v007's T, the receipt pins and the V006 at that T (by the copy rule above), and records it in V006. It pins the record it supersedes, and it is the only second record allowed.
- **Entries after T.** The cutoff entry lists every V006 entry stamped after T (c2v007's T). A gate whose full sha first occurs in such an entry is not a Phase-1 gate document. A gate first pinned after M-15 reads LATE on either side of the cutoff (r3a L455).

**Evidence.** RUNBOOK L163-167, L183, L263; c2v006 L113, L967-993, L1347-1409, L1452-1476; A157 L1245; r3a L455-463 (a LATE gate only adds unsigned misses).

**Implements.** Root: the copies, and the single successor cutoff record on GATE_CUTOFF_BEFORE_T. P-112 close-attempt: the machine copy and its T, once. c2v007: re-derives the terminal set and T, refuses GATE_CUTOFF_BEFORE_T, and excludes the after-T gates (with the RUNBOOK text).

**Blocks.** The Phase-1 FULL build.

### Claude3 0237 N1 (+N2)

**Question.** Should AT-0b's --values and --values-sha256 come from the values_sha256 logged in L1?

**Ruling.** Yes.
- AT-0b's `--values` is the values file whose sha256 equals `L1.values_sha256`, checked from bytes before the call, never a re-serialized copy.
- `--values-sha256` is that value.
- Every sha passed to phase1 is lower case.

**Evidence.** 0237 L34-35; README_PHASE1_C2V003B L31-35; A149 L976.

**Implements.** RUNBOOK c2v007 text. v003b already enforces it.

**Blocks.** AT-0b and AT-1 (Phase 2).

### Claude3 0237 N3

**Question.** How is a phase1 successor handled after the freeze?

**Ruling.** phase1 v003b `7d891ff7` is the tool of record in both phases (A210, the P-117 record), and no successor is commissioned. If a defect ever forces a successor after the freeze, option (b) applies:
- the logged v003b L1 stays the L1 of record and is never replaced;
- the successor's band writes a new L1 by exclusive create, logged beside the original with a byte diff showing that only `module` differs;
- the successor is POST-PREDICTION (r3a L51-55).

Option (a) is not adopted.

**Evidence.** 0237 L31-33; A171 L1590-1593; A210; r3a L51-55, L209.

**Implements.** Done (A210).

**Blocks.** Nothing now.

### Claude4 0248 VN1

**Question.** Phase 2 has no producer for A16.4. Every honest Phase-2 freeze would refuse until one exists.

**Ruling (D12).** This implements registered A16.4 (r3a L379).
- **Which entries.** The A16.4 entries are the v003g kind SENS_NGC entries whose theta_ngc geometry differs from the registered geometry as the spec of record states it, compared from bytes, not with literals.
- **The answer.** For each one, the replay adapter returns, in memory, valid=false, a reason carrying GEOMETRY_NOT_EXPOSED, and no valid row (v003g L3016-3025). A non-registered geometry on any other entry kind raises.
- **Never launched or registered.** c2v007:
  - keeps `kind` in the value-free plan;
  - exempts these entries from CALL_RECORD_MISSING, from the roster contexts and from the replay index;
  - gives them own_disposition GEOMETRY_NOT_EXPOSED_IN_MEMORY. The sens-budget rule counts them as evaluated, and they never trigger V-N1.
- **Recorded.** PASS_RECORD lists each in-memory answer. RUNBOOK step 6's "never invents" names this as its one registered exception.

**Evidence.** 0248 L41-43; v003g L2321, L2557-2559, L2995-3029; c2v006 L481, L513, L1133-1136, L1145, L1253; the driver `577f8c94` has no GEOMETRY_NOT_EXPOSED path.

**Implements.** c2v007, with TESTED MUST_PASS and MUST_FAIL cases.

**Blocks.** Phase-2 pass one and every honest Phase-2 freeze. Not Phase 1.

### Claude4 0248 DN5

**Question.** V-N1 counts members only. Do capped or unevaluated Phase-2 sensitivity entries count?

**Ruling (D12).** They count. This is a disclosed pre-result registration under A133 §3 (L201: "new registrations, made before any result and disclosed"), and it settles the DN5 item that A178 left open.
- **What it replaces.** It replaces the scope of the C2V004 V-N1 rule (`write_freeze_manifest_inputs[allow_incomplete].value.phase2.true_if_and_only_if`; README_RI45_14_C2V004 L37). The list's bytes are unchanged.
- **The rule.** Phase-2 allow_incomplete is True if and only if a member or a sensitivity entry of an evaluated alternative has one of these own_dispositions in the last pass's replay plan; otherwise it is False:
  - UNEVALUATED_CAP;
  - UNEVALUATED_STEP7_DISCREPANCY;
  - UNEVALUATED_INFRA_REPEAT (G13; itself a pre-result registration under A133 §3);
  - UNEVALUATED_CUSTODY_BREACH (G16; itself a pre-result registration under A133 §3).

  GEOMETRY_NOT_EXPOSED_IN_MEMORY never triggers it.
- **Who reads it.** c2v007 exposes the value in the replay plan, and G26 takes it from this entry, not from the pinned list. G3 is closed (DN1).
- **Timing.** This entry comes before any step-5 output, so it meets r3a L149 and M-8.

**Evidence.** 0248 L44-46; A163 L1415; A178; A133 L172-173, L201, L206; r3a L149; RUNBOOK L293 (v003g L3675-3678).

**Implements.** c2v007 and G26.

**Blocks.** The Phase-2 freeze.

### Open items

- **G28 (NEEDS_INFO, not ruled).** The step-7 ledger root is due before the first FULL build (Phase-1 step 4), not before S0 (A201 L2578). Root then fixes an absolute directory outside every build directory. A later change is a V006 event.
- **G7's extractor.** The A135 item 11 extractor ruling is due before the TSR support record.
- **The three residuals.** A second monitor refusal at the same attempt number and MONITOR_STARTED_NO_LAUNCH_JSON (both D7's), and MONITOR_ENDED_NO_RECEIPT, go to root (disclosed reading 19). Each is decided only with the run volume mounted. MONITOR_STARTED_NO_LAUNCH_JSON and MONITOR_ENDED_NO_RECEIPT each hold their call non-terminal, and so hold step 4, until root rules in V006: P-112 refuses every launch of the call until then. Root's ruling on either takes the RESIDUAL_RETRY form (process rulings), except in the S0_SEED_SERIAL limit disclosed there; a ruling in any other form needs a P-112 successor. After a second monitor refusal at one k (MONITOR_REFUSED_TWICE), P-112 cannot see the unrecorded refusal and does not hold the call; holding it, and so holding step 4, is root's procedure until root rules it in V006 (process rulings, D7).
- **G16 3(b) in Phase 2.** The custody successor's form for a SENSITIVITY-only replay entry, which `_apply_unevaluated` does not mark (c2v006 L1818). Root rules it before Phase-2 pass one. Phase 1 is complete without it.

### Launch condition, process rulings and reviewers

- **P-112 launch (D8).** P-112 is a Codex2 build. Claude4 reviews it after Fri 23-Oct 19:00Z (A205 items 8 and 11(2); A208).
  - Root writes P-112's adoption entry only after that review returns 0 blocking. The entry carries one line, `TOOL_PIN P112_LAUNCHER_CX2V001 <sha256 of the tool's bytes> <the tool's realpath>`, in the kit's pin-line form. The kit's parser ignores `TOOL_PIN`, which is not one of its KINDS (`a10965b7` L41-43); nor is `RESIDUAL_RETRY` one.
  - The gate covers every subcommand that writes a record: launch, close-attempt, assemble-registry, stop-outside-set and record-monitor-refused. Each refuses unless V006 holds exactly one whole-line TOOL_PIN (PIN_RE form) named P112_LAUNCHER_CX2V001, carrying the tool's own sha and realpath. A TOOL_PIN line is a whole V006 line, under an entry heading, matching `^TOOL_PIN ([A-Z0-9][A-Z0-9_]*) ([0-9a-f]{64}) (/.*\S)$` (the kit's PIN_RE form, `a10965b7` L43). Text that mentions TOOL_PIN inside a line, as this entry does, is not a pin line. A line that begins `TOOL_PIN P112_LAUNCHER_CX2V001` and does not match refuses TOOL_PIN_MISMATCH. Dry mode and the read-only `status` are exempt.
  - The version is part of the pin name. A fixed P-112 is pinned under its own name (for example P112_LAUNCHER_CX2V002), so no V006 line ever needs removing.
  - No launch is made on root verification alone. P-112 is needed at u_A, about Tue 27 to Wed 28 Oct. If the review is late, root records the slip.
- **Spec fills.** P-112 never runs or imports the filler, because the filler opens the slots pin (fill_step5_c2v001 L264, L292). Root fills each P-112 call's spec directory under its blinding guard, as for S0. P-112 only checks the fill.
- **NGC ρ point registrations (A211 consequence 2, N3).** Point custody admits exactly the four registered S0 keys. Every Phase-1 member or F point outside S0 needs a root NGC ρ point registration before its acceptance. Root writes each one when u_A fixes the actual set. P-112 does not register.
- **Disk (D9).** P-112's launch check refuses unless the run volume has the attempt's output cap + 20 GiB free. An OUTPUT_CAP serial rerun therefore needs 292 GiB. Root names the run volume in the P-112 config.
- **Run volume first.** MONITOR_ENDED_NO_RECEIPT, MONITOR_STARTED_NO_LAUNCH_JSON, the D7 `absent` checks and the RESIDUAL_RETRY residual check (below) are decided only after the P-112 §6.10 mount check passes (the run volume is mounted, not symlinked). With the run volume unmounted, `status` reports RUN_VOLUME_NOT_MOUNTED, and close-attempt, record-monitor-refused, assemble-registry and launch refuse RUN_VOLUME_NOT_MOUNTED (a stop, as in G16 3) and write nothing. The sampler's 60 s wait for a receipt (G25 item 4) is counted only while the volume is mounted. On root's side, root writes a kit MONITOR_REFUSED record, and a RESIDUAL_RETRY line, only on existence checks made with the run volume mounted. A receipt on an unmounted volume is not absent: after a host restart, a finished attempt whose receipt sits on the unmounted volume is never reported, refused or ruled as a residual.
- **Monitor refusal (D7).** A monitor that refuses writes no .launch.json.
  - The refusal is recorded in MONITOR_REFUSED_ATTEMPT_RECORD_C2V001, by exclusive create. It maps to INFRA, and it is not an attempt of the call.
  - **Path.** For a P-112 call, P-112 `record-monitor-refused` writes `<p112_launch_root>/launches/P112_<NAME>_MONITOR_REFUSED_CX2V001_A<k>.json`. For a kit call, root writes `<S0 launch root>/monitor_refused/<NAME>_MONITOR_REFUSED_C2V003A_A<k>.json`, outside the kit's `launches/`. Root writes kit records itself, because S0 launches come before P-112 is adopted.
  - **Exact key set:**
    - schema;
    - name and attempt (k);
    - launcher: `KIT_C2V003A` or `P112_CX2V001`;
    - writer {name, sha256}: `ROOT` with null, or `P112_LAUNCHER_CX2V001` with the tool's sha;
    - plan {path, sha256}. For a kit call this is `<work>/plan.json`;
    - monitor_stdout and monitor_stderr {path, sha256}. For a kit call these are `<work>/monitor.stdout.txt` and `<work>/monitor.stderr.txt` (serial script L126, L195; twin script L81, L147);
    - absent {outdir, receipt, launch_json, receipt_stdout, receipt_stderr}: the planned paths (`<outdir>`, `<outdir>.receipt.json`, `<outdir>.receipt.json.launch.json`, `<outdir>.receipt.json.stdout.txt`, `<outdir>.receipt.json.stderr.txt`), each absent when the record is written;
    - date_u, from `date -u`;
    - rule.
  - **A monitor that started is not a refusal.** root_monitor creates `<receipt>.stdout.txt` and `.stderr.txt` by exclusive open (L143-144) after its refusal checks (L133) and before Popen and `.launch.json`. A monitor that dies there leaves both files, and a relaunch at the same k fails on that open every time. If either file exists, the event is not a D7 refusal: `record-monitor-refused` refuses MONITOR_STARTED_NO_LAUNCH_JSON, and root rules (a driver may have started).
  - **A kit record waits for the monitor to exit.** The kit's scripts exit 5 after about 120 s without `.launch.json` even while the monitor is still alive (serial script L202-208; twin script L150-155). Root writes a kit record only after that monitor pid has exited. If the kit script exited 5 at its 120 s wait (serial L206-208; twin L155) with the monitor alive, root stops that monitor pid the same way before writing anything: it confirms that the pid's command line names root_monitor and this receipt, sends TERM, KILL after 15 s, and waits for it to exit. If `.launch.json` then exists, root stops its child with kill-target and records a kit MISLAUNCH with the kit's `launch-record --outcome MISLAUNCH`; otherwise the D7 record rules apply. kill-target runs without `--mon-pid` here: the monitor is gone, so the child's parent has changed and kill-target's parent check (kit L958-959) would refuse; it still checks the group leader, the exact command and the spec (L932-957). Such a MISLAUNCH has no monitor receipt, so the attempt is MONITOR_ENDED_NO_RECEIPT (below).
  - The work directory's `monitor.stdout.txt` and `monitor.stderr.txt` are hashed only when no `.launch.json` exists. A run's `<outdir>.receipt.json.stdout.txt` and `.stderr.txt` are never opened.
  - P-112 accepts a root-written record. It checks the exact key set, the schema, the name and k, every pin from bytes, and, while no relaunch at the same k has started (no LAUNCH or MISLAUNCH record of (NAME, k), and neither `<outdir>.receipt.json.stdout.txt` nor `.stderr.txt` of k exists), that every `absent` path is still absent. Once the same-k relaunch has started, those paths belong to the relaunch and are not re-checked; the writer's check at date_u stands.
  - Root may relaunch once, at the same attempt number, and records the refusal in V006. A kit call is relaunched through the kit (order-check admits k, and register returns ALREADY_REGISTERED_SAME_SPEC, kit L635-644). A P-112 call is relaunched through P-112, which admits its existing same-spec registry entry in the same way.
  - If the refused attempt is the seed serial's first, the V006 record waits until the relaunch's launch record (A161 N2), and the G15 copy is taken first.
- **A monitor that ends without a receipt (MONITOR_ENDED_NO_RECEIPT; a residual).** A LAUNCH or MISLAUNCH record of the attempt exists, the monitor pid is gone, and `<outdir>.receipt.json` is absent.
  - Causes: the host restarts or panics during a run of several days; the monitor is killed, a stop at the launch bound with `.launch.json` present included (the D7 kit bullet above; brief §11.5); root_monitor's receipt write (`_write_x`, L199) fails because the run volume is lost or full (the receipt sits beside the outdir on that volume).
  - "Gone" means that no live process has the record's `monitor_pid` (kit L1132; P-112 carries the same key) with a command line naming root_monitor and this attempt's receipt path. A pid reused after a restart is therefore not the monitor.
  - The attempt has no monitor receipt, so it has no status and no attempt receipt. The call cannot reach a terminal attempt receipt, and step 4 cannot begin (A133 L210). It goes to root. No value is read, and neither the outdir nor the receipt's stdout and stderr files are opened.
  - P-112, with the run volume mounted ("Run volume first", above): the sampler stops when the monitor pid is gone and no receipt has appeared 60 s later, and writes nothing at the outdir path; close-attempt refuses MONITOR_ENDED_NO_RECEIPT; `status` reports it; every launch of that call refuses MONITOR_ENDED_NO_RECEIPT until a RESIDUAL_RETRY line for it (next bullet); any other ruling needs a P-112 successor.
- **Root's ruling on a residual: one machine form (RESIDUAL_RETRY).** Root's ruling on MONITOR_ENDED_NO_RECEIPT or MONITOR_STARTED_NO_LAUNCH_JSON has one machine form: a whole V006 line `RESIDUAL_RETRY <NAME> <k>` under the ruling entry. It is not a kit KINDS token, and it is parsed anchored, as TOOL_PIN: the line matches `^RESIDUAL_RETRY ([A-Z0-9][A-Z0-9_]*) ([1-9][0-9]*)$` under an entry heading. Text that mentions RESIDUAL_RETRY inside a line, as this entry does, is not such a line. A line that begins `RESIDUAL_RETRY ` and does not match refuses every P-112 launch (RESIDUAL_RETRY_MALFORMED). Duplicate lines for one (NAME, k) act as one.
  - With the line, attempt k of NAME is a non-attempt (G27 item 5) that uses its number. The next legal attempt is a retry at k+1 with attempt k's caps and solo mode, and no new registry entry (brief §6.12 applies, even at k = 1). That retry is P-112's, and the brief §1b carve-out ends for that call (G25 item 8). Numbering counts the k of every RESIDUAL_RETRY line for NAME.
  - Attempt k's caps and solo mode are those in its LAUNCH or MISLAUNCH record. With no such record (MONITOR_STARTED_NO_LAUNCH_JSON), they are the caps and solo mode the next-legal-attempt rule gave attempt k, recomputed from the records before it.
  - P-112 launches the retry only when no live process runs attempt k's monitor command or its planned driver command (`run --spec <spec> --outdir <outdir of k>`); otherwise it refuses RESIDUAL_ATTEMPT_PROCESS_ALIVE. The outdir of k is the kit's (`run_name_for`, kit L318, L354-355, under s0.run_root) when attempt k was the kit's (no kit LAUNCH record, P-112 attempt or RESIDUAL_RETRY line of the call before it; G25 item 8), and P-112's (brief §5) otherwise. MONITOR_STARTED_NO_LAUNCH_JSON leaves no record naming its launcher, so this rule decides it.
  - P-112 honours the line only while attempt k of NAME is one of the two residuals: a LAUNCH or MISLAUNCH record of k whose monitor is gone with no receipt; or no LAUNCH or MISLAUNCH record of k, the receipt's stdout or stderr present, and no `.launch.json`. Otherwise it refuses RESIDUAL_RETRY_NOT_RESIDUAL, so a line never turns an attempt that has a monitor receipt into a non-attempt. These are existence checks; nothing is opened.
  - Without the line, the call stays held. Any other ruling needs a P-112 successor.
  - **A second monitor refusal at one k (MONITOR_REFUSED_TWICE, D7)** cannot be recorded (exclusive create), so the state on disk is the same as after the first refusal. P-112 cannot see an unrecorded second refusal and does not hold the call; it admits a further launch at k as it admitted the first relaunch. Holding the call after MONITOR_REFUSED_TWICE is root's procedure (root runs every launch), and a third launch at k is made only on root's V006 ruling; no P-112 successor is needed for it.
  - One limit, disclosed: S0_SEED_SERIAL before its first kit LAUNCH record. P-112 refuses every launch until the kit holds a seed LAUNCH record (brief §6.2; r3a L454), and the kit's order-check refuses every other S0 call (SEED_SERIAL_NOT_LAUNCHED_FIRST, kit L785-788). A residual there needs a successor of the kit or of P-112, which root names in its ruling.
- **Schedule risk (disclosed; rule (c) as registered, not a new rule).**
  - A failing call needs two solo reruns at the doubled wall: up to 1,220,648 s each for a serial (S0 serials included), and 45,504 s for the twin.
  - Each serial rerun can add about 14 days to the start of Phase-1 step 4.
  - The hold rule runs every counted rerun alone, so reruns of different calls do not overlap, and their delays add.
- **Reviewers (D13).**
  - RUNBOOK c2v007, text and builder, is a root build reviewed by Codex1 with DN1/DN2 (A208 item 2(a)), not Claude4. It is pinned before Phase-1 step 4 (G1).
  - P-112 is reviewed by Claude4 (A205 item 8).
  - The G26 step-8 freeze script is a root build reviewed by Codex2 (A205 item 10).

### Disclosed readings

1. REFUSED, BLOCKED and signal deaths with no finish record are INFRA (A133 §3(c), "not INFRA").
2. Infrastructure deaths that surface as FAILED, FAILED_AT_STAGE or NONE|EXIT read literally as FAILED (D2). That includes a full disk, and a lost volume, when the monitor's receipt is still written; otherwise the attempt is MONITOR_ENDED_NO_RECEIPT (reading 19). The guard is the solo pair at the doubled wall.
3. ROUTE_A_NO_FIXED_POINT is FAILED, because it is a non-zero exit (L9102).
4. When the monitor and the driver disagree (FINISHED with a non-completed finish; CHILD_FAILED with COMPLETED or COMPLETED_INVALID), the status is INFRA.
5. A STOPPED_<cap> monitor status wins over every driver-side value.
6. A REFUSED or BLOCKED attempt is retried solo at the replaced attempt's caps. Two consecutive solo attempts with identical spec, caps and REFUSED (or BLOCKED) status read UNEVALUATED_INFRA_REPEAT. This is a pre-result registration under A133 §3 (L201), and it joins the DN5 trigger list.
7. "Other NGC process" is the declared tool list (D5). It holds the A211 stack of record, handoff c2v003a (the stricter reading), values writer v004 (A212) and the other listed producers and extractors. The ps count is a lower bound. The guarantee is the hold rule, which also covers any NGC tool not on the list, whenever it was adopted (the list reflects adoptions through A212).
8. "At RAM" is host RAM, and for the twin RAM × 11 (A172 N4; D3).
9. "Doubled" is 2 × the first attempt's wall cap. "Identical" is the identical composite raw status. The pair is the last two attempts of the call, non-attempts excluded, as c2v006 reads it; an attempt of any class between two failures separates them.
10. An OUTPUT_CAP rerun doubles the output cap, and the identity twin never has one. An INFRA or MISLAUNCH retry repeats the replaced attempt's caps and solo mode. A REFUSED or BLOCKED retry always runs solo.
11. Outside-set S0 serials are stopped at u_A (A133 L103).
12. A MONITOR_REFUSED attempt, or a LAUNCH or MISLAUNCH with no run directory or an unregistered spec, is not an attempt of the call. After such a LAUNCH or MISLAUNCH the call retries with its caps and solo mode (first-attempt caps if no attempt precedes it), with no new registry entry. An attempt named in a RESIDUAL_RETRY line while it has no monitor receipt is a non-attempt too, and the call retries the same way. A line never makes an attempt with a monitor receipt a non-attempt: assemble-registry and c2v007 refuse RESIDUAL_RETRY_NOT_RESIDUAL for such an attempt, and root rules.
13. A failed identity twin (a rule-(c) pair) is terminal for step 4. The identity then stays UNTESTED, and every call stays serial (A133 L111; A135 item 3).
14. The builder's θ function and the program θ key are both carried, and neither replaces the other.
15. DN5 replaces the C2V004 V-N1 trigger scope. The list's bytes are unchanged.
16. VN1's in-memory GEOMETRY_NOT_EXPOSED answers are the one registered exception to "never invents", and they count as evaluated.
17. G16 3(b): a call whose registered result fails to verify, with the run volume mounted, and has no same-sha copy is UNEVALUATED_CUSTODY_BREACH. This is a pre-result registration under A133 §3 (L201), and it joins the DN5 trigger list. The successor that records it is c2v006 `_apply_unevaluated` applied to exactly such calls, with UNEVALUATED_CUSTODY_BREACH in place of UNEVALUATED_STEP7_DISCREPANCY; it therefore also lowers member_budget, so later members read UNEVALUATED_BY_ORDER_TRUNCATION. c2v007 ledgers it as a CUSTODY entry kind and re-derives it byte for byte; anything else reads STEP7_LEDGER_BROKEN. A missing volume is a stop, never a breach.
18. G24: T is the latest time_utc over the set's terminal attempt receipts, as c2v007 re-derives it. Entries stamped after T are listed, and a gate that first appears in one of them is not a Phase-1 gate document. A cutoff record dated before c2v007's T reads GATE_CUTOFF_BEFORE_T, and root writes one successor record.
19. Three residual judgment points remain, and all three go to root: a second monitor refusal at the same attempt number and MONITOR_STARTED_NO_LAUNCH_JSON (a monitor that left its receipt stdout or stderr but wrote no .launch.json), both D7's; and MONITOR_ENDED_NO_RECEIPT (a LAUNCH or MISLAUNCH record exists, the monitor pid is gone, and the receipt is absent). Each is decided only with the run volume mounted. No value is read in any of them, and the outdir is never opened. Root's ruling on the last two has one machine form, a whole V006 line `RESIDUAL_RETRY <NAME> <k>`: attempt k, while it has no monitor receipt, becomes a non-attempt that uses its number, and the next legal attempt is P-112's retry at k+1 with attempt k's caps and solo mode. A line never makes an attempt with a monitor receipt a non-attempt (RESIDUAL_RETRY_NOT_RESIDUAL, and root rules). After a second monitor refusal at one k, root's procedure holds the call, not P-112, and a third launch at that k is made only on root's V006 ruling.
20. The kit keeps its own relaunches of an S0 call (after a kit MISLAUNCH, and the D7 relaunch) until the call has a LAUNCH record, a P-112 attempt or a RESIDUAL_RETRY line.

### Implementation owners

| owner | items | reviewer | needed by |
|---|---|---|---|
| P-112 launcher (Codex2) | G13 raw status and map, and the solo retry of REFUSED and BLOCKED; G25 sampler (five null cases, whole-second comparison, 1 s lead and tail), solo mode, reruns, twin mode, host RAM, stop-outside-set; G27 entries, attempt receipts, assemble-registry and its verify mode; D6 numbering with the kit carve-out (and the k of every RESIDUAL_RETRY line), and the retry after a non-attempt LAUNCH or MISLAUNCH; D7 records (five `absent` paths), MONITOR_STARTED_NO_LAUNCH_JSON, acceptance of root-written records (the `absent` check only until the same-k relaunch starts), and the same-k relaunch; MONITOR_ENDED_NO_RECEIPT (the sampler's 60 s stop, the close-attempt and launch refusals, `status`); the run volume first (RUN_VOLUME_NOT_MOUNTED before any residual, `absent` or RESIDUAL_RETRY check); RESIDUAL_RETRY (the anchored parse, the residual check in launch and assemble-registry, the live-process check, the retry at k+1); a monitor still alive with no .launch.json at the launch bound (stop it, then a MISLAUNCH or the D7 rules); `complete` as G25 item 4 defines it; the rule-(c) pair as c2v006 reads it; D8 TOOL_PIN gate (whole lines in PIN_RE form only) on every writing subcommand; D9 disk check; G24 machine cutoff copy, once, with T as the latest time_utc | Claude4, after Fri 23-Oct 19:00Z | 0 blocking before u_A (about Tue 27 to Wed 28 Oct) |
| RUNBOOK and builder c2v007 (root build) | attempt-receipt residence and re-derivation; recomputing other_ngc_processes_max from the pinned sample (whole-second comparison); attempt-0 evidence; twin RAM × 11 check; kit M-15 form; the INFRA_REPEAT pair (two consecutive solo attempts, identical spec, caps and status); the CUSTODY_BREACH successor (c2v006 `_apply_unevaluated` with UNEVALUATED_CUSTODY_BREACH, nothing else changed), its CUSTODY ledger entry kind, and the reader's re-check of both conditions with STEP7_LEDGER_BROKEN (two MUST_FAIL cases); non-attempt exclusion (an attempt named in a RESIDUAL_RETRY line only while it has no monitor receipt; RESIDUAL_RETRY_NOT_RESIDUAL otherwise); G7 tsr-support and tsr-check; VN1; DN5 value; G24 re-derivation of the terminal set and T, GATE_CUTOFF_BEFORE_T, and after-T gate exclusion; G16, G24 and N1 text | Codex1 (A208 item 2(a)) | pinned before Phase-1 step 4 (G1) |
| G26 freeze script (root build) | V-N1 per DN5 | Codex2 (A205 item 10) | before step 8 |
| Root procedures | the dict as receipt_status_classes; G15 copy; copies before every V006 write, from M-15 until c2v007 accepts the cutoff record; the single G24 successor cutoff record on GATE_CUTOFF_BEFORE_T; D4 stops; D7 records for kit calls (path and keys above), each written only after the monitor pid has exited and only with the run volume mounted, a monitor still alive when the kit script exited 5 at its 120 s wait being stopped first; a V006 ruling on each of the three residuals (reading 19), with a RESIDUAL_RETRY line where the ruling is a retry, written only on existence checks made with the run volume mounted; holding a call after MONITOR_REFUSED_TWICE, with a third launch at that k only on a V006 ruling; the hold rule, including NGC tools not on the list (adopted after A212); the TOOL_PIN line in P-112's adoption entry; spec fills for every P-112 call under the blinding guard; NGC ρ point registrations for every member or F point outside S0 at u_A (A211 N3); G16 custody copies of each terminal attempt's result, monitor receipt and attempt receipt at its receipt's close, and of the cut records at step 3, all before pass one, pinned at step 5; the run-volume mount check before any G16 3(a) or 3(b); the A135 item 11 extractor ruling before G7; the G16 Phase-2 SENSITIVITY-only form before Phase-2 pass one; G28 before the first FULL build | none | as listed |
| S0 kit C2V003A | no change | none | none |
