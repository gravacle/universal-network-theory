# REVIEW 0458 MATH V001: exact grouped density Fourier regrouping

**Role:** distinct reviewer, not author (MATH/EXACTNESS lens). I wrote neither the module nor the fixtures and did not read the other reviewer's review.

**Verdict: PASS_WITH_NOTES.** There are no blocking issues.

The regrouping is an exact finite-sum identity for the 0445 law. On this host every per-term factor it uses (vertical phase, Bessel value and argument, angular phase, k_perp, alpha) is bit-identical to the one 0445 forms for the same (wave, q). Only the summation order differs. Against my own exact rational oracle, 0458 is as accurate as the pinned 0445: worst 2.3e-16 against 2.6e-16, both relative to the per-wave bound B_k. Every scaling formula I checked by counting matches.

This review is UNTESTED at root scale and on root geometry. The deciding test remains root's comparison against the saved actual 0445 output.

## Hashes (sha256 computed from bytes, before and after all runs)

| File | sha256 |
|---|---|
| Task 0458 `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0458_2026-10-16_claude2_exact_grouped_density_fourier.md` | `18eb2dba463378903a952fd408d1f3b8a5cff9fc9be1b580921cbab9c1e51fdf` (match) |
| 0445 contraction `.../nonzero_density_fourier_0445/nonzero_density_fourier_c2v001.py` | `255e09f4889b6ed470e3424d3a3c41f3a21c433f3095e04ea12af7a96bc5aaf4` (match) |
| Jn provider `.../nonzero_density_fourier_0445/posix_libm_bessel_jn_provider_c2v001.py` | `9ec3f1c9fb8afe1ffa4a2bb24df5daf4d2695aa51574984658cb753cfc304f67` (match) |
| 0455 pattern `.../exact_scalar_force_0455/exact_scalar_force_c2v001.py` | `0dab62be91cfd793949ef251aa3e731b4544e7131606599784762cb4101175ea` (match) |
| Module under review `grouped_density_fourier_c2v001.py` | `9db7efd1ef18927c5886ab9b28d4f72cae16770cb3d3b04f574237b006a4bcbe` (matches the author report) |
| `INTERFACE_0458_V001.md` | `74fc9b4a51076ffb9013cef6bb6ccbf5bc1425c990ccf8610129eab53f5c7f0d` (matches) |
| `fixtures_0458_c2v001.py` | `65ffda168ffb57fddb19ca9de0810e95ba794fb672d1e21300fa12ea5d71a7ba` (matches) |
| `CONVENTION` digest, recomputed from the loaded module | `da0e164a979b3706f79e92dbd85d07c81083ab3ebfa036b2689d853842b2df78` (matches INTERFACE L17) |

I modified no existing file. This review is the only file I wrote in the 0458 folder (exclusive create, noclobber). I read no project data, NPZ, raw samples or target data, imported no root worker and made no project run.

## Independent derivation (law and regrouping)

**Law.** Over phi of a real perturbation, ∫dφ e^{-i k_perp R cos(φ-α)} e^{±imφ} = 2π (-i)^m J_m(k_perp R) e^{±imα}, using J_{-m} = (-1)^m J_m. So a single (-i)^m multiplies both harmonics, both harmonics share the vertical factor e^{-i k_z z}, and there is no extra 2. This is 0445 L6-7 and module L13-14. The quadrature oracle in item 2 checks the law directly, with no Bessel function and no (-i)^m: it uses signed k_x and k_y in e^{-i k·x}.

**Regrouping.** J_m depends on (k, q) only through (k_perp, R), and E only through (k_z, z_q). For wave k in cell c_k = (z_k, p_k), with P_k = e^{imα_k}:

S_k = P_k Σ_r J(p_k, r) Σ_{q∈r} w_q ρ_q E(z_k, q) + conj(P_k) Σ_r J(p_k, r) Σ_{q∈r} w_q conj(ρ_q) E(z_k, q).

This holds exactly, because the R groups partition q. Both branches use the same E. The code matches this term by term:

| Step | Module lines |
|---|---|
| A = (w·ρ, w·conj ρ) | L798-801 |
| V[g] = Σ_{s∈g} A·E, one einsum per R group with assignment (no accumulation), so each slot is used once | L824-827 |
| T = Σ_r V[r,:,z]·J[p_c,r] | L853-855 |
| Per-wave gather with that wave's own P | L874-877 |
| `scale*(unit*acc)`, the same arithmetic order as 0445 L275, applied once | L879 |

Group values are bitwise members (`_group_exact`, L270-283). So kz_unique[idx(k)] has the same bits as k_z(k), and the same holds for k_perp and R. Each factor is therefore the identical floating-point expression of identical inputs.

**Accuracy.** The regrouping does not degrade conditioning. The first-order error of T is bounded by u·(n_r + n_R + O(1))·Σ_q |w J ρ|, which is the same B_k scale as 0445's u·(nq + O(1))·B_k. Here n_r is the size of the largest R group and u = 2^-53. Since n_r,max + n_R ≤ nq + 1, the 0458 envelope is never wider than 0445's.

## What was executed

Everything below ran in `/private/tmp/claude-501/-Users-bgm-MB-Work/573ea246-f21c-48d3-b8cc-d28a1f8b2c42/scratchpad/r0458/REVIEW_0458_MATH_V001` with the root interpreter `/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -I -B` (Python 3.12.14, NumPy 2.3.5, arm64). The thread environment was VECLIB_MAXIMUM_THREADS = OPENBLAS_NUM_THREADS = OMP_NUM_THREADS = MKL_NUM_THREADS = 1. All inputs were synthetic.

The pinned 0445 module and provider were loaded from hash-verified bytes and used only as an oracle, with the provider unchanged (`create_jn_provider(library_policy='posix_find_library_m', expected_library_path=None, max_cache_entries=0)`, status READY).

| File | sha256 | Result |
|---|---|---|
| `fixture_run.txt` (fixture script, full run) | `adb5a9489637664b3629c052f021e66f83c803ebed475f7dfd5abebe1e6130ae` | PASS 23, INFO 2, FAIL 0, 4.0 s |
| `fixture_run_results.json` | `bcba026949754561ee3e93f9673183455bc9f025ef1ba70afa4940265624572d` | (same run) |
| `review_math_0458.py` (my oracles and checks) | `7975d680eca1439e9104f6ad37d21b1b5b599b6069878ab53f91dbad05eeb29e` | |
| `review_run_v2.txt` (final run of the above) | `d7aa431e8d1faa303ee0125c732e38094f2eb9e51fff6bfe04ed09a1b9250b4d` | 0 FAIL, 7.9 s |
| `review_math_0458_supp.py` (memory, structure, c-scaling, root arithmetic) | `4de4d4a19bc9ff4076334742fabcaf5300be5228b41d5d58bede1c3b019f11d8` | |
| `review_supp_run.txt` | `911d459f15d43120ef00dbd100ee190a0336e1aaf2bde782909d9ecf2204e777` | 0 FAIL |
| `zero_sign_check.py` / `zero_sign_run.txt` | `13f3cb7adac714932841f6dc9c57f27fac6ab7face8b043404ca76e05f8dd5f7` / `c39dc30be68905c1a1fa87c7c4d917c2a0b566f437c7071743d8383e1873a1ec` | informational |
| `review_run_v1.txt` (first run, superseded) | `170f2207ec7b06f1d4cb92dc94afe2673444c4be8e5a7dd70cc51c21713abdb6` | two FAILs, both errors in my harness (below) |

The v1 run had two errors in my own harness, and both were fixed before v2:

1. The quadrature oracle was normalized by B_k, which is exactly 0 at k_perp = 0 (and tiny for a single high-m term). It is now normalized by |c²2π| Σ w·2|ρ|.
2. My counting wrapper was bound at prepare, but evaluation was called with the bare provider, so `INVALID_INPUT` was returned as designed.

### My oracles (written by me)

- **X, exact.** A `fractions.Fraction` evaluation of the 0445 finite law, given the per-term float64 factors. The factors are w, J_m from the provider called row by row (a different call layout from both modules), exp(-i k_z z), exp(i m α), ρ and the float prefactor. This is the order-free value that both implementations round.
- **F, fsum.** A `math.fsum` direct sum, used for the q = 2000 case.
- **Q, quadrature.** An azimuthal trapezoid of e^{-i(k_x R cos φ + k_y R sin φ)}[ρ e^{imφ} + conj(ρ) e^{-imφ}], with N = 2(max k_perp R + m) + 96 nodes. It uses no Bessel function, no α and no (-i)^m.

Errors are normalized per wave by B_k = |c²2π| Σ_q |w_q J_m| 2|ρ_q|.

### Results (m = 1..6 throughout unless stated)

1. **Factor and argument bitwise identity.** This was tested on three fixtures: irregular, random (q = 300, nk = 120) and SI galaxy-scale.
   - For every (wave, q), the geometry's E, J_m, P, Bessel argument k_perp·R, k_perp, α and k_z/R group values are bitwise equal to the 0445-defined factors.
   - I recorded the provider argument sets from the pinned 0445 run and from 0458's prepare. The distinct (order, argument-bit) sets are identical (43, 561 and 34 per order), with the same zero-argument patterns. The provider checks at L253-267 are character-for-character the 0445 checks at L128-141.
   - 0458 makes 18, 30 and 12 provider calls, against 1632, 18000 and 1104 for 0445.
2. **Equivalence with the exact oracle.**

   | Case | 0458 vs X | 0445 vs X | 0458 vs 0445 | Q (quadrature) |
   |---|---|---|---|---|
   | Irregular: q = 61 with 7 R values (incl. 1-ulp R, exact duplicate q, z = ±0, mixed z/w inside R groups); nk = 49 (duplicates, holes 17/77, equal k_perp at 5 different α, k_z = ±0 and 1-ulp k_z, 5 k_perp = 0 signed-zero waves) | 1.56e-16 | 1.74e-16 | 3.1e-16 | 1.6e-16 |
   | SI galaxy-scale (R ~ kpc, ρ ~ 1e-21, c = 2.998e8) | 6.6e-17 | 7.7e-17 | — | 1.0e-16 |
   | Random q = 300, nk = 120 | 2.3e-16 | 2.6e-16 | — | — |
   | q = 2000, nk = 400 (against F) | 8.2e-17 | 2.1e-16 | — | — |
   | All-distinct R and k (nr = nq, nz = np = nk) | 1.7e-16 | 1.4e-16 | — | — |
   | q = 1, nk = 1 | 1.5e-16 | — | — | 1.7e-16 |

   - k_perp = 0 outputs are exactly 0. Their sign bits equal 0445's in 30 of 30 cases, and 48 of 294 outputs are fully bitwise equal.
   - Outputs are bitwise invariant across (wave_chunk, position_chunk) of (5,3), (1,1), (999,999), (7,13), (64,100) and (400,1).
3. **Real-linearity, complex-linearity, branch isolation and rotation** (all values normalized by B_k).

   | Check | Result |
   |---|---|
   | Real-linearity | ≤ 1.9e-16 |
   | Complex-linearity violated | \|F(iρ) − iF(ρ)\| between 0.40 and 0.68, so F is not complex-linear |
   | Plus branch, (F(ρ) − iF(iρ))/2, against my one-branch sum | ≤ 1.3e-16 |
   | Minus branch, (F(ρ) + iF(iρ))/2, against conj(ρ)·conj(P) with the same E | ≤ 1.1e-16 |
   | Distance of the minus branch from a conjugated-E minus branch | 0.37–0.58 |
   | Closed form for ρ = e^{iθ} r (θ ∈ {0, π/2, −2.2, π, 0.9}): 2 S Σ w J E r cos(mα + θ) | ≤ 8.8e-16 |

4. **Wrong-law sensitivity**, computed with my exact oracle. Minimum normalized distance of the 0458 output from each wrong law:

   | Wrong law | Distance |
   |---|---|
   | Conjugated E on the minus branch | 0.37 |
   | Extra factor 2 | 0.30 |
   | (+i)^m (odd m) | 0.60 |
   | Minus branch dropped | 0.20 |
   | α → \|α\| (angle symmetry) | 0.19 |
   | Order m−1 | 0.25 |

5. **Every q exactly once.** Each of the 61 single-q sources (including an exact-duplicate q, 1-ulp R and z = ±0), for m ∈ {1, 4}, matches its exact single-term value to ≤ 3.6e-16. The superposition of the single-q outputs matches the all-q output to 3.1e-16.
6. **A/B/A.** A is reproduced bitwise. B on the reused geometry is bitwise equal to B on a fresh geometry. All geometry arrays are byte-unchanged after the runs.
7. **Extreme magnitudes.**
   - Dynamic range \|ρ\| from 1e-130 to 1e100 with w·e^{±60}: 0458 vs X 1.9e-16, 0445 vs X 2.5e-16.
   - Subnormal-range terms: absolute error of 33 subnormal units for 0458 and 37 for 0445. Both underflow silently.
   - Overflow-edge status divergence in both directions (note N1).
8. **Scaling by counting.** I wrapped `np.einsum` and the provider, compared the geometry arrays' sizes, and measured with tracemalloc. Two cases were counted: irregular, and q = 2000 / nk = 400.
   - Group counts equal my own independent bit-unique counts.
   - E = nz·nq c128, J = nm·np·nr f64 and angular = nm·nk all match.
   - Map bytes 4105 and 66872, and digest bytes 21897 and 358792, are exactly the formula values.
   - Scatter: einsum calls = nr, and MACs = 2·nq·nz exactly (1342; 28000).
   - Cell sum: MACs = 2·nc·nr exactly (238; 8036), with calls 12 ≤ 19 and 35 ≤ 39.
   - Every einsum call had `optimize=False`.
   - Provider calls equal nm·ceil(np/pp), and provider elements equal nm·np·nr.
   - **Supplement** (nq = 60000, nk = 600, nr = 300, nz = 10, nc = 227):
     - The evaluate traced peak is 0.73× of 16·work + validation copies + blocks.
     - The prepare peak is 1.12× of caches + maps + maximum block + validation copies (note N4).
     - No geometry array reaches nq·nk.
     - c → 2c multiplies the output by exactly 4, bitwise, so the prefactor is applied once.
     - Structural maps are verified: wave → cell (own k_z and k_perp group), cells grouped by k_z with correct offsets, and position_order is a permutation.
     - The root-size arithmetic in INTERFACE L279-284 is correct: 5,971,968 B per k_z; 221,184 B; 1,495,296; 746,496; 859,963,392.
9. **Static checks.** In the module the only contractions are 2 `np.einsum(..., optimize=False)` calls (L827, L855). There is no BLAS product, errstate/seterr, warnings use, `.real`/`.imag` or `open`. This agrees with fixture T02.

## Blocking issues

None.

## Notes (non-blocking)

- **N1. Overflow-edge status parity is not guaranteed in either direction** (module L798-804, L827; INTERFACE L294-298). 0458 forms w·ρ and V without the J factor; 0445 forms w·J·E·bracket and 2|ρ| in its bracket. I demonstrated both directions:
  - **0458 refuses, 0445 completes:** with w·ρ ≈ 1e350 and J_6 ≈ 2e-59, 0458 gives FAILED_CLOSED at `source_weighting` (under errstate raise and ignore), while 0445 completes (2.5e-18 against X).
  - **0458 completes, 0445 refuses:** with \|ρ\| ≈ 1.2e308 and w ≈ 1e-12, 0445 gives FAILED_CLOSED at `azimuthal_bracket` (raise) or `position_sum` (ignore), while 0458 completes with 7.4e-17 against X.

  No wrong finite value is produced in either direction, and these magnitudes are far from the SI galaxy range (outputs ~1e57). INTERFACE item 5 only implies this. A future INTERFACE version should say plainly that FAILED_CLOSED vs COMPLETE parity with 0445 holds only away from the overflow edge.
- **N2. Root's comparison scale B_k is not exposed** (INTERFACE L387). Computing B_k densely costs as much as 0445. It is an exact grouped nonnegative sum, cheap from the geometry record:

  B_k = |-(c·c)·(2π)| · 2 · Σ_r |J_m(kperp_{p_k} R_r)| · Σ_{q∈r} w_q |ρ_q|

  using `bessel[slot]`, `position_order`, `r_offsets`, `weights_sorted` and `wave_perp_index`. Its first-order envelope is |Δ0458 − Δ0445| ≲ (2·nq + O(10))·u·B_k ≈ 8.3e-11·B_k at nq = 373248, worst case (computed). The observed values are ≤ 3.1e-16·B_k at q ≤ 2000 (measured).
- **N3. Operation labels** (module L342 and L344; INTERFACE L269 and L271). The MAC counts are exact. However, `np.einsum` casts the float64 J rows to complex128, and `np.multiply(w, ρ)` casts w, so the "complex-by-real" and "real-by-complex" stages run as complex×complex products: about 2× the label's real-flop cost for the cell stage. This does not affect memory limits or exactness.
- **N4. Prepare transients beyond the formulas** (module L493-521). The np.unique, argsort and bincount copies and the `np.unique(waves.view(uint64), axis=0)` row count are O(nq+nk) and not enumerated. They measured about 12% above the enumerated bytes at nq = 60000. INTERFACE L394 discloses the O(nk+nq) allocation before the limit check.
- **N5. Bitwise factor identity is empirical, not required for exactness** (INTERFACE L49). It holds here because the elementwise loops (hypot, arctan2, complex exp, products) are layout-independent on this host (NumPy 2.3.5, arm64). The regrouping's exactness holds to roundoff even if a factor differed by one ulp.
- **N6. The dense E cache can reach the forbidden table size** (module L554; INTERFACE L388). E is nq·nz, which tends to nq·nk (13.76 GB at root sizes) as nz → nk. `max_vertical_entries` is the guard; root sets it from the `prepare_geometry` counts.
- **N7. Outside the math lens: interrupt during COMPLETE packaging** (module L901 → L772-776; fixture T18c). An interrupt there loses the result without a retained record, as in 0445. I leave this to the contract review.
