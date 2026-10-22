# REVIEW 0405 A V003: equivalence of the compact Birth store (UNT 0411 item 4)

**Role:** distinct reviewer, not author. I wrote neither V002 nor V003, nor either FIX_DELTA.
**Date:** 2026-10-16. **Method:** static text review only.

- Nothing was imported or executed: not V002, not V003, not the sampler, not module B, and no legacy, UNT, Codex or root module.
- The only code run was `python3 -I -B` (Python 3.9.6) on text copies in my own scratch directory: `ast.parse` plus an in-memory `compile`, an AST signature/constant comparison and a per-scope name check. I also ran `diff -u` and `shasum -a 256`.
- No run, benchmark, numerical case, network access or install took place. The worked examples below were done by hand on paper-sized symbolic graphs.
- `Universal Network Theory` was read only. Of the failure evidence I read only `receipt.json`, `stdout.txt` and the empty `stderr.txt`. I opened no file whose name contains TRIAL, FIT, Newton, FIELD_, ROTATION, MOM1, rotmod or MassModels. That includes the TRIAL recipe and the root worker cited in the receipt.
- For the API reconciliation I grepped, without executing, the text of the sampler V002 (`0d041119…a942a941`) and V003 (`e367f240…6e97721`) and of module B V002 (`173f608d…bb81`). I searched them for private operator names.
- There is no `__pycache__` or `.pyc` in the artifact directory. This file was written by exclusive create, and no other file was modified.

## Binding inputs (sha256 recomputed from bytes; all match)

| file | sha256 |
|---|---|
| 0411 task | 7b102be61d78c22af98ca14f6bcadf867ce025c42509c1bacb216563ba3cf599 |
| owned_parent_operator_v002.py (base) | b5fded4d1272322036748d4d1b4e634a804c1da1ad6717e70e32b4f2a364a94e |
| owned_parent_operator_v003.py (under review; 136,060 B, 2,637 lines) | a04f87954b68bb2dcc5a1af42a465b1d554ed1fc14d9b22d43e05e3e664f7f07 |
| FIX_DELTA_0405_A_V003.md (49,219 B) | 1e8652a854a53e24fe46a6b35755c3e6fe1f710f0c8dc43bd2cececde7cd8638 |
| FIX_DELTA_0405_A_V002.md | 47a96b7623c093c8efe2b78419b427b38fedac6e921d94b03f89d38b530e6d9e |
| FINAL_CHECK_0405_V001.md | af8fffec27657b7a26cfaea66b2803c67758ba77b9e5267f2b8035ca40f7afcd |
| receipt.json | 5c299ce78fbe9bf7447fb5231fe6fa6209697639e6d12732da95799bbf9457c1 |
| stdout.txt | 8c31b32362a2cfedfefa0e33d0371e08209932d062b9087178e1a7cc0c1b3528 |
| stderr.txt (0 bytes) | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| CONTRACT (section 4 read) | fcad9039574f1666af005bb76a231f14b90f0c8dd82acebd2b16ab77941cd642 |

**Failure as recorded.** The receipt shows MEMORY_CAP, exit −9 at 2.693899542 s, with a conservative combined peak of 1,235,435,520 B against a 1,073,741,824 B cap. Sampled RSS rose in steps of about 0.19 GB from 1.3 s onward. stdout ends at "Starting two-chain collective evaluation". This is an allocation failure, not a result.

## Verdict: PASS_WITH_NOTES

V003 is record-for-record equivalent to V002 for every admitted input and every admitted value of the new key. It is also equivalent across cache eviction.

The repair matches 0411 items 1 to 3:

- The context retains edge codes only.
- Eligibility is tested by shifts over the actual cut and child codes, before any mask, target graph or key is built.
- Every candidate, owner, multiplicity, support, weight, amplitude and canonical target is preserved.
- The structural cache is bounded by a validated, required registration key with exact rebuild on eviction.

The only compatibility delta is that new required registration key. It is the form the coding rules allow ("validated registration/caps key … without default").

**Blocking issues: none.**

## Diff reconciliation

- My own `diff -u` V002→V003 has 16 hunks, +185/−85 lines.
- Its body is byte-identical to the diff embedded in FIX_DELTA_0405_A_V003.md (`cmp` after the two header lines).
- **Documentation-only hunks.** The module docstring (l.1-23, 137-142, 225-228), `LIMITATIONS` L11/L14 text (l.329-361, 390-391), and the docstrings of `OwnedModelContext`, `validate_owned_model` and `_owner_birth`.
- **Code hunks:**
  - `_REGISTRATION_KEYS` (l.423-425)
  - `_admit_registration` (l.871-877, 896)
  - `OwnedModelContext.__init__` (l.1015)
  - `_forward_channels` (l.1121-1134)
  - new `_forward_descriptor` (l.1137-1165)
  - `_reverse_channels` (l.1168-1214)
  - new `_reverse_descriptor` (l.1217-1242)
  - `_info_for` (l.1291-1305)
  - the Birth block of `_transitions` (l.1596-1637)
- **Byte-identical to V002:** `_root_cuts`, `_graph_info`, `_admit_key`, `_amplitude`, `_weights`, `_birth_weights`, `_support_labels`, `_owner_id`, `_transition_records`, `_process_row`, `primitive_events`, the build and assembly code, reads and `reference_preparation`.
- **Removed private channel fields:** `cutmask`, `children` (forward) and `pairs`, `starmask`, `newborn_mask` (reverse). In V002 each was read only inside `_transitions` (V002 l.1504-1528). I grepped every `ch["…"]` and `ref[1]["…"]` read in both versions.
- **Downstream readers are unchanged:** `_amplitude` (j), `_birth_weights` (c, j, newborn_at_target, raw_edges, target_edgeset), `_support_labels` (j, cut, root_other, child_edges) and `_owner_id` (j, cut).
- **No consumer reaches the private store.** No caller module accesses `_infos`, `_owner_birth`, `_forward_channels`, `_reverse_channels`, `_transitions`, `_info_for`, or any of the removed fields (grep of sampler V002/V003 and module B V002).

## Equivalence trace (hand)

Notation: codes are nonnegative ints below NA·NB, `2^c = 1 << c`, and `bit_c(x) = (x >> c) & 1`. For c ≥ 0, `x & 2^c ≠ 0` holds iff `bit_c(x) = 1`.

### Cut enumeration, witnesses and deduplication (unchanged code)

- `_root_cuts` (l.1097-1118) is byte-identical. Both bipartition mirrors are covered by `_code_any`.
- Each cut has exactly one edge at the root, (root, rn[k]). The other three edges (w_i, x_i) end at the other neighbours x_i of the root, with distinct w_i ≠ root.
- Unordered cuts are deduplicated per root by `set` and `sorted`.
- Per owner, channels come from root o_j only. So (G, C, j) exists iff o_j ∈ W_G(C), each once. A cut witnessed by several roots gives one channel per witnessing owner, with no multiplicity factor. This is the V002 reading accepted at FINAL_CHECK item 7, and it is untouched.
- **V003 store (l.1129-1134).** `array('q')` is extended with each sorted 4-tuple, in `_root_cuts` order. It is empty when slot j is active, as V002's list was.
- **V003 read-back (l.1602-1603).** `tuple(cuts[i:i+4])` with step 4 restores the same tuple of Python ints in the same order. The codes are below 2^63, and the store length is a multiple of 4 by construction.

### Distinct cut codes (needed for the census identity)

- Each cut edge has as its opposite-part endpoint a different neighbour of the root: rn[k] for the root edge, and x_i for the others. These four neighbours are distinct in a simple graph.
- Bipartite edges are determined by their endpoint pair. So the four codes are distinct, which matches the author's F3.
- Hence `popcount(inc & cutmask) = Σ_k bit_{cut[k]}(inc)`.

### Forward owner guards and census (l.1598-1606 vs V002 l.1502-1504)

- **Witness.** By construction, as above.
- **Slot absent.** The store is empty when the slot is active (l.1130). `not cuts` skips only an empty loop.
- **Donors RR.** V002 tested `((dm >> 2j) & 3) == 3` per channel. V003 hoists it per owner (`!= 3: continue`). It is invariant in the cut loop, so the same channels are selected.
- **Census exactly two.** V002 tested `_popcount(inc & cutmask) == 2`. V003 tests `x[0]+x[1]+x[2]+x[3] == 2` with `x[k] = bit_{cut[k]}(inc)`. By the distinct-codes identity this is the same predicate.
- **Order of construction.** The test runs before `_forward_descriptor`. An ineligible cut builds no mask, child code, target graph or key.
- **Caching unchanged.** `_owner_birth` is still called before the guards, as in V002. Ineligible owners still build (now compact) structure, so the caching behaviour is the same.

### Forward child construction, target and key (l.1137-1165, 1607-1614)

- **Child codes.** For each c in cut order: (u, v) = `_edge_ends(c)` (A end, B end), then `_code(u, b_j)`, then `_code(a_j, v)`. These are V002's expressions in V002's order, so `child_edges[2k]` and `child_edges[2k+1]` are the children of `cut[k]`.
- **Cut mask.** The same OR of 2^c over the cut.
- **Target graph.** V002 computed `(edgeset & ~cutmask) | (2^cu_k | 2^cv_k)` over k. V003 ORs the same eight 2^cc. OR is associative, commutative and idempotent, so the int is identical.
- **Bit copy to both children.** V002 did `new_inc = inc & ~cutmask`, then ORed `cmask_k` when `inc & 2^{cut[k]}`. V003 ORs `2^child[2k] | 2^child[2k+1]` when `x[k]`, and `x[k] = 1` iff `inc & 2^{cut[k]} ≠ 0`. Identical int.
- **Newborn R with p = q = 0.** The target keeps p, q and s unchanged. a_j and b_j are absent in the source, and `_admit_key` forbids p|q|s bits on absent vertices, so the newborns enter in R with p = q = 0. Unchanged.
- **Donors RR→II.** `dm & ~(3 << 2j)`. Unchanged.
- **Slot.** `slots | 2^j`. Unchanged.
- **Canonical target key.** `(slots|2^j, target, new_inc, p, q, s, dm&~(3<<2j))`. Every field is an identical int.
- **Other fields.** `root_other` (`port_codes[root]` minus cut), `raw_edges`, `j`, `cut`, `newborn_at_target=True` and `c=None` use V002's expressions.

### Reverse graph-level guards (l.1168-1214; logic unchanged)

The early returns are unchanged:

- slot j inactive;
- **a_j ~ b_j exclusion:** `a_new in u_side` returns empty.

The 4! pairings are walked in `permutations` order with these tests unchanged:

- **Duplicate-edge test:** any restored code already in edgeset is rejected.
- **Predecessor owner witness:** both branches, o in A and o in B, the `pred == set(v_side)` / `set(u_side)` tests, and `root_other`.

What changed:

- Removed: the per-owner `starmask` and the per-pairing `restmask`, child tuple and dict.
- Each survivor now appends `(pairs, root_other)`, where `pairs = ((star_ub[i], star_av[σ(i)], restored[i]))_i` is V002's own `pairs` tuple.
- **Predecessor simple q4.** It is still implied as in V002. The restored codes are distinct because u_side is distinct. They are absent from G by the duplicate test. Every u ∈ u_side and v ∈ v_side trades its newborn edge for exactly one restored edge, and a_j, b_j lose all four edges.

### Reverse state-level guards (l.1615-1630 vs V002 l.1511-1526)

- **Donors II.** V002 skipped per candidate when `(dm >> 2j) & 3` was nonzero. V003 hoists this per owner (loop-invariant). `not cands` skips only an empty loop.
- **Ready with p = q = 0.** V002 tested `(p|q|s) & (2^{a_j} | 2^{b_j})`, which is nonzero iff `bit_{a_j}(pqs)` or `bit_{b_j}(pqs)` (a_j ≠ b_j). V003 tests exactly that, hoisted, on NV-bit vertex ints.
- **Equal paired child bits.** Both walk the pairs in order and stop at the first k with `bit_{ub_k}(inc) ≠ bit_{av_k}(inc)`. V002 set `equal = False`. In V003 `len(x) < 4` holds exactly when that stop occurred.
- **Census two.** V002 tested `census == 2` with census = Σ `bit_{ub_k}`. V003 tests `x[0]+…+x[3] == 2` with the same summands. The `or` short-circuits, so the sum is read only when `len(x) == 4`.
- These tests run before `_reverse_descriptor`, so an ineligible pairing builds nothing.

### Reverse descriptor, target and key (l.1217-1242, 1631-1637)

- **Star mask.** It is the OR over the four pairs of `2^{ub} | 2^{av}`. The ub are star_ub. The av are star_av permuted by σ, a bijection. So the bit set is star_ub ∪ star_av, which is V002's starmask.
- **Restored mask and cut.** `restmask` is the OR of `2^{rc_i}`, and `cut = tuple(sorted(rc_i))`. Both equal V002's.
- **child_edges.** `sorted([ub_0, av_0, …, ub_3, av_3])` is the same multiset as `star_ub + star_av`, so it gives V002's sorted tuple. The eight codes are distinct because (a_j, b_j) is excluded, though only multiset equality is needed.
- **Target.** `(edgeset & ~starmask) | restmask` with equal operands.
- **New incidence.** V002 built `inc & ~starmask` and ORed `2^{rc_k}` for each `x_k = 1`. V003 does the same with `pairs[k][2] = rc_k`. Identical.
- **Key.** `(slots & ~2^j, target, new_inc, p, q, s, dm | (3<<2j))`. This restores RR and removes exactly slot j's newborns. Unchanged.
- **Other fields.** `root_other`, `raw_edges`, `newborn_at_target=False` and `c=None` use V002's expressions.

### Records, amplitudes, supports, weights and multiplicity

- `_transitions` returns the same `(kind, ref-fields, target)` triples, in the same order: native records, then forward records by scope owner and stored cut order, then reverse records by scope owner and permutation order.
- **Amplitude.** `_amplitude` reads only `ch["j"]`: ε_j forward and its conjugate in reverse. Unchanged.
- **Supports and owner_id.** These read j, cut, root_other and child_edges, which are equal. The forward and reverse `cut` are the same sorted code tuple, so the forward/reverse owner_ids still coincide.
- **Endpoint-mean weights.** `_birth_weights` is byte-identical. It is a pure function of (source edgeset = `info["edgeset"]` = `key[1]`, `target_edgeset`, `raw_edges`, the newborn pair, the donors, the registration).
  - V002 cached `c` on the retained dict, whose graph was fixed, so the cache always held this same value.
  - V003 recomputes it on the transient dict. The arithmetic is identical: `_weights` counts integer anchors, then divides and sorts by cell.
  - A missing `edge_cells` entry raises at the same point in both versions, because a failing value was never cached.
- **Multiplicity.** One record per eligible (G, C, j) or pairing. Nothing is added, merged or dropped.
- **Not exposed.** The dict is never part of a `_Channel` or `_IndexedEvent`, so its transience is invisible to callers.

### Cache eviction and exact recomputation (l.1291-1305)

- **Policy.** On each call the entry is popped and reinserted, so dict order is use order. While the length exceeds the bound, the first key, the least recently used, is deleted.
  - The key just inserted is last and the bound is at least 1, so it is never the one evicted.
  - If `_graph_info` raises, nothing is inserted.
- **Call sites.** There are only three: `_admit_key` (l.1438), `_process_row` (l.2089) and `primitive_events` (l.2451). Each public call obtains exactly one info and keeps its own reference. An eviction during the call therefore cannot affect it; later writes go to the orphaned dict.
- **Rebuild is exact.** `_graph_info` is deterministic in the edgeset, the validated dom and `ctx._ports`, which is never evicted, so port codes are identical without re-invoking `port_order`. The other parts follow:
  - `_owner_birth` depends only on dom, `nbrs`, `edgeset` and `slots_mask`.
  - `w_edge`/`w_deg` come from pure `_weights`.
  - `coverage_ok` restarts empty, so `_require_coverage` re-checks. Map profiles are pure. Accessor values come from `ctx._edge_values`, which is not evicted, so there is no re-invocation. A failing accessor was never cached in either version.
  - The same failures, and the same messages, arise in both versions.
- **Result.** Records after any eviction pattern equal V002's.
- **release_caches()** still drops all three caches (l.1024-1028). After it, the L5/L8 determinism requirement on `port_order` and the accessors applies, unchanged.

## Worked symbolic examples (by hand, nothing executed)

**Domain.** graph0 = K_{4,4} with A originals at vids 0-3 and B originals at vids 12-15 (the `_admit_graph0` layout). Then:

- K = 8, NA = NB = 12, and `code(a, b) = 12a + (b − 12)`.
- Owner j = 0 has o = 0, a_0 = 4 and b_0 = 16.

**Forward, k = 0, matching (1, 2, 3).**

- Cut edges: (0,12), (1,13), (2,14), (3,15), with codes (0, 13, 26, 39), distinct.
- Children in cut order: (0,16)=4, (4,12)=48, (1,16)=16, (4,13)=49, (2,16)=28, (4,14)=50, (3,16)=40, (4,15)=51. So `child_edges = (4,48,16,49,28,50,40,51)`.
- Take inc with bits 0 and 26 among the cut codes:
  - **V002:** `popcount(inc & (2^0|2^13|2^26|2^39)) = 2`. It sets `new_inc = inc & ~cutmask | (2^4|2^48) | (2^28|2^50)`.
  - **V003:** x = [1, 0, 1, 0], sum 2. k = 0 adds child[0], child[1] = 4, 48. k = 2 adds child[4], child[5] = 28, 50. Same int.
- **Target.** Both give K_{4,4} − {0,13,26,39} + {4,16,28,40,48,49,50,51}. b_0 is adjacent to 0-3, a_0 is adjacent to 12-15, and every original still has degree 4.
- **Second mirror.** Root 12 (owner j = 4, o = 12 ∈ B) also generates the cut (0,13,26,39): k with rn[k] = 0, matching (13, 14, 15). So (G, C, 0) and (G, C, 4) are two distinct channels, each once, with children at a_4 = 8 and b_4 = 20. Both versions agree.

**Reverse from that target (slot 0 active).**

- u_side = (0,1,2,3), v_side = (12,13,14,15). a_0 = 4 is not in u_side.
- star_ub = (4,16,28,40) and star_av = (48,49,50,51).
- **σ = id.** Restored = (0,13,26,39), none present. The witness test holds: o = 0 has neighbours (13,14,15,16), and {13,14,15} ∪ {12} = v_side. root_other = (1,2,3).
- **Other σ.** Every other σ is rejected by the duplicate-edge test. In G′, original i keeps every B neighbour except 12+i, so any σ ≠ id restores some (i, v) that is already present. Both versions keep only σ = id.
- **Bits.** Pairs (4,48), (16,49), (28,50), (40,51) carry equal bits (1,1), (0,0), (1,1), (0,0), so the census is 2.
- **Result.** new_inc = inc′ & ~(star bits) | 2^0 | 2^26, which is the source inc. The target is the K_{4,4} edgeset. Donors are RR and slot 0 is cleared.
- **Descriptor.** child = sorted(4,48,16,49,28,50,40,51) = V002's sorted(star_ub + star_av). cut = (0,13,26,39), the forward cut, so the owner_id matches.
- **Failure cases.** Flipping bit 48 alone makes pair 0 unequal. V002 sets `equal = False`, and V003 has `len(x) = 0`, so neither gives a record. Setting bits on pairs 0, 1 and 2 with equal partners gives census 3, and neither version gives a record.

## Public API reconciliation

- **Signatures.** My AST comparison of V002 and V003 found these identical: the public module function signatures (8 functions, all keyword-only, no defaults), every class method signature of `OwnedModelContext` and `OwnedParentOperator`, the `_Channel`/`_IndexedEvent` fields, and the imports. No public name was added or removed.
- **Module constants.** The only differences are `LIMITATIONS`, whose text is documentation, and `_REGISTRATION_KEYS`, which gains `"max_cached_graphs"`.
- **Record formats, `resources()` and exceptions.** Unchanged, apart from the new validation failure.
- **Input-schema delta (accepted).** `registration['max_cached_graphs']` is required.
  - Missing: `_keyset` gives "missing required keys ['max_cached_graphs'] (no defaults)".
  - Bad value (bool, non-integer or < 1): a named failure (l.871-877).
  - The value is stored as `int` and read by `OwnedModelContext`.
  - This is exactly the "validated registration key without default" the coding rules permit. Registration, not caps, is the right place, because the state-level path used by the sampler never sees caps.
  - The sampler passes `registration` unchanged to `validate_owned_model`, and neither consumer builds a registration internally. Only root's binding must add one positive integer. Until it does, validation fails closed, as with V002's `whitening`.

## Remaining costs (author's report checked)

My own arithmetic agrees with FIX_DELTA "Remaining costs". It uses CPython 30-bit digits, NA·NB = 36,864 at L4 and 2,359,296 at L8, and 13,824 / 110,592 structural forward cuts per graph.

- **Retained per cached graph.** Forward store 32 B/cut, about 0.44 MB at L4. Reverse is at most 6 pairings per active owner: the witness forces σ(i0), leaving 3!, as confirmed in the trace. With O(V+E) structure the total is about 0.5–1.5 MB per graph at L4, times `max_cached_graphs`.
- **V002 for comparison.** About 20 KB per forward candidate × 13,824, or about 0.28 GB per fully enumerated L4 graph, accumulated across graphs. This is consistent in order with the receipt's ~0.19 GB RSS steps. It is not a reconstruction of them.
- **Still present per call.**
  - Every eligible Birth record keeps two O(NA·NB)-bit key ints (target edgeset and new_inc), its labelled supports and a transient descriptor dict in the `_transitions` list. This is about tens to ~100 MB per full-scope L4 call, and O(10^10) B per full-scope call at L8, still infeasible.
  - Native flip keys: one inc per scope edge.
  - Four census shifts per structural cut: allocation churn, not peak.
  - Birth weights are recomputed per eligible record.
  - A rebuild after eviction re-pays `_bits(edgeset)` and the on-demand C_loc.
  - The `_ports` and `_edge_values` caches are not bounded.
  - All of these are disclosed in L11 (d)/(e) and the FIX_DELTA. V003 removes cross-graph accumulation, not the within-call output peak. Like the author, I make no claim that the next L4 attempt fits or mixes.

## Notes (non-blocking)

1. **Census-shift sizes understated.** The FIX_DELTA gives census-shift temporaries as "≤ 1.6 KB" at L4 and "≤ 105 KB" at L8. That holds for graphs whose incidence stays in the G0 code range. Once any slot is active, inc can contain (a_j, v) codes, up to about 4.9 KB at L4 and about 315 KB at L8 (the full-range figures in its own table). This affects only the churn estimate, not peak or correctness.
2. **Port-order cache still grows.** `ctx._ports` gains entries for the neighbourhoods changed in each new graph: at most ten vertices per Birth (eight cut endpoints and two newborns). Only `release_caches()` clears it, and that is disclosed. If root keeps its per-enumeration `release_caches()`, `max_cached_graphs` bounds only within-call structure. If root drops it to benefit from the LRU, `_ports` grows slowly with distinct graphs visited. Either way records are unchanged.
3. **Stale usage note.** USAGE_NOTE_0405_V001.md lists the V002 registration keys and does not mention `max_cached_graphs`. Root's binding and any usage text must add the key. This is not a V003 code defect.
4. **Untested.** V003 has never been executed, by its author or by me. This review establishes static equivalence only.

## AST results (mine; text copies in scratch, `python3 -I -B`, 3.9.6)

| check | V002 | V003 |
|---|---|---|
| parse + in-memory compile | OK | OK |
| top-level node types | docstring Expr (l.1 only), Import/ImportFrom, Assign, FunctionDef, ClassDef | same |
| `@`, `.dot/.matmul/.vdot/.inner/.tensordot`, print/open/exec/eval/`__import__` | none | none |
| `einsum` without `optimize=False` | none | none |
| public module functions keyword-only, no defaults | 8/8 | 8/8 |
| imports | — | identical to V002 (`array` already imported) |
| unresolved names in changed functions (`_admit_registration`, `_forward_channels`, `_forward_descriptor`, `_reverse_channels`, `_reverse_descriptor`, `_owner_birth`, `_info_for`, `_transitions`) | — | none |

## Attestation

I am the distinct equivalence reviewer for V003. I did not author V002, V003, either FIX_DELTA or the usage note. Nothing was imported or executed. Static text operations ran only from my scratch directory. No file in the artifact directory or under `Universal Network Theory` was modified, moved, deleted or chmod-ed. This review was written by exclusive create.
