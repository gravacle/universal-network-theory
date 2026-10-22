# CHECK 0438 V002 DELTA: c2v001 → c2v002 (lane numerics convention)

**Verdict: PASS_WITH_NOTES.** Nothing is blocking.

**Role:** distinct delta checker. I did not write c2v001, CHECK_0438_V001 or c2v002/FIX_DELTA. I wrote my own diff, AST checks and stubs, and I did not reuse the author's fixtures.

## Inputs (sha256 recomputed from bytes; every one matches the fix report)

| File | sha256 |
|---|---|
| Task `FROM_CODEX/0438_2026-10-16_claude_free_surface_density_projection.md` | 83c963759f875285ce0b33148de1684318cbb81aa4658e1128bede3fe76a5c4c |
| `free_surface_density_projection_c2v001.py` (base, unchanged) | b07fd00875e90e92c396b31103f3306dd8d85fbb1a10a44725f809a1553c6112 |
| `INTERFACE_0438_V001.md` (base, unchanged) | 0879a70bed60c2372f8f73641875dcb686ec0fdcdd2240fdfafd5f5ce5dc6163 |
| `CHECK_0438_V001.md` (base, unchanged) | 738a5029aadf9720c62e5bac728ed36a351855a52b6e211b4b86c10a734605f7 |
| `free_surface_density_projection_c2v002.py` | d1d73bbc178c869f5492bb1bb2e6ec06f9342bffcf73280b1416052bc9f25f8c |
| `INTERFACE_0438_V002.md` | bde6eb0f55eeb2cf79ba05294cb5da0ed8a942d39e26b52fdeb25a0ee954992f |
| `FIX_DELTA_0438_V002.md` | de39f4b772d4f0288b769c16dcc699b856546116272e6a6c58d51bbe941cff02 |
| Author scratch `r0438v2/fixtures_0438v2.py` | ba2ad10b933045a1df775d9bb4de800fe35cc49634714b53eaa6bd07a7832a2b |
| Author scratch `r0438v2/final_run.out` | ac412977d65612a9eedb52e1d877392427a4ef3d5d60d216bbfc76eccad00947 |
| Author scratch `r0438v2/original_fixtures_on_c2v002.out` | 48f9f8d8e15d254efca3c765122b0ee12cb112d0db54401e48c05312e9840ece |
| Author scratch `r0438v2/c2v001_to_c2v002.diff` | 6fcbc53a7cf8db066f03ddc3186f1c213a2179ad590221fe10146ae65f519b68 |
| c2v001 author fixtures `r0438/fixtures_0438.py` (as listed in FIX_DELTA) | 18076dca0ad41833b7579b802d613bf5ddf652735ddf56e7bb8d8ad9bfce8b4a |

My scratch files are in `/private/tmp/claude-501/-Users-bgm-MB-Work/573ea246-f21c-48d3-b8cc-d28a1f8b2c42/scratchpad/r0438v2-check/`:

| File | sha256 |
|---|---|
| `check_0438v2_delta.py` | ee2be5d72ade66c9fbb6a50bdcc06f60182d8db71702b297c0f55d36f405d9ca |
| `check_run.out` (87/87 PASS) | 3e3cc4d034bf213fbc285cfd3e64df98e5fb889299c01b1922ec3d600a8fcd0c |
| `my_diff_body.txt` (my own `diff -u`, without the two header lines) | 4d02dad82a59ca0e816d701cd1222ada4db16cfb0a2aa9b65775ee71819010b9 |

## What was executed
- `shasum -a 256` on every file above.
- My own `diff -u c2v001 c2v002` and `diff -u INTERFACE V001 V002`. My diff body is byte-identical to the author's `c2v001_to_c2v002.diff` and to the diff embedded in FIX_DELTA, lines 156–344.
- `/usr/bin/python3 -I -B check_0438v2_delta.py` (Python 3.9.6, numpy 2.0.2, `signal.alarm(560)`). The script ran on synthetic stubs only and loaded both modules by file path. It appends the numpy user-site path explicitly, because `-I` disables user site. It used no project data and ran nothing under `/Users/bgm/Research/Universal Network Theory`.

## Scope of the change (diff and AST)
- **A9, AST comparison.** Each top-level definition and constant was compared after stripping docstrings. Only `_compute` and `_arithmetic` differ, and `_norm2` is new. The constants, validation, masks, `_result`, `_reject` and `_project_density_sized` are AST-identical. `project_density` differs only in its docstring, and the module docstring is the only other change.
- **Products.** I checked each einsum in the diff against the product it replaces. Each subscript is the same contraction as the original product.

  | Quantity | c2v001 | c2v002 |
  |---|---|---|
  | M | `VH @ X` | `"il,lj->ij"` |
  | three b terms | `·.conj().T @ v` | `"il,l->i"` |
  | delta_rho | `V @ a` | `"ij,j->i"` |
  | residual | `M @ a - b` | `"ij,j->i"`, then `- b` |
  | mass diagnostic | `np.dot(W, δρ)` | `"l,l->"` (unconjugated) |
  | norm | `linalg.norm` | `_norm2`, numpy's own formula `sqrt(re·re + im·im)` |

- **Conjugation.** There are still exactly three `.conj().T`, on V, VR and VZ (A7: 3 and 3).
- **AST convention checks (A1–A5).**
  - There is no `@`.
  - No dot, matmul, vdot, inner, tensordot, norm, outer, kron or multi_dot is named.
  - No errstate, seterr, seterrcall or warnings-filter call is named.
  - There is no `with` statement.
  - All 9 einsums have literal subscripts and `optimize=False`.
  - `linalg` is used only for `solve`, `svd` and `LinAlgError`.
  - The only import is numpy.
- **isfinite.** There are 8 call sites in both versions (A6).
- **The only other edits, all needed by the convention or the fail-closed handler:**
  - `out`, `a` and `fail` are created before assembly.
  - `state` tracks progress.
  - The condition number is computed without dividing by an exact zero. The values are unchanged: inf for a zero sv_min, NaN for a skipped block, and the ratio elsewhere.
  - The residual norms and the dot diagnostic are computed into locals before any key is set.

## Results of my stubs (87/87 PASS)
- **B: full size (72×32×8) through the public API, modes 0..8.**
  - The stub is random block-diagonal V with dense VR and VZ.
  - Both versions return `computed` with no warnings and identical key sets, for every mode.

  | c2v002 compared with | Quantity | Worst relative difference over modes 0..8 |
  |---|---|---|
  | c2v001 | a | 2.7e-15 |
  | c2v001 | delta_rho | 2.3e-15 |
  | c2v001 | b and its terms | 2.5e-15 |
  | c2v001 | dot_W_delta_rho | 4.1e-15 |
  | c2v001 | M_blocks, singular values, cond | 0 (bitwise) |
  | independent reference (pairwise `np.sum`, no BLAS or einsum; per-block solve) | a | 1.1e-15 |
  | independent reference | delta_rho | 1.1e-15 |
  | independent reference | b | 0 |
  | independent reference | M | 4.2e-16 |

  - The off-block maximum is exactly 0 in both versions.
  - The residual global norm is about 4e-13 in both, against max|b| of about 2.1e2 to 2.7e2.
- **C: complex V, VR and VZ through `_compute` (reduced core).**
  - b equals the conjugated reference to 2.4e-16, and c2v001 to 1.8e-16.
  - M blocks equal V^H W V.
  - delta_rho = V·a and dot(W, δρ) are unconjugated, the same as c2v001.
- **D: caller `np.seterr(all="raise")` with finite input.**
  - Modes 0..8 all return `computed`, bitwise equal to the default-errstate run.
  - The caller's errstate is unchanged after each call.
  - The run is also `computed` and bitwise equal under raise plus `warnings.simplefilter("error")`, and under default errstate plus warnings "error".
- **E: overflowing inputs fail closed with blocks retained.**

  | Case | Settings | Result |
  |---|---|---|
  | E1: V block 4 scaled by 1e160, so the einsum overflow is silent and M_4 = inf | default and raise | `failed_closed_solve`, failed_block 4, completed 4. The 32 retained coefficients are bitwise equal to the unperturbed run. Same outcome as c2v001. No warnings. |
  | E2: M_6 diagonal with a 2e-306 entry and b_6[7] about 1e11, so the solve result overflows | default and raise | `failed_closed_solve`, failed_block 6, completed 6 (cond_6 = 1.8e306). Same outcome as c2v001. |
  | E3: ρ·ξ_R = 1e200·1e200 at a block-5 node (elementwise assembly overflow) | raise | `failed_closed_floating_point`, stage "assembly of M and b", completed 0. a and δρ are None, and no b or residual keys are present. |
  | E3 | warnings "error" | `failed_closed_floating_point`, from a RuntimeWarning |
  | E3 | default | 2 visible RuntimeWarnings, then `failed_closed_solve` |
  | E3 | ignore | silent `failed_closed_solve`. c2v001 gives `failed_closed_solve` silently in all four settings. |

- **F: injected exceptions.**

  | Injected | Result |
  |---|---|
  | `FloatingPointError` at the block-5 solve | `failed_closed_floating_point`, stage "block solves", failed_block 5, completed 5. The 40 coefficients are bitwise equal to the good run, b and M_blocks are kept, and there are no residual keys. |
  | `RuntimeWarning` at the block-5 solve | same as above |
  | `FloatingPointError` in `_norm2` | all 72 blocks (576 coefficients) retained bitwise, failed_block None, no residual or dot keys |
  | `ValueError` | `failed_closed_internal`; the outer guard is unchanged |

- **G: probes.**
  - Under raise, `einsum(optimize=False)` is silent on both overflow (inf) and underflow (0), as INTERFACE V002 states.

## Notes (none blocking)
1. **A diagnostic overflow under raise now ends the call with nothing retained** (measured in G).
   - **Case:** a finite block whose cond exceeds about 1.8e308 (block 6 diagonal, one column scaled by 1e-156, so sv_min is of order 1e-312).
   - **Results:**

     | Version, setting | Result |
     |---|---|
     | c2v002, `np.seterr(all="raise")` | `failed_closed_floating_point` at "off-block check and block diagnostics", completed 0 |
     | c2v001 on the same input | `failed_closed_solve` at block 6, completed 6 |
     | c2v002, default errstate | `failed_closed_solve` at block 6, completed 6, plus one visible "overflow encountered in divide" |

   - **Cause:** c2v001 computes the diagnostics before the solves, and the convention now lets the caller's errstate act there.
   - INTERFACE V002 documents this behaviour. It is not a defect of the delta.
   - Getting retention in this case would mean moving the diagnostics after the solves. That is a change beyond the convention, so it should come in a separate version, if anyone wants it.
2. **Under `all="raise"`, underflow fails the call.** With ρ = 1e-300 and ξ_z = 1e-20, c2v002 returns `failed_closed_floating_point` ("underflow encountered in multiply"). Under the default errstate the same input is `computed`. This is documented. It matters near vanishing-density surfaces only if the root caller sets `under="raise"`.
3. **A genuine floating-point exception cannot retain some blocks but not others.** In the code as written, 0 < completed < 72 cannot arise from one:
   - assembly and diagnostics run before the solves;
   - the solve loop contains no ufunc that honours errstate, because `linalg.solve` sets its own.

   Genuine overflowing inputs that fail with partial retention arrive as `failed_closed_solve` through `isfinite` (E1, E2), exactly as in c2v001. The `failed_closed_floating_point` retention path is verified by injection only, both by me and by the author.
4. **The author's choice to also catch `RuntimeWarning` is accepted.**
   - It is consistent with the fail-closed contract: without it, the warnings-"error" route would land in `failed_closed_internal` and lose the retained blocks.
   - The catch also covers subclasses of RuntimeWarning, such as numpy's ComplexWarning. The arithmetic path has no complex-to-real cast, so no such subclass can be raised there today.
   - It is reversible as FIX_DELTA describes.
5. **Exceptions no longer propagate to the caller.** As the brief specifies, a `FloatingPointError` or an escalated RuntimeWarning comes back as a status dict with `failed_stage` and `floating_point_exception`.
6. **Key order changed, key set did not.** The insertion order of keys in the result dict is different: mode, n_blocks and block_size now come before b. Only a consumer that depends on dict order would notice.
7. **Running numpy under `-I`.** `python3 -I` disables user site, and numpy 2.0.2 lives in `~/Library/Python/3.9/lib/python/site-packages`. Both my stubs and the author's fixtures add that path explicitly.
