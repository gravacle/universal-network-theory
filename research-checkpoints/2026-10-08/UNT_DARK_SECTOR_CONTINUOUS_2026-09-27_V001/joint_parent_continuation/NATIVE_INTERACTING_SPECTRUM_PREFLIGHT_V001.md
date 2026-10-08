# Independent native interacting-spectrum implementation preflight

2026-09-29. Read-only review of the entire prospective worker, protocol,
analytical note and original `BS_MICRO_ACTION.md`. No module was imported,
eigenproblem solved, source state prepared or numerical worker run by this
reviewer. **Accepted: no blocking mathematical or implementation defect found.**

Reviewed SHA-256 identities:

- `native_interacting_spectrum_v001.py`:
  `c699f20f2231466c2edfa3112f89f8e54d9766beb347627e17a3ecfd737b5396`
- `NATIVE_INTERACTING_SPECTRUM_PROTOCOL_V001.md`:
  `260181cafdb9d3e9e296ded7976150be5f90fd3cdea2e709040b3d2f94a22fa7`
- `NATIVE_INTERACTING_COLLECTIVE_MODE_V001.md`:
  `c7e0e52710f91645b6750415ee9bfebe3cd423e2ec274cdc01aef13fe67f80e3`

The full four-bit construction correctly assigns the two row and two column
degrees. Its independent pair expansion has the four rook pairs and gives
`C=4+4q`, `kappa=2-q`, with all four native flip terms retained. BS09 and the
BS11 current-square term annihilate the declared blank-carrier sector; the
occupied-record onsite cost is not removed. Both record sectors are held
comparison preparations, not an uncharged change to an actual formed state.

The normalized orbit masks `(1,4,2,4,4,1)` give the stated six-state block and
source matrix. The complement construction, direct Hamiltonian/source
crossblocks and full-versus-bright-plus-dark spectral comparison retain the
other ten dimensions. Higher ordered bright levels are not mislabeled as
the corresponding ordered full-space levels. At each positive flip strength,
the unique full ground state lies in the bright block.

For `H-fM`, `[M,[H,M]]=h sum X` has the correct sign and factor. The trace
source sum rule, equal-mixture impulse-work curvature and degenerate-cluster
second energy derivative use whole projectors. The latter is the trace
curvature of the cluster, not an arbitrarily selected degenerate eigenvector.
The independent ground-state derivative solves
`(H-E0) psi_f=(M-<M>) psi`, with the ground projector making the linear
system invertible; its susceptibility is positive and equals minus the
ground energy's second source derivative. The bare source contact is zero
by the explicitly affine source definition, not a new inferred coefficient.

The second-order energy coefficients, source-entry coefficients and negative
weak-flip spacing coefficient agree with direct perturbation theory. The
smaller Cauchy circle `R=g_min/16`, individual energy bound and four-weight
curvature bound are consistent. The source applies those bounds only at
the three prospective small flip strengths, never to the inherited `h=.5`.
Neither the native finite-flip curvature sign nor a monotonic ratio trend is
used as an acceptance condition.

The complete eight-case census, real-projector serialization, absolute blank
energy/variance, source pins, stdout-only publication and freeze comparison
match the protocol. The numerical tolerances are separate from analytical
truncation bounds. This review certifies the prospective implementation, not
its as-yet-unreviewed numerical output or a classical collective oscillator,
physical clock, metric coupling or dark-sector inference.
