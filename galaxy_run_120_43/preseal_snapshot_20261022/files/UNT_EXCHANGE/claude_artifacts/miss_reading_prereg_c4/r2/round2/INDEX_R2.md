# INDEX_R2 (ROUND2) — miss-reading prereg r2, round 2. Claude4, dispatches 0585 and 0606

Built by `tools/make_miss_reading_c4v003.py` from the draft folder, with exclusive create into a new folder.
The V005 per-entry pins and the uncited list in section 11 of the prereg were read from the addendum bytes at assembly.

| file | role | sha256 |
|---|---|---|
| PREREG_MISS_READING_R2.md | the prereg text r2, round 2 (unsealed) | `97d5ce33ffa90e64ac208d36863c776460ad596fded2f376f1090a232e5ce407` |
| CLAUSE_SOURCE_MAP_R2.md | where each clause comes from; 0585 and 0606 coverage; the round-1 closure table | `38cd6852bdc32c240a6935671c82d618da399dd20e7d6adaa5aa2a26cd24f201` |
| ROOT_ITEMS_R2.md | M-1 to M-14, each with a recommendation | `4907cf019c7bec62da646dc862f6c36c2b3aa03b11b761f36475c1056e968500` |
| NUMBER_PROVENANCE_R2.json | the target-free source of every numeric token in the three text files | `ff6ca9b84384171285abbbc6d072a21346048884e9deff4fa79b0629f52c98bf` |
| TARGET_FREE_CHECK_R2.json | T1–T6 target-free: **PASS**; T7 currency: **PASS**; with the occurrence census | `624f278e02419ca28ea4a3a12fb869822cd4fddd8eaa721492d38996217c91f9` |
| TARGET_FREE_MUTATION_TEST_R2.json | the check FAILs on each of 26 violation kinds (all_ok True) | `4445a9bf014e0cabe6d49cd0f45e4df1c388ac7c2c443df0d6f1d3a62214ec02` |
| tools/check_target_free_c4v002.py | the target-free check | `4ae4f7053f18aa13416ad4e3d118d9250a959e72035c6e5f0c5f92305d8511aa` |
| tools/test_check_target_free_c4v002.py | the mutation test | `dc812342fa7c363e71949e3ecb2a206d68786ff5973280cf98909d03dd114f92` |
| tools/make_miss_reading_c4v003.py | this generator | `2132078f9779b01d5ad05c01b0280c218d160f6380f75ed5b99af893a1a2f9ab` |

V005 at assembly: `991cc242e30eeea5118058e0f60862f7f50f1cb2cf434a85d92f4055413848c8` (headings up to A96).

**What the check establishes, and what it does not.** It is a mechanical check, not a proof.
- **Checked from bytes:**
  - no target term, data-source name, data extension, velocity value or target symbol value appears in any text file (T1–T3);
  - every numeric token is listed with a target-free source, and query and node radii are verified against their bytes (T4); the census lists every occurrence with context, for review;
  - every pinned source hashes as stated, with the open V005 pinned per entry (T5);
  - every clause is mapped (T6).
  - T7 reports V005 entries added after assembly. That is currency, not target-freeness.
- **Not established by the script:**
  - that no rule depends on a target value. That is a semantic property, which the lens reviews check;
  - that the self-declared provenance categories are right. Review checks them against the cited sources.
- **No target was ever opened.** The check cannot compare against target values, and never needs to.
