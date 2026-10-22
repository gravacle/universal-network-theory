# S0 run root: the proposed path, checked (s0_launch_kit_c2 C2V003)

**Who and what.** A Claude2 root-workflow lane checked this at Mon Oct 19 17:58:16 UTC 2026 for root. It is a report only. Nothing was created, listed or written on /Volumes/External1: the checks are an lstat of each named ancestor and the volume's free space (`df` / `disk_usage`).

## Bottom line

- **The proposed run root `/Volumes/External1/Research/UNT_STEP5_RUNS/S0_PHASE1_V001`:** no symlinked ancestor (yes); no `ngc3198` or `uvt_` component (yes); free space 2877.48 GiB against the 564 GiB needed, 4 x 136 GiB + 20 GiB (yes). Its parent `/Volumes/External1/Research/UNT_STEP5_RUNS` is **absent**; the grandparent `/Volumes/External1/Research` exists.
- **The C2V002 launch kit refuses it, twice (FORMAL from `s0_kit_c2v002.py` `0ba823f3` L309-312, evaluated here on the string, TESTED).** The run root must sit exactly one level under `/Volumes/External1`, and its name must match `^NGC_[A-Za-z0-9_.-]+$`. The first refusal is `RUN_ROOT_NOT_ONE_LEVEL_UNDER_/Volumes/External1`; the second would be `RUN_ROOT_NAME_MUST_START_NGC_`. The launch script's usage line says the same (`--run-root /Volumes/External1/NGC_<NAME>`, `launch_s0_serial_root_c2v002.sh` `d2b7a37b` L8).
- **The same root in the kit's form, `/Volumes/External1/NGC_S0_PHASE1_V001`, passes every check, the kit's included.** It is absent, its parent is the mounted volume, and no ancestor is a symlink. Using the deeper spelling would need a kit successor; this lane recommends the kit's form.
- **Root does not create it.** root_monitor creates the receipt's parent at launch (`root_monitor_c2v001.py` `ba031c23` L135, `receipt.parent.mkdir(parents=True, exist_ok=True)`), and the kit's `ext1-check` accepts an absent run root (L867).

## Checks (TESTED at 2026-10-19T17:58:16Z)

| Check | `/Volumes/External1/Research/UNT_STEP5_RUNS/S0_PHASE1_V001` | `/Volumes/External1/NGC_S0_PHASE1_V001` |
|---|---|---|
| Absolute and normal | yes | yes |
| Ancestors (lstat) | `/Volumes`: exists, directory, realpath equal<br>`/Volumes/External1`: exists, directory, realpath equal<br>`/Volumes/External1/Research`: exists, directory, realpath equal<br>`/Volumes/External1/Research/UNT_STEP5_RUNS`: absent<br>`/Volumes/External1/Research/UNT_STEP5_RUNS/S0_PHASE1_V001`: absent | `/Volumes`: exists, directory, realpath equal<br>`/Volumes/External1`: exists, directory, realpath equal<br>`/Volumes/External1/NGC_S0_PHASE1_V001`: absent |
| No symlinked ancestor | yes | yes |
| No `ngc3198` component | yes | yes |
| No `uvt_` component | yes | yes |
| Kit `path_rules` (runs_ext, uvt_, UNT_INTERNAL_RUNS, C5H marker) | PASS | PASS |
| Parent exists | no (/Volumes/External1/Research/UNT_STEP5_RUNS absent) | yes |
| One level under `/Volumes/External1` (kit L309) | NO | yes |
| Name `NGC_*` (kit L312) | NO | yes |
| Kit admits it | **NO: RUN_ROOT_NOT_ONE_LEVEL_UNDER_/Volumes/External1** | **yes** |

## Disk (TESTED; External1 mounted: yes)

| Quantity | Value |
|---|---|
| Free | 3089670524928 bytes = 2877.48 GiB (of 3725.83 GiB) |
| Needed for the four S0 serial outputs at the cap | 4 x 136 GiB + 20 GiB = 564 GiB (605590388736 bytes) |
| Margin | 2313.48 GiB |
| Kit per-start check (one output cap + 20 GiB; kit `ext1-check`) | 156 GiB |

**Context, not a check here.** The campaign shares External1. A147 L3-01 (V006 `73663c84` L909) forecasts about 2.1 TB for it, UNTESTED until W1 is measured: that is 1955.8 GiB, so the campaign plus the four S0 caps come to about 2519.8 GiB against 2877.48 GiB free. A147 calls this tight against External1 alone and has root re-forecast from W1's measured outputs before free space falls below the next wave's need plus all NGC outputs.

## Not done

- Nothing was created on External1, and no directory there was listed.
- No run tree was opened.
