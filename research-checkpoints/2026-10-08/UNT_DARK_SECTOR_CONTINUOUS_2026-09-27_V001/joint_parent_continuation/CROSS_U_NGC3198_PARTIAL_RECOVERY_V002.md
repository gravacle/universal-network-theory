# Recover the unfinished disk solves with inexact Newton V002

2026-10-06 UTC. Numerical recovery, with no change to S_cross physics,
P(X), grid, quadrature, ordinary source, epsilon, boundary or observable.
V001 source ae4285fc9c19cdf2d8efa176ac3d770b7eaf379a75fa3b9627bc9d3f6f3179e1
is preserved. This worker may launch only AFTER V001's natural completion
and authenticated final receipt; there is no competing execution owner.
All V001 completed cases are copied rather than repeated. All failures,
partial directions, accepted fields, checkpoint commits and histories remain.

V001 asked for inner residual.001 before its first Newton step. Its first
closed cases stopped at600 iterations with unfinished relative residuals
around.2. Those are numerical failures, not physical exclusions. Recover
their exact accepted field and saved whitened Newton direction after
checking the parent receipt, every output hash, NPZ commit and identity.
Recompute the actual residual, current preconditioner and true partial
direction residual. Keep the entire old history as ancestry.

Use fixed inexact forcing eta=min(.5,max(1e-6,.5sqrt(current error))). If an
authenticated partial direction satisfies that true inner target, use it
directly; otherwise solve the remaining correction from that direction.
This recovers completed linear work rather than replaying the old solve.
The stored failed direction is in symmetric-preconditioned coordinates;
divide by the current sqrt(diagonal) only when proposing a physical step.
BiCGSTAB permits an indefinite operator, without regularizing it. Its new
correction remains capped at600 iterations. With eta<=.5, the actual
weighted residual directional derivative is negative regardless of
Hessian definiteness. The same32-step domain/Armijo backtracking tests the
full nonlinear residual before accepting any proposed field.

Allow40 recovery Newton updates, require the SAME final residual1e-8,
and preserve state/history after every accepted step. Preserve a newly
unfinished linear direction on failure. Retain all16 outcomes, including
failed cases and all43 measurement rows. Copy no old field diagnostic as
if it described a changed field. This script reports the actual recovered
curve and residual; post-solve stability/weak-metric/source envelopes and
spatial/modal/integration/outer checks are subsequent useful work.
All physical qualification flags remain false. Any unresolved case gives
explicit failed-batch status and exit3. A fixed iteration allowance or
finite positive sampled curvature is not physical success.

Source/protocol must be reviewed and sealed before root execution. No
agent scientific execution, overwrite, automatic resume, Goal, heartbeat
or self-submission. This is the existing scientific continuation, not a
new coordination framework. The original18459 coefficient worker is
preserved. Both workers and exact next action remain recorded in the
existing continuation log while active.
