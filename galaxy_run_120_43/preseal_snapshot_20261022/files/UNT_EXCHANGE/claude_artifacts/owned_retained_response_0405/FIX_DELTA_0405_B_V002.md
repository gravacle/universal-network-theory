# FIX DELTA 0405 module B: owned_retained_source_columns v001 -> v002

Fix author for module B. Static work only: neither module, nor any legacy/UNT/Codex module, was imported or executed. The only code run was `python3 -I -B` with `ast.parse` and an in-memory `compile` on the V002 TEXT, from a scratch directory outside this folder. No `__pycache__` was written here. No numerical control, propagation, data extraction, network use or install. V001 is unchanged.

| file | bytes | sha256 |
|---|---|---|
| owned_retained_source_columns_v001.py | 84801 | a9773a6dcdc5535d38808308b0d7ebf5ff89dc680b70144e5c3e57a9e2670a27 |
| owned_retained_source_columns_v002.py | 116917 | 173f608d9b4effdf61c3ea0bfb147aaf5528a742c3ec2501d41f5397b36bbe81 |

Binding inputs verified from bytes before writing: CONTRACT fcad9039574f1666af005bb76a231f14b90f0c8dd82acebd2b16ab77941cd642; 0405 7baab49ebbd01de684df56a074b823552c1eca9e787384ad0a0084144295c003; 0406 a465d9e3f703f2a2f19d383446c6a2bf6486e5f6be9fdf5996fc96dfb4693d50; ADDENDUM 7cb15b4a5ac2ea33dfd43801c011142bc2b2388c3be0087152c049e78deccd39; HP time-derivative addendum (cited by ADDENDUM item 1) 2fc9dc2c0197d6b3d0e2ff5893ba32b7ef89ba5424680bc06bd5210d5207226a; 0408 c0f0eaa940ce95c495fa2d7c21d59cae2a49e8028cc084df878d203e3c42e341.

## Per-issue resolution (V002 line numbers)

1. Issue "both" (B l.549-609 and l.1299-1315; A L9). Resolved in module B, with no change to module A. A's L9 delegation is now met by B V002.
   - `_contract_node` (l.735-868) applies H to [L, dL] and to its image, which gives H L, H^2 L, H dL and H^2 dL. It forms B_b L and B_b H L from apply_E on [L, H L] plus the read diagonals, and H B_b L from apply_H. It applies each E_alpha to [L, H L, H^2 L].
   - `_derivative_terms` (l.702-732), with `_pair_applied`, `_pair_diag`, `_sym` and `_anti` (l.646-699), returns <L_A> = (i/hbar)<[H,A]>, <A_A> = -(1/hbar^2)<[H,[H,A]]>, the homogeneous tangent derivatives, and the explicit contact coefficients G1 = (i/hbar)<[B_b,A]>_0 and G2 = -(1/hbar^2)<[B_b,[H,A]] + [H,[B_b,A]]>_0. These cover every E_alpha, every read row (first-moment, pair and coarse m/R/S) and every presence row, on the same state and with the same full-H matvec.
   - The K' term f_b'(t) G1 is assembled into one-sided second derivatives at l.1716-1738.
   - Bounds extend the v001 Cauchy-Schwarz node bounds at l.1700-1712.
   - Outputs: `result["time_derivatives"]` (l.1800-1834) and `error_bounds["time_derivatives"]` (l.1835-1859).
   - The read/frame partial derivatives are stated to be explicitly zero for the fixed current-state reads in `contacts["time_derivatives"]` (l.1001-1043), the docstring TIME DERIVATIVES section (l.122-166) and LIMITATIONS L15-L17 (l.249-278).

2. Issue B (B l.748-1355; LIMITATIONS l.130-191; A L9). Resolved by the same change.
   - Same-state first and second derivatives of the means use apply_H. Response derivatives differentiate 2 Re<l|A|dl_b> with i hbar dl_b' = H dl_b + V_b l. This includes the source term f_b G1, where G1 = (2/hbar) Im sum_k s_k <A l_k|B_b l_k> in trace mode, and at second order the f_b G2 and f_b' G1 terms.
   - Per-entry bounds use norm_bound_H: c1 = 2 normH/hbar and c2 = 4 normH^2/hbar^2 scale the existing mean/response bounds, G1 uses (2/hbar)||B_b|| ||A||, and G2 uses (8 normH/hbar^2)||B_b|| ||A||. They are listed in the docstring DERIVATIVE BOUNDS section (l.155-166).
   - K' and frame terms: the background K' is 0 at the flat point, the first-order K' = sum_b f_b' B_b is retained, and partial_t A = 0 for the fixed registration (l.1001-1043, L17).
   - The ADDENDUM is recorded in LIMITATIONS L15 (l.249-260).
   - Sign note, not a defect in either version: the review prints d<A>/dt = (2/hbar) Im sum s <H l|A l>, which holds for an inner product linear in its first slot. With <x|y> antilinear in x, as coded (conj on the first factor), the correct form is (2/hbar) Im sum s <A l|H l> = -(2/hbar) Im sum s <H l|A l>. V002 implements the convention-free commutator form (i/hbar)(X - X^dagger) with X = <H l|A l> (l.695-699, l.725).

3. Issue B ("n/a"). Resolved.
   - Full-H first and second derivatives are returned for all first-moment, pair and presence means, plus the coarse rows (l.1802-1834).
   - mu and raw M are typed and returned separately, with their response derivatives, through `by_kind` (l.1806-1833). The integration typing with module A tokens is in LIMITATIONS L18 (l.279-284).
   - The explicit caller declaration is a new REQUIRED keyword-only argument `time_derivative_contacts` = {"read_frame": "fixed_current_state_reads", "background_generator": "flat_point_time_independent_H"} (l.1094, admission at l.1204-1225, constants at l.287-288). Any other key set or value fails explicitly, so nothing is silently dropped.
   - The explicit fields are `contacts["time_derivatives"]` (read_frame_partial, background_generator_K_prime, source_generator_K_prime, proper_time, c_number_frame; l.1001-1043), together with `response["contact_G1"]`, `["contact_G2"]` and `["profile_at_nodes"]`.
   - Coarse rows (m_alpha, R_alpha_i, S_alpha_ij) are accepted as read rows. V001 already accepted every typed diagonal row, and A's coarse rows pass B's presence/value checks. V002 makes this explicit (L18) and covers these rows in the derivatives.

## Judgements (issues or parts not treated as code defects)

- **Issue 3, "accept coarse rows as read rows."** This part was already satisfied by V001. No code change was needed, only documentation (L18).
- **Issue 3, "caller-supplied read/frame and K' contact inputs."** These are implemented as explicit declarations with fail-closed alternatives, not as caller-computed numeric arrays. The reason is that an operator-level time-dependent read, registration or support, or a time-dependent background generator, cannot be evaluated on B's state through the shared operator interface. A caller cannot form such state expectations either.
- **Caller-side combinations.** A c-number frame acting linearly on rows, O(t) = T(t) O, and the homogeneous proper-time chain rule are caller-side combinations of the returned quantities. Their formulas are stated in `contacts["time_derivatives"]`.
- **Source-side frame time dependence.** This is represented exactly by fixed-row columns whose declared profiles carry it, and their K' terms are then the returned f_b' G1.

## Scope of change (everything else unchanged)

- **Interface.** `propagate_source_columns` gains one required keyword argument. The result dict gains `time_derivatives`, `error_bounds["time_derivatives"]`, `contacts["time_derivatives"]` and `conventions["time_derivatives"]`.
- **Unchanged outputs.** Every v001 output is unchanged in exact arithmetic. H L and E_alpha L now come from the first r columns of wider apply blocks.
- **Cost.** Node cost and the working-entry estimate increase, and both are stated (docstring COST l.168-178, `_entries_estimate` l.887-916, `worst_case_column_applications` l.1568-1573, `cost_statement` l.1868-1874).
- **One-sidedness.** Profiles may be discontinuous at nodes, so assembled response derivatives are returned as left limits (nodes 1..K) and right limits (nodes 0..K-1). No side is chosen (L16, `_profile_node_values` l.919-942).
- **Not changed.** The propagation recursion, residual bounds, forcing, preparation paths, `g00_lapse_coordinate_contact` and `partial_legendre_blocks`.

## AST check (python3 -I -B, ast.parse plus in-memory compile of the V002 text, Python 3.9.6)

- **Imports.** Only `math` and `numpy`.
- **Banned constructs.** No `@`/MatMult and no dot, matmul, vdot, inner, tensordot, outer or kron. No print, open, exec, eval or input. No lambda, global/nonlocal, yield or async. No errstate or warnings control.
- **einsum.** Every einsum call has `optimize=False`.
- **Module top level.** Only the docstring, imports, function definitions and literal constants (`LIMITATIONS`, `_READ_FRAME_FIXED`, `_BACKGROUND_FLAT`). Nothing executes at import.
- **Public functions.** All are keyword-only with zero defaults: `propagate_source_columns` (9 keyword-only), `g00_lapse_coordinate_contact` (2) and `partial_legendre_blocks` (10).
- **Size.** 29 top-level defs (v001: 23).

## diff -u v001 v002

```diff
--- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/owned_retained_response_0405/owned_retained_source_columns_v001.py	2026-10-16 03:14:48.390934921 -0500
+++ /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/owned_retained_response_0405/owned_retained_source_columns_v002.py	2026-10-16 04:12:56.239961891 -0500
@@ -1,7 +1,11 @@
 """Owned retained response: same-state full-H primal/tangent source-column propagator.
 
-UNT task 0405, module B (contract section 11(B)), version v001. Static author
+UNT task 0405, module B (contract section 11(B)), version v002. Static author
 implementation: written as text and never imported or executed by its author.
+v002 = v001 plus ONLY the MANDATORY ADDENDUM V001 item 1 time-derivative reads (same-state
+full-H first/second native-time derivatives of every mean and response, the explicit
+generator K' term, their error bounds, and the explicit read/frame and background-generator
+declarations); every v001 output, equation and bound is unchanged.
 
 Binding sources (sha256 computed from bytes before writing):
   * OWNED_RETAINED_RESPONSE_FULL_H_SOURCE_COLUMN_IMPLEMENTATION_CONTRACT_V001.txt
@@ -22,6 +26,12 @@
     a7d048c11a826d6d2627afd3f5324458a0350bc6abbd58bd8ab8d6c39d7eedf7
   * coefficient_method/FINITE_STATIONARY_PAIR_KERNEL_LAPSE_LIMIT_AND_COMPLETION_CORRECTION_V001.md
     facdfe454904ea27b38df19865168a7560bf24b56cb774c549ea53a1addec9b4
+  * coefficient_method/OWNED_RETAINED_PROVIDER_IMPLEMENTATION_MANDATORY_READ_AND_LABEL_ADDENDUM_V001.txt
+    7cb15b4a5ac2ea33dfd43801c011142bc2b2388c3be0087152c049e78deccd39 (BINDING; item 1)
+  * response_packet_audit/SAME_ACTION_COVARIANCE_VOLUME_TIME_DERIVATIVES_ADDENDUM_V001.md
+    2fc9dc2c0197d6b3d0e2ff5893ba32b7ef89ba5424680bc06bd5210d5207226a (cited by item 1:
+    L_O = partial_tau O + (i/hbar)[K,O], A_O = partial_tau^2 O + (2i/hbar)[K,partial_tau O]
+    + (i/hbar)[K',O] - [K,[K,O]]/hbar^2)
 Legacy code read as text only (never imported or executed):
   * exploratory_physics/root_native_shared_parent_clock_transport_v001.py
     d7871d1bd4c55b826c2d7a04606a2552e418017c12379fc018b90811aae4a2a9, taylor_step
@@ -34,7 +44,7 @@
 
 Public entries (keyword-only, no defaults):
   propagate_source_columns(*, operator, preparation, source_columns, time_grid, hbar,
-                           stepper, caps, dtype)
+                           stepper, caps, dtype, time_derivative_contacts)
   partial_legendre_blocks(*, chi_EE, chi_EO, chi_OE, chi_OO, contacts, read_quotient,
                           energy_quotient, declared_zero_modes, relative_singular_floor,
                           exclusion_tolerance)
@@ -109,11 +119,59 @@
 reads diagonal. Declared norm bounds are checked on every application (necessary, not
 sufficient) and read diagonality is checked once (necessary, not sufficient).
 
+TIME DERIVATIVES (v002; MANDATORY ADDENDUM V001 item 1 and the HP addendum 2fc9dc2c). At
+every node, on the SAME state and with the SAME full-H matvec, for every output A (every
+E_alpha, every operator read row -- first-moment, pair and coarse m/R/S rows alike -- and
+every presence row). The background is the flat point n = 0, j = 0, so the zeroth-order
+generator is K = H, time independent, with tau = t (N_bg = 1), and the first-order
+generator is K = H + sum_b f_b(t) B_b, B_b = sum_alpha cE[b,alpha] E_alpha - sum_A cO[b,A]
+O_A, whose derivative K' = sum_b f_b'(t) B_b is RETAINED. Reads, registration, frame and
+support are the operator's fixed current-state definitions, so partial_t A = 0 and the
+(2i/hbar)[K, partial_t A] term is zero (declared by the caller in time_derivative_contacts;
+anything else fails explicitly, LIMITATIONS L17). Then, exactly,
+    d<A>/dt         = <L_A> = (i/hbar) <[H,A]>,
+    d2<A>/dt2       = <A_A> = -(1/hbar^2) <[H,[H,A]]>,
+    d delta<A>/dt   = (i/hbar) delta_b<[H,A]> + f_b(t) G1[A,b],
+    d2 delta<A>/dt2 = -(1/hbar^2) delta_b<[H,[H,A]]> + f_b(t) G2[A,b] + f_b'(t) G1[A,b],
+    G1[A,b] = (i/hbar) <[B_b, A]>_0,
+    G2[A,b] = -(1/hbar^2) <[B_b,[H,A]] + [H,[B_b,A]]>_0,
+with delta_b<X> = 2 Re sum_k s_k <l_k|X|dl_bk> for Hermitian X (these follow from
+i hbar rho' = [K, rho] and i hbar delta rho' = [H, delta rho] + [V_b, rho]; f_b' G1 is the
+(i/hbar)<[K',A]> term). In column form, with Z^dagger over the family indices and
+<x|y> antilinear in x:
+    <L_A>  = (i/hbar)(X - X^dagger),        X = <H l|A l>,
+    <A_A>  = -(1/hbar^2)(Y + Y^dagger - 2Z), Y = <H^2 l|A l>, Z = <H l|A|H l>,
+    hom1   = P + P^dagger,  P = (i/hbar)(<H l|A dl> - <A l|H dl>),
+    hom2   = -(1/hbar^2)(Q + Q^dagger), Q = <H^2 l|A dl> - 2<H l|A|H dl> + <A l|H^2 dl>,
+    G1     = (i/hbar)(W - W^dagger), W = <B l|A l>,
+    G2     = -(1/hbar^2)(U + U^dagger), U = <H B l|A l> + <B H l|A l> - 2<B l|A|H l>,
+built from H L, H(H L), H dL, H(H dL), E_alpha on [L, H L, H^2 L], B_b L, B_b H L and
+H B_b L (trace mode: sum_k s_k of the diagonal, i.e. X + X^dagger -> 2 Re x and
+(i/hbar)(X - X^dagger) -> -(2/hbar) Im x). Profiles may be discontinuous at nodes, so the
+assembled response derivatives are returned as LEFT limits (nodes 1..K, from interval k-1)
+and RIGHT limits (nodes 0..K-1, from interval k), with the exact one-sided node values f_b
+and f_b'; the homogeneous and contact pieces are single-valued and are returned too. d<H>/dt
+is identically zero at the flat point and is not returned.
+DERIVATIVE BOUNDS (same Cauchy-Schwarz scheme; each output is the exact expectation or
+response of a fixed operator C on the computed state). With ||(i/hbar)[H,A]|| <= c1 ||A||,
+c1 = 2 normH/hbar, ||[H,[H,A]]||/hbar^2 <= c2 ||A||, c2 = 4 normH^2/hbar^2:
+    mean first/second : the mean bound with ||A|| -> c1 ||A|| / c2 ||A||,
+    hom1/hom2         : the response bound with ||A|| -> c1 ||A|| / c2 ||A||,
+    G1[A,b] : (2/hbar) ||B_b|| ||A|| (eps_L (||L_N||_F + ||L0||_F) + R1),
+    G2[A,b] : (8 normH/hbar^2) ||B_b|| ||A|| (eps_L (||L_N||_F + ||L0||_F) + R1),
+    first  (side) : bound(hom1) + |f_b(side)| bound(G1),
+    second (side) : bound(hom2) + |f_b(side)| bound(G2) + |f_b'(side)| bound(G1).
+These are rigorous in exact arithmetic under the same operator premises (normH a true bound
+on ||H||_2); the rounding list above also applies to the extra matvecs, contractions and
+the evaluation of f_b and f_b' at nodes.
+
 COST. Per substep: (N+1) apply_H calls on a [D, r(1+m)] block, plus for every order with
 active forcing one apply_E call per energy cell carrying a nonzero coefficient (block
-[D, r * number of such sources]) and O(D r m) diagonal read work. Per observation node:
-1 apply_H and n_E apply_E calls on [D, r] plus O((n_read + m) D r) contraction work
-(family path O(n_read m D r^2)). Working memory is O(D r (12 m + P + 12)) entries; a
+[D, r * number of such sources]) and O(D r m) diagonal read work. Per observation node
+(v002, including the time derivatives): apply_H on [D, (1+m) r] twice and, for m > 0, on
+[D, m r] once; apply_E per cell on [D, 3 r] ([D, 2 r] when m = 0) plus, per cell carrying a
+nonzero energy source coefficient, on [D, 2 r]; plus O((n_read + m) D r) contraction work
+(family path O(n_read m D r^2)). Working memory is O(D r (20 m + P + 30)) entries; a
 dense density input propagates r = D columns and adds about 6 D^2 entries (its eigh and
 reconstruction check cost O(D^3)). D is the
 FULL owned inventory component dimension from module A, exponential in V0; nothing here
@@ -188,8 +246,47 @@
     energy-partition residual are diagnostics, not outputs used elsewhere; (e) operator
     dimension, energy_cells and read_labels are read as attributes, every other interface
     member is called with keyword arguments exactly as in the shared interface.
+L15. MANDATORY ADDENDUM V001 item 1 (7cb15b4a...; HP addendum 2fc9dc2c...). Full-H first and
+    second native-time derivatives of every mean (<L_A>, <A_A>) and of every response are
+    returned at every node on the same state, with per-entry bounds (module docstring,
+    TIME DERIVATIVES). They are exact same-state commutator reads, not finite differences of
+    node values. The explicit generator K' term is retained: at the flat point the
+    zeroth-order K = H is time independent (K' = 0), and the first-order K' = sum_b
+    f_b'(t) B_b enters the response second derivative as f_b' G1 (returned separately with
+    G1, G2 and the node values f_b, f_b'). Derivatives are with respect to the native time
+    t of time_grid; tau = t at the flat point (N_bg = 1). The nonlinear centered and volume
+    reads of the HP addendum (C' = M' - mu' mu^T - mu mu'^T, C'', v'/v, H_v, a_v''/a_v) are
+    caller-side combinations of the returned mu, M, mu', M', mu'', M'' and are not formed
+    here (L3); a singular C is not regularized here because C is not formed here.
+L16. One-sided node values. Profiles may be discontinuous at nodes (L5), and so may their
+    derivatives. Assembled response derivatives are therefore returned as left limits
+    (nodes 1..K, interval k-1 evaluated at its end) and right limits (nodes 0..K-1,
+    interval k evaluated at its start); no side is chosen. Mean derivatives and the
+    homogeneous/contact pieces are single-valued (the state is continuous).
+L17. Read/frame and generator declarations (time_derivative_contacts, required, exact keys).
+    'read_frame' must be 'fixed_current_state_reads': every E_alpha, read and presence row is
+    the operator's fixed current-state definition with fixed registration, frame, scale and
+    support, so partial_t A = partial_t^2 A = 0 and the (2i/hbar)[K, partial_t A] term
+    vanishes; state-dependent 1/m_alpha, presence and adjacency are inside A and act through
+    the commutator (no separate count derivative is added). 'background_generator' must be
+    'flat_point_time_independent_H': K = H at n = 0, j = 0, N_bg = 1. Any other value fails
+    explicitly: an operator-level time-dependent read/registration/support, or a nonzero or
+    time-dependent background lapse/source, is not representable through the shared
+    interface (L4) and is never silently dropped. A c-number registered frame acting
+    linearly on returned rows, O(t) = T(t) O, and the homogeneous proper-time
+    reparametrization d/dtau = N_bg^-1 d/dt are caller-side combinations of returned
+    quantities (formulas in contacts['time_derivatives']).
+L18. Moment typing with module A v001 tokens (integration note; module B still groups by the
+    exact token, L1): first_moment_Z and coarse_first_R are first moments (mu, registered
+    X), pair_ZZ and coarse_second_S raw second moments (M), vertex_presence and
+    coarse_population_m presence/population. Coarse rows m_alpha, R_alpha_i, S_alpha_ij are
+    accepted as ordinary diagonal read rows for means, responses, source columns and time
+    derivatives; their per-configuration 1/m_alpha is inside the operator (L3).
 """
 
+_READ_FRAME_FIXED = "fixed_current_state_reads"
+_BACKGROUND_FLAT = "flat_point_time_independent_H"
+
 
 # ---------------------------------------------------------------------------
 # Admission helpers (private)
@@ -546,40 +643,187 @@
 # Same-state contractions and their bounds at one observation node
 # ---------------------------------------------------------------------------
 
+def _pair_applied(X, Y, sig, mode):
+    """Column pairing <X|Y> with the output operator already applied to one side.
+
+    X, Y: [D, r] (primal-shaped) or [D, m, r] (tangent-shaped), at most one tangent-shaped.
+    trace mode: sum_k s_k <X_k|Y_k> (scalar, or [m]); family mode: [r, r] (or [m, r, r]).
+    """
+    Xc = np.conj(X)
+    if mode == "trace":
+        if X.ndim == 2 and Y.ndim == 2:
+            return np.einsum("xk,xk,k->", Xc, Y, sig, optimize=False)
+        if X.ndim == 2:
+            return np.einsum("xk,xbk,k->b", Xc, Y, sig, optimize=False)
+        return np.einsum("xbk,xk,k->b", Xc, Y, sig, optimize=False)
+    if X.ndim == 2 and Y.ndim == 2:
+        return np.einsum("xk,xl->kl", Xc, Y, optimize=False)
+    if X.ndim == 2:
+        return np.einsum("xk,xbl->bkl", Xc, Y, optimize=False)
+    return np.einsum("xbk,xl->bkl", Xc, Y, optimize=False)
+
+
+def _pair_diag(Vd, X, Y, sig, mode):
+    """Column pairing <X|diag(Vd_a)|Y> for every row a of a real diagonal matrix Vd [n_a, D].
+
+    Shapes as _pair_applied with a leading n_a axis.
+    """
+    Xc = np.conj(X)
+    if mode == "trace":
+        if X.ndim == 2 and Y.ndim == 2:
+            w = np.einsum("xk,xk,k->x", Xc, Y, sig, optimize=False)
+            return np.einsum("ax,x->a", Vd, w, optimize=False)
+        if X.ndim == 2:
+            w = np.einsum("xk,xbk,k->bx", Xc, Y, sig, optimize=False)
+        else:
+            w = np.einsum("xbk,xk,k->bx", Xc, Y, sig, optimize=False)
+        return np.einsum("ax,bx->ab", Vd, w, optimize=False)
+    if X.ndim == 2 and Y.ndim == 2:
+        return np.einsum("ax,xk,xl->akl", Vd, Xc, Y, optimize=False)
+    if X.ndim == 2:
+        return np.einsum("ax,xk,xbl->abkl", Vd, Xc, Y, optimize=False)
+    return np.einsum("ax,xbk,xl->abkl", Vd, Xc, Y, optimize=False)
+
+
+def _sym(Z, mode):
+    """Z + Z^dagger over the family axes: trace mode 2 Re z; family mode trailing [r, r]."""
+    if mode == "trace":
+        return 2.0 * np.real(Z)
+    return Z + np.conj(np.swapaxes(Z, -1, -2))
+
+
+def _anti(Z, mode, hbar):
+    """(i/hbar)(Z - Z^dagger): trace mode -(2/hbar) Im z; family mode trailing [r, r]."""
+    if mode == "trace":
+        return (-2.0 / hbar) * np.imag(Z)
+    return (1j / hbar) * (Z - np.conj(np.swapaxes(Z, -1, -2)))
+
+
+def _derivative_terms(*, arrays, applied, Vd, sig, m, mode, hbar):
+    """Same-state time-derivative pieces for one output family (module docstring, TIME
+    DERIVATIVES; ADDENDUM item 1).
+
+    arrays: named columns L, HL, H2L (primal) and, for m > 0, dL, HdL, H2dL, BL, BHL, HBL
+    (tangent-shaped). Diagonal outputs pass Vd [n_a, D]; one E_alpha output passes Vd None
+    and applied = {L: E L, HL: E H L, H2L: E H^2 L (m > 0)}, using <X|E Y> = <E X|Y>.
+    Returns d1 = <L_A>, d2 = <A_A> and, for m > 0, hom1, hom2 (homogeneous tangent
+    derivatives) and G1, G2 (explicit source/K' contact coefficients).
+    """
+    def pair(x, y):
+        if Vd is not None:
+            return _pair_diag(Vd, arrays[x], arrays[y], sig, mode)
+        if y in applied:
+            return _pair_applied(arrays[x], applied[y], sig, mode)
+        return _pair_applied(applied[x], arrays[y], sig, mode)
+
+    hb2 = hbar * hbar
+    out = {
+        "d1": _anti(pair("HL", "L"), mode, hbar),
+        "d2": -(_sym(pair("H2L", "L"), mode) - _sym(pair("HL", "HL"), mode)) / hb2,
+    }
+    if m > 0:
+        P = (1j / hbar) * (pair("HL", "dL") - pair("L", "HdL"))
+        Q = pair("H2L", "dL") - 2.0 * pair("HL", "HdL") + pair("L", "H2dL")
+        U = pair("HBL", "L") + pair("BHL", "L") - 2.0 * pair("BL", "HL")
+        out["hom1"] = _sym(P, mode)
+        out["hom2"] = -_sym(Q, mode) / hb2
+        out["G1"] = _anti(pair("BL", "L"), mode, hbar)
+        out["G2"] = -_sym(U, mode) / hb2
+    return out
+
+
 def _contract_node(*, operator, S, r, m, D, sig, mode, cells, values, presence, dt, budget,
-                   failures, normE, normH, consistency_tolerance, where):
-    """Means and responses of H, every E_alpha, every read and presence at one node.
+                   failures, normE, normH, consistency_tolerance, where, cE, dO, hbar):
+    """Means, responses and their time derivatives of H, every E_alpha, every read and
+    presence at one node.
 
     trace mode : scalars  <A> = sum_k s_k <l_k|A|l_k>,  2 Re sum_k s_k <l_k|A|dl_bk>.
     family mode: r x r    M_kl = <v_k|A|v_l>,  K_kl = <v_k|A|dv_bl> + <dv_bk|A|v_l>.
     E_alpha and H are applied through the operator (Hermitian premise: <A l|dl> = <l|A|dl>);
-    reads/presence are contracted with their materialized diagonals.
+    reads/presence are contracted with their materialized diagonals. v002: the same-state
+    first/second time derivatives (module docstring, TIME DERIVATIVES) use H applied to
+    [L, dL] and to its image, B_b L and B_b H L (cE, dO), H B_b L, and E_alpha applied to
+    [L, H L, H^2 L]; the v001 means/responses use the same H L and E_alpha L columns.
     """
     L = S[:, :r]
     dLr = S[:, r:].reshape(D, m, r)
     Lc = np.conj(L)
-    HL = _apply_block(operator=operator, method="apply_H", kwargs={}, block=L, D=D, dt=dt,
+    Y1 = _apply_block(operator=operator, method="apply_H", kwargs={}, block=S, D=D, dt=dt,
+                      budget=budget, failures=failures, bound=normH,
+                      consistency_tolerance=consistency_tolerance,
+                      what=f"H mean and first time derivative at {where}")
+    if Y1 is None:
+        return None
+    Y2 = _apply_block(operator=operator, method="apply_H", kwargs={}, block=Y1, D=D, dt=dt,
                       budget=budget, failures=failures, bound=normH,
-                      consistency_tolerance=consistency_tolerance, what=f"H mean at {where}")
-    if HL is None:
+                      consistency_tolerance=consistency_tolerance,
+                      what=f"second time derivative at {where}")
+    if Y2 is None:
         return None
+    HL = Y1[:, :r]
+    H2L = Y2[:, :r]
+    arrays = {"L": L, "HL": HL, "H2L": H2L}
+    if m > 0:
+        arrays.update({"dL": dLr, "HdL": Y1[:, r:].reshape(D, m, r),
+                       "H2dL": Y2[:, r:].reshape(D, m, r)})
+        # Source generators B_b = sum_alpha cE[b,alpha] E_alpha - diag(dO_b) on L and H L.
+        BL = np.zeros((D, m, r), dtype=dt)
+        BHL = np.zeros((D, m, r), dtype=dt)
+        LHL = np.concatenate([L, HL], axis=1)
+        for ia, alpha in enumerate(cells):
+            bs = [b for b in range(m) if float(cE[b, ia]) != 0.0]
+            if not bs:
+                continue
+            Zb = _apply_block(operator=operator, method="apply_E", kwargs={"alpha": alpha},
+                              block=LHL, D=D, dt=dt, budget=budget, failures=failures,
+                              bound=normE[ia], consistency_tolerance=consistency_tolerance,
+                              what=f"source generators at {where}, cell index {ia}")
+            if Zb is None:
+                return None
+            for b in bs:
+                coeff = float(cE[b, ia])
+                BL[:, b, :] += coeff * Zb[:, :r]
+                BHL[:, b, :] += coeff * Zb[:, r:]
+        del LHL
+        for b in range(m):
+            BL[:, b, :] -= dO[b][:, None] * L
+            BHL[:, b, :] -= dO[b][:, None] * HL
+        HB = _apply_block(operator=operator, method="apply_H", kwargs={},
+                          block=BL.reshape(D, m * r), D=D, dt=dt, budget=budget,
+                          failures=failures, bound=normH,
+                          consistency_tolerance=consistency_tolerance,
+                          what=f"H on source generators at {where}")
+        if HB is None:
+            return None
+        arrays.update({"BL": BL, "BHL": BHL, "HBL": HB.reshape(D, m, r)})
+        Eblock = np.concatenate([L, HL, H2L], axis=1)
+    else:
+        Eblock = np.concatenate([L, HL], axis=1)
     n_E = len(cells)
     out = {}
     if mode == "trace":
         out["H"] = complex(np.einsum("xk,xk,k->", Lc, HL, sig, optimize=False))
         E_mean = np.zeros(n_E, dtype=np.complex128)
         E_resp = np.zeros((n_E, m), dtype=np.float64)
+        Ed = {"d1": np.zeros(n_E, dtype=np.float64), "d2": np.zeros(n_E, dtype=np.float64)}
+        Ed.update({key: np.zeros((n_E, m), dtype=np.float64)
+                   for key in ("hom1", "hom2", "G1", "G2")})
     else:
         out["H"] = np.einsum("xk,xl->kl", Lc, HL, optimize=False).astype(np.complex128)
         E_mean = np.zeros((n_E, r, r), dtype=np.complex128)
         E_resp = np.zeros((n_E, m, r, r), dtype=np.complex128)
+        Ed = {"d1": np.zeros((n_E, r, r), dtype=np.complex128),
+              "d2": np.zeros((n_E, r, r), dtype=np.complex128)}
+        Ed.update({key: np.zeros((n_E, m, r, r), dtype=np.complex128)
+                   for key in ("hom1", "hom2", "G1", "G2")})
     for ia, alpha in enumerate(cells):
-        EL = _apply_block(operator=operator, method="apply_E", kwargs={"alpha": alpha}, block=L,
-                          D=D, dt=dt, budget=budget, failures=failures, bound=normE[ia],
-                          consistency_tolerance=consistency_tolerance,
-                          what=f"E mean/response at {where}, cell index {ia}")
-        if EL is None:
+        Z = _apply_block(operator=operator, method="apply_E", kwargs={"alpha": alpha},
+                         block=Eblock, D=D, dt=dt, budget=budget, failures=failures,
+                         bound=normE[ia], consistency_tolerance=consistency_tolerance,
+                         what=f"E mean/response/time derivatives at {where}, cell index {ia}")
+        if Z is None:
             return None
+        EL = Z[:, :r]
         if mode == "trace":
             E_mean[ia] = np.einsum("xk,xk,k->", Lc, EL, sig, optimize=False)
             E_resp[ia] = 2.0 * np.einsum("xk,xbk,k->b", np.conj(EL), dLr, sig,
@@ -588,6 +832,13 @@
             E_mean[ia] = np.einsum("xk,xl->kl", Lc, EL, optimize=False)
             Mb = np.einsum("xk,xbl->bkl", np.conj(EL), dLr, optimize=False)
             E_resp[ia] = Mb + np.conj(np.swapaxes(Mb, 1, 2))
+        applied = {"L": EL, "HL": Z[:, r:2 * r]}
+        if m > 0:
+            applied["H2L"] = Z[:, 2 * r:3 * r]
+        terms = _derivative_terms(arrays=arrays, applied=applied, Vd=None, sig=sig, m=m,
+                                  mode=mode, hbar=hbar)
+        for key, val in terms.items():
+            Ed[key][ia] = val
     out["E"] = E_mean
     out["E_resp"] = E_resp
     if mode == "trace":
@@ -604,6 +855,13 @@
         Pb = np.einsum("ax,xk,xbl->abkl", presence, Lc, dLr, optimize=False)
         out["O_resp"] = Ob + np.conj(np.swapaxes(Ob, 2, 3))
         out["P_resp"] = Pb + np.conj(np.swapaxes(Pb, 2, 3))
+    Od = _derivative_terms(arrays=arrays, applied=None, Vd=values, sig=sig, m=m, mode=mode,
+                           hbar=hbar)
+    Pd = _derivative_terms(arrays=arrays, applied=None, Vd=presence, sig=sig, m=m, mode=mode,
+                           hbar=hbar)
+    # Output order as v001: all E_alpha, then every read row; presence rows separately.
+    out["deriv"] = {key: np.concatenate([Ed[key], Od[key]], axis=0) for key in Od}
+    out["deriv_P"] = Pd
     out["norm_L"] = _fro(L)
     out["norm_dL"] = np.array([_fro(dLr[:, b, :]) for b in range(m)], dtype=np.float64)
     return out
@@ -633,18 +891,53 @@
     G, F, column selection, apply copy and output (5 m r), the Taylor window (P+1) r, node
     contraction temporaries (4 r), dO (m) and the probe (1), all times D; plus outputs,
     bounds and by-kind copies (r x r complex in family mode, with the einsum temporaries).
+    v002 time derivatives add, conservatively and as if simultaneous with propagation:
+    node columns H[L, dL] and H^2[L, dL] (2 (1+m) r), B L, B H L, H B L with apply copies
+    (6 m r), [L, H L] and [L, H L, H^2 L] with apply copies/outputs (16 r), conjugate and
+    trace-weight temporaries (4 m), all times D; plus derivative outputs (mean first/second,
+    homogeneous/contact pieces, one-sided totals), their bounds, by-kind copies and profile
+    node values, and 12 (n_out + n_read)(1 + m) per-node derivative temporaries (each
+    [r, r] complex in family mode).
     """
     cols = (1 + m) * r
     entries = D * (7 * cols + 5 * m * r + P1 * r + 4 * r + m + 1)
+    entries += D * (2 * cols + 6 * m * r + 16 * r + 4 * m)
+    deriv_vals = (n_out + n_read) * n_obs * (2 + 8 * m) + n_read * n_obs * (4 + 4 * m)
+    deriv_bds = (n_out + n_read) * n_obs * (2 + 8 * m) + 4 * m * n_obs
+    deriv_tmp = 12 * (n_out + n_read) * (1 + m)
     if mode == "trace":
         entries += 3 * (n_out + n_read + 1) * n_obs * (1 + m)
+        entries += deriv_vals + deriv_bds + deriv_tmp
     else:
         rr = r * r
         entries += (3 * (n_out + n_read + 1) * n_obs * (1 + m) * rr
                     + 4 * n_read * m * rr + 2 * (n_out - n_read) * m * rr)
+        entries += (deriv_vals + deriv_tmp) * rr + deriv_bds
     return entries
 
 
+def _profile_node_values(*, prof, grid):
+    """One-sided node values of the declared per-interval polynomial profiles (L16).
+
+    prof[b, k, p] multiplies (t - t_k)^p on [t_k, t_{k+1}]. Returns float64 [m, K] arrays:
+    f_left, df_left  = f_b and f_b' at node k+1 from interval k (tau = t_{k+1} - t_k);
+    f_right, df_right = f_b and f_b' at node k from interval k (tau = 0).
+    Exact algebra evaluated in float64; no interpolation or side choice.
+    """
+    m, K, P1 = prof.shape
+    f_left = np.zeros((m, K), dtype=np.float64)
+    df_left = np.zeros((m, K), dtype=np.float64)
+    f_right = prof[:, :, 0].copy()
+    df_right = prof[:, :, 1].copy() if P1 > 1 else np.zeros((m, K), dtype=np.float64)
+    for k in range(K):
+        tau = float(grid[k + 1]) - float(grid[k])
+        for p in range(P1):
+            f_left[:, k] += prof[:, k, p] * (tau ** p)
+            if p >= 1:
+                df_left[:, k] += float(p) * prof[:, k, p] * (tau ** (p - 1))
+    return f_left, df_left, f_right, df_right
+
+
 # ---------------------------------------------------------------------------
 # Result skeletons
 # ---------------------------------------------------------------------------
@@ -705,6 +998,51 @@
             "derivatives; covariance-only response is never inverted here; the "
             "register-spec property tr C <= 4 is documented, never clipped"
         ),
+        "time_derivatives": {
+            "read_frame_partial": {
+                "value": 0.0,
+                "statement": (
+                    "declared read_frame 'fixed_current_state_reads': every E_alpha, read and "
+                    "presence row is a fixed current-state operator with fixed registration, "
+                    "frame, scale and support, so partial_t A = partial_t^2 A = 0 and the "
+                    "(2i/hbar)[K, partial_t A] term of A_O is zero; 1/m_alpha, presence and "
+                    "adjacency changes are inside A and act through the commutator (no "
+                    "separate count derivative). Other declarations fail explicitly"
+                ),
+            },
+            "background_generator_K_prime": {
+                "value": 0.0,
+                "statement": (
+                    "declared background_generator 'flat_point_time_independent_H': the "
+                    "zeroth-order generator is K = H at n = 0, j = 0, N_bg = 1, tau = t, so "
+                    "K' = 0 for the means; a nonzero or time-dependent background lapse/source "
+                    "needs H[n0(t), j0(t)] and fails explicitly (LIMITATIONS L4, L17)"
+                ),
+            },
+            "source_generator_K_prime": (
+                "first order: K = H + sum_b f_b(t) B_b, K' = sum_b f_b'(t) B_b; its term "
+                "f_b'(t) G1[A,b] = (i/hbar) <[K',A]>_0 is RETAINED in every response second "
+                "derivative and returned separately (time_derivatives['response'] contact_G1 "
+                "with profile_at_nodes df), never dropped"
+            ),
+            "proper_time": (
+                "derivatives are in the native time t of time_grid. For a homogeneous "
+                "background lapse N_bg(t): d/dtau = N_bg^-1 d/dt, d2/dtau2 = N_bg^-2 d2/dt2 "
+                "- N_bg^-3 (dN_bg/dt) d/dt. Linearized about N_bg = 1 for a uniform lapse "
+                "column with all energy coefficients equal to c (delta N_bg = c f_b): "
+                "delta(dA/dtau) = delta(dA/dt) - c f_b dA/dt, delta(d2A/dtau2) = "
+                "delta(d2A/dt2) - 2 c f_b d2A/dt2 - c f_b' dA/dt; every ingredient is "
+                "returned. A spatially nonuniform lapse keeps the coordinate-time foliation "
+                "(HP addendum); per-cell clocks are not averaged here"
+            ),
+            "c_number_frame": (
+                "a registered frame acting linearly on fixed rows, O(t) = T(t) O, is a "
+                "caller-side combination: d<TO>/dt = T'<O> + T<O>', d2<TO>/dt2 = T''<O> + "
+                "2 T'<O>' + T<O>'' (and the same for responses); on the source side it is "
+                "represented exactly by fixed-row columns whose declared profiles carry the "
+                "frame time dependence, whose K' terms are then the returned f_b' G1"
+            ),
+        },
     }
 
 
@@ -716,6 +1054,7 @@
         "flags": [],
         "means": None,
         "response": None,
+        "time_derivatives": None,
         "error_bounds": None,
         "contacts": _contacts_statement(),
         "resources": {},
@@ -737,6 +1076,12 @@
             ),
             "units": "one caller-declared consistent system; no conversion",
             "reduction": "full-H propagation only; no P/Q reduction is implemented",
+            "time_derivatives": (
+                "native time t; means first = <L_A> = (i/hbar)<[H,A]>, second = <A_A> = "
+                "-(1/hbar^2)<[H,[H,A]]>; response first = hom1 + f_b G1, second = hom2 + "
+                "f_b G2 + f_b' G1 (f_b' G1 = (i/hbar)<[K',A]>_0), one-sided at nodes: left = "
+                "nodes 1..K from interval k-1, right = nodes 0..K-1 from interval k"
+            ),
         },
     }
 
@@ -746,7 +1091,7 @@
 # ---------------------------------------------------------------------------
 
 def propagate_source_columns(*, operator, preparation, source_columns, time_grid, hbar,
-                             stepper, caps, dtype):
+                             stepper, caps, dtype, time_derivative_contacts):
     """Same-state full-H primal + tangent propagation; native means and joint responses.
 
     Arguments (keyword-only, required, no defaults):
@@ -783,10 +1128,16 @@
       caps: {"max_working_entries": int > 0, "max_column_applications": int > 0,
         "max_substeps": int > 0}; exceeded caps fail explicitly before being exceeded.
       dtype: a complex numpy dtype for all propagated arrays.
-
-    Returns a dict {ok, stage_reached, failures, flags, means, response, error_bounds,
-    contacts, resources, conventions}. means, response and error_bounds are filled only on
-    complete success. Shapes (n_obs = K + 1, n_out = n_E + n_read):
+      time_derivative_contacts (v002, ADDENDUM item 1; LIMITATIONS L17): {"read_frame":
+        "fixed_current_state_reads", "background_generator": "flat_point_time_independent_H"}
+        -- the explicit declaration of the read/frame partial-derivative and background
+        generator K' terms (both zero for these declarations); any other key set or value
+        fails explicitly, never silently dropped.
+
+    Returns a dict {ok, stage_reached, failures, flags, means, response, time_derivatives,
+    error_bounds, contacts, resources, conventions}. means, response, time_derivatives and
+    error_bounds are filled only on complete success. Shapes (n_obs = K + 1,
+    n_out = n_E + n_read):
       trace mode (purification, density):
         means["E"] [n_E, n_obs], means["H"] [n_obs], means["O"] [n_read, n_obs],
         means["presence"] [n_read, n_obs], means["by_kind"][token] = {"rows", "O",
@@ -798,6 +1149,19 @@
         [n_read, n_obs], "response" [n_out, m, n_obs], "presence_response"
         [n_read, m, n_obs], "primal_state_fro" [n_obs], "tangent_state_fro" [m, n_obs],
         "source_quadrature" 0.0, plus statements of what is and is not covered.
+      time_derivatives (v002; trace mode shown, family mode adds trailing [r, r]):
+        "means": {"first", "second" [n_out, n_obs], "presence_first", "presence_second"
+          [n_read, n_obs], "by_kind"[token] = {"rows", "output_rows", "first", "second",
+          "presence_first", "presence_second"}};
+        "response": {"homogeneous_first", "homogeneous_second", "contact_G1", "contact_G2"
+          [n_out, m, n_obs] and "presence_..." [n_read, m, n_obs] versions;
+          "profile_at_nodes": {"left": {"nodes", "f", "df"}, "right": {...}} with [m, K];
+          "left": {"nodes" (1..K), "first", "second" [n_out, m, K], "presence_first",
+          "presence_second" [n_read, m, K]}; "right": the same for nodes 0..K-1;
+          "by_kind"[token] = {"output_rows", "left_first", "left_second", "right_first",
+          "right_second"}}.
+        error_bounds["time_derivatives"] holds a real bound array of the same leading
+        shape for every array above (no by_kind copies), plus covered/not-covered text.
     """
     result = _new_propagation_result()
     failures = result["failures"]
@@ -837,6 +1201,26 @@
         cap_cols = _admit_positive_int("caps.max_column_applications",
                                        cp["max_column_applications"], failures)
         cap_sub = _admit_positive_int("caps.max_substeps", cp["max_substeps"], failures)
+    # v002 (ADDENDUM item 1; LIMITATIONS L17): explicit read/frame and background-generator
+    # declarations for the time-derivative reads; unsupported declarations fail closed.
+    tdc = _admit_mapping("time_derivative_contacts", time_derivative_contacts,
+                         ("read_frame", "background_generator"), failures)
+    if tdc is not None:
+        rf = tdc["read_frame"]
+        if not (isinstance(rf, str) and rf == _READ_FRAME_FIXED):
+            failures.append(
+                f"input time_derivative_contacts.read_frame: {rf!r} is not "
+                f"{_READ_FRAME_FIXED!r}; an explicitly time-dependent read, registration, "
+                "frame, scale or support needs its partial derivatives and transformed "
+                "generator, which the shared operator interface cannot supply (not dropped)"
+            )
+        bg = tdc["background_generator"]
+        if not (isinstance(bg, str) and bg == _BACKGROUND_FLAT):
+            failures.append(
+                f"input time_derivative_contacts.background_generator: {bg!r} is not "
+                f"{_BACKGROUND_FLAT!r}; a nonzero or time-dependent background lapse/source "
+                "generator (K' != 0 at zeroth order) is not implemented (LIMITATIONS L4)"
+            )
     grid = _admit_array("time_grid", time_grid, 1, False, failures)
     if grid is not None:
         if grid.shape[0] < 2:
@@ -1181,8 +1565,12 @@
     norm_L0 = _fro(L0)
     cols = (1 + m) * r
     resources["r"] = r
+    # v002 node work: apply_H on [L, dL], on its image and (m > 0) on B L; apply_E per cell
+    # on [L, H L, H^2 L] ([L, H L] when m = 0) and per source-carrying cell on [L, H L].
+    n_E_src = sum(1 for ia in range(n_E) if m > 0 and bool(np.any(cE[:, ia] != 0.0)))
+    node_cols = (2 * cols + m * r + n_E * (3 if m > 0 else 2) * r + n_E_src * 2 * r)
     resources["worst_case_column_applications"] = (
-        n_read + total_sub * (max_order + 1) * (cols + n_E * m * r) + n_obs * (1 + n_E) * r)
+        n_read + total_sub * (max_order + 1) * (cols + n_E * m * r) + n_obs * node_cols)
 
     # ---- Stage 6: propagation ------------------------------------------------------------
     result["stage_reached"] = "propagation"
@@ -1207,6 +1595,23 @@
     bd_Presp = np.zeros((n_read, m, n_obs), dtype=np.float64)
     eps_L_hist = np.zeros(n_obs, dtype=np.float64)
     eps_b_hist = np.zeros((m, n_obs), dtype=np.float64)
+    # v002 time-derivative outputs (ADDENDUM item 1) and their bounds.
+    if mode == "trace":
+        tail, cdt = (), np.float64
+    else:
+        tail, cdt = (r, r), np.complex128
+    TD = {"first": np.zeros((n_out, n_obs) + tail, dtype=cdt),
+          "second": np.zeros((n_out, n_obs) + tail, dtype=cdt),
+          "presence_first": np.zeros((n_read, n_obs) + tail, dtype=cdt),
+          "presence_second": np.zeros((n_read, n_obs) + tail, dtype=cdt)}
+    TR = {}
+    for key in ("hom1", "hom2", "G1", "G2"):
+        TR[key] = np.zeros((n_out, m, n_obs) + tail, dtype=cdt)
+        TR["presence_" + key] = np.zeros((n_read, m, n_obs) + tail, dtype=cdt)
+    BD = {key: np.zeros(arr.shape[:2], dtype=np.float64) for key, arr in TD.items()}
+    BD.update({key: np.zeros(arr.shape[:3], dtype=np.float64) for key, arr in TR.items()})
+    c1 = 2.0 * normH / hbar_in
+    c2 = 4.0 * normH * normH / (hbar_in * hbar_in)
     opnorm = np.concatenate([np.array(normE, dtype=np.float64), normO])
     imag_max = 0.0
     drift_max = 0.0
@@ -1248,7 +1653,8 @@
         node = _contract_node(operator=operator, S=S, r=r, m=m, D=D, sig=sig, mode=mode,
                               cells=cells, values=values, presence=presence, dt=dt,
                               budget=budget, failures=failures, normE=normE, normH=normH,
-                              consistency_tolerance=ctol, where=f"node {i}")
+                              consistency_tolerance=ctol, where=f"node {i}", cE=cE, dO=dO,
+                              hbar=hbar_in)
         if node is None:
             return result
         if mode == "trace":
@@ -1281,14 +1687,70 @@
         bd_Presp[:, :, i] = pr
         eps_L_hist[i] = eps_L
         eps_b_hist[:, i] = eps_b
+        # v002 time derivatives on the same state, and their Cauchy-Schwarz bounds
+        # (module docstring, TIME DERIVATIVES / DERIVATIVE BOUNDS).
+        TD["first"][:, i] = node["deriv"]["d1"]
+        TD["second"][:, i] = node["deriv"]["d2"]
+        TD["presence_first"][:, i] = node["deriv_P"]["d1"]
+        TD["presence_second"][:, i] = node["deriv_P"]["d2"]
+        if m > 0:
+            for key in ("hom1", "hom2", "G1", "G2"):
+                TR[key][:, :, i] = node["deriv"][key]
+                TR["presence_" + key][:, :, i] = node["deriv_P"][key]
+        base = eps_L * (node["norm_L"] + norm_L0) + R1
+        for pre, onorm in (("", opnorm), ("presence_", normP)):
+            for order, cfac, hkey in (("first", c1, "hom1"), ("second", c2, "hom2")):
+                mb, rb = _node_bounds(opnorm=cfac * onorm, eps_L=eps_L, eps_b=eps_b,
+                                      norm_L=node["norm_L"], norm_L0=norm_L0,
+                                      norm_dL=node["norm_dL"], Bnorm=Bnorm, R1=R1,
+                                      absint=absint, hbar=hbar_in)
+                BD[pre + order][:, i] = mb
+                BD[pre + hkey][:, :, i] = rb
+            BD[pre + "G1"][:, :, i] = ((2.0 / hbar_in) * base) * (onorm[:, None]
+                                                                  * Bnorm[None, :])
+            BD[pre + "G2"][:, :, i] = ((8.0 * normH / (hbar_in * hbar_in)) * base) * (
+                onorm[:, None] * Bnorm[None, :])
 
     # ---- Stage 7: finite admission and packaging ---------------------------------------
     result["stage_reached"] = "packaging"
+    # v002: one-sided response time derivatives (LIMITATIONS L16) from the single-valued
+    # homogeneous and contact pieces and the exact one-sided profile node values.
+    f_left, df_left, f_right, df_right = _profile_node_values(prof=prof, grid=grid)
+    ex = (None, slice(None), slice(None)) + (None,) * len(tail)
+    exb = (None, slice(None), slice(None))
+    sides = {}
+    for side, fv, dfv, sl, nodes in (("left", f_left, df_left, slice(1, None),
+                                      tuple(range(1, n_obs))),
+                                     ("right", f_right, df_right, slice(0, K),
+                                      tuple(range(0, K)))):
+        f_e, df_e = fv[ex], dfv[ex]
+        fa, dfa = np.abs(fv)[exb], np.abs(dfv)[exb]
+        vals, bds = {"nodes": nodes}, {"nodes": nodes}
+        for pre in ("", "presence_"):
+            g1 = TR[pre + "G1"][:, :, sl]
+            vals[pre + "first"] = TR[pre + "hom1"][:, :, sl] + f_e * g1
+            vals[pre + "second"] = (TR[pre + "hom2"][:, :, sl] + f_e * TR[pre + "G2"][:, :, sl]
+                                    + df_e * g1)
+            bg1 = BD[pre + "G1"][:, :, sl]
+            bds[pre + "first"] = BD[pre + "hom1"][:, :, sl] + fa * bg1
+            bds[pre + "second"] = (BD[pre + "hom2"][:, :, sl] + fa * BD[pre + "G2"][:, :, sl]
+                                   + dfa * bg1)
+        sides[side] = {"f": fv, "df": dfv, "values": vals, "bounds": bds}
     named = (("means E", E_mean), ("means H", H_mean), ("means O", O_mean),
              ("means presence", P_mean), ("response", resp), ("presence response", P_resp),
              ("bound means", bd_mean), ("bound H", bd_H), ("bound presence", bd_P),
              ("bound response", bd_resp), ("bound presence response", bd_Presp),
              ("primal state bound", eps_L_hist), ("tangent state bound", eps_b_hist))
+    named += tuple((f"time derivative {key}", arr) for key, arr in TD.items())
+    named += tuple((f"time derivative response {key}", arr) for key, arr in TR.items())
+    named += tuple((f"time derivative bound {key}", arr) for key, arr in BD.items())
+    for side, sd in sides.items():
+        named += ((f"profile {side} node values", sd["f"]),
+                  (f"profile {side} node derivatives", sd["df"]))
+        named += tuple((f"time derivative response {side} {key}", arr)
+                       for key, arr in sd["values"].items() if key != "nodes")
+        named += tuple((f"time derivative bound {side} {key}", arr)
+                       for key, arr in sd["bounds"].items() if key != "nodes")
     for name, arr in named:
         bad = int(np.count_nonzero(~np.isfinite(arr)))
         if bad:
@@ -1335,6 +1797,64 @@
             "bounds on Frobenius norms of the r x r compressed error matrices (valid for every "
             "family density of trace norm <= 1)" if mode == "family" else None),
     }
+    # v002: MANDATORY ADDENDUM V001 item 1 outputs (module docstring, TIME DERIVATIVES).
+    out_rows = {kd: [n_E + i for i in rows] for kd, rows in rows_by_kind.items()}
+    result["time_derivatives"] = {
+        "mode": mode,
+        "time_parameter": "native time t of time_grid (flat point: tau = t, N_bg = 1)",
+        "output_labels": out_labels, "source_labels": tuple(src_labels),
+        "means": {
+            "first": TD["first"], "second": TD["second"],
+            "presence_first": TD["presence_first"], "presence_second": TD["presence_second"],
+            "by_kind": {kd: {"rows": rows, "output_rows": tuple(out_rows[kd]),
+                             "first": TD["first"][out_rows[kd]],
+                             "second": TD["second"][out_rows[kd]],
+                             "presence_first": TD["presence_first"][list(rows)],
+                             "presence_second": TD["presence_second"][list(rows)]}
+                        for kd, rows in rows_by_kind.items()},
+        },
+        "response": {
+            "homogeneous_first": TR["hom1"], "homogeneous_second": TR["hom2"],
+            "contact_G1": TR["G1"], "contact_G2": TR["G2"],
+            "presence_homogeneous_first": TR["presence_hom1"],
+            "presence_homogeneous_second": TR["presence_hom2"],
+            "presence_contact_G1": TR["presence_G1"],
+            "presence_contact_G2": TR["presence_G2"],
+            "profile_at_nodes": {
+                side: {"nodes": sd["values"]["nodes"], "f": sd["f"], "df": sd["df"]}
+                for side, sd in sides.items()},
+            "left": sides["left"]["values"], "right": sides["right"]["values"],
+            "by_kind": {kd: {"output_rows": tuple(out_rows[kd]),
+                             "left_first": sides["left"]["values"]["first"][out_rows[kd]],
+                             "left_second": sides["left"]["values"]["second"][out_rows[kd]],
+                             "right_first": sides["right"]["values"]["first"][out_rows[kd]],
+                             "right_second": sides["right"]["values"]["second"][out_rows[kd]]}
+                        for kd, rows in rows_by_kind.items()},
+        },
+    }
+    result["error_bounds"]["time_derivatives"] = {
+        "means_first": BD["first"], "means_second": BD["second"],
+        "presence_means_first": BD["presence_first"],
+        "presence_means_second": BD["presence_second"],
+        "response_homogeneous_first": BD["hom1"], "response_homogeneous_second": BD["hom2"],
+        "contact_G1": BD["G1"], "contact_G2": BD["G2"],
+        "presence_response_homogeneous_first": BD["presence_hom1"],
+        "presence_response_homogeneous_second": BD["presence_hom2"],
+        "presence_contact_G1": BD["presence_G1"], "presence_contact_G2": BD["presence_G2"],
+        "left": sides["left"]["bounds"], "right": sides["right"]["bounds"],
+        "covered": (
+            "the same primal/tangent state bounds and factorization residual propagated "
+            "through same-state commutator reads by Cauchy-Schwarz with ||(i/hbar)[H,A]|| <= "
+            "2 normH ||A||/hbar, ||[H,[H,A]]||/hbar^2 <= 4 normH^2 ||A||/hbar^2, ||G1 "
+            "operator|| <= 2 ||B_b|| ||A||/hbar, ||G2 operator|| <= 8 normH ||B_b|| "
+            "||A||/hbar^2, and |f_b|, |f_b'| at the stated node side"
+        ),
+        "not_covered": (
+            "the v001 rounding list, also for the extra matvecs and contractions and for the "
+            "float64 evaluation of f_b, f_b' at nodes; premises as v001 plus normH a true "
+            "bound on ||H||_2 (observed on every apply_H as a necessary condition only)"
+        ),
+    }
     resources["taylor_orders"] = {
         "min": min(orders) if orders else None, "max": max(orders) if orders else None,
         "total": int(sum(orders))}
@@ -1347,8 +1867,10 @@
         H_mean - np.sum(E_mean, axis=0))
     resources["cost_statement"] = (
         "per substep (N+1) apply_H on [D, r(1+m)] plus forcing apply_E per active cell; per "
-        "node 1 apply_H and n_E apply_E on [D, r]; memory O(D r (12 m + P + 12)); D is the "
-        "full owned inventory component (exponential in V0), not reduced here"
+        "node (v002, with time derivatives) apply_H twice on [D, r(1+m)] and once on "
+        "[D, m r], apply_E per cell on [D, 3r] ([D, 2r] if m = 0) and per source-carrying "
+        "cell on [D, 2r]; memory O(D r (20 m + P + 30)); D is the full owned inventory "
+        "component (exponential in V0), not reduced here"
     )
     result["ok"] = True
     result["stage_reached"] = "complete"
```
