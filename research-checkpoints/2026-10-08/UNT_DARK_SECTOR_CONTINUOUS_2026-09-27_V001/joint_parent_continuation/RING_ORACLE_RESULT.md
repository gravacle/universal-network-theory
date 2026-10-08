# Independent Newtonian ring oracle: authenticated result

2026-09-28. **COMPLETE: 397 checks, 20 model/radius cases, no failed checks.**
The parent ran the frozen worker once: 0.0926301 seconds and 40,288,256 bytes
self RSS. This review rechecked saved hashes, check arithmetic and retained
values; it did not rerun a field calculation or change frozen files.

## Custody and numerical qualification

All 11 frozen source identities match current files. The result's freeze
link and canonical payload digest also match:

    RING_ORACLE_FROZEN.json
    2942e7f9a01b68b44cc2c3138ae1e1c1d2fdb977af837bfa1ef77894d6d36ddb
    RING_ORACLE_RESULTS.json
    0d296b8e2025051b407f7cc4af17b203d01e17fd2d509941c99e9d6fecd3441f
    canonical payload
    a07dac00ab93b1e4f2d321cae0eb85eeed0afb91548996768e0fd5be781ce1d2

Largest retained discrepancies:

| Check | Observed maximum |
|---|---:|
| AGM elliptic integrals against direct angular quadrature | 2.52e-15 scaled |
| Signed ring kernels against direct angular force/potential | 4.67e-15 scaled |
| Finite-height Kuzmin radial force against exact solution | 9.44e-13 absolute |
| Galaxy order48/order96 force or potential | 1.83e-15 scaled |
| Numerical mass plus exact omitted tail against source mass | 3.37e-15 relative |
| Two successive height extrapolants | 3.136e-4 scaled |

The largest height difference occurs at 2.7 kpc and is about 0.0314 percent
of the force. It is an observed convergence diagnostic, not a rigorous
remainder bound. The Kuzmin potential difference is 4.77e-7, consistently
inside its prospective analytic omitted-tail bound; the known distant
potential offset is not concealed as roundoff. Galaxy omitted-tail force
bounds are below 6.14e-14 `(km/s)^2/kpc`.

## The four modeled source masses

All masses below include the one declared helium correction in each gas
component. No mass normalization or tail was adjusted to a velocity.

| Component/choice | Mass in solar masses |
|---|---:|
| Stars, common fixed continuation | 1.5753633648e10 |
| H I, truncated endpoint | 1.5011373222e10 |
| H I, exponential endpoint | 1.5134141725e10 |
| H2, truncated endpoint | 3.8952607312e8 |
| H2, exponential endpoint | 5.7477950872e8 |

Totals for `(HI_tail,H2_tail)=(0,0),(0,1),(1,0),(1,1)` are respectively
3.1154532943e10, 3.1339786379e10, 3.1277301446e10 and 3.1462554881e10
solar masses. These follow the declared interpolated sources, not a claim
that every observational component or its uncertainty is now known.

## Retained midplane-force estimates

The entries are the finer `2*g(z/2)-g(z)` estimate in `(km/s)^2/kpc`.
Positive means an inward physical acceleration; no signs were discarded.

| R (kpc) | HI0/H2 0 | HI0/H2 1 | HI1/H2 0 | HI1/H2 1 |
|---|---:|---:|---:|---:|
| 2.7 | 1501.88348 | 1499.90211 | 1501.87709 | 1499.89572 |
| 8.7 | 948.44907 | 958.28300 | 948.42778 | 958.26171 |
| 20.7 | 271.83621 | 274.23499 | 271.77476 | 274.17354 |
| 35.7 | 117.87961 | 118.55234 | 117.67281 | 118.34554 |
| 43.7 | 94.12158 | 94.55861 | 93.34199 | 93.77902 |

The signed-component check matters. At R=2.7 kpc and the smallest retained
height 0.01875 kpc, truncated H I contributes **-12.33684** while stars
contribute +1487.00263: the gas's outward contribution is preserved despite
its positive mass density. At R=43.7 kpc, z=0.0285519 kpc, truncated H I
instead contributes +56.58976, larger than the stellar +36.53916. Extending
H I beyond the measured endpoint adds mass but reduces the inward field at
these interior checkpoints. This is ordinary disk geometry, not a new UNT
effect, and illustrates why neither a spherical enclosed-mass substitution
nor unsigned component-speed addition is an adequate source check.

## Interface scope and next comparison

This qualifies the independent Newtonian force oracle for the 20 declared
interior checkpoints. The public `field()` currently asserts
`0<R<source_cutoff`, where the common numerical source cutoff is 117.5 kpc.
It therefore **cannot directly provide a 255-kpc outer boundary** despite
the earlier general interface intention. No such boundary mesh was run.
Supporting exterior evaluation requires an additive reviewed extension of
the panel/tail-bound logic, not bypassing its assertion or modifying the
now-frozen oracle. The declared interior results are unaffected.

The finite-volume Newtonian runs can next be interpolated to these five
radii and compared against their matching source alternative, with the
finite-volume boundary approximation and radial interpolation made explicit.
No such saved run was available when this note was written. No nonlinear
or observed-galaxy success follows from this Newtonian qualification alone.

Review roles: this reviewer derived and implemented the oracle, so this is
not an independent audit of its own authorship. The independent method is
the ring integral versus the parent's finite-volume solver. The math agent
separately checked the ring identities, AGM correction and height-limit
formula; the parent reviewed, froze and executed the implementation.
