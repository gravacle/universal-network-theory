# Independent saved-state spherical audit

2026-10-04. **PASS: 620/620 audit checks**, retaining all **23/23 producer
controls and all 12 states**. The 0.210-second audit imported no producer,
performed no field solve or fit, and used only frozen saved states.
The numerical slot has been released.

## Reconstruction

Authenticated source, protocol, result and every case hash. Reconstructed
the midpoint meshes, origin and outer faces, identical-interior domain
extension, positive spectral weights and moments, physical scaling and
Plummer source. Independently formed face fluxes
F=r_face^4 delta_u/delta_r, then the diffusion term
-lambda^2 delta_F/cell_volume. This does not use the producer's assembled
diagonal/off-diagonal operator. The largest independently normalized field
residual is 3.83e-13, below the unchanged 1e-9 gate. The largest difference
from the saved normalized residual array is 2.19e-13; this is expected
floating-point reassociation, not a residual-sign discrepancy. The global
telescoping flux balance also passes its term-scaled arithmetic check.

Reconstructed matched finite-spectrum local fields, every local cubic and
flux identity, the outer local-mode condition, explicit two-node log-radius
interpolation, A, total g, and all mesh/spectral/domain comparisons. Checked
the independently saved exact-radius local baselines using Newton cubic
evaluation and positive angular quadrature, without rerunning their inverse.
The saved Newton-correction gate is retained and checked, not independently
re-solved or promoted to a rigorous nonlinear error certificate.

Maximum changes in A across the prescribed family are 0.00225672 (mesh),
3.95e-9 (spectrum), and 1.03e-11 (domain), all below 0.02. Every saved modal
field is positive. No case or radius was removed.

## Full force relative to the flat-speed value

The dimensionless circular-speed comparison is
v_c^2/sqrt(G M a0)-1=r*(g/a0)-1, not A itself. On the finest extended
domain, the declared readouts give:

| M/Msun | r=5 | r=10 | r=20 | r=50 |
|---|---:|---:|---:|---:|
| 10^7 | -0.0371044 | -0.0281511 | -0.0160827 | -0.00682190 |
| 10^9 | +0.0842433 | +0.0387616 | +0.0185513 | +0.00729046 |
| 10^11 | +0.0854104 | +0.0394084 | +0.0188913 | +0.00743055 |

All saved nodes between r=5 and 50 have the same respective sign. Replacing
the interpolated local baseline by its saved exact-radius value changes
these dimensionless totals by at most 1.57e-4 and preserves every sign; this
is a descriptive interpolation-bias diagnostic, not a replacement result.

A(50) is 0.987466764, 0.980321429 and 0.980253027 for increasing mass.
Thus the spatial correction lowers the local response in all three cases,
while the full low-mass curve lies below the nominal flat value and the two
higher-mass curves lie above it at these radii. This is consistent with the
formal sign-changing far-field coefficient, but finite-radius agreement
does not prove the asymptotic limit or a global existence/uniqueness theorem.

These are prepared, isolated, settled Plummer configurations of the changed
effective parent with the disclosed ell=100 pc. They are not observed
galaxies, disk predictions, formation histories, external-field tests,
Cassini estimators, or shared-cosmology predictions. The earlier 94-galaxy
score still tests only the zero-gradient local proxy.

## Custody

- Producer result: `657fa06ac5fe875a6ccef405b8061c42eb63f4715ed7878ee16f6836e10682f7`.
- Audit source: `3c8d14f9afad863d296573a9ae2fe4231f5957ee98668a29e6b47a2808e36222`.
- Audit JSON: `075d0f463b0729ae2aa597439527cc1d2518c25b17704afacab2b605fb5de33e`.

Frozen inputs were read only. The new JSON receipt was published atomically
with no-overwrite semantics; no numerical or scientific gate was relaxed.
