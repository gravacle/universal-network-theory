# L12 failed-launch custody and V002 retry plan

This DEVELOPMENT-only packet preserves the first Stage-3 launch attempt as a
failed control-plane event.  It authenticates exactly twelve immutable records
and logs, proves nine downstream artifacts absent, and reserves a disjoint V002
retry namespace.  The final target/hostile L12 workspace and history paths do
not change.

The primary obstruction is a path-generation mismatch: the hostile cache-build
authorization correctly retains historical target V012 hashes, but the hostile
worker attempted to resolve them at the newer active target paths.  The exact
historical records remain in the authenticated A18 retirement snapshot.  A
future adapter must route only that historical custody lookup to those retired
bytes; it may not substitute current hashes or change a physical operator.

The target process-start refusal is classified as a secondary peer-exit
cascade.  Its initial process-start authentication succeeded and its READY
record was published.  The later lookup failed only after the hostile peer had
already exited.

Run only:

```sh
python3 -B failed_launch_recovery_plan.py plan
python3 -B test_failed_launch_recovery_plan.py
```

No production mode exists.  This packet does not publish the future obstruction
record, implement/freeze the adapter, create retry records, launch a worker, or
create a workspace/history.  Those remain blocked on independent same-hash
review of future frozen bytes.
