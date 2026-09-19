# Hostile V004R4 storage-cache and native history method

## Status and boundary

This is the independent hostile branch for the finite cached L=10 and L=12
record checks. It preserves the reversed-combination basis, reversed edge
enumeration, full canonical lineage masks, and the V003
Chebyshev/recurrence-replay evolution. It is not a target-Krylov
implementation. Its terminal shards are headerless little-endian complex128
files. No field or file is to be relabeled as a target solver or NPY artifact.

The method produces finite record evidence only. It does not calculate a
spectrum and supports no z=1, continuum, emergence, or gravity claim.

## Immutable storage cache

For each L in 4, 6, 8, 10, and 12, the builder materializes:

1. reversed fixed-weight carrier masks and directed exchange source/target
   ranks for each of the 3L hostile edges;
2. exact event-admission rank pairs;
3. exact same/add lineage rank maps; and
4. one manifest that binds every member's path, dtype, shape, byte count, and
   SHA-256 to the frozen hostile source packet.

The frozen packet includes the method, builder, consumer and preflight plus
all eight packet-local Python dependencies they execute:
`independent_prefix_history.py`, `independent_prefix_history_v002.py`,
`independent_prefix_history_v003.py`, `independent_prefix_history_v004.py`,
`independent_prefix_history_v004r2.py`, `v004r2_common.py`,
`validate_v004r4_zero_length_preflight.py`, and `v004r4_cache_io.py`.
Each executable authenticates and retains those dependency descriptors for its
entire operation. The separately frozen final-history validator is also
hash-bound, descriptor-loaded, and retained before it is executed.

The two q=0 exchange arrays are ordinary immutable zero-byte files. The
consumer represents each as a read-only empty ndarray and never asks NumPy to
memory-map an empty file. Every nonempty array is mapped from a duplicated,
already-authenticated descriptor. All cache descriptors remain held through
history publication and are reauthenticated after evolution.

## Native evolution record

The consumer uses the existing independent V003 low-memory recurrence replay:

- rough accuracy: checkpoints 16,24,32,48,64,80; 18 quadrature nodes;
  tolerance 3e-9;
- sharp accuracy: checkpoints 24,32,48,64,80,96; 28 quadrature nodes;
  tolerance 8e-11;
- algorithm identity: `RECURRENCE_REPLAY_GL_GROUPS`;
- numerical-allocation guard: 1,400,000,000 bytes;
- scratch guard: 21,474,836,480 bytes;
- RSS guard: 17,179,869,184 bytes; and
- wall guard: 21,600 seconds.

Every emitted solver record has the native twelve-field base schema. The
event-L actual solver adds exactly the four terminal-streaming certificates.
The comparison retains the native `rough_sharp` field. The resource record
retains `peak_logical_state_plus_cache_bytes`; it is not converted to the
target resource vocabulary.

At L=12 the exact raw-file accounting is:

- maximum simultaneously live state: 8,773,664,640 bytes;
- cache payload: 826,221,912 bytes;
- state plus cache: 9,599,886,552 bytes;
- reserve: 1,048,576 bytes; and
- hostile filesystem floor: 9,600,935,128 bytes.

## Owner-once and cross-branch audit

The hostile row records the independently computed allow/blocked split, write,
retained and genesis quantities, currents, owner-once residuals, continuity
residuals, norms, and full sector weights. It does not copy target rows. The
cross-auditor projects only shared physical observables, derives target-only
owner-once fields from the native row, and compares terminal amplitudes after
an independently reconstructed target-rank to reversed-rank mask bijection.

Target terminal NPY payloads begin after their authenticated headers. Hostile
terminal payloads begin at byte offset zero. The different solver telemetry,
comparison vocabulary, resource vocabulary, and storage framing are evidence
of implementation independence and are never required to be identical.

## Publication and authorization

No cache or history is constructed before an immutable freeze, complete
nonphysical preflight, and independent hostile audit. L=10 requires its exact
one-way authorization. L=12 additionally requires the exact L=10 cross audit,
readiness schedule and schedule audit, both one-way L=12 authorizations, the
two-live-worker handshake, and the worker-release barrier.

The L=12 cache manifest preregisters the postbuild audit's canonical path,
schema, and identity but deliberately does not contain its future digest. The
postbuild audit then binds the completed manifest SHA-256, and the L=12 history
binds both digests. This one-way dependency is acyclic. Non-L12 cache manifests
carry a null postbuild field and are authenticated directly by their bounded
stage authorization and consuming cache context.

The prepayload audit has one exact schema. It binds the freeze, complete source
census, preflight-result digest, independent auditor role, preservation of
V004R3, a seven-entry absence census (including the postbuild audit), positive
all-pass checks, non-execution, and the nonphysical claim boundary. The
cache-build authorization reconstructs that complete audit; a partial or
differently keyed audit cannot authorize construction.

L=12 is executable only as a worker launched over an inherited duplex socket.
Before opening a cache or history, the worker retains its executable and sends
one canonical READY record containing its PID, kernel-derived process-start
token, executable path/hash, paths, channel identity, and a SHA-256 commitment
to an internal 32-byte nonce. The coordinator retains the process handle and
executable descriptor, publishes an exact V002 two-worker handshake and
release, then sends a canonical release command on that same channel. The
worker retains and cross-checks both files before revealing the nonce in its
release ACK. The ACK binds the exact release-command bytes. L=10 remains a
separate one-way authorized non-orchestrated control.

After a successful L=12 atomic history publication, the worker opens and
retains the immutable canonical output, authenticates its descriptor, path,
mode, link count, parent identity, and SHA-256, and sends the exact canonical
`V012_L12_WORKER_COMPLETION_V001` frame on the inherited channel. It then
shuts down its write side and remains a live, blocked process until the
coordinator closes its side without sending any further bytes. The worker
rechecks output custody after EOF before exiting. This supplies an honest
terminal-live sampling boundary; it is not a physical-result adjudication.

The canonical aggregate records are
`DUAL_L12_LAUNCH_HANDSHAKE_V002.json` and
`DUAL_L12_WORKER_RELEASE_V002.json`; the per-worker socket command and ACK
remain V001 wire records. The worker rejects a pre-existing handshake or
release after schedule expiry and independently requires distinct target and
hostile authorization hashes, PIDs, worker IDs, channel IDs, and nonce
commitments. Preserved V005 obstruction evidence may retain its historical
0644 mode: custody records that exact mode, inode, timestamps, size, and hash
and rejects any later drift, while all newly frozen authority remains
strictly non-writable.

Terminal files are fsynced, made immutable, hashed from retained descriptors,
and retained through atomic no-clobber history publication. Cleanup removes a
staging path only when it still names the held staging inode, and a canonical
inode is never deleted after the no-clobber link succeeds. The publisher also
retains the canonical parent-directory identity and refuses a rename, swap, or
symlink substitution before the link. The L=12 writer
calls the independently frozen A25 validator before publication. Any missing,
changed, stale, aliased, writable, symlinked, nonfinite, or over-limit input
causes refusal without a positive history result.
