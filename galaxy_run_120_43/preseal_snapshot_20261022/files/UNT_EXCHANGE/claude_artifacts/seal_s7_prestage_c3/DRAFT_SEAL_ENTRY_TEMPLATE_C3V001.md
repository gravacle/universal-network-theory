# DRAFT_SEAL_ENTRY_TEMPLATE_C3V001: the fields of the seal entry, and where each pin comes from (DRAFT for root)

**From:** a Claude3-lane helper, for the lead, under root dispatch 0850 item 4 (P-105).
**This is a template, not an entry.** No value is invented. Every `<<…>>` is a placeholder that root fills from bytes (`shasum -a 256`) or from `date -u`. The header time is substituted from `date -u` and never typed.
**Pins already fixed by the named sources** are filled with full sha256 values, copied from bytes or from the named V006 sections. The lead re-verifies every one from bytes when the entry is filled.

## 0. Rules the entry must meet (FORMAL)

- **R-a. Placement.** It is appended to V006 at the END trigger of the write freeze (DRAFT_WRITE_FREEZE_WINDOW §2). It must be **the first V006 heading whose section contains the rendered text's sha256** (text §11). No earlier entry may contain that sha (M-6 item 2).
- **R-b. Acyclic.** The rulings on M-1 to M-16 are cited by id, or made here (M-6 item 2). The entry is outside the V006 entry table, and so is every later entry.
- **R-c. What it registers** (M-6 items 2 and 5; M-12 "Seal"; M-15; text §8 header):
  - the text, the classifier and the agreement record;
  - [r3a] the Phase-1 registry root, and the `band`/`agree` shas;
  - the gate-status list;
  - the timing attestation.
- **R-d. Closure.** The seal is complete only when T7 passes against this entry: the prefix sha check (byte check R6), with `verdict_currency` read from the check's JSON, not from its exit code (M-6 item 4).
- **R-e. Reading gate (A133 §2 row 2).** The seal **and** the S1 reading must both be recorded before any Phase-1 NGC value is read. Until then, Phase-1 reads stay validity-only.

## 1. The template

```
## A<<n>>: SEAL. The r3a miss-reading prereg and the M-12 classifier pair are sealed; the V006 write freeze closes (UTC <<date -u>>)

**1. Sealed text (M-6 item 2).**
- PREREG_MISS_READING_R3A.md, as rendered: `<<absolute path>>` sha256 **<<64-hex>>**
  (the sha that check T7 uses to find this entry; no earlier V006 entry contains it).
- ROOT_ITEMS_R3A.md: `<<path>>` `<<sha256>>`. Expected to equal the basis `9c40b567410e066465f01b21d656398ce6abd9c62fd16959b8bb92ed56aee6ae` (byte check R4).
- CLAUSE_SOURCE_MAP_R3A.md: `<<path>>` `<<sha256>>`. Expected to equal the basis `03ded7fa39b4b7cf1400cd2f89536eed727ca8c420c97d60485afddcce771e09`, or to differ only by additions Claude4 lists (R4).
- V005_ENTRY_TABLE_R3A.json `<<sha256>>`; V006_ENTRY_TABLE_R3A.json `<<sha256>>` (both are named in the text's §8 header).
- Render basis: outside the nine §11 generator sites, the text is byte-identical to the template the M-12 classifiers were built on, `classifier_a_c4/build_c4v001/basis/PREREG_MISS_READING_R3A.md` `1e17eb459c43d40205e7ed913da16de8b67e2762fa5e1a440699de796d9216a5` (Claude3 byte check R2: <<TRUE/FALSE>>).
- SEAL CANDIDATE post: `/Users/bgm/Research/UNT_EXCHANGE/FROM_CLAUDE4/<<file>>` `<<sha256>>`. Publication time: <<the later of its date -u stamp and its file birth time>>.

**2. Root items.** M-1 to M-16 are cited by id as ruled in <<entry id(s); 0751 says "M-12 as A142 adopted it by id">>. M-8, scoring a FREEZE_INCOMPLETE manifest, as ruled in <<the A133 V006 batch entry>>. Nothing is re-ruled here, except <<none | list>>.

**3. M-12 (0751 ruling (a); A177; G17 as extended in <<entry id>>).**
- M-12 is cited by id. A176 is recorded as root's ruling on implementation B (M-6 item 2): the Claude2 builder; Codex1's kernels pinned by their V089 shas; the information barrier with its audited READ_LOG; and the distinct-lineage review of B before the Phase-2 seal (Codex2, A205 item 7).
- Classifier A, the CLASSIFIER: `claude_artifacts/classifier_a_c4/build_c4v004/classifier_a_c4v004.py` `e92aa30e22b98fea6c6e517702c02f77c43bfe429f69f8e0392963c94edc4cb0` (A173: 0 blocking, 476/476). Fenced runner: `<<tools/run_fenced_c4ep1.py path>>` `<<sha256 | not pinned>>`.
- Classifier B, the agreement partner, never run on real data: `claude_artifacts/classifier_b_c2/build_c2v005/classifier_b_c2v005.py` `cec5bfe9582899437aa715d78e1dfdb36089ebead04f840d4d68893b3d1251c7` (A193). README `5cfb42a134897efb0bb2cf447f8265f87f1354a1c572651de82068dd7966fc03`; HASHES_C2V005 `<<full sha; A193 gives 862ccb67>>`; READ_LOG `<<full sha; A193 gives 4aa328de>>`.
- A/B agreement record: `<<path>>` `<<sha256>>` (A193: 364 of 368 shared bundles; B352, B407, B412 and B419 are forged-only differences, recorded as A115 NOTEs; the verifier's 10 of 10 honest bundles agree).

**4. M-6 [r3a] pins.**
- Phase-1 registry root, for the PHASE_MISMATCH stop (text §1.1): `<<absolute path>>`.
- The A133 `band` and `agree` commands: `claude_artifacts/phase1_c2/phase1_c2v003b.py` `7d891ff7d81b0e9d103707d79c7a057cedc6dc1e893a0f4e9372a51d0b796dd4`, commands `band` and `agree` (A210: the tool of record; the fallback `d64351ec` is not used).

**5. The r3 candidate.** Claude4 0124 (`73f5faab369abcd20dc7901811b0eae9d0cb8a9135c0df61b66f185d7b9c71b2`) is withdrawn for the two-phase run through the FAIL mechanism, in <<entry id, stamped <<time>> | this entry>> (M-6 item 1 [r3a]).

**6. M-14, the STAGE0 successor.** <<PINNED: `claude_artifacts/stage0_successor_c2/prediction_freeze_c2v003g_stage0_c2v002.py` `d260ee308a7f215176cab1fff51e94cb52c7fc6cdd64aa4da48c66f8091820f0` (A175: pin-eligible), which registers STAGE0 as a Phase-2 step-5 call (text §6.3) | NOT PINNED>>.

**7. M-15, the gate-status list.** The first step-5 launch receipt is the S0 identity pair's: `<<path>>` `<<sha256>>`, written `<<UTC>>`.

| gate document | sha256 | pinned in | entry stamp (date -u) | status (ON-TIME = stamped before the first launch receipt) |
|---|---|---|---|---|
| <<…>> | <<…>> | <<A…>> | <<…>> | <<ON-TIME / LATE>> |

**8. TSR records (A177).**
- Flag record: `ROOT_TSR_FLAG_RECORD_V003` `7d3c1eb915cd9a85b1a9dab388e6a3fb6c218ef3d4e8e6f2dc726bea15c54070`. It supersedes V002 for the seal. `sealed.tsr_flag_record_sha256` and the freeze manifest's `input_files` name the same record.
- Support record (`schema: UNT_ROOT_TSR_SUPPORT_CX3V001`, its exact nine keys): <<`path` `sha256` | NOT YET BUILT (G7): read later, at the sha the score entry pins, as a carrier input (text §11 "Inputs are not changes")>>.
- Records the text names: compare `6f095f64a1f1acc2ad2910af12f645e18acdf16fb62bfd936386a61c47ef30e9`, N1 `8867c3766cc08585286ca969d4aa3fdec47fd9b15a8fe815d466346119c95c70`, GL nodes `ec1dcca572f295dab24e343650a519b6c96e3557e6ccc603f453dea490cb717d` (template §11, verified at render by T5).

**9. V005 and V006 currency (M-6 items 3–4).**
- V005 frozen whole-file sha `<<sha256>>` equals the table's `v005_sha256_read`: <<TRUE>>.
- V006 at Claude4's assembly read: whole-file `<<sha256>>`, trimmed `<<sha256>>`, read `<<date -u>>`. This equals root's FREEZE-OPEN post `<<FROM_CLAUDE2 path>>` `<<sha256>>`.
- The V006 table has <<N>> rows, one per `## ` heading before this entry. A133 is CITED_PINNED at section sha `<<sha256>>`; every other row is NO_CHANGE.
- r3a check: `<<JSON path>>` `<<sha256>>`. `verdict_currency` = <<value as read from the JSON>>; T5 <<…>>; T7 <<…>>. The T7 prefix check after this entry: <<PASS>> (Claude3 byte check R6).

**10. Write freeze (P-117).** Opened by <<FREEZE-OPEN post, UTC>>. This entry closes it. No V006 byte changed between the two (R5/R6).

**11. G17 (P-117).** The single CLASSIFIER role is extended to the M-12 pair in <<entry id | this entry, with the text of DRAFT_G17_M12_EXTENSION §2>>.

**12. Reviews.**
- Claude3's r3a single-pass delta review (A176 §2; A205 item 12): `<<path>>` `<<sha256>>`, verdict <<…>>, blocking <<n>>.
- Earlier rounds: the clause map's r3a fix, fix-check, fix-check-2, delta-check and delta-check-2 tables.

**13. Timing and attestation (M-6 item 1).**
- No step-5 NGC output value of either phase has been read. The fallback versions do not apply. The last SEAL CANDIDATE before the seal is item 1's post.
- Validity facts seen before the seal (receipts, valid flags and reason codes, and who saw them): <<list>>.
- Statements of no step-5 output value read, from each lane that touched the text or the classifier after step 5 launched (S0 START <<UTC>>):
  - Claude4 <<post path + sha>>;
  - Claude3 <<post>>;
  - Claude2/root <<post>> (B's builder and agents, if active after S0 START);
  - <<Codex2, if its B review ran after S0 START>>.
- Reading gate (A133 §2 row 2): the S1 reading is <<recorded in A<<m>> | NOT YET; Phase-1 NGC reads stay validity-only until it is recorded>>.
- The pre-score checks (text §1.1) run at the score entry, on the frozen Phase-1 manifest, which does not exist at the seal.

**14. Disclosures, for this entry and the PROVISIONAL (PHASE-1, FREEZE_INCOMPLETE) label.** Text D1–D5 of §2 of this template. The same text goes in root's `root_disclosures` record for the Phase-1 score.

**PLAN.** P-105 → DONE. P-117 → DONE (the write-freeze window and G17 recorded).
```

## 2. Disclosure text for item 14 (draft wording, from the named sources)

- **D1 (A176 §1; A190; A193).** Classifier B's integration was built by Claude2 on Codex1's kernels, which are pinned by their V089 shas. It sits behind an information barrier from classifier A, and it reads the producers' bytes for record forms (A190). The A/B agreement is therefore partly same-family.
- **D2 (A176 §1; A205 item 7).** For Phase 1, the principal's direction supersedes A133's "different lineage" requirement for B (A176 §1). A distinct-lineage adversarial review of B (Codex2, A205 item 7) is due before the Phase-2 seal. It does not gate Phase 1.
- **D3 (A205 item 13).** Concentration: on one path, Codex3 is the generator and output-diff reviewer, the campaign-set reviewer, the certificate-policy signer and the per-wave EPS signer.
- **D4 (A201, "Publication").** The Phase-1 score is published automatically as PROVISIONAL (PHASE-1, FREEZE_INCOMPLETE). AT-1 may SUPERSEDE it. ORIGINAL_K reads NOT_AVAILABLE. The band is never a tier. B is same-family. Phase 2 is the score of record.
- **D5 (A193).** A and B agree on 364 of the 368 shared bundles. The 4 that differ (B352, B407, B412, B419) are inputs that the producers themselves refuse, forged or malformed only, recorded as A115 NOTEs. The verifier's 10 honest, producer-built bundles agree 10 of 10.

## 3. Where each pin comes from

| Field | Pin source (named) | Known now? |
|---|---|---|
| Rendered text, ROOT_ITEMS, clause map, V005/V006 table JSONs | Claude4's final render and its SEAL CANDIDATE post (A205 item 11(1)) | no: Claude4, Fri 23 Oct 19:00Z onward |
| Basis template, ROOT_ITEMS and clause-map shas | `classifier_a_c4/build_c4v001/basis/` (A176), from bytes | **yes** (TESTED) |
| Classifier A sha | V006 A173 | **yes** |
| Classifier B sha, README | V006 A193 (sha); README from bytes | **yes** |
| B HASHES / READ_LOG full shas | A193 gives only the prefixes `862ccb67` / `4aa328de` | prefixes only; root hashes them |
| Agreement record | not in the named sources | no (root) |
| Fenced runner sha | README A names the path and the fence `175b995b…` only | no (root) |
| Phase-1 registry root path | the P-112/cw8 launch root that root creates before first use (A282 v003-N3; A272 checklist) | no (root) |
| phase1 v003b (`band`, `agree`) | V006 A210 | **yes** |
| r3 candidate 0124 sha | template §11 | **yes** |
| STAGE0 successor sha | README B producer table, `d260ee30…` full; A175 pin-eligible | **yes** (pin decision: root, R6) |
| Gate-status list | the S0 M-15 entry on verdict day | no (root, Thu 22) |
| First step-5 launch receipt | S0 identity-pair launch, Thu 22 | no |
| TSR flag record V003 | V006 A177 | **yes** |
| TSR support record | G7 (A177; A201 item 1) | no (root) |
| compare / N1 / GL-node shas | template §11 | **yes** |
| V005 sha, V006 shas, read time, check JSON | the render and the freeze | no |
| Claude3 review | R3A_DELTA_REVIEW_PRESTAGE_C3V001 run at the render | no |
| Lane no-read statements | each lane, after S0 START | no |
| S1 reading | S8, after u_A | no |
