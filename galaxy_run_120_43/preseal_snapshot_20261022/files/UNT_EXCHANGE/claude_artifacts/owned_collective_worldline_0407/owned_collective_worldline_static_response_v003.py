"""Owned collective static response by positive imaginary-time worldlines.

UNT task 0407, version v003: v002 (sha256
0d041119bd11227746238663ed93d99863d3a94c8295e539dbed15255b42a941, preserved unchanged) plus the
0410 section 1 direct real-mode derivative columns, the FINAL_CHECK R1 operator v002 palette
call and the R3 coarse-row wording. v002 was the fix of v001 (sha256
0552b71c88547bf0d0795976d2d3c333d8c38388831c8dc5499cb8ddd909eb8f, preserved unchanged) for the
review/0408/0409 blocking items: model-level member check, additive blocked-palette move,
actual operator API, root adapter read/source callback. Static author implementation: written
as text and never imported or executed by its author. numpy plus the Python standard library.

Binding sources (sha256 computed from bytes before writing; all read-only):
  * UNT_EXCHANGE/FROM_CODEX/0407_2026-10-16_main_collective_worldline_evaluator.md
    f3f60cebd42db1120b2193968404644a1890cf2f5e48563c2d94544a4bd33fc3
  * helpers/coefficient_method/
    OWNED_COLLECTIVE_POSITIVE_WORLDLINE_STATIC_RESPONSE_IMPLEMENTATION_PROPOSED_V001.txt
    915e8a43607bb93885b00c888a144d9f18fdbea0fccee046f9dab41523a80ec3   ("SPEC")
  * helpers/coefficient_method/
    OWNED_RETAINED_PROVIDER_IMPLEMENTATION_MANDATORY_READ_AND_LABEL_ADDENDUM_V001.txt
    7cb15b4a5ac2ea33dfd43801c011142bc2b2388c3be0087152c049e78deccd39
  * helpers/coefficient_method/
    OWNED_RETAINED_RESPONSE_FULL_H_SOURCE_COLUMN_IMPLEMENTATION_CONTRACT_V001.txt
    fcad9039574f1666af005bb76a231f14b90f0c8dd82acebd2b16ab77941cd642   (operator definition)
  * UNT_EXCHANGE/FROM_CODEX/0406_2026-10-16_response_moments_and_current_state_keys.md
    a465d9e3f703f2a2f19d383446c6a2bf6486e5f6be9fdf5996fc96dfb4693d50
  * CODEX1/COARSE_REGISTER_STATE_BOUNDARY_WORKING_SPECIFICATION_V001.json
    032a564bd018b7302bd60de633f8e3c9d2f91f8c079f16b62548bce0e4e53d94   (semantics only)
  * CODEX1/GALAXY_COLLECTIVE_MODEL_ASSEMBLY_2026-10-15.md, lines 300-327 only
    (common-phase zero-holonomy unitary gauge)
  * CODEX1/COARSE_PROPER_TIME_ENERGY_COUPLING_PROPOSAL_V002.json
    494d0124c1cd49841760dfc49673d696eab3486d75b31fda708679fa5cacb78a   (counted assumption)
  * helpers/coefficient_method/COARSE_ENERGY_PARTIAL_LEGENDRE_METRIC_COUPLING_CANDIDATE_V001.md
    d81d48e8407f5576305dbbb50a275f163401bbb91f67b5938dc9736ec8b21663
  * helpers/coefficient_method/UNIFORM_ENERGY_KUBO_IDENTITIES_AND_LEGENDRE_ZERO_MODE_V001.md
    a7d048c11a826d6d2627afd3f5324458a0350bc6abbd58bd8ab8d6c39d7eedf7
v002 additions (sha256 from bytes before writing; read-only; values never taken from them):
  * UNT_EXCHANGE/FROM_CODEX/0408_2026-10-16_collective_palette_and_physical_registration_binding.md
    c0f0eaa940ce95c495fa2d7c21d59cae2a49e8028cc084df878d203e3c42e341
  * UNT_EXCHANGE/FROM_CODEX/0409_2026-10-16_actual_adapter_and_remaining_all_pair_allocation.md
    53465ac03cfb88bc7e641c15d8659591a315eafabb77dd966890e6dfb4ebb73c
  * helpers/coefficient_method/OWNED_WORLDLINE_BLOCKED_PALETTE_MOVE_IMPLEMENTATION_V001.txt
    3b06ee3392894de2e96716c86f7b3184c792a407a81435f95aa448440418ca16   ("PALETTE"), with its
    distinct review helpers/response_packet_audit/OWNED_WORLDLINE_BLOCKED_PALETTE_DISTINCT_REVIEW_V001.json
    42e4041006a07e3d9f5a44afbd079077be1e60ef91919d34251915f0e2f8de35
  * claude_artifacts/owned_retained_response_0405/owned_parent_operator_v001.py
    27ad1762dbdc559eb92edcb6f7fe83790b73a4e23d71b12500b8586c811de3b6   (ACTUAL operator API,
    read as text)
  * helpers/coefficient_method/owned_diamond_registration_input_adapter_v001.py
    0705be7ca500a3b8329566ba014b80645231be2178ad5b8ef089dbca163b3f77   (root adapter, read as
    TEXT only; its public callables are reached at run time through a caller-supplied object)
  * helpers/recovered_packet_audit/OWNED_DIAMOND_CURRENT_GRAPH_COLLECTIVE_REGISTRATION_PROPOSED_V001.json
    f65dbc234ae082df342235b1a6c13a0282cf94665ba3e1c3989d12b12e7d7174 and its companion
    OWNED_DIAMOND_WHITENING_DUAL_SOURCE_MANDATORY_COMPANION_V001.json
    9eb4861cce5e4c435a259811dbca289e7e95a2b4ac34732c9f6c3ee56c34d7d7   (semantics only)
v003 additions (sha256 from bytes before writing; read-only; values never taken from them):
  * UNT_EXCHANGE/FROM_CODEX/0410_2026-10-16_direct_mode_columns_and_equal_time_pair_completion.md
    ac1db8fa81c06672d495448b82835072978dee8bce0d3a017044de29cc440e34   (section 1 only)
  * helpers/coefficient_method/OWNED_WORLDLINE_REAL_MODE_SCORE_AND_METRIC_PAIRING_SPEC_V001.txt
    2b294c7a59758aa994bf043c0c01e2e3cf0a3ec9327d5ec35757826851d46f9b   ("MODE SPEC")
  * claude_artifacts/owned_collective_worldline_0407/FINAL_CHECK_0407_V001.md
    1e352a9eac3d672bf93da60ba4c00270eb1279269208e5052628b060e1d19042   (items R1, R2, R3)
  * claude_artifacts/owned_retained_response_0405/owned_parent_operator_v002.py
    b5fded4d1272322036748d4d1b4e634a804c1da1ad6717e70e32b4f2a364a94e   (ACTUAL operator v002
    API, read as text; its palette_channels is the palette enumeration called here)
Style reference (read as text): claude_artifacts/scalar_metric_solve_0397/
scalar_metric_particular_solve_v002.py (fail-closed result dict).

PUBLIC ENTRY (keyword-only, every argument required, no defaults):
  owned_collective_worldline_static_response(*, operator_api, graph0, model, registration,
      initial_paths, beta, lapse_factors, source_coefficients, volume_gradient_coefficients,
      volume_multiplier, gauge_phases, derivative_coordinates, tracked_read_labels,
      diagonal_read_source_callback, chain_generators, move_parameters, palette_parameters,
      caps, burn_in_sweeps, measurement_sweeps, error_parameters, numerical_tolerances,
      implicit_closure)
The v002 signature is unchanged (no public argument is added in v003): the 0410 mode
columns enter as fixed affine direction mappings inside derivative_coordinates (MODE SPEC
s1 "minimal API delta"; L21), next to the unchanged tuple coordinate interface.
It returns a plain fail-closed dict with "ok", "status" (complete | incomplete |
unsupported | failed), "stage_reached" and "failures". When ok is False every populated
field is evidence only, never a result.

OPERATOR API: the ACTUAL owned_parent_operator_v001.py / owned_parent_operator_v002.py API
(state level, basis free; the operator module is NOT imported here). The caller passes
`operator_api`, a mapping or object exposing these module-level, keyword-only callables:
  validate_owned_model(*, graph0, model, registration)
      -> {"ok", "stage_reached", "failures", "context"}; context.energy_cells is the ordered
         tuple of coarse cells (a "status" "unsupported", if ever returned, is passed through).
  canonical_state_key(*, context, state) -> canonical key (tuple of ints); equal keys <=>
      equal current labelled configurations (0406 item 2); == must give a single bool.
  primitive_channels(*, context, state) -> list of records BEFORE aggregation with fields
      owner_id, kind in {diag, flip, hop, bind, admit, admit_rev, birth, birth_rev},
      target_state (canonical key; None for diag), amplitude (complex <target|h_X|state>),
      queried_support, changed_support (tuple of hashable anchors), energy_weights (tuple
      aligned with context.energy_cells, (w(target)+w(source))/2). Records of kind "diag"
      are the diagonal owners; they are skipped here and read through diagonal_terms. Every
      reverse reconnection is a record; coincident destinations stay separate records. A
      record with amplitude exactly 0 is skipped (no jump mark).
  diagonal_terms(*, context, state) -> the kind "diag" records; the real diagonal value is
      the record amplitude and energy_weights[alpha] = w_alphaX(state).
  read_rows(*, context, state) -> {"labels": state-independent tuple of typed labels,
      "values": float64 [n], "presence": float64 [n]}; absent rows have value 0.
  palette_channels(*, context, state, palette_owners) -> the ACTUAL operator v002 palette
      enumeration (op v002 L1837; absent in operator v001): the primitive_channels records
      (same fields) of every primitive whose permanent palette groups (classification below)
      meet `palette_owners`, passed here as a frozenset of original owner labels, with all
      Birth reverse alternatives and full current eligibility; its palette-owned "diag"
      records are skipped. Required only when palette_parameters is not None.
ROOT ADAPTER (owned_diamond_registration_input_adapter_v001.py; diagonal_read_source_callback
supplies the adapter object at run time; these ACTUAL signatures are called unchanged):
  adapted_moment_reads(*, operator_module, context, state, binding) -> {"cells", "R", "S",
      ...}: whitened, configuration-normalized (current present count) coarse moments.
  pair_source_hamiltonian(*, reads, j_R, j_S) -> -j_R.R' - J_S:S' (whitened duals).
  raw_to_whitened_sources(*, j_R_raw, j_S_raw) -> (j_R', J_S') (only for source_frame "raw").
Kind -> gauge increments (contract section 3 + assembly lines 300-327): flip and hop
change no record bit, cell or slot; bind flips one record bit q_v; admit R->S raises the
Spent number N_S by one (admit_rev lowers it); birth adds one active slot N with
newborns loaded R,p=q=0 (birth_rev removes it). Reverse pairs: flip<->flip, hop<->hop,
bind<->bind, admit<->admit_rev, birth<->birth_rev.
Palette classification (PALETTE; permanent labels inside the operator owner_id): birth and
birth_rev ("birth", owner, cut) -> {owner}; flip and hop (family, ("edge", (A, B))) ->
{group(A), group(B)}; bind, admit and admit_rev (family, ("vertex", v)) -> {group(v)}; with
group(original o) = o and group(a_j) = group(b_j) = o from graph0["slots"]. Forward and
reverse primitives carry the same owner_id, so membership is reversal invariant.

WHERE THE SPEC IS IMPLEMENTED
  Section 1 (member, gauge, H_c, beta, component): _model_member_check (model-level, every
    supplied coefficient, before any state is visited), _admit_gauge_phases, _gauge_table,
    _channels_from_records (per-primitive gauge check at visited states, W >= 0),
    _diagonal_at (real diagonals), _segment_core (H_c = H[N] - sum_a j_a O_a - pair
    sources - lambda A); validate_owned_model is called first.
  Section 2 (closed paths, no basis, primitive jump marks): path dict {segments,
    events, times}; _segment_core/_channels_at enumerate only the current state's
    channels; per-primitive W with lapse weights BEFORE aggregation; r(x) = sum W.
  Section 3 (detailed-balance moves): _move dispatcher; _interval_move (global
    unconditioned CTMC regrowth from the fixed initial endpoint, endpoint rejection,
    min(1, exp{int_new(r-D) - int_old(r-D)}) in log arithmetic, all lengths < beta plus
    the whole circle with anchor fixed), _rotate (uniform origin rotation, probability
    one), _ctmc_segment; ADDITIVE _palette_move (PALETTE; held outside marks, restricted
    inside CTMC, held-rate ratios) with the global moves kept at nonzero probability.
  Section 4 (estimators): _measure (S_a, T_ab, time-averaged reads), _estimate
    (<S>, Cov(S,S) + <T>, read means, Cov(S, read)), result "estimates".
  Section 7 (cost and errors): caps -> status incomplete (never rejection); _analyze
    (batch means, jackknife joint covariance, integrated autocorrelation, R-hat across
    independent chains, mixing status); storage/work described under COST.
  Section 5 is NOT implemented: implicit_closure must be None (contract retained).
  Section 6 is scope: see "scope" in the result and CONVENTIONS_0407_V003.md.
WHERE THE MODE SPEC (0410 section 1) IS IMPLEMENTED (v003, L21-L23)
  MODE SPEC s1 (fixed real columns before storage): _admit_mode_direction (signed weights,
    no partition admission), _diagonal_at (lapse direction D_a = sum_diag d_X v_X with
    v_X = sum_alpha phi_alpha w_alphaX), _event_from_channel (rho = v_X / multiplier from
    the endpoint-averaged transition weights), _reads_at (source direction D_a = -sum_alpha
    phi_alpha sum_f c_f O_alpha,f from the SAME callback evaluation that enters H_c);
    _measure stores only the projected n_u columns; no full cell Hessian is formed.
  MODE SPEC s2/0410 (extensive outputs): _mode_metadata (binding stage) and _mode_outputs
    fill result "modes" (F_total gradient/Hessian, extensive score/contact moments, profile
    S, sum, c1 and Gram, base sources, error positions, uniform first/pair moments from the
    _reads_at cell sums); no division by any mode norm.
  MODE SPEC s3-s5 (Legendre, J, contact, metric/EH pairing, block admissibility) are the
    root metric adapter's and are NOT implemented here.

SEMANTICS. In the positive gauge G = (-1)^{sum_v q_v} (-e^{i phi_adm})^{N_S}
(-e^{i phi_birth})^{N} (assembly lines 300-327, e^{-i theta} epsilon = -|epsilon| written
as -e^{i phi_birth} = e^{i theta}), every primitive matrix element h_X[y,x] becomes
conj(G(y)) h_X[y,x] G(x); it must equal -|h_X[y,x]| (real, nonpositive) within the
caller's relative gauge_phase tolerance, otherwise status "unsupported" (outside the
proven common-phase zero-holonomy member). Before that, _model_member_check verifies the
member on the caller's model mapping itself, for every supplied coefficient (L2). With
n_alpha = N_alpha - 1 and the V002 support mean weights wbar_alphaX,
    W_X(x->y) = |h_X[y,x]| * (1 + sum_alpha n_alpha wbar_alphaX)        (per primitive),
    D(x) = sum_diag d_X(x) (1 + sum_alpha n_alpha w_alphaX(x))
           - sum_a j_a O_a(x) + P(x) - lambda A(x),     A(x) = sum_a a_a O_a(x),
    P(x) = pair_source_hamiltonian(reads(x), j_R', J_S') = -j_R'.R'(x) - J_S':S'(x)
           (root adapter callback, whitened duals; 0 when the callback is None),
    r(x) = sum_X W_X(x->.),   H_c = D - W,   Z = Tr exp(-beta H_c).
Every new state (after every transition, Birth included) gets FULL diagonal_terms,
read_rows and callback reads; the SAME evaluation enters D, every D_a and the tracked
time averages (no copied-bit shortcut, no output-only correction).
A closed path on the imaginary-time circle [0, beta) has weight
exp(-int D) prod_events W. Source coordinates u are ("lapse", cell) [d/dn = d/dN],
("source", label) [j_label], ("volume_multiplier",) [lambda], ("pair_source_R", cell, i)
[j_R'[cell][i]] and ("pair_source_S", cell, i, j), i <= j [the symmetric pair J_S'[i][j] =
J_S'[j][i], declared multiplicity 1 if i == j else 2] and (v003) the fixed affine mode
directions {"kind": "lapse_direction"} [N_alpha = N_alpha(base) + eta phi_alpha] and
{"kind": "source_direction"} [H_c gains -eta sum_alpha phi_alpha sum_f c_f O_alpha,f]
(L21); all are affine, so D_ab = W_ab = 0 exactly and
    S_a  = -int D_a + sum_events W_a/W,       T_ab = -sum_events W_a W_b / W^2,
    d_a log Z = <S_a>,   d_ab log Z = Cov(S_a, S_b) + <T_ab>,
    F_a = -<S_a>/beta,   F_ab = -(Cov + <T>)/beta.
For a lapse coordinate F_{n_alpha} = <E_alpha> is the full (diagonal plus offdiagonal)
coarse energy mean; for a read source F_{j} = -<O>. Time-averaged diagonal reads
Rbar_r = (1/beta) int O_r give <O_r> and d<O_r>/du_a = Cov(S_a, Rbar_r) on the SAME
ensemble. Imaginary time and Monte Carlo sweeps are never physical or native time.

CONVENTIONS. Thermal Legendre: with F = -log Z / beta and H_c = H[N] - j.O, the
functional F + j.Q (Q = <O>) has QQ Hessian +chi^-1 (F_jj = -chi_OO^iso, F_nn =
-chi_EE^iso, F_nj = +chi_EO^iso, chi^iso_AB = int_0^beta <dA(tau) dB(0)>). Real-time
action signs are not imported. The result is the STATIC ISOTHERMAL native functional
(fixed beta, re-prepared canonical state), not fixed-preparation retarded response and
not the complete metric propagator; no EH matching, c_star, scale or normalization is
supplied or used. Absolute F is not estimated (needs a normalization not implemented).

COST. One stored path holds one state object, canonical key and O(n_u + n_r) numbers per
dwell segment plus O(n_u) numbers per event: O(events * (state size + n_u + n_r)) through
this state-level API (see LIMITATIONS L3). Each generated event of a global move costs one
primitive_channels, one diagonal_terms, one read_rows, one canonical_state_key and (with
the callback) one adapted_moment_reads call at the new state, all O(current vertices) or
O(registered labels) in the worst case, plus the reverse-pairing check. A palette event
replaces the full channel enumeration by palette_channels (restricted exit rate
r_S) but KEEPS the global diagonal_terms / read_rows / callback reads per new state, and
one restricted enumeration per old dwell segment inside the interval: the remaining
global per-event cost is reported, not hidden (L3, L19). Exit rates of segments created by
palette moves are enumerated lazily when a global move needs them. A measurement uses the
stored per-segment read rows and costs O(events * (n_u + n_r)) arithmetic. Error analysis
stores O(chains * measurements * (n_u^2 + n_r)) numbers and O(J * n_y) jackknife
replicates. No Hilbert-space list, basis index or dense operator is built. Mode directions
(v003) add, per new state, O(diagonal records * nonzero weights * lapse directions) for the
lapse projections and O(cells * fields) per source direction plus O(9 * cells) for the
uniform moments; per event O(nonzero weights * lapse directions). n_u counts directions
(e.g. 20 for one joint cosine/sine block), never cells times fields, so per-sample storage
is O(n_u^2 + n_r) whatever the cell count.

LIMITATIONS: see the module-level string LIMITATIONS.
"""

import bisect
import math
from collections.abc import Mapping

import numpy as np


LIMITATIONS = """
L1. Operator API is the ACTUAL owned_parent_operator_v001.py API (sha256 27ad1762...),
    unchanged in owned_parent_operator_v002.py (sha256 b5fded4d...): energy_weights tuples
    aligned with context.energy_cells, the diagonal value is the "diag" record amplitude,
    primitive_channels also returns the "diag" records (skipped here), read_rows returns
    {labels, values, presence} arrays with state-independent labels. The palette move calls
    the ACTUAL operator v002 enumeration palette_channels(*, context, state, palette_owners)
    (FINAL_CHECK R1; operator v001 has none, so with v001 a non-None palette_parameters
    fails closed at input admission). Mismatches fail closed.
L2. Positive gauge, verified on TWO lines. (a) Model level, before any state is visited:
    _model_member_check reads the caller's model mapping against the contract s3/s10
    coefficient schema (exactly the 13 diagonal scalars Delta, Ud, dstar, epsilon_c,
    epsilon_r, lambda_R, lambda_J, E_R, E_S, E_I, e_R, e_I, C_identity plus the profiles
    h, t, theta, g, kappa, epsilon) and checks EVERY supplied entry, whether or not any
    chain ever enumerates it: h_e > 0, t_e > 0 and theta_e == 0 exactly for every edge key
    (newborn/child edges included), g_v > 0, kappa_v != 0 with |kappa_v - |kappa_v|
    exp(i admission_phase)| <= gauge_phase*|kappa_v| for every vertex, the same for every
    owner's epsilon_j with birth_phase, and every diagonal scalar a finite real. A Mapping
    profile is checked entry by entry; a bare scalar is a declared uniform value; a
    callable profile is admitted only through its declared uniform attribute `value` (the
    root adapter's UniformEdgeProfile returns exactly that value for every ordered A-B
    pair by its text, so the check trusts that declaration rather than enumerating all
    potential endpoint pairs, which 0408/0409 forbid). Any other form, a missing or
    unknown key, a violation or a non-evaluable entry returns status "unsupported" before
    sampling. A zero kappa or epsilon has no phase and is unsupported (the member has
    nonzero common kappa and Birth amplitude). (b) Second line, unchanged from v001: every
    primitive enumerated at every VISITED state (all alternatives, restricted palette
    enumerations included) must gauge to -|h|. The gauge itself is applied through
    per-kind increments of record parity, Spent number and slot number (contract section
    3) with caller-declared gauge_phases {admission_phase = arg kappa, birth_phase = arg
    epsilon}. Net increments of every regrown segment are compared with the replaced
    segment (and the initial path must close them).
L3. Storage. The SPEC's O(V0 + events) path storage presumes event-delta storage. Through
    target_state objects this module stores one state object and key per dwell segment,
    i.e. O(events * state size) unless the operator's states share structure. An
    operator "apply event delta" API would be needed to reach the SPEC bound. Per-event
    work keeps GLOBAL terms: diagonal_terms, read_rows and the callback reads are full
    O(current vertices / registered labels) evaluations at every new state, in global and
    palette moves alike; no incremental diagonal or dependency cache is implemented.
L4. Absolute free energy F = -log Z/beta is NOT estimated (None): the positive path
    measure gives derivatives only. A normalization (e.g. thermodynamic integration in
    beta) is not implemented. No global energy scalar is subtracted from D.
L5. Coordinates are affine: lapse n_alpha (identical derivative to N_alpha), read source
    j_label, lambda, whitened pair sources (L20), fixed mode directions (L21). W_ab = D_ab =
    0 exactly. Nonlinear coordinates (e.g. g00 with N = sqrt(1 + 2 n_g)) follow by the
    caller's chain rule d_vv log Z = J^T H J +
    sum_a d_a log Z d_vv u_a using the returned first AND second derivatives. Read-frame,
    registration, preparation and map derivative contacts are NOT included (reads fixed).
L6. Zero-rate source-opening directions (an available primitive with W = 0 but W_a != 0)
    are detected only at visited states; such a direction is dropped from all outputs and
    listed as unsupported. With N_alpha > 0 and nonnegative partition weights it cannot
    occur; it is reachable only with weights that make 1 + sum n wbar = 0. A lapse mode
    direction (L21) is such a direction when sum_alpha phi_alpha wbar_alphaX != 0 at a
    primitive with multiplier 0; source directions have W_a = 0 and never are.
L7. Conserved-resource component. All chains must start in ONE declared component; the
    module cannot verify membership without enumeration. Explicitly weighted unions of
    superselection components are not combined here (caller weights separate runs).
L8. Coarse moments (0408/0409). Operator rows of kind coarse_first_R / coarse_second_S
    are unsupported in EVERY role (source coefficient, volume term, derivative coordinate,
    tracked read): status "unsupported". The reason is the 0409 rule "avoid
    allocating or duplicating unsupported raw moment sources": the corrected moments have
    ONE source of truth here, the root adapter callback, so no second moment row is
    allocated beside it. For operator v001 (sha256 27ad1762...) those rows are moreover
    built with one global port frame, which cannot represent the registered B = -A frames.
    Operator v002 (sha256 b5fded4d...) builds them with the registered per-part frames
    (B = -A under the 0408 registration) and registration['whitening'] folded in; they
    would still duplicate the callback's moments and pair-source allocation and stay
    refused. Whitened, configuration-normalized
    (current present count) coarse R', S' come only from the root adapter callback
    (adapted_moment_reads), as labels ("whitened_R", cell, i) and ("whitened_S", cell, i,
    j) with i <= j (S' is symmetric; the lower triangle is not duplicated). The adapter's
    raw (unwhitened) moments and its duplicate presence/Z/pair values are never allocated
    as reads or sources. Whitened labels enter H_c ONLY through pair_source_hamiltonian
    with the callback's j_R, j_S (generic ("source", label) coefficients or coordinates on
    them are unsupported duplicates); they may be tracked and used in A. The module never
    forms C = M - mu mu^T (caller: adapter central_covariance on ensemble means) and never
    inverts covariance-only response. Read-read susceptibilities come from making the
    reads source coordinates (d2logZ); no separate read-read path covariance is returned.
L9. A ("fixed diagonal volume gradient") is interpreted literally as an explicit linear
    combination of diagonal reads (operator rows and/or whitened callback reads) with caller
    coefficients and multiplier lambda. A(m) self-consistency (SPEC section 5) is not
    solved; implicit_closure must be None (status unsupported otherwise).
L10. Interval selection density (SPEC ambiguity): start time uniform on [0, beta); with
    probability whole_circle_probability the whole circle anchored at that time; else a
    length beta*U*f with U uniform on [0,1) and f drawn from caller-weighted components
    (at least one f = 1 so every length below beta has positive density). Rotation is a
    separate move with caller probability. All are source independent and symmetric. The
    same interval density is used by the global and the palette moves; the move type is
    chosen with state-independent probabilities p_rot, p_palette, 1 - p_rot - p_palette.
L11. H[N] weighting is the literal source functional H + sum n_alpha E_alpha, i.e.
    multiplier 1 + sum n_alpha wbar_alpha; it equals sum N_alpha wbar_alpha when the
    weights partition, which is checked to the caller's weight_partition tolerance at
    every enumerated nonzero primitive and diagonal term.
L12. Reverse pairing check (no omitted reverse): at every sampled event x->y the summed
    rate of reverse-kind primitives y->x must equal the summed forward rate of the same
    kind x->y (relative reverse_rate tolerance). Candidates are first filtered by equal
    changed_support; if none matches, all reverse-kind channels are keyed (expensive,
    counted in diagnostics). Hermiticity elsewhere is the operator's responsibility.
L13. Errors are statistical/assessed (batch jackknife, between-chain spread, Sokal
    integrated autocorrelation, Gelman-Rubin R-hat) against caller thresholds; they are
    NOT a mixing-time bound. If mixing is failed or unassessable (including fewer than two
    chains) no error band, replicate set or covariance is returned. Columns constant in
    every sample of every chain are listed; their zero spread is a sample statistic only.
    Mixing is judged on the primary linear columns (S, T, read averages, event count),
    not separately on products.
L14. Caps (events per path, total events, sweeps, channel enumerations) end the whole
    computation with status incomplete and partial diagnostics; no estimate is returned
    and no path is ever rejected because of a cap. Restricted, lazy and verification
    enumerations count as channel enumerations; replayed held marks count as events.
L15. An exact floating-point coincidence of event times (zero holding time, rotation
    origin or interval end equal to an event time, or rounding to beta) ends the
    computation as failed rather than perturbing times.
L16. Not implemented: SPEC section 5 (HP implicit closure, cosmic preparation, initial
    phase-kick observables), directed-worm or other efficiency moves, translation
    averaging, EH/vacuum matching, c_star, physical normalization and any numerical or
    physical input choice.
L17. Operator exceptions are converted to status failed; the module's own programming
    errors are not caught.
L18. Measurement is taken once after every measurement sweep; consecutive measurements
    are correlated and handled only by the error analysis above.
L19. Blocked palette move (PALETTE, additive). A palette S (frozenset of original owner
    labels) is drawn from the caller's weighted list and the interval by L10, both state
    independent. Old events in the interval are held when their permanent groups (module
    docstring classification) miss S; times and descriptors are kept. The held descriptor
    is (kind, owner_id); it must identify at most one positive-rate record at any state
    (more than one -> failed). Between held marks only member channels run, with their
    actual rates and total r_S; a held mark is replayed through palette_channels
    on its own groups and the proposal is rejected when the record is absent (guard,
    newborn/donor image or eligibility failure) or has zero rate; the replayed event gets
    the same reverse-pairing and self-loop checks as a sampled one. Endpoint mismatch
    rejects. Acceptance is min(1, exp{int_I new(r_S - D) - int_I old(r_S - D) + sum_held
    log(W(new pre-event)/W(old pre-event))}); endpoint rejection is never renormalized as a
    conditioned bridge. Records returned by palette_channels that are not members
    by this classification are dropped (counted in diagnostics); COMPLETENESS (no omitted
    member primitive) is the operator's contract, cross-checked against
    primitive_channels at every restricted enumeration only when
    verify_against_full_enumeration is True (costly). No dependency cache is implemented
    (none may omit affected events or globally normalized reads). No fast-mixing claim:
    blocked moves alone are not claimed irreducible, so global regrowth keeps probability
    1 - p_rot - p_palette > 0.
L20. Pair sources (root adapter, companion equations). ("pair_source_R", cell, i)
    differentiates j_R'[cell][i] (D_a = -R'_i); ("pair_source_S", cell, i, j), i <= j,
    differentiates the symmetric pair J_S'[i][j] = J_S'[j][i] jointly with declared
    multiplicity 1 (i == j) or 2 (i < j) (D_a = -mult * S'_ij), preserving the Frobenius
    contraction. Fixed whitening is the caller's/registration's: reads are whitened by the
    adapter; dual sources are taken as given (source_frame "whitened") or converted ONCE by
    the adapter's raw_to_whitened_sources (source_frame "raw"); derivatives are always in
    the whitened dual frame (raw-frame derivatives by the caller's chain rule, never a
    second whitening). The adapter value and the module's linear reconstruction must agree
    within source_consistency_tolerance at every state, else failed. The callback binding
    must hold the SAME graph0 and registration objects as the operator call.
L21. Mode directions (0410 section 1; MODE SPEC s1-s2). derivative_coordinates may also
    hold mappings {"id", "kind": "lapse_direction", "profile_id", "cell_weights"} or {"id",
    "kind": "source_direction", "profile_id", "cell_weights", "label_weights"}; their
    coordinate key is (kind, id) and ids are unique. cell_weights phi: finite reals over
    EVERY cell of context.energy_cells (explicit zeros), signed, not all zero. They are
    derivative directions around the caller's positive base lapse and sources, NOT an energy
    partition: no sign, sum or partition admission is applied to them (the operator's own
    energy_weights keep the V002 partition check, L11). Lapse direction: N_alpha =
    N_alpha(base) + eta phi_alpha; per primitive v_X = sum_alpha phi_alpha w_alphaX with the
    operator's energy_weights, i.e. exactly the allocations of H[N] (endpoint-averaged
    (w(y) + w(x))/2 on transitions, w(x) on diagonal owners); D_a = sum_diag d_X v_X and
    rho_a = v_X / multiplier. Source direction: label_weights {field: c_f} over the nine
    whitened callback fields ("whitened_R", i) and ("whitened_S", i, j), i <= j in 0..2,
    not all zero; D_a = -sum_alpha phi_alpha sum_f c_f O_alpha,f with O_alpha,f the
    UNNORMALIZED whitened element R'_i or S'_ij of the SAME adapter evaluation that enters
    H_c, and W_a = 0. No multiplicity is added: c_f on an off-diagonal S field is the
    caller's chart factor (e.g. sqrt(2) for a Mandel component); c_f equals mult times the
    coefficient of ("pair_source_S", cell, i, j) (L20). A source direction is a fixed
    combination of the L20 pair coordinates, so it allocates and duplicates no source: base
    sources remain the callback j_R'/J_S'. Source directions need the callback, whose cells
    must equal context.energy_cells. Projection is applied per primitive and per state
    BEFORE any sample is stored; no per-cell column, full cell Hessian or cells-times-fields
    block is ever formed. Directions sharing a profile_id must carry identical cell_weights.
    A general fixed matrix P combining declared directions into further columns is NOT a
    separate input: all coordinates are affine, so P^T g, P^T H P and the same linear map of
    the returned jackknife replicates are exact post hoc (caller).
L22. Mode metadata and pairing. The pairing is the unit discrete cell pairing over
    context.energy_cells (weight 1 per cell); an unequal-weight cell pairing is NOT
    implemented (it would need the weighted dual pairing throughout). Per profile the
    result gives S = sum phi^2, sum phi and c1 = sum phi / S (metadata only), and the Gram
    G_mn = sum_alpha phi_m phi_n over all declared profiles with its largest normalized
    offdiagonal |G_mn| / sqrt(G_mm G_nn). Orthonormality is the caller's declaration (0410):
    it is reported, never thresholded (no tolerance is chosen here). Outputs are EXTENSIVE
    (derivatives of F_total = -log Z / beta in eta); no score, covariance, contact or
    estimate is divided by S or by any mode norm. Normalized F_mode, Gram duals, the
    Legendre transform, the J Jacobian, background contacts and the metric/EH pairing (MODE
    SPEC s2-s5) belong to the root metric adapter and are not computed here. The joint block
    is returned whole: no phase averaging, isotropy, cosine/sine decoupling or
    symmetrization between profiles is applied. Whether the declared directions form an
    invariant block of the complete static source Hessian (MODE SPEC s3, s5) is NOT tested
    here; the caller must declare every coupled column. Uniform-block lapse/metric tadpoles
    and constraints need separate uniform-profile directions or runs.
L23. Uniform first/pair moments. When mode directions are present and the callback is
    given, nine extra tracked columns ("uniform_whitened_R", i) and ("uniform_whitened_S",
    i, j), i <= j, hold the per-state cell SUMS sum_alpha R'_alpha,i and sum_alpha
    S'_alpha,ij over the callback cells, from the same evaluation that enters H_c. They are
    tracked separately from the mode columns; their means, responses and errors follow the
    tracked-read rules. No division by the cell count, no Mandel factor and no central
    covariance C = M - mu mu^T is applied (root: mu = sum / n_cells, M likewise). Without
    the callback they are absent (result modes "uniform_moments" is None). These two label
    kinds are reserved: a caller tracked label or an operator read label of either kind
    fails.
"""


class _Stop(Exception):
    """Internal fail-closed termination carrying status, stage and message."""

    def __init__(self, status, stage, message):
        Exception.__init__(self, message)
        self.status = status
        self.stage = stage
        self.message = message


# ----------------------------------------------------------------------------------
# Scalar and record admission helpers
# ----------------------------------------------------------------------------------


def _is_real_scalar(value):
    if isinstance(value, (bool, np.bool_)):
        return False
    return isinstance(value, (int, float, np.integer, np.floating))


def _real_value(value):
    """Finite float from an admitted real scalar, else None."""
    if not _is_real_scalar(value):
        return None
    try:
        out = float(value)
    except (OverflowError, ValueError, TypeError):
        return None
    if not math.isfinite(out):
        return None
    return out


def _complex_value(value):
    """Finite complex from an admitted real or complex scalar, else None."""
    if isinstance(value, (bool, np.bool_)):
        return None
    admitted = (int, float, complex, np.integer, np.floating, np.complexfloating)
    if not isinstance(value, admitted):
        return None
    try:
        out = complex(value)
    except (OverflowError, ValueError, TypeError):
        return None
    if not (math.isfinite(out.real) and math.isfinite(out.imag)):
        return None
    return out


def _hashable(value):
    try:
        hash(value)
    except TypeError:
        return False
    return True


def _field(record, name):
    """(present, value) of field `name` of an operator record (mapping key or attribute)."""
    if isinstance(record, Mapping):
        if name in record:
            return True, record[name]
        return False, None
    if hasattr(record, name):
        return True, getattr(record, name)
    return False, None


def _admit_real(name, value, failures):
    out = _real_value(value)
    if out is None:
        failures.append(
            f"input {name}: {type(value).__name__} is not an admitted finite real scalar"
        )
    return out


def _admit_int(name, value, minimum, failures):
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, np.integer)):
        failures.append(f"input {name}: {type(value).__name__} is not an integer")
        return None
    out = int(value)
    if out < minimum:
        failures.append(f"input {name}: {out} is below the minimum {minimum}")
        return None
    return out


def _admit_mapping(name, value, failures):
    if not isinstance(value, Mapping):
        failures.append(f"input {name}: {type(value).__name__} is not a mapping")
        return None
    return value


def _admit_required_keys(name, mapping, keys, failures):
    """True if `mapping` has exactly the required keys."""
    missing = [k for k in keys if k not in mapping]
    extra = [k for k in mapping if k not in keys]
    if missing:
        failures.append(f"input {name}: missing keys {missing!r}")
    if extra:
        failures.append(f"input {name}: unknown keys {extra!r}")
    return not missing and not extra


def _admit_operator_api(operator_api, need_restricted, failures):
    names = [
        "validate_owned_model",
        "canonical_state_key",
        "primitive_channels",
        "diagonal_terms",
        "read_rows",
    ]
    if need_restricted:
        names.append("palette_channels")  # actual operator v002 name (FINAL_CHECK R1)
    api = {}
    for nm in names:
        present, fn = _field(operator_api, nm)
        if not present or not callable(fn):
            failures.append(
                f"input operator_api: callable {nm!r} is missing (operator API in docstring)"
            )
        else:
            api[nm] = fn
    return api if len(api) == len(names) else None


def _model_schema():
    """Contract s3/s10 coefficient schema (diagonal scalars, transition profiles)."""
    scalars = ("Delta", "Ud", "dstar", "epsilon_c", "epsilon_r", "lambda_R", "lambda_J",
               "E_R", "E_S", "E_I", "e_R", "e_I", "C_identity")
    profiles = ("h", "t", "theta", "g", "kappa", "epsilon")
    return scalars, profiles


def _unsupported_raw_kinds():
    """Operator coarse moment rows refused in every role (0409: no duplicated moment source).

    Operator v001 builds them with one global port frame (cannot represent B = -A); operator
    v002 builds them with per-part B = -A frames plus the registration whitening, but they
    would duplicate the root adapter callback's moments and pair-source allocation (L8).
    """
    return ("coarse_first_R", "coarse_second_S")


def _whitened_kinds():
    """Read-label kinds supplied by the root adapter callback (whitened R', S')."""
    return ("whitened_R", "whitened_S")


def _uniform_kinds():
    """Reserved kinds of the v003 uniform (cell-summed) whitened moment columns (L23)."""
    return ("uniform_whitened_R", "uniform_whitened_S")


def _mode_fields():
    """The nine whitened callback fields a source direction may weight (L21), fixed order."""
    fields = [("whitened_R", i) for i in range(3)]
    fields += [("whitened_S", i, j) for i in range(3) for j in range(i, 3)]
    return tuple(fields)


def _uniform_labels():
    """Uniform first/pair moment column labels (L23), in _mode_fields order."""
    return tuple(("uniform_" + f[0],) + f[1:] for f in _mode_fields())


def _label_kind(label):
    if isinstance(label, tuple) and label and isinstance(label[0], str):
        return label[0]
    return None


def _component(value):
    return (not isinstance(value, (bool, np.bool_)) and isinstance(value, (int, np.integer))
            and 0 <= int(value) <= 2)


def _whitened_label_ok(label, cells):
    kind = _label_kind(label)
    if kind == "whitened_R":
        return len(label) == 3 and label[1] in cells and _component(label[2])
    if kind == "whitened_S":
        return (len(label) == 4 and label[1] in cells and _component(label[2])
                and _component(label[3]) and int(label[2]) <= int(label[3]))
    return False


def _admit_pair_sources(j_r, j_s, where, failures):
    """({cell: [3 reals]}, {cell: symmetric [[3 reals] x 3]}) or None (whitened or raw)."""
    if not isinstance(j_r, Mapping) or not isinstance(j_s, Mapping):
        failures.append(f"{where}: j_R and j_S must be mappings cell -> 3-vector / 3x3 matrix")
        return None
    if not j_r or set(j_r) != set(j_s):
        failures.append(f"{where}: j_R and j_S must be nonempty with the same cells")
        return None
    out_r = {}
    out_s = {}
    seq = (list, tuple, np.ndarray)
    for cell in j_r:
        vec = j_r[cell]
        mat = j_s[cell]
        vals = None
        if isinstance(vec, seq) and len(vec) == 3:
            vals = [_real_value(x) for x in vec]
        rows = None
        if isinstance(mat, seq) and len(mat) == 3 and all(
            isinstance(row, seq) and len(row) == 3 for row in mat
        ):
            rows = [[_real_value(x) for x in row] for row in mat]
        if vals is None or None in vals:
            failures.append(f"{where}: j_R[{cell!r}] is not a 3-vector of finite reals")
            continue
        if rows is None or any(None in row for row in rows):
            failures.append(f"{where}: j_S[{cell!r}] is not a 3x3 matrix of finite reals")
            continue
        if any(rows[i][j] != rows[j][i] for i in range(3) for j in range(3)):
            failures.append(
                f"{where}: j_S[{cell!r}] is not exactly symmetric (Frobenius contraction of a "
                "symmetric source; multiplicities are never hidden)"
            )
            continue
        out_r[cell] = vals
        out_s[cell] = rows
    if len(out_r) != len(j_r):
        return None
    return out_r, out_s


def _admit_pair_callback(value, graph0, registration, failures):
    """Root adapter read/source callback (0408/0409) or None."""
    if value is None:
        return None
    keys = ("adapter", "operator_module", "binding", "source_frame", "j_R", "j_S",
            "source_consistency_tolerance")
    name = "diagonal_read_source_callback"
    mp = _admit_mapping(name, value, failures)
    if mp is None or not _admit_required_keys(name, mp, keys, failures):
        return None
    frame = mp["source_frame"]
    if not (isinstance(frame, str) and frame in ("whitened", "raw")):
        failures.append(f"input {name}['source_frame']: must be 'whitened' or 'raw'")
        return None
    fn_names = ["adapted_moment_reads", "pair_source_hamiltonian"]
    if frame == "raw":
        fn_names.append("raw_to_whitened_sources")
    fns = {}
    for nm in fn_names:
        present, fn = _field(mp["adapter"], nm)
        if not present or not callable(fn):
            failures.append(f"input {name}['adapter']: callable {nm!r} is missing")
        else:
            fns[nm] = fn
    if not callable(getattr(mp["operator_module"], "state_labels", None)):
        failures.append(
            f"input {name}['operator_module']: the adapter calls operator_module.state_labels; "
            "an object with that callable attribute is required"
        )
    binding = mp["binding"]
    if not isinstance(binding, Mapping) or "graph0" not in binding or "registration" not in binding:
        failures.append(f"input {name}['binding']: a mapping with 'graph0' and 'registration'")
    elif binding["graph0"] is not graph0 or binding["registration"] is not registration:
        failures.append(
            f"input {name}['binding']: binding['graph0'] and binding['registration'] must be the "
            "SAME objects passed as graph0 and registration (one source of truth for ports, "
            "cells and presence)"
        )
    tol = _admit_real(f"{name}['source_consistency_tolerance']",
                      mp["source_consistency_tolerance"], failures)
    if tol is not None and not tol >= 0.0:
        failures.append(f"input {name}['source_consistency_tolerance']: must be >= 0")
        tol = None
    pair = _admit_pair_sources(mp["j_R"], mp["j_S"], f"input {name}", failures)
    if len(fns) != len(fn_names) or tol is None or pair is None:
        return None
    return {
        "fns": fns,
        "operator_module": mp["operator_module"],
        "binding": binding,
        "source_frame": frame,
        "j_R": pair[0],
        "j_S": pair[1],
        "tol": tol,
    }


def _admit_palette_parameters(value, failures):
    """Additive blocked-palette move parameters (PALETTE) or None (move disabled)."""
    if value is None:
        return None
    name = "palette_parameters"
    keys = ("selection_probability", "palettes", "verify_against_full_enumeration")
    mp = _admit_mapping(name, value, failures)
    if mp is None or not _admit_required_keys(name, mp, keys, failures):
        return None
    p_sel = _admit_real(f"{name}['selection_probability']", mp["selection_probability"], failures)
    if p_sel is not None and not 0.0 < p_sel < 1.0:
        failures.append(f"input {name}['selection_probability']: must lie in (0, 1)")
        p_sel = None
    verify = mp["verify_against_full_enumeration"]
    if not isinstance(verify, (bool, np.bool_)):
        failures.append(f"input {name}['verify_against_full_enumeration']: must be a bool")
        verify = None
    raw = mp["palettes"]
    pals = []
    if not isinstance(raw, (list, tuple)) or not raw:
        failures.append(f"input {name}['palettes']: nonempty list of (weight, owner labels)")
    else:
        for i, item in enumerate(raw):
            if not isinstance(item, (list, tuple)) or len(item) != 2:
                failures.append(f"input {name}['palettes'][{i}]: not a (weight, owners) pair")
                continue
            w = _real_value(item[0])
            owners = item[1]
            ok = isinstance(owners, (list, tuple, set, frozenset)) and len(owners) > 0 and all(
                _hashable(o) for o in owners
            )
            if w is None or not w > 0.0 or not ok:
                failures.append(
                    f"input {name}['palettes'][{i}]: need weight > 0 and a nonempty collection "
                    "of hashable original owner labels"
                )
                continue
            pals.append((w, frozenset(owners)))
    if p_sel is None or verify is None or not pals or len(pals) != len(raw):
        return None
    total = math.fsum(w for w, _ in pals)
    cumulative = []
    acc = []
    for w, s in pals:
        acc.append(w)
        cumulative.append((math.fsum(acc) / total, s))
    return {
        "selection_probability": p_sel,
        "palettes": pals,
        "cumulative": cumulative,
        "verify": bool(verify),
    }


def _admit_label_roles(sources, vgrad, tracked, coords, pair_cells, failures, unsupported):
    """0408/0409: no unsupported raw coarse rows, no duplicated whitened source allocation."""
    roles = [("source_coefficients", lbl) for lbl in sources]
    roles += [("volume_gradient_coefficients", lbl) for lbl in vgrad]
    roles += [("tracked_read_labels", lbl) for lbl in tracked]
    roles += [("derivative_coordinates", c[1]) for c in coords if c[0] == "source"]
    for role, lbl in roles:
        kind = _label_kind(lbl)
        if kind in _unsupported_raw_kinds():
            unsupported.append(
                f"input {role}: {lbl!r} is an operator coarse moment row; per 0409 no unsupported "
                "raw moment source is allocated or duplicated: corrected moments enter only "
                "through diagonal_read_source_callback (operator v001 rows use one global port "
                "frame; operator v002 rows use per-part B = -A frames plus whitening and would "
                "duplicate the callback moments) (L8)"
            )
        elif kind in _whitened_kinds():
            if role in ("source_coefficients", "derivative_coordinates"):
                unsupported.append(
                    f"input {role}: {lbl!r} would duplicate the pair-source allocation; "
                    "whitened moments are sourced only through the callback j_R/j_S and "
                    "('pair_source_R'|'pair_source_S', ...) coordinates (L8, L20)"
                )
            elif pair_cells is None:
                failures.append(
                    f"input {role}: {lbl!r} needs diagonal_read_source_callback (whitened reads)"
                )
            elif not _whitened_label_ok(lbl, pair_cells):
                failures.append(
                    f"input {role}: {lbl!r} is not ('whitened_R', cell, i) or "
                    "('whitened_S', cell, i, j) with i <= j in 0..2 and a callback cell"
                )


def _admit_lapse_factors(value, failures):
    mp = _admit_mapping("lapse_factors", value, failures)
    if mp is None:
        return None
    if len(mp) == 0:
        failures.append("input lapse_factors: at least one coarse cell is required")
        return None
    out = {}
    for cell, raw in mp.items():
        n = _real_value(raw)
        if n is None or not n > 0.0:
            failures.append(
                f"input lapse_factors[{cell!r}]: must be a finite real > 0 (N_alpha), got {raw!r}"
            )
            continue
        out[cell] = n
    return out


def _admit_label_reals(name, value, failures):
    mp = _admit_mapping(name, value, failures)
    if mp is None:
        return None
    out = {}
    for label, raw in mp.items():
        v = _real_value(raw)
        if v is None:
            failures.append(f"input {name}[{label!r}]: not a finite real, got {raw!r}")
            continue
        out[label] = v
    return out


def _admit_gauge_phases(value, failures):
    mp = _admit_mapping("gauge_phases", value, failures)
    if mp is None:
        return None
    if not _admit_required_keys("gauge_phases", mp, ("admission_phase", "birth_phase"), failures):
        return None
    phi_a = _admit_real("gauge_phases['admission_phase']", mp["admission_phase"], failures)
    phi_b = _admit_real("gauge_phases['birth_phase']", mp["birth_phase"], failures)
    if phi_a is None or phi_b is None:
        return None
    return {"admission_phase": phi_a, "birth_phase": phi_b}


def _mode_field(field):
    """Normalized whitened callback field ("whitened_R", i) / ("whitened_S", i, j), i <= j."""
    if not isinstance(field, tuple) or not field or field[0] not in _whitened_kinds():
        return None
    n_idx = 1 if field[0] == "whitened_R" else 2
    if len(field) != 1 + n_idx or not all(_component(x) for x in field[1:]):
        return None
    if n_idx == 2 and int(field[1]) > int(field[2]):
        return None
    return (field[0],) + tuple(int(x) for x in field[1:])


def _admit_mode_direction(i, spec, pair_cells, failures):
    """(key, direction) of one v003 fixed affine mode direction (L21), or None.

    Signed cell weights are derivative directions around the positive base lapse and
    sources, NOT an energy partition: only finiteness and a nonzero profile are required.
    """
    name = f"derivative_coordinates[{i}]"
    where = f"input {name}"
    kind = spec["kind"] if "kind" in spec else None
    if isinstance(kind, str) and kind == "lapse_direction":
        keys = ("id", "kind", "profile_id", "cell_weights")
    elif isinstance(kind, str) and kind == "source_direction":
        keys = ("id", "kind", "profile_id", "cell_weights", "label_weights")
    else:
        failures.append(
            f"{where}: a mode direction mapping needs kind 'lapse_direction' or "
            "'source_direction' (L21)"
        )
        return None
    if not _admit_required_keys(name, spec, keys, failures):
        return None
    good = True
    if not _hashable(spec["id"]) or not _hashable(spec["profile_id"]):
        failures.append(f"{where}: 'id' and 'profile_id' must be hashable")
        good = False
    raw = spec["cell_weights"]
    phi = {}
    if not isinstance(raw, Mapping) or not raw:
        failures.append(f"{where}: 'cell_weights' must be a nonempty mapping cell -> finite real")
        good = False
    else:
        for cell, val in raw.items():
            v = _real_value(val)
            if v is None:
                failures.append(
                    f"{where}: cell_weights[{cell!r}] = {val!r} is not a finite real (signed "
                    "derivative weights are admitted; no partition admission)"
                )
                good = False
                continue
            phi[cell] = v
        if good and all(v == 0.0 for v in phi.values()):
            failures.append(f"{where}: cell_weights are identically zero (S = 0)")
            good = False
    fields = None
    if kind == "source_direction":
        if pair_cells is None:
            failures.append(
                f"{where}: a source_direction weights the whitened callback moments; "
                "diagonal_read_source_callback is required (L21)"
            )
            good = False
        lw = spec["label_weights"]
        if not isinstance(lw, Mapping) or not lw:
            failures.append(f"{where}: 'label_weights' must be a nonempty mapping field -> real")
            good = False
        else:
            order = _mode_fields()
            fields = []
            for field, coef in lw.items():
                norm = _mode_field(field)
                c = _real_value(coef)
                if norm is None or c is None:
                    failures.append(
                        f"{where}: label_weights[{field!r}] needs a field ('whitened_R', i) or "
                        "('whitened_S', i, j), i <= j in 0..2, with a finite real coefficient"
                    )
                    good = False
                    continue
                fields.append((norm, c))
            fields.sort(key=lambda fc: order.index(fc[0]))
            if good and all(c == 0.0 for _, c in fields):
                failures.append(f"{where}: label_weights are identically zero")
                good = False
    if not good:
        return None
    direction = {
        "id": spec["id"],
        "kind": kind,
        "profile_id": spec["profile_id"],
        "phi": phi,
        "fields": None if fields is None else tuple(fields),
    }
    return (kind, spec["id"]), direction


def _admit_coordinates(value, lapse, pair_cells, failures, modes):
    """Coordinate keys in caller order; v003 mode directions are also recorded in `modes`."""
    if not isinstance(value, (list, tuple)):
        failures.append("input derivative_coordinates: must be a list or tuple of tuples")
        return None
    out = []
    ids = set()
    for i, coord in enumerate(value):
        if isinstance(coord, Mapping):
            got = _admit_mode_direction(i, coord, pair_cells, failures)
            if got is None:
                continue
            key, direction = got
            if direction["id"] in ids:
                failures.append(
                    f"input derivative_coordinates[{i}]: duplicate mode direction id "
                    f"{direction['id']!r}"
                )
                continue
            ids.add(direction["id"])
            modes[key] = direction
            out.append(key)
            continue
        if not isinstance(coord, tuple) or not coord or not _hashable(coord):
            failures.append(
                f"input derivative_coordinates[{i}]: {coord!r} is not a nonempty hashable tuple"
            )
            continue
        tag = coord[0]
        if tag == "lapse" and len(coord) == 2:
            if lapse is not None and coord[1] not in lapse:
                failures.append(
                    f"input derivative_coordinates[{i}]: lapse cell {coord[1]!r} has no lapse factor"
                )
                continue
        elif tag == "source" and len(coord) == 2:
            pass
        elif tag == "volume_multiplier" and len(coord) == 1:
            pass
        elif tag in ("pair_source_R", "pair_source_S"):
            n_idx = 1 if tag == "pair_source_R" else 2
            ok = (
                pair_cells is not None
                and len(coord) == 2 + n_idx
                and coord[1] in pair_cells
                and all(_component(x) for x in coord[2:])
                and (n_idx == 1 or int(coord[2]) <= int(coord[3]))
            )
            if not ok:
                failures.append(
                    f"input derivative_coordinates[{i}]: {coord!r} is not ('pair_source_R', "
                    "cell, i) or ('pair_source_S', cell, i, j), i <= j in 0..2, with cell a "
                    "diagonal_read_source_callback cell (callback required)"
                )
                continue
        else:
            failures.append(
                f"input derivative_coordinates[{i}]: {coord!r} is not ('lapse', cell), "
                "('source', label), ('volume_multiplier',), ('pair_source_R', cell, i), "
                "('pair_source_S', cell, i, j) or a mode direction mapping (L21)"
            )
            continue
        if coord in out:
            failures.append(f"input derivative_coordinates[{i}]: duplicate {coord!r}")
            continue
        out.append(coord)
    profiles = {}
    for key, direction in modes.items():
        pid = direction["profile_id"]
        if pid not in profiles:
            profiles[pid] = direction["phi"]
        elif profiles[pid] != direction["phi"]:
            failures.append(
                f"input derivative_coordinates: mode direction {key!r} reuses profile_id "
                f"{pid!r} with different cell_weights (one fixed profile per id; L21)"
            )
    return out


def _admit_labels(name, value, failures):
    if not isinstance(value, (list, tuple)):
        failures.append(f"input {name}: must be a list or tuple of hashable labels")
        return None
    out = []
    seen = set()
    for i, label in enumerate(value):
        if not _hashable(label):
            failures.append(f"input {name}[{i}]: label is not hashable")
            continue
        if label in seen:
            failures.append(f"input {name}[{i}]: duplicate label {label!r}")
            continue
        seen.add(label)
        out.append(label)
    return out


def _admit_generators(value, failures):
    if not isinstance(value, (list, tuple)) or not value:
        failures.append("input chain_generators: a nonempty list of numpy Generators is required")
        return None
    ids = set()
    for i, gen in enumerate(value):
        if not isinstance(gen, np.random.Generator):
            failures.append(
                f"input chain_generators[{i}]: {type(gen).__name__} is not numpy.random.Generator"
            )
            return None
        if id(gen) in ids:
            failures.append(
                f"input chain_generators[{i}]: the same Generator object is reused; "
                "independent chains need distinct Generators"
            )
            return None
        ids.add(id(gen))
    return list(value)


def _admit_initial_paths(value, kinds, failures):
    if not isinstance(value, (list, tuple)) or not value:
        failures.append("input initial_paths: a nonempty list (one entry per chain) is required")
        return None
    out = []
    for c, spec in enumerate(value):
        if not isinstance(spec, Mapping) or "x0" not in spec or "events" not in spec:
            failures.append(f"input initial_paths[{c}]: must be a mapping with 'x0' and 'events'")
            continue
        events = spec["events"]
        if not isinstance(events, (list, tuple)):
            failures.append(f"input initial_paths[{c}]['events']: must be a list (may be empty)")
            continue
        parsed = []
        good = True
        for i, ev in enumerate(events):
            if not isinstance(ev, Mapping) or not all(
                k in ev for k in ("tau", "kind", "owner_id", "target_key")
            ):
                failures.append(
                    f"input initial_paths[{c}]['events'][{i}]: needs tau, kind, owner_id, target_key"
                )
                good = False
                continue
            tau = _real_value(ev["tau"])
            if tau is None:
                failures.append(f"input initial_paths[{c}]['events'][{i}]: tau not finite real")
                good = False
                continue
            if not _hashable(ev["kind"]) or ev["kind"] not in kinds:
                failures.append(
                    f"input initial_paths[{c}]['events'][{i}]: unknown kind {ev['kind']!r}"
                )
                good = False
                continue
            parsed.append((tau, ev["kind"], ev["owner_id"], ev["target_key"]))
        if good:
            out.append({"x0": spec["x0"], "events": parsed})
    return out if len(out) == len(value) else None


def _admit_move_parameters(value, failures):
    keys = (
        "moves_per_sweep",
        "rotation_probability",
        "whole_circle_probability",
        "length_components",
    )
    mp = _admit_mapping("move_parameters", value, failures)
    if mp is None or not _admit_required_keys("move_parameters", mp, keys, failures):
        return None
    moves = _admit_int("move_parameters['moves_per_sweep']", mp["moves_per_sweep"], 1, failures)
    p_rot = _admit_real("move_parameters['rotation_probability']", mp["rotation_probability"], failures)
    p_whole = _admit_real(
        "move_parameters['whole_circle_probability']", mp["whole_circle_probability"], failures
    )
    if p_rot is not None and not 0.0 < p_rot < 1.0:
        failures.append("input move_parameters['rotation_probability']: must lie in (0, 1)")
        p_rot = None
    if p_whole is not None and not 0.0 < p_whole < 1.0:
        failures.append("input move_parameters['whole_circle_probability']: must lie in (0, 1)")
        p_whole = None
    comps_raw = mp["length_components"]
    comps = []
    if not isinstance(comps_raw, (list, tuple)) or not comps_raw:
        failures.append(
            "input move_parameters['length_components']: nonempty list of (weight, upper_fraction)"
        )
    else:
        for i, comp in enumerate(comps_raw):
            if not isinstance(comp, (list, tuple)) or len(comp) != 2:
                failures.append(f"input length_components[{i}]: not a (weight, upper_fraction) pair")
                continue
            w = _real_value(comp[0])
            f = _real_value(comp[1])
            if w is None or not w > 0.0 or f is None or not 0.0 < f <= 1.0:
                failures.append(
                    f"input length_components[{i}]: need weight > 0 and 0 < upper_fraction <= 1"
                )
                continue
            comps.append((w, f))
        if comps and not any(f == 1.0 for _, f in comps):
            failures.append(
                "input length_components: at least one component must have upper_fraction 1 so "
                "that every interval length below beta has positive selection density"
            )
            comps = []
    if moves is None or p_rot is None or p_whole is None or not comps:
        return None
    total = math.fsum(w for w, _ in comps)
    cumulative = []
    acc = []
    for w, f in comps:
        acc.append(w)
        cumulative.append((math.fsum(acc) / total, f))
    return {
        "moves_per_sweep": moves,
        "rotation_probability": p_rot,
        "whole_circle_probability": p_whole,
        "length_components": comps,
        "cumulative_components": cumulative,
    }


def _admit_caps(value, failures):
    keys = (
        "max_events_per_path",
        "max_total_events",
        "max_sweeps",
        "max_channel_enumerations",
    )
    mp = _admit_mapping("caps", value, failures)
    if mp is None or not _admit_required_keys("caps", mp, keys, failures):
        return None
    out = {}
    for k in keys:
        v = _admit_int(f"caps['{k}']", mp[k], 1, failures)
        if v is None:
            return None
        out[k] = v
    return out


def _admit_error_parameters(value, n_measure, failures):
    keys = (
        "batches_per_chain",
        "sokal_window_constant",
        "rhat_max",
        "min_batch_length_over_tau",
        "max_explicit_covariance_dimension",
    )
    mp = _admit_mapping("error_parameters", value, failures)
    if mp is None or not _admit_required_keys("error_parameters", mp, keys, failures):
        return None
    batches = _admit_int("error_parameters['batches_per_chain']", mp["batches_per_chain"], 2, failures)
    c_win = _admit_real("error_parameters['sokal_window_constant']", mp["sokal_window_constant"], failures)
    rhat_max = _admit_real("error_parameters['rhat_max']", mp["rhat_max"], failures)
    ratio = _admit_real(
        "error_parameters['min_batch_length_over_tau']", mp["min_batch_length_over_tau"], failures
    )
    max_dim = _admit_int(
        "error_parameters['max_explicit_covariance_dimension']",
        mp["max_explicit_covariance_dimension"],
        0,
        failures,
    )
    if c_win is not None and not c_win > 0.0:
        failures.append("input error_parameters['sokal_window_constant']: must be > 0")
        c_win = None
    if rhat_max is not None and not rhat_max >= 1.0:
        failures.append("input error_parameters['rhat_max']: must be >= 1")
        rhat_max = None
    if ratio is not None and not ratio > 0.0:
        failures.append("input error_parameters['min_batch_length_over_tau']: must be > 0")
        ratio = None
    if batches is not None and n_measure is not None and n_measure % batches != 0:
        failures.append(
            f"input error_parameters['batches_per_chain']={batches} must divide "
            f"measurement_sweeps={n_measure} (no samples are dropped)"
        )
        batches = None
    if None in (batches, c_win, rhat_max, ratio, max_dim):
        return None
    return {
        "batches_per_chain": batches,
        "sokal_window_constant": c_win,
        "rhat_max": rhat_max,
        "min_batch_length_over_tau": ratio,
        "max_explicit_covariance_dimension": max_dim,
    }


def _admit_tolerances(value, failures):
    keys = ("gauge_phase", "weight_partition", "reverse_rate")
    mp = _admit_mapping("numerical_tolerances", value, failures)
    if mp is None or not _admit_required_keys("numerical_tolerances", mp, keys, failures):
        return None
    out = {}
    for k in keys:
        v = _admit_real(f"numerical_tolerances['{k}']", mp[k], failures)
        if v is None or not v >= 0.0:
            failures.append(f"input numerical_tolerances['{k}']: must be a finite real >= 0")
            return None
        out[k] = v
    return out


# ----------------------------------------------------------------------------------
# Gauge (SPEC section 1; assembly lines 300-327)
# ----------------------------------------------------------------------------------


def _kind_table():
    """kind -> (record-parity change mod 2, Spent-number change, slot-number change, reverse)."""
    return {
        "flip": (0, 0, 0, "flip"),
        "hop": (0, 0, 0, "hop"),
        "bind": (1, 0, 0, "bind"),
        "admit": (0, 1, 0, "admit_rev"),
        "admit_rev": (0, -1, 0, "admit"),
        "birth": (0, 0, 1, "birth_rev"),
        "birth_rev": (0, 0, -1, "birth"),
    }


def _gauge_table(kinds, phases):
    """kind -> conj(G(y)) G(x) for G = (-1)^{sum q} s_a^{N_S} s_b^{N}, |s_a| = |s_b| = 1.

    s_a = -exp(i admission_phase), s_b = -exp(i birth_phase); a change +1 of N_S (or N)
    contributes conj(s), a change -1 contributes s, a record-bit flip contributes -1.
    """
    s_a = -complex(math.cos(phases["admission_phase"]), math.sin(phases["admission_phase"]))
    s_b = -complex(math.cos(phases["birth_phase"]), math.sin(phases["birth_phase"]))
    table = {}
    for kind, (dq, dns, dn, _) in kinds.items():
        f = complex(1.0, 0.0)
        if dq % 2 == 1:
            f = -f
        if dns == 1:
            f = f * s_a.conjugate()
        elif dns == -1:
            f = f * s_a
        if dn == 1:
            f = f * s_b.conjugate()
        elif dn == -1:
            f = f * s_b
        table[kind] = f
    return table


def _profile_entries(name, prof):
    """(form, [(where, value), ...]) for every supplied entry of a model profile.

    A Mapping is read entry by entry; a bare scalar is a declared uniform value; a callable
    is admitted only through its declared uniform attribute `value` (root adapter
    UniformEdgeProfile). Anything else cannot be evaluated: (None, reason).
    """
    if isinstance(prof, Mapping):
        return "mapping", [(f"model['{name}'][{k!r}]", v) for k, v in prof.items()]
    if _complex_value(prof) is not None:
        return "uniform_scalar", [(f"model['{name}']", prof)]
    if callable(prof):
        present, val = _field(prof, "value")
        if present:
            return "uniform_accessor_value", [(f"model['{name}'].value", val)]
        return None, (
            f"model['{name}'] is a callable without a declared uniform 'value'; its entries "
            "cannot be checked without enumerating every potential endpoint pair"
        )
    return None, (
        f"model['{name}'] has type {type(prof).__name__}, not a mapping or a declared uniform"
    )


def _model_member_check(model, phases, tol_g):
    """Model-level common-phase zero-holonomy member check (SPEC s1; L2a), state independent.

    Returns (ok, problems, forms). Every supplied coefficient of the caller's model mapping
    is checked against the contract s3/s10 schema; nothing depends on visited states.
    """
    problems = []
    forms = {}
    count = [0]

    def bad(msg):
        count[0] += 1
        if len(problems) < 20:
            problems.append(msg)

    scalars, profiles = _model_schema()
    if not isinstance(model, Mapping):
        return False, ["model is not a mapping; membership cannot be evaluated"], forms
    expected = set(scalars) | set(profiles)
    missing = [k for k in scalars + profiles if k not in model]
    unknown = [k for k in model if k not in expected]
    if missing or unknown:
        return False, [
            f"model keys differ from the contract s3/s10 coefficient schema (missing "
            f"{missing!r}, unknown {unknown!r}); membership cannot be evaluated"
        ], forms
    for k in scalars:
        if _real_value(model[k]) is None:
            bad(f"model['{k}'] = {model[k]!r} is not a finite real scalar (real diagonal profile)")
    unit = {
        "kappa": complex(math.cos(phases["admission_phase"]), math.sin(phases["admission_phase"])),
        "epsilon": complex(math.cos(phases["birth_phase"]), math.sin(phases["birth_phase"])),
    }
    for name in profiles:
        form, entries = _profile_entries(name, model[name])
        if form is None:
            bad(entries + "; membership cannot be evaluated")
            continue
        forms[name] = form
        for where, raw in entries:
            if name in ("h", "t", "g"):
                v = _real_value(raw)
                if v is None or not v > 0.0:
                    bad(f"{where} = {raw!r}: must be a finite real > 0 (member: real h, t, g > 0)")
            elif name == "theta":
                v = _real_value(raw)
                if v is None or v != 0.0:
                    bad(f"{where} = {raw!r}: hopping phase must be exactly 0 (zero holonomy)")
            else:
                z = _complex_value(raw)
                if z is None or z == 0:
                    bad(f"{where} = {raw!r}: a nonzero finite scalar is required (phase defined)")
                elif not abs(z - abs(z) * unit[name]) <= tol_g * abs(z):
                    which = "admission_phase" if name == "kappa" else "birth_phase"
                    bad(
                        f"{where} = {raw!r}: its phase differs from gauge_phases['{which}'] "
                        "beyond the gauge_phase tolerance (no common phase)"
                    )
    if count[0] > len(problems):
        problems.append(f"... {count[0] - len(problems)} further member violations not listed")
    return count[0] == 0, problems, forms


# ----------------------------------------------------------------------------------
# Operator access (state level; no basis)
# ----------------------------------------------------------------------------------


def _op(run, name, **kwargs):
    """Call an operator API function; any exception is a failed computation."""
    fn = run["api"][name]
    try:
        return fn(**kwargs)
    except _Stop:
        raise
    except Exception as exc:  # fail closed on operator errors (L17)
        raise _Stop(
            "failed", run["stage"], f"operator {name} raised {type(exc).__name__}: {exc}"
        )


def _state_key(run, state):
    return _op(run, "canonical_state_key", context=run["context"], state=state)


def _keys_equal(run, a, b):
    try:
        eq = a == b
    except Exception as exc:
        raise _Stop("failed", run["stage"], f"canonical keys not comparable: {exc}")
    if isinstance(eq, (bool, np.bool_)):
        return bool(eq)
    raise _Stop(
        "failed",
        run["stage"],
        f"canonical key comparison returned {type(eq).__name__}, not a single bool",
    )


def _energy_weights(run, raw, where):
    """{cell: w} (nonzero entries) from an energy_weights tuple aligned with context.energy_cells."""
    cells = run["energy_cells"]
    try:
        arr = np.asarray(raw)
    except Exception as exc:
        raise _Stop("failed", run["stage"], f"{where}: energy_weights not an array ({exc})")
    if arr.ndim != 1 or arr.shape[0] != len(cells) or arr.dtype.kind not in "iuf":
        raise _Stop(
            "failed",
            run["stage"],
            f"{where}: energy_weights is not a real sequence aligned with context.energy_cells",
        )
    arr = arr.astype(np.float64)
    if not bool(np.all(np.isfinite(arr))):
        raise _Stop("failed", run["stage"], f"{where}: energy_weights not finite")
    return {cells[int(i)]: float(arr[i]) for i in np.flatnonzero(arr)}


def _lapse_multiplier(run, weights, where):
    """1 + sum_alpha n_alpha w_alpha after checking the V002 partition sum_alpha w_alpha = 1."""
    total = math.fsum(weights.values())
    if not abs(total - 1.0) <= run["tol"]["weight_partition"]:
        raise _Stop(
            "failed",
            run["stage"],
            f"{where}: support weights sum to {total!r}, not 1 within weight_partition "
            "tolerance (V002 partition; a no-anchor term needs an explicit assignment)",
        )
    n_of = run["n_of_cell"]
    mult = math.fsum([1.0] + [n_of[c] * w for c, w in weights.items()])
    if not math.isfinite(mult):
        raise _Stop("failed", run["stage"], f"{where}: lapse multiplier not finite")
    return mult


def _projected_weight(phi, weights):
    """v_X = sum_alpha phi_alpha w_alphaX of one primitive (L21), from its nonzero weights."""
    return math.fsum([phi[cell] * w for cell, w in weights.items()])


def _signature(changed):
    try:
        sig = frozenset(changed)
    except TypeError:
        return None
    return sig


def _enumeration_tick(run):
    counters = run["counters"]
    if counters["channel_enumerations"] >= run["caps"]["max_channel_enumerations"]:
        raise _Stop(
            "incomplete",
            run["stage"],
            "cap max_channel_enumerations reached; computation ended (no path was rejected)",
        )
    counters["channel_enumerations"] += 1


def _channels_at(run, state):
    """Nonnegative per-primitive rates at `state` (SPEC sections 1-2), before aggregation."""
    _enumeration_tick(run)
    records = _op(run, "primitive_channels", context=run["context"], state=state)
    return _channels_from_records(run, records, "primitive_channels")


def _channels_from_records(run, records, source):
    """Gauge check (L2b), lapse weighting and rates of operator records; 'diag' skipped."""
    if not isinstance(records, (list, tuple)):
        raise _Stop("failed", run["stage"], f"{source} did not return a list")
    kinds = run["kinds"]
    tol_g = run["tol"]["gauge_phase"]
    channels = []
    for i, rec in enumerate(records):
        where = f"{source} record {i}"
        present_k, kind = _field(rec, "kind")
        if not present_k:
            raise _Stop("failed", run["stage"], f"{where}: field 'kind' missing")
        if isinstance(kind, str) and kind == "diag":
            continue  # diagonal owner: read through diagonal_terms (actual operator API)
        fields = {}
        for nm in ("owner_id", "target_state", "amplitude", "changed_support", "energy_weights"):
            present, val = _field(rec, nm)
            if not present:
                raise _Stop("failed", run["stage"], f"{where}: field {nm!r} missing")
            fields[nm] = val
        if not _hashable(kind) or kind not in kinds:
            raise _Stop("failed", run["stage"], f"{where}: unknown kind {kind!r}")
        amp = _complex_value(fields["amplitude"])
        if amp is None:
            raise _Stop("failed", run["stage"], f"{where}: amplitude not a finite complex scalar")
        if amp == 0:
            continue  # exactly zero matrix element: no jump mark, W = W_a = 0
        mag = abs(amp)
        gauged = amp * run["gauge"][kind]
        if not abs(gauged + mag) <= tol_g * mag:
            raise _Stop(
                "unsupported",
                run["stage"],
                f"{where}: kind {kind!r} owner {fields['owner_id']!r}: gauged element "
                f"{gauged!r} is not real nonpositive (-|h| = {-mag!r}) within the "
                "gauge_phase tolerance: outside the proven common-phase zero-holonomy member "
                "(nonzero holonomy, non-common phase, complex flip/Bind) or gauge_phases do not "
                "equal the model's common arg kappa / arg epsilon",
            )
        weights = _energy_weights(run, fields["energy_weights"], where)
        mult = _lapse_multiplier(run, weights, where)
        if mult < 0.0:
            raise _Stop(
                "unsupported",
                run["stage"],
                f"{where}: lapse multiplier 1 + sum n wbar = {mult!r} < 0 makes the gauged "
                "offdiagonal rate negative; positivity requires positive support lapse",
            )
        if mult == 0.0:
            for cell, w in weights.items():
                if w != 0.0 and cell in run["lapse_index"]:
                    run["zero_rate_directions"].add(("lapse", cell))
            for idx, phi in run["lapse_dirs"]:
                if _projected_weight(phi, weights) != 0.0:
                    run["zero_rate_directions"].add(run["coords"][idx])  # L6, L21
            continue
        rate = mag * mult
        if not (math.isfinite(rate) and rate > 0.0):
            raise _Stop("failed", run["stage"], f"{where}: rate {rate!r} not finite positive")
        channels.append(
            {
                "kind": kind,
                "owner": fields["owner_id"],
                "target": fields["target_state"],
                "W": rate,
                "mult": mult,
                "weights": weights,
                "sig": _signature(fields["changed_support"]),
                "key": None,
                "has_key": False,
            }
        )
    exit_rate = math.fsum(ch["W"] for ch in channels)
    if not math.isfinite(exit_rate):
        raise _Stop("failed", run["stage"], "exit rate r(x) not finite")
    return channels, exit_rate


def _record_groups(run, kind, owner_id):
    """Permanent original-owner groups of a primitive (PALETTE; module docstring), from labels."""
    group = run["group"]
    labels = None
    try:
        if kind in ("birth", "birth_rev"):
            if owner_id[0] == "birth":
                labels = (owner_id[1],)
        elif kind in ("flip", "hop"):
            tag, pair = owner_id[1]
            if tag == "edge" and len(pair) == 2:
                labels = (pair[0], pair[1])
        elif kind in ("bind", "admit", "admit_rev"):
            tag, vertex = owner_id[1]
            if tag == "vertex":
                labels = (vertex,)
        if labels is not None:
            return frozenset(group[lab] for lab in labels)
    except (TypeError, KeyError, IndexError, ValueError):
        pass
    raise _Stop(
        "failed",
        run["stage"],
        f"primitive kind {kind!r} owner_id {owner_id!r} cannot be classified into permanent "
        "original-owner groups (palette membership must come from permanent labels)",
    )


def _record_identity(run, rec, where):
    """Hashable (kind, owner_id, target_state, amplitude, energy_weights) of one record."""
    vals = []
    for nm in ("kind", "owner_id", "target_state", "amplitude", "energy_weights"):
        present, val = _field(rec, nm)
        if not present:
            raise _Stop("failed", run["stage"], f"{where}: field {nm!r} missing")
        vals.append(val)
    try:
        ident = (vals[0], vals[1], vals[2], complex(vals[3]),
                 tuple(float(x) for x in vals[4]))
        hash(ident)
    except Exception as exc:
        raise _Stop("failed", run["stage"], f"{where}: record identity not hashable ({exc})")
    return ident


def _palette_members(run, records, owners, source):
    """Non-diag records whose permanent groups meet `owners` (others dropped and counted)."""
    if not isinstance(records, (list, tuple)):
        raise _Stop("failed", run["stage"], f"{source} did not return a list")
    out = []
    dropped = 0
    for i, rec in enumerate(records):
        present_k, kind = _field(rec, "kind")
        present_o, owner_id = _field(rec, "owner_id")
        if not present_k or not present_o:
            raise _Stop("failed", run["stage"], f"{source} record {i}: kind/owner_id missing")
        if isinstance(kind, str) and kind == "diag":
            continue
        if not _hashable(kind) or kind not in run["kinds"]:
            raise _Stop("failed", run["stage"], f"{source} record {i}: unknown kind {kind!r}")
        if _record_groups(run, kind, owner_id).isdisjoint(owners):
            dropped += 1
            continue
        out.append(rec)
    return out, dropped


def _palette_channels(run, state, owners):
    """Member channels and restricted exit rate r_S at `state` (operator v002 palette_channels)."""
    _enumeration_tick(run)
    run["counters"]["restricted_enumerations"] += 1
    records = _op(run, "palette_channels", context=run["context"], state=state,
                  palette_owners=owners)
    members, dropped = _palette_members(run, records, owners, "palette_channels")
    run["counters"]["restricted_nonmember_records_dropped"] += dropped
    if run["palette"]["verify"]:
        _enumeration_tick(run)
        run["counters"]["palette_verifications"] += 1
        full = _op(run, "primitive_channels", context=run["context"], state=state)
        expected, _ = _palette_members(run, full, owners, "primitive_channels")
        want = {}
        for i, rec in enumerate(expected):
            ident = _record_identity(run, rec, f"primitive_channels record {i}")
            want[ident] = want.get(ident, 0) + 1
        got = {}
        for i, rec in enumerate(members):
            ident = _record_identity(run, rec, f"palette_channels record {i}")
            got[ident] = got.get(ident, 0) + 1
        if want != got:
            raise _Stop(
                "failed",
                run["stage"],
                "palette_channels differs from the palette members of "
                "primitive_channels at a visited state (omitted, extra or altered member "
                "records; verify_against_full_enumeration)",
            )
    return _channels_from_records(run, members, "palette_channels")


def _diagonal_at(run, state):
    """Diagonal H[N] energy, its lapse derivatives and (v003) lapse-direction projections.

    Lapse directions (L21): sum_diag d_X v_X with v_X = sum_alpha phi_alpha w_alphaX, formed
    per record from its own weights (no per-cell column is stored).
    """
    records = _op(run, "diagonal_terms", context=run["context"], state=state)
    if not isinstance(records, (list, tuple)):
        raise _Stop("failed", run["stage"], "diagonal_terms did not return a list")
    tol_g = run["tol"]["gauge_phase"]
    h_terms = []
    lapse_terms = {cell: [] for cell in run["lapse_index"]}
    dir_terms = {idx: [] for idx, _ in run["lapse_dirs"]}
    for i, rec in enumerate(records):
        where = f"diagonal_terms record {i}"
        present_k, kind = _field(rec, "kind")
        if present_k and not (isinstance(kind, str) and kind == "diag"):
            raise _Stop("failed", run["stage"], f"{where}: kind {kind!r} is not 'diag'")
        present_v, raw = _field(rec, "amplitude")
        present_w, wraw = _field(rec, "energy_weights")
        if not present_v or not present_w:
            raise _Stop(
                "failed", run["stage"], f"{where}: fields 'amplitude' and 'energy_weights' required"
            )
        z = _complex_value(raw)
        if z is None:
            raise _Stop("failed", run["stage"], f"{where}: value not a finite scalar")
        if not abs(z.imag) <= tol_g * abs(z.real):
            raise _Stop(
                "unsupported",
                run["stage"],
                f"{where}: diagonal value {z!r} is not real; outside the declared member",
            )
        value = z.real
        if value == 0.0:
            continue
        weights = _energy_weights(run, wraw, where)
        mult = _lapse_multiplier(run, weights, where)
        h_terms.append(value * mult)
        for cell, w in weights.items():
            if cell in lapse_terms:
                lapse_terms[cell].append(value * w)
        for idx, phi in run["lapse_dirs"]:
            dir_terms[idx].append(value * _projected_weight(phi, weights))
    return (math.fsum(h_terms), {c: math.fsum(v) for c, v in lapse_terms.items()},
            {idx: math.fsum(v) for idx, v in dir_terms.items()})


def _index_read_labels(run, labels):
    """Once per run: index the operator's state-independent read labels."""
    try:
        lab_t = tuple(labels)
    except TypeError:
        raise _Stop("failed", run["stage"], "read_rows['labels'] is not a sequence")
    index = {}
    for i, lbl in enumerate(lab_t):
        if not _hashable(lbl):
            raise _Stop("failed", run["stage"], f"read_rows label {i} is not hashable")
        if _label_kind(lbl) in _whitened_kinds():
            raise _Stop(
                "failed", run["stage"], f"operator read label {lbl!r} collides with callback labels"
            )
        if run["uniform_labels"] and _label_kind(lbl) in _uniform_kinds():
            raise _Stop(
                "failed", run["stage"],
                f"operator read label {lbl!r} collides with the reserved uniform moment "
                "labels (L23)",
            )
        if lbl in index:
            raise _Stop("failed", run["stage"], f"read_rows: duplicate label {lbl!r}")
        index[lbl] = i
    missing = [lbl for lbl in run["needed_operator_labels"] if lbl not in index]
    if missing:
        raise _Stop(
            "failed",
            run["stage"],
            f"referenced read labels {missing[:20]!r} are not operator read_rows labels (labels "
            "are state independent; an absent object has value 0 and presence 0, not a "
            "missing label)",
        )
    run["read_index"] = {lbl: index[lbl] for lbl in run["needed_operator_labels"]}
    run["read_labels_ref"] = labels
    run["read_labels_tuple"] = lab_t


def _read_array(run, rows, name):
    arr = rows[name]
    n = len(run["read_labels_tuple"])
    if type(arr) is not np.ndarray or arr.ndim != 1 or arr.shape[0] != n or arr.dtype.kind != "f":
        raise _Stop("failed", run["stage"], f"read_rows['{name}'] is not a float array [{n}]")
    if not bool(np.all(np.isfinite(arr))):
        raise _Stop("failed", run["stage"], f"read_rows['{name}'] not finite")
    return arr


def _whitened_moments(run, reads):
    """Validated whitened R'[cell] (3) and S'[cell] (3x3, exactly symmetric) of the callback."""
    if not isinstance(reads, Mapping) or any(k not in reads for k in ("cells", "R", "S")):
        raise _Stop("failed", run["stage"], "adapted_moment_reads did not return cells, R and S")
    try:
        cells = tuple(reads["cells"])
    except TypeError:
        raise _Stop("failed", run["stage"], "adapted_moment_reads['cells'] is not a sequence")
    pair = run["pair"]
    if pair["cells"] is None:
        if len(set(cells)) != len(cells) or set(cells) != set(pair["j_R"]):
            raise _Stop(
                "failed",
                run["stage"],
                "adapter cells differ from the cells of the callback j_R/j_S sources",
            )
        pair["cells"] = cells
    elif cells != pair["cells"]:
        raise _Stop("failed", run["stage"], "adapter cells changed between states")
    out_r = {}
    out_s = {}
    seq = (list, tuple, np.ndarray)
    try:
        for cell in cells:
            vec = reads["R"][cell]
            mat = reads["S"][cell]
            r = [_real_value(x) for x in vec] if isinstance(vec, seq) and len(vec) == 3 else None
            s = None
            if isinstance(mat, seq) and len(mat) == 3 and all(
                isinstance(row, seq) and len(row) == 3 for row in mat
            ):
                s = [[_real_value(x) for x in row] for row in mat]
            if r is None or None in r or s is None or any(None in row for row in s):
                raise _Stop("failed", run["stage"], f"adapter R/S of cell {cell!r} not finite real")
            if any(s[i][j] != s[j][i] for i in range(3) for j in range(3)):
                raise _Stop("failed", run["stage"], f"adapter S of cell {cell!r} not symmetric")
            out_r[cell] = r
            out_s[cell] = s
    except (KeyError, TypeError) as exc:
        raise _Stop("failed", run["stage"], f"adapter R/S not indexable by cell ({exc})")
    return cells, out_r, out_s


def _reads_at(run, state):
    """Full diagonal reads at `state` (operator rows, callback whitened moments, pair source).

    Returns (values for every referenced label, pair source value P(x), {coordinate index:
    D_a of P}). The SAME evaluation feeds D, every D_a and the tracked time averages.
    """
    rows = _op(run, "read_rows", context=run["context"], state=state)
    if not isinstance(rows, Mapping) or any(k not in rows for k in ("labels", "values", "presence")):
        raise _Stop("failed", run["stage"], "read_rows did not return {labels, values, presence}")
    labels = rows["labels"]
    if run["read_labels_ref"] is None:
        _index_read_labels(run, labels)
    elif labels is not run["read_labels_ref"]:
        try:
            same = tuple(labels) == run["read_labels_tuple"]
        except Exception:
            same = False
        if not same:
            raise _Stop(
                "failed", run["stage"], "read_rows labels changed between states (must be fixed)"
            )
    vals = _read_array(run, rows, "values")
    _read_array(run, rows, "presence")
    values = {lbl: float(vals[i]) for lbl, i in run["read_index"].items()}
    pair = run["pair"]
    pair_value = 0.0
    pair_da = {}
    if pair is not None:
        fns = pair["fns"]
        try:
            reads = fns["adapted_moment_reads"](
                operator_module=pair["operator_module"],
                context=run["context"],
                state=state,
                binding=pair["binding"],
            )
        except Exception as exc:
            raise _Stop(
                "failed", run["stage"], f"adapted_moment_reads raised {type(exc).__name__}: {exc}"
            )
        cells, r_w, s_w = _whitened_moments(run, reads)
        for lbl in run["needed_whitened"]:
            if lbl[0] == "whitened_R":
                values[lbl] = r_w[lbl[1]][int(lbl[2])]
            else:
                values[lbl] = s_w[lbl[1]][int(lbl[2])][int(lbl[3])]
        try:
            raw_p = fns["pair_source_hamiltonian"](reads=reads, j_R=pair["j_R"], j_S=pair["j_S"])
        except Exception as exc:
            raise _Stop(
                "failed",
                run["stage"],
                f"pair_source_hamiltonian raised {type(exc).__name__}: {exc}",
            )
        pv = _real_value(raw_p)
        if pv is None:
            raise _Stop("failed", run["stage"], "pair_source_hamiltonian value not finite real")
        terms = []
        for cell in cells:
            jr = pair["j_R"][cell]
            js = pair["j_S"][cell]
            for i in range(3):
                terms.append(-jr[i] * r_w[cell][i])
                for j in range(3):
                    terms.append(-js[i][j] * s_w[cell][i][j])
        recon = math.fsum(terms)
        scale = math.fsum(abs(x) for x in terms)
        if not abs(pv - recon) <= pair["tol"] * scale:
            raise _Stop(
                "failed",
                run["stage"],
                f"pair_source_hamiltonian {pv!r} differs from -j_R.R' - J_S:S' = {recon!r} beyond "
                "source_consistency_tolerance (H_c and its source derivatives would disagree)",
            )
        pair_value = pv
        for idx, coord in run["pair_coords"]:
            i = int(coord[2])
            if coord[0] == "pair_source_R":
                pair_da[idx] = -r_w[coord[1]][i]
            else:
                j = int(coord[3])
                pair_da[idx] = -(1.0 if i == j else 2.0) * s_w[coord[1]][i][j]
        # v003 source directions (L21): D_a = -sum_alpha phi_alpha sum_f c_f O_alpha,f, the
        # UNNORMALIZED projection of this same evaluation (no division by any mode norm).
        for idx, phi, fields in run["source_dirs"]:
            terms = []
            for cell in cells:
                w = phi[cell]
                if w == 0.0:
                    continue
                for f, c in fields:
                    o = r_w[cell][f[1]] if f[0] == "whitened_R" else s_w[cell][f[1]][f[2]]
                    terms.append(-w * c * o)
            pair_da[idx] = math.fsum(terms)
        # v003 uniform first/pair moments (L23): cell sums, tracked separately.
        for lbl in run["uniform_labels"]:
            if lbl[0] == "uniform_whitened_R":
                values[lbl] = math.fsum([r_w[cell][lbl[1]] for cell in cells])
            else:
                values[lbl] = math.fsum([s_w[cell][lbl[1]][lbl[2]] for cell in cells])
    return values, pair_value, pair_da


def _segment_core(run, state):
    """Dwell-segment record {state, key, D, r (lazy), Da, row} from FULL diagonal reads."""
    key = _state_key(run, state)
    d_h, d_lapse, d_dirs = _diagonal_at(run, state)
    values, pair_value, pair_da = _reads_at(run, state)
    src = math.fsum([-j * values[lbl] for lbl, j in run["sources"].items()])
    vol = math.fsum([a * values[lbl] for lbl, a in run["volume_gradient"].items()])
    diag = math.fsum([d_h, src, pair_value, -run["lam"] * vol])
    if not math.isfinite(diag):
        raise _Stop("failed", run["stage"], "diagonal energy D(x) not finite")
    da = np.zeros(run["n_u"], dtype=np.float64)
    for idx, coord in enumerate(run["coords"]):
        if coord[0] == "lapse":
            da[idx] = d_lapse[coord[1]]
        elif coord[0] == "source":
            da[idx] = -values[coord[1]]
        elif coord[0] == "volume_multiplier":
            da[idx] = -vol
        elif coord[0] == "lapse_direction":
            da[idx] = d_dirs[idx]  # v003 projected lapse direction (L21)
        else:  # pair_source_R / pair_source_S / v003 source_direction (callback reads)
            da[idx] = pair_da[idx]
    row = np.array([values[lbl] for lbl in run["tracked_all"]], dtype=np.float64)
    return {"state": state, "key": key, "D": diag, "r": None, "Da": da, "row": row}


def _segment_at(run, state):
    """Dwell-segment record with its full exit rate, and the state's full channels."""
    seg = _segment_core(run, state)
    channels, exit_rate = _channels_at(run, state)
    seg["r"] = exit_rate
    return seg, channels


def _seg_rate(run, seg):
    """Full exit rate r(x) of a segment, enumerated lazily (palette-created segments)."""
    if seg["r"] is None:
        _, exit_rate = _channels_at(run, seg["state"])
        seg["r"] = exit_rate
    return seg["r"]


def _target_key(run, ch):
    if not ch["has_key"]:
        ch["key"] = _state_key(run, ch["target"])
        ch["has_key"] = True
    return ch["key"]


def _event_from_channel(run, ch):
    """Event record with rho_a = W_a / W (lapse: wbar_alpha / multiplier; others 0).

    v003 lapse directions (L21): rho_a = v_X / multiplier, v_X = sum_alpha phi_alpha
    wbar_alphaX from the transition's own endpoint-averaged weights (projected per event).
    """
    rho = np.zeros(run["n_u"], dtype=np.float64)
    for cell, w in ch["weights"].items():
        idx = run["lapse_index"].get(cell)
        if idx is not None:
            rho[idx] = w / ch["mult"]
    for idx, phi in run["lapse_dirs"]:
        rho[idx] = _projected_weight(phi, ch["weights"]) / ch["mult"]
    dq, dns, dn, _ = run["kinds"][ch["kind"]]
    return {"kind": ch["kind"], "owner": ch["owner"], "W": ch["W"], "rho": rho,
            "dq": dq, "dns": dns, "dn": dn}


def _summed_rate(run, channels, kind, sig, target_key, use_sig):
    terms = []
    for c in channels:
        if c["kind"] != kind:
            continue
        if use_sig and (sig is None or c["sig"] != sig):
            continue
        if _keys_equal(run, _target_key(run, c), target_key):
            terms.append(c["W"])
    return math.fsum(terms)


def _no_self_loop(run, x_seg, y_seg, chosen):
    """An offdiagonal primitive must change the canonical state (diagonal belongs to D)."""
    if _keys_equal(run, x_seg["key"], y_seg["key"]):
        raise _Stop(
            "failed",
            run["stage"],
            f"primitive kind {chosen['kind']!r} owner {chosen['owner']!r} maps a state to "
            "itself; diagonal contributions must come from diagonal_terms",
        )


def _reverse_check(run, x_seg, x_channels, chosen, y_seg, y_channels):
    """Reverse pairing at a sampled event x->y (no omitted reverse; L12)."""
    rev_kind = run["kinds"][chosen["kind"]][3]
    sig = chosen["sig"]
    fwd = rev = 0.0
    if sig is not None:
        fwd = _summed_rate(run, x_channels, chosen["kind"], sig, y_seg["key"], True)
        rev = _summed_rate(run, y_channels, rev_kind, sig, x_seg["key"], True)
    if rev == 0.0:
        fwd = _summed_rate(run, x_channels, chosen["kind"], sig, y_seg["key"], False)
        rev = _summed_rate(run, y_channels, rev_kind, sig, x_seg["key"], False)
        if rev > 0.0:
            run["counters"]["reverse_signature_fallbacks"] += 1
    if rev == 0.0:
        raise _Stop(
            "failed",
            run["stage"],
            f"reverse primitive missing: event kind {chosen['kind']!r} owner "
            f"{chosen['owner']!r} has no {rev_kind!r} primitive back to its source",
        )
    if not abs(fwd - rev) <= run["tol"]["reverse_rate"] * max(fwd, rev):
        raise _Stop(
            "failed",
            run["stage"],
            f"reverse rate mismatch for kind {chosen['kind']!r}: forward {fwd!r} vs "
            f"reverse {rev!r} (H[N] not Hermitian or weights not endpoint-averaged)",
        )


# ----------------------------------------------------------------------------------
# Paths and moves (SPEC sections 2-3)
# ----------------------------------------------------------------------------------


def _check_times(run, times, horizon):
    prev = 0.0
    for t in times:
        if not (t > prev and t < horizon):
            raise _Stop(
                "failed",
                run["stage"],
                "floating-point event-time coincidence or rounding to the circle end; "
                "computation ended rather than perturbing times (L15)",
            )
        prev = t


def _net_increments(events):
    dq = sum(e["dq"] for e in events) % 2
    dns = sum(e["dns"] for e in events)
    dn = sum(e["dn"] for e in events)
    return dq, dns, dn


def _rotate(run, path, origin):
    """Uniform time-origin rotation: the same closed path with new origin `origin`."""
    if origin == 0.0:
        return path
    beta = run["beta"]
    times = path["times"]
    segments = path["segments"]
    events = path["events"]
    s = bisect.bisect_right(times, origin)
    if s > 0 and times[s - 1] == origin:
        raise _Stop("failed", run["stage"], "rotation origin coincides with an event time (L15)")
    new_times = [t - origin for t in times[s:]] + [t - origin + beta for t in times[:s]]
    _check_times(run, new_times, beta)
    return {
        "segments": [segments[s]] + segments[s + 1:] + segments[1:s + 1],
        "events": events[s:] + events[:s],
        "times": new_times,
    }


def _clipped_integral(run, segments, times, horizon, length):
    """int_0^length (r - D) d tau; segment j spans [t_j, t_{j+1}), t_0 = 0, t_{K+1} = horizon."""
    terms = []
    k = len(times)
    for j in range(len(segments)):
        lo = 0.0 if j == 0 else times[j - 1]
        if lo >= length:
            break
        hi = times[j] if j < k else horizon
        if hi > length:
            hi = length
        terms.append((_seg_rate(run, segments[j]) - segments[j]["D"]) * (hi - lo))
    return math.fsum(terms)


def _choose_channel(channels, exit_rate, rng):
    u = float(rng.random()) * exit_rate
    acc = 0.0
    for ch in channels:
        acc += ch["W"]
        if u < acc:
            return ch
    return channels[-1]


def _ctmc_segment(run, start_seg, length, rng, outside_events):
    """Unconditioned reference CTMC (rates W, holding rate r) from start_seg for `length`."""
    channels, exit_rate = _channels_at(run, start_seg["state"])
    if start_seg["r"] is None:
        start_seg["r"] = exit_rate
    segments = [start_seg]
    events = []
    times = []
    current = start_seg
    t = 0.0
    caps = run["caps"]
    counters = run["counters"]
    while exit_rate > 0.0:
        dt = float(rng.exponential(1.0 / exit_rate))
        t_next = t + dt
        if t_next >= length:
            break
        if not t_next > t:
            raise _Stop("failed", run["stage"], "zero holding time in floating point (L15)")
        chosen = _choose_channel(channels, exit_rate, rng)
        if counters["events"] >= caps["max_total_events"]:
            raise _Stop(
                "incomplete",
                run["stage"],
                "cap max_total_events reached; computation ended (no path was rejected)",
            )
        if len(events) + 1 + outside_events > caps["max_events_per_path"]:
            raise _Stop(
                "incomplete",
                run["stage"],
                "cap max_events_per_path reached by a proposal; computation ended "
                "(the proposal was not rejected, so no high-event path is excluded)",
            )
        counters["events"] += 1
        y_seg, y_channels = _segment_at(run, chosen["target"])
        chosen["key"] = y_seg["key"]
        chosen["has_key"] = True
        _no_self_loop(run, current, y_seg, chosen)
        _reverse_check(run, current, channels, chosen, y_seg, y_channels)
        events.append(_event_from_channel(run, chosen))
        times.append(t_next)
        segments.append(y_seg)
        current = y_seg
        channels = y_channels
        exit_rate = y_seg["r"]
        t = t_next
    return segments, events, times


def _select_interval(run, rng, diag, prefix):
    """Source-independent symmetric interval density (L10): (origin, whole, length) or None."""
    beta = run["beta"]
    mp = run["moves"]
    origin = float(rng.random()) * beta
    whole = float(rng.random()) < mp["whole_circle_probability"]
    if whole:
        diag[prefix + "whole_circle_proposals"] += 1
        return origin, True, beta
    u = float(rng.random())
    frac = mp["cumulative_components"][-1][1]
    for cum, f in mp["cumulative_components"]:
        if u < cum:
            frac = f
            break
    length = float(rng.random()) * frac * beta
    diag[prefix + "interval_proposals"] += 1
    if not length > 0.0:
        diag[prefix + "zero_length_intervals"] += 1
        return None
    return origin, False, length


def _move(run, path, rng, diag):
    """Move type by state-independent probabilities: rotation, palette (if enabled), global."""
    u = float(rng.random())
    p_rot = run["moves"]["rotation_probability"]
    if u < p_rot:
        diag["rotations"] += 1
        return _rotate(run, path, float(rng.random()) * run["beta"]), False
    pal = run["palette"]
    if pal is not None and u < p_rot + pal["selection_probability"]:
        return _palette_move(run, path, rng, diag)
    return _interval_move(run, path, rng, diag)


def _interval_move(run, path, rng, diag):
    """Global interval regrowth with endpoint rejection (SPEC section 3; the v001 move)."""
    beta = run["beta"]
    sel = _select_interval(run, rng, diag, "")
    if sel is None:
        return path, False
    origin, whole, length = sel
    rot = _rotate(run, path, origin)
    k = len(rot["times"])
    if whole:
        m = k
    else:
        m = bisect.bisect_left(rot["times"], length)
        if m < k and rot["times"][m] == length:
            raise _Stop("failed", run["stage"], "interval end coincides with an event time (L15)")
    terminal = rot["segments"][m]
    segs, evs, times = _ctmc_segment(run, rot["segments"][0], length, rng, k - m)
    if not _keys_equal(run, segs[-1]["key"], terminal["key"]):
        diag["endpoint_rejections"] += 1
        return path, False
    if _net_increments(evs) != _net_increments(rot["events"][:m]):
        raise _Stop(
            "failed",
            run["stage"],
            "gauge increments of two segments between the same endpoints differ: primitive "
            "kind labels are inconsistent with a state-function gauge (L2)",
        )
    old_int = _clipped_integral(run, rot["segments"], rot["times"], beta, length)
    new_int = _clipped_integral(run, segs, times, length, length)
    log_acc = new_int - old_int
    if not math.isfinite(log_acc):
        raise _Stop("failed", run["stage"], "log acceptance ratio not finite")
    if log_acc < 0.0 and not float(rng.random()) < math.exp(log_acc):
        diag["metropolis_rejections"] += 1
        return path, False
    new_path = {
        "segments": segs + rot["segments"][m + 1:],
        "events": evs + rot["events"][m:],
        "times": times + rot["times"][m:],
    }
    _check_times(run, new_path["times"], beta)
    back = beta - origin
    if not back < beta:
        back = 0.0
    return _rotate(run, new_path, back), True


def _choose_palette(pal, rng):
    u = float(rng.random())
    owners = pal["cumulative"][-1][1]
    for cum, s in pal["cumulative"]:
        if u < cum:
            owners = s
            break
    return owners


def _count_new_event(run, path_events):
    """Event caps for palette proposals (incomplete, never a rejection; L14)."""
    caps = run["caps"]
    counters = run["counters"]
    if counters["events"] >= caps["max_total_events"]:
        raise _Stop(
            "incomplete",
            run["stage"],
            "cap max_total_events reached; computation ended (no path was rejected)",
        )
    if path_events > caps["max_events_per_path"]:
        raise _Stop(
            "incomplete",
            run["stage"],
            "cap max_events_per_path reached by a palette proposal; computation ended "
            "(the proposal was not rejected, so no high-event path is excluded)",
        )
    counters["events"] += 1


def _palette_move(run, path, rng, diag):
    """Additive blocked-palette move (PALETTE; L19).

    Outside-palette marks inside the interval are held (times and (kind, owner_id)
    descriptors); between them only member channels run with their actual rates and total
    r_S; held marks are replayed on the proposed state (absent or zero rate -> reject);
    endpoint mismatch rejects; log ratio int_I new(r_S - D) - int_I old(r_S - D) +
    sum_held log(W_new / W_old). Unconditioned generation plus rejection, never a bridge.
    """
    beta = run["beta"]
    owners = _choose_palette(run["palette"], rng)
    sel = _select_interval(run, rng, diag, "palette_")
    if sel is None:
        return path, False
    origin, whole, length = sel
    diag["palette_proposals"] += 1
    rot = _rotate(run, path, origin)
    k = len(rot["times"])
    if whole:
        m = k
    else:
        m = bisect.bisect_left(rot["times"], length)
        if m < k and rot["times"][m] == length:
            raise _Stop(
                "failed", run["stage"], "palette interval end coincides with an event time (L15)"
            )
    terminal = rot["segments"][m]
    held = []
    for i in range(m):
        ev = rot["events"][i]
        if _record_groups(run, ev["kind"], ev["owner"]).isdisjoint(owners):
            held.append((rot["times"][i], ev))
    outside = k - m
    pending = len(held)
    current = rot["segments"][0]
    channels, r_s = _palette_channels(run, current["state"], owners)
    segs = [current]
    rates = [r_s]
    evs = []
    times = []
    t = 0.0
    log_held = 0.0
    for bound, hev in held + [(length, None)]:
        while r_s > 0.0:
            dt = float(rng.exponential(1.0 / r_s))
            t_next = t + dt
            if t_next >= bound:
                break
            if not t_next > t:
                raise _Stop("failed", run["stage"], "zero holding time in floating point (L15)")
            chosen = _choose_channel(channels, r_s, rng)
            _count_new_event(run, len(evs) + 1 + pending + outside)
            y_seg = _segment_core(run, chosen["target"])
            chosen["key"] = y_seg["key"]
            chosen["has_key"] = True
            _no_self_loop(run, current, y_seg, chosen)
            y_channels, y_rs = _palette_channels(run, y_seg["state"], owners)
            _reverse_check(run, current, channels, chosen, y_seg, y_channels)
            evs.append(_event_from_channel(run, chosen))
            times.append(t_next)
            segs.append(y_seg)
            rates.append(y_rs)
            current, channels, r_s, t = y_seg, y_channels, y_rs, t_next
        if hev is None:
            break
        groups = _record_groups(run, hev["kind"], hev["owner"])
        x_channels, _ = _palette_channels(run, current["state"], groups)
        matches = [
            c for c in x_channels
            if c["kind"] == hev["kind"] and _keys_equal(run, c["owner"], hev["owner"])
        ]
        if len(matches) > 1:
            raise _Stop(
                "failed",
                run["stage"],
                f"held descriptor (kind {hev['kind']!r}, owner {hev['owner']!r}) matches "
                f"{len(matches)} positive-rate records at one state; a held replay must be "
                "deterministic (L19)",
            )
        if not matches:
            diag["palette_held_rejections"] += 1  # illegal held event or zero held rate
            return path, False
        held_ch = matches[0]
        pending -= 1
        _count_new_event(run, len(evs) + 1 + pending + outside)
        y_seg = _segment_core(run, held_ch["target"])
        held_ch["key"] = y_seg["key"]
        held_ch["has_key"] = True
        _no_self_loop(run, current, y_seg, held_ch)
        y_held, _ = _palette_channels(run, y_seg["state"], groups)
        _reverse_check(run, current, x_channels, held_ch, y_seg, y_held)
        log_held += math.log(held_ch["W"]) - math.log(hev["W"])
        evs.append(_event_from_channel(run, held_ch))
        times.append(bound)
        channels, r_s = _palette_channels(run, y_seg["state"], owners)
        segs.append(y_seg)
        rates.append(r_s)
        current, t = y_seg, bound
    if not _keys_equal(run, current["key"], terminal["key"]):
        diag["palette_endpoint_rejections"] += 1
        return path, False
    if _net_increments(evs) != _net_increments(rot["events"][:m]):
        raise _Stop(
            "failed",
            run["stage"],
            "gauge increments of two segments between the same endpoints differ: primitive "
            "kind labels are inconsistent with a state-function gauge (L2)",
        )
    old_terms = []
    for j in range(m + 1):
        lo = 0.0 if j == 0 else rot["times"][j - 1]
        hi = rot["times"][j] if j < m else length
        seg = rot["segments"][j]
        _, r_old = _palette_channels(run, seg["state"], owners)
        old_terms.append((r_old - seg["D"]) * (hi - lo))
    new_terms = []
    for j, seg in enumerate(segs):
        lo = 0.0 if j == 0 else times[j - 1]
        hi = times[j] if j < len(times) else length
        new_terms.append((rates[j] - seg["D"]) * (hi - lo))
    log_acc = math.fsum(new_terms) - math.fsum(old_terms) + log_held
    if not math.isfinite(log_acc):
        raise _Stop("failed", run["stage"], "palette log acceptance ratio not finite")
    if log_acc < 0.0 and not float(rng.random()) < math.exp(log_acc):
        diag["palette_metropolis_rejections"] += 1
        return path, False
    new_path = {
        "segments": segs + rot["segments"][m + 1:],
        "events": evs + rot["events"][m:],
        "times": times + rot["times"][m:],
    }
    _check_times(run, new_path["times"], beta)
    diag["palette_accepted"] += 1
    back = beta - origin
    if not back < beta:
        back = 0.0
    return _rotate(run, new_path, back), True


def _initial_path(run, spec):
    """Admit a caller closed path (x0 plus events) or a constant path (no events)."""
    beta = run["beta"]
    seg0, channels = _segment_at(run, spec["x0"])
    segments = [seg0]
    events = []
    times = []
    current = seg0
    prev = 0.0
    if len(spec["events"]) > run["caps"]["max_events_per_path"]:
        raise _Stop("incomplete", run["stage"], "initial path exceeds max_events_per_path")
    for i, (tau, kind, owner, target_key) in enumerate(spec["events"]):
        if not (tau > prev and tau < beta):
            raise _Stop(
                "failed", run["stage"], f"initial event {i}: tau must increase strictly in (0, beta)"
            )
        matches = [
            c
            for c in channels
            if c["kind"] == kind and _keys_equal(run, c["owner"], owner)
            and _keys_equal(run, _target_key(run, c), target_key)
        ]
        if len(matches) != 1:
            raise _Stop(
                "failed",
                run["stage"],
                f"initial event {i}: {len(matches)} positive-rate primitives match "
                f"(kind {kind!r}, owner {owner!r}, target key); exactly one is required",
            )
        chosen = matches[0]
        y_seg, y_channels = _segment_at(run, chosen["target"])
        _no_self_loop(run, current, y_seg, chosen)
        _reverse_check(run, current, channels, chosen, y_seg, y_channels)
        events.append(_event_from_channel(run, chosen))
        times.append(tau)
        segments.append(y_seg)
        current = y_seg
        channels = y_channels
        prev = tau
    if not _keys_equal(run, segments[-1]["key"], seg0["key"]):
        raise _Stop("failed", run["stage"], "initial path is not closed: x(beta) != x0")
    if _net_increments(events) != (0, 0, 0):
        raise _Stop(
            "failed",
            run["stage"],
            "initial closed path has nonzero net gauge increments (L2)",
        )
    return {"segments": segments, "events": events, "times": times}


# ----------------------------------------------------------------------------------
# Estimators (SPEC section 4)
# ----------------------------------------------------------------------------------


def _measure(run, path):
    """Per-path S_a, T_ab, time-averaged tracked reads and event count."""
    beta = run["beta"]
    n_u = run["n_u"]
    n_r = run["n_r"]
    segments = path["segments"]
    events = path["events"]
    times = path["times"]
    k = len(times)
    bounds = [0.0] + list(times) + [beta]
    dur = np.array([bounds[j + 1] - bounds[j] for j in range(k + 1)], dtype=np.float64)
    da = np.zeros((k + 1, n_u), dtype=np.float64)
    for j, seg in enumerate(segments):
        da[j] = seg["Da"]
    rho = np.zeros((k, n_u), dtype=np.float64)
    for i, ev in enumerate(events):
        rho[i] = ev["rho"]
    score = -np.einsum("l,la->a", dur, da, optimize=False) + rho.sum(axis=0)
    contact = -np.einsum("ka,kb->ab", rho, rho, optimize=False)
    reads = np.zeros((k + 1, n_r), dtype=np.float64)
    for j, seg in enumerate(segments):
        reads[j] = seg["row"]  # the same full read evaluation that entered D and D_a
    read_avg = np.einsum("l,lr->r", dur, reads, optimize=False) / beta
    return score, contact, read_avg, k


def _sums(S, T, R):
    return {
        "n": S.shape[0],
        "S": S.sum(axis=0),
        "SS": np.einsum("ia,ib->ab", S, S, optimize=False),
        "T": T.sum(axis=0),
        "R": R.sum(axis=0),
        "SR": np.einsum("ia,ir->ar", S, R, optimize=False),
    }


def _sums_combine(parts, sign):
    out = {k: parts[0][k] for k in parts[0]}
    for p in parts[1:]:
        for k in out:
            out[k] = out[k] + sign * p[k]
    return out


def _estimate(sm):
    n = float(sm["n"])
    g = sm["S"] / n
    m = sm["R"] / n
    cov = sm["SS"] / n - np.einsum("a,b->ab", g, g, optimize=False)
    tmean = sm["T"] / n
    hess = cov + tmean
    resp = sm["SR"] / n - np.einsum("a,r->ar", g, m, optimize=False)
    return {"g": g, "cov": cov, "T": tmean, "H": hess, "m": m, "resp": resp}


def _layout(est, iu):
    return np.concatenate([est["g"], est["H"][iu], est["m"], est["resp"].ravel()])


def _sokal_tau(series, c_window):
    """Integrated autocorrelation time with Sokal's self-consistent window."""
    x = np.asarray(series, dtype=np.float64)
    n = x.shape[0]
    if n < 2:
        return "unassessable", None, None
    xc = x - x.mean()
    var0 = float(np.einsum("i,i->", xc, xc, optimize=False)) / n
    if var0 == 0.0:
        return "constant", None, None
    f = np.fft.rfft(xc, 2 * n)
    acov = np.fft.irfft(f * np.conj(f), 2 * n)[:n] / n
    rho = acov / acov[0]
    taus = 0.5 + np.cumsum(rho[1:])
    windows = np.arange(1, n, dtype=np.float64)
    hit = np.flatnonzero(windows >= c_window * taus)
    if hit.size == 0:
        return "unassessable", None, None
    tau = float(taus[hit[0]])
    if not tau > 0.0:
        return "unassessable", None, None
    return "assessed", tau, int(hit[0]) + 1


def _rhat(columns):
    """Gelman-Rubin potential scale reduction for one column, columns shape (C, M)."""
    c, m = columns.shape
    if c < 2 or m < 2:
        return "unassessable", None
    means = columns.mean(axis=1)
    within = float(np.mean(columns.var(axis=1, ddof=1)))
    if within == 0.0:
        if float(means.max() - means.min()) == 0.0:
            return "constant", None
        return "failed", math.inf
    between = m * float(means.var(ddof=1))
    var_plus = (m - 1.0) / m * within + between / m
    return "assessed", math.sqrt(var_plus / within)


def _analyze(run, series, errp, n_u):
    """Batch jackknife, between-chain spread, autocorrelation and R-hat (SPEC section 7)."""
    n_r = run["n_r"]
    n_chains = len(series)
    n_meas = series[0]["score"].shape[0]
    n_batch = errp["batches_per_chain"]
    blen = n_meas // n_batch
    iu = np.triu_indices(n_u)
    block_sums = []
    chain_sums = []
    for ser in series:
        S, T, R = ser["score"], ser["contact"], ser["reads"]
        for b in range(n_batch):
            sl = slice(b * blen, (b + 1) * blen)
            block_sums.append(_sums(S[sl], T[sl], R[sl]))
        chain_sums.append(_sums(S, T, R))
    total = _sums_combine(chain_sums, 1.0)
    point = _estimate(total)
    per_chain = [_estimate(cs) for cs in chain_sums]

    # Primary linear columns for mixing: S_a, T_ab (upper), read averages, event count.
    names = (
        [("score", a) for a in range(n_u)]
        + [("contact", (int(i), int(j))) for i, j in zip(iu[0], iu[1])]
        + [("read", lbl) for lbl in run["tracked_all"]]
        + [("events_per_path", None)]
    )
    prim = []
    for ser in series:
        cols = [ser["score"], ser["contact"][:, iu[0], iu[1]], ser["reads"],
                ser["events"].reshape(-1, 1).astype(np.float64)]
        prim.append(np.concatenate(cols, axis=1))
    prim = np.stack(prim, axis=0)  # (C, M, n_cols)
    c_win = errp["sokal_window_constant"]
    ratio_min = errp["min_batch_length_over_tau"]
    column_status = []
    tau_table = np.full((n_chains, len(names)), np.nan)
    rhat_values = np.full(len(names), np.nan)
    constant_columns = []
    for col in range(len(names)):
        r_status, r_val = _rhat(prim[:, :, col])
        if r_val is not None:
            rhat_values[col] = r_val
        if r_status == "constant":
            column_status.append("constant")
            constant_columns.append(names[col])
            continue
        status = "passed"
        if r_status == "unassessable":
            status = "unassessable"
        elif r_status == "failed" or r_val > errp["rhat_max"]:
            status = "failed"
        for c in range(n_chains):
            t_status, tau, _ = _sokal_tau(prim[c, :, col], c_win)
            if t_status == "assessed":
                tau_table[c, col] = tau
                if blen < ratio_min * tau:
                    status = "failed"
            elif status != "failed":
                status = "unassessable"
        column_status.append(status)
    stuck = [i for i, ser in enumerate(series) if ser["accepted_in_measurement"] == 0]
    if stuck or "failed" in column_status:
        mixing = "failed"
    elif n_chains < 2 or "unassessable" in column_status:
        mixing = "unassessable"
    else:
        mixing = "passed"

    per_chain_batch_se = []
    for ser in series:
        lin = np.concatenate([ser["score"], ser["reads"]], axis=1)
        bm = lin.reshape(n_batch, blen, lin.shape[1]).mean(axis=1)
        per_chain_batch_se.append(np.sqrt(bm.var(axis=0, ddof=1) / n_batch))

    mixing_report = {
        "status": mixing,
        "stuck_chains_zero_accepted_regrowths_in_measurement": stuck,
        "primary_columns": names,
        "column_status": column_status,
        "constant_columns": constant_columns,
        "rhat": rhat_values,
        "integrated_autocorrelation_time": tau_table,
        "batch_length": blen,
        "thresholds": {
            "rhat_max": errp["rhat_max"],
            "min_batch_length_over_tau": ratio_min,
            "sokal_window_constant": c_win,
        },
        "per_chain_batch_means_standard_errors_score_then_reads": per_chain_batch_se,
        "note": (
            "statistical/assessed diagnostics, not a mixing-time bound; per-chain batch "
            "errors are within-chain statistics and are not an error band unless status "
            "is 'passed'"
        ),
    }

    errors = None
    if mixing == "passed":
        n_y = n_u + iu[0].shape[0] + n_r + n_u * n_r
        jn = len(block_sums)
        reps = np.zeros((jn, n_y), dtype=np.float64)
        for i, blk in enumerate(block_sums):
            loo = _sums_combine([total, blk], -1.0)
            reps[i] = _layout(_estimate(loo), iu)
        dev = reps - reps.mean(axis=0)
        factor = (jn - 1.0) / jn
        se = np.sqrt(factor * np.einsum("iy,iy->y", dev, dev, optimize=False))
        cov = None
        if n_y <= errp["max_explicit_covariance_dimension"]:
            cov = factor * np.einsum("iy,iz->yz", dev, dev, optimize=False)
        chain_y = np.stack([_layout(e, iu) for e in per_chain], axis=0)
        between_se = np.sqrt(chain_y.var(axis=0, ddof=1) / n_chains)
        errors = {
            "layout": (
                "y = [dlogZ_du (n_u), d2logZ_du2 upper triangle row-major (n_u(n_u+1)/2), "
                "read_means (n_r), read_mean_responses row-major a-major (n_u*n_r)]"
            ),
            "jackknife_blocks": jn,
            "jackknife_standard_errors": se,
            "jackknife_replicates": reps,
            "joint_covariance": cov,
            "joint_covariance_note": (
                "joint covariance = (J-1)/J sum_i (y_i - ybar)(y_i - ybar)^T over the returned "
                "leave-one-batch-out replicates; formed explicitly only when n_y <= "
                "max_explicit_covariance_dimension"
            ),
            "between_chain_standard_errors": between_se,
        }
    return point, per_chain, mixing_report, errors


# ----------------------------------------------------------------------------------
# Mode metadata and extensive outputs (v003; 0410 section 1, MODE SPEC; L21-L23)
# ----------------------------------------------------------------------------------


def _mode_metadata(run, modes, lapse):
    """Profiles (S, sum, c1), unit-pairing Gram, directions and base sources; (meta, problem).

    Called at the binding stage, after every profile is checked to list exactly
    context.energy_cells. Nothing here divides a score or estimate by any mode norm.
    """
    cells = run["energy_cells"]
    pids = []
    phis = {}
    directions = []
    for key in run["coords"]:
        if key not in modes:
            continue
        d = modes[key]
        if d["profile_id"] not in phis:
            pids.append(d["profile_id"])
            phis[d["profile_id"]] = d["phi"]
        directions.append({
            "coordinate": key,
            "id": d["id"],
            "kind": d["kind"],
            "profile_id": d["profile_id"],
            "label_weights": None if d["fields"] is None else [list(fc) for fc in d["fields"]],
        })
    profiles = []
    for pid in pids:
        vals = [phis[pid][c] for c in cells]
        s_norm = math.fsum([v * v for v in vals])
        total = math.fsum(vals)
        if not (math.isfinite(s_norm) and s_norm > 0.0 and math.isfinite(total)):
            return None, f"mode profile {pid!r}: S = sum phi^2 = {s_norm!r} is not finite positive"
        profiles.append({"profile_id": pid, "values": vals, "S": s_norm, "sum_phi": total,
                         "c1": total / s_norm})
    n_p = len(pids)
    gram = np.zeros((n_p, n_p), dtype=np.float64)
    for m in range(n_p):
        for n in range(m, n_p):
            g = math.fsum([phis[pids[m]][c] * phis[pids[n]][c] for c in cells])
            if not math.isfinite(g):
                return None, f"mode profiles {pids[m]!r}, {pids[n]!r}: Gram entry not finite"
            gram[m, n] = g
            gram[n, m] = g
    worst = None
    for m in range(n_p):
        for n in range(m + 1, n_p):
            r = abs(float(gram[m, n])) / math.sqrt(float(gram[m, m]))
            r = r / math.sqrt(float(gram[n, n]))
            worst = r if worst is None or r > worst else worst
    pair = run["pair"]
    base_pair = None
    if pair is not None:
        base_pair = {
            "source_frame_input": pair["source_frame"],
            "j_R_whitened": {c: list(pair["j_R"][c]) for c in pair["j_R"]},
            "j_S_whitened": {c: [list(row) for row in pair["j_S"][c]] for c in pair["j_S"]},
        }
    meta = {
        "pairing": (
            "unit discrete cell pairing over context.energy_cells (weight 1 per cell); "
            "unequal cell weights are not implemented (L22)"
        ),
        "cell_order": list(cells),
        "profiles": profiles,
        "profile_gram_order": list(pids),
        "profile_gram": gram,
        "gram_max_normalized_offdiagonal": worst,
        "orthonormality_note": (
            "orthonormality is the caller's declaration (0410); the actual Gram is reported "
            "and never thresholded; nonorthogonal profiles need the root's Gram/dual pairing"
        ),
        "directions": directions,
        "base": {
            "lapse_factors": {c: lapse[c] for c in cells},
            "source_coefficients": dict(run["sources"]),
            "pair_sources": base_pair,
            "note": "derivatives are taken around these base inputs (eta = 0)",
        },
        "uniform_moments": None if not run["uniform_labels"] else {
            "labels": list(run["uniform_labels"]),
            "n_cells": len(cells),
        },
        "extensive": None,
        "note": (
            "EXTENSIVE derivatives of F_total = -log Z / beta in the eta coordinates of the "
            "declared directions; no division by S or any mode norm inside the sampler; the "
            "full joint block is returned (no phase averaging, isotropy or cosine/sine "
            "decoupling); normalization F_mode = F_total / S, Gram duals, Legendre transform, "
            "J, background contacts and metric/EH pairing belong to the root metric adapter"
        ),
    }
    return meta, None


def _mode_outputs(meta, coord_order, point, tracked_all, beta, errors):
    """Extensive mode block from the joint estimates (selection only; nothing divided by S)."""
    pos = {key: i for i, key in enumerate(coord_order)}
    keys = [d["coordinate"] for d in meta["directions"]]
    kept = [k for k in keys if k in pos]
    sel = np.array([pos[k] for k in kept], dtype=np.int64)
    n_us = len(coord_order)
    g = point["g"][sel]
    hess = point["H"][np.ix_(sel, sel)]

    def tri(p, q):
        a, b = (p, q) if p <= q else (q, p)
        return n_us + a * n_us - (a * (a - 1)) // 2 + (b - a)

    grad_pos = [int(p) for p in sel]
    hess_pos = [[tri(int(p), int(q)) for q in sel] for p in sel]
    source_rows = [i for i, k in enumerate(kept) if k[0] == "source_direction"]
    out = {
        "coordinates": kept,
        "dropped_unsupported": [k for k in keys if k not in pos],
        "positions_in_coordinate_order": grad_pos,
        "dlogZ_deta": g,
        "d2logZ_deta2": hess,
        "score_covariance": point["cov"][np.ix_(sel, sel)],
        "contact_mean": point["T"][np.ix_(sel, sel)],
        "F_total_gradient": -g / beta,
        "F_total_hessian": -hess / beta,
        "projected_read_means_extensive": {
            "coordinates": [kept[i] for i in source_rows],
            "values": np.array([g[i] / beta for i in source_rows], dtype=np.float64),
            "note": (
                "Q_ext = sum_alpha phi_alpha sum_f c_f <O_alpha,f> = <S_a>/beta "
                "(unnormalized; equals -F_total_gradient on these rows)"
            ),
        },
        "error_layout_positions": {"gradient": grad_pos, "hessian": hess_pos},
        "F_total_gradient_standard_errors": None,
        "F_total_hessian_standard_errors": None,
        "errors_note": (
            "joint errors are errors['jackknife_replicates'] / ['joint_covariance'] at the "
            "listed y positions; F_total = -y/beta, so its standard errors are the jackknife "
            "standard errors divided by beta (only when mixing passed)"
        ),
    }
    if errors is not None:
        se = errors["jackknife_standard_errors"]
        out["F_total_gradient_standard_errors"] = se[np.array(grad_pos, dtype=np.int64)] / beta
        out["F_total_hessian_standard_errors"] = (
            np.array([[se[y] for y in row] for row in hess_pos], dtype=np.float64) / beta
        )
    uni = None
    if meta["uniform_moments"] is not None:
        r_idx = np.array([tracked_all.index(lbl) for lbl in meta["uniform_moments"]["labels"]],
                         dtype=np.int64)
        uni = dict(meta["uniform_moments"])
        uni["read_positions"] = [int(r) for r in r_idx]
        uni["error_layout_positions"] = [
            n_us + (n_us * (n_us + 1)) // 2 + int(r) for r in r_idx
        ]
        uni["cell_sum_means"] = point["m"][r_idx]
        uni["mode_responses"] = point["resp"][np.ix_(sel, r_idx)]
        uni["note"] = (
            "cell sums of whitened R'_i and S'_ij (i <= j) per state, time-averaged; no division "
            "by n_cells, no Mandel factor, no central covariance (L23)"
        )
    return out, uni


def _new_result():
    return {
        "ok": False,
        "status": None,
        "stage_reached": None,
        "failures": [],
        "flags": [],
        "inputs": None,
        "coordinate_order": None,
        "direction_status": None,
        "tracked_read_labels": None,
        "read_kinds": None,
        "member_check": None,
        "modes": None,
        "estimates": None,
        "errors": None,
        "mixing": None,
        "diagnostics": None,
        "conventions": {
            "hamiltonian": (
                "H_c = H[N] - sum_a j_a O_a - j_R'.R' - J_S':S' - lambda A, H[N] = H + "
                "sum_alpha n_alpha E_alpha, n = N - 1; per primitive multiplier 1 + sum_alpha "
                "n_alpha wbar_alphaX applied BEFORE aggregation; beta is one global inverse "
                "energy; the pair term is the root adapter's pair_source_hamiltonian"
            ),
            "pair_sources": (
                "R', S' whitened, configuration-normalized (current present count) coarse "
                "moments from adapted_moment_reads; j_R', J_S' whitened duals (caller input, or "
                "converted once by raw_to_whitened_sources); ('pair_source_S', cell, i, j), "
                "i <= j, moves J_S'[i][j] = J_S'[j][i] together: multiplicity 1 (i == j) or 2"
            ),
            "moves": (
                "rotation (p_rot), additive blocked palette (p_palette, PALETTE note) and global "
                "interval regrowth (1 - p_rot - p_palette > 0), all state independent"
            ),
            "positive_gauge": (
                "G = (-1)^{sum q} (-e^{i admission_phase})^{N_S} (-e^{i birth_phase})^{N}; "
                "gauged offdiagonal elements must equal -|h|; W = |h| * multiplier >= 0; the "
                "gauge is diagonal, so D, diagonal reads and read sources are unchanged by it"
            ),
            "free_energy": (
                "F = -log Z / beta (absolute value not estimated); F_a = -<S_a>/beta; "
                "F_ab = -(Cov(S_a,S_b) + <T_ab>)/beta; F_{n_alpha} = <E_alpha>, F_{j} = -<O>"
            ),
            "legendre": (
                "thermal Legendre F + j.Q (Q = <O>) has QQ Hessian +chi^-1; F_jj = -chi_OO^iso, "
                "F_nn = -chi_EE^iso, F_nj = +chi_EO^iso, chi^iso_AB = int_0^beta <dA(tau) dB(0)>; "
                "real-time action signs are not imported"
            ),
            "time": (
                "tau in [0, beta) is imaginary time (inverse energy); Monte Carlo moves and "
                "sweeps are Markov iterations; neither is physical or native real time"
            ),
            "affine_coordinates": (
                "('lapse', cell) differentiates n_alpha (= N_alpha), ('source', label) j_label, "
                "('volume_multiplier',) lambda, ('pair_source_R', cell, i) j_R'[cell][i], "
                "('pair_source_S', cell, i, j) the symmetric pair J_S'[i][j]; second-source "
                "contacts are exactly zero in these coordinates; other coordinates (raw-frame "
                "sources included) by the caller's chain rule"
            ),
            "mode_directions": (
                "v003 (L21-L23): ('lapse_direction', id) differentiates eta in N_alpha = "
                "N_alpha(base) + eta phi_alpha; ('source_direction', id) adds -eta sum_alpha "
                "phi_alpha sum_f c_f O_alpha,f to H_c (whitened callback fields, unnormalized); "
                "projected per primitive before storage; outputs are EXTENSIVE F_total "
                "derivatives with no division by S or any mode norm; unit cell pairing; full "
                "joint block, no phase averaging; normalization, Gram duals, Legendre and "
                "metric pairing are the root metric adapter's"
            ),
        },
        "scope": (
            "Static isothermal native functional of the quasi-static maximum-entropy closure at "
            "fixed beta (canonical re-preparation), on the conserved-resource component of the "
            "initial paths, with Born count fluctuating. Not fixed-preparation retarded response "
            "(e.g. chi_HH^iso = beta Var(H) while retarded chi_HH = 0) and not the complete "
            "metric propagator. No EH/vacuum matching, c_star, scale, normalization, physical "
            "input or fit is supplied or used. Finite-volume and wavelength convergence, "
            "matching and normalization errors are separate and not estimated here."
        ),
        "limitations": LIMITATIONS,
    }


def owned_collective_worldline_static_response(
    *,
    operator_api,
    graph0,
    model,
    registration,
    initial_paths,
    beta,
    lapse_factors,
    source_coefficients,
    volume_gradient_coefficients,
    volume_multiplier,
    gauge_phases,
    derivative_coordinates,
    tracked_read_labels,
    diagonal_read_source_callback,
    chain_generators,
    move_parameters,
    palette_parameters,
    caps,
    burn_in_sweeps,
    measurement_sweeps,
    error_parameters,
    numerical_tolerances,
    implicit_closure,
):
    """Static joint source Hessians of the owned collective by positive worldline sampling.

    Arguments (keyword-only, all required, no defaults; no value is chosen here):
      operator_api: mapping/object with the ACTUAL state-level callables listed in the module
        docstring (validate_owned_model, canonical_state_key, primitive_channels,
        diagonal_terms, read_rows; plus palette_channels when palette_parameters is
        not None), supplied at run time; nothing is imported.
      graph0, model, registration: passed unchanged to validate_owned_model. The model must
        be the common-phase zero-holonomy member (real h, t, g > 0, zero hopping phases,
        uniform admission phase, common Birth phase, real diagonals). Before sampling,
        _model_member_check verifies this on EVERY supplied coefficient of the model
        mapping (every edge key including newborn/child edges, every vertex, every owner),
        independent of which states the chains visit; a violation, an unknown schema key or
        a profile it cannot evaluate returns status "unsupported". Every primitive at every
        visited state is checked again (second line).
      initial_paths: one entry per chain, {"x0": state, "events": [ {tau, kind, owner_id,
        target_key}, ... ]}; an empty event list is the constant path at x0. Events must
        have 0 < tau strictly increasing < beta, match exactly one positive-rate primitive
        and close at x0. All chains must lie in one declared conserved-resource component.
      beta: finite real > 0 (one global inverse energy).
      lapse_factors: {cell: N_alpha > 0} for exactly the cells of context.energy_cells.
      source_coefficients: {operator read label: j_a} (may be empty); H_c gains -sum j_a O_a.
      volume_gradient_coefficients: {read label: a_a} with A = sum a_a O_a (may be empty;
        whitened callback labels allowed).
      volume_multiplier: lambda (finite real); H_c gains -lambda A.
      gauge_phases: {"admission_phase": arg kappa, "birth_phase": arg epsilon} of the
        member's common phases (radians).
      derivative_coordinates: list of ("lapse", cell) | ("source", label) |
        ("volume_multiplier",) | ("pair_source_R", cell, i) | ("pair_source_S", cell, i, j)
        with i <= j (pair coordinates need the callback; L20) | (v003, L21) a fixed affine
        mode direction mapping {"id": hashable (unique), "kind": "lapse_direction",
        "profile_id": hashable, "cell_weights": {cell: finite real phi_alpha} over EVERY
        cell of context.energy_cells, signed, not all zero} or {"id", "kind":
        "source_direction", "profile_id", "cell_weights", "label_weights": {field: finite
        real c_f} over ("whitened_R", i) / ("whitened_S", i, j), i <= j, not all zero}
        (source directions need the callback). A mode direction's coordinate key is (kind,
        id); its derivatives are around the base lapse_factors / sources (no partition
        admission on phi). The tuple interface is unchanged and may be mixed with these.
      tracked_read_labels: list of read labels whose time averages, means and responses
        are returned (operator presence, first-moment Z, pair, population rows, or
        ("whitened_R", cell, i) / ("whitened_S", cell, i, j), i <= j, from the callback).
        Operator coarse_first_R / coarse_second_S rows are unsupported in every role: per
        0409 the corrected moments come only from the callback and are never duplicated
        (operator v001 rows: one global port frame; operator v002 rows: per-part B = -A
        frames plus whitening, refused as duplicates) (L8).
      diagonal_read_source_callback: None, or the root adapter path {"adapter": object
        exposing adapted_moment_reads and pair_source_hamiltonian (and
        raw_to_whitened_sources for source_frame "raw"), "operator_module": object passed
        unchanged as operator_module (must expose state_labels), "binding": the adapter
        binding whose "graph0" and "registration" are the SAME objects as graph0 and
        registration, "source_frame": "whitened" | "raw", "j_R": {cell: 3 reals}, "j_S":
        {cell: symmetric 3x3 reals}, "source_consistency_tolerance": real >= 0}. Its reads
        are evaluated at every new state and used in D, every D_a and every time average.
      chain_generators: list of distinct numpy.random.Generator, one per chain (same
        length as initial_paths); all randomness of chain c uses chain_generators[c].
      move_parameters: {"moves_per_sweep": int >= 1, "rotation_probability": (0,1),
        "whole_circle_probability": (0,1), "length_components": [(weight > 0,
        upper_fraction in (0,1]), ...] with at least one upper_fraction == 1}.
      palette_parameters: None (no palette move) or {"selection_probability": (0,1) with
        rotation_probability + selection_probability < 1, "palettes": [(weight > 0,
        nonempty collection of original owner labels), ...],
        "verify_against_full_enumeration": bool}; the additive blocked-palette move (L19).
      caps: {"max_events_per_path", "max_total_events", "max_sweeps",
        "max_channel_enumerations"} positive ints; reaching any ends the run "incomplete".
      burn_in_sweeps: int >= 0. measurement_sweeps: int >= 1 (one measurement per sweep).
      error_parameters: {"batches_per_chain": int >= 2 dividing measurement_sweeps,
        "sokal_window_constant": > 0, "rhat_max": >= 1, "min_batch_length_over_tau": > 0,
        "max_explicit_covariance_dimension": int >= 0}.
      numerical_tolerances: {"gauge_phase", "weight_partition", "reverse_rate"} reals >= 0
        (relative gauge/Hermiticity tolerances and absolute partition tolerance).
      implicit_closure: must be None (SPEC section 5 contract retained for later);
        anything else returns status "unsupported".

    Returns a dict: ok, status, stage_reached, failures, flags, inputs, coordinate_order,
    direction_status, tracked_read_labels, read_kinds, member_check, modes (None without mode
    directions; else profile/Gram metadata, base sources, direction positions, extensive
    F_total gradient/Hessian and score/contact moments, error-layout positions and uniform
    first/pair moments; L21-L23), estimates {dlogZ_du, d2logZ_du2,
    score_covariance, contact_mean, F (None), F_u, F_uu, read_means, read_mean_responses,
    per_chain, mean/max events per path, samples}, errors (only when mixing passed),
    mixing, diagnostics, conventions, scope, limitations. "ok" is True only when status is
    "complete", every requested direction is supported and mixing "passed". With mode
    directions and the callback, tracked_read_labels (output) ends with the nine reserved
    uniform moment labels (L23).
    """
    result = _new_result()
    failures = result["failures"]
    result["stage_reached"] = "inputs"
    if implicit_closure is not None:
        result["status"] = "unsupported"
        failures.append(
            "implicit_closure: v003 implements ordinary fixed-source equilibrium sampling only; "
            "the SPEC section 5 implicit HP volume closure is a retained later contract, so "
            "implicit_closure must be None"
        )
        return result

    kinds = _kind_table()
    unsupported = []
    api = _admit_operator_api(operator_api, palette_parameters is not None, failures)
    beta_in = _admit_real("beta", beta, failures)
    if beta_in is not None and not beta_in > 0.0:
        failures.append(f"input beta: must be > 0, got {beta_in!r}")
        beta_in = None
    lapse = _admit_lapse_factors(lapse_factors, failures)
    sources = _admit_label_reals("source_coefficients", source_coefficients, failures)
    vgrad = _admit_label_reals("volume_gradient_coefficients", volume_gradient_coefficients, failures)
    lam = _admit_real("volume_multiplier", volume_multiplier, failures)
    phases = _admit_gauge_phases(gauge_phases, failures)
    pair = _admit_pair_callback(diagonal_read_source_callback, graph0, registration, failures)
    pair_cells = None if pair is None else set(pair["j_R"])
    modes_in = {}
    coords = _admit_coordinates(derivative_coordinates, lapse, pair_cells, failures, modes_in)
    tracked = _admit_labels("tracked_read_labels", tracked_read_labels, failures)
    if None not in (sources, vgrad, tracked, coords):
        _admit_label_roles(sources, vgrad, tracked, coords, pair_cells, failures, unsupported)
    uniform_active = bool(modes_in) and pair is not None  # L23
    if uniform_active and tracked is not None:
        for lbl in tracked:
            if _label_kind(lbl) in _uniform_kinds():
                failures.append(
                    f"input tracked_read_labels: {lbl!r} uses a reserved uniform moment kind; "
                    "these columns are added automatically with mode directions (L23)"
                )
    gens = _admit_generators(chain_generators, failures)
    paths_in = _admit_initial_paths(initial_paths, kinds, failures)
    if gens is not None and paths_in is not None and len(gens) != len(paths_in):
        failures.append(
            f"input chain_generators ({len(gens)}) and initial_paths ({len(paths_in)}) differ in length"
        )
    moves = _admit_move_parameters(move_parameters, failures)
    palette = _admit_palette_parameters(palette_parameters, failures)
    if moves is not None and palette is not None and not (
        moves["rotation_probability"] + palette["selection_probability"] < 1.0
    ):
        failures.append(
            "input palette_parameters['selection_probability']: rotation_probability + "
            "selection_probability must be < 1 so the global regrowth keeps nonzero "
            "selection probability (blocked moves alone are not claimed irreducible)"
        )
        palette = None
    caps_in = _admit_caps(caps, failures)
    burn = _admit_int("burn_in_sweeps", burn_in_sweeps, 0, failures)
    n_meas = _admit_int("measurement_sweeps", measurement_sweeps, 1, failures)
    errp = _admit_error_parameters(error_parameters, n_meas, failures)
    tol = _admit_tolerances(numerical_tolerances, failures)
    if coords is not None and tracked is not None and not coords and not tracked:
        failures.append("input: no derivative coordinate and no tracked read; nothing to compute")
    result["inputs"] = {
        "beta": beta_in,
        "lapse_factors": None if lapse is None else dict(lapse),
        "source_coefficients": None if sources is None else dict(sources),
        "volume_gradient_coefficients": None if vgrad is None else dict(vgrad),
        "volume_multiplier": lam,
        "gauge_phases": phases,
        "derivative_coordinates": coords,
        "mode_directions": [
            {"coordinate": k, "profile_id": d["profile_id"],
             "cells_weighted": len(d["phi"]),
             "label_weights": None if d["fields"] is None else [list(fc) for fc in d["fields"]]}
            for k, d in modes_in.items()
        ],
        "tracked_read_labels": tracked,
        "diagonal_read_source_callback": None if pair is None else {
            "source_frame": pair["source_frame"],
            "cells": len(pair["j_R"]),
            "source_consistency_tolerance": pair["tol"],
        },
        "chains": None if gens is None else len(gens),
        "move_parameters": None if moves is None else {
            k: moves[k] for k in ("moves_per_sweep", "rotation_probability",
                                  "whole_circle_probability", "length_components")
        },
        "palette_parameters": None if palette is None else {
            "selection_probability": palette["selection_probability"],
            "palettes": [(w, sorted(map(repr, s))) for w, s in palette["palettes"]],
            "verify_against_full_enumeration": palette["verify"],
        },
        "caps": caps_in,
        "burn_in_sweeps": burn,
        "measurement_sweeps": n_meas,
        "error_parameters": errp,
        "numerical_tolerances": tol,
    }
    if failures:
        result["status"] = "failed"
        failures.extend(unsupported)
        return result
    if unsupported:
        result["status"] = "unsupported"
        failures.extend(unsupported)
        return result

    referenced = set(sources) | set(vgrad) | set(tracked)
    referenced |= {c[1] for c in coords if c[0] == "source"}
    run = {
        "api": api,
        "context": None,
        "stage": "model",
        "beta": beta_in,
        "n_of_cell": {cell: n - 1.0 for cell, n in lapse.items()},
        "lapse_index": {c[1]: i for i, c in enumerate(coords) if c[0] == "lapse"},
        "coords": coords,
        "n_u": len(coords),
        "sources": sources,
        "volume_gradient": vgrad,
        "lam": lam,
        "tracked": tracked,
        "tracked_all": list(tracked) + (list(_uniform_labels()) if uniform_active else []),
        "n_r": len(tracked) + (len(_uniform_labels()) if uniform_active else 0),
        "lapse_dirs": [(i, modes_in[c]["phi"]) for i, c in enumerate(coords)
                       if c[0] == "lapse_direction"],
        "source_dirs": [(i, modes_in[c]["phi"], modes_in[c]["fields"])
                        for i, c in enumerate(coords) if c[0] == "source_direction"],
        "uniform_labels": _uniform_labels() if uniform_active else (),
        "pair": None if pair is None else dict(pair, cells=None),
        "pair_coords": [(i, c) for i, c in enumerate(coords)
                        if c[0] in ("pair_source_R", "pair_source_S")],
        "needed_operator_labels": [lbl for lbl in referenced
                                   if _label_kind(lbl) not in _whitened_kinds()],
        "needed_whitened": [lbl for lbl in referenced if _label_kind(lbl) in _whitened_kinds()],
        "read_index": None,
        "read_labels_ref": None,
        "read_labels_tuple": None,
        "energy_cells": None,
        "group": None,
        "palette": palette,
        "kinds": kinds,
        "gauge": _gauge_table(kinds, phases),
        "tol": tol,
        "caps": caps_in,
        "moves": moves,
        "counters": {
            "events": 0,
            "channel_enumerations": 0,
            "sweeps": 0,
            "reverse_signature_fallbacks": 0,
            "restricted_enumerations": 0,
            "restricted_nonmember_records_dropped": 0,
            "palette_verifications": 0,
        },
        "zero_rate_directions": set(),
    }
    chain_diag = []

    def _diagnostics():
        return {
            "counters": dict(run["counters"]),
            "chains": [dict(d) for d in chain_diag],
            "zero_rate_directions": sorted(map(repr, run["zero_rate_directions"])),
        }

    # ---- Stage: operator schema validation (the member check follows; L2) --------
    result["stage_reached"] = "model"
    try:
        validated = api["validate_owned_model"](
            graph0=graph0, model=model, registration=registration
        )
    except Exception as exc:
        result["status"] = "failed"
        failures.append(f"validate_owned_model raised {type(exc).__name__}: {exc}")
        return result
    v_ok = validated.get("ok") if isinstance(validated, Mapping) else None
    if not (isinstance(v_ok, (bool, np.bool_)) and bool(v_ok)) or "context" not in validated:
        status = validated.get("status") if isinstance(validated, Mapping) else None
        result["status"] = "unsupported" if status == "unsupported" else "failed"
        failures.append("validate_owned_model did not return ok True with a context")
        if isinstance(validated, Mapping) and isinstance(validated.get("failures"), (list, tuple)):
            failures.extend(f"validate_owned_model: {f}" for f in validated["failures"])
        return result
    run["context"] = validated["context"]

    # ---- Stage: model-level member check (state independent; L2a) ----------------
    result["stage_reached"] = "member_check"
    m_ok, m_problems, m_forms = _model_member_check(model, phases, tol["gauge_phase"])
    result["member_check"] = {
        "status": "verified" if m_ok else "unsupported",
        "profile_forms": m_forms,
        "problems": m_problems,
        "note": (
            "every supplied coefficient of the model mapping checked before sampling; the "
            "per-primitive gauge check at visited states remains a second line (L2)"
        ),
    }
    if not m_ok:
        result["status"] = "unsupported"
        failures.append(
            "model is not verified to lie in the common-phase zero-holonomy member (checked on "
            "every supplied coefficient, independent of visited states)"
        )
        failures.extend(f"member_check: {p}" for p in m_problems)
        return result

    # ---- Stage: binding of energy cells, palette groups and dual sources --------------
    result["stage_reached"] = "binding"
    present_c, cells = _field(run["context"], "energy_cells")
    if not present_c or not isinstance(cells, (list, tuple)) or not all(_hashable(c) for c in cells):
        result["status"] = "failed"
        failures.append("context.energy_cells is missing or not a sequence of hashable cells")
        return result
    if len(set(cells)) != len(cells) or set(cells) != set(lapse):
        result["status"] = "failed"
        failures.append(
            "lapse_factors must cover exactly the cells of context.energy_cells (one N_alpha > 0 "
            "per coarse cell; energy_weights are aligned with that order)"
        )
        return result
    run["energy_cells"] = tuple(cells)
    if palette is not None:
        try:
            originals = list(graph0["A"]) + list(graph0["B"])
            group = {o: o for o in originals}
            for o in originals:
                for lab in graph0["slots"][o]:
                    group[lab] = o
        except (TypeError, KeyError) as exc:
            result["status"] = "failed"
            failures.append(f"graph0 permanent owner groups cannot be read for the palette: {exc}")
            return result
        bad = [sorted(map(repr, s - set(originals))) for _, s in palette["palettes"]
               if not s <= set(originals)]
        if bad:
            result["status"] = "failed"
            failures.append(f"palette_parameters: labels {bad!r} are not original owner labels")
            return result
        run["group"] = group
    if pair is not None and pair["source_frame"] == "raw":
        try:
            converted = pair["fns"]["raw_to_whitened_sources"](
                j_R_raw=pair["j_R"], j_S_raw=pair["j_S"]
            )
            conv_r, conv_s = converted
        except Exception as exc:
            result["status"] = "failed"
            failures.append(f"raw_to_whitened_sources failed: {type(exc).__name__}: {exc}")
            return result
        whitened = _admit_pair_sources(conv_r, conv_s, "raw_to_whitened_sources output", failures)
        if whitened is None or set(whitened[0]) != set(pair["j_R"]):
            result["status"] = "failed"
            failures.append("raw_to_whitened_sources did not return sources on the same cells")
            return result
        run["pair"]["j_R"], run["pair"]["j_S"] = whitened
    if modes_in:
        # v003 mode directions (L21, L22): every profile lists exactly context.energy_cells;
        # source directions need callback cells equal to those cells.
        bad = [repr(k) for k, d in modes_in.items() if set(d["phi"]) != set(cells)]
        if bad:
            result["status"] = "failed"
            failures.append(
                f"mode directions {bad[:20]!r}: cell_weights must list exactly the cells of "
                "context.energy_cells (explicit zeros; unit cell pairing, L22)"
            )
            return result
        if run["source_dirs"] and set(run["pair"]["j_R"]) != set(cells):
            result["status"] = "failed"
            failures.append(
                "source directions: diagonal_read_source_callback cells (j_R/j_S) must equal "
                "context.energy_cells (L21)"
            )
            return result
        meta, problem = _mode_metadata(run, modes_in, lapse)
        if meta is None:
            result["status"] = "failed"
            failures.append(problem)
            return result
        result["modes"] = meta

    n_u = run["n_u"]
    n_r = run["n_r"]
    series = []
    try:
        # ---- Stage: initial closed paths ------------------------------------------
        result["stage_reached"] = "initial_paths"
        paths = []
        for c, spec in enumerate(paths_in):
            run["stage"] = f"initial_paths[{c}]"
            paths.append(_initial_path(run, spec))
        # ---- Stage: sampling ------------------------------------------------------
        result["stage_reached"] = "sampling"
        for c in range(len(paths)):
            rng = gens[c]
            path = paths[c]
            diag = {
                "chain": c,
                "initial_events": len(path["times"]),
                "rotations": 0,
                "interval_proposals": 0,
                "whole_circle_proposals": 0,
                "zero_length_intervals": 0,
                "endpoint_rejections": 0,
                "metropolis_rejections": 0,
                "palette_proposals": 0,
                "palette_interval_proposals": 0,
                "palette_whole_circle_proposals": 0,
                "palette_zero_length_intervals": 0,
                "palette_held_rejections": 0,
                "palette_endpoint_rejections": 0,
                "palette_metropolis_rejections": 0,
                "palette_accepted": 0,
                "accepted_regrowths": 0,
                "accepted_in_measurement": 0,
                "sweeps_completed": 0,
                "measurements": 0,
            }
            chain_diag.append(diag)
            score = np.zeros((n_meas, n_u), dtype=np.float64)
            contact = np.zeros((n_meas, n_u, n_u), dtype=np.float64)
            reads = np.zeros((n_meas, n_r), dtype=np.float64)
            n_events = np.zeros(n_meas, dtype=np.int64)
            for sweep in range(burn + n_meas):
                if run["counters"]["sweeps"] >= caps_in["max_sweeps"]:
                    raise _Stop(
                        "incomplete",
                        f"chain {c} sweep {sweep}",
                        "cap max_sweeps reached; computation ended",
                    )
                run["counters"]["sweeps"] += 1
                run["stage"] = f"chain {c} sweep {sweep}"
                measuring = sweep >= burn
                for _ in range(moves["moves_per_sweep"]):
                    path, accepted = _move(run, path, rng, diag)
                    if accepted:
                        diag["accepted_regrowths"] += 1
                        if measuring:
                            diag["accepted_in_measurement"] += 1
                if measuring:
                    i = sweep - burn
                    s_vec, t_mat, r_vec, k = _measure(run, path)
                    score[i] = s_vec
                    contact[i] = t_mat
                    reads[i] = r_vec
                    n_events[i] = k
                    diag["measurements"] += 1
                diag["sweeps_completed"] += 1
            series.append(
                {
                    "score": score,
                    "contact": contact,
                    "reads": reads,
                    "events": n_events,
                    "accepted_in_measurement": diag["accepted_in_measurement"],
                }
            )
    except _Stop as stop:
        result["status"] = stop.status
        result["stage_reached"] = stop.stage
        failures.append(stop.message)
        result["diagnostics"] = _diagnostics()
        return result

    # ---- Stage: directions and analysis -------------------------------------------
    result["stage_reached"] = "analysis"
    supported = [i for i, c in enumerate(coords) if c not in run["zero_rate_directions"]]
    result["direction_status"] = {
        repr(c): ("supported" if i in supported else "unsupported: zero-rate source-opening")
        for i, c in enumerate(coords)
    }
    if len(supported) != len(coords):
        result["flags"].append(
            "unsupported directions dropped from every output (zero-rate source opening; no "
            "division by zero, no fabricated derivative)"
        )
    sup = np.array(supported, dtype=np.int64)
    for ser in series:
        ser["score"] = ser["score"][:, sup]
        ser["contact"] = ser["contact"][:, sup][:, :, sup]
    n_us = len(supported)
    point, per_chain, mixing, errors = _analyze(run, series, errp, n_us)
    beta_f = run["beta"]
    all_events = np.concatenate([ser["events"] for ser in series])
    result["coordinate_order"] = [coords[i] for i in supported]
    result["tracked_read_labels"] = list(run["tracked_all"])
    result["read_kinds"] = [_label_kind(lbl) for lbl in run["tracked_all"]]
    result["estimates"] = {
        "beta": beta_f,
        "dlogZ_du": point["g"],
        "d2logZ_du2": point["H"],
        "score_covariance": point["cov"],
        "contact_mean": point["T"],
        "F": None,
        "F_note": "absolute F = -log Z / beta not estimated (L4)",
        "F_u": -point["g"] / beta_f,
        "F_uu": -point["H"] / beta_f,
        "read_means": point["m"],
        "read_mean_responses": point["resp"],
        "per_chain": [
            {"dlogZ_du": e["g"], "d2logZ_du2": e["H"], "read_means": e["m"]} for e in per_chain
        ],
        "mean_events_per_path": float(all_events.mean()),
        "max_events_per_path_measured": int(all_events.max()),
        "samples_total": int(all_events.shape[0]),
    }
    result["mixing"] = mixing
    result["errors"] = errors
    result["diagnostics"] = _diagnostics()
    if result["modes"] is not None:
        ext, uni = _mode_outputs(result["modes"], result["coordinate_order"], point,
                                 run["tracked_all"], beta_f, errors)
        result["modes"]["extensive"] = ext
        result["modes"]["uniform_moments"] = uni
        worst = result["modes"]["gram_max_normalized_offdiagonal"]
        if worst is not None and worst != 0.0:
            result["flags"].append(
                f"mode profiles are not exactly orthogonal under the unit cell pairing (largest "
                f"normalized Gram offdiagonal {worst!r}); the root pairing must use the returned "
                "Gram (L22)"
            )
    if mixing["constant_columns"]:
        result["flags"].append(
            "constant columns (no sample variation in any chain) are listed in "
            "mixing.constant_columns; their zero spread is not evidence of mixing"
        )
    if mixing["status"] != "passed":
        result["flags"].append(
            f"mixing {mixing['status']}: no error band, replicate set or covariance is returned; "
            "estimates are evidence only"
        )
    result["status"] = "complete"
    result["stage_reached"] = "complete"
    result["ok"] = mixing["status"] == "passed" and len(supported) == len(coords)
    return result
