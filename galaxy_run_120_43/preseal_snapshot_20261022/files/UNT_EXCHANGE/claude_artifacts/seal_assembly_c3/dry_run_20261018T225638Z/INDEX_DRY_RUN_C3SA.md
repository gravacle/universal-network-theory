# INDEX: dry run of the SELECTED tuple (ROOT_SEAL_STEPS_c3v010.sh), Claude3, FROM_CODEX/0642 (A105)

Written 2026-10-18T22:59:56Z (`date -u`). Root script `ROOT_SEAL_STEPS_c3v010.sh` `2b9d02fa34b06c4c672c58617a9e93e5bacca26924405106e462d2af397cecef`; helper `tools/seal_steps_c3sa_c3v011.py` `7caad125be19160c6e431dcf6be8f038cb9bba172c95f1f8059ebcdd938a0aff`; runner `tools/run_pinned_c3sa_c3v003.py` `2b040e94…`; fence `tools/fence_c3sa_c3v003.py` `9c62ad49…`; slot draft `c93691f5…`. The open V005 at setup was `18fd9a83b23c61f227a88df42e4f7a374dae5f91be3a3e18fafa6fdcc3557787` (A105 newest). Set up and run by `tools/setup_dry_run_c3sa_c3v002.sh` (`1af1128c…`) with generator `tools/make_dry_run_c3sa_c3v004.py` (`bb91cb1d…`).

**Nothing was created in any real seal location, and the real step-2 output root was never created.** `/Users/bgm/Research/UNT_INTERNAL_RUNS` was still absent after both passes (lstat). Every output is under `passA/` and `passB/` here.
- **Step 9 was STUBBED and never executed.** Step 8 ran fenced, with `C5H_REGISTERED_RUN_DIRS` redirected to a stand-in; the stand-in manifest names no case and no run tree.
- **Fence refusals: 0** (step 2a in both passes; step 8 in pass B, where `fence_events` is empty and the compare's rc is 0).
- **The pycache prefix stayed empty** in both passes.
- RP-S1 ran on the scratch root `passX/scratch_internal/UNT_INTERNAL_RUNS/V007_STEP2_R5_BUILD_V007`. Its parent was absent at setup, as on disk, so the parent was created and then the root exclusively. The root was verified as a real directory with realpath equal to the literal, `st_dev` 16777232 equal to /System/Volumes/Data, and empty, and it was still empty and the same inode at the end (pass B summary).

| step | pass A (faithful: v001 placeholders) | pass B (S16: tools 3 and 4 via the dry-run shim) |
|---|---|---|
| 0 preflight (now also: one text-of-record pin with its derived table bytes; RP-S1 check mode on the root) | PASS | PASS |
| 1 FROZEN copy | PASS (18fd9a83) | PASS (18fd9a83) |
| 2 dispositions (v003 object, A102-A105, labelled fixture b1e59eaf) + tool 1 + re-hash | PASS | PASS |
| 2a driver BUILD record | PASS (d9226430) | PASS (d9226430) |
| 3 template outputs (41 fresh) + **RP-S1 output root created and recorded** + binder | PASS | PASS (parent created; root st_ino 14242172; 451.67 GiB free) |
| 3a final slots / 4 sealed prereg | PASS | PASS (a0796691 / 4798af24) |
| 4a tool 3 (after B4) | **REFUSE** `TEXT_OF_RECORD_NOT_R4` (v001; expected). STOPPED. | PASS |
| 5 sealed compare / 5a tool 2 | not reached | PASS (fcd1cbe8) |
| 8 --gates-only, fenced | not reached | PASS (sealed mode, test_mode False; fence 0) |
| 9 --validity-only --case C5H | not reached | **STUBBED** (b4e84612 booleans fixture) |
| 10 tool 4 / 11 SEAL_RECORD (= tool 4 stderr sha) | not reached | PASS (9873d749) |
| 12 config + guard v008 self-check + **W7-S1 re-check of the written config** | not reached | PASS (875ea38a; 15 rows, byte-equal, in table order) |
| 13 receipt / summary (+ RP-S1 verify: still the same empty root) | not reached | PASS (a9e9810a) |

## Substitution set (published; the diffs are the exact text)
S01–S16 are as in dry runs 6 and 7: the scratch outputs; the byte-identical binder copy; the status flag; the v001 bare-name dispositions form (S08, dry run only); the stand-in gates manifest; the draft-path and config-path flags; the step-8 dryrun fence and stand-in; step 9 stubbed (S15); and, in pass B only, S16, the dry-run shim for tools 3 and 4 (`tools/dryrun_tool_shim_c3sa_c3v004.py` `5f76c4be…`; not a seal tool). This run adds two:
- **S17:** `OUTPUT_ROOT_TO_CREATE` is a scratch path (`passX/scratch_internal/UNT_INTERNAL_RUNS/V007_STEP2_R5_BUILD_V007`).
- **S18:** `OUTPUT_ROOT_IS_TEMPLATE_ROOT=0`. The template's output strings stay the real ones, are only checked absent, and nothing is created there.

| file | sha256 |
|---|---|
| passA/SUBSTITUTION_A.diff (48 changed lines) | c327551d6754737f5d82a60c6e0314c5245f6c41e2a7aea568115198e54d2295 |
| passB/SUBSTITUTION_B.diff (52 changed lines) | 8ffaed38d0a39af88274ac772de306a627969f5155d46353340eef352f1930f4 |
| passA/ROOT_SEAL_STEPS_DRYRUN_A.sh / passB/…_B.sh | 03b6e4dc3b037dd8c43a7895671f0217fd746ea12ba585a22587a09b8035b8a9 / 588a7838a97b840c2f0583aa5292ee7026f278aea8f307a59d2cdc8947a0ee18 |
| passA/SUBSTITUTIONS_A.json / passB/SUBSTITUTIONS_B.json | 67e686cf675a0341640a7ffc01a01144273b1a80d554b3fe6a33eec739ae0a32 / 625b21aaf608cc1ae20dc89126a9ddd59986390a3495e8e8364e2ed40665f66b |
| passA/RUN_A.sh / passB/RUN_B.sh (labelled stand-in root inputs) | 5edc4c063e67d2cf8c8b0801f1f66a70359bbffe62d2cbc73ab98dbf50733064 / f0382e2eb20bd2b09a4afbda3ebfe5d96b118733daf04ea0e542c97c1d1d31cf |
| passA stdout / stderr | caa12a90b8ce10fa666c4c8fc0ec31748ee90ea6f27163b02a2471409daf0091 / 66bb90aecd876b0b1f6f3ed36a165318c98bc0720ec8cefc9f1211caf94b2414 |
| passB stdout / stderr | 21fbe3fe3025785c289992c8e1de1e543a1f40315a1bdb70e349843882cf7d77 / 79e597d4307d6419310f1029b74406af48981906b613c3db79a78949fa6ef521 |
| fixtures/_DISPOSITIONS_V003_OBJECT.tmp.json (labelled FIXTURE, not dispositions of record) | b1e59eaf6d858884be5c7c07e08b7ed58441f2144685d791fc4814cbb68f2a02 |

The previous run, `../dry_run_20261018T225153Z/`, used script c3v009 and helper c3v010; both are superseded (see README c3v003). Its results matched this run step for step.
