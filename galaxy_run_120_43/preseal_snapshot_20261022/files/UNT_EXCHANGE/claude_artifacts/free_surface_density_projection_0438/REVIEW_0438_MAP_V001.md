# REVIEW 0438 MAP V001: `project_density_map` (map c2v001)

Role: distinct reviewer, not author. I wrote neither the map module nor either fixture set.
Date: 2026-10-16. Scope: the 0441 Claude2 map extension only. Synthetic stubs only; no project data, no project runs, nothing written under `/Users/bgm/Research/Universal Network Theory`.

## Verdict: PASS_WITH_NOTES

No blocking issues. The module implements the 0441 equations and signs exactly, forms each 8x8 mass block once, solves each block against multiple right-hand sides, respects the caller's `rhs_batch_size`, retains correct completed (block, batch) prefixes on every failure path tested, and meets the lane convention. The notes below are about the retention bookkeeping text and caller obligations, not the arithmetic.

## Hashes (sha256, computed from bytes by this reviewer)

| File | sha256 |
|---|---|
| `FROM_CODEX/0441_2026-10-16_parallel_lane_execution_addendum.md` | a5cab71ad8a296760c5cab455c8b56a18fe61344e1189bc19d57a10b99cc5987 (matches) |
| `FROM_CODEX/0438_2026-10-16_claude_free_surface_density_projection.md` | 83c963759f875285ce0b33148de1684318cbb81aa4658e1128bede3fe76a5c4c (matches) |
| `free_surface_density_projection_map_c2v001.py` (under review) | 1422ace7b8a544bd48b3c9ef36454831ad99a7cd354be148b353bc29b641fcee (matches author; unchanged after all runs) |
| `INTERFACE_0438_MAP_V001.md` | e71e7468df814746d597038a1ad60de45e6c1c8c211110e006ce9e5bcaa9741d (matches author) |
| `free_surface_density_projection_c2v001.py` | b07fd00875e90e92c396b31103f3306dd8d85fbb1a10a44725f809a1553c6112 (unchanged) |
| `free_surface_density_projection_c2v002.py` | d1d73bbc178c869f5492bb1bb2e6ec06f9342bffcf73280b1416052bc9f25f8c (unchanged) |
| `CHECK_0438_V001.md` | 738a5029aadf9720c62e5bac728ed36a351855a52b6e211b4b86c10a734605f7 |
| `CHECK_0438_V002_DELTA.md` (exists, so c2v002 is the primary comparator) | faef4cd215b47283a81ceed5406abfd8d2c40a65caf86be224b3f043d1e72271 |
| `fixtures_0438_map_c2v001.py` (fixture helper) | b6cecb2363383ec6f9aca32af14927a8a07ea5fed133046d81142b9803ab148f (matches helper) |
| author `scratchpad/r0441/author/fixtures_0441_map.py` | b24a7ced8801eb736070a61c97dad4ad1c2d26a8ab242082d4d907f7277966fc (matches author; hash only, not re-run) |
| author `scratchpad/r0441/author/final_run.out` | ab1665964ad01e983df40d12c85630691f4f93d1400d15f2d8845127819a7c1a (matches; 186/186 PASS) |
| helper `scratchpad/r0441/fixtures/run_map_c2v001.out` / `.json` | 3b8e4cc48f63cebb0c5d2f50c97750a69583a75b5e8d5225ff624c35aba6c8ce / 18fd248c40d12c42ba4610ff1060bc99b798478d238739b22b20847d8178c799 (match) |
| reviewer `scratchpad/r0441/review/review_fixture_run.out` | 8c5aca3dc6d39a489808369f5db1d9ad07f8c25102cec9fb55deb051e3bfc02f |
| reviewer `scratchpad/r0441/review/review_fixture_run.json` | 3dad7ee959348a4fcc7420840a84c8e86ac3c8bee11a173419f0a961cecd750d |
| reviewer `scratchpad/r0441/review/review_spot_checks_0441.py` | 67af1f9e240a4e78316370164a33126653b2076d6b265263fd65041e87ee77ea |
| reviewer `scratchpad/r0441/review/review_spot_checks_run1.out` | 04c6d03903558a7174f6184d0fea1cadfb87823adda56bc8591424f83018be21 |

`scratchpad` = `/private/tmp/claude-501/-Users-bgm-MB-Work/573ea246-f21c-48d3-b8cc-d28a1f8b2c42/scratchpad`.

## What was executed

Environment: `/usr/bin/python3 -I -B` (3.9.6), numpy 2.0.2 appended from the user site, arm64 macOS. No `__pycache__` was written in the artifact directory or the review directory.

1. **Fixture helper's script against the map module**, run from `scratchpad/r0441/review`:
   `python3 -I -B fixtures_0438_map_c2v001.py <map module> project_density_map --expect-sha256 1422ace7... --out review_fixture_run.json --timeout 300`
   Result: **pass=549 fail=0 unresolved=0 info=58, VERDICT=ALL_PASS, exit 0, 14.9 s.** Identical counts to the helper's own run. No keymap was needed.
2. **Reviewer spot checks** (`review_spot_checks_0441.py`, written independently of both fixture sets; random block-diagonal V, dense VR and VZ, random positive W, R, rho, random complex maps; full public shape 2304x576). Result: **181 PASS, 0 FAIL, 16 INFO, 22.7 s.**

## Findings by review item

**Modal sign and conjugate transposes.** Line 373: `b_azimuthal = (-1j * mode) * einsum("il,lk->ik", VH, (W*rho/R)[:,None]*xi_phi)`. The radial term uses `VR.conj().T` (360, 371), the vertical term `VZ.conj().T` (361, 375), the azimuthal term `V.conj().T` (326, 373). xi is never conjugated. `(W*rho/R)` is evaluated as `(W*rho)/R`, the literal 0441 grouping (363). Checks:
- Manufactured exact case (VR = VZ = V, xi_R = V C1/rho, xi_phi = R V C2/rho, xi_z = V C3/rho): coefficients = C1 − 1j·m·C2 + C3 to 1.2e-15 for m = 0, 2, 7; the +1j variant is off by 1.5–1.9 (relative).
- Conjugation identities with real V, VR, VZ (mode 3): B(conj ξ) = +conj(B(ξ)) for ξ_R and ξ_z, and −conj(B(ξ)) for ξ_phi, each bitwise; the opposite sign is off by 2.0.
- Azimuthal term alone equals −4j·Vᵀ((W rho/R) ξ_phi) to 1.5e-16 at m = 4; at m = 0, B does not depend on ξ_phi (bitwise).

**Mass blocks formed once; multiple-RHS solves; no inverse.** M is assembled once by one `einsum("il,lj->ij")` (328); the 72 diagonal blocks are copied once into `M_blocks` (337) and reused by every batch. A `solve` spy with nfree = 5, bs = 2 recorded exactly 216 = 72·3 calls, each (8,8) against (8,w) with w = 2,2,1, and the matrix passed for block i was bitwise identical in every batch. An einsum spy saw the M subscript exactly once among 31 einsum calls. `inv`, `pinv` and `lstsq` were patched to raise and were never called. No ridge, clipping, tolerance or rescaling appears in the source. `numpy.linalg.solve` re-runs LU on the same 8x8 block for each batch; that is allowed by 0441 (the block is formed once) and costs nothing material.

**Equality with a dense reference and with the vector function column by column.**
- Independent dense reference (full 576x576 M, B with the 0438 grouping, dense solve; test side only), modes 0, 1, 5, 8 × bs 1, 2, 5, 7, nfree = 5: coefficients ≤ 6.2e-16, G ≤ 7.0e-16, B ≤ 6.7e-16, mass integral ≤ 2.4e-15 (relative); M_blocks, singular values, condition numbers and residual norms agree bitwise; residual recomputed from the dense M agrees to 4.4e-16 of max|B|.
- c2v002 `project_density` called column by column (modes 1 and 5, bs 2): a 6.1e-16, delta_rho 6.9e-16, b 5.9e-16, residual 6.9e-16, mass 1.8e-15; M_blocks and singular values bitwise equal.
- c2v001 the same way: a 2.7e-15, delta_rho 2.6e-15, b 3.0e-15, mass 7.4e-15; M_blocks bitwise equal.
- Batch-size results were bitwise identical across bs 1, 2, 5, 7 for each mode on this machine (an observation, not a guarantee); a bs of 10^18 gives one batch and the bs = nfree result bitwise.

**rhs_batch_size handling and memory bound.** Required keyword, no default; Python or numpy integer ≥ 1; bool, numpy bool, float, str, None and 0-d arrays rejected with zero solves. Batches are `range(0, nfree, bs)` (261). Per-batch temporaries are created inside the loop and released (`del` at 376, 378). tracemalloc, measured from the first block solve onward (so it covers later batches' B assembly, the solves, G, the residual and the norms):

| nfree | bs | loop peak above entry |
|---|---|---|
| 128 | 1 | 0.51 MB |
| 128 | 8 | 1.38 MB |
| 128 | 64 | 9.16 MB |
| 512 | 8 | 1.38 MB |

The peak grows with bs, does not depend on nfree, and stays inside the author's stated bound of (4·2304 + 8·576)·16 B per batch column plus about 0.6 MB. The fixed cost of M assembly (the 10.6 MB `W[:,None]*V` temporary plus 2.65 MB for M) and the result arrays (65,112 B per column) are outside the batch bound, as the interface says.

**Saved failure prefixes.** In every case below the primary result keys were None, no key mentions acceptance, `completed_block_batch` equalled the pairs actually solved, `failed_block`/`failed_batch` named the failing pair, retained `partial_coefficients` matched the good run bitwise where marked complete and were NaN elsewhere, retained G, residual, norms and mass matched the good run bitwise for completed batches and were NaN elsewhere, and the mass blocks and SVD diagnostics were retained (nfree = 7, bs = 2, 4 batches):
- non-finite solve result injected at (block 5, batch 1) → `failed_closed_solve`;
- KeyboardInterrupt injected at (block 40, batch 2) → returned as `interrupted`;
- LinAlgError injected at (block 0, batch 3) → `failed_closed_solve`;
- finite-input overflow (ξ_R = 1e308 at the row with the largest W·rho, column 4, batch 2) under the default errstate (one RuntimeWarning reached the caller, so nothing was suppressed; `failed_closed_solve` at block 0, batch 2), under `errstate(all='raise')` and under a warnings "error" filter (both `failed_closed_floating_point` in "assembly of B", batch 2);
- KeyboardInterrupt in the first einsum (M assembly) → `interrupted`, stage "assembly of M", nothing marked complete, all partials NaN;
- a singular block (one zero V column in block 9) → `failed_closed_solve` at (9, 0) with 9 pairs complete.

The same finite data computed bitwise-identical results under `errstate(all='raise')` combined with a warnings "error" filter.

**Validation.** 32 reviewer rejection cases, each returning `rejected_input` with the right `field` and zero solves: ξ shape mismatches (wider, narrower, 1-D, 3-D, wrong row count, nfree = 0), real-dtype ξ, NaN in the last batch's columns, inf, `np.matrix` and list inputs, eight bad `rhs_batch_size` values, four bad modes, blank and bytes provenance, a 1e-300 off-block V entry, integer V, complex VR, a short VZ, zero W, infinite R and negative rho. A clongdouble case was skipped because clongdouble is complex128 on arm64. Positional calls, a missing `rhs_batch_size` and an extra keyword raise TypeError. complex64 ξ gives the exact complex128 upcast bitwise; Fortran-ordered ξ agrees. Validation is otherwise the vector function's, line for line (178–235 against c2v002 `_validate`).

**Lane convention (AST of the module text).** No `@` or `@=`; no `dot`, `matmul`, `vdot`, `inner`, `tensordot`, `multi_dot`, `norm`, `inv`, `pinv`, `lstsq`, `errstate`, `seterr`, `filterwarnings`, `simplefilter`, `catch_warnings`, `nan_to_num` or `clip`; imports are numpy only; all 11 einsum calls pass `optimize=False` (and every einsum seen at runtime had `optimize=False`); the only linalg calls are `solve` (392) and `svd` (344). Exception handlers: (FloatingPointError, RuntimeWarning) at 280, KeyboardInterrupt at 285, Exception at 287 and 442, LinAlgError at 345 and 393. Incidental evidence for the convention: the reviewer's own test-side BLAS `@` references emitted spurious "divide by zero / overflow / invalid encountered in matmul" RuntimeWarnings on finite data on this machine (36 lines in `review_spot_checks_run1.out`), while the module's einsum path produced none under `errstate(all='raise')`.

## Blocking issues

None.

## Notes (non-blocking)

1. **`partial_B` of the failing batch is stored before its finiteness test.** `store["B"][:, c0:c1] = Bk` and `B_assembled_batches.append(k)` (379–380) run before the per-block isfinite test (388). In the default-errstate overflow case, `partial_B` column 4 held 576 non-finite entries while batch 2 was listed in `B_assembled_batches`. The interface says partial entries are "NaN unless they completed and passed their checks" and that B columns of batch k "are valid if k is in B_assembled_batches"; neither holds for the batch named in `failed_batch`. Callers should treat `partial_B[:, failed batch]` as unchecked. A successor should either correct that sentence or list the batch only after its B passes the finiteness test. Coefficients, G, residual, norms and mass are masked correctly.
2. **KeyboardInterrupt is returned, not re-raised** (285–286). This satisfies 0441's retention requirement, but a driver that loops over modes or map sets will keep running after Ctrl-C unless it tests `status == "interrupted"` and stops. Root's driver must do that.
3. **Interrupt windows of one statement.** Between storing and recording (379→380, 398→399, 416–420→421), and during the post-processing at 289–306 and 446–453, an asynchronous KeyboardInterrupt can either leave valid, checked values in a partial array that the bookkeeping does not list (the mask only ever under-reports, which is the safe direction) or, in the last two spans, propagate and lose the dict. This is narrow and cannot be fixed fully in Python; recorded for completeness.
4. **Diagnostics share the vector function's behaviour.** An SVD that fails to converge leaves NaN singular values with no flag (345–346), and an exactly zero smallest singular value gives cond = inf. This is unchanged from c2v002 and has no threshold, as required.
5. The batch-size bitwise invariance and the bitwise equality of M_blocks with the vector versions are observations on numpy 2.0.2 / arm64, not guarantees; all comparisons above pass at tolerance as well.

## Scope

Not reviewed: physics, the free-surface and boundary-flux assumptions (stated, not verified, by the module), the Euler join, or any project-scale run. The author's own fixture set was checked by hash and its recorded output only.
