# LENS 3: tests and seal integration. Compare r14, delta review of record (Claude4 helper)

Dispatch 0651 (`8bed78cb…`), root entry A114 in V006. Builder: Codex1. Reviewer: a helper of lane Claude4, which is cross-lineage to the builder. Written 2026-10-19 at about 03:40Z (UTC from `date -u`). I refuted by default. Each claim is labelled TESTED (run or hashed from bytes here), FORMAL (read from bytes, not executed) or UNTESTED. AUTHOR-RUN marks counts the builder produced that I did not re-run.

## Verdict

**0 BLOCKING under A115, neither class (a) nor class (b).** V006 moved from `ca5d7ae3` to `63e7802f` during this review. A115 was appended, and A114's text is unchanged on re-read.

- **The r14 source (`f3f9ba7e`).** For this lens, it is exactly what A114 rules.
- **SELECTED_R14_CX1V002 (`6b650ece`).** This is the publication that integrates with seal tools v004.
- **SELECTED_R14_CX1V001 (`dc74949d`), the file named in the dispatch.** It is not seal-ready. Its IMPL `854cad0d` is refused by tool 4 (TESTED), so it must not be the file sealed.
- **The selected seal pre-stage (c3v009 → ROOT_SEAL_STEPS_c3v020).** It refuses r14 (FORMAL) and needs a successor.

Both seal-path items fail closed and have no physics effect. Under A115 they are therefore NOTE class, but each is a required action before the seal.

## Hashes checked from bytes before use (TESTED; none differ, so no stop)

All of these were hashed with `shasum` and again inside the fenced probe (S0, 24/24):

- SELECTED V001: `dc74949d1d4f19336661f8ce85e9a85de0176837adad61c7a9585a147f933533`
- Source: `f3f9ba7ec4439933ab88c7623a6ede5b04763b83f0610b1917393362f33c67d7`
- FIELDS V002 `2ce9f1c7…` and FIELDS V001 `a33b153b…`
- IMPL `854cad0d…`, VALIDATION `930ca7bc…`, harness `998e0c2e…`
- SOURCE_DELTA `56a95b7e…`, HASHES `8b92153a…`
- r13: `f5adfd11…`
- Newer files also in r14/:
  - SELECTED V002 `6b650ececefee673ec3e04849574f9a4b75b977288afd3c9949a4b8d2d3cd49a`
  - IMPL V002 `2ba6d12ecc36ab444365348573b7f49a02a12a818dd15d67de35d77300fa17c9`
  - HASHES V002 `46b811c1…`
- Seal tools v004, all matching SELECTED_SEAL_TOOLS_V004_C4V001 `593c59fa`: tool 4 `9787cf58…`, tool 2 `c2c5dfc5…`, tool 3 `316973a1…`, tool 1 `a56f8d79…`, seal_common `101a3aeb…`
- Fence `c993d34c…` and runner `fe904509…`, copied byte-identical into tools/
- Root inputs: V001 `b9db6fd1`, V002 `a0284ece`, V003_DRAFT `21968a07`
- r6 SELECTED: `7200acd9`
- V005 live: `c01b3c51`

Every `{path, sha256}` pin inside HASHES V001 (50 pins), HASHES V002 (4), VALIDATION (34), SELECTED V001 (7), SELECTED V002 (8), SOURCE_DELTA (2) and BUILD_PROGRESS (9) re-hashes to its pin, with the byte counts matching (TESTED, probe_hashes_c4).

## (1) The 12 A114 MUST assertions

- **Where they are** (TESTED by diff). They are harness L4319–4321: `A114_MUST_I4_TOKEN_ACCEPTED`, plus `A114_MUST_TOKEN_REFUSED_<g>` for 11 gates: B0, B0prime_RERUN, B1, B1_OFF, B2, B3, DOUBLING, EPS, GQ, LO and LO_NGC.
- **The harness delta from r13's harness (`71c7b516`).** It is exactly:
  - the docstring and CMP path (L1, L52, L68);
  - the 3 inserted MUST lines;
  - the FIELDS comparison at L5210–5211, retargeted to `FIELDS_R14_CX1V001.md`.
- **Re-run in my own process under the fence** (TESTED; fixture producer files written in my folder; harness REG_OBJ shape, C2V003 pins).
  - **r14: 12/12 pass.**
  - **r13: 11/12 pass.** It fails exactly `A114_MUST_I4_TOKEN_ACCEPTED`, with refusal code `PRODUCER_REGISTRY_GATE_RECORDS`.
  - **Only that one assertion is r14-specific.** The 11 refusals pass on both rounds; they are regression guards.
- **A sweep over all 26 gates, in two forms:**
  - **faithful:** the harness base, then the token on one gate;
  - **isolated:** no token in the base, then the token on one gate only.

  r14 accepts exactly `SRB_ROT, RB_FP, T2I, EA, MT, I1T, FLAG_RULINGS, HARMONICS, SR_K, I4`. r13 accepts the same set without I4, so the difference is exactly `{I4}`. Every refusal is `PRODUCER_REGISTRY_GATE_RECORDS`. The B0-family gates the MUST list does not name (B0prime_DRY, B0_FA, B0_RO1, B0_N3) are refused as well (TESTED).
- **The token end to end on I4** (TESTED; synthetic I4 records, `evaluate_gate`, r14):

  | Case | Result |
  |---|---|
  | Token, valid record | PASS |
  | No token, no sha | RECORD_DEFECT `GATE_RECORD_SHA_NOT_ROOT_REGISTERED_A67_N2:I4` |
  | Registered by sha | PASS |
  | Token, unregistered producer | RECORD_DEFECT `PRODUCER_NOT_ROOT_REGISTERED_A62_2:I4` (the token does not bypass the producer pin) |
  | Token, failing record | FAIL `I4_SERIAL_PARALLEL_NOT_BITWISE_EQUAL` |
  | Token, PASS verdict over bitwise false | RECORD_DEFECT `VERDICT_PASS_CONTRADICTS_DATA:I4` |
  | r13, hand-built token | RECORD_DEFECT `GATE_RECORD_TOKEN_NOT_ALLOWED_FOR_THIS_GATE_NEW52:I4` |

  `gate_record_sha_codes` on a hand-built token agrees with each module's allowed set for every gate.
- **Nothing else changed** (TESTED):
  - Same line count (5865). One line differs, L341, and it is r13's tuple plus `'I4'`.
  - The exact inverse restores `f5adfd11`. The byte delta is +6.
  - Among 206 module constants, the only one that differs structurally is `GATE_RECORD_AFTER_SEAL_ALLOWED`.
  - All 209 function code objects are identical, first line numbers included. g_I4 and its verdict are unchanged.
  - `required_gates('parallel8')` contains I4, and `serial_with_exemption` does not, in both rounds.
  - The case block `76309ae3` sets `route_a_mode` = `parallel8`, the only key I printed.
  - The generated contract `FIELDS_R14_CX1V001` differs from r12's `FIELDS_R12_CX3V002` (`5cc95a06`) in one line only: L66, which adds I4 to the token list.
- **The real registry V009 (`32ddadcb`).** It loads identically through r13's and r14's `load_producer_registry`: 26 producer and comparator pins hashed, nothing refused by the fence. A V010-like copy, with `I4` = PRODUCED_AFTER_THE_SEAL, is accepted by r14 and refused by r13. The token on EPS, B0_N3, B0_RO1 or GQ is refused by both (TESTED, probe_registry_v009_c4, 9/9).
- **Builder counts (AUTHOR-RUN).** 718/718 (706 inherited plus 12), real-record 70/70, mutation 96/96.
  - Evidence shas verified: `author_v002.stdout` `d8ccd0be`, which ends "718/718 pass" and shows the 12 A114 lines as PASS; `real_v001.json` `5bc8c880`, whose `script_sha256` is f3f9ba7e; `MUTATION_R13.json` `7bb7e539`, 96/96.
  - The real-record and mutation tools differ from r13's only by the r14 path (TESTED by diff).
  - I did not re-run the whole suite.

## (2) Seal tool 4 integration (critical)

I loaded tool 4 from its folder with its sibling modules and verified the siblings from bytes. I then called its own `new_items_codes` under the fence (TESTED):

| compare_impl pin | reviewed sha | Result |
|---|---|---|
| `COMPARE_V007_IMPL_R14.md` `854cad0d` (items `[]`, or one valid item) | f3f9ba7e | **REFUSED `NEW_ITEMS_IMPL_NOT_THE_REVIEWED_SOURCE`** |
| `COMPARE_V007_IMPL_R14_CX1V002.md` `2ba6d12e` (items `[]`, or one item) | f3f9ba7e | PASS, no failure |
| r13 IMPL `274f7049` | f3f9ba7e | REFUSED |
| r13 IMPL | f5adfd11 | PASS (control) |
| IMPL V002 | f5adfd11 | REFUSED |
| IMPL V002 path, pinned with V001's sha | — | `PIN_BYTES_MISMATCH` |

Which r14 files contain f3f9ba7e in full (TESTED):

- IMPL V001 contains neither the full sha nor the 8-hex prefix.
- Files that do contain it: IMPL V002, both SELECTED files, both HASHES files, SOURCE_DELTA, VALIDATION and BUILD_PROGRESS.
- Files that do not: both FIELDS files, both harness files and the source itself.

The check is a substring test. SELECTED_R14_CX1V001, offered as a "compare_impl", passes it (see F6).

SELECTED V002 against V001 (TESTED):

- They differ only in `utc`, `implementation`, `note` and `supersedes_selection`.
- IMPL V002 is IMPL V001's bytes plus one appended section, "Reviewed source binding (Claude4 0129)".

## (3) Tool 2: check_sealed_compare_c4v003 (FORMAL, plus TESTED)

- **FORMAL.** Tool 2 takes `--reviewed` and `--sealed` by path, and takes the slots and prereg by path.
  - Its only constants are the five A82 pin names in seal_common.
  - Tools 1, 2 and 3, seal_common and tool 5 contain no r13 sha, no r13 path, no `GATE_RECORD_AFTER_SEAL` and no `'I4'` (grep counts are 0).
  - Tool 4's only r13 reference is the E_R6_1 text.
- **TESTED.** In r14 each of the five pins is assigned exactly once, as `NAME = None…`. `ADDENDUM_V005_CITED` is the open V005 path, and `SCHEMA_REPORT` is unchanged.
- **TESTED: PASS with five pins set.** Tool 2's `run()` gives PASS on r14 with a synthetic sealed copy in which only the five pin lines are set. The copy is never executed; its notes are `ADDENDUM_V005_CITED` and `CITES_OPEN_ADDENDUM_PATH`.
- **TESTED: refusals.**
  - An r13-based sealed copy against reviewed r14: REFUSE `NON_PIN_LINE_DIFFERS` at line 341.
  - A slot that still names r13: REFUSE `REVIEWED_PATH_NOT_THE_SLOT` and `PREREG_COMPARE_SLOT_DIFFERS`.
- **TESTED: tool 3 on r14.** Tool 3's `COMPARE_API` is all present on r14, loaded through `load_reviewed_compare` from the verified bytes. The constants tool 3 reads equal r13's.

## (4) The C-08 table (TESTED)

- **V002.** Its 19 rows cite the r13 file.
- **V003_DRAFT.** Its 19 rows cite the r14 file, with the same lines.
- **Line check.** For every row, in both rounds, the cited line carries its `NEW-n` id, and it is that id's first line.
- **No line shift.** r13 and r14 have identical first-line maps.
- **Id set.** The row ids are exactly the 19 NEW ids in r14.
- **No NEW id in any IMPL.** The r13 IMPL, IMPL V001 and IMPL V002 carry none.
- **Row keys.** V003_DRAFT rows carry exactly `{new_item_id, file, line, declared_in_r13}`, all set to false.
- **Tool 4 form check.** `manual_disclosures_form_codes` gives PASS on V002 and on V003_DRAFT.

## (5) E_R6_1, a disclosure item for root's V003 (TESTED; not an r14 defect)

- **What E_R6_1 is.** Tool 4's `E_R6_1` equals r6 SELECTED `basis.erratum_E_R6_1`: 469 characters, UTF-8 sha `c28202b0…`.
- **What it says.** It names `v007_compare_c2/r13/COMPARE_V007_IMPL_R13.md (274f7049...)` as "The IMPL of record".
- **Why V003 must carry the succession.** Tool 4 requires `e_r6_1_text == E_R6_1`, and V001, V002 and V003_DRAFT all comply. So the r13 → r14 succession has to be stated in V003, not in E_R6_1.
- **What V003_DRAFT already does.**
  - Its row `A114_I4_AFTER_SEAL_R14` names r14 f3f9ba7e, SELECTED_R14_CX1V002 and IMPL V002 `2ba6d12e`.
  - The row says r14 "supersedes r13" and "declares no NEW item", and that E_R6_1 is "kept byte-identical".
  - Its `c08_confirmation` names the r14 sha and IMPL V002.
- **Also historical.** r6 SELECTED `basis.unchanged_bindings` still reads "compare candidate r13 f5adfd11"; the A114 row covers this.
- **What remains.** V003 is a DRAFT. Root must finalize and pin it.

## Findings

| ID | Severity (A115 class) | Label | Finding |
|---|---|---|---|
| F1 | SHOULD_FIX (NOTE class: fail-closed, no physics effect) | TESTED | SELECTED_R14_CX1V001's IMPL `854cad0d` does not name f3f9ba7e, so tool 4 refuses `NEW_ITEMS_IMPL_NOT_THE_REVIEWED_SOURCE`. **Resolved by SELECTED_R14_CX1V002 / IMPL V002 `2ba6d12e` (PASS).** The NEW-item list (P6, Claude4 0129 dependency 1), the seal pre-stage and V003 must pin V002. |
| F2 | SHOULD_FIX (NOTE class: fail-closed) | FORMAL | The selected pre-stage ROOT_SEAL_STEPS_c3v020 (`36058df8`; tuple c3v009 `9e10eae1`) is r13-bound. Details follow the table. Fix: a successor pinning r14 f3f9ba7e, IMPL V002, disclosures V003, registry V010, with r13 added to the superseded list. |
| F3 | NOTE | TESTED | The inherited comment at r14 L332–334 still lists I4 among the gates "registered by record sha", which contradicts L341. A114 permits only the one-line change. FIELDS_R14_CX1V002's header states the supersession. No code reads the comment. |
| F4 | NOTE | TESTED | Only 1 of the 12 MUST assertions discriminates r14 from r13. `R12_ADAPTED_..._ONLY_ON_THE_NINE_POST_SEAL_GATES` is self-referential: it passes on r13 and r14, and its name says NINE where there are now ten. No author test drives the I4 token through `evaluate_gate`, because `registry_with_records` (harness L531–543) re-registers each written record by sha. I covered that path (S4, 7 checks). |
| F5 | NOTE | TESTED | `r14/tests_kmax_tail_compare_c2v007_r13_cx3v001.py` (`b00e533a`) is not r13's harness (`71c7b516`). It is the failed author v001 harness, which differs from `998e0c2e` only at L5210–5211. The name is misleading. |
| F6 | NOTE (tamper-robustness, later version) | TESTED | Tool 4's IMPL check is a substring test: any pinned file containing the sha passes, as SELECTED V001 does. Honest inputs are unaffected. |
| F7 | NOTE (disclosure) | TESTED | E_R6_1 names the r13 IMPL `274f7049`. The succession belongs in V003. V003_DRAFT's A114 row and `c08_confirmation` carry it correctly; it needs to be finalized and pinned. |
| F8 | NOTE (confirmation) | TESTED | The C-08 rows in V002 and V003_DRAFT are correct against r14 bytes: no line shift, same 19 ids, and the tool 4 form check passes. |

**F2 detail: where c3v020 is bound to r13.**
- L272 sets `COMPARE_R13_SHA=f5adfd11`.
- L365 refuses any reviewed compare other than r13: "REFUSE: the reviewed compare must be r13 f5adfd11".
- L218 and L377 role-pin `impl_of_record_r13` to 274f7049.
- L222 pins disclosures V002 `a0284ece`.
- L241 pins registry V009 `32ddadcb`.
- `COMPARE_SUPERSEDED_SHAS` lacks r13.
- The C-04 helper, c3v019 `91b15dc6`, loads the compare from the `--compare`/`--compare-sha` arguments, so it is generic. Only r14's loader accepts V010's I4 token (TESTED).
- BUILD_V007 `94bc05a5`, guard v008 `294cb776`, launcher v007 `861bba68` and the binder `f3e4e2be` carry no compare pin (TESTED, grep counts 0).

## UNTESTED

- The real I4 producer, the N1 spec and the V010 registry bytes. Not published, or not reviewed here.
- The I4 run pair, and any production execution.
- The seal pre-stage successor.
- A full tool 4 build (`build()`) on real slots. I called only `new_items_codes` and `manual_disclosures_form_codes`.
- The whole 718-case author suite, the real-record check and the mutation check. These were not re-run (AUTHOR-RUN).

## What ran (TESTED) and the evidence

Everything ran through `tools/run_fenced_c4st2.py` with fence_c4v002. Every run reported selftest 8/8, exception probes 15/15 and `blocked_after_selftest: []`. Nothing protected was opened. No driver, comparator CLI or seal-tool CLI was run, and nothing was deleted.

| File | sha256 |
|---|---|
| `probe_integration_c4.py` | `e20cd4f36e1d2fadf8e27c9e272cc4cc735c361c163e6c58a861ca9d0501d937` |
| `out/run_20261019T033109Z/PROBE_RESULTS_C4.json` (112/112) | `ffa2a576fd9d14502cba69795353fa76603bc90073c8f9e19f8395c83748b67c` |
| `out_run_20261019T033109Z.stdout.txt` | `2cdfcf032740c6e1c80b24f44360d9905786d85d3d88d66bc8f45bb50acb36d0` |
| `out/run_20261019T033041Z/PROBE_RESULTS_C4.json` (earlier run, kept) | `ec993f10240de4b533a9447fe12d3ebd5c655c02de3e03d830a6613d5b218d5c` |
| `probe_registry_v009_c4.py` | `98a7a288986d28f338b0a0b2e6575e5eabaf6922643876b065b04880862de8e3` |
| `out/reg_20261019T033459Z/REGISTRY_V009_PROBE_C4.json` (9/9) | `ee7037b13620c05117457aaae34dadaac8af0cd17713303c3198d1cf9daf7fff` |
| `probe_hashes_c4.py` | `7b4cf8ddf9915459f23719f7c07abc5b2eed863a4afb7ef6ac73de24125273ad` |
| `out/hash_20261019T033531Z/HASH_MANIFEST_PROBE_C4.json` (0 bad) | `c22fe4b24af7ac54bbe13280c3eabb837279a20b0cef7ae493af9937cf8aa863` |
| Fence stderr summary (identical for all runs) | `fea03ab3061a372b69d4c0f62c5843308422305ad75604cd3852999432d506ee` |

The earlier run (033041Z) scored 111/112. Its one failure came from my probe, not from r14: it compared constants by `repr`, and function reprs inside the dict constants carry memory addresses. That run was produced by an earlier, overwritten revision of `probe_integration_c4.py`, which differed only in `consts()`.
