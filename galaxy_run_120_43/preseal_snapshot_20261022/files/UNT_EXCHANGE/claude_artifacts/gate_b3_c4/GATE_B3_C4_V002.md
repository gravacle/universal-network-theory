# GATE_B3_C4_V002 — gate B3 final verdict: **PASS**. Every B3 item now evaluated for outer cube8 and cyl8 (single reviewer)

Claude4 main session, inline, single reviewer. Helpers are unavailable until 2026-10-23T19:00Z (weekly limit). UTC 2026-10-18T12:48:29Z (`date -u`).

**Dispatches** (sha256 from bytes):
- 0507 `3845e2864f0f4a7f660450289b101d1f3d1c072e9d34cbe37b141294dbe411ca`
- 0509 `d4d1686c10f1f82115a2f015f3f1471f554380a5d27ac7b4cb061cf192c52ea5`
- 0527 `e662fd4d176f71b0d422f24a640f88b6dcccbeca5e4148a9fe3fc7062710a2e4`

**Extends** `GATE_B3_C4_V001.md` (`a336838aa2d533c5e417f584836dd3fa1dc51fe29ffb61c932f5f55d34f81ed1`). Its 32/32 numeric results stand unchanged.

**Status of the two items V001 left NOT RUN:**
- the reference/body angular reads (TailBoundary tap): RUN, PASS;
- the fs-column potential(z): RUN, PASS.

No launches beyond the 0509 stage replays. C5H, `UVT_*` and NGC3198 targets were not read. Nothing was deleted.

## Verdict against the registered B3 text

The gate text is R1 `gates_before_any_T_result.B3`, quoted verbatim:

> independent-lane Cartesian implementation (no import of the tail library; box(8)\cube(4), doubling-converged 1e-10) on saved C4R3: value/gradient/Hessian <= 1e-8/1e-7/1e-6 of max; lapse pair <= 1e-8 max|t|; bd(z=0) == 0.0 exactly; facade midplane ratio == 0.0 and HI v003 L67 passes; reference/body angular reads (TailBoundary tap) <= 1e-7 max|grad t|; column potential(z) <= 1e-7 of max tail potential difference; imaginary part == 0.0; PLUS a cylinder-O case: O = cylinder K_big = 8 over cube 4, same points and tolerances, the independent lane integrating in (k_perp, psi, k_z) with the cube corner zone K < k_perp <= sqrt2 K handled by its psi limits

| B3 item | tolerance | cube8 | cyl8 | where |
|---|---|---|---|---|
| value | ≤ 1e-8 of max | 4.7e-15 | 4.9e-15 | V001 E1 |
| gradient | ≤ 1e-7 of max | 4.7e-15 | 3.1e-15 | V001 E1 |
| Hessian | ≤ 1e-6 of max | 4.3e-15 | 2.3e-15 | V001 E1 |
| lapse pair b0 | ≤ 1e-8 max\|t\| | 6.5e-15 | 3.6e-15 | V001 E2 |
| lapse pair bd | ≤ 1e-8 max\|t\| | 7.7e-15 | 5.1e-15 | V001 E2 |
| bd(z = 0) == 0.0 exactly | 0 nonzero | 0.0e+00 | 0.0e+00 | V001 E3 |
| facade midplane ratio == 0.0 | exact | 0.0e+00 | 0.0e+00 | V001 E5 |
| HI v003 L67 passes | passes | PASS | (same check) | V001 |
| **reference angular reads (tap), grad t** | ≤ 1e-7 max\|grad t\| | **4.0e-15** | **2.8e-15** | this report |
| reference angular reads (tap), t | (reported) ≤ 1e-7 max\|t\| | 5.6e-15 | 4.0e-15 | this report |
| **body angular reads (tap), grad t** | ≤ 1e-7 max\|grad t\| | **3.8e-15** | **2.8e-15** | this report |
| body angular reads (tap), t | (reported) ≤ 1e-7 max\|t\| | 4.4e-15 | 3.8e-15 | this report |
| **fs-column potential(z), column 00** | ≤ 1e-7 of max tail potential difference | **9.8e-16** | **1.4e-15** | this report |
| **fs-column potential(z), column 30** | ≤ 1e-7 of max tail potential difference | **1.2e-13** | **1.2e-13** | this report |
| imaginary part == 0.0 | exact | 0.0e+00 | 0.0e+00 | V001 E6 |
| independent lane doubling-converged | ≤ 1e-10 | 3.0e-15 / 2.0e-15 / 2.2e-15 | 5.6e-16 / 9.9e-16 / 1.2e-15 | V001 (value / gradient / Hessian) |
| no import of the tail library | none | PASS | | V001; this report re-scanned `b3_points_v001.py` |

**Checks:** 81 in total, 0 failed.
- V001: 32/32.
- fs-columns taps, custody and potential: 28/28.
- reference + body taps and custody: 21/21.

**Reproducibility.** The REF checks were run twice: once alone (`B3_TAP_COMPARE_REF_V001.json`) and once with BODY. All REF values are bitwise equal across the two runs.

## The tap and potential comparisons (`tools/b3_tap_compare_v001.py`)

**Independent side.** `tools/b3_points_v001.py` evaluates t, grad t and the Hessian at arbitrary 3-D points. It reuses V001's own J0, stars and gas transforms and its Cartesian and (k⊥, ψ, k_z) quadratures.
- **Gas** comes from the stage's own source elements (positions, J), assigned to their GL4 annulus columns, with m = −J/c².
- **Its imports are b3_independent_v001, math, numpy.** No tail-library code is involved.

**Module side.** The module side is the tapped jets: the replays' `uv_tail_tap.npz`, component 0. For fs columns it is also the line-v002 potential(z), built through the rebuilt module state's `lapse_pair`.

| tap | reads compared | unique (x, y) | R (kpc) | z (kpc) | tap sha256 | state digest |
|---|---|---|---|---|---|---|
| FSC_cube8 | 4000 of 4000 | 32 | 0.2064–6.0204 | -1.00–1.00 | `e95296e9c3b925f064140bd688748f7be01cb5b6e22d63bcbb507e828c86a028` | `b46c00b79df49197f79fdf052a01a4fef86111e822edc6490e65cbf7f03b0eba` |
| FSC_cyl8 | 4000 of 4000 | 32 | 0.2064–6.0204 | -1.00–1.00 | `4480c7e3b3408155497241b64616d1fa5e6c7bc2883b5e4720accf37103841cf` | `d0a374c58e648e82fc643b4b31294552ca0b6039587df5c5e04a2128eb9264ec` |
| REF_cube8 | 4000 of 4000 | 64 | 0.2014–0.2114 | -0.40–0.40 | `03336d6d3d396dae93d55c0b0a52a093b0e038ff035187038982db6a23118b83` | `49520cc801c150052c5a79309224c3bc7055130b176891f1cb3fde30fddaaae1` |
| REF_cyl8 | 4000 of 4000 | 64 | 0.2014–0.2114 | -0.40–0.40 | `fb185309adc7341367a9f62ce0be27019de77f813396c7c2f1bc34d1e132e345` | `2ec1a62cff10a139525ae9135a1d5cc1d4b3b66e1301dc006e2393914d82eb57` |
| BODY_cube8 | 4000 of 4000 | 448 | 0.2064–5.4335 | -0.92–0.84 | `37e40a058936837f6d3c4ba8d76d0f6487c9dea5ce0bc4e879cf7b91d23c6ff1` | `49520cc801c150052c5a79309224c3bc7055130b176891f1cb3fde30fddaaae1` |
| BODY_cyl8 | 4000 of 4000 | 448 | 0.2064–5.4335 | -0.92–0.84 | `cc6c885c2adff2b5e6f323eff58b136613cce48b03b2306a8f8e100e9c742f08` | `2ec1a62cff10a139525ae9135a1d5cc1d4b3b66e1301dc006e2393914d82eb57` |

**What the taps cover.** Each tap holds the first 4000 reads of its stage. The reads checked here are the stage's own TailBoundary calls; they test the wiring (positions, units, state, component).
- **FSC:** 2 distinct radii in 0.2064–6.0204 kpc, 245 distinct z in -1.00–1.00 kpc (cyl8 tap: same stage, same rule).
- **REF:** 4 distinct radii in 0.2014–0.2114 kpc, 181 distinct z in -0.40–0.40 kpc (cyl8 tap: same stage, same rule).
- **BODY:** 28 distinct radii in 0.2064–5.4335 kpc, 223 distinct z in -0.92–0.84 kpc (cyl8 tap: same stage, same rule).
- **Every other radius:** the module values at every GL4 radius were already compared in V001.

**Extra beyond the B3 text: tap Hessian ≤ 1e-6 of max.**
- FSC: cube8 3.7e-15, cyl8 2.9e-15.
- REF: cube8 3.5e-15, cyl8 3.3e-15.
- BODY: cube8 2.9e-15, cyl8 2.3e-15.

**Other fs-columns tap reads:**
- t: 5.8e-15 (cube8), 4.4e-15 (cyl8);
- grad t: 4.1e-15 (cube8), 2.8e-15 (cyl8).

Components 1–9 of every tapped jet are exactly 0 in all six taps.

**potential(z).** It is c²·⟨lr_j(z)⟩ over the 16 line azimuths, through line v002 `lapse_difference`.
- **Module pair:** `state.lapse_pair`, as `binding.line_lapse_pair` calls it.
- **Independent pair:** t(x, y, 0) and t(x, y, z) − t(x, y, 0) from the independent lane.
- **z values:**
  - up to 40 values evenly spaced through the z values the replayed solver actually evaluated (from the tap);
  - for the completed column 30, also its final GL nodes (counts in the table).
- **Arrays kept:** `out/B3_TAP_POTENTIAL_{CUBE8,CYL8}_V001.npz`, holding z, the module potential, the independent potential and the tail potential difference.

| case | column | R (kpc) | z values | max tail potential difference (m²/s²) | max total potential (m²/s²) | module − independent, over the max tail difference |
|---|---|---|---|---|---|---|
| cube8 | 00 | 0.2064 | 40 tapped + 0 final nodes | 2.581e+08 | 5.916e+08 | 9.8e-16 |
| cube8 | 30 | 6.0204 | 40 tapped + 32 final nodes | 7.44e+05 | 2.828e+08 | 1.2e-13 |
| cyl8 | 00 | 0.2064 | 40 tapped + 0 final nodes | 2.577e+08 | 5.912e+08 | 1.4e-15 |
| cyl8 | 30 | 6.0204 | 40 tapped + 32 final nodes | 7.529e+05 | 2.828e+08 | 1.2e-13 |

At column 30 (cube8), the module − independent difference is 8.9e-08 m²/s². That is 3.2e-16 of the total potential 2.83e+08 m²/s², which is the double-precision floor of the potential.

## Custody: the replays bound to the module under test

**fs columns.** The module state is rebuilt in-process from the stage's own inputs, as the binding builds it.
- Inputs: stars_registered plus roster_body of the offset `updated_base_arrays`, cfg, kept, γ_eff, eval radii and the recorded i1t.
- Cross-checks against the replay's records, each case:
  - **cube8:**
    - `custody_checkpoint_START_payload_equals_replay`: PASS (0.0e+00).
    - `custody_offset_finish_sha_equals_replay`: PASS (0.0e+00).
    - `custody_tail_config_file_sha_equals_replay`: PASS (0.0e+00).
    - `custody_kept_region_equals_replay`: PASS (0.0e+00).
    - `gamma_eff_module_equals_independent`: PASS (0.0e+00).
    - `custody_rebuilt_state_digest_equals_replay`: PASS (0.0e+00).
    - `custody_rebuilt_jets_equal_tap_bitwise_mismatches`: PASS (0.0e+00).
    - `col30_custody_rebuilt_potential_reproduces_replay_enthalpy_bitwise_mismatches`: PASS (0.0e+00).
  - **cyl8:**
    - `custody_checkpoint_START_payload_equals_replay`: PASS (0.0e+00).
    - `custody_offset_finish_sha_equals_replay`: PASS (0.0e+00).
    - `custody_tail_config_file_sha_equals_replay`: PASS (0.0e+00).
    - `custody_kept_region_equals_replay`: PASS (0.0e+00).
    - `gamma_eff_module_equals_independent`: PASS (0.0e+00).
    - `custody_rebuilt_state_digest_equals_replay`: PASS (0.0e+00).
    - `custody_rebuilt_jets_equal_tap_bitwise_mismatches`: PASS (0.0e+00).
    - `col30_custody_rebuilt_potential_reproduces_replay_enthalpy_bitwise_mismatches`: PASS (0.0e+00).
- **What this establishes.** The potential(z) compared above is, bit for bit, the potential the replayed fs-columns solver used: the solver records h = Hc − φ(z) at its final nodes, and the rebuilt state reproduces it.

**Reference and body.**
- `REF_custody_body_arrays_sha_equals_C4V005_body_finish`: PASS.
- `REF_cube8_state_digest_equals_fixture_manifest`: PASS.
- `REF_cyl8_state_digest_equals_fixture_manifest`: PASS.
- `REF_BODY_cube8_state_digest_equal`: PASS.
- `REF_BODY_cyl8_state_digest_equal`: PASS.
- The body stage refuses a state differing from the reference (UV_TAIL_REFERENCE_BODY_MISMATCH), and both replays completed.

## Replays run (0509): stage scripts only, on saved inputs

Tool: `tools/b3_replay_v001.py` (`6dc4c099b51aed1a187baa68c3f7f68a5e15a1132969abc15fb00a283b280558`), driving the route-B lane's helpers with UVT_RB_DRAFT set to `replay/`.

| job | exit | elapsed (s) | finish.json sha256 |
|---|---|---|---|
| BODY_CUBE8 | 0 | 519 | `905164345337a28642ed1c7ac22b4cda14c9e92dbd9961fe407bd7d4ca2fddbd` |
| BODY_CYL8 | 0 | 511 | `623c3dddb310da1dd91eb4ba6e1b572652f68d6ef5e5e7608e9f1129f9216b58` |
| FSC_CUBE8 | 0 | 30 | `368728bbceeb08446ec7ac15177ea354d50bf6a5237313611a450e4cad06bd8f` |
| FSC_CYL8 | 0 | 30 | `38d41b42b2eaac82ca4fd812520b8f14905679eddb0b296d52ee4cfc73aee19c` |
| REF_CUBE8 | 0 | 2655 | `82c988242c623c606300aff5ea1b33788ddd00cf105871a1d51ca68928b47fdc` |
| REF_CYL8 | 0 | 2629 | `995505ee1b99dc3c07742a4f1683cf6a7820da31fdfedacb1800b3e1b083af6d` |

**Successors** (sha256 from bytes):
- REF: `ddo_homotopy_reference_root_worker_v001_gal_c2v005_uvt_c2v003.py` `4778fc73d52973da7ab2c07bcbcfc9d0f502277fe34b5a42440962593f648c56`;
- BODY: `ddo_saved_root_body_array_root_v002_gal_c2v005_uvt_c2v001.py` `674e2b20d737b9c6e5efde54b37d15aeea14288e1e4f91e759c9a291e197ca2b`;
- FSC: `ddo_fixed_K_free_surface_root_v001_gal_c2v005_uvt_c2v001.py` `a5de0a1dd9be1115eaf8c928884ad9cdc9777eed8970899a1bd385c29acf5a15`;
- binding: `7288a5d17976cc0267316e16f6a15aab2ca5c87d810c7d498f2a3787fe571651`.

**Fixture route-A manifests** (built by the lane's fixture helper): cube8 `6f9c2222e2c63080f25ce54db571d094b227c4eb0ef9d0d31a58f320f3813f96`, cyl8 `55ff2894eac216780f371b8b923fa782a572ebdf46784c4b37c1b4173a997ff8`.

**Inputs and adaptations, disclosed:**
1. **C4R3 has no reference or body stage of its own; it admits the C4_V005 prefix.** So the reference and body replays run on C4_V005's saved stage inputs: route-A checkpoint iteration 6, the seed and the 03_body body arrays. The fs-columns replay runs on C4R3's own `01_offset`.
1. schema block V003->V005 on saved C4 per-stage configs (fields unchanged); body custody.reference_run -> this replay.
1. fs-columns controls radial_indices -> [0, 30].
1. reference successor r4 uvt_c2v003 4778fc73.
1. stage shim: driver v009-GEO _stage (lane helper C.launch).
1. tap N = 4000.
1. **fs column 0 fails under tail ON** with MASS_ENTHALPY_NOT_BRACKETED, in both cases. The C4R3 tail-OFF bracket is used.
   - Its tapped reads and potential(z) are compared above. The solver evaluated potential(z) there before refusing.
   - Column 30 completed.
   - See the observation below.

**Disk** (MB = 1e6 bytes):
- `replay/fixtures/`: 194 MB. The largest file is `b3_route_a_cube8_state.npz` at 120 MB; the fixture state arrays are written by the lane helper for the manifests.
- `replay/out/`: 126 MB. Per job: BODY_CUBE8 40 MB, BODY_CYL8 40 MB, FSC_CUBE8 4 MB, FSC_CYL8 4 MB, REF_CUBE8 19 MB, REF_CYL8 19 MB.
- Nothing was deleted (no-deletion rule); root may remove intermediates.

## Observation (TESTED on these replays; not a B3 item)

The tail at the test outer K 8 (not production K_big) is large at the centre. The tail-OFF bracket used is [151250000.0, 302500000.0] m²/s².
- **cube8, column 0** (R = 0.206 kpc), over the tapped |z| range:
  - the max tail potential difference is 2.58e+08 m²/s², against a max total of 5.92e+08 m²/s²;
  - the mass residuals at the bracket ends are -0.8279 and -0.3007, so the column is under-mass at both ends;
  - the saved tail-OFF C4R3 column 0 converged at Hc = 300356198.3630061 m²/s².
- **cube8, column 30** (R = 6.020 kpc):
  - the tail is 0.26% of the max total potential;
  - Hc = 284679166.86087847 m²/s², against tail-OFF 284444519.1696286 m²/s² (+0.082%).
- **cyl8, column 0** (R = 0.206 kpc), over the tapped |z| range:
  - the max tail potential difference is 2.58e+08 m²/s², against a max total of 5.91e+08 m²/s²;
  - the mass residuals at the bracket ends are -0.8279 and -0.3005, so the column is under-mass at both ends;
  - the saved tail-OFF C4R3 column 0 converged at Hc = 300356198.3630061 m²/s².
- **cyl8, column 30** (R = 6.020 kpc):
  - the tail is 0.27% of the max total potential;
  - Hc = 284688711.7065489 m²/s², against tail-OFF 284444519.1696286 m²/s² (+0.086%).

**Relevance:** the A32 full-hull bracket rule for tail-ON calls.

## Process and load

- **Replays:** at most 2 processes, nice 10, single-thread BLAS, per 0509.
- **Comparisons:** started after 0527 lifted the caps. FSC and REF ran beside the 2 body replays.
- **Single-thread BLAS was kept on purpose:** the bitwise custody checks must reproduce the replay's own environment.

## Disclosures

- `tools/b3_points_v001.py` (a Hessian path added) and `tools/b3_tap_compare_v001.py` (rewritten) were revised before any comparison was run. No comparison output exists from an earlier version.
- The tool shas were recorded at the first comparison launch (`out/run_tap_compare_tool_shas_V001.txt`) and re-verified before the REF+BODY run: unchanged.
- **Single reviewer.** No separate helper lanes are available. The independent lane is my own code (V001 plus `b3_points`), sharing no code with the module.

