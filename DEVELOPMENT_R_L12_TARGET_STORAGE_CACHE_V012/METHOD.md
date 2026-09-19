# Target V012 portable storage-only cache successor

**Status:** `HARD_LOCKED_PRE_PAYLOAD_PRE_PHYSICAL_EXECUTION`

## Scope and claim boundary

This packet is the narrowly bounded audit-bound control-plane successor to
target V011, preserving every V005--V011 source, freeze, result, passing audit,
and obstruction record under exact hash custody.
V005 correctly constructed five storage-only caches, but its first independent
L4 `CacheContext` authentication stopped before physics because the active
Python rejects `Path.stat(follow_symlinks=False)`. The exact obstruction is
frozen at SHA-256
`be0608223cc97f1fa07c28cfa1fdbf77cf26cfffa5660eee719d5c879e8b1a2d`.
V005's gate and cache bytes remain preserved and ineligible for consumption.
V006 replaced only those four calls with portable
`os.stat(path, follow_symlinks=False)` and requires fresh cache construction at
the distinct canonical root `CACHE_PAYLOADS_V006`. Its independent hostile
audit nevertheless failed `2/277` control-plane attacks: cache authorization
did not bind the hostile audit itself, and the L12 schedule accepted unrelated
files under arbitrary hostile role labels. That immutable failure is recorded
at SHA-256
`f1a1d88c266c5e099b929d9cc38ec3008c662ebf70afafbd1a10c798ebf151f4`.
V007 preserved both earlier branches and repaired only those authorization
holes. Its frozen prepayload hostile audit passed `341/341`, its dual gate
authorized fresh storage-only caches, and all five caches were constructed.
The required first actual L4 `CacheContext` authentication nevertheless stopped
before physics because NumPy refuses to memory-map the authenticated zero-byte
`carrier_q_00_sources.i32` record. The exact V007 obstruction is frozen at
SHA-256
`a9cb384baef15fc72a61f0009b67d8e5aef95b14084f767b2168ef70efbd4d62`.
V008 retained the V007 zero-length repair, passed its independent prepayload
audit `366/366`, built five fresh caches, and passed an independent postbuild
payload audit `3483/3483`, including actual L4 and L12 `CacheContext`
authentication. The frozen V008 physical-gate validator nevertheless did not
require or validate that postbuild audit, so V008 is fail-closed before physics.
That exact binding obstruction is frozen at SHA-256
`2dc1cbedaf72579666e97404e624e1e974c015572c24c2f4d834d933e075f390`.
V009 introduced the noncircular postbuild-audit, base-gate, hostile-gate-audit,
and outer-control chain. Its independent hostile review replayed the frozen
preflight `285/285` but found five accepted bypasses: four malformed values for
the postbuild `checks` field and one extra-authority field in the base physical
gate. The exact V009 obstruction is frozen at SHA-256
`ff063573868b96aa14b1bdee218c4d6e2c039b8ba844e9753a21e7a48d8965fc`.
V010 required the exact postbuild check map and the exact base-gate key set,
but hostile review found that Python equality still admitted `True` for the
integer `1` and `1100.0` for the integer `1100`. It also found that the future
independent physical-gate audit schema did not itself attest the exact base
gate key census. The V010 hostile obstruction is frozen at SHA-256
`ae4238262273d5529c6a84985553669768714cfb5889e8793fdb52750dd927cf`.
That immutable failure record contains one malformed 63-character predecessor
digest; the separate custody correction that binds the actual V009 obstruction
without amending V010 is frozen at SHA-256
`3e8f129a4b36ed3f71ab7783d99e9f0cab3e23d5b9254c71eea6e94fc6b1f5d1`.

V011 retained those repairs and passed its frozen nonphysical preflight
`292/292`, but its independent hostile review accepted 16 malformed records in
six blocking classes: Boolean/float aliases for three audit pass counters,
float aliases in the postbuild payload and semantic censuses, integer aliases
for false absence entries, and float aliases in outer authorized-length lists.
That failure is frozen at SHA-256
`0dc595ff78e4fa5d81a42a285d3b74ce93758dd8bb42c836471bd3e3e898e2f6`.

V012 repairs all six V011 type holes with exact Python type tests. It also
separates universal base custody from stage-specific authority: the base gate
binds all five cache manifests, the control outer gate authorizes only L4/L6/L8,
a distinct audited control-stage record unlocks L10, and a distinct audited L10
stage plus the audited readiness schedule permits two one-way L12
authorizations.  Both immutable authorizations must precede a blocked-worker
handshake, and that handshake must precede the dual-worker release that unlocks
L12. Every new authorization,
audit, stage, schedule, and history JSON is read from a stable no-follow
read-only descriptor with duplicate keys and nonfinite constants refused.
Prior histories are reconstructed against the canonical V004 projections and
immutable terminal shards instead of accepting producer `PASS` fields.
Nested freeze/resource/telemetry/comparison records use recursive exact-type
comparison, so Python aliases such as `0 == False`, `1 == True`, and
`60.0 == 60` confer no authority. Legacy JSON evidence is strict-parsed from
the same stable descriptor that is hashed, and long cache/history operations
retain authenticated authority custody and reauthenticate it before
publication. Retained authority also requires the exact absolute path to equal
its resolved path before and after authentication and on every verification,
so replacing a parent directory with a symlink alias cannot preserve authority.
It retains the authenticated zero-length behavior and builds fresh at
`CACHE_PAYLOADS_V012`; it does not read, copy, link, or reuse V005, V007, or
V008 payload bytes, and V006, V009, V010, and V011 created no payload. No
physical operation is changed.

Four independent pre-freeze specifications are immutable inputs to this packet.
The obligation matrix at SHA-256
`49a1a5901249c0476ebd775d60b9342436e4391a2a97b9c08f1082247b719e77`
maps all 26 future artifacts, 17 promotion stages, six V011 findings, 18 V012
checklist items, positive fixtures, and adversarial mutation classes. The
authorization-state model at SHA-256
`182c73d94494b1c78aee8bbed7de7371519c9074461a74101b136eb9d7f5898c`
exhausted all `2^18 = 262144` PASS/PENDING states, found 26 legal states and
reached all 26, and refused all 4,718,124 invalid-state/action pairs. These are
control-plane specifications only; they grant no cache, history, or physics
authority.

The dual-launch coordinator packet is frozen by manifest SHA-256
`a6b6c61fa4e44cb53965b22c0fa0999c612a72cca9c90e31835bda3fa1a3336f`.
That manifest binds `README.md` at
`0a4b0694fca19f56c0628c3ad663859ac5697187af151f7e4501ab42f2f477db`,
`RESULT.json` at
`f7e6774fc8e308a6f601323393976ce0c1af23bfe6338148e18e46773a3ab3f9`,
`VERIFICATION.txt` at
`171bb3432a19d8a541f1a0ed0f772801c97f9046cb94af4b0d0b4ef1d4f642f1`,
`dual_launch_coordinator.py` at
`b4934b6603f923ab1039ae4aeb98d477e4ad6813b280e70a0ee1ba3667346406`,
`production_dual_l12_launcher.py` at
`095f8cd25499ea4f36cba913038cfbdadfe6e56309046370d4eeb03c347c1d71`,
`synthetic_fixtures.py` at
`ad887cf5a0b06df2f064faf4d31249afdd4899c2c6bb56b3e0336fe59dad8ba4`,
and `test_dual_launch_coordinator.py` at
`49294c74c9c6f4ab9bf3207bf1b80ef12445d448727b51be714c21b0e52aa2c9`,
and `test_production_dual_l12_launcher.py` at
`65baa98c07f3a07dc763b0b5f5619f5b453bdeb7a2ad4109bf96394ce2707d8a`.
It exhausts all 5,040 permutations of the seven-action launch DAG, admits only
the two target/hostile authorization sibling orders, and leaves every refused
transition state unchanged. This packet is a non-I/O integration contract;
the production release record retains the narrower production claim boundary.

The production-DAG refinement packet is sealed by manifest SHA-256
`6172bc362ef9bbe250fecfb8466882f10c534ed173ca29b5b01428054ea2ca6f`.
The target runtime authority binds exactly its three production dependencies:
`independent_final_auditor.py` at
`99677ffabeedc6db84047bd3637fd292e137d66c2de02eef66633ed789a92f2f`,
`production_dag_refinement.py` at
`ec84094f6d4df6cb22a6fbae2205242f51e8217261e47b5b0fb460d245da5d56`,
and `production_evidence_orchestrator.py` at
`d85275417f92961a2809822bcfc635d9e23e16bc7ad4fde43183ddcb78620b20`.
Test and fixture helpers are excluded from runtime authority.  The production
obligation dispatcher additionally hard-pins the exact final-auditor bytes it
executes.

The frozen `validate_preflight.py` turns every one of the matrix's 477
artifact/mutation assignments into an executed production-contract refusal
case. It constructs and accepts exactly 33 native-schema, artifact-specific
positive fixtures, including all eight A22 forms and 12 owner-once authority
instances, then dispatches all 36 mutation classes through the same artifact validators called
by live builder, consumer, coordinator, and final-auditor sinks.
For A23--A27, the 73 native sink refusals that are more specific than their
matrix mutation categories are frozen independently in the target dispatcher
and must agree exactly with the hash-pinned final-auditor map.
Writable-file, descriptor/path-replacement, and premature-artifact cases use
the corresponding production custody/absence hooks. The cases include raw duplicate-key and
nonfinite JSON, Boolean/integer/float aliases, unsafe path/hash and provenance
changes, writable evidence, descriptor/path replacement, cache and stage
bypasses, incomplete history and shard projections, target/hostile aliasing,
resource freshness, launch/telemetry, L10/L12 cross mismatches, premature
artifacts, and false-absence changes. No fixture is written at a
canonical gate, cache, workspace, history, telemetry, or final-audit path.

A passing run exclusively creates the read-only
`PREFLIGHT_MUTATION_LEDGER_V001.json` before the preflight result. Its exact
schema is `TARGET_V012_PREPAYLOAD_MUTATION_LEDGER_V001`; it binds this matrix,
the freeze, all five frozen source hashes, the production-validator module and
hook, 33 positive-fixture hashes, 477 mutated-fixture hashes, 477 per-case
mutation-evidence hashes, and the ordered 477-row refusal ledger. Every row
names the exact validator and hook and records exactly one executed production
sink call. The preflight result binds those 33 positive and 477 mutation sink
calls, the ledger identity and digest, and the validator-module digest. Before
publication, the result independently reconstructs its exact schema, claim,
nonexecution booleans, check census, five allocation rows, resource limits,
frozen-file bindings, compatibility flags, and ledger binding. A rerun after any source hash changes explicitly invalidates the
prior ledger rather than inheriting its PASS. The later independent prepayload
audit must independently reconstruct this ledger and replay the cases; the
target-produced ledger alone is not independent authorization.
Each `mutated_fixture_sha256` is the canonical mutation-receipt digest over the
artifact ID, mutation class, raw mutated-byte digest, and mutation-evidence
digest. Thus two semantic classes cannot claim separate coverage by replaying
the same mutated bytes; all 477 receipt digests must be distinct.
The complete freeze and sealed-dependency census is reauthenticated after the
mutation suite, immediately before ledger publication, and again before the
preflight result publication. Drift in the delegated independent final auditor
therefore cannot hide behind unchanged target source hashes.

The target preflight does not serialize the independent hostile nonphysical
preparation branch. It permits already-sealed hostile method, builder,
consumer, preflight, freeze, preflight result, and prepayload-audit records.
It still requires the hostile cache-build and L10/L12 authorizations, entire
V004R4 cache payload root, cached-L10 gate, hostile postbuild payload audit,
physical-output and workspace
roots, and every shared cross/schedule/handshake/release/telemetry artifact to
be absent. Thus source review can proceed in parallel, while payload and
physical promotion remain fail-closed.

The V012 source quintet, freeze, and both new audit-preparation packets are
sealed without write bits and authenticated through stable no-follow
descriptors. Older hash-pinned V003/V004/V005--V011 parents retain their
historical repository modes and are treated only as explicitly declared legacy
evidence; V012 does not silently reinterpret a writable legacy mode as a new
authority record.

The original target-V004 `TARGET_L12_GATE_V004.json` is a required immutable
parent: it records the passing 273/273 L4, L6, L8, and L10 target controls. The
48/48 preserved-workspace custody observation and its frozen cross-diagnostic
are also required parents. The latter found target/hostile differences no
larger than `1.05e-12` for q=0..10 but `4.826848271244497e-5` for q=11. It is
therefore only a diagnostic of incomplete coarse states, not a completed
history, restart state, or target/hostile equivalence result. Those preserved
workspaces remain evidence and must never be consumed or mutated by V012.

The cache serializes only immutable index data which target V004 otherwise
reconstructs.  It retains every carrier occupation mask and every canonical
lineage mask in the target `fixed_words` order.  It changes no state vector,
basis state, coefficient, operator, graph, edge order, current orientation,
write rule, predicate, observable, numerical method, tolerance, or stopping
rule.  There is no quotient, truncation, sampling, surrogate, or hash-based
reconstruction of physical state.

ALLOW remains the characteristic fresh-cell projector, REQUIRE remains the
branchwise cost/lineage audit, and SELECT remains the exact owner-once
trajectory.  The `-1` exchange coefficient, `Phi=pi/4`, dwell `pi/2`, rough
and sharp resolutions, connector definition, and ledger residuals are those
of frozen target V004.  The terminal event continues to stream both exact
children from immutable `H_(L-1)` rows; no `H_L` array is created.  Sharp
`H_11` remains the retained terminal record.

## Immutable payload

For every `q=0,...,L`, the hash-pinned target builder's payload contains:

```text
carrier_q_Q_words.u32       all C(2L,q) carrier masks in target order
carrier_q_Q_offsets.u64     3L+1 offsets in target graph order
carrier_q_Q_sources.i32     concatenated occupied-u/blank-v source ranks
carrier_q_Q_targets.i32     matching XOR-toggled target ranks
```

For every event `n=0,...,L-1` and old charge `q=0,...,n`:

```text
admission_n_N_q_Q_blank.i32       blank old-carrier column ranks
admission_n_N_q_Q_destination.i32 exact q+1 target-column ranks
```

For every canonical prefix basis `n=0,...,L-1`, all masks are serialized as
`lineage_n_N_q_Q_words.u32`.  For nonterminal `n=0,...,L-2`, the exact stay
and accepted row maps into prefix `n+1` are serialized as `i32` arrays.
Every payload file is immutable, byte-counted, and SHA-256 pinned.  A future
target cache must be built by this target builder and must never consume or
share hostile cache payload bytes.

## Exact resource certificates

All byte counts include raw array bytes, including edge-offset arrays.  At
L12:

```text
carrier basis/exchange/offset arrays       744,528,576 B
carrier admission maps                     81,676,960 B
canonical lineage masks                        16,380 B
lineage stay/write row maps                    16,376 B
complete cache payload                     826,238,292 B
V004 maximum live H10+H11 state          8,773,664,640 B
state plus cache                          9,599,902,932 B
terminal cache/index conservative peak      234,782,536 B
authentication cache conservative peak      252,944,080 B
maximum certified cache window              252,944,080 B
```

The fixed gates are:

- V004 numerical Krylov workset: at most `1,000,000,000 B`;
- terminal amplitude window: at most `512 MiB`;
- cache payload plus live state plus reserve: below `20 GiB`;
- free scratch before payload build or physical execution: at least the
  exact size-specific combined certificate plus `1 MiB`;
- conservative simultaneously mapped cache indices: at most `512 MiB`;
- cache-builder RSS: at most `4 GiB`, wall: at most `21,600 s`;
- physical consumer RSS: at most `16 GiB`, wall: at most `21,600 s`.

The target and independently implemented hostile L12 histories are scheduled
concurrently only after the L10 cross-gate passes. Their two `16 GiB` process
caps plus their two conservative `252,944,080 B` authentication peaks give the
frozen additive launch bound

```text
2 * (17,179,869,184 + 252,944,080) = 34,865,626,528 B
```

This is `32.471 GiB`. It leaves `13,134,373,472 B` (`12.231 GiB`) on a
decimal 48-GB host, or `16,673,981,424 B` (`15.529 GiB`) on a 48-GiB host.
The target and hostile scratch minima are respectively `9,600,954,452 B` and
`9,600,935,128 B`.  The target includes its NumPy headers; the independently
implemented hostile path preserves raw `.c128` shards and native Chebyshev
telemetry.  The two scratch minima sum to `19,201,889,580 B`.
A separately created
`AUDIT_R_L12_PARALLEL_EXECUTION_V001/SHARED_AGGREGATE_SCHEDULE_GATE_V001.json`
is one shared target/hostile readiness record. Its exact schema is
`V012_DUAL_L12_READINESS_SCHEDULE_V001` and its classification is
`READY_FOR_INDEPENDENT_SCHEDULE_AUDIT`. It binds the exact target/hostile L10
cross-gate and canonical, pairwise-distinct executable, workspace, and output
paths for both workers. It contains no authorization, handshake, or release
record. The independent schedule audit has schema
`V012_DUAL_L12_READINESS_SCHEDULE_AUDIT_V001`, classification
`PASS_INDEPENDENT_PREAUTHORIZATION_READINESS_AUDIT`, and must reconstruct the
schedule, cross-gate, exact types, two-role custody, resource arithmetic,
freshness, and telemetry absence before either L12 authorization may exist.
At schedule capture it must contain measurements no more than 300 seconds old,
report `NORMAL` memory pressure, at least `48,000,000,000 B` total host memory,
at least `34,865,626,528 B` currently available memory, and at least
`19,201,889,580 B` available on the shared workspace filesystem. The consumer
checks every bound and hostile artifact hash before accepting the schedule.
This readiness schedule supplements rather than weakens either per-process guard.
It preregisters the byte-identical central telemetry path
`AUDIT_R_L12_PARALLEL_EXECUTION_V001/SHARED_AGGREGATE_TELEMETRY_V001.json`,
which must be absent before release. The schedule is valid for at most 300
seconds and declares a maximum dual-worker release skew of 60 seconds.
After an L12 worker atomically publishes and reauthenticates its immutable
history, it sends one bounded canonical
`V012_L12_WORKER_COMPLETION_V001` frame containing the exact process/channel
identity and output path/hash.  The worker then shuts down only its write side
and remains live until the coordinator has authenticated both completion
frames and closes the channel; any returned or trailing byte refuses.  This
terminal-live barrier applies only to L12 and does not alter L4--L10 execution.

Logical allocation arithmetic is proved by the nonphysical preflight.  It is
not empirical RSS or runtime evidence.  During a future physical run the
consumer checks RSS and elapsed wall time at least once per second while the
Hamiltonian is active, and at each admission charge boundary.  Crossing a
limit raises before an output record can be written; any partial workspace is
left intact as obstruction evidence.  The final record also reconstructs the
logical scratch, numerical workset, RSS, and wall gates rather than accepting
a producer boolean.

## Hard-lock sequence

`DUAL_OBSTRUCTION_AND_COMPATIBILITY_GATE_V012.json` is absent at freeze. The builder
and consumer refuse before creating a payload, history output, or workspace
unless that future gate:

1. has classification
   `AUTHORIZE_TARGET_V012_FRESH_CACHE_AFTER_V005_V006_V007_V008_V009_V010_AND_V011_CONTROL_PLANE_OBSTRUCTIONS`;
2. pins this method, builder, consumer, preflight, and freeze;
3. hash-pins exactly one target and one hostile six-hour obstruction record,
   the V005 runtime-compatibility obstruction, the V005 dual gate, all five
   superseded V005 cache manifests, the V006 hostile-audit obstruction, the
   V007 prepayload audit and dual gate, all five superseded V007 cache
   manifests, the V007 runtime-compatibility obstruction, and the complete
   V008 custody set including its passing postbuild audit and binding
   obstruction, the frozen V009 hostile-audit obstruction, and both the frozen
   V010 hostile-audit obstruction and its separate custody-correction record,
   plus the frozen V011 source, freeze, preflight, and hostile-audit obstruction;
4. binds the exact path and SHA-256 of
   `AUDIT_R_L12_TARGET_STORAGE_CACHE_V012/HOSTILE_AUDIT_RESULT_V001.json`,
   whose exact schema/classification, complete frozen-source hashes, freeze and
   preflight-result hashes, exact check map and reconstructed total, zero
   failures, no-symlink assertion, exact Boolean absence census, and claim
   boundary are revalidated by the
   builder before the cache root can be created; and
5. verifies for each six-hour record the exact schema, role, L12 size, unresolved
   status, V004 implementation/method/freeze custody, original 21,600-second
   limit, an elapsed duration at least that limit, no completed physical
   output, and classification `SIX_HOUR_RESOURCE_OBSTRUCTION`.

Each obstruction record must separately hash-pin an execution log and a
distinct JSON wall-monitor record.  The monitor has schema
`L12_WALL_MONITOR_EVIDENCE_V005`, exact target/hostile role and implementation
hash, `wall_limit_seconds=21600`, observed duration at least that limit, and
`termination_reason=WALL_LIMIT_REACHED`.  The four evidence paths and the two
obstruction records must be globally distinct in both path and digest. The gate is not a runtime guess: both
six-hour records are mandatory.

Physical execution additionally requires a future universal base
`PHYSICAL_EXECUTION_GATE_V012.json` that pins the obstruction gate, cache
manifests, consumer, method, freeze, original target gate, custody observation,
incomplete-state disposition, and the exact path/schema/SHA-256 of a passing
independent V012 postbuild payload audit. An independent hostile audit must
then verify that exact base gate. For L4, L6, and L8 only, the final unlock is
`CONTROL_EXECUTION_AUTHORIZATION_GATE_V012.json`, which exact-hash-binds the
base gate, postbuild audit, and physical-gate hostile audit and authorizes only
those three controls. The base gate alone never authorizes a history. Cache
authentication completes before any physical workspace or output is created.
Authentication rejects extra files, directories, symlinks, writable cache
members, wrong bytes or hashes, noncanonical mask order, wrong edge offsets, out-of-range or
noninjective ranks, incorrect oriented XOR exchange, altered fresh-cell
admission, and altered owner-once lineage destinations.

The cache root is canonical, nonsymlinked, and mode `0555`; every payload and
manifest member is an ordinary nonsymlink file with mode `0444`. Authentication
opens every member once with no-follow read-only descriptors, hashes those
descriptors, and constructs all later memory maps from descriptor duplicates.
It verifies canonical parent-path identity plus path/device/inode/size custody
and rehashes the still-open descriptors after the history. A writable-directory
replacement, parent rename-plus-symlink alias, or post-authentication path swap
therefore refuses before result publication.

Cached histories are staged. L4, L6, and L8 must all complete and be
hash-pinned by `CACHED_CONTROL_L4_L8_GATE_V012.json`, and that stage record
must pass the independent
`CACHED_CONTROL_L4_L8_GATE_AUDIT_V001.json`. Only then may the distinct
`L10_EXECUTION_AUTHORIZATION_GATE_V012.json` unlock L10. L10 must in turn be
hash-pinned by `CACHED_L10_GATE_V012.json` and independently accepted by
`CACHED_L10_GATE_AUDIT_V001.json`. L12 remains locked until both reconstructed,
audited stages, the exact independent target/hostile L10 cross gate
`TARGET_HOSTILE_L10_CROSS_GATE_V001.json`, and the independently audited shared
readiness schedule pass. Every
staged history is compared field-by-field with the canonical V004 finite
history: discrete data and event structure exactly; finite physical values to
absolute tolerance `1e-8`; solver telemetry by exact schema, convergence, fixed
24-node fine quadrature, and frozen resource bounds. The terminal q census,
shape, byte count, and SHA-256 must equal the canonical V004 manifest, while
the packet-local shard is opened immutably and rehashed through the same stable
descriptor. A resource or numerical miss can preserve an incomplete workspace
as evidence, but no physical output JSON is written.

The L12 target is additionally hard-locked on the fresh dual-worker readiness
schedule described above. Failure of host capacity, available-memory,
memory-pressure, filesystem, freshness, or hostile-custody checks refuses the
target before L12 workspace creation. This supports safe parallel activity;
it does not authorize either implementation to consume the other's cache or
workspace.
After the independent schedule audit exists, distinct immutable
`TARGET_L12_EXECUTION_GATE_V012.json` and
`AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/HOSTILE_L12_EXECUTION_GATE_V004R4.json`
records must each bind the readiness schedule, schedule audit, exact L10
cross-gate, role consumer, and role L12 cache manifest. Their exact schemas are
`TARGET_V012_L12_ONE_WAY_AUTHORIZATION_V001` and
`HOSTILE_V004R4_L12_ONE_WAY_AUTHORIZATION_V001`; neither one-way record may
launch a worker by itself.

Both authorized workers are prelaunched in a blocked state without creating a
workspace. Only after their identities, paths, readiness epochs, NORMAL memory
pressure, schedule/audit hashes, and both authorization hashes pass may the
coordinator seal
`AUDIT_R_L12_PARALLEL_EXECUTION_V001/DUAL_L12_LAUNCH_HANDSHAKE_V002.json`
under schema `V012_DUAL_L12_BLOCKED_WORKER_HANDSHAKE_V002`. Only that immutable
handshake may permit
`AUDIT_R_L12_PARALLEL_EXECUTION_V001/DUAL_L12_WORKER_RELEASE_V002.json` under
schema `V012_DUAL_L12_WORKER_RELEASE_V002`. The release binds both exact worker
identities and authorization hashes, reconstructs deterministic per-role
release tokens, and limits release skew to 60 seconds. Any missing sibling
authorization, embedded schedule handshake, early workspace, early telemetry,
or one-role release refuses closed.

After atomic target L12 history publication and reauthentication, the target
consumer sends its exact completion frame, shuts down only the write side of
its authenticated control channel, and waits for coordinator EOF without
trailing bytes.  The coordinator must preserve all 12 owner-once authorization,
READY, handshake, release, command, ACK, and completion records before postrun
telemetry is accepted.  A later final adjudication remains externally locked on
both target and hostile L12 outputs plus telemetry that binds the schedule
audit, all 12 authority records, and both output hashes. A schedule-audit pass
is not a terminal target/hostile comparison and cannot be promoted as one.

At freeze, only syntax checks and exhaustive index/allocation/lock preflight
are authorized. The V001 preflight also executes the complete 477-assignment
mutation matrix, attacks frozen-file/dependency/resource mutations, exact
record types, strict JSON parsing, staged-DAG reachability, prior-history
reconstruction, and cross-row evidence aliasing. It also executes the portable
`os.stat` form on this interpreter. V005 through V011 results remain external predecessor evidence;
no V012 cache payload and no physical history may be generated before the
V012 freeze, preflight, and independent hostile audit pass.

## Claims

The preflight may prove only index identities, exact storage arithmetic, and
hard-lock behavior.  A future cache build would produce authenticated storage
indices only.  A future execution would remain a finite empirical history
requiring independent hostile comparison.  Spectral scaling, `z=1`, a
thermodynamic phase, continuum behavior, spacetime algebra, universal
coupling, emergence, and gravity remain open.  No grid, graviton, Ward axiom,
reservoir, or continuum assumption is introduced.
