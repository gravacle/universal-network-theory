# Connected fourth-order graph response and its native size bound

2026-09-27. Exact coefficient calculation, independently checked algebraically
by the root and record-response agent. No numerical worker, new interaction,
parameter adoption, preparation or geometric identification. The resident
regular-graph virtual-response and uniform-degree bounds supply the common
native sector; no dataless source was opened.

**Result.** Disconnected two-edge contributions cancel from the canonical
fourth-order operator. After retaining but separating a scalar depending only
on record counts, the remaining diagonal and graph-switching operator has
norm O(Omega^4/N^2) at fixed preferred degree. This is smaller than the largest
second-order arrangement contrast O(Omega^2/N). It improves the finite-order
comparison, but does not bound every higher order of the native Hamiltonian.

## 1. Fix the effective-operator convention

Keep the complete fixed-record, carrier-free BS Hamiltonian H=H0+V,
V=-h sum_e X_e, h=Omega/N. All d0-regular graphs span P with common energy
Ecl. Assume the previous strict common-degree condition

    c=Delta+4U(d0-d_*),
    g=U-max(|c/2|,|c/2-lambda|)>0,       gamma=2g.          (1)

Then Q=1-P has H0-Ecl>=gamma. Storage, spectator constants and the native
extensive margin remain retained. Define the positive reduced resolvent
R=Q(H0-Ecl)^(-1)Q and S_j=P V R^j V P. In the canonical Hermitian convention
obtained by normalizing the Feshbach P component, without a subsequent
arbitrary unitary rotation inside P,

    H2=-S_1,
    H4=-P V R V R V R V P + (S_2 S_1+S_1 S_2)/2.         (2)

The normalization term matters. To this order the energy-dependent equation
is e(I+S_2)psi=(-S_1-PVRVRVRVP)psi. Multiplying on both sides by
(I+S_2)^(-1/2) gives (2). Odd coefficients vanish by link-number parity.
The formulas are exact Taylor coefficients at fixed N. A finite truncation
still needs an appropriate weak-coupling domain and remainder control.

Both S_1 and S_2 are diagonal in the graph basis: two distinct flips cannot
restore every target degree. For a graph G write

    s_e=1-2n_e(G),    delta_e=c-lambda(q_u+q_v),
    a_e=2U+s_e delta_e >= gamma.                          (3)

For distinct edges e,f, the two-flip energy is

    a_ef=a_e+a_f+J_ef,
    J_ef=2U s_e s_f if e,f share a vertex, and 0 otherwise.

Every realized intermediate state has energy at least gamma above Ecl.

## 2. Exact diagonal cancellation

For an unordered edge pair e,f the four irreducible return paths are
effe, efef, feef, fefe. Their contribution to the first term of H4 is

    -h^4 (1/a_e+1/a_f)^2/a_ef.

The normalization term contributes
h^4(a_e+a_f)/(a_e^2 a_f^2). Combining them, and retaining the one-edge
self term from normalization, gives

    (H4)_GG=h^4 sum_e a_e^(-3)
                  +h^4 sum_(e<f sharing a vertex) F(e,f),
    F(e,f)=J_ef(a_e+a_f)
                 /[a_e^2 a_f^2(a_e+a_f+J_ef)].            (4)

For disjoint edges J_ef=0, so their two contributions cancel EXACTLY,
including with inhomogeneous records. Keeping only the irreducible path
sum would incorrectly leave an extensive number of disconnected terms.

To separate the arrangement-independent scalar, evaluate the coefficient
functions in (4) with all formal signs s_e=+1. This defines

    A_ab=2U+c-lambda(a+b),        a,b in {0,1},
    F^+_(a;bc)=2U(A_ab+A_ac)
                   /[A_ab^2 A_ac^2(A_ab+A_ac+2U)].         (5)

Let n_(L,a),n_(R,a) be the two layer counts of occupation a. The resulting
scalar C4/h^4 is the sum of

    sum_(a,b) n_(L,a)n_(R,b) A_ab^(-3)

and the two star sums

    sum_a n_(L,a) [choose(n_(R,0),2) F^+_(a;00)
                   +n_(R,0)n_(R,1) F^+_(a;01)
                   +choose(n_(R,1),2) F^+_(a;11)],

plus the same expression with L,R exchanged. Thus C4 depends on record
counts and fixed native coefficients, not graph arrangement. It is a formal
coefficient baseline, NOT the energy of an empty physical graph. It remains
part of the complete effective energy. Its leading size can be O(Omega^4/N).

Only occupied edges differ from the single-edge baseline: there are Nd0.
At a star, the number of unordered pairs touching at least one occupied
edge is choose(N,2)-choose(N-d0,2)<=Nd0. Across 2N stars there are at most
2N^2 d0 such pairs. No other diagonal term differs.

All single coefficients lie in [0,gamma^(-3)]. For J>0,
0<=F<=2/gamma^3; for J<0, -4/gamma^3<=F<=0, using the unreduced path
expression to bound denominators safely. Since 0<=F^+<=2/gamma^3,

    max_G |(H4)_GG-C4|
       <= (h^4/gamma^3)[Nd0+12N^2 d0].                  (6)

This removes the O(N^3) count of unaffected all-addition star pairs before
taking a norm. Bounding the entire diagonal first would lose that gain.

## 3. Exact graph switches and a norm bound

An off-diagonal four-flip path between regular graphs must flip four distinct
edges forming an alternating rectangle: two occupied opposite edges are
removed and the two absent opposite edges are added. The normalization term
is diagonal, so for such G,G',

    (H4)_(G'G)=-h^4 sum_(24 orders pi)
       1/[Delta_G(pi_1) Delta_G(pi_1 pi_2)
                                  Delta_G(pi_1 pi_2 pi_3)]. (7)

Here Delta_G(S)=H0(G with S flipped)-Ecl. Every one-, two-, and three-flip
intermediate lies in Q, so all 24 terms are included and positive before
the overall minus sign. Each matrix element has magnitude <=24h^4/gamma^3.

Each switch is determined by an unordered pair of occupied edges. There
are at most choose(Nd0,2)<=(Nd0)^2/2 possibilities; pairs sharing a vertex
or with occupied cross edges simply fail to produce a switch. The maximum
absolute row sum, and hence the Hermitian off-diagonal operator norm, is
at most 12Omega^4 d0^2/(gamma^3 N^2). Combining with (6),

    ||H4-C4 P|| <= Omega^4/(gamma^3 N^2)
                               [12d0+12d0^2+d0/N].       (8)

This is a bound on the entire arrangement-dependent canonical operator,
including graph mixing, not just a difference of diagonal expectations.
No selected graph or assumed locality entered the count.

## 4. Consequence for the fourth-order truncation only

The earlier result is H2=C2 P+K_N L11 with K_N=h^2 k(c,U,lambda), where
k is fixed and nonzero away from lambda=0 and c=lambda. Let L_* be the
feasible maximum L11 if K_N<0, or minimum if K_N>0. Define the nonnegative
integer deficit D_L=|L11-L_*|. For a ground state of H2+H4, the variational
principle and (8) give

    <D_L> <= 2||H4-C4P||/|K_N|=O(Omega^2),
    <D_L>/N=O(Omega^2/N).                                (9)

Markov's inequality likewise bounds Pr(D_L>=epsilon N) by O(Omega^2/N)
for fixed epsilon>0. The coefficients depend on g,d0 and nonzero k.
Thus fourth-order graph mixing does not force a macroscopic deficit from
the favored arrangement in this truncated operator. At sufficiently small
Omega it also bounds weight outside the exact extremal subspace. This is
an effective P-space statement, not an assertion about an untransformed
observable or a prepared native state.

There is a concrete physical discrimination in the balanced case. Put n1
occupied records on EACH layer, with n1>=d0 and N-n1>=d0. Separate
d0-regular occupied and blank blocks then attain L11,max=d0 n1. Degree
counting gives the exact number of mixed occupied/blank edges as
E10+E01=2(d0 n1-L11). For K_N<0, every exact extremizer therefore has
ZERO links between the two record classes, and (9) gives only O(Omega^2)
expected mixed edges in the fourth-order truncated ground state. For
nonzero fixed class fractions and d0, total incidence is instead Nd0.
This particular arrangement preference favors record/blank segregation;
it does not establish a connected, locally geometric network. The balance
and feasibility assumptions are essential, and no formation process or
full-Hamiltonian segregation theorem is implied.

Equation (8) does NOT finish the all-order problem. A generic uniform
O(Omega^6) remainder need not be smaller than the O(Omega^2/N) total
second-order contrast as N grows. Preserving a macroscopic preference in
the full native ground state needs a bound on the NONCONSTANT higher-order
remainder that is o(1/N), or another direct comparison. Exact extremal
subspace selection concerns still smaller single-step gaps O(Omega^2/N^2).
Disconnected cancellation at fourth order alone is not that theorem.

## 5. Exact algebraic fixtures for independent verification

These are prospective analytical fixtures, not adopted parameter changes.
For N=2,d0=1,U=1,c=1,lambda=1/2, with one occupied record on each layer,
order the two matchings as (11+00) and (10+01). Then

    H2/h^2 = diag(-23/10,-13/6),
    H4/h^4 = [[-317/600, -832/225],
              [-832/225, -689/1080]].                    (10)

The off-diagonal positive path sum is
2/3+2/15+18/25+98/45=832/225. At the simpler uniform-detuning fixture
c=lambda=0 with the same U,N,d0,

    H2/h^2=-2 I,
    H4/h^4=[[-1/2,-5/2],[-5/2,-1/2]].                    (11)

The formulas retain the original microscopic feedback and edge flips.
Their outcome is a controlled finite-order relational arrangement response;
it supplies neither three-dimensional space, cooling, physical attraction
nor a universal gravitational coupling.
