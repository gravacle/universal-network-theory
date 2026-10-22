# FINAL CHECK 0405 V001: modules A and B, V002

**Role:** distinct checker. I wrote neither module, neither fix, nor the usage note.
**Date:** 2026-10-16.
**Method:** static text review only. Neither module, nor any legacy, UNT, Codex or root module (the root adapter included), was imported or executed. The only code run was `python3 -I -B` (Python 3.9.6) applying `ast.parse` plus an in-memory `compile` to the module TEXTS, and `diff -u`/`shasum`, all from my own scratch directory. No `__pycache__` exists in the artifact directory. No numerical control, propagation, data extraction, network access or package install was performed. No file whose name contains Newton, FIELD_, ROTATION, FIT, TRIAL, MOM1, rotmod or MassModels was opened, and no target velocity, validation outcome or historical fit/response array was read. Read-only access to `Universal Network Theory` was used to hash and read the binding texts.

## Verdict: PASS_WITH_NOTES

- Every blocking issue in both V001 reviews, and every forced item for A and B, is closed in the V002 texts.
- Each "not a defect" judgement by the fix authors is correct.
- My own `diff -u` of V001 against V002 shows no logic change outside the issues, beyond the benign representation and order changes listed in section 3.
- Both V002 modules pass the AST inertness check.
- The usage note matches the code. It has a few small omissions and one ambiguous notation (section 5), and it does not overclaim.

Remaining items (section 6) are non-blocking for the modules. One of them (R1) is an integration action that root must take in its own adapter before launch. Both modules remain **UNTESTED**: neither has ever been executed.

## 1. Hashes (sha256 computed from bytes by me)

| File | sha256 | bytes | Matches given |
|---|---|---|---|
| A `owned_parent_operator_v002.py` | `b5fded4d1272322036748d4d1b4e634a804c1da1ad6717e70e32b4f2a364a94e` | 128154 | yes |
| B `owned_retained_source_columns_v002.py` | `173f608d9b4effdf61c3ea0bfb147aaf5528a742c3ec2501d41f5397b36bbe81` | 116917 | yes |
| A V001 (preserved) | `27ad1762dbdc559eb92edcb6f7fe83790b73a4e23d71b12500b8586c811de3b6` | 103243 | yes, unchanged |
| B V001 (preserved) | `a9773a6dcdc5535d38808308b0d7ebf5ff89dc680b70144e5c3e57a9e2670a27` | 84801 | yes, unchanged |
| FIX_DELTA_0405_A_V002.md | `47a96b7623c093c8efe2b78419b427b38fedac6e921d94b03f89d38b530e6d9e` | 86521 | yes |
| FIX_DELTA_0405_B_V002.md | `23052ba6453cbecc962b4ad7039d229d69ec08be303eddb3fab3221b817b33b7` | 54551 | yes |
| USAGE_NOTE_0405_V001.md | `3abd1b9fd7131aaef1bdb63d16c653dcf51dbfb578f78c6b8cb437040b4197ae` | 13665 | yes |
| REVIEW_0405_FIDELITY_V001.md | `dfd97e2fa36a6510599245a3629106c1e51df3a2d75aa381d1b163ddecf5fd46` | 20827 | yes |
| REVIEW_0405_STATIC_CODE_V001.md | `9cd0ad3b5e9c578b3d9ae82f525185017aa86ba076cd9654face14b2e94f49c6` | 13447 | yes |
| CONTRACT | `fcad9039574f1666af005bb76a231f14b90f0c8dd82acebd2b16ab77941cd642` | | yes |
| MANDATORY ADDENDUM | `7cb15b4a5ac2ea33dfd43801c011142bc2b2388c3be0087152c049e78deccd39` | | yes |
| HP time-derivative addendum | `2fc9dc2c0197d6b3d0e2ff5893ba32b7ef89ba5424680bc06bd5210d5207226a` | | yes |
| 0405 / 0406 / 0407 | `7baab49ebbd01de684df56a074b823552c1eca9e787384ad0a0084144295c003` / `a465d9e3f703f2a2f19d383446c6a2bf6486e5f6be9fdf5996fc96dfb4693d50` / `f3f60cebd42db1120b2193968404644a1890cf2f5e48563c2d94544a4bd33fc3` | | yes (0407 had no pin; matches fidelity review) |
| 0408 / 0409 | `c0f0eaa940ce95c495fa2d7c21d59cae2a49e8028cc084df878d203e3c42e341` / `53465ac03cfb88bc7e641c15d8659591a315eafabb77dd966890e6dfb4ebb73c` | | yes |
| REG0408 / WHITEN companion | `f65dbc234ae082df342235b1a6c13a0282cf94665ba3e1c3989d12b12e7d7174` / `9eb4861cce5e4c435a259811dbca289e7e95a2b4ac34732c9f6c3ee56c34d7d7` | | yes |
| PALETTE move spec | `3b06ee3392894de2e96716c86f7b3184c792a407a81435f95aa448440418ca16` | | yes |
| Root adapter (text only) | `0705be7ca500a3b8329566ba014b80645231be2178ad5b8ef089dbca163b3f77` | | yes |
| V002 proposal / adoption | `494d0124c1cd49841760dfc49673d696eab3486d75b31fda708679fa5cacb78a` / `b5e7c2e3f12a6a4e3358a3c63a797783645d69240e757778ca42a91729a22465` | | yes |

## 2. Per-issue closure table (V002 line numbers)

| # | Source | Issue | Status | Evidence in final text |
|---|---|---|---|---|
| 1 | Fidelity B1 / forced_A 1 / forced_B 1 (both) | ADDENDUM item 1 time derivatives missing | **CLOSED** | B `_derivative_terms` l.702-732, `_contract_node` l.735-868, bounds l.1700-1712, one-sided assembly l.1716-1738, outputs l.1802-1857, L15-L17. A L9 l.286-301 states the explicit read/frame partial derivatives are zero. The A judgement (B is the single source of K(t); no A copy) is correct: the review allowed "in module B". |
| 2 | Static B1 / forced_B 2 (B) | Same gap, plus bounds, K' statement and LIMITATIONS | **CLOSED** | Bounds use c1 = 2‖H‖/ħ, c2 = 4‖H‖²/ħ², G1 (2/ħ)‖B_b‖‖A‖, G2 (8‖H‖/ħ²)‖B_b‖‖A‖, all on the v001 base eps_L(‖L_N‖+‖L0‖)+R1 (l.1613-1614, 1700-1712). The K' term f_b′ G1 is retained (l.1732-1733, bound l.1736-1737). The background K' = 0 statement is in `contacts["time_derivatives"]` (l.1001ff). L15 is recorded. |
| 3 | forced_B 3 (B) | Typed mu/M, explicit read/frame and K' contact inputs, coarse rows as read rows | **CLOSED** | New required `time_derivative_contacts` with exact keys and values. Any other value fails closed before propagation (l.1204-1230). `by_kind` derivative outputs per token; L18 typing. Coarse m/R/S rows are generic diagonal read rows. Implementing the read/frame input as a fail-closed declaration rather than numeric arrays is acceptable: an operator-level time-dependent read cannot pass through the shared interface. |
| 4 | Fidelity B2 / forced_A 2 (A) | One global 4x3 frame; B = −A not expressible | **CLOSED** | `_admit_frames` l.868-921 accepts four forms: global, {'A','B'} (newborn a_j in A and b_j in B, since vids < NA are exactly the A labels), per-vertex map, or callable. `_real_table` l.850-865 checks shape (4,3), real dtype (complex and bool rejected) and finiteness. The frames are used in `_reads_from_z` l.1752-1753. |
| 5 | forced_A 4 (0408 item 1 corrected by 0409 item 1) | Per-vertex negative B frames; adapter alignment; same moments in reads, H_c sources and derivatives; fixed whitening as explicit input; current-count normalization; full outgoing reads | **CLOSED** (integration action R1 is root's) | Required `registration['whitening']`: real, finite, nonsingular by an SVD ratio test (l.822-827). It is folded in as `frames_w` = W f_v[a] (l.841), so R' = W R and S' = W S Wᵀ. This matches the WHITEN companion (W = C0^(-1/2), Rprime = W R, Sprime = W S Wᵀ) and the adapter (W = √3/2, white_S = 0.75 raw_S). There is one `_reads_from_z` path for `read_rows`, `read_values` and `apply_O`, so B sources and derivatives use the same corrected rows. 1/m_alpha is per configuration. Ports are recomputed from the current graph and Z is rebuilt per state (`_z_bytes`), with no copied bits. The frame equals REG0408 (v_part,a = 2·prototype_part,a = ±T[a]). |
| 6 | Fidelity B3 / forced_A 3, 5 (0408 item 2) | `_edge_table` and `hop_BA` force all-pairs tables | **CLOSED** | `_edge_table` l.625 returns ('accessor', f) for a non-Mapping callable. `_edge_value` l.1214-1242 calls f(edge=(A,B)) only for edges actually met, validates with `_edge_scalar` (real and finite; complex h rejected), and caches. `hop_BA` is removed. `_amplitude` l.1532-1552 gives the same floats, −t·exp(iθ) and its conjugate. Missing entries are named failures at state level (l.1258-1274) and in the build (l.1966-1971, l.2213-2221). Build amplitudes are never formed after a coverage miss, because `_process_row` returns early. |
| 7 | forced_A 6 (0408 item 3) | Basis-free owner-palette enumeration | **CLOSED** | `palette_channels` l.1837, `_palette_scope` l.1415, `_owner_birth` l.1160. The membership rule matches the PALETTE text (Birth by owner j; sites by permanent group; edges if either endpoint group is selected; donors by owner; C_identity never). Per-owner `_root_cuts` (l.1043) gives exactly V001's channel set: W_G(C) is by construction the set of roots generating C, so "o_j ∈ W_G(C)" equals "C generated from root o_j". The (C, j) dedup is the same. Every reverse 4! pairing and every image test is unchanged. Global per-event costs are reported in L11 (a)-(d), L13 and resources. |
| 8 | forced_A 7 (0409 item 2) | Dense `newborn_edge_mask` | **CLOSED** | Masks and `_vertex_present` are removed. Equivalence: `_graph_info` defines slot j active iff a_j and b_j have current edges, and rejects half-present pairs. V001's "newborn has an incident edge" test is therefore exactly `newborn_at_target` (forward: target; reverse: source). Degree-owner calls pass only present vertices. Reachable graphs and Birth/reverse eligibility are unchanged. |
| 9 | forced_A 8 (0409) | Accessor called with the ordered (A,B) pair | **CLOSED** | `prof(edge=_edge_labels(dom, c))`, where the labels are (A label, B label). The adapter's `UniformEdgeProfile.__call__(self, edge)` accepts the keyword and checks the A then B parts. There is no all-pairs iteration. |
| 10 | forced_A 9 (0408 allocation) | endpoint_anchors_only, owner_vertex, uniform identity | **CONFIRMED** (no code change needed) | `_weights` l.1555: `edge_mode` false adds no edge anchor; `owner_vertex` adds the owner's vertex anchor to a set, counted once. The explicit `identity_allocation` with C_identity is admitted (A L2 l.228ff). |

## 3. Diff scope (own `diff -u` V001 to V002)

My diffs (A: 40 hunks, +639/−262; B: 22 hunks) are byte-identical, apart from the `---`/`+++` header lines, to the diffs embedded in FIX_DELTA A and B.

**A, changes beyond the issue text, judged benign:**
- **Birth record order** is now owner then cut; it was cut then root. Records are order-free. Distinct forward channels have distinct targets: a different slot, or a different G−C, because C ≠ C′ as edge sets. Distinct reverse pairings give distinct predecessors. So no two Birth records share (target, source), the lexsort/reduceat aggregation is unaffected, and stored H and E_alpha are unchanged.
- **The resources key `port_vectors_equal_register_spec` is removed** and replaced by `frame_mode`, `frames_A_equal_register_table`, `frames_B_equal_negated_register_table`, `whitening` and `edge_profile_kinds`. B only stores `resources()` as a dict, so B is unaffected.
- **Coverage is lazy**, with per-graph `coverage_ok` and per-edge accessor caches. The failure messages now name the reason. `primitive_channels` still requires full current-edge coverage and `diagonal_terms` still requires `edge_cells`, both as in V001.
- **Everything else is unchanged:** natives, diagonal items (same order under `_full_scope`), V002 weights, the reverse body and the reference family.

**B:**
- The change is purely additive. The only re-plumbing is that `HL` now comes from `apply_H` on [L, dL] and `EL` from `apply_E` on [L, HL(, H²L)]. Columns are independent, so v001 values are the same in exact arithmetic.
- Behaviour changes, all stated by the B fix author:
  - one new required keyword argument;
  - larger per-node column applications;
  - a larger memory estimate (12m+P+12 becomes 20m+P+30), so the caps now fail closed earlier.
- I re-derived every formula from iħρ′ = [K,ρ] and iħδρ′ = [H,δρ] + f_b[B_b,ρ], with <x|y> antilinear in x:
  - <L_A> = (i/ħ)(X − X†), X = <Hl|Al>;
  - <A_A> = −(Y + Y† − 2Z)/ħ²;
  - hom1 = P + P†;
  - hom2 = −(Q + Q†)/ħ²;
  - G1 = (i/ħ)(W − W†), W = <B l|A l>;
  - G2 = −(U + U†)/ħ², U = <HBl|Al> + <BHl|Al> − 2<Bl|A|Hl>;
  - response second derivative = hom2 + f G2 + f′ G1.

  All match, including the E_alpha "applied" pairings and the family [r,r] index order.
- B_b = Σ cE E_alpha − diag(dO_b) matches the v001 forcing sign. Bnorm = Σ|cE|‖E‖ + max|dO| is a valid bound on ‖B_b‖₂.
- The bounds are valid: `_node_bounds` is linear in the operator norm, and each derivative output is the exact expectation or response of a fixed Hermitian operator on the computed state.
- The one-sided profile indexing is correct: left is node k+1 from interval k, right is node k from interval k.
- **Sign note:** the B author's remark is correct. Under the coded convention, d<A>/dt = −(2/ħ) Im<Hl|Al> = (2/ħ) Im<Al|Hl>, so the static review's formula (2/ħ) Im<Hl|Al> has the wrong sign. V002 uses the convention-free commutator form.

## 4. AST inertness (re-run on final texts)

| Check | A V002 | B V002 |
|---|---|---|
| `ast.parse` and in-memory `compile` | OK | OK |
| Imports | numpy, math, cmath, sys, array.array, collections.abc.Mapping, itertools.permutations/product, typing.NamedTuple | numpy, math |
| `@` / dot / matmul / vdot / inner / tensordot / outer / kron | none | none |
| print / open / exec / eval / compile / `__import__` / lambda / global / yield / async / warnings / threads / os | none | none |
| `einsum` without `optimize=False` | none | none |
| Top level | docstring, imports, literal constants, defs and classes only. Class bodies hold only annotations, defs and docstrings (two NamedTuples, `_Stop(Exception)`, two classes). No decorators. | docstring, imports, literal constants (`LIMITATIONS`, two tokens), defs only |
| Public callables | 8 module functions plus all operator/context methods, keyword-only with no defaults (`palette_channels`: 3 kw-only) | 3 functions, keyword-only with no defaults (9, 2 and 10 args) |
| Unused private top-level functions / never-bound loaded names | none / none | none / none |

## 5. Usage note accuracy

**Matches the code:**
- **API:**
  - all 8 A public functions with their exact keyword sets;
  - the operator members;
  - `reference_preparation`, which returns a sparse isometry plus a dense L = V F [D,r] factor;
  - the 3 B functions with exact argument sets;
  - the preparation, source_columns and caps keys;
  - the exact `time_derivative_contacts` value;
  - the dtype identity requirement.
- **Shapes:**
  - n_read = 33·V0 + 10·n_E;
  - n_out = n_E + n_read;
  - means, response, time_derivatives (including one-sided [n_out, m, K_t]) and the family [r,r] tails.
- **Signs:**
  - H[n,j] = H + Σ n E − Σ j O and V_b;
  - the Kubo and χ relations;
  - Γ blocks identical to the B docstring;
  - the g00 contact −J2<E> = +<E>/N³;
  - hop −t e^{+iθ} for B→A;
  - R' = W R and S' = W S Wᵀ.
- **Error-bound statement:** it matches the covered and not-covered lists in B, and the "premises checked only as necessary conditions" wording.
- **Cost figures:**
  - D(1+18V0+132K) in resources;
  - 20m+P+30;
  - 2.2e11 at V0 = 8;
  - 2,359,296 codes at L = 8;
  - "a full build reaches its caps for any physical G0".
- **Not-implemented list:** matches A L4-L9 and B L3, L4, L9 and L13.

**Overclaim:** none. It states UNTESTED, says no V002 review existed when it was written, and states that no physical result follows.

**Minor findings (non-blocking):**
- **N1.** Section 2 writes the stepper as `{'taylor_residual', max_order, …}`. The actual key is `'method': 'taylor_residual'`, and a caller copying the notation would fail closed on the missing `'method'` key.
- **N2.** Section 6 says a source-dependent preparation "fails closed". It has no input at all: B L4 says it is "not computed", so it is unrepresentable rather than rejected. The lapse/background and read/frame items do fail closed, through `time_derivative_contacts`.
- **N3.** Section 3 omits the presence time-derivative arrays:
  - `presence_first`/`presence_second` [n_read, n_obs];
  - presence homogeneous/contact [n_read, m, n_obs];
  - presence one-sided [n_read, m, K_t].
- **N4.** Section 4 says the derivative bounds scale with 2‖H‖/ħ and 4‖H‖²/ħ². That is true for the mean and homogeneous parts. The contact bounds scale with (2/ħ)‖B_b‖ and (8‖H‖/ħ²)‖B_b‖, and the one-sided totals add |f|- and |f′|-weighted terms. The statement is incomplete but not wrong.
- **N5.** It does not say that `palette_channels` returns only the palette-OWNED diagonal records. Under the PALETTE MH ratio, the full diagonal D must come from `diagonal_terms` (A L13).
- **N6.** It does not mention the renamed A resources keys (section 3), or that a single global frame table is still accepted and only flagged (see R1).
- **N7.** Section 2 says `validate_owned_model` "returns a context". It returns {ok, stage_reached, failures, context}; the general result-dict sentence covers this.

## 6. Remaining real issues (none blocking module acceptance)

- **R1. Integration, root-owned adapter (action for root before launch).**
  - The adapter's `build_inputs` registration (0705be7c…) has the seven V001 keys: it has no `'whitening'`, and its `'port_vectors'` is the single A-frame table that the adapter itself labels a placeholder. V002 rejects the missing key by name, so the adapter's `bind_context` raises.
  - Root must add `'whitening'` = (√3/2)·I₃ (the adapter's own W, which equals C0^(-1/2) for C0 = (4/3)I) and `'port_vectors'` = {'A': T, 'B': −T}, with T the REGISTER table.
  - **Hazard:** if only `'whitening'` is added, V002 accepts the global placeholder. Every B vertex's coarse R row then has the wrong sign. This is flagged only in `resources()` (`frame_mode='global'`, `frames_B_equal_negated_register_table=False`). Root's binding should check those two flags before any launch.
  - This is not a module defect. Accepting a global common frame is a legitimate explicit option, and a default whitening would be a hidden default.
- **R2. Unquantified per-key memory (cost reporting gap).**
  - Canonical keys hold `edgeset` and `inc` as Python ints whose bit length reaches the largest current edge code (code = a·NB + (b−NA)).
  - At L = 8 that is about 786k bits (about 98 KB per int) for G0-supported states, and up to 2,359,296 bits (about 295 KB per int) once high-index newborn a_j are present. Two such ints per key give about 0.2 to 0.6 MB per stored key.
  - L11(a) reports the O(NA·NB) bit-operation cost but not the bytes per key. A sampler that stores many states should budget for this.
- **R3. Carried V001 non-blocking items, unchanged:**
  - A L12 says coefficient values never remove a record, but the Ud record is omitted when (d − dstar)² = 0 (l.1452-1454; amplitude zero, so no numerical effect);
  - identity_allocation is admitted at 1e-12 while the build integrity tolerance is about 1e-13, so an admitted allocation can fail closed;
  - in B, an ndarray passed as `stepper.method` or `preparation.kind` raises an ambiguous-truth ValueError (malformed input only);
  - A `_ice_extend` RecursionError and eigh LinAlgError are not caught (unreachable at realizable sizes);
  - A's state-level API raises ValueError (a declared deviation).
- **R4. Documented scope limits, not defects:**
  - Retained loop/count reads are not implemented, and no binding specification for them was supplied.
  - Second-order (n,j) responses are not computed.
  - Derivatives are only about the flat point with a fixed preparation. The HP addendum's self-consistent time-dependent K(τ) beyond linear order, and any time-dependent background, fail closed.
  - C′, C″ and the volume, H_v and a″ reads are formed by the caller.
  - B needs a fully built operator, and for any physical G0 the full build exceeds every practical cap (G0 block about 2.2e11 at V0 = 8). The production derivative path therefore exists only on finite toy-size components until a controlled reduction exists. Both modules say this honestly.
- **R5. Status.** Both V002 modules are UNTESTED: static review only, never executed by any author or reviewer. This check does not change that.

## 7. Statement

I am the distinct checker. I did not author either module, either fix, or the usage note. Nothing was imported or executed: no module, legacy file, UNT/Codex file, root adapter or test. Only static text operations (`ast.parse` and an in-memory `compile`, diff, sha256) ran from my scratch directory. No file in the artifact directory or under `Universal Network Theory` was modified. This file was written by exclusive create.
