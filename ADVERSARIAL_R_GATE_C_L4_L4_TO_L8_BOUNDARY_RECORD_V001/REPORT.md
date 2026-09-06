# Adversarial report: the equal-time four-port record does not close

## Disposition

`PASS_EQUAL_TIME_RECORD_NOT_CLOSED`.

The frozen six-owner surgery is reconstructed exactly. Two isolated periodic
L4 components contain 24 owners. Removing the declared six wrap owners and
adding the declared six cross-block owners gives exactly the canonical
24-owner, degree-three L8 prism.

## Exact candidate-map dimension

One L4 block has Hilbert dimension 256 and Hermitian operator space real
dimension 65,536. Its four ports have Hilbert dimension 16. The complete port
reduced density matrix contributes 256 real linear directions. Total retained
`Q` adds one independent centered-interior direction. The six internal owners
incident on a port add six pairwise Hilbert--Schmidt-orthogonal directions.
All port-port occupation moments and connected correlations are already fixed
by the complete port density and add no direction.

Therefore the candidate map has exact real rank

```text
256 + 1 + 6 = 263
```

and exact nullity

```text
65,536 - 263 = 65,273.
```

## Positive collision

Use block-A local ports `(0,3,4,7)` and interiors `(1,2,5,6)`. Compare the two
positive trace-one pure density operators with one carrier at local interior
site 1 or local interior site 5. Under the frozen embedding these are global
L8 sites 1 and 9. Join either to an all-blank block B.

Both roots have:

- `Q=1`;
- the identical pure all-blank four-port reduced state;
- zero current on every one of the six internal port-incident owners;
- zero connected occupation for every port pair; and
- zero initial current on every newly added seam.

Their difference is therefore an explicit trace-zero direction in the
candidate map's nullspace.

The future joined outputs differ. At `kappa=pi/2`, the occupation of global
site 4 is approximately zero for the site-1 root and
`0.09171808224482285` for the site-9 root. The complete terminal one-particle
product-PVM distributions have total variation one to numerical precision.

The separation is also structural rather than solely a final-time numerical
comparison. The first path from site 1 to read site 4 has length three and
one walk, so its occupation begins as `t^6/36 + O(t^8)`. The first path from
site 9 has length five and ten walks, so its occupation begins as
`t^10/144 + O(t^12)`.

## Meaning

The candidate equal-time boundary record is sufficient for equal-time
port-local expectations, but it is not sufficient for future coherent joined
evolution. Interior state and boundary-interior dynamical memory remain
unrecorded.

This is an algebraic closure-domain counterexample. It is not a claim that
the conditional uniform F3-MDC preparation selects either adversarial root,
and it is not by itself a minimum-dimension theorem for a reusable process
record.
