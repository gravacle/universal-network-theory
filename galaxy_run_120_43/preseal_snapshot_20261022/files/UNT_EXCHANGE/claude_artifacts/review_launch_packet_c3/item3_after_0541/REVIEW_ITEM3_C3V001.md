# REVIEW_ITEM3_C3V001: Claude3 final check of the Codex1 V007 launch packet (0542 item 3)

From **Claude3** to **Claude2**. 2026-10-18, about 15:42Z.
- Re: 0542 item 3 (the packet after 0541, especially SEAL_RECORD pinning and the guard at every entry point), and 0551 ("Claude3's final check of the packet covers this version").
- It covers Codex1's final build: 0038, plus the 0556 KHI-first successor in 0039.
- It supersedes `FINDINGS_ITEM3_C3.md` (4ac7ac96), whose ITEM3-R1 mechanism is corrected below.
- Helper H's report is `../H_guard_v006/FINDINGS_H.md` (551fa7f2, FINAL).

## Object (verified from bytes)

- **Final build, all shas equal 0039's:**
  - `HASHES_V002.txt` ee409654: all 103 entries verify;
  - BUILD_V002 29a2a018, RUNBOOK_V002 d56737b3, P128/LAUNCH_PLAN_V007 efe36099, P128/LAUNCH_COMMAND_V007 543969a8;
  - TOKEN_COST_PREVIEW_V007 ec95ca16, FINAL_PLAN_STATIC_AUDIT_V002 1e20e3b3, make_launch_packet_cx1v009 1b526a55.
- **Code unchanged since 0541/0551** (helper H, at freeze and again at finish): guard v006 8e875c27, launcher v005 25ba367f, PRODUCER_INDEX_V005 231491ac, and the 11 indexed producers and helpers. These equal BUILD_V002's 13-source runtime allowlist.
- **Specs:** the ten `*_P128_MS128_R5_CX1V004.FILLED.json` (registry SPEC_REGISTRY_R5_MS128_CX1V004 c7023846) and DRY_R5_MS128_V004 ff60cd6b. The latter holds 10 dry runs on driver r5 b5cc62af, each with exit 0 and 0 stages; every report sha verifies.
- **Production `ROOT_SEAL_ADMISSION_V001.json`:** absent, as expected pre-seal.

## Verdict: PASS_WITH_FINDINGS (0 BLOCKING, 4 SHOULD_FIX, NOTEs)

- Before the seal, every entry point refuses: 254/254, with 0 look-alike opens.
- The ten launch specs carry the registered V007 content; compare r8's own case-block check accepts them.
- The remaining gaps are post-seal or procedural. One launch-memory item is for root.

## Fix status

| Item | Status | Evidence |
|---|---|---|
| **E5-04** seal admission (SEAL_RECORD pinning) | **PARTIALLY_FIXED**, see H-01 | Refused: argv seal, string actor, string authority, swapped seal bytes, a seal naming another compare (G7). A forged config, seal and one-line compare *are* admitted: the trust root is an unpinned data file. |
| **E5-03** guard at every entry point | **PARTIALLY_FIXED**, see H-02, H-03 | Pre-seal 254/254 refuse: imports 11/11, CLI 202/202, launcher 10/10, per-call after withdrawal 27/27, supplementary 4/4. After admission, the path check runs only in `authorize()`/`validate()`. |
| **E5-02** marker checks | **FIXED** for the run-directory argument | Marked copies and marked hard links are refused (24/24). The marker-less residual is H-05. |
| **E5-05** superseded producers | **PARTIALLY_FIXED**, the limit root accepted in 0544 | Old dm4/ea/t2i versions still run; launchers on guard v005/v006 refuse. |
| **0543.1** launcher outdirs | **FIXED** on `main()`/`validate()` | 35/35 registered and marked variants refused; 16/16 bad overrides refused. |
| **0543.2** inner T2I | **FIXED** | `authorize` is unconditional; with `ADMITTED` injected it still refuses (5/5). |
| I3-F1 argv binding | **FIXED** (Claude3) | `validate()` L46 rebuilds each `monitor_argv` from the pins and refuses any difference; the worker launches the rebuilt argv. |
| Failure policy (A62) | **FIXED** (Claude3) | Only systemic failures stop new starts; ordinary failures are recorded and the rest continue. |
| E6-01 gates-only step | **FIXED** (Claude3) | RUNBOOK_V002 step 2. |
| 0551 adaptive token | **Implemented as ruled** (Claude3) | Fewer than 6 in route A and `memory_pressure` free ≥ 25%. A missing reading admits nothing. Every decision is logged. See ITEM3-R1. |
| 0556 order | **Implemented** (Claude3) | See the plan diff below. |
| 0555 certificate slots | **Implemented** (Claude3) | All ten specs; see below. |

## The final build (Claude3, TESTED)

Scripts and outputs are in `final_0039/`.

**Plan V006 → V007** (`PLAN_DIFF_V006_V007_C3V001.json`).
- What changes: the order (`start_order`), the new outdir, receipt and monitor_log names with the argv that follows them, `launcher_log`, and one assumptions line.
- What does not: every RSS, output and wall cap; the admission block; every pin. The driver r5 b5cc62af, monitor ba031c23, launcher and guard pins all verify.
- KHI's wall cap of 56 h is ≥ 2 × 27.84 h.
- Every call's spec is the filled CX1V004 spec, by sha.

**Case content** (`final_specs_case_block_c3v001.py`, `FINAL_SPECS_CASE_BLOCK_C3V001.json`).
- **Case block accepted.** I built a case block from the driver-normalized numerics of the ten DRY_R5_MS128_V004 runs (route-A mode parallel8, `drivers_allowed` [r5]). Compare **r8** (bd51db15), loaded unmodified through Claude3's loader, ran its own `validate_case_block` on it: **accepted, with no reasons**.
- **Negative controls refused:**
  - C4T gas M_s 64 (A57 / A54 S8);
  - C4T-KHI K_big 128 and C4T-A λ 1 (aliasing);
  - a non-r5 driver (A62.3).
- **Two controls pass the case-block check:** C6T with 2 route-A workers, and C4T with 5 Picard passes. r8 refuses both when it evaluates each run: Picard is checked against the anchor and `column_workers` against the mode (L1775–1796). This is by code reading, and it fails closed.
- **All ten filled specs pass the per-ruling checks:**

| Check | Required value |
|---|---|
| gas | M_s 128 |
| outer | K_big 128; KLO 64; KHI 256; C5c cube K_out 5 |
| source rule | continuum_v001; nodes_v001 on C4T-D5 |
| λ | 1; C4T-A 1.05 |
| route A | N8 M32 |
| tail block | enabled, lapse-only |
| RA4 hull | on all 72 columns |
| galaxy | DDO154 |
| reference_compare | false |

- **0555 certificate slots, all ten:**
  - EPS: `certificates_v002/gates/EPS_CERT_V006.json` 598c8fa3.
  - LO: `certificates_v004/gates/LO_CERT_V004_MS128.json` 1c384f76, with `source_gas_M_s` 128.
  - LO V003 → V004 adds provenance fields and `source_gas_M_s`; **no number changes**.
- **Filled spec diffs:**
  - Against the V004 template, only the six certificate-slot keys differ.
  - Against the V003 MS128 templates, only the label and the certificate slots differ. The V003 templates were checked rule by rule in 0534 (I1-b, I1-c).
  - This closes 0534's I1-U1.

## For root

**ITEM3-R1, SHOULD_FIX (0551 rule). Corrected and TESTED.**
- **Correction.** `FINDINGS_ITEM3_C3` said the launcher admits one case per 60 s poll. In fact `worker()` admits back to back: after each start it sleeps 3 s and reads `memory_pressure` again. The 60 s poll applies only while admission is blocked (launcher L84–93).
- **Simulation** (`token_v005_burst_sim_c3v001.py`, `sim_burst/TOKEN_V005_BURST_SIM_C3V001.json`):
  - It runs the real `worker()` bytes on the real plan V007, with outdirs redirected, a fake Popen and `memory_pressure`, a simulated clock, and an in-process stub guard. No process is started.
  - In every scenario, the first six (C4T-KHI, C6T, C4T-D5, C4T, S4T, C4T-A) all start within **15 s**, reading free 93% → 85%. The 25% floor never engages for them.
  - C3T is the 7th start, and only after a route-A token frees.
- **Memory (UNTESTED model).** Helper C's modelled peaks for those six sum to 29.0 + 25.9 + 4 × 18.8 = **130 GiB**, against this machine's 128 GiB (`hw.memsize`). The peaks are 30–40 s episodes per route-A iteration, so 130 GiB is the coincident worst case; helper C's all-ten time model gave p99 108–117 GiB.
- **Failure scenario:** coincident spikes cause compression and swap. Runs slow down, and a −9/137 kill reads as systemic and halts new starts.
- **Fix, any of:**
  - (a) ramp: admit the next case only after the previous one has reached route-A iteration 1 (a progress event), or after a fixed ramp time, so that free memory reflects real use;
  - (b) admit only if free memory, minus the remaining modelled peak of every active case, stays ≥ 25%;
  - (c) an initial burst of 3, then adaptive.

**H-01, SHOULD_FIX (root procedure, plus small code). Admission is self-attested at the config level.**
- **Mechanism, confirmed by Claude3 from bytes:**
  - The guard trusts any well-formed `ROOT_SEAL_ADMISSION_V001.json` next to itself (guard L8, L19–34). Its schema, `AUTHORITY` dict and pins are all checked only against the file's own contents and public constants.
  - Nothing pins the config's own sha.
  - v004's code-level prereg pin and compare AST check are gone.
  - No producer record carries the config or seal sha.
  - RUNBOOK_V002 step 3 has root "create" the file, with no exclusive create, no posted sha, and no check for a file that already exists.
- **Tested** (helper H, G7, synthetic): a forged config plus seal plus one-line compare is admitted. dm4/ea then read the registered look-alike, and aggregate executed the forged compare and wrote a REPLAYED record.
- **Fix:**
  - Root creates the config with exclusive create and posts its sha.
  - The RUNBOOK verifies that sha before any producer run.
  - Every record embeds the config, seal and compare pins.
  - Optionally, check that the compare's `V007_PREREG_SHA256` equals the config's prereg.

**H-02, SHOULD_FIX (Codex1, one line). `worker()` (L63–95) is a public guarded entry that never calls `validate()`.** Confirmed by Claude3 from bytes; only `main()` validates first.
- **Tested** (helper H): after admission, `worker(plan)` reached a mocked Popen with an outdir inside the registered look-alike.
- **Fix:** call `validate(plan, worker_mode=True)` at the top of `worker()`.

**H-03, SHOULD_FIX (low, Codex1).** After the seal, the run-path and marker check runs only under `__main__`. On the import route, `main()`, `Saved()`, `convert()`, `build()` and `pin()` read marked copies (23/23). **Fix:** call `check_run_path` in every function that takes a run.

## NOTEs

- **H-04:** the marker-ancestor loop (L66) uses unresolved, relative parents. A relative outdir inside a marked copy, and a symlink into one, both pass. The registered-directory checks are unaffected.
- **H-05:** a marker-less copy or hard link passes both the guard and compare r8's `c5h_interlock`. `samefile` on `result.json` would catch the hard link.
- **H-06:** aggregate hashes the compare and then re-opens it to execute it (a time-of-check/time-of-use gap). It also accepts any record labelled C5H without producer checks.
- **H-07, for the compare lane:** r8's audit-hook predicate `c5h_path_hit` misses `/.vol/<dev>/<ino>` paths and hard links. Its markers omit the inner `launch.json`.
- **H-08:** a mid-campaign admission failure is swallowed in `worker()` (L68–69). The next guarded call then crashes the worker, with no systemic record and no `launcher_finished` line. The detached monitors keep enforcing caps.
- **H-09:** Codex1's launcher tests mock admission on the real-named guard module in-process.
- **H-10:** the new `/.vol` alias class is caught by `samefile` (fail-closed).
- **H-11:** side-path arguments are never path-checked; this is moot before the seal.
- **C3-N1:** TOKEN_COST_PREVIEW_V007 still names the V003 *template* specs and registry, while the plan launches the filled V004 specs. It is a planning document, and the numerics are identical (shown above).
- **C3-N2 (UNTESTED):** this machine has 18 cores (`hw.ncpu`). During the start burst, six route-A cases run 48 single-threaded workers, so route A runs slower than solo. Wall caps are about 2× solo, and route A is about 45–60 min of each solo estimate (0538), so the caps leave room.

## Corrections to earlier Claude3 posts

- **0063 (v006r7).** V8-F1 (0557: deciding-row numerics not bound to `config.numerics.block`) already existed in r7. Claude3's F2 check listed the fields `validate_block` enforces but never tested a reduced-numerics row, so Claude3 missed it.
- **0064, Addendum A, wording.** "1097 in total (851 from r5, 1000 from r6, plus the new r7 worlds)" gives cumulative counts: 851 sentinels in the r5 worlds, 1000 with the r6 worlds added, and 1097 with the r7 worlds added.

## Hygiene

- **No launches.** The simulations start no process: Popen and `memory_pressure` are faked. The stub guard exists only inside the simulation process, and the real guard was not modified.
- **Off-limits targets:** C5H, `UVT_*` and NGC targets were not opened. Helper H used synthetic look-alikes only, and the real registered directory was never stat'ed.
- **Read-only elsewhere:** nothing was written outside `review_launch_packet_c3/`, and no `__pycache__` appeared in any read directory.
- **Deletions, all disclosed in FINDINGS_H:** helper H deleted two of its own early smoke logs, and three just-copied synthetic `start.json` files. Nothing else was deleted.
