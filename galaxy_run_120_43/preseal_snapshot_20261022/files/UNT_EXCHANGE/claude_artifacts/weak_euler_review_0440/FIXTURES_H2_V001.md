# FIXTURES_H2_V001: manufactured cases and failure behavior for the 0439 weak Euler assembly

This file belongs to the Claude4 review lane (dispatch 0440, amended by 0441). It was written by **helper H2**, a local helper inside the Claude4 lane, not an external account. H2's assignment is independent manufactured cases and failure behavior. Algebra and sign review belongs to helper H1, and the consolidated verdict belongs to the Claude4 lead.

- **Date:** 2026-10-16.
- **Status:** every result here is implementation-conformance evidence on synthetic arrays only. It is not a physical verdict (`not_assessed` physically).
- **What was not touched:** no project data, project module, galaxy data, calibration/target velocity or validation outcome was opened, and no project calculation was launched.
- **Claude3's implementation:** H2 did not inspect or run `weak_euler_assembly_c3v001.py`. Section 9 gives the command for running these fixtures against it.

## Pinned sources (read only)

| Source | SHA256 (`shasum -a 256`, 2026-10-16) |
|---|---|
| Root contract `.../CODEX1/ADDITIONAL_CLAUDE_WEAK_EULER_TASKS_V001.json` | `5c30449de636b1f3da751d07ad90caafe964ed19444b0648df8fd9726ade9ebe` (matches pin) |
| Prior weak contraction `.../helpers/coefficient_method/owned_nonzero_modal_weak_adjustment_v002.py` | `5cae4ee994f1ca07fdf703af529e7f5df9df2c2ed642d478df89beb692a25c51` (matches pin) |
| Helicity maps `.../helpers/coefficient_method/owned_32q8_regular_helicity_maps_v001.py` | `280149dc028260d865604948633bb8a1332c5ee01be916895c02df42e2b280c6` (matches pin) |
| Dispatch `FROM_CODEX/0438_2026-10-16_claude_free_surface_density_projection.md` | `83c963759f875285ce0b33148de1684318cbb81aa4658e1128bede3fe76a5c4c` (observed; no pin given) |

The harness hashes the contract again on every run. Both result files record `meta.contract_hash_verified = true`.

## H2 files (exclusive)

| File | SHA256 | Role |
|---|---|---|
| `reference_weak_euler_h2v001.py` | `61f1982cbb48a25e1bd1a50afa13c217eb0b77bb905e7db5b19511c714b2a4ac` | Loop reference transcription with no validation |
| `fixtures_weak_euler_h2v001.py` | `a958ecb83279bb4fa069786d0741c13e6ba757a39b6e85e5efe1a86567f8cda7` | Harness F0-F7 and CLI |
| `fixture_results_h2v001_reference.json` | `296fd463ded48dc62f5b425d58e3fde52cc2e12a823f8e1dcfbae9a900d0d51d` | F0-F5 run on the reference, plus the F6 harness self-test |
| `fixture_results_h2v001_mutations.json` | `74261329bd8879704f1b5f7ad7c50d00f1db7568bf19335f0eb035fd854cff99` | F7 control and 27 mutants |
| `FIXTURES_H2_V001.md` | this file; its hash is reported in the H2 return | |

Both result JSONs are deterministic: fixed seeds, no timestamps. Regenerating them in memory reproduced both saved files byte for byte.

## 1. Contract equations as transcribed

Source: `author_task.equations`, with the unicode minus normalized to ASCII. `vw` abbreviates `volume_weights`.

```
E  = -K_R[:,None]*U_R - K_z[:,None]*U_z
PM = (gamma*P/rho)[:,None]*G + rho[:,None]**gamma*E          ('**' binds before '*')
VR = i*m*Omega[:,None]*U_R
VP = -(R*Omega_R)[:,None]*U_R + i*m*Omega[:,None]*U_phi - (R*Omega_z)[:,None]*U_z
VZ = i*m*Omega[:,None]*U_z
AR = i*m*Omega[:,None]*VR - 2*Omega[:,None]*VP
AP = i*m*Omega[:,None]*VP + (2*Omega+R*Omega_R)[:,None]*VR + (R*Omega_z)[:,None]*VZ
AZ = i*m*Omega[:,None]*VZ
A  = U_R^H diag(vw*rho) AR + U_phi^H diag(vw*rho) AP + U_z^H diag(vw*rho) AZ
     - divU^H diag(vw) PM - [U_R^H diag(vw*P_R/rho) + U_z^H diag(vw*P_z/rho)] G
b  = -U_R^H(vw*rho*f_R) - U_phi^H(vw*rho*f_phi) - U_z^H(vw*rho*f_z)
returned: A/normalization_scale, b/normalization_scale, unscaled E, PM, VR, VP, VZ
```

These lines match the pinned prior contraction (`owned_nonzero_modal_weak_adjustment_v002.py` L44-L58). The prior file builds its own G (L43) and its own forcing (L55-L57). In the new contract both are supplied inputs.

The reference (`reference_assemble(**canonical)`) uses explicit Python loops over point `p`, trial column `j` and test column `k` with Python complex scalars. It uses no broadcasting and no matrix products, and it does no validation. It returns the canonical dict plus `A_unscaled` and `b_unscaled`.

## 2. F0 hand case (npoints = 1, nfree = 1)

**Inputs:**
- Real vectors: R = 2, rho = 8, P = 12, K_R = 1, K_z = 3, P_R = 16, P_z = -24, Omega = 2, Omega_R = 1.5, Omega_z = -1, volume_weights = 0.5.
- Maps: U_R = 1+2i, U_phi = 2-i, U_z = -1+i, divU = 3-2i, G = 2+i.
- Forcing: f_R = 1-i, f_phi = 2i, f_z = -3+i.
- Scalars: m = 2, gamma = 5/3, normalization_scale = 4.

Every Omega, shear, K, P-gradient, G and forcing entry is nonzero, and the maps are complex. rho = 8 is chosen so that 1/rho, 1/rho^2 and rho^gamma differ; vw = 0.5 so that vw, vw^2 and 1 differ; m = 2 so that m and m^2 differ.

**Derived scalars:**

| Quantity | Value |
|---|---|
| i·m·Omega | 4i |
| R·Omega_R | 3 |
| R·Omega_z | -2 |
| 2·Omega + R·Omega_R | 7 |
| vw·rho | 4 |
| gamma·P/rho | 5/2 |
| rho^gamma = 8^(5/3) = 2^5 | 32 |
| vw·P_R/rho | 1 |
| vw·P_z/rho | -3/2 |

**Steps:**

1. E = -(1)(1+2i) - (3)(-1+i) = (-1-2i) + (3-3i) = **2 - 5i**
2. PM = (5/2)(2+i) + 32(2-5i) = (5+2.5i) + (64-160i) = **69 - 157.5i**
3. VR = 4i(1+2i) = **-8 + 4i**
4. VP = -3(1+2i) + 4i(2-i) - (-2)(-1+i) = (-3-6i) + (4+8i) + (-2+2i) = **-1 + 4i**
5. VZ = 4i(-1+i) = **-4 - 4i**
6. AR = 4i(-8+4i) - 2·2·(-1+4i) = (-16-32i) + (4-16i) = **-12 - 48i**
7. AP = 4i(-1+4i) + 7(-8+4i) + (-2)(-4-4i) = (-16-4i) + (-56+28i) + (8+8i) = **-64 + 32i**
8. AZ = 4i(-4-4i) = **16 - 16i**
9. The terms of A (unscaled):
   - T1 = conj(U_R)·vw·rho·AR = 4(1-2i)(-12-48i) = 4(-108-24i) = -432 - 96i
   - T2 = conj(U_phi)·vw·rho·AP = 4(2+i)(-64+32i) = 4(-160) = -640
   - T3 = conj(U_z)·vw·rho·AZ = 4(-1-i)(16-16i) = 4(-32) = -128
   - T4 = -conj(divU)·vw·PM = -0.5(3+2i)(69-157.5i) = -0.5(522-334.5i) = -261 + 167.25i
   - T5 = -[conj(U_R)·1 + conj(U_z)·(-3/2)]·G = -[(1-2i) + (1.5+1.5i)](2+i) = -(2.5-0.5i)(2+i) = -5.5 - 1.5i
   - **A_unscaled = -1466.5 + 69.75i**, so **A = A_unscaled/4 = -366.625 + 17.4375i**
10. The terms of b:
    - -4(1-2i)(1-i) = -4(-1-3i) = 4 + 12i
    - -4(2+i)(2i) = -4(-2+4i) = 8 - 16i
    - -4(-1-i)(-3+i) = -4(4+2i) = -16 - 8i
    - **b_unscaled = -4 - 12i**, so **b = -1 - 3i**

**How the hand values are checked:**
- The fixture hard-codes these values (`HAND_EXPECTED`, `HAND_INTERMEDIATE`).
- Check `F0_hand_values_exact_rational_selfcheck` recomputes all of them in exact `Fraction` complex arithmetic and found no mismatch. This check does not call the target.

**Floating-point note:** `8.0**(5/3)` evaluates to 32.00000000000001 because 5/3 is not exactly representable. As a result, the loop reference returns PM = 69.00000000000001 - 157.50000000000003i and Im A = 17.437500000000007. The F0 scale-aware error is 1.85e-16, against a tolerance of 1e-12.

## 3. Fixture list

All targets are called on private deep copies of the inputs. Every call made during F0-F5 is checked for in-place modification of its inputs.

- **F0 hand case:** one check of all seven outputs against the Section 2 values, plus the exact-rational self-check.
- **F1 loop-reference comparison:** 9 checks, one per shape and seed, each covering m = 1..6.
  - Shapes and seeds: non-square (7, 3) with seeds 11/12/13; square (4, 4) with seeds 21/22/23; tall (16, 5) with seeds 31/32/33.
  - Inputs: positive non-constant R, rho, P and vw; non-constant K, P-gradient and Omega vectors; Omega_R and Omega_z drawn from N(0, 0.5²), so both shears are nonzero; complex maps and forcing with independent N(0,1) real and imaginary parts; normalization_scale drawn from U(0.5, 4).
  - All of A, b, E, PM, VR, VP and VZ are compared with rtol 1e-12.
  - The square case exists to expose a missing `[:,None]`. With npoints = nfree, numpy broadcasts a point vector across columns instead of failing.
- **F2 term isolation:** seed 41, (5, 3), m = 3, ns = 1.6. Every term switch starts at zero and only the named terms are enabled. Each case is compared with its own separately written einsum expectation, covering all seven outputs.
  - a. Omega only, with the additional requirement that A is Hermitian.
  - b. Omega with Omega_R, also with A Hermitian.
  - c. Omega with Omega_z, the vertical shear alone.
  - d. P_R only, with divU = 0.
  - e. P_z only, with divU = 0.
  - f. K_R only.
  - g. K_z only.
  - h. K_R and K_z together.
  - i. G with P only.
  - j. All forcing.
  - k-m. f_R, f_phi and f_z each alone.
  - n and o. The radial- and vertical-shear contributions isolated by difference against case a.
- **F3 reference-free properties:** seed 61, (7, 3), m = 3, ns = 1.3. These checks use no reference.
  - **Global phase:** multiplying all five maps by e^{0.7i} leaves A invariant, sends b to e^{-0.7i}b, and multiplies every map by e^{0.7i}.
  - **Column phases** t = (0.3, -1.1, 2.0): A_kj picks up e^{i(t_j - t_k)}, b_k picks up e^{-i t_k}, and map column j picks up e^{i t_j}.
  - **Forcing:** b is linear in (f_R, f_phi, f_z) with complex alpha and beta. A and the maps do not depend on the forcing; this was also recorded bitwise.
  - **Volume weights:** scaling vw by c = 2 or 0.37 scales A and b by c and leaves the maps unchanged. For c = 2 the result was also recorded bitwise.
  - **Normalization:** multiplying ns by 3 divides A and b by 3 and leaves the maps unchanged.
  - **Dependence on m:**
    - The third difference of A over m = 1..4, 2..5 and 3..6 vanishes.
    - The second difference of A in m equals -2[U_R^H diag(vw rho Omega^2) U_R + U_phi^H(..)U_phi + U_z^H(..)U_z]/ns.
    - b does not depend on m.
    - E and PM do not depend on m.
    - VR and VZ are proportional to m, and VP is affine in m.
  - **Radial rescaling:** with R multiplied by c and both shears divided by c (c = 2 and 3), every output is unchanged.
- **F4 G verbatim, no input mutation, output form:** seed 71, (7, 3), m = 2, ns = 0.8. G is independent of divU; their normalized overlap is 0.133.
  - PM == (gamma P/rho) G + rho^gamma E, with the supplied G and the formula E.
  - A(G1) - A(G2) = -[divU^H diag(vw gamma P/rho) + U_R^H diag(vw P_R/rho) + U_z^H diag(vw P_z/rho)](G1-G2)/ns, and PM(G1) - PM(G2) = (gamma P/rho)(G1 - G2).
  - A(divU1) - A(divU2) = -(divU1 - divU2)^H diag(vw) PM/ns, with the maps and b unchanged.
  - Output types, shapes and complex dtype: A is (nfree, nfree), b is (nfree,), and each map is (npoints, nfree), all `ndarray`.
  - Inputs are bitwise unchanged across every call.
  - Record-only: output/input memory aliasing, returned key sets, and warnings raised during valid calls.
- **F5 no hidden forcing:** seed 81. With f_R = f_phi = f_z = 0, b must be **exactly** 0 (bitwise `== 0`, shape (nfree,)) for every m = 1..6, even though G, P, K, both P gradients, Omega and both shears are nonzero. A second case sets Omega = 0 while keeping P_R, P_z, K and G nonzero; b must also be exactly 0.
- **F6 malformed-input probes:** 218 probes; see Section 6. Each probe records:
  - its expectation and contract basis
  - whether the target accepted or rejected it, with exception type and message
  - a heuristic flag for incidental numpy/Python errors
  - any warnings
  - for accepted probes, finite-output status and agreement with the reference on the (coerced) inputs

  F6 does not run against the reference, which by design does no validation.
- **F7 mutation study:** `run_mutation_study`; see Section 7.

## 4. Tolerance rationale

- **Scale-aware error.** The error is `max|got - exp| / max(max|exp|, 1)`. A normwise scale avoids blow-ups on entries that are near zero because of cancellation. The floor of 1 matters only where the contract makes an output structurally zero, which happens in the F2 isolations; there it turns the comparison into an absolute 1e-12 test. All fixture inputs are O(1), so the floor never masks a nonzero discrepancy. The smallest discrepancy on any failing mutant check was 3.0e-3 (P_R/rho**2 in F0); 437 value-mismatch failures were observed across the mutants. That is more than nine orders of magnitude above the 1e-12 tolerance.
- **Why 1e-12.**
  - Each output entry is a sum of at most 16 points of products of at most about 6 factors, so the rounding bound is about (16 + 10)·eps times the summed magnitude.
  - Observed agreement:
    - The reference's largest error on any check was 3.6e-16.
    - The independent vectorized control agreed with the loop reference to at most 6.4e-16 over all F1 cases.
    - The F2 expectations agreed to at most 2.5e-16.
  - 1e-12 therefore leaves more than three orders of magnitude of margin for a BLAS-based implementation with a different summation order, and remains far below any genuine defect.
- **Difference checks** (F2n/F2o, F4 G/divU linearity, F3 m-differences) are scaled by the operands' magnitude, which is the rounding scale of a difference.
- **Exact criteria:**
  - F5 requires b exactly 0, since 0 times any finite value is exactly 0 in IEEE arithmetic.
  - F4 requires the inputs to be bitwise unchanged.
  - For c = 2 in the volume-weight and radial-rescaling checks, bitwise equality is recorded but not required. The reference achieved it.

## 5. Results

### Reference self-run

File: `fixture_results_h2v001_reference.json`.

- **F0-F5:** 46 passed, 0 failed, 0 errors. There are 2 record-only entries: no output/input aliasing, and returned keys A, A_unscaled, E, PM, VP, VR, VZ, b, b_unscaled.
- **F6:** skipped.
- **Inputs:** bitwise unchanged across all 95 calls.
- **F1:** compares the reference with itself here, so it passes trivially. The genuine checks in this run are F0, F2, F3, F4 and F5.

### F6 harness self-test

This is stored in the same file under `f6_harness_selftest`. It runs every probe against `_selftest_validating_reference`, a strict reading of the stated input rules wrapped around the reference. It is a harness self-test, not a proposed implementation.

- All 173 reject probes were rejected, none flagged incidental.
- All 16 accept probes were accepted, and their outputs matched the reference.
- The 29 record-only probes were recorded. The self-test validator accepted 14 and rejected 15; its choices for these probes are arbitrary.

This shows each reject probe is genuinely malformed and each accept probe is genuinely valid.

### Mutation control

File: `fixture_results_h2v001_mutations.json`. The control is an independent vectorized transcription (`_transcription`, with mutation=None). It passed every F0-F5 check, and its largest disagreement with the loop reference over F1 was 6.39e-16.

### Unsaved demonstration run

This run was not saved and is reproducible. The non-validating vectorized control was run through `run_all` with F6 enabled, behind a keyword-renaming tuple adapter.
- Of the 173 reject probes, 94 were silently accepted.
- The other 79 were rejected, and 52 of those were flagged as incidental numpy/Python errors.
- All 16 accept probes were accepted and matched the reference.

So F6 distinguishes deliberate validation from accidental failure, and the adapter path works, including the missing-kwarg, positional-call and unknown-kwarg probes.

## 6. F6 probe catalog

The full per-probe list, with basis, is in `fixture_results_h2v001_reference.json` under `f6_harness_selftest.checks`. `probe_catalog()` returns the same list.

**Pass rules:**
- **reject:** passes iff the call raises.
- **accept:** passes iff the call returns, all outputs are finite, and they match the loop reference within 1e-12.
- **record_only:** the outcome is recorded with no verdict. If the target accepted, agreement with the reference on the coerced inputs is also recorded.

Rejections whose messages look like incidental numpy/Python failures (broadcast, matmul or index errors, unsupported operands, ...) are listed in `f6_summary.rejections_flagged_incidental`. Such a call fails closed but did not validate. The lead should judge these from the recorded messages.

| Group | Probes | Expected | Basis |
|---|---|---|---|
| Accept | baseline; m = 1..6; Omega all negative; Omega all zero; no radial or vertical shear; K and P gradients zero; G zero map; divU zero map; all forcing zero; npoints = 1 with nfree = 1; nfree > npoints with (3, 5) maps (16 probes) | accept | Satisfies every stated requirement. Positivity is required only of R, rho, P and vw; zero is finite; the contract places no npoints/nfree ordering constraint, and the assembly does not solve. |
| Missing kwarg | Each of the 23 canonical inputs omitted | reject | 0439: all inputs are required keyword-only with no numerical defaults. Root JSON: no hidden callbacks/defaults. |
| Call form | Positional call; unknown extra kwarg | reject | Same as above. An unknown keyword must not be silently ignored. |
| m | 0, 7, -1, 1.0, 1.5, "1", None | reject | Root JSON: integer m in 1..6. |
| m | True; numpy.int64(2) | record_only | The contract is silent on bool and on numpy integer types. The pinned prior root code L18 (`type(m) is not int`) would reject both. |
| gamma | 1.4; 5/3 + 1e-12; nan; "5/3"; None | reject | gamma = 5/3 is supplied, and 0439 says to validate gamma = 5/3. For 5/3 + 1e-12 this is the strict-equality reading: no module-chosen tolerance. |
| gamma | numpy.float64(5/3) | record_only | The value is exactly 5/3; the contract is silent on scalar type. |
| normalization_scale | 0; -1; nan; inf; "1"; None | reject | Positive explicit scale required. inf would silently zero A and b, and the prior root code L60 rejects a nonfinite scale. |
| normalization_scale | True; int 2 | record_only | The contract is silent on bool and on scalar type. |
| provenance | ""; None | reject | Nonempty provenance required. |
| provenance | "   "; 123 | record_only | The contract is silent on whitespace and on type; the analogous 0438 contract says string. |
| Real vectors (each of 11) | Wrong length; 2-D column; 0-d scalar; nan; inf; complex dtype with nonzero imaginary part | reject | Required real finite vectors of shape (npoints,). A 0-d scalar would broadcast silently. |
| Real vectors (each of 11) | Complex dtype with exactly zero imaginary part | record_only | The values are real; the contract is silent on dtype. |
| Positivity (R, rho, P, vw) | One entry 0; all entries 0; one entry negative | reject | R, rho, P and vw must be positive. |
| R extras | Python list; int64 dtype; float32 dtype | record_only | The contract is silent on container type, dtype and precision. |
| Maps (each of 5) | Wrong npoints; mismatched nfree; 1-D; 3-D; nan in real part; nan in imaginary part; inf | reject | Required complex finite npoints x nfree maps with consistent shapes. |
| Maps (each of 5) | Real dtype | record_only | The contract is silent on dtype. |
| Forcing (each of 3) | Wrong length; 2-D column; 0-d scalar; nan; inf | reject | Required complex finite vectors of shape (npoints,). |
| Forcing (each of 3) | Real dtype | record_only | The contract is silent on dtype. |

Totals: 218 probes, of which 173 are reject, 16 accept and 29 record_only.

## 7. F7 mutation table

Each mutant is the vectorized control with one defect. F0-F5 ran on every mutant; F6 did not, because neither the control nor the mutants validate. All **27 of 27** mutants were detected, including all **17 of 17** required ones. "F1" means 9 of 9 F1 checks failed by value unless noted.

| Mutation | Category | Detected by (fixtures) | Discriminating checks beyond F0/F1 |
|---|---|---|---|
| U_phi^T instead of U_phi^H, AP test side | required | F0 F1 F2 F3 | F2a-c; F3 global phase; F3 column phases; F3 second difference in m |
| conj(AR) on the trial side | required | F0 F1 F2 F3 | F2a-c, n, o; F3 global phase; column phases; second difference |
| vw applied twice in the AZ term | required | F0 F1 F2 F3 | F2a-c; F3 vw x2 and x0.37; second difference |
| vw omitted in the divU pressure term | required | F0 F1 F2 F3 F4 | F2f-i; F3 vw scaling; F4 G and divU linearity |
| P_R/rho**2 | required | F0 F1 F2 F4 | F2d; F4 G linearity |
| Pressure-term sign flipped | required | F0 F1 F2 F4 | F2f-i; F4 G and divU linearity |
| G-term sign flipped | required | F0 F1 F2 F4 | F2d, F2e; F4 G linearity |
| 2·Omega·VP dropped from AR | required | F0 F1 F2 | F2a-c, n, o |
| R·Omega_R dropped from AP | required | F0 F1 F2 | F2b, F2n |
| R·Omega_z dropped from VP | required | F0 F1 F2 | F2c, F2o |
| Omega_R and Omega_z swapped | required | F0 F1 F2 | F2b, c, n, o |
| f_phi times an extra i·m/R | required | F0 F1 F2 F3 | F2j, F2l; F3 b independent of m; F3 R rescaling x2 and x3 |
| PM returned divided by ns | required | F0 F1 F2 F3 F4 | F2d-i; F3 ns scaling; F4 PM verbatim; F4 G linearity |
| E with column broadcasting (missing `[:,None]`) | required | F1 F2 F3 F4 F5 | Value mismatch only in F1 square (4, 4), all 3 seeds. 6 non-square F1 checks and 35 others raise broadcast errors. F0 (1x1) cannot see it. |
| b sign flipped | required | F0 F1 F2 | F2j-m |
| G replaced by vw·G | required | F0 F1 F2 F3 F4 | F2d, e, i; F3 vw scaling; F4 PM verbatim; F4 G and divU linearity |
| A replaced by (A + A^H)/2 | required | F0 F1 F2 F4 | F2c, d-i, o; F4 linearity. Not seen by F2a/b, where A is Hermitian. |
| m0 axisymmetric residual added to b | extra | F0 F1 F2 F3 F5 | **F5 both checks**; F2a-e; F3 forcing linearity; R rescaling |
| Supplied G ignored (-rho·divU used) | extra | F0 F1 F2 F4 | **F4 PM verbatim; G and divU linearity**; F2a-m |
| i·m replaced by -i·m | extra | F0 F1 F2 | F2a-c |
| +R·Omega_z·U_z in VP | extra | F0 F1 F2 | F2c, F2o |
| R·Omega_z·VZ dropped from AP | extra | F0 F1 F2 | F2c, F2o |
| Extra 2·pi factor on A and b | extra | F0 F1 F2 F3 F4 | F2a-o; second difference; F4 linearity |
| A transposed | extra | F1 F2 F3 F4 | F2a-i, n, o; F3 column phases; second difference; F4. F0 (1x1) cannot see it. |
| gamma missing in PM | extra | F0 F1 F2 F4 | F2d, e, i; F4 PM verbatim; F4 linearity |
| b conjugated | extra | F0 F1 F2 F3 | F2j-m; F3 global phase; column phases; forcing linearity |
| divU^T instead of divU^H | extra | F0 F1 F2 F3 F4 | F2f-i; F3 global phase; column phases; F4 linearity |

Per-check names and error values are in `fixture_results_h2v001_mutations.json` under `mutations[*].detected_by_value_mismatch` and `detected_by_exception`.

## 8. Algebraic consequences of the contract text

The following facts were established by F2/F3: the hand-derived expectations matched the loop transcription to at most 2.5e-16. They are consequences of the supplied equations, not physics verdicts. Whether they express the intended physics is for H1 and root.

- **Shear terms cancel in AP.** With any Omega_R and Omega_z, AP = 2i·m·Omega²·U_R - m²·Omega²·U_phi. The term i·m·Omega·(-R·Omega_R·U_R - R·Omega_z·U_z) coming from VP is cancelled exactly by R·Omega_R·VR + R·Omega_z·VZ.
- **Shear enters A only through AR** (via -2·Omega·VP):
  - Radial shear adds U_R^H diag(2·vw·rho·Omega·R·Omega_R) U_R, which is Hermitian.
  - Vertical shear adds U_R^H diag(2·vw·rho·Omega·R·Omega_z) U_z, with no U_z^H(..)U_R counterpart. With Omega_z ≠ 0 the inertial block is therefore not Hermitian.
  - With Omega_z = 0, K = 0, G = 0 and both P gradients zero, A is Hermitian (F2a/F2b, to at most 1.6e-16).
- **Dependence on m.** A is quadratic in m. Its m² coefficient is -[U_R^H D U_R + U_phi^H D U_phi + U_z^H D U_z]/ns, with D = diag(vw·rho·Omega²).
- **b** does not depend on m or R, and it is exactly 0 for zero forcing.
- **E and PM** do not depend on m.

## 9. Running the harness against a future module path

Use this command for Claude3's frozen module. Choose a **lead-owned** output name: the H2 files are exclusive, so do not overwrite them.

```
/usr/bin/python3 -I -B "/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/weak_euler_review_0440/fixtures_weak_euler_h2v001.py" \
  --module "/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/weak_euler_0439/weak_euler_assembly_c3v001.py" \
  --func assemble_weak_euler \
  --out "/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/weak_euler_review_0440/<LEAD_OWNED_RESULTS>.json"
```

**How it runs:**
- The command works from any working directory.
- The target and the optional adapter are loaded by file path, and no bytecode is written.
- `meta.target.module_sha256` records the hash of the file that was actually executed.
- The exit status is 0 iff no check has status `fail` or `error`. Record-only entries never fail.

**Adapter.** Add `--adapter-module PATH` if the target's argument or output names differ from the canonical ones. The adapter module is lead-owned. A template:

```python
RENAME = {}                       # canonical -> target name, e.g. {'R': 'radius'}
def to_target(kw):                # must tolerate a missing key (F6 missing-kwarg probes)
    return {RENAME.get(k, k): v for k, v in kw.items()}
def from_target(raw):             # return canonical A, b (already /normalization_scale), E, PM, VR, VP, VZ
    return raw
```

Positional-call probes pass `to_target`'s values in their dict order. Python API: `run_all(target, adapter=None, out_json=None, skip=(), target_info=None)`.

**What to read in the output:**
- `summary.failures`
- `f6_summary.failing_probes`
- `f6_summary.rejections_flagged_incidental`
- `f6_summary.record_only_outcomes`
- per-check `detail`, which holds per-key errors, failing m, exception messages and bitwise flags

**Regenerating the H2 files:**

```
/usr/bin/python3 -I -B .../fixtures_weak_euler_h2v001.py --reference-run  --out .../fixture_results_h2v001_reference.json
/usr/bin/python3 -I -B .../fixtures_weak_euler_h2v001.py --mutation-study --out .../fixture_results_h2v001_mutations.json
```

## 10. Limits

- **Scope of the inputs.** All inputs are synthetic and O(1), with at most 16 points and 5 free columns. The fixtures carry no physical scales and say nothing about conditioning, memory or performance at the 2304-point x nfree project size.
- **What the fixtures cannot see.** They observe only returned values, exceptions and input immutability. Internal properties are invisible unless they change values: whether diagonal matrices are materialized, whether contractions are economical, or whether an unused pseudoinverse or solve exists. Static inspection by the lead/H1 must cover these. The raw return key set is recorded so that extra outputs, such as a solution vector, are visible.
- **Out of scope.** G's construction (0438), boundary/surface terms (assumed zero by the contract) and the physical correctness of the equations are not tested.
- **Independence of the reference.** F1 depends on the H2 loop transcription, which is itself cross-checked in four ways: the exact-rational hand case, the separately derived F2 expectations, the reference-free F3 identities, and the independent vectorized control (agreement to at most 6.4e-16).
- **Interpretation.** Record-only probes and the incidental-error flag are information, not verdicts. The flag is a regex over exception messages.
