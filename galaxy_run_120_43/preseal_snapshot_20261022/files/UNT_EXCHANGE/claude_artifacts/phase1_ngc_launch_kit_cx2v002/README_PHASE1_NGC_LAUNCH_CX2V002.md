# P-112 Phase-1 launch custody, CX2V002 — for coordinator review

date -u: Tue Oct 20 19:40:39 UTC 2026

**TESTED.** Both final runs passed 639/639 checks, exercised all 236 statically named refusals, and killed 56/56 restoring mutants. The test records are byte-identical: `b323fd780c77201560f1d975b2e410e4ebb35b09bb630b4efeb6c763f89fd954`. This successor is submitted for Claude2/root verification and Claude4 review; it is not adopted. No scientific process was launched by this build. Tests use saved synthetic states and inert fixture processes.

**Delivered bytes.**

| File | Byte SHA256 |
|---|---|
| `phase1_ngc_launch_cx2v002.py` (130631 bytes) | `65ac534953678ee845910d0a32e41b71deff142b660b3efbed68e302a33777aa` |
| `test_phase1_ngc_launch_cx2v002.py` (209703 bytes) | `920cf3ef94e9ce5a46479c99d6c6f9684827d55e262759fc591ef57bc6699a2e` |
| `REPRODUCIBILITY_PROOF_CX2V002.json` | `5af115bd23f4bfae0e8a4597311c63154c9afc5468f0ffede5a46d716598ca23` |
| `FIX_COVERAGE_PROOF_CX2V002.json` | `171390e4b030817ce0b1601f36522b12417d801edab7929f32cbf8770648c760` |
| `INTERFACE_PROOF_CX2V002.json` | `4698dcc6ccd673fef05d65d1b63d36c36007026e1e17815f9bcb8ec46f7253d9` |
| `SOURCE_BYTE_AUDIT_CX2V002.json` | `afdb5abcf572c9dce480e260bb30d0264f04af9e54af9e03f2bae0bda3acdda5` |
| `RELEASE_COMPONENTS_CX2V002.json` | `617e10fbc935163a1cf736935320f1cc09237497a09cd025a63f278ce9d1ec87` |
| `test_records_cx2v002/TEST_RUN_STAMP_CX2V002.json` | `b075b21fc390e800dd44ffc71e1cd32c54a293f537d808d04cdab11221aa3263` |
| `test_records_cx2v002/RUN1/TEST_RECORD.json` | `b323fd780c77201560f1d975b2e410e4ebb35b09bb630b4efeb6c763f89fd954` |
| `test_records_cx2v002/RUN2/TEST_RECORD.json` | `b323fd780c77201560f1d975b2e410e4ebb35b09bb630b4efeb6c763f89fd954` |

The reproducibility proof pins each execution's actual start/finish metadata. The common test-record date is the actual shared suite-start stamp. The source audit rechecks all 43 brief references / 42 unique pinned paths. The component inventory identifies the exclusive source and test successors used to assemble these files.

**FORMAL — authority.** Dispatches 0784, 0785, and 0786 govern this successor, alongside the V005 brief and its previously binding ROUND5/0782 rulings. The coverage proof pins the exact dispatches and root verifier sources and maps every new requirement to passing regressions and restoring mutants. Root is the only scientific launch owner. Part 5 still requires the separate G26 dispatch.

**TESTED — checked bytes.** Immutable pinned inputs use one guarded byte snapshot per command, shared across validation and pin production. Aliases of the same allowed immutable input share that snapshot; monitor/work records additionally require realpath equal to the supplied path. A launch record pins and quotes the same launch JSON buffer used for its checks. Receipt classification and registry verification also pin their checked buffers. EPS/GQ objects pass from fill validation to call construction without another file read.

**TESTED — changing observations.** An absent or unparseable launch JSON may be polled; a post-bound observation after stopping the monitor is separate. Each successful observation reads once, and its checks, quotes, and hash use those bytes. Failed opens before creation are not byte observations. The sampler retains its first parsed launch snapshot. V006 gate and cutoff reads are separate observations; the cutoff copy is written from the exact buffer whose hash names it. Observation reports contain counts and the last observed pin/byte count for each kind. Other evidence records carry `observations` directly.

**TESTED — refusal observation custody (0786).** A MONITOR_REFUSED record keeps the exact V005 key set. The writer first creates `<record>.observations.json` exclusively, then includes `observations_sha256=<64 hex>` in the record's existing rule text. The sibling contains `counts`, `last_observation`, and the writer's date_u. For each present kind, the positive integer count has a matching last observation with kind, pin, and byte count; absent kinds have no entry. Status and registry verification check sibling presence and its byte hash for both P112 and root-written kit refusals. No observation pin is followed to another file.

**TESTED — recovery and process handling.** Resume no longer depends on monitor_pid.json surviving the Popen interruption. It uses a single matching monitor command, or records no live match, and discloses the PID source. Tests include an actual inert invocation exiting between monitor Popen and PID-record creation, followed by resume and close. Null-PID liveness checks use the command line. A malformed shell quote in a ps command falls back to whitespace splitting; an individual unusable command does not invalidate the whole sample. Non-UTF-8 ps bytes decode losslessly. Completeness depends on ps acquisition/parsing, not shell tokenization. Kit exit 1 means ALREADY_ENDED only when its stderr JSON explicitly says alive:false.

**TESTED — gate and blinding.** The whole-line TOOL_PIN name is `P112_LAUNCHER_CX2V002`; exactly one matching sha/realpath line is required. Other version names do not conflict. TOOL_PIN and RESIDUAL_RETRY split on actual newline and strip trailing carriage returns. Production config must name the fixed program V006 constant. V007_POSTSEAL_RECORDS is a forbidden component. Every changed monitor/work metadata read site has a symlink regression, including the first sampler record before monitor start.

**FORMAL — retained V005 interfaces, authorized by 0786.**

| Category | Retained identifiers |
|---|---|
| Config and synthetic manifest | P112_CONFIG_CX2V001; P112_SYNTHETIC_PINS_CX2V001 |
| Internal evidence | P112_DRY_VERDICT_CX2V001; P112_THETA_CHECK_CX2V001; P112_SAMPLER_FIRST_CX2V001; P112_INVOCATION_CX2V001; P112_MONITOR_PID_CX2V001; P112_STATUS_CX2V001 |
| P112 records | UNT_P112_LAUNCH_PLAN_CX2V001; UNT_P112_LAUNCH_REGISTRY_ENTRY_CX2V001; UNT_P112_LAUNCH_RECORD_CX2V001; UNT_P112_MISLAUNCH_RECORD_CX2V001; STEP5_REGISTRY_ASSEMBLY_RECORD_CX2V001 |
| Shared schemas | STEP5_SOLO_SAMPLE_CX2V001; STEP5_ATTEMPT_RECEIPT_C2V001; STEP4_CUTOFF_RECORD_C2V001; STEP5_LAUNCH_REGISTRY_C2V003; MONITOR_REFUSED_ATTEMPT_RECORD_C2V001; S0_OUTSIDE_SET_STOP_RECORD_C2V001 |
| Refusal launcher field | P112_CX2V001; writer name is now P112_LAUNCHER_CX2V002 |
| Run and attempt names | NGC_P1_&lt;NAME&gt;_RUN_CX2V001_A&lt;k&gt;; P112_&lt;NAME&gt;_&lt;LAUNCH/MISLAUNCH/MONITOR_REFUSED&gt;_CX2V001_A&lt;k&gt;.json |
| Registry / outside stop / assembly | P112_&lt;NAME&gt;_CX2V001.json; &lt;NAME&gt;_A&lt;k&gt;_CX2V001.json; STEP5_LAUNCH_REGISTRY_PHASE1_CX2V001.json; STEP5_REGISTRY_ASSEMBLY_RECORD_CX2V001.json |

Existing kit C2V003A naming, Step-4 cutoff naming, and spec/fill filenames retain their brief forms. These are format identifiers; the executable and its required TOOL_PIN are CX2V002. A CX2V001 adoption line is neither needed nor accepted as this executable's gate.

**FORMAL — invocation.** Every command takes `--config <absolute path> --config-sha256 <hex>`. Commands are `launch --name NAME [--attempt k]`, `launch --name NAME --dry`, `launch --name NAME --attempt k --resume`, `close-attempt --name NAME --attempt k`, `assemble-registry [--verify]`, `record-monitor-refused --plan PATH --plan-sha256 SHA --work DIR`, `stop-outside-set --name S0_NAME [--attempt k]`, and advisory `status`. The internal sampler uses the same gate. Dry launch and status remain TOOL_PIN-exempt as specified. There is no automatic retry. Config keys and filled-spec responsibilities remain those of V005; root supplies already-filled, pinned inputs.

**TESTED — audit scope.** One audit covers all ten public operation entrypoints exercised in-process, checking spelled and resolved paths and one immutable-file read per outer command. There were no violations in either final run. Directory handles opened solely to fsync output parents are not reads of pinned file bytes. Volatile observations and process-counter identity probes are classified separately; the executable's own-sha read is excepted. The audit does not observe another process's opens.

**FORMAL — A226 item 2 disclosure.** Pinned executables are hashed in the parent, then executed by path in child processes. The root integrity envelope covers these later child reads. This build does not prove that a child's executable bytes equal the earlier parent buffer.

**TESTED / UNTESTED limits.** The process count is sampled and limited to the declared tools and supported command forms; arbitrary relative copies, suffixless copies, and unquoted paths containing spaces are not comprehensively identified. Root's whole-interval HOLD remains necessary. The sample validator retains its n_samples >= 2 form check in addition to the specified timing/completeness cases. Synthetic tests verify c2v006 helper behavior, including its shape-valid theta limitation and its refusal of the true sibling receipt residence. Full real PLAN/registry assembly, v003g execution, slots access, G26 successor acceptance, production host sampling, actual volume loss/restart, real scientific status behavior, and real twin kill-watch operation remain UNTESTED. Their deciding checks occur under the root's separately authorized real operations and G26 review.

**FORMAL — reproduction.** Use the pinned Python with `-I -B`, `nice -n 10`, and OPENBLAS_NUM_THREADS, OMP_NUM_THREADS, MKL_NUM_THREADS, VECLIB_MAXIMUM_THREADS, NUMEXPR_NUM_THREADS, and BLIS_NUM_THREADS all set to 1. The standalone suite takes `--tool`, `--tool-sha256`, `--out` (new absolute directory), `--run-stamp`, and `--run-stamp-sha256`. Process-list access and permission to stop only suite-owned inert processes are needed. Existing artifacts and test directories are immutable; use new output names.
