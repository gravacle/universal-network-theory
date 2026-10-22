# sched v004a (S45_C2V004A): max_concurrent 8 (V006 A172)

Claude2 sched_s45_c2, for root (A172 "Build sched v004a with this one leaf"). Stamp (date -u at write): Mon Oct 19 20:11:04 UTC 2026.
Nothing was launched. Only the synthetic mock driver ran, under the pinned root monitor inside `v004a/test_runs/`, as in the v004 tests (G06).

## Base

The v004 hashes were verified from bytes before the build. `HASHES_S45_C2V004.txt` is `ab9561d58ba77ca12a0b2d7b3d2772ac2bd3955c17034a8d85a1c37ddfb559af`, and all 75 of its rows are OK. The v004 config is `cbc36b7af83fdde102290f1e6d33f100925ce47ac31394968988b59771edf751`.

## How the leaf was applied

`build_sched_delta_s45_c2v004a.py` first checks every pin. It then:
- reads the design value from bytes: `RUN_CONFIG_DDO154_V005.json` L78 is `"max_concurrent": 8,`, and `LAUNCH_V005.md` L182 reads "process budget 17, max_concurrent 8". It cross-checks both against A172's 8.
- writes `SCHED_DELTA_S45_C2V004A.json`, which sets only `max_concurrent` and appends one note citing V006 A172;
- applies the delta to the v004 config with the unchanged apply tool `apply_sched_delta_s45_c2v002.py` (`2a18b280`, which has `max_concurrent` in its ALLOWED_SET).

The v004 builder was not copied. It always rebuilds from R9 and also emits DIRECT_BATCH_PARAMS and CAPS, which this item must not change.

## Files (sha256 from bytes)

| file | sha256 |
|---|---|
| RUN_CONFIG_DDO154_CX2V006R9_S45_C2V004A.json | 63dac53de88303404c64e899856485bd912a4c493e44a93af0a6cb393240e4ec |
| SCHED_DELTA_S45_C2V004A.json | 5e2c0c4ac1bb4ea4836c29ec4806060c2c5ffaa3bca599b91849e1f147753c38 |
| DELTA_REPORT_S45_C2V004_TO_S45_C2V004A.json | fdd3d470ef292446a346bffc0a7687754a93143da39d75cd2625ef39c1c86ee4 |
| build_sched_delta_s45_c2v004a.py | 5ba736efa92a90d1fe0c44e37d9fbc5b1cc0a68ebe59e9480f8c9d6ec3d0f4a6 |
| leaf_diff_s45_c2v004a.py | 5ab247fd7f8bd068f6a29f155cfef37cb7e61ca48290dba27b5715e7e1113d47 |
| LEAF_DIFF_S45_C2V004A.json | 006e181fcf2ef0d895cc3b5bd3f8e68a9d28e1a57455afdc77e6853d77f12dc0 |
| pin_compare_s45_c2v004a.py | 9de41c574c962ecd8a6ce443a3a9316b76b438c16990f61a33000d67cfe6ea51 |
| PHYSICS_PINS_S45_C2V004A.json | b23390a8dc902d5471de9e92d47092c9182864810d4553e1d3d2c29ff5a7cb1c |
| tests/test_sched_s45_c2v004a.py | 922ea4b6c805bc5984af671f5b9ad470a0ad57cf352fb5d9534cdf9026a271d1 |
| TEST_STDOUT_S45_C2V004A_RUN1.txt = _RUN2.txt | 61fc621942c5bda73bd6ee93dce709a07efe4c4dbc87bf5639dc799277c64a27 |

`HASHES_S45_C2V004A.txt` lists every file here, including the stdouts, the DIFF_* files and all of test_runs. It does not list itself.

## Diffs

- **Against v004 (`cbc36b7a`):** the leaf diff is exactly `max_concurrent` (1 to 8) and `notes`. The notes keep v004's notes as a byte prefix plus one appended A172 note. In the text diff, only those two lines change.
- **Against R9 (`721c7230`):** v004's six leaves (`disk_guard.per_call_bytes`, `orphan_wait.cap_s`, `per_call.{output,rss,wall}`, `notes`) plus `max_concurrent`.
- **Equivalence:** R9 plus one combined delta (v004's set plus `max_concurrent`, both notes) gives the same bytes, `63dac53d` (test X01B).
- **pin_compare:** 78 of 78 physics pins are equal, and the rows are identical to v004's. The numerics canonical sha is `4b2a5a87efab5407c683ab0a3c1d7ea1da027ffa03fbf338b50cbb5ca4199e68`, unchanged. The changed top-level keys are `disk_guard`, `max_concurrent`, `notes`, `orphan_wait` and `per_call`, all scheduling-only.
- **Tool diffs:** pin_compare v004a changes only the successor path and the schema name relative to v004. leaf_diff v004a compares against v004 instead of v003 and records that DIRECT_BATCH_PARAMS is unchanged. Both diffs are in the DIFF_* files.

## Parent dry acceptance (as the v004 tests: plan_only on never-created work dirs)

The run uses the R9 wrapper's Context and plan_only on the R9, v004 and v004a configs. Each work dir is local and never created; no /Volumes path was opened, and the audit refuses any such open.
- **Same across all three:** campaign module campaign_c2v005, process budget 17, gates_ok, cache id, base spec sha, seed spec sha, weights, status OK, and the next wave apart from `batches`.
- **Cache id:** prefix `878d612a`, the same as the v004 tests. Equality of the full value across the three configs is asserted in K05.
- **Parent config block (L1724-1751):** it accepts (8, 17, True). It refuses max_concurrent 18 > budget 17 at L1732-1733 (K04B).
- **The process budget is what limits concurrency at 8.**
  - Each call is weighted peak 8 in route A and 2 after it. A start needs accounted processes plus 8 to be at most 17 (campaign_c2v005 L203), and starts are also bounded by the count check at L200. So at most 1 + (17-8)//2 = 5 calls can run at once, which is fewer than 8.
  - The parent's own L3316 gives a per-batch estimate of min(8, 17//8) = 2.
  - `campaign_dict` (L2638) passes max_concurrent 8, process_budget 17 and stage_aware true.
  - G06 ran 6 synthetic calls at 8. It observed at most 3 calls at once and 16 accounted processes (≤ 17), COMPLETE 6/6, with RSS cap RAM and no gate.

## Tests

Two runs: `test_runs/RUN_20261019T200922Z_52188` (TEST_RESULTS `305924ee2cccfce55876beb21c854d31c4afd6b6cc8bb5108a6a0431d4e93d33`) and `test_runs/RUN_20261019T200930Z_52275` (TEST_RESULTS `288cc360aa8ff93ca01685a17df66279b3d87cc60fbf106cc0a2688356803b02`).
- **Result:** 33/33 each (MUST_PASS 25, MUST_FAIL 8), with 0 audit denials. The only subprocesses were 6 pinned-python monitors per run. The stdout is byte-identical across the two runs.
- **Ported from v004 (b8fa8f42):** X01-X08, K00-K05, G01-G06, Z01-Z02 and A01.
- **New:**
  - X01B, the R9 equivalence;
  - X03, max_concurrent == 8 from the design bytes;
  - X04, the only leaf diffs against v004 are `max_concurrent` and `notes`;
  - Y01, the builder reproduces its outputs byte for byte;
  - Y02, caps v004 unchanged, so the wall is not re-derived;
  - Y03, a predecessor pin mismatch is refused;
  - Y04 and Y04A, the W1 path (see below);
  - K04B and K06, the budget limit;
  - D01, DIRECT_BATCH_PARAMS unchanged;
  - Z03, the leaf-diff record.
- **Dropped:** the v004 D02-D06 rows (DIRECT_BATCH_PARAMS content) and Y01/Y02/Y05/Y06 (caps-module internals). v004a does not touch those objects. v004's rows stand for them.
- `test_runs/*/rebuild_n4/` holds synthetic test outputs of the v004 builder under the tag S45_C2V9SYN, including a synthetic DIRECT_BATCH_PARAMS. They are not successors.

## What did not change

- DIRECT_BATCH_PARAMS_S45_C2V004 (`7c3ceae5`; its successor C2V004B is a separate A172 item).
- caps_s45_c2v004 (`f97541f6`); the wall cap of 100800 s, which stays PROVISIONAL under A140 N4 and was not re-derived; orphan_wait = wall + 600 s; RSS = RAM; output 80 GiB; the disk guard.
- campaign c2v005 (`d35d5d4a`), process_budget 17, stage_aware, campaign_wall_cap_s 172800, numerics and every physics pin.
- Single-thread BLAS (test env), and every v004 file (23 of 23 top-level rows re-verified in Z02).

## For root

1. **W1 rebuild path.**
   - The v004 builder's tested Y04 (A140 N4) path, which A172 names for W1, rebuilds from R9 and re-emits max_concurrent 1 (Y04, TESTED).
   - Applying this same `SCHED_DELTA_S45_C2V004A.json` with apply v002 to that N4 output restores 8. The result's leaf diff against v004a is then only the wall, the orphan wait and the notes (Y04A, TESTED).
   - Root rules the W1 procedure: the v004 builder N4 run plus this delta (no new code), or a builder successor.
2. **The config sha changes** from `cbc36b7a` to `63dac53d`. Anything that pins the v004 config sha must re-pin, and the wave plans record config_sha256 (parent L3320). The cache id is unchanged, so cache entries carry over.
3. **Claude4 reviews the v004 to v004a delta** before W1 (A172).
