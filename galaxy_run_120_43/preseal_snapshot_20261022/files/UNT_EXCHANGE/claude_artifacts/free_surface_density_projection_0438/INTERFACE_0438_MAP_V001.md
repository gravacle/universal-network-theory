# INTERFACE 0438 MAP V001: batched density-projection map (Claude2, map c2v001)

Module: `free_surface_density_projection_map_c2v001.py` in this directory. sha256 `1422ace7b8a544bd48b3c9ef36454831ad99a7cd354be148b353bc29b641fcee`. numpy only, inert at import, no I/O.

Tasks: `FROM_CODEX/0441_2026-10-16_parallel_lane_execution_addendum.md` (a5cab71ad8a296760c5cab455c8b56a18fe61344e1189bc19d57a10b99cc5987, Claude2 section) and its parent `FROM_CODEX/0438_2026-10-16_claude_free_surface_density_projection.md` (83c963759f875285ce0b33148de1684318cbb81aa4658e1128bede3fe76a5c4c).

The vector API is preserved unchanged and is not imported:
- `free_surface_density_projection_c2v001.py` (b07fd00875e90e92c396b31103f3306dd8d85fbb1a10a44725f809a1553c6112)
- `free_surface_density_projection_c2v002.py` (d1d73bbc178c869f5492bb1bb2e6ec06f9342bffcf73280b1416052bc9f25f8c)

This is the same 0438 projection applied to each column. It is not a new physical equation.

## Signature
`project_density_map(*, value, partial_R, partial_z, weights, radius, rho, xi_R, xi_phi, xi_z, mode, provenance, rhs_batch_size)`

- Every argument is keyword-only and required, with no defaults. A missing, positional or extra argument raises TypeError.
- Every other outcome is returned as a dict.
- `rhs_batch_size` comes only from the caller. It is never chosen internally.

## Equations (0441) and where they are in the code
The `@` in 0441 means the mathematical product. Every product here is `numpy.einsum(..., optimize=False)` with explicit subscripts. The code never uses `@`, dot, matmul, vdot, inner, tensordot or linalg.norm.

| Equation | Lines |
|---|---|
| `M = V.conj().T @ (W[:,None]*V)`: `einsum("il,lj->ij", VH, W[:,None]*V)`, formed once | 326, 328 |
| Exact block-diagonal check of M, then the 72 diagonal 8x8 blocks copied once into `M_blocks` | 331–334, 337, 356 |
| Per-block SVD diagnostics (no threshold) | 339–355 |
| `(W*rho)` and `(W*rho/R)`, formed once | 362, 363 |
| B, radial term: `VR.conj().T @ ((W*rho)[:,None]*xi_R)`, `"il,lk->ik"` | 360, 370, 371 |
| B, azimuthal term: `- 1j*mode*V.conj().T @ ((W*rho/R)[:,None]*xi_phi)`, written as `(-1j*mode)*einsum(...)` | 372, 373 |
| B, vertical term: `+ VZ.conj().T @ ((W*rho)[:,None]*xi_z)` | 361, 374, 375 |
| B summed for the batch's columns | 377 |
| Block solve: `numpy.linalg.solve(M_blocks[i], B[8i:8i+8, batch])`, with multiple RHS | 384–399 |
| `G = V @ coefficients`: `"ij,jk->ik"` | 404 |
| Direct residual `M coefficients - B`, using the assembled M | 406 |
| Residual norms per (block, column) and per column, via einsum | 409, 410 |
| Mass integral `dot(W, G[:,j])`: `"l,lk->k"`, unconjugated and not forced to zero | 412 |

The code never uses a ridge, clipping, pinv, lstsq, a dense inverse, a tolerance, hidden weights, rescaling or an acceptance flag. W enters each integral exactly once.

## Validation
Validation is the same as in the vector function: exact ndarray types, real float V/VR/VZ (2304,576), positive finite W/R/rho (2304,), exact zero outside the 72 diagonal 32x8 blocks of V, mode an integer 0..8 with bool rejected, and a non-empty provenance. The map adds two rules:
- **xi_R, xi_phi, xi_z:** complex64 or complex128 (real dtypes are rejected), 2-D with identical shape `(2304, nfree)` and nfree ≥ 1. They must be finite, which is checked one batch of columns at a time.
- **rhs_batch_size:** a Python or numpy integer ≥ 1, with bool rejected. Values larger than nfree give a single batch.

A failure returns `status="rejected_input"` with `field` and `reason`.

## Batching and memory
Batch k covers columns `batch_column_ranges[k] = (k*bs, min(nfree, (k+1)*bs))`. For each batch the order is:
1. Assemble B for the batch.
2. Solve blocks 0..71.
3. Compute G, the residual, the norms and the mass integral.

**Mass blocks.** Each mass block is formed once. `numpy.linalg.solve` LU-factorizes the 8x8 block on each (block, batch) call, so with `rhs_batch_size ≥ nfree` each block is factorized exactly once.

**Memory, three parts:**
- **Batch-independent:** the `W[:,None]*V` temporary while M is assembled (10.6 MB), M itself (2.65 MB) and the validation masks (about 1.6 MB).
- **Results:** 65,112 B per column of nfree.
- **Per-batch temporaries:** at most (4·2304 + 8·576)·16 B ≈ 221 KB per batch column, plus about 0.6 MB of einsum buffering.

**Measured on full-size stubs** (tracemalloc, nfree=64), for the batch loop:

| bs | Batch-loop memory |
|---|---|
| 1 | 0.56 MB |
| 4 | 0.95 MB |
| 16 | 2.82 MB |
| 64 | 6.07 MB |

That is about 68–95 KB per column. The assembly stage peaks at 17.4 MB for every bs.

## Returns, `status="computed"`
- **Results:**
  - `coefficients` (576,nfree), `G` (2304,nfree) and `B` (576,nfree), all complex128;
  - `residual` (576,nfree), `residual_block_column_norm` (72,nfree) and `residual_column_norm` (nfree,);
  - `mass_integral` (nfree,), complex.
- **Mass blocks and diagnostics:** `M_blocks` (72,8,8), `M_offblock_max_abs`, `block_singular_values` (72,8) with their min/max, and `block_condition_number`.
- **Bookkeeping:** `nfree`, `rhs_batch_size`, `n_batches`, `batch_column_ranges`, `completed_block_batch` (all True), `completed_batches`, `B_assembled_batches`, `n_completed_columns`, `mode`, `layout`, `equation`, `parent_equation_0438`, `assumptions_not_verified` and `not_computed`.

## Failure and retention format (after validation)
| Status | Cause |
|---|---|
| `failed_closed_solve` | LinAlgError, a non-finite M/B block, solution, G, residual, norm or mass integral, or an M that is not exactly block diagonal |
| `failed_closed_floating_point` | FloatingPointError, or a RuntimeWarning escalated by the caller's errstate or warnings filter; `floating_point_exception` holds the text |
| `interrupted` | KeyboardInterrupt. It is returned, not re-raised, so the caller must test `status` |
| `failed_closed_internal` | Any other exception |

Every failure status keeps:
- **Where it stopped:** `failed_stage` ("assembly of M", "off-block check and block diagnostics", "assembly of B", "block solves", "G, residual and mass integral"), `failed_batch` and `failed_block`.
- **What completed:** `completed_block_batch` (72, n_batches) (`numpy.argwhere` gives the (block, batch) pairs), `B_assembled_batches`, `completed_batches` and `n_completed_columns`.
- **The mass blocks and diagnostics.**
- **`partial_<key>` for each result array.** Entries are NaN unless they completed and passed their checks:
  - coefficients block i of batch k is valid if `completed_block_batch[i,k]`;
  - B columns of batch k are valid if k is in `B_assembled_batches`;
  - G, residual, norm and mass columns are valid if k is in `completed_batches`.

The primary result keys are None. There is no acceptance flag. An interruption during validation propagates unchanged, because no work exists yet.

## Author fixtures (synthetic stubs only; `python3 -I -B`, numpy 2.0.2)
`scratchpad/r0441/author/fixtures_0441_map.py` (b24a7ced8801eb736070a61c97dad4ad1c2d26a8ab242082d4d907f7277966fc) gives **186/186 PASS** on this file (`final_run.out`, ab1665964ad01e983df40d12c85630691f4f93d1400d15f2d8845127819a7c1a).

- **Comparison with independent vector calls.** The primary comparator is c2v002, because CHECK_0438_V002_DELTA exists; c2v001 was also run.

  | Case | Batch sizes | Largest relative difference |
  |---|---|---|
  | Reduced size, modes 0..8 | 1, 2, 3, 7, 50 | ≤ 6.8e-16 |
  | Full size, against c2v002 | 2 | coefficients 8.8e-16, G 8.9e-15, B 8.0e-16 |
  | Full size, against c2v001 | 2 | coefficients 4.6e-15, G 1.6e-14, B 3.1e-15 |

  M_blocks are bitwise equal to both vector versions. The B differences come from the 0441 grouping `(W*rho)*xi` against the vector's `W*(rho*xi)`.
- **Batch-size invariance.** Results were bitwise identical across every bs tested on this machine. This is an observation, not a guarantee.
- **Dense full-solve reference.** Agreement is ≤ 2.2e-14.
- **Manufactured exact solution** (VR=VZ=V, mode 3). The coefficients equal c1+c2+c3 to 5e-16. The +i·mode sign is distinguishable from the -i·mode sign.
- **Analytic Legendre columns.** The radial, the −i·m azimuthal and the vertical 2cz terms are all correct.
- **Conjugation.** B(iξ) = iB(ξ) bitwise.
- **Other input checks.** complex64 input gives the exact upcast, and Fortran-ordered input gives identical results.
- **Validation.** 41 rejection cases pass.
- **Retention:**
  - a singular block (reduced size, and block 37 at full size);
  - overflow in batch 2 under default, raise and warnings-"error" settings;
  - an injected KeyboardInterrupt, ValueError or LinAlgError at (batch 1, block 2);
  - a KeyboardInterrupt during B assembly;
  - a non-finite G;
  - an overflow of M.

  The retained prefixes are bitwise equal to the good run.
- **Call accounting.** `solve` was called exactly 72·n_batches times with shapes (8,8) and (8,width). inv, pinv and lstsq were never called. There was one M einsum, and every einsum used `optimize=False`.
- **Inputs and outputs.** Inputs are unmodified, results are deterministic, and no `__pycache__` was written.

## Assumptions (stated, not verified) and scope
- The weak form has no surface term, from physical-vacuum vanishing density.
- The radial boundary flux is root-enforced.
- Not computed: pressure, velocity, source response, equilibrium, modal solution, physical acceptance.

## Private test hook
`_project_density_map_sized(..., n_radii, n_nodes, n_coeffs)` is for reduced-size stubs only.
