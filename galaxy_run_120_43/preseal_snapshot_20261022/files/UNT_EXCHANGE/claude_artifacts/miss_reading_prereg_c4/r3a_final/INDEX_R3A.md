# INDEX_R3A (r3a): the miss-reading prereg r3a. Claude4, dispatches 0585, 0606 and 0619 (A98), and 0687 (A133)

Built by `tools/make_miss_reading_c4v005.py` from the draft folder below, with exclusive create into a new folder. The V005 entry table in the prereg's sources section is rendered from the hand-written `V005_ENTRY_TABLE_R3A.json`, after the generator checked it against the V005 bytes (every heading once, in file order, verbatim; each pinned section sha). The cited V005 set is taken from the texts, and every cited entry is pinned.

| file | role | sha256 |
|---|---|---|
| PREREG_MISS_READING_R3A.md | the prereg text r3a (unsealed) | `9e45cd4d709fa20245bb983c7d9fb5a085c8def1bb15c973c976c2dde764618d` |
| CLAUSE_SOURCE_MAP_R3A.md | where each clause comes from; dispatch coverage; closure tables | `185bb7190714adea99ad398a73232578abaeb63ed460cd3a1b3c75d3c735ee69` |
| ROOT_ITEMS_R3A.md | root items, each with a recommendation | `26ce474cd75308286bc12f98707ddcd24765e30732c3cf1afa010f93b513ddb6` |
| NUMBER_PROVENANCE_R3A.json | the target-free source of every numeric token in the three texts | `e42ab9878401a2c8eac165dec8c924d02ee1d2b46160294ba84d36e3d2d2c217` |
| V005_ENTRY_TABLE_R3A.json | the hand-written V005 entry table, read at `2026-10-18T23:12:12Z` | `d69eed1379124f01e53f1da9eefeaa3e070c04f24cc4ebc7fcc6efe275d820be` |
| V006_ENTRY_TABLE_R3A.json | the hand-written V006 entry table, read at `2026-10-19T13:01:54Z` | `340effa9a790ae305355988bea234956cc2f7dfa88f82ac2dfe414987b2c6a76` |
| tools/check_target_free_c4v004.py | the target-free check | `955a4c048ef7bb23e555c32dc47984d587c03f0b47a369d574aeddb6a89d2cfb` |
| tools/test_check_target_free_c4v004.py | the mutation test | `1f1e5791b060676c0219411ddeaee5355caec44f37e4b7af12881fe60758bafd` |
| tools/make_miss_reading_c4v005.py | this generator | `eb907fc98f92e0dc1f5ad9f5638e4edbb762a9651ead56f897736d5a2f8970e6` |

**Draft inputs, for replay:**

| draft file | sha256 |
|---|---|
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/miss_reading_prereg_c4/r3a_work/text_c4/PREREG_MISS_READING_R3A.md` | `a32aed4d73f2eab66bd3c96135c9d8519a37c2242ba502185209af4b866537b6` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/miss_reading_prereg_c4/r3a_work/text_c4/CLAUSE_SOURCE_MAP_R3A.md` | `185bb7190714adea99ad398a73232578abaeb63ed460cd3a1b3c75d3c735ee69` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/miss_reading_prereg_c4/r3a_work/text_c4/ROOT_ITEMS_R3A.md` | `26ce474cd75308286bc12f98707ddcd24765e30732c3cf1afa010f93b513ddb6` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/miss_reading_prereg_c4/r3a_work/text_c4/NUMBER_PROVENANCE_R3A.json` | `e42ab9878401a2c8eac165dec8c924d02ee1d2b46160294ba84d36e3d2d2c217` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/miss_reading_prereg_c4/r3a_work/text_c4/V005_ENTRY_TABLE_R3A.json` | `d69eed1379124f01e53f1da9eefeaa3e070c04f24cc4ebc7fcc6efe275d820be` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/miss_reading_prereg_c4/r3a_work/text_c4/V006_ENTRY_TABLE_R3A.json` | `340effa9a790ae305355988bea234956cc2f7dfa88f82ac2dfe414987b2c6a76` |

**V005 at assembly:** `c01b3c51e34501d77e474594cc0b4be72c6e068c7f58a595055316313a8d4bb1`, from the byte copy `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/miss_reading_prereg_c4/r3a_work/final_c4/V005_COPY_c01b3c51.md`. The entry table covers its 60 headings; 22 are CITED_PINNED.

**V006 at assembly:** `0d93aa8b6c04f6a62cd5f135c34461b556e6ffd10c478f01bc56533099047386`, from the byte copy `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/miss_reading_prereg_c4/r3a_work/final_c4/V006_COPY_0d93aa8b.md`. The V006 entry table covers its 32 headings; 1 are CITED_PINNED. The seal entry, when root writes it, is the first V006 heading naming the rendered prereg's sha; it and later entries lie outside the table.

**Generator hook self-probe** (direct calls, no side effects): subprocess /bin/sh REFUSED; subprocess python without the tool REFUSED; write outside --out REFUSED; mkdir outside --out REFUSED; os.remove REFUSED; the check command ALLOWED.

**Results.** The check writes `TARGET_FREE_CHECK_R3A.json` and the mutation test `TARGET_FREE_MUTATION_TEST_R3A.json`. `HASHES_R3A.txt` gives the sha256 of every file. The generator exits 0 only when the target-free and currency verdicts both PASS and every mutation case and hook probe is caught. This INDEX is written before the checks, so that the check scans it.

**What the check establishes, and what it does not.** It is a mechanical check against fixed deny-lists and a listed-value inventory; it is not exhaustive and it is not a proof.
- **Checked from bytes:**
  - T1 to T3: no deny-listed term (also split by separators), data-file extension, unpinned NGC3198-named file, URL, HTML entity or comment, disallowed letter, velocity unit or target-symbol value (symbol then value, value then symbol, or a symbol column of a table) in the three texts, this INDEX, the provenance JSON or the two entry-table JSONs, and no unexpected file in the bundle;
  - T4: every number token of the three texts and of the JSON notes that survives the stated stripping rules is listed (digits grouped by underscores or thousands commas, leading-dot numbers and numbers before a prime or inside emphasis included), every listed value occurs, every category is in the closed list and passes its verification (radii and node values against bytes; quoted values located in pinned sources; labels shape-checked; post numbers against the exchange folders); the census lists every occurrence with its context;
  - T5: every sources row parses and every pinned source hashes as stated; the cited V005 entries are pinned by section sha, with allow-listed end-markers and a tail pin; a cited V006 entry must be pinned in the V006 table;
  - T6: every clause is mapped;
  - T7 (currency, not target-freeness): the V005 entry table covers the V005 bytes exactly, and nothing in V005 changed since it was read; the V006 entry table does the same for every V006 heading before this text's seal entry.
- **Not established by the script:** that no rule depends on a target value (a semantic property, which the lens reviews check), and that the shape-checked categories are right (review checks them against the cited sources).
- **No target was ever opened.** The check cannot compare against target values, and never needs to.
- **Stated limits of the check and its hook:**
  - os.stat, os.lstat, os.path.exists, os.path.isfile and os.path.realpath raise no audit event, so the hook cannot refuse a stat; the code tests every path against the deny-list before it stats or opens it, lexically first on the raw path (before any ".." is collapsed; NFKC- and case-folded, invisible marks removed, separators squashed; no filesystem call) and then by the realpath of every prefix, whose symlink resolution uses lstat and readlink (a link target is lstat-ed while it is resolved) but never opens the resolved path;
  - the hook sees Python-level events only: native code, descriptors opened before it was installed and an open relative to a dir_fd are outside its path test; the check starts no process;
  - the deny-list and the unit, symbol and identifier patterns are fixed lists; they are not exhaustive;
  - T4 checks token values, not each occurrence; the census lists every occurrence with its context for review;
  - categories come from a closed list; quoted values are located in pinned source bytes, which is a weak test for small integers; HEADING_OR_ITEM_NUMBER, INDEX and REVIEW_COUNT are shape-checked only; post numbers are checked against the exchange folders;
  - an identifier chain is skipped when it matches a registered shape, occurs in a pinned source or is declared in the provenance; a value glued into such a chain is not seen;
  - T4 does not value-check bare numbers in the provenance uses strings (they derive the listed values) or in INDEX (written by the generator from counts and shas); T1 to T3 still scan both for terms, units and symbol-value pairs;
  - number words below eleven, roman numerals, clock-shaped ratios, a middle dot between digits (read as multiplication, as in a square root times a number) and digit-for-letter spellings are not value-checked;
  - T5 judges a pinned source target-free by its path; content target-freeness rests on the source registration;
  - T7 compares against the V005 and V006 bytes it reads; a currency PASS is meaningful only against the live files or the frozen copies; V006 is found by its registered file name, and its seal entry by the prereg sha it names;
  - the check never opens target data, so it cannot compare the text with target values;
