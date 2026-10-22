# Storage plan erratum to README_H3_CAMPAIGN_PATH_C2V001 §6 (V006 A191 B1)

Claude2 for root. Stamp (`date -u` before writing): Tue Oct 20 02:19:32 UTC 2026 (Mon 21:19 CDT). Nothing was moved, deleted or launched. The only disk reads were `df -k` on the two mount points. No run tree was listed. Labels: TESTED (measured or ran), FORMAL (arithmetic from cited numbers), UNTESTED (forecast).

**It supersedes** README §6 (`6d2b4ee2`) Plan items 1-2: the 48 GiB figure, the 600 GiB move and the "about 300 GiB" left on the internal disk. It replaces the wave-15-only arithmetic of §6 Facts bullets 4-5 with the binding condition over all waves. §6 Constraints and Plan items 3-4 stand, with the threshold in §4 below.

## 1. What was wrong

README §6 took HEADLINE11 + S0 ×4 as about 48 GiB. The run sheet's own forecast evidence (`W1_DISK_FORECAST_WITH_HEADLINE11_S0x4.json`, `eed9e834`) carries 397,867,631,966 B, which is **370.5 GiB**. Its 878.8 GiB shortfall already used that figure: 878.8 − 508.3 = 370.5. The run sheet's table label "51.5 GB" is the same slip.

With 370.5 GiB, Plan item 2 ("move at least 600 GiB to the internal disk") no longer fits. The internal disk would need 600 + 370.5 = 970.5 GiB, and it has 953.0 GiB free. The "about 300 GiB left" in that item is wrong.

## 2. Inputs

| input | value | source |
|---|---|---|
| External1 | 3,725.8 GiB size, 847.9 GiB used, **2,877.5 GiB free** | `df -k /Volumes/External1`, 02:19:12Z (TESTED) |
| Internal disk (`/System/Volumes/Data`) | 1,858.1 GiB size, 881.4 GiB used, **953.0 GiB free** | `df -k`, 02:19:12Z (TESTED) |
| b, measured | 17,442,511,906 B = **16.24 GiB** per call (C5c, largest receipt) | run sheet §3 |
| b, high case | **57.19 GiB** per call (16.24 + 26 × 1.575, 32 iterations) | run sheet L214 |
| HEADLINE11 + S0 ×4 | **370.5 GiB** | forecast evidence `eed9e834`; A191 |
| waves n_k | `[1,8,2,1,1,1,10,10,24,8,2,1,10,10,24,7]`, 120 calls (ENGINE_SHAPED, ASSUMED shape) | `storage_check_h3_c2v001` L36 |
| guard, reserve | 80 GiB per call, 20 GiB | A147 L3-01; parent L3503-3506 |

## 3. The binding condition

The parent admits wave k only if the work dir's volume has n_k × 80 + 20 GiB free. The campaign's earlier waves stay on that volume, because the work dir cannot move (§6 Constraints). So the campaign volume must hold, for every k:

  need_k = (Σ_{j<k} n_j)·b + n_k·80 GiB + 20 GiB, and the requirement is R = max_k need_k.

| wave k | n_k | calls before | need_k at b = 16.24 (GiB) | need_k at b = 57.19 (GiB) |
|---|---|---|---|---|
| 1 | 1 | 0 | 100.0 | 100.0 |
| 2 | 8 | 1 | 676.2 | 717.2 |
| 7 | 10 | 14 | 1,047.4 | 1,620.7 |
| 8 | 10 | 24 | 1,209.9 | 2,192.7 |
| 9 | 24 | 34 | 2,492.3 | 3,884.6 |
| 13 | 10 | 69 | 1,940.9 | 4,766.4 |
| 14 | 10 | 79 | 2,103.3 | 5,338.4 |
| **15** | 24 | 89 | **3,385.8** | 7,030.3 |
| **16** | 7 | 113 | 2,415.6 | **7,043.0** |

(Waves 3-6 and 10-12 are lower and are left out.) So **R = 3,385.8 GiB at b = 16.24, binding at wave 15**, and **R = 7,043.0 GiB at b = 57.19, binding at wave 16** (FORMAL).

## 4. Do both volumes together hold the program (A147)?

The program here is the campaign plus HEADLINE11 + S0 ×4. The NGC step-5 outputs are not counted, because the permitted reads give no size for them; each GiB of them comes out of the spare below.

**b = 16.24 GiB (measured): yes, with 74.1 GiB to spare across both volumes, and only one way.** (FORMAL; UNTESTED until W1 measures b)
- HEADLINE11 + S0 ×4 must go to the internal disk. On External1 they would need 878.8 GiB moved off it. External1 holds only 847.9 GiB of other data, so it would be 30.9 GiB short even with everything moved.
- Before wave 15, between **508.3 and 582.4 GiB** of External1's other data must move to the internal disk by verified move. 508.3 is R − 2,877.5. 582.4 is 953.0 − 370.5.
- That leaves 74.1 GiB free on the internal disk, which is the system disk. Any working margin root keeps there, any NGC output and any other lane's runs come out of those 74.1 GiB.
- Whether 508.3 GiB of External1's other data is movable is UNTESTED. `storage_check_h3_c2v001 move` decides it per directory.
- **Additional storage needed: 0 GiB** on these conditions. With a working margin of X GiB on the internal disk, or Y GiB of NGC and other outputs, it is max(0, X + Y − 74.1) GiB.

**b = 57.19 GiB (high case): no.** (FORMAL)
- R = 7,043.0 GiB, and External1 is 3,725.8 GiB in all. No amount moved makes the campaign fit there: it is 3,317.6 GiB short, counting free space plus all 847.9 GiB of other data.
- Even with only the campaign on External1, it halts at wave 9, short 1,007.1 GiB. Moving all other data still leaves wave 9 short by 159.2 GiB.
- Across both volumes the shortfall is **3,583.1 GiB**: R + 370.5 − (2,877.5 + 953.0).
- The work dir cannot span volumes, because the parent reads free space at the work dir. So the additional storage needed is **one campaign volume with at least 7,043.0 GiB free**, for example an 8 TB drive at 7,450.6 GiB nominal. HEADLINE11, S0 and the moved data then fit on External1 and the internal disk.

**Threshold (FORMAL):**
- Both volumes together hold the program only if **b ≤ 17.08 GiB per call**. That is 5% above the measured 16.24, at zero internal margin, binding at wave 15.
- External1 alone, with all other data moved off it, would allow up to 20.06 GiB per call. But the internal disk cannot take 847.9 + 370.5 GiB, so 17.08 binds.

## 5. Plan, corrected

1. HEADLINE11, S0 and NGC outputs go to the internal disk (370.5 GiB plus NGC). This amends A140 N3, which put NGC outputs on External1, so it needs a root ruling (unchanged from §6).
2. Before wave 15, move 508.3 to 582.4 GiB of non-pinned other data from External1 to the internal disk by verified move. Recompute both ends of that range with W1's measured b.
3. Run the `wave` check before every relaunch (unchanged).
4. **Decision at W1.** W1's `final_output_bytes` gives b (UNTESTED). If b > 17.08 GiB, the two volumes cannot hold the program, and A147 requires root to alert the principal before W1 + 2 days. The fix is then a campaign volume with at least R(b) free; R(57.19) = 7,043.0 GiB.
   - Because the work dir cannot move, a new volume means a new work dir and cache, so W1 reruns (§6 item 4).
   - If b ≤ 17.08 GiB, steps 1 and 2 suffice. The spare is 74.1 GiB at b = 16.24, and it shrinks by 89 GiB for each 1 GiB rise in b.
