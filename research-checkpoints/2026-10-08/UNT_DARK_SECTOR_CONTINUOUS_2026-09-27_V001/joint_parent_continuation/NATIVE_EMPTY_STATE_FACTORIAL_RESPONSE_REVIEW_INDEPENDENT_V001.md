# Independent review: empty-state factorial response bound

2026-09-30. Source-only review by `short_path_adversarial`; no numerical
execution, model import, new state or changed coefficient. Reviewed all of
`NATIVE_EMPTY_STATE_FACTORIAL_RESPONSE_BOUND_V001.md`, SHA256
`37234c6777754497cac6b76d2e99198f94f97974a81b3b6b5c5decb5d0e024fd`.

Verdict: PASS for the stated fixed-scaling, empty-prepared, finite bipartite
parent and affine opposite-layer source. No correction is required.

## Independently checked algebra

The raising block between m and m+1 of L independent edge qubits is a
0/1 incidence matrix with column sum L-m and row sum m+1. Its spectral norm
bound sqrt[(L-m)(m+1)] is valid without symmetric-state preparation; uniform
vectors merely show saturation. Tensoring spectator registers does not
change the norm. With L=N^2 and h=Omega/N, the stated Omega sqrt(m+1)
bound follows. Sector-preserving terms can be arbitrarily correlated and
do not enter the factorial commutator.

The key Cauchy factorization is exactly
`(m)_(r-1)*sqrt(m+1)=sqrt[(m+1)_r*(m)_(r-1)]`.
Pair the first factor with v_(m+1) and the second with v_m. Their squared
sums are mu_r and at most mu_(r-1), respectively. Thus the differential
bound, its regularized square-root integration and empty-start induction
mu_r<=tau^(2r) are correct. For r beyond the register size the left side
vanishes; no unphysical occupation tail is asserted.

At a vertex the same proof has only N incident qubits and flip scale
h sqrt(N)=Omega/sqrt(N). The other flips commute with that degree. Summing
the second factorial moment over 2N vertices gives <C><=tau^4/N without
factorizing vertex statistics. A pair of distinct edges in a simple graph
shares at most one vertex, so C<=binom(M,2) is the correct pointwise bound.

I independently expanded the falling-factorial polynomial:

    [(M)_2]^3=(M)_6+12(M)_5+38(M)_4+32(M)_3+4(M)_2.

Its ordinary-power expansion is M^6-3M^5+3M^4-M^3, as required.
The nonnegative coefficients permit insertion of the moment bounds.
Cauchy--Schwarz applied as <C^2><=sqrt(<C><C^3>) gives exactly

    W_T<=sqrt(2) U^2 tau^2 sqrt[Q(tau^2)/N].

The subsequent chi coefficient 2sqrt(2)U^2/(hbar sqrt(N)) is correct.
Q has nonnegative coefficients and is monotone for nonnegative arguments,
so its endpoint value bounds the full fixed-age triangle. The note correctly
does not mistake that endpoint bound for the identically zero equal-time
commutator.

## Scope, source work and limits

For the PLUS source the response sign is minus chi. The unforced source mean
vanishes by layer exchange, the affine source has no quadratic contact, and
the stated |W^(2)|<=K_N||dot f||_1||f||_1 follows directly. It is a magnitude
bound, not a positivity theorem. My separate two-time/work derivation finds
a signed short-window quadratic form; there is no conflict with this bound.

For fixed U,Omega and any fixed native-age window, the bound genuinely
controls the full parent, not merely a matching projection or a fixed-order
series, and tends to zero at least as N^(-1/2). N-dependent age, amplitude,
source shape, U or physical ruler/volume requires explicit rescaling; an
infinite-age/static limit has not been exchanged with N. Empty preparation
is indispensable. Arbitrary incidence-changing ports or a different source
operator are not covered. Restoring sector-preserving record couplings can
preserve the moment inequalities without preserving the held model's source
dictionary or exchange symmetry; the note retains that distinction.

This is a conditional analytical result, not a derived astronomical clock,
native passive formation law, observational exclusion, or global failure of
UNT. No physical-promotion flag or outstanding program lane changes.
