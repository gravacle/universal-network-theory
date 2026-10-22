# FIX DELTA 0405 module A: owned_parent_operator v001 -> v002

Fix author for module A. The work was static only. Neither module, nor any legacy, UNT or Codex module, nor the root adapter, was imported or executed. The only code run was `python3 -I -B` with `ast.parse` and an in-memory `compile` on the V002 TEXT, from a scratch directory outside this folder. No `__pycache__` was written here. No numerical control, propagation, data extraction, network use or install was performed. V001 is unchanged. V002 was written by exclusive create.

| file | bytes | lines | sha256 |
|---|---|---|---|
| owned_parent_operator_v001.py | 103243 | 2151 | 27ad1762dbdc559eb92edcb6f7fe83790b73a4e23d71b12500b8586c811de3b6 |
| owned_parent_operator_v002.py | 128154 | 2528 | b5fded4d1272322036748d4d1b4e634a804c1da1ad6717e70e32b4f2a364a94e |

Binding inputs verified from bytes before editing (all match their pins):

- CONTRACT fcad9039574f1666af005bb76a231f14b90f0c8dd82acebd2b16ab77941cd642
- 0405 7baab49ebbd01de684df56a074b823552c1eca9e787384ad0a0084144295c003
- 0406 a465d9e3f703f2a2f19d383446c6a2bf6486e5f6be9fdf5996fc96dfb4693d50
- ADDENDUM 7cb15b4a5ac2ea33dfd43801c011142bc2b2388c3be0087152c049e78deccd39
- HP time-derivative addendum 2fc9dc2c0197d6b3d0e2ff5893ba32b7ef89ba5424680bc06bd5210d5207226a
- 0408 c0f0eaa940ce95c495fa2d7c21d59cae2a49e8028cc084df878d203e3c42e341
- 0409 53465ac03cfb88bc7e641c15d8659591a315eafabb77dd966890e6dfb4ebb73c
- registration f65dbc234ae082df342235b1a6c13a0282cf94665ba3e1c3989d12b12e7d7174
- whitening companion 9eb4861cce5e4c435a259811dbca289e7e95a2b4ac34732c9f6c3ee56c34d7d7
- blocked-palette move 3b06ee3392894de2e96716c86f7b3184c792a407a81435f95aa448440418ca16
- root adapter 0705be7ca500a3b8329566ba014b80645231be2178ad5b8ef089dbca163b3f77 (read as text only)
- REGISTER 032a564bd018b7302bd60de633f8e3c9d2f91f8c079f16b62548bce0e4e53d94
- REVIEW_0405_FIDELITY_V001.md dfd97e2fa36a6510599245a3629106c1e51df3a2d75aa381d1b163ddecf5fd46

## Per-issue resolution (V002 line numbers)

1. **"both" (time derivatives, ADDENDUM item 1; A L9).** On the A side this is resolved by an exact statement. No A code was added: A already exposes every member that the commutator means need, and module B V002 (FIX_DELTA_0405_B_V002.md) forms them.
   - L9 (l.286-301) replaces "belong to module B" with a precise statement. Every read row (presence, Z, ZZ, m and whitened R/S) and every E_alpha is a fixed current-state operator. The explicit read/frame partial derivatives are therefore zero, so L_O = (i/hbar)[K,O] and A_O = (i/hbar)[K',O] - [K,[K,O]]/hbar^2 exactly.
   - Graph-sector dependence of 1/m_alpha and of the ports enters only through the commutators, so there is no count derivative.
   - Reads are diagonal, so only the H and E_alpha parts of K and K' contribute.
   - K(t), K', the tangents and the node bounds live in B and are built from apply_H, apply_E and read_values/apply_O on the same state. The SCOPE docstring is updated to match (l.165-173).
   - This is consistent with B V002's declared `read_frame = fixed_current_state_reads`.

2. **A (frames, l.694-706, l.1436-1437).** Resolved.
   - `registration['port_vectors']` now accepts four forms, admitted by `_admit_frames` (l.868-921): one 4x3 table; {'A': 4x3, 'B': 4x3} per part (newborn a_j in A, b_j in B); a Mapping from every vertex label to a 4x3 table; or a callable `port_vectors(*, vertex)` called once per label.
   - Each table is validated by `_real_table` (l.850-865) for shape (4,3), real dtype and finiteness.
   - The frames are stored per vertex [NV,4,3] (l.832-847). Reads use the per-vertex frames (`_reads_from_z` l.1749-1754, einsum "nva,vai->nvi").
   - The REG0408 frames are {'A': T, 'B': -T}.
   - Resources report `frame_mode`, `frames_A_equal_register_table` and `frames_B_equal_negated_register_table` (l.842-843, l.1930-1932). This replaces the V001 `port_vectors_equal_register_spec`.
   - These are the only coarse R/S rows, so module B read sources and sampler H_c use the corrected moments, not output-only copies.

3. **A (_edge_table copies; hop_BA table).** Resolved.
   - `_edge_table` (l.625-648) returns ('map', dict) for a Mapping (V001 behaviour, entries validated eagerly) or ('accessor', callable). An accessor is never iterated.
   - `hop_BA` is removed (l.709-710).
   - `_edge_value` (l.1214-1242) calls `accessor(edge=(A label, B label))` only for edges that are actually met. It validates the value (real and finite; a complex h is rejected via `_edge_scalar` l.615-622) and caches it per edge until `release_caches()` (l.969-976).
   - A missing map entry or a failing accessor is an explicit failure that names the edge. At state level this comes from `_require_coverage`/`_raise_coverage` (l.1258-1274). In the build it is recorded per edge in `_discover` (l.1966-1971) and reported at the coverage stage (l.2211-2221).
   - `_amplitude` (l.1532-1552) forms -t e^{+i theta} per edge. The float operations are identical to V001.
   - A uniform profile is the caller's explicit accessor. There is no uniform default and no all-pairs iteration.

4. **A (registration port_vectors as corrected by 0409, plus the adapter alignment, whitening, normalization and reads items).**
   - **Frames:** resolved as in item 2. B vertices, including newborn b_j, carry the explicitly supplied frame, which for REG0408 is the negative frame.
   - **Whitening:** resolved. There is a new REQUIRED explicit `registration['whitening']`: a real, finite, nonsingular 3x3 W. A singular-value floor applies (l.821-827); `_REGISTRATION_KEYS` is at l.381-382.
     - W is folded exactly into the read frames as `frames_w = W f_v[a]` (l.841). This gives R' = W R and S' = W S W^T in every coarse row.
     - The dual sources j' = W^-T j and J' = W^-T J W^-1 are the coefficients on these rows (docstring l.140-153, L8 l.269-285).
     - The identity gives raw moments.
   - **Ports:** port_order is still called with the current neighbours of each new (vertex, neighbour set). The R/S normalization uses the current per-configuration m_alpha (unchanged).
   - **Full outgoing reads:** these are stated in the `read_rows` docstring (l.1861-1874): all rows are recomputed from the current graph, with no copied bits for Birth.
   - **Adapter alignment** (L14, l.338-350):
     - Accepted unchanged: its `port_order(*, vertex, neighbours)` (called by keyword with labels as V001 did), `UniformEdgeProfile` (called as `accessor(edge=(A,B))`, which its `__call__(self, edge)` accepts), and its g/kappa/epsilon dicts, cells, endpoint/owner_vertex allocation and uniform identity allocation.
     - Its `build_inputs` registration lacks the now-required 'whitening' key, so V002 fails closed naming that key. Its 'port_vectors' is the placeholder single A table, which V002 accepts as form (i) and flags with `frames_B_equal_negated_register_table = False`.
     - To make the operator rows equal `adapted_moment_reads`, root's binding must pass {'A': T, 'B': -T} and the companion's W. No value is chosen here.

5. **A (_edge_table / hop_BA, 0408 item 2).** Same change as item 3.

6. **A (state-level palette API, 0408 item 3).** Resolved.
   - New public `palette_channels(*, context, state, palette_owners)` (l.1837-1858), with `_admit_palette` (l.1820-1834) and `_palette_scope` (l.1415-1432).
   - Membership follows the intrinsic label rule of the palette move: Birth/reverse of owner j; site, degree, Bind and admission owners of v by v's permanent group; edge owners if either endpoint's group is in the palette; donors by their owner; C_identity never.
   - Only palette owners are enumerated. Birth uses per-owner witness search from root o_j (`_root_cuts` l.1043-1064, `_forward_channels` l.1067-1098, `_reverse_channels` l.1101-1157, cached per owner by `_owner_birth` l.1160-1166). It keeps every reverse pairing and the full eligibility tests (unchanged `_transitions` body, l.1502-1529).
   - Records come from the same `_diagonal_records`/`_transition_records` with complete supports, now taking a scope (`_full_scope` l.1408-1412).
   - The remaining global per-event costs are reported in L11 (l.307-321), L13 (l.325-337) and resources (`canonical_key_edge_code_space` and `state_level_per_event_global_costs`, l.1922-1929). These costs are: bit-set keys over NA*NB codes (O(NA*NB) bit operations per key operation, 2,359,296 codes at L=8); O(V+E) structure per new supporting graph; and full read recomputation per state.

7. **A (newborn_edge_mask, 0409 item 2).** Resolved.
   - `_admit_graph0` (l.567-572) no longer builds any mask, and `_vertex_present` is removed.
   - `_weights` (l.1555-1591) takes vertices known to be present. `_birth_weights` (l.1615-1630) passes a_j and b_j only on the side where slot j is active, which is the forward target or the reverse source, using the new channel flag `newborn_at_target` (l.1094, l.1152).
   - This is identical to V001 on every admitted configuration, because `_graph_info` admits a newborn iff it has degree four and its pair is active. This is a representation change only. Reachable graphs and Birth/reverse eligibility are unchanged.

8. **A (edge-profile accessors as the adapter defines).** Resolved as in item 3. The accessor is called with keyword `edge=(A label, B label)`, the ordered current pair. Every returned h, t and theta is validated as real and finite (h complex rejected), with no all-pairs iteration.

9. **A (registration defaults, 0408 root allocation).** Confirmed, no code change. L2 (l.228-236) documents it.
   - `'endpoint_anchors_only'` adds no edge anchor (`_weights` edge anchors only if `edge_mode`).
   - `'owner_vertex'` maps each donor factor to the owner's own vertex anchor (0, o_j). The anchors form a set, so the owner is counted once and never multiplied by the two donor factors.
   - `identity_allocation` {cell: 1/n_cells} over the original cells is admitted (|sum-1| <= 1e-12; 1/216 x 216 at L=6 is within 3e-14), with C_identity explicit.

## Judgements (not treated as module-A code defects)

- **Issue 1 computation.** The commutator means, K' term, tangent derivatives and bounds are computed in module B, as the issue's primary location says. Duplicating them as an A member would create a second source of truth for K(t) and for the node bounds. A's part was the missing read/frame time-dependence statement and the delegation wording, both now fixed.
- **Global single-table port_vectors kept.** This is form (i), an explicit REGISTER-spec common-frame member. Rejecting it would break the adapter's validated schema without adding safety; it is flagged in resources and in L8/L14. REG0408 requires form (ii), (iii) or (iv).
- **'whitening' made required.** "Explicit registration input" admits no default. The cost is one key in root's binding, which must also change its placeholder frame.
- **Not changed** (outside the blocking list):
  - the canonical key representation;
  - `_bits` speed;
  - the L12 wording note;
  - the identity-allocation tolerance note from the static review.
  The global costs are reported instead.

## Scope of change (everything else unchanged)

- **Order and types.** Birth records are now ordered by owner, then by cut, not by cut, then by witness.
- **Records.** Records are unaggregated and order-free. No duplicate (target, source) pair can arise among Birth records: distinct owners give distinct slots, distinct cuts give distinct target graphs, and distinct pairings give distinct predecessors. Build aggregation is therefore unaffected.
- **Unchanged behaviour.** Diagonal, native and Birth semantics, supports, weights, keys, caps, assembly, norm bounds and the reference family are unchanged. `diff -w` confirms that `_forward_channels` and `_reverse_channels` are re-indented, with only the per-owner entry and exit lines changed.

## AST check (python3 -I -B, ast.parse plus in-memory compile of the V002 TEXT, Python 3.9.6)

- **Imports.** cmath, math, sys, array.array, collections.abc.Mapping, itertools (permutations, product), typing.NamedTuple, numpy (unchanged). No scipy, warnings, os or threading.
- **Banned constructs.** No MatMult/'@'. No dot, matmul, vdot, inner, tensordot, outer or kron. No errstate. No print, open, exec, eval, input, compile, __import__ or globals. No lambda, global/nonlocal, yield or async.
- **einsum.** Every einsum call has `optimize=False`, including the new "ij,vaj->vai" and "nva,vai->nvi".
- **Module top level.** Only the docstring, imports, defs, classes and literal constants. Nothing executes at import.
- **Public callables.** There are 23 (V001: 22, plus `palette_channels`). All are keyword-only with zero defaults.
- **Unused private functions.** None.
- **Undefined names.** The only one flagged is `ev`→`dom`, which is the enclosing-scope closure already present in V001 (`_support_labels`).

## diff -u owned_parent_operator_v001.py owned_parent_operator_v002.py

```diff
--- owned_parent_operator_v001.py	2026-10-16 03:33:56.460232027 -0500
+++ owned_parent_operator_v002.py	2026-10-16 04:15:24.940270363 -0500
@@ -1,9 +1,33 @@
-"""Owned-parent operator adapter V001 -- UNT task 0405, contract section 11(A).
+"""Owned-parent operator adapter V002 -- UNT task 0405, contract section 11(A).
 
-STATUS. Static author implementation (AUTHOR A). Its author never imported or
-executed it, any legacy module, or any UNT/Codex module. It contains no numerical
-control, no propagation, no data extraction and no parameter value. Every physical
-coefficient, profile, registration and state is explicit caller input.
+STATUS. Static fix of V001 (owned_parent_operator_v001.py sha256
+27ad1762dbdc559eb92edcb6f7fe83790b73a4e23d71b12500b8586c811de3b6, preserved unchanged) by the
+module-A fix author. Only the blocking review issues are changed (REVIEW_0405_FIDELITY_V001.md
+dfd97e2fa36a6510599245a3629106c1e51df3a2d75aa381d1b163ddecf5fd46, 0408, 0409): per-vertex/per-part
+frames and an explicit fixed whitening inside the coarse reads; lazy validated edge-profile
+accessors; a basis-free palette channel enumeration with per-owner C_loc; presence from slots
+instead of all-potential-edge newborn masks; the read time-dependence statement for the ADDENDUM
+item 1 derivatives. Its author never imported or executed it, any legacy module, or any UNT/Codex
+module. It contains no numerical control, no propagation, no data extraction and no parameter
+value. Every physical coefficient, profile, registration and state is explicit caller input.
+
+V002 ADDITIONAL BINDINGS (sha256 computed from bytes before editing)
+  0408      XCH/FROM_CODEX/0408_2026-10-16_collective_palette_and_physical_registration_binding.md
+            c0f0eaa940ce95c495fa2d7c21d59cae2a49e8028cc084df878d203e3c42e341  (items 1-3, root allocation)
+  0409      XCH/FROM_CODEX/0409_2026-10-16_actual_adapter_and_remaining_all_pair_allocation.md
+            53465ac03cfb88bc7e641c15d8659591a315eafabb77dd966890e6dfb4ebb73c  (B = -A frames; newborn masks)
+  REG0408   UPC/helpers/recovered_packet_audit/OWNED_DIAMOND_CURRENT_GRAPH_COLLECTIVE_REGISTRATION_PROPOSED_V001.json
+            f65dbc234ae082df342235b1a6c13a0282cf94665ba3e1c3989d12b12e7d7174  (API semantics only)
+  WHITEN    UPC/helpers/recovered_packet_audit/OWNED_DIAMOND_WHITENING_DUAL_SOURCE_MANDATORY_COMPANION_V001.json
+            9eb4861cce5e4c435a259811dbca289e7e95a2b4ac34732c9f6c3ee56c34d7d7  (API semantics only)
+  PALETTE   UPC/helpers/coefficient_method/OWNED_WORLDLINE_BLOCKED_PALETTE_MOVE_IMPLEMENTATION_V001.txt
+            3b06ee3392894de2e96716c86f7b3184c792a407a81435f95aa448440418ca16  (palette membership rule)
+  HPTIME    UPC/helpers/response_packet_audit/SAME_ACTION_COVARIANCE_VOLUME_TIME_DERIVATIVES_ADDENDUM_V001.md
+            2fc9dc2c0197d6b3d0e2ff5893ba32b7ef89ba5424680bc06bd5210d5207226a  (L_O, A_O; see L9)
+  ADAPTER   UPC/helpers/coefficient_method/owned_diamond_registration_input_adapter_v001.py
+            0705be7ca500a3b8329566ba014b80645231be2178ad5b8ef089dbca163b3f77  (root-owned, read as TEXT
+            only, never imported or executed; its port_order and UniformEdgeProfile signatures are
+            admitted as written, see L14)
 
 BINDING SPECIFICATION (each sha256 computed from bytes before authoring)
   UPC = /Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13
@@ -90,7 +114,10 @@
   cut's opposite endpoints, exactly one cut edge meets the root, the four same-part endpoints are
   distinct. Unordered cuts are deduplicated across witnesses. Channel (G, C, j) exists iff original
   o_j witnesses C, slot j is absent, donors (o_j,0),(o_j,1) are RR and the cut census is exactly two;
-  each (G, C, j) once, no multiplicity factor. Surgery deletes the four cut edges (u, v), u in A,
+  each (G, C, j) once, no multiplicity factor. V002: the witness set W_G(C) is exactly the set of
+  roots whose local search generates C, so the channels of owner j are generated from root o_j
+  alone (per-owner, lazily cached per graph); the channel set is identical to V001's global C_loc
+  pass followed by the witness filter. Surgery deletes the four cut edges (u, v), u in A,
   v in B, adds children (u, b_j) and (a_j, v) each carrying the cut bit, keeps every other factor and
   bit, inserts a_j, b_j in R with p = q = 0, and sends the donor pair RR -> II (loaded map, not the
   PRIMARY blank-I BirthMap.encode l.145). birth_rev at an active slot enumerates all 4! pairings of
@@ -114,10 +141,16 @@
   (present or not): presence indicator; four presence-masked single-port Z_(v,a) = 1-2 n_(e_a); six
   pair reads Z_a Z_b; ports ordered by the caller's deterministic registration['port_order'] on the
   CURRENT neighbours. Per coarse cell alpha: population m_alpha (present vertices, newborns in their
-  owner's cell), R_alpha,i = (1/m_alpha) sum_v t_vi, S_alpha,ij = (1/m_alpha) sum_v t_vi t_vj with
-  t_v = sum_a Z_va port_vectors[a] and 1/m_alpha a current-state factor inside the operator. Absent
-  rows have value 0 and presence 0 (no conditional normalization). Raw first and second moments are
-  separate rows; centring (C = M - mu mu^T) is a caller-side combination.
+  owner's cell), R_alpha,i = (1/m_alpha) sum_v (W t_v)_i, S_alpha,ij = (1/m_alpha) sum_v (W t_v)_i
+  (W t_v)_j with t_v = sum_a Z_va f_v[a], f_v the REGISTERED frame of vertex v (V002: global,
+  per-part, per-vertex table or callable; the 0408 registration has B frames = -A frames, which no
+  port permutation produces), W = registration['whitening'] (explicit fixed 3x3; identity for raw
+  moments), and 1/m_alpha a current-state factor inside the operator. These corrected moments are
+  the ONLY coarse R/S rows: read_rows, read_values, apply_O, and therefore every source column, H_c
+  source and source derivative built on these rows, use the same frames and whitening (dual sources
+  j' = W^-T j, J' = W^-T J W^-1 are the coefficients on these rows). Absent rows have value 0 and
+  presence 0 (no conditional normalization). Raw first and second moments are separate rows;
+  centring (C = M - mu mu^T) is a caller-side combination.
 
 PHASE CONVENTION. For stable edge (a, b), a in A, b in B, the carrier transfer b -> a has amplitude
   -t_e exp(+i theta_e) and a -> b has -t_e exp(-i theta_e), its exact conjugate. This is the PRIMARY
@@ -125,13 +158,19 @@
   l.259-261, with edges (u in A, v in B) as in periodic_q4 l.92). The ADDITIONAL one-carrier code
   (root_native_shared_parent_clock_transport_v001.py l.77-79) gives +theta to A -> B; the contract
   binds the PRIMARY convention, so the two differ by theta -> -theta. theta_e, t_e, h_e are keyed
-  by the current (A label, B label) pair; zero phase is never inferred.
-
-SCOPE. Module A only: validated model/context, canonical keys, state-level primitive channels,
-  diagonal terms and reads (for samplers that never enumerate a basis), structural basis
-  enumeration with caps, matrix-free apply_H / apply_E / apply_O, read arrays, norm bounds,
-  resources, and the optional DECLARED reference family. No propagation, response contraction,
-  Legendre step, P/Q reduction, time derivative or physical state choice (module B / root).
+  by the current (A label, B label) pair; zero phase is never inferred. V002: each of h, t, theta
+  is an explicit Mapping or a caller accessor called as accessor(edge=(A label, B label)) only for
+  edges of configurations actually met; every accessed value is validated (L5).
+
+SCOPE. Module A only: validated model/context, canonical keys, state-level primitive channels
+  (complete or restricted to a declared owner palette), diagonal terms and reads (for samplers
+  that never enumerate a basis), structural basis enumeration with caps, matrix-free apply_H /
+  apply_E / apply_O, read arrays, norm bounds, resources, and the optional DECLARED reference
+  family. No propagation, response contraction, Legendre step, P/Q reduction or physical state
+  choice (module B / root). Native-time derivatives (ADDENDUM item 1, HPTIME): every read row and
+  E_alpha here is a fixed operator with zero explicit time/frame partial derivatives; the commutator
+  means <L_O>, <A_O> with the actual K, K' are formed by module B from apply_H, apply_E and the read
+  diagonals on its propagated state (L9).
 
 PUBLIC API (all keyword-only, no defaults; state-level functions raise ValueError on bad input)
   validate_owned_model(*, graph0, model, registration) -> {ok, stage_reached, failures, context}
@@ -142,6 +181,9 @@
       admit_rev, birth, birth_rev; target_state canonical key (None for diag); energy_weights a
       tuple over context.energy_cells of (w_alphaX(target) + w_alphaX(source))/2.
   diagonal_terms(*, context, state) -> the kind == 'diag' records of primitive_channels
+  palette_channels(*, context, state, palette_owners) -> the primitive_channels records whose
+      permanent owner lies in the declared palette of original owner labels (L13), without
+      enumerating the other owners (V002, 0408 item 3)
   read_rows(*, context, state) -> {labels, values float64 [n_read], presence float64 [n_read]}
   build_owned_operator(*, graph0, model, registration, seed_states, caps, dtype)
       -> {ok, stage_reached, failures, operator, resources}; operator members: dimension, dtype,
@@ -158,7 +200,10 @@
   alone has 2^(3V0) * C(2V0, V0) states (all incidence words times local states with N_c = S_g);
   for the smallest simple q4 bipartite graph (V0 = 8) that is about 2.2e11. A full build therefore
   exceeds any practical cap; build_owned_operator reports this and fails at the cap. The state-level
-  functions cost O(V + 108V + 24K) per call plus a one-off per-graph structure.
+  functions cost O(V + 108V + 24K) per call plus a one-off per-graph structure; palette_channels
+  evaluates only palette owners (O(s) natives, 108 root choices and 24 pairings per palette owner)
+  but keeps the global per-event costs listed in L11 (bit-set keys over NA*NB edge codes, per-graph
+  structure, globally normalized reads).
 
 LIMITATIONS: see the module constant LIMITATIONS (each ambiguity is implemented literally and listed).
 """
@@ -184,7 +229,11 @@
     anchor". The caller declares registration['donor_anchor']: 'owner_vertex' (each donor factor is
     the owner vertex anchor, counted once with it) or 'separate_at_owner_cell' (each donor factor is
     its own anchor in the owner's cell). Newborn cells are DERIVED from the owner cell (REGISTER) and
-    cannot be registered separately in this version.
+    cannot be registered separately in this version. The 0408 root-selected allocation is supported
+    exactly as written: edge_cells='endpoint_anchors_only' adds no edge anchor; donor_anchor=
+    'owner_vertex' makes each donor factor the owner's own vertex anchor, counted once together with
+    it (a set of distinct anchors; never multiplied by the two donor factors); identity_allocation
+    {cell: 1/n_cells} over the fixed original cells with the explicitly supplied C_identity.
 L3  Degree-feedback support. Ud, lambda_R and lambda_J owners at v support v plus its four incident
     edges (hence its four neighbours as endpoints), reading contract s.3 "incident-edge/endpoint
     anchors it queries". Birth support uses only the owner's own root o_j adjacency (the guard of
@@ -197,7 +246,18 @@
     rule on newborn/child edges is UNCHOSEN in the sources (0400 row 4, check E2); it is caller data
     keyed by the current (A,B) pair. The many-carrier matrix of T_e(theta != 0) is NOT WRITTEN in the
     sources (0400 row 2 (ii)); the edge-local hard-core exchange with the PRIMARY one-carrier phase
-    entry is implemented, as the contract binds.
+    entry is implemented, as the contract binds. V002 (0408 item 2, 0409): model['h'], ['t'] and
+    ['theta'] are each EITHER a Mapping (A label, B label) -> real (every supplied entry admitted
+    eagerly, as V001) OR a caller accessor, called as accessor(edge=(A label, B label)) with the
+    ordered current endpoint pair (root adapter UniformEdgeProfile accepts this), only for edges of
+    configurations actually evaluated -- never for all potential pairs (9 L^6 at L=8). Every
+    accessed value is validated when first accessed (real and finite; a complex h is rejected,
+    ADDENDUM 3) and cached per stable edge until release_caches(); the accessor must be a
+    deterministic function of the ordered pair. A uniform profile is the caller's explicit
+    accessor returning one value; this module has no uniform default. A missing Mapping entry or a
+    failing accessor is an explicit coverage failure naming the edge (state level: raised when a
+    configuration containing the edge is evaluated; build: reported after the structural closure);
+    no possible new edge is omitted or approximated.
 L6  Hop orientation follows the PRIMARY backend; the ADDITIONAL one-carrier reference has the
     opposite sign of theta. Records do not carry a hop direction; it is implied by the target.
 L7  Reference family. reference_preparation computes chi as the unique ground vector of the
@@ -206,14 +266,39 @@
     and consistent with the analytic control in the galaxy assembly note (l.522). If the declared
     full local H(2) is meant to contain more, pass chi explicitly. The family is a DECLARED reference,
     never a default state; a degenerate ground fails.
-L8  Ports. Port order is a caller callable of (current vertex label, current neighbour labels); it
-    must be deterministic. Results are cached per (vertex, neighbour set); release_caches() drops
-    the cache, after which a nondeterministic callable would change reads. The tetrahedral frame
-    table is registration['port_vectors']; the exact bound tr C <= 4 (||t_v||^2 = 4-(d_v-2)^2) holds
-    for the REGISTER table (+-1/2 rows) and is a documented property, never a clip.
-L9  Reads. Retained loop/count reads of the collective action are not implemented (additional outputs,
-    not requested here). Read values are float64. Native-time first/second derivatives of reads and
-    any K' generator terms (ADDENDUM 1) belong to module B.
+L8  Ports and frames. Port order is a caller callable of (current vertex label, current neighbour
+    labels), recomputed from the CURRENT graph (root adapter make_port_order: relative permanent
+    anchors, REG0408 current_port_ordering); it must be deterministic. Results are cached per
+    (vertex, neighbour set); release_caches() drops the cache, after which a nondeterministic
+    callable would change reads. V002 frames (0408 item 1 as corrected by 0409 item 1):
+    registration['port_vectors'] is (i) one real 4x3 table for every vertex, (ii) {'A': 4x3,
+    'B': 4x3} per bipartition part (newborn a_j in A, newborn b_j in B), (iii) a Mapping from EVERY
+    vertex label to a 4x3 table, or (iv) a callable port_vectors(*, vertex) -> 4x3, called once per
+    vertex label at validation. Every table is checked for shape (4, 3), real dtype and finiteness;
+    row a is the frame vector of port a. REG0408 (B frames are the NEGATIVES of the A frames with the
+    same index; no port permutation produces them) is form (ii) {'A': T, 'B': -T} or (iii)/(iv);
+    resources report frame_mode and whether the A/B frames equal T / -T for the REGISTER table T.
+    registration['whitening'] W (explicit real nonsingular 3x3; the identity gives raw moments) is
+    applied INSIDE the coarse operators, R' = W R and S' = W S W^T, implemented exactly as the
+    whitened frame vectors W f_v[a]. There is no second (raw) set of coarse R/S rows; the raw
+    per-vertex Z and ZZ rows remain. With frames T or -T at every vertex (||t_v||^2 = 4-(d_v-2)^2)
+    the raw bound tr C <= 4 holds, so tr C' <= 4 ||W||_2^2; documented properties, never clips.
+L9  Reads and time derivatives. Retained loop/count reads of the collective action are not
+    implemented (additional outputs, not requested here). Read values are float64. ADDENDUM item 1 /
+    HPTIME: every read row (presence, Z, ZZ, m, whitened R and S) and every E_alpha is a FIXED
+    operator on the canonical basis -- registration, frames, whitening, port order, cells and the
+    per-configuration 1/m_alpha are current-state functions with no explicit time, source or lapse
+    argument -- so the explicit read/frame partial derivatives VANISH: partial_tau O = partial_tau^2
+    O = 0, and exactly L_O = (i/hbar)[K,O], A_O = (i/hbar)[K',O] - [K,[K,O]]/hbar^2. Graph-sector
+    dependence of 1/m_alpha and of ports enters only through these commutators (Birth and reverse act
+    on them); an added count derivative would double count. All read rows are diagonal, so
+    [O_A, O_B] = 0 and only the H and E_alpha parts of K, K' contribute to a commutator with a read
+    row. The actual time-dependent K = H[n(t), j(t)]/N_bg and K' (source and lapse derivatives) live
+    with the propagated state in module B, which forms <L_O>, <A_O>, their tangent derivatives and
+    error bounds from apply_H, apply_E and read_values/apply_O on the SAME state (single source of
+    truth for K(t) and the node bounds); this module does not evaluate those means itself. A caller
+    who makes a registration, frame or read explicitly time dependent must add its partial
+    derivatives; no such input exists in this module.
 L10 Numerics. Amplitudes and weights are float64 Python values, then cast to the caller dtype for
     apply_*. norm_bound_* bound the STORED matrix (absolute column sums with an explicit summation
     inflation); rounding of stored coefficients relative to exact model values and matvec rounding
@@ -221,10 +306,47 @@
     E_alpha = H) use summation tolerances; they are internal consistency checks, not validation.
 L11 No compression, Krylov, P/Q reduction or memory kernel. The full basis is exponential (see COST);
     state-level functions are the route for samplers. Context caches grow with the number of distinct
-    supporting graphs visited; the caller bounds memory with release_caches().
+    supporting graphs visited; the caller bounds memory with release_caches(). Remaining GLOBAL
+    per-event costs of the basis-free functions (0408 item 3; honest report, not removed in V002):
+    (a) canonical keys are bit sets over fixed codes; the edgeset and inc ints span NA*NB edge codes
+    (NA = NB = V0/2 + K; 2,359,296 codes at L=8), and every key construction, XOR and bit test costs
+    O(NA*NB) bit operations whatever the palette size; (b) each distinct supporting graph (every
+    Birth or reverse target) builds O(V+E) structure once -- neighbour lists, q4/presence
+    validation, port_order lookups for every present vertex -- with bit extraction O(E*NA*NB), and
+    primitive_channels additionally checks profile coverage of every current edge once per graph;
+    (c) read_rows recomputes every read row of the state (presence, Z, ZZ and the per-cell
+    normalized coarse sums) by design: full outgoing reads after every transition, with ports
+    reassigned from the current graph and current populations, never a copied-bit shortcut for
+    Birth; (d) caches of graph structure, ports and accessor values grow with distinct graphs/edges.
+    Birth witness search is per original owner root (V002), so only evaluated owners pay for C_loc.
 L12 primitive_channels lists diagonal owners only where their operator element is structurally
     nonzero (e.g. epsilon_r only at q_v=1); failed Birth-reverse pairings and other exact zeros
     produce no record. Coefficient VALUES never remove a record (a zero coefficient gives amplitude 0).
+L13 Palette (V002, 0408 item 3, PALETTE). palette_channels(palette_owners) returns exactly the
+    primitive_channels records (same function, amplitudes, complete queried/changed supports and
+    weights) whose PERMANENT owner is in the declared palette, by the intrinsic label rule of
+    PALETTE: Birth/reverse of owner j iff j is in the palette; site, Bind, admission and degree
+    owners at vertex v iff the permanent group of v (v itself for an original, owner j for a_j and
+    b_j) is; edge owners (flip, hop, Delta) iff either endpoint's group is; donor owners iff their
+    owner is. C_identity has no owner and is never in a palette. All Birth reverse pairings and the
+    full current eligibility (current-graph witness, slot, donors, census, image tests) of palette
+    owners are kept. The diagonal records returned are only the palette-OWNED ones: a palette
+    transition can change diagonal owners outside the palette (e.g. Ud/lambda at the far endpoint of
+    a palette edge) and globally normalized reads; their values come from diagonal_terms/read_rows or
+    from the records' complete supports. Coverage is checked for the palette edges; Birth weights
+    query their own raw edges. The global per-event costs of L11 remain.
+L14 Root adapter alignment (ADAPTER, read as text only, not yet root-reviewed). Its
+    port_order(*, vertex, neighbours) and UniformEdgeProfile (called here as accessor(edge=(A, B)))
+    are admitted unchanged, as are its g/kappa/epsilon dicts, cells, original_cell,
+    'endpoint_anchors_only', 'owner_vertex' and uniform identity_allocation. Its build_inputs
+    registration has the seven V001 keys only: it lacks the now REQUIRED explicit
+    registration['whitening'] (no default), so validate_owned_model fails closed naming that key,
+    and its 'port_vectors' is a single A-frame table (the adapter's own comment calls it a
+    placeholder). For this operator's coarse rows to equal its adapted_moment_reads whitened R/S,
+    the binding must pass port_vectors {'A': T, 'B': -T} and the companion's whitening (WHITEN:
+    W = C0^(-1/2) with C0 = (4/3) I); then reads, module B read sources, sampler H_c sources and every
+    source derivative use one set of corrected moments, and pair_source_hamiltonian with
+    raw_to_whitened_sources is the same contraction expressed caller-side. No value is chosen here.
 """
 
 
@@ -257,7 +379,8 @@
                 "E_R", "E_S", "E_I", "e_R", "e_I", "C_identity")
 _PROFILE_KEYS = ("h", "t", "theta", "g", "kappa", "epsilon")
 _REGISTRATION_KEYS = ("cells", "original_cell", "edge_cells", "donor_anchor",
-                      "identity_allocation", "port_order", "port_vectors")
+                      "identity_allocation", "port_order", "port_vectors", "whitening")
+_EDGE_PROFILES = ("h", "t", "theta")
 _CAP_KEYS = ("max_dimension", "max_graphs", "max_events_per_row")
 _STATE_KEYS = ("slots", "edges", "occupied", "carriers", "records", "spent", "donors_ready")
 _EDGE_ENDPOINTS_ONLY = "endpoint_anchors_only"
@@ -386,11 +509,6 @@
     return np.frombuffer(buf, dtype=dtype) if len(buf) else np.zeros(0, dtype=dtype)
 
 
-def _vertex_present(dom, edgeset, v):
-    j = dom["newborn_slot"].get(v)
-    return True if j is None else bool(edgeset & dom["newborn_edge_mask"][v])
-
-
 # ---------------------------------------------------------------------------
 # Admission of graph0, model and registration
 # ---------------------------------------------------------------------------
@@ -446,16 +564,12 @@
     owner_vid = [j if j < n_a0 else na + (j - n_a0) for j in range(k_slots)]
     a_vid = [n_a0 + j for j in range(k_slots)]
     b_vid = [na + n_b0 + j for j in range(k_slots)]
+    # V002 (0409 item 2): no all-potential-edge newborn masks. Newborn presence is slot occupancy
+    # (a_j, b_j present iff slot j is active), passed explicitly where it is needed (_birth_weights).
     newborn_slot = {}
-    newborn_edge_mask = {}
     for j in range(k_slots):
         newborn_slot[a_vid[j]] = j
         newborn_slot[b_vid[j]] = j
-        newborn_edge_mask[a_vid[j]] = ((1 << nb) - 1) << (a_vid[j] * nb)
-        mask = 0
-        for ia in range(na):
-            mask |= 1 << (ia * nb + (b_vid[j] - na))
-        newborn_edge_mask[b_vid[j]] = mask
     label_order = list(owner_vid)
     for j in range(k_slots):
         label_order.extend((a_vid[j], b_vid[j]))
@@ -466,7 +580,7 @@
         "owner_index": {o: j for j, o in enumerate(originals)},
         "owner_vid": owner_vid, "owner_of_original": {v: j for j, v in enumerate(owner_vid)},
         "a_vid": a_vid, "b_vid": b_vid, "newborn_slot": newborn_slot,
-        "newborn_edge_mask": newborn_edge_mask, "label_order": label_order,
+        "label_order": label_order,
     }
     edges = graph0["edges"]
     if not isinstance(edges, (list, tuple)):
@@ -498,10 +612,29 @@
     return dom
 
 
+def _edge_scalar(name, value, failures, flip_note):
+    """One admitted real edge coefficient (complex flip h rejected, 0406 item 3; ADDENDUM 3)."""
+    if flip_note and isinstance(value, (complex, np.complexfloating)):
+        failures.append(f"{name}: complex flip coefficient {value!r} rejected (0406 item 3; "
+                        "ADDENDUM 3): -h_e X_e is Hermitian only for real h_e and a complex value is "
+                        "never copied to both directions")
+        return None
+    return _real(name, value, failures)
+
+
 def _edge_table(dom, name, table, failures, flip_note):
+    """Edge profile: ('map', {code: real}) from a Mapping, or ('accessor', callable) (V002, L5).
+
+    A Mapping is admitted entry by entry as in V001. An accessor is NOT iterated: it is called as
+    accessor(edge=(A label, B label)) only for edges actually met, and each value is validated then
+    (_edge_value). Anything else fails.
+    """
     if not isinstance(table, Mapping):
-        failures.append(f"{name}: a mapping (A label, B label) -> real is required")
-        return {}
+        if callable(table):
+            return ("accessor", table)
+        failures.append(f"{name}: a mapping (A label, B label) -> real or an accessor "
+                        "accessor(edge=(A label, B label)) -> real is required")
+        return ("map", {})
     out = {}
     for key, value in table.items():
         c = _edge_from_labels(dom, key)
@@ -509,15 +642,10 @@
             failures.append(f"{name}: key {key!r} is not an ordered bipartite pair (A label, B label) "
                             "of declared vertex labels")
             continue
-        if flip_note and isinstance(value, (complex, np.complexfloating)):
-            failures.append(f"{name}[{key!r}]: complex flip coefficient {value!r} rejected (0406 item 3; "
-                            "ADDENDUM 3): -h_e X_e is Hermitian only for real h_e and a complex value is "
-                            "never copied to both directions")
-            continue
-        x = _real(f"{name}[{key!r}]", value, failures)
+        x = _edge_scalar(f"{name}[{key!r}]", value, failures, flip_note)
         if x is not None:
             out[c] = x
-    return out
+    return ("map", out)
 
 
 def _vertex_table(dom, name, table, failures, kind):
@@ -578,9 +706,8 @@
     out["epsilon"] = eps
     if failures:
         return None
-    # Oriented hop amplitude b -> a (PRIMARY l.259-261 convention, see module docstring).
-    out["hop_BA"] = {c: -out["t"][c] * cmath.exp(1j * out["theta"][c])
-                     for c in out["t"] if c in out["theta"]}
+    # V002 (0408 item 2): no materialized hop table; the oriented hop amplitude b -> a
+    # (PRIMARY l.259-261 convention) is formed per accessed edge in _amplitude.
     return out
 
 
@@ -691,34 +818,109 @@
         identity = tuple((a, fr[a]) for a in sorted(fr) if fr[a] != 0.0)
     if not callable(registration["port_order"]):
         failures.append("registration['port_order']: a callable port_order(*, vertex, neighbours) is required")
-    pv_in = None
-    if isinstance(registration["port_vectors"], (list, tuple, np.ndarray)):
-        try:
-            pv_in = np.asarray(registration["port_vectors"])
-        except (TypeError, ValueError):
-            pv_in = None
-    pv = None
-    if pv_in is None or pv_in.dtype.kind not in "iuf" or pv_in.shape != (4, 3):
-        failures.append("registration['port_vectors']: a real 4x3 tetrahedral frame table is required")
-    else:
-        pv = pv_in.astype(np.float64)
-        if not np.all(np.isfinite(pv)):
-            failures.append("registration['port_vectors']: entries must be finite")
+    frames, frame_mode = _admit_frames(dom, registration["port_vectors"], failures)
+    whitening = _real_table("registration['whitening']", registration["whitening"], (3, 3), failures)
+    if whitening is not None:
+        sv = np.linalg.svd(whitening, compute_uv=False)
+        if not sv[-1] > 64.0 * np.finfo(np.float64).eps * sv[0]:
+            failures.append("registration['whitening']: a nonsingular real 3x3 matrix W is required "
+                            "(dual sources j' = W^-T j need W invertible; pass the identity for raw moments)")
     if failures:
         return None
     cell_vids = [np.array([v for v in dom["label_order"] if cell_vid[v] == a], dtype=np.int64)
                  for a in range(len(cells))]
+    na = dom["NA"]
+    table = np.array(_REGISTER_SPEC_PORT_VECTORS, dtype=np.float64)
     return {
         "cells": tuple(cells), "cell_index": cell_index, "cell_vid": cell_vid,
         "edge_mode": edge_mode, "edge_cell": edge_cell, "donor_mode": donor_mode,
-        "identity": identity, "port_order": registration["port_order"], "port_vectors": pv,
-        "port_vectors_equal_register_spec": bool(np.array_equal(pv, np.array(_REGISTER_SPEC_PORT_VECTORS))),
+        "identity": identity, "port_order": registration["port_order"],
+        # V002 (0408 item 1, 0409 item 1, WHITEN): registered per-vertex frames [NV, 4, 3] and the
+        # fixed whitening W, folded exactly into the read frames W f_v[a] used by every coarse row.
+        "frames": frames, "frame_mode": frame_mode, "whitening": whitening,
+        "frames_w": np.einsum("ij,vaj->vai", whitening, frames, optimize=False),
+        "frames_A_equal_register_table": bool(np.all(frames[:na] == table)),
+        "frames_B_equal_negated_register_table": bool(np.all(frames[na:] == -table)),
         "w_site": [((cell_vid[v], 1.0),) for v in range(dom["NV"])],
         "w_donor": [((cell_vid[dom["owner_vid"][d // 2]], 1.0),) for d in range(2 * dom["K"])],
         "cell_vids": cell_vids,
     }
 
 
+def _real_table(name, value, shape, failures):
+    """A finite real float64 array of exactly the given shape, or None with a failure."""
+    arr = None
+    if isinstance(value, (list, tuple, np.ndarray)):
+        try:
+            arr = np.asarray(value)
+        except (TypeError, ValueError):
+            arr = None
+    if arr is None or arr.dtype.kind not in "iuf" or arr.shape != shape:
+        failures.append(f"{name}: a real array of shape {shape} is required")
+        return None
+    out = arr.astype(np.float64)
+    if not np.all(np.isfinite(out)):
+        failures.append(f"{name}: entries must be finite")
+        return None
+    return out
+
+
+def _admit_frames(dom, spec, failures):
+    """Registered frame of every vertex label, float64 [NV, 4, 3] (V002, L8).
+
+    spec: a 4x3 table for every vertex ('global'); {'A': 4x3, 'B': 4x3} by bipartition part,
+    newborn a_j in A and b_j in B ('per_part'); a Mapping from every vertex label to a 4x3 table
+    ('per_vertex_table'); or a callable spec(*, vertex) -> 4x3 called once per vertex label
+    ('per_vertex_callable'). Row a of a table is the frame vector of port a.
+    """
+    nv, na = dom["NV"], dom["NA"]
+    labels = dom["labels"]
+    frames = np.zeros((nv, 4, 3), dtype=np.float64)
+    name = "registration['port_vectors']"
+    if isinstance(spec, Mapping):
+        if set(spec.keys()) == {"A", "B"}:
+            mode = "per_part"
+            ta = _real_table(f"{name}['A']", spec["A"], (4, 3), failures)
+            tb = _real_table(f"{name}['B']", spec["B"], (4, 3), failures)
+            if ta is not None and tb is not None:
+                frames[:na] = ta
+                frames[na:] = tb
+        else:
+            mode = "per_vertex_table"
+            seen = set()
+            for key, value in spec.items():
+                v = dom["vid"].get(key) if _is_label(key) else None
+                if v is None:
+                    failures.append(f"{name}: key {key!r} is neither a declared vertex label nor the "
+                                    "per-part pair 'A', 'B'")
+                    continue
+                t = _real_table(f"{name}[{key!r}]", value, (4, 3), failures)
+                if t is not None:
+                    frames[v] = t
+                    seen.add(v)
+            missing = [labels[v] for v in range(nv) if v not in seen]
+            if missing:
+                failures.append(f"{name}: no frame for vertex labels {missing!r} (a per-vertex table "
+                                "covers every vertex that can appear; no default)")
+    elif callable(spec):
+        mode = "per_vertex_callable"
+        for v in range(nv):
+            try:
+                got = spec(vertex=labels[v])
+            except Exception as exc:  # a caller registration failure becomes an explicit failure
+                failures.append(f"{name} raised {type(exc).__name__} ({exc}) for vertex {labels[v]!r}")
+                continue
+            t = _real_table(f"{name}(vertex={labels[v]!r})", got, (4, 3), failures)
+            if t is not None:
+                frames[v] = t
+    else:
+        mode = "global"
+        t = _real_table(name, spec, (4, 3), failures)
+        if t is not None:
+            frames[:] = t
+    return frames, mode
+
+
 def _read_layout(dom, reg):
     """Typed read labels and their internal specs (same order everywhere)."""
     labels, specs = [], []
@@ -751,7 +953,8 @@
 
     Built by validate_owned_model. Attributes: energy_cells (ordered cell labels), read_labels
     (typed read rows), vertex_labels, owners. Caches are pure functions of the validated inputs
-    and the current graph; release_caches() drops them (see LIMITATIONS L8, L11).
+    and the current graph (and of deterministic caller accessors); release_caches() drops them
+    (see LIMITATIONS L5, L8, L11).
     """
 
     def __init__(self, *, dom, model, reg):
@@ -764,11 +967,13 @@
         self.read_labels, self._read_spec = _read_layout(dom, reg)
         self._infos = {}
         self._ports = {}
+        self._edge_values = {name: {} for name in _EDGE_PROFILES}
 
     def release_caches(self):
-        """Drop cached per-graph structure and port orders; they are rebuilt on demand."""
+        """Drop cached per-graph structure, port orders and accessor values; rebuilt on demand."""
         self._infos = {}
         self._ports = {}
+        self._edge_values = {name: {} for name in _EDGE_PROFILES}
 
 
 def validate_owned_model(*, graph0, model, registration):
@@ -777,14 +982,18 @@
     graph0: {'A': [...], 'B': [...], 'edges': [(A label, B label), ...],
              'slots': {original label: (a_j label, b_j label)}}  -- simple bipartite q4, K = V0.
     model: real Delta, Ud, dstar, epsilon_c, epsilon_r, lambda_R, lambda_J, E_R, E_S, E_I, e_R,
-           e_I, C_identity; 'h', 't', 'theta': {(A label, B label): real} (h real; coverage of
-           every edge that occurs is checked when a graph containing it is met); 'g': {vertex:
-           real}, 'kappa': {vertex: complex} for EVERY vertex label; 'epsilon': {owner: complex}.
+           e_I, C_identity; 'h', 't', 'theta': each {(A label, B label): real} or an accessor
+           accessor(edge=(A label, B label)) -> real, called lazily per edge met (h real; coverage
+           of every edge that occurs is checked when a graph containing it is met; L5); 'g':
+           {vertex: real}, 'kappa': {vertex: complex} for EVERY vertex label; 'epsilon':
+           {owner: complex}.
     registration: 'cells' (ordered labels), 'original_cell' {original: cell}, 'edge_cells'
            ('endpoint_anchors_only' or {(A,B): cell}), 'donor_anchor' ('owner_vertex' or
            'separate_at_owner_cell'), 'identity_allocation' {cell: fraction, sum 1},
            'port_order' callable(*, vertex, neighbours) -> ordered neighbour labels,
-           'port_vectors' real 4x3 frame table.
+           'port_vectors' frames: one real 4x3 table, {'A': 4x3, 'B': 4x3}, {vertex label: 4x3}
+           for every vertex, or callable(*, vertex) -> 4x3 (L8), 'whitening' explicit real
+           nonsingular 3x3 W applied inside the coarse R/S reads (identity for raw moments).
     Returns {'ok', 'stage_reached', 'failures', 'context'}; context is an OwnedModelContext.
     """
     result = {"ok": False, "stage_reached": "inputs", "failures": [], "context": None}
@@ -831,125 +1040,134 @@
     return out
 
 
-def _c_loc(dom, nbrs):
-    """C_loc(G) of the CURRENT graph (CLOC l.7; LEDGER l.13): cut -> witnessing roots.
+def _root_cuts(dom, nbrs, root):
+    """Cuts of C_loc(G) in the CURRENT graph witnessed by one root (CLOC l.7; LEDGER l.13).
 
-    For every root (both bipartition mirrors) and every choice of the root's single cut edge,
-    each other neighbour x is matched to a neighbour of x other than the root, with distinct
-    endpoints. Unordered cuts are deduplicated across all witnesses and orientations.
+    For every choice of the root's single cut edge, each other neighbour x is matched to a
+    neighbour of x other than the root, with distinct endpoints. This is V001's _c_loc rule for a
+    single root: the witness set W_G(C) is exactly the set of roots generating C, so the channels
+    (G, C, j) with o_j in W_G(C) are the cuts generated from root o_j (V002 per-owner evaluation).
+    Unordered cuts are deduplicated.
     """
-    out = {}
-    for root in nbrs:
-        rn = nbrs[root]
-        for k in range(4):
-            others = [rn[i] for i in range(4) if i != k]
-            cands = [[w for w in nbrs[x] if w != root] for x in others]
-            for ch in product(*cands):
-                if ch[0] == ch[1] or ch[0] == ch[2] or ch[1] == ch[2]:
-                    continue
-                cut = [_code_any(dom, root, rn[k])]
-                for i in range(3):
-                    cut.append(_code_any(dom, ch[i], others[i]))
-                out.setdefault(tuple(sorted(cut)), set()).add(root)
-    return {cut: tuple(sorted(w)) for cut, w in out.items()}
+    out = set()
+    rn = nbrs[root]
+    for k in range(4):
+        others = [rn[i] for i in range(4) if i != k]
+        cands = [[w for w in nbrs[x] if w != root] for x in others]
+        for ch in product(*cands):
+            if ch[0] == ch[1] or ch[0] == ch[2] or ch[1] == ch[2]:
+                continue
+            cut = [_code_any(dom, root, rn[k])]
+            for i in range(3):
+                cut.append(_code_any(dom, ch[i], others[i]))
+            out.add(tuple(sorted(cut)))
+    return sorted(out)
 
 
-def _forward_channels(dom, info):
-    """Owned Birth channels (G, C, j): C in C_loc(G), original o_j a witness, slot j absent."""
+def _forward_channels(dom, info, j):
+    """Owned Birth channels (G, C, j) of owner j: C in C_loc(G) witnessed by original o_j, slot j absent."""
     out = []
+    if (info["slots_mask"] >> j) & 1:
+        return out
     edgeset = info["edgeset"]
-    cl = _c_loc(dom, info["nbrs"])
-    for cut in sorted(cl):
-        for root in cl[cut]:
-            j = dom["owner_of_original"].get(root)
-            if j is None or (info["slots_mask"] >> j) & 1:
-                continue
-            a_new, b_new = dom["a_vid"][j], dom["b_vid"][j]
-            cutmask = 0
-            children = []
-            child_codes = []
-            for c in cut:
-                u, v = _edge_ends(dom, c)
-                cu, cv = _code(dom, u, b_new), _code(dom, a_new, v)
-                cutmask |= 1 << c
-                # Copy the cut bit to BOTH children (PRIMARY BirthMap.encode_incidence l.130-136,
-                # here with loaded Ready newborns and owned donors, GEN l.31-34).
-                children.append((1 << c, (1 << cu) | (1 << cv)))
-                child_codes.extend((cu, cv))
-            target = edgeset & ~cutmask
-            for _bit, cmask in children:
-                target |= cmask
-            root_other = tuple(c for c in info["port_codes"][root] if c not in cut)
-            out.append({
-                "j": j, "cut": cut, "cutmask": cutmask, "children": tuple(children),
-                "child_edges": tuple(child_codes), "root_other": root_other,
-                "target_edgeset": target,
-                "raw_edges": tuple(sorted(set(cut) | set(root_other) | set(child_codes))),
-                "c": None,
-            })
+    root = dom["owner_vid"][j]
+    a_new, b_new = dom["a_vid"][j], dom["b_vid"][j]
+    for cut in _root_cuts(dom, info["nbrs"], root):
+        cutmask = 0
+        children = []
+        child_codes = []
+        for c in cut:
+            u, v = _edge_ends(dom, c)
+            cu, cv = _code(dom, u, b_new), _code(dom, a_new, v)
+            cutmask |= 1 << c
+            # Copy the cut bit to BOTH children (PRIMARY BirthMap.encode_incidence l.130-136,
+            # here with loaded Ready newborns and owned donors, GEN l.31-34).
+            children.append((1 << c, (1 << cu) | (1 << cv)))
+            child_codes.extend((cu, cv))
+        target = edgeset & ~cutmask
+        for _bit, cmask in children:
+            target |= cmask
+        root_other = tuple(c for c in info["port_codes"][root] if c not in cut)
+        out.append({
+            "j": j, "cut": cut, "cutmask": cutmask, "children": tuple(children),
+            "child_edges": tuple(child_codes), "root_other": root_other,
+            "target_edgeset": target, "newborn_at_target": True,
+            "raw_edges": tuple(sorted(set(cut) | set(root_other) | set(child_codes))),
+            "c": None,
+        })
     return out
 
 
-def _reverse_channels(dom, info):
-    """Every candidate predecessor reconnection of every active slot with its graph-level tests.
+def _reverse_channels(dom, info, j):
+    """Every candidate predecessor reconnection of active slot j with its graph-level tests.
 
     State-level tests (child bits, census, newborn Ready p=q=0, donors II) are in _transitions.
     """
     out = []
+    if not (info["slots_mask"] >> j) & 1:
+        return out
     edgeset = info["edgeset"]
     nbrs = info["nbrs"]
     na = dom["NA"]
-    for j in _bits(info["slots_mask"]):
-        a_new, b_new = dom["a_vid"][j], dom["b_vid"][j]
-        u_side = nbrs[b_new]
-        v_side = nbrs[a_new]
-        if a_new in u_side:
-            continue  # a_j adjacent to b_j: no predecessor of the loaded map exists
-        star_ub = tuple(_code(dom, u, b_new) for u in u_side)
-        star_av = tuple(_code(dom, a_new, v) for v in v_side)
-        starmask = 0
-        for c in star_ub + star_av:
-            starmask |= 1 << c
-        o = dom["owner_vid"][j]
-        o_nbrs = nbrs[o]
-        for sigma in permutations(range(4)):
-            restored = tuple(_code(dom, u_side[i], v_side[sigma[i]]) for i in range(4))
-            if any((edgeset >> c) & 1 for c in restored):
-                continue  # duplicate old edge: zero
-            if o < na:
-                if o not in u_side:
-                    continue  # owner not a cut endpoint: no witness
-                i0 = u_side.index(o)
-                pred = (set(o_nbrs) - {b_new}) | {v_side[sigma[i0]]}
-                if pred != set(v_side):
-                    continue
-                root_other = tuple(_code(dom, o, w) for w in o_nbrs if w != b_new)
-            else:
-                if o not in v_side:
-                    continue
-                i0 = sigma.index(v_side.index(o))
-                pred = (set(o_nbrs) - {a_new}) | {u_side[i0]}
-                if pred != set(u_side):
-                    continue
-                root_other = tuple(_code(dom, u, o) for u in o_nbrs if u != a_new)
-            restmask = 0
-            for c in restored:
-                restmask |= 1 << c
-            pairs = tuple((star_ub[i], star_av[sigma[i]], restored[i]) for i in range(4))
-            child = tuple(sorted(star_ub + star_av))
-            out.append({
-                "j": j, "cut": tuple(sorted(restored)), "pairs": pairs, "starmask": starmask,
-                "child_edges": child, "root_other": root_other,
-                "target_edgeset": (edgeset & ~starmask) | restmask,
-                "newborn_mask": (1 << a_new) | (1 << b_new),
-                "raw_edges": tuple(sorted(set(restored) | set(root_other) | set(child))),
-                "c": None,
-            })
+    a_new, b_new = dom["a_vid"][j], dom["b_vid"][j]
+    u_side = nbrs[b_new]
+    v_side = nbrs[a_new]
+    if a_new in u_side:
+        return out  # a_j adjacent to b_j: no predecessor of the loaded map exists
+    star_ub = tuple(_code(dom, u, b_new) for u in u_side)
+    star_av = tuple(_code(dom, a_new, v) for v in v_side)
+    starmask = 0
+    for c in star_ub + star_av:
+        starmask |= 1 << c
+    o = dom["owner_vid"][j]
+    o_nbrs = nbrs[o]
+    for sigma in permutations(range(4)):
+        restored = tuple(_code(dom, u_side[i], v_side[sigma[i]]) for i in range(4))
+        if any((edgeset >> c) & 1 for c in restored):
+            continue  # duplicate old edge: zero
+        if o < na:
+            if o not in u_side:
+                continue  # owner not a cut endpoint: no witness
+            i0 = u_side.index(o)
+            pred = (set(o_nbrs) - {b_new}) | {v_side[sigma[i0]]}
+            if pred != set(v_side):
+                continue
+            root_other = tuple(_code(dom, o, w) for w in o_nbrs if w != b_new)
+        else:
+            if o not in v_side:
+                continue
+            i0 = sigma.index(v_side.index(o))
+            pred = (set(o_nbrs) - {a_new}) | {u_side[i0]}
+            if pred != set(u_side):
+                continue
+            root_other = tuple(_code(dom, u, o) for u in o_nbrs if u != a_new)
+        restmask = 0
+        for c in restored:
+            restmask |= 1 << c
+        pairs = tuple((star_ub[i], star_av[sigma[i]], restored[i]) for i in range(4))
+        child = tuple(sorted(star_ub + star_av))
+        out.append({
+            "j": j, "cut": tuple(sorted(restored)), "pairs": pairs, "starmask": starmask,
+            "child_edges": child, "root_other": root_other,
+            "target_edgeset": (edgeset & ~starmask) | restmask, "newborn_at_target": False,
+            "newborn_mask": (1 << a_new) | (1 << b_new),
+            "raw_edges": tuple(sorted(set(restored) | set(root_other) | set(child))),
+            "c": None,
+        })
     return out
 
 
+def _owner_birth(dom, info, j):
+    """(forward channels, reverse candidates) of owner j in this graph, built once on demand."""
+    hit = info["birth"].get(j)
+    if hit is None:
+        hit = (_forward_channels(dom, info, j), _reverse_channels(dom, info, j))
+        info["birth"][j] = hit
+    return hit
+
+
 def _graph_info(ctx, edgeset):
-    dom, mod, reg = ctx._dom, ctx._model, ctx._reg
+    dom = ctx._dom
     labels = dom["labels"]
     codes = _bits(edgeset)
     nb = {}
@@ -978,14 +1196,11 @@
     port_codes = {}
     for v in nbrs:
         port_codes[v] = tuple(_code_any(dom, v, w) for w in _port_order(ctx, v, nbrs[v]))
-    missing = {k: tuple(c for c in codes if c not in mod[k]) for k in ("h", "t", "theta")}
-    missing["edge_cells"] = tuple(c for c in codes if c not in reg["edge_cell"]) if reg["edge_mode"] else ()
-    info = {"edgeset": edgeset, "codes": tuple(codes), "nbrs": nbrs, "present": tuple(nbrs),
+    # V002: profile coverage is checked lazily (_require_coverage / palette edges) and Birth
+    # channels are built per owner on demand (_owner_birth); nothing is enumerated eagerly.
+    return {"edgeset": edgeset, "codes": tuple(codes), "nbrs": nbrs, "present": tuple(nbrs),
             "present_mask": present_mask, "slots_mask": slots_mask, "port_codes": port_codes,
-            "missing": missing, "w_edge": {}, "w_deg": {}}
-    info["fwd"] = _forward_channels(dom, info)
-    info["rev"] = _reverse_channels(dom, info)
-    return info
+            "coverage_ok": set(), "w_edge": {}, "w_deg": {}, "birth": {}}
 
 
 def _info_for(ctx, edgeset):
@@ -996,15 +1211,69 @@
     return info
 
 
-def _require_coverage(ctx, info, names):
-    miss = info["missing"]
-    parts = [f"{name} lacks edges {[_edge_labels(ctx._dom, c) for c in miss[name]]!r}"
-             for name in names if miss[name]]
+def _edge_value(ctx, name, c):
+    """Validated real value of edge profile name ('h', 't', 'theta') on stable edge code c (V002, L5).
+
+    A Mapping profile is looked up (admitted entry by entry at validation). An accessor is called
+    as accessor(edge=(A label, B label)) once per edge, validated and cached. Raises ValueError
+    naming the edge on a missing entry, an accessor exception or an inadmissible value.
+    """
+    kind, prof = ctx._model[name]
+    if kind == "map":
+        x = prof.get(c)
+        if x is None:
+            raise ValueError(f"model['{name}'] has no entry for stable edge {_edge_labels(ctx._dom, c)!r}")
+        return x
+    cache = ctx._edge_values[name]
+    x = cache.get(c)
+    if x is not None:
+        return x
+    edge = _edge_labels(ctx._dom, c)
+    try:
+        got = prof(edge=edge)
+    except Exception as exc:  # a caller accessor failure becomes an explicit failure
+        raise ValueError(f"model['{name}'] accessor raised {type(exc).__name__} ({exc}) for stable edge "
+                         f"{edge!r}") from exc
+    fails = []
+    x = _edge_scalar(f"model['{name}'](edge={edge!r})", got, fails, name == "h")
+    if fails:
+        raise ValueError("; ".join(fails))
+    cache[c] = x
+    return x
+
+
+def _edge_problem(ctx, name, c):
+    """None if edge code c is covered for name ('h', 't', 'theta', 'edge_cells'), else a message."""
+    if name == "edge_cells":
+        if ctx._reg["edge_mode"] and c not in ctx._reg["edge_cell"]:
+            return f"registration['edge_cells'] has no cell for stable edge {_edge_labels(ctx._dom, c)!r}"
+        return None
+    try:
+        _edge_value(ctx, name, c)
+    except ValueError as exc:
+        return str(exc)
+    return None
+
+
+def _raise_coverage(ctx, codes, names):
+    parts = []
+    for name in names:
+        for c in codes:
+            msg = _edge_problem(ctx, name, c)
+            if msg is not None:
+                parts.append(msg)
     if parts:
         raise ValueError("coefficient/registration coverage: " + "; ".join(parts)
                          + " (no default value and no zero-phase inference)")
 
 
+def _require_coverage(ctx, info, names):
+    """Coverage of every edge of the current graph; remembered per graph once satisfied."""
+    todo = tuple(name for name in names if name not in info["coverage_ok"])
+    _raise_coverage(ctx, info["codes"], todo)
+    info["coverage_ok"].update(todo)
+
+
 # ---------------------------------------------------------------------------
 # States: admission, canonical keys, labelled form
 # ---------------------------------------------------------------------------
@@ -1136,18 +1405,46 @@
 # The single source of truth: diagonal owners, transitions, amplitudes, weights, reads
 # ---------------------------------------------------------------------------
 
-def _diagonal_items(ctx, info, key):
+def _full_scope(ctx, info):
+    """Every primitive owner of the configuration (complete channel list)."""
+    k = ctx._dom["K"]
+    return {"codes": info["codes"], "vertices": info["present"], "donors": range(2 * k),
+            "owners": range(k), "identity": True}
+
+
+def _palette_scope(ctx, info, owners):
+    """Owners in a palette of original owner indices (PALETTE intrinsic label rule, L13).
+
+    Vertices: o_j, and a_j, b_j when slot j is active (a newborn's group is its owner). Edges: every
+    current edge with an endpoint among those vertices (either endpoint group in the palette).
+    Donors: (o_j, 0), (o_j, 1). Birth/reverse: owner j. C_identity: none.
+    """
+    dom = ctx._dom
+    verts = []
+    for j in owners:
+        verts.append(dom["owner_vid"][j])
+        if (info["slots_mask"] >> j) & 1:
+            verts.extend((dom["a_vid"][j], dom["b_vid"][j]))
+    verts.sort()
+    codes = sorted({c for v in verts for c in info["port_codes"][v]})
+    return {"codes": tuple(codes), "vertices": tuple(verts),
+            "donors": tuple(d for j in owners for d in (2 * j, 2 * j + 1)),
+            "owners": tuple(owners), "identity": False}
+
+
+def _diagonal_items(ctx, info, key, scope):
     """(name, ref, feature) with amplitude model[name]*feature; contract s.3 diagonal list.
 
     Feature values follow PRIMARY CanonicalJoin.channels l.253 (full lambda_J sum d*p).
+    scope selects the owners (_full_scope: all; _palette_scope: a palette).
     """
     _slots, _edgeset, inc, p, q, s, dm = key
     dstar = ctx._model["dstar"]
     out = []
-    for c in info["codes"]:
+    for c in scope["codes"]:
         if (inc >> c) & 1:
             out.append(("Delta", ("edge", c), 1.0))
-    for v in info["present"]:
+    for v in scope["vertices"]:
         d = 0
         for c in info["port_codes"][v]:
             d += (inc >> c) & 1
@@ -1165,76 +1462,85 @@
                 out.append(("lambda_R", ("degree", v), -float(d)))
         # M_v = 1: a present site is S or R; the I-cell projector (E_I) is identically zero here.
         out.append(("E_S", ("vertex", v), 1.0) if s & bit else ("E_R", ("vertex", v), 1.0))
-    for d in range(2 * ctx._dom["K"]):
+    for d in scope["donors"]:
         out.append(("e_R", ("donor", d), 1.0) if (dm >> d) & 1 else ("e_I", ("donor", d), 1.0))
-    out.append(("C_identity", ("identity",), 1.0))
+    if scope["identity"]:
+        out.append(("C_identity", ("identity",), 1.0))
     return out
 
 
-def _transitions(ctx, info, key):
+def _transitions(ctx, info, key, scope):
     """(kind, ref, target key) for every allowed primitive transition, before aggregation.
 
     Native channels after PRIMARY CanonicalJoin.channels l.256-269 and SECONDARY event_channels
     l.136-142 (XOR bit updates), with structural closure independent of coefficient values.
+    scope selects the owners (_full_scope: all; _palette_scope: a palette); every Birth channel
+    and every reverse pairing of a selected owner is evaluated with its full eligibility.
     """
     dom = ctx._dom
     slots, edgeset, inc, p, q, s, dm = key
     out = []
-    for c in info["codes"]:
+    for c in scope["codes"]:
         out.append(("flip", ("edge", c), (slots, edgeset, inc ^ (1 << c), p, q, s, dm)))
-    for c in info["codes"]:
+    for c in scope["codes"]:
         if (inc >> c) & 1:
             a, b = _edge_ends(dom, c)
             pa, pb = (p >> a) & 1, (p >> b) & 1
             if pa != pb:
                 out.append(("hop", ("edge", c, "B_to_A" if pb else "A_to_B"),
                             (slots, edgeset, inc, p ^ (1 << a) ^ (1 << b), q, s, dm)))
-    for v in info["present"]:
+    for v in scope["vertices"]:
         bit = 1 << v
         if p & bit:
             out.append(("bind", ("vertex", v), (slots, edgeset, inc, p, q ^ bit, s, dm)))
-    for v in info["present"]:
+    for v in scope["vertices"]:
         bit = 1 << v
         if not (s & bit) and not (p & bit):
             out.append(("admit", ("vertex", v), (slots, edgeset, inc, p | bit, q, s | bit, dm)))
         elif (s & bit) and (p & bit):
             out.append(("admit_rev", ("vertex", v), (slots, edgeset, inc, p ^ bit, q, s ^ bit, dm)))
-    for ch in info["fwd"]:
-        j = ch["j"]
-        if ((dm >> (2 * j)) & 3) == 3 and _popcount(inc & ch["cutmask"]) == 2:
-            new_inc = inc & ~ch["cutmask"]
-            for cbit, cmask in ch["children"]:
-                if inc & cbit:
-                    new_inc |= cmask
-            out.append(("birth", ("birth", ch),
-                        (slots | (1 << j), ch["target_edgeset"], new_inc, p, q, s, dm & ~(3 << (2 * j)))))
-    for ch in info["rev"]:
-        j = ch["j"]
-        if (dm >> (2 * j)) & 3 or (p | q | s) & ch["newborn_mask"]:
-            continue  # donors not II, or a newborn not Ready with p = q = 0: zero
-        census = 0
-        new_inc = inc & ~ch["starmask"]
-        equal = True
-        for ub, av, rc in ch["pairs"]:
-            x = (inc >> ub) & 1
-            if x != (inc >> av) & 1:
-                equal = False  # unequal paired child bits: zero (PRIMARY BirthMap.decode l.154-157)
-                break
-            census += x
-            if x:
-                new_inc |= 1 << rc
-        if equal and census == 2:
-            out.append(("birth_rev", ("birth", ch),
-                        (slots & ~(1 << j), ch["target_edgeset"], new_inc, p, q, s, dm | (3 << (2 * j)))))
+    for j in scope["owners"]:
+        for ch in _owner_birth(dom, info, j)[0]:
+            if ((dm >> (2 * j)) & 3) == 3 and _popcount(inc & ch["cutmask"]) == 2:
+                new_inc = inc & ~ch["cutmask"]
+                for cbit, cmask in ch["children"]:
+                    if inc & cbit:
+                        new_inc |= cmask
+                out.append(("birth", ("birth", ch),
+                            (slots | (1 << j), ch["target_edgeset"], new_inc, p, q, s, dm & ~(3 << (2 * j)))))
+    for j in scope["owners"]:
+        for ch in _owner_birth(dom, info, j)[1]:
+            if (dm >> (2 * j)) & 3 or (p | q | s) & ch["newborn_mask"]:
+                continue  # donors not II, or a newborn not Ready with p = q = 0: zero
+            census = 0
+            new_inc = inc & ~ch["starmask"]
+            equal = True
+            for ub, av, rc in ch["pairs"]:
+                x = (inc >> ub) & 1
+                if x != (inc >> av) & 1:
+                    equal = False  # unequal paired child bits: zero (PRIMARY BirthMap.decode l.154-157)
+                    break
+                census += x
+                if x:
+                    new_inc |= 1 << rc
+            if equal and census == 2:
+                out.append(("birth_rev", ("birth", ch),
+                            (slots & ~(1 << j), ch["target_edgeset"], new_inc, p, q, s, dm | (3 << (2 * j)))))
     return out
 
 
-def _amplitude(model, kind, ref):
-    """Primitive amplitudes; every reverse is the exact conjugate of its forward (ADDENDUM 3)."""
+def _amplitude(ctx, kind, ref):
+    """Primitive amplitudes; every reverse is the exact conjugate of its forward (ADDENDUM 3).
+
+    Edge profiles are read through _edge_value (validated Mapping entry or accessor value, V002).
+    The oriented hop b -> a is -t_e exp(+i theta_e) (PRIMARY l.259-261); a -> b is its conjugate.
+    """
+    model = ctx._model
     if kind == "flip":
-        return complex(-model["h"][ref[1]])
+        return complex(-_edge_value(ctx, "h", ref[1]))
     if kind == "hop":
-        z = model["hop_BA"][ref[1]]
+        c = ref[1]
+        z = -_edge_value(ctx, "t", c) * cmath.exp(1j * _edge_value(ctx, "theta", c))
         return z if ref[2] == "B_to_A" else z.conjugate()
     if kind == "bind":
         return complex(model["g"][ref[1]])
@@ -1246,10 +1552,13 @@
     return z if kind == "birth" else z.conjugate()
 
 
-def _weights(ctx, edgeset, raw_edges, raw_vertices, raw_donors):
+def _weights(ctx, edgeset, raw_edges, present_vertices, raw_donors):
     """V002 equal-weight support fractions at the configuration whose graph is edgeset.
 
-    Only anchors PRESENT in that configuration count; each distinct anchor once.
+    Only anchors PRESENT in that configuration count; each distinct anchor once. Raw edges are
+    tested against edgeset; present_vertices are vertex anchors the caller knows to be present in
+    that configuration (V002, 0409 item 2: newborn presence is slot occupancy, decided by the
+    caller, never by an all-potential-edge mask).
     """
     dom, reg = ctx._dom, ctx._reg
     anchors = set()
@@ -1260,9 +1569,8 @@
             anchors.add((0, b))
             if reg["edge_mode"]:
                 anchors.add((1, c))
-    for v in raw_vertices:
-        if _vertex_present(dom, edgeset, v):
-            anchors.add((0, v))
+    for v in present_vertices:
+        anchors.add((0, v))
     for d in raw_donors:
         if reg["donor_mode"] == "owner_vertex":
             anchors.add((0, dom["owner_vid"][d // 2]))
@@ -1305,13 +1613,19 @@
 
 
 def _birth_weights(ctx, ch, source_edgeset):
-    """(w(source) + w(target))/2 per cell; identical for a forward channel and its reverse."""
+    """(w(source) + w(target))/2 per cell; identical for a forward channel and its reverse.
+
+    The newborn labels a_j, b_j are present exactly on the side where slot j is active: the target
+    of a forward Birth, the source of a reverse (V002 replacement of V001's newborn edge masks;
+    in every admitted configuration a newborn has an incident edge iff its slot is active).
+    """
     if ch["c"] is None:
         j = ch["j"]
-        raw_v = (ctx._dom["a_vid"][j], ctx._dom["b_vid"][j])
+        newborn = (ctx._dom["a_vid"][j], ctx._dom["b_vid"][j])
         raw_d = (2 * j, 2 * j + 1)
-        ws = dict(_weights(ctx, source_edgeset, ch["raw_edges"], raw_v, raw_d))
-        wt = dict(_weights(ctx, ch["target_edgeset"], ch["raw_edges"], raw_v, raw_d))
+        at_target = ch["newborn_at_target"]
+        ws = dict(_weights(ctx, source_edgeset, ch["raw_edges"], () if at_target else newborn, raw_d))
+        wt = dict(_weights(ctx, ch["target_edgeset"], ch["raw_edges"], newborn if at_target else (), raw_d))
         ch["c"] = tuple((a, 0.5 * (ws.get(a, 0.0) + wt.get(a, 0.0))) for a in sorted(set(ws) | set(wt)))
     return ch["c"]
 
@@ -1377,25 +1691,25 @@
     return tuple(out)
 
 
-def _diagonal_records(ctx, info, key):
+def _diagonal_records(ctx, info, key, scope):
     n_alpha = len(ctx.energy_cells)
     out = []
-    for name, ref, feat in _diagonal_items(ctx, info, key):
+    for name, ref, feat in _diagonal_items(ctx, info, key, scope):
         qs, cs = _support_labels(ctx, info, ref, "diag")
         out.append(_Channel(_owner_id(ctx, name, ref), "diag", None, complex(ctx._model[name] * feat),
                             qs, cs, _dense(n_alpha, _native_weights(ctx, info, ref))))
     return out
 
 
-def _transition_records(ctx, info, key):
+def _transition_records(ctx, info, key, scope):
     n_alpha = len(ctx.energy_cells)
     out = []
-    for kind, ref, target in _transitions(ctx, info, key):
+    for kind, ref, target in _transitions(ctx, info, key, scope):
         w = _birth_weights(ctx, ref[1], info["edgeset"]) if ref[0] == "birth" \
             else _native_weights(ctx, info, ref)
         qs, cs = _support_labels(ctx, info, ref, kind)
         out.append(_Channel(_owner_id(ctx, _FAMILY[kind], ref), kind, target,
-                            _amplitude(ctx._model, kind, ref), qs, cs, _dense(n_alpha, w)))
+                            _amplitude(ctx, kind, ref), qs, cs, _dense(n_alpha, w)))
     return out
 
 
@@ -1433,8 +1747,10 @@
             if alpha not in cache:
                 vids = ctx._reg["cell_vids"][alpha]
                 m = present[:, vids].sum(axis=1).astype(np.float64)
-                t = np.einsum("nva,ai->nvi", z[:, vids, :].astype(np.float64),
-                              ctx._reg["port_vectors"], optimize=False)
+                # V002: each vertex's REGISTERED frame (B = -A under REG0408) with the fixed
+                # whitening W folded in: t'_v = sum_a Z_va W f_v[a] = W t_v (L8).
+                t = np.einsum("nva,vai->nvi", z[:, vids, :].astype(np.float64),
+                              ctx._reg["frames_w"][vids], optimize=False)
                 cache[alpha] = (m, t)
             m, t = cache[alpha]
             has = m > 0.0
@@ -1479,7 +1795,7 @@
     ctx = _context(context)
     key, info = _admit_state(ctx, state)
     _require_coverage(ctx, info, ("edge_cells",))
-    return _diagonal_records(ctx, info, key)
+    return _diagonal_records(ctx, info, key, _full_scope(ctx, info))
 
 
 def primitive_channels(*, context, state):
@@ -1497,12 +1813,58 @@
     ctx = _context(context)
     key, info = _admit_state(ctx, state)
     _require_coverage(ctx, info, ("h", "t", "theta", "edge_cells"))
-    return _diagonal_records(ctx, info, key) + _transition_records(ctx, info, key)
+    scope = _full_scope(ctx, info)
+    return _diagonal_records(ctx, info, key, scope) + _transition_records(ctx, info, key, scope)
+
+
+def _admit_palette(ctx, palette_owners):
+    dom = ctx._dom
+    if not isinstance(palette_owners, (list, tuple, set, frozenset)) or len(palette_owners) == 0:
+        raise ValueError("palette_owners: a nonempty list, tuple or set of original owner labels is required")
+    out = set()
+    bad = []
+    for o in palette_owners:
+        j = dom["owner_index"].get(o) if _is_label(o) else None
+        if j is None or j in out:
+            bad.append(o)
+            continue
+        out.add(j)
+    if bad:
+        raise ValueError(f"palette_owners: {bad!r} are not (non-repeated) original owner labels")
+    return tuple(sorted(out))
+
+
+def palette_channels(*, context, state, palette_owners):
+    """Primitive channels of an explicit state restricted to a declared owner palette (0408 item 3).
+
+    palette_owners: nonempty list/tuple/set of ORIGINAL owner labels (the union of the selected
+    permanent owner groups). Returns exactly the primitive_channels records whose permanent owner is
+    in the palette, by the intrinsic label rule of the blocked-palette move (L13): Birth/reverse of
+    owner j iff j is in the palette; site, Bind, admission and degree owners at v iff v's permanent
+    group (v for an original, owner j for a_j, b_j) is; flip, hop and Delta owners iff either
+    endpoint's group is; donor owners iff their owner is; C_identity never. Owners outside the
+    palette are not enumerated (Birth witness search runs only from palette roots); every Birth
+    channel and every reverse pairing of a palette owner keeps its full current eligibility and
+    complete queried/changed supports. Diagonal records are the palette-OWNED ones only; values of
+    diagonal owners and reads outside the palette that a palette event changes must come from
+    diagonal_terms/read_rows or the supports. Raises ValueError on invalid input or missing
+    coverage of a palette edge. Global per-event costs that remain are listed in LIMITATIONS L11.
+    """
+    ctx = _context(context)
+    owners = _admit_palette(ctx, palette_owners)
+    key, info = _admit_state(ctx, state)
+    scope = _palette_scope(ctx, info, owners)
+    _raise_coverage(ctx, scope["codes"], ("h", "t", "theta", "edge_cells"))
+    return _diagonal_records(ctx, info, key, scope) + _transition_records(ctx, info, key, scope)
 
 
 def read_rows(*, context, state):
     """Presence, single-port Z, pair and coarse reads of one state, typed and labelled.
 
+    Every row is recomputed from the CURRENT configuration: ports reassigned by port_order on the
+    current neighbours, current populations m_alpha, registered per-vertex frames and the fixed
+    whitening (coarse R' = W R, S' = W S W^T). Call it on the outgoing state after every transition
+    (including Birth and reverse); no bits are copied from a predecessor.
     Returns {'labels': context.read_labels, 'values': float64 [n_read], 'presence': float64 [n_read]}.
     """
     ctx = _context(context)
@@ -1557,13 +1919,26 @@
         "contract_cost_formula": "O(D(1+6Vmax+132K)), Vmax=3V0 (contract section 11)",
         "caps": dict(caps),
         "cost_statement": "exponential full domain; matrix-free sparse action; no compression",
+        "canonical_key_edge_code_space": dom["NA"] * dom["NB"],
+        "state_level_per_event_global_costs": (
+            "basis-free functions (primitive_channels, palette_channels, diagonal_terms, read_rows) "
+            "keep: bit-set key ints over NA*NB edge codes, O(NA*NB) bit operations per key "
+            "construction, XOR and bit test whatever the palette size; O(V+E) structure per distinct "
+            "supporting graph (neighbours, q4 validation, port_order lookups; full-list coverage); "
+            "full read recomputation per state (globally normalized coarse reads); palette_channels "
+            "evaluates only palette owners (per-owner C_loc and reverse pairings). See LIMITATIONS L11, L13"),
+        "frame_mode": ctx._reg["frame_mode"],
+        "frames_A_equal_register_table": ctx._reg["frames_A_equal_register_table"],
+        "frames_B_equal_negated_register_table": ctx._reg["frames_B_equal_negated_register_table"],
+        "whitening": tuple(tuple(float(x) for x in row) for row in ctx._reg["whitening"]),
+        "edge_profile_kinds": {name: ctx._model[name][0] for name in _EDGE_PROFILES},
     }
 
 
 def _new_run(caps):
     return {
         "caps": caps, "prov": {}, "keys": [], "graphs": set(),
-        "missing": {"h": set(), "t": set(), "theta": set(), "edge_cells": set()}, "missing_any": False,
+        "missing": {"h": {}, "t": {}, "theta": {}, "edge_cells": {}}, "missing_any": False,
         "max_row": 0, "max_trans": 0,
         "H_diag": array("d"), "H_abs": array("d"), "E_diag": array("d"),
         "h_tgt": array("q"), "h_src": array("q"), "h_re": array("d"), "h_im": array("d"),
@@ -1587,15 +1962,13 @@
             raise _Stop(f"max_graphs cap {caps['max_graphs']} reached before admitting a further supporting "
                         "graph (no graph block is dropped; no operator is returned)")
         run["graphs"].add(edgeset)
-        m, reg = ctx._model, ctx._reg
         for c in _bits(edgeset):
-            for name in ("h", "t", "theta"):
-                if c not in m[name]:
-                    run["missing"][name].add(c)
-                    run["missing_any"] = True
-            if reg["edge_mode"] and c not in reg["edge_cell"]:
-                run["missing"]["edge_cells"].add(c)
-                run["missing_any"] = True
+            for name in _EDGE_PROFILES + ("edge_cells",):
+                if c not in run["missing"][name]:
+                    msg = _edge_problem(ctx, name, c)
+                    if msg is not None:
+                        run["missing"][name][c] = msg
+                        run["missing_any"] = True
     pid = len(run["keys"])
     run["keys"].append(key)
     run["prov"][key] = pid
@@ -1605,8 +1978,9 @@
 def _process_row(ctx, run, pid):
     key = run["keys"][pid]
     info = _info_for(ctx, key[1])
-    diag = _diagonal_items(ctx, info, key)
-    trans = _transitions(ctx, info, key)
+    scope = _full_scope(ctx, info)
+    diag = _diagonal_items(ctx, info, key, scope)
+    trans = _transitions(ctx, info, key, scope)
     n = len(diag) + len(trans)
     cap = run["caps"]["max_events_per_row"]
     if n > cap:
@@ -1632,7 +2006,7 @@
     run["H_abs"].append(habs)
     run["E_diag"].extend(erow)
     for (kind, ref, _target), tpid in zip(trans, tpids):
-        amp = _amplitude(model, kind, ref)
+        amp = _amplitude(ctx, kind, ref)
         run["h_tgt"].append(tpid)
         run["h_src"].append(pid)
         run["h_re"].append(amp.real)
@@ -1776,7 +2150,6 @@
             "arrays_exact": int(sum(x.nbytes for x in arrays)),
             "basis_keys_estimate": int(n * (2 * per_key + 200)),
             "note": "keys estimate = tuple and int objects of the first key plus two dict slots per state"},
-        "port_vectors_equal_register_spec": ctx._reg["port_vectors_equal_register_spec"],
     })
     parts = {"D": n, "dtype": dt, "real_dtype": rdt, "ctx": ctx, "keys": keys_sorted,
              "index": {k: i for i, k in enumerate(keys_sorted)}, "H_diag": h_diag_s, "H_csr": h_csr,
@@ -1836,12 +2209,14 @@
         return result
 
     result["stage_reached"] = "coverage"
-    for name in ("h", "t", "theta", "edge_cells"):
-        miss = sorted(run["missing"][name])
+    for name in _EDGE_PROFILES + ("edge_cells",):
+        miss = run["missing"][name]
         if miss:
             where = "registration['edge_cells']" if name == "edge_cells" else f"model['{name}']"
-            failures.append(f"{where}: no value for stable edges {[_edge_labels(ctx._dom, c) for c in miss]!r} "
-                            "that occur in the enumerated component (no default; zero phase is never inferred)")
+            failures.append(f"{where}: no admitted value for stable edges "
+                            f"{[_edge_labels(ctx._dom, c) for c in sorted(miss)]!r} that occur in the "
+                            "enumerated component (no default; zero phase is never inferred): "
+                            + "; ".join(miss[c] for c in sorted(miss)))
     if failures:
         return result
 
@@ -1965,8 +2340,10 @@
         i = self._checked_index(index)
         key = self._p["keys"][i]
         info = _info_for(self.context, key[1])
+        scope = _full_scope(self.context, info)
         out = []
-        for r in _diagonal_records(self.context, info, key) + _transition_records(self.context, info, key):
+        for r in _diagonal_records(self.context, info, key, scope) + \
+                _transition_records(self.context, info, key, scope):
             t = i if r.target_state is None else self._p["index"][r.target_state]
             out.append(_IndexedEvent(r.owner_id, r.kind, i, t, r.amplitude, r.queried_support,
                                      r.changed_support, r.energy_weights))
```
