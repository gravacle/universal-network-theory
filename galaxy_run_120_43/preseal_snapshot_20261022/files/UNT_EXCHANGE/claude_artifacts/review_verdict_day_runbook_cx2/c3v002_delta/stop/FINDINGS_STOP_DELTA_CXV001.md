# Codex2 internal delta closure — C3V002 F-STOP-1

`date -u`: Wed Oct 21 16:16:47 UTC 2026

**FORMAL PASS: F-STOP-1 is closed.** No new blocking finding in this narrow delta. This internal handback is not launch authorization. Mechanical text comparisons are TESTED; all shell execution and production behavior remain UNTESTED.

P0 line 125 is now `set -euo pipefail`, immediately before `source` at line 126. XREF identifies it as REDERIVED J:L12, matching J's exact bytes. The generator prepends `R('J', 12)`. Removing this one added line leaves P0 unchanged; all 26 other executable block bodies and the remaining XREF source/kind/text rows are unchanged.

**B9b closure (FORMAL):** in the documented fresh `/bin/bash FILE` invocation containing P0 and B9b, binder line 455 is an ordinary top-level simple command, outside a conditional, short-circuit list, pipeline or other errexit exception. Its nonzero exit stops the call before caps-check line 456. The prior partial-output counterexample cannot mask binder refusal. Partial outputs still require preservation and a new root ruling.

**B4 closure (FORMAL):** comparator line 241 is likewise an ordinary top-level simple command. Its refusal stops before the hash and printf. If comparator succeeds but later shasum fails, pipefail makes the `shasum | cut` substitution fail; the assignment-only command at line 243 has that substitution's status, so errexit stops before printf at line 244. This does not rely on errexit inheritance inside command substitutions: the pipeline status and the outer assignment are decisive.

**STOP prose:** line 17 explicitly says every nonzero exit is a STOP, including kit exit 4, and requires review before continuing. The semantic human gates after zero exits remain required. General Bash errexit exceptions still exist; the formal closure above concerns the actual reviewed simple-command sequences.

**Changed-code risk:** V is now sourced under nounset. A lexical check of its actual assignments, excluding comments, found all referenced uppercase variables defined before use; it contains no option resets. The universal fail-fast behavior is intentional. No scientific command, flags, output paths, body commands or batch ordering changed. The initial in-memory lexical check incorrectly included comment references and failed; the corrected check passed. No reviewed runtime behavior was tested or failed.

**Nonblocking provenance nit:** runbook line 3 still names `build_runbook_c3v001.py`. The actual successor generator002 is byte-pinned below and its delta implements the exact P0 guard. The stale display label does not reopen F-STOP-1 or change command behavior; correct it in any further prose successor.

No reviewed generator, module, runbook block, shell fragment, bash syntax check, failure fixture, scientific command or monitor ran. Only static reads and comparisons ran. No run-tree stat/list/read, V006 read, actual NGC data, postseal records, session logs or network access occurred. Reviewed files were not modified.

## Evidence — SHA256 from bytes

- **runbook_C3V001**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/verdict_day_runbook_c3/RUNBOOK_EXEC_C3V001.md`
  SHA256 `553a0e2c7b1f023c22f68877fc233cf1de5eae2faec70ad81f206d93e6efd170`
- **runbook_C3V002**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/verdict_day_runbook_c3/RUNBOOK_EXEC_C3V002.md`
  SHA256 `3a1487488969e156bc8540c1d3d147d5e3c38f44a09b13e5c32070f1d524696f`
- **xref_C3V001**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/verdict_day_runbook_c3/XREF_C3V001.json`
  SHA256 `aca0ada17bd513dbdbe64268e7901af931552c0fb67a4ba2d93542ef204f0643`
- **xref_C3V002**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/verdict_day_runbook_c3/XREF_C3V002.json`
  SHA256 `59a415e5ee625a65f78fe53b1add5020c7a03c6373902e3b621e0ddd0184cd3b`
- **generator_c3v001**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/verdict_day_runbook_c3/build_runbook_c3v001.py`
  SHA256 `9f018e3b20917a7c777ff901ee70aba87de682aaba2bf6bbc30913c44088d5ff`
- **generator_c3v002**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/verdict_day_runbook_c3/build_runbook_c3v002.py`
  SHA256 `39d25274245a2b9a8010e85d20a251828f4fc273ba94ec89892848a3bf217945`
- **J**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/verdict_day_sheet_addendum_cx3/S0_J_ADDENDUM_CX3V001.md`
  SHA256 `d6bdd5fe8563bfd378ad6cd083d5bfc719f67b5c6c018796f5cee0a2d6251320`
- **V**: `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/VERDICT_DAY_VARS_C2V001.sh`
  SHA256 `49607ea4a8660f296516e610718bb26db303ad19c6c517a9f409ba11be56eff5`
- **dispatch_0304**: `/Users/bgm/Research/UNT_EXCHANGE/FROM_CLAUDE3/0304_2026-10-21_verdict-day-runbook-C3V002-fixes-Codex2-F-STOP-1-fail-fast-in-P0-plus-2-SHOULD_FIX-delta-recheck-requested.md`
  SHA256 `47f98fd95e4c4ca443f6955bdb6d2cc0c480195b0b413196907133f5470ec5a8`
- **prior_stop_finding**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_verdict_day_runbook_cx2/stop_paste/FINDINGS_STOP_PASTE_CXV001.md`
  SHA256 `14317d035b6211b53fb6e1516e3e1b9893db1cbf234f0ada087ebd2d16a948e1`
- **Static comparisons (13/13 passed)**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_verdict_day_runbook_cx2/c3v002_delta/stop/STATIC_STOP_DELTA_CXV001.json`
  SHA256 `d20436de8adf32a7b9d515fae37a0d5f13592abe6430843c95559ea95519e98a`
