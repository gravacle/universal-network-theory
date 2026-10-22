# REVIEW 0405 — integrated model fidelity, modules A and B (V001)

**Role:** distinct integrated-model-fidelity reviewer, not author. I wrote neither module.
**Method:** static text review only. Neither module, nor any legacy, UNT or Codex module, was imported or executed. The only code run was `python3 -I -B` with `ast.parse`/`compile` on the two module TEXTS, from my own scratch directory. No `__pycache__` was written into the artifact directory. No numerical control, propagation, data extraction, network access or package install was performed. No file whose name contains Newton, FIELD_, ROTATION, FIT, TRIAL, MOM1, rotmod or MassModels was opened, and no target velocity, validation outcome or historical fit/response array was read.

## Verdict: FAIL

The pair is not ready for root's integrated launch, for two reasons:

1. The MANDATORY ADDENDUM item 1 time-derivative reads (with their K' terms) are missing from both modules.
2. Module A cannot represent the root-adopted 0408 production registration. Its frames and edge profiles do not fit, and the frame gap gives wrong first moments.

Everything else checked is faithful to the contract and its sources. The one exception is the non-blocking notes below. The operator core (domain, keys, primitives, C_loc Birth/reverse, V002 weights, reads) and the propagator core (equations, signs, error bounds, Legendre blocks) need no correction.

## Hashes (sha256 from bytes)

| item | sha256 |
|---|---|
| Module A `owned_parent_operator_v001.py` (103243 B) | `27ad1762dbdc559eb92edcb6f7fe83790b73a4e23d71b12500b8586c811de3b6` (matches author A report) |
| Module B `owned_retained_source_columns_v001.py` (84801 B) | `a9773a6dcdc5535d38808308b0d7ebf5ff89dc680b70144e5c3e57a9e2670a27` (matches the 0115 note) |
| CONTRACT | `fcad9039574f1666af005bb76a231f14b90f0c8dd82acebd2b16ab77941cd642` ✓ |
| Task 0405 | `7baab49ebbd01de684df56a074b823552c1eca9e787384ad0a0084144295c003` ✓ |
| 0406 | `a465d9e3f703f2a2f19d383446c6a2bf6486e5f6be9fdf5996fc96dfb4693d50` ✓ |
| ADDENDUM | `7cb15b4a5ac2ea33dfd43801c011142bc2b2388c3be0087152c049e78deccd39` ✓ |
| HP time-derivative addendum (cited by ADDENDUM) | `2fc9dc2c0197d6b3d0e2ff5893ba32b7ef89ba5424680bc06bd5210d5207226a` ✓ |
| 0408 | `c0f0eaa940ce95c495fa2d7c21d59cae2a49e8028cc084df878d203e3c42e341` ✓ |
| 0408 registration / companion | `f65dbc234ae082df342235b1a6c13a0282cf94665ba3e1c3989d12b12e7d7174` ✓ / `9eb4861cce5e4c435a259811dbca289e7e95a2b4ac34732c9f6c3ee56c34d7d7` ✓ |
| 0407 (no pin supplied; computed) | `f3f60cebd42db1120b2193968404644a1890cf2f5e48563c2d94544a4bd33fc3` |
| REGISTER spec | `032a564bd018b7302bd60de633f8e3c9d2f91f8c079f16b62548bce0e4e53d94` ✓ |
| V002 / adoption | `494d0124…cb78a` ✓ / `b5e7c2e3…22465` ✓ |
| LEDGER / CLOC / GEN / cut-class companion / DOMAIN | `732bc83e…e0a0` ✓ / `388621c0…af53` ✓ / `8ab3d7a7…6930` ✓ / `eebf34cc…6316` ✓ / `71568045…9243` ✓ |
| Partial Legendre / Kubo / pair-kernel | `d81d48e8…1663` ✓ / `a7d048c1…dfc7` ✓ / `facdfe45…dec9b4` ✓ |
| 0399 map / FIDELITY_V002 / COMPLETENESS / erratum | `5edcf7e5…e584` ✓ / `0c661284…8134` ✓ / `ca91cbb3…dc3a` ✓ / `b1552d8a…a497` ✓ |
| 0400 definitions / check | `f2957b9b…cf69` ✓ / `8ca3f00a…e4ae8` ✓ |
| PRIMARY legacy backend | `0d28150ff9edeab3b75543acb6dbd7da472770e1ccec98dfaf948348650c07a3` ✓ |

The table abbreviates long hashes only where the full pinned value is given in the task. Every one was computed in full and matched.

## Blocking issues

**B1 (both; module B primary). ADDENDUM item 1 time derivatives are absent.**
- **Where:** B l.549–609 (`_contract_node` computes `HL` but uses it only for <H>), outputs at B l.1299–1315; A LIMITATIONS L9, l.214–216, assigns the derivatives to module B.
- **Issue:** The mandatory addendum and the HP addendum (`2fc9dc2c…`) require full-H first and second native-time derivatives of the means, or a controlled equivalent. These are <L_O> = <(i/hbar)[K,O]> and <A_O> = <(i/hbar)[K',O] − [K,[K,O]]/hbar²>, for R, S and every read row. The explicit generator K' terms (source and lapse time dependence) must be retained.
- Module B returns only the node means and linear responses. Module A defers the derivatives to B. Neither module supplies them, and nothing in the returned data allows a controlled reconstruction. Means at grid nodes are not a controlled derivative.
- **Required fix:** In B (or as an A operator member that B consumes), return at each node the commutator means. Use the SAME full-H matvec on the SAME state: H L and H(H L), together with the read diagonals and the E_alpha actions. Include:
  - the explicit K' term from the actual time-dependent source/lapse;
  - the corresponding tangent (response) derivatives;
  - error bounds that extend the existing Cauchy–Schwarz node bounds.
- If registration, frame or read is explicitly time-dependent, keep its partial derivatives. They are zero for the fixed current-state reads of V001, and that should be stated.

**B2 (module A). The 0408 B-part frames cannot be represented, so first moments are wrong.**
- **Where:** A l.694–706 (one global `registration['port_vectors']` 4×3), used at l.1436–1437.
- **Issue:** The adopted 0408 registration (`f65dbc23…`) uses B-part frame vectors equal to the negatives of the A-part vectors with the same index. No port permutation of the tetrahedral set gives −v_a; for example −(1,1,1)/2 is not in the set. So no caller input to V001 can express the registration.
- Under any single table, the per-vertex t_v of every B vertex has the wrong sign, which makes R_alpha (mu) wrong and hence C = M − mu mu^T wrong. S is sign-invariant.
- The same frames must enter the dual read sources (whitening companion), so the source columns built from these rows are wrong as well.
- **Required fix:** As 0408 item 1 specifies, accept an explicit per-vertex (or per-part) frame table or a callable. Validate dimensions and finiteness. Use the same frames for reads and sources, preserved as V002. Root has already identified this gap.

**B3 (module A). Edge profiles require enumerating every possible endpoint pair.**
- **Where:** A l.501–520 (`_edge_table` copies every supplied mapping entry) and l.582–583 (`hop_BA` materializes a second table). Coverage is checked only for edges met later (l.981, l.1591–1598).
- **Issue:** Edges can appear anywhere after Birth and its reverses. To avoid a mid-run coverage failure, a caller must therefore enumerate all possible A–B pairs for h, t and theta: 9L^6 = 2,359,296 pairs at L=8. 0408 item 2 is binding and forbids exactly this for a uniform physical profile. The results are not numerically wrong, but V001 cannot serve the production binding.
- **Required fix:** As 0408 item 2 specifies, accept explicitly declared uniform h/t/theta values and/or current-edge profile accessors. Keep the (A,B) endpoint keys. Validate every accessed value. Arbitrary missing map entries must remain explicit failures. Root has already routed this to V002.

## Checked and confirmed (contract sections 2–8 and 11, 0406, ADDENDUM 2–3, non-negotiables)

**Domain and identity (section 2, ADDENDUM 2, 0406 item 2)**
- graph0 is admitted as a simple bipartite q4 graph with distinct original labels, and K=V0 slots with distinct a_j (A) and b_j (B) labels (A l.398–498).
- The canonical key (slots, edgeset, inc, p, q, s, donors) is made only of bitmasks over fixed label ids. It carries no history field, so equal labelled configurations merge.
- The edge code is a function of the ordered (A label, B label) pair (l.352–371). h, t and theta are keyed by that pair, so merged states get identical phases.
- A newborn's cell is its owner's cell, with no genealogy (l.631–635), as REGISTER requires.

**Inventory**
- M_v=1 on every present site, with an R/S cell and free p and q: 8 local states.
- The declared sector is enforced explicitly: N_c = S_graph (l.1088) and donors RR iff the slot is absent (l.1083–1087). Q = M = V0+2K follows. Local Q_v is unrestricted.
- Admission changes N_c. No fixed-N_c basis is used. An I-cell ambient domain is not implemented, and A L4 states this; that is allowed by section 2 as stated.

**Diagonal (section 3)**
- The diagonal terms are (l.1139–1171):
  - Delta n_e per occupied edge;
  - Ud (d−dstar)² per present vertex;
  - epsilon_c p, epsilon_r q, −lambda_R d q, +lambda_J d p;
  - E_R or E_S per present site (E_I is identically 0 on this inventory);
  - e_R/e_I per donor;
  - C_identity once per state.
- This matches PRIMARY `CanonicalJoin.channels`, including the full lambda_J Σ d p and not the SECONDARY restored_bs11 term. No energy zero is set per graph or slot.

**Transitions (section 3, 0406 item 3, ADDENDUM 3)**
- Flip: −h_e on every present edge, with h real; complex values are rejected at l.512.
- Hop: only when n_e=1 and the endpoint p values differ. It swaps p and leaves q and the cells fixed.
- Hop phase: B→A is −t e^{+iθ} and A→B is its conjugate (l.582, l.1236–1238). This equals PRIMARY: the `-phases[e]` entry for the v→u move, with periodic_q4 edges written (u∈A, v∈B).
- Bind: +g_v whenever p_v=1, including the R,p=1 states, with g real (rejected otherwise at l.533).
- Admission: R,p=0 → S,p=1 with amplitude kappa; the reverse has conj(kappa); q is unchanged.
- Birth: amplitude epsilon_j; the reverse has conj(epsilon_j). Each reverse is the exact conjugate of its forward.
- Phase-rule ambiguities are recorded in A L5 and L6: no child-edge phase rule exists in the sources, no many-carrier T_e(θ≠0) is written, and the ADDITIONAL reference has the opposite orientation.

**C_loc and Birth (section 4, LEDGER l.13, CLOC l.7, GEN l.27–36, companion)**
- `_c_loc` (l.834–854) is enumerated in the CURRENT graph from every present root in both parts. It fixes one cut edge at the root and matches each other neighbour x to a neighbour of x other than the root, with distinct endpoints. Unordered cuts are deduplicated across witnesses, and a witness set is kept. The cut class is C_loc, not all-matchings.
- The forward channel exists iff o_j is in the witness set, slot j is absent, donors are RR and the census is 2. Each (G,C,j) appears once (m_c=1).
- Surgery deletes the four (u,v) cut edges, adds (u,b_j) and (a_j,v) carrying the copied bit, and keeps every other factor. The newborns are R with p=q=0 because their bits were zero while absent. Donors go RR→II. This is not the blank-I BirthMap.encode.

**Reverse**
- For each active slot, all 4! pairings are tried (l.893–948). A pairing contributes zero in any of these cases:
  - a restored edge duplicates a surviving edge;
  - a_j is adjacent to b_j (correct: that is never in the forward image);
  - o_j is not a cut endpoint;
  - the predecessor neighbours of o_j are not exactly the opposite endpoints. This is checked in the PREDECESSOR, never as a fresh target-side test.
- At state level (l.1211–1228), the reverse requires donors II, newborns R with p=q=0, equal paired child bits and restored census 2.
- I verified forward/reverse consistency by hand. Each forward record from x to y has exactly one reverse pairing from y to x that passes, and each passing reverse corresponds to a valid forward. Different pairings give distinct predecessors and separate records.
- Failed images produce no record. Native owners act on every state, including reverse-failure states.

**Supports and V002 weights (section 5, V002 support_weights/birth_support)**
- `_weights` (l.1249–1283) counts each distinct present anchor once with equal weight, at each configuration. Edges count through their endpoints, plus the edge itself when `edge_cells` is a map. Newborns count only where present. Donors count through their declared anchor.
- For Birth, `_birth_weights` (l.1307–1316) gives (w(source)+w(target))/2 over the identical raw set for forward and reverse. I checked that the raw sets match: the restored cut equals the forward cut, the children equal the star edges, and root_other equals the three surviving root edges.
- Native transitions preserve the graph, so their two endpoint weights are equal.
- E_alpha is assembled per primitive before aggregation. Build integrity checks confirm Hermitian H and E_alpha and Σ_alpha E_alpha = H (l.1736–1746). C_identity uses an explicit `identity_allocation`.
- With the root-selected `endpoint_anchors_only` and `owner_vertex` options (0408), Birth support is the 8 cut endpoints, plus a_j and b_j on the side where they exist. Support is not reduced to the owner cell.

**Reads (section 5, 0406 item 1, ADDENDUM 1 first part, REGISTER complete_reads)**
- Every vertex label has a presence row, 4 presence-masked Z rows and 6 pair Z_aZ_b rows. Absent rows have value 0 and presence 0, with no conditional normalization.
- Ports come from the caller's current-neighbour ordering, recomputed per current graph with no copied labels.
- Coarse m_alpha counts present vertices, with newborns in the owner cell and donors not counted. R_alpha,i and S_alpha,ij carry a per-configuration 1/m_alpha inside the diagonal operator (l.1412–1449), matching REGISTER and the 0408 present_count.
- Labels are typed by element 0: vertex_presence, first_moment_Z, pair_ZZ, coarse_population_m, coarse_first_R or coarse_second_S, together with the vertex, port and cell.
- The bound tr C ≤ 4 is documented, never clipped.

**Basis, caps and cost (sections 2 and 11)**
- The structural BFS closure (l.1575–1646) is independent of coefficient values.
- max_dimension, max_graphs and max_events_per_row fail before being exceeded. Coverage failures list the edge labels. Nothing is truncated.
- The cost is stated honestly:
  - the G0 block alone has 2^(3V0)·C(2V0,V0) states, about 2.16e11 for V0=8 (I recomputed this);
  - the section 11 formula is O(D(1+6Vmax+132K)).

**Reference family (section 1)**
- `reference_preparation` uses G0, slots absent, donors RR, and chi on each original site. Chi is the unique ground state of the declared four-state H(2), with diagonal entries consistent with the C7 diagonal at d=2, or it is supplied explicitly.
- The ice words cover the complete degree-two subspace.
- The family is labelled a DECLARED reference and fails when degenerate or not contained.

**State-level API (0407)**
- validate_owned_model, canonical_state_key, primitive_channels, diagonal_terms and read_rows are all present. They share their internals with the indexed operator.

**Module B equations (section 6)**
- Propagation: i hbar l' = H l and i hbar dl_b' = H dl_b + V_b l, with V_b = f_b(Σ cE E_alpha − Σ cO O_A). So energy columns have +f E and every read column (first-moment and pair) has −f O. dl_b(t0)=0.
- Response: delta<A> = 2 Re Σ_k s_k <l_k|A|dl_bk>, contracted on the SAME state for all E_alpha, read and presence outputs.
- Mixed states: purification is supported; a dense Hermitian rho gets a full-rank signed factor, never made low-rank. Family mode gives compressed V†(...)V matrices for all outputs.
- No P/Q reduction is used.

**Taylor recursion and residuals**
- I re-derived the recursion: u_{n+1} = c/(n+1) H u_n and w_{n+1} = c/(n+1)(H w_n + B G_n) with G_n = Σ_p a''_p u_{n−p}.
- I re-derived the exact residuals: η_ψ = −σ^N H u_N and η_b = −σ^N H w_N − Σ_{j=N}^{N+P} σ^j B G̃_j.
- The bounds follow: ρ_ψ = h‖Hu_N‖/((N+1)ħ), and ρ_b as coded at l.493–503.
- `_shift_scale` re-expands the source exactly. The window indexing u_{n−p} is correct.

**Error-bound completeness**
- The bounds cover:
  - the primal and tangent residual integrals;
  - the tangent forcing error carried from the primal, (‖B‖/ħ)·eps_L·∫|f|;
  - source quadrature, which is exactly zero for polynomial profiles;
  - read and energy contractions, by Cauchy–Schwarz;
  - the density factorization residual R1.
- Rounding that is not covered is stated. Count leakage is a diagnostic only.

**Contacts (sections 6–7)**
- In the affine coordinate H_nn = H_nj = H_jj = 0. The read, preparation and registration contacts are explicitly zero for the fixed V001 reads.
- `g00_lapse_coordinate_contact` gives J1 = 1/N and J2 = −1/N³, with W contact −J2<E> (= +<E> at the flat point, i.e. H_{n_g n_g} = −E, uniform −H). It is exposed and never dropped.

**Partial Legendre (section 8)**
- The blocks are Γ_QQ = −Y_OO^−1, Γ_Qn = −Y_OO^−1 Y_OE, Γ_nQ = −Y_EO Y_OO^−1 and Γ_nn = Y_EE − Y_EO Y_OO^−1 Y_OE. They are formed on the caller's quotient, with contacts added to W before the Schur complement. The sign mapping matches the candidate's "W_nn includes Chi_EE − <H_nn>".
- Declared zero modes must be excluded from the quotient, and a singular reduced chi_OO is rejected with no regulator or pseudoinverse.
- No matching coefficient is invented, and the result is not equated with the full metric propagator.

**A/B interface**
- Every member B requires exists in A with the same semantics: dimension, energy_cells, read_labels, apply_H(block), apply_E(alpha=label, block), read_values(), read_presence(), apply_O(read_index, block), norm_bound_H(), norm_bound_E(alpha=label), resources(), basis_key, index_of and primitive_events.
- B's read typing token is element 0 of A's tuple labels.
- A's absent-read zeros satisfy B's check that values are 0 where presence is 0.
- A's absolute-column-sum bounds are valid ‖·‖₂ bounds for Hermitian matrices.
- B does not import A.

**Coding rules (AST on text)**
- Imports: A uses numpy plus stdlib (array, cmath, collections.abc, itertools, math, sys, typing); B uses numpy and math only.
- There is no `@` or dot/matmul/vdot/inner/tensordot/outer, no print/open/exec/eval and no warnings handling.
- At module level there are only imports, definitions, classes and literal constants.
- Every public function and method is keyword-only with no defaults.

## Notes (non-blocking)

1. **dtype coupling.** A rejects any block whose dtype is not exactly the operator dtype (A l.1931–1936). B casts blocks to its own `dtype` (B l.378). A mismatch fails closed through B's `_call`. The caller must pass the same complex dtype to both modules.
2. **Family path needs a dense isometry.** B's `family_isometry` needs a dense V [D, r]. A's `reference_preparation` returns a sparse isometry (rows, cols, values) plus an optional dense `factor`. The caller must assemble V, or use the factor through the purification path. This is not a semantic mismatch.
3. **L12 wording.** A L12 says coefficient values never remove a record. The Ud diagonal record is omitted when (d−dstar)²=0, and dstar is a coefficient (A l.1155–1157). The amplitude is 0 either way, so H, E_alpha and the samplers are unaffected. The wording should be corrected.
4. **Support readings.** A L3 includes the four neighbours in the degree-feedback support (literal contract section 3) and uses only o_j root adjacency plus the cut for the Birth guard. DOMAIN §3 describes forward witness search as inspecting the root's neighbours and their incident edges. For testing o_j ∈ W_G(C) the module's set is sufficient and yields the same anchor set (the 8 cut endpoints). Both are documented ambiguities that belong in the allocation-sensitivity study.
5. **0408 item 3, per-event cost.** primitive_channels works without a basis, as required. However, each new supporting graph (every Birth or reverse) triggers a full C_loc recomputation of order 108·V and a port_order call for every present vertex. A describes this as a "one-off per-graph structure". For the sampler it is a global per-event cost and should be reported as such.
6. **Retained loop/count reads.** These are not implemented (A L9). Contract sections 5 and 8 make them additional same-state outputs when the collective action requests them. No binding specification of them was supplied with this task.
7. **Second-order responses.** B is linear about n=0, j=0 (L4). This is consistent with the section 6 linear Kubo scope. Second-source derivatives of C outside Q=(mu,M) coordinates would need actual second-order mean derivatives, which B does not compute.
8. **Slightly negative eigenvalues.** B admits eigenvalues ≥ −psd_tolerance and keeps them with sign −1, without modifying rho. The tolerance is the caller's declared choice.
9. **Per-slot epsilon.** epsilon_j per slot generalizes GEN's single epsilon (0399 E3). The shared interface asks for per-slot values, and the uniform member is the caller's equal values.
10. **Exponential cost.** The full-basis route is exponential, as both modules state. Per 0407, production uses the state-level API.

No physical parameter, state, profile, registration value or calibration is chosen in this review. No response coefficient or galaxy prediction is claimed.
