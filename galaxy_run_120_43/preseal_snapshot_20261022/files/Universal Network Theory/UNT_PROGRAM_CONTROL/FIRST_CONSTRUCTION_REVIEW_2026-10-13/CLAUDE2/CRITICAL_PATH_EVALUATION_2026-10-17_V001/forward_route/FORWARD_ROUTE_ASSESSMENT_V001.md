# DDO154 forward route: where the m≥1 forcing comes from, and how ready the axisymmetric state is (V001)

This is a read-only analysis of saved outputs. I launched no program script and modified no program files. NGC3198 target velocities were not opened. The structured version, with every JSON path and hash, is `FORWARD_ROUTE_ASSESSMENT_V001.json` in the same folder. The supporting scripts and outputs are in `scripts/` and in the sibling `*.json` files.

Paths below are relative to `UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/` unless stated otherwise. CI = `UNT_PROGRAM_CONTROL/CURRENT_INSTRUCTIONS.md`, LIVE = `CODEX1/LIVE_MODEL_CONSTRUCTION_DIRECTION_2026-10-15.md`, ASM = `CODEX1/GALAXY_COLLECTIVE_MODEL_ASSEMBLY_2026-10-15.md`.

## 1. Where the m≥1 forcing comes from (TESTED-POSITIVE at the saved trial point)

**What the forcing is.** In the finite-material identity evaluation, every mode residual is gravitational. From `DDO154_FINITE_MATERIAL_FIRST_CALL_RUN_V002/diagnostic/finish.json` `identity.mode_residuals[*].gravity_l2_J`:

| Mode | m1 | m2 | m3 | m4 | m5 | m6 |
|---|---|---|---|---|---|---|
| Residual (J) | 6.09e44 | 9.75e44 | 3.33e42 | 1.12e45 | 3.96e42 | 6.74e42 |

The kinetic and pressure parts are at most 2.8e32 J. Relative to the radial m=0 gravity of 4.805e47 J, the modes are 1.27e-3, 2.03e-3, 6.9e-6, 2.34e-3, 8.2e-6 and 1.4e-5.

**The sources are axisymmetric by construction.**
- The HI+He source is built from annular Bernstein controls (LIVE:37).
- The initial and fixed sources use an analytic J0 azimuth (V002 `result.json` `/result/binding_custody/bessel_custody/source_scope`).
- Each gas column is solved in the 16-azimuth *mean* potential and then tiled identically over 16 azimuths (`helpers/coefficient_method/ddo_fixed_K_free_surface_root_v005.py:75,87,95-96`).

Measured, the azimuthal variation of rho0, P0, K0, enthalpy and the integrated source is ≤4.3e-16. The F3 gas Fourier source is exactly invariant under x/y mirrors, the xy swap and a 90° rotation; under the z-mirror it changes by 4.0e-10, which is roundoff.

**The "source offset" is not a displacement.** `DDO154_BODY_SOURCE_OFFSET_RUN_V001` is an additive Fourier correction: the new body source minus the exact G4 gas blob. It is itself symmetric to ≤2.9e-16.

**The kernel has a lattice frame, and the disk axis is not a symmetry axis of it.**
- The chart is x = ℓ_F C̄^{1/2} ξ with ξ = A m, where A is the diamond Bravais matrix (`helpers/recovered_packet_audit/owned_physical_fourier_metric_quadrature_v005.py:3-7,75-80,101-104`).
- The native symbol is a Fejér-weighted sum over the L=4 grid at k_prim mod 2π (`owned_positive_cardinal_source_hessian_v001.py:83-100`). It is therefore periodic on the reciprocal lattice.
- ℓ_F = 3.21 kpc. The physical k-cube spans 2.12 reciprocal-lattice periods per primitive axis.
- The eigenvalues of C̄ are 0.516, 0.727 and 1.462. Their principal axes sit at 47.4°, 42.6° and 89.8° from the disk axis.
- The galaxy plane is the chart xy plane. The 66° is only the observational inclination, used for source re-facing and for the sin66/sin64 observation map.
- The EH block works in physical k and is rotation-covariant (`owned_static_action_metric_binding_v002.py:168-206`). All rotational-symmetry breaking therefore comes from the native part.

**Measured kernel symmetry** (unit lapse response in `DDO154_BODY_SOURCE_OFFSET_RUN_V001/offset/unit_response.npz`):
- The kernel is real (imaginary part 2.7e-17) and even under k → −k (4.9e-14). The field is therefore point-symmetric about the galaxy centre, so odd m can only appear as z-odd structure.
- Partner differences under reflections and rotations about the disk axis are large:

| Range | z-mirror | x-mirror | y-mirror | xy swap | 90° rotation |
|---|---|---|---|---|---|
| All k | 0.256 | 0.273 | 0.178 | 0.757 | 0.768 |
| k = 0.2–0.5 /kpc | 0.026 | — | — | — | 0.054 |
| k = 1–2 /kpc | 0.0007 | — | — | — | 0.0015 |
| k < 0.2 /kpc | 0.14–1.58 (across shells) | | | | |

**Size of the m≥1 force at the 12 radii** (newest reference, `DDO154_LOWER_ENTROPY_REFRESHED_ROTATION_RUN_V002/rotation/rotation_base_arrays.npz`, mass-weighted |F_R,m|/|F_R,0|):
- m=2 is 2.6e-3 at 0.49 kpc and grows to 1.2e-2 at 5.92 kpc.
- m=1 is 3.7e-4 to 9.5e-4. It is purely z-odd and vanishes at the midplane.
- m=3 is 1e-6 to 1.3e-5.
- m=4 is 2.1e-3 to 1.6e-2.
- m=8 is at most 4.1e-3.
- The azimuthal force as a fraction of RΩ² is 0.006–0.027. Over all 72 columns it reaches at most 0.148, at 13.85 kpc.

**Which part is kernel and which is numerics** (`ring_attribution_F3.json`, `cutoff_test_F3.json`):
- Replacing the kernel with its D4×z-mirror-symmetrized or isotropic shell average removes m=1, 2 and 3 to ≤1e-14. It leaves m=4 and m=8 unchanged; for example at 2.96 kpc, m4 is 1.6e-2 with the actual kernel and 1.5e-2 with the isotropic one.
- With the isotropic kernel, the m=4 range across the 12 radii depends on the truncation shape:

| Truncation | m4 range |
|---|---|
| Full cube | 2.1e-3 to 1.6e-2 |
| Cylinder, k⊥ ≤ 2/kpc | 2.4e-4 to 3.0e-3 |
| Sphere, \|k\| ≤ 2/kpc | 3.4e-5 to 6.9e-4 |

So:
- m=2 and the z-odd m=1 and m=3 come only from the native lattice-frame anisotropy.
- m=4 and m=8 are mostly numerical, from the corners of the Cartesian 72³ k-cube. The largest finite-material residual (m4) therefore inherits a numerical artifact.

**The older V002 field.** Its ring forcing is larger:
- m4 reaches 0.18 and m8 reaches 0.20 of m0.
- A cylindrical cutoff reduces m4 to ≤1.6e-2, but m8 stays near 0.2. That component comes from the gas being solved in 8 azimuth columns.
- At 8 sample azimuths, the m=8 component aliases onto m=0. The circular speed at 4.44 kpc spans 33.67 to 43.48 km/s across azimuth.
- The non-monotonic V002 rows are therefore numerical, not physical (TESTED-POSITIVE).

**No other physical input produces m≥1.** The stars are analytic rings, the boundary is an isolated zero perturbation, and there is no tide or exterior source. mubar enters only through the kernel.

## 2. Is the m≥1 response orientation dependent?

- **Orientation dependence (TESTED-POSITIVE).** The kernel is not invariant under any rotation or reflection about the disk axis. Rotating the galaxy in its plane rotates the m=2 phase. Tilting the disk axis changes the magnitudes of m=1 and m=2.
- **m=0 is nearly insensitive (TESTED-POSITIVE).** Fully isotropizing the kernel changes the m=0 radial force by +5.4e-4 to +2.0e-3 at the 12 radii.
- **No orientation law exists in the program.** No adopted rule fixes the galaxy's orientation relative to the lattice. The code fixes it implicitly: disk axis = chart z, with the symmetric square root of C̄ (`owned_physical_fourier_metric_quadrature_v005.py:80`).
- **Rotated-axis family: UNTESTED.** Deciding test: keep the kernel, rotate the source positions so the disk axis lies along each C̄ principal axis and along a lattice [111] direction, then compare the 12 m0 rows and the m=2 amplitude.

## 3. The axisymmetric state

### `DDO154_STABLE_CACHED_COUPLED_RUN_V002`

**What it solved.** A finite fixed point between:
- the full 10-field native+EH metric response on the 72³ composite Gauss cube (k_max 2/kpc), and
- HI two-sided free-boundary columns (Γ 5/3, σ0 11 km/s: `ddo_actual_initial_source_preparation_v007.py:101`) on 72 radii × 8 azimuths, with stars fixed and analytic.

Its row speed is the cos²-weighted mean of v(φ) multiplied by sin66/sin64.

**Parameters:**
- Eref = 1.4642919592e58 J
- ℓ_F = 9.905025037e19 m
- γ = 2.941048894e41
- γ/Eref is 10× the V008 value
- Common scale seed = 0.158413, set from the DDO median of 43.3 km/s
- K from σ0 = 11 km/s

**Convergence.** The gas residual fell from 4.56e57 J to 2.45e56 J over 5 iterations, against a bound of 2.72e56 J. This is CONVERGED_FINITE_FIXED_POINT for the finite source closure only.

**Cost.** 1593.6 s and 1.142 GB.

**Speeds (km/s):** 12.763, 23.507, 26.487, 32.335, 37.506, 35.393, 41.251, 47.576, 38.995, 49.751, 33.336, 51.044. Four rows fall inside the frozen rectangles and 8 outside; the maximum |std| is 33.0.

**Hashes:** result `79855e78…`, receipt `8af39557…`, seed `694eaaaa…`.

### Newest axisymmetric reference: second refreshed lower-entropy m0 state

The chain is `DDO154_LOWER_ENTROPY_REFRESHED_COLUMNS_RUN_V002`, then `…_REFRESHED_ROTATION_RUN_V002`, then `…_REFRESHED_COLUMN_MEAN_RUN_V002` (ASM:1643).

**What it solved:**
- K = (64/121) × the original K, i.e. the 8 km/s label at the original density.
- Free-surface columns solved in the φ-mean of the lagged field.
- Pressure-balanced m0 rotation from φ-means (`ddo_free_surface_rotation_root_v005.py:109`), with the full m≥1 residual stored (`:114`).
- HI-weighted mean of RΩ per column.
- Same parameters as V002.

**Stability:**
- Maximum 12-speed change between iterations: 0.009515 km/s.
- Minimum Ω²: 1.905e-33 s⁻² (all positive).
- Latest-column source residual: 3.95e-4.
- The F3 feedback has not yet been fed back into new columns.

**Cost:**
- Columns: 627 s, 0.62 GB
- Feedback: 19 s
- Rotation: 165 s, 0.81 GB
- Observation: 0.1 s

**Speeds (km/s):** 11.582, 21.883, 29.132, 34.538, 38.187, 41.436, 44.627, 47.757, 49.193, 49.398, 50.910, 48.655. These are in `…COLUMN_MEAN_RUN_V002/observation/result.json` `prediction.rows`, hash `24400235…`.

**Rectangle membership (descriptive only).** 9 rows inside and 3 outside: rows 08 (+1.46 km/s), 09 (+1.79) and 11 (+3.51). The maximum |std| is 7.28.

## 4. Forward-call readiness for calibration

**Route A** is `helpers/recovered_packet_audit/ddo_composite_stable_cached_root_worker_v002.py` plus a seed JSON. It is fully parameterized by (Eref, ℓ_F, γ, numerics) and costs 1594 s and 1.14 GB per call. It carries the m=4 and m=8 numerical artifacts.

**Route B** is the clean m0 chain:
1. `ddo_body_source_offset_root_v003`
2. `ddo_fixed_K_free_surface_root_v005`
3. `ddo_free_surface_native_feedback_root_v004`
4. `ddo_free_surface_rotation_root_v005`
5. `ddo12_lower_entropy_column_mean_root_v004`

It is **not a forward function yet.** Every stage checks the pinned seed SHA `694eaaaa…` and the checkpoint identity `98816902…` (`ddo_homotopy_reference_root_worker_v001.py:22-25`). The body-offset stage also hard-codes DDO154 (`:53`). It needs a parameterized successor and a review.

**Parameters that can change without re-sampling the native response:**

| Parameter | What a change requires |
|---|---|
| Common scale s | Exact 1/s rescale of the unit response; no rebuild |
| γ/Eref | One kernel rebuild, about 124 s or less |
| ℓ_F | One kernel rebuild, about 124 s or less |
| Entropy K | A controls input |
| Distance | Source rescale |
| Inclination | Re-facing plus the observation map |
| M/L, He factor, Γ | No kernel rebuild |

The 11 native ratios and b do need native re-sampling (the coefficients are in `PROVISIONAL_L4_COEFFICIENT_FREEZE_V001/coefficients.npz`).

**Cost of one route-B call:** about 800 s per Picard pass, times 2–3 passes, plus ≤124 s for a kernel rebuild and about 140 s for the source transform. That is roughly 30–45 minutes single-threaded, at ≤1.13 GB. The 72 columns are independent and could run in parallel.

**Blocker: Fourier truncation convergence is UNTESTED.** Changing only the truncation shape (cube to sphere, |k| ≤ 2/kpc) changes the m0 radial force at the 12 radii by:

−18.8%, −15.0%, −9.2%, −2.6%, +2.4%, +3.6%, +1.4%, −1.3%, −2.4%, −1.6%, +0.1%, +1.4%

That is roughly −9.9% to +1.8% in speed. This effect is larger than the kernel-origin m≥1 effect. Deciding test: extend k_max to 3–4 /kpc with outer panels at a fixed source, compare the 12 rows, and adopt a spherical or cylindrical truncation.

## 5. NGC3198 readiness

**What exists:**
- `ngc43_composite_coupled_root_worker_v001.py` (`1b95a4ff…`), `ngc_composite_full_coupled_binding_v001.py` and `ngc_actual_initial_source_preparation_v001.py`. These passed static review (PASS_SCOPED_CONDITIONAL_SOLVER).
- The inputs cover 43 target-free query radii from 0.32 to 44.08 kpc, 51 HI bins, 10 H2 detections, and an H2 tail scale of 1.8064 kpc, with a 72°/73° projection (ASM:1629).
- An older tensor-grid driver, `ngc43_coupled_trial_root_driver_v001.py`.

**What is missing:**
- There is no NGC seed (Eref, ℓ_F, γ, numerics, h2_tail_mass_rtol) and no frozen calibrated region.
- It has never been launched.
- It follows the V002-type azimuth-resolved route, which carries the m=8 and m=4 artifacts. The clean m0 route has no NGC port.
- The k-domain is unverified for 44 kpc. Kernel anisotropy is 14–158% at k < 0.2 /kpc, and the DDO outer azimuthal force already reaches 0.148.
- The provisional settings (σ0 11 km/s, Γ 5/3, the H2 proxy and tail, a single-plane 72°/73° projection) remain counted assumptions.
- The source bundle is CANDIDATE_NOT_ADMITTED.

Execution is UNTESTED.

## 6. The counted approximation, and whether the instructions allow it

**What the approximation assumes:**
- **A1 – the state.** The galaxy state is the stationary axisymmetric m=0 member: circular streaming, polytropic free surfaces with the observed Σ, and fixed axisymmetric stars.
- **A2 – the response.** The kernel is left anisotropic and unmodified. Only the m=0 projection Φ0 = ⟨c² ln N⟩_φ drives the state. For an axisymmetric source this is exactly the response of the kernel's azimuthal average about the disk axis, which keeps the k⊥/k_z anisotropy. It is a symmetry projection, not an isotropy assumption, and the newest reference already does this.
- **A3 – the orientation.** Disk axis = chart z, a counted choice. No law fixes it. The m0 sensitivity to isotropization is ≤0.2%; the rotated-axis family is UNTESTED.
- **A4 – the neglected m≥1 response.** The kernel-origin m≥1 forcing is carried as an explicit sensitivity.
  - At the midplane, ε₂ runs from 2.6e-3 to 1.12e-2. The z-odd ε₁ at 0.2 kpc runs from 9.5e-4 down to 1.8e-4.
  - As an indicator (not a prediction), the pointwise speed spread 0.5ε₂v runs from 0.015 to 0.272 km/s across rows 01–12. That is comparable to σ = 0.2–0.3 km/s for rows 06–09.
  - Back-reaction on m0 is of order ε², at most about 1.3e-4.
  - The effect on the observable estimator is UNTESTED. Deciding test: compute the linear m=2 response of the m0 state to artifact-free forcing and push it through the HI estimator at sampled position angles.
- **A5 – numerical modes.** The m=4 and m=8 components are numerical and must not be carried as physical forcing.

**Instructions that support it:**
- CI:142: "authorizes standard boundary approximations where force balance or mass continuity encounters analytical friction. Record any approximation actually selected and its scientific scope."
- CI:75: "approximately axisymmetric average of observed ordinary matter … Compare response to averaged sources with averages of fuller responses where feasible".
- CI:133: theory choices may be made and counted.
- ASM:1377: "a computational branch under an explicitly assessed stationary, translation-invariant reference, rotationally symmetric about z; it does not presume full3D isotropy".

**Instructions that constrain it:**
- CI:75: "This does not supply a symmetric native response, thin disk, equilibrium, circular orbits or a classical gravitational law."
- LIVE:41: "Do not invent a correlation length, isotropy, continuum limit or finite physical wavelength coverage."
- ASM:17 and LIVE:17: "Full cosmic comparison remains later; anisotropic native output must not be silently forced into an isotropic-rate branch."
- CI:79: do not run a knowingly inadequate model.
- CI:114: evaluate sensitivity and numerical convergence.

**Verdict: consistent, under conditions.**
- The approximation restricts the *state* to m=0 and projects the *field* onto m=0. It does not substitute a symmetric or isotropic kernel, which is what CI:75 and LIVE:41 forbid.
- ASM:17 refers to the cosmic isotropic-rate branch and is not engaged here. The projection is explicit, not silent.

The conditions are:
1. Count A1–A4 together with their measured sensitivities.
2. Keep the kernel unmodified and keep the stored m≥1 residual.
3. Declare the orientation choice and run the orientation-family test. Otherwise an implicit frame choice becomes an undeclared input, which LIVE:41 forbids.
4. Exclude the m=4 and m=8 numerical artifacts.
5. Settle k_max convergence before calibration. At up to 18.8% in the inner-row m0 force, it is the dominant open numerical issue, larger than the m≥1 effect.

The verdict is a documentary assessment, not a numerical result.
