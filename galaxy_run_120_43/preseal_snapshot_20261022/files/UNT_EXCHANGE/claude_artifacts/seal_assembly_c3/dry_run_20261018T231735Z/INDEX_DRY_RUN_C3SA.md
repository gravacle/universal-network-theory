# INDEX: dry run of the SELECTED tuple (ROOT_SEAL_STEPS_c3v011.sh), Claude3, FROM_CODEX/0643 (A106)

Written 2026-10-18T23:22:37Z (`date -u`). Root script `ROOT_SEAL_STEPS_c3v011.sh` `af74e9bde45a5ec0d082ed61f61261757986f1796ebf448746355bf1871111dc`; helper `tools/seal_steps_c3sa_c3v012.py` `b13483966fcb8755608d73e05c0e70dc94e39a2b07635f54efc0c86849748bac`; runner c3v003 `2b040e94…`; fence c3v003 `9c62ad49…`; slot draft `c93691f5…`. The open V005 is the FINAL `c01b3c51e34501d77e474594cc0b4be72c6e068c7f58a595055316313a8d4bb1` (143,081 bytes; A106 is its last entry). Set up and run by `tools/setup_dry_run_c3sa_c3v003.sh` (`1dc0c5af…`) with generator `tools/make_dry_run_c3sa_c3v005.py` (`03f16bef…`).

**Nothing was created in any real seal location.** The real step-2 output root was never created: `/Users/bgm/Research/UNT_INTERNAL_RUNS` was still absent afterwards (lstat).
- **Step 9 was STUBBED and never executed.**
- **Fence refusals: 0** (step 2a, step 3b and step 8).
- **The pycache prefix stayed empty** in both passes.
- **Prereg r6 and seal tools v003 are not published.** So r5 and two labelled SELECTED fixtures stand in for them (S19–S21). In the root script both stay PENDING, and step 0 refuses.

| step | pass A (faithful) | pass B (S16 shim for tools 3 and 4; S22) |
|---|---|---|
| 0 preflight (C-02 text-of-record check against the r6 SELECTED stand-in; v003 SELECTED names the tools; RP-S1 check) | PASS | PASS |
| 1 FROZEN copy: sha and length checked BEFORE copying, re-hashed after | PASS (c01b3c51, 143,081 bytes) | PASS (same) |
| 2 dispositions (A102–A106 labelled fixture df2fdf74) + tool 1 + re-hash / 2a driver BUILD record | PASS | PASS (d9226430) |
| 3 output root (RP-S1) + binder + **C-05/C-06 bound-check** | PASS | PASS |
| 3a final slots | PASS | PASS (9455f61e) |
| **3b C-04**: every slot record through r13's own `load_producer_registry` against V009 | **REFUSE** (see below). STOPPED. | REFUSE logged in STEP_03B_C04.json; continues (S22) |
| 4 sealed prereg / **4a C-02** + tool 3 | not reached | PASS (d63072a4) / PASS / PASS |
| 5 sealed compare / 5a tool 2 | not reached | PASS (2f41a02a) |
| 8 --gates-only fenced + row scan + **C-03 provenance** | not reached | PASS (sealed mode; the 8 slotted gate records evaluated, all PASS) |
| 9 | not reached | **STUBBED** |
| **10 C-02** + tool 4 / 11 SEAL_RECORD | not reached | PASS / PASS (c2939e2e = tool 4 stderr) |
| 12 config + guard self-check + W7-S1 re-check / 13 receipt / summary | not reached | PASS (48f07525) / PASS (bf732df1) / PASS (output root still the same empty directory) |

**C-04 on the draft's slots (V009):**

`C04_SLOT_RECORDS_FAIL_THE_REGISTRY {"certificates.EPS_NGC": ["GATE_RECORD_SHA_NOT_ROOT_REGISTERED_A67_N2:EPS", "PRODUCER_NOT_ROOT_REGISTERED_A62_2:EPS"], "certificates.I1T_NGC": ["C04_NOT_A_REGISTRY_GATE:certificates.I1T_NGC:I1T_NGC"]}`

Every other slot passes: EPS, LO, GQ, DOUBLING, LO_NGC, the three identity records (with comparator and tokens), the comparator and the registry pin. This is a root-ruling item (P12).

## Substitutions
S01–S18 are as in dry run 9. This run adds four:
- **S19:** `PREREG_TOR` = r5 (dry run only; r6 is not published).
- **S20:** `R6_SELECTED` is a labelled fixture naming r5 (`fixtures/R6_SELECTED_DRYRUN_FIXTURE.json` `30f6f63e…`).
- **S21:** `V003_SELECTED` is a labelled fixture naming the v001 placeholders (`fixtures/V003_SELECTED_DRYRUN_FIXTURE.json` `ad1ced7f…`).
- **S22 (pass B only):** C-04 runs in full and its verdict is logged, but a REFUSE does not stop pass B. The root script stops there.

| file | sha256 |
|---|---|
| passA/SUBSTITUTION_A.diff (54 changed lines) | e63e1a31f68b751b35aba421c3e1666face30c8e2c32ed808dbddb352762734a |
| passB/SUBSTITUTION_B.diff (63 changed lines) | e3396758ce73e21b1115bf8fd0483d7d7f60f4c8d4bd8c86358a3f8f2a570887 |
| passA/ROOT_SEAL_STEPS_DRYRUN_A.sh / passB/…_B.sh | e114935398cffbe5607cfadd6891986fdf3123eba1a5907c4e7cdb697bad60d6 / f8de811cb46f509f4438677fe520e85fb36b42b318e86d20615fafb42c44a42d |
| passA/SUBSTITUTIONS_A.json / passB/SUBSTITUTIONS_B.json | b6c29eedc479449dffa6cedca07fbafd37803bf3c56d58c4f8bfc9263040c14d / 6602dc05abf84bfca936d550bbf308edc9c0f26b046c135f04f498a30031e372 |
| passA/RUN_A.sh / passB/RUN_B.sh | 7d21f66bc24cc33c6a8a71ae12949badd69cb58d7fe90866497608e51895fd03 / 16ea982f29ca2ebac00c3a8527129e84f50f1f9b9137d41c7da1e710fa6ed2d7 |
| passA stdout / stderr | 1c79e86fc4bd0f3062602bfb8db623f91a59a87603dc06c413fd89190ecba076 / 302807c15ae73a5fb57a3c7c791ca0635c9cf0b96e62ebfe0eb6f9aca785ecaf |
| passB stdout / stderr | ea9d458ea67925c018b754499f6ff31b4d59e5003005b8db0bceae91c787bce2 / f1d04cc9b78f9e9fd1b3c29d6952921103d1a4d94cb3f02fecd9ccf65e952070 |
| fixtures/_DISPOSITIONS_V003_OBJECT.tmp.json (labelled FIXTURE) | df2fdf74d45a5785a66d76f4a12b962533ac0a0e27bcca8991cc3143c19a374c |
