# Usage note 0405 V001: owned-parent operator (A) and retained source columns (B)

2026-10-16. Written by the usage-note author, who wrote neither module. The modules were read as text only; nothing was imported or executed.

**Status: UNTESTED.** No author or reviewer has ever executed either module. The two reviews on file (FIDELITY `dfd97e2fa36a6510599245a3629106c1e51df3a2d75aa381d1b163ddecf5fd46`, STATIC_CODE `9cd0ad3b5e9c578b3d9ae82f525185017aa86ba076cd9654face14b2e94f49c6`) judged V001 and both returned FAIL. V002 answers their blocking items according to the fix deltas (A `47a96b7623c093c8efe2b78419b427b38fedac6e921d94b03f89d38b530e6d9e`, B `23052ba6453cbecc962b4ad7039d229d69ec08be303eddb3fab3221b817b33b7`). No review of V002 accompanied this note.

| File (sha256 computed from bytes) | Bytes |
|---|---|
| A `owned_parent_operator_v002.py` `b5fded4d1272322036748d4d1b4e634a804c1da1ad6717e70e32b4f2a364a94e` | 128154 |
| B `owned_retained_source_columns_v002.py` `173f608d9b4effdf61c3ea0bfb147aaf5528a742c3ec2501d41f5397b36bbe81` | 116917 |
| CONTRACT `fcad9039574f1666af005bb76a231f14b90f0c8dd82acebd2b16ab77941cd642` · ADDENDUM `7cb15b4a5ac2ea33dfd43801c011142bc2b2388c3be0087152c049e78deccd39` | |
| Preserved, superseded: A v001 `27ad1762dbdc559eb92edcb6f7fe83790b73a4e23d71b12500b8586c811de3b6` · B v001 `a9773a6dcdc5535d38808308b0d7ebf5ff89dc680b70144e5c3e57a9e2670a27` | |

## 1. Semantic scope
**A** builds a finite Hamiltonian and its reads for an explicit labelled simple bipartite q4 graph G0. It has K = V0 owner slots, newborn labels a_j and b_j, and private donor pairs. It implements the current owned member H as follows:
- **Diagonal:** the contract s.3 terms, including C_identity.
- **Flip:** amplitude −h_e.
- **Hop:** b→a has amplitude −t_e e^{+iθ_e} and a→b has its conjugate. It is a hard-core exchange with no CAR sign.
- **Bind:** amplitude +g_v.
- **Admission:** κ_v forward, κ_v* reverse.
- **Birth:** the loaded Birth ε_j B, with C_loc taken in the current graph. The reverse has amplitude ε_j* and tries all 4! pairings with the full image tests.

The inventory has M_v = 1 (8 local states per site), with the sector N_c = S_g and donors RR exactly when the slot is absent. E_α is formed with the V002 equal-weight, endpoint-averaged support fractions, so it is Hermitian and Σ_α E_α = H. The reads are diagonal:
- per vertex label: presence, 4 values Z = 1−2n, 6 products ZZ;
- per cell: m_α, R' = W R and S' = W S Wᵀ, using the registered frames and a current-state factor 1/m_α.

**B** computes the linear retarded response at the flat point n = 0, j = 0 with a fixed preparation. It returns the response of every E_α and every read row (presence rows included) to the declared source columns. It also returns:
- native means;
- first and second native-time derivatives of the means and the responses (ADDENDUM item 1);
- the g00 coordinate contact;
- partial Legendre blocks on kernels that the caller has discretized.

All outputs are mathematical functions of the caller's inputs.

## 2. API and required inputs
Every public function is keyword-only and has no defaults. Results are fail-closed dicts with `ok`, `stage_reached` and `failures`. A's state-level functions raise ValueError instead.

**A**
- `validate_owned_model(graph0, model, registration)` returns a `context`.
- Basis-free functions: `canonical_state_key`, `state_labels`, `primitive_channels`, `diagonal_terms`, `read_rows` (each takes context and state) and `palette_channels(context, state, palette_owners)`.
- `build_owned_operator(graph0, model, registration, seed_states, caps, dtype)` returns an operator with `dimension`, `dtype`, `energy_cells`, `read_labels`, `basis_key`, `index_of`, `primitive_events`, `apply_H(block)`, `apply_E(alpha, block)`, `apply_O(read_index, block)`, `read_values()`, `read_presence()`, `norm_bound_H()`, `norm_bound_E(alpha)`, `resources()` and `reference_preparation(chi, ice_factor)`.

**Inputs to A**
- **graph0** = {A, B, edges[(A,B)], slots{o_j: (a_j, b_j)}}. Every original vertex must have degree 4.
- **model**:
  - Real scalars Delta, Ud, dstar, epsilon_c, epsilon_r, lambda_R, lambda_J, E_R, E_S, E_I, e_R, e_I, C_identity.
  - h, t, θ: each is either a map (A,B)→real or an `accessor(edge=(A,B))`. Together they must cover every edge that occurs, including all newborn and child edges. The sources do not fix the child-edge phase rule, so the caller must supply those phases; zero phase is never assumed. A complex h is rejected.
  - g (real) and κ (complex) for every vertex label, newborns included.
  - ε (complex) for each owner.
- **registration**:
  - cells; original_cell (newborns and donors inherit the owner's cell);
  - edge_cells: `'endpoint_anchors_only'` or a map;
  - donor_anchor: `'owner_vertex'` or `'separate_at_owner_cell'`;
  - identity_allocation, summing to 1;
  - a deterministic `port_order(*, vertex, neighbours)`;
  - port_vectors: one 4×3 table, {'A', 'B'} tables, a per-vertex map, or a callable;
  - whitening W: a real nonsingular 3×3 matrix (the identity gives raw moments).

  The 0408 binding needs port_vectors = {'A': T, 'B': −T} and the companion W. The root adapter's current `build_inputs` has no `'whitening'` key, so validation fails closed on it (A L14).
- **seed_states:** the basis is the structural reachable component of the seeds.
- **caps** {max_dimension, max_graphs, max_events_per_row}.
- **dtype:** complex.

**B**
- `propagate_source_columns(operator, preparation, source_columns, time_grid, hbar, stepper, caps, dtype, time_derivative_contacts)`:
  - **preparation** is one of:
    - `{'kind':'purification', 'factor': L[D,r], 'trace_tolerance'}`
    - `{'kind':'density', 'rho': ρ[D,D], 'trace_tolerance', 'hermiticity_tolerance', 'psd_tolerance'}`
    - `{'kind':'family_isometry', 'isometry': V[D,r], 'isometry_tolerance'}`

    Nothing is renormalized, and ρ is kept at full rank as a signed factor.
  - **source_columns** = {labels (m unique strings), energy_coefficients real [m, n_E], read_coefficients real [m, n_read], profiles real [m, K_t, P+1]}. The profiles are coefficients of (t−t_k)^p on each interval.
  - **time_grid** is strictly increasing, of length K_t+1; t₀ is the preparation time and observations are taken only at nodes. **hbar** > 0.
  - **stepper** = {'taylor_residual', max_order, max_step_norm_product, residual_tolerance, consistency_tolerance}.
  - **caps** = {max_working_entries, max_column_applications, max_substeps}.
  - **dtype** must be identical to A's dtype; otherwise A rejects the blocks and the run fails closed.
  - **time_derivative_contacts** must be exactly {read_frame: 'fixed_current_state_reads', background_generator: 'flat_point_time_independent_H'}.
- `g00_lapse_coordinate_contact(n_g, energy_means)`.
- `partial_legendre_blocks(chi_EE, chi_EO, chi_OE, chi_OO, contacts, read_quotient, energy_quotient, declared_zero_modes, relative_singular_floor, exclusion_tolerance)`.
- **Glue from A to B:** `reference_preparation` returns a sparse isometry and, optionally, L = V F [D,r]. Either pass L as `'purification'`, or assemble a dense V for `'family_isometry'`. This family is DECLARED, never a default state.

## 3. Outputs, shapes, signs
Notation:
- n_E = number of cells.
- n_read = 33·V0 + 10·n_E. Each of the 3V0 vertex labels has presence, 4 Z and 6 ZZ rows; each cell has m, 3 R and 6 S rows.
- n_out = n_E + n_read: all E_α first, then the read rows.
- n_obs = K_t + 1.

Outputs:
- **means:** E [n_E, n_obs], H [n_obs], O and presence [n_read, n_obs].
- **response:** values [n_out, m, n_obs] and presence [n_read, m, n_obs]. Both means and response also come grouped `by_kind`.
- **time_derivatives:**
  - means first and second [n_out, n_obs];
  - homogeneous parts and contacts G1, G2 [n_out, m, n_obs];
  - assembled response derivatives taken one-sided: left at nodes 1..K_t and right at nodes 0..K_t−1, each [n_out, m, K_t];
  - the profile node values f and f′.
- **error_bounds:** the same leading shapes for every output.
- **Family mode:** every value gains trailing [r, r] complex Hermitian axes holding V†(·)V. The caller contracts these with the family density.

Sign conventions:
- H[n,j] = H + Σ n_α E_α − Σ j_A O_A, with n = N−1. The source is V_b = f_b(Σ cE E_α − Σ cO O_A): energy columns enter with +, read columns with −.
- δ⟨A⟩ = 2 Re Σ_k s_k⟨l_k|A|dl_bk⟩ = ∫ f_b [Σ cO χ_{A,O} − Σ cE χ_{A,E}], with χ_AB = (i/ħ)θ(t−s) Tr ρ₀[A_H(t), B_H(s)]. Hence δO = χ_OO j − χ_OE n and δE = χ_EO j − χ_EE n.
- d⟨A⟩/dt = (i/ħ)⟨[H,A]⟩ and d²⟨A⟩/dt² = −⟨[H,[H,A]]⟩/ħ². The second derivative of the response keeps the K′ term f_b′ G1.
- Γ_QQ = −Y_OO⁻¹, Γ_Qn = −Y_OO⁻¹Y_OE, Γ_nQ = −Y_EO Y_OO⁻¹, Γ_nn = Y_EE − Y_EO Y_OO⁻¹ Y_OE. Contacts are added before the Schur complement. Singular and zero-mode directions are rejected, and no regulator is used.
- The g00 contact is −J2⟨E_α⟩ = +⟨E_α⟩/N³.
- An absent read has value 0 and presence 0; there is no conditional normalization.
- The centered C = M − μμᵀ and the HP volume reads are combinations the caller forms.

## 4. Error bounds: what they mean
Each bound limits |computed − exact| for one output of the stated finite model. The bounds hold in exact arithmetic under these premises:
- H and every E_α are Hermitian, and Σ E_α = H;
- `norm_bound_*` are true upper bounds;
- the reads are diagonal.

These premises are checked only as necessary conditions.

**Covered:**
- Taylor truncation of the primal and of every tangent (a-posteriori residual integrals);
- the tangent forcing error inherited from the primal;
- Cauchy–Schwarz contractions;
- the density factorization residual R1.

Source quadrature is exact. The derivative bounds scale with 2‖H‖/ħ and 4‖H‖²/ħ². `norm_bound_H` is an absolute column sum, so the bounds are worst-case and can be loose.

**Not covered:**
- floating-point rounding anywhere, including A's float64 coefficients;
- eigh error beyond its measured residual;
- violations of the premises that the necessary-condition checks miss.

Norm leakage is reported as a diagnostic, not as a bound. The bounds say nothing about whether G0, the coefficients, the registration, the preparation or the sources are physically right.

## 5. Finite domain and exponential cost
D is the size of the structural reachable component, closed under every channel whatever the coefficient values. Caps fail before they are exceeded, and nothing is truncated.

The domain is exponential. The G0 block alone has 2^(3V0)·C(2V0,V0) states, about 2.2×10¹¹ at V0 = 8 (K₄,₄, the smallest simple q4 bipartite graph).

| Item | Cost |
|---|---|
| Sparse action | O(D(1+6Vmax+132K)), Vmax = 3V0, K = V0; `resources` reports D(1+18V0+132K) |
| A storage | H CSR plus n_E E_α CSR |
| Working vectors (contract) | O(D r (m+1)) |
| Working vectors (B's own estimate, including derivatives) | O(D r (20m+P+30)) entries, plus read_values and read_presence of [n_read, D] each |
| Dense ρ | r = D columns, about 6D² entries, O(D³) eigh; never replaced by a low-rank state |
| Substeps | about Δt·norm_bound_H / (ħ·max_step_norm_product) |

For any physical G0 a full build reaches its caps, and B needs a built operator. The basis-free A functions avoid D, but they keep global per-event costs: keys over NA·NB edge codes (2,359,296 at L = 8), O(V+E) structure for each new graph, and a full read recomputation per state (A L11). No compression, Krylov method or P/Q reduction is provided.

## 6. Not implemented
- P/Q reduction and the memory kernel.
- Matching coefficients and the matched EH/vacuum split. The Legendre blocks invent none and are not the full metric propagator.
- A physical state, calibration, and units. One consistent system is declared by the caller; there is no conversion.
- Retained loop/count reads.
- Second-order (n,j) responses.
- A nonzero or time-dependent background lapse, a source-dependent preparation, and time-dependent reads or frames. These fail closed.
- The ambient I-cell domain and separately registered newborn cells.
- Many-carrier T_e(θ≠0). It is not written in the sources; an edge-local hard-core exchange is implemented instead.

## 7. Assumptions and what does not follow
- **V002 proper time.** The V002 support-mean proper-time coupling (`494d0124c1cd49841760dfc49673d696eab3486d75b31fda708679fa5cacb78a`, adoption `b5e7c2e3f12a6a4e3358a3c63a797783645d69240e757778ca42a91729a22465`) is a provisionally adopted, explicitly counted assumption, not a derived native law. It fixes E_α, and therefore every lapse column, χ_EE, χ_EO, χ_OE and every Γ block that involves n.
- **Caller-declared choices.** edge_cells, donor_anchor, identity_allocation, the frames, W and the child-edge phases are caller data (A L1–L3, L5, L8). Results depend on them.
- **No physical results.** These modules do not by themselves yield a physical response coefficient, a calibration, G_eff, a halo or a galaxy prediction. They return numbers for a finite model on whatever inputs are supplied. Physical meaning requires the bound inputs (coefficients, registration, state, sources, matching) and a separate review.
- **Non-blocking wording issues carried into V002.**
  - A L12 says coefficient values never remove a record, yet the Ud record is dropped when (d−dstar)² = 0. The amplitude is zero, so nothing changes.
  - identity_allocation is admitted at 1e−12, but the build integrity check uses a tolerance of about 1e−13. An admitted allocation can therefore fail closed.
