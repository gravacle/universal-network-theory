# Native carrier return resolves correlations hidden by the mean graph

2026-09-27. Exact finite-Hamiltonian theorem with one frozen, bounded
integer-arithmetic check. No metric, volume, dark density or new physical
interaction is assigned. This is a new native-restriction fixture, not a
production retry or a replacement for the actual formed-state experiments.

## 1. A short-time identity that retains quantum link flips

Restrict the original BS source-off hold to one carrier of fixed content.
Let P_u project onto its position u, with identity on all other factors.
Assume a simple graph, one possible link per pair, and that every hold term
apart from H_hop=-t_hop sum_e n_e T_e preserves each carrier position.
The original incidence flip -h_N sum X_e does preserve position and is
retained. The current-squared term is position-diagonal in this sector.
Arbitrary unspecified BS ports need not satisfy this assumption.

For any normalized complete state rho=P_u rho P_u and Q_u=I-P_u,

    Q_u H P_u=-t_hop sum_(v adjacent to u) n_uv |v><u|,
    Tr(rho H Q_u H)=t_hop^2 sum_v Tr(rho n_uv).

The second line uses orthogonal carrier destinations and the exact projector
identity n_e^2=n_e, not independent link occupations. Consequently

    1-R_u(tau)
      =(tau^2 t_hop^2/hbar^2) sum_v <n_uv>_rho + O(tau^3),
    R_u(tau)=Tr[P_u exp(-iHtau/hbar) rho exp(iHtau/hbar)].

This leading result requires neither a nondegenerate spectrum nor frozen
links. In the same conditional graph state, replacing n_uv by its mean
w_uv in a carrier Hamiltonian instead gives sum_v w_uv^2. Its error at this
order is proportional to sum_v w_uv(1-w_uv). This rejects that mean-Hamiltonian
transport substitution, not BS16's explicitly limited elliptic diagnostic.

For an initially position-entangled formed state, rho_u=P_u rho P_u is
subnormalized. A declared two-time position-read protocol keeps every
p_u=Tr(rho_u); for p_u>0 its weights are Tr(rho_u n_uv)/p_u and the gap above
is multiplied by p_u. Zero-probability branches contribute zero. This initial
measurement changes carrier coherences and can change hopping energy; its
backaction/work must be owned. It is not the unmeasured original trajectory.

## 2. Same means and energy, different native return

Use the two diagonal graph ensembles in
[the graph-correlation screen](MEAN_GRAPH_CORRELATION_GEOMETRY_SCREEN_V001.md):
uniform within-layer relabelings of C8 or two disjoint C4s on N=4+4 nodes.
Both have every vertex degree two, all mean links 1/2, and equal native
initial energy under identical fixed uniform records, onsite states and
zero ports. A retained initial carrier-position anchor is essential for a
return measurement; an untagged uniform carrier mixture alone is not that
experiment. Layer-preserving automorphisms are transitive on each layer in
both graphs, so a representative with carrier at vertex 0 gives the orbit
return without selecting a favorable graph or node.

For these diagonal preparations the two hold return functions obey

    R_two_C4(tau)-R_C8(tau)
       = t_hop^4 tau^4/(6 hbar^4) + O(tau^6)

with nonzero native link flips and the scalar-on-regular-graphs diagonal
energy specified below. The even remainder here uses the real symmetric
Hamiltonian and real diagonal preparation; it is not a generic formed-state
time-reversal assertion. This is an exact Taylor-coefficient result, not a
claim that the truncated series has measured finite-time accuracy.

Independent word-count proof through order four:

- Zero-hop contributions cancel because the remaining Hamiltonian commutes
  with P_u. Each side of the return projector needs an even number of hops
  on a bipartite graph; odd total hopping degree contributes nothing.
- With two hops and no link flips, the nonhop diagonal energy is a common
  scalar on each initial two-regular graph for every carrier position.
  Those scalar phases cannot distinguish the two ensembles.
- An odd number of link flips has zero diagonal-graph trace. With two hops
  and two flips, both flips must use the same edge. Both hops on their side
  of P_u traverse one edge out and back. Using X_f n_e X_f=n_e for f!=e and
  1-n_e for f=e reduces the graph factors to functions of a single link.
  Equal one-edge means make these contributions identical.
- Only the four-hop term distinguishes the graphs. The diagonal adjacency
  fourth moments are 6 and 8; the squared second moments agree at 4. For
  pure hopping the return fourth coefficient is (A^2_uu)^2/4+A^4_uu/12.
  Its difference is therefore (8-6)/12=1/6. Native flip terms add the same
  correction to both coefficients; they have not been switched off.

All record occupations are equal and held fixed in this theorem. It isolates
graph-correlation dependence in declared initial states, not record-history
formation, a record-arrangement intervention or a maintenance mechanism.

## 3. Frozen finite verification and resource result

[Protocol](native_geometry_moments/PROTOCOL.md) and
[source](native_geometry_moments/check_taylor.py) were hashed before the one
execution; [FROZEN.json](native_geometry_moments/FROZEN.json) is unchanged.
The exact model uses h_N=1 (Omega=4), t_hop=1, Delta=4, U_d=1, d_star=2,
lambda_R=lambda_J=epsilon_r=epsilon_psi=hbar=1, q_v=1, formation off and
zero ports. The sufficient BS extensive bound holds with delta_E=1.

The sparse basis is |graph_mask,carrier_vertex>. Its implemented diagonal is

    2*edge_count + sum_v(degree_v-2)^2 + 9 + degree_carrier.

The graph flip and hopping matrix elements are -1. No large dense matrix,
eigensolver, package, subprocess or secondary numerical worker was used.

The [result](native_geometry_moments/RESULTS.json), transcribed without changing
values from successful process stdout (exit code 0), is

| Quantity | C8 | Two C4s |
| --- | ---: | ---: |
| Initial energy in the displayed restriction | 27 | 27 |
| Four-edge square count | 0 | 2 |
| Return coefficient of tau^2 | -2 | -2 |
| Return coefficient of tau^4 | 11/6 | 2 |
| Largest sparse support | 4518 | 4440 |

The fourth difference is exactly 1/6. The hypothetical mean-adjacency model
instead gives second coefficient -1. Hermitian moment identities were also
checked by distinct inner products of the sparse powers. All calculations
used integers/Fractions, with no numerical acceptance tolerance.

One Python 3.9.6 process completed the diagnostic in 0.029991292 seconds and
reported peak RSS 18,808,832 bytes on Darwin. The protocol had an eight-second
alarm and a 25,000-state support cap; neither is represented as a job-wide
memory-enforcement qualification. Optimization mode was rejected explicitly
before execution so the exact assertions could not be disabled.

### Additive post-run spectator clarification

An independent reviewer found no algebraic blocker before execution. Its
later documentation suggestion arrived after the run: “all other storage
fixed” should explicitly identify blank, uncoupled writer/reservoir spectators
with zero storage energy. The frozen displayed matrix and code already use
the +9 record/carrier storage contribution and no spectator contribution.
Blank uncoupled spectators realize that restriction, but this prose state
mapping was not separately frozen before the run. This clarification is
recorded after execution; the protocol/source have not been rewritten.

Thus the number 27 is the complete initial energy of the specified computed
restriction, not an authenticated complete physical preparation with every
external supply accounted for. A common fixed spectator offset would shift
both values equally without changing energy equality or any return result.
No retry, fitted correction or retrospective tolerance change occurred.

## 4. Relation to actual formed-state evidence and the dark-sector boundary

The existing K2,2 formed-state source independently retains A=n00*n10,
B=n01*n11 and W=<A>+<B>+2<AB>, and links these to the full carrier H^2
block. Its saved result includes the full incidence distribution and joint
path statistics; it must not be replaced by products of edge means.

That experiment's matching gate remains failed: its native P/Q preparations
differ in count, feedback energy and complete hold energy. Its reported
energy difference 0.0017598451898050982 is not repaired by this new fixture.
The present engineered diagonal ensembles do not substitute for those
coherent formed states or establish that their history causes only an
arrangement change. Source/result were inspected read-only; no old run was
replayed or edited.

The useful result is narrower and constructive: graph correlations are both
native information and operationally relevant to propagation, even when
mean incidence and initial modeled energy agree. A geometry construction
must retain the relevant correlations or justify their controlled reduction.
Macroscopic dimension, physical volume/stress, causal spacetime geometry,
record formation and dark-sector predictions remain unproved.
