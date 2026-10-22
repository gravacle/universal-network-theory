# P-112 Phase-1 NGC launcher, CX2V001

Date -u: Tue Oct 20 18:42:02 UTC 2026

**FORMAL — authority and scope.** This is Codex2's build for Claude2 dispatch 0781 / 0767 part 3. The brief is P112_LAUNCHER_BRIEF_V005, with ROUND5_DEFECTS_C2V001 items 1–9 taking precedence and 0782 supplying the refusal-log and T12 rulings. Exact authority files and byte hashes are included in the manifest. The build is for coordinator review; root adds the TOOL_PIN only after Claude4's zero-blocking review. Part 5 remains a separate root dispatch.

**TESTED — verification.** Both final runs passed 580/580 checks, including all 229 statically named refusal codes and 35/35 killed mutants. RUN1 and RUN2 TEST_RECORD.json are byte-identical: `50e0951bfe19216e143a8e90785e9569a9fd795334acc1a605144df08d1a5e15`. Their shared date_u is the actual suite-start stamp; each run's EXECUTION_METADATA.json contains its own actual start and finish date -u. REPRODUCIBILITY_PROOF_CX2V001.json binds those records. All tests use synthetic inputs; live tests start only inert fixture processes. Production science was not launched.

**TESTED — delivered bytes.** The launcher is `phase1_ngc_launch_cx2v001.py`, SHA256 `a72d96c150ca1c638474cddba23f5264374c7ae9aa285c3d38ebfb3e61519bb1` (122677 bytes). The standalone suite is `test_phase1_ngc_launch_cx2v001.py`, SHA256 `fd50301bbbe4e4d6e91ad30a4881eaab6f54a1ab77a1856edea04b9d9670b76e` (161740 bytes). HASHES_CX2V001.txt records byte hashes for the review artifacts and cited sources. SOURCE_BYTE_AUDIT_CX2V002.json rechecks all 43 brief references / 42 unique pinned paths.

**FORMAL — command surface.** Every invocation takes `--config <absolute path> --config-sha256 <64 lowercase hex>`. The public commands are:

| Command | Purpose |
|---|---|
| `launch --name NAME [--attempt k]` | Validate and start exactly one root-authorized attempt; never choose a subsequent attempt automatically. |
| `launch --name NAME --dry` | Produce a fresh dry plan, without starting a monitor. TOOL_PIN exempt. |
| `launch --name NAME --attempt k --resume` | Finish custody of an interrupted invocation with an existing launch JSON. |
| `close-attempt --name NAME --attempt k` | Project a validated monitor receipt into the sibling attempt receipt. |
| `assemble-registry [--verify]` | Assemble the actual call set or compare its bytes against the saved registry. |
| `record-monitor-refused --plan PATH --plan-sha256 SHA --work DIR` | Record a clean pre-launch monitor refusal without consuming k. |
| `stop-outside-set --name S0_NAME [--attempt k]` | Stop only a kit-verified outside-set serial and record the stop. |
| `status` | Return advisory status, non-attempts and next-attempt information. TOOL_PIN exempt. |

**FORMAL — configuration.** The exact top-level keys are `schema`, `python`, `v006`, `v006_copy_dir`, `run_volume`, `run_root`, `p112_launch_root`, `s0`, `host_ram_bytes_expected`, `plan_output_primary`, `plan_build_record`, `selection`, `fdplan`, `spec_of_record`, `at0a_pass`, `members`, and `f_points`. Schema is P112_CONFIG_CX2V001; RAM is 137438953472. `s0` contains `launch_root` and `run_root`. Phase-1 inputs are root-supplied `{path, sha256}` pins. Each member supplies `{log_index, role, order, member_id, handoff, fill_dir, eps, gq}`; F rows supply `{label, handoff, fill_dir, eps, gq}` in F0/F1/F2 order. The fixed Python path is the one in the brief. Root supplies already-filled specs; this tool never runs the filler or registers NGC points.

**TESTED — custody and recovery.** Tests cover exact theta bits, signed zero, one-ulp changes, S0 mapping, F de-duplication, the 54-string status map, terminal/retry rules, correct-volume checks, close-before-write gates, nine receipt roles, literal pin grammar, and unchanged kit numbering/order-check behavior. Separate synthetic invocations demonstrate recovery after first-sample failure and after monitor refusal: the same entry is retained, ALREADY_REGISTERED_SAME_SPEC is reported on stderr, k is reused, and a new work directory is used. Resume tests cover live and ended monitors, original/reused invocation PIDs, and mismatches. The same-outdir guard also checks a command-qualified prior sampler before relaunch.

**TESTED — process and output boundaries.** Synthetic tests exercise the sampler's lead/tail, five null cases, refusal/no-receipt bounds, process aliases, PID reuse and qualified stopping. Tests that simulate timeout bounds use an injected clock; the unresponsive-process test intercepts signals. The P112 open audit checks the exercised close paths for run-output reads and sentinel projection. Separate tests reject forbidden path spellings and symlink aliases. The real monitor API is used only with inert synthetic drivers and synthetic output files.

**FORMAL — production gate and semantics.** Every record-producing command, including registry verification and the internal sampler, checks the exact whole-line TOOL_PIN for this tool's bytes and realpath. The process count is a sampled lower bound over the declared 13-tool list; root's HOLD condition supplies whole-interval exclusion, including tools absent from that list whenever adopted. Runtime records use exclusive creation. No root TOOL_PIN or program-control file was written by this build.

**TESTED — interface limits.** INTERFACE_PROOF_CX2V001.json binds the actual c2v006 helper calls. `_launch_registry` accepts the assembled registry and also accepts a different shape-valid theta digest. P112 byte verification refuses changed registry bytes, as 0782 directs. `_receipt` reads all nine roles on the synthetic inside-run copy; c2v006 `_terminal` rejects the true sibling receipt with RECEIPT_NOT_IN_RUN_DIR. No full builder assembly, v003g execution, or slots access was used.

**UNTESTED — production claims and deciding tests.**

| Claim not established here | Deciding test |
|---|---|
| Real driver status behavior | First real close-attempt. |
| Real PLAN theta_engine key set versus export/fdplan, and theta_ngc nuisance spelling | First theta check on the real PLAN output. |
| Full real PLAN–registry theta agreement | Root's first real Phase-1 registry assembly, per 0782. |
| G26 successor acceptance of sibling receipts | Root G26 build and separately dispatched part-5 review. |
| Sampler behavior on the production machine | First P112 attempt. |
| Actual run-volume space for the 292 GiB boundary | The production launch check. |
| Real twin kill-watch operation under the P112 launch root | First twin rerun, if one occurs. |
| Acceptance of a real root-written monitor-refusal record | First kit monitor refusal, if one occurs. |
| Real host-restart or volume-loss no-receipt event | First such event, if one occurs. |
| Real monitor alive without launch JSON at the launch bound | First such event, if one occurs. |

**FORMAL — reproducing the synthetic suite.** Use the pinned Python with `-I -B`, `nice -n 10`, and all six BLAS/thread variables set to 1. The standalone suite requires `--tool`, `--tool-sha256`, `--out` (a new absolute directory), `--run-stamp`, and `--run-stamp-sha256`. The delivered shared stamp is pinned in REPRODUCIBILITY_PROOF_CX2V001.json. The suite needs process-list access and permission to stop only its own inert fixture processes. Existing run directories are immutable; use a new output name for another execution.
