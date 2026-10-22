# INDEX_R2 (ROUND1) — miss-reading prereg r2, Claude4, dispatch 0585

Built by `tools/make_miss_reading_c4v002.py` from the draft folder, with exclusive create into a new folder.
The V005 per-entry pins in section 11 of the prereg were read from the addendum bytes at assembly.

| file | role | sha256 |
|---|---|---|
| PREREG_MISS_READING_R2.md | the prereg text r2 (unsealed) | `6437ea33432f50971eef81e549a8e5789d0bd892efaf2d0f423ce4c933f30143` |
| CLAUSE_SOURCE_MAP_R2.md | where each clause comes from, plus the 0585 coverage table | `b105b55d7f80c5868d936f577ce81e92992999440f5cd85a06decbc62650d24b` |
| ROOT_ITEMS_R2.md | M-1 to M-12, each with a recommendation | `1d7af792f9b115fc7882254b694d82299217c3ab846d7d26d591f45a5c5eaf7f` |
| NUMBER_PROVENANCE_R2.json | the target-free source of every numeric token in the prereg | `c81b5a7a579476480a085681ebd6eb8aa445e38b6a7abe2284dba3716b0c2832` |
| TARGET_FREE_CHECK_R2.json | the T1–T6 result on these bytes: **PASS** | `aab683236116bc3562df86f3b9542a54eec3446c44a8f0e5569ff2b305d2180b` |
| TARGET_FREE_MUTATION_TEST_R2.json | the check FAILs on each of 14 violation kinds (all_ok True) | `2a8202b823beb5cd0bc03c9e1e2b0377d9de59410a698c8d185f39739d66bc41` |
| tools/check_target_free_c4v001.py | the target-free check | `85457a43c654aa13b49fa528b786a615e99a51eaa29b4ba42687a2c0f3396cc7` |
| tools/test_check_target_free_c4v001.py | the mutation test | `fc403648a57b3f0ee30b164e2cde48e3c1889bfee33938c8b23a93c1fd88ea11` |
| tools/make_miss_reading_c4v002.py | this generator | `8c0d9fc2fb962f3e72de9e6a7a03cc11aa38efccd59981713fbcc0008b32576a` |

V005 at assembly: `17cb4fd496845823227562682341eb605304d0ec14842d3e26369215e49d538b` (last entry A89).

**What the check proves, and what it does not.**
- **Proved (by construction, from bytes):** the text names no target file, data source, velocity value or target symbol value (T1–T3).
  - Every number in it has a target-free source (T4). The query radii are verified against the slots bytes.
  - Every pinned source is target-free and hashes as stated (T5). The open V005 is pinned per entry.
  - Every clause is mapped (T6).
- **Not proved by the script:** that no rule depends on a target value. That is a semantic property.
  - The rules use only frozen quantities, plus (v_q, sigma_q) inside the score output (I-2, I-3).
  - The independent lens checks review this property.
- **No target was ever opened.** The check cannot compare against target values; it never needs to.
