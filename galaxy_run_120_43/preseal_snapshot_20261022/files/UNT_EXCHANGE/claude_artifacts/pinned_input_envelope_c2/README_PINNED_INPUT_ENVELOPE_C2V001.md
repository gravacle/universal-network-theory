# pinned_input_envelope_c2v001: the root integrity envelope (V006 A226 item 3)

This tool was built by a Claude2 root workflow for V006 A226 item 3. Codex1 reviews it. It is mechanical and read-only toward every pinned input: no network, no launches, and every output is created exclusively.

Single read (A226 item 1, E_A220_1): every file is opened at most once per subcommand. The sha256 recorded, the byte count recorded and, for the documents `collect` parses, the parsed object all come from the chunks that one `os.read` pass returned. Metadata comes from fstat on the same descriptor, taken before and after the read.

| file | sha256 |
|---|---|
| `pinned_input_envelope_c2v001.py` | `ecfce024bd7e26e5973765a7e8d027654b1f80e0bd82887da29de2de8b194ec1` |
| `tests/test_pinned_input_envelope_c2v001.py` | `f5d22952e3af613ce0f224a58f633d322920f7b1d4b1da4c94fb02a181c36cf5` |
| `tests/mutation_check_c2v001.py` | `60697e57ddfedc69e54d625acda548b5b548989831ac83ebf94643b17e76a420` |

HASHES_PINNED_INPUT_ENVELOPE_C2V001.txt lists these files, this README and the result records.

## What it does

- **collect** builds the phase's pin set. It reads the root-supplied documents and V006, walks every `{path, sha256}` pin, follows pinned JSON documents up to `--max-depth`, and writes the deduplicated pin set.
  - `--doc PATH` walks the document and also enters it in the set, at the sha of the bytes read now.
  - `--doc-pin SHA PATH` does the same, but the bytes must hash to SHA.
  - `--walk-only PATH` walks the document without entering it. Use this for anything that is still being appended to, such as a growing registry.
  - `--pin-list PATH` reads an explicit list of pins.
  - `--v006 PATH` reads V006's whole-line `GATE_PIN`, `HANDOFF_PIN`, `SPEC_PIN`, `WATCH_PIN`, `TOOL_PIN` and `ROOT_LISTED_ROW_GATE` lines, in the kit's PIN_RE form. V006 itself is never in the set, because it grows during every phase.
- **snapshot** reads every pinned file once, keyed by realpath. For each file it records the sha256 from the bytes, bytes_read, size, mtime_ns, ctime_ns, ino, dev, mode and nlink. For each pin it records match or mismatch, plus realpath, final_symlink and readlink. It writes the manifest with its own `body_sha256` and a `<out>.sha256` sidecar.
  - Exit 0: every pin matches.
  - Exit 3: some pin is missing, mismatched, not a regular file or changed during the read. The manifest is still written as evidence.
- **compare** checks a start manifest against an end manifest. The verdict is **INVALIDATE** (exit 3) if any of these is true:
  - a pin is not matched at start or at end;
  - a sha256 changed;
  - size, mtime_ns or ino changed (the file was rewritten or replaced, even with the same bytes now);
  - realpath, final_symlink or readlink changed (for example, a retargeted symlink);
  - the file set changed.
  
  Changes to mode, nlink, ctime_ns or dev are **notes** only. They cannot change bytes, and dev changes on a remount. Otherwise the verdict is **OK** (exit 0).
- **Exit 2** means refused input, and nothing is written. Any other code is a tool error.

**Content guard (hash_only).** No subcommand ever parses or follows a file in these cases:
- any component of the path or realpath contains `ngc3198`, in any case (the house rule, as in P-112 `path_rules`);
- any component contains `v007_postseal_records`;
- the basename is `result.json`, `finish.json` or `progress.jsonl`.

If such a file is pinned, `snapshot` hashes its bytes and records `hash_only: true`. `collect` never opens it. A guarded root document, pin set, manifest or output path is refused unopened.

The only exception is `--v006`. Its basename may contain NGC3198, as in P-112 `read_v006`, but its directories may not, and it must end in `.md`. Any path with a `.codex` component, as written or resolved, is never opened, not even to hash it. A pin into such a path refuses.

## Commands

```sh
PY=/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
T=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/pinned_input_envelope_c2/pinned_input_envelope_c2v001.py
V006="/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V006_ADDENDUM.md"
E=<root's envelope directory for the phase>    # not inside a run tree; no 'ngc3198' in any name

# START: after the phase's configs, plans, C1 and registry entries are final; before the phase's first launch
$PY -I -B $T collect --phase <PHASE> --doc <config> [--doc ...] [--doc-pin <sha> <C1>] [--walk-only <registry>] \
    [--pin-list <extra pins>] --v006 "$V006" --out $E/ENVELOPE_<PHASE>_PINSET.json        # prints file_sha256 (P)
$PY -I -B $T snapshot --pins $E/ENVELOPE_<PHASE>_PINSET.json --pins-sha256 <P> --label start \
    --out $E/ENVELOPE_<PHASE>_START.json                                                  # prints file_sha256 (S); must exit 0
# END: after the phase's last receipt
$PY -I -B $T snapshot --pins $E/ENVELOPE_<PHASE>_PINSET.json --pins-sha256 <P> --label end \
    --out $E/ENVELOPE_<PHASE>_END.json                                                    # prints file_sha256 (N)
$PY -I -B $T compare --start $E/ENVELOPE_<PHASE>_START.json --start-sha256 <S> \
    --end $E/ENVELOPE_<PHASE>_END.json --end-sha256 <N> --out $E/ENVELOPE_<PHASE>_COMPARE.json   # 0 OK / 3 INVALIDATE
```

Here is how to read each step:
- A **collect** exit of 3 means a followed pinned document was missing or did not match its pin. The pin set is written, and the start snapshot will show which pin.
- A **start snapshot** exit of 3 means a pinned input already differs from its pin, so the phase does not launch on it.
- A **compare** exit of 3 means INVALIDATE. A226 item 3 applies, as pre-registered: the phase's runs are kept, never read as evidence, and rerun under rule (c) with new attempts.
- Root records P, S, N and the compare verdict in V006.
- The end snapshot always uses the start's pin set. Never re-collect at the end.

## Per launch phase

The phase token is the `--phase` value. It may contain only letters, digits, `_`, `.` and `-`. The documents named below are the ones A226 item 3 names: the phase's configs, plans, C1 and registry, plus V006's pins. Supply each by its absolute path. The `--v006` flag is always given.

| phase | token | root documents to supply (besides `--v006`) | START | END |
|---|---|---|---|---|
| S0 seed | `S0_SEED` | The S0 seed call's run config and spec, the S0 kit's launch inputs, and the GATE_DOCUMENT_PINS file it requires (as `--doc-pin`). The 15 V006 GATE_PINs come in through `--v006`. | before the kit's seed launch | after the seed's receipt |
| HEADLINE11 | `HEADLINE11` | Each HEADLINE11 run config, its plan, the C1 policy (`--doc-pin`), and the admission and registry entries for its calls. | before the first HEADLINE11 launch | after the last HEADLINE11 receipt |
| W1 | `W1` | The W1 run config (the candidate built by apply_h3_fields c2v006), the campaign plan, C1 (`--doc-pin`), and the registry and launch-registry entries. | before the first W1 launch | after the last W1 receipt |
| each wave | `W2`, `W3`, ... | That wave's configs, plan, C1 (`--doc-pin`), and registry entries. Use one pin set per wave. | before the wave's first launch | after the wave's last receipt |
| Phase-1 NGC set | `PHASE1_NGC` | The P-112 config(s), the NGC launch registry entries (`--walk-only` if they are appended during the phase), and C1. | before P-112's first launch | after the set's last receipt |
| S1 | `S1` | The S1 configs, plan and registry entries. | before S1's first launch | after S1's last receipt |
| Phase-1 freeze | `PHASE1_FREEZE` | The G26 freeze script's input documents and the freeze spec. | before the freeze script runs | after the freeze record is written |

Notes on the phases:
- **Phase-1 NGC.** An NGC3198-named pinned file is hashed (`hash_only`) and never parsed. Pins inside it are therefore not walked. If any of them must be covered, give them through `--pin-list`.
- **V006 TOOL_PIN lines** are collected. Once V006 holds `TOOL_PIN P112_LAUNCHER_CX2V001 ...`, the launcher's bytes are in every later pin set. A TOOL_PIN line for this tool would cover the envelope itself in the same way.
- **Today's V006.** The real file parses with 15 pin lines (all GATE_PIN) and 0 malformed lines. All 15 paths end in `.json`, are unguarded, and sit under `UNT_EXCHANGE/claude_artifacts` (`ngc_ntest_eval_cx`, `ngc_point_producer_c4`, `ngc_route_tail_readiness_cx3`, `tail_scheme_impl_c2`). `collect` will follow them as gate documents. Use `--max-depth 0` to hash them without parsing them. This check read only V006's bytes and opened none of the 15.

## Choices made beyond the ruling's text (disclosed)

1. **ROOT_LISTED_ROW_GATE lines are collected too.** They are in the kit's PIN_RE, and they are V006 pins.
2. **A malformed V006 pin line refuses (exit 2).** The kit refuses the same file.
3. **Pin dicts follow the task's definition.** A pin is any dict with at least `path` (a string) and `sha256` (64 hex characters).
   - Upper-case hex is accepted, recorded in lower case, and kept as `sha256_as_written`.
   - A relative path is **unresolved** and refuses unless `--allow-unresolved` is given. With that flag it is recorded, never hashed, and counted in compare as `unresolved_pins_not_checked`.
   - A dict with both keys that fails the test is a near pin. It is reported and never hashed.
4. **Only `.json` and `.jsonl` pins are followed.** Every pin is in the set whether or not it was followed. The default depth is 8 and the default size cap is 64 MiB. Each (realpath, sha) is parsed at most once.
5. **A same-bytes rewrite invalidates.** If mtime_ns or ino changed, the file was written or replaced during the phase, and its bytes during the phase cannot be vouched for. Changes to mode, nlink, ctime_ns and dev are notes.
6. **Symlinks are recorded, not refused.** The realpath is read with O_NOFOLLOW, and a retargeted symlink INVALIDATEs.
7. **The content guard is broader than NGC3198 data.** It also covers `result.json`, `finish.json`, `progress.jsonl` and V007_POSTSEAL_RECORDS. It is the house rule: any component containing ngc3198 is guarded, so target-free NGC3198-named specs are hash_only as well.

## Verification (synthetic only)

**Tests.** Each run has 52 MUST_PASS rows:
- P: the pin walk, including nested pins, V006 lines and refusals;
- S: single read, using audit-hook open counts and read-changing `os.read` fixtures;
- C: compare;
- G: the content guard;
- L: symlinks, FIFOs, directories and dangling links;
- W: outputs;
- X: the CLI through the codex python;
- Z: the audit, which requires that nothing was refused and that the only subprocess is the codex python.

| run | result | TEST_RESULTS.json sha256 |
|---|---|---|
| `test_runs/RUN_20261020T183901Z_38551` | 52/52 pass, audit 0 refused | `bf5803411a87bd67d99771781a1b52edecf2eb47e35ee348ead88c7e370d849d` |
| `test_runs/RUN_20261020T183902Z_38650` | 52/52 pass, audit 0 refused | `21fd5629f4d2ed6a7134655136b4a6a91b280f43f5d87077cfa5d6f096cdc9e5` |

**Mutation check** (`mutation_runs/RUN_20261020T183906Z_38831`): the baseline passed 52/52, and **20 of 20 mutants were killed**. MUTATION_RESULTS.json sha256 is `720a6664159bc341da8bccd273d77074bdc905d0ed4e29284c14ccd42848bfa0`. The mutants:
- M01: the sha comes from a second read;
- M02: bytes_read comes from fstat;
- M03 and M04: a followed or root document is parsed from a second read;
- M05: the content guard is removed from following, in both layers;
- M06: TOOL_PIN is dropped;
- M07: compare ignores a sha change;
- M08: compare ignores unmatched pins;
- M09: pins are deduplicated on path only;
- M10: resolution is not compared;
- M11: the depth check is off by one;
- M12: there is no recursion;
- M13: the output is overwritten;
- M14: there is no body_sha256 check;
- M15: there is no changed-during-read check;
- M16: a rewrite does not invalidate;
- M17: V006 lines are stripped of leading whitespace;
- M18: a .codex pin is not refused at collect;
- M19: the one-read cache is removed;
- M20: unresolved pins are accepted silently.

During the build, no NGC3198 data, run output, V007_POSTSEAL_RECORDS or `~/.codex` path was opened. Files read outside this folder and the codex runtime:
- V006, for the A226 text and its pin-line syntax;
- the following, as source code only: the S0 kit's PIN_RE (`s0_prelaunch_record_c2v001.py` L43), the house single-read and test patterns (`apply_h3_fields_c2v006.py` and its tests), the P-112 path guard (`phase1_ngc_launch_cx2v001_draft005.py`), and a grep of `claude_artifacts` `*.py` sources for PIN_RE and guard patterns.

No existing file was edited.

Usage:
```
PY -I -B tests/test_pinned_input_envelope_c2v001.py [--tool PATH] [--runs-root DIR]
PY -I -B tests/mutation_check_c2v001.py
```
