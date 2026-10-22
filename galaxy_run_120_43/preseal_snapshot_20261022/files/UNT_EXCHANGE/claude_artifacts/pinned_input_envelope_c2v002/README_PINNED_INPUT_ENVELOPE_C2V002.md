# pinned_input_envelope_c2v002: the root integrity envelope, with the A228 rulings

This is the successor of `pinned_input_envelope_c2v001` (`ecfce024`). A Claude2 root workflow built it for V006 A226 item 3, on the rulings D1 to D7 in V006 A228. Codex1 reviews it.

The tool is mechanical and read-only toward every pinned input. It uses no network, launches nothing, and creates every output exclusively. Nothing in the c2v001 folder was edited.

**Single read** (A226 item 1, E_A220_1) is unchanged. Each file is opened at most once per subcommand. The sha256, the byte count and, for documents that `collect` parses, the parsed object all come from the chunks of that one `os.read` pass. Metadata comes from fstat on the same descriptor. The new xattr names (D4) are read from that descriptor too, before the second fstat.

Two calls are new, and both are `os.stat` calls that open nothing:
- in `collect`, one per pin, to learn the pin's (dev, inode) for D1;
- in `snapshot`, one per excluded path.

| file | sha256 |
|---|---|
| `pinned_input_envelope_c2v002.py` | `0fac239ad7e5573084bfa494e55a344f40ab4deaa3469d5d54671ca5b457598c` |
| `tests/test_pinned_input_envelope_c2v002.py` | `d0494cafcf15698aec985e7d56bcedcd4dfbe279b37677a04b007851b1945dff` |
| `tests/mutation_check_c2v002.py` | `59e20a66b1b4c24595bb5ac82c29ab71856f34c49f413b08e929c9210ccdd6a2` |

`HASHES_PINNED_INPUT_ENVELOPE_C2V002.txt` lists these files, this README and every result record.

## What changed from c2v001 (A228 D1 to D7)

| ruling | what c2v002 does |
|---|---|
| **D1 / B1** V006 is an excluded growing file, however it is reached | `collect` reads `--v006` first. After that, any pin whose realpath is the V006 file goes to the pin set's `excluded` block, and so does any pin that is the same inode (a hard link). The block names the kind `v006_growing_file`, the rule, the reason and every source. This holds whether the pin came from a root document, a followed document, a pin list or V006's own pin lines. These pins are never in `pins` and never snapshotted. |
| **D2 / B2** the default depth is 0 | `--max-depth` defaults to 0: only the root documents are walked. A depth above 0 refuses unless `--depth-reason TEXT` is given. The depth and the reason are recorded in the pin set and in every manifest. |
| **D3 / N5** scope and exclusions | `--scope PATH POINTER` walks only the RFC 6901 subtree of the root document given as PATH (`--doc`, `--doc-pin` or `--walk-only`, spelled exactly as given). The pointers it records run from the document root.<br>`--exclude PATH --reason TEXT` can be repeated. Each `--reason` belongs to the `--exclude` just before it. A pin whose realpath or inode is PATH is listed under `excluded` with the reason and is never snapshotted. The list is in the pin set, both manifests and the compare report. |
| **D4 / N2** ctime | `snapshot` records each file's xattr names. In `compare`, a ctime-only change (bytes, size, mtime and inode all equal) is a **NOTE** (`CTIME_CHANGED_EXPLAINED`) when the xattr-name set changed. Otherwise it is **INVALIDATE** (`CTIME_CHANGED_UNEXPLAINED`). The c2v001 README line saying that ctime "cannot change bytes" was wrong (the verifier's case A4) and is withdrawn. |
| **D5 / N3** documents that do not parse | These refuse with exit 2 and write nothing:<br>- a root document that fails to parse: `ROOT_DOC_NOT_JSON`, `PIN_LIST_NOT_JSON`, `V006_NOT_UTF8`;<br>- a root document over `--max-follow-bytes`: `ROOT_DOC_TOO_LARGE`;<br>- a followed document that fails to parse: `FOLLOWED_DOC_NOT_JSON`. |
| **D6 / N4** compare | `--start-sha256` and `--end-sha256` are required, both by argparse and by the function (`MANIFEST_SHA256_REQUIRED`). |
| **D7 / N1** paths that do not encode | A pin path that does not encode as UTF-8 refuses with exit 2 (`PIN_PATH_NOT_ENCODABLE`), even with `--allow-unresolved`. Root, exclude, scope, output and input paths are checked the same way. |
| **N6** | Disclosed, not fixed. `O_NOFOLLOW` protects the last path component only. A parent folder swapped after `realpath` is a race that needs tampering at the same moment. |

Compare also refuses (`EXCLUDED_LISTS_DIFFER`) when the start and end manifests carry different excluded lists.

## Commands

```sh
PY=/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
T=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/pinned_input_envelope_c2v002/pinned_input_envelope_c2v002.py
V006="/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V006_ADDENDUM.md"
C1=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/c1_h1_c2/C1_H1_C2V001.json
C1_SHA=4015932226dcfbf9783b96de1daa512ef5c7a397ac4ca093d701ead362ed92c1
REG=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/registry_c2v001/REGISTRY_31pts_20261020T140004Z.json
REG_SHA=2dea408ff698e265a41bac1ef2562737ae98ffd4583477632e7a79507a15e319
C1_SCOPED="--doc-pin $C1_SHA $C1 --scope $C1 /tail_readiness"     # D3: C1 only through its binding block
E=<root's envelope directory for the phase>    # not inside a run tree; no 'ngc3198' in any name

# START: after the phase's configs, plans, admissions and registry entries are final; before the phase's first launch
$PY -I -B $T collect --phase <PHASE> --max-depth 0 <the phase's sources, below> --v006 "$V006" \
    --out $E/ENVELOPE_<PHASE>_PINSET.json                                         # prints file_sha256 (P); must exit 0
$PY -I -B $T snapshot --pins $E/ENVELOPE_<PHASE>_PINSET.json --pins-sha256 <P> --label start \
    --out $E/ENVELOPE_<PHASE>_START.json                                          # prints file_sha256 (S); must exit 0
# END: after the phase's last receipt (same pin set; never re-collect)
$PY -I -B $T snapshot --pins $E/ENVELOPE_<PHASE>_PINSET.json --pins-sha256 <P> --label end \
    --out $E/ENVELOPE_<PHASE>_END.json                                            # prints file_sha256 (N)
$PY -I -B $T compare --start $E/ENVELOPE_<PHASE>_START.json --start-sha256 <S> \
    --end $E/ENVELOPE_<PHASE>_END.json --end-sha256 <N> --out $E/ENVELOPE_<PHASE>_COMPARE.json   # 0 OK / 3 INVALIDATE
```

How to read each step:
- **collect exit 3:** a followed pinned document was missing or did not match its pin. This happens only at depth above 0.
- **collect exit 2:** refused input (a ruling D2, D3, D5 or D7 refusal, or a c2v001 refusal). Nothing is written.
- **START snapshot exit 3:** a pinned input already differs from its pin, so the phase does not launch on it.
- **compare exit 3:** INVALIDATE. A226 item 3 applies, as pre-registered: the phase's runs are kept, never read as evidence, and rerun under rule (c) with new attempts.
- **Root records** P, S, N, the compare verdict and the report's `excluded` list (with `n_excluded_pins_not_checked`) in V006.

## Per launch phase (depth 0 everywhere; no depth reason is written)

The sources are the phase's run configs, plans and admissions, as A228 D3 says. These carry C1's tail_readiness. C1 itself enters only as `$C1_SCOPED`, so its provenance pins outside the binding block are not in the envelope. Those are the two `/private/tmp` scratch drafts under `supersedes` and `sources_read_v002`.

Rules for supplying sources:
- Give each source by absolute path. Use `--doc-pin <sha> <path>` when root holds the sha, and `--doc` otherwise.
- `$C1_SCOPED` and `--doc-pin $REG_SHA $REG` go in every phase whose run config carries a `tail_readiness` block. The registry is the frozen CP-1 certificate registry (A207) that C1's tail_readiness pins. A226 item 3 names the registry's pins.
- A document that is appended to during the phase goes in as `--walk-only <path> --exclude <path> --reason "<why>"`. It is walked, not entered, and any pin to it elsewhere is listed rather than snapshotted.
- `--v006 "$V006"` is always given. V006 is then excluded wherever it is pinned (D1).

| phase | `--phase` | sources (besides `--v006 "$V006"`), all at `--max-depth 0` | START | END |
|---|---|---|---|---|
| S0 seed | `S0_SEED` | The S0 seed call's run config and spec (`--doc-pin`) and its admission record. The kit's gate file is `--doc-pin <5e688882…> /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s0_launch_kit_c2/GATE_DOCUMENT_PINS_V002.json`. Add `$C1_SCOPED --doc-pin $REG_SHA $REG` only if the seed config carries `tail_readiness`. The 15 V006 GATE_PINs come in through `--v006`. | before the kit's seed launch | after the seed's receipt |
| HEADLINE11 | `HEADLINE11` | Each HEADLINE11 run config, its plan and the admission records for its calls (`--doc-pin`); `$C1_SCOPED`; `--doc-pin $REG_SHA $REG`. | before the first HEADLINE11 launch | after the last HEADLINE11 receipt |
| W1 | `W1` | The W1 run config (the candidate written by apply_h3_fields c2v006, A227), the campaign plan and the admission and launch-registry entries (`--doc-pin`); `$C1_SCOPED`; `--doc-pin $REG_SHA $REG`. A launch registry that is appended during W1: `--walk-only` plus `--exclude ... --reason`. | before the first W1 launch | after the last W1 receipt |
| each wave | `W2`, `W3`, ... | That wave's run configs, plan and admission entries (`--doc-pin`); `$C1_SCOPED`; `--doc-pin $REG_SHA $REG`. Use one pin set per wave. | before the wave's first launch | after the wave's last receipt |
| Phase-1 NGC set | `PHASE1_NGC` | The P-112 config(s) and plan (`--doc-pin`). The NGC launch registry: `--walk-only <path> --exclude <path> --reason "appended during the phase"`. Add `$C1_SCOPED --doc-pin $REG_SHA $REG` if a P-112 config carries `tail_readiness`. NGC3198-named pinned files are hashed only. | before P-112's first launch | after the set's last receipt |
| S1 | `S1` | The S1 run configs, plan and admission entries (`--doc-pin`). Add `$C1_SCOPED --doc-pin $REG_SHA $REG` if an S1 config carries `tail_readiness`. | before S1's first launch | after S1's last receipt |
| Phase-1 freeze | `PHASE1_FREEZE` | The G26 freeze script's input documents and the freeze spec (`--doc-pin`). The script itself is covered once V006 carries its TOOL_PIN. | before the freeze script runs | after the freeze record is written |

Notes on the phases:
- **Depth.** Every command above is depth 0. Above depth 0, following reaches whatever the pins name, and B2 found that the history of pins includes old run outputs on External1. The S0 run folder `/Volumes/External1/NGC_S0_PHASE1_V001` does not contain "ngc3198". The content guard covers only NGC3198-named paths, V007_POSTSEAL_RECORDS, and `result.json`, `finish.json` and `progress.jsonl`. So never raise the depth for a phase whose roots pin run-tree files, and write the reason with `--depth-reason` when the depth is raised.
- **Phase-1 NGC.** An NGC3198-named pinned file is hashed (`hash_only`) and never parsed. Pins inside it are therefore not walked. If any of them must be covered, give them through `--pin-list`.
- **TOOL_PIN lines** in V006 are collected. A TOOL_PIN line for this tool would cover the envelope itself.
- **A path pinned at two shas** by two sources is two pins, and one of them must mismatch at START (exit 3). That is a real conflict between the phase's own documents. Resolve it in the documents, not with `--exclude`.
- **Do not open pinned inputs in GUI apps during a phase.** macOS can rewrite an xattr value under the same name (for example `com.apple.lastuseddate#PS`). That moves ctime without changing the name set, so it reads `CTIME_CHANGED_UNEXPLAINED` and INVALIDATEs (D4, as ruled).

## Real-input check: depth 0 collect only, no snapshot

`real_collect_check/` holds the pin set from this collect (phase token `REALCHECK_C1SCOPED_D0`, 2026-10-20 19:16Z), its `.sha256` sidecar, and the audit log written by `real_collect_audit.py`. That script runs the tool in-process under an audit hook. The hook refuses any open of an NGC3198-named path other than V006, `/Volumes`, `.codex` or V007_POSTSEAL_RECORDS, and any write outside the folder.

```
collect --doc-pin $C1_SHA $C1 --scope $C1 /tail_readiness --doc-pin $REG_SHA $REG --v006 "$V006"   (depth 0)
```

Results:
- **Exit 0**, pin set file sha `a847028b1d2befce9a5cf06758bfe5909562d0ad1cd6b07b3eb565313d769aca`. The audit denied nothing.
- **Opens:** C1, the registry and V006, once each, and nothing else outside the interpreter and this folder.
- **C1 scoped to `/tail_readiness`** gives 13 pins:

  | block | pins |
  |---|---|
  | `approved_certificate_producers` | 6 |
  | `row_policy_reviews` | 3 |
  | `custody_deriver` | 1 |
  | `certificate_policy_review` | 1 |
  | `state_enumerator` | 1 |
  | `certificate_registry` | 1 |

- **The registry** gives 126 pin occurrences, and V006 gives 15 GATE_PIN lines with 0 malformed. V006 was `52ede862…` at the time.
- **The pin set** has 125 distinct pins: 112 `depth_limited`, 11 `not_json_suffix` and 2 root documents.
- **Clean:** no `/private/tmp` pin, no `/Volumes` pin, and no path pinned at two shas.
- **V006 exclusion:** the entry is present with 0 pins. At depth 0 nothing in these sources pins V006. The B1 path was C1, then the CX3 policy review at depth 1.

The builder took no snapshot of real inputs. A snapshot hashes every pinned file, including gate files under `ngc_ntest_eval_cx/out`. Root's first START snapshot is the first real snapshot.

## Choices beyond the rulings' text (disclosed)

1. **Inode identity (D1, D3).** An excluded file is matched by realpath and also by (dev, inode).
   - At collect, `os.stat` of each pin path is used. A hard link to V006 is listed under `excluded` with `matched_by: inode`.
   - At snapshot, a pin that now resolves to an excluded realpath is not opened. A file whose fstat on the one descriptor shows an excluded inode is closed unread. Both are `excluded_not_read`, which is never a match, so the snapshot exits 3.
2. **`--depth-reason`** is required for any depth above 0, and it is recorded. This makes "0 unless a reason is written" mechanical.
3. **Scope.**
   - There is one scope per root document. It is keyed by the exact path string given, and a different spelling refuses `SCOPE_NOT_A_ROOT_DOCUMENT`.
   - A scope applies to `--doc`, `--doc-pin` and `--walk-only` only.
   - A `--doc` or `--doc-pin` that is scoped is still entered in the set at the sha of its bytes.
   - A pointer that does not resolve refuses, and so does one that resolves to a scalar. Pointer syntax is RFC 6901: it starts with `/`, uses `~0`/`~1` escapes, and array indices have no leading zeros.
4. **Exclusions.**
   - An exclusion names one file, not a folder.
   - An exclusion that matches nothing is still listed, with 0 pins.
   - These refuse: two exclusions with the same realpath (including one that duplicates V006), a `--doc` or `--doc-pin` that is excluded, and an exclusion or reason that is missing, blank or out of order.
5. **D4 is read literally.**
   - A chmod or an added hard link moves ctime without changing the xattr-name set. Each now INVALIDATEs. The mode or nlink change is still listed as a note, but it does not explain ctime.
   - The c2v001 rows C09 and C10 are carried with this expectation.
   - A ctime change that comes with a byte, size, mtime or inode change is a note beside that change's own INVALIDATE.
   - If the xattr names cannot be read, a ctime change cannot be explained, so it INVALIDATEs.
6. **D5 is extended to followed documents over the cap.** These also refuse (`FOLLOWED_DOC_TOO_LARGE`), where c2v001 skipped them silently. The ruling's text names only parse failure for followed documents. The c2v001 `warnings` field is gone, because nothing is now only a warning.
7. **xattr names on macOS** are read with flistxattr(2) through ctypes on the open descriptor, because `os.listxattr` is Linux-only in this Python. Only the names are read; no values.
8. **`snapshot --pins-sha256` stays optional.** D6 covers compare. The README commands always pass it.

The c2v001 choices still stand:
- ROOT_LISTED_ROW_GATE lines are collected.
- A malformed V006 pin line refuses.
- Upper-case hex is accepted, recorded in lower case.
- Relative pins are unresolved unless `--allow-unresolved` is given.
- Only `.json` and `.jsonl` pins are followed.
- A same-bytes rewrite (mtime or inode changed) invalidates.
- Symlinks are recorded, and a retargeted one invalidates.
- The content guard is broader than NGC3198 data.

## Verification (synthetic)

**Tests.** Each run has 82 MUST_PASS rows.
- All 52 c2v001 rows are carried under their c2v001 ids. Rows whose invocation changed:
  - those that need following now pass an explicit depth with a reason;
  - P05 is the explicit depth-8 run;
  - compare passes both shas;
  - C02's wrong-sha cases pass one wrong sha and one right one.
- Rows whose expectation changed are C09 and C10 only (D4, choice 5).
- There are 30 new rows:

  | group | rows | what they cover |
  |---|---|---|
  | X02 | 1 | CLI refusals for D2, D3, D6 and D7, including a non-UTF-8 argv path |
  | D1 | 7 | V006 excluded through a followed review at an old sha, its own pin line, a pin list, a symlink and a hard link; START 0, V006 appended, compare OK; a forged excluded list refused; the contrast without `--v006` exits 3; a symlink or hard link that becomes V006 after collect is excluded and not read; refusals |
  | D2 | 3 | default depth 0, the depth-reason refusals, the depth recorded |
  | D3 | 7 | the scope is exactly the tail pins; the contrast where unscoped START exits 3 on the scratch draft; escaped and array scopes; 11 scope refusals; exclusions by either spelling, listed in the pin set, manifests and report; an appended excluded file gives OK; 9 exclude refusals |
  | D4 | 6 | xattr names recorded; added or removed xattrs explain ctime; a value rewrite gives INVALIDATE; the verifier's A4 case gives INVALIDATE; an xattr change never masks a byte change |
  | D5 | 2 | 9 parse and cap refusals; at depth 0 a broken pinned document is not opened |
  | D6 | 2 | missing shas refuse; the verifier's A5 forged END is refused against the recorded END sha |
  | D7 | 2 | 11 paths that do not encode refuse with exit 2, not a crash; a re-signed pin set or an input path that does not encode refuses |

- The audit refused nothing in either run. The only subprocesses were the codex python, 13 per run.

| run | result | TEST_RESULTS.json sha256 |
|---|---|---|
| `test_runs/RUN_20261020T191701Z_53730` | 82/82 pass, audit 0 refused | `cfb915a2df0f70b3b7c1a2aa941cf7ce135253b6c65be714289de551e7539bfc` |
| `test_runs/RUN_20261020T191703Z_53758` | 82/82 pass, audit 0 refused | `a1eda8336d30c4eb84f0fb444844069e19f6599440c8cb80a5983de2598f77f2` |

**Mutation check** (`mutation_runs/RUN_20261020T191709Z_53815`): the baseline passed 82/82, and **45 of 45 mutants were killed**. MUTATION_RESULTS.json sha256 is `7e0d72be46c18ea520b6d8b853b3d4b44d82632c493d91dc27ea166ebad78f4f`.
- M01 to M20 carry the c2v001 mutants, with their anchors re-taken from the c2v002 source.
- M21 to M45 cover the rulings:
  - M21 to M30, D1 and D3 exclusion: V006 not registered; path-string-only match; no inode identity; excluded pins entered; snapshot reads an excluded realpath; snapshot ignores the inode; manifest without the excluded list; compare ignores the excluded lists; an excluded `--doc` accepted; duplicate exclusions accepted.
  - M31 to M32, D2: default depth 8; depth reason not required.
  - M33 to M35, D3: scope ignored; a scope that names no root accepted; reason not required.
  - M36 to M38, D4: an unexplained ctime change is only a note; mode or nlink explains ctime; xattr names not recorded.
  - M39 to M41, D5: no size cap; a parse failure is only a warning; an over-cap followed document skipped.
  - M42, D6: compare shas optional, in both layers.
  - M43 to M45, D7: encoding check removed; an unencodable path recorded as unresolved; root path encoding not checked.

**What the build read.** No NGC3198 data, run output, V007_POSTSEAL_RECORDS or `~/.codex` was opened. Outside this folder and the codex runtime, the build read:
- the c2v001 package (tool, tests, README, HASHES);
- the workflow journal holding the verifier's result;
- V006: entries A226 to A228, plus grep lines for the registry, `tail_readiness`, the pin lines and the phase documents;
- directory listings of `s0_launch_kit_c2/` and `c1_h1_c2/`;
- the bytes of C1, the registry and V006, through the tool's depth-0 collect above.

No existing file was edited.

Usage:
```
PY -I -B tests/test_pinned_input_envelope_c2v002.py [--tool PATH] [--runs-root DIR]
PY -I -B tests/mutation_check_c2v002.py
```
