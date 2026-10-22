# REPORT: independent check of prereg r5 and the V007 case block, and the seal rehearsal rerun on r12

Claude4 helper (r5_check). UTC {UTC} (`date -u`). Folder `claude_artifacts/v007_final_prereg_c4/r5_check/`. Labels: **TESTED** (run or read from bytes here), **FORMAL** (follows from code or text read here), **UNTESTED**. Severities: BLOCKING, SHOULD_FIX, NOTE. Refute-by-default throughout.

**Objects (sha256 from bytes).** Prereg r5 `{S:/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/r5/KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R5.json}`; r4 `{S:/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/r4/KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R4.json}`; case block `{S:/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/r5/case_block/CASE_BLOCK_V007_C4V001.json}`; compare r12 cx3v002 `{S:/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r12/kmax_tail_compare_c2v007_r12_cx3v002.py}`; FIELDS_R12 `{P:/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r12/FIELDS_R12_CX3V002.md}`, IMPL_R12 `{P:/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r12/COMPARE_V007_IMPL_R12.md}`. Rulings: the open V005 addendum, read from two exclusive byte copies in `scratch/`: copy 1 `{S:scratch/V005_ADDENDUM_READ_COPY_1_R5CHK.md}` (21:10:54Z, A47-A101, the bytes r5 was generated from) and copy 2 `{S:scratch/V005_ADDENDUM_READ_COPY_2_R5CHK.md}` (21:23:09Z, adds **A102**). Every entry A47-A102 was read in full.

## Verdict

- **Case block CASE_BLOCK_V007_C4V001 confirmed (TESTED).** r12's own `validate_case_block`, loaded unmodified in-process under my fence, returns `[]`; each of the 11 entries equals my own derivation from the ten FILLED specs and their driver-r5 dry runs; 43 of 47 mutations are refused and the other 4 are admitted exactly as predicted; 6/6 duplicate-key byte mutations refuse.
- **Prereg r5 traced (TESTED, FORMAL).** Every r4 to r5 change sits in a logged clause with a ruling, defect or gap behind it; no untouched clause changed; 187/187 pins verify from bytes; the entry table A82-A101 re-hashes 20/20 and its four "no change" rows hold.
- **CASE_BLOCK_ABSENT is gone (TESTED).** A scratch sealed r12 reading a scratch sealed r5 reaches and passes the case-block step in sealed mode and completes `--gates-only`. All 13 registered pre-seal records read PASS. The same holds on r13 in test mode.
- **SEAL_NOT_READY on r5 as written.** 1 BLOCKING (F-01: A102 at 21:22Z postdates r5 and touches its text), 3 SHOULD_FIX, notes. The remaining refusals in the rehearsal are root's seal-assembly items and the records that are not built (section 5).

## 1. r4 to r5 diff, from bytes

- My own leaf differ (`tools/diff_r4_r5_r5chk.py`, root items keyed by id): **756 differing leaves** (676 added, 11 removed, 69 changed). The builder's audit counts 1039, because it compares root items by position; both counts are consistent. Record `out/DIFF_R4_R5_R5CHK.json` `{P:out/DIFF_R4_R5_R5CHK.json}`, full text `out/DIFF_R4_R5_R5CHK.txt` `{P:out/DIFF_R4_R5_R5CHK.txt}`. TESTED.
- **Every differing clause group maps to a DELTA_R4_R5 row (1-47) or to erratum E1** (`revision`, `supersedes_draft`). No other clause differs; every "revised clause" an entry-table row names does differ. TESTED.
- **Root items:** RI-01..RI-26 are unchanged by id, except RI-24 (status annotated "moot for V007 under A96") and RI-27 (OPEN to RESOLVED by A82). RI-28..RI-37 are new. TESTED.
- **Pins:** all 187 `{path, sha256}` pairs in r5 verify from bytes; the only non-sha is the frozen addendum, correctly `PENDING_ROOT_AT_SEAL_ASSEMBLY`. No pin names a runs_ext, UVT_* or C5H path. `out/PIN_VERIFY_R5_PREREG_R5CHK.json` `{P:out/PIN_VERIFY_R5_PREREG_R5CHK.json}`. TESTED.
- **Content, refute by default (FORMAL).** Each changed clause was read against its cited entry: A82 (RI-27; no write after the freeze), A83/A86/A91/A96 (compare slot: reviews of record replace the stopped recheck lenses), A83/A92 (comparator check of record; R5_V001 records), A86.1 (GQ_CERT_V006), A87 (B3 JSON, DOUBLING ea48ac2b and its `ddo_gas_M_s`, LO_NGC V002), A88/A99.5 (SR_K after the seal; r12 L338 `GATE_RECORD_SHA_REQUIRED = ()` and L341 read from bytes), A89 (measured cost), A93 (NGC registry), A94/A97/A100/A101 (B2), A96 (r5 only), A99.1/A99.2/A99.3 (BUILD_V007, case block, entry table). All hold. The one loosening against r4, dropping "three recheck lenses" from the compare rule, is root's (A83, A86, A96). Two wording problems are in F-01 and F-02.
- **ngc_gas_M_s 96.** GQ_NGC_91_MS96_V001 `{P:/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_ntest_eval_cx/out/GQ_NGC_91_MS96_V001.json}` reads verdict PASS (threshold 1e-12; scalar fields only read), and Codex1 0032 `{P:/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX1/0032_2026-10-18_gq91_pass_and_latest_rulings.md}` states the values. RI-23's condition is factual, so 96 is consistent; no A-entry names the record (F-13). TESTED.

## 2. The entry table (A99.3)

- **Section shas re-extracted from bytes** by an independent byte-level extractor (`tools/entry_shas_r5chk.py`) on copy 1: **20/20 rows match, headings equal**, no duplicate heading, no entry from A82 to A101 without a row. Five rows (A84, A85, A95, A98, A101) were also re-hashed with `sed` line ranges and `shasum`. On copy 2 (with A102) the 20 rows still re-hash, because A102 was inserted above A101 and changes no other section; **A102 has no row**. `out/ENTRY_SHAS_R5CHK.json` `{P:out/ENTRY_SHAS_R5CHK.json}`, `out/ENTRY_SHAS_ON_COPY2_R5CHK.json` `{P:out/ENTRY_SHAS_ON_COPY2_R5CHK.json}`. TESTED.
- **The four "no change" rows, judged against the entry text (FORMAL, CONFIRMED):**
  - **A84** schedules speculative r6 identity runs, concurrent lane work and Codex3's step-5 readiness. It changes no rule, and A96 later made r6 moot.
  - **A85**: items 2-4 are RUNBOOK root steps that change no sealed byte (A85's own words). Neither r4 nor r5 has any clause on QoS, output volume or caffeinate (searched in both JSON files). A85.3's one indirect effect, the V011 template's internal-volume outputs, enters r5 through A99.1 (V6-S2) in the launch-packet rule. A85.1 adopts nothing before the seal.
  - **A95**: taskpolicy is preferred, not required, and production stays single-thread BLAS. Neither text has a clause on lane priority or BLAS threading.
  - **A98**: PAR-TB concerns the NGC v011 successors (step 5), and the miss-reading prereg r3 is step 6. Neither is V007 text.
- **The 16 "revised here" rows** each name clauses that do change, and the change matches the entry (section 1).
- **A102 (21:22Z) is not covered**, and it touches r5's text: F-01.

## 3. The case block

**Validation (TESTED).** `tools/case_block_check_r5chk.py`, run under `tools/fence_c4v002.py` with r12 `4bd7b262` loaded unmodified from its bytes: **127/127 checks**. Record `out/CASE_BLOCK_CHECK_R5CHK.json` `{S:out/CASE_BLOCK_CHECK_R5CHK.json}`.
- `validate_case_block(case block of record)` returns `[]`, in default mode and in parallel8. The block's route_a_mode is parallel8 and its key map is `[]`.
- **The spec list and shas, re-derived from the sources:**
  - SPEC_REGISTRY_R5_MS128_CX1V004 `{P:/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/SPEC_REGISTRY_R5_MS128_CX1V004.json}` lists exactly the ten T-cases, with driver r5 and the A70 certificate slots; every FILLED spec hashes to its pin.
  - DRY_R5_MS128_V004 `{P:/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/DRY_R5_MS128_V004.json}` names that registry and driver r5. Each of its ten dry reports hashes to its pin and names its FILLED spec by path and sha, with driver r5, exit 0, no executed stage, no binding blocker and no unexplained, beyond-pending or static refusal.
  - Plans V010 `{P:/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/P128/LAUNCH_PLAN_V010.json}` and V011 `{P:/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/P128/LAUNCH_PLAN_V011_CX3V001.json}` launch exactly those ten FILLED specs. V011 differs from V010 in **51 string leaves only**, all output paths moved from External1 runs_ext to `UNT_INTERNAL_RUNS`; no spec, driver, registry, order or cap leaf differs.
  - **Each of the 11 entries equals my derivation** (grid and truncation from r12's registered constants; `/numerics` = the dry report's `normalized_spec.numerics`; tail and ro1_required true; drivers_allowed [r5]; uv_tail sha = the pinned library's `normalize_config`, which equals the driver-side `normalized_sha256` 10/10; C5H = call 60b46130 on v009-EXT 999331af with nothing else registered). Notes are excluded from the comparison; each note names its FILLED spec sha and dry report sha.
  - The dry normalization only adds `/truncation/kmax_inverse_kpc` on 9 cases (not S4T), and changes or removes no leaf. C4T-D5's `/numerics` equal the C5H reference outside `composite_grid_spec` and `uv_tail`.
- **In-memory mutations: 47, all as expected.**
  - **43 are refused**: each of the 11 cases dropped; an unknown case added; uv_tail shas swapped between C4T and C4T-KHI; a uv_tail sha set to a spec sha; C5H set to the reviewed C5 spec 09ff5a96; the whole /numerics of C4T and C4T-KLO swapped, alone or with their shas; C2T given the superseded CX1V002 numerics; drivers_allowed r4, or [r5, r4]; four malformed key maps (a missing field, a pointer mapped twice, a pointer inside uv_tail, a pointer outside /numerics) and a map that is not a list; a bogus route mode; schema C2V002; an unknown top-level key; tail or ro1_required false; a wrong grid; S4T as a cube; KLO K_big 32; gas M_s 64; C4T-A lambda 1.0; D5 column_workers 1; a seed factor of 0.1; D5 on continuum; a changed certificate sha; C5H with the tail on or driver r5; an unknown entry key; empty brackets.
  - **4 are admitted, as predicted (FORMAL from the code, then TESTED):** an edited note; two well-formed key-map entries on allowed pointers; and route_a_mode serial_with_exemption while the numerics carry column_workers 8. See F-07.
- **Byte-level duplicate keys, read back with r12's `load_strict_file`: 6/6 refused.** A duplicate schema, a duplicate case C4T, a duplicate entry key, a duplicate numerics key and a duplicate with equal values each give `CASE_BLOCK_DUPLICATE_JSON_KEY_A71`. A duplicate behind a 4301-digit integer gives `CASE_BLOCK_UNREADABLE`: the case-block reader has no text fallback, so the A-B1 class does not reach it.
- **Through r12's own CLI (TESTED, fenced, no outdir created on any refusal):**

  | run | mutation | code |
  |---|---|---|
  | M1 | test prereg binding a key-map-modified copy with the record's sha 76309ae3 | CASE_BLOCK_SHA_MISMATCH |
  | M2 / M8 | r5 (test) / scratch sealed (sealed mode) with `--case-block` at another path | CASE_BLOCK_DIFFERS_FROM_THE_PREREG |
  | M3 / M9 | `--route-a-mode serial_with_exemption` (test / sealed) | ROUTE_A_MODE_SOURCES_DIFFER |
  | M4 | r4, no `--case-block` (on r12 and on r13) | CASE_BLOCK_ABSENT |
  | M5 | test prereg binding the duplicate-C4T copy (its own sha) | CASE_BLOCK_DUPLICATE_JSON_KEY_A71 |
  | M6 | test prereg binding a copy with C4T-KHI dropped (its own sha) | CASE_BLOCK_INVALID |
  | M7 | test prereg binding the well-formed key-map copy with its own sha | admitted (exit 0; see F-07) |
  | M10 | sealed mode with `--test-producer-registry` | TEST_OPTION_IN_SEALED_MODE |

## 4. Rehearsal rerun on r12 (scratch only)

**Scratch inputs** (`tools/make_scratch_seal_r5chk.py`, `tools/make_scratch_slots_v2_r5chk.py`; folder `scratch/rehearsal_r12/`, index `SCRATCH_INPUTS_R5CHK.json` `{P:scratch/rehearsal_r12/SCRATCH_INPUTS_R5CHK.json}`). None is a seal input of record. Nothing was created in a real seal location.
- **Frozen stand-in:** a byte copy of the open V005 file at 21:33:55Z, `{P:scratch/rehearsal_r12/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM_FROZEN.md}` (= copy 2, with A102).
- **Sealed prereg A** `{P:scratch/rehearsal_r12/KMAX_TAIL_PREREG_V007_SEALED_SCRATCH_A_R5CHK.json}` (PENDING kept PENDING: frozen addendum, driver BUILD record, bound plan and command, cascade addendum) and **sealed prereg B** `{P:scratch/rehearsal_r12/KMAX_TAIL_PREREG_V007_SEALED_SCRATCH_B_R5CHK.json}` (the same, with clearly labelled GAP placeholders). Every other slot holds its current candidate, verified from bytes: driver r5 b5cc62af; compare r12 4bd7b262; c2v007r2 052da0fe; R5_V001 B1/B1_OFF/B0prime_RERUN; BUILD_V007 94bc05a5; EPS 598c8fa3, LO 1c384f76, GQ V006 5a1b39f8, DOUBLING ea48ac2b, EPS_NGC 1d5eef1b, LO_NGC V002 33bc2190, I1T_NGC 3ae7981a; registry C3V009 32ddadcb; cache NOT_APPLICABLE_R5; ngc_gas_M_s 96; admission entry = BUILD_V007's launcher v007 and guard v008.
- **Scratch sealed r12:** P `{P:scratch/rehearsal_r12/kmax_tail_compare_c2v007_r12_SEALED_SCRATCH_P_R5CHK.py}`, with PIN_ADDENDUM_V005 and PIN_DRIVER_BUILD_RECORD kept None; and B `{P:scratch/rehearsal_r12/kmax_tail_compare_c2v007_r12_SEALED_SCRATCH_B_R5CHK.py}`, with all five A82 pins set (V007_PREREG_SHA256 = prereg B; PIN_ADDENDUM_V005 = the stand-in; PIN_DRIVER_BUILD_RECORD = a byte copy of the rehearsal draft 2a3e4308; PIN_V010_R5_CHECK = CHECK.md 89a6de88; PIN_PRODUCER_REGISTRY = C3V009). A `diff` against r12 shows exactly those five lines.

**Seal tools v002 (they landed during this check: README `{P:/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/seal_tools_v002/README_SEAL_TOOLS.md}`; I ran its set of record, `r2/`, whose file hashes match its README; each tool ran under my fence, since tool 3 imports the compare).** TESTED:

| run | tool and inputs | verdict and codes |
|---|---|---|
| T1a | tool 1, prereg B, stand-in | REFUSE: FROZEN_PATH_NOT_PATH_TO_BE (the stand-in is not at path_to_be: root's copy); **UNCOVERED_LATER_ENTRY: A102** |
| T1b | the same, `--covered-later A102` | REFUSE: FROZEN_PATH_NOT_PATH_TO_BE only |
| T5 | tool 5 (driver BUILD record printer), r12, CHECK.md | PASS: record `{S:scratch/rehearsal_r12/DRIVER_BUILD_R5_TOOL5_R12_R5CHK.json}`, as the v002 README states. It equals the rehearsal draft except for the draft's `note` key |
| T2a | tool 2, sealed compare P, slots A | REFUSE: PIN_NOT_SET (PIN_ADDENDUM_V005), PIN_NOT_SET (PIN_DRIVER_BUILD_RECORD), CITED_ADDENDUM_BYTES_NOT_PINNED |
| T2b | tool 2, sealed compare B, slots B | **PASS** (note CITES_OPEN_ADDENDUM_PATH) |
| T3a | tool 3, slots A, text of record r5 with `--text-of-record-sha` | REFUSE, 20 codes: 14 PENDING_VALUE, 1 PIN_PENDING, 4 PIN_TYPES (each on the four PENDING pins and their sealed-prereg values), CASE_BLOCK_NOT_VALIDATED (no active driver BUILD record) |
| T3b | tool 3, slots B, r5 with sha | REFUSE, 11 codes, every one on a scratch stand-in: FROZEN_SLOT_NOT_PATH_TO_BE; PLAN_DRIVER/ADDENDUM_NOT_THE_SLOT, PLAN_LAUNCHER/GUARD_NOT_BUILD_SUPPORTED, PLAN_TEMPLATE_NOT_NAMED_IN_BUILD, PLAN_TEMPLATE_NOT_THE_PREREG_NAMED_TEMPLATE, PLAN_NOT_BOUND, PLAN_CALLS, BOUND_COMMAND_NOT_THE_BINDER_LINE (the bound-plan and command placeholders); ADMISSION_ENTRY_NOT_THE_PLAN. **No case-block, certificate (D-01), identity or BUILD_V007 code**: the case block validates in the sealed-mode order, with DDO M_s 128 registered and key map `[]`; BUILD_V007's allowlist is 15/15; 46 PENDING strings remain outside slot values (D-09) |
| T3c | as T3b, without `--text-of-record-sha` | + TEXT_OF_RECORD_PIN_PENDING |
| T3d | as T3b, r4 as the text of record | + SEALED_PREREG_TEXT_CHANGED |
| T3e | full chain (tools 1 and 2 inside tool 3, `--covered-later A102`) | the T3b codes + T1:FROZEN_PATH_NOT_PATH_TO_BE |

**Compare r12, `--gates-only` only, under my fence** (manifest `{P:scratch/rehearsal_r12/GATES_ONLY_MANIFEST_R5CHK.json}`: the 13 pre-seal records registered in C3V009, each sha from bytes; no case, identity-run or R-PAIR directory). `--validity-only` was never run. TESTED:

| run | object | result |
|---|---|---|
| G-S1 | sealed compare P (two pins PENDING), sealed mode | REFUSED: SEALED_PIN_ADDENDUM_V005_PENDING |
| **G-S2** | sealed compare B, sealed mode | **exit 0: the case block is read from `binding_inputs.case_block` and accepted. CASE_BLOCK_ABSENT is gone.** `GATES_ONLY.json` `{P:out/G_S2_SEALED_B_GATES_ONLY/GATES_ONLY.json}`, test_mode false, script_sha256 = the scratch compare |
| G-T1 | r12 unmodified, test mode, prereg B, test registry C3V009, test driver BUILD record = the T5 output | exit 0; the same gate verdicts as G-S2 |
| G-T2 | r12 unmodified, test mode, r4 plus `--case-block` = my byte copy of the case block (76309ae3) | exit 0; the same gate verdicts (the rehearsal's G3 read CASE_BLOCK_INVALID with the draft) |
| G-T3 | r13 f5adfd11 (A102), test mode, as G-T1 | exit 0; the same gate verdicts |
| M11 | sealed compare B with PIN_ADDENDUM_V005 = 70a48f51 (the pre-A102 bytes r5 was generated from) | REFUSED: V005_ADDENDUM_SHA_MISMATCH. The A82 hazard is live: a write to the open V005 file after the freeze breaks the sealed compare |

**Gate verdicts (G-S2 = G-T1 = G-T2 = G-T3):** PASS for B0, B0prime_DRY, B0prime_RERUN, B0_FA, B1, B1_OFF, B2, B3, EPS, DOUBLING, GQ, LO and LO_NGC (13/13 registered pre-seal records). MISSING for **B0_RO1, B0_N3 and I4** (required, not built) and for the nine post-seal gates I1T, T2I, SRB_ROT, RB_FP, SR_K, EA, MT, HARMONICS and FLAG_RULINGS (by design). The identity runs read MISSING:NOT_IN_MANIFEST, by design: their directories are UVT_* trees, which only root reads.

**r13.** Codex3 froze r13 at 21:22Z (A102). My AST comparison shows 439 of 440 top-level nodes equal to r12; only `check_record_codes` differs (3 hunks, +2 lines). The case-block path is therefore the same code, and G-T3 confirms it (TESTED). r12 line references shift by +2 after L877 (L5706 becomes L5708).

## 5. Updated gap list (r5 + r12/r13), with owners

| id | item | state now (evidence) | owner | blocks seal |
|---|---|---|---|---|
| GAP-01 | frozen V005 addendum | MISSING. The open file is now 27b62183 (A102); freeze after the last pre-seal entry. M11: a stale pin refuses | Claude2 | YES |
| GAP-02 | entries after A81 | the r5 table A82-A101 is honest and re-hashes (20/20, on both byte copies). **A102 is uncovered and touches the compare rule (F-01)** | Claude2 (route), then Claude4 (r6) | YES |
| GAP-03 | case block | **CLOSED**: 76309ae3, pinned in r5; valid on r12 and r13 (TESTED here); Codex2 0507 and 0517 PASS | none | no |
| GAP-04 | driver BUILD record (B2a) | PENDING root. Tool 5 v002 prints it (25b4ff69 with CHECK.md), and r12 admits it (T5, G-T1) | Claude2 | YES |
| GAP-05 | driver check record (RI-36) | candidate CHECK.md 89a6de88; it passes r12 `check_record_codes` (T5) | Claude2 | YES |
| GAP-06 | final compare round | r12 FAIL (Claude3 0083, A-B1). A102 orders r13, f5adfd11, frozen; it differs from r12 only in `check_record_codes` (TESTED). Delta reviews by Claude3 and Codex2 pending (0632) | Claude3, Codex2; then Claude2 | YES |
| GAP-07/08 | identity comparator and records | DONE (A92); B1, B1_OFF and B0prime_RERUN PASS in G-S2 | none | no |
| GAP-09 | BUILD of record | BUILD_V007 94bc05a5: verified from bytes here (15/15 sources, 34/34 packaging pins, V011 = V010 + 51 output strings). Claude4's own delta check (0102, `review_build_v007_c4/`) is still running; Claude2 adoption pending (RI-29) | Claude4; Claude2 | YES |
| GAP-10 | bound plan and command (B3) | PENDING: the binder runs on V011 at the seal (T3b codes come from the placeholders) | Claude2 | YES |
| GAP-11 | DOUBLING refused by tool 3 | **CLOSED** in seal tools v002 r2 (T3b: no CERTIFICATE code on ea48ac2b) | none | no |
| GAP-12 | EPS_NGC and I1T_NGC records | root confirms (checklist A7) | Claude2 | YES (A7) |
| GAP-13 | producer registry | candidate C3V009 32ddadcb; its 13 records PASS in G-S2. B0_N3, B0_RO1 and I4 are empty (a V010 once built) | Claude3; Claude2 pins | YES |
| GAP-14 | B0_N3, B0_RO1 (b)(c), I4 | **NOT BUILT**: MISSING in G-S2 (required pre-seal gates) | Claude2 (runs; the I4 N1 pair); root or Codex1 (the B0_N3 scan); Claude4 (records) | YES |
| GAP-15 | B2 | **CLOSED**: C3V003 915fbcda PASS (A101; G-S2) | none | no |
| GAP-16 | B6 outputs of record | root only. G-S2 shows the sealed `--gates-only` path completes. `--validity-only` never ran here | Claude2 | YES |
| GAP-17 | B7 inputs: key map, NEW-item list, raw successor custody | MISSING; v002 defines their schemas. The key map is `[]` (RI-30) | Claude2 (assign) | YES |
| GAP-18 | CASCADE_MAP_R5_ADDENDUM | MISSING, no owner (RI-32). Tool 3 v002 requires it but checks only its name and a mention of the map sha (F-03) | Claude2 (owner) | YES |
| GAP-19 | driver r6 | CLOSED (A96) | none | no |
| GAP-20 | SR_K | after the seal (A88), the first post-seal step; RI-37 (producer-pin reading) | Claude2 | no |
| GAP-21 | admission config and receipt (B8, B9) | after the SEAL_RECORD; B8 = BUILD_V007's 15 sources; builder v002 has an admission mode | Claude2 | no (blocks launch) |
| GAP-22 (new) | r5 text versus A102 | F-01, F-02 | Claude2, then Claude4 | YES |
| GAP-23 (new) | text-of-record pin for tool 3 v002 | TEXT_OF_RECORD_SHA is PENDING; without `--text-of-record-sha`, T3c refuses TEXT_OF_RECORD_PIN_PENDING. Root rules r5 or r6 the text of record | Claude2; Claude4 (pin-only tool successor) | YES |
| GAP-24 (new) | independent review of seal tools v002 | landed 21:21-21:32Z; Codex3's review (0628) was waiting on delivery (0633) | Codex3 | YES (root uses them) |
| RI-31 | checklist A6 | B0 record c2cec35b covers r5 against r4 at M_s 64; there is no M_s 128 dry-identity row | Claude2 | YES (A6) |
| RI-35 | D-09 | 46 PENDING strings outside slot values (T3b passthrough); v002's builder states that the SEAL_RECORD is the authority | Claude2 (accept) | no |

## Findings

**F-01 BLOCKING (TESTED, FORMAL). A102 postdates r5 and touches its text, so r5 cannot be sealed as written.**
- A102 (21:22Z) rules that Codex3 builds r13 to close A-B1, that Claude3 and Codex2 delta-check it, and that "prereg r5's compare slot takes r13". The open V005 is now 27b62183.
- r5's entry table ends at A101. A99.3 requires the prereg to list every entry from A82 to the freeze. Tool 1 v002 refuses UNCOVERED_LATER_ENTRY: A102 (T1a), and my extractor finds A102 without a row.
- r5's compare-slot rule begins "The final compare round is r12 cx3v002 (4bd7b262 ...)". That sentence is now false, and r5's RI-28 is no longer open.
- A `--covered-later A102` note makes tool 1 pass (T1b), but a no-change note would be untrue. Seal tool 3 v002 does not read the rule text, so it would not catch the mismatch either.
- **Fix:** Claude4 writes prereg r6 once r13's delta reviews are in. It needs an A102 row ("revised here": the compare slot names r13 and its reviews of record), a generic compare rule (F-02) and RI-28 resolved. Alternatively, Claude2 rules an explicit superseding seal-record note for A102 and the r12 sentence (amending A99.3's literal requirement).
- **Owner:** Claude2 (the route), then Claude4.

**F-02 SHOULD_FIX (FORMAL). r5's compare-slot rule adds a path that A81 RI-20 does not have.**
- The rule continues "if a review of record reports a blocking item, the slot waits for root's ruling (a fix round, or a ruling on the item)". RI-20 requires 0 blocking from each review of record. "A ruling on the item" would let a seal proceed on a round whose review still reports a blocking item.
- **Fix (r6):** "V007 seals on the final round whose delta reviews of record each report 0 blocking (A81 RI-20, as applied by A83, A86, A91, A96, A102); candidates: r12 (superseded, A102), r13". Any root ruling that clears an item without a fix round is then a later entry, handled by the table.
- **Owner:** Claude4.

**F-03 SHOULD_FIX (TESTED). Seal tool 3 v002 accepts any CASCADE_MAP_R5_ADDENDUM file that mentions the r5 cascade map sha.**
- My labelled GAP placeholder (`{P:scratch/rehearsal_r12/CASCADE_MAP_R5_ADDENDUM_GAP_PLACEHOLDER_R5CHK.md}`), which is not an inventory, passed every cascade-addendum check (T3b: no CASCADE_* code).
- A69 requires an immutable inventory addendum that names the unreachable pin-only successor, and no tool verifies that content.
- **Fix:** the tool 3 successor requires the named successor path and sha, verified from bytes, or root checks the content at A4 and records it.
- **Owners:** Claude4 (tools) and Claude2 (A4, RI-32).

**F-04 SHOULD_FIX (TESTED; open dependency). r5 binds BUILD_V007 94bc05a5 before its delta check and adoption.**
- The BUILD sha is in the text: `named_candidates_verified_from_bytes.build`, which tool 3 v002 binds.
- I verified it from bytes: 15/15 allowlist entries, the allowlist file equal, the first 13 as in V006, 34/34 packaging pins, and V011 = V010 + 51 output strings.
- Claude4's delta check (0102) is still running and Claude2's adoption is pending. A successor BUILD would force r5 or r6 to be regenerated and tool 3 to be re-pinned. This confirms the builder's F-05 / RI-29.
- **Owners:** Claude4 (delta) and Claude2 (adoption).

**F-05 NOTE (TESTED). The case block is confirmed by an independent derivation.**
- 127/127 checks; 47/47 mutations as expected; 6/6 byte mutations refused; the CLI codes M1-M6 and M8-M10 as listed in section 3.
- It is valid on r13 too (G-T3).

**F-06 NOTE (TESTED). CASE_BLOCK_ABSENT is gone; the sealed gates-only path completes.**
- G-S2 completes, with the 13 pre-seal PASS records and the gaps listed in section 5.
- G-S1 refuses SEALED_PIN_ADDENDUM_V005_PENDING while pins stay PENDING.
- M11 shows the A82 freeze hazard.

**F-07 NOTE (TESTED). Only the prereg's case-block sha protects the key map and the route mode.**
- `validate_case_block` admits a well-formed key-map entry on an allowed pointer, and route_a_mode serial_with_exemption with column_workers 8 numerics. The per-run column-workers check comes later, at r12 L2566.
- In sealed mode the binding's sha refuses any byte change (M1), and a differing CLI mode refuses (M3, M9).
- A test prereg that binds a modified block by its own sha is admitted (M7). Its GATES_ONLY body is byte-identical to the unmodified run's, because the body carries no prereg or case-block sha.
- The protection of record is therefore the chain: sealed compare, then V007_PREREG_SHA256, then the binding_inputs.case_block sha. RI-30 (the SEAL_RECORD key map equal to `[]`) should be enforced; the v002 builder README says it is (R-10).

**F-08 NOTE (TESTED). Seal tools v002 r2 behave as their README states on the scratch inputs.**
- D-01 is closed, D-04 runs the case block in the sealed-mode order, D-10 is enforced, the BUILD_V007 allowlist reads 15/15, and A-B1-class check records are refused (README; not re-probed here).
- Tool 5 output 25b4ff69 differs from the rehearsal draft 2a3e4308 only by the draft's `note` key. Checklist B2a still names the draft as the template; it should name tool 5.

**F-09 NOTE (FORMAL). The entry table A82-A101 is honest.**
- 20/20 section shas from bytes, by two methods.
- The four "no change" rows hold against the entry texts (section 2).

**F-10 NOTE (TESTED). The r4 to r5 delta is complete and traced.**
- 756 differing leaves, all inside DELTA rows 1-47 and erratum E1; every claimed revised clause differs; 187/187 pins verify.

**F-11 NOTE (FORMAL). Small text inconsistencies, all for a successor:**
- (a) The RI-20 and RI-21 statuses still state the r4 criteria ("three recheck lenses", "own check") without the A83 pointer that RI-24 got for A96.
- (b) The B2 clause runs "(<= 0.05 km/s) A94: ..." with no separator.
- (c) `seal_record_requirements[4]` (the order of record) omits the driver BUILD record creation that [8] and checklist B2a place before the sealed compare.
- (d) "r12 L5706" and similar line citations become r13 L5708.
- (e) Checklist A1 names r12, and checklist B1 says there is no entry after A101.

**F-12 NOTE (TESTED). BUILD_V007 does not name the case block's provenance.**
- It names plan V011 (whose registry field is c7023846) but not SPEC_REGISTRY, DRY_R5_MS128_V004 or the case block.
- The case block's dry-run provenance is pinned in BUILD_V005 and in the block's notes. The chain V011, registry, FILLED specs verifies from bytes.

**F-13 NOTE (TESTED). r5 fixes ngc_gas_M_s 96 on a lane record that no A-entry names.**
- The record is Codex1 0032 / GQ_NGC_91_MS96_V001 (PASS). It is consistent with RI-23.
- Root's checklist-A7 confirmation should be recorded in an A-entry or a seal-record note.

**F-14 NOTE (TESTED). The fence.**
- `tools/fence_c4v002.py` `{S:tools/fence_c4v002.py}` is the exact `{P:tools/fence_c4v001.py}` copy plus the two read-only exceptions, made by five anchored edits plus a path-predicate `selftest_v002()`. Diff: `out/FENCE_C4V001_TO_C4V002_R5CHK.diff` `{P:out/FENCE_C4V001_TO_C4V002_R5CHK.diff}`; its 5 removed lines are each replaced.
- In every fenced run: selftest 8/8, selftest_v002 24/24, **BLOCKED after the selftests []**, and my runner's extra stat/list guard refused 0.
- The only BLOCKED entry anywhere was the smoke test's deliberate write-open of V005.
- D-11 is closed for lane runs: G-S2 read the V004 and V005 addenda under exception (b).
- Three different v002 fences now exist (the r5 builder's 53078e39, seal tools' c993d34c, and mine), each documented.

**F-15 NOTE. Process disclosures.**
- One unquoted `echo ======` in a read-only `cat` chain tripped zsh `=`-expansion (rule 6). It errored after the first `cat` and wrote nothing.
- `tools/noop_r5chk.py` ends in a stray heredoc line. It is unused; `noop_r5chk_v2.py` supersedes it.
- The fence's own inherited selftest trial `read_runs_ext` realpaths a nonexistent probe under the runs_ext root. That stats the runs_ext root link and directory, never the C5H run or any UVT_* path.
- My session's primary working directory is Codex2's `review_v007_case_block_cx2/prereg_binding/`. Nothing was written there; every write used an absolute path inside `r5_check/`.

## Rules kept

- No launch.
- No `--validity-only`.
- No read, list or stat of `runs_ext/KMAX_A2F10_C5H_RUN_V001` or any `runs_ext/UVT_*` tree. The manifest names no run directory, and the runner's stat/list guard would have refused any such path; it refused 0.
- No NGC3198 target or observed-velocity data. From the GQ_NGC certificate I read only scalar fields.
- No recursive content search: `grep` ran only on single named files.
- Writes only inside `r5_check/`, each by exclusive create; PARTIAL.md is append-only.
- No deletes, moves or network.
- Python `-I -B`, numpy only, single-thread BLAS env vars. `taskpolicy -b` was accepted.
- Every sha comes from bytes, and every timestamp from `date -u`.

## Reproduction (shell names)

`PY=/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`; `D=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/r5_check`; `ENV="OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1"`; `RUN="$PY -I -B $D/tools/run_fenced_r5chk.py $D/tools/fence_c4v002.py {S:tools/fence_c4v002.py}"`. Every tool refuses an existing output, so use a fresh output name each time.
- Diff: `$PY -I -B $D/tools/diff_r4_r5_r5chk.py <r4.json> <r5.json> <NEW.json> <NEW.txt>`
- Entry shas: `$PY -I -B $D/tools/entry_shas_r5chk.py <addendum copy> <r5.json> <NEW.json>`
- Pins: `$PY -I -B $D/tools/verify_pins_r5chk.py <r5.json> <NEW.json>`
- Case block: `env $ENV $RUN $D/tools/case_block_check_r5chk.py <NEW.json> <NEW scratch dir>`
- Seal tool runs: `env $ENV $RUN <seal_tools_v002/r2 tool> <args as in out/V2_*.console.txt>`
- Compare runs: `env $ENV $RUN <compare> --prereg ... --manifest $D/scratch/rehearsal_r12/GATES_ONLY_MANIFEST_R5CHK.json --outdir <NEW> --gates-only [...]`. The exact argv of each G-*/M* run is in this folder's PARTIAL.md and console captures.

## Files (sha256 from bytes; HASHES.txt lists every file)

| file | sha256 |
|---|---|
| `out/CASE_BLOCK_CHECK_R5CHK.json` | `{S:out/CASE_BLOCK_CHECK_R5CHK.json}` |
| `out/DIFF_R4_R5_R5CHK.json` | `{S:out/DIFF_R4_R5_R5CHK.json}` |
| `out/ENTRY_SHAS_R5CHK.json` | `{S:out/ENTRY_SHAS_R5CHK.json}` |
| `out/ENTRY_SHAS_ON_COPY2_R5CHK.json` | `{S:out/ENTRY_SHAS_ON_COPY2_R5CHK.json}` |
| `out/PIN_VERIFY_R5_PREREG_R5CHK.json` | `{S:out/PIN_VERIFY_R5_PREREG_R5CHK.json}` |
| `out/G_S2_SEALED_B_GATES_ONLY/GATES_ONLY.json` | `{S:out/G_S2_SEALED_B_GATES_ONLY/GATES_ONLY.json}` |
| `out/V2_T3b.console.txt` | `{S:out/V2_T3b.console.txt}` |
| `scratch/rehearsal_r12/SCRATCH_INPUTS_R5CHK.json` | `{S:scratch/rehearsal_r12/SCRATCH_INPUTS_R5CHK.json}` |
| `tools/fence_c4v002.py` | `{S:tools/fence_c4v002.py}` |
| `tools/run_fenced_r5chk.py` | `{S:tools/run_fenced_r5chk.py}` |
| `scratch/V005_ADDENDUM_READ_COPY_2_R5CHK.md` | `{S:scratch/V005_ADDENDUM_READ_COPY_2_R5CHK.md}` |
