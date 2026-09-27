# Target scaling execution attempt log V001

## Preserved pre-physics failure

Checkpoint root: `CHECKPOINTS/L4_EVENT00_TARGET_V001`

The initial L4 launch bound kernel SHA-256
`97727a6793e6b21f66be61c13734dba97b8aab9c645a2b3dcd7f48b9f61c7cd6`
and stopped before completing its first q-sector task.  macOS `spawn` could not
re-import the authenticated resumable runtime because the wrapper had assigned
it a temporary module alias.  The runtime recorded `RUN_FAILED` with zero of
five tasks completed.  It published no sector result and no physical output.

The failed identity and append-only journal are retained without alteration.
Because the corrected source has a different hash, that checkpoint is
ineligible for resume.  The corrected run keeps the runtime's canonical,
importable module name and uses a distinct owner-once checkpoint root:
`CHECKPOINTS/L4_EVENT00_TARGET_V001R1`.

## Preserved resume-harness fixture-permission failure

Evidence root: `RESUME_EQUIVALENCE`

The first restart-harness attempt completed its uninterrupted control and
deliberately stopped its second run after two sector commits.  It then stopped
before resume while attempting to truncate a disposable checkpoint copy:
`copytree` had correctly preserved the immutable task file's `0444` mode, so
the test mutation was denied.  No resume-gate result was published.

That partial evidence is retained.  The harness was corrected only to make the
specific copied fixture file writable; original checkpoint files remain
immutable.  The corrected source SHA-256 is
`098503b78befef95055cc9e80ef56b1750b7acd6411dd997103741fe7c6fd5a0`
and its owner-once evidence root is `RESUME_EQUIVALENCE_V001R1`.
