# phase1_c2v001: the A133 Phase-1 tool

**Labels.** TESTED = run here on synthetic fixtures with the result shown. FORMAL = follows from the cited code or text. UNTESTED = not run; the test that would decide it is named.

**Text of record.** `CLAUDE2/A133_TWO_PHASE_PROTOCOL_V001.md` (`cd92ef91`), sections 1, 2, 4 and 5. Ruling A133 in `ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V006_ADDENDUM.md` (`1a65ec9f` when read).

**Scope.** No production run was made. No campaign or cache on real data was read. No NGC3198 target, value or path was opened. The tests use synthetic fixtures only.

## Files

| File | Role |
|---|---|
| `phase1_c2v001.py` | The tool: `snapshot`, `handoff`, `fdplan`, `band`, `agree at0a / at0b / at1` |
| `test_phase1_c2v001.py` | 71 checks: 33 MUST_FAIL and 38 MUST_PASS |
| `test_runs/RUN_20261019T111724Z_82011/`, `test_runs/RUN_20261019T111742Z_84964/` | The two record runs: 71/71 each, with `RESULTS.json` |
| `HASHES.txt` | sha256 from bytes |

Earlier `test_runs/RUN_*` directories are development runs on superseded bytes. They are kept, never edited, and are not the record.

## Pins (sha256 from bytes; imported, never modified)

| Pin | sha256 |
|---|---|
| orchestrator `calibration_orchestrator_c2/v005/calibration_orchestrator_c2v005.py` | `c75a889ff4646a816329756124a19532cbc166d26f47ce2ea5147b71c2cf7c4d` |
| engine `calibration_engine_freeze_v003b_v003d/calibration_region_engine_c2v003b.py` | `6ec8b2d0085a9460bbf481852ea5e0f64dac09af3c8a6c6fea2bf126057c3bc3` |
| freeze `freeze_score_readiness_cx3/v003g/prediction_freeze_c2v003g_cx3v001.py` | `48a1e48a5230fff346705c338da30a8ee53a8643193dbe4616c25e61eab3d405` |
| `kmax_prereg_v005_c2/KMAX_MATRIX_PREREG_V005.json` (τ) | `dbddc02c4d793b44a12136fc4fc88b20c001865ddd4c89b1b70c57bc406bb174` |

- The tool checks each pin before and after import.
- It refuses a campaign whose coordinate spec does not pin engine c2v003b.
- It refuses unless `criterion.tau_definition` is the registered text. τ_i/σ_i = 0.25.
- Read-only inputs used by the tests: coordinate spec V002 (`89e7d33e`), addendum V005A (`ff438ed1`), taxonomy V003 (`a65ddee0`), monitor (`ba031c23`), campaign launcher c2v005 (`d35d5d4a`), the template the spec names, and the DDO154 region's `distance_summary` numbers only.

## Usage

Use the campaign interpreter, so that `check_runtime` compares like with like:

```
PY=/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
$PY -I -B phase1_c2v001.py snapshot --config C --config-sha256 H --out-dir NEW
$PY -I -B phase1_c2v001.py fdplan --s0-only --config C --config-sha256 H --out-dir NEW
$PY -I -B phase1_c2v001.py fdplan --config C --config-sha256 H --snapshot SNAPDIR --snapshot-sha256 H --interior-count K --out-dir NEW
$PY -I -B phase1_c2v001.py handoff --config C --config-sha256 H --snapshot SNAPDIR --snapshot-sha256 H --interior-count K \
     --provenance P --provenance-sha256 H --root-fields R --root-fields-sha256 H --out-dir NEW
$PY -I -B phase1_c2v001.py band --seal-path SEAL --seal-sha256 H --snapshot SNAPDIR --snapshot-sha256 H \
     --fdplan FDPLAN_C2V001.json --fdplan-sha256 H --values V --values-sha256 H --out-dir NEW
$PY -I -B phase1_c2v001.py agree at0a --config C --config-sha256 H --snapshot SNAPDIR --snapshot-sha256 H --s0 S0_C2V001.json --s0-sha256 H --out-dir NEW
$PY -I -B phase1_c2v001.py agree at0b --snapshot SNAPDIR --snapshot-sha256 H --phase2-record REC --phase2-record-sha256 H \
     --phase2-registry REG --values V --values-sha256 H --members M --members-sha256 H --out-dir NEW
$PY -I -B phase1_c2v001.py agree at1 --config C --config-sha256 H --interior-count K --snapshot SNAPDIR --snapshot-sha256 H \
     --l1 L1 --l1-sha256 H --fdplan F --fdplan-sha256 H --at0a A --at0a-sha256 H --at0b B --at0b-sha256 H \
     --phase2-record REC --phase2-record-sha256 H --phase2-registry REG --members M --members-sha256 H --out-dir NEW
```

- `K` is the RI45-14 `interior_count`. Root fixes it; the tool never chooses it.
- Every input file is passed with its sha256, which is checked from bytes. The snapshot sha is the one root logs.

**Exit codes.** 0 ok; 3 refused; 4 not ready; 10 AGREEMENT_DEFECT; 20 Phase-1 terminal (no NGC call).

**Fail-closed rules.** Every check runs before the output directory is created.
- `--out-dir` must not exist, its parent must exist, and it must not lie inside the campaign work dir.
- Files are created exclusively and never overwritten.
- Any unanticipated exception is reported as REFUSED.
- The campaign work dir is only read. The tests hash the whole tree before and after `snapshot`, `handoff` and `at0a` (T01, T06, T08).

## What each command checks

### `snapshot` (A133 1.2, 1.3)

**Setup.**
- Builds `Context(config)` and `prepare(create=False)` from the pinned orchestrator, as `plan` does. `Cache.open` re-verifies every cache entry from its bytes.
- Requires WORK_DIR.json to MATCH.

**Prefix.**
- The prefix is the committed waves below the first WAVE_PLAN whose families include `march0`.
- Each prefix wave must have WAVE_RESULT.json.
- Waves must be numbered 1..W−1.
- Every plan up to and including the march0 plan must carry this config's cache id, config sha256 and gate digest.
- The replay sees only cache entries from those waves (plus a written ANCHOR_ALIAS). Waves after march0, and any wave in flight, are invisible to it, so the snapshot is free of races.

**Pass 1.**
- Runs the unmodified engine at the registered budget. The forward classifies each call with the orchestrator's own `Probe.context`.
- B_P1 is the log index of the first `march0` call. The tool refuses if that index ever differs from the number of forward calls made.
- Only the families seed, jacobian, repair and gd_pre may come first. Any other family, or a cache miss, stops the replay (NOT_READY).
- An exploration call with m_id = 0 gives NO_IDENTIFIED_DIRECTION.
- A replay that ends without a march0 call with an engine terminal status (SEED_INVALID … NO_ADMITTED_POINT_FOUND) gives that status. Both cases write `SNAPSHOT_C2V001.json` only, with `ngc_calls: 0`, and exit 20.
- If B_P1 is reached but the march0 plan is not yet written, the result is NOT_READY.

**Pass 2.**
- Runs the replay at budget B_P1, twice. The two runs must be byte-equal in the engine's canonical bytes.
- Status must be BUDGET_EXHAUSTED, with `stage_reached == 'march'`, log length B_P1, a primary_anchor inside the prefix, and m_id > 0. These conditions are what reject B_P1 ± 1.
- The thetas must be the same as in pass 1.

**Other checks.**
- `check_runtime` must return no differences.
- v003g `select_representative_points` runs on the run. Its anchor must be u_A by log index and by bitwise u.

**Writes.**
- `PHASE1_CALIBRATION_RECORD_BUDGET_EXHAUSTED_<sha16>.json` and a new `PHASE1_CALIBRATION_REGISTRY.jsonl`, through the engine's `write_calibration_record`, then verified.
- `SNAPSHOT_C2V001.json`: B_P1; the prefix calls (keys and families); the plan and result shas; the record shas; u_A (log index, source, u with hex, θ); the v003g role of u_A.

### `fdplan` (A133 1.4)

**`--s0-only`.** Uses the config alone and is target-free.
- S0 is the seed (the trial u, or `u_seed`) and its three Jacobian first-attempt points.
- The side rule is A133's: h = min(rel_step, 1 − u_k); below min_step the minus side is used, with min(rel_step, u_k).
- θ comes from the engine's own `to_natural` on the campaign engine spec. The keys are the orchestrator's `theta_key`.

**Default.**
- F is the three FD points from u_A, by the same side rule, clipped onto the box as `_evaluate_point` does.
- If u_A is the seed, each F point must also be in the record bit for bit, and it is taken from there.
- M is the v003g members at the RI45-14 `interior_count`. Each member's θ is re-derived bit for bit.
- `distinct_calls` is M ∪ F deduplicated by exact θ. An F point equal to a member is the same call, not a skip.
- Each point carries `theta_shared` (shared coordinates only). NGC slot values never appear.

### `handoff` (RI45-01 except COMPLETE; RI45-10 output)

**Checks, in order.**
1. The native `verify_calibration_record`, and the record must equal the snapshot.
2. The double replay is re-run from the campaign cache and must reproduce the recorded run byte for byte. This catches a forged or truncated record that has been re-registered.
3. `check_runtime`.
4. v003g reclassification: `admission_reverified`, the fingerprint equals the record's, and the anchor is u_A.
5. The export must be the complete admitted roster, compared entry by entry.
6. Plan and admission provenance, per admitted point:
   - the cache entry's wave and call index lead to a WAVE_PLAN call with the same key and spec sha;
   - that plan's sha256 from bytes equals the root-published one;
   - the root-published admission record of that wave names the plan sha.
7. Post-state acceptance: a byte-pinned record with root-attested status `ACCEPTED`. It must bind this point (its theta key or spec sha256 appears in the bytes) and no other admitted point.
8. Point-scoped certificates: at least one, each byte-pinned, each binding this point and no other.

**Writes.**
- `TARGET_FREE_EXPORT_C2V001.json`: exactly schema, mode, target_free, coordinate_pin and admitted_points. Every admitted point carries exactly log_index, u and theta_natural.
- One `HANDOFF_<log_index>_C2V001.json` per v003g member, with exactly the 10 RI45-10 fields.
- `HANDOFF_RECEIPT_C2V001.json`, with `launch_authorized: false`.

**Mode fence.** A synthetic campaign hands off `SYNTHETIC_DRY_ONLY` only. A real campaign hands off `ADMITTED` only.

### `band` (A133 1.5 and the allowance of section 4; writes L1)

**Seal.** The command refuses without `--seal-path` and `--seal-sha256`, and the seal bytes must hash to that sha. It does this before reading anything else.

**Inputs from the record.**
- The rectangles are re-derived from the region bytes.
- u_A must re-classify as admitted.
- q_A = (f(u_A) − centre)/σ, S = the identifiability `scaled_jacobian`, V_I and V_N.

**Values.** The F points in the fdplan must equal u_A + Δu e_k. The values file must bind u_A and each F point by theta key, and must have 43 rows.

**Per row q:**
- K_q = (g_q(F_k) − g_q(u_A))/Δu_k, and w = V_I K_q.
- Band: two LPs of w·c over |q_A + S V_Iᵀc| ≤ halfwidth/σ, 0 ≤ u_A + V_Iᵀc ≤ 1 and |c_k| ≤ max_repair_step/√m_id, solved with the engine's `_lp_max`.
- Allowance a_q: two LPs over |S V_Iᵀc| ≤ 0.25, the box, and |c_k| ≤ hull_growth_tol.
- 172 LPs at 43 rows.
- A row INVALID at u_A or at any F point, or with a non-OPTIMAL band LP, reads NOT_AVAILABLE, never a zero-width band.
- Also reported: FD noise 2ε|Δu|/h at each optimum (or `FD_NOISE_NOT_BOUNDED`), K_q·v_j for each near-null v_j, and NON_DISCRIMINATING.

**Label.** `PHASE1_LINEARISED_ADMITTED_SET_PROJECTION_TRUNCATED_LOWER_BOUND_ON_SPREAD_NOT_A_TIER`, conditional on A13. It is never a tier.

### `agree` (A133 section 4)

**`at0a`, at the Phase-1 freeze.**
- Recomputes B_P1 and the B_P1 replay; both must equal the snapshot.
- Every log θ below B_P1 must be a prefix cache entry, bit for bit.
- The march0 plan must be unchanged.
- The orchestrator's own `Probe.run(..., 'probe')` on the prefix cache must request exactly the committed march0 plan's (key, θ) list, in order.
- The S0 θ bits must equal the record's.
- `check_runtime`.
- Any failure gives AGREEMENT_DEFECT (scope prefix), exit 10.

**`at0b`, at the Phase-2 freeze.**
- The Phase-2 record verifies, with the same region and the same engine parameters apart from the budget.
- Its primary anchor equals u_A (log index and u, bitwise).
- Its first B_P1 log entries are byte-equal to Phase 1's.
- The u_A member's result pin sha equals Phase 1's.

**`at1`.**
- The members must be exactly the Phase-2 v003g members at K.
- For each valid PRIMARY member and each row available in both phases, the test is: lo − a − e + K V_Nᵀn ≤ g(u_m) ≤ hi + a + e + K V_Nᵀn.
- Outcome: COVERED, or SUPERSEDED with each failing (member, row), its excess, |n_m| and category (OUTSIDE_TRUST_RADIUS, then OUTSIDE_LINEAR_DDO_REGION, then NGC_NONLINEAR). If AT-0a or AT-0b is not PASS (or not for this snapshot and record), the outcome is AGREEMENT_DEFECT.
- Also reported:
  - per row, the Phase-2 envelope width against the band width;
  - the NGC linearity residuals;
  - max |f − f_lin|/τ over the Phase-2 admitted points;
  - each identified projection range against the linear region, at 0.00625 u.

## Input formats defined by this tool

None of these existed before this build. Each is pinned by sha on the command line.

| Schema | Content |
|---|---|
| `PHASE1_PUBLISHED_PROVENANCE_C2V001` | `cache_id`; `wave_plans {wave: sha256}`; `admissions {wave: {path, sha256}}`; `points {theta_key: {post_state_acceptance: {path, sha256, status}, certificates: [{path, sha256}]}}` |
| `PHASE1_HANDOFF_ROOT_FIELDS_C2V001` | `mode`, `root_admission`, `policy_pin`, `v007_adoption_pin`, `certificate_pins`, `driver_branch`, `driver_acceptance_pin`, `coordinate_pin` |
| `PHASE1_NGC_VALUES_C2V001` | `query_ids` (43); `points`: Phase 1 `{role u_A or F_k, theta_key, result_pin, valid[43], speeds_km_s[43], eps_km_s[43]}`; Phase 2 `{role member, log_index, theta_key, member_valid, result_pin, valid, speeds_km_s}` |

The values files are assembled by root from NGC result files. The tool never opens an NGC result file.

## Tests (TESTED, synthetic, 2 identical record runs: 71/71, MUST_FAIL 33/33, audit denials 0)

**How the fixtures are built.**
- The real orchestrator builds each campaign: Context, Probe, make_plan, _commit_plan, run_wave, ingest, finalise, with its in-process test executor.
- Inputs: the real V002 spec and engine, the real V005A addendum (3 free coordinates), the real taxonomy, a toy forward and a synthetic 12-row region.
- Oracle: a direct engine run with the same forward.
- An audit hook refuses any write outside the run dir, and any open of a path with an `ngc3198` or `uvt_` component.

**A133 section 5 MUST_FAIL list → tests:**

| A133 MUST_FAIL | Tests |
|---|---|
| B_P1 off by one | T12: budget B_P1 − 1 and + 1 refused; a snapshot file claiming B_P1 + 1 refused; at0a on it refused |
| replay or prefix mismatch | T13: altered prefix forward; non-byte-equal replay; prefix miss. T11: prefix not committed; B_P1 reached before the march0 plan; a prefix wave without WAVE_RESULT. T24: tampered march0 plan; altered S0 bits. T14: a self-consistent forged record and a truncated roster, both caught by the double replay |
| anchor different from v003g's | T14: v003g anchor ≠ u_A; record anchor ≠ snapshot u_A |
| a non-OPTIMAL program or an INVALID FD row filled in | T18: simplex fault injected → NOT_AVAILABLE. T17: INVALID at F1 → NOT_AVAILABLE, no lo/hi/width |
| `band` without the seal sha | T16: no seal → refused, nothing written; wrong seal sha → refused |
| v003g on a synthetic BUDGET_EXHAUSTED record | T15: MUST_PASS on the B_P1 record; MUST_FAIL on one with no admitted point and on one with m_id = 0 (L1326) |
| also: RI45-01 controls | T07: published-plan hash mismatch; acceptance missing; acceptance refused; certificate bound to another point; admission not naming its plan; ADMITTED mode on a synthetic campaign. T02 and T08: out dir exists, out dir inside the work dir, config pin mismatch. T19 and T23: at0b re-binding defect; at1 under an AT-0 defect |

**MUST_PASS.**
- B_P1 and u_A equal the oracle in five scenarios:

| Scenario | B_P1 | u_A source |
|---|---|---|
| seed admitted | 7 | seed |
| Jacobian point admitted | 7 | log_scan |
| repair | 8 | repair |
| repairs failing, then pre-march global design | 22 | global_design |
| halving | 8 | seed |

  Of these, the halving case's F0 is the DDO-invalid first-attempt point, taken from the record.
- Terminal statuses are reported with no record: NO_ADMITTED_POINT_FOUND, SEED_INVALID and NO_IDENTIFIED_DIRECTION.
- The single admitted point has role `hull_vertex`, with 4 distinct calls.
- S0 from the config equals the record bit for bit.
- The handoff export and handoffs are correct.
- at0a passes, and still passes after the whole campaign has run.
- A snapshot taken after completion equals the early one.
- Band LP bounds are verified independently. Both optima are feasible, and every one of 20,000 and 4,702 sampled feasible points lies inside, including a case where the DDO rows bind.
- at0b passes. at1 gives COVERED for a constant toy and SUPERSEDED for a nonlinear toy, with the categories recomputed independently.
- The three categories come out right on hand-placed points.

## FORMAL and [D] readings for the reviewer (Claude3)

1. B_P1 counts engine evaluations (log entries). The tool refuses if this ever differs from forward calls; it differs only if `to_natural` fails.
2. The m_id = 0 rule fires at the first exploration call, or on a COMPLETE replay with no identified direction. With the V002 parameters the second case cannot happen (global_design_count 12).
3. AT-1 noise term [D]: e_q = max(noise at the band's lo and hi optima) + Σ_k 2ε_q|(V_Nᵀn_m)_k|/h_k, with ε_q = the largest per-row ε over u_A and the F points. A row whose a_q is NOT_AVAILABLE is not tested and is listed.
4. The v003g freeze spec uses the coordinate spec's NGC placeholder slots. The selection reads only engine coordinates; the tool checks that they reproduce the campaign's own. NGC slot values never enter an output.
5. The provenance binding is by exact token (theta key or spec sha256 in the record bytes). The acceptance status is root's attestation in the provenance file. The tool does not interpret the content of real R-B5 or R-C1/C8 records.
6. The gate digest must be equal across processes (each WAVE_PLAN's against the snapshot's Context). This holds in the synthetic runs. With the real deciding and adoption gates it is FORMAL: the gate dicts hold no timestamps.

## UNTESTED (and the test that decides each)

- **The real campaign.** Run `snapshot` on DDO154_CALIBRATION_ORCH_V005 once the march0 plan exists, check against `plan`'s probe and the FINAL record (AT-0b).
- **An anchor-alias seed.** The handoff refuses it (no wave provenance). The V005A numerics disable the alias (FORMAL); a successor is needed if it is used.
- **Real provenance records.** R-B5 acceptance and R-C1/C8 certificates. Run `handoff` on the first real ones; if their bytes bind the point by another identity, the handoff refuses and a successor is needed.
- **F points through step 5.** F points are not admitted points, so the RI45-10 handoff carries members only. The selected filler (`fill_step5_cx3v003`) refuses 3-u points (RI45-02). F needs the RI45-02/RI45-08 consumer successor. Decided by a dry fill of the fdplan output.
- **Real NGC values, ε_q from point certificates, and the timing of each command at scale.** Run `band` on the Phase-1 values after the seal.
- **Headlines, E3 lines, patterns and tier changes.** These are r3a scoring outputs on target data, not computed here.

**Size.** The tool is about 1,000 lines against A133's "about 300". The extra lines are the RI45-01 provenance checks and the section-4 reported lines.
