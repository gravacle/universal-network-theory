# M1_REVERSIBILITY_0457_V001: reversibility of the whole-path admission residence transport

Claude4 lane, helper M1 (mathematical reversibility), dispatch 0457, 2026-10-16. This is a review input for the Claude4 lead. It is not the lane verdict and makes no mixing claim. Root (Codex1) owns physics, launches and acceptance. Nothing in it was run on the project: no sampling, project arrays, target data, V004/V006 import, or edits to author files.

## Pinned inputs (SHA256 verified at read time)

| Input | SHA256 |
|---|---|
| 0457 dispatch `FROM_CODEX/0457_2026-10-16_claude4_admission_residence_review.md` | `efdc659f…0f125f13` |
| 0456 author contract `FROM_CODEX/0456_2026-10-16_claude3_admission_residence_transport.md` | `4b33c8e4…2cddb87ac` |
| Birth template `…/coefficient_method/owned_worldline_birth_residence_transport_v001.py` | `6f866bda…8823f9f6e8` |
| Sampler base V004 `…/owned_collective_worldline_static_response_pairallk_v004.py` (read as text) | `7d079892…3c9` |
| V006 wrapper `…pairallk_v006.py` (read as text) | `896cadbb…6b7` |
| Operator V003 `claude_artifacts/owned_retained_response_0405/owned_parent_operator_v003.py` (read as text) | `a04f8795…7f07` |
| Module under review: `claude_artifacts/admission_residence_0456/admission_residence_transport_c3v001.py` (equal to `lead_copy_5b19e90e`) | `5b19e90ee4fcf86a0b8fe570abb607ae23c8047771abc4ab317c167f1837d653` |

Line references below are V004 `Lnnnn`, V003 `V3:Lnnnn` and c3v001 `C:Lnn`.

## Verdict (M1 scope)

- **The move is exactly π-reversible** under the standing contracts A1–A5. The proposal is: uniform vertex from a frozen roster, uniform admission mark of that exact owner at dwell 0, the operator's own transform applied to every dwell piece, guards G1–G5, and target-checked replay. The acceptance is min(1, R) with
  `log R = log(N_fwd/N_rev) − Σ_{i=0..k} Δt_i (D_new,i − D_old,i) + Σ_events [log W_new − log W_old]`.
  No admission amplitude, time density or event-count factor belongs in R.
- **c3v001 matches the derivation in every reversibility-critical line** (§7). On nine tiny toy operators, its exact transition kernel equals my independent reference kernel entrywise, with a maximum relative difference of 0.0, and satisfies detailed balance to ≤ 8.9e-16 (§8).
- **No reversibility defect was found.** §9 lists contract and wording notes.

## 0. Setting and standing assumptions

**Path.** A rooted closed path is ω = (k; σ; t):
- σ = (x_0,…,x_k; m_1,…,m_k), with key(x_k) = key(x_0).
- Each m_i is a positive primitive record (kind_i, owner_i) at x_{i−1} whose canonical target is key(x_i).
- t ∈ Δ_k(β) = {0 < t_1 < … < t_k < β}.

In code, `segs[i]` is x_i. `segs[k]` is the closing piece of the dwell that the origin cuts. `events[i]` is m_{i+1}. With `ends = [0]+times+[β]`, Δt_i = ends[i+1] − ends[i] for i = 0..k.

**Target.** The reference measure is λ = Σ_k Σ_σ δ_σ ⊗ Leb_{Δ_k(β)}. The target density is
`π(ω) = exp(−Σ_{i=0..k} Δt_i D(x_i)) · Π_{i=1..k} W(m_i)`.
This is per individual primitive mark, with no 1/K!, the same target as every other move (V004 docstring L332-333 and L680-682). D is the full `_segment_core` D: the lapse-weighted diagonal, −Σ j_a O_a, the pair source P and −λA (L2650-2685).

**Standing assumptions.** All are existing contracts, verified by reading only.
- **A1 (class functions).** Records, targets, W, D and rows depend on a state only through its canonical key. `V3:_admit_state` (L1459-1475) reduces every accepted representation to the key, and record targets are canonical keys.
- **A2 (identity).** There is at most one positive record per (kind, owner) per state. `_unique_mark` (L3207-3224) fails closed otherwise.
- **A3 (positivity).** W = |h|·mult > 0 and is finite. Zero amplitude or a zero multiplier means no record (L2231, L2254-2265). D is finite (L2662-2663).
- **A4 (off-diagonal).** key(τ(x)) ≠ key(x). Admission toggles (p_v, s_v), and `_no_self_loop` is at L2749.
- **A5 (frozen roster).** R is a unique tuple of graph0 original labels with group[v] = v, fixed independently of the current path. Write M = |R|.

## 1. Transform, bijection, unit Jacobian, MH ratio (items 1 and 4)

**Definitions.**
- o_v = ("admission", ("vertex", v)).
- For a ∈ {admit, admit_rev}, ā is the other kind (V004 kind table L1925-1926).
- τ_{v,a}(x) is the target of the unique positive a-record of owner o_v at x.
- S_v(x) is the set of positive records at x of kind admit or admit_rev with owner exactly o_v. N_v(x) = |S_v(x)|.

**Domain.** 𝒟_{v,a} is the set of skeletons σ that satisfy:
- **G1 (dwell):** τ_{v,a}(x_i) is defined for every i = 0..k. Write y_i = τ_{v,a}(x_i).
- **G2 (inverse/canonical):** the ā-record of o_v exists at y_i, and its target key is key(x_i), for every i.
- **G3 (closure):** key(y_0) = key(y_k). This follows from A1, which is why a failure here is a hard error.
- **G4 (replay):** for every event i, the (kind_i, owner_i) record at y_{i−1} exists and targets key(y_i).
- **G5 (reverse selection):** S_v(y_0) contains the ā-record of o_v with target key(x_0). This is G2 at i = 0, given A1 and A2.

**Transform.** T_{v,a}(k; σ; t) = (k; y_0..y_k; m'_1..m'_k; t), where m'_i is the replayed record.

**Lemma 1 (involution).** T_{v,a}(𝒟_{v,a}) ⊆ 𝒟_{v,ā}, and T_{v,ā}∘T_{v,a} = id on 𝒟_{v,a}. So T_{v,a} is a bijection from 𝒟_{v,a} onto 𝒟_{v,ā} with inverse T_{v,ā}.

*Proof.* Let ω' = T_{v,a}ω and check the guards for (v, ā) at ω':
- G1' is G2.
- G2' holds because τ_{v,ā}(y_i) has key(x_i), and by A1 its a-record of o_v is that of x_i, which targets y_i.
- G3' is the closure of ω.
- G4' holds because by A2 the (kind_i, owner_i) record at x_{i−1} is m_i, and m_i targets x_i since ω is valid.

The same facts give T_{v,ā}ω' = ω on canonical keys. ∎

**Jacobian.** T acts as the identity on (k, t) and as a bijection on skeletons, so T maps λ restricted to 𝒟_{v,a} onto λ restricted to 𝒟_{v,ā}. The dimension does not change and the Jacobian is 1. There is no simplex volume, 1/k! or insertion position.

**Proposal.** The label (v, a) is chosen with probability
`q_{v,a}(ω) = (1/M) · 1[a-record of o_v ∈ S_v(x_0)] / N_v(x_0)`.

**Theorem 1 (labelled detailed balance).** Let
`R_{v,a}(ω) = π(ω') q_{v,ā}(ω') / (π(ω) q_{v,a}(ω)) = [N_v(x_0)/N_v(y_0)] · exp(−Σ_i Δt_i [D(y_i) − D(x_i)]) · Π_i W(m'_i)/W(m_i)`
and α = min(1, R). Then for every label and all measurable A, B:
`∫_A π q_{v,a} α_{v,a} 1_B(T_{v,a}·) dλ = ∫_B π q_{v,ā} α_{v,ā} 1_A(T_{v,ā}·) dλ`.

*Proof.* Change variables with Lemma 1. Then use R_{v,ā}(ω') = 1/R_{v,a}(ω) and the symmetry of min(x, y). ∎

Consequences:
- q_{v,ā}(ω') > 0 by G2 at i = 0.
- Summing over the label involution (v, a) ↔ (v, ā) gives detailed balance of the whole move, including when two labels lead to the same ω'. The self-loop mass is diagonal, so πP = π.
- Since M is frozen, it cancels.
- **Zero-event path (k = 0):** log R = log(N_v(x_0)/N_v(y_0)) − β[D(y_0) − D(x_0)].

**Gauge.** Every replayed mark keeps its kind, so each event's gauge increment (dq, dns, dn) is unchanged (kind table L1919-1927). So is the closed path's net zero. N_S shifts by ±1 on all dwells, and no phase enters.

**Why there is no admission, time-density or event factor.** Neither ω nor ω' contains an admission event at v. The a-record is only the operator's lookup for the state map τ, which is applied to all k+1 dwell pieces. π(ω') has the same k replayed marks and the same times. No time coordinate is added, so there is no |κ_v| or W_adm, no Δt or β density, and no (k+1) count. Any such factor f breaks Theorem 1:
1. **A direction-independent f** (for example |κ_v|, W of the chosen mark, or β/(k+1)) gives R_fwd·R_rev = f² ≠ 1. The Hermitian pair has W(a at x_0) = W(ā at y_0), so the factor does not cancel.
2. **A reciprocal, direction-dependent f** (×|κ| for admit, ÷|κ| for admit_rev) keeps reciprocity but samples π·|κ_v|^{±1[v admitted]} ≠ π.

Toy mutants `adm_W` and `insert_event` violate detailed balance on every toy (§8).

## 2. Guard symmetry (item 2)

**Lemma 2.** ω ∈ 𝒟_{v,a} if and only if T_{v,a}ω ∈ 𝒟_{v,ā}, with T_{v,ā}T_{v,a}ω = ω. If ω ∉ 𝒟_{v,a}, then ω is not T_{v,ā}ω' for any ω' ∈ 𝒟_{v,ā}; otherwise Lemma 1 for (v, ā) would place it in 𝒟_{v,a}. A guard rejection is therefore never a one-way door.

How each forward guard at ω maps to the reverse move from ω' = Tω:

| Forward guard (c3v001) | What it gives the reverse from ω' |
|---|---|
| G1 dwell mark a at every x_i (C:L101-103) | Reverse G2: the a-records at τ_{v,ā}(y_i) ≅ x_i target y_i |
| G2 ā at every y_i, canonical target key(x_i) (C:L105-109) | Reverse G1 at every dwell, and the reverse lands exactly on ω |
| G3 closure (C:L111-112, hard error) | The reverse closure is the closure of ω |
| G5 reverse selection in the new dwell-0 roster (C:L113-116) | q_{v,ā}(ω') > 0, and N_rev = N_v(y_0) |
| G4 replay on y with target check (C:L127-129) | The reverse replay on x reproduces each m_i (A2 and validity of ω) |
| Stored-event check on x: mark, target, W = stored (C:L124-126) | Not a guard: the precondition ω ∈ supp π |

Implementation variants that would break exactness, or need care. Counts are violations/off-diagonal transitions from §8.
- **V1, state-dependent vertex choice.** "Eligible vertices only", "resample on empty" or "resample on guard failure" makes q depend on M(ω) ≠ M(ω'). Exposed:
  - hard-core toy: eligible_only 96/96; resample_guard 96/96;
  - ladder toy: resample_guard 45440/46464.
  
  On the V003-like toy both happen to be harmless (0 violations), because V003 admission guards are per vertex. Do not rely on that.
- **V2, wrong count rule.** A non-uniform mark choice (for example ∝ W), or N counted at a different dwell or with a different filter in each direction, gives the wrong Hastings factor. The `count` mutant is exposed only on the ladder toy, because N_fwd/N_rev ≡ 1 under V003.
- **V3, non-canonical comparisons.** Comparing raw or labelled states makes rejections depend on representation. A forward from a labelled-form path can fail while its reverse, whose new dwells are canonical operator targets, passes. c3v001 compares keys only. The toy ran 73 non-canonical representation cases, all identical to canonical.
- **V4, no per-dwell inverse/canonical check.** Then T need not be an involution when the operator's reverse is missing, or is not an exact inverse, at some dwell.
  - Exposed: non-Hermitian `edgeguard` 144/336 and non-involutive `lossy` 144/336.
  - The check is redundant under V003, where admit and admit_rev are exact XOR inverses with equal positive W, but it must stay.
- **V5, replay without the target check.** Replay without the target check, with aggregated or summed marks, or with first-match marks either leaves the support or unpairs the marks. `no_target` is exposed on the cond toy with 192 off-support transitions.
- **V6, partial transform.** Transforming only the dwells that carry the mark is never accepted.
  - **Lemma 3:** with dwell 0 and closing piece k transformed and target-checked replay, any boundary from an untransformed to a transformed dwell fails. The untransformed source carries the same record, whose target key(x_{j+1}) ≠ key(τ(x_{j+1})) by A2 and A4.
  - Toy kernel difference: 0.0.
  - The per-dwell dwell guard is still needed to define τ.
- **V7, hand toggling bits.** This is a different involution and may even be exact on V003-like states. It bypasses operator-owned masks and guards, which 0456 forbids. That is a contract issue, not a reversibility one.
- **V8, state-dependent reference dwell.** A reference dwell chosen in a way that T does not preserve (for example "first dwell where v has a mark") is not mirrored. `segs[0]`, fixed by the time origin, is preserved because times are unchanged.
- **V9, wider owner filter.** A group-level filter that includes newborn admissions stays exact if the same filter is used in both directions (newborn toy group_filter 0/2560), but it moves a different vertex than 0456 specifies (§6).

## 3. Self-loops and hard failures (item 3)

**Self-loops.** The kernel is P(ω,·) = Σ_labels q·α·δ_{Tω} + r(ω)·δ_ω. Detailed balance constrains only the off-diagonal part. Any rejection that depends only on (ω, label) and an independent uniform preserves π once Lemma 2 holds. The self-loops are:
- empty S_v(x_0): probability 1/M per such v, with no resampling (C:L91-93);
- failure of any of G1–G5;
- impossible replay, which is equivalent to π(ω') = 0;
- Metropolis rejection: accept iff log R ≥ 0 or u < e^{log R}, with u ~ U[0,1) (C:L138-139). The toy threshold test passed 48 of 48.

**Hard Stop.** A hard Stop ends the chain, and the run ends with status failed or incomplete. It is correct only for conditions that are impossible on supp π under A1–A5:
- a stored mark that is missing, targets the wrong key, or has W different from the stored value (W is recomputed deterministically);
- duplicate (kind, owner) records, which leave q undefined;
- a transformed path that is not closed, which contradicts A1;
- a non-finite log R or read change, which contradicts A3;
- a malformed roster, group or path;
- the event cap (`incomplete`).

**Why the split matters.** If a reachable condition (G1–G5 or replay) were a Stop, ordinary paths would end runs, and any retry-until-success policy would condition on avoiding them. If an impossible condition were a self-loop, a contract breach would be hidden and the chain would continue on unverified states.

**Budget, cap and enumeration stops.** These are interruptions, not rejections. c3v001 never writes into the input path; the toy checked 1375 interruption points with identical input snapshots and no committed diagnostics. Such stops must never be converted into rejections or resumed with fresh randomness inside one measurement stream. Doing so would sample from the move conditioned on not being interrupted, which is a cost-dependent bias. V006 declares `'resumable': False`.

## 4. N_fwd/N_rev under V003 (item 4)

**Under V003 the count term is exactly 0.**
- `V3:_transitions` L1590-1595: admit exists iff (p_v,s_v) = (0,0), giving (1,1); admit_rev exists iff (1,1), giving (0,0).
- Both kinds have owner ("admission", ("vertex", label_v)) (`_FAMILY` V3:L436-437; `_owner_id` V3:L1781-1791).
- W = |κ_v|·(1 + Σ_α n_α w_site[v]_α), with registration site weights (V3:L1717-1718; w_site is weight 1.0 on v's own cell, V3:L894). It does not depend on the state.
- Hence N_v(x) = 1[(p_v,s_v) ∈ {(0,0),(1,1)}] · 1[κ_v ≠ 0] · 1[site multiplier > 0] ∈ {0,1}.
- Every legal transition has N_v(x_0) = N_v(y_0) = 1.

**When N_fwd/N_rev ≠ 1 could occur in principle:**
- more than one admission primitive per owner and state, such as multi-level or cell-typed admission (ladder toy: N = 2 at the middle level);
- positivity of the admission mark that depends on the state and changes under T;
- a roster filter wider than the exact owner.

In every case, log(N_fwd/N_rev) is exactly the Hastings factor of the uniform mark choice, so the formula stays correct. The `count` mutant violates only on the ladder toy (46464/46464).

## 5. Detailed balance versus ergodicity and mixing (item 5)

**What Theorem 1 does and does not give.**
- Theorem 1 gives π-reversibility, and hence π-invariance, of this kernel only.
- A mixture with a state-independent selection probability of π-reversible kernels is π-reversible. A deterministic cycle is π-invariant.
- Root's schedule must choose this move with a probability that does not depend on the current path; the module chooses none.
- Irreducibility, aperiodicity, convergence and mixing belong to the whole sampler.

**This move alone is reducible.**
- It preserves k, the times, every event's (kind, owner) and every component other than (p_v, s_v).
- It acts only on 𝒟. Under V003 the status is binary, so each orbit within a fiber has at most 2^{|R|} paths; multi-level toys allow more.
- Irreducibility must come from the existing regrowth, palette, pair and rotation moves, which keep nonzero probability.

**When V003 admits the move** (as read; consistent with the base toy). The move is legal for v iff all three hold:
1. κ_v ≠ 0 and the site multiplier is > 0.
2. (p_v, s_v) is constant over all k+1 pieces and in {(0,0), (1,1)}. That means no admission or hop event at v.
3. For (1,1) → (0,0), there is no bind event at v, because bind needs p_v = 1.

Every other V003 event replays with unchanged W. No amplitude or energy weight depends on (p_v, s_v): `_amplitude` V3:L1641-1661, `_weights`/`_native_weights` V3:L1664-1721, `_birth_weights` V3:L1724-1739. birth_rev tests only newborn bits.

**What it changes.**
- (p_v, s_v) and N_S over the whole path, for one original vertex.
- D in each piece, through v's diagonal owners (ε_c p_v, E_S/E_R, λ_J d_v p_v, with their lapse multipliers and D_a). So under V003, log R = −Σ_i Δt_i ΔD_i, and ΔD_i varies with d_v(i).
- V003 `read_rows` depends only on occupancy (V3:L1970-1983 via `_reads_from_z`). So the source/pair/volume read terms and the tracked `row` are unchanged, and c3v001's read-integral diagnostic sums are expected to be exactly 0 for every accepted V003 move (as read, not executed).

**What it cannot change.**
- Paths in which v's status changes partway: any admission or hop excursion at v. These belong to the κ pair and regrowth moves.
- (1,1) paths with a bind event at v.
- Newborn admissions.
- k, the times, or event kinds and owners.

**Exactness is not efficacy.**
- Acceptance is the whole-path Boltzmann ratio exp(−Σ Δt_i ΔD_i), which is tiny when β|ΔD̄| ≫ 1.
- Legality fails whenever v has status-changing events.
- Acceptance and changed counts are not evidence of mixing. Whether the slow residence_ε_c/E_S, λ_J and Ud modes decorrelate is for root's measured run.

## 6. Owner format (item 6)

**The sampler-level owner** is the record owner_id ("admission", ("vertex", label)):
- V004 L2267-2279 sets `ch['owner']` from the record's owner_id.
- `_record_groups` (L2298-2301) reads owner_id[1] = ("vertex", label) and maps it through `run['group'][label]`.
- `run['group']` exists only under a palette binding (L5094-5111; default None at L4953). It maps each graph0 original label to itself and its slot newborns to that label.
- V003 K = V0 (V3:L585, L622), so every original vertex is a palette owner.

**Failure modes:**
- Filtering on ("vertex", v), or copying the Birth pattern `owner[1] == label`, gives empty rosters. The move then always self-loops: detailed balance holds trivially but the move is inert. The toy `bare_owner` mutant has 0 off-diagonal transitions on every toy.
- Vertex indices instead of labels make the group lookup fail.
- `group = None` must fail closed.

**Checklist and signals.**
- Use the exact owner tuple.
- Use the palette `frozenset((group[v],))`.
- Validate group[v] == v.
- A fixture with (p_v, s_v) = (0,0) must give N_fwd = 1.
- In a run, `admission_residence_empty_reference_vertex == attempts` signals an inert move.

c3v001 satisfies all of this: C:L57, L63, L58 and L74-79.

## 7. Code-review checklist (item 7), with c3v001 status from static reading

| # | Requirement (why) | c3v001 | Status |
|---|---|---|---|
| 1 | The roster is a frozen, unique, nonempty tuple of originals with group[v] == v, and the group map exists; otherwise fail closed (A5, §6) | L72-79 | yes |
| 2 | The vertex is chosen uniformly from the whole roster, whatever its eligibility; an empty roster self-loops with no resampling (V1) | L90-93 | yes |
| 3 | Marks are filtered on kind ∈ {admit, admit_rev} and the exact owner ("admission", ("vertex", v)), through palette `group[v]` (§6, V9) | L57-63 | yes |
| 4 | Roster uniqueness is enforced via `_unique_mark`, and an unexpected admission owner descriptor fails closed (A2) | L65-68 | yes |
| 5 | The mark is chosen uniformly from the roster; N_fwd = roster size at `segs[0]` (V2) | L94, L118 | yes |
| 6 | Inverse kinds: admit ↔ admit_rev (matches V004 L1925-1926) | L96 | yes |
| 7 | **Every** piece (k+1, including `segs[k]`) is transformed through the operator target and `_segment_core`; no copying or hand toggling (Lemma 1, V6, V7) | L99-104 | yes |
| 8 | Per-dwell inverse mark with canonical target equal to the old key (V4) | L105-109 | yes |
| 9 | A closure failure on the transformed path is a hard error (G3, A1) | L111-112 | yes |
| 10 | Reverse selection: unique ā in the new dwell-0 roster, targeting the old dwell-0 key; N_rev = new roster size (G5) | L113-118 | yes |
| 11 | log R terms and signs: log N_fwd − log N_rev; −Δt_i(D_new − D_old) with Δt from `ends`; +log W_after − log W_before (Theorem 1) | L117-130 | yes |
| 12 | No admission W, κ, time-density, β or k factor; the chosen mark's W is unused (§1) | L95, L117-132 | yes |
| 13 | Stored-event mark, target or W inconsistency is a hard failure (§3) | L124-126 | yes |
| 14 | Replay on transformed pieces checks the target key; failure self-loops; new events come from `_event_from_channel` (V5) | L127-131 | yes |
| 15 | Finite checks on log R and the read changes | L133-134, L143-144, L152-153 | yes |
| 16 | Budget checks: before the proposal, every enumeration and the commit, and between pieces in the loops | L50, L56, L71, L100, L123, L145 | yes |
| 17 | Atomic commit: the input path, segments, events and times are never mutated; the result is a new dict with a copied times list | L98-157 | yes (toy-verified) |
| 18 | Metropolis: accept iff log R ≥ 0 or u < exp(log R) | L138-139 | yes (threshold toy-verified) |
| 19 | Diagnostics: counts only; no hard-coded state-tuple index (no `key[6]`) | L38-46, L135-156 | yes |
| 20 | No global sampler patching, no schedule or mixture choice, inert import (`math` only) | whole file | yes |
| 21 | Root integration (outside the module): select the move with a fixed, path-independent probability; a budget stop ends the run and is never turned into a rejection | n/a | for root |

## 8. Synthetic exact-kernel evidence (`M1_check_v001.py`)

**Method.**
- Pure Python, single thread, no numpy; about 33 s.
- Command: `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -I -B M1_check_v001.py`. Exit 0 means `ALL_EXPECTATIONS_HOLD`.
- Every closed path is enumerated on fixed-(k, t) fibers: k ∈ {0, 2, 4, 6}, β = 1.7. Odd-k fibers are empty in these toys.
- Since the move preserves (k, t) and λ is counting × Lebesgue, fiberwise detailed balance for all t implies it on the whole space. The fixed t vectors are finite evidence; the proof covers all t.

**Toys.** These are not the native operator.
- **base:** V003-like. Admit only at (0,0) → (1,1), admit_rev at (1,1) → (0,0); q kept; sector #p = #s; flip, hop and bind.
- **wdep:** event W depends on s.
- **ladder:** three-level admission.
- **hardcore:** exclusion between vertices.
- **cond:** a bind whose target depends on s_a.
- **kappa0:** κ_b = 0.
- **newborn:** a same-group non-original vertex.
- **edgeguard** and **lossy:** deliberately non-Hermitian or non-involutive.

**Results.** There are 52,560 closed paths.
- **Reference kernel:** detailed balance with maximum relative error 8.9e-16, and global balance ≤ 6.7e-16.
- **Zero-event formula:** exact (error 0.0) on 1,472 transports.
- **c3v001, executed from hash-checked source with no bytecode**, through a mock that transcribes V004's `_record_groups`, `_palette_channels`, `_unique_mark`, `_keys_equal`, `_target_key`, `_check_times` and `_budget_check`:
  - its kernel equals the reference kernel exactly (maximum relative difference 0.0) over 57,344 changed transitions;
  - |Δ log MH| = 0.0;
  - detailed balance holds with 0 violations.
- **Contract checks on c3v001:**
  - 1,375 budget interruptions: input unchanged, no commit;
  - 48 stored-W corruptions: `failed`;
  - 73 non-canonical representations: identical outcomes;
  - 48 Metropolis threshold pairs;
  - 6 roster or group misuse cases: fail closed.

**Mutants** (violations/off-diagonal transitions):

| Mutant | base | wdep | ladder | hardcore | cond | edgeguard | lossy | newborn |
|---|---|---|---|---|---|---|---|---|
| reference / c3v001 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| sign of ΔD | 6528/6528 | 1088/1088 | all | all | all | all | all | all |
| count dropped | 0 | 0 | 46464/46464 | 0 | 0 | 0 | 0 | 0 |
| admission W factor | all | all | all | all | all | all | all | all |
| inserted-event factor | all | all | all | all | all | all | all | all |
| event-W dropped | 0 | 704/1088 | 0 | 0 | 0 | 0 | 0 | 0 |
| Δt index shifted | 6412/6528 | 992/1088 | 28800/46464 | 64/96 | 800/896 | 144/192 | 144/192 | 736/1664 |
| replay target unchecked | 0 | 0 | 0 | 0 | 192/1088 | 0 | 0 | 0 |
| eligible-only vertex | 0 | 0 | 0 | 96/96 | 0 | 0 | 0 | 0 |
| resample on guard failure | 0 | 0 | 45440/46464 | 96/96 | 0 | 0 | 0 | 0 |
| no inverse check | 0 | 0 | 0 | 0 | 0 | 144/336 | 144/336 | 0 |
| bare owner ("vertex", v) | 0/0 (inert) | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 |
| group filter | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0/2560 (exact) |
| partial transform | identical to reference (Lemma 3) | | | | | | | |

## 9. Contract issues, notes and untested cases

**Contract and wording notes.** None blocks reversibility.
1. **0456 owner prose.** 0456 says the owner is ("vertex", v). The sampler-level owner is ("admission", ("vertex", v)). c3v001 uses the correct form; any other consumer must too (§6).
2. **INTERFACE wording.** INTERFACE_0456_V001 says "only attempt-level counters can have been recorded before an interruption". In fact `<kind>_selected`, rejection reasons, `legal_transport` and `admission_residence_last_proposal` (C:L97, L135-137) are written before the commit checkpoint (C:L145). An interruption there leaves a last-proposal record for a move that was never committed. This affects diagnostics only, not the path.
3. **Uninformative diagnostic.** Under V003 the read-integral diagnostic is expected to be identically 0, because reads depend only on occupancy. A D or D_a integral built from existing segment fields would show the actual residence change without any new formula. Root's choice.
4. **Exact float equality.** `before['W'] != ev['W']` uses exact equality, inherited from the template. This is valid under deterministic recomputation (A1); nondeterminism would fail closed, loudly rather than with bias.
5. **Integration conditions (root).**
   - Select the move with a fixed, path-independent probability.
   - Run only with a palette binding (`run['group']`).
   - Treat budget, cap and enumeration stops as terminal (incomplete), never as rejections or resumable with new randomness.

**Untested here:**
- native V003 states and the real V004/V006 functions (mock transcription only, with no palette-verify mode, lapse multipliers, enumeration caps, Birth events, source/pair/volume D terms, D_a or allk fields);
- interaction with rotation and the schedule;
- any statement about mixing or efficacy.
