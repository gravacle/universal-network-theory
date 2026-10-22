# FIXTURES_N2_0451_V001: N2 implementation fixtures for 0451

- **Role:** N2, the local implementation-fixture helper inside the Claude4 review lane.
- **Scope:** this is not an acceptance verdict. It is synthetic analytic geometry only: no project data, no project run, no field or parameter search.
- **Contract:** `ANNULAR_KNOT_RADIAL_CORRECTION_CHOICE_V001.json` `58ffcbb8…`. Its pin is verified at run time, and so are the helper `87866875…`, the v001 scalar module `3bd792ba…` and the v001 helicity module `280149dc…`.
- **Module use:**
  - Only `_spline_matrices` from the pinned helper is called, on synthetic knots.
  - The v001 scalar and helicity modules are read as text and never imported.

## Files

| file | sha256 |
|---|---|
| `fixtures_n2v001.py` (harness) | `ae9e35cd699d8ccbc0b06a8efd39bab0311f12f8bbdc9282a4082d139f9dae79` |
| `fixture_results_n2v001_self.json` | `79a7586ffd5a1164e919c14242c511cb3087b94339d6b926ecc06aca6fbd5d2f` |
| `fixture_results_n2v001_c3.json` | `ac2070ae371c6c17d09887908a056e397f59b6c77d18ee300e00a0ceb94ac165` |
| `c3_snapshot_23bb22fb/annular_knot_maps_c3v001.py` (`cmp`-identical to the frozen 0450 file) | `23bb22fb94c3a6b39b84479a1c5e03812fbcdeaf6180ca85ddad083a3d3d92c4` |

## Run commands

Run from this directory with `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1`. The interpreter is `PY=/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3` (3.12.14, numpy 2.3.5).

```
$PY -I -B fixtures_n2v001.py --self --out fixture_results_n2v001_self.json
$PY -I -B fixtures_n2v001.py --module c3_snapshot_23bb22fb/annular_knot_maps_c3v001.py \
   --scalar-fn build_annular_scalar_maps --helicity-fn build_annular_regular_helicity_maps \
   --adapter c3v001 --out fixture_results_n2v001_c3.json
```

Runtimes are 5.8 s and 1.6 s. No bytecode is written.

**Built-in adapter `c3v001`:**
- It supplies `old_scalar_maps` through a v001-convention input emulator. The emulator is written from the v001 text (L17-38) and uses the helper spline exactly as v001 L19-21.
- It does not repeat v001's input validation, so the malformed probes reach the module's own checks.
- The self-run checks the emulator against my independent expectation:
  - zeta and weights are bitwise equal;
  - root derivatives agree to 9.3e-14;
  - value blocks agree to the Bonnet recurrence to 2.8e-15, and off-diagonal blocks are zero.
- The caller tolerances are `edge_absolute_tolerance = weight_relative_tolerance = 64·eps = 1.42e-14`. Rank controls are rel 1e-12 and abs 0.

## Synthetic geometry

Each geometry has 18 random annuli in s=(R/L)² with 0=s₀<…<s₁₈=1. Each annulus has `leggauss(4)` nodes in s. Nodes are R=L√s, and weights are (L²/2)(b−a)/2·Wᵢ, summing to L²/2. Roots are [c−h, c+h] from smooth c(s), h(s) with h>0 and |c|<h. Each column has 32 z nodes.

| geometry | L | geometry shape | z rule | min Δs |
|---|---|---|---|---|
| G1 | 3.0 | linear in s | split 16+16 GL at random t | 0.031 |
| G2 | 2.5e20 | smooth, nonlinear | split | 0.031 |
| G3 | 0.7 | smooth, nonlinear | plain 32-point GL | 0.032 |

## Independent expectation

- Edge truth comes from the generator.
- The natural cubic cardinal basis on the 19 edges uses an own Thomas solve with power-form evaluation.
- Legendre polynomials and their derivatives come from the Bonnet recurrence.
- The root derivatives follow the v001 convention: a 72-node natural cubic in s, with an own spline.
- The contract chain rule uses V=B_jP_a, ∂_RV=B_R,jP_a−B_jP'_a(c_R+ζh_R)/h and ∂_zV=B_jP'_a/h.
- Raw helicity maps use d/dR(R/L)^e=e(R/L)^(e−1)/L.
- Column norms are the norms of the literally stacked (UR,UP,UZ)/L.
- The exact outer rows are [½T,½T,0] with T=kron(e₁₈,I₈).
- The null-space projector I−Bᵀ(BBᵀ)⁻¹B does not depend on the QR basis.

## Fixtures and tolerances

### F-edges
- Recovered edges equal the generator edges within 1e-13 absolute.
- s₀=0 and s₁₈=1, with a bitwise flag reported.
- Fail-closed: the module must raise on each of these 14 probes per geometry (42 in all over G1-G3):
  - one inner node moved 1e-9 relative, and one group-end node moved 1e-9;
  - one weight changed 1e-9, and a sum-preserving pair of weights changed 1e-9;
  - s₀=1e-9;
  - s₁₈=1−1e-9;
  - all edges shifted −1e-9 with the measure kept exact;
  - an overlap of 1e-7 with a compensating gap, and an overlap of 1e-7 alone;
  - two groups swapped, and the nodes reversed within one group;
  - GL nodes placed in R instead of s, with the measure kept exact;
  - L mismatched by 1e-9;
  - 68 nodes.
- INFO: a valid geometry with a last annulus of width 1e-3.

### F-scalar
- trial_shape is 19×8 and quadrature_shape is 72×32.
- `value`, `partial_R` and `partial_z` are 2304×152, real, and within 1e-12 relative of the expectation.
- The outer trace equals kron(e₁₈,I₈) within 1e-15, with a bitwise flag reported.
- The surface traces and `radial_derivative` match one of the two possible generalizations.
- **Intrinsic check:** this uses only the module's node values. The cubic per annulus through its 4 GL nodes must give:
  - δ_jk at all 19 edges, within 1e-12;
  - C¹ and C² continuity;
  - S''=0 at s=0 and s=1;
  - consistency with the module's dB/ds at the nodes.

  The last three hold within 1e-9 relative, and the whole check uniquely characterizes the natural cubic cardinal spline.

### F-chain
- ∂_RV and ∂_zV agree with central finite differences of the analytic V(R,z) to 1e-6 relative, with steps of 1e-6·L and 1e-6·h. The half-step error is also reported.
- The chain term is 63-71% of max|∂_RV|.

### F-preserve
- Roots are bitwise identical.
- zeta and weights_RdRdz are within 1e-14 relative.
- Root radial derivatives match the v001 72-node convention within 1e-11.
- Target only: custody fail-closed probes:
  - root derivatives off by 1 ulp;
  - one value-block entry off by 1 ulp;
  - one weights_RdRdz entry off by 1e-9;
  - wrong v001 sha and wrong helper sha;
  - tolerance `None`.

### F-helicity (m=1..6 on every geometry)
- Status is REGULAR.
- All 10 maps are 2304×448, and the transform is 456×448.
- Exponents are |m+1|, |m−1| and |m|.
- Norms are within 1e-13.
- Braw is exactly 8×456 with the vertical block zero, so there is no lid.
- Singular values are within 1e-12, and threshold = abs + rel·σ_max.
- Z = diag(norms)·T is orthonormal within 1e-12, with max|BZ| ≤ 1e-13 and the projector within 1e-12. It has 448 columns.
- The true-outer ξ_R in reduced coordinates is ≤ 1e-13.
- **All 10 maps equal raw maps @ ONE returned transform**, within 1e-11.
- divU equals the identity built from the returned maps.
- For random y, the finite-difference product rule, chain rule and divergence of the physical field hold to 1e-6.
- Fail-closed: rel=2 forces an unresolved rank.
- INFO: m=0 and m=7.
- Target only: a 1-ulp mismatch in R and a 1e-12 mismatch in L must both raise.

### F-noproj
- An AST scan finds:
  - no linalg calls other than svd/qr, and no solve outside a spline function;
  - no rho, density, mass, ridge, clip or symmetrization identifiers;
  - only static top-level statements.
- No callables are returned.
- Calibration: the v001 scalar and helicity texts give PASS, and a synthetic density-projection snippet gives FAIL.

## Self-run result

| comparison | result |
|---|---|
| Expectation against the pinned helper spline | values ≤7.1e-16, dB/ds ≤5.1e-16, 72-node geometry derivative ≤4.5e-16; the outer and axis rows are bitwise e₁₈ and e₀; cardinality at the knots is exact |
| Reference suites (own spline and helper spline) | 360 PASS and 14 INFO each, 0 FAIL |

## Mutation table

Each mutation is run on G1, m ∈ {1,2,6}. All 14 are detected, and the unmutated reference gives 0 FAIL.

| mutation | detected | by |
|---|---|---|
| knots = 72 nodes (old maps) | yes (39 failed checks) | edges, scalar, chain, helicity |
| missing 2R/L² | yes (10) | scalar, chain, helicity |
| wrong sign of the ζ chain term | yes (8) | scalar, chain, helicity |
| 576 slices left in place | yes (3, build error) | helicity |
| ξ_z lid added | yes (15) | helicity |
| different transform for derivatives | yes (6) | helicity: shared transform, finite-difference product rule |
| outer trace at s₇₁, not s=1 | yes (13) | scalar, helicity |
| root derivatives zeroed | yes (9) | preserve, scalar, chain, helicity |
| exponents swapped | yes (18) | helicity |
| transverse norm missing ½ | yes (12) | helicity |
| edge tolerance 1e-6 | yes (6) | edges, fail-closed |
| weight check skipped | yes (2) | edges, fail-closed |
| sorting unordered input | yes (2) | edges, fail-closed |
| density projection with ridge (static) | yes | noproj |

## Frozen Claude3 module c3v001 `23bb22fb…` (done-0450, 0005)

The snapshot is `cmp`-identical and the harness ran only on the copy. **Result: 390 PASS, 20 INFO, 0 FAIL, 0 ERROR.** The static scan PASSes: the only linalg calls are svd (L282) and qr (L293), it imports only numbers and numpy, and its top level is static.

| check | worst over G1-G3, all m |
|---|---|
| edges against the generator | 3.3e-16; s₀ and s₁₈ bitwise 0 and 1 |
| V, ∂_RV, ∂_zV against the expectation | 7.6e-15, 4.8e-14, 6.4e-15 |
| outer trace | bitwise kron(e₁₈,I₈) |
| intrinsic: cardinality, C², natural ends, node derivative | 1.4e-14, 1.4e-13, 1.9e-14, 7.0e-14 |
| finite differences: ∂_RV, ∂_zV | 3.9e-9, 1.4e-10 |
| zeta, weights, roots | bitwise; root derivatives 9.3e-14 against own, 5.4e-14 against helper |
| helicity: norms, orthonormality, BZ, projector, outer ξ_R | 4.9e-15, 1.5e-14, 1.5e-16, 1.5e-14, 7.3e-18 |
| all maps at one shared transform; divU identity; physical finite differences | 5.7e-14; 0; 6.2e-9 |
| fail-closed probes | 69 of 69 fail closed: 66 raised the module's own ValueError (42 edge, 18 custody, 6 helicity input-mismatch), and 3 rank probes returned `UNRESOLVED_OUTER_CONSTRAINT_RANK` |

None of the following is a defect. They are observations that root needs when choosing tolerances or interfaces:

1. **The weight tolerance gates two checks.** `weight_relative_tolerance` gates both the 32-term custody check at L134-137 and the RdR GL check at L162-166.
   - Consider a packet that v001 accepts, because L18 allows Σwz=2h at rtol 1e-12, but whose z-weight sum is off by 5e-13. The custody check refuses it at 64·eps, with message "relative 5.002e-13".
   - Root's `weight_relative_tolerance` must therefore cover its actual z-weight sum deviation, and that loosens L162-166 to the same level.
2. **The weight residual at L162-163 scales like eps·s/Δs.** It is computed from differences of recovered edges.
   - A valid geometry whose last annulus has width 1e-3 is refused at 64·eps in G2 and G3, with residual 1.1e-13.
   - My reference implementation does the same, so this is a matter of tolerance selection, not a defect.
3. **Two array meanings changed, as documented by Claude3.**
   - `radial_derivative` (L196) is now dB/dR, 72×19 (v001: 72×72).
   - `lower_surface_trace` and `upper_surface_trace` (L194-195) are now kron(B,·), 72×152.
   - Consumers that expect the v001 shapes fail on shape rather than silently.
4. **One v001 ingredient remains in ∂_RV, by contract item 3.** The preserved v001 72-node-spline root derivatives (c_R, h_R) carry their own approximation. On the nonlinear synthetic geometries, ∂_RV differs from a finite difference of the analytic generator geometry by 2.9e-3 (G2) and 3.9e-3 (G3), relative to max|∂_RV|. This is information about the preserved convention, not about project data.

## Limitations

- The results come from three synthetic geometries.
- The caller tolerances are mine, not root's.
- The emulator stands in for the actual v001 `build()` output.
- None of this says anything about convergence, physical adequacy or the project packet.
