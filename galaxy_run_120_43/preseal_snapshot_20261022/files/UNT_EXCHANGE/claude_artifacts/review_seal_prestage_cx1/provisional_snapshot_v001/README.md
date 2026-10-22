# README: V007 seal-assembly pre-stage (Claude3 builder, dispatch 0626)

Written 2026-10-18T21:56:33Z (`date -u`). Root dispatch: FROM_CODEX/0626 (`c555ee94…`). Updates folded in: Claude4 0103 (prereg r5), 0629/0630/0632 (A102: compare r13), 0633/0634 with Claude4 0105/0106 (seal tools v003: dispositions JSON). The cross-check of this folder: Codex2 was named, but A103 reassigns it, finally to Codex1 (0636).

## What root runs

**`ROOT_SEAL_STEPS_c3v006.sh`** (`cb3aeb32…`) is the current script. `ROOT_SEAL_STEPS.sh` (`f7590383`) and c3v002 to c3v005 are superseded and kept unchanged, because files are never overwritten. It calls the pinned helper `tools/seal_steps_c3sa_c3v007.py` (`2f08fb88…`) and fence `tools/fence_c3sa_c3v003.py` (`9c62ad49…`), and verifies both from bytes. Run it with `/bin/bash ROOT_SEAL_STEPS_c3v006.sh`, after exporting the root inputs listed in its header. **Step 0 refuses by design until PENDING item P1 is closed:** the v003 tool pins go in a successor script, see the checklist below.

It stops at the first failure: `set -Eeuo pipefail`, and every helper and tool exits 2 on REFUSE. A STOPPED line goes to the terminal's stderr.
- Every file is created exclusively (`open(…,'x')`, noclobber, `mkdir`). Nothing is overwritten, edited or deleted.
- Every input is verified from bytes before its step uses it.
- It uses the pinned isolated Python (`-I -B`, with the realpath binary's sha checked) and single-thread BLAS. No network; process starts and network calls are fenced in the in-process steps.
- Before every step after the freeze, it re-checks that the open V005 file is still byte-equal to the frozen copy (A82, A99.6).
- **Nothing touches the registered C5H run except step 9.**

## Order of record and citations (V005 line numbers are those of snapshot 27b62183, `addendum_read/V005_ADDENDUM_READ_COPY_2_C3SA.md`; A103 shifts them by +12 in 643ef6ef)

| step | action | citation |
|---|---|---|
| 0 | preflight; writes nothing | SEAL_CHECKLIST_R5 L7 ("each complete before step B1"); RUNBOOK_V008 L19 (prescribed isolated Python) |
| 1 | exclusive FROZEN copy of the open V005, exactly the bytes root states | SEAL_CHECKLIST_R5 L23 (B1); prereg r5 seal_record_requirements[4](1); A81 RI-26 (L1270); A82 (L1255: "Once the frozen copy exists, root writes nothing more to this file"); FORMAT_V005 L14 (beside the open file); r5 `seal_slots.frozen_addendum.path_to_be` |
| 2 | dispositions JSON, tool 1 (check_frozen_addendum), entry-table re-hash | README_SEAL_TOOLS v001 L11 ("after B1"); SEAL_CHECKLIST_R5 L23; r5 srr[11]; 0633; Claude4 0105 |
| 2a | driver r5 + exclusive driver BUILD record | SEAL_CHECKLIST_R5 L24–L25 (B2/B2a); r5 srr[8]; A72; A96 |
| 3 | RUNBOOK_V008 L37 pre-binding output-root check; build-only binder | SEAL_CHECKLIST_R5 L26 (B3); A81 RI-25 (L1269); RUNBOOK_V008 L19; binder L18 (outputs NEW under its folder) |
| 3a | SLOT_VALUES_FINAL = the draft with run-time pins and root rulings | README_SEAL_TOOLS L27 (mapping), L33 (Slot JSON) |
| 4 | sealed prereg = r5 with every `seal_slots.<k>.value` filled | SEAL_CHECKLIST_R5 L27 (B4); README_SEAL_TOOLS L26; r5 srr[4](3) |
| 5 | sealed compare = the reviewed source with exactly the five pin lines set | SEAL_CHECKLIST_R5 L28 (B5); A82 (L1245); README_SEAL_TOOLS L28; r5 srr[4](4), srr[8] |
| 6 | check_slot_fill | README_SEAL_TOOLS L12 ("after B4") |
| 7 | check_sealed_compare | README_SEAL_TOOLS L13 ("after B5") |
| 8 | sealed `--gates-only`, fenced; its manifest names no case | SEAL_CHECKLIST_R5 L29 (B6); r5 srr[0], srr[1]; A46 RA13; A47 I3 |
| 9 | sealed `--validity-only --case C5H`, stdout to a file (**the only C5H step**) | the same |
| 10 | build_seal_record (prints the record; sha to stderr) | README_SEAL_TOOLS L14, L16–L22; SEAL_CHECKLIST_R5 L30 (B7) |
| 11 | exclusive SEAL_RECORD; its sha must equal tool 4's stderr | 0561 item 1.1; A81 RI-19 (L1263); README_SEAL_TOOLS L22 |
| 12 | exclusive ROOT_SEAL_ADMISSION config + the real guard v008 `admission()` self-check | 0561 item 1.2; A81 RI-19; FORMAT_V005 L7; guard v008 L8, L19–L43; SEAL_CHECKLIST_R5 L31 (B8); r5 srr[10] |
| 13 | exclusive SEAL_ADMISSION_RECEIPT naming the config and seal shas | 0561 item 1.3; A81 RI-19; FORMAT_V005 L8; SEAL_CHECKLIST_R5 L32 (B9) |

Steps 2a and 3a are inserted relative to 0626's list of 13. 2a is B2a of SEAL_CHECKLIST_R5: PIN_DRIVER_BUILD_RECORD must exist before step 5. 3a writes the slot file that steps 4 to 6 consume. Tool numbering: 0626 calls check_slot_fill "tool 2" and check_sealed_compare "tool 3", while Claude4's file headers number them the other way round. This script names the tools by file, and runs check_slot_fill before check_sealed_compare.

## PENDING_ROOT: created or supplied by root at assembly (exact paths)

`CTRL` = `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2`; `PKT` = `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1`.

| item | expected path | fixed by |
|---|---|---|
| FROZEN addendum | `CTRL/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM_FROZEN.md` | FIXED: r5 path_to_be; FORMAT_V005 L14; v002 D-10 enforces it |
| dispositions JSON (root writes) | `CTRL/V007_SEAL_ASSEMBLY_INPUTS/COVERED_LATER_DISPOSITIONS_V007.json` (the script requires the folder; the name is proposed) | 0633; Claude4 0105 format |
| driver BUILD record | `CTRL/V007_SEAL_ASSEMBLY/DRIVER_BUILD_RECORD_R5_V007_SEAL.json` | PROPOSED |
| bound plan | `PKT/P128/LAUNCH_PLAN_V011_CX3V001_BOUND_R5_V007_SEAL.json` | PROPOSED name; under the binder folder FIXED (binder L18) |
| bound command | `PKT/P128/LAUNCH_COMMAND_V011_CX3V001_BOUND_R5_V007_SEAL.txt` | the same |
| slot values (final) | `CTRL/V007_SEAL_ASSEMBLY/SLOT_VALUES_FINAL_V007.json` | PROPOSED |
| sealed prereg | `CTRL/V007_SEAL_ASSEMBLY/KMAX_TAIL_PREREG_V007_SEALED.json` | PROPOSED |
| sealed compare | `CTRL/V007_SEAL_ASSEMBLY/<reviewed basename>_SEALED_V007.py` (for r13: `kmax_tail_compare_c2v007_r13_cx3v001_SEALED_V007.py`) | PROPOSED |
| E-SEAL1 outputs | `CTRL/V007_SEAL_ASSEMBLY/E_SEAL1_GATES_ONLY_OUT/GATES_ONLY.json` (+ `.stdout.txt`), `…/E_SEAL1_VALIDITY_ONLY_C5H_OUT/VALIDITY_ONLY.json` (+ `.stdout.txt`), and the step-9 manifest `MANIFEST_VALIDITY_C5H_V007.json` | PROPOSED |
| SEAL_RECORD | `CTRL/V007_SEAL_ASSEMBLY/SEAL_RECORD_V007.json` | PROPOSED |
| ROOT_SEAL_ADMISSION config | `PKT/ROOT_SEAL_ADMISSION_V001.json` | FIXED: guard v008 L8 CONFIG; FORMAT_V005 L7 |
| SEAL_ADMISSION_RECEIPT | `CTRL/V007_SEAL_ASSEMBLY/SEAL_ADMISSION_RECEIPT_V001.json` (schema name `UNT_ROOT_SEAL_ADMISSION_RECEIPT_V001` PROPOSED) | PROPOSED |
| compare reviewed source | root-supplied path and sha. The candidate is r13 `v007_compare_c2/r13/kmax_tail_compare_c2v007_r13_cx3v001.py` (`f5adfd11…`), with `SELECTED_R13_CX3V001.json` (`10acd098…`). | A102 |
| B7 inputs | the key-equivalence map, NEW-item disposition list and raw successor-custody record (root-supplied path and sha; v002 defines their JSON forms) | GAP-17; RI-30; A81 RI-20; A59 |
| CASCADE_MAP_R5_ADDENDUM | root-supplied path and sha (required before the seal on r5) | r5 srr[9]; A69; RI-32 |
| step-8 manifest | `MANIFEST_GATES_ONLY_DRAFT_C3SA.json` (`e5967bb9…`). This is a DRAFT: the 13 registered gate records, and identity_runs = the R5_V001 records' run.path strings. Root confirms the three UVT_* run directories (a root-only read). | this builder |
| step-9 C5H spelling | `UNT_SEAL_C5H_RUN_DIR`: one of the sealed compare's `C5H_REGISTERED_RUN_DIRS`, compared as a string only | root |

Each `V007_SEAL_ASSEMBLY` path takes `_ATTEMPT_n` on attempt n > 1 (`UNT_SEAL_ATTEMPT`). On a later attempt the FROZEN copy is reused only if it holds exactly the stated bytes.

## PENDING_ROOT_RULING (candidates)

| item | candidates (verified from bytes) | note |
|---|---|---|
| compare slot (RI-28, resolved to A102) | r13 `f5adfd11ea7ecc982ba7650944f6a6d69eeff8be690bde6265a18d07d3bb2157`, SELECTED_R13 `10acd09887bffa5130e2ebbff7d54ab2d70ea7aff0fb2cd696e0cda0fcf6bb5e` | waits for two 0-blocking delta reviews: Claude3, and Codex1 substituting for Codex2 (A103). The script refuses r12, r11 and r10 as the reviewed source. |
| driver check record (RI-36) | `driver_r5/check/CHECK.md` `89a6de88739e1c4b76c39dc11d7417d7e243b7235511d8ea0951e1493865b632`; Codex3 0602 `review_r5_certs_cx3/R5_REVIEW_FINAL_V001.md` `6758bd24784ec514d73054a30a8fdd673c3d0c571521a62514ba4260f3ad7ba9` | both pass r12's `check_record_codes` (TESTED in-process). Any other record needs a successor draft. |
| certificates.EPS_NGC (GAP-12; SEAL_CHECKLIST_R5 A7 "root confirms") | `certificates_ngc_k32/gates/EPS_CERT_NGC91_V001.json` `1d5eef1b602d2489ba8c0e652156555bbd2bfddf083931c7c4c82fa0a1e0c13d` | the single candidate. A70 assigns the NGC K32 tree, and this is the only EPS record in it. No sha-level ruling. |
| certificates.I1T_NGC (GAP-12) | `certificates_v002/gates/I1T_NGC_T120L_V001.json` `3ae7981a0c022d50a153a0857b10660661fedfd5adedcba3b805802b4a1809b6` | the single candidate. No A-entry names it, and it states no M_s. |
| RI-29, RI-30, RI-31, RI-32, RI-33, RI-34, RI-35, RI-37 | ROOT_ITEMS_R5 (`2387dc23…`) | acknowledged by the exact `UNT_SEAL_ROOT_ACK` string. RI-33: B0_N3, B0_RO1 and I4 are MISSING and fail closed in gates-only. |
| covered-later (RI-34) | the entries after A101 at the freeze: **A102 and A103 as of 21:53Z** | each needs a row in the dispositions JSON |

## Slot values filled from bytes (SLOT_VALUES_DRAFT.json `c93691f5…`; schema UNT_V007_SEAL_SLOTS_C4V001)

driver_branch `r5` (A96); ngc_gas_M_s `96`, supported by r5 `production_tail.ngc_gas_M_s`, GQ_CERT_V006 `gas_M_s_NGC` 96, compare `NGC_GAS_M_S_A57`, and Codex1 0032's GQ_NGC_91_MS96_V001 `be148bab` (A81 RI-23 not triggered).
- driver: b5cc62af
- identity_comparator: c2v007r2 052da0fe
- identity_gate_records: Z2 = B1 83e7b067, Z2_OFF_RO1 = B1_OFF 3b9ad402, B0prime_RERUN e33af53d
- launch_packet.build: BUILD_V007 94bc05a5
- certificates: EPS 598c8fa3, LO 1c384f76, GQ V006 5a1b39f8, DOUBLING ea48ac2b, LO_NGC V002 33bc2190
- producer_registry: V009 32ddadcb
- cache_directory_r6_only: `NOT_APPLICABLE_R5`

Every filled value equals prereg r5's `named_candidates_verified_from_bytes`, asserted by `tools/make_slot_draft_c3sa.py`. **Cross-reference, not slots** (`SLOT_XREF_C3SA.json` `4bd214a8…`):
- B2 C3V003 `915fbcda` (`gate_b2_c3/out/B2_GATE_RECORD_C3V003.json`)
- B3 `83c853b9` (`seal_records_c4/build/records/B3_RECORD_C4V001.json`)
- B0 c2cec35b, B0prime_DRY 7842d2a7, B0_FA 888488cd
- case block `76309ae3` (= r5 `binding_inputs.case_block`)

Every slot record and every cross-reference record is listed in registry V009's `gate_records`. Its identity_comparators and identity_tokens match the records.

## Path strings (README L32; r4 N7) and the firmlink

The binder pins `str(Path(p).resolve())`. For all 47 slot and binder paths, realpath, `Path.resolve()` and the binder's own `pin()` (run in-process) equal the literal `/Users/...` string (`evidence/PATH_RESOLUTION_C3SA_V001.json`). The one exception is `python3`, a symlink to python3.12, which is only ever used as a literal.
- `/System/Volumes/Data/...` names the same inode, but realpath does **not** normalize it. So an absolute firmlink-spelled argument would pin a second spelling that launcher v007 and guard v008 compare as unequal.
- `getcwd()` reports `/Users` even after a `cd` to the firmlink spelling (`evidence/FIRMLINK_CWD_PROBE_C3SA_V002.txt`).
- The helper refuses any non-`/Users/` or non-canonical spelling, `/private`, `/.vol`, `..` and `//`.

## Seal tools: v001 placeholders now; v003 successor checklist

The coordinator directed v001 placeholders until v003 is posted. `seal_tools_v002/` is now on disk (README `da29c008`, tool set of record `r2/`) but has not been posted, and 0639 ruled it FAIL on D-05. v003 = r2 + D-05 + B8 (Claude4 0105/0106). **The successor script (c3v007) must:**
1. Pin the v003 files: seal_common and tools 1–5. Set `SEAL_TOOLS_STATUS` and `T_DISPOSITIONS_FLAG_STATUS=PUBLISHED`. Mode `v003_dispositions` already passes `--dispositions D --dispositions-sha H` to tools 1, 3 and 4. v003 removes `--covered-later`.
2. Use the v002/v003 slot schema (`UNT_V007_SEAL_SLOTS_C4V002`, or v003's name). It has two more keys: `cascade_map_r5_addendum` {path, sha256}, which is root input P7, and `admission_entry` {launcher 861bba68, guard 294cb776}. That means a successor SLOT_VALUES_DRAFT, with the helper's SLOT_KEYS following it.
3. Add `--text-of-record-sha <r5 sha>` to tools 3 and 4 (v002 README "Text of record").
4. Give tool 4 the compare's own `GATES_ONLY.json` and `VALIDITY_ONLY.json` (R-04), not the stdout captures. Add `--b2-record` (B2 915fbcda; A100; r5 srr[12]).
5. B2a: use tool 5 (`print_driver_build_record`) with exclusive write, or keep this helper. **Use one method only.** The bytes differ only in the helper's `note`; this helper's record is deterministic (`d9226430…` for r13 + CHECK.md).
6. Add the B8 check `--check-admission-config <config> --seal-record <SEAL_RECORD>` after step 12.
7. **D-10 consequence:** v002/v003 require the frozen copy exactly at path_to_be. A scratch dry run of tools 1, 3 and 4 is then impossible without a tool-side dry-run allowance. **R-04 consequence:** the step-9 stub would have to imitate VALIDITY_ONLY.json. Both need deciding before a v003 dry run.

## Residual risks and limits

- **A82 hazard.** Compare r13 hashes the **open** V005 path. Any write to it after the freeze breaks the sealed compare. The script re-checks before each step but cannot police later writes. The open file changed three times during this build: 70a48f51 → 27b62183 (A102) → 643ef6ef (A103). Root freezes exactly what it reviewed.
- **Step 8 in ROOT mode** reads the three UVT_* identity-run trees (B6). Before that read, it scans them with no follow and refuses any symlink. The fence refuses C5H spellings only.
- **Attempts.** A failure after step 1 leaves partial outputs, which are never deleted. `UNT_SEAL_ATTEMPT=n` gives fresh names. The config path is fixed, so a failure after step 12 needs root handling.
- **v001 tool 4** writes generic no-change notes (the D-05 defect). v003 carries the dispositions instead.
- **Not verified here** (root-only, or not yet landed): the identity-run trees and the C5H run; raw successor custody; the internal output volume beyond an st_dev comparison; v003's acceptance of these inputs; the BUILD_V007 delta (RI-29); the r13 deltas.

## Process notes and errata

- E-C3SA-1: `evidence/FIRMLINK_CWD_PROBE_C3SA_V001.txt` has a conclusion line written before the measurement. It is wrong for the relative-path case; V002 is correct.
- E-C3SA-2: an over-broad key filter printed the LO_CERT_V004_MS128 `v_state_km_s` and `tau_km_s` arrays to my context. These are saved-C4R3 model state speeds and V005 tolerances, not targets or V007 results.
- Superseded before use: helper c3sa…c3v006 (a false positive on the manifest note, in dry run 2), fence c3sa and c3v002, script versions 1 to c3v005, and earlier dry runs. Each defect is listed in PARTIAL.md.
- The fence self-test: non-strict `posixpath.realpath` swallows the fence's PermissionError (an OSError). The syscall is still never made and the refusal is counted, so every guarded step requires a refusal count of 0.
- Dry run of record: `dry_run_20261018T215307Z/INDEX_DRY_RUN_C3SA.md`. File hashes: `HASHES_C3SA.txt`.
