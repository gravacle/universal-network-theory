# Collective record formation: exploratory calculations

Date: 2026-10-28  
Status: **Exploratory research notes and reproducible toy calculations.**  
Source baseline: [`79a5ae3d689df5e4572d9f955d002a173baccdbf`](https://github.com/gravacle/universal-network-theory/commit/79a5ae3d689df5e4572d9f955d002a173baccdbf).

## Research question

Can record formation or retention depend on cooperation among several initially event-independent components, with the retained information residing in the joint system rather than in any isolated component?

This question arose while examining the upstream requirements of a records-to-electromagnetism-to-gravity account. An isolated-record construction is not assumed to be a necessary prerequisite for investigating collective formation. The starting ingredients, preparation, interactions, source, and query must nevertheless be declared explicitly. Starting with a population of completed records would be an initial-condition assumption, not a derivation of their formation.

These explorations do not establish that a single-record starting point caused previous project failures. Existing UNT work already contains multiple initial components. Population size, correlations, interaction structure, and formation protocol are distinct variables.

## Results at a glance

| Investigation | What was checked | Result and limit |
|---|---|---|
| Correlation-only quantum record | Exact two-component density matrices, fixed source-blind parity query, and evolution under a stipulated interacting Hamiltonian | The joint record is perfectly distinguishable in the ideal model while each component separately is uninformative. The supplied preparation, write, hold, and read are not derived from UNT. |
| Cooperative finite retention | Exact two- or eight-state continuous-time Markov evolution after a finite event-dependent write pulse | At dimensionless hold time 5, majority-read accuracy is 87.30% for three interacting components and 50.45% for three independent components. Interaction and preparation resources differ. This shows improved retention in an assumed model, not impossibility of isolated formation. |
| Native loop coexistence audit | Existing q4/F3 support, boundary, and ice-sector claims, plus two small Boolean confirmations | General retained `K` support can coexist with active `K`-gated `n` links. The raw finite q4 slab still has an empty global degree-two ice sector. A complete autonomous record-derived support/boundary/loop chain is not demonstrated by the reviewed documents. |

The first two are transparent illustrative calculations performed for this exploration. The third is a bounded source audit and confirmation of existing statements. None is a new UNT theorem, an external peer review, a physical implementation, or a derivation of electromagnetism.

## 1. Information retained only in correlations

The common blank is `|00>`. Supplied preparation and event-dependent writing produce `( |00> + |11> )/sqrt(2)` or `( |00> - |11> )/sqrt(2)`. Each local density matrix is `I/2` for either event, while a fixed joint `XX` parity read identifies the event perfectly.

The stipulated hold Hamiltonian is `H = XX + 0.3 ZZ`. Both written states are eigenstates, so their density matrices remain fixed during ideal holding. Exact algebra and numerical evolution agree: joint trace distance is one, each local trace distance is zero, and fixed-read contrast is one. A declared local phase-flip perturbation reduces contrast to `exp(-0.2 t)`; the ideal result is not a general noise-protection claim.

This demonstrates a possible joint record of a supplied event. It does not explain the origin of the event, quantum state space, gates, interaction, or readout, and it does not close physical control or work accounting.

Files: [model and interpretation](correlation_record_notes.md), [runnable calculation](correlation_record.py), [machine-readable results](correlation_record_results.json).

## 2. Cooperative retention after writing

The abstract binary variables have a supplied energy `H = -J sum_(i<j) q_i q_j - h sum_i q_i` and detailed-balance flip dynamics. Both event alternatives start in the same zero-field equilibrium for their model. A pulse `h = +/-1.5` writes for time 5, then the writer is disconnected and `h = 0`. A fixed majority query is used throughout. Parameters were fixed before calculation; there was no sampling, fitting, or optimization.

Readout total-variation distance is zero for indistinguishable output distributions and one for perfect distinction:

| Hold time | One component | Three independent | Three interacting |
|---:|---:|---:|---:|
| 0 | 0.899049413 | 0.985227863 | 0.902587063 |
| 1 | 0.330741796 | 0.478022748 | 0.861943410 |
| 5 | 0.006057747 | 0.009086510 | 0.746016113 |
| 20 | 0.000000001853 | 0.000000002780 | 0.434919474 |

The independent trio writes more strongly during the fixed pulse, while the interacting trio retains more of the distinction afterward. All finite positive-temperature cases eventually forget the event. The interacting equilibrium blank is already correlated but contains no information about the later event. This calculation does not derive those initial correlations from an uncorrelated preparation.

The main comparison uses the same number of components. It is not an equal-total-energy comparison: the coupling, equilibrium preparation, bath, writer, and query are supplied resources. No physical spin interpretation is assigned to the binary variables.

Files: [model and interpretation](cooperative_record_notes.md), [runnable calculation](cooperative_record.py), [machine-readable results](cooperative_record_results.json).

## 3. Native loop route and a corrected distinction

The [native-loop audit](native_loop_audit.md) separates three conditions: record-retained physical support, a nonempty global degree-two sector, and active microscopic dynamics that induce loop transitions.

An earlier conversational generalization that retaining support requires freezing every link flip was too broad. In the FH construction, the support projector fixes the program and `K`, not the active `n` word, and the qualified hold can retain the existing `K`-gated actuator. Switching off both flip terms belongs to the separate saturated FD carrier comparator. The audit cites the precise FH sections and replaces that overgeneralization.

Two genuine boundaries remain: the raw finite q4 slab has a degree-one boundary child, so it cannot satisfy degree two at every vertex; and saturated degree-four carrier transfer and degree-two ice are disjoint slices of the same binary incidence field. These statements do not establish an impossibility for every collective architecture.

The next native calculation is a finite coexistence witness with all three conditions in one declared preparation and parent. A supplied boundary or periodic completion must remain visibly listed as a premise.

## Reproduce the calculations

Recorded environment: Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0. Dependencies are recorded in [requirements.txt](requirements.txt).

From this directory:

```bash
python3 correlation_record.py
python3 cooperative_record.py
```

Each script writes its associated JSON file and includes numerical consistency checks. Use `--output PATH` to select a different output file. All times and model parameters are dimensionless; no physical lifetime or energy calibration is claimed.

## Claim boundary and continuation

No electromagnetic field, electromagnetic current, or Maxwell action is used as an explicit variable in these two toy models. This alone does not establish a physical implementation independent of EM. The mathematical interactions and control operations are stipulated, and neither toy has been mapped to the complete native UNT formation/custody conditions.

The saved results justify investigating collective encoding and retention mechanisms. They do not demonstrate a photon, physical charge, Maxwell dynamics, the observed alpha, gravity, a cosmological initial state, or the cause of earlier failures. Spin and cosmological interpretations remain deferred.

See [HANDOFF.md](HANDOFF.md) for the current decision, next assignments, source boundaries, and instructions for resuming the research from this record.
