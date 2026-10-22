# NGC3198 route A at A2F10: free-boundary failure diagnosis (V001)

**Scope.** This diagnoses `NGC3198_ROUTE_A_A2F10_RUN_V001`, which failed in iteration 0.
- The evidence is single-column replays of the pinned HI column solver on the run's own saved iteration-0 operator.
- No route-A run was launched.
- No target or velocity file was read. No `result.json` of a KMAX_, D7R1, V005, V006, V007 or DECIDING run was opened.
- The A2F10 anchor is a target-free feasibility point, not a calibrated point.
- Machine-readable twin: `DIAGNOSIS_V001.json`.

## Headline

**The columns are unconfined. This is not a search-limit artefact.**

- **Column 2503 (R 52.655 kpc, φ 1.374), plus side: no free boundary exists anywhere sampled, up to 1000 kpc.**
  - The lapse rise peaks at 3.205e-9 at z = 30 kpc. That is 0.952 of the escape threshold 3.366e-9.
  - Above that it falls: −5.80e-8 at 95 kpc and −2.13e-7 at 270 kpc.
  - The minus side crosses the threshold at 9.0 kpc.
- **Iteration-0 failing set.** All 2489 unsolved columns were replayed.
  - 1808 fail at 95 kpc.
  - All 1808 still fail at 136.5 kpc with 2048 calls; 0 are rescued.
  - All 1808 are unconfined within 500 kpc on at least one side.
  - Their radii span 52.655–136.301 kpc.
  - Their HI quadrature mass fraction is **2.55e-4**, or 3.55e6 M☉ of 1.391e10 M☉. TESTED-POSITIVE.

## Validation of the replay harness

`tools/replay_lib_v001.py` rebuilds the inputs and callback the run used:

- the metric callback, exactly as in solver c2v001:129-158;
- the iteration-0 prepared operator, from the checkpoint START blobs (the file sha and the array digest are both verified);
- C̄ and μ̄, from the IDENTITY caller record (digests equal the IDENTITY);
- the gas roster, by rebuilding prep v001:104-118 and 164-179.

Checks, from `replay/VALIDATION_V001.json`:

- The roster digest equals the IDENTITY `gas_columns` digest.
- All 2503 completed-column input digests match.
- Columns 0, 1000, 2496 and 2502 re-solve **bitwise equal** to their checkpoint records.
- Column 2503 reproduces the recorded failure message **byte for byte**.

Status: TESTED-POSITIVE.

## 1. The FAILURE record

**Column.** Index 2503 is annulus 19, GL4 node 2, azimuth 7 of 32.

| Field | Value |
|---|---|
| R | 1.6247730102205963e21 m (52.655 kpc) |
| radial weight | 2.6686e19 m |
| φ weight | 2π/32 |
| Σ | 2.1808e-5 kg/m² |

**HI options.** These are the seed values:
- σ0 = 11 km/s
- Γ = 5/3
- step 0.2 kpc, limit 95 kpc
- root tolerance 1e-8 kpc
- log-lapse tolerance 1e-13
- 1024 calls, 8 panels

**What the solver computes.** The module is `hi_two_sided_free_boundary_v002.py`, sha `665b5589`.
- **Log threshold** (hi v002:41): `log1p(h0/c²)`, where h0 = Γσ0²/(Γ−1) = 3.025e8 m²/s². This gives 3.3657664e-9, i.e. (17.4 km/s)²/c².
- **Log residual** (hi v002:61-62): `[ln N(z) − ln N(0)] − threshold`.
  - N = 1 + δn (metric evaluator v002:76).
  - The gas edge is the first sampled z where the residual is ≥ 0. There the polytropic enthalpy u reaches 0 (hi v002:97).
- **Recorded value.** `actual_log_residual` = −6.137e-8. So at z = 95 kpc the lapse is 5.80e-8 **below** its midplane value.

**Which side failed.** The plus side.
- `root(-1)` runs first (hi v002:91). The minus side bracketed at [−9.0, −8.8] kpc.
- The plus side then sampled z = 0.2 … 95 kpc and never reached the threshold.

**Why the search stopped.** The search limit stopped it, not the call budget.
- The loop `while distance<limit` ran out at hi v002:66, and the for-else branch raised at hi v002:76-77.
- The solve used 548 of 1024 calls: 1 midplane, 71 on the minus side and 476 on the plus side (`replay/COLUMN_2503_CALL_ACCOUNTING_V001.json`).
- Solver c2v001:159-179 catches only that column's error, returns `FAILED_SOURCE_PREPARATION` and does not retry.

## 2. Column 2503 with larger limits

The call caps were set so they never bind (`replay/COLUMN_2503_PROFILE_V001.json`).

| limit (kpc) | calls cap | outcome |
|---|---|---|
| 95 | 1067 | NOT_BRACKETED, plus, residual −6.137e-8 |
| 136.5 | 1483 | NOT_BRACKETED, plus, residual −1.1756e-7 |
| 190 | 2017 | NOT_BRACKETED, plus, residual −1.705e-7 |
| 272.97 | 2847 | NOT_BRACKETED, plus, residual −2.158e-7 |
| 500 | 5117 | NOT_BRACKETED, plus, residual −2.328e-7 |

**Log-ratio profile, plus side** (the residual is this minus 3.366e-9):

| z (kpc) | ln N(z) − ln N(0) |
|---|---|
| 1 | −4.9e-10 |
| 5 | −1.6e-9 |
| 10 | −9.5e-10 |
| 20 | +1.73e-9 |
| **30** | **+3.205e-9 (maximum)** |
| 40 | +1.41e-9 |
| 50 | −4.2e-9 |
| 60 | −1.31e-8 |
| 80 | −3.74e-8 |
| 95 | −5.80e-8 |
| 135 | −1.12e-7 |
| 190 | −1.67e-7 |
| 270 | −2.13e-7 |
| 500 | −2.30e-7 |
| 730 | −2.92e-7 |
| 1000 | −1.52e-7 |

**Minus side.** It reaches the threshold at 9.0 kpc. The maximum is 1.91e-8 at 38 kpc. It falls to −3.65e-8 at 95 kpc.

**z-asymmetry.** Within 95 kpc, the odd part of the profile is up to 1.10e-8 (3.3× the threshold).

**Where the metric is defined.** It is defined at every finite z.
- It is a finite sum over the 80 distinct composite-Gauss k_z nodes (line v001:46-53). The cube is the nonperiodic Gauss quadrature of prep v001:120-157.
- **There is no Fourier box and no periodic image.** TESTED: max |lnN(z + 272.97 kpc) − lnN(z)| is 2.33e-7, against max |lnN| of 1.14e-7.
- 272.97 kpc is the k-domain coverage length, used for the k_min check; it equals 2 × the 136.48 kpc HI support. It is not a period.

**Where each panel stops integrating e^{ikz}.** This is a diagnostic, not an error bound. The criterion is the first |z| at which the panel's Gauss rule errs by more than 1e-3 × the panel width. The same heights apply to |x| and |y|.

| panel (1/kpc) | [0,0.01] | [0.01,0.03] | [0.03,0.1] | [0.1,0.3] | [0.3,1] | [1,2] |
|---|---|---|---|---|---|---|
| order | 3 | 3 | 4 | 5 | 10 | 15 |
| height (kpc) | 361.5 | 181 | 89 | 46 | 36.5 | 43 |

## 3. The full iteration-0 failing set

**Roster.** 4992 columns = 156 GL4 radial nodes × 32 azimuths, ordered inner to outer. The completed columns 0–2502 cover R ≤ 52.655 kpc.

**Coverage.** All 2489 unsolved columns were replayed; none were sampled out. Files: `replay/SWEEP_SUMMARY_V001.json` and `replay/sweep/`.

| | at 95 kpc / 1024 calls | at 136.5 kpc / 2048 calls |
|---|---|---|
| OK | 681 | 681 (roots identical, 681/681) |
| NOT_BRACKETED | 1808 (first failing side: minus 1181, plus 627) | 1808 (0 rescued) |

**Unconfined within the profile height.** 1808 columns at every height checked: 95, 136.5, 272.97 and 500 kpc.

**Failing set.**
- R from 52.655 to 136.301 kpc.
- Mass fraction 2.550e-4 (3.55e6 M☉).
- The first failing column is 2503.

**Pattern.** The failures are erratic in φ and in R.
- In ring 2496 (52.66 kpc), 2 of the 25 unsolved columns fail.
- Rings at 69.8, 70.5, 81.2–84.8 and 104.6 kpc fail on all 32 columns.
- Between 94 and 136 kpc, unconfined columns sit next to confined columns with roots of 0.4–4 kpc.
- Confined roots reach 25.70 kpc among the completed columns and 30.48 kpc among the unsolved ones.

Status: TESTED-POSITIVE.

## 4. Physics reading (facts)

**Threshold against the vertical rise.**
- The gas edge needs ln N(z) − ln N(0) = h0/c² = 3.37e-9.
- At R ≥ 52 kpc the replayed rises peak at about 1e-9 to 4e-8. In ring 2496 the barrier is 0.95–12× the threshold; by 55 kpc it is below 0 to 7×.
- Above the peak, the rise turns over. In the six decomposed columns it falls to between −5e-9 and −6e-8 at 95 kpc, and to between −1.7e-7 and −2.2e-7 at 273 kpc.

**k-shell decomposition** (`replay/KSHELL_DECOMPOSITION_V001.json`). δn is split exactly into cube shells; the closure check is |lnN − log1p(δn)| ≤ 1.1e-16.
- **The large-z fall comes from the long-wavelength shells.**
  - The |k| < 0.03/kpc shell is monotone negative in column 2503: −1.0e-8 at 30 kpc, −6.1e-8 at 95 kpc and −2.2e-7 at 273 kpc.
  - The [0.03, 0.1) shell adds −1.8e-8 at 95 kpc.
  - The z-phase of these panels is resolved out to 89–361 kpc. The fall is therefore **not** z-phase aliasing.
- **The barrier is a small difference of larger terms.** In column 2503 the rise up to 30 kpc comes from the [0.1, 0.3) shell (+2.0e-8), offset by the two lowest shells (−1.5e-8). These terms are 3–30× the threshold.
- **The transverse sampling is unresolved at these radii.** At R = 52.66 kpc, the transverse coordinates exceed the panel heights of [0.1, 0.3) (46 kpc), [0.3, 1) (36.5 kpc) and [1, 2) (43 kpc).
  - The high-k shells then change by about 1e-8 between neighbouring azimuths. At z = 30 kpc the [0.3, 1) shell gives +1.06e-8 at φ = 0 (column 2496, root 0.98 kpc) and −2.1e-9 at φ = 0.196 (column 2497, root 12 kpc).
  - Root decision A1-numerics already treats cube-corner m = 4 / m = 8 structure as numerical.

**Classification.** This is **not** a numerics limit. For all 1808 columns, no edge exists above 95 kpc within the domain; the check covered up to 500 kpc for every column and up to 1000 kpc for column 2503. Under the installed iteration-0 operator (A2F10 anchor, G80C grid), these columns are **unconfined within the domain**. Their confinement margin is set by k-shell terms that are larger than the threshold, and some of those terms are beyond the panel resolution criterion.

**Open questions:**

| Claim | Status | Deciding test |
|---|---|---|
| The long-wavelength fall is response physics at the anchor point, not small-k sampling of the response symbol | UNTESTED | Re-prepare the iteration-0 operator with refined panels below 0.1/kpc, then replay column 2503 and ring 2496 with this harness |
| The confinement pattern at R ≥ 46 kpc does not depend on the grid | UNTESTED | The same re-prepare with refined [0.03, 0.3] panels, or G80E14 |
| The failing set is the same in iterations ≥ 1 | UNTESTED | Needs an iteration-1 operator; none exists |

## 5. Options (root decides)

| | (a) raise `hi_search_limit` | (b) truncate the route-A gas roster | (c) a reviewed alternative in code |
|---|---|---|---|
| **Viable?** | **No.** TESTED-NEGATIVE: 0 of 1808 rescued at 136.5 kpc; all unconfined to 500 kpc. A run would fail at column 2503 with NOT_BRACKETED at z = 136.5 kpc, residual −1.1756e-7. | Counted option. Viability UNTESTED until the code exists. | **None exists** (details below). |
| **What changes** | Seed `hi_search_limit_kpc` 136.5 and `hi_max_metric_calls` 2048. Bitwise neutral for bracketed columns (681/681 identical). | Ring rule: keep columns 0–2495 (R ≤ 51.746 kpc); drop 2496 columns. Annulus rule: cut at 50.847 kpc. | — |
| **Constants status** | The limit is a root-decided counted numeric (N4). The call cap and step are carried from the DDO control (seed provenance: "not NGC-reviewed"). hi v002:26-28: the limit is a failure budget, not a cutoff. | Mirrors N2, which cuts route B at 66.904 kpc (3.9e-5). The route-A domain would then sit inside route B's. | — |
| **Cost** | Seed and request (the builder is ready), plus a new NGC route-B solver template and driver pins. v006 `template_mapping_check` (v006:1471-1480) refuses otherwise, because drivers v006, v007 and v008 hard-code template `ba5e87eb` (search_limit 95). | Code change. Prep v001 has no truncation input (164-179); the worker LOCAL pins prep `c54c7cc9`; launcher v001:97-98 refuses masks. Needs prep v002, worker and binding pins, a manifest, a launcher successor and review. About half the columns per iteration. | — |
| **Target-free** | Yes | Yes | — |
| **Queries ≤ 44.08 kpc** | Unchanged, because bracketed columns are bitwise identical. | UNTESTED. The dropped gas (7.0e-4 to 1.09e-3 of HI, 9.7e6 to 1.5e7 M☉) lies outside every query radius, but its field at R ≤ 44 kpc has not been computed. | — |
| **DDO154** | DDO seeds copy their HI controls from DDO seed V002 (driver c2v001:543-570; 32 kpc). A shared rule changes only DDO calls that hit NOT_BRACKETED. | The same rule must apply. It is a no-op at DDO A2F10, where every column bracketed (N2 R5; not re-tested here). Other calibration points are UNTESTED. The rule must also say what happens if a later iteration unconfines a kept column. | — |

**Why (c) is empty:**
- Quadrature v002 does have `declared_noncompact_tracer` with a tail integral (v002:61-66). However, hi v002:113-115 hard-codes `finite_free_boundary`, and an unconfined polytrope has no defined tail. Using it would need a new HI module and review.
- hi v003 is a precision variant. The legacy path's float error is at most 1.1e-16, against residuals of 1e-10 to 1e-7, so it would change nothing (TESTED).
- G80E14 (the N2 proposal) and σ0/Γ are other levers. G80E14 is numerics and its effect on confinement is UNTESTED. σ0 and Γ are adopted physics assumptions; changing them is not a numerics fix.

## 6. Seed v002 (built, dry-run ALL_PASS, NOT launched)

**Tools:**
- builder `seed_v002/tools/build_seed_v002.py` (`3ad23a39`)
- dry run `seed_v002/tools/dryrun_seed_v002.py` (`f760400e`)

**What the builder does.**
- It rebuilds the seed from 478a8467 and the serial request from 9da3461b.
- It builds the PAR N8 and N3 requests by executing the packet's `build_par_files_c2v002.py` from its pinned bytes.
- It re-pins the V002 addendum to its current bytes (`17c26616`), or adds the file given by `--frozen-decisions`.
- It accepts `--hi-search-limit-kpc`, `--hi-max-metric-calls` and `--hi-search-step-kpc`; the defaults are the current values.

**What the dry run does.** It re-runs the packet's own `dryrun_route_a_f10_v001.py` (`d3_child`, `d4_static`) and `dryrun_par_c2v002.py` (`t6_child`), loaded from their pinned bytes, with only their path globals re-pointed.

**DEFAULT variant.** `numerical_inputs` are unchanged.

| File | sha256 |
|---|---|
| `DEFAULT/seed/NGC3198_ROUTE_A_A2F10_SEED_C2V002_DEFAULT.json` | `88ef386d2bd4e14be23709d21b23fd3b7b57a2cc85adcc09d6a0459bcbc108da` |
| `DEFAULT/launcher/NGC3198_ROUTE_A_A2F10_REQUEST_C2V002_DEFAULT.json` (serial → `runs/NGC3198_ROUTE_A_A2F10_RUN_V002`) | `e1e9161711beeab20dc263b987e032fdc44be0b29866e2b49328e4c34dfc6204` |
| `DEFAULT/launcher/NGC3198_ROUTE_A_A2F10_PAR_N8_REQUEST_C2V002.json` (→ `runs/NGC3198_ROUTE_A_A2F10_PAR_RUN_V002`) | `a0597cf85b459b171a4e11b8e4b46c40e9e66fdd53844723c7e9dc77b024636b` |
| `DEFAULT/launcher/NGC3198_ROUTE_A_A2F10_PAR_N3_REQUEST_C2V002.json` | `7b6e559071d7150e792b0b864bc3f195e4728c17415872664dee8958cf8d5f26` |
| `DEFAULT/route_b_spec/CALL_NGC3198_ROUTE_B_A2F10_PAR_TEMPLATE_C2V006.json` | `bfa54e3252f3bee1b61d6653d6e55f2357a9e7c30c43b9083715577c41b4581e` |
| `DEFAULT/dryrun_v002/DRYRUN_REPORT_SEED_V002_DEFAULT.json`: ALL_PASS (S0, D1–D5, P1–P3) | `824c855a6e366b7d9a218c5580d26715fb1d2d3d21d7fc64bf505ce6d9e82add` |

**B1 is resolved.** TESTED-POSITIVE: with the v002 seed, the worker's seed-provenance check ran and passed, and execution reached the binding stub, in both D3 (serial) and P2 (parallel).

**Label caveat.** The P2 `seed_mode` text "REAL seed 478a8467" is a literal label inside the reused module. The bytes actually used were the v002 seed; P1 verified that both PAR requests pin `88ef386d`.

**Prediction if DEFAULT is launched** (UNTESTED): the same failure at column 2503, because the numerical inputs are identical and the replay reproduces the failure bitwise.

**HI136, option (a).** Not written, because (a) is not viable. An in-memory dry build gives seed `b58e60e2…` and request `d9a9c6d2…`.

## Launch commands that would follow each option (none launched)

**DEFAULT, serial.** Predicted to reproduce the column-2503 failure.

```
nohup /Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -I -B /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/galaxy_m0_forward_c2_0466/root_monitor_c2v001.py --driver /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_impl_c2/route_a/launcher/ngc_route_a_launch_c2v001.py --driver-sha256 f5e5e0fe2a9e7529c18f89b315e03d897a87ab88545214520fe0ab1b9e447767 --spec /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_a_freeboundary_c2/seed_v002/DEFAULT/launcher/NGC3198_ROUTE_A_A2F10_REQUEST_C2V002_DEFAULT.json --outdir '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs/NGC3198_ROUTE_A_A2F10_RUN_V002' --receipt '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs/NGC3198_ROUTE_A_A2F10_RUN_V002.receipt.json' --wall-cap-s 21600 --rss-cap-bytes 4294967296 --output-cap-bytes 17179869184 --poll-s 2.0 > '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs/NGC3198_ROUTE_A_A2F10_RUN_V002.monitor.log' 2>&1 &
```

**DEFAULT, parallel N8.** Uses a 12 GiB tree-RSS cap, which is the B3 root declaration.

```
nohup /Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -I -B /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/galaxy_m0_forward_c2_0466/root_monitor_c2v001.py --driver /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_f10_c2/route_a_f10_parallel/launcher/ngc_route_a_launch_c2v002.py --driver-sha256 d814713462275c01b07e4e68c0c611fdc9cbc8a8789dfb92b2cbc6bbbc3c7004 --spec /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_a_freeboundary_c2/seed_v002/DEFAULT/launcher/NGC3198_ROUTE_A_A2F10_PAR_N8_REQUEST_C2V002.json --outdir '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs/NGC3198_ROUTE_A_A2F10_PAR_RUN_V002' --receipt '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs/NGC3198_ROUTE_A_A2F10_PAR_RUN_V002.receipt.json' --wall-cap-s 21600 --rss-cap-bytes 12884901888 --output-cap-bytes 17179869184 --poll-s 2.0 > '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs/NGC3198_ROUTE_A_A2F10_PAR_RUN_V002.monitor.log' 2>&1 &
```

**DEFAULT, parallel N3.** The same command as N8 with two substitutions:
- spec: `…/DEFAULT/launcher/NGC3198_ROUTE_A_A2F10_PAR_N3_REQUEST_C2V002.json`
- `--rss-cap-bytes 4294967296`

**(a) HI136.** Predicted to fail at column 2503 (z = 136.5 kpc), so it is not recommended. The steps would be:

1. Build the files:

   ```
   nice -n 10 <python> -I -B .../seed_v002/tools/build_seed_v002.py --variant HI136 --serial-run NGC3198_ROUTE_A_A2F10_HI136_RUN_V001 --par-run NGC3198_ROUTE_A_A2F10_HI136_PAR_RUN_V001 --hi-search-limit-kpc 136.5 --hi-max-metric-calls 2048 --write
   ```

2. Run the dry run:

   ```
   .../seed_v002/tools/dryrun_seed_v002.py HI136 NGC3198_ROUTE_A_A2F10_HI136_RUN_V001 NGC3198_ROUTE_A_A2F10_HI136_PAR_RUN_V001 --hi-search-limit-kpc 136.5 --hi-max-metric-calls 2048
   ```

3. Launch with the DEFAULT serial command, changing only the spec to `…/HI136/launcher/NGC3198_ROUTE_A_A2F10_REQUEST_C2V002_HI136.json` and the outdir, receipt and log to `NGC3198_ROUTE_A_A2F10_HI136_RUN_V001`.

Route B would additionally need a new NGC solver template and new driver pins.

**(b) truncation.** No exact command can exist until prep v002, the worker and the launcher successor are written and reviewed. After that, the command takes the DEFAULT shape with the new launcher, spec and outdir.

**(c)** None.

## Errors register

**E1.** The first DEFAULT `--write` set the PAR builder's `SERIAL_RUN` to the v002 run name. The route-B PAR template copy therefore came out byte-identical to `bbb37ca6` and still named RUN_V001.
- Fix: `SERIAL_RUN` is now the run name inside the base template.
- DEFAULT was regenerated with `--overwrite-own`.
- These superseded first-generation shas are no longer on disk: seed `52efe838`, request `5a8f7d4c`, PAR N8 `b1fbc9ea`, PAR N3 `d95d897a`, diffs `0f9fe5b4` and `ef0abee7`, seed diff `73ad5c67`.

**N1.** `check/` was created empty at the start of this lane and has been left for the checker.
