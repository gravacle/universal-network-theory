# CHECK 0438 MAP V002 DELTA: map c2v001 → c2v002 (review note 1)

Role: distinct delta checker. I am not the map author, the reviewer, the fixture helper or the fix author. Date: 2026-10-16. UNT 0441, Claude2 lane.

Synthetic stubs only. No project data, no project-scale runs, nothing written under `/Users/bgm/Research/Universal Network Theory`. All runs used `/usr/bin/python3 -I -B` (3.9.6) with numpy 2.0.2 appended from the user site, in `scratchpad/r0441v2/check`, where `scratchpad` = `/private/tmp/claude-501/-Users-bgm-MB-Work/573ea246-f21c-48d3-b8cc-d28a1f8b2c42/scratchpad`.

## Verdict: PASS_WITH_NOTES

The only code change is the Note-1 retention gate. Statuses, stop locations, equations and every other retention key are unchanged, and successful runs at full size are bitwise identical to c2v001. The interface is accurate. The notes below are non-blocking.

## Hashes (sha256 from bytes, by this checker)

| File | sha256 | |
|---|---|---|
| `free_surface_density_projection_map_c2v001.py` (base) | 1422ace7b8a544bd48b3c9ef36454831ad99a7cd354be148b353bc29b641fcee | matches; unchanged after all runs |
| `free_surface_density_projection_map_c2v002.py` (under check) | 7015470d186acab3ffe6cb21aa105ae60e0c0b4d96effa3a79f15c4c14019947 | matches fix author; unchanged after all runs |
| `INTERFACE_0438_MAP_V001.md` | e71e7468df814746d597038a1ad60de45e6c1c8c211110e006ce9e5bcaa9741d | matches |
| `INTERFACE_0438_MAP_V002.md` | 66995a129565e19b2a4a1a034554ab4895a51c853d6dec6437581fc3f6491293 | matches fix author |
| `REVIEW_0438_MAP_V001.md` | 1013905ba262e807ad7e551c160760facf6fdb876a6ce1bbd49282232e9e9976 | matches |
| `FIX_DELTA_0438_MAP_V002.md` | 8188961ff9bffd44641e0c63e872477969e3ca3646822b6bd267585d7fb8078e | matches fix author |
| `fixtures_0438_map_c2v001.py` (fixture helper script) | b6cecb2363383ec6f9aca32af14927a8a07ea5fed133046d81142b9803ab148f | matches |
| fix author `r0441v2/fix/fixture_run_c2v002.out` / `.json` | 2e62fe4a165aafaaf1d0f13bded33f897eaf55cfa51ca8151dc1459555850fa7 / f5c490db39d1877a57af4fae24740d06e06b9cc135c14745d4b40d96d55087bf | match the fix report |
| fix author `repro_note1_c2v002.py` / `_run1.out` | e6496bc12478e72ce7cd0b6af964c7f301ff58e1bbe840dd2af7e3d1773c3871 / ce725715a0d6ecacb257b7c0fc9506d17650b6d17cafd9a5179ec6cd2672413e | match |
| fix author `author_fixture_on_c2v002.out` | 7e4f29bf0ca98b93b23ace553bd27c49df95396ee160852dd632cc1339bba0c6 | matches |
| fix author `t8b_conjuncts.py` / `_run1.out` | c5bf3dcb468ff066299abf0c84ec18b714863b6388aed22463048ae412a7bd41 / af81792cf3e9594760f6c01f0600ecbd0709b8b9b5b25978af4f15e588bf533d | match |
| author `r0441/author/fixtures_0441_map.py` | b24a7ced8801eb736070a61c97dad4ad1c2d26a8ab242082d4d907f7277966fc | matches |
| reviewer `r0441/review/review_fixture_run.out` (c2v001 baseline) | 8c5aca3dc6d39a489808369f5db1d9ad07f8c25102cec9fb55deb051e3bfc02f | matches the review |

Checker files in `scratchpad/r0441v2/check`:

| File | sha256 |
|---|---|
| `ast_delta_check.py` | e5d398b8b633fc17b9066d14553dc5db0e915c64073a3211e4082d6d97f0eb38 |
| `ast_delta_check_run1.out` | 54048df11960e73ccf7feaee3c2fc0a4a3dab8ea8df434b6e83584de7df07b26 |
| `my_map_diff_body.txt` (my `diff -u` body) | a34c2399f87663d824525fc63df1f0002df9def639fee2665acf6e663025bbe5 |
| `fixtures_0438_map_c2v001.copy.py` (byte copy of the helper script) | b6cecb2363383ec6f9aca32af14927a8a07ea5fed133046d81142b9803ab148f |
| `check_fixture_run_c2v002.out` | 5cb9d7629523ccf90e579d54cd865823b5a9d10e3b28ff34ea2a352ed922a508 |
| `check_fixture_run_c2v002.json` | a3bc9663bd4e94f98f6e0f2d890c9bc9167a0b426f02f22870c47ca135916c5d |
| `check_delta_0441v2.py` (own reproduction) | 2f6691535654f46b623d4b0968758d8b21745d61554f2bc3071d3149f9dd0795 |
| `check_delta_0441v2_run3.out` (record run) | b57f533a04b0a4086eea969f70a0da300331d4977718906c1beffae32e3da2cc |
| `author_fixture_on_c2v002_check.out` | 2d29e684b1dd9d4cc9def04e2875efca3b4467e0b1f869386d91122ea9e676f3 |

Checker-side errors, superseded by run3: `check_delta_0441v2_run1.out` (c11b91ab40de2ce416316dea9d170cebaaa33329a4e021929b30759f2a0a6fe4) had 5 FAILs and a TypeError from my test design. The L1 stub used 1e200 entries, so even the finite reference run failed closed at the residual norm and there was no reference. One line also expected Fortran-order and C-order runs to be bitwise equal, which is outside the delta. `check_delta_0441v2_run2.out` (71ee6c8c02f038d51ba7c8d72a8ab32d552f3d3eb4e0113d3969d81f3861e611) is a SyntaxError in my script. Neither involved the module.

## 1. The delta

**My own `diff -u` c2v001 → c2v002.** There are four hunks:
- three are docstring text: the module docstring header and the retention paragraph, and the `project_density_map` docstring;
- one is code, in `_arithmetic`. The two statements `store["B"][:, c0:c1] = Bk` and `out["B_assembled_batches"].append(k)` are replaced by a four-line comment plus:

```python
if np.all(np.isfinite(Bk)):
    store["B"][:, c0:c1] = Bk
    out["B_assembled_batches"].append(k)
```

The diff embedded in `FIX_DELTA_0438_MAP_V002.md` contains my diff body verbatim.

**AST with docstrings stripped** (`ast_delta_check.py`):
- `_arithmetic` is the only function that differs;
- module-level statements, including the equation and assumption constants, are identical;
- removing the new `if` and keeping its body gives exactly c2v001's AST (`True`).

The fix is therefore the Note-1 bookkeeping alone.

**Lane scan of c2v002.**
- No `@`, `@=`, dot, matmul, vdot, inner, tensordot, multi_dot, norm, inv, pinv, lstsq, errstate, seterr, filterwarnings, catch_warnings, nan_to_num or clip.
- 11 einsum calls, all `optimize=False`.
- The only import is numpy.
- linalg use: `svd` 350, `solve` 403, `LinAlgError` 351 and 404.
- isfinite references go from 11 to 12.

**Why the stop decision cannot change.** The 72 per-block tests at line 399 test `Bk[8i:8i+8]` for i = 0..71. Together these are exactly rows 0..575 of `Bk`. A non-finite `Bk` is therefore always caught at or before its first non-finite block, unless an earlier singular or non-finite solve stops the batch first. A finite `Bk` passes both tests. The new test only gates the two retention statements and returns nothing.

`np.isfinite` on inf/NaN complex values raises nothing and warns nothing under `errstate(all='raise')` together with a warnings "error" filter (S1 PASS). So the gate adds no floating-point stop. Its only new allocation is a 576 B-per-column boolean.

## 2. Interface V002 accuracy

**Line references.** Every line reference in the equation table was checked against c2v002 and is correct:
- M at 332 and 334; the block check at 337–340, 343 and 362; SVD at 345–361;
- the `(W*rho)` and `(W*rho/R)` factors at 368 and 369; B terms at 366/376/377, 378/379 and 367/380/381; the B sum at 383;
- the new gate at 389–391; the block solve at 395–410;
- G at 415, the residual at 417, norms at 420 and 421, mass at 423.

The exception handlers (286, 291, 293, 453, 351, 404) and linalg lines (350, 403) are also correct.

**Statements verified by my runs:**
- `B_assembled_batches` lists a batch only after its whole B is finite;
- a non-finite B is never stored, and unlisted batches are NaN in real and imaginary parts;
- `completed_batches` ⊆ `B_assembled_batches`;
- under-reporting happens for a batch with completed pairs but non-finite B in a later block;
- status, reason and `failed_*` are unchanged;
- computed results are bitwise equal to c2v001;
- no new result key is added;
- the interrupt window between 390 and 391 is in the safe direction.

## 3. Fixture helper script rerun on c2v002

Command: `fixtures_0438_map_c2v001.copy.py <c2v002> project_density_map --expect-sha256 7015470d… --out check_fixture_run_c2v002.json --timeout 300`, using a byte-identical copy of b6cecb23….

Result: **pass=549 fail=0 unresolved=0 info=58, VERDICT=ALL_PASS, exit 0**, 14.8 s.

After masking hashes, timings and the fixture path, my output differs from the reviewer's c2v001 run in one line only: `C0.imports … isfinite calls 11` became `12`. This matches the fix report.

## 4. Own reproduction at full size (`check_delta_0441v2.py`, run3)

Result: **238 PASS, 0 FAIL, 12 INFO**, 13.1 s.

The script loads c2v001 and c2v002 from the artifact directory without bytecode. Inputs are my own stub: block-diagonal random V (2304×576), dense random VR and VZ, W in U(0.2, 1.5), R in U(0.5, 3), rho in U(0.3, 2), and random complex ξ. Both versions run on identical inputs, and every returned key is compared bitwise: arrays by dtype, shape and bytes; floats by bytes. RuntimeWarnings reaching the caller are counted with `simplefilter("always")`, which does not escalate them.

The c2v002 invariants are checked on every failure case:
- `completed_batches` ⊆ `B_assembled_batches`;
- listed batches have finite `partial_B`, bitwise equal to the good run;
- unlisted batches are NaN in real and imaginary parts;
- the `partial_coefficients` mask matches `completed_block_batch`, bitwise equal to the good run where completed;
- partial G, residual, norms and mass are valid only for completed batches;
- primary keys are None;
- there is no `failed_batch_B_unvalidated` key.

| Case | Input | c2v001 | c2v002 | Keys that differ |
|---|---|---|---|---|
| O default | bs 2, nfree 7, mode 3, `xi_R[1801,4]=1e308` (row of max W·rho 2.954) | failed_closed_solve at (block 0, batch 2); listed [0,1,2]; 576 of 1152 `partial_B[:,4:6]` entries non-finite | same status, reason and location; listed [0,1]; batch 2 NaN; batches 0–1 equal to good run | only `B_assembled_batches`, `partial_B` (batch 2 columns) |
| O raise / O warn-error | same input | failed_closed_floating_point, "assembly of B", batch 2 | identical | none |
| L1 (new, last block) | `VZ[1500,:]=0` except 1e150 on block 71's columns; `xi_z[1500,4]=1e160`; bs 3, mode 5 | fails at (block 71, batch 1), 143 pairs; listed [0,1] with 8 non-finite entries | same stop; listed [0]; batch 1 NaN while its 71 completed coefficient blocks equal the good run | only `B_assembled_batches`, `partial_B` |
| L1 raise / L1 warn-error | same input | the same: the einsum overflow raised no FloatingPointError and no warning | same as default | only `B_assembled_batches`, `partial_B` |
| L2 (new, earlier stop) | zero V column in block 3 plus non-finite B in block 50 of batch 0 | "singular M block" at (3, 0); listed [0] with non-finite B | same stop; listed []; batch 0 NaN | only `B_assembled_batches`, `partial_B` |
| L3 (B finite, later failure) | inf injected into G of batch 1 | failed_closed_solve, "non-finite G or residual", batch 1 | batch 1 still listed with finite B | none |
| K1 (new statement) | KeyboardInterrupt raised inside c2v002's new `isfinite(Bk)` for batch 2, compared with c2v001 interrupted at its last B-term einsum of batch 2 | interrupted, "assembly of B", batch 2 | identical | none |
| T1 (note-3 window) | KeyboardInterrupt injected by trace at line 391, batch 1 | n/a | interrupted; listed [0]; `partial_B` batch 1 finite and equal to the good run | (INFO: the documented safe-direction window) |

RuntimeWarning counts were compared in O default (1 and 1) and in L1 under all three settings (0 and 0). They are equal, so nothing is suppressed or added.

## 5. Successful runs at full size are bitwise identical

These use the same full-size stub (2304×576, 72 blocks), nfree 9, and every returned key compared bitwise. All results below are status `computed` with every key bitwise equal between c2v001 and c2v002.

| Runs | Extra checks |
|---|---|
| Modes 0, 3 and 8 × bs 1, 2, 4, 9 and 50 (15 configurations) | `B_assembled_batches == completed_batches == all batches`; no warnings |
| complex64 ξ | — |
| Fortran-ordered V, VR, VZ and ξ | — |
| `errstate(all='raise')` combined with a warnings "error" filter | also equal to the default-settings run |
| A repeated run | deterministic |

The keys compared include coefficients, G, B, residual and norms, mass integral, M_blocks, singular values and condition numbers, layout, equations and bookkeeping.

## 6. Author fixture on c2v002 (information)

`r0441/author/fixtures_0441_map.py` (b24a7ced…) gives **185/186**. The only FAIL is the first T8b check, whose conjunct `B_assembled_batches == [0, 1, 2]` encodes the removed defect. The second T8b check passes: retained G, coefficients, residual and mass of batches 0–1 are bitwise equal to the good run, and batch 2 is NaN.

My output equals the fix author's `author_fixture_on_c2v002.out` apart from hashes, timings and the print order of two Python sets.

## Notes (non-blocking)

1. **Lineage lines dropped.** `INTERFACE_0438_MAP_V002.md` no longer carries the 0441/0438 task-file hashes (a5cab71a…, 83c96375…) or the vector-API hashes (b07fd008…, d1d73bbc…) that V001 listed. It reaches them only through "Supersedes … V001". The module docstring still names b07fd008…. A later interface revision should restore these lines.
2. **"Unlisted batches are NaN" has one exception.** It is the documented note-3 window between lines 390 and 391. T1 shows the effect: finite, checked B equal to the good run, in an unlisted batch. This is the safe direction and is stated in the interface.
3. **Author fixture T8b expects the old behaviour.** Its successor should expect `[0, 1]`.
4. **Silent einsum overflow under every setting.** The fix author saw it under the default errstate. L1 shows the same under `errstate(all='raise')` and under a warnings "error" filter: no exception, no warning. On numpy 2.0.2 / arm64, only the explicit isfinite tests catch einsum overflow. Under raise/error settings, the "failed_closed_floating_point" status therefore covers elementwise overflow but not einsum overflow, which arrives as "failed_closed_solve". This is unchanged from c2v001.
5. **Fortran order is not bitwise C order.** With V, VR, VZ and ξ all Fortran-ordered, results agree with the C-order run to 6.3e-16 relative but are not bitwise equal on this machine. Both versions are identical to each other. This is outside the delta and is consistent with review note 5: bitwise observations are not guarantees.

## Scope

Not checked: the physics, the free-surface and boundary-flux assumptions, the memory measurements (not repeated; the gate adds one 576 B-per-column boolean), or anything at project scale. No `__pycache__` was written in the artifact, check or author directories.
