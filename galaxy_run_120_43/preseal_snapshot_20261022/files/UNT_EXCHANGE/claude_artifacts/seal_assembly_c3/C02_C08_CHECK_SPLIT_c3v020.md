# C-02 to C-08: what ROOT_SEAL_STEPS_c3v020.sh checks (for root's R-05 ruling) (Claude3)

Written 2026-10-19T02:58:46Z (`date -u`).
- **Script:** `ROOT_SEAL_STEPS_c3v020.sh` `36058df84bb2088970be442bc64445a4c6939b45df3e9cb3294cedef62c65ac0`.
- **Helper:** `tools/seal_steps_c3sa_c3v019.py` `91b15dc6…`.
- **Why this table exists.** basis.for_root R-05 of `SELECTED_SEAL_TOOLS_V004_C4V001` (`593c59fa`) cites r6 `seal_record_requirements[13]` (A106.2): the seal record states which of C-02 to C-08 the seal script checked and which root checked by hand.
- **Scope.** This is a factual reading of the script's bytes and of dry run `dry_run_20261019T025053Z` (both passes).
- **Not edited:** no disclosures file. Root's V002 (`a0284ece…`, A112) carries the row `A106_2_SRR13_CHECK_SPLIT`. The last column compares this table with that row.

| item | r6 srr[13] wording | c3v020 | step : line (helper subcommand → log) | dry run A / B | V002 row says |
|---|---|---|---|---|---|
| C-02 | the text-of-record pin equals r6's stored sha | **checked by c3v020** | step 0 : L370 (`check-tor`, verdict on stderr); step 4a : L590 (`check-tor` + the sealed prereg → `STEP_04A_C02.json`); step 10 : L656 (same → `STEP_10_C02.json`) | PASS / PASS | script ✓ |
| C-03 | B6 provenance | **checked by c3v020** | **step 8** : L622 (`gates-provenance` → `STEP_08_C03.json`) | PASS / PASS | script ✓ |
| C-04 | the slot records load through r13's own load_producer_registry against V009; every slot passes (A107 excludes EPS_NGC, I1T_NGC) | **checked by c3v020** | step 3b : L559 (`slot-registry` → `STEP_03B_C04.json`) | PASS / PASS | script ✓ |
| C-05 | launcher and guard match BUILD_V007 by exact name and sha | **checked by c3v020** | step 3 : L534 (`bound-check`, its c05 part → `STEP_03_C05_C06.json`) | PASS / PASS | script ✓ |
| C-06 | the whole bound command byte-compared with the binder's output | **checked by c3v020** | step 3 : L534 (`bound-check`, its c06 part → `STEP_03_C05_C06.json`) | PASS / PASS | script ✓ |
| C-07 | the generic covered-later sentence (D-05) | **not checked by script** | D-05 lives in the seal tools: v004 tools 1, 3 and 4 refuse the removed covered-later flag. The script only passes the dispositions object, and at step 2 : L469 (`dispositions` → `STEP_02_DISPOSITIONS.json`) it checks that object's rows. That is related, but it is not the C-07 check. | n/a (step 2 PASS / PASS) | D-05, enforced by seal tools v004 ✓ |
| C-08 | NEW-item ids against the IMPL | **not checked by script** | Root's manual check, recorded in V002's `c08_table` (19 rows) and `c08_confirmation`. Step 0 : L382 (`check-disclosures`) checks only that the file is well formed. Step 11 : L677 (`check-seal-record-disclosures`, R-02) checks that the SEAL_RECORD carries the file verbatim. Neither checks C-08's content. | n/a (steps 0 and 11 PASS / PASS) | by hand by root ✓ |

**Result.** The row `A106_2_SRR13_CHECK_SPLIT` in V002 ("C-02, C-03, C-04, C-05 and C-06 were checked by the seal script …; C-07 is D-05, enforced by seal tools v004; C-08 was checked by hand by root") **agrees with this table** on every item.

Line numbers are those of the c3v020 bytes above. The step functions start at: step 0 L342, step 2 L465, step 3 L505, step 3b L555, step 4a L584, step 8 L608, step 10 L645, step 11 L669.
