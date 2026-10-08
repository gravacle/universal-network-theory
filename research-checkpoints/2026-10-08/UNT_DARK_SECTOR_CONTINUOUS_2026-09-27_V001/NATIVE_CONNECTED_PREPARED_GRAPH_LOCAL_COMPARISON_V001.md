# Connected prepared graphs: a controlled local-readout limit

2026-09-27. Exact analytical continuation of
`NATIVE_PREPARED_GRAPH_PERSISTENCE_AND_TRANSFER_V001.md`, read after its
resident flag check. The recovered BS microscopic source was already read
in full and its resident status rechecked. No numerical calculation,
formation protocol, fixed-incidence intervention, or physical metric is
introduced.

**Result.** The earlier O(1/N) local-readout comparison for a disconnected
matching extends to EVERY prepared graph of bounded maximum degree,
including connected graphs. Arbitrary onsite formation can remain active.
A sharper one-carrier bound also gives explicit nonvanishing transfer on
a prepared connected cycle while every native incidence flip remains active.

## 1. Native full evolution and the distinct comparison

Take one K_(N,N) slab with initial state |G〉〈G| tensor rho_m, where
rho_m is any nongraph state, including a mixed or spatially entangled one.
G is a specified computational-basis graph, with maximum degree z. Use

    H(s)=H_diag,graph(s)−(Omega/N)sum_e X_e
             +sum_v h_v(s)+sum_all_possible_e n_e B_e(s).       (1)

The first term is graph-only and diagonal in every n_e. Each h_v acts only
on the nongraph factors at vertex v; arbitrary onsite native copying and
time-dependent formation schedules are allowed. B_e acts only on its two
endpoint nongraph factors, with uniform norm bound ||B_e(s)||<=b. For the
source's fixed coefficients one may take

    b=|t_hop|+lambda_J+2lambda_R.

Propagators must exist, for example for piecewise-continuous finite-dimensional
coefficients. Nonlocal nongraph ports and additional incidence-changing
controls are outside (1).

The frozen comparison is

    H_G(s)=sum_v h_v(s)+sum_{e in G} B_e(s).                    (2)

It acts on nongraph factors only and is not substituted into the full
dynamics. For a readout A supported on a fixed vertex set X, write
A_G(T,s)=U_G(T,s)† A U_G(T,s). The predecessor proves the exact identity

    <A>_full(T)−<A>_G(T)
       =(i/hbar)int_0^T ds sum_e
         <(n_e−g_e)[B_e(s),A_G(T,s)]>_full,s.                  (3)

For Q_e the wrong-bit projector relative to G, its unconditional population
satisfies y_e(s)<=Omega²s²/(N²hbar²). Since Q_e commutes with the nongraph
commutator, each summand's magnitude is bounded by
y_e(s)||[B_e(s),A_G(T,s)]||. This uses positivity, not factorization of
the evolved joint state.

## 2. A finite-operator propagation bound derived on G

For each vertex let E_v be normalized partial trace over that vertex,
followed by tensoring its identity. Define

    delta_v(O)=||O−E_v O||,      D(O)=sum_v delta_v(O).

These conditional expectations commute and contract operator norm. For an
endpoint operator B_uv,

    ||[B_uv,O]|| <=2b[delta_u(O)+delta_v(O)].                  (4)

Indeed E_u E_v O commutes with B_uv, and
O−E_u E_v O=(O−E_u O)+E_u(O−E_v O).

Remove all onsite h_v by their product interaction picture. They can have
arbitrary strengths: this picture preserves supports, B_e norms, and
delta_v. For the remaining graph evolution, split the generator into edges
not incident on v and its incident edges. The first part evolves
O−E_v O unitarily. Duhamel's identity and ||I−E_v||<=2 give

    delta_v(tau) <=delta_v(0)
        +(4b/hbar)int_0^tau du sum_{w adjacent_G v}
                                      [delta_v(u)+delta_w(u)]. (5)

This also holds for the backward comparison evolution from T to s.
Summing and using max degree z yields

    D(A_G(T,s)) <=2|X| ||A|| exp[v(T−s)],
    v=8bz/hbar.                                               (6)

The initial factor follows from delta_v(A)=0 outside X and
delta_v(A)<=2||A|| inside X. This is a direct graph-operator estimate.
One may retain the matrix exponential of (4b/hbar)(degree matrix+adjacency)
in (5) for a sharper walk-dependent bound. Neither estimate assumes a
spacetime cone, dimension, or physical length for a graph edge.

Every vertex belongs to exactly N possible edges of the full bipartite
slab, whether or not those edges lie in G. Thus (4) and (6) imply

    sum_all_possible_e ||[B_e(s),A_G(T,s)]||
        <=4b N |X| ||A|| exp[v(T−s)].                          (7)

Combining (3) and (7) proves

    |<A>_full(T)−<A>_G(T)|
       <=min{2||A||,
             4b |X| ||A|| Omega² I_v(T)/(N hbar³)},            (8)

where

    I_v(T)=int_0^T s² exp[v(T−s)]ds
          =2[exp(vT)−1−vT−(vT)²/2]/v³  (v>0),
    I_0(T)=T³/3,
    I_v(T)<=T³ exp(vT)/3.                                    (9)

The bound is O(1/N) for fixed T,z,|X| and coefficients. It is also an
explicit criterion for other time/support scalings; an unrestricted
long-time limit does not follow. For an effect 0<=A<=I, the trivial
cap 2||A|| may be replaced by one.

## 3. Sharper source-off one-carrier probability bound

Turn formation off and keep records fixed. Retain exactly one carrier of
one content; this is an invariant native sector. For a vertex readout,

    A=q_v^psi=|v〉〈v|,
    A_G(T,s)=|phi(T,s)〉〈phi(T,s)|.

The frozen carrier Hamiltonian, up to a common scalar, is

    H_car,G=lambda_J D_G−t_hop A_Graph.                        (10)

Here D_G is the degree matrix and A_Graph the adjacency matrix, not the
readout operator. Fixed-record feedback contributes only a carrier-scalar
term. On an edge the nonscalar carrier part is

    B_e,car=−t_hop(|u〉〈v|+|v〉〈u|)
                       +lambda_J(|u〉〈u|+|v〉〈v|),
    ||B_e,car||<=b_c:=|t_hop|+lambda_J.

For a Hermitian B and normalized phi,
||[B,|phi〉〈phi|]||=sqrt(<B²>_phi−<B>_phi²)<=||B phi||.
Consequently

    sum_all_possible_e ||[B_e,A_G(T,s)]||
       <=b_c N ||phi(T,s)||_1
       <=b_c N exp[v_c(T−s)],
    v_c=z|t_hop|/hbar.                                        (11)

The last step follows by removing the diagonal degree potential and
bounding the induced l1 norm of the adjacency generator by z|t_hop|/hbar.
It starts from ||phi(T,T)||_1=1. Therefore

    |Pr_full(v;T)−Pr_G(v;T)|
       <=min{1, b_c Omega² I_vc(T)/(N hbar³)}.                 (12)

The full carrier may become entangled with incidence; (12) does not discard
that entanglement or suppress its native feedback. The rank-one step is
specific to this source-off carrier sector, while (8) allows arbitrary
onsite formation and nongraph states.

## 4. Explicit connected transfer that persists as N grows

Choose G=C_(2N), the connected bipartite cycle, N>=2. Its maximum degree
is two. With one initially localized carrier at u and fixed records, all
diagonal terms in (10) are scalar, and the frozen propagator is, up to
phase, exp[i t_hop T A_Graph/hbar]. Let v neighbor u and t_hop!=0.

At T_*=hbar/(8|t_hop|), put alpha=t_hop T_*/hbar, so |alpha|=1/8.
The adjacency norm is two. The exponential remainder obeys

    ||exp(i alpha A_Graph)−I−i alpha A_Graph||
       <=sum_{k>=2}(1/4)^k/k! <=1/24.

Since (A_Graph)_(v,u)=1, the neighbor amplitude has magnitude at least
1/8−1/24=1/12, hence

    Pr_G(v;T_*)>=1/144,
    Pr_full(v;T_*)>=1/144
       −b_c Omega² exp(1/4)/(1536 |t_hop|³ N).                 (13)

This is a conservative, explicit nonzero transfer probability at a fixed
time, uniform over the growing connected cycle. All N² native incidence
flips and possible-edge couplings are present in the full model on the
left. The cycle is an owned initial condition, not a dynamically selected
phase or a graph claimed to have formed in this time interval.

Equation (8) establishes a broader local-readout limit on any prepared
connected bounded-degree graph; (13) supplies a concrete transport witness.
The clock is the microscopic Hamiltonian clock and the comparison uses
graph adjacency. No physical ruler, universal gravitational response, or
preparation/cooling process has been inferred from these bounds.
