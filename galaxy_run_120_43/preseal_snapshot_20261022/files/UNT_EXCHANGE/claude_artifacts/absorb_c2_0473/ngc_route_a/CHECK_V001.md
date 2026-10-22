# CHECK_V001: independent check of NGC_ROUTE_A_V002_REVIEW_V001

**Verdict: PASS_WITH_CORRECTIONS**

- The N1 port verdict and the fixture verdict stand.
- I re-derived every numerics fact independently, and all of them reproduce.
- I found 9 defects:
  - 1 stale hash in the .md;
  - 1 misread of measured roots;
  - 1 grid ranking that the evidence cited for it does not support;
  - 1 spoke-resolution geometry that is too optimistic;
  - 1 off-by-ceil call bound;
  - 4 context or wording items.
- None of them reverses an N1 or fixture status. Two of them change how the numerics proposal should read (D3, D4).
- No estimate was repaired. No PSD or sign repair was found or done.

**Scope.** Claude2 lane, absorb 0473. The checker did not write the review.

**Write location.** All writes are under `ngc_route_a/check_v001/` plus this file.

**What was not done:** no launch, no NGC3198 target velocities opened, no deletion, and nothing touched in any run directory.

**Runtime.** `codex-primary-runtime python3 -I -B`, numpy only, single thread.

## Checker artifacts (sha256 from bytes)

| File | sha256 |
|---|---|
| `check_v001/check_numerics_v001.py` (written from the sources; does not import the review's script) | `58d4e34206be140fe81c5c40bc8a1881b1f7e5fdf96251265eb8668a67e0ffa0` |
| `check_v001/CHECK_NUMERICS_V001.json` | `61ea00e326d8bed93becee5b3e940cff2743008481d107b599e61cc4df66e23f` |
| `check_v001/fixture_repro/FIXTURE_RESULTS_REPRO.json` (fresh re-run of the byte-identical fixture drivers and toys in a new tree) | `0271bb39c7daeac4d9acc91e6926fec9fee744ff456ba950ca6c459353ce4e36` |

**Inputs re-verified from bytes:**
- profile `f5becd45…`, manifest `a2936517…` (keys `Rad_text`, `Rad_unit`, ids only; no velocity fields);
- DDO V002 progress `3fe2ba91…`, result `79855e78…`, seed `694eaaaa…`;
- NGC seed `ff0d70b4…`;
- the NGC, DDO v001 and DDO v002 binding and worker files;
- the port pair `cc5db369…` / `42bdd23e…`;
- the 5 LOCAL pins (prep `c54c7cc9`, composite `75092cf6`, stream `cbbc4b96`, base `7167a264`, prediction `54136c71`). All match.
- `ngc_composite_full_coupled_binding_v002.py` is not present in `helpers/recovered_packet_audit/`, which confirms the install constraint.

## Confirmed claims

### N1: TESTED-POSITIVE

I checked this with `diff` and my own difflib run.

- **Binding.** The only change is the 28-line insertion after NGC v001:45. It is textually identical to DDO's insertion after v001:51.
- **Worker.** There are 3 changes:
  - the `LOCAL['binding']` pin → v002/`cc5db369…`;
  - the seed-coordinate block at v002:59-62;
  - the caller-identity fields at v002:102-103.

  The last two are textually identical to DDO's.
- **Lineage hunks.** The DDO-vs-NGC hunk counts are 10/10 (binding) and 9/9 (worker) before and after the port.
- **Compile.** Both files compile.
- **Prep keys.** The binding reads `data['fourier_arguments'][Eref, ell_F, gamma, Cbar, mubar, jbar, registered_bravais, boundary_description]`, `c_m_s`, `gas_columns[*].hi_options`, `source_pins` and `stellar_quadrature_mass_kg`. NGC prep v001 returns all of them (:113-125, 274-283, 297-302).

### Fixture: TESTED-POSITIVE (toy scope), reproduced

- **Result.** A fresh run in a new tree gives `ALL_PASS: true`, and all 9 case outcomes are identical (S0-S8).
- **Analysis fields.** Every analysis field is equal, except the checkpoint identity sha. Mine is `d7ab7c47…`, against `25c79a44…` in the record. That is expected, because the identity binds absolute seed and toy paths.
- **Reproduced behaviour:**
  - S1/S3 reconstructed gas is bitwise equal;
  - the resume point is {1, 5};
  - binding v001 and v002 with `checkpoint=None` are bitwise equal.

### Code facts verified by reading

- **HI free boundary (hi v002).**
  - The search breaks at the first bracket, so the limit costs nothing for bracketed columns (:66-77).
  - The call cap is `len(cache)>=max_metric_calls` (:51-52).
  - Each column gives 17 nodes (2·panels+1).
- **Solver (`44d9c23c`).**
  - Columns run in `gas_columns` order, inner→outer (prep:168-179).
  - The first column `ValueError` returns `FAILED_SOURCE_PREPARATION` (:152-179).
- **Checkpoint.** c2v003:474-475 caps columns at ≤100000.
- **Columns.** A zero-mean Bernstein bin has all-zero coefficients, so the prep:176 skip equals the zero-annular-mean skip. That gives 39 × 4 = 156 columns per azimuth. **FORMAL-RESULT confirmed.**

### Numerics reproduced exactly (my script against NUMERICS_FACTS_V001)

| Group | Reproduced values |
|---|---|
| NGC geometry | 51/39 annuli; column R_max 136.30; support 136.48; fraction of columns beyond 45.49 = 0.5641 and beyond 66.9 = 0.3590; 43 queries 0.32-44.08; minimum edge distance 0.011485 kpc at 8.04 |
| DDO roots and calls | Calls formula: 0 mismatches over 2880 columns. Calls 73/89/258. Max \|root\| 22.681 kpc (iteration 4, column 569, R = 14.049), 70.9 % of 32. Edge mean root / R = 1.266. |
| DDO timing | 0.1369 s + 2.570e-4 s/call (median 0.1616 s); transform tail 101.8-102.5 s |
| DDO stencils | radial max 7.30e-4, median 1.10e-5; angular max 4.87e-2, median 2.82e-3 |
| HI budget | fixed calls 67; Σ ≤ 191.4 kpc; calls at L = 32/64/95: 387/707/1017 |
| Grids | G72/G80B/G80C/G80D pass the replicated prep checks; maximum rad/node at 44.08 kpc = 7.347/3.673/3.086/3.568; cost 80³/72³ = 1.372 |
| Stencil scalings | 0.2368, 1.7632, 0.002686; (m·da)²/6 values as stated |
| Cost model | 0.140/0.561/1.543/4.769 h at nk = 80 |

**Claude4 N2 citations.** These reproduce at the cited JSON paths:
- A: G72 worst panel error 4.7e-3 at 14.1 and 0.286 at 22.68; ≥0.56 at 88.16 for every grid;
- B: index 5 = 44.08 kpc;
- C, D, E, F and H.

## Defects and corrections

**D1. Record and hash (MD §2, S3 row).**
- **Defect.** "The identity sha is the same, `bd469dee…`" cites the superseded `FIXTURE_RESULTS_TRY3.json`.
- **Correction.** The record `FIXTURE_RESULTS_V001.json` gives S1 = S3 = **`25c79a44b29c6c3eb9d7a2eaf41bbd4a56f144e61aeb2c65496832e629d2ac33`**. The review JSON is already correct.

**D2. Misread of measured DDO roots (hi_search_limit row).**
- **Defect.** "The minus side is larger (19.5 vs 12.4 kpc)" is false as a side statement. Those two values are the single φ=0 column of the edge annulus: z− = 19.46 and z+ = 12.41.
- **Correction.** Over the 8 edge azimuths, the mean is z− = z+ = **17.78 kpc** in iteration 4, and the means are equal in every iteration. The measured pattern is z−(φ) = z+(φ+π), not a minus-side excess. Edge roots span 12.4-22.7 kpc across azimuths.
- **Impact.** Removing the side claim leaves the symmetric-limit proposal unchanged.

**D3. Grid ranking not supported by the cited evidence.**
- **Defect.** G80D is proposed as primary and G80C as the alternate. The same N2-B toys favour G80C on the derivative metric. The 43 rows use derivatives (pred v005:118-131: dP/dR and dlnN/dR).
- **Evidence.** Maximum over queries ≤44.08 kpc of dU/max\|dU_ref\|:

  | Toy case | G80C | G80D |
  |---|---|---|
  | poisson\|disk | 0.011 | 0.015 |
  | toyIR\|disk | 0.011 | 0.016 |
  | toyIR\|point | 0.0054 | 0.053 |
  | toyIR\|hi_like | 0.0032 | 0.0042 |
  | poisson\|point | 0.0054 | 0.053 |

  G80D is better only on U (potential) error, for example hi_like at 44.08: 2.2e-6 against 8.1e-4.
- **Further caveat.** At 44.08 kpc the point-source U error is 0.40 (G80C) and 1.23 (G80D), so no grid resolves U there. The review cites only the hi_like U error.
- **Correction.** On the cited evidence, rank **G80C first and G80D second**, or present them unranked. Both remain UNTESTED on the program operator, and the deciding test is unchanged.

**D4. Spoke "resolved beyond R = n/kmax" uses an isotropic cutoff, but the program cube is the signed cube |k_i| ≤ kmax.**
- **Why it matters.** In-plane |k| reaches 2√2 = 2.83 /kpc on the diagonals. Spoke harmonics are therefore fully excluded only for R < n/(2√2) and partially passed between that radius and n/kmax.
- **Corrected suppression radii (full / isotropic):**

  | n | Full exclusion inside | Isotropic edge (review) |
  |---|---|---|
  | 8 | 2.83 kpc | 4 kpc |
  | 32 | 11.3 kpc | 16 kpc |
  | 88 | 31.1 kpc | 44 kpc |
  | 272 | 96.2 kpc | 136 kpc |

- **Specific claims that are false:**
  - "88 (unresolved at every query radius)" is false even isotropically, because 44.08 > 44.0. Under the cube, 7 of 43 queries lie beyond 31.1 kpc.
  - "272 (unresolved over the HI support)" is false under the cube.
- **Corrected counts.** Full-suppression n at the maximum query is ≥125; over the HI support it is ≥387.
- **N2-C caveat.** N2-C used a spherical |k| < 2 toy, so its bias numbers do not cover cube-corner passage. The number of queries beyond the isotropic edge for n = 32 is 15 of 43; beyond the cube-corner edge it is 17 of 43.
- **Proposal.** 32 stays a proposal; its stated resolution radius should read 11.3-16 kpc.

**D5. HI call-cap bound.**
- **Defect.** "A symmetric limit is ≤ 95.7 kpc" ignores the ceilings in the call count. At 95.7 kpc the count is 1025 calls, which exceeds the 1024 cap.
- **Correction.** The largest symmetric limit is **95.6 kpc** (1023 calls).
- **Impact.** The proposal of 95 (1017 calls) is unaffected.

**D6. Context omitted (grid and outer columns).**
- **Defect.** "56 % of columns lie beyond 45.5 kpc" omits Claude4's own N2-G mass figure, which the review says it incorporates. Annuli beyond 44.08/45.49 kpc hold **0.40 %** of HI annular mass, and beyond 66.9 kpc they hold 3.9e-5. I recomputed this as π·m·Δs.
- **What stays valid.** The failure-risk argument holds: any outer column failure stops the iteration.
- **What changes.** "Outer columns grid-dominated" bears on the 43 rows only through about 0.4 % of HI mass. It should not be read as a large prediction-level effect. That effect is UNTESTED; the deciding test is unchanged.

**D7. Context omitted (azimuth step).**
- **Defect.** The review does not say what `azimuth_step_rad` affects. It enters only the diagnostics: Euler, continuity and adiabatic residuals and `pressure_phi_stencil_difference` (pred v005:155-201). `speed_km_s` uses only the radial derivative (:118-131, 214-218).
- **Correction.** The 0.0025 proposal does not change the 43 predicted rows.
- **Scale of the measured quantity.** DDO's 4.9 % angular stencil difference is relative to a near-zero quantity. Measured \|Δ∂φP\| / (R·\|∂R P\|) has maximum **2.2e-6** and median 9.6e-8.

**D8. Wording.**
- **Defect.** "0.0025 equals the DDO kmax·R·da at the NGC outer query (0.00269)."
- **Correction.** 0.0025 < 0.00269, which gives kmax·R·da = 0.220 against DDO's 0.237. Say "at or below".

**D9. Approximation stated as value.**
- **Defect.** "(m·da)²/6 reaches 0.52" is the leading-order figure.
- **Correction.** The exact central-difference error 1 − sin x/x is **0.443** at da = 0.02 and 0.0081 at da = 0.0025. The conclusion is unchanged.

**Observation (not a defect).** The ported `preparation_scope` label ("Adopted reference rest-energy source, N-only HI vertical preparation") is DDO wording copied byte-exactly into the NGC identity. That is exactly what the dispatch asked for ("change nothing else"). It is metadata only, but it does not mention NGC's H2 tail.

## Corrected key numbers

| Item | Review | Corrected |
|---|---|---|
| S1/S3 checkpoint identity sha (record V001) | bd469dee… | **25c79a44b29c6c3eb9d7a2eaf41bbd4a56f144e61aeb2c65496832e629d2ac33** |
| DDO edge-annulus mean roots z−/z+ | 19.5 / 12.4 (side excess) | **17.78 / 17.78** (no side excess; 19.46/12.41 is φ=0 only) |
| Largest symmetric HI limit within 1024 calls at step 0.2 | ≤95.7 | **95.6** (proposal 95 → 1017 calls, OK) |
| Grid ranking on the cited N2-B derivative evidence | G80D, then G80C | **G80C, then G80D** (or unranked); both UNTESTED |
| Spoke full-exclusion radius n/(2√2) for n = 8/32/88/272 | 4/16/44/136 kpc | **2.83/11.3/31.1/96.2 kpc** |
| n for full exclusion at 44.08 kpc / over the HI support | 88.16 / 273 | **≥125 / ≥387** (signed cube) |
| HI mass fraction beyond 45.49 kpc (for the "56 % of columns") | not stated | **0.40 %** (3.9e-5 beyond 66.9) |
| Exact central-difference error at the band edge, da 0.02 / 0.0025 | 0.52 / 0.008 | **0.443 / 0.0081** |
| DDO angular stencil difference / (R·\|∂R P\|) | not stated | **max 2.2e-6** |

Everything else in the review's numerics table and JSON reproduces to the stated precision.

## Status words after correction

| Item | Status |
|---|---|
| N1 port | **TESTED-POSITIVE** |
| Fixture | **TESTED-POSITIVE** (toy scope, reproduced) |
| Column count 4992 at n_az 32 | **FORMAL-RESULT** |
| h2_tail_mass_rtol | **FORMAL-RESULT + TESTED-POSITIVE** (synthetic) |
| hi_search_limit, grid, azimuth count, azimuth step | **UNTESTED**, with the deciding tests as the review states them |
| Grid ranking | Re-ordered per D3 |
