# 0385 author notes, v001

Author: Claude helper (AUTHOR role). A different helper does the static review.
Artifact: `square_spatial_source_v001.py` in this directory. It has one public function, `square_spatial_source(*, ...)`, with 17 required keyword-only arguments and no defaults.

`square_source_coefficient_v001.py` (0384) was not modified. Its helpers were copied into the new file rather than imported.

## Sources (sha256 computed from bytes at authoring time)

| Source | Role | sha256 |
|---|---|---|
| FROM_CODEX/0385_2026-10-15_square_spatial_source_inert_implementation.md | formula authority | e1e0ea13a63a01c3290f57440c8de9d6e087a4a9eb056e7e146e3cc3309e9823 |
| claude_artifacts/square_source_coefficient_0384/square_source_coefficient_v001.py | structure and helpers copied | 21b80b8d9cad371e48fba57b413a75c6111f026b85725f84f13e9bfff782b57f |
| claude_artifacts/square_source_coefficient_0384/STATIC_REVIEW_0384_V001.md | 0384 review, read for carried notes | c11274f3541c10c59f2a99b4047893391107da5f4c9834770b539cdb1e5d37e2 |
| FROM_CODEX/0384_2026-10-15_square_source_coefficient_inert_implementation.md | 0384 formulas | cc991dab500b1d02bb201aad3a747290952337cf5c509aedf19d3e6d6692e1a3 |
| CODEX1/GALAXY_COLLECTIVE_MODEL_ASSEMBLY_2026-10-15.md | context only; the file is mutable and its current bytes differ from both earlier pins | e904d4b05db0adaa44ce1fe8a6978878a06fc9fdd450a0fa54082bec6e8670a1 |

## Spec-to-code mapping (line numbers in v001)

| 0385 item | Code |
|---|---|
| All 0384 local inputs plus explicit tolerances; no defaults | signature L268–286 |
| j_vec: required finite real length-4 list, tuple or shape-(4,) array, vertex order 0..3; scalars and other shapes rejected, never broadcast | `_real_vector4_input` L54–85; called at L365 |
| Same reference checks (r2, g, kappa, mu0, delta) | L401–425 |
| Same H(d), complete eigensystems of H(1)–H(3), chi, e2, gap, residuals | `_local_block` L99–112; L427–488 |
| Same cycle, sigma, a_v, D | L492–510 |
| b_Sv = 4 a_v² | L512 |
| c(S, j_vec) = Ud D + mu0 Σa − 4 Σ_v j_v a_v², written as Σ_v j_v b_v | L513–514 |
| Kronecker-sum denominators; every used denominator > pos_tol before inversion; minimum tracked | L516–561 |
| Per-prefix transform into the complete tensor eigenbasis and back, with source axes carried through an einsum ellipsis | `_site_apply` L115–131, L134–147 |
| f_new = R f; f_new_v = b_v R² f + R f_v; f_new_vw = 2 b_v b_w R³ f + b_v R² f_w + b_w R² f_v + R f_vw, with Rⁿ as repeated division | `_apply_resolvent_jet` L150–186 (b_v R² f_w at L175, b_w R² f_v at L175–176) |
| 24 histories, prefixes S1→S2→S3, D checks (2; 2 or 4; 2) before any inversion | L563–599 |
| Start from (psi, 0, 0); contract with conj(psi); sum over 24 | L601–635 |
| Fail closed on finite, imaginary, positivity of J, and Hessian symmetry; no symmetrization | L637–681 |
| Units: J E⁻³, J_v E⁻⁴, J_vw E⁻⁵, j_vec E | L239 |
| Scope and qualification | L240–264 |

## Static identities (to be checked later, not run now)

With j_v = j for every v:
1. c(S, j_vec) = Ud D + mu0 Σa − 4 j D, which is 0384's c(S, j). So **J equals the 0384 J**.
2. Σ_v R_v = (Σ_v b_v) R² = 4D R² = R′, so **Σ_v J_v equals the 0384 Jprime**.
3. Σ_vw R_vw = 2 (4D)² R³ = 32 D² R³ = R″. The jet is linear in these, so **Σ_vw J_vw equals the 0384 Jsecond**.

Each equality holds exactly in exact arithmetic. Floating-point results should agree only to roundoff, because the code computes Σ_v j_v b_v and 0384 computes 4.0·j·D.

Further statements to check later:
- J_vw = J_wv.
- In the stoquastic gauge the 0384 review describes, R ≥ 0 entrywise and b_v ≥ 0, so J_v ≥ 0 and J_vw ≥ 0 entrywise. These are reported as `min_real_J_v` and `min_real_J_vw` but are not gated (see choice 3 below).

## Retained qualification (0385, explicit)

For a fixed real profile c, the lower-order contact is

  −∂_c² E^(2) = 32 h² Σ_edges r_(3,σ_e) (c_u + c_v)².

This matches assembly L333 in its current bytes. A uniform incidence count can make its uniform specialization scalar; a nonuniform source need not.

The square coefficient computed here is NOT the sole leading spatial response. These terms remain separate and are not set to zero:
- the h² diagonal contact;
- the fourth-order diagonal terms;
- state redistribution;
- coupled-field terms;
- physical-map terms.

No canonical fold enters this four-edge off-diagonal entry, but the separate diagonal folds still belong to the full action. The `scope` string and the `static_notes` repeat this.

## Working-array sizes

| Array | Shape | Elements | Size |
|---|---|---|---|
| f | (4,4,4,4) | 256 | 4 KiB complex128 |
| f_v | (4,4,4,4,4) | 1024 | 16 KiB |
| f_vw | (4,4,4,4,4,4) | 4096 | 64 KiB (the largest array) |
| denominator arrays (14) | (4,4,4,4) float64 | 256 each | 28 KiB total |
| local eigensystems (3) | 4×4 | | |

- Peak live memory in one resolvent step is under about 1 MiB.
- No 256×256 (65536-element) array is ever formed.
- Total work is about 1.2×10⁷ multiply-adds across about 1.8×10³ einsum calls.
- The per-history output, 24 × (1 + 4 + 16) pairs, is well under 32 MiB.

## Choices beyond the literal text (for the reviewer)

1. **Hessian symmetry gate.** The gate is max|J_vw − J_wv| ≤ resid_tol·max(1, max|J_vw|), using the fixed tolerance set; no new tolerance was added.
   - The cross term is evaluated as (b_v R² f_w + b_w R² f_v). IEEE addition is commutative, so this grouping is expected to give a residual of zero or roundoff size.
   - This is not symmetrization: J_vw is returned entry by entry exactly as computed.
2. **Imaginary-part gate.** The 0384 form, |Im| ≤ imag_tol·max(1, |Re|), is applied to all 21 sums (J, the 4 J_v, the 16 J_vw).
3. **Positivity gate.** Re J > 0 is gated as in 0384. 0385 states no sign for J_v or J_vw, so their minimum real parts are reported only.
4. **Unchanged from 0384.** The orthonormality residual, gap > pos_tol, use of all 256 eigenvalues as denominators, absolute herm and resid tolerances, and strict input admission.
5. **j_vec admission.** Only a list, tuple or shape-(4,) ndarray is accepted. Other sequence types, numpy scalars, 0-d arrays and boolean or complex elements are rejected.

## Unresolved points

- Whether the Hessian symmetry gate should scale with max|J_vw| or have its own tolerance; the signature fixes the tolerance set.
- Whether J_v ≥ 0 and J_vw ≥ 0, which the gauge argument implies, should be gated.
- The 0384 review's open points carry over unchanged:
  - eigh thread pinning at launch (N1);
  - tolerance forms and units (N2, N3);
  - pos_tol also gating the gap (N4).
- The assembly file keeps changing. 0385 is pinned as the authority above.

## Execution statement

The module was never executed or imported, and no tests, numerical examples or calculations were run. The only Python run on it was AST parsing:
- `ast.parse` as a syntax check, which passed;
- an AST walk that listed einsum calls and their keyword arguments, MatMult nodes, module-level node types and the signature.

The walk found 11 einsum calls, all with optimize=False, and no MatMult. Module level holds only Import and FunctionDef nodes. The function has 17 required keyword-only arguments.

The files were drafted in the session scratchpad and then created here exclusively. No network was used. Nothing was written under /Users/bgm/Research/Universal Network Theory.
