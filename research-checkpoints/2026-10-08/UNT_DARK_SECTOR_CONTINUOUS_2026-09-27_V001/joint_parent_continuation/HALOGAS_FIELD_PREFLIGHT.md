# Independent HALOGAS eight-case preflight

Accepted before root execution; no requested source change. This review read
all three new files, the complete inherited ring implementation and V002 solver
API, and the source/tracer scope note. Only syntax and read-only JSON/header/
hash arithmetic were performed. No module was imported and no source
qualification, force quadrature or PDE was executed by the reviewer.

Exact reviewed identities:

- `halogas_density.py`:
  `f2e7b75fdcdbd8b690a148f7f19800a0662690be51ec3c6164c6cc2cc9b6394a`
- `halogas_field_compute.py`:
  `56e36318aa63dd5e3e46ca3a978e5705efcdf68b8f61eb8f777141ed14be30a6`
- `HALOGAS_FIELD_PROTOCOL.md`:
  `587a35af46767ff03852b23e7e3538fc834de999b2792c5855d86e8ae4000499`

## Source implementation

The code implements the already reviewed quadratic Bernstein polynomial in
R^2, with the correct cubic primitive and factor Delta(R^2)/2 for integral
R*Sigma*dR. Indexing at zero, internal boundaries and the outer edge is
consistent with C0 continuity. Infinite upper integration limits clip to the
finite support; exterior density/integral are zero. Nonnegative net bin
masses are required before construction. This does not clip the negative
pixel contributions already included in those signed bin totals.

The exactly contiguous complete prefixes are required to be 51 and 17 bins.
No flux-dependent trimming or choice between resolutions occurs. The full,
included, excluded and negative-pixel ledgers, zero-retention bins and common
support are retained. The explicit exterior zero remains a contrast model,
not a claim of physical absence. The 1.36 HI helium factor is applied once.
Stars use the same fixed full-profile calibration as the completed control;
H2 and its inherited helium convention are unchanged.

Three Gauss points in R integrate degree-five R*Sigma exactly in exact
arithmetic, so the independent full-bin and subinterval checks are valid.
The center derivative is analytically zero; its code check records that
identity rather than claiming independent derivative observations. Control
positivity, Bernstein bound, exact zero intervals, continuity, exterior zero,
per-bin mass and shared totals are all scheduled before any PDE.

## Independent force oracle

The runner calls only the generic immutable `field` and source-knot machinery
of the existing ring implementation, not its old source factory or the
piecewise-linear slope helper. The generic API needs only sigma, integral,
knots and tail; the Bernstein component supplies each correctly. Its finite
support is included in the cutoff, while stellar/H2 exponential remainders
retain their own signed-force/potential tail accounting.

There are ten predetermined new oracle cases: two sources at all five
inherited radii, each with three deterministic knot-separated heights and
both orders 48/96. Quadrature panels include the new density knots. The
smaller near-knot height for a changed source is geometrically specified,
not selected from a force result. Component masses, potentials and signed
forces are retained. Height extrapolation, mass closure, both-order agreement
and tail checks use unchanged criteria. The five-radius Newtonian grid
comparison uses each source's own fresh oracle, not an old-density reference.

The prior AGM, direct-angular ring and exact Kuzmin checks remain inherited
qualified evidence. A fresh quadrature for the new sources does not by itself
make the gas reconstruction observationally complete.

## Eight cases, control pairing and restart

The loop is exactly 40 then 120 arcsec, each at N256/L255 nonlinear,
N320/L1023 nonlinear, N512/L255 nonlinear and N512/L255 Newtonian. It carries
the new source into bottom annular flux, component/total masses, spherical
outer boundary and smooth initial field. No physical operator or constitutive
function is monkey-patched or tuned.

Every result pairs with the completed ML36 calibrated control at the same
mesh, domain and equation. All 43 observation identities are checked and
retained, including signed force/v-squared and null real speed if needed.
The negative-force omission count is disclosed in each descriptive summary.
No residual or nominal quoted-error sum is an acceptance gate. Both mesh and
remote-domain comparisons use the same new source's coarse baseline.

Checkpoint names are distinct for each new source/case. The inherited loader
authenticates case, freeze, field and completed history; the solver recomputes
convergence from the supplied field and charges the existing history against
its unchanged 300-update allowance. Completed results are authenticated and
reused. Failed qualifications/cases are preserved and stop this frozen attempt.
No old checkpoint, source or result is replaced.

## Custody and claims

Static recursive checking verified seven old manifests and 74 distinct
ancestor files: calibration, original galaxy field, ring oracle, both
stretched-disk versions, original disk solver and new planar extraction.
All actually imported physical/numerical helpers occur in that authenticated
ancestry. This count excludes the new direct source/protocol/context additions
and explicitly added final control outputs, so it is not the final manifest
size or a count of independent scientific tests.

The runner additionally authenticates the fixed extraction-result bytes and
flat seal, photometric script/input identities, original qualified result
payloads and complete same-grid calibration control cases. Its new freeze
captures exact source, input and model settings before qualification/force
work. New publications use the existing atomic no-overwrite result helper.

No preflight blocker was found. The experiment is a post-exposure, fixed-plane,
retained-emission source/representation sensitivity with an adopted common
law. Holding the old velocity table fixed does not make it a joint HALOGAS
source/tracer/warp reconstruction. Both outcomes and the lost-mask/exterior
ledger must remain visible regardless of whether either residual improves.
This preflight does not claim that the unrun numerical checks have passed,
that the density is unique, or that native UNT gravity has been derived.
