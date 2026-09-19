# L12 target/hostile cross-adjudication method V001

**Status:** `FROZEN_BEFORE_L12_HISTORY_OUTPUT`

This bounded adjudicator accepts only separately SHA-256-pinned target and
hostile L12 result records.  It does not import either history engine.  It
checks the complete event census, canonical dimension identities, resource
and convergence gates, all owner-once and conservation residuals, every
sector weight, and the agreed history observables at `1e-8`.
The 20 GiB scratch, 16 GiB RSS, six-hour wall, and implementation-specific
1.0/1.4 GB numerical-workspace limits are reconstructed from typed raw
telemetry rather than trusted from a Boolean.  Sector nonnegativity and
normalization use the stricter downstream manifest bounds `-1e-12` and
`1e-9`; the charge moment of every sector distribution must reconstruct the
retained ledger charge.

The retained preterminal H11 states are part of the gate.  For every charge
`q=0,...,11`, the adjudicator checks the exact canonical shard shape and byte
census, independently hashes both files, and compares every complex amplitude
in bounded row chunks.  This preserves complete lineage and carrier support;
it is not an observable-only comparison, quotient, truncation, or sample.
Both real and imaginary parts must be finite.  Each shard is hashed before
and after the comparison, and both paths must remain within separately named
terminal roots.  Those roots and the exact canonical shard names are pinned
by the pre-output active-execution custody observation (session, PID, command,
workspace birth, implementation hash, and then-open rough shard), so a caller
cannot substitute an arbitrary terminal directory.
Target NumPy headers are not expected to match the hostile raw-file bytes, so
custody is recorded by independent per-file SHA-256 values while numerical
identity is tested on decoded complex128 arrays.

The two independent engines deliberately use different basis orders.  Target
rows and columns enumerate `combinations(range(width),q)`; hostile rows and
columns enumerate `combinations(reversed(range(width)),q)`.  Before comparing
labeled amplitudes, the adjudicator constructs the exact mask-preserving
target-rank-to-hostile-rank permutation independently on both the width-11
lineage axis and width-24 carrier axis.  It proves each map is a complete
bijection, applies it in bounded chunks without permuting/materializing the
full state, and records both permutation hashes for every `q`.

The program refuses to overwrite output and fails closed on any missing,
non-finite, unresolved, over-limit, or mismatched datum.  A pass establishes
only two-implementation agreement for this finite L12 history under the
frozen representation and numerical tolerance.  It does not establish an
infinite-size limit, spectral scaling, criticality, continuum behavior,
spacetime algebra, emergence, or gravity.

On a complete pass only, the adjudicator also emits a hash-bound manifest
adapter for the hostile record.  The adapter copies the entire hostile JSON
and adds only `dimension = full_dimension`, because the independently written
history uses the latter key while the already-frozen spectrum-manifest schema
requires the former.  The adapter records its source hash and this
adjudicator's hash.  No row, amplitude, observable, tolerance, classification,
or physical field is altered.

The adjudicator requires the externally supplied hash of this freeze and an
exact frozen dependency census.  Its two outputs use create-new atomic links;
if final audit publication fails after the schema adapter is linked, that new
adapter is removed rather than left as an orphaned passing input.
