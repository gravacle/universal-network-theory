# Independent native ruler-discriminator review

2026-09-29. Accepted within the existing native 16-state source/readout model.
The complete source, protocol, step addendum and synthetic witness were read.
The underlying analytical normal-form/source note and witness were independently
checked before implementation; this full numerical-source audit finished after
the parent reported its run, not as an independent pre-run numerical review.

All 17 frozen inputs and the canonical payload authenticate. The result keeps
15 actual state/age rows, 90 sector rows (70 retained and 20 explicitly null),
60 delays, 240 signed finite pulses and six separately labeled constructed-state
controls. All 55,766 producer check entries passed. Runtime 0.055702 s; peak
self RSS 38,928,384 bytes on Darwin, not aggregate job memory.

- Result: `3d67d00feb7c43a5bfac598d154429b5aff46865f830295ddf5cfe00d962dc2c`
- Freeze: `ad6836ce590af6d89e6b8d28243549f094eadd90a6660c1c29373057ee875014`
- Payload: `d25217c0827cf9bcda0399d4c82c2a5b512220fa5975930543912f84f85336e7`

Independent saved algebra passed 2,291 checks without propagation, Kubo
quadrature or pulse reruns. Direct contraction of each original formed vector
independently verifies its age-zero triple correlation and impulse-work sign.
Every retained conditional Bloch rotation, compact action, affine energy,
incidence source map and lower-point k/M relation recombines correctly. Sector
sums reproduce the old held energy, incidence, record mean and signed source
moment. Null weights were not divided or substituted for full states.

The actual native preparation has a nonzero, phase-sensitive writer-to-carrier
response. Its controlling correlation changes sign while held energy and each
sector's action, radius and weight stay invariant:

| Held age | <Xa Yc,std Yrec> | Plus-step quartic coefficient |
|---|---:|---:|
| 0 | 0.410452359 | 0.00427554541 |
| 0.25 | 0.357396321 | 0.00372287834 |
| 0.5 | 0.150867619 | 0.00157153770 |
| 1 | -0.241915966 | -0.00251995798 |
| 2 | -0.536211033 | -0.00558553160 |

Held native energy remains 4.1279840123 in the owned units. Across all declared
delays its exact step derivative ranges -2.57039e-7 to 1.89403e-7; the distinct
ideal-impulse derivative ranges -1.25875e-5 to 9.62452e-6. Neither the sign nor
a nonzero value was a success condition. Small finite-pulse changes retain
absolute numerical allowances rather than an unsupported relative-precision
claim. The onset powers and full response are not interchangeable.

All signed finite changes, their linear predictions, central/Richardson
comparisons and on/off work recombine. Maximum work-ledger discrepancy is
7.18e-15; signed held-energy changes span approximately -0.00143230 to
0.00143154. The source is not treated as energy-free.

The constructed zeta=.5 pair is separate evidence: under the native held
Hamiltonian both states have energy 39/8 and baseline carrier probability 1/2,
but opposite step-quartic coefficients ±1/192 and impulse-cubic coefficients
±1/48. The proper marginals refer specifically to the three groups record-pair,
incidence and carrier, not every three-of-four individual-qubit marginal.
Its exact matrix theorem is not a claim that the actual native preparation
produced those mixed states. The formal R-dephased controls likewise preserve
the unperturbed baseline but are not free physical erasure or shared phase clocks.

The result therefore strengthens the native interface: a specified writer
source interrogates correlations through an owned carrier readout, and compact
affine sector mechanics is verified without discarding phase or mandatory
momentum terms. It does not yet identify that source as physical metric strain,
derive a collective quartic continuum, or establish gravitational dynamics.

Reproducible audit: `native_ruler_discriminator_saved_audit_v001.py` and
`NATIVE_RULER_DISCRIMINATOR_V001_AUDIT_DATA.json`. Later aged intersector
correlations cannot be reconstructed from the saved conditional blocks alone;
their full-kernel checks and dephased nulls remain authenticated producer
evidence, supported by the independently reviewed operator identities.
