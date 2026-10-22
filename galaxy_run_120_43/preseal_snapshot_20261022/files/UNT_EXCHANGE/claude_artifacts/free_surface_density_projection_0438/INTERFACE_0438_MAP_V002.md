# INTERFACE 0438 MAP V002: batched density-projection map (Claude2, map c2v002)

Module: `free_surface_density_projection_map_c2v002.py` in this directory. sha256 `7015470d186acab3ffe6cb21aa105ae60e0c0b4d96effa3a79f15c4c14019947`. numpy only, inert at import, no I/O.

Supersedes map c2v001 (`free_surface_density_projection_map_c2v001.py`, 1422ace7b8a544bd48b3c9ef36454831ad99a7cd354be148b353bc29b641fcee; interface `INTERFACE_0438_MAP_V001.md`, e71e7468df814746d597038a1ad60de45e6c1c8c211110e006ce9e5bcaa9741d). c2v001 is left in place, unchanged.

Fix delta: `FIX_DELTA_0438_MAP_V002.md` (diff and rationale).

## What changed from c2v001
The change resolves note 1 of `REVIEW_0438_MAP_V001.md` (1013905ba262e807ad7e551c160760facf6fdb876a6ce1bbd49282232e9e9976, PASS_WITH_NOTES).

**The defect.** In c2v001, a batch's B was stored in the retained B array and the batch was appended to `B_assembled_batches` before any finiteness test. After a non-finite B, `partial_B` therefore held non-finite values for a batch that was listed as assembled.

**The fix.** c2v002 stores B and appends the batch only after the whole batch's B passes an explicit `numpy.all(numpy.isfinite(Bk))` test (lines 389–391). A non-finite B is never stored, so its `partial_B` columns stay NaN.

**What the new test decides.** It controls retention only. The stop is still decided by the per-block test at line 399, so the following are all c2v001's:
- status, reason, `failed_stage`, `failed_batch` and `failed_block`;
- `completed_block_batch` and `completed_batches`;
- every other retained array.

The code-only AST diff is that single `if` wrapper. No new result key is added. The labelled-unvalidated-key option was not used.

## Signature
`project_density_map(*, value, partial_R, partial_z, weights, radius, rho, xi_R, xi_phi, xi_z, mode, provenance, rhs_batch_size)`

- Every argument is keyword-only and required, with no defaults. A missing, positional or extra argument raises TypeError.
- Every other outcome is returned as a dict.
- `rhs_batch_size` comes only from the caller. It is never chosen internally.

## Equations (0441) and where they are in the code
The `@` in 0441 means the mathematical product. Every product here is `numpy.einsum(..., optimize=False)` with explicit subscripts. The code never uses `@`, dot, matmul, vdot, inner, tensordot or linalg.norm.

| Equation | Lines (c2v002) |
|---|---|
| `M = V.conj().T @ (W[:,None]*V)`: `einsum("il,lj->ij", VH, W[:,None]*V)`, formed once | 332, 334 |
| Exact block-diagonal check of M, then the 72 diagonal 8x8 blocks copied once into `M_blocks` | 337–340, 343, 362 |
| Per-block SVD diagnostics (no threshold) | 345–361 |
| `(W*rho)` and `(W*rho/R)`, formed once | 368, 369 |
| B, radial term: `VR.conj().T @ ((W*rho)[:,None]*xi_R)`, `"il,lk->ik"` | 366, 376, 377 |
| B, azimuthal term: `- 1j*mode*V.conj().T @ ((W*rho/R)[:,None]*xi_phi)`, written as `(-1j*mode)*einsum(...)` | 378, 379 |
| B, vertical term: `+ VZ.conj().T @ ((W*rho)[:,None]*xi_z)` | 367, 380, 381 |
| B summed for the batch's columns | 383 |
| **New:** B retained and the batch listed in `B_assembled_batches` only if the whole batch's B is finite | 389–391 |
| Block solve: `numpy.linalg.solve(M_blocks[i], B[8i:8i+8, batch])`, with multiple RHS, after the per-block isfinite test of M block and B block | 395–410 |
| `G = V @ coefficients`: `"ij,jk->ik"` | 415 |
| Direct residual `M coefficients - B`, using the assembled M | 417 |
| Residual norms per (block, column) and per column, via einsum | 420, 421 |
| Mass integral `dot(W, G[:,j])`: `"l,lk->k"`, unconjugated and not forced to zero | 423 |

The code never uses a ridge, clipping, pinv, lstsq, a dense inverse, a tolerance, hidden weights, rescaling or an acceptance flag. W enters each integral exactly once.

Exception handlers:
- (FloatingPointError, RuntimeWarning) at 286;
- KeyboardInterrupt at 291;
- Exception at 293 and 453;
- LinAlgError at 351 and 404.

The only linalg calls are `svd` (350) and `solve` (403).

## Validation
Validation is unchanged from c2v001 and the same as in the vector function: exact ndarray types, real float V/VR/VZ (2304,576), positive finite W/R/rho (2304,), exact zero outside the 72 diagonal 32x8 blocks of V, mode an integer 0..8 with bool rejected, and a non-empty provenance. The map adds two rules:
- **xi_R, xi_phi, xi_z:** complex64 or complex128 (real dtypes are rejected), 2-D with identical shape `(2304, nfree)` and nfree ≥ 1. They must be finite, which is checked one batch of columns at a time.
- **rhs_batch_size:** a Python or numpy integer ≥ 1, with bool rejected. Values larger than nfree give a single batch.

A failure returns `status="rejected_input"` with `field` and `reason`.

## Batching and memory
Batch k covers columns `batch_column_ranges[k] = (k*bs, min(nfree, (k+1)*bs))`. For each batch the order is:
1. Assemble B for the batch.
2. If the whole batch's B is finite, retain it and list the batch.
3. Solve blocks 0..71.
4. Compute G, the residual, the norms and the mass integral.

**Mass blocks.** Each mass block is formed once. `numpy.linalg.solve` LU-factorizes the 8x8 block on each (block, batch) call, so with `rhs_batch_size ≥ nfree` each block is factorized exactly once.

**Memory.** The memory description is c2v001's:
- **Batch-independent:** the `W[:,None]*V` temporary while M is assembled (10.6 MB), M itself (2.65 MB) and the validation masks (about 1.6 MB).
- **Results:** 65,112 B per column of nfree.
- **Per-batch temporaries:** at most (4·2304 + 8·576)·16 B ≈ 221 KB per batch column, plus about 0.6 MB of einsum buffering.

The new test adds one boolean temporary of 576 B per batch column. It is created after X and the three B-term arrays have been released, so it stays inside that bound.

| bs | Batch-loop memory, c2v001 (tracemalloc, full-size stubs, nfree=64) |
|---|---|
| 1 | 0.56 MB |
| 4 | 0.95 MB |
| 16 | 2.82 MB |
| 64 | 6.07 MB |

These measurements were not repeated for c2v002.

## Returns, `status="computed"`
These are identical to c2v001, and every key is bitwise equal on the fix-author runs below.
- **Results:**
  - `coefficients` (576,nfree), `G` (2304,nfree) and `B` (576,nfree), all complex128;
  - `residual` (576,nfree), `residual_block_column_norm` (72,nfree) and `residual_column_norm` (nfree,);
  - `mass_integral` (nfree,), complex.
- **Mass blocks and diagnostics:** `M_blocks` (72,8,8), `M_offblock_max_abs`, `block_singular_values` (72,8) with their min/max, and `block_condition_number`.
- **Bookkeeping:** `nfree`, `rhs_batch_size`, `n_batches`, `batch_column_ranges`, `completed_block_batch` (all True), `completed_batches`, `B_assembled_batches` (all batches), `n_completed_columns`, `mode`, `layout`, `equation`, `parent_equation_0438`, `assumptions_not_verified` and `not_computed`.

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
  - B columns of batch k are valid if k is in `B_assembled_batches`. A batch is listed only after all of its B entries passed an isfinite test. Columns of batches that are not listed are NaN in both real and imaginary parts (this is new in c2v002);
  - G, residual, norm and mass columns are valid if k is in `completed_batches`.

The primary result keys are None. There is no acceptance flag. An interruption during validation propagates unchanged, because no work exists yet.

Consequences of the fix that callers can rely on:
- `completed_batches` ⊆ `B_assembled_batches`.
- A batch can have completed (block, batch) pairs without being in `B_assembled_batches`. This happens when its B is non-finite only in a later block: the earlier blocks pass the per-block test and are solved. Their coefficients are valid, as `completed_block_batch` says, while `partial_B` for that batch is NaN in full.
- So for the failing batch, retained B is under-reported, never over-reported. This was checked with a full-size case that fails at block 40 of batch 2 (repro D4 below).

The interrupt-window remark of review note 3 still applies. An asynchronous KeyboardInterrupt between the store at 390 and the append at 391 can leave checked, finite values in `partial_B` for a batch that is not listed. That is the safe direction.

## Evidence for c2v002 (synthetic stubs only; `/usr/bin/python3 -I -B`, numpy 2.0.2, python 3.9.6)
`scratchpad` = `/private/tmp/claude-501/-Users-bgm-MB-Work/573ea246-f21c-48d3-b8cc-d28a1f8b2c42/scratchpad`. All runs were made from `scratchpad/r0441v2/fix`.

### 1. Fixture helper script
`fixtures_0438_map_c2v001.py` (b6cecb2363383ec6f9aca32af14927a8a07ea5fed133046d81142b9803ab148f) was run with `--expect-sha256 7015470d…`:

| | |
|---|---|
| Result | **pass=549 fail=0 unresolved=0 info=58, VERDICT=ALL_PASS**, exit 0, 14.7 s |
| `fixture_run_c2v002.out` | 2e62fe4a165aafaaf1d0f13bded33f897eaf55cfa51ca8151dc1459555850fa7 |
| `fixture_run_c2v002.json` | f5c490db39d1877a57af4fae24740d06e06b9cc135c14745d4b40d96d55087bf |

Apart from hashes and timings, the line-by-line output differs from the reviewer's c2v001 run (`scratchpad/r0441/review/review_fixture_run.out`) in one line only: the C0 isfinite call count went from 11 to 12.

### 2. Reproduction of the reviewer's case
`repro_note1_c2v002.py` (e6496bc12478e72ce7cd0b6af964c7f301ff58e1bbe840dd2af7e3d1773c3871) gives **75 PASS, 0 FAIL, 8 INFO**, 4.9 s. Output: `repro_note1_c2v002_run1.out` (ce725715a0d6ecacb257b7c0fc9506d17650b6d17cafd9a5179ec6cd2672413e).

**D: the reviewer's R7d default-errstate batch-2 overflow, reproduced exactly.** Inputs: `make_stub(11)`, `make_xi(41, 7)`, mode 3, bs 2, and `xi_R[70, 4] = 1e308`, where row 70 has the largest W·rho (5.884).

| | c2v001 | c2v002 |
|---|---|---|
| `B_assembled_batches` | [0, 1, 2] | [0, 1] |
| `partial_B` column 4 | 576 non-finite entries | NaN (real and imaginary) |
| `partial_B` column 5 | 576 finite entries | NaN (real and imaginary) |

In c2v002, all 1152 entries of `partial_B[:, 4:6]` are NaN in both parts, and batches 0 and 1 are bitwise equal to the good run.

Unchanged from c2v001, and bitwise equal:
- status `failed_closed_solve`;
- reason "non-finite M block or B block [stage: block solves; batch: 2; block: 0]";
- `failed_stage`, `failed_batch` and `failed_block`;
- `completed_block_batch` (144 pairs) and `completed_batches` [0, 1];
- every other key, and `partial_B` outside batch 2.

One RuntimeWarning still reaches the caller, so nothing is suppressed. No `failed_batch_B_unvalidated` key exists.

**D2, D3: the same input under `errstate(all='raise')` and under a warnings "error" filter.** Every key is bitwise equal to c2v001: `failed_closed_floating_point`, stage "assembly of B", `B_assembled_batches` [0, 1].

**D4: B non-finite only in the block-40 rows of batch 2.** Inputs: `VR[1000, :] = 0` except 1e10 on block 40's columns, and `xi_R[1000, 4] = 1e300`.
- Both versions fail at (block 40, batch 2) with 40 pairs of batch 2 completed.
- c2v002 leaves batch 2 unlisted, with `partial_B` NaN in full. c2v001 lists it, with 8 non-finite entries out of 1152.
- Every other key is bitwise equal.
- Observation on numpy 2.0.2 / arm64: this einsum overflow raised no RuntimeWarning, and the explicit isfinite tests caught it.

**F1–F6 and G: other paths, every key bitwise equal to c2v001.**

| Case | Failure path |
|---|---|
| F1 | Non-finite solve at (5, 1) |
| F2 | KeyboardInterrupt at (40, 2) |
| F3 | LinAlgError at (0, 3) |
| F4 | ValueError at (2, 1) |
| F5 | Singular block 9 |
| F6 | KeyboardInterrupt in M assembly |
| G | Good runs at bs 1, 2 and 7 |

The c2v002 invariants above held in every case.

### 3. Author's fixtures run on c2v002, for information
`scratchpad/r0441/author/fixtures_0441_map.py` (b24a7ced8801eb736070a61c97dad4ad1c2d26a8ab242082d4d907f7277966fc) gives **185/186**. Output: `author_fixture_on_c2v002.out` (7e4f29bf0ca98b93b23ace553bd27c49df95396ee160852dd632cc1339bba0c6).

- **The one FAIL is T8b.** It asserts `B_assembled_batches == [0, 1, 2]`, which is the c2v001 behaviour that note 1 removes.
- **Each conjunct of T8b was checked separately** with `t8b_conjuncts.py` (c5bf3dcb468ff066299abf0c84ec18b714863b6388aed22463048ae412a7bd41; output af81792cf3e9594760f6c01f0600ecbd0709b8b9b5b25978af4f15e588bf533d). Every conjunct holds on c2v002 except that one, and c2v002 gives [0, 1].
- **Every other line** of the 186 matches the c2v001 `final_run.out`, apart from the hash and the set-print ordering.

### 4. Evidence carried over from c2v001
The code-only difference is the retention `if`, and computed results are bitwise equal to c2v001. The c2v001 comparisons therefore apply unchanged:
- with the vector function;
- with the dense reference;
- the manufactured, Legendre and conjugation checks;
- call accounting;
- the lane convention.

These are listed in `INTERFACE_0438_MAP_V001.md` and `REVIEW_0438_MAP_V001.md`.

Hashes from bytes: the module 7015470d…; the c2v001 module and every input file were unchanged after all runs. No `__pycache__` was written in the artifact directory.

## Assumptions (stated, not verified) and scope
- The weak form has no surface term, from physical-vacuum vanishing density.
- The radial boundary flux is root-enforced.
- Not computed: pressure, velocity, source response, equilibrium, modal solution, physical acceptance.

Review notes 2–5 are unchanged by this fix:
- KeyboardInterrupt is returned, not re-raised.
- Interrupt windows of one statement remain.
- The SVD diagnostics carry no flag.
- Bitwise observations are not guarantees.

## Private test hook
`_project_density_map_sized(..., n_radii, n_nodes, n_coeffs)` is for reduced-size stubs only.
