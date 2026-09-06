# Exact-through-L8 hydrodynamic criticality seed result

## Decision

```text
NO_CANDIDATE_L4_L8__STOP_NO_L10_L12
36/36 target checks PASS
```

No sector at any of `L=4,6,8` is a seed under the frozen rule.  Consequently
the intersection of seed-cell unions is empty.  The protocol therefore stops
before L10/L12, predictive macroscopic closure, mode universality, spatial
critical-response fitting, or two-cluster work.

This is a bounded finite-prism null for the adopted total-rail `m=1`
ground-state response diagnostic.  It is not evidence that criticality is
impossible under another authenticated parent or at larger accumulation
scales.

## Complete response table

All complete fixed-`q` eigenspectra through half filling are retained under
`RAW/`.  Particle-hole equivalence supplies the complementary sectors.

| L | q | rho | dim H_(L,q) | Delta_act | chi_tau | R_low |
|---:|---:|---:|---:|---:|---:|---:|
| 4 | 1 | 0.1250 | 8 | 2.000000000 | 0.395284708 | 0.500000000 |
| 4 | 2 | 0.2500 | 28 | 2.463075497 | 0.341638044 | 0.428094708 |
| 4 | 3 | 0.3750 | 56 | 2.645981059 | 0.317001733 | 0.386692237 |
| 4 | 4 | 0.5000 | 70 | 2.988994832 | 0.291628290 | 0.380601986 |
| 6 | 1 | 0.0833 | 12 | 1.000000000 | 0.881917104 | 0.750000000 |
| 6 | 2 | 0.1667 | 66 | 1.432775715 | 0.605628323 | 0.668501057 |
| 6 | 3 | 0.2500 | 220 | 1.667371519 | 0.520382483 | 0.632801772 |
| 6 | 4 | 0.3333 | 495 | 1.842230480 | 0.469772941 | 0.618498809 |
| 6 | 5 | 0.4167 | 792 | 1.936393471 | 0.440047139 | 0.588502634 |
| 6 | 6 | 0.5000 | 924 | 2.135581211 | 0.405535110 | 0.590417241 |
| 8 | 1 | 0.0625 | 16 | 0.585786438 | 1.584089449 | 0.853553391 |
| 8 | 2 | 0.1250 | 120 | 0.914145764 | 0.986479251 | 0.784968830 |
| 8 | 3 | 0.1875 | 560 | 1.120212007 | 0.797042810 | 0.749151133 |
| 8 | 4 | 0.2500 | 1,820 | 1.266065439 | 0.702672515 | 0.732829821 |
| 8 | 5 | 0.3125 | 4,368 | 1.382688543 | 0.641938711 | 0.724792505 |
| 8 | 6 | 0.3750 | 8,008 | 1.467715856 | 0.602147285 | 0.715899285 |
| 8 | 7 | 0.4375 | 11,440 | 1.496802967 | 0.579854287 | 0.679290394 |
| 8 | 8 | 0.5000 | 12,870 | 1.647631702 | 0.532236798 | 0.687595061 |

At every size, `Delta_act` increases across the eligible interior density
rows and `chi_tau` decreases.  Hence no row can simultaneously be a strict
local gap minimum and a strict local response-timescale maximum.  This—not a
threshold or degeneracy exclusion—is what makes the seed sets empty.

Every non-vacuum row was stable under `w_floor/10`, `w_floor`, and
`10*w_floor`; all `R_low` values are far above `1e-6`.  The largest checked
response-support eigenpair residual was `2.4851e-13`, below the frozen
`1e-10` limit.

## Structural controls

- The L4/L6/L8 prisms have `3L` unique owner edges and degree three at every
  site.
- Every owner transition preserves `Q`.
- The one-carrier spectra reproduce
  `-2 cos(2 pi m/L) +/- 1` within `3.11e-15`.
- The spectra are independent of write count because the frozen Hamiltonian
  contains no `N`.
- Particle-hole sectors are exactly related by global bit complement.
- Chiral spectral symmetry holds within `1.14e-13`.  The mid-spectrum zero
  modes were retained only as anti-false-positive controls.

## Telemetry

- environment: Darwin arm64, Python 3.9.6, NumPy 2.0.2;
- declared BLAS threads: one;
- complete elapsed time: `320.462 s`;
- maximum sector time: `158.518 s` at L8;
- maximum resident set: `8,034,484,224` bytes (`7.48270 GiB`);
- frozen guards: 45 minutes and 12 GiB per L8 sector;
- L10/L12 executed: **no**.

## Claim boundary

**Proved inputs:** finite topology and owner census, number conservation,
particle-hole map, one-carrier band identity, and authenticated binomial
sector weights.

**Adopted:** sharp-sector projection, `m=1` total-rail response channel,
density cells, and seed rule.

**Empirical:** all finite many-body spectra, response gaps, `chi_tau`,
residues, and the empty seed classification.

**Open:** any critical density, thermodynamic limit, alternate authenticated
critical channel, macroscopic closure, universal coupling, continuum
behavior, emergence, or gravity.
