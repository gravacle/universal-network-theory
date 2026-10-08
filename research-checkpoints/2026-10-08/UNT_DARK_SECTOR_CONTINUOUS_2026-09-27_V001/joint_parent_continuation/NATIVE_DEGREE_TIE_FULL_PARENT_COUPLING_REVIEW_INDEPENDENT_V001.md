# Independent review: exact first-tie parent off-block coupling

2026-09-30; `short_path_adversarial`. Complete source-only reading and independent
hand algebra; no numerical run, import, eigensolver, coefficient adoption or
ledger change. Reviewed `NATIVE_DEGREE_TIE_FULL_PARENT_COUPLING_V001.md`, SHA
`def8c842be9bd1bbd21ae8cd0a6338160ac28d81aaab2851371b519b75205390`.

**Verdict: PASS; no correction requested.** The exact off-block statements and
fixed-N bare second-order coefficient are justified. They do not establish a
uniform full-parent source gap or lift the projected static-response theorem.

## Independent checks

- A matching can leave P only by addition. Joining a matched and unmatched
  vertex produces a two-edge path, one degree-two penalty, and two matching
  parents; there are 2m(N-m) such additions. Joining distinct matched endpoints
  produces a three-edge path, two penalties, and one matching parent; there
  are m(m-1) additions. Distinct m have orthogonal Q images by total edge count.
- The resulting Gram matrix has diagonal
  h^2[2m(N-m)+m(m-1)] and one off-diagonal h^2 for each endpoint slide. Its
  nonnegative symmetric constant-row-sum adjacency has degree 2m(N-m), so
  its largest Gram eigenvalue is exactly h^2*m*(4N-3m-1). Maximizing the
  quadratic over real m yields the declared upper bound, while the exact norm
  uses the integer maximum. The m=0 and m=N cases are retained correctly.
- For a fixed left star, a matching column has at most N-1 illegal additions
  and an excluded row has at most two parents through that same star.
  The rectangular row/column-sum norm bound is therefore sqrt[2(N-1)].
  The degree-diagonal source contributes no QTP, giving the stated anchored
  norm after retaining the full S/N term. Entrywise absolute domination by
  the flip matrix also justifies the bounded-profile off-block bound.
- The opposite constant-layer source is the difference of the full degree
  penalties. It annihilates P and has QTP=0, but is not the zero operator in Q.
  The projected dark-plane selection rule cannot be imported into the dressed
  full parent without controlling this QTQ insertion.
- Differentiating the fixed-P Feshbach expression at fixed E gives both
  off-block source terms and the positive-sign R_Q QTQ R_Q term. The sign
  follows from differentiating (E-QHQ)^(-1) with respect to the affine source.
  Energy dependence and higher source contacts cannot be discarded. At finite
  N, E0 lies strictly below the Q compression ground: equality would put the
  unique strictly positive full ground wholly in Q, a contradiction. This
  does not supply a lower bound uniform in N.
- The two bare denominators are -2U and -4U. On the right-trivial fixed-m
  space, right-endpoint slides contribute m(N-m) times the identity and
  left-endpoint slides are the Johnson adjacency. For F(A)=sum_(i in A)x_i
  with sum_i x_i=0, direct replacement counting gives
  A_Johnson F=[m(N-m)-N]F. The stated positive difference
  K2_standard(m)-K2_singlet(m)=h^2*N/(2U)=Omega^2/(2UN) follows.

## Scope of the useful progress

The coupling norm is uniformly bounded despite the much larger full flip norm;
the anchored off-block source is additionally suppressed. These are exact
parent-operator facts. They sharpen the next control problem but do not solve it.
Even a separately proved O(U) interacting eliminated gap gives only an O(1)
self-energy norm estimate, insufficient by itself to preserve the presently
proved O(N^(-1/2)) projected source-gap lower bound under a naive norm comparison.
That inconclusiveness is not evidence that the actual parent gap closes.

The bare K2 cancellation is at the same m and in the specified source sectors.
Its shared diagonal term still depends on m; the two radial eigenvectors need
not sample it identically. Therefore the coefficient identity is not an
eigenvalue-splitting theorem, an all-N effective approximation, or a source
susceptibility calculation. The note preserves these distinctions correctly.

The constructive next theorem is representation-resolved control of the
interacting self-energy and its source derivatives, including the layer-odd
singlet channel and all contact/normalization factors. A failure to prove that
control is not itself a newly discovered response. Formation, clock, geometry,
volume, absolute pressure and observational comparison remain outside these
operator statements. No further numerical sweep is recommended by this review.
