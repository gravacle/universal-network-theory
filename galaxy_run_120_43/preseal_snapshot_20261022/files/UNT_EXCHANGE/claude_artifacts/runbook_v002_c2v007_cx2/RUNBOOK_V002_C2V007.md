# RUNBOOK_V002_C2V007 — review candidate, A253

date -u: Wed Oct 21 10:36:02 UTC 2026

Status: **UNTESTED in production; not adopted.** Claude2 is coordinator and sole scientific launch owner. This build/review delivery authorizes no launch, target read, score, or change to an existing artifact. Root review and adoption remain separate. Every path in a runtime pin is absolute; every SHA256 is computed from the exact bytes read. Writes use new names and exclusive creation.

This is the complete current workflow description for the c2v007 builder. The c2v006 runbook is historical where its retry, cap, snapshot, custody, geometry, M15, or TSR text differs below. Step numbers 1–10 remain unchanged. Phase 1 executes registration before its first replay pass because it has no sensitivity calls.

## Reviewed inputs and evidence scope

| Existing source | SHA256 from bytes |
|---|---|
| `roster_builder_c2v007_a253_v001.py` | `799fb2d002ba39885326f161e1efbe3ad35dd2b66d3c84f961ddce910e9cd15b` |
| `../phase1_ngc_launch_kit_cx2v004/phase1_ngc_launch_cx2v004.py` | `8cec1b56fc682f638fee57329eefc9b3cddfa47959d175e7095fc0c5fe0342c9` |
| `../freeze_score_readiness_cx3/v003g/prediction_freeze_c2v003g_cx3v001.py` | `48a1e48a5230fff346705c338da30a8ee53a8643193dbe4616c25e61eab3d405` |
| Historical `../runbook_v002_c2/RUNBOOK_V002_C2V006.md` | `e162db3e7bcaf348db2455aac9032ac8b0c57bb536ec97d043b6d9aad084349b` |

TESTED claims in the delivery concern invented files, saved receipts, static computations and replay only. No real slots, observed or target velocities, scientific runs, forbidden run trees, or session logs were read. The root-pinned cause producer is read as source bytes for its identity; the builder never executes it. Its production classifications and root adoption are UNTESTED here. Runtime output names below describe files to be generated; their hashes are computed when those files exist.

## 0. Preconditions and controls

Root pins the adopted runbook, builder, launcher, frozen spec-of-record, gate documents, receipt contract and phase inputs before the operation that uses them. Full 64-hex hashes are required; prefixes are not pins. This review candidate alone establishes no production gate.

The adopted ceilings are Phase 1 **2026-11-06T05:59:00Z** and Phase 2 **2026-12-01T05:59:00Z**. The interruption policy refuses a different ceiling. Phase 1 is a reporting and freeze boundary: it does not stop work that continues toward Phase 2. The launcher uses remaining Phase-2 time for the monitor wall cap.

G28 remains **OPEN_ROOT_RULING**: Claude2 must fix one absolute step-7 ledger root outside build directories, and register it before the first FULL build. This lane supplies no default. Changing that root is a new root event, not a way to reset a ledger.

A218 operational errata: use **guard 014 / launcher 015 / binder 011** as the stated version chain, subject to their adopted pins. **PRELAUNCH005 / guard011** remains a **candidate**, not an adopted replacement. No example in this runbook substitutes that candidate for an adopted guard.

M15 uses the kit's exact 15-key prelaunch record, its nested V006 hash/byte count and its date/epoch binding. Root preserves the exact logged V006 bytes. The builder checks every captured seed/twin launch receipt against the prelaunch time and the complete captured launch set. A launch time alias is not an accepted replacement for `utc`.

Every build stage carries the saved `spec_of_record` pin. DN1: **steps 1a and 1b use the saved spec-of-record**, not reconstructed defaults. **Step 8 installs V-N1 `geometry_runtime`** around the final writer. This is also required when the saved pass contains the approved invalid-geometry answers.

Runtime Python is the program's prescribed isolated interpreter, single-thread BLAS, `-I -B`, under `nice -n 10`. Local checks attempted that priority; this host reported `setpriority: Operation not permitted`. They otherwise completed under the specified interpreter and thread environment.

## Receipt and interruption contract

The literal status map has 54 exact entries; its canonical-byte SHA256 is `c36c37886aa67db763160681be99904c3ae9f22ebb51f3e841adadfa0e1cdb54`. No wildcard, substring classification, or default class is allowed. The nine receipt roles are `status` mapped to `raw_status`, plus `time_utc`, `spec_sha256`, `theta_sha256`, `rss_cap_bytes`, `wall_cap_s`, `host_ram_bytes`, `other_ngc_processes_max`, and `output_cap_bytes`.

The builder independently re-derives each closed attempt from its monitor receipt and pinned launch, registry, sample and stop records. It verifies the monitor self-hash and projection. A missing, incomplete, same-second lead, short tail, or gapped solo sample yields null; null is never evidence of zero other processes. Both counted model failures must have full evidence and be solo. Attempt zero must supply its required minimum even when a later pair is counted. Twin rerun RSS is eleven host RAM.

CAP, output-cap, signal, root-stop and other nonphysics outcomes never count as model failures. Output cap doubles on retry; wall cap is not doubled. Identical-spec retries continue subject to launcher admission and the adopted ceilings; there is no attempt-count abandonment.

A counted model pair has two distinct monitor receipts with the same spec, driver, status, failing stage, failure code, exception class and raise-site identity. A positive value-free cause is restricted to `ROUTE_A_NO_FIXED_POINT` or clean `ITERATION_BUDGET_EXHAUSTED`, with the required model status and all five bound hashes. `SITE_SET:` and `CLASS_SET:` strings are compared exactly, never followed as paths.

The exact value-free cause keys are `status`, `failing_stage`, `failure_code`, `exception_class`, `raise_site`, `bound_shas`, `model_outcome`, `model_outcome_reason`; `bound_shas` has `receipt`, `result`, `finish`, `spec`, `driver`. The builder binds the monitor, spec, driver and available result pins without opening finish/result for cause classification. The producer must be root-pinned in the frozen V006 no later than T. A missing result hash cannot authenticate a positive model pair.

Two consecutive identical solo FAILED statuses without authenticated causes produce `HELD_FOR_CAUSE`. Two repeated REFUSED/BLOCKED statuses produce `HELD_FOR_FIX`. Neither is a failure terminal, an automatic retry authorization, or UNEVALUATED before the ceiling. No automatic hold release is invented.

`INTERRUPTION_POLICY_C2V002` has exactly `schema`, `phase`, `cause_producer`, `deadline_utc`, `deadline_registration`, `attempts`, `closures`. Each attempt-policy row has `receipt`, `cause`, `root_stop`. Cause and root-stop pins may be null. The reviewed producer pin may be null only when no cause is supplied.

A bound root stop is nonphysics. Its record has `schema`, `date_u`, `call`, `launch_json`, `registration`, and its time must fall within that attempt. This root-stop record form is a review interface; separate root acceptance is not implied.

An identity twin is PLANNED_STOP only with its exact bound watch record: schema, designed reason, run directory, launch pin, child process group and successful watch-stop result. STOPPED_* alone is insufficient.

Natural terminal states are FINISHED, a permitted bound twin PLANNED_STOP, or the first authenticated model pair. No later attempt can undo a terminal prefix. Run directories are distinct and disjoint, receipt times strictly increase, and every receipt belongs to its registered spec and exact theta.

## Phase 1

**1a. Selection.** Use the registered budget-exhausted calibration record and saved spec-of-record. Save the selection by exclusive creation. Do not read target velocities.

**1b. Exact theta plan.** Run the builder's PLAN stage with that same spec. Run the budget-zero planning operations for the evaluated alternatives and save their value-free outputs. No evaluated values belong in a PLAN. The P112 context reconstructs the planned calls from selection, PLAN, FDPLAN, handoffs, fills, certificates and registered specs. It compares actual theta bits; one ulp differs. S0 reuse must pass all physical-bit checks, not merely an equal point key.

**1. Scientific attempts.** Claude2 alone owns launches. This builder has no launch operation. Each actual attempt has its own immutable run directory and saved custody. P112's admission, memory and residual checks remain required. No-run-directory and wrong-spec observations are nonattempts; they cannot silently become model failures. F points and the identity twin enter OTHER calls, not the member roster.

**3. Gather existing custody.** Preserve receipts and pinned dependencies. A roster call carries its own result/cut pin or explicit null as allowed by its disposition. No borrowing another call's file by path, inode or receipt hash. A cut record resides inside its terminal run directory and no other call's run directory. Distinct honest calls may have byte-identical cuts; FINISHED results retain the cross-call content check.

**4. Capture the Phase-1 boundary and register.** Use `phase1-snapshot` with a pinned `PHASE1_SNAPSHOT_INPUT_C2V007` input containing exactly `schema`, `launcher`, `config`, `interruption_policy`. The launcher/config are the reviewed P112 interface. The new output directory must not exist. The command gates on P112's root tool pin and checks both mounts before capture.

The snapshot captures the complete planned call set, including calls never launched, actual registry entries where present, existing launch/attempt custody, nonattempts and pending observations. It fabricates no launch entry, closed receipt, run directory, result or sample. If a monitor receipt completed by the ceiling still needs the normal custody close, the command refuses until that close is performed.

Only closed attempts ending by the Phase-1 ceiling are eligible. T is the maximum terminal time when every planned call is terminal by that ceiling; otherwise T equals the ceiling. Snapshot creation time is separate. An incomplete snapshot before the ceiling is refused. An ordinary all-terminal freeze before the ceiling is allowed.

Each incomplete call receives a `SCHEDULE_CEILING_CLOSURE_C2V002` with exactly `schema`, `phase`, `date_u`, `deadline_utc`, `deadline_registration`, `call`, `last_receipt`. The call is its registered five-field identity; the last eligible receipt may be null. `n_attempts=0` means no eligible closed attempts, not a claim that no operating-system process ever started. Saved pending and launch records preserve that distinction.

The output includes the exact V006 copy, a five-field-per-call launch registry, the snapshot, closure records, the final interruption policy, cutoff record and a build-input patch. The patch supplies the registry, verification pins, policy, gate cutoff and exact eligible attempt lists. Runtime output hashes are returned from the exact buffers written.

The builder verifies the saved snapshot and its source hashes; it never re-scans current attempt histories to reinterpret Phase 1. The V006 parser uses the frozen bytes. Later Phase-2 receipts, entries or mutable V006 text cannot change the saved proof. Historical absence and liveness observations remain explicitly root-trusted observations; hash verification is not a retroactive proof of absence.

Run the FULL build using the patch and saved inputs. Phase 1 has no separate MEMBERS stage. A snapshot-backed empty attempt list is allowed only with its valid call-keyed closure. Its class is SCHEDULE_CEILING, disposition UNEVALUATED_SCHEDULE_CEILING, and result/cut are null. Nonempty attempt lists must exactly equal the saved snapshot lists.

The gate cutoff is the byte buffer copied and hashed. Its record binds T and the actual non-null terminal/last-eligible receipt pins. The record date cannot precede T. One corrective successor is permitted only for the defined early-date defect; it cannot create an arbitrary new cutoff. A gate or producer first pinned after T is not retrospectively usable.

**4a. Gate list and report.** Produce the exact schema-bearing gate list and the separate evidence report. The report checks M15's nested fields, date/epoch and complete launch coverage. Root pins generated records without hand editing.

**2. First replay pass.** Under the FULL build and its rosters, run PASS_ONE in process. Replay saved states only. Phase-1 sensitivity budget is zero. The command writes a validity-only pass record; it does not write prediction arrays. The chosen D1 member and exact saved result pins are retained in that record.

**5. Custody and registration.** Save the six roster pins, builder/build record, replay plan, source input pins, gate list/report and custody copies. The custody root is outside and not an ancestor of run trees. Copies are byte-identical and distinct files; they must survive loss of the original. Empty attempts require no invented receipt/result copy.

**6. Seal and reading gates.** Root's adopted seal and reading gates are prerequisites to any later value release. The runbook, a successful build, or a passing synthetic test grants no target or score permission. Preserve the frozen registration and source pins.

**7. Consistency replay and ledger.** PASS_K uses the same admitted plan. `step7` compares validity and appends a hash-chained result under the fixed G28 root. A discrepancy makes the affected member UNEVALUATED and generates a machine successor plan; it never writes a successor roster. A superseded plan cannot be compared or replayed again. Each ledger read re-derives results and successor bytes from saved evidence. Root records the head hash; deletion of a final entry is not independently detectable without that external record.

G16: first verify the registered source. If it fails but a same-SHA custody copy exists, require root restoration rather than mark the member UNEVALUATED. Only when both sources are absent/bad may `custody` append its machine CUSTODY transition, lower budgets and reset sensitivity. Missing run volumes stop processing. Phase-2 sensitivity-only custody remains OPEN_ROOT_RULING; no format is invented.

**8. Final freeze.** After the adopted seal/reading gates, run a final PASS_K in process against the current admitted plan. Require exact byte equality with the ledger head's PASS_K and a NO_NEW_DISCREPANCY head. The freeze writer consumes only those in-memory outputs and the unchanged roster mapping. Its `allow_incomplete` is the builder-derived value, not an operator toggle. Phase 1 uses true.

V-N1: the only approved invalid-geometry exception is an exact `NGC3198_NUISANCE` sensitivity entry differing from registered geometry. It is answered in memory with GEOMETRY_NOT_EXPOSED, false validity and null rows/speeds. It creates no forward call, context or replay-index entry, consumes evaluated budget, and never triggers DN5. `geometry_runtime` temporarily applies the narrow result-row and frozen-row adapters and restores both. Any finite row or other sensitivity kind refuses. The G26 wrapper delivery remains a separate task; this runbook does not claim that wrapper is already implemented or adopted.

**8a. TSR and pre-target checks.** `tsr-support` binds the current NO_NEW_DISCREPANCY ledger head, its byte-equal PASS_K, D1/FDPLAN member identity, extractor policy and compare record. It emits the exact nine-key support projection with the original policy slots-pin spelling. That command never opens the slots pin. `tsr-check` requires both the support record and projection input; an arbitrary prior pass or a pending support placeholder is insufficient.

**9-pre. Seal check.** Verify the adopted source/registration pins and unchanged six-roster mapping. Log manifest and registration hashes, phase/calibration record, L1, build record, ledger directory/head and the completed pre-target checks before any target read.

**9. Score.** Only Claude2's separately authorized scoring workflow may open targets. The Phase-1 score is provisional and incomplete. No target operation is supplied or executed by this build/review lane.

**10. Denominators.** PRIMARY retains denominator 43; registered INVALID nulls are misses. Phase-1 STAGE0 is not evaluated or scored. ORIGINAL_K is unavailable as prescribed by the registered phase rules. No post-target change to roster, cut, reference or denominator is allowed.

## Phase 2

Before the Phase-1 score, root fixes the committed rule set and Phase-1-score V006 cutoff, with the sealed module/slots version. A later scientific rule change follows the exploratory commitment treatment; this lane does not decide it.

**1a/1b** use the campaign's own calibration record, disjoint phase root, saved spec-of-record and budget-zero plans for every evaluated alternative. **1** belongs to Claude2's launcher workflow. Phase-1 reuse requires exact theta, driver, allowed spec re-binding and roster-input/cut agreement; it is not granted merely by an equal hash in an unrelated call.

**2** builds MEMBERS and runs PASS_ONE to establish D1. **2b** saves the whitelist-only sensitivity plan. **2c** registers the required sensitivity calls. Approved V-N1 geometry entries are in-memory invalid answers, without a launch. **3–4** gather and register the complete phase call set with the phase cutoff and FULL build. The saved entry-source verifier supports the Phase-2 registry interface; production producer adoption remains UNTESTED.

**4a–6** preserve gate/M15 evidence, custody, original rosters and seal/reading gates. **7** repeats the consistency ledger process. If D1 changes, compute its budget-zero sensitivity plan in memory and derive the leading available-call/geometry-answer budget. It creates no new scientific call. Discrepancies remain UNEVALUATED even if a later replay agrees.

At the Phase-2 ceiling, incomplete calls use bound schedule closures. DN5 sets `allow_incomplete=True` for UNEVALUATED_STEP7_DISCREPANCY, UNEVALUATED_CUSTODY_BREACH or UNEVALUATED_SCHEDULE_CEILING in evaluated members or primary sensitivity entries. Approved geometry answers alone do not trigger it. Otherwise the value is false. **8–9-pre** use the final in-process, ledger-equal PASS_K and the same unchanged roster mapping. **9** is the separately authorized score of record. **10** uses 43 for PRIMARY/ORIGINAL_K and, only if STAGE0 is evaluated under the adopted successor, its registered eight-query non-headline denominator.

## Public interfaces and verification limits

The existing builder input schema name is retained, but c2v007 requires `spec_of_record` at every stage and `registry_verification`, `custody`, `interruption_policy` at MEMBERS/FULL. Phase-1 FULL also binds the cutoff record. `verify-registry` accepts either the prior completed P112 assembly proof or the A253 `{launcher, config, snapshot}` proof. These alternatives are explicit and do not silently fall back after a snapshot refusal.

Commands are `build`, `pass`, `step7`, `custody`, `sens-budget`, `verify-registry`, `phase1-snapshot`, `check-gate-list`, `seal-check`, `tsr-record`, `tsr-support`, `tsr-check`. The snapshot command takes `--input`, `--input-sha256`, `--out-dir`. No scientific launcher, monitor runner or target-scoring command exists here.

A226 applies one guarded byte snapshot per immutable path/file identity per public command, shared across the builder, P112 verifier and freeze module. Hashing, parsing and custody copies use that same buffer. Restoring mutation tests cover removal of the cache, stale live-history rechecks, source hashes, terminal/T derivation, call and closure binding, cause identities, root stops, solo evidence, RSS, cutoff, custody, M15, geometry, TSR and delegated G27 checks.

TESTED: synthetic real-context PLAN reconstruction, never-launched/pending/mixed/late Phase-1 capture, future-file independence, full zero-attempt builds, inherited replay/ledger rules, value-free cause classification and immutable-output/read fences. UNTESTED: production data, real liveness/clock races, real launch admission, real source-restoration operations, cause-producer adoption, complete production freeze/score, and the forthcoming G26 wrapper. No synthetic result is a scientific result.
