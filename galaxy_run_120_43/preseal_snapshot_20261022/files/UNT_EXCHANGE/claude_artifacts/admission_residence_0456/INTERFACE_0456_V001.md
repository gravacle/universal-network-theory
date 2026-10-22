# INTERFACE_0456_V001 — whole-path admission residence transport c3v001

Module `admission_residence_transport_c3v001.py` (this directory). It has an inert import (`math` only) and adapts the pinned Birth transport `owned_worldline_birth_residence_transport_v001.py` (`6f866bda…`). Physical status: not_assessed.

## API

`move(run, path, rng, diag, sampler, owner_roster) -> (path, 'rejected') | (new_path, 'changed')`

- **sampler:** the actual pinned V006 module object, injected. It uses `_Stop`, `_budget_check`, `_record_groups`, `_palette_channels`, `_unique_mark`, `_segment_core`, `_target_key`, `_keys_equal`, `_event_from_channel` and `_check_times`. No global function is patched, and no schedule or mixture weight is chosen here.
- **run:** uses `stage`, `beta`, `caps['max_events_per_path']`, the budget hook (through `_budget_check`), and `group`. `group` maps labels to permanent original owners and exists only under a palette binding. If it is absent the move fails closed.
- **owner_roster:** a tuple of unique graph0 A+B original vertex labels, frozen by root, each with `run['group'][v] == v`.
- **path:** a closed `{'segments': k+1, 'events': k, 'times': k}`, as in the sampler.

## Proposal

1. Choose v uniformly from `owner_roster`, whatever its eligibility. The owner is `('admission', ('vertex', v))`, which is V003 `owner_id`.
2. The forward roster is the actual positive `admit`/`admit_rev` records with exactly that owner, at dwell 0, from `_palette_channels(group[v])`. Records of newborn vertices in v's group have a different owner and are excluded. An admission record at v with any other owner descriptor fails closed.
   - **Empty roster:** self-loop (`empty_reference_vertex`), with no resampling.
   - **Roster size:** under V003 the roster has at most one mark, since admit needs p = s = 0 and admit_rev needs p = s = 1. The general N factor is kept anyway.
3. Choose the mark uniformly; the inverse kind is the other of admit/admit_rev. The move:
   - transforms every dwell through `_segment_core`, applying the operator's own target;
   - requires the inverse mark, with canonical target equal to the old key, in each dwell;
   - requires closure of the transformed path;
   - requires the reverse mark in the new dwell-0 roster, targeting the old dwell-0 key.
4. Each stored event is re-verified (mark, target, W) at its old dwell; a mismatch fails closed. It is then replayed with the same kind and owner on the transformed dwell. A missing mark or wrong target is a self-loop. New events come from `_event_from_channel`. Times and event count are unchanged.
5. log MH = log(N_fwd/N_rev) − Σ_i (t_{i+1} − t_i)(D_new,i − D_old,i) + Σ_events log(W_new/W_old), with t_0 = 0 and t_{k+1} = β. There is no admission amplitude, event-count or time-density factor. Metropolis applies only when log MH < 0.

**RNG draws:** vertex index, then mark index, then `random()` only when log MH < 0, the same order as Birth.

## Diagnostics (`diag`)

- **Counters `admission_residence_<name>`:**
  - `attempts`;
  - `admit_selected` and `admit_rev_selected`;
  - rejection reasons, each also counting `rejected`: `empty_reference_vertex`, `dwell_guard`, `inverse_guard`, `inverse_canonical_target`, `reverse_selection`, `event_replay_guard_or_target`, `metropolis`;
  - `legal_transport`;
  - `accepted_changed`, `admit_accepted_changed` and `admit_rev_accepted_changed`.
- **`admission_residence_last_proposal`:** a dict with kind, vertex, forward_count, reverse_count and log_mh_ratio.
- **Read sums:** `admission_residence_read_integral_change_sum` and `…_absolute_…` hold Σ_i dt_i (row_new − row_old) over the sampler's tracked reads. They are written only after the atomic-commit budget checkpoint. No state-tuple index is read.

## Fail-closed and interruptions

Each of the following raises `sampler._Stop('failed')`:
- an invalid roster;
- no groups;
- a malformed or unclosed path;
- a transformed path that is not closed;
- an inconsistent stored mark or rate;
- a non-finite log MH or read change;
- a mismatch in read-diagnostic length;
- an unexpected admission owner.

More events than the cap raises `_Stop('incomplete')`.

Budget checkpoints are 'before' (proposal, every enumeration, atomic commit) and 'between' (the dwell-transform and event-replay loops). Any stop propagates. The input path and its lists are never mutated, so an interruption retains the old path. Only attempt-level counters can have been recorded before an interruption.

## Scope

This is a restricted reversible proposal that supplements existing moves. It makes no claim of ergodicity, mixing or improvement. Admissions of newborn vertices are not proposed, since the roster is graph0 originals per 0456. Root selects the fixed mixture weight and measures any effect on mixing.
