# Exact held-out L10/L12 joint lineage--carrier execution packet V001

Status: `FROZEN_PRE_HELDOUT_OUTPUT__READY_FOR_AUTHORIZED_EXACT_EXECUTION`

This packet freezes the exact execution and resource gate for Step 8 of the
owner-once lineage discriminator plan. It was created after the independently
reproduced L4/L6/L8 seed result and before any L10/L12 witness value was
computed or opened.

The packet:

- binds the four retained target/hostile L10/L12 prefix histories by history
  hash and complete terminal-shard manifest digest;
- preserves the original 60-GiB method freeze as historical authority;
- recognizes the later exact V003 prefix-lineage successor and its successful
  19,201,889,580-byte combined scratch certificate without rewriting the old
  rule;
- freezes terminal two-child reconstruction, rough/sharp comparison,
  target/hostile separation, sequential and concurrent schedules, resource
  telemetry, authorization guards, deterministic schemas, and fail-closed
  outcomes; and
- retains the parent witness equations, tolerances, statistic, and
  classifications without change.

No held-out scientific output belongs in this directory at freeze.

Files:

- [`PROTOCOL.md`](PROTOCOL.md) -- human-readable frozen protocol;
- [`INPUT_AND_RESOURCE_GATE.json`](INPUT_AND_RESOURCE_GATE.json) -- exact
  machine-readable inputs and resource arithmetic;
- `validate_heldout_gate.py` -- fail-closed validator; use
  `--full-shard-hash` for complete byte authentication;
- `test_validate_heldout_gate.py` -- protocol/gate tests; and
- `SOURCE_HASHES.sha256` -- sealed packet-source manifest.

Validation commands, run from the repository root:

```bash
python3 DEVELOPMENT_R_OWNER_ONCE_JOINT_LINEAGE_CARRIER_HELDOUT_EXECUTION_V001/validate_heldout_gate.py
python3 DEVELOPMENT_R_OWNER_ONCE_JOINT_LINEAGE_CARRIER_HELDOUT_EXECUTION_V001/validate_heldout_gate.py --full-shard-hash
python3 -m unittest -v DEVELOPMENT_R_OWNER_ONCE_JOINT_LINEAGE_CARRIER_HELDOUT_EXECUTION_V001/test_validate_heldout_gate.py
```

Successful validation authenticates readiness only. It does not authorize or
execute a witness calculation and does not read amplitudes as scientific
values.
