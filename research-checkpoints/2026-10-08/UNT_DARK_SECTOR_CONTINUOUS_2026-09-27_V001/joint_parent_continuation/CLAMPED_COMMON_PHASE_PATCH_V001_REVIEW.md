# Clamped common-phase patch V001: independent saved-results review

2026-09-29. Accepted as retained numerical evidence, with four explicitly
nonconverged outcomes. This review executes only saved-array/hash arithmetic;
it does not rerun the material kernel, orbit quadrature, Jacobian, Newton
iteration or spatial solver. The reviewer authored the frozen driver and
collector; the law and scope peers independently preflighted them. The law
peer authored the material kernel, which this reviewer independently read.
Thus this is a separately implemented arithmetic audit, not an independently
implemented PDE solution.

## Binding and audit

The original physical sources are unchanged:

- Driver `clamped_common_phase_patch_v001.py`:
  `c4279bb3690174f2158eb46c46b23adfed008c9585e5f2bf381e0eb04744a3b3`.
- Protocol `CLAMPED_COMMON_PHASE_PATCH_PROTOCOL_V001.md`:
  `b867a6db67d8bfcc1746bbf14830acd8a10c36bfbaa31dc049bb045f21bb7daa`.
- Material `clamped_phase_material_v001.py`:
  `d8472d6d585167bab8756a9451254693aab675294c86aa4321ff56d50c5cc7a8`.
- Physical freeze: `83085beb8df6d5a706b449f1ba4c5751698f81f1792c436e78e1e9f42600ec31`.

All eight `CLAMPED_COMMON_PHASE_PATCH_V001_CASE_000.json` through `_007.json`
transports authenticate their complete raw bytes, payload and shared freeze.
All 64 unique ancestral files, 12 manifests and 303 manifest-member
occurrences authenticate. The saved source rows match the original finite-gap
screen exactly. The reproducible receipt contains every case's exact hashes:

- `clamped_common_phase_patch_saved_audit_v002.py`:
  `0a7ad47b3f473510136e316f1a3b0056b8ec1675a9efe3163e5cf1915906b8f4`.
- `CLAMPED_COMMON_PHASE_PATCH_V001_SAVED_AUDIT.json`:
  `a9afd71883d29cc28dbbe57c099f8ba854253a04aec92a7277c8695a921c2a96`.

Its 229,016 saved-arithmetic comparisons pass. They independently recombine
phase energy/pressure and J, hard/soft reaction, annular volume and sheet
flux, source/outer-flux ledger, per-copy action inventory, local lengths,
omitted-stress readouts, seed differences and qualification status. Finite
differences and quadrature agreement remain original producer controls, not
newly executed independent checks.

The collector result has SHA
`e88805622c128700e7e1d6597cea8fc4514a7347116d2179462b045ef14ee5f6`,
with freeze `9a95f1eaa4ce06cb69144882905d5e73f76092ec4e29989482178ddaeed34caf`.
`clamped_patch_collection_saved_audit_v001.py` independently uses explicit
four-corner interpolation and compensated summation, rather than the
collector's successive one-dimensional interpolation. All 24 prescribed
comparisons and 3,432 metric comparisons pass; maximum scaled difference
is 1.84e-14. Its receipt is
`CLAMPED_COMMON_PHASE_PATCH_COLLECTION_V001_SAVED_AUDIT.json`.

## Complete outcomes, not an all-converged certificate

| Hard gap R | Box L | Meshes | Seed outcomes |
| --- | --- | --- | --- |
| 128 | 1 | 16², 32² | All four converged |
| 128 | 2 | 16², 32² | All four converged |
| 8192 | 1 | 16², 32² | All four converged |
| 8192 | 2 | 16² | Line-search failure; iteration limit |
| 8192 | 2 | 32² | Two line-search failures |

There are 12/16 converged seeds, with final normalized residuals at most
2.35e-11. The other four residuals remain 1.65–1.78, with signed flux defects
of about -0.85 to -0.89. They are not equilibria. Their empty/occupied regions,
signed potentials, source arrays and full histories remain saved; no result
is discarded because it is unfavorable.

All 354 actually executed producer controls pass, but only 15/16 Jacobians
are qualified by all four directional comparisons. Case7/seed1 has active-set
switching and is explicitly unqualified, not passed by omission. Likewise
`COMPLETE_RETAINED_OUTCOMES` records completed attempts, not successful roots.
Total measured producer runtime is 180.715 seconds, maximum self RSS
380,108,800 bytes; this is not whole-machine or combined-process memory.

## What the results establish

For the six converged cases, the two seeds agree closely. On their prescribed
N16-to-N32 shared centres, the symmetric volume-weighted RMS differences are
0.076–0.154% in Phi, 0.833–1.329% in radial gradient and 0.542–0.877% in vertical
gradient. The R8192/L1 radial comparison is 1.032%. These are descriptive
refinement differences, not a newly selected accuracy threshold or proof
that every local feature is resolved.

The finite common-phase hard state is not generally negligible. In the
converged R8192/L1 patch, its normalized integrated source is
0.146385–0.146705, versus sheet flux 0.292893; the soft reaction contributes
only about 3.46e-8. The retained I/Ib reaches 7.91e5 while |Phi| stays below
1.54e-7. This demonstrates why a small potential does not imply a small
common-phase state contrast. It does not identify action contrast with the
complete gravitating density, which also has polarization/divergence and
stress terms.

For R128, hard-source integrals are about 6.05e-9 in L1 and 6.97e-8 in L2;
the corresponding soft integrals are about 2.37e-8 and 1.00e-7. These values
follow from the full retained state rather than imposing a smooth hard source.

Boundary placement matters strongly: for the converged R128 solutions,
changing L1 to L2 changes shared-point radial gradients by 35.3–36.2% and
vertical gradients by 49.4–50.5% in the declared RMS metric. This compares
different externally clamped patches, not isolated-domain convergence. The
R8192/L2 retained failures cannot supply a physical clamp-convergence result.
Agreement of two seeds is not uniqueness; failure of these seeds is not a
nonexistence proof. All reported differences and signs are retained.

## Necessary interpretation boundaries

The nonzero bottom flux at the bottom/outer-wall intersection conflicts with
a C1 extension of the zero wall potential. The independently checked local
constant-coefficient corner solution has a logarithmic gradient singularity,
although its potential is bounded. Thus full-domain maximum-gradient or
omitted-stress refinement must not assume smooth corner data. No grid points
were removed after outcomes. The collector's documented geometric
no-extrapolation mask is not a newly chosen corner mask.

This is a conditional, open-reservoir, weak-lapse constitutive/BVP screen.
It is not an isolated disk, an observed rotation-curve fit, a full tensor
metric solution, a dynamically formed state, a selected halo boundary or
dynamical stability result. The absolute matched vacuum and source-state
accounting are retained. The finite-field material coefficients and hard
self-gravity are included; replacing them with the tiny cosmic susceptibility
would be a different problem. The collector correctly leaves
`numerical_resolution_certified=false`.

The constructive outcome is therefore precise: some declared same-state
patches admit numerically converged roots, their hard reaction can be large,
and the colder/larger-patch attempts expose an unresolved equilibrium or
solver-branch question. A separately labeled attribution/continuation test
can investigate it without replacing these original outcomes or claiming a
galaxy or cosmological success.
