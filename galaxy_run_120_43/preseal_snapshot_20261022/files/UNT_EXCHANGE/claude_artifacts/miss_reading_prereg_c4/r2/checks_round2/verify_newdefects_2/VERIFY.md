# VERIFY — round-2 finding R2B-02 (lens newdefects), adversarial verification

A helper of lane Claude4, under dispatches 0585 (`9003633293ff1db7d5153cabc338fd058cc199d834976b05543b7603b9433abd`) and 0606 (`dbb80c77cb085626303a9ce4e8d48e761dfd8525eece32022154e7e69881e28e`), run refute-by-default under 0592 (`b1a5310f…`). Nothing in the object was edited; Claude4 owns the fix round. Times are from `date -u` (start 20:31:00Z; report 20:41:41Z).

## Verdict

- **NOT REFUTED.** The quoted text is there, and it is defective as claimed.
- **Severity: SHOULD_FIX, confirmed.** It is not BLOCKING and not a NOTE (reasons in §4).
- **Fix: the direction is right, but the wording is not sufficient.** As worded it keeps one post-trigger choice, asks for output that cannot always be computed, leaves the field-map channel open, and misses one post-target trigger. A better fix is in §5.
- **One small correction to the finding.** C-9 L496 can also be read as granting the same unconditioned NOT_READ, rather than scoping it to a stop. Either way C-9 calls the risk closed, so the defect stands. The clearest sign of the intended scope is the CSM B-5 row ("post-defect rulings limited"), which the binding text does not carry.

## Object (verified from bytes against round2/HASHES_R2.txt; all 10 match)

| file | sha256 |
|---|---|
| PREREG_MISS_READING_R2.md | `97d5ce33ffa90e64ac208d36863c776460ad596fded2f376f1090a232e5ce407` |
| CLAUSE_SOURCE_MAP_R2.md | `38cd6852bdc32c240a6935671c82d618da399dd20e7d6adaa5aa2a26cd24f201` |
| ROOT_ITEMS_R2.md | `4907cf019c7bec62da646dc862f6c36c2b3aa03b11b761f36475c1056e968500` |
| NUMBER_PROVENANCE_R2.json | `ff6ca9b84384171285abbbc6d072a21346048884e9deff4fa79b0629f52c98bf` |
| TARGET_FREE_CHECK_R2.json | `624f278e02419ca28ea4a3a12fb869822cd4fddd8eaa721492d38996217c91f9` |
| TARGET_FREE_MUTATION_TEST_R2.json | `4445a9bf014e0cabe6d49cd0f45e4df1c388ac7c2c443df0d6f1d3a62214ec02` |
| INDEX_R2.md | `0d24b8fe778fb704398a7039f579977d92e51dfd152994d6e68048cffa03b926` |
| tools/check_target_free_c4v002.py | `4ae4f7053f18aa13416ad4e3d118d9250a959e72035c6e5f0c5f92305d8511aa` |
| tools/test_check_target_free_c4v002.py | `dc812342fa7c363e71949e3ecb2a206d68786ff5973280cf98909d03dd114f92` |
| tools/make_miss_reading_c4v003.py | `2132078f9779b01d5ad05c01b0280c218d160f6380f75ed5b99af893a1a2f9ab` |

The lens report is `checks_round2/newdefects/REVIEW.md` (`5b7c8b48…`), R2B-02 at L127–143.

## 1. Are the quotes there? Yes, all four.

| finding's quote | bytes in PREREG r2 |
|---|---|
| [C-1.1] L130–134 | L130 "**After target access,** root may only:"; L131 "correct a field map without changing any value; or"; L132 "declare the classification NOT_READ."; L134 "Root may never change a tier, zone, pattern, member or reading rule after target access." |
| [C-9] L496 | "\| Root discretion after a stop condition \| Every stop is checked before target access. Afterwards, only a value-preserving field map or NOT_READ (§1.1). \|" |
| [C-5.3] L357 | "**E3, the verdict line [C-5.3].** One line, always reported, computed on the frozen reference member." |
| [C-P] L25 | "Every outcome registers; nothing is prescribed." |

- **The evidence sentence is also right.** L120: "Every stop condition below is target-free." L121: each is checked "**before any target is opened**". L129: "Any of these stops the classification with CLASSIFICATION_INPUT_DEFECT, before target access."
- **NOT_READ is defined nowhere.** It occurs only at PREREG L132 and L496. It is absent from ROOT_ITEMS, the CSM, INDEX, NUMBER_PROVENANCE, TARGET_FREE_CHECK and all three tools (grep of each named file). No text says what NOT_READ covers, whether the classifier tables are still published, or whether the E3 line prints.

## 2. Is it really defective? Eight refutation attempts

**R1. "The clause sits under 'Pre-score checks', so it covers only the stop case." Fails.**
- Every stop runs, and must pass, before target access (L121, L129). If one fires there, the classification stops before any target exists. So the post-target clause never follows a stop; it is unconditioned by construction.
- In the v003g path no stop can newly fire after target access. My reproduction (§3) shows every stop input is byte-identical across target sets. So any post-target NOT_READ under r2 is a free choice.
- The author meant a post-defect scope. CSM L102 (B-5): "post-defect rulings limited (C-1.1)". Round-1 B-5's fix (`checks/targetfree/REVIEW.md` L165, `2eab5519…`): "Limit post-defect rulings to a field map that preserves values, or to NOT_AVAILABLE for the affected rows." The binding L130 kept neither "post-defect" nor "affected rows".

**R2. "Nothing is suppressed, because the headline stands (I-5)." Partly true; the defect stands.**
- The freeze module's within-error headline is untouched (L62).
- But this document produces the parts NOT_READ would remove:
  - OUTER_FAILURE (§2 L209);
  - the patterns;
  - the E3 verdict line (§5.3).
- V004 A15 E3 (`487d4449…` L43–44) is "binding": "An outer-row failure would be TESTED-NEGATIVE for exactly this". This text is what turns "outer-row failure" into a rule (L209). Under NOT_READ, whether A15 E3 fired would be decided by hand, after the targets are opened.

**R3. "M-12 makes the classifier's tables the report." Fails.**
- ROOT_ITEMS L234: "Root runs A on the real score, and A's tables are the report's tables." That is a recommendation, and it neither defines nor forbids NOT_READ.
- NOT_READ is a root declaration, made outside the classifier. Even if the tables were published, a NOT_READ classification is not the registered reading, which is against "Every outcome registers" (L25).

**R4. "The C-P gap-filler settles it." Fails.**
- C-P L30: "Where this text is silent, the reading less favourable to the model as registered is chosen."
- The text is not silent here: it grants NOT_READ.
- Which reading is "less favourable" depends on whether E3 is TESTED-NEGATIVE. So the gap-filler cannot settle the clause before target access.

**R5. "A48 already forbids it." This supports the finding instead.**
- The prereg pins the whole A48 section. I recomputed it from the current V005 bytes: L30–64, `526cfceacade31d16dc4f5c7fd023573515898692d4f40d22bfebc9216008ee6`, equal to PREREG §11 L569.
- The section's governing principle (V005 L34) includes: "A failure reading that does not rest on an unresolved or flagged input is still read, because its next step matters even when nothing is adopted."
- The prereg imports only the gap-filler from it (C-P L30; §11 L569, "the governing principle: where the text is silent, the stricter reading"). §1.1 L132 contradicts the sentence it leaves out.
- **Program usage.** In A48, NOT_READ is a registered outcome with listed triggers, and values stay reportable. Ruling 18 (V005 L55): "'No T-test is read' applies to NO_RUN, INCOMPLETE and NUMERICS_UNCERTIFIED/NON_LAPSE_TAIL_MATERIAL. T values may be reported descriptively, labelled 'not read'." Ruling 10 (L48) has the same shape. r2 uses the word as an untriggered root option.

**R6. "C-9 does not scope NOT_READ, so there is no C-9/§1.1 conflict." A wording correction only.**
- The row's risk column is "Root discretion after a stop condition". Its closure ("Afterwards, only … NOT_READ") can be read as the same grant as §1.1.
- On that reading, C-9 lists as closed a risk that the grant itself leaves open: a post-target veto. It is not in the residual-risk rows (L500–501).
- The finding should say "C-9 calls the risk closed while §1.1 leaves an unconditioned NOT_READ". It need not depend on C-9 scoping the clause.

**R7. "Already covered by A98 or 0619." Fails.**
- V005 A98.2 (L956–961) and 0619 (`238858d1…`) cover only the undefined-sign defect and Codex2's late-seal-fallback should-fix.
- Neither Codex2 0490 (`3a922168…`) nor REVIEW_CX2V001 (`7e3b6211…`) nor FINDINGS_CX2V001 (`d9228c31…`) mentions the post-target clause. In those files, NOT_READ appears only in Codex2's own fix for the fallback.
- The rehearsal rough edges (`19807bb3…`) do not raise it either. So r3 must carry R2B-02 explicitly.

**R8. "The 'regression' claim is wrong." Fails; the claim is accurate.**
- **Round 1.** Round-1 r2 (`6437ea33…`) L93: "Root then rules before any reading is reported. The score stands as computed." That ruling was conditioned on a fail-closed stop, but its content was unconstrained.
- **Round 2.** The round-2 wording follows round-1 L-C13's proposed fix almost verbatim (`checks/consistency/REVIEW.md` L321, `a586fb87…`): "After the targets are opened, root may only correct a field map, with no value changing, or declare the classification NOT_READ." That proposal assumed the post-stop context. The rewrite kept the limited content and dropped the trigger.
- So "replaced an unconstrained ruling with an unconditioned escape" is exact. The defect entered by transcribing a round-1 lens fix without its context.

## 3. Reproduction (synthetic only; fenced; no module import)

- **Tool and output.** `tools/stop_inputs_target_independence_vnd2.py` (`2fe34119…`) writes `STOP_INPUTS_TARGET_INDEPENDENCE_VND2.json` (`26021cec…`).
- **Method.**
  - It checks the v003g module sha (`48a1e48a…`), then extracts five pure helpers with `ast`: `_median`, `_ladder_row`, `_score_members`, `_band_rows` and `_pointwise_envelope`. Decorators are dropped, and the module is never imported.
  - It then runs the helpers on three synthetic members against three synthetic target sets: all HIT; every OUTER row 10σ low; and the same with one σ of 5e-324, which gives NON_FINITE_SIGMA_RATIO.
  - The ids are SYN-Q01–SYN-Q43, with predictions 1000 + 10j km/s and σ = 2 km/s, deliberately implausible.
  - An audit hook allowed only the module read and the output write. **0 fence events.**
- **Result.**
  - **The stop inputs are byte-identical across all three target sets** (one sha, `5266fd5c…`): the reference-row statuses (41 VALID, 2 INVALID), the ids in order, the row key set (15 keys, including `sigma_ratio`, which is null under NON_FINITE_SIGMA_RATIO), and the envelope label.
  - **The E3 value differs:** NOT_NEGATIVE_AT_OUTER (M = 0 of N_v = 8), against TESTED-NEGATIVE (M = 8 of 8).
- **Reading.**
  - In the v003g `score_after_freeze` path, every branch that shapes the output depends on frozen fields only (L4218–4303: freeze status, coordinate mode, alternative statuses).
  - So a stop check that passes before targets cannot newly fail after them. The r2 NOT_READ is therefore available exactly when, and only when, the outcome is known.

## 4. Severity: SHOULD_FIX is right

- **Not a NOTE.** The clause is a post-target, outcome-dependent veto over the one binding reading: A15 E3, through OUTER_FAILURE and §5.3. It contradicts C-P L25 and §5.3 L357, and the pinned A48 principle. C-9 claims the risk is closed. The prereg exists to remove exactly this kind of choice.
- **Not BLOCKING.** Using the veto would be a public root act, and the freeze headline survives it (I-5). Nothing is mis-computed. A one-clause amendment closes it, and r3 is already ordered (0619), so it is fixed before any seal.
- **Consistent with round 1.** Round 1 rated the matching post-target-ruling defects SHOULD_FIX: L-C13 and B-5.

## 5. Does the proposed fix work? The direction is right; four gaps

The proposal reads: "Allow NOT_READ after target access only if a §1.1 stop, re-run on the real score, fires. The classifier output is still computed and published, labelled NOT_READ with the stop reason, and the E3 line is printed. A field-map correction must leave every target-free output field byte-identical and is pinned with its diff."

**F1. "Allow … only if" keeps a choice.** When the trigger fires, root still chooses between a field-map correction, after which the classification is read, and NOT_READ. That choice is made with the targets open. The response must be fixed in advance.

**F2. "Still computed … and the E3 line is printed" cannot always be met, and is unsafe when it can.**
- For the stop "a field named here is missing", the outputs that need that field cannot be computed.
- For the ids-order and zone-table stops, a printed E3 value would rest on a defective input. A48 L34 reads only failure readings that do not.
- The reverse case also matters. A stop that touches only the envelope label affects NEAR alone. Under B-5's "affected rows" scoping and A48, E3 should then still be **read**, not just printed under a NOT_READ label.

**F3. The field-map test does not bind the fields that decide tiers.** "Every target-free output field byte-identical" constrains ids, zones, R_q and flags. A remap of `within_error` or `sigma_ratio` would pass it and change every tier. The test has to check outputs that depend on targets, using a synthetic set with both hits and misses.

**F4. One post-target trigger is missing.**
- ROOT_ITEMS M-6 item 5 (L130) says: "At the score step, root verifies the sealed shas from bytes before the classifier runs."
- RUNBOOK_V001 (`9557b5aa…`) has no classifier step. Its step 9 (L26) is `score_after_freeze`. So, as ordered, this sha check runs after target access.
- If it fails, the proposed fix gives no registered response: it forbids NOT_READ, and the sealed classifier cannot be used.

**Better fix (r3):**
1. **Triggers (§1.1).** "NOT_READ is a registered outcome, never a root option. Its only triggers are:
   - (a) a §1.1 stop condition fires when the sealed classifier re-runs the stop checks on the real score;
   - (b) the M-6 item 5 sha verification fails.

   Item 5 is run before RUNBOOK step 9 (before target access) and recorded in the score entry."
2. **What NOT_READ covers.**
   - "The freeze headline (I-5) is reported as computed.
   - Every output whose inputs the defect does not touch is computed, read and reported as registered. In particular, the E3 line is read whenever the OUTER rows, the ids, the zone table and `score_status`, `within_error` and `sigma_ratio` are intact (A48: a failure reading that does not rest on an unresolved or flagged input is still read).
   - Each output that depends on the defective input reads NOT_READ (<stop code>). Any value that can still be computed is given descriptively, labelled 'not read' (A48 ruling 18).
   - The E3 line is always printed, with one of its three values or NOT_READ (<stop code>)."
3. **Field maps after target access.**
   - "A field map may only rename keys. It is **required**, not optional, when a key-name stop fires and a renaming exists that reproduces, byte for byte, the sealed classifier's outputs on the sealed M-12 agreement suite expressed in the real score's format. Otherwise NOT_READ applies.
   - The map and the suite-replay record are pinned in a root entry before the classifier's output on the real score is read.
   - No other post-target action exists."
4. **Consequential edits.**
   - C-9 L496 becomes: "Root discretion after target access | None: NOT_READ has fixed target-free triggers and a defined scope; a field map is required and verified by suite replay (§1.1)."
   - State the triggers in CSM L102 (B-5) and L122 (L-C13).
   - Add the trigger cases to the M-12 agreement suite: one stop that touches only NEAR (E3 still read), and one that touches the OUTER rows (E3 reads NOT_READ).

This fix adds no new choice after target access. In the v003g path its triggers are effectively unreachable, which is what the seal needs.

## 6. Adjacent (outside R2B-02; not verified further)

I-7 L91–92 classifies "the **first** successful `score_after_freeze`", and calls "any later … re-score after target access" EXPLORATORY. Suppose a first call refuses after the target rows were passed (for example, `target_rows rejected`; v003g L4198–4217). The text does not say whether a corrected second call is then classified or is EXPLORATORY. The fix round may want to settle this together with the NOT_READ triggers.

## 7. What was read, and what was not

- **Object.** All 10 round-2 files (hash check), with PREREG, ROOT_ITEMS and CSM read in full. Round-1 r2 PREREG (`6437ea33…`, L70–125). The round-1 reviews `checks/consistency/REVIEW.md` (L300–429), `checks/targetfree/REVIEW.md` (L148–167), and a grep of all six `checks/verify_*/VERIFY.md`, none of which discuss L-C13.
- **Sources.**
  - V005 open, read at 20:33:39Z: `7f552858be77888ff1e3abc4d490e7e88ca5a16374bad84ad8ae043686b39fa2` (A48 L30–64; A98 L948–961). Every V005 line number in this file refers to this read.
  - V005 re-read at 20:43:20Z: `5a996e97d633cc11a4cb255fe8ba1cdf746d93367621c004aca29382affb6a26`. The only new entry is A101, at L890 (B2 record of record; registry V008), which touches neither NOT_READ nor the post-target clause. The A48 section is still L30–64 and still `526cfcea…`. A98 has moved to L958–970.
  - The object re-checked at 20:43:20Z: all 10 files still match HASHES_R2.txt.
  - V004 frozen `487d4449…` (A15, L26–50). V003 `5bef6552…` (hash only).
  - Freeze v003g: module `48a1e48a…` (L2072–2091, L4011–4303); slots `d3859b42…` (hash only); RUNBOOK `9557b5aa…`.
  - Dispatches 0585, 0606, 0592 and 0619. Codex2 0490 and its review files. The Codex2 prep checklist (`020ef3f1…`). Codex1 0058 (`fc5af831…`, hash only) and the rehearsal record (`19807bb3…`, rough edges).
- **Not read.** No NGC3198 target, observed velocity, rotmod/Vobs/MassModels/SPARC path, runs_ext path or UVT_* item. No recursive content search. Nothing was launched, and no project calculation was run.

## Files in this folder

- PARTIAL.md, VERIFY.md (this file), REVIEW.md (summary), HASHES.txt;
- STOP_INPUTS_TARGET_INDEPENDENCE_VND2.json;
- tools/stop_inputs_target_independence_vnd2.py.
