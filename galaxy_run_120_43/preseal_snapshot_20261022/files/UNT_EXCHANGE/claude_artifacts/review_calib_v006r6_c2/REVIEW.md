# REVIEW_CALIB_V006R6_C2: delta review of Codex2's calibration orchestrator successor v006r6_v002 (0533 / FROM_CODEX2/0429)

Claude2 review lane, 2026-10-18 ~13:40Z. Refute-by-default, with my own synthetic fixtures and tools. Codex2's harnesses were read, never run.

## Verdict: PASS_WITH_FINDINGS (0 BLOCKING, 4 SHOULD_FIX, 6 NOTE)

- **All six prior findings are fixed as the dispatch specified:** A-01, A-02, A-03, A-04, A-06 and B4-1.
- **Each fix was tested at its real call site.** I used the actual config, with only the work dir redirected into this folder, plus my own fixtures.
- **No v005 guard is weakened.** The code-signature diff of the patched v005 namespace changes exactly the declared adapter names. Every other guard is code-identical.
- **Config and pins are correct:** P128 with gas M_s 128, driver r5 b5cc62af, and the r5 pins in discovery.
- **Not launch authorization.** Every scientific gate stays closed: deciding, numerics, adoption, capability, certificate policy and u_i.

**Totals:** 208/208 of my checks behave as required. That includes 6 explicit OBSERVATION rows, which are what the findings below rest on. The audit hook recorded 0 launch or process attempts, and the object manifest still verifies 897/897 from bytes after the review.

## Object (hashed from bytes)

| Item | sha256 |
|---|---|
| orchestrator `calibration_orchestrator_cx2v006r6_v002.py` | 09a8f28aa36ba2ac396d7957e1dbee28cf52d7f18f5a1887bfa14915ab35eb88 |
| core `calibration_core_cx2v006r6_v002.py` | 921abceaa7d8fc6be98619a2bb4eb1f7ddf5de5cb7d7d7a443c6f0dfc611ffbf |
| adoption_policy `adoption_policy_cx2v006r6_v002.py` | c7776f70ebe6cf9f3cc78836b1833861ef92c610db4ae57c84c3c36a9993c448 |
| config `RUN_CONFIG_DDO154_CX2V006R6_P128_MS128.json` | 48f1206d3068a4d7b26a6ce336f5601fb305f8bde40d1126426bf4c296172bc7 |
| BUILD_CX2V006R6_V002.md | 2b4af2558c67978012e7e7930897f5008d485880c2eb170618d11aaded86b03b |
| HASHES_CX2V006R6_V002.txt (897/897 verify) | b9651a6d2469d709037cb5c58f64f47dac94c340aa91a68c4e277dde2782e233 |
| TYPED_BLOCKERS_CX2V006R6.json | f147252e0d7aafb6ea40260ae59edd25581b5ff5fa37771791915eb54577aba6 |
| discovery `consumed_states_cx2v005.py` | 7b7400f331970a5f5fb7f7104f5e1850a765fcd04fc993100b5d1f0f37f4d653 |
| guard `certificate_guard_cx2v003.py` | 5f1e49e689a859c003b137c45c07f887423443ef2c726182616b41bf290c9c2f |
| packet FROM_CODEX2/0429 | 0cb52744b41b3b0f2bd79b82acb8182faaee2c6f5d760a1629691868c4a996f3 |
| dispatch FROM_CODEX/0533 | 9f1ee52a148618a0ce41c6320667edede0427918c804da83d47c703a324e80e2 |
| prior review (Claude3) | 8016cad0e816807088b062df850a1727f9a02b799b9b7b77aaece4b3c0d8e777 |
| base v005 orchestrator | c75a889ff4646a816329756124a19532cbc166d26f47ce2ea5147b71c2cf7c4d |
| V005 addendum (A55, A57, v006r5 entry) | 97a02ad3d1a125bae3debb9dc6446a54406945d72b0a7419a4e8e9b744dcfca1 |
| V004 addendum (A30, A32) | 487d44498205e563c752e692b48bbb7288055591c72cfdcf5a75d849fef3d82b |

## Results by item

| # | Item | Result | Tool / output |
|---|---|---|---|
| 1 | A-01 receipt reasons at both call sites | **PASS** | t1, 28/28 |
| 2 | A-03 sealed ADOPT_TAIL + full C4-6; empty allowlist | **PASS_WITH_FINDINGS** (F1) | t2, 60/60 |
| 3 | A-02 refusal → exit 3, never an invalid evaluation | **PASS** (N1) | t3, 9/9 |
| 4 | A-04 no RESOLUTIONS write before put | **PASS_WITH_FINDINGS** (F4) | t4, 7/7 |
| 5 | A-06 out/result.json; handoff writer; re-ingest | **PASS** (N2, N3) | t5, 34/34 |
| 6 | B4-1 alternate-D gated; headline ungated | **PASS_WITH_FINDINGS** (F3) | t6, 33/33 |
| 7 | Nothing else weakened vs v005 | **PASS_WITH_FINDINGS** (F2, pre-existing) | t7, 10/10 |
| 8 | P128/M_s128 config and r5 pins; distance lineage | **PASS** | t8, 27/27 |

### 1. A-01 (TESTED)

**Fixtures.** I wrote six bad receipts, each with a correct monitor self-hash where the case needs one:
- a non-receipt JSON;
- non-JSON bytes;
- STOPPED_WALL_CAP;
- FINISHED with driver_status FAILED;
- a foreign result pin;
- a tampered self-hash.

Pristine v005 `_receipt_ok` returns a reason for each of them.

**Deciding site.** Core `check_deciding` refuses each bad receipt in either row position, with the v005 reason. `route_a_column_workers_verified` is then None. A positive control with two good receipts passes with N = 8. A missing receipt key, a wrong pin sha and a single run also refuse.

**Capability site.** A real Context gives the 9 actual probe-point spec shas, all at D = 4.04. The positive control passes, and every bad receipt on one corner refuses with its reason.

### 2. A-03 (TESTED)

**The shipped allowlist.**
- `APPROVED_V007_SEALS = frozenset()` is the only assignment in the file, as an AST literal.
- The core re-hashes the policy file against c7776f70 on every call.

**The shipped policy refuses.**
- I built a complete synthetic seal set: compare source with literals, prereg binding the case block, C4T spec and result, report and addendum. The shipped policy refuses it with exactly `V007_SEAL_NOT_IN_REVIEWED_ALLOWLIST`. The allowlist is the only thing holding it.
- The actual config (all null) reads `V007_SEALED_ADOPT_TAIL_PENDING`.
- `synthetic=True` raises.
- A real Context built on the complete set has its numerics, adoption and gates_ok refused.

**With my seal registered.** This used an in-memory copy of the policy with only the allowlist line changed; nothing was written to disk.
- The complete set passes.
- 22 single-defect sets each refuse for their own reason. The defects include: reading ADOPT or RETAIN; test_mode true; tests_read false; prereg mismatch; compare sha mismatch; schema mismatch; block ≠ C4T numerics; non-fresh admit; C4T result not COMPLETED, not valid, other spec, or not the report input; not valid_all; case block not bound by the prereg; r4 driver; no u_i; compare not P128; unsealed compare (no V007_PREREG_SHA256); no addendum pin; an unregistered tuple; deciding N unverified.
- A self-asserted r5-style document in the verdict slot refuses.

**v005 C4-6 through r6 `Context.check_adoption`.** This ran on a real Context, with the passing numerics gate injected.
- The complete derivation passes.
- Each of these refuses on its own: missing timing model, timing model naming another spec, no receipts, a receipt outside the grid, a STOPPED receipt, a foreign-result receipt, caps below measured use, caps that differ from the config, a disk-guard mismatch, other seed/base/capability/verdict/case, and each tail binding (reading, compare, prereg, driver, registry).
- The original A-03 hand-made document refuses.
- So do capability not ok and numerics not ok.

### 3. A-02 (TESTED)

**The refusal escapes.** On a real Context/Orchestrator/Probe with engine v003b, I placed an uncertified entry for the engine's first requested key. `CertificateRefusal` (a BaseException, not an Exception) propagates out of the engine and out of `Probe.run`.

**Control.** The same refusal raised as an ordinary Exception reproduces Claude3's premise: the engine absorbs it, and the probe reports complete = True with calls 1 and hits 0.

**CLI.** `main wave` returns **3**, with status REFUSED naming `CERTIFICATE_CACHE_REFUSED` and launches_performed 0. An entry that is already bad at open refuses there with OrchestratorError (the exit-3 path).

### 4. A-04 (TESTED)

**The fix works.**
- Real work dirs with my synthetic WAVE_PLAN, HALT and ledger.
- `resolve --decision invalid` refuses at put with `CERTIFICATE_UNCERTIFIED_CACHEABLE_RESULT`, and **no RESOLUTIONS line** is written.
- A later prepare succeeds, the same token resolves `retry` (one line), and the token is single-use.

**Control.** The v005 order under the r6 put leaves the line and wedges every later prepare (Claude3's finding).

### 5. A-06 (TESTED: synthetic plumbing, not science)

**Synthetic world.** I built my own certificate world (custody deriver, enumerator, producer, proofs, bundles, registry, policy review) and a tail-ON result hand-written in the campaign v005 layout. Real planning ran end to end: `make_plan` → prelaunch certificate check → `_commit_plan`.

**Before the handoff.** The first ingest halts **INFRA** `CERTIFICATE_ACCEPTANCE_REFUSED`, with never_resolve_invalid set. The provenance result_path is `<call_dir>/out/result.json`.

**Writer refusals.** `write_acceptance` refuses each of the following and writes nothing:
- no parent prelaunch bundle;
- an LO shell above 0.005;
- swapped prelaunch proofs;
- an unapproved producer;
- a STOPPED receipt;
- the old root layout;
- discovery v005 as enumerator (`COMPLETE_CONSUMED_STATE_INVENTORY_REQUIRED`; discovery is never complete, by design).

**Writer success.** On a valid bundle it writes the handoff, then re-verifies it from its bytes.
- An identical existing handoff is re-read, not rewritten.
- A conflicting valid bundle is refused and the bytes are unchanged.

**Re-ingest.**
- `reingest` gives VALID with a new cache entry and 0 launches. HALT.json and WAVE_RESULT.json bytes are unchanged.
- A second reingest is idempotent, and a wrong call index refuses.
- A fresh orchestrator verifies the entry at open, and the probe **hits** the key, so there is no duplicate forward.
- A later resolve reads `ALREADY_CACHED`.
- A rewritten handoff makes the cache refuse at open (`CERTIFICATE_ACCEPTANCE_EVIDENCE_CHANGED`).

**Discovery v005.**
- It reads `out/result.json` and `out/inputs/call_spec.json`.
- It refuses the root-only layout before reading any result.
- It refuses a supplied result that differs from the bytes.

### 6. B4-1 (TESTED)

**Refused without evidence.**
- All 18 active alternate-D P128 templates (16 corners and 2 distance plans) are refused by `prelaunch_check` with `SENSITIVITY_DECIDING_III_REQUIRED`.
- All 36 old ones (32 corners and 4 plans) are refused first by A55/A57.
- The old physical points moved onto the P128 block are still sensitivity-gated.

**Headline ungated.** All 8 headline templates read `HEADLINE_NOT_GATED`, and all 9 headline probe points pass the full prelaunch with no sensitivity evidence.

**With my synthetic deciding-iii evidence.**
- A complete set at D_hi passes, and the alternate-D prelaunch then passes.
- 22 single-defect sets each refuse: run at 4.04, tail-OFF, K64, M_s64, not full hull, other galaxy, invalid result, other spec, STOPPED / FAILED / non-receipt receipt, no finish.json, no runs, review not binding the runs, review FAIL, and each of the document's verdict, hull flag, driver, status, test, owner and schema.

**Distance lineage (own AST closure).** The cited definition lines are exact (v009-GEO 939/953/1087/1112; r4/r5 1479/1493/1627/1652). The transitive in-module closure is the same set in v009-GEO and r5:
- 10 functions, all AST-identical in r4 and r5;
- 4 constants, all AST-identical: GALAXIES, GEOMETRY_PINS, KPC_M, PROFILE_NAME.

This confirms Codex2's statement and goes further. It is still source identity, not the required run.

### 7. Guard diff (TESTED)

**Changed names, v005 → r6.** Code signatures resolved through the MRO, with set constants canonicalised. The changed names are exactly:
- constants: CONFIG_KEYS, DECLARED_CHANGED_PATHS, KNOWN_REAL_DRIVER_SHA256, MAPPING_ID, MODULE_NAME, NEVER_INVALID_PREFIXES, SCHEMA_CACHE_ID;
- classes: Mapper, Context, Cache, CampaignExecutor, Orchestrator;
- functions: check_deciding, check_numerics, the new resolve.

**Unchanged guards.** 36 listed v005 guards are identical, including Lock, receipt/finish custody, Taxonomy, Probe, `_receipt_ok`, `_ProbeStop`, main, EXIT and the cache classes.

**The changed constants only add to v005:**
- NEVER_INVALID_PREFIXES gains `CERTIFICATE_`;
- DECLARED_CHANGED_PATHS gains only the two certificate slots;
- CONFIG_KEYS gains `tail_readiness`;
- KNOWN_REAL_DRIVER_SHA256 gains r5.

**resolve.** The r6 version equals v005's statement for statement. The only change is that `cache.put` moves ahead of `append_jsonl` (`out/run_*/DIFF_RESOLVE_V005_R6.diff`).

The r5 → r6 delta touches only the dispatch items.

### 8. Config and pins (TESTED)

**Config contents.**
- Config 48f1206d; driver pin r5, and its file hashes to it.
- The block passes `validate_block`: cylinder K_big 128.0, gas M_s 128 lagrange3_s_gl4, the 72-column full hull, route A workers 8, cube, K 4, unrescaled lapse-only tail-ON.
- Both slots are PENDING; the recovery rules are empty.

**Pins.** All 8 config pins verify. The taxonomy is for r5, and the work dir is pinned to VolumeUUID 7752BF6F….

**Context.**
- It refuses an r4 driver, a missing `tail_readiness`, K64, M_s64, workers 1, `ro1_workers` and λ = 2.
- The actual config builds, with every gate closed.

**Discovery and library.** Discovery v005 has DRIVER_SHA r5, and its 6 SOURCE_PINS verify. The r5 driver pins tail library v002 (2026f2b6) with an 8 GiB memory cap (A55).

## SHOULD_FIX

**F1. The V007 seal tuple does not bind the verdict report bytes (A-03 residual; TESTED with the allowlist patched in memory).**
- The allowlisted tuple is (compare sha, prereg sha, addendum sha, report schema).
- My passing positive control was a hand-written report: no comparator ever ran. Once a seal is registered, any report naming the registered comparator sha with ADOPT_TAIL and consistent inputs passes `check_numerics`.
- This matches v005, which also trusted a config-pinned report. But it does not meet "only a sealed V007 compare verdict record". BUILD's "matching JSON cannot authorize" holds only while the allowlist is empty.
- **Fix:** the reviewed successor that registers the seal must also register the verdict report's sha256 (`verdict_artifact`), or re-derive `decision` inertly from the report inputs.
- **No exposure today:** the empty allowlist refuses everything (TESTED).

**F2. The deciding gate binds no run identity (pre-existing since v006r1; not in the 0533 list; TESTED).**
- `check_deciding` needs only at least 2 FINISHED/COMPLETED r5 receipts plus a self-asserted document. `row['spec_sha256']` is never tied to anything: receipts of arbitrary specs pass.
- Nothing checks tail-ON, workers 8, D = 4.04, which row is the re-anchor, or the result content.
- Its `route_a_column_workers_verified = 8` then authorizes the block's workers 8 in the adoption policy.
- v005 bound specific spec shas, the result content and the comparator report from bytes. This is the same class of gap as A-03, at a lower layer.
- **Fix:** bind each row the way `sensitivity_gate` already does:
  - pin the spec and run `validate_block`;
  - D = 4.04;
  - workers 8 from the result's normalized spec;
  - result COMPLETED and valid, plus the finish binding;
  - named re-anchor and workers-8 rows.
- **When:** before TAIL_DECIDING_RUNS evidence is pinned.

**F3. The deciding-(iii) gate is under-specified and binds only one caller (B4-1; TESTED).**

What the gate is missing:
- Any single completed tail-ON full-hull run at any D ≠ 4.04, plus a PASS review, satisfies it. D_hi evidence also unlocks D_lo.
- No comparator report and no reference-side run is read. Under A32, (iii) is a two-driver per-call comparison, with `ended_unix_ns` masked.

Who it binds:
- In A13 fixed mode the orchestrator never generates D ≠ 4.04.
- So all 16 + 2 sensitivity cases are standalone driver launches. The gate binds them only if Claude2's launch procedure calls `ctx.prelaunch_check` on each spec.

**Fix:**
- Root specifies the rerun: which D values, the reference side, and the comparator and its mask.
- The gate binds per-D evidence and a comparator report from bytes.
- Expose a one-call check (or launcher) for standalone sensitivity specs, and add it to the launch checklist.

**F4. `resolve --decision invalid` is now unreachable for every item, and this is not declared (A-04 consequence; TESTED).**
- The r6 put refuses root entries, which carry no result.
- Even with a certificate exemption, put-before-append cannot pass v005 L1: `_verify_impl` for ROOT_RESOLUTION requires the RESOLUTIONS line to exist already.
- This fails closed: the work dir stays usable and retry works.
- But the HALT.json rule text (v005 ingest) still offers `--decision invalid`, and neither BUILD nor TYPED_BLOCKERS says root-invalid is disabled.
- **Fix:** declare it. If root wants MODEL_INVALID resolutions for tail-ON calls, a successor must specify a certified root-resolution form and an ordering compatible with L1.

## NOTEs

- **N1 (A-02 scope).** Exit 3 holds in the r6 CLI (`plan` and `wave`), as TESTED. The inherited v005 `main run`, or an import-driven `Orchestrator.run`, lets `CertificateRefusal` escape as an uncaught BaseException: interpreter exit 1 with a traceback (TESTED with a stub). This still fails closed. Catch it in the r6 run wrapper when the launch entry is built.
- **N2 (re-ingest).** It passes campaign status `OK` to the executor. That is excluded from `entry_core`, so the cache is unaffected. It also never consults HALT.json or the key's latest launch wave. This is harmless for identical specs; state it in the launch procedure.
- **N3.** The handoff `writer` field is never verified. Everything else in the handoff is re-verified from bytes, so a hand-written handoff gains nothing. Not a hole.
- **N4.** `core.check_numerics` hashes the policy file and then re-reads it to execute it, with no re-hash after loading; v005 `load_pinned_module` re-hashes. This is a local TOCTOU only.
- **N5.** Codex2's 96/96 static/dry run used the superseded unnumbered candidate (8d5d06af). v002 differs only in the allowlist and the two pins: I diffed it, and STATIC_DELTA_V002 declares it. My t6 and t8 re-ran those gate checks on v002.
- **N6. Carried from Claude3, not re-measured here:**
  - the hull top margin is about 2.5%;
  - column 71's rfs override has 0.72% headroom;
  - the like-for-like EPS spread is about 118×;
  - N-04 and N-05 remain scientific obligations.

## UNTESTED (out of scope or unavailable)

- Full live campaign and cache integration with real driver output.
- Any real certificate, the V007 seal, deciding or capability runs, and caps.
- Whether my synthetic proofs or enumerator correspond to anything scientific: they test plumbing only.
- The r5 driver's own internals beyond its pins and the distance-path AST.

## Method and hygiene

**Tools.** `tools/` holds `common.py` (pinned loader and audit hook), `t1`–`t6`, `t7_dump_namespace.py`, `t7_compare_guards.py` and `t8`. Each was run with `python3 -I -B`.

**Final outputs** (one run directory each):

| Test | Output |
|---|---|
| T1 | `out/run_20261018T133855_59829/` |
| T2 | `out/run_20261018T133856_59835/` |
| T3 | `out/run_20261018T133857_59841/` |
| T4 | `out/run_20261018T133859_59899/` |
| T5 | `out/run_20261018T133900_60125/` |
| T6 | `out/run_20261018T133904_60775/` |
| T7 dumps | `out/run_20261018T133904_60893/`, `out/run_20261018T133904_60911/`, `out/run_20261018T133905_60931/` |
| T7 compare | `out/run_20261018T133905_60951/` |
| T8 | `out/run_20261018T133905_60976/` |

Fixtures are in the matching `fixtures/run_*` directories.

**Superseded earlier runs.** These are kept, not deleted, and are not cited:
- `out/T1_A01_RECEIPTS.json` and `out/T2_A03_ADOPTION.json`, before per-run directories existed. The latter is 59/60 because of my own over-strict expectation; it was corrected and re-ran at 60/60.
- The first namespace dumps, whose frozenset constants were ordered by hash seed. The dumper was canonicalised and re-run.

**Audit hook.** A process audit hook:
- refused any subprocess, spawn, fork or socket (0 attempts recorded);
- refused any write or mutation outside this folder;
- refused any deletion except the orchestrator's own `.tmp` atomic-write temp file;
- refused C5H, NGC target and `.codex` paths.

**Scope kept.**
- No launch.
- No solver subprocess. The driver was used only for in-process `normalize_spec` and AST parsing.
- C5H and NGC targets were not opened.
- The object is unchanged: 897/897 after the review.

Hashes of everything here are in `HASHES.txt`, computed from bytes.
