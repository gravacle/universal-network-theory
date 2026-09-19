"""THE UNIVERSAL RECORD MODEL (URM) — named by the principal, 2026-08-20.
One object that represents the entire program, and the overall representation of the proof:
PROOF_V002 is this model's narration. "Universal" is operational — one model, any record surface
(T-33: six mechanisms at machine precision; D-25: world-tier surfaces provenance-pinned) — and is a
title, not a claim.

The principal, 2026-08-20: "We need a model to work on that represents the full project."

Layers, each resting on registered rows:
  DEFINITION   clauses (i')-(v') with tolerances (O-51; census GR1-GR4)  -> ProjectModel.clauses
  LAWS         lifetime and steady value from the record's own Liouvillian mode
               (C-69, C-70 -- FORMAL, six mechanisms)                    -> .lifetime, .steady_value
  FORMATION    written vs unwritten configuration; the five source
               standards (C-71 PROVED; C-72 PARTIAL)                     -> .configuration
  CORNER       t_m -> infinity, W -> 0 reduces to the exact commutant
               records of record_model (C-75, T-28)                      -> .corner
  GEOMETRY     the C-77 increments as a first-class layer (T-46):
               earned distance d_W (C-78), interface rank + the
               boundary law, both tiers (C-79), the two-region
               taxonomy and w_min = d (C-80), certifiability and
               the locality zero (C-81), the certification window
               law (C-83), encoding-level formation (C-71/C-72)          -> .distance,
               .interface_rank, .world_interface, .mutual_interface,
               .winding_interface, .coupling_cost, .certifiability,
               .cert_window, .formation_orientation, .formation_occupancy
               (machinery ported from the sealed lanes in model/geometry.py)
  ARROW        record threshold, entanglement-without-record, inside
               invariance, history, and fragment redundancy (F-17..F-21) -> .arrow_*
  COUNT LAW    the surviving-record census and its two widths (C-86)      -> .census, .count_widths
  CLASSES      venue-earned coupling classes and critical kernel
               (C-87, C-90)                                              -> .coupling_venue, .reachable_class, ...
  WRITING      conserving/critical writer kernels and the surface gap
               (C-91)                                                    -> .writing_*
  ROLES        the four role sentences, honestly scoped                  -> .roles
  ALPHA ROLE   exact ALLOW/REQUIRE/SELECT typing for physical alpha       -> .alpha_role,
                                                                             .alpha_role_certificate
  U-DCL        adopted working postulate plus exact conditional universal
               Coverage-U theorem; natural validity remains open          -> .udcl_postulate,
                                                                             .udcl_postulate_certificate
  WORLD INPUT  source-custodied observations with no automatic verdict     -> .world_observation,
                                                                             .world_observation_certificate
  FORM INPUT   generic formation-data contract with zero proof promotion   -> .formation_input,
                                                                             .formation_input_certificate
  GAMMA FLOW   origin-neutral flow states and explicitly typed outputs     -> .gamma_flow,
                                                                             .gamma_flow_certificate,
                                                                             .gamma_flow_states,
                                                                             .gamma_flow_proof_outputs
  FRONTIER     missing-data and theory-state proof boundary                -> .proof_frontier,
                                                                             .proof_frontier_certificate,
                                                                             .proof_frontier_proof_states,
                                                                             .proof_frontier_theory_states,
                                                                             .proof_frontier_execution_frontier
  H-GRAVITY    finite-group historywise nonselection discriminant          -> .historywise_gravity_discriminant,
                                                                             .historywise_gravity_discriminant_certificate
  GFT          conditional record-first working-theory closure             -> .gravity_formation_theory,
                                                                             .gravity_formation_theory_certificate
  MICRO-G      additive microscopic-gravity progress checkpoint            -> .gravity_microscopic_progress,
                                                                             .gravity_microscopic_progress_certificate
  RELATIONAL   adopted finite ARGER formation Gate; closed L14 seam       -> .relational_accumulation,
                                                                             .relational_accumulation_certificate
  UNT          top-level typed composition with all proof types retained   -> .universal_network_theory,
                                                                             .universal_network_theory_certificate

A RecordSurface is a physicist-supplied parameterization of a device or specimen in SI; it is
not by itself real-world validation.  Actual measurements enter separately through
URM.world_observation(), whose closed bundle preserves raw-source custody, normalization, units,
coverage, and provenance while issuing no scientific verdict.  A new law is a layer method with
a validator gate and claim row; agreement with the world requires a prospectively frozen
prediction and an actual-surface comparison with stated tolerance, semantics, and a power
control.  validate_urm.py is the integrated conjunction; validate_project.py preserves the
public-entry and backward-compatibility gates."""
import numpy as np
import grounded as G

_SZ = np.array([[1, 0], [0, -1]], dtype=complex)
_SP = np.array([[0, 1], [0, 0]], dtype=complex)
_SM = _SP.conj().T


class RecordSurface:
    """A real record surface: named constants in SI units. dE and E_b in J, T in K, f0 in Hz."""
    def __init__(self, name, mechanism, dE, E_b, T, f0, thermal=True):
        self.name, self.mechanism = name, mechanism
        self.dE, self.E_b, self.T, self.f0, self.thermal = dE, E_b, T, f0, thermal

    def open_system(self):
        """(H, {L_k}) for the two-state record. CONVENTION (corrected per the solidity review):
           E_b is the ACTIVATION ENERGY FROM THE METASTABLE (upper) WELL -- the standard Arrhenius
           meaning. Escape from upper: f0 exp(-E_b/kT); from lower: f0 exp(-(E_b+dE)/kT); detailed
           balance holds automatically. The earlier midpoint convention silently reduced the escape
           barrier by dE/2, producing a 5-6 order contradiction with the measured azobenzene cis
           lifetime. Returns None where the surface is NOT thermally activated -- the model DECLINES
           rather than returning a number."""
        if not self.thermal:
            return None
        kT = G.KB * self.T
        gu = self.f0 * np.exp(-self.E_b / kT)              # escape from the metastable well
        gd = self.f0 * np.exp(-(self.E_b + self.dE) / kT)  # reverse, from the lower well
        if not (np.isfinite(gd) and np.isfinite(gu)) or (gd < 1e-300 and gu < 1e-300):
            return None
        H = -(self.dE / 2) * _SZ
        return H, [np.sqrt(gd) * _SM, np.sqrt(gu) * _SP], _SZ


class ProjectModel:
    # ---------------------------------------------------------------- DEFINITION (O-51)
    def clauses(self, s, t_m, C_v, W_write):
        """The five amended clauses on a RecordSurface, with the tolerances declared."""
        sys = s.open_system()
        if sys is None:
            return dict(applies=False, why="not a thermally activated two-state record; the model declines")
        H, Ls, R = sys
        return dict(applies=True,
                    i=dict(spectral_family=True),
                    ii=G.clause_ii(H, Ls, R, t_m),
                    iii=G.clause_iii(s.dE, s.T, C_v),
                    iv=G.clause_iv(W_write, s.dE, s.T),
                    v=G.clause_v(s.E_b, s.T))

    # ---------------------------------------------------------------- LAWS (C-69, C-70; FORMAL)
    def lifetime(self, s):
        """tau from the RECORD'S OWN Liouvillian mode. Closed form exp(E_b/kT)/f0 is the check,
           never the source."""
        sys = s.open_system()
        if sys is None:
            return None
        H, Ls, R = sys
        return G.lifetime(H, Ls, R)

    def steady_value(self, s):
        """<R>_ss from the Liouvillian's stationary state. Closed form tanh(dE/2kT) is the check."""
        sys = s.open_system()
        if sys is None:
            return None
        H, Ls, R = sys
        if not Ls:
            return None    # no dissipator: a steady state is not defined; decline, never an arbitrary vector
        Lv = G.liouvillian(H, Ls)
        w, V = np.linalg.eig(Lv)
        j = int(np.argmin(np.abs(w)))
        rho = V[:, j].reshape(2, 2, order='F'); rho = rho / np.trace(rho)
        return float(np.real(np.trace(rho @ R)))

    # ---------------------------------------------------------------- FORMATION (C-71/C-72 machinery)
    def configuration(self, per_record, pattern):
        """The accumulated configuration quantity of a medium: per_record = the one-record magnitude
           (charge, moment-energy, ...), pattern = array of record values (0/±1). Returns the sum,
           the absolute sum, and |sum|/sum|.| -- the accumulation-vs-screening discriminator (C-46).
           The claim this machinery carries: the UNWRITTEN medium's accumulated quantity is null and
           WRITING creates an extensive, sign-definite value. Scoped pending the solidity review."""
        p = np.asarray(pattern, dtype=float)
        ssum, sabs = per_record * p.sum(), per_record * np.abs(p).sum()
        return dict(sum=ssum, abs_sum=sabs,
                    ratio=(abs(ssum) / sabs if sabs > 0 else None))

    # ---------------------------------------------------------------- CORNER (C-75; T-28)
    def corner(self, H, Ls=()):
        """DEF-A: at t_m -> infinity with no dissipation the slow modes are exactly the commutant,
           whose dimension is sum over eigenspaces of m_E^2. Both are returned so the reduction is
           CHECKED, never assumed."""
        rates, obs = G.slow_modes(H, list(Ls), np.inf)
        w = np.linalg.eigvalsh(np.asarray(H, dtype=complex)); mult = {}
        for x in w:
            key = round(float(x), 9); mult[key] = mult.get(key, 0) + 1
        return dict(slow_dim=len(rates), commutant_dim=sum(m * m for m in mult.values()))

    # ---------------------------------------------------------------- GEOMETRY (T-46; C-77 increments)
    # Every method below delegates to model/geometry.py, where the sealed-lane machinery
    # lives (exact F_2 bitmasks, writer searches, cut-ranks -- ported, not reimplemented).
    # Each geometry function's docstring names its claim row, sealed source, and owners.
    def distance(self, carrier, s, s2):
        """C-78: earned distance d_W between configurations s, s2 -- minimal admissible-
           writer weight, searched exhaustively (LANE_T42_A_DISTANCE, sealed).  carrier:
           the toric torus side L (the sealed venue).  On the torus d_W = L*a + L*b, the
           minimal boundary-crossing cost.  s, s2: label pairs in {0,1}^2."""
        import geometry as GE
        return GE.dW(int(carrier), s, s2)

    def distance_matrix(self, carrier):
        """C-78: the full 4x4 d_W class matrix on the toric carrier (side L = carrier),
           plus class minima and the computed code distance."""
        import geometry as GE
        return GE.dW_class_matrix(int(carrier))

    def interface_rank(self, L, s):
        """C-79 corner: cut-rank IR2 and content capacity capP of the s x s block at
           side L; thick scope: IR2 = 8s-10, capP = 2s^2+2s-5, and
           32*capP == (IR2+10)^2 + 8*(IR2+10) - 160 (LANE_T42_C_BOUNDCAP /
           LANE_T42_D_DERIVE, sealed)."""
        import geometry as GE
        return GE.interface_rank(L, s)

    def world_interface(self, n):
        """C-79 world: counted access aggregates of the n^3 barrier-record block --
           IFACE = 6n^2, CAP_d1 = n^3-(n-2)^3 = 6n^2-12n+8 (the C-82 per-epoch law),
           CAP_total = n^3, with IFACE^3 == 216*CAP_total^2 (LANE_T42_C_BOUNDCAP world
           tier / LANE_T42_D_DERIVE, sealed)."""
        import geometry as GE
        return GE.world_counts(n)

    def mutual_interface(self, L, s, g):
        """C-80: mutual interface I(A:B) of two s x s blocks at separation g -- zero
           identically when separated, seam law I_IR = 2(s-2) at single contact
           (LANE_O54_A_CORNER, sealed)."""
        import geometry as GE
        return GE.two_region_blocks(L, s, g)

    def winding_interface(self, L, w, r0):
        """C-80: the non-contractible pair's exact constant w at every distance
           (LANE_O54_A_CORNER control (ii), sealed)."""
        import geometry as GE
        return GE.winding_pair(L, w, r0)

    def coupling_cost(self, Lx, Ly, u, v):
        """C-80: the coupling-writer law w_min = d_gen between two hole records,
           exhaustive coset scan (LANE_O54_C_ATTEMPT, sealed; defect construction
           Bravyi-Kitaev)."""
        import geometry as GE
        return GE.coupling_cost(Lx, Ly, u, v)

    def certifiability(self, L, s):
        """C-81: the certify/write ledger of the s x s block -- CERT computed two sealed
           routes and equal to the cut-rank law 8s-10; WRITE0 = 0, the locality theorem
           (LANE_T43_A_CORNER, sealed)."""
        import geometry as GE
        return GE.certifiability(L, s)

    def cert_window(self, n, W):
        """C-83: CERT_W(n) = min(n^3, W*(6n^2-12n+8)); W=1 is C-82's per-epoch law,
           W=inf is DEF-A's immortal-record volume corner (LANE_T45_CLOCK, sealed)."""
        import geometry as GE
        return GE.cert_window(n, W)

    def formation_orientation(self):
        """C-71/C-72, orientation encoding (T-32, sealed seed 7): the accumulation table
           for DC-saturated / random / DC-free / AC-erased patterns, through the same
           configuration instrument as the FORMATION layer.  Returns
           dict[(name, N)] -> configuration dict (per_record = the CoCrPt grain moment)."""
        import geometry as GE
        return {key: self.configuration(GE.M_GRAIN, pat)
                for key, pat in GE.orientation_patterns().items()}

    def formation_occupancy(self):
        """C-71/C-72, occupancy encoding (T-34, sealed seed 11): written pages are
           one-signed for EVERY pattern (electron-only injection, mechanism-constitutive);
           the unwritten page is null within the declared +-5e/cell tolerance.  Returns
           dict(written_ratios, all_programmed, unwritten, null_within_tolerance)."""
        import geometry as GE
        pats = GE.occupancy_patterns()
        q = GE.N_E * GE.E_CHARGE
        # electron injection: each programmed cell stores -q; the sign was open in design
        # space and is fixed once per device by the write (the lane's premise, kept)
        ratios = [self.configuration(q, -p)['ratio'] for p in pats['written']
                  if p.sum() > 0]
        allp = self.configuration(q, -pats['all_programmed'])
        unw = self.configuration(GE.E_CHARGE, pats['unwritten_e'])
        tol = pats['tol_e'] * GE.E_CHARGE
        return dict(written_ratios=ratios, all_programmed=allp, unwritten=unw,
                    tolerance=tol, null_within_tolerance=bool(abs(unw['sum']) <= tol))

    # ---------------------------------------------------------------- ARROW (T-54/T-55; F-17..F-21)
    # Every method below delegates to model/arrow.py -- machinery ported from the sealed
    # arrow lanes or delegated to record_model, per that module's header.
    def arrow_threshold(self, lam=0.8, weights=(1, 2), coupling=None):
        """F-17: THE ARROW CARRIES THE RECORD'S OWN THRESHOLD.  chi(O:B) swept over every
           observable of each listed weight in the mean-force state under the weight-d
           coupling -- sealed: 0.00000000 on all 24 weight-1 observables, 0.11448276 at
           weight 2 = d, closed form from Z_B(+-1) exact (LANE_F1_ARROW part 4, sealed).
           Owner: ORIGINAL.  Scope: SINGLE-CARRIER, toric-2x2 (sealed T-9 audit)."""
        import arrow as AW
        return AW.arrow_threshold(lam=lam, weights=weights, coupling=coupling)

    def arrow_ledger(self, lam=0.8):
        """F-18: THE RECORD'S ARROW IS NOT AMBIENT DECOHERENCE.  The four-row coupling
           ledger (weight, I(S:B), chi(record:B)) -- sealed: the weight-1 coupling entangles
           I(S:B) = 0.04549256 yet transfers ZERO record bits (LANE_F1_ARROW/f1b part (c),
           sealed).  Owner: ORIGINAL.  Scope: SINGLE-CARRIER."""
        import arrow as AW
        return AW.arrow_ledger(lam=lam)

    def arrow_invariance(self, n_unitaries=12, seed=5, lam=0.8):
        """F-19: IRREVERSIBILITY FROM INSIDE.  System-only unitaries cannot reduce I(S:B)
           (sealed 3.686e-14 over 12 unitaries; covariance check passes; chi about the FIXED
           label moves 1.145e-01) -- the copy is relocatable, never erasable, from inside
           (LANE_F1_ARROW/f1b parts (a,b), sealed).  Owner: BORROWED (textbook invariance);
           the relative-arrow reading for records ours (T-III.6)."""
        import arrow as AW
        return AW.arrow_invariance(n_unitaries=n_unitaries, seed=seed, lam=lam)

    def arrow_history(self, times, coupling=None, lam=0.8, env=None, keep_states=()):
        """The arrow as a HISTORY (F-20-adjacent): chi(record:B)(t) from a product state
           with <record> exactly conserved -- the record is READ, not written; negative
           times are the sealed reversal control (LANE_PF2_DYNAMICAL, sealed; one
           eigendecomposition serves every time).  RecordModel.formation is the single-time
           twin (validate_formation.py).  Owner: ASSEMBLED.  F-20's mechanism TWO-CARRIER
           (toric-2x2; bouquet); this venue toric."""
        import arrow as AW
        return AW.arrow_history(times, coupling=coupling, lam=lam, env=env,
                                keep_states=keep_states)

    def arrow_redundancy(self, coupling=None, lam=0.8, t=4.0, env=None):
        """F-21: REDUNDANCY CARRIES THE RECORD'S THRESHOLD.  Whole-bath and per-fragment
           chi through RecordModel.redundancy -- sealed: fragments 0.789366/0.048377/
           0.678602 under the weight-d coupling, EXACTLY ZERO under weight-1
           (LANE_PF2_DYNAMICAL parts 3-4, sealed).  Owner: ASSEMBLED (quantum-Darwinism-
           style apparatus, Zurek/Blume-Kohout; the threshold-in-fragments finding ours).
           Scope: fragment bits SINGLE-CARRIER toric-only -- the T-9 battery replicated
           only the whole-bath weight-1 null on [[8,1,2]]/[[4,2,2]]."""
        import arrow as AW
        return AW.arrow_redundancy(coupling=coupling, lam=lam, t=t, env=env)

    def arrow_observation(self, env, coupling, record=None, model=None, lam=0.8, t=4.0,
                          tier="world", provenance=None):
        """OBSERVATION ENTRY for the arrow family (T-54/T-55): score a NEW bath/fragment
           observation through the family's own instruments -- I(S:B), whole-bath chi,
           per-fragment chi, and the verdicts (holds_record_bits, entangled_without_record
           = the F-18 class, redundant_fragments).  A custom RecordModel must bring its own
           explicit record; the toric default is used only with the default model.  D-25 AT
           THE GATE: world-tier baths require provenance; corner baths must self-declare
           'DEF-A'.  Every outcome registers -- entangled-without-record is a RESULT, not
           a failure."""
        import arrow as AW
        return AW.score_bath_observation(env, coupling, record=record, model=model, lam=lam,
                                         t=t, tier=tier, provenance=provenance)

    # ---------------------------------------------------------------- COUNT LAW (T-54; C-86)
    # Delegates to model/countlaw.py -- machinery ported from LANE_T47_A_WIDTH and
    # LANE_T47_B_STAIRCASE (sealed), registered via LANE_T47_D_REGISTER. The corner law
    # k = min_E v2(m_E) remains homed at model/count_law.py (C-14), referenced not duplicated.
    def census(self, surfaces, t_m):
        """C-86: THE SURVIVING-RECORD COUNT LAW k(t_m) -- the URM's wholly-owned
           falsifiable census (LANE_T47_A_WIDTH sec. 6, LANE_T47_B_STAIRCASE secs.
           C/D/G, sealed; registered via LANE_T47_D_REGISTER).  surfaces: a LIST of
           RecordSurface objects, world-tier ones built through URM.surface() so D-25
           provenance rides on every row; t_m: the retention spec in s.  Counts a
           record only while BOTH its values are durable -- clause (ii') on the
           record's OWN Liouvillian mode, |lambda_record| <= 1/t_m -- so each record
           dies at its SHALLOWER value's escape, at the parameter-free drop time
           t*_i = f0^-1 exp((B_i-dE_i)/kT)/(1+e^{-dE_i/kT}).  Returns k by the
           instrument AND k_formula by the derived width delta_pop(t_m) =
           kT ln(expm1(B/kT - ln f0 t_m)) so the agreement is CHECKED, never assumed;
           plus the dated drop schedule, delta_coh = hbar/t_m, the departure term
           sum_over_dead tanh(dE_i/2kT) (remanence persists while records die), and
           the declined list (non-thermal surfaces are declared, never silently
           counted).  THE SIGNATURE IS THE C-76 GATE: (surfaces, t_m) and nothing
           else -- no width, tolerance, or clustering parameter exists on this path;
           checks_countlaw.py gates the unreachability.  Owners per C-86 (ownership
           PARTIAL): Neel/Street-Woolley/Sharrock own the activation window as a
           remanence-decay device; Charap-Lu-He and Weller-Moser the dE = 0 corner;
           Preisach-Neel rate-level asymmetry; ours the derived width, the two-face
           unification, the margin-free integer census, the departure term."""
        import countlaw as CLW
        return CLW.census(surfaces, t_m)

    def count_widths(self, s, t_m):
        """C-86: both faces of clause (ii') on one RecordSurface at one retention
           spec -- delta_pop from the record's own constants (B = E_b + dE, the exact
           convention map; None when t_m is beyond the symmetric bound exp(B/kT)/(2 f0),
           which IS the no-crossing condition), delta_coh = hbar/t_m, and the record's
           own instrument drop time beside its closed form (the check, never the
           source).  LANE_T47_A_WIDTH, sealed."""
        import countlaw as CLW
        B = s.E_b + s.dE
        return dict(delta_pop=CLW.delta_pop(B, s.T, s.f0, t_m),
                    delta_coh=CLW.delta_coh(t_m),
                    t_star=CLW.drop_time(s),
                    t_star_formula=CLW.drop_time_formula(s))

    # ---------------------------------------------------------------- CLASSES (T-54; C-87/C-90)
    # Every method below delegates to model/classes.py, where the sealed-lane machinery
    # lives (exact ints/Fractions on the measurement path; certified tails; computed
    # booleans -- ported, not reimplemented).  Each docstring names its claim row, sealed
    # source, and owners.
    def coupling_venue(self, name, adj, provenance=None, tier="world", sector=None):
        """C-87 observation entry: a NEW venue graph (a record surface's access geometry)
           enters as an adjacency structure through the D-25 provenance gate -- world tier
           REFUSED without a pinned source, corner tier must self-declare 'DEF-A'
           (LANE_T44_B_WORLD S0 / LANE_T44_A_CORNER S0, sealed).  adj: list over nodes of
           [(neighbor, multiplicity), ...]; the gate also refuses empty adjacency,
           non-integer/out-of-range neighbor indices, and multiplicities that are not
           strictly positive integers.  sector optionally declares the venue limit
           ('Z3'/'Z2'/'Z1') for the evidence instruments."""
        import classes as CC
        return CC.venue(name, adj, provenance=provenance, tier=tier, sector=sector)

    def world_coupling_venue(self, n):
        """C-90: the world venue (earned D=3) -- the n^3 census-grain torus with the PINNED
           provenance (GR1 grains, face adjacency, T42_C/T43_B lineage; one walk step = one
           grain-boundary crossing = one unit of writer weight, the Gamma price C-80/O-54).
           Returns (VenueGraph, cells, idx).  (LANE_T44_B_WORLD S0, sealed.)"""
        import classes as CC
        return CC.world_venue(n)

    def corner_coupling_venue(self, Lx, Ly):
        """C-87: the corner venue (earned D=2) -- the dual lattice of the model's OWN ported
           carrier: plaquettes of geometry.Torus adjacent iff their supports share a carrier
           edge, computed from the plaquette masks alone, multiplicity kept; DEF-A
           self-declared.  (LANE_T44_A_CORNER/t44a_lib.py plaquette_adjacency,
           verbatim-in-substance; sealed row sums exactly 4 on (4,6) and (3,7).)"""
        import classes as CC
        return CC.corner_venue(Lx, Ly)

    def chain_coupling_venue(self, L):
        """C-87: the D=1 control venue (cycle C_L, DEF-A).  (t44a_lib.py cycle_adjacency,
           verbatim; sealed: row sums exactly 2, mu_c = 1/2 the venue's own.)"""
        import classes as CC
        return CC.chain_venue(L)

    def critical_price(self, venue):
        """C-87/C-90: the venue's OWN critical coupling price mu_c, LOCATED by computation,
           never a literal (D-8): Perron row-sum candidate 1/deg, (I - mu_c A) annihilates
           the constant vector, exact-rational resolvent SINGULAR at mu_c (the D-15 zero)
           and SOLVABLE at mu_c*(19/20), mu_c*(21/20) beside it (the positive controls; on
           the sealed deg-6 venue these are exactly the sealed 19/120 and 7/40).  Sealed
           values: 1/6 world D=3, 1/4 corner D=2, 1/2 chain D=1.  DECLINES on a venue that
           is not degree-regular.  Owners: Perron-Frobenius/Gershgorin standard.
           (LANE_T44_B_WORLD S0/S2; LANE_T44_A_CORNER S2, sealed.)"""
        import classes as CC
        return CC.mu_c_of(venue)

    def reachable_class(self, venue, mu, evidence=False):
        """C-87: THE REACHABLE-CLASS VERDICT -- the computed boolean triple (exponential,
           critical, divergent) for a declared coupling price mu, by exact rational
           comparison against the venue's own computed mu_c; exactly one True whenever mu_c
           is located.  evidence=True additionally runs the class's own instrument on the
           declared sector: subcritical booleans (ratios <= 1 - 1/20, Cauchy, power
           exclusion), the critical 1/d kernel signature (INV window, deepening-stabilized),
           or the divergence witness.  A price must be nonnegative; negative mu is refused
           before any verdict or evidence is emitted.  (LANE_T44_B_WORLD taxonomy +
           S2/S3/S4, sealed.)"""
        import classes as CC
        return CC.class_verdict(venue, mu, evidence=evidence)

    def coupling(self, mu, target, K):
        """C-87 class (1): the Gamma-priced coupling G_mu(d) = sum over admissible strings
           of mu^weight on the D=3 sector -- exact partial sum (Fraction) with the exact
           geometric tail (6mu)^{K+1}/(1-6mu); leading term N_min mu^d with w_min = d the
           confinement cost (C-80/O-54 standing).  Owners: walk generating functions,
           Spitzer/Lawler; comparison tier only.  Negative mu is refused rather than
           producing a signed 'tail bound'.  (t44b_lib.py series_3d, verbatim.)"""
        import classes as CC
        return CC.series_3d(mu, target, K)

    def critical_kernel(self, targets, M):
        """C-90: the regularized critical kernel a_M(x) = sum (N_2m(0)-N_2m(x))/36^m at the
           COMPUTED mu_c = 1/6, exact rationals, with certified tails beside it
           (classes.diff_tail_bound / abs_tail_bound; honest for M >~ 1000).  The D=3
           critical member is the 1/d POWER LAW: the sealed M=1400 exponent bracket contains
           1; separately, the M=2800 coefficient bracket [0.476369, 0.487321] contains owner
           3/(2 pi) (comparison).  See the fixed-distance caveat below.  Owners: Polya
           1921 transience, Watson 1939 G(0), Spitzer P26.1 coefficient -- comparisons only.
           (LANE_T44_B_WORLD S4 + register row C-90, sealed.)"""
        import classes as CC
        return CC.crit_kernel_3d(targets, M)

    def class_discriminator(self, K2=6000, K1=80000):
        """C-87: the cross-dimension discriminator -- ONE instrument (doubling-increment
           ratios of the regularized critical kernel), three venues, three pairwise-DISJOINT
           declared windows: D=1 LINEAR [9/5,11/5], D=2 LOG [4/5,5/4], D=3 INV [2/5,3/5].
           The critical class is the earned dimension's own; mu = 1/6 is critical on D=3 and
           subcritical on D=2.  (LANE_T44_B_WORLD S5, sealed.)"""
        import classes as CC
        return CC.discriminator(K2=K2, K1=K1)

    # ---------------------------------------------------------------- WRITING (T-54/T-55; C-91)
    # Every method below delegates to model/writing.py, where the sealed-lane machinery
    # lives (exact Fraction kernels, venues from carrier supports, the coset instrument
    # reused from geometry.py -- ported, not reimplemented).
    def writing_kernel_verdict(self, venue, c=0):
        """C-91 kernel tier: the invariant lazy-family kernel c*I + ((1-c)/deg)*A on a
           kernel venue ('C8' | 'T3' | 'T4' | 'Z27'), with conservation (double
           stochasticity), criticality (exact det(I - K)), link amplitudes, and the
           CTRL-LEAK control beside it.  The sealed identity: conserving <=> critical,
           per-crossing amplitude 1/deg identically for every nonzero crossing share
           (LANE_T48_A_DERIVATION, sealed).  The identity endpoint c=1 is conserving and
           critical but has no crossing, so per_crossing is None.  Owners: unital channels /
           Birkhoff (re-verified on explicit operators in-lane), Perron, Gershgorin."""
        import writing as WW
        from fractions import Fraction as Fr
        try:
            c = Fr(c)
        except (TypeError, ValueError, ZeroDivisionError) as exc:
            raise ValueError("writing_kernel_verdict requires a rational 0 <= c <= 1") from exc
        if c < 0 or c > 1:
            raise ValueError("writing_kernel_verdict requires 0 <= c <= 1")
        adj = {"C8": WW.ring_venue(8)["adj"], "T3": WW.plaquette_venue(3)["adj"],
               "T4": WW.plaquette_venue(4)["adj"], "Z27": WW.grain_venue(3)["adj"]}[venue]
        K = WW.kernel_uniform(adj, c)
        deg = WW.venue_degree(adj)
        conserving = WW.is_doubly_stochastic(K)
        return dict(deg=deg, conserving=conserving,
                    critical=bool(conserving and WW.crit_det(K) == 0),
                    link_amplitudes=WW.link_amplitudes(adj, K),
                    per_crossing=(Fr(1, deg) if c < 1 else None),
                    leak_det=WW.crit_det(WW.leak_kernel(adj, Fr(9, 10))))

    def writing_uniformity(self, Lx, Ly):
        """C-91 corner tier: uniformity EARNED from the writer algebra on the (Lx, Ly)
           plaquette venue rebuilt from carrier supports -- the elementary writer's
           invariant tuple on every link, mu_c located in-lane (Perron row sums + exact
           resolvent singular at 1/deg, nonsingular beside), and the unique conserving
           member t* = 1/deg = mu_c (LANE_T48_B_CORNER, sealed at (4,6), (3,7), (5,5)).
           Owners: carrier Kitaev quant-ph/9707021; coset instrument o54c lineage
           (geometry.py); Perron/Gershgorin/Feller as in-lane."""
        import writing as WW
        from fractions import Fraction as Fr
        cv = WW.corner_venue(Lx, Ly)
        inv = WW.writer_invariants(cv)
        return dict(invariant_tuple=inv[0], identical=all(v == inv[0] for v in inv),
                    n_links=len(inv),
                    mu_c=WW.mu_c_locate(cv["rows"], 0, beside=(Fr(1, 8), Fr(23, 100))),
                    conserving_member=WW.conserving_member(cv["rows"]))

    def writing_transport(self, n, a):
        """C-91 world tier, E1 TRANSPORT (iv' literal): the energy-conserving writer on the
           n^3 census venue at per-attempt amplitude a -- conserving AND critical
           (mu = 1/deg = mu_c) at EVERY dE and barrier; verdicts computed, never narrated
           after enforcing the probability domain 0 <= a <= 1/deg (invalid rows refuse);
           (LANE_T48_C_WORLD V1, sealed).  Owners: Stinespring (why row sums 1 is the
           dilation's structural property; the sums themselves computed)."""
        import writing as WW
        _c, _i, nbr = WW.torus3(n)
        return WW.transport_verdict(nbr, WW.ensemble_transport(nbr, a))

    def writing_trail_retreat(self, n, u, b):
        """C-91 world tier, E2 TRAIL WITH RETREAT: the raw two-rate writer with
           backtracking kept -- conserving at every dE, uniform (1/deg) exactly at dE = 0,
           split (b, 1)/(5b + 1) beside.  The constructor computes deg from the venue and
           refuses u < 0, b < 0, or (deg-1)*u*b + u > 1 before a verdict is formed
           (LANE_T48_C_WORLD V2, sealed).  Owners: Goldstein 1951 / Kac 1974 named for
           the persistence remark, comparison-only."""
        import writing as WW
        _c, _i, nbr = WW.torus3(n)
        return WW.retreat_verdict(nbr, WW.ensemble_trail_retreat(nbr, u, b))

    def writing_trail_decay(self, n, u, b, counting="H1"):
        """C-91 world tier, E3 TRAIL WITH DECAY (the model's own erase channel): NEVER
           critical -- mu = b/(deg*b + 1), f0 and E_b dropping out exactly; the COMPUTED
           mass ratio mu_c/mu is returned; the closed form ln(1 + e^{dE/kT}/l) is checked
           against it by the validator, never sourced from it (LANE_T48_C_WORLD V3/V4,
           sealed; the DONE_WHEN control).  counting='NB' uses the venue's own
           directed-edge criticality reference (Hashimoto 1989, earned by row sums).
           Both counting rules refuse negative or overfull probability rows; any other
           counting label is refused rather than silently treated as NB."""
        import writing as WW
        _c, _i, nbr = WW.torus3(n)
        W = WW.ensemble_trail_decay(nbr, u, b, counting)
        return (WW.decay_verdict(nbr, W) if counting == "H1"
                else WW.decay_verdict_nb(nbr, W))

    def writing_gap(self, s, n=4, den=10 ** 9):
        """C-91 + D-25, THE OBSERVATION ENTRY: a real record surface's written-trail mass
           gap.  REFUSES without provenance (build s through URM.surface); declines
           non-thermal surfaces and dials whose exponential underflows or whose declared
           rational denominator cannot resolve a positive lower bound.  Otherwise the
           surface's b = exp(-dE/kT) is bracketed by exact rationals, the E3 kernel is
           built and measured exactly at both brackets (u independence re-computed at
           entry), the closed form is checked against every computed ratio, and the float
           gap is certified INSIDE the computed bracket."""
        import writing as WW
        return WW.surface_gap(s, n=n, den=den)

    # ---------------------------------------------------------------- ROLES (honestly scoped)
    def roles(self):
        return {
            "EM": "world-tier EM is a physically instantiated write/hold/read mechanism in declared "
                  "record packets, not a universally proved substrate of every record. A conserved "
                  "current reaches Maxwell response only under the separate MCR action, gauge, "
                  "boundary, and Ward packet; compact U(1) emergence remains open.",
            "GAMMA": "For the first qualified positive-margin binary record, complete-query "
                     "squared-fidelity gamma_Q obeys D_TV>=B_rec>0 => gamma_Q<=1-B_rec^2<1, "
                     "so I_gamma=-log(gamma_Q)>0: the gamma-information seed is present at "
                     "record formation, but is not microscopic classical gravity. State-family "
                     "gamma_state supplies an exact rank-three QFI coframe candidate. At the "
                     "isotropic S_4 point, GSGB's s_gamma=ell_F^2 f P matches EO's "
                     "q_EO=(4a^2/3)P under ell_F^2 f=4a^2/3. Equivalently, ET's "
                     "Bures-line q_gamma=(ell_B^2 f/4)P requires ell_B^2 f=16a^2/3, "
                     "with ell_B=2 ell_F; away from isotropy an explicit tetrad/null "
                     "binding is required. The "
                     "restrictive same-parent Gaussian influence gamma_IF + complete-control + "
                     "known-temperature KMS + causal/contact packet reconstructs a dressed "
                     "retarded response. The three gamma objects require a separate common "
                     "read/dilation theorem before identification. Generic gamma is not a force "
                     "and determines neither time orientation nor curvature. With the separately "
                     "supplied ER routing law, the same retained record can control exact common "
                     "two-probe Lorentz holonomy. Because that routing is supplied, this is an "
                     "intermediate witness, not the final same-world theorem; global same-sector "
                     "ancestry and physical soldering remain open.",
            "ALPHA": "Alpha is constitutive domain identity. SAI/AWAI establishes the domain "
                     "alpha requirement. Independent measurement fixes alpha at chi_0 for the "
                     "governing domain. For any "
                     "record r, ACTVIS(r,W_obs) together with SAI1--SAI8 implies "
                     "alpha_r(chi)=T_{chi<-chi_0}[alpha_obs(chi_0)]. ACTVIS independently "
                     "establishes ancestry to the governing domain. "
                     "Thus an ACTVIS record cannot choose a private record- or region-level alpha; "
                     "an aligned inequivalent value falsifies its same-sector assignment or at "
                     "least one SAI premise. Bare REC, DCL_phys, and URFT establish neither "
                     "ACTVIS nor governing-domain ancestry. ALLOW: the declared ideal packet admits "
                     "the exact construction-scoped interval I_chi intersect "
                     "((-ln(1-delta))/(4*pi*B^2), infinity), with every positive alpha in I_chi "
                     "admitted at zero relevance floor. This is not a complete-universe interval, "
                     "and its 0.50 cavity read contrast is not the GFT majority Gate. REQUIRE: "
                     "every ACTVIS record in the governing domain inherits the domain-matched alpha "
                     "trajectory; changing alpha defines a different domain structure. SELECT: "
                     "governing-domain selection is a "
                     "separate proposition and may not exist; complete-universe singleton REQUIRE "
                     "also remains open. AWAI proves the domain alpha requirement and supplies "
                     "neither gravity nor G.",
            "GRAVITY": "Classical gravity is not placed on the microscopic record surface; the first "
                       "qualified positive-margin binary record already carries the nonzero "
                       "gamma-information seed described above. In the declared "
                       "F3-QIRN successor calculations, retained-record loading can carry the exact U_d "
                       "cycle sector through 4 U_d chi_0^R(0)=1 into open classical degree plateaus. "
                       "An exact finite custody-handoff model forms derivative pair memory, composes finite "
                       "serial paths and a symmetric equal-depth branch/rejoin cycle, and supplies extensive "
                       "reversible active/quarantine BREAK; on serial support the same interaction has an "
                       "exact open one-dimensional TFIM phase for U_d>2h. On independently earned bipartite "
                       "support, degree lock is an exact discrete Gauss sector and the existing link flip "
                       "derives alternating-cycle ring dynamics. On supplied z=4,d*=2 diamond ice, the exact "
                       "leading F3 Hamiltonian reaches the published pure-kinetic U(1) liquid; independently, "
                       "the actual hard-core carrier makes every fixed even cubic torus a local two-switch "
                       "free-energy basin in an open controlled regime, while the saturated carrier makes "
                       "periodic diamond a saddle. On supplied cubic eligibility, d*=3 is exactly the "
                       "zero-charge spin-half U(1) quantum-link sector. Formed pair memory can lawfully gate "
                       "that successor field, but unchanged BS09 hopping follows occupied G_n rather than the "
                       "full degree-six eligibility graph, so the saturated carrier margin is not additive and "
                       "no direct K_e T_e law is installed. One joint trace has a nonzero carrier-incidence "
                       "backresponse, and its complete h^2 Y^2 dressing gives carrier density and hopping "
                       "response rather than symmetric-detuning electric stiffness. The exact full thermal square has open "
                       "positive and negative response regions and multiple tuned crossings, so beta U_d=1 is not universal. "
                       "Exact physical shared-edge composition preserves both one-cell anchor signs; its sector-correct "
                       "global gluing contrast and a distinct same-six-site pinned-ensemble Mobius finite difference are "
                       "nonzero and sign-changing. This remains a two-cell, one-carrier dilute result, and the pinning "
                       "controller/work is not yet physically completed. "
                       "The unchanged qutrit law already supplies the fixed-content hard-core two-carrier sector, with "
                       "(J_e^psi)^2=q_u+q_v-2q_uq_v. Its exact 1920-state trace proves that finite signs depend on collision "
                       "algebra and number preparation; the allowed global rule N_m=m is not a selected fixed-density phase "
                       "or a full-content trace. The exact fixed-width transfer limit proves that the matched canonical "
                       "and grand intensive responses agree but remain analytic at finite temperature, so a strip zero is "
                       "a crossover rather than a phase transition. On a supplied two-dimensional square sheet, the unchanged "
                       "incidence trace is exactly a record-occupation-dependent Ising interaction and one witness straddles "
                       "its thermodynamic critical surface. A second exact theorem restores positive degree lock and proves "
                       "open blank-boundary-disordered/occupied-carrier-ordered regions at a BS13-stable witness. A typed "
                       "volume-wise composition routes actual FPMH derivative records into active storage or retained "
                       "quarantine and switches those carrier responses while conserving total formed-relation occupation "
                       "across KEEP/BREAK. This is conditional formation-to-phase causation through active occupation, not "
                       "a history-only effect at matched active state. A fixed-separate-marginal controller construction "
                       "is rejected as record causation because its decoder cancels record ancestry end to end. A distinct "
                       "pair-rebinding circuit changes the phase through active joint correlation while complete separate "
                       "fields, sharp counts, spectra, and mutual information remain matched. Heterogeneous accumulation "
                       "is controlled by contour/path topology rather than scalar density: equal-density placements have "
                       "different exact responses. FPMH composition fixes 32 formation episodes, eight active authenticated "
                       "records, and 24 quarantined formed excitations while retaining that response difference. F3 reads "
                       "the active pattern rather than provenance, and the route topology is supplied. The reciprocal audit "
                       "proves that the sealed h=t=0 hold has zero retarded carrier-to-incidence and carrier-to-pair-memory "
                       "response. Restoring the inherited BS06 flip gives an exact finite carrier-conditioned Rabi channel, "
                       "but no common-background collective limit is earned and fixed-time local response is O(N^-2). "
                       "The minimal incidence degree defect acquires "
                       "second-order line-graph hopping but fails the isolated finite-residue pole gate because a flat cycle "
                       "fiber touches the dispersive band and the degree residue vanishes; inherited flip scaling also gives "
                       "vanishing thermodynamic bandwidth. These results do not yet supply autonomous support, nonzero-dynamics "
                       "phase persistence, a common metric, or gravity. "
                       "A lawful joint endpoint trace also has an exact open conditional ALLOW-side bias without K_e T_e, "
                       "but physical sector access and matched occupied-n switching remain open. Qualified retained occupation changes virtual "
                       "degree-defect denominators and therefore produces an exact record-patterned electric "
                       "potential and plaquette stiffness without a geometry reward. If one collective phase "
                       "carries paired electric and magnetic stiffnesses to the same IR scale, they determine "
                       "an optical cone and coupling and can carry sectoral tidal curvature. Maxwell conformal "
                       "invariance still leaves the spatial-volume factor needed for nonzero static G00 "
                       "unresolved in the U(1) sector alone. A calibrated same-parent massive probe would fix "
                       "N=omega0/mu and A=omega0/(mu c), but without an earned proper mass, clock, residue, or "
                       "cell scale an exact compensator leaves that volume unidentifiable for one uncontrolled "
                       "probe. Several fixed-mass probes provide an exact scale-free alternative: a common static "
                       "metric exists exactly when their cone identities agree and their coordinate-gap ratios "
                       "are spatially constant. Those conditions determine the N,A profiles and coordinate G00 "
                       "up to one global scale; a varying gap ratio falsifies common fixed-mass geometry. Current "
                       "F3 has not yet earned the required independently resolved continuum species. Its two bare content "
                       "labels give duplicate rank-one carrier rows, while its storage qutrits do not propagate between "
                       "vertices. The minimal bare incidence degree-defect candidate has failed the stable-pole gate "
                       "at its first controlled hopping order. Exact screening of its already-present carrier-dressed "
                       "one-hole continuation permits static dressing or binding but proves an isolation-bandwidth "
                       "dichotomy: exact-complement touching cannot create a uniform gap, while a uniformly isolated "
                       "continuation has bandwidth O(N^-1) under inherited h_N=Omega/N. Finite-density, controlled "
                       "gap-closing/double-scaling, and higher-sector routes remain open. The exact finite-density boundary "
                       "has an O(1) channel only with macroscopic Johnson coherence: authenticated classical word accumulation "
                       "and the conditioned dressed Gibbs state have c_J=0 and O(N^-1) escape curvature. Separately, the "
                       "earned Q_uv^auth is a partial set-valued authenticated custody field: declared support is symmetric, "
                       "writer provenance directed, and untested pairs are undefined rather than zero. Explicit common-parent "
                       "products realize every supplied finite graph, so URFT/FPMH alone entails no sparsity, dimension, or "
                       "locality. Its exact common-generator kappa_(v<-u) seminorm distinguishes a direct generator block from "
                       "two-step-only influence. The unchanged one-pair FPMH/PESC composition passes it exactly: "
                       "kappa_KEEP(v<-u)=kappa_KEEP(u<-v)=abs(t_psi)/hbar, while both matched BREAK blocks vanish under the "
                       "same complete Hamiltonian. On one complete finite declared census, this composition gives "
                       "kappa_(v<-u)=abs(t_psi) S_uv^auth/hbar in both directions on every pair, so direct influence support "
                       "is exactly active authenticated support. The fixed-number finite-time signal equals the carrier transition "
                       "amplitude and obeys separate factorial and Lieb--Robinson-type graph-distance bounds conditional on a supplied "
                       "maximum degree. This earns a supplied-network relational propagation cone without K_eT_e; endpoint reciprocity "
                       "is not carrier-to-record back-reaction. In the complete existing post-formation source-off parent, the full "
                       "authenticated support projector S_e=F_e Z_e^KEEP P_e^K commutes with the Hamiltonian, so every support-word "
                       "probability is frozen for arbitrary complete states. This proves passive graph retention but closes autonomous "
                       "or corrective selection of the authenticated graph by existing source-off terms; successor incidence may still "
                       "evolve inside fixed authenticated eligibility. The exact K_(6,6), degree-three hostile screen proves finite "
                       "component-merger and fragment access, but the completed known one-carrier diagonal response gives the fragmented "
                       "2K_(3,3) graph strictly lower fixed-graph free energy at finite temperature. Physical zero-temperature band bottoms "
                       "tie, and graph entropy is separate. The exact carrier-dressed h^4Y switch coefficient cancels at symmetric "
                       "detuning; in the controlled detuned domain its correction is below 3/16 per labeled switch and 1/48 on the "
                       "normalized merger block, so it cannot reverse the pure switch. The reciprocal Hermitian amplitude is not merger "
                       "tension. The exact all-orders-in-carrier diagonal response at O(h^2) is a Sylvester/Liouville inverse. In the "
                       "finite K_(6,6) witness its relative fragment/connected sign changes with temperature, while proper cold degenerate "
                       "perturbation returns to fragment preference. It is real feedback, not a universal connector. The exact dense-eligibility "
                       "count is exp[d n log n+O(n)], whereas a prospectively fixed finite-complexity local family has rank at most "
                       "exp[2n log n+O(n)]. Under the explicit endpoint-extensive width premise osc(H_n)<=w n, its fixed-temperature Gibbs "
                       "weight vanishes for d>=3 even with off-diagonal graph dynamics. This is not yet a full-parent verdict: dense eligibility "
                       "has n^2 physical relation resources, fixed switch amplitude can have Theta(n^2) width, and enlarged record/factor/event "
                       "locality is a separate representation. Counting active pair tokens as factor vertices gives average degree below four "
                       "but does not cure hubs: complete endpoint projection has maximum degree N-1 and radius-three saturation. The present "
                       "carrier law propagates directly on that endpoint projection; the record token is a preparation ancestor, not an "
                       "intermediate site. Existing URFT/FPMH does not imply a uniform active endpoint capacity. The explicit missing "
                       "UCAIC_sigma(B) premise assigns every simultaneous active relation distinct named endpoint ports until BREAK/deactivation "
                       "and forbids a direct bypass. Conditional on it, Delta(K)<=B, M<=BN/2, fixed-size cell embeddings are O(N), and the DV "
                       "cone constant is size independent. UCAIC is not derived or adopted and selects no connectedness or dimension. The strongest "
                       "finite-dimensional capacity route is now exact: a full Cartesian m-bit code in one D-dimensional endpoint-accessible carrier "
                       "requires 2^m<=D under perfect whole-word decoding, while jointly randomized bit reads obey sum_i[1-h_2(p_i)]<=log_2D, with "
                       "jointly stable averaged RMR/gamma corollaries. Parity, central fanout, external edge memories, and shared buses prove that ordinary "
                       "per-context RMR/gamma and finite endpoint dimension do not derive episode-faithful ownership, persistence, uniform accessible "
                       "dimension, or no bypass. History-wise phase inheritance is exact once one complete physical formation instrument is branchwise "
                       "closed on a prospectively fixed realized phase Phi: finite induction covers every nonterminal active/reject/quarantine successor "
                       "without selecting an outcome, while terminal outcomes end their histories. K_j is the complete typed phase state, A_j its "
                       "authenticated support word, and G_j its simple active endpoint projection; EB bounds G_j, DW freezes A_j and G_j between writer "
                       "windows, and DV supplies the controlled simple one-episode cone. Snapshot control alone does not derive the update law: alternating "
                       "bounded supports, monotone binary-tree growth, and four-cell cacti are exact countermodels. The isolated candidate is a recursive "
                       "same-parent writer law with phase-local writers, complete grammar closure, and bypass rejection/quarantine; it is not derived by "
                       "current FPMH. The complete "
                       "dense-parent ledger now proves O(n) width for the exact degree-locked compression under explicit bounded edge/bulk/port "
                       "premises, an intensive one-toggle boundary for h_n=Omega/n, O(1) exact-Y second-order width under a uniform Sylvester gap, "
                       "and O(n^-2) leading switch width, but no all-orders effective-width theorem. The full soft degree penalty has Theta(n^3) "
                       "width. On the clean classical symmetric slice, Z1/Zd=n^2 exp(-2 beta U_d), and every fixed finite-maximum-degree family has "
                       "weight at most exp[-n log n+O(n)] at fixed finite temperature and fixed couplings. Thus fixed soft degree preference does not "
                       "thermally produce finite valence on that slice; hard capacity, formation-time rank reduction, growing scales, zero-temperature "
                       "control, and nonequilibrium protection remain escapes, and the claim is not exported to the nonzero carrier/current/port parent. "
                       "Conditional UCAIC plus a connected attaching lineage of bounded authenticated cells gives connected endpoint/cell-dual graphs "
                       "and a linear cell census, but a diamondized trivalent tree satisfies those conditions while its balls grow as 9*2^k-8. The exact "
                       "sufficient missing law is a physically counted all-ball frontier bound |partial B|<=A|B|^(1-1/D); conditionally it gives "
                       "|B(v,r)|<=(1+Ar/D)^D and excludes uniform expanders. A,D are supplied frontier data, not a derived dimension; physical "
                       "front collision, coalescence, or sealing remains to be derived or falsified from the formation/work/port ledger. "
                       "One exact conditional mechanism now reaches that frontier law: complete future-equivalent AB/BA event-front coalescence, "
                       "plus an explicit authenticated class/edge/cell lift and bounded named ports, gives N_0^2 support with the uniform all-root "
                       "bound |partial B|<=8 sqrt(2)|B|^(1/2); finite count caps compose with EF, while constitutive merger BREAK restores the "
                       "binary tree and exponential growth. Current FPMH/F3 does not instantiate the complete merger observable or its drift/variance, "
                       "and the tuned cycle zero is not a front-balance law. Keeping the append arrows gives a conditional truncated operational "
                       "1+1 causal-diamond poset: t=#A+#B, x=#A-#B, reachability iff Delta t>=|Delta x| on the parity lattice, and "
                       "tau_comb^2=4(|I|-ell-1). This is not yet a physical spacetime-event census; the one-class/one-event lift, uniform event-volume "
                       "density, conformal factor, calibration, and common probes remain open. Higher-rank raw orthants are polyhedral and are not "
                       "invertibly linearly equivalent to higher-dimensional Lorentz cones. The exact OPEN-token ledger xi=G-C-2P-Q supplies a "
                       "conditional drift trichotomy, but zero drift yields only a fixed-exploration high-probability square-root bound, not history-wise "
                       "or simultaneous all-ball SAF; a branchwise seal-credit/lifetime invariant and token-to-boundary map remain required. Finally, a "
                       "turn phase genuinely tensor-local to a redundant full-word history factor, or restricted to one fixed front block, is exactly "
                       "front-invisible under partial trace and every CN-descending future. This does not cover a Q-controlled phase on CN's minimal rank "
                       "encoding, whose labels are reused across front sectors. A canonical coherent checkerboard-like construction would use a front-active "
                       "coin/conditioned shift before persistent recording; more generally, recombination must become front-active or use a fully owned "
                       "history-to-front descent break. Current F3/PESC installs no earned implementation of that join. "
                       "The exact positive complement retains every complete history as an OPEN active disposition (q,c), or an explicit terminal label, "
                       "plus a blind residual rank z. Right congruence is the recursive append gate, reference-stable Z descent prevents residual leakage, "
                       "and failure of the further CPTP C descent is exactly the condition for bounded memory to affect the scored front. For uniform "
                       "k=|C|, active RFCD layers obey F_n<=sum_i min(k,binom(n,i))<=2+k(n-1); arbitrary refined graph balls grow by at most k and degree "
                       "is at most k Delta+k-1. Last-symbol chirality gives exactly F_n=2n and cumulative count 1+R(R+1), whereas FULL-RESIDUAL BREAK "
                       "restores 2^n. This does not restore interference between orthogonally tagged histories. No displayed current-parent variable "
                       "supplies the required statistic or coin: transported content is bounded but propagation-blind, FPMH direction is provenance while "
                       "active K is undirected, and K,n are edge-indexed. "
                       "A prospective extension closes the corresponding finite propagation calculation on one supplied fixed authenticated support. "
                       "Reusing the existing qutrit occupied contents as probe chirality, but newly instantiating an onsite coin and content-conditioned "
                       "transfer, gives an exact one-carrier conditioned shift. A single complete route/SWAP unitary gives chirality KEEP versus a Q-only "
                       "C-descending BREAK with displaced content retained in garbage. Structural formation history is fixed and blind; the interfering "
                       "alternatives are unrecorded probe paths, so persistent orthogonal path records recover the incoherent EJ limit. In the padded bulk, "
                       "cos Omega(k)=cos(ka)cos(theta) and |v_g|<=a/Delta tau; scaling a/Delta tau=c and theta=mc^2 Delta tau/hbar has principal limit "
                       "H_eff=hbar c k sigma_z+mc^2 sigma_x. This proves a prospective conditional 1+1 relativistic probe architecture, not a current-parent "
                       "matter law. The coin, conditioned transfer, front embedding, coherent-before-terminal-REC schedule, physical scale, 3+1 support, "
                       "common metric, and gravity remain unearned. "
                       "A finite coin cannot repair that missing support: the principal differential rank is at most the number of independent support "
                       "characters, and internal noncommutativity does not alter the raw positive-append orthant. On a separately supplied signed "
                       "rank-three support, an exact Pauli split-step walk has an isotropic Weyl infrared principal cone and an explicitly anisotropic "
                       "ultraviolet dispersion. Four channels with Gram entries 1 and -1/3 give a coordinate-free local tetrahedral frame; exact "
                       "scalar-square isotropy is equivalent to Clifford anticommutators, and an exact nonzero Dirac mass requires internal dimension "
                       "at least four. Two independently prepared probes passing the same scoped Clifford test establish a common-cone candidate only "
                       "for those probes. Signed support, inverse channels, global gluing/holonomy, the coin, probe species, physical scale, universality, "
                       "curvature, and gravity remain unearned. "
                       "The corresponding conformal-scale bridge is exact at conditional finite 1+1 scope. If a branch-stable proper angular frequency "
                       "mu_*, an independently calibrated common null speed c_*, the EL-step/EI-layer clock lock, and an independently falsifiable "
                       "one-base-Q-cell/one-physical-cell binding are physically supplied, then Delta tau=theta/mu_*, a=c_*Delta tau, "
                       "ds^2=-c_*^2 dT^2+dX^2=-4a^2 du dv, and v_square=2a^2. Complete intervals obey "
                       "V_2=(a^2/2)tau_comb^2=2a^2(|I|-ell-1), and exact M3 refinement is the phase-square law. Without the independent frequency "
                       "standard, an exact Weyl compensator preserves RFCD order, EL phase, dimensionless momentum, and the speed ratio while scaling "
                       "metric and volume. Gamma, record counts, and order therefore do not secretly fix the physical scale. The calibration/cell "
                       "binding, physical 3+1 support, continuum, curvature, common stress response, and gravity remain unearned. "
                       "The sealed bounded q=4 stream witness supplies an explicit compatible record-front merger with exact complete-port S_4 "
                       "covariance. Conditional clock/cell calibration turns its count contrasts into the exact rank-three A_3 tetrahedral frame "
                       "and a local 3+1 Lorentz-signature simplex. Matching its isotropic EO quadratic form to the QFI coframe uses the explicit "
                       "GSGB ell_F^2 f=4a^2/3 scale/soldering premise, equivalently ET's "
                       "ell_B^2 f=16a^2/3 with ell_B=2 ell_F; it is not derived, and anisotropic matching requires an explicit "
                       "tetrad/null binding. The Boolean-cell theorem defines a common two-probe Lorentz connection, and the "
                       "ER witness proves that one qualified retained record can control nontrivial versus identity holonomy with identical signed "
                       "module inventory. This is common-connection curvature, not Levi-Civita curvature: ER fails the natural-coframe torsion "
                       "equation. GSGB therefore establishes a typed gamma-to-gravity connection lane, not a completed physical chain. The final "
                       "real-world target is one same-world derivation from qualified record to gamma seed, physical QFI/EO soldering, selected "
                       "Levi-Civita curvature under refinement, and universal stress/Einstein-Hilbert response, with neither geometry nor routing "
                       "inserted as a premise. GSGB-JOIN, "
                       "QFI-to-physical-coframe G-SOLDER, compatible torsion-free connection selection, controlled refinement, and the downstream "
                       "gravity gates remain open. "
                       "Nonlinear off-diagonal h^4Y^2/h^6Y remains open, but the active need is a scale-stable capacity/formation law. Any candidate must "
                       "reverse or bypass this adverse component tension "
                       "without inserting connectivity, then derive stable sparse connected support, degree, dimension, and distance, "
                       "an isolated finite-residue local pole, and physical thermodynamic propagation. These results "
                       "are not yet one autonomous thermodynamic gravity parent. "
                       "After one common smooth Lorentzian metric is earned, a positive "
                       "matched total Ricci coefficient, including the finite-shell contribution, "
                       "conditionally supplies the full nonlinear "
                       "leading-derivative Einstein-Hilbert action and complete-stress back-reaction; a "
                       "composite metric also requires the explicit-force and dense-tangent-span gates. "
                       "Autonomous support/phase selection, physical multi-species/common-volume realization, "
                       "the common metric, symmetric rank-two order, global same-sector ancestry, physical soldering/refinement, "
                       "the coefficient sign, the absolute scale, and observed SI G remain open.",
        }


# ---------------------------------------------------------------------- D-25: provenance registry
# The model is grounded in real record data, never the toy category (the principal, 2026-08-20).
# World-tier surfaces constructed through the URM's public gate MUST carry provenance; corner
# carriers must self-declare DEF-A. Sealed lanes predate this gate and use the raw class.
PROVENANCE = {
    "CoCrPt grain": "magnetic anisotropy; K_u ~ 2e5 J/m^3 class; stability rule K_uV/kT onset 35+/-2, "
                    "~60 for 10-yr: Weller & Moser, IEEE Trans. Magn. 35, 4423 (1999)",
    "CoCrPt HDD grain": "magnetic anisotropy; K_u ~ 2e5 J/m^3 class; stability rule K_uV/kT onset "
                        "35+/-2, ~60 for 10-yr: Weller & Moser, IEEE Trans. Magn. 35, 4423 "
                        "(1999); display-name alias of CoCrPt grain",
    "NAND floating gate": "trapped charge; detrapping E_a ~ 1.0 eV across generations; JEDEC 1-yr/30C "
                          "EOL spec (LANE_T41_EXTERNAL/CITATIONS.md)",
    "Azobenzene": "photoisomerisation; t1/2 = 1.4 d in benzene at 35 C, dH = 21.1 kcal/mol = 0.915 eV "
                  "(ACS Cent. Sci., PMC9951306)",
    "Azobenzene cis/trans": "photoisomerisation; t1/2 = 1.4 d in benzene at 35 C, dH = 21.1 "
                            "kcal/mol = 0.915 eV (ACS Cent. Sci., PMC9951306); display-name "
                            "alias of Azobenzene",
    "DNA base tautomer": "chemical bond; census GR1 values, source class: quantum-chemistry literature",
    "Fe(II) spin crossover": "spin-state transition; census GR1 values",
    "Alanine enantiomer": "parity violation; PVED ~ 1e-19..1e-17 eV literature class; instrument declines",
}


class URM(ProjectModel):
    """The public gate of the Universal Record Model.

       D-25 is enforced at both model-carrier constructors: surface() REFUSES a world-tier
       parameterization without provenance, and corner() REFUSES an exact carrier that does
       not self-declare DEF-A.  world_observation() is the distinct measurement-input door;
       passing its custody contract is necessary but is not validation of a theory.  New laws
       enter as ProjectModel layer methods plus validator gates and claim rows; new external
       numbers enter only as pinned comparisons with stated tolerance, semantics, and a power
       control."""

    @staticmethod
    def surface(name, mechanism, dE, E_b, T, f0, thermal=True, provenance=None, tier="world"):
        if tier == "corner":
            if provenance != "DEF-A":
                raise ValueError(
                    "URM REFUSES: a corner carrier must self-declare provenance='DEF-A' — the exact "
                    "idealisation may never silently pose as the world (D-25).")
        else:
            p = provenance or PROVENANCE.get(name)
            if not p or not str(p).strip():
                raise ValueError(
                    "URM REFUSES: a world-tier RecordSurface requires PROVENANCE — the real record it "
                    "models and its constants' pinned sources (D-25, the principal 2026-08-20: the "
                    "model is grounded in real record data, never the toy category). Register the "
                    "source in model.project_model.PROVENANCE or pass provenance=... explicitly.")
        s = RecordSurface(name, mechanism, dE, E_b, T, f0, thermal=thermal)
        s.provenance = provenance or PROVENANCE.get(name) or ("DEF-A" if tier == "corner" else None)
        s.tier = tier
        return s

    @staticmethod
    def world_observation(manifest_path):
        """Load one physicist-supplied, content-addressed observation bundle.

        This is the URM's measurement input door.  It validates the closed schema,
        units, custody hashes, registered normalization, and declared coverage.  It
        deliberately returns no formation or gravity verdict: agreement with a
        prospectively frozen theory must be scored by a separate scientific layer.
        """
        from world_observation import load_world_observation

        return load_world_observation(manifest_path)

    @staticmethod
    def world_observation_certificate(manifest_path):
        """Return the non-scientific custody/coverage certificate for an observation."""
        return URM.world_observation(manifest_path).certificate()

    @staticmethod
    def formation_input(manifest_path):
        """Load one closed V002 physical formation input without scoring science."""
        from formation_input import load_formation_input

        return load_formation_input(manifest_path)

    @staticmethod
    def formation_input_certificate(manifest_path):
        """Return structural custody and D-to-V eligibility; authorize no claim."""
        return URM.formation_input(manifest_path).certificate()

    @staticmethod
    def formation_execution(manifest_path, execution_envelope_path):
        """Attach generic frozen-predicate outputs without a scientific verdict."""
        from formation_input import attach_formation_execution

        return attach_formation_execution(
            URM.formation_input(manifest_path), execution_envelope_path
        )

    @staticmethod
    def formation_validation(manifest_path):
        """Assess only whether distinct DEVELOPMENT and VALIDATION data are eligible."""
        from formation_input import assess_validation_pair

        return assess_validation_pair(URM.formation_input(manifest_path))

    @staticmethod
    def gamma_flow(manifest_path):
        """Evaluate one closed origin-neutral gamma-flow envelope through Repair3."""
        from gamma_flow import load_gamma_flow

        return load_gamma_flow(manifest_path)

    @staticmethod
    def gamma_flow_certificate(manifest_path):
        """Return the derived gamma-flow certificate; no input outcome is trusted."""
        return URM.gamma_flow(manifest_path).certificate()

    @staticmethod
    def gamma_flow_states(manifest_path):
        """Return the four internal discovery states without promoting proof output."""
        return dict(URM.gamma_flow(manifest_path).internal_discovery_states)

    @staticmethod
    def gamma_flow_proof_outputs(manifest_path):
        """Return Repair3-bounded authoritative proof mappings for GF0 through UGE."""
        return dict(URM.gamma_flow(manifest_path).proof_outputs)

    @staticmethod
    def proof_frontier(manifest_path):
        """Load the public-data proof frontier without promoting either proof."""
        from proof_frontier import load_proof_frontier

        return load_proof_frontier(manifest_path)

    @staticmethod
    def proof_frontier_certificate(manifest_path):
        """Return missing blockers, runnable work, and theory states with zero proof output."""
        return URM.proof_frontier(manifest_path).certificate()

    @staticmethod
    def proof_frontier_proof_states(manifest_path):
        """Return blocker or nonauthoritative input states; authorize no readiness/proof."""
        return dict(URM.proof_frontier(manifest_path).proof_states)

    @staticmethod
    def proof_frontier_theory_states(manifest_path):
        """Return theory support states under the strict unavailable-data fallback rule."""
        return dict(URM.proof_frontier(manifest_path).theory_states)

    @staticmethod
    def proof_frontier_execution_frontier(manifest_path):
        """Return available unrun obligations even when other obligations lack data."""
        return list(URM.proof_frontier(manifest_path).available_execution_frontier)

    @staticmethod
    def alpha_role():
        """Expose the pinned physical-alpha ALLOW/REQUIRE/SELECT theorem."""
        from alpha_role import alpha_role

        return alpha_role()

    @staticmethod
    def alpha_role_certificate():
        """Return exact allowance/inheritance status with selection left open."""
        from alpha_role import alpha_role_certificate

        return alpha_role_certificate()

    @staticmethod
    def udcl_postulate():
        """Expose the pinned U-DCL postulate and transitive axiomatic closure only.

        The separate CACNM theorem can transport an exact reference margin through a
        finite DAG only with common complete ports and full-channel certificates; it
        creates neither approximate DCL_phys nor REC. The separate FDFU theorem derives
        such a finite DAG for bounded finite-horizon recurrent missions whose every
        feedback cycle has positive total lower delay; it excludes instantaneous loops,
        Zeno accumulation, unbounded spawning/horizons, and hidden cross-use memory.
        """
        from udcl_postulate import udcl_postulate

        return udcl_postulate()

    @staticmethod
    def udcl_postulate_certificate():
        """Return its immutable zero-input certificate; natural validity stays open."""
        from udcl_postulate import udcl_postulate_certificate

        return udcl_postulate_certificate()

    @staticmethod
    def historywise_gravity_discriminant():
        """Expose the pinned finite-group formal discriminant; authorize no physics."""
        from historywise_gravity_discriminant import historywise_gravity_discriminant

        return historywise_gravity_discriminant()

    @staticmethod
    def historywise_gravity_discriminant_certificate():
        """Return its immutable zero-input certificate with every claim ceiling intact."""
        from historywise_gravity_discriminant import (
            historywise_gravity_discriminant_certificate,
        )

        return historywise_gravity_discriminant_certificate()

    @staticmethod
    def gravity_formation_theory():
        """Expose the hash-pinned closed working theory; accept no data or solver input."""
        from gravity_formation_theory import gravity_formation_theory

        return gravity_formation_theory()

    @staticmethod
    def gravity_formation_theory_certificate():
        """Return its immutable zero-input certificate with empirical ceilings intact."""
        from gravity_formation_theory import gravity_formation_theory_certificate

        return gravity_formation_theory_certificate()

    @staticmethod
    def gravity_microscopic_progress():
        """Expose sealed F3 progress through GL6CS without changing V014 semantics."""
        from gravity_microscopic_progress import gravity_microscopic_progress

        return gravity_microscopic_progress()

    @staticmethod
    def gravity_microscopic_progress_certificate():
        """Return exact collar, identifiability, reciprocity, and open-gate results."""
        from gravity_microscopic_progress import gravity_microscopic_progress_certificate

        return gravity_microscopic_progress_certificate()

    @staticmethod
    def relational_accumulation():
        """Expose authenticated finite relational accumulation with the L14 seam closed."""
        from relational_accumulation import relational_accumulation

        return relational_accumulation()

    @staticmethod
    def relational_accumulation_certificate():
        """Return the governing finite block certificate and closed L14 state."""
        from relational_accumulation import relational_accumulation_certificate

        return relational_accumulation_certificate()

    @staticmethod
    def universal_network_theory():
        """Expose the pinned UNT master theorem as a typed composition only."""
        from universal_network_theory import universal_network_theory

        return universal_network_theory()

    @staticmethod
    def universal_network_theory_certificate():
        """Return the zero-input UNT closure certificate with type ceilings intact."""
        from universal_network_theory import universal_network_theory_certificate

        return universal_network_theory_certificate()

    def roles(self):
        """Keep the historical role ledger, but replace its superseded gravity frontier."""
        roles = super().roles()
        roles["GRAVITY"] = (
            "The authenticated record block passes the finite ARGER Gate and establishes "
            "PASS_FINITE_DISCRETE_GFT_Z1_L4_L12 for the complete A009--A016 block "
            "from exact bounded membership, deduplicated authenticated mass above 0.50 "
            "at every tested size, and positive finite visibility in all 13 (L,q) rows. "
            "The authenticated construction through L12 completes the evidence "
            "obligation for this Gate application. The conditional dynamical-z=1 theorem is supplementary, while "
            "the RGRL/WTC infrared-response layer described next remains separately "
            "typed. L14 is "
            "INCOMPLETE_PRESERVED_NO_SCIENTIFIC_RESULT and is not a premise of the "
            "L4--L12 Gate. Gravity Formation Theory is separately closed as an exact "
            "record-first implication inside "
            "the explicit WTC-H1--H5 adopted-RGRL, memory-realization, same-metric response, "
            "Ward/constraint, and guarded endpoint premises; AURFT/U-DCL remains upstream "
            "program context rather than an extra theorem hypothesis. No graviton premise is required: the leading Einstein--Hilbert form is "
            "classified directly in the local four-dimensional metric-only two-derivative "
            "response class, and observed G calibrates its positive total Ricci coefficient only "
            "after same-leading-order remainders are excluded or controlled. RGRL is adopted, not empirically confirmed. "
            "The long route ledger that follows is historical: its open microscopic solder or particle gates do not reopen "
            "the WTC working implication. Under the adopted "
            "clarification, RGRL-C supplies full-rank or declared dense-range off-shell "
            "constitutive ancestry on the local spatial-metric tangent; it does not by itself "
            "supply an on-shell force law. The on-shell H^R kernel is separately established "
            "or measured, and the GI21 compatibility/type join is open. On the V002 well-posed "
            "retarded quotient with no unresolved zero mode, the same complete dressed source, "
            "remainder, and physical solution data give exactly zero on-shell response, and H^R "
            "may vanish without reducing the off-shell rank. The old local "
            "RGRL-C SPAG force/common-freefall labels are retired. The no-laboratory public-data "
            "substitute proves that the admitted packets lack the randomized same-parent eight-"
            "cell lineage intervention and do not identify beta_TM; its NIST/BIPM number is an "
            "optimistic planning envelope, not a SPAG limit. A bounded 28-query second pass found "
            "no new qualifying lineage root and retained only clock-network and femtonewton-force "
            "protocol components; the Panda response holdout remained closed. The independently source-calibrated "
            "G lane now has an exact finite-source/two-mode dressed forward model. It identifies "
            "p=Gs on a calibrated nonsingular row, while a free source scale obeys "
            "F(G,s)=F(Gq,s/q). The NIST/BIPM public apparatus reduces exactly to eight summary "
            "torque observations with a nonzero source column, but free source scale and "
            "configuration remainders prevent the full real fit; ten required fields remain absent. "
            "The official HUST-2018 release goes further: one figure-level ToS stiffness "
            "response is recovered, all three processed AAF source-response forwards close "
            "within 0.2 ppm without accepted G, and a representative acceleration stream "
            "separates the source and background harmonics. Processed source coefficients, "
            "missing mass geometry, transfer, corrections, calibration, covariance, and "
            "complete apparatus stress still prevent full GC16 or a new G. Equal-configuration "
            "ToS endpoint returns now also have an exact rank, overlap, and telescoping ledger, "
            "but separate same-ordinal panels and the missing no-excursion arm make it a history-"
            "confound diagnostic rather than causal memory or lineage gravity. Public unprocessed "
            "HUST geometry supplies exact conditional homogeneous source functionals and converged "
            "AAF/ToS coefficients, but the AAF pair distances leave two coordinate shears and the "
            "full apparatus remainder is not identified. Combining those kernels with corrected public "
            "responses, without accepted G, gives three conditional AAF quotients and seven affine ToS "
            "families; a normalization collision proves total inertia does not identify the missing "
            "source multipole, so no physical G point or interval is public. Public central corrections and "
            "signed ToS anelastic corrections now give calibrated partial kernels and narrow the residual "
            "comparator gaps, but the remaining row-wise harmonic source remainder is inferable from the "
            "authors' processed kernel rather than independently owned. One independently reconstructible "
            "row-bound remainder would unlock the first independent source-side row evaluation using the "
            "released response summary. A hostile-audited "
            "bounded public search found no qualifying remainder, physical map, or raw response packet on its "
            "declared surfaces; two dissertation leads remain acquisition targets, and the search is not a "
            "world-exhaustive absence claim. A separate 101,628-sample mechanical archive establishes "
            "same-apparatus path dependence but lacks authenticated lineage, randomized KEEP/BREAK, a common "
            "future query, covariance, and any gravity observable. The processed five-clock network has exact "
            "K5 cut rank four, cycle dimension six, and marginal-box optimum rho*=27/82; shared "
            "clocks/runs, assumed GR/common g, and absent joint covariance keep this at node-scalar "
            "compatibility rather than independent gravity or common-metric evidence. "
            "Real fit data and a lineage source remain absent. Beyond the conditional "
            "AFR raw-front route, q4 common-child incidence now exactly supplies the A3 sibling "
            "kernel, isotropic root second moment, covolume, and refining mathematical affine "
            "atlas. A supplied repeatable hop/onsite schedule gives an exact child-only phase and "
            "uniform Floquet parent/child separation, while the static source-off stagger and an "
            "autonomous phase remain absent. A supplied massless collective action has a smooth "
            "3+1 principal cone, but physical metric solder, clock/probe/physical-volume binding, tensor "
            "constraints, stress vertex, and gravity are open. Two adjacent q4 front cosets are "
            "exactly the diamond net in their translation completion and are locally exhausted by "
            "deep finite slabs. The later fixed-program solder physically binds finite local edges, "
            "so the deep-interior leading diamond-ice operator is represented; the raw slab has no "
            "global d*=2 sector, and a global U(1) phase still needs a supplied regular completion. "
            "Stability, all-orders control, visible EM, and tensor gravity remain open. On any "
            "supplied saturated q4 support, the "
            "unchanged one-carrier F3 restriction already gives exact scalar incidence hopping; no "
            "new hopping law is needed for that restricted result. But current BQ4 labels do not "
            "autonomously instantiate coexisting F3 sites/edges. Given a supplied finite F3 array, "
            "address map, q4 edge list, cap, schedule, and complete ports, existing FPMH/PESC gates "
            "do give an exact reversible fixed-program support solder and nonedge/guard quarantine. "
            "Both raw and K-gated incidence flips must be off or continuously cancelled during its "
            "invariant hold. This is not autonomous or scalable support selection. The source-off "
            "parent owns no static positive child detuning, and full degree-four hopping is exactly incompatible with d*=2 ice on the "
            "same binary incidence field. Six lawful FPMH records give a static S4 pair-register "
            "representation, while inherited register dynamics conserve every pair projector. "
            "Distinct physical q4 link factors instead give FJ's exact conditional finite rank-six "
            "A1/E/T2 spectral response, nearest-cell response, and finite spreading under programmed "
            "H_resp; this is not yet a continuum tensor solder or autonomous pole. Ice projection "
            "leaves one-link T2 and centered-pair E, and the local Fisher shortcut fails: its "
            "complement-broken rank-six covariance map borrows a vector-mean dyad. The fixed order-eight "
            "parent retains J8=429 h^8/(16 U_d^7) and V8=0. The finite H6 TT "
            "screen has nonzero connected two-Q and four-Q composite responses and positive composite "
            "Legendre quartics, but four bilinear Q insertions are an eight-one-link object. Composite "
            "amputation is not four-one-link or channel-2PI amputation. Its lowest selected composite "
            "pole lies above the finite two-one-link threshold proxy and is not energy-exclusive, so "
            "it earns only a finite precursor, not a thermodynamic tensor pole. The projected q4/F3 "
            "branch inherits one scalar compact-U1 Gauss species; H6/H8 rings preserve it, and four "
            "pair identities do not create the independent vector-plus-scalar first-class packet "
            "required by RGRL-B. The collective inventory now proves, on the favorable translation-"
            "complete FI screen, static co-metric coefficient rank six but retarded root-source rank "
            "zero because those sources commute and are conserved. This does not erase FJ's distinct "
            "conditional rank-six response. No present same-parent object simultaneously supplies six "
            "tensor configurations, nondegenerate conjugates, and the rank-two null packet. The first "
            "Q4-BLOCK-STRAIN-CTP prerequisite is now executed: four tetrahedral edge dyads have exact "
            "A1+T2 rank four and an E null of dimension two. Additive multi-edge weights, fixed Feshbach "
            "reduction, and every projected word through order eight retain that null. The complete "
            "covering-matched reduced CW/FM source has exact microscopic rank four and effective rank at "
            "most four; the degree tensor is one prospective query choice, while the unreduced physical "
            "BS source remains underdetermined. Existing degree/link/ice pair operators make E queryable "
            "and locally H6-dynamical, but identical H[0] admits rank-four additive and rank-six root-pair "
            "source derivatives. A symmetric lumped capacitance fails with exact E nullity two, while a "
            "fully grounded pair-resolved elastance and complete central kernel conditionally realize DPAR; "
            "ideal fixed-coupling Coulomb gives lambda=-1/2 without changing H[0]. Under explicit S10/FV-PURE, "
            "the projected nonidentity source has off-shell rank six. Its two explicit rank-closing pieces "
            "compose with the exact 180-state homogeneous sector in the hierarchy six family operators to "
            "five modulo identity to commutator rank three to ground retarded/first-moment rank two, with two "
            "rank-one residues. Generated Qdiag orders two, four, and six and their folds are omitted from that "
            "witness result, but their exact completion on the same component reduces them to the pair source "
            "plus identities with fE=1-x^2-(37/12)x^4-(16247/900)x^6. The complete homogeneous hierarchy "
            "therefore remains five to three to two to two with the same poles. Retaining each insertion's "
            "native A/B vertex or link-midpoint support before Fourier resolution exactly recovers m=0 and "
            "preserves all three fE coefficients at m=1 over Q(zeta_240); the ring remains a nonzero independent "
            "off-diagonal source. At x=2/5 and 1/2 the sampled finite response hierarchy is six through all five "
            "rank gates, TT ground-image rank is two, and four nonzero poles respond. Its nonzero spatial "
            "contraction excludes naive transversality. FZ proves the selected projected incidence charge is "
            "identically zero and leaves the full Ward packet undecided; GA supplies fixed-charge current ancestry, "
            "and GB supplies exact local ring-energy continuity while local momentum remains open. GC supplies the "
            "covering family, exact reciprocal momenta, and rank-two TT kinematics; FY's terminal 107-check custody "
            "replay makes this Phase A packet fully sealed. GD closes the historical direct route's G1 total-momentum gate on "
            "its declared auxiliary recoil torus without changing the FY source, and GF V005 seals that route's prospective "
            "particle-observable contract. That graviton/helicity route is now non-load-bearing for working-theory closure. "
            "The record-first completion instead uses observable pair memory C=<Y>, not the natural control J. At the symmetric "
            "localization point its six tetrahedral columns span Sym2. At a flat reference or for the locally frozen principal "
            "symbol, every nonzero momentum has intrinsic-curvature rank three with a three-dimensional pure-gradient kernel. "
            "Its finite full-support commuting pair sector has exact source reciprocity only under GK-S1--GK-S5 and a complete "
            "DPAR whole-pair tangent. Neither bounded result alone is gravity. The bare scalar-weighted GD "
            "flip/recoil projection also fails the declared FZ Ward embedding, closing that narrow shortcut without "
            "excluding a native complete current/contact parent. The active deeper lane is the microscopic derivation of RGRL-B "
            "from a translation-owning Maxwell + terminal + reservoir + support parent, followed by complete CTP/Ward and "
            "finite-family scaling. Empirical matched-lineage confirmation, strict origin of the whole Einstein--Hilbert "
            "coefficient, and a parameter-free numerical G remain open; see "
            "gravity_formation_theory_certificate() for pinned custody and exact ceilings."
        )
        return roles

    def corner(self, H, Ls=(), provenance=None):
        """D-25-gated DEF-A entry to the exact commutant corner."""
        if provenance != "DEF-A":
            raise ValueError(
                "URM REFUSES: an exact corner carrier must self-declare provenance='DEF-A' "
                "(D-25).")
        return super().corner(H, Ls=Ls)
