# INDEX: dry run of the SELECTED tuple (ROOT_SEAL_STEPS_c3v007.sh), Claude3 fix round 0639/0640

Written 2026-10-18T22:25:15Z (`date -u`). Root script `ROOT_SEAL_STEPS_c3v007.sh` (`e7409d93d17cdcde0e113ba971233fb59ade77157e2fe0b4a0c91f6b20b985cb`); helper `tools/seal_steps_c3sa_c3v009.py` (`000798141398d27308d95e7a25fc64d17abe9831c47a2b27457439b7bc7922a3`); runner `tools/run_pinned_c3sa_c3v002.py` (`b57e4859c498bf57e05706dcd83d89db0f14102c33aec7359580c155d924861c`); fence `tools/fence_c3sa_c3v003.py` (`9c62ad49…`); slot draft `SLOT_VALUES_DRAFT.json` (`c93691f5…`, unchanged). The open V005 at setup was `acb7f44a…`, with A104 the newest entry.

**Nothing was created in any real seal location.** Every output is under `passA/` and `passB/` here.
- Step 9 was **STUBBED and never executed**.
- Step 8 ran the scratch-sealed compare in-process, behind a fence armed before its bytes executed. `C5H_REGISTERED_RUN_DIRS` was redirected to a stand-in, and the stand-in manifest names no case and no run tree.
- **Fence refusals: 0** (step 2a in both passes, step 8 in pass B).
- **Every Python process ran with `-X pycache_prefix=<seal folder>/NO_PYCACHE_PREFIX_EMPTY`.** The folder is still empty in both passes, and no `__pycache__` was created.
- Every seal tool, the binder and the step-9 slot ran through the pinned-source runner.

| step | action | pass A (faithful: v001 placeholders) | pass B (S16: tools 3 and 4 via the dry-run shim) |
|---|---|---|---|
| 0 | preflight (seal folder absent before any Python; pins; inputs) | PASS | PASS |
| 1 | B1 FROZEN copy | PASS (acb7f44a) | PASS |
| 2 | dispositions v003 object (A102, A103, A104) + tool 1 + re-hash | PASS | PASS |
| 2a | driver BUILD record (r13 builtin + CHECK.md) | PASS (d9226430) | PASS (d9226430) |
| 3 | pre-binding check + binder via the runner | PASS | PASS |
| 3a | final slots | PASS | PASS (afb3d67c) |
| 4 | B4 sealed prereg | PASS | PASS (aeb13ef9) |
| 4a | tool 3 check_slot_fill (after B4) | **REFUSE** `TEXT_OF_RECORD_NOT_R4` (v001; expected). STOPPED. | PASS |
| 5 | B5 sealed compare (5 pin lines) | not reached | PASS (d4be19a4) |
| 5a | tool 2 check_sealed_compare (after B5) | not reached | PASS |
| 8 | --gates-only, fenced | not reached | PASS (sealed mode; 13 registered records PASS; fence 0) |
| 9 | --validity-only --case C5H | not reached | **STUBBED** |
| 10 | tool 4 build_seal_record | not reached | PASS |
| 11 | SEAL_RECORD (sha = tool 4 stderr) | not reached | PASS (95c1c7ee) |
| 12 | config + guard v008 admission() self-check | not reached | PASS (d0951473; 15 sources) |
| 13 | receipt | not reached | PASS (5328cb22) |

## Substitution set (published; the diffs are the exact text)

S01–S05 move the output paths into scratch. S06 is the byte-identical binder copy (the same sha). S07 is the status flag. **S08:** the single `--dispositions` line becomes the v001 bare-name form, because only the v001 placeholders exist. S09 is the inputs folder. S10 is the stand-in gates manifest. S11/S12 are the draft-path and config-path expectations. S13/S14 set the step-8 dryrun fence mode and its stand-in. **S15:** step 9 is a stub. **S16 (pass B only):** tools 3 and 4 run through `tools/dryrun_tool_shim_c3sa_c3v003.py` (`154dc9ca…`). The shim is the pinned runner plus two constant patches: text of record r5, and `ddo_gas_M_s` for D-01. It is **not a seal tool**.

| file | sha256 |
|---|---|
| passA/SUBSTITUTION_A.diff (44 changed lines) | a07717eff836b035fdc15f267413c8907b0c264ef2e8756d932464c7ddb1c73f |
| passB/SUBSTITUTION_B.diff (48 changed lines) | fab61d236eac4365767be9ebe9562f6ff96e3cbf314bb630ba9b8f739bb25e4a |
| passA/SUBSTITUTIONS_A.json / passB/SUBSTITUTIONS_B.json | b87c94eeadda30a83001f5d798fdafe29b8bc812fec7a2ff78a18c4916211e5c / c9cf168ccc1e57e562ced156da7a5a44b2814fcd130b6e2949b14cde5ec4b9c9 |
| passA/ROOT_SEAL_STEPS_DRYRUN_A.sh / passB/…_B.sh | dd2651eb1cb200e5aba7b2f964237d7b3e3de81761cc9d288a7f9def23d196ad / 4f0d2720ac4e3cb4dcf220b616ebc828fb8787e618d82e334fac7b670fcbefb4 |
| passA/RUN_A.sh / passB/RUN_B.sh (labelled stand-in root inputs) | 136737ad605a8e31972746ec804c65d2bb8f7f98a3369306c8b72967556f19c6 / 7f67102c71ab5c20f4f751e720ec68e6f43dc0998d03939fc1642ca554c438c6 |
| passA stdout / stderr | 1f826312ca79c556d5377531719bd03b9f7ec874f8ca2884359771d3028f6e65 / cfb0fcd8947df460cd6213f1cb18f0940f2b6a7fa7f6ee76de0d2dd697f3efcd |
| passB stdout / stderr | bb22aebf22c37a2bea19906ef162784dd5e7a602008ecba96c536fb79292c72c / 1438d66586e1ccd425ccf5bb67880e1cc0a6739d2fe9d7c6b94d4f3ee8a35639 |
| passB dispositions fixture (v003 object, labelled FIXTURE) | 1250e0fb22b8638268e9a76586ed700d7a25a34673f25d8349862ff2418fb3ab |

The MUST_FAIL controls for B1, B2 and B3 are in `../mustfail_20261018T221642Z/`. Its results are `MUSTFAIL_RESULTS_C3SA.json` (`1d07745a…`), `b2/B2_RESULTS_C3SA.txt` (`43476148…`), `b2/B2_RESULTS_RUNNER_C3V002.txt` (`dc653945…`) and `b2/B2_RESULTS_RUNNER_C3V002_TOOLLIKE.txt` (`443f5de3…`).
