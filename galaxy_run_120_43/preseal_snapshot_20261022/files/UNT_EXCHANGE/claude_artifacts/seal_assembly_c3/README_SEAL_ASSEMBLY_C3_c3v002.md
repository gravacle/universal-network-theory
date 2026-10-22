# README c3v002: the SELECTED seal pre-stage tuple (Claude3; fix round FROM_CODEX/0639 + 0640)

Written 2026-10-18T22:25:58Z (`date -u`). This supersedes `README_SEAL_ASSEMBLY_C3.md` (`2391590b`) for everything the fix round changes; that file stays for history. The selection is `SELECTED_SEAL_PRESTAGE_C3SA.json`. Codex1 delta-checks the tuple.

## The selected tuple

| role | file | sha256 |
|---|---|---|
| script (root runs it) | `ROOT_SEAL_STEPS_c3v007.sh` | e7409d93d17cdcde0e113ba971233fb59ade77157e2fe0b4a0c91f6b20b985cb |
| per-step helper | `tools/seal_steps_c3sa_c3v009.py` | 000798141398d27308d95e7a25fc64d17abe9831c47a2b27457439b7bc7922a3 |
| pinned-source runner (new) | `tools/run_pinned_c3sa_c3v002.py` | b57e4859c498bf57e05706dcd83d89db0f14102c33aec7359580c155d924861c |
| in-process fence (unchanged) | `tools/fence_c3sa_c3v003.py` | 9c62ad4902c895f0aeeba3a78976b5944146ee0de153989dbc79470528dd2863 |
| slot draft (unchanged) | `SLOT_VALUES_DRAFT.json` | c93691f5d1931beef8abb656ced3446c99d0adf286d4b5de0c709ecb570284ba |
| step-8 manifest draft (unchanged) | `MANIFEST_GATES_ONLY_DRAFT_C3SA.json` | e5967bb9901fda39703553c5c02b4d11a580ef8456f6c0b7d315ee4c750f09da |

Root runs `/bin/bash ROOT_SEAL_STEPS_c3v007.sh` after exporting the root inputs listed in its header. **Step 0 still refuses until seal tools v003 is pinned (P1).** Then a successor script swaps in the v003 pins (see the checklist in `README_SEAL_ASSEMBLY_C3.md`). The interface already matches v003: `--dispositions` and `--dispositions-sha` go to tools 1, 3 and 4.

## The three fixes

- **SA-CX1-B1: no metadata on a link target.**
  - `path_policy` no longer calls realpath or resolve. `nofollow_walk` lstats each prefix from `/`, never following.
  - A symlink component is refused **at the link**. Its own text (readlink) is checked for protected names and `/.vol`; the target is never stat'ed, resolved or opened.
  - Files are read through `O_NOFOLLOW`, with an inode match against the walk.
  - The identity-run check in ROOT step 8 uses the same walk.
- **SA-CX1-B2: no bytecode path.**
  - Every module the helper loads (fence, compare, guard) goes through `load_pinned`: read once, sha checked, then `compile` of that buffer and `exec` into a fresh module.
  - `run_pinned_c3sa_c3v002.py` does the same for the seal tools, their sibling modules (pre-loaded in order), the binder and the step-9 compare. An unpinned sibling import beside a pinned file is refused.
  - **Every Python process gets `-X pycache_prefix=<seal folder>/NO_PYCACHE_PREFIX_EMPTY`.** The folder is created empty in step 1, `-B` keeps it empty, and every step checks that it is still empty. This also neutralizes third-party `importlib` loads, including compare r13's own `load_pinned_module` (L694–L700, finding F1).
  - Preflight refuses before any Python runs if the seal folder already exists.
- **SA-CX1-B3 + PV-D05-1: the v003 dispositions contract.**
  - The input is only the v003 object `{schema, frozen_addendum_sha256, entries}`, with schema `UNT_V007_LATER_ENTRY_DISPOSITIONS_C4V001`. The key names and schema come from Claude4's v003 **dev work copies**: `seal_common_c4v003.py` L24 `101a3aeb` and `check_frozen_addendum_c4v003.py` L43–L45 `72d9191d`, read at 22:10Z. They are **PENDING v003 final**.
  - The bare-list, `dispositions` and `rows` forms are refused and removed from the helper and the script. The same pinned file goes to tools 1, 3 and 4.
  - Changed cited entries are detected byte for byte against the bytes the prereg's table was read from (r5 `addendum_read`, 70a48f51).
  - On a changed entry, plain `no_change` refuses. `revised` needs `prereg_revision`; that key name is mine and PENDING v003. `no_change_after_change` needs `changed_text`, present in the new section bytes and absent from the old, and a non-empty `why_no_prereg_effect`.
  - Plain `no_change` is accepted only for entries after the table.

## Tool order (stated, as 0639 asks)

README_SEAL_TOOLS of v002 (`da29c008`, L35–L40; **on disk, unposted**; v003 has not landed), with Claude4's numbers:

| step | tool |
|---|---|
| 2 | tool 1 check_frozen_addendum (after B1) |
| 2a | tool 5 print_driver_build_record (B2a; v001 has none, so the helper builds the identical record) |
| 4a | tool 3 check_slot_fill (after B4) |
| 5a | tool 2 check_sealed_compare (after B5) |
| 10 | tool 4 build_seal_record (B7) |
| 12 | tool 4 `--check-admission-config` (B8, v002/v003 only; the helper's guard v008 self-check stands in) |

0626 had listed "6. tool 2, 7. tool 3" after B5. The script now follows the README.

## MUST_FAIL controls (`mustfail_20261018T221642Z/`; all synthetic, inside this folder)

**B1** (`MUSTFAIL_RESULTS_C3SA.json` `1d07745a…`). The number is the count of stat, lstat, readlink, access, open, listdir and scandir attempts on the link target. Each attempt was blocked before its syscall. **Required: 0 for the new helper.**

| case | new c3v009 | old c3v007 (reproduction) |
|---|---|---|
| pin via an absolute alias to the protected look-alike | REFUSE / **0** | REFUSE / 4 |
| relative alias to the protected look-alike | REFUSE / **0** | REFUSE / 4 |
| two-hop alias (innocent first text) | REFUSE / **0** | REFUSE / 4 |
| alias to a runs_ext/UVT_* look-alike | REFUSE / **0** | REFUSE / 6 |
| alias to an innocent directory | REFUSE / **0** | REFUSE / 4 |
| output under an alias parent | REFUSE / **0** | REFUSE / 1 |
| dangling alias whose text is /.vol | REFUSE / **0** | not run (it would reach the real /.vol) |
| control: the canonical path | PASS / 0 | PASS / 0 |

**B2** (`b2/B2_RESULTS*.txt`; a stale `.pyc` with the matching header and a different payload is planted next to the correct source):

| case | result |
|---|---|
| old `_fence` pattern (importlib `exec_module`) | **UNPINNED_BYTECODE** (reproduction) |
| new `load_pinned` | **PINNED_SOURCE** |
| runner, tool-like main with a stale sibling `.pyc` | **PINNED_SOURCE** for both |
| runner, unpinned sibling import | **UNPINNED_SIBLING_IMPORT_REFUSED** |
| third-party `importlib` load under `-X pycache_prefix=<empty>` | **PINNED_SOURCE** (prefix stays empty) |
| importlib loader calls in helper c3v009 code | **0** |
| contrast: a plain sibling import | UNPINNED_BYTECODE (finding F2) |

**B3 / PV-D05-1** (17 cases, all as required):
- **Refused:** a bare list, the `dispositions` key, the `rows` key, a wrong schema, an extra top-level key, a row for an unchanged cited entry, an empty reason, plain `no_change` on a changed entry, a **generic `changed_text`** ("## A"), a **`changed_text` present in the old bytes**, a `changed_text` absent from the new bytes, an empty `why_no_prereg_effect`, `revised` without a pointer, and a changed entry left without a row.
- **Passed:** the v003 object for A102–A104; `no_change_after_change` naming the change exactly; `revised` with a pointer.
- The changed-entry cases use a **synthetic** frozen variant in which A90 gains one labelled fixture line (`SYNTHETIC_FROZEN_A90_CHANGED_NOT_ROOT_TEXT.md`).
- **v003 tool 1 on these fixtures is UNTESTED:** v003 has not landed, and its dev copy predates PV-D05-1.

## Dry run of record: `dry_run_20261018T222335Z/INDEX_DRY_RUN_C3SA.md`

- **Pass A** (faithful: v001 placeholders): steps 0–4 PASS. Step 4a, v001 tool 3, REFUSEs `TEXT_OF_RECORD_NOT_R4` as expected, and the script stops.
- **Pass B** (dry-run shim for tools 3 and 4): every step from 0 to 13 PASSes, with step 9 STUBBED.
- **Fence refusals: 0.** The pycache prefix stays empty.

## PENDING (changes since README c3v001)

- **The compare slot is ruled.** A104 (22:13Z): r13 `f5adfd11` with SELECTED_R13 `10acd098` is the compare of record, with both deltas at 0 blocking. Root still supplies it at invocation, and the script refuses r12, r11 and r10. The draft's marker text, "pending freeze", predates A104; the draft is unchanged, as the fix round asked.
- **The dispositions JSON** (root writes it at `CTRL/V007_SEAL_ASSEMBLY_INPUTS/COVERED_LATER_DISPOSITIONS_V007.json`) needs rows for **A102, A103 and A104** at the current V005 `acb7f44a`, plus any entry added before the freeze.
- **All other PENDING_ROOT and PENDING_ROOT_RULING items are unchanged** from README c3v001: RI-36 check record; EPS_NGC and I1T_NGC; the B7 inputs; CASCADE_MAP_R5_ADDENDUM; the C5H spelling; the free-space floor; the ack string; seal tools v003.

## Findings for other owners (FYI, both TESTED by analogy on synthetic modules)

- **F1 (compare r13).** `load_pinned_module` (L694–L700) checks the source sha, then runs `spec.loader.exec_module`. A header-matched stale `__pycache__/kmax_compare_c2v005.cpython-312.pyc` would execute instead of the pinned V005 compare. This is the B2 class. Here it is mitigated by `-X pycache_prefix=<empty>`; a compare successor could exec the verified buffer instead.
- **F2 (Claude4's seal tools).** They `sys.path.insert` their own folder and import their siblings through the import system. Run directly, they would execute a stale sibling `.pyc`. Here the runner (verified buffers, pre-loaded) and the pycache prefix close it.

The full file list, with superseded files, is in `SELECTED_SEAL_PRESTAGE_C3SA.json` and `HASHES_C3SA_c3v002.txt`.
