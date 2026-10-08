# Additive prospective stretched-grid numerical repair V002

The first V001 large-domain case, N=256, L=128, eta=.01, stopped at its
first PCG allowance of 2148 iterations with residual approximately 9.05e-8.
It did not reach the unchanged 1e-12 linear target. Its failed case, nine
preceding passing near-domain cases, sources and freeze remain untouched.

This V002 changes only the linear numerical iteration allowance and verifies
acceptance against an explicitly recomputed residual. It imports the original
mesh, potential quadrature and finite-volume operator without modification.
The source, constitutive law, inherited r, geometry, initialization, Picard
damping and all scientific/convergence tolerances remain the same.

## Fixed repair

- Use the same diagonal preconditioner, but maximum PCG iterations are
  `32*N+100` instead of `8*N+100`.
- Accept a linear solution only if `||rhs-A*x||/||rhs|| <= 1e-12` from a
  fresh operator application, not solely the recursive residual vector.
- If the recurrence reaches that target but the true residual has not,
  replace the residual and restart the conjugate direction using the same
  preconditioner, within the same fixed total iteration allowance.
- Record recurrence error, number of true-residual checks, direction
  restarts, allowance and exit reason in each linear-step history. A failed
  solve is published as a failed case, never treated as a physical result.
- Keep maximum 300 Picard iterations, damping .6 (direct update for the
  Newtonian comparison), nonlinear residual1e-9, relative flux balance2e-6,
  zero clipped faces, and all prior boundary/source/force tests unchanged.

Rerun all thirteen original benchmark cases under V002 source identity:
N=64,128,256 and L=8 at eta=.01,1,100; N=256,L=128 at those same eta; and
Newtonian eta=1,N=128,L=8. Keep .5<=R<=4 scoring, successive near-domain
refinement improvement and finest/large-domain/Newtonian error below2%.
No original passing case substitutes for a V002 result.

`test_stretched_disk_v002.py freeze` creates a new exclusive
`STRETCHED_DISK_V002_FROZEN.json`. It hashes the new files, exact imported
operator/law and actual inherited shape result, and verifies every named
input of both earlier freezes. Results use the new `stretched_V002_` prefix
with atomic no-overwrite completed-case publication and the same verified
resume contract. Prior failures are neither overwritten nor relabelled.

The optional new `solve(...,checkpoint=callback,history_start=None)` hook
calls `callback(phi_copy,history_copy)` after each completed Picard update.
It performs no automatic checkpoint writes and is unused by these tiny
benchmarks. A future caller owns its source/input validation and durable
publication before reusing that potential as `initial` and its history as
`history_start`. Sequential completed outer indices are required; their
count is included in the 300-update allowance, and convergence is checked
again on the actual resumed field. No new crash-recovery qualification is
claimed here.

Only the root runs numerical workers. This prospective numerical repair
does not add a new physical equation, fitted parameter, observational
comparison or tolerance change. A successful rerun would qualify the same
large-domain discretization, not yet its boundary approximation on real data.
