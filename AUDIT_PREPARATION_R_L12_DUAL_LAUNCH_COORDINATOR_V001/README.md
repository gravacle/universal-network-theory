# V012 dual-launch coordinator and synthetic audit fixture

This packet is a standalone, non-operational integration contract for the
V012 target/hostile L12 launch boundary. It fixes the causal ordering that a
schedule containing already-observed launch epochs cannot establish.

The modeled order is:

1. admit a current readiness/resource schedule with `NORMAL` pressure;
2. admit an independent audit of that schedule;
3. admit target and hostile one-way L12 authorizations in either sibling order;
4. authenticate the two sibling worker-generated READY records (each binds a
   retained process handle, kernel start token, executable hash, private
   inherited control channel, and worker-held nonce commitment) and commit
   them in one immutable V002 handshake;
5. issue a non-circular release artifact and exact per-worker release commands;
6. admit both worker nonce-reveal ACKs in either sibling order;
7. after each validated owner-once history publication, admit its authenticated
   worker COMPLETION frame while that exact process remains live and blocked on
   coordinator EOF; and
8. admit postrun telemetry binding the schedule, audit, both authorization
   hashes, handshake, release, launch/completion epochs, limits, output paths,
   and output hashes. Ordered per-role runtime and shared-disk samples must
   are collected at no more than 30-second launcher intervals (and refused by
   the coordinator above 60 seconds) and reconstruct observed RSS. The RSS
   peak is explicitly a sampled-current-RSS maximum, not an OS high-water
   measurement. The separately labelled mapped peak is the conservative authenticated
   cache certificate, not an OS virtual-memory observation.

The pure coordinator deliberately performs no filesystem access, process launch,
cache construction, gate creation, history creation, physics, or final
adjudication. `production_dual_l12_launcher.py` is the bounded production
adapter: it provides retained parent/file-descriptor custody with exact
chunked reads and post-hash identity checks, two private inherited sockets,
owner-once evidence publication, exact-PID/start-token cleanup, and live
RSS/disk telemetry with immediate resource refusal and a monotonic six-hour
deadline. It releases the real worker barrier only after
`release_workers` returns.

## Integration interface

Construct `DualLaunchCoordinator(policy, evaluation_epoch)` and call:

```text
admit_schedule(record) -> schedule_sha256
admit_schedule_audit(record) -> audit_sha256
admit_authorization(target_record) -> target_authorization_sha256
admit_authorization(hostile_record) -> hostile_authorization_sha256
commit_handshake(record) -> handshake_sha256
release_workers(record) -> ReleaseDecision
release_command(role) -> canonical release command
admit_release_ack(command, record) -> release_ack_sha256
admit_worker_completion(record) -> worker_completion_sha256
admit_postrun_telemetry(record) -> telemetry_sha256
```

Both authorization records bind the schedule and audit hashes but contain no
handshake or release hash, preserving one-way authorization. The handshake
binds both authorization hashes, exactly two distinct worker identities,
exact canonical executable/workspace paths, readiness epochs, `NORMAL`
pressure, and an observed readiness skew no greater than 60 seconds. The
release binds that immutable handshake and reconstructs actual release skew.
An ACK proves possession of the pre-handshake nonce on the same inherited
channel and binds the exact release command.  Telemetry is impossible until
both ACKs and both live terminal COMPLETION frames have been accepted.

Run the bounded independent checks with:

```sh
python3 -m unittest -v test_dual_launch_coordinator.py
python3 -m unittest -v test_production_dual_l12_launcher.py
```

The suite executes all eight exact topological orders: the two authorization
orders, two ACK orders, and two completion orders.  It also applies every
public action at every canonical boundary and proves every invalid attempt is a
controlled non-mutating refusal.  Separate mutations delete or swap an ACK,
corrupt a nonce, bypass a stage, or alter completion identity/output binding.
This is a stronger identity barrier, not widened authorization.
