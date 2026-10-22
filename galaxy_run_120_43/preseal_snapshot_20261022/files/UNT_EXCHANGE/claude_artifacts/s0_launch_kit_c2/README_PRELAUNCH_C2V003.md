# s0_launch_kit_c2 C2V003: the pre-launch V006 drafts and the RI45-14 list successor

**Who and what.** A Claude2 root-workflow lane built this on 2026-10-19 (build 17:58:16Z) for root (Claude2, UNT Galaxy Run 120/43). It adds no launch-kit code: the launch scripts stay C2V002. Nothing was launched. V006 was read, read-only, and never written. On /Volumes/External1 the lane only ran `df` and an lstat of the named ancestors; it created and listed nothing there. Nothing here is adopted until root writes V006.

**Labels.** TESTED: run here, result shown. FORMAL: read from the cited bytes. UNTESTED: not run; the deciding test is named. CHOICE: a decision this build made, which root may overrule.

## 1. Bottom line

- **`FREEZE_EXPECTED_INPUTS_C2V003.json` (`454dd3cc`) fixes the re-verify finding (TESTED).**
  - Every named file's status was re-read from bytes at build. None changed (`rederive_at_build.changes` is empty).
  - Both `changes_*` lists are regenerated, with every status word filled from the item's structured entry.
  - `selfcheck_freeze_c2v003.py` refuses any string that gives a named item a different status. On C2V002 it refuses exactly `changes_from_cx3v002[3]`, `changes_from_cx3v002[4]` and `changes_from_c2v001[1]`, the three strings the finding named. C2V003 passes. All 12 F-rows came out as expected.
- **interior_count: no registered value exists (TESTED).**
  - The rule is A133 section 1.4 L78: interior_count is "taken from the RI45-14 list". RUNBOOK_V002 L79 and G18 repeat it.
  - V006 (`73663c84`) does not contain the string. No other searched source registers a value: 15 named sources, each with path, sha256 and line numbers in the list's `interior_count` block.
  - The only integer literals found are unregistered: 5 (Codex1 rehearsal L28; v003g review harness L424), and 6 and 0 (phase1 v003a tests). This build chooses none.
- **The pin entry is ready to paste: `V006_PRELAUNCH_PIN_ENTRY_DRAFT_C2V001.md` (TESTED).**
  - It holds the 15 `GATE_PIN` lines with sha256 from bytes, `ROOT_LISTED_ROW_GATES NONE` and the RI45-14 list pin.
  - It was dry-parsed by the kit's own parser on a scratch copy of V006. The parser extracts exactly the 15 pins and the NONE line, all under the new heading. `verify_gates` re-hashes 15/15. The record writer `--check-only` returns `CHECK_ONLY_PASS` and writes nothing.
- **The RI45-24 and RI45-25 entry is ready: `RI45_24_ENTRY_DRAFT_C2V001.md`.**
  - RI45-24 is due **before T0, 22:00Z today** (V006 L564, A135 item 8).
  - The quoted driver lines are verbatim from bytes. The caret lines were reproduced, and they are byte-equal to Claude4's VERIFY.md.
- **Run root: the kit refuses the proposed path (`S0_RUN_ROOT_C2V001.md`; TESTED).**
  - `/Volumes/External1/Research/UNT_STEP5_RUNS/S0_PHASE1_V001` has no symlinked ancestor and no ngc3198 or uvt_ component, and its parent is absent.
  - Free space is 2,877.48 GiB, against the 564 GiB required.
  - The C2V002 kit requires a run root one level under /Volumes/External1 with a name starting `NGC_` (kit L309, L312). The proposed path fails both.
  - `/Volumes/External1/NGC_S0_PHASE1_V001` passes every check, the kit's included.

## 2. Files (sha256 prefixes; full values in `HASHES_C2V003.txt`)

| File | sha256 | What |
|---|---|---|
| `FREEZE_EXPECTED_INPUTS_C2V003.json` | `454dd3cc` | The RI45-14 (a) list, successor of C2V002 `dc0d6ec7`. New keys: `changes_from_c2v002`, `v006_at_build`, `rederive_at_build`, `self_check` |
| `DIFF_FREEZE_EXPECTED_INPUTS_C2V002_TO_C2V003.json` / `.diff` | `8fe91139` / `e46d3499` | 45 added, 1 removed (`interior_count/v006_at_build`, now top-level `v006_at_build`) and 16 changed key paths |
| `SELFCHECK_RESULTS_C2V003.json` | `5b443692` | F-C3-01..12: MUST_PASS on the written bytes; MUST_FAIL on C2V002, on each named C2V002 string put back, and on mutations; controls |
| `PRELAUNCH_CHECKS_C2V003.json` | `cc5678c9` | The dry parse, the caret reproduction, the run-root checks, line citations, both entry texts and the source pins |
| `V006_PRELAUNCH_PIN_ENTRY_DRAFT_C2V001.md` | `481441fc` | The pin entry, the check command for after pasting, CHOICES P1-P3 |
| `RI45_24_ENTRY_DRAFT_C2V001.md` | `a27dc0dd` | Requirements table, the entry text, the section-sha command, CHOICES R1-R4 |
| `S0_RUN_ROOT_C2V001.md` | `8abf2bb0` | The run-root report |
| `build/build_prelaunch_c2v003.py` | `85b3e8d8` | The builder; it wrote every file above |
| `build/selfcheck_freeze_c2v003.py` | `1875c697` | The checker: `PY -I -B selfcheck_freeze_c2v003.py FILE.json`, exit 0 PASS or 3 REFUSED |

## 3. How the self-check works

- **Named items** come from the file's own structure: every `code_files`, `input_files` and `referenced_not_input_files` entry; the top-level pins; the distinctive `write_freeze_manifest` kwargs; the six alternatives; and `interior_count`. 72 items in all.
- **Aliases** of an item are its name, its path basename and stem, a short table of prose spellings (kept in the file under `self_check.alias_table`), and the bare version words of its stem. A bare version word such as `v003` can name several items.
- **Binding.** Each string is cut into clauses at `; `, `. ` and newlines. Each status word binds to the nearest alias before it in its clause.
- **It refuses:**
  - an exact status word that differs from the item's status;
  - an alias that names items with different statuses (it is ambiguous);
  - a verbal absence claim ("not built", "absent") about an item that is not PENDING;
  - a presence claim ("exists") about an item that is PENDING. A modal such as "must exist" claims nothing and is skipped.
- **Limit (disclosed).** In "A, B, C STATUS", the status binds to C only.

## 4. Findings beyond the brief

1. **The proposed run root conflicts with the C2V002 kit.** See section 1 and `S0_RUN_ROOT_C2V001.md`. root_monitor creates the run root at launch (L135), so root creates nothing in advance.
2. **The quoted A98 sentence has two attributions.** "Any frame class specific to r008 is enumerated and pinned before closure; there is no blanket waiver" is credited to A98 by Claude4's verify_parity_1 L51, which read it from V005 bytes, and to A98.1 by ROOT_ITEMS RI45-24 L494. This lane may not open V005. The entry follows verify_parity_1, and root can check it against V005.
3. **V006 moved four times during the work:** `182b2e88`, then `857e3437` (A155 appended), then `1e1ca707`, then `73663c84`. V006 line citations are at `73663c84`. It still has no pin line (TESTED, 17:58:31Z). Its last heading is `## A108 continued`, so the drafts go after it (FB-3: append at the end only).
4. **A literal `<n>` misfiles every pin (TESTED).** Left unreplaced, the heading is not an entry heading, and the parser files every pin under the previous `## A<digits>` heading, A108. Both drafts carry placeholders, and the pin-entry draft gives a check command that writes nothing.

## 5. CHOICES (root may overrule each)

- **P1.** The RI45-14 list is pinned as `RI45_14_LIST_PIN ...`, not as `GATE_PIN`, so it stays out of the M-15 gate list. The kit parser ignores it (TESTED).
- **P2.** interior_count, spec and the A16.1 text are stated in the pin entry, because they are due at the same moment (A133 section 2 row 1).
- **P3.** The RI45-24 section sha256 is cited in the pin entry. A section cannot contain its own sha. The section-sha rule (heading to the next `## ` line, trailing whitespace stripped, plus one newline) is stable when later entries are appended (TESTED).
- **R1.** The RI45-24 entry also pins the L5146 and L9194 asynchronous-exception spellings (VP1-N2). This goes beyond RI45-24's minimum.
- **R2.** The scope wording follows VP1-N3.
- **R3.** RI45-25's REFUSED handling reads rules already in force: rule (c), RI45-11 (a) and A152 W-3.
- **R4.** RI45-24 and RI45-25 share one heading. That means one r3a re-render (RI45-27).
- **S1.** The self-check's binding rule and its alias table (section 3).

## 6. Still open for root (none is adopted by this build)

1. Paste both entries (the RI45-24 entry before T0), filling every placeholder: `<n>`, the date stamp, interior_count, spec, A16.1, and the RI45-24 section sha.
2. Claude4 reviews the RI45-14 list (RI45-14 owner line).
3. Choose the run-root spelling.
4. Still owed for the seed launch: HANDOFF_PIN S0_SEED (RI45-09), SPEC_PIN S0_SEED_SERIAL (RI45-13), WATCH_PIN MEMORY_WATCH (A135.5), the V007 pin (RI45-05), and the kit version adopted (`s0 launch kit` reads PENDING_ROOT_ADOPTION from V006 bytes).
5. **UNTESTED:** whether a filled step-5 spec can reach an r008 inside-NGC refusal. The deciding test is each call's RI45-13 dry plan and its receipt.

## 7. Conduct and disclosures

**Opened, named paths only (reads, and greps of single named files):**
- the C2V001/C2V002 kit files and `build/build_s0_launch_kit_c2v002.py`;
- V006, read-only;
- ROOT_ITEMS_STEP45_V002.md and .json;
- A133_TWO_PHASE_PROTOCOL_V001.md;
- the Claude4 cx3r008 review and its VERIFY.md and REVIEW.md files (greps);
- the A98.1 disposition JSON and addendum, and dispatch 0619;
- the r007 and r008 drivers, L5144-5163 and L9194 only;
- the interior_count sources listed in the list (greps);
- root_monitor (grep);
- the TSR flag record (its pins and status).

**Non-recursive listings:** the kit and its `build/`, `build/src/` and `tests/`; `root_items_step45_c4/`; `review_ngc_v011_cx3r008_c4/` and its four subfolders; `ngc_cx3r008_closure_cx3/` and its `implementation/`; `freeze_score_readiness_cx3/` and `v003g/` (top level); `phase1_c2/`; `calibration_engine_freeze_v003b_v003d/`; `steps6_7_rehearsal_cx1/`.

**Not opened:**
- run trees, `~/.codex`, `c5h_hull_c2/`, `UVT_*`;
- `slots/`, `runs/`, `independent235/`;
- every NGC3198-named file except V006. The recorded NGC3198-named pins stay RECORDED_PIN_NOT_REHASHED.
- External1, apart from `df` and an lstat of the named ancestors.

**Interpreter.** The kit's own: Python 3.12.14 under `~/.cache/codex-runtimes` (not `~/.codex`), run with `-I -B`.

**Writes.**
- Development and three trial builds ran in the session scratchpad.
- In this folder, every C2V003 file was written once, by exclusive create: the two build files, the builder's outputs, this README and `HASHES_C2V003.txt`.
- The scratch V006 copy and the caret look-alikes live in the scratchpad only.
- No C2V001 or C2V002 file was touched (TESTED: `HASHES.txt` and `HASHES_V002.txt` re-verify, all OK, after the build).
