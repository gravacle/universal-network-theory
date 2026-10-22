# INDEX: dry run of the FINAL tuple (ROOT_SEAL_STEPS_c3v016.sh) with the REAL prereg r6 and the REAL seal tools v003, Claude3

Written 2026-10-19T01:16:06Z (`date -u`). Root script `ROOT_SEAL_STEPS_c3v016.sh` `dcdb746c76546169bc0b4702c832265b59115c552480f248bdd5c3f354f0a6e8`; helper `tools/seal_steps_c3sa_c3v016.py` `21f0eb09e927722237459d65cf60eae79d92acf4c6a25bb4340f1519e66d28c0`; runner c3v003 `2b040e94…`; fence c3v003 `9c62ad49…`; slot draft `SLOT_VALUES_DRAFT_c3v002.json` `02d97c37…` (C4V002). Text of record: r6 `d28c95f5` via `SELECTED_R6_C4V001` `7200acd9`. Tools: v003 via `SELECTED_SEAL_TOOLS_V003_C4V001` `cf7e5b2f`. Setup `tools/setup_dry_run_c3sa_c3v009.sh` (`af35cd57…`), generator `tools/make_dry_run_c3sa_c3v008.py` (`0c2c0201…`), shim `tools/dryrun_tool_shim_c3sa_c3v007.py` (`df19ac11…`).

**Both passes run every step with the real v003 tools.** Step 9 was STUBBED and never executed. Fence refusals: 0. The pycache prefix stayed empty. The real `/Users/bgm/Research/UNT_INTERNAL_RUNS` is still absent.

**The published substitutions:**
- **S01–S06, S09–S14, S17, S18:** scratch outputs and the binder copy; the stand-in gates manifest; the fence mode; the scratch output root.
- **S15:** the step-9 stub writes a booleans stdout fixture plus a labelled B6-form `VALIDITY_ONLY.json` (cases C5H, `valid: false`).
- **S16 and S16b (both passes), the D-10 allowance only.** A dry run never writes the real FROZEN `path_to_be`.
  - The direct tool 1 run gets its own `--allow-open-copy-for-dry-run`.
  - Inside tools 3/4, the shim passes `allow_open=True` to tool 1, and turns tool 3's single code `FROZEN_SLOT_NOT_PATH_TO_BE` into the note `DRY_RUN_D10_FROZEN_SLOT_PATH_ALLOWED`.
- **S23 (pass B only):** the tools get no dispositions file.

**The fixtures (labelled):** the dispositions object (`entries: []`), the cascade-map addendum naming CASCADE_MAP_R5_C2V001 `a7281e10`, and the three B7 inputs in the v003 C4V002 forms.

| step | pass A (tools get the pinned `entries: []` file) | pass B (S23: no dispositions file) |
|---|---|---|
| 0: C-02 role `text_of_record`; r6 roles; v003 roles (8); RP-S1 check | PASS | PASS |
| 1 FROZEN (sha + length) / 2 v003 tool 1 (`--expect-frozen-sha c01b3c51`, `--addendum-at-text-of-record`) | PASS (notes: DRY_RUN_FROZEN_PATH_NOT_PATH_TO_BE, DISPOSITIONS_VERIFIED) | PASS |
| 2a v003 tool 5 → copy-exclusive → helper check-driver-build-record | PASS (record `25b4ff69…`, the README's tool 5 bytes) | PASS (`25b4ff69…`) |
| 3 / 3a / 3b C-04 / 4 / 4a C-02 + v003 tool 3 | PASS | PASS |
| 5 / 5a v003 tool 2 / 8 + C-03 / 9 STUBBED | PASS | PASS |
| 10 C-02 + v003 tool 4 build (schema `UNT_V007_SEAL_RECORD_C4V003`, `text_of_record_pinned_by: ROOT_ARGUMENT`, B2 block) | PASS (`later_entry_dispositions` pin `ed7aa568`) | PASS (`NOT_SUPPLIED_NONE_REQUIRED`) |
| 11 SEAL_RECORD / 12 config + W7-S1 + **v003 tool 4 `--check-admission-config` (B8)** / 13 receipt | PASS (2da845c1 / 6ed79761 / c92b0fb2) | PASS (d7821ddf / c094dbf7 / 69fe9500) |

| file | sha256 |
|---|---|
| passA/SUBSTITUTION_A.diff (60 changed lines) | 47e0b5ff837aa647bccee5c42a24597a20fa8407299f4287c7dde89910ab315f |
| passB/SUBSTITUTION_B.diff (62 changed lines) | d806b03f84fbdca55a8f6fd79772d5442e75ea1673b7df14d83d999e06257324 |
| passA/ROOT_SEAL_STEPS_DRYRUN_A.sh / passB/…_B.sh | c759e0b9e7f0456461d8494652916279374bcf95103d3ff1d3b57473f50e7293 / bad16d59d281641e2388de992ab337758f8f89a97e6b1e1a31ef83eac1a8d9c5 |
| passA/SUBSTITUTIONS_A.json / passB/SUBSTITUTIONS_B.json | 253eb9e6ccf5c64132a4fcb0a6d1b4aad35171c6a09d5eca0e3466549b169a9c / 0c72bb08fe0e0c4461ff658adf3ced77ac71505875dd868a191f7e8c6e8f50f2 |
| passA/RUN_A.sh / passB/RUN_B.sh | ad0fcff922a814710aea6c32a9609fa023d7053ab5890b8c3ebef299e736fcbb / 26759cd3d16eaa38353732933e21c5dbddf644ce5e1011f460f37c87ab72133b |
| passA stdout / stderr | a9a4335ab8437a34e22a53fc13d228b87b30c3ecb36e7207906e510b62cf2286 / 1224b15b789d654f335afb6354cb4eeaa2f947492261bc028feab7c08037cfc3 |
| passB stdout / stderr | 347c8de45f5fc66f9de951ec4909446768122f3753b9e79feaafe08b57677b08 / a6e52d07d901ecf89608a2c976ee0037fb6bb87e8f36216fe16e995e4ac7c781 |
