# Prospective complete90-graph induced-switch census

2026-09-29. No output inspected. Root owns the only numerical execution.

Enumerate every simple bipartite N=4, k=2 graph from the6^4 row-pattern
candidates, enforcing every column degree. Retain all90 resulting graphs:
18 disconnected pairs of four-cycles and72 connected eight-cycles. Store
each original16-bit edge mask, component vertex lists, every switch and
neighbor index. No connected-only postselection or microscopic coefficient
change. This is the dimensionless leading operator H_eff/g4=-A, with its
common scalar energy shift omitted only from transition probabilities.
It is NOT full2^16 native incidence propagation.

Check the legal-rectangle adjacency independently through its symmetry,
degree/topology neighbor counts and common-neighbor/four-cycle count.
Check that the configuration-space switch graph is connected; distinguish
this from incidence-graph connectivity. Compute all90 adjacency eigenvalues
and the full positive Perron vector. Check the exact normalized2-orbit
quotient [[0,8],[8,8]], its intertwining, lambda_max=4+4sqrt5 and connected
ground probability(1+1/sqrt5)/2. Explicitly retain its comparison with the
uniform graph-count probability .8; do not call the connected majority an
enhancement or selection of connected geometry.

The declared dynamical input is the COHERENT uniform disconnected vector.
Use tau=g4*t/hbar at fixed values

    0, pi/(32sqrt5), pi/(16sqrt5), pi/(8sqrt5),
    3pi/(16sqrt5), pi/(4sqrt5), 1.

Compare full90-dimensional spectral evolution to the independent2-by2
quotient and to .8sin^2(4sqrt5*tau). Retain all90 output graph probabilities.
No native age in physical units is assigned. Add the explicit incoherent
uniform-D density control and all18 individual-D connection probabilities
from the same full unitary: these need not obey the coherent formula. Check
their relabeling equality, normalization and their exact initial tau^2
coefficient16 versus64 for the coherent input. Both prepared controls start
with topology probability0 and mean dimensionless kinetic energy0; their
coherence preparation is not asserted free or actually formed.

Integer combinatorial checks use exact tolerance0. All floating isometry,
eigenvector/eigenvalue, probability, normalization and conservation controls
use fixed absolute1e-10. No outcome-dependent tolerance or desired connected
sign is permitted. Retain all failed controls. There is no fit, stochastic
sampling or irreversible evolution. A90-by90 NumPy eigensystem and seven
small unitaries are the only numerical workload; one thread, no checkpoint
needed and target output below1MiB.

The analytical degree-sector note, quotient derivation, original BS source,
worker and this protocol enter the prospective snapshot. `freeze` prints
that snapshot without running enumeration/evolution; root saves it with
apply_patch as NATIVE_SWITCH_GRAPH_V001_FROZEN.json. `run` requires matching
sources and prints one complete result wrapper with payload/freeze hashes.
The worker writes no files, disables bytecode and returns exit2 on numerical
control failure. Root reviews and publishes outputs. The finite-N strong-
degree projection, full-Q denominators, actual native parameter/state and
operational ruler conditions remain those of the analytical companion;
passing this census does not establish them.
