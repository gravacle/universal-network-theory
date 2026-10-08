# Controlled dilute-addition trial above a native regular graph

2026-09-27. Exact variational upper bound, not a ground-state ansatz or
proved bosonic limit. No numerical run or added interaction. The resident
native sparse-bound and regular virtual-response notes were read; the
recovered BS source had already been read in full. The construction is in
their carrier-free, fixed-record, source-off sector with h=Omega/N.

Let G be ANY d0-regular simple bipartite graph, with fixed integer d0,
complete common diagonal energy Ecl, and binary record occupations q_v.
Set c=Delta+4U(d0-d_*), and suppose the common-degree gap condition holds:

    g=U−max(|c/2|,|c/2−lambda|)>0,   gamma=2g.

For adding an absent edge e=(u,v), write

    G_e^+=2U+c−lambda(q_u+q_v) >= gamma.

All fixed storage and spectator energies remain in Ecl.

## Exact trial and its energy

Keep every edge occupied in G in the state |1〉. Independently put each
absent edge in the ground state of G_e^+ n_e−hX_e. This product is a
variational trial only; it does not assert that the actual ground state
factorizes or that the fixed occupied edges are protected physically.
For an absent edge,

    F(G)=[G−sqrt(G²+4h²)]/2,
    p_e=[1−G_e^+/sqrt((G_e^+)²+4h²)]/2 <= h²/gamma².

Let A_v be the number of trial additions incident on vertex v. Relative
to the same complete regular energy, the native diagonal Hamiltonian on
this trial support is exactly

    Hdiag−Ecl = sum_absent G_e^+ n_e
                 +2U sum_v sum_{e<f absent at v} n_e n_f.

The occupied-edge flip expectations vanish. Independence of the absent
edges therefore gives the exact trial expectation

    Etrial−Ecl = sum_absent F(G_e^+)
                   +2U sum_v sum_{e<f absent at v} p_e p_f.       (1)

The last term is a nonnegative, explicitly retained degree-collision cost.
No physical relaxation or bosonic approximation enters (1).

## Uniform error and large-N consequence

For every G>0 and every h,

    0 <= F(G)+h²/G = 4h⁴/[G(G+sqrt(G²+4h²))²] <= h⁴/G³.

Let f_{L,a},f_{R,b} be the actual fractions of record value a,b in {0,1}
on the two layers, and G_ab^+=2U+c−lambda(a+b). There are exactly
N² f_{L,a} f_{R,b} possible edges of each endpoint type. The reference
graph occupies Nd0 edges, while each vertex has N−d0 absent edges.
Using these counts and h=Omega/N in (1) proves

    E0−Ecl <= −Omega² sum_{a,b} f_{L,a}f_{R,b}/G_ab^+
                 +Omega² d0/(gamma N)
                 +Omega⁴/(gamma³ N²)
                 +2U Omega⁴/(gamma⁴ N).                        (2)

The occupied-edge subtraction supplies the second term. The individual
qubit remainder supplies the third. The final term bounds all vertex
collisions; it follows from
2U N(N−d0)(N−d0−1)p_max² <= 2U N³ h⁴/gamma⁴.
If fewer than two edges are absent at a vertex the corresponding pair
count is zero, consistently with this bound.

Thus for fixed coefficients and convergent layer fractions,

    limsup_{N→infinity}(E0−Ecl)
       <= −Omega² sum_{a,b} f_{L,a}f_{R,b}/G_ab^+.               (3)

The trial's correction is independent of regular-graph arrangement at
leading order, with an explicit O(1/N) error. This statement holds at
fixed Omega without a weak-Omega expansion. It controls this variational
upper bound, not equality for the true energy. The trial retains expected
O(1) added edges and has O(1/N) degree-collision expectation.

A matching lower bound has NOT been established here. The true state can
include removals, coherent superpositions of regular graphs, and virtual
processes not represented by this trial. The uniform O(1) defect theorem
alone does not fix their energy. Consequently (3) supports one side of the
proposed independent-oscillator energy limit but does not prove that limit,
the state approximation, or survival/loss of the smaller arrangement
splitting. The separately verified connected fourth-order cancellation is
additional finite-order evidence, not an all-orders replacement for the
missing lower bound.
