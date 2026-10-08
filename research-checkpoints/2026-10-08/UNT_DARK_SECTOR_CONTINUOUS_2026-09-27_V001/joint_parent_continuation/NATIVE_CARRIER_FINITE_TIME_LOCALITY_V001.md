# A finite-time native carrier locality bound

2026-09-29. New analytical result, no numerical worker or parameter fit.
The sector is the same declared one-carrier, blank-register, copying-off held
Hamiltonian as `NATIVE_CARRIER_RULER_PATHWAY_V001.md` (SHA-256
`4277871cd49f7e45169f3fd7db0b5d49b9b66651f6b4ac257d794a5230254db8`).
The selected-bit parity and Gram-sum arguments below were independently
checked by the analytical peer before this note was saved.

## Result

For an incidence graph initially in a definite basis configuration G, native
carrier transport approaches transport on G at every fixed finite clock time
as N increases, even though the incidence state itself may undergo order-one
global changes. The comparison evolves the incidence state under its FULL
Hamiltonian; it freezes only the carrier's reference graph. This distinction
avoids the non-improving whole-graph leakage bound.

Let c=|lambda_J|+|t_hop|, k=|Omega|/(N hbar), and define

    E_N(T) = (c/hbar) integral_0^T
             sqrt[N sinh²(ks)+N² sinh⁴(ks)] ds.                 (1)

Then the reduced-carrier trace distance, with the convention one-half trace
norm, satisfies

    D(rho_carrier(T), rho_frozen_G(T)) <= min(1,E_N(T)).         (2)

In particular every carrier-projector probability differs by at most the
right side. A convenient explicit upper bound on (1) is

    (c/hbar){sqrt(N)[cosh(kT)-1]/k
                 +N[sinh(2kT)/(4k)-T/2]} .                    (3)

Take the zero-Omega limit by continuity. At fixed T and fixed couplings,
(3) has expansion

    c|Omega|T²/(2 hbar² sqrt(N))
                +c Omega² T³/(3 hbar³ N)+O(N^(-5/2)).          (4)

Thus (2) improves as O(N^(-1/2)); this is a proved upper bound, not an assertion
that the actual leading error must have that scaling. It also supplies a
sufficient growing window T=o(N^(1/4)) at fixed coefficients. It does not
control arbitrary long times or prove relativistic causality.

## 1. Exact comparison Hamiltonian

On the complete bipartite incidence register and one-carrier space, write

    H_inc = F({n_e}) - h_N sum_e X_e,     h_N=Omega/N,
    V_e = lambda_J(P_u+P_v)-t_hop T_uv,
    H = H_inc + epsilon_psi I + sum_e n_e V_e,
    H_0 = H_inc + epsilon_psi I + sum_e n_e(G) V_e.             (5)

F is the original diagonal incidence energy, including the complete degree
penalty. No small operator norm for F is assumed. The exact current-square
identity in this sector is `J_uv²=P_u+P_v`, so (5) retains the native degree
onsite contribution and not merely its mean. Additional copying, creation,
incidence-changing carrier ports, or populated registers are not included.

For the product initial state `|G> tensor |chi>`, reference evolution factorizes:

    U_0(s)|G,chi> = |phi_G(s)> tensor |chi_G(s)> ,

where phi_G follows H_inc and chi_G follows the exact frozen carrier
Hamiltonian. All far incidence flips and their diagonal interactions remain
in phi_G. The actual evolved state under H can be entangled; no factorization
assumption is imposed on it. The factorized state is used only inside the
exact Duhamel comparison.

## 2. Selected-bit change bound without an extensive norm

Choose k_s specified incidence bits. Put only those k_s flip terms into the
interaction-picture perturbation; the remaining H_inc commutes with all the
selected n_e. Each transformed selected flip has norm one and flips exactly
its selected bit. To finish with every selected bit opposite to its initial
value, its number of insertions must be odd.

Bounding each ordered Dyson contribution by its norm and summing the odd
counts gives

    ||P(all k_s specified bits changed) phi_G(s)||
                         <= sinh(|h_N|s/hbar)^(k_s).           (6)

This follows from the multinomial series: after the ordered-time factor
s^m/m!, summing all sequences with odd counts m_1,...,m_k leaves the product
of k_s sinh series. No bound on F or on the other N²-k_s flip terms enters.

Let Delta n_e=n_e-n_e(G), and q=sinh(ks). The eigenvalue of Delta n_e is
zero or a fixed sign times the projector onto that changed bit. Therefore

    <(Delta n_e)²> <= q²,
    |<Delta n_e Delta n_f>| <= q⁴       (e != f).              (7)

These bounds apply to the reference incidence state. They do not posit
independent probabilities for different edges.

## 3. Carrier Gram bound and Duhamel estimate

For any normalized one-carrier chi,

    sum_e ||V_e chi||² <= c² N.                               (8)

Each V_e acts only on its two endpoints, with norm at most c; every vertex
belongs to N possible edges. For cross terms, use endpoint absolute sums:

    sum_(e,f) |<V_e chi,V_f chi>|
      <= sum_v [N|lambda_J||chi_v|
                       +|t_hop| sum_(w opposite v)|chi_w|]²
      <= c² N².                                               (9)

The final bound uses the norm N of the complete-bipartite adjacency matrix.
Disjoint-endpoint operators have zero inner product; correlations are not
discarded. Including diagonal pairs again in the bound (9) only weakens it.

Equations (7)-(9) give, for the exact reference product state,

    ||(H-H_0)U_0(s)|G,chi>||²
                            <= c²[N q²+N² q⁴].                (10)

Duhamel's identity and unitarity of the full H evolution then imply

    ||[U(T)-U_0(T)]|G,chi>|| <= E_N(T).                       (11)

Pure-state trace distance is at most this vector distance, and partial trace
cannot increase trace distance. This proves (2). Convexity extends the result
to any initial carrier density operator with the same definite incidence G.
An initially coherent superposition of different graphs is not covered by
this specific fixed-G preparation theorem.

Equation (3) follows from sqrt(a+b)<=sqrt(a)+sqrt(b), integrating sinh and
sinh². Its error window concerns this microscopic held clock, not a clock
calibrated to a physical metre or second. No probability claim is made from
an upper bound larger than one.

## 4. Operational locality relative to a bounded-degree reference graph

Now also take the carrier initially at vertex v_0 of G, whose maximum degree
is D_max. Let d_G(v,v_0) be graph distance in its reachable component. The
frozen diagonal `epsilon_psi+lambda_J degree_G(v)` commutes with the weight
`W=exp(mu d_G)`. For the weighted Schrödinger generator
`A=-i W H_frozen W^(-1)/hbar`, the Hermitian sum `A+A^dagger`
has norm at most

    2 |t_hop| D_max sinh(mu)/hbar,

because adjacent graph distances differ by at most one. Equivalently its
Hermitian part `(A+A^dagger)/2` has half this bound. The weighted squared
norm consequently grows no faster than the exponential of that rate. For
any mu>0 and integer d>=0,

    P_frozen[d_G >= d]
        <= min(1,exp[-2mu d
                       +2|t_hop|D_max sinh(mu)T/hbar]).       (12)

Vertices disconnected from the source have exactly zero frozen arrival; they
can be included in the outside set without extending W to infinite values.
Combining (2) and (12),

    P_native[outside radius d in G]
        <= min(1, exp[-2mu d+2|t_hop|D_max sinh(mu)T/hbar]
                        +min(1,E_N(T))).                     (13)

The frozen exponential term may be optimized over mu. When
d>|t_hop|D_max T/hbar, its stationary choice satisfies
`cosh(mu)=d hbar/(|t_hop|D_max T)`; zero time/hopping has the evident direct
limit. This is an exponential propagation bound, not a strictly vanishing
outside probability or a derived relativistic light cone.

For a family of initially bounded-degree graphs, fixed finite time, and fixed
microscopic couplings, (13) gives an N-improving operational-locality statement
even though the whole incidence graph need not stay unchanged. The degree
energy and all induced carrier/graph correlations were included in the proof.

## 5. Relation to the exact shortcut coefficient

For an initially localized carrier and an absent direct opposite-slab edge,
the unique flip-then-hop H² route gives the previously verified

    P_v(T) = Omega² t_hop² T⁴/(4N² hbar⁴) + O_N(T⁶).          (14)

Summing the T⁴ coefficients over the N-degree_G(v_0) absent opposite-slab
edges gives O(T⁴/N) at bounded degree. That coefficient alone is not a uniform
finite-time bound: ordinary three-hop frozen transfer also contributes to
those vertices at order T⁶ and can remain finite at later times. Equations
(1)-(13), rather than interchange of the Taylor and large-N limits, supply
the finite-time conclusion.

The existing N2/N3 census is not a numerical validation of a large-N limit,
and its native-versus-entire-frozen-state error is a DIFFERENT comparison:
that older control freezes the incidence state as well. Here the far graph
is free to evolve. This theorem supplies a constructive native route to
robust operational locality, not yet the physical geometry/clock dictionary,
autonomous graph preparation, or the gravitational field law.
