# INTERFACE_V003B_DELTA: galaxy_m0_forward_c2v003b relative to c2v003

`INTERFACE_C2_0466_V001.md` and `INTERFACE_V003_DELTA.md` still apply. This file lists only what v003b changes. Nothing was launched: simulate-mode dry runs and synthetic tests only (11/11 pass, `test_runs_v003b/RUN_V003/TEST_RESULTS.json`; earlier runs are in `test_runs_v003b/superseded`). The two in-progress runs were not touched. Hashes are computed from bytes and listed in `HASHES_V003B.txt`.

| | File | sha256 |
|---|---|---|
| base | `galaxy_m0_forward_c2v003.py` | `b052e3ae43fcf8782cc9cca99dec2cdc8f7fcbf479af7b92738feb196c00033b` |
| v001 | `galaxy_m0_forward_c2_0466/galaxy_m0_forward_c2v001.py` | `75b0c08a44eac92caedd46564eaaefe08b88a6c536e95cb46f54a9d8da962f22` |
| new | `galaxy_m0_forward_c2v003b.py` | `7ce59e05f39e0517fd7c1d89a6c31b116b96662ee475fec88f47ae76ab1184f1` |
| line diff vs v001 | `DIFF_V001_V003B.txt` | 408 lines added, 22 removed |
| line diff vs v003 | `DIFF_V003_V003B.txt` | 239 lines added, 17 removed |

The call, result and dry-run schemas are unchanged.

## 1. Outcome

| Nuisance | Status in v003b |
|---|---|
| `physical.distance_Mpc` | **Exposed.** Any finite positive value is accepted. |
| `physical.inclination_deg` | **Still registered-only (66).** Every other value is refused with `BLOCKED_GAS_REDEPROJECTION`; see §4. |

At the registered geometry (4.04 Mpc, 66 deg), v003b plans, writes and pins nothing that v003 does not (§3). This is the calibration-spec trial point (t10).

## 2. Where distance enters, and how v003b derives it

**No producer script for `GALAXY_RADIAL_SOURCE_REFERENCE_V001.json` exists on disk.** Each formula below is the documented rule. Before it is used at D, `derive_geometry()` checks that it reproduces the pinned registered record **bitwise** (`registered_formula_guards`; t01).

Notation: λ = D/4.3 (the HI extraction distance) and μ = D/4.04 (the photometry and catalogue distance). Every source and query length therefore scales by μ.

| Quantity | Formula at D | Source of the rule | Bitwise at 4.04 |
|---|---|---|---|
| HI `s_edges_kpc2` | `(r_4.3·λ)²`, with r = calibration input NA `r_lo[0]`+`r_hi[:18]` | calibration input `source_conversion.distance`; `extract_source.py` radii = angle·D | yes |
| HI annular means and boundary/middle controls | unchanged | same ("angular-bin surface density unchanged") | yes |
| HI `integrated_mass`, `original_retained_mass_scaled`, `support_radius`, pairing difference | `fsum(π·1e6·Δs·mean)`, `fsum(mass)·1.36·λ²`, `r_hi[-1]·λ`, as stored | same (masses ∝ λ²) | yes |
| stellar `radius_kpc` | `arcsec·(D·1e3)/206264.806…` | `STELLAR_PHOTOMETRIC_REFERENCE_MEAN_PROFILE_V001` `radius_kpc_reference` | yes |
| stellar Σ | `Σ_64·cos66/cos64`, independent of distance | photometric `Sigma_L=cos(i)·I_sky`; profile `stellar_faceon_factor_from_64deg` | yes |
| stellar `outer_scale` (Rd), `height` (Rd/7.3) | pinned value · μ | photometric `R_d … converted with D`; binding V001 `h=Rd/7.3` | yes (·1.0) |
| stellar masses; midplane density | ·μ²; ·1/μ | follow from the radii and h | yes |
| binding `query_rows.radius_m` | `r_cat·(D/4.04)·kpc_m` | calibration `r_model = r_cat·(D/4.04)` | yes |
| monotone source | the pinned reviewed reducer V002 (`50edaba7`) re-run on the per-call HI record, with the saved sweeps and KKT | `DDO154_MONOTONE_SOURCE_RECONSTRUCTION_RUN_V001` launch | yes; every computed key |

**One documented substitution.** The Rd recipe (OLS) reproduces the saved Rd only to 2 ulp: 0.35842260988496**64** against **66**. So Rd and h are scaled from the pinned values by μ instead of being recomputed.

Masses are never set directly in the stages. They follow from the scaled radii, exactly as the reviewed code computes them (t11).

**Per-call files** go under `<outdir>/inputs/`:
- `geometry_C/GALAXY_RADIAL_SOURCE_REFERENCE_V001.json`, the per-call profile. Only `galaxies.DDO154` is re-derived; the NGC entry is copied unchanged.
- `geometry_C/GALAXY_PHYSICAL_SOURCE_STATE_BINDING_V003.json`, a byte copy, sha `7cadac8b…`, re-verified.
- `geometry_monotone_source.json`.
- `geometry_column_mean_binding.json`.

The profile has to live in a directory named as prep's `C`, because prep V007/V008 reads `C/'GALAXY_RADIAL…'` and `C/'…BINDING_V003.json'`. Both copies are pinned from bytes. Content is deterministic per D: for example, the profile sha is `59c7f6c1…` at the box upper edge and `f0a47044…` at the lower edge.

**Stage plumbing.** These overrides are added only when the distance is not 4.04. Each uses an existing shim mechanism and targets an existing global (t07: no `OVERRIDE_TARGET_ABSENT`; t08 runs the real `_stage` shim on the real prep and homotopy modules).

| Stage | Override |
|---|---|
| route A | prep module patch `C` → `geometry_C`. Merged with the COEFFICIENT patch when the coefficients are not the default. |
| reference | `stage_globals` `PROFILE`, `PROFILE_SHA` |
| body, offset, columns, rotation, feedback | `reuse_patch` adds `PROFILE`, `PROFILE_SHA`. The offset reads its radial domain from it; body checks against it. |
| body | `SOURCE` plus the third `DATA_PINS` entry → per-call monotone source |
| rotation v001/v005 | `SOURCE`, `SOURCE_SHA`. Feedback's `SOURCE` is a code module and is not touched. |
| column mean v004 | `PINS[0]` → per-call binding |

**What t06 checks.** In run mode with a no-op Popen, every request at D = 4.1115 and D = 3.9811 equals the registered request once exactly these entries are removed.

**New refusals.** These only affect the error path.
- `ROUTE_A_GEOMETRY_MISMATCH`: the profile pin in the checkpoint `code_pins` is not this call's profile.
- `REFERENCE_GEOMETRY_MISMATCH`: the admitted reference `source_custody.sha256` does not match.
- `BODY_GEOMETRY_MISMATCH`: the admitted body `input_pins` lacks this call's monotone source.

So admitted registered-geometry outputs cannot be reused at another D (t09). The saved chain passes these checks at 4.04.

## 3. Bitwise identity at 4.04 Mpc / 66 deg

| Evidence | Result |
|---|---|
| t01 | `derive_geometry(4.04, 66)` equals the pinned DDO154 profile record, monotone source and binding, bitwise. |
| t04 (simulate CLI) | For all 8 shipped DDO154 specs (REPRO PINNED_FULL, ADMIT_PREFIX, RULE_FULL, EXAMPLE_SPHERE, KMAX C2/C3/C4/R), the entire `DRYRUN_REPORT.json` and `DRYRUN_PLAN.txt` of v003 and v003b are identical apart from `driver_sha256`, after normalizing the report-dir prefix. The NGC refusal is identical too. The v003 author's `compare_dryrun_plans_c2v003.py` agrees: `dryrun_v003b/PLAN_COMPARE_*_V003B_VS_V003.json`, with `other_report_differences = ['/driver_sha256']` for all 8. |
| t05 (run mode, synthetic) | `subprocess.Popen` is replaced by a no-op, so the real `run_stages` writes each `request.json` and nothing executes. Every request, generated input and start/result/finish record matches v003's byte for byte, apart from the outdir prefix, timings, driver path and sha. That holds for 5 specs, and no geometry file is written. |
| t11 | The real prep V007 `prepare_inputs`, on a synthetic 8-node cube, gives bitwise-identical gas columns, stellar positions and masses, and initial gas Fourier, whether `C` points at the pinned directory or at a per-call copy made at 4.04. |

The seed annotation string `'galaxy_m0_forward_c2v003'` is deliberately left unchanged, so non-reused per-call seeds stay byte-identical to v003's.

## 4. Inclination: stopped, not guessed

| | |
|---|---|
| **Item** | Gas source at i ≠ 66 |
| **Status** | COMPUTED item with no existing stage; not a formula |
| **Why** | `extract_source.py` (`934f25d9`, `UNT_DARK_SECTOR…/external_ddo154_v001`) assigns each THINGS moment-0 pixel to an annulus by deprojected radius, `y/cos(i)` with `SETTINGS inclination_deg 66`, before any annular mass or mean exists. A new i reassigns pixels, so no factor on the pinned 18 means/edges can represent it. Applying only the stellar cos(i)/cos64 and the observation sin(i)/sin64 would produce a mixed-plane source, which the calibration input forbids ("Inclination/warp changes require corresponding source deprojection"). |
| **Deciding work** | A reviewed re-extraction stage at i: `extract_source.py` with `inclination_deg = i`, then the profile composition above (×1.36, λ, 18-bin complete prefix), then reducer V002. After that, the existing `derive_geometry` covers the rest. |

The inclination-dependent pieces that do have pinned formulas are already in `derive_geometry`, written with `inc` and verified at 66:
- stellar Σ·cos(i)/cos64;
- binding `physical_inclination_rad = radians(i)`;
- `released_velocity_reference_factor`.

They are gated by `normalize_spec` and by `derive_geometry`, which both refuse i ≠ 66 (t03).

## 5. Untested and out of scope

**Route-A rows are not at the call geometry.**
- Prep reads the 12 query radii at 4.04 Mpc from the calibration input.
- The route-A binding hard-codes `radians(66)/radians(64)`.
- They are diagnostics only. `identity.route_a.route_a_rows_scope` says so, and t11 confirms the query radii are unchanged.
- Route A would fail only if 14.10·D/4.04 kpc < 5.92 kpc, that is D < 1.70 Mpc.

**Numerics are not rescaled with D.** This is declared in `identity.geometry.unchanged_numerics`:
- the kpc-valued seed controls;
- the composite k grid;
- the column solver template.

**FS bracket margin: UNTESTED.**
- At 4.04, nominal FS columns reach 0.9983 × 3.025e8, the top of the template bracket.
- The overridden columns 5–9 and 45–50 start at 1.00045 × 3.025e8, the bottom of the override bracket.
- A ±1.5–1.8 % distance step changes lengths and masses by that order. FS columns near 3.025e8 may therefore fail to bracket at the box edges.
- The deciding test is the FS column failures of the first D-edge call.
- Any repair is a declared `brackets.rule.fs_absolute_overrides` entry, an existing spec field, not a code change.

**Unchanged:** `campaign_c2v001.py` (`71274ceb`), `root_monitor_c2v001.py` (`ba031c23`), every stage script and every pin used at 4.04.
