# Independent review of the local response bound

Review date: 2026-09-27. Verdict: **PASS at the explicitly conditional,
finite-dimensional mathematical scope**, with both wording refinements below
applied to the unsealed draft and analytically rechecked.
This is an independent analytic check within the project, not external peer
review or verification that the UNT family satisfies the hypotheses.

Reviewed source: `LOCAL_RESPONSE_BOUND_V001.md`, SHA-256
`6bda9fb5a825d5453240fd8c30854b7657f01c5ac25465e5fd5797a419f2861b`.
The verdict applies to those exact bytes; later corrections should identify
their own source hash or retain this review as the earlier snapshot. The first
reviewed draft had SHA-256
`00446bcfa87be3cf28d2be165fa5250f87b954eb8713b284da333d0b3260d3e7`;
only the title, review status, and the two clarifications below changed.

## Derivation check

With `U(t)=exp(-itH)`, Heisenberg differentiation gives
`d'(t)=i Tr(U(t)^dagger[H,Otilde]U(t) Delta)`.
Consequently the sign of `a=i Tr([H,Otilde]Delta)` is correct and the second
derivative is `-Tr(U(t)^dagger[H,[H,Otilde]]U(t)Delta)`.
The operator `i[H,Otilde]` is Hermitian; the trace of its product with Hermitian
Delta is real by cyclicity. Thus a is real without requiring commutation.

The equal carrier marginal gives d(0)=0. Trace duality and unitary invariance
give the global bound `|d''(s)|<=b M`. Taylor's remainder can be written as
`t^2 integral_0^1 (1-u)d''(ut) du`, which proves the stated `t^2 b M/2`
bound for either sign of real t. Reverse triangle inequality then yields the
nonnegative witness lower bound after clipping at zero.

The reduced difference X is Hermitian and traceless. Subtracting the midpoint
of O's spectrum leaves norm w/2 and does not change its pairing with X. Hence
`|Tr(OX)| <= (w/2)||X||_1 = w D_C`. The denominator is **w**, not 2w.
It is legitimate even when the carrier dimension changes, provided the stated
spectral diameter is positive. Delta is a difference of normalized states, so
`M<=2` is correct; when M=0 the entire bound is trivially zero.

For the family, `b_L M_L<=B` and `|a_L|>=a0` give
`|t|a0-t^2B/2 >= |t|a0/2` whenever `0<|t|<=a0/B`.
The denominator bound `0<w_L<=W` then proves
`D_C,L(t)>=|t|a0/(2W)` for every admitted L. No interchange of a time derivative
with an infinite-size limit is used. The time is fixed independently of L.

Common output-unitary invariance is correct. If the carrier state is conjugated
by V, the corresponding same-value witness is `V O V^dagger`. A general noisy
channel can erase the response; contractivity supplies an upper bound, not
preservation of this lower bound.

## Exact sign and normalization witness

Take S and C to be qubits, set `0<epsilon<=1`, and let X, Y, Z be Pauli matrices:

```text
rho   = (I_4 + epsilon Z_S tensor Y_C)/4,
sigma = I_4/4,
H     = g Z_S tensor X_C,             g real,
O     = Z_C.
```

Both states are positive with unit trace and have equal S and C marginals.
Sigma is exactly the product of rho's separate marginals. Direct Pauli algebra
gives

```text
M = epsilon,             w = 2,
a = 2 g epsilon,         b = 4 g^2,
d(t) = epsilon sin(2 g t),
Tr_S[U Delta U^dagger] = (epsilon/2) sin(2 g t) Z_C,
D_C(t) = (epsilon/2) |sin(2 g t)|.
```

This independently confirms the derivative sign, negative-time absolute value,
trace-distance factor 1/2, and saturation `|d(t)|=w D_C(t)` of the observable
duality step. It is an exact illustrative construction, not an UNT calculation.

## Applied wording refinements and application ceiling

1. The title and corollary now specify **size-uniform response at a fixed short time**.
   It does not imply a signal persists for long times; the two-qubit example
   repeatedly returns to zero. Conditional uniform lower bounds imply a scalar
   liminf bound along admitted sizes, but do not construct or prove existence of
   a thermodynamic-limit state or dynamics.
2. If the second derivative is identically zero for every real time in this
   finite-dimensional unitary setting, d is linear and globally bounded, hence
   a=0. In particular, `b M=0` cannot furnish a nonzero linear response. The
   revised draft explicitly identifies this degenerate case; it is not an
   additional route satisfying a0>0.

The original application caveats are warranted: a discrete UNT admission map
needs a justified Hamiltonian interpolation on the actual common state space;
one L4 response does not imply a nonzero derivative at the chosen origin;
uniform a0 and B must be earned for the specified family; and neither this
lemma nor an illustrative two-qubit witness supplies native geometry, a
continuum, gravity, or the numerical value of a physical constant.

No material mathematical defect was found. Only the authorized unsealed draft
received the two wording clarifications and review status; no historical sealed
theorem was changed. The central inequalities and their proof are unchanged.
