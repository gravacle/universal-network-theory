# V012 preregistered hostile-audit methodology

**Status:** `PREREGISTERED_OBLIGATIONS_ONLY__NO_AUTHORITY_GRANTED`

## Boundary

This directory freezes the audit obligations for the bounded target-V012 path
through a finite L12 target/hostile comparison.  It is not a target packet and
does not create or authorize a gate, cache, workspace, history, physical run,
or scientific result.  The machine-readable authority is
`AUDIT_OBLIGATIONS_V001.json`; this document only explains how to apply it.

The final adjudicator is deliberately implementation-independent.  Its
source, driver, and tests are hash-frozen as dependencies before the target
preflight can execute.  An auditor must
parse raw UTF-8 JSON itself, reject duplicate keys and nonfinite constants,
open evidence by stable no-follow read-only descriptors, and independently
reconstruct every required census, digest, projection, resource bound, stage
transition, and target/hostile comparison.  It must not import, call, monkey
patch, or treat the return value of any target builder, consumer, preflight,
validator, or V004/V004R4 execution module as audit evidence.

## Audit order

1. Freeze and hash all five target sources, including the dedicated production
   obligation validator, and hash exactly the independent final auditor,
   production-DAG refinement, production evidence orchestrator, and production
   dual-L12 launcher before exposing them to the completed target packet. Test
   and fixture helpers are excluded from production authority. Authenticate
   the complete dual-launch coordinator packet against manifest SHA-256
   `a6b6c61fa4e44cb53965b22c0fa0999c612a72cca9c90e31835bda3fa1a3336f`
   and its exact eight-member source/result/verification census before accepting
   any launch-protocol dependency.
2. Validate the target source/freeze and preflight record, then run the
   independent prepayload audit while every future authority, payload, and
   physical artifact remains absent.
3. Validate the universal custody gate separately from the L4/L6/L8 control
   authorization.  Build/authenticate storage payloads only after the custody
   gate; do not infer physical authority from cache existence.
4. Independently audit all five caches and the base physical gate.  Permit only
   L4/L6/L8 under the first outer authorization.
5. Reconstruct the L4/L6/L8 histories against sealed V004, audit their stage
   gate, and only then audit the distinct L10 authorization.  Reconstruct L10,
   audit its stage gate, and require an exact target/hostile L10 cross-gate.
6. Establish hostile L12 eligibility transitively, create and audit the shared
   readiness/resource schedule, then authenticate distinct one-way target and
   hostile L12 authorizations.  Only after both immutable authorizations exist
   may two prelaunched blocked workers commit a distinct immutable handshake;
   only that handshake may authorize the exact dual-worker release.  The
   readiness schedule itself contains no handshake or release record.
7. After the dual-worker release and contemporaneous execution, reconstruct exact telemetry, both L12
   outputs, all unlock/audit hashes, and the final cross-adjudication.

No later PASS may repair or reinterpret an earlier failed artifact.  A failed
obligation produces a new immutable obstruction record outside this
preparation directory and leaves the path locked.

## Fixture and mutation discipline

Every matrix artifact has at least one required positive-fixture specification
and a nonempty list of mutation classes.  A22 has eight separately identified
positive forms: both one-way authorizations, READY, V002 handshake, V002
release, release command, ACK, and terminal-live completion.  Those forms
represent the exact 12 owner-once role instances. Each fixture has the artifact's native
production schema and is created in an auditor-owned temporary directory.  It
must never be written at a canonical target path and confers no authority.
The 33 positive fixtures and all 477 assigned hostile cases must execute the
same production contract validator invoked at artifact publication.  Custody
and premature-artifact cases instead execute the real descriptor and absence
hooks.  A22 semantic cases execute at their declared native coordinator state
transition and retain its refusal text verbatim; no mutation-label relabeling
is permitted.  A generic acceptance sink, or a validator existing only in the
test harness, is not evidence.  For each case, the ledger records the fixture and
mutated-byte digests, mutation-evidence digest, exact production hook and
validator function, expected and actual refusal, exact one-call census, and
whether any canonical artifact was created.

Positive acceptance alone is insufficient.  Promotion requires all 477
required mutations to refuse at the declared production contract, all check
totals to be independently reconstructed from the executed test ledger, and
exact agreement between `checks_passed`, `checks_total`, and the reconstructed
count.  The preflight result itself is then validated as a whole: exact schema
and claim; nonexecution booleans; complete check map; allocation and resource
censuses; all five frozen-source digests; freeze and mutation-ledger bindings;
and compatibility locks.  Python numeric equality is never an exact-type test:
booleans, integers, and floats are distinct.

The filesystem floor is reconstructed from two independent native storage
models.  Target scratch is `9,600,954,452 B`, including its NumPy headers.
Hostile scratch is `9,600,935,128 B`; its peak live state contains 23 raw
`.c128` shards (the adjacent prefix pair), with
exactly zero container-header bytes and native Chebyshev telemetry.  The exact
concurrent floor is `19,201,889,580 B`; the
hostile implementation must not be normalized to the target Krylov layout.
The resource certificate actively mutates the hostile header census to the
target-style `23 * 128 B` surcharge and requires the exact raw-c128 header
refusal.

## Custody and long-running use

Every authority or evidence file must be an ordinary nonsymlink file reached
through an exact absolute path with no symlinked parent component.  The exact
absolute-versus-resolved identity is checked before authentication, after the
descriptor is opened, and again at every retained-custody verification.  Unless
an explicitly sealed legacy parent is read-only evidence, it must have no
write bit.  The auditor opens with `O_RDONLY|O_NOFOLLOW`, hashes the descriptor,
records device/inode/size/mtime/ctime, parses bytes from that descriptor, and
rehashes/re-stats the still-open descriptor after validation.  Long-running
consumers retain or duplicate authenticated descriptors and reauthenticate
them before publication.  Path reopens, symlink swaps, writable replacements,
parent rename-plus-symlink aliases, and cross-role path/digest aliasing are
mandatory hostile cases.

Every owner-once publisher holds the canonical parent with
`O_DIRECTORY|O_NOFOLLOW`; staging creation, no-clobber linking, reopening,
identity checks, inode-owned cleanup, and directory `fsync` are performed
relative to that held descriptor.  An ancestor rename followed by a symlink to
the same directory must refuse while leaving any already-linked immutable
evidence intact.

The prelaunch absence census includes the hostile postbuild payload audit, the
target and hostile one-way L12 authorizations, both immutable worker READY
records, `DUAL_L12_LAUNCH_HANDSHAKE_V002.json`, and
`DUAL_L12_WORKER_RELEASE_V002.json`, both release commands, both ACKs, and both
completion records.  These 12 authority records are each owner-once.  Each
release is delivered by its exact wire command and acknowledged by a
nonce-bound immutable ACK.  After each L12
history is atomically published and reauthenticated, its still-live worker
sends an exact `V012_L12_WORKER_COMPLETION_V001` frame, closes only the write
side of the control channel, and waits for coordinator EOF without trailing
bytes.  The coordinator authenticates both frames and preserves their target
and hostile completion records before accepting postrun telemetry.  A schedule that embeds a handshake, a
handshake admitted before both authorization hashes are immutable, or a
release admitted before the handshake is a mandatory fail-closed case.  The
postrun telemetry must bind the schedule audit, both authorizations, the
handshake, and the worker release, and its launch epochs must reconstruct from
the release epochs.

## Completion criterion

An audit layer passes only when every artifact obligation assigned to that
layer has: exact schema/key/type/value checks; complete hash provenance; stable
custody; independent reconstruction; one passing positive fixture; all
assigned mutations refused; and an exact nonphysical claim boundary.  The
final L12 audit additionally requires both complete output hashes, exact
postrun telemetry, the sealed L10 cross-gate, and independent comparison.  It
can establish only a finite L12 accumulation result; spectrum, scaling,
continuum, emergence, and gravity remain outside this contract.
