# Independent helper preflight: fixed-source external transfer

Read-only code and analytical review, 2026-09-28. No module import, ring
calculation, field solve, target velocity lookup or source extraction performed.
AST parsing passed. Reviewed `fixed_source_transfer.py` SHA-256:

`6ee1ce726e096c9e96e66a40c9830c189e9e7f632c83b4d9f489009717df378c`.

**The reusable numerical helper is acceptable within the stated interface.**
The source-own caller and its complete freeze/qualification are not yet
implemented by this file and are not implicitly accepted here.

- The inherited field law, inverse, logarithmic mesh, V002 PCG/Picard operator,
  thin-disk flux normalization, derivative-based readout and numerical
  thresholds are unchanged. The conversion `q=GM/a0`, annular flux, monopole
  boundary derivative and `v²=R*a0*g` are dimensionally consistent. No observed
  velocity enters either the oracle or the field helper.
- The same declared components supply exact source mass, bottom flux, initial
  reference scale, outer boundary and independent signed Newtonian ring
  calculation. The oracle retains both quadrature orders, three decreasing
  heights, signed radial force, linear-height extrapolation and tail bounds.
  Its 2% field comparison includes the retained quadrature/height differences;
  it does not substitute an algebraic nonlinear response for a disk PDE.
- A case checkpoint binds field bytes, shape/dtype, full completed-outer
  history, case and freeze identity. Publication is atomic; resume validates
  that state and recomputes convergence. V002 charges resumed iterations to
  the same allowance. Failed completed cases are published with their failed
  checks, not overwritten as if successful. These are code-level findings;
  no new restart qualification run was performed here.
- Source-control radii are caller-owned and independent of target velocities.
  Five such radii do **not** qualify the whole radial curve. After the observed
  table is opened, every scored radius must be checked against coarse/fine
  and enlarged-domain saved arrays at the same unchanged 2% threshold. This
  requires only saved-field interpolation/arithmetic, not another PDE.

Necessary caller responsibilities, not additional user approvals:

1. Verify the transitive frozen law/operator/shape and numerical-qualification
   identities, actual source factory/data/geometry, oracle and case census.
   `authenticated()` validates a result envelope against a supplied digest;
   it does not itself verify every member of that freeze.
2. Bind the complete source shape. `qualified_masses` checks component masses
   only: equal masses do not identify equal radial densities. The caller's
   source freeze and density qualification must supply that missing identity.
3. Fix five finite, strictly increasing, distinct source-only control radii
   inside the supported mesh/source interval and away from source knots.
   This extra validation can be made in the helper or the caller before run.
4. Authenticate any already completed case before reuse, including exact
   model/N/extent/equation/radii/source identity and all its checks. Preserve
   nonconverged results and defer physical interpretation accordingly.

The initial guessed potential and fixed numerical box sizes are convergence
choices, not changes to source mass, response law, observational geometry or
physical force. No blocking mathematical or unit error was found in this
reviewed version. Subsequent code edits require a new recorded source hash.

## Addendum: pre-run radius validation and small I/O tests

The author added `validate_radii()` and calls it in both oracle and case
entry points. The five values must now be finite, positive, distinct and
strictly increasing. This directly closes responsibility 3 at helper level.
Reviewed updated helper SHA-256:
`c4df9cbab9228a405453571b2ab3cb26836c52ef6c142f15ba88cf7db6d8f08c`.

Read-only inspection of `test_fixed_source_transfer.py`, SHA-256
`9f860d8b14ba87da7129c99d827ed897a688c4231f9d0d186ccf6c090bb33ebf`,
confirms three focused tests cover invalid radius inputs, actual checkpoint
write/load/replacement and wrong case/freeze/shape refusals, and atomic
result publication/authentication/overwrite refusal. The parent reports all
three pass; this reviewer did not rerun them. They test I/O custody, not an
interrupted/resumed galaxy solve or source-factory qualification. No numerical
law/source/tolerance change or new mathematical blocker was found.
