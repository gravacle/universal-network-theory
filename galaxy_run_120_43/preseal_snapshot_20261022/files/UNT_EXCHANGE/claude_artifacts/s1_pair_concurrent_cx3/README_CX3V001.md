# S1 concurrent pair — review candidate CX3V001

Codex3 for Claude2, dispatch 0838(c), A274. Wed Oct 21 13:25:52 UTC 2026.

Ready for Claude3 review, not adopted and not launched. The batch contains exactly `S1_UA_C3T`, then `S1_UA_C4T`, at POST_S1. It admits the second call after the first completed route-A iteration and the normal 60 s poll; it does not wait for the first call to finish. One unchanged machine lock covers both. HEADLINE11's existing guard014, launcher015 and binder011 bytes/pins are untouched.

## Files and behavior

| File in v001 | Change |
|---|---|
| step4_guard_c2v014_s1pair_cx3v001.py | S1-only admission; exact ordered pair and max_active=2. One new helper validates each byte-pinned original single-call admission/plan. `native_preflight` chooses that call's original admission; `core_priority_admission` replays both specs. Other guard functions are AST-identical. |
| step4_launcher_c2v015_s1pair_cx3v001.py | Guard bootstrap pin only, plus explanatory text. Every runtime function is AST-identical to launcher015, including worker, lock, ramp, disk checks, normal QoS, single-thread BLAS, sleep assertions and drain behavior. |
| step4_bind_c2v011_s1pair_cx3v001.py | New `assemble-pair` mode plus new guard pin. Original `bind` function is AST-identical. Assembly copies the two original call objects and references their original admissions; writes a new pair plan and unbound candidate after full validation. |
| s1_pair_root_cx3v002.py | Necessary handoff companion: the old root wrapper also rejects a two-call plan. Default DRY. Preserves registration-in-force, filled K3/K4 specs, both native preflights, step-2/campaign-state checks, inactive process-table check and exclusive prelaunch/outcome records. Uses the new pair launcher. C14's single-call/window restrictions are superseded under A274; no memory gate is restored. |

The two C1s are essential. C3T uses the S1 C1 and KS5 chain; C4T uses the campaign b1 C1. A single shared top-level config would be wrong. New `s1_pair_admissions` maps the two exact case names to the original **bound single-call admission pins** in both parent plan and parent admission. Each child retains its own config, context, adoption policy, direct adapter and source review. The parent's reviewed source map must contain their consistent union plus the new tools and existing S1 replayer. It must not silently replace a source hash.

For each child the guard verifies root authority, exact one-case order/call/caps, source review/bytes, original guard014/launcher015 lineage, identical call data, fill record, V007 binding, core-priority state and ramp. Both spec files are replayed and byte-pinned. Native preflight records are recomputed from their original per-case contexts. Neither spec, theta, certificate, grid, driver, output path, per-call cap nor reading rule changes. Plan JSON is newly serialized; "unchanged call bytes" in test metadata means equal call-object content plus unchanged spec-file byte pins, not byte-equal whole plan serialization.

## Root inputs and commands (all production steps UNTESTED here)

1. Prepare the two original one-call POST_S1 plans and root-bound admissions using the existing S1 fill/plan path and binder011, with distinct appropriate C1s. Both must reference one actual written S1 fill, the same theta/branch/attempt and the same V007. Build native PRELAUNCH records for each. Do not execute their single-call launch commands. Existing single-call plans are provenance inputs to the pair assembler.
2. Claude3/root completes the pair source review for the union of both child `sources`, all four new files in the table, and the existing pinned S1 replayer. Preserve every child source review and admission. Parent review schema/status/verdict/approved_sources remain the guard's existing contract.
3. Root chooses new names under the existing step4 packet directory. Output parents must already exist. The pair launcher log and every child's monitor-log/receipt parent must be real directories under the existing fixed OUTPUT_ROOT on External1; root creates those **parents**, not call outdirs, receipts or log files. The guarded output-root/mounted-volume/free-space checks remain mandatory. The pair batch disk bound is the sum of both output caps plus 20 GiB; each start repeats the per-call cap plus 20 GiB check.

```bash
PY=/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
ART=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts
PAIR="$ART/s1_pair_concurrent_cx3/v001"
BINDER="$PAIR/step4_bind_c2v011_s1pair_cx3v001.py"
PACKET="$ART/step4_launch_packet_cx1"
# C3_ADMISSION_PIN, C4_ADMISSION_PIN and PAIR_SOURCE_REVIEW_PIN are root's absolute path@actual-byte-sha strings.
# PAIR_LAUNCHER_LOG is a fresh absolute path under guard's fixed External1 output root, with an existing parent.
"$PY" -I -B "$BINDER" assemble-pair \
  --c3t-admission "$C3_ADMISSION_PIN" --c4t-admission "$C4_ADMISSION_PIN" \
  --source-review "$PAIR_SOURCE_REVIEW_PIN" --launcher-log "$PAIR_LAUNCHER_LOG" \
  --plan-out "$PACKET/S1_PAIR_PLAN_CANDIDATE_V001.json" \
  --candidate-out "$PACKET/S1_PAIR_ADMISSION_CANDIDATE_V001.json"
"$PY" -I -B "$BINDER" \
  --final-plan "$PACKET/S1_PAIR_PLAN_CANDIDATE_V001.json" \
  --admission-candidate "$PACKET/S1_PAIR_ADMISSION_CANDIDATE_V001.json" \
  --plan-out "$PACKET/S1_PAIR_PLAN_BOUND_V001.json" \
  --admission-out "$PACKET/S1_PAIR_ADMISSION_BOUND_V001.json" \
  --command-out "$PACKET/S1_PAIR_EXECUTOR_COMMAND_V001.sh"
```

Assembly/bind grant no launch authority. All output files are exclusive-create; use entirely new names after a partial failure. No cleanup/overwrite/retry is performed. With inactive campaign children, the assembler supplies the same pinned S1 replay contract explicitly for the pair. With active children it must exactly match their existing overlap contract. Both child core-priority states must agree; the root launch config must match them.

After independent root publication of the exact **parent** admission digest, populate `UNT_STEP4_ADMISSION_PATH`/`UNT_STEP4_ADMISSION_SHA256`. Root computes `PAIR_PLAN_PIN` from the bound plan bytes; `REGISTRATION_PIN` is the existing implemented S1 registration; `V006_PIN` names the actual constant root file at its current byte SHA; `S1_LAUNCH_CONFIG_PIN` binds schema UNT_S1_LAUNCH_CONFIG_C2V002 with campaign_state ACTIVE/INACTIVE and step2_route_a_state INACTIVE. The C14 campaign_window is not required by the successor.

```bash
"$PY" -I -B "$PAIR/s1_pair_root_cx3v002.py" \
  --plan "$PAIR_PLAN_PIN" --registration "$REGISTRATION_PIN" --v6 "$V006_PIN" \
  --launch-config "$S1_LAUNCH_CONFIG_PIN" --record "$S1_PAIR_DRY_RECORD"
```

Require ADMITTED and all applicable checks PASS. Freeze/snapshot the complete final pair input closure with its two child admissions/plans/preflights, both C1s, fill, specs, source review, controls and tool pins. Root records the current S1 phase START and preserves the same pinset for END. This build does not freeze a future S1 C1 or sign its pending KS5 policy review.

Only after adoption, root publication, successful real dry preflight, START and root's go-ahead does Claude2 invoke the same wrapper with a **new** record path, `--launch --confirm <actual bound-plan sha>`. Use the pair wrapper as the root handoff; the binder's command file documents its underlying executor and must not be used to skip S1 registration/state/prelaunch-record checks. The old s1_launch_root_c2v002c wrapper remains unchanged and cannot receive the pair plan. Neither of the two old single-call commands is launched.

The wrapper writes its prelaunch record before starting the pair launcher and an outcome afterward. A failed outcome write retains the actual LAUNCHED/SPAWN_FAILED state with an error; it does not falsely imply no process started. Launcher return is not scientific completion. Root follows both monitor receipts. Any cap/infrastructure/failure reading keeps the existing root ruling and no-automatic-retry rules. The existing S1 reader accepts the original spec/prelaunch/output references, which the pair preserves.

## Validation

TESTED on final source paths: **53/53 functional controls + 15/15 integration/root-handoff controls = 68/68**. No scientific process was started, and no real volume/run tree or observed velocity was read.

- Full guard and binder admission on both distinct synthetic C1s; both native preflights rechecked at actual worker polls/starts. Wrong batch/cases/order/max_active, caps, core-priority, memory field, authority/source review, child pin, replay bytes and context swaps refuse.
- The actual worker starts C4T while C3T is active, under a real scratch flock, with only subprocess/clock/disk stubs. A systemic first-call failure drains before a second call; a second batch cannot acquire that lock. All launcher runtime functions are AST-identical to launcher015.
- Integration uses the actual S1 filler/replayer, KS5 and b1 wrapper/certificate-policy paths over synthetic certificate worlds. Identity normalization and custody return are the disclosed inherited test seams; actual source modules are read under the guard fence. Both exact filled specs pass their own C1 and fail swapped C1s. No scientific driver normalization or geometry is executed.
- Pair root DRY, registration/state/step2/inactive-process checks, active-without-C14-window admission, confirmation refusal, existing-record refusal and simulated outcome-write failure are covered. The "launch" branch test uses an in-memory process stub; zero real child processes.
- **4/4 targeted mutants detected:** allow max_active 1/3; remove child authority; remove child caps binding; force C3 context for both calls. The last fails the positive fixture at assembly and emits no suite record; its captured traceback is included. Mutation evidence uses draft guard/launcher bytes that are byte-equal to the final guard/launcher; binder differs only by final directory pins.

UNTESTED: real S1 u_A fill, actual S1 C1/KS5 signed policy and campaign C1 source closures, real mounted-volume/disk/process checks, production preflights/START/launch, contention and performance. Deciding checks are Claude3's review and root's real pair DRY using the eventual signed inputs. The proposed 11–18 h saving is root's forecast, not a measurement here.

Development disclosure: the first synthetic suite was 49/51 because its worker harness omitted the synthetic publication environment; test successor v002 supplies it and passes 53/53. No guard/launcher/binder correction was needed. Root wrapper v001 is an unused development file; v002 preserves launch status if its outcome record cannot be written. All predecessors/drafts remain immutable.

## Pins from bytes

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s1_pair_concurrent_cx3/v001/step4_guard_c2v014_s1pair_cx3v001.py` — `1274a39a19a7d8540858b8f45be0b683e776fa4fc1386bec10871bb0342ac6cc`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s1_pair_concurrent_cx3/v001/step4_launcher_c2v015_s1pair_cx3v001.py` — `2e41da3746053f073d3c775de29c5c8df156deaa861e2b774ee88d7ab96808aa`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s1_pair_concurrent_cx3/v001/step4_bind_c2v011_s1pair_cx3v001.py` — `f57f5f1db134a6b50bce4b950a01ad8c7145ad71db3a45bb20334dde99c9b7c4`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s1_pair_concurrent_cx3/v001/s1_pair_root_cx3v002.py` — `c08b5b789a3c89a64e0ef3eae7d455d4aacd2112fe0268ad346f8a239b634b6b`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s1_successors_c2/step4_guard_c2v014.py` — `6efdca016416a919b25a1e23d46a415b75fe2b5e60145ba098f864730975165d`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s1_successors_c2/step4_launcher_c2v015.py` — `cd987edd097323999847208d7b5fdfd93dadecb8a10beb6feaf91a0c53b68e0b`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s1_successors_c2/step4_bind_c2v011.py` — `d3d9702eb8096d11b98461f1c62c67931b9ecf74957cee95fbc3a60f60deaea0`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s1_successors_c2/s1_path_lib_c2v002c.py` — `99e2be175e546992c70984435bc480e1eddb90b052fda65ddcbfe8780bdbd27e`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s1_successors_c2/s1_launch_root_c2v002c.py` — `d4e310138c3c2a068d6a963d32c230a52cdca4467ece8e60de39fce3b5955684`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s1_successors_c2/README_S1_PATH_C2V002C.md` — `135a0426d297a34a7aa2f766efc1bc4fe7c460bde1429ad02e0dccf8ab4a31d0`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s1_successors_c2/test_s1_path_c2v002c.py` — `e6a5782912f920776aad3e479027688868c8f3b12766f3a7ca37bcbb59f9ec8c`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s1_pair_concurrent_cx3/test_s1_pair_cx3v002.py` — `4918ed05d1a8cb87c13ba0dcba33d1f5228bfdbd57905647285190af7e3e2623`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s1_pair_concurrent_cx3/test_s1_real_replay_cx3v002.py` — `36076fdb2fe2a13caf997666bd4f464a5eafdc3ba1285896e006f8fcca1b73bf`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s1_pair_concurrent_cx3/v001_functional_test001/TEST_RECORD.json` — `6879a9ef59c88adcadd6b47531441989bf02b80d5be99c34c1ffc755aeda256d`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s1_pair_concurrent_cx3/v001_real_replay_test002/TEST_RECORD.json` — `a4b62e7e59d69c68c168ce953ddc1f7a8dc9fa5bb343f437c7c929e1605e4584`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s1_pair_concurrent_cx3/build_s1_pair_cx3v001.py` — `ca04b815c00a3e053b0ab2637cd9363b9c09302cf3aaab912b3c8091c6928242`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s1_pair_concurrent_cx3/v001/BUILD_RECORD_CX3V001.json` — `7923cd28c66a52408e3f895920a733f693cdee4721b898117fda7ef42b8e72d1`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s1_pair_concurrent_cx3/MUTATION_RESULTS_CX3V001.json` — `f710c6650b02e23a73fbe2fb8b9afa9028757ae0db93034d68cc0bba6851ebd2`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s1_pair_concurrent_cx3/MUTATION_DEFINITIONS_CX3V001.json` — `9e0f4df44695264f71dc76044386bf3fd9ba31bb5025fb726379096ae04d21b4`
- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0838_2026-10-21_codex3_S0_J0_J2_sheet_addendum_then_policy_then_S1_pair.md` — `0e6ad28a0dd6c44086413f1973a56d11502b221ce989be3fa8952355ac391f28`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s1_pair_concurrent_cx3/DIFF_step4_guard_c2v014__S1PAIR_CX3V001.diff` — `e3284d572db0ed93162085f9b170e29cdf338c8b4d739fc5e43d8a1ccb0466c5`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s1_pair_concurrent_cx3/DIFF_step4_launcher_c2v015__S1PAIR_CX3V001.diff` — `b1f1c7a8c6bd2f61290729ab4aa9ff073d76bd1a75615ba9b4d2f24e27e1e3e8`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s1_pair_concurrent_cx3/DIFF_step4_bind_c2v011__S1PAIR_CX3V001.diff` — `78a54635fa55f6b18581c77b16ed5e488ec28d87ee3d7d1481c0c947dbb7ccf9`
