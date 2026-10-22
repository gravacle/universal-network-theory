# REVIEW 0405: STATIC CODE REVIEW V001

Role: distinct static-code reviewer, not author (I wrote neither module).
Method: careful reading and hand-tracing of the two module TEXTS only. Neither module, nor any legacy, UNT or Codex module, was imported or executed. The only code run was `python3 -I -B` with `ast.parse` and an in-memory `compile` on the file text, from a scratch directory outside the artifact folder. Nothing was written into the artifact folder except this file, which was created exclusively. No numerical controls, propagation, data extraction, network use or installs.

## Inputs (sha256 recomputed from bytes)

| file | sha256 |
|---|---|
| owned_parent_operator_v001.py (module A, 103243 B, 2151 lines) | 27ad1762dbdc559eb92edcb6f7fe83790b73a4e23d71b12500b8586c811de3b6 |
| owned_retained_source_columns_v001.py (module B, 84801 B, 1604 lines) | a9773a6dcdc5535d38808308b0d7ebf5ff89dc680b70144e5c3e57a9e2670a27 |
| contract OWNED_RETAINED_RESPONSE_FULL_H_SOURCE_COLUMN_IMPLEMENTATION_CONTRACT_V001.txt | fcad9039574f1666af005bb76a231f14b90f0c8dd82acebd2b16ab77941cd642 |
| ADDENDUM OWNED_RETAINED_PROVIDER_IMPLEMENTATION_MANDATORY_READ_AND_LABEL_ADDENDUM_V001.txt | 7cb15b4a5ac2ea33dfd43801c011142bc2b2388c3be0087152c049e78deccd39 |
| register spec COARSE_REGISTER_STATE_BOUNDARY_WORKING_SPECIFICATION_V001.json | 032a564bd018b7302bd60de633f8e3c9d2f91f8c079f16b62548bce0e4e53d94 |
| task 0405 / correction 0406 | 7baab49e...c003 / a465d9e3...3d50 (both match the module headers) |

Both module hashes match the author/orchestrator statements.

## Verdict: FAIL (one blocking issue, module B)

Module A has no blocking defect. Module B's propagation, contraction, bound and Legendre arithmetic is correct as traced. However, B omits a mandatory deliverable of ADDENDUM item 1, and module A explicitly delegates that deliverable to B.

## Blocking issues

| # | module | line | issue | required fix |
|---|---|---|---|---|
| 1 | B (A delegates it at A l.214-216, L9) | B l.748-1355 (`propagate_source_columns`; outputs l.1299-1337); LIMITATIONS l.130-191 | The mandatory ADDENDUM V001 item 1 requires "full-H first/second native-time derivatives or a controlled equivalent" of the first moments mu and raw second moments M and of their responses, with K' and changing-read/frame terms retained when applicable. B returns only node values of means and responses. There are no time-derivative outputs, no error bounds for them and no statement on K'. B's LIMITATIONS never mention the ADDENDUM. Module A's L9 assigns exactly these derivatives to B, so the integrated provider does not supply them. Finite differences of node values taken by a caller would not be a controlled equivalent. | Add same-state derivative outputs for every E_alpha and read row, at every node. For a time-independent H with diagonal reads: d<A>/dt = (i/hbar)<[H,A]> = (2/hbar) Im sum_k s_k <H l_k \| A l_k>; d2<A>/dt2 = -(1/hbar^2)<[H,[H,A]]>, built from apply_H. For the tangents, differentiate 2 Re<l\|A\|dl_b> using i hbar dl_b' = H dl_b + V_b l. This adds the source term (2/hbar) Im<l\|A V_b(t)\|l> at time t (and its f_b' term at second order). Propagate per-entry bounds through the same Cauchy-Schwarz scheme, with norm_bound_H in place of A's norm. State explicitly that K' and changing-frame terms are zero for this fixed-registration linear rule, or implement them where a source-dependent read applies. Record the item in LIMITATIONS. |

## Hand-trace results (all requested items)

### Module A
- **Canonical key and index_of.** The key is (slots, edgeset, inc, p, q, s, donors), with bit sets over fixed ids. The vid layout is A-originals, A-newborns, B-originals, B-newborns (l.443-448). The edge code a*NB + (b-NA) has inverse `_edge_ends` (l.348-353). No history field exists. `_admit_key` (l.1069-1093) checks the bit ranges, the slot/newborn match, inc within the edgeset, p/q/s on present vertices, the donor sector (RR iff absent) and N_c = S_g. `basis_key` -> labelled pairs -> `_parse_state_mapping` reproduces the identical int tuple, so `index_of` (l.1951) round-trips. The basis is sorted by the key tuple, and `perm` remaps every event index (l.1717-1728). Consistent.
- **Forward primitive and exact adjoint.** Pairs are flip c with flip c (-h_e, real; complex values rejected at l.512), hop B_to_A (-t e^{+i theta}) with A_to_B (conjugate) on the same edge (l.582, l.1236-1238), bind with bind (+g real, l.533), admit kappa with admit_rev conj(kappa) (l.1241-1244), and birth eps_j with birth_rev conj(eps_j). Each (x,y) pair has exactly one primitive, and its reverse is a one-to-one partner. Native weights are identical at both ends because the graph is unchanged. Birth weights are (w(G)+w(T))/2, computed from the same raw anchor set (cut, root_other, children, newborns, donors) on both channel sides. Forward root_other equals reverse root_other (the owner's three non-cut edges), and the float addition commutes. So H and every E_alpha are Hermitian by construction, and sum_alpha w = 1 gives sum_alpha E_alpha = H. The build re-checks both (l.1737-1746).
- **Birth forward then reverse (symbolic, G0 = K_{4,4}, cut = perfect matching {(a_i,b_i)}, owner a1, census 2).** The target removes the matching and adds (a_i,B_j),(A_j,b_i) with copied bits. Newborns have no p/q/s bits and donors go to II. Reverse at T: u_side = {a_i} and v_side = {b_i}. Any sigma other than the identity restores an existing edge (a_i,b_k), k != i, and is rejected at l.917. For the identity, the witness test (l.919-926) holds. Paired bits are equal, census is 2, new_inc restores the cut bits, and target_edgeset = T - star + C = G0. Slots are cleared and donors RR. The predecessor key is restored exactly. In general, every accepted sigma's predecessor has o_j as a C_loc witness, so the forward channel (P_sigma, C_sigma, j) exists and maps back to T. The correspondence is a bijection.
- **Reverse failed images.** Several conditions each give an exact zero with no record: a_j adjacent to b_j (l.906), a duplicate restored edge, owner not an endpoint or pred-neighbourhood mismatch, donors not II, newborn bits not zero, unequal paired bits, and census != 2. Native owners are enumerated independently, so they still act on such states.
- **Aggregation only after primitives.** `_process_row` stores one entry per primitive. `_aggregate` (l.1649) sums duplicates only at assembly. `primitive_events` / `primitive_channels` return unaggregated records.
- **apply_* shapes and dtype.** `_checked_block` requires a plain ndarray [D,k] with exactly the operator dtype. The output is diag[:,None]*b plus CSR segment sums. Chunked `reduceat` boundaries are correct, rows are unique per segment, and the output has shape [D,k] in the operator dtype. apply_O multiplies by the real-cast read row.
- **einsum subscripts.** "nva,ai->nvi" and "nv,nv->n" (coarse reads) are correct. All einsums use optimize=False (AST-verified).
- **Reads versus the register spec.** Z = 1-2n is stored as int8 (+1/-1, 0 when absent). Presence, four first-moment Z, six pairs and m_alpha are recorded. R_alpha,i = (1/m_alpha) sum t_vi and S_alpha,ij = (1/m_alpha) sum t_vi t_vj use the current-state 1/m_alpha (np.divide where m>0). The port vectors match the spec's +-1/2 frame. Newborns sit in the owner's cell with no genealogy.
- **Caps.** max_dimension (l.1580) and max_graphs (l.1586) are checked before admission. max_events_per_row (l.1612) is checked before storing. All three fail via _Stop. Nothing is truncated.
- **Result dicts.** validate, build and reference_preparation return their declared key set on every path.

### Module B
- **Taylor recursion.** u_{n+1} = (-ih/hbar)/(n+1) H u_n, and w_{n+1} = (-ih/hbar)/(n+1)(H w_n + B G_n) with G_n = sum_p a''_p u_{n-p}. The window indexing (l.437-440, l.538-540) supplies u_{n-p} for p <= min(P,n). The coefficient matching was derived independently, and it agrees.
- **Residual polynomial.** The residuals derived independently are eta_psi = -sigma^N H u_N and eta_b = -sigma^N H w_N - sum_{j=N}^{N+P} sigma^j B Gt_j, with Gt_j restricted to j-p <= N. The code ranges (l.498-503) match exactly. The integral of sigma^j gives h/(j+1). The acceptance order and the accumulated sum are consistent: acc holds the order-n polynomial at test time.
- **Error-bound arithmetic.** eps_L += rho_psi. Then eps_b += rho_b + (||B_b||/hbar) eps_L(end) h sum|a''_p|/(p+1), which is the forcing error from the primal over the substep (l.1242-1244), with ||B_b|| = sum|cE| normE + max|dO|. Node bounds come from the exact identities <l_N\|A\|l_N> - <l\|A\|l> = <e\|A\|l_N> + <l\|A\|e> and <l_N\|A\|dl_N> - <l\|A\|dl> = <e\|A\|dl_N> + <l\|A\|e_b>, with Cauchy-Schwarz in Frobenius norm. The density path adds R1 = sqrt(D)||resid||_F (trace-norm bound) and the commutator response term 2||A|| ||B|| R1 int|f|/hbar. Source quadrature is exact. All of this is correct in exact arithmetic, and the uncovered rounding is stated.
- **Tangent forcing sign.** F = sum_alpha cE E_alpha G - dO*G, with dO = cO*values. This gives V_b = +f E_alpha (energy) and -f O_A (reads), and i hbar dl' = H dl + V l. It matches contract section 6, and the docstring's Kubo identity (resp = int f (cO chi_OA - cE chi_OE)) is consistent with delta<A> = -(i/hbar) int <[A_I(t), V_I(s)]>.
- **Purification contraction.** 2 Re sum_k s_k <l_k\|A\|dl_bk>, via einsum "xk,xbk,k->b" on conj(E l) (E Hermitian). Reads use w_x = sum s|L|^2 and z_bx = Re sum s conj(L) dL. The dLr reshape [D,m,r] matches the column layout (1+b)r..(2+b)r. In family mode, K = V^dag A dV + dV^dag A V is correct (Mb + conj swap).
- **Partial Legendre.** Gamma_QQ = -Y_OO^-1. Gamma_Qn = -solve(Y_OO, Y_OE). Gamma_nQ = -(solve(Y_OO^T, Y_EO^T))^T = -Y_EO Y_OO^-1. Gamma_nn = Y_EE - Y_EO Y_OO^-1 Y_OE. The contact signs (X_OE = chi_OE - C_OE and so on) are consistent with W_jj = chi_OO, W_jn = -chi_OE, W_nj = -chi_EO and W_nn = chi_EE. Basis rank, declared zero-mode exclusion and Y_OO singular values are all checked against the caller floor, with no regulator or pseudoinverse. Correct.
- **g00 contact.** N = sqrt(1+2n_g), J1 = 1/N, J2 = -1/N^3, and the contact is -J2<E> (+<E> at the flat point). This is consistent with H_{n_g n_g} = -H. Correct.
- **Caps, result dicts, interface.** The column budget is checked before each call. The substep plan and the working-entry estimate are checked before propagation and allocation. Every return path carries the full skeleton. B never imports A and calls every member with A's exact keyword names. The dtypes must be identical; a mismatch becomes an explicit failure, not a wrong number.

## AST / inertness (python3 -I -B on file text, scratch dir)
- A imports: numpy, cmath, math, sys, array, collections.abc.Mapping, itertools (permutations, product), typing.NamedTuple. B imports: numpy, math. No scipy.
- No MatMult or '@'. No dot, matmul, vdot, inner, tensordot, outer or kron. No print, open, exec, eval, input, warnings or errstate. No threads, global/nonlocal, async, lambda or yield. Every einsum has optimize=False.
- Module top level holds only imports, defs, classes, the docstring and literal constants. Nothing executes at import.
- All public functions and methods (A: 7 functions, 2 classes, 13 operator methods plus release_caches; B: 3 functions) are keyword-only with zero defaults.

## Notes (non-blocking)
1. A l.686 versus l.1736/1745: identity_allocation is admitted at |sum-1| <= 1e-12, but the build integrity tolerance is about 4 eps (max_row + n_alpha + 2), roughly 1e-13. An admitted allocation can therefore fail the diagonal sum_alpha E = H check (fail-closed but confusing), and state-level weights may sum to 1 +- 1e-12. Tighten admission to the integrity scale or document it.
2. A l.1156: the Ud diagonal record is omitted when (d - dstar)^2 == 0. Here a coefficient VALUE (dstar) removes a record, contrary to the L12 wording. There is no numerical effect.
3. A l.1886 (`_ice_extend`, recursion depth 2V0) and l.2047 (`eigh`) can raise RecursionError or LinAlgError uncaught from reference_preparation. This is unreachable at any realizable basis size.
4. B l.822 and l.1033: `stp["method"] != ...` and `pkind == ...` raise ValueError (ambiguous truth value) if a caller passes an ndarray there. This is a non-fail-closed path on malformed input only.
5. A state-level functions raise ValueError instead of returning result dicts. This is a declared deviation; the indexed builder is fail-closed.
6. B L4: second-order (n, j) responses ("actual second mean derivatives" in the register spec's source_columns) are not computed. Only linear responses plus raw first and second means are returned. Consistent with the shared interface, but root must source second-order terms elsewhere if needed.
7. The A/B dtype must be identical (A l.1931-1936, B l.378). A mismatch is an explicit failure.
8. Cost reality (A l.155-161, l.1553): the G0 block alone has 2^(3V0) C(2V0,V0) states, about 2.2e11 for the smallest simple q4 bipartite graph (V0 = 8). The integrated A->B path therefore fails at any practical cap without a controlled compression, as the contract acknowledges. This is honest reporting, not a defect.
9. A's interface deviations (8-field records, alpha label, plain-ndarray dtype rule, extra typed read rows, dict-valued reference_preparation) are all compatible with B. B reads the kind token from label[0], passes alpha from energy_cells and never calls primitive_events.
