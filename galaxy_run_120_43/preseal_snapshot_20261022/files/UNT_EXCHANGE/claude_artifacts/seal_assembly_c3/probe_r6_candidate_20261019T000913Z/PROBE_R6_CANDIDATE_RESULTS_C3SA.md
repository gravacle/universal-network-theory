# PROBE: helper c3v013 on the prereg r6 CANDIDATE (Claude3, 0644)

Written 2026-10-19T00:12:21Z (`date -u`). The object is the r6 candidate `v007_final_prereg_c4/r6/KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R6.json`, `d28c95f56321f566b444c3e0bfbbe0ecdac564cbc03a8583ecd5f8d0ae40c0a9` (Claude4 0111). **It is a candidate, not SELECTED, and nothing in the selected tuple pins it.** The probe ran helper `seal_steps_c3sa_c3v013.py` (`ad581a06…`) through its CLI on labelled probe fixtures in this folder. Nothing was written outside it.

| # | step | result |
|---|---|---|
| 1 | `check-tor`: r6 named by a probe SELECTED fixture with an exact `{path, sha256}` pair | PASS: r6 is UNSEALED, and its `seal_slots` keys equal the helper's |
| 2 | the bytes r6's entry table was read from (`entries_after_A81.addendum_read`) | `byte_copy` is an **ABSOLUTE** path inside r6's folder (`r6/addendum_read/V005_ADDENDUM_READ_AT_R6_GENERATION.md`, `c01b3c51`, 143,081 bytes). r5's was relative. |
| 3, 4 | dispositions and rehash, first try | REFUSE `PATH_SPELLING_REFUSED`. This was **my probe's own error**: it joined the absolute path onto the folder. The helper behaved correctly. |
| 3b | dispositions with the empty v003 object `{schema, frozen_addendum_sha256: c01b3c51…, entries: []}` | PASS: later entries [] and changed cited entries []. The empty path works on r6. |
| 4b | rehash-entries | PASS: changed table rows [] |
| 5 | sealed-prereg: r6 plus dry run 11's final slots | PASS (`892f2ea1…`): r6's slot keys are compatible with the slot draft |
| 6 | `check-tor` with that sealed prereg | PASS: byte-equal to r6 plus the slot values |

**Finding, fixed in script c3v013:**
- Script c3v012's `tor_table_bytes` refused any absolute `byte_copy`, so wiring r6 would have refused at step 0.
- c3v013 accepts an absolute `byte_copy` only inside the text of record's own folder, plus the relative r5 form.
- It refuses an empty value, `..`, and an absolute path outside the folder.
- Controls `tor_table_bytes_test_20261019T001039Z/` (`137b9a28…`): 6/6 PASS. They run the function text extracted from the script, with r5, the r6 candidate and four bad forms.

| file | sha256 |
|---|---|
| R6_CANDIDATE_PROBE_SELECTED_FIXTURE.json (labelled probe fixture) | 609e2c0db3cc3e790d12d61a8d155d11e16682a943bad5dda8da8a847d3d5b9d |
| PROBE_V005_ADDENDUM_FROZEN.md (helper freeze of the final V005) | c01b3c51e34501d77e474594cc0b4be72c6e068c7f58a595055316313a8d4bb1 |
| DISPOSITIONS_EMPTY_PROBE.json | e187a73977a66304b455a407d4cf46d0abadc8facc62bd824e25bb487042a932 |
| PROBE_SEALED_R6.json | 892f2ea12c291fb5bb6c7a1f3af27830fe7385498e7f86d9fc37f2096d3dd884 |
