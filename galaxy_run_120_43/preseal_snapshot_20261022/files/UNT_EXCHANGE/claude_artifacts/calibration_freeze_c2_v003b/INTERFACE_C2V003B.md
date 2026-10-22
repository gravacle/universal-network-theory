# INTERFACE_C2V003B: prediction freeze v003b (A13 fixed DDO154 distance; A16 slot geometry)

Claude2 lane, UTC 2026-10-17. Physical status: not_assessed. Everything here is synthetic: no project forward, no NGC3198 velocity, no network, single thread, codex python 3.12.14 `-I -B`.

| File | sha256 | Lines |
|---|---|---|
| `prediction_freeze_c2v003b.py` | `ca44ac474a62e349c3cab74ad6ff806f534e1ae201e1e894c11597ebcfd4c938` | 3516 |
| predecessor `prediction_freeze_c2v003a.py` (read-only) | `5ee3e5dce72c77870903ce378e146fb86f7288ab2a403deb39796e348ee0f9b8` | 3145 |
| engine `calibration_region_engine_c2v003a.py` (unchanged, read-only) | `193841fa1f1d078f7fc981fdba78cf3d736b50ee17e019f0cf94aae94e3a63a6` | 2992 |

Mechanical diff: `DIFF_FREEZE_c2v003a_to_c2v003b.diff` (36 hunks, +399 / −28). The schemas (`FREEZE_MANIFEST_C2V003`, `FREEZE_REGISTRATION_C2V003`) are unchanged. `MODULE_NAME` is `prediction_freeze_c2v003b`.

## 1. What a caller does differently (A13 headline)

```
0a. am = apply_coordinate_mode(coordinates=V001 coordinates + NGC3198 slots V002,
                               coordinate_mode=COORDINATE_SPEC_ADDENDUM_V004.coordinate_mode)
0b. fs = make_freeze_coordinate_spec(coordinates=am['coordinates'])     # fs['coordinate_mode'] == DDO154_DISTANCE_FIXED_AT_REGISTERED
1.. engine, record, select, evaluate, reference, sensitivity: the v003a call order, unchanged
5.  write_freeze_manifest(..., notes=<slots V002 notes_block_for_manifest + an A18 entry>, ...)
```

- `fs['engine_coordinates']` equals the orchestrator c2v004 `ctx.engine_coordinates` in the A13 mode, canonically (TESTED). The orchestrator's own V001-to-A13 rule changes only the role of `distance_Mpc`.
- forward_ngc must refuse every NGC3198 geometry other than the registered 13.8 Mpc / 72° with a reason containing `GEOMETRY_NOT_EXPOSED` (A16.4).

## 2. Changes

### 2.1 Coordinate mode (A13)

- **New scope `ddo154_fixed`.** It requires role `fixed`, kind `distance`, units Mpc, `reference_value` = `trial_value` = 4.04, and sensitivity None. At most one DDO154 distance is allowed in total.
  - Its engine coordinate is scope `DDO154`, role `fixed`, sensitivity `NONE`.
  - The box is kept only for the engine's binding to `region.distance_summary`.
  - It is never sampled and never passed to forward_ngc.
- **Mode derivation.** The mode is a function of the coordinate list: `DDO154_DISTANCE_FIXED_AT_REGISTERED` if a `ddo154_fixed` coordinate is present, otherwise None (v003a behaviour). The writer, the verifier and the scorer all re-derive it from the frozen coordinates.
- **New `apply_coordinate_mode(*, coordinates, coordinate_mode)`** (keyword-only, fail-closed). It takes the V001-form list and the addendum declaration.
  - FIXED changes only the scope and role of the single DDO154 distance, and requires `fixed_engine_coordinates == {name: 4.04}` and trial value 4.04.
  - NUISANCE returns the list unchanged and requires `fixed_engine_coordinates` to be empty.
  - In both modes the varying engine names must equal `free_coordinates`.
  - It refuses a list that already holds a fixed distance.
- **`make_freeze_coordinate_spec`** additionally returns `coordinate_mode`, only in the A13 mode.

### 2.2 Manifest content (A13 mode only)

- **Labels.** Every NGC3198 band label ends with `; conditional on DDO154 D=4.04 (A13)`. This covers:
  - every `pointwise_envelope` row, including those of `alternative_results`;
  - `sensitivity.label` and every `sensitivity.per_query` row;
  - all three `band_scope` entries, the headline among them.
- **`conditional_on_trial_values`** gains one entry: kind `DDO154_FIXED_COUNTED_CONSTANT`, status `FIXED_COUNTED_CONSTANT_NOT_A_NUISANCE`, `sensitivity_evaluated` false.
- **New top-level key `headline_conditions`.** The module generates it, and the verifier recomputes it and requires equality. It holds:
  - the mode, plus the A13 citation (V003 addendum, sha `5bef6552…`, frozen and pinned);
  - the free engine coordinates;
  - the fixed counted constant;
  - the band condition;
  - the admissibility sentence;
  - `recorded_alternatives = [DDO154_DISTANCE_NUISANCE, NOT_EVALUATED_BEFORE_FREEZE, scored false]`;
  - the A16 slot summary;
  - the structural-assumption keys present.
- **Required notes:**
  - `notes.ngc3198_slot_sensitivity`, the A16.1 block (§2.3);
  - `notes.structural_assumptions` with `SA-BH-01` and `SA-REACH-01`, each with a non-empty `text_verbatim`;
  - one entry with `section: "A18"` and a non-empty `text_verbatim`.
- **Alternatives.** A declared alternative named `DDO154_DISTANCE_NUISANCE` with status `EVALUATED_BEFORE_FREEZE` refuses. A NOT_EVALUATED one is accepted.
- **Scorer.** The scorer echoes the A13 labels and adds `headline.band_condition` and `headline.headline_conditions`. It lists `DDO154_DISTANCE_NUISANCE` among the alternatives with `scored: false`.

### 2.3 NGC3198 slot geometry (A16.1 / A16.4)

- **When it applies.** The check applies in any mode when `notes.ngc3198_slot_sensitivity` is present. In the A13 mode the block is required.
- **The block must hold:**
  - status `NOT_EVALUATED_BEFORE_FREEZE`;
  - `applies_to` equal to the slot names;
  - `declared_range` equal to the slot boxes and trial values, units included;
  - `headline_geometry` equal to the slot trial values (distance 13.8 Mpc, and the inclination equal to its `reference_value` when one is declared);
  - a non-empty `manifest_reading_note`.
- **A16.4.** Every **evaluated** NGC3198 slot sensitivity entry must be a refusal: the flag is not True, no row is valid, and the reasons contain `GEOMETRY_NOT_EXPOSED`.
  - A box-end call that returned valid refuses the freeze, because it would freeze a false zero sensitivity.
  - A refusal without that reason also refuses.
  - Budget-unevaluated entries are counted, not refused (FREEZE_INCOMPLETE covers them).
- **Effect.** Every box-limited sensitivity row is invalid by design (43 of 43 in every test), and the manifest says so in `headline_conditions.ngc3198_slot_box_sensitivity`.
- **4-coordinate mode.** The A16 check adds no manifest content there; it is a check only.

### 2.4 Unchanged

Everything else is unchanged, as are the 4-coordinate outputs. The only exceptions are:
- `MODULE_NAME`;
- refusal texts that enumerate the accepted scopes or distance scopes, which now name `ddo154_fixed`;
- a 4-coordinate manifest carrying `headline_conditions`, which is refused with a different message (v003a: "unexpected keys");
- the A16.4 refusal above when the slot block is declared.

## 3. Choices (each a declaration, not a measurement)

| # | Choice | Alternative not taken |
|---|---|---|
| C1 | A new scope `ddo154_fixed` (the constant is not a nuisance) | role `fixed` inside `ddo154_nuisance`, which is still refused (probe P3 shape, test M7) |
| C2 | The mode is derived from the coordinate list | A separate mode argument stored in the manifest, which has two sources of truth |
| C3 | The distance alternative lives in the module-generated `headline_conditions` and the scorer's alternatives list | Requiring root to add it to `alternatives.declared`, whose ALT_KINDS have no calibration-coordinate kind |
| C4 | The A16 checks run in the 4-coordinate mode only when the slot block is declared | Always: a v003a-shaped call would then refuse |
| C5 | In the A13 mode, SA-BH-01, SA-REACH-01 and an A18 entry are required (A10, A12.2 and A18 say they enter the manifest). A18 is found by `section`, because the root has not named a key | Optional notes |
| C6 | With refused slot calls the whole box-limited band is invalid, as in v003a's per-query rule and A16.4's reading | Dropping the slot entries from the band, which would change v003a semantics (A16.1: root changes the declaration instead) |
| C7 | The V004 decisions addendum is open, so it is cited by name and never pinned; its bytes read `ffed3096…` at build time | — |

## 4. Tests (all on the final bytes `ca44ac47…`)

| Suite | Result | Run |
|---|---|---|
| `tests/test_freeze_c2v003b.py`. Blocks:<ul><li>R: 4D regression vs v003a on one engine run, clock frozen; manifests byte-identical after normalising module, own pin and self-hash; scorer equal; the A16 block is check-only in 4D; v003a writes and v003b refuses for a geometry-ignoring forward with the block declared.</li><li>M: mode vs the orchestrator rule; bad declarations.</li><li>SL: slots V002.</li><li>W: A13 writer, 8 positive checks and 11 refusals.</li><li>V: 10 re-hashed tamperings refused, a re-hashed control verifies, and v003a refuses the A13 manifest.</li><li>S: scorer.</li></ul> | **54/54 PASS** | `tests/runs/run_20261017T225053Z_53958` |
| `tests/test_orchestrator_freeze_path_c2v003b.py`. The orchestrator c2v004 T3 `freeze_path`, adapted (in-process executor, v003b pin), in two modes:<ul><li>4D, synthetic addendum: equal to v003a after normalisation.</li><li>3D, real V004 addendum: the addendum's FREEZE_COORDINATE_COMPATIBILITY deciding test, synthetic, reaches FREEZE_COMPLETE; engine coordinates equal `ctx.engine_coordinates`; the V001 list on the 3D record is still refused; v003a refuses the A13 list.</li></ul> | **10/10 PASS** | `tests/runs/ORCH_FREEZE_PATH_20261017T225054Z_53977` |
| Root call order toy `root_call_order_toy_v003b.py --mode 4D` (the v003a toy inputs) | FREEZE_COMPLETE, verify ok, 28 admitted, 10 members (as v003a) | `root_call_order_runs/run_4D_20261017T225052Z_53948` |
| Root call order toy `--mode 3D`:<ul><li>slots V002 and the A18 note;</li><li>refusing forward_ngc;</li><li>2 free coordinates, D fixed 4.04.</li></ul> | FREEZE_COMPLETE, verify ok, 26 admitted, 10 members; 4/4 box-end calls GEOMETRY_NOT_EXPOSED; 0/43 box rows valid; DDO154_DISTANCE_NUISANCE scored false | `root_call_order_runs/run_3D_20261017T225052Z_53950` |
| v003 self-test (path-only wrapper) | **64/64 PASS** | `regression/v003_selftest/runs/run_20261017T225031Z_51945` |
| X1 probes (path-only wrapper) | **19/19 PASS** | `regression/x1_probes/runs/run_20261017T225032Z_52087` |
| v003 checker fixtures (path-only wrapper) | **52/52 PASS**; pass/fail by id equal to the v003a record; `n_calls` 529 (as v003a) | `regression/checker_v003/runs/run_20261017T225038Z_52988` |
| v003a independent X1 attack check (path plus freeze-sha wrapper) | **41/41 PASS** plus OBS1/OBS2 (as v003a); ids and pass flags equal to the v003a record | `regression/x1_attack_check/runs/run_20261017T225044Z_53500` |

Each wrapper diff (`regression/*/PATH_WRAPPER.diff`) changes 2–4 lines. The self-test and the checker open the target-free NGC3198 query manifest `a2936517…`, ids only, as in v003a.

**Read-only trees were not modified (TESTED).** No file in `calibration_freeze_c2_v003a/`, `calibration_orchestrator_c2/v004/`, `ngc_freeze_inputs_c3/` or the monitor folder has an mtime after this lane started. Every v003a HASHES.txt entry still verifies.

## 5. UNTESTED, with deciding tests

- **The real forwards, the real DDO154 region `13c16a63…` and the real query manifest in PROGRAM_PIN role, all in the A13 mode.** Deciding test: the real ROOT_CALL_ORDER run.
- **A real NGC3198 forward_ngc wrapper returning GEOMETRY_NOT_EXPOSED.** A16.4 lists it as a required check before step 5: one real call at D = 12.545 Mpc and one at i = 69°. This module only enforces the consequence. No real wrapper exists under claude_artifacts (slots V002 notes).
- **The distance-as-nuisance alternative.** It is NOT_EVALUATED_BEFORE_FREEZE by design (A13). Deciding work: gal_c2v005 plus schema V005, then the D Jacobian column at two step sizes.
- **The orchestrator's campaign executor path into this freeze** (the T3 subprocess waves). The in-process executor was used to stay within 3 processes. The record and replay are the orchestrator's own in both cases.
- **`calibration_orchestrator_c2/v004a/`,** which appeared during this work. It was not read or tested.
- **The orchestrator coordinate spec and config still pin v003a** for the orchestrator's engine-coordinate derivation, and its `freeze_gate` text still asks for a successor. Root pins v003b for ROOT_CALL_ORDER steps 2–5. Changing the orchestrator pins was out of scope.

## 6. Housekeeping

- `__pycache__/prediction_freeze_c2v003b.cpython-312.pyc` was written by one `py_compile` syntax check. It is left in place, with no deletion. Every run used `-B`.
- Superseded runs are kept:
  - `tests/runs/run_20261017T224709Z_39932`: my audit hook was too broad and refused the root-decisions file; 37/39.
  - `tests/runs/run_20261017T224724Z_42099` and `tests/runs/ORCH_FREEZE_PATH_20261017T224911Z_47876`: pre-final bytes; 54/54 and 10/10.
  - `root_call_order_runs/run_4D_20261017T224404Z_25109` and `root_call_order_runs/run_3D_20261017T224408Z_25249`: pre-final bytes `cb0d352b…`.
  - The only change between those bytes and the final bytes is the wording of one refusal message.
