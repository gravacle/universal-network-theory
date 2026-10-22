# STORAGE_AUDIT_C3V001: two-volume storage audit and forecast (root 0865, V006 A305)

From: Claude3 (deputy analysis). 2026-10-22T11:04:40Z (`date -u`). Sources only: configs and tool bytes, all pinned below. No run tree, volume content or NGC data was read. The free-space figures come from Codex3 0674 (`df`, 2026-10-21 11:43Z) and A305; root re-measures at plan time.

**Labels:** FORMAL (from source). The arithmetic was checked by script. Forecasts are UNTESTED estimates.

## 1. Every planned output root

| Output | Root (field, file:line) | Volume | Note |
|---|---|---|---|
| Campaign W1–Wn | work_dir `/Volumes/UNT_CAMPAIGN/DDO154_CAMPAIGN_V001`, logs `…/DDO154_CAMPAIGN_LOGS_V001` (A277) | **UNT_CAMPAIGN** | the only campaign; it cannot span or migrate (A256, 0674) |
| HEADLINE11 (and every step-4 direct batch) | `STEP4_OUTPUT_ROOT` (VARS `49607ea4` L15); guard014 `OUTPUT_VOLUME` hard-coded External1 (`6efdca01` L275) | External1 | the code fixes it; it cannot drift |
| L2 direct batch (7 calls) | `D = OUTPUT_ROOT/DDO154_JACOBIAN_R<row>_<key16>_A<n>`, 7 pre-created (A278, A280) | External1 | **They must stay mounted and unmoved for the whole campaign:** the campaign's cache references them, because the import is by reference |
| S1 pair (S8) | the pair guard's hard-coded `OUTPUT_VOLUME` (`1274a39a` L277) under the same OUTPUT_ROOT | External1 | |
| S0 runs | `S0_RUN_ROOT` (VARS L17) | External1 | |
| S0 kit launch records | `S0_LAUNCH_ROOT` (VARS L16) | **internal** | records only |
| Phase-1/2 NGC runs (P112 cw8 v003) | config `run_root` = `<run_volume>/NGC_*`, enforced (`4d5b47e7` L851) | **whatever `run_volume` says** | **ROOT FIELD: it must be `/Volumes/External1` (see §4)** |
| P112 launch root | config `p112_launch_root`, refused if under `/Volumes/` (L835) | **internal** | records and locks only, by design |
| CP-1 point runs (row 32, rows 501/504 adapt, W3 acceptance) | `--out-root` must be `claude_artifacts/s4rc1_c3/cp1_*` (runner `da08d725` L161; common `fcd63a73` L56) | **internal** | moving them needs a runner and common successor (pinned bytes): not proposed |
| Verdict-day working folder (chain, seal record, POSTSEAL_PS, envelopes, PRELAUNCH) | `R=$ART/h3_at_verdict_c2` (VARS L7) | internal | small: JSON and chain sources |
| Seal and classifier outputs; importer acceptance records | `claude_artifacts/...` (N1 0343) | internal | small: KB to MB |

**Nothing defaults onto UNT_CAMPAIGN except the campaign.**
- The only heavy non-campaign output whose volume is a root **field** is the P112 `run_volume`/`run_root` pair.
- On the internal disk, only CP-1 can be sizable. Its per-point size is not stated in the sources. The internal disk had 929 GB free (A305), so the watchdog's 600/300 GB alarms cover it.

## 2. Forecast

**UNT_CAMPAIGN (8 TB = 7450.58 GiB nominal; root uses the df at the mount):**
- **Formula:** `R(b) = max_k [ (Σ_{j<k} n_j)·b + n_k·80 + 20 ]` GiB, with H = Y = 0 because the campaign is the only occupant. The shape is storage_check's ASSUMED 120-call shape `[1,8,2,1,1,1,10,10,24,8,2,1,10,10,24,7]` (STORAGE_PLAN_ERRATUM L22).
- **b = 16.24 GiB/call:** R = **3385.77 GiB** (wave 15) = **45.4 %**; retained after all 120 calls = 1949.4 GiB.
- **b = 57.19 GiB/call:** R = **7042.47 GiB** (wave 16) = **94.5 %**, which is above the 85 % trigger; retained = 6862.8 GiB (92.1 %).
- **The b at which the forecast reaches a given fill:** 100 % at b* = **60.80 GiB/call** (binding wave 16); **85 % at b = 49.36 GiB/call** (wave 15).

**External1 (non-campaign; 2,877.48 GiB free at 0674):**
- HEADLINE11+S0×4, measured: 370.5 GiB. That is 24.70 GiB per NGC call over 15 calls, the per-call estimate used below.
- L2 direct batch, 7 × b: 113.7 to 400.3 GiB retained. The launch needs 7×80+20 = 580 GiB free (guard).
- S1 pair, 2 × b: 32.5 to 114.4 GiB retained. The launch needs 180 GiB free.
- SENS_LO, SENS_HI and DIII (22 NGC direct calls, DBP C2V004D `5d3f4bb8`): about 543.5 GiB at 24.70 GiB/call. Their output-cap ceiling is 1824 GiB.
- **Subtotal:** 1060.2 GiB (low b) to 1428.7 GiB (high b). External1 has **1817.3 to 1448.8 GiB left for the Phase-1/2 P112 roster**: about 73 to 58 NGC calls at 24.70 GiB, or 22 to 18 at the 80 GiB cap.
- **Ceiling:** the DBP output caps alone total 2864 GiB, about External1's whole free space. Every direct batch running to its cap would fill it. The watchdog's 300 GB loud alarm is the backstop.
- **Not in the sources:** the P112 roster size (the Phase-1 PLAN, u_A chain G-20) and rerun counts. Root compares them with the remaining figure above at u_A.

## 3. The commands after W1 acceptance (A192 item 5; storage_check `8eee1f68`, usage L23)

The tool tests `R(b) + other <= total_free` over ONE pooled figure (L18). The campaign cannot use External1, so the **binding** check is the per-volume one (a). The combined form (b), which 0865 asks for, is necessary but not sufficient.
```bash
ST="$ART/h3_campaign_path_c2/storage_check_h3_c2v003.py"; WD=/Volumes/UNT_CAMPAIGN/DDO154_CAMPAIGN_V001
SHAPE=1,8,2,1,1,1,10,10,24,8,2,1,10,10,24,7
F_CAMP=<UNT_CAMPAIGN free bytes from root's df at the mount, before W1>   # or: current df free + W1 call-dir bytes
F_E1=<External1 free bytes, df at the same time>; H_E1=<remaining planned non-campaign bytes on External1, §2>
# (a) BINDING: the campaign volume alone
"$PY" -I -B "$ST" wave --work-dir "$WD" --next-calls <n_W2> --threshold-total-free-bytes "$F_CAMP" --threshold-other-program-bytes 0 --threshold-waves "$SHAPE" --out <NEW>/STORAGE_W1_CAMPAIGN.json
# (b) COMBINED, as 0865 asks: both volumes pooled
"$PY" -I -B "$ST" wave --work-dir "$WD" --next-calls <n_W2> --threshold-total-free-bytes $((F_CAMP + F_E1)) --threshold-other-program-bytes "$H_E1" --threshold-waves "$SHAPE" --out <NEW>/STORAGE_W1_COMBINED.json
# (c) External1 on its own: H_E1 + 300 GiB alarm margin <= F_E1
```
- Exit 0: the next wave fits. Exit 5: HALTED_DISK.
- The JSON `threshold` block gives `b_star_GiB`, the binding wave and `fits`. b is measured by the tool from W1's call dir after acceptance (L8), as A192 item 5 requires.

## 4. Early warning, and the root checklist item

**Rule (A305):** at W1 acceptance, root reads b from (a).
- If **b > 49.4 GiB/call** (85 % on nominal 8 TB; recompute with the real F_CAMP), or (a) reports `fits: false`, root decides at once. It does not wait for the disk to fill.
- The options are root's, for example a larger campaign volume before W2 or a smaller program. A file move does not work: the campaign is bound to its volume and work-dir identity.

**Checklist item S-1 (root adopts it):**
1. **P112 cw8 config at u_A:** set `run_volume = "/Volumes/External1"` and `run_root = "/Volumes/External1/NGC_<PHASE>_V001"` (the launcher enforces the layout at L851). `p112_launch_root` stays internal (L835).
2. **Keep External1 mounted** from the L2 direct batch until the campaign ends. The imported D folders stay referenced by the campaign cache.
3. **At W1 acceptance,** run (a), (b) and (c) above, and apply the 85 %% rule.
4. **At u_A,** compare the P112 roster forecast (roster × about 24.7 GiB, or × 80 at the cap) with External1's free space minus 300 GiB.
5. **No code change is proposed.** CP-1 stays internal by design, watched by the internal-disk alarm.

**Pins:** VARS `49607ea4`, guard014 `6efdca01`, S1-pair guard `1274a39a`, cw8 v003 `4d5b47e7`, CP-1 runner `da08d725`, common `fcd63a73`, storage_check `8eee1f68`, DBP C2V004D `5d3f4bb8`, Codex3 LANE_A `b393ddba`.
