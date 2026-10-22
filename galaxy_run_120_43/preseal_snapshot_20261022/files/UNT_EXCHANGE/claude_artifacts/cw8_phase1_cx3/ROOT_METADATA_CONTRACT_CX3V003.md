# Root metadata contract — CX3V003

date -u: Wed Oct 21 13:37:52 UTC 2026

FORMAL interface description of the reviewed candidate; actual production inputs are UNTESTED. Only Claude2 launches science. The worker selection command itself reads metadata and writes one new choice record. It does not run the comparator or either seed state.

Use the existing P112 configuration key set, schema P112_CONFIG_CX2V004 or P112_CONFIG_CX3CW8V001, with the exact candidate tool registered under an A-numbered section:

```
TOOL_PIN P112_LAUNCHER_CX3CW8V003 <launcher_sha256> <absolute_launcher_path>
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


0842/A281 operational rules:

- Exactly one CW8_LICENSE_PIN line is permitted and is never superseded. A license change requires a new tool version.
- A Phase-2 change to any bound scope field requires a new config under a root V006 event.
- The selector takes an exclusive flock on the launch root's persistent empty `.worker_choices.lock` inode, refreshes cached calls, then reads and publishes choices while holding the lock. Preserve the inode; never remove or replace it during use. No stale-lock cleanup is needed: process exit releases the kernel lock.
- A concurrent cohort selection that finds all calls already chosen refuses CW8_NO_NEW_CALLS; default-serial selection returns ALREADY_SELECTED. Neither writes a second choice.
- Malformed forecast/comparator JSON, shapes, values and numeric overflow durably select serial within otherwise valid selection custody. This does not promise a write when the work root, gate, source custody or filesystem is itself unavailable.
- S0 historical attempt specs bind by SHA256; honest fresh fill paths with the same bytes are accepted. Ordinary full-cw8 choice authentication still requires its exact root spec pin.
- The Phase-1 snapshot builder refuses SNAPSHOT_SOLO_FAILED_CAUSE_REQUIRED if an eligible solo FAILED attempt lacks a monitor-bound cause record. A valid model_outcome=false cause with an unknown reason satisfies this binding requirement. Missing/null or incorrectly bound records do not.
- Phase 1 remains a reporting cutoff; Phase 2 alone bounds admissions and monitor wall. Existing cause/fix holds and the worker-only raw-byte spec rule are unchanged. This builder accepts only the v003 launcher hash.

Evidence (SHA256 from bytes):
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cw8_phase1_cx3/phase1_ngc_launch_cx3cw8v003.py` — `4d5b47e75f90241460dd0b86155ddae2267117c31f6043fc57777ea94564919d`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cw8_phase1_cx3/roster_builder_c2v007_cx3cw8v003.py` — `f710334b6f5ec2663fbebd826c7b326ebf7ff9eb600e751584de4f518a4e0b11`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cw8_phase1_cx3/g26_freeze_cx3cw8v003.py` — `171710bb5428d7baa9e05fda049c1095239ea5461eae351abbbacea1d608fa89`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cw8_phase1_cx3/CW8_SOURCE_PINS_CX3V001.json` — `3cd81174542c7d8d863b3f3aece27b33e15f6372d6b9f4d44918b258e04ecd1d`.
- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0842_2026-10-21_codex3_cw8_v003_F2_sha_only_plus_hardening_before_0838c.md` — `704951f325ca1adb8de119d6a624c1ab7f6b7c881fb6c70bdc01d664b6d9498f`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cw8_phase1_cx3/VALIDATION_CX3V003.json` — `541d11886c9c460ec50c59ece02487f77cff4454f4aea74915849022a7dc4774`.
