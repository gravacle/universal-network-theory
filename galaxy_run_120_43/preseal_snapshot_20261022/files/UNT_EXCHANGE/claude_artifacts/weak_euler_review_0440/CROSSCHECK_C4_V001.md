# CROSSCHECK_C4_V001: adversarial cross-check of H1 (algebra oracle) and H2 (loop reference and harness)

Claude4 review lane, dispatch 0440 as amended by 0441. Written 2026-10-16 by a local helper, the adversarial cross-checker. It is not an external-account response, a physical verdict or the 0440 PASS/FAIL. Codex1 (root) owns physics, launches and acceptance; the Claude4 lead owns the verdict.

**Scope.** The work used small synthetic arrays only: assembly fixtures have at most 16 points and 5 free columns, and the quadrature check uses 8x8 = 64 nodes. No project module was imported or executed. No galaxy data, mesh arrays, calibration or target velocities, or validation outcomes were opened, and no project calculation was launched. Claude3's `weak_euler_assembly_c3v001.py` and the files in the lead's `c3_snapshot_8632bda6/` were not opened or run; that directory was only listed.

## 0. Bottom line

1. **H2 reference (`reference_weak_euler_h2v001.py`): no transcription error.** The line-by-line reading is in §1. Numerically it agrees with three independent routes:
   - the pinned equation text evaluated mechanically;
   - an independent hand-typed transcription by the cross-checker;
   - the H1 closed-form oracle.

   It also agrees with exact rational arithmetic to roundoff.
2. **H1 (`algebra_oracle_h1v001.py`, `ALGEBRA_SIGN_H1_V001.md`): no algebra, sign or derivation error.** I redid every step by hand: the substitution of VR/VP/VZ into AR/AP/AZ, the M_p matrix, the pressure/density restructuring, the thermal-wind cancellation, the conjugation argument for the weak φ-component, continuity and the Lindblad determinant. Independent finite-difference and quadrature checks agree with each step (§2).
3. **Oracle vs reference.** Over 216 random complex cases, the largest max-abs relative error is **3.589e-15 for A** and **5.498e-16 for b**.
   - The 3.6e-15 comes from cancellation in a single 1x1 entry (seed 2, m = 1).
   - Scaled by the componentwise condition scale, the errors are 5.886e-16 for A and 2.330e-16 for b.
   - Against exact `Fraction` arithmetic (180 cases), every float route is within 3.47e-15 max-abs relative and 4.52e-16 condition-scaled.
4. **The H2 harness reproduces exactly.**
   - F0-F5 on the reference: 46 pass, 2 record, 1 skipped, 95 target calls.
   - F6 self-test: 218 probes. All 173 reject probes are rejected, all 16 accept probes pass, and the 29 record-only probes split 14 accepted / 15 rejected.
   - F7 mutation study: 27 of 27 mutants detected.
   - Both in-memory serializations are **byte-identical** to H2's saved JSON files (same SHA-256).
   - H2's unsaved F6 demonstration also reproduces: 94 of 173 reject probes are silently accepted, 52 rejections are flagged incidental, and the accept probes pass 16/16.
   - The harness gives no false FAIL: two further independent correct implementations each pass all 46 F0-F5 checks.
   - It is sensitive: 26 additional defect mutants not in H2's list were all detected, each by 9 of 9 F1 checks.
5. **Contract vs prior v002: I agree with H1. The root contract has no real equation discrepancy.** Twelve v002 lines (L39, L44-L49, L52-L54, L57, L58) are present verbatim. A hand copy of the v002 contraction, fed the same supplied inputs, equals the contract reference to 6.1e-16. The remaining differences are the ones H1 lists:
   - the G discretization, which is by design;
   - the global 2π weight convention, a scale only;
   - forcing, background derivatives and normalization, which are now supplied by root.

## Inputs (SHA-256, `shasum -a 256` and re-hashed at run time by the script)

| File | SHA-256 |
|---|---|
| Root contract `.../CODEX1/ADDITIONAL_CLAUDE_WEAK_EULER_TASKS_V001.json` | `5c30449de636b1f3da751d07ad90caafe964ed19444b0648df8fd9726ade9ebe` (matches pin) |
| Prior v002 `.../coefficient_method/owned_nonzero_modal_weak_adjustment_v002.py` (read only, never imported) | `5cae4ee994f1ca07fdf703af529e7f5df9df2c2ed642d478df89beb692a25c51` (matches pin) |
| Helicity maps `.../coefficient_method/owned_32q8_regular_helicity_maps_v001.py` (read only; L64 read) | `280149dc028260d865604948633bb8a1332c5ee01be916895c02df42e2b280c6` (matches pin) |
| `FROM_CODEX/0438_2026-10-16_claude_free_surface_density_projection.md` | `83c963759f875285ce0b33148de1684318cbb81aa4658e1128bede3fe76a5c4c` (observed; no pin) |
| H1 `algebra_oracle_h1v001.py` | `29fc7fd429c921c4e6e7c04a624ce4db6ffcb0b32a8c0f5a432413ce73feb23e` |
| H1 `ALGEBRA_SIGN_H1_V001.md` | `b42bab82c1ab510e2c74a498fdfe944c35f21a56cb4da25fc8274ad5bb90251e` |
| H1 `check_h1_oracle_v001.py` | `ae5238153a1efe6dd1354488620d3d8d07713f3e77dd2255350d5621ae78d53a` |
| H2 `reference_weak_euler_h2v001.py` | `61f1982cbb48a25e1bd1a50afa13c217eb0b77bb905e7db5b19511c714b2a4ac` |
| H2 `fixtures_weak_euler_h2v001.py` | `a958ecb83279bb4fa069786d0741c13e6ba757a39b6e85e5efe1a86567f8cda7` |
| H2 `fixture_results_h2v001_reference.json` | `296fd463ded48dc62f5b425d58e3fde52cc2e12a823f8e1dcfbae9a900d0d51d` |
| H2 `fixture_results_h2v001_mutations.json` | `74261329bd8879704f1b5f7ad7c50d00f1db7568bf19335f0eb035fd854cff99` |
| H2 `FIXTURES_H2_V001.md` | `a9f2ce2bfa64132667800e0492203f6c83c61eaebc4cf879d7aa0e744f2a4463` |

Every hash above equals the value H1 and H2 reported. The cross-check script is `crosscheck_c4_v001.py`, SHA-256 `701e6834bae41fab1064055a9c964186bafa5889fe277096bf7d5737b9db8e78`. This note cannot contain its own hash; the hash is in the structured return.

## 1. H2 reference, line by line against the contract (task 1)

The contract's `author_task.equations` contains 11 entries and 10 U+2212 minus signs. After normalization, the first 10 entries equal the cross-checker's own typed transcription exactly (script section [1]).

| Reference line(s) | Contract item | Finding |
|---|---|---|
| L41-42 | npoints = len(R), nfree = len(U_R[0]) | Correct for (npoints, nfree) arrays. There is no validation, by design; the harness owns it. |
| L46-67 | float/complex scalar unpacking | Harmless. float() would drop the imaginary part of a numpy complex, but the reference is never asked to validate. In the F6 self-test, the validator rejects complex real vectors before the reference is called. |
| L81 | E = -K_R U_R - K_z U_z | Correct: both minus signs, K_R on U_R, K_z on U_z. |
| L83 | PM = (γP/ρ)G + ρ^γ E | Correct. `rho**gamma*E` is read as (ρ^γ)E. No weight. G is used verbatim. |
| L85, L91 | VR = imΩU_R, VZ = imΩU_z | Correct: `1j*m`, not -1j*m. |
| L87-89 | VP = -(RΩ_R)U_R + imΩU_φ - (RΩ_z)U_z | Correct: both shear minus signs, R inside both products. |
| L93 | AR = imΩVR - 2ΩVP | Correct. |
| L95-97 | AP = imΩVP + (2Ω+RΩ_R)VR + (RΩ_z)VZ | Correct: the coefficient multiplies VR, and RΩ_z multiplies VZ. |
| L99 | AZ = imΩVZ | Correct. |
| L105-117 | A[k][j], k = test (conjugated), j = trial | Correct. Only the test map is conjugated; trial factors (AR, AP, AZ, PM, G) are not. The weights appear once per term: w·ρ for the three inertial terms; w alone for the pressure term, with leading minus; w·P_R/ρ and w·P_z/ρ for the density bracket, which divides by ρ and not ρ², carries a leading minus and has no U_φ term. |
| L120-127 | b = -U_R^H(wρf_R) - U_φ^H(wρf_φ) - U_z^H(wρf_z) | Correct: three minus signs, test-side conjugation, f_φ used verbatim with no extra i·m/R. |
| L130-132 | A/ns, b/ns | Correct. There is a single division, applied to A and b only. |
| L137-147 | Returned maps | E, PM, VR, VP and VZ are unscaled. A_unscaled and b_unscaled are extra keys. |

**Transcription errors found: none.**

The numerical confirmation is in §3:
- the reference vs the contract-literal evaluation: maps bitwise equal, A ≤ 8.2e-16, b ≤ 5.8e-16;
- the reference vs exact arithmetic: condition-scaled A 4.5e-16 and b 1.9e-16.

I also re-derived H2's hand case independently: E = 2-5i, PM = 69-157.5i, VR = -8+4i, VP = -1+4i, VZ = -4-4i, AR = -12-48i, AP = -64+32i and AZ = 16-16i.
- The inertial part is 4[(-108-24i) + (-160) + (-32)] = -1200-96i.
- The pressure part is -0.5(3+2i)(69-157.5i) = -261+167.25i.
- The density part is -(2.5-0.5i)(2+i) = -5.5-1.5i.
- So A_unscaled = -1466.5+69.75i and A = -366.625+17.4375i.
- b_unscaled = -4[(-1-3i) + (-2+4i) + (4+2i)] = -4-12i, so b = -1-3i.

These match H2's values exactly. Section [4] confirms the reference, the literal evaluation and the oracle to 1.85e-16. H2's floating-point note also holds: 8.0**(5/3) = 32.00000000000001, and the reference's Im A = 17.437500000000007.

## 2. Independent algebra (task 2)

**Substitution.** I substituted VR, VP and VZ into AR, AP and AZ by hand:
- AR = (-m²Ω² + 2RΩΩ_R)U_R - 2imΩ²U_φ + 2RΩΩ_z U_z.
- In AP, the U_R coefficient is -imRΩΩ_R + 2imΩ² + imRΩΩ_R = 2imΩ², the U_φ coefficient is -m²Ω², and the U_z coefficient is -imRΩΩ_z + imRΩΩ_z = 0.
- AZ = -m²Ω²U_z.

This equals H1's M_p = -m²Ω²I + 2imΩ²J + R∂_R(Ω²)e_Re_Rᵀ + R∂_z(Ω²)e_Re_zᵀ, with J = e_φe_Rᵀ - e_Re_φᵀ. The term 2imΩ²J is Hermitian, and the only non-Hermitian entry is (R,z) = 2RΩΩ_z.

Section [5] extracted M_p by driving the pinned contract text with unit maps. It matches my hand form to 1.8e-16, and H1's `pointwise_inertial_matrix` matches it exactly (0.0). The determinant of the (R,φ) block works out by hand to m²Ω²(m²Ω² - κ²), with κ² = 4Ω² + 2RΩΩ_R, as H1 states.

**δv and δa.** I re-derived δv = (v0·∇)ξ - (ξ·∇)v0 and δa = (v0·∇)δv + (δv·∇)v0, including the unit-vector rotation terms, for a static pattern with exp(+imφ). The results are exactly the contract's VR, VP, VZ and AR, AP, AZ.
- The independent route δa = (v0·∇)²ξ - (ξ·∇)a0, with a0 = -Ω²R e_R, gives the same M_p.
- I also confirmed by hand the continuity identity ∇·(ρδv) + v0·∇δρ = 0 with δρ = -∇·(ρξ). The shear terms of δv_φ cancel the Ω-gradient terms.
- **Section [7]** is an independent Cartesian check, coded separately from H1's: 4th-order central differences with h = 1e-3, analytic Ω(R,z) with nonzero Ω_R and Ω_z, complex polynomial U, 4 points and m = 1..6.
  - δv vs the contract: 8.2e-11.
  - δa vs the contract: 8.1e-11.
  - Mutant VP with +RΩ_zU_z: deviation ≥ 1.7e-2.
  - Mutant AP with -RΩ_zVZ: deviation ≥ 1.8e-2.

**Weak-form φ-component conjugation.** H1's argument is correct. The φ part of ∫conj(W)·∇(δP e^{imφ}) is conj(U_φ)(imδP/R). Because conj(i) = -i, this equals -conj(imU_φ/R)δP. That pairs with the +im in divU (helicity L64 reads `(1j*m)*maps['UP']/rr`), so ∫conj(U)·∇δP = -∫conj(divU)δP once the surface terms are dropped. This gives the term `-divU^H diag(w) PM`, with one weight and no ρ.

**Section [8]** checks this by Gauss-Legendre quadrature, 8x8 nodes, exact for these polynomial integrands, with δP = 0 on the boundary of [1,2]x[-1,1]:
- each component and the total: 9.4e-16;
- divU built with -im: mismatch 1.42;
- the unconjugated (bilinear) form: mismatch 0.93.

**Pressure/density restructuring (H1 §1i).** By hand I substituted G = -(ρ divU + ρ_R U_R + ρ_z U_z) and P_R = ρ^γK_R + (γP/ρ)ρ_R, with the same for z. The result is exactly H1's nine-term form. Its anti-Hermitian part is ½[U_R^H D(w(P_Rρ_z - P_zρ_R)/ρ)U_z - h.c.].
- Differentiating the two equilibrium components and eliminating Φ0 gives 2RΩΩ_z = (P_zρ_R - P_Rρ_z)/ρ².
- Hence (P_Rρ_z - P_zρ_R)/ρ = -2ρRΩΩ_z, which cancels the inertial vertical-shear anti-Hermitian part exactly.

**Section [6]** tests this on 54 consistent backgrounds:

| Quantity | Result |
|---|---|
| Restructured form vs contract pressure/density part, and vs H1 `oracle_parts` | 3.8e-15 |
| Full A, anti-Hermitian relative norm | ≤ 4.0e-16 |
| Inertial part alone | ≥ 7.0e-3 |
| Pressure part alone | ≥ 0.139 |
| The two anti-Hermitian parts cancel to (relative to the inertial anti-Hermitian part) | 1.75e-14 |
| Inconsistent Ω_z (+0.3) | ≥ 6.6e-3 |

**Other H1 statements checked.** Each of the following is correct:
- The pattern-speed remark: im(Ω-Ω_p) replaces imΩ, while 2Ω and the shear terms are unchanged.
- The FFT/16 statement: X_m/16 = c·e^{imφ_0}.
- PM reduces to -γP∇·ξ - ξ·∇P when δρ = -∇·(ρξ) exactly.
- The 0438 sign derivation (+, -im, +).
- The note that the natural BC of the dropped pressure surface term is Eulerian δP = 0. This is a scope note: it coincides with the physical Lagrangian ΔP = 0 only where ξ·∇P = 0, which is why v002 L69 keeps the surface ΔP as a diagnostic only.

**H1's check script.** I re-ran `check_h1_oracle_v001.py` (stdout only; it writes no files; the directory listing was unchanged). It reproduces every number in H1's §2 table exactly: 6.011e-16, 3.631e-16, 4.311e-16, 4.284e-16, 5.272e-3, 0.5807, 7.642e-12, 9.346e-12, 1.184e-11, 1.445e-15, 1.144e-14, 3.439e-16, 4.412e-16, and all 20 mutant rows.

**Derivation or oracle errors found: none.**

## 3. Cross-check script results (task 3)

Run: `/usr/bin/python3 -I -B /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/weak_euler_review_0440/crosscheck_c4_v001.py`. It uses Python 3.9.6 and numpy 2.0.2, exits 0 and takes about 3.7 s. Output is deterministic, and the last line is `RESULT_JSON {...}`.

H1's oracle and H2's reference are loaded by path with importlib, and no bytecode is written. Four independent routes are compared:
- **H2 reference:** loops.
- **H1 oracle:** closed-form einsum.
- **Contract-literal:** the pinned equation strings themselves. Equations 1-8 are evaluated verbatim. Equations 9-10 are mechanically translated: `X^H` → `H(X)`, `diag` → dense `np.diag`. The translation is checked against a hand-checked expected string.
- **C4:** the cross-checker's own einsum transcription.

**[2] Random complex cases: 216.**
- Seeds 0-5; shapes (7,3), (4,4), (16,5), (9,1), (1,1) and (3,5); m = 1..6.
- Ω_R and Ω_z have magnitude in [0.2, 0.8] with random sign. Odd seeds give Ω of mixed sign.
- Maps have independent N(0,1) real and imaginary parts.

| Comparison | max-abs relative error |
|---|---|
| oracle/ns vs reference, A | **3.589e-15** (Frobenius 3.589e-15; condition-scaled **5.886e-16**; worst case seed 2, shape (1,1), m = 1) |
| oracle/ns vs reference, b | **5.498e-16** (Frobenius 4.206e-16; condition-scaled 2.330e-16) |
| contract-literal vs reference, A / b / maps | 8.228e-16 / 5.756e-16 / 0 (bitwise) |
| C4 vs reference, A / b / maps | 1.641e-15 / 5.498e-16 / 0 |
| oracle vs contract-literal, A / b | 3.625e-15 / 4.427e-16 |
| reference A_unscaled/ns vs A (and the same for b) | 2.189e-16 |

Two further facts from this section:
- Output shapes were correct in every case, including nfree = 1 with npoints > 1 and nfree > npoints.
- Both sensitivity probes are far above roundoff: setting Ω_z to 0 changes A by at least 8.5e-4, and dropping the test-side conjugation changes the inertial part of A by at least 0.223.

**[2b] Exact rational arithmetic: 180 cases.** Shapes (4,3), (3,3), (1,1), (9,1) and (16,5); seeds 0-5; m = 1..6. ρ^γ is held at its float value.

| Route | max-abs rel A | max-abs rel b | condition-scaled A | condition-scaled b |
|---|---|---|---|---|
| H2 reference | 2.011e-15 | 4.196e-16 | 4.516e-16 | 1.947e-16 |
| H1 oracle | 3.466e-15 | 4.380e-16 | 2.862e-16 | 2.032e-16 |
| contract-literal | 2.011e-15 | 2.677e-16 | 3.332e-16 | 1.295e-16 |
| C4 | 6.704e-16 | 4.380e-16 | 2.999e-16 | 2.032e-16 |

The 1e-15-level max-abs figures come from cancellation in small entries. Every route is within about 2 ulp of the exact value on the componentwise condition scale.

**[3] Root-structured cases: 96.** U_R and U_z are real-dtype, U_φ is purely imaginary, divU and G are real-valued with complex dtype, and the forcing is complex.
- Agreement: oracle vs reference A 7.2e-16 and b 3.9e-16; contract-literal vs reference A 6.6e-16, b 8.5e-16, maps 0.
- In this structure **A is exactly real**: max |Im A|/max|A| = 0.0. b is complex: |Im b|/max|b| ≥ 0.038.
- Dropping the test-side conjugation only on U_φ changes A by ≥ 0.216 and b by ≥ 0.292. Dropping it on U_R, U_z and divU changes A by only 3.9e-16, which is invisible.
- This confirms the lead's V002 note. In root's map structure only U_φ conjugation errors are visible, so the random complex fixtures remain necessary.

## 4. H2 harness re-run (task 4)

The CLI requires `--out`, which would write a file, so I used the Python API with `out_json=None` and wrote no files.

| Run | Result |
|---|---|
| `run_reference_selfcheck` | F0 2/2, F1 9/9, F2 15/15, F3 13/13, F4 5 pass + 2 record, F5 2/2, F6 skipped. Overall **46 pass, 2 record, 1 skipped, all_pass**. 95 target calls; largest check error 3.588e-16. |
| F6 self-test | **218 probes.** Reject 173/173 rejected, 0 flagged incidental. Accept 16/16 pass. Record-only 29 (14 accepted, 15 rejected). No failing probes. |
| Serialization | sha256 `296fd463...0d51d`, **byte-identical** to `fixture_results_h2v001_reference.json` |
| `run_mutation_study` | **27/27 detected** (17/17 required), control all-pass with the same counts. Smallest failing-check value mismatch 2.980e-3 (P_R/ρ², F0). |
| Mutation-study file contents | 437 value-mismatch detections and 41 exception detections; control F1 maximum 6.387e-16. |
| Serialization | sha256 `74261329...cff99`, **byte-identical** to `fixture_results_h2v001_mutations.json` |
| H2 "unsaved demonstration", identity adapter and a C4 keyword-renaming tuple adapter | Both: 94 of 173 reject probes silently accepted, 79 rejected (52 flagged incidental), accept 16/16, F0-F5 clean. This reproduces H2's figures. |
| Bitwise flags in the saved JSON | Volume weights x2 and R x2: bitwise in all outputs. x0.37 and x3: within tolerance, not bitwise. This matches H2's claim. |

**False FAIL test.** Two further correct implementations were run through `run_all` F0-F5: the C4 einsum transcription and the contract-literal evaluation. Each gave **46 pass, 2 record, all_pass**, with largest check errors 7.7e-16 and 6.3e-16. A correct but differently coded implementation therefore does not trip H2's expectations or tolerances.

**Sensitivity test.** 26 defect mutants not in H2's list were all detected, each failing 9/9 F1 checks. The smallest finite failing value was 6.6e-3. The mutants were:
- G conjugated;
- K_z paired with U_R;
- E sign;
- weights inside E;
- ρ^(5//3);
- ρ in place of ρ^γ;
- VR missing `[:,None]`;
- VP missing the R factor;
- m hard-coded to 1 in VP;
- Coriolis factor 1;
- Coriolis sign;
- the AP coefficient applied to VP;
- AP radial-shear sign;
- the AZ term using AR;
- ρ in the pressure weight;
- conjugated PM trial;
- pressure weight missing `[:,None]`;
- the P_z density term tested with U_φ;
- b missing ρ;
- f_R and f_z swapped;
- f_φ tested with U_z;
- A real part only;
- A Hermitian-transposed;
- A divided by ns²;
- A not normalized;
- VR divided by ns.

**Harness errors found: none.**

## 5. Contract vs prior v002 (task 5)

**I agree with H1's assessment: the root contract has no real equation discrepancy.**
- Section [9] confirms that the exact text of v002 L39, L44-L49, L52-L54, L57 and L58 is present.
- A hand copy of the L44-48, L52-54 and L58 expressions was given the contract's supplied inputs in place of v002's internal quantities: W = Ω, RR = R, WR/WZ = Ω_R/Ω_z, K_R, K_z, P_R and P_z, vol = volume_weights, and G, divU and f. It agrees with the contract reference for A, b and all maps to 6.1e-16. v002 itself was never imported or executed.
- G discretization: v002 L43 uses a lumped nodal adjoint; 0438 uses a consistent-mass projection. Both are weak forms of δρ = -∇·(ρξ) with the signs (+, -im, +) and the zero-flux drop. This is a deliberate operator change, not an equation error.
- Weights: v002 L39 sums over the 16 azimuthal cells, which includes the 2π. On a common quadrature this is a global scale on A and b only; H1's check [G] reproduces this to 4.4e-16, and G is degree-0 homogeneous in W. This was not verified on mesh arrays.
- Forcing, background derivatives and normalization are now supplied by root. They affect b and values only, not the form of the operator.

## 6. Observations for the lead (coverage notes, not errors)

1. **nfree = 1 with npoints > 1 is absent from H2's harness**, which has only the (1,1) case. H1's checklist recommends it. I found no plausible defect that the existing shapes miss but an (n>1, 1) case would catch. For example, a missing `[:,None]` (the C4 mutants `VR_column_broadcast` and `pressure_weight_broadcast`) is caught by value in the square (4,4) case and raises an exception at non-square shapes. The case is cheap, though. Add an (n>1, 1) comparison when Claude3's module is evaluated, for example against the H1 oracle. The cross-check covered (9,1) for oracle, reference and literal only.
2. **H2's F0-F5 use positive Ω only.** Negative Ω is exercised only by the F6 probe `accept_Omega_all_negative`, so the evaluation of Claude3's module should not skip F6. Alternatively, a mixed-sign-Ω comparison could be added; [2] shows the oracle and reference agree on mixed-sign Ω.
3. **H1 oracle usage.** It requires a Python int `m` (`type(m) is int`) and real-dtype real vectors. It returns **unscaled** A and b, so divide by normalization_scale before comparing.
4. **Error metric.** Max-abs relative error is inflated by cancellation in single-entry cases; the 1x1 case reaches 3.6e-15. For a roundoff judgment, the condition-scaled metric (≤ 6e-16 here) is the cleaner yardstick. The smallest mutant signals sit far above either: 8.9e-4 (H1 mutants, oracle metric), 2.98e-3 (H2 mutants, harness metric) and 6.6e-3 (C4 mutants, harness metric).

## 7. Process and limits

- **Files written:** only `crosscheck_c4_v001.py` and this note. The `ls -laR` digest of the review directory was identical before and after every run, and no `__pycache__` or `.pyc` was created. H1's, H2's and the lead's files were not modified.
- **Read for context only:** CURRENT_INSTRUCTIONS.md, CLAUDE4_START_HERE, dispatches 0438-0441 and 0445, and the lead's PARTIAL_REVIEW_0440_V002/V003 notes. I did not open Claude3's module or any file in the lead's snapshot directory (I only listed the directory).
- **Not established here:**
  - actual mesh weights and the 2π convention on real arrays;
  - the 0438 G construction itself;
  - boundary traces;
  - conditioning or behavior at project scale (2304 x nfree);
  - any physical adequacy.
