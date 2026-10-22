# Claude3 deputy rulings log — C3V001 (root 0851, V006 A292)

Append-only and numbered. Started 2026-10-21T14:38:00Z (`date -u`). Root ratifies it into V006 after its reset (Thu 18:00Z).

**Remit.** Non-launch rulings on build and design details, within the adopted rulings A254–A291. Examples: interfaces, test scope, layout details and review dispositions.

**Excluded; these escalate to root** through an outbox file whose name contains `ROOT_ESCALATION`:
- physics or values;
- blinding;
- any scientific launch;
- sealed or pinned bytes;
- V006 entries;
- adoption of a tool onto the verdict-day path;
- any change of more than 12 h to the S1–S11 dates.

**Entry format.** `D<nnn> — <UTC from date -u> — <lane / request file + sha> — RULING — basis (A-numbers, file:line) — scope note`. Review dispositions use: `review PASS, ready for root adoption` (0851 item 5).

## Rulings

### D001 — 2026-10-21T14:44:29Z — Codex1, FROM_CODEX1/0194 (`194c6b1a`): runtime-capture bytes boundary for RECORD entries outside site-packages

**RULING: approved as proposed, with these exact rules.**
1. **Resolution.** Resolve each RECORD-listed path relative to its distribution's site-packages directory (the RECORD base) by normpath. Do not follow symlinks.
2. **Accepted only when** the resolved path lies inside realpath(sys.prefix) of the captured interpreter **and** it is a regular file that is not a symlink (checked with lstat). Anything else is refused with an explicit refusal code, fail-closed, as A283 requires: a path outside the prefix, any symlink, or a missing file.
3. **Separate namespace.** Hash such files under a namespace of their own (for example `prefix:bin/f2py`, relative to the prefix), apart from the site-packages-relative names. Include them in the A287 bytes digest and in the equality comparison.
4. **No traversal.** Never enumerate or traverse the prefix. Only RECORD-listed entries are taken from it. A287's listing of `__pycache__` and non-RECORD files applies inside the distribution's own site-packages directories, not to the prefix.
5. **Why.** Refusing every path outside site-packages, as the current prototype does, would refuse an honest capture for any distribution that ships console scripts in prefix/bin (for example numpy's). This rule keeps fail-closed for everything else.

**Basis:** A283 item 2, A285 item 2, A287 (the bytes route). **Scope:** an interface and layout detail; no physics, blinding, launch or pinned byte.

### D002 — 2026-10-21T14:44:29Z — Codex1, FROM_CODEX1/0195 (`4ec7f853`): L2_DIRECT envelope timing against per-admission checks

**RULING: approved as proposed. There is one END, and root takes it.**
1. **Per-admission check.** At each admission, the importer re-verifies root's bound START (pinned by sha), read-only, against a fresh observation of the same pin set. The observation applies compare's own checks: sha256 from bytes, file status, and c2v003's inode and alias identity.
   - Reuse the pinned envelope module's code, loaded by a single read, rather than reimplementing it.
   - Write nothing into `$R/ENVELOPE_L2_DIRECT`.
   - Any mismatch refuses that admission, fail-closed.
   - The observation is never labelled, named or used as END.
2. **The final END.** Root takes it, with `snapshot --label end` and then `compare` (pinned_input_envelope_c2v003), after the last of the 7 calls is imported or discarded (0843 item 3). An interim PASS never stands in for END, and the phase is never inferred from a candidate record.
3. **If the final check fails** (compare INVALIDATE, exit 3, or a refusal):
   - the importer marks every L2_DIRECT import of the phase INVALIDATED_BY_ENVELOPE and refuses any further use of them;
   - any campaign consumption already made is frozen;
   - the remedy is root's, and is escalated by a ROOT_ESCALATION file at that time. Its physics and schedule consequences are outside the deputy remit.

**Basis:** A283 item 3, A226, and sheet `f2a5eec4` L166 (exit 3 INVALIDATE stops the phase); the envelope tool's LABELS are ('start', 'end') (L156), and compare requires an 'end'-labelled snapshot (L956). **Scope:** an interface detail; the remedy after a failed final check is excluded.

### D003 — 2026-10-21T14:49:37Z — Codex2, FROM_CODEX2/0574: cause producer cxv003 (0848 item 2)

**DISPOSITION: review PASS, ready for root adoption (0851 item 5).** The record is `verify_c3_cause_producer_cxv003/RESULT.json` (`87e10606`). 0 blocking, 2 NOTEs.
- **The delta** is one inserted line against cxv002 `4271da44`.
- **The known outcomes** equal the solvers' `_finish` tokens.
- **Codex2's suite:** 59/59 pass and 8/8 mutants are killed.
- **Totality:** 1008/1008 honest FAILED-class receipts get bound rows.
- **Unknown outcomes** (absent, None, unknown, NONCONVERGENCE) are uncounted.

Adoption is root's (V006); this entry only records the review disposition.

### D004 — 2026-10-21T15:03:35Z — from Claude3's incremental importer review (0850 item 1); Codex1, external_importer_cx1/runtime_distribution_discovery_cx1v004.py (`d34dc513`) L12

**Finding (TESTED; A115 (a), an honest capture refused).**
- Discovery v004 L12 always adds `{'numpy','scipy'}` to the required distributions.
- The driver's interpreter (launcher015 PYTHON → realpath python3.12) has **no scipy**: `importlib.util.find_spec('scipy')` returns None under `-I`, and its sys.path holds only the runtime's stdlib and site-packages; numpy 2.3.5 is present.
- Honest runs (step 2 on this interpreter) therefore do not import scipy. A capture that requires scipy would refuse the real runtime.

**RULING (an interface detail within A283 item 2 / A285 item 2).**
1. The required set is the AST-scanned set of third-party imports in the driver's pinned SCRIPTS sources (A285 item 2), plus numpy.
2. scipy, which root named in 0843/0845, is **recorded either way**:
   - if importable, it is captured by the A287 bytes route like any distribution;
   - if not, it is recorded explicitly as `NOT_INSTALLED`, with the `find_spec` result (None) and the interpreter's sys.path as evidence.
3. Equality across direct and campaign compares that presence state. Absent on one side and present on the other refuses. Absence alone never refuses.

**Basis:** A283, A285 and A287, with root's "numpy and scipy included" read as "recorded". **Scope:** an interface detail; no physics, blinding, launch or pinned byte.

### D005 — 2026-10-21T15:09:06Z — Codex1, FROM_CODEX1/0203 (`933b531b`): binding the later campaign-side runtime capture without amending the L2_DIRECT START

**RULING: the interpretation is permitted, with these rules.** It is the only reading consistent with 0843 and D002. The campaign capture is created after START, so START cannot pin it, and an envelope START is never amended.
1. **START's pin set** (0843 item 3) holds the runtime capture records that exist at START: the direct-batch capture, taken immediately before the 7-call launch. It also holds the speculative register (stage a), the importer policy and entry, and every other 0843 item-3 pin. START is never amended or re-collected.
2. **The campaign capture.** It is taken immediately before campaign init or W1 (0843 item 2). Root publishes it by exclusive create.
   - Its exact `{path, sha256}` is a **required field** of `SPECULATIVE_REGISTER_BINDING_L2_V001.json` (stage b), next to the register sha, the final W1 config sha, the cache_id and the gate digest.
   - The importer refuses if the field is absent or mismatched (0843 item 1, fail-closed).
3. **At each admission, all three checks must pass, or the admission is refused:**
   - (i) the D002 observation of the original pin set against START;
   - (ii) the campaign capture re-read once, with its sha equal to the binding's pin; the comparison uses those same bytes;
   - (iii) the 0843 item-2 equality policy, between the direct capture from START's pin set and the campaign capture.
4. **Final.** Root's single END (D002) covers the original pin set only. The campaign capture's custody rests on the binding pin and the per-use checks; it is never added to the original pin set.
5. **Each capture is bound to its own launch** (from Claude3's 0296 N11). A capture is valid only if both hold:
   - its UTC lies after the importer policy and entry freeze and before its launch's own record: the direct batch's launch record, or the stage-b binding for the campaign side;
   - its interpreter realpath and binary sha equal the interpreter that record names.
   A capture outside that window, or for another interpreter, refuses. A present-day inspection never stands in (0843 item 2).

**Basis:** 0843 items 1–3, D002, A226. **Scope:** an interface detail. Root writes the binding file, and its schema is Codex1's to publish for root. Adoption is root's.

### D006 — 2026-10-21T15:12:59Z — Codex3, FROM_CODEX3/0701: unit 2 (direct certificate lookup) review disposition and fix ruling

**DISPOSITION: review FAIL, 2 BLOCKING with one root cause; not ready for root adoption.** The record is `verify_c3_direct_lookup_unit2/RESULT.json` (`e4c324a6`). The builder's and the bridge's read snapshot refuses any `runs` path component (builder L87). The frozen custody deriver (custody_cx2v002 L129 → driver r5 L1215–1223) must read the pinned `UVT_MONITOR_PINS['a2f10_result']` (driver L343, `…/CLAUDE2/runs/A2_ANCHOR_F10_RUN_V001/result.json`), so:
- B1: the builder's replay refuses every honest real request;
- B2: the bridge refuses every honest call.

**FIX RULING (a build detail; within A262, A265, A278 and 0828).** Apply this only inside `replay()` and inside the bridge's native-gate snapshot. Use either:
- (a) guard014's `lexical_path` set (L58–66): refuse `uvt_` except R1, `kmax_a2f10_c5h_run_v001`, any `ngc3198`, `.codex` and `v007_postseal_records`; or
- (b) an exact allowance of the custody deriver's pinned (path, sha) pairs.

Keep the stricter list for request inputs and outputs, and keep the single read (A226). Add a seam test with a real path shape: a pinned file under a `runs` component is accepted, and an unpinned `runs` path is refused. Claude3 re-reviews the fix delta.

### D007 — 2026-10-21T15:12:59Z — Codex2, FROM_CODEX2/0575: unit 3 (7-call admission) review disposition

**DISPOSITION: review PASS, 0 blocking, ready for root adoption (0851 item 5).** The record is `verify_c3_seven_call_unit3/RESULT.json` (`7d00794a`). No guard, launcher or binder successor is needed now.

**Conditional (N1).** If unit 2's direct_context or `cfg.context_module` loads the c2v004 ledger wrapper (`7c9b4248`) inside native_preflight, guard014's compile contract (L27–29, L150) refuses it. In that case the smallest successor is guard015 = guard014 + {`7c9b4248`: {`79e8936d`}}, with launcher016 and binder012 changing only the guard pin. Codex3 should design unit 2 to avoid that load. Root acts on the fill-checklist NOTEs N3–N10.

### D008 — 2026-10-21T16:06:50Z — reviewer for the verdict-day runbook's narrow check (0850 item 2; Claude3 0300)

**RULING (a review-disposition detail).** The narrow check of `RUNBOOK_EXEC_C3V001.md` (`553a0e2c`) is opened to **Codex2**, alongside Codex3 and Codex1, and goes to whichever lane is free first.
- **Basis:** 0850 asks for "a narrow check by Codex3 or Codex1 if either is free; otherwise root reads it". Codex3 is on unit 2's fix (0298) and Codex1 on the importer. Codex2 has been idle since 0578 (15:15Z), with both 0848 items reviewed PASS.
- **Independence:** Codex2 authored none of the runbook's command sources. The sheet is Codex1's, and the J addendum is Codex3's.
- **Unchanged:** root still reads the runbook if no check lands before Thu 01:00 CDT.

**Scope:** no physics, blinding, launch or adoption.

### D009 — 2026-10-21T16:18:48Z — verdict-day runbook: review disposition (0850 item 2; Codex2 0580, 0583)

**DISPOSITION: RUNBOOK_EXEC_C3V002.md (`3a148748`) passes its narrow check with 0 blocking (Codex2 0583, `584b1f64`); F-STOP-1 is closed. It is the runbook root executes from (0851 item 6).**
- C3V001 (`553a0e2c`) is superseded.
- The two nonblocking notes stay in the post, not in a C3V003, to avoid churn before the verdict:
  - (a) root records the twin DRY's own leaf `dry/S0_SEED_CW8_TWIN_A1_<UTC>_<pid>` and its plan, fill-check and dry-verdict files before START, because the twin does not print that location;
  - (b) the header line naming the v001 generator is cosmetic; the C3V002 generator is `build_runbook_c3v002.py` `39d25274`.

**Scope:** a review disposition; root uses the runbook at its own discretion.

## D010 — 2026-10-21T17:25:56Z — 0852/0853 (A293–A295): escalated, not ruled

- **What happened:** the row 302, 501 and 504 EPS_UNCERTIFIED analysis, and the 1.1× rule precision question, were escalated to root as FROM_CLAUDE3/0309 (`ROOT_ESCALATION`). The analysis of record is `w3_row302_eps_c3/ANALYSIS_C3V001.md` f80c9a3e.
- **Why it is not a deputy ruling:** a registered physics-process criterion, the engine path and the L2 composition are outside the remit (0851; A294 and A295 reserve the final text for root).
- **The recommendation (root's to adopt):**
  - M = 10 and f = 0.1, that is ε_s ≤ 1 % of eps_max;
  - |L2 − L1| ≤ 1e-6;
  - a dense envelope audit with ratio ≤ 1.05;
  - conservative substitution ε := M·ε_s;
  - L2 at 6 calls.
- **Facts posted** in 0307 (halvings 404 and 405 certify) and 0308 (rows 501 and 504 uncertified).

### D011 — 2026-10-21T17:35:44Z — 0855 (A296): F5-gap proposal escalated (0312); A296 integration NOTE (0311)

- **Escalated, not ruled:** FROM_CLAUDE3/0312 (`ROOT_ESCALATION`), proposal `f5_gap_proposal_c3/F5_GAP_PROPOSAL_C3V001.md` 671f8948.
  - It covers the engine path and a registered campaign rule, so root rules after Thu 18:00Z.
  - Recommended: the hold ladder, Jacobian-side NUMERICS_UNAVAILABLE only, no substitution for other purposes, the build landing before W1, and pre-certification of the FD points.
- **NOTE 0311 (FORMAL):** an A296 successor EPS adapter must enter C1's `approved_certificate_producers`, and the signed policy 55926860 must be re-signed, before W1. The cache id binds the policy.
- **Context:** Codex2 0586's independent analysis agrees with ANALYSIS_C3V001 on every A296 condition.
- **Erratum, cosmetic:** D010 was written with an `##` heading; the earlier entries use `###`.

### D012 — 2026-10-21T17:53:22Z — A297 review of Codex2 0589 (A296 numerical successor): review PASS, ready for root adoption

- **Result:** `review_a296_successor_c3/RESULT_C3V001.json` ef2aa83c62d6ecda367a18a60c593c8749881c6d6cd77beec0a548f2e8a55459, with 0 blocking and NOTEs N1–N6. Posted as FROM_CLAUDE3/0315.
- **Basis:**
  - my own readback and the rule function reproduce the successors byte for byte;
  - 45/48 records UNCHANGED;
  - tests 89/89;
  - the blinding-clean path was confirmed under a blocking hook;
  - the original saved dense audits were reproduced exactly at [45, 46] and [64, 65].
- **Scope:** a review disposition. A297 adopts on this PASS, and adoption is root's.

### D013 — 2026-10-21T18:38:04Z — Codex2 0591 (A296 full integration, 0856/A298): review FAIL, 3 BLOCKING, one root cause; fix per D006

- **Result:** `review_a296_integration_c3/RESULT_C3V001.json` 9bcee6ad0c4eb4dd363019609d2e92fba0dc20a3a051d6e4081ff63e04acfa94. Posted as FROM_CLAUDE3/0317.
- **F1–F3:** the inherited cx3v001 `runs` refusal of the honest pinned custody read, in:
  - `direct_cert_lookup_a296` (5288bc17);
  - `direct_preflight_cert_a296` (90905236);
  - `registry_verify_a296` (98f687a1).
- **Fix:** D006 applies unchanged; re-issue those three, or `eps_lineage` plus its cascade. Re-review on the delta.
- **Everything else PASSES and may proceed:** the bridge (C1 producer 7), core, guards, stage, Step4, the W1 chain and the C1 list.

### D014 — 2026-10-21T18:45:40Z — verdict-day runbook C3V002: a second narrow check PASS (Codex3 0706), recorded

- **Codex3's REVIEW_CX3V001.json** (ca185900) and CHECK_RECORD_CX3V002 (c8c945a1) give PASS for RUNBOOK_EXEC_C3V002 (3a148748):
  - 489 code lines agree with the XREF;
  - 326 source comparisons, 0 mismatches;
  - `bash -n` on P0 plus all 26 calls;
  - the probes stop as intended.
- **Its only note** is the cosmetic header naming the v001 generator, already in D009 (b).
- **Lineage, as disclosed:** Codex3 authored the J addendum and the section 5/6 checker.
- The check was taken before my 0319 stand-down note landed, and it adds independent assurance. The D009 disposition is unchanged: root uses the runbook at its discretion.

### D015 — 2026-10-21T18:58:03Z — Codex2 0593 (A296 integration delta, D006 scoped custody pin): review PASS, ready for root adoption

- **Result:** `review_a296_integration_c3/RESULT_C3V002.json` ef6f71a6505662c69a7cb5ab4f103e0ee5b0242d68a0b450927f587a64b8146e. Posted as FROM_CLAUDE3/0320.
- **F1–F3 are closed,** by the single exact a2f10 custody pin inside `custody_reads()`; everything else stays strict.
- **The overall A296 integration is PASS, 0 blocking.** The root-owned prerequisites are listed in 0320.
- **Unit 2 (cx3v001, Codex3)** remains FAIL under D006.

### D016 — 2026-10-21T23:11:04Z — root 0857 item 4: A296 R3 approved-signer reviews for rows 302, 501 and 504 routed to Codex3

- **Ruling:** Codex3 signs, as the root-approved CP-1 EPS signer lane (A202 ruling 1). The excluded reviewer lanes are [Claude2, Codex2]; the operator lane of all three POINT_START files is Claude2, from bytes.
- **Prerequisites (TESTED):**
  - the successor records and R1(c) audits passed in 0315, including `blinding_clean_audit_path_A297`, and A297 adopts them;
  - the stage v002 0c9d0243 stage-only outputs (CX2V003) are TESTED and ok.
- **Dispatch:** FROM_CLAUDE3/0324, 429100b0df22fb36. It carries the exact per-row sources and the review contract (fields checked by stage `review_gate` L180–199 and core L405–413; `adapter_sha256` = bridge 1eb94a51).
- **Placement:** outside any adapt output root.
- **Waits for root:**
  - review-sha approval and `--approved-signer-lane Codex3`;
  - the producer set (bridge 1eb94a51, rule 669f0640, audit 618ba8fa, original a1dcdea8);
  - the adapt call.
- **Target return:** Thu 2026-10-22 15:00Z.

### D017 — 2026-10-21T23:20:16Z — F4 (new, blocking for W1 on the A296 chain): the adopted acceptance step refuses the A296 campaign entry; Codex2 builds a successor that changes one line

- **Finding (FORMAL, fail-closed):**
  - `h3_accept_call_c2v004` (eb895263) L94/L143 requires `ENTRY_NAME == 'h3_campaign_entry_c2v004'`.
  - The A296 entry (05738509) L63 and every cascade-generated entry (r12 placeholder af4e4f36 L63) carry `h3_campaign_entry_a296_cx2v001`.
  - README_CAMPAIGN_CERT_C2V004 L80 routes campaign calls only through the step.
- **Erratum to 0320:** the chain verdict becomes FAIL, 1 blocking, until the successor is reviewed. The 23-file results stand.
- **Ruling:** Codex2 builds `campaign/h3_accept_call_a296_cx2v001.py`. It differs from `h3_accept_call_c2v004` only in ENTRY_LINE and the matching refusal, docstring and usage text, and comes with bounded synthetic tests (see 0325 §3).
- **Target:** review-ready Thu 15:00Z; Claude3 reviews; it joins root's Thu adoption set.
- **Also recorded:** the deps record must carry `deps.guard` = 3939bc47 and the exact seven producers.
- **R3 reviews (D016 return, Codex3 0709):** Claude3's gate check PASSes both gates; 14/14 negative controls refused per row. Evidence: `root_thu_checklist_c3/evidence/R3_GATE_CHECK_C3V001.json` 073b9c36.
- **Post:** FROM_CLAUDE3/0325, 2485fd1cddb9270f.
- D017 follow-up 2026-10-21T23:28:58Z: Codex2 0596 successor edcd3ffa reviewed PASS 0 blocking (review_f4_accept_c3/RESULT_C3V001.json 91950348; post 0326); A296 chain back to PASS.

### D018 — 2026-10-21T23:30:17Z — C1 successor (A298; root 0857 item 2): a deterministic proposed draft and a fill-tool successor are prepared, and Codex3 pre-signs the C1 policy re-review now

- **Draft:** `root_thu_checklist_c3/c1_successor/draft_c3v001/C1_H1_DRAFT_C2V003.json`, 387b1b35.
  - Builder: `build_c1_successor_draft_c3v001.py`, 2fec6c97. Leaf diff: 5966bb66.
  - The tail changes only in entry 7 (bridge 1eb94a51) and in the `certificate_policy_review` placeholder. Tail digest without the review: 3c03bae3. A separate recomputation agrees.
- **Fill tool:** `fill_c1_pin_c2v003_c3v001.py`, 8a645ca3. It changes constants and labels only, and was generated from v002 3faf4a6c by counted replacements. Synthetic tests: 10/10.
- **Ruling:**
  - Codex3 signs `DDO154_CERTIFICATE_POLICY_REVIEW_C1_H1_CX3V002` against the draft now. This saves root a round trip; any change to the draft voids it.
  - Codex3 prepares the campaign re-sign CX3V002, which waits for root's new C1 sha.
  - Root rules on the draft, runs the fill and records it in V006.
- **Post:** FROM_CLAUDE3/0327, 63f1515deba3546e.

### D019 — 2026-10-22T03:36:25Z — root 0861: contingency rule for taking over the L2 importer (logged as root asked; root ratifies)

- **Trigger:** Claude3 takes over the importer build if Codex1 has posted no status by Thu 13:00Z (08:00 CDT), posts that Fri Oct 23 12:00 CDT is unreachable, or stops at its credit floor.
- **Takeover setup:**
  - start from `external_importer_cx1/` (read only) and rulings A278, A283, A285 and A287;
  - write only in `external_importer_c3/`;
  - reviewer: Codex2 (narrow) or Claude4 (Fri 19:00Z on), named in the handoff;
  - if Fri noon is out of reach, report early (A262 fallback).
- **State at logging:**
  - Codex1 posted status FROM_CODEX1/0240 (FAIL, 3 blocking; Fri noon "a target, not yet verified reachable").
  - The trigger is not met. Claude3 re-checks at 13:00Z. Incremental review continues; the last pass was 0296.

### D020 — 2026-10-22T03:36:25Z — deputy corrections to root 0859 and 0860, posted in FROM_CLAUDE3/0330

- **0859 (Codex2, post-C1 pin successors):**
  - FORMAL from source: on the A296 path, lookup v003, preflight v003 and registry_verify v003 take C1 from the ROOT_BOUND binding.
  - The 24 sources hold the frozen C1 only as a296_binding `OLD_C1`, which is lineage, and as an unused lookup v003 constant. Only the legacy, unbound paths reach cx3v001.
  - Guidance: Codex2 confirms this by its own trace. If its trace agrees, it pre-stages a synthetic bound-mode test with a stand-in C1, plus a finalize step for the metadata rebinding (checklist 3d). If its trace finds an enforced pin, it builds that successor as 0859 says.
- **0860 (Codex3):** two re-signs.
  - The C1 policy re-sign must precede root's freeze; it is independent of the C1 sha, so sign it now.
  - The campaign re-sign follows the freeze.
  - Without the first, root's R3 deadlocks.

### D021 — 2026-10-22T07:54:02Z — Codex1, FROM_CODEX1/0245 (`48fc52d0`) question 1: the acceptance-dependency record for direct-call acceptance

**RULING.**
1. **Direct calls are accepted with exactly the campaign's own acceptance-dependency record:** the record root fills at checklist C3V002 (`81e24b58`) step 3f (R7). An imported result is then checked by the same producers as a natural W1 result.
   - Template: `ACCEPT_DEPS_RECORD_C2V001_TEMPLATE.json` (`48ec0e01`).
   - `deps.guard` = the A296 b1 guard `certificate_guard_b1_a296_cx2v003.py` (`3939bc47`). Guard `9e3fc109`, which appears in the template and in CONTINUATION_CX1V134's pins, is superseded on this path.
   - `policy.approved_certificate_producers` = the ordered seven of the new C1. Bridge `1eb94a51` is the seventh.
   - `deps.lo_core`, `deps.srb_adapter` and the policy fields come from the frozen C1's `acceptance_policy_inputs_from_c1`. Draft C2V003 (`387b1b35`) gives the values: lo_core `12d36305`, and srb_adapter `adapt_call_srb_rot` (`08e9ac0a`). The real C1 sha exists only after root's fill.
2. **The record is a root-supplied input.** The importer entry takes it only as a root-supplied `{path, sha256}` invocation input, under the same rule as importer_root_binding v002's other anchors. It never derives the record from C1, a candidate or a cache entry.
3. **The inert seed path** uses a record with these values that is labeled SYNTHETIC and never placed in a production path.
4. **Codex2's 0859 post-C1 pre-stage is not this input.** Its acceptance dependencies carry no C1 pin (Codex2 0602).

**Basis:** A262 ("admits by reference … with full provenance checks"); A278; the A296/A298 chain; checklist step 3f; the template's `sources` column. **Scope:** an interface and selection detail. Root writes the real record.

### D022 — 2026-10-22T07:54:02Z — Codex1, FROM_CODEX1/0245 (`48fc52d0`) question 2: phase authority under D002 item 3. The importer writes no phase journal and no checkpoints

**RULING.** The proposed design (a root-pinned phase binding, plus importer-appended ADMIT/CONSUME/finality events and checkpoints) is not adopted. It is replaced by a stateless rule that derives the phase state from root's envelope files.

This changes how D002 item 3 is implemented, not what it achieves. An L2_DIRECT import is refused at every use once the phase's final check fails, and freezing consumption already made stays root's remedy.
1. **Phase identity** is the START pin already in root binding v002 (`envelope.start`, `47569b91`). It is re-hashed at each use.
2. **Phase state** is derived at each admission and at each use of an imported entry, under the held lock. The sources are the files that root's pinned envelope tool wrote in `$R/ENVELOPE_L2_DIRECT`. The importer writes nothing there (D002 item 1).
   - (a) **OPEN:** no `end`-labelled snapshot exists. An admission requires the D002 item-1 observation and the D005 checks.
   - (b) **FINAL_PASS:** an `end` snapshot exists, and the pinned tool's signed compare report for exactly (the bound START, that END) has outcome OK. This is checked with the pinned compare-core checks of `final_envelope_evidence_cx1v001` (`635b4daa`).
   - (c) **Anything else refuses with `INVALIDATED_BY_ENVELOPE`.** That covers an `end` snapshot with an INVALIDATE report, with no report (compare refused with exit 2 and wrote none), or with a malformed report. Rule (c) closes the case where a refusal leaves no file.
   - The short window between root's END snapshot and its compare also refuses. END follows the last import or discard, so no admission is lost.
3. **Import association** is the cache entry's DIRECT_EXTERNAL provenance, matched to its stage-a register record (row, key, spec pin, call root) under the bound register pin. There are no ADMIT or CONSUME event files.
4. **Restart is stateless:** every use re-derives items 1–3.
   - The parent cache's exclusive put stays the only write.
   - An interrupted admission leaves either nothing or a complete cache entry, under the parent's own semantics.
5. **Freeze.** After a failed final check, the importer's only duty is to refuse further use, per (c). Freezing consumption already made is root's remedy, escalated at that time (D002 item 3).
6. **Reuse, not new code.**
   - `cache_phase_forward`'s `phase_use` callback becomes this stateless check, built from `final_envelope_evidence` v001 and the envelope observation guard.
   - The following leave the critical path but are kept as predecessors; nothing is deleted:
     - `phase_journal_storage_cx1v001.py` (`37605e6d`)
     - `phase_checkpoint_cx1v001.py` (`65c95450`)
     - `phase_invalidation_cx1v001.py` (`9b7013ae`)
     - `cache_phase_checkpoint_adapter_cx1v001.py` (`39317638`)

**Basis:** A283 item 3, A226, D002, D005. The envelope tool's exits (OK 0, INVALIDATE 3, refusal 2, possibly with no report) are as Codex1 found in its source audit (CONTINUATION V126).

**Scope:** an interface and design detail inside A283, with no physics, blinding or launch change. Every branch stays fail-closed. Root ratifies.

### D023 — 2026-10-22T07:54:02Z — root 0862 (`44941222`) and 0861 (`3546128b`): importer assessment disposition. No takeover; Codex1 continues under a helper freeze, a set build order and checkpoints

**RULING (within D019).**
1. **No takeover now.** Codex1 stays the builder, and Claude3 stays the incremental cross-family reviewer (A262).
2. **Helper freeze.** This makes Codex1's own 0244 proposal binding. Until the importer is review-ready, the only new files are:
   - the seed-path integration pieces: the entry, the VALID leg, the D022 callback and the production acceptance loader;
   - their tests;
   - successors that fix review findings.
3. **Build order:**
   1. refusal controls on the 0247 path (already in progress);
   2. the D021 record and a pinned production acceptance loader replacing the H55 seams, with dependency closure checked only against the record's pins;
   3. the D022 callback;
   4. the installed authenticated entry (I3: root binding v002, register a/b, runtime-capture checks, envelope observation and VALID; factory v002 still refuses VALID at L28);
   5. whole-engine lazy-import equivalence on the inert engine against the baseline (A262/A271 invariance);
   6. policy V007 and the freeze record (root binding `runtime.freeze`), then the review-ready post.
4. **Checkpoints:**
   - Thu 13:00Z (the D019 re-check): a Codex1 status giving the state of steps 1–6.
   - Thu 18:00Z (root's reset): steps 1–3 TESTED inert, or a post naming the exact blocker.
   - Claude3 then gives root a go/no-go recommendation for L2. The decision is root's.
5. **Takeover triggers.** These refine D019 and keep its Fri-noon trigger.
   - **Credit:** at ≤10 %% credit, Codex1 posts a handoff file (seed-path state, open steps, pins) and Claude3 takes over from it. Codex1 stops at 5 %%.
   - **Silence:** after 60 min of silence while steps are open, Claude3 pings. After 120 min, Claude3 takes over from the last continuation.
6. **Fallback.** Suppose no reviewed, frozen importer exists when the direct batch's runtime capture must be taken. That moment is after the importer freeze and immediately before the 7-call launch (A283 item 3, D005 item 5).
   - Then the 7 calls run as natural campaign waves (A262 fallback). Custody and physics are unchanged; the cost is the L2 saving.
   - Deferring the importer pin past START would let the importer be written after the direct results exist. That is a custody change and root's call, and it is not recommended.

**Basis:** 0861/D019, A262, A265, A271, A283, D002, D005; Codex1 0244, 0246 and 0247. **Scope:** a build-order and ownership ruling. No physics, blinding, launch or date change.

### D024 — 2026-10-22T07:58:30Z — runbook finalization (0850 item 2) and two verdict-day decisions: escalated, not ruled (FROM_CLAUDE3/0334, ROOT_ESCALATION)

- **E1:** HEADLINE11 stays on C1 V001 and the c2v004 r12 chain, and the A296 chain is for the campaign only. This is Claude3's reading; root decides, because adoption onto the verdict-day path is excluded from the deputy remit.
- **E2:** A296's V006 entries (R1, R3) must avoid the seed's V006 write window (B11.1 up to the confirmed launch record). Root decides the order.
- **Runbook:** C3V002 stands. The pins re-hash equal and no command changes; record `7078054a`.

### D025 — 2026-10-22T08:06:30Z — Codex2, FROM_CODEX2/0602 and 0603: post-C1 finalizer v004 review disposition and placement of checklist item 3d

- **Review:** `finalize_post_c1_cx2v004.py` (`5743cfef`): review PASS, ready for root adoption at step D1. Record `a849ca05`, 0 blocking, NOTEs N1–N3.
- **RULING:** item 3d moves from Thursday R6 to step D1, the direct-batch preparation, after R5 and once its four inputs exist.
  - The inputs are the lookup request, the bound records, their verification and the admission predecessor. They are root's direct-batch artifacts, and none exists before the batch.
  - Codex2 builds nothing further, and its 0603 wait is closed.
- **Basis:** the finalizer's input checks (L156–184); A278; checklist C3V003 (`a56cc86a`).
- **Scope:** a sequencing and build detail. Root writes every input.

### D026 — 2026-10-22T08:09:50Z — clarifies D022 item 2: envelope-tool sidecars in `$R/ENVELOPE_L2_DIRECT` (from Claude3 0338, finding F1)

**RULING.**
- A `X.sha256` entry is accepted only as the pinned envelope tool's sidecar: `X` must exist in the same folder, and the bytes must be exactly `"<sha256 of X>  <basename X>\n"` (`pinned_input_envelope_c2v003.py` `9d531381` L548–549).
- A valid sidecar is skipped from JSON parsing. A sidecar whose `X` is missing or whose content is wrong refuses.
- Every other non-JSON entry refuses, as before.
- **Basis:** D022, A283 item 3, A115. Without this rule the honest tool output refuses every import (TESTED, 0338).
- **Scope:** an interface detail. Fail-closed is unchanged for every non-tool entry.

### D027 — 2026-10-22T08:14:32Z — r12 publication collision (0339). Escalated to root as option (A) or (B). Deputy hedge: Codex3 pre-stages an A296 variant of its §6 gate checker

- **Escalated, not ruled.** Which chain verdict-day B6 runs touches the verdict-day path, so root chooses (A) or (B) in 0339. Claude3 recommends (A).
- **RULING (deputy; a non-launch review tool):** Codex3 pre-stages `check_verdict_gates_cx3v004`. It is `check_verdict_gates_cx3v003` (`78358dac`) with `GEN` set to `make_campaign_cascade_a296_cx2v001.py` (`114c90c3`) and the baseline set to `placeholder_chain_a296_cx2v001/v006r12_c4`. Nothing else changes.
  - It is a hedge, and it is unused unless root picks (A). Adoption onto the verdict-day path stays root's.
- **Codex1 0252:** the importer authenticates the published A296 wrapper and entry only as root-supplied anchors. The `integration/campaign` copy is the cascade's source text.

### D028 — 2026-10-22T08:43:27Z — Codex1 0257/0258: FINAL importer review disposition (A262; D023 step 6)

- **review PASS, ready for root adoption once F2's delta passes.** Claude3 0347; 0 blocking code defects; policy V007 `e41240d7`, entry `95ed2a2f`.
- **F2 (required before the freeze):** name P2 `runtime_distribution_capture_cx1v004` (`f9c508a6`) as the capture producer, with its root command and pins, and mark P1 `runtime_capture_entry_cx1v003` (`c58aff70`) superseded. TESTED: P1 refuses on the real interpreter; P2 records validate and compare equal.
- **NOTEs for root:** N1 the records root; N2 the W1 `campaign` pin `d35d5d4a`; N3 the publish collision (0339/0341).
- **Basis:** A262, A283 item 2, A285, A287, D004, D005. **Scope:** a review disposition. Adoption and the operational freeze are root's.

### D029 — 2026-10-22T08:47:41Z — Codex1 0259: F2 delta review disposition. The importer review is complete

- **review PASS, ready for root adoption:** policy `IMPORTER_POLICY_CX1V007_F2.json` `6c8439ec`, entry `importer_entry_cx1v001` `95ed2a2f`, templates v002, root binding template `e2aecea4`, START pins `96265e2d`.
- The 13-leaf policy delta was TESTED (Claude3 0348). P2 is the only capture producer, and P1 is superseded.
- **Root items:** N1–N3 (0347). N3 depends on root's A302 amendment (0339/0341).

### D030 — 2026-10-22T11:11:18Z — root 0867 (A307): disposition. No rebuild of the reviewed I1/I2. Claude3 builds the stage-b register-binding writer; Codex1 builds the stage-a register writer

- **Correction:** I1–I3 are already built and review-PASS (D029). Claude3 does not rebuild them unless root says so explicitly.
- **Gaps:** neither register writer exists (`register_two_stage_cx1v003` `0d5aae44` only validates).
  - Stage a goes to Codex1 per 0867. Claude3 builds it if Codex1 hits its floor first.
  - Stage b goes to Claude3, in `external_importer_c3/`. The reviewer is Claude4 (Fri 19:00Z) or Codex3 (narrow).
- **Claude3 reviews the launch-time pieces:** P2 `f9c508a6` (TESTED in 0347; source review to follow) and the START pins `96265e2d`.
- **Basis:** 0867, A283 item 1, D005, D029. **Scope:** build allocation within 0867. No launch, physics or date change.

### D031 — 2026-10-22T11:14:53Z — launch-time review (Codex1 0264) and the SL-1 gap: Claude3 builds the direct-launch-record writer together with the stage-b binding writer

- `speculative_register_writer_cx1v001` `ce6f2a90`: review PASS for its scope, with NOTEs R1 and R2 (0357).
- **SL-1:** `SPECULATIVE_LAUNCH_L2_V001` has no writer or template, yet `check_launches` requires it. It is required before the direct launch.
- **RULING:** Claude3 builds one tool in `external_importer_c3/` with subcommands `direct-launch` and `binding`, both validated against the pinned consumers before an exclusive write. Reviewer: Codex2 (narrow). Codex1 conserves its credit.
- **Basis:** 0867, A283 items 1–2, D005. **Scope:** build allocation and an interface detail.

### D032 — 2026-10-22T11:18:58Z — Codex2 0617: F5-R2 evidence contract, approved as the design basis for the inert backlog #2 build

- **Contract:** a pinned root decision binds the probe miss, the identities, HELD_UNCERTIFIABLE, the registered-rule failure, the A296 failure or ineligibility, and the verifier and rule pins. It is revalidated on the command and on every reuse, and a point that now certifies is refused.
- **Evidence:** every record is the output of an existing pinned producer, with schemas named by the builder from the sources.
- **Scope:** inert build only. Root ratifies the contract at adoption (A298 phase boundary). Physics is unchanged until adoption.

### D033 — 2026-10-22T13:50:15Z — root-records writer v002: review disposition

- `l2_root_records_writer_c3v002.py` `65741e7ddb3c5a25`: **review PASS, ready for root adoption** (Codex1 0276; review `78ff67a1373acb5a`; 25/25 tests).
- v001 is NOT FOR USE. The exact commands are in 0369.
- Backlog #4 is confirmed to Codex1 (inert; reviewer Claude3).

### D034 — 2026-10-22T13:54:49Z — Codex1 0280: backlog #5 (cw8 v003-N3). A diagnostic-only lock-refusal record is approved

- **Record:** `CW8_LOCK_REFUSAL_RECORD_V001`, written by exclusive create at a root-supplied path that is outside `worker_choices` and never inside a missing launch root.
- **Authority:** none. No selection is made, the existing cfg and choice contracts are unchanged, and no cohort is ever published after a lock failure (N8).
- **Delivery:** a new root-invoked successor entry. Claude3 reviews it; root adopts it.
- **Scope:** an interface and hardening detail. No launch or physics change.

### D035 — 2026-10-22T14:03:06Z — backlog #8: Claude4 0258 NOTEs. Writer c3v002 built; delta review by Claude4

- c3v001 `d8db59ce`: review PASS with 0 blocking (Claude4 0258).
- **RULING:**
  - S2: `close` refuses a second closure for the same call in the records folder.
  - S3: validation copies go in a private temporary folder outside the records folder.
  - S4: PHASE_2 only; PHASE_1 is refused until root rules.
  - S1: a root procedure in README C3V002 (close only stopped calls; registry binding and last attempt receipt; one folder; roster build right after).
- **Objects:** `schedule_ceiling_writer_c3v002.py` `6b773463c7fbfa98`; tests 33/33 with 5 mutants killed (`d39f5b4b`); README `a28c9321`.
- **Scope:** a build and interface detail. Root still rules the A272 folder and whether Phase 1 is in scope.

### D036 — 2026-10-22T14:03:06Z — backlog #6 (G26 test successor): Codex1's claim (0285) is confirmed; Claude3 reviews it. Claude3 claims #7

- 0871 listed #6 and #7 for Claude3 to build. Codex1 claimed #6 at 14:00Z and delivered it at 0286, so Claude3 does not duplicate it. The backlog row is "B: any Codex; R: Claude".
- **Reviews:** Claude3 reviews #6 (0286) and #5 (0284). Neither is Claude3's build.
- **#7** (the roster builder step7/custody parent-exists check, A272 hardening) is claimed by Claude3 as builder. Claude4 reviews it.
- **Scope:** backlog allocation within 0871. No launch, physics or date change.

### D037 — 2026-10-22T14:03:44Z — backlog #7: Codex1's claim (0287, 14:02:21Z) came before Claude3's (D036, 14:03:06Z). #7 goes to Codex1, and D036's #7 clause is withdrawn

- **First claim wins:** Codex1 is the builder of #7 and Claude3 its distinct reviewer, as the backlog row "B: Codex; R: Claude" says.
- **Fallback:** if Codex1 stops before delivering (credit), Claude3 takes #7 over from Codex1's posted state.
- **Scope:** backlog allocation within 0871.

### D038 — 2026-10-22T14:04:59Z — backlog #7, FINAL: Codex1 yielded #7 (0288, 14:04:00Z, crossing D037). Claude3 builds it, and D037 is superseded

- Codex1 stopped its build and kept an untested draft, `roster_parent_hardening_cx1/roster_builder_cw8_parent_cx1v001.py` `c8c38ee4`. It is preserved as an abandoned draft: not adoptable, not reviewed, and Claude3 does not edit it.
- **Builder:** Claude3. Codex1's credit is about 5 %; Claude3's is about 86 % (0871).
- **Reviewer:** Codex1, narrow, as offered in 0288, if its credit allows; otherwise Claude4 after Fri 14:00 CDT.
- **Scope:** backlog allocation within 0871.

### D039 — 2026-10-22T14:26:07Z — backlog #2 (F5-R2) is reassigned to Claude3 (root 0871 lists it for Claude3). Codex2's claim (0615/0616) lapses

- **Facts:**
  - Codex2's last post was 0617 at 11:16:53Z.
  - 0871 (13:41Z) puts Codex2 at 0 % credit.
  - The announced build folder `claude_artifacts/f5_r2_wrapper_cx2/cx2v001/build/` does not exist, so there is no partial work to preserve.
- **RULING:**
  - Claude3 builds #2 after #1, in 0871's order, under the D032 contract.
  - Codex2's FORMAL findings in 0616/0617 are binding design inputs: a separate cache kind, and the current request's purpose, family and branch checked on every use.
  - Reviewer: Codex2 after its reset if available; otherwise Codex1 (narrow) or Claude4.
  - If Codex2 resumes before Claude3 starts #2, Codex2 posts at once and the deputy re-arbitrates.
- **Scope:** backlog allocation within 0871. Inert build, held; adopted only at a phase boundary on root's ruling (A298).
