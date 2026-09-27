# L4--L8 autonomous lineage-sensitive scaling target protocol V001

Date frozen: 2026-09-27

Status: `TARGET_IMPLEMENTATION_FROZEN__L4_ONLY__L6_L8_PROHIBITED`

## 1. Prospective finite question

For each authorized finite size, begin at the completed owner-once terminal
checkpoint, symmetrically dephase both arms across sharp carrier-number
sectors, and compare the retained joint lineage--carrier state with the
same-sector product of its complete quantum marginals.  Apply one reversible
revisit admission and the unchanged carrier transport.  Does the carrier
state distinguish the two arms?

The eventual all-event schedule treats every label `e=0,...,L-1` as an
independent revisit from the same terminal checkpoint.  Revisit events are
not applied sequentially.  In this packet only `(L,e)=(4,0)` may execute.

## 2. Frozen migrated inputs and relocation

The source histories are the tracked V012 L4/L6/L8 histories.  Their retained
`terminal_shards` are actually sharp preterminal `H_(L-1)` q-shards.  All 18
shards are ignored computational custody whose exact shape, byte count, and
SHA-256 are bound by those histories.

Historical paths beginning

```text
/Users/brianmulconrey/PerInfo/where-atoms-come-from/audited-386ee2c/
```

remain provenance and are never rewritten.  The runtime requires the exact
expected suffix

```text
DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/WORKSPACES/
L{L}/sharp/prefix_{L-1}/q_{q}.npy
```

under the current repository root.  It rejects any different historical
string, duplicate/missing q, traversal, symlink, path outside the root,
wrong hash, byte count, shape, `complex128` dtype, or non-C array order.  It
hashes each shard before and after copying its contents.

The absent `CACHE_PAYLOADS_V012` directories are not inputs to this packet.
No historical file is modified.

## 3. Terminal-sector reconstruction

For a requested terminal carrier sector `q`, reconstruct the final admission
from preterminal sectors `q` and `q-1` using the frozen owner-once ordering and
`phi=pi/4`.  The stay branch has the original blocked-state convention; the
forward branch maps the final lineage and carrier bits from zero to one.
Apply the authenticated target V004 fine transport to the resulting amplitude
matrix `Psi_q`.

The L4 terminal reconstruction must reproduce the registered dense route
through the downstream response observables.  The L6/L8 reconstruction
interface exists but its executable entry point remains locked.

## 4. Actual and same-q-product arms

For every terminal block,

```text
rho_A = direct_sum_q |Psi_q><Psi_q|,
rho_P = direct_sum_q rhoS_q tensor rhoC_q / p_q.
```

Both arms therefore remove cross-q coherence, retain all within-q quantum
coherence, and have identical complete lineage marginal, complete carrier
marginal, and q weights before the revisit.

The actual branch applies the joint reversible admission directly to each
`Psi_q`.  For the product branch, tracing the lineage after a one-event
admission depends exactly on the reduced event-bit state of `rhoS_q/p_q`.
Fixed q makes that one-bit state diagonal.  Its two probabilities define at
most four carrier Kraus factors applied to the factor `Psi_q^T` of `rhoC_q`.
This is an exact rewriting of the frozen product state, not a diagonal sham.

## 5. Signed low-rank readout

After merging all input contributions into output carrier-number sector `r`,
write

```text
sigma_A,r = F_A,r F_A,r^dagger,
sigma_P,r = F_P,r F_P,r^dagger,
Delta_r   = Z_r J_r Z_r^dagger,
Z_r       = [F_A,r, F_P,r],
J_r       = diag(+I,-I).
```

Use thin QR, `Z_r=Q_r R_r`.  The nonzero eigenvalues of `Delta_r` are those
of the reduced Hermitian matrix `R_r J_r R_r^dagger`.  The trace-distance
contribution is one half the sum of their absolute values.  No full carrier
density matrix is formed.

Configuration probabilities are factor row norms.  Number-sector weights,
all signed site occupations, configuration TV, number-sector TV, occupation
RMS, and trace distance add across the orthogonal output number sectors.
Trace distance before and after common carrier transport must agree.

## 6. Checkpoint and publication contract

One task is `(L,event,resolution,q_out,branch)`.  V001 creates the five
`L4/event0/fine/target` tasks in deterministic q order with one worker.  It
reuses the authenticated `ResumableProcessPool` and durable-evidence modules.
The canonical runtime module name is retained so macOS spawn can authenticate
and unpickle it in child processes.

The run identity binds the task plan, parameters, kernel path/hash, engine
hash, history hash, dense-baseline hash, and branch/phase.  Task JSON is
immutable and authenticated on resume.  A changed plan requires refusal.
SIGINT/SIGTERM stops before final publication and recovery requires explicit
`--resume`.  The final result is an immutable, fsynced, atomic owner-once
publication.  Partial arrays are never interpreted as final output.

The preserved `L4_EVENT00_TARGET_V001` attempt stopped before its first task
because an initial wrapper loaded the runtime under a non-importable temporary
module alias.  Its identity and failure journal are retained; no physical
sector result or final output was produced.  The source-corrected owner-once
run uses `L4_EVENT00_TARGET_V001R1`.

## 7. L4 acceptance gate

Synthetic tests must first show:

1. reduced QR trace distance and configuration TV agree with explicit density
   matrices, including dependent columns and a zero-difference control;
2. actual and same-q-product admission factors agree with explicit joint
   density evolution and partial trace; and
3. all 18 L4/L6/L8 retained shards authenticate while L6/L8 execution is
   rejected.

The L4 physical gate then requires:

```text
maximum difference from every registered dense fine observable <= 5e-12
QR reconstruction, reduced Hermiticity, eigen/trace residual    <= 1e-11
trace-distance common-transport invariance                       <= 1e-11
actual/product trace error                                       <= 1e-11
TV contraction controls                                          <= 1e-11
all values finite; normalized observables in [0,1] (+1e-12)
warnings and floating-point invalid/divide/overflow events        zero
```

Pass classification is `PASS_DENSE_L4_TARGET_REPRODUCTION`.  Any failed
authentication, convergence, warning, nonfinite value, or control prevents
final publication.

## 8. Locked later stages

L6 and L8 are not automatically authorized by an L4 target pass.  They remain
locked until all of the following exist: dense L4 pass, separately frozen
independent hostile/audit agreement, deliberate interruption/resume
equivalence, and a reviewed benchmark with ETA, peak RSS, disk, and power
window.  L6 must precede L8 and revise the L8 estimate.

The L8 curvature response adapter is not emitted by this packet.  A later
version may emit it only after complete target/audit all-event agreement and
an exact canonical-JSON contract.

## 9. Claim ceiling

This is finite target-side numerical machinery.  An L4 pass reproduces a
known one-size mechanism and nothing more.  Later finite results, if
authorized, can establish only their frozen finite response values.  No
result here proves a scaling law, thermodynamic persistence, curvature,
geometry, continuum physics, dark matter, dark energy, or gravity.
