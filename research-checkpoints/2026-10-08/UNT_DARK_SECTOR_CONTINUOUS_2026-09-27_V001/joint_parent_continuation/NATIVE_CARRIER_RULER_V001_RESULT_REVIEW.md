# Native carrier ruler V001: independent result review

2026-09-29. **Accepted within the declared native one-carrier, prepared-graph sector.** No load-bearing operator, numerical-method, custody, or saved-readout defect was found. This is an independent **post-run** implementation/result audit; the earlier analytical review was pre-run, but this reviewer did not finish implementation preflight before execution. No propagation, fitted parameter, new input state, or altered threshold was used here.

## Authenticated evidence

The seven input files match every SHA-256 in the freeze. Result configuration and parameters match that freeze; the canonical payload digest and outer freeze digest match their stored values. All 44 cases (two sizes × two graph preparations × eleven declared times), 22 method rows, four frozen spectral controls, six Schur controls, and 513 distinct original checks are retained. Every original check passes its original tolerance.

| Artifact | SHA-256 |
|---|---|
| `native_carrier_ruler_v001.py` | `00a09a8c3caffc0ffe8df76a54787ddc010ec4d5196bedf773c34258d656b252` |
| Numerical protocol | `b938c0fa340f368717ee89b4b87a7d70ed5d0a501d0a8650dd8baf28dbbf59a1` |
| Analytical pathway | `4277871cd49f7e45169f3fd7db0b5d49b9b66651f6b4ac257d794a5230254db8` |
| Analytical review | `516f810a366fe9f1a381c0a74fc7bec51f74b4f40f5aeeb29c32c33b4ebd6fad` |
| `NATIVE_CARRIER_RULER_V001_FROZEN.json` | `e507c9efbf07d5a3106cf96c4bbaa4f6940e68dd93d308a5e79ccc8b13c43abb` |
| `NATIVE_CARRIER_RULER_V001_RESULTS.json` | `f170be1dc580c2c0c2f3ebfd1740d1e728a69970c5ba4acf1d3dfc0a25b5713b` |
| Canonical result payload | `03547490d2bff92f0f4aa92c212323c072e7529499f5998bb8d1f852ba78512f` |
| Independent audit source | `048877c7322564564c8a543438a0e5ccf5fd2ee7b8cf18f145aa4717f9848279` |

The other three exact source identities are retained in `NATIVE_CARRIER_RULER_V001_AUDIT_DATA.json`. Hashes establish artifact identity, not scientific truth by themselves.

## Implementation and independent recombination

The complete final source and protocol were read. The inherited diagonal includes the full degree-dependent current-square term, since one-carrier `J_uv²=P_u+P_v`; it does not replace that term with the square of a mean current. Hopping and flip signs, the old-reader mapping, the tree11 end-anchor placement, and all absolute energy offsets agree with the analytical note. With the declared orientation, `〈nJ_uv〉=2 Im Σ n conj(ψ_u)ψ_v`; current is `t〈nJ〉`, negative at the left endpoint and positive at the right endpoint. The saved continuity convention therefore agrees with the Hamiltonian.

The tensor/bit action and independently assembled row-sparse action implement the same operator without a dense 3072-square matrix. Gershgorin enclosure, shifted Chebyshev/FFT expansion, conservative Bessel-tail/alias envelopes, shifted Taylor product-tail bound, and center phases are consistent. Their exact-arithmetic tail bounds are not misrepresented as floating-point error guarantees. The N2 eigensolver and frozen 4/6-node controls supply additional checks, not independent new physical models.

`native_carrier_saved_audit_v001.py` imports no numerical model, runs no propagator and writes no files. It authenticates the artifacts and independently recombines **2,848 saved-data arithmetic checks**: complete census, population sums/readout mappings, every edge-current flow, continuity, all component-energy sums, initial/conserved energies and variance, probability-set inclusions, leakage-bound formulas, native/frozen state bound, C4/C6 closed-form amplitudes, finite-time ratios, method-to-case references, Taylor and Chebyshev log-bound arithmetic, and Schur self-energy formulas. Results are saved in `NATIVE_CARRIER_RULER_V001_AUDIT_DATA.json`.

| Quantity | Maximum absolute discrepancy |
|---|---:|
| Original two-method state agreement | `2.3010919299514992e-14` |
| Independently recombined current continuity | `1.5213524884316598e-14` |
| Component-energy sum against saved total | `1.1013412404281553e-13` |
| Mean energy against exact initial value | `5.897504706808832e-13` |
| Variance against 1.5 | `2.114575181622058e-11` |
| C4/C6 full return amplitude | `2.7689457488368945e-15` |

The variance is the largest original residual and is far below its frozen **absolute** `2e-8` gate. The audit does not reconstruct raw state vectors from observables; those vectors are not stored. Thus its independent state-level evidence is source/operator analysis plus authenticated two-method checks, not an unperformed third propagation.

The worker reported **8.81425075000152 seconds** and **46,579,712 bytes peak self RSS** (about 44.42 MiB). This is process-self memory, not independently measured aggregate job memory.

## What the native calculation establishes

The added two-vertex path changes an actual inherited carrier's transfer while preserving a substantial probability of the prepared connectivity. This is stronger than the earlier scalar-probe comparison: the carrier and its degree-sensitive term are in the resident native Hamiltonian. The initial localized-carrier energy cost is still explicit: `21.5→31.5` for the cycle and `15.5→25.5` for the tree, exactly **+10**, with variance 1.5 in each preparation. The calculation compares separately prepared fixed-N sectors; it does not dynamically perform that growth transition or supply its work.

At the **eleven sampled times only**, the probability minima are:

| Preparation | Exact prepared graph | Connected graph (not necessarily the original graph) |
|---|---:|---:|
| N2 cycle | 0.9001177316 | 0.9943152560 |
| N2 tree | 0.8705507235 | 0.8978118946 |
| N3 cycle | 0.9216635877 | 0.9974353215 |
| N3 tree | 0.9061481768 | 0.9302920614 |

These are observed sample minima, **not continuous-time lower bounds**. The general graph-leakage bound gives only `P(exact graph)≥max(0,1−τ²)`, becoming uninformative at `τ≥1`. The actual sampled survival therefore matters; a vacuous bound does not establish graph destruction. Exact graph, retained backbone and arbitrary connectivity are distinct observables, and their saved inclusion inequalities hold. Likewise, high graph survival does not make the full state identical to the frozen-graph state: at age4 the N3 state differences are 0.36247 (cycle) and 0.33362 (tree).

The short-time derivative identities pass exactly within the numerical operator checks: subdivision removes the direct prepared edge, but an incidence flip followed by a carrier hop yields unconditional reader probability `τ⁴/144+O(τ⁶)`. Requiring return to the exact prepared graph instead gives a `τ⁶` leading probability, with both cycle three-hop routes retained. These are Taylor coefficients, not finite-time laws. At the smallest positive sample `τ=1/32`, the unconditional `P_reader/τ⁴` is 0.00690247/0.00691685, close to but not forced to equal `1/144=0.00694444`; the full later ratios remain in the artifact.

Finite-time behavior is not a uniform slowdown. At age1 the cycle reader probability changes from 0.17486058 (N2) to 0.00162277 (N3), and the tree from 0.20106941 to 0.00058463. At age4 the N3 cycle reaches 0.72828600 versus N2 0.13886595; the N3 tree reaches 0.30016531 versus N2 0.16033450. Subdivision reorganizes coherent transfer, arrival structure and recurrence. It is not merely a constant rescaling of an old propagation clock.

The frozen-graph Schur response retains its energy dependence and poles at carrier energies 1 and 2; shared spectral endpoints do not make the old edge and subdivided path operationally identical. Nothing in this calculation yet identifies physical distance, photons, a universal metric, galaxy gravity, or populated record-formation dynamics. Its constructive output is a native, work-accounted transport diagnostic that a proposed physical geometry must now respect.
