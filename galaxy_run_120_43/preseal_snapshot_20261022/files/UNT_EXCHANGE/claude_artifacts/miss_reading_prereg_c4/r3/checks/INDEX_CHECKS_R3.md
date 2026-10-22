# INDEX_CHECKS_R3: the closure table and the pattern suite, added to r3/ after the generator

Added by the final build stage (a helper of lane Claude4; dispatch 0619, A98.2), as the stage brief directs: the pattern suite and its results in `checks/`, and the closure table in `r3/`. Each file was created with exclusive create at 2026-10-19T02:07:41Z (`date -u`), after the generator had finished. Paths are relative to `r3/`. From `r3/`, `shasum -a 256 -c checks/HASHES_CHECKS_R3.txt` re-verifies the four files below.

**Scope of the generator's files.** The generator wrote `INDEX_R3.md` and `HASHES_R3.txt` before these additions. They describe its own 12 files, and `HASHES_R3.txt` lists only those. The files below are hashed in `checks/HASHES_CHECKS_R3.txt`.

| file | what it is | sha256 |
|---|---|---|
| `CLOSURE_R3.json` | byte copy of `r3_work/text_c4/CLOSURE_R3.json` | `d75587f3f5755d9d98f90ea4621cd43a738ab9458cd0038053ccaac81d9d9818` |
| `checks/pattern_suite_c4v001.py` | byte copy of `r3_work/integrate_c4/pattern_suite_c4v001.py` | `11ee5d4228dc527ad4792c6ee1dacdc284c518f20e178c29122df1564472aa68` |
| `checks/PATTERN_SUITE_RESULTS_R3.json` | the suite's output, run in this stage beside this folder's PREREG (`b0fba984543c5c93fc4d25497c6e9e97f33662d3a98a63856b4933e4b1f47dd0`) and ROOT_ITEMS (`b33270fe9e07bbe3990cdeca6859daf08dd7d1e9836936befd2086d023edc4fb`) | `b09fcc6fc07da91b5a3f4ec2f701b754c582efeb73c7dad23f0ce8f4626bff39` |
| `checks/INDEX_CHECKS_R3.md` | this file | in `checks/HASHES_CHECKS_R3.txt` |

## The closure table

`CLOSURE_R3.json` (schema `UNT_MISS_READING_R3_CLOSURE_C4V001`) has 94 rows: 85 FIXED, 2 NOT_ADOPTED, 7 ROUTED_TO_TOOLS_STAGE. They cover every finding of the round-2 recheck (lenses R2-A, R2-B and R2-C, with their refuters), both Codex2 0490 items, and the 21 round-1 rows that the recheck found only partly closed. The findings of the r3 refute stage are not in it; their dispositions are in the r3 fix table of `CLAUSE_SOURCE_MAP_R3.md`.

TESTED in this stage:
- the closure builder `r3_work/text_c4/tools/build_closure_r3_c4.py` (`34e393b3985d0bf202a8ca751fca3f5d17db7d1fd2c38a8881eaf688284681d0`), run inside the check's audit hook, reproduces it byte for byte and reports no coverage problem;
- its 73 round-2 rows appear verbatim in the clause map, rendered as the fix stage renders them, and its round-1 rows are in the clause map's round-1 table (20 by id, and the Codex2 checklist row by name).

## The pattern suite

`checks/pattern_suite_c4v001.py` was written in the integrate stage from the r3 text. It is an independent implementation of the r3 rules on synthetic, dimensionless rows. By its header, it opens only the two texts (to hash them), its own bytes and its output file. Its rules are hard-coded, so the two text shas it records name the files it was run beside, not files it parsed.

Results in this folder: all_ok true, run from 2026-10-19T02:05:58Z to 2026-10-19T02:06:56Z (57.8 s). Each verdict:
- named cases (42): true;
- named LATE pairs (8): true;
- other rule cases (39): true;
- exhaustive enumeration, five row states, 1 to 3 rows per zone, four value schemes (14,895,500 outcomes): no violation, and the scalar and vectorized forms agree: true;
- the same with zero-row zones allowed (3,796,416 outcomes): no violation: true;
- exhaustive LATE-gate pairs (68,694,048 pairs): no violation, and the two forms agree: true;
- random outcomes at the registered zone sizes (60,000): no violation: true;
- every change that section 4 says a LATE gate can make is witnessed: true.

What all_ok does not cover:
- **MINORITY_MISS** (section 3), which the fix stage added: the suite's A10 checks are per outcome. The fix stage tested the row-level rule by replaying the refute stage's enumerations, in `r3_work/fixlog_c4/FIX_RULES_REPLAY_V001.json` (`7b95f31eb493b2289193f42ccd8319585209d4f0adb9bf736bef4627d68f7d42`, all_ok true, 0 violations). That file is not copied here.
- **The `text_findings` field** holds fixed strings from the integrate stage. PS-1, PS-4 and PS-5 quote sentences that this folder's PREREG and ROOT_ITEMS no longer contain (TESTED in this stage by containment); the fix stage closed them (RL-02; N-06 with PS-4; RL-04 with PS-5). PS-2 and PS-3 are still open notes (FIXLOG N-01 and N-02).
- **The `drift_conflict_case` field** compares the suite's default R-DRIFT rule with the superseded literal reading of the old section 3. The default rule follows the fixed order of section 3 (no trigger gives PATTERN_NOT_HELD; then an against-condition gives INCONSISTENT). A value of true records that the two readings differ; it is not a defect of this text.

## The check and these additions

The bundle check's T1 accepts only the generator's file names at the top of a bundle. Run with `--dir r3`, it lists `CLOSURE_R3.json` and `checks` as unexpected bundle files, and reads target-free FAIL from that line alone. TESTED in this stage: every other check passed, and currency passed against the live V005 and V006. The generator's `TARGET_FREE_CHECK_R3.json` was computed before these additions. To re-run the check on the bundle alone, run it on a folder that holds exactly the files listed in `HASHES_R3.txt`.

In this stage, `CLOSURE_R3.json`, the suite, its results and this index were scanned with the check's own T1 to T3 functions, with no pinned names: deny-listed terms, data-like file names, links, HTML entities and comments, disallowed letters, velocity units, and symbol and value pairs. There was no hit. That scan does not test where numbers come from; T4 covers the three texts only.
