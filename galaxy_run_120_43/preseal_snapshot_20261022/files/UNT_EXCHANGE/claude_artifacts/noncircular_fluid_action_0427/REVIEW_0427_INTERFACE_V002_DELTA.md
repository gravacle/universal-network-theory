# REVIEW 0427 INTERFACE V002 DELTA: interface, shape and failure review of c2v001 → c2v002

- **Role:** same-lens distinct delta reviewer (interface, shape and failure). I did not write c2v001, c2v002, INTERFACE V001 or V002, FIX_DELTA_0427_V002, the V001 reviews or the author's fixtures.
- **Date:** 2026-10-16
- **Verdict: PASS_WITH_NOTES.**
  - B1 and B2 from `REVIEW_0427_INTERFACE_V001.md` are closed, and so are both Codex 0428 items.
  - No blocking issue remains.
  - Outside the declared delta, nothing changed in code behaviour, equations, call counts or rejection stages.
  - Five non-blocking notes are in §4.

## 1. Hashes recomputed from bytes (all match; no mismatch, so the review proceeded)

| file | sha256 |
|---|---|
| Task 0427 `FROM_CODEX/0427_2026-10-16_reviewed_noncircular_fluid_operator_implementation.md` (read fully) | `1e9e7cfb4be32cae313543374edb76c647a14530720cb276c83f6e464e95c164` |
| Spec `DDO_NONCIRCULAR_DISPLACEMENT_CORRECTION_PROPOSED_V001.txt` (read fully) | `d97ae766d98a03e14b5eaff39e1b9dcf0395167164eef0e135b5553709980cb4` |
| Equation review `NONCIRCULAR_DISPLACEMENT_EQUATIONS_REVIEW_V001.json` | `99fca0f60683d0b40e13be4fd9c4b78936d2cc8c07753bead84f8fed863fad4e` |
| Context `galaxy_coupled_fourier_hi_prediction_v006.py`, text only (L59-82, L171-190) | `e0d0888de2487c9de1346b4268c0ef9c12401965134333741b389bb3a5cdca79` |
| Context `owned_physical_fourier_metric_quadrature_v004.py`, text only (source convention) | `61dc1369726413cda55e87b6175adccce095c65495cb3d94afbff1b50a255582` |
| Codex 0428 `0428_2026-10-16_0427_finite_diagnostics_and_base_clarification.md` (read for the item list) | `e94cc68d2ebde91ae839f7a960e964ef909474358993028d860088164266da60` |
| `ddo_noncircular_displacement_action_c2v001.py` (preserved, unchanged) | `6b4f2cc6ee0e0c1a4408e555004b510d2d11058bc6f3e9cc82f6ce697ef9e482` |
| **Reviewed** `ddo_noncircular_displacement_action_c2v002.py` | `056db7b19443d4a88dcb6396531dfe1ff61acd8ba8387e6bfd0a8b64cf179925` |
| `INTERFACE_0427_V001.md` (preserved, unchanged) | `1c34edf3fce32f7705382d9f1b802ec2d53ad6b097c57b4fad4bff64af4b60eb` |
| **Reviewed** `INTERFACE_0427_V002.md` | `82d7c6cdf37eb40b03d429e77ae11e1a3c80cd80f630f67ea8dbba972d834a7c` |
| **Reviewed** `FIX_DELTA_0427_V002.md` | `06e1753aa50806c1179ccae40da092bc542c48acd697f06085381ba180a7d435` |
| `REVIEW_0427_INTERFACE_V001.md` (B1, B2 source) | `1df58f47d90c457f0ad952489aa3b6118e8c6588e9abf4e5f3358edfc6496f42` |
| `REVIEW_0427_EQUATIONS_V001.md` | `95eda7c805b6068d7dee442bddfe7586a4f8bcf625c40976d324617db832d21a` |

I did not open the DDO154 run result packet or any observation or calibration data, and I wrote nothing under `Universal Network Theory`.

## 2. The delta itself

- **My own diffs match.** I ran `diff -u` on the module and on the INTERFACE. Both outputs (314 and 346 lines) are byte-identical to the diffs embedded in FIX_DELTA §5.1 and §5.2:
  - `my_module.diff`: `738c64a30976d951571f468314c9bcd1b4f7bf7874e044d3202f3b7f17a8e7c7`
  - `my_interface.diff`: `d46cbc436598a08b9428bfbbae4c0a8881a9fc567b1dd373689a3134cf78fb24`

  I read every hunk.
- **AST scope.**
  - The changed top-level definitions are exactly: the docstring, `MODULE_TAG`, `NOT_DONE`, `_grid_array`, `_triple`, `_bulk`, `evaluate_bulk_action` and `evaluate_boundary_rows`.
  - Exactly two were added, `_MODULE_ERRSTATE` and `_require_finite_outputs`, and none were removed.
  - The public signatures are identical to c2v001.
- **`_bulk` statement by statement.** I removed the delta plumbing: `trace.append`, the `shapes` argument, the `input_shapes` key and the final sweep. After that, both versions have 86 statements, and they are identical except for two string literals. One is the axisymmetry rejection message (0428-B wording). The other is the identity-diagnostic `scope` text.
- **INTERFACE §4 line map.** I checked it against the c2v002 file and it is accurate (L87, L94-95, L137-143, L152, L222-236, L256, L273-276, L399-418, L426/L432, L463/L473/L475, L484-510, L515-517, L576-583, L596, L631-632).

## 3. Issue closure

| item | requirement | evidence (§5 test ids) | status |
|---|---|---|---|
| **B1** lower-rank arrays broadcast along the wrong axis | Only 0-d or full-rank arrays with explicit singletons are accepted. Any other rank is rejected with a reason, and shapes are recorded. | **T2:** <br>• All 72 cases are rejected at `input_validation` with "rank" in the reason and zero derivative or response calls. That is 24 array arguments (R, phi, z, rho0, K0, P0, Omega, angular forcing, 3 xi, 3 r0 and 10 supplied base derivatives), each at ranks 1, 2 and 4. A rank-1 Python list is rejected too. <br>• On the 8×8×8 square grid, c2v001 still accepts 1-D Omega(R) and differentiates it along z (Omega_z = 0.200; defect reproduced), while c2v002 rejects it. <br>• Explicit (N,1,1) input gives residuals bitwise equal to the full-array input, with Omega_R = −0.2 and Omega_z = 0. <br>• 0-d, (1,N,1), (1,1,N), (N,1,N) and nested-list rank-3 inputs are accepted. <br>• `input_shapes` is exact: 14 keys in callbacks mode and 24 in supplied mode, with () for 0-d. <br>• A full-rank non-broadcastable shape (N,2,1) is still rejected. <br>• Lapse arrays still require the exact shape. | **CLOSED** |
| **B2** missing Root fact: the free-surface position and the surface-mass source | Doc only: a §7 missing fact, plus fact 7 restricted to the actual surface | **T12:** <br>• INTERFACE V002 §7 fact 10 states where the rho0→0 surface lies and requires either (a) the adapter's surface-displacement source, consistent with v004's k=0/boundary-normal assignment, or (b) a retained-order assessment. <br>• Fact 7 says `lagrangian_dP = 0` is the spec s5 condition only at the actual rho0→0 surface. <br>• The identity was re-derived on my own 9×8×7 Chebyshev/FFT grid with Clenshaw–Curtis weights: ∫δρ dV = −1.2257447 and −∮ρ0 ξ·n dA = −1.2257447. <br>• The module needs no code change, correctly, because it has no quadrature. | **CLOSED** |
| **0428-F** final continuity/entropy diagnostics and all returned arrays finite-validated, or an explicit unavailable status that is never accepted | Non-finite values never returned with ok=True | **T9:** <br>• **Diagnostic overflow.** In my own construction, Ω·∂φδK and δv_z·K0_z overflow only after the last callback. c2v001 returns ok=True with a NaN `linearized_entropy`. c2v002 fails closed (`floating_point`, phase `identity_diagnostics`) with the response called once. The same happens under the caller errstate default, raise, ignore and warn, and the errstate is restored every time. <br>• **Base residual overflow.** This is a second, independent class: Ω·K0_φ in `base_entropy_residual`, with ξ = 0. c2v001 returns ok=True with inf. c2v002 fails closed at `base_checks`. So the fix covers returned arrays beyond the two diagnostics 0428 named. <br>• **Sweep alone.** I made a scratch copy in which only `_MODULE_ERRSTATE` is set to ignore. Its sweep fails closed (`output_validation`) on both cases. <br>• **Sweep completeness.** I made 242 injections into a real success result: NaN, inf and complex at every returned array leaf, and NaN and inf at every returned float, including `boundary_state` (a mappingproxy) and `lapse_used`. The sweep rejected all 242, and the result contains no container type the sweep does not traverse. <br>• **Fail-closed policy.** No "unavailable" status exists, so nothing non-finite can be mistaken for a valid residual. | **CLOSED** |
| 0428-F reading: `induced_response_full` is not traversed | The author asked a distinct reviewer to confirm this | <br>• The object is the caller's, retained by identity, and the spec requires it unmodified. <br>• Its validity, including complex fields, is the adapter's to define. <br>• The lapse arrays actually used are validated and returned in `lapse_used`. <br>• INTERFACE §6 states the exclusion. <br>• **T11:** NaN in a non-lapse native field still gives ok=True. See note R1. | **CONFIRMED** (note R1) |
| **0428-B** no new base gate | Only the polytrope and axisymmetry gates remain; wording only | <br>• In `_bulk` the only base-gate change is message text (§2). <br>• **T7:** 38 non-rank invalid inputs fail at the same stage in c2v001 and c2v002 (input_validation 20, forcing_partition 6, base_checks 2, derivative_callback 3, source_feedback 7), always as exactly 4-key dicts. <br>• No new rejection of a correctly computed finite output was found; the floating-point layer rejects only values c2v001 returned non-finite or overflowed. | **CLOSED** |
| 0428-B negative Ω² accepted as given; r0 may be nonzero | Omega used as given; r0 not tested; no clipping or dropping | **T10:** <br>• In the synthetic reference, the pressure gradient exceeds the inward force, so Ω² < 0 on 55.6% of nodes. <br>• Three caller real-Ω choices were each accepted: Ω ≡ 0 (0-d), signed √\|Ω²\|, and a sign-changing 0.3−0.5R. <br>• `boundary_state['Omega']` is bitwise equal to the input. <br>• Each `r0_*` term is bitwise equal to the supplied nonzero r0, and residual(r0) − residual(0) = r0 to ≤1e-14 relative. <br>• Residuals are bitwise equal to c2v001. <br>• `not_done` states that there is no force-balance gate. | **CLOSED** |
| Three Euler components; full native output; one feedback call | Unchanged | **T11 and T6:** <br>• `euler_residual` has exactly R/phi/z. <br>• The whole callback output is retained by identity, including extra keys. <br>• `response_call_count` is 1, and the response is called once on success and on the post-response failures tested (T9). | **UNCHANGED (holds)** |
| Nothing else changed | — | <br>• **T6:** across 8 valid fixtures (weak and exact lapse forms, callbacks and supplied modes, 2 seeds), c2v001 and c2v002 agree bitwise on every returned array (76-77 per fixture) and on every scalar and string, apart from the module tag, `input_shapes`, the scope text and the `not_done` line. <br>• Derivative call counts are 7/15/7 in callbacks mode and 4/11/4 in supplied mode, identical in both versions. <br>• **T8:** boundary rows are unchanged: they are separate from the bulk, the bulk residual is untouched, and the `boundary_state` key set is identical. | **CONFIRMED** |

## 4. Remaining issues

**Blocking: none.**

**Non-blocking notes:**

- **R1. ok=True does not certify the native object.**
  - `induced_response_full` is excluded from the sweep. A NaN in a non-lapse native field passes with ok=True (T11).
  - INTERFACE §6 says so, but the result dict carries no in-band marker.
  - Root's adapter should validate its own native output before using it in the final checks (spec s4/s6). A later version could state the exclusion in `not_done` or a scope string.
- **R2. Ignoring underflow lets subnormal results lose precision without warning.**
  - `under='ignore'` gives finite values, as INTERFACE §3 says, but they are not always accurate. In `probe_subnormal_underflow.py` the same configuration was run with ρ0 scaled by 1e-160, so that ρ0² ≈ 1e-320 is subnormal.
  - Result: the term −δρ P0_R/ρ0² is off by 1.8e-3 relative, and ok=True.
  - c2v001 behaves identically, so this is pre-existing and depends on the units.
  - **What Root must ensure:** in Root's units, ρ0², ρ0^γ and their products with perturbations must stay above about 2.2e-308. INTERFACE §3 could add one sentence saying so.
- **R3. A diagnostic-only overflow discards everything.**
  - Under the chosen fail-closed policy, a non-finite diagnostic also discards the finite three-component residual and the reference to the native output.
  - 0428 permits this, and it matches the no-partial-fields contract. If Root needs the native output in that case, its adapter must keep its own copy.
- **R4. The version bump changes which bulk results the boundary rows accept.** c2v002's `evaluate_boundary_rows` refuses a c2v001 bulk result because of the module tag (T8). This is expected, and Root must not mix versions.
- **R5. Notes carried over from V001, unchanged and outside the fix list.**
  - N1: in supplied mode, the axisymmetry gate sees only the caller's ∂φ arrays.
  - N2: masked arrays lose their mask.
  - N3: consistency between the lapse and the native output is the adapter's responsibility.
  - N4: wording. `evaluate_boundary_rows` also returns `module` and `stage`, and its failure stages are still not listed. The new `floating_point` reason in boundary rows names no phase, while INTERFACE §3's phase list describes the bulk only.
  - N5-N7: as before.

## 5. What was executed

**Setup.**
- **Runtime:** codex runtime Python 3.12.14, numpy 2.3.5, run as `python3 -I -B` under a perl `alarm` timeout.
- **Directory:** `/private/tmp/claude-501/-Users-bgm-MB-Work/573ea246-f21c-48d3-b8cc-d28a1f8b2c42/scratchpad/r0427-delta-interface-shape-failure`.
- **Fixtures:** NONPHYSICAL and algebraic only: synthetic polynomial and trig fields, my own Chebyshev/FFT spectral or second-order FD callbacks, and linear nonlocal stub responses.
- **Module loading:** each module was loaded by reading its published bytes, checking the sha256, and compiling in memory.
- **Excluded:** no project run, no DDO154 or NGC3198 data, no target velocities, no network, no installs. No `.pyc` was written next to the artifacts.

| file | sha256 | result |
|---|---|---|
| `review_0427_v002_delta_fixtures.py` | `8ef56b6381b9a2473e51276b6e7aec3a95d7170d62510d547bf2c9b1df01d53b` | — |
| `run1.txt` | `120385207231828408253e761369d0e0050653d076f1363b39481d977d9529e6` | **57/57 PASS** (T0-T12 above) |
| `probe_subnormal_underflow.py` | `6476c934193a2a796b2cdbd9838d32854e902edbe364c731b568e9ffda086ebe` | — |
| `probe_subnormal_run.txt` | `c939e9dfeb9059832311e5c21ba84476c4ba5468e6331cd5d35803264df93b45` | R2: 1.765e-03 relative, both versions |
| author suite `r0427-fix/test_0427_algebraic_fixtures_v002.py` (`3cec22e4ed834d2910b3067c36641d4a8aafcba287268ffbc2c2813887ec0ab1`), unmodified, rerun on c2v002 → `author_v002_suite_on_c2v002.txt` | `e57ad910882459c013085044c76e40ed0ef948003c676117cfe5ee2f9d9d2ef0` | 127/127 |
| same suite rerun on c2v001 → `author_v002_suite_on_c2v001.txt` | `005fdac4f6a0c31b347a7f9a6e092cd2b6312622fda9f06198700d29ab1caa44` | 107/127 (the 20 delta defects) |

Both reruns of the author's suite are identical to the author's recorded `run_v002_final.txt` and `contrast_c2v001_final.txt`, except for one line in each. In that line, a Python set prints in a different order, which comes from hash randomization.

## 6. Scope

This review covers only the c2v001 → c2v002 delta, read through the interface, shape and failure lens, together with INTERFACE V002 and the FIX_DELTA claims. Equations and units were checked only as unchanged, by bitwise equivalence with c2v001; c2v001 itself was reviewed for them in V001. The review does not cover:
- physical adequacy
- Root's base, grid, adapter or boundaries
- any solve, resonance or stationarity

The verdict applies to c2v002 `056db7b19443d4a88dcb6396531dfe1ff61acd8ba8387e6bfd0a8b64cf179925` and INTERFACE V002 `82d7c6cdf37eb40b03d429e77ae11e1a3c80cd80f630f67ea8dbba972d834a7c` exactly as hashed.
