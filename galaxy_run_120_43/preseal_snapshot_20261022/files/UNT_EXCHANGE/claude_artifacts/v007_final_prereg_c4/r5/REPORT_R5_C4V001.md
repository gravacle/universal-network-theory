# REPORT: prereg r5 and the V007 case block (Claude4 r5 helper, A99 seal path)

UTC 2026-10-18T21:06:20Z (`date -u`). Folder `claude_artifacts/v007_final_prereg_c4/r5/`. Labels: **TESTED** (run or read from bytes here), **FORMAL** (follows from code or text read here), **UNTESTED**.

## Result

- **The V007 case block is built and reads valid under r12's own `validate_case_block` (TESTED).**
  - `case_block/CASE_BLOCK_V007_C4V001.json`, sha256 `76309ae39f23060cc662c4e218a41e1f95c56a26992402218a6198625f85ee71`, 89879 bytes.
  - Codex2 0507 checked it: PASS, zero findings. A101 rules it the case block of record, pinned as `binding_inputs.case_block` in r5.
- **Prereg r5 is built (TESTED: generated from bytes; audited against r4).**
  - `KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R5.json`, sha256 `3245899f68081a48928a7242a1d9f1ee3694bb13b3f04913dcb2825104a93393`.
  - It carries `binding_inputs.case_block`.
  - The BUILD of record is BUILD_V007, filled from bytes: `94bc05a5db1e6350b246c22e850ae62d95cd05ce21cdf5b329e3edded588a0de`.
  - Its entry table covers A82-A101 (16 revised here, 4 no change).
  - The compare slot rule is set for r12 cx3v002, the driver is r5, and `ngc_gas_M_s` is 96.
  - The seal checklist, root items, delta, clause map and hashes follow.
- **The seal is still not ready.** 10 root items are open (RI-28 to RI-37). The most important:
  - **RI-28, BLOCKING for the seal:** Claude3's r12 delta review of record (0083) reports 1 BLOCKING item (A-B1). Under A81 RI-20, r12 does not clear the compare slot until root rules.
  - **RI-29:** BUILD_V007's Claude4 delta check and Claude2 adoption are pending.

## 1. The case block (A99.2)

**What r12 requires (FORMAL, from code).**
- Requirements come from `validate_case_block` (r12 L1469-1583, with `tail_content_codes` L1402-1459) and from FIELDS_R12_CX3V002 section 4.
- The schema is UNT_KMAX_TAIL_V007_CASE_BLOCK_C2V003.
- Exactly 11 cases: the ten T-cases plus C5H.
- Each T-case carries:
  - its grid and truncation;
  - `tail` and `ro1_required` true;
  - `drivers_allowed` = [the sealed driver];
  - its `/numerics` registered whole;
  - `uv_tail_config_sha256`, the pinned library's `normalize_config` sha;
  - the A54 S8 tail content: P = 128, KLO 64 and KHI 256, cube K_out 5 for C5c, lambda 1.05 for C4T-A, nodes_v001 with the G5 ext_grid for D5, every other uv_tail key equal to C4T's, and gas M_s 128.
- C4T-D5's numerics equal the C5H reference outside `composite_grid_spec` and `uv_tail` (RA1, A50 S1).
- C5H carries tail and ro1_required false, call 60b46130 and drivers [999331af].
- In sealed mode the compare reads the block only from `binding_inputs.case_block` (L5706).

**Inputs, each verified from bytes (TESTED).**
- SPEC_REGISTRY_R5_MS128_CX1V004 `c7023846`: the ten FILLED specs.
- Plan template LAUNCH_PLAN_V010 `26f1ebf9`: the same ten FILLED shas.
- DRY_R5_MS128_V004 `ff60cd6b` and its ten dry reports: driver r5, no blockers, no unexplained refusals, each dry report naming its FILLED spec.
- All of these are byte-pinned in BUILD_V005 `46bc5b5d`.

**The recipe is Claude3's** (`validate_registry_r11_c3v001.py`; its r12 successors `validate_registry_r12_c3v001/_c3v002.py`).
- Each T-case registers its driver-r5 dry-run `normalized_spec.numerics`. The dry normalization only adds `/truncation/kmax_inverse_kpc`, on 9 cases. It changes or removes no spec leaf (TESTED).
- `route_a_mode` is parallel8 (A47 I4, A51).
- `key_equivalence_map` is [].
- The pinned-library uv_tail sha equals the driver-side `normalized_sha256` of every dry run (TESTED, 10/10).
- Both certificates are the A70 slots (EPS 598c8fa3, LO 1c384f76), and their files hash to their pins (TESTED).

**Validation (TESTED, under fence_c4v002).**
- r12 cx3v002 was exec'd unmodified in-process by `tools/load_r12_c4r5.py`.
- `validate_case_block` returns [] on the in-memory block, and [] again on the written bytes read back with r12's own `load_strict_file`.
- P = 128 and the registered gas M_s = 128.
- 193 of 193 build checks pass.
- 22 of 22 must-refuse mutations refuse, for example a schema change, a missing case, a retired label, an r4 driver, M_s 64, a KLO/KHI swap, a C4T-A alias, a tampered tail sha, a seed factor of 0.1, D5 numerics that differ from C5H, a bad key map, and S4T truncated as a cube.
- Record: `out/CASE_BLOCK_BUILD_C4V001.json` `bcf560de77cd42f67fedb62744df0723a052c1f2ffc4f4b2a7bed874eb5b59ad`.

**The sealed-mode path (TESTED).**
- I replayed r12's L5705-L5729 steps with r12's own functions.
- **On r5:** CASE_BLOCK_ACCEPTED (`76309ae39f23060cc662c4e218a41e1f95c56a26992402218a6198625f85ee71`).
- **On r4:** `CASE_BLOCK_ABSENT`.
- **A CLI `--route-a-mode serial_with_exemption`** refuses with `ROUTE_A_MODE_SOURCES_DIFFER`. So root's B6 commands must pass no route-A mode, or exactly parallel8.
- Record: `out/R5_PREREG_CASE_BLOCK_PATH_CHECK_C4V001.json` `b779391a2aa5e3af60d4da19decafbbd5fa655d8be59fe082e907de5114b6366`.

**Why the draft `6bf4ce5a` reads CASE_BLOCK_INVALID (TESTED, in layers, on in-memory copies).**
1. Its schema is C2V002, but r12 needs C2V003. This is the first refusal, and on its own it stops validation.
2. With the schema fixed, the case labels still include the retired C4T-K16 and C4T-K64 (A54, A56 require KLO and KHI).
3. With the labels fixed, 37 reasons remain:
   - every T-case has drivers_allowed = v010 r3 `4c14552f`, not r5 `b5cc62af`;
   - uv_tail_config_sha256 is a PENDING string, written before the specs were FILLED;
   - the pinned library refuses each uv_tail (UV_TAIL_CONFIG_INVALID);
   - C4T-D5 is "NOT_BUILDABLE", with unknown keys `refusal` and `status` and no `/numerics`;
   - K_big is 32 where A55 needs 128, and gas M_s is 64 where A57 needs 128;
   - the KLO, KHI and C4T-A tails are not distinct from C4T's.

The draft predates A54/A55/A57, the FILLED specs and driver r5.

## 2. Prereg r5

**The generator** is `tools/make_v007_final_draft_c4v005_p3.py` (`ef00666cd85ba280f781d8bbb16223573d915bec4f9b4fe503d20e4c23026a30`), in my folder `r5/tools/` because I may write only inside r5/.
- The first draft, `make_v007_final_draft_c4v005.py` (`f4de79cb9894ca6c10247cf5f1a11ddaa6f581c8a702d21e84195d162c006c4e`), refused in its own row/edit consistency check before writing anything: it compared `x[2]` with a logged `x.2`.
- `p2` (`4fd17fcc5c98be05145e717ac7ed20fdc2b7b7a9d17a763d45c682443be14e69`) fixed that; its dry run was inspected.
- `p3` added cosmetics, the registry V009 candidate and RI-37.
- p3 was chained patch, then dry run, then real run. Its dry run and real run gave the same prereg sha.

**What it does.**
- It reads r4 `e3b6b5b2` and every input from bytes; a prefix mismatch refuses.
- It reads the open V005 file once from bytes (`70a48f51`; byte copy `addendum_read/`) and builds the entry table.
- It refuses any entry from A82 onward that has no row.
- It finds BUILD_V007 by name and checks it:
  - exactly 15 distinct supported sources, each verified from bytes;
  - launcher v007 and guard v008 among them;
  - the predecessor BUILD_V006 `fb9e6a4a`;
  - the selected template LAUNCH_PLAN_V011_CX3V001 (`1b406591784ab4647e4aaf2686d9b3d18a259fadb435391439d2ff75df22ad3c`) launches exactly the case block's ten FILLED specs, with driver r5 and registry c7023846;
  - the template differs from V010 only in 51 output-path strings.

**The changes, each traced in `DELTA_R4_R5.md`** (47 edits, plus erratum E1 for three header bookkeeping leaves):
- **A99.2, D-03:** `binding_inputs.case_block` {path, sha256}, plus `case_block_rule`.
- **A99.1, D-02:** the launch-packet BUILD of record is BUILD_V007. `seal_record_requirements[10]` and `run_list.limits` name its launcher, guard and 15 sources; checklist B8 binds the same.
- **A99.3, D-05, R-02:** `entries_after_A81`, one row per entry A82-A101, each "revised here" (with clauses) or "no change, because ...", each with its section sha256 from bytes. A83 is "revised here": the compare rule's rechecks of record and the comparator's check of record. A99 and A101 are "revised here". The section rule is stated, and two shas were re-derived independently with sed and shasum.
- **A83, A86, A90, A91, A96:** the compare slot names r12 cx3v002 (`4bd7b262`; SELECTED 91aa9747; FIELDS 5cc95a06; IMPL ef0db32d; HASHES 3eb2912d) and its delta reviews of record, Claude3's and Codex2's, 0 blocking each. Its state is PENDING_ROOT_RULING, because Claude3 0083 reports A-B1.
- **A96:** the driver is v010 r5 and r6 is not a candidate. RI-24 and the cache slot are moot (`cache_directory_r6_only` = `NOT_APPLICABLE_R5`). The r6 branch text is removed from successors, the role table, memory guard, tail cache, identity gates, run list, the seal record requirements, the outcome tests and scope_untested.
- **ngc_gas_M_s = 96** (`fixed_across_all_cases.production_tail.ngc_gas_M_s`, value 96). It cites A81 RI-23 and Codex1 0032 (`3e8c9fc9`); the record `GQ_NGC_91_MS96_V001` (`be148bab`) reads PASS for NGC_T120L, M_s 96 against 192 on [2, 91]: 1.219e-15 and 2.335e-14 P0, both below 1e-12 (TESTED from bytes; rehearsal R-08).
- **A86:** GQ record of record GQ_CERT_V006 `5a1b39f8`.
- **A87:** the B3 record of record is the JSON `83c853b9`; DOUBLING is ea48ac2b with its M_s field `ddo_gas_M_s` (R-13, D-01); LO_NGC is V002 33bc2190.
- **A88:** SR_K moves after the seal.
- **A89:** the measured KHI cost.
- **A92:** c2v007r2 and the R5_V001 identity records.
- **A93:** the NGC registry named in the scope note.
- **A94, A97, A100, A101:** B2 follows its text exactly; the A97 decision rule; the A100 disposition and values of record; the C3V003 record of record. `seal_record_requirements[12]` repeats the B2 disclosure and the A101 erratum.
- **A82:** RI-27 resolved; no write to the open V005 file after the freeze.
- **Registry:** the candidate is C3V009 `32ddadcb` (Claude3 0087: V008 plus BUILD_V007's four post-seal producer pins). C3V008 `f189cd3f` stays as A101's baseline. The slot value stays PENDING for root.
- **SEAL_CHECKLIST_R5 adds:**
  - B2a, the driver BUILD record creation step. The template is the rehearsal's REHEARSAL DRAFT `2a3e4308` (D-06).
  - A6, with the 0598 B0 record `c2cec35b` as candidate (R-09).
  - The explicit later-entry list in B1 (D-05).
  - B8, bound to BUILD_V007's 15 sources.
  - A11-A14: the case block, BUILD_V007, B2 C3V003, and B0_N3/B0_RO1/I4.
- **Unchanged.** Every untouched r4 rule is byte-identical (TESTED by the audit: 1039 leaves differ from r4, and 1036 lie inside logged clauses). The other 3 are `revision` and `supersedes_draft`, recorded in erratum E1. By id, root items changed only RI-24 and RI-27.
- **No value is guessed.** Every value that waits on root carries PENDING_ROOT_AT_SEAL_ASSEMBLY or PENDING_ROOT_RULING (census in `out/AUDIT_R5_VS_R4_C4V001.json`).

**Seal tool 1 v001 on r5 (TESTED, dry-run mode, against the generation byte copy):** PASS. A46-A101 are cited (56 entries), all present, with no uncovered later entry.

**Seal tool 3 v001** is pinned to r4 and cannot check r5 by design. Seal tools v002 (a separate helper) should:
- pin r5 `3245899f68081a48928a7242a1d9f1ee3694bb13b3f04913dcb2825104a93393`;
- read `ddo_gas_M_s` (D-01);
- read the named build BUILD_V007 `94bc05a5db1e6350b246c22e850ae62d95cd05ce21cdf5b329e3edded588a0de`.

## 3. The fence

`tools/fence_c4v002.py` (`53078e39b34a22d1ee83e5b2d68c85e7644970838a2c88974397bb31912c1a4e`) is the exact copy `tools/fence_c4v001.py` (`f813c43099cfdadd3a779e395d223887d0df7cd8c8a8eb67b3a73de86eb699f0`) plus two read-only exceptions, documented in `tools/FENCE_C4V002_NOTE.md`:
- (a) uvt_*.py sources outside every runs_ext tree;
- (b) the CLAUDE2 V00*_ADDENDUM*.md decision records.

Every other block is kept. The diff is `out/FENCE_C4V001_TO_C4V002.diff` (`7dbeeb4bde414c459bdd7193bf44af18aaaf4928d0e2b6a7c5199b5d739ecb6e`).

Three fenced runs were made: CB1 (the build), CB2 (the path check) and T1 (seal tool 1). In each, selftest gave 8/8, selftest_v002 gave 17/17, and **BLOCKED after the selftests was []** (TESTED; console captures in `out/`). The loader's stat guard refused 0.

## 4. Open items (root and lanes)

- **RI-28, PENDING_ROOT_RULING (compare slot).** Claude3's r12 delta review of record (0083, 8fe311ba) is FAIL with 1 BLOCKING item, A-B1: in check_record_codes (r12 L875-879) an integer literal longer than 4300 digits raises a plain ValueError before the duplicate-key hook, so a duplicate-key check record falls to the text test and is admitted. Codex2's review of record (0485) reads 0 blocking. A81 RI-20 needs 0 blocking from each.
- **RI-29, PENDING (BUILD of record).** BUILD_V007 is the BUILD of record (A99.1). It landed (Codex3, 94bc05a5db1e6350b246c22e850ae62d95cd05ce21cdf5b329e3edded588a0de) and is filled here from bytes; its Claude4 delta check and Claude2 adoption are pending.
- **RI-30, RECOMMENDATION (rehearsal R-10).** The case block's own key_equivalence_map is [] and validate_case_block reads it; the SEAL_RECORD carries a separate key map (seal_record_requirements[3], A48 AMB-13). No tool checks that the two agree.
- **RI-31, PENDING_ROOT_RULING (checklist A6).** The candidate B0 record c2cec35b (Claude4 0598; registered in C3V007/C3V008) covers r5 against r4 on the registry V002 P128 rows at gas M_s 64; the production M_s 128 set (c7023846) has no r5 == r4 dry-identity row, and A55 ruling 2 asks for every spec (0598 independent check F3).
- **RI-32, PENDING_ROOT_RULING (owner).** CASCADE_MAP_R5_ADDENDUM (A69: the immutable inventory addendum naming the unreachable pin-only successor) is required before the seal on r5, has no owner and is not on disk (rehearsal GAP-18).
- **RI-33, PENDING (records not built).** B0_N3 (an r5 static guard scan), B0_RO1 parts (b) and (c) (replays) and I4 (a production run, C2T N8 against N1, whose N1 spec pair root fixes) are not built; their registry slots are empty and fail closed (rehearsal GAP-14; Claude3 0084).
- **RI-34, PROCEDURE (entries after the table).** The entry table covers A82-A101, the newest entry at r5 generation. Root may add entries before the freeze.
- **RI-35, NOTE (rehearsal D-09).** Seal tool 3 forbids changes outside seal_slots.<k>.value, so the sealed prereg keeps this draft's status line and the PENDING strings outside the slot values.
- **RI-36, PENDING_ROOT_RULING (driver check record).** PIN_V010_R5_CHECK has no A-entry naming it. Candidate: driver_r5/check/CHECK.md (89a6de88, the Claude-lineage r5 check, PASS_WITH_FINDINGS); Codex3 0602 (A69) is the other r5 check (rehearsal GAP-05).
- **RI-37, PENDING_ROOT_RULING (registry reading).** Claude3 0087 registers only aggregate_records v008 (9794123d) as the SR_K gate-record producer in C3V009; sr_k_static v009 (cc2eb3bb) writes per-state component records (schema UNT_SR_K_STATE_CX1V001), whose custody is a runbook item (r12 review note B-N3). PRODUCER_INDEX_V009_CX3V001 lists both under SR_K. The SR_K clause names both as the sealed pinned producers (A88).

## 5. Rules kept, and process notes

**Rules kept.**
- No launch and no compare `main()`. `--validity-only` was never run.
- No read, list or stat of `runs_ext/KMAX_A2F10_C5H_RUN_V001`. Nothing under `runs_ext/UVT_*` was opened. No NGC3198 target or observed-velocity data was opened. No recursive content search over broad trees.
- Writes were made only inside r5/. Every new file was created exclusively, by Python `open('x')`. Console captures were piped into an exclusive-create writer. The only appends were to my PARTIAL.md.
- No deletes, moves or network.
- Python: `-I -B`, numpy only, single-thread BLAS. `taskpolicy -b` was accepted.

**Disclosures.**
- One `echo =====` line tripped zsh `=` expansion (rule 6). It errored before running anything and wrote nothing.
- The fence's own selftest trial `read_runs_ext` (unchanged from v001) realpaths a nonexistent probe under the runs_ext root, and the fence refuses it. It stats neither the C5H run nor any UVT_* path (FORMAL).
- An `ls` of the CLAUDE2 control folder printed `runs_ext` as an entry name. Nothing inside it was listed.
- The open V005 file changed twice while I worked:
  - A100 was added between 20:22Z and 20:41Z;
  - A101 was added by 20:46Z.
  - Each change was copied by exclusive create (scratch copies 1-3), read in full, and integrated. It was unchanged at 21:04Z.
- **The state moved while I worked:**
  - BUILD_V007 landed at 20:44:19Z;
  - registry V008, then V009;
  - B2 C3V003;
  - Claude3 0083 (A-B1);
  - Codex2 0507 PASS on the case block.
  - r5 integrates all of these from bytes.

## Files (sha256 from bytes)

| file | sha256 |
|---|---|
| `case_block/CASE_BLOCK_V007_C4V001.json` | `76309ae39f23060cc662c4e218a41e1f95c56a26992402218a6198625f85ee71` |
| `out/CASE_BLOCK_BUILD_C4V001.json` | `bcf560de77cd42f67fedb62744df0723a052c1f2ffc4f4b2a7bed874eb5b59ad` |
| `KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R5.json` | `3245899f68081a48928a7242a1d9f1ee3694bb13b3f04913dcb2825104a93393` |
| `KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R5.md` | `2ed287717a831b422d93ad62339a85aa5b1ffbc570d39bd3ddc6066e8989c208` |
| `SEAL_CHECKLIST_R5.md` | `7ff81720e6cf108a6f71d478dcc23493fb1ee943ed2c90e88873715a2921bd13` |
| `ROOT_ITEMS_R5.md` | `2387dc23c790a894b6f969d133d48eb0a095f46ed97448fce67070ed59cdd3d4` |
| `DELTA_R4_R5.md` | `741cb7985125f1cb705a289001a329aee74c6c8314b80b1877a7c72d88e6fd4a` |
| `DELTA_R4_R5_ERRATUM_E1.md` | `b68a1f539cd0c6e9a4fe5bc4d841d0ceae7c2070a37bb05d2f4f09d46fdc10e8` |
| `CLAUSE_SOURCE_MAP_R5.md` | `378202ec67f93ddbee2233828ff18432af45b77f42d7c993321bb589ab340b31` |
| `ENTRY_TABLE_R5.md` | `b4bf8392db0ed5919b9583cf2f8b71b4d1ec26fd3c735cfd622e9cb81ac3063e` |
| `HASHES_R5.txt` | `21fe01a4a8f6d6888bdd32f15a8e2229987de8f9cff8d068500e113bfa2d1f8a` |
| `addendum_read/V005_ADDENDUM_READ_AT_R5_GENERATION.md` | `70a48f51e20311de82a37b13bee8cf18f7eaf9adbb976d957e50c5334e7c8c7e` |
| `tools/make_v007_final_draft_c4v005_p3.py` | `ef00666cd85ba280f781d8bbb16223573d915bec4f9b4fe503d20e4c23026a30` |
| `tools/make_v007_final_draft_c4v005.py` | `f4de79cb9894ca6c10247cf5f1a11ddaa6f581c8a702d21e84195d162c006c4e` |
| `tools/make_v007_final_draft_c4v005_p2.py` | `4fd17fcc5c98be05145e717ac7ed20fdc2b7b7a9d17a763d45c682443be14e69` |
| `tools/patch_gen_c4v005_p2.py` | `c331958a47b8523c5fbf432b91ebabdc11bb750a6d12fca64572b838e79982a1` |
| `tools/patch_gen_c4v005_p3.py` | `eded69a1669bc51a7ac9aa4d2419f1fa53f813d9f050873e6bdaedc53023759c` |
| `tools/build_case_block_c4v001.py` | `11823fe0e9c0dab0b3f47360e73f8a572e7259f534647eca3a3b257d96beaaae` |
| `tools/load_r12_c4r5.py` | `caf3ea9c795083133c351f7813f1d35f7fd8242f5dfacc324295896ff614e79e` |
| `tools/run_fenced_c4r5.py` | `d7b42e3a68a8354368899061d0d429a02b75abe4f8cca973ebea4367281fe1d5` |
| `tools/fence_c4v001.py` | `f813c43099cfdadd3a779e395d223887d0df7cd8c8a8eb67b3a73de86eb699f0` |
| `tools/fence_c4v002.py` | `53078e39b34a22d1ee83e5b2d68c85e7644970838a2c88974397bb31912c1a4e` |
| `tools/make_fence_c4v002.py` | `b1b3c01e921208fc8a3c9b15d0a33c0e3b251ba809e725de0ecb58452b58d3b0` |
| `out/FENCE_C4V001_TO_C4V002.diff` | `7dbeeb4bde414c459bdd7193bf44af18aaaf4928d0e2b6a7c5199b5d739ecb6e` |
| `tools/FENCE_C4V002_NOTE.md` | `03ab21284c907ab0a8b3305fea38a629b263990f66f9e799a05425754f57ab90` |
| `out/R5_PREREG_CASE_BLOCK_PATH_CHECK_C4V001.json` | `b779391a2aa5e3af60d4da19decafbbd5fa655d8be59fe082e907de5114b6366` |
| `tools/check_r5_case_block_path_c4v001.py` | `d451013a8aedaf8041639125bc97133b647a7e34825d70a152848139fc091f13` |
| `out/AUDIT_R5_VS_R4_C4V001.json` | `4374e85aea8a59ab418e2e6cb32e8d09bc23bdcf50d5fbc209ddeca18bd709ac` |
| `tools/audit_r5_vs_r4_c4v001.py` | `791ae9394fd613d26a913ed1318ca5e6242822786856d093da24a021679662d2` |
| `out/CB1_BUILD_CASE_BLOCK.console.txt` | `01a7be91fae1f30ca91ac74f2bba8169acdd2457c3a603040595ab32f23bf207` |
| `out/CB2_R5_CASE_BLOCK_PATH.console.txt` | `cae2e41f86d81b9608cc43a5f2a9cf2527efb347bd854109fb87f38506d47879` |
| `out/T1_R5_DRY_TOOL1.console.txt` | `eef86e229830d20b8c6294f0515deb9714819f2e2bcb973f2ec9442908d7d885` |
| `PARTIAL.md` | `dceafe5c04813e5898da49327b2df1998098bff450e07e983feb9d2e23c2071b` |

