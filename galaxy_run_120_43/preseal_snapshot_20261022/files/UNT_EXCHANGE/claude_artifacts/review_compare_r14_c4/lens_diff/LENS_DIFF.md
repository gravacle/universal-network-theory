# LENS_DIFF: compare r14, delta review of record, lens 1 (diff and pins)

- **Reviewer:** a Claude4 helper (lens_diff). Cross-lineage: Codex1 built r14. Dispatch 0651, root entry A114 (V006).
- **Times (`date -u`):** started 2026-10-19T03:20:03Z; written 2026-10-19T03:35:24Z or later.
- **Object:** SELECTED_R14_CX1V001.json `dc74949d1d4f19336661f8ce85e9a85de0176837adad61c7a9585a147f933533`, as dispatched. Its successor SELECTED_R14_CX1V002.json `6b650ececefee673ec3e04849574f9a4b75b977288afd3c9949a4b8d2d3cd49a` (utc 03:19:19Z) is also in r14/, so it is covered too (N1).
- **Severity rule:** A115 was appended to V006 during this review (the file sha went from `ca5d7ae3…` at 03:20Z to `63e7802f…` at 03:35Z; A114's section, lines 120 to 140, now hashes to `21720e08…`). Under A115, only a finding that is reachable from honest pinned producers, or that can change a physics reading, blocks. Everything else is a NOTE.

## Verdict

**0 BLOCKING, 0 SHOULD_FIX, 10 NOTE.**

Every byte of r14 equals r13 except one insertion of 6 bytes, `, 'I4'`, which makes `'I4'` the last element of `GATE_RECORD_AFTER_SEAL_ALLOWED` (L341). The exact inverse gives back r13 `f5adfd11`. All 114 publication pins match their bytes. No line number moves anywhere, so every C-08 row is valid for both r13 and r14. The notes below concern prose, test names and publication hygiene. None of them changes a gate verdict.

## 0. Shas, all from bytes (TESTED)

Every sha the dispatch gives matches its bytes. These were checked at 03:20Z, and the core files again at 03:34:56Z:

- SELECTED V001 `dc74949d…`
- r14 source `f3f9ba7e…` (410439 bytes)
- FIELDS V002 `2ce9f1c7…`, FIELDS V001 `a33b153b…`
- IMPL `854cad0d…`
- VALIDATION `930ca7bc…`
- author harness `998e0c2e…`
- SOURCE_DELTA `56a95b7e…`
- HASHES V001 `8b92153a…`
- r13 source `f5adfd11…` (410433 bytes)

Fence tools: `fence_c4v002.py` `c993d34c…` and `run_fenced_c4st2.py` `fe904509…` were copied into `tools/` and are byte-identical to the originals (cmp). Every script ran through the runner: selftest 8/8, exception probes 15/15, and **0 blocked after the selftest** in every run.

## 1. Byte, line, token and AST diff, r13 to r14 (TESTED)

Script: `scripts/diff_r13_r14.py`. Output: `out/DIFF_R13_R14_C4.json` (`c97169c4…`).

- **Bytes:** the common prefix is 34476 bytes and the common suffix 375957 bytes, which sum to all 410433 bytes of r13. The only addition in r14 is `, 'I4'` at L341, columns 115 to 121.
- **Lines:** 5865 newlines in each file, no CR. There is one line opcode, a replacement of L341 by L341, and every line keeps its number.
- **Tokens:** two tokens are inserted, `OP ','` and `STRING "'I4'"`, both on L341. The 614 comments are identical in text and in line. The string-token multiset is unchanged apart from that one inserted token.
- **AST:** both files have 440 top-level nodes with the same names. There are 231 function and class definitions, identical including their AST and their line spans. Of the 207 module constants, only `GATE_RECORD_AFTER_SEAL_ALLOWED` differs. Its Assign node and Tuple node end 6 columns later, and one Constant is added.
- **Exact inverse:** replacing the r14 line (unique in r14) with the r13 line gives sha `f5adfd11…`. The forward step on r13 gives `f3f9ba7e…`. The r14 line equals the r13 line with `, 'I4')` in place of its closing `)`.
- **SOURCE_DELTA:** its `diff` field equals `difflib.unified_diff(r13, r14)` exactly (876 chars), and its claim `exact_inverse_restores_parent: true` holds.
- **Runtime, fenced import of both modules (TESTED):** `scripts/fenced_token_and_contract.py`, output `out/TOKEN_AND_CONTRACT_C4.json`.
  - Importing either module touches no files beyond its own module and numpy. A static scan of module-level calls finds only math, tuple, dict, re.compile and `_num`. The fence logged 0 blocked operations.
  - The runtime tuples are r13 = 9 gates and r14 = the same 9 plus `I4`.
  - Each of the 25 `ALL_GATES` was tried with a minimal synthetic registry carrying `PRODUCED_AFTER_THE_SEAL`:
    - `producer_registry_from_obj` and `gate_record_sha_codes` change **only for I4**: refused becomes accepted, and `[GATE_RECORD_TOKEN_NOT_ALLOWED_FOR_THIS_GATE_NEW52:I4]` becomes `[]`.
    - r14 accepts the token on I1T, T2I, SRB_ROT, RB_FP, SR_K, EA, I4, MT, HARMONICS and FLAG_RULINGS.
    - r14 refuses it on B0, B0prime_DRY, B0prime_RERUN, B0_FA, B1, B1_OFF, B2, B3, B0_RO1, B0_N3, EPS, DOUBLING, GQ, LO and LO_NGC.
  - The tuple has four consumers: L1122 (loader acceptance), L1126 (refusal message), L1184 (`gate_record_sha_codes`) and L5172 (the FIELDS rendering). The refusal message now ends in `…/SR_K/I4`, as expected.

## 2. Pins (TESTED)

Script: `scripts/verify_pins.py`. Output: `out/PINS_R14_C4.json` (`44acb6af…`).

- **114 of 114 `{path, sha256[, bytes]}` pins match their bytes, with 0 failures.** By record: SELECTED V001 7/7, SELECTED V002 8/8, HASHES V001 50/50, HASHES V002 4/4, VALIDATION 34/34, SOURCE_DELTA 2/2, BUILD_PROGRESS 9/9.
- The pin graph is acyclic and no file pins itself. HASHES V002 is the only unpinned publication file, which is expected because it is the top of the chain.
- **Evidence agrees with the claims (TESTED from the logs; the suites were not re-run):**
  - author v002 TEST_SUMMARY: 718/718, with `script_sha256` f3f9ba7e and `tests_sha256` 998e0c2e;
  - author v001: 717/718, the only failure being `R12_FIELDS_R12_CX3V002_MD_IS_THE_REGENERATED_CONTRACT_BYTE_FOR_BYTE`;
  - real_v001.json: 70 expectations, `all_expectations_met` true, script f3f9ba7e, tool 8b541b98;
  - MUTATION_R13.json: 96/96;
  - guard logs: author v002 and v001 have 24 logs each with 0 denials, real has 1 log with 0, mutation has 1 log with 7 (the inherited /.vol probes).

## 3. FIELDS (TESTED)

Scripts: `scripts/fenced_token_and_contract.py` and `scripts/fields_decompose.py`. Output: `out/FIELDS_DECOMPOSE_C4.json`.

- **Regeneration (fenced):** in-process `write_field_contract` into `gen/` gives r13 `5cc95a06…`, equal to `r12/FIELDS_R12_CX3V002.md`, and r14 `a33b153b…`, equal to `FIELDS_R14_CX1V001.md`.
- **FIELDS V001 vs the r13 generated contract:** the only difference is `, I4` on L66, inside the rendered sentence "the string is accepted only for SRB_ROT, …, SR_K, I4". That line renders the token set, so A114 justifies it.
- **FIELDS V002 vs the r13 FIELDS of record (`7b116b01…`):** V002 is made of three parts:
  - a new r14 preamble of 6 lines. It is justified as the A114 note, and its claims are true by the diff: the R12 heading is inherited, I4 is required for parallel8, and its record requirements are unchanged;
  - r13's A102 explanation, **minus its "SHA256 from bytes" block** and with the line "The inherited field specification follows verbatim." replaced by "## Current generated contract" (N5);
  - FIELDS V001, exact bytes.

  The r13 FIELDS of record is itself the r13 explanation, then the marker line, then exactly `FIELDS_R12_CX3V002.md`.

## 4. Author harness, r13 `71c7b516` to r14 `998e0c2e` (TESTED)

Script: `scripts/diff_harnesses.py`. Outputs: `out/HDIFF_*.diff` and `out/HDIFF_SUMMARY.json`.

- **Five hunks, 5 lines removed and 8 added:**
  1. docstring L1: the candidate's file name, r13 to r14;
  2. **usage line L52: the harness's own file name, r13 to r14.** This one is not among the IMPL's three categories, and it is cosmetic;
  3. `CMP` at L68: the candidate path;
  4. L4319 to L4321: the 12 A114 MUST assertions. They come right after `R12_ADAPTED_A88_…`, one for `I4` accepted and 11 for refused (B0, B0prime_RERUN, B1, B1_OFF, B2, B3, DOUBLING, EPS, GQ, LO, LO_NGC), using the existing `tk` dictionary of loader results;
  5. L5210 to L5211: the generated-contract reference now points at `FIELDS_R14_CX1V001.md`, under the same test ID.
- **Roster:** r13's 706 IDs keep their order, and their (pass, outcome, expected, subtype) values are identical. The 12 new IDs sit at position 621. There are no duplicate IDs.
- **v001 harness** (`r14/tests_…_r13_cx3v001.py`, `b00e533a`): it differs from v002 only in the FIELDS reference, which is the failed attempt the IMPL describes.
- **Other tools:**
  - The guard is identical to r13's (`fc69b438`).
  - The entry tool and four record/mutation tools differ from their r13 copies by path substitutions only (r13 paths become r14 paths). `run_checks` is identical.
  - The IMPL does not mention the record/mutation path substitutions (N7).

## 5. Line numbers and C-08 (TESTED)

Script: `scripts/new_tag_lines.py`. Output: `out/NEW_TAG_LINES_C4.json`.

- **No line number changed** (see §1). The changed line, L341, carries no NEW id.
- r13 and r14 contain the same **19 NEW ids**, and every occurrence of every id is on the same line in both files. First lines:

  | ID | Line | ID | Line | ID | Line | ID | Line |
  |---|---|---|---|---|---|---|---|
  | NEW-4 | 2848 | NEW-7 | 87 | NEW-13 | 236 | NEW-16 | 4989 |
  | NEW-17 | 86 | NEW-19 | 272 | NEW-21 | 108 | NEW-30 | 4440 |
  | NEW-31 | 54 | NEW-34 | 1638 | NEW-39 | 209 | NEW-44 | 5059 |
  | NEW-52 | 32 | NEW-53 | 3171 | NEW-54 | 3635 | NEW-60 | 103 |
  | NEW-64 | 2038 | NEW-71 | 3326 | NEW-73 | 866 | | |

- `c08_table` checks:
  - Disclosures V001 (`b9db6fd1`) and V002 (`a0284ece`) cite the r13 file. V003_DRAFT (`21968a07`) cites the r14 file.
  - **In all three, the 19 rows are exactly the source's 19 ids, and each row's line is that id's first line.** The cited lines are byte-identical in r13 and r14.

## Findings (all NOTE under A115)

- **N1, the selection succeeded (TESTED).** SELECTED V002 `6b650ece` supersedes the dispatched V001 `dc74949d`, by sha.
  - The two differ only in `implementation` (`854cad0d` becomes `COMPARE_V007_IMPL_R14_CX1V002.md` `2ba6d12e`), `note`, `supersedes_selection` and `utc`.
  - IMPL V002 is the IMPL V001 bytes plus one appended section. That section names `f3f9ba7e…` in full and says "r14 declares no NEW item", as Claude4 0129 (`14562edf`, 03:15:42Z) asked.
  - Root's disclosures V003_DRAFT names V002 and IMPL V002.
  - This review covers both selections. The review of record should name V002 (`6b650ece`).
- **N2, stale inherited prose in the source (TESTED, no effect).**
  - The comment at L332 to L334 still says "every other gate (EPS, GQ, LO, LO_NGC, DOUBLING, the B-gates, I4) is registered by record sha", which L341 now contradicts.
  - L1125, L1178 and the FIELDS row text at FIELDS V001 L261 ("SR_K included by A88") cite A88 and not A114.
  - All of this is byte-identical to r13, because A114 says nothing else changes. The FIELDS V002 preamble discloses it ("Earlier statements that I4 must be registered by record sha are superseded only on token timing").
- **N3, a stale test ID.** `R12_ADAPTED_A88_TOKEN_ACCEPTED_ONLY_ON_THE_NINE_POST_SEAL_GATES` now passes with ten gates. Its assertion is relative to `M.GATE_RECORD_AFTER_SEAL_ALLOWED`, plus SR_K in and EPS out, so no harness assertion pins the exact ten-element set. The byte diff does pin it (§1).
- **N4, MUST coverage.**
  - The 12 MUST assertions exercise only the loader.
  - They do not name B0prime_DRY, B0_FA, B0_RO1 or B0_N3. RI-33 builds B0_RO1 and B0_N3 before the seal.
  - They do not exercise the second consumer, `gate_record_sha_codes` (L1184), for I4.
  - This review TESTED both consumers for all 25 gates, and only I4 changes. A114's literal list is satisfied.
- **N5, FIELDS V002 edits the inherited r13 text without saying so.** It drops r13's "SHA256 from bytes" block, which pinned:
  - 0629 `ca8606b0`;
  - the r13 source `f5adfd11`;
  - r12 FIELDS `5cc95a06`;
  - the parent SOURCE_DELTA `f87a921d`.

  It also replaces the line "follows verbatim". Seal tools v004 do not read FIELDS (grep of the named tool files), so the edit is not needed for the tools. No r14 record pins r13's FIELDS of record `7b116b01`, which is still intact.
- **N6, a self-consistency test.** The harness's FIELDS test compares r14's regenerated contract to `FIELDS_R14_CX1V001.md`, a file that r14 generated. The independent check is §3: V001 equals the r12/r13 generated contract plus `, I4` on L66.
- **N7, hygiene of the harness copies.**
  - `r14/tests_kmax_tail_compare_c2v007_r13_cx3v001.py` (`b00e533a`) carries r13's harness name, but its bytes differ from the r13 harness of record (`71c7b516`). It is the failed v001 r14 harness.
  - `r14/tools/author_entry_cx3v001.py` (`9bccb5fa`) was edited but never used. The recorded commands invoke the guard directly, and the entry's output base `out/author_cx3v001` does not exist.
  - The IMPL does not mention the path substitutions in the record/mutation tools.
- **N8, unpinned evidence.** HASHES and VALIDATION do not pin `out/author_v002/TEST_SUMMARY.json` (the structured 718/718 record, which agrees with the pinned stdout), the v001 guard logs, or the real/mutation stdout. The scope line says the list is not exhaustive.
- **N9, root chronology.** The A113 header says 03:25Z and the A114 header says 03:35Z. But the V006 file's mtime was 03:14Z when A114 was first read here at 03:20Z, and r14 was built from 03:15Z to 03:18Z citing A114 (BUILD_PROGRESS at 03:15:27Z). The A114 text re-read at 03:35Z, after A115 was appended (file mtime about 03:28Z), looks the same as the 03:20Z reading. That comparison is FORMAL: it was made by eye, because the 03:20Z bytes were not saved. V003_DRAFT, whose mtime is 03:19Z, says "~03:45Z". These are forward-dated stamps, not clock stamps. They do not affect "before any T result".
- **N10, c08 wording.** `c08_confirmation` says each id is "carried as a [NEW-n] tag". In r14's bytes, only NEW-52 ever appears bracketed (first at L1106), and its row correctly cites L32, the first mention of the id. The rows are right; only the wording is loose.

## UNTESTED or out of this lens

- the actual I4 N1/N8 pair, the I4 producer and its V010 registration;
- the case block `76309ae3` (`parallel8`), which was not read;
- end-to-end evaluation of an I4 record bound by the token;
- re-running the author, real and mutation suites (only the logs were checked);
- production execution.

RI-33's phrase "once the runs exist" was found in prereg r6 `ROOT_ITEMS_R6.md` L38, as a recommendation. That support is FORMAL.

## Conduct

- Writes: only inside this folder (`tools/`, `scripts/`, `out/`, `gen/`, `PARTIAL.md`, `LENS_DIFF.md`). Nothing was deleted, moved or sent over the network.
- r13 and r14 code was executed only under the fence, on synthetic inputs.
- Some read-only checks ran outside the fence: shasum, cat, sed, grep and diff on named author files, and one-line `python3 -I -B -c` JSON parses of author outputs (TEST_SUMMARY, real_v001.json, MUTATION_R13.json, guard logs). None of them imported r13 or r14.
- Disclosure: `ls -la r14/out/author_guard_v002` lstat-ed one empty directory there named `KMAX_A2F10_C5H_RUN_V001`. It is the author guard's inert stand-in (log GUARD_44148 names it as the `standin`). It is not under runs_ext and not a symlink, and it was not entered. No runs_ext, UVT run output, C5H run or target data was opened, listed or stat-ed.
- One empty fenced run, with a stdin script, produced no output. `scripts/source_delta_diffcheck.py` replaced it.
