# INDEX: dry run of the FINAL selected tuple (ROOT_SEAL_STEPS_c3v008.sh), Claude3 0641

Written 2026-10-18T22:30:12Z (`date -u`). Script `ROOT_SEAL_STEPS_c3v008.sh` `023b2bbf63007ce2ce9e91f053313a40af4c69d57136633c88e8aed4c449b8c9`; helper c3v009 `00079814…`; runner c3v003 `2b040e94a2b74eae981485288471376b86be0784a0a50b59093312c4fd87bf73`; fence c3v003 `9c62ad49…`; slot draft `c93691f5…`. The open V005 was `acb7f44a…`. The substitution set S01–S16 is the same as in `../dry_run_20261018T222335Z/INDEX_DRY_RUN_C3SA.md`; only the shim differs, `tools/dryrun_tool_shim_c3sa_c3v004.py` `5f76c4be…`, derived from runner c3v003.

Nothing was created in any real seal location. **Step 9 was STUBBED, never executed.** Step 8 was fenced, with C5H redirected to a stand-in and no run tree in the manifest. **Fence refusals: 0.** The pycache prefix stayed empty in both passes.

| step | pass A (v001 placeholders) | pass B (shim for tools 3 and 4) |
|---|---|---|
| 0, 1, 2, 2a, 3, 3a, 4 | PASS | PASS |
| 4a tool 3 (after B4) | **REFUSE** `TEXT_OF_RECORD_NOT_R4` (v001; expected). STOPPED. | PASS |
| 5, 5a tool 2 (after B5) | not reached | PASS |
| 8 gates-only | not reached | PASS (sealed mode; 13 registered records PASS; fence 0) |
| 9 | not reached | **STUBBED** |
| 10, 11 (SEAL_RECORD a952e383 = tool 4 stderr), 12 (config 8ce07a16; guard self-check PASS), 13 (receipt 060bc77e) | not reached | PASS |

| file | sha256 |
|---|---|
| passA/SUBSTITUTION_A.diff | fbe590bc84931c47b73b2cc1eacc0bd67dcd4c5d742d77a5bd2d16961d93065e |
| passB/SUBSTITUTION_B.diff | 66b9903733914f045c27edf9e7489ab95339612cae64d62f3d67e84fcb045f54 |
| passA/ROOT_SEAL_STEPS_DRYRUN_A.sh / passB/…_B.sh | 263195400c6f9e0094859bd4e3c8962a8ce7ec1e3a1c1cf8cfcd7bd2c1afbeae / 177b03ad51a2ef1bb878eb244bc2abd7e83f2a87e92d143e2a767154699a9298 |
| passA/SUBSTITUTIONS_A.json / passB/SUBSTITUTIONS_B.json | f770b5ae9b789b2b4e34c79d748f1e23823f569f607e6c57db618d38e55b20e4 / 6d1963ccd35ebe00db0eefd36dda005aa6255617112141cbc1944f3be4cbc649 |
| passA/RUN_A.sh / passB/RUN_B.sh | 4f54f0ca42f3cb95a9c641477cb1f867904cf5d1c358b94986c3680ce80fb257 / 0cc884c40fa960859c90aea5f41459b794de06304d59417dbe0d5ed044e8701f |
| passA stdout / stderr | 1f826312ca79c556d5377531719bd03b9f7ec874f8ca2884359771d3028f6e65 / 427173d146778b3addbbf1f54435d363aa72b41a1be1191104cff145df26dce4 |
| passB stdout / stderr | 3d6beae2345057f9a5a1bc150897c86f20a4bc0786229cd2ebf3201df49d8937 / 7812b65e792e32e4ce945763900a876cb24974065d87ff601836630a015b2922 |
