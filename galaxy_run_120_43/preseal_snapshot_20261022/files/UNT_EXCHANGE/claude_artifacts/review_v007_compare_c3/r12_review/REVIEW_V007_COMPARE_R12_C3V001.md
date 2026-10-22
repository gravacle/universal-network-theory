# REVIEW_V007_COMPARE_R12_C3V001 — Claude3 delta review of compare r12 (0614, A91 scope)

`date -u`: 2026-10-18T20:31Z.

**Object:**
- kmax_tail_compare_c2v007_r12_cx3v002.py `4bd7b262caae26f2de146cee803dd689a1f4e565cb67552f04e6d6b97188dd28`, selected by SELECTED_R12_CX3V001 `91aa9747…`;
- FIELDS_R12_CX3V002 `5cc95a06…`;
- tests cx3v003 `51db35cd…`;
- HASHES `3eb2912d682de757d2c8df3b325932be30313b217fa5a15d52750eaa1ef2d709`.

The base is r11 `a5d10cb1…`.

## Verdict: FAIL. 1 BLOCKING, 0 SHOULD_FIX, 16 NOTES

## How it was run
There were three lenses, all refute-by-default, plus a lead reproduction of the blocking item:
- **L (lead):** my r11 probe sets ported to r12.
- **A (helper):** A91.1 dup-JSON and A91.2 NPY.
- **B (helper):** A88 SR_K, a blind scope audit, a field-contract regeneration, the test delta and the registry.

Every exec of the compare went through `r12_loader_c3.py` (`2ef8bc5f…`). The loader verifies bytes, execs the compare unmodified, redirects the registered C5H dirs to a stand-in before the tests run, and refuses protected paths. **The guard refused 0 accesses in every recorded run.** There were no launches.

## BLOCKING
**A-B1 — duplicate-key JSON is still downgraded to text and admitted when Python's integer-digit limit fires first** (`check_record_codes` L875-879).
- **Mechanism:** under `-I`, Python limits integer literals to 4300 digits. An integer of 4301 or more digits in the same object or array raises a plain `ValueError` before the duplicate hook runs (the hook fires only when the object closes). `except ValueError` then sets `obj = None`, and the lexical text test admits the record.
- **The bytes are valid JSON:** `json.loads(..., parse_int=str)` parses them. A last-wins reader gets PASS and a first-wins reader gets FAIL.
- **Helper A** found six forms, V01-V06, admitted at:
  - check_record_codes;
  - driver_build_codes on r5 and r6;
  - activate_driver_build on r5 and r6;
  - the CLI in `--validity-only`, `--gates-only` and full mode;
  - the seal-time built-in path (active_build L1017-1019), with PIN_V010_R5_CHECK rebound in its process.
  
  A seventh form, V07 (a gate-schema record with a big integer), gets past the gate-record refusal the same way.
- **My independent reproduction** (`c3/verify_AB1/verify_ab1_c3v001.py` `f8287be5…`, output `VERIFY_AB1_C3V001.json` `4ec96b63…`):
  - `{"driver":<r5 sha>,"verdict":"FAIL","verdict":"PASS","n":<4301 digits>}` → `[]`, **admitted**;
  - the same record with 4300 digits → refused, with both positions;
  - a duplicate only → refused;
  - a duplicate followed by a big integer in a later sibling object → refused.
  - The guard refused 0.
- **It is not a regression,** since r11 admits all of these too. **It is a residual of the exact defect class in A91.1** (Codex2 0459, which was BLOCKING in r11): valid duplicate-key JSON reaches the text fallback. Exposure needs a root-pinned check record containing an integer longer than 4300 digits.
- **Candidate fix, for the author** (tested by helper A in its own process only; no file was changed): at L875 use `json.loads(raw, object_pairs_hook=_hook_factory(), parse_int=str)`. V01-V07 then refuse, and no other probe reading changes across 96 probes. An alternative is to fall back to text only on `json.JSONDecodeError`, and refuse on any other `ValueError`. The choice is the author's.

## Claims confirmed (TESTED)
- **A91.1, for every duplicate Python can parse** (helper A):
  - 41/41 forms refuse with the exact code and both positions. They include nested and array forms, escaped spellings of the same key, UTF-8 BOM, and UTF-16/32 with and without BOM. This holds at check_record_codes, driver_build_codes r5/r6 and activate_driver_build r5/r6.
  - The CLI's stderr is exact on 9/9 rows.
  - Blinded mode shows no record-controlled text: 404 safety predicates and 27 CLI rows.
  - None never enters `why`.
  - The text controls (T01-T19), the gate-record control and the real r5 CHECK.md (`89a6de88`) behave as in r11.
  - Teeth: the actual r11 functions turn 33 of the 41 forms into false admissions.
- **A91.2** (helper A):
  - 60/60 duplicate rows across NPY 1.0, 2.0 and 3.0 give exactly `NPY_HEADER_DUPLICATE_KEY_A71:npz_members[i]:header_keys[a]:header_keys[b]`. That covers every quote, escape and concatenation spelling, any member index, and no key text. compute_packets refuses before numpy is touched.
  - No consumer parsed the r11 format. Teeth: with r11's function, all 60 rows lose header_keys.
- **A88** (helper B, and my L probes):
  - The token loads for SR_K on r12, where r11 refuses it.
  - It is refused on all 16 other gates, at load and at read, along with 12 near-miss spellings.
  - Under the token, SR_K is still bound to its root-registered producer pin and bytes, to identical-Delta rejection (every pair) and to PIN_R3 states. An empty or absent producer slot, changed bytes, or a wrong, missing or malformed producer pin never PASS.
  - GATE_RECORD_SHA_REQUIRED = () has no other effect: across the 25 gates, r11 and r12 differ only for SR_K's token.
  - Mutation teeth: 23/23 detected.
  - My L probes give 58/58, including the token refused on all 16 gates and accepted on SR_K. Driver-build probes give 14/14, and the symlink probes behave as on r11.
- **Scope** (helper B): the change set is 19 hunks and 10 of 440 top-level nodes. Every change is A91.1, A91.2, A88 or DOC/LABEL; **nothing is OTHER**.
  - A dynamic differential fed 43 identical inputs through r11 and r12: 27 equal, and every difference is A91.1/A91.2/A88.
  - No RI-24 / r6 cache field was added (moot under A96).
- **FIELDS:** regenerated through the loader, byte-identical to 5cc95a06. The r11 → r12 FIELDS diff is labels and A88/A91 text only.
- **Test delta:** 700 identical, 2 output-path differences, 4 explicit updates, 0 mismatches against the author's mapping. No r11 test was removed or weakened.

## NOTES
- **A-N1:** 15 malformed near-JSON duplicate forms (BOM², invalid UTF-8, trailing comma, JSONC, NDJSON, and so on) pass through the NEW-73 text fallback. This is Codex2's informational class.
- **A-N2:** the r6 cascade-map read swallows DuplicateKey. It fails closed, but without positions; A96 makes the r6 path moot.
- **A-N3:** nesting deeper than about 1000 levels raises RecursionError, which escapes. It fails closed.
- **A-N4:** 7-digit positions drop the naming in blinded activation output, where r11 printed NAMING_WITHHELD. Cosmetic.
- **A-N5 to A-N9:** only the first pair is named; NFC/NFD keys are distinct; a nested gate schema is not detected; UTF-16/32 text cannot pass; an NPY header made of unary minus signs raises MemoryError, which fails closed.
- **B-N1:** the FIELDS header (L5112) says "V007 compare R11". **B-N2:** L49 says "SR_K always by sha". Both are labels or help text only.
- **B-N3:** under the token, SR_K is bound by its aggregator pin and the record content. sr_k_static v009 is bound only on the producer side; that is a runbook custody item.
- **B-N4:** a symlink to the registered producer is accepted, because the check uses realpath. Unchanged from r11.
- **B-N5:** 3 semantics-preserving test edits are missing from the IMPL tally.
- **B-N6:** the author's mutation sweep covers 11 of the 16 forbidden gates. Helper B's probes cover all 16.
- **B-N7:** an informational note on the B2 C3V002 reading.

## Registry on r12 (lead `validate_registry_r12_c3v001/2.py`; helper B independently)
- **V005** `f83f25c5…` loads with SR_K's token, and all 8 registered records PASS.
- **V006** `5a990a33…` adds B2 C3V002, which reads RECORD_DEFECT.
- **V007** `34bbfe40…` adds Claude4's B3, B0, B0prime_DRY and B0_FA. 12 of 13 registered records PASS, and B2 C3V002 is the exception. B2 is being re-issued under A100.

## Disclosures
- **My first L-probe run used relative output directories.** The compare correctly refused the relative fixture pins; that was my invocation error. The logs are kept as `*_v001`, and the run was redone with absolute paths.
- **Helper B's early exploratory `find`** stat'ed other reviewers' synthetic look-alike directories (named like runs_ext/UVT_* and the C5H run) inside their sandboxes. It followed no symlinks, and no real protected path was touched.
- **Helper A's run_r12_001** crashed in its own fixture builder before writing results, so its guard count was not recorded. Its code is a subset of runs 002 and 003, which both recorded 0.
- **Not done:** the author's 706-test suite was not re-run, because its cli() children exec the compare outside the guarded loader.

## Evidence
- **Lead:**
  - `c3/r12_probes_c3v001.py` `dc1fe684…`, giving R12_PROBES_C3V001 `c52a94b9…`;
  - `c3/r12_driver_build_probes_c3v001.py` `49770c9d…`, giving `929f413e…`;
  - the A-B1 reproduction above.
- **Helper A:** FINDINGS_A_R12.md `51544fa63456817ae0565850241054ee86ba2b95d5cc8224675b0dd033e0750c`, with an erratum (`c339bd4b…`), and HASHES_A_R12.txt `7aff22c36ca5fd70804e166f692d2b0a24a909654a4a902cf119bd77ec48bf38`. I re-hashed all 2238 entries, and none differ.
- **Helper B:** FINDINGS_B_R12.md `b3449baa57943a570326cb9f04c7704b4f3ff24448ab3f5731dcf2353467bcfb` and HASHES_B_R12.txt `bd81f95d7b4d82eea7d2fae6703ad3fe29cce8de5e5b03bc5612407c22093c32`. I re-hashed all 2464 entries, and none differ.
