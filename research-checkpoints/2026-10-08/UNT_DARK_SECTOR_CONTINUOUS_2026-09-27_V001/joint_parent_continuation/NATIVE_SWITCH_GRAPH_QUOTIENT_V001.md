# Exact topology quotient of the induced N=4, k=2 switch operator

2026-09-29. Analytical result for the leading degree-preserving operator
derived in NATIVE_DEGREE_SWITCH_CHANNEL_V001.md. No additional microscopic
term, physical coefficient choice, formation, fit or numerical execution.

## Exact census and operator

A simple two-regular bipartite graph with four vertices on each side is
either a single eight-cycle C or two disjoint four-cycles D. There are

    |D|=3*3*2=18,   |C|=4!*3!/2=72,   total90.

For D, partition each side into two unordered pairs (three choices each)
and match the pair blocks in two ways. For C, fix one left vertex as the
cycle origin, order the other three left vertices and all four right
vertices, then divide by the two orientations.

Let A be the unweighted adjacency matrix whose entries are1 exactly for
one legal alternating-rectangle switch. A D graph has16 switches, all to
C: choose one of the four edges of each component, then reconnect the
two pairs crosswise. A C graph has12 switches by the exact common-neighbor
formula. Relabeling is transitive on each topology class; double counting
18*16=72*4 gives four D neighbors and hence eight C neighbors per C graph.

The two normalized COHERENT orbit sums |D>,|C> therefore form an exact
invariant subspace of A with

    A_orbit = [[0,8],[8,8]].                            (1)

All90 graph states remain in the full operator. Equation(1) is a symmetry
reduction, not a projection that discards the other88 states for arbitrary
initial conditions. The physical leading effective Hamiltonian is
common_energy*I-g4*A, with g4>0 derived from the four-flip denominators.
Only the common identity is irrelevant to this transition-probability
calculation; it is not removed from any physical energy/volume ledger.

## Ground-vector and preparation-dependent dynamics

The orbit eigenvalues are4+/-4sqrt5. The eigenvector for the larger value
lifts to a strictly positive vector on all90 states, and hence is a Perron
vector of the full nonnegative adjacency matrix. Connectivity of the switch
graph makes it unique; the prospective enumeration checks connectivity
without assuming that physical incidence graphs are connected. Its weights
in the normalized orbit basis are

    |a_D|^2=(1-1/sqrt5)/2,
    |a_C|^2=(1+1/sqrt5)/2.                              (2)

Thus the leading kinetic ground state has connected probability about
.7236068. The unweighted graph-count baseline is72/90=.8. It therefore
RELATIVELY ENHANCES disconnected configurations, despite retaining a
connected majority. Per-configuration C/D amplitude is(1+sqrt5)/4; the
corresponding probability ratio is below1. This is not a selection of
connected spatial geometry.

For dimensionless time tau=g4*t/hbar, start from the COHERENT uniform
|D> vector, not an individual D graph or an incoherent uniform mixture.
Since A_orbit=4I+8sigma_x-4sigma_z,

    P_C(tau)=(4/5)sin^2(4sqrt5*tau).                   (3)

It reaches .8 and returns to zero periodically. This is reversible
amplitude transfer, not an irreversible increase in connectedness. The
full unitary is exp(+i*tau*A), with the sign from H_eff=-g4*A.

A useful preparation control uses rho_D=(1/18)sum_D |G><G|. It has the
same initial topology probability and mean dimensionless kinetic energy0
as |D><D|, but a different relational coherence. Exactly at small tau,

    P_C,coherent=64*tau^2+O(tau^4),
    P_C,incoherent=16*tau^2+O(tau^4).                   (4)

The first coefficient is||A|D>||^2=64, the second is the average16
outgoing links per D graph. By relabeling symmetry every individual D
graph has the same total connected probability as that mixture, though
its probabilities for labeled targets differ. Neither preparation is
claimed to have been produced by native record formation. Their equal
initial energy is not an assertion that preparing their coherence is free.

## Physical scope

This exact finite graph calculation tests an induced native operator, not
the full2^16 incidence evolution or a new value of lambda_R. Its microscopic
use requires the strict k=2 degree manifold and controlled elimination of
degree defects established in the companion note. The inherited positive
kappa ground state is not in that regime. No spatial embedding, operational
dimension, physical time scale, attraction law or cosmological result is
obtained by reinterpreting this configuration-space adjacency as a metric.

The result is nevertheless informative: the native induced channel moves
between component topologies, and its complete leading ground and dynamics
can be determined without adding a loop term or postselecting connection.
