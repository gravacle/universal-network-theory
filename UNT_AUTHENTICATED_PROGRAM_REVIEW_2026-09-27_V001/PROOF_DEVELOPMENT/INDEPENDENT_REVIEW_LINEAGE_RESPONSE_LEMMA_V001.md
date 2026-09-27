# Independent review of the finite marginal-sufficiency lemma

Date: 2026-09-27. Verdict: **ACCEPT_FINITE_DIMENSIONAL_MATHEMATICS_WITH_STATED_SCOPE**.

Originally reviewed `LINEAGE_RESPONSE_LEMMA_V001.md` at SHA-256
`64d8fac2bdf3a60a504ad1513fd8c0e48ee929f2e10c6930d242c2fa2d23f9d7`.
The reviewed final status-reconciled source has SHA-256
`0e7c0d213778710757ed6b08c9dd842104b7f59033b8e8f31667e863029ca51b`.
An integration check compared the entire source before and after reconciliation:
only its pending-review header and final review-status sentence changed. The
mathematical statements, proof, proposed test, and their scopes are unchanged.
The acceptance is project-internal analytic review, not external peer review or
verification of the proposed UNT all-size hypotheses.
The exact rational toy `verify_lineage_response_toy.py` was inspected at SHA-256
`eb77da90af96d93630f1e3ed426f6218e1751c08ff0285a259809090ca8d17e3`
and run with `python3 -B`; it passed. The toy checks one classical diagonal
sector, not all quantum directions or an UNT calculation.

No mathematical error was found in the equivalence, dual criterion or bounds.
The acceptance is for the elementary finite-dimensional linear-algebra theorem
under its stated domain and channel assumptions, not a claim of originality,
an exact proof of the numerical L4 response, or a physical theory of gravity.

The full-domain equivalence is sound: kernel annihilation implies equal outputs
for equal retained marginals; the converse uses an interior full-rank state and
small Hermitian zero-marginal perturbations. The perturbations preserve trace
and block support. Linear factorization is well-defined precisely on the image
of the retained-information map. This does not make the factor map a physical
channel combining unknown input marginals.

The sector product has the correct normalization `s_q tensor c_q / p_q` and is
a valid state with the same complete marginals and sector weights. Its zero
weight convention follows from positivity. Product-comparator invariance and
marginal sufficiency are equivalent because the comparator depends only on
those marginals; no linearity or universal physical implementation of the
decorrelation map is assumed.

The Hilbert–Schmidt orthogonal complement is the sectorwise local-sum space
`A_q tensor I + I tensor B_q`; the traceless/traceless basis has dimension
`(dS^2-1)(dC^2-1)`, including the zero-dimensional factor cases. Compression of
the pulled-back observable onto the block input algebra is correctly stated.
For restricted reachable families the necessary and sufficient subspace is the
span of actual equal-marginal pair differences, not automatically the full
zero-marginal kernel. The note explicitly preserves this distinction.

Trace-distance contraction gives `Delta_C <= ||Gamma||_1/2 <= 1`; the bounded
observable lower bound has the correct factor of two. For effects the factor
disappears because the output difference has trace zero. A common final carrier
unitary preserves trace distance and can change fixed occupation readouts.
None of these facts says every input correlation, or every interacting channel,
produces a nonzero response at a particular physical checkpoint.

The L4 implication is appropriately typed: its numerically resolved actual/
product pair refutes marginal sufficiency for that pair and hence the larger
full state domain at the declared numerical-certificate scope. It does not
become an exact symbolic nonzero theorem without a separately certified bound.
The first-pass unread carrier closure has a different continuation/domain and
is not contradicted.

The proposed `d4/2` persistence floor is an arbitrary exploratory design choice
anchored to an openly known development value. This review does **not** endorse
it as physically motivated, natural, or necessary. It is currently an example
of a falsifiable finite rule; any actual selection needs a separate prospective
freeze and a justification for the scientific question it answers. Passing it
at L6/L8 would not prove an all-size law. The proposed all-size overlap bound
would mathematically imply a uniform response bound, but proving that overlap
from unchanged parent dynamics is precisely the outstanding work.

No dark-matter, dark-energy, metric, curvature, cosmological-ratio or Einstein
claim is established by this lemma. Its useful contribution is to identify
what a further proof must control: an actual correlation component together
with its noncancelling response under the specified continuation.
