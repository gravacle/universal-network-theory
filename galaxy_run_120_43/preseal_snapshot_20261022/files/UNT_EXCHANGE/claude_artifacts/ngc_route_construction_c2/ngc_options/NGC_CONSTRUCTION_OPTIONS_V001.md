# NGC_CONSTRUCTION_OPTIONS_V001: decision memo for Claude2 on the open NGC3198 route-A/route-B fields

Claude2 lane, `ngc_route_construction_c2/ngc_options/`. This memo recommends. It decides nothing. Claude2 decides.

**What was run.** One script, `ngc_options_facts_v001.py` (sha `9e65bd0f…97af`), wrote `NGC_OPTIONS_FACTS_V001.json` (sha `8ba60ee7…188e`). It is numpy only, single thread, run with `-I -B`. It verifies every input pin from bytes. It calls three reviewed pure functions in memory on real source data or on synthetic columns:
- the monotone reducer V002 `reduce_source`;
- the annular Bernstein kernel v001;
- the column-mean adapter v002 with the observation module v001.

Nothing was written outside this folder. There was no project launch. The only NGC file opened with radii is the target-free manifest. No NGC3198 velocity file was opened.

**Labels.**
- `FORMAL`: follows from code or algebra.
- `TESTED-POSITIVE` / `TESTED-NEGATIVE`: measured in the facts script, or in a cited run.
- `UNTESTED`: open, with its deciding test named.
- `ROOT DECISION NEEDED`: no reviewed value exists, so a choice must be made from the options listed.

**Abbreviations.** `R` = `…/FIRST_CONSTRUCTION_REVIEW_2026-10-13`. `map` = `route_b_stages_general_c2/map/HARDCODING_MAP_V001.md`. `0473` = `absorb_c2_0473/ngc_route_a/NGC_ROUTE_A_V002_REVIEW_V001.md`. File keys such as `body`, `reference`, `ngc_prep`, `cm_adapter` and `driver` follow `map` §3, with the same shas.

## 0. Recommendations at a glance

| # | Item | Recommended (Claude2 decides) | Decision class | Counted assumption? | Cost driver |
|---|---|---|---|---|---|
| S1 | NGC column count | 39 nonzero annuli × GL order, using the skip-zero roster (156 at GL4) | FORMAL, no choice | no | – |
| S2 | Body roster rule | The body successor adopts skip-zero and compares against reference radii | guard change, no choice | no | review only |
| **S3** | Q01 (0.32 kpc) and Q02 (0.64 kpc) below the innermost node | **A: uniform `source_gauss_order` = 10**, the smallest uniform order with innermost node ≤ 0.32 kpc. Fallback: **C**, report both rows as invalid and count them as misses | ROOT DECISION NEEDED | yes (numerics, target-free coverage rule) | ×2.5 gas columns, ×6.25 fixed-source rings vs GL4 |
| S4 | Pinned join/reference module/body base literals | Join successor with `n_columns` from inputs. Keep 16 angles, σ0 11 km/s and Γ 5/3 | code successor, no choice | no | review only |
| **S5** | NGC monotone source | **M2: segment-monotone successor of reducer V002** (direction rule, zero-target handling, one isolated-bin exception). Fallback: **M1**, declared substitution by the profile controls | ROOT DECISION NEEDED | yes (source-family member) | < 1 s compute, one review, off the critical path |
| F | HI/(HI+He) ratio | 1/1.36 | same method | no (it cancels) | 0 |
| F | Entropy K factor | 64/121, the same member as DDO | ROOT DECISION NEEDED | already counted for DDO; shared, not new | 0 |
| F | FS bracket | [h0/2, 1.05·h0], same derivation as DDO plus DDO's recorded 5 % extension | same method + 1 numeric | numerics | ≈ 0 |
| F | Solver template | Map from the NGC seed HI controls the same way DDO's was; search limit = NGC `hi_search_limit_kpc` | same method | numerics transfer | more vertical samples in outer columns |
| D | Domain and k-grid | Full 136.5 kpc support. nk = 80 (G80D, with G80C as deciding comparison). `k_domain.length_kpc` = 272.97 | ROOT DECISION NEEDED | numerics | ×1.37 transform vs G72 |
| A | Route-A seed numerics | The 0473 proposals plus: GL order per S3, `max_iterations` 16, other tolerances carried | ROOT DECISION NEEDED | numerics transfer group | see §3 |

Section 2 covers the remaining `NONE_IN_REVIEWED_CODE` fields. They are per-call custody values or galaxy-agnostic numerics, and none of them is a choice.

## 1. Structural findings S1-S5

### S1. 156 columns, not 204: FORMAL, no choice

- **The roster rule.** It skips nodes where Σ = 0: `ngc_prep:176`, `reference:85`.
- **The zero annuli.** NGC has 12 zero-mean annuli out of 51, at indices [25, 27-29, 32-34, 38, 44, 45, 48, 49].
- **Why 204 is not admissible.** `join:13` refuses Σ ≤ 0, and `cm_adapter:49` refuses any column with zero intensity (`MISSING_EMISSION_IN_SUPPLIED_COLUMN`).
- **The count.** `n_columns` = 39 × GL order. That gives 156 at GL4 and 390 at GL10 (facts T1). The count is fixed by the S3 decision.

### S2. Body roster: guard change, no choice

- **The mismatch.** `body:61-64` builds R over all annuli and requires R == reference `radii_m`.
- **What the successor needs.** It loops with the same Σ == 0 skip as `reference:85`, using the profile controls. Route A built the roster from the profile, not from the monotone source. It keeps the equality guard.
- **What else to replace.** The `leggauss(4)` and `len(R) != 72` literals (body:60-61, 64) become the config fields.

### S3. Q01/Q02 below route-B radial support: ROOT DECISION NEEDED

**Facts.**
- **Coupling (FORMAL).** The route-B radial nodes are the route-A roster.
  - `reference:78-89` rebuilds the roster from `ni['source_gauss_order']`.
  - It requires the roster digest to equal the checkpoint's `inputs_sha256.gas_columns`.
  - `body:64` requires the same radii.
  - So any node-based fix must be made in the route-A seed, before route A runs. The order is part of the checkpoint identity, so it cannot be changed on resume.
- **Annulus widths.** NGC annuli are 2.676 kpc wide in R; DDO's are 0.783 kpc (facts T5).
- **GL4 node spacing.** The NGC innermost GL4 node is at 0.7052 kpc. The largest node gap below 7.06 kpc is 0.868 kpc, against a query spacing of 0.32 kpc. DDO GL4: gap 0.266 kpc, query spacing 0.49 kpc.
- **What the reviewed adapter does (TESTED, facts T3/T4).** On the real adapter with synthetic columns at GL4:
  - with all 43 rows: `ValueError: QUERY_OUTSIDE_SUPPLIED_RADIAL_SUPPORT: NGC3198-Q01`;
  - with the 41 in-support rows: it returns 41 rows;
  - at GL10, with all 43 rows: it returns 43 rows. Q01 is supported by nodes 0.3057 and 0.6951 kpc.

**Smallest node by uniform GL order** (facts T1; NGC; columns per azimuth; fixed-source rings are stellar + H2, which use the same `gauss`, `ngc_prep:187-249`):

| Order | Innermost node (kpc) | Covers Q02 | Covers Q01 | Columns per azimuth | Route-A columns at n_az = 32 | Fixed rings vs GL4 | Largest node gap < 7.06 kpc |
|---|---|---|---|---|---|---|---|
| 4 | 0.7052 | no | no | 156 | 4992 | 1.00 | 0.868 |
| 5 | 0.5796 | yes | no | 195 | 6240 | 1.56 | 0.750 |
| 8 | 0.3771 | yes | no | 312 | 9984 | 4.00 | 0.491 |
| **10** | **0.3057** | yes | **yes** | 390 | 12480 | 6.25 | 0.398 |
| 12 | 0.2570 | yes | yes | 468 | 14976 | 9.00 | 0.335 |

All of these are under the checkpoint limit of 100000 columns (`c2v003:474-475`).

**Options.**

| Option | What | Consequences | Cost | Counted |
|---|---|---|---|---|
| **A** | Uniform `source_gauss_order` = 10. This is within the reviewed method: `ngc_prep:51-55,162-179` takes the order as an explicit integer with no default, and `reference:78` reads it. | All 43 rows are calculable with no extrapolation. Inner radial resolution improves 2.2× (gap 0.868 → 0.398 kpc). Stellar and H2 quadrature also refine. Route A and route B both carry 390 radial columns. | Route A, indicative: column and transform phases ×2.5 vs GL4. 0473's 0.56 h/iteration estimate (nk 80, n_az 32) becomes about 1.4 h/iteration. The one-time fixed-source transform is ×6.25. Route-B per-column stages are ×2.5 vs GL4 (×5.4 vs DDO) (§5). | Yes. The radial GL order is a numerics choice, selected by a target-free geometric rule: the smallest order whose innermost node is ≤ the smallest query radius. |
| B | Uniform order 5, which covers Q02 only. Combine it with C for Q01. | 42 rows calculable, 1 invalid. | ×1.25 columns, ×1.56 rings | Yes |
| **C** | Keep the order; report Q01 and Q02 as `INVALID_OUTSIDE_RADIAL_SUPPORT`. The NGC binding passes only the 41 in-support rows to the unchanged adapter, and the stage emits the 2 rows as invalid. | 2/43 rows are permanently missing for this construction. Any score counts them as misses. Inner resolution stays coarse (0.868 kpc gaps against 0.32 kpc queries). | 0 compute. A stage/binding wrapper is needed, but no adapter change. | No new physics. It is a scoring consequence. |
| D | GL10 in annulus 0 only (162 columns per azimuth). | Same coverage as A. This is not the reviewed rule. It needs successors of ngc_prep (roster), the reference worker (roster reproduction) and body, each with a review. | +4 % compute. Review sits on the route-A critical path, because prep must change first. | Yes (new roster rule) |
| E | Adapter regularity anchor: interpolate between v(0) = 0 and the first node. | This is a new observation rule. It bridges linearly over 0 → 0.705 kpc across the rising inner curve, and the estimator bias is untested. | Adapter successor plus review | Yes (physical assumption) |
| F | Take Q01 and Q02 from route A (`prediction v005` evaluates at query radii). | Mixes two different observables in one 43-row vector. | 0 | Yes (hybrid estimator) |

**Recommendation: A**, with C as the fallback if route-A time at 2.5× is not acceptable. Reasons:
- A stays inside reviewed code.
- Its selection rule is geometric and target-free.
- It also fixes the coarse inner sampling that comes from NGC's 3.4× wider annuli.
- It must be fixed before route A starts.

Cost scales with order × n_az, so S3 and the `source_azimuth_count` choice (§3) should be decided together.

D is cheaper in compute but puts new reviewed code in front of route A. E and F introduce new observation semantics.

### S4. Pinned dependency literals: code successor, no choice

- **`join` v001.** It hard-codes 72 (join:11,26) and refuses Σ ≤ 0 (join:13). A join successor takes `n_columns` from its inputs and keeps `n_phi` == 16 (join:14) and the Σ guard.
- **`reference_module` v003 and `body_base` v003.** They hard-code 16 angles, σ0 11 km/s and Γ 5/3. NGC prep uses the same σ0 and Γ (`ngc_prep:113`), so they stay as they are (§2, `mesh.n_phi`).
- **Pins.** Every stage PINS entry that names `join` changes to the successor's sha. The rotation stage is the one affected.

### S5. NGC monotone source: ROOT DECISION NEEDED

**How DDO got it.**
- **The reducer.** The reviewed reducer V002 (`HR/ddo_monotone_bernstein_source_controls_v002.py`, sha `50edaba7…`; reviews `DDO_MONOTONE_BERNSTEIN_QP_V001_REVIEW_V001` and `MONOTONE_SOURCE_V002_FROZEN_MIDPLANE_REVIEW_V001` `a1680b6d`, both PASS_SCOPED) was run by `CODEX1/ddo154_monotone_source_reconstruction_monitor_v001.py:4` with `--max-sweeps 200000 --kkt-tolerance 1e-10` on `galaxies.DDO154.HI_plus_He`. The record key is hard-coded at reducer:117.
- **What it solves.** A Hildreth QP: minimise ½Σ((d_i−t_i)/t_i)² subject to d_i ≥ b_i ≥ d_{i+1} ≥ 0, with b_i = 3m_i − d_i − d_{i+1}. Targets are the adjacent mean at the endpoints and the neighbour average in the interior (reducer:3-6, 35, 43-46). The observed means are exact.
- **Why DDO used it.** The profile's own controls follow the rule "d_ends = m_ends, d_internal = min(adjacent means)" (profile `root_choices`). That rule puts a hump in every bin. The facts measure it on DDO at GL4:
  - **Rising nodes:** 36/72 GL4 nodes have dΣ/ds > 0 under the profile controls, and 0/72 under the monotone controls.
  - **Negative midplane Ω²:** the frozen-field midplane diagnostic (`CODEX1/DDO154_MONOTONE_FROZEN_MIDPLANE_RUN_V001/result.json`, sha `7c5fdd1c…`) found 10 such nodes under the old controls, at 39, 43, 47, 51, 55, 59, 62, 63, 66 and 67. The first six recur every 4 nodes, the same position within each annulus. Under the monotone source there are 3 (63, 64, 65).
- **Where route B uses it.** Body Σ (`body:66`, kernel v002) and rotation Σ_R (`rotation:79-82`). Route A uses the profile controls (`ngc_prep:105-118`, `reference:67-77`).

**What happens for NGC.**
- **Refused (TESTED-NEGATIVE, facts T2).** In-memory `reduce_source` on `galaxies.NGC3198.HI_plus_He` raises `ValueError: This branch requires positive nonincreasing actual means` (reducer:31-32). The same harness reproduces the saved DDO controls bitwise.
- **Empty family (FORMAL).** A nonincreasing Σ(s) has nonincreasing bin means. NGC means rise over bins 0→3 (4.87, 6.06, 6.68, 6.71 M☉/pc²). So the V002 family is empty for NGC, regardless of the guard.
- **Other features of the NGC means.** There are 12 exact zeros, and there are rising steps at bins 22, 25, 29, 34, 35, 38, 39, 41, 45 and 49 (facts T2).
- **Profile humps.** The NGC profile controls give 78/156 GL4 nodes with dΣ/ds > 0. Inside 44.08 kpc the count is 34/66.

**Options.**

| Option | What | Consequences | Cost | Counted |
|---|---|---|---|---|
| M0 | Run V002 unchanged | Refuses (TESTED). The family is empty (FORMAL). | – | – |
| **M1** | Declared substitution: body and rotation read the profile record (the profile controls) | Route B uses the same Σ that route A's roster used. This is an existing admitted source member, and the profile says "Full admitted controls retained as source sensitivity". It keeps the per-bin hump, which DDO removed: 34/66 rising nodes inside the query range. DDO's measured link from humps to negative Ω² (10 → 3) makes a column-mean refusal (`column_mean:32`, any ω ≤ 0 refuses all rows) a real risk. That risk is UNTESTED for NGC. It also departs from DDO's route-B member, which is a cross-galaxy asymmetry. | 0 code beyond the generalized stages | Yes (substitution, plus the asymmetry) |
| **M2** | Successor reducer V003, segment-monotone. Same objective, targets and Hildreth method. Per bin, it imposes monotone in a declared direction: d_i ≥ b_i ≥ d_{i+1} if the bin's boundary targets fall, and d_i ≤ b_i ≤ d_{i+1} if they rise. It needs four additions: (i) zero-target handling, because zero-mean bins force their controls to 0, and t = 0 breaks the current scaling at reducer:36-42; (ii) the galaxy key as an argument; (iii) an exception for **bin 26**, a single nonzero bin between zero bins 25 and 27. C0, nonnegativity and the exact mean force a hump there (FORMAL), at R 69.6-72.3 kpc, outside the queries, with negligible mass; (iv) the inner peak placed at the edge between bins 2 and 3 (8.03 kpc). There, the boundary targets rise through bin 2 (6.37 → 6.70) and fall through bin 3 (6.70 → 6.48), and the peak is feasible because d_3 ≥ 6.7147 = m_3. | It keeps DDO's purpose (no within-bin humps) for non-monotone means. Route B uses a different Σ shape from route A, exactly as in DDO (body status `OLD_FIELD_NEW_NORMALIZED_SOURCE`). | One small module, one distinct review, < 1 s to run. It is **off the critical path**: only body and rotation consume it, after route A converges. | Yes (new counted source-family member, as binding V003 / `DDO_FIXED_K0_SOURCE_PROVENANCE_V002` require for any reconstruction change) |
| M3 | Closest-target nonnegative QP without monotonicity | Does not remove humps. It gives no benefit over M1. | as M2 | yes |

**Recommendation: M2**, with M1 as the fallback if M2 fails review.
- **Why M2.** It is DDO's method generalized in exactly the dimension NGC breaks. It leaves the observed means and mass unchanged. Its cost is hidden behind the route-A runtime.
- **Deciding test, M1 vs M2 (UNTESTED).** After the NGC reference run, count nonpositive Ω² nodes in the first FS rotation under each source. Run a frozen-midplane diagnostic analogous to DDO's for each. These take seconds.

## 2. Field-by-field: the other `NONE_IN_REVIEWED_CODE` fields

### 2.1 Per-call custody and run outcomes: no options; produced by the NGC runs

| Field | DDO value and how obtained | NGC rule |
|---|---|---|
| `custody.seed_sha256` | `694eaaaa…`. The sha of the root-selected seed V002 bytes (reference:22). | The sha of the root-selected NGC seed. Candidate `ff0d70b4…` is `NOT_ROOT_SELECTED` and carries the DDO numerics, so a new seed V003 should be composed from the §3 choices, with its sha taken from bytes. |
| `custody.checkpoint_identity_sha256` | `98816902…`, from the route-A checkpoint `IDENTITY.json` (reference:23,55-57). | Read from the NGC route-A checkpoint. |
| `custody.offset_finish_sha256` | `8e1d7060…`, from the offset run's `finish.json` (columns:14). | Read from the NGC offset run. |
| `custody.reference_run` | Directory plus start/finish shas (body:19-22). | Read from the NGC reference run. |
| `custody.body_worker_sha256` | `271e5612…` = body v002 bytes (offset:19). | The sha of the generalized body successor's bytes. |
| `custody.column_mean_input_pins` | The binding plus the rotation/columns run start/finish (column_mean:7). | The NGC binding (§2.3) plus the NGC run files. The driver already patches these per call (driver:1148), but always with the DDO binding (driver:91). That literal must become the config field. |
| `route_a.accepted_iteration` | 4: `iteration_0004`, with `COMPLETED.json` `converged: true` (reference:60-63; driver:719,725). | The NGC iteration whose `COMPLETED.json` has `converged` true. Every custody guard is kept. If NGC never converges, it has no value and route B does not start. |

### 2.2 Mesh and column numerics: galaxy-agnostic; keep the DDO values

| Field | DDO | Options | Recommended | Why | Counted |
|---|---|---|---|---|---|
| `mesh.n_phi` | 16. Inline in body:81 and columns:75,84,94,96; also in reference_module:31, body_base:35 and join:14,26,28 | 16; or another value, which needs successors of reference module v003, body base v003 and join | **16** | It is the only value compatible with the reviewed reference module, which produces the saved 16-angle rows. It is independent of route-A `source_azimuth_count`. | no (the same numerics as DDO) |
| `mesh.eta_order` | 8 (body:65 `leggauss(8)`) | 8; or higher (body cost ∝ eta) | **8** | The body vertical GL is affine between the saved roots, so the order is relative to column height. | no |
| `column.n_z` | 32 = 2 × template `quadrature_order` 16 (column_module:16,48) | 32 (16 per side); or higher | **32** | Polytropic column density is smooth on each side. Taller NGC columns are mapped by the same affine panels. UNTESTED for NGC: if the le-pass `mass_relative_residual` histories show quadrature-limited residuals, 2×24 is the next step. | numerics transfer (1 item, grouped with the template) |

### 2.3 Observation binding (new NGC JSON, ROOT DECISION NEEDED on texts)

DDO's binding (`CODEX1/DDO154_COLUMN_MEAN_REFERENCE_BINDING_V001.json`, `f42c7c65…`, `ROOT_SELECTED_CONDITIONAL_PREPARATION_OBSERVABLE_NOT_CALIBRATION`) is a root-composed JSON. Its fields are below, with how NGC gets each one.

| Field | DDO value and method | NGC value and source | Status |
|---|---|---|---|
| `query_rows` | 12 rows. radius_m = Rad × kpc_m (0.49 kpc → 1.51198e19 m) | 43 manifest rows; radius_m = float(Rad_text) × kpc_m, the same rule as `ngc_prep:65-66`. S3 decides whether 43 or 41 go to the adapter. | supplied (manifest `a2936517`) |
| `distance_Mpc` | 4.04 (profile registration) | 13.8 (profile `NGC3198.geometry`) | supplied |
| `physical_inclination_rad` / `released_inclination_rad` | radians(66) / radians(64) | radians(72) / radians(73), from `ngc_binding:79` | supplied |
| `HI_to_HI_plus_He_mass_ratio` | 1/1.36 = 0.7352941176470588 (the binding value equals 1/1.36 bitwise, facts T6). The tracer rule is "weights_m·ρ/1.36" | **1/1.36** (same method). Profile NGC `helium`: "factor1.36 applied once; NGC input already included it". Main source `settings.helium_factor` 1.36, `rules.helium`. Alternative: 1 (bare HI+He weights). | **Non-load-bearing.** FORMAL: a constant per-column factor cancels in moment/intensity (`cm_adapter:47-50`). TESTED-POSITIVE (synthetic, real adapter): the 41 rows differ by ≤ 2.8e-14 km/s (relative 2.3e-16) for ratios 1/1.36, 1, 0.75 and 0.5. The main source marks 1.36 as SECONDARY (primary verification open), which does not affect the rows. |
| `tracer_rule` | "restricted DDO atomic-gas-only member … weights_m·ρ/1.36 … No H2 or stellar density used …" | Proposed text: "Fixed atomic-H tracer abundance: HI emission weights = solved weights_m·ρ/1.36; helium constant cancels from normalized means. H2 and stars are gravitating fixed sources and are not emission-weighted. Declared optically-thin tracer/coordinate-path reference, not recovered sky-pixel weights." | ROOT DECISION NEEDED (wording) |
| `observation_rule` | "Constant R along each column, zero radial/vertical streaming, no beam; HI-weighted mean of R·Ω, piecewise-linear interpolation onto supplied 12 radii without extrapolation; inclination once …" | The same text with "43 radii". Under S3-C, add "Q01 and Q02 lie below the innermost radial node and are reported INVALID_OUTSIDE_RADIAL_SUPPORT". | counted, shared with DDO (no new assumption) |
| `geometry.registered.HI_original_distance_Mpc` | 4.3 (profile DDO geometry; `radial_distance_scale` 4.04/4.3) | **13.8**. Main source `settings.distance_pc` 13800000.0, and the S2_HALOGAS radial-coordinate text "at 13.8 Mpc", which means no rescaling. Alternative: omit, since no stage reads it (driver registered geometry only). | supplied from data; no effect on numerics |

### 2.4 Brackets, entropy and driver arguments

**`brackets.fs_nominal_absolute_bracket_m2_s2`** (DDO [1.5125e8, 3.025e8]).

- **How DDO got it.** `CODEX1/DDO154_OUTER_FREE_SURFACE_CONTROLS_V001.json` `selection` says: "one-half through original nominal gamma sigma^2/(gamma-1), sigma 11 km/s". Facts T6 confirms bitwise that lo = h0/2 and hi = h0, with h0 = Γσ0²/(Γ−1) = 3.025e8.
- **DDO's correction.** `…FREE_SURFACE_BRACKET_CORRECTION_CONTROLS_V001.json` moved 11 columns to [h0, 1.05·h0], equal bitwise to 3.17625e8. The reason recorded: "mass deficits at prior upper H: 0.09 … 4.46 percent".
- **NGC.** σ0 and Γ are identical (`ngc_prep:113`), so the same method gives the same numbers. The value is derived, not transferred.
- **Options.**
  - (i) [h0/2, h0], with failures recorded and manual corrections, as in DDO;
  - (ii) **[h0/2, 1.05·h0]**, a single declared bracket;
  - (iii) [h0/2, h0] with an automatic retry on [h0, 1.05·h0], which needs a driver change.
- **Recommendation: (ii).**
  - It folds DDO's recorded correction into the nominal rule, so there are no ad-hoc per-index corrections.
  - The cost is negligible: the width grows 1.1×, about +0.14 bisection steps (`column_module:57-67`).
  - If the column mass is monotone in H, the root is bracket-independent. That holds for the connected branch, but it is UNTESTED for NGC.
  - **Caveat.** A higher upper H makes columns taller. At outer columns the upper evaluation may hit the search limit (`NO_TWO_SAMPLED_FREE_SURFACES`, column_module:36), which is tied to the template search limit below.

**`brackets.solver_template`.**
- **How DDO's maps from seed V002 (facts T6, all bitwise).**
  - `search_step` = `hi_search_step_kpc` (0.2) × kpc_m.
  - `search_limit` = `hi_search_limit_kpc` (32) × kpc_m.
  - `root_tolerance` = `hi_root_tolerance_kpc` (1e-8) × kpc_m.
  - `enthalpy_root_tolerance` = c² × `hi_log_lapse_tolerance` (1e-13).
  - `quadrature_order` 16, `mass_rtol` 1e-8, `max_mass_iterations` 64 and `max_potential_calls` 20000 are DDO-selected.
- **Options.**
  - (i) **The same mapping from the NGC seed**, so `search_limit` = NGC `hi_search_limit_kpc` (0473 proposes 95);
  - (ii) the DDO template verbatim (32 kpc).
- **Recommendation: (i).**
  - DDO's outermost column already failed at 1.2·H with "no surface in 32 kpc" (`…REFRESHED_OUTER_BRACKET_CORRECTION_CONTROLS_V001.json`).
  - 36 % of NGC columns lie beyond 66.9 kpc.
  - At 95 kpc and 0.2 kpc per step, the cached samples are at most about 950 per side, plus bisection points. That fits in 20000 calls.
- **Counted.** The DDO-selected quadrature and budget values are one numerics transfer.

**`brackets.rule_factors`** (rfs [0.8, 1.2], le_first [0.4, 0.9], le_next [0.8, 1.1]; driver:154-155; `rule_brackets` at driver:750-756).
- **How DDO got them.**
  - LE1 selection text: "0.4..0.9 of preceding 11-reference columns".
  - RFS index 71: "Former upper 1.2H has no surface in 32 kpc … choose numerical upper 1.01H".
- **The entropy coupling (FORMAL).** le_first [0.4, 0.9] brackets the α = 0.529 entropy jump. It is only consistent with K factor 64/121. A factor of 1 would need new le_first factors.
- **Recommendation.** Keep the same factors. Pre-declare the DDO fallback form: upper factor → 1.01 for a column whose upper evaluation has no surface within the search limit. This needs a declared `rfs_factor_overrides`/`le_factor_overrides` entry, or a driver retry.
- **Counted.** Yes, as one numerics transfer.

**`brackets.repro_overrides`.** Not applicable; set to `{}`. The DDO entries are indices of DDO's saved chain.

**`entropy.K_factor`** (DDO 64/121 = (8/11)², bitwise, facts T6; driver:97).
- **How DDO got it.** `CODEX1/DDO154_LOWER_ENTROPY_PREPARATION_CHOICE_V001.json` (`7da90782…`) records status `ADOPTED_SEPARATE_SENSITIVITY_MEMBER_NOT_VALIDATED`.
  - **Cause:** 28 nonpositive nodes in the refreshed FS rotation at the original K (finish `25484f7e…`).
  - **Authority:** the σ0 sensitivities [8, 14] km/s in `GALAXY_PHYSICAL_SOURCE_STATE_BINDING_V003.json`.
- **Options.**
  - (i) **64/121**, the same member as DDO (8 km/s at the original reference density);
  - (ii) 1.0, the 11 km/s reference;
  - (iii) 196/121, the 14 km/s sensitivity;
  - (iv) per-galaxy selection of the largest factor with all Ω² > 0. This is target-free, but it is a galaxy-tuned value.
- **Recommendation: (i).**
  - Both galaxies stay in one preparation member, so no NGC-specific choice is added.
  - It is the only factor for which the reviewed le_first factors are designed.
- **Deciding test.** Whether NGC has all Ω² > 0 at 64/121 is UNTESTED. The le rotation `positive_rotation_square` flag (driver pass record) decides it, and `column_mean:32` refuses otherwise. In that case, record a TESTED-NEGATIVE for this member; do not tune.

**`driver.fixed_args`** (wave_batch 256, position_batch 512, bessel_cache_entries 500000, mass_relative_tolerance 1.1e-8; driver:81-82).
- Keep them.
- The batches and the cache are resource controls. With about 2× (GL4) to 5× (GL10) more positions, a cache of 500000 lowers the hit rate. That costs time only.
- `mass_relative_tolerance` is a reviewed tolerance.

## 3. NGC route-A seed numerics

These come from 0473 §3; Claude4's N2 findings are incorporated there. The values must all be fixed before route A starts, because the checkpoint identity contains `numerical_controls`: the 33 seed keys, as 0473 decoded them. A change on resume gives `IDENTITY_MISMATCH`, which was TESTED for `pressure_step_kpc` and `Eref`.

| Numeric | DDO value and method | Options | Recommended | Status / deciding test |
|---|---|---|---|---|
| `source_gauss_order` | 4. Carried in the DDO seed lineage. Seed V002's `quadrature_selection_evidence` covers the lapse/grid only, with no radial-GL rationale. | 4 / 5 / 10 / 12 (§S3) | **10** (S3-A), or 4 with S3-C | FORMAL coverage. Cost in S3 table. |
| `source_azimuth_count` / `observation_azimuth_count` | 8 / 8 | 0473: 8, 32, 88, 272 / 12 | **32 / 12** (0473) | UNTESTED. Deciding test: n_src 32 vs 64 at iteration 0. With GL10, columns = 12480. |
| `hi_search_limit_kpc` | 32 | 32 / 95 (largest symmetric limit within 1024 calls at 0.2 kpc) | **95** (0473) | UNTESTED. Iteration 0 shows the first `FREE_BOUNDARY_NOT_BRACKETED`. |
| `composite_grid_spec` / `fourier_points_per_axis` | G72 (`DIRECT_LAPSE_PANELS72_V001`) | G72 / G80C / G80D; > 80 needs a prep successor (`ngc_prep:142`) | **G80D, with G80C as the deciding comparison** (0473) | UNTESTED. Compare iteration-0 outer-column roots and gas under the two grids. |
| `pressure_step_kpc` | 0.005 (TESTED on DDO) | 0.005 | **0.005** | The run's own d/d2 check decides it. |
| `azimuth_step_rad` | 0.02 | 0.02 / 0.0025 (matches DDO's kmax·R·da at 44.08 kpc) | **0.0025** (0473) | UNTESTED. Deciding test: the `pressure_phi_stencil_difference` median against DDO's 0.28 %. |
| `h2_tail_mass_rtol` | none (DDO has no H2 tail) | any value ≳ 1e-14 passes identically | **1e-12** | FORMAL + TESTED (0473 N2-E) |
| `max_iterations` | 8. DDO converged at iteration 4 (5 iterations run). | 8 / 16 | **16** | Budget only: a converged run stops early, so the iterates are unchanged. 8 is too small if NGC needs more than 8, and the value cannot be raised on resume. Cost is 0 if NGC converges by 8. |
| `relaxation`, `source_rtol`, `pressure_rtol`, reality/hermitian/solve tolerances, `hi_*` tolerances, `hi_max_metric_calls` 1024, `hi_panels_per_side` 8, `kmax_inverse_kpc` 2, `analytic_initial_azimuth` true | Carried from DDO seed V002 | carry; or re-select | **carry** | Counted as one "DDO numerics transfer" group. Each check fails loudly in the run. |
| Physical point Eref, ℓ_F, γ, s | DDO seed V002 values (call spec) | – | not an NGC field | These are shared calibration constants, outside this memo. |

## 4. Domain 44 kpc vs 136 kpc and k-grid resolution against the 80-node prep cap

**Facts** (from facts T5/T7 and NUMERICS_FACTS_V001):
- **Extents.** Queries reach 44.08 kpc. The HI support reaches 136.48 kpc, so in-plane separations reach 272.97 kpc.
- **Columns beyond the query range.** 56.4 % of columns lie beyond 45.49 kpc, and 35.9 % beyond 66.90 kpc.
- **HI mass beyond the query range.** Only 0.397 % of the HI mass lies beyond 45.49 kpc, and 0.0039 % beyond 66.90 kpc.
- **Outer-panel phase per node** (outer positive panel):

| Grid | at 44.08 kpc | at 136.48 kpc |
|---|---|---|
| G72 | 7.35 rad | 22.7 rad |
| G80C | 2.94 rad | 9.10 rad |
| G80D | 3.57 rad | 11.05 rad |

- **k_min.** k_min ≤ 2π/L holds for L = 44.08, 136.48 and 272.97 kpc on all three grids.
- **Prep cap.** `ngc_prep:142` caps nk at 80.

**Options.**

| Option | What | Consequences | Cost | Counted |
|---|---|---|---|---|
| **K1** | Full support, nk = 80 (G80D), with G80C as the deciding comparison | No source change. Outer columns may be grid-dominated (UNTESTED). | ×1.37 transform vs G72 | numerics |
| K2 | Truncate the HI source at 45.49 or 66.90 kpc | Removes 0.40 % / 0.0039 % of HI mass and 56 % / 36 % of columns. This is the largest cost lever (÷2.3 / ÷1.56 columns). | It changes the reviewed source (the profile record) and the route-A identity | **source change: ROOT DECISION; not recommended under the no-physics-change rule** |
| K3 | Raise the cap: prep successor, nk 96 | 0473/N2-A: no grid of 96 nodes or fewer resolves X ≥ 88 kpc, so it does not fix the outer columns | ×1.73 vs nk 80, plus review | numerics |
| K4 | Lower kmax | Changes the cutoff. G80K15 showed no gain (0473). | – | yes |

**Recommendation: K1.**
- Also set the driver call-spec `numerics.k_domain.length_kpc` = **272.97**, which is 2 × the HI support: the largest separation the check is meant to cover. It passes for G80C and G80D, and costs nothing.
- K2 is reported as a lever, not recommended.

## 5. Cost of 72 vs 156 (and 390) columns

**The code change.** It is the same at any count. Every 72 literal becomes `radial.n_columns`: 21 stage occurrences, plus join and driver:96 (map §3). The join successor is S4. The body roster is S2.

**Measured DDO elapsed times** (receipts hashed in facts T8), with NGC scaled by the column ratio. This is indicative and NOT MEASURED. Transform-type stages get a further ×1.37 if the grid moves to nk 80. Outer columns also carry more vertical samples (95 vs 32 kpc search).

| Stage | DDO measured (s) | NGC GL4 ×2.17 (s) | NGC GL10 ×5.42 (s) |
|---|---|---|---|
| reference | 932 | 2019 | 5048 |
| body | 160 | 347 | 868 |
| offset | 264 | 572 | 1429 |
| FS columns (outer + remaining) | 29 + 540 | 1233 | 3083 |
| FS rotation | 163 | 353 | 883 |
| FS native feedback | 18 | 39 | 98 |
| LE refreshed columns (one pass) | 627 | 1359 | 3397 |
| LE refreshed rotation (one pass) | 165 | 358 | 896 |
| LE native feedback (one pass) | 19 | 42 | 105 |
| column mean | 0.1 | 0.2 | 0.6 |

**Route-B chain** (FS + RFS + 3 LE passes):
- DDO is about 1.4 h serial. The RFS columns pass is not among the hashed receipts, so it is taken as ≈ the FS columns pass.
- NGC is indicatively about 3.1 h (GL4), up to about 4.2 h with ×1.37.
- At GL10 it is about 7.7 h, up to about 10.6 h.

**Route A, before this.** 0473 estimates about 0.56 h per iteration at GL4 / n_az 32 / nk 80. At GL10 that is about 1.4 h per iteration.

**Memory.** The arrays (n, 16, 32) stay small at any count.

**One extra open item (UNTESTED).** The rotation stage builds d ln K/dR with a spline over all radial nodes (`rotation:83`). NGC's 12 zero-mass annuli leave node gaps between 66.9 and 133.8 kpc, so the spline bridges them. Deciding test: compare the spline derivative at nodes adjacent to the gaps against a one-sided finite difference in the first NGC rotation run.

## 6. Counted assumptions that the recommended set adds for NGC

1. **Radial GL order 10.** A numerics choice made by the target-free coverage rule (S3-A). Under S3-C, add instead "2 rows invalid, scored as misses".
2. **Segment-monotone source member V003** (S5-M2). This is a new source-family member, with the bin-26 hump exception.
3. **DDO numerics transfer group.** The solver template's quadrature and budget values, the bracket rule factors with DDO's two fallback forms, n_z 32, η 8, n_φ 16, and the carried route-A tolerances.
4. **Extended FS bracket upper bound** 1.05·h0.
5. **Route-A numerics.** n_src 32 / n_obs 12, G80D, `hi_search_limit` 95, `azimuth_step` 0.0025, `max_iterations` 16, `h2_tail_mass_rtol` 1e-12.
6. **NGC observation-binding texts.** These share DDO's optically-thin, no-beam, constant-R assumptions. Nothing new.

These add nothing: K factor 64/121 (shared with DDO), HI ratio 1/1.36 (cancels), and `HI_original_distance` 13.8 (data).

## 7. Deciding tests (none of them is a launch here; each is a reading of the first NGC runs)

1. **Iteration-0 vertical search.** At route-A iteration 0, find the first `FREE_BOUNDARY_NOT_BRACKETED` (radius and side). This tests `hi_search_limit` and the template search limit.
2. **Grid.** Compare G80C and G80D at iteration 0: outer-column roots and gas at R > 45 kpc.
3. **Azimuths.** Compare n_src 32 and 64: the updated-gas difference at iteration 0.
4. **Source member.** Count nonpositive Ω² in the FS rotation under M2 and under M1.
5. **Entropy member.** Read the le rotation `positive_rotation_square` at K factor 64/121.
6. **Spline across the zero-annulus gaps.** Compare the spline derivative with a one-sided difference at nodes next to the gaps (§5).

## 8. Files (sha256 from bytes)

| File | sha256 |
|---|---|
| `ngc_options_facts_v001.py` | `9e65bd0f4ce537464c483918f932bf96c91364f73bcc42cef20836f3c16297af` |
| `NGC_OPTIONS_FACTS_V001.json` | `8ba60ee7fe1cc25c4e95b8ffa26dffd88548345244c2f2f4ec6797b0eb44188e` |
| `NGC_CONSTRUCTION_OPTIONS_V001.json` and this memo | in `HASHES_NGC_OPTIONS_V001.txt` |

Inputs read, each pinned from bytes:
- the `map` pair: `8874e393…` (md) and `2c05f362…` (json);
- 0473 review `d99c82ed…`;
- the 11 facts-script pins;
- `DDO154_LOWER_ENTROPY_PREPARATION_CHOICE_V001` `7da90782…`;
- `DDO154_OUTER_FREE_SURFACE_CONTROLS_V001` `f9f07c0e…`;
- `…BRACKET_CORRECTION_CONTROLS_V001` `7719e7d8…`;
- `…REFRESHED_OUTER_BRACKET_CORRECTION_CONTROLS_V001` `87eef1fd…`;
- `…LOWER_ENTROPY_FREE_SURFACE_CONTROLS_V001` `c2f8b434…`;
- `…MONOTONE_FROZEN_MIDPLANE_RUN_V001/result.json` `7c5fdd1c…`;
- `GALAXY_PHYSICAL_SOURCE_STATE_BINDING_V003` `7cadac8b…`;
- `NGC3198_MAIN_SOURCE_ANNULAR_INPUT_V001` `84e20bc0…`.
