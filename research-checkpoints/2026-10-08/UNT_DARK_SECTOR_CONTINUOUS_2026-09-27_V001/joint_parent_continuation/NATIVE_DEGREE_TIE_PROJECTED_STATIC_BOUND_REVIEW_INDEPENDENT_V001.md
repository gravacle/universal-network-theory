# Independent review: complete projected source-sector static bound

2026-09-30; `short_path_adversarial`. Independent hand derivation and complete
source-only reading of `NATIVE_DEGREE_TIE_PROJECTED_STATIC_BOUND_V001.md`, SHA
`57530e06b99ad9608dc8afde899804884947402eafb7d7860813b875ac1887de`.
No diagonalization, numerical worker, import, source modification or ledger edit.

**Verdict: PASS, with no correction requested.** The result controls every
ground-to-excited transition of the declared node-energy source inside exact
PHP. It bounds a source-visible gap, not necessarily the global first gap.

## Independent source-exhaustion and block derivation

At fixed m, right permutations identify a normalized basis indexed by occupied
left m-subsets A. Each subset has N!/(N-m)! injection configurations. Between
A and A plus one left vertex, the corresponding normalized S matrix element
is sqrt(N-m). Thus the right-trivial dynamics is a weighted Boolean-subset
raising/lowering operator, without choosing a graph geometry.

For any real vector x_i with sum x_i=0, use F_m(A)=sum_(i in A)x_i. Elementary
subset counting gives

    sum_(|A|=m) F_m(A)^2 = binom(N-2,m-1) sum_i x_i^2,
    sum_(i in B) F_m(B minus i) = m F_(m+1)(B).

The squared adjacent norm ratio is (N-m-1)/m in this normalized subset basis.
Multiplying by its raising coefficient produces exactly

    b_m = sqrt[m(N-m)(N-m-1)],  1<=m<=N-2.

This independent derivation agrees with the note's unnormalized full-graph
basis, where the injection-count factor is included in the norm. The m=0,N
standard states vanish. Repeating by exchanging layers gives the identical
other block, orthogonal under the independent layer-permutation action.

Crucially, source completeness does not depend on merely guessing these blocks
or measuring a radial gap. In a size-m graph, a matched anchor has one deletion
and no addition, whereas an unmatched anchor has N-m possible additions.
Subtracting the S/N component from the node star gives the exact source amplitude

    -(h/2)[phi_(m-1)-(N-m)phi_(m+1)](1_anchor_matched-m/N).

It lies in the explicitly closed span just derived. Uniform total energy is
ground-parallel and opposite constant layer sources vanish on P. Every real
node profile decomposes into those two dark singlets and the two reached
standard sectors; no additional representation enters its spectral measure.
The multiplicity argument in the note is consistent, but the explicit closed
span and source amplitude already suffice for the bound.

## Gap and susceptibility constants

The positive Perron ground of the complete matching flip graph is in the
uniform-m singlet block, with a_m=(N-m)sqrt(m+1) and largest eigenvalue lambda0.
On every standard interior link,

    (b_m/a_m)^2 = 1 - N/[(m+1)(N-m)]
                <= [(N-1)/(N+1)]^2.

Padding the standard block with zero endpoint rows/columns permits entrywise
nonnegative-matrix comparison with the singlet block. Hence rho(A1) is at most
((N-1)/(N+1))*lambda0 and every source-visible energy gap obeys

    Delta >= 2h*lambda0/(N+1).

For N=2, A1 is simply [0], so the statement also covers the empty interior-link
case. A two-adjacent-level Rayleigh trial at p=floor(N/2) gives
lambda0>=a_p>=N^(3/2)/(2sqrt(2)). With the unchanged h=Omega/N this yields

    delta_N = Omega*sqrt(N)/[sqrt(2)*(N+1)].

Combining the independently reviewed projected source weight
W_u<=Omega^2*Q_u/[4(N-1)] with positivity and Delta>=delta_N gives

    chi_u(0) <= Omega*(N+1)*Q_u/[sqrt(2)*(N-1)*sqrt(N)],
    chi_anchor(0) <= Omega*(N+1)/[sqrt(2)*N^(3/2)].

All factors of two, h and the PLUS-source sign convention agree. These are
upper/lower bounds, not spectral asymptotic equalities. No eigensolver, empirical
gap assumption or fitted time/normalization was needed.

## What is newly settled and what is not

The anchored static inverse-gap exception left open by a weight-only theorem
is closed in this exact projected model: at fixed microscopic Omega and fixed
anchor normalization the static susceptibility vanishes at least as N^(-1/2).
This is not a uniform O(1) bound for arbitrary bounded extended profiles;
Q<=2N instead gives the stated O(Omega sqrt(N)) bound. It does not bound an
undamped real-frequency resonance or supply relaxation of an evolved state.

The physical source Z introduces Q_x/c^4 and any susceptibility density also
requires an independently owned V_N. For example, the same bound with extensive
volume and three-dimensional radius scaling may grow as N^(1/6), exactly as
the note states. The anchor result cannot be silently extrapolated to that
different profile. No spatial dimension or volume law is derived here.

Most importantly P is still not an invariant subspace of the full parent. The
bare 2U excluded-degree gap does not bound its interacting eliminated resolvent,
source dressing or contact corrections uniformly in N. The new exact-PHP bound
does not certify a full-parent low-energy approximation, ground-state formation,
absolute pressure, physical gravity or an observational conclusion. It identifies
what a full-parent mechanism would have to change or add under the same source
ownership; it is not a general failure theorem for UNT.

Preceding source bound reviewed at
`77a80c2c28c1eded98190f82bb3f98994d2bd24c4150ea30180263ede48c092a`;
its independent review is
`NATIVE_DEGREE_TIE_PROJECTED_SOURCE_BOUND_REVIEW_INDEPENDENT_V001.md`, SHA
`18d65e8c2bbdf616067628638e5b902f1637ef8a34d87a8451bda849e7f4047b`.
