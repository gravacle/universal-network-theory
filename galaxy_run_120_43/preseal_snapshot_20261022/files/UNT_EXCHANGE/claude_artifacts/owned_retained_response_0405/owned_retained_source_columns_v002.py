"""Owned retained response: same-state full-H primal/tangent source-column propagator.

UNT task 0405, module B (contract section 11(B)), version v002. Static author
implementation: written as text and never imported or executed by its author.
v002 = v001 plus ONLY the MANDATORY ADDENDUM V001 item 1 time-derivative reads (same-state
full-H first/second native-time derivatives of every mean and response, the explicit
generator K' term, their error bounds, and the explicit read/frame and background-generator
declarations); every v001 output, equation and bound is unchanged.

Binding sources (sha256 computed from bytes before writing):
  * OWNED_RETAINED_RESPONSE_FULL_H_SOURCE_COLUMN_IMPLEMENTATION_CONTRACT_V001.txt
    fcad9039574f1666af005bb76a231f14b90f0c8dd82acebd2b16ab77941cd642
  * UNT_EXCHANGE/FROM_CODEX/0405_2026-10-16_main_owned_response_provider_implementation.md
    7baab49ebbd01de684df56a074b823552c1eca9e787384ad0a0084144295c003
  * UNT_EXCHANGE/FROM_CODEX/0406_2026-10-16_response_moments_and_current_state_keys.md
    a465d9e3f703f2a2f19d383446c6a2bf6486e5f6be9fdf5996fc96dfb4693d50 (binding corrections)
  * CODEX1/COARSE_REGISTER_STATE_BOUNDARY_WORKING_SPECIFICATION_V001.json (adopted)
    032a564bd018b7302bd60de633f8e3c9d2f91f8c079f16b62548bce0e4e53d94 (semantics only)
  * CODEX1/COARSE_PROPER_TIME_ENERGY_COUPLING_PROPOSAL_V002.json
    494d0124c1cd49841760dfc49673d696eab3486d75b31fda708679fa5cacb78a; adoption record
    b5e7c2e3f12a6a4e3358a3c63a797783645d69240e757778ca42a91729a22465 (provisional,
    explicitly COUNTED assumption; not a derived native law)
  * coefficient_method/COARSE_ENERGY_PARTIAL_LEGENDRE_METRIC_COUPLING_CANDIDATE_V001.md
    d81d48e8407f5576305dbbb50a275f163401bbb91f67b5938dc9736ec8b21663
  * coefficient_method/UNIFORM_ENERGY_KUBO_IDENTITIES_AND_LEGENDRE_ZERO_MODE_V001.md
    a7d048c11a826d6d2627afd3f5324458a0350bc6abbd58bd8ab8d6c39d7eedf7
  * coefficient_method/FINITE_STATIONARY_PAIR_KERNEL_LAPSE_LIMIT_AND_COMPLETION_CORRECTION_V001.md
    facdfe454904ea27b38df19865168a7560bf24b56cb774c549ea53a1addec9b4
  * coefficient_method/OWNED_RETAINED_PROVIDER_IMPLEMENTATION_MANDATORY_READ_AND_LABEL_ADDENDUM_V001.txt
    7cb15b4a5ac2ea33dfd43801c011142bc2b2388c3be0087152c049e78deccd39 (BINDING; item 1)
  * response_packet_audit/SAME_ACTION_COVARIANCE_VOLUME_TIME_DERIVATIVES_ADDENDUM_V001.md
    2fc9dc2c0197d6b3d0e2ff5893ba32b7ef89ba5424680bc06bd5210d5207226a (cited by item 1:
    L_O = partial_tau O + (i/hbar)[K,O], A_O = partial_tau^2 O + (2i/hbar)[K,partial_tau O]
    + (i/hbar)[K',O] - [K,[K,O]]/hbar^2)
Legacy code read as text only (never imported or executed):
  * exploratory_physics/root_native_shared_parent_clock_transport_v001.py
    d7871d1bd4c55b826c2d7a04606a2552e418017c12379fc018b90811aae4a2a9, taylor_step
    (its lines 159-168): the Taylor recursion term_{k} = (-i step/k) H term_{k-1} is reused
    here. Its a priori remainder (|step| * model.bound) is REPLACED by the a posteriori
    residual bound below, and the recursion is extended to tangent columns with exact
    polynomial forcing. No parameter value or other logic is taken from it.
  * canonical_join_backend_v002.py (0d28150f...) and native_many_carrier_sparse_operator_v001.py
    (6b8d8dfd...) are operator-side (module A) material; nothing from them is used here.

Public entries (keyword-only, no defaults):
  propagate_source_columns(*, operator, preparation, source_columns, time_grid, hbar,
                           stepper, caps, dtype, time_derivative_contacts)
  partial_legendre_blocks(*, chi_EE, chi_EO, chi_OE, chi_OO, contacts, read_quotient,
                          energy_quotient, declared_zero_modes, relative_singular_floor,
                          exclusion_tolerance)
  g00_lapse_coordinate_contact(*, n_g, energy_means)
Each returns a plain fail-closed dict with "ok", "stage_reached" and "failures"; when ok
is False every populated field is failure evidence only.

SEMANTICS. The operator is any object exposing the shared module-A interface (it is
duck-typed; module A is NOT imported). With n = N - 1 (affine coarse lapse source, adopted
V002 support-mean proper-time placement inside the operator's E_alpha) and read sources j:
    H[n, j] = H + sum_alpha n_alpha E_alpha - sum_A j_A O_A,   sum_alpha E_alpha = H.
Every preparation column l_k (purification factor, signed density factor or family
isometry column) evolves with the SAME full H, and every source column b adds a tangent:
    i hbar d l_k/dt       = H l_k,
    i hbar d dl_{b,k}/dt  = H dl_{b,k} + V_b(t) l_k,      dl_{b,k}(t0) = 0,
    V_b(t) = f_b(t) * ( sum_alpha cE[b,alpha] E_alpha - sum_A cO[b,A] O_A ).
So an energy/lapse column has V = +f E_alpha and a read (first-moment or pair) column has
V = -f O_A (contract section 6). Outputs (all E_alpha, then every operator read row, on
the SAME state) are
    mean   <A>(t)      = sum_k s_k <l_k(t)|A|l_k(t)>,
    resp   delta<A>(t) = 2 Re sum_k s_k <l_k(t)|A|dl_{b,k}(t)>,
with s_k = +1 except for retained slightly negative density eigenvalues (s_k = -1).
Equivalently, with chi_AB(t,s) = (i/hbar) theta(t-s) Tr rho0 [A_H(t), B_H(s)],
    resp[o,b,t] = int_{t0}^{t} ds f_b(s) ( sum_A cO[b,A] chi_{o,O_A}(t,s)
                                           - sum_alpha cE[b,alpha] chi_{o,E_alpha}(t,s) ),
i.e. delta O = chi_OO j - chi_OE n and delta E = chi_EO j - chi_EE n. No stationarity,
ground, Gibbs, ice or Markov assumption is used; memory is contained exactly in full-H
evolution. No P/Q reduction is implemented. Source profiles f_b are caller-declared
per-interval polynomials (ascending powers of t - t_k on [t_k, t_{k+1}]); observation
times are exactly the time-grid nodes. Nothing is fitted or interpolated.

UNITS. hbar, time_grid, operator energies and source profiles are in one caller-declared
consistent system: f_b * E_alpha and f_b * O_A must have energy units. No conversion.

ERROR BOUND (rigorous in exact arithmetic; derivation in _taylor_substep and
_node_bounds). On each substep of length h inside one interval, with sigma = s/h and the
source re-expanded exactly as f(s) = sum_p a''_p sigma^p, the scaled Taylor terms are
    u_0 = L(start),  u_{n+1} = (-i h/hbar)/(n+1) H u_n,
    w_0 = dL_b(start), w_{n+1} = (-i h/hbar)/(n+1) [H w_n + B_b G_n],  G_n = sum_p a''_p u_{n-p},
and the substep result is sum_{n<=N} u_n, sum_{n<=N} w_n. The truncated polynomials obey
the evolution equations up to the exactly computable residuals
    eta_psi(s) = -sigma^N H u_N,
    eta_b(s)   = -sigma^N H w_N - sum_{j=N}^{N+P} sigma^j B_b Gt_j,
    Gt_j = sum_{p: 0 <= j-p <= N, p <= P} a''_p u_{j-p}.
For Hermitian H the homogeneous error grows by at most int ||eta||/hbar, so per substep
    rho_psi = h ||H u_N||_F / ((N+1) hbar),
    rho_b   = (h/hbar) [ ||H w_N||_F/(N+1)
                         + ||B_b|| sum_{j=N}^{N+P} sum_p |a''_p| ||u_{j-p}||_F/(j+1) ],
    eps_L  <- eps_L + rho_psi,
    eps_b  <- eps_b + rho_b + (||B_b||/hbar) eps_L(end) h sum_p |a''_p|/(p+1),
the last term being the tangent forcing error carried from the primal error. Here
||B_b|| = sum_alpha |cE[b,alpha]| norm_bound_E(alpha) + max_x |sum_A cO[b,A] O_A(x)|.
Source quadrature error is ZERO by construction: the polynomial forcing enters the Taylor
recursion exactly; its truncation is inside eta_b. Read contractions are bounded by
Cauchy-Schwarz with ||L(t)||_F = ||L0||_F:
    |mean error|  <= ||A|| eps_L (||L_N(t)||_F + ||L0||_F) [+ ||A|| R1],
    |resp error|  <= 2 ||A|| (eps_L ||dL_{b,N}(t)||_F + ||L0||_F eps_b)
                     [+ 2 ||A|| ||B_b|| R1 int_{t0}^{t}|f_b| / hbar],
where R1 = sqrt(D) ||rho_h - L diag(s) L^dagger||_F is the measured trace-norm bound of
the density factorization residual (zero for purification and family inputs). For the
family-isometry path the same numbers bound the Frobenius norm of the compressed r x r
error matrices, hence |Tr(rho_ice * error)| for every family density with trace norm <= 1.
Count/norm leakage is reported only as a diagnostic, never as an error bound.

NOT COVERED: floating-point rounding in the recursion, in substep accumulation (Taylor
cancellation is reported as term_mass_ratio), in the exact-algebra re-expansion of
source coefficients and the placement of substep starts j*h, in operator applications
(module A), in einsum contractions and norm evaluations, in the computation of the
bounds themselves, in eigh beyond the measured reconstruction residual, and in the
dtype down-cast of operator outputs. The bounds also presume the operator premises: H and
every E_alpha Hermitian, sum_alpha E_alpha = H, norm_bound_E(alpha) a true upper bound,
reads diagonal. Declared norm bounds are checked on every application (necessary, not
sufficient) and read diagonality is checked once (necessary, not sufficient).

TIME DERIVATIVES (v002; MANDATORY ADDENDUM V001 item 1 and the HP addendum 2fc9dc2c). At
every node, on the SAME state and with the SAME full-H matvec, for every output A (every
E_alpha, every operator read row -- first-moment, pair and coarse m/R/S rows alike -- and
every presence row). The background is the flat point n = 0, j = 0, so the zeroth-order
generator is K = H, time independent, with tau = t (N_bg = 1), and the first-order
generator is K = H + sum_b f_b(t) B_b, B_b = sum_alpha cE[b,alpha] E_alpha - sum_A cO[b,A]
O_A, whose derivative K' = sum_b f_b'(t) B_b is RETAINED. Reads, registration, frame and
support are the operator's fixed current-state definitions, so partial_t A = 0 and the
(2i/hbar)[K, partial_t A] term is zero (declared by the caller in time_derivative_contacts;
anything else fails explicitly, LIMITATIONS L17). Then, exactly,
    d<A>/dt         = <L_A> = (i/hbar) <[H,A]>,
    d2<A>/dt2       = <A_A> = -(1/hbar^2) <[H,[H,A]]>,
    d delta<A>/dt   = (i/hbar) delta_b<[H,A]> + f_b(t) G1[A,b],
    d2 delta<A>/dt2 = -(1/hbar^2) delta_b<[H,[H,A]]> + f_b(t) G2[A,b] + f_b'(t) G1[A,b],
    G1[A,b] = (i/hbar) <[B_b, A]>_0,
    G2[A,b] = -(1/hbar^2) <[B_b,[H,A]] + [H,[B_b,A]]>_0,
with delta_b<X> = 2 Re sum_k s_k <l_k|X|dl_bk> for Hermitian X (these follow from
i hbar rho' = [K, rho] and i hbar delta rho' = [H, delta rho] + [V_b, rho]; f_b' G1 is the
(i/hbar)<[K',A]> term). In column form, with Z^dagger over the family indices and
<x|y> antilinear in x:
    <L_A>  = (i/hbar)(X - X^dagger),        X = <H l|A l>,
    <A_A>  = -(1/hbar^2)(Y + Y^dagger - 2Z), Y = <H^2 l|A l>, Z = <H l|A|H l>,
    hom1   = P + P^dagger,  P = (i/hbar)(<H l|A dl> - <A l|H dl>),
    hom2   = -(1/hbar^2)(Q + Q^dagger), Q = <H^2 l|A dl> - 2<H l|A|H dl> + <A l|H^2 dl>,
    G1     = (i/hbar)(W - W^dagger), W = <B l|A l>,
    G2     = -(1/hbar^2)(U + U^dagger), U = <H B l|A l> + <B H l|A l> - 2<B l|A|H l>,
built from H L, H(H L), H dL, H(H dL), E_alpha on [L, H L, H^2 L], B_b L, B_b H L and
H B_b L (trace mode: sum_k s_k of the diagonal, i.e. X + X^dagger -> 2 Re x and
(i/hbar)(X - X^dagger) -> -(2/hbar) Im x). Profiles may be discontinuous at nodes, so the
assembled response derivatives are returned as LEFT limits (nodes 1..K, from interval k-1)
and RIGHT limits (nodes 0..K-1, from interval k), with the exact one-sided node values f_b
and f_b'; the homogeneous and contact pieces are single-valued and are returned too. d<H>/dt
is identically zero at the flat point and is not returned.
DERIVATIVE BOUNDS (same Cauchy-Schwarz scheme; each output is the exact expectation or
response of a fixed operator C on the computed state). With ||(i/hbar)[H,A]|| <= c1 ||A||,
c1 = 2 normH/hbar, ||[H,[H,A]]||/hbar^2 <= c2 ||A||, c2 = 4 normH^2/hbar^2:
    mean first/second : the mean bound with ||A|| -> c1 ||A|| / c2 ||A||,
    hom1/hom2         : the response bound with ||A|| -> c1 ||A|| / c2 ||A||,
    G1[A,b] : (2/hbar) ||B_b|| ||A|| (eps_L (||L_N||_F + ||L0||_F) + R1),
    G2[A,b] : (8 normH/hbar^2) ||B_b|| ||A|| (eps_L (||L_N||_F + ||L0||_F) + R1),
    first  (side) : bound(hom1) + |f_b(side)| bound(G1),
    second (side) : bound(hom2) + |f_b(side)| bound(G2) + |f_b'(side)| bound(G1).
These are rigorous in exact arithmetic under the same operator premises (normH a true bound
on ||H||_2); the rounding list above also applies to the extra matvecs, contractions and
the evaluation of f_b and f_b' at nodes.

COST. Per substep: (N+1) apply_H calls on a [D, r(1+m)] block, plus for every order with
active forcing one apply_E call per energy cell carrying a nonzero coefficient (block
[D, r * number of such sources]) and O(D r m) diagonal read work. Per observation node
(v002, including the time derivatives): apply_H on [D, (1+m) r] twice and, for m > 0, on
[D, m r] once; apply_E per cell on [D, 3 r] ([D, 2 r] when m = 0) plus, per cell carrying a
nonzero energy source coefficient, on [D, 2 r]; plus O((n_read + m) D r) contraction work
(family path O(n_read m D r^2)). Working memory is O(D r (20 m + P + 30)) entries; a
dense density input propagates r = D columns and adds about 6 D^2 entries (its eigh and
reconstruction check cost O(D^3)). D is the
FULL owned inventory component dimension from module A, exponential in V0; nothing here
reduces it. Caps fail explicitly before being exceeded; no support is truncated.

LIMITATIONS: see the module-level string LIMITATIONS.
"""

import math

import numpy as np


LIMITATIONS = """
L1. Read typing (0406 item 1). Raw means/responses are partitioned by the kind token each
    operator.read_labels entry declares: a dict key or attribute named 'kind',
    'read_kind', 'moment' or 'type' (first present), else element 0 of a tuple/list label.
    A label without a string token is an explicit failure. The token strings themselves
    (e.g. first-moment versus pair) are module A's; module B groups rows by the exact token
    and never guesses. Interface alignment with module A must be confirmed at integration.
L2. Diagonal reads. Read forcing and read contractions use the materialized diagonal
    operator.read_values(); operator.apply_O is compared with it once on one deterministic
    non-constant vector within stepper consistency_tolerance. That check is necessary,
    not sufficient, for diagonality; a non-diagonal apply_O would invalidate the forcing
    and the bounds.
L3. Coarse normalization. Module B applies no normalization of its own: no conditional
    normalization, no 1/<m_alpha>, no frozen counts. Coarse R_alpha,i and S_alpha,ij of the
    adopted register spec (with the diagonal current-state 1/m_alpha inside the operator)
    are sourced/responded only if module A exposes them as read rows. Nonlinear caller-side
    combinations (C = M - mu mu^T; delta C = delta M - delta mu mu^T - mu delta mu^T; second
    derivatives with products of first derivatives AND second mean derivatives) are NOT
    formed here. A covariance-only response is never inverted here. The register-spec
    property tr C <= 4 is documented, never imposed or clipped.
L4. Linearization point. Means and responses are about the flat point n = 0, j = 0 with a
    FIXED preparation (delta psi(t0) = 0). A nonzero background lapse, a source-dependent
    preparation, re-prepared equilibrium derivatives and second-order (n, j) responses are
    not computed. Contacts are reported explicitly (zero Hamiltonian contacts in the affine
    n coordinate; g00 coordinate contact via g00_lapse_coordinate_contact).
L5. Observation times are the time-grid nodes only. Profiles are per-interval polynomials
    in t - t_k and may be discontinuous at nodes; no interpolation choice is made.
    Source coefficients must be real (Hermitian sources); complex coefficients are rejected.
L6. Error bounds are rigorous only in exact arithmetic and only under the operator premises
    listed in the module docstring; floating-point rounding listed there is not covered.
    residual_tolerance below the dtype rounding level cannot be verified by this module.
L7. Density input. The Hermitian part (rho + rho^dagger)/2 is factorized by numpy.linalg.eigh;
    all D eigencolumns are kept (no rank reduction) and eigenvalues within psd_tolerance
    below zero are retained exactly with sign -1 (signed factor). The anti-Hermitian part
    only affects imaginary parts, which are not reported. The eigh residual is measured
    and enters the bounds through R1; its O(D^3) cost is real.
L8. Family isometry. Outputs are r x r compressed Hermitian matrices for the DECLARED
    reference family (V rho_ice V^dagger); the family is not a default physical state and
    no member is chosen here. Bounds are on Frobenius norms of the compressed errors.
L9. No P/Q (projected memory) reduction is implemented; full-H propagation only.
L10. partial_legendre_blocks works on caller-discretized finite matrices of causal kernels
    with a caller-declared quotient (bilinear pairing T^T chi S); contact terms are
    additive W second-derivative contacts supplied explicitly by the caller and applied
    BEFORE the Schur complement. It invents no matching/EH coefficient and does not
    identify a raw finite susceptibility with the complete metric propagator (finite
    pair-kernel correction). Singularity is judged by a caller relative floor; no
    regulator or pseudoinverse is ever used.
L11. Working-memory estimates count this module's arrays only (not module A internals or
    numpy temporaries). Column-application caps count columns passed to apply_* calls.
L12. Operator exceptions and malformed outputs are converted into explicit failures.
L13. The finite owned inventory component is exponential in V0; feasibility for any
    physical G0 is not claimed. No physical parameter, state, profile or default is
    supplied by this module.
L14. Ambiguities resolved literally: (a) the contract's pair-coefficient array is
    implemented as read_coefficients over EVERY operator read row (first-moment and pair,
    0406 item 1); (b) "observation quadratures" are the time-grid nodes; (c) presence means
    and presence responses are returned as additional same-state outputs (raw presence/
    population, register spec), never as replacements or normalizers; (d) <H>(t) and the
    energy-partition residual are diagnostics, not outputs used elsewhere; (e) operator
    dimension, energy_cells and read_labels are read as attributes, every other interface
    member is called with keyword arguments exactly as in the shared interface.
L15. MANDATORY ADDENDUM V001 item 1 (7cb15b4a...; HP addendum 2fc9dc2c...). Full-H first and
    second native-time derivatives of every mean (<L_A>, <A_A>) and of every response are
    returned at every node on the same state, with per-entry bounds (module docstring,
    TIME DERIVATIVES). They are exact same-state commutator reads, not finite differences of
    node values. The explicit generator K' term is retained: at the flat point the
    zeroth-order K = H is time independent (K' = 0), and the first-order K' = sum_b
    f_b'(t) B_b enters the response second derivative as f_b' G1 (returned separately with
    G1, G2 and the node values f_b, f_b'). Derivatives are with respect to the native time
    t of time_grid; tau = t at the flat point (N_bg = 1). The nonlinear centered and volume
    reads of the HP addendum (C' = M' - mu' mu^T - mu mu'^T, C'', v'/v, H_v, a_v''/a_v) are
    caller-side combinations of the returned mu, M, mu', M', mu'', M'' and are not formed
    here (L3); a singular C is not regularized here because C is not formed here.
L16. One-sided node values. Profiles may be discontinuous at nodes (L5), and so may their
    derivatives. Assembled response derivatives are therefore returned as left limits
    (nodes 1..K, interval k-1 evaluated at its end) and right limits (nodes 0..K-1,
    interval k evaluated at its start); no side is chosen. Mean derivatives and the
    homogeneous/contact pieces are single-valued (the state is continuous).
L17. Read/frame and generator declarations (time_derivative_contacts, required, exact keys).
    'read_frame' must be 'fixed_current_state_reads': every E_alpha, read and presence row is
    the operator's fixed current-state definition with fixed registration, frame, scale and
    support, so partial_t A = partial_t^2 A = 0 and the (2i/hbar)[K, partial_t A] term
    vanishes; state-dependent 1/m_alpha, presence and adjacency are inside A and act through
    the commutator (no separate count derivative is added). 'background_generator' must be
    'flat_point_time_independent_H': K = H at n = 0, j = 0, N_bg = 1. Any other value fails
    explicitly: an operator-level time-dependent read/registration/support, or a nonzero or
    time-dependent background lapse/source, is not representable through the shared
    interface (L4) and is never silently dropped. A c-number registered frame acting
    linearly on returned rows, O(t) = T(t) O, and the homogeneous proper-time
    reparametrization d/dtau = N_bg^-1 d/dt are caller-side combinations of returned
    quantities (formulas in contacts['time_derivatives']).
L18. Moment typing with module A v001 tokens (integration note; module B still groups by the
    exact token, L1): first_moment_Z and coarse_first_R are first moments (mu, registered
    X), pair_ZZ and coarse_second_S raw second moments (M), vertex_presence and
    coarse_population_m presence/population. Coarse rows m_alpha, R_alpha_i, S_alpha_ij are
    accepted as ordinary diagonal read rows for means, responses, source columns and time
    derivatives; their per-configuration 1/m_alpha is inside the operator (L3).
"""

_READ_FRAME_FIXED = "fixed_current_state_reads"
_BACKGROUND_FLAT = "flat_point_time_independent_H"


# ---------------------------------------------------------------------------
# Admission helpers (private)
# ---------------------------------------------------------------------------

def _admit_real(name, value, failures):
    """Admit a finite real scalar as float, or record a failure and return None."""
    if isinstance(value, (bool, np.bool_)):
        failures.append(f"input {name}: a boolean is not an admitted real scalar")
        return None
    if not isinstance(value, (int, float, np.integer, np.floating)):
        failures.append(f"input {name}: type {type(value).__name__} is not an admitted real scalar")
        return None
    try:
        out = float(value)
    except (OverflowError, ValueError, TypeError):
        failures.append(f"input {name}: not representable as a float64 value")
        return None
    if not math.isfinite(out):
        failures.append(f"input {name}: not finite ({out!r})")
        return None
    return out


def _admit_positive_real(name, value, failures):
    out = _admit_real(name, value, failures)
    if out is not None and not out > 0.0:
        failures.append(f"input {name}: must be > 0, got {out!r}")
        return None
    return out


def _admit_nonnegative_real(name, value, failures):
    out = _admit_real(name, value, failures)
    if out is not None and not out >= 0.0:
        failures.append(f"input {name}: must be >= 0, got {out!r}")
        return None
    return out


def _admit_positive_int(name, value, failures):
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, np.integer)):
        failures.append(f"input {name}: must be an integer, got type {type(value).__name__}")
        return None
    out = int(value)
    if out <= 0:
        failures.append(f"input {name}: must be > 0, got {out!r}")
        return None
    return out


def _admit_mapping(name, value, keys, failures):
    """Admit a dict with exactly the given keys (no missing, no extra), else None."""
    if not isinstance(value, dict):
        failures.append(f"input {name}: type {type(value).__name__} is not a dict")
        return None
    missing = [k for k in keys if k not in value]
    extra = [k for k in value if k not in keys]
    if missing:
        failures.append(f"input {name}: missing keys {missing!r} (no defaults are supplied)")
    if extra:
        failures.append(f"input {name}: unknown keys {extra!r} (rejected, not ignored)")
    if missing or extra:
        return None
    return value


def _admit_array(name, value, ndim, allow_complex, failures):
    """Admit a plain ndarray or nested list/tuple of finite numbers with the given ndim.

    Returns float64 (real input) or complex128 (complex input when allowed), else None.
    Booleans, objects, ndarray subclasses, non-finite entries and complex values where
    not allowed are rejected.
    """
    if isinstance(value, np.ndarray):
        if type(value) is not np.ndarray:
            failures.append(f"input {name}: ndarray subclass {type(value).__name__} is not admitted")
            return None
        arr = value
    elif isinstance(value, (list, tuple)):
        try:
            arr = np.array(value)
        except (ValueError, TypeError) as exc:
            failures.append(f"input {name}: not a rectangular numeric array ({exc})")
            return None
    else:
        failures.append(f"input {name}: type {type(value).__name__} is not an array, list or tuple")
        return None
    if arr.ndim != ndim:
        failures.append(f"input {name}: ndim {arr.ndim} is not {ndim} (shape {arr.shape!r})")
        return None
    kind = arr.dtype.kind
    if kind == "c":
        if not allow_complex:
            failures.append(f"input {name}: complex entries are not admitted (real required)")
            return None
        out = arr.astype(np.complex128)
    elif kind in ("f", "i", "u"):
        out = arr.astype(np.float64)
    else:
        failures.append(f"input {name}: dtype {arr.dtype!r} is not an admitted numeric dtype")
        return None
    bad = int(np.count_nonzero(~np.isfinite(out)))
    if bad:
        failures.append(f"input {name}: {bad} non-finite entries")
        return None
    return out


def _fro(X):
    """Frobenius norm accumulated in float64 by explicit elementwise arithmetic."""
    re = np.asarray(X.real, dtype=np.float64)
    total = float(np.sum(re * re))
    if np.iscomplexobj(X):
        im = np.asarray(X.imag, dtype=np.float64)
        total += float(np.sum(im * im))
    return math.sqrt(total)


def _max_abs(X):
    return float(np.max(np.abs(X))) if X.size else 0.0


def _member(obj, name):
    """Fetch an attribute; any exception (including from a property) means absent."""
    try:
        return True, getattr(obj, name)
    except Exception as exc:  # converted to an explicit failure by the caller
        return False, f"{type(exc).__name__}: {exc}"


def _call(failures, what, fn, kwargs):
    """Call an operator member; exceptions become explicit failures, never silence."""
    try:
        return True, fn(**kwargs)
    except Exception as exc:  # converted to an explicit failure
        failures.append(f"operator: {what} raised {type(exc).__name__}: {exc}")
        return False, None


def _read_kind(label):
    """Kind token of a read label (see LIMITATIONS L1), or None when undeclared."""
    token = None
    if isinstance(label, dict):
        for key in ("kind", "read_kind", "moment", "type"):
            if key in label:
                token = label[key]
                break
    else:
        for key in ("kind", "read_kind", "moment", "type"):
            present, value = _member(label, key)
            if present and isinstance(value, str):
                token = value
                break
        if token is None and isinstance(label, (tuple, list)) and len(label) > 0:
            token = label[0]
    if isinstance(token, str) and token:
        return token
    return None


# ---------------------------------------------------------------------------
# Operator application with caps, shape/finite checks and norm-bound observation
# ---------------------------------------------------------------------------

def _apply_block(*, operator, method, kwargs, block, D, dt, budget, failures, bound,
                 consistency_tolerance, what):
    """Apply operator.<method>(block=..., **kwargs) to a [D, k] block.

    Fails BEFORE a call that would exceed the column-application cap. The block is
    passed as a fresh C-contiguous copy so the operator cannot alias module state. The
    output must be a plain [D, k] real/complex finite ndarray. When bound is not None,
    ||out||_F <= (1 + consistency_tolerance) * bound * ||block||_F is required: a
    violation means a declared norm bound is false and every error bound would be
    invalid, so it is a failure.
    """
    k = int(block.shape[1])
    if budget["used"] + k > budget["cap"]:
        failures.append(
            f"caps: max_column_applications {budget['cap']} would be exceeded by "
            f"{method} during {what} ({budget['used']} used + {k}); stopped before exceeding"
        )
        return None
    budget["used"] += k
    budget["by_method"][method] += k
    arg = np.array(block, dtype=dt, order="C", copy=True)
    ok, out = _call(failures, f"{method} during {what}", getattr(operator, method),
                    dict(kwargs, block=arg))
    if not ok:
        return None
    if type(out) is not np.ndarray or out.shape != (D, k) or out.dtype.kind not in ("f", "c"):
        shape = getattr(out, "shape", None)
        failures.append(
            f"operator: {method} during {what} returned {type(out).__name__} with shape "
            f"{shape!r}; a plain real/complex ndarray of shape {(D, k)!r} is required"
        )
        return None
    out = out.astype(dt, copy=False)
    if not bool(np.all(np.isfinite(out))):
        failures.append(f"operator: {method} during {what} returned non-finite entries")
        return None
    if bound is not None:
        lhs = _fro(out)
        rhs = (1.0 + consistency_tolerance) * bound * _fro(block)
        if lhs > rhs:
            failures.append(
                f"operator: declared norm bound {bound!r} violated by {method} during {what} "
                f"(||out||_F = {lhs!r} > (1 + consistency_tolerance) * bound * ||in||_F = "
                f"{rhs!r}); error bounds would be invalid"
            )
            return None
    return out


# ---------------------------------------------------------------------------
# Taylor substep with exact polynomial forcing and a posteriori residual bounds
# ---------------------------------------------------------------------------

def _shift_scale(*, coeffs, tau0, h):
    """Re-expand f(tau0 + s) = sum_q a_q (tau0 + s)^q as sum_p a''_p (s/h)^p (exact algebra).

    a'_p = sum_{q >= p} a_q binom(q, p) tau0^(q-p),  a''_p = a'_p h^p.  coeffs: [m, P+1].
    """
    m, P1 = coeffs.shape
    out = np.zeros((m, P1), dtype=np.float64)
    for p in range(P1):
        acc = np.zeros(m, dtype=np.float64)
        for q in range(p, P1):
            acc = acc + coeffs[:, q] * (float(math.comb(q, p)) * (tau0 ** (q - p)))
        out[:, p] = acc * (h ** p)
    return out


def _forcing(*, operator, window, n, r, m, D, a2, active, cE, cells, normE, dO, dt, budget,
             failures, consistency_tolerance, where):
    """F_b = B_b G_{b,n}, G_{b,n} = sum_p a''_{b,p} u_{n-p}, B_b = sum cE E_alpha - diag(dO_b).

    window[-1 - p] is u_{n-p}. Returns [D, m r] (tangent layout) or None on failure.
    """
    P1 = a2.shape[1]
    G = np.zeros((D, m * r), dtype=dt)
    for b in range(m):
        if not active[b]:
            continue
        for p in range(0, min(P1 - 1, n) + 1):
            coeff = float(a2[b, p])
            if coeff != 0.0:
                G[:, b * r:(b + 1) * r] += coeff * window[-1 - p]
    F = np.zeros((D, m * r), dtype=dt)
    for ia, alpha in enumerate(cells):
        bs = [b for b in range(m) if active[b] and float(cE[b, ia]) != 0.0]
        if not bs:
            continue
        cols = np.concatenate([np.arange(b * r, (b + 1) * r) for b in bs])
        Yb = _apply_block(operator=operator, method="apply_E", kwargs={"alpha": alpha},
                          block=G[:, cols], D=D, dt=dt, budget=budget, failures=failures,
                          bound=normE[ia], consistency_tolerance=consistency_tolerance,
                          what=f"source forcing at {where}, order {n}, cell index {ia}")
        if Yb is None:
            return None
        for j, b in enumerate(bs):
            F[:, b * r:(b + 1) * r] += float(cE[b, ia]) * Yb[:, j * r:(j + 1) * r]
    for b in range(m):
        if active[b]:
            F[:, b * r:(b + 1) * r] -= dO[b][:, None] * G[:, b * r:(b + 1) * r]
    return F


def _taylor_substep(*, operator, S, r, m, D, h, hbar, a2, active, cE, cells, normE, normH,
                    dO, Bnorm, tol, max_order, dt, budget, failures, consistency_tolerance,
                    where):
    """One substep of the augmented primal/tangent system by Taylor recursion.

    S: [D, (1+m) r] start state; columns [0, r) primal, [(1+b) r, (2+b) r) tangent b.
    Scaled terms (sigma = s/h): u_{n+1} = c/(n+1) H u_n, w_{n+1} = c/(n+1)(H w_n + B G_n),
    c = -i h/hbar. Before adding order n+1, the residual integrals of the order-n
    polynomials are evaluated (module docstring, ERROR BOUND):
      rho_psi = h ||H u_n||_F / ((n+1) hbar)                                 [primal]
      rho_b   = (h/hbar)(||H w_n||_F/(n+1)
                + ||B_b|| sum_{j=n}^{n+P} sum_{p=max(0,j-n)}^{min(P,j)} |a''_p| ||u_{j-p}||_F/(j+1))
    These follow from eta_psi = -sigma^n H u_n and
    eta_b = -sigma^n H w_n - sum_{j>=n} sigma^j B Gt_j, with int_0^h sigma^j ds = h/(j+1)
    and ||B Gt_j|| <= ||B_b|| sum_p |a''_p| ||u_{j-p}||. The substep is accepted at the
    first n with rho_psi <= tol and every rho_b <= tol; if n reaches max_order first, it
    fails explicitly (nothing is accepted silently).
    """
    P1 = a2.shape[1]
    c = -1j * h / hbar
    T = S.copy()
    acc = S.copy()
    window = [T[:, :r].copy()]
    unorm = [_fro(T[:, :r])]
    mass = _fro(T)
    for n in range(max_order + 1):
        Y = _apply_block(operator=operator, method="apply_H", kwargs={}, block=T, D=D, dt=dt,
                         budget=budget, failures=failures, bound=normH,
                         consistency_tolerance=consistency_tolerance,
                         what=f"Taylor order {n} at {where}")
        if Y is None:
            return None
        rho_psi = h * _fro(Y[:, :r]) / ((n + 1) * hbar)
        rho_b = np.zeros(m, dtype=np.float64)
        for b in range(m):
            s = _fro(Y[:, (1 + b) * r:(2 + b) * r]) / (n + 1)
            if active[b]:
                for j in range(n, n + P1):
                    tot = 0.0
                    for p in range(max(0, j - n), min(P1 - 1, j) + 1):
                        tot += abs(float(a2[b, p])) * unorm[j - p]
                    s += Bnorm[b] * tot / (j + 1)
            rho_b[b] = h * s / hbar
        if rho_psi <= tol and bool(np.all(rho_b <= tol)):
            acc_norm = _fro(acc)
            return {
                "S": acc,
                "rho_psi": rho_psi,
                "rho_b": rho_b,
                "order": n,
                "term_mass_ratio": (mass / acc_norm) if acc_norm > 0.0 else None,
            }
        if n == max_order:
            worst_b = float(np.max(rho_b)) if m else 0.0
            failures.append(
                f"propagation: residual did not close at {where}: after max_order = "
                f"{max_order} the integrated residual bounds are primal {rho_psi!r}, "
                f"tangent max {worst_b!r}, residual_tolerance {tol!r}; no step accepted "
                "(reduce max_step_norm_product or raise max_order)"
            )
            return None
        coef = c / (n + 1)
        Tn = np.empty_like(T)
        Tn[:, :r] = coef * Y[:, :r]
        if m > 0 and not any(active):
            Tn[:, r:] = coef * Y[:, r:]
        elif m > 0:
            F = _forcing(operator=operator, window=window, n=n, r=r, m=m, D=D, a2=a2,
                         active=active, cE=cE, cells=cells, normE=normE, dO=dO, dt=dt,
                         budget=budget, failures=failures,
                         consistency_tolerance=consistency_tolerance, where=where)
            if F is None:
                return None
            Tn[:, r:] = coef * (Y[:, r:] + F)
        T = Tn
        acc += T
        mass += _fro(T)
        window.append(T[:, :r].copy())
        if len(window) > P1:
            window.pop(0)
        unorm.append(_fro(T[:, :r]))
    return None  # unreachable: the loop returns or fails at n == max_order


# ---------------------------------------------------------------------------
# Same-state contractions and their bounds at one observation node
# ---------------------------------------------------------------------------

def _pair_applied(X, Y, sig, mode):
    """Column pairing <X|Y> with the output operator already applied to one side.

    X, Y: [D, r] (primal-shaped) or [D, m, r] (tangent-shaped), at most one tangent-shaped.
    trace mode: sum_k s_k <X_k|Y_k> (scalar, or [m]); family mode: [r, r] (or [m, r, r]).
    """
    Xc = np.conj(X)
    if mode == "trace":
        if X.ndim == 2 and Y.ndim == 2:
            return np.einsum("xk,xk,k->", Xc, Y, sig, optimize=False)
        if X.ndim == 2:
            return np.einsum("xk,xbk,k->b", Xc, Y, sig, optimize=False)
        return np.einsum("xbk,xk,k->b", Xc, Y, sig, optimize=False)
    if X.ndim == 2 and Y.ndim == 2:
        return np.einsum("xk,xl->kl", Xc, Y, optimize=False)
    if X.ndim == 2:
        return np.einsum("xk,xbl->bkl", Xc, Y, optimize=False)
    return np.einsum("xbk,xl->bkl", Xc, Y, optimize=False)


def _pair_diag(Vd, X, Y, sig, mode):
    """Column pairing <X|diag(Vd_a)|Y> for every row a of a real diagonal matrix Vd [n_a, D].

    Shapes as _pair_applied with a leading n_a axis.
    """
    Xc = np.conj(X)
    if mode == "trace":
        if X.ndim == 2 and Y.ndim == 2:
            w = np.einsum("xk,xk,k->x", Xc, Y, sig, optimize=False)
            return np.einsum("ax,x->a", Vd, w, optimize=False)
        if X.ndim == 2:
            w = np.einsum("xk,xbk,k->bx", Xc, Y, sig, optimize=False)
        else:
            w = np.einsum("xbk,xk,k->bx", Xc, Y, sig, optimize=False)
        return np.einsum("ax,bx->ab", Vd, w, optimize=False)
    if X.ndim == 2 and Y.ndim == 2:
        return np.einsum("ax,xk,xl->akl", Vd, Xc, Y, optimize=False)
    if X.ndim == 2:
        return np.einsum("ax,xk,xbl->abkl", Vd, Xc, Y, optimize=False)
    return np.einsum("ax,xbk,xl->abkl", Vd, Xc, Y, optimize=False)


def _sym(Z, mode):
    """Z + Z^dagger over the family axes: trace mode 2 Re z; family mode trailing [r, r]."""
    if mode == "trace":
        return 2.0 * np.real(Z)
    return Z + np.conj(np.swapaxes(Z, -1, -2))


def _anti(Z, mode, hbar):
    """(i/hbar)(Z - Z^dagger): trace mode -(2/hbar) Im z; family mode trailing [r, r]."""
    if mode == "trace":
        return (-2.0 / hbar) * np.imag(Z)
    return (1j / hbar) * (Z - np.conj(np.swapaxes(Z, -1, -2)))


def _derivative_terms(*, arrays, applied, Vd, sig, m, mode, hbar):
    """Same-state time-derivative pieces for one output family (module docstring, TIME
    DERIVATIVES; ADDENDUM item 1).

    arrays: named columns L, HL, H2L (primal) and, for m > 0, dL, HdL, H2dL, BL, BHL, HBL
    (tangent-shaped). Diagonal outputs pass Vd [n_a, D]; one E_alpha output passes Vd None
    and applied = {L: E L, HL: E H L, H2L: E H^2 L (m > 0)}, using <X|E Y> = <E X|Y>.
    Returns d1 = <L_A>, d2 = <A_A> and, for m > 0, hom1, hom2 (homogeneous tangent
    derivatives) and G1, G2 (explicit source/K' contact coefficients).
    """
    def pair(x, y):
        if Vd is not None:
            return _pair_diag(Vd, arrays[x], arrays[y], sig, mode)
        if y in applied:
            return _pair_applied(arrays[x], applied[y], sig, mode)
        return _pair_applied(applied[x], arrays[y], sig, mode)

    hb2 = hbar * hbar
    out = {
        "d1": _anti(pair("HL", "L"), mode, hbar),
        "d2": -(_sym(pair("H2L", "L"), mode) - _sym(pair("HL", "HL"), mode)) / hb2,
    }
    if m > 0:
        P = (1j / hbar) * (pair("HL", "dL") - pair("L", "HdL"))
        Q = pair("H2L", "dL") - 2.0 * pair("HL", "HdL") + pair("L", "H2dL")
        U = pair("HBL", "L") + pair("BHL", "L") - 2.0 * pair("BL", "HL")
        out["hom1"] = _sym(P, mode)
        out["hom2"] = -_sym(Q, mode) / hb2
        out["G1"] = _anti(pair("BL", "L"), mode, hbar)
        out["G2"] = -_sym(U, mode) / hb2
    return out


def _contract_node(*, operator, S, r, m, D, sig, mode, cells, values, presence, dt, budget,
                   failures, normE, normH, consistency_tolerance, where, cE, dO, hbar):
    """Means, responses and their time derivatives of H, every E_alpha, every read and
    presence at one node.

    trace mode : scalars  <A> = sum_k s_k <l_k|A|l_k>,  2 Re sum_k s_k <l_k|A|dl_bk>.
    family mode: r x r    M_kl = <v_k|A|v_l>,  K_kl = <v_k|A|dv_bl> + <dv_bk|A|v_l>.
    E_alpha and H are applied through the operator (Hermitian premise: <A l|dl> = <l|A|dl>);
    reads/presence are contracted with their materialized diagonals. v002: the same-state
    first/second time derivatives (module docstring, TIME DERIVATIVES) use H applied to
    [L, dL] and to its image, B_b L and B_b H L (cE, dO), H B_b L, and E_alpha applied to
    [L, H L, H^2 L]; the v001 means/responses use the same H L and E_alpha L columns.
    """
    L = S[:, :r]
    dLr = S[:, r:].reshape(D, m, r)
    Lc = np.conj(L)
    Y1 = _apply_block(operator=operator, method="apply_H", kwargs={}, block=S, D=D, dt=dt,
                      budget=budget, failures=failures, bound=normH,
                      consistency_tolerance=consistency_tolerance,
                      what=f"H mean and first time derivative at {where}")
    if Y1 is None:
        return None
    Y2 = _apply_block(operator=operator, method="apply_H", kwargs={}, block=Y1, D=D, dt=dt,
                      budget=budget, failures=failures, bound=normH,
                      consistency_tolerance=consistency_tolerance,
                      what=f"second time derivative at {where}")
    if Y2 is None:
        return None
    HL = Y1[:, :r]
    H2L = Y2[:, :r]
    arrays = {"L": L, "HL": HL, "H2L": H2L}
    if m > 0:
        arrays.update({"dL": dLr, "HdL": Y1[:, r:].reshape(D, m, r),
                       "H2dL": Y2[:, r:].reshape(D, m, r)})
        # Source generators B_b = sum_alpha cE[b,alpha] E_alpha - diag(dO_b) on L and H L.
        BL = np.zeros((D, m, r), dtype=dt)
        BHL = np.zeros((D, m, r), dtype=dt)
        LHL = np.concatenate([L, HL], axis=1)
        for ia, alpha in enumerate(cells):
            bs = [b for b in range(m) if float(cE[b, ia]) != 0.0]
            if not bs:
                continue
            Zb = _apply_block(operator=operator, method="apply_E", kwargs={"alpha": alpha},
                              block=LHL, D=D, dt=dt, budget=budget, failures=failures,
                              bound=normE[ia], consistency_tolerance=consistency_tolerance,
                              what=f"source generators at {where}, cell index {ia}")
            if Zb is None:
                return None
            for b in bs:
                coeff = float(cE[b, ia])
                BL[:, b, :] += coeff * Zb[:, :r]
                BHL[:, b, :] += coeff * Zb[:, r:]
        del LHL
        for b in range(m):
            BL[:, b, :] -= dO[b][:, None] * L
            BHL[:, b, :] -= dO[b][:, None] * HL
        HB = _apply_block(operator=operator, method="apply_H", kwargs={},
                          block=BL.reshape(D, m * r), D=D, dt=dt, budget=budget,
                          failures=failures, bound=normH,
                          consistency_tolerance=consistency_tolerance,
                          what=f"H on source generators at {where}")
        if HB is None:
            return None
        arrays.update({"BL": BL, "BHL": BHL, "HBL": HB.reshape(D, m, r)})
        Eblock = np.concatenate([L, HL, H2L], axis=1)
    else:
        Eblock = np.concatenate([L, HL], axis=1)
    n_E = len(cells)
    out = {}
    if mode == "trace":
        out["H"] = complex(np.einsum("xk,xk,k->", Lc, HL, sig, optimize=False))
        E_mean = np.zeros(n_E, dtype=np.complex128)
        E_resp = np.zeros((n_E, m), dtype=np.float64)
        Ed = {"d1": np.zeros(n_E, dtype=np.float64), "d2": np.zeros(n_E, dtype=np.float64)}
        Ed.update({key: np.zeros((n_E, m), dtype=np.float64)
                   for key in ("hom1", "hom2", "G1", "G2")})
    else:
        out["H"] = np.einsum("xk,xl->kl", Lc, HL, optimize=False).astype(np.complex128)
        E_mean = np.zeros((n_E, r, r), dtype=np.complex128)
        E_resp = np.zeros((n_E, m, r, r), dtype=np.complex128)
        Ed = {"d1": np.zeros((n_E, r, r), dtype=np.complex128),
              "d2": np.zeros((n_E, r, r), dtype=np.complex128)}
        Ed.update({key: np.zeros((n_E, m, r, r), dtype=np.complex128)
                   for key in ("hom1", "hom2", "G1", "G2")})
    for ia, alpha in enumerate(cells):
        Z = _apply_block(operator=operator, method="apply_E", kwargs={"alpha": alpha},
                         block=Eblock, D=D, dt=dt, budget=budget, failures=failures,
                         bound=normE[ia], consistency_tolerance=consistency_tolerance,
                         what=f"E mean/response/time derivatives at {where}, cell index {ia}")
        if Z is None:
            return None
        EL = Z[:, :r]
        if mode == "trace":
            E_mean[ia] = np.einsum("xk,xk,k->", Lc, EL, sig, optimize=False)
            E_resp[ia] = 2.0 * np.einsum("xk,xbk,k->b", np.conj(EL), dLr, sig,
                                         optimize=False).real
        else:
            E_mean[ia] = np.einsum("xk,xl->kl", Lc, EL, optimize=False)
            Mb = np.einsum("xk,xbl->bkl", np.conj(EL), dLr, optimize=False)
            E_resp[ia] = Mb + np.conj(np.swapaxes(Mb, 1, 2))
        applied = {"L": EL, "HL": Z[:, r:2 * r]}
        if m > 0:
            applied["H2L"] = Z[:, 2 * r:3 * r]
        terms = _derivative_terms(arrays=arrays, applied=applied, Vd=None, sig=sig, m=m,
                                  mode=mode, hbar=hbar)
        for key, val in terms.items():
            Ed[key][ia] = val
    out["E"] = E_mean
    out["E_resp"] = E_resp
    if mode == "trace":
        w = np.einsum("xk,xk,k->x", Lc, L, sig, optimize=False).real
        z = np.einsum("xk,xbk,k->bx", Lc, dLr, sig, optimize=False).real
        out["O"] = np.einsum("ax,x->a", values, w, optimize=False)
        out["P"] = np.einsum("ax,x->a", presence, w, optimize=False)
        out["O_resp"] = 2.0 * np.einsum("ax,bx->ab", values, z, optimize=False)
        out["P_resp"] = 2.0 * np.einsum("ax,bx->ab", presence, z, optimize=False)
    else:
        out["O"] = np.einsum("ax,xk,xl->akl", values, Lc, L, optimize=False)
        out["P"] = np.einsum("ax,xk,xl->akl", presence, Lc, L, optimize=False)
        Ob = np.einsum("ax,xk,xbl->abkl", values, Lc, dLr, optimize=False)
        Pb = np.einsum("ax,xk,xbl->abkl", presence, Lc, dLr, optimize=False)
        out["O_resp"] = Ob + np.conj(np.swapaxes(Ob, 2, 3))
        out["P_resp"] = Pb + np.conj(np.swapaxes(Pb, 2, 3))
    Od = _derivative_terms(arrays=arrays, applied=None, Vd=values, sig=sig, m=m, mode=mode,
                           hbar=hbar)
    Pd = _derivative_terms(arrays=arrays, applied=None, Vd=presence, sig=sig, m=m, mode=mode,
                           hbar=hbar)
    # Output order as v001: all E_alpha, then every read row; presence rows separately.
    out["deriv"] = {key: np.concatenate([Ed[key], Od[key]], axis=0) for key in Od}
    out["deriv_P"] = Pd
    out["norm_L"] = _fro(L)
    out["norm_dL"] = np.array([_fro(dLr[:, b, :]) for b in range(m)], dtype=np.float64)
    return out


def _node_bounds(*, opnorm, eps_L, eps_b, norm_L, norm_L0, norm_dL, Bnorm, R1, absint,
                 hbar):
    """Per-entry bounds at a node for outputs with operator norms opnorm [n_out].

    mean[o]    = ||A_o|| (eps_L (||L_N||_F + ||L0||_F) + R1)
    resp[o, b] = 2 ||A_o|| (eps_L ||dL_bN||_F + ||L0||_F eps_b + ||B_b|| R1 int|f_b| / hbar)
    From <l_N|A|l_N> - <l|A|l> = <e|A|l_N> + <l|A|e>, <l_N|A|dl_N> - <l|A|dl> =
    <e|A|dl_N> + <l|A|e_b>, Cauchy-Schwarz over columns, ||L(t)||_F = ||L0||_F, and the
    factorization residual R (trace norm <= R1): |Tr A U R U^dagger| <= ||A|| R1 and its
    response |.| <= 2 ||A|| ||B_b|| R1 int|f_b| / hbar.
    """
    mean = opnorm * (eps_L * (norm_L + norm_L0) + R1)
    per_b = eps_L * norm_dL + norm_L0 * eps_b + Bnorm * R1 * absint / hbar
    resp = 2.0 * opnorm[:, None] * per_b[None, :]
    return mean, resp


def _entries_estimate(*, D, r, m, P1, n_out, n_read, n_obs, mode):
    """Estimate of array entries held by this module (operator internals excluded).

    Propagation: S, T, Tn, Y, acc, the apply copy and a cast (7 (1+m) r columns), forcing
    G, F, column selection, apply copy and output (5 m r), the Taylor window (P+1) r, node
    contraction temporaries (4 r), dO (m) and the probe (1), all times D; plus outputs,
    bounds and by-kind copies (r x r complex in family mode, with the einsum temporaries).
    v002 time derivatives add, conservatively and as if simultaneous with propagation:
    node columns H[L, dL] and H^2[L, dL] (2 (1+m) r), B L, B H L, H B L with apply copies
    (6 m r), [L, H L] and [L, H L, H^2 L] with apply copies/outputs (16 r), conjugate and
    trace-weight temporaries (4 m), all times D; plus derivative outputs (mean first/second,
    homogeneous/contact pieces, one-sided totals), their bounds, by-kind copies and profile
    node values, and 12 (n_out + n_read)(1 + m) per-node derivative temporaries (each
    [r, r] complex in family mode).
    """
    cols = (1 + m) * r
    entries = D * (7 * cols + 5 * m * r + P1 * r + 4 * r + m + 1)
    entries += D * (2 * cols + 6 * m * r + 16 * r + 4 * m)
    deriv_vals = (n_out + n_read) * n_obs * (2 + 8 * m) + n_read * n_obs * (4 + 4 * m)
    deriv_bds = (n_out + n_read) * n_obs * (2 + 8 * m) + 4 * m * n_obs
    deriv_tmp = 12 * (n_out + n_read) * (1 + m)
    if mode == "trace":
        entries += 3 * (n_out + n_read + 1) * n_obs * (1 + m)
        entries += deriv_vals + deriv_bds + deriv_tmp
    else:
        rr = r * r
        entries += (3 * (n_out + n_read + 1) * n_obs * (1 + m) * rr
                    + 4 * n_read * m * rr + 2 * (n_out - n_read) * m * rr)
        entries += (deriv_vals + deriv_tmp) * rr + deriv_bds
    return entries


def _profile_node_values(*, prof, grid):
    """One-sided node values of the declared per-interval polynomial profiles (L16).

    prof[b, k, p] multiplies (t - t_k)^p on [t_k, t_{k+1}]. Returns float64 [m, K] arrays:
    f_left, df_left  = f_b and f_b' at node k+1 from interval k (tau = t_{k+1} - t_k);
    f_right, df_right = f_b and f_b' at node k from interval k (tau = 0).
    Exact algebra evaluated in float64; no interpolation or side choice.
    """
    m, K, P1 = prof.shape
    f_left = np.zeros((m, K), dtype=np.float64)
    df_left = np.zeros((m, K), dtype=np.float64)
    f_right = prof[:, :, 0].copy()
    df_right = prof[:, :, 1].copy() if P1 > 1 else np.zeros((m, K), dtype=np.float64)
    for k in range(K):
        tau = float(grid[k + 1]) - float(grid[k])
        for p in range(P1):
            f_left[:, k] += prof[:, k, p] * (tau ** p)
            if p >= 1:
                df_left[:, k] += float(p) * prof[:, k, p] * (tau ** (p - 1))
    return f_left, df_left, f_right, df_right


# ---------------------------------------------------------------------------
# Result skeletons
# ---------------------------------------------------------------------------

def _contacts_statement():
    return {
        "coordinate": (
            "affine lapse n = N - 1 and read sources j: H[n, j] = H + sum_alpha n_alpha "
            "E_alpha - sum_A j_A O_A, linear in (n, j); E_alpha carry the adopted V002 "
            "support-mean placement (provisional, counted assumption)"
        ),
        "hamiltonian_second_order": {
            "H_nn": 0.0, "H_nj": 0.0, "H_jj": 0.0,
            "statement": (
                "zero in the affine n coordinate for this linear rule; any other "
                "coordinate (e.g. g00) generates nonzero contacts that must be added to "
                "the W second derivatives BEFORE any Schur complement"
            ),
        },
        "read": {
            "value": 0.0,
            "statement": (
                "E_alpha, O_A and presence are source-independent operators in this "
                "rule; a source-dependent read or registration needs its own contact"
            ),
        },
        "preparation": {
            "value": 0.0,
            "statement": (
                "fixed preparation, delta psi_b(t0) = 0; a varied or re-prepared state "
                "(e.g. equilibrium at shifted lapse) is a different experiment whose "
                "covariance/preparation terms are not computed here"
            ),
        },
        "registration": {
            "value": 0.0,
            "statement": (
                "support weights w_alphaX, presence and 1/m_alpha normalization are "
                "state-dependent diagonal parts INSIDE module A's operators; their "
                "registration is fixed and not source dependent here"
            ),
        },
        "one_point": (
            "W_n = -<E_alpha>(t) and W_j = <O_A>(t) are means['E'] and means['O']; they "
            "feed every reparametrization contact"
        ),
        "g00_coordinate": (
            "g00 = -(1 + 2 n_g), N = sqrt(1 + 2 n_g): use g00_lapse_coordinate_contact. At "
            "the flat point dn/dn_g = 1, d2n/dn_g2 = -1, H_{n_g n_g} = -E_alpha (uniform: "
            "-H), and the W_{n_g n_g} contact is +<E_alpha>(t) delta_{alpha beta} "
            "delta(t - s); it is exposed, never dropped"
        ),
        "moments": (
            "raw first and second means and their responses are returned separately "
            "(by read kind token); centered covariance is a caller-side combination: "
            "delta C = delta M - delta mu mu^T - mu delta mu^T, with second derivatives "
            "containing products of first derivatives AND actual second mean "
            "derivatives; covariance-only response is never inverted here; the "
            "register-spec property tr C <= 4 is documented, never clipped"
        ),
        "time_derivatives": {
            "read_frame_partial": {
                "value": 0.0,
                "statement": (
                    "declared read_frame 'fixed_current_state_reads': every E_alpha, read and "
                    "presence row is a fixed current-state operator with fixed registration, "
                    "frame, scale and support, so partial_t A = partial_t^2 A = 0 and the "
                    "(2i/hbar)[K, partial_t A] term of A_O is zero; 1/m_alpha, presence and "
                    "adjacency changes are inside A and act through the commutator (no "
                    "separate count derivative). Other declarations fail explicitly"
                ),
            },
            "background_generator_K_prime": {
                "value": 0.0,
                "statement": (
                    "declared background_generator 'flat_point_time_independent_H': the "
                    "zeroth-order generator is K = H at n = 0, j = 0, N_bg = 1, tau = t, so "
                    "K' = 0 for the means; a nonzero or time-dependent background lapse/source "
                    "needs H[n0(t), j0(t)] and fails explicitly (LIMITATIONS L4, L17)"
                ),
            },
            "source_generator_K_prime": (
                "first order: K = H + sum_b f_b(t) B_b, K' = sum_b f_b'(t) B_b; its term "
                "f_b'(t) G1[A,b] = (i/hbar) <[K',A]>_0 is RETAINED in every response second "
                "derivative and returned separately (time_derivatives['response'] contact_G1 "
                "with profile_at_nodes df), never dropped"
            ),
            "proper_time": (
                "derivatives are in the native time t of time_grid. For a homogeneous "
                "background lapse N_bg(t): d/dtau = N_bg^-1 d/dt, d2/dtau2 = N_bg^-2 d2/dt2 "
                "- N_bg^-3 (dN_bg/dt) d/dt. Linearized about N_bg = 1 for a uniform lapse "
                "column with all energy coefficients equal to c (delta N_bg = c f_b): "
                "delta(dA/dtau) = delta(dA/dt) - c f_b dA/dt, delta(d2A/dtau2) = "
                "delta(d2A/dt2) - 2 c f_b d2A/dt2 - c f_b' dA/dt; every ingredient is "
                "returned. A spatially nonuniform lapse keeps the coordinate-time foliation "
                "(HP addendum); per-cell clocks are not averaged here"
            ),
            "c_number_frame": (
                "a registered frame acting linearly on fixed rows, O(t) = T(t) O, is a "
                "caller-side combination: d<TO>/dt = T'<O> + T<O>', d2<TO>/dt2 = T''<O> + "
                "2 T'<O>' + T<O>'' (and the same for responses); on the source side it is "
                "represented exactly by fixed-row columns whose declared profiles carry the "
                "frame time dependence, whose K' terms are then the returned f_b' G1"
            ),
        },
    }


def _new_propagation_result():
    return {
        "ok": False,
        "stage_reached": None,
        "failures": [],
        "flags": [],
        "means": None,
        "response": None,
        "time_derivatives": None,
        "error_bounds": None,
        "contacts": _contacts_statement(),
        "resources": {},
        "conventions": {
            "sources": (
                "V_b(t) = f_b(t) (sum_alpha cE[b,alpha] E_alpha - sum_A cO[b,A] O_A); energy "
                "columns +f E_alpha, read (first-moment or pair) columns -f O_A"
            ),
            "response": (
                "response[o, b, t] = delta<A_o>(t) = 2 Re sum_k s_k <l_k(t)|A_o|dl_bk(t)> = "
                "int ds f_b(s)(sum_A cO[b,A] chi_{o,A}(t,s) - sum_alpha cE[b,alpha] "
                "chi_{o,E_alpha}(t,s)), chi_AB(t,s) = (i/hbar) theta(t-s) Tr rho0 "
                "[A_H(t), B_H(s)]"
            ),
            "outputs": "all E_alpha (operator.energy_cells order), then every operator read row",
            "profiles": (
                "profiles[b, k, p] multiplies (t - t_k)^p on [t_k, t_{k+1}]; observation "
                "times are the time-grid nodes"
            ),
            "units": "one caller-declared consistent system; no conversion",
            "reduction": "full-H propagation only; no P/Q reduction is implemented",
            "time_derivatives": (
                "native time t; means first = <L_A> = (i/hbar)<[H,A]>, second = <A_A> = "
                "-(1/hbar^2)<[H,[H,A]]>; response first = hom1 + f_b G1, second = hom2 + "
                "f_b G2 + f_b' G1 (f_b' G1 = (i/hbar)<[K',A]>_0), one-sided at nodes: left = "
                "nodes 1..K from interval k-1, right = nodes 0..K-1 from interval k"
            ),
        },
    }


# ---------------------------------------------------------------------------
# Public: propagate_source_columns
# ---------------------------------------------------------------------------

def propagate_source_columns(*, operator, preparation, source_columns, time_grid, hbar,
                             stepper, caps, dtype, time_derivative_contacts):
    """Same-state full-H primal + tangent propagation; native means and joint responses.

    Arguments (keyword-only, required, no defaults):
      operator: any object with the shared module-A members dimension, basis_key,
        index_of, primitive_events, apply_H(*, block), energy_cells, apply_E(*, alpha,
        block), read_labels, read_values(), read_presence(), apply_O(*, read_index, block),
        norm_bound_H(), norm_bound_E(*, alpha), resources(). Module A is not imported.
      preparation: exactly one of
        {"kind": "purification", "factor": L [D, r], "trace_tolerance": t}
            rho0 = L L^dagger; |Tr L^dagger L - 1| <= t is required (never renormalized);
        {"kind": "density", "rho": rho [D, D], "trace_tolerance": t,
         "hermiticity_tolerance": th, "psd_tolerance": tp}
            max|rho - rho^dagger| <= th, |Tr rho - 1| <= t, lambda_min >= -tp; factorized as
            a signed full-rank factor (LIMITATIONS L7), never made low-rank;
        {"kind": "family_isometry", "isometry": V [D, r], "isometry_tolerance": ti}
            max|V^dagger V - I| <= ti; outputs are r x r compressed matrices for the
            declared reference family (LIMITATIONS L8), not a default state.
      source_columns: {"labels": m unique strings,
        "energy_coefficients": real [m, n_E] (sign +, operator.energy_cells order),
        "read_coefficients": real [m, n_read] (sign -, operator.read_labels order;
            first-moment AND pair rows per 0406 item 1),
        "profiles": real [m, K, P+1] per-interval polynomial coefficients}.
        m = 0 is admitted (means only); pass ndarrays of shape (0, ...) then.
      time_grid: real strictly increasing [K+1], K >= 1; t0 = time_grid[0] is the fixed
        preparation time; observations at every node.
      hbar: finite real > 0, in the caller's units.
      stepper: {"method": "taylor_residual", "max_order": int > 0,
        "max_step_norm_product": real > 0 (each substep h has h norm_bound_H / hbar <= it),
        "residual_tolerance": real > 0 (per-substep integrated residual bound, primal and
            every tangent, Frobenius units),
        "consistency_tolerance": real > 0 (relative slack for the norm-bound observation and
            the apply_O versus read_values diagonal check; keep it at rounding level: the
            error bounds always use the declared norms unchanged, never the slack)}.
      caps: {"max_working_entries": int > 0, "max_column_applications": int > 0,
        "max_substeps": int > 0}; exceeded caps fail explicitly before being exceeded.
      dtype: a complex numpy dtype for all propagated arrays.
      time_derivative_contacts (v002, ADDENDUM item 1; LIMITATIONS L17): {"read_frame":
        "fixed_current_state_reads", "background_generator": "flat_point_time_independent_H"}
        -- the explicit declaration of the read/frame partial-derivative and background
        generator K' terms (both zero for these declarations); any other key set or value
        fails explicitly, never silently dropped.

    Returns a dict {ok, stage_reached, failures, flags, means, response, time_derivatives,
    error_bounds, contacts, resources, conventions}. means, response, time_derivatives and
    error_bounds are filled only on complete success. Shapes (n_obs = K + 1,
    n_out = n_E + n_read):
      trace mode (purification, density):
        means["E"] [n_E, n_obs], means["H"] [n_obs], means["O"] [n_read, n_obs],
        means["presence"] [n_read, n_obs], means["by_kind"][token] = {"rows", "O",
        "presence"}; response["values"] [n_out, m, n_obs], response["presence"]
        [n_read, m, n_obs], response["by_kind"][token] = {"output_rows", "values",
        "presence"}.
      family mode: the same keys with trailing [r, r] complex Hermitian compressed axes.
      error_bounds: "means" [n_out, n_obs], "H_mean" [n_obs], "presence_means"
        [n_read, n_obs], "response" [n_out, m, n_obs], "presence_response"
        [n_read, m, n_obs], "primal_state_fro" [n_obs], "tangent_state_fro" [m, n_obs],
        "source_quadrature" 0.0, plus statements of what is and is not covered.
      time_derivatives (v002; trace mode shown, family mode adds trailing [r, r]):
        "means": {"first", "second" [n_out, n_obs], "presence_first", "presence_second"
          [n_read, n_obs], "by_kind"[token] = {"rows", "output_rows", "first", "second",
          "presence_first", "presence_second"}};
        "response": {"homogeneous_first", "homogeneous_second", "contact_G1", "contact_G2"
          [n_out, m, n_obs] and "presence_..." [n_read, m, n_obs] versions;
          "profile_at_nodes": {"left": {"nodes", "f", "df"}, "right": {...}} with [m, K];
          "left": {"nodes" (1..K), "first", "second" [n_out, m, K], "presence_first",
          "presence_second" [n_read, m, K]}; "right": the same for nodes 0..K-1;
          "by_kind"[token] = {"output_rows", "left_first", "left_second", "right_first",
          "right_second"}}.
        error_bounds["time_derivatives"] holds a real bound array of the same leading
        shape for every array above (no by_kind copies), plus covered/not-covered text.
    """
    result = _new_propagation_result()
    failures = result["failures"]
    resources = result["resources"]

    # ---- Stage 1: control inputs ---------------------------------------------------
    result["stage_reached"] = "inputs"
    hbar_in = _admit_positive_real("hbar", hbar, failures)
    dt = None
    try:
        dt = np.dtype(dtype)
    except TypeError as exc:
        failures.append(f"input dtype: not a numpy dtype ({exc})")
    if dt is not None and dt.kind != "c":
        failures.append(f"input dtype: {dt!r} is not a complex dtype")
        dt = None
    stp = _admit_mapping("stepper", stepper, ("method", "max_order", "max_step_norm_product",
                                              "residual_tolerance", "consistency_tolerance"),
                         failures)
    max_order = kappa = tol = ctol = None
    if stp is not None:
        if stp["method"] != "taylor_residual":
            failures.append(f"input stepper.method: {stp['method']!r} is not 'taylor_residual'")
        max_order = _admit_positive_int("stepper.max_order", stp["max_order"], failures)
        kappa = _admit_positive_real("stepper.max_step_norm_product",
                                     stp["max_step_norm_product"], failures)
        tol = _admit_positive_real("stepper.residual_tolerance", stp["residual_tolerance"],
                                   failures)
        ctol = _admit_positive_real("stepper.consistency_tolerance",
                                    stp["consistency_tolerance"], failures)
    cp = _admit_mapping("caps", caps, ("max_working_entries", "max_column_applications",
                                       "max_substeps"), failures)
    cap_entries = cap_cols = cap_sub = None
    if cp is not None:
        cap_entries = _admit_positive_int("caps.max_working_entries",
                                          cp["max_working_entries"], failures)
        cap_cols = _admit_positive_int("caps.max_column_applications",
                                       cp["max_column_applications"], failures)
        cap_sub = _admit_positive_int("caps.max_substeps", cp["max_substeps"], failures)
    # v002 (ADDENDUM item 1; LIMITATIONS L17): explicit read/frame and background-generator
    # declarations for the time-derivative reads; unsupported declarations fail closed.
    tdc = _admit_mapping("time_derivative_contacts", time_derivative_contacts,
                         ("read_frame", "background_generator"), failures)
    if tdc is not None:
        rf = tdc["read_frame"]
        if not (isinstance(rf, str) and rf == _READ_FRAME_FIXED):
            failures.append(
                f"input time_derivative_contacts.read_frame: {rf!r} is not "
                f"{_READ_FRAME_FIXED!r}; an explicitly time-dependent read, registration, "
                "frame, scale or support needs its partial derivatives and transformed "
                "generator, which the shared operator interface cannot supply (not dropped)"
            )
        bg = tdc["background_generator"]
        if not (isinstance(bg, str) and bg == _BACKGROUND_FLAT):
            failures.append(
                f"input time_derivative_contacts.background_generator: {bg!r} is not "
                f"{_BACKGROUND_FLAT!r}; a nonzero or time-dependent background lapse/source "
                "generator (K' != 0 at zeroth order) is not implemented (LIMITATIONS L4)"
            )
    grid = _admit_array("time_grid", time_grid, 1, False, failures)
    if grid is not None:
        if grid.shape[0] < 2:
            failures.append("input time_grid: at least two nodes are required")
        elif not bool(np.all(grid[1:] > grid[:-1])):
            failures.append("input time_grid: nodes must be strictly increasing")
    if failures:
        return result
    K = int(grid.shape[0]) - 1
    n_obs = K + 1
    rdt = np.empty(0, dtype=dt).real.dtype
    budget = {"cap": cap_cols, "used": 0,
              "by_method": {"apply_H": 0, "apply_E": 0, "apply_O": 0}}
    resources["dtype"] = str(dt)
    resources["unit_roundoff"] = float(np.finfo(dt).eps)
    resources["column_applications"] = budget

    # ---- Stage 2: operator ---------------------------------------------------------
    result["stage_reached"] = "operator"
    required = ("dimension", "basis_key", "index_of", "primitive_events", "apply_H",
                "energy_cells", "apply_E", "read_labels", "read_values", "read_presence",
                "apply_O", "norm_bound_H", "norm_bound_E", "resources")
    callables = ("basis_key", "index_of", "primitive_events", "apply_H", "apply_E",
                 "read_values", "read_presence", "apply_O", "norm_bound_H", "norm_bound_E",
                 "resources")
    members = {}
    for name in required:
        present, value = _member(operator, name)
        if not present:
            failures.append(f"operator: required member {name!r} missing ({value})")
            continue
        if name in callables and not callable(value):
            failures.append(f"operator: member {name!r} is not callable")
            continue
        members[name] = value
    if failures:
        return result
    D = members["dimension"]
    if isinstance(D, (bool, np.bool_)) or not isinstance(D, (int, np.integer)) or int(D) <= 0:
        failures.append(f"operator: dimension {D!r} is not a positive integer")
        return result
    D = int(D)
    try:
        cells = tuple(members["energy_cells"])
        labels = tuple(members["read_labels"])
    except TypeError as exc:
        failures.append(f"operator: energy_cells/read_labels not iterable ({exc})")
        return result
    n_E = len(cells)
    n_read = len(labels)
    if n_E == 0:
        failures.append("operator: energy_cells is empty; no E_alpha outputs or lapse sources")
    try:
        if len(set(cells)) != n_E:
            failures.append("operator: energy_cells contains duplicate labels")
    except TypeError as exc:
        failures.append(f"operator: energy_cells labels are not hashable ({exc})")
    if failures:
        return result
    ok, nH = _call(failures, "norm_bound_H()", members["norm_bound_H"], {})
    normH = _admit_nonnegative_real("operator.norm_bound_H()", nH, failures) if ok else None
    normE = []
    for ia, alpha in enumerate(cells):
        ok, nE = _call(failures, f"norm_bound_E(alpha=cells[{ia}])", members["norm_bound_E"],
                       {"alpha": alpha})
        normE.append(_admit_nonnegative_real(f"operator.norm_bound_E(cells[{ia}])", nE, failures)
                     if ok else None)
    _, raw_values = _call(failures, "read_values()", members["read_values"], {})
    _, raw_presence = _call(failures, "read_presence()", members["read_presence"], {})
    _, op_resources = _call(failures, "resources()", members["resources"], {})
    if failures:
        return result
    values = _admit_array("operator.read_values()", raw_values, 2, False, failures)
    presence = _admit_array("operator.read_presence()", raw_presence, 2, False, failures)
    if not isinstance(op_resources, dict):
        failures.append(f"operator: resources() returned {type(op_resources).__name__}, not a dict")
    if failures:
        return result
    if values.shape != (n_read, D) or presence.shape != (n_read, D):
        failures.append(
            f"operator: read_values shape {values.shape!r} / read_presence shape "
            f"{presence.shape!r} must both be {(n_read, D)!r}"
        )
        return result
    if not bool(np.all((presence == 0.0) | (presence == 1.0))):
        failures.append("operator: read_presence entries must be exactly 0 or 1")
    if bool(np.any((presence == 0.0) & (values != 0.0))):
        failures.append("operator: read_values must be 0 where presence is 0 (absent reads)")
    kinds = [_read_kind(lab) for lab in labels]
    undeclared = [i for i, kd in enumerate(kinds) if kd is None]
    if undeclared:
        failures.append(
            f"operator: {len(undeclared)} read labels carry no declared kind token (first "
            f"indices {undeclared[:8]!r}); first-moment/pair typing is required (LIMITATIONS L1)"
        )
    if failures:
        return result
    rows_by_kind = {}
    for i, kd in enumerate(kinds):
        rows_by_kind.setdefault(kd, []).append(i)
    rows_by_kind = {kd: tuple(rows) for kd, rows in rows_by_kind.items()}
    normO = np.array([_max_abs(values[a]) for a in range(n_read)], dtype=np.float64)
    normP = np.array([_max_abs(presence[a]) for a in range(n_read)], dtype=np.float64)
    resources.update({"D": D, "n_energy_cells": n_E, "n_reads": n_read,
                      "read_kinds": {kd: len(rows) for kd, rows in rows_by_kind.items()},
                      "operator_resources": op_resources})
    # Diagonal consistency of apply_O with read_values on one non-constant vector
    # (necessary, not sufficient; LIMITATIONS L2). Counted against the column cap.
    probe = ((np.arange(D, dtype=np.float64) + 1.0) / float(D)).astype(dt)[:, None]
    for a in range(n_read):
        Yo = _apply_block(operator=operator, method="apply_O", kwargs={"read_index": a},
                          block=probe, D=D, dt=dt, budget=budget, failures=failures,
                          bound=None, consistency_tolerance=ctol,
                          what=f"diagonal consistency check of read {a}")
        if Yo is None:
            return result
        diff = _max_abs(Yo - values[a][:, None] * probe)
        if diff > ctol * max(1.0, float(normO[a])):
            failures.append(
                f"operator: apply_O(read_index={a}) differs from diag(read_values()[{a}]) by "
                f"{diff!r} > consistency_tolerance scale; reads must be diagonal"
            )
            return result

    # ---- Stage 3: source columns --------------------------------------------------------
    result["stage_reached"] = "sources"
    sc = _admit_mapping("source_columns", source_columns,
                        ("labels", "energy_coefficients", "read_coefficients", "profiles"),
                        failures)
    if sc is None:
        return result
    cE = _admit_array("source_columns.energy_coefficients", sc["energy_coefficients"], 2,
                      False, failures)
    cO = _admit_array("source_columns.read_coefficients", sc["read_coefficients"], 2, False,
                      failures)
    prof = _admit_array("source_columns.profiles", sc["profiles"], 3, False, failures)
    src_labels = sc["labels"]
    if failures:
        return result
    m = int(cE.shape[0])
    if cE.shape != (m, n_E):
        failures.append(f"source_columns.energy_coefficients: shape {cE.shape!r} is not [m, {n_E}]")
    if cO.shape != (m, n_read):
        failures.append(f"source_columns.read_coefficients: shape {cO.shape!r} is not "
                        f"[{m}, {n_read}]")
    if prof.shape[0] != m or prof.shape[1] != K or prof.shape[2] < 1:
        failures.append(f"source_columns.profiles: shape {prof.shape!r} is not [{m}, {K}, P+1>=1]")
    if not isinstance(src_labels, (tuple, list)) or len(src_labels) != m or not all(
            isinstance(s, str) for s in src_labels) or len(set(src_labels)) != m:
        failures.append(f"source_columns.labels: {m} unique strings are required")
    if failures:
        return result
    P1 = int(prof.shape[2])
    if m > 0:
        dO64 = np.einsum("ba,ax->bx", cO, values, optimize=False)
    else:
        dO64 = np.zeros((0, D), dtype=np.float64)
    dO = dO64.astype(rdt)
    Bnorm = np.array([
        sum(abs(float(cE[b, ia])) * normE[ia] for ia in range(n_E)) + _max_abs(dO64[b])
        for b in range(m)], dtype=np.float64)
    del dO64
    n_out = n_E + n_read
    resources.update({"n_sources": m, "profile_degree": P1 - 1,
                      "source_norm_bounds": Bnorm.copy()})

    # ---- Stage 4: substep plan (checked before any propagation) -------------------------
    result["stage_reached"] = "plan"
    nsub = []
    total_sub = 0
    for k in range(K):
        x = (float(grid[k + 1]) - float(grid[k])) * normH / (hbar_in * kappa)
        if not math.isfinite(x):
            failures.append(f"plan: substep count for interval {k} is not finite")
            return result
        nsub.append(max(1, int(math.ceil(x))))
        total_sub += nsub[-1]
        if total_sub > cap_sub:
            failures.append(f"caps: max_substeps {cap_sub} would be exceeded (interval {k}); "
                            "stopped before propagation")
            return result
    resources.update({"substeps_per_interval": tuple(nsub), "total_substeps": total_sub,
                      "working_entries_cap": cap_entries})

    # ---- Stage 5: preparation (memory cap checked before factor allocation) -------------
    result["stage_reached"] = "preparation"
    if not isinstance(preparation, dict) or "kind" not in preparation:
        failures.append("input preparation: a dict with a 'kind' entry is required")
        return result
    pkind = preparation["kind"]
    R1 = 0.0
    prep_report = {"kind": pkind}
    resources["preparation"] = prep_report
    if pkind == "purification":
        prep = _admit_mapping("preparation", preparation,
                              ("kind", "factor", "trace_tolerance"), failures)
        if prep is None:
            return result
        ttol = _admit_positive_real("preparation.trace_tolerance", prep["trace_tolerance"],
                                    failures)
        L0 = _admit_array("preparation.factor", prep["factor"], 2, True, failures)
        if failures:
            return result
        if L0.shape[0] != D or L0.shape[1] < 1:
            failures.append(f"input preparation.factor: shape {L0.shape!r} is not [D={D}, r>=1]")
            return result
        r = int(L0.shape[1])
        mode = "trace"
        entries = _entries_estimate(D=D, r=r, m=m, P1=P1, n_out=n_out, n_read=n_read,
                                    n_obs=n_obs, mode=mode)
        resources["working_entries_estimate"] = entries
        if entries > cap_entries:
            failures.append(f"caps: working-entry estimate {entries} > max_working_entries "
                            f"{cap_entries}; stopped before allocation")
            return result
        trace = _fro(L0) ** 2
        prep_report["trace"] = trace
        if not abs(trace - 1.0) <= ttol:
            failures.append(
                f"input preparation.factor: Tr L^dagger L = {trace!r} differs from 1 by more "
                f"than trace_tolerance {ttol!r} (never renormalized)"
            )
            return result
        sig = np.ones(r, dtype=np.float64)
    elif pkind == "density":
        prep = _admit_mapping("preparation", preparation,
                              ("kind", "rho", "trace_tolerance", "hermiticity_tolerance",
                               "psd_tolerance"), failures)
        if prep is None:
            return result
        ttol = _admit_positive_real("preparation.trace_tolerance", prep["trace_tolerance"],
                                    failures)
        htol = _admit_positive_real("preparation.hermiticity_tolerance",
                                    prep["hermiticity_tolerance"], failures)
        ptol = _admit_positive_real("preparation.psd_tolerance", prep["psd_tolerance"],
                                    failures)
        if failures:
            return result
        r = D
        mode = "trace"
        entries = 6 * D * D + _entries_estimate(D=D, r=r, m=m, P1=P1, n_out=n_out,
                                                n_read=n_read, n_obs=n_obs, mode=mode)
        resources["working_entries_estimate"] = entries
        if entries > cap_entries:
            failures.append(
                f"caps: dense density path needs about {entries} entries (full-rank factor, "
                f"never made low-rank) > max_working_entries {cap_entries}; stopped before "
                "factorization"
            )
            return result
        rho = _admit_array("preparation.rho", prep["rho"], 2, True, failures)
        if failures:
            return result
        if rho.shape != (D, D):
            failures.append(f"input preparation.rho: shape {rho.shape!r} is not {(D, D)!r}")
            return result
        rho = rho.astype(np.complex128, copy=False)
        herm_dev = _max_abs(rho - np.conj(rho.T))
        tr = complex(np.einsum("ii->", rho, optimize=False))
        prep_report.update({"hermiticity_deviation": herm_dev, "trace_real": tr.real,
                            "trace_imag": tr.imag})
        if not herm_dev <= htol:
            failures.append(f"input preparation.rho: max|rho - rho^dagger| = {herm_dev!r} > "
                            f"hermiticity_tolerance {htol!r}")
        if not abs(tr - 1.0) <= ttol:
            failures.append(f"input preparation.rho: |Tr rho - 1| = {abs(tr - 1.0)!r} > "
                            f"trace_tolerance {ttol!r}")
        if failures:
            return result
        rho_h = 0.5 * (rho + np.conj(rho.T))
        del rho
        try:
            lam, V = np.linalg.eigh(rho_h)
        except np.linalg.LinAlgError as exc:
            failures.append(f"preparation: eigh of the Hermitian part did not converge ({exc})")
            return result
        lam_min = float(lam[0])
        prep_report["lambda_min"] = lam_min
        if not lam_min >= -ptol:
            failures.append(f"input preparation.rho: lambda_min = {lam_min!r} < -psd_tolerance "
                            f"{-ptol!r} (not PSD within the declared tolerance)")
            return result
        # Signed full-rank factor: rho_h = L diag(sig) L^dagger, all D columns kept.
        sig = np.where(lam < 0.0, -1.0, 1.0).astype(np.float64)
        L0 = V * np.sqrt(np.abs(lam))[None, :]
        del V
        resid = rho_h - np.einsum("ik,k,jk->ij", L0, sig, np.conj(L0), optimize=False)
        R1 = math.sqrt(float(D)) * _fro(resid)
        del resid, rho_h
        n_negative = int(np.count_nonzero(lam < 0.0))
        prep_report.update({
            "negative_eigenvalues_retained_signed": n_negative,
            "exactly_zero_eigenvalues_kept": int(np.count_nonzero(lam == 0.0)),
            "factorization_trace_norm_bound_R1": R1,
            "columns": D,
        })
        if not math.isfinite(R1):
            failures.append("preparation: factorization residual is not finite")
            return result
        if n_negative:
            result["flags"].append(
                f"preparation: {n_negative} eigenvalues in [-psd_tolerance, 0) retained exactly "
                "with sign -1 (signed factor; rho not modified)"
            )
    elif pkind == "family_isometry":
        prep = _admit_mapping("preparation", preparation,
                              ("kind", "isometry", "isometry_tolerance"), failures)
        if prep is None:
            return result
        itol = _admit_positive_real("preparation.isometry_tolerance",
                                    prep["isometry_tolerance"], failures)
        L0 = _admit_array("preparation.isometry", prep["isometry"], 2, True, failures)
        if failures:
            return result
        if L0.shape[0] != D or L0.shape[1] < 1:
            failures.append(f"input preparation.isometry: shape {L0.shape!r} is not [D={D}, r>=1]")
            return result
        r = int(L0.shape[1])
        mode = "family"
        entries = _entries_estimate(D=D, r=r, m=m, P1=P1, n_out=n_out, n_read=n_read,
                                    n_obs=n_obs, mode=mode)
        resources["working_entries_estimate"] = entries
        if entries > cap_entries:
            failures.append(f"caps: working-entry estimate {entries} > max_working_entries "
                            f"{cap_entries}; stopped before allocation")
            return result
        gram = np.einsum("xk,xl->kl", np.conj(L0), L0, optimize=False)
        iso_dev = _max_abs(gram - np.eye(r))
        prep_report["isometry_deviation"] = iso_dev
        if not iso_dev <= itol:
            failures.append(f"input preparation.isometry: max|V^dagger V - I| = {iso_dev!r} > "
                            f"isometry_tolerance {itol!r}")
            return result
        sig = np.ones(r, dtype=np.float64)
        prep_report["statement"] = ("declared reference-family compression V^dagger(...)V; "
                                    "not a default physical state")
    else:
        failures.append(f"input preparation.kind: {pkind!r} is not 'purification', "
                        "'density' or 'family_isometry'")
        return result
    L0 = L0.astype(dt)
    norm_L0 = _fro(L0)
    cols = (1 + m) * r
    resources["r"] = r
    # v002 node work: apply_H on [L, dL], on its image and (m > 0) on B L; apply_E per cell
    # on [L, H L, H^2 L] ([L, H L] when m = 0) and per source-carrying cell on [L, H L].
    n_E_src = sum(1 for ia in range(n_E) if m > 0 and bool(np.any(cE[:, ia] != 0.0)))
    node_cols = (2 * cols + m * r + n_E * (3 if m > 0 else 2) * r + n_E_src * 2 * r)
    resources["worst_case_column_applications"] = (
        n_read + total_sub * (max_order + 1) * (cols + n_E * m * r) + n_obs * node_cols)

    # ---- Stage 6: propagation ------------------------------------------------------------
    result["stage_reached"] = "propagation"
    if mode == "trace":
        E_mean = np.zeros((n_E, n_obs), dtype=np.float64)
        H_mean = np.zeros(n_obs, dtype=np.float64)
        O_mean = np.zeros((n_read, n_obs), dtype=np.float64)
        P_mean = np.zeros((n_read, n_obs), dtype=np.float64)
        resp = np.zeros((n_out, m, n_obs), dtype=np.float64)
        P_resp = np.zeros((n_read, m, n_obs), dtype=np.float64)
    else:
        E_mean = np.zeros((n_E, n_obs, r, r), dtype=np.complex128)
        H_mean = np.zeros((n_obs, r, r), dtype=np.complex128)
        O_mean = np.zeros((n_read, n_obs, r, r), dtype=np.complex128)
        P_mean = np.zeros((n_read, n_obs, r, r), dtype=np.complex128)
        resp = np.zeros((n_out, m, n_obs, r, r), dtype=np.complex128)
        P_resp = np.zeros((n_read, m, n_obs, r, r), dtype=np.complex128)
    bd_mean = np.zeros((n_out, n_obs), dtype=np.float64)
    bd_H = np.zeros(n_obs, dtype=np.float64)
    bd_P = np.zeros((n_read, n_obs), dtype=np.float64)
    bd_resp = np.zeros((n_out, m, n_obs), dtype=np.float64)
    bd_Presp = np.zeros((n_read, m, n_obs), dtype=np.float64)
    eps_L_hist = np.zeros(n_obs, dtype=np.float64)
    eps_b_hist = np.zeros((m, n_obs), dtype=np.float64)
    # v002 time-derivative outputs (ADDENDUM item 1) and their bounds.
    if mode == "trace":
        tail, cdt = (), np.float64
    else:
        tail, cdt = (r, r), np.complex128
    TD = {"first": np.zeros((n_out, n_obs) + tail, dtype=cdt),
          "second": np.zeros((n_out, n_obs) + tail, dtype=cdt),
          "presence_first": np.zeros((n_read, n_obs) + tail, dtype=cdt),
          "presence_second": np.zeros((n_read, n_obs) + tail, dtype=cdt)}
    TR = {}
    for key in ("hom1", "hom2", "G1", "G2"):
        TR[key] = np.zeros((n_out, m, n_obs) + tail, dtype=cdt)
        TR["presence_" + key] = np.zeros((n_read, m, n_obs) + tail, dtype=cdt)
    BD = {key: np.zeros(arr.shape[:2], dtype=np.float64) for key, arr in TD.items()}
    BD.update({key: np.zeros(arr.shape[:3], dtype=np.float64) for key, arr in TR.items()})
    c1 = 2.0 * normH / hbar_in
    c2 = 4.0 * normH * normH / (hbar_in * hbar_in)
    opnorm = np.concatenate([np.array(normE, dtype=np.float64), normO])
    imag_max = 0.0
    drift_max = 0.0
    orders = []
    mass_max = 0.0

    S = np.zeros((D, cols), dtype=dt)
    S[:, :r] = L0
    del L0
    eps_L = 0.0
    eps_b = np.zeros(m, dtype=np.float64)
    absint = np.zeros(m, dtype=np.float64)

    for i in range(n_obs):
        if i > 0:
            k = i - 1
            h = (float(grid[k + 1]) - float(grid[k])) / nsub[k]
            for j in range(nsub[k]):
                where = f"interval {k}, substep {j}"
                a2 = _shift_scale(coeffs=prof[:, k, :], tau0=j * h, h=h)
                active = [bool(np.any(a2[b] != 0.0)) for b in range(m)]
                step = _taylor_substep(operator=operator, S=S, r=r, m=m, D=D, h=h,
                                       hbar=hbar_in, a2=a2, active=active, cE=cE, cells=cells,
                                       normE=normE, normH=normH, dO=dO, Bnorm=Bnorm, tol=tol,
                                       max_order=max_order, dt=dt, budget=budget,
                                       failures=failures, consistency_tolerance=ctol,
                                       where=where)
                if step is None:
                    return result
                S = step["S"]
                fint = h * np.array([sum(abs(float(a2[b, p])) / (p + 1) for p in range(P1))
                                     for b in range(m)], dtype=np.float64)
                eps_L = eps_L + step["rho_psi"]
                eps_b = eps_b + step["rho_b"] + (Bnorm / hbar_in) * eps_L * fint
                absint = absint + fint
                orders.append(step["order"])
                if step["term_mass_ratio"] is not None:
                    mass_max = max(mass_max, step["term_mass_ratio"])
        node = _contract_node(operator=operator, S=S, r=r, m=m, D=D, sig=sig, mode=mode,
                              cells=cells, values=values, presence=presence, dt=dt,
                              budget=budget, failures=failures, normE=normE, normH=normH,
                              consistency_tolerance=ctol, where=f"node {i}", cE=cE, dO=dO,
                              hbar=hbar_in)
        if node is None:
            return result
        if mode == "trace":
            imag_max = max(imag_max, abs(node["H"].imag), _max_abs(node["E"].imag))
            H_mean[i] = node["H"].real
            E_mean[:, i] = node["E"].real
        else:
            H_mean[i] = node["H"]
            E_mean[:, i] = node["E"]
        O_mean[:, i] = node["O"]
        P_mean[:, i] = node["P"]
        resp[:n_E, :, i] = node["E_resp"]
        resp[n_E:, :, i] = node["O_resp"]
        P_resp[:, :, i] = node["P_resp"]
        drift_max = max(drift_max, abs(node["norm_L"] - norm_L0))
        mean_b, resp_b = _node_bounds(opnorm=opnorm, eps_L=eps_L, eps_b=eps_b,
                                      norm_L=node["norm_L"], norm_L0=norm_L0,
                                      norm_dL=node["norm_dL"], Bnorm=Bnorm, R1=R1,
                                      absint=absint, hbar=hbar_in)
        bd_mean[:, i] = mean_b
        bd_resp[:, :, i] = resp_b
        hb, _ = _node_bounds(opnorm=np.array([normH]), eps_L=eps_L, eps_b=eps_b,
                             norm_L=node["norm_L"], norm_L0=norm_L0, norm_dL=node["norm_dL"],
                             Bnorm=Bnorm, R1=R1, absint=absint, hbar=hbar_in)
        bd_H[i] = hb[0]
        pm, pr = _node_bounds(opnorm=normP, eps_L=eps_L, eps_b=eps_b, norm_L=node["norm_L"],
                              norm_L0=norm_L0, norm_dL=node["norm_dL"], Bnorm=Bnorm, R1=R1,
                              absint=absint, hbar=hbar_in)
        bd_P[:, i] = pm
        bd_Presp[:, :, i] = pr
        eps_L_hist[i] = eps_L
        eps_b_hist[:, i] = eps_b
        # v002 time derivatives on the same state, and their Cauchy-Schwarz bounds
        # (module docstring, TIME DERIVATIVES / DERIVATIVE BOUNDS).
        TD["first"][:, i] = node["deriv"]["d1"]
        TD["second"][:, i] = node["deriv"]["d2"]
        TD["presence_first"][:, i] = node["deriv_P"]["d1"]
        TD["presence_second"][:, i] = node["deriv_P"]["d2"]
        if m > 0:
            for key in ("hom1", "hom2", "G1", "G2"):
                TR[key][:, :, i] = node["deriv"][key]
                TR["presence_" + key][:, :, i] = node["deriv_P"][key]
        base = eps_L * (node["norm_L"] + norm_L0) + R1
        for pre, onorm in (("", opnorm), ("presence_", normP)):
            for order, cfac, hkey in (("first", c1, "hom1"), ("second", c2, "hom2")):
                mb, rb = _node_bounds(opnorm=cfac * onorm, eps_L=eps_L, eps_b=eps_b,
                                      norm_L=node["norm_L"], norm_L0=norm_L0,
                                      norm_dL=node["norm_dL"], Bnorm=Bnorm, R1=R1,
                                      absint=absint, hbar=hbar_in)
                BD[pre + order][:, i] = mb
                BD[pre + hkey][:, :, i] = rb
            BD[pre + "G1"][:, :, i] = ((2.0 / hbar_in) * base) * (onorm[:, None]
                                                                  * Bnorm[None, :])
            BD[pre + "G2"][:, :, i] = ((8.0 * normH / (hbar_in * hbar_in)) * base) * (
                onorm[:, None] * Bnorm[None, :])

    # ---- Stage 7: finite admission and packaging ---------------------------------------
    result["stage_reached"] = "packaging"
    # v002: one-sided response time derivatives (LIMITATIONS L16) from the single-valued
    # homogeneous and contact pieces and the exact one-sided profile node values.
    f_left, df_left, f_right, df_right = _profile_node_values(prof=prof, grid=grid)
    ex = (None, slice(None), slice(None)) + (None,) * len(tail)
    exb = (None, slice(None), slice(None))
    sides = {}
    for side, fv, dfv, sl, nodes in (("left", f_left, df_left, slice(1, None),
                                      tuple(range(1, n_obs))),
                                     ("right", f_right, df_right, slice(0, K),
                                      tuple(range(0, K)))):
        f_e, df_e = fv[ex], dfv[ex]
        fa, dfa = np.abs(fv)[exb], np.abs(dfv)[exb]
        vals, bds = {"nodes": nodes}, {"nodes": nodes}
        for pre in ("", "presence_"):
            g1 = TR[pre + "G1"][:, :, sl]
            vals[pre + "first"] = TR[pre + "hom1"][:, :, sl] + f_e * g1
            vals[pre + "second"] = (TR[pre + "hom2"][:, :, sl] + f_e * TR[pre + "G2"][:, :, sl]
                                    + df_e * g1)
            bg1 = BD[pre + "G1"][:, :, sl]
            bds[pre + "first"] = BD[pre + "hom1"][:, :, sl] + fa * bg1
            bds[pre + "second"] = (BD[pre + "hom2"][:, :, sl] + fa * BD[pre + "G2"][:, :, sl]
                                   + dfa * bg1)
        sides[side] = {"f": fv, "df": dfv, "values": vals, "bounds": bds}
    named = (("means E", E_mean), ("means H", H_mean), ("means O", O_mean),
             ("means presence", P_mean), ("response", resp), ("presence response", P_resp),
             ("bound means", bd_mean), ("bound H", bd_H), ("bound presence", bd_P),
             ("bound response", bd_resp), ("bound presence response", bd_Presp),
             ("primal state bound", eps_L_hist), ("tangent state bound", eps_b_hist))
    named += tuple((f"time derivative {key}", arr) for key, arr in TD.items())
    named += tuple((f"time derivative response {key}", arr) for key, arr in TR.items())
    named += tuple((f"time derivative bound {key}", arr) for key, arr in BD.items())
    for side, sd in sides.items():
        named += ((f"profile {side} node values", sd["f"]),
                  (f"profile {side} node derivatives", sd["df"]))
        named += tuple((f"time derivative response {side} {key}", arr)
                       for key, arr in sd["values"].items() if key != "nodes")
        named += tuple((f"time derivative bound {side} {key}", arr)
                       for key, arr in sd["bounds"].items() if key != "nodes")
    for name, arr in named:
        bad = int(np.count_nonzero(~np.isfinite(arr)))
        if bad:
            failures.append(f"packaging: {name} has {bad} non-finite entries; left unreported")
    if failures:
        return result
    out_labels = tuple(("E", c) for c in cells) + tuple(("O", lab) for lab in labels)
    result["means"] = {
        "mode": mode,
        "time_grid": grid.copy(),
        "E": E_mean, "H": H_mean, "O": O_mean, "presence": P_mean,
        "energy_cells": cells, "read_labels": labels,
        "by_kind": {kd: {"rows": rows, "O": O_mean[list(rows)], "presence": P_mean[list(rows)]}
                    for kd, rows in rows_by_kind.items()},
    }
    result["response"] = {
        "mode": mode,
        "values": resp, "presence": P_resp,
        "output_labels": out_labels, "source_labels": tuple(src_labels),
        "by_kind": {kd: {"output_rows": tuple(n_E + i for i in rows),
                         "values": resp[[n_E + i for i in rows]],
                         "presence": P_resp[list(rows)]}
                    for kd, rows in rows_by_kind.items()},
    }
    result["error_bounds"] = {
        "means": bd_mean, "H_mean": bd_H, "presence_means": bd_P,
        "response": bd_resp, "presence_response": bd_Presp,
        "primal_state_fro": eps_L_hist, "tangent_state_fro": eps_b_hist,
        "source_quadrature": 0.0,
        "density_factorization_R1": R1,
        "covered": (
            "primal and tangent truncation (a posteriori residual integrals), tangent forcing "
            "error carried from the primal, read/energy contractions of both, and the measured "
            "density factorization residual; source quadrature is exact (zero)"
        ),
        "not_covered": (
            "floating-point rounding in recursion, accumulation (see term_mass_ratio), source "
            "re-expansion, substep time placement, operator applications, contractions, norm "
            "and bound evaluation, eigh beyond its measured residual, dtype down-casts; "
            "operator premises (Hermitian H and E_alpha, sum E_alpha = H, true norm_bound_E, "
            "diagonal reads) are assumed, checked only as necessary conditions"
        ),
        "family_mode_meaning": (
            "bounds on Frobenius norms of the r x r compressed error matrices (valid for every "
            "family density of trace norm <= 1)" if mode == "family" else None),
    }
    # v002: MANDATORY ADDENDUM V001 item 1 outputs (module docstring, TIME DERIVATIVES).
    out_rows = {kd: [n_E + i for i in rows] for kd, rows in rows_by_kind.items()}
    result["time_derivatives"] = {
        "mode": mode,
        "time_parameter": "native time t of time_grid (flat point: tau = t, N_bg = 1)",
        "output_labels": out_labels, "source_labels": tuple(src_labels),
        "means": {
            "first": TD["first"], "second": TD["second"],
            "presence_first": TD["presence_first"], "presence_second": TD["presence_second"],
            "by_kind": {kd: {"rows": rows, "output_rows": tuple(out_rows[kd]),
                             "first": TD["first"][out_rows[kd]],
                             "second": TD["second"][out_rows[kd]],
                             "presence_first": TD["presence_first"][list(rows)],
                             "presence_second": TD["presence_second"][list(rows)]}
                        for kd, rows in rows_by_kind.items()},
        },
        "response": {
            "homogeneous_first": TR["hom1"], "homogeneous_second": TR["hom2"],
            "contact_G1": TR["G1"], "contact_G2": TR["G2"],
            "presence_homogeneous_first": TR["presence_hom1"],
            "presence_homogeneous_second": TR["presence_hom2"],
            "presence_contact_G1": TR["presence_G1"],
            "presence_contact_G2": TR["presence_G2"],
            "profile_at_nodes": {
                side: {"nodes": sd["values"]["nodes"], "f": sd["f"], "df": sd["df"]}
                for side, sd in sides.items()},
            "left": sides["left"]["values"], "right": sides["right"]["values"],
            "by_kind": {kd: {"output_rows": tuple(out_rows[kd]),
                             "left_first": sides["left"]["values"]["first"][out_rows[kd]],
                             "left_second": sides["left"]["values"]["second"][out_rows[kd]],
                             "right_first": sides["right"]["values"]["first"][out_rows[kd]],
                             "right_second": sides["right"]["values"]["second"][out_rows[kd]]}
                        for kd, rows in rows_by_kind.items()},
        },
    }
    result["error_bounds"]["time_derivatives"] = {
        "means_first": BD["first"], "means_second": BD["second"],
        "presence_means_first": BD["presence_first"],
        "presence_means_second": BD["presence_second"],
        "response_homogeneous_first": BD["hom1"], "response_homogeneous_second": BD["hom2"],
        "contact_G1": BD["G1"], "contact_G2": BD["G2"],
        "presence_response_homogeneous_first": BD["presence_hom1"],
        "presence_response_homogeneous_second": BD["presence_hom2"],
        "presence_contact_G1": BD["presence_G1"], "presence_contact_G2": BD["presence_G2"],
        "left": sides["left"]["bounds"], "right": sides["right"]["bounds"],
        "covered": (
            "the same primal/tangent state bounds and factorization residual propagated "
            "through same-state commutator reads by Cauchy-Schwarz with ||(i/hbar)[H,A]|| <= "
            "2 normH ||A||/hbar, ||[H,[H,A]]||/hbar^2 <= 4 normH^2 ||A||/hbar^2, ||G1 "
            "operator|| <= 2 ||B_b|| ||A||/hbar, ||G2 operator|| <= 8 normH ||B_b|| "
            "||A||/hbar^2, and |f_b|, |f_b'| at the stated node side"
        ),
        "not_covered": (
            "the v001 rounding list, also for the extra matvecs and contractions and for the "
            "float64 evaluation of f_b, f_b' at nodes; premises as v001 plus normH a true "
            "bound on ||H||_2 (observed on every apply_H as a necessary condition only)"
        ),
    }
    resources["taylor_orders"] = {
        "min": min(orders) if orders else None, "max": max(orders) if orders else None,
        "total": int(sum(orders))}
    resources["max_term_mass_ratio"] = mass_max
    resources["max_imaginary_part_of_trace_means"] = imag_max if mode == "trace" else None
    resources["max_norm_drift_diagnostic_not_a_bound"] = drift_max
    # Premise diagnostic for sum_alpha E_alpha = H (not a bound): compare with
    # error_bounds H_mean + sum of E mean bounds plus rounding.
    resources["max_energy_partition_residual_diagnostic"] = _max_abs(
        H_mean - np.sum(E_mean, axis=0))
    resources["cost_statement"] = (
        "per substep (N+1) apply_H on [D, r(1+m)] plus forcing apply_E per active cell; per "
        "node (v002, with time derivatives) apply_H twice on [D, r(1+m)] and once on "
        "[D, m r], apply_E per cell on [D, 3r] ([D, 2r] if m = 0) and per source-carrying "
        "cell on [D, 2r]; memory O(D r (20 m + P + 30)); D is the full owned inventory "
        "component (exponential in V0), not reduced here"
    )
    result["ok"] = True
    result["stage_reached"] = "complete"
    return result


# ---------------------------------------------------------------------------
# Public: g00 lapse coordinate contact
# ---------------------------------------------------------------------------

def g00_lapse_coordinate_contact(*, n_g, energy_means):
    """Coordinate conversion contact for g00 = -(1 + 2 n_g) versus the affine lapse n = N - 1.

    N = sqrt(1 + 2 n_g), n(n_g) = N - 1,  J1 = dn/dn_g = 1/N,  J2 = d2n/dn_g2 = -1/N**3.
    The source functional H[n(n_g)] = H + sum_alpha n(n_g,alpha) E_alpha gives
      dH/dn_g,alpha = J1 E_alpha,   d2H/dn_g,alpha2 = J2 E_alpha
    (flat point n_g = 0: E_alpha and -E_alpha; uniform: -H). With W_n = -<E_alpha>,
      W_{g g}(alpha t, beta s) = J1(alpha,t) W_nn(alpha t, beta s) J1(beta,s)
                                 + delta_{alpha beta} delta(t - s) J2(alpha,t) W_n(alpha,t),
    so the local contact coefficient is -J2 <E_alpha>(t) = +<E_alpha>(t)/N**3 (flat point:
    +<E_alpha>(t)); in partial_legendre_blocks it enters as an additive W_nn contact. A
    first-order n_g column equals an n column with profile J1 f. This helper returns
    pointwise coefficients only; the delta(t - s) must be discretized consistently with
    the caller's profile/observation pairing. propagate_source_columns linearizes about
    n = 0, so its outputs pair with n_g = 0; a nonzero background needs H[n0] (not here).

    Arguments (keyword-only, required): n_g and energy_means, real arrays of one common
    shape (e.g. [n_E, n_obs]); 1 + 2 n_g > 0 is required.
    """
    result = {"ok": False, "stage_reached": "inputs", "failures": [], "N": None, "n": None,
              "J1_dn_dng": None, "J2_d2n_dng2": None, "hamiltonian_second_derivative_factor": None,
              "W_second_order_contact": None,
              "statement": ("contact = -J2 <E_alpha>(t), local in cell and time; never dropped; "
                            "first-order columns convert with J1")}
    failures = result["failures"]
    admitted = {}
    for name, value in (("n_g", n_g), ("energy_means", energy_means)):
        if type(value) is np.ndarray:
            admitted[name] = _admit_array(name, value, value.ndim, False, failures)
        elif isinstance(value, (list, tuple)):
            try:
                nd = np.array(value).ndim
            except (ValueError, TypeError) as exc:
                failures.append(f"input {name}: not a rectangular numeric array ({exc})")
                continue
            admitted[name] = _admit_array(name, value, nd, False, failures)
        else:
            failures.append(f"input {name}: a plain real ndarray or nested list is required")
    if failures:
        return result
    ng = admitted["n_g"]
    em = admitted["energy_means"]
    if ng.shape != em.shape:
        failures.append(f"input: n_g shape {ng.shape!r} differs from energy_means shape {em.shape!r}")
        return result
    base = 1.0 + 2.0 * ng
    if not bool(np.all(base > 0.0)):
        failures.append("input n_g: 1 + 2 n_g must be > 0 everywhere (N real and positive)")
        return result
    N = np.sqrt(base)
    J1 = 1.0 / N
    J2 = -1.0 / (N * N * N)
    contact = -J2 * em
    result["stage_reached"] = "contact"
    if not (bool(np.all(np.isfinite(J1))) and bool(np.all(np.isfinite(contact)))):
        failures.append("contact: non-finite coefficients; left unreported")
        return result
    result.update({"N": N, "n": N - 1.0, "J1_dn_dng": J1, "J2_d2n_dng2": J2,
                   "hamiltonian_second_derivative_factor": J2, "W_second_order_contact": contact,
                   "ok": True, "stage_reached": "complete"})
    return result


# ---------------------------------------------------------------------------
# Public: partial Legendre blocks
# ---------------------------------------------------------------------------

def partial_legendre_blocks(*, chi_EE, chi_EO, chi_OE, chi_OO, contacts, read_quotient,
                            energy_quotient, declared_zero_modes, relative_singular_floor,
                            exclusion_tolerance):
    """Partial Legendre (in j only) blocks on a caller-declared admissible quotient.

    Finite matrices of causal kernels (rows: outputs, e.g. (read or cell, observation
    time); columns: source columns), discretized by the caller:
      chi_OO [a, b], chi_OE [a, c], chi_EO [d, b], chi_EE [d, c]  (real or complex).
    contacts: {"OO": [a, b], "OE": [a, c], "EO": [d, b], "EE": [d, c]} additive W
      second-derivative contacts, applied BEFORE reduction and Schur complement:
        W_jj = chi_OO + C_OO,  W_jn = -chi_OE + C_OE,  W_nj = -chi_EO + C_EO,
        W_nn = chi_EE + C_EE   (e.g. C_EE = -<H_nn>: zero in affine n; the g00 contact of
        g00_lapse_coordinate_contact in n_g coordinates). Pass explicit zero arrays when
        none apply; nothing is assumed.
      Effective blocks: X_OO = chi_OO + C_OO, X_OE = chi_OE - C_OE, X_EO = chi_EO - C_EO,
      X_EE = chi_EE + C_EE.
    read_quotient: {"output_basis": T_O [a, q], "source_basis": S_O [b, q]};
    energy_quotient: {"output_basis": T_E [d, p], "source_basis": S_E [c, p]};
      reduced blocks use the bilinear dual pairing: Y_OO = T_O^T X_OO S_O [q, q],
      Y_OE = T_O^T X_OE S_E, Y_EO = T_E^T X_EO S_O, Y_EE = T_E^T X_EE S_E.
    declared_zero_modes: {"read_output": [a, z1], "read_source": [b, z2],
      "energy_output": [d, z3], "energy_source": [c, z4]} (zero columns allowed): directions
      the caller declares conserved/zero (e.g. uniform energy). Each must be excluded from
      the matching quotient basis under the SAME bilinear pairing as the reduction:
      ||B^T z|| <= exclusion_tolerance ||B||_F ||z|| (for real bases: z orthogonal to span B).
    relative_singular_floor: basis ranks and Y_OO invertibility require s_min > floor s_max.
    Outputs:
      Gamma_QQ = -Y_OO^-1, Gamma_Qn = -Y_OO^-1 Y_OE, Gamma_nQ = -Y_EO Y_OO^-1,
      Gamma_nn = Y_EE - Y_EO Y_OO^-1 Y_OE  (numpy.linalg.solve; no inverse regularizer).
    These are the affine fixed-read CTP retarded blocks with the declared contacts; no
    matched EH/vacuum coefficient is invented and they are not the complete metric
    propagator (LIMITATIONS L10).
    """
    result = {"ok": False, "stage_reached": "inputs", "failures": [], "Gamma_QQ": None,
              "Gamma_Qn": None, "Gamma_nQ": None, "Gamma_nn": None, "reduced": None,
              "diagnostics": None,
              "statement": ("affine fixed-read partial Legendre blocks with caller contacts, on "
                            "the declared quotient; CTP typing, initial/boundary data and EH "
                            "matching remain the caller's explicit inputs")}
    failures = result["failures"]
    blocks = {}
    for name, value in (("chi_OO", chi_OO), ("chi_OE", chi_OE), ("chi_EO", chi_EO),
                        ("chi_EE", chi_EE)):
        blocks[name] = _admit_array(name, value, 2, True, failures)
    floor = _admit_positive_real("relative_singular_floor", relative_singular_floor, failures)
    etol = _admit_positive_real("exclusion_tolerance", exclusion_tolerance, failures)
    ct = _admit_mapping("contacts", contacts, ("OO", "OE", "EO", "EE"), failures)
    rq = _admit_mapping("read_quotient", read_quotient, ("output_basis", "source_basis"),
                        failures)
    eq = _admit_mapping("energy_quotient", energy_quotient, ("output_basis", "source_basis"),
                        failures)
    zm = _admit_mapping("declared_zero_modes", declared_zero_modes,
                        ("read_output", "read_source", "energy_output", "energy_source"),
                        failures)
    if failures:
        return result
    C = {key: _admit_array(f"contacts[{key!r}]", ct[key], 2, True, failures)
         for key in ("OO", "OE", "EO", "EE")}
    T_O = _admit_array("read_quotient.output_basis", rq["output_basis"], 2, True, failures)
    S_O = _admit_array("read_quotient.source_basis", rq["source_basis"], 2, True, failures)
    T_E = _admit_array("energy_quotient.output_basis", eq["output_basis"], 2, True, failures)
    S_E = _admit_array("energy_quotient.source_basis", eq["source_basis"], 2, True, failures)
    Z = {key: _admit_array(f"declared_zero_modes[{key!r}]", zm[key], 2, True, failures)
         for key in ("read_output", "read_source", "energy_output", "energy_source")}
    if failures:
        return result
    a, b = blocks["chi_OO"].shape
    c = blocks["chi_OE"].shape[1]
    d = blocks["chi_EO"].shape[0]
    expected = {"chi_OO": (a, b), "chi_OE": (a, c), "chi_EO": (d, b), "chi_EE": (d, c)}
    for name, shape in expected.items():
        if blocks[name].shape != shape:
            failures.append(f"shape: {name} is {blocks[name].shape!r}, expected {shape!r}")
        if C[name[4:]].shape != shape:
            failures.append(f"shape: contacts[{name[4:]!r}] is {C[name[4:]].shape!r}, "
                            f"expected {shape!r}")
    q = T_O.shape[1]
    p = T_E.shape[1]
    for name, arr, shape in (("read_quotient.output_basis", T_O, (a, q)),
                             ("read_quotient.source_basis", S_O, (b, q)),
                             ("energy_quotient.output_basis", T_E, (d, p)),
                             ("energy_quotient.source_basis", S_E, (c, p))):
        if arr.shape != shape or shape[1] < 1:
            failures.append(f"shape: {name} is {arr.shape!r}, expected {shape!r} with >= 1 column")
    for key, rows in (("read_output", a), ("read_source", b), ("energy_output", d),
                      ("energy_source", c)):
        if Z[key].shape[0] != rows:
            failures.append(f"shape: declared_zero_modes[{key!r}] has {Z[key].shape[0]} rows, "
                            f"expected {rows}")
    if failures:
        return result

    result["stage_reached"] = "quotient"
    bases = {"read_output": T_O, "read_source": S_O, "energy_output": T_E, "energy_source": S_E}
    basis_sv = {}
    for key, B in bases.items():
        if B.shape[1] > B.shape[0]:
            failures.append(f"quotient: {key} basis has {B.shape[1]} columns > {B.shape[0]} rows; "
                            "cannot have full column rank")
            return result
        try:
            sv = np.linalg.svd(B, compute_uv=False)
        except np.linalg.LinAlgError as exc:
            failures.append(f"quotient: singular values of {key} basis did not converge ({exc})")
            return result
        basis_sv[key] = sv
        if not (float(sv[0]) > 0.0 and float(sv[-1]) > floor * float(sv[0])):
            failures.append(f"quotient: {key} basis is rank deficient (s_min {float(sv[-1])!r}, "
                            f"s_max {float(sv[0])!r}, floor {floor!r}); degenerate quotient")
        zmat = Z[key]
        Bn = _fro(B)
        for col in range(zmat.shape[1]):
            zc = zmat[:, col]
            overlap = _fro(np.einsum("ri,r->i", B, zc, optimize=False))
            if overlap > etol * Bn * _fro(zc):
                failures.append(f"quotient: declared zero mode {key}[:, {col}] is retained by "
                                f"the quotient (overlap {overlap!r}); not an invertible "
                                "response direction")
    if failures:
        return result

    result["stage_reached"] = "reduction"
    X_OO = blocks["chi_OO"] + C["OO"]
    X_OE = blocks["chi_OE"] - C["OE"]
    X_EO = blocks["chi_EO"] - C["EO"]
    X_EE = blocks["chi_EE"] + C["EE"]
    Y_OO = np.einsum("ri,rs,sj->ij", T_O, X_OO, S_O, optimize=False)
    Y_OE = np.einsum("ri,rs,sj->ij", T_O, X_OE, S_E, optimize=False)
    Y_EO = np.einsum("ri,rs,sj->ij", T_E, X_EO, S_O, optimize=False)
    Y_EE = np.einsum("ri,rs,sj->ij", T_E, X_EE, S_E, optimize=False)
    try:
        sv = np.linalg.svd(Y_OO, compute_uv=False)
    except np.linalg.LinAlgError as exc:
        failures.append(f"reduction: singular values of reduced chi_OO did not converge ({exc})")
        return result
    s_max = float(sv[0])
    s_min = float(sv[-1])
    if not (s_max > 0.0 and s_min > floor * s_max):
        failures.append(f"reduction: reduced chi_OO is singular on the declared quotient "
                        f"(s_min {s_min!r}, s_max {s_max!r}, floor {floor!r}); singular/zero-mode "
                        "direction rejected, no regulator or pseudoinverse")
        return result

    result["stage_reached"] = "solve"
    try:
        inv_OO = np.linalg.solve(Y_OO, np.eye(q, dtype=Y_OO.dtype))
        A_OE = np.linalg.solve(Y_OO, Y_OE)
        B_EO = np.linalg.solve(Y_OO.T, Y_EO.T).T
    except np.linalg.LinAlgError as exc:
        failures.append(f"solve: reduced chi_OO singular to working precision ({exc})")
        return result
    Gamma_QQ = -inv_OO
    Gamma_Qn = -A_OE
    Gamma_nQ = -B_EO
    Gamma_nn = Y_EE - np.einsum("ij,jk->ik", Y_EO, A_OE, optimize=False)
    res_inv = _fro(np.einsum("ij,jk->ik", Y_OO, inv_OO, optimize=False) - np.eye(q))
    res_OE = _fro(np.einsum("ij,jk->ik", Y_OO, A_OE, optimize=False) - Y_OE)
    res_EO = _fro(np.einsum("ij,jk->ik", B_EO, Y_OO, optimize=False) - Y_EO)
    for name, arr in (("Gamma_QQ", Gamma_QQ), ("Gamma_Qn", Gamma_Qn), ("Gamma_nQ", Gamma_nQ),
                      ("Gamma_nn", Gamma_nn)):
        if not bool(np.all(np.isfinite(arr))):
            failures.append(f"solve: {name} has non-finite entries; left unreported")
    if not all(math.isfinite(x) for x in (res_inv, res_OE, res_EO)):
        failures.append("solve: residual diagnostics are not finite")
    if failures:
        return result
    result.update({
        "Gamma_QQ": Gamma_QQ, "Gamma_Qn": Gamma_Qn, "Gamma_nQ": Gamma_nQ, "Gamma_nn": Gamma_nn,
        "reduced": {"chi_OO": Y_OO, "chi_OE": Y_OE, "chi_EO": Y_EO, "chi_EE": Y_EE},
        "diagnostics": {"chi_OO_singular_values": sv, "cond_2": s_max / s_min,
                        "basis_singular_values": basis_sv,
                        "residual_inverse_fro": res_inv, "residual_Qn_fro": res_OE,
                        "residual_nQ_fro": res_EO},
        "ok": True, "stage_reached": "complete",
    })
    return result
