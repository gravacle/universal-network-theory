# FREEZE_DELTA_NOTES — prediction_freeze_c2v002.py (Claude2 lane)

Date (UTC): 2026-10-17.

**Supersedes** `calibration_freeze_0462/prediction_freeze_c3v001.py` (`ed6b5a3e…09200`). That file is read-only and unchanged.

**Scope**
- Claude4 0023 defects **A3** and **A4**.
- The freeze/scorer parts of contract decisions **D5, D6, D8, D9 and D10**.
- The freeze side of **D7**: the INNER_SAMPLE label and the truncation flag.

**Not in this file (engine lane):**
- A1 (false empty region);
- A2 (`_edge_t` tolerance), whose lesson is applied only in the freeze's own `_edge_t`;
- D7 march iteration and the global design;
- D10's `distance_summary` box for DDO154;
- the engine-side null-space completion. The freeze *requires* the completed basis but does not compute it.

**Safety.** No NGC3198 velocity was read. The only NGC3198 file opened is the target-free query manifest. No forward model, no project run, no network, no scipy, single thread.

## Hashes (computed from bytes)

| File | SHA256 |
|---|---|
| `prediction_freeze_c2v002.py` (2433 lines) | `613f34387507a0eb590b95b3d9ad73515a8459255c56a18c22db3469ec85314b` |
| `freeze_selftest_c2v002/selftest_freeze_c2v002.py` | `197d089c2369be3dd01ca79fdedb9476d936fe7f288245c6ce7376cd6492adc0` |
| `freeze_selftest_c2v002/mutants_c2v002.py` | `ea64f74a28075e3cc0dff356233f5ea0d33e12f3ea35a33bd67ff380424481f7` |
| `freeze_selftest_c2v002/runs/run_20261017T133922Z_93587/SELFTEST_RESULTS_C2V002.json` | `2171437d38248b4477c67a8924f04cafed6dff8b32c0ee4559e4e661751b97b0` |
| `freeze_selftest_c2v002/mutants/20261017T133906Z/MUTANT_RESULTS_C2V002.json` | `4bbde01c8920339d2ed6aa2733c0fb40b9f3e41ac4efee80686aad78b3103414` |

**Results.**
- **Self-test:** 99 checks, 0 failed, on the module at `613f3438…`.
- **Mutants:** 12 targeted single-point mutants, all 12 killed. M08 survived the first pass; check SC.11 was then added and kills it.
- Earlier `runs/` and `mutants/` subfolders are intermediate runs and are kept (nothing deleted). Some were made while the self-test was still changing; only the two results files above are the evidence of record.

## API delta (keyword-only, no defaults; every function returns a dict with `ok` and `reasons`)

| v001 | v002 |
|---|---|
| `load_query_manifest(path, expected_sha256)` | Unchanged. It now reads through the regular-file reader. |
| — | **new** `make_freeze_coordinate_spec(coordinates)` (D10) |
| `select_representative_points(exploration, interior_count)` | Adds a `spec` argument. |
| `evaluate_envelopes(forward_ngc, points, query_ids, budget)` | Adds a `spec` argument and returns per-member arrays. |
| — | **new** `select_reference_member(selection, evaluation)` (D5) |
| — | **new** `evaluate_sensitivity(forward_ngc, reference, selection, spec, query_ids, null_direction_rule, budget)` (D6) |
| `write_freeze_manifest(out_path, parameter_region, alternatives, observation_rule, envelopes, query_ids, code_files, input_files, notes)` | Takes `out_path, registration_path, parameter_region, observation_rule, spec, selection, alternatives, alternative_evaluations, reference, sensitivity, query_ids, code_files, input_files, notes, allow_incomplete`. |
| `verify_freeze_manifest(freeze_manifest_path)` | Same signature. Checks the v002 structure and internal consistency. |
| — | **new** `verify_registration(registration_path)` (D8) |
| `score_after_freeze(freeze_manifest_path, target_rows)` | Takes `freeze_manifest_path, registration_path, expected_manifest_file_sha256, target_rows`. |

**Root call order:**
1. `make_freeze_coordinate_spec`
2. Engine on `engine_coordinates`
3. `select_representative_points`
4. `evaluate_envelopes`, once per EVALUATED alternative
5. `select_reference_member`
6. `evaluate_sensitivity`
7. `write_freeze_manifest`
8. Log `manifest_file_sha256` and `registration_file_sha256` in a FROM_ message before opening targets.
9. `score_after_freeze`

**Manifest schema.** `FREEZE_MANIFEST_C2V002` has 26 top-level keys; see `MANIFEST_KEYS` at the top of the module.
- Removed: `predictions` (`velocity` was the per-query median).
- Added: `freeze_status`, `incomplete_reasons`, `admitted_region`, `coordinates`, `members`, `member_evaluation`, `reference_member`, `pointwise_envelope`, `sensitivity`, `band_scope`, `conditional_on_trial_values`, `alternative_results` and `headline_rule`.

## Line-level delta (v001 line → v002 line)

### A3 — partial envelopes frozen as valid

| v001 | v002 | Change |
|---|---|---|
| L713 `valid = used >= 1 and n_valid == used` (over **evaluated** points) | L1088–1098 `_pointwise_envelope` | A query is valid iff `n_valid == n_members` over **every selected** member. An unevaluated member has `row_valid` all False, so it invalidates every query. |
| L718 `'n_points': used` | L1096 `'n_members': n` (selected) | Partiality is visible in the bytes. |
| L678–686 (break on budget; unevaluated points vanish) | L1174–1192 | Unevaluated members stay in the record with `evaluated=False` and `reasons=['NOT_EVALUATED…']`. `status` is `COMPLETE` iff every selected member was evaluated. |
| L722 (`status` returned but never frozen) | L1488–1500 `_incomplete_reasons`; L2004 writer gate | The writer refuses when the exploration status is not `COMPLETE`, the primary or any evaluated alternative's member evaluation is not `COMPLETE`, or the sensitivity run is not `COMPLETE`. `allow_incomplete=True` instead stamps `freeze_status: FREEZE_INCOMPLETE` with `incomplete_reasons`. The verifier recomputes both (L1856–1861), so relabelling as complete fails (CX4.10). |
| "one failed point voids all 43" | `members[*].member_valid` and `row_valid[43]` frozen | The strict envelope still voids the query, as D5 requires. Every valid member remains scored, and the failed member is visible and scores 0. |

### A4 — unpinned or vacuous manifest

| v001 | v002 | Change |
|---|---|---|
| L730–744 `_pin_files` accepts `[]`, `/dev/null` and FIFOs | L1896–1911 | A non-empty list is required. Each pin goes through `_read_regular` (L206–241): `os.open(O_NONBLOCK)`, then `fstat`, then `S_ISREG`, and a size of at least 1. The **realpath** is recorded (fixes F2-N05) along with the byte count. |
| L852–855 | L2015–2021 | `code_files` must include this module's realpath. Duplicate pin paths are refused. |
| L1050–1068 `_verify_impl` reads pins even after the hash fails, with a blocking read | L2103–2147 `_verify_bytes` | Pins are read only after the self-hash, canonical-bytes and structure checks pass (fixes F2-N01). Each pin is read regular-file-only and must match sha, bytes and realpath. |
| (none) | L1866–1886 | The structure check refuses empty pin lists and pins with `bytes < 1`, so a re-hashed manifest with emptied pins fails (A4.9). |

### D5 — headline is per member

| v001 | v002 | Change |
|---|---|---|
| L717 `central = median` → manifest `velocity` (L788) | removed | No median or central curve exists anywhere in the bytes (CX2.4). |
| L1135–1156 one within-count from `velocity` | L2252–2263 `_score_members`; L2379–2400 headline | Every member gets a 43-row LADDER table (observed, predicted, quoted sigma, signed residual, sigma ratio, fractional error, valid, within_error). The headline reports the min/median/max of the **primary** members' counts (unevaluated or invalid rows count 0), the frozen reference member's count, `freeze_status`, `admitted_set_label` and `region_possibly_truncated`. |
| — | L1204–1252 | `REFERENCE_RULE`: among evaluated members with all 43 rows valid, take the one whose identified-subspace projection is nearest the centroid of **all** admitted points; ties go to the lowest `log_index`. It is frozen in `reference_member` together with the ranking. |
| — | L758–761, L970–971 | The selection adds a `centroid_nearest` admitted point so that the rule can choose it. `admitted_projections_identified` freezes every admitted point's projection; the verifier recomputes the centroid, the ranking and each member's membership (CX4.8, CX4.11). |
| — | L2401–2403 | The pointwise envelope is still reported, labelled `POINTWISE_ENVELOPE_NOT_A_REALIZABLE_CURVE` with `headline: False`. |

### D6 — null and fixed directions

| v001 | v002 | Change |
|---|---|---|
| L491–579: near-null directions and fixed coordinates sit at their trial values; DDO-only sensitivity | L1254–1443 `evaluate_sensitivity` | Starts from the reference member. Each near-null direction (both signs) is moved to the computational-box edge (`box_ends`, using `_edge_t` with \|v_i\|≤1e-12 treated as inert) or by `step_u`. Each sensitivity-declared fixed shared coordinate and NGC3198 nuisance is moved to its lower/upper bound or to trial±step (clipped). |
| — | (same function) | Records `limited_by` (`COMPUTATIONAL_BOX` / `DECLARED_STEP`), per-entry speeds and deltas, and `linearised_ddo_shift_sigma` (DDO sensitivity × \|t\|). It reports a per-query **box-limited band**, labelled separately with `headline: False`, and a per-target max\|Δ\|. |
| — | manifest `band_scope` (fixed text) and `conditional_on_trial_values` (L1503–1525) | Every fixed shared coordinate, NGC3198 nuisance and near-null direction is listed with its trial value, its units and whether its sensitivity was declared and evaluated. The verifier recomputes the whole plan from the reference member (L1720–1776). |

### D8 — integrity

| v001 | v002 | Change |
|---|---|---|
| The self-hash is the only identity | L2079–2095 | A registration file (`FREEZE_REGISTRATION_C2V002`, exclusive create) records `expected_manifest_file_sha256` = sha256 of the manifest **file bytes**, the self-hash, the byte count and its own canonical self-hash. |
| L1088–1105 scorer | L2286–2347 | The scorer refuses in these cases: the registration fails to verify; the `expected_manifest_file_sha256` argument differs from the registered value (L2317); the file bytes hash differently (L2330, checked before any parse); or the manifest fails full verification or its self-hash differs from the registered one. |
| — | (scorer output) | It echoes the expected and actual file sha, the self-hash, the registration file sha and `target_rows_sha256` (canonical JSON of the supplied rows, L2348). |

### D9 — alternatives

| v001 | v002 | Change |
|---|---|---|
| L816 `alternatives` is free metadata | L1446–1485 | Structure: `{'primary', 'declared': [{name, kind ∈ state/source/approximation, description, status ∈ EVALUATED_BEFORE_FREEZE / NOT_EVALUATED_BEFORE_FREEZE}]}`. The primary must be EVALUATED. `alternative_evaluations` keys must equal exactly the EVALUATED set (L1971). |
| — | (manifest and scorer) | Non-primary evaluated alternatives freeze their own member arrays in `alternative_results` and are scored `NON_PRIMARY` with `headline: False`. NOT_EVALUATED alternatives are listed with `scored: False` ("sensitivity only, never scored as the headline"). |

### D10 — nuisances, units, null space

| v001 | v002 | Change |
|---|---|---|
| L340–370: DDO nuisances end up in `theta_natural` passed to `forward_ngc` | L671–680 `_theta_ngc_from_engine` | `forward_ngc` receives the **shared coordinates plus NGC3198 nuisance slots** only, never a DDO154 nuisance. The verifier checks that `theta_ngc` keys are exactly these (L1574–1582; CX4.9, D10.6). |
| (no units, no scopes) | L455–597 `_build_spec` | Every coordinate needs non-empty `units` and a `scope` (`shared`, `ddo154_nuisance` or `ngc3198_nuisance`). |
| | | **Distance:** units Mpc, with reference 4.04 (DDO154) or **13.8** (NGC3198). |
| | | **Inclination:** units deg. |
| | | **NGC3198 slots:** exactly one distance slot and one inclination slot. Each must declare a sensitivity. The slots are excluded from `engine_coordinates`. |
| L432–443: right vectors taken as given | L794–827 | The basis must be complete and orthonormal: exactly n vectors of length n, with `identified ∪ near_null` partitioning 0..n−1, and `varying_names` matching the spec. Otherwise `NULL_SPACE_NOT_COMPLETE`. If fewer singular values are supplied, they are zero-padded with a NOTE. |
| — | L873–888 | Each admitted point's θ is checked against its u under the spec transforms (rel tol 1e-9). |

### D7 (freeze side)

L979–992 builds `truncation_evidence`. Each of the following sets `region_possibly_truncated`:
- `EXPLORATION_STATUS_<s>` when the status is not `COMPLETE`;
- `ENGINE_FLAG_REGION_POSSIBLY_TRUNCATED`, from `region_possibly_truncated: True` or a `flags` entry;
- `ENGINE_COVERAGE_NOT_REPORTED`, which the v001 engine always triggers;
- `ADMITTED_POINT_ON_COMPUTATIONAL_BOX_FACE`.

Also:
- `admitted_set_label` is always `INNER_SAMPLE`.
- The engine's `coverage` dict is copied as given.
- **For the engine lane:** emit `region_possibly_truncated` (bool) and/or a `flags` list, an optional `coverage` dict, a full `identifiability` (`right_vectors` n×n, `identified`, `near_null`, `varying_names`, `singular_values`) and `unidentified_directions[].sensitivity`.

### Kept from v001

- Canonical JSON and exclusive create.
- The FORBIDDEN screen (any depth, lowercase). Recursion is now caught, which fixes F2-05.
- Target-row binding: 43 rows, exact keys, manifest order, finite values, sigma > 0.
- The within rule `|residual/sigma| <= 1` on valid rows only.
- Inert import and standard library only (`stat` added).
- Hull vertex, anchor and interior selection with v001 tie-breaks.
- Small changes:
  - an inconsistent engine `hull_box` is a WARNING only, as before;
  - a malformed `hull_box` entry is now skipped instead of refused;
  - a non-finite sigma ratio or fractional error from a subnormal sigma becomes `None` with a row note and never passes (F2-06).

## Claude4 counterexamples, v001 against v002 (synthetic, same inputs)

| Case | v001 (frozen, read-only) | v002 |
|---|---|---|
| **CX1, 3 of 21 evaluated** | `BUDGET_EXHAUSTED`, yet all 43 queries valid. This toy's band is at a 0.897 median width fraction; Claude4's toy gave 0.74. | 0/43 envelope queries valid and 18 members `evaluated=False`. The writer **refuses**. With `allow_incomplete` it stamps `FREEZE_INCOMPLETE`; the scorer then shows it, and unevaluated members score 0/43. |
| **CX1b, one failure of 21** | 43/43 invalid, with no member record | Envelope 0/43 (strict), but 20 valid members are scored. The failing member is frozen invalid and scores 0, and the reference is a valid member. |
| **CX2, median curve** | median curve 43/43 | Members 28/29/29; headline min 28 / median 29 / max 29. The reference member (centroid-nearest, p=0.5) scores 28. No central curve appears in the bytes. |
| **CX3, near-null direction** | Q43 band 3.1 km/s | The pointwise envelope stays 3.1 (labelled). The box-limited sensitivity band is **43.6 km/s**: direction 2 has max\|Δ\| 21.8, `limited_by COMPUTATIONAL_BOX` and a linearised DDO shift of 0.00135σ. A declared `step_u` of 0.1 gives 8.72. |
| **CX4, edited and re-hashed** | +7 km/s forgery scored 43/43 | The forgery, with derived fields recomputed, still passes `verify_freeze_manifest`, because a self-hash is public. `score_after_freeze` **refuses** it: the file sha differs from the registered value, and both hashes are echoed. Passing the forged file's own hash is also refused, as is a registration edited to that hash. |
| **D02 (via the v001 engine), q trial 0.5 vs 0.9** | Disjoint bands | Both box-limited Q01 bands span 30.0 km/s and overlap. |

## Open limitations (stated, not hidden)

1. **One-at-a-time displacements.** The box-limited band moves one direction at a time from the reference member. It is neither a joint corner search nor DDO154-rechecked: the linearised DDO shift is recorded, not evaluated. The cost is 2 × (near-null directions + declared coordinates) forward_ngc calls.
2. **Registration timing.** D8 identity holds only if the registered file hash is logged externally, in a FROM_ message, before target access. The module cannot enforce that time ordering.
3. **Alternative member sets.** A non-primary alternative's members are not tied to the primary admitted projections, because an alternative may carry its own calibration. An alternative that changes the DDO154 calibration should be its own freeze.
4. **Centroid convention.** The centroid is taken in the unit-box projection onto the identified right vectors, so it depends on the computational box like every u-space quantity.
