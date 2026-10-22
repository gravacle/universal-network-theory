# REVIEW 0405 module A V003: resource and API review (UNT 0411)

**Role:** distinct resource/API reviewer, not author. I wrote neither V002 nor V003.
**Date:** 2026-10-16. **Method:** static text review only.

- Nothing was imported or executed: not V002, not V003, not the evaluator, not the root adapter, not module B, and no UNT, Codex or root module.
- The only code I ran was `python3 -I -B` (Python 3.9.6) from my own scratch directory. It did `ast.parse` plus an in-memory `compile` on the module TEXTS, an AST comparison of V002 and V003, and a per-scope name check. I also ran `diff`, `shasum`, `grep` and plain arithmetic for the byte estimates in section 8.
- No run, benchmark, numerical case, network access or install took place.
- Access to `Universal Network Theory` was read-only. From the failure evidence I read only `receipt.json`, `stdout.txt` and the empty `stderr.txt`. I opened no file whose name contains TRIAL, FIT, Newton, FIELD_, ROTATION, MOM1, rotmod or MassModels, including the TRIAL recipe cited in the receipt. I did not open the root worker either.
- There is no `__pycache__` in the artifact directory. This file was written by exclusive create.

## 1. Binding inputs (sha256 computed from bytes; all match their pins)

| file | sha256 |
|---|---|
| 0411 task | 7b102be61d78c22af98ca14f6bcadf867ce025c42509c1bacb216563ba3cf599 |
| owned_parent_operator_v002.py (base, unchanged) | b5fded4d1272322036748d4d1b4e634a804c1da1ad6717e70e32b4f2a364a94e |
| **owned_parent_operator_v003.py (under review; 136,060 B, 2,637 lines)** | **a04f87954b68bb2dcc5a1af42a465b1d554ed1fc14d9b22d43e05e3e664f7f07** |
| FIX_DELTA_0405_A_V003.md (49,219 B) | 1e8652a854a53e24fe46a6b35755c3e6fe1f710f0c8dc43bd2cececde7cd8638 |
| FIX_DELTA_0405_A_V002.md | 47a96b7623c093c8efe2b78419b427b38fedac6e921d94b03f89d38b530e6d9e |
| FINAL_CHECK_0405_V001.md | af8fffec27657b7a26cfaea66b2803c67758ba77b9e5267f2b8035ca40f7afcd |
| receipt.json | 5c299ce78fbe9bf7447fb5231fe6fa6209697639e6d12732da95799bbf9457c1 |
| stdout.txt | 8c31b32362a2cfedfefa0e33d0371e08209932d062b9087178e1a7cc0c1b3528 |
| stderr.txt (0 bytes) | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| CONTRACT (section 4 read) | fcad9039574f1666af005bb76a231f14b90f0c8dd82acebd2b16ab77941cd642 |
| evaluator owned_collective_worldline_static_response_v002.py | 0d041119bd11227746238663ed93d99863d3a94c8295e539dbed15255b42a941 |
| root adapter owned_diamond_registration_input_adapter_v001.py | 0705be7ca500a3b8329566ba014b80645231be2178ad5b8ef089dbca163b3f77 |
| module B owned_retained_source_columns_v002.py (grep only) | 173f608d9b4effdf61c3ea0bfb147aaf5528a742c3ec2501d41f5397b36bbe81 |

The evaluator pin equals the sampler V002 named in 0411 as the module that ran.

## 2. Verdict: PASS_WITH_NOTES

**Blocking issues: none.**

- V003 meets 0411 items 1 to 3.
- The Birth store keeps only edge codes. Every donor, newborn and census guard runs before any mask, target graph or key is built.
- I traced every changed mask and code operation independently (section 4). Records, their order, the deduplication, owner, multiplicity, supports, endpoint-mean weights, amplitudes and canonical targets are identical to V002.
- The per-graph structure cache is bounded by a validated, required registration key. Eviction cannot change any record (section 5).
- Public names, signatures, record fields and `resources()` keys are unchanged. The only input-schema change is the new required key, which is the form of caller control the task permits.

**Status.**
- V003 is UNTESTED: it has never been executed.
- Whether the next L4 attempt fits under the 1 GiB cap is also UNTESTED. The deciding test is a measured run under root's caps.

## 3. Ineligible Birth proposals: what is created and what is retained

**Retained per (graph, owner)** (`_forward_channels` l.1121-1134, `_reverse_channels` l.1168-1214, `_owner_birth` l.1245-1251):
- Forward: a flat `array('q')` of the four sorted codes of each `_root_cuts` cut, in V002 order. That is 32 B per cut, at most 108 per absent owner.
- Reverse: one `(pairs, root_other)` tuple of small code ints per pairing that passes the graph-level tests. There are at most 6 per active owner, because the witness test fixes sigma at the owner's index.
- No cut, child, star, restored or newborn bit mask is kept, and no target graph int.

**Created for an ineligible forward cut** (l.1602-1606):
- One 4-tuple, a 4-element list of 0/1 ints, and four shift temporaries `inc >> c`.
- Each temporary is freed immediately, so one is alive at a time. Its size is at most the size of `inc`: about 1.6 KB at L4 and 105 KB at L8 on G0, rising to 4.9 KB and 315 KB when slots are active.
- No mask, child code, target graph, key or dict is built.

**Created for an ineligible reverse pairing** (l.1622-1630): at most eight shift temporaries of the same kind, and nothing else.

**Donor guards (both directions) and the newborn-Ready guard (reverse):** hoisted per owner (l.1600, l.1617-1621). They test only small vertex/donor ints.

Two transient shifts remain:
- The shift temporaries are the "shifts over the actual cut/child codes" that 0411 item 1 prescribes. They are transient and never retained.
- The graph-level duplicate-old-edge test `edgeset >> c` in `_reverse_channels` (l.1194) is unchanged from V002 and is also transient.

## 4. Equivalence trace (independent of the FIX_DELTA's F1-F8 and R1-R10, and agreeing with them)

**Removed fields.**
- `cutmask`, `children`, `pairs`, `starmask` and `newborn_mask` were read only in V002 `_transitions` (grep of V002 l.1504-1528).
- Downstream readers use only `j`, `cut`, `child_edges`, `root_other`, `target_edgeset`, `newborn_at_target`, `raw_edges` and `c`. Those readers are `_amplitude`, `_birth_weights`, `_support_labels` and `_owner_id`, and all four are AST-identical to V002.

**Forward.**
- *Candidate order.* The store keeps `_root_cuts` (unchanged) order. `tuple(cuts[i:i+4])` restores the same ints, since every code is below 2^63.
- *Census.* The four cut codes are distinct. Each cut edge meets a different root-side neighbour: the root edge meets rn[k], and edge i meets others[i]. Those four are distinct neighbours in a simple q4 graph, and ch[i] is never the root and lies in the root's part. So `popcount(inc & cutmask) == sum((inc >> c) & 1)`: same predicate.
- *Donor guard.* `((dm >> 2j) & 3) != 3` is loop-invariant, so hoisting it selects the same channels. `_owner_birth` is still called first for every scope owner, so the caching pattern is unchanged.
- *Children, target and new incidence.* `child_codes` uses the same `_code(u, b_j)` and `_code(a_j, v)` order. OR-ing the eight `1 << cc` into `edgeset & ~cutmask` equals V002's OR of the four two-bit `cmask`s. `x[k] = (inc >> cut[k]) & 1` is the same truth value as V002's `inc & cbit`, and the bits OR-ed into `new_inc` are V002's `cmask` for cut[k].
- `root_other`, `raw_edges`, `j`, `newborn_at_target` and `c = None` use the V002 expressions on the same `info`.

**Reverse.**
- The loop body up to `pairs` is unchanged: restored codes, duplicate test, both witness branches and `root_other`. The stored pairings are the same, in `permutations(range(4))` order.
- *Newborn guard.* `(p|q|s) & ((1<<a_j)|(1<<b_j))` is nonzero exactly when bit a_j or bit b_j of `p|q|s` is set.
- *Pair test.* The same shifts run in the same order. "No break" becomes `len(x) == 4`, and the census becomes `sum(x) == 2`.
- *Star mask and child tuple.* The ub over pairs are `star_ub[i]` and the av are `star_av[sigma(i)]`. Since sigma is a bijection, the bit set and the sorted 8-tuple equal V002's. The 8 codes are distinct because `a_j` is not adjacent to `b_j` (early return at l.1186).
- *Restored mask and cut.* `rc_i` is `restored[i]`, so `restmask` and `tuple(sorted(restored))` are equal. The target `(edgeset & ~starmask) | restmask` and `new_inc` are therefore equal.

**Weights.**
- `ch["c"]` is now computed once per transient descriptor instead of once per retained V002 dict.
- `_birth_weights` (unchanged) is a pure function of (source edgeset = `info["edgeset"]`, `target_edgeset`, `raw_edges`, `j`, `newborn_at_target`) and the registration. None of these depends on `inc`, `p`, `q`, `s` or `dm`, so the values are identical.

**Lifetime.**
- Records never reference a descriptor. `owner_id` and the supports are built from labels, and `_dense` copies the weights into a new tuple.
- So the descriptors die when `_transition_records`, `_process_row` or `primitive_events` returns, and no reference cycle exists.

The Birth law of CONTRACT section 4 (C_loc both mirrors, witness, slot, donors, census two, copy-to-both-children, the reverse full-image checks, no multiplicity) is untouched.

## 5. Structural-cache bound

**Mechanism** (`_info_for` l.1291-1305):
- Every access pops and reinserts the entry, so the most recent graph is last.
- Then `while len > max_cached_graphs: del oldest`. The just-accessed graph is never evicted, because the bound is validated to be at least 1.
- If `_graph_info` raises, nothing is inserted.

**It actually bounds accumulation.**
- `ctx._infos` is written only by `_info_for` (plus `__init__` and `release_caches`).
- Each info's contents are bounded per graph: neighbours, port codes, presence, `w_edge` ≤ E entries, `w_deg` ≤ V entries, and `birth` ≤ K owners.
- The access points are `_admit_key` (every state admission, the build seeds and `index_of`), `_process_row` and `primitive_events`. Each call holds exactly one `info`, so an evicted graph's local reference stays valid for the rest of that call.

**Eviction cannot change results.**
- Every info field is a pure function of the edgeset, the validated inputs, `ctx._ports` and `ctx._edge_values`.
- `ctx._ports` and `ctx._edge_values` are not evicted, so a rebuild never re-invokes `port_order` or an edge accessor for a value already admitted.
- Failing callables are never cached, in V002 or in V003.
- Coverage flags are re-derived from the cached values.
- Therefore records are identical for every admitted bound. Only the rebuild time differs.

**Size retained per cached graph** (section 8 arithmetic): about 0.6–1 MB at L4 and about 5–10 MB at L8, of which the forward store is 0.47 MB and 3.7 MB. This agrees with the author's 0.5–1.5 MB and 5–15 MB.

**Not bounded.** `ctx._ports` and `ctx._edge_values` grow per distinct admitted graph:
- Up to about 11 new (vertex, neighbour-set) entries of about 0.35 KB each.
- Up to 8 new edges × 3 accessor profiles of about 0.1 KB each.
- Together about 4–7 KB per graph, at both L4 and L8.
- Only `release_caches()`, the existing public control, clears them. See N2.

## 6. Public API compatibility

**Module surface** (AST comparison of the V002 and V003 texts):
- The 21 public module functions and methods have identical names and signatures, all keyword-only. With the two keyword-only class constructors that makes the author's 23.
- No function anywhere in the module has a default.
- The `_Channel` fields (owner_id, kind, target_state, amplitude, queried_support, changed_support, energy_weights) and the `_IndexedEvent` fields are unchanged.
- `_static_resources`, `_assemble` and `resources()` are AST-identical, so the `resources()` keys and values are unchanged.
- Changed definitions are exactly: `_admit_registration`, `OwnedModelContext.__init__`, `_forward_channels`, `_reverse_channels`, `_info_for` and `_transitions`, plus the new `_forward_descriptor` and `_reverse_descriptor` and a docstring-only change to `_owner_birth`. The only changed assignments are `LIMITATIONS` (text) and `_REGISTRATION_KEYS`.
- The FIX_DELTA's embedded diff body matches the actual `diff -u` line for line (16 hunks, +194/−85).

**Input delta.** `registration['max_cached_graphs']` is REQUIRED.
- If missing: `registration: missing required keys ['max_cached_graphs'] (no defaults)`.
- If invalid: a message naming the key. bool, np.bool_, float and values ≤ 0 are rejected; a numpy integer is accepted and stored as `int`.
- In the other direction, V002 rejects a registration carrying this key as an unknown key. Registrations are therefore version-specific.

**Evaluator V002.**
- Required API names (l.446-465): `validate_owned_model`, `canonical_state_key`, `primitive_channels`, `diagonal_terms` and `read_rows`, plus `owner_restricted_channels`, which root's wrapper maps to `palette_channels`. All are unchanged.
- It passes `registration` unchanged (l.2717) and requires the adapter binding to hold the same object (l.580). It reads the record fields kind, owner_id, target_state, amplitude, changed_support and energy_weights (l.1243-1312), all unchanged. It touches no private cache.
- Compatible. Until the key is present it fails closed at stage `model`, with the operator's message.

**Root adapter V001.**
- `build_inputs` (l.145-154) emits the seven V001 registration keys. As already established for V002, root's recipe adds `whitening` and the A/B frames.
- The adapter's own functions read only `registration['cells']` and `['port_order']` and call `state_labels`, so the extra key affects nothing in the adapter.
- Root's binding must add one positive integer. I did not read root's recipe or worker, so where exactly root adds it is not verified here.

**Module B V002.** It neither builds nor validates a registration (grep), so it is unaffected.

## 7. AST inertness (V003 text; identical results for V002)

| check | result |
|---|---|
| parse + in-memory compile | OK |
| imports | array.array, cmath, collections.abc.Mapping, itertools.permutations/product, math, numpy, sys, typing.NamedTuple (unchanged); `sys` used only for `getsizeof` |
| MatMult / dot / matmul / vdot / inner / tensordot / outer / kron | none |
| einsum without `optimize=False` | none |
| I/O (open, print, input, write/read, load/save, environ, exit), exec/eval/compile/`__import__`, global/nonlocal | none |
| top level | docstring, imports, literal constants, defs and classes only; no decorators; nothing runs at import |
| defaults | none in any function; all public callables keyword-only |
| changed functions: unresolved names / unused private defs | none / none |

## 8. Remaining transient costs (code-structure arithmetic, CPython int = 24 + 4·ceil(bits/30) B; nothing run)

Geometry: L4 has V0 = K = 128, NA = NB = 192, NA·NB = 36,864 and 64 cells. L8 has V0 = K = 1024, NA = NB = 1536, NA·NB = 2,359,296 and 512 cells.

The int sizes follow from that:

| int | L4 | L8 |
|---|---|---|
| full edge-space int | 4.9 KB | 315 KB |
| G0 edgeset/inc | 1.6 KB | 105 KB |
| forward Birth target and new_inc (mean over j; the (a_j, v) children set the top bit) | 3.3 KB | 210 KB |

**Per eligible forward Birth record, held in the returned list.**
- Two key ints (target, new_inc), a 7-tuple key with small slot/donor ints, owner_id, the 19 distinct labelled anchors of the queried/changed supports (about 2.3 KB) and a dense energy-weight tuple (568 B at L4, 4.15 KB at L8).
- Until `_transition_records` returns there is also a descriptor dict with small tuples (about 1.3 KB).
- That is about 11 KB per record at L4 and about 0.43 MB at L8. Reverse records are similar, at most 6 per active owner.

**Transient churn per eligible forward record** (time, not peak): the cut mask, ~cutmask twice, eight `1 << cc`, the OR chain and up to 30 weight shifts. That is about 0.12 MB at L4 and about 7 MB at L8, with at most one or two large temporaries alive at a time.

| per call | L4 | L8 |
|---|---|---|
| structural forward cuts tested (108·K) | 13,824 | 110,592 |
| census shift churn (time) | ≈ 46 MB | ≈ 2.3e10 B |
| eligible Birth output, illustrative 6/16 census-two fraction | ≈ 5.2e3 records, ≈ 58 MB | ≈ 4.1e4 records, ≈ 1.8e10 B |
| eligible Birth output, all-eligible bound | ≈ 0.16–0.2 GB | ≈ 4.7e10–7e10 B |
| descriptor and weight churn (time) | ≈ 0.6–1.7 GB | ≈ 3e11 B |
| native flip keys and records | ≈ 1.3 MB | ≈ 0.23 GB |
| palette call per owner (output) | ≈ 0.5–1.6 MB | ≈ 17–70 MB |
| rebuild of an evicted graph (`_bits` churn) | ≈ 1.3 MB (G0-like) to 11 MB (all slots active) | ≈ 0.64 GB to 5.8 GB |

What these numbers mean:
- **Peak.** V003 no longer accumulates about 0.2–0.4 GB of mask-rich candidates per visited L4 graph. Peak becomes the bounded cache, plus one call's output list, plus O(1) temporaries, plus the slowly growing port/accessor caches.
- **Evaluator.** It retains the target keys of each channel list it keeps (current and proposed states), so its holdings scale with the per-call output above.
- **L8 full scope.** Full-scope enumeration at L8 remains infeasible on output alone, as in V002.

## 9. Notes (non-blocking)

- **N1. Required key.** Root's binding must add `registration['max_cached_graphs']` (DECLARED by root; resource control only; records are invariant to its value). The same registration object then cannot be passed to V002.
- **N2. Unbounded value caches.** `ctx._ports` and `ctx._edge_values` still grow by about 4–7 KB per distinct admitted graph, at L4 and L8 alike. 1e5 admitted graphs is about 0.4–0.7 GB, which matters against a 1 GiB cap in long runs. Their only control is `release_caches()` at a cadence the caller declares. The author discloses this (L11 (d)).
- **N3. Interplay with root's mitigation.** If root keeps its per-enumeration `release_caches()`, the LRU bound never engages and every call rebuilds structure (cost (b)). A bound of 1 rebuilds on every x/y alternation; that is exact, only slower.
- **N4. Duplicate edgeset per cached graph.** On a cache hit the dict key becomes the caller's edgeset object, while `info["edgeset"]` keeps the original. So up to two equal edgeset ints are retained per cached graph: ≤ 10 KB at L4 and ≤ 0.63 MB at L8. This is small next to the per-graph sizes, and correctness is unaffected.
- **N5. LRU cost.** `next(iter(dict))` after front deletions scans dict holes, costing O(bound) pointer checks at worst. This is negligible next to the O(NA·NB) key work.
- **N6. Calibration of the author's figures.**
  - L8 full-scope output is ≈ 1.8e10 B at the illustrative fraction and up to ≈ 7e10 B at the bound. The chat summary's "about 1e10 bytes" is the right order but about 2× low.
  - The rebuild churn figures (10 MB at L4, 6 GB at L8) are all-slots-active bounds. G0-like graphs give about 1.3 MB and 0.64 GB.
  - The chat summary's "+185/−85" diff count is +194/−85 (2637 − 2528 = 109). The FIX_DELTA itself states no count.
- **N7. Unread files.** Root's worker and recipe were not read. Nothing here verifies the root binding beyond the adapter text.

Reviewer: distinct resource/API reviewer, not author. Nothing was imported or executed.
