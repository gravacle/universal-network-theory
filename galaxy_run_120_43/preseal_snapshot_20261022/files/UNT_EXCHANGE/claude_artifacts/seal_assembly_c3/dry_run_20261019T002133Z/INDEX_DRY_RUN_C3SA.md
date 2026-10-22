# INDEX: dry run of the SELECTED tuple (ROOT_SEAL_STEPS_c3v014.sh) with the REAL prereg r6, Claude3

Written 2026-10-19T00:25:27Z (`date -u`). Root script `ROOT_SEAL_STEPS_c3v014.sh` `0775e5c5002bf3d46874a37338ec1da731211d174939b1a0879a4ed5d2c3e8c7`; helper `tools/seal_steps_c3sa_c3v014.py` `f41dd02f28ea46f227712fc0774e6a9069eafdc160a98438a3e8bbc6759ec931`; runner c3v003 `2b040e94…`; fence c3v003 `9c62ad49…`; slot draft `c93691f5…`. The text of record is the **real** prereg r6 `d28c95f5…`, named by the **real** `SELECTED_R6_C4V001.json` `7200acd9…`, and nothing stands in for it. V005 is the FINAL `c01b3c51…`. Setup `tools/setup_dry_run_c3sa_c3v005.sh` (`08f14e96…`); generator `tools/make_dry_run_c3sa_c3v007.py` (`a0b87736…`): S01–S18 and S21 only (the v003 stand-in). Shim `tools/dryrun_tool_shim_c3sa_c3v005.py` (`e595b088…`): the text-of-record constant is r6.

**Nothing was created in any real seal location.** `/Users/bgm/Research/UNT_INTERNAL_RUNS` is still absent.
- **Step 9 was STUBBED and never executed.**
- **Fence refusals: 0.** The pycache prefix stayed empty.

| step | pass A (faithful) | pass B (S16 shim, r6 constant) |
|---|---|---|
| 0: check-tor (role `text_of_record`), `selected-roles` (addendum copy, case block, IMPL of record, closed V005), r6 binds the case block | PASS | PASS |
| 1 FROZEN (c01b3c51, 143,081 bytes) / 2 dispositions (r6: `entries: []`, later and changed both empty) + v001 tool 1 + re-hash / 2a | PASS | PASS |
| 3 (+C-05/C-06) / 3a / 3b C-04 (A107 exclusions; 9 admitted) | PASS | PASS |
| 4 / 4a C-02 + tool 3 | 4 PASS, C-02 PASS, tool 3 **REFUSE** `TEXT_OF_RECORD_NOT_R4` (v001 placeholder; expected). STOPPED. | PASS |
| 5, 5a / 8 (+C-03) / 9 / 10 (+C-02) / 11 / 12 (+W7-S1) / 13 / summary | not reached | PASS / PASS / **STUBBED** / PASS / PASS (b2dfd2bf) / PASS (42a97cbc) / PASS (c9baf56f) / PASS (text-of-record pin and the exact E_R6_1 text recorded) |

| file | sha256 |
|---|---|
| passA/SUBSTITUTION_A.diff (50 changed lines) | 24b7113fc61651c2f5437aa91d64c97775e52be8c8d2ab1ae5404d70ecf13399 |
| passB/SUBSTITUTION_B.diff (54 changed lines) | 58d3660d7ebe356788cd30def15694276c826670a7928ee79f295a5c34826ab4 |
| passA/ROOT_SEAL_STEPS_DRYRUN_A.sh / passB/…_B.sh | fd458262372377129bf7b239cc87aeb5ed651c300e4b492c1456bf04493c649a / e30f4af42cf7c087e016e5892dc30c8b0cd74a982924fb547e1094973cac75db |
| passA/SUBSTITUTIONS_A.json / passB/SUBSTITUTIONS_B.json | ba92eeadd3ef86050dce0ab7fee94bf0fe521a31291ad4b4ec1e94355f90102b / 115da3a23cb6c8e826a361b55b6969b51cd28e4709965538731fa46cd19c4b86 |
| passA/RUN_A.sh / passB/RUN_B.sh | d554ed251be69cd90761f3003a9e02eca112d095493174e1c9a03d7b467a90cf / 4d518a6e72851f97c3175fc1e36f8d27903e1a8ae868c536ce3ee07d7fb627ce |
| passA stdout / stderr | 0f0fea4007cfa202320e12cbd4024185a9ed4b9669a0405612952fa72d97d367 / 8000d1bd9e8645d22edb6766210d892d461f293f9b456b64451532136251549e |
| passB stdout / stderr | 026500cf6c342bd91eda83fec58a110a5a2d4e94a9887f2931690b85bb63034e / 7687bcba8d0d5cc2c927bb1f20288ef27f8aef619507fa8fee3c4417de749c43 |
| fixtures: dispositions (r6, `entries: []`) / v003 SELECTED stand-in | ed7aa568233f1e4a5250dbff2d41907b617045a4faa967ef27cb1c2998f9a9be / ad1ced7f… |
