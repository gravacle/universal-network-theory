# Root review: uniform degree and connected arrangement bounds

2026-09-27. Analytical and exact-arithmetic verification, not observational
validation. Root read the current native source and both new derivations.
Two GPT-6 Astra Ultra agents derived/reviewed independently within the same
model family. No claim of independent physical experiments is implied.

## Uniform degree theorem

Reviewed `NATIVE_UNIFORM_REGULAR_DEGREE_BOUND_V001.md`, SHA256
`c1cf35ca125b809c748549df0f2bf5013245dc42a598189584f2b0fc85a5c592`.

Root confirms: integer deviations give H0-Ecl >= g K; the exact star norm
is N(2d0+1)-2d0^2; the defective-star expectation is bounded by
2 sqrt[N(d0+1)] k_v (or the hole version). Summing stars proves the
state-dependent flip bound without using ||V||=Omega N. Completing the
square then gives the stated O(1) ground-energy and total-defect bounds.
The result applies at any fixed Omega once a_N>0, not only in perturbation
theory. No assumption of a factorized actual ground state is required.

A useful stronger form of the incidence corollary is the diagonal operator
inequality |M-Nd0| <= K/2. Thus even the ground expectation of the ABSOLUTE
edge-count deviation is O(1), not merely the absolute difference of means.
This does not force the whole graph to be exactly regular with probability
tending to one. For example, an O(1) expected number of defects is compatible
with a nonvanishing probability of at least one defect.

For the separate small-Omega theorem, K>=2 on Q permits the relative form
bound. B=QVP satisfies B^dagger B=Omega^2 P because two distinct flips
cannot restore every degree. Schur inertia then counts rank(P) negative
shifted eigenvalues; principal-submatrix interlacing puts the rest at least
delta_N above Ecl. Feshbach elimination gives x(delta_N+x)<=Omega^2 and
the leakage ratio. The weighted-resolvent expansion with link-number parity
gives the uniform fourth-order error; none of these steps asserts a small
unweighted ||QVQ||. The unequal feasible degree-list extension uses the same
integer bound and still has K>=2 on Q.

## Connected fourth-order theorem

Reviewed `NATIVE_CONNECTED_FOURTH_ORDER_GRAPH_RESPONSE_V001.md`, SHA256
`63f74ae8336ba063c81e86551f906f18d9bf72554c7cc081ce85ccf9255a09bd`.
Root independently obtained the pair contribution

    h^4 [ (a+b)/(a^2 b^2) - (1/a+1/b)^2/(a+b+J) ]
      = h^4 J(a+b)/[a^2 b^2(a+b+J)].

It is zero for disjoint edges. The canonical normalization term is necessary
for this cancellation. The all-add scalar retains, rather than discards,
the shared energy. Counting the O(N^2 d0) affected star pairs and the
O(N^2 d0^2) possible switches gives the stated O(Omega^4/N^2) operator
bound. Every sign, gap, and canonical normalization in the source was checked.

For a ground state of the FOURTH-ORDER TRUNCATION, the variational principle
implies a bounded expected L11 deficit and vanishing deficit per vertex.
For balanced record classes with n1>=d0 and N-n1>=d0 and an attractive coefficient, root also
confirms E10+E01=2(d0 n1-L11): the extremizers segregate the two classes.
Neither statement has yet been proved for the full untruncated Hamiltonian,
the untransformed full-space L11 observable, or an actually prepared state.

## One-shot exact coefficient diagnostic

The `connected_fourth_order/` source/protocol were frozen before their sole
execution. The root and both agents reviewed the derivation; the record
agent reviewed the complete implementation before launch. The inverse agent
also returned implementation approval. Complete node-energy path sums were
compared against connected pair formulas and independent 24-order switches.
All arithmetic for scored comparisons used exact rational numbers.

Result: 178,008 exact checks passed across seven fixtures. Regular-manifold
sizes were 2,2,2,2,6,24,90; the last case was N=4,d0=2. No finite-h spectrum,
large-network extrapolation, empirical data, or new parameter fit was scored.
Both signs and the zero of the second-order arrangement coefficient were
included. Every output matrix and graph basis is preserved.

The worker completed with exit code zero, elapsed 0.750978125 seconds and
observed self peak RSS 27,820,032 bytes on Darwin. It used standard-library
Python only, no child worker or numerical library, under 30-second wall and
CPU limits. RSS was measured, not enforced as a hard aggregate memory cap.
Each of the seven completed cases was flushed and fsynced to a journal;
read-only postchecks found that journal exactly equal to final result cases.
No retry was performed. The source and protocol hashes still match the freeze.

Result SHA256:
`bc1ed57d95cd99e756a153cab1dc5f3fa292c551a6f35fdc55cf870347dddafc`.
Journal SHA256:
`372dafb794755a0519f84b64ef1a203ffad1741472678a8406f62109ddfc77c8`.
The initial manual uniform-diagonal arithmetic error and its prelaunch
correction remain documented in the protocol. It did not alter a scored
tolerance, case, or result.

## Independent dilute-addition trial

Root also reviewed `NATIVE_REGULAR_DILUTE_ADDITION_UPPER_BOUND_V001.md`,
SHA256 `84ef17b19b465f6bb028498ade4a370bb5526fd82a8bb097ba85dd27dee0f3a7`.
The exact product-trial collision term and rationalized single-qubit energy
identity are correct. Their O(1/N) error proves a variational limsup only.
It does not supply the missing matching lower bound or an actual preparation.

Final document review caught and corrected ambiguous notation in the conditional
ensemble note (the binary relative-entropy bound uses the tilted Ptheta, not
the untilted P0), an omitted surviving single-edge term in the frontier's prose,
and an insufficiently explicit full-segregation feasibility condition. These
were documentation corrections; no frozen source, protocol, or result changed.

The scientific frontier advances on size control and arrangement dynamics.
Native physical volume, autonomous population/maintenance selection, clocks,
universal gravity, and joint DM/DE observables remain unclosed.
