date -u: Mon Oct 19 19:40:00 UTC 2026

# SLOT_GEOMETRY_FINDING_C2V004: where the CX2V006 placeholder NGC3198 slots are used, and the successor this needs

**From** the Claude2 root workflow `ri45-14-c2v004-and-slot-geometry` (A163). **Status:** a finding for root. It builds no tool successor and authorizes nothing.

**Verdicts of the A163 CHECK** (`NGC3198_GEOMETRY_TRACE_C2V004.json` `c1ac10f8`, all tested dry):
- **S0_SPECS_OK.** The S0 point handoffs and filled S0 NGC call specs carry 13.8 Mpc / 72 deg.
- **FDPLAN_OK.** The F points carry no NGC geometry. The filled F specs carry 13.8 / 72.
- **FREEZE_SPEC_PLACEHOLDER.** phase1 `freeze_spec` builds its v003g spec from the placeholder slots.

S0 may launch (A163 L1406). The placeholder use is real, but it is confined to member selection.

## 1. Every code site that touches the NGC3198 slots

FORMAL: lines read from the bytes at the shas given. TESTED: run dry in `DRYRUN_FREEZE_C2V004.json`.

| Site | File (sha) | Lines | What it does with the slots |
|---|---|---|---|
| `freeze_spec(ctx)` | phase1_c2v003b (`7d891ff7`) | L432-440 (placeholder at L435) | It appends `ctx.spec.ngc3198_nuisance_slots.placeholder_for_engine_coordinate_derivation`, applies the addendum mode, and checks that the engine coordinates equal the campaign's. |
| the same | phase1_c2v002 (`d64351ec`) / v003a (`385b287c`) | L372-380 (L375) / L420-428 (L423) | Identical. |
| `v003g_members` | v003b | L443-447 | Its only caller of `freeze_spec`. It passes the spec only to `select_representative_points`. |
| callers of `v003g_members` | v003b | snapshot L500 (literal 0, anchor check), handoff L643, fdplan L801, agree at1 L1276 | Selection only. The tool never calls `evaluate_envelopes`, `evaluate_sensitivity` or `write_freeze_manifest` (grep: 0). |
| `Context.__init__` | orchestrator c2v005 (`c75a889f`) | L1656-1665 | It uses `cfg.ngc3198_slots`, or else the placeholder, only to derive and check `engine_coordinates`. `ctx.freeze_spec` is set at L1661 and never read again. |
| `prepare` geometry | filler `fill_step5_c2v001` (`ec417e76`) | L292, L297-298 | It takes the NGC geometry from POLICY_C2V001 `slots` = slots V003 (`d3859b42`): 13.8 / 72. This is the only geometry source for S0, F and member call specs. It is correct. |
| `_theta_ngc_from_engine` | v003g (`48a1e48a`) | L1019-1026; used at L2163 (members), L2313 and L2331 (sensitivity), L2625 (validation) | It puts every member's NGC3198 slots at the spec's trial values. **This is where a placeholder spec would act:** the inclination would be 70.0 deg. |
| `_check_slot_geometry` | v003g | L2941-3037 | It compares the spec's NGC slots with `notes.ngc3198_slot_sensitivity`. |

## 2. What the placeholder use does and does not do (TESTED)

**What it does not do:**
- **D-09.** On one synthetic run over the real CX2V006 engine coordinates, `select_representative_points` with the placeholder spec and with the spec of record gives canonically equal `admitted_region` and `points` (12 members). The engine coordinates of the two specs are equal: canonical sha256 `54120a12…2e27`.
- **No phase1 output is affected.** Handoff, fdplan and at1 member sets, and the snapshot's anchor check, carry no NGC3198 slot value.

**What it would do if the placeholder spec reached an NGC call:**
- **D-10.** The PLAN outputs (`evaluate_envelopes` at budget 0) carry `theta_ngc` 13.8 / 70.0 under the placeholder spec, against 13.8 / 72.0 under the spec of record. Under the placeholder, the launch-registry theta keys (RUNBOOK_V002_C2V005, G27) and the replay adapter's exact-theta lookup would miss every launched call.
- **D-07.** With an A16.4 wrapper, every member is refused (GEOMETRY_NOT_EXPOSED), `select_reference_member` returns NO_VALID_MEMBER, and the writer refuses.
- **D-08.** With a forward that ignores geometry, the writer refuses at A16.1 (declared_range twice, headline_geometry).

**The residual hazard.** CX2V006's placeholder inclination has `reference_value` null. Notes built from the placeholder spec itself would pass the A16.1 check at 70 deg. C2V004 closes this: its notes are slots V003's block, checked byte for byte (contract row K3).

## 3. The remedy now in force in C2V004 (no tool change)

- **The spec of record.** `write_freeze_manifest_inputs[spec].value.spec_of_record` (`e2a7650e…94ec`) is also written as `FREEZE_SPEC_OF_RECORD_C2V004.json`, whose file sha256 is the same. It is passed to every v003g call that takes `spec`:
  - selection at step 1a;
  - the PLAN `evaluate_envelopes` at step 1b;
  - the pass driver's `spec` input (roster_builder_c2v005 L1710);
  - `evaluate_sensitivity`;
  - `write_freeze_manifest`.
- **"Same spec" is engine-only.** Check IC-P1-MEMBERS requires the handoff and fdplan members to equal the freeze selection's (log_index, role, order). A difference is a defect for root, not a choice.
- **The launch registry producer** (G27, not yet confirmed) must key each call on its `theta_ngc` under the spec of record. Builder check R2e refuses a mismatch, so a placeholder key fails closed.

## 4. The minimal successor needed

**For correctness: none.**
- The placeholder spec reaches only `select_representative_points`.
- Selection reads engine fields only (D-09).
- C2V004 routes the spec of record to every call that reads the NGC3198 slots.
- No S0, F or member call spec is affected (S0_SPECS_OK, FDPLAN_OK).

**Optional hardening (not built here).** It would remove placeholder geometry from the phase1 tool altogether. If root wants it, the minimal successor is `phase1_c2v003c`, with exactly one change, in `freeze_spec` (v003b L432-440):
- Replace the placeholder list with slots V003 `ngc3198_slots`, read from the pinned path at sha256 `d3859b42…0969`, key `ngc3198_slots` only.
- Keep the engine-coordinate equality refusal (L438-439) unchanged.
- Optionally, record the spec's canonical sha256 (it must equal `e2a7650e…94ec`) in the snapshot, handoff and fdplan outputs.

**What the hardening would change:**
- Members stay byte-identical (D-09). Only the module name and tool sha change.
- Under V006 A168 (L1519), both classifiers would then bind the successor's sha as a pin delta.
- Because no correctness gap exists, the expected cost is that pin delta plus one lean review. The benefit is defence in depth only.
