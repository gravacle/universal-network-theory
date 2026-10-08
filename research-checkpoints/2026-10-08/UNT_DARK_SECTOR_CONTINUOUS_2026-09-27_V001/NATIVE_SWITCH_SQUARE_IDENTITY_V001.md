# Native switch degree and square correlations

2026-09-27. Exact finite combinatorial identity, with a conditional application
to the already-derived fourth-order graph Hamiltonian. No numerical run.

The [degree-manifold derivation](NATIVE_DEGREE_MANIFOLD_CORRELATION_SELECTION_V001.md)
obtained a switch-adjacency term `-k A_switch`, where `k=5h^4/(2U^3)>0`,
from four original microscopic link flips. It added no loop interaction.
The identity here makes the correlation dependence of that term explicit.
It is not a physical geometry, a new coupling or a large-N phase proof.

## 1. An exact count for every regular graph

Take any simple labeled bipartite graph with N vertices in each layer and
degree d at every vertex. For each distinct pair i,j of left-layer vertices,
let c_ij be their number of common right-layer neighbors. A two-edge switch
between these rows must choose one neighbor exclusive to i and one exclusive
to j. There are exactly `(d-c_ij)^2` choices. Each choice produces one
distinct new labeled graph; different row pairs cannot produce the same
switched graph. Therefore its degree in the configuration-space switch graph is

    r(G) = sum_(i<j) (d-c_ij)^2.

Counting each right vertex's pairs of left neighbors gives

    sum_(i<j) c_ij = N d(d-1)/2.

Every four-edge square has exactly one left pair and two common neighbors, so

    C4(G) = sum_(i<j) choose(c_ij,2).

Using `c^2=c+2 choose(c,2)` yields the exact identity

    r(G) = R0 + 2 C4(G),
    R0 = choose(N,2)d^2 - (2d-1)N d(d-1)/2
       = (Nd/2)[(N+2)d-2d^2-1].

R0 alone need not be positive. The complete r(G) is a nonnegative integer.
For N=4,d=2, R0=12: the eight-cycle has 12 switches and two four-cycles
have 16. For d=1, C4=0 and R0=N(N-1)/2, the familiar count obtained by
exchanging the destinations of any pair of matched edges. For d=N, the
constant and `2C4` cancel, as they must for the single complete graph.

## 2. An inseparable effective loop contribution

On the Hilbert space of labeled regular graphs, write

    D_switch = diag(r(G)),
    L_switch = D_switch - A_switch,
    C4_hat = diag(C4(G)).

The exact matrix identity is

    -k A_switch = k L_switch - 2k C4_hat - k R0 I.

Consequently the derived effective Hamiltonian can equally be written

    H_eff = [C - N^2 h^2/(2U) + D4 - k R0] I
            + k L_switch - 2k C4_hat + O_N(h^6/U^5),

where C and D4 retain their original complete-energy meanings. The asymptotic
remainder is fixed-N and carries no new uniform large-N control.

This shows where an effective square-count contribution comes from without
postulating a microscopic loop term. It must remain paired with `k L_switch`:
the loop coefficient and the mixing coefficient are fixed by the same native
flips. Their graph-dependent diagonals cancel in the original adjacency
representation. Dropping the Laplacian, tuning the two coefficients separately,
or treating the square term as an independently measured microscopic energy
would change the model.

For normalized amplitudes psi on configuration space,

    <psi|-k A_switch|psi>
      = k sum_{unordered switch-neighbor pairs G,H}|psi_G-psi_H|^2
        -2k <C4_hat> -k R0.

Correlation selection therefore trades amplitude variation across accessible
graphs against their square counts. Merely maximizing C4 is not the ground-
state problem. The identity neither proves that a local macroscopic geometry
forms nor that fragmentation is universally favored. Here L_switch connects
whole graph configurations; it is not the BS16 vertex Laplacian or a spacetime
operator. Its dimensions count transitions in state space, not physical length.

## Scientific consequence

The native degree penalty and single-link flips already contain a constrained
effective correlation mechanism. A subsequent locality or scaling calculation
must test that mechanism as a whole, with its preparation and finite-N control,
rather than insert a freely adjustable loop energy to obtain the desired phase.
Nothing here supplies physical volume, stress, dark abundance or an attractor.
