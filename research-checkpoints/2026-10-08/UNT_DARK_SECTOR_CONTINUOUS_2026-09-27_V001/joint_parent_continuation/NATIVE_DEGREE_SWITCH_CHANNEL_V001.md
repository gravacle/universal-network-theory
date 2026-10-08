# Native degree-sector boundaries and an induced switch channel

2026-09-29. Analytical continuation of BS06/BS11; no numerical worker,
parameter adoption, fit, new loop term or alteration of frozen evidence.

**Constructive result.** The native flips DO induce degree-preserving
four-edge switches in a strict regular-degree ground manifold. Their first
nonzero matrix element, energy denominators and sign are fixed below. At a
degree boundary a different first-order collective channel appears. Neither
result puts the inherited positive-edge-cost ground state into that manifold,
or proves that the resulting graph is connected or spatially local.

## 1. Exact degree sectors, including their boundaries

Use one slab, N vertices on each side, all carriers blank, copying/ports
off, and uniform held record occupancy q=0 or1. Retain record onsite energy
E_on=2N epsilon_r q. The exact restricted parent is

    H=E_on+sum_v f(d_v)-h sum_e X_e,
    f(d)=U(d-d_*)^2+(Delta_q/2)d,
    Delta_q=Delta-2lambda_R q, h=Omega/N.                (1)

Carrier transfer/current terms annihilate the blank-carrier sector. Record
contents can be fixed arbitrarily; their occupancy is an explicit sector,
not a free preparation or an assertion of completed record formation.

Put d0=d_*-Delta_q/(4U), with U>0. A strict interior degree minimum k,
1<=k<N, occurs exactly when |k-d0|<1/2. Equivalently, writing the edge
coefficient kappa=Delta_q+2U(1-2d_*),

    -4Uk < kappa < -4U(k-1).                            (2)

There exist simple k-regular bipartite graphs, so every vertex can attain
that minimum simultaneously. Their common absolute energy is
E_k=E_on+2N f(k). Let P project onto ALL such incidence basis states, not
onto a selected connected graph. Set Q=1-P and V=-h sum_e X_e.

The energy costs of adding an empty edge and removing an occupied edge
from a regular graph are respectively

    A=2[f(k+1)-f(k)]=kappa+4Uk >0,
    B=2[f(k-1)-f(k)]=-kappa-4U(k-1)>0,
    A+B=4U.                                            (3)

At least two units of total absolute degree deviation are required to leave
P. Convexity gives the exact unperturbed gap delta0=min(A,B), attained by
a single flip. The cases k=0,N have only the allowed one-sided cost and a
unique empty/complete regular graph; they have no switch manifold.

At the boundary kappa=-4Uk, the minimizing degrees are k and k+1, not just
k. The degenerate ground space must include all graphically allowed mixtures
of those degrees. Flips that join two degree-k vertices (or undo such a join)
can remain in that ground space: PVP is then NONZERO at first order.
Using (3) with a zero denominator would be a misuse of the strict-sector
expansion, not evidence for an infinite response.

For the inherited U=d_*=1, Delta=4, lambda_R=1/2, kappa is2 for blank
records and1 for full records. Both lie in the degree-zero region. The
previous O(1)-edge passive-ground theorem therefore remains intact. For
full records the strict k=1 interval would instead be 1<lambda_R<3,
the strict k=2 interval3<lambda_R<5. Their centered values2 and4 are
OFF-INHERITED examples of the same microscopic family, not chosen physical
coefficients or repairs of the completed calculations.

These examples can lie outside BS13's simple sufficient coefficient region;
that must not be silently ignored. There is, however, a separate extensive
lower bound, already derived in the connectivity note. For nonnegative
onsite gaps, held ports/copying off, and c_psi=max(0,|t|-lambda_J), set
a=Delta-2lambda_R-c_psi-4U d_*. The complete held register family satisfies

    H >= N[2U d_*^2-Omega-max(0,-a)^2/(8U)] I.          (2a)

This follows from the edgewise carrier/current bound, record occupancy<=1,
sum_v d_v^2>=2M^2/N and completion of the square in M>=0. A fixed number
of bounded local copy terms per node adds its explicitly bounded O(N) debit
if switched on. Thus leaving the sufficient BS13 domain does not imply
unbounded energy per node. This lower bound is not a proof of a connected
phase, the projection control below, or a physical parameter adoption.

## 2. Lower-order terms cannot rewire a regular graph

Distinct simple graphs with exactly the same degrees differ on an
alternating even cycle, whose minimum length here is four. Thus

    P V P=0,
    P(sum_e X_e)^2P=N^2 P,
    ||Q V P||=hN=Omega.                                 (4)

There is no two-flip off-diagonal transition within P: the only two-flip
return is to flip the same edge twice. The second-order effective energy is
the common scalar

    E^(2)=-h^2[kN/B+(N^2-kN)/A].                        (5)

It is independent of topology. Odd orders within P vanish by incidence
parity. At fourth order, a diagonal return flips either one edge four times
or two distinct edges twice. Its denominators depend only on whether the
two edges share a vertex and on their occupied/empty signs. The respective
adjacent pair counts in a k-regular graph are

    occupied/occupied: 2N binom(k,2),
    empty/empty:       2N binom(N-k,2),
    mixed:             2Nk(N-k).

Disjoint counts are the fixed complements. Folded second-order terms are
also scalar by (5). Consequently the fourth-order diagonal shift is common
to the entire regular manifold. No topology-selecting diagonal potential
has been silently omitted at this order.

## 3. The induced four-edge switch, with all24 paths

Consider two occupied opposite edges of a rectangle whose other two edges
are empty. The target removes the occupied edges and adds the empty ones,
preserving all degrees. The four distinct flips can occur in24 orders.
No intermediate state is in P. Write '+' for an addition and '-' for a
removal. There are four permutations of edge labels for each sign word.

    sign word      three intermediate energy costs
    ++--           A,2A,A
    --++           B,2B,B
    +-+-           A,C,A
    -+-+           B,C,B
    +--+           A,C,B
    -++-           B,C,A
    C=(A+B)/2=2U.

In a mixed two-flip intermediate the shared vertex has returned to degree
k; the two other vertices have opposite unit deviations, giving cost C.
Each flip matrix element is -h; three resolvents (E_k-H0)^-1 give the
negative sign. The leading off-diagonal effective element is exactly

    <G'|H_eff|G>=-g4+O_N(h^6),
    g4=h^4 S(A,B),
    S=2/A^3+2/B^3+(4/C)(1/A+1/B)^2
     =2(A+B)(A^2+3AB+B^2)/(A^3 B^3)>0.                 (6)

The folded fourth-order terms cannot alter this off-diagonal element,
because lower-order off-diagonal elements vanish. At a centered minimum,
A=B=2U and g4=5h^4/(2U^3). This is a microscopically generated switch term,
not an added loop operator or a declaration that the rectangle is a
geometrical plaquette. The possible arrows still form the complete
bipartite set and carry no native distance.

## 4. What is actually controlled as N changes

For each fixed finite N, ordinary isolated-subspace perturbation theory is
controlled at sufficiently small h. A conservative sufficient condition is

    2||V||=2hN^2=2Omega N < delta0.                     (7)

It is deliberately sufficient, not necessary. Together with the exact
resolvent expansion it controls the order statement in (6). The symbol
O_N does not hide a claim of an N-uniform remainder. Fixed microscopic
Omega and h=Omega/N do NOT satisfy (7) for arbitrarily large N. Failure
of this bound also does not establish a physical breakdown: the true
off-block norm in (4) is only Omega, not Omega N.

A sharper exact target is available. For the full interacting Q block,

    H_eff(E)=E_k P+P V Q(E-QHQ)^-1 Q V P.               (8)

If its actual denominator distance is g_Q>0, the eliminated component of
an eigenstate obeys ||Q psi||<=Omega ||P psi||/g_Q and the self-energy
norm is at most Omega^2/g_Q. Establishing a uniform g_Q and controlling the
linked higher-order terms would justify an N-uniform slow-sector theory;
counting a small flip coefficient alone does not establish either fact.

At the formal fourth-order level, fixed k,A,B,Omega give an individual
switch element O(N^-4). Each graph has at most binom(N,2)k^2 switches,
so the switch-operator bandwidth/norm is O(N^-2), after subtracting common
energy shifts. This identifies a candidate slow collective channel. It is
not yet a proved long-time approximation to the full fixed-Omega parent,
and it supplies no clock conversion into physical seconds.

## 5. Rearrangement versus connected geometry

For k=1, the manifold is all perfect matchings. A switch exchanges the
partners of any two left vertices. Every configuration has binom(N,2)
neighbors. The leading effective ground vector is the uniform superposition
of matchings: the switch graph is connected by such transpositions and its
constant row sum is its largest adjacency eigenvalue. All measured graphs
remain disjoint pairs for N>1.

There is a directly calculable collective spectral scale. For any numbers
x_j with sum_j x_j=0, the configuration function x_(pi(1)), where pi is a
matching permutation, is an eigenfunction of the transposition Laplacian
with eigenvalue N. Hence the leading switch Hamiltonian has a nontrivial
excitation at g4 N=O(N^-3) above that uniform vector. This is an explicit
mode, not an assertion that every omitted spectral scale has been bounded.
Coherent rearrangement of matchings does not itself create a connected
instantaneous carrier geometry.

For k=2, switches can merge two cycles or split a cycle. The native kinetic
term therefore really can change topology inside a fixed-degree sector;
there is no invariant restriction to the originally prepared component
count. It does not automatically favor a single long cycle. Let c_ij be the
number of common right neighbors of left vertices i,j, and let C4(G) count
four-cycles. The exact number of legal switches is

    F(G)=sum_(i<j)(k-c_ij)^2
        =Nk[Nk-2k^2+2k-1]/2+2 C4(G).                  (9)

This follows from sum c_ij=N binom(k,2) and
sum c_ij^2=N binom(k,2)+2C4. For instance k=2,N=4 gives12 switches for
an eight-cycle and16 for two separate four-cycles. Row count alone does not
prove ground-state concentration, but it demonstrates why a kinetic
selection calculation must retain disconnected configurations. No positive
dimension, metric locality or gravitational equation follows from a degree
constraint or its induced switch term.

## 6. A different exact collective channel at the first boundary

At kappa=0 the unperturbed degree-zero/one ground space is ALL matchings,
including the empty one. Let |m> be the normalized uniform superposition
of m-edge matchings. Its number of configurations is
N!^2/[m!(N-m)!^2]. An m-matching allows (N-m)^2 additions and an
(m+1)-matching has m+1 removals. The first-order projected Hamiltonian has
the exact bright matrix element

    <m+1|PVP|m>=-h(N-m)sqrt(m+1)
                =-Omega(1-m/N)sqrt(m+1), 0<=m<N.       (10)

Independent left/right relabelings act transitively at each m, so these
uniform states form an exactly invariant subspace of the projected operator.
The diagonal is the common full unperturbed energy; a diagnostic -fM adds
-fm. Equation(10) is a finite-capacity native collective channel. For m<<N
its ladder resembles a linearly driven oscillator, but at the boundary
there is no derived positive harmonic restoring frequency, no positive
quartic pressure law, and no right to discard saturation or the eliminated
degree-two states. For N>=2 the gap to that excluded space is2U before flips; 
for N=1 there is no excluded degree-two sector. In the N>=2 cases,
the same finite-N projection-control obligation remains. Every basis graph
in this manifold is still a matching. This is a distinct critical regime,
not a continuation of (6) through zero denominators.

## 7. The discriminating next calculation, if needed

The theorem itself needs no numerical run. Its smallest implementation
check is N=2 at a DECLARED centered k=1 parameter (for example full records,
lambda_R=2, otherwise inherited), with weak flip controls chosen before
output. Compare the two matching-state splitting to2g4, retaining the full
sixteen-state spectrum and leakage. This would test the derived operator,
not qualify the inherited lambda_R=1/2 ground state as connected.

A more geometrically informative small next question is the leading k=2,
N=4 switch matrix, enumerated only on exact regular graphs. Its basis can
be generated from at most binom(4,2)^4=1296 row patterns before enforcing
column sums; there is no need to propagate the full2^16 incidence space.
Retain every component topology and compare its complete kinetic spectrum,
not a selected connected graph. Such a calculation is conditional on the
controlled strong-degree limit, and cannot replace the full-Q denominator
test needed at fixed microscopic coefficients and growing N.

The substantive path forward is thus precise: native degree feedback can
create a constrained manifold, native flips generate its switch dynamics,
and its complete operational connectivity/ruler behavior can be tested.
The actual inherited positive-cost passive branch supplies neither that
manifold nor its preparation. Excited regular states cannot automatically
reuse the ground-manifold proof: for example at inherited kappa=2,N>=3,
replacing three disjoint matched edges by two adjacent edges preserves the
diagonal energy while leaving regularity. At kappa=1,N>=4 the same occurs
by replacing four matching edges by two adjacent edges. These exact
resonances must be retained in an excited-sector reduction; their presence
does not by itself assert a nonzero lowest-order transition or decay rate.

## Resident source identities

* `../recovered_sources/BS_MICRO_ACTION.md`:
  `00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec`.
* `NATIVE_RECORD_CONNECTIVITY_PATHWAY_V001.md`:
  `81bbb3b72e00c03475b8efcc63c861907adb8b0da72bd50f27c89a6bc0b6775c`.
* `NATIVE_VOLUME_INCREMENT_PATHWAY.md`:
  `c60b04d6584bf12b7db9ce5b52815c0010aeb13fe0a2a86324cbedd929cf4c6a`.

All energies, source costs and parameter changes remain explicit. This is
an effective channel derived from the stated native family, not a fitted
dark component or a new microscopic topology term.
