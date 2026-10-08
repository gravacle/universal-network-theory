# Independent analytical review: native interacting incidence block

2026-09-29. Complete review of `NATIVE_INTERACTING_COLLECTIVE_MODE_V001.md`,
SHA-256 `c7e0e52710f91645b6750415ee9bfebe3cd423e2ec274cdc01aef13fe67f80e3`.
No eigenproblem, evolution or fit was run. **Accepted: no load-bearing
operator, normalization or asymptotic defect found.**

The four-link rook graph has four adjacent pairs. Expanding the degree
penalty gives the stated absolute constant `4+4q`, linear cost `2-q`, and
pair coefficient `2U`; blank carrier terms vanish in this declared sector.
The normalized configuration counts `(1,4,2,4,4,1)` independently give every
off-diagonal entry of the six-state block. Uniform `M` preserves it exactly;
the ten-dimensional complement remains part of the full model. Positivity
and uniqueness of the full ground state at `h>0` put that ground state in
the bright block, but do not identify higher bright levels with the next
full-space levels.

Direct second-order nondegenerate perturbation theory reproduces all three
energy shifts and
`K_spec/h^2=-6/kappa+8/(kappa+2U)-2/(kappa+4U)`.
This equals the note's negative rational expression. First-order eigenvector
corrections give the signs and denominators of all three source entries;
the squared lowest-pair ratio is `1/2`, not the canonical oscillator's `2`.
The `U->0` individual-branch interpretation must be replaced by the summed
degenerate strength, exactly as stated.

The source identity `[M,[H,M]]=h sum X` and its signed eigenstate spectral
sum rule have the correct factor two. They constrain the actual source
normalization rather than supplying a free effective mass or contact.

The complex-h justification is sufficient. Since the diagonal matrix is
normal and `||F||=4`, each perturbed eigenvalue lies within `4|h|` of a
diagonal eigenvalue. For `|h|<g_min/8` the disks are disjoint, identifying
analytic branches. On the smaller Cauchy circle `R=g_min/16`, each branch
shift is at most `4R`. Parity makes the branches even; the curvature
combination has absolute coefficient weights `1+2+1=4`, giving the stated
`16R (|h|/R)^4/[1-(|h|/R)^2]` remainder. Neither this domain nor the leading
negative sign is silently extended to the inherited `h=1/2`.

The quantum/classical distinction is essential and correctly retained:
affine expectation energy in exact eigen-population actions coexists with
unequal quantum transition spacings. Three energy levels alone do not
derive an amplitude-dependent constant-mass classical oscillator, its
source ladder, or a large-occupation limit. The Feshbach expression also
correctly retains its energy and source dependence.

The prospective full16-versus-bright6 calculation is an appropriately small,
decisive test of this **native source channel**. Either sign of its exact
inherited-parameter curvature is scientifically admissible. No preparation,
physical strain/volume assignment or cosmological/galaxy inference follows
from this analytical certificate alone. Implementation and output require
their own independent checks.
