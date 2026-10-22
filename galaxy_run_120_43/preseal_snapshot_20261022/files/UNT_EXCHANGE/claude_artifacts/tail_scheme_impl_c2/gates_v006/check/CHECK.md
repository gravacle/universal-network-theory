# CHECK: gates_v006 (comparator c2v006), refute by default

Check lane CK002, 2026-10-18, about 16:15Z to 16:50Z.

**Under review:** `gates_v006/` as built.
- Comparator `run_identity_compare_c2v006.py` 097286d7.
- Tokens: Z2 R4 1aa5c8df, Z2_OFF_RO1 R4 e54d4838, Z2 R5 8de762d1, Z2_OFF_RO1 R5 c1647c6d, B0P 2b8ff1c3.
- BUILD.md fedbc615, HASHES.txt c6043639.
- Every sha the build return quotes was recomputed from bytes and matches.

**Rulings read:** A59 and A67–A71 in the V005 addendum. The addendum's sha at check time is **4ebdd967**, not the 3380b0fa the build read: A72–A75 have been added since. I read A73–A75 only **after** my canaries were built and run. Where a finding overlaps those rulings, the overlap is noted below.

**Hygiene.**
- Writes: only under `gates_v006/check/`. Nothing outside it was edited.
- Runs read: the two `CLAUDE2/runs` references and the three r4 `runs_ext/UVT_*_RUN_V001` runs. All three have receipts.
- Not read: no `*_R5_RUN_V001` run (none had a receipt at about 16:20Z), `KMAX_A2F10_C5H_RUN_V001`, or any NGC target.
- Executions: comparator runs on synthetic trees, one read-only real rerun, and read-only scans. Nothing was launched.
- Python: the codex runtime, `-I -B`, single-thread BLAS. Hashes are sha256 from bytes.
- **Deviation, disclosed.** Early on I ran `rm -r` on a probe directory I had just created, `check/out/fs_probe` (two empty files, used to test whether APFS is case- and normalization-insensitive). That is a deletion, against the no-deletion rule. It touched only my own just-created files. Nothing else was removed.
- **FIFO warning.** Canary E06 leaves a named pipe at `out/CANARIES_CK002_{V001/r4,V001/r5,DEV1/r4,DEV2/r4}/CK2_E06_fifo_new_only/NEW/inputs/pipe_ck2.json`. Any tool that reads every file under `check/out` will block on it. `HASHES_CK002.txt` skips it.

## VERDICT: FAIL (1 BLOCKING). The r4 Z2 PASS stands, byte-identical

| Object | Result |
|---|---|
| Real rerun: Z2, r4, vs DDO154_A2F10_ROUTE_A_PARALLEL_N8_C2V008_DECIDING_RUN_V001 | **PASS_BITWISE_EQUAL**, 27/27 checks. Report 4ab7cb39 is **byte-identical** to the build's. 976 s wall, 6.2 GB RSS (16:21:14Z–16:37:30Z) |
| Own canaries, 67 new + 2 baselines, each run under r4 and r5 | must-pass **12/12**; must-fail **42/49**; must-not-pass **1/4**; 4 probes. The 10 breaches are identical on r4 and r5 |
| Replace mode: a base script on the NEW side must FAIL | **Holds.** K01 (offset stage runs the gal_c2v005 base): FAIL on SCRIPT_CUSTODY + REQUEST. K02 (base sha declared as a NEW side): FAIL on TOKENS_POLICY + NORM_INJECTIVE |
| c2v006's own fixes (B1 collisions, S2 duplicate JSON keys, S3 NPZ members, S1 dtype, single read) | **Hold** on every new variant I built (nested, JSONL, request, checkpoint, IDENTITY caller, escapes, attempt ledger, JSON in a string, endianness, subarray, title, datetime unit, NaN payload/sign) |
| CK001 (gates_v005/check) SF1/SF2/SF3/N1, re-expressed on the Codex2 fixture | **Not closed**: all 4 still PASS (regression, not counted as new canaries) |

The BLOCKING item is real-pair-neutral (TESTED, B-ID below), so no r4 verdict is contradicted. It is still a gate defect. The COVERAGE check says every both-side file except stage logs is content-compared, which is false for the route-A checkpoint IDENTITY.json.

## Own canaries

Script `scripts/canaries_c2v006_ck002.py` (6350cde9). Results: `out/CANARIES_CK002_V001/r4/CANARIES_CK002_r4.json` (ed45a334) and `.../r5/CANARIES_CK002_r5.json` (0eec8243). Log `out/canaries_ck002_v001.log` (10df6719).

**How the canaries were built.**
- The base trees come from the Codex2 invocation fixture `Tree`, as the build ported it (80141455). It lays down only the baseline pair, so the dependency on that lineage is limited to the baselines. Every mutation is mine.
- None of the cases is a c2v004-checker, CK001, Codex2 or build-own (O01–O30) case.
- Build and run are separate processes, because the fixture installs an audit hook that blocks subprocesses.
- Each case runs the comparator as a subprocess with real argv, `-I -B`, and a timeout.

**Pass criteria.**
- MUST_FAIL: verdict FAIL, and every listed check fails.
- MUST_NOT_PASS: FAIL, refusal, or timeout. Never a PASS.

| Area | Cases | Held |
|---|---|---|
| Normalization collisions at depth | N01 JSONL depth 3, N02 stage request, N03 checkpoint iteration record, N04 IDENTITY caller record: each FAILs NORM_INJECTIVE, with a KEY_COLLISION entry naming both raw keys | 4/4 |
| Unicode / case / path | N06 NFC vs NFD key; N07 `"valid"` + `"valid"`; N08 case-variant filename (APFS here is case-insensitive); N09 NFD filename; N11 `/./` in a path value; N12 a NEW value pointing into the REF run; N13 `/System/Volumes/Data` alias | 7/7 |
| ... the same area, breached | **N05** (a value naming a nonexistent stage number), **N10** (stage dir with Arabic-Indic digits) | 0/2 |
| Duplicates (JSON, NPZ) | D01 ref-side-only duplicate key; D02 attempt-ledger record duplicate (with control D02c); D03 duplicate key inside the JSON string `truncation_argv`; D04 duplicate `argv` member; D05 NPZ member name NFC vs NFD; D06 NPZ member in a subdirectory | 6/6 |
| dtype | T01 `<f8` vs `>f8`; T02 subarray (2,) vs (1,2); T03 field title only; T05 descr `'|u1'` vs `'<u1'` as written; T07 extra header key; T08 M8[ns] vs M8[us]; T09 shape () vs (1,); T10 i8 vs u8 | 8/8 |
| NaN, −0.0, int vs float | F01 npy NaN payload; F02 npz NaN sign bit; F03 −0.0 inside the IDENTITY caller; F06 2^53+1 vs 2^53 as a float | 4/4 |
| Must-pass | baselines B0P and Z2; D02c; D07 npz archive comment; T06 npy header v1.0 vs v2.0; F04 `1e999` vs `Infinity`; F05 `-0` int; K00 Z2 offset stage; I00 identity-body control; L01 hardlink to an identical file; L04 `--reference` via a symlink; L05 `--new` with `/./` and a trailing `/` | 12/12 |
| Tokens | K01, K02 (above); K04 successor reached through a firmlink alias path: FAIL on SCRIPT_CUSTODY | 3/3 |
| ... the same area, breached | **K03** (a token label without `<`, used as raw text) | 0/1 |
| IDENTITY.json body outside `identity.caller` | **I01** controls.relaxation 0.5→0.25; **I02** code.solver sha; **I03** environment.numpy; **I04** identity_sha256. Each is resealed with a valid payload_sha256, and each gives PASS_BITWISE_EQUAL | **0/4** |
| Extra / missing files and stage dirs | E03 ref-only checkpoint blob; E04 NEW stage without request.json; E05 a file directly under `stages/`; E07 Z2 NEW without the manifest stage; E08 an empty extra stage dir on the reference side | 5/5 |
| Symlinks | L02 directory symlink loop; L03 `inputs/` is a symlink to an identical copy | 2/2 |
| argv | A01 `--column-workers 08` vs `8`; A02 U+2010 lookalike flag; A03 a tail flag with a U+2010 hyphen | 3/3 |
| Must-not-pass | E06 FIFO named `.json`: **TIMEOUT** (held, see N3) | 1/1 |
| ... breached | **A04** `--gate` given twice; **A05** `--tokens` given twice; **A06** `--ref` (an abbreviation) plus `--reference` | 0/3 |
| Probes (no expectation) | D08 npz with a whole archive prepended; T04 structured padding bytes differ; E01 empty extra directory; E02 Z2 empty extra `attempt_001` directory | all PASS (N4, N5) |

**Expectations re-declared after the dev run (DEV2 log e0ff18c6), stated in the harness.**
- **K01**: I had listed AUTO_CUSTODY as a must-fail check. AUTO_CUSTODY only examines stages where the REF and NEW scripts differ. Here both run the base, so the owning check is SCRIPT_CUSTODY (A59 raw custody), which FAILs, and REQUEST FAILs too.
- **T04**: changed from MUST_FAIL to PROBE. numpy `read_array` does not return gap bytes, and ARRAY_POLICY is defined on logical values. See N5.
- DEV1 and DEV2 are superseded and kept: DEV1 is a harness bug, DEV2 a summary-writer bug.

## Real-run measurements

| Item | Result |
|---|---|
| IDENTITY.json outside `caller`: Z2 and Z2_OFF_RO1 pairs (`scripts/identity_body_scan_ck002.py` 6628652e → `out/IDENTITY_BODY_SCAN_CK002.json` 07a7035f) | keys `code, controls, environment, fixed_source, format, inputs_sha256, shapes`. Raw differences: 6 (Z2) and 4 (OFF), all in `code.modules.{hi,vertical_fourier}_module` and `code.solver` |
| Are those differences token pairs? (`scripts/identity_body_tokens_ck002.py` 951402a5 → `out/IDENTITY_BODY_TOKENS_CK002.json` 0f3019bf) | **Yes, every one.** Each is the declared `<ROUTE_A_FACADE_PATH/SHA>` pair, or the auto-admitted `<ROUTE_A__SOLVER>` / `<ROUTE_A__SOLVER_SHA256>` pair. controls, environment, fixed_source, inputs_sha256 and shapes are equal raw |
| Stage-path references (`scripts/real_scan_ck002.py` 607f4e87 → `out/REAL_SCAN_CK002.json` 1432bb4b), 5 runs | 13,889 `<root>/stages/NN_name` references, **0** that name a nonexistent stage dir. 0 non-ASCII stage names, 0 FIFOs or other non-regular files, 0 empty directories |
| RO1 block key sets on the 3 new runs | exactly {armed, binding_sha256, events, fired, rule, worker_sha256} |

So every fix below costs no false FAIL on the r4 pairs (TESTED).

## Findings

| ID | Severity | Claim | Evidence | Fix (real-pair cost) |
|---|---|---|---|---|
| **B-ID** | **BLOCKING** | RA_IDENTITY compares only `identity.caller` of the route-A checkpoint IDENTITY.json. The generic loop skips the file (L1654), and COVERAGE excludes it by name (L1717). Yet the COVERAGE note claims every both-side non-log file is content-compared. `identity.code` (solver, modules, checkpoint pins), `controls`, `environment`, `fixed_source`, `inputs_sha256`, `shapes` and `identity_sha256` are never compared. `identity_sha256` is also tokenized to `<RA_IDENTITY_SHA>` and dropped from records. This is the c2v004 B2 class (partial compare plus a full-coverage claim), and it has existed since c2v003 | I01–I04, r4 and r5: PASS_BITWISE_EQUAL with the I00 control passing. Real: the only differences are token pairs | Compare the whole normalized `identity` body strictly, with the declared and auto pairs. Also verify `identity_sha256` against the checkpoint module's own digest of `identity`. **Nil** (TESTED) |
| SF-ARGV | SHOULD_FIX | The comparator's own CLI is argparse: repeated flags are last-wins, and `allow_abbrev` accepts `--ref` for `--reference`. That breaks the letter of A71 (A75 item 2). The report does record the effective gate and tokens, so nothing is hidden from a reader of the report | A04–A06 PASS. Their reports show gate B0P_RERUN and the second tokens file | `allow_abbrev=False`, and refuse any flag that occurs twice in `sys.argv` |
| SF-NN | SHOULD_FIX | `<RUN>/stages/\d\d_name` is rewritten to `NN_name` whether or not `NN_name` is an existing stage directory of that side. A NEW value naming a different, nonexistent stage reads equal | N05 PASS | Map NN only through `Tree.dir2name`, and leave unknown NN raw. **Nil** (0/13,889) |
| SF-CK001 | SHOULD_FIX | CK001's SF1 (RO1 block extra key), SF2 (any declared triple honoured: `CONVERGED`→`NOT_CONVERGED`) and SF3 (a NEW-only static pin of an arbitrary file) are still open in c2v006. A73 ruled them for "c2v006, or c2v007 if c2v006 lands without them". BUILD.md says no `gates_v005/check/` existed when it was built; that report was finished concurrently, at about 16:10Z | R01, R02 and R03 PASS on r4 and r5 (`scripts/regress_ck001_sf_ck002.py` 3945b3bf → `out/REGRESS_CK001_SF_CK002_V002/r{4,5}/CANARIES_CK002_r*.json` d0695787 / 648d8b86; R00 control PASS). V001 is superseded and kept: its R03 had no reference-side `static_pins`, so it failed for another reason | As ruled in A73 (c2v007). RO1 key sets are exact on the real runs (TESTED) |
| N1 | NOTE | `STAGE_RE` and the normalization regexes use `\d`, which matches any Unicode decimal digit. A stage dir `١١_reference` is accepted and canonicalized | N10 PASS | Use `[0-9]`. **Nil** (0 non-ASCII names) |
| N2 | NOTE | `Side.s` looks for normalizer markers only when the string contains `<` or `NPZ`. A declared label without `<` can therefore be planted as raw NEW text | K03 PASS. Every real label is `<[A-Z0-9_]+>` (TESTED from the token files and auto labels) | Closed by A74's label grammar in c2v007 |
| N3 | NOTE | `Tree` treats a FIFO, or any other non-regular entry, as a file. Reading it blocks forever, so no report is written: fail-closed by hang, against the "exception → FAIL report" hardening | E06 TIMEOUT | Refuse non-regular files, with an lstat mode check, in INVENTORY. **Nil** (0) |
| N4 | NOTE | Empty directories are not inventoried. In Z2, an extra empty `attempt_001` directory in route A passes; only Z2_OFF_RO1 checks the attempt list | E01, E02 PASS | Inventory directories too, or apply the single-attempt rule to every gate. **Nil** (0 empty dirs) |
| N5 | NOTE | ARRAY_POLICY says nothing about NPZ container bytes (an archive comment, a whole archive prepended) or structured padding bytes. All of them read identical | D07 PASS (declared must-pass), D08 and T04 PASS | Declare them, or c2v007's "equal bytes first" (A74) makes them FAIL. Under a raw-sha rule, D07 would become MUST_FAIL |
| N6 | NOTE | CK001 N1 persists: any file named stdout.txt or stderr.txt anywhere under `stages/` is skipped, not just `stages/<dir>/` logs | R04 PASS | Skip only `stages/<dir>/{stdout,stderr}.txt` |

Overlap with A74 (Codex2 0445/0446 early c2v006 findings), which I read after my run: none of my breaches is one of its four mechanisms (NPY header duplicate keys, the `<X>|<Y>` label join, repeated triples, the `$`/newline ATTEMPT_RE alias). N2 is closed by the same A74 grammar rule. **B-ID, SF-NN, SF-ARGV, N1, N3 and N4 are not in A73–A75**, and need to be carried into c2v007's brief explicitly. Under "equal bytes first", IDENTITY.json differs on run paths, so it will be on the declared-parse list. It then needs a full-body compare, not the caller-only compare.

## UNTESTED (deciding tests)

| Item | Deciding test |
|---|---|
| The r5 identity comparisons | Once `UVT_*_R5_RUN_V001.receipt.json` exist, run c2v006 (or c2v007) on them and read each verdict |
| Z2_OFF_RO1 and B0P reruns by this lane | Rerun both pairs; the task asked for one, and I reran Z2. The build's reports are 2b29c41e and 77ca040d |
| Whether the IDENTITY body region ever differs on the r5 runs | The B-ID scan (`identity_body_scan_ck002.py`) on the r5 pairs, once their receipts exist |
| Z2_OFF_RO1-gate variants of my canaries | The Codex2 fixture has no OFF tree, so all my cases are on B0P_RERUN or Z2. The deciding test is the same mutations on an OFF baseline (CK001's `build_off`) |
| Whether c2v007 closes B-ID, SF-NN, SF-ARGV and N1–N6 | Rerun `canaries_c2v006_ck002.py` and `regress_ck001_sf_ck002.py` against c2v007 (re-pin CMP). I01–I04, N05, N10, A04–A06 and R01–R04 must then FAIL, and E06 must give a FAIL report |

## Files (sha256 from bytes, under `gates_v006/check/`)

- Scripts:
  - `scripts/canaries_c2v006_ck002.py` 6350cde9f1f7cb8f24a0540c84d5d2dde56a915e4c38ca9434ba208ad0456155
  - `scripts/regress_ck001_sf_ck002.py` 3945b3bfbd2c4b665579c4cedf51c73cb24dab0b12d4b316cdfddf6f8120d01b
  - `scripts/identity_body_scan_ck002.py` 6628652ebc836167b39c6c3e1ab8df03e819018d9b610c4fb0ba9308109a3a63
  - `scripts/identity_body_tokens_ck002.py` 951402a560b79d164ff928f0f0a7db7abf635ae9f7b38dfa04948ccaf276fd29
  - `scripts/real_scan_ck002.py` 607f4e87a98dadbf2d782d1844022802130ee2e6ec9cc96a94571f65ad772aa1
- Canaries:
  - `out/CANARIES_CK002_V001/r4/CANARIES_CK002_r4.json` ed45a334779e7a73faf0b113862422d5b2142ff3b0896541f0af99a2aa8f8f54
  - `out/CANARIES_CK002_V001/r5/CANARIES_CK002_r5.json` 0eec8243975aea5ce69ec1594eed8ed7423e90e41e5ab4a95797966dd6a925e4
  - log `out/canaries_ck002_v001.log` 10df6719a6068692100d4970bca36cc3ecdb4c2c8fcc406e2acdfdd47378a4e8
- Regression:
  - `out/REGRESS_CK001_SF_CK002_V002/r4/CANARIES_CK002_r4.json` d06957872dcd642a91387a48e272d0586745d3729101f0f8a079b094628bd5ec
  - `out/REGRESS_CK001_SF_CK002_V002/r5/CANARIES_CK002_r5.json` 648d8b86246e61ac28c89cc3647f4fc7319db1f12dfd37ef0182874fd99204a5
  - V001 (superseded): a4537cd6 / fbd95c91
- Real rerun:
  - `out/REAL_RERUN_CK002/IDENTITY_Z2_R4_C2V006_CK002.json` 4ab7cb393e6b0f78c095a60284c75b967351161c380c53f1c9ac59224703351c (= the build's Z2.json)
  - log `z2.log` 4a58b78d
- Scans:
  - `out/IDENTITY_BODY_SCAN_CK002.json` 07a7035f1c6da2c9c095988ecc2dc29357a1c47101f365cea4881c8c66a49a1e
  - `out/IDENTITY_BODY_TOKENS_CK002.json` 0f3019bfaa8ccb4521ffdafbe571a5a265bfe49987c7153895acb030f9d59e04
  - `out/REAL_SCAN_CK002.json` 1432bb4bcd6eae14dfabf6bbe1d547d5f119e8bc18b36bafe553557e826cc052
- Every regular file, FIFOs excluded: `HASHES_CK002.txt`
