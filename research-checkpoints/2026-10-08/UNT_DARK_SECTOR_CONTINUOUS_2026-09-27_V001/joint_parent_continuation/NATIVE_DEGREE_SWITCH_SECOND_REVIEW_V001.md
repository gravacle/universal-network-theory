# Independent degree-switch analytical review

2026-09-29. Full read of `NATIVE_DEGREE_SWITCH_CHANNEL_V001.md`, including
the final extensive-bound and N>=2 clarifications. Reviewed SHA-256:
`bd52d3200aa758613471f9d1053a402d8c3e7560420a3da99357787acf082f23`.
**Accepted.** No eigensolver, enumeration, propagation or fit was run.

The degree-square expansion, strict k-sector interval and positive one-flip
costs A,B agree with BS06/BS11. Convexity and the bipartite degree-sum
constraint give the stated exact unperturbed gap. The separate extensive
bound outside BS13 follows from the edgewise transfer/current minimum,
record occupancy<=1, sum d_v^2>=2M^2/N and minimizing
`2U M^2/N+aM` over M>=0. It does not assert projection control or connectivity.

Two distinct flips cannot preserve every degree in a simple bipartite graph.
Thus PVP=0 and P(sum X)^2P=N^2P, giving the exact off-block norm Omega.
The second-order counts and the fourth-order adjacent/disjoint pair counts
are fixed throughout the regular manifold. Folded lower-order products are
scalar, so they cannot change the fourth-order off-diagonal switch element.

For a rectangle, each of the six sign words has four labeled paths. The
mixed two-flip cost is C=(A+B)/2=2U. Three negative resolvent denominators
produce the negative amplitude; summing all24 products gives
`2/A^3+2/B^3+(4/C)(1/A+1/B)^2`. Its centered value is `5/(2U^3)`.
No microscopic loop term was inserted. The fixed-N O(h^6) remainder and
the sufficient norm criterion are appropriately distinguished from an
unproved uniform-in-N reduction at fixed Omega.

The exact full-Q resolvent bound uses the correct numerator norms Omega
and Omega^2. The switch degree bound gives the stated O(N^-2) fourth-order
operator scale; the matching transposition mode has eigenvalue N and
excitation g4*N. For k=2, the common-neighbor identity reproduces
`F(G)=Nk[Nk-2k^2+2k-1]/2+2C4(G)`, including12 versus16 switches in the two
N=4 topologies. Larger row count alone is not a ground-state concentration
proof, exactly as stated.

At kappa=0 the entire matching manifold is required. Its configuration
counts and addition/removal degrees give exactly
`-Omega(1-m/N)*sqrt(m+1)`. This is a first-order finite-capacity channel,
not the strict-sector formula at a zero denominator or a derived positive
harmonic frequency. The excluded-space gap2U correctly requires N>=2.

Finally, the inherited kappa=2 or1 remains in the empty-degree passive
branch. The explicitly named changed-parameter sectors and inherited
excited-sector resonances are not hidden recalibrations. This is genuine
native effective-channel mathematics, not yet a physical metric, connected
phase, large-occupation quartic mode or dark-sector prediction.
