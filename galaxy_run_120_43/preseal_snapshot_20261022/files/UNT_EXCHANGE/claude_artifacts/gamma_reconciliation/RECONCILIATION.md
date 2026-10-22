# Γ reconciliation: is the V005 gravity search looking with a UNT perspective?
Claude, 2026-10-12. Built from `charter.md` and `canonical.md` in this folder; tags: [cited] path:line, [own] my derivation or `checks/`, [gap]. Read-only; no project code run; `lanes/P54_CODEX3` not read. CORE = `program-worktree/CORE_FRAMEWORK_V001.md`, V005 = `CANONICAL_MODEL_7_PROPOSAL_V005.txt` (full path in canonical.md:85-86), Pnn = `UNT_EXCHANGE/lanes/Pnn_*`, OUT = `checks/*_OUTPUT.txt`.

**Answer: no.** The 120/43 chain measures matter's local q-footprint, which is the coupling/occupancy layer. In V005, Γ lives in the incidence register: the flux/winding class of the ice manifold. No lane measures that class as Γ.

## 1. V005's q Records against R1–R3 (DEF-A, CORE:98-118)
- **(ii) fails globally.** Bind `g p_v X_q,v` is a term of H (V005 L6, L17). At p_v=1 it anticommutes with R_v=1−2q_v.
- **R2 fails.** In the Q=0 sector q_v is durable, since Bind and admission are inactive (P50 L110-117), but it has no admissible writer. (iv) ⟺ Tr(P_E R_v)=0 on every eigenspace (CORE:116), so the q_v=0 and q_v=1 blocks would have to be isospectral. Their traces differ by dim·(ε_r−2λ_R), because ⟨d_v⟩=2 on the 4-regular old and Born graphs [own]. A writer is excluded unless ε_r=2λ_R, which V005 does not declare; even then, isospectrality is unshown [gap].
- **R3 fails.** Whenever p_v=1, a one-site term writes and erases q_v (P27 L27). The Q=0 freezing is charge superselection: one local carrier insertion restores the writer. Under the amended (v′) (CORE:82), the on-site cost (1−2q)(ε_r−λ_R d_v) (P50 L118-119) is a tilt: one flip direction is downhill, so there is no barrier E_b [own].
- **R1** holds only through symmetry-related words, and R1 is cheap (G-11).
- **Verdict:** q_v is not Γ, in agreement with P27 L26, L30 and P50 L19-20. Spent, M_v, Q and the Q=0 q-words fail the same way (canonical.md §3).

## 2. What in V005 does satisfy R1–R3
- **Structure and label [own].** I = {d_v=2 ∀v} is the set of 2-factors (fully packed loops) of the 4-regular q4 graph. Its label Φ ∈ H₁(T³;ℤ)=ℤ³ comes from E_link=n−½ oriented A→B (P42b L173-177).
- **THEOREM [own]** (h=0, Q=0 sector, any q-word, generic coefficients): R_S=(−1)^{Φ_S} is an exact DEF-A record, where S is a cross-section avoiding the 4 cut edges that no new-star cycle crosses.
  - **(ii)** H|h=0 is diagonal in n apart from Tjoin, and Tjoin intertwines Φ_S (canonical.md §4.4).
  - **(iii)/R1.** On I, Σn_e=N_v and −λ_RΣd_v q_v=−2λ_RΣq. So all ice states with a fixed q-word and fixed cells are degenerate, and they carry many Φ: 6 of 6 sampled states distinct at L=4,5,6 (OUT).
  - **(iv)/R2.** The alternating flip U_γ on a non-contractible γ away from the cut and stars preserves every d_v and Σn, so [U_γ,H]=0, and it shifts Φ by [γ]. Its minimum weight is 2L for L≥4, as a product of 2L single-edge flips each of which leaves I. This is P-3's "admissible only as a whole" (CORE:171-181).
  - **(v)/R3.** A U supported on a contractible D maps n∈I to ice states n′, and n−n′ is a cycle in D, hence a boundary. So Φ is unchanged and U†R_S U≠−R_S. This is the Theorem C analogue; 0 of 1687 flippable short loops changed Φ (OUT).
- **At h≠0.**
  - Gauss law is broken: [Hjoin,G_v]=−iη_v hΣY (P48 L57-68). Φ becomes a perturbative label; sector-to-sector tunneling is O(h^{2L}), conditional on an uncertified defect gap Ud±μ_v>0 (P48 L163-165).
  - Records tilt the sectors at O(h²): W=2L²Σq−F·b (P42 L59-84). Ring dynamics splits them at O(h⁶): the max-flux layered state has 0 flippable hexagons [own]. The native phase is UNDETERMINED (P42 L155-165), and exact R1 survives only between symmetry-related sectors.
  - Shape: a U(1)/ℤ³ flux, a different mechanism from the charter's gapped ℤ₂ toric code. This is described, not ranked (D-9).
- **Native 2-cells [own].** "Contractible" is set by the lowest-order alternating loops: hexagons at h⁶, Birth 4-cycles at h⁴. Γ ≅ Z₁(I)/⟨short loops⟩ = ℤ³ only for L≥4. At L=2 and L=3 the shortest winding cycle is 4 and 6, no longer than a ring loop, so the literal L2 member (FROM_CODEX2/0096 L10) has no Γ (OUT).
- **The raw cycle space** β₁=2L³+1 is not Γ, because hexagons and Birth 4-cycles are local.
- **Birth rewrites Γ's record space itself** (OUT; illustrative cuts, not the declared one at V001 L30-33). Δβ₁=+2 in every case. Classes above ring length:

  | cut | L=4 | L=6 |
  |---|---|---|
  | spread | 3→1 | 3→8, max length 12→10 |
  | local | 3→3 | 3→4 |
- **Correction to charter.md §7.2.** Carriers are not Φ-writers: hopping "changes carriers only, not n_e" (P48 L65).

## 3. Where the 120/43 search is aimed
- **What it measures:** the Record-probability footprint around carriers (TO_CODEX/0104 L20), its reach and fall-off on Born sites (0101 L16), and a gapless channel for long range (0107 L9).
- **What steers it:** "a flat rotation curve needs a slowly falling footprint" (0097 L19), feeding a potential→43-velocities harness (PLAN.md L68, P-46).
- **The object is q_v,** which fails R2 and R3. That is the coupling layer, and C-80 says "the falloff enters only through the coupling" (REG:9674-9700). Pure Γ has no falloff.
- **The steering quantity is a falloff exponent,** which CORE:18-25 excludes. Computing it and reporting it as a relationship is allowed; choosing lanes by it makes a classical form the test (D-1).
- **Γ enters no link of the chain.** The only Γ contact was Codex2's F·b sector bias (P42 L59-84), filed as background selection. C-90/91's kernel is Γ-priced; the V005 kernel is Bind-priced.

## 4. A Γ-first search inside V005 (native; classical forms only as final-scale relationships)
- **G1 Certify.** Register the h=0 theorem. Compute the sector-resolved spectrum of the projected ring model against L (R1 at h≠0; report the measured splitting, with no target law). Produce the defect-gap certificate Ud±μ_v>0 (R3 in the full H).
- **G2 Cost of writing Γ.** Compute the inter-sector amplitude A(γ) at O(h^{2L}), whose energy denominators carry μ_v=μ0+λ_J p_v−λ_R q_v (P47 L111-118). Matter and Records then set the price of writing Γ through a region: the native form of C-78's "distance = boundary-crossing cost".
- **G3 Records→Γ.** Compute ΔE(Φ | pattern) for crossed and compact patterns. Uniform backgrounds do not tilt the sectors; interfaces (b) do. So Γ responds to Record boundaries, not Record density, which is C-77's shape.
- **G4 Matter↔Γ [own; size open].** At h=0 with Q≥1, n is still conserved, but U_γ no longer commutes with loop-confined hopping (P47b L5-27). Compare carrier spectra on winding and contractible loops to measure how matter splits or selects Γ sectors.
- **G5 Birth→accumulated Γ.** For the declared cut, compute the map of protected classes: rank, systole/cosystole profile, pairing, and whether Φ is carried or written.
  - V005 already holds three of Corollary 5.4's five objects: (1) old⊕Born fibers, (3) the owned transition ε_B Tjoin, and (5) Q/M intertwined (V005 L11-15). Objects (2) and (4) need to be declared.
  - One Birth level caps accumulation. The repeated-Birth test model (P-51) should report Γ-class growth and protection, not q reach.
- **G6 T-20 in V005.** The collective quantity is the Γ-class data of the effective fiber over Birth histories, as a function of matter and Record content through G2–G5. C-80 anticipates constants, homological switches and w_min=d; these are results, not nulls (D-14).

## 5. Premise conflicts the principal registers (declared, not computable)
- **P-a.** "Record" in V005 (q_v, V005 L4) is not the charter's record (CORE:98-106). S1 says matter and space "are made of Records" (V005 L28); in the charter's sense, that points to Γ-protected incidence structure, not to q bits.
- **P-b.** R3 has two readings: exact (v), or amended (v′) (O-51, which postdates the charter). q_v fails both. The reading decides any barrier-protected candidate.
- **P-c.** The charter claims gravity comes from Γ (THIRD_TERM_V001.md:62-66), but the 120/43 kernel carries no Γ. This premise has to be registered either way.
- **P-d.** The canonical L is declared (V001 L30-33; 0096 L10), and Γ exists only for L≥4.
- **Documentary, not a principal matter:** the charter is stale. Uniqueness FAILED at G-6 (SL:41), and T-20 is DONE and was reread into C-77 (plan.tsv:17; SL:248).
