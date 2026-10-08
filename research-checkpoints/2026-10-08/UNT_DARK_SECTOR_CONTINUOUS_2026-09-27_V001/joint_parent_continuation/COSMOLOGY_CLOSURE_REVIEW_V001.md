# Independent review of the conditional cosmological closure

2026-09-28. Read-only scientific and saved-arithmetic audit. No cosmological
integration, fit, new population, or change to the inherited vacuum matching.

## Verdict

The calculation correctly identifies what the unexcited, geodesic-clock branch
does and what it does not supply. With the already reference-calibrated vacuum
and either stated standard-BBN baryon benchmark, the illustrative late-time
flat branch gives H0 = 61.84088745 or 61.89665064 km/s/Mpc. Reproducing the same
adopted reference H0 would require an additional positive dustlike coefficient
7.35302235 or 7.09514380 times the baryon coefficient. These are conditional
energy-budget requirements, not a derived native abundance, an independent
cosmological fit, or evidence of a measured new component.

The construction has a useful falsifiable consequence: homogeneous zero mode
amplitudes stay zero under the retained equations. A source preparation or
population mechanism is therefore scientifically necessary if the excited
branch is to supply the missing budget. Calling the permitted oscillator
energy “network energy” alone does not predict its magnitude. Conversely,
an actually derived occupation and its energy transfer can be tested with
these same equations without adding a separately fitted dust component.

## Mathematical checks

- The on-shell scalar-mode energy and pressure, their continuity equation,
  and their quadratic/dust and quartic/radiation limits agree with the retained
  action. Those statements do not import unproved perturbation stability.
- For H² = L + B x³ + R x⁴ + K x², the secant slope of
  (H² − L − R x⁴)/x² against x is B. The curvature cancellation is exact.
- Assigning the missing present coefficient E to curvature closes H0 only:
  the reference minus curved-branch H² is E x²(x−1), not zero at later x.
- The ideal dust-plus-vacuum age formula is correct for that extrapolated
  branch. Its roughly 22.8–22.9 Gyr central values are not a full early-universe
  prediction; radiation and the state history were excluded from this
  illustrative arithmetic.
- A linear clock-charge density that redshifts as a⁻³ is distinct from a
  freely specifiable positive homogeneous population. The sign and boundary
  qualifications in the governing note must be retained.

## Saved-data audit

The script was read without rerunning its publication path. A separate
standard-library calculation authenticated all nine recorded input files,
the reference freeze and canonical result-payload digest, all nine inherited
reference cases, and both BBN choices. All 18 combinations and all four
redshifts per combination were retained. Independently evaluating the ages
with the logarithmic form of asinh, the closure fractions, q0, transition
redshift, three histories and curvature identity gave 612 scalar comparisons;
maximum error scaled by max(1, absolute values) was 2.23642e-15.

- Arithmetic source SHA-256:
  `75b01c29db6c806f026308e7a0ee5679db182551b23dd00cbb622bd524731610`.
- Saved arithmetic result SHA-256:
  `258097f5a80c8cfb4891d93e02a1f6224eb54b73014c276683f05c8b3989f153`.

This audit verifies custody and arithmetic, not independence of the inherited
cosmological calibration. The BBN figures remain the two named external,
standard-theory benchmarks; their use is explicit and conditional rather than
a silent scale/domain import. No statistical significance or complete DM/DE
resolution follows from these comparisons alone.

Reviewed artifacts: `COSMOLOGY_CLOSURE_TEST_V001.md`,
`cosmology_closure_arithmetic.py`, `COSMOLOGY_CLOSURE_ARITHMETIC.json`, and the
authenticated inherited shape-reference inputs.
