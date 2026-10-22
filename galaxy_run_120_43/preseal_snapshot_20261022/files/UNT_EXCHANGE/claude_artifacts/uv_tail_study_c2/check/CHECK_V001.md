# Independent adversarial check of UV_TAIL_STUDY_V001 (track 2)

Checker lane, 2026-10-17. Read-only on the saved R3 cube states (C2R3, C3R3, C4R3, RR3). No run launched, no target or observed velocity opened, nothing imported from `tools/`. numpy only, nice 10, single-thread BLAS, at most 2 processes. Everything I wrote is in `check/` under the prefixes `adv_*` and `ADV_*`, plus this file and `CHECK_HASHES_V001.txt`.

## Verdict

**CONFIRMED WITH FINDINGS.**
- The study's numbers reproduce from an independent implementation to ≤1e-4 km/s.
- Its agreement verdict (V-c4, TESTED-NEGATIVE) holds.
- The tail formula and the symbol facts hold.
- **The stage classification has one material error (F1).** Route A, the reference and the body are not "initial geometry only". The body produces the entropy K0 from the truncated route-A field, and every route-B column solve and rotation reads K0. Between C2 and C4, K0 drifts by 22–30% in the row window.
- As a result, the plan in (d) (route-A successor "optional"; T1 puts the tail only in the columns, rotation and feedback) and the Return's attribution of the residual to route-B vertical under-binding are not established.

## 1. Tail formula and error bound (re-derived)

**Convention.** δn(x) = Σ_kept dk/(2π)³ · T(k) · S(k) · e^{ik·x}, with S = −c²ρ̂ (prep v007; ring transform −c² Σ m J0(k⊥R) e^{−ik_z z}).

**Asymptote.** Newtonian: Φ_N(k) = −4πGρ̂/k² = 4πG S/(c²k²). So

  Qinf · Φ_N/c² = [c⁴/(16πGγ_eff)] · 4πG S/(c⁴k²) = S/(4γ_eff k²).

G cancels. The tail term equals the operator's own asymptotic symbol T∞ = 1/(4γ_eff k²) applied over the omitted region, and R = ∫_omitted (q−1) T∞ S e^{ikx}, with q = 4γ_eff k² T. **This matches the study.**

**Measured on each case's own `unit_response`** (all nodes; script `adv_tail_check_v001.py`):

| quantity | C2 | C3 | C4 |
|---|---|---|---|
| max \|1−q\| for \|k\| ≥ 2 | 5.88e-4 | 5.88e-4 | 5.88e-4 |
| Im/Re of T | 2.9e-14 | 2.9e-14 | 2.9e-14 |
| I1: total vs unit·(stars + gas), max rel | 3.5e-16 | 2.3e-16 | 3.5e-16 |
| my gas-ring rebuild vs `new_gas_fourier_J` (3000 random nodes) | 6.0e-15 | 6.6e-15 | 5.7e-15 |
| my star-ring rebuild vs `fixed_source_fourier_J` | 2.9e-15 | 2.6e-15 | 2.6e-15 |

**1−q by |k| bin (C4 nodes).**

| \|k\| bin (/kpc) | 1–1.5 | 1.5–2 | 2–2.5 | 2.5–3 | 3–4 | 4–5 | 5–6 | 6–7 |
|---|---|---|---|---|---|---|---|---|
| mean 1−q | 3.8e-4 | 1.8e-4 | 1.1e-4 | 7.4e-5 | 4.8e-5 | 4.8e-5 | 4.4e-5 | 3.7e-5 |
| c = (1−q)k² | 5.6e-4 | 5.5e-4 | 5.6e-4 | 5.7e-4 | 5.8e-4 | 9.5e-4 | 1.3e-3 | 1.5e-3 |

This confirms V-b3: the 1/k² law holds on 1–4 /kpc and flattens above.

**Bound.** |R(x)| ≤ sup_{k>K} |1−q| · ∫|integrand(x)|. This is correct as a form. Two caveats (F3, F4 below):
- sup |1−q| is measured only up to 6.9 /kpc. Beyond that, A21 gives point checks only, at 30 and 1000 /kpc.
- "≤0.16% of the tail" is a ratio of maxima taken at different columns. It is not a pointwise statement.

## 2. Independent recomputation of the tail (C2, C3, C4; rows 01/05/09 shown, all 12 computed)

**Method** (`adv_tail_check_v001.py`):
- Cartesian tensor Gauss quadrature in (kx, ky, kz) over box(12)\box(K), with the quadrant reduced by D4 symmetry.
- No cylindrical reduction and no arccos azimuthal measure.
- Variants:
  - `box`: box outer cutoff;
  - `disk`: also cut to k⊥ ≤ 12, which matches the study's cylinder outer cutoff;
  - `m0`: J1 radial derivative;
  - `P16`: the rotation's actual 16-azimuth mean.
- The pinned rotation law (owned_free_surface_rotation_v001:16–20) is applied as Ω² → Ω² + δB/(A·R), with rows through the pinned adapter v002.
- With no correction, the saved rows reproduce to 0.0 and A reproduces to 0.0.

**Static tail δv (km/s), discrete source, Kb 12:**

| case | row | mine (disk, m0) | study discrete_12 | study continuum_64 | mine P16 − m0 |
|---|---|---|---|---|---|
| C2 | 01 | 5.1995 | 5.1996 | 5.2645 | 0.000 |
| C2 | 05 | 1.2084 | 1.2083 | 1.2486 | 0.000 |
| C2 | 09 | 0.6246 | 0.6247 | 0.6283 | 0.001 |
| C4 | 01 | 2.1385 | 2.1386 | 2.2079 | 0.000 |
| C4 | 05 | 0.2014 | 0.2014 | 0.2527 | 0.002 |
| C4 | 09 | 0.1428 | 0.1428 | 0.1478 | 0.014 |

- Over all 12 rows, mine minus study is at most 1e-4 km/s: 0.0013 / 0.0009 / 0.0004 τ for C2 / C3 / C4.
- Quadrature check (C2, order 8 at width 0.2 vs order 6 at width 0.25): ≤4.5e-5 km/s.
- My continuum stars (my own 48/200 radial roster, exact sech², box 12) give C2 row 01 = 5.117 against the study's stars-only 5.131 (discrete 12) and 5.158 (continuum 64). This is consistent once the Kb difference is allowed for.

**Result.** The study's integrator, source, sign, normalization and proxy are **TESTED-POSITIVE** by an independent method.

## 3. Agreement claim (prereg V005 τ_i; `adv_agreement_v001.py`)

| rows | Dhat_2_3 | Dhat_3_4 | Dhat_2_4 |
|---|---|---|---|
| uncorrected (saved) | 31.45 | 12.47 | 38.93 |
| mine: disk m0 / disk P16 | 12.39 / 12.54 | 8.90 / 9.09 | 19.24 / 18.96 |
| mine: box m0 / box P16 | 12.44 / 12.25 | 8.81 / 8.98 | 19.34 / 18.59 |
| mine: gas disk + continuum stars, m0 / P16 | 12.31 / 12.46 | 8.95 / 9.13 | 19.10 / 18.88 |
| study discrete_12 / continuum_64 | 12.38 / 12.34 | 8.90 / 8.95 | 19.24 / 19.17 |

**V-c4 (static correction does not make C2/C3/C4 agree) is CONFIRMED.** It is robust to the outer cutoff, to the azimuth rule and to the star rule: the improvement is 1.4–2.6×, and every Dhat stays above 8.

I did not recompute the sphere and cylinder cases. Their numbers, and so the cross-shape collapse (V-c5), are **not independently recomputed**. I did verify that the cylinder kept region is {k⊥ ≤ K, |k_z| ≤ K}: the driver mask is applied on G_K (v005:329–358, prereg grids). That matches `outside_measure`, and the cube arccos measure is analytically correct.

## 4. Classification against the code paths

**Confirmed citations.**
- line v002:46–61: `evaluate_line` with additive `boundary_*`.
- line v002:64–101: `lapse_difference`, with b0 and bd documented as "boundary perturbations".
- fs v005:75–87: `potential(z)` is c² times the mean over 16 φ of log1p, with zero slots at :80 and :85; `solve_column` is at :92.
- rotation v005:94–110: 16 azimuths, zero slots at :97, mean at :109, law at :110.
- feedback v004:88–101: no real-space lapse read.
- offset v003:76–95.
- body v002:72–73 also passes zero `boundary()` slots.

**F1 (MATERIAL).** K0 is a persistent truncation-dependent input that the study omits. The trace:
- body v002:84 writes K0 from `evaluate_saved_radius` over the route-A prepared field (line reads with zero slots).
- offset `updated_base_arrays` passes K0 on.
- K0 becomes `base_K_values`, then K = entropy_scale·K0, in every column solve (fs v005:52–53, 72, 92) and every rotation (rotation v005:58, 84, 110; d lnK/dR enters Ω²).

Measured (`adv_k0_drift_v001.py`):

| comparison | row window 0.4–6.2 kpc | at R < 0.4 kpc |
|---|---|---|
| K0(C3)/K0(C2) | 0.83–0.87 | 0.82 |
| K0(C4)/K0(C2) | 0.70–0.78 | 0.72 |
| inner control R vs C2 | ≤6.7e-4 | |

The control shows the drift is K-edge truncation, not inner quadrature.

Consequences:
- **(i)** The table entries "route A: not needed for the route-B fixed point (by I1)" and "reference/body: initial geometry only" are wrong. I1 covers the field and not K0.
- **(ii)** The static proxy holds K0 fixed per case, so its residual includes the K0 drift.
- **(iii)** The 18–37% root shrink from C2 to C4, cited as evidence of route-B vertical under-binding, is confounded with a 22–30% drop in K0. Polytropic scaling (H ∝ K^{3/8} for an external well to K^{3/5} for a self-gravitating layer) would give about 9–18% shrink from K0 alone. That is an estimate, UNTESTED.
- **(iv)** The direct pressure-gradient channel alone (C2 state with C3's or C4's K0 shape, h and ρ held fixed; physically inconsistent, magnitude only) moves rows by ≤0.10 and ≤0.30 km/s respectively. The main channel, through the column solves, is not computed.
- **(v)** In (d), the "route-A successor (optional)" must become required, together with the reference and body tail reads (their slots exist). Otherwise prereg T1 cannot pass for a UV-only reason. The pre-named outcome "T1 fails but T2 passes: residual is not UV" would then misattribute a UV effect (the K0 drift) as non-UV.

**Counted numerics or model change.**
- I agree it is counted numerics for the k > K completion. It is a quadrature completion with the operator's own algebraic asymptote (A21: lapse entry exactly −1/4) and a remainder measured on [2, 6.9] /kpc. The status stays UNTESTED until review, as the study says.
- The continuum source rule is two separate things:
  - For the stars, it is the exact transform of the declared sech² profile, so it is a counted quadrature.
  - For the gas, the cubic-in-s interpolant between the 4 Gauss columns per annulus is a new radial interpolation rule. Route B defines the solved gas only at the 72 columns.
- The source rule changes the outcome at the τ level: discrete-12 against continuum-64 moves rows by up to about 0.5τ (C4 row 05: 0.052 km/s against τ = 0.1). It must therefore be preregistered with numbers, not only declared.

## 5. Other findings

- **F2 (minor, implementation).** Route B reads 16 azimuths. Kept + tail(16-azimuth) equals the full field exactly, while kept + tail(m=0) leaves the kept cube's m=16 alias in place. The measured alias (cylinder outer cutoff) is ≤0.011 / 0.021 / 0.026 km/s, which is 0.05 / 0.16 / 0.27 τ for C2 / C3 / C4. That is small in km/s but not negligible against the T2 tolerance of τ/4. The tail should be evaluated at the same 16 azimuths (P16).
- **F3 (minor).** The remainder bound is about 0.01–0.015 km/s absolute, which is 0.2–0.3 τ on rows 06–08 (τ = 0.05). It is not negligible against τ/4. A per-shell sup tightens it about 4× for C4, since max |1−q| is 1.4e-4 on 4–5 /kpc.
- **F4 (minor).** The A21 and node-symbol constants differ. A21 gives 1 − Q(2)/limit = 3.1e-4 (c ≈ 1.2e-3 over 0.3–2 /kpc), against node c ≈ 5.5e-4 (mean 1.1e-4 at 2–2.5 /kpc). Both are ≤6e-4, so this is not material, but the 1/k² constant depends on direction.
- **F5 (minor).** For the discrete source at Kb 12, the box and cylinder outer cutoffs differ by ≤0.037 / 0.044 / 0.051 km/s (m=0), up to about 1τ on rows 06–08. This independently supports V-c2: the discrete UV limit is ill-posed.
- **F6 (process).**
  - The deletion of three `out/` files breaks the no-deletion rule. It is self-reported and needs registration by the root.
  - The study's own validation scripts were written into `check/` and labelled "Independent checks" in the .md. They are author-side checks; only the `adv_*` and `CHECK_V001.md` files here are independent.
  - The study's HASHES.txt verifies 56 of 56 OK from bytes.
- **F7 (overclaim).** The Return's first sentence says most of the leftover gap "comes from the gas columns, which the truncated lapse binds far too weakly in the vertical direction". The study's own V-c8 marks this UNTESTED, and F1 is a competing channel.
- **F8 (minor).** V-a1 is called "consistent with a 1/K–1/K² tail", yet the sphere's q of 0.579 lies outside the 0.35–0.50 band. It holds for 2 of 3 shapes and is descriptive only.

## 6. Claim-by-claim status (checker)

| study claim | checker status |
|---|---|
| I1 (final field = unit·final source) | TESTED-POSITIVE (re-measured, all nodes) |
| Asymptote 1/(4γ_eff k²); G cancels | TESTED-POSITIVE (derived; q measured) |
| \|1−q\| ≤ 5.9e-4 for \|k\| ≥ 2; 1/k² only on 1–4 /kpc | TESTED-POSITIVE (on 2–6.9 /kpc); above 6.9 /kpc UNTESTED except at 30 and 1000 |
| \|R\| ≤ 0.16% of the tail | form correct; ratio of maxima, not pointwise; ≈0.2–0.3 τ on rows 06–08 (F3) |
| Static tail rows (C2/C3/C4) | TESTED-POSITIVE (independent, ≤1e-4 km/s) |
| V-c4: static correction does not converge C2/C3/C4 | TESTED-NEGATIVE, confirmed (Dhat 12.25–12.54 / 8.81–9.13 across 6 variants) |
| m=16 alias negligible | partly: ≤0.27 τ (F2) |
| Route-B insertion points and slots | TESTED-POSITIVE (code read) |
| Route A, reference and body need no tail for the route-B fixed point | TESTED-NEGATIVE (F1: K0 drift 22–30%) |
| Residual = route-B vertical under-binding | UNTESTED; confounded by K0 (F1) |
| Counted numerics (k > K completion) | argued and agreed; UNTESTED until review; gas continuum rule is a new interpolation rule |
| V-c5 shape collapse, V-c6 K-swap, t6, t7 forecast | not recomputed by checker |

**Deciding test for F1.** Rerun the static proxy, or better the T1 fixed points, with K0 taken from a single grid, for example C4's route-A body, for all of C2/C3/C4. Alternatively, put the tail in the route-A/reference/body reads. If the residual Dhat falls substantially, the K0 channel is real.
