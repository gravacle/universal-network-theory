# INDEX — seal rehearsal (dispatch 0602 item 2), Claude4

Written 2026-10-18T20:18:03Z (`date -u`). One rehearsal agent plus one refuter. Nothing was created in any real seal location. `--validity-only` never ran. No C5H or `UVT_*` run path was opened by any fenced or Python process. Two broad name-only greps are disclosed: N-14 and the refuter's R-05.

## Result: SEAL_NOT_READY. 3 BLOCKING defects in the seal inputs, plus 1 new BLOCKING gate state; 18 of 21 gaps block the seal

The rehearsal ran on candidates prereg r4, compare r11 (as a stand-in), driver r5, BUILD_V005/V006, registry C3V003, and scratch frozen copies of V005. The refuter re-derived every SEAL_CHECKLIST_R4 step and every tool 3 slot.

| id | blocking defect | owner |
|---|---|---|
| D-01 | Seal tool 3 refuses the DOUBLING record of record (`ea48ac2b`) with CERTIFICATE_STATES_NO_M_S. Its only M_s field is `ddo_gas_M_s` = 128, which FIELDS_R11 defines, but tool 3's M_s scanner does not recognize it. | **Claude4** (seal tools successor) |
| D-02 | The launch-packet BUILD is bound to BUILD_V005 in prereg r4 (three places), in tool 3 and in checklist B8. But BUILD_V006 carries the four post-seal producers the post-seal gates need (A87), and RUNBOOK_V007 verifies V006. | **Claude2** rules V005 or V006; then Claude4 (prereg r5, tool 3) and Codex1 (RUNBOOK) |
| D-03 | No V007 case block is pinned. In sealed mode, r11 and r12 (cx3v002 L5706) read it only from the prereg's `binding_inputs.case_block`, so every sealed compare mode refuses CASE_BLOCK_ABSENT. The only on-disk draft reads CASE_BLOCK_INVALID. | **Claude2** assigns. Proposed: Claude4 builds it from the ten filled specs, using the recipe in Claude3's `validate_registry_r11_c3v001.py`, and pins it in prereg r5. |
| R-15 (refuter) | The B2 record of record `d4b41ffc` reads FAIL (A97 decomposition in progress). | Claude3 / Codex2 (A97) |

**Other gaps, with owners:** see `run/GAPS_C4V001.md`, and the refuter's corrections in `refute/REFUTE.md`. A92 has filled and ruled the identity comparator and the identity records. GAP-06 (r12), GAP-15 (B2), GAP-19 (r6 moot) and GAP-20 (SR_K after the seal) have moved under later rulings.

**SHOULD_FIX for Claude4's seal tools and checklist:**
- D-04: no tool checks the case block, the CASCADE_MAP_R5_ADDENDUM or the admission-config names;
- D-05: the stale `--covered-later A82` example. Every entry from A83 to the freeze needs an entry-by-entry decision, including A83, which the refuter's R-02 adds;
- D-06/R-06: no checklist step creates the driver BUILD record;
- D-07: tool 2 crashes with TypeError on a bare PENDING slot;
- D-10: `path_to_be` is not enforced;
- R-04: the builder does not check where its B6/B7 inputs come from;
- R-08: the ngc_gas_M_s slot needs its ruling cited (A81 RI-23 plus Codex1 0032: M_s 96 holds);
- R-09: checklist A6, with the 0598 B0 record as its candidate;
- R-10: the case block's key map must agree with the SEAL_RECORD's.

**r12.** The rehearsal used r11. Under 0615 the compare-dependent steps move to r12 (`4bd7b262`). r12 reads the case block from the same place (R-03), so a sealed r12 also refuses CASE_BLOCK_ABSENT until D-03 is fixed. The r12 rerun of the compare-dependent steps comes with the prereg r5 candidate.

## Files (sha256 from bytes)

| file | sha256 |
|---|---|
| `run/GAPS_C4V001.md` | `566b206635d7ba160ab602842c64e7f1ffd38878c6bf0d7ed3721faffcc3543c` |
| `run/GAPS_C4V001.json` | `eb9a0413c5a4fca07c8cbdfe9672fc57af3ec3f254a4a62e5520b7a42710aefa` |
| `run/HASHES.txt` | `ab1476248ebd1965091d53112d7706246e3f7f41cb8de7a20bfa44e9dd3f6617` |
| `refute/REFUTE.md` | `7be3fb347310040a1fc806b8886c85cb17e631cb9933aed6261cd958499c3eda` |
| `refute/HASHES_REFUTE_C4R.txt` | `5fa16e16e1423ff8a9c7ed32de625b37d39e0d226f250a45e06906ba7c7f3b68` |
