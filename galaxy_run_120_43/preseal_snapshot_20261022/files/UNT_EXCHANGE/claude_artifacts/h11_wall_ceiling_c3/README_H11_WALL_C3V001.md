# HEADLINE11 first-attempt wall to the Phase-2 ceiling — C3V001 (root 0836, V006 A271)

Claude3 build, review candidate. Not adoption, and not a launch.

## Trace (TESTED from bytes)
- **Where the wall lives.** HEADLINE11's `wall_cap_s` comes only from the step-4 packet parameters: `sched_s45_c2/v004b/DIRECT_BATCH_PARAMS_S45_C2V004B.json` (`e239d21e`), at `batches.HEADLINE.caps_per_case.<case>.wall_cap_s` = 100800 for all 11 cases.
- **How it reaches the plan.** Its scope text says root copies `caps_per_case` into the plan calls and into the admission's `cfg.caps` (ROOT_CAPS_BINDING).
- **guard014** `6efdca01` (L388-392) only requires each call's caps to be positive integers and equal to `cfg.caps[case]`. It neither pins the DBP nor bounds the wall.
- **binder c2v011** `d3d9702e` copies the plan bytes and the admission unchanged, and runs guard014's validate at bind (L31-54).
- **launcher015** `cd987edd` passes the call's wall to the monitor (L19).
- **The monitor** `root_monitor_c2v001` `ba031c23` takes any wall > 0 as a float (L116, L163, L232).
- **No wall anywhere else.** produce_final_step4_specs_c4v004, apply_h3_fields_c2v006, step4_prelaunch_c2v005 and step4_bind_c2v011 contain no wall field. So no FINAL spec byte, no 0778 table-D pin, no H1 config and no sealed or numerics byte changes.

## The change (data only)
- **DBP C2V004C** is C2V004B with the 11 HEADLINE `wall_cap_s` leaves set to W. W is the whole seconds from the fill time to the Phase-2 ceiling 2026-12-01T05:59:00Z (Mon Nov 30 23:59 CST; A246, A249).
- **Provenance leaves** also change: `schema`, `supersedes.{path,sha256,what_changes}` and a new `note_a271`.
- **Nothing else changes:** every RSS cap stays RAM, every output cap stays, and SENS_LO, SENS_HI, POST_S1 and DIII stay unchanged.
- **Builder:** `build_params_s45_c2v004c_c3v001.py` `ab9a054e`. It reads only the pinned C2V004B bytes, asserts the leaf-diff scope, and writes by exclusive create into a new folder.
- **Pre-built instance** (fill 2026-10-22T09:30:00Z, the earliest S4T R3 receipt time, A260):
  - `C2V004C_FILL_20261022T093000Z/DIRECT_BATCH_PARAMS_S45_C2V004C.json` `ce9cbef8caaef8120377f302647c71d80387353d192d25d7d0b7e13e5872e809`;
  - `LEAF_DIFF_S45_C2V004C.json` `a904dcae1b950cc3fa07737aeed34ce9795383e864eb5e459289183517161738`;
  - W = 3,443,340 s (39 d 20 h 29 m).
- **Why the earliest fill time.** Because W is counted from the earliest plausible fill, W is never less than the exact time remaining at any later fill. No wall cap therefore ends a run before the ceiling.
- **The overrun is bounded.** A call can run past the ceiling by at most (fill delay + its own start delay, a few hours). That matters only for a run of about 40 days, and the ceiling freezes the score either way.
- **Exact alternative (optional).** At fill time, root runs the builder with `--fill-utc "$(date -u +%Y-%m-%dT%H:%M:%SZ)"` into a new folder and uses those pins.

## Tests (synthetic; the real C2V004B is read only)
- `test_build_c2v004c_c3v001.py` `820349f4`; record `TEST_RECORD_C3V001.json` `a38a5a12`.
- 18/18 checks pass, including:
  - the exact 16-leaf scope (11 walls plus provenance);
  - RSS, output and other walls unchanged;
  - determinism;
  - refusals for a fill too late, a fill after the ceiling, non-canonical UTC, a tampered base, an existing out dir and a relative out dir;
  - the CLI's exclusive outputs.
- 4/4 restoring mutants are killed: scope check removed with a SENS wall changed; a shorter wall allowed; the base pin skipped; the wall rounded up.

## UNTESTED
- Root's fill of the real GUARD014_FINAL_PLAN and FINAL_ADMISSION_CANDIDATE. The deciding check is the sheet amendment's check command after bind.
- Monitor behavior at multi-week walls, which is code-read only (a float compare, L163).
