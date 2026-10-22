# README c3v005: the SELECTED seal pre-stage tuple after FROM_CODEX/0644 (A107) (Claude3)

Written 2026-10-19T00:13:04Z (`date -u`). This supersedes `README_SEAL_ASSEMBLY_C3_c3v004.md` (`5236dcbc`) for everything 0644 changes; c3v004 stays for history and for the unchanged sections it details. The selection of record is `SELECTED_SEAL_PRESTAGE_C3SA_c3v005.json`. Codex1 runs the final delta.

## The selected tuple

| role | file | sha256 |
|---|---|---|
| script (root runs it) | `ROOT_SEAL_STEPS_c3v013.sh` | c1a469e98c842af37a4c8886459f4f2e2262053ea8848eebdf4a432dc5d641cd |
| per-step helper | `tools/seal_steps_c3sa_c3v013.py` | ad581a06854ad5ce0e337624860cdf07c04181fccb066f71e79128f1d9b05200 |
| pinned-source runner (unchanged) | `tools/run_pinned_c3sa_c3v003.py` | 2b040e94a2b74eae981485288471376b86be0784a0a50b59093312c4fd87bf73 |
| in-process fence (unchanged) | `tools/fence_c3sa_c3v003.py` | 9c62ad4902c895f0aeeba3a78976b5944146ee0de153989dbc79470528dd2863 |
| slot draft (unchanged) | `SLOT_VALUES_DRAFT.json` | c93691f5d1931beef8abb656ced3446c99d0adf286d4b5de0c709ecb570284ba |
| step-8 manifest draft (unchanged) | `MANIFEST_GATES_ONLY_DRAFT_C3SA.json` | e5967bb9901fda39703553c5c02b4d11a580ef8456f6c0b7d315ee4c750f09da |

The convenience watchdog `step2_disk_watch.sh` (`bd0d9bab…`) is unchanged and stays outside the seal tuple and its hash chain.

**Step 0 still refuses**, because prereg r6 and seal tools v003 are still PENDING (P1, P11).
- At 00:11Z neither `SELECTED_R6_C4V001.json` nor `SELECTED_SEAL_TOOLS_V003_C4V001.json` existed under `v007_final_prereg_c4/`. Claude4 0112 says both follow its refuters' verdicts.
- The r6 **candidate** (`d28c95f5`, 0111) has landed. It is probed below but not wired, because Claude4 asks to wire the SELECTED file, not the candidate.

## What 0644 (A107; Codex1 0101) changes
- **P12 = A107 option (b).**
  - Step 3b passes an explicit two-entry exclusion list, `C04_EXCLUSIONS`:
    - `certificates.EPS_NGC` = `…/certificates_ngc_k32/gates/EPS_CERT_NGC91_V001.json` / `1d5eef1b…`;
    - `certificates.I1T_NGC` = `…/certificates_v002/gates/I1T_NGC_T120L_V001.json` / `3ae7981a…`.
  - The helper accepts exactly that list and nothing else (`C04_A107_EXCLUSIONS`). These refuse:
    - a third slot;
    - a missing entry;
    - a repeated entry;
    - another path or sha;
    - an excluded slot whose pin differs from the A107 pin;
    - an exclusion naming a slot the file does not hold.
  - Excluded slots are still pinned from bytes and reported with their registry codes.
  - C-04 applies to every other slot. No registry V010.
- **C02-SEL-STRICT.** A SELECTED file is parsed strictly from the one buffer `pin()` read. Each of these refuses with a typed `SELECTED_*` code:
  - invalid UTF-8 or a BOM;
  - nesting deeper than 64;
  - a duplicate key;
  - NaN, Infinity, or a float overflowing to inf;
  - an integer longer than 4300 digits;
  - trailing or invalid text;
  - a non-object top level.
  - There is no substring fallback anywhere.
- **C02-SEL-ASSOCIATION.** Each requested `(path, sha)` must be one object of that parse, with `path` equal to the absolute path and `sha256` equal to the sha.
  - Strings elsewhere never count, and a suffixed path (`.other`) never counts.
  - An object giving the same path another sha, or no sha, refuses.
  - The schema follows Claude4 0112 (exact `{path, sha256}` pairs). **The role keys are PENDING** Claude4's real SELECTED files. The same function serves `check-tor` (r6) and `selected-names` (v003).
- **A106-C03-S1.** The slot sha and the body's `record_sha256` are validated as 64-hex lowercase SHA-256 **before** the comparison: `C03_MALFORMED_SLOT_SHA` / `C03_MALFORMED_BODY_RECORD_SHA`.
- **Codex1's C04 boundary note: closed.**
  - Each non-excluded slotted gate record must also carry its gate's pass verdict from r13's own `GATE_PASS_VERDICTS`. A registered FAIL, an absent or an unknown verdict refuses with `C04_VERDICT_NOT_THE_GATE_PASS_VERDICT`.
  - The output field is now `records_registry_admitted_with_the_gate_pass_verdict`.
  - C-04 is still registry admission plus the pass verdict, not `evaluate_gate`.
- **Script c3v013, found by probing the r6 candidate.** `tor_table_bytes` now also accepts an ABSOLUTE `byte_copy` inside the text of record's own folder. That is r6's form; r5 used a relative one. Script c3v012 would have refused r6 at step 0.

## Wiring r6 and v003 (the next, small successor; from the SELECTED files, verified from bytes)
### r6 (two lines)
- Set:
  - `PREREG_TOR="<r6 path>"; PREREG_TOR_SHA="<sha>"`
  - `R6_SELECTED="…/SELECTED_R6_C4V001.json"; R6_SELECTED_SHA="<sha>"`
- `check-tor` requires the exact pair in the strict parse. If Claude4's real schema has a role key for the text of record, the successor can require it too.
- On the candidate the probe already passes `check-tor`, `tor_table_bytes`, the empty-dispositions object, rehash, `sealed-prereg` and the full `check-tor`: `probe_r6_candidate_20261019T000913Z/PROBE_R6_CANDIDATE_RESULTS_C3SA.md`, `13136b1b…`.
- The dispositions file for r6 is `{schema, frozen_addendum_sha256: c01b3c51…, entries: []}`.

### v003
- Set the five `T_*` pins, `V003_SELECTED` and its sha, and `SEAL_TOOLS_STATUS`.
- Update the RUN forms to v003's module names.
- Add tool 1 `--addendum-at-text-of-record "$TABLE_BYTES"`, and tool 4 `--check-admission-config` at step 12.
- Then re-run dry-run passes A and B.

## C-08: ROOT MANUAL CHECK (unchanged; the exact steps)
r13's IMPL `COMPARE_V007_IMPL_R13.md` (`274f7049…`) has no NEW-item id, so the ids are found in the compare source (`f5adfd11`; NEW-52 occurs 11 times).
1. `shasum -a 256 <NEW-item list> <IMPL> <compare>`
2. List the ids:
   `python3 -I -B -c 'import re,sys; print(sorted(set(re.findall(r"\bNEW-[0-9]+\b", open(sys.argv[1]).read()))))' <list>`
3. For each id:
   `grep -n -w 'NEW-<n>' <IMPL> <compare>`
   Record id, file and line.
4. An id with no hit refuses the seal. Put the table in the seal record's disclosures, with "C-08 checked by hand by root (A106.2)".

C-08 appears in the script only as a summary `root_next` instruction. Root has to do it at assembly, before the SEAL_RECORD, and the seal record must say so (Codex1 0101).

## PENDING
| # | item | now |
|---|---|---|
| P1 | seal tools v003 | NOT PUBLISHED (step 0 refuses) |
| P11 | prereg r6 (C-02) | NOT SELECTED (step 0 refuses); the candidate `d28c95f5` is probed, not wired |
| P12 | C-04 scope for EPS_NGC and I1T_NGC | **RULED A107 option (b); done** (`C04_EXCLUSIONS`) |
| P2-P10 | as in README c3v004 | unchanged (P3 RI-36 and P4 GAP-12 remain PENDING_ROOT_RULING) |

## Controls (all re-run on helper c3v013 / script c3v013; step 9 never executed)

| suite | folder | result |
|---|---|---|
| A + C-02…C-06 + SEL + C03-S1 + C-04 A107/verdict | `mustfail_c0x_20261019T000552Z/` (`83d74dde…`) | **73/73 ALL_OK** |
| Codex1's own five C02 counterexample files (read only), with its inert TOR | (in the suite above, CX1-SEL-1…5) | all REFUSE; `selected_good.json` PASS |
| Codex1's three C03 cases (null, empty, `not-a-sha`), plus a malformed body only and upper case | (C03-5…9) | all REFUSE |
| W7-S1 + RP-S1 | `mustfail_w7rps1_20261019T000643Z/` (`642c6324…`) | 41/41 |
| B1 + B3 | `mustfail_regress_20261019T000643Z/` (`97be4743…`) | ALL_OK (B1 0 target reads; B3 A102-A106) |
| B2 + N1 (now a saved script) | `mustfail_b2n1_20261019T000840Z/` (`3d9c058a…`) | ALL_OK |
| `tor_table_bytes` (the script's own function text) | `tor_table_bytes_test_20261019T001039Z/` (`137b9a28…`) | 6/6 |
| watchdog | `watchdog_test_20261019T000645Z/` (`bd2a5939…`) | ALL PASS |

The first B2/N1 run (`mustfail_b2n1_20261019T000753Z`, `a03506db`, script c3v002) had **two harness expectation errors, not product defects**; it is superseded by c3v003:
- B2-4 with a plain main cannot even find the sibling under `-I`, as the original 22:16Z run recorded.
- B2-6's pattern matched the helper's own `_exec_module` alias.

**Dry run of record:** `dry_run_20261019T001047Z/INDEX_DRY_RUN_C3SA.md`.
- Pass A: C-04 PASS at 3b; stops at 4a, where v001 tool 3 refuses r5 (expected).
- Pass B: every step PASS; step 9 STUBBED; fence 0.

## Superseded in this round
- `ROOT_SEAL_STEPS_c3v011.sh` (`af74e9bd`), `ROOT_SEAL_STEPS_c3v012.sh` (`cb41f72c`; dry run 000226Z only) and helper `seal_steps_c3sa_c3v012.py` (`b1348396`).
- `SELECTED_SEAL_PRESTAGE_C3SA_c3v004.json` (`76651cf7`) and README c3v004.
- `tools/mustfail_c0x_c3sa_c3v001.py` and `tools/mustfail_b2_n1_c3sa_c3v002.sh`.
- `tools/make_dry_run_c3sa_c3v005.py` and `tools/setup_dry_run_c3sa_c3v003.sh`.

The full file list is in `HASHES_C3SA_c3v004.txt`.
