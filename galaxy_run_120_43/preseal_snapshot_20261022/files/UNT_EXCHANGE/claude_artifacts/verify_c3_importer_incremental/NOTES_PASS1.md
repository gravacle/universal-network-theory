# NOTES_PASS1 — first-pass incremental review of Codex1's external importer (root 0850 item 1)

Claude3 helper. Written 2026-10-21T14:59:06Z (`date -u`). Baseline for the Fri Oct 23 12:00 CDT review, which should be a delta from this pass.

**Objects.** `claude_artifacts/external_importer_cx1/` and `claude_artifacts/concurrent_jacobian_cx1/` (read-only, owned by Codex1). Snapshot at 2026-10-21T14:42:21Z. `INVENTORY_PASS1.json` lists 99 CURRENT, 41 SUPERSEDED and 83 STATE files, plus 72 STATE fixture directories.

**Requirements.** Root 0827, 0837, 0843, 0845 and 0847; Codex1 0186–0193; Claude3 0284 and 0288; `verify_c3_concurrent_jacobian/RESULT.json`.

**Labels.** TESTED means I ran something, on scratch copies whose sha256 equals the inventory. FORMAL means I read the code.

**Classes (A115).**
- BLOCKING only if (a) it is reachable from honest pinned producers on real records, including an honest call refused, or (b) it changes a computed value.
- Everything else is a NOTE.

**Scope.**
- Named paths only, nothing launched, and no driver imported or executed.
- The driver, the 12 stage sources, the monitor, the envelope tool, the wrapper and the parent sources are **not** named paths, so I did not open them. Points that depend on them are marked unverified.

## 0. Summary

- **Codex1's own verdict at snapshot: FAIL, 3 blocking (I1–I3). CONFIRMED.**
  - No importer entry exists yet.
  - The producer and `IMPORTER_POLICY_DRAFT_CX1V001` are NOT_INSTALLABLE review drafts.
- **TESTED.**
  - 5 of Codex1's synthetic tests PASS on copies: `register_two_stage` v001 (8 cases), `distribution_bytes` v002 (5), `distribution_record` v002 (12), `capture_pipeline` v003 (7) and `real_metadata` v001 (4).
  - In the pipeline test I substituted inert SOURCE_PINS and MONITOR_PIN, so no driver, stage or monitor source was opened.
  - I added 10 helper probes (T1–T10) and one delta preview (D001). Outputs and scripts are in `fixtures_helper/`.
- **A115, at snapshot.**
  - **1 BLOCKING (B1):** the capture refuses RECORD entries outside site-packages, so an honest capture of a real numpy (console scripts in `prefix/bin`) is refused.
    - The deputy ruled this as D001 at 14:44:29Z, and a candidate fix landed after the snapshot.
    - The delta preview is TESTED and conforms (4/4).
  - **0 value-changing findings.**
  - Everything else is a NOTE.
- **`concurrent_jacobian_cx1` is unchanged since Claude3's 0271 verify.**
  - It still has 13 files, all with mtimes at or before 12:05Z.
  - CONSOLIDATED `b272e1dc`, FINAL_DESIGN `1fa34f0f` and EXTENSION `d0823cd9` equal the RESULT.json pins.
  - `branch_trace_cx1v001.py` is not re-reviewed (RESULT N2 stands).
- **Rulings already given (post-snapshot).** The two root inputs Codex1 asked for after 0193 are already ruled by the Claude3 deputy, as `DEPUTY_D001_D002_OBSERVED_CX1V001.txt` in the object folder records:
  - D001: the outside-site RECORD boundary (CX1 0194);
  - D002: L2_DIRECT envelope timing (CX1 0195).
- **Post-snapshot arrivals.** 34 entries landed between 14:42 and 14:54Z, and 7 of the pass-1 CURRENT files are already superseded. The superseded ones are executor_hook v002 and the whole selected capture chain (bytes v002, owned_bytes v002, discovery v003, record v002, capture v002, test pipeline v003). See `INVENTORY_PASS1.json` → `post_snapshot_arrivals`.

## 1. Requirement checks

### 1.1 0843 item 1: the speculative register (`register_two_stage_cx1v001.py`)

**What it does.** It is a prerequisite selector, not an admission.
- It reads the binding, then the register: exactly 2 snapshot reads.
- The binding must have exactly the fields {schema `SPECULATIVE_REGISTER_BINDING_L2_V001`, register {path, sha256}, context {config_sha256, cache_id, gate_digest}}.
- The register must have exactly {schema `SPECULATIVE_REGISTER_L2_V001`, entries}, with 7 entries.
  - Each entry has row ∈ {28, 29, 30, 31, 300, 301, 302}, a unique 64-hex key and a unique call_root named `DDO154_JACOBIAN_R<row>_<key[:16]>_A<attempt>`.
  - Each entry pins its spec, launcher, guard, binder, DBP and runtime_capture.

**Requirement checks.**
- **Both files required; fail-closed if either is missing or mismatched. PASS, TESTED.**
  - CX1 test: foreign register, foreign context, duplicate row, wrong spec, missing call and foreign root name are all refused.
  - Probe T6: a missing binding is refused (EVIDENCE_UNREADABLE); a good binding selects row 28; an unregistered key returns None (the normal campaign path).
- **COMPLETED_INVALID never auto-ingested. PASS.**
  - The register carries no status, and a status field is refused (TESTED in the CX1 test).
  - Admission requires classification VALID: `valid_admission_cx1v002.py` L65 (FORMAL).
  - `inflight_policy_cx1v001` maps COMPLETED_INVALID to RETAIN_SPECULATIVE_INVALID_FOR_ROOT, and a failed acceptance to RETAIN_FAILED_ACCEPTANCE_FOR_ROOT (TESTED T8).

**NOTEs.**
- **N1 (FORMAL): the two-stage selector is not wired.**
  - No CURRENT module imports `register_two_stage_cx1v001`.
  - `planned_binding_cx1v001.py` L10/L41 still uses the single-stage `speculative_register_cx1v001.select_registered`. That is a different schema (`CX1_SPECULATIVE_REGISTER_V001`, with fields theta_key/spec/driver/direct_plan/case/runtime_environment/envelope_phase), so it would refuse the 0843 register.
  - `valid_admission` and `executor_hook` consult no register.
  - This belongs to I3.
- **N2 (TESTED T6): the policy draft's field names are refused by the code.**
  - The policy draft lists binding fields as flat `register_sha256, config_sha256, cache_id, gate_digest`.
  - A binding written that way is refused (L2_BINDING_SCHEMA).
  - Root needs one exact, published schema, or a writer tool, for both files before writing them at H11 end.
- **N3 (TESTED T6): context values must be 64-hex.**
  - `register_two_stage` L12 requires config_sha256, cache_id and gate_digest to be 64 lowercase hex.
  - A non-hex cache_id is refused (L2_CONTEXT).
  - Confirm the c2v004 cache_id and gate-digest formats; if either is not 64-hex, an honest binding is refused.
- **N4 (FORMAL): rows and call-root naming are hard-coded.**
  - Rows are fixed at L23 and the call-root name at L28. They must equal root's register writer and A278's D.
  - With unique rows, one attempt per row fits 0837: an uncounted direct call falls back to the campaign.

### 1.2 0843 item 2 with 0845/0847: the runtime capture

**Which chain.** The policy draft selects `runtime_distribution_capture_cx1v002.py`, with its 7 sha-pinned HELPERS:
- `runtime_policy_cx1v001`, `runtime_fingerprints_cx1v002`, `runtime_distribution_cx1v001`, `runtime_distribution_bytes_cx1v002`, `runtime_distribution_owned_bytes_cx1v002`, `runtime_distribution_discovery_cx1v003` and `runtime_distribution_record_cx1v002`.

**How it runs.**
- It runs under `-I -B` (L18).
- It execs each helper only after a sha check, so helpers resolve only to the pinned bytes.
- It writes its output by exclusive create (L53).

**Superseded by role.** These are CURRENT by version but their role is superseded:
- `runtime_capture_entry_cx1v003` and `runtime_capture_assembly_cx1v002`: the sys.modules route, which CX1 0192 found insufficient;
- `runtime_policy_cx1v002`, whose `compare_records` handles the old schema.

**Requirement checks.**
- **C1. Interpreter realpath and binary sha256. PASS.**
  - `record.assemble` → `FileFingerprints.capture(sys.executable)` gives the realpath via `resolve(strict=True)` and a sha from the bytes, with inode/size/mtime/ctime stability checks.
  - TESTED in the pipeline test with an inert interpreter file.
  - Per 0847, the interpreter is static, so the binary sha covers its code.
- **C2. sys.version and sys.flags. PASS, with NOTE N5.**
  - Both are recorded. The record requires `isolated==1` and `dont_write_bytecode==1`; a record with flags 0/0 is refused (RUNTIME_FLAGS, TESTED T5).
  - **N5 (FORMAL).** These are the capture process's own flags. They describe the driver child only because the monitor launches `python -I -B <driver> run --spec … --outdir …` (`terminal_association_cx1v001.py` L22). The record itself does not bind to the receipt command.
- **C3. Third-party distributions from an AST scan of the pinned SCRIPTS. PASS, with NOTE N6.**
  - `prepare()` verifies 13 source pins by sha (driver b5cc62af plus the 12 stages), walks Import/ImportFrom nodes, refuses relative imports and always adds numpy and scipy.
  - The producer's SOURCE_PINS equal `RUNTIME_STAGE_SOURCE_AUDIT_CX1V001` 13/13, in order (TESTED cross-check; the sources themselves were not opened).
  - **N6 (TESTED on CX1's audit statements; FORMAL).**
    - The only third-party root the scan finds is **numpy**. scipy enters only through the forced {numpy, scipy} inclusion.
    - All 12 stages load further modules with `importlib.util.spec_from_file_location`/`exec_module`, and the scan does not see their imports.
    - This is within 0845's ruled scope. But a third-party package other than numpy and scipy, imported only by those dynamically loaded modules, would go uncaptured.
    - Suggest recording the dynamically loaded module paths and their AST import roots, or getting a root statement that numpy and scipy are the only third-party packages.
- **C4. The bytes route only. PASS.**
  - `capture_bytes` builds a domain-tagged sha256 over the sorted relative names. For each name it hashes a length-prefixed name, then the 8-byte size, then the bytes.
  - It walks owned roots recursively, so the inner `.dylibs` and `.so` files are included. Conventional sibling `<name>.libs`/`.dylibs` directories are included too.
  - `__pycache__` files are listed with `excluded_from_equality=True` and left out of the digest. Files outside RECORD are listed with `outside_RECORD=True` and included in the digest.
  - A RECORD-only row (`identity_basis distribution_RECORD`) is refused (DISTRIBUTION_IDENTITY).
  - TESTED: CX1 bytes test; pipeline; T2 (a `.pyc` change leaves the digest equal, a stray file changes it); T3 (inner `.dylibs` and a sibling `numpy.libs` are in the digest); T9.
  - **N7 (TESTED T3b).** An unlisted library directory with an unconventional name outside the package directory is not covered. FORMAL: low risk, because macOS numpy/scipy wheels keep `.dylibs` inside the package.
  - **N8 (FORMAL).** The pinned helper `runtime_distribution_cx1v001` still carries the RECORD-only route that 0847 refused (`capture_distribution`, `compare_distributions`). The selected chain uses only its `need()`. Harmless, but the policy should say so, or the helper should be split.
- **C5. RECORD entries outside site-packages. B1, BLOCKING at snapshot.**
  - **What fails.** `runtime_distribution_owned_bytes_cx1v002.py` L32/L34 refuses RECORD_OUTSIDE_SITE, so the capture refuses any distribution whose RECORD lists console scripts in `../../../bin`.
    - TESTED T1, on a fabricated layout.
    - FORMAL for the real layout: numpy's `f2py`/`numpy-config`. I did not read the real runtime's numpy RECORD because it is not a named path. The lead can authorize one named read to confirm.
  - **Why BLOCKING.** It is A115 (a): an honest capture of the real runtime is refused, so no runtime evidence and no import.
  - **Status.**
    - Codex1 flagged it (0193 limitations, 0194), and the deputy ruled D001 at 14:44:29Z.
    - The candidate fix landed post-snapshot: bytes v003, owned_bytes v003, discovery v004, capture v003 (`prefix_root=sys.prefix`) and record v003.
  - **Delta preview, TESTED on copies of bytes v003 and owned_bytes v003:**
    - an entry inside the prefix is accepted as `prefix:bin/f2py` and is in the digest (changing it changes the digest);
    - entries outside the prefix (RECORD_OUTSIDE_PREFIX) and symlinks (PREFIX_SYMLINK) are refused;
    - a missing prefix file is refused, but as RECORD_METADATA_LIST_CHANGED, because Python 3.12 `importlib.metadata` drops missing files from `Distribution.files`.
    - All of this is fail-closed, as D001 rule 2 requires.
  - The full v003 chain review is the pass-2 delta.
- **C6. Whitelisted normalized environment. PASS, with NOTE N9.**
  - The whitelist is the six THREADS, PATH, LANG, TMPDIR, PYTHON*, DYLD* and LC_*.
  - Normalization removes PYTHON* and sets the six thread variables to '1'. DYLD* is retained so that the producer refuses it (FORBIDDEN_DYLD).
  - LANGUAGE, HOME, secrets, MallocNanoZone and __CF_* are not recorded.
  - TESTED: T4 and the pipeline test (SECRET excluded). `effective_environment` in policy v001 (pinned) and v002 are identical (T4).
  - **N9 (FORMAL).**
    - The normalization is Codex1's model of the monitor; CX1 0190 claims it is exact. I did not re-verify it, because the monitor is not a named path.
    - The model is applied to the capture process's own environment (root's shell); it is not observed in the child. So the compared thread values and PYTHON* absence are equal by construction.
    - The capture and the launch must therefore come from the same shell. That is procedural. A launcher-side environment digest in the receipt would close it.
- **C7. macOS build and hardware model. PASS.**
  - They come from `/usr/bin/sw_vers -buildVersion` and `/usr/sbin/sysctl -n hw.model`, with a timeout and a non-empty-output check.
  - The build is compared; the model is recorded only (TESTED T5).
- **C8. Driver and monitor shas. PASS.**
  - `assemble` re-hashes the driver b5cc62af and monitor ba031c23 from bytes, refuses a mismatch, and includes both in the compared identity.
  - FORMAL, plus TESTED with inert pins.
- **C9. Equality policy. PASS, with NOTE N10.**
  - `compare` checks `validate(a)==validate(b)` over: the interpreter sha, the driver sha, the monitor sha, {distribution: (version, digest)}, {import: distribution}, the thread values and the macOS build.
  - PYTHON* and DYLD* must be absent on both sides.
  - Recorded but not compared: realpaths, sys_version, sys_flags, hardware model, PATH, LC_*, LANG, TMPDIR, captured_utc and the producer.
  - TESTED T5: equal when only the hardware model, PATH, time, version or producer differ; refused (RUNTIME_MISMATCH) when the macOS build differs. This matches 0843 and 0845 item 5.
  - **N10 (TESTED T7).** Two comparators coexist. `runtime_policy_cx1v002.compare_records` refuses distribution records (RUNTIME_SCHEMA). The policy should name `record.compare` as the only comparator, and state the PYTHON*/DYLD*-absence rule, which is enforced in `validate` but missing from the draft's compare list.
- **C10. Fail-closed when evidence is absent. PASS.**
  - `validate` requires every field.
  - The producer refuses on a helper or source pin mismatch, existing output, an empty platform fact or a changed environment.
  - TESTED: CX1 record test (12 cases) and pipeline (7).
- **C11. No present-day inspection instead of a launch-time capture. NOTE N11 (TESTED T5): not enforced at snapshot.**
  - **The record layer cannot tell.**
    - `captured_utc` only has to be timezone-aware; a capture dated 2099 validates.
    - `launch_association` is `REQUIRES_ROOT_BINDING`, and `compare` returns `launch_association_verified: False`.
  - **Direct side.** The register pins each call's capture sha at launch.
  - **Campaign side.** There is no slot for it: the BINDING schema is exactly {schema, register, context}.
  - **Missing (I3):**
    - a root-bound campaign-side capture pin;
    - a check that captured_utc is no later than the receipt's `utc_start`;
    - a check that realpath(receipt python) equals the capture's interpreter realpath. Receipts bind python by path string (CX1 0190).

### 1.3 0843 item 3: the L2_DIRECT envelope (`envelope_guard_cx1v002.py`)

- **E1 (FORMAL): what the guard checks.**
  - The phase is fixed to `L2_DIRECT` (L17).
  - It loads the envelope tool (sha `9d531381`) privately by a single read.
  - It reads only the START and END manifests that were passed in (ENVELOPE_UNEXPECTED_READ otherwise).
  - It checks the body hash, the phase, the pin_set body and file sha, that `unresolved_pins` is empty, and that each required pin matches from bytes. Then it runs the tool's `compare`.
  - **Not TESTED:** it needs the tool, which is not a named path. I did not verify that the sha maps to `pinned_input_envelope_c2v003`.
- **E2 (FORMAL): root binding is left to the caller.**
  - start, end, pin_set and required_pins are caller parameters, and nothing checks that the manifests live in `$R/ENVELOPE_L2_DIRECT`.
  - The guard itself never infers the phase from a candidate record.
  - Wiring is missing (I3).
- **E3: START/END against per-admission checks. Design-open at snapshot (NOTE).**
  - **The conflict.**
    - The guard needs END.
    - `inflight_policy` refuses before WAIT or IMPORT when the envelope is not valid (REFUSE_ENVELOPE even for RUNNING or terminal-valid calls; TESTED T8).
    - 0843 puts END after the last import.
    - Wired as-is, every honest admission would be refused, so it would become BLOCKING.
  - **Status.**
    - The deputy ruled D002 at 14:44:29Z: re-verify START at each admission against a fresh observation; root takes one final END; if that fails, mark the imports INVALIDATED_BY_ENVELOPE.
    - `envelope_observation_adapter_cx1v001`/`v002` and `envelope_observation_guard_cx1v001` landed post-snapshot. Pass-2 delta.
- **E4 (FORMAL): the START pin set and its timing. Ask root or the deputy.**
  - 0843's pin set includes the importer policy and entry, the register and the runtime captures, and START is taken before the 7-call launch (H11 end, about Fri morning).
  - **(a)** The policy and the entry must be final and pinned before that launch, which is earlier than the Fri 12:00 CDT review target.
  - **(b)** The BINDING file and the campaign-side capture only exist at campaign init, after START, so they cannot be required pins of START.

### 1.4 One immutable importer policy, a separate entry, and wrapper/cache identity unchanged

- **P1 (TESTED T10, FORMAL): the policy draft is pinned correctly.**
  - `IMPORTER_POLICY_DRAFT_CX1V001.json` (sha `7161a89f`) landed during the listing.
  - Its status is NOT_INSTALLABLE_REVIEW_DRAFT and `scientific_launch_authority` is false.
  - Its 4 component pins equal the bytes, and the producer pins its 7 helpers by sha.
  - It records 0845's argument (`exec_verified` L577–586 plus the SCRIPTS pin table).
  - It already pins capture v002 and record v002, which are superseded post-snapshot.
- **P2: the policy covers only part of the importer.**
  - The separate entry does not exist.
  - No lifecycle component is in the policy: valid_admission, executor_hook, custody, request_guard, the cache adapters, the handoff writer and wait.
  - This is I1/I2.
- **P3 (FORMAL): wrapper and cache identity unchanged. CONFIRMED at the byte level.**
  - `certificate_spec_adapter`, `classifier_spec_adapter` and `scheduler_adapter` rewrite one expression or hook in the pinned wrapper `7c9b4248`, parent `c75a889f` and scheduler `d35d5d4a` functions, in process, by AST. They refuse on a sha or shape mismatch.
  - The source bytes and cache_id are untouched.
  - Local calls keep the original functions: there are separate `*_external` variants, and the selector routes only external entries to them.
- **P4 (FORMAL): resumes after the first import depend on the importer.**
  - After the first import, a cache reopen needs the importer's verifier: the selector forces external validation by call_dir location.
  - Whether the plain wrapper refuses an External1 call_dir is not verified (the wrapper is not a named path).
  - The runbook must route every resume after the first import through the entry. Integration should TEST that a plain-wrapper reopen refuses rather than accepts.

## 2. The other CURRENT code (I1/I2 lifecycle), first-pass notes

**Read in full** (FORMAL unless marked):
- valid_admission v002, executor_hook v002, request_guard v002, custody_guard v003, direct_layout, snapshot, readonly_scope, original_spec_resolver;
- the 4 cache modules, direct_accept_prepare v002, direct_handoff_writer v001;
- planned_binding, inflight_policy, wait_registered, terminal_association.

**Read at the header only:** scheduler_adapter, exclusive_output_scope v003, static_code_pin_graph, certificate_spec_adapter and classifier_spec_adapter beyond the rewrite core, runtime_capture_entry v003 and runtime_capture_assembly v002.

- **`valid_admission_cx1v002`: covers 0827 item 1.** It checks:
  - the held `ORCHESTRATOR.lock` inode;
  - committed WAVE_PLAN equality, and that WAVE_RESULT is absent;
  - UNREQUESTED_POINT, the theta key and value, DUPLICATE_IMPORT and the mapper bytes;
  - that the original directory is canonical, not moved and external;
  - the layout, the final spec bytes and the certified slots;
  - custody: receipt, result, finish, the monitor `verify_receipt` and the acceptance pass sequence (latest pass; first pass INCOMPLETE);
  - the existing handoff, classification VALID and the bundle.
  - It never writes.
- **`executor_hook_cx1v002`: fails closed, but the fallback paths are not wired.**
  - A Refusal from `_validate` (L39) aborts the whole wave rather than one call. That is fail-closed.
  - The CAP/INFRA fallback to the normal path, and the in-flight wait for the W1 seed (0837), both depend on an installer that filters candidates through `inflight_policy`/`wait_registered`. That installer is not wired.
  - `executor_hook` v003/v004 ("wait hook") landed post-snapshot. Delta.
- **Infrastructure failure cannot become MODEL_INVALID (FORMAL).** Refusal is a BaseException (`snapshot_cx1v001.py` L11), so `except Exception` cannot turn it into MODEL_INVALID. I did not re-read the engine's handlers; CX1 0186's synthetic whole-engine replay covers them.
- **`direct_handoff_writer_cx1v001` writes into the original call directory (NOTE).**
  - It writes `TAIL_CERTIFICATE_ACCEPTANCE.json` there, on External1 (L16, exclusive create, fsync, readback).
  - Nothing is copied or moved, but the custody-of-record directory gains a file, and External1 must be writable at campaign time.
  - Root or the deputy should confirm this under 0827 item 1.
- **`readonly_scope_cx1v001` is single-thread only (NOTE).** L59 refuses unless `threading.active_count()==1`. If the live campaign process has other threads at validation or ingest, an honest admission is refused. This is unverified against campaign_c2v005; TEST it in integration.
- **`original_spec_resolver_cx1v001` fixes the local layout (NOTE).** L36–37 accept only `waves/wave_NNNN/campaign/call_NNNN`. That must equal every local call layout, including resume.
- **Version hygiene (NOTE).** Some CURRENT files import SUPERSEDED versions:
  - custody v003 → request_guard v001;
  - handoff writer v001 → request_guard v001 and valid_admission v001;
  - planned_binding v001 → request_guard v001, valid_admission v001 and speculative_register v001;
  - producer and record v002 → runtime_policy v001.

  `require`, `check_held_lock` and `effective_environment` behave identically across these versions (diffs, and T4). The exception is planned_binding's register, which is semantically old (N1).
- **Test coverage (NOTE).** `test_runtime_real_metadata_cx1v001` and `test_runtime_distribution_discovery_cx1v002` exercise SUPERSEDED owned_bytes v001 and discovery v002. Only the pipeline v003 test covers the selected discovery v003 and owned_bytes v002.

## 3. Missing for Friday (Codex1's I1–I3, plus specifics)

- **I1. Lifecycle and cache integration:**
  - the separate entry or installer;
  - wiring the executor hook to `inflight_policy`, the wait and the 0837 in-flight seed;
  - moving `planned_binding` onto the two-stage register (N1);
  - integrating the cache verifier and put with the real wrapper. Codex1 still marks as UNTESTED the synthetic mapper/taxonomy, cache header creation and the original atomic writer;
  - the real-process single-thread check;
  - the resume rule (P4).
- **I2. The acceptance entry:**
  - the direct acceptance producer (h3_accept_call c2v004 semantics) in the original External1 directories;
  - the ruling on the handoff writer's custody write;
  - the F6/negative path stays root's per call; it is explicitly unsupported and fail-closed.
- **I3. Authenticated runtime, environment, envelope and register:**
  - exact root-facing schemas, or a writer, for REGISTER and BINDING (N2);
  - the cache_id and gate-digest formats (N3);
  - a binding for the campaign-side capture, and the capture-to-receipt association by time and interpreter realpath (C11);
  - review of the D001 v003 chain (C5);
  - review of the D002 per-admission START observation, the final root END and INVALIDATED_BY_ENVELOPE handling (E3);
  - the envelope required-pin list derived from the register and policy, not from candidates (E2);
  - START pin-set timing against the policy and entry freeze (E4);
  - confirming that the envelope tool sha `9d531381` is `pinned_input_envelope_c2v003`.
- **Also:**
  - a final, installable, immutable policy V001 that names every component and the one comparator (N10);
  - tests that exercise the CURRENT discovery and owned_bytes directly;
  - running `test_envelope_guard_cx1v003` and `test_driver_env_normalization_cx1v001`, which need the envelope tool and the monitor. The lead should name those paths if they are wanted.

## 4. Reads not done

- I did not open the driver, the stage sources, the monitor, the envelope tool, the wrapper or parent sources, the runtime's site-packages, or the depth-2 fixture contents (A137).
- I did not open CX1 0194/0195, which are not named; their content is reflected in the deputy log in the object folder.
- I did not read NGC3198 data, any run tree, External1, V007_POSTSEAL_RECORDS, ~/.codex or the V006 log.
- All test output is under `fixtures_helper/` and scratch.
