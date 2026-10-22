# REVIEW 0427 EQUATIONS V002 DELTA: equations, units and signs (c2v001 → c2v002)

- **Role:** same-lens, distinct delta reviewer (equations, units, signs). I wrote none of the reviewed files: the c2v001 or c2v002 module, INTERFACE V001 or V002, FIX_DELTA, or any author or prior-reviewer fixture. I did not run any prior fixture script. Every check below comes from my own fixtures.
- **Date:** 2026-10-16
- **Verdict: PASS_WITH_NOTES.** There are no blocking issues.
  - B1, B2 and the 0428 items are resolved.
  - Spec §3-4 equations, signs and units are bitwise unchanged on every success path I ran.
  - The only behaviour changes are the documented ones.
  - Six notes follow in §4. None is required for 0427/0428.

## 1. Bytes (sha256 recomputed from bytes; all match the pins given to me or in FIX_DELTA)

| item | sha256 |
|---|---|
| Task 0427 | `1e9e7cfb4be32cae313543374edb76c647a14530720cb276c83f6e464e95c164` |
| Codex 0428 `0428_2026-10-16_0427_finite_diagnostics_and_base_clarification.md` | `e94cc68d2ebde91ae839f7a960e964ef909474358993028d860088164266da60` |
| Spec `DDO_NONCIRCULAR_DISPLACEMENT_CORRECTION_PROPOSED_V001.txt` (read fully, §2-7) | `d97ae766d98a03e14b5eaff39e1b9dcf0395167164eef0e135b5553709980cb4` |
| Equation review JSON | `99fca0f60683d0b40e13be4fd9c4b78936d2cc8c07753bead84f8fed863fad4e` |
| Context v006, read as text only (lines 59-82, 171-190) | `e0d0888de2487c9de1346b4268c0ef9c12401965134333741b389bb3a5cdca79` |
| Context v004, text only, hash checked | `61dc1369726413cda55e87b6175adccce095c65495cb3d94afbff1b50a255582` |
| c2v001 module (preserved) | `6b4f2cc6ee0e0c1a4408e555004b510d2d11058bc6f3e9cc82f6ce697ef9e482` |
| **c2v002 module (reviewed)** | `056db7b19443d4a88dcb6396531dfe1ff61acd8ba8387e6bfd0a8b64cf179925` |
| INTERFACE V001 (preserved) | `1c34edf3fce32f7705382d9f1b802ec2d53ad6b097c57b4fad4bff64af4b60eb` |
| **INTERFACE V002 (reviewed)** | `82d7c6cdf37eb40b03d429e77ae11e1a3c80cd80f630f67ea8dbba972d834a7c` |
| **FIX_DELTA_0427_V002.md (reviewed, read fully)** | `06e1753aa50806c1179ccae40da092bc542c48acd697f06085381ba180a7d435` |
| REVIEW_0427_INTERFACE_V001.md / REVIEW_0427_EQUATIONS_V001.md | `1df58f47d90c457f0ad952489aa3b6118e8c6588e9abf4e5f3358edfc6496f42` / `95eda7c805b6068d7dee442bddfe7586a4f8bcf625c40976d324617db832d21a` |

I did not open the DDO154 run packet or any observation or calibration data. I wrote nothing under `Universal Network Theory`.

## 2. Own diff and "nothing else changed"

I ran `diff -u` myself on both pairs:
- module diff: `mydiff_module.txt`, 314 lines, `738c64a30976d951571f468314c9bcd1b4f7bf7874e044d3202f3b7f17a8e7c7`
- INTERFACE diff: `mydiff_iface.txt`, 346 lines, `d46cbc436598a08b9428bfbbae4c0a8881a9fc567b1dd373689a3134cf78fb24`

Both match the FIX_DELTA §5 diffs byte for byte, apart from the `---`/`+++` header lines. Every module hunk is one of these:
- the docstring and `MODULE_TAG`
- the `_MODULE_ERRSTATE` constant
- one new `NOT_DONE` line
- the rank rule and shape recording in `_grid_array`/`_triple`
- `_require_finite_outputs`
- `errstate` set to raise, plus the `FloatingPointError` handlers (bulk and boundary)
- `trace` markers
- comment and rejection-message wording
- the `input_shapes` key
- the diagnostic `scope` string
- the output sweep

No arithmetic line of spec §3-4 is touched.

Checks run on the published bytes:
- **Equation block.** From displacement→perturbation through `lin_ent`, 102 code lines with trace and comment lines removed, the block is textually identical across the two versions (T7).
- **Line map.** Every line number in the INTERFACE V002 §4 table and the "new in V002" table points to the stated code, for example L404 cs2, L405-409 div, L410 dK, L411 dP, L415-417 dv, L426/L432 source and call, L463/L473 lapse, L475, L484-495, L515-517 and L576-583.
- **Signatures and imports.** Public signatures are identical (keyword-only, no defaults). Imports are only `math`, `types`, `collections.abc` and `numpy`. The top level holds only docstring, imports, assignments, defs and a class.

## 3. Issue closure

| item | status | evidence (my fixtures, §5) |
|---|---|---|
| **B1**: lower-rank arrays right-aligned | **Resolved** | Rank rule at L137-143. A 1-D Omega(R) is rejected at `input_validation` with zero callback and zero response calls. An explicit (N_R,1,N_z) base is accepted with `input_shapes['Omega']==(25,1,21)`, and its base values are bitwise equal to the full arrays (T5). The shape-failure lens owns the full rank sweep. |
| **B2**: free-surface position and surface-mass source (doc) | **Resolved** | The facts are in INTERFACE §7 fact 10 and fact 7, and §1/§2/§3 cross-reference them. The module is correctly unchanged. I checked the stated identity's sign and units with the module's own `drho` (including the 1/R factor), using Clenshaw-Curtis in R and z and trapezoid in phi with the measure R dR dphi dz. The result is ∫drho dV = −0.14088455497704 and −∮rho0 ξ·n dA = −0.14088455497704, with relative difference 3e-15. The value is nonzero, so `delta_f_n` carries net source c²∮rho0 ξ·n dA (T6). |
| **0428-F**: final continuity/entropy diagnostics and returned arrays | **Resolved (fail-closed variant)** | There are two layers: module arithmetic raises on divide, overflow and invalid, and a finite sweep runs before `ok=True`. **No "unavailable" status exists, so a non-finite diagnostic is never returned as valid.** (a) On a real success result, I replaced each of the 77 module-owned array leaves and 7 float leaves with NaN or inf in turn, covering both diagnostics, the base residuals, every Euler term, `lapse_used` and all of `boundary_state`. The sweep caught 84 of 84 (T4a). (b) I built a natural overflow confined to `lin_ent` with consistent callbacks. c2v001 returns `ok=True` with a non-finite `linearized_entropy` and finite Euler residuals, which reproduces the defect. c2v002 returns `{ok:False, stage:'floating_point'}` naming `identity_diagnostics`, with 4 keys, one response call and the caller errstate restored (T4b). (c) Success outputs are bitwise identical under the caller's errstate set to ignore or to raise (T4c). |
| 0428: no new base gate | **Resolved** | The base-check code is unchanged; only a message and comments differ. The AST shows only `rho ** 2` and `rho ** gam` as powers, so Omega is never squared, and no comparison involves r0 or Omega (T2f). |
| 0428: negative Omega² accepted as given | **Resolved** | In the fixture, 3312 of 6300 nodes have P0_R/rho0 + Phi0_R < 0, so no real circular Omega exists there, and the caller's Omega changes sign (−0.64…0.55). These cases are accepted: Omega ≡ 0, Omega with exact zeros on a radial row, and Omega = −50·Omega−3 with r0×10⁶ (T2d, T2e). Omega and its callback derivative are used bitwise as given (T2c). |
| 0428: r0 may be nonzero | **Resolved** | With xi = 0 and F = 0, each residual equals r0 bitwise in all three components (T2a). res(xi,r0) − res(xi,0) − r0 is at most 0.5 ulp, and a 0-d r0 is accepted (T2b). The sign is consistent with spec §2/§3: r0_R = P0_R/rho0 + Phi0_R − R Omega², checked with an analytic r0. |
| Three Euler components | **Preserved** | All three match the exact jet reference (T1). |
| Full native output | **Preserved** | `induced_response_full` is the same object, extra keys included (T1). |
| One feedback call | **Preserved** | `response_call_count` = 1 with one actual call in every run. Derivative-callback counts are identical across versions (7/15/7 callbacks, 4/11/4 supplied) (T1). |
| Nothing else changed | **Verified** | In 6 success configurations, every returned array of c2v001 and c2v002 is bitwise identical, including signed zeros: weak and exact lapse, each in callback and supplied mode, plus Omega ≡ 0 and the exact-zero-row case (76 or 77 arrays each). The only differing leaves are `module`, `identity_diagnostics.scope`, the added `not_done` line and the added `input_shapes` key (T1, T2d). |

## 4. Remaining issues

**Blocking: none.**

Notes (non-blocking):
1. **Ignoring underflow can still give finite but inaccurate values.**
   - INTERFACE §3 says underflow "can only give finite values". That is true, but the fix's "finite but wrong" protection covers overflow only.
   - I rescaled only the mass unit by 10^k; all accelerations should be invariant (T4d).
     - At k = −158 the drho·P0_R/rho0² term is off by 9e-6.
     - At k = −160 it is off by 8.7% and res_R by 0.22%, still with `ok=True`.
     - At k = −163 the call fails closed (`floating_point`).
   - The threshold is set by rho0² and products such as drho·P0_R reaching about 1e-308. SI and cgs galactic magnitudes (about 1e-42 and 1e-60) are more than 200 orders of magnitude away, so 0427 and 0428 are unaffected.
   - Suggested for a future INTERFACE: state that these products must stay in the normal float range in the caller's units.
2. **Memory layout.** The module's read-only copy of a singleton-axis input is not C-contiguous: its strides are (2016, 8, 96), against (2016, 168, 8) for a full array, although the values are identical. Callbacks that depend on layout, such as BLAS `tensordot`, therefore give (N_R,1,N_z) and full-array residuals that differ by at most 1.2e-14 relative, not bitwise (T5). FIX_DELTA's "bitwise equal to the full-array input" holds only for layout-insensitive callbacks. There is no effect on the equations. Optionally, use `np.ascontiguousarray` in `_readonly` in a later version, or have INTERFACE §3 state that callback arguments may arrive in any layout.
3. **INTERFACE V002 §4** says the equations "are shifted by +58 lines". The actual shifts run from +57 (base residuals) to +62 (diagnostics). The table's line numbers are all correct.
4. **`induced_response_full` is not traversed** (the author asked for confirmation). I confirm this reading is acceptable:
   - It is the caller's opaque object, retained unmodified by identity as 0427 requires.
   - The lapse arrays the module actually uses are validated and returned under `lapse_used`.
   - A NaN inside the native object passes the sweep (T4a), and INTERFACE §6 says so.
   - Root must not read `ok=True` as certifying the native output. The adapter owns that, consistent with the v006 evaluator's own non-real/non-finite raise.
5. **Failure stage labels.** Some inputs that c2v001 rejected as "nonfinite" at `base_checks` or `euler_residual` now report `floating_point`. Both fail closed with 4 keys. This is informational only.
6. **Prior notes carried forward unchanged.** These are equation-review notes 1-8 and the interface review's N1-N7, for example the spec-dropped terms that vanish for an axisymmetric base, now within `base_axisymmetry_rtol`. The interface reviewer's N2 (masked arrays) is outside this lens.

## 5. What was executed (NONPHYSICAL algebraic fixtures only)

**Setup:**
- Runtime: codex runtime `python3 -I -B`, Python 3.12.14 and numpy 2.3.5. The run took under a second.
- Location: scratchpad `r0427-delta-equations-units-signs/`.
- Data: synthetic analytic fields only. No project run, no DDO154/NGC3198 data, no target velocities, no network and no installs.
- Module loading: both modules ran from their sha256-verified bytes via `compile(bytes)`. Nothing was imported from the artifact folder and no `.pyc` was written.
- Callbacks: Chebyshev in R ∈ [1, 2.5] and z ∈ [−0.6, 0.6], Fourier in phi, on a 25×12×21 grid.

**Base and inputs:**
- Base: gamma = 1.4. rho0 is exp-modulated, K0 is nonbarotropic, and P0 = K0 rho0^γ.
- Omega has vertical shear and changes sign.
- xi has m = 1 and m = 2 content, with phi-dependent xi_z so that the R Omega_z terms are active.
- Forcing F has m = 1 and m = 2, and r0 is analytic and nonzero.
- Stub response: nonlocal (a two-node phi rotation plus a local term). It was run in both the weak δn and the exact δN/N0 forms.

**Independent reference:**
- Vectorized order-2 truncated Taylor jets in (R, phi, z) give exact forward-mode derivatives, with no finite differences and no spectral rule.
- The reference is evaluated from the spec §3-4 text over the whole grid.

| file | sha256 |
|---|---|
| `delta_eq_fixtures.py` | `1027f5a0e283eb0d0040e05f99088fee552aa29b8283bf0a35d260f434a7c0d4` |
| `run_delta_eq.txt` (**55/55 PASS**) | `efa22e4e698a852aa61036e1abe76031e5c61562e54d0f022b02fae9e0d39ec9` |
| `run_delta_eq.stderr.txt` (empty) | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

- **T1, jet reference and version equivalence** (weak/exact × callbacks/supplied):
  - c2v002 matches the exact reference for every quantity: drho, dK, dP, cs2, the three dv, lagrangian_dP, delta_f_n, dPhi_induced, dPhi_total and the three residuals. The worst field error is 4.7e-13, the worst full residual 4.1e-12, and the operator part without r0 at most 1.7e-11, all relative.
  - The continuity and entropy identities are at most 1.1e-13 and 1.9e-14.
  - All arrays are bitwise identical to c2v001.
- **T2:** the 0428-B cases, covering Omega given, negative circular Omega², Omega ≡ 0, zero rows, r0 entering exactly once, and the AST checks.
- **T3, units:** under L = 3.7, T = 0.45 and M = 2.2, every output and every individual Euler term scales by its own dimension to at most 5.8e-11, in both lapse forms. There are no hidden constants. The dimensions are:
  - c² drho: M L⁻¹ T⁻²
  - dPhi: L² T⁻²
  - residuals: L T⁻²
- **T4:** 0428-F, covering sweep coverage, the natural overflow, errstate invariance and the underflow scan.
- **T5:** B1 spot check and layout.
- **T6:** B2 identity.
- **T7:** text, AST and signature identity.

**Scope.** This review covers equations, units, signs and the delta only. It is not a solve, a base construction, a boundary realization, a resonance analysis or a physical adoption, and it does not establish a stationary state.
