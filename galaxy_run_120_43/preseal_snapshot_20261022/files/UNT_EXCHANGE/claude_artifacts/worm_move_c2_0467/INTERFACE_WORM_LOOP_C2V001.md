# Worm-loop whole-path move: interface note (c2v001)

Lane: Claude2, `worm_move_c2_0467`. Authority: ROOT_DECISIONS_A1_A2_2026-10-17_V001.md, section A2, "Next sampling remedy (D2)". The binding review corrections (REVIEW_V001.md) are applied.

**Status:** implemented and verified on synthetic and explicit native states. Nothing was sampled or launched. It now needs a distinct review; only root launches it.

## Files

| File | Role |
|---|---|
| `owned_worm_loop_whole_path_c2v001.py` | The move. It replaces only the 10% current-graph cycle slot. |
| `owned_worm_committed_capture_durability_v002.py` | Durability V002. It adds the reference key, Birth census and U to every row. V001 is unchanged. |
| `owned_L4_worm_loop_recipe_v003.py` | Generated from recipe V001 by explicit edits. |
| `owned_L4_worm_loop_root_worker_v003.py` | Generated from worker V002 by explicit edits. |
| `owned_L4_worm_loop_monitor_v003.py` | Generated from monitor V002 by explicit edits. |
| `build_worm_pilot_packet_v003.py`, `DELTA_*.diff`, `PACKET_BUILD_REPORT_V003.json` | The edits themselves, plus unified diffs against the predecessors. |
| `WORM_LOOP_PILOT_DELTA_SPEC_V003.json` | The delta spec: proposal, choice ledger, bounds, pilot, deciding tests, pins. |
| `worm_loop_fixture_c2v001.py`, `worm_fixture_toy_c2v001.py` → `WORM_LOOP_FIXTURE_RESULTS_C2V001.json` | Exact-enumeration fixtures. |
| `worm_loop_native_explicit_check_c2v001.py` → `WORM_LOOP_NATIVE_EXPLICIT_CHECK_C2V001.json` | Operator V003 run on explicit L=4 states. |
| `durability_v002_fixture_v001.py` → `DURABILITY_V002_FIXTURE_RESULTS_V001.json` | Durability fixture. Its integration blocks are in `*_integration_run/`. |
| `packet_delta_check_v003.py` → `PACKET_DELTA_CHECK_V003.json` | Static and fake-module checks of the V003 packet. |
| `HASHES_C2V001.txt` | SHA-256 of every deliverable, computed from the bytes. |

`devrun/` holds outputs from development iterations of earlier module bytes. They are not evidence.

## Call signature

```
move(run, path, rng, diag, sampler, owner_roster, state_labels) -> (path, 'changed' | 'rejected')
```

This is the same signature as the cycle module it replaces.

- `sampler` is the pinned V006 module.
- `owner_roster` is the fixed original A+B tuple.
- `state_labels` is the operator's public keyword-only function.

The move uses these sampler functions: `_Stop`, `_budget_check`, `_record_groups`, `_palette_channels`, `_unique_mark`, `_target_key`, `_state_key`, `_segment_core`, `_event_from_channel`, `_keys_equal`, `_check_times`. It also reads `run['context']`, `run['beta']`, `run['caps']['max_events_per_path']`, `run['burn_in_sweeps']` and `run['stage']`, and `diag['sweeps_completed']`.

Pure helpers, used by the fixtures:
- `eligible_colouring`
- `grow_walk`
- `walk_branch_product`
- `reverse_edges`
- `loop_contract`

Module constants, pinned by recipe V003: `MODULE_VERSION='worm_c2v001'`, `MAX_WALK_STEPS=1024`, `LOOKAHEAD=True`.

## Rule

**Eligible graph.** An edge is eligible if it is present in every dwell and has the same occupancy in every dwell.

**Walk.**
1. Choose a start v0 uniformly from the roster.
2. Choose a viable occupied edge uniformly.
3. Keep choosing a viable eligible edge of the alternate colour uniformly.
4. Stop at the first revisit of a vertex w. The loop is w…w. The tail is not flipped.

**Flip.** Flip the loop in every dwell.

**Hastings ratio.** The reverse walk is the same v0 and the same tail, followed by the loop in the opposite orientation. It is recomputed on the transformed colouring. The ratio is the forward branching product over the reverse branching product, times exp(−Σ dt ΔD), times the event W ratios.

**Self-loops.** These cases leave the path unchanged:
- empty start
- dead end
- step cap reached
- reverse walk impossible
- a transformed event fails its replay guard or target

**Terminal failures.** These stop the run rather than self-loop:
- a malformed or unclosed path
- an inconsistent stored event
- a missing native flip mark at the reference dwell
- a key-contract violation
- eligibility that is not invariant under the loop flip

## Declared choice: LOOKAHEAD

The literal rule takes every alternate-colour edge as a candidate. The one-step viability lookahead additionally excludes a continuation into an unvisited vertex that has no edge of the next required colour.

- **Effect.** On an explicit native defect-laden state (U=84), closure rose from 40% under the literal rule to 77% (`N4`). On defect-free states it changes nothing.
- **Exactness.** Both rules are exactly enumerated (F1–F3, and F8 for the literal rule). The forward and reverse counts coincide in both cases (FORMAL), and they are recomputed on every proposal.
- **To revert:** set `LOOKAHEAD = False`, then rebuild and re-pin.

## Results

**F1. Proposal symmetry, exact Fractions.** Every closed walk's reverse regenerates the same loop with the identical integer product. It is produced by `grow_walk` itself.

| Graph | States | Check |
|---|---|---|
| Q3, which has 4-cycles | all 4096 | aggregate Q(a→b)=Q(b→a) over 5312 ordered pairs |
| honeycomb 2×3 torus | 39 (d=1, d=2 and a defect sector) | aggregate |
| honeycomb 3×3 torus | 42 (dimer sector) | aggregate |
| L=2 periodic diamond | 24 of the 2970 ice-sector states | walk level |

Winding and contractible loops are both proposed. For example, the 3×3 torus gave 40716 winding and 10908 contractible closed walks.

**F2. End-to-end exact kernel of `move()`.** The kernel was enumerated over all scripted random choices in 8 cases against a toy target. The toy target deliberately does not leave D or the event W invariant under a loop flip. The 8 cases are:
- Q3, no events (selected degree sectors)
- Q3, a flip pair (all 4096 incidence words)
- Q3, a hop pair (all 4096 incidence words)
- Q3, Birth followed by its reverse (all 4096 incidence words)
- Q3, Birth, flip, flip, Birth reverse (all 4096 incidence words)
- honeycomb 2×3 torus: no events, a flip pair, a hop pair

Results:
- Maximum relative detailed-balance error is ≤2.0e-15.
- Maximum difference from the independent oracle kernel is ≤1.4e-15.
- Every row sums to 1.
- Every output path is valid, and the input is never mutated.

**F3. Forward plus reverse log MH.** For all 65,862 legal proposals, the forward and reverse log MH sum to exactly 0.0, and the reverse move restores the original path.

**F4–F6. Replay, guards and interruption.**
- Replayed events carry the transformed native W.
- Every guard fires.
- The move was interrupted at each of its 42 budget checkpoints. The input stayed unchanged each time, and no read-integral or accepted counter was written. The last checkpoint is `before worm-loop atomic commit`.

**F7. Mutants.** All four mutants are caught, and the control passes.

| Mutant | Caught by |
|---|---|
| Wrong reverse probability (loop not reversed) | detailed balance and oracle |
| Missing start branching factor | detailed balance and oracle |
| One-dwell-only flip | oracle |
| One-dwell flip with guards removed | invalid paths and oracle |
| Control: the same factor omitted in both directions | passes, as it should |

**Native checks (operator V003, explicit L=4 states, no sampler).**
- **N1:** the label-route loop flip equals the composition of native flip marks, and only the incidence component changes.
- **N2:** the raw and uniform-lapse diagonal sums are bit-identical after an alternating loop, while 39–201 reads change. A single-edge flip does change the diagonal.
- **N3:** 10 of 10 worm flips on an explicit Birth/reverse path replay both native events exactly.
- **N4:** mean loop length is 13–18 and mean tail is 7–9. The fraction of length-4 loops is 0 on the seed (all its loops wind), 15% on the born state and 17% on the defect-laden state.

**Durability.**
- The keys round-trip exactly, including 36864-bit ints and the native seed and born keys.
- The digest is hex, which avoids Python's int-to-decimal digit limit at L=4.
- Census, U and the time means are exact.
- The V001 fields are retained, and a mismatched commit tuple is detected.

**Packet.**
- All pins match their bytes.
- `branch_of` equals V001's thresholds at 200,009 points.
- A fake-module run dispatches every branch, and the worm receives 7 arguments.
- The seed 2026101701 is bound three times.
- `OWNED_L4_WORM_LOOP_RUN_V001` is absent.

## Production expectation (computed, not assumed)

Under TRIAL with uniform lapse and zero sources, D and the replayed W are exactly invariant (N2). The log MH is therefore expected to be exactly 0, with no Metropolis rejections. The counters `worm_loop_log_mh_exactly_zero`, `_log_mh_negative`, `_metropolis` and `_walk_ratio_nonunit` record what actually happens.

## What this does not do

- It cannot move the Birth census, the slot roster or any degree (FORMAL).
- There is no mixing claim. The deciding tests are those in the spec: the all-36 and background criterion, census and U stationarity from the new per-row series, and the sector question from the saved reference keys.
