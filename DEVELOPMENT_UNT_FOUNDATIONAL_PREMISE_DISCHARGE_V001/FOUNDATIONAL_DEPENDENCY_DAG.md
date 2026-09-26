# Foundational dependency DAG

**Status:** initial critical-path map, 2026-09-25
**Authority:** audit aid only; source theorems and their seals remain controlling.

## Reading rule

A solid arrow means “is required to support,” not “has already proved.” A
dashed arrow marks partial support, a route-specific condition, or a historical
constraint rather than a universal prerequisite. A green node is established
at its stated ceiling; amber is an adopted premise; blue is an active computed
lane; red is an audited negative result; orange has unresolved custody/audit;
gray is open; and a gray dashed border is superseded. The graph therefore makes
the central gap visible instead of allowing an exact conditional conclusion to
hide an unproved antecedent.

```mermaid
flowchart TD
    B0["B0: finite record construction<br/>EXACT membership + COMPUTED mass/visibility<br/>at published finite ceiling"]
    B1["B1: lineage-carrier association<br/>COMPUTED through L12; signed persistence FAIL"]
    B2["B2: lineage changes future dynamics<br/>COMPUTED one-revisit mechanism at L4"]
    B3["B3: size persistence of dynamical response<br/>OPEN"]
    C1["C1: parent-selected native relation/metric<br/>OPEN"]
    C2["C2: held-out finite native curvature<br/>OPEN"]
    C2P["C2-PATH: L8 formation-order path association<br/>NEGATIVE at frozen sensitivity"]
    C3["C3: refinement and continuum correspondence<br/>OPEN for finite-curvature route"]

    RA["RGRL-A causal-volume realization<br/>ADOPTED / OPEN TO DERIVE"]
    RB["RGRL-B local metric deformation<br/>ADOPTED / OPEN TO DERIVE"]
    RC["RGRL-C constitutive lineage ancestry<br/>ADOPTED / OPEN TO DERIVE"]

    E1["WTC E1 common physical metric<br/>OPEN THEOREM HYPOTHESIS"]
    E2["WTC E2 complete stress and constraints<br/>OPEN THEOREM HYPOTHESIS"]
    E3["WTC E3 reciprocal back-reaction<br/>OPEN THEOREM HYPOTHESIS"]
    E4["WTC E4 invariant endpoint and coefficients<br/>CONDITIONAL theorem + open inputs"]
    EH["Einstein-Hilbert response<br/>EXACT conditional implication"]
    F["Independent physical discrimination<br/>OPEN"]

    B0 --> B1 --> B2 --> B3
    B0 --> C1 --> C2 --> C3
    C1 -. "first fixed candidate" .-> C2P
    C1 --> RA
    C1 --> RB
    C3 -. "required to promote the finite-curvature route" .-> RA
    C3 -. "required to promote the finite-curvature route" .-> RB
    B3 --> RC
    RA --> RC
    RB --> RC
    RA --> E1
    RB --> E1
    RB --> E2
    E1 --> E2
    RC --> E3
    E1 --> E3
    E2 --> E3
    E3 --> E4 --> EH --> F

    G2ID["G2 gravity = H1 identification<br/>SUPERSEDED"]
    G2GB["G2 Gauss-Bonnet record count<br/>EXACT bounded topology lemma"]
    G7["G7 corrected capacity index<br/>EXACT topology lemma"]
    X2["X2 fixed-complex back-reaction obstruction<br/>NEGATIVE"]
    H9["H9 record-path holonomy criterion<br/>DEFINITION / wrong-object correction"]
    H14["H14 carrier plaquette-holonomy selection<br/>DEFINITION / tested observable"]
    H15["H15 finite Z2 plaquette-holonomy independence<br/>NEGATIVE at tested ceiling"]
    AV["GL6AV retained-formation clock response<br/>EXACT partial dynamics"]
    PM["PMICS curvature-symbol capacity<br/>EXACT kinematic lemma"]
    PS["PMSR memory/source reciprocity<br/>EXACT commuting-parent lemma"]
    SD["SDCP 6 spatial + Ward + constraints<br/>EXACT conditional closure"]
    RI["RIEHB post-geometry back-reaction<br/>EXACT conditional mechanism"]
    BQ["GL6BQ finite-orbit non-Ricci residual<br/>AUTHOR NEGATIVE CLAIM; CUSTODY/AUDIT OPEN"]
    BQD["GL6BQ degree-six design sufficiency<br/>AUTHOR CONDITIONAL CLAIM; CUSTODY/AUDIT OPEN"]

    G2ID -. "superseded physical framing" .-> G2GB
    G2GB --> G7
    G7 -. "historical constraint" .-> C1
    G2ID -. "fixed-complex route" .-> X2
    H9 --> H14 --> H15
    H15 -. "rules out tested Z2 plaquette source shortcut" .-> C1
    AV -. "partial support" .-> B2
    AV -. "partial support" .-> RB
    PM -. "capacity, not realization" .-> RB
    PS -. "partial same-parent reciprocity" .-> RB
    SD -. "closure if physical premises hold" .-> E2
    RI -. "post-geometry mechanism" .-> E3
    RI -. "invariant endpoint" .-> E4
    BQ -. "forbids inserted isotropy" .-> C3
    BQD -. "conditional design route" .-> C3

    classDef established fill:#d8f3dc,stroke:#237a3b,color:#111;
    classDef adopted fill:#ffe8a1,stroke:#9a6b00,color:#111;
    classDef active fill:#dbeafe,stroke:#2563eb,color:#111;
    classDef negative fill:#fee2e2,stroke:#b91c1c,color:#111;
    classDef definition fill:#f3e8ff,stroke:#7e22ce,color:#111;
    classDef open fill:#eceff1,stroke:#59636e,color:#111;
    classDef superseded fill:#f1f5f9,stroke:#94a3b8,color:#64748b,stroke-dasharray:5 5;
    classDef custody fill:#fff7ed,stroke:#c2410c,color:#111;
    class B0,B1,B2,G2GB,G7,AV,PM,PS,SD,RI,EH established;
    class RA,RB,RC adopted;
    class X2,H15,C2P negative;
    class H9,H14 definition;
    class G2ID superseded;
    class BQ,BQD custody;
    class B3,C1,C2,C3,E1,E2,E3,E4,F open;
```

## Current adjudication

The repository contains more foundational work than the finite Zenodo capsule
shows. That work is scientifically relevant because it includes exact bounded
lemmas and failed routes, not only successful constructions. It does not,
however, erase the main logical gap:

```text
established finite record results
    != derived record-conditioned spacetime

(RGRL + WTC hypotheses) -> Einstein-Hilbert response
    != microscopic dynamics -> RGRL + WTC hypotheses
```

The premise-discharge program is therefore not a request to discard the
framework. It is a request to prove or falsify the arrows that the current
working theory explicitly adopted.

## Premise-discharge status

The source audit finds that none of D1--D3 or E1--E4 is fully discharged under
the program's evidence rule.

| Gate | Existing evidence | Decisive missing step | Status |
|---|---|---|---|
| D1 causal volume | RFCD exact finite `1+1` order; TROV operational preorder; same-parent projective causal-measure theorem; exact fixed-finite-ray obstruction | Parent-selected probe-complete `3+1` chronology, manifold/refinement, common probes, and independently calibrated four-volume | `OPEN` |
| D2 local deformation | PMICS curvature-symbol capacity; PMSR finite commuting reciprocity; GL6T finite lineage-gated response; separate charge, energy, and recoil pieces | One same parent with physical metric solder, complete local stress/source, temporal/current/contact operators, off-shell Ward packet, gluing, and common cone | `OPEN` |
| D3 lineage ancestry | FPMH matched finite KEEP/BREAK custody and GL6T forward response | Reconstructed geometry that prospectively follows lineage under a complete collateral ledger; the tested old-support reciprocal route is exactly zero in GL6BC | `OPEN` |
| E1 common metric | Conditional optical/clock/probe lemmas recorded in the emergence register | Same physical proper-time, transport, principal, and variational metric across matter, EM, records, clocks, and independent probes | `OPEN` |
| E2 stress/constraints | SDCP exact implication plus partial finite charge/energy/recoil results | Complete same-parent stress, contacts, ports, Ward identity, initial constraints, and propagation | `OPEN` |
| E3 reciprocal loop | RIEHB conditional macroscopic loop and finite upward-response pieces | One genealogy generated from records through metric/stress and back into every future sector | `OPEN` |
| E4 endpoint/coefficients | RIEC/RIEHB/WTC exact conditional Einstein-Hilbert classification | Physical antecedents, extra-channel exclusion, controlled corrections, microscopic or empirical coefficient custody; `G` is presently calibrated and `Lambda` remains free | `OPEN` |

The exact source anchors and evidence classes for these rows are in
`FOUNDATIONAL_CLAIM_LEDGER.tsv`. Register-only entries whose source lanes are
absent from this checkout are not treated as reverified theorem evidence.

## Existing results that constrain the next work

- **G2 is not a physical derivation.** Its exact Gauss-Bonnet identity survives
  as a bounded closed-surface corollary, while its definitional identification
  was superseded. G7 supplies the corrected Euler--Poincare capacity index and
  displays why unrestricted `2-chi` fails on a disk.
- **X2 and H15 matter.** They rule out two bounded shortcuts: internal
  back-reaction on the tested fixed complex and direct sourcing of the tested
  finite Z2 plaquette holonomy by record content. H15 is not a universal
  holonomy no-go.
- **GL6AV matters.** It provides genuine same-parent record dependence of a
  leading collective interaction, but its own theorem excludes a complete
  physical metric interpretation.
- **PMICS matters.** It proves that the candidate six-component pair-memory
  tangent has the correct local intrinsic-curvature quotient. It does not
  derive the physical tangent or its dynamics.
- **PMSR matters.** It proves a finite commuting-parent mixed-derivative
  reciprocity between observable pair memory and a physical-source response.
  It does not transport that result through the complete noncommuting F3
  parent.
- **SDCP and RIEHB matter.** They sharply reduce the macroscopic task once a
  common physical metric, complete source/Ward packet, initial constraints,
  coefficient sign, and tangent span have been earned. Their exactness is
  conditional on those physical inputs; it does not earn them.
- **GL6BQ may matter after custody is repaired.** Its author theorem says the
  authenticated finite orientation orbit leaves a non-Ricci residual and
  separately proves sufficiency of a hypothetical degree-six design. Missing
  manifest-listed packet files and the absent distinct hostile audit prevent
  either result from being promoted as independently verified here.
- **RGRL and WTC remain visible as assumptions.** Their conditional theorem is
  exact, but its physical antecedents remain the critical path.

## Immediate executable order

1. Finish the historical claim ledger and package crosswalk while preserving
   the completed finite calculations and their negative outcomes.
2. Retain the reconciled L10/L12 result as resolved finite association plus a
   failed signed persistence prediction; do not convert either into an all-size
   claim.
3. Retain the independently reproduced L4 first-revisit response as a mechanism
   result and design any B3 scale test prospectively.
4. Re-adjudicate the native relational-object question after the controlled L8
   formation-order-path null. Do not choose a richer graph after seeing that
   null without a new prospective derivation and freeze. This diagnostic branch
   need not block logically independent causal-volume or physical-deformation work.
5. Treat finite curvature as a finite test until a refinement theorem earns a
   continuum object; require that refinement only for routes that use the
   finite curvature object as a continuum antecedent.
6. Work through RGRL-A/B/C and WTC E1-E4 as explicit proof obligations. RGRL-C
   requires both a lineage intervention and an earned reconstructed geometry;
   E2 requires the common physical metric as well as the source/Ward packet.
   Keep negative outcomes in the same ledger.
