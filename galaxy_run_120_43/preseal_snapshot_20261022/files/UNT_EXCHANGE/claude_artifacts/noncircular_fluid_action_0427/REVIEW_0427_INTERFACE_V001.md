# REVIEW 0427 INTERFACE V001: interface, shape and failure review of c2v001

- **Role:** distinct reviewer, not the author. I did not write or edit the module, the INTERFACE note or the author's fixtures.
- **Date:** 2026-10-16
- **Verdict: FAIL.** There are two blocking issues, B1 (code) and B2 (INTERFACE). Both have small, contained fixes. The equations, inertness, failure handling, callback contracts and the separation of bulk from boundary all passed.

## 1. Hashes recomputed from bytes (all match)

| file | sha256 |
|---|---|
| Task 0427 `0427_2026-10-16_reviewed_noncircular_fluid_operator_implementation.md` | `1e9e7cfb4be32cae313543374edb76c647a14530720cb276c83f6e464e95c164` |
| Spec `DDO_NONCIRCULAR_DISPLACEMENT_CORRECTION_PROPOSED_V001.txt` | `d97ae766d98a03e14b5eaff39e1b9dcf0395167164eef0e135b5553709980cb4` |
| Equation review `NONCIRCULAR_DISPLACEMENT_EQUATIONS_REVIEW_V001.json` | `99fca0f60683d0b40e13be4fd9c4b78936d2cc8c07753bead84f8fed863fad4e` |
| Context `galaxy_coupled_fourier_hi_prediction_v006.py` (text only, lines 59-82 and 171-190) | `e0d0888de2487c9de1346b4268c0ef9c12401965134333741b389bb3a5cdca79` |
| Context `owned_physical_fourier_metric_quadrature_v004.py` (text only, docstring source convention) | `61dc1369726413cda55e87b6175adccce095c65495cb3d94afbff1b50a255582` |
| Reviewed `ddo_noncircular_displacement_action_c2v001.py` | `6b4f2cc6ee0e0c1a4408e555004b510d2d11058bc6f3e9cc82f6ce697ef9e482` |
| Reviewed `INTERFACE_0427_V001.md` | `1c34edf3fce32f7705382d9f1b802ec2d53ad6b097c57b4fad4bff64af4b60eb` |
| Author fixtures `r0427/test_0427_algebraic_fixtures.py` | `89e20cb76a529a920d69ea69b736f9b4fff72e12024dd32fb15eb01d8d67d8b6` |

## 2. What was executed

Everything ran in `/private/tmp/claude-501/-Users-bgm-MB-Work/573ea246-f21c-48d3-b8cc-d28a1f8b2c42/scratchpad/r0427-if`. The interpreter was the codex runtime Python 3.12.14 with numpy 2.3.5, run as `python3 -I -B`, which only reads the runtime. The fixtures are nonphysical and algebraic only. I used no project run, no DDO154 or NGC3198 data, no run packet, no target velocities, and no network or installs. Nothing was written under `/Users/bgm/Research/Universal Network Theory`.

1. **Author fixtures rerun against the published bytes:** 93/93 pass. Output is `author_rerun.txt` (`9d725b8a8ecb31a40079345ebf0e1c4355f7d4062e620b72f024bedec38409ef`).
2. **My fixtures,** `review_0427_interface_fixtures.py` (`144b3638a53e9f659436f1ee855dadef85fd828af762fac1f83c6c5adba00279`), with output `review_run2.txt` (`37c9e4e81286a900744e8bc1be71162e8b1bb1924a0be8996ae33463e9a2e4a5`). 136 of 138 checks pass. The 2 that fail are PROBE checks written to fail when the hazard exists; they record B1 and N2.
3. **Broadcast consequence probe,** `probe_broadcast_square_grid.py` (`336a8c77e8b844b2aa342650bb33b72096137c9712aef1575521783e79606a6c`), with output `probe_broadcast_run.txt` (`8d118be5cead02037d5069f3f9cb41797330a2dbe7dea4d83245f9fb845a47d2`).

My fixtures cover the following:
- **AST inertness:**
  - Imports are only `math`, `types`, `collections.abc` and `numpy`.
  - The top level holds only a docstring, imports, literal constants and defs.
  - There are no I/O or dynamic-exec names, and no `linalg`, `pinv`, `lstsq`, `clip`, `nan_to_num`, `maximum`, `minimum`, `where`, `fft`, `mean` or `gradient` attributes.
  - There are exactly two public functions. Both are keyword-only, with no defaults and no `*args` or `**kw`.
- **Import audit:** executing the compiled module body raises no `open`, `os`, `socket` or `subprocess` audit events.
- **Independent Cartesian reference:** coordinate-free, using nested 4th-order central differences of analytic fields. It covers (v0·∇)dv + (dv·∇)v0 + ∇dΦ + ∇dP/ρ0 − δρ∇P0/ρ0² + r0, the Lie-bracket dv and −div(ρ0ξ). The fixture is new and differs from the author's:
  - gamma = 3
  - vertical shear Ω_z = −0.3 + 0.2R
  - forcing with m = 1 and m = 2
  - a nonlocal stub response
  - 6 nodes
  
  Fields agree within 2.1e-11 and the three residuals within 6.3e-9, relative to the largest term. A Coriolis sign flip would be detected.
- **Rejection paths:** 89 bulk cases (50 input_validation, 12 forcing_partition, 2 base_checks, 9 derivative_callback, 16 source_feedback) and 11 boundary-row cases. Every failure dict has exactly the keys {ok, module, stage, reason}, and the callback and response call counts were asserted for every case.
- **Call counts and order:** the response was called exactly once on every successful path and on every path that failed after it. It was never called before the static, polytrope and axisymmetry gates.
- **Retention, aliasing and modes:** the full response output was retained by identity and left unmodified. Neither inputs nor outputs were aliased or mutated. Supplied and callback modes agree, and the exact-lnN form was checked. The caller's errstate was preserved under `seterr(all='raise')`.
- **Boundary rows:** they are separate from the bulk residual, each callback was called once, and the fields mapping is read-only with exactly the documented keys.

## 3. Blocking issues

### B1. Lower-rank arrays are silently broadcast along the wrong axis (code: `_grid_array`, lines 114-124)

`_grid_array` accepts any array that numpy can broadcast to `grid_shape`. numpy aligns shapes from the right, so a lower-rank array is applied along the trailing axes. On a grid with equal axis lengths, a 1-D radial profile is therefore applied as a function of the last axis (z). It is not rejected and nothing is recorded.

The probe ran on an 8×8×8 (R, phi, z) grid with exact callbacks and passed `Omega=Omega(R)` as a 1-D array. The result was `ok=True` with Omega_R = 0 and Omega_z = 0.5, which should have been the reverse. Compared with the explicit `(N,1,1)` input, the residuals were wrong by 0.067 against a scale of 0.16 (R), 0.105 against 0.22 (phi) and 0.0088 against 0.02 (z). The axisymmetry and polytrope gates cannot catch this, because Omega(z) is axisymmetric.

The same path serves R, phi, z, rho0, K0, P0, Omega, xi, r0, the angular forcing and the supplied base derivatives. The task asks for broadcast compatibility to be "explicit", and this review was asked to check for silent broadcasting surprises.

**Required fix:**
- Accept only `arr.ndim == 0` or `arr.ndim == len(grid_shape)`, so singleton axes must be explicit (for example `Omega[:, None, None]`). Reject any other rank with a recorded reason.
- Optionally, record each input's original shape in the success result.
- Update INTERFACE §2 to match.
- Add fixtures: a 1-D profile on a square grid is rejected, and `(N,1,1)` is accepted.
- Issue the fix as a new file, c2v002, with INTERFACE V002, and have a distinct reviewer check the delta.

### B2. The INTERFACE omits a fact Root must supply: the free-surface position and its effect on mass in the source feedback (doc fix; §7)

The module requires rho0 > 0 and P0 > 0 at every node, as the task demands. A grid can therefore never contain the zero-density polytropic surface that spec §5 relies on ("no spurious surface-mass delta"). Two consequences follow.

- **The source passed to the response does not conserve mass.** At any grid face where rho0 > 0 and ξ·n ≠ 0, typically the top and bottom faces, the bulk `drho = −div(rho0 ξ)` omits the mass that crosses the face. Its volume integral is −∮ rho0 ξ·n dA, not zero, so `delta_f_n` carries a spurious net mass, which is k→0 content that v004 refuses.
- **The boundary row is not the spec condition there.** `lagrangian_dP = 0` imposed at such an interior face is not the spec §5 free-surface condition.

Facts 1 and 7 of the INTERFACE mention the surface-location representation and k=0 handling, but neither states this consequence.

**Required fix:** add a missing-fact item to INTERFACE §7. Root must state where the physical rho0→0 surface lies relative to the grid faces. Root must then do one of the following:
- supply the boundary-layer, surface-displacement source contribution inside the response adapter, consistent with v004's k=0/boundary-normal assignment
- give the retained-order assessment that shows it is negligible

The INTERFACE should also say that the free-surface row is the spec condition only at the actual surface. No module code change is needed, because the module has no quadrature and must not choose one.

## 4. Checks that passed

- **Inertness:** confirmed by AST and the audit hook. The module uses only numpy and the stdlib, does nothing at import, performs no I/O, and its public callables are keyword-only with no defaults.
- **Validation (outside B1):**
  - Exact shape is enforced for every callback output and for the lapse arrays; broadcastable-but-not-exact shapes are rejected.
  - Real dtypes only: complex, bool, object, string and datetime are all rejected.
  - Values must be finite.
  - R, rho0, P0, K0, gamma and c must be strictly positive. A single zero node and a −1e-300 value were both rejected, not clamped. gamma is rejected when bool, a 0-d array or a string.
  - Tolerances must be ≥ 0.
- **Callbacks:**
  - The signatures match the INTERFACE: `partial_X(f)` positional, `induced_response(*, delta_f_n)` and `cb(*, fields)`.
  - Outputs are validated.
  - Exceptions return fail-closed dicts that carry the stage.
  - A failure after the response, in the Euler terms or the diagnostics, returns a fail-closed dict with no partial fields.
- **Response:**
  - It is called exactly once and receives a read-only `delta_f_n = −c² drho`.
  - A mutation made by flipping the writeable flag is detected.
  - The full output is retained by identity, unmodified, extra keys included.
  - The lapse form must match the declaration, and mixed or extra keys and N0 ≤ 0 are rejected.
  - dPhi_induced is c²δn (weak field) or c²δN/N0 (exact), with no silent choice. This matches the review JSON qualifications.
- **Forcing partition:** the fixed convention is enforced. The full-saved-field r0, the alternative convention, induced feedback in r0 or in the forcing, forcing that includes m=0, int or np.bool_ flags, missing or extra keys and empty provenance are all rejected. dPhi_total = forcing + induced, each exactly once.
- **Equations (spec §3, read line by line, plus the independent Cartesian reference):** I checked the conservative cylindrical divergence with 1/R, dK, dP with cs² = γP0/ρ0, the three dv components including −R(Ω_R ξ_R + Ω_z ξ_z), and all three residual signs (LHS − RHS). With that residual sign, r0 = (v0·∇)v0 + ∇Φ0 + ∇P0/ρ0. The INTERFACE line references (L342-L455) are accurate.
- **Bulk and boundary separation:** boundary rows are evaluated only by `evaluate_boundary_rows`, the bulk residual was bitwise unchanged after them, and an attempt to write to a bulk field from a row callback was refused.
- **Nothing invented:** the module supplies no base, derivatives, circulation, boundary values, grid library, Fourier convention, fit, closure, ridge, pseudoinverse, isotropization or angular mean, and no density clamp. It never drops feedback.
- **Result keys:** failures always carry exactly 4 keys. On success the top-level key set is the same in weak and exact form and matches INTERFACE §6.
- **Units and limitations:** both are stated in the module docstring, in `not_done` and in the INTERFACE.

## 5. Notes (not blocking)

- **N1. In supplied mode the axisymmetry gate sees only the caller's d_phi arrays.** A non-axisymmetric rho0 passed with `rho0_phi = 0` is accepted (probe). By design, supplied derivatives are never checked against the callbacks. This should be stated in the INTERFACE, or the gate alone could use the callbacks for d_phi of the base fields.
- **N2. Masked arrays lose their mask.** `np.asarray` drops the mask, so a masked rho0 is accepted and the masked nodes are used (probe). Reject `np.ma.MaskedArray` and other ndarray subclasses, or document this.
- **N3. The lapse component comes from the adapter, not the module.** The module cannot check that it is the n-component of the same `native_response`. INTERFACE fact 1 covers the extraction; it should say plainly that this consistency is the adapter's responsibility.
- **N4. Small INTERFACE wording points:**
  - §6: `evaluate_boundary_rows` also returns `module` and `stage`, and its failure stages (`input_validation`, `boundary_callback`, `internal`) are not listed.
  - §3: it says `native_response` is retained "as induced_response_full". In fact the whole callback output mapping is retained; §6 states this correctly.
- **N5. Measured callback counts (not a contract).**
  - Callbacks mode uses partial_R/phi/z = 7/15/7 per action, of which 4/8/4 come before the response.
  - Supplied mode uses 4/11/4.
  - Diagnostics use 1/2/1 after the residual. A failure there closes the whole action, which is acceptable.
- **N6. Terms dropped by the axisymmetric base, as in the spec.** The φ equation omits −δρ P0_φ/(ρ0² R), and dv omits the Ω_φ terms. Both follow spec §3's axisymmetric base, so the residual is spec-exact only to within the caller's `base_axisymmetry_rtol`, which is gated.
- **N7. Integer arrays are upcast to float64.** A uint64 value above 2^53 would lose precision. This is negligible.

## 6. Scope of this review

This review did not check:
- the physical adequacy of the leading-order approximation, which is covered by the equation review JSON and spec §6
- Root's adapter, base, grid, boundaries or launch
- any solve, resonance or stationarity

The verdict applies to c2v001 and INTERFACE V001 exactly as hashed above.
