# Compare r13 author validation

`date -u`: Sun Oct 18 21:21:35 UTC 2026

**TESTED_PASS: 706/706 author assertions; 0 failed.** Exit status 0; stderr empty. No test expectations changed. Every test ID, ordering, coverage tag, expected value and passing status matches the selected r12 summary.

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r13/kmax_tail_compare_c2v007_r13_cx3v001.py` — SHA256 `f5adfd11ea7ecc982ba7650944f6a6d69eeff8be690bde6265a18d07d3bb2157`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r13/tests_kmax_tail_compare_c2v007_r13_cx3v001.py` — SHA256 `71c7b516bca41a8b0779e5da39704a84d1188bdeeb8f3df4920f843faae7e5aa`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r13/out/author_cx3v001/TEST_SUMMARY.json` — SHA256 `cad67c41fd8b7d56d092ac070fabfe5dc79dce6280e3e7f3e98ccfdbf81dd60c`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r13/AUTHOR_VALIDATION_CX3V001.json` — SHA256 `4f88cae8b967d23e6b0ac25b50016a4f0d48627c3ec79660deedc14b36a8b936`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r13/AUTHOR_706_MAPPING_CX3V001.json` — SHA256 `eb0413c2157be629e98eb1443f56527341c9dbd1cb1f7cedcd2697be12672a76`

The only production AST node changed is `check_record_codes` (1 of 440; the other 439 are unchanged). It parses the JSON candidate with the existing duplicate hook and local `parse_int=str`; only `JSONDecodeError` selects the existing text fallback. A different `ValueError` returns `DRIVER_BUILD_CHECK_RECORD_UNREADABLE`. The exact inverse block substitution reconstructs all parent source bytes. `driver_build_codes`, `activate_driver_build`, `active_build` and comparison CLI admission already delegate to this classifier. Shared scientific `loads_strict` retains numerical integer semantics. Documentation/help labels and the generated field contract remain inherited as required by the single-fix scope.

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r13/SOURCE_DELTA_CX3V001.json` — SHA256 `8275e8d50efdf334ab10f913b62e1e30982f76374f2017eb3d3cdafa3e539645`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r12/kmax_tail_compare_c2v007_r12_cx3v002.py` — SHA256 `4bd7b262caae26f2de146cee803dd689a1f4e565cb67552f04e6d6b97188dd28`

The harness was audited before execution. Six source-path/doc/fixture/field-file replacements preserve the original suite exactly under inverse substitution. Immutable fixture producers and the inherited field-contract baseline are read from r12. Every comparator subprocess is re-entered through the guard, whose AST binding replaces protected identities with inert local stand-ins before any module execution. Guard tripwires deny real UVT/C5H contents and metadata, observed/target data paths, /.vol aliases, deletion/rename and network; writes are confined and exclusive.

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r13/AUTHOR_HARNESS_BUILD_CX3V001.json` — SHA256 `2d5830d73824bd3ac0da3c2176a6734d66a0ad257684140b7b01fe5dc07bd764`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r13/tools/guard_r13_cx3v001.py` — SHA256 `fc69b438eda34fed93e1ce37526a0bd3b8369d44b09d5ca9a2737cee0415ef9d`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r13/tools/author_entry_cx3v001.py` — SHA256 `83b3434136326b05d8dbb6ff2cf158538b97c58f8ea71bc630b1efd40c71e5d3`

Observed 24 completed guard logs, zero denied operations, and maximum per-process RSS 1,016,266,752 bytes (under 8 GiB). The logs and their full byte hashes are listed in the validation record. No scientific launch or production comparison was performed; the suite exercises comparator logic on permitted saved and synthetic fixtures. The separate V01–V07/T01–T19, real-record and mutation evidence is not counted as this lane's 706 checks.

**UNTESTED here:** scientific production execution, future root seal, and cross-lineage adoption.
