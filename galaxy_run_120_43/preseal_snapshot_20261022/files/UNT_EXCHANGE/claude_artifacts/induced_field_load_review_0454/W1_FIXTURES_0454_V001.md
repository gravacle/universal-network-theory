# W1_FIXTURES_0454_V001: independent fixtures for the 0453 induced-field weak load

Helper **W1**, Claude4 independent review lane, 2026-10-16. Dispatch 0454 (`a6b544c8…f320fa`). Spec 0453 (`fbcda35f…2f0`). Pinned 0439 kernel `weak_euler_assembly_c3v001.py` (`8632bda6…13da`), whose `b` is at L307-323.

Scope: synthetic fixtures only. No project data, target data, validation outcomes, project calculation or physical acceptance. Claude3's files were read, never edited. The harness ran only on W1's byte-identical copy. Codex1 owns physics, launches and acceptance.

## W1 verdict (scope: this operation only)

The frozen Claude3 module `induced_field_weak_load_c3v001.py` (sha256 `7f68fba13d93d506b7d1db1e7818f247992d56bb7930190da7d6f3524f0cfb64`) shows **no defect**. Its copy is `W1_snapshot_7f68fba1/`, cmp-identical and set read-only (0444).

- **Checks:** 76/76 value checks pass and 28/28 fixture self-checks pass.
- **Probes:** 67 pass, 0 fail, 24 recorded.
- **Interpreters:** the verdicts and bitwise flags are identical under 3.12.14 / numpy 2.3.5 and 3.9.6 / numpy 2.0.2.
- **0439 equality:** `delta_b` is **bitwise identical** to the frozen 0439 `b` in 6/6 cross-check cases, under both interpreters.
- **Virtual work:** the real-virtual-work identity holds with error at most 9.8e-17 of its absolute-value bound.
- **Purity:** inputs were bitwise unchanged in every probe, including rejected calls. Outputs never alias inputs or each other. Each call returns fresh buffers.
- **Hygiene:** the module hash was unchanged after the runs, and no files (`__pycache__` included) were created.

Line notes, none of them defects:

- **L108-112:** `m` must be a Python `int`. `np.int64(3)`, `True` and `1.0` are rejected, matching the 0439 L183-187 precedent. Root must pass `int(m)`. The 0453 text does not fix the type.
- **L119:** `grad` is checked only as exactly `(n,3)`. When n == 3, a transposed `(3,n)` array is accepted silently and gives a different value (`grad_square_n3_transposed`). The same holds for maps when n == k. No shape check can detect this, so root must keep the orientation.
- **L136-153:** the operation sequence equals 0439 L313-322 with `f_c = grad[:, c]`, which is why the result is bitwise equal.
  - L150 `delta_b /= normalization_scale` is computed by numpy as a multiplication by `1/s`. This was verified on both numpy versions: 0 differences from `t*(1/s)`, and 19-56% of elements differ from exact `t/s` at the 1-ulp level. 0439 L322 does the same, so the two agree bitwise.
  - The W1 loop reference uses exact division and explicit sums. It agrees with the module to at most 4.6e-16 absolute (2.7e-17 of the bound), not bitwise, except in the dyadic H2 case, where it is bitwise.
- **L140-142:** a non-finite `w*rho*grad` operand is rejected even at points whose map rows are exactly zero. This matches 0439 L316-318.
- **L151-153:** the component loads are `-U_c^H(w rho g_c)/s`. Their sum equals `delta_b` to within 3.9e-17 of the bound; only the rounding order differs, as documented.

## 1. Operation

`delta_b = -(U_R^H(w*rho*g_R) + U_phi^H(w*rho*g_phi) + U_z^H(w*rho*g_z))/s`

- `w` = R dR dz, without 2π.
- `g` = `grad` (n,3) = `fft(field, axis=angles)[m]/16` per cylindrical component, with synthesis `exp(+i m phi)`.
- `g_phi` is already (1/R)∂_φδΦ.
- `m` (1..6) does not enter the formula.

`W1_reference_v001.py` implements this formula with explicit loops and Python complex scalars only: no matmul and no numpy reduction in the kernel. It also holds the mutants.

## 2. Virtual-work identities (the core fixture)

The fixture builds a **real** potential on synthetic points (R_p, z_p), with w_p = R_p dR_p dz_p and ρ_p > 0:

δΦ(R,φ,z) = Σ_{m'∈M} 2 Re[Φ_{m'}(R,z) e^{im'φ}], with M ⊂ {1..7} and Φ_{m'} = A R^p e^{-aR²+ibz}(1+cz²).

The analytic mode coefficients are G_R = ∂_RΦ, G_φ = (im'/R)Φ and G_z = ∂_zΦ, so each real component is g_c = Σ_{m'}(G_{c,m'} e^{im'φ} + c.c.). The fixture samples g_c on φ_j = 2πj/16 and takes root-style inputs `grad = fft(g, axis=angle)[m]/16`.

**Coefficient.** On 16 equispaced angles, (1/16)Σ_j e^{iqφ_j} = 1 if q ≡ 0 (mod 16) and 0 otherwise. For 1 ≤ m ≤ 6 and 1 ≤ m' ≤ 7, m' ≡ m only when m' = m, and −m' ≡ m is impossible because 2 ≤ m+m' ≤ 13. So FFT/16 bin m returns exactly G_{c,m}, the coefficient of e^{+imφ}, not 2G. This is checked against the analytic values (self-check).

**(a) Projection.** The direct angular integral is

−Σ_p w_pρ_p Σ_c conj(U_c[p,k]) (1/2π)Σ_j (2π/16) e^{−imφ_j} g_c(R_p,φ_j,z_p) = s·δb_k

The normalization (1/2π)(2π/16) = 1/16 is exactly the FFT/16 convention, so δb carries **no 2π**. Every m' ≠ m in the field drops out, which gives mode isolation. One case contains only off-target modes and must give δb ≈ 0.

**(b) Real virtual work.** Take a random complex y, the real displacement ξ = 2Re(U y e^{imφ}) and the real force F = −ρ∇δΦ. Then

W = Σ_p w_p Σ_j (2π/16) ξ·F = 4π Re(y^H (s·δb)).

Derivation, with a_c = (U_c y)(p):

1. ξ_c g_c = (a_c e^{imφ} + c.c.)(Σ G_{c,m'} e^{im'φ} + c.c.).
2. On 16 angles, the e^{±i(m+m')φ} terms vanish because 2 ≤ m+m' ≤ 13. This includes the m' = m cross terms **e^{±2imφ}**, since 2m ≤ 12 < 16. The 16-angle grid needs m, m' ≤ 7.
3. The e^{±i(m−m')φ} terms vanish unless m' = m, since |m−m'| ≤ 6.
4. What survives is a_c conj(G) + conj(a_c) G = 2Re(conj(a_c)G).
5. Hence Σ_j(2π/16) ξ_cF_c = −ρ·**2π**·**2**Re(conj(a_c)G_{c,m}), and summing over p, c and k gives 4πRe(y^H s δb).

The factor **2** comes from the two surviving conjugate cross terms of the real 2Re fields. The **2π** is the azimuthal integral, which is deliberately absent from w. Both belong to the real-field bookkeeping and must not appear in δb.

**(c) Reconstruction.** δb_k = [W(e_k) + i W(i e_k)]/(4π s). This recovers all of δb from real work alone.

**Caveat (0453/0454), illustrated and recorded only.**

- The projection is complex-linear in the supplied coefficient: |b(iG) − i b(G)|/|b(G)| = 0.0 exactly.
- The real chain y → ξ = 2Re(…) → real field → bin m is only real-linear in general. W1's toy example uses the field (1+ε cos 2mφ)ξ with m = 2. Then G = a + (ε/2)conj(a), self-checked to 2.4e-15. The measured |b(G(iy)) − i b(G(y))|/|b(G(y))| is 0.146 at ε = 0.3, and 1.2e-16 for C3 (2.0e-16 for the reference) at ε = 0, where a mode-diagonal real operator maps a e^{imφ} + c.c. to λa e^{imφ} + c.c.
- The real virtual work is likewise only real-linear in y.
- So complex-linearity of this projection does not certify complex-linearity of the coupled density, c.c. and field operator. Root keeps the iteration design.

## 3. Fixtures and tolerances

"bound" means a target-independent absolute-value bound: Σ_p|wρ|Σ_c|U_c||g_c|/s. The proj and vw families use the angular-field magnitude instead. RTOL = 1e-12.

| family | content | n | tolerance |
|---|---|---|---|
| fixture_selfcheck (target-independent) | central-difference check of the analytic gradient (h = 1e-5); FFT/16 equals the analytic coefficient; the direct DFT equals FFT/16; bin −m equals conj(bin m) | 28 | FD 1e-6·max\|g\|; others 1e-12·max\|g\| |
| hand | H1 (n=k=1, root dtypes) → −0.75−0.5i; H2 (n=k=2, general complex, dyadic) → [−4.375−0.5i, −3.125+0.21875i]; H3 (unit sign case) → −1 | 3 | **exact** (all arithmetic dyadic) |
| proj_direct | target·s against the direct 16-angle integral (a) | 7 | RTOL·bound |
| proj_coeff_consistency | target(analytic G) against target(FFT/16) | 7 | RTOL·bound/s |
| vw_random | W_real = 4πRe(y^H δb s) for 4 random complex y | 7 | RTOL·(Σ\|terms\| + 4πΣ\|y\|bound) |
| vw_reconstruct | δb from real work only (c) | 7 | as above, per element |
| ident | complex-linear in grad (α = 0.6−1.3i and α = i); conjugate-linear in maps; additive; ρ, w and s scaling; point and column permutation; m = 1..6 give the same δb; component additivity; bitwise determinism; real-dtype maps equal complex-dtype maps | 13 | 2-3·RTOL·bound |
| comp | single-map isolation (loop expectation) and cross-zero (exact 0) for R, φ and z | 6 | 2·RTOL·bound; exact 0 |
| loads | convention identification and sum = δb | 2 | 4·RTOL |
| formula / ref / x0439 | vectorized formula / W1 loop reference / frozen 0439 `b`, with the bitwise flag recorded | 9/9/6 | 4·RTOL·bound |

The potential cases are (id, n, k, m, maps, s):

- m1_general: 11, 4, 1, complex, 2.3
- m2_root: 9, 3, 2, root, 1.7
- m3_general: 8, 2, 3, complex, 3.1
- m4_root: 11, 4, 4, root, 0.37
- m5_root: 7, 5, 5, root, 0.81
- m6_general_k_gt_n: 5, 7, 6, complex, 5.9
- m3_offmode_only: 8, 3, 3, complex, 2.3, with M = {1,2,4,5,6,7}

All other cases use M = {1..7}. "Root" maps follow root's dtypes: real float64 U_R and U_z, and a purely imaginary complex128 U_phi.

## 4. Probe catalog (classified against the 0453 text)

**expected_reject.** Every one raised in both the W1 reference and C3: ValueError, or TypeError for the argument probes.

- **m:** 0, 7 and −1.
- **ρ and w:** a zero, negative, NaN or inf entry; a complex value with nonzero imaginary part; length n+1; shape (n,1).
- **grad:** (3,n) with n = 6; (n,2); (n,3,1); (n,4); flat (3n,); (n+1,3); a (16,n,3) angle array; NaN in the real part; NaN in the imaginary part; inf.
- **maps:** U_phi with k+1 columns; U_z with n+1 rows; 1-D U_R; all three maps 1-D; 3-D U_R; (k,n) U_R; NaN in U_phi; inf in U_z; NaN in the imaginary part of U_R.
- **s:** 0, −2.3, NaN, +inf, −inf and the string "2.3".
- **missing argument:** s, grad or m.
- **overflow:**
  - w·ρ = inf;
  - conj(U)·wρg overflows;
  - two finite terms sum to inf;
  - a non-finite operand at map rows that are exactly zero;
  - s = 5e-324 makes the quotient overflow.

**expected_accept.** All returned the correct value:

- the baseline case;
- m = 1..6;
- the non-contiguous grad view;
- n = 3 in the correct orientation;
- root dtypes (real U_R and U_z);
- all-real maps;
- Fortran-order maps;
- strided map views;
- read-only inputs.

The purity checks also pass: no output-to-input aliasing, fresh buffers on every call, bitwise-identical repeat calls, and an output shape of (k,).

**record_only** probes (0453 does not decide these; the 0439 precedent is given in each harness rationale):

| probe | W1 ref | C3 c3v001 |
|---|---|---|
| m = True / 1.0 | raise | raise |
| m = np.int64(3) | return (value ok) | **raise** (L108, Python int required) |
| ρ, w complex dtype with zero imaginary part | raise | raise |
| ρ, w integer dtype | return ok | return ok |
| ρ, w bool | raise | raise |
| grad real float64 | return ok | return ok |
| n = 3, grad transposed | return, value differs | return, value differs (cannot be detected) |
| maps integer / complex64 | return ok | return ok |
| maps bool | raise | raise |
| k = 0 / n = 0 | raise | raise |
| s = True / complex 2.3+0j / 0-d array | raise | raise |
| s = 2 / np.float64(2.3) | return ok | return ok |
| unknown keyword / all positional | TypeError | TypeError |
| outputs aliasing each other | none | none |

No Python warnings were emitted by C3 in any probe.

## 5. Mutation study (single changes to the W1 reference kernel)

Each mutant ran against 52 value checks (hand, proj, vw, ident, comp and loads). The formula/ref/x0439 families were excluded so that detection rests on the independent fixtures. The unmutated kernel produced 0/52 failures, so there were no false positives. **21/21 mutants were detected**, every one of them by both the direct projection and the real virtual work.

| mutation | failed checks | proj_direct and vw cases detecting | hand |
|---|---|---|---|
| missing conj (all maps) | 25/52 | all 6 | H1, H2 |
| missing conj, φ only | 23/52 | all 6 | H1, H2 |
| missing conj, R and z only | 14/52 | **general complex cases only** (m1, m3, m6) | H2 |
| conj on gradient instead of maps | 27/52 | all 6 | H1, H2 |
| extra conj on gradient | 26/52 | all 6 | H1, H2 |
| sign flipped | 24/52 | all 6 | H1-H3 |
| normalization omitted / applied twice | 24/52 / 25/52 | all 6 | H1, H2 |
| extra 2π / factor 2 | 25/52 each | all 6 | H1-H3 |
| extra 1/R on grad_phi / R×grad_phi | 22/52 each | all 6 | H1, H2 |
| R instead of 1 in the measure (w·R) | 25/52 | all 6 | H1-H3 |
| components swapped R↔z / φ↔R | 26/52 each | all 6 | H1-H3 |
| w omitted / ρ omitted | 25/52 each | all 6 | H1, H2 |
| (wρ)² | 25/52 | all 6 | H2 |
| output conjugated / real part only | 27/52 each | all 6 | H1, H2 |
| grad_phi × m | 19/52 | m2-m6 (m = 1 cannot detect it) | H2 |

"All 6" means the six potential cases m1-m6. The off-mode case gives δb ≈ 0 by construction.

**Lesson:** with root's real U_R/U_z, U^H and U^T coincide on R and z. A missing conjugation there is invisible to root-structured inputs, so general complex maps are required to test it.

## 6. Results

| run | checks | self-checks | probes pass / fail / recorded | mutations | worst err/bound (proj, vw) | 0439 bitwise |
|---|---|---|---|---|---|---|
| self (W1 reference, sha `4008cd46…af65`) | 76/76 | 28/28 | 67 / 0 / 24 | 21/21, 0 false positives | 1.6e-16, 9.8e-17 | H2 only (loops vs BLAS: ≤ 2.2e-16 abs) |
| C3 snapshot `7f68fba1` | 76/76 | 28/28 | 67 / 0 / 24 | n/a | 1.4e-16, 9.8e-17 | **6/6** |

Both interpreters produced identical summaries, per-check verdicts, bitwise flags and probe outcomes. The 3.9 outputs are scratch files that were compared only: `/private/tmp/claude-501/-Users-bgm-Research-UNT-EXCHANGE/d3eba6e0-d470-48a9-b17d-717c88261d09/scratchpad/W1_0454/W1_results_self_py39.json` and `/private/tmp/claude-501/-Users-bgm-Research-UNT-EXCHANGE/d3eba6e0-d470-48a9-b17d-717c88261d09/scratchpad/W1_0454/W1_results_c3_py39.json`.

The runtime is under 1 s per run.

## 7. Exact commands

```
P=/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3   # or /usr/bin/python3 (3.9.6; the harness appends the 3.9 user site-packages)
D=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/induced_field_load_review_0454
R0439=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/weak_euler_0439/weak_euler_assembly_c3v001.py
# self-run (reference + mutation study)
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 $P -I -B $D/W1_fixtures_v001.py \
  --module $D/W1_reference_v001.py --func induced_field_weak_load_reference \
  --ref0439 $R0439 --mutation-study --out $D/W1_results_self_v001.json
# Claude3 frozen module (W1 copy only)
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 $P -I -B $D/W1_fixtures_v001.py \
  --module $D/W1_snapshot_7f68fba1/induced_field_weak_load_c3v001.py --func induced_field_weak_load \
  --ref0439 $R0439 --out $D/W1_results_c3_v001.json
```

The harness maps target parameters by signature name matching, which was unambiguous for C3: `grad` maps to the canonical gradient and every other name is exact. An ambiguous signature writes an adapter description and exits with status 3 (`--adapter-module` protocol in the harness docstring). The exit status is 0 on a full pass.
