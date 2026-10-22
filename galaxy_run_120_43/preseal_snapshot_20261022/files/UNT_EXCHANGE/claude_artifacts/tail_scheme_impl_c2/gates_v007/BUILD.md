# GATES_V007: identity comparator c2v007

Claude2 sub-agent, `tail_scheme_impl_c2/gates_v007/`, 2026-10-18 (about 16:20Z to 17:55Z).

**Rulings (binding).** V005 addendum A59, A67 N1, A68, A71, A73 (SF1, SF2, SF3, N3, N6), A74, plus A76 (c2v006's checker carried into c2v007) and A79.4 (NPZ logical-key alias; "also in scope: the identity comparator c2v007"). Addendum sha at last read: 4b937ec1 (A80 present; A80 does not touch c2v007).

**Inputs read.**
- Predecessor `gates_v006/`: BUILD.md fedbc615, comparator 097286d7, DIFF, selftest, tools, and its finished checker `check/CHECK.md` (CK002, 5296c5c0 per A76).
- Codex2 on c2v005: `review_comparator_c2v005_cx2/` (REVIEW 9317cd0d).
- Codex2 on c2v006: FROM_CODEX2 0444, 0445, 0446, 0447 (final, FAIL); `review_comparator_c2v006_cx2/` (REVIEW a11e0bb8; source_audit, ledger, a73, counterexamples, selftest_audit).
- The c2v005 check: `gates_v005/check/CHECK.md` (CK001).
- FROM_CODEX2 0448–0457 (compare r10 review; 0456/0457 carry the A79.4 rule to c2v007).

## Verdicts

| Item | Result |
|---|---|
| Comparator `run_identity_compare_c2v007.py` | **06ff52d6** (full sha below) |
| Selftest `selftest/out/SELFTEST_C2V007_V002/SELFTEST_C2V007.json` (ca057755) | **PASS**: 835/835 judged rows, 8/8 driver units, 0 breaches, every suite exit 0, under r4 and r5 (TESTED). V001 (59ad8ed5, 825/825) ran before the five canaries added from Codex2's c2v007 review preparation; it is superseded and kept |
| r4 Z2 vs DDO154_A2F10_ROUTE_A_PARALLEL_N8_C2V008_DECIDING_RUN_V001 | **PASS_BITWISE_EQUAL**, 31/31 checks (`out/IDENTITY_C2V007_R4_V001/Z2.json` 10a028c5) |
| r4 Z2_OFF_RO1 vs the same reference | **PASS_BITWISE_EQUAL**, 31/31 (Z2_OFF_RO1.json 9a3284b2) |
| r4 B0P_RERUN vs DDO154_ROUTE_B_C2V009_DECIDING_ADMIT_PREFIX_RUN_V001 | **PASS_BITWISE_EQUAL**, 26/26 (B0P_RERUN.json 117677de) |
| r5 comparisons (three) | **UNTESTED**: the r5 runs were still running. `R5_IDENTITY_COMPARE_COMMANDS_C2V007.sh` (92d28db5) is written and **not run** |
| r4 records (`records/R4_V001/`) | B1 and B1_OFF PASS_BITWISE_EQUAL_EXCEPT_DECLARED; B0prime_RERUN PASS_RESULT_EQUAL_EXCEPT_DECLARED. **Not seal records** (A67 N1: r4 driver sha) |
| A71 site inventory (`selftest/out/SELFTEST_C2V007_V002/A71_SITES_C2V007.json` e115dee3) | 446 sites: 232 fixed-key, 102 tagged with a guard, 43 justified, 63 set views, 6 copies, **0 untagged**, 0 duplicate constant keys (TESTED) |

## What c2v007 is

c2v007 is c2v006 with a new first layer and a smaller parse-and-normalize surface. Every c2v006 check keeps its meaning; nothing is relaxed. The full diff is `DIFF_c2v006_c2v007.diff` (3f19a27c). Main changes:

1. **Equal bytes first (A74), check BYTES_EQUAL.** (Logs: A74 says every file is compared by raw sha256, and A76 only limits where a log exclusion may apply. c2v007 therefore excludes no log. All 46 Z2 and 38 B0P stage logs are byte-equal on the r4 pairs, TESTED.)
   - Every file of both trees is hashed once (a stream, sha256 from bytes).
   - A both-side file whose sha differs FAILs, naming the file, unless its canonical path matches the CLOSED declared list `DECLARED_DIFFER` (a literal in the source, below). A declared file is then compared semantically, as in c2v006.
   - A file on one side only FAILs (BYTES_EQUAL and INVENTORY), unless it is a declared new-only file (the c2v006 H1 list, unchanged) or an attempt-ledger file paired by ATTEMPT_LEDGER.
   - **No file is skipped.** Stage logs are compared by bytes (A76: c2v006's by-name stdout/stderr skip is gone).
   - Undeclared files are never parsed. Only JSON/JSONL can be declared (asserted at import), so every .npy/.npz that both runs have is compared by raw bytes, container bytes included (A76 N5).
2. **Strict parse of declared files only (A74), checks STRICT_PARSE and PARSE_SURFACE.**
   - The store opens only regular files of the tree (lstat), and parses only declared files. Any other parse attempt FAILs PARSE_SURFACE.
   - JSON/JSONL keep object_pairs_hook (a duplicate FAILs even with equal values).
   - **NPY headers (0445 item 1):** `npy_header_dict` runs `ast.parse` on the header. A non-literal, a non-dict, a non-string key or a **duplicate key** FAILs before any value is evaluated. Values are evaluated one by one afterwards.
   - **NPZ (A79.4, 0456):** members are read by ZipInfo. A duplicate raw name, an extensionless member (refused outright), a duplicate logical key, data before the first member and an archive comment all FAIL.
   - A declared file is read a second time for parsing, and the sha of the parsed bytes must equal the first sha (TREE_STABLE). Every recorded file is re-hashed at the end.
3. **Tokens (A73 SF2, A74), check TOKENS_POLICY.**
   - The comparator derives the A59 triples itself (`derive_tokens`). The reference driver is the reference run's start.json driver, verified in REFERENCE_DRIVERS from bytes. The selected driver comes from its hashed bytes. Both are read as restricted AST; no code is executed.
   - Derivation: SCRIPTS (route_a excluded; for Z2 the 8 UVT kinds take SCRIPTS_UVT, A59 F1, and each successor must hash to its pin and name its base, L1193–1194), GALAXY_CONFIG_FILES, GC_SCHEMA and GC_SCHEMA_NAME, as path / sha / basename forms where they differ. For Z2 and Z2_OFF_RO1 the RO1 route-A binding and facade pins are added (reference sides = the c2v003 entries, verified from bytes).
   - Every derived pin is checked against bytes, except paths naming NGC3198, which are never opened.
   - **The supplied list must equal the derivation exactly.** A triple that is not derivable, a derived triple that is missing, a label outside `<[A-Z0-9_]+>`, a raw that is not a custody form (absolute code path, 64-hex sha, code basename, schema id; never a verdict word or a number), or **a repeated triple (RECORD_DEFECT, both indexes named; 0445 item 3)** refuses the comparison: TOKENS_POLICY and COMPARISON_REFUSED FAIL (and NO_LAST_WINS for a repeat), and nothing further is compared. Tokens-file metadata (`gate`, `driver`, `reference_driver`) must match the call.
   - Custody tokens (route-A worker, solver, driver) are verified per stage against the driver tables, as in c2v006. A pair already derived adds no custody token. Identical pairs of several stages are grouped under one label. Labels are **never joined** (0445 item 2).
   - Attempt-ledger tokens must have the checkpoint module's format `[0-9]{20}-[0-9]+-[0-9a-f]{8}` (c2v003 L478). A verdict word can therefore never be an attempt token.
4. **Injective normalization, check NORM_INJECTIVE.**
   - One left-to-right pass replaces the token raws, the run root, and 64-hex shas of this tree's files and checkpoint records.
     - The run root is replaced only at a path boundary on both sides.
     - A stage directory is replaced only when it is an actual stage directory of that tree with a unique name (SF-NN).
   - Every other `<` is escaped as `<~`.
   - Outputs are self-delimiting: `<RUN>`, `<STAGE:name>`, `<SHA:` plus length-prefixed sorted names plus `>`, or a grammar label. The map is therefore invertible.
   - **For every normalized string, decode(N(v)) == v is checked.** On the real runs that is 6.9 M strings per Z2 side and 92 k per B0P side, all decoded (TESTED). A 20 000-string fuzz over every output and marker form also decodes (E U04).
   - c2v006 policy is kept: raw text containing normalizer output FAILs, a sha token naming two distinct identity shas FAILs, and any non-bijective token relation FAILs.
5. **DECLARED_CLASSES** (own hardening).
   - Each declared entry lists the normalization classes allowed in its files. A class that fires in a file whose entry does not allow it FAILs.
   - Masked keys must sit at the same paths on both sides, except under a subtree an applied declared rule excused.
6. **IDENTITY body (A76 B-ID).**
   - RA_IDENTITY compares the whole checkpoint identity: caller decoded, code, controls, environment, fixed_source, format, inputs_sha256 and shapes.
   - A present identity_sha256 must be the checkpoint module's digest of the identity, and a present caller.sha256 the digest of the caller.
   - A malformed record FAILs RA_IDENTITY (no exception). IDENTITY.json counts in COVERAGE.
7. **SF1:** RO1 blocks must have exactly the registered key set {rule, armed, fired, events, worker_sha256, binding_sha256}, in RO1 and in the RESULT rule that excuses the block.
   **SF3:** a new-only static pin is admitted only when (path, sha) is an entry of the selected driver's tables and the bytes match.
8. **N3 containment** (`guarded_resolve`, also verbatim in the fill-tool successor `tools/fill_picard_member_c2v003.py`; E U06 checks the two are AST-identical).
   - Each component is tested before lookup by:
     - the marker in the NFC-casefolded name;
     - lexical NFC-casefold containment;
     - parent (st_dev, st_ino) plus folded name, which catches `/System/Volumes/Data` firmlinks and NFD and case aliases;
     - the registered (st_dev, st_ino) taken from the parent's listing, which catches `/.vol/<dev>/<ino>`.
   - Symlinks are followed component by component, so a link to any such spelling is caught. `..` is applied by the walk, never by `abspath`.
   - The `abspath` point closes the A79.5 "link then `/../`" class. That class also affected c2v002.
   - An unavailable registered identity refuses (A79.3).
   - The comparator applies the guard to `--reference` and `--new` before reading anything.
9. **Strict CLI (A76 SF-ARGV):** each flag exactly once and spelled exactly; no abbreviation, `--flag=value` or positional argument. Also refused: a run as its own reference, nested runs, and `--out` inside a run.
10. **Inventory (A76 N1, N3, N4):**
    - stage digits are ASCII `[0-9]`;
    - FIFOs, sockets and devices FAIL INVENTORY without being opened;
    - directories are inventoried, so an empty extra directory FAILs;
    - the attempt ledger uses fullmatch with a grouped-key guard before any inventory entry is removed (0446).
11. **CROSS_RUN_REFERENCE** (own hardening): a byte scan during hashing. A NEW file that names the reference run root FAILs, even when it is byte-equal to the reference file (a copied record).
12. **A71 everywhere:** see the site table. Also new: `put()` refuses a check reported twice, and the report merge must be disjoint.

## The closed declared list (A74; literal `DECLARED_DIFFER` in the source)

**How it was derived.** A raw sha256 diff of the three r4 pairs (scratch `bytediff.py`) was taken first. B0P: 1245 both-side files, 806 equal, 439 differ. Z2 and Z2_OFF_RO1: 4347 both-side files, 852 equal, 3495 differ. Every NPY/NPZ, every checkpoint blob and every stage log is byte-equal.

The differing files are JSON/JSONL records carrying the c2v006 declared-difference classes: run paths, stage numbers, shas of differing files, the driver path and sha, script custody, timestamps and pids, and RA digests.

The class sets are the unions observed on the three pairs, both sides (dev runs dev1/dev2). r5 runs with the same specs are expected to fire the same classes. A new class fails closed (DECLARED_CLASSES).

| Id | Gates | Canonical path (fullmatch) | Allowed classes | Files differing Z2 / OFF / B0P |
|---|---|---|---|---|
| D01 | all | `start.json` | CUSTODY_TOKEN, DECLARED_RULE, DRIVER_TOKEN, FILE_SHA, MASKED_KEY, TAIL_KEY | 1/1/1 |
| D02 | all | `result.json` | CUSTODY_TOKEN, DECLARED_RULE, DRIVER_TOKEN, FILE_SHA, LEDGER_TOKEN, MASKED_KEY, RA_SHA, RUN_PATH, STAGE_DIR, TAIL_KEY | 1/1/1 |
| D03 | all | `finish.json` | FILE_SHA, MASKED_KEY, RUN_PATH | 1/1/1 |
| D04 | all | `progress.jsonl` | FILE_SHA, MASKED_KEY | 1/1/1 |
| D05 | all | `inputs/(fs\|le[0-9])_manifest.json` | FILE_SHA, RUN_PATH, STAGE_DIR | 4/4/4 |
| D06 | all | `inputs/galaxy_config_((columns\|feedback\|rotation)_vNNN\|column_mean_vNNN_leN).json` | DRIVER_TOKEN, FILE_SHA, RA_SHA, RUN_PATH, STAGE_DIR | 10/10/10 |
| D07 | all | `stages/<name>/request.json` | CUSTODY_TOKEN, DRIVER_TOKEN, FILE_SHA, RA_SHA, RUN_PATH, STAGE_DIR | 23/23/19 |
| D08 | all | `stages/(fs\|rfs\|leN)_columns_NN/columns/(column_NNNN\|start\|finish).json` | DRIVER_TOKEN, FILE_SHA, MASKED_KEY, RA_SHA, RUN_PATH, STAGE_DIR, TAIL_KEY | 378/378/376 |
| D09 | all | `stages/(fs\|leN)_feedback/feedback/(start\|finish).json, progress.jsonl` | DRIVER_TOKEN, FILE_SHA, MASKED_KEY, RA_SHA, RUN_PATH, STAGE_DIR | 9/9/9 |
| D10 | all | `stages/(fs\|leN)_rotation/rotation/(start\|finish).json, progress.jsonl` | D09 + TAIL_KEY | 12/12/12 |
| D11 | all | `stages/leN_column_mean/observation/result.json` | DRIVER_TOKEN, FILE_SHA, RUN_PATH, STAGE_DIR | 3/3/3 |
| D12 | all | `stages/offset/offset/(start\|finish).json, progress.jsonl` | DRIVER_TOKEN, FILE_SHA, MASKED_KEY, RUN_PATH, STAGE_DIR, TAIL_KEY | 3/3/2 |
| D13 | A2F10 | `inputs/call_spec.json` | DECLARED_RULE, TAIL_KEY | 1/1/– |
| D14 | A2F10 | `inputs/galaxy_config_(body\|offset\|reference).json` | DRIVER_TOKEN, FILE_SHA, RA_SHA, RUN_PATH, STAGE_DIR | 3/3/– |
| D15 | A2F10 | `stages/(body/body\|reference/reference)/(radius_NNNN\|start\|finish).json, progress.jsonl` | DRIVER_TOKEN, FILE_SHA, MASKED_KEY, RA_SHA, RUN_PATH, STAGE_DIR, TAIL_KEY | 150/150/– |
| D16 | A2F10 | `stages/route_a/attempt_NNN/(start\|finish\|result).json, progress.jsonl` | CUSTODY_TOKEN, DECLARED_RULE, DRIVER_TOKEN, FILE_SHA, LEDGER_TOKEN, MASKED_KEY, RA_SHA, RUN_PATH, STAGE_DIR, TAIL_KEY | 4/4/– |
| D17 | A2F10 | `stages/route_a/checkpoint/IDENTITY.json` | CUSTODY_TOKEN, DRIVER_TOKEN, FILE_SHA, RUN_PATH | 1/1/– |
| D18 | A2F10 | `stages/route_a/checkpoint/iteration_NNNN/(COMPLETED\|START\|column_NNNNN).json` | FILE_SHA, RECORD_DROP | 2890/2890/– |
| LEDGER | A2F10 | `stages/<name>/checkpoint/attempts/<token>.(start\|end).json` (paired by order) | MASKED_KEY, RECORD_DROP | 4 files (one token each side) |

Notes:
- "A2F10" means Z2, Z2_OFF_RO1 and Z2_OFF.
- `N` stands for an ASCII digit, and the source has the exact regexes.
- Declared new-only files are unchanged from c2v006 (H1). Their directories are declared for Z2 only.
- **Z2_OFF** has no real pair; it uses the A2F10 entries (UNTESTED on real data).

## Tokens

`tools/make_tokens_c2v007.py` (cda66514) executes the comparator's own `derive_tokens` from the comparator's hashed bytes, so the tool and the comparator cannot disagree. Results:

| Driver | Z2 | Z2_OFF_RO1 | B0P_RERUN | Derive record |
|---|---|---|---|---|
| r4 | 1fe10ef7 (50) | 1a6f6fa8 (50) | 86f9161b (0) | a7c299ce |
| r5 | 0773782b (50) | 29eab731 (50) | bbe2eb49 (0) | 8ef5d2bf |

**Checks:**
- The pair set of every file equals the c2v006 file of the same gate and driver (TESTED). Labels differ by design: c2v006 used the c2v003 GEO_PIN_nn numbering.
- The final comparator's derivation equals every shipped file (TESTED, E U12, both drivers).
- The derive records name the comparator bytes current at derivation time (35c8f274, a development build with the same `derive_tokens`). The comparator re-derives the list at every run.

## A71 site table (every list-to-mapping / dict-from-pairs site)

`tools/a71_inventory_c2v007.py` (b8bda286) enumerates every dict display, dict/set comprehension, `dict()`/`set()` call, setdefault/update and subscript store from the full AST. Full list: `A71_SITES_C2V007.json` (e115dee3); summary: 446 sites, 0 untagged (selftest unit S_a71, TESTED). Data-dependent sites by guard:

| Guard tag | Sites (scope) | Guard | Test |
|---|---|---|---|
| A71[JSON] | `_pairs` | object_pairs_hook refuses a duplicate member, equal values too | CD D_O06/O07/O08/O26, K N07/D01/D02/D04, X whole-gate duplicate_json_key |
| A71[NPY_HEADER] | `npy_header_dict` | AST key check before any value is evaluated | E10–E13b, U01, X a71 units |
| A71[NPZ] | `npz_identity_bytes` | raw name, extensionless member, logical key, prepended data, comment | E14, E15, E15c, D_O10/O27 (bytes) |
| A71[CLI] | `parse_cli` | each flag once, exact spelling | E37–E40, K A04–A06 |
| A71[TOKEN_TRIPLES] | `token_file_defects` | repeated supplied triple = RECORD_DEFECT naming both indexes | E20, U03, X a71 F05 |
| A71[TOKEN_RELATION] | `build_tokens` | multimaps; two labels per pair, two pairs per label, fan-out all FAIL; never joined | E21, E22, U02, D_O20/O21 |
| A71[SIDE_TOKENS], A71[TOKEN_CLASS] | `Side.__init__`, `_compare` | bijection asserted (TOKEN_MAP_NOT_BIJECTIVE) after build_tokens | E21/E22 (upstream refusal) |
| A71[HEXMAP], A71[HEXINV] | `Side.__init__`, `_compare` | sha → set of all names; many-to-one FAILs | D_O23, E61 |
| A71[NORM_KEYS] | `Side.norm` | two raw keys to one key FAIL naming both (unreachable: the map is injective) | E59 (no KEY_COLLISION, raw-text FAIL) |
| A71[STAGE_DIRS] | `Tree.__init__` | duplicate stage names / numbers excluded and FAIL | CD C_F04/F05, B/X structural F01–F04 |
| A71[INVENTORY], A71[DIR_INVENTORY] | `Tree.__init__`, `Store.__init__` | canonical collisions keep neither and FAIL | structural F03, E42 |
| A71[LEDGER] | `_compare` | fullmatch, token format, grouped-key collision before any removal | E49–E54, X ledger F02/F03, K D02 |
| A71[ARGV] | `StrictArgv` | repeated stage flag reads as DUPLICATE | D_O17 |
| A71[STAGE_RECORDS] | `_compare` | duplicate stage record name | D_O18 |
| A71[STATIC_PINS], A71[RA_PINS] | `_compare`, `ra_new_pins` | normalized pin-key collision becomes COLLIDED | E34–E36, U07 |
| A71[DRIVER_AST], A71[DRIVER_ENV] | `_ev`, `driver_env`, `driver_tables` | duplicate dict-literal key in a driver refuses | source; U12 (real drivers parse) |
| A71[CUSTODY_GROUP] | `auto_custody` | identical pairs grouped with every stage label kept | real Z2 (6 custody tokens), C_F25/F27/F30 |
| A71[DECLARED_LIST] | `declared_entry`, `_compare` | a path matched by two entries is AMBIGUOUS (never first-wins) | source (no overlap in the literal list) |
| A71[NEW_ONLY_GROUP], A71[STAGE_KEYED], A71[ACCUMULATOR], A71[FIXED_KEYS], A71[IDENTITY_CALLER] | various | keys unique by construction (stage names, constant tuples), accumulators that keep every member, or one intended replacement | inventory review |
| A71[CHECKS], A71[REPORT_MERGE] | `put`, `main` | a check reported twice keeps both and FAILs; report sections never overwrite | source |

The 43 JUSTIFIED sites are caches keyed by absolute path, counters, and projections of an existing mapping's own keys. Each has a written reason in the tool (`JUSTIFIED`). The 63 SET_VIEW sites are set algebra on existing key sets, for comparison only.

## Selftest

`selftest/selftest_c2v007.py` (4d8a5038) with `selftest/canaries_c2v007.py` (ff853f81). It runs every suite as its own process under r4 and r5, and judges every row against `selftest/expect_c2v007.json` (5f611606, built by `make_expect_c2v007.py` 1c917096; 354 cases).

**Judging rule:**
- **A MUST_FAIL passes only if every owner check fails.** An unrelated failure does not count, and COMPARATOR_EXCEPTION never stands in for an owner.
- The 72 weak Codex2 wrapper expectations (Codex2 0447 S2) therefore carry explicit owners. The c2v005-review structural and invocation suites use Codex2's own cx2v003/cx2v004 owner maps.

**Ports.** `selftest/port_c2v007.py` (3f826903) writes 16 ports plus diffs into `selftest/ported/` (record 253c1d60). Each substitution is asserted to apply exactly once. The substitution classes are:
- SHIM: deterministic ZIP member timestamps, so equal synthetic NPZ bytes are equal;
- PATHS;
- TOKENS: the fixture's hand-written labels are replaced by the derivation;
- DIGEST: the fixture's `'9'*64` identity_sha256 becomes the real digest;
- A73: c2v007 artefacts, plus one c2v006-era predicate restated at the token gate.

| Suite | Source | Rows (r4+r5) | Result |
|---|---|---|---|
| A | Codex2 c2v005 review: source-audit whole gate 9 + duplicate NPZ 2 (the c2v006 group A) | 22 | 22/22 |
| B | Codex2 c2v005 review: structural 23, invocation 24 (the c2v006 group B) | 94 | 94/94 |
| CD | the c2v006 own canaries (c2v004-CHECK ports C, own D O01–O30) | 150 | 150/150 |
| X | Codex2 c2v006 review: counterexamples whole gate 20, structural 25, invocation 24; source-audit probes 9 + 18 units; ledger 4; A73 predicates 47 | 247 | 247/247 |
| K | the c2v006 workflow's checker CK002: 69 canaries + 5 CK001 SF regressions | 148 | 148/148 |
| E | own c2v007 canaries (76 whole-gate cases: 10 MUST_PASS, 57 MUST_FAIL, 9 MUST_REFUSE; plus 11 units; per driver) | 174 | 174/174 |
| S | driver units: A71 inventory; hashed-bytes exec; no argparse; no `$` anchor; no `\d`; no log skip; N6 checker on 17 synthetic cases (11 receipts, 6 reports); R5 script order and pin | 8 | 8/8 |

**Expectation changes from c2v006 / Codex2 / CK002.** Every change is listed per row in `expect_c2v007.json` with its reason code. Counts by code:
- KEPT 220;
- R_BYTES 56;
- R_PARSE_SURFACE 15;
- R_TOKENS 10;
- R_INJECTIVE 8;
- R_A76 6;
- R_ARGV 3;
- R_LEDGER 2;
- R_DIGEST 1;
- R_CLOSED 33.

The codes mean:
- **R_BYTES / R_PARSE_SURFACE (A74):** an undeclared file is bytes, never parsed. BYTES_EQUAL owns its difference, and the group check fails with it.
- **R_TOKENS:** a non-derivable token refuses before AUTO_CUSTODY or NORM_INJECTIVE are reached.
- **R_INJECTIVE:** the c2v006 KEY_COLLISION constructions leave two distinct keys and FAIL on the file's own check.
- **R_LEDGER:** a synthetic attempt name outside the checkpoint token format.
- **R_DIGEST:** CK002's reseal does not recompute identity_sha256.
- **R_A76:** a FIFO, an empty directory, or NPZ container bytes.
- **R_ARGV:** a repeated or abbreviated comparator flag.
- **R_CLOSED:** a finding predicate that c2v006 reproduced now reads closed. All 47 Codex2 A73 requirement predicates hold (c2v006: 20/47).

**Flipped polarity (all declared):**
- MUST_PASS → MUST_FAIL: C_P01, C_P02, C_P04 (R_BYTES); CK2 D02c (R_LEDGER), D07 (R_A76), T06 (R_BYTES), I00 (R_DIGEST); X a71 P08 and ledger P00 (R_TOKENS / R_LEDGER).
- MUST_FAIL → MUST_PASS: D_O03, D_O05, D_O11, because the same bytes are on both sides and an undeclared file is never parsed (R_PARSE_SURFACE). Their declared-file forms are own canaries E57–E61 (FAIL NORM_INJECTIVE).

**0445 / 0446 constructions on their owning checks (MUST_FAIL, TESTED):**
- duplicate NPY descr, duplicate NPZ shape, equal duplicate fortran_order, non-dict and non-literal headers: STRICT_PARSE when the file is declared (E10–E13b; real Z2 parses its 7 sidecar/manifest NPZ under this rule). On an undeclared file, Codex2's exact bytes FAIL BYTES_EQUAL + STAGES (E16–E18, X a71 F01–F03).
- the joined-label pair: TOKENS_POLICY + COMPARISON_REFUSED (E21, X a71 F06; build_tokens never joins, U02).
- repeated triples: TOKENS_POLICY + NO_LAST_WINS (E20, X a71 F05, U03).
- the ledger newline alias: ATTEMPT_LEDGER + INVENTORY + BYTES_EQUAL (E51/E52, X ledger F02/F03).

**Added from Codex2's c2v007 review preparation** (`review_comparator_c2v007_cx2/prep/`, UNTESTED crosswalks read before closing), all MUST_FAIL on their owners:
- E15d: an NPY duplicate key spelled with adjacent string literals (STRICT_PARSE);
- E15e: an equal duplicate in a v2.0 header (STRICT_PARSE);
- E15f: a byte-identical duplicate key in a declared record on both sides, where equal bytes never skip the declared strict parse (STRICT_PARSE);
- E48b: an unknown outer IDENTITY.json field (RA_IDENTITY);
- E48c: a correctly re-digested unknown nested identity field (RA_IDENTITY).

**Own canaries for SF1, SF2, SF3, N3, N6:**
- SF1: E31–E33;
- SF2: E20–E30, U12;
- SF3: E34–E36, U07;
- N3: E62, E64, E65, U05, U06. U05 covers child, firmlink, NFD, case, symlink, `/.vol` inode, a symlink to the firmlink spelling, a symlink to the NFD spelling, link-then-`..`, unavailable identity and sibling negatives;
- N6: U10, U11, S_n6 (receipts FINISHED / FAILED / RUNNING / exit 1 / exit True / stopped / retried / wrong driver / duplicate key / symlink / missing; verdicts PASS / FAIL / exit 1 / other comparator / wrong gate / missing).

**Discrimination.** Every Codex2 0447 blocker (B1–B3, S1) and every CK002 breach (N05, N10, K03, I01–I04, A04–A06, R01–R04) read PASS on c2v006 in its reviewers' own published results. The same constructions FAIL their owners on c2v007 here. No separate c2v006 run of the E harness was made: it calls c2v007-only functions.

## Real r4 pairs (`out/IDENTITY_C2V007_R4_V001/`; command lines in `run_env.txt` 8d808a09)

Python: `-I -B`, single-thread BLAS (OMP/OPENBLAS/MKL/NUMEXPR/VECLIB/BLIS = 1), no nice. Three pairs run in parallel, 17:39:14Z–17:40:57Z, exit codes 0/0/0.

| Gate | Report | Checks | Wall | Peak RSS | Both-side files: equal bytes / declared differing / undeclared | New-only declared | Parsed (ref, new) | Strings round-tripped (ref, new) |
|---|---|---|---|---|---|---|---|---|
| Z2 | 10a028c5 | 31/31 | 100 s | 2.8 GB | 4347: 852 / 3495 / **0** | 21 | 3485, 3504 | 6 904 055, 6 904 681 |
| Z2_OFF_RO1 | 9a3284b2 | 31/31 | 103 s | 2.8 GB | 4347: 852 / 3495 / **0** | 1 | 3485, 3486 | 6 904 055, 6 904 250 |
| B0P_RERUN | 117677de | 26/26 | 11 s | 0.2 GB | 1245: 806 / 439 / **0** | 0 | 431, 431 | 92 334, 92 396 |

All three pairs, every check:
- STRICT_PARSE 0 problems; PARSE_SURFACE 0; NORM_INJECTIVE 0 collisions and every string decoded; NO_LAST_WINS 0; TREE_STABLE 0 changes; DECLARED_CLASSES 0; CROSS_RUN_REFERENCE 0;
- RO1 key sets exact;
- RA_IDENTITY digests verified on both sides;
- tokens: 50 supplied = 50 derived for Z2 and OFF, 0 = 0 for B0P.

c2v006 needed 600 s and 6.2 GB for Z2. The c2v006 PASS verdicts on these pairs are confirmed under the stricter c2v007 rules (TESTED).

## Records and the r5 script

- `tools/write_identity_records_c2v007.py` (f3ae76b0) is the c2v006 writer plus four things:
  - the c2v007 comparator;
  - a strict report check (schema, failing == []);
  - N6 receipt predicates: status FINISHED, driver_status COMPLETED, exit_code int 0, stop_reason null, retries 0;
  - `allow_abbrev=False`.

  r4 records: B1 fd31d7d0, B1_OFF b7ec9322, B0prime_RERUN 8242f09b, WRITE_RECORDS 5787de3c, log 7c35b6df. All carry `a67_n1.is_v010_r5 = false`, so they are not seal records.
- `R5_IDENTITY_COMPARE_COMMANDS_C2V007.sh` (92d28db5), written by `tools/write_r5_script_c2v007.py` (90d9532c). **It was not run.** In order, it:
  1. pins the comparator (06ff52d6), the three r5 token files, the checker and the writer;
  2. checks every receipt strictly with `tools/r5_gate_check_c2v007.py receipts` (5dcd5142) before any comparison;
  3. runs the three comparisons and collects each exit code from its own PID;
  4. reads every verdict with `r5_gate_check_c2v007.py verdicts` (schema, gate, driver, PASS_BITWISE_EQUAL, failing == [], comparator sha, exit code 0);
  5. writes `records/R5_V001` only after all three pass. Any failure exits 1 naming the item.

## Closure list

| Item | Status | Evidence |
|---|---|---|
| 0445.1 NPY header duplicates (last-wins literal_eval) | **CLOSED, TESTED** | AST key check before evaluation; E10–E13b STRICT_PARSE; U01; X a71 units now False |
| 0445.2 joined token labels | **CLOSED, TESTED** | labels never joined; grammar `<[A-Z0-9_]+>`; supplied list = derivation; E21, E22, U02; injectivity round-trip on all real strings |
| 0445.3 repeated identical triples | **CLOSED, TESTED** | RECORD_DEFECT naming both indexes → TOKENS_POLICY + NO_LAST_WINS; E20, U03, X a71 F05 |
| 0446 attempt-ledger newline alias | **CLOSED, TESTED** | fullmatch, `[A-Za-z0-9_-]` tokens, checkpoint token format, grouped-key guard; E51–E54, X ledger F02/F03 |
| 0447 S2 weak selftest assertions | **CLOSED, TESTED** | every MUST_FAIL has owners; COMPARATOR_EXCEPTION never substitutes |
| A73 SF1 RO1 full key set | **CLOSED, TESTED** | E31–E33, K R01, A73 predicates |
| A73 SF2 tokens bound to the A59 derivation | **CLOSED, TESTED** | in-comparator derivation; equality required; custody raw forms; E20–E30, K R02, U12 |
| A73 SF3 selected-driver static pins | **CLOSED, TESTED** | E34–E36, U07, K R03 |
| A73 N3 firmlink / NFD containment | **CLOSED, TESTED** | `guarded_resolve` in comparator + fill tool c2v003; U05, U06, E62 |
| A73 N6 receipt status, each verdict | **CLOSED for the script and writer (TESTED by unit); the r5 run itself UNTESTED** | S_n6, U10, U11; script not run |
| A74 equal bytes first / closed list / parse surface | **CLOSED, TESTED** | BYTES_EQUAL, PARSE_SURFACE, DECLARED_CLASSES; real pairs 0 undeclared |
| A76 B-ID whole IDENTITY body | **CLOSED, TESTED** | E46–E48, K I01–I04, real digests verified |
| A76 SF-ARGV | **CLOSED, TESTED** | E37–E40, K A04–A06 |
| A76 SF-NN | **CLOSED, TESTED** | E45, K N05 |
| A76 N1 / N3 / N4 / N5 / log scope | **CLOSED, TESTED** | E44 + K N10; E41 + K E06 (a FAIL report, no hang); E42, E43, K E01/E02; E14/E15, K D07/D08/T04; E03/E04, K R04 |
| A79.3 unavailable registered identity refuses | **CLOSED, TESTED** | U05 `unavailable_registered_identity_refuses` |
| A79.4 NPZ extensionless member / logical-key alias | **CLOSED, TESTED** | E15c; NPZ_MEMBER_NOT_NPY + logical-key guard |
| A79.5 symlink-to-alias and link-then-`..` (class applied to the containment layer) | **CLOSED, TESTED** | U05 (the `abspath` bypass was found by this build's own canary and fixed) |
| A71 site table with guards and tests | **CLOSED, TESTED** | table above; S_a71 0 untagged |

## OPEN and UNTESTED (each with its deciding test)

| Item | Deciding test |
|---|---|
| The three r5 comparisons and their seal records | When each `UVT_*_R5_RUN_V001.receipt.json` exists and reads FINISHED, run `R5_IDENTITY_COMPARE_COMMANDS_C2V007.sh`. It exits 0 only if all three read PASS_BITWISE_EQUAL and the records are written |
| Whether r5 differs only in the declared files and classes | The same run: any undeclared byte difference or new class FAILs naming the file, and must then be reviewed, never tuned |
| Independent cross-lineage check of c2v007 (A70 practice) | Codex2 0448 queued a c2v007 review to start when this BUILD.md exists. A Claude-lineage check lens is also expected by A74 (wf_17f396c8) |
| Z2_OFF gate on real data | No Z2_OFF pair exists; synthetic only (structural suites) |
| CK001 N2 hardening: masked uv_tail records in Z2 cross-checked against the inputs files | NOTE carried from CK001, not required by A73–A79. Masking is limited to TAIL_KEY-declared files (DECLARED_CLASSES). Deciding test: a canary that alters a masked stage uv_tail record (FAILs only if implemented) |
| A file changed and restored between its hash and the end re-hash | Not detectable by re-hashing, as in c2v006. Every verdict uses bytes whose sha is recorded |
| NGC3198 GALAXY_CONFIG pins in the derivation | By design not opened (no NGC3198 file is read). These pairs rest on the driver tables only |

## Hygiene and disclosures

- **Runs read:**
  - the finished r4 identity runs `runs_ext/UVT_Z2_A2F10_RUN_V001`, `UVT_Z2_OFF_RO1_A2F10_RUN_V001` and `UVT_B0P_RERUN_ADMIT_PREFIX_RUN_V001`;
  - their receipts (writer);
  - the references `CLAUDE2/runs/DDO154_A2F10_ROUTE_A_PARALLEL_N8_C2V008_DECIDING_RUN_V001` and `DDO154_ROUTE_B_C2V009_DECIDING_ADMIT_PREFIX_RUN_V001`;
  - the precondition-L result `DDO154_ROUTE_B_C2V008_DECIDING_ADMIT_PREFIX_RUN_V001/result.json` (writer).
- **Not read:** any `*_R5_RUN_V001` file, any C5H file, and any NGC3198 target.
- **Disclosure, listings.**
  - One `ls` of `runs_ext` printed its entry names, including the r5 and C5H names; C5H was filtered from the display only.
  - The containment guard lists `runs_ext` (names and DirEntry inodes) at each call, to identify the C5H directory's inode without stat-ing or opening it.
  - E62 passes the C5H path as a string; it is refused from the marker before any lookup.
- **Nothing was launched. No existing artefact was edited or deleted.**
  - During the build I edited my own new gates_v007 files in place: the comparator, tools, the fill-tool copy, and the R5 script, which the generator rewrote with the final pin.
  - Every final output was created exclusively after the last edit. The final selftest and the real runs use the final comparator bytes, and both reports record 06ff52d6 at start and end.
  - The only `rm` commands ran on scratchpad paths before those paths existed.
  - I stopped my own stale observe run (`pkill`) after editing the comparator under it.
- **Writes outside gates_v007:** development outputs went to this session's scratchpad (`.../scratchpad/c2v007_dev/`):
  - byte diffs of the r4 pairs;
  - dev comparator copies and dev runs (dev1, dev2) on the real r4 pairs;
  - observe-mode selftests and dev ports.

  They are not evidence, and none is cited as a result except the derivation of the declared list, which is reproduced by the final runs.
- **FIFO warning:** E41 and CK002 E06 leave named pipes under `selftest/out/SELFTEST_C2V007_V00{1,2}/`. HASHES.txt lists them by name without reading them.
- Python: the codex runtime, `-I -B`. Hashes are sha256 from bytes. Full list: HASHES.txt.

## Key files (sha256 from bytes)

- `run_identity_compare_c2v007.py` 06ff52d636c640ebe9a92a4b2cf54620a01514992019e2b2f2dca1529f7dc188
- `DIFF_c2v006_c2v007.diff` 3f19a27cf180e7254a1f9e785261a62f776fa8f34e254c1cbde0d694a2e53501
- `R5_IDENTITY_COMPARE_COMMANDS_C2V007.sh` 92d28db561683256417c2cca4b10cf3e87bf3620850c595b96b1399d2e3b5267
- `tools/make_tokens_c2v007.py` cda665149f08bf22bf5247cdfae6f96f8bede8db185d1e3384a4a1f8567742a6
- `tools/fill_picard_member_c2v003.py` 54992e3353ff472f70ee4830bfcb816d9768dc15172a5c72b124bf310a273e20
- `tools/write_identity_records_c2v007.py` f3ae76b0816b1b9d3fe401c4034bac9c92715e1f2e6c1ff678b89c9c9bd7d871
- `tools/r5_gate_check_c2v007.py` 5dcd51422409f3354b480e67bd59c28f1b3412b756ea3228d834d133a673d745
- `tools/a71_inventory_c2v007.py` b8bda286f0fb04c11d8216dc028eb1d6f7ad957d5f34a4a8cda916976c432351
- `selftest/selftest_c2v007.py` 4d8a503828b2be6a5a0161b3fdc5bd3b772d9129d2e46e19ec3fd22e984c4357
- `selftest/canaries_c2v007.py` ff853f81f07fe11313840704278da76507134b8dcbc109397c154d1edb46819b
- `selftest/expect_c2v007.json` 5f611606b6e5ee9ff01a1c7ea5a415f600f889488a845965d3aa80f315941996
- `selftest/out/SELFTEST_C2V007_V002/SELFTEST_C2V007.json` ca057755003c006cb618fac4a2e9071b5723a316c362a0b02f0f9568c30a0101 (V001, superseded: 59ad8ed5b06b1b357e8dc633f7a041f26c78a8954021dba7770ef143aeeeebc4)
- `out/IDENTITY_C2V007_R4_V001/Z2.json` 10a028c53bdf7245d491c761afc63f3e5f745ddffd6b33e6255f9a01faf38751
- `out/IDENTITY_C2V007_R4_V001/Z2_OFF_RO1.json` 9a3284b26d1461a1b19f0117ecd382e3331c21cc25cb4f38889a225b0600fdd4
- `out/IDENTITY_C2V007_R4_V001/B0P_RERUN.json` 117677de157fe1e9c88f626e1118eec0072908e01ff37d781b930dd45153cbdd
- Every other file: `HASHES.txt`.
