# INTERFACE_C2_0466_V002: NGC3198 configuration for the route-B driver

Claude2 lane, dispatch 0466. This adds an NGC3198 configuration to `galaxy_m0_forward_c2v002.py`. `c2v001` and its specs are untouched. Nothing ran on project data. The only things executed were `dry-run`, the synthetic tests and one NGC `run`, which stops BLOCKED before any stage starts. No NGC3198 velocity file was opened. The rotmod `.dat` named in the manifest provenance is listed under `sources.not_opened`.

`R` = `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13`.

## 1. Result

- **NGC3198 cannot produce the 43 speeds with existing reviewed code.**
- **Route B is blocked.** No reviewed NGC stage exists after route A (§3).
- **Route A is also blocked.** The reviewed NGC43 worker and binding v001 cannot open any existing checkpoint module (§2).
- **What c2v002 does instead.** It normalizes, pins and seeds an NGC call, then plans the exact route-A command. `run` writes `start`, `inputs`, `result` and `finish` with status `BLOCKED` and `executed_stages: 0`. The reader for the 43-row output and its m≥1 diagnostics is built and tested on synthetic data, ready for when a reviewed successor exists.
- **DDO154 behaviour is unchanged.** All four DDO specs produce a dry-run report identical to the c2v001 one once report-dir paths and the driver sha are normalized (`dryrun/DDO_REGRESSION_C2V001_VS_C2V002_V001.json`). For the sphere example, the generated manifest's sha also differs, because the manifest embeds its own path. `normalize_spec` returns identical output for every c2v001 spec. The only addition on the DDO side is an optional `numerics.k_domain`; leaving it out gives exactly the c2v001 behaviour.

## 2. Route-A blocker (measured on the real modules with a synthetic caller dict)

The NGC worker v001 builds `caller_identity` from `seed`, `code_pins`, `worker` and `boundary_prescription`. The binding adds `composite_full_driver` and the adapter adds `composite_source_binding`. None of the three writes `physical_parameters` or `numerical_controls`. Every checkpoint version (c2v001, c2v002, c2v003) requires both.

| Pairing | Outcome |
|---|---|
| fixedsrc solver `44d9c23c` + c2v003 `069b3935` | `CheckpointError: CALLER_IDENTITY_FIELD_REQUIRED physical_parameters`, from the real `_identity` |
| fixedsrc solver + c2v001 or c2v002 | `FIXED_SOURCE_SELECTION_IDENTITY` is absent, so the solver refuses the supplied fixed source |
| non-fixedsrc solver `c91c5051` | It has no `fixed_source_fourier_J` parameter, but the adapter always passes one |

There is a precedent. `DDO154_STABLE_CACHED_COUPLED_RUN_V001` failed with the same message after 15 s. DDO's fix was the reviewed stable-cached binding v002. NGC binding and worker v001 are clones of the earlier DDO composite v001 (I compared them with `diff`). The DDO route A that the route-B checkpoint came from also used the stable HI facade, stable line v002, HI v003 and the scalar-lapse inverse cache. NGC v001 has none of these.

**What unblocks it:** a reviewed NGC successor of binding/worker v001, built the same way as `ddo_composite_stable_cached_binding_v002`. Until then, launching the planned command would fail at checkpoint open.

## 3. Every DDO-specific hard-coding in the route-B chain, and the NGC equivalent

Line numbers are located from bytes by the dry-run (`route_b_hardcoding` in the report).

| Stage / file:line | DDO hard-coding | NGC equivalent | Status |
|---|---|---|---|
| route_a worker v002:18 | prep V007 (`galaxies['DDO154']`, 12 rows, DDO H2/stars) | NGC prep v001 `c54c7cc9`, which supplies `galaxies['NGC3198']`, the 43-row manifest, HI σ0 11 km/s and Γ 5/3 (prep:113), the H2 model (prep:212-249) and analytic stars. The H2 model is 10 centres plus a constant core plus a matched exponential tail with Rd = 1.806 kpc, at the stellar sech² height (a counted proxy). | SUPPLIED |
| route_a worker v002:15,19,21 | stable binding v002, stable HI/line/cache, c2v003 caller contract, 66/64° | NGC binding v001 `9e9caf83` gives 72/73° and 43 rows, but lacks the contract and the stable modules | BLOCKER |
| driver base seed | DDO seed V002 `694eaaaa` | No NGC seed exists. The driver composes a CANDIDATE (§5). | CANDIDATE |
| reference worker:60,62,67 | `galaxies['DDO154']`, iteration 4 only | none | BLOCKER |
| reference module v003:31 | σ 11 km/s, Γ 5/3, 16 angles | the same adopted values as NGC prep | compatible |
| body v002:20,58,64,85,88 | DDO monotone source, `galaxies['DDO154']`, 72 radii, (72,16,8) | none. NGC has 51 annuli × GL order (204 at order 4), and there is no NGC monotone source. | BLOCKER |
| offset v003:53,98,107-108 | `galaxies['DDO154']`, (72,16,8,10) | none | BLOCKER |
| columns v001/v003/v005 (v005:44,67) | index 0..71, iteration 4 | none | BLOCKER |
| rotation v001/v005 (v005:17,75,91) | DDO monotone source, complete 72 | none | BLOCKER |
| feedback v002/v004 (v004:74-75) | 72×16×32 measure | none | BLOCKER |
| column mean v004:7,31,35 | DDO 12-row binding (4.04 Mpc radii, sin66/sin64), 72 columns | none. No 43-row NGC binding exists. | BLOCKER |
| driver brackets | DDO solver template and FS absolute brackets [1.5125e8, 3.025e8] | none. The NGC enthalpy scale is unknown before an NGC route A exists. | BLOCKER |
| driver entropy | K factor 64/121, selected on DDO | not applicable | n/a |
| driver geometry | 4.04 Mpc / 66° (released 64°) | profile geometry 13.8 Mpc / 72° (face-on factor 1.0) and binding v001 72/73° | SUPPLIED |
| driver output | 12 DDO rows | 43 rows NGC3198-Q01..Q43, route A only | SUPPLIED (reader) |

Only the declared reference values are accepted: distance 13.8 Mpc and inclination 72°. Other values are refused, because no reviewed code rescales the source radii or re-projects.

## 4. k-domain (call-spec numeric `numerics.k_domain.length_kpc`)

- **Check (refusable):** the smallest positive axis node k_min must satisfy k_min ≤ 2π/L. It is required for NGC. For DDO it is optional, and leaving it out keeps the c2v001 behaviour.
- **The default DDO grid already passes.** That grid is `DIRECT_LAPSE_PANELS72_V001`: 12 panels of order 6, breaks 0, ±0.01, ±0.03, ±0.1, ±0.3, ±1 and ±2 per kpc. Its smallest node is k_min = 3.38e-4 /kpc (2π/k_min = 18,600 kpc).

| L | Required k_min (2π/L) | Covered |
|---|---|---|
| 44.08 kpc (queries) | 0.1425 /kpc | yes |
| 100 kpc (spec) | 0.0628 /kpc | yes |
| 136.48 kpc (HI support) | 0.0460 /kpc | yes |

So the panel spec needed for k_min is the existing default, and no new grid is required for k_min coverage.

- **What does differ (DIAGNOSTIC, no threshold):** the phase of exp(ikL) carried per Gauss node on the outer panels. On [1, 2]/kpc it is:

| Extent | Phase per node |
|---|---|
| DDO HI support, 14.1 kpc | 2.35 rad |
| NGC queries, 44.08 kpc | 7.35 rad |
| NGC HI support, 136.5 kpc (gas columns reach it) | 22.75 rad |

- **Status: UNTESTED.** NGC prep v001 caps the grid at 80 nodes per axis, so at kmax = 2/kpc the per-node phase can drop by at most about 10%.
- **Deciding test:** once route A is unblocked, run NGC route A on the default 72-node grid and on an 80-node redistribution with the same kmax, then compare the 43 rows.

## 5. Seed call spec: `specs/CALL_NGC3198_SEED_C2V002.json`

- **Physical point.** The current DDO seed V002 values, with s = 1, 13.8 Mpc and 72°:
  - Eref = 1.4642919592009638e58 J
  - ℓ_F = 9.905025036587288e19 m
  - γ = 2.9410488940677744e41
- **Grid and k-domain.** The grid is `null`, which means the DDO default grid. k_domain L = 100 kpc. Truncation is cube.
- **H2 tolerance.** `h2_tail_mass_rtol = 1e-12` is DECLARED. The reviewed worker requires an explicit value and no reviewed value exists. It controls arithmetic mass matching only; the tail is normalized to its exact mass, so the error is at rounding level.
- **Candidate worker seed** (`seed_ngc_c2v002.json`, sha `ff0d70b4…` in the dry-run):
  - It keeps every DDO V002 numerical control unchanged. These were selected on DDO and are not reviewed for NGC; for example `hi_search_limit_kpc` is 32 and `pressure_step_kpc` is 0.005.
  - It adds `h2_tail_mass_rtol`.
  - It differs from DDO V002's `numerical_inputs` only in that key.
  - Its key set equals the NGC prep v001 signature exactly. This is checked from bytes.
  - Its seed `pins` are the manifest, profile, tail reduction, H2 source and DDO seed V002.
  - It is `NOT_ROOT_SELECTED`; Claude2 owns that selection.
- **Planned command.** The dry-run prints it: NGC worker, fixedsrc solver and c2v003, all pinned; start iteration 0; fresh outdir and checkpoint.
- **Cost estimate (NOT MEASURED):** about 1.3–1.5 h serial. This scales DDO's measured 1594 s for 576 gas columns and 12 queries to up to 1632 columns and 43 queries.

## 6. Output (built, synthetic-tested; for the first real NGC run)

`ngc_read_route_a_result(result.json, finish.json)` returns the following:

- **`rows`.** 43 rows `{id, Rad_text_kpc, speed_km_s}` in manifest order, plus `speeds_km_s`.
- **`valid`.** True only when all of these hold:
  - the worker returned `RETURNED_ACTUAL_RESULT`;
  - the result sha equals the one in `finish.json`;
  - the ids are the manifest ids, in order;
  - every speed is finite;
  - the source fixed point converged;
  - `predictions_available` is set.
- **`m_ge_1_diagnostics`.** These are DIAGNOSTIC_ONLY. Per query:
  - |FFT_m(v)|/|FFT_0(v)| of the circular-trial speed over the observation azimuths;
  - the azimuthal range of v;
  - max |Euler residual| (R, φ, z);
  - max |continuity rate|.

  It also gives the global maximum for each m.

## 7. Files and checks

| Item | Content |
|---|---|
| `galaxy_m0_forward_c2v002.py` | driver |
| `specs/CALL_NGC3198_SEED_C2V002.json` | seed call spec |
| `dryrun/DRYRUN_NGC3198_SEED_V002/` | report, plan and candidate seed |
| `dryrun/DRYRUN_*_V002/` | the 4 DDO dry-runs with c2v002 |
| `dryrun/DDO_REGRESSION_C2V001_VS_C2V002_V001.json` | DDO regression |
| `tests/tests_c2v002.py` | the c2v001 suite run against c2v002, plus 15 NGC checks |
| `test_runs/TEST_RESULTS_C2V002_RUN_V001.json` | 50/50 pass |
| `superseded/` | pre-final NGC dry-runs |

Dry-run checks:

- 25 static pins and 25 transitively pinned files verify.
- The 16 modules that prep v001 loads by path are hashed from bytes.
- No file imports scipy.
- Both reviews are `PASS_SCOPED_CONDITIONAL_SOLVER` with no blocking corrections, and their pins match.
- The worker's `LOCAL` table equals the configuration.

Hashes are in `HASHES_C2V002.txt`, computed from bytes.
