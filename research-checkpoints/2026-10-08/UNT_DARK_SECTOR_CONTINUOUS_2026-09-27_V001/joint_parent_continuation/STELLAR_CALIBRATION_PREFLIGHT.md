# Independent preflight: one fixed stellar-calibration substitution

2026-09-28. Read `stellar_calibration_compute.py`,
`STELLAR_CALIBRATION_PROTOCOL.md`, the preceding design, and the actual
saved ring-component schema. No module was imported or numerical worker
executed by this preflight. **Accepted: no blocking mathematical or
source-consistency defect found.**

## Source and physical comparison

The code reads the exact externally specified calibration scalar, checks
its arithmetic and source/input hashes, and constructs a fresh stellar
profile. Its core and tail are scaled along with its measured interior;
the original arrays are not mutated. Both gas profiles, their tails,
helium factors, distance, geometry, law and physical acceleration scale
remain unchanged. This is not a new SPARC radial-profile substitution.

The same new component list supplies the exact annular bottom flux,
component masses, total-mass monopole boundaries, and initial monopole.
The boundary tangential gradients use the appropriate nonlinear or
Newtonian inverse for that new mass. No old-mass boundary remains paired
with the new source. The source-scaling check verifies unchanged gas mass
and the prescribed stellar factor before scientific acceptance.

No new normalization is inferred from the observed velocities. Every new
case is compared with its original HI1/H21 case at exactly the same grid,
domain and equation, retaining signed force, signed velocity squared and
all observed rows. Negative-force cases remain explicit; summaries do not
manufacture real speeds from their magnitudes. Empty real-speed subsets
and missing real paired speeds are handled without invalid JSON.

The interpretation is appropriately narrow: a fixed conversion-convention
sensitivity test on already exposed data, not a measurement of the true
stellar M/L or independent validation of a native network gravity law.

## Newtonian reference and nonlinear qualification

All fields in each saved ring component are linear in that component's
mass density. Scaling its potential, radial force, integrated mass and
omitted mass by the stellar multiplier is therefore exact arithmetic for
the same original quadrature. Gas components remain unchanged. Recombining
each height/order before the two linear extrapolations preserves their
meaning. The original signed components, including outward forces, are
not replaced by absolute values.

The force-tail bound scales with the new total omitted mass and keeps
`G*M_omitted/(cutoff-R)^2`; all five radii satisfy its geometric premise.
The same original order, height and mass-closure tolerances are retained.
The recombined oracle is independent of the finite-volume implementation,
but correctly is not described as a new independent quadrature or datum.

The three new nonlinear grids reproduce the original source-specific
domain/refinement test. Both variations compare against the **new** coarse
source case. The fourth case supplies the new-source Newtonian field and
is checked at all five recalibrated oracle radii. No componentwise
superposition is used for the nonlinear field.

The final sheet reconstruction uses the new same-domain nonlinear and
Newtonian cases, reusing the already reviewed algebraic helpers. Its
source flux, monopole reference, four signed terms and closure checks
are all formed from the new source. All profiles have continuous tails,
so its absence of a hard-truncation warning is correct. This diagnostic
does not independently certify a vertical-field measurement.

## Custody and restart

Input validation requires all16 original cases, their frozen source
ancestry, exact model/grid/equation identities, payload hashes and original
pass flags. The inherited stretched qualification and ring ancestry are
verified; relevant files are included in the new manifest. The calibration
script and both data inputs are checked against its retained JSON identities,
and the scalar is checked against the specified published conversion.

New case names, freeze, recombined oracle and final result are distinct from
all original paths. Exclusive atomic result publication preserves previous
outputs. Rolling checkpoints use the actual inherited authenticated
writer/reader with the new case identity and freeze hash. Completed outer
history is retained and counts against the unchanged total allowance.
No monkey-patching, automatic tolerance change or failed-case replacement
is introduced.

The author addressed the sole completeness suggestion before freeze:
the recombined oracle now retains both its force-tail bound and the
corresponding `G*M_omitted/(cutoff-R)` potential-tail bound. The added
expression was independently re-read and is correct. No scientific
threshold or force calculation changed; no outstanding preflight issue
remains.
