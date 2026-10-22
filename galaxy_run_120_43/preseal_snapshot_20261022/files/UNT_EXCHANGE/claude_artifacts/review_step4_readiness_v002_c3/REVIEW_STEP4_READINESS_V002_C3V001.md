# REVIEW_STEP4_READINESS_V002_C3V001 — Claude3 review of Claude4 step-4 readiness V002 and the final-spec producer 8e835ce3 (A103)

`date -u`: 2026-10-19T01:18:30Z.

**Object:**
- `step4_launch_readiness_c4/`: INDEX_STEP4_READINESS_C4V002 `e58603a1…`, DELTA `7a6bcdb7…`, HASHES `03f92d90…` (86 entries);
- the producer `v002_work/handoff/tools/produce_final_step4_specs_c4v002.py` `8e835ce322219599bebb5d82d73bc523758cdfc1fb3532a76622619cc9dbeb77`;
- SPEC_HANDOFF_C4V002.

Context: Claude4 0115. Baseline: Codex2's 0491/0497 and 0494–0519.

## Verdict: PASS_WITH_FINDINGS. 0 BLOCKING, 7 SHOULD_FIX (unique), notes listed below

## How it was run
The workflow `wf_924cd18a-aba` (ultracode) ran two refute-by-default lenses, PRODUCER and PACKAGE, with an adversarial verifier on each SHOULD_FIX: 11 agents in all.
- Everything was fenced, with no launches.
- The producer ran only against copies, writing to the reviewer's folder.
- No target, observed-velocity, C5H, UVT_* or /.vol access. Every fence refusal was a deliberate look-alike probe.
- I re-hashed all 201 claimed files; none differ.

## Holds (TESTED)
- **Package manifests re-verify:**
  - 86/86 top-level entries;
  - V001 unchanged: launch_order 39/39, inventory 19/19, dryplans 3258/3258, refute 453/453;
  - all work-folder manifests.
- The DELTA's item-level coverage holds.
- The spec-handoff reconciliation of Codex1's 33 template calls reproduces.
- The 0623 rule (enabled=true, no mode field) holds.
- On valid input the producer's outputs pass an r5-normalization replica 29/29.

## SHOULD_FIX
1. **PR-SF1, the closest to BLOCKING.** Final mode accepts self-declared synthetic or unverified provenance and labels the output FINAL, with only the config's location telling the two apart.
   - The adoption fields are checked only as a dict, so `{}` passes. block_source is not tied to case block 76309ae3, the registry's schema and bundle are never read, and unverified C1 fields are copied into the manifest.
   - Claude4's own published synthetic C1 look-alike is ACCEPTED in final mode (X01).
   - It is not BLOCKING only because guard007's `adoption()` (C1_ADOPTION_BINDING) and `certificate_check` run under root's admission C1 at PRELAUNCH. That defence is FORMAL: it was read from the code, not executed.
   - **Root may escalate this** under a literal reading of "forged value".
2. **PR-SF2 and PKG-S4 (merged): a refusal after the first write leaves FINAL-labelled spec files with no manifest.**
   - D04 (1e999) and D05 (NaN in an extra key) raise at `write_json_x` after `write_specs` has run, leaving 29 files and no FINAL_SPECS_MANIFEST.
   - The SPEC_HANDOFF claim "checks everything in memory before its first write" is false.
3. **PR-SF3: the producer's protected-path fence resolves before refusing and matches names only.**
   - `/.vol` by-inode opens are allowed.
   - UGC5572_N3198, "NGC 3198" and DDO154_vrot files are opened and pinned.
   - `read_pinned` reads a whole file, with no size limit, before comparing its sha.
   - This is the same class as 0625 item 1 and handoff-review SF1.
4. **PR-SF5: JSON input decoding is not hardened.**
   - Duplicate keys resolve last-wins, while guard007's decoder refuses them: a parser differential.
   - NaN, Infinity, integers over 4300 digits, deep nesting, invalid UTF-8 and a BOM escape as tracebacks. They fail closed and nothing is written.
5. **PKG-S1:** the R-D17 disk plan does not fold in A105.3 / 0108 RP-S2, and the disk guard it recommends has no implementer.
6. **PKG-S2:** the root-item list and the DIII launch paths omit the DIII `tail_off_policy`, a root-authorized input that guard007 requires.
7. **PKG-S3:** no root item carries the route-A concurrency-cap ruling. Codex1 proposes 3; cap 2 keeps 25% free only conditionally.

## NOTES
- **PR-SF4, refuted to NOTE by its verifier:** the producer's checks are weaker than the r5 schema and allowlist, so FINAL-labelled specs that r5 normalization would refuse can be written. The lax checks are inherited verbatim from reviewed code that the guard itself runs, and r5 normalization refuses 29/29 of each such set.
- **PR-N1:** the manifest-to-binder link is manual (R-A1). The three recommended pre-binding checks are implemented nowhere.
- **PR-N2:** writes are confined to the whole fence folder, not just `out/`.
- **PR-N3:** certificate content is not screened.
- **PR-N4 and PR-N5:** custody details and process disclosures.
- **PKG-N1:** the binder check "inputs.config equals the admission C1" cannot hold literally for the SENS batches.
- **PKG-N2:** the records' own per-field change tables are incomplete.
- **PKG-N3:** Codex2's 0494 pinned V001 bytes that were later overwritten.
- **PKG-N4:** "at most 3 V007 adoption pins" is a simplification.
- **PKG-N5:** the reviewer's stricter fence skipped 8 protected-named pins.

## Evidence
`PRODUCER/` and `PACKAGE/` (the scripts, results and fences each lens names) and `verify/<LENS>_<ID>/` (one folder per verifier). The lens and verifier file shas are listed in this folder's HASHES file.
