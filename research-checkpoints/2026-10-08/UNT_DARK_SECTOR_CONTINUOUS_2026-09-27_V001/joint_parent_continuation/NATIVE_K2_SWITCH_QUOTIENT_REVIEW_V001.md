# Independent analytic check: N=4, k=2 switch quotient

2026-09-29. No graph enumeration, matrix diagonalization or propagation run.
This checks the prospective leading switch operator, not a full native
fixed-Omega effective-theory error bound.

Every simple 2-regular bipartite graph on four plus four labeled vertices is
either two four-cycles (D) or one eight-cycle (C). The counts are
`D=3*3*2=18` and `C=4!*3!/2=72`. The latter counts alternating Hamiltonian
cycles without orientation duplication.

Each D graph has 16 legal switches, all of which join the two components.
The degree-switch formula independently gives 12 switches for each C graph.
All C graphs lie in one relabeling orbit, so the number of D neighbors is
constant. Counting undirected D-C edges gives `18*16/72=4`; its other eight
neighbors are C graphs. These statements derive the neighbor census without
numerically selecting a connected subset.

For the normalized **coherent uniform** orbit sums `|D>` and `|C>`, the
leading adjacency restricts exactly to

    A_bright = [[0,8],[8,8]].

The off-diagonal element is `18*16/sqrt(18*72)=8`. Its eigenvalues are
`4±4sqrt(5)`. The larger has positive coefficients in both orbit sums, so
its lifted full-space vector is strictly positive and is a spectral-radius
eigenvector of the nonnegative full adjacency. A uniqueness assertion also
requires connectivity of the full switch graph, which the prospective
enumeration can check directly.

For `H_switch=-g4 A` after common shifts, its connected ground weight is
`(1+1/sqrt(5))/2`. Removing the scalar diagonal part leaves a two-level
matrix with off-diagonal 8g4 and detuning 4g4. Starting specifically in the
coherent uniform `|D>` state therefore gives

    P_C(t)=(4/5) sin^2(4sqrt(5) g4 t/hbar).

This does **not** automatically describe one disconnected basis graph or an
incoherent mixture over the 18 D graphs, which contain other symmetry
sectors. The full dynamics remain reversible.

The ground's connected majority is not evidence of preferential connected
selection: its weight approximately 0.7236 is below the raw counting
fraction `72/90=0.8`. Relative to the uniform basis measure, the kinetic
ground enhances disconnected configurations. The useful result is an exact
native-induced topology-changing channel and a small prospective spectral
test, not a derived connected physical geometry, cosmological growth law,
metric or controlled N-uniform long-time evolution.
