# L14 Targeted Scout V003 — clean-run execution repair

V003 is an isolated execution successor to V002. It does not modify V001/V002,
the frozen L12 workspaces, Stage-6R2, the topology sidecar, Stage-6R3, or any
frozen numerical source.

## What V003 adds

- Task-level owner-once result commits with SHA-256 authentication and directory fsync.
- Resume binding to the exact run ID, branch, phase, kernel bytes, parameters, task IDs, payload hashes, and work weights.
- Graceful SIGINT/SIGTERM behavior: stop submitting work, allow active tasks to commit, then return a resumable status.
- Target/Hostile independence with no fail-fast sibling termination.
- Exact target/hostile merge rules: identical atom census, q assignments, intervals, and sector masses; all original numerical predicates must be true.
- Owner-once Phase-2 authorization before q8/q9 can run.
- An AWS no-compute CloudFormation stack, retained encrypted checkpoint EBS, disposable maximum-performance gp3 scratch, versioned S3 evidence, SSM-only administration, and a cross-restart runtime ledger.
- A retained-EBS runtime observer that emits a durable advisory at 835 minutes and never stops computation or powers off an instance.
- A complete q0-q14 capacity certificate and deterministic q-aware concurrency; the numerical method, sectors, tolerances, and reduction order are unchanged.
- L14 execution overrides that remove inherited row-window, RSS, and wall-clock rejection predicates while retaining their telemetry.
- A dependency-closed source bundle contract: exact kernel dependencies, preserved predecessor sources and Stage-6R2 input, the regression report, a portable CPython archive, and a hashed offline NumPy/mpmath wheelhouse are all authenticated before packaging and reverified after extraction.
- A scoped operator role created by the reviewed no-compute stack; the normal IAM user remains read-only and has no long-lived access key.
- Paid launch scripts that remain unusable until `launch_enabled=true`, an exact command-line authorization token, exact-kernel regression, live identity/quota/hardware/price/budget checks, and the staged Phase-1 record all pass.

## What V003 does not claim

The exact L14 ports extend only length-generic predecessor formulas and preserve every original numerical predicate; they do not claim an L14 result before computation. The Linux x86_64 regression and every source/runtime dependency are owner-once hash-bound in `KERNEL_BINDINGS_RELEASE_V003R3.json`. The earlier `KERNEL_BINDINGS.json` remains preserved as the pre-release fail-closed record. `package_source.py` and `readiness.py` fail closed if any release binding is absent or changed.

The files under `tests/` use `fixture_kernel.py`, which is visibly marked non-physics. Fixture output cannot satisfy the production binding.

## Key files

- `durable_evidence.py`: immutable publication and optional owner-once S3 mirror.
- `resumable_runtime.py`: bounded process pool and task-level resume.
- `branch_runner.py`: strict exact-kernel adapter.
- `merge_branches.py`: target/hostile authentication and merge.
- `scout_coordinator.py`: Phase 1 → gate → conditional Phase 3 → final report.
- `independent_launcher.py`: local two-branch non-fail-fast supervision.
- `readiness.py`: fail-closed local/online launch preflight.
- `package_source.py`: deterministic, regression-gated source bundle.
- `stack_parameters.py`: allocation-free, authenticated CloudFormation parameter generation; refuses unbound kernels/runtime.
- `aws/stage_assets.py`: owner-once no-compute publication of the authenticated bootstrap and source bundle, with stack/template/parameter verification and a local staging receipt.
- `AWS_SETUP_CHECKLIST.md`: the full account-to-teardown sequence.
- `EXACT_KERNEL_AUDIT.json`: the preserved pre-port static obstruction audit.
- `EXACT_KERNEL_AUDIT_R2.json`: the passing exact-port release audit and unchanged-physics claim boundary.
- `KERNEL_BINDINGS_RELEASE_V003R3.json`: owner-once production-runtime, kernel, predecessor, regression, and V003 execution-repair audit bindings.
- `capacity_plan.py`: allocation-free q0-q14 workspace and concurrency certificate; it is not a numerical-kernel binding.
- `AWS_DISCOVERY_SNAPSHOT.json`: read-only account, quota, hardware, network, AMI, price, and budget observations made during preparation.
- `PREP_TEST_REPORT.json`: mechanics-only test evidence and explicit exclusions.
- `PREP_SHA256SUMS`: checksum manifest for every prepared source, test, configuration, and evidence file.
- `aws/`: no-compute infrastructure, bundle/runtime verification, branch boot, dual runtime guards, staging, and explicitly gated paid launch tools.

## Local validation

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 -B readiness.py
```

The first command tests mechanics with fixtures. The second is expected to fail closed until the exact kernels, exact regression, AWS checks, and explicit launch flag all pass.

## Readiness boundary

The checked-in configuration remains deliberately **not launchable** because
`launch_enabled=false`; only an explicitly reviewed production copy may change
that field. AWS quota, hardware, and budget capacity never substitute for the
exact kernel/runtime binding, Linux regression, live preflight, or separate
paid-launch authorization.
