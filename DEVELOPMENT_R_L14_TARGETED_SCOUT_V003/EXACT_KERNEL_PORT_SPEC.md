# Exact L14 kernel port and regression specification

This document defines the remaining numerical work. It is not authorization to change a tolerance, predicate, or physics definition.

## Frozen inputs

Every file and SHA-256 in `SOURCE_LINEAGE.json` is read-only. The L14 implementation must be a successor package; it may import or copy pure length-independent kernels, but it must not edit the L12 sources or their evidence.

## Required Target kernel scope

1. Generalize target cache generation from the frozen V012 formulas to L=14 without reusing the V012 historical authorization gate.
2. Preserve basis ordering, carrier words, admission indices, lineage arrays, dtypes, edge orientation, row ordering, and exact source constants.
3. Execute event histories through event 14 with original actual/null convergence predicates and no boolean override.
4. Commit every independently complete numerical shard or reduction before marking its task complete. Scratch files may use local NVMe; any artifact referenced by a committed result must be under the retained checkpoint EBS root.
5. Produce q4–q9 probability masses and atom geometry built from histories L4, L6, L8, L10, L12, and L14.

## Required Hostile kernel scope

The Hostile implementation must be an independent derivation. It must preserve the V004R4/V003 basis and recurrence definitions, extend them to L=14, retain its original convergence criteria, and produce the blind geometry without importing Target numerical outputs.

## Task protocol

Each module bound in `KERNEL_BINDINGS.json` must export:

```python
build_task_plan(branch, phase, request, context) -> list[dict]
run_task(task_payload, context) -> dict
reduce_results(branch, phase, request, results, context) -> dict
```

`build_task_plan` must be deterministic. Each task has a stable `task_id`, JSON `payload`, and positive integer `work_units`. `run_task` must return a JSON object and list every committed artifact as `{path, sha256, bytes}`. `reduce_results` must be deterministic and return `L14_SCOUT_BRANCH_RESULT_V002`.

The bridge request computes atom geometry only for q4–q7, but its mass ledger must natively include q4–q9 so the early-stop upper bound is mathematical rather than estimated. The conditional request computes q8–q9 only after Phase-2 authorization.

## Exact production runtime

The binding must include a hashed, offline Linux x86_64 wheelhouse and a
`--require-hashes` requirements lock. The same Python and NumPy versions must
be used for the exact L4-L12 regression and the L14 AWS run. A regression
performed only against the macOS runtime cannot authenticate the production
binding. `package_source.py` must include the complete dependency closure;
`aws/verify_bundle.py` rehashes every extracted file and checks the live Python
and NumPy versions before either numerical branch starts.

## Required original numerical fields

Every branch result must make these predicates explicit and true:

- `all_actual_and_null_solvers_converged`
- `residual_l1_within_original_bound`
- `actual_norm_error_within_original_bound`
- `transport_number_drift_within_original_bound`
- `rough_sharp_agreement_within_original_bound`

The result must also preserve raw comparison scalars and thresholds in its evidence payload. Missing, unresolved, or non-finite values fail closed.

## Mandatory regression before binding

Run both new kernels at L4, L6, L8, L10, and L12 against the frozen engines. For every length compare:

- cache manifest census, shapes, dtypes, ordering, and SHA-256 where byte identity is expected;
- event-row census and event order;
- rough and sharp reductions;
- raw convergence values and predicate outcomes;
- reverse support probability, transport-node residual L1, actual norm error, and transport-number drift;
- sector masses, atom IDs, q labels, rational density intervals, z, and y;
- Target/Hostile agreement under the original exact or numerical comparison rule.

The regression report must enumerate every comparison, its rule, values, and result. “Close enough,” fixture parity, or a newly chosen tolerance is not a pass.

## L14 admission checks

Before production, the port must perform allocation-free census checks and refuse unless:

- the exact Phase-1 peak fits the selected memory and retained checkpoint capacity;
- Phase 3 cannot be opened without the owner-once authorization artifact;
- the branch has exclusive custody of its own workspace;
- the kernel, request, and task-plan hashes match the resume identity;
- the cumulative compute-minute guard has remaining capacity.

The V001 feasibility audit measured approximately 62.510 GiB for the q0–q7 Phase-1 admission window, 241.273 GiB through q9, and 345.810 GiB for the full exact history state. Those are admission facts, not permission to use an unvalidated reduced state.
