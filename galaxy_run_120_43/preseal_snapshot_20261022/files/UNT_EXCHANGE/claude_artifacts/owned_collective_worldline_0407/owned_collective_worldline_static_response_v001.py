"""Owned collective static response by positive imaginary-time worldlines.

UNT task 0407, version v001. Static author implementation: written as text and never
imported or executed by its author. numpy plus the Python standard library only.

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
Style reference (read as text): claude_artifacts/scalar_metric_solve_0397/
scalar_metric_particular_solve_v002.py (fail-closed result dict).

PUBLIC ENTRY (keyword-only, every argument required, no defaults):
  owned_collective_worldline_static_response(*, operator_api, graph0, model, registration,
      initial_paths, beta, lapse_factors, source_coefficients, volume_gradient_coefficients,
      volume_multiplier, gauge_phases, derivative_coordinates, tracked_read_labels,
      extra_diagonal_reads, chain_generators, move_parameters, caps, burn_in_sweeps,
      measurement_sweeps, error_parameters, numerical_tolerances, implicit_closure)
It returns a plain fail-closed dict with "ok", "status" (complete | incomplete |
unsupported | failed), "stage_reached" and "failures". When ok is False every populated
field is evidence only, never a result.

ASSUMED OPERATOR API (state level, basis free; the operator module is NOT imported here).
The caller passes `operator_api`, a mapping or object exposing these module-level,
keyword-only callables (names to be reconciled by the final checker if they differ):
  validate_owned_model(*, graph0, model, registration)
      -> dict with "ok" True and a validated "context"; otherwise its "status"
         ("unsupported" is passed through, anything else is "failed") and "failures".
  canonical_state_key(*, context, state) -> key; equal keys <=> equal current labelled
      configurations (0406 item 2). Keys must compare with == to a single bool.
  primitive_channels(*, context, state) -> list of records BEFORE aggregation, one per
      primitive, each a mapping (or object) with fields
        owner_id, kind in {flip, hop, bind, admit, admit_rev, birth, birth_rev},
        target_state, amplitude (complex <target|h_X|state>), queried_support,
        changed_support (iterable of hashables), weights {cell: (w(target)+w(source))/2}.
      Every reverse reconnection alternative is a record; coincident destinations stay
      separate records. A record with amplitude exactly 0 is skipped (no jump mark).
  diagonal_terms(*, context, state) -> list of records with value (real), support and
      weights {cell: w(state)}.
  read_rows(*, context, state) -> list of records with label (hashable, unique per
      state), value (real) and optionally kind (e.g. presence / first-moment Z / pair).
      A label absent at a state has value 0 there (presence-masked reads; contract 5).
Kind -> gauge increments (contract section 3 + assembly lines 300-327): flip and hop
change no record bit, cell or slot; bind flips one record bit q_v; admit R->S raises the
Spent number N_S by one (admit_rev lowers it); birth adds one active slot N with
newborns loaded R,p=q=0 (birth_rev removes it). Reverse pairs: flip<->flip, hop<->hop,
bind<->bind, admit<->admit_rev, birth<->birth_rev.

WHERE THE SPEC IS IMPLEMENTED
  Section 1 (member, gauge, H_c, beta, component): _admit_gauge_phases, _gauge_table,
    _channels_at (gauge check, W >= 0), _diagonal_at (real diagonals), _segment_at
    (H_c = H[N] - sum_a j_a O_a - lambda A); validate_owned_model is called first.
  Section 2 (closed paths, no basis, primitive jump marks): path dict {segments,
    events, times}; _segment_at/_channels_at enumerate only the current state's
    channels; per-primitive W with lapse weights BEFORE aggregation; r(x) = sum W.
  Section 3 (detailed-balance moves): _interval_move (unconditioned CTMC regrowth from
    the fixed initial endpoint, endpoint rejection, min(1, exp{int_new(r-D) -
    int_old(r-D)}) in log arithmetic, all lengths < beta plus the whole circle with
    anchor fixed), _rotate (uniform origin rotation, probability one), _ctmc_segment.
  Section 4 (estimators): _measure (S_a, T_ab, time-averaged reads), _estimate
    (<S>, Cov(S,S) + <T>, read means, Cov(S, read)), result "estimates".
  Section 7 (cost and errors): caps -> status incomplete (never rejection); _analyze
    (batch means, jackknife joint covariance, integrated autocorrelation, R-hat across
    independent chains, mixing status); storage/work described under COST.
  Section 5 is NOT implemented: implicit_closure must be None (contract retained).
  Section 6 is scope: see "scope" in the result and CONVENTIONS_0407_V001.md.

SEMANTICS. In the positive gauge G = (-1)^{sum_v q_v} (-e^{i phi_adm})^{N_S}
(-e^{i phi_birth})^{N} (assembly lines 300-327, e^{-i theta} epsilon = -|epsilon| written
as -e^{i phi_birth} = e^{i theta}), every primitive matrix element h_X[y,x] becomes
conj(G(y)) h_X[y,x] G(x); it must equal -|h_X[y,x]| (real, nonpositive) within the
caller's relative gauge_phase tolerance, otherwise status "unsupported" (outside the
proven common-phase zero-holonomy member). With n_alpha = N_alpha - 1 and the V002 support
mean weights wbar_alphaX,
    W_X(x->y) = |h_X[y,x]| * (1 + sum_alpha n_alpha wbar_alphaX)        (per primitive),
    D(x) = sum_diag d_X(x) (1 + sum_alpha n_alpha w_alphaX(x))
           - sum_a j_a O_a(x) - lambda A(x),     A(x) = sum_a a_a O_a(x),
    r(x) = sum_X W_X(x->.),   H_c = D - W,   Z = Tr exp(-beta H_c).
A closed path on the imaginary-time circle [0, beta) has weight
exp(-int D) prod_events W. Source coordinates u are ("lapse", cell) [d/dn = d/dN],
("source", label) [j_label] and ("volume_multiplier",) [lambda]; all are affine, so
D_ab = W_ab = 0 exactly and
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

COST. One stored path holds one state object, canonical key and O(n_u) numbers per dwell
segment plus O(n_u) numbers per event: O(events * (state size + n_u)) through this
state-level API (see LIMITATIONS L3). Each generated event costs one primitive_channels,
one diagonal_terms, one read_rows and one canonical_state_key call at the new state (all
O(current vertices) in the worst case) plus the reverse-pairing check; each measurement
costs one read_rows call per distinct dwell state and O(events * (n_u + n_r)) arithmetic.
Error analysis stores O(chains * measurements * (n_u^2 + n_r)) numbers and O(J * n_y)
jackknife replicates. No Hilbert-space list, basis index or dense operator is built.

LIMITATIONS: see the module-level string LIMITATIONS.
"""

import bisect
import math
from collections.abc import Mapping

import numpy as np


LIMITATIONS = """
L1. Operator API is ASSUMED (docstring): function names, record field names (owner_id,
    kind, target_state, amplitude, queried_support, changed_support, weights, value,
    label) and kind tokens. Mismatches fail closed ("failed"); the final checker
    reconciles names with owned_parent_operator_v001.py.
L2. Positive gauge. The gauge is applied through per-kind increments of record parity,
    Spent number and slot number (contract section 3), with caller-declared common
    phases gauge_phases {admission_phase = arg kappa, birth_phase = arg epsilon}. Every
    primitive enumerated at every VISITED state (all alternatives, not only those taken)
    is checked; primitives at never-visited states are not. Model-level membership (real
    h, t, g > 0, zero hopping phases, uniform kappa phase, common epsilon phase) is
    otherwise delegated to validate_owned_model. Net increments of every regrown segment
    are compared with the replaced segment (and the initial path must close them), which
    detects kind labels inconsistent with a state-function gauge on sampled paths only.
L3. Storage. The SPEC's O(V0 + events) path storage presumes event-delta storage. Through
    target_state objects this module stores one state object and key per dwell segment,
    i.e. O(events * state size) unless the operator's states share structure. An
    operator "apply event delta" API would be needed to reach the SPEC bound.
L4. Absolute free energy F = -log Z/beta is NOT estimated (None): the positive path
    measure gives derivatives only. A normalization (e.g. thermodynamic integration in
    beta) is not implemented. No global energy scalar is subtracted from D.
L5. Coordinates are affine: lapse n_alpha (identical derivative to N_alpha), read source
    j_label, lambda. W_ab = D_ab = 0 exactly. Nonlinear coordinates (e.g. g00 with
    N = sqrt(1 + 2 n_g)) follow by the caller's chain rule d_vv log Z = J^T H J +
    sum_a d_a log Z d_vv u_a using the returned first AND second derivatives. Read-frame,
    registration, preparation and map derivative contacts are NOT included (reads fixed).
L6. Zero-rate source-opening directions (an available primitive with W = 0 but W_a != 0)
    are detected only at visited states; such a direction is dropped from all outputs and
    listed as unsupported. With N_alpha > 0 and nonnegative partition weights it cannot
    occur; it is reachable only with weights that make 1 + sum n wbar = 0.
L7. Conserved-resource component. All chains must start in ONE declared component; the
    module cannot verify membership without enumeration. Explicitly weighted unions of
    superselection components are not combined here (caller weights separate runs).
L8. Coarse R_alpha, S_alpha with the current-state 1/m_alpha normalization are available
    only through the caller's extra_diagonal_reads callable (registration-owned); the
    module never forms C = M - mu mu^T and never inverts covariance-only response. The
    physical read-read susceptibility is obtained by making those reads source
    coordinates (d2logZ); a separate read-read path covariance is not returned.
L9. A ("fixed diagonal volume gradient") is interpreted literally as an explicit linear
    combination of diagonal reads (operator rows and/or extra reads) with caller
    coefficients and multiplier lambda. A(m) self-consistency (SPEC section 5) is not
    solved; implicit_closure must be None (status unsupported otherwise).
L10. Interval selection density (SPEC ambiguity): start time uniform on [0, beta); with
    probability whole_circle_probability the whole circle anchored at that time; else a
    length beta*U*f with U uniform on [0,1) and f drawn from caller-weighted components
    (at least one f = 1 so every length below beta has positive density). Rotation is a
    separate move with caller probability. All are source independent and symmetric.
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
    and no path is ever rejected because of a cap.
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


def _admit_operator_api(operator_api, failures):
    names = (
        "validate_owned_model",
        "canonical_state_key",
        "primitive_channels",
        "diagonal_terms",
        "read_rows",
    )
    api = {}
    for nm in names:
        present, fn = _field(operator_api, nm)
        if not present or not callable(fn):
            failures.append(
                f"input operator_api: callable {nm!r} is missing (assumed API in docstring)"
            )
        else:
            api[nm] = fn
    return api if len(api) == len(names) else None


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


def _admit_coordinates(value, lapse, failures):
    if not isinstance(value, (list, tuple)):
        failures.append("input derivative_coordinates: must be a list or tuple of tuples")
        return None
    out = []
    for i, coord in enumerate(value):
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
        else:
            failures.append(
                f"input derivative_coordinates[{i}]: {coord!r} is not ('lapse', cell), "
                "('source', label) or ('volume_multiplier',)"
            )
            continue
        if coord in out:
            failures.append(f"input derivative_coordinates[{i}]: duplicate {coord!r}")
            continue
        out.append(coord)
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


def _weights(run, raw, where):
    if not isinstance(raw, Mapping):
        raise _Stop("failed", run["stage"], f"{where}: weights is not a mapping cell -> real")
    out = {}
    for cell, w in raw.items():
        if cell not in run["n_of_cell"]:
            raise _Stop(
                "failed",
                run["stage"],
                f"{where}: weight cell {cell!r} has no caller lapse factor",
            )
        wf = _real_value(w)
        if wf is None:
            raise _Stop("failed", run["stage"], f"{where}: weight {cell!r} = {w!r} not finite real")
        out[cell] = wf
    return out


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


def _signature(changed):
    try:
        sig = frozenset(changed)
    except TypeError:
        return None
    return sig


def _channels_at(run, state):
    """Nonnegative per-primitive rates at `state` (SPEC sections 1-2), before aggregation."""
    counters = run["counters"]
    if counters["channel_enumerations"] >= run["caps"]["max_channel_enumerations"]:
        raise _Stop(
            "incomplete",
            run["stage"],
            "cap max_channel_enumerations reached; computation ended (no path was rejected)",
        )
    counters["channel_enumerations"] += 1
    records = _op(run, "primitive_channels", context=run["context"], state=state)
    if not isinstance(records, (list, tuple)):
        raise _Stop("failed", run["stage"], "primitive_channels did not return a list")
    kinds = run["kinds"]
    tol_g = run["tol"]["gauge_phase"]
    channels = []
    for i, rec in enumerate(records):
        where = f"primitive_channels record {i}"
        fields = {}
        for nm in ("owner_id", "kind", "target_state", "amplitude", "changed_support", "weights"):
            present, val = _field(rec, nm)
            if not present:
                raise _Stop("failed", run["stage"], f"{where}: field {nm!r} missing")
            fields[nm] = val
        kind = fields["kind"]
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
        weights = _weights(run, fields["weights"], where)
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


def _diagonal_at(run, state):
    """Diagonal H[N] energy and its lapse derivatives (real diagonals verified)."""
    records = _op(run, "diagonal_terms", context=run["context"], state=state)
    if not isinstance(records, (list, tuple)):
        raise _Stop("failed", run["stage"], "diagonal_terms did not return a list")
    tol_g = run["tol"]["gauge_phase"]
    h_terms = []
    lapse_terms = {cell: [] for cell in run["lapse_index"]}
    for i, rec in enumerate(records):
        where = f"diagonal_terms record {i}"
        present_v, raw = _field(rec, "value")
        present_w, wraw = _field(rec, "weights")
        if not present_v or not present_w:
            raise _Stop("failed", run["stage"], f"{where}: fields 'value' and 'weights' required")
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
        weights = _weights(run, wraw, where)
        mult = _lapse_multiplier(run, weights, where)
        h_terms.append(value * mult)
        for cell, w in weights.items():
            if cell in lapse_terms:
                lapse_terms[cell].append(value * w)
    return math.fsum(h_terms), {c: math.fsum(v) for c, v in lapse_terms.items()}


def _reads_at(run, state):
    """Diagonal reads at `state`: operator rows plus caller extra reads (labels disjoint)."""
    rows = _op(run, "read_rows", context=run["context"], state=state)
    if not isinstance(rows, (list, tuple)):
        raise _Stop("failed", run["stage"], "read_rows did not return a list")
    values = {}
    kinds = {}
    for i, rec in enumerate(rows):
        present_l, label = _field(rec, "label")
        present_v, raw = _field(rec, "value")
        if not present_l or not present_v:
            raise _Stop("failed", run["stage"], f"read_rows record {i}: label and value required")
        if not _hashable(label):
            raise _Stop("failed", run["stage"], f"read_rows record {i}: label not hashable")
        v = _real_value(raw)
        if v is None:
            raise _Stop("failed", run["stage"], f"read_rows record {i}: value not finite real")
        if label in values:
            raise _Stop("failed", run["stage"], f"read_rows: duplicate label {label!r}")
        values[label] = v
        present_k, kind = _field(rec, "kind")
        if present_k:
            kinds[label] = kind
    if run["extra"] is not None:
        try:
            extra = run["extra"](context=run["context"], state=state, rows=rows)
        except Exception as exc:
            raise _Stop(
                "failed", run["stage"], f"extra_diagonal_reads raised {type(exc).__name__}: {exc}"
            )
        if not isinstance(extra, Mapping):
            raise _Stop("failed", run["stage"], "extra_diagonal_reads did not return a mapping")
        for label, raw in extra.items():
            if label in values:
                raise _Stop(
                    "failed", run["stage"], f"extra read label {label!r} collides with a read row"
                )
            v = _real_value(raw)
            if v is None:
                raise _Stop("failed", run["stage"], f"extra read {label!r} not finite real")
            values[label] = v
            kinds[label] = "extra_diagonal_read"
    pending = run["labels_unseen"]
    if pending:
        seen = [lbl for lbl in pending if lbl in values]
        for lbl in seen:
            pending.discard(lbl)
    return values, kinds


def _segment_at(run, state):
    """Dwell-segment record {state, key, D, r, Da} at `state` and its channels."""
    key = _state_key(run, state)
    channels, exit_rate = _channels_at(run, state)
    d_h, d_lapse = _diagonal_at(run, state)
    values, _ = _reads_at(run, state)
    src = math.fsum([-j * values.get(lbl, 0.0) for lbl, j in run["sources"].items()])
    vol = math.fsum([a * values.get(lbl, 0.0) for lbl, a in run["volume_gradient"].items()])
    diag = math.fsum([d_h, src, -run["lam"] * vol])
    if not math.isfinite(diag):
        raise _Stop("failed", run["stage"], "diagonal energy D(x) not finite")
    da = np.zeros(run["n_u"], dtype=np.float64)
    for idx, coord in enumerate(run["coords"]):
        if coord[0] == "lapse":
            da[idx] = d_lapse[coord[1]]
        elif coord[0] == "source":
            da[idx] = -values.get(coord[1], 0.0)
        else:
            da[idx] = -vol
    seg = {"state": state, "key": key, "D": diag, "r": exit_rate, "Da": da}
    return seg, channels


def _target_key(run, ch):
    if not ch["has_key"]:
        ch["key"] = _state_key(run, ch["target"])
        ch["has_key"] = True
    return ch["key"]


def _event_from_channel(run, ch):
    """Event record with rho_a = W_a / W (lapse: wbar_alpha / multiplier; others 0)."""
    rho = np.zeros(run["n_u"], dtype=np.float64)
    for cell, w in ch["weights"].items():
        idx = run["lapse_index"].get(cell)
        if idx is not None:
            rho[idx] = w / ch["mult"]
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


def _clipped_integral(segments, times, horizon, length):
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
        terms.append((segments[j]["r"] - segments[j]["D"]) * (hi - lo))
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


def _interval_move(run, path, rng, diag):
    """One move: rotation (prob p_rot) or interval regrowth with endpoint rejection."""
    beta = run["beta"]
    mp = run["moves"]
    if float(rng.random()) < mp["rotation_probability"]:
        diag["rotations"] += 1
        return _rotate(run, path, float(rng.random()) * beta), False
    origin = float(rng.random()) * beta
    whole = float(rng.random()) < mp["whole_circle_probability"]
    if whole:
        length = beta
        diag["whole_circle_proposals"] += 1
    else:
        u = float(rng.random())
        frac = mp["cumulative_components"][-1][1]
        for cum, f in mp["cumulative_components"]:
            if u < cum:
                frac = f
                break
        length = float(rng.random()) * frac * beta
        diag["interval_proposals"] += 1
        if not length > 0.0:
            diag["zero_length_intervals"] += 1
            return path, False
    rot = _rotate(run, path, origin)
    k = len(rot["times"])
    if whole:
        m = k
    else:
        m = bisect.bisect_left(rot["times"], length)
        if m < k and rot["times"][m] == length:
            raise _Stop("failed", run["stage"], "interval end coincides with an event time (L15)")
    terminal = rot["segments"][m]
    old_int = _clipped_integral(rot["segments"], rot["times"], beta, length)
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
    new_int = _clipped_integral(segs, times, length, length)
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
    cache = {}
    tracked = run["tracked"]
    for j, seg in enumerate(segments):
        key = seg["key"]
        cacheable = _hashable(key)
        if cacheable and key in cache:
            reads[j] = cache[key]
            continue
        values, kinds = _reads_at(run, seg["state"])
        row = np.array([values.get(lbl, 0.0) for lbl in tracked], dtype=np.float64)
        for lbl in tracked:
            if lbl in kinds and lbl not in run["tracked_kinds"]:
                run["tracked_kinds"][lbl] = kinds[lbl]
        reads[j] = row
        if cacheable:
            cache[key] = row
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
        + [("read", lbl) for lbl in run["tracked"]]
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
# Result
# ----------------------------------------------------------------------------------


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
        "estimates": None,
        "errors": None,
        "mixing": None,
        "diagnostics": None,
        "conventions": {
            "hamiltonian": (
                "H_c = H[N] - sum_a j_a O_a - lambda A, H[N] = H + sum_alpha n_alpha E_alpha, "
                "n = N - 1; per primitive multiplier 1 + sum_alpha n_alpha wbar_alphaX applied "
                "BEFORE aggregation; beta is one global inverse energy"
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
                "('volume_multiplier',) lambda; second-source contacts are exactly zero in these "
                "coordinates; other coordinates by the caller's chain rule"
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
    extra_diagonal_reads,
    chain_generators,
    move_parameters,
    caps,
    burn_in_sweeps,
    measurement_sweeps,
    error_parameters,
    numerical_tolerances,
    implicit_closure,
):
    """Static joint source Hessians of the owned collective by positive worldline sampling.

    Arguments (keyword-only, all required, no defaults; no value is chosen here):
      operator_api: mapping/object with the state-level callables listed in the module
        docstring (validate_owned_model, canonical_state_key, primitive_channels,
        diagonal_terms, read_rows), supplied at run time; nothing is imported.
      graph0, model, registration: passed unchanged to validate_owned_model. The model must
        be the common-phase zero-holonomy member (real h, t, g > 0, zero hopping phases,
        uniform admission phase, common Birth phase, real diagonals); violations found at
        visited states return status "unsupported".
      initial_paths: one entry per chain, {"x0": state, "events": [ {tau, kind, owner_id,
        target_key}, ... ]}; an empty event list is the constant path at x0. Events must
        have 0 < tau strictly increasing < beta, match exactly one positive-rate primitive
        and close at x0. All chains must lie in one declared conserved-resource component.
      beta: finite real > 0 (one global inverse energy).
      lapse_factors: {cell: N_alpha > 0} for every coarse cell appearing in any weight.
      source_coefficients: {read label: j_a} (may be empty); H_c gains -sum j_a O_a.
      volume_gradient_coefficients: {read label: a_a} with A = sum a_a O_a (may be empty).
      volume_multiplier: lambda (finite real); H_c gains -lambda A.
      gauge_phases: {"admission_phase": arg kappa, "birth_phase": arg epsilon} of the
        member's common phases (radians).
      derivative_coordinates: list of ("lapse", cell) | ("source", label) |
        ("volume_multiplier",).
      tracked_read_labels: list of read labels whose time averages, means and responses
        are returned (presence, first-moment Z, pair, or extra reads).
      extra_diagonal_reads: None or callable(*, context, state, rows) -> {label: real} for
        caller/registration diagonal reads (e.g. coarse R, S with current 1/m_alpha);
        labels must not collide with operator read rows.
      chain_generators: list of distinct numpy.random.Generator, one per chain (same
        length as initial_paths); all randomness of chain c uses chain_generators[c].
      move_parameters: {"moves_per_sweep": int >= 1, "rotation_probability": (0,1),
        "whole_circle_probability": (0,1), "length_components": [(weight > 0,
        upper_fraction in (0,1]), ...] with at least one upper_fraction == 1}.
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
    direction_status, tracked_read_labels, read_kinds, estimates {dlogZ_du, d2logZ_du2,
    score_covariance, contact_mean, F (None), F_u, F_uu, read_means, read_mean_responses,
    per_chain, mean/max events per path, samples}, errors (only when mixing passed),
    mixing, diagnostics, conventions, scope, limitations. "ok" is True only when status is
    "complete", every requested direction is supported and mixing "passed".
    """
    result = _new_result()
    failures = result["failures"]
    result["stage_reached"] = "inputs"
    if implicit_closure is not None:
        result["status"] = "unsupported"
        failures.append(
            "implicit_closure: v001 implements ordinary fixed-source equilibrium sampling only; "
            "the SPEC section 5 implicit HP volume closure is a retained later contract, so "
            "implicit_closure must be None"
        )
        return result

    kinds = _kind_table()
    api = _admit_operator_api(operator_api, failures)
    beta_in = _admit_real("beta", beta, failures)
    if beta_in is not None and not beta_in > 0.0:
        failures.append(f"input beta: must be > 0, got {beta_in!r}")
        beta_in = None
    lapse = _admit_lapse_factors(lapse_factors, failures)
    sources = _admit_label_reals("source_coefficients", source_coefficients, failures)
    vgrad = _admit_label_reals("volume_gradient_coefficients", volume_gradient_coefficients, failures)
    lam = _admit_real("volume_multiplier", volume_multiplier, failures)
    phases = _admit_gauge_phases(gauge_phases, failures)
    coords = _admit_coordinates(derivative_coordinates, lapse, failures)
    tracked = _admit_labels("tracked_read_labels", tracked_read_labels, failures)
    if extra_diagonal_reads is not None and not callable(extra_diagonal_reads):
        failures.append("input extra_diagonal_reads: must be None or a callable")
    gens = _admit_generators(chain_generators, failures)
    paths_in = _admit_initial_paths(initial_paths, kinds, failures)
    if gens is not None and paths_in is not None and len(gens) != len(paths_in):
        failures.append(
            f"input chain_generators ({len(gens)}) and initial_paths ({len(paths_in)}) differ in length"
        )
    moves = _admit_move_parameters(move_parameters, failures)
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
        "tracked_read_labels": tracked,
        "extra_diagonal_reads": None if extra_diagonal_reads is None else "callable",
        "chains": None if gens is None else len(gens),
        "move_parameters": None if moves is None else {
            k: moves[k] for k in ("moves_per_sweep", "rotation_probability",
                                  "whole_circle_probability", "length_components")
        },
        "caps": caps_in,
        "burn_in_sweeps": burn,
        "measurement_sweeps": n_meas,
        "error_parameters": errp,
        "numerical_tolerances": tol,
    }
    if failures:
        result["status"] = "failed"
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
        "n_r": len(tracked),
        "tracked_kinds": {},
        "extra": extra_diagonal_reads,
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
        },
        "zero_rate_directions": set(),
        "labels_unseen": set(referenced),
    }
    chain_diag = []

    def _diagnostics():
        return {
            "counters": dict(run["counters"]),
            "chains": [dict(d) for d in chain_diag],
            "labels_never_observed": sorted(map(repr, run["labels_unseen"])),
            "zero_rate_directions": sorted(map(repr, run["zero_rate_directions"])),
        }

    # ---- Stage: model validation (operator owns the model-level checks) ----------
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
                    path, accepted = _interval_move(run, path, rng, diag)
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
    result["tracked_read_labels"] = list(tracked)
    result["read_kinds"] = [run["tracked_kinds"].get(lbl) for lbl in tracked]
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
    if run["labels_unseen"]:
        result["flags"].append(
            "some referenced labels were never present in any visited state's reads (value 0 "
            "throughout); see diagnostics.labels_never_observed"
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
