# INDEX: dry run of the c3v009 tuple (ROOT_SEAL_STEPS_c3v020.sh) with the REAL seal tools v004 and both disclosure flags, Claude3

Written 2026-10-19T02:59:11Z (`date -u`).

**The tuple under test**

| role | file | sha256 |
|---|---|---|
| root script | `ROOT_SEAL_STEPS_c3v020.sh` | `36058df84bb2088970be442bc64445a4c6939b45df3e9cb3294cedef62c65ac0` |
| helper | `tools/seal_steps_c3sa_c3v019.py` | `91b15dc688a2c28e1b5362d9568a80f92431938eb5e2807367b2327a37290cbf` |
| runner / fence | c3v003 | `2b040e94…` / `9c62ad49…` |
| slot draft | `SLOT_VALUES_DRAFT_c3v003.json` | `e12292a2…` |

- **Tools:** all five from `seal_tools_v004`, pinned from `SELECTED_SEAL_TOOLS_V004_C4V001` `593c59fa`. Tool 4 is `build_seal_record_c4v004.py` `9787cf58`.
- **Disclosures:** root's V002 `a0284ece` (A112).
- **Dry-run tooling:**
  - setup `c3v009_prestage/tools/setup_dry_run_c3sa_c3v013.sh` (`c44220306a34ecf7b2ff3cdb2d13b32643acd0c0aef9d94fc3e7690c7f1585e9`);
  - generator `c3v009_prestage/tools/make_dry_run_c3sa_c3v010.py` (`ab01df67…`): no S24 or S25, no stand-in;
  - shim c3v007 (`df19ac11…`): the D-10 allowance only.
- **Gate before the passes:** the tool-4 import/RUN-FORM/CLI check c3v003 returned PASS on the real v004 bytes.

**Both passes: ALL STEPS PASS (32 PASS lines each).**
- Step 9 was STUBBED and never executed.
- Fence refusals: 0. The pycache prefix stayed empty.
- The real `/Users/bgm/Research/UNT_INTERNAL_RUNS` is still absent.
- Step 10's tool-4 call carries `--manual-disclosures "$DISCLOSURES" --manual-disclosures-sha256 "$DISCLOSURES_SHA"` exactly once in each pass's script.

**Substitutions:** S01–S06, S09–S14, S15, S16, S16b, S17 and S18; S23 in pass B only.

| step | pass A | pass B |
|---|---|---|
| 0: check-tor, r6 roles, check-disclosures (V002), the v004 roles (10, one file), A111 draft checks, RP-S1 | PASS | PASS |
| 1–3a, 3b C-04, 4, 4a C-02 + tool 3, 5, 5a, 8 + C-03, 9 STUB | PASS | PASS |
| 10: C-02 + tool 4 v004 build with both flags | PASS | PASS |
| 11: SEAL_RECORD (schema `UNT_V007_SEAL_RECORD_C4V004`) + **R-02** `STEP_11_DISCLOSURES_VERBATIM` | PASS | PASS |
| 12 config + W7-S1 + tool 4 v004 B8 / 13 receipt / summary | PASS | PASS |

**What each record carries.** `manual_disclosures`, at `manual_disclosures.content` (object) and `.raw_text` (text):
- `pin` = V002's path and sha;
- `raw_text` sha256 = `a0284ece…`;
- `content` with the row `A106_2_SRR13_CHECK_SPLIT`.

**The setup's diagnostic line.** It searched the records for V001, because a V001 path was hardcoded in its diagnostic. It found **no** V001 copy, which is correct. The V002 locate is in the README.

| file | sha256 |
|---|---|
| passA/SUBSTITUTION_A.diff / passB/SUBSTITUTION_B.diff | 2b2fffb3130bffad8b8622b00b2f7600396e0e957d3373d9d5020596799951c2 / 2e30731d7115060abc137e3ceac088c86b3d5918d7745045df2068f3d6fbaaca |
| passA/ROOT_SEAL_STEPS_DRYRUN_A.sh / passB/…_B.sh | a4bb6142039141e649765bead498a6a76333069a79077eaf394b1978827c4d7c / a801f4b5bd4fe9d2cb2bc58f0a5f862cbaadd6f13bcade5e3773076529eb0c45 |
| passA/RUN_A.sh / passB/RUN_B.sh | 7d4e42756eb88d8a22f229b307d1dd3ccd4e775d46b91d46ff0508af5b13bb57 / 34ca251f33db8dce051d6a6e91a533af35b11a8b9d68f3b0f991b681f9f25444 |
| passA stdout / stderr | 5ed7f5c2c7dd34bd401e6019bbe77c9975278ce289767dfcff1aeca785a7b6ac / dfcdde9b2bb94241dfcd22c3c53660600cb5ed5f8dceff535433fd2473c1cc3c |
| passB stdout / stderr | 1c37364b2bc02ea2068260efe9eece2071d3098fccfecdb09363fb6291807e7c / 03661dadc68820a07129864905b97cf031351ceec40210bcd0f9e2a984d46b5e |
| SEAL_RECORD A / B | 01eef4e0f4aaee30c8c6e0c017f9e6e33593f0fda1b5a78f47f899fd164b7550 / 0174ea9503035ddf4b54a51184eac3e8901248d68d5518d47e8188be1bd1dd58 |
| config A / B | e422c8d5a13af311e6373191a297dac81179bbc5c6457a5de1599f966825ee65 / 9f8f26b1389a2adbe5e037bf7ce921c964920c991b0d6ff60d30767ff1f6a4a0 |
| receipt A / B | 8af97cb3b5ab3130d3ab5b16649c90064c4d67a2172649fb29eab85c1f952207 / cf1451d0bde73cef2c528b4ee142e53d514906ab767c8a3ebb890b098e121b0e |
| STEP_11_DISCLOSURES_VERBATIM.json A / B | 42db8f16aceb45690cb8b7e88f20974149180f4678d700d164c356473dc45cc1 / 5d1e08f6b7677cbc137c2d36cc361b68358e321b6b59189b5f7768a1766a1afa |
| summary A / B | e87857f106fb3421ae26bd701bae866073d039089e66c1f123fe9e2b69e3c81d / 704ebe0c3aa58076637f0d8b449a3b58c64092f5d04c1e40a3f3aad94a70b16f |
