# V004R4 cross-branch contract — draft, deliberately unfrozen

**Status:** `DRAFT_BLOCKED_ON_TARGET_V007_FREEZE_AND_AUDIT_INTERFACE`

V004R3 is preserved verbatim as a failed predecessor. This draft is not a
freeze, build authorization, cache authorization, execution authorization, or
physical protocol. Its sole purpose is to make the next cross-branch custody
interface explicit before target V007 publishes immutable identities.

## Required target V007 interface

V004R4 will accept no V005 or V006 target artifact. Before V004R4 can freeze,
target V007 must publish immutable, independently audited records for:

1. its freeze and complete frozen file/dependency census;
2. its hostile pre-payload audit result and positive check count;
3. its exact cached L10 pass gate and complete L10 history/comparison lineage;
4. its immutable L12 cache manifest; and
5. the target consumer identity that will validate the shared launch gate.

The V004R4 freeze will replace every `UNBOUND_TARGET_V007_*` sentinel in the
draft validator with a literal SHA-256, schema, classification, positive check
count, and canonical repository path. `assert_ready_for_freeze()` refuses while
any sentinel remains. This prevents an early or implicit V005/V006 fallback.

## Preregistered hostile-audit dependency

The future V004R4 cache-build authorization gate must contain an
`independent_hostile_audit` binding with the canonical audit-result path, its
SHA-256, the exact pass classification, and a positive `checks_passed ==
checks_total`. The validator also opens that audit result and requires:

- the exact V004R4 freeze and frozen method/common/builder/consumer/preflight
  hashes;
- a zero-failure, positive all-pass count;
- explicit V004R3 byte preservation;
- all future gates/caches/workspaces/histories absent during the audit; and
- a nonphysical claim boundary.

Thus a build gate cannot be manufactured from a classification label alone,
and V004R4 cannot repeat V004R3's audit-identity omission.

## One shared aggregate L12 gate

After both branches have independently passed their cached L10 gates and
sealed their L12 cache manifests, both L12 consumers must validate the same
byte-identical shared record:

`AUDIT_R_L12_PARALLEL_EXECUTION_V001/SHARED_AGGREGATE_SCHEDULE_GATE_V001.json`

That record binds both branches' freeze, independent-audit, consumer, exact
cached-L10-gate, and L12-cache-manifest hashes. Each branch's L12 execution
gate then pins the shared gate's SHA-256. The shared record does not pin either
execution gate, avoiding a cryptographic cycle.

The shared gate includes a fresh resource snapshot and requires:

- exact aggregate RSS-plus-mapping bound: `34,865,626,528 B`;
- unchanged per-process RSS guard: `17,179,869,184 B`;
- target and hostile mapped peaks: `252,944,080 B` each;
- target disk minimum: `9,600,951,508 B`;
- hostile disk minimum: `9,600,935,128 B`;
- combined disk minimum: `19,201,886,636 B`;
- nominal host memory: at least `48,000,000,000 B`;
- available memory and workspace free disk at snapshot no smaller than their
  aggregate bounds;
- one filesystem identity for both workspaces;
- launch only after both exact cached L10 passes; and
- target/hostile launch skew no greater than 60 seconds.

The gate preregisters one canonical telemetry record. Both launchers use that
same path and schema. Telemetry must capture per-role launch/completion epoch,
wall time, peak RSS, peak mapping, exit code, output hash, and periodic free
disk samples. The telemetry path must be absent before launch and is never a
substitute for either branch's own result validation.

## Claim boundary

This draft concerns record custody, resource scheduling, and future finite
history authentication only. It runs no cache construction or physical
evolution and does not support a spectrum, scaling, continuum, emergence, or
gravity claim.
