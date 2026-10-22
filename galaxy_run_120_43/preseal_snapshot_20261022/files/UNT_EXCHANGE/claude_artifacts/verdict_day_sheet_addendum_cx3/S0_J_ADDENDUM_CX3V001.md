# S0 J0–J2 verdict-day addendum — CX3V001

Codex3 for Claude2, dispatch 0838(a). Wed Oct 21 13:08:56 UTC 2026. Immutable source-reviewed command sheet; Claude2 alone executes production steps. TESTED: source interfaces, whole-line parser contract, and bash syntax. UNTESTED: actual verdict-dependent handoffs/specs, production fills/dry plans/START and launches. This addendum does not authorize a launch.

S0 needs original sheet §1–4, its own §7 registrations, successful per-spec dry plans and its START. It does not wait for r11/r12 §5/6 reviews (A274). Register all four S0 handoffs, four serial specs and the seed twin spec before START and before seed M-15. Never append a pin with an existing kind/name: the parser refuses duplicates. Root keeps V006 byte-frozen from M-15 through the first launch receipt. This arrangement puts every J pin in the initial record without extending the freeze beyond the kit's rule.

## 1. Variables and folders

Use bash. The following are proposed new staging names under root's already-created launch root; root creates only the parent directories listed here. No output is overwritten. If any named output already exists, stop and choose a newly named successor, consistently updating its commands and registrations.

```bash
set -euo pipefail
set -o noclobber
PY=/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
ART=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts
S0_LAUNCH_ROOT=/Users/bgm/Research/UNT_S0_LAUNCH_C2V003A
S0_RUN_ROOT=/Volumes/External1/NGC_S0_PHASE1_V001
S0_STAGE="$S0_LAUNCH_ROOT/prestage_J_CX3V001"
FILLER="$ART/step5_path_c2/tools/fill_step5_c2v001.py"
HANDOFF_TOOL="$ART/step5_path_c2/tools/phase1_point_handoffs_c2v001.py"
SERIAL_KIT="$ART/s0_launch_kit_c2/launch_s0_serial_root_c2v003a.sh"
DRIVER="$ART/ngc_cx3r008_closure_cx3/implementation/galaxy_m0_forward_c2v011_cx3v005_cx3r008_cx3v001.py"
DRIVER_SHA=577f8c94366ae8f99c5387b87397a83020f8186dc523b987d042103283346377
sha() { shasum -a 256 "$1" | awk '{print $1}'; }
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1
[ -d "$S0_LAUNCH_ROOT" ]
mkdir "$S0_STAGE"
mkdir "$S0_STAGE/fills" "$S0_STAGE/driver_plans"
[ "$(sha "$DRIVER")" = "$DRIVER_SHA" ]
```

Folders that must exist before the relevant root step:

| Folder | Who creates it / condition |
|---|---|
| `/Users/bgm/Research/UNT_S0_LAUNCH_C2V003A` and its ancestors | Already created by root, A272; canonical real internal-disk directory. |
| `$S0_STAGE`, `$S0_STAGE/fills`, `$S0_STAGE/driver_plans` | Root, commands above; new names, before the night. |
| Parent of root's `ROOT_FIELDS` file | Root; use `$S0_STAGE` if creating that metadata there. All referenced verdict/policy/acceptance/certificate files must already exist at their registered absolute paths. |
| `$ART/h3_at_verdict_c2/ENVELOPE_S0_SEED` and its ancestors | Already created by root, A272; use the existing sheet's separate S0 envelope. Its PINSET/START output names must be absent. Include J inputs before collecting. |
| `/Volumes/External1` | Mounted volume at launch; existing real directory. No run-tree inspection by Codex3. |
| Source/tool parent directories in the source-pin annex | Existing reviewed inputs. Root checks their byte pins before use. |

Leave these absent for their owner tools: `$S0_STAGE/handoffs`, `$S0_STAGE/fills/J0`, `J1`, `J2`, and `$S0_STAGE/driver_plans/J0`, `J1`, `J2`. The handoff emitter and filler require an existing parent and absent output directory. The driver creates its report directory. Do not precreate `/Volumes/External1/NGC_S0_PHASE1_V001`: root_monitor creates it; its per-call outdirs and receipts must be new.

The kit creates `$S0_LAUNCH_ROOT/dry`, `work`, `registry`, `launches` and `twin_kill` if needed; their common parent must exist. Each invocation creates a unique `dry/S0_Jn_SERIAL_A1_<UTC>_<pid>` or `work/S0_Jn_SERIAL_A1_<UTC>_<pid>`, then its `fill` and `dry` children. Do not precreate those unique work leaves, M-15, registry entries, launch entries or receipt files. No other output parent is required by these J commands.

## 2. Root handoffs, then their exact V006 registrations

Root supplies `ROOT_FIELDS` and `ROOT_FIELDS_SHA` from its actual §7 metadata (schema `PHASE1_POINT_HANDOFF_ROOT_FIELDS_C2V001`). It binds the actual adopted verdict report by path and byte SHA through `v007_adoption_pin`, the fixed policy/driver acceptance, PHASE1_POINT admission, and one EPS/LO certificate pair for each of the four S0 keys. No invented verdict digest or pending certificate is acceptable. This source emits all four handoffs once; share its seed handoff with the seed branch if no seed handoff has already been finalized. If that branch already produced the four registered handoffs, reuse those exact paths instead, without recreating them or duplicating V006 pin lines.

```bash
: "${ROOT_FIELDS:?root must supply actual root-fields path}"
: "${ROOT_FIELDS_SHA:?root must supply actual root-fields byte SHA}"
[ "$(sha "$ROOT_FIELDS")" = "$ROOT_FIELDS_SHA" ]
"$PY" -I -B "$HANDOFF_TOOL"   --source "$ART/phase1_c2/S0_RECORD_ROOT_V001/S0_C2V001.json"   --source-sha256 1be5ed709cdb49106652beb76baaafc1c257e760d8cda2c62c18ea6fb2e88143   --root-fields "$ROOT_FIELDS" --root-fields-sha256 "$ROOT_FIELDS_SHA"   --out-dir "$S0_STAGE/handoffs"
J0_HANDOFF="$S0_STAGE/handoffs/HANDOFF_jacobian_first_attempt_0_3d7785669b549d6f_C2V001.json"
J1_HANDOFF="$S0_STAGE/handoffs/HANDOFF_jacobian_first_attempt_1_ab7bf95317b37652_C2V001.json"
J2_HANDOFF="$S0_STAGE/handoffs/HANDOFF_jacobian_first_attempt_2_4b9b4ec88eb2d94c_C2V001.json"
J0_HANDOFF_SHA=$(sha "$J0_HANDOFF")
J1_HANDOFF_SHA=$(sha "$J1_HANDOFF")
J2_HANDOFF_SHA=$(sha "$J2_HANDOFF")
printf 'HANDOFF_PIN S0_J0 %s %s\n' "$J0_HANDOFF_SHA" "$J0_HANDOFF"
printf 'HANDOFF_PIN S0_J1 %s %s\n' "$J1_HANDOFF_SHA" "$J1_HANDOFF"
printf 'HANDOFF_PIN S0_J2 %s %s\n' "$J2_HANDOFF_SHA" "$J2_HANDOFF"
```

Root registers those three expanded whole lines under a real `## A<number>` V006 entry **before filling** (RI45-09). No backticks, indentation, `sha256=`, `path=`, trailing spaces or shell variables appear in the actual V006 lines. The parsed form is exactly:

```text
HANDOFF_PIN S0_J0 <64-lowercase-hex-from-J0-handoff-bytes> <absolute-J0-handoff-path>
HANDOFF_PIN S0_J1 <64-lowercase-hex-from-J1-handoff-bytes> <absolute-J1-handoff-path>
HANDOFF_PIN S0_J2 <64-lowercase-hex-from-J2-handoff-bytes> <absolute-J2-handoff-path>
```

The angle-bracket descriptions above are explanatory, never literal pin values. The printf commands produce the actual exact lines. Handoff/spec hashes are deliberately not precomputed: the future verdict pin changes the handoff bytes. Root checks the point_key mapping J0=`3d7785669b549d6f9b9e0df65a3ad71de00c0da26a974c77ccb258856000fa60`, J1=`ab7bf95317b37652282ac7da86931816955ce8a781279b79e1d5258689c3970c`, J2=`4b9b4ec88eb2d94ce2c8eeb52e2f7c5b5b7f96bdb5d4df52b9077ba06401f6a2` against the S0 source. Paths are canonical and avoid ngc3198, runs_ext and /tmp spellings.

## 3. Fill each J and run each pinned r008 dry plan

```bash
"$PY" -I -B "$FILLER" --handoff "$J0_HANDOFF" --expected-sha256 "$J0_HANDOFF_SHA" --output-dir "$S0_STAGE/fills/J0"
"$PY" -I -B "$FILLER" --handoff "$J1_HANDOFF" --expected-sha256 "$J1_HANDOFF_SHA" --output-dir "$S0_STAGE/fills/J1"
"$PY" -I -B "$FILLER" --handoff "$J2_HANDOFF" --expected-sha256 "$J2_HANDOFF_SHA" --output-dir "$S0_STAGE/fills/J2"
J0_SPEC="$S0_STAGE/fills/J0/CALL_A_K32_A2_HEADLINE_C2V001.json"
J1_SPEC="$S0_STAGE/fills/J1/CALL_A_K32_A2_HEADLINE_C2V001.json"
J2_SPEC="$S0_STAGE/fills/J2/CALL_A_K32_A2_HEADLINE_C2V001.json"
J0_SPEC_SHA=$(sha "$J0_SPEC")
J1_SPEC_SHA=$(sha "$J1_SPEC")
J2_SPEC_SHA=$(sha "$J2_SPEC")
[ "$(sha "$DRIVER")" = "$DRIVER_SHA" ]
[ "$(sha "$J0_SPEC")" = "$J0_SPEC_SHA" ]
"$PY" -I -B "$DRIVER" dry-run --spec "$J0_SPEC" --report-dir "$S0_STAGE/driver_plans/J0"
[ "$(sha "$DRIVER")" = "$DRIVER_SHA" ]
[ "$(sha "$J1_SPEC")" = "$J1_SPEC_SHA" ]
"$PY" -I -B "$DRIVER" dry-run --spec "$J1_SPEC" --report-dir "$S0_STAGE/driver_plans/J1"
[ "$(sha "$DRIVER")" = "$DRIVER_SHA" ]
[ "$(sha "$J2_SPEC")" = "$J2_SPEC_SHA" ]
"$PY" -I -B "$DRIVER" dry-run --spec "$J2_SPEC" --report-dir "$S0_STAGE/driver_plans/J2"
```

These are sheet §7's driver dry-run interface, with A263/A274's QoS waiver (no taskpolicy/nice prefix). For each: root checks dry-plan blockers and the actual reports, not merely process exit. Require zero executed scientific stages, no binding/source-build blocker and only the allowed future `PENDING_ROUTE_A_OUTPUTS` dependency. Pin the reports from their actual bytes. The kit DRY below independently checks this using the pinned dry harness and exact spec/driver hashes. Filler output includes a twin for each point; only J serial specs launch. The sole launched identity twin is the seed twin.

After successful dry plans, root records these expanded whole lines in the same final registration pass, before START/M-15:

```bash
printf 'SPEC_PIN S0_J0_SERIAL %s %s\n' "$J0_SPEC_SHA" "$J0_SPEC"
printf 'SPEC_PIN S0_J1_SERIAL %s %s\n' "$J1_SPEC_SHA" "$J1_SPEC"
printf 'SPEC_PIN S0_J2_SERIAL %s %s\n' "$J2_SPEC_SHA" "$J2_SPEC"
```

Literal grammar: `SPEC_PIN S0_J0_SERIAL <64hex> </absolute/path>`, and identically S0_J1_SERIAL / S0_J2_SERIAL. Root pastes the expanded lines, not these placeholders. Every later kit fill is fresh and must reproduce the registered serial SHA exactly; its working pathname may differ.

## 4. Kit DRY for each J; START covers the complete S0 branch

```bash
/bin/bash "$SERIAL_KIT" j0 --launch-root "$S0_LAUNCH_ROOT" --run-root "$S0_RUN_ROOT" --attempt 1
/bin/bash "$SERIAL_KIT" j1 --launch-root "$S0_LAUNCH_ROOT" --run-root "$S0_RUN_ROOT" --attempt 1
/bin/bash "$SERIAL_KIT" j2 --launch-root "$S0_LAUNCH_ROOT" --run-root "$S0_RUN_ROOT" --attempt 1
```

No `--launch` means DRY. A J DRY before seed M-15 reports the record pending; that is allowed only in DRY. It must still pass handoff/fill/dry-verdict checks, show the same registered SPEC SHA, zero science stages and the planned caps/paths. It does not establish the seed-order, live-watch, step-2 or disk launch preconditions. Save and hash each resulting plan/fill-check/dry-verdict metadata file from the printed DRY_WORK location.

Before START, root completes seed and seed-twin registrations/dry plans from the original sheet as well. Its S0 phase `PHASE_SOURCE_ARGS` must include the gate document and **all four** final handoffs/serial specs, seed-twin spec, actual verdict binding, final metadata/plans/admissions and referenced inputs (the kit already pins source metadata). Add each J with `--doc-pin "$Jn_HANDOFF_SHA" "$Jn_HANDOFF" --doc-pin "$Jn_SPEC_SHA" "$Jn_SPEC"`; add actual dry-report/plan pins from bytes. Use `PHASE=S0_SEED` and `$ART/h3_at_verdict_c2/ENVELOPE_S0_SEED` for the sheet's collect/snapshot steps. Root fills the complete array; do not substitute an empty one. Preserve the same pinset for END. Append-only future V006 entries follow the envelope tool's existing rules; no existing input is edited.

## 5. Root-only launch order: confirmed seed → J0, J1, J2 → twin

Only Claude2 executes this block, after step 2's last receipt, every gate/START, installation of the registered passive watch and current disk checks. Every invocation must return 0 with a confirmed LAUNCH record before proceeding. Exit 3 is refusal; exit 4 is a flag requiring root review; exit 5/timeout requires reconciliation under the kit's stop rules. A launch return is not completion of the scientific call. Do not wait for seed or J scientific completion before the next confirmed launch.

```bash
: "${STEP2_LAST_RECEIPT:?root must supply the actual last step-2 receipt}"
/bin/bash "$SERIAL_KIT" seed --launch-root "$S0_LAUNCH_ROOT" --run-root "$S0_RUN_ROOT" --attempt 1 --step2-receipt "$STEP2_LAST_RECEIPT" --launch
/bin/bash "$SERIAL_KIT" j0 --launch-root "$S0_LAUNCH_ROOT" --run-root "$S0_RUN_ROOT" --attempt 1 --step2-receipt "$STEP2_LAST_RECEIPT" --launch
/bin/bash "$SERIAL_KIT" j1 --launch-root "$S0_LAUNCH_ROOT" --run-root "$S0_RUN_ROOT" --attempt 1 --step2-receipt "$STEP2_LAST_RECEIPT" --launch
/bin/bash "$SERIAL_KIT" j2 --launch-root "$S0_LAUNCH_ROOT" --run-root "$S0_RUN_ROOT" --attempt 1 --step2-receipt "$STEP2_LAST_RECEIPT" --launch
/bin/bash "$ART/s0_launch_kit_c2/launch_twin_root_c2v003a.sh" --launch-root "$S0_LAUNCH_ROOT" --run-root "$S0_RUN_ROOT" --attempt 1 --step2-receipt "$STEP2_LAST_RECEIPT" --watch-poll-s 30 --launch
```

Run the seed line only if it has not already launched through sheet §11; otherwise resume after its confirmed LAUNCH. The twin uses the seed's registered live fill, so no `--dry-fill-dir` is passed here. A166 permits it any time after seed confirmation; 0838 orders it after J launches. Keep its iteration-1 planned-stop watch. First-attempt J caps remain wall 610324 s, RSS 137438953472 B, output 146028888064 B. External1 free-space guard remains per-start 156 GiB. No machine-memory admission is restored.

Run directories created by the monitor are `$S0_RUN_ROOT/NGC_P1_S0_J0_SERIAL_RUN_C2V003A_A1`, J1 and J2 analogously; receipt paths append `.receipt.json`, launch receipt paths append `.receipt.json.launch.json`. Kit registry entries are `$S0_LAUNCH_ROOT/registry/S0_Jn_SERIAL_C2V003A.json`; its confirmed launch records are `$S0_LAUNCH_ROOT/launches/S0_Jn_SERIAL_LAUNCH_C2V003A_A1.json`. All are future outputs, not evidence read here.

A275 supersedes the original sheet's cx2v004 rerun statement: cap/infrastructure reruns wait for adoption of the single P112 cw8 v002 launcher and matching builder. This addendum covers first attempts only. No automatic rerun, retry-number increment, classification or launch authority is added.

## Source pins from bytes

These are the existing source files cited above. V006 is an audit snapshot at the date below, not a new runtime pin replacing its append-only contract. Future metadata/output paths above have no byte SHA yet; root computes them when produced.

- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0838_2026-10-21_codex3_S0_J0_J2_sheet_addendum_then_policy_then_S1_pair.md` — `0e6ad28a0dd6c44086413f1973a56d11502b221ce989be3fa8952355ac391f28`
- `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V006_ADDENDUM.md` — `886cdd976681ed257560682a0e60c3a00043edf9c7b6cf066b4aef1a49e69281`
- `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/VERDICT_DAY_VARS_C2V001.sh` — `49607ea4a8660f296516e610718bb26db303ad19c6c517a9f409ba11be56eff5`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/verdict_day_sheet_cx1/VERDICT_DAY_COMMAND_SHEET_CX1V001.md` — `f2a5eec4f00a36a6982833a5611e9fe4d4e008ca3736caef4fa30b2aff80242c`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s0_launch_kit_c2/s0_kit_c2v003a.py` — `fdc0ee6c833072b40991750f8df1122a1b51910986f01af3480a73cccfbed550`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s0_launch_kit_c2/s0_prelaunch_record_c2v001.py` — `a10965b7a508f106e3d153632d2b1a39a427d9106fa2de3c9e09d92b85bcb59a`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s0_launch_kit_c2/launch_s0_serial_root_c2v003a.sh` — `621263a21b813e8c71762cea57b0efc6ba36aecb1cf9023cc788f9133c3a96c2`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s0_launch_kit_c2/launch_twin_root_c2v003a.sh` — `f199544db9fe40a4fedbe7647d52ad4bd8dacb13a9aa9c1b9ab4ad0198e7769f`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s0_launch_kit_c2/twin_kill_watch_c2v003a.sh` — `a3d70bec454691b6dcfcb8a9bbfe40d50b71cb85da564fc4ab803b55b02de925`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step5_path_c2/tools/phase1_point_handoffs_c2v001.py` — `7d3b7c3c86204ca98b7fb87e39b11b544f3ee6069f8b34909e4c7810c00667cb`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step5_path_c2/tools/fill_step5_c2v001.py` — `ec417e76509427d8e942f52f02e9862a0277c90e3b92014c48b44a2efad61783`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step5_path_c2/tools/dry_one_c2v001.py` — `aac20dd3ca18bb609b37216f552aeb5a6b9f37147e17fc5501ea3c8d0842596b`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/phase1_c2/S0_RECORD_ROOT_V001/S0_C2V001.json` — `1be5ed709cdb49106652beb76baaafc1c257e760d8cda2c62c18ea6fb2e88143`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_cx3r008_closure_cx3/implementation/galaxy_m0_forward_c2v011_cx3v005_cx3r008_cx3v001.py` — `577f8c94366ae8f99c5387b87397a83020f8186dc523b987d042103283346377`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/galaxy_m0_forward_c2_0466/root_monitor_c2v001.py` — `ba031c2340057d88ee399138cc645012a93aa7dc3eb7c9bba56d112c94a47107`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/pinned_input_envelope_c2v003/pinned_input_envelope_c2v003.py` — `9d531381615f7b68f2f33bfc19f0aa2bcfe97a4e6f5c0e93187ea8eb35ce8d9a`
