# GATES_V006: identity comparator c2v006

Claude2, `tail_scheme_impl_c2/gates_v006/`, 2026-10-18 (about 15:40Z to 16:20Z).

**Rulings.** V005 addendum A59, A67 N1, A68, A69/A70 (comparator ruling), and A71 (no last-wins anywhere). The addendum sha at read time was 3380b0fa.

**Inputs.**
- Base comparator: c2v005 `6f656c68`.
- Codex2 cross-lineage review `review_comparator_c2v005_cx2/`: REVIEW.md `9317cd0d`, FINDINGS_CX2V001 `8a0700f7`.
- c2v004 check: `gates_v004/check/CHECK.md`.
- Drivers: r4 `b9ae92d5` and r5 `b5cc62af`.

There is no `gates_v005/check/` directory. `gates_v005/selftest/` is empty on bytes, so the builder left no c2v005 canary set; see the selftest section.

## Verdicts

| Item | Result |
|---|---|
| comparator `run_identity_compare_c2v006.py` | **097286d7** (full sha below) |
| selftest (`selftest/out/SELFTEST_C2V006_V001/SELFTEST_C2V006.json` 8b611f09) | **PASS**, all groups, on both r4 and r5 |
| r4 Z2 vs DDO154_A2F10_ROUTE_A_PARALLEL_N8_C2V008_DECIDING_RUN_V001 | **PASS_BITWISE_EQUAL**, 27/27 checks (`out/IDENTITY_C2V006_R4_V001/Z2.json` 4ab7cb39) |
| r4 Z2_OFF_RO1 vs the same reference | **PASS_BITWISE_EQUAL**, 27/27 (Z2_OFF_RO1.json 2b29c41e) |
| r4 B0P_RERUN vs DDO154_ROUTE_B_C2V009_DECIDING_ADMIT_PREFIX_RUN_V001 | **PASS_BITWISE_EQUAL**, 22/22 (B0P_RERUN.json 77ca040d) |
| r5 comparisons (three) | **UNTESTED**: at 16:10Z no `UVT_*_R5_RUN_V001.receipt.json` existed, so no r5 run was read |
| FIELDS records, r4 | B1 PASS_BITWISE_EQUAL_EXCEPT_DECLARED; B1_OFF PASS_BITWISE_EQUAL_EXCEPT_DECLARED; B0prime_RERUN PASS_RESULT_EQUAL_EXCEPT_DECLARED. **None of these is a seal record** (A67 N1: driver_sha256 is r4, not r5) |

## What c2v006 changes

c2v006 is c2v005 plus the items below. Every c2v004 and c2v005 check keeps its meaning; nothing is relaxed. The full diff is in `DIFF_c2v005_c2v006.diff` (ded144d3).

**(1) CX2-V5-B1, check NORM_INJECTIVE.** Normalization must be injective on each side.

`Side.norm` checks every dict at every depth. If two raw keys normalize to the same key, the check FAILs with a KEY_COLLISION entry that names both raw keys and the object path. The value becomes a COLLIDED sentinel that never compares equal, so nothing is last-wins.

The check also FAILs on:
- a raw key or string that already contains normalizer output (`<RUN>`, `<JSONFILE:`, `<RA_PAYLOAD:`, `<RA_IDENTITY_SHA`, `NPZ:`, `NPZ_INVALID:`, or any token label in use);
- two distinct 64-hex values that map to one hexmap token. NPZ content tokens are exempt, because NPZ content equivalence is declared;
- a token raw string paired with two counterparts, or one token label used for two pairs.

Two further rules:
- When one sha names several files, it maps to the sorted join of their tokens.
- `<RUN>` replaces the run root only when the next character is not `[A-Za-z0-9_-]`. A longer sibling name is therefore not the run, while `RUN.receipt.json` still normalizes.

On Codex2's exact counterexample, the report carries `KEY_COLLISION raw_keys [<new run>/x, <RUN>/x]`.

**(2) CX2-V5-S2, check STRICT_PARSE.** JSON files, JSONL lines, the tokens file and the checkpoint records are all parsed with `object_pairs_hook`.
- A duplicate member FAILs, naming the key and both values. This holds even when the two values are equal.
- Non-UTF-8 or unparseable input FAILs.
- A defective file reads as an UNPARSEABLE sentinel.
- A tokens file with a duplicate key is REFUSED.

**(3) CX2-V5-S3, check STRICT_PARSE.** NPZ archives are opened from their bytes with zipfile, and every central-directory entry is listed. Each of these FAILs, naming both entries:
- a duplicate member name;
- a member that is not `NAME.npy`;
- two members with one logical key.

Each member is read through its own ZipInfo, never by name, because a by-name read is last-wins.

**(4) CX2-V5-S1: structured dtype identity.** The header descr is compared as written, together with dtype.str, itemsize, and the ordered fields (name, offset, format, shape).

**(5) CX2-V5-S4, check TREE_STABLE: one read per file.** Each run file is read once.
- Its sha256 and its parsed value come from those same bytes. JSON, NPZ and NPY values are cached, and checkpoint records keep their raw bytes for the canonical-form check.
- JSONL and raw files are hashed from the bytes that are compared.
- The checkpoint module and the drivers are executed or AST-read from the bytes that were hashed.
- At the end, every recorded file is re-hashed. Any change FAILs.

**(6) CX2-V5-N1: the declared ARRAY_POLICY** (also recorded in every report).
- An array is a `.npy` file or one `.npz` member. Its identity is the tuple: header descr, dtype.str, itemsize, structured fields, shape, header fortran_order, sha256 of the logical C-order values, and sha256 of any trailing bytes.
- **Storage order is part of identity for .npy and .npz alike.** This keeps c2v004 H2's .npy rule and extends it to .npz.
- Neither NPZ compression nor member order is part of identity.
- `allow_pickle` is False.
- Route-A checkpoint blobs are compared by raw bytes (RA_BLOBS) and are not parsed.

**(7) A71, check NO_LAST_WINS.** Every list-to-mapping site has a guard:
- argv flags read by name: a repeated flag reads as DUPLICATE;
- stage_records names;
- normalized static-pin and declared route-A pin keys;
- canonical inventory paths (these also FAIL INVENTORY);
- driver-table dict literals in the AST reader.

**Own hardening.**
- Decoded numpy arrays keep dtype and shape in normalized form, and tuples stay tuples. The real caller records carry 4 ndarrays and no tuples; their types are equal on both sides (TESTED by the real PASS).
- A comparator exception writes a FAIL report (COMPARATOR_EXCEPTION, with the strictness checks marked partial) instead of crashing.
- An existing `--out` is refused before any work starts.
- A comparator source change during a run FAILs.

## Tokens (A59 replace mode)

`tools/make_tokens_c2v006.py` (21f9df0f) is the c2v005 tool (5891360c) with two changes: output names C2V006, and A71 strict parsing. Its rule and checks are unchanged.

| Driver | Z2 replace | Z2_OFF_RO1 | B0P | Derive record |
|---|---|---|---|---|
| r4 | 1aa5c8df | e54d4838 | 2b8ff1c3 | 28c63e8a |
| r5 | 8de762d1 | c1647c6d | 2b8ff1c3 | 613fedea |

Each declared list equals the c2v005 list for the same driver and gate (TESTED).

## Selftest (synthetic only)

`selftest/selftest_c2v006.py` (9ca7d24d) runs every group under both r4 and r5.

| Group | What | r4 | r5 |
|---|---|---|---|
| A | Codex2 reproducible counterexamples (source_audit whole-gate 9 + duplicate NPZ 2). Ported with paths only; each finding must FAIL on the check that owns it (key_collision: NORM_INJECTIVE with the KEY_COLLISION naming both keys; duplicate JSON or NPZ: STRICT_PARSE; structured and storage order: STAGES; ordinary changes: RESULT) | 11/11 | 11/11 |
| B | Codex2 c2v005 canary suites, ported: structural 23 and invocation/value 24 | 23/23, 24/24 | 23/23, 24/24 |
| C | the c2v004 CHECK canary set (B1/B2/S1–S3: F01–F30, P00–P08, Q01–Q05), ported onto c2v005/6-valid trees | inside 75/75 | inside 75/75 |
| D | own c2v006 canaries O01–O30 | inside 75/75 | inside 75/75 |
| S | source and unit checks | 7/7 | — |

The C+D total of 75/75 per driver breaks down as 13/13 MUST_PASS, 61/61 MUST_FAIL and 1/1 MUST_REFUSE.

**Group S** checks:
- load_cm, load_driver and driver_raw run exec/compile on the hashed bytes, with no `spec_from_file_location`;
- the reference-driver tables come from the hashed bytes;
- `Store.verify` detects a file changed after its single read;
- an equal-valued duplicate key is refused.

**Group C** is rebuilt on a new base because the c2v004 base trees fail c2v005's gates. Reason: they have no result driver_sha256 and no driver-planned scripts (TESTED: NEW_DRIVER_PIN and SCRIPT_CUSTODY fail on the B0P baseline). Every case is rebuilt on the Codex2 invocation fixture Tree. The c2v004 Q probes, which were declared-uncompared classes, are MUST_FAIL here.

**Group D** covers:
- key collisions at depth, in lists, one-sided, and through NPZ-equal hex keys;
- raw normalizer text in values and in keys;
- duplicate keys in nested JSON, JSONL, a new-only input and checkpoint IDENTITY.json;
- NPZ non-.npy and same-key members;
- structured field order, and aligned vs packed;
- trailing bytes; 1-D order (PASS); 2-D C vs F (FAIL);
- duplicate argv and duplicate stage_records;
- TREE_STABLE fault injection: a file is changed in place after its read;
- token pairing and label reuse; a tokens file with a duplicate key (REFUSED);
- two identity shas mapped to one token;
- the exception path and the run-root boundary;
- identical JSON files cited by sha (PASS);
- the plain-key form of Codex2's positive control (PASS).

**Expectations re-declared under c2v006 policy.** Both are stated in the harness, and the ported diffs are in `selftest/ported_cx2/DIFF_*`.
1. Invocation P17 (npz C vs F) changes from PASS to **FAIL** on STAGES, under ARRAY_POLICY.
2. The Codex2 source-audit **baseline** changes from PASS to **FAIL on NORM_INJECTIVE only**. Its fixture uses the literal key `<RUN>/x`, which is raw normalizer text. The same control without that text is D_O30 and passes.

**Discrimination.** The same C+D harness was run against c2v005 6f656c68 on r4 (`selftest/out/DISCRIMINATION_C2V005_R4_V001/CANARIES_C2V006.json` a5291748).
- c2v005 holds 13/13 MUST_PASS and every group-C case.
- It breaches 24 of the 30 group-D MUST_FAIL cases and the MUST_REFUSE case. Some breaches are a PASS, some a crash, and some fail only on an unrelated check.
- c2v006 breaches none.

**Coverage limit.** Codex2's unpublished-checker overlap item stays UNTESTED. These suites are ports and own cases, not a cross-lineage check of c2v006. A70 requires its own independent canary check.

## Real r4 identity comparisons

Each pair was run with:
- `python3 -I -B`, single-thread BLAS;
- `--driver r4` and the r4 tokens above;
- the three comparisons in parallel, 16:00:41Z to 16:10:46Z.

nice was unavailable in this sandbox, so the real comparisons ran at normal priority. The selftest ran under nice 10.

| Gate | Report | Wall time | Peak RSS | Files compared (both sides) | Files parsed (ref, new) |
|---|---|---|---|---|---|
| Z2 | 4ab7cb39 | 601 s | 6.2 GB | 4347, of which 46 logs were skipped | 3899, 3918 |
| Z2_OFF_RO1 | 2b29c41e | 606 s | 6.1 GB | 4347, of which 46 logs were skipped | 3899, 3900 |
| B0P_RERUN | 77ca040d | 133 s | 3.7 GB | 1245, of which 38 logs were skipped | 823, 823 |

The new strictness checks pass on all three pairs:
- STRICT_PARSE: 0 problems;
- NORM_INJECTIVE: 0 collisions, 0 raw normalizer text, 0 shared-sha joins;
- NO_LAST_WINS: 0 hits;
- TREE_STABLE: 0 changes.

So the c2v005 PASS verdicts on these pairs are confirmed under the stricter rules (TESTED).

## FIELDS records (`records/R4_V001/`)

`tools/write_identity_records_c2v006.py` (ecee65a4) writes schema UNT_KMAX_TAIL_V007_GATE_RECORD_C2V002 with the FIELDS_R8 §6 field names. Everything is read from bytes:
- the comparator and token shas are recomputed and must match the report;
- the result and reference shas;
- the receipt result and driver pins;
- the call spec;
- the B1 domain: outer K_big 2.0 = K 2.0, with domain_empty_all_stages true.

| Record | Sha | Verdict |
|---|---|---|
| B1_R4_C2V006.json | e5228566 | PASS_BITWISE_EQUAL_EXCEPT_DECLARED |
| B1_OFF_R4_C2V006.json | d3df0fef | PASS_BITWISE_EQUAL_EXCEPT_DECLARED |
| B0prime_RERUN_R4_C2V006.json | afd76dcd | PASS_RESULT_EQUAL_EXCEPT_DECLARED |
| WRITE_RECORDS_R4_C2V006.json | c9c7db09 | — |

Reference shas: 883b37a0 for B1 and B1_OFF, f33eb362 for B0prime_RERUN. differences_outside_custody and differences_outside_declared are `[]`. The B0prime_RERUN call spec is 4ac5527a.

**precondition_L (B1)** is computed in the writer and recorded with its basis.

TESTED from bytes:
- f33eb362 (v009 deciding (i)) and b76f7afc (v008 deciding (i)) are both COMPLETED on the same spec;
- their rows, speeds_km_s and final_pass are bitwise equal;
- their deciding_test blocks are identical: PASS_BITWISE_EQUAL, 360/360 columns, against the same saved chain. A30 records the same result.

UNTESTED: a file-by-file compare of the two deciding-(i) trees. Their stage-array equality holds only transitively, through the saved chain.

**A67 N1.** All three records carry `a67_n1.is_v010_r5 = false`, because the runs carry r4 result driver_sha256. Under compare r8 an r4 identity run reads IDENTITY_RUN_DRIVER_NOT_V010_R5_A67_N1. These records are the A68/A70 c2v006 rerun on r4. The seal records must come from the r5 runs.

## UNTESTED, each with its deciding test

| Item | Deciding test |
|---|---|
| The three r5 comparisons and their records | Once each `UVT_*_R5_RUN_V001.receipt.json` exists (receipt status FINISHED), run the three commands above with `--driver r5` and the R5 tokens (Z2 8de762d1, Z2_OFF_RO1 c1647c6d, B0P 2b8ff1c3) into `out/IDENTITY_C2V006_R5_V001/`. Then run `tools/write_identity_records_c2v006.py --driver r5 --reports out/IDENTITY_C2V006_R5_V001 --outdir records/R5_V001`. |
| Independent canary check of c2v006 (A70) | A cross-lineage lane runs its own canaries against 097286d7 |
| A file changed and then restored between its single read and the end-of-run re-hash | Not detectable by re-hashing. Compared content is still the in-memory bytes whose sha is recorded, so the result reflects what was read. No check claims more than that. |
| precondition L as a full pairwise tree compare | A comparator gate for a v008 vs v009 deciding-(i) pair (none exists) |

## Hygiene

- Runs read: the finished r4 identity runs with receipts (UVT_Z2_A2F10_RUN_V001, UVT_Z2_OFF_RO1_A2F10_RUN_V001, UVT_B0P_RERUN_ADMIT_PREFIX_RUN_V001) and the CLAUDE2/runs references. That includes DDO154_ROUTE_B_C2V008_DECIDING_ADMIT_PREFIX_RUN_V001/result.json, read for precondition L.
- Not read: KMAX_A2F10_C5H_RUN_V001 and every NGC target.
- **Disclosure, r5 listing:** one shell glob, `ls runs_ext/UVT_*R5_RUN_V001*`, listed the top-level names (inputs, progress.jsonl, stages, start.json) of the three unfinished r5 run directories. No file in them was opened.
- Nothing was launched. Nothing was deleted or moved. No existing file was edited.
- **Disclosure, writes outside gates_v006:** development-only outputs went to this session's scratchpad (`.../scratchpad/dev_*.json|log`, `.../scratchpad/c2v006_dev/`). These were:
  - dev comparator runs of intermediate builds on the three r4 pairs. The two Z2 dev runs report COMPARATOR_SOURCE_CHANGED_DURING_RUN, because the source was edited while they ran;
  - dev selftests.

  They are not evidence, and none is cited above.
- Python: the codex runtime, `-I -B`. Hashes are sha256 from bytes and are listed in full in HASHES.txt.

## Files (sha256 from bytes)

- `run_identity_compare_c2v006.py` 097286d762dd171361e7ff5bbb98b3d48029e790de5869b28aa6218098491e48
- `DIFF_c2v005_c2v006.diff` ded144d333a50eaa0f0d45a36850f104227ed348a5db1abcff46c6658bd6621b
- `tools/make_tokens_c2v006.py` 21f9df0f7442f4de121b5425ce60d448e292f9ba69e4c700ffc056ebca6cc4d7
- `tools/write_identity_records_c2v006.py` ecee65a4d52920adc5f3c0dfe6f1fc7fa343909142cc56da6d3ac8ccaefc13b2
- `selftest/selftest_c2v006.py` 9ca7d24de7d837fc66771d34ae6b44701f1071780ce8de1ce7a6b446e28d4a30
- `selftest/canaries_c2v006.py` 3a225d41b64a3729bdc3994e85e3abf79135fb1e01810bfb8cce9c5820c15223
- `selftest/out/SELFTEST_C2V006_V001/SELFTEST_C2V006.json` 8b611f092dec968f751e1078667aba32c7ef39b71f5d9f9e0bf3706c978d2610
- `out/IDENTITY_C2V006_R4_V001/Z2.json` 4ab7cb393e6b0f78c095a60284c75b967351161c380c53f1c9ac59224703351c
- `out/IDENTITY_C2V006_R4_V001/Z2_OFF_RO1.json` 2b29c41e601f1b3317183678fbc193eae423b5e63134a8bebd27470d343703f2
- `out/IDENTITY_C2V006_R4_V001/B0P_RERUN.json` 77ca040de386fc750d136a28b66f6819a285939ee820ee54be0f07f17563aff6
- `records/R4_V001/B1_R4_C2V006.json` e52285660b1a4b5c52cbf68a08de40306e4796676af27af758a33883f1192e34
- `records/R4_V001/B1_OFF_R4_C2V006.json` d3df0fef53aca5539d3e5a6c2be6311afc1f42dc0f34ffe3399e7a88f8cb2d98
- `records/R4_V001/B0prime_RERUN_R4_C2V006.json` afd76dcd879836cb8755e97704c71fd1b6f07280a1ff64c5f46ce38264eff576
- Every other file: `HASHES.txt`.
