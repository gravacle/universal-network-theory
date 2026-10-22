# ALGEBRA_SIGN_H1_V002_CODE: line-by-line algebra and sign review of the frozen candidate c3v001

Lane: Claude4 review lane (dispatch 0440, amended by 0441 and 0446). Author: local helper **H1** (algebra, complex signs, vertical shear). This is a helper note for the Claude4 lead. It is not an external-account response and not a physical verdict. Codex1 owns physics, launches and acceptance.

H1 edited no Claude3 file and imported or ran no project module. It opened no galaxy data, calibration or target velocities, or validation outcomes. Only the pinned copy was loaded, by path, for three tiny stdout-only probes (§5). The original file was hashed but never imported.

## Object and hashes (`shasum -a 256`)

| file | sha256 | when |
|---|---|---|
| `c3_snapshot_8632bda6/weak_euler_assembly_c3v001.py` (pinned copy, 344 lines) | `8632bda6d4a80d0d25bfa90ef4b1066954b6bc67c90f184d0a78c232bf3013da` | before and after this review |
| `weak_euler_0439/weak_euler_assembly_c3v001.py` (original) | identical | before and after |
| `CODEX1/ADDITIONAL_CLAUDE_WEAK_EULER_TASKS_V001.json` (contract) | `5c30449de636b1f3da751d07ad90caafe964ed19444b0648df8fd9726ade9ebe` | matches pin |

**Reused, not repeated:**
- the H2 harness on these bytes: 235 pass, 31 record, 0 fail (PARTIAL_REVIEW_0440_V003_PREFREEZE.md);
- the lead's AST static check (STATIC_REPORT_c4lead.json);
- the H1 phase-1 derivation and oracle (ALGEBRA_SIGN_H1_V001.md).

**Not duplicated:** the lead's oracle-vs-module and root-structured fixture comparisons.

## Verdict (H1 scope)

**PASS.** Every equation in the pinned contract is realized at the lines below. Each has the contract's signs and factors, conjugation on the test side only, `[:, None]` row broadcasting, exactly one volume weight per A/b term, and normalization of A and b only. The validation code meets every item of the phase-1 checklist.

**Defects found: none.** That is 0 blocking, 0 minor and 0 note.

## 1. Equation trace

Notation: w = volume_weights, D(d) = diagonal of the point vector d (the code never forms one), s = normalization_scale.

| contract item | implementing lines | verdict |
|---|---|---|
| E = -K_R[:,None]*U_R - K_z[:,None]*U_z | 221-222 | matches. The AST of L221 is (-K_R[:,None])*U_R, then `E -= K_z[:, None] * U_z`. Same left-to-right order as the contract. |
| PM = (gamma*P/rho)[:,None]*G + rho[:,None]**gamma*E | 228-229 | matches. `(rho**gamma)[:, None]` is elementwise the same as `rho[:, None]**gamma`. The validated float 5/3 is used at both sites. |
| VR = i*m*Omega[:,None]*U_R | 216, 234 | matches. `i_m_Omega = 1j * m * Omega` (+i, never -i). |
| VP = -(R*Omega_R)[:,None]*U_R + i*m*Omega[:,None]*U_phi - (R*Omega_z)[:,None]*U_z | 238-240 | matches. In the AST of L238 the unary minus is on the coefficient, then `+=` (L239) and `-=` (L240). |
| VZ = i*m*Omega[:,None]*U_z | 244 | matches |
| AR = i*m*Omega[:,None]*VR - 2*Omega[:,None]*VP | 272-273 | matches. It is formed in scratch Y and is not returned; the contract does not return it. L273 parses as (2*Omega[:,None])*VP. |
| AP = i*m*Omega[:,None]*VP + (2*Omega+R*Omega_R)[:,None]*VR + (R*Omega_z)[:,None]*VZ | 282-284 | matches. (2Ω + RΩ_R) multiplies VR and RΩ_z multiplies VZ. |
| AZ = i*m*Omega[:,None]*VZ | 291 | matches |
| A term 1: +U_R^H D(w rho) AR | 269, 274, 277 | matches |
| A term 2: +U_phi^H D(w rho) AP | 285, 287 | matches |
| A term 3: +U_z^H D(w rho) AZ | 292, 295 | matches |
| A term 4: -divU^H D(w) PM | 299, 301 | matches. The weight is w only, with no rho, and the term is subtracted. |
| A term 5: -U_R^H D(w P_R/rho) G | 275, 277 | matches. It has a minus sign and is divided by rho, not rho**2. It is subtracted after the L274 scaling by w*rho, so it carries no second weight. |
| A term 6: -U_z^H D(w P_z/rho) G | 293, 295 | matches. The same order holds relative to L292. |
| A as four grouped products | 272-301 | matches, by the distributivity argument in §3 |
| b = -U_R^H(w rho f_R) - U_phi^H(w rho f_phi) - U_z^H(w rho f_z) | 269, 313-321 | matches. The code follows the contract's three-term sequence exactly. `w_rho * f_phi` (L314) is the only use of f_phi. |
| normalization: return A/s, b/s | 304, 322; gate 193-197 | matches. Each division happens once, after full accumulation. Nothing else is divided. |
| unscaled maps E, PM, VR, VP, VZ | 221-245, 328-332 | matches. None is written after L222, L229, L234, L240 or L244. They are returned without scaling or weighting. |
| prohibitions | whole file | matches. None of the following is present: inverse, solve, pseudoinverse, ridge, clip, symmetrization, spectrum, tolerance or acceptance; an m0, Phi0, equilibrium-residual or extra forcing term; density reconstruction or a pressure reset. |

## 2. Cross-cutting confirmations

1. **Conjugation on the test side only.**
   - The only conjugations are `.conj().T` on U_R (L277), U_phi (L287), U_z (L295), divU (L301), and in b on U_R, U_phi and U_z (L319-321). These are the 7 sites in the static report.
   - On the trial side nothing is conjugated: U_R, U_phi and U_z in L221-244; G in L228, L275 and L293; VR, VP, VZ and PM in the Y integrands; f in L313-315.
   - There is no bare `.T`, `vdot` or `inner`.
2. **Row broadcasting.** All 21 products of a point vector with an (npoints, nfree) array use `[:, None]`.
   - The 15 contract sites are at L221, 222, 228, 229, 234, 238, 239, 240, 244, 272, 273, 282, 283, 284 and 291: E 2, PM 2, VR 1, VP 3, VZ 1, AR 2, AP 3, AZ 1.
   - The six weight sites are at L274, 275, 285, 292, 293 and 299.
   - b forms only (npoints,)·(npoints,) products (L313-315) and then (nfree, npoints) @ (npoints,).
   - No `X.conj().T * d` form occurs.
   - The square trap (npoints == nfree) and the nfree == 1 outer-product trap therefore cannot occur at any site. H2 F1 covers the square case (4,4); probe 3 below covers (7,1).
3. **Volume weight exactly once.**
   - Inertial terms: w*rho at L274, L285 and L292.
   - Density terms: w*P_R/rho at L275 and w*P_z/rho at L293.
   - Pressure term: w at L299.
   - b: w*rho at L313-315.
   - E, PM, VR, VP, VZ and the AR, AP, AZ integrands contain no w. G is never weighted or written.
   - The order guarantees this: L274 runs before L275 and L292 runs before L293, so G receives only w*P/rho.
4. **Pressure and density signs.**
   - Density: `Y -= (w * P_R / rho)[:, None] * G` (L275) and `Y -= (w * P_z / rho)[:, None] * G` (L293). The phi group (L282-287) has no density term.
   - Pressure: `A -= divU.conj().T @ (w[:, None] * PM)` (L299-301).
5. **Inertial couplings.**
   - 2*Omega: -2Ω VP in AR (L273), and +2Ω VR inside (2Ω + RΩ_R) in AP (L283).
   - R*Omega_R: minus on U_R in VP (L238), plus in AP (L283).
   - R*Omega_z: minus on U_z in VP (L240), plus on VZ in AP (L284).
   - i*m*Omega is formed once (L216) and used at L234, 239, 244, 272, 282 and 291.
6. **f_phi and the sign of b.** f_phi is used verbatim (L314): there is no i*m/R, 1/R, FFT or differentiation. In b, L319 negates the whole product and L320-321 use `-=`.
7. **Normalization.** Only `A /= normalization_scale` (L304) and `b /= normalization_scale` (L322).
8. **G is never modified.**
   - L179 only casts G to complex128. The cast preserves values for int, float and complex64 input; a complex128 input is the same object.
   - G is then only read, at L228, L275 and L293.
   - All 19 in-place writes target fresh locals: E, PM, VP, Y, A and b.
9. **No m0 or Phi0.**
   - There is no Phi0 input or term.
   - m enters only at L216, with no per-mode branch.
   - A contains exactly the six contract terms and b exactly the three forcing terms.

## 3. The four grouped products equal the contract A

1. **Row scaling.** For any (npoints, nfree) array Y, D(d)Y = `d[:, None] * Y`. By associativity, X^H D(d) Y = X^H (D(d) Y).
2. **Expand the bracket.** By right distributivity, the contract's last term is
   [U_R^H D(w P_R/rho) + U_z^H D(w P_z/rho)] G = U_R^H D(w P_R/rho) G + U_z^H D(w P_z/rho) G.
   Therefore

   A_contract = U_R^H D(w rho) AR - U_R^H D(w P_R/rho) G + U_phi^H D(w rho) AP + U_z^H D(w rho) AZ - U_z^H D(w P_z/rho) G - divU^H D(w) PM.

3. **Merge by test map.** Left distributivity, X^H Y1 - X^H Y2 = X^H (Y1 - Y2), merges the two U_R^H terms and the two U_z^H terms:

   A_contract = U_R^H Y_R + U_phi^H Y_phi + U_z^H Y_z - divU^H Y_div,

   with
   - Y_R = (w rho)[:,None]*AR - (w P_R/rho)[:,None]*G (L272-275)
   - Y_phi = (w rho)[:,None]*AP (L282-285)
   - Y_z = (w rho)[:,None]*AZ - (w P_z/rho)[:,None]*G (L291-293)
   - Y_div = w[:,None]*PM (L299)

4. **The code computes exactly these.** It forms the four products at L277, L287, L295 and L301 and accumulates them with the same signs. Matrix addition is commutative, so the accumulation order does not matter.
5. **Normalization.** Division by the scalar s distributes over the sum, so the single division at L304 equals the contract's A/normalization_scale.
6. **Floating point.** The two forms are equal in exact arithmetic. In floating point the only difference is the regrouped summation, an elementwise subtraction inside Y instead of a difference of two products. That is roundoff: 2.1e-16 in probe 3.
7. **b** is not regrouped; L319-321 follow the contract sequence, and L322 divides it.

## 4. Phase-1 checklist (ALGEBRA_SIGN_H1_V001.md §5) against the code

| # | item | lines | result |
|---|---|---|---|
| 1 | signature | 146-148 | PASS. 23 required keyword-only parameters follow a bare `*`, with no defaults and no `*args`/`**kwargs`. The names equal the checklist list. |
| 2 | m | 183-187 | PASS. `type(m) is int` rejects bool, np.bool_, numpy integers and float; 1 <= m <= 6 is enforced. Rejecting numpy integers is stricter than "Integer" and is already recorded in V003. It raises a ValueError rather than accepting silently. |
| 3 | gamma | 109-121, 188-192, 228-229 | PASS. bool is rejected (L111). Non-Real values, including complex, are rejected (L111; np.complex128 in probe 2). NaN and inf fail L189. The test is the exact `gamma != 5.0 / 3.0`: no tolerance and no `5//3`. The same validated gamma is used in `gamma*P/rho` and `rho**gamma`. |
| 4 | normalization_scale | 193-197 | PASS. It must be numbers.Real and not bool, finite and > 0. Probe 2: np.True_, np.complex128(2) and the 0-d np.array(2.0) are rejected; np.int64(2) is accepted as 2.0. |
| 5 | provenance | 198-201 | PASS. It must be a str containing a non-whitespace character. This is stricter than "nonempty" and is recorded in V003. |
| 6 | real vectors | 55-83, 162-173 | PASS. The dtype kind is checked (L68) before the cast (L78), so no imaginary part is ever dropped. bool, object, string and datetime are rejected. The shape must be exactly (npoints,), because L57 requires equal ndim, so (npoints,1) fails. Values must be finite (L79). R, rho, P and w must be > 0 (`positive=True` at L162, 164, 165, 173). |
| 7 | maps | 86-106, 174-179 | PASS. Each map must be exactly 2-D with shape (npoints, nfree), with nfree >= 1 taken from U_R. int, float and complex input is cast to complex128 without changing values. Both parts must be finite. There is no `.real` or `abs` anywhere. |
| 8 | forcing vectors | 180-182 | PASS. Shape (npoints,), finite, complex accepted. Every shape is tied to npoints from R (L163). |
| 9 | conjugate on the test side only | 277, 287, 295, 301, 319-321 | PASS (§2.1) |
| 10 | `[:, None]` broadcasting | 21 sites (§2.2) | PASS. Square case: H2 F1. nfree = 1: probe 3 gives A (1,1), b (1,) and maps (7,1). |
| 11 | weights exactly once | §2.3 | PASS. There is no extra 2π, R or annular factor; R appears only in R*Omega_R and R*Omega_z. |
| 12 | density term | 275, 293 | PASS. Divided by rho, with a leading minus, acting on G, and with no U_phi term. |
| 13 | pressure term | 299-301 | PASS |
| 14 | signs | 221-222, 228-229, 238-240, 273, 275, 283-284, 293, 301, 319-321 | PASS. All minus and plus signs are as listed in V001 §5. |
| 15 | imaginary unit | 216 | PASS. +1j*m at all six sites. |
| 16 | AP coefficient | 283-284 | PASS |
| 17 | PM | 228-229 | PASS. rho**gamma is used, not rho; the G coefficient is gamma*P/rho. |
| 18 | f_phi verbatim | 314 | PASS |
| 19 | no extra forcing or equilibrium term | whole file | PASS |
| 20 | G used exactly as supplied | 179, 228, 275, 293 | PASS |
| 21 | normalization | 304, 322 | PASS |
| 22 | no symmetrization | whole file | PASS. A is never transposed or combined with its adjoint. |
| 23 | no input mutation | 19 in-place writes (static report) | PASS. Every write targets a fresh local. Validated inputs, which may alias the caller's arrays, are only read. H2 F4 confirms this. |
| 24 | forbidden calls | whole file | PASS. The static report confirms this, and every line was read. |
| 25 | imports and purity | 31-34 | PASS. math and numbers (stdlib, used only for validation) and numpy. There is no I/O, global mutation, randomness, callback or default. |
| 26 | economy | 277, 287, 295, 301, 319-321 | PASS. There are no (npoints, npoints) or diagonal arrays: four (nfree, npoints) @ (npoints, nfree) products and three matrix-vector products. |
| 27 | returns | 325-344 | PASS. A is (nfree, nfree), b is (nfree,), the five maps are (npoints, nfree), provenance is echoed, and physical_status is `not_assessed`. There is no solution, acceptance or tolerance key. |
| 28 | one code path for every m | 216 | PASS |
| 29 | fixture design | n/a | Owned by H2 and the lead: the completed H2 run and the in-progress oracle comparison. Not repeated here. |
| — | fail-closed | 124-143, 215, 223, 230, 235, 241, 245, 276, 286, 294, 300, 305, 316-318, 323 | PASS (details below). |

**Fail-closed details:**
- Every returned array and every operand of a contraction is checked to be finite.
- Overflow during accumulation stays non-finite through the later +, - and division by a finite positive s, so the checks at L305 and L323 catch it.
- A ValueError leaves no partial result.
- Validation failures raise ValueError naming the parameter. A missing, positional or unknown argument raises Python's TypeError.

## 5. Probes

All probes ran under the root interpreter (`python3 -I -B`, Python 3.12.14, numpy 2.3.5), with the pinned copy loaded by path and `sys.dont_write_bytecode = True`. Output went to stdout only, and nothing was written next to the copy.

1. **AST of the sign-bearing statements** at L221, 222, 229, 238, 240, 273, 275, 283, 293, 301 and 319.
   - At L221 and L238 the unary minus binds to the coefficient: (-K_R[:,None])*U_R and (-(R*Omega_R)[:,None])*U_R.
   - L273 parses as (2*Omega[:,None])*VP, and L319 negates the whole product.
   - Every other sign is carried by the augmented operator (Sub or Add) listed in §1.
2. **`_real_scalar` (L109-121):**

   | input | result |
   |---|---|
   | np.True_ | ValueError |
   | np.complex128(2) | ValueError |
   | np.array(2.0) | ValueError |
   | np.int64(2) | 2.0 |
   | np.float64(5/3) | 1.6666666666666667 |

3. **nfree = 1 tall case.** Setup: (npoints, nfree) = (7, 1), m = 1..6, complex maps and forcing, nonzero Omega_R and Omega_z, s = 1.7. Reference: an inline, ungrouped transcription of contract equations 1-10.
   - The output shapes are correct.
   - The maximum relative error is 2.09e-16 for A (regrouping roundoff) and 0 for b (same evaluation sequence).
   - E, PM, VR, VP and VZ are bitwise equal to the literal contract expressions on this runtime.

Probe scripts (session scratchpad, not deliverables):
- `/private/tmp/claude-501/-Users-bgm-Research-UNT-EXCHANGE/d3eba6e0-d470-48a9-b17d-717c88261d09/scratchpad/h1v002/probe_h1v002.py`
- `/private/tmp/claude-501/-Users-bgm-Research-UNT-EXCHANGE/d3eba6e0-d470-48a9-b17d-717c88261d09/scratchpad/h1v002/probe_h1v002_nfree1.py`

## 6. Limits

- This is an algebra, sign and validation review of the code. Numerical equivalence on general cases was established by H2 (done). Equivalence on root-structured cases is the lead's oracle-vs-module run (in progress). Neither was repeated.
- The contract's physical presuppositions are root's and cannot be checked inside the module (ALGEBRA_SIGN_H1_V001.md §4). They are the static pattern, P = K rho^gamma with consistent gradients, thermal wind, the dropped surface terms, and the 0438 G join requirements.
- The contract-silent accept/reject behaviors already recorded in V003 were not re-tested; their implementing lines are cited above.
