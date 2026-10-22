# DBP C2V004D: the POST_S1 walls to the Phase-2 ceiling (C3V001; root 0844, V006 A284)

This is a Claude3 build and review candidate. It is not an adoption and not a launch. **C2V004C stays the verdict-day object and is unchanged.** C2V004D is for S8 onward.

## Trace (TESTED from bytes)

- **Where the walls live.** They sit at `batches.POST_S1.caps_per_case.ROOT_NAMES_AT_REGISTRATION_K3|_K4.wall_cap_s`, which is 100800 in both C2V004B (`e239d21e`) and C2V004C (`ce9cbef8`). C2V004C left POST_S1 byte-identical to C2V004B.
  - Root names the two entries at registration as S1_UA_C3T and S1_UA_C4T, in the pair guard's `S1_OVERLAP_CASES` order.
  - The two entries' caps are identical, so the K3/K4 mapping does not affect any value.
- **How the walls reach the pair.** The S1 pair guard (`1274a39a`) binds each call's caps three ways:
  - to the parent admission's `cfg.caps[case]` (ROOT_CAPS_BINDING, L428);
  - to its child admission's `caps` (L377);
  - to its child plan's call bytes (L381).
- **How the wall is used.** The successor launcher passes the call's wall to the monitor `ba031c23`, which takes any wall > 0. The same trace as C2V004C applies: no FINAL spec, H1 config or numerics byte holds a wall.

## The change (data only)

**C2V004D is C2V004C with the two POST_S1 `wall_cap_s` leaves set to W**, by C2V004C's fill rule.
- **The fill.** The pre-built fill is 2026-10-22T09:30:00Z, C2V004C's own fill (the earliest S4T R3 receipt time, A260). So W = 3,443,340 s, equal to C2V004C's HEADLINE walls.
- **Provenance leaves:** `schema`, `supersedes.{path,sha256,what_changes}` (now pointing at C2V004C) and a new `note_a284`.
- **Leaf diff.** Against C2V004C, exactly 7 leaves change: 2 walls plus 5 provenance leaves. Against C2V004B, exactly 19 change: 13 walls, plus `schema`, `supersedes.*`, `note_a271` and `note_a284`.
- **Asserted unchanged:** C2V004C's 11 HEADLINE walls, every RSS cap (physical RAM), every output cap, every DIII, SENS_LO and SENS_HI wall, and every non-cap byte.
- **Fill rule.** W is counted from the earliest plausible fill, so it is never less than the exact time remaining at any later fill. No wall cap therefore ends a run before the ceiling (A246). The ceiling freezes the score either way (A249).
  - The builder refuses a fill earlier than C2V004C's, so no POST_S1 wall exceeds the HEADLINE walls.
  - It also refuses any wall of 100800 s or less.
- **Exact alternative (optional).** At S8 fill time, root runs the builder with `--fill-utc "$(date -u +%Y-%m-%dT%H:%M:%SZ)"` into a new folder. Only the two POST_S1 walls move; the HEADLINE walls stay C2V004C's.

## Files (sha256 from bytes)

- **Builder:** `build_params_s45_c2v004d_c3v001.py` `1e16b718003154b061d2969ba95914f461212c48aa0bf430e3e94cb93b3e8e84`. It reads only the pinned C2V004B and C2V004C bytes, asserts both leaf-diff scopes, and writes by exclusive create into a new folder.
- **Instance:**
  - `C2V004D_FILL_20261022T093000Z/DIRECT_BATCH_PARAMS_S45_C2V004D.json` `5d3f4bb84c35adee296048264ed306102ae51267f7da7ba2595cce561698f7a2`;
  - `C2V004D_FILL_20261022T093000Z/LEAF_DIFF_S45_C2V004D.json` `971575dd5f315a8087107b568a47de25b41c47c1ff98753a21750d561abed899`.
- **Check script:** `check_s1_pair_caps_c3v001.py` `5f24c6bf37e3fd2ae04cd300cd9a11835356967e13b0f7b983377c9319cb72ce`. Run it after root assembles the pair:

  ```
  python3 -I -B check_s1_pair_caps_c3v001.py <C2V004D path> <its sha256> <pair plan> <parent admission>
  ```

  It checks that five records carry the DBP POST_S1 caps (wall, RSS and output): the pair plan, the parent admission, both child admissions and both child plans. The children are read through the parent's pinned refs, with their sha256 verified. It also checks that the parent admission's plan pin matches the plan bytes.

## Tests (synthetic; the real C2V004B and C2V004C are read only)

- **Test and record:** `test_build_c2v004d_c3v001.py` `04756b2ef434199b0199e0c847403c3792be463fbd32640b875a613e6f2f2468`; record `test_c2v004d_run002/TEST_RECORD.json` `3f1a101758da65deb6d186830f6ae91aa0c7439c0d40c09ccd0bbe305872c113`.
- **Result:** 8/8 pass.
  - **18 builder checks**, including:
    - both exact leaf scopes;
    - HEADLINE walls equal to C2V004C's;
    - determinism;
    - a later exact fill moves only the POST_S1 walls;
    - refusals for a fill too late, a fill after the ceiling, a fill before C2V004C's fill, non-canonical UTC, a tampered C2V004B and a tampered C2V004C.
  - **4 CLI checks.**
  - **12 checker cases.** The positive case passes, and each of these is refused with its exact code:
    - a pair filled from C2V004C's caps;
    - an old wall in the plan, the parent admission, a child admission or a child plan;
    - a changed RSS;
    - a bad child pin;
    - the wrong order;
    - an unbound plan;
    - a DBP sha mismatch;
    - C2V004C passed in place of C2V004D.
- **Mutants:** 11/11 restoring mutants are killed.
  - **6 builder mutants:** scope checks removed together with a DIII wall change; a shorter wall allowed; the C2V004C pin skipped; the wall rounded up; the HEADLINE walls refilled from the new fill; a fill before C2V004C allowed.
  - **5 checker mutants:** the child-plan caps, the parent-admission caps, the pin sha or the plan binding left unchecked; only the wall compared.
- `test_c2v004d_run001/` is the same suite run before a dead-code line was removed from the test, and it also passed. `run002` is the record.

## UNTESTED

- Root's fill of the real S1 pair records. The deciding check is `check_s1_pair_caps_c3v001.py` after assembly and bind.
- Monitor behaviour at multi-week walls. This is code-read only (a float compare), as for C2V004C.
