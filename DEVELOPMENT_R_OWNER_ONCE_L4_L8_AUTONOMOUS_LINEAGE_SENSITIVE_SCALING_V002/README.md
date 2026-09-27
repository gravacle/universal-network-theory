# L4 hardened restart successor V002

Date: 2026-09-27. Disposition: `PASS_L4_HARDENED_RESTART_AND_DENSE_REPRODUCTION__L6_L8_LOCKED`.

This packet changes checkpoint custody, not the V001 scientific calculation.
The V001 L4 kernel, frozen engine, baseline, history, and retained shards are
authenticated before use. A small execution adapter permits the unchanged
scientific kernel to run from a descendant integration commit while preserving
the frozen parent commit/tree and exact dependency hashes. The adapter's own
hash is bound in the task identity and sector receipts. The preterminal shard
paths remain repository-relative at runtime; the historical absolute path is
preserved as provenance.

The accepted run is `CHECKPOINTS/L4_EVENT00_TARGET_V002R3` and
`PHYSICAL_OUTPUTS/L4_TARGET_REPRODUCTION_V002R3.json`. All five q-sector
results and receipts are individually immutable. `RUN_IDENTITY.json` binds
source, parameters, tasks, and exact kernel bytes. Each result's strict outer
and scientific schema is checked; receipts bind raw bytes and the scientific
projection; the append-only journal binds each committed hash; `COMPLETE.json`
binds ordered result and receipt sets. The final L4 aggregate is reconstructed
from these checked sectors. The R3 registered result and sector scientific
payloads are exactly equal to the sealed V001 dense target result. Dense
reproduction maximum absolute difference remains `9.992007221626409e-16`.
Measured R3 wall time was `1.025244` seconds and maximum observed RSS was
`34,947,072` bytes; its checkpoint footprint was `23,390` bytes. These are
local L4 measurements, not L6/L8 or remote forecasts. Power was not metered.

The `test_hardened_runtime.py` suite passed 15/15 on disposable copies of R3.
It includes changed configuration/identity and corrupted content
refusals, recovery from a missing `RUN_BOUND`, result-only and result+receipt
unjournaled crash windows, and a missing final completion-journal event. It
also used a durable `Q4_STARTED` marker to deliver SIGTERM during the final
in-flight task after four commits: exit 75, no `COMPLETE`, and no final marker.
Explicit resume completed, with all five scientific sectors equal to an
uninterrupted control. A result without journal authority is replayed and
compared scientifically before recovery; a replay mismatch refuses. Local
advisory locking enforces one controller per checkpoint root. An existing
final output can be accepted only after full checkpoint verification and
reconstruction on explicit `--resume`.

R1 and R2 in this packet are retained as superseded development attempts. R1
predated strict journal/crash-window checks. R2 passed its then-current dense
run but its source hash was superseded by a later kernel-authentication fix.
Neither is the accepted restart gate; do not overwrite or promote them.

Commands from the repository root:

```text
python3 -B DEVELOPMENT_R_OWNER_ONCE_L4_L8_AUTONOMOUS_LINEAGE_SENSITIVE_SCALING_V002/test_hardened_runtime.py
python3 -B DEVELOPMENT_R_OWNER_ONCE_L4_L8_AUTONOMOUS_LINEAGE_SENSITIVE_SCALING_V002/verify_packet.py
python3 -B DEVELOPMENT_R_OWNER_ONCE_L4_L8_AUTONOMOUS_LINEAGE_SENSITIVE_SCALING_V002/run_l4_v002.py --resume
```

This is deliberately L4-only. L6/L8 remain hard-locked in V001. A future
long-run successor must qualify remote execution, a pinned numerical
environment, process-tree memory/power bounds, and interruptible long replay
before L6 production. The V002 replay path waits for one L4 sector to finish
and is not itself proof of responsive cancellation of a multi-hour recovery
task. Its absolute kernel pathname in `RUN_IDENTITY` requires the same remote
path for a copied checkpoint; fresh remote execution and same-path remote
restarts are possible only after the separate SSH contract gates pass. No
remote run, scaling persistence, L8 curvature, geometry, or gravity claim is
made here.
