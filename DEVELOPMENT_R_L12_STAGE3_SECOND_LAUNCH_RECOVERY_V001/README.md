# Stage 3 second-launch recovery V001

Classification: `DEVELOPMENT_FIXED_SCOPE_CANDIDATE_PENDING_HOSTILE_REVIEW`

This packet repairs only the hostile worker's missing `positive_integer`
predicate and regenerates the exact descendant cache/L10/A18 authority chain.
It authenticates and retires exactly 14 predecessor entries, requires nine L12
outputs to remain absent, replays only hostile L10, and stops before L12.

The non-mutating plan, dry-run, and focused tests pass. Live execution is
forbidden until independent same-hash review accepts the frozen source and test
bytes. The deterministic chain ends at the L10 authorization candidate; L10
history, L10 gate, and A18 hashes are derived only from the live replay.

Restart is fail-closed at a partial cache or partial L10 computation: those
bytes are preserved as an obstruction rather than deleted or automatically
repaired. Owner-once publication checkpoints are restartable. This packet does
not implement a generalized crash-recovery framework.

Claim boundary: no L12 history, spectral, continuum, or gravity result.
