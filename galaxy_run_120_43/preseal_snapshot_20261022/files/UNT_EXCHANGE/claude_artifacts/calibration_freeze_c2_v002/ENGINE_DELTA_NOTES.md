# ENGINE_DELTA_NOTES — calibration_region_engine_c2v002.py (Claude2 lane)

Date (UTC): 2026-10-17. Supersedes `calibration_freeze_0462/calibration_region_engine_c3v001.py` (`f5613832…0e84e0b`), which is read-only and unchanged (re-hashed after every run).

**Scope**
- Claude4 0023 defects **A1** (false empty region) and **A2** (`_edge_t` tolerance).
- Engine side of decisions **D7** (iterated marches, global design, INNER_SAMPLE, REGION_POSSIBLY_TRUNCATED) and **D10** (units, scopes, `distance_summary` box, null-space completion).
- Engine-side should-fix items and cheap notes from the E1/E2/E3 slice reviews and verifiers in `review_0462_0464/`.

**Not in this file:** D5, D6, D8 and D9, and the freeze side of D7/D10 (`prediction_freeze_c2v002.py`, other helper).

**Safety.** No project forward model, no project run, no network, no scipy, single thread. The only data file opened is the hash-verified DDO154 region file (traced in T16). No NGC3198 file of any kind was opened.

## Hashes (computed from bytes)

| File | SHA256 |
|---|---|
| `calibration_region_engine_c2v002.py` (2422 lines) | `248ba5f909adfce589b11e6e52227b5ce182edd3ce01317b1d063fd994c02e05` |
| `engine_c2v002_selftest/selftest_engine_c2v002.py` | `4de0308cd550530201afe8ccbec39d06d12ea108067f4f374102adc08dd1e852` |
| `engine_c2v002_selftest/SELFTEST_RESULTS_ENGINE_C2V002.json` | `947dbd5792774d3abcce6ae1dc5a7321553a0b16f15c6a5588dda09d89a8b26c` |
| `engine_c2v002_selftest/ENGINE_DELTA_c3v001_to_c2v002.diff` (`diff -u`, 54 hunks, +1282/−286) | `fe55f42450585b510f9164523dce755eab4ac5995c5e7e47258ca56c9208fd53` |
| v001 engine (read-only, unchanged) | `f5613832fcb6e452b4490d56453cce37fb8846e802442407e794f80a6ec84e0b` |
| DDO154 region file | `13c16a6394fde450c9c1d9b258a8fb5dd01d80ce275a54d9761a285f76145b6d` |

**Self-test:** 75 checks, 0 failed. Two separate processes give byte-identical results files.

**Runtime:** codex python 3.12.14 `-I -B`, numpy 2.3.5, all six BLAS thread variables set to 1.

## API delta

All public functions remain keyword-only with no defaults, and every return carries `ok` and `reasons`.

| v001 | v002 |
|---|---|
| `explore_region(…, design_count, rng_seed, budget, log)` | Adds the required `global_design_count`, `max_march_rounds` and `hull_growth_tol`. |
| `run_calibration_region(…, design_count, rng_seed)` | Adds `global_design_count`, `max_march_rounds`, `hull_growth_tol` and `ddo154_distance = {'name', 'modulus_half_width_multiple'}`. |
| coordinate dict: 6 fields | Adds the required `units` (a non-empty str), `scope` and `sensitivity`. |
| — | **new** `shared_theta(spec, theta_natural)`, `ddo154_distance_box(distance_summary, modulus_half_width_multiple)` and `direction_box_extent(u, direction)` |

**Coordinate fields**
- `scope` is `'shared'` or `'DDO154'`; the freeze lane's spelling `'ddo154_nuisance'` is accepted as an alias.
- `sensitivity` is `'NONE'`, `'BOX_ENDS'` or `{'step_natural': x}`; the freeze lane's spellings `None`, `{'mode': 'box_ends'}` and `{'mode': 'step', 'step': x}` are accepted.
- Rules:
  - free coordinates must be shared;
  - nuisance coordinates must be DDO154;
  - sensitivity is allowed only on shared fixed coordinates, and trial ± step must lie inside the box;
  - `'ngc3198_nuisance'` is refused, because other galaxies' slots never enter this engine.

**Exploration statuses:** `COMPLETE`, `BUDGET_EXHAUSTED`, `NO_ADMITTED_POINT_FOUND` and `NO_VALID_EVALUATION`.
- `ok` is True only for `COMPLETE`.
- Run-level statuses add `INPUT_INVALID`, `SEED_INVALID`, `JACOBIAN_INCOMPLETE`, `JACOBIAN_FAILED` and `EXPLORATION_FAILED`.
- `NO_ADMITTED_POINT` no longer exists.

**New output fields.** The exploration output, and the run output where marked "run", gain:
- `admitted_point_found`;
- `empty_region` (never True);
- `emptiness_proven` (always False);
- `admitted_set_label='INNER_SAMPLE'` and its statement;
- `region_possibly_truncated` and `truncation_causes` (run);
- `flags` (run);
- `coverage`;
- `box_limited_null_directions`;
- `primary_anchor`, `log_scan`, `repair.phases` and `repair.terminated_by`;
- `global_design`, `march_rounds` (including `lp_rays`), `refinement_status` and `hull_history`;
- `near_null_shifted`;
- `coordinate_units` (run) and `coordinate_ranges` (with units);
- `n_admitted_by_purpose`;
- per admitted point: `identified_projection`, `near_null_projection`, `on_anchor_slice` and `interior_score`;
- `shared_names` and `ddo154_scoped_names` (run);
- `ddo154_distance_binding` (run).

Log entries gain `u_clip_move`, and the purposes gain `'global_design'`.

## Line-level delta (v001 line → v002 line)

The full mechanical delta is `engine_c2v002_selftest/ENGINE_DELTA_c3v001_to_c2v002.diff`.

### A1 — false "empty region"

| v001 | v002 | Change |
|---|---|---|
| L1154–1158: `empty_region=True`, `ok=True`, `NO_ADMITTED_POINT` | L1791; L1951–1966 | `empty_region` is False when an admitted witness exists and None otherwise; it is never True, and `emptiness_proven` is always False. `NO_ADMITTED_POINT_FOUND` (the reason says "NOT a proof … must not be registered as 'the model family fails DDO154'") and `NO_VALID_EVALUATION` both have `ok=False`. |
| L1412–1417: only the seed reaches the exploration | L1601–1625 (`verified_admitted`, `admitted_entries`); L1856–1867 | **Whole-log scan:** every log entry (seed, Jacobian, repair, march, bisection, design, global design) is re-classified from its logged prediction. When the anchor is not admitted, the most interior admitted entry becomes the primary anchor before any repair call. `admitted_points` is built from the whole log (L1763–1790). |
| L1108–1153: one L2 repair on identified directions | L1869–1949 | **Repair:** phase `identified` (the v001 step), then phase `numerical_rank` (every direction with s_k > 1e-9·s_max; review E2-F2(b)), up to `repair_iterations` evaluations each. `terminated_by` records the reason; `iterations_exhausted` is reported as "not evidence of emptiness" (E3-M2). |
| L1124–1125: L2 step only | L1409–1438 `_minimax_step`; used at L1900 | **Step metric:** a max-norm (Lawson) refinement of the step, as E3-FIX1. It replaces the L2 step only on a strict improvement, so a reachable target keeps the L2 step bit for bit (T12). |
| L1151: `cap = 0.5*cap` | L1938: `cap = 0.5*min(cap, norm)` | The retried step is really shorter (E3-M3). |
| L1111–1112: no identified direction means empty | L1951–1966 | When nothing is admitted, a coarse global Halton design over the whole box runs before the march. |

### A2 — `_edge_t` without tolerance

| v001 | v002 | Change |
|---|---|---|
| L933–942 | L1273–1288 | Components with \|d_j\| ≤ `_BOX_TOL` are treated as zero. Face slack uses `max(1−a_j, _BOX_TOL)` and `min(−a_j, −_BOX_TOL)` (E2 verifier P1b), so interior anchors are byte-identical. |
| L1179–1192 | L1682–1696 | A side closed at a face with no evaluation sets `closed_at_face_without_evaluation` and emits a reason (E3-M4). |
| L1179: `t > t_edge + _T_TOL` | L1682: `t > t_edge` | Every t beyond the edge goes to the exact edge evaluation (E1-N1). |

### D7 — coverage

| v001 | v002 | Change |
|---|---|---|
| — | L2017–2023 | **Coarse global design.** A Halton design over all of [0,1]^n (bases are the first n primes, first index `rng_seed+1`, duplicates skipped) runs after the local design, unless it already ran. `global_design_count=0` adds the cause `global_design_not_run`. |
| — | L2035–2160 | **Iterated rounds**, `max_march_rounds` of them. Each round has two parts.<br>(a) **Linearised-polytope rays** (E3-F5's alternative; `_lp_max` L1441, a dense simplex with Bland's rule). The polytope uses the fixed seed Jacobian, re-based at the current extreme admitted point and bounded by the box. It is maximised along ±v_k. If its extent beats the hull by more than `hull_growth_tol`, the engine marches from the primary anchor toward that vertex.<br>(b) **Outward axis marches** from unused extreme admitted points.<br>The rounds stop when the hull box grows by ≤ `hull_growth_tol`, which gives `CONVERGED` / `CONVERGED_NO_NEW_EXTREME_ANCHOR`. Otherwise the end state is `ROUNDS_EXHAUSTED`, `BUDGET_EXHAUSTED` or `NOT_REQUESTED`. |
| L1075–1083: hull from the admitted list | L1763–1840 `finalise` | **Finalise.** The hull is taken over all admitted log entries. The label is `INNER_SAMPLE`. `truncation_causes` can contain `budget_exhausted`, `hull_convergence_not_verified`, `march_reached_box_edge`, `admitted_point_on_box_face`, `global_design_not_run` or `no_identified_direction`. Near-null directions are listed separately in `box_limited_null_directions` (D6 is the freeze module's job). |
| L1262–1265 | L2024–2033 | **Budget.** Running out of budget inside the core stages gives `BUDGET_EXHAUSTED`, and unfinished sides get boundary None (E3-F7). Running out during the iterated rounds keeps `COMPLETE` with the causes `budget_exhausted` and `hull_convergence_not_verified`. |

### D10 — units, scopes, distance, null space

| v001 | v002 | Change |
|---|---|---|
| L123–144, L378–442 | L181–260, L507–586 | **Spec.** `units`, `scope` and `sensitivity` are validated and normalised, and the spec gains `units`, `internal_units` (`ln(Mpc)` for log coordinates), `scopes`, `shared_names`, `ddo154_scoped_names` and `sensitivity_declared_names`. |
| — | L666–700 `shared_theta` | Strips the DDO154-scoped coordinates. |
| `distance_summary` loaded but unused | L708–762 `ddo154_distance_box`; L2206–2245 `_check_distance_binding`; called from the run | **Distance box.** The box is mu_c − k(mu_c − mu_lo68) … mu_c + k(mu_hi68 − mu_c), mapped to Mpc; k=1 returns the reported 68 values exactly. The summary's internal consistency is checked: central = 10^((mu−25)/5) to 1e-9. The run refuses a distance coordinate whose box differs (relative 1e-12), whose units are not Mpc, whose scope is not DDO154, whose role is free or whose transform is not log. |
| L885–886: padded zeros, no record | L1207–1240 | **Null space.** `null_space_completion` records rank bound, padded indices, orthonormality error and null residual, and a reason is emitted when n > 12. Also new: `effective_null_tolerance = max(tol, max(m,n)·eps)` (E2-M1) and the warning `near_null_with_sensitivity_ge_1` (E2-F2(b)). |

### Review should-fix items and notes fixed on the engine side

| Item | v001 | v002 |
|---|---|---|
| E1-F1 `to_unit` reasons lost | L486 | L638 |
| E1-F5 / N4 linear face overshoot; log overflow | L460–469 | L611–618 (x and v clamped for both transforms) |
| E1-F6 / N2 raising return or `str()` | L521–533, L627–639 | `_safe_str` L115; `try` around handling L896–918 |
| E1-F8 / N3 ndarray transform or role | L125–127 | `isinstance(…, str)` guards at L220–223 |
| E1-F9 str reasons dropped | L531–532 | L779–781 |
| E1-F10 unexpected keys silent | L583–593 | L846–849: `unexpected_keys` plus a reason (validity unchanged) |
| E1-F13 `bounds_semantics` in `to_unit` | L485 | L633 |
| E1-N5 logged speeds ≠ classified speeds | L634–638 | L907–910 |
| E2-F3 halving keeps the clipped side; wasted minus call | L736–770 | L1012–1054 |
| E2-F5 non-finite | L772, L879–896 | Column L1061–1063; S and SVD checks L1190–1201; `cond` 'inf' L1216 |
| E2-F6 sign tie-break | L813–816 | L1106–1121 |
| E2-F7 / M4 asymmetric span; stencil indices | L775–778 | L1066–1073: `span`, `asymmetric`, `plus_log_index`, `minus_log_index` |
| E2-F8 failed columns `ok=True` | L800–803 | L1096–1097: `COMPLETE_WITH_FAILED_COLUMNS` with `ok=False`; the run maps it to `JACOBIAN_INCOMPLETE` (L2382) |
| E2-F10 `rel_step` unbounded | L681 | ≤ 0.5 at L964 and L2291 |
| E2-F12 aliasing of returned points | L949–954 | L1337–1346 (deep copies) |
| E2-F4 / E3-F11 inconsistent identifiability report accepted | L957–991 | L1348–1407: checks row_ids, varying_names, orthonormal V, ordered s, ‖S v_k‖ = s_k, and that `identified` follows from the rule |
| E3-F2 repair box clip moves near-null | L1130 | L1916–1928: `near_null_component` per step, `near_null_shifted` and a reason (verifier's replacement; the clip itself is kept) |
| E3-F3 `trial_projection` is the seed | L1063 | L1659–1667: `trial_projection` from the trial values, plus `seed_projection` and `trial_differs_from_seed` |
| E3-F6 `min_step > rel_step` reported as `SEED_INVALID` | L1309–1326 | L2290: `INPUT_INVALID` |
| E3-F8 duplicate design points | L1243–1257 | L2010 and the global design: duplicates within `_BOX_TOL` are skipped and counted |
| E2-M3 admitted Jacobian points excluded | L1042–1095 | Covered by A1: every admitted log entry is in the set |

## Kept from v001

Hash-before-parse region binding; the closed rectangle; the validity rules; the log schema; seed reuse; the doubling march with one edge evaluation; exactly `bisection_steps` bisections; the round-0 `boundary` / `boundary_detail` semantics; the local Halton design; the per-call budget check; `ngc3198_access='NONE'`; `bounds_semantics`; inert import.

**Parity (T12).** With the new stages off (`global_design_count=0`, `max_march_rounds=0`) and no finding triggered, the evaluation sequence is identical to v001 in u, call for call:
- 61 = 61 calls with an admitted interior seed;
- 61 = 61 calls with a rejected seed whose linear target is reachable.

The round-0 boundaries are also identical.

**Documented, not changed:** `np.True_` is accepted as `valid` (E1-F2). The freeze lane must apply the same rule to the forward returns it handles.

## Self-test evidence: Claude4 counterexamples, v001 against v002 (same inputs, synthetic)

| Case | v001 (frozen) | v002 |
|---|---|---|
| **A1, tol 0.01** (P4 D6a, rebuilt independently). The grid truth reproduces **3981** admitted points out of 1001². | `NO_ADMITTED_POINT`, `empty_region=True`, 8 evaluations | `COMPLETE`. The `numerical_rank` repair is admitted at its first step; every admitted point is checked against the toy truth. With repair and global design disabled: `NO_ADMITTED_POINT_FOUND`, `empty_region=None`, `ok=False`. |
| **A2, face-anchor march truncation.** An inert coordinate `d` has its trial value at 0, order `adbc`, n=4. Three coupling seeds trigger the LAPACK leak on this build. | Sides closed at t=0 with no evaluation: seed 1 (0−, 1+, 2+), seed 2 (0−, 1−), seed 3 (0−, 1−, 2−) | The boundaries equal the interior control (`u_d=0.5`) to **0.0**. No side is closed, and the status is `COMPLETE`. |
| `_edge_t([0,.5],[−1e−17,1])` | 0.0 | 0.5. A genuine outward component (−1e−3) still exits at once (≤ 1e−9). |
| E3 VD1 (L2 optimum rejected, minimax admitted) | false empty | `COMPLETE` through the max-norm repair, with no global design |
| E3 VD3 (zero Jacobian) | false empty | `COMPLETE` through the global design |
| E3 M1 (admitted Jacobian entry) | false empty that contradicts its own log | `COMPLETE`. The primary anchor is the Jacobian entry (log 1), with 0 repair calls. |
| E3 M2 (repair-iteration limit) | false empty | `NO_ADMITTED_POINT_FOUND` with `terminated_by=iterations_exhausted` when there is no global design; `COMPLETE` with one |
| E3 M3 (invalid band on the L2 path) | 3 identical evaluations at u=0.5, then false empty | 0.5 (invalid), then 0.59 (admitted), `COMPLETE` |
| Truly empty control | — | `NO_ADMITTED_POINT_FOUND`, `empty_region=None`, `emptiness_proven=False` |
| **D7, E3 D4 parallelogram.** True range of y−½ is ±0.30. | ±0.2424 (coverage 0.81), 87 evaluations | ±0.2997 (coverage 0.999), 210 evaluations. Rounds: growth 0.049, then 0.0, giving `CONVERGED`. |
| D7, two islands | one island | both islands (4 global-design points in the second); every point is checked against the truth |
| E2-M1, tol 0, s_min 1.3e−16 | `near_null=[]` | `near_null=[3]` |
| E2-F3 (seed 0.01, invalid below 0.004, `max_halvings=1`) | column fails | column succeeds, with no repeated stencil point |

**Other checks**

- **Inertness and signatures:** AST top level, no `__main__`, keyword-only with no defaults.
- **Spec refusals:** 9 bad specs, refused without raising.
- **Freeze-lane spellings:** accepted; `ngc3198_nuisance` is refused.
- **Distance box:**
  - k=1 gives the reported 68 values exactly; k=2 is derived from the modulus;
  - an inconsistent summary is refused;
  - a coordinate box of [3.9, 4.2], wrong units, or a missing binding gives `INPUT_INVALID` with 0 evaluations.
- **Null space:** n=14 > 12 gives padded indices [12, 13], orthonormality error 1.6e−15 and a reason.
- **Identifiability reports:** reversed, scaled, or with the wrong identified set → refused with 0 evaluations.
- **Budget sweep:** budgets 0–59 and N±1, with N = 105. log = min(budget, N), and each log is a prefix of the full run. Results are strict JSON and `empty_region` is never True. Unfinished sides are None. Between the end of the core stages (51) and N, the status is `COMPLETE` with `budget_exhausted`.
- **Determinism:** canonical sha `c1f83c02…4369`.
- **Pathological forwards:** `ValueError(10**5000)`, a dict with a raising `get`, str reasons, extra keys and an out-of-box u are all logged, and nothing escapes.
- **File access:** only the region file is opened.
- **Freeze-lane outputs:** `flags` and `coverage` are emitted.

## For the root and the freeze lane

1. **Integration (blocking for a joint run).**
   - `prediction_freeze_c2v002.py` L628–629 builds `engine_coordinates` as six-field dicts. This engine requires `units`, `scope` and `sensitivity`, and refuses six-field dicts as "missing fields".
   - Pass the full coordinate dicts, minus the `ngc3198_nuisance` slots. Extra keys (`kind`, `reference_value`) are ignored, and the freeze spellings are accepted.
   - Also pass `ddo154_distance={'name': <the DDO154 distance coordinate>, 'modulus_half_width_multiple': k}`. The draft spec's `distance_Mpc` box [3.98107…, 4.11150…] is the k=1 box exactly.
2. **Budget cost of D7.** A sizing toy matches the 0470 proposal: 5 varying coordinates, 4 identified directions, `rel_step` 0.05, `march_step` 0.05, 3 bisections, `design_count` 12, `global_design_count` 12.
   - The core stages use **85** evaluations.
   - With `hull_growth_tol` 0.02, the iterated rounds converge at **203**.
   - With a budget of 120, the run ends `COMPLETE` with `REGION_POSSIBLY_TRUNCATED` (`budget_exhausted`, `hull_convergence_not_verified`).
   - The budget and `max_march_rounds` are the root's call. Set `hull_growth_tol` no smaller than the bisection resolution (about `march_step·2^−bisection_steps`); below that, the rounds chase bisection noise.
3. **Freeze gate.** Gate on `status == 'COMPLETE'`, then read `region_possibly_truncated` / `truncation_causes`.
   - A region with any near-null direction is listed in `box_limited_null_directions`, which is D6's input.
   - Admitted points may lie off the anchor's near-null slice: Jacobian, global-design and `numerical_rank` repair points. Each point carries `on_anchor_slice` and `near_null_projection`.

## Not changed (outside the engine, or open)

- **E2-F2 / M2:** the relative identification rule, and FD-truncation artefacts at small tolerances. These are interface decisions for the coordinator. The `numerical_rank` repair phase and the `s ≥ 1` warning mitigate them; the rule is unchanged.
- **E2-F11:** Halton correlation at high bases (n ≥ 10).
- **E1 notes left as they were:**
  - F3: `_U_TOL` snapping in `to_unit`, which has no caller;
  - F4: fixed values supplied to `to_unit`;
  - F7: a huge linear box;
  - F12: a forged region dict;
  - F14 and F15: region-file mutants, which are interface-compliant.
- **`JACOBIAN_FAILED`** is still unreachable from the run.
- **Untested:**
  - the nonlinear chord-stall mechanism (E3-F1);
  - LAPACK builds other than Accelerate arm64 (the A2 trigger pattern depends on the build; the fix does not);
  - any real forward model.
