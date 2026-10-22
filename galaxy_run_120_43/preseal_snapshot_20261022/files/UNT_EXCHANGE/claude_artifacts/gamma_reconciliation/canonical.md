# Canonical V005: what "Record" means, its global structures, and which ones are protected

Claude, 2026-10-12. Reconciliation input for the principal's question *"Are we sure that we're looking at
the search with a UNT perspective?"* (relayed in `TO_CODEX/0106`).

Rules followed: this was read-only everywhere. Nothing was written outside this directory, and no
project or Codex code was run. Two small checks of my own are in `checks/`. Codex3's parallel P-54 lane
(`lanes/P54_CODEX3`) was **not** read, so the two readings stay independent. No classical quantity is
used as a criterion (charter D-1). Γ is judged only against R1/R2/R3.

Tags: **[cited]** means stated in a source, with path and lines given. **[own]** means my own derivation
or check in `checks/`. **[gap]** means it is not established anywhere I read.

---

## 0. Bottom line

1. **V005's "Record" q_v is a local per-vertex register.** Its only writer is the strictly local Bind
   term `g p_v X_r,v`, which is part of H and is gated by a carrier at that same vertex. q_v is not
   conserved whenever a carrier can be present. It is frozen only in the carrier-free and Ready-free
   charge sector (Q=0), and only because the writer is absent there, not because anything protects it.
   **By its form it fails R2 and R3.** The canonical documents themselves already say a bare q bit is
   not a qualified record.
2. **The other exact labels in V005 are local inventories or symmetry charges, not topology.** These are
   the global carrier+Ready charge Q, the per-site Ready+Spent label M_v and the q-words frozen at Q=0. A
   local operation changes each of them. None of them meets R2/R3.
3. **The one V005 structure with the R1–R3 *shape* lives in the incidence register n, not in q.** It is
   the flux/winding sector of the ice manifold (all degrees d_v=2) on the periodic old graph. That sector
   is an integer homology class, H₁(T³) ≅ ℤ³. Every alternating loop that fits in a contractible region
   preserves it. The shortest operation that changes it is an alternating loop flip of weight 2L.
   [own: proof below, and the check found 0 flux changes in 1687 flippable short loops; writer weight
   8/10/12 at L=4/5/6.]
4. **The protection is conditional.**
   - Gauss law is exact only on the projected ice subspace. At h≠0 the full H breaks it [cited, P48].
   - So protection in the full model is perturbative, at order 2L, and needs a defect-gap certificate
     that has not been supplied.
   - Exact degeneracy between sectors (R1's "same energy") is undetermined.
   - The tiny canonical sizes have no protection at all: at L=2 the shortest winding cycle has length 4,
     and at L=3 it has length 6, the same as a ring flip. [own]
5. **Matter and Records do not write the flux label.** Only `-h X` and Birth change n. Instead they act
   on it in two ways:
   - **Energy bias.** Layered written/blank patterns add an energy linear in the flux, F·b [cited, P42
     V002 §3].
   - **Protection gap.** q and p shift the local cost of Gauss defects through
     `μ_v = μ0 + λ_J p_v − λ_R q_v` [cited, P47 D1]. Defects are exactly the excitations whose transport
     would change the flux.
6. **Birth changes the cycle space.** It always adds 2 to the cycle rank when the graph stays connected,
   and it can disconnect a tiny graph. What it does to the protected classes depends on where the four
   cut edges are [own MCB check]:
   - **Cut inside one small patch:** the new cycles are short (length 4 or 8), the three winding classes
     keep length about 2L, and the flux label passes through Birth unchanged.
   - **Cut spread across the torus:** the new stars short-circuit the winding classes (length 16 drops to
     12 or less at L=8) and add classes of intermediate length.

   The canonical first-cut geometry is a declaration I did not reproduce.

---

## 1. Sources read

| ID | Path | Used for |
|---|---|---|
| CHARTER | `/Users/bgm/Research/Universal Network Theory/program-worktree/THIRD_TERM_V001.md` | R1–R3 (L21–27), H₁ is a candidate (L39–45), the claim and T-20 (L62–73) |
| SUPERSEDED | `.../program-worktree/GRAVITY_DEFINED_V001.md` | earlier definition table (L8–18), superseded (L1–2) |
| CORE | `.../program-worktree/CORE_FRAMEWORK_V001.md` | record clauses (i)–(v) (L100–106); admissible U, [U,H]=0 (L114–124); P-3, writer admissible only as a whole (L171–181) |
| CLAIM | `.../program-worktree/THE_CLAIM_V001.md` | Theorems A–D roles (L39–46) |
| V005 | `.../CANONICAL_V006_SELECTION_AND_EXACT14_CROSSWALK_V001/CANONICAL_MODEL_7_PROPOSAL_V005.txt` (full path in 0051) | domain/registers L4; H7 L5–7; admission L9–10; Hjoin L11–12; Birth L15; Bind/admission/feedback L17; S1 L28; p/q/Spent distinct and blank-insertion open L32; tracial q=1/2 control L34 |
| V001 | same dir, `CANONICAL_MODEL_7_PROPOSAL_V001.txt` | Bind changes a Record, Nc fixed (L19–20); four-cut/two-star map, "four net bonds" (L25–28); map/cut/embedding are declared choices (L30–33) |
| V004 review | same dir, `CANONICAL_MODEL_7_PROPOSAL_V004_INDEPENDENT_REVIEW_V001.txt` | PASS_DOCUMENTARY (L3–5) |
| 0051 | `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0051_2026-10-12_S1-canonical-registration-...md` | S1 registered in V005; blank states are controls; P49 derives the background (L5) |
| P27 | `/Users/bgm/Research/UNT_EXCHANGE/lanes/P27_CODEX3/GRAVITY_BRIDGE_CANONICAL_V004_PORT_V002.md` | q is not S/S_cut/K/C_ab/metric (L26); [HA,q]=0, [Bind,q]≠0 (L27); a qualified record needs more than a bit (L30); admission is not a q writer (L98) |
| P50 | `/Users/bgm/Research/UNT_EXCHANGE/lanes/P50_CODEX3/P50_CANONICAL_MATTER_DICTIONARY_V002.txt` (+ `INDEPENDENT_MATTER_DICTIONARY_THEORY_REVIEW_V001.txt`, PASS_SCOPED) | registers (L13–20); defects and loops, "no generic topological protection" (L76–101); winding label ≠ loop ≠ defect pair (L92–94); Q0 memory (L110–117); q flip cost, Bind writes/erases (L118–125); A_v conserved, Spent reversible (L130–140); Born (L150–166); dispositions (L206–212) |
| P50b | `.../P50_CODEX3/P50_BIND_CLOUD_SELF_ENERGY_AND_CURVATURE_V001.txt` | carrier+Record dressing (context only) |
| P42 | `/Users/bgm/Research/UNT_EXCHANGE/lanes/P42_CODEX2/P42_SECOND_FOURTH_ORDER_DIAGONAL_TERMS_V002.txt` | formal and uncertified (L1–3); E2 with λ_R in denominators (L22–45); γ sign (L47–51); layered W is constant within a sector, linear flux bias (L59–84); crossed pattern changes W locally (L86–114); uniform-q E4 is configuration-independent (L141–148) |
| P42b | `.../P42_CODEX2/P42_BINARY_FAMILY_AND_SAME_STATE_RESPONSE_V003.txt` | E_link=n−½, ice is divergence-free, Ud penalizes Gauss defects (L173–177); conditional flux-sector energy form (L182–188) |
| P42c | `.../P42_CODEX2/P42_PATTERNED_OPTICAL_MSCM_PROTOCOL_V001.txt` | restates the sector constant/bias (L108–111) |
| P45 | `/Users/bgm/Research/UNT_EXCHANGE/lanes/P45_CODEX2/P45_SIXTH_ORDER_UNIFORM_DIAGONAL_AND_ENDPOINTS_V001.txt` | uniform-α order-6 diagonal counts are independent of the flux sector (L62–70); ring operator c_b I + K_b R (L84–89) |
| P48 | `/Users/bgm/Research/UNT_EXCHANGE/lanes/P48_CODEX3/P48_FULL_CANONICAL_CONSTRAINT_CENSUS_V001.txt` (+ `ROOT_DISTINCT_CONSTRAINT_CENSUS_THEORY_REVIEW_V001.json`, PASS_SCOPED_ANALYTIC_THEORY_WITH_EXPLICIT_LIMITS; + `P48_S1_PHYSICAL_SCOPE_ADDENDUM_V001.txt`) | N2 Born graph disconnected (L17–19); Gauss operators and ranks (L29–55); h breaks Gauss (L57–72); Birth intertwines Gauss, new length-4 cycles (L74–82); diagonal-linear conserved span Q, M_v (L90–128); not gauge constraints (L136–152); projected degree-2 kinematic (L154–173); verdict (L216–225) |
| P47 | `/Users/bgm/Research/UNT_EXCHANGE/lanes/P47_CODEX3/P47_RING_ENERGY_BIRTH_AND_DEFECT_COMPOSITE_CHANNELS_V001.txt` | surgery is not automatically a local defect; "Born surgery changes connectivity, cycle space, constrained sectors" (L93–109); defect-occupation identity D1 (L111–118) |
| P47b | `.../P47_CODEX3/P47_LOOP_CONFINED_NATIVE_HISTORY_AND_GRAPH_EXPOSURE_V002.txt` | carriers confined to occupied ice loops exactly (L5–27); Birth releases confinement (L215–219) |
| P47c | `.../P47_CODEX3/P47_TOTAL_RING_SIGN_AND_MAGNETIC_SCOPE_V001.txt` | ring-sign Z₂/U(1) link-phase scope (L91–121) |
| P51 | `/Users/bgm/Research/UNT_EXCHANGE/lanes/P51_CODEX2/P51_TEST_MODEL_FINITE_BIRTH_THEORY_V001.txt` (+ `FROM_CODEX2/0096...` L10–12) | lexicographic cuts reuse the 4 smallest A anchors; connectedness to be checked (L86–103); literal L2 member has 2⁴⁸ words (0096 L10) |
| P49 | `/Users/bgm/Research/UNT_EXCHANGE/lanes/P49_CODEX2/P49_QPOSITIVE_QUOTIENT_FRAGMENT_AND_EOS_CONTROL_V001.txt` | N2 four parallel edges; Born graph has two disconnected components (L6–9) |

The V005 directory is
`/Users/bgm/Research/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/ROOT_UNT_LOCAL_RESIDENCY_MANIFEST_V002/exploratory_physics/PHASE12_PARALLEL_SCREEN_V001/H_record_front_provisional_V001/NATIVE_COEFFICIENT_DEPENDENCE_AUDIT_V001/CANONICAL_V006_SELECTION_AND_EXACT14_CROSSWALK_V001/`.

---

## 2. What "Record" means in V005

**Register [cited, V005 L4].** Every site carries independent factors: a hard-core carrier p_v, the
"native Record" q_v ∈ {0,1}, and a cell register in span{I,R,S}, where R = Ready and S = Spent. Every
edge carries an incidence bit n_e. The degree is d_v = Σ_{e∋v} n_e.

**Terms of H that involve q [cited, V005 L5–7]:**
- `+ε_r Σ_v q_v` (diagonal);
- `−λ_R Σ_v d_v q_v` (diagonal feedback, which couples q to the incidence degree);
- `+g Σ_v p_v X_r,v` (Bind).

**Which operators change q:**

| owner | changes q? | source |
|---|---|---|
| Bind `g p_v X_r,v` | **yes, and it is the only native writer/eraser.** It is local and gated by a carrier at the same vertex. It rotates q even at a Spent site. | V005 L17; V001 L19–20; P27 L27, L98 |
| admission HA (R/blank-p ↔ S/occupied-p) | no: [HA, q_v] = 0 | V005 L9, L17; P27 L27 |
| hopping `−t n_e T_e(θ)` | no (moves the carrier only) | P48 L65 |
| incidence flip `−h X_e` | no | P48 L57–66 |
| Birth Tjoin | inserts **blank** q at the two new stars and copies old q unchanged | V005 L15 |

**Consequences:**
- **Conservation.** q_v is not conserved in any sector where p_v can be 1 (P27 L27; V005 L17: "Nspent
  and Nq … neither is asserted monotone"). In the carrier-free and Ready-free sector Q=0, Bind and
  admission are inactive and every q-word is an exact invariant (P50 L110–117; P48 L125–126). That
  invariance holds only because the writer is absent from the sector (a superselection by Q), not
  because of any protection.
- **Energetics on ice.** On the exact ice manifold d_v = 2, so the feedback term reduces to the constant
  `2λ_R Σ q` [cited, P42 L38–40]. q therefore affects the incidence structure only through virtual
  Gauss-defect excursions: the λ_R-dependent denominators D_e = 2Ud + σ_e(δ − λ_R(q_u+q_v)) (P42 L22–45).
  [own reading] So the channel through which Records reach the incidence structure is the same
  defect-excursion channel that §4.3 identifies as the threat to the flux label's protection.
- **The documents already limit what a "Record" is.** P27 L26: "q is not Spent S, the cut census
  S_cut, … or a metric." P27 L30: a qualified record requires "operational preparation,
  distinguishability, retention, complete read and lineage controls; an instantaneous bit occupation
  … alone does not meet those conditions." P50 L19–20: "a bare q bit does not by itself certify
  redundant classical information, a mass, or a particle worldline."
- **S1 (V005 L28, L32).** S1 declares that every physical state is Record-filled. It gives no numeric
  meaning to "filled" and does not identify p with q or Spent with q.

**q_v against the charter's record clauses (CORE L100–106) [own, from the cited operator facts]:**

| clause | q_v (as R_v = 1−2q_v) |
|---|---|
| (i) involution | yes |
| (ii) durable, [H,R]=0 | **fails whenever Q≥1** (Bind is in H). Holds only inside the Q=0 sector. |
| (iii) distinguishes states of the same energy | only through symmetry-related words. Flipping one bit costs (1−2q)(ε_r − λ_R d_v) in the frozen diagonal subcase (P50 L118–119). |
| (iv) writable by an admissible U | the native writer is Bind itself, which is local and part of H |
| (v) protected: no admissible single-region operation flips it | **fails.** The writer is a one-site operator, `X_r,v` gated by `p_v`. |

**Verdict: q_v fails R2 and R3 by construction.** This agrees with TO_CODEX/0106 L13. The word "Record"
in V005 names a register. It does not name the charter's record.

---

## 3. Other local labels and charges

| structure | what is exact | R1/R2/R3 verdict | source |
|---|---|---|---|
| Spent census S_v | reversed by admission | not durable; fails R2/R3 | V005 L17; P50 L130–140, L209–210 ("Spent permanence REFUTED") |
| M_v = Ready_v + Spent_v | exactly conserved at every site, including the zero-extended new sites | local label: a single-site cell operator outside H changes it, so it fails R2/R3. This is symmetry/superselection, not topology. | P48 L101–128, L136–144; P50 L132 |
| global Q = Σ(p+Ready) | exactly conserved, one U(1) charge | sectors are charge sectors; a local carrier creation operator changes Q; fails R2/R3 | P48 L102, L136–138; P50 L14 |
| q-words in Q=0 | exact invariants | frozen only because Bind is absent; a single local carrier insertion re-enables writing; fails R3 | P50 L110–117 |
| old/Born sector projector | not conserved, since Birth acts coherently in both directions | not a record | P48 L119; P50 L152–154 |

P48's exhaustive result (L121–135) is limited to the diagonal-linear ansatz. The full commutant of H
(nonlinear, off-diagonal and collective operators) is explicitly not exhausted, so this table does not
claim that no other conserved structure exists. **[gap]**

---

## 4. Global and topological structures

### 4.1 Raw graph cycle space versus the homology classes

**[own check: `checks/diamond_cycle_flux_birth_check.py` and `checks/min_cycle_basis_profile.py`]**

Setup: periodic q4 diamond on an L×L×L torus of primitive cells, with V = 2L³ vertices and E = 4L³
edges. The script's cell conventions are mine. The canonical L and labels are declarations I did not
reproduce.

- **Cycle rank.** β₁ = E − V + 1 = 2L³ + 1. Almost all of it is spanned by hexagons, the ring-flip loops.
- **Minimum cycle basis (exact, GF(2)).** For L = 4, 6, 8 it is {6: β₁−3, 2L: 3}. So the cycle space
  modulo short loops is rank 3, which is H₁(T³), and every one of the three classes has a shortest
  representative of length **2L** (8, 12, 16).
- **Hexagons carry no winding for L ≥ 4.** All length-≤6 cycles have winding 0, and float, GF(2) and
  mod-p ranks agree.
- **Tiny sizes have no protection length.**
  - L=2 (V=16, E=32, the literal "L2" size in 0096 L10): girth 4, and 4-cycles already wind. The
    shortest winding cycle has length 4, which is shorter than a ring loop.
  - L=3: the shortest winding cycle has length 6, equal to the hexagons, so the quotient is 0.

  At these sizes a ring flip can already change the topology. This is consistent with 0027 having to
  look elsewhere (PG(2,3)) for a girth-6 witness.

### 4.2 Gauss law

- **Operators and rank [cited, P48 L29–55].** G_v = η_v(d_v − 2), with η = ±1 by sublattice. The G_v
  commute. Their rank is Nv − c on each graph, and Nv_old + 1 for the old/Born direct sum.
- **Broken at h≠0 [cited, P48 L57–72].** `[Hjoin, G_v] = −i η_v h Σ_{e∋v} Y_e`. So at h ≠ 0 local Gauss
  is not conserved, even in Q=0 with q=0. At h=0 the G_v are conserved labels, but they are not imposed
  constraints.
- **Birth intertwines Gauss exactly** (P48 L74–82, eq. 2). Each new star gets degree S_cut = 2.
- **Projected degree-2 subspace P2.** G_v P2 = 0 holds kinematically with every register and Born
  off-image retained (P48 L154–173). Records, Bind and admission "do NOT algebraically destroy the
  degree2 constraint", but P2 is not certified to be a separated low band (L163–165).
- **Defect energetics** (P47 RING L111–118, D1):
  `H = K + U_d N_def + Σ_v (μ0 + λ_J p_v − λ_R q_v) s_v`, with s_v = d_v − 2 and
  μ0 = Δ_can/2 + 2U_d(2 − d*). **Carriers and Records shift the local Gauss-defect cost.**

### 4.3 Flux / winding sectors of the ice manifold

**Definition [cited, P42b L173–177].** Orient each edge A→B and set E_link = n − ½. Ice (d_v = 2) is
divergence-free.

**Homology statement [own].**
- The difference n − n′ of two ice configurations is an integer 1-cycle.
- Its class in H₁(T³; ℤ) ≅ ℤ³ is the flux change Φ(n) − Φ(n′). Here
  Φ = Σ_e (n_e − ½)·disp_e / L, or equivalently the intersection number with three cross-sections.
- If n and n′ differ only inside a contractible region, the difference cycle is a boundary, so ΔΦ = 0.
- Hence **no ice-preserving operation supported in a contractible region changes Φ.** This holds
  exactly on the ice manifold, for every alternating loop of any length that fits in such a region.
- Check: 6 random ice states each at L = 4, 5, 6 gave 6 distinct flux classes per L. Of 254, 518 and
  915 flippable alternating short loops, 0 changed Φ. The shortest alternating loop that does change Φ
  had length 2L = 8, 10, 12.

**Writer [own].**
- The flip of an alternating non-contractible loop, of weight ≥ 2L, changes Φ_j by ±1.
- It is a product of 2L single-edge operations, and each single-edge flip alone leaves the ice manifold.
  This matches the charter's P-3 shape (CORE L171–181): "admissible only as a whole".
- In the full H the writer appears at order h^{2L}, or through a defect pair transported around the
  torus.

**Energetics across sectors (R1).**
- *Diagonal degeneracy for uniform q [cited].* For uniform q, the second-order diagonal energy W is
  constant on the ice manifold (P42 L83–84). E4 is configuration-independent (P42 L141–148). The order-6
  diagonal counts are "independent of the ice configuration, including the flux sector" (P45 L69–70).
  So through order 6 in the diagonal part, uniform-Record backgrounds leave the flux sectors degenerate.
- *The off-diagonal ring term splits sectors.* It acts within each sector (P45 L84–89) and its
  spectrum depends on the sector. [own] The maximal-flux layered state at L=4 has **zero** flippable
  hexagons, unlike generic sectors.
- *Conditional splitting form [cited].* If a quadratic deconfined description is independently
  qualified, flux energy takes the form κΦ²/(2L) (P42b L182–188). That is power-law splitting, not
  exact degeneracy.
- *Status.* Native phase and stiffness are **UNDETERMINED** (P42 L155–165). Exact degeneracy
  holds only between symmetry-related sectors.
- *Records bias the sectors [cited, P42 L59–84].* For layered Record patterns the diagonal term gives
  W = 2L²Σq_i − F·b, where b counts written-to-blank interfaces. This is **constant within a fixed
  winding sector and linear in the flux F between sectors**: "The h2 term biases global flux sectors
  and can change background selection." For crossed patterns a single remote hexagon changes W
  (L86–114), so the "constant within sector" property is specific to layered patterns.

**Protection outside the ice manifold.**
- At h ≠ 0 the label is protected only perturbatively, at order 2L. This needs a defect gap
  Ud ± μ_v > 0. No certificate exists (P48 L163–165; P42 L1–3: "FORMAL PERTURBATIVE, UNCERTIFIED AT THE
  PHYSICAL TUPLE").
- P50 L96–101 says correctly that loop names supply no generic topological protection. The protection
  above comes from homology plus the defect gap. It does not come from any loop's name.

**Shape difference from the charter's verified candidate [cited + own].**
- The charter's verified carrier is the toric code's 2D H₁(Σ) with a ℤ₂ intersection form (CORE
  L136–141; SUPERSEDED L8–18).
- V005's label is a 3D ℤ³ (U(1)-type) flux, paired H₁ × H₂ with cross-sections.
- The splitting law (power-law for a Coulomb-type flux sector versus exponential for a gapped ℤ₂ code)
  is a native phase question. It is not a criterion.

### 4.4 Birth and the cycle space

**Cited facts:**
- Each cut edge (u,v) becomes (u,starB) and (starA,v). The children copy the bit, and Birth is gated
  on S_cut = 2. It is reversible (Tjoin†) and retains all off-images (V001 L25–28; V005 L15; P48
  L13–17).
- Birth intertwines degrees, so the ice manifold maps into the ice manifold (P48 eq. 2).
- New length-4 cycles appear (P48 L81–82).
- "Born surgery changes connectivity, cycle space, constrained sectors and spectra. A rank/flux-sector
  change is a global structural observation" (P47 L102–103).
- The tiny N2 Born graph is disconnected (P48 L17–19; P49 L6–9).
- Under the P26 test rule, later cuts reuse the four smallest A anchors (P51 L86–103).

**Own (minimum-cycle-basis length profiles; my illustrative cuts, not the declared canonical one):**

| L | old | Born, local cut | Born, spread cut (anchors L/2 apart) |
|---|---|---|---|
| 4 | {6:126, 8:3} | {4:3, 6:125, 8:3} | {4:1, 6:129, 8:1} |
| 6 | {6:430, 12:3} | {4:3, 6:428, 8:1, 10:1, 12:2} | {6:427, 8:7, 10:1} |
| 8 | {6:1022, 16:3} | {4:3, 6:1020, 8:1, 14:1, 16:2} | {6:1018, 8:1, 10:7, 12:1} |

- β₁ rises by exactly 2 in every case (all connected). Ice is preserved (all degrees 2 after the
  copy-surgery).
- **Local cut:** the new classes have length 4 or 8, independent of L, so they are not protected. The
  three winding classes keep length about 2L.
- **Spread cut:** the stars act as shortcuts. The longest basis cycle drops from 2L to about L + 4, and
  classes of intermediate length appear.
- **Intertwining identity [own].** Let S be an old cross-section edge set disjoint from the four cut
  edges, such that no new-star cycle crosses S. Then Φ_S^new · T = T · Φ_S^old, so Birth carries the
  flux label unchanged. When a star cycle does cross S, a short loop through the star flips Φ_S. For
  such a cut, Birth degrades protection.

### 4.5 Occupied loops and carriers

- **Cited [P47b L5–27].** At fixed ice incidence, carrier motion is exactly confined to its occupied
  component, a cycle or path in the degree-2 occupied subgraph. Bind can change q but cannot move the
  resource.
- **Cited [P47b L215–219].** Full h and Birth release this confinement.
- **[own inference, gap]** The topology of the occupied loops (contractible or winding, and their
  lengths) is set by the incidence sector. In the maximal-flux layered state every occupied loop is a
  straight winding line of length 2L. So a carrier's band (P50 L41–42) and the trail of q it writes
  through Bind follow loops whose shape depends on the flux sector. Two conditions remain unquantified:
  whether matter can thereby *read* the sector, and whether the q it writes feeds back through W.

---

## 5. Protection summary (R1 / R2 / R3)

| structure | R1 SPACE (size > 1, same energy) | R2 non-local WRITER | R3 no local write or destroy | verdict |
|---|---|---|---|---|
| q_v (V005 "Record") | only through symmetry-related words | **no**: writer is local Bind in H | **no** | not Γ (§2) |
| Q=0 frozen q-words | as above | **no** | **no**: frozen only by charge sector | not Γ |
| Spent S_v | – | **no** (admission) | **no** | not Γ |
| M_v, Q | charge/inventory sectors | **no**: local operations change them | **no** (symmetry, not topology) | not Γ |
| raw graph cycle space β₁ | – | Birth (a term of H) changes it | **no** for its local part (hexagons, Birth 4-cycles) | not Γ as a whole |
| **ice flux class Φ ∈ H₁(T³)** | sectors exist; diagonal-degenerate through order 6 for uniform q; ring and phase splitting **undetermined**; Records with interfaces bias by F·b | **yes**: alternating non-contractible loop of weight 2L; no contractible alternating loop changes Φ (exact on ice) | **exact on the ice manifold**; in full H only at order 2L and conditional on a defect gap (uncertified); none at L ≤ 3 | **the only Γ-shaped candidate in V005; R1 degeneracy and full-H R3 are open** |
| Birth-added classes | – | Birth is the writer and is in H | local cut: length O(1), not protected; spread cut: shortens the winding classes | Birth is a native writer of the cycle space and, with a spread cut, a degrader of Φ's protection |

---

## 6. How matter, Records and Birth act on the Γ-shaped structure (native statements only)

1. **Writing.** Only `−h X` (at order 2L, or through transported defects) and Birth can change Φ. Bind,
   hopping, admission, ε_r, the cell energies and both feedback terms cannot (P48 L57–68).
2. **Energy bias.** Layered written/blank patterns tilt the flux sectors linearly in F times the number
   of interfaces b (P42 L59–84). Uniform written backgrounds (the S1 class with no interfaces) do not
   tilt them, up to the diagonal orders cited.
3. **Protection gap.** Records and carriers shift the local Gauss-defect cost by −λ_R q_v and +λ_J p_v
   (P47 D1). Defects are the excitations whose transport around the torus changes Φ.
4. **Birth.** Birth is coherent and reversible, and changes the cycle space (Δβ₁ = +2 when connected).
   Whether it preserves Φ's protection depends on the declared geometry of the four cut edges (§4.4).
   The graph itself is in superposition, so the "space of sectors" depends on the sector (old vs Born).

---

## 7. Open items, classified (none handed back as choices)

- **Declared:**
  - The canonical L, cell convention and first-cut labels (V001 L30–33, "declared choices"). Whether the
    literal member has any protection length depends on these (§4.1).
  - The naming premise "V005's q_v Record = the charter's record". The sources contradict it on their
    face (§2). Registering it is the principal's prerogative per TO_CODEX/0106 item 4. It is recorded
    here only as a conflict.
- **To be computed:**
  - Exact or certified sector splitting for uniform-q backgrounds, ring term included (R1). Currently
    UNDETERMINED: P42 L155–165.
  - A defect-gap certificate Ud ± μ_v > 0 with μ_v including q and p (R3 in the full H). Not supplied:
    P48 L163–165.
  - The flux-sector map through the declared canonical Birth (the §4.4 identity applied to the literal
    cut).
  - The general commutant beyond the diagonal-linear ansatz (P48 L130–135).
- **To be measured (native, no classical template):**
  - The response of the flux-sector distribution to Record patterns (F·b bias, background selection),
    and to Birth.
  - Whether carrier spectra or Bind trails depend on the sector (§4.5).

---

## 8. Own check files (written only in this directory)

- `checks/diamond_cycle_flux_birth_check.py` → `checks/diamond_cycle_flux_birth_check_OUTPUT.txt`.
  Covers cycle ranks (float, GF(2), mod-p), windings of short cycles, shortest winding cycle, random ice
  flux classes, flux invariance under flippable short alternating loops, the shortest flux-changing
  alternating loop, and Birth surgery degrees and quotients.
- `checks/min_cycle_basis_profile.py` → `checks/min_cycle_basis_profile_OUTPUT.txt`. Exact GF(2)
  minimum cycle basis length profiles (Horton candidates plus greedy elimination) for the old graph and
  both Birth variants at L = 4, 6, 8.
- Both are pure combinatorics on graphs built by the scripts themselves. Neither imports or executes any
  project or Codex code.
