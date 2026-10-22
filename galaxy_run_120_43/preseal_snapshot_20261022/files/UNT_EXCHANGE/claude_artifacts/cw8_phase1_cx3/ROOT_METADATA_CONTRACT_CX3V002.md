# Root metadata contract — CX3V002

date -u: Wed Oct 21 12:57:57 UTC 2026

FORMAL interface description of the reviewed candidate; actual production inputs are UNTESTED. Only Claude2 launches science. The worker selection command itself reads metadata and writes one new choice record. It does not run the comparator or either seed state.

Use the existing P112 configuration key set, schema P112_CONFIG_CX2V004 or P112_CONFIG_CX3CW8V001, with the exact candidate tool registered under an A-numbered section:

```
TOOL_PIN P112_LAUNCHER_CX3CW8V002 <launcher_sha256> <absolute_launcher_path>
SPEC_PIN <ordinary_call_name> <serial_sha256> <absolute_serial_path>
SPEC_PIN <ordinary_call_name>_FULL_CW8 <cw8_sha256> <absolute_cw8_path>
CW8_LICENSE_PIN path=<absolute_license_path> sha256=<license_sha256>
```

Placeholders above are illustrative and must be filled from bytes. One license registration is permitted; no existing scientific source/spec is edited. The cw8 fill spec must already exist and differ from the serial file only by the column_workers token 1→8. All other bytes, including whitespace, stay identical. An existing worker-8 twin spec can be used as the ordinary full-call variant only if that exact-byte rule passes and the separate ordinary full-call SPEC_PIN registers it; the call itself remains a full member/F, never the identity twin.

The license is an immutable object with exactly these keys:
- schema: CW8_PHASE1_LICENSE_CX3V001
- date_u: actual UTC creation text
- scope: FULL_MEMBER_F_CALLS_ONLY
- comparator_record: absolute path and byte SHA256 of the root-approved S0 pair record
- source_pins: exactly the seven named pins in the cited source-pin record (driver, comparator, checkpoint_module, serial_worker, parallel_worker, serial_solver, parallel_solver)
- seed_serial_spec / seed_twin_spec: exact root SPEC_PIN objects for S0_SEED_SERIAL and S0_SEED_CW8_TWIN
- full_rss_multiplier: integer 11

The comparator record must have schema UNT_STEP5_NGC_IDENTITY_PAIR_RECORD_C2V001, verdict SERIAL_EQUALS_PARALLEL_BITWISE_TAIL_ON, bitwise_equal true, iterations_compared [0,1] (integers), nonempty strictly-true checks, empty differing_files/not_ready, values_printed false, and exactly the driver/checkpoint_module/tool/serial_spec/twin_spec pins. The tool pin is the comparator source; worker/solver hashes are also independently verified from source bytes.

The forecast has exactly these keys:
- schema: CW8_PHASE1_FORECAST_CX3V001
- date_u and observed_utc: actual creation text and ISO UTC observation time; age must be 0–900 seconds at selection
- calls: sorted complete list of currently eligible new P112 ordinary call names, after S0 reuse, member/F deduplication and historical/previous-choice exclusions
- host_cores: integer 18; cores_in_use: integer 0–6
- remaining_barrier_h: expectation and upper, finite nonnegative hours remaining on the existing S0/other critical barrier
- scope: exact configuration values for plan_output_primary, plan_build_record, selection, fdplan, spec_of_record, at0a_pass, members and f_points

Root's metadata-only invocation, after candidate adoption and preparation of actual pinned inputs:

```
<approved_python> -I -B <review_launcher> select-workers --config <config_path> --config-sha256 <config_sha256> --forecast <forecast_path> --forecast-sha256 <forecast_sha256>
```

The command selects the full eligible new cohort. It is an admission decision, not a harmless query: omitting a license/forecast or supplying unsupported inputs records serial for that cohort, and that choice will not later be upgraded. Use a fresh forecast at the actual admission decision. The pre-launch dry operation does not itself commit serial. Ordinary root launch/close/assembly commands follow the existing P112 workflow after selection. No driver, monitor, sampler, watch or comparator command was run to verify this interface.

Choices live under the configured launch root's worker_choices directory, one exclusive content-addressed CHOICE record for the cohort. A new config with changed scientific-scope fields cannot reuse it. Preserve that directory and all raw spec/license/forecast pins for restart and final assembly. The roster builder's existing registry_verification inputs name this candidate launcher, the chosen config and the actual assembly record. Its receipt verifier rederives the role and exact bytes. G26 must use its supplied successor to pin the supplied roster builder.

Operational model limit: 1–3 new calls, 12–18 available cores, uniform 0818 costs, and root-managed staging of eight-core A phases. Root should not assume that the selector enforces runtime CPU allocation. Eleven RAM is a monitor accounting cap under the accepted ruling; it is not an empirical aggregate-memory measurement.

Evidence (SHA256 from bytes):
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cw8_phase1_cx3/phase1_ngc_launch_cx3cw8v002.py` — `6de0d06a16a5ffab7b49bc76bc9219d0bfbd67a91020129677a5f4078846f852`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cw8_phase1_cx3/roster_builder_c2v007_cx3cw8v002.py` — `a2d8dc00fd80322a2ba6822648c7399d46e9a4e55bbf309cd2efbc0e33665e7e`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cw8_phase1_cx3/g26_freeze_cx3cw8v002.py` — `332253d215387fa69822be3e96ec38c5bea5c4e6ffae4fabc53b0298ca312e2b`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cw8_phase1_cx3/CW8_SOURCE_PINS_CX3V001.json` — `3cd81174542c7d8d863b3f3aece27b33e15f6372d6b9f4d44918b258e04ecd1d`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cw8_phase1_cx3/cli_cx3v002_run001/EVIDENCE.json` — `bd9fb3781b92605ddaa7832da9af1ca8984c1b4ae6d0816f8ee1db502bd1e6b8`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cw8_phase1_cx3/test_cli_and_custody_cx3v002.py` — `67c02bbe0875a627ca2fd09da751cee5a8915da11ba8124cbe197a763339ecf7`.

0835/A270 amendment: this candidate is the single Phase-1/2 launcher. A first admission or rerun may occur after the Phase-1 reporting cutoff; the Phase-2 deadline alone limits admission and the final monitor wall. Holds take precedence over reporting UNEVALUATED. Bound model_outcome=false records, even with an unrecognized reason, release an uncounted solo rerun; missing records still hold repeated solo failures. Retain earlier cause bytes for later readable classification. Existing REFUSED/BLOCKED fix holds retain their separate release rule. Only the V002 launcher hash is accepted by the new builder; config schema compatibility with CX2V004 does not authorize that older launcher. License/forecast/choice schema names and the raw-spec worker-only rule are unchanged.

Amendment evidence (SHA256 from bytes):
- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0835_2026-10-21_codex3_cw8_v002_fold_P112_F1_F3_fixes.md` — `9ff4686832ffcc3506b4ec92c9782d77003d58cfdd402b85fd3637fc867e2cfc`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cw8_phase1_cx3/BUILD_0835_CX3V002.json` — `00c995e3bfab756e3464115c059f6be4321944de0eebfeb054d928b1b11082c0`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cw8_phase1_cx3/F1_F3_cx3v002_run001/TEST_RECORD.json` — `4436b95e0828908636b6a1ed3b12b9939324d382d511cd5b97a242923e0ed83c`.
