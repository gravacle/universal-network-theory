# Exact held-out L10/L12 joint lineage--carrier execution protocol V001

Date: 2026-09-23

Status: `FROZEN_PRE_HELDOUT_OUTPUT__READY_FOR_AUTHORIZED_EXACT_EXECUTION`

## 1. Purpose and non-observation declaration

This packet implements only the execution and resource gate already required
by Section 8 of
[`DEVELOPMENT_R_OWNER_ONCE_JOINT_LINEAGE_CARRIER_WITNESS_V001/PROTOCOL.md`](../DEVELOPMENT_R_OWNER_ONCE_JOINT_LINEAGE_CARRIER_WITNESS_V001/PROTOCOL.md).
It does not change the observable, controls, equations, tolerances, event
schedule, checkpoint, or classification.

At this freeze:

```text
D_10 has not been computed or opened.
D_12 has not been computed or opened.
No held-out target, hostile, or reconciliation result exists in this packet.
```

The sealed L4/L6/L8 reconciliation satisfies prerequisites 1--3 of the
held-out rule. This packet authenticates prerequisite 4 and freezes the exact
larger-size execution before any held-out witness value is generated.

## 2. Unchanged scientific definition

For `L in {10,12}`, use the same owner-once state, the same terminal checkpoint
after event `L-1` transport and before any revisit, and the same definitions

\[
 w_L={1\over L}\sum_{q,S,C}p_{L,q}(S,C)
       \sum_e\left(F_e(S)-{q\over L}\right)n_e(C),
\]

\[
 D_L=w_L-w_L^{\rm sham}
 ={1\over L}\sum_{q,e}p_{L,q}\,\operatorname{Cov}_{L,q}(F_e,n_e),
\]

\[
 \tau_L=\max(10^{-9},50d_L,100r_L),
 \qquad
 T_{10:12}=\min\left({|D_{10}|\over\tau_{10}},
                     {|D_{12}|\over\tau_{12}}\right).
\]

`d_L`, `r_L`, the sector-matched sham, the exact within-`q` lineage shuffle,
the row/column accumulators, and every numerical tolerance retain their
definitions in the parent protocol. There is no fit, extrapolation, sign
selection, clipping, changed centering, or alternative observable.

## 3. Authority chain

Execution is permitted only when all of these immutable records authenticate:

1. frozen witness protocol SHA-256
   `70984a927c30585704622dfd03ee91bf516cd9a5d14474a228d231144e5e513e`;
2. sealed seed disposition SHA-256
   `2ce9852ef40d16d50b7a6553d0173e041c9cfdcc59925819f900f21f8a684f14`,
   whose classification is
   `RESOLVED_OWNER_ONCE_JOINT_LINEAGE_CARRIER_WITNESS_L4_L8`, whose
   `T_4_8>1`, and whose seed controls pass;
3. exact prefix-lineage reconstruction theorem and protocol;
4. the four retained target/hostile L10/L12 history records and their
   terminal-shard metadata; and
5. a fresh resource-telemetry record satisfying Section 9.

The complete paths, hashes, shard-manifest digests, counts, and byte totals are
machine-bound in [`INPUT_AND_RESOURCE_GATE.json`](INPUT_AND_RESOURCE_GATE.json).
The four history records are the authoritative per-shard hash manifests. The
gate canonicalizes each `terminal_shards` list to repository-relative paths
and hash-binds that complete list; an implementation may not substitute an
unlisted shard or absolute-path alias.

## 4. Historical 60-GiB rule and the successful V003 successor

The original streamed-method freeze remains historically correct and
immutable. It required at least `60 GiB` free scratch before its original L12
method could start. That literal rule is preserved at SHA-256
`1d6da35196cdf7deac0f4d9b8a099eec997e969ee0b25f9ff580ff2a13242d40`.
This packet does not edit, reinterpret, or retroactively waive that gate.

The later V003 process-parallel successor proved and successfully executed an
exact prefix-lineage representation. It retained every canonical lineage and
carrier amplitude, materialized `H_(L-1)` rather than `H_L`, and streamed the
orthogonal terminal children. Its V012 resource certificate requires:

```text
concurrent target + hostile RAM bound       34,865,626,528 B
minimum total host memory                   48,000,000,000 B
headroom on a decimal 48-GB host            13,134,373,472 B
combined target + hostile scratch minimum   19,201,889,580 B
per-process RSS limit                       17,179,869,184 B
hard wall limit per branch                     345,600 s
```

That successor is not a relaxation or an approximation of the old method. It
is a distinct, exact, hash-custodied representation that already completed
both target and hostile L12 histories. Therefore:

```text
60-GiB rule = still binding for the original frozen method lineage.
19,201,889,580-B rule = binding for this exact V003 successor lineage.
```

The old obstruction is preserved as superseded only for the V003 successor;
it is not erased from history and grants no authority to unrelated methods.

## 5. Retained exact inputs

The held-out calculation consumes four pairwise distinct, read-only terminal
prefix roots:

| Branch | Size | Canonical retained prefix | Exact shard bytes |
|---|---:|---|---:|
| target | L10 | `DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/WORKSPACES/L10/sharp/prefix_09` | `160,241,360` |
| target | L12 | `DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/WORKSPACES/L12_PROCESS_PARALLEL_V003R1/sharp/prefix_11` | `6,675,615,936` |
| hostile | L10 | `AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/V004R4_WORKSPACES/L10/sharp/prefix_09` | `160,240,080` |
| hostile | L12 | `AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/V004R4_WORKSPACES/L12_PROCESS_PARALLEL_V002/sharp/prefix_11` | `6,675,614,400` |

Target uses `.npy` shards in target canonical order. Hostile uses raw `.c128`
shards in its independently reversed order. Neither branch may read the
other's shard bytes, basis maps, matrices, scratch, source implementation, or
result before independent publication.

Every shard must be a regular non-symlink file with the exact size and hash in
its bound history record. Directory totals are not substitutes for per-file
authentication. A missing, additional, aliased, size-mismatched, or
hash-mismatched shard refuses before numerical execution. Some preserved
hostile V003 shards retain their historical writable mode; this packet does
not rewrite that provenance. They must be opened read-only with no-follow
semantics, remain unmodified, and reauthenticate before and after every
calculation. An attempted or observed write refuses publication.

## 6. Terminal reconstruction

For each branch and size, authenticate the retained sharp state in `H_(L-1)`.
For each old sector and canonical preterminal row:

1. reconstruct the final fresh event `e=L-1` with the branch's already frozen
   admission implementation;
2. retain both orthogonal admission images, selected by the last lineage bit;
3. apply the branch's frozen sharp transport to each child in bounded row
   windows;
4. accumulate `p_(L,q)`, `w_L`, `w_L^sham`, every `q` contribution,
   row/column marginals, shuffle identity, and residuals by exact addition; and
5. discard a child window only after both independently ordered accumulators
   have consumed it.

The full logical `H_L` array is never allocated. This is the inverse terminal
recipe proved by PLB-4, not a trace, sample, quotient, branch deletion, fitted
distribution, carrier-only closure, or macro surrogate. The calculation may
stream the witness because it is diagonal in the joint lineage--carrier basis.

## 7. Coarse/fine histories and independence

The retained shards are the authenticated sharp/fine `H_(L-1)` histories.
The branch-specific rough/coarse companion must be regenerated into a new,
empty, size- and role-specific scratch root using the corresponding frozen
propagator and event schedule. It may not overwrite or modify a retained
shard. The sharp/fine terminal readout is reconstructed from the retained
sharp prefix; the rough/coarse terminal readout is reconstructed from the new
rough prefix. Both use the same frozen final-event checkpoint.

Target and hostile executions have separate source trees, basis order,
carrier edge order, propagation method, scratch roots, logs, and raw result
paths. Before both raw results are immutable and hashed:

- target may not inspect hostile source, arrays, scratch, result, or value;
- hostile may not inspect target source, arrays, scratch, result, or value;
- neither may use a value from L4/L6/L8 to tune L10/L12 numerics; and
- reconciliation may not begin.

The branch results must each include rough/sharp, row/column, sector, sham,
shuffle, norm, content, charge, marginal, source-hash, and input-hash fields.
The independent reconciliation then computes `d_L`, `r_L`, `tau_L`, and
`T_10:12` exactly as frozen.

## 8. Execution schedules

### 8.1 Sequential fallback schedule

On a machine that does not have `34,865,626,528 B` freshly available RAM, run
one branch at a time:

```text
authenticate all four inputs
run and seal target L10
run and seal hostile L10
reconcile L10 controls without opening or selecting L12 by outcome
run and seal target L12
run and seal hostile L12
reconcile L10/L12 once
```

L12 remains mandatory once an authorized held-out execution begins and the
resource gate passes; L10 cannot be used as a result-dependent stop or tuning
gate. The intermediate L10 reconciliation checks implementation health only.

Each branch retains the `17,179,869,184 B` RSS ceiling and `345,600 s` hard
wall. Require at least `19,201,889,580 B` free scratch before the schedule so
that exact retained inputs, isolated rough regeneration, partial obstruction
evidence, and the alternate branch remain protected. Sequential execution is
the default for the present workstation.

The completed successor histories provide runtime references, not stop
predictions: target `57,414.175905833 s` (`15.948 h`) and hostile
`55,695.198680708 s` (`15.471 h`). Their exact sum is `113,109.374586541 s`
(`31.419 h`). The held-out readout may be faster because it reuses retained
sharp prefixes, but no shorter wall allowance is inferred.

### 8.2 Optional concurrent schedule

Concurrent target/hostile execution is permitted only when telemetry no more
than 300 seconds old proves all of:

```text
memory pressure                           NORMAL
total host memory                         >= 48,000,000,000 B
currently available memory                >= 34,865,626,528 B
shared-filesystem free scratch             >= 19,201,889,580 B
target and hostile scratch/output roots    pairwise distinct
```

The maximum release skew is 60 seconds. Per-process RSS and wall gates remain
in force. The historical concurrent critical path was
`57,414.175905833 s` (`15.948 h`); this is reference telemetry, not a promised
runtime. The scheduler selects concurrent execution when every fresh gate
passes and otherwise selects the sequential fallback; it never
oversubscribes based on nominal installed memory.

## 9. Fresh telemetry and authorization

Resource telemetry is a separate control-plane JSON record. It must contain
only the frozen schema fields, integer byte counts, an integer capture epoch,
`NORMAL` memory pressure, selected schedule, and the exact scratch/output
roots. Validation must occur no more than 300 seconds after capture and again
immediately before numerical allocation. Hostname, username, device serial,
and scientific values are forbidden. Telemetry is not copied into the
deterministic scientific result.

The exact execution guards are:

```text
AUTHORIZE_EXACT_HELDOUT_TARGET_L10_L12_JOINT_WITNESS_V001
AUTHORIZE_EXACT_HELDOUT_HOSTILE_L10_L12_JOINT_WITNESS_V001
AUTHORIZE_EXACT_HELDOUT_L10_L12_RECONCILIATION_V001
```

Each literal token authorizes only its named role and only after source,
input, resource, absence, and separation checks pass. A missing or mismatched
token exits without creating a result. It is never persisted as a credential.

## 10. Deterministic result schemas

All scientific JSON is strict UTF-8, sorted-key JSON with finite numbers,
repository-relative paths, no hostname, no timestamp, and one trailing
newline. The three schemas are:

```text
OWNER_ONCE_HELDOUT_TARGET_JOINT_WITNESS_RAW_V001
OWNER_ONCE_HELDOUT_HOSTILE_JOINT_WITNESS_RAW_V001
OWNER_ONCE_HELDOUT_JOINT_WITNESS_RECONCILIATION_V001
```

Each raw result binds this protocol, the machine gate, its implementation,
its complete authenticated input census, and every required diagnostic. The
reconciliation binds both immutable raw results and reproduces every
classification predicate. Reruns with unchanged inputs must be byte-identical.

## 11. Fail-closed dispositions

No new scientific classification is introduced.

- Missing authorization, pre-existing output, input drift, branch aliasing,
  stale telemetry, insufficient RAM, insufficient scratch, or a required
  exact calculation exceeding the resource gate returns
  `EXACT_JOINT_WITNESS_SCALING_OBSTRUCTION` without approximation.
- A nonfinite value, failed numerical/control condition, or unresolved
  target/hostile comparison returns
  `OWNER_ONCE_JOINT_LINEAGE_CARRIER_WITNESS_UNRESOLVED`.
- If both sizes resolve and `T_10:12>1`, return
  `HELD_OUT_OWNER_ONCE_JOINT_LINEAGE_CARRIER_WITNESS_L10_L12`.
- If both sizes resolve and `T_10:12<=1`, return
  `HELD_OUT_OWNER_ONCE_JOINT_WITNESS_NOT_REPRODUCED`.

Partial output is obstruction evidence only and cannot be promoted. There is
no fallback to sampling, truncation, compression that changes arithmetic,
carrier-marginal substitution, one-branch publication, one-size publication,
or a relaxed guard.

## 12. Claim boundary

A held-out pass proves only that the preregistered finite terminal
lineage--carrier witness reproduces at exact L10 and L12 under the same
owner-once parent and controls. It does not prove future back-reaction, a
record-reading interaction, persistence after revisit, entanglement, an
all-`L` or thermodynamic limit, the ARGER Gate, RGRL, alpha, GL6T, spacetime,
metric response, Einstein--Hilbert dynamics, or gravity.
