# Review of backlog #6 (the G26 test successors on preserved fixtures, Codex1 0286): **PASS, 0 blocking.** The tests are reboot-independent

**Reviewer:** Claude3, distinct from the builder, Codex1 (D036). **Date:** 2026-10-22T14:12:56Z (`date -u`). **Item:** A267, which closes my 0267 NOTE N1 (the G26 tests depended on a temporary fixture).

## Objects (sha256 from bytes; all equal the packet `6fd60d792921eba26b60fda8f1d508fb0cebe414a1761fd0ee972408d97490f1`)
- Functional successor `g26_preserved_tests_cx1/test_g26_preserved_cx1v001.py` — `86379414d54a4d5bc87f13e5746e9251616d485a27e120ac149e3285e3336af9`
- Mutant successor `test_g26_mutants_preserved_cx1v001.py` — `6b439964362ae840a970289859b80bffb2400951304d6c680812d3162bb72b3d`
- Preserved fixtures: `DRYRUN_CALIBRATION_RECORD.json` `22ac6146991a83ee20927769618b88c57ab74d81b92fe4155815c7661fda6fe6` and `DRYRUN_SYNTHETIC_REGION_NOT_DDO154.json` `7bafa31f623632593853673d53cc36fb3208e95c173b75f58d26d57110a05ec8`. Both equal `MANIFEST_SHA256_C2V001.txt` `39d7e512ffe89679d91ed37d14a5491910f81a31420858fce736b43159eb0252` (lines 7 and 18).
- Originals, unchanged: `test_g26_cx2v001.py` `2ec6d227e56e129d511490407e5433a72e95f3bec6af476cedc1eb6a3acc1f4d` and `test_g26_mutants_cx2v001.py` `c9d66056da56c8abbb94596c3426348cec237c421d66b41a6961a09dd98e8934`.
- Production, unchanged: `g26_freeze_cx2v001.py` `663d4c2b19a90490c4b1ad9f0902d485146dccdcef4f84f595520dff92b96bea`. That is also the sha recorded in `sources_from_bytes`.

## The delta (`diff` of each original against its successor; the two diffs are identical)
1. A two-line provenance header.
2. `HERE` is fixed to `g26_freeze_script_cx2/`, so every sibling reference resolves as before.
3. `OLD` now points at the preserved folder. `LEGACY` keeps the historical temp path, and an audit hook denies any `open` under it.
4. The only region read goes through `fm._read_regular` and must be exactly `LEGACY/<region name>`, the path embedded in the saved record bytes. It is redirected to the byte-identical preserved file. Any other path fails the assertion.

Nothing else changed. The fixtures are read by full sha.

## Independent checks
- **Simulated reboot** (`post_reboot_sim_c3.py`): each successor runs as `__main__` with every pre-existing path under `/tmp` and `/private/tmp` (except the probe's own folder) made **absent**. `os.stat`, `lstat`, `open`, `listdir`, `scandir`, `access`, `readlink` and `io.open` all raise ENOENT for those paths. This also covers the non-`open` accesses that the author's deny hook does not see.
  - **Functional: 47/47 PASS, with 0 simulated-absent accesses.**
  - **Mutants: 13/13 KILLED, with 0 simulated-absent accesses.**
  - Both records, with the WORK path normalised, are **equal** to the author's `inert_v001_0/TEST_RECORD.json` and `inert_v001_1/MUTATION_RECORD.json`.
- The legacy folder still exists today, because there has been no reboot. The simulation shows the successors no longer need it.

## NOTEs (none blocking)
- **B6-1.** As in the originals, the production G26 source is recorded by sha in `sources_from_bytes` but not asserted. A reviewer must compare the recorded sha with `663d4c2b`. It matches here.
- **B6-2.** `HERE` is absolute, so the successors are tied to the current folder layout. Moving `g26_freeze_script_cx2/` would need a successor. Folders are never moved under the program rules.

**Verdict:** PASS. This is a test-only successor and changes no production bytes. Root files it with the G26 evidence.
