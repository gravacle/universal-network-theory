# CHECK V001: NGC3198 route-A A2F10 free-boundary diagnosis

**Checked:** `DIAGNOSIS_V001.md` (`bdb02a64…`), `DIAGNOSIS_V001.json` (`9fad71da…`), the `seed_v002/` files and the lane return.
**Checker:** an independent adversarial checker. It wrote only under `check/`.

**Method:**
- I wrote my own record decoder and replay harness (`check/tools/replay_c1.py`). I did not import `tools/replay_lib_v001.py`.
- Every module and blob sha was recomputed from bytes against the run's IDENTITY and START.
- The metric callback is transcribed from solver c2v001:129-158, with zero boundary jets (prep v001:269-273).
- I made single-column replays only. Nothing was launched.
- Runtime: the pinned codex python with `-I -B`, under `nice -n 10`, single-thread BLAS env, at most 5 workers.

**Target hygiene.** No velocity, target or V_obs file was opened.
- No result.json was opened: not the KMAX_/D7R1/V005/V006/V007/DECIDING ones, and not RUN_V001's either.
- The only profile input read is `GALAXY_RADIAL_SOURCE_REFERENCE_V001.json` (`f5becd45`), the run's own target-free source input. Of it, only the `HI_plus_He` block was used, plus a key-name scan.
- A scan of the diagnosis tools found no target, manifest or result.json access. TESTED-POSITIVE.

**No launches.**
- `runs/` holds no `NGC3198_ROUTE_A_*_V002` or `HI136` directory.
- No route-A NGC process is running. The processes that are running are root's KMAX/D7R2/DDO runs, and I did not touch them.

## VERDICT: PASS_WITH_CORRECTIONS

Everything numerical in the return re-derives exactly from bytes:
- the failure message;
- the call accounting;
- the extended-limit outcomes;
- the 1808/681 split;
- the first-failing-side counts;
- the mass fraction;
- the cut fractions;
- the seed diffs.

Option (a) is TESTED-NEGATIVE as stated, and the seed v002 changes nothing beyond what is claimed.

One MAJOR correction concerns the classification. The failing set is computed on an operator that, at these radii, carries azimuthal error larger than the escape threshold. That error is by root decision A1 numerical, not physical. "Not a numerics limit" (md:170) holds only in the sense "not a search-limit or call-budget limit".

## Re-derived facts (all TESTED-POSITIVE unless marked)

| # | Claim | Checker result | Evidence |
|---|---|---|---|
| R1 | Decoded FAILURE inputs | R = 0x1.6051053184631p+70 m (52.655307 kpc), φ 1.37445; step/limit/tolerance = 0.2 / 95 / 1e-8 kpc; σ0 11 km/s, Γ 5/3, 1024 calls, 8 panels; threshold log1p(h0/c²) = 3.3657664138980042e-09 | `out/CHECK_2503_C1.json` |
| R2 | Replay fidelity | Roster digest equals IDENTITY `gas_columns`. Rebuilt roster[2503] == FAILURE inputs (Python equality). All 2503 completed `column_input_sha256` match (0 mismatches). Columns 0, 1, 517, 1234, 2000, 2495, 2496, 2497, 2501 and 2502 re-solve with results equal to the decoded records (equality and type-tagged digest). | `out/VALIDATE_C1.json` |
| R3 | Column 2503 failure | Message reproduced **byte for byte**. 548 calls (1 + 71 minus + 476 plus), all unique. Minus side brackets at 9.0 kpc. Stopped by the limit (hi v002:66, 76-77), not the budget. | `out/CHECK_2503_C1.json` |
| R4 | Larger limits | At 136.5, 190, 272.97 and 500 kpc with non-binding caps: NOT_BRACKETED on the plus side. Residuals −1.1756077981851133e-07, −1.7046e-07, −2.1581e-07 and −2.3285e-07, equal to the diagnosis. | same |
| R5 | Plus-side profile | Maximum +3.2049808757559286e-09 at 30.0 kpc (0.952 of the threshold). −5.8006e-08 at 95 kpc, −2.1321e-07 at 270, −1.5206e-07 at 1000. Minus side: maximum 1.9121e-08 at 38.4 kpc. All equal to the diagnosis table. | same |
| R6 | Full sweep, 2489 columns, own harness | 95 kpc: 1808 fail, 681 OK. 136.5 kpc / 2048 calls: 0 rescued, and 681/681 roots identical. First failing side: minus 1181, plus 627. All 1808 are NOT_BRACKETED and unconfined to 500 kpc on at least one side. R range 52.655–136.301 kpc. Ring 2496: 2 of 25 unsolved fail (2503, 2519). **Per-column agreement with the diagnosis sweep: 0 disagreements** (OK flags, roots and messages at both limits). | `out/SWEEP_COMPARE_C1.json`, `out/sweep_*_of_5.jsonl` |
| R7 | Failing mass | 3.548e6 Msun of 1.39136e10 Msun gives **2.5503e-4**. | same |
| R8 | (b) cut fractions | Columns ≥ 2496 (R ≥ 52.655): 6.98e-4. R > 50.847: 1.087e-3. R > 66.904: 3.90e-5. R_2495 = 51.746 kpc. | `out/MASSES_C1.json` |
| R9 | No periodic images | The line sum is a finite nonperiodic sum over 80 unique Gauss k_z values (line v001:20, 46-53). lnN(270) − lnN(0) = −2.13e-7 ≠ 0. 272.97 kpc is not a period. | code and R5 |
| R10 | Code claims | hi v002:26-28 (limit is a failure budget), :66/:76-77, :113-115 (`finite_free_boundary` hard-coded). quadrature v002 has the `declared_noncompact_tracer` branch. hi v003 differs from v002 only by the optional direct log-ratio read (diff checked). prep v001 has no truncation input. Worker v002:16 pins prep `c54c7cc9`. launcher v001:97-98 refuses `mask`. v006 `template_mapping_check` is at :1471-1481. Drivers v006:262, v007:289 and v008:324 pin template `ba5e87eb`. Seed provenance: `hi_search_limit_kpc` is "DECIDED: N4"; `hi_max_metric_calls`/`hi_search_step_kpc` are "CARRIED… not NGC-reviewed". DDO base seed limit is 32 kpc. | code reads |
| R11 | Seed v002 vs 478a8467 | Exactly 4 leaf changes: the addendum sha in `decision_refs` and in `pins` (4070146d → 17c26616), `status`, and the added `seed_v002` block. **`numerical_inputs` unchanged; `derived` unchanged (1017).** All 10 pins verify from current bytes. | `tools/diff_json_c1.py` |
| R12 | Requests vs 9da3461b / packet PAR N8/N3 | Each has exactly 7 leaf changes: seed path and sha (argv and `launch_pins`), the outdir and checkpoint run name V001 → V002, and `note`. The route-B PAR template copy differs from `735dbb5d` only in the attempt/checkpoint directory and the label run name. All claimed shas match the bytes. Dry-run D3 `start.json` shows the worker pin `42bdd23e` (= installed worker v002) with seed `88ef386d`, so the seed-provenance loop (worker v002:57-58) passed. | same |

## Findings

**F1 — MAJOR — `DIAGNOSIS_V001.md:170` (and the return's "Physics reading") — the classification overstates robustness.**

The statement "This is **not** a numerics limit" holds only as "not a search-limit or call-budget limit". What I tested:

- **Azimuthal error on the actual operator (TESTED).** The iteration-0 source is exactly axisymmetric: `analytic_initial_azimuth` is true, so prep v001:288-296 builds both the fixed source and the initial gas as analytic rings. The true midplane lapse is therefore φ-independent. Across the 32 columns of one ring, the replayed midplane lnN varies by:

  | Ring (kpc) | Spread / threshold |
  |---|---|
  | 13.6 | 2.0 |
  | 40.3 | 6.8 |
  | 52.655 (the failing ring) | 12.8 |
  | 69.8 | 28 |
  | 115.3 | 46 |

  Source: `out/RING_PHI_C1.json`. Root A1-numerics (ROOT_DECISIONS_A1_A2:50) declares this cube-corner m=4/m=8 structure numerical. So at R ≳ 50 kpc the operator carries non-physical structure an order of magnitude larger than the 3.37e-9 escape threshold.
- **Grid adequacy on a known field (TESTED).** I put an exactly known isotropic field (a Gaussian-smoothed point mass) on the run's own G80C nodes. Its vertical difference Φ(R,φ,30 kpc) − Φ(R,φ,0) has these maximum relative errors over φ (`out/ANISO_C1.json`):

  | R (kpc) | a = 10 kpc | a = 5 kpc | a = 3 kpc |
  |---|---|---|---|
  | 52.655 | 0.2% | 1.1% | 63% |
  | 80 | 60% | 357% | 1965% |
  | 120 | 12× | 66× | 107× |

  For comparison, the threshold is about 1.5% of |lnN0| (2.19e-7) at 52.655 kpc.

- **Consequence.** The confinement verdict is at or below the grid's accuracy floor from about 50 kpc, and is quadrature-dominated beyond about 80 kpc. That covers 1258 of the 1808 failing columns (504 at 80–100 kpc and 754 at 100–140 kpc).
- **Column 2503 itself is marginal.** Its plus-side barrier is 0.952 of the threshold, a 4.8% shortfall.
- **What survives.** "Unconfined" is TESTED-POSITIVE as a property of the installed finite sum. Option (a) stays TESTED-NEGATIVE, because a run uses the same finite sum.
- **What it does not establish.** Whether these columns are physically unconfined at the anchor is UNTESTED.
- **Deciding test.** Re-prepare the iteration-0 operator on a transversely refined grid, then replay rings 2496 and 2560 and a ring at ≥ 80 kpc with `check/tools/replay_c1.py`. The refined grid should add nodes in the [0.01, 0.03], [0.03, 0.3] and [0.3, 2] panels, or be G80E14; the order must keep panel heights at or above about 140 kpc. In each ring, check that the φ-spread of lnN0 falls below the threshold before reading confinement.
- **Correction.** md:170 should read: "not a search-limit/budget limit; whether it is physical or grid numerics is UNTESTED, and the operator's own φ-error exceeds the threshold at these radii (TESTED)".
- **Missing option.** The options table should list grid numerics (G80E14 or another transverse refinement) as a counted option (d) with that deciding test. It currently appears only as "other levers" at md:195.

**F2 — MINOR — md:14, 21, 138 — "no free boundary up to 1000 kpc" and "unconfined to 500 kpc" describe the finite sum where it has no fidelity.**
- There are no periodic images (R9).
- On the same known field along z at φ = 0 and R = 52.655 kpc, the G80C sum's absolute level is wrong by 28% at 273 kpc and by 2.05× at 1000 kpc (`out/LOWK_C1.json`).
- The replayed lnN(z) − lnN(0) does not decay at z = 2e3–1e6 kpc. Its window means are −3.7e-8 to −2.8e-7, its spread 1e-8 to 1e-7, and its maximum |value| up to 4.2e-7.
- Vertical differences are accurate to ≤ 0.33% up to 136.5 kpc (a ≥ 10 kpc), and to 5.6% at 273 kpc.
- **Correction.** Heights above about 140–270 kpc are quadrature-limited, not image-limited. Statements beyond that height should be labelled "finite-sum property; no physical content". This does not change (a), which fails already at 136.5 kpc.

**F3 — MINOR (physics fact omitted) — md §4.** The diagnosis describes the large-z fall without saying where it comes from.
- **Low-k amplitude.** The iteration-0 lapse amplitude A₀(k) = weighted_response/dk-weight is finite and positive as |k| → 0. It is about +6–8e56 at 0.002–0.007/kpc; A·k² → 0, so it is not 1/k². It changes sign near |k| ≈ 0.025/kpc, inside the order-3 panel [0.01, 0.03].
- **Origin decomposition.** At the origin the |k| < 0.03 shell contributes +2.5e-7 and the higher shells −1.6e-6.
- **Midplane lnN with R.** It is −1.1e-6 at R = 2 kpc, crosses zero near 20 kpc, and holds at about +1.8 to +2.9e-7 from 40 to 200 kpc (`out/LOWK_C1.json`, `out/VALIDATE_C1.json`).
- **Reading.** The large-z fall is lnN relaxing from this elevated outer plateau. The sign change sits inside a 3-node panel, so the refinement in F1 and the md:176 deciding test must include [0.01, 0.03].
- **Status.** All of the above is TESTED as facts of the installed operator. Whether it is physical is UNTESTED, with the F1 deciding test.

**F4 — MINOR — md:176 vs the return.** The deciding test says "refined panels below 0.1/kpc" in the md and "below 0.3/kpc" in the return. Use one statement, and include transverse/high-k refinement per F1.

**F5 — MINOR — option (b) cost and caveats (md §5).**
- Truncation also changes the iteration-0 operator itself: prep v001:257-268 builds the initial gas from the kept roster. So the 2503 completed records are not reusable, and kept columns at 46–52 kpc must be re-solved.
- Their barriers are 0.95–12× the threshold, against a φ-error of about 8–13× the threshold (F1).
- (b)'s viability remains UNTESTED, and that statement is correct. The table should add "completed iteration-0 records not reusable; kept outer ring within grid error".

**F6 — MINOR — `seed_v002` packaging.**
- The builder emits a route-B template copy only for the PAR run.
- The packet's serial route-B template `ngc_f10_c2/route_b_v006/specs/CALL_NGC3198_ROUTE_B_A2F10_TEMPLATE_C2V006.json` (`bbb37ca6`) still names `NGC3198_ROUTE_A_A2F10_RUN_V001` (3 occurrences).
- If root chooses the serial DEFAULT launch, a serial route-B template re-pointed to RUN_V002 is also needed. This affects route B only, and only if route A ever converges.

**F7 — NIT — `HASHES.txt`** has 56 hash entries plus 1 header line, not "57 entries". All 56 verify from bytes, and none is missing.

**F8 — INFO — DEFAULT relaunch prediction.** "Reproduces the column-2503 failure exactly" is well supported but stays UNTESTED until run.
- The supporting reasons: the numerical inputs are identical (R11), the operator is a deterministic function of the seed, and the replay is bitwise.
- Launching DEFAULT therefore buys no new information about confinement. It only re-measures the same failure about 24 min in.

## Option claims against code: summary

**(a)**
- The constants status is correct: the limit is root-decided (N4), and the calls and step are carried DDO controls.
- The route-B refusal path is correct (v006:1471-1481; three drivers pin `ba5e87eb`).
- TESTED-NEGATIVE is confirmed: 0 of 1808 rescued.
- Heights above 136.5 kpc are not made meaningless by periodic images (there are none). They are quadrature-limited (F2).

**(b)**
- The code obstacles are confirmed: no truncation input in prep, the prep pin in the worker, and the launcher mask refusal.
- The mass fractions are confirmed.
- Viability is UNTESTED, plus F5.

**(c)**
- Confirmed empty as reviewed code.
- hi v003 is precision-only. The tail branch exists only in quadrature v002 and is unreachable from hi v002:113-115.

**Missing (d):** grid numerics, per F1.

## Checker files (sha256 in `check/HASHES.txt`)

**Tools** (`check/tools/`):
- `replay_c1.py`
- `check_2503_c1.py`
- `sweep_c1.py`
- `compare_sweep_c1.py`
- `lowk_c1.py`
- `aniso_c1.py`
- `ring_phi_c1.py`
- `masses_c1.py`
- `diff_json_c1.py`

**Outputs** (`check/out/`):
- `CHECK_2503_C1.json`
- `VALIDATE_C1.json`
- `SWEEP_COMPARE_C1.json`
- `sweep_{0..4}_of_5.jsonl`
- `LOWK_C1.json`
- `ANISO_C1.json`
- `RING_PHI_C1.json`
- `MASSES_C1.json`
