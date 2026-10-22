# CX2V003 README contract text

date -u: Tue Oct 20 20:23:13 UTC 2026

**FORMAL — implementation contract.** Dispatch 0789 governs CX2V003, retaining 0784–0786 and the V005 brief except where explicitly changed. The whole-line TOOL_PIN name is `P112_LAUNCHER_CX2V003`. Claude2 is the sole scientific launch owner. This contract describes the implementation and its limits; test results are reported separately.

**FORMAL — bytes and observations.** Immutable inputs are read once per command through guarded snapshots. Validation, hashes and quoted fields use that same buffer. Monitor and work metadata read through `read_record` additionally require realpath equality and one hard link. Failed opens are not observations. Launch JSON polling, a fresh post-bound observation, and V006 gate/cutoff reads are separate volatile observations, each read once. Records expose observation counts and last observed pins. Cutoff copies use the exact source buffer and reject hard links. The production V006 path remains fixed; its live gate read has its explicitly retained special handling.

**FORMAL — work-log boundary (A09).** Work logs are guard-read only. Work logs are not checked for realpath equality. Only the logs of a refused invocation that never started its own driver may be hashed. This permission belongs to that invocation's work directory; a same-k relaunch does not change it. Other guard-read-only paths include the existing cutoff-record summary, M15 custody and kit registry; the realpath check is not a blanket claim about every read. The command audit checks byte-read counts and forbidden spelled/resolved paths within the parent process.

**FORMAL — process handling (V1, F-a–F-e).** The sampler no longer raises MULTIPLE_MONITORS. Before monitor_pid.json exists it uses the plan's exact monitor argv and requires pgid == pid. Once present, that metadata is read once and subsequent monitor matches are filtered to its PID. A pgrep-form liveness probe cannot terminate sampling or extend monitor liveness. Resume and null-PID liveness use exact argv plus pgid == pid; the existing refusal for multiple exact live matches remains outside the sampler. Blank-command ps rows are valid and uncounted. Command tokens use whitespace splitting only; ps text is not shell-quoted input. Invalid UTF-8 ps bytes use surrogateescape. Unknown candidate identity files must be regular and at most 8 MiB; descriptor metadata is checked before a bounded read, with nonblocking open to avoid FIFO replacement hangs.

Kit kill-target captures bytes with a 30-second timeout. Exit 1 means ALREADY_ENDED only for valid stderr JSON with alive:false, a valid launch child PID, and a process table containing neither that PID nor the planned driver command. Malformed stderr, timeout or inconclusive liveness gives NOT_KILLED_TARGET_REFUSED. Signals still require qualified ownership and are rechecked before each signal. Launch JSON container and consumed field types are checked before use; malformed shapes produce LAUNCH_JSON_FORM or LAUNCH_JSON_FIELD_FORM.

**FORMAL — interrupted refusal custody (A06).** MONITOR_REFUSED keeps its exact shared key set. Its observation sibling is exclusively created first, with its hash in the parent's rule token. A crash leaving a sibling without its parent is refused as ORPHAN_OBSERVATIONS_SIBLING by status and retry. No file is overwritten or silently reused. Existing parent records still require the sibling's presence and verified bytes. A coordinator must resolve the orphan by an explicit successor procedure.

**FORMAL — remaining Lens-1 changes.** Both s0.launch_root and s0.run_root receive config-time realpath checks. Close requires the solo sample's monitor_receipt pin to equal the receipt actually checked. IMPLEMENTATION_REVISION and v006_gate_observation were removed. Runtime schemas and filenames retain the authorized V005 forms listed below.

**FORMAL — retained V005 interfaces, authorized by 0786.**


| Category | Retained identifiers |
|---|---|
| Config and synthetic manifest | P112_CONFIG_CX2V001; P112_SYNTHETIC_PINS_CX2V001 |
| Internal evidence | P112_DRY_VERDICT_CX2V001; P112_THETA_CHECK_CX2V001; P112_SAMPLER_FIRST_CX2V001; P112_INVOCATION_CX2V001; P112_MONITOR_PID_CX2V001; P112_STATUS_CX2V001 |
| P112 records | UNT_P112_LAUNCH_PLAN_CX2V001; UNT_P112_LAUNCH_REGISTRY_ENTRY_CX2V001; UNT_P112_LAUNCH_RECORD_CX2V001; UNT_P112_MISLAUNCH_RECORD_CX2V001; STEP5_REGISTRY_ASSEMBLY_RECORD_CX2V001 |
| Shared schemas | STEP5_SOLO_SAMPLE_CX2V001; STEP5_ATTEMPT_RECEIPT_C2V001; STEP4_CUTOFF_RECORD_C2V001; STEP5_LAUNCH_REGISTRY_C2V003; MONITOR_REFUSED_ATTEMPT_RECORD_C2V001; S0_OUTSIDE_SET_STOP_RECORD_C2V001 |
| Refusal launcher field | P112_CX2V001; writer name is now P112_LAUNCHER_CX2V003 |
| Run and attempt names | NGC_P1_&lt;NAME&gt;_RUN_CX2V001_A&lt;k&gt;; P112_&lt;NAME&gt;_&lt;LAUNCH/MISLAUNCH/MONITOR_REFUSED&gt;_CX2V001_A&lt;k&gt;.json |
| Registry / outside stop / assembly | P112_&lt;NAME&gt;_CX2V001.json; &lt;NAME&gt;_A&lt;k&gt;_CX2V001.json; STEP5_LAUNCH_REGISTRY_PHASE1_CX2V001.json; STEP5_REGISTRY_ASSEMBLY_RECORD_CX2V001.json |

Existing kit C2V003A naming, Step-4 cutoff naming, and spec/fill filenames retain their brief forms. These are format identifiers; the executable and its required TOOL_PIN are CX2V003. A CX2V001 adoption line is neither needed nor accepted as this executable's gate.


**FORMAL — invocation.** Commands retain the V005 config pin and argument forms: launch, dry launch, launch --resume, close-attempt, assemble-registry [--verify], record-monitor-refused, stop-outside-set and advisory status. The internal sampler uses the same adoption gate. Dry launch and status are gate-exempt as specified. Root supplies filled pinned inputs; P-112 does not fill specs or register scientific points. There is no automatic retry.

**FORMAL — A226 item 2 disclosure.** Pinned executables are hashed in the parent, then executed by path in child processes. The root integrity envelope covers those later child reads. An in-process audit does not prove child executable buffer identity. Volatile observations, counter identity reads and the tool's own-sha read are separately classified in the single-read audit.

**UNTESTED — production scope.** Synthetic fixtures and static checks do not establish real scientific outcomes, production host sampling, actual volume loss/restart, a real twin watch, full real PLAN/registry assembly, slots or v003g behavior, or G26 successor acceptance. Process detection is sampled and limited to the declared tools and supported forms; arbitrary relative/suffixless copies and unquoted paths with spaces are not comprehensively identified. Root's whole-interval HOLD remains necessary. The c2v006 helper theta/residence limitations remain for the separately dispatched G26 review.

**FORMAL — reproduction.** Use the pinned Python with -I -B, nice -n 10, and all six prescribed BLAS/thread variables set to 1. The standalone suite takes --tool, --tool-sha256, --out (a new directory), --run-stamp and --run-stamp-sha256. Tests use only synthetic saved states and inert fixture processes authorized by the brief. No real scientific driver, target, /Volumes path or network is used. All existing artifacts remain immutable; every successor and run uses a new name.
