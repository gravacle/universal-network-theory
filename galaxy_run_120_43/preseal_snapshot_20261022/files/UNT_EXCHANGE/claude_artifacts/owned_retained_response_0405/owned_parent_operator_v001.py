"""Owned-parent operator adapter V001 -- UNT task 0405, contract section 11(A).

STATUS. Static author implementation (AUTHOR A). Its author never imported or
executed it, any legacy module, or any UNT/Codex module. It contains no numerical
control, no propagation, no data extraction and no parameter value. Every physical
coefficient, profile, registration and state is explicit caller input.

BINDING SPECIFICATION (each sha256 computed from bytes before authoring)
  UPC = /Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13
  XCH = /Users/bgm/Research/UNT_EXCHANGE
  CONTRACT  UPC/helpers/coefficient_method/OWNED_RETAINED_RESPONSE_FULL_H_SOURCE_COLUMN_IMPLEMENTATION_CONTRACT_V001.txt
            fcad9039574f1666af005bb76a231f14b90f0c8dd82acebd2b16ab77941cd642
  ADDENDUM  UPC/helpers/coefficient_method/OWNED_RETAINED_PROVIDER_IMPLEMENTATION_MANDATORY_READ_AND_LABEL_ADDENDUM_V001.txt
            7cb15b4a5ac2ea33dfd43801c011142bc2b2388c3be0087152c049e78deccd39  (mandatory)
  TASK      XCH/FROM_CODEX/0405_2026-10-16_main_owned_response_provider_implementation.md
            7baab49ebbd01de684df56a074b823552c1eca9e787384ad0a0084144295c003
  0406      XCH/FROM_CODEX/0406_2026-10-16_response_moments_and_current_state_keys.md
            a465d9e3f703f2a2f19d383446c6a2bf6486e5f6be9fdf5996fc96dfb4693d50  (binding corrections)
  REGISTER  UPC/CODEX1/COARSE_REGISTER_STATE_BOUNDARY_WORKING_SPECIFICATION_V001.json
            032a564bd018b7302bd60de633f8e3c9d2f91f8c079f16b62548bce0e4e53d94  (adopted)
  V002      UPC/CODEX1/COARSE_PROPER_TIME_ENERGY_COUPLING_PROPOSAL_V002.json
            494d0124c1cd49841760dfc49673d696eab3486d75b31fda708679fa5cacb78a  (provisionally adopted,
            explicitly COUNTED assumption; adoption record UPC/CODEX1/COARSE_PROPER_TIME_ENERGY_COUPLING_ADOPTION_V001.json
            b5e7c2e3f12a6a4e3358a3c63a797783645d69240e757778ca42a91729a22465)
  LEDGER    UPC/CODEX1/READINESS_OWNED_READY_FALLBACK_ADOPTION_AND_POSTULATE_LEDGER_V001.md
            732bc83ec2e599021dcc6533dca54761f9c40979ce7f2a7651a6d19b2f0e97a0
  CLOC      UPC/CODEX1/READINESS_CURRENT_GRAPH_ROOT_NEIGHBOR_MATCHING_AND_SCALING_PROPOSED_V001.md
            388621c0ed2b5929ab097a77fa0ba8da576cbbfe4d682840080679671bf7af53
  GEN       UPC/helpers/coefficient_method/CURRENT_GRAPH_ALL_MATCHING_LOADED_BIRTH_GENERATOR_PROPOSED_V001.md
            8ab3d7a70a02cc55cec8301b5c6c2d880945d7682ccd0c71812feeec00136930, with its mandatory companion
            CURRENT_GRAPH_BIRTH_CUT_CLASS_PARAMETERIZATION_SCOPE_COMPANION_V001.md
            eebf34cc5d08e2e44c20784398ce7639bb99675b5b23cbe01003800cb7a76316 (cut class C(G)=C_loc)
  DOMAIN    UPC/helpers/coefficient_method/OWNED_READY_CURRENT_GRAPH_LOCAL_REWRITE_BOUND_AND_NATIVE_CLOCK_WINDOW_PROPOSED_V001.md
            715680458489837d3306bdbb2f05ffb9c56e9fb25fdb5371dafc369743559243
  SUPPORT   XCH/claude_artifacts/native_energy_support_0399/NATIVE_ENERGY_OWNER_SOURCE_MAP_0399_V001.md
            5edcf7e56d337c9ad9a5911c46789045f4f89007c0b49bf7d25acbe08abde584, applied with
            SOURCE_CHECK_0399_FIDELITY_V002.md 0c661284b9ce10b447ddc2c868942740c53fa418df332f247c7cb5690ff88134,
            SOURCE_CHECK_0399_COMPLETENESS_V001.md ca91cbb318169eb498d2d586395a2472f14d763a84c28b25b1b1d5a50ee4dc3a
            and its erratum b1552d8a69a7a620f2c98d24b5f151854ed11087f6a91b1099c634fcea76a497
  PRIMS     XCH/claude_artifacts/native_primitive_definitions_0400/NATIVE_PRIMITIVE_DEFINITIONS_0400_V001.md
            f2957b9baef013e5bf0dd8a365ffdba2acaf2ddcce355f21540478b9c418cf69, applied with
            SOURCE_CHECK_0400_V001.md 8ca3f00a35eb8dc5c7f64ca132faae2b598e3911b038444a1269f7dae07d4ae8
  H(2)      UPC/helpers/response_packet_audit/EXACT_R_PURE_FLIP_IMPLEMENTATION_APPLICABILITY_REVIEW_RECORD_V001.json
            f032b0888307da3669099706c8ac1a776f41bc4e1c553ec5fc729d8e4399830d (l.17 "complete four-state H(2)")
            and UPC/CODEX1/GALAXY_COLLECTIVE_MODEL_ASSEMBLY_2026-10-15.md
            39afc2e24d89093d9c9c8fb339640b2c89ed724bd537526a4e376b11e413b9dd (only grep hit l.522, l.742 viewed)
  Also read (they govern module B, not this module): partial Legendre d81d48e8407f5576305dbbb50a275f163401bbb91f67b5938dc9736ec8b21663,
  Kubo/zero mode a7d048c11a826d6d2627afd3f5324458a0350bc6abbd58bd8ab8d6c39d7eedf7, pair kernel/lapse
  facdfe454904ea27b38df19865168a7560bf24b56cb774c549ea53a1addec9b4.
  Legacy code, read as TEXT only (never imported or executed); reused logic is attributed inline:
    PRIMARY   canonical_join_backend_v002.py 0d28150ff9edeab3b75543acb6dbd7da472770e1ccec98dfaf948348650c07a3
    SECONDARY native_many_carrier_sparse_operator_v001.py 6b8d8dfdd8b1973f80b587c98584610759ca8d796010fa3dcf3928741f8caf88
    ADDITIONAL root_native_shared_parent_clock_transport_v001.py d7871d1bd4c55b826c2d7a04606a2552e418017c12379fc018b90811aae4a2a9
  Result-dict style: XCH/claude_artifacts/scalar_metric_solve_0397/scalar_metric_particular_solve_v002.py
    ef767fd79f60852e23ec0de29b04737cf4acfacca3461d83f5b3d01413abaecf

SEMANTICS (current owned member P26_CONCURRENT_BIRTH_V002_OWNED_READY, LEDGER l.3, l.11-20)
  Domain. graph0 is an explicit labelled simple bipartite degree-four graph G0 on the original
  vertices. K = V0 owner slots, one per original vertex o_j, each with two fixed newborn labels
  a_j (part A) and b_j (part B) and one private donor pair (o_j, 0), (o_j, 1). Original vertices
  persist; a_j, b_j are present exactly when slot j is active.
  State. Canonical key (slots, edgeset, inc, p, q, s, donors): seven nonnegative ints = bit sets
  over fixed ids (owner order, stable edge codes, vertex ids, donor ids). It is a function of the
  CURRENT labelled configuration only: supporting graph, active slots, incidence n_e, carrier p_v,
  record q_v, cell (R or S per present site), donors (R_D or I_D). Equal labelled configurations
  reached by different histories are the same key; no history label exists (contract s.2; ADDENDUM 2).
  Stable edge key. The ordered bipartite pair (A-part label, B-part label) of the current endpoints
  (ADDENDUM 2, 0406 item 2, REGISTER coarse_register.edges). Internally code = id(A)*NB + offset(B).
  An old edge restored by any inverse reconnection has the same key and the same coefficients.
  Inventory. M_v = 1 on every present site: cell R or S, p and q free (8 local states); the key
  cannot represent an I cell on a present site. Declared sector (contract s.2): N_c = S_graph and
  donor pair j is RR iff slot j is absent, II iff active; hence Q = M = V0 + 2K. Local Q_v is not
  restricted. Admission changes N_c. States outside this sector are rejected explicitly.
  Basis (build_owned_operator only). The STRUCTURAL reachable component of the caller seeds: closure
  under every primitive channel, independent of coefficient values (a zero coefficient still
  connects), sorted by canonical key. Caps fail explicitly before being exceeded; nothing is truncated.
  H (contract s.3), every primitive exposed before aggregation:
    diagonal  Delta n_e (edge owner); Ud (d_v-dstar)^2, -lambda_R d_v q_v, +lambda_J d_v p_v (degree
              owners; full local lambda_J is sum d*p, PRIMARY l.253, never the SECONDARY restored_bs11
              hard-core completion); epsilon_c p_v, epsilon_r q_v, E_R R_v, E_S S_v, E_I I_v (site
              owners; I_v is identically 0 in this inventory); e_R R_D + e_I I_D per donor; C_identity
              once per state (common to every sector; no per-graph/slot/state energy zero).
    flip      n_e -> 1-n_e on every present edge, amplitude -h_e (h_e REAL, ADDENDUM 3 / 0406 item 3).
    hop       only n_e = 1 with p_a != p_b; swap p; q, cells untouched; hard-core exchange, no CAR sign.
    bind      p_v = 1 flips q_v, amplitude +g_v (g_v REAL), any cell including R with p = 1.
    admit     R, p=0 -> S, p=1 with kappa_v; admit_rev S, p=1 -> R, p=0 with conj(kappa_v); q kept.
    birth     forward epsilon_j * B_(G,C,j); birth_rev conj(epsilon_j) * B_(G,C,j)^dagger (s.4 below).
  Birth (contract s.4; LEDGER l.13; GEN l.27-36; CLOC l.7). C_loc(G) is enumerated in the CURRENT
  graph from both bipartition root mirrors: a root's four opposite-part neighbours are exactly the
  cut's opposite endpoints, exactly one cut edge meets the root, the four same-part endpoints are
  distinct. Unordered cuts are deduplicated across witnesses. Channel (G, C, j) exists iff original
  o_j witnesses C, slot j is absent, donors (o_j,0),(o_j,1) are RR and the cut census is exactly two;
  each (G, C, j) once, no multiplicity factor. Surgery deletes the four cut edges (u, v), u in A,
  v in B, adds children (u, b_j) and (a_j, v) each carrying the cut bit, keeps every other factor and
  bit, inserts a_j, b_j in R with p = q = 0, and sends the donor pair RR -> II (loaded map, not the
  PRIMARY blank-I BirthMap.encode l.145). birth_rev at an active slot enumerates all 4! pairings of
  b_j's four A neighbours with a_j's four B neighbours, reconstructs each predecessor and keeps the
  pairing only if the complete forward image holds: no restored edge duplicates a surviving edge,
  paired child bits are equal, census two, a_j and b_j in R with p = q = 0, donors II, and o_j
  witnesses the restored cut in the PREDECESSOR graph (never a fresh target-side test). A failed
  pairing is an exact zero matrix element and produces no record. Native owners act on every state,
  including all reverse-failure states. Coincident destinations remain separate records.
  Supports (contract s.3, V002 support_weights). Each record lists raw anchors as ('vertex', label),
  ('edge', (A label, B label)) or ('donor', (owner label, k)). The energy support of a primitive at
  configuration z is the set of registered anchors of (queried | changed) that are PRESENT at z:
  an edge contributes its two endpoint vertices (plus itself when registration['edge_cells'] is a
  map), a vertex counts if present, a donor factor counts as its declared anchor. Equal weight per
  distinct anchor; w_alphaX(z) = (anchors in cell alpha)/(anchors). Newborn labels count only on a
  side where they exist. C_identity has no anchor and uses registration['identity_allocation'].
  Energy blocks (contract s.5): E_alpha[y,x] = sum_X (w_alphaX(y)+w_alphaX(x))/2 h_X[y,x]; the
  reverse primitive gets the identical symmetric weight, so E_alpha is Hermitian and
  sum_alpha E_alpha = H on every primitive.
  Reads (contract s.5; 0406 item 1; ADDENDUM 1; REGISTER complete_reads). For every vertex label
  (present or not): presence indicator; four presence-masked single-port Z_(v,a) = 1-2 n_(e_a); six
  pair reads Z_a Z_b; ports ordered by the caller's deterministic registration['port_order'] on the
  CURRENT neighbours. Per coarse cell alpha: population m_alpha (present vertices, newborns in their
  owner's cell), R_alpha,i = (1/m_alpha) sum_v t_vi, S_alpha,ij = (1/m_alpha) sum_v t_vi t_vj with
  t_v = sum_a Z_va port_vectors[a] and 1/m_alpha a current-state factor inside the operator. Absent
  rows have value 0 and presence 0 (no conditional normalization). Raw first and second moments are
  separate rows; centring (C = M - mu mu^T) is a caller-side combination.

PHASE CONVENTION. For stable edge (a, b), a in A, b in B, the carrier transfer b -> a has amplitude
  -t_e exp(+i theta_e) and a -> b has -t_e exp(-i theta_e), its exact conjugate. This is the PRIMARY
  CanonicalJoin convention (canonical_join_backend_v002.py l.249 docstring "v->u has +theta",
  l.259-261, with edges (u in A, v in B) as in periodic_q4 l.92). The ADDITIONAL one-carrier code
  (root_native_shared_parent_clock_transport_v001.py l.77-79) gives +theta to A -> B; the contract
  binds the PRIMARY convention, so the two differ by theta -> -theta. theta_e, t_e, h_e are keyed
  by the current (A label, B label) pair; zero phase is never inferred.

SCOPE. Module A only: validated model/context, canonical keys, state-level primitive channels,
  diagonal terms and reads (for samplers that never enumerate a basis), structural basis
  enumeration with caps, matrix-free apply_H / apply_E / apply_O, read arrays, norm bounds,
  resources, and the optional DECLARED reference family. No propagation, response contraction,
  Legendre step, P/Q reduction, time derivative or physical state choice (module B / root).

PUBLIC API (all keyword-only, no defaults; state-level functions raise ValueError on bad input)
  validate_owned_model(*, graph0, model, registration) -> {ok, stage_reached, failures, context}
  canonical_state_key(*, context, state) -> (slots, edgeset, inc, p, q, s, donors) ints
  state_labels(*, context, state) -> labelled history-free pairs (dict() gives a state mapping)
  primitive_channels(*, context, state) -> [record(owner_id, kind, target_state, amplitude,
      queried_support, changed_support, energy_weights)]; kind in diag, flip, hop, bind, admit,
      admit_rev, birth, birth_rev; target_state canonical key (None for diag); energy_weights a
      tuple over context.energy_cells of (w_alphaX(target) + w_alphaX(source))/2.
  diagonal_terms(*, context, state) -> the kind == 'diag' records of primitive_channels
  read_rows(*, context, state) -> {labels, values float64 [n_read], presence float64 [n_read]}
  build_owned_operator(*, graph0, model, registration, seed_states, caps, dtype)
      -> {ok, stage_reached, failures, operator, resources}; operator members: dimension, dtype,
      energy_cells, read_labels, context, basis_key(*, index), index_of(*, key),
      primitive_events(*, index), apply_H(*, block), apply_E(*, alpha, block), read_values(),
      read_presence(), apply_O(*, read_index, block), norm_bound_H(), norm_bound_E(*, alpha),
      resources(), reference_preparation(*, chi, ice_factor).
  The operator is assembled from exactly the same internal functions as primitive_channels,
  diagonal_terms and read_rows (one source of truth).

COST. Exponential. Per basis row: at most 2V flips, 2V hops, V binds, V admissions and (contract
  s.11) conservatively 132K Birth/reverse channels, plus the diagonal owners; sparse action is
  O(D(1+6Vmax+132K)) with Vmax = 3V0, plus registration cost. The G0 block of the declared sector
  alone has 2^(3V0) * C(2V0, V0) states (all incidence words times local states with N_c = S_g);
  for the smallest simple q4 bipartite graph (V0 = 8) that is about 2.2e11. A full build therefore
  exceeds any practical cap; build_owned_operator reports this and fails at the cap. The state-level
  functions cost O(V + 108V + 24K) per call plus a one-off per-graph structure.

LIMITATIONS: see the module constant LIMITATIONS (each ambiguity is implemented literally and listed).
"""

import cmath
import math
import sys
from array import array
from collections.abc import Mapping
from itertools import permutations, product
from typing import NamedTuple

import numpy as np


LIMITATIONS = """\
L1  Edge anchors. Contract s.3 says the Delta edge owner "queries its endpoints/edge"; V002 counts
    "graph vertex or graph-attached resource anchor"; the adopted register spec gives cells only to
    vertex labels. The caller declares registration['edge_cells']: 'endpoint_anchors_only' (an edge
    variable is attributed to its two endpoint vertex anchors) or a map (A,B)->cell (the edge is an
    additional anchor, endpoints still counted). Weights differ between the two; neither is chosen here.
L2  Donor anchors. REGISTER: newborn labels inherit the owner's cell and "its donors use that same
    anchor". The caller declares registration['donor_anchor']: 'owner_vertex' (each donor factor is
    the owner vertex anchor, counted once with it) or 'separate_at_owner_cell' (each donor factor is
    its own anchor in the owner's cell). Newborn cells are DERIVED from the owner cell (REGISTER) and
    cannot be registered separately in this version.
L3  Degree-feedback support. Ud, lambda_R and lambda_J owners at v support v plus its four incident
    edges (hence its four neighbours as endpoints), reading contract s.3 "incident-edge/endpoint
    anchors it queries". Birth support uses only the owner's own root o_j adjacency (the guard of
    channel (C,j)); other witnesses of the same cut are not queried by that channel.
L4  Inventory. The key encodes M_v=1 on present sites; an ambient I-cell domain is not implemented
    (E_I is retained in the model and contributes 0). The declared sector N_c=S_graph with donors
    fixed by slot occupancy is enforced; other invariant sectors are rejected, not silently admitted.
L5  Profiles. epsilon_j per owner slot and t_e per edge generalize the sources' displayed uniform
    epsilon and t (GEN l.40; DOMAIN l.9); the uniform member is the caller's equal values. The phase
    rule on newborn/child edges is UNCHOSEN in the sources (0400 row 4, check E2); it is caller data
    keyed by the current (A,B) pair. The many-carrier matrix of T_e(theta != 0) is NOT WRITTEN in the
    sources (0400 row 2 (ii)); the edge-local hard-core exchange with the PRIMARY one-carrier phase
    entry is implemented, as the contract binds.
L6  Hop orientation follows the PRIMARY backend; the ADDITIONAL one-carrier reference has the
    opposite sign of theta. Records do not carry a hop direction; it is implied by the target.
L7  Reference family. reference_preparation computes chi as the unique ground vector of the
    four-state local block H(2) on {R p0 q0, R p0 q1, S p1 q0, S p1 q1} at d=2 (admission kappa_v,
    Bind g_v, exact r2 = epsilon_r - 2 lambda_R), from the review record "complete four-state H(2)"
    and consistent with the analytic control in the galaxy assembly note (l.522). If the declared
    full local H(2) is meant to contain more, pass chi explicitly. The family is a DECLARED reference,
    never a default state; a degenerate ground fails.
L8  Ports. Port order is a caller callable of (current vertex label, current neighbour labels); it
    must be deterministic. Results are cached per (vertex, neighbour set); release_caches() drops
    the cache, after which a nondeterministic callable would change reads. The tetrahedral frame
    table is registration['port_vectors']; the exact bound tr C <= 4 (||t_v||^2 = 4-(d_v-2)^2) holds
    for the REGISTER table (+-1/2 rows) and is a documented property, never a clip.
L9  Reads. Retained loop/count reads of the collective action are not implemented (additional outputs,
    not requested here). Read values are float64. Native-time first/second derivatives of reads and
    any K' generator terms (ADDENDUM 1) belong to module B.
L10 Numerics. Amplitudes and weights are float64 Python values, then cast to the caller dtype for
    apply_*. norm_bound_* bound the STORED matrix (absolute column sums with an explicit summation
    inflation); rounding of stored coefficients relative to exact model values and matvec rounding
    are not covered here. Build integrity checks (Hermiticity of H and every E_alpha, sum_alpha
    E_alpha = H) use summation tolerances; they are internal consistency checks, not validation.
L11 No compression, Krylov, P/Q reduction or memory kernel. The full basis is exponential (see COST);
    state-level functions are the route for samplers. Context caches grow with the number of distinct
    supporting graphs visited; the caller bounds memory with release_caches().
L12 primitive_channels lists diagonal owners only where their operator element is structurally
    nonzero (e.g. epsilon_r only at q_v=1); failed Birth-reverse pairings and other exact zeros
    produce no record. Coefficient VALUES never remove a record (a zero coefficient gives amplitude 0).
"""


class _Channel(NamedTuple):
    owner_id: tuple
    kind: str
    target_state: object
    amplitude: complex
    queried_support: tuple
    changed_support: tuple
    energy_weights: tuple


class _IndexedEvent(NamedTuple):
    owner_id: tuple
    kind: str
    source_index: int
    target_index: int
    amplitude: complex
    queried_support: tuple
    changed_support: tuple
    energy_weights: tuple


class _Stop(Exception):
    """Internal: a declared cap or an inconsistency stops enumeration (fail closed)."""


_SCALAR_KEYS = ("Delta", "Ud", "dstar", "epsilon_c", "epsilon_r", "lambda_R", "lambda_J",
                "E_R", "E_S", "E_I", "e_R", "e_I", "C_identity")
_PROFILE_KEYS = ("h", "t", "theta", "g", "kappa", "epsilon")
_REGISTRATION_KEYS = ("cells", "original_cell", "edge_cells", "donor_anchor",
                      "identity_allocation", "port_order", "port_vectors")
_CAP_KEYS = ("max_dimension", "max_graphs", "max_events_per_row")
_STATE_KEYS = ("slots", "edges", "occupied", "carriers", "records", "spent", "donors_ready")
_EDGE_ENDPOINTS_ONLY = "endpoint_anchors_only"
_DONOR_MODES = ("owner_vertex", "separate_at_owner_cell")
_REGISTER_SPEC_PORT_VECTORS = ((0.5, 0.5, 0.5), (0.5, -0.5, -0.5),
                               (-0.5, 0.5, -0.5), (-0.5, -0.5, 0.5))
_PAIRS = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
_SYM3 = ((0, 0), (0, 1), (0, 2), (1, 1), (1, 2), (2, 2))
_CHI_FROM_H2 = "ground_of_declared_local_H2"
_FAMILY = {"flip": "flip", "hop": "hop", "bind": "bind", "admit": "admission",
           "admit_rev": "admission", "birth": "birth", "birth_rev": "birth"}


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------

def _popcount(x):
    # SECONDARY l.49 count(): bin(mask).count('1') (Python 3.9 has no int.bit_count).
    return bin(x).count("1")


def _bits(x):
    """Ascending positions of the set bits of a nonnegative int."""
    out = []
    while x:
        low = x & -x
        out.append(low.bit_length() - 1)
        x ^= low
    return out


def _is_label(x):
    return isinstance(x, (int, str)) and not isinstance(x, bool)


def _keyset(name, mapping, required, failures):
    keys = list(mapping.keys())
    missing = [k for k in required if k not in mapping]
    unknown = [repr(k) for k in keys if k not in required]
    if missing:
        failures.append(f"{name}: missing required keys {missing} (no defaults)")
    if unknown:
        failures.append(f"{name}: unknown keys {unknown} (nothing is ignored)")
    return not missing and not unknown


def _real(name, value, failures):
    # Admission style follows scalar_metric_particular_solve_v002.py _real_input.
    if isinstance(value, (bool, np.bool_)):
        failures.append(f"{name}: a boolean is not an admitted real scalar")
        return None
    if isinstance(value, (complex, np.complexfloating)):
        failures.append(f"{name}: complex value {value!r} rejected; this coefficient must be real")
        return None
    if not isinstance(value, (int, float, np.integer, np.floating)):
        failures.append(f"{name}: type {type(value).__name__} is not an admitted real scalar")
        return None
    try:
        out = float(value)
    except (OverflowError, ValueError, TypeError):
        failures.append(f"{name}: not representable as a float64 value")
        return None
    if not math.isfinite(out):
        failures.append(f"{name}: not finite ({out!r})")
        return None
    return out


def _complex(name, value, failures):
    if isinstance(value, (bool, np.bool_)):
        failures.append(f"{name}: a boolean is not an admitted complex scalar")
        return None
    if not isinstance(value, (int, float, complex, np.integer, np.floating, np.complexfloating)):
        failures.append(f"{name}: type {type(value).__name__} is not an admitted complex scalar")
        return None
    try:
        out = complex(value)
    except (OverflowError, ValueError, TypeError):
        failures.append(f"{name}: not representable as a complex128 value")
        return None
    if not (math.isfinite(out.real) and math.isfinite(out.imag)):
        failures.append(f"{name}: not finite ({out!r})")
        return None
    return out


def _edge_ends(dom, c):
    return c // dom["NB"], dom["NA"] + c % dom["NB"]


def _code(dom, a, b):
    return a * dom["NB"] + (b - dom["NA"])


def _code_any(dom, x, y):
    return _code(dom, x, y) if x < dom["NA"] else _code(dom, y, x)


def _edge_from_labels(dom, pair):
    """Stable edge code of an ORDERED bipartite pair (A label, B label), else None."""
    if not isinstance(pair, (list, tuple)) or len(pair) != 2:
        return None
    x, y = pair[0], pair[1]
    if not (_is_label(x) and _is_label(y)):
        return None
    vx = dom["vid"].get(x)
    vy = dom["vid"].get(y)
    if vx is None or vy is None or not (vx < dom["NA"] <= vy):
        return None
    return _code(dom, vx, vy)


def _edge_labels(dom, c):
    a, b = _edge_ends(dom, c)
    return (dom["labels"][a], dom["labels"][b])


def _eps_of(dtype):
    """Unit roundoff scale of a numeric dtype (float64 for integer inputs)."""
    return float(np.finfo(dtype).eps) if np.dtype(dtype).kind in "fc" else float(np.finfo(np.float64).eps)


def _np_buffer(buf, dtype):
    """numpy view of an array.array buffer (empty-safe)."""
    return np.frombuffer(buf, dtype=dtype) if len(buf) else np.zeros(0, dtype=dtype)


def _vertex_present(dom, edgeset, v):
    j = dom["newborn_slot"].get(v)
    return True if j is None else bool(edgeset & dom["newborn_edge_mask"][v])


# ---------------------------------------------------------------------------
# Admission of graph0, model and registration
# ---------------------------------------------------------------------------

def _admit_graph0(graph0, failures):
    if not isinstance(graph0, Mapping):
        failures.append("graph0: a mapping with keys 'A', 'B', 'edges', 'slots' is required")
        return None
    if not _keyset("graph0", graph0, ("A", "B", "edges", "slots"), failures):
        return None
    part_a, part_b = graph0["A"], graph0["B"]
    for name, part in (("A", part_a), ("B", part_b)):
        if not isinstance(part, (list, tuple)) or len(part) == 0:
            failures.append(f"graph0['{name}']: a nonempty list or tuple of vertex labels is required")
        elif not all(_is_label(x) for x in part):
            failures.append(f"graph0['{name}']: every vertex label must be an int or a str (not bool)")
    if failures:
        return None
    originals = list(part_a) + list(part_b)
    if len(set(originals)) != len(originals):
        failures.append("graph0: original vertex labels must be distinct across A and B")
        return None
    slots = graph0["slots"]
    if not isinstance(slots, Mapping):
        failures.append("graph0['slots']: a mapping original label -> (a_j, b_j) is required")
        return None
    owner_set = set(originals)
    missing = [o for o in originals if o not in slots]
    unknown = [repr(k) for k in slots if not (_is_label(k) and k in owner_set)]
    if missing:
        failures.append(f"graph0['slots']: no slot declared for original vertices {missing!r} (K = V0)")
    if unknown:
        failures.append(f"graph0['slots']: keys {unknown} are not original vertex labels")
    if failures:
        return None
    a_new, b_new = [], []
    for o in originals:
        pair = slots[o]
        if not isinstance(pair, (list, tuple)) or len(pair) != 2 or not all(_is_label(x) for x in pair):
            failures.append(f"graph0['slots'][{o!r}]: a pair (a_j label, b_j label) is required")
            continue
        a_new.append(pair[0])
        b_new.append(pair[1])
    if failures:
        return None
    every = originals + a_new + b_new
    if len(set(every)) != len(every):
        failures.append("graph0['slots']: newborn labels must be distinct from each other and from originals")
        return None
    n_a0, n_b0, k_slots = len(part_a), len(part_b), len(originals)
    na, nb = n_a0 + k_slots, n_b0 + k_slots
    labels = list(part_a) + a_new + list(part_b) + b_new
    owner_vid = [j if j < n_a0 else na + (j - n_a0) for j in range(k_slots)]
    a_vid = [n_a0 + j for j in range(k_slots)]
    b_vid = [na + n_b0 + j for j in range(k_slots)]
    newborn_slot = {}
    newborn_edge_mask = {}
    for j in range(k_slots):
        newborn_slot[a_vid[j]] = j
        newborn_slot[b_vid[j]] = j
        newborn_edge_mask[a_vid[j]] = ((1 << nb) - 1) << (a_vid[j] * nb)
        mask = 0
        for ia in range(na):
            mask |= 1 << (ia * nb + (b_vid[j] - na))
        newborn_edge_mask[b_vid[j]] = mask
    label_order = list(owner_vid)
    for j in range(k_slots):
        label_order.extend((a_vid[j], b_vid[j]))
    dom = {
        "labels": labels, "vid": {lab: i for i, lab in enumerate(labels)},
        "NA": na, "NB": nb, "NV": na + nb, "nA0": n_a0, "nB0": n_b0,
        "V0": k_slots, "K": k_slots, "owners": originals,
        "owner_index": {o: j for j, o in enumerate(originals)},
        "owner_vid": owner_vid, "owner_of_original": {v: j for j, v in enumerate(owner_vid)},
        "a_vid": a_vid, "b_vid": b_vid, "newborn_slot": newborn_slot,
        "newborn_edge_mask": newborn_edge_mask, "label_order": label_order,
    }
    edges = graph0["edges"]
    if not isinstance(edges, (list, tuple)):
        failures.append("graph0['edges']: a list or tuple of (A label, B label) pairs is required")
        return None
    edgeset0 = 0
    degree = [0] * dom["NV"]
    for e in edges:
        c = _edge_from_labels(dom, e)
        if c is None:
            failures.append(f"graph0['edges']: {e!r} is not an ordered bipartite pair (A label, B label)")
            continue
        a, b = _edge_ends(dom, c)
        if a in newborn_slot or b in newborn_slot:
            failures.append(f"graph0['edges']: {e!r} touches a newborn label; G0 has original vertices only")
            continue
        if (edgeset0 >> c) & 1:
            failures.append(f"graph0['edges']: duplicate edge {e!r}; the supporting graph must be simple")
            continue
        edgeset0 |= 1 << c
        degree[a] += 1
        degree[b] += 1
    bad = [labels[v] for v in owner_vid if degree[v] != 4]
    if bad:
        failures.append(f"graph0: original vertices without degree four: {bad!r}")
    if failures:
        return None
    dom["edgeset0"] = edgeset0
    return dom


def _edge_table(dom, name, table, failures, flip_note):
    if not isinstance(table, Mapping):
        failures.append(f"{name}: a mapping (A label, B label) -> real is required")
        return {}
    out = {}
    for key, value in table.items():
        c = _edge_from_labels(dom, key)
        if c is None:
            failures.append(f"{name}: key {key!r} is not an ordered bipartite pair (A label, B label) "
                            "of declared vertex labels")
            continue
        if flip_note and isinstance(value, (complex, np.complexfloating)):
            failures.append(f"{name}[{key!r}]: complex flip coefficient {value!r} rejected (0406 item 3; "
                            "ADDENDUM 3): -h_e X_e is Hermitian only for real h_e and a complex value is "
                            "never copied to both directions")
            continue
        x = _real(f"{name}[{key!r}]", value, failures)
        if x is not None:
            out[c] = x
    return out


def _vertex_table(dom, name, table, failures, kind):
    if not isinstance(table, Mapping):
        failures.append(f"{name}: a mapping vertex label -> value covering every vertex label is required")
        return {}
    out = {}
    for key, value in table.items():
        v = dom["vid"].get(key) if _is_label(key) else None
        if v is None:
            failures.append(f"{name}: key {key!r} is not a declared vertex label")
            continue
        if kind == "bind" and isinstance(value, (complex, np.complexfloating)):
            failures.append(f"{name}[{key!r}]: complex Bind coefficient {value!r} rejected (0406 item 3; "
                            "ADDENDUM 3): +g_v p_v X_q is Hermitian only for real g_v")
            continue
        x = _complex(f"{name}[{key!r}]", value, failures) if kind == "complex" else \
            _real(f"{name}[{key!r}]", value, failures)
        if x is not None:
            out[v] = x
    missing = [dom["labels"][v] for v in range(dom["NV"]) if v not in out]
    if missing:
        failures.append(f"{name}: no value for vertex labels {missing!r} (every vertex that can appear, "
                        "originals and newborns, needs an explicit value; no default)")
    return out


def _admit_model(dom, model, failures):
    if not isinstance(model, Mapping):
        failures.append("model: a mapping of explicit coefficients and profiles is required")
        return None
    if not _keyset("model", model, _SCALAR_KEYS + _PROFILE_KEYS, failures):
        return None
    out = {}
    for k in _SCALAR_KEYS:
        out[k] = _real(f"model['{k}']", model[k], failures)
    out["h"] = _edge_table(dom, "model['h']", model["h"], failures, True)
    out["t"] = _edge_table(dom, "model['t']", model["t"], failures, False)
    out["theta"] = _edge_table(dom, "model['theta']", model["theta"], failures, False)
    out["g"] = _vertex_table(dom, "model['g']", model["g"], failures, "bind")
    out["kappa"] = _vertex_table(dom, "model['kappa']", model["kappa"], failures, "complex")
    eps_in = model["epsilon"]
    eps = {}
    if not isinstance(eps_in, Mapping):
        failures.append("model['epsilon']: a mapping owner label -> complex epsilon_j is required")
    else:
        for key, value in eps_in.items():
            j = dom["owner_index"].get(key) if _is_label(key) else None
            if j is None:
                failures.append(f"model['epsilon']: key {key!r} is not an original owner label")
                continue
            z = _complex(f"model['epsilon'][{key!r}]", value, failures)
            if z is not None:
                eps[j] = z
        missing = [dom["owners"][j] for j in range(dom["K"]) if j not in eps]
        if missing:
            failures.append(f"model['epsilon']: no Birth amplitude for owner slots {missing!r} (no default)")
    out["epsilon"] = eps
    if failures:
        return None
    # Oriented hop amplitude b -> a (PRIMARY l.259-261 convention, see module docstring).
    out["hop_BA"] = {c: -out["t"][c] * cmath.exp(1j * out["theta"][c])
                     for c in out["t"] if c in out["theta"]}
    return out


def _admit_registration(dom, registration, failures):
    if not isinstance(registration, Mapping):
        failures.append("registration: a mapping is required")
        return None
    if not _keyset("registration", registration, _REGISTRATION_KEYS, failures):
        return None
    cells = registration["cells"]
    if not isinstance(cells, (list, tuple)) or len(cells) == 0:
        failures.append("registration['cells']: a nonempty ordered list or tuple of cell labels is required")
        return None
    try:
        cell_index = {}
        for i, c in enumerate(cells):
            if c in cell_index:
                failures.append(f"registration['cells']: duplicate cell label {c!r}")
            cell_index[c] = i
    except TypeError:
        failures.append("registration['cells']: cell labels must be hashable")
        return None
    if failures:
        return None
    oc = registration["original_cell"]
    cell_vid = [None] * dom["NV"]
    if not isinstance(oc, Mapping):
        failures.append("registration['original_cell']: a mapping original label -> cell is required")
        return None
    for key, value in oc.items():
        j = dom["owner_index"].get(key) if _is_label(key) else None
        if j is None:
            failures.append(f"registration['original_cell']: key {key!r} is not an original vertex label")
            continue
        try:
            alpha = cell_index.get(value)
        except TypeError:
            alpha = None
        if alpha is None:
            failures.append(f"registration['original_cell'][{key!r}]: {value!r} is not a declared cell")
            continue
        cell_vid[dom["owner_vid"][j]] = alpha
    missing = [dom["owners"][j] for j in range(dom["K"]) if cell_vid[dom["owner_vid"][j]] is None]
    if missing:
        failures.append(f"registration['original_cell']: no cell for original vertices {missing!r}")
    if failures:
        return None
    # REGISTER coarse_register.cells: newborn labels inherit the owner's cell (current-state anchor,
    # no genealogy); donors use that same anchor/cell.
    for j in range(dom["K"]):
        cell_vid[dom["a_vid"][j]] = cell_vid[dom["owner_vid"][j]]
        cell_vid[dom["b_vid"][j]] = cell_vid[dom["owner_vid"][j]]
    empty = [cells[a] for a in range(len(cells))
             if not any(cell_vid[v] == a for v in dom["owner_vid"])]
    if empty:
        failures.append(f"registration['cells']: cells {empty!r} contain no original vertex "
                        "(REGISTER: nonempty cells partitioning the original-owner labels)")
    ec = registration["edge_cells"]
    edge_cell = {}
    if isinstance(ec, str):
        if ec != _EDGE_ENDPOINTS_ONLY:
            failures.append(f"registration['edge_cells']: {ec!r} is neither {_EDGE_ENDPOINTS_ONLY!r} nor a map")
        edge_mode = False
    elif isinstance(ec, Mapping):
        edge_mode = True
        for key, value in ec.items():
            c = _edge_from_labels(dom, key)
            try:
                alpha = cell_index.get(value)
            except TypeError:
                alpha = None
            if c is None or alpha is None:
                failures.append(f"registration['edge_cells']: entry {key!r} -> {value!r} is not "
                                "(ordered (A label, B label) pair) -> declared cell")
                continue
            edge_cell[c] = alpha
    else:
        failures.append(f"registration['edge_cells']: {_EDGE_ENDPOINTS_ONLY!r} or a map is required")
        edge_mode = False
    donor_mode = registration["donor_anchor"]
    if not (isinstance(donor_mode, str) and donor_mode in _DONOR_MODES):
        failures.append(f"registration['donor_anchor']: one of {_DONOR_MODES!r} is required")
    ia = registration["identity_allocation"]
    identity = ()
    if not isinstance(ia, Mapping):
        failures.append("registration['identity_allocation']: a mapping cell -> fraction is required "
                        "(C_identity has no anchor; V002 requires an explicit allocation)")
    else:
        fr = {}
        for key, value in ia.items():
            try:
                alpha = cell_index.get(key)
            except TypeError:
                alpha = None
            if alpha is None:
                failures.append(f"registration['identity_allocation']: {key!r} is not a declared cell")
                continue
            x = _real(f"registration['identity_allocation'][{key!r}]", value, failures)
            if x is not None:
                if x < 0.0:
                    failures.append(f"registration['identity_allocation'][{key!r}]: negative fraction {x!r}")
                fr[alpha] = x
        if fr and not abs(math.fsum(fr.values()) - 1.0) <= 1e-12:
            failures.append("registration['identity_allocation']: fractions must sum to 1 "
                            f"(|sum-1| <= 1e-12); got {math.fsum(fr.values())!r}")
        if not fr:
            failures.append("registration['identity_allocation']: at least one cell fraction is required")
        identity = tuple((a, fr[a]) for a in sorted(fr) if fr[a] != 0.0)
    if not callable(registration["port_order"]):
        failures.append("registration['port_order']: a callable port_order(*, vertex, neighbours) is required")
    pv_in = None
    if isinstance(registration["port_vectors"], (list, tuple, np.ndarray)):
        try:
            pv_in = np.asarray(registration["port_vectors"])
        except (TypeError, ValueError):
            pv_in = None
    pv = None
    if pv_in is None or pv_in.dtype.kind not in "iuf" or pv_in.shape != (4, 3):
        failures.append("registration['port_vectors']: a real 4x3 tetrahedral frame table is required")
    else:
        pv = pv_in.astype(np.float64)
        if not np.all(np.isfinite(pv)):
            failures.append("registration['port_vectors']: entries must be finite")
    if failures:
        return None
    cell_vids = [np.array([v for v in dom["label_order"] if cell_vid[v] == a], dtype=np.int64)
                 for a in range(len(cells))]
    return {
        "cells": tuple(cells), "cell_index": cell_index, "cell_vid": cell_vid,
        "edge_mode": edge_mode, "edge_cell": edge_cell, "donor_mode": donor_mode,
        "identity": identity, "port_order": registration["port_order"], "port_vectors": pv,
        "port_vectors_equal_register_spec": bool(np.array_equal(pv, np.array(_REGISTER_SPEC_PORT_VECTORS))),
        "w_site": [((cell_vid[v], 1.0),) for v in range(dom["NV"])],
        "w_donor": [((cell_vid[dom["owner_vid"][d // 2]], 1.0),) for d in range(2 * dom["K"])],
        "cell_vids": cell_vids,
    }


def _read_layout(dom, reg):
    """Typed read labels and their internal specs (same order everywhere)."""
    labels, specs = [], []
    cells = reg["cells"]
    for v in dom["label_order"]:
        lab = dom["labels"][v]
        cell = cells[reg["cell_vid"][v]]
        labels.append(("vertex_presence", lab, cell))
        specs.append(("P", v))
        for a in range(4):
            labels.append(("first_moment_Z", lab, a, cell))
            specs.append(("Z", v, a))
        for a, b in _PAIRS:
            labels.append(("pair_ZZ", lab, a, b, cell))
            specs.append(("ZZ", v, a, b))
    for alpha, cell in enumerate(cells):
        labels.append(("coarse_population_m", cell))
        specs.append(("m", alpha))
        for i in range(3):
            labels.append(("coarse_first_R", cell, i))
            specs.append(("R", alpha, i))
        for i, j in _SYM3:
            labels.append(("coarse_second_S", cell, i, j))
            specs.append(("S", alpha, i, j))
    return tuple(labels), tuple(specs)


class OwnedModelContext:
    """Validated graph0 / model / registration plus per-graph structural caches.

    Built by validate_owned_model. Attributes: energy_cells (ordered cell labels), read_labels
    (typed read rows), vertex_labels, owners. Caches are pure functions of the validated inputs
    and the current graph; release_caches() drops them (see LIMITATIONS L8, L11).
    """

    def __init__(self, *, dom, model, reg):
        self._dom = dom
        self._model = model
        self._reg = reg
        self.energy_cells = reg["cells"]
        self.vertex_labels = tuple(dom["labels"])
        self.owners = tuple(dom["owners"])
        self.read_labels, self._read_spec = _read_layout(dom, reg)
        self._infos = {}
        self._ports = {}

    def release_caches(self):
        """Drop cached per-graph structure and port orders; they are rebuilt on demand."""
        self._infos = {}
        self._ports = {}


def validate_owned_model(*, graph0, model, registration):
    """Validate the explicit owned-parent inputs once; return a fail-closed result dict.

    graph0: {'A': [...], 'B': [...], 'edges': [(A label, B label), ...],
             'slots': {original label: (a_j label, b_j label)}}  -- simple bipartite q4, K = V0.
    model: real Delta, Ud, dstar, epsilon_c, epsilon_r, lambda_R, lambda_J, E_R, E_S, E_I, e_R,
           e_I, C_identity; 'h', 't', 'theta': {(A label, B label): real} (h real; coverage of
           every edge that occurs is checked when a graph containing it is met); 'g': {vertex:
           real}, 'kappa': {vertex: complex} for EVERY vertex label; 'epsilon': {owner: complex}.
    registration: 'cells' (ordered labels), 'original_cell' {original: cell}, 'edge_cells'
           ('endpoint_anchors_only' or {(A,B): cell}), 'donor_anchor' ('owner_vertex' or
           'separate_at_owner_cell'), 'identity_allocation' {cell: fraction, sum 1},
           'port_order' callable(*, vertex, neighbours) -> ordered neighbour labels,
           'port_vectors' real 4x3 frame table.
    Returns {'ok', 'stage_reached', 'failures', 'context'}; context is an OwnedModelContext.
    """
    result = {"ok": False, "stage_reached": "inputs", "failures": [], "context": None}
    failures = result["failures"]
    dom = _admit_graph0(graph0, failures)
    if dom is None or failures:
        return result
    mod = _admit_model(dom, model, failures)
    reg = _admit_registration(dom, registration, failures)
    if failures or mod is None or reg is None:
        return result
    result["context"] = OwnedModelContext(dom=dom, model=mod, reg=reg)
    result["ok"] = True
    result["stage_reached"] = "complete"
    return result


# ---------------------------------------------------------------------------
# Current-graph structure: ports, C_loc, forward and reverse Birth channels
# ---------------------------------------------------------------------------

def _port_order(ctx, v, nbr):
    key = (v, nbr)
    hit = ctx._ports.get(key)
    if hit is not None:
        return hit
    labels = ctx._dom["labels"]
    shown = tuple(labels[w] for w in nbr)
    try:
        got = ctx._reg["port_order"](vertex=labels[v], neighbours=shown)
    except Exception as exc:  # a caller registration failure becomes an explicit failure
        raise ValueError(f"registration['port_order'] raised {type(exc).__name__} ({exc}) "
                         f"for vertex {labels[v]!r}") from exc
    ids = None
    if isinstance(got, (list, tuple)) and len(got) == 4:
        ids = [ctx._dom["vid"].get(x) if _is_label(x) else None for x in got]
        if None in ids or tuple(sorted(ids)) != nbr:
            ids = None
    if ids is None:
        raise ValueError(f"registration['port_order'] for vertex {labels[v]!r} returned {got!r}, "
                         f"not an ordering of its current neighbours {shown!r}")
    out = tuple(ids)
    ctx._ports[key] = out
    return out


def _c_loc(dom, nbrs):
    """C_loc(G) of the CURRENT graph (CLOC l.7; LEDGER l.13): cut -> witnessing roots.

    For every root (both bipartition mirrors) and every choice of the root's single cut edge,
    each other neighbour x is matched to a neighbour of x other than the root, with distinct
    endpoints. Unordered cuts are deduplicated across all witnesses and orientations.
    """
    out = {}
    for root in nbrs:
        rn = nbrs[root]
        for k in range(4):
            others = [rn[i] for i in range(4) if i != k]
            cands = [[w for w in nbrs[x] if w != root] for x in others]
            for ch in product(*cands):
                if ch[0] == ch[1] or ch[0] == ch[2] or ch[1] == ch[2]:
                    continue
                cut = [_code_any(dom, root, rn[k])]
                for i in range(3):
                    cut.append(_code_any(dom, ch[i], others[i]))
                out.setdefault(tuple(sorted(cut)), set()).add(root)
    return {cut: tuple(sorted(w)) for cut, w in out.items()}


def _forward_channels(dom, info):
    """Owned Birth channels (G, C, j): C in C_loc(G), original o_j a witness, slot j absent."""
    out = []
    edgeset = info["edgeset"]
    cl = _c_loc(dom, info["nbrs"])
    for cut in sorted(cl):
        for root in cl[cut]:
            j = dom["owner_of_original"].get(root)
            if j is None or (info["slots_mask"] >> j) & 1:
                continue
            a_new, b_new = dom["a_vid"][j], dom["b_vid"][j]
            cutmask = 0
            children = []
            child_codes = []
            for c in cut:
                u, v = _edge_ends(dom, c)
                cu, cv = _code(dom, u, b_new), _code(dom, a_new, v)
                cutmask |= 1 << c
                # Copy the cut bit to BOTH children (PRIMARY BirthMap.encode_incidence l.130-136,
                # here with loaded Ready newborns and owned donors, GEN l.31-34).
                children.append((1 << c, (1 << cu) | (1 << cv)))
                child_codes.extend((cu, cv))
            target = edgeset & ~cutmask
            for _bit, cmask in children:
                target |= cmask
            root_other = tuple(c for c in info["port_codes"][root] if c not in cut)
            out.append({
                "j": j, "cut": cut, "cutmask": cutmask, "children": tuple(children),
                "child_edges": tuple(child_codes), "root_other": root_other,
                "target_edgeset": target,
                "raw_edges": tuple(sorted(set(cut) | set(root_other) | set(child_codes))),
                "c": None,
            })
    return out


def _reverse_channels(dom, info):
    """Every candidate predecessor reconnection of every active slot with its graph-level tests.

    State-level tests (child bits, census, newborn Ready p=q=0, donors II) are in _transitions.
    """
    out = []
    edgeset = info["edgeset"]
    nbrs = info["nbrs"]
    na = dom["NA"]
    for j in _bits(info["slots_mask"]):
        a_new, b_new = dom["a_vid"][j], dom["b_vid"][j]
        u_side = nbrs[b_new]
        v_side = nbrs[a_new]
        if a_new in u_side:
            continue  # a_j adjacent to b_j: no predecessor of the loaded map exists
        star_ub = tuple(_code(dom, u, b_new) for u in u_side)
        star_av = tuple(_code(dom, a_new, v) for v in v_side)
        starmask = 0
        for c in star_ub + star_av:
            starmask |= 1 << c
        o = dom["owner_vid"][j]
        o_nbrs = nbrs[o]
        for sigma in permutations(range(4)):
            restored = tuple(_code(dom, u_side[i], v_side[sigma[i]]) for i in range(4))
            if any((edgeset >> c) & 1 for c in restored):
                continue  # duplicate old edge: zero
            if o < na:
                if o not in u_side:
                    continue  # owner not a cut endpoint: no witness
                i0 = u_side.index(o)
                pred = (set(o_nbrs) - {b_new}) | {v_side[sigma[i0]]}
                if pred != set(v_side):
                    continue
                root_other = tuple(_code(dom, o, w) for w in o_nbrs if w != b_new)
            else:
                if o not in v_side:
                    continue
                i0 = sigma.index(v_side.index(o))
                pred = (set(o_nbrs) - {a_new}) | {u_side[i0]}
                if pred != set(u_side):
                    continue
                root_other = tuple(_code(dom, u, o) for u in o_nbrs if u != a_new)
            restmask = 0
            for c in restored:
                restmask |= 1 << c
            pairs = tuple((star_ub[i], star_av[sigma[i]], restored[i]) for i in range(4))
            child = tuple(sorted(star_ub + star_av))
            out.append({
                "j": j, "cut": tuple(sorted(restored)), "pairs": pairs, "starmask": starmask,
                "child_edges": child, "root_other": root_other,
                "target_edgeset": (edgeset & ~starmask) | restmask,
                "newborn_mask": (1 << a_new) | (1 << b_new),
                "raw_edges": tuple(sorted(set(restored) | set(root_other) | set(child))),
                "c": None,
            })
    return out


def _graph_info(ctx, edgeset):
    dom, mod, reg = ctx._dom, ctx._model, ctx._reg
    labels = dom["labels"]
    codes = _bits(edgeset)
    nb = {}
    for c in codes:
        a, b = _edge_ends(dom, c)
        nb.setdefault(a, []).append(b)
        nb.setdefault(b, []).append(a)
    bad = [labels[v] for v in sorted(nb) if len(nb[v]) != 4]
    if bad:
        raise ValueError(f"supporting graph: vertices {bad!r} do not have degree four "
                         "(a simple bipartite q4 graph is required)")
    gone = [labels[v] for v in dom["owner_vid"] if v not in nb]
    if gone:
        raise ValueError(f"supporting graph: original vertices {gone!r} are absent (originals persist)")
    slots_mask = 0
    for j in range(dom["K"]):
        pa, pb = dom["a_vid"][j] in nb, dom["b_vid"][j] in nb
        if pa != pb:
            raise ValueError(f"supporting graph: newborn pair of owner {dom['owners'][j]!r} is half present")
        if pa:
            slots_mask |= 1 << j
    nbrs = {v: tuple(sorted(nb[v])) for v in sorted(nb)}
    present_mask = 0
    for v in nbrs:
        present_mask |= 1 << v
    port_codes = {}
    for v in nbrs:
        port_codes[v] = tuple(_code_any(dom, v, w) for w in _port_order(ctx, v, nbrs[v]))
    missing = {k: tuple(c for c in codes if c not in mod[k]) for k in ("h", "t", "theta")}
    missing["edge_cells"] = tuple(c for c in codes if c not in reg["edge_cell"]) if reg["edge_mode"] else ()
    info = {"edgeset": edgeset, "codes": tuple(codes), "nbrs": nbrs, "present": tuple(nbrs),
            "present_mask": present_mask, "slots_mask": slots_mask, "port_codes": port_codes,
            "missing": missing, "w_edge": {}, "w_deg": {}}
    info["fwd"] = _forward_channels(dom, info)
    info["rev"] = _reverse_channels(dom, info)
    return info


def _info_for(ctx, edgeset):
    info = ctx._infos.get(edgeset)
    if info is None:
        info = _graph_info(ctx, edgeset)
        ctx._infos[edgeset] = info
    return info


def _require_coverage(ctx, info, names):
    miss = info["missing"]
    parts = [f"{name} lacks edges {[_edge_labels(ctx._dom, c) for c in miss[name]]!r}"
             for name in names if miss[name]]
    if parts:
        raise ValueError("coefficient/registration coverage: " + "; ".join(parts)
                         + " (no default value and no zero-phase inference)")


# ---------------------------------------------------------------------------
# States: admission, canonical keys, labelled form
# ---------------------------------------------------------------------------

def _label_items(name, value, failures):
    if isinstance(value, (list, tuple, set, frozenset)):
        return list(value)
    failures.append(f"state['{name}']: a list, tuple or set is required")
    return []


def _parse_state_mapping(ctx, state, failures):
    dom = ctx._dom
    if not _keyset("state", state, _STATE_KEYS, failures):
        return None
    slots = 0
    for o in _label_items("slots", state["slots"], failures):
        j = dom["owner_index"].get(o) if _is_label(o) else None
        if j is None or (slots >> j) & 1:
            failures.append(f"state['slots']: {o!r} is not a (non-repeated) owner label")
            continue
        slots |= 1 << j
    edgeset = 0
    for e in _label_items("edges", state["edges"], failures):
        c = _edge_from_labels(dom, e)
        if c is None or (edgeset >> c) & 1:
            failures.append(f"state['edges']: {e!r} is not a (non-repeated) ordered pair (A label, B label)")
            continue
        edgeset |= 1 << c
    inc = 0
    for e in _label_items("occupied", state["occupied"], failures):
        c = _edge_from_labels(dom, e)
        if c is None or (inc >> c) & 1:
            failures.append(f"state['occupied']: {e!r} is not a (non-repeated) ordered pair (A label, B label)")
            continue
        inc |= 1 << c
    masks = []
    for name in ("carriers", "records", "spent"):
        m = 0
        for lab in _label_items(name, state[name], failures):
            v = dom["vid"].get(lab) if _is_label(lab) else None
            if v is None or (m >> v) & 1:
                failures.append(f"state['{name}']: {lab!r} is not a (non-repeated) vertex label")
                continue
            m |= 1 << v
        masks.append(m)
    dm = 0
    for item in _label_items("donors_ready", state["donors_ready"], failures):
        ok = isinstance(item, (list, tuple)) and len(item) == 2 and _is_label(item[0]) \
            and item[0] in dom["owner_index"] and isinstance(item[1], int) \
            and not isinstance(item[1], bool) and item[1] in (0, 1)
        d = 2 * dom["owner_index"][item[0]] + item[1] if ok else None
        if d is None or (dm >> d) & 1:
            failures.append(f"state['donors_ready']: {item!r} is not a (non-repeated) (owner label, 0|1)")
            continue
        dm |= 1 << d
    if failures:
        return None
    return (slots, edgeset, inc, masks[0], masks[1], masks[2], dm)


def _admit_key(ctx, key):
    dom = ctx._dom
    slots, edgeset, inc, p, q, s, dm = key
    if min(key) < 0 or slots >> dom["K"] or dm >> (2 * dom["K"]) or edgeset >> (dom["NA"] * dom["NB"]) \
            or (p | q | s) >> dom["NV"]:
        raise ValueError("state key: a field is negative or outside its declared bit range")
    info = _info_for(ctx, edgeset)
    problems = []
    if info["slots_mask"] != slots:
        problems.append("the slot set does not match the newborn vertices of the supporting graph")
    if inc & ~edgeset:
        problems.append("occupied edges outside the supporting graph")
    if (p | q | s) & ~info["present_mask"]:
        problems.append("carrier/record/spent bits on absent vertices")
    wrong = [dom["owners"][j] for j in range(dom["K"])
             if ((dm >> (2 * j)) & 3) != (0 if (slots >> j) & 1 else 3)]
    if wrong:
        problems.append(f"donor pairs of owners {wrong!r} violate the declared sector (RR iff the slot "
                        "is absent, II iff active)")
    if _popcount(p) != _popcount(s):
        problems.append(f"carrier count {_popcount(p)} != spent-cell count {_popcount(s)} (declared "
                        "sector N_c = S_graph)")
    if problems:
        raise ValueError("state: " + "; ".join(problems))
    return key, info


def _admit_state(ctx, state):
    """Return (canonical key, graph info) for a canonical key, labelled mapping or labelled pairs."""
    if isinstance(state, tuple) and len(state) == 7 and \
            all(isinstance(x, int) and not isinstance(x, bool) for x in state):
        return _admit_key(ctx, state)
    if isinstance(state, tuple):
        try:
            state = dict(state)
        except (TypeError, ValueError) as exc:
            raise ValueError("state: a canonical key, a labelled mapping or labelled pairs is required") from exc
    if not isinstance(state, Mapping):
        raise ValueError("state: a canonical key, a labelled mapping or labelled pairs is required")
    failures = []
    key = _parse_state_mapping(ctx, state, failures)
    if failures or key is None:
        raise ValueError("; ".join(failures))
    return _admit_key(ctx, key)


def _external_key(dom, key):
    slots, edgeset, inc, p, q, s, dm = key
    lab = dom["labels"]
    return (
        ("slots", tuple(dom["owners"][j] for j in _bits(slots))),
        ("edges", tuple(_edge_labels(dom, c) for c in _bits(edgeset))),
        ("occupied", tuple(_edge_labels(dom, c) for c in _bits(inc))),
        ("carriers", tuple(lab[v] for v in _bits(p))),
        ("records", tuple(lab[v] for v in _bits(q))),
        ("spent", tuple(lab[v] for v in _bits(s))),
        ("donors_ready", tuple((dom["owners"][d // 2], d % 2) for d in _bits(dm))),
    )


def _context(context):
    if not isinstance(context, OwnedModelContext):
        raise ValueError("context: an OwnedModelContext from validate_owned_model is required")
    return context


# ---------------------------------------------------------------------------
# The single source of truth: diagonal owners, transitions, amplitudes, weights, reads
# ---------------------------------------------------------------------------

def _diagonal_items(ctx, info, key):
    """(name, ref, feature) with amplitude model[name]*feature; contract s.3 diagonal list.

    Feature values follow PRIMARY CanonicalJoin.channels l.253 (full lambda_J sum d*p).
    """
    _slots, _edgeset, inc, p, q, s, dm = key
    dstar = ctx._model["dstar"]
    out = []
    for c in info["codes"]:
        if (inc >> c) & 1:
            out.append(("Delta", ("edge", c), 1.0))
    for v in info["present"]:
        d = 0
        for c in info["port_codes"][v]:
            d += (inc >> c) & 1
        bit = 1 << v
        x = (d - dstar) * (d - dstar)
        if x != 0.0:
            out.append(("Ud", ("degree", v), x))
        if p & bit:
            out.append(("epsilon_c", ("vertex", v), 1.0))
            if d:
                out.append(("lambda_J", ("degree", v), float(d)))
        if q & bit:
            out.append(("epsilon_r", ("vertex", v), 1.0))
            if d:
                out.append(("lambda_R", ("degree", v), -float(d)))
        # M_v = 1: a present site is S or R; the I-cell projector (E_I) is identically zero here.
        out.append(("E_S", ("vertex", v), 1.0) if s & bit else ("E_R", ("vertex", v), 1.0))
    for d in range(2 * ctx._dom["K"]):
        out.append(("e_R", ("donor", d), 1.0) if (dm >> d) & 1 else ("e_I", ("donor", d), 1.0))
    out.append(("C_identity", ("identity",), 1.0))
    return out


def _transitions(ctx, info, key):
    """(kind, ref, target key) for every allowed primitive transition, before aggregation.

    Native channels after PRIMARY CanonicalJoin.channels l.256-269 and SECONDARY event_channels
    l.136-142 (XOR bit updates), with structural closure independent of coefficient values.
    """
    dom = ctx._dom
    slots, edgeset, inc, p, q, s, dm = key
    out = []
    for c in info["codes"]:
        out.append(("flip", ("edge", c), (slots, edgeset, inc ^ (1 << c), p, q, s, dm)))
    for c in info["codes"]:
        if (inc >> c) & 1:
            a, b = _edge_ends(dom, c)
            pa, pb = (p >> a) & 1, (p >> b) & 1
            if pa != pb:
                out.append(("hop", ("edge", c, "B_to_A" if pb else "A_to_B"),
                            (slots, edgeset, inc, p ^ (1 << a) ^ (1 << b), q, s, dm)))
    for v in info["present"]:
        bit = 1 << v
        if p & bit:
            out.append(("bind", ("vertex", v), (slots, edgeset, inc, p, q ^ bit, s, dm)))
    for v in info["present"]:
        bit = 1 << v
        if not (s & bit) and not (p & bit):
            out.append(("admit", ("vertex", v), (slots, edgeset, inc, p | bit, q, s | bit, dm)))
        elif (s & bit) and (p & bit):
            out.append(("admit_rev", ("vertex", v), (slots, edgeset, inc, p ^ bit, q, s ^ bit, dm)))
    for ch in info["fwd"]:
        j = ch["j"]
        if ((dm >> (2 * j)) & 3) == 3 and _popcount(inc & ch["cutmask"]) == 2:
            new_inc = inc & ~ch["cutmask"]
            for cbit, cmask in ch["children"]:
                if inc & cbit:
                    new_inc |= cmask
            out.append(("birth", ("birth", ch),
                        (slots | (1 << j), ch["target_edgeset"], new_inc, p, q, s, dm & ~(3 << (2 * j)))))
    for ch in info["rev"]:
        j = ch["j"]
        if (dm >> (2 * j)) & 3 or (p | q | s) & ch["newborn_mask"]:
            continue  # donors not II, or a newborn not Ready with p = q = 0: zero
        census = 0
        new_inc = inc & ~ch["starmask"]
        equal = True
        for ub, av, rc in ch["pairs"]:
            x = (inc >> ub) & 1
            if x != (inc >> av) & 1:
                equal = False  # unequal paired child bits: zero (PRIMARY BirthMap.decode l.154-157)
                break
            census += x
            if x:
                new_inc |= 1 << rc
        if equal and census == 2:
            out.append(("birth_rev", ("birth", ch),
                        (slots & ~(1 << j), ch["target_edgeset"], new_inc, p, q, s, dm | (3 << (2 * j)))))
    return out


def _amplitude(model, kind, ref):
    """Primitive amplitudes; every reverse is the exact conjugate of its forward (ADDENDUM 3)."""
    if kind == "flip":
        return complex(-model["h"][ref[1]])
    if kind == "hop":
        z = model["hop_BA"][ref[1]]
        return z if ref[2] == "B_to_A" else z.conjugate()
    if kind == "bind":
        return complex(model["g"][ref[1]])
    if kind == "admit":
        return model["kappa"][ref[1]]
    if kind == "admit_rev":
        return model["kappa"][ref[1]].conjugate()
    z = model["epsilon"][ref[1]["j"]]
    return z if kind == "birth" else z.conjugate()


def _weights(ctx, edgeset, raw_edges, raw_vertices, raw_donors):
    """V002 equal-weight support fractions at the configuration whose graph is edgeset.

    Only anchors PRESENT in that configuration count; each distinct anchor once.
    """
    dom, reg = ctx._dom, ctx._reg
    anchors = set()
    for c in raw_edges:
        if (edgeset >> c) & 1:
            a, b = _edge_ends(dom, c)
            anchors.add((0, a))
            anchors.add((0, b))
            if reg["edge_mode"]:
                anchors.add((1, c))
    for v in raw_vertices:
        if _vertex_present(dom, edgeset, v):
            anchors.add((0, v))
    for d in raw_donors:
        if reg["donor_mode"] == "owner_vertex":
            anchors.add((0, dom["owner_vid"][d // 2]))
        else:
            anchors.add((2, d))
    counts = {}
    for tag, x in anchors:
        if tag == 0:
            alpha = reg["cell_vid"][x]
        elif tag == 1:
            alpha = reg["edge_cell"].get(x)
            if alpha is None:
                raise ValueError(f"registration['edge_cells'] lacks edge {_edge_labels(dom, x)!r}")
        else:
            alpha = reg["cell_vid"][dom["owner_vid"][x // 2]]
        counts[alpha] = counts.get(alpha, 0) + 1
    n = len(anchors)
    return tuple((alpha, counts[alpha] / n) for alpha in sorted(counts))


def _native_weights(ctx, info, ref):
    tag = ref[0]
    if tag == "edge":
        w = info["w_edge"].get(ref[1])
        if w is None:
            w = _weights(ctx, info["edgeset"], (ref[1],), (), ())
            info["w_edge"][ref[1]] = w
        return w
    if tag == "degree":
        w = info["w_deg"].get(ref[1])
        if w is None:
            w = _weights(ctx, info["edgeset"], info["port_codes"][ref[1]], (ref[1],), ())
            info["w_deg"][ref[1]] = w
        return w
    if tag == "vertex":
        return ctx._reg["w_site"][ref[1]]
    if tag == "donor":
        return ctx._reg["w_donor"][ref[1]]
    return ctx._reg["identity"]


def _birth_weights(ctx, ch, source_edgeset):
    """(w(source) + w(target))/2 per cell; identical for a forward channel and its reverse."""
    if ch["c"] is None:
        j = ch["j"]
        raw_v = (ctx._dom["a_vid"][j], ctx._dom["b_vid"][j])
        raw_d = (2 * j, 2 * j + 1)
        ws = dict(_weights(ctx, source_edgeset, ch["raw_edges"], raw_v, raw_d))
        wt = dict(_weights(ctx, ch["target_edgeset"], ch["raw_edges"], raw_v, raw_d))
        ch["c"] = tuple((a, 0.5 * (ws.get(a, 0.0) + wt.get(a, 0.0))) for a in sorted(set(ws) | set(wt)))
    return ch["c"]


def _support_labels(ctx, info, ref, kind):
    """Raw (queried, changed) anchors of one primitive, labelled."""
    dom = ctx._dom
    lab = dom["labels"]

    def ev(c):
        return ("edge", _edge_labels(dom, c))

    tag = ref[0]
    if tag == "edge":
        e = (ev(ref[1]),)
        if kind == "diag":
            return e, ()
        if kind == "flip":
            return e, e
        a, b = _edge_ends(dom, ref[1])
        ab = (("vertex", lab[a]), ("vertex", lab[b]))
        return e + ab, ab
    if tag == "degree":
        return (("vertex", lab[ref[1]]),) + tuple(ev(c) for c in info["port_codes"][ref[1]]), ()
    if tag == "vertex":
        x = (("vertex", lab[ref[1]]),)
        return (x, ()) if kind == "diag" else (x, x)
    if tag == "donor":
        return (("donor", (dom["owners"][ref[1] // 2], ref[1] % 2)),), ()
    if tag == "identity":
        return (), ()
    ch = ref[1]
    j = ch["j"]
    donors = (("donor", (dom["owners"][j], 0)), ("donor", (dom["owners"][j], 1)))
    newborn = (("vertex", lab[dom["a_vid"][j]]), ("vertex", lab[dom["b_vid"][j]]))
    cut = tuple(ev(c) for c in ch["cut"])
    root = tuple(ev(c) for c in ch["root_other"])
    child = tuple(ev(c) for c in ch["child_edges"])
    if kind == "birth":
        return cut + root + donors, cut + child + newborn + donors
    return newborn + child + root + donors, child + cut + newborn + donors


def _owner_id(ctx, name, ref):
    dom = ctx._dom
    tag = ref[0]
    if tag == "birth":
        ch = ref[1]
        return ("birth", dom["owners"][ch["j"]], tuple(_edge_labels(dom, c) for c in ch["cut"]))
    if tag == "identity":
        return ("C_identity",)
    if tag == "edge":
        return (name, ("edge", _edge_labels(dom, ref[1])))
    if tag in ("vertex", "degree"):
        return (name, ("vertex", dom["labels"][ref[1]]))
    return (name, ("donor", (dom["owners"][ref[1] // 2], ref[1] % 2)))


def _dense(n_alpha, sparse):
    out = [0.0] * n_alpha
    for alpha, f in sparse:
        out[alpha] = f
    return tuple(out)


def _diagonal_records(ctx, info, key):
    n_alpha = len(ctx.energy_cells)
    out = []
    for name, ref, feat in _diagonal_items(ctx, info, key):
        qs, cs = _support_labels(ctx, info, ref, "diag")
        out.append(_Channel(_owner_id(ctx, name, ref), "diag", None, complex(ctx._model[name] * feat),
                            qs, cs, _dense(n_alpha, _native_weights(ctx, info, ref))))
    return out


def _transition_records(ctx, info, key):
    n_alpha = len(ctx.energy_cells)
    out = []
    for kind, ref, target in _transitions(ctx, info, key):
        w = _birth_weights(ctx, ref[1], info["edgeset"]) if ref[0] == "birth" \
            else _native_weights(ctx, info, ref)
        qs, cs = _support_labels(ctx, info, ref, kind)
        out.append(_Channel(_owner_id(ctx, _FAMILY[kind], ref), kind, target,
                            _amplitude(ctx._model, kind, ref), qs, cs, _dense(n_alpha, w)))
    return out


def _z_bytes(dom, info, inc):
    """Per-vertex port values Z = 1 - 2 n (int8; 0 for absent vertices), [NV, 4] row-major."""
    zb = bytearray(4 * dom["NV"])
    for v in info["present"]:
        base = 4 * v
        for a, c in enumerate(info["port_codes"][v]):
            zb[base + a] = 255 if (inc >> c) & 1 else 1
    return bytes(zb)


def _reads_from_z(ctx, z, rows):
    """Read values and presence, float64 [len(rows), n], from int8 port values z [n, NV, 4]."""
    n = z.shape[0]
    vals = np.zeros((len(rows), n), dtype=np.float64)
    pres = np.zeros((len(rows), n), dtype=np.float64)
    present = z[:, :, 0] != 0
    cache = {}
    for k, r in enumerate(rows):
        spec = ctx._read_spec[r]
        kind = spec[0]
        if kind == "P":
            vals[k] = present[:, spec[1]]
            pres[k] = 1.0
        elif kind == "Z":
            vals[k] = z[:, spec[1], spec[2]]
            pres[k] = present[:, spec[1]]
        elif kind == "ZZ":
            vals[k] = z[:, spec[1], spec[2]].astype(np.float64) * z[:, spec[1], spec[3]].astype(np.float64)
            pres[k] = present[:, spec[1]]
        else:
            alpha = spec[1]
            if alpha not in cache:
                vids = ctx._reg["cell_vids"][alpha]
                m = present[:, vids].sum(axis=1).astype(np.float64)
                t = np.einsum("nva,ai->nvi", z[:, vids, :].astype(np.float64),
                              ctx._reg["port_vectors"], optimize=False)
                cache[alpha] = (m, t)
            m, t = cache[alpha]
            has = m > 0.0
            pres[k] = has
            if kind == "m":
                vals[k] = m
            elif kind == "R":
                np.divide(t[:, :, spec[2]].sum(axis=1), m, out=vals[k], where=has)
            else:
                num = np.einsum("nv,nv->n", t[:, :, spec[2]], t[:, :, spec[3]], optimize=False)
                np.divide(num, m, out=vals[k], where=has)
    return vals, pres


# ---------------------------------------------------------------------------
# Public state-level API (no basis enumeration required)
# ---------------------------------------------------------------------------

def canonical_state_key(*, context, state):
    """Canonical key (slots, edgeset, inc, p, q, s, donors) of an explicit state.

    state: a canonical key, a labelled mapping {'slots', 'edges', 'occupied', 'carriers',
    'records', 'spent', 'donors_ready'} (edges as (A label, B label), donors as (owner, 0|1)),
    or the labelled pairs returned by state_labels. Raises ValueError on any invalid state.
    """
    ctx = _context(context)
    return _admit_state(ctx, state)[0]


def state_labels(*, context, state):
    """Labelled, history-free form of a state (tuple of (field, labels) pairs; dict() gives a mapping)."""
    ctx = _context(context)
    return _external_key(ctx._dom, _admit_state(ctx, state)[0])


def diagonal_terms(*, context, state):
    """Every diagonal primitive owner of the state, with support and per-cell weights.

    Records (owner_id, kind='diag', target_state=None, amplitude, queried_support,
    changed_support, energy_weights[alpha] = w_alphaX(state)) in context.energy_cells order.
    """
    ctx = _context(context)
    key, info = _admit_state(ctx, state)
    _require_coverage(ctx, info, ("edge_cells",))
    return _diagonal_records(ctx, info, key)


def primitive_channels(*, context, state):
    """All primitive channels out of an explicit state, BEFORE aggregation.

    Records (owner_id, kind, target_state, amplitude, queried_support, changed_support,
    energy_weights). kind in diag/flip/hop/bind/admit/admit_rev/birth/birth_rev; target_state
    is a canonical key (None for diag); energy_weights[alpha] = (w_alphaX(target) +
    w_alphaX(source))/2 in context.energy_cells order, so E_alpha[target, source] contributions
    are energy_weights[alpha]*amplitude. Every valid reverse reconnection is its own record;
    coincident destinations stay separate. A candidate reconnection failing any image test is an
    exact zero and yields no record; all native owners still act. Raises ValueError on invalid
    input or missing coefficient coverage.
    """
    ctx = _context(context)
    key, info = _admit_state(ctx, state)
    _require_coverage(ctx, info, ("h", "t", "theta", "edge_cells"))
    return _diagonal_records(ctx, info, key) + _transition_records(ctx, info, key)


def read_rows(*, context, state):
    """Presence, single-port Z, pair and coarse reads of one state, typed and labelled.

    Returns {'labels': context.read_labels, 'values': float64 [n_read], 'presence': float64 [n_read]}.
    """
    ctx = _context(context)
    key, info = _admit_state(ctx, state)
    z = np.frombuffer(_z_bytes(ctx._dom, info, key[2]), dtype=np.int8).reshape(1, ctx._dom["NV"], 4)
    vals, pres = _reads_from_z(ctx, z, range(len(ctx.read_labels)))
    return {"labels": ctx.read_labels, "values": vals[:, 0].copy(), "presence": pres[:, 0].copy()}


# ---------------------------------------------------------------------------
# Basis enumeration and sparse assembly (index-based operator)
# ---------------------------------------------------------------------------

def _admit_caps(caps, failures):
    if not isinstance(caps, Mapping):
        failures.append(f"caps: a mapping with integer keys {_CAP_KEYS} is required")
        return None
    if not _keyset("caps", caps, _CAP_KEYS, failures):
        return None
    out = {}
    for k in _CAP_KEYS:
        v = caps[k]
        if isinstance(v, bool) or not isinstance(v, (int, np.integer)) or int(v) < 1:
            failures.append(f"caps['{k}']: a positive integer is required, got {v!r}")
        else:
            out[k] = int(v)
    return out if len(out) == len(_CAP_KEYS) else None


def _admit_dtype(dtype, failures):
    try:
        dt = np.dtype(dtype)
    except TypeError:
        failures.append(f"dtype: {dtype!r} is not a numpy dtype")
        return None
    if dt.kind != "c":
        failures.append(f"dtype: a complex numpy dtype is required, got {dt}")
        return None
    return dt


def _static_resources(ctx, caps):
    dom = ctx._dom
    v0, k = dom["V0"], dom["K"]
    return {
        "V0": v0, "K": k, "vertex_labels": dom["NV"], "n_cells": len(ctx.energy_cells),
        "n_read_rows": len(ctx.read_labels),
        "G0_block_inventory_sector_size": (2 ** (3 * v0)) * math.comb(2 * v0, v0),
        "G0_block_note": "states with graph G0, no active slot, donors RR, M_v=1 and N_c=S_g: "
                         "2^(2V0) incidence words x C(2V0,V0) 2^V0 local states; an exact count of "
                         "that block of the declared sector, not a claim about reachability",
        "contract_cost_formula": "O(D(1+6Vmax+132K)), Vmax=3V0 (contract section 11)",
        "caps": dict(caps),
        "cost_statement": "exponential full domain; matrix-free sparse action; no compression",
    }


def _new_run(caps):
    return {
        "caps": caps, "prov": {}, "keys": [], "graphs": set(),
        "missing": {"h": set(), "t": set(), "theta": set(), "edge_cells": set()}, "missing_any": False,
        "max_row": 0, "max_trans": 0,
        "H_diag": array("d"), "H_abs": array("d"), "E_diag": array("d"),
        "h_tgt": array("q"), "h_src": array("q"), "h_re": array("d"), "h_im": array("d"),
        "e_alpha": array("q"), "e_tgt": array("q"), "e_src": array("q"), "e_re": array("d"),
        "e_im": array("d"), "Z": [],
    }


def _discover(ctx, run, key):
    pid = run["prov"].get(key)
    if pid is not None:
        return pid
    caps = run["caps"]
    if len(run["keys"]) >= caps["max_dimension"]:
        raise _Stop(f"max_dimension cap {caps['max_dimension']} reached before admitting a further basis "
                    "state: the structural reachable component is larger than the cap (no support is "
                    "truncated; no operator is returned)")
    edgeset = key[1]
    if edgeset not in run["graphs"]:
        if len(run["graphs"]) >= caps["max_graphs"]:
            raise _Stop(f"max_graphs cap {caps['max_graphs']} reached before admitting a further supporting "
                        "graph (no graph block is dropped; no operator is returned)")
        run["graphs"].add(edgeset)
        m, reg = ctx._model, ctx._reg
        for c in _bits(edgeset):
            for name in ("h", "t", "theta"):
                if c not in m[name]:
                    run["missing"][name].add(c)
                    run["missing_any"] = True
            if reg["edge_mode"] and c not in reg["edge_cell"]:
                run["missing"]["edge_cells"].add(c)
                run["missing_any"] = True
    pid = len(run["keys"])
    run["keys"].append(key)
    run["prov"][key] = pid
    return pid


def _process_row(ctx, run, pid):
    key = run["keys"][pid]
    info = _info_for(ctx, key[1])
    diag = _diagonal_items(ctx, info, key)
    trans = _transitions(ctx, info, key)
    n = len(diag) + len(trans)
    cap = run["caps"]["max_events_per_row"]
    if n > cap:
        raise _Stop(f"max_events_per_row cap {cap} would be exceeded: a basis row has {n} primitive "
                    f"records ({len(diag)} diagonal owners, {len(trans)} transitions); nothing stored")
    run["max_row"] = max(run["max_row"], n)
    run["max_trans"] = max(run["max_trans"], len(trans))
    tpids = [_discover(ctx, run, item[2]) for item in trans]
    run["Z"].append(_z_bytes(ctx._dom, info, key[2]))
    if run["missing_any"]:
        return  # coverage failure is reported after the structural closure completes
    model = ctx._model
    erow = [0.0] * len(ctx.energy_cells)
    hd = 0.0
    habs = 0.0
    for name, ref, feat in diag:
        amp = model[name] * feat
        hd += amp
        habs += abs(amp)
        for alpha, f in _native_weights(ctx, info, ref):
            erow[alpha] += f * amp
    run["H_diag"].append(hd)
    run["H_abs"].append(habs)
    run["E_diag"].extend(erow)
    for (kind, ref, _target), tpid in zip(trans, tpids):
        amp = _amplitude(model, kind, ref)
        run["h_tgt"].append(tpid)
        run["h_src"].append(pid)
        run["h_re"].append(amp.real)
        run["h_im"].append(amp.imag)
        w = _birth_weights(ctx, ref[1], key[1]) if ref[0] == "birth" else _native_weights(ctx, info, ref)
        for alpha, f in w:
            run["e_alpha"].append(alpha)
            run["e_tgt"].append(tpid)
            run["e_src"].append(pid)
            run["e_re"].append(f * amp.real)
            run["e_im"].append(f * amp.imag)


def _aggregate(group, tgt, src, re, im):
    """Sum duplicate (group, tgt, src) entries; sorted by (group, tgt, src); with |.| sums."""
    if tgt.size == 0:
        e = np.zeros(0, dtype=np.int64)
        f = np.zeros(0, dtype=np.float64)
        return e, e, e, f, f, f
    order = np.lexsort((src, tgt, group))
    g, t, s, r, i = group[order], tgt[order], src[order], re[order], im[order]
    new = np.ones(t.size, dtype=bool)
    new[1:] = (g[1:] != g[:-1]) | (t[1:] != t[:-1]) | (s[1:] != s[:-1])
    st = np.flatnonzero(new)
    a = np.sqrt(r * r + i * i)
    return (g[st], t[st], s[st], np.add.reduceat(r, st), np.add.reduceat(i, st),
            np.add.reduceat(a, st))


def _hermitian_violation(g, t, s, r, i, a, tol_factor):
    if t.size == 0:
        return False
    order = np.lexsort((t, s, g))
    if not (np.array_equal(s[order], t) and np.array_equal(t[order], s) and np.array_equal(g[order], g)):
        return True
    diff = np.hypot(r[order] - r, -i[order] - i)
    return bool(np.any(diff > tol_factor * (a + a[order])))


def _csr(tgt, src, vals):
    if tgt.size == 0:
        e = np.zeros(0, dtype=np.int64)
        return {"rows": e, "starts": e, "cols": e, "vals": vals}
    new = np.ones(tgt.size, dtype=bool)
    new[1:] = tgt[1:] != tgt[:-1]
    st = np.flatnonzero(new)
    return {"rows": tgt[st], "starts": st, "cols": src.copy(), "vals": vals}


def _csr_apply(csr, block, out):
    """out[rows] += segment sums of vals * block[cols] (PRIMARY action_sparse l.287-299, vectorized)."""
    vals = csr["vals"]
    nnz = vals.size
    if nnz == 0:
        return
    starts, rows, cols = csr["starts"], csr["rows"], csr["cols"]
    nseg = starts.size
    chunk = 1 << 20
    g0 = 0
    while g0 < nseg:
        e0 = int(starts[g0])
        g1 = int(np.searchsorted(starts, e0 + chunk, side="left"))
        if g1 <= g0:
            g1 = g0 + 1
        e1 = int(starts[g1]) if g1 < nseg else nnz
        contrib = vals[e0:e1, None] * block[cols[e0:e1], :]
        out[rows[g0:g1], :] += np.add.reduceat(contrib, starts[g0:g1] - e0, axis=0)
        g0 = g1


def _column_bound(diag, csr, n, max_row):
    absv = np.abs(csr["vals"].astype(np.complex128))
    col = np.bincount(csr["cols"], weights=absv, minlength=n) + np.abs(diag.astype(np.float64))
    return float(col.max()) * (1.0 + (max_row + 2) * 2.0 ** -52)


def _assemble(ctx, run, dt):
    keys = run["keys"]
    n = len(keys)
    n_alpha = len(ctx.energy_cells)
    rdt = np.zeros(1, dtype=dt).real.dtype
    order = np.array(sorted(range(n), key=keys.__getitem__), dtype=np.int64)
    perm = np.empty(n, dtype=np.int64)
    perm[order] = np.arange(n, dtype=np.int64)
    keys_sorted = [keys[i] for i in order]
    h_diag = _np_buffer(run["H_diag"], np.float64)[order]
    h_abs = _np_buffer(run["H_abs"], np.float64)[order]
    e_diag = _np_buffer(run["E_diag"], np.float64).reshape(n, n_alpha)[order].T.copy()
    z = np.frombuffer(b"".join(run["Z"]), dtype=np.int8).reshape(n, ctx._dom["NV"], 4)[order]
    h_t = perm[_np_buffer(run["h_tgt"], np.int64)]
    h_s = perm[_np_buffer(run["h_src"], np.int64)]
    e_t = perm[_np_buffer(run["e_tgt"], np.int64)]
    e_s = perm[_np_buffer(run["e_src"], np.int64)]
    e_a = _np_buffer(run["e_alpha"], np.int64).copy()
    hg, ht, hs, hre, him, habs_e = _aggregate(np.zeros(h_t.size, dtype=np.int64), h_t, h_s,
                                              _np_buffer(run["h_re"], np.float64),
                                              _np_buffer(run["h_im"], np.float64))
    eg, et, es, ere, eim, eabs = _aggregate(e_a, e_t, e_s, _np_buffer(run["e_re"], np.float64),
                                            _np_buffer(run["e_im"], np.float64))
    integrity = []
    tol = 4.0 * np.finfo(np.float64).eps * (run["max_row"] + n_alpha + 2)
    if _hermitian_violation(hg, ht, hs, hre, him, habs_e, tol):
        integrity.append("integrity: aggregated H is not Hermitian within summation tolerance")
    if _hermitian_violation(eg, et, es, ere, eim, eabs, tol):
        integrity.append("integrity: some aggregated E_alpha is not Hermitian within summation tolerance")
    sg, st, ss, sre, sim, sabs = _aggregate(np.zeros(et.size, dtype=np.int64), et, es, ere, eim)
    if not (np.array_equal(st, ht) and np.array_equal(ss, hs)) or \
            np.any(np.hypot(sre - hre, sim - him) > tol * (sabs + habs_e)):
        integrity.append("integrity: off-diagonal sum_alpha E_alpha differs from H")
    if np.any(np.abs(e_diag.sum(axis=0) - h_diag) > tol * (h_abs + 1e-300)):
        integrity.append("integrity: diagonal sum_alpha E_alpha differs from H")
    h_csr = _csr(ht, hs, (hre + 1j * him).astype(dt))
    bounds = np.searchsorted(eg, np.arange(n_alpha + 1))
    e_csr = []
    for alpha in range(n_alpha):
        lo, hi = int(bounds[alpha]), int(bounds[alpha + 1])
        e_csr.append(_csr(et[lo:hi], es[lo:hi], (ere[lo:hi] + 1j * eim[lo:hi]).astype(dt)))
    h_diag_s = h_diag.astype(rdt)
    e_diag_s = e_diag.astype(rdt)
    norm_h = _column_bound(h_diag_s, h_csr, n, run["max_row"])
    norm_e = [_column_bound(e_diag_s[a], e_csr[a], n, run["max_row"]) for a in range(n_alpha)]
    arrays = [h_diag_s, e_diag_s, z, h_csr["rows"], h_csr["starts"], h_csr["cols"], h_csr["vals"]]
    for c in e_csr:
        arrays.extend((c["rows"], c["starts"], c["cols"], c["vals"]))
    per_key = sys.getsizeof(keys_sorted[0]) + sum(sys.getsizeof(x) for x in keys_sorted[0])
    dom = ctx._dom
    resources = _static_resources(ctx, run["caps"])
    resources.update({
        "D": n, "graph_count": len(run["graphs"]),
        "events_per_row_max": run["max_row"], "transitions_per_row_max": run["max_trans"],
        "stored_H_offdiagonal_entries": int(h_csr["vals"].size),
        "stored_E_offdiagonal_entries": {ctx.energy_cells[a]: int(e_csr[a]["vals"].size)
                                         for a in range(n_alpha)},
        "per_matvec_elementary_work": {
            "apply_H_per_column": n + int(h_csr["vals"].size),
            "apply_E_per_column": {ctx.energy_cells[a]: n + int(e_csr[a]["vals"].size)
                                   for a in range(n_alpha)},
            "apply_O_per_column": n},
        "contract_cost_formula_value": n * (1 + 18 * dom["V0"] + 132 * dom["K"]),
        "memory_estimate_bytes": {
            "arrays_exact": int(sum(x.nbytes for x in arrays)),
            "basis_keys_estimate": int(n * (2 * per_key + 200)),
            "note": "keys estimate = tuple and int objects of the first key plus two dict slots per state"},
        "port_vectors_equal_register_spec": ctx._reg["port_vectors_equal_register_spec"],
    })
    parts = {"D": n, "dtype": dt, "real_dtype": rdt, "ctx": ctx, "keys": keys_sorted,
             "index": {k: i for i, k in enumerate(keys_sorted)}, "H_diag": h_diag_s, "H_csr": h_csr,
             "E_diag": e_diag_s, "E_csr": e_csr, "Z": z, "norm_H": norm_h, "norm_E": norm_e,
             "max_row": run["max_row"], "resources": resources}
    return parts, integrity


def build_owned_operator(*, graph0, model, registration, seed_states, caps, dtype):
    """Enumerate the structural reachable component of seed_states and build the sparse operator.

    seed_states: nonempty list/tuple of explicit states (any form accepted by canonical_state_key).
    caps: {'max_dimension', 'max_graphs', 'max_events_per_row'} positive ints; each fails
    explicitly before being exceeded. dtype: complex numpy dtype of apply_* arithmetic.
    Returns {'ok', 'stage_reached', 'failures', 'operator', 'resources'}. Uses exactly the
    state-level functions' internals (validate_owned_model, _diagonal_items, _transitions,
    _amplitude, _weights, _z_bytes, _reads_from_z), so there is one source of truth.
    """
    result = {"ok": False, "stage_reached": "inputs", "failures": [], "operator": None, "resources": None}
    failures = result["failures"]
    validated = validate_owned_model(graph0=graph0, model=model, registration=registration)
    failures.extend(validated["failures"])
    cap = _admit_caps(caps, failures)
    dt = _admit_dtype(dtype, failures)
    if failures or not validated["ok"] or cap is None or dt is None:
        return result
    ctx = validated["context"]
    result["resources"] = _static_resources(ctx, cap)

    result["stage_reached"] = "seeds"
    if not isinstance(seed_states, (list, tuple)) or len(seed_states) == 0:
        failures.append("seed_states: a nonempty list or tuple of explicit states is required")
        return result
    seeds = []
    for i, st in enumerate(seed_states):
        try:
            seeds.append(_admit_state(ctx, st)[0])
        except ValueError as exc:
            failures.append(f"seed_states[{i}]: {exc}")
    if failures:
        return result

    result["stage_reached"] = "enumeration"
    run = _new_run(cap)
    try:
        for key in seeds:
            _discover(ctx, run, key)
        pid = 0
        while pid < len(run["keys"]):
            _process_row(ctx, run, pid)
            pid += 1
    except (_Stop, ValueError) as exc:
        failures.append(f"enumeration: {exc}")
    result["resources"].update({"states_discovered": len(run["keys"]), "graphs_discovered": len(run["graphs"]),
                                "events_per_row_max_seen": run["max_row"]})
    if failures:
        return result

    result["stage_reached"] = "coverage"
    for name in ("h", "t", "theta", "edge_cells"):
        miss = sorted(run["missing"][name])
        if miss:
            where = "registration['edge_cells']" if name == "edge_cells" else f"model['{name}']"
            failures.append(f"{where}: no value for stable edges {[_edge_labels(ctx._dom, c) for c in miss]!r} "
                            "that occur in the enumerated component (no default; zero phase is never inferred)")
    if failures:
        return result

    result["stage_reached"] = "assembly"
    parts, integrity = _assemble(ctx, run, dt)
    result["resources"] = parts["resources"]
    result["stage_reached"] = "integrity"
    if integrity:
        failures.extend(integrity)
        return result
    result["operator"] = OwnedParentOperator(parts=parts)
    result["ok"] = True
    result["stage_reached"] = "complete"
    return result


# ---------------------------------------------------------------------------
# Index-based operator
# ---------------------------------------------------------------------------

def _local_h2(model, v):
    """Four-state local block H(2) on [R p0 q0, R p0 q1, S p1 q0, S p1 q1] at d = 2 (L7)."""
    base = model["Ud"] * (2.0 - model["dstar"]) * (2.0 - model["dstar"])
    r2 = model["epsilon_r"] - 2.0 * model["lambda_R"]
    c2 = model["epsilon_c"] + 2.0 * model["lambda_J"]
    kap = model["kappa"][v]
    g = model["g"][v]
    h = np.zeros((4, 4), dtype=np.complex128)
    h[0, 0] = base + model["E_R"]
    h[1, 1] = base + r2 + model["E_R"]
    h[2, 2] = base + c2 + model["E_S"]
    h[3, 3] = base + c2 + r2 + model["E_S"]
    h[2, 0] = kap
    h[0, 2] = kap.conjugate()
    h[3, 1] = kap
    h[1, 3] = kap.conjugate()
    h[3, 2] = g
    h[2, 3] = g
    return h


def _ice_extend(i, inc, ends, codes, deg, rem, out, cap):
    if len(out) > cap:
        return
    if i == len(codes):
        if all(x == 2 for x in deg.values()):
            out.append(inc)
        return
    a, b = ends[i]
    rem[a] -= 1
    rem[b] -= 1
    if deg[a] + rem[a] >= 2 and deg[b] + rem[b] >= 2:
        _ice_extend(i + 1, inc, ends, codes, deg, rem, out, cap)
    if deg[a] < 2 and deg[b] < 2:
        deg[a] += 1
        deg[b] += 1
        _ice_extend(i + 1, inc | (1 << codes[i]), ends, codes, deg, rem, out, cap)
        deg[a] -= 1
        deg[b] -= 1
    rem[a] += 1
    rem[b] += 1


class OwnedParentOperator:
    """Index-based matrix-free owned-parent operator (built only by build_owned_operator).

    Members: dimension, dtype, energy_cells, read_labels, context, basis_key, index_of,
    primitive_events, apply_H, apply_E, read_values, read_presence, apply_O, norm_bound_H,
    norm_bound_E, resources, reference_preparation.
    """

    def __init__(self, *, parts):
        self._p = parts
        self.dimension = parts["D"]
        self.dtype = parts["dtype"]
        self.context = parts["ctx"]
        self.energy_cells = self.context.energy_cells
        self.read_labels = self.context.read_labels
        self._cell_pos = {c: i for i, c in enumerate(self.energy_cells)}

    def _checked_index(self, index):
        if isinstance(index, bool) or not isinstance(index, (int, np.integer)) \
                or not 0 <= int(index) < self.dimension:
            raise ValueError(f"index: an integer in [0, {self.dimension}) is required, got {index!r}")
        return int(index)

    def _checked_block(self, block):
        if type(block) is not np.ndarray or block.ndim != 2 or block.shape[0] != self.dimension \
                or block.dtype != self.dtype:
            raise ValueError(f"block: a plain ndarray of shape [{self.dimension}, k] and dtype "
                             f"{self.dtype} is required")
        return block

    def _alpha(self, alpha):
        try:
            pos = self._cell_pos.get(alpha)
        except TypeError:
            pos = None
        if pos is None:
            raise ValueError(f"alpha: {alpha!r} is not one of energy_cells {self.energy_cells!r}")
        return pos

    def basis_key(self, *, index):
        """Labelled history-free key of basis state index (dict() of it is a state mapping)."""
        return _external_key(self.context._dom, self._p["keys"][self._checked_index(index)])

    def index_of(self, *, key):
        """Basis index of a state given in any form accepted by canonical_state_key."""
        k = _admit_state(self.context, key)[0]
        i = self._p["index"].get(k)
        if i is None:
            raise KeyError("state is valid but not in the enumerated reachable component")
        return i

    def primitive_events(self, *, index):
        """Primitive records of basis row index before aggregation (same core as primitive_channels).

        Records (owner_id, kind, source_index, target_index, amplitude, queried_support,
        changed_support, energy_weights); diagonal records have target_index == source_index.
        """
        i = self._checked_index(index)
        key = self._p["keys"][i]
        info = _info_for(self.context, key[1])
        out = []
        for r in _diagonal_records(self.context, info, key) + _transition_records(self.context, info, key):
            t = i if r.target_state is None else self._p["index"][r.target_state]
            out.append(_IndexedEvent(r.owner_id, r.kind, i, t, r.amplitude, r.queried_support,
                                     r.changed_support, r.energy_weights))
        return out

    def apply_H(self, *, block):
        """H block, matrix-free (aggregated sparse entries; no dense D x D)."""
        b = self._checked_block(block)
        out = self._p["H_diag"][:, None] * b
        _csr_apply(self._p["H_csr"], b, out)
        return out

    def apply_E(self, *, alpha, block):
        """E_alpha block, E_alpha[y,x] = sum_X (w_alphaX(y)+w_alphaX(x))/2 h_X[y,x]."""
        a = self._alpha(alpha)
        b = self._checked_block(block)
        out = self._p["E_diag"][a][:, None] * b
        _csr_apply(self._p["E_csr"][a], b, out)
        return out

    def read_values(self):
        """All read rows, float64 [n_read, D]; 0 where the row's object is absent."""
        return _reads_from_z(self.context, self._p["Z"], range(len(self.read_labels)))[0]

    def read_presence(self):
        """Presence (0/1) of every read row, float64 [n_read, D]."""
        return _reads_from_z(self.context, self._p["Z"], range(len(self.read_labels)))[1]

    def apply_O(self, *, read_index, block):
        """Diagonal read O_r applied to block (presence-masked values)."""
        if isinstance(read_index, bool) or not isinstance(read_index, (int, np.integer)) \
                or not 0 <= int(read_index) < len(self.read_labels):
            raise ValueError(f"read_index: an integer in [0, {len(self.read_labels)}) is required")
        b = self._checked_block(block)
        vals = _reads_from_z(self.context, self._p["Z"], [int(read_index)])[0][0]
        return vals.astype(self._p["real_dtype"])[:, None] * b

    def norm_bound_H(self):
        """Upper bound on ||H||_2: max absolute column sum of the stored Hermitian matrix (L10)."""
        return self._p["norm_H"]

    def norm_bound_E(self, *, alpha):
        """Upper bound on ||E_alpha||_2 (same construction)."""
        return self._p["norm_E"][self._alpha(alpha)]

    def resources(self):
        """Dimension, sizes, per-matvec work, memory estimate and caps (plain dict copy)."""
        return dict(self._p["resources"])

    def reference_preparation(self, *, chi, ice_factor):
        """DECLARED reference family of contract section 1 -- never a default state.

        Original G0, no active slot, donors RR, chi on every original site, rho_ice = F F^dagger on
        the complete degree-two incidence subspace of G0. chi: 'ground_of_declared_local_H2' (unique
        ground of the four-state H(2) per original site, L7) or an explicit complex [V0, 8] array
        (rows in owner order, column 4*S + 2*p + q, each row unit norm; nothing is renormalized).
        ice_factor: None (return only the sparse isometry and ice words) or a complex [n_ice, r]
        factor F with Tr F^dagger F = 1 in the returned ice-word order.
        Returns {'ok', 'stage_reached', 'failures', 'family', 'chi', 'ice_words', 'isometry_rows',
        'isometry_cols', 'isometry_values', 'factor'}.
        """
        res = {"ok": False, "stage_reached": "inputs", "failures": [],
               "family": "DECLARED REFERENCE FAMILY (contract section 1); not a default or physical state",
               "chi": None, "ice_words": None, "isometry_rows": None, "isometry_cols": None,
               "isometry_values": None, "factor": None}
        fails = res["failures"]
        ctx = self.context
        dom, model = ctx._dom, ctx._model
        v0 = dom["V0"]
        eps = np.finfo(np.float64).eps
        if isinstance(chi, str):
            if chi != _CHI_FROM_H2:
                fails.append(f"chi: the only admitted string is {_CHI_FROM_H2!r}")
                return res
            rows = []
            for j, v in enumerate(dom["owner_vid"]):
                h2 = _local_h2(model, v)
                w, vecs = np.linalg.eigh(h2)
                scale = float(np.abs(h2).sum())
                if not w[1] - w[0] > 64.0 * eps * max(1.0, scale):
                    fails.append(f"chi: local H(2) ground at {dom['owners'][j]!r} is not unique "
                                 f"(gap {w[1] - w[0]!r})")
                    continue
                g = vecs[:, 0]
                k = int(np.argmax(np.abs(g)))
                g = g * (abs(g[k]) / g[k])
                row = np.zeros(8, dtype=np.complex128)
                row[[0, 1, 6, 7]] = g
                rows.append(row)
            if fails:
                return res
            chi_arr = np.array(rows)
        else:
            if type(chi) is not np.ndarray or chi.shape != (v0, 8) or chi.dtype.kind not in "iufc":
                fails.append(f"chi: a plain numeric ndarray of shape ({v0}, 8) or {_CHI_FROM_H2!r} is required")
                return res
            chi_arr = chi.astype(np.complex128)
            if not np.all(np.isfinite(chi_arr)):
                fails.append("chi: entries must be finite")
                return res
            norms = np.sum(chi_arr.real * chi_arr.real + chi_arr.imag * chi_arr.imag, axis=1)
            tol = 64.0 * _eps_of(chi.dtype) * 8
            bad = [dom["owners"][j] for j in range(v0) if not abs(norms[j] - 1.0) <= tol]
            if bad:
                fails.append(f"chi: rows for {bad!r} are not unit norm (nothing is renormalized)")
                return res
        res["chi"] = chi_arr
        res["stage_reached"] = "ice_words"
        edgeset0 = dom["edgeset0"]
        codes = _bits(edgeset0)
        ends = [_edge_ends(dom, c) for c in codes]
        deg = {v: 0 for v in dom["owner_vid"]}
        rem = {v: 4 for v in dom["owner_vid"]}
        words = []
        _ice_extend(0, 0, ends, codes, deg, rem, words, self.dimension)
        if len(words) > self.dimension:
            fails.append("ice words outnumber the basis dimension; the family is not contained in it")
            return res
        words.sort()
        word_pos = {w: i for i, w in enumerate(words)}
        nnz = [int(np.count_nonzero(chi_arr[j])) for j in range(v0)]
        expected = 1
        for x in nnz:
            expected *= x
        all_ready = (1 << (2 * dom["K"])) - 1
        r_rows, r_cols, r_vals = [], [], []
        found = [0] * len(words)
        underflow = 0
        for idx, key in enumerate(self._p["keys"]):
            slots, edgeset, inc, p, q, s, dm = key
            if slots or edgeset != edgeset0 or dm != all_ready:
                continue
            wpos = word_pos.get(inc)
            if wpos is None:
                continue
            amp = 1.0 + 0.0j
            support = True
            for j, v in enumerate(dom["owner_vid"]):
                x = chi_arr[j, 4 * ((s >> v) & 1) + 2 * ((p >> v) & 1) + ((q >> v) & 1)]
                if x == 0:
                    support = False
                    break
                amp *= complex(x)
            if not support:
                continue
            found[wpos] += 1
            if amp == 0:
                underflow += 1
            r_rows.append(idx)
            r_cols.append(wpos)
            r_vals.append(amp)
        short = sum(1 for f in found if f != expected)
        if short or underflow:
            fails.append(f"reference family not contained in the enumerated component: {short} of "
                         f"{len(words)} ice words lack some of the {expected} chi-supported local "
                         f"configurations; {underflow} amplitudes underflow (seed G0 with donors RR)")
            return res
        res["ice_words"] = tuple(tuple(_edge_labels(dom, c) for c in _bits(w)) for w in words)
        res["isometry_rows"] = np.array(r_rows, dtype=np.int64)
        res["isometry_cols"] = np.array(r_cols, dtype=np.int64)
        res["isometry_values"] = np.array(r_vals, dtype=np.complex128)
        res["stage_reached"] = "factor"
        if ice_factor is not None:
            f = ice_factor
            if type(f) is not np.ndarray or f.ndim != 2 or f.shape[0] != len(words) or f.shape[1] < 1 \
                    or f.dtype.kind not in "iufc":
                fails.append(f"ice_factor: None or a plain numeric ndarray [{len(words)}, r] is required")
                return res
            fc = f.astype(np.complex128)
            if not np.all(np.isfinite(fc)):
                fails.append("ice_factor: entries must be finite")
                return res
            tr = float(np.sum(fc.real * fc.real + fc.imag * fc.imag))
            if not abs(tr - 1.0) <= 64.0 * _eps_of(f.dtype) * f.size:
                fails.append(f"ice_factor: Tr F^dagger F = {tr!r} is not 1 (nothing is renormalized)")
                return res
            lf = np.zeros((self.dimension, f.shape[1]), dtype=self.dtype)
            lf[res["isometry_rows"], :] = (res["isometry_values"][:, None] * fc[res["isometry_cols"], :]).astype(self.dtype)
            res["factor"] = lf
        res["ok"] = True
        res["stage_reached"] = "complete"
        return res
