# pinned_input_envelope_c2v003: one read per inode (Codex1 0164, CX1-ENV-01)

This is the immutable successor of `pinned_input_envelope_c2v002` (`0fac239a`). A Claude2 root builder made it for the one blocking finding in Codex1's review 0164. Root chose the fix: **share one read keyed by (dev, ino)**. Each alias still records its own path, and the manifest marks aliases with `alias_of`.

Only the read and caching path changed. Everything else is c2v002 as built, including the rulings D1 to D7 and errata E1, which is carried below. The c2v002 README (`bcf34ecb…`) still describes the tool, apart from the delta in this file. This folder was created new, and nothing existing was edited.

| file | sha256 |
|---|---|
| `pinned_input_envelope_c2v003.py` | `9d531381615f7b68f2f33bfc19f0aa2bcfe97a4e6f5c0e93187ea8eb35ce8d9a` |
| `tests/test_pinned_input_envelope_c2v003.py` | `2bcfc1b8a78319b1162aa546ab9a39994f6e1cacef8e4e4b344a201a79067e9b` |
| `tests/mutation_check_c2v003.py` | `7d94e191986793289bb5d3a0e0c2c975b877df66235f9ff7871e42561fcc080a` |
| `tests/ast_delta_c2v003.py` | `a05c67e42a57c30bc5ca2c18c157ffbd5b9a28d80052cafd59353b484f472c99` |

`HASHES_PINNED_INPUT_ENVELOPE_C2V003.txt` lists these files, this README and every result record.

## The finding

**CX1-ENV-01** (Codex1 0164, `OWN_CHECKS.json` and `own_checks_cx1.py`):
- c2v002's snapshot grouped files by realpath. Two hard-link paths to one regular file are two realpaths, so each was opened and read. The same inode was read twice, and the exit was 0.
- `OneRead.get` in collect had the same realpath-only cache.
- Codex1 scoped this as a contract violation of A226 item 1 (single read). It found no unhashed bytes accepted and no scientific result implicated.

## The fix

**The key.** The one read is keyed by the file's identity: the (dev, ino) that fstat reports on the `O_NOFOLLOW` descriptor that was read.

**Snapshot and collect handle a realpath the same way:**
1. Before opening a realpath, the tool takes its identity with `os.lstat`. This opens nothing and does not follow a symlink. If that identity is an inode already read in this subcommand, the realpath takes that read's result and is **never opened**.
2. Otherwise `read_once` opens it with `O_NOFOLLOW` and fstats it. If the descriptor turns out to be an inode already read (the name changed between the lstat and the open), the descriptor is **closed before any `os.read`** and the realpath takes that result.
3. In both cases the name takes the shared result only if its own stat still matches the read on all of these: `size`, `mtime_ns`, `ctime_ns`, `ino`, `dev`, `mode` and `nlink`. Its own stat is the lstat from step 1, or the fstat on its descriptor from step 2.
   - If any of them differs, the inode changed after its one read, or its number was reused.
   - The name is then `changed_during_read`, with its own metadata and no sha. That is never a match, and the file is not read again.

So each inode is content-read at most once per subcommand. Only the race in step 2 opens a second name, and it is opened and fstat'ed only, never read.

**Alias marking:**
- **Snapshot** still writes one file entry per realpath. Each entry keeps its own `file_key`, its own pins and resolution, and its own `content_guard` and `hash_only`.
  - Every entry now has `alias_of`. It names the realpath that was read, or is `None` for an entry that was read itself.
  - The primary of an inode is its sorted-first realpath.
  - Manifest `counts` adds `n_alias_files`.
- **Collect:**
  - The pin set adds `read_aliases`, a list of `{realpath, alias_of}` for each document realpath that shared another's read.
  - In `counts`, `n_files_read` is now the number of realpaths read on their own (one per inode). Before, it was every realpath reached.
  - `counts` adds `n_read_aliases`.
  - The primary is the first realpath reached.

**Version names.** These are now `c2v003`: `TOOL` and the schemas `UNT_PINNED_INPUT_ENVELOPE_{PINSET,MANIFEST,COMPARE}_C2V003`. So c2v003 refuses a c2v002 pin set or manifest with `INPUT_WRONG_SCHEMA`. **Root takes a phase's pin set, START and END all with one tool version.**

## What did not change (AST check)

`tests/ast_delta_c2v003.py` does the following:
- reads c2v002, checking it against `0fac239a` from its bytes, and reads c2v003;
- compares their top-level statements by name, ignoring line numbers;
- passes only when every difference is in the allowed list.

Run `ast_delta/RUN_20261020T195528Z_79677/AST_DELTA.json` (sha256 `66c4c08482721224e3185085bfe2b4d0afff05aa4a7c951e02be104fc670af24`) gave **PASS, 0 problems**.

| result | names |
|---|---|
| identical | 68 of c2v002's 77 top-level names. These include `compare`, every guard (`never_open_reason`, `content_guard`, `pin_path_problem`, `check_out`, `load_signed`), `resolution`, `walk_pins`, the V006 and pointer parsers, `write_signed`, the CLI and every D1-D7 constant. |
| changed: version only | `TOOL`, `SCHEMA_PINSET`, `SCHEMA_MANIFEST`, `SCHEMA_COMPARE` (c2v002 to c2v003 and nothing else), and the module docstring |
| changed: read path | `read_once` gains the `read_ids` argument, its docstring, and one `if` after the exclusion check. `OneRead` changed. |
| changed in `collect` | Only the statement that builds the pin set: it adds `read_aliases` and `counts/n_read_aliases`, and changes `counts/n_files_read`. |
| changed in `snapshot` | Only these: the added `read_by_id = {}`, the read loop `for rp in sorted(by_file)`, and `counts/n_alias_files` added to the manifest. |
| added | `ALIAS_READ`, `FILE_ENTRY_OWN`, `_lstat_id`, `_rec_id`, `_share` |
| removed | none |

As a builder check in scratch (not a package record), the script was also run against five copies of c2v003, each with one out-of-scope edit:
- compare ignores a sha change;
- another collect statement changed;
- the snapshot pin entries changed;
- an extra pin-set key;
- a different `TOOL` string.

It returned FAIL on each.

## Choices beyond the ruling (disclosed)

1. **What is shared.** Any result that carries the descriptor's fstat is shared: `ok`, `changed_during_read`, `not_regular`, `too_large`, and `excluded_not_read` reached by inode. A result with no descriptor is never shared, and that name is handled on its own exactly as in c2v002. These are `missing`, `unreadable`, `symlink_at_open`, an exclusion by realpath, and collect's guarded `hash_only`.
2. **The metadata check** (step 3 above) goes beyond "keyed by (dev, ino)". Without it, a name could carry a result from before a change, or a reused inode number could take another file's result. With it, either case is `changed_during_read`, which never matches, and there is still no second read. Rows H08 and H08b test it, and mutant M55 removes it.
3. **The pre-check uses `lstat`, not `stat`.** A symlink swapped in at a realpath after resolution therefore matches no inode that was read. It is opened `O_NOFOLLOW` and gives `symlink_at_open`, as in c2v002.
4. **Exclusion comes before sharing.** An excluded realpath is still not opened. In `read_once`, the excluded-inode check comes before the already-read check.
5. **The guard comes before sharing in collect.** A guarded name never takes a shared buffer. In H02, an NGC3198-named hard link of a followed document stays `hash_only`, is never opened and is never parsed.
6. **Collect parses an alias document's shared buffer** once for its own spelling. The `followed` set is still keyed by (realpath, sha), as in c2v002. So the pins found in it carry both spellings as sources, and there is no second read.
7. **`compare` is unchanged** and does not compare `alias_of`. A name that joins or leaves an inode always changes its `ino`, so the result is `FILE_REWRITTEN` and INVALIDATE (H04, H04b).
8. **Pinned files that collect never opens** (all of them at depth 0) have no alias information in the pin set. `read_aliases` covers only the documents collect read. Snapshot marks aliases among all pinned files.

## Errata E1 (carried from c2v002, `README_ERRATA_C2V002_E1.md` sha256 `048ad43ec7231caaabaf2b32d4139248aeb49e94d16e832c02cb091746cc6faa`; in force for c2v003)

1. **F1, shell.** The command blocks rely on word splitting of variables such as `$C1_SCOPED`, which zsh (this host's shell) does not do. **Run every command block with `/bin/bash`**, or write the arguments out, or use zsh's `${=VAR}`. Root runs them under `/bin/bash`.
2. **F2, the S0 row.** The S0 gate file is `--doc-pin 5e688882451824931f964e610cf17597d82ee0eb246fb0dce528ec0c6e148042 /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s0_launch_kit_c2/GATE_DOCUMENT_PINS_V002.json`. This is the full sha256. It matches V006 L1245 (verified from bytes by the c2v002 independent verifier).
3. **Operating rules that follow from D4:**
   - **Root never chmods a pinned input.** A chmod, or an added hard link, reads INVALIDATE (the carried C09 and C10).
   - **No pinned input is opened in a GUI app during a phase.** An xattr value rewrite reads INVALIDATE.
   - New in c2v003: hard links that already exist among pinned names at START are read once and marked. A name that is split from, or joined to, an inode during the phase reads INVALIDATE (H04, H04b).

## Commands

The c2v002 README's command block, per-phase table and notes apply unchanged. Make two substitutions:
- the tool line becomes `T=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/pinned_input_envelope_c2v003/pinned_input_envelope_c2v003.py`;
- E1 F1 and F2 apply.

The steps, exit codes and the D1, D3 and depth rules are c2v002's.

## Verification (synthetic)

**Tests.** Each run has 94 MUST_PASS rows.
- The 82 c2v002 rows are carried unchanged under their ids.
- 12 rows are new, in group H.
- The H rows count reads in two independent ways:
  - the tool's `os` is an `InodeCounter` that counts opens and content reads per inode, using the **test's own** fstat on every descriptor the tool opens;
  - the audit hook's opens per path are summed per inode.

| row | what it shows |
|---|---|
| H01 | Codex1's repro (`input.txt` plus a hard link) in snapshot. Exit 0. The inode is opened once and read once (counter and audit). There are two entries, and the second name is `alias_of` the first. Both pins match on their own realpaths. |
| H02 | Collect with a root document plus its hard link (`--walk-only`) and a followed document plus its hard link. Each inode is opened once and read once. `read_aliases` lists both. Both are followed, and their pins carry both spellings. An NGC3198-named link stays `hash_only` and unopened. |
| H03 | Four names of one inode, one of them NGC3198-named. There are four entries, each with its own key and guard. `alias_of` points to the sorted-first name, and `n_alias_files` is 3. A symlink to one name resolves to it and adds no entry. One mismatching pin gives exit 3. |
| H03b | The same alias set at START and END. Both exit 0, with the same marks. Compare is OK with no problems and no notes. |
| H04 | Split: an alias at START is replaced by its own inode with the same bytes and mtime. END reads each inode once and clears `alias_of`. Compare is INVALIDATE, with `FILE_REWRITTEN` (ino) on that name. |
| H04b | Join: two inodes at START, then one name becomes a hard link to the other. END reads the inode once and sets `alias_of`. Compare is INVALIDATE, with `FILE_REWRITTEN` (ino). |
| H05, H05b | The descriptor check, in snapshot and in collect. The alias's lstat pre-check is hidden. The alias is opened and fstat'ed (2 opens) but read once only. It is marked. The snapshot entry equals the one from the normal path. |
| H06 | A symlink alias behaves as in c2v002: one entry, `alias_of` None, one open and one read, and `final_symlink`/`readlink` recorded. Collect follows a symlinked document once, with no read alias. |
| H07 | The CLI through the codex python, on a hard-link pair. collect, START, END and compare all exit 0. The manifest marks the alias, and the summary counts it. |
| H08, H08b | The inode changes (its mtime moves) right after its one read. The other name is `changed_during_read`, keeps its own metadata and gets no sha. It is never read again. Snapshot exits 3 on both paths. In collect it is a collect problem, and collect exits 3. |

| run | result | TEST_RESULTS.json sha256 |
|---|---|---|
| `test_runs/RUN_20261020T195428Z_78333` | 94/94 pass, audit 0 refused | `acbbbb4997d40bede9549b75bf6988059ea8877af8a667252cda9d852f9d8a2b` |
| `test_runs/RUN_20261020T195430Z_78380` | 94/94 pass, audit 0 refused | `5a6b55b9989d4e5f5705e8a3b858657618345bc65307761232948d1659bedb6b` |

Both runs show tool `9d531381…` and test `2bcfc1b8…`. The only subprocess was the codex python, 17 times per run.

**Contrast.** The same suite was run against the unchanged c2v002 tool (`0fac239a`), in `contrast_c2v002_runs/RUN_20261020T195539Z_79687`, TEST_RESULTS.json sha256 `5121470442809a5f0cc84e15ffd83040b513893d36c7b60c2af3ecfe298b0098`.
- **82 pass and the 12 H rows fail.**
- H01 counts 2 reads and 2 opens of the one inode, and H02 counts 2 reads of each inode. These are CX1-ENV-01 reproduced by the new rows.
- H06 fails on c2v002 only because c2v002 has no `alias_of`, `n_alias_files` or `read_aliases`. Its symlink behaviour passes.

**Mutation check** (`mutation_runs/RUN_20261020T195436Z_78406`, MUTATION_RESULTS.json sha256 `a28cbd33c7ff5e6d361ea3199cc528fd9ef2c583ed429720f4bfc08278326184`): the baseline passed 94/94, and **55 of 55 mutants were killed**.
- M01 to M45 are carried from c2v002 with the same intent. Two anchors were re-taken because their code moved:
  - M19 now clears both cache layers before every get. Rows P09, H02, H05b, H06 and H08b kill it.
  - M26 matches the new call. Row D1_05 kills it.
- M46 to M55 are new:

| mutant | what it does | killed by |
|---|---|---|
| M46 | snapshot goes back to realpath-only caching (both layers) | H01 H03 H03b H04 H04b H05 H07 H08 |
| M47 | collect goes back to realpath-only caching (both layers) | H02 H05b H08b |
| M48 | snapshot has no descriptor identity check | H05 H08 |
| M49 | collect has no descriptor identity check | H05b |
| M50 | snapshot has no lstat pre-check | H01 H03 H04b H08 |
| M51 | collect has no lstat pre-check | H02 |
| M52 | the manifest does not mark aliases | H01 H03 H03b H04 H04b H05 H07 H08 |
| M53 | the pin set does not list read aliases | H02 H05b H08b |
| M54 | `read_once`'s descriptor check is removed at its source | H05 H05b H08 |
| M55 | `_share` has no metadata check | H08 H08b |

## Tested and untested

- **TESTED-POSITIVE**, as listed above and on synthetic fixtures only:
  - one content read per inode in snapshot and collect, counted independently;
  - alias marking;
  - an alias's inode changing between START and END reads INVALIDATE;
  - the descriptor check;
  - the metadata check;
  - symlink behaviour unchanged;
  - all 82 c2v002 rows;
  - AST identity outside the read and caching path.
- **UNTESTED**, each with the test that would decide it:
  - A real-input collect or snapshot with c2v003. The deciding test is root's first depth-0 collect and START snapshot of a phase, with the read counts in the pin set and the manifest.
  - Inode-number reuse inside one snapshot is not simulated. The metadata check covers it by design. The deciding test is a fixture that deletes the primary after its read and recreates a file at the same inode number before the alias check.
  - Hard links across devices are impossible by construction, so this has no test.
- **Disclosed, unchanged (N6).** `O_NOFOLLOW` protects the last path component only.

## What the build read

The build read:
- the c2v002 package: tool, tests, README, errata E1 and HASHES;
- Codex1's review folder `review_final_deltas_cx1/ENVELOPE_C2V002_REVIEW_CX1_V001/`: `REVIEW_RESULT.json`, `OWN_CHECKS.json` and `own_checks_cx1.py`;
- the codex runtime python.

It did not open NGC3198 data, run outputs, V007_POSTSEAL_RECORDS, V006, `/Volumes` or `~/.codex`, and it used no network. All fixtures are synthetic, under this folder's `test_runs/`, `mutation_runs/` and `contrast_c2v002_runs/`, and the audit hook refused nothing. No existing file was edited.

Usage:
```
PY=/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
$PY -I -B tests/test_pinned_input_envelope_c2v003.py [--tool PATH] [--runs-root DIR]
$PY -I -B tests/mutation_check_c2v003.py [--runs-root DIR]
$PY -I -B tests/ast_delta_c2v003.py [--runs-root DIR]
```
