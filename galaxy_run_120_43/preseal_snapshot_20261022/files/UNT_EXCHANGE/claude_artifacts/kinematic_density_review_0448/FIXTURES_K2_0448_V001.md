# K2 implementation fixtures for 0448 (kinematic density map), V001

Claude4 review lane, local helper K2. This is a helper report, not an external-account response. Date 2026-10-16. Review only: no project module imported or run, and no galaxy data, solve outputs, target velocities or validation outcomes opened. Inputs are small analytic and random fixtures.

Root contract `KINEMATIC_DENSITY_COMPARISON_CHOICE_V001.json` (SHA256 `9e4c070e…e14d`, verified):
`Gkin = -rho[:,None]*divU - rho_R[:,None]*U_R - rho_z[:,None]*U_z`.

## Result for Claude3's module

Target: `kinematic_density_0447/kinematic_density_c3v001.py`, SHA256 `a8b2d578fbb0c41a02dac6a5fcfb3e5333ef3a998090cc1fc97c1117b1aaea22`. The harness ran only on the byte-identical copy `c3_snapshot_a8b2d578/kinematic_density_c3v001.py` (cmp-verified; the harness re-checks byte identity).

- **Results.** The two interpreters agree exactly: Python 3.12.14 with numpy 2.3.5, and Python 3.9.6 with numpy 2.0.2. Statuses, probe outcomes and output digests are all identical. Totals: 88 passed, 1 failed (P53), 14 recorded.
- **A1–A3.** All pass. On every case that records an output digest (12 of 12: A1 G+, G−, P, H, EOS; A2 six random cases plus root-structured), the module's output is **bitwise identical** to the independent K2 loop reference. The A1 error against the analytic −div(ρξ) is at most 2.9e-16, scaled. The module also does the following:
  - Gives an exactly real Gkin on the root-structured helicity inputs.
  - Gives byte-identical output for real-dtype and complex128 copies of the same maps. The lossless cast happens before the arithmetic.
  - Does not mutate or alias its inputs, and accepts read-only, strided and Fortran-ordered inputs.
- **A4.** 44 of 45 reject probes and 11 of 11 accept probes behave as expected. Each overflow probe (P63–P65) fails closed with a `ValueError` (lines 98–106).
- **Defect (non-blocking): P53, an int64 map holding 2**53+1, is accepted.**
  - Lines 72 and 78 accept kinds `"i"` and `"u"`. Line 65, `a.astype(dtype, copy=False)`, then rounds 9007199254740993 to 9007199254740992. I confirmed that rounding with numpy alone, without running the module.
  - This contradicts 0447 ("cast maps losslessly to complex128") and the module's own docstring at line 30. Vectors have the same issue, via line 72 to float64.
  - Related, platform-dependent: kinds `"f"`/`"c"` admit longdouble/clongdouble. That is lossless on this machine (itemsize 8, P60) but lossy where longdouble is 80-bit.
  - No effect on root's actual maps, which are float64/complex128.
  - Fix options: drop `"i","u"` at lines 72 and 78. Or reject integer input with max|v| > 2**53, and reject `"f"` itemsize > 8 or `"c"` itemsize > 16.
- **Blocking corrections from K2 fixtures: none.**

## Reference self-run

`fixture_results_k2v001_reference.json`: 50 passed, 0 failed and 70 recorded on both interpreters, with identical results. A1–A3 pass, and the loop reference equals the vectorized contract literal exactly (A2 scaled error 0.0). All 17 mutants are detected. A4 is recorded only, because the reference deliberately has no validation.

## Run commands (each well under one second)

```
D=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/kinematic_density_review_0448
PY=/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
cd $D
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 $PY -I -B $D/fixtures_kinematic_k2v001.py \
  --reference-run --interpreters "$PY,/usr/bin/python3" --out $D/fixture_results_k2v001_reference.json
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 $PY -I -B $D/fixtures_kinematic_k2v001.py \
  --module $D/c3_snapshot_a8b2d578/kinematic_density_c3v001.py --func kinematic_density_map \
  --source-of-copy /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/kinematic_density_0447/kinematic_density_c3v001.py \
  --interpreters "$PY,/usr/bin/python3" --out $D/fixture_results_k2v001_c3.json
```

How it runs:
- The parent re-executes the harness under each interpreter with `-I -B` and the single-thread environment. Each child writes JSON to stdout, so no temp files are created.
- Omit `--interpreters` for a single run.
- Exit status is 0 only if every scored item passes. Here the reference run exits 0 and the c3 run exits 1 (P53).
- The target is loaded by file path with importlib, with `sys.dont_write_bytecode=True`. No `__pycache__` was produced.

## A1: analytic −div(ρξ) on nonconstant densities

For an axisymmetric ρ(R,z) and ξ ∝ e^{+imφ}:
div(ρξ) = R⁻¹∂_R(RρξR) + (im/R)ρξφ + ∂_z(ρξz) = ρ·divU + ρ_R U_R + ρ_z U_z,
with divU = ∂_R U_R + U_R/R + imU_φ/R + ∂_z U_z. The φ term enters only through divU, because ρ has no φ-gradient. Every case uses 17 scattered points and 6 independent ξ columns with m = 1…6. The expected value comes from a **product route** that never uses ρ_R, ρ_z or divU.

- **G± (Gaussian column).**
  - Density: ρ = ρ₀(1+aR²)e^{−z²/h²}, with ρ₀ = 1.3 and h = 0.8. G+ uses a = 0.45; G− uses a = −0.2, so ρ_R < 0.
  - Gradients: ρ_R = 2aRρ₀e^{−z²/h²} and ρ_z = −(2z/h²)ρ.
  - Displacement: each ξ component is a sum of terms T = cRⁿz^l·exp(−βz²+iκR), with complex c and β (Re β > 0) and n ∈ {0, ½, 1, 3/2, 2}. Derivatives: ∂_R T = T(n/R+iκ) and ∂_z T = cRⁿe^{…}(l z^{l−1} − 2βz^{l+1}).
  - Product route: RρξR and ρξz expand into terms of the same class (coefficients multiply, exponents add, the R power rises by one), which are then differentiated term by term.
- **P (polytrope-like column, complex ξ) and H (helicity structure).**
  - Density: ρ = ρ_c(R)q^{3/2}, with ρ_c = 2e^{−R/1.1}, q = 1−ζ², ζ = z/H, H = 0.35(1+0.4R) and |ζ| ≤ 0.85.
  - Gradients: ρ_R = −(ρ_c/R_d)q^{3/2} + 3ρ_c q^{1/2}ζ²H′/H and ρ_z = −3ρ_c q^{1/2}ζ/H.
  - Displacement: ξ_c = a_cR^{n_c}e^{iκ_cR}Π_c(ζ), with cubic Π_c.
  - Chain rule at fixed z: ∂_R = ∂_R|_ζ − ζ(H′/H)∂_ζ and ∂_z = H⁻¹∂_ζ.
  - Product route: RρξR = a(R)Q(ζ), with a = a_Rρ₀R^{n+1}e^{(iκ−1/R_d)R} and Q = q^{3/2}Π_R. Then ∂_R(RρξR) = a′Q − aQ′ζH′/H, with Q′ = −3ζq^{1/2}Π_R + q^{3/2}Π_R′, and ∂_z(ρξz) = c_z(R)Q_z′/H.
  - Case H uses real a_R, a_z and Π, imaginary a_φ, and κ = 0. That gives float64 U_R and U_z, imaginary U_φ, and a real-valued complex128 divU (exactness asserted). The target's imaginary part must be exactly 0.
- **Fixture validation** (independent of the target, tolerance 1e-8):
  - Fourth-order central finite differences of the closed-form ρ and ξ, and of the products RρξR and ρξz in cylindrical form.
  - A Cartesian finite-difference divergence of ρξe^{imφ} at φ₀ = 0.7 and 2.3. This checks the +U_R/R term and the e^{+imφ} sign.
  - Maximum deviation is 8.4e-11. The identity expansion matches the product route to ≤ 2.9e-16 (scaled).
- **EOS case.**
  - Gradients come from the provider relation (lines 44–46, transcribed): ρ_R = (P_R − ρ^{5/3}K_R)/((5/3)P/ρ) and ρ_z = P_z/((5/3)P/ρ). Here K = 0.7(1+0.3R), K_R = K·logK_R and P = Kρ^{5/3}, with P_R and P_z exact derivatives.
  - The round trip reproduces ρ_R and ρ_z to 2.8e-16, and Gkin then matches −div(ρξ) to 1.9e-16.
  - Lagged pressure data P_R(1+1e-3) and P_z(1−2e-3) change Gkin by exactly −Δρ_R U_R − Δρ_z U_z (7.9e-17 scaled). Gkin then departs from −div(ρξ) by 1.1e-3 relative.
  - **Scope:** Gkin realizes −div(ρξ) only to the extent that the supplied ρ_R and ρ_z are gradients of the supplied ρ.
  - K2 does not address agreement between the pointwise identity and the quadrature/weak form; that is K1's question.

## A2 and A3

- **A2.**
  - Random complex inputs in shapes 7×3, square 5×5 and 1×1, nfree = 1 (9×1), npoints = 1 (1×4), and an 8×6 case spanning 10^±6. Tolerance is 1e-14 relative to |ρ||divU| + |ρ_R||U_R| + |ρ_z||U_z|.
  - A root-structured case must give an exactly real output.
  - Byte-identity checks: float64 versus complex128 U_R/U_z; float64 versus complex128 divU; complex64 and float32 maps versus their complex128 casts.
- **A3.**
  - Exact signature `(*, rho, rho_R, rho_z, U_R, U_z, divU)`, with no defaults and no U_φ, m or R parameter.
  - Output is complex128 with the shape of U_R.
  - Linearity at 1e-13. Exact power-of-two homogeneity in the maps and the vectors. f(iX) = i·f(X); a conjugating implementation gives −i·f(X).
  - Exact column-subset and row-subset independence.
  - No mutation (byte snapshots) and no output aliasing (`np.shares_memory`).
  - Accepts read-only, strided and Fortran-ordered inputs. Results are deterministic.

## A4 probe catalogue

Expected outcomes and their basis in the contract or 0447 text:

- **Reject (45 probes).**
  - Calling convention (signature, no hidden defaults; no phi term a second time): missing kwarg (P01, P02), positional call (P03), extra U_phi (P04) or m (P05).
  - Vector shape ("consistent shapes"): wrong length (P06–P08), broadcastable (1,) (P09), 2-D (P10, P11), 0-D (P12).
  - Vector values ("finite real vectors"): nan or inf (P13–P16), complex with nonzero imaginary part (P17, P18).
  - Positive ρ: ρ = +0.0, −0.0 or negative (P21–P23).
  - Non-real vector dtype: object (P31), string (P32).
  - Map shape: wrong npoints (P34–P37), wrong nfree (P38, P39), broadcastable (n,1) or (1,nfree) (P40, P41), 1-D (P42, P43), 3-D (P44).
  - Map values ("finite maps"): nan or inf, including imaginary-only (P45–P48).
  - Non-real map dtype: object (P50), string (P51).
  - Lossless cast: int64 holding 2**53+1 (P53).
  - Non-finite output: overflow in one product, in the sum only, or in the imaginary part only (P63–P65).
  - Non-finite vector: ρ_R = inf against a zero U_R row (P68).
- **Accept (11 probes).**
  - ρ = 1e-300 (P24).
  - All-negative ρ_R or ρ_z (P25, P26), and ρ_R = ρ_z = 0 (P27): gradients may have either sign.
  - complex64, float32 and float16 maps (P54–P56); the root-structured dtypes (P57); float64 divU (P58).
  - A large but finite 1e300 product (P66) and subnormal output (P67).
  - Accepted values must also equal the reference.
- **Record only (12 probes; the contract is silent).**
  - Vectors: complex with zero imaginary part (P19, P20), int64 (P28), float32 (P29), bool (P30), Python lists (P33).
  - Maps: bool (P49; rejection preferred), small int64 (P52), nested lists (P59), longdouble (P60).
  - npoints = 0 (P61) and nfree = 0 (P62).
  - Claude3's module rejects bool, complex vectors and empty dimensions. It accepts integers, float32, lists and longdouble (itemsize 8).

## A5 mutation table (all detected in the reference self-run)

| id | mutation | detected by (main groups) |
|---|---|---|
| M01–M03 | sign of each of the three terms flipped | A1 all cases, A2 |
| M04 | ρ missing on divU | A1, A2 |
| M05 | ρ_R and ρ_z swapped | A1, A2 |
| M06 | duplicate φ term −ρ·imU_φ/R (in A1 the actual φ part; elsewhere a synthetic array) | A1, A2. A real duplicate is structurally impossible: the signature has no U_φ, and P04 confirms U_phi is rejected |
| M07 | duplicate cylindrical term −ρU_R/R | A1, A2 |
| M08 / M09 | extra R on ρ_R·U_R / extra 1/R on ρ·divU | A1, A2 |
| M10 | conjugated maps | complex A1/A2 cases, A3 linearity. Not visible on the real case H, as expected |
| M11 | vectors broadcast without `[:,None]` | broadcast `ValueError` on non-square inputs; wrong values in square 5×5; (n,n) output when nfree = 1 |
| M12 | real part only | complex A1/A2 cases |
| M13 | transposed output | shape checks |
| M14 | in-place write into the divU input | A3 mutation/aliasing and read-only checks; A2 casts |
| M15 / M16 | ρ_R used on U_z / ρ_z term dropped | A1, A2 |
| M17 | complex64 precision | A1, A2 |

## Limits

- Results apply to snapshot `a8b2d578…` only; a revised module needs a rerun with the second command.
- The finite-difference checks validate the fixtures; they are not target tests.
- Physical acceptance, the weak/quadrature comparison and root's project calculation are outside K2.
