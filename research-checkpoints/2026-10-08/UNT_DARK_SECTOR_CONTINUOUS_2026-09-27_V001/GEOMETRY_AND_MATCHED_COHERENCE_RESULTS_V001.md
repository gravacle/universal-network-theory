# Geometry and matched-coherence results

2026-09-28. Continuation of frontier V026. These are small local calculations
and analytical results in the existing network/carrier model, not new L6/L8
production calculations or an astronomical fit.

## Scientific outcome

We now have a general geometry-local rule for the leading motion of a
uniformly distributed carrier, plus controls showing that the relevant link
correlations change that motion while classical graph/record statistics,
mean energy, and energy variance are held fixed.

This advances the proposed explanation from “network structure matters” to
an explicit question we can calculate: **which spatial pattern of link
correlations does record formation create, and what motion does that pattern
produce?** No extra dark component or new attractive interaction was inserted
into these controls. The unchanged native Hamiltonian drives their evolution.

## 1. The motion law extends beyond the original four-site example

For a finite simple bipartite possible-edge skeleton with V vertices, consider

    H = D(n) - sum_e h_e X_e - sum_e J_e n_e A_e.

Here n_e is link occupation, X_e flips that link, A_e connects its two carrier
endpoints, and D is any real diagonal network energy. The initial carrier is
uncorrelated with the network and uniform, I/V. The network density matrix
can be arbitrary. Units have hbar=1.

Orders one through five in every site probability vanish. The sixth-order
term is

    P_v(t) = 1/V + t^6 <K_v> + O(t^7),

    K_v = 1/(80V) sum_{a-b-c wedges}
          h_ab h_bc J_ab^2 J_bc^2
          (2 delta_vb - delta_va - delta_vc) X_ab X_bc.

Every unordered adjacent pair of edges is counted once. Each pair contributes
twice at its common vertex and minus once at each outer endpoint. Summing
over all vertices gives zero: this is redistribution, not particle creation.
The expectation of the paired-flip operator is a link coherence, not an
occupation count or proof of entanglement.

The predeclared exact-integer census passed all **20 geometry/coupling cases**:
86 site identities and 430 lower-order zero identities. It includes paths,
stars, cycles, disconnected components, K2,3, heterogeneous couplings, vertex
relabeling, and several diagonal-energy controls. The run took 4.04 seconds;
the largest matrix dimension was 384. There were no numerical tolerances in
these integer identities.

The arbitrary-graph claim rests on a separate derivation, not extrapolation
from those 20 examples. Closed-carrier-walk classification reduces all terms
through order six to local supports. A 52-case exact word certificate and an
independent multiset-word enumeration confirm the remaining cancellations.
The review also checked additional initial-bit and diagonal-energy cases.

The branching tests matter: the former ordinary-Laplacian formula works on
paths/cycles but needs correction at a branch. The general form is

    W_e = h_e J_e^2 X_e,  S_v = sum_{e incident v} W_e,
    K_v = sum_{u adjacent v} W_uv (S_v-S_u)/(80V).

These are signed operator weights, not ordinary positive diffusion weights.
The diagonal energy is absent from this leading coefficient but still affects
state formation and later-time motion. Thus removing it from this formula
does not remove records from the full dynamics.

Details: [derivation](</Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/geometry_coherence_law/ANALYTICAL_DERIVATION.md>),
[frozen protocol](</Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/geometry_coherence_law/PROTOCOL.md>),
[results](</Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/geometry_coherence_law/RESULTS.json>),
[independent review](</Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/geometry_coherence_law/REVIEW.md>).

## 2. Motion differs even with classical statistics and energy matched

First, in all 12 inherited native preparations, we isolated each of the four
adjacent-link coherence sectors and reversed its phase. Each plus/minus pair
has the same complete graph/record occupation probabilities, record reduced
state, and complete mean energy. All 48 contrasts are numerically resolved
at each of times 1, 2, and 4. At time 0.5, 30 are resolved and 18 remain below
the declared 1e-10 reporting floor.

This prospective calculation saved all 108 control density matrices and
predictions before propagation. Its 2,160 prediction checks and 5,582 run
checks passed. Independently evaluated primary readouts agree within
2.10e-14. Propagation took 0.335 seconds, with peak self RSS 80.5 MB.

The first controls change energy variance, which was explicitly measured.
We therefore strengthened the comparison with an additive mathematical
construction: mix two coherence sectors so their second-energy-moment shifts
cancel. The weights depend only on initial coherences, not on desired motion.
All six sector pairs and all 12 preparations were retained.

The resulting **72 matched pairs** share:

- Every initial classical graph/record probability and the full record marginal.
- The same full mean energy, second energy moment, and energy variance.
- The same carrier initialization and the same subsequent Hamiltonian.

All 72 still have a resolved record-site motion contrast at time 4. The
half-difference between the two controls ranges from 1.03e-8 to 2.30e-5 in
absolute probability. Raw accumulation changes sign between the two controls
in 26 of 72 cases; a universal sign reversal is not claimed. At earlier times
some contrasts remain unresolved. The full 288-comparison census is retained.

This construction passed 5,544 checks. The maximum energy-matching residual
was 5.69e-14. It took 0.527 seconds and required no new propagation: linear
evolution allows the saved readouts to be mixed exactly as the states are.
It is a **post-run constructive result**, not a fresh blind validation run.

One inherited example (formation 2T, finite age 2T, observation time 4,
mixture of x/y and u/v sectors) gives:

| State | Record-site probability change | Mean energy | Energy variance |
|---|---:|---:|---:|
| Common dephased baseline | -1.26801198e-6 | 12.28095833925 | 0.277191878989 |
| Matched plus mixture | +2.09905793e-5 | 12.28095833925 | 0.277191878989 |
| Matched minus mixture | -2.35266033e-5 | 12.28095833925 | 0.277191878989 |

The mixture weight is 0.8041480748 on the x/y sector; the other sector carries
the opposite phase. All cases, not just this example, are in the receipt.
At this finite time the leading t^6 term alone even has the opposite sign
from the complete plus readout. Consequently finite-time conclusions use
the propagated evidence, not an uncontrolled short-time extrapolation.

The two mixtures average to the baseline, so their opposite baseline-relative
responses follow from linearity. The useful finding is that the response is
nonzero under the stronger matching, together with the explicit local rule
identifying the relevant coherences. Matching two energy moments does not
match the entire energy distribution or every record-conditioned moment.
Indeed, independent review finds a changed q-weighted second moment in all
144 mixtures, with absolute changes up to 9.284e-5. The matching claim is
for the unconditional full-system moments, not a stronger sector-by-sector
equivalence.
Both controls also have the same preparation-energy difference from the
original formed state (0.004323629236 in this example); preparation is not
assumed free or naturally occurring.

Details: [initial protocol](</Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/pair_phase_motion_control/PROTOCOL.md>),
[initial evidence audit](</Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/pair_phase_motion_control/REVIEW.md>),
[moment-matching construction](</Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/pair_phase_motion_control/MOMENT_MATCHED_CONSTRUCTION.md>),
[all matched results](</Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/pair_phase_motion_control/MOMENT_MATCHED_RESULTS.json>),
[independent moment-matching review](</Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/pair_phase_motion_control/MOMENT_MATCHED_REVIEW.md>).

## 3. A useful size result without a large calculation

For the native complete-bipartite skeleton K_N,N, V=2N and h=Omega/N, the exact
largest possible sixth-order site coefficient is

    ||K_v|| = Omega^2 J^4 (N-1)/(80 N^2).

Relative to the initial per-site probability 1/(2N), the sharp bound is

    Omega^2 J^4 (N-1)/(40N).

Thus size alone does not force the maximal relative leading response to
vanish. This is an attainable operator bound, not a prediction of the actual
formed state. Conversely, identical pair coherence everywhere on this regular
skeleton cancels the leading redistribution exactly. Spatial variation is
therefore central to this mechanism.

The derivation includes a finite-N remainder bound. It does not exchange the
short-time and large-size limits or claim a finite-time macroscopic law.
No full native N=3 state calculation was run.

## Scientific interpretation and next bridge

Continuation: the formation test proposed below has now been completed; see
[native formation results](</Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/formation_coherence_causality/SCIENTIFIC_REPORT.md>)
and frontier V028.

The mechanism is now more specific: **spatially organized link coherence can
change transport without changing the initial classical network distribution
or its first two energy moments.** This is relevant to the user's proposed
network explanation of apparent dark-sector behavior: the explanatory variable
can be relational organization rather than an added matter/energy component.

The next highest-leverage bridge is native formation: derive which record
histories produce which spatial coherence patterns, then predict the resulting
transport without selecting its sign. The larger-geometry question should be
posed in terms of that measurable pattern, rather than just increasing matrix
size. A gravity or expansion interpretation additionally needs an independently
defined distance/time observable and the corresponding quantitative law.
The present outputs are probability transport in the stated model; they do
not yet supply a galaxy rotation curve or cosmic expansion prediction.

## Evidence identities and execution scope

SHA-256 identities:

- Geometry freeze: `afdb3999fb76cf56790e1939779fe4f2002a3a53213b33dfe6f5eaaeb1e63aac`.
- Geometry results: `33e219950a0d29663ccdfa6145eca5e4b91599ce17beffb31141e45130445290`.
- Pair-control freeze: `cd26dcdb8896187145a787bc1a22efc84affe8fbf599b6c44593afaea55c7be9`.
- Pair-control predictions: `14c03cc767e43110e473330063691044ad42e0ba2cf1e23b3eface749ccde645`.
- Pair-control results: `2b4e9a961d0ea5bcefaa30ec099a32a38f1d572f437ebebec942950651145e37`.
- Moment-matched results: `1d3d3e6818526f93714e84e1bec5bf8a08954bdef243966fc39986d9585d666d`.

Frozen receipts were not edited. Work used small single-thread local jobs and
saved outputs; no checkpoint infrastructure was needed. No remote dispatch,
new packages, VM, L8 work, GitHub publication, or system settings changes were
performed. All calculations described here have completed.
