# Finite path dynamics from a common product blank

Date: 2026-10-28

Status: **New, explicitly declared finite path instantiation. Not a reproduction of the unavailable GRA-CH theorem, a record-formation certificate, or an EM result.**

## What was done

We propagated a common all-empty link state under a finite simultaneous interacting Hamiltonian, retaining the endpoint terms. This avoids preparing an interacting ground state or thermal ensemble in advance. It tests whether an explicitly supplied shared interaction generates joint correlations from an initially uncorrelated link blank.

The complete fixed grid was executed:

- Simultaneously present binary link counts `M = 1, 3, 5, 7, 9, 11, 13, 15`.
- Local tunnelling amplitude `h = 1`, fixed as `M` changes.
- Shared degree-penalty coefficients `Ud = 0, 1, 4`, fixed across sizes.
- Reported times `t = 0, 0.25, 0.5, 1, 2, 4`, in units with `hbar = 1`.
- Initial state: the product `|n_1=0,...,n_M=0>`.
- Frozen ancestry gates `K_i = 1`; their preparation and retention are model inputs.

No parameter fitting or post-result grid selection was performed. Sparse matrix-exponential action was used; no dense Hamiltonian was constructed. The largest state vector had `2^15 = 32,768` components.

## Declared Hamiltonian and boundaries

For a path of `M` links and `M+1` vertices, the declared hold is

`H = -h sum_i X_i + Ud[(n_1-1)^2 + sum_(i=1)^(M-1)(n_i+n_(i+1)-1)^2 + (n_M-1)^2]`.

Here `n_i=(1-Z_i)/2`. Equivalently,

`H = -h sum_i X_i + (Ud/2) sum_i Z_i Z_(i+1) + (Ud/2)(Z_1+Z_M) + Ud(M+1)/2`.

For `M=1`, both endpoint contributions act on the same link. They are counted twice, as the original degree formula requires.

The source audit permits fixed local tunnelling for a serial composition. The **simultaneous shared-interaction hold and the finite endpoint prescription above are explicit choices in this new instantiation**. They must not be presented as verified details of the missing CH source theorem.

`M` is not automatically the native adjacent-layer width `N`, composition-layer depth `L`, or a number of qualified records. In particular, this is not the dense-family limit with local amplitude `h_N=Omega/N`. The number of links, total hardware, total coupling count, and initial energy grow with `M`. There is no equal-total-resource comparison across sizes.

Odd link counts were selected prospectively because a path then has an even number of vertices and can admit the classical degree-one matching. An even-link path would instead have an unavoidable perfect-matching parity obstruction. Endpoints have not been silently discarded or replaced by periodic boundaries.

## Matched independent control

For every `M`, `Ud`, and time, we also calculate the exactly factorized control

`H_control = -h sum_i X_i + (Ud/2)(Z_1+Z_M)`.

It keeps the same one-body endpoint fields while removing only the shared `ZZ` term. Its connected covariance between distinct links is identically zero for the product initial state, at every size and time. Each individual occupation is computed analytically from

`p_i(t) = h^2/(h^2+a_i^2) * sin^2(sqrt(h^2+a_i^2)*t)`,

where `a_1=a_M=Ud/2`, with both fields added when `M=1`; interior `a_i=0`.

For `Ud=0`, all occupations reduce to `sin^2(t)` and the full propagated model agrees with this independent result. This control comparison is needed because simply changing `Ud` to zero also removes the endpoint fields.

## Completed results

Define the connected occupation covariance as

`C_ij = <n_i n_j> - <n_i><n_j>`.

The interacting holds generate nonzero connected covariance from the product blank. The matched independent controls remain factorized. Thus these finite results demonstrate actual joint effects of the **supplied shared interaction**, rather than an effect of merely having more independently evolving links.

Selected results at `t=4`:

| Ud | M links | Mean occupation | Mean nearest-neighbor covariance | End-to-end covariance |
|---:|---:|---:|---:|---:|
| 1 | 3 | 0.331744835 | 0.076549544 | 0.069245060 |
| 1 | 7 | 0.443143473 | 0.123981374 | 0.015991758 |
| 1 | 11 | 0.446558548 | 0.120375649 | 0.000825714 |
| 1 | 15 | 0.448330676 | 0.118857313 | 0.000000043 |
| 4 | 3 | 0.052509226 | 0.028118600 | 0.026375149 |
| 4 | 7 | 0.067038236 | 0.035157782 | 0.002739374 |
| 4 | 11 | 0.118560486 | 0.080482153 | 0.019137478 |
| 4 | 15 | 0.140278028 | 0.094659664 | 0.013009997 |

At `M=15,t=4`, the matched independent controls have mean occupations `0.597010608` for `Ud=1` and `0.502080807` for `Ud=4`, with all distinct-link connected covariances exactly zero. The full `Ud=0` model has mean occupation `0.572750017` and nearest-neighbor covariance consistent with zero within numerical error.

The connected staggered variance per link is

`V_stag/M = sum_(i,j) (-1)^(i+j) C_ij / M`.

At `M=15,t=4`, it is `0.244707435` for `Ud=0`, `0.091780699` for `Ud=1`, and `0.022565139` for `Ud=4`. The nearest-neighbor covariances at this selected time are positive. These source-off trajectories from the blank must not be relabelled as an antiferromagnetic ground-state or ordered-phase calculation. The dynamics are unitary and need not yield monotonic behavior in size or time.

The JSON includes every size and reported time, each link's occupation, the averaged connected-covariance profile at every separation, center-to-link covariances, center-to-near-end covariance with the exact distance stated, end-to-end covariance, and the staggered variance both including and excluding local diagonal variances.

## What this establishes and what it leaves open

The finite calculations establish that the declared simultaneous interacting hold can create joint correlations from the common link blank. Such effects already occur with three links. They provide a controlled distinction between independent scaling and shared-interaction dynamics.

They do not establish a retained readable record of an input event: only one common blank trajectory was evolved, and no two-event write/read mission was tested. Correlation alone is not a full record certificate. They also do not derive the interaction, the support, the ancestry gates, a Maxwell field, a thermodynamic phase, or an electromagnetic identification.

The specific time window `t<=4` and maximum size `M=15` do not exclude slower behavior or longer correlations at larger sizes or times. No extrapolation to millions of links is justified by this sweep. The all-size factorization statement applies to the independent control only.

The physical support, fixed ancestry gates, their initial resources, and the simultaneous hold are supplied. For this newly declared family, the prepared blank has initial energy `Ud(M+1)` and the total resource count changes with size. Connecting this hold to an actual native formation procedure remains a separate task.

## Numerical verification and reproduction

Run:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 declared_path_dynamics.py
```

The script uses Python 3.12.14, NumPy 2.3.5, and SciPy 1.17.0. It writes `declared_path_dynamics_results.json` alongside itself, unless `--output` is supplied.

Over the complete sweep, the maximum norm-squared error was approximately `3.97e-13`, and the maximum absolute energy-conservation error was `1.30e-11`. The independently solvable `Ud=0` and `M=1` cases matched their analytic controls within the script's `1e-9` tolerance. The slowest individual state propagation took approximately 1.51 seconds in the recorded environment; this is a local runtime observation, not a scaling guarantee.

An independent dense calculation built the expanded Pauli Hamiltonian directly, rather than the sparse bit-counting construction. It checked 18 small-system cases at M=1,3,5, Ud=1,4, and times 0.5,1,4. Occupations and connected covariances agreed within 6.37e-15. See [validate_declared_path.py](validate_declared_path.py) and [scaling_validation.json](scaling_validation.json). This check uses dense matrices only for those small validation systems; the scaling sweep uses sparse evolution.

## Source custody and the all-size control

The [FPMH composition theorem, sections 2–4](https://github.com/gravacle/universal-network-theory/blob/79a5ae3d689df5e4572d9f955d002a173baccdbf/LANE_CROSS_RFT_MGFT_FINITE_PAIR_MEMORY_HANDOFF_V001/COMPOSITION_THEOREM.md) explicitly constructs serial pair memory for every finite number M of handoffs. Its postformation gate terms commute. For fixed memory eigenvalues and initially product links, their propagator factorizes at every size. Consequently, merely adding independent copies cannot create connected cross-link correlations, including at a billion links. This is an exact result for that gate-only preparation and dynamics, not for every interacting record model.

The [F3 microscopic action, sections 2–3](https://github.com/gravacle/universal-network-theory/blob/79a5ae3d689df5e4572d9f955d002a173baccdbf/LANE_GRA_BS_F3_QIRN_MICRO_ACTION_V001/MICRO_ACTION.md) supplies the degree-penalty interaction form. Its original dynamics are an ordered product of slabs and use h_N=Omega/N, where N counts vertices per adjacent layer. The simultaneous open-path hold studied here is a declared extension; it is not silently identified with that dense/slab limit.

The [model status](https://github.com/gravacle/universal-network-theory/blob/79a5ae3d689df5e4572d9f955d002a173baccdbf/MODEL.md) and [experiment register](https://github.com/gravacle/universal-network-theory/blob/79a5ae3d689df5e4572d9f955d002a173baccdbf/GRAVITY_EMERGENCE_EXPERIMENT_REGISTER_V001.md) report a serial collective-phase result. The cited controlling GRA-CH directory was absent from the complete baseline root tree and its named THEOREM.md and RESULT.md were unavailable. This calculation therefore does not reproduce that claim or assign its missing boundary conditions.

The matched independent control here changes a Hamiltonian term. It is not the native KEEP/BREAK operation. Likewise, total connected staggered variance contains local diagonal fluctuations even in an independent model; the off-diagonal occupation covariances are the specific joint-effect evidence.

## Figure and next question

[Scaling figure](scaling_correlations.svg) shows the predeclared t=4 slice without fitting or extrapolation. [render_scaling_plot.py](render_scaling_plot.py) reproduces it with Matplotlib.

The next causal test is to compare two matched retained-memory routes under one full K-dependent hold: full KEEP versus moving one formed relation into quarantine. Start links in the same blank and keep all later sources disconnected. The difference in a distant fixed link read would test a response to the changed local active memory. It would go beyond correlation generation, while still leaving the charge, gauge, and field-dynamics requirements of EM open.
