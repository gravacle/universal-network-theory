# Owner-once carrier-marginal closure verification protocol V001

Date: 2026-09-22

Status: `FROZEN_CANDIDATE__PRE_HOSTILE_OUTPUT`

## 1. Question

Test the exact theorem in [`THEOREM.md`](THEOREM.md) against two separately
written finite implementations.  The target and hostile calculations must
compare:

1. the full joint lineage--carrier evolution of the frozen owner-once
   accumulation model; and
2. the same carrier ladder evolved with the matched channel

   ```text
   K0 = P_occupied + cos(phi) P_blank
   K1 = -i sin(phi) a_event^dagger P_blank,
   ```

   with the channel's environmental outcome unread by future dynamics.

The closed ladder without `K0/K1` is not the matched null.

## 2. Required sizes and chronology

`L=4` and `L=6` are mandatory complete finite controls.  `L=8` may be added
as a supplemental scalable control but cannot rescue a failure at L4 or L6.
Each size begins with blank carriers and the declared loaded active cycle,
applies events `0,...,L-1` exactly once, and stops before a revisit.

The transport dwell, graph, admission angle, Taylor order, and substep count
must be common within each full/reduced comparison and recorded in its result.
The default finite target control uses `phi=pi/4`, dwell `pi/2`, Taylor order
12, and 16 transport substeps.

## 3. Mandatory comparisons

At initialization and after every admission and transport, report where
applicable:

- prefix freshness probability at the next event;
- purification or factor residual;
- reduced-carrier Hilbert--Schmidt residual;
- explicit reduced-state trace distance at L4;
- sharp-`q` sector-weight disagreement;
- site-occupation disagreement;
- instantaneous oriented-current disagreement;
- actual integrated-current disagreement;
- null integrated-current disagreement; and
- actual-minus-null integrated-current disagreement.

Common numerical evolution error and full-versus-reduced disagreement must be
reported separately.  A common norm drift is not a model discrepancy.

## 4. Frozen pass conditions

For each mandatory size:

```text
maximum full-versus-reduced disagreement <= 2e-10
maximum absolute norm/control error       <= 2e-10
fresh-lineage probability                 <= 2e-10
```

Every required event and required observable must be present.  A missing,
nonfinite, or silently clipped value fails the implementation.  L4 explicit
trace distance is required; a purification or Gram-factor bound may replace
the dense trace calculation above L4.

## 5. Independence requirement

The hostile implementation may read the frozen historical protocol and
theorem but must not import target verifier modules, matrices, basis maps, or
result values.  It must use independently written basis ordering, admission,
transport, partial-trace/reduction, and current logic.  Source hashes and all
runtime parameters must be recorded in deterministic JSON without host names,
timestamps, or absolute paths.

The target implementation may import the historical seed engine as the joint
side of its comparison, but its reduced carrier channel must be independently
implemented.

## 6. Disposition

Only agreement of the analytic proof, the finite target, and the hostile
implementation permits

```text
PASS_EXACT_OWNER_ONCE_CARRIER_MARGINAL_CLOSURE__FINITE_ACCUMULATION_SCOPE_ONLY
```

Any disagreement returns

```text
OWNER_ONCE_CARRIER_MARGINAL_CLOSURE_REJECTED_OR_UNRESOLVED
```

No tolerance may be changed after hostile output is opened.  A pass establishes
the correct lineage-erased comparator for the frozen accumulation engine.  It
does not establish a thermodynamic limit, remove joint lineage observables, or
decide any record-reading parent elsewhere in the repository.
