# INDEX: dry run of the SELECTED tuple (ROOT_SEAL_STEPS_c3v013.sh), Claude3, FROM_CODEX/0644 (A107)

Written 2026-10-19T00:12:21Z (`date -u`). Root script `ROOT_SEAL_STEPS_c3v013.sh` `c1a469e98c842af37a4c8886459f4f2e2262053ea8848eebdf4a432dc5d641cd`; helper `tools/seal_steps_c3sa_c3v013.py` `ad581a06854ad5ce0e337624860cdf07c04181fccb066f71e79128f1d9b05200`; runner c3v003 `2b040e94…`; fence c3v003 `9c62ad49…`; slot draft `c93691f5…`. The open V005 is the FINAL `c01b3c51…` (143,081 bytes). Setup `tools/setup_dry_run_c3sa_c3v004.sh` (`41cdc93a…`); generator `tools/make_dry_run_c3sa_c3v006.py` (`f00073fb…`): S01-S21, **no S22**, since A107 rules the C-04 exclusions.

**Nothing was created in any real seal location.** `/Users/bgm/Research/UNT_INTERNAL_RUNS` was still absent afterwards.
- **Step 9 was STUBBED and never executed.**
- **Fence refusals: 0** (steps 2a, 3b and 8). The pycache prefix stayed empty.
- r5 and two labelled SELECTED fixtures stand in for the unpublished r6 and v003 (S19–S21).

| step | pass A (faithful) | pass B (S16 shim for tools 3 and 4) |
|---|---|---|
| 0 / 1 / 2 / 2a / 3 (+C-05/C-06) / 3a | PASS | PASS |
| **3b C-04** with the A107 two-entry exclusion list | **PASS**: 9 records admitted with their gate pass verdicts; EPS_NGC and I1T_NGC excluded and reported | **PASS** (same) |
| 4 / 4a C-02 + tool 3 | 4 PASS, C-02 PASS, tool 3 **REFUSE** `TEXT_OF_RECORD_NOT_R4` (v001; expected). STOPPED. | PASS |
| 5, 5a / 8 (+C-03) / 9 / 10 (+C-02) / 11 / 12 (+W7-S1) / 13 / summary | not reached | PASS / PASS / **STUBBED** / PASS / PASS (fb8dd5ef) / PASS (9907f647) / PASS (4c9ebefe) / PASS (output root still the same empty directory) |

| file | sha256 |
|---|---|
| passA/SUBSTITUTION_A.diff (54 changed lines) | f35bf284b09114a2af96fe81623517e9e990de11f85df022551da7e61ff55fee |
| passB/SUBSTITUTION_B.diff (58 changed lines) | b66086a73ee75127a96a667f64952be54e1b2de4f93ecde294cccadd9af70ad1 |
| passA/ROOT_SEAL_STEPS_DRYRUN_A.sh / passB/…_B.sh | a30491ea400ee325ba4d63d6219d07df9ababfaef45c626dbfc6991f87d936ef / af8d9d50d5c9ea441cdc26cfac1464e653ef68879dc9e9d2986bb9c8eeb607a5 |
| passA/SUBSTITUTIONS_A.json / passB/SUBSTITUTIONS_B.json | e946a56dce1fe66d24c2d794cfe300dba4dddc46f1898c3e6abfde9a1948ff83 / d6b47e03a87375b0a4817bea21739111503d89707134cf28a6ca47284fe3d032 |
| passA/RUN_A.sh / passB/RUN_B.sh | d13696626f35ff7166db72c0d8d2790ac4b89a170dbf6a5fce7680b2d22df4c5 / a314298d2041156d88beebda7fb9a4583f327a953ec629f4c6807bba9dbe4c2b |
| passA stdout / stderr | 88b5802091112673e1326e99be6cdd98eb6132dcc9d49a76301f71843dee9d40 / 5f3e2f4f024216ea9423b86dea6d0b6628f1249d130b8f06f40cb510d4479be5 |
| passB stdout / stderr | 74fd5a19e8bd5caa6c013f87b68f438739fcd3bf0bc47888e24e4d799e3407c5 / db8edf74294e2bd5413dd5b919e49c92512e8f49369b88335e015c17ea01ce14 |
| fixtures: dispositions (A102-A106) / r6 SELECTED stand-in / v003 SELECTED stand-in | df2fdf74… / 30f6f63e… / ad1ced7f… |

The previous run, `../dry_run_20261019T000226Z/`, used script c3v012. It had the same outcomes; c3v013 changes only `tor_table_bytes`.
