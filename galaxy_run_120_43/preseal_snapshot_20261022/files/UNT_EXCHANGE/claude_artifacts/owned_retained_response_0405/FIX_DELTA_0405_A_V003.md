# FIX DELTA 0405 module A: owned_parent_operator v002 -> v003 (UNT 0411 compact Birth candidates)

**Role:** author of V003. **Date:** 2026-10-16. **Method:** static only.

- Nothing was imported or executed: not V002, not V003, and no legacy, UNT, Codex or root module.
- The only code run was `python3 -I -B` (Python 3.9.6) on file TEXT from my scratch directory: `ast.parse` plus an in-memory `compile`, an AST signature comparison, `diff` and `shasum`.
- No `__pycache__` exists in the artifact directory.
- No run, benchmark, numerical case, network access or install took place.
- Access to `Universal Network Theory` was read-only. From its failure evidence I read only `receipt.json`, `stdout.txt` and the empty `stderr.txt`. No file whose name contains TRIAL, FIT, Newton, FIELD_, ROTATION, MOM1, rotmod or MassModels was opened, including the TRIAL recipe cited in the receipt.
- V002 is unchanged. V003 and this file were written by exclusive create (`open(path, "xb")`).
- V003 is **UNTESTED**: it has never been executed.

## Files and binding inputs (sha256 computed from bytes)

| file | bytes | lines | sha256 |
|---|---|---|---|
| owned_parent_operator_v002.py (base, unchanged) | 128154 | 2528 | b5fded4d1272322036748d4d1b4e634a804c1da1ad6717e70e32b4f2a364a94e |
| owned_parent_operator_v003.py (new) | 136060 | 2637 | a04f87954b68bb2dcc5a1af42a465b1d554ed1fc14d9b22d43e05e3e664f7f07 |

All binding inputs matched their pins:

- Task 0411: 7b102be61d78c22af98ca14f6bcadf867ce025c42509c1bacb216563ba3cf599
- Failure receipt.json: 5c299ce78fbe9bf7447fb5231fe6fa6209697639e6d12732da95799bbf9457c1
- stdout.txt: 8c31b32362a2cfedfefa0e33d0371e08209932d062b9087178e1a7cc0c1b3528
- stderr.txt: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 (0 bytes)
- CONTRACT: fcad9039574f1666af005bb76a231f14b90f0c8dd82acebd2b16ab77941cd642. Section 4 was read; it is unchanged by V003.
- FIX_DELTA_0405_A_V002.md: 47a96b7623c093c8efe2b78419b427b38fedac6e921d94b03f89d38b530e6d9e. FINAL_CHECK_0405_V001.md: af8fffec27657b7a26cfaea66b2803c67758ba77b9e5267f2b8035ca40f7afcd. Both were read; their pins match FINAL_CHECK section 1 and the receipt.

**Failure as recorded.** Status FAILED_OR_INCOMPLETE, stop_reason MEMORY_CAP, exit -9 at 2.693899542 s. Conservative combined peak was 1,235,435,520 bytes against a 1,073,741,824-byte cap. Sampled RSS rose in steps of about 0.19 GB from 1.2 s onward. stdout ends at "Starting two-chain collective evaluation". No estimate was returned. This is an allocation failure, not a physical or mixing result.

## What changed (and nothing else)

The Birth candidate store now keeps only edge codes, and every eligibility test runs before any mask, target graph or key is built. The per-graph structure cache is bounded by a declared, validated registration key. Diagonal, native, read, weight, amplitude, support, key, build, assembly, operator and reference-family code is byte-identical to V002. The only other changes are documentation.

### Change map (V003 line numbers)

| # | V003 lines | V002 lines | change |
|---|---|---|---|
| 1 | 1-18 | 1 | Module docstring: new V003 STATUS paragraph. The V002 status is kept verbatim under "V002 STATUS". |
| 2 | 137-142 | 120-123 | Birth semantics paragraph: one V003 sentence added (cache holds codes only), then reflowed. The text is otherwise unchanged. |
| 3 | 225-228 | 206 | COST: V003 memory sentence. |
| 4 | 329-361 | 307-321 | L11: the cache bound and its semantics; (d) narrowed to the unbounded port/accessor caches; new (e) on V003 transient costs. |
| 5 | 390-391 | (after 349) | L14: the root binding must also pass `max_cached_graphs`. |
| 6 | 424-425 | 381-382 | `_REGISTRATION_KEYS` gains `"max_cached_graphs"`. |
| 7 | 871-877, 896 | (after 827), 846 | `_admit_registration`: validation of `max_cached_graphs` (int or numpy integer, not bool, at least 1; fail closed with a message naming it). The admitted value is stored as `reg["max_cached_graphs"]`. |
| 8 | 1007-1008, 1015 | 957 | `OwnedModelContext`: docstring, and `self._max_graphs` read from the admitted registration. |
| 9 | 1048-1050 | 996 | `validate_owned_model` docstring lists the new key. |
| 10 | 1121-1134 | 1067-1098 | `_forward_channels`: compact store, a flat `array('q')` of the four sorted codes of each cut, in V002 order. |
| 11 | 1137-1165 | (new) | `_forward_descriptor`: transient V002 channel dict plus the transient cut mask, built only for an eligible forward channel. |
| 12 | 1168-1214 | 1101-1157 | `_reverse_channels`: the graph-level tests are unchanged. It stores `(pairs, root_other)` per surviving pairing. Removed: starmask/restmask/child/dict construction. |
| 13 | 1217-1242 | (new) | `_reverse_descriptor`: transient V002 channel dict plus the transient star mask, built only for an eligible pairing. |
| 14 | 1246 | 1161 | `_owner_birth` docstring only. |
| 15 | 1291-1305 | 1206-1211 | `_info_for`: bounded LRU over graphs (pop/reinsert; drop the oldest beyond the bound). |
| 16 | 1596-1637 | 1502-1528 | `_transitions` Birth/reverse block: hoisted loop-invariant guards; census and pair tests by shifts over the cached codes before any construction; descriptors and target keys built only for eligible channels. |

The private fields removed from the channel dicts are `cutmask`, `children`, `pairs`, `starmask` and `newborn_mask`. In V002 they were read only inside `_transitions` (grep-verified: no other reference in V002 or V003).

The fields read downstream are unchanged in name and value:

- `j`, `cut`, `child_edges`, `root_other`, `target_edgeset`, `newborn_at_target`, `raw_edges`, `c`.
- They are read by `_owner_id` (j, cut), `_support_labels` (j, cut, root_other, child_edges), `_amplitude` (j) and `_birth_weights` (c, j, newborn_at_target, raw_edges, target_edgeset). All four functions are byte-identical to V002.

## Equivalence argument for every changed mask/code operation and guard

Notation: a code c is a nonnegative int below NA*NB. `2^c` means `1 << c`. For ints, `(x >> c) & 1` is bit c of x.

### Forward (owner j with slot absent, current graph G)

**F1. Candidate set and order.**
- V002 created one dict per element of `_root_cuts(dom, nbrs, o_j)`. That is a sorted list of sorted 4-tuples, deduplicated as unordered cuts. V003 appends the same tuples, in the same order, to `array('q')` (V003 l.1132-1133).
- `tuple(cuts[i:i+4])` (l.1603) rebuilds each tuple exactly: `'q'` stores every int below 2^63 exactly.
- Nothing is filtered at store time. Slot j active gives no candidates in both versions (l.1130).
- `_root_cuts` is unchanged. So the cut deduplication, the witness rule and "each (G, C, j) once" are unchanged.

**F2. Donor guard (l.1600).**
- V002 evaluated `((dm >> 2j) & 3) == 3` per channel. dm and j are loop-invariant, so hoisting it to the owner (`!= 3: continue`) selects the same channels.
- `_owner_birth` is still called first, as in V002, so caching is unchanged. The `not cuts` test only skips an empty loop.

**F3. Census (l.1604-1605).**
- V002 tested `_popcount(inc & cutmask) == 2` with cutmask the OR of `2^c` over the four cut codes.
- The four codes are distinct. In `_root_cuts` the cut edges are (root, rn[k]) and (w_i, x_i), with rn[k] and the x_i the four distinct neighbours of the root in a simple graph. Each edge therefore has a distinct opposite-part endpoint.
- So `popcount(inc & cutmask) = sum over c of ((inc >> c) & 1)`, which is exactly `x[0]+x[1]+x[2]+x[3]`. Same predicate.
- It is evaluated before `_forward_descriptor`, so an ineligible cut builds no mask, child code, target graph or key.

**F4. Child codes (l.1149-1154).** Same expressions as V002: for (u, v) = `_edge_ends(c)`, `_code(u, b_j)` then `_code(a_j, v)`, appended in cut order. So `child_edges[2k]` and `child_edges[2k+1]` are the children of `cut[k]`, exactly as in V002.

**F5. Cut mask and target graph (l.1151, 1155-1157).**
- V002: `target = edgeset & ~cutmask`, then `target |= (2^cu | 2^cv)` per cut edge.
- V003: the same `edgeset & ~cutmask` (same cutmask), then `target |= 2^cc` for each of the eight child codes.
- OR is associative, commutative and idempotent, so the int is identical.

**F6. New incidence (l.1609-1612).**
- V002: `new_inc = inc & ~cutmask`, then `if inc & 2^c: new_inc |= 2^cu | 2^cv` per cut edge.
- For c >= 0, `inc & 2^c != 0` iff `(inc >> c) & 1 == 1`, which is `x[k]`, computed on the same `inc` and the same `cut[k]`.
- V003 ORs `2^child[2k] | 2^child[2k+1]`, which is the V002 cmask of `cut[k]` by F4. Identical int.

**F7. root_other, raw_edges, cut, j, newborn_at_target, c (l.1158-1164).**
- Same expressions as V002. `c not in cut` is tested on a tuple with equal values.
- `raw_edges` is `sorted(set(cut) | set(root_other) | set(child_codes))`.
- `c` starts as None. `_birth_weights` (unchanged) then computes `(w(source) + w(target))/2` from `info["edgeset"]`, `target_edgeset`, `raw_edges`, the newborn pair and the donors, which are V002's inputs.
- V002 cached that value on the retained dict. It is a pure function of the same inputs, and the source graph is fixed per info, so the recomputed value is identical. Only the cost changes (residual (e) below).

**F8. Record (l.1613-1614).** Same kind `birth`, ref `("birth", ch)`, and key `(slots | 2^j, target, new_inc, p, q, s, dm & ~(3 << 2j))`. The order is owners in scope order, then cuts in stored order (V002 order). Each eligible cut gives exactly one record: no multiplicity factor and no extra record.

### Reverse (owner j with slot active, current graph G)

**R1. Candidate set and order (l.1168-1214).**
- The V002 loop body is unchanged up to `pairs`: the restored codes, the duplicate-old-edge test by shifts on `edgeset`, both witness/predecessor branches, and `root_other`.
- Only the dict construction and the per-owner starmask are removed. V003 appends `(pairs, root_other)` for the same surviving permutations, in `permutations(range(4))` order.
- Early returns (slot inactive; a_j adjacent to b_j) are unchanged.

**R2. Donor guard (l.1617).** V002 skipped per candidate when `(dm >> 2j) & 3` is nonzero. That is loop-invariant, so it is hoisted per owner. `not cands` only skips an empty loop.

**R3. Newborn Ready guard (l.1619-1621).**
- V002 skipped when `(p|q|s) & ((1 << a_j) | (1 << b_j))` is nonzero. Since a_j != b_j, that holds iff bit a_j or bit b_j of `pqs = p|q|s` is set.
- V003 tests exactly `(pqs >> a_j) & 1 or (pqs >> b_j) & 1`. It is loop-invariant, so it is hoisted. These are vertex ints of NV bits, not edge-space ints.

**R4. Paired child bits and census (l.1622-1630).**
- V002 walked the pairs in order. It set `x = (inc >> ub) & 1` and stopped (equal = False) when x differed from `(inc >> av) & 1`. Otherwise it summed the census. It was eligible iff it did not stop and census == 2.
- V003 performs the same shifts on the same codes in the same order and appends each equal bit. "Did not stop" is then `len(x) == 4`, and the census is `x[0]+...+x[3]`. Same predicate.
- It is evaluated before `_reverse_descriptor`, so an ineligible pairing builds nothing. (V002 also built `inc & ~starmask` for every candidate before testing; that had no effect on the output.)

**R5. Star mask (l.1231).**
- V002 OR-ed `2^c` over `star_ub + star_av`. V003 ORs `2^ub | 2^av` over the four pairs.
- The ub_i are `star_ub[i]` for i = 0..3. The av_i are `star_av[sigma(i)]`, and sigma is a bijection, so as a set they are star_av.
- Same set of bits, so the same int.

**R6. Restored mask and cut (l.1232, 1237).** rc_i = restored[i] in i order. So the OR over rc_i equals V002's restmask, and `tuple(sorted(restored))` equals V002's cut.

**R7. child_edges (l.1233-1235).** `star = [ub_0, av_0, ..., ub_3, av_3]` is the multiset `star_ub ∪ star_av` (8 codes; they are distinct because a_j is not in u_side). `tuple(sorted(star))` equals V002's `tuple(sorted(star_ub + star_av))`.

**R8. Target graph (l.1238).** `(info["edgeset"] & ~starmask) | restmask` is the V002 expression with equal operands (R5, R6).

**R9. New incidence (l.1632-1635).**
- V002 built `inc & ~starmask`, then OR-ed `2^rc_i` for each i with x_i = 1, with all four i processed when eligible.
- V003 builds `inc & ~starmask`, then ORs `2^pairs[k][2]` (that is rc_k) for x[k] = 1. Identical.

**R10. raw_edges, root_other, newborn_at_target, c, record.**
- Same expressions and values as V002. `_birth_weights` is unchanged with identical inputs, as in F7.
- The record kind is `birth_rev` with key `(slots & ~2^j, target, new_inc, p, q, s, dm | (3 << 2j))`. Order: owners in scope order, then pairings in permutation order.
- A failed pairing still gives no record, and native owners still act on every state (unchanged code).

### Consequences

**Records.** `primitive_channels`, `palette_channels`, `diagonal_terms`, `OwnedParentOperator.primitive_events` and the build (`_process_row`) receive identical `(kind, ref-fields, target)` triples in identical order. They therefore emit identical records: owner_id, kind, target key, amplitude, queried/changed supports, energy weights and order.

**Model quantities preserved.**
- Every legal forward and reverse candidate is kept.
- The deduplication rule, owner and primitive multiplicity (none) are unchanged.
- Support, endpoint-mean allocation, amplitude and canonical target are unchanged.
- There is no cut sampling, truncation or graph restriction.

**Build.** The stored H, every E_alpha, the norm bounds and the integrity checks are unchanged.

## Cache bound and control semantics

**Control.**
- The control is the new REQUIRED registration key `max_cached_graphs`: a positive integer (Python int or numpy integer; bool rejected). There is no default.
- If it is missing, `validate_owned_model` fails closed with `registration: missing required keys ['max_cached_graphs'] (no defaults)`.
- A bad value fails with `registration['max_cached_graphs']: a positive integer is required, got ...`.
- It is a resource control only. Records are identical for every admitted value.

**What is bounded.**
- `ctx._infos`: the per-graph structure keyed by the graph's edgeset int.
- That structure covers neighbours, port codes, presence, the slot mask, coverage flags, the native weight caches `w_edge`/`w_deg`, and the compact Birth store `birth`.

**Policy: least recently used, in `_info_for` (l.1291-1305).**
- Every access pops and reinserts the graph, making it most recent.
- After the access, while the count exceeds the bound, the oldest graph is deleted.
- The graph just accessed is never the one evicted, because it is last and the bound is at least 1.

**When an access happens.**
- On every state admission: `canonical_state_key`, `state_labels`, `diagonal_terms`, `primitive_channels`, `palette_channels`, `read_rows`, and `OwnedParentOperator.index_of`.
- In the build: on admission of seeds and on every processed row.
- On `OwnedParentOperator.primitive_events`.
- No function holds two graphs at once. A caller's local `info` reference stays valid for the rest of its call even if that graph is evicted later.

**Exact recomputation.**
- An evicted graph is rebuilt on its next use by the same `_graph_info` and on-demand `_owner_birth`.
- Every cached field is a deterministic function of the edgeset, the validated inputs, and the port orders and edge values held in `ctx._ports`/`ctx._edge_values`. Those two caches are not evicted, so eviction never re-invokes a caller callable for an already admitted value.
- A failing port_order or accessor is never cached, in V002 or V003, so it is re-invoked on the next check either way.
- `release_caches()` is unchanged: it drops all three caches. After it, the registered port_order and accessors are re-invoked and must be deterministic (L5, L8; unchanged requirement).

**What is not bounded.**
- `ctx._ports` (per vertex and current neighbour set) and `ctx._edge_values` (per stable edge) are not bounded. They grow by a handful of entries per new graph: a Birth changes the neighbour sets of at most 11 vertices and adds 8 edges. Only `release_caches()` clears them.
- The build's own bookkeeping (`run["graphs"]`, `run["keys"]`) is V002 behaviour and is bounded by its caps.

**Implications of the declared value.** These are facts, not a recommendation; no value is chosen here.

| Declared value | Effect |
|---|---|
| 1 | Keeps only the graph of the latest call. A step that evaluates x then a Birth proposal y and returns to x rebuilds x's structure. |
| 2 | Keeps the current graph and one other. |
| Larger | Fewer rebuilds. Memory grows linearly in the value, by the per-graph sizes below. |

A build whose structural component has more graphs than the bound rebuilds a graph's structure when a row of an evicted graph is processed. This is exact, only slower.

**Root's per-enumeration `release_caches()` mitigation** remains compatible and harmless. With V003 it is no longer needed to bound graph structure. It still clears the port and accessor caches, at the price of rebuilding everything per call.

**No general cache framework.** The cache is one dict and seven lines in `_info_for`.

## Public API compatibility

- **Signatures.** An AST comparison of V002 and V003 covers public module functions with positional and keyword-only argument names, every class method signature, the NamedTuple record fields (`_Channel`, `_IndexedEvent`) and the public constants: 42 items, identical. The 23 public callables are keyword-only with no defaults (unchanged).
- **Outputs.**
  - Record formats and contents are unchanged (equivalence above).
  - `resources()` keys and values are unchanged.
  - Exceptions are unchanged except that a missing or bad `max_cached_graphs` now fails at validation.
  - `LIMITATIONS` is unchanged except for documentation text.
- **Input schema (the one compatibility delta).** `registration` must contain `max_cached_graphs`. Root's current binding (adapter `build_inputs` plus the recipe that adds `whitening` and frames) will fail closed, naming the key, until it adds one positive integer. This is the same pattern as V002's required `whitening`.
- **Internal construction.** `OwnedModelContext(*, dom, model, reg)` now reads `reg["max_cached_graphs"]`. It is built only by `validate_owned_model`. Direct construction from a hand-made internal dict is not a supported path, as before.
- **Unreachable failure.** `array('q').extend` would raise OverflowError only for a code of 2^63 or more, which needs NA*NB > 9.2e18. That is unreachable.

## Remaining costs, with honest orders of magnitude

These are arithmetic estimates from CPython 3.9 int layout (24 + 4·ceil(bits/30) bytes). They are not measurements: nothing was run.

Geometry from the module's own figures: V0 = 2L^3, K = V0, and NA = NB = 1.5 V0.

| Quantity | L=4 | L=8 |
|---|---|---|
| V0 | 128 | 1024 |
| NA·NB | 36,864 codes | 2,359,296 codes |
| Full-range edge int | about 4.9 KB | about 315 KB |
| G0 edgeset int (max code 63·192+63) | about 1.6 KB | about 105 KB |
| Birth target / new incidence int (child codes reach the a_j rows) | about 3–5 KB | about 0.1–0.3 MB |
| Structural forward candidates per graph (108 per absent owner) | 13,824 | 110,592 |

### Retained per cached graph

| | L=4 | L=8 |
|---|---|---|
| **V002**, mask-rich dict per forward candidate | about 20 KB per candidate (cutmask, 4 cbits, 4 two-bit child masks reaching the a_j rows, target, dict), so roughly 0.2–0.4 GB per fully enumerated G0-like graph. This is the same order as the receipt's ~0.19 GB RSS steps, not a reconstruction of them. It accumulated per distinct graph. | about 1.3 MB per candidate, about 1.5e11 B per graph (infeasible) |
| **V003** forward store (32 B per cut) | about 0.44 MB | about 3.5 MB |
| **V003** reverse store (≤ 6 surviving pairings per active owner: the witness test forces the owner's partner, leaving 3! = 6; about 0.65 KB each) | ≤ about 0.5 MB | ≤ about 4 MB |
| **V003** other structure: O(V+E) neighbours/ports/codes, native weight caches and the key int | about 0.1–0.3 MB | about 2–5 MB |

**V003 total retained** is at most `max_cached_graphs` × (about 0.5–1.5 MB at L4, about 5–15 MB at L8), plus the slowly growing port and accessor caches.

### Transient per full-scope `primitive_channels` call (present in V002 too, unless marked V003)

**(i) Census shifts.** 4 shifts of `inc` per structural cut. Each allocates a temporary int of up to the size of `inc` and frees it at once, so the peak is +1 temporary.
- L4: 55,296 shifts of ≤ 1.6 KB.
- L8: 442,368 shifts of ≤ 105 KB, about 2e10 B of allocation churn in total. That is time, not peak.
- V002 instead did one AND per cut plus `bin()` string popcount, which is heavier.

**(ii) Eligible Birth records.** The number of cuts with census exactly two is state-dependent. As an illustration only, with independent fair bits it is 6/16, about 5×10^3 at L4 and about 4×10^4 at L8.
- Each eligible record keeps two O(NA·NB)-bit key ints (target, new_inc). It also keeps the labelled record: owner_id with 4 edge labels, 9 queried and 16 changed labelled anchors, and a dense energy-weight tuple of 8·n_cells + 56 B.
- Before records are built, the internal `_transitions` list also holds one descriptor dict (about 1.2 KB) per eligible record, plus transient mask/OR temporaries, each freed at once.
- **L4:** about 10–15 KB + 8·n_cells B per record, so O(10^1–10^2) MB per call.
- **L8:** about 0.2–0.6 MB per record, so O(10^10) B per call. Full-scope `primitive_channels` at L8 therefore remains infeasible on its output alone, unchanged from V002.
- **Palette call at L8:** per palette owner ≤ 108 cuts (≤ 432 census shifts) and ≤ 108 eligible records, about 0.2–0.6 MB each, so ≤ about 65 MB at the all-eligible bound and about 25 MB at the illustrative 6/16. Reverse ≤ 6 per active palette owner.

**(iii) Native flip keys (unchanged).** One new `inc` int per scope edge (2V0 edges in G0).
- L4: about 256 × 1.6 KB, about 0.4 MB.
- L8: about 2048 × 105 KB, about 0.2 GB per full-scope call.
- Hop, bind and admit keys reuse `inc`/`edgeset`, plus small vertex ints.

**(iv) V003: Birth weights are recomputed per eligible record.** V002 cached them on the retained dict. That is ≤ 2 × 15 shifts of the source and target edgeset ints per record (raw edges ≤ 4 cut/restored + 3 root + 8 child), peak +1 temporary. L8 churn is about 5 MB per record.

**(v) V003: graph rebuild after eviction re-pays cost (b).** `_bits(edgeset)` makes about 3 big-int temporaries per edge.
- L4: ≲ 768 edges × 3 × 4.9 KB, about 10 MB of churn.
- L8: ≲ 6144 × 3 × 315 KB, about 6 GB of churn (time, not peak).
- Plus port-cache lookups and per-owner `_root_cuts` again on demand.
- Each `_infos` access hashes the edgeset int twice (pop and reinsert), O(size).

**(vi) Unchanged V002 global costs (L11 (a)-(c)).** O(NA·NB) bit cost per key construction/XOR/bit test, O(V+E) structure per new graph, and full read recomputation per state.

### Per-call peak

- **V003:** the retained bound above, plus one call's output list (ii) and (iii), plus O(1) temporaries.
- **V002:** additionally retained about 0.2–0.4 GB per distinct fully enumerated L4 graph, accumulating across calls.

V003 removes that accumulation. It does not remove the within-call output peak of full-scope enumeration. This is not a claim that the next L4 attempt will fit or mix: no run was made.

## AST check (python3 -I -B, Python 3.9.6, ast.parse + in-memory compile of the V003 TEXT)

| Check | Result |
|---|---|
| parse + compile | OK, on both the scratch text and the installed bytes |
| Imports | unchanged: array.array, cmath, collections.abc.Mapping, itertools.permutations/product, math, numpy, sys, typing.NamedTuple. `array` was already imported. |
| Banned constructs | none: no `@`, dot, matmul, vdot, inner, tensordot, outer, kron, errstate, print, open, exec, eval, input, compile, `__import__`, globals, lambda, global/nonlocal, yield or async |
| einsum without optimize=False | none |
| Top level | docstring, imports, literal constants, defs and classes only. Nothing executes at import. No decorators. |
| Public callables | 23, all keyword-only with no defaults, identical to V002 |
| Unused private top-level functions | none |
| Never-bound loaded names | none |
| Per-scope check of every changed function | no unresolved names (`_admit_registration`, `_forward_channels`, `_forward_descriptor`, `_reverse_channels`, `_reverse_descriptor`, `_owner_birth`, `_info_for`, `_transitions`) |
| Full AST report | identical to V002's |
| Public signature and record-field comparison | 42 items, identical |

**Status.** UNTESTED: static only, never executed by its author. A distinct reviewer must trace F1-F8 and R1-R10, and reconcile the compatibility delta above (0411 item 4).

## diff -u owned_parent_operator_v002.py owned_parent_operator_v003.py

```diff
--- owned_parent_operator_v002.py
+++ owned_parent_operator_v003.py
@@ -1,6 +1,23 @@
-"""Owned-parent operator adapter V002 -- UNT task 0405, contract section 11(A).
+"""Owned-parent operator adapter V003 -- UNT task 0405, contract section 11(A); 0411 repair.
 
-STATUS. Static fix of V001 (owned_parent_operator_v001.py sha256
+V003 STATUS (UNT 0411). Copy of V002 (owned_parent_operator_v002.py sha256
+b5fded4d1272322036748d4d1b4e634a804c1da1ad6717e70e32b4f2a364a94e, preserved unchanged) with ONLY
+the exact representation repair of the Birth candidate store, after the first full-owned L4 run
+was killed on measured memory (0411 7b102be61d78c22af98ca14f6bcadf867ce025c42509c1bacb216563ba3cf599).
+(1) Per graph and owner the context caches only the four sorted edge codes of each C_loc cut
+(array 'q') and, per surviving reverse pairing, its small (ub, av, rc) code triples and root
+codes; no cut/child/star/restored bit mask and no target graph integer is cached. (2) The donor,
+newborn and census eligibility of every candidate is tested with bit shifts over its actual cut
+or child codes BEFORE any mask, target graph or target key is built; masks, children and the
+target graph are built transiently, by the V002 expressions, only for an eligible channel.
+Every forward and reverse candidate, the cut deduplication, owner, multiplicity, support,
+endpoint-mean weight, amplitude, canonical target and record order are unchanged. (3) The
+per-graph structure cache is bounded by the new REQUIRED, validated registration key
+'max_cached_graphs' (positive int, no default): least recently used graphs beyond it are
+evicted and rebuilt exactly on their next use (L11). Public names, signatures and record
+formats are unchanged. Its author never imported or executed it. UNTESTED (static only).
+
+V002 STATUS. Static fix of V001 (owned_parent_operator_v001.py sha256
 27ad1762dbdc559eb92edcb6f7fe83790b73a4e23d71b12500b8586c811de3b6, preserved unchanged) by the
 module-A fix author. Only the blocking review issues are changed (REVIEW_0405_FIDELITY_V001.md
 dfd97e2fa36a6510599245a3629106c1e51df3a2d75aa381d1b163ddecf5fd46, 0408, 0409): per-vertex/per-part
@@ -117,10 +134,12 @@
   each (G, C, j) once, no multiplicity factor. V002: the witness set W_G(C) is exactly the set of
   roots whose local search generates C, so the channels of owner j are generated from root o_j
   alone (per-owner, lazily cached per graph); the channel set is identical to V001's global C_loc
-  pass followed by the witness filter. Surgery deletes the four cut edges (u, v), u in A,
-  v in B, adds children (u, b_j) and (a_j, v) each carrying the cut bit, keeps every other factor and
-  bit, inserts a_j, b_j in R with p = q = 0, and sends the donor pair RR -> II (loaded map, not the
-  PRIMARY blank-I BirthMap.encode l.145). birth_rev at an active slot enumerates all 4! pairings of
+  pass followed by the witness filter. V003: that per-owner cache holds only edge codes; masks,
+  children and the target graph are derived from the codes for eligible channels only.
+  Surgery deletes the four cut edges (u, v), u in A, v in B, adds children (u, b_j) and (a_j, v)
+  each carrying the cut bit, keeps every other factor and bit, inserts a_j, b_j in R with
+  p = q = 0, and sends the donor pair RR -> II (loaded map, not the PRIMARY blank-I
+  BirthMap.encode l.145). birth_rev at an active slot enumerates all 4! pairings of
   b_j's four A neighbours with a_j's four B neighbours, reconstructs each predecessor and keeps the
   pairing only if the complete forward image holds: no restored edge duplicates a surviving edge,
   paired child bits are equal, census two, a_j and b_j in R with p = q = 0, donors II, and o_j
@@ -203,7 +222,10 @@
   functions cost O(V + 108V + 24K) per call plus a one-off per-graph structure; palette_channels
   evaluates only palette owners (O(s) natives, 108 root choices and 24 pairings per palette owner)
   but keeps the global per-event costs listed in L11 (bit-set keys over NA*NB edge codes, per-graph
-  structure, globally normalized reads).
+  structure, globally normalized reads). V003 memory: the retained Birth store is 32 bytes per cut
+  (at most 108 per absent owner) plus one small code tuple per surviving reverse pairing, for at
+  most registration['max_cached_graphs'] graphs; every eligible Birth record still materializes
+  its two O(NA*NB)-bit target key ints in the returned list (L11 (e)).
 
 LIMITATIONS: see the module constant LIMITATIONS (each ambiguity is implemented literally and listed).
 """
@@ -305,9 +327,19 @@
     are not covered here. Build integrity checks (Hermiticity of H and every E_alpha, sum_alpha
     E_alpha = H) use summation tolerances; they are internal consistency checks, not validation.
 L11 No compression, Krylov, P/Q reduction or memory kernel. The full basis is exponential (see COST);
-    state-level functions are the route for samplers. Context caches grow with the number of distinct
-    supporting graphs visited; the caller bounds memory with release_caches(). Remaining GLOBAL
-    per-event costs of the basis-free functions (0408 item 3; honest report, not removed in V002):
+    state-level functions are the route for samplers. V003 (0411) structural cache bound: the
+    per-graph structure (neighbours, port codes, presence, coverage flags, native weights and the
+    compact Birth store) is kept for at most registration['max_cached_graphs'] distinct supporting
+    graphs; using a graph makes it most recent, and the least recently used graph beyond the bound
+    is evicted. An evicted graph is rebuilt by the same pure _graph_info/_owner_birth on its next
+    use, so every record is unchanged; the rebuild re-pays only cost (b) below. The per-vertex
+    port_order and per-edge accessor caches are NOT evicted, so eviction never re-invokes a caller
+    callable for an already admitted value; release_caches() still drops every cache, after which
+    the registered port_order and edge accessors are called again and must be deterministic (L5,
+    L8). A build whose component has more graphs than the bound rebuilds evicted structure when a
+    row of that graph is processed (exact, slower). Native flip keys (one new inc int per scope
+    edge) are unchanged V002 output costs. Remaining GLOBAL per-event costs of the basis-free
+    functions (0408 item 3; honest report, not removed in V002):
     (a) canonical keys are bit sets over fixed codes; the edgeset and inc ints span NA*NB edge codes
     (NA = NB = V0/2 + K; 2,359,296 codes at L=8), and every key construction, XOR and bit test costs
     O(NA*NB) bit operations whatever the palette size; (b) each distinct supporting graph (every
@@ -317,7 +349,15 @@
     (c) read_rows recomputes every read row of the state (presence, Z, ZZ and the per-cell
     normalized coarse sums) by design: full outgoing reads after every transition, with ports
     reassigned from the current graph and current populations, never a copied-bit shortcut for
-    Birth; (d) caches of graph structure, ports and accessor values grow with distinct graphs/edges.
+    Birth; (d) graph structure is bounded as above, but the port_order cache (per vertex and current
+    neighbour set) and the accessor value caches (per stable edge) still grow with the distinct
+    neighbourhoods/edges met until release_caches(); (e) V003 transient costs: the census of every
+    candidate cut is four shifts of inc (each shift allocates a temporary int of up to NA*NB bits,
+    freed at once); every ELIGIBLE Birth/reverse channel builds, transiently, its cut/star mask,
+    target graph int and new incidence int (O(NA*NB) bits each) plus a small descriptor dict and
+    recomputes its endpoint-mean weights (V002 cached them on the retained channel dict); the
+    target key ints and the labelled records stay in the returned list, so one full-scope
+    primitive_channels call holds O(#eligible Birth) keys of two O(NA*NB)-bit ints at once.
     Birth witness search is per original owner root (V002), so only evaluated owners pay for C_loc.
 L12 primitive_channels lists diagonal owners only where their operator element is structurally
     nonzero (e.g. epsilon_r only at q_v=1); failed Birth-reverse pairings and other exact zeros
@@ -347,6 +387,8 @@
     W = C0^(-1/2) with C0 = (4/3) I); then reads, module B read sources, sampler H_c sources and every
     source derivative use one set of corrected moments, and pair_source_hamiltonian with
     raw_to_whitened_sources is the same contraction expressed caller-side. No value is chosen here.
+    V003: the binding must also pass the REQUIRED registration['max_cached_graphs'] (L11); its
+    absence fails closed naming the key. No value is chosen here.
 """
 
 
@@ -379,7 +421,8 @@
                 "E_R", "E_S", "E_I", "e_R", "e_I", "C_identity")
 _PROFILE_KEYS = ("h", "t", "theta", "g", "kappa", "epsilon")
 _REGISTRATION_KEYS = ("cells", "original_cell", "edge_cells", "donor_anchor",
-                      "identity_allocation", "port_order", "port_vectors", "whitening")
+                      "identity_allocation", "port_order", "port_vectors", "whitening",
+                      "max_cached_graphs")
 _EDGE_PROFILES = ("h", "t", "theta")
 _CAP_KEYS = ("max_dimension", "max_graphs", "max_events_per_row")
 _STATE_KEYS = ("slots", "edges", "occupied", "carriers", "records", "spent", "donors_ready")
@@ -825,6 +868,13 @@
         if not sv[-1] > 64.0 * np.finfo(np.float64).eps * sv[0]:
             failures.append("registration['whitening']: a nonsingular real 3x3 matrix W is required "
                             "(dual sources j' = W^-T j need W invertible; pass the identity for raw moments)")
+    # V003 (0411): declared bound on the per-graph structure cache (L11); resource control only.
+    mcg = registration["max_cached_graphs"]
+    if isinstance(mcg, bool) or not isinstance(mcg, (int, np.integer)) or int(mcg) < 1:
+        failures.append(f"registration['max_cached_graphs']: a positive integer is required, got {mcg!r} "
+                        "(the declared maximum number of supporting graphs whose structure the context "
+                        "retains; least recently used graphs beyond it are evicted and rebuilt exactly; "
+                        "no default)")
     if failures:
         return None
     cell_vids = [np.array([v for v in dom["label_order"] if cell_vid[v] == a], dtype=np.int64)
@@ -843,7 +893,7 @@
         "frames_B_equal_negated_register_table": bool(np.all(frames[na:] == -table)),
         "w_site": [((cell_vid[v], 1.0),) for v in range(dom["NV"])],
         "w_donor": [((cell_vid[dom["owner_vid"][d // 2]], 1.0),) for d in range(2 * dom["K"])],
-        "cell_vids": cell_vids,
+        "cell_vids": cell_vids, "max_cached_graphs": int(mcg),
     }
 
 
@@ -954,13 +1004,15 @@
     Built by validate_owned_model. Attributes: energy_cells (ordered cell labels), read_labels
     (typed read rows), vertex_labels, owners. Caches are pure functions of the validated inputs
     and the current graph (and of deterministic caller accessors); release_caches() drops them
-    (see LIMITATIONS L5, L8, L11).
+    (see LIMITATIONS L5, L8, L11). V003: per-graph structure is kept for at most
+    registration['max_cached_graphs'] graphs (least recently used evicted, rebuilt exactly).
     """
 
     def __init__(self, *, dom, model, reg):
         self._dom = dom
         self._model = model
         self._reg = reg
+        self._max_graphs = reg["max_cached_graphs"]
         self.energy_cells = reg["cells"]
         self.vertex_labels = tuple(dom["labels"])
         self.owners = tuple(dom["owners"])
@@ -993,7 +1045,9 @@
            'port_order' callable(*, vertex, neighbours) -> ordered neighbour labels,
            'port_vectors' frames: one real 4x3 table, {'A': 4x3, 'B': 4x3}, {vertex label: 4x3}
            for every vertex, or callable(*, vertex) -> 4x3 (L8), 'whitening' explicit real
-           nonsingular 3x3 W applied inside the coarse R/S reads (identity for raw moments).
+           nonsingular 3x3 W applied inside the coarse R/S reads (identity for raw moments),
+           'max_cached_graphs' positive int (V003: declared bound on cached per-graph structure;
+           resource control only, records are identical for every admitted value; L11).
     Returns {'ok', 'stage_reached', 'failures', 'context'}; context is an OwnedModelContext.
     """
     result = {"ok": False, "stage_reached": "inputs", "failures": [], "context": None}
@@ -1065,43 +1119,60 @@
 
 
 def _forward_channels(dom, info, j):
-    """Owned Birth channels (G, C, j) of owner j: C in C_loc(G) witnessed by original o_j, slot j absent."""
-    out = []
+    """Owned Birth cuts (G, C, j) of owner j: C in C_loc(G) witnessed by original o_j, slot j absent.
+
+    V003 (0411): compact store. A flat array('q') holding the four sorted edge codes of every cut
+    of _root_cuts(o_j), in the V002 channel order (empty if slot j is active). No cut or child bit
+    mask, child code or target graph is built or retained here; _forward_descriptor derives them
+    from these codes only for a channel that passes the donor and census eligibility.
+    """
+    out = array("q")
     if (info["slots_mask"] >> j) & 1:
         return out
-    edgeset = info["edgeset"]
+    for cut in _root_cuts(dom, info["nbrs"], dom["owner_vid"][j]):
+        out.extend(cut)
+    return out
+
+
+def _forward_descriptor(dom, info, j, cut):
+    """Transient V002 channel dict of one ELIGIBLE forward Birth (cut: its four sorted codes).
+
+    V003 (0411): the V002 _forward_channels fields used downstream (j, cut, child_edges,
+    root_other, target_edgeset, newborn_at_target, raw_edges, c), built by the V002 expressions
+    only after _transitions has found the census two and donors RR; never cached. Also returns
+    the transient cut mask for the incidence surgery in _transitions.
+    """
     root = dom["owner_vid"][j]
     a_new, b_new = dom["a_vid"][j], dom["b_vid"][j]
-    for cut in _root_cuts(dom, info["nbrs"], root):
-        cutmask = 0
-        children = []
-        child_codes = []
-        for c in cut:
-            u, v = _edge_ends(dom, c)
-            cu, cv = _code(dom, u, b_new), _code(dom, a_new, v)
-            cutmask |= 1 << c
-            # Copy the cut bit to BOTH children (PRIMARY BirthMap.encode_incidence l.130-136,
-            # here with loaded Ready newborns and owned donors, GEN l.31-34).
-            children.append((1 << c, (1 << cu) | (1 << cv)))
-            child_codes.extend((cu, cv))
-        target = edgeset & ~cutmask
-        for _bit, cmask in children:
-            target |= cmask
-        root_other = tuple(c for c in info["port_codes"][root] if c not in cut)
-        out.append({
-            "j": j, "cut": cut, "cutmask": cutmask, "children": tuple(children),
-            "child_edges": tuple(child_codes), "root_other": root_other,
-            "target_edgeset": target, "newborn_at_target": True,
-            "raw_edges": tuple(sorted(set(cut) | set(root_other) | set(child_codes))),
-            "c": None,
-        })
-    return out
+    cutmask = 0
+    child_codes = []
+    for c in cut:
+        u, v = _edge_ends(dom, c)
+        cutmask |= 1 << c
+        # Copy the cut bit to BOTH children (PRIMARY BirthMap.encode_incidence l.130-136,
+        # here with loaded Ready newborns and owned donors, GEN l.31-34): codes (u, b_j), (a_j, v).
+        child_codes.extend((_code(dom, u, b_new), _code(dom, a_new, v)))
+    target = info["edgeset"] & ~cutmask
+    for cc in child_codes:
+        target |= 1 << cc
+    root_other = tuple(c for c in info["port_codes"][root] if c not in cut)
+    ch = {
+        "j": j, "cut": cut, "child_edges": tuple(child_codes), "root_other": root_other,
+        "target_edgeset": target, "newborn_at_target": True,
+        "raw_edges": tuple(sorted(set(cut) | set(root_other) | set(child_codes))),
+        "c": None,
+    }
+    return ch, cutmask
 
 
 def _reverse_channels(dom, info, j):
     """Every candidate predecessor reconnection of active slot j with its graph-level tests.
 
     State-level tests (child bits, census, newborn Ready p=q=0, donors II) are in _transitions.
+    V003 (0411): compact store. One small tuple (pairs, root_other) of edge codes per pairing that
+    passes the graph-level tests, in the V002 order, with pairs = ((ub_i, av_sigma(i), rc_i) for
+    i = 0..3); no star, restored or newborn mask and no predecessor graph is built or retained
+    here; _reverse_descriptor derives them only for a pairing that passes the state-level tests.
     """
     out = []
     if not (info["slots_mask"] >> j) & 1:
@@ -1116,9 +1187,6 @@
         return out  # a_j adjacent to b_j: no predecessor of the loaded map exists
     star_ub = tuple(_code(dom, u, b_new) for u in u_side)
     star_av = tuple(_code(dom, a_new, v) for v in v_side)
-    starmask = 0
-    for c in star_ub + star_av:
-        starmask |= 1 << c
     o = dom["owner_vid"][j]
     o_nbrs = nbrs[o]
     for sigma in permutations(range(4)):
@@ -1141,24 +1209,41 @@
             if pred != set(u_side):
                 continue
             root_other = tuple(_code(dom, u, o) for u in o_nbrs if u != a_new)
-        restmask = 0
-        for c in restored:
-            restmask |= 1 << c
         pairs = tuple((star_ub[i], star_av[sigma[i]], restored[i]) for i in range(4))
-        child = tuple(sorted(star_ub + star_av))
-        out.append({
-            "j": j, "cut": tuple(sorted(restored)), "pairs": pairs, "starmask": starmask,
-            "child_edges": child, "root_other": root_other,
-            "target_edgeset": (edgeset & ~starmask) | restmask, "newborn_at_target": False,
-            "newborn_mask": (1 << a_new) | (1 << b_new),
-            "raw_edges": tuple(sorted(set(restored) | set(root_other) | set(child))),
-            "c": None,
-        })
+        out.append((pairs, root_other))
     return out
 
 
+def _reverse_descriptor(dom, info, j, pairs, root_other):
+    """Transient V002 channel dict of one reverse pairing that passed every state-level test.
+
+    V003 (0411): the V002 _reverse_channels fields used downstream (j, cut, child_edges,
+    root_other, target_edgeset, newborn_at_target, raw_edges, c), built by the V002 expressions
+    from the cached code triples; never cached. Also returns the transient star mask for the
+    incidence surgery in _transitions. The ub over pairs are star_ub in order and the av are
+    star_av permuted by sigma, so the star set, starmask and sorted child tuple equal V002's.
+    """
+    starmask = 0
+    restmask = 0
+    star = []
+    restored = []
+    for ub, av, rc in pairs:
+        starmask |= (1 << ub) | (1 << av)
+        restmask |= 1 << rc
+        star.extend((ub, av))
+        restored.append(rc)
+    child = tuple(sorted(star))
+    ch = {
+        "j": j, "cut": tuple(sorted(restored)), "child_edges": child, "root_other": root_other,
+        "target_edgeset": (info["edgeset"] & ~starmask) | restmask, "newborn_at_target": False,
+        "raw_edges": tuple(sorted(set(restored) | set(root_other) | set(child))),
+        "c": None,
+    }
+    return ch, starmask
+
+
 def _owner_birth(dom, info, j):
-    """(forward channels, reverse candidates) of owner j in this graph, built once on demand."""
+    """(forward cut codes, reverse code tuples) of owner j in this graph, built once on demand (V003)."""
     hit = info["birth"].get(j)
     if hit is None:
         hit = (_forward_channels(dom, info, j), _reverse_channels(dom, info, j))
@@ -1204,10 +1289,19 @@
 
 
 def _info_for(ctx, edgeset):
-    info = ctx._infos.get(edgeset)
+    """Structure of graph edgeset from the context cache, bounded by max_cached_graphs (V003, L11).
+
+    The dict is kept in use order (a hit is moved to the end); beyond the declared bound the least
+    recently used graph is dropped. A dropped graph is rebuilt by the same pure _graph_info on its
+    next use; callers keep their own reference for the rest of the call.
+    """
+    infos = ctx._infos
+    info = infos.pop(edgeset, None)
     if info is None:
         info = _graph_info(ctx, edgeset)
-        ctx._infos[edgeset] = info
+    infos[edgeset] = info
+    while len(infos) > ctx._max_graphs:
+        del infos[next(iter(infos))]
     return info
 
 
@@ -1499,33 +1593,48 @@
             out.append(("admit", ("vertex", v), (slots, edgeset, inc, p | bit, q, s | bit, dm)))
         elif (s & bit) and (p & bit):
             out.append(("admit_rev", ("vertex", v), (slots, edgeset, inc, p ^ bit, q, s ^ bit, dm)))
+    # V003 (0411): every guard below is tested by shifts over the candidate's own cut/child codes
+    # (and small vertex/donor ints) BEFORE any mask, target graph or target key is built.
     for j in scope["owners"]:
-        for ch in _owner_birth(dom, info, j)[0]:
-            if ((dm >> (2 * j)) & 3) == 3 and _popcount(inc & ch["cutmask"]) == 2:
-                new_inc = inc & ~ch["cutmask"]
-                for cbit, cmask in ch["children"]:
-                    if inc & cbit:
-                        new_inc |= cmask
-                out.append(("birth", ("birth", ch),
-                            (slots | (1 << j), ch["target_edgeset"], new_inc, p, q, s, dm & ~(3 << (2 * j)))))
+        cuts = _owner_birth(dom, info, j)[0]
+        if not cuts or ((dm >> (2 * j)) & 3) != 3:
+            continue  # slot j active (no candidate) or donors not RR: zero
+        for i in range(0, len(cuts), 4):
+            cut = tuple(cuts[i:i + 4])
+            x = [(inc >> c) & 1 for c in cut]
+            if x[0] + x[1] + x[2] + x[3] != 2:
+                continue  # cut census not exactly two: zero; nothing is built
+            ch, cutmask = _forward_descriptor(dom, info, j, cut)
+            child = ch["child_edges"]
+            new_inc = inc & ~cutmask
+            for k in range(4):
+                if x[k]:
+                    new_inc |= (1 << child[2 * k]) | (1 << child[2 * k + 1])
+            out.append(("birth", ("birth", ch),
+                        (slots | (1 << j), ch["target_edgeset"], new_inc, p, q, s, dm & ~(3 << (2 * j)))))
     for j in scope["owners"]:
-        for ch in _owner_birth(dom, info, j)[1]:
-            if (dm >> (2 * j)) & 3 or (p | q | s) & ch["newborn_mask"]:
-                continue  # donors not II, or a newborn not Ready with p = q = 0: zero
-            census = 0
-            new_inc = inc & ~ch["starmask"]
-            equal = True
-            for ub, av, rc in ch["pairs"]:
-                x = (inc >> ub) & 1
-                if x != (inc >> av) & 1:
-                    equal = False  # unequal paired child bits: zero (PRIMARY BirthMap.decode l.154-157)
-                    break
-                census += x
-                if x:
-                    new_inc |= 1 << rc
-            if equal and census == 2:
-                out.append(("birth_rev", ("birth", ch),
-                            (slots & ~(1 << j), ch["target_edgeset"], new_inc, p, q, s, dm | (3 << (2 * j)))))
+        cands = _owner_birth(dom, info, j)[1]
+        if not cands or (dm >> (2 * j)) & 3:
+            continue  # no candidate pairing, or donors not II: zero
+        pqs = p | q | s
+        if (pqs >> dom["a_vid"][j]) & 1 or (pqs >> dom["b_vid"][j]) & 1:
+            continue  # a newborn not Ready with p = q = 0: zero
+        for pairs, root_other in cands:
+            x = []
+            for ub, av, _rc in pairs:
+                xb = (inc >> ub) & 1
+                if xb != (inc >> av) & 1:
+                    break  # unequal paired child bits: zero (PRIMARY BirthMap.decode l.154-157)
+                x.append(xb)
+            if len(x) != 4 or x[0] + x[1] + x[2] + x[3] != 2:
+                continue  # unequal pair or census not two: zero; nothing is built
+            ch, starmask = _reverse_descriptor(dom, info, j, pairs, root_other)
+            new_inc = inc & ~starmask
+            for k in range(4):
+                if x[k]:
+                    new_inc |= 1 << pairs[k][2]
+            out.append(("birth_rev", ("birth", ch),
+                        (slots & ~(1 << j), ch["target_edgeset"], new_inc, p, q, s, dm | (3 << (2 * j)))))
     return out
 
 
```
