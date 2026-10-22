# REVIEW 0410 MODES V001: owned collective worldline static response, v003

**Role.** Distinct reviewer, not author. I did not write v003 or any earlier version of this module, its DELTA or its CONVENTIONS note.

**Method.** I read the files as text and traced them by hand. I imported and executed nothing: not the module, not either operator, not the root adapter, and no UNT, Codex or legacy code. I ran no numbers, did no sampling and extracted no data. The only code I ran was:
- `shasum -a 256`;
- `diff -u`;
- `python3 -I -B` doing `ast.parse`, `compile` (no exec) and `symtable` on TEXT copies of v002 and v003 in my own scratch directory.

There is no `__pycache__` in the 0407 directory or in my scratch directory. I wrote nothing in `Universal Network Theory`, and I opened no file with a forbidden name. This file is the only file I wrote in the 0407 directory, and I wrote it by exclusive create. Date: 2026-10-16.

## Verdict: PASS_WITH_NOTES

- **Blocking issues: none.** I found no wrong math, normalization or target distribution, no interface mismatch that gives wrong numbers, no crash on valid input and no hard-rule violation.
- The 0410 section 1 / MODE SPEC section 1-2 requirements are implemented. The estimator algebra and the extensive normalization are correct by hand trace.
- R1, R2 and R3 from FINAL_CHECK_0407_V001 are closed.
- Runs without mode directions are unchanged from v002, apart from the intended R1 API name and three additive result keys.
- Notes N1-N11 below are non-blocking. N1 and N2 matter for root integration: N1 is the input form, which fails closed; N2 is the Mandel coefficient convention.

## Hashes (full sha256, recomputed from bytes)

| File | sha256 | Status |
|---|---|---|
| owned_collective_worldline_static_response_v003.py (164654 B, 3486 lines) | e367f240e3cfc38300dee75a85a56bc13fb1eaa2ee8f3a26fe8a270216e97721 | matches the author report |
| owned_collective_worldline_static_response_v002.py (base) | 0d041119bd11227746238663ed93d99863d3a94c8295e539dbed15255b42a941 | unchanged |
| owned_collective_worldline_static_response_v001.py | 0552b71c88547bf0d0795976d2d3c333d8c38388831c8dc5499cb8ddd909eb8f | unchanged |
| DELTA_0410_MODES_V003.md | c7b7dff2bbc745f90a31e90bb9ac61ca1dfc5e6f2ea5508acbba267b489dab7a | matches the author report |
| CONVENTIONS_0407_V003.md (333 lines) | 09f26701cab08e3c00eea5d27c2d038411a16d17499563b0de6c745043f71fe8 | matches the author report |
| FINAL_CHECK_0407_V001.md | 1e352a9eac3d672bf93da60ba4c00270eb1279269208e5052628b060e1d19042 | binding, matched |
| FIX_DELTA_0407_V002.md | 94c1518231d42b58418111f790611d3c5d635195e6fbc4d88c5c66e2757a7b41 | read |
| REVIEW_0407_PALETTE_V001.md | 251a6077291e44bc1f3a658abc138cfeacf16084684b7720c8561e1646d20c29 | read |
| 0410 brief | ac1db8fa81c06672d495448b82835072978dee8bce0d3a017044de29cc440e34 | binding, matched |
| MODE SPEC (read fully) | 2b294c7a59758aa994bf043c0c01e2e3cf0a3ec9327d5ec35757826851d46f9b | binding, matched |
| operator owned_parent_operator_v002.py (present, so used) | b5fded4d1272322036748d4d1b4e634a804c1da1ad6717e70e32b4f2a364a94e | binding, matched |
| root adapter owned_diamond_registration_input_adapter_v001.py | 0705be7ca500a3b8329566ba014b80645231be2178ad5b8ef089dbca163b3f77 | binding, matched |
| registration JSON | f65dbc234ae082df342235b1a6c13a0282cf94665ba3e1c3989d12b12e7d7174 | binding, matched (hashed; semantics only) |
| whitening companion JSON | 9eb4861cce5e4c435a259811dbca289e7e95a2b4ac34732c9f6c3ee56c34d7d7 | binding, matched (hashed; semantics only) |
| 0409 brief (R3 wording check) | 53465ac03cfb88bc7e641c15d8659591a315eafabb77dd966890e6dfb4ebb73c | read |

## Diff verification

- My own `diff -u v002 v003` has 1034 lines: 41 hunks, 604 added and 64 removed lines. Apart from the two header path lines, its body is **byte-identical** to the fenced diff in DELTA_0410_MODES_V003.md, lines 158-1191.
- An AST comparison of every module-level def (v002 against v003) gives:
  - 8 new defs: `_admit_mode_direction`, `_mode_field`, `_mode_fields`, `_mode_metadata`, `_mode_outputs`, `_projected_weight`, `_uniform_kinds`, `_uniform_labels`;
  - 0 removed defs;
  - 14 changed defs: `_admit_coordinates`, `_admit_label_roles` (message only, R3), `_admit_operator_api` (R1), `_analyze` (`tracked_all`), `_channels_from_records`, `_diagonal_at`, `_event_from_channel`, `_index_read_labels`, `_new_result`, `_palette_channels` (R1), `_reads_at`, `_segment_core`, `_unsupported_raw_kinds` (docstring only, R3) and the public function.
- Every change maps to the mode addition, R1 or R3. No change touches the move code (`_move`, `_select_interval`, `_interval_move`, `_ctmc_segment`, `_palette_move`, `_rotate`, `_initial_path`), the estimators `_measure`/`_estimate`/`_layout`, R-hat or Sokal. The RNG consumption order is therefore unchanged.

## Requirement trace (v003 line numbers)

| Requirement (0410 s1 / MODE SPEC / task) | Evidence | Status |
|---|---|---|
| Project scores and log-contacts onto caller profiles BEFORE storage; no 640-coordinate cell Hessian | Lapse directions: `_diagonal_at` L1685 and L1715-1716 form D_a = Σ_diag d_X v_X per record. `_event_from_channel` L1974-1975 forms ρ_a = v_X/mult per event. v_X = Σ_α φ_α w_αX comes from `_projected_weight` L1465-1467 over the record's own nonzero weights. Source directions: `_reads_at` L1895-1904. Per dwell only `Da[n_u]` and `row[n_r]` are stored (`_segment_core` L1924-1937); per event only `rho[n_u]`. `_measure` (unchanged, L2459-2482) builds S[n_u] and T[n_u,n_u]. No per-cell list exists for a mode direction: `lapse_terms` holds only tuple `("lapse", cell)` coordinates. The callback's per-cell R'/S' dicts are transient per state and never stored. | MET |
| Signed lapse-cell and read-label weights; no nonnegative-partition admission on mode weights | `_admit_mode_direction` L872-955 requires only finite reals, not identically zero. There is no sign, sum or partition test. The partition check `_lapse_multiplier` L1448-1462 still applies to the operator's `energy_weights` only. | MET |
| Same incoming/outgoing endpoint-averaged allocations as H[N] | v_X uses the same `weights` dict that enters `mult` (L1535-1536, L1709-1710). Operator v002 supplies (w(y)+w(x))/2 for Birth (`_birth_weights` op L1615-1630). For flip, hop, bind and admit the source and target supports coincide (`_native_weights` op L1594-1612; the edgeset is unchanged), so the average is the same. Diag records use w(x). | MET |
| Same corrected current-graph read/source callback as the physical Hamiltonian | The source-direction D_a (L1895-1904) is computed inside the callback block from the SAME `adapted_moment_reads` evaluation (L1841-1851) that gives P(x) in D (L1858-1885, L1921). Base sources stay the callback j_R'/J_S'. No operator coarse row is used. | MET |
| Full joint cos/sin block (normally 20); no phase averaging or isotropy | All declared directions are coordinates of one joint run (`run["coords"]`). `_analyze`/`_estimate` give the full joint Hessian and jackknife. `_mode_outputs` L2796-2813 selects the block with `np.ix_` and does not symmetrize, average or decouple. | MET |
| EXTENSIVE F_total gradient/Hessian | `_mode_outputs` L2814-2815: F_total_gradient = −g/β and F_total_hessian = −(Cov+⟨T⟩)/β. There is no division by S. | MET |
| Joint errors | `error_layout_positions` (L2803-2804, L2824): gradient y = p; Hessian y = n_us + tri(p,q). My hand check of `tri` against `np.triu_indices` row-major gives a·n − a(a−1)/2 + (b−a) plus the n_us offset, which is correct. F standard errors are se/β when mixing passed (L2833-2838). The full replicates and covariance stay in `errors`. | MET |
| Actual profile/Gram metadata | `_mode_metadata` L2696-2786 at binding (L3326-3331): per profile S = Σφ², Σφ and c1 = Σφ/S (metadata only); unit-pairing Gram G_mn; largest normalized off-diagonal; directions; base lapse, base read sources and the whitened j_R'/J_S' actually used (after raw conversion, since `run["pair"]` is read after L3307). | MET |
| Separately tracked uniform first/pair moments | Cell sums Σ_α R'_α,i and Σ_α S'_α,ij (i ≤ j) come from the same evaluation (L1905-1910). They are appended as 9 tracked columns (`tracked_all` L3174-3175) with means, responses and error positions (L2839-2853). Reserved labels: input L3082-3089, operator collision L1735-1740. | MET |
| No division by the mode norm inside the sampler | I searched by hand: S and c1 appear only in `_mode_metadata`. No score, covariance, contact or estimate is divided by S. | MET |
| Keep the original coordinate interface | The tuple branch of `_admit_coordinates` (L981-1023) is unchanged except for one failure message. The public signature is AST-identical: 0 positional, 23 keyword-only, no defaults. | MET |
| Root does pairing/Legendre (not implemented) | No J, Legendre, Gram dual, background contact or EH pairing appears in the code (L22). | MET |
| R1 palette call against actual operator v002 | See the API section. | CLOSED |
| R2 CONVENTIONS_0407_V003.md | See the R2 section. | CLOSED |
| R3 coarse-row wording | See the R3 section. | CLOSED |

## Estimator algebra and normalization (hand trace)

For a closed path, the weight is w = exp(−∫D) Π_events W. Every coordinate is affine: N_α(η) = N_α(base) + η φ_α for a lapse direction, and D(η) = D₀ − η Σ_α φ_α Σ_f c_f O_α,f for a source direction. Then:

- **Lapse direction.**
  - mult_X(η) = 1 + Σ_α (N_α(base) + ηφ_α − 1) w̄_αX = mult_X + η v_X.
  - Hence W_a/W = v_X/mult_X and ∂²log W = −(v_X/mult_X)².
  - D_a = Σ_diag d_X v_X.
  - The code matches: L1974-1975 and L1715-1716; T from `_measure` L2477.
- **Source direction.**
  - D_a = −Σ_α φ_α Σ_f c_f O_α,f and W_a = 0, so ρ = 0. `rho` is initialized to zeros and set only for lapse coordinates (L1969-1975).
  - The code matches: L1895-1904.
- **Moments.** S_a = −∫D_a + Σρ_a and T_ab = −Σρ_aρ_b. Therefore ∂_a log Z = ⟨S_a⟩ and ∂_ab log Z = Cov + ⟨T⟩. With F_total = −log Z/β, F_a = −⟨S_a⟩/β and F_ab = −(Cov+⟨T⟩)/β.
- **Normalization against MODE SPEC s2.** F_mode = F_total/S, so F_mode,a = −⟨s_a⟩/(βS) and F_mode,ab = −(Cov+⟨t⟩)/(βS). This follows from the returned extensive values by one division by S at the root. Because no sample is divided by S, the S² error that MODE SPEC s2 warns about cannot occur.
- **Projection identity.**
  - S_dir = Σ_α φ_α S_(lapse α) and T_dir,dir' = Σ_αβ φ_α φ'_β T_αβ hold exactly for every path.
  - The stored columns are therefore exactly P^T s_full and P^T t_full P, without forming the per-cell objects (MODE SPEC s1).
  - Combining declared directions by a further fixed P after the run is exact for means and for jackknife replicates, because all are linear in y.
- **Q_ext.** `projected_read_means_extensive` = ⟨S_a⟩/β = Σφ Σ c ⟨O⟩ on source rows (L2816-2822). This is correct.
- **Zero-rate.** If mult_X = 0 and v_X ≠ 0, then W = 0 but W_a ≠ 0, so the direction is dropped and listed (L1544-1551, L6). This is correct, and unreachable at a positive base lapse with partition weights.
- **Coefficient c_f.** For c_f on S'_ij with i < j, H_c contracts both S'_ij and S'_ji. A Mandel component j_M = √2 J_ij therefore gives D_a = −√2 φ S'_ij, so c_f = √2. Moving the symmetric pair (L20) gives c_f = 2. The documented relation c_f = mult × (pair_source_S coefficient) is correct.

## Actual operator / adapter API compatibility (text only)

| v003 calls | Actual source | Result |
|---|---|---|
| `palette_channels(*, context, state, palette_owners)` (`_admit_operator_api` L554; `_op` L1645-1646) | op v002 L1837 `palette_channels(*, context, state, palette_owners)`. `_admit_palette` L1820-1834 accepts list, tuple, set or frozenset of ORIGINAL owner labels (`owner_index` over A+B, op L580). It returns palette-owned diag records plus member transitions (L1858). | **Match.** The module passes a frozenset of A+B labels; the binding stage checks palettes ⊆ A+B (L3276-3290). Held replays pass `_record_groups` output, which is also original labels. Diag records are skipped (`_palette_members` L1630-1631). |
| owner_id formats for groups (`_record_groups` L1574-1599) | op v002 `_owner_id` L1672-1684; `_FAMILY` L393-394 (admit and admit_rev give "admission") | match |
| `energy_weights` dense tuple aligned with `context.energy_cells` | op `_dense` L1687-1691; `energy_cells = reg["cells"]` L964 | match; v_X uses the same dict as mult |
| coarse row kinds refused | op v002 `_read_layout` L924-948 still emits `coarse_first_R` / `coarse_second_S` | the refusal still triggers (L8, R3) |
| `adapted_moment_reads(*, operator_module, context, state, binding)` returning `cells`, `R`, `S` | adapter L177-232. `cells = binding["registration"]["cells"]` (L186) is the same registration object as the operator's (identity check, L701-706). R and S are configuration-normalized and whitened (L223-227), and S is exactly symmetric. | match. The source-direction cell equality (L3319-3325) holds by construction for the actual chain. |
| `pair_source_hamiltonian(*, reads, j_R, j_S)` | adapter L235-251 | match (unchanged from v002) |
| `raw_to_whitened_sources(*, j_R_raw, j_S_raw)` | adapter L254-257 | match (unchanged) |

Mode directions need no new operator or adapter function.

## Interface, semantics and inertness

- **Prior interface.** For runs without mode directions, `tracked_all == tracked`, `n_r` is unchanged, `lapse_dirs`, `source_dirs` and `uniform_labels` are empty, and `_diagonal_at`'s third return value is empty. `_segment_core`, `_event_from_channel`, `_analyze` and the outputs therefore give exactly the v002 values. The additive keys are `modes: None`, `inputs.mode_directions: []` and `conventions.mode_directions`. The only behavioural change outside modes is R1 (see N6).
- **Caps / incomplete.** No cap, truncation or new random draw is added. The existing caps still end a run as `incomplete` (L14), and the mode projections do not alter any rate, D or acceptance.
- **Crash scan on valid input.**
  - `phi[cell]` lookups are safe: the profile keys equal `context.energy_cells` (L3311-3318), and the source cells equal the callback cells (L3319-3325, `_whitened_moments` L1777-1786).
  - `modes_in[c]` cannot KeyError, because a tuple coordinate tagged `lapse_direction` or `source_direction` fails admission (L1013-1019).
  - When every mode direction is dropped, `_mode_outputs` handles an empty `sel` (empty index arrays and `np.ix_`).
  - I found no crash.
- **AST (my own, text copy, `python3 -I -B`):**
  - parse and compile: OK;
  - imports are only `bisect`, `math`, `collections.abc.Mapping` and `numpy`;
  - no `MatMult`, and no `dot`/`matmul`/`vdot`/`inner`/`tensordot`/`linalg`/`outer`/`kron` name or attribute;
  - 10 `einsum` calls, all `optimize=False`;
  - no `print`/`open`/`eval`/`exec`/`compile`/`__import__`/`input`/`globals`/`locals`/`vars`/`breakpoint`/`exit`/`quit` call; the two `getattr` calls are the v002 record/field accessors (L503, L693);
  - no `os`/`sys`/`subprocess`/`threading`/`socket`/`pickle`/`ctypes`/`io`/`pathlib`/`shutil`/`multiprocessing`/`asyncio`/`time`/`random` name, and no numpy save/load/tofile attribute;
  - module level holds the docstring, 4 imports, the `LIMITATIONS` string constant, `class _Stop(Exception)` and 92 defs; there are no decorators and no global/nonlocal, so nothing runs at import; the only lambda is the sort key (L942);
  - `symtable` finds no undefined globals;
  - one public callable with 0 positional and 23 keyword-only parameters and no defaults, identical to v002.

## R1, R2, R3

- **R1 (closed).**
  - `_admit_operator_api` requires `palette_channels` (L554).
  - `_palette_channels` calls it with `palette_owners=owners` (L1645-1646). The verify path and the messages use the new name (L1647-1670).
  - The stale "not on disk" / ASSUMED text is gone: a grep finds no `owner_restricted`, `not on disk` or `ASSUMED`.
  - L1 (L233-240), the module docstring (L102-107), COST (L208), L19 (L358, L364) and the public docstring (L2971) are updated.
- **R2 (closed).** CONVENTIONS_0407_V003.md covers:
  - the signature, including `diagonal_read_source_callback`, `palette_parameters` and the mode inputs (s1, s6);
  - the actual operator record fields and `palette_channels` (s2);
  - all outputs, including `member_check` and `modes` (s7);
  - H_c with −j_R'·R' − J_S':S', and the pair and mode coordinates with multiplicities (s3);
  - the model-level member check (s4) and the palette move (s5);
  - cost, storage and measurement (s9);
  - L1-L23 (s11).

  I spot-checked its line references (`_move` L2175, `_palette_move` L2265, `_model_member_check` L1330, `_mode_metadata` L2696, `_mode_outputs` L2789) and they are correct. One wording imprecision is in N6.
- **R3 (closed).**
  - The refusal reason is now worded in L8 (L289-299), the `_unsupported_raw_kinds` docstring (L575-582), the admission message (L790-794) and the public docstring (L3007-3010).
  - The reason is the 0409 rule "avoid allocating or duplicating unsupported raw moment sources". This matches the 0409 text, line 15.
  - Operator v001 (one global frame) and operator v002 (per-part B = −A frames plus whitening, op L1750-1753) are both named.
  - The logic is unchanged.

## Blocking issues

None.

## Notes (non-blocking)

- **N1. Input form differs from the MODE SPEC's literal minimal API (fails closed).**
  - MODE SPEC s1 writes `{kind:'source_direction', label_weights:{label:coefficient}}`. v003 instead requires:
    - `id` and `profile_id`;
    - `cell_weights` for both kinds;
    - for source directions, a factorized weight φ_α·c_f over the nine cell-free whitened fields.
  - A spec-literal or per-cell-label form is rejected at admission as `failed`; it never gives wrong numbers.
  - The 10/20-column use case is fully expressible in the v003 form. Non-factorized weightings need several directions plus a post-hoc P.
  - The root runner must build the v003 form. The author records this (DELTA limitations 1-2).
- **N2. The Mandel factor is the caller's.** c_f is applied to the tensor element S'_ij, so an off-diagonal Mandel direction needs c_f = √2 (the symmetric-pair coordinate needs 2). A caller who passes 1, intending a unit Mandel component, gets that column scaled by 1/√2: its gradient row by 1/√2 and its Hessian diagonal by 1/2. This is documented (L21, CONVENTIONS s6). The root should set the coefficients explicitly.
- **N3. The nonorthogonality flag has no tolerance.** The flag at L3466-3472 fires for any nonzero normalized Gram off-diagonal. Floating-point cos/sin profiles on the L=4 lattice will usually leave rounding residues of about 1e-16, so the flag can be expected in normal runs. It is informational only. Root should read `profile_gram`.
- **N4. Uniform `n_cells` and the sum domain.**
  - `uniform_moments.n_cells` is `len(context.energy_cells)` (L2775), but the sums run over the callback cells (L1906-1910).
  - Callback cells must equal the energy cells only when source directions exist (L3319).
  - With the actual adapter both are `registration["cells"]` of the same object, so they agree by construction. A non-actual adapter with a different cell set and lapse-only directions would make the root's sum/n_cells inconsistent.
  - A robustness tightening, not a defect for the actual chain.
- **N5. Normalized F_mode and Q_mode are not returned.**
  - 0410's EXTENSIVE convention is followed. MODE SPEC s2's "report both" is satisfied only through S, c1 and Q_ext, which allow one division at the root.
  - Background μ and M come as cell sums; the root divides by n_cells.
  - Recorded by the author (DELTA limitations 6-7).
- **N6. The R1 behavioural change and the "exactly v002" wording.**
  - DELTA says runs without mode directions "compute exactly what v002 computes", and CONVENTIONS line 12 says v003 "changes no v002 logic for runs without mode directions".
  - This holds for every sampled value. The palette API contract did change, as R1 intends:
    - an operator mapping that exposes only `owner_restricted_channels` (the FINAL_CHECK alias route) now fails closed;
    - actual operator v002 now runs where v002 failed.
- **N7. Uniform columns join the mixing judgment.** The 9 uniform columns are primary mixing columns (L2583). With mode directions and the callback, they can make mixing `failed` or `unassessable` and so suppress error bands. This is consistent with the tracked-read rules; noted for the run budget.
- **N8. Positions not listed.** Error-layout positions are listed for the uniform means but not for `mode_responses`. They follow from the documented a-major layout: y = n_us + n_us(n_us+1)/2 + n_r + a·n_r + r.
- **N9. Partial `base` metadata.** `modes.base` omits λ and the volume-gradient coefficients; they are in `result["inputs"]`. MODE SPEC s1 assumes a uniform translation-invariant background, but uniformity of the base lapse and sources is not checked. The root can check it from `base`, and must for the MODE SPEC s3 uniform contact shortcut.
- **N10. Stale message.** The `_admit_coordinates` message "must be a list or tuple of tuples" (L961) predates the mapping form.
- **N11. Carried items.**
  - Operator v002 still has no review file (FINAL_CHECK R7).
  - The FINAL_CHECK R4 integration notes are unchanged: the registration needs `whitening` and per-part `port_vectors`, the same object must be used as `binding["registration"]`, and `binding["L"]` is required.
  - Also unchanged: R5 (callable `.value` declaration) and sampler N2/N5/N6/N7.
  - 0410 section 2 (the equal-time two-hop sector) is out of scope for this delta.

## LIMITATIONS of this review (recorded, not resolved)

- Compatibility rests on static reading of operator v002 and the adapter. Nothing was executed.
- "Orthonormal" profiles are the caller's declaration. I checked that the Gram is reported, not that any caller profile is orthonormal.
- Whether the declared directions form an invariant block of the full static source Hessian (MODE SPEC s3, s5) is the root's to establish. The module does not test it, and neither did I.
- The unit cell pairing is accepted as the adopted pairing on the basis of the registration's uniform cells. A weighted pairing would need the weighted dual throughout (L22).
- I made no claim about mixing, acceptance, cost or physical values. No physics, value, scale or target was chosen or read.
