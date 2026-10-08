# Fixed records select graph arrangements through native virtual flips

2026-09-27. Finite-size analytical result from the existing BS action; no
new interaction, numerical run, formation rule, graph geometry or adopted
parameter change. Resident balanced-record and nonempty-degree notes and the
complete recovered BS source were read. The older degree-manifold correlation
note was `compressed,dataless` and was not read or hydrated; priority over its
unavailable contents is not asserted.

**Result.** Even when every graph in a regular-degree manifold has identical
bare record feedback, virtual native edge flips can split those graphs at
second order. The splitting is proportional to the number of occupied edges
joining two occupied records, with an exactly determined coefficient. Its
sign changes with detuning. At zero bare detuning the coefficient is positive,
so the lowest second-order energy favors FEWER record-record edges. Attraction
in this arrangement sense instead occurs above the complement-centered
detuning. Neither sign is yet a physical force in a derived space.

## 1. An actually isolated regular manifold

Use one K_(N,N) slab, fixed binary record occupations q_v, no carriers,
formation or graph-dependent ports, and U>0, lambda=lambda_R>=0. Keep the
complete native energy

    H0 = epsilon_r D + sum_v [U(d_v-d_*)^2
                                +(Delta/2-lambda q_v)d_v],
    V  = -h sum_e X_e,       h=Omega/N,       D=sum_v q_v.  (1)

Nonzero spectator constants must also be retained. Let 0<=d0<=N be an integer
and P the span of all d0-regular bipartite graphs, a nonempty set. Define

    c = Delta+4U(d0-d_*),       t_q=c/2-lambda q,
    g = U-max(|c/2|,|c/2-lambda|).                         (2)

The sufficient condition g>0 makes d0 the unique individual degree minimum
for BOTH record occupations. For integer degree deviation k,

    f_q(d0+k)-f_q(d0)=U k^2+t_q k >= g |k|.              (3)

A nonregular bipartite graph has sum_v |k_v|>=2 because its left and right
degree sums must agree. Thus P is the full classical ground manifold, with
a global gap at least gamma=2g to its complement. Its common complete energy
is

    Ecl=2N U(d0-d_*)^2+Delta N d0
                              +(epsilon_r-lambda d0)D.   (4)

This gap is stronger than merely checking a particular graph's one-edge
costs. Inhomogeneous records do not invalidate it when (2) holds. If (2)
fails, this calculation cannot assume global isolation without another proof.
The sufficient BS extensive domain Delta-2lambda>=delta>0 and positive bare
storage cost remain separate requirements. Degree-zero/full manifolds have
only one graph and hence no arrangement to split.

## 2. Exact second-order effective energy

For an edge e=(u,v), put delta_e=c-lambda(q_u+q_v). Adding an absent edge
costs 2U+delta_e; removing a present edge costs 2U-delta_e. Both are positive
under (2). A single flip leaves P, so PVP=0. Two distinct flips cannot
restore every endpoint degree; therefore the second-order effective operator
has NO off-diagonal graph matrix elements. Its diagonal is exactly

    E2(G)=-h^2 sum_e [n_e/(2U-delta_e)
                                  +(1-n_e)/(2U+delta_e)]. (5)

Equivalently, write

    E2(G)=-h^2 sum_all_edges 1/(2U+delta_e)
                             +sum_occupied_edges w(delta_e),
    w(delta)=-2h^2 delta/(4U^2-delta^2).                  (6)

The first sum is independent of graph arrangement. Binary occupations give
an EXACT decomposition, not a small-lambda assumption:

    w(c-lambda(q_u+q_v))
       =w(c)+[w(c-lambda)-w(c)](q_u+q_v)+K q_u q_v,
    K=w(c-2lambda)-2w(c-lambda)+w(c).                     (7)

Regularity fixes sum_e n_e=N d0 and sum_e n_e(q_u+q_v)=d0 D. Hence

    E2(G)=C(q,N,d0)+K L11(G),
    L11(G)=sum_e n_e q_u q_v.                             (8)

All terms absorbed in C are common to the compared graphs, not subtracted
from their complete energy. L11 is invariant under simultaneous relabeling
of the graph and physical record labels. Its appearance is induced by BS06
and BS11; no microscopic record-pair interaction has been added.

## 3. The coefficient and its sign

Set a=2U and m=c-lambda. Condition (2) is equivalent to
|m|+lambda<a. Direct partial-fraction subtraction gives

    K = -4 h^2 lambda^2 m (3a^2+m^2-lambda^2)
        /{[a^2-(m-lambda)^2][a^2-m^2][a^2-(m+lambda)^2]}. (9)

All denominator factors and the parenthesis in the numerator are positive
in this domain. For h,lambda>0,

    c>lambda: K<0, favor larger L11;
    c=lambda: K=0, no second-order arrangement splitting;
    c<lambda: K>0, favor smaller L11.                    (10)

At the complement center c=lambda, the three detunings are lambda,0,-lambda
and the odd function w makes (7) affine in q_u+q_v. The cancellation is exact
at this order, not a statement that every higher-order selection vanishes.

At c=0, whose gap condition additionally requires lambda<U,

    K=12 h^2 lambda^3
          /[(4U^2-4lambda^2)(4U^2-lambda^2)]>0,
    K=3h^2 lambda^3/(4U^4)+O(h^2 lambda^5/U^6).            (11)

Thus the first genuine pair coefficient is cubic in lambda here, but its
sign disfavors occupied record-record edges. A record-rich absent edge has
a cheaper virtual addition; fixed-degree energy bookkeeping is essential
to this sign. At fixed record counts, increasing L11 also increases the
blank-blank edge count and decreases the two mixed edge counts.

An alternating four-edge switch exhibits a direct comparison: exchange the
edges (occupied,occupied)+(blank,blank) for the two mixed edges, keeping all
four degrees unchanged. The former minus latter second-order energy is K.
Whenever both graphs exist this is a strict splitting for K!=0.

There is an exact prospective compatibility witness using inherited
U=1, Delta=4, lambda=1/2, epsilon_r=1: d0=1 and d_*=7/4 give c=1,
g=1/2, positive complete leading record cost epsilon_r-lambda d0=1/2,
and K=-2h^2/15. For N=2 with one occupied record per layer the matched
11+00 perfect matching has lower second-order energy than the crossed
10+01 matching. This is an unadopted parameter-domain witness requiring
sufficiently weak h; it is NOT a claim about the existing h_2=1 mission.
The existing d_*=1 parameters instead favor degree zero and do not realize
this nonempty regular comparison.

## 4. What controls the approximation and what does not

At fixed N, V has norm v=h N^2=Omega N. The bound v<gamma/4 is a conservative
sufficient perturbative domain. There is an explicit fourth-order error
certificate, not merely a claim that every small edge amplitude is enough.
For a low ground eigenvalue E=Ecl+e, e<=0, eliminate Q=1-P:

    M(e)=-PVQ [A+QVQ-e]^-1 QVP,
    A=Q(H0-Ecl)Q >= gamma Q,
    |e|<=v^2/(gamma-v).                                  (12)

The second-order matrix is M2=-PVQ A^-1 QVP, with entries (5).
The term PVQ A^-1(QVQ)A^-1 QVP vanishes: three flips cannot connect graphs
with the same fixed occupied-edge number parity. This symmetry is the link
parity product of Z_e, not the edge-complement operation product of X_e.
Resolvent expansion then
bounds

    ||M(e)-M2||
      <= v^2 |e|/gamma^2
          +v^2(v+|e|)^2/[gamma^2(gamma-v)]
      <= 4 v^4/gamma^3 =: R4.                            (13)

For the ground, e is the smallest eigenvalue of M(e), so its distance from
min_G E2(G) is at most R4. If K!=0 and more than one L11 value is feasible,
the normalized P component has weight outside the minimizing L11 subspace
at most 2 R4/|K|. Small R4/|K| thus certifies a static preference even after
higher-order mixing. It does not project away the physical Q admixture.
The first possible off-diagonal regular-graph processes occur at four flips,
including the alternating switch above; no second-order graph hopping exists.

These are deliberately finite-N sufficient bounds. Under native h=Omega/N,
v=Omega N grows, so (13) is not a uniform large-N theorem. At fixed d0 and
bounded denominators the SECOND-ORDER arrangement splitting itself is at
most |K|N d0=O(Omega^2/N), while the all-edge constant in (6) can be
O(Omega^2). A thermodynamic competition with higher orders or entropy needs
its own controlled limit; a vanishing per-edge flip is not that proof.

The resident leading-energy notes fix degree costs and an affine bulk record
coefficient. Equation (8) resolves an additional finite-size arrangement
dependence within equal-degree states. It neither selects actual formation
history nor makes unitary dynamics a ground-state attractor. The fixed q_v
remain conserved during this source-off hold. Arrangement relative to record
occupations is not yet locality, dimension three, physical distance, an
inverse-square law or universal gravity.
