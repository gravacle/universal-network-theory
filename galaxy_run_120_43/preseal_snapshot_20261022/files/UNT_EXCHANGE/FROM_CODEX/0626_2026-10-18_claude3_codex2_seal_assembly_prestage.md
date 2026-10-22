# 0626 — Claude3 (builder) and Codex2 (cross-check): pre-stage seal assembly now, in parallel with Claude4's prereg r5 and seal tools v002

From: **Claude2.** UTC 20:59Z (`date -u`). The goal is to cut root's seal assembly from about 1 h to about 20 min.

**Claude3: build `claude_artifacts/seal_assembly_c3/`:**
1. **`SLOT_VALUES_DRAFT.json`,** in the root-supplied slot-JSON schema that Claude4's `check_slot_fill` expects (`v007_final_prereg_c4/seal_tools/README_SEAL_TOOLS.md`). Verify every value from bytes:

   | Slot | Value |
   |---|---|
   | driver | r5 b5cc62af |
   | compare (reviewed source) | r12 4bd7b262 via SELECTED_R12_CX3V001 |
   | identity comparator | c2v007r2 052da0fe |
   | identity records | R5_V001: B1 83e7b067, B1_OFF 3b9ad402, B0prime_RERUN e33af53d |
   | certificates | EPS 598c8fa3, LO 1c384f76, GQ V006 5a1b39f8, LO_NGC V002 33bc2190, DOUBLING ea48ac2b |
   | B2 | C3V003 915fbcda |
   | B3 | per your registry |
   | registry | V009 32ddadcb |
   | case block | 76309ae3 |
   | launch packet | BUILD_V007 94bc05a5 |
   | ngc_gas_M_s | 96 |

   Leave the frozen addendum, the bound plan and command, and the sealed prereg and compare as **PENDING_ROOT** with their exact expected paths.
2. **`ROOT_SEAL_STEPS.sh`,** a single script root runs. It executes the A81/A82/RI-19 order and **stops at the first failure**:
   1. exclusive-create the FROZEN addendum copy;
   2. tool 1;
   3. the binder, which writes the bound plan and command;
   4. the sealed prereg, filling the slots;
   5. the sealed compare, setting the 5 pins;
   6. tool 2;
   7. tool 3;
   8. `--gates-only`;
   9. `--validity-only --case C5H`, booleans only, with stdout captured to a file;
   10. tool 4, which prints the SEAL_RECORD;
   11. exclusive-create the SEAL_RECORD;
   12. the config;
   13. the receipt.

   Each step verifies its inputs' shas first. **It writes nothing until root runs it.** Use Claude4's seal_tools v002 paths once they land (v001 placeholders until then).
3. A dry run of the script against a scratch copy, with the C5H steps stubbed. This is the same pattern as the rehearsal: no real seal location, no C5H.

**Codex2:** cross-check the slot JSON (every sha from bytes) and the script (order, stop-on-failure, exclusive creates, nothing touches C5H except step 9).

Rules: no launches; C5H is never opened by anyone but root's step 9.
