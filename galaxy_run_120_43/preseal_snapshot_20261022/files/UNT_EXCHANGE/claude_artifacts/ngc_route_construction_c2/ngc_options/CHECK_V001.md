# CHECK_V001: independent check of `ngc_options/` (NGC_CONSTRUCTION_OPTIONS_V001)

Claude2 lane, independent checker (not the author). Everything I wrote is in `ngc_options/check_v001/` plus this file. There was no project launch, and no NGC3198 velocity file was opened (only the target-free manifest). The check used numpy only, single thread, `-I -B`, and every hash below is computed from bytes.

## Verdict: PASS_WITH_CORRECTIONS (1 major, 8 minor)

- **Nothing is invented and nothing is decided.** Every NGC value in the memo traces to reviewed code or data, to the 0473 review, or to arithmetic on them. Every open value is either labelled `ROOT DECISION NEEDED` with options or recommended for Claude2 to decide.
- **Every cited source line I checked says what the memo says (§2).** The exceptions are the minor items below.
- **Major defect.** The S5-M2 specification is wrong as written. The memo says the segment-monotone reducer needs "one isolated-bin exception" (bin 26). An exact chain-LP check shows that **5 bins need a within-bin hump whatever directions are chosen**. The memo's target-sign direction rule needs **6**. All of them lie beyond the query range (≥ 58.9 kpc), so M2's purpose inside 44.08 kpc survives, but the rule must be respecified before review (D1).

## 1. Reproduction and code checks

| Check | Result |
|---|---|
| Artifact hashes vs `HASHES_NGC_OPTIONS_V001.txt` | All 4 match (`9e65bd0f…`, `8ba60ee7…`, md `5a30ce31…`, json `1cc053be…`) |
| Facts script rerun (a byte copy in `check_v001/rerun/`) | Output **byte-identical** to `NGC_OPTIONS_FACTS_V001.json` (`8ba60ee7…`) |
| AST scan of the facts script | The only I/O call is `OUT.open('x')` (line 327). Imports are stdlib + numpy. There is no subprocess. The only velocity-like string is the manifest name. |
| Top-level side effects of the 4 modules it executes (reducer V002, adapter v002, obs v001, kernel v001) | None (the reducer's `main()` is `__main__`-guarded) |
| Input pins (11 in the facts script, plus the map pair, 0473 and the 8 extra JSONs cited in memo §8) | All recomputed from bytes; all match their cited prefixes |
| Cited code files (map §7 keys) | All 15 shas match the map |

**Independent re-derivation.** `check_v001/check_ngc_options_v001.py` uses its own Bernstein evaluator, its own roster code and different synthetic data. Results:

- **Zero bins.** 12 zero bins [25, 27-29, 32-34, 38, 44, 45, 48, 49]. The edge controls are 0 at all of them. The annuli have a uniform width of 2.676 kpc.
- **Roster.** 156/195/312/390/468 columns at GL 4/5/8/10/12. The smallest nodes and the max gaps below 7.06 kpc (= Q22) agree to the last ulp. The minimum uniform order covering Q01 is 10.
- **Adapter, my synthetic data.**
  - GL4 with 43 rows refuses at Q01; with the 41 in-support rows it returns 41.
  - GL5 with 43 rows refuses at Q01; with 42 rows it returns 42.
  - GL10 returns 43.
  - The HI ratio cancels: |Δ| ≤ 2.8e-14 km/s for ratios 1/1.36, 1 and 0.3.
- **Reducer V002.** It refuses NGC (reducer:31-32) and reproduces the saved DDO controls bitwise.
- **Domain fractions and grids.**
  - Mass and column fractions beyond 45.49 / 66.90 kpc: 0.397 % / 0.0039 % of mass, 56.4 % / 35.9 % of columns.
  - G72/G80C/G80D phases and k_min checks are as stated. The grid definitions match 0473 `numerics_facts_v001.py:141-144`.
- **Cost arithmetic.** DDO chain 1.42 h. NGC 3.08 h (GL4), 4.22 h (×1.37), 7.69 h (GL10) and 10.55 h (×1.37).
- **Small numerics.** The FS bracket width ratio is 1.1, which costs +0.1375 bisection steps. There are 21 n_columns needle hits on 18 lines in the map.

## 2. Source-line verification (memo citation → what the bytes say)

All of the following were read and match the memo's statement:

- **ngc_prep.**
  - :51-55 explicit integer orders ≥ 2, and the signature (:36-44) has no default;
  - :63-67 manifest rows and radius rule;
  - :105-118 profile controls and σ0 11000 / Γ 5/3;
  - :142 nk ≤ 80;
  - :162-179 roster with the Σ==0 skip at :176;
  - :187-249 stellar/H2 rings use the same `gauss` radially and vertically, so they scale as (n/4)².
- **reference.**
  - :22-23 SEED/IDENTITY;
  - :55-63 identity and iteration_0004 converged custody;
  - :67-77 profile controls;
  - :78-89 roster from `ni['source_gauss_order']`, with the digest equal to the checkpoint `gas_columns`;
  - :85 skip.
- **body.**
  - :19-23 reference run and monotone SOURCE pins;
  - :57/66 Σ from the monotone `source_record`;
  - :60-61 `leggauss(4)`;
  - :62-64 all-annuli R == reference radii and `len 72`;
  - :65 `leggauss(8)`;
  - :81 `n_phi=16`.
- **join.** :11 and :26 hard-code 72; :13 refuses Σ ≤ 0; :14 requires n_phi == 16.
- **cm_adapter.** :47-50 moment/intensity, with `MISSING_EMISSION` at :49; :55 `QUERY_OUTSIDE_SUPPLIED_RADIAL_SUPPORT`.
- **column_mean.** :7 binding pin; :31/35 72; :32 ω ≤ 0 refuses; :41 ratio applied to the weights.
- **rotation.** :75-76 and :91-95 72/16; :79-82 Σ_R from the monotone controls; :83 spline over R nodes for d ln K/dR.
- **columns.** :14 OFFSET_SHA; :75/84/94/96 16 angles.
- **offset.** :19 BODY_WORKER_SHA.
- **column_module.**
  - :16/48 GL panels give n_z = 32;
  - :36 `NO_TWO_SAMPLED_FREE_SURFACES`;
  - :57-67 mass bisection.
- **Other modules.** reference_module:31 and body_base:28/35 (16 angles, σ0, Γ). ngc_binding:73 (43 rows) and :79 (radians 72/73).
- **driver c2v002.**
  - :81-82 fixed args;
  - :91 DDO binding;
  - :92 template;
  - :94-97 registered geometry, n_columns/n_queries, K 64/121;
  - :130-131 DDO overrides (11 FS indices; RFS 71 → 1.01);
  - :154-155 rule factors, including the existing `rfs_factor_overrides`/`le_factor_overrides`;
  - :719/725 iteration 4;
  - :750-756 `rule_brackets`;
  - :1045/1049 template bracket;
  - :1148 per-call PINS;
  - `k_domain.length_kpc` exists (:1686-1688, check at :1708-1733).
- **reducer V002.**
  - :3-6 objective and targets;
  - :31-32 guard;
  - :35 targets;
  - :36-42 scaling, where a zero target gives norm 0 and a refusal at :41;
  - :43-46 constraints;
  - :117 hard-coded DDO key.
- **c2v003:474-475.** `resumable_coupled_gas_0422/coupled_gas_checkpoint_c2v003.py`: iterations ≤ 10000, columns ≤ 100000.
- **CODEX1 JSONs.**
  - The monitor:4 arguments are 200000 / 1e-10.
  - OUTER_FS selection text ("one-half through original nominal gamma sigma²/(gamma-1)"), as quoted.
  - BRACKET_CORRECTION: 11 indices at [h0, 1.05·h0] with "0.09percent..4.46percent".
  - REFRESHED_OUTER: index 71, "no surface in32kpc", choose 1.01H.
  - LOWER_ENTROPY_FS: "0.4..0.9 of preceding11-reference columns".
  - LOWER_ENTROPY_PREPARATION_CHOICE: status `ADOPTED_SEPARATE_SENSITIVITY_MEMBER_NOT_VALIDATED`, cause 28 nodes, finish `25484f7e…`.
  - SOURCE_STATE_BINDING_V003: σ0 sensitivity [8, 14].
  - Frozen-midplane `result.json`: old negative Ω² at [39, 43, 47, 51, 55, 59, 62, 63, 66, 67]; new at [63, 64, 65].
  - DDO binding: status, 12 rows at 0.49 kpc spacing, radians 66/64, ratio 1/1.36, tracer/observation texts.
  - Seed V002: 33 keys, `max_iterations` 8, `source_gauss_order` 4; its `quadrature_selection_evidence` is lapse-only.
- **Main source NGC3198 annular input.**
  - `settings.helium_factor` 1.36 and `rules.helium` text;
  - `settings.distance_pc` 13800000.0;
  - S2 `radial_coordinate` "…at 13.8 Mpc".
- **0473 review.**
  - Proposals 95 kpc, G80D/G80C (orders as stated), n_src 32 / n_obs 12, azimuth step 0.0025 (DDO median 0.28 %), `h2_tail` 1e-12 (N2-E), 0.56 h/iteration;
  - N2-A (no ≤ 96 grid resolves X ≥ 88 kpc);
  - G80K15 shows no gain;
  - the 33-key `numerical_controls`;
  - `IDENTITY_MISMATCH` tested for `pressure_step_kpc` and Eref.

## 3. Defects

### D1 (MAJOR): S5-M2 needs at least 5 forced-hump bins, not 1; the stated direction rule needs 6

**Where.** md §1 S5 M2 row and the S5 table "one isolated-bin exception"; §6 item 2; JSON `structural[S5].options[M2].what` and `counted_assumptions_added[1]`.

**Test.** `check_v001/check_m2_feasibility_v001.py` → `CHECK_M2_FEASIBILITY_V001.json`.

**Method.** Exact forward projection of the chain LP. A falling bin requires d_i ≥ b ≥ d_{i+1} ≥ 0, a rising bin requires 0 ≤ d_i ≤ b ≤ d_{i+1}, and a zero bin forces d_i = d_{i+1} = 0. The projection of each bin's polygon is an interval, so the check is exact. Minimal exemption sets were found by exhaustive subsets of size ≤ 3 per zero-delimited island.

| Island (bins, R kpc) | Memo rule directions | Minimal humps, memo rule | Minimal humps, any directions |
|---|---|---|---|
| 0-24 (0-66.9) | RRRF…F | 1: {22} or {23} (58.9-64.2 kpc) | **0** |
| 26 (69.6-72.3) | R | 1: {26} | 1: {26} |
| 30-31 (80.3-85.6) | RF | 1: {30} | 1: {30} |
| 35-37 (93.7-101.7) | RFF | 1: {36} | 1: {36} |
| 39-43 (104.4-117.8) | RFFRF | 2: {40, 42} | 2: {40, 42} |
| 46-47, 50 | RF, R | 0 | 0 |

**Why (FORMAL).**
- Two consecutive falling bins require m_i ≥ d_{i+1} ≥ m_{i+1}. At bins 22→23 the targets fall in both bins (m21 > m23, m22 > m24) while the means rise (m22 4.04e-4 < m23 6.31e-4).
- A rising-then-falling two-bin island between zeros needs both d ∈ [1.5·m30, 3·m30] and d ∈ [1.5·m31, 3·m31]. These are disjoint when the means differ by more than 2×, and m30/m31 ≈ 3.85.
- The same mechanism, with more bins, applies to islands 35-37 and 39-43.

**Consequence.**
- The memo's "(iii) an exception for bin 26" is correct for bin 26 but incomplete.
- M2 as specified (target-sign directions + zero handling + bin-26 exception) is infeasible. A reducer built to that spec would fail or be unresolved.
- Inside the query range, hump-free monotone segments are feasible: island 0-24 needs 0 humps under some direction assignment. The memo's target-sign rule, however, already needs one exemption at 58.9-64.2 kpc in that island.
- All forced humps are beyond 58.9 kpc, where the HI mass fraction is below 0.4 % (below 0.004 % beyond 66.9 kpc). So M2's stated purpose is not undermined for the 43 queries.

**Correction needed.** Respecify M2 before review:
- state either a feasibility-based direction rule, or the target-sign rule with an explicit exemption set;
- list the forced-hump bins {26, 30, 36, 40, 42} (FORMAL, direction-independent) plus any rule-induced bin;
- change "one isolated-bin exception" in §0, §1, §6 and the JSON.

The label for M2's feasibility should be TESTED-NEGATIVE for the rule as written. The facts script did not test it.

### D2 (minor): rising-node counts include rounding-level slopes

Bins with flat profile controls (d_i = d_{i+1} = m_i) give |dΣ/ds| of about 1e-15 relative, and the facts script counts these as rising. These are DDO bin 17 and NGC bins 0, 22 and 41. Excluding |slope| ≤ 1e-12·m:

| Count | Memo | Corrected |
|---|---|---|
| DDO profile | 36/72 | 34/72 |
| NGC profile | 78/156 | 72/156 |
| NGC inside 44.08 kpc | 34/66 | 32/66 |

"That rule puts a hump in every bin" is also overstated: exactly flat bins have none. The qualitative argument is unchanged.

### D3 (minor): §2.4 template arithmetic

"Cached samples are at most about 950 per side". At 95 kpc and 0.2 kpc per step it is 475 per side, or 950 for both sides. The conclusion (well within 20000 calls) is unchanged.

### D4 (minor): classification of the K factor

`entropy.K_factor` 64/121 is listed as "already counted for DDO; shared, not new" and in §6 as adding nothing. However:
- its source records `ADOPTED_SEPARATE_SENSITIVITY_MEMBER_NOT_VALIDATED`, selected in response to a DDO-specific failure (28 nonpositive nodes);
- the map classes it `NUMERICS_DDO_SELECTED`;
- the memo counts the coupled le_first factors as a DDO transfer but not the K factor itself.

It should either join the counted DDO-transfer group or carry an explicit argument for why sharing a member adds no NGC assumption. It remains `ROOT DECISION NEEDED` with options (i)-(iv), so nothing is decided.

Related point: "It is only consistent with K factor 64/121" (le_first) is stronger than shown. What is formal is that factor 1 gives an H ratio of about 1, which lies outside [0.4, 0.9]. Intermediate factors are not excluded.

### D5 (minor): §0 line 36 contradicts §2

§0 line 36 says the §2 fields are custody or galaxy-agnostic and "none of them is a choice". But §2.3 (tracer-text `ROOT DECISION NEEDED`) and §2.4 (FS bracket options i-iii, template options i-ii, K factor `ROOT DECISION NEEDED`, `n_z` alternative) contain choices.

### D6 (minor): undefined key and section reference

- `c2v003` is not defined in the memo's abbreviations. I verified it as `resumable_coupled_gas_0422/coupled_gas_checkpoint_c2v003.py:474-475`.
- The memo says file keys "follow map §3", but `column_module`, `reference_module`, `body_base`, `ngc_binding` and `mesh` are resolved only by map §7.

### D7 (minor): review citation for reducer V002

`DDO_MONOTONE_BERNSTEIN_QP_V001_REVIEW_V001` reviews the V001 bytes (`27d6d121…`). V002 (`50edaba7`) is covered by the delta review `MONOTONE_SOURCE_V002_FROZEN_MIDPLANE_REVIEW_V001` (`a1680b6d`). The memo's wording reads as if both reviewed V002. Both are PASS_SCOPED, as stated.

### D8 (minor): `geometry.registered.HI_original_distance_Mpc`

The memo gives 13.8 as "supplied", and §6 says it adds nothing. The map classes it `NONE_IN_REVIEWED_CODE`. The value is genuinely sourced: main source `settings.distance_pc` 13800000.0 and S2 `radial_coordinate` "at 13.8 Mpc", both verified. But the memo should state that it is a recommendation over the map's NONE status, with "omit" as the alternative it already lists. It is non-load-bearing, since no stage reads it.

### D9 (minor, informational): §4 phase table

The table reports outer-panel phase only. G80C's worst panel at 44.08 kpc is [0.3, 1] at 3.09 rad per node (0473 NUMERICS_FACTS 3.0856), not the outer panel's 2.94. The ordering G80C < G80D still holds.

## 4. Not defects (checked and confirmed)

- **S1-S4 structural facts and S3 options A-F.** The arithmetic is correct. Option A is inside reviewed code: prep takes the order with no default and the reference reads `ni`. The GL order is in the checkpoint identity, so it must be fixed before route A.
- **S5 refusal and formal emptiness of the V002 family for NGC.** The inner peak at edge 3 (8.03 kpc) follows from the targets (6.369 → 6.698 → 6.483). The bin-26 forced hump is FORMAL.
- **HI ratio.** Non-load-bearing, both FORMAL and TESTED.
- **FS bracket.** h0/2, h0 and 1.05·h0 are bitwise as stated.
- **Template mapping.** The mapping from the seed is bitwise as stated.
- **`k_domain.length_kpc` 272.97.** The field exists, and the check passes on all grids.
- **`max_iterations` 16.** This is clearly marked as an addition to 0473 with its reason. It is in the 33-key identity.
- **Labels.** All UNTESTED items carry a deciding test, and none is presented as a null.

## 5. Files (sha256 from bytes)

| File | sha256 |
|---|---|
| `check_v001/check_ngc_options_v001.py` | `03994148cf2a168089b707a1ac0188a8d85ddff282eb6750dd5ca822fe2fb8fa` |
| `check_v001/CHECK_FACTS_V001.json` | `8a3a3d399ae512d9a1a42328cab165e277c74d279f55ab48d8fb0df617adda09` |
| `check_v001/check_m2_feasibility_v001.py` | `f22f3a3c8fc3bfe1154c11ce429051efac305af6ebe83d3f2def7f06e4e99685` |
| `check_v001/CHECK_M2_FEASIBILITY_V001.json` | `18cc3638bbec7c4d8c6036176825a29c463e6ee9ca97bdeefd89309417e11599` |
| `check_v001/rerun/ngc_options_facts_v001.py` (byte copy) | `9e65bd0f4ce537464c483918f932bf96c91364f73bcc42cef20836f3c16297af` |
| `check_v001/rerun/NGC_OPTIONS_FACTS_V001.json` (rerun output) | `8ba60ee7fe1cc25c4e95b8ffa26dffd88548345244c2f2f4ec6797b0eb44188e` |
