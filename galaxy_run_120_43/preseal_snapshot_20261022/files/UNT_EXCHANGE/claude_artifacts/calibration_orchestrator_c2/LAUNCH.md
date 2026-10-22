# LAUNCH: DDO154 calibration orchestrator c2v001

Claude2 launches. Nothing here has been launched. Hashes are in `HASHES.txt`.

## 0. What runs

| Piece | File | sha256 |
|---|---|---|
| orchestrator | `calibration_orchestrator_c2v001.py` | see HASHES.txt |
| coordinate spec (proposed final, freeze it first) | `DDO154_CALIBRATION_COORDINATE_SPEC_V001.json` | see HASHES.txt |
| proposed run config | `RUN_CONFIG_DDO154_V001.json` | see HASHES.txt |
| engine / freeze | `calibration_freeze_c2_v003a/…engine_c2v003a.py` / `…freeze_c2v003a.py` | `193841fa…` / `5ee3e5dc…` |
| forward driver | `absorb_c2_0473/driver_f/galaxy_m0_forward_c2v003c.py` (includes v003b's distance support) | `ed326130…` |
| monitor / campaign | `galaxy_m0_forward_c2_0466/root_monitor_c2v001.py` / `campaign_c2v001.py` | `ba031c23…` / `71274ceb…` |
| anchor (reused, not rerun) | `CLAUDE2/runs/A2_ANCHOR_F10_RUN_V001` result / receipt | `bcd2f64e…` / `f8bc976a…` |

The work dir in the config is `CLAUDE2/runs/DDO154_CALIBRATION_ORCH_V001`. It must not already exist, or it must be a work dir of this same config. Change it in the config if you want another location. Editing the config changes its sha, and that is fine: the config is not pinned anywhere else.

Set `PY=/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3` and `O=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calibration_orchestrator_c2`.

## 1. Before W1

1. **Freeze the coordinate spec.** Copy it to its frozen location if you want one. If you do, put the copy's path and sha in `coordinate_spec` in the config.
2. **Numerics.** `"numerics": null` means the anchor numerics: cube truncation, default grid, Picard 4, rule brackets, `column_workers` 2.
   - With these numerics the anchor alias is used, and W1 is the 4 Jacobian +side calls.
   - After the P-88 kmax verdict, put the converged numerics block in `numerics`. That changes the cache id and disables the alias, so the seed is computed first. If `column_workers` changes, `max_concurrent` must satisfy `max_concurrent × column_workers ≤ 12` (6 at 2 workers, 12 at 1).
3. **Disk (D3).** Each call writes about 6.1 GB (the anchor's `final_output_bytes`). About 262 GB is free.
   - Before each wave, the disk guard requires `n_calls × 8 GiB` (the output cap) plus a 20 GiB reserve.
   - Without a retention rule it halts with `HALTED_DISK` after roughly 25–30 calls.
   - The orchestrator never deletes anything. Retention is your decision.
4. **Dry plan** (read-only; writes nothing and creates no work dir):
   ```
   OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 $PY -I -B $O/calibration_orchestrator_c2v001.py plan --config $O/RUN_CONFIG_DDO154_V001.json
   ```
   The expected output with the default numerics:
   - `alias.used: true`, with max relative deviation 3.37e-15;
   - `next_wave.n_calls: 4`, family `jacobian`;
   - u steps of +0.05 on s, γ/Eref, ℓ_F and D (s 0.10883, γ 3.7026e42, ℓ_F 1.0616e20, D 4.04652);
   - `cache_id a49fbb97…`.

## 2. Run (resumable; one command)

```
cd /tmp && nohup env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
  NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 \
  $PY -I -B $O/calibration_orchestrator_c2v001.py run --config $O/RUN_CONFIG_DDO154_V001.json \
  >> "/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs/DDO154_CALIBRATION_ORCH_V001.log" 2>&1 &
```

- Add `--max-waves N` to stop after N waves. Running the same command again continues.
- **Resume after an interruption** (crash, kill, reboot): run the same command.
  - A stale lock is renamed, not deleted.
  - The interrupted wave is re-derived by the probe and must match its `WAVE_PLAN.json`.
  - Calls still running from the old campaign are waited for. They are never relaunched or touched.
  - Their receipts are then verified, and only the calls that never started are launched.
- **Progress:** watch `work_dir/EVENTS.jsonl` and `waves/wave_NNNN/WAVE_RESULT.json`, or run `… status --config …`.

## 3. Halts and decisions (nothing is retried automatically)

| Exit | Status | Meaning | Action |
|---|---|---|---|
| 0 | `COMPLETE` | Replay made zero uncached calls twice with identical bytes. The calibration record and registry are written and verified. | Read `FINAL_SUMMARY.json`. |
| 4 | `HALTED_INFRA` | A monitor cap (wall / RSS / output), a missing or unverifiable receipt, a spec refusal, or an unexpected driver status. | Inspect `waves/wave_NNNN/INFRA_HALT.json`, then run `… resolve --config … --wave NNNN --key <prefix>\|--all --decision invalid\|retry --reason "<text>"`, then rerun `run`. |
| 7 | `HALTED_UNRESOLVED` | A key that failed for infrastructure reasons is requested again before it was resolved. | Resolve it as above. |
| 5 | `HALTED_DISK` | Not enough free disk for the next wave. | Apply retention, then rerun. |
| 10 | `ORPHANS_STILL_RUNNING` | Calls of an interrupted wave are still running after 6 h. | Wait, then rerun. |
| 9 | `REPLAY_FAILED` | Should never happen. | Report it; do not freeze. |
| 3 | `REFUSED` | A pin or configuration error. | Fix it. |

**Model outcomes are cached as invalid evaluations and are final.** These are the driver statuses `COMPLETED_INVALID`, `FAILED_AT_STAGE`, `BLOCKED` (including `ROUTE_A_ITERATION_NOT_4`, PC-9), `ROUTE_A_NO_FIXED_POINT` and `FAILED`.
- The driver status is kept as `failure_class`.
- They are never relaunched.
- Any side stopped by one of them is listed in `FINAL_SUMMARY.validity_limited_sides_D6`.

## 4. Expected waves and times (each real call ~1.9 h, ~1.45 GB RSS, ~6.1 GB disk)

A batch is at most 6 calls running at once (6 × 2 column workers = 12 processes). A wave with more than 6 calls runs in ⌈n/6⌉ batches. Wave wall time ≈ batches × 1.9 h; the slowdown from 6-way contention is UNTESTED.

| Wave | Calls | Batches | Content |
|---|---|---|---|
| W1 | 4 | 1 | Jacobian +side of s, γ/Eref, ℓ_F, D (seed = anchor alias, 0 calls) |
| W2 | 4 | 1 | Jacobian −sides. Each is requested only if its +side was valid, so it cannot be predicted earlier. An invalid +side gives a halved +side instead. |
| W3–W5 | 1 each | 1 each | Linearised repair. The anchor is not admitted: rows 06, 08, 09 and 11 are outside, so the repair is sequential (≤ 3). |
| then, if nothing is admitted | 12 | 2 | Pre-march global Halton design. If still nothing is admitted, the run ends `NO_ADMITTED_POINT_FOUND` (emptiness not proven, D5) after about 21–24 calls, ~9 batches ≈ 17 h, ~140 GB. |
| then, if a point is admitted | ≤ 2m per wave | 1–2 each | Round-0 march and bisection: all sides in parallel, ≤ 10 sequential steps. |
| — | 24 | 4 | Local and global Halton designs (one wave) |
| — | ≤ 2m per wave | 1–2 each | Iterated rounds (LP rays, then axis marches) until the budget of 120 binds |

On the synthetic toy with these engine parameters (4 varying coordinates), the main case took 80 calls in 22 waves / 25 batches. At 1.9 h per batch, a full 120-call run is about 30–40 batches, or 57–76 h. It needs about 730 GB without retention.

## 5. After `COMPLETE`

`FINAL_SUMMARY.json` carries:
- the engine status and the truncation causes;
- the record and registry hashes (log `record_file_sha256` externally, ROOT_CALL_ORDER step 1b/6);
- the D6 and D7 lists;
- the cache waste (`n_unused_launched_theta`, 0 on every test).

Freeze only if `engine_status == COMPLETE`. Follow ROOT_CALL_ORDER steps 2–8 with the replayed run object, the pinned record (step 5 `input_files`), the real NGC3198 slots and the real NGC forward.
- The `Context.freeze_spec` built with the real `ngc3198_slots` must reproduce the same `engine_coordinates`; the orchestrator refuses otherwise.
- The tested sequence is `tests/test_orchestrator_c2v001.py::freeze_path`.
- `ORIGINAL_K` is declared `EVALUATED_BEFORE_FREEZE`, so its evaluation on the selected points must be supplied. If it will not be evaluated, record the change to `NOT_EVALUATED_BEFORE_FREEZE` before step 5. `ML_3p6_0.4` and `ML_3p6_0.6` are `NOT_EVALUATED_BEFORE_FREEZE` because driver v003c does not expose M/L (PC-5).

## 6. Test command (synthetic; mock workers ~2 s per call)

```
$PY -I -B $O/tests/test_orchestrator_c2v001.py      # writes only under $O/test_runs/RUN_<UTC>_<pid>/
```
