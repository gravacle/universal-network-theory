# REVIEW 0407: sampler and detailed balance, v001

**Role.** I am a distinct reviewer and not the author. I reviewed by static, hand-traced reading of the text only. I imported or executed nothing: not the module, not the operator, and no UNT, Codex or legacy code. I ran no numbers and did no sampling. The only tool run was `python3 -I -B` with `ast.parse` plus `compile` on the file text, from my own scratch directory. No `__pycache__` was written to the 0407 directory. Date: 2026-10-16.

**Reviewed file.** `owned_collective_worldline_static_response_v001.py`, 83799 bytes, sha256 `0552b71c88547bf0d0795976d2d3c333d8c38388831c8dc5499cb8ddd909eb8f`. This matches the author's report. `CONVENTIONS_0407_V001.md` has sha256 `7787d6a54ac1dbdf9e5374b215a4df2c399dde5a7e5f932815816614cd76f182`, which also matches.

**Binding inputs.** All eight hashed inputs match their sha256 computed from bytes:
- task 0407 `f3f60ceb…3fc3`
- SPEC `915e8a43…80ec3`
- addendum `7cb15b4a…ccd39`
- contract `fcad9039…1cd642`
- 0406 `a465d9e3…3d50`
- register spec `032a564b…3e53d94`
- V002 `494d0124…cb78a`
- partial Legendre `d81d48e8…1b8b21663`
- Kubo/zero-mode `a7d048c1…edf7`

Of the assembly file I read only lines 300–327.

**Operator text.** The operator now exists: `owned_retained_response_0405/owned_parent_operator_v001.py`, sha256 `27ad1762dbdc559eb92edcb6f7fe83790b73a4e23d71b12500b8586c811de3b6`. It is a concurrent draft. I read it as text only, to align names and conventions.

## Verdict: FAIL (one blocking issue)

The core sampler and its detailed balance pass the hand trace: the CTMC proposal, endpoint rejection, Metropolis exponent, the selection density, the anchor and rotation moves, closure and bookkeeping, and the cap discipline. The estimator algebra also passes. The one blocking item is the verification of the positive-gauge member. Fixing it is small.

## Blocking

### B1. The member is verified only at visited states, and the delegated model-level check does not exist

**Lines:** 1765–1781 (model stage), 143–151 (LIMITATIONS L2), 1610–1613 (docstring).

**Issue.**
- The brief and SPEC §1 require the common-phase, zero-holonomy member: real h, t, g > 0, zero hop phases, a uniform admission phase, a common Birth phase and real diagonals. The rule is "verify, else unsupported".
- The module checks the gauge only for primitives enumerated at visited states (L807–817). It says that model-level membership "is otherwise delegated to validate_owned_model".
- The actual operator's `validate_owned_model` (L774–803, `_admit_model` L548–584 of the draft) does not check the member. It admits:
  - arbitrary `theta` on every edge key, including newborn and child edges, whose phase the sources leave UNCHOSEN (operator L5);
  - complex `kappa_v` per vertex;
  - complex `epsilon_j` per owner;
  - real `h` and `g` of either sign.
- A model outside the member can therefore return `complete` or `ok=True` when its offending coefficients sit only on primitives the chains never enumerate. Typical cases are newborn-edge `theta`, or `epsilon_j` for an owner whose Birth channel never became eligible.
- In that case the result is the |H|-gauged (sign-free) target, not exp(−βH). This is a target-measure guarantee resting on which states happened to be visited, against an explicit "verify, else unsupported" requirement. The error is bounded by the weight of the unvisited sectors when mixing is good. It is not bounded under metastability.

**Required fix.**
- Before sampling, verify membership at model level, independent of visited states. Either:
  - (a) require an additional `operator_api` callable, for example `positive_gauge_member(*, context, gauge_phases, tolerance)`; or
  - (b) check the `model` mapping directly, using the contract §3/§10 coefficient schema.
- Either way the check must cover every supplied coefficient:
  - h_e > 0, t_e > 0 and theta_e == 0 for every edge key, including newborn and child edges;
  - g_v > 0 for every vertex;
  - arg kappa_v equal to `admission_phase` for every vertex label;
  - arg epsilon_j equal to `birth_phase` for every owner;
  - all diagonal coefficients real.
- If the check is absent, fails, or cannot be evaluated, return `unsupported`.
- Keep the existing per-primitive visited-state check as a second line, and correct L2 and the docstring.

## Hand trace of the requested checks

| Check | Result | Where |
|---|---|---|
| Holding rate r(x) = Σ per-primitive W. Coincident destinations are separate marks, summed only for r. | PASS | 835–848 |
| Jump choice proportional to each primitive's W. | PASS (see N3) | 1093–1100, 1120 |
| Exponential waiting time with scale 1/r. An absorbing state (r = 0) is handled. | PASS | 1113–1119 |
| The segment runs for exactly the interval length. The last dwell is clipped at `length`. | PASS | 1116, 1195 |
| Endpoint rejection by canonical key, with no other filtering. | PASS | 1185–1187 |
| The exponent is exactly ∫new(r−D) − ∫old(r−D), over the same [0, length). Products of W cancel, giving π_new q_old / (π_old q_new). | PASS | 1078–1090, 1183, 1195–1196 |
| Log-space acceptance. No draw is made when log_acc ≥ 0. | PASS | 1196–1201 |
| Selection density: uniform start, a caller length mixture independent of path and source, an f = 1 component required, and the whole circle with probability p_whole. The reverse uses the same density. | PASS | 1157–1173, 546–551 |
| Whole-circle move: the anchor is the state at a uniform origin, regrowth runs for β, and the path must return to the anchor. | PASS | 1159–1161, 1176–1178 |
| Rotation: uniform origin, accepted with probability one. Segment and event reindexing is correct for s = 0, 0 < s < k and s = k. Valid only for static sources, which these are. | PASS | 1058–1075, 1154–1156 |
| Closure kept: new path = segs + rot.segments[m+1:]. The last new segment carries the terminal key, so the path stays closed for m = k. | PASS | 1202–1206 |
| Bookkeeping after accept and reject: rejection returns the original object, which nothing mutates; acceptance rotates back by β − origin. Segment count = events + 1 throughout. | PASS (see N4) | 1187, 1201, 1207–1211 |
| RNG comes only from the caller's per-chain Generator. There is no global numpy RNG. | PASS | 1094, 1114, 1154–1169, 1199, 1796 |
| Caps end the run as `incomplete` with diagnostics only, and no path is rejected because of a cap. The cap is checked before the event is appended. | PASS (see N6) | 777–782, 1121–1133, 1223–1224, 1818–1823, 1851–1856 |
| Positive-gauge check, with `unsupported` returned. | PARTIAL, see B1. Per-primitive check: PASS at 807–817. Gauge table against assembly lines 300–327, contract §3 and operator `_amplitude`: flip −h has factor 1; hop −t e^{±iθ} has factor 1; bind +g has factor −1; admit κ/κ* has factors conj(s_a)/s_a; birth ε/ε* has factors conj(s_b)/s_b. Each gauges to −\|·\|. | 657–692 |
| N_alpha > 0. A multiplier < 0 returns `unsupported`; = 0 marks a zero-rate direction. | PASS | 353–360, 820–831 |
| No basis enumeration (current-state channels only), no Born-count restriction, all reverses kept, reverse pairing checked at sampled events. | PASS | 774–851, 1004–1030 |
| Nothing cached across source changes. Segment D, r and Da are fixed for one run's sources. The `_measure` read cache is local to one call. There is no module-level state. | PASS | 939–959, 1289–1304 |
| Estimators. Lapse ρ = w̄/mult; for these affine coordinates W_ab = D_ab = 0, so T_ab = −Σρ_aρ_b. Also checked: S_j = ∫O, ∂_j log Z = β⟨O⟩, F_j = −⟨O⟩, F_n = ⟨E_α⟩, Cov(S, Ō) = d⟨O⟩/du, and the thermal Legendre Hessian +χ⁻¹. | PASS | 969–978, 1286–1287, 1328–1336, 1889–1890 |
| Zero-rate source-opening direction is dropped, with no division by zero. | PASS (visited states only, L6) | 827–831, 1860–1874 |
| Hard rules: imports are only bisect, math, collections.abc and numpy. No `@`, dot, matmul, vdot or inner. Every einsum passes optimize=False. No print, open, eval or exec. At module level there are only the docstring, imports, the LIMITATIONS constant, `_Stop` and function definitions. The one public function has 22 keyword-only arguments and no defaults. `ast.parse` and `compile` are clean. | PASS | — |

## Notes (non-blocking)

**N1. The current operator draft's API does not match the assumed one (final checker).** As written, every run against the draft returns `failed` at the first `_segment_at`. This is fail-closed and biases nothing. The differences:
- `primitive_channels` also returns `kind='diag'` records with `target_state=None`. The adapter must drop these from the jump list and take diagonals only from `diagonal_terms`, to avoid double counting.
- Weights are `energy_weights`, a tuple in `context.energy_cells` order, not a mapping `weights`. `lapse_factors` must then cover every energy cell.
- Diagonal records carry `amplitude`, not `value`.
- `read_rows` returns `{labels, values, presence}` arrays, not a list of records.
- `owner_id` for Birth may embed internal structures. The equality in `_initial_path` must then still return a single bool.

**N2. Reverse check.** The fallback scan starts only when the signature-filtered reverse sum is exactly 0 (L1012). A partial signature match among coincident destinations could raise a spurious "rate mismatch" `failed`. Suggest falling back whenever the filtered sums disagree. This is not reachable for the draft's kinds, whose destinations are unique.

**N3. `_choose_channel` (L1093–1100).** It accumulates with plain `+`, while r is a `fsum`, so the final channel can absorb O(ε) of extra probability. This is negligible. A cumulative sum consistent with the exit rate would remove it.

**N4. Time rounding.** Rotating and rotating back moves event times by O(ulp β) on each accepted move. If origin < ulp(β)/2, `back` rounds to β and the returned path stays rotated by `origin`. That rotation is measure-preserving, so it is harmless. The L15 coincidences end the run as `failed`, with probability about 0.

**N5. Chain independence.** Generators are checked by `id` only (L455). Identically seeded generators with identical initial paths would give identical chains: R-hat of 1 and a between-chain SE of 0, which could pass falsely. Suggest comparing `bit_generator.state`, or stating that this is the caller's responsibility.

**N6. Path cap and proposal length.** `max_events_per_path` is checked on proposals before endpoint rejection (L1127). Long whole-circle proposals (about βr events) therefore end the run even when they would have been rejected. That is consistent with no bias, but the cap must be sized for proposal length, not accepted length. Document this.

**N7. Batch SEs under failed mixing.** Per-chain batch-mean SEs are returned inside `mixing` even when mixing failed (L1452–1472). They are labelled as not an error band. Consider withholding them unless mixing passed.

**N8. Storage.** Storage is O(events × key size) (L3), against the SPEC's O(V0 + events). With the draft's int-bitmask keys this is O(V0) bits per dwell, and edgeset objects are shared between births. It is acceptable as documented.

**N9. Read covariances.** Read-read Duhamel covariances Cov(Ō_r, Ō_s) are not returned (L8). The same quantity comes as d²log Z by making those reads source coordinates, and C = M − μμᵀ is formed downstream, consistent with 0406 and the operator. The draft supplies coarse R and S as operator rows, so `extra_diagonal_reads` is not the only route.

**N10. Initial-path matching.** Initial events are matched by (kind, owner_id, target key), which needs `owner_id` to tell coincident destinations apart. A constant initial path is always admissible.

**N11. Mixing judgement.** Mixing is judged on the linear columns, not on the S_aS_b products (L13). The jackknife covers the products only through their batch structure. This is acceptable as an assessed error and not a bound.

**N12. Ambiguities L9–L11.** I accept the literal readings of L9–L11 (A as a fixed linear combination, the interval-density choice, and 1 + Σ n w̄ with a partition check). None of them affects detailed balance.
