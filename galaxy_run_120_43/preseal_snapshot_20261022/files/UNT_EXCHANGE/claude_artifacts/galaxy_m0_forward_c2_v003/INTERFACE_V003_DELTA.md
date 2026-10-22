# INTERFACE_V003_DELTA: galaxy_m0_forward_c2v003 relative to c2v001

`INTERFACE_C2_0466_V001.md` (`10d1db3c…`) still applies. This file lists only what changes. Nothing here launched a project calculation. Everything was run in simulate mode or as a synthetic test (14/14 pass, `test_runs/RUN_V004/TEST_RESULTS.json`). All hashes are computed from bytes and listed in `HASHES.txt`.

| | File | sha256 |
|---|---|---|
| base | `galaxy_m0_forward_c2_0466/galaxy_m0_forward_c2v001.py` | `75b0c08a44eac92caedd46564eaaefe08b88a6c536e95cb46f54a9d8da962f22` |
| new | `galaxy_m0_forward_c2v003.py` | see `HASHES.txt` |
| line diff | `DIFF_V001_V003.txt` | 164 lines added, 6 removed |
| monitor (reused, unchanged) | `galaxy_m0_forward_c2_0466/root_monitor_c2v001.py` | `ba031c2340057d88ee399138cc645012a93aa7dc3eb7c9bba56d112c94a47107` |
| campaign (reused, unchanged) | `galaxy_m0_forward_c2_0466/campaign_c2v001.py` | `71274ceb15e57786ee8f575fd74b48e848193467156f0adcebbe7ee415e44597` |

The schemas are unchanged: call `UNT_GALAXY_M0_FORWARD_CALL_C2V001`, result `UNT_GALAXY_M0_FORWARD_RESULT_C2V001`, dry-run `…_DRYRUN_C2V001`. Existing specs and the kmax comparison script's `adapt_result()` therefore work unchanged.

## 1. Route-A prep pin (item 1)

**Located and verified from bytes:**
- `helpers/coefficient_method/ddo_actual_initial_source_preparation_v007.py` `ac905597…`
- `helpers/coefficient_method/ddo_actual_initial_source_preparation_v008.py` `bb05f974…`. The only diff from v007 is line 130, `nk>80` → `nk>96`.
- `helpers/response_packet_audit/CURRENT_SOURCE_ALL_PANEL_DERIVATIVE_AUDIT_REVIEW_V001.json` `aa12d69f…`

**Rule:**

| Axis nodes | Prep used | How |
|---|---|---|
| ≤ 80 | v007, as in c2v001 | No override. Route A uses the worker's own `LOCAL['prep']`. |
| 81–96 | v008 | The request carries `stage_dict_items: {LOCAL: {prep: {path, sha256}}}`. The shim replaces exactly that one `(path, sha)` entry of the route-A worker's `LOCAL` dict after the worker's code has run. Before replacing, it re-verifies the file from bytes and requires that the entry exists. Dict order is kept. |
| > 96 | none | Refused. |

**What else follows the prep choice:**
- The `COEFFICIENT`/`COEFFICIENT_SHA` patch targets whichever prep is used, so v008 for the large grids.
- The route-A worker still verifies every `LOCAL` pin itself.
- The binding accepts the module because its `accepted_module_pins` come from that same `LOCAL`.
- No route-B stage references the prep (checked by grep).
- The v008 review file is a static pin of every call.

**Why v007 is kept for ≤ 80 nodes instead of using v008 everywhere.** For those grids, v008's grid construction is bitwise equal to v007's: t05 runs both reviewed guard blocks from bytes and gets an identical axis for G2. But the prep file's path and sha enter the route-A `code_pins`, and from there the checkpoint `IDENTITY` (`98816902…` at reproduction). So v008 cannot reproduce the saved identity bitwise. v007 stays.

**Evidence that reproduction plans are unchanged.** `dryrun/PLAN_COMPARE_*.json` compares v003 against v001 simulated in the same way. For `REPRO_PINNED_ADMIT_PREFIX` (19 stages), `REPRO_PINNED_FULL` (22 stages) and `KMAX_C2`, all of these are identical after normalizing the report-dir prefix and the generated-manifest sha:
- every stage row (script, sha, argv, stage_globals, module_patches, mask, argv and override comparisons);
- `DRYRUN_PLAN.txt`;
- the simulated final rows.

**Report fields that differ from v001** (none of them is a stage input):
- `driver_sha256`;
- `identity.route_a.prep` and `custody.prep_code_pins` (new; these record v007);
- two extra static pins: v008 and the review;
- `transitive_pins.verified_files`, 45 → 46;
- the route-A pins note;
- the new summary wording fields.

## 2. Declared kmax grids G3/G4/GR (item 2)

**What changed.** `normalize_spec` accepts a composite grid with more than 80 nodes per axis only if its `(breaks, panel_orders, total)` equals one of the declared grids. These are `DECLARED_LARGE_GRIDS`; t03 checks them against `KMAX_MATRIX_PREREG_V001.json` (`d5acfc2f…`).

| Grid | Breaks | Orders | Nodes per axis |
|---|---|---|---|
| G3 | ±3 + G2 | 6×14 | 84 |
| G4 | ±4, ±3 + G2 | 6×16 | 96 |
| GR | G2 | 6, 8×10, 6 | 92 |

Grids with ≤ 80 nodes are accepted exactly as in v001 (t03, t04).

**The `cube`-with-`kmax` refusal is unchanged.** No declared spec needs it removed:
- the wave-1 C2/C3/C4/R specs are cube without `kmax_inverse_kpc`;
- the wave-2 S/Y templates are sphere or cylinder with kmax equal to the grid edge, which is allowed (t02).

**The specs run unchanged.**
- `specs/wave1` C2/C3/C4/R normalize identically under v001 and v003 (t01).
- Their bytes are unchanged (`7c7330bf…`, `9c71cf5c…`, `e24d52e3…`, `46491eba…`).
- The kit's own generator reports `driver_mentions_prep_v008: true` against v003 and regenerates byte-identical CALL specs (t11).

**Driver-sha re-pin.** `specs/CAMPAIGN_KMAX_WAVE1_C2V003.json` is `CAMPAIGN_KMAX_WAVE1_C2V001.json` with only the `driver` block changed (path and sha → v003). It is equivalent to the kit's one-line regeneration:

```
make_kmax_specs_c2v001.py wave1 … --driver <v003> --driver-sha256 <H>
```

The calls, monitor and caps are identical (t14).

**Simulated plans** (`dryrun/V003_KMAX_{C3,C4,R,C2}_V001`, 0 stages executed, no pin problems, no scipy):
- C3, C4 and R plan route A with `LOCAL[prep] := v008` and the A2 `COEFFICIENT` patch on v008.
- C2 plans v007 with the patch on v007, identical to v001.
- Rule mode stops planning at the RFS stage, whose controls depend on computed enthalpies, as in v001.

## 3. Mask-fired assertion (item 3; CHECK_V001 §3 correction 2)

**What runs.** For sphere and cylinder only, `mask_fired_check()` runs after the offset stage, in run mode, before `OFFSET_SHA` is formed. It:
1. reloads `unit_response.npz` and `offset_prepared.npz`;
2. requires their `wavevectors` to be bitwise equal;
3. recomputes the mask with the same `truncation_mask()`;
4. requires every row outside the mask to be exactly 0.

**What it records** in `identity.truncation.mask_check`:
- kept and total nodes;
- the outside row count;
- the count of kept rows that are all zero;
- the file shas;
- `vacuous`.

It also writes a `mask_check` progress event.

**On failure** it raises `StageFailed('MASK_NOT_FIRED …')`, so the call ends `FAILED_AT_STAGE` and no column stage starts (t09). The message includes the kept count. Cube installs no hook and runs no check, as before.

## 4. CHECK_V001 corrections applied (item 4)

| CHECK_V001 item | Change |
|---|---|
| §3 corr. 1: mixed field | Documented in the `truncation_mask` docstring and in `identity.truncation.scope`. Route A, reference and body run unmasked (cube G4). Under sphere or cylinder, these are cube-G4 plus the masked offset: the offset real-space total; its reality, lapse and C-eigenvalue guards; and `updated_base_arrays` `full_fields_complex`/`Phi0`/`angular_forcing_dPhi`/`base_residual_r0`. Downstream stages read only `radial_nodes_m`, `K0`, `Sigma` and the RdR weights from that file. |
| §3 corr. 3 | Recorded as a constraint. The cache `evaluate()` bypasses the wrapped `prepare`, so only `prepare()` may be relied on. |
| §1 doc: override counts | Read "50 of 52" (`ADMIT_PREFIX`) and "56 of 58" (`FULL`) where INTERFACE line 110 and §10 say "50/50" and "56/56". The 2 others are the extra LE1/LE2 column-mean `PINS`. The dry-run summary now prints `overrides_wording` and `overrides_not_noop`. |
| §2 minor | `per_call_seed` adds a top-level `c2_changed_fields` note: base sha, changed fields, and which copied annotations describe the base seed. It is added only when the seed is not reused. No stage reads it; only `numerical_inputs`, `physical` and `pins` are read (grep). Consequence: the seed sha of non-reused seeds differs from v001's. Reused base seeds (all reproduction specs, C2) are unchanged. |
| §8 scan scope | INTERFACE line 234 should read: "no scipy in the checker's 59-file scan (`CHECK_V001` §8); the driver scanner verifies 46 pinned files and misses separate `NAME`/`NAME_SHA` globals and prep-local `paths`". The scanner code is unchanged. |
| Further defect 1 | `require_bracket_source()`: in rule mode, a missing previous column raises `StageFailed('<tag> column(s) […] failed; no bracket source')` instead of a bare `KeyError` (t10). |
| Further defect 2 | `result.json` gains `picard_bound_met`: true, false, or null when there is no bound or no change (t10). |
| Further defect 3 | Coefficient, pinned-controls and admit paths must be absolute (refused otherwise). All shipped specs already use absolute paths and normalize as in v001 (t04). |

**Not changed (outside this item list):**
- Further defect 4: the `reference_comparison` gap at the reference radii.
- Further defect 5: the example-spec overrides.
- CHECK §6 corrections 1–3, which are in `campaign_c2v001.py`; it is reused unchanged by sha. Until §6.1 is fixed, never `--resume` a campaign while monitors of a crashed campaign are still alive.

## 5. Operational note for the kmax matrix

`CLAUDE2/runs/KMAX_C2_A2_RUN_V001` runs under v001 (`75b0c08a…`). For C2 the v003 plan is identical to v001's (`dryrun/PLAN_COMPARE_KMAX_C2_V001.json`). However, `kmax_compare_c2v001.py` gate V3 requires one `driver_sha256` across all cases, while C3, C4 and R can only run under v003. As built, combining that C2 result with v003 cases gives V3 = false, which means INCOMPLETE. Two paths keep the comparison decidable:
- C2 is re-run under v003 (about 1.74 h);
- V3 is amended to accept the pair {v001, v003} for ≤ 80-node cases, on the evidence of the plan identity above.

The same applies to wave-2 S2 and Y2 admitting that C2.
