# VERIFY — adversarial verification of fidelity finding A-01 (miss-reading prereg r2, round 1)

Verifier: a helper of lane Claude4, `verify_fidelity_1`, one of the dispatch-0592 checks of 0585. Refute by default.
- Nothing in the object was edited. No NGC3198 target, observed velocity or data table was opened. Nothing was launched, and no project calculation was run.
- Every sha256 below comes from bytes, and every time from `date -u`. Started 2026-10-18T19:18:45Z. Report written 2026-10-18T19:28:47Z.

**Verdict: NOT REFUTED. A-01 is CONFIRMED, at severity BLOCKING.**
- The defect is real. [C-I6] mis-cites 0512, and it contradicts its own preceding bullet and A66.2/0550. The contradiction sits in the clause that decides whether the document applies, and the outcome that has actually occurred triggers it.
- **The fix is right in substance but not sufficient as written** (F1–F3 in §5).
  - It ties applicability to the gate of "the registered compare", and no compare record has been pinned. Several compare records with different gates sit side by side.
  - Its wording could be read as "gate OPEN means route A/B runs".

## 1. Bytes verified

**The object.** All 10 files match `HASHES_R2.txt` and the task list:

| file | sha256 |
|---|---|
| PREREG_MISS_READING_R2.md | `6437ea33432f50971eef81e549a8e5789d0bd892efaf2d0f423ce4c933f30143` |
| CLAUSE_SOURCE_MAP_R2.md | `b105b55d7f80c5868d936f577ce81e92992999440f5cd85a06decbc62650d24b` |
| ROOT_ITEMS_R2.md | `1d7af792f9b115fc7882254b694d82299217c3ab846d7d26d591f45a5c5eaf7f` |
| NUMBER_PROVENANCE_R2.json | `c81b5a7a579476480a085681ebd6eb8aa445e38b6a7abe2284dba3716b0c2832` |
| TARGET_FREE_CHECK_R2.json | `aab683236116bc3562df86f3b9542a54eec3446c44a8f0e5569ff2b305d2180b` |
| TARGET_FREE_MUTATION_TEST_R2.json | `2a8202b823beb5cd0bc03c9e1e2b0377d9de59410a698c8d185f39739d66bc41` |
| INDEX_R2.md | `6c1919a900d56fcb7438015db6a6be1d1d28fd07ee17a9bee6e1e007c0045b9b` |
| tools/check_target_free_c4v001.py | `85457a43c654aa13b49fa528b786a615e99a51eaa29b4ba42687a2c0f3396cc7` |
| tools/test_check_target_free_c4v001.py | `fc403648a57b3f0ee30b164e2cde48e3c1889bfee33938c8b23a93c1fd88ea11` |
| tools/make_miss_reading_c4v002.py | `8c0d9fc2fb962f3e72de9e6a7a03cc11aa38efccd59981713fbcc0008b32576a` |

**Sources read:**

| source | sha256 |
|---|---|
| FROM_CODEX/0512 (N-test outcome names) | `adac97bbf1884f932b1b046f2d1f04b404a15d019ea840f000b34b58ad45d190` |
| FROM_CODEX/0550 (A66 consequence; the gate field) | `5c686ae8fd82cea995fcdd1ed5bff2d0d688514c45582871cb2b97f231b8b457` |
| FROM_CODEX/0585 (the r2 dispatch) | `9003633293ff1db7d5153cabc338fd058cc199d834976b05543b7603b9433abd` |
| FROM_CODEX/0603 (the rehearsal dispatch) | `e4e94fa616457a2df662550febd528ffef46ae203fdec94b0054cb8b5d221a16` |
| FROM_CODEX/0606 (the rough edges) | `dbb80c77cb085626303a9ce4e8d48e761dfd8525eece32022154e7e69881e28e` |
| FROM_CODEX/0607–0611, checked for any later N-test or prereg ruling (none found; 0610 only queues a review) | 0607 `54f4dd48…`, 0608 `a5a2854a…`, 0609 `35a1848d…`, 0610 `29e72c1c…`, 0611 `9455bc03…` |
| V005 addendum (open) | `50fe0f1c0f3d9d4f9acc8a44677b7d37b2b7c96e682ee2f0c2c270cb8c0a7477` |
| V001 | `6aecf0cb340b28f911d0e71c1ef3d6aede5e495309cdd40ee44ae9e49e785345` |
| `claude_artifacts/ngc_ntest_eval_cx/out/K32_COMPARE_COMPLETE_V001.json` (only its outcome, gate and reason fields were extracted) | `6f095f64a1f1acc2ad2910af12f645e18acdf16fb62bfd936386a61c47ef30e9` |
| `…/out/K16_COMPARE_COMPLETE_V001.json` (same fields only) | `8ff95be328e23aa811a93c61bb65ed16d4a1f1a92ac6f9c8064475b8008e4dc9` |
| `…/out/K32_COMPARE_PARTIAL_V001.json` and `V005` (same fields only) | V001 `3ab87f21…`, V005 `8a330b81…` |
| `…/ngc_ntest_eval_cx/ntests_compare_k32_cxv003.py` (the gate producer; equals the record's `producer.sha256`) | `283193be92330805733f865943b01624f1dfb28f22177d18dc06370d2829fa2d` |
| `…/ngc_ntest_eval_cx/ntests_core_k32_cxv001.py` (the core it imports) | `0182cdc6cd1aa4f965d32f4003433690e961c04b94152a641d6eed491b8815b1` |
| `claude_artifacts/steps6_7_rehearsal_cx1/REHEARSAL_COMPLETE_V001.json` | `19807bb3bca7279e6af71fee40dfefa4ba474ebcdc1289b06dc4598394c35d36` |
| the lens's V005 snapshot `checks/fidelity/V005_SNAPSHOT_READ.md` | `bba6daf53ad07d691d09648801bc113b61718e4be0568a6d870cdb87982d1a17` |

**Notes on V005:**
- It was read at 19:20:12Z and re-hashed unchanged at 19:28:35Z. A copy is kept in this folder as `V005_SNAPSHOT_READ_V1.md`, with the same sha.
- **V005 line numbers below refer to `50fe0f1c`**, unless another version is named.
- I recomputed the r2 §11 section pins for A64, A65 and A66 under r2's extraction rule, and all three MATCH: A64 `9984d581…`, A65 `290eac4a…`, A66 `34469531…`. So the defect is not caused by V005 drifting: the cited sections are byte-identical to what r2 pinned.
- **Final read at 19:31:48Z:** `6145a1f92cbace8d36f86a7c15be4d79ee6992717a5c57438cdd62045e070c7c`, kept as `V005_SNAPSHOT_READ_V2.md`.
  - The only change from `50fe0f1c` is a new entry, **A93** ("NGC cx3r007 accepted (Claude4 0092)", 19:31Z), inserted above A92. It touches no N-test, gate or I-6 matter.
  - The A64, A65 and A66 pins still MATCH.
  - In these bytes the cited lines move to L946 (A90 gate) and L1275 (0512 log). L634 is unchanged.

## 2. Q1: Is the quoted text there, and is it defective?

**The quote is there, verbatim.**
- PREREG_MISS_READING_R2.md [C-I6]:
  - L54: "**N-test outcome.** It is decided by the registered compare (A66.1): N_PASS, or N_FAIL_N1 confined to TRUNCATION_SHAPE rings (A66.2)."
  - L55: "A failure of N0, NQ, N2 or N3′, or an N1 failure on a ring that is not TRUNCATION_SHAPE, blocks NGC route A/B (A66.3)."
  - L56: "Under the 0512 ruling logged in V005, only N_PASS is an input to route A/B. So any other outcome, such as N_INCOMPLETE or N_NO_RUN, also gives no route-A/B run."
  - L57: "With no route-A/B run there is no score, and this document is not applied."
- CLAUSE_SOURCE_MAP_R2.md L21, row C-I6: "(N_PASS is the only input to route A/B)".
- NUMBER_PROVENANCE_R2.json L472–L477, key "0512": "the 0512 N-test ruling (N_PASS is the only input to route A/B), logged in V005 after the A65 heading".

**The text is defective, for five reasons:**
1. **It mis-cites 0512.**
   - 0512 L16 reads: "`N_PASS` licenses nothing by itself. It is an input to the NGC route-A/B step."
   - V005 L1269, which logs 0512, reads: "N_PASS is only an input to NGC route A/B."
   - r2 L56 reads: "only N_PASS is an input to route A/B".
   - The word "only" has moved from the predicate ("merely an input": N_PASS is not sufficient) to the subject ("N_PASS and nothing else": an exclusivity claim). Neither 0512 nor its V005 log makes the exclusivity claim.
2. **It is false on r2's own citations.**
   - A66.2 (V005 L634) reads: "**N_FAIL_N1 confined to TRUNCATION_SHAPE rings does not block NGC route A/B.**"
   - 0550 L10 says the same.
   - r2 cites A66.2 itself, two lines earlier (L54).
3. **The invariant contradicts itself.**
   - L54 admits N_FAIL_N1 confined to TRUNCATION_SHAPE rings.
   - L56 says that every outcome other than N_PASS "gives no route-A/B run".
   - The words "also" and "such as N_INCOMPLETE or N_NO_RUN" hint that the author meant only the outcomes not covered by L54–L55. The literal text, "only N_PASS", is unambiguous all the same.
4. **The contradiction reaches every reading and the document's own applicability.**
   - [C-P] L18–L20 reads: "**Every reading is conditional on:** … the registered NGC numerics of I-6."
   - L57 makes "no route-A/B run" disapply the document.
5. **The case the literal L56 excludes is the case that has occurred.**
   - The K32 compare `6f095f64` shows:
     - `outcome` N_FAIL_N1;
     - `failures` ["N_FAIL_N1"];
     - `tests_read` true;
     - `production_K_big` 32;
     - `n_route_ab_gate` OPEN;
     - `n_route_ab_reason_codes` ["TRUNCATION_SHAPE_RESIDUAL_ONLY_A66"].
   - A90 (V005 L937–L940) reads: "NGC K32 N-tests (Codex1 0056): N_FAIL_N1, tests_read = true" and "Under A66 the route A/B gate reads **OPEN**, for the sole reason TRUNCATION_SHAPE_RESIDUAL_ONLY_A66."

**Where the defect came from.**
- r2 introduced it. V001 has no N-test or route-A/B wording at all (grep of V001 is empty), and the map classes C-I6 as NEW.
- Both A66 (about 14:55Z) and 0550 (about 14:58Z) predate the r2 assembly. INDEX_R2 L18 gives V005 at assembly as `17cb4fd4…`, last entry A89.
- A90 post-dates the assembly, but the defect does not depend on A90. It exists against A66.2 alone.
- 0550 is cited nowhere in r2. A grep for "0550" and "n_route_ab" over the prereg, the map, the root items and the provenance file is empty.

**Independent corroboration.** Codex1's rehearsal (`19807bb3`; its input pin is this very r2, `6437ea33…`) gives rough edge "I6": "I6 mentions A66 shape-only allowance but later says only N_PASS under0512. Clarify precedence before score." Dispatch 0606 item 6 reads: "I6: the A66 versus 0512 wording."

## 3. Refutation attempts (all failed)

| attempt | why it fails |
|---|---|
| R-a. The author's intent is recoverable from "also" and the examples. | A sealed prereg must not need a charitable reading of its own applicability condition. "only N_PASS is an input" is explicit, and it is attributed to a root ruling that does not say it. |
| R-b. L57's trigger is factual: if route A/B actually runs, "no route-A/B run" is false and the document applies. | L56 registers that N_FAIL_N1 "gives no route-A/B run". Under [C-P], a run fed by N_FAIL_N1 then lies outside what the sealed text says can feed route A/B. Whether the readings apply becomes a question someone has to rule on after the score, which is exactly the steering surface §9 exists to close. It can be argued in either direction once the result is known. |
| R-c. The A48 principle resolves the conflict toward the stricter reading. | r2 imports A48 only for silence. L21 reads: "Where this text is silent, the reading less favourable …". A48's own words (V005 L34) are also about silence: "Where the text is silent, the stricter-on-adoption reading is chosen." Here the text is contradictory, not silent. Even if A48 were stretched to cover it, root would have to rule after the score. |
| R-d. r2 has some other precedence rule. | It has none. A grep of the three text files for precedence, govern, prevail, conflict, contradict and supersed finds only PREREG L4 (the V001-supersession line) and the A48 "governing principle" lines (L21 and L421). ROOT_ITEMS M-6 (L112–L125) handles later V006 entries, not conflicts with entries already cited. |
| R-e. Under 0512 alone, N_PASS was effectively the only admissible outcome, so r2 is just stating pre-A66 law. | In substance that is close: 0512 gives no route for a failure. But r2 states it after A66 and in the same invariant that cites A66.2, so the statement is false as of the text's own sources. And it is still attributed to 0512 as "only N_PASS", which 0512 does not say. |
| R-f. V005 has drifted, so the cited sections may have changed. | The A64, A65 and A66 section pins all MATCH in `50fe0f1c` (§1). The 0512 log at L1269 lies inside the A65 section, which runs from L1239 to the end of the file, and that section is pinned unchanged. |
| R-g. A later dispatch or entry has changed the gate rule. | 0607–0611 contain no N-test, gate or I-6 ruling; 0610 L7 only queues a Codex2 review of r2. A93 (19:31Z) accepts cx3r007 and names the step-5 launch registry, with no gate or I-6 change. |

## 4. Q2–Q3: Does the evidence say what the finding claims, and is the severity right?

**Every evidence item checks out:**

| finding's evidence | verified | location in `50fe0f1c` |
|---|---|---|
| 0512 (`adac97bb`) item 2: "N_PASS licenses nothing by itself. It is an input to the NGC route-A/B step." | yes (the source puts N_PASS in backticks) | 0512 L16, inside item 2 (L10–L16) |
| V005 L1245, A65 trailing block: "N_PASS is only an input to NGC route A/B." | yes, as content | L1269 here. It is L1245 in `0753f2d8`, the lens's reference version, and L1231 in `bba6daf5` |
| V005 L634, A66.2 | yes | L634, stable across all three versions |
| 0550 (`5c686ae8`): "Add a field n_route_ab_gate … Do not change the 0512 outcome names." | yes. The elided words are "to the compare output". | 0550 L14 |
| V005 L916, A90: "the route A/B gate reads OPEN, for the sole reason TRUNCATION_SHAPE_RESIDUAL_ONLY_A66." | yes, as content | L940 here. It is L916 in `0753f2d8` and L902 in `bba6daf5` |
| K32 compare `6f095f64`: N_FAIL_N1, gate OPEN | yes, with reason TRUNCATION_SHAPE_RESIDUAL_ONLY_A66 and tests_read true | the record's fields |
| rehearsal rough edge "I6" and 0606 item 6 | yes. The rehearsal frames it as "clarify precedence", which is softer than "inverts", but it is the same conflict. | `19807bb3` rough_edges id I6; 0606 L11 |

**Accuracy nits.** None of these changes the verdict.
- **N-1.** "This inverts 0512" is loose. More exactly, it transposes the scope of "only": a statement that N_PASS is not sufficient becomes a claim that N_PASS is exclusive, that is, necessary.
- **N-2.** "The bullet just before it" is imprecise. The explicit allowance is in the parent bullet, L54. The immediately preceding sibling, L55, implies it only by exclusion.
- **N-3.** The finding gives V005 line numbers without naming the V005 version, and the open file shifts as root inserts entries (A92 was inserted above A91). Cite the V005 sha (`0753f2d8`) or the section instead: A90, third bullet under "NGC K32 N-tests"; A65 trailing "Lanes" block, third bullet.

**Severity: BLOCKING, confirmed.**
- **Wrong to seal.** The sealed text would mis-state a root ruling (0512), in a binding invariant, against A66.2 and 0550.
- **Unsafe to seal.** The contradiction sits in the applicability condition that every reading inherits ([C-P]). The realized outcome triggers it: N_FAIL_N1 with the gate OPEN.
- **No repair after the seal.** Once sealed, the conflict can only be settled by a root ruling made after the score is known. Preventing such rulings is the reason for sealing before targets open.
- **SHOULD_FIX was considered and rejected.** The defect is not cosmetic. It is the document's own disapplication route, on the live case.

## 5. Q4: Would the proposed fix work without creating a new problem?

**The core replacement is correct.** It is consistent with the gate producer of record, `ntests_compare_k32_cxv003.py` (`283193be…`):
- The gate defaults to BLOCKED (L16).
- When the tests are not read, it stays BLOCKED with `N_TESTS_NOT_ADMITTED_OR_INCOMPLETE` (L18–L19). Both N_INCOMPLETE and N_NO_RUN leave `tests_read` false: core L108–L109 and L112, plus producer L29–L30 and L48.
- It reads OPEN only if N0, NQ, N2 and N3′ pass, there is no N1 failure on a non-TRUNCATION_SHAPE ring, no reference-check failure and no unexplained N1 failure (L28 and L32–L37).
- The OPEN reason is `ALL_BLOCKING_N_TESTS_PASS` or `TRUNCATION_SHAPE_RESIDUAL_ONLY_A66`.
- N_PASS implies that every reference spread is below θ (core L65), so N_PASS always reads OPEN.
- So the fix's three factual statements hold for this producer: OPEN for N_PASS, OPEN for N_FAIL_N1 confined to TRUNCATION_SHAPE rings, and BLOCKED for every other outcome.

**It is not sufficient as written:**
- **F1 (required): pin the record of record at the seal, not only in D-4 at score time.**
  - D-4 is "filled at score time from the slotted records" (PREREG L325). "Slotted" applies to the certificates (A81 RI-23, V005 L1083), not to the compare.
  - `ngc_ntest_eval_cx/out/` holds several compare records:
    - `K16_COMPARE_COMPLETE_V001.json` (`8ff95be3…`): outcome N_FAIL_N1, with **no `n_route_ab_gate` field**;
    - `K32_COMPARE_PARTIAL_V001` to `V005`: N_INCOMPLETE, gate BLOCKED;
    - `K32_COMPARE_COMPLETE_V001.json` (`6f095f64…`): N_FAIL_N1, gate OPEN.
  - The fix makes applicability turn on the gate field of "the registered compare". Someone could then point to the K16 record, which has no gate field and so is not OPEN, and run the same disapplication argument. A64.3 ("N1 is read only on the production-K_big records") and A90 weigh against that, but no root entry pins a compare sha.
  - Write into I-6 now, as a fact at writing in the same style as D-3: "The NGC N-test record of record is `claude_artifacts/ngc_ntest_eval_cx/out/K32_COMPARE_COMPLETE_V001.json` (`6f095f64…`; producer `ntests_compare_k32_cxv003.py` `283193be…`; Codex1 0056; A90): N_FAIL_N1, `n_route_ab_gate` OPEN, reason TRUNCATION_SHAPE_RESIDUAL_ONLY_A66. A successor replaces it only through a root entry made before any target is opened (for example, after an RI-23 M_s 128 recompute or the A90 LO I1-T ruling), and the seal entry names it."
  - The pin creates no seal-pin cycle, because the compare record does not pin the prereg.
- **F2 (required): the gate is necessary, not sufficient.**
  - The fix's "That happens for N_PASS, or for N_FAIL_N1 …" can be read as "route A/B runs" rather than "the gate is OPEN".
  - Say instead: "The gate reads OPEN only for N_PASS (reason ALL_BLOCKING_N_TESTS_PASS) or for N_FAIL_N1 confined to TRUNCATION_SHAPE rings (reason TRUNCATION_SHAPE_RESIDUAL_ONLY_A66)."
  - Add: "The gate is not launch authorization." That is the record's own `n_route_ab_ruling`: "this gate is not launch authorization". Root's other step-5 conditions are separate and recorded in D-4. They include:
    - the A90 LO I1-T ruling (V005 L942: "it is ruled before any NGC route A/B launch");
    - A93's launch registry `cd30429c`, whose three should-fix items must be closed "before any step-5 launch" (V005 `6145a1f9`, A93).

    This overlaps the lens's A-06.
- **F3 (required): attribute exactly, or the fix repeats A-01's class of defect.**
  - 0550 created the field and listed the blocking failures, and A66.2–A66.3 rule them.
  - BLOCKED for N_INCOMPLETE and N_NO_RUN is the producer's behaviour (L18–L19). It agrees with 0512's closing line: "Unknown or missing input reads N_INCOMPLETE, never a pass." Cite it that way.
  - Do not attribute "route A/B runs only when the gate is OPEN" to 0550 alone.
- **F4 (optional hardening): remove the disapplication route by construction.**
  - Replace L57 with: "If an NGC route-A/B score exists, this document is applied in full; no clause of I-6 disapplies it. If the record of record's gate did not read OPEN, every pattern and reading carries the label PROVISIONAL (N_GATE_NOT_OPEN), as I-7 does for FREEZE_INCOMPLETE."
  - This fits [C-P] "Every outcome registers" and A48's "A failure reading … is still read" (V005 L34).
- **F5 (housekeeping):**
  - T4 needs a provenance entry for each new bare numeric token: "0550", and "0603" or "0606" if they are cited.
  - Update map row C-I6 and the 0585-coverage row for A64/A66 so that both cite 0550 and A90.
  - Pin 0512 (`adac97bb…`) and 0550 (`5c686ae8…`) in §11.
  - The generator copies the texts from the draft folder, so it needs no change.

## 6. Result

| field | value |
|---|---|
| id | A-01 |
| refuted | no |
| severity | BLOCKING |
| fix sufficient as written | no. The core is correct; add F1–F3. F4 and F5 are recommended. |
