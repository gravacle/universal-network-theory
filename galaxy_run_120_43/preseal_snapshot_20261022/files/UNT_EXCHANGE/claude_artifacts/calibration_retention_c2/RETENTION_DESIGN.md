# Calibration retention sweeper c2v001: design, consumer proofs, tests

Claude2 lane, retention track, 2026-10-17. Tool: `retention_sweeper_c2v001.py`. Status: **READY_FOR_CHECK**. Nothing real has been removed. Every test ran on synthetic call directories under `test_runs/`.

## 1. Authority and scope

The principal's decision is recorded in `UNT_PROGRAM_CONTROL/CURRENT_INSTRUCTIONS.md`, last section, under this heading (the tool requires the exact line):

`## Principal: intermediate cleanup authorized for calibration calls — 2026-10-17 ~17:50Z`

- **Scope:** calibration forward calls only, meaning calls under the calibration orchestrator's work dir. A call qualifies only after it has completed and been verified.
- **May be removed:** route-A checkpoint blobs, node diagnostics and stage arrays.
- **Always kept:** result.json, receipts, specs, logs, and a full sha256+size manifest written before anything is removed.
- **Reproducibility:** every call stays recomputable bit for bit from its pinned spec and driver.
- **Never touched:** the anchor, convergence, deciding, REPRO, NGC and CODEX1 runs.

`--apply` refuses unless `--authorization` equals that heading and the heading appears verbatim in the instructions file. The sha256 of that file is recorded in every manifest and record. Without `--apply` the tool only plans: it reads and writes nothing else.

## 2. Layout assumptions (explicit and configurable)

From orchestrator c2v001 (L640-713, L842-846, L1054), c2v002 (L1112, L1347-1434, L1563, L1747) and campaign_c2v001 (L4, L137-147). The layout is identical in c2v001 and c2v002 (as of 250c988a):

```
<work_dir>/CONFIG_COPY_<sha16(config bytes)>.json
<work_dir>/cache/<cache_id>/{CACHE_HEADER.json, entries/<theta_key>.json}
<work_dir>/waves/wave_NNNN/{WAVE_PLAN.json, WAVE_RESULT.json, campaign/}
<work_dir>/waves/wave_NNNN/campaign/call_NNNN/{spec.json, RECEIPT.json(.launch.json|.stdout.txt|.stderr.txt),
                                               monitor.stdout.txt, monitor.stderr.txt, out/<driver output>}
```

- **Driver output:** c2v003c and c2v006 share one layout, `out/stages/NN_<name>/...` (c2v003c L957-961; c2v006 L834-839).
- **Confirmed** on the anchor and on REPRO_PINNED_FULL (read only).
- **Overrides:** every name is in `LAYOUT_DEFAULT` and can be overridden with `--layout L.json`. The layout sha256 is recorded in the manifest.
- **Orchestrator adapters:** selected by the config schema (`..._CONFIG_C2V001` or `..._C2V002`). The orchestrator module is pinned on the command line (`--orchestrator`, `--orchestrator-sha256`).
- **Sweeper output:** written only inside `<call>/RETENTION/`. Files are `MANIFEST_PRE_RETENTION.json`, `RETENTION_RECORD.json`, `ATTEMPTS.jsonl`, and a `.lock` held with flock.

## 3. Whitelist and consumer proofs

Globs are relative to the call outdir `<call>/out` and are matched one segment at a time. The bytes and file counts come from the anchor A2_ANCHOR_F10_RUN_V001, using read-only stat in `--estimate-from` mode (`evidence/ESTIMATE_ANCHOR_A2F10_V002_all.json`).

| Rule | Glob (under `out/`) | Tier / authorized as | Anchor bytes (files) |
|---|---|---|---:|
| W1 | `stages/[0-9][0-9]_route_a/checkpoint/blobs/*.npy` | route_a_checkpoint_blobs / route-A checkpoint blobs | 1,263,074,048 (22) |
| W2 | `stages/[0-9][0-9]_route_a/attempt_[0-9][0-9][0-9]/arrays/*.npz` | route_a_attempt_arrays / stage arrays | 1,128,708,288 (24) |
| W3 | `stages/[0-9][0-9]_route_a/attempt_NNN/node_diagnostics/iteration_*_nodes.jsonl` | node_diagnostics | 1,231,362,847 (6) |
| W4 | `stages/[0-9][0-9]_offset/offset/unit_nodes/iteration_*_nodes.jsonl` | node_diagnostics | 706,068,951 (3) |
| W5 | `stages/[0-9][0-9]_offset/offset/{offset_prepared,source_offset,unit_response,updated_base_arrays}.npz` (4 rules) | stage_chain_arrays / stage arrays | 263,919,368 (4) |
| W6 | `stages/[0-9][0-9]_*_rotation/rotation/rotation_base_arrays.npz` | stage_chain_arrays | 346,935,986 (4) |
| W7 | `stages/[0-9][0-9]_*_feedback/feedback/{feedback_prepared,gas_source_feedback,refreshed_prepared}.npz` (3 rules) | stage_chain_arrays | 949,548,710 (9) |
| **Total** | | | **5,889,618,198 (72)** of 6,081,118,006 |

**Never removable, even if a glob were widened** (`NEVER_REMOVE_*`):
- any `result.json`, `finish.json`, `start.json`, `request.json`, `failure.json` or `FAILURE.*`;
- `IDENTITY.json`, `COMPLETED.json`, `START.json`, `*.end.json` and `*.start.json`;
- `operator_identity.json`, `progress.jsonl`, `checkpoint.lock`, `call_spec.json` and `seed_*`;
- all `*.txt` and `*.log` files, `spec.json`, and `RECEIPT*` and `monitor.*`.

Directories are never removed.

**Also kept on purpose (small; read by evidence or useful as records):**
- the checkpoint iteration records `iteration_NNNN/*.json` (about 74 MB), which pin every blob by sha256;
- `body_arrays.npz` (3.4 MB);
- `column_*_source.npz`;
- reference/body radius JSONs;
- the route-A attempt `result.json` (44.6 MB).

### 3a. Who reads each whitelisted file, and that nothing does after the call is final

**While the call runs** (the only time these files are read), every stage subprocess reads the earlier stages of the same call. Its `request.json` argv shows this on the anchor:
- body, offset, columns, rotation and feedback take `--checkpoint-directory .../01_route_a/checkpoint`, which uses W1 through the checkpoint module `_get` (coupled_gas_checkpoint_c2v003 L236-253);
- columns, rotation and feedback take `--offset-directory`, which uses W5;
- feedback takes `--rotation-directory`, which uses W6;
- the next pass reads the feedback output, W7;
- c2v006's `deciding_test_verdict` and `reference_comparison` (L2008-2101) compare this call's arrays with the CODEX1 saved chain in-run, and record the verdict in result.json;
- W3 and W4 are written only (worker v002 L105 `node_log_directory=out/'node_diagnostics'`, offset stage L227 per v002/DISK_OPTIONS_V001.md s1). They are pinned nowhere: v002's DISK_OPTIONS reports this as TESTED on the anchor;
- W2 is not read by any route-B stage. The attempt `result.json` and `progress.jsonl` reference its array shas, so those references become dangling.

**After the call is final** (receipt FINISHED and the cache entry written), every consumer that re-reads a call directory, and exactly what it reads:

| Consumer | On | Reads from the call dir | Whitelisted file read? |
|---|---|---|---|
| root_monitor_c2v001 `verify_receipt` (L203-224) | verify | RECEIPT.json, result.json | no |
| root_monitor_c2v001 `run_monitored` (L123-124) | (re)launch | refuses if the outdir exists, so a driver can never run into a retained outdir | no |
| driver c2v003c `cmd_run` / c2v006 `cmd_run` (L2189-2190) | run | refuses an existing outdir | no |
| campaign_c2v001 resume (L117-128, `_record_from_receipt` L59-71) | resume | RECEIPT.json, spec.json, result.json; launches only absent call dirs (`mkdir(exist_ok=False)` L138) | no |
| orchestrator c2v001 `CampaignExecutor.classify` (L715-767) | ingest | RECEIPT.json (L726), spec.json (L736), result.json (L743) | no |
| orchestrator c2v001 `Cache._verify` (L457-473) | every cache open (run/plan/status/resolve) | result.json bytes (L466-468) | no |
| orchestrator c2v001 `orphans` (L652-669) | resume | RECEIPT.json, RECEIPT.json.launch.json, only for calls without a receipt | no |
| orchestrator c2v001 `finalise`/`summary` (L1086-1188), replay (Probe L572-636) | replay/record | cache entries, WAVE_PLAN/WAVE_RESULT; the engine is fed from the cache only | no |
| orchestrator c2v002 `collect_evidence` (L667-775) | ingest | `stages/` and `checkpoint/` listings (L683, L698-700), `attempts/*.end.json` (L694-695), `iteration_NNNN/COMPLETED.json` (L705-708), `iteration_NNNN/FAILURE.*.json` (L709-712), `attempt_000/failure.json` (L714-716), route_a `request.json` (L718-719) and the seed file it names (L722-725), failed-stage `*/failure.json` (L741-744), `*_columns_NN/columns/finish.json` (L753-755), `reference/finish.json` (L762-764) | no, and directories are kept |
| orchestrator c2v002 `Cache._verify` (L1139-1190) | every cache open | result.json (L1158-1169); every evidence file hash (L1170-1172) | no; E7 also refuses any overlap |
| orchestrator c2v002 `orphans` + `live_processes` (L214-240, L1364-1388) | resume/resolve | RECEIPT.json, launch record, process table | no |
| engine calibration_region_engine_c2v003a | probe/replay/record | observation region (L571), its own record/registry (L2768-2790, L2797-2917); forward values come from the orchestrator cache | no call-dir file |
| freeze prediction_freeze_c2v003a `_pin_files` (L2444-2460) | freeze | caller-supplied code/input files (query manifest + DDO154 region required, L2315-2341) | no call-dir file |
| driver dry-run `saved_runs` (c2v003c L138-155, c2v006 L227, L2403) | dry-run/replay | hard-coded CODEX1 saved-chain dirs, never a calibration call | no |
| driver c2v006 `admit` (L744-769, L1646-1690) | a later run whose spec admits this call's route A | attempt + checkpoint dirs of the admitted call (needs W1) | **yes, if a spec names the call.** The calibration mapper never changes `admit` (c2v001 L93-94, L414-420; c2v002 L91, L1096-1100), and E8 refuses any call named by any spec or wave plan in the work dir |
| replay tools parallel_route_a_c2/replay (stage_replay_inputs L10, L26-35) | real-data replay | blobs of the A2 anchor run (hard-coded), never a calibration call | no |
| checkpoint module `_scan`/`open_run` (L325-370, L466) | route-A resume | lists blobs; used only by a worker resuming that checkpoint. The driver always starts a fresh checkpoint (`--start-iteration 0`) | no |

**Lost capability (DECLARED, not hidden).** After retention, a call cannot be re-verified from its intermediates, and its route A cannot be admitted into another run. Any pin-walking re-check of the stage chain (start/finish sha pins of the removed npz) also fails. Re-derivation is possible only by re-running the pinned driver on `spec.json`.

The manifest keeps sha256+size of every removed file. Blob names are their own sha256 (checked on one anchor blob, `f39af55c…`; coupled_gas_checkpoint_c2v003 L16, L227). The kept iteration records also pin them. So a future recompute can be checked against the manifest at the blob level. NPZ file bytes cannot be compared this way: they carry zip timestamps (c2v006 L2008-2010).

## 4. Bytes freed per call, and calls affordable at 233 GB free

Measured from the anchor (6,081,118,006 bytes in 4,336 files; receipt-side files add about 0.19 MB). Free space is taken as 233×10⁹ bytes. The v001/v002 config disk guard is 8 GiB per call plus a 20 GiB reserve.

| Categories removed | Freed per call | Residual per call | Calls affordable (space only) | Wave 12: space / v001-guard limit | Wave 24: space / guard |
|---|---:|---:|---:|---:|---:|
| none | 0 | 6.081 GB | 38 | - | - |
| node_diagnostics | 1.937 GB | 4.144 GB | 56 | 45 / 38 | 39 / 25 |
| + route_a_attempt_arrays | 3.066 GB | 3.015 GB | 77 | 57 / 47 | 45 / 25 |
| + route_a_checkpoint_blobs | 4.329 GB | 1.752 GB | 132 | 91 / 73 | 61 / 27 |
| **all (authorized scope, default)** | **5.890 GB (96.85 %)** | **0.1915 GB** | **1,216** | **735 / 578** | **366 / 52** |

How the columns are computed:
- **Space only:** `(free − 20 GiB − w × 6.081 GB) / residual + w`. A whole wave sits at full size until it is ingested, because retention needs the final cache entry.
- **Guard limit:** `(free − 20 GiB − w × 8 GiB) / residual + w`. This is the point at which the orchestrator's HALTED_DISK rule (c2v001 L961-966) starts refusing a wave of size w.

What the table shows:
- With the full authorized scope, 120 calls need about 23 GB of residual plus one in-flight wave.
- The binding limit is the disk guard for waves of 24 or more (52 calls), not the space itself.
- The narrower tiers alone cannot hold 120 calls at 233 GB.

A modelled worst call (k=7, P=6) is about 9.5 GB (v002/DISK_OPTIONS_V001.md s2). Its whitelisted fraction is UNTESTED; the deciding measurement is the first real `plan` output on such a call.

## 5. Eligibility, removal protocol, crash safety

**E1-E8** are listed in the module docstring and enforced in `Env.eligibility`, `Env._structure_ok` and `Env.tree`. Each one fails closed: any unreadable fact makes the call ineligible.

- **Live processes:** found in the `ps` command lines (the sweeper's own ancestry is excluded), from the launch-record child pid, and with `lsof +D`. macOS `lsof +D` exits 1 even when it prints PIDs (observed), so only exit codes above 1 count as failure.
- **Orchestrator verification:** done in process with the pinned orchestrator module itself. `Cache._verify` runs on the re-read entry. `CampaignExecutor.classify` is re-run on the call and must reproduce the cached class, failure class, forward record and every provenance field it emits. For c2v002 that includes taxonomy rule/code and evidence-file hashes.
- **Pins that must still resolve:** the driver bytes, the receipt's spec pin, every `out/start.json` static pin, and the spec's coefficients pin.
- **Default classes:** only VALID entries with driver_status COMPLETED are retained. MODEL_INVALID/INVALID calls need `--include-model-invalid`, so failures are preserved by default. INFRA and NUMERICS_LIMITED calls are never cached, so they are never eligible.

**Apply sequence:**
1. Take a per-call flock.
2. Append to `ATTEMPTS.jsonl`.
3. Hash every file and write `MANIFEST_PRE_RETENTION.json` (tmp, fsync, rename onto an absent name, dir fsync). Re-read it and verify its self-hash and content.
4. Unlink only `removable` files under `out/`. Parent directories are opened with `O_NOFOLLOW|O_DIRECTORY`. Before each unlink the inode, size and `nlink==1` are re-checked. Files with `nlink>1` are kept and reported.
5. Re-hash every kept file against the manifest. Confirm the removable files are absent and no unexpected file exists. Re-run E1-E8, including receipt, cache and classify.
6. Write `RETENTION_RECORD.json` last, then re-read and verify it.

**States:**
- **FRESH:** no manifest.
- **PARTIAL:** a manifest but no record. The call is detectable by `plan`, which reports `already_removed`. A rerun checks every remaining file against the manifest (a changed kept file or an unexpected file refuses), then completes and records `removed_in: earlier_attempt`.
- **RETAINED:** both files present, self-hashes valid. A rerun is a no-op; `--verify-retained` re-checks.

## 6. Tests (synthetic only; final run `test_runs/RUN_20261017T181724Z_32257/TEST_RESULTS.json`)

**74 tests, 74 PASS, 0 FAIL.** The run used sweeper a40f413f, mock driver 254800ca, orchestrator c2v001 51895c04 and c2v002 250c988a (bytes at test time), monitor ba031c23, campaign 71274ceb, and taxonomy 25d188df.

The calls were produced by the real pinned campaign and monitor with a mock driver that writes the anchor layout in small files (at most 2 concurrent calls, so at most 4 worker processes). They were ingested by the real orchestrator `classify` and `Cache.put`.

| Group | n | What was tested |
|---|---:|---|
| U (unit) | 3 | Whitelist on 30 paths (anchor names and near misses); unsafe paths; tier selection |
| S | 1 | 18-call synthetic wave through campaign + monitor + c2v001 ingest |
| A (c2v001, adversarial) | 57 | Plan writes nothing; per-call refusals:<br>• symlink to an outside file, symlinked stage dir (E7)<br>• tampered result.json, tampered receipt self-hash, tampered spec.json (E3)<br>• no cache entry, two entries, MODEL_INVALID default, wave not ingested (E4)<br>• broken static pin (E6)<br>• live process naming the call, file held open (lsof), launch child pid alive (E5)<br>• call named by another wave plan's admit block (E8)<br>• symlinked wave dir into a protected sibling, `..`, outside path, relative path (E1)<br>Authorization: missing, wrong line, absent heading, authorization without apply.<br>Clean apply:<br>• removed set equals an independent recomputation; kept files byte-identical<br>• manifest and record verify; monitor `verify_receipt`, c2v001 `Cache._verify` and `classify` identical<br>• idempotent rerun; verify-retained; hardlink kept<br>Crash handling:<br>• crash mid-removal, after manifest, before record; reruns complete; kept-file change and unexpected file refuse<br>Work dir = real anchor, real CODEX1, synthetic A2_ANCHOR/KMAX sibling, or the runs dir: all refused.<br>Protected sibling and outside files byte-identical. |
| B (c2v001, consumers) | 7 | Full sweep retains 3 calls; c2v001 `Cache.open(create=False)` passes; real campaign resume gives RESUMED_OK ×3 with launched 0; re-ingest identical; rerun no-op; verify-retained; kept bytes identical |
| C (c2v002) | 6 | c2v002 classify: 2 VALID + 1 MODEL_INVALID (R10 reads the iteration dirs and end record); default sweep skips MODEL_INVALID; with the flag it is retained; c2v002 `Cache.open` (F2 + evidence hashes) passes; classify identical incl. evidence; no evidence file is whitelisted |

Earlier runs `RUN_20261017T181309Z_26665` and `RUN_20261017T181335Z_27076` are kept as found. They are failed iterations of the test file: an lsof exit-code handling bug in the sweeper, since fixed, and a stale taxonomy pin in the test. Neither is a reference run.

## 7. Claims register

| Claim | Status | Deciding test if UNTESTED |
|---|---|---|
| Whitelisted files are read by no orchestrator/engine/freeze/monitor/campaign code path after the call is final | TESTED-POSITIVE by code reading (lines in s3a) and on synthetic calls (A25-A26, B02-B04, C04-C05) | - |
| Real calls of driver c2v006 match the layout and whitelist | TESTED-POSITIVE on the anchor and REPRO_PINNED_FULL layouts (estimate mode, read-only); UNTESTED on a c2v006 calibration call (none exist) | First real wave: `plan` must list exactly the W1-W7 files and zero refusals other than E5 for running calls |
| Retention keeps every call recomputable bit for bit from spec+driver | UNTESTED. The tool guarantees only the prerequisites: spec, driver bytes and static/coefficient pins resolve (E6, TESTED-POSITIVE/-NEGATIVE on synthetic A02.c17); spec and receipt are kept | Root relaunches one retained call's `spec.json` with the pinned driver into a fresh dir. Compare `speeds_km_s` bitwise with the kept result.json, and the recomputed blob sha256s with the manifest's W1 entries |
| A c2v002 change that reads a whitelisted file at ingest is caught | Defence in depth. E7 overlap check plus classify identity plus post-verify. The direct E7 overlap path is UNTESTED (unreachable with c2v002 250c988a) | A c2v002 variant whose `collect_evidence` hashes a node-diagnostics file; `plan` must refuse with E7/E4 |
| Bytes freed per call 5,889,618,198 (96.85 %) | TESTED-POSITIVE on the anchor (MEASURED); on real calibration calls UNTESTED | Sum of `bytes_freed` in the first RETENTION_RECORDs |
| macOS `lsof +D` exits 1 with PIDs printed | TESTED-POSITIVE (observed; A18) | - |

## 8. How root runs it (root launches; plan first)

```
PY=/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
S=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calibration_retention_c2/retention_sweeper_c2v001.py
O=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calibration_orchestrator_c2/v002/calibration_orchestrator_c2v002.py
nice -n 10 $PY -I -B $S --orch-config <RUN_CONFIG.json> --orchestrator $O --orchestrator-sha256 <sha of O>      # plan
nice -n 10 $PY -I -B $S --orch-config ... --orchestrator ... --orchestrator-sha256 ... \
    --apply --authorization "## Principal: intermediate cleanup authorized for calibration calls — 2026-10-17 ~17:50Z"
nice -n 10 $PY -I -B $S --orch-config ... --orchestrator ... --orchestrator-sha256 ... --verify-retained
```

- Run between waves, after each wave's WAVE_RESULT.json exists. It is safe while the orchestrator runs the next wave: E5 skips any call a process references, and nothing the orchestrator re-reads is removed.
- Today both real configs refuse in plan mode because their work dirs do not exist yet (`evidence/REAL_CONFIG_PLAN_V001_C2V00{1,2}.json`).

## 9. Disclosures

- **Stray write.** One test stdout log was written to `/tmp/claude-501/ret_test.log`, outside the output dir. It was copied to `evidence/TEST_STDOUT_RUN_20261017T181541Z.txt` and left in place (no deletion).
- **Unread files.** No NGC3198 file was opened. No result.json of a protected run was read except the A2 anchor's own `result.json` keys/`stage_records` and `start.json` static pins, which are permitted.
