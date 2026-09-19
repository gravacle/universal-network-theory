# Stage-3 A20/A21/A22 production-entry adapter

Repository-wide source search found consumers and validators for A20, A21, and
the two prelaunch A22 authorization records, but no executable publisher for
those four records.  The frozen `production_dual_l12_launcher.py` begins by
opening them and therefore cannot create them.

`stage3_entry_adapter.py` is the minimum nonphysical bridge.  It retains the
exact A18 cross-gate, both frozen consumers, and both L12 cache manifests;
checks the A18 path/hash/record bindings; captures current macOS memory and
workspace disk state through retained parent descriptors; constructs and
publishes A20; reconstructs A21 from the retained canonical A20 raw bytes in
the separate `independent_a20_auditor.py`; retains canonical A21 before it
constructs the two one-way A22 authorizations; and passes every record through
the frozen coordinator and production obligation validators.

The packet also carries the exact patched-launcher candidate.  That launcher
cannot execute directly: its physical entry requires the adapter's retained
destination-parent guard.  The guard performs exact name censuses immediately
before handshake and release and supplies all live filesystem/free-disk
samples from held descriptors.

Modes:

- `fixture`: deterministic in-memory construction only.
- `dry-run`: real stable-descriptor inputs and live resources, no publication.
- `publish`: owner-once A20, A21, target-A22, hostile-A22 publication only.
- `launch`: launch only through the authenticated retained-parent guard after
  the four canonical entry records exist.

Only `launch` can launch workers; the adapter itself contains no physics.
Publication is unavailable unless L12 workspaces, L12 outputs, and telemetry
are absent.  A failure after any owner-once commit leaves durable partial
evidence.  A retry resumes only when every existing predecessor is the exact
expected, fresh canonical byte string; mismatch and stale evidence are
preserved and refused.  No mode deletes or replaces a canonical name.

Run the bounded hostile checks with:

```sh
python3 -B test_stage3_entry_adapter.py
```

The live memory capture uses `/usr/bin/memory_pressure -Q`.  Because that tool
reports an integer free percentage, the adapter subtracts one full percentage
point before converting to available bytes.  This is deliberately one-way:
rounding can reject a viable launch but cannot admit a threshold-edge launch.

Claim boundary: executable Stage-3 entry and guarded-launch control only.  At
freeze time no A20-A22 record has been published, no worker has been launched,
and no L12, spectrum, continuum, or gravity result is asserted.
