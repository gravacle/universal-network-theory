# Channel-bearing-owner Birth-residence transport and worm V004 pilot packet: interface note (c2v002)

Lane: Claude2, `birth_kinetics_c2`. Authority: the next remedy in section 7 of `WORM_PILOT_EVALUATION_V001.md`, as reviewed in `review/REVIEW_V001.md` (PASS_WITH_CORRECTIONS). This note applies the review's corrections. In particular, it does not claim that census/U slowness causes the residual R/S failure; that remains UNTESTED.

**Status:** implemented and verified on synthetic states and on explicit native states. Nothing was sampled or launched. It needs a distinct review before root launches it. `CODEX1/OWNED_L4_WORM_BIRTHK_RUN_V001` is absent.

## The one change

The reviewed V001 Birth transport (`6f866bda…`) picks the owner uniformly from all 128 roster owners. When that owner has no Birth or reverse mark at the reference dwell, the attempt self-loops. In `OWNED_L4_WORM_LOOP_RUN_V001` this happened on 81.7% and 80.0% of attempts.

c2v002 picks the owner uniformly from S(x), the owners that do have such a mark at the reference dwell x, and corrects for this exactly:

```
log MH = [log|S(x)| - log|S(y)|] + [log|R(x,o)| - log|R(y,o)|] - sum dt (D_new - D_old) + sum log(W_new/W_old)
```

R(x,o) is V001's per-owner roster, and y is the reference dwell after the move. Both counts are recomputed on every proposal. Everything else is unchanged from V001: the marks, the whole-path transform, the guards, event replay, the weights and the target.

S and every R come from one palette enumeration over the union of the roster's owner groups. A legal attempt therefore costs two enumerations, the same as V001.

The operator contract says this union enumeration gives the same rosters as V001's per-owner enumeration. Every proposal enforces it with these checks:
- The chosen mark must equal the per-owner mark at x.
- The reverse mark must equal the per-owner inverse mark at y.
- No Birth mark may have an owner outside the roster.

A failed check is a contract failure (status `failed`). The diagnostics follow the worm module's atomicity pattern: read-integral sums, the donor diagnostic and accepted counters are written only after the `before Birth residence atomic commit` checkpoint. V001 wrote its read sums before that checkpoint.

## Files

| File | Role |
|---|---|
| `owned_worldline_birth_residence_transport_c2v002.py` | The transport. `MODULE_VERSION='birth_residence_c2v002'` |
| `owned_L4_worm_birthk_recipe_v004.py` | Recipe V003 with the Birth slot changed (4 edits). It pins the new module bytes and checks its version |
| `owned_L4_worm_birthk_root_worker_v004.py` | Worker V003 with 7 edits (listed below) |
| `owned_L4_worm_birthk_monitor_v004.py` | Monitor V003 with 6 edits: worker V004 and its pins (including the Birth module), output `OWNED_L4_WORM_BIRTHK_RUN_V001`, hard wall 9000 s |
| `build_worm_birthk_packet_v004.py`, `DELTA_*.diff`, `PACKET_BUILD_REPORT_V004.json` | The build edits, and unified diffs against V003 and against the V001 transport |
| `WORM_BIRTHK_PILOT_DELTA_SPEC_V004.json` (written by `write_delta_spec_v004.py`) | Delta spec: proposal, choice ledger, bounds, pilot, deciding tests, pins |
| `birth_residence_fixture_c2v002.py`, `birth_fixture_toy_c2v002.py` → `BIRTH_RESIDENCE_FIXTURE_RESULTS_C2V002.json` | Exact-enumeration fixtures |
| `birth_residence_native_explicit_check_c2v002.py` → `BIRTH_RESIDENCE_NATIVE_EXPLICIT_CHECK_C2V002.json` | Operator V003 on explicit L=4 states |
| `packet_delta_check_v004.py` → `PACKET_DELTA_CHECK_V004.json` | Static, fake-module and real-prepare checks of the packet |
| `HASHES_C2V002.txt` | SHA-256 of every deliverable, computed from the bytes |

`devrun/` holds outputs from development iterations. They are not evidence.

The worker V004 edits:
- the recipe and Birth pins;
- seed 2026101702;
- warmup 512 → 1024, with measurements staying at 1024;
- max_sweeps 3072 → 4096;
- the time-proportional caps doubled;
- the budget hook replaced after preparation;
- `result['schedule_binding']` and `result['birth_residence_request']` added.

## Call signature

```
move(run, path, rng, diag, sampler, owner_roster) -> (path, 'changed' | 'rejected')
```

This is V001's signature, and recipe V004 calls it unchanged.

The move uses these sampler functions: `_Stop`, `_budget_check`, `_record_groups`, `_palette_channels`, `_unique_mark`, `_target_key`, `_segment_core`, `_event_from_channel`, `_keys_equal`, `_check_times`.

It reads `run['group']`, `run['beta']`, `run['caps']['max_events_per_path']`, `run['burn_in_sweeps']` and `run['stage']`, plus `diag['sweeps_completed']`.

The counters keep the `birth_residence_` prefix and also have `birth_residence_measurement_` copies. The new counters are:
- `channel_bearing_owner_count_sum`
- `no_channel_bearing_owner`, which replaces `empty_reference_owner`
- `owner_count_ratio_nonunit`
- `log_mh_negative`

`birth_residence_last_proposal` also carries the forward and reverse owner counts and every log term.

## Results

**F1: exact kernel.** `move()` was enumerated over all scripted RNG choices on a toy whose target is not invariant under Birth.
- Scope: 9 cases, 1200 closed paths and 1648 off-diagonal transitions.
- The cases cover: no events, flip pairs, a Birth/reverse pair, Birth with interleaved flips, and reverse-then-Birth. Three of them use the restricted roster (3, 4).
- In the toy, owner 3 never has a mark, and the other owners have marks depending on state.
- 592 legal proposals change |S|, and 176 reference states have an empty S.
- Detailed balance holds to ≤1.0e-15, and the kernel matches an independent oracle to ≤3.3e-16.
- Every row sums to 1, every output is valid, and the input is never mutated.

**F2: forward plus reverse log MH.** On all 1648 legal proposals the sum is exactly 0.0, and the reverse move restores the path.

**F3–F5: guards, replay and interruption.**
- Terminal failures fire for malformed, over-cap and unclosed paths, bad rosters, a stored-W mismatch, union/per-owner disagreement (skewed W or a missing reverse) and an owner outside the roster.
- These cases are reached as self-loops: empty S (with zero draws), dwell guard, inverse guard, inverse canonical target, event replay and Metropolis.
- Replayed events carry the transformed W.
- The move was interrupted at each of its 36 budget checkpoints. The input stayed unchanged each time, and no read-integral, accepted or donor diagnostic was written.

**F6: mutants and controls.** Detailed balance catches every mutant, with a relative error of 0.5. Both controls pass.

| Variant | Result |
|---|---|
| Owner-count correction missing | caught |
| All roster owners counted | caught |
| All owners with any mark counted | caught |
| V001 owner selection combined with the c2v002 correction | caught |
| Control: per-owner enumeration, same kernel | passes |
| Control: the reviewed V001 transport, which is exact for its own proposal | passes |

**F7: no-owner self-loops on the toy.** The self-loop probability falls from 0.367 under V001 to 0. The legal-transport probability rises from 0.450 to 0.724.

**Native C1: union partition.** The union partition matches all 128 per-owner rosters and the `primitive_channels` partition on 4 explicit states, with 0 owners differing.

| State | Active slots | \|S\| | V001 empty-owner fraction | Marks |
|---|---|---|---|---|
| seed | 0 | 128 | 0 | 4608 Birth marks |
| 12 native Births | 12 | 123 | 0.039 | |
| saturated (128 native Births) | 128 | 20 | **0.844** | reverse marks only |
| saturated + 64 flips | 128 | 11 | **0.914** | reverse marks only |

The saturated rows reproduce the pilot's empty-owner fraction of about 81%. A union call takes 0.015–0.03 s on saturated states and 0.17 s near the seed.

**Native C2: shim run.** The module was run through a native-state shim of the sampler API. The shim is not V006; for TRIAL it uses W = |amplitude| and D = the raw diagonal. All 27 changed proposals reverse exactly with a log MH sum of 0.0. |S| changes across moves, for example 11 → 13.

**Packet check.**
- All pins match their bytes.
- Only the recipe and Birth source pins differ from V003, and `branch_of` matches V003 at 200,009 points.
- In the fake dispatch, the Birth move receives 6 arguments, and V001 is refused.
- A real recipe V004 `prepare` was run (no sampling), followed by the worker V004 schedule block executed verbatim. The worker's frozen-value guards pass, and the schedule becomes burn-in 1024 with caps {10000, 4.8M, 4096, 3.2M}.
- The replaced hook stops at exactly 3.2M calls and at 8800 s.

## Declared choices (ledger in the spec)

- Time-proportional caps are doubled together with the 9000 s hard wall: soft wall 8800 s, 3.2M calls and enumerations, and 4.8M events. RSS (4 GiB hard, 3.5 GiB soft), output (2 GiB) and the per-path event cap are unchanged.
- max_sweeps = 4096 is computed: the sampler caps the total over both chains.
- The family recipe is pinned and hard-codes its soft budget, so worker V004 replaces the hook after preparation, using the same clock and call counter.
- Two cases that V001 handled silently are now contract failures:
  - a Birth owner outside the roster, which V001 ignored;
  - a union/per-owner disagreement at the reverse, which V001 treated as a `reverse_selection` self-loop.

## Launch (root only, after a distinct review)

```
/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -I -B /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/birth_kinetics_c2/owned_L4_worm_birthk_monitor_v004.py
```

## Deciding tests (unchanged criteria)

- The all-36 plus background criterion.
- The census/U two-part rule with flat quarter means.
- Born edges shared between the chains rising toward the within-chain lag-512 overlap.

There is no mixing claim. Counts of accepted moves are not evidence on their own.
