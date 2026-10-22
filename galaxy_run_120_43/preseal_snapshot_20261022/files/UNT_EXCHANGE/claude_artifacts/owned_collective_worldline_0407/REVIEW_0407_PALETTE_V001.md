# REVIEW 0407: blocked-palette move in the v002 worldline module (V001)

**Role:** distinct palette-move reviewer. I did not write worldline v001 or v002, the PALETTE note, or its distinct review.

**Mode:** static text review only.
- Nothing was imported or executed.
- The only Python run was `python3 -I -B` doing `ast.parse` and `compile` on the module's bytes, from a scratch directory.
- No `__pycache__` was written into the 0407 directory.
- No numerical runs, sampling, data extraction, network access or package installs.
- Read-only on `Universal Network Theory`. No forbidden-name files were opened.

## Inputs (full sha256 computed from bytes)

| File | sha256 | Check |
|---|---|---|
| `claude_artifacts/owned_collective_worldline_0407/owned_collective_worldline_static_response_v002.py` | `0d041119bd11227746238663ed93d99863d3a94c8295e539dbed15255b42a941` | ast.parse + compile OK; no undefined names in the palette functions |
| `helpers/coefficient_method/OWNED_WORLDLINE_BLOCKED_PALETTE_MOVE_IMPLEMENTATION_V001.txt` ("PALETTE") | `3b06ee3392894de2e96716c86f7b3184c792a407a81435f95aa448440418ca16` | matches |
| `helpers/response_packet_audit/OWNED_WORLDLINE_BLOCKED_PALETTE_DISTINCT_REVIEW_V001.json` | `42e4041006a07e3d9f5a44afbd079077be1e60ef91919d34251915f0e2f8de35` | matches |
| `claude_artifacts/owned_retained_response_0405/owned_parent_operator_v001.py` (text; owner_id formats, guards) | `27ad1762dbdc559eb92edcb6f7fe83790b73a4e23d71b12500b8586c811de3b6` | matches the module docstring |
| `claude_artifacts/owned_retained_response_0405/owned_parent_operator_v002.py` (text; API reconciliation only) | `b5fded4d1272322036748d4d1b4e634a804c1da1ad6717e70e32b4f2a364a94e` | read only |

## Verdict

**PASS_SCOPED.** As written, the blocked-palette move is a correct additive Metropolis-Hastings move for the marked positive path measure exp(-∫D)·ΠW.
- I found no blocking correctness defect.
- One fail-closed integration item (R1) must be reconciled before `palette_parameters` can be non-None against either on-disk operator.
- The move is correct but does not yet accelerate per-event cost (N2).

## Blocking issues

None found on correctness.

## Required before use (fails closed; not a correctness defect)

**R1. The restricted-enumeration API name and keyword do not match the on-disk operator.**
- The module requires `owner_restricted_channels(*, context, state, owners)`. See the docstring at L86-91, `_admit_operator_api` at L454-455, and the call at L1389-1390.
- Operator v001 has no restricted enumeration.
- Operator v002 is now on disk. It exposes `palette_channels(*, context, state, palette_owners)` at L1837.
- So with either operator passed directly, a non-None `palette_parameters` stops at input admission with status `failed`. No result is ever wrong because of this.
- The classification in operator v002 matches the module's `_record_groups`:
  - Birth and its reverse go by owner j.
  - Site, Bind and admission go by vertex group.
  - flip and hop go by either endpoint group.
  - Newborns a_j and b_j belong to group j.
  - Diagonal records it returns are skipped by `_palette_members` (L1374-1375).
- The module docstring and FIX_DELTA say "0405 module A v002 was not on disk". That statement is now stale.
- The final checker must reconcile the name, the keyword (`owners` vs `palette_owners`) and the rest of the v002 API. I did not choose an alias.

## Hand verification

### 1. Proposal-density cancellation, as implemented

**Setup.**
- The origin o is uniform on [0, β).
- The length L uses the L10 density. The palette S is drawn from caller weights.
- All three draws are state independent (`_choose_palette` L1939, `_select_interval` L1856). They have the same density for the forward and the reverse move.
- In the rotated frame, I = [0, L). The held skeleton H is every event in I whose groups miss S (L1996-2000), with its times and its (kind, owner_id).

**Target ratio.** For the old path X and the proposed path Y, which agree outside I:

π(Y)/π(X) = exp(-∫_I D_Y + ∫_I D_X) · Π_{inside,Y} W · Π_{H,Y} W / (Π_{inside,X} W · Π_{H,X} W).

**Forward proposal density.**

q(Y|X) = c · exp(-∫_I r_S(Y)) · Π_{inside,Y} W · 1[every held replay legal, endpoint matches].
- Held replays are deterministic given (state, descriptor), so they add no density factor.
- Between held marks, the code draws `rng.exponential(1/r_S)` (numpy scale = 1/rate) at L2013.
- It picks a member channel with probability W/r_S (`_choose_channel` L1797).
- A draw that passes a held bound is discarded, then redrawn after the replay. By memorylessness, the survival factor exp(-r_S·(bound - t)) is part of the density.
- When r_S = 0, the loop goes straight to the held mark (L2012).

**Reverse proposal density.**

q(X|Y) = c · exp(-∫_I r_S(X)) · Π_{inside,X} W.
- The reverse move holds the identical skeleton, because classification depends only on (kind, owner_id) (L1999) and replayed events keep those labels (L2061).
- Replaying H on X's pre-event states returns X's own held records. This holds because (kind, owner_id) identifies at most one positive-rate record per state, which L2040-2047 enforces (more than one match gives `failed`).

**The ratio matches the code.** Combining the three expressions:

exp(∫_I(r_S - D)_Y - ∫_I(r_S - D)_X) · Π_H W_Y/W_X

This is exactly L2089, with:
- `new_terms` (L2084-2088). `rates[j]` comes from the same `_palette_channels(owners)` call that drove the CTMC.
- `old_terms` (L2077-2083). r_S is recomputed at each old state by the same function, and D is the stored D.
- `log_held` (L2060).
- min(1, e^x) at L2092.

**Indexing checked.**
- `len(segs) == len(rates) == len(times) + 1`.
- New segment j spans [times[j-1], times[j]), with times[-1] read as 0, and the last segment ends at L.
- Old segments j = 0..m use `rot["times"]`, with the last one clipped at L.
- Held marks are appended at their own `bound` times (L2062).
- Inside times lie strictly between bounds (L2015-2018). `_check_times` runs on the spliced path (L2100).

### 2. Palette membership by permanent labels; reversal invariance

`_record_groups` (L1318-1343):

| Kind | owner_id read | Groups |
|---|---|---|
| birth, birth_rev | `owner_id[1]` | the original owner. Operator `_owner_id` gives `("birth", owners[j], cut labels)`. |
| flip, hop | `("edge", (A, B))` | {group(A), group(B)} |
| bind, admit, admit_rev | `("vertex", v)` | {group(v)} |

- group(o) = o, and group(a_j) = group(b_j) = o, read from `graph0["slots"]` (L2770-2787).
- Palette labels must be original owners. Anything else gives `failed`.
- Only `owner_id` is consulted. Energy weights, supports and guards never enter membership.
- An unparseable owner_id or an unknown label gives `failed`, never a guess.

**Reversal invariance.**
- In the operator v001/v002 text, forward and reverse share their owner_id: the admission family, the birth family (the reverse's cut is `sorted(restored)`, and the forward cut is a sorted C_loc key), and the self-reverse kinds flip, hop and bind.
- In any case, reversibility of the move only needs the class to be a function of the event label, and it is.
- Non-member records returned by the restricted call are dropped and counted (L1378-1380, L1392).
- The optional verification compares multisets of (kind, owner_id, target, amplitude, energy_weights) against the palette members of `primitive_channels` (L1393-1413).

### 3. Held-event legality rejection

The held mark is replayed through the restricted enumeration on the held event's own groups, at the proposed current state (L2034-2050).
- The operator's guards remove the record, which gives a rejection (L2048-2050). These guards are:
  - donors;
  - Birth census and C_loc witness;
  - equal paired child bits;
  - newborn Ready with p = q = 0;
  - duplicate restored edge and predecessor witness.
- Records with zero amplitude or a zero lapse multiplier are not channels (L1268-1269, L1291-1295). So a proposed zero held rate also rejects.
- Equality of the whole prior global graph is never required.
- A replayed event gets:
  - the self-loop check and the Hermitian-partner check (L2057-2059);
  - a full new-state evaluation (L2054);
  - cap accounting as an event (L2053).

### 4. Unmatched-endpoint rejection without bridge renormalization

- L2067-2069 returns `(path, False)`. There is no conditioning and no renormalization.
- For the whole circle, the terminal state is the fixed anchor state.
- Gauge net increments are compared, and a mismatch gives `failed` (L2070-2076).

### 5. Retained rate ratios

- L2060 adds log W(new pre-event) - log W(old pre-event).
  - `held_ch["W"]` is the replayed record at the proposed state. Its multiplier uses the endpoint-averaged weights of the replayed transition.
  - `hev["W"]` is stored with the old event. Its pre-event segment travels with it through every splice and rotation, so it is the old pre-event state.
- When a pre-event state is unchanged, the record is the same and the term is exactly 0 (subject to N4).
- Inside W factors never appear in the ratio. They cancel against the proposal, as the PALETTE note requires.

### 6. Coexistence with global moves at nonzero selection probability

- `_move` (L1879-1889) draws one uniform u:
  - rotation with probability p_rot;
  - palette with probability p_sel;
  - global regrowth with probability 1 - p_rot - p_sel.
- Admission requires p_rot and p_sel in (0, 1), and p_rot + p_sel < 1 strictly (L2606-2614). Otherwise the run is `failed`.
- The global moves handle segments created by the palette move: the lazy full rate in `_seg_rate` (L1658-1663) and the start of `_ctmc_segment` (L1809-1811).
- Each component is reversible with respect to the same π, and the mixture weights are state independent.
- Blocked moves alone are not claimed to be irreducible (L19).

### 7. Caches never omit affected events or globally normalized reads

- No dependency cache, frontier or incremental diagonal exists (L3, L19).
- Every state created by an inside event or a held replay gets a full `_segment_core` (L2021, L2054). That means canonical key, `diagonal_terms`, `read_rows`, and the callback's `adapted_moment_reads` plus `pair_source_hamiltonian`.
- `_reads_at` (L1541-1623) caches only the state-independent label index, and fails if the labels change.
- The reused objects are the anchor `rot["segments"][0]`, `rot["segments"][m+1:]` and `rot["events"][m:]`. All of them sit at states that are identical by canonical key, and the endpoint check runs before the splice. So their D, D_a, read rows and the W of the first post-interval event are unchanged.
- The distinct review's adapter requirement also holds on the palette path:
  - the whitened callback enters D at every new palette state;
  - global-frame coarse rows are unsupported in every role (L8).
- This item holds by absence. It must be reviewed again if a frontier or cache is added.

### 8. Coincident-target marks

- Each operator record becomes one channel (L1299-1311). r_S is the `fsum` of record W values (L1312).
- There is no aggregation by target, and no merged amplitude is added again.
- The verification counts multisets.

## Notes (non-blocking)

- **N1.** See R1 above.
- **N2. The PALETTE efficiency instructions are not implemented.** These are the label/dependency event indices, cached unchanged segments, the changed-state frontier, and incremental local diagonals ("Use ...").
  - Every replayed held event costs one full `_segment_core` (O(V0) reads and callback) plus three restricted enumerations.
  - Every old interval segment costs one more restricted enumeration (two when verification is on).
  - The per-proposal cost is therefore O(events in I × V0), which is the naive replay the note warns about.
  - Correctness is unaffected, and L3, L19 and COST disclose this.
  - It does block any claim that the move speeds up per-event cost. Any gain would come only through acceptance, and none is claimed.
- **N3. Descriptor granularity.** The held descriptor is (kind, owner_id), not an explicit partial map.
  - In the operator v001/v002 text this does identify the local partial map:
    - flip, bind and hop are XOR maps with guards;
    - admit and admit_rev are separated by their guards;
    - Birth and its reverse are fixed by (owner, cut labels) and the current star.
  - The hop owner_id carries no direction. So a replay can realize the opposite hop direction, B_to_A instead of A_to_B. This is the same partial map, p_a ^ p_b under the guard p_a ≠ p_b, with the same |t|. The move remains valid because the reverse replay recovers the old record uniquely.
  - For other operators, any ambiguity gives `failed`.
- **N4. W provenance.**
  - Exact cancellation of the inside W factors needs two enumerations to give bitwise-identical amplitude and energy_weights for the same primitive. So does the exact zero of unchanged held terms. The two enumerations are whichever one generated the event, and `owner_restricted_channels`.
  - `verify_against_full_enumeration=True` checks this at every restricted call. With False, it is the operator's contract.
  - The setting is the caller's to declare.
- **N5. Missing reverse at a held replay ends the run.** When the Hermitian partner is missing, `_reverse_check` returns status `failed` rather than rejecting. The held primitive's own reverse-reconnection guards still reject through the operator's enumeration (an absent record). So this is stricter than the PALETTE note, never looser.
- **N6. Group-map collisions are handled by the operator.** The binding at L2773-2776 would silently overwrite a colliding slot label. It is safe only because operator v001 `validate_owned_model` rejects repeated or colliding newborn labels (L439-442), and that runs first.
- **N7. Documentation drift.**
  - `CONVENTIONS_0407_V001.md` still describes the v001 API: `extra_diagonal_reads`, with no `palette_parameters` and no callback.
  - The "operator v002 not on disk" statement is stale (see R1).

## LIMITATIONS (ambiguities, recorded literally; no physics or values chosen)

- **Interval density.** PALETTE does not specify an interval density for the palette move. The module reuses the L10 global density, which is state independent and identical in both directions. I accept it as a literal reading.
- **"Reverse condition fails → reject".** I read this as the held primitive's own reverse and predecessor guards, which live in the operator's enumeration. The module additionally treats a missing Hermitian partner as `failed` (N5).
- **"Local partial-map descriptor".** I read it as (kind, owner_id) for the operator v001/v002 text only. I did not verify this for any other operator (N3).
- **"Use label/dependency indices ... frontier".** I read this as the acceleration instruction. MH correctness does not need it, so it is recorded as N2 and is not blocking.
- **Operator properties.** Completeness of the restricted enumeration, Hermiticity and descriptor uniqueness were checked only by reading the operator text, never by execution.
- **No claims made.** This review makes no claim about mixing, acceptance, cost or irreducibility.
