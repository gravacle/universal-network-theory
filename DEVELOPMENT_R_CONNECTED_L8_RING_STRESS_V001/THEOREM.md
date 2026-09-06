# Connected L8 ring interaction stress — numerical result

## Scope and parent

The 256 retained heads of the conditional R-B preparation split into 32
eight-site rings along the inherited second generator. Unlike R-C's disjoint
two-record blocks, every site participates in two native transfer terms.

On each ring the source is off and

\[
 H=-\sum_iT_{i,i+1}+\sum_i(-1)^i q_i,
\tag{K01}
\]

with periodic `i`. This uses the native F3 transfer and onsite terms. The
initial state is `(|B>+|x>)^tensor8/sqrt(2^8)`, inherited from the adopted
`alpha=r0` preparation; that attachment is not bare-F3 derived. The complete
failure-inclusive qutrit/controller/work/reference read remains in force.

## Computation

The script constructs the full `2^8=256` blank/content matrix, diagonalizes
it with NumPy, evolves for `tau=pi/(2sqrt(2))`, and independently integrates
each oriented current in the energy basis. No dense `3^512` evolution occurs.

For one ring the result is:

- occupations alternate `0.312588864610359` and `0.687411135389641`;
- integrated currents alternate `+/-0.093705567694821`;
- nearest-neighbor connected occupation correlation is approximately
  `-0.026133160509504` on every edge;
- retained total changes from `4.0` to `3.999999999999999`;
- record-number-law maximum change is `4.17e-16`;
- record-ledger residual `r1=1.59e-15`, `r_infinity=3.47e-16`;
- norm and energy errors are `1.12e-16` and `4.45e-16`.

Across 32 identical rings, expected retained total remains `128` within
`3e-14`. Absolute oriented throughput is approximately `23.988625330...`,
while the signed ring-current sum is zero within numerical tolerance. The
connected correlation is nonzero: the calculation is not a disjoint-block
relabeling.

## Classification

This is **controlled numerical evidence**, not an exact result. The tiny
nonzero ledger residual is consistent with floating-point diagonalization and
current integration because it lies below the preregistered `2e-11` L1 and
`3e-12` Linf tolerances and beside stronger norm, energy, and number-law
controls. It is not labeled a physical defect or necessary term.

The calculation shows connected interaction, positional redistribution, and
nonzero correlations while retaining record number for this prepared pulse.
It does not establish generic retention, critical accumulation, a continuum
limit, Ward behavior, or gravity.
