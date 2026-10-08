# Reviewed stdout publisher: independent scope preflight V001

2026-09-29. Read-only source review by geometry_native_scope; no invocation,
import, compilation or scientific producer was executed by this reviewer.

Reviewed `publish_reviewed_stdout_v001.py`, SHA256
`2c37dda44d7bf4aa685185797afff1a0d2131be002ceab8129a7b42a1420f19e`,
and the actual reused publisher/source bytes. The publisher pin is
`f4cf2cea4d4d42688616ee671f66b5717a0fb554f1ea4972783d9cc1b00071b8`;
the hard qualifier pin is
`4a8a0b7260b970aa4aa11b682e4b3377f96ad0b7dd0d47ce6d0735db888fc8d6`;
the HYREC BAO interval producer pin is
`c35a24011a92462d725824eff0a96bdfca7ae11a5935e462a5dce3f7ce85fdb3`.
All three pins match the actual files inspected.

The six named jobs have fixed sources, argument lists and destinations:
BAO freeze/collection and hard freeze/build/benchmark/full qualification.
No caller-supplied command or unbounded output target is accepted. Paths
are confined to the verified project root, symlink targets are rejected,
and an existing destination is refused before the producer is invoked.

The reused publisher binds source/input/output identities and publishes by
an atomic, fsynced no-overwrite hard-link operation. Successful JSON must
be a finite object; applicable canonical payload/freeze identities are
checked. Failed invocation, malformed output or publication failure retains
captured stdout and the exception/traceback in a uniquely named attempt
receipt rather than overwriting an existing scientific result. This is not
a hidden retry mechanism and does not turn an unqualified payload into a
scientific success.

Scope qualification: this wrapper captures Python stdout, not an independent
Python stderr stream. Subprocess C stdout/stderr are retained by the already
reviewed hard producer's own invocation receipts. This is acceptable for the
six fixed jobs as written; it is not a general arbitrary-command recorder.

No blocker found for the declared immutable-output handling. This preflight
does not attest to later execution outcomes or replace their saved-data
audits. No numerical or scientific acceptance criterion was changed.
