# Independent review of the exact shell inertia result

The separately versioned exact-integral kinetic kernel passes the four prospectively fixed discrete checks. This resolves the observed quadrature accuracy defect for those test cases; it does not establish continuum accuracy or repair the previous full trajectories. Review was limited to source, saved aggregates and file hashes. No producer was imported or rerun.

## Evidence and custody

The complete kernel, wrapper and protocol had independent source-only approval before execution. The saved result is `SPHERICAL_EXACT_KINETIC_ORACLE_V001_RESULTS.json`, SHA-256 `738dd1f841cfa1648f178c4dcbc556f5333b0e560ab3daae82908cd3f715250b`. Its intent is SHA-256 `519974b2736eb77abe8d41dfabd062c1c4f18f97c9874014a46b960563abee1d`. The result's recorded canonical payload digest is `5f30a14ee7325be158e8da8640cc43432b516fbcd20619dbe88b887793f411c5`.

The reviewer independently rehashed the result, intent and every file named in the result's input map, and matched the displayed hashes to that map and the reviewed source identities. The result reports successful end-of-run custody verification and no runtime or custody exception. This review did not independently recompute the canonical payload digest or the numerical comparisons; the authenticated source and saved comparison records are the basis of the interpretation.

Reviewed kernel SHA-256: `78765ef0e2d29c044642b1d944682a81ff5d48b22de9d0cb16b7bc47b9c7e11a`.

Reviewed wrapper SHA-256: `929565d2c72971fe3e1d3e856a5417a8d0e39948f7338bb55b040d2464e5d66e`.

Reviewed protocol SHA-256: `609e9fdcdde1c4b347dc772cf55420350b093902c53ede4c6f0fea2265d0e317`.

## What passed

The single-origin, uniform, graded and thin-annulus cases each completed once under one fixed closed-form method. No quadrature order was selected from earlier outcomes. All 585 recorded scalar comparison entries passed, with zero failed groups. These entries are implementation controls, not independent physical tests.

| Saved control | Maximum normalized residual | Frozen tolerance |
| --- | ---: | ---: |
| Arithmetic comparisons | 3.4831e-16 | 2e-11 |
| Fixed-momentum derivative and associated work comparisons | 6.7060e-10 | 2e-6 |
| Matrix against exact rational integral | 5.5511e-17 | 2e-11 |
| Supplied-velocity geometric force against exact rational derivative | 1.7347e-18 | 2e-11 |

The literal assembled matrices had positive exact-rational LDL pivots. Their saved infinity-norm condition numbers range from 1 to 4.2059, and the largest relative forward-error bound is 1.3118e-16. These certificates concern the four actual assembled matrices, not arbitrary meshes. The unchanged origin, harmonic-force, fixed-momentum derivative, affine-null and nonzero-velocity instantaneous work controls also passed. The analysis reports approximately 0.086 seconds and 35,946,496 bytes peak self RSS.

## Interpretation and remaining work

The earlier quadrature result remains failed and immutable at SHA-256 `bb9810e5d392e2ce7ee3ae3d2bdf48abbe7576bd349c2d2928e77fb332228327`. Its 35 failed groups were confined to lower-order integral accuracy and downstream comparisons; its finite-difference and literal-matrix solve controls passed. The new rational-polynomial implementation removes the quadrature approximation while preserving the same finite-shell kinetic action and canonical signs. It does not reclassify any earlier failed order.

The next justified step is separately reviewed integration into the spatial solver, followed by characteristic/stability, shell-crossing, energy, time-step, domain and spatial-convergence tests. The instantaneous work identity is not a time-evolved conservation test. No halo, lensing, merger, full metric, native formation, observational or DM/DE-replacement claim follows. All promotion flags in the saved result remain false, all 11 mandatory scientific lanes remain open, and the separate failed thermal audit is unaffected.
