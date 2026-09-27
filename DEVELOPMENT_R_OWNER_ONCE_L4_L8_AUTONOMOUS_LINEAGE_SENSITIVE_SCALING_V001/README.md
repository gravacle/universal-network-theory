# L4--L8 autonomous lineage-sensitive scaling target V001

Status: `PASS_DENSE_L4_TARGET_AND_RESUME_GATES__L6_L8_EXECUTION_LOCKED`

This packet implements the target half of the finite lineage-sensitive
response scaling program.  It reconstructs terminal sector amplitudes from
the authenticated target V012 retained sharp preterminal shards, constructs
the actual and same-`q` product arms as signed low-rank carrier factors, and
uses thin QR plus a reduced Hermitian eigensystem for trace distance.

V001 authorizes only the frozen `L=4`, event-zero dense-reproduction gate.
The code authenticates the `L=6` and `L=8` inputs but rejects every numerical
execution request at those lengths.  It does not create an audit packet,
curvature result, or L8 response adapter.

## Commands

```bash
python3 test_target_lineage_scaling.py -v
python3 target_lineage_scaling.py authenticate
python3 target_lineage_scaling.py run-l4
python3 target_lineage_scaling.py run-l4 --resume
python3 target_lineage_scaling.py verify-l4
python3 verify_packet.py
```

The completed real-process restart gate is implemented by
`resume_equivalence.py`; its owner-once evidence is under
`RESUME_EQUIVALENCE_V001R1`.  Re-running it against that same evidence root is
intentionally refused.

`run-l4` uses the authenticated resumable runtime with one output carrier
number sector as the checkpoint unit.  An interrupted run publishes no final
result; `--resume` is mandatory and accepts checkpoints only when the full
task/configuration/source/input identity still matches.

The ignored target cache payload directories were not migrated into this
clone and are not consumed.  The route uses committed engine code and the 18
history-sealed retained preterminal shards only.  Historical absolute paths
remain unchanged.  Runtime relocation accepts only the exact frozen suffix,
rejects symlinks and traversal, and checks hash, bytes, shape, dtype, and
array order before use.

## Registered L4 result

The source-corrected owner-once run completed all five q-sector checkpoints:

```text
classification                    PASS_DENSE_L4_TARGET_REPRODUCTION
wall                              0.903229917 s
maximum measured RSS              35,176,448 bytes
checkpoint storage                19,443 bytes
final result storage              15,210 bytes
dense registered-value max error  9.992007221626409e-16
```

The prior pre-physics import failure is preserved in `ATTEMPT_LOG.md`.  It
completed zero sectors and produced no physical output.

The deliberate restart gate also passes.  SIGTERM was sent after two immutable
sector results; the graceful stop retained three of five, published neither a
final result nor `COMPLETE`, and returned `75`.  Explicit resume produced all
five sector hashes and the canonical final hash
`0d5de10f17498fc12e05b26a56cdfe316c0c1f7db87fd21a45cb3b019406ac39`,
identical to an uninterrupted control.  Changed configuration, input, source,
task plan, truncated checkpoint, and corrupt checkpoint were all refused; an
orphan temporary file was ignored unchanged.

## Claim boundary

An L4 pass is only a target-side reproduction of the already sealed L4
single-revisit mechanism.  It is not independent evidence and establishes no
finite-size scaling, persistence, curvature, geometry, continuum, RGRL/WTC
premise, dark-sector result, or gravity result.  L6 and L8 remain prohibited
until the independent implementation, interruption/resume, and measured
resource gates are jointly satisfied.
