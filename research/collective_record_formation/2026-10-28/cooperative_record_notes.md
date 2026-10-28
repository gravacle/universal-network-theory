# Cooperative record formation and finite retention

Date: 2026-10-28

Status: **Exploratory stochastic toy model. Not a UNT proof, a physical implementation, or a derivation of electromagnetism.**

## Question and outcome

Can interactions among several initially event-independent components improve their ability to retain a newly written distinction?

In this explicitly assumed finite model, **yes**. Three interacting binary components retain much more readable event information than three independent components at the same stated hold times. This is a finite-retention result. The isolated component also forms a record during the pulse, so this experiment does **not** show that isolated record formation is impossible or explain the project's earlier failures.

## Exact model and frozen protocol

The components are abstract binary variables `q_i = -1 or +1`, without a physical spin identification. Their supplied energy is

`H(q; h) = -J sum_(i<j) q_i q_j - h sum_i q_i`.

One component flips per transition, at the supplied detailed-balance rate

`w_i(q) = nu / (1 + exp(beta * [H(flip_i(q)) - H(q)]))`.

The fixed choices, made before executing the calculation, are:

- `beta = 1`, `nu = 1`.
- One component with `J = 0`; three independent components with `J = 0`; three mutually interacting components with `J = 1`.
- Both event alternatives start from the same zero-field Gibbs distribution for their respective model. No initial state contains information about the later event label.
- An event `x = -1 or +1` supplies a write pulse `h = 1.5 x` lasting `5 / nu`.
- After the pulse, the source is disconnected and `h = 0`. The interaction and thermal dynamics remain active.
- Hold times are `0, 1, 5, 20`, in units of `1 / nu`.
- The fixed source-blind read is the sign of `sum_i q_i`. Odd component counts avoid a tie convention. The read has no event-label input.

This is full finite-state propagation by `scipy.linalg.expm`, with two or eight states. It uses no random samples, fitted coefficients, parameter search, or selected trajectory.

## Computed readout contrast

The reported quantity is the total-variation distance between the two binary readout distributions, conditional on the two source events. It lies between zero (no distinguishability through this read) and one (perfect distinguishability).

| Hold time | One component | Three independent | Three interacting |
|---:|---:|---:|---:|
| 0 | 0.899049412685 | 0.985227863163 | 0.902587062847 |
| 1 | 0.330741795524 | 0.478022748404 | 0.861943409542 |
| 5 | 0.006057747292 | 0.009086509790 | 0.746016112989 |
| 20 | 0.000000001853 | 0.000000002780 | 0.434919473850 |

At hold time 5, the balanced classification accuracy of the same majority read is approximately **50.45%** for the three independent components and **87.30%** for the three interacting components. At hold time 20, the interacting model's accuracy is approximately **71.75%**. No success threshold was preregistered, so these are continuous contrasts, not pass/fail scientific gates.

The initial tradeoff matters: three independent components write a larger contrast by the end of the fixed pulse than the interacting components do. The advantage of interaction appears in subsequent retention. In the interacting model, changing one component of a fully aligned configuration costs `4 J`; that barrier is a consequence of the **supplied** interaction energy.

For these particular distributions, majority-readout TV equals the complete joint-state TV to numerical precision. The machine-readable result includes both, plus full initial distributions and checks.

## Resource accounting and interpretation limits

The primary controlled comparison is **three independent versus three interacting** components: same component count, source-field amplitude per component, pulse duration, temperature, attempt rate, and query. It is not an equal-total-energy comparison. The interacting system has three pair couplings and a different equilibrium distribution and preparation resource requirement. Those are physical inputs, not free benefits.

Comparing one with three components additionally changes the hardware count and total source-field coupling. That comparison cannot isolate interaction as the cause of improved performance.

The following are assumed, not derived: the binary state space, interaction energy, bath, stochastic transition law, source event, pulse timing, initial equilibrium preparation, and majority query. A physical implementation would need to justify them. No electromagnetic field, electromagnetic source current, or Maxwell action appears in the mathematical model, but that alone does not establish a physical realization independent of electromagnetism.

The interacting zero-field Gibbs blank already contains intercomponent correlations. It contains no information about the subsequent event label. Thus this experiment demonstrates writing a new event-dependent distinction into a correlated substrate; it does not derive the substrate's correlations from an initially uncorrelated collection.

All three finite positive-temperature chains are irreducible. They eventually return to the same event-independent equilibrium, so their information about the event tends to zero. This is finite retention, not permanent memory or an infinite-system phase result.

The experiment supports the mathematical possibility of **cooperation improving retention after formation**. It does not yet demonstrate that the UNT native formation law supplies this interaction, that only collective systems can form records, or that electromagnetism emerges from record formation. The next justified UNT task would be to identify whether an already permitted interaction produces an analogous retention barrier, with its resources and control ports explicitly accounted for.

## Reproduction and checks

Run:

```bash
python3 cooperative_record.py
```

Dependencies used: Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0. The script writes `cooperative_record_results.json` alongside itself unless `--output` is supplied.

The script checks probability normalization and nonnegativity, generator conservation, zero-field equilibrium stationarity, detailed balance, and that the fixed query does not increase total-variation distinguishability. Each numerical tolerance is `1e-12`. All checks passed.
