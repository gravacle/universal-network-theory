# Native thermal packet: independent saved-result review V001

2026-09-29. Accepted within the stated finite native-sector scope. No producer, propagator, time integral or eigensolver was rerun.

## Exact identities and complete census

- Result: `NATIVE_THERMAL_PACKET_V001_RESULTS.json`, SHA256 `8531cd6f2cf7d60e4b981428c9f80b55ee76b23f17bd4ab91c0e435894010538`.
- Freeze SHA256 `4a6ed3c387bc87961264806ef630f988199bfdde0b3f9d81fb53b11a2c40f0b3`.
- Payload SHA256 `a0466fe81368ca2dedc4763e58213f4321998507a86f268b04013dcfb7222c23`.
- Producer source/protocol match the accepted `380e7364...` / `08b9d077...` bytes exactly.

All four preparations, 44 held states, four complete 110x110 complex correlations, 264 causal response blocks, 216 complete four-edge probe rows and 72 integral controls are retained. Each record sector has 48 resolved energy groups and all 1,128 distinct group pairs for each of its two states; no line is omitted by the reporting floor. Producer: `COMPLETE`, 3,794 checks, no failures, 0.487642 seconds and maximum 96,108,544 bytes self RSS.

Independent audit authenticated 17 files, two manifests and 22 member occurrences. A separately assembled basis-row Hamiltonian/local-energy/current representation was applied only to the saved state vectors. Every local energy/current, incidence/population observable, connected equal-time covariance, source double-commutator, absolute storage/feedback ledger and energy variance was reconstructed. The full two-time arrays reproduce all response blocks, equal-time blocks and nonstationary work identities. Probe connected/dephased differences, complex Hermiticity, Schwarz bounds, norm bounds, age-independent dephased values, line ratios and complete group census pass.

The audit has 191,106 passing arithmetic entries, maximum error 1.592e-12. It checks saved Gram eigenvalue certificates by trace/Frobenius moments and their declared tolerances, not an independent PSD diagonalization. Two-time/probe arrays are internally cross-checked, not repropagated; stationary projectors are not independently recomputed. These limits are explicit in the receipt.

Reproducer `native_thermal_packet_saved_audit_v001.py` SHA256 `518b2d2203f09bc213bf4b0233b443dc629746538c0b9b526d321e7da7ed1802`; receipt `NATIVE_THERMAL_PACKET_V001_SAVED_AUDIT.json` SHA256 `2c3f6d7a33e337f0a38878da0038b5935c192de6e45760771e6359a343d58095`. `NATIVE_THERMAL_PACKET_SAVED_AUDIT_ATTEMPT_001.md` preserves the auditor-only syntax and integer-serialization corrections; frozen scientific outputs were unchanged.

## Useful controlled contrast

The cycle q=0/q=1 pair has identical initial total energy 21.5, variance 1.5, local-energy means and zero currents. It evolves under the same native action/coefficient choices but different owned record sectors. The occupied-record storage +4 and initial feedback -4 cancel in total energy, not in the subsequent incidence dynamics.

Resolved differences appear without a new energy-temperature fit. At native age 2 the left-patch energies are 10.86315059 and 10.85530058; fluxes are +0.53962483 and +0.50533930. Across the retained ages, the largest absolute patch-energy difference is 0.01622369, and the largest flux difference is 0.03428553. Both patch fluxes change sign over time; neither is monotonic dissipative relaxation.

For the same cycle pair, the largest probe-matrix difference is 0.04926048 at age 0.5, duration 2, frequency 0.75, plus/emission sign. The connected-matrix difference there is 0.02144130. Maximum connected off-diagonal magnitudes across each complete cycle census are 0.00126729 (q=0) and 0.00321787 (q=1). These are source correlation coefficients in native units, not emitted photon counts or a sky correlation. Maxima describe retained data; they were not success gates or chosen windows for execution.

The tree comparison also changes transport and probes, but its initial energies differ, 15.5 versus 16.5; its initial left-patch energies differ by 0.5. It must not be advertised as an equal-energy control. Its largest probe/connected-matrix differences are 0.15602126 and 0.11065054, respectively. The receipt retains all signed age contrasts, not only these extrema.

These results establish a finite-cell mechanism: record feedback affects correlated local transport and weak-probe response even at equal initial total energy in the cycle pair. They do not establish equality of the complete energy distributions, actual preparation dynamics, a temperature, an irreversible conductance or a common equilibrium.

## Stationary versus actual-state interpretation

The actual coherent kernels retain age dependence and reversible current flow. Their whole-energy-dephased comparators are explicitly different states. Many dephased transitions are population inverted; for example, the strongest resolved cycle pair has absorption/emission ratio corresponding to beta_eff about -0.70868 for q=0 and -0.77299 for q=1. Strong tree lines already contain both positive and negative beta_eff. The complete beta ranges are strongly line dependent. Extreme ratios at tiny gaps/weak weights are not relatively certified temperatures and are not needed for the conclusion: these supplied states are not demonstrated common positive-temperature baths.

The source-work identity sum_v chi_vA=<dot h_A(s)> correctly need not vanish. Stored regular kernels obey the reviewed continuity identity; a full theta-retarded derivative additionally has its equal-time delta-contact. A hypothetical source must retain its switching work. Here no source pulse, loading trajectory or probe backreaction was evolved.

Connected initial graphs, nonzero native currents and positive probe Gram matrices are genuine prerequisites for a transport/correlation account, but do not alone yield Planck radiation, a Markov heat equation, common KMS ratios, macroscopic mixing or observed CMB anisotropies. No physical photon/second/ruler dictionary or inflation/Big-Bang-origin premise is silently added. The next thermal claim would need a controlled common-state transport/noise and energy-debit limit, not an imposed uniform-temperature reset.
