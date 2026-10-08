# Fixed stellar-calibration comparison V001

This additive, post-exposure experiment implements
`STELLAR_CALIBRATION_TEST_DESIGN.md`. It changes one source convention, not the
gravity law or a fitted parameter. All original 16 cases must exist, authenticate
and pass their original numerical checks before even this experiment's freeze.
No original source, result, checkpoint or freeze is replaced.

## Frozen source and cases

Identity: `ML36_CAL_HI1_H21_V001`. Read the exact scalar
`1.2567828155112788` from the retained photometric comparison JSON; verify its
script/input hashes and its published-convention arithmetic. Scale a fresh
copy of the full Leroy stellar profile, including flat core and exponential
tail, by this scalar. Both gas tails remain on and all gas densities are
unchanged. Keep the original geometry, distance, law, `a0`, and shape parameter.
No inclination correction, radial profile substitution, density fitting or
velocity fitting is performed. Numerical digits of the scalar do not imply
that precision in the published coefficient 280.

Run exactly these four jobs, in this order:

| N | domain extent (kpc) | equation |
|---:|---:|---|
| 256 | 255 | original nonlinear law |
| 320 | 1023 | original nonlinear law |
| 512 | 255 | original nonlinear law |
| 512 | 255 | Newtonian |

Case names begin with the new source identity and include N, extent and
Newtonian flag. Use the original immutable mesh/operator, V002 solver,
boundary quadrature, exact density integral, observations reader and
authenticated checkpoint helpers. The original runner's `main` and
hard-coded source factory are not invoked or monkey-patched. The changed
component list supplies *both* bottom annular flux and all component/total
masses; every outer boundary and starting monopole uses this new total mass.

The baseline starts from the same kind of smooth monopole guess as the original
experiment, not a velocity-informed or rescaled numerical solution. Save a
rolling case-local checkpoint after every completed outer update, with the
new freeze and case identity plus field/history hashes. Resume authenticates
these values, retains the completed history, and inherits the total 300-outer
iteration allowance. A completed case is authenticated and reused, not rerun.
Failures remain published and stop this frozen attempt; no automatic tolerance
change, initial-condition search or failed-case overwrite occurs.

## Independent Newtonian reference

Authenticate the existing qualified ring result and its ancestors. Retain its
five radii, three heights and both orders. For every stored height/order form
the exact component-linear combination
`g_new=g_old+(c-1)g_star`; likewise for the potential and component/missing
masses. Then form both original linear-height extrapolations. This is reuse
of an independent-of-FV implementation, not a freshly independent quadrature.

Publish this compact recombined oracle separately before the field jobs, with
its source-freeze hash. Retain all heights/orders, signed values, both
extrapolations, omitted-tail bounds and the original numerical criteria:
48/96 differences `<=1e-8 * max(1,abs(reference))`, height-extrapolation change
`<=1e-3` on the same scale, component mass closure `<=1e-9` relative, and tail
force bound `<=1e-10` relative to `max(1,abs(reference))`.

The new N512 Newtonian curve must agree at all five radii within
`0.02*max(1,abs(oracle)) + abs(extrap_fine-extrap_coarse)
+ abs(last_height_order96-last_height_order48)` in `(km/s)^2/kpc`. Exterior
rings' outward forces must stay signed. The oracle's unchanged `R<cutoff`
limitation is harmless here; it is not used as an outer boundary.

## Numerical qualification and readouts

Use the original numerical criteria unchanged: convergence, relative source
mass error `<=1e-13`, flux balance `<=2e-6`, actual nonlinear residual `<=1e-9`,
zero clipped faces, and `<2%` mesh/domain force change at the existing comparison
radii `R>=2 kpc`. Both refinement and remote-domain cases compare with the
new-source N256/L255 baseline. The physical source-scaling ledger must match
the old gas masses and `c` times the old stellar mass within `1e-13` relative.

Retain all 43 observed rows, signed force, signed velocity squared, real speed
where available, errors and residuals. Pair each with the original HI1/H21
case at exactly the same grid/domain/equation. Report all signed changes and
the inherited `R>=0,2,8 kpc` descriptive summaries. The nominal sum of squared
quoted-error units is not a fitted likelihood or a scientific acceptance gate.

After all four cases qualify, use the new-source N512/L255 nonlinear and
Newtonian pair for the already defined sheet-jump/solenoidal diagnostics.
Reuse the immutable algebraic helpers from `disk_response_diagnostic.py`, not
its original-model `main`. Preserve all 43 rows and the four signed force and
velocity-squared terms from `DISK_RESPONSE_DIAGNOSTIC.md`, with closure checks
at `1e-11*max(1,scale)`. Reconstructing the vertical component is a boundary
condition inference, not an independent vertical measurement. The remaining
field term includes finite-boundary and numerical effects. No fit or additional
PDE is hidden in this postprocessing.

## Custody and execution boundary

The additive source manifest includes this protocol, design, implementation,
photometric JSON/script/audit, all imported modules, diagnostic definitions,
all inherited source/solver/ring dependencies and qualified benchmark files,
and all 16 complete original case files. Authentication checks the nested
freeze manifests and payloads before publishing this freeze. New outputs are
exclusive atomic publications linked to this freeze and canonical payload
hashes; only the exact new rolling checkpoint can be replaced on progress.

Single-thread numerical libraries and the existing one-worker workflow remain.
The script is inert until explicit `freeze` or run. Root reviews/freezes/runs
after the original queue finishes; this implementation has not been executed.
There is no observational-success gate and no search over source conventions.
The result tests this fixed source sensitivity, not which M/L nature chooses
and not an independently derived native UNT gravity interface.
