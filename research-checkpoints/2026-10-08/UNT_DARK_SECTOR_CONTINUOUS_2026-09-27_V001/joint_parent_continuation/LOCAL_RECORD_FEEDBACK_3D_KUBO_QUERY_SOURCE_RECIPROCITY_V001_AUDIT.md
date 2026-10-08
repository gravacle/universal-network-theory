# Independent saved Kubo audit V001

PASS: 3236 independent metadata/statistical assertions; all 20 datasets and 1,024 complete leave-block replicas. All 1,077 current inputs, 15 direct pins and 21 checkpoints authenticate. No producer, Hamiltonian, sampler or RNG replay.

| Dataset | trace K_A ± SE | trace derivative_a K_A ± SE | Parent status |
|---|---|---|---|
| c0_I01 | 20.7802171 ± 0.601 | -4.003424193 ± 2.3 | CHAIN_DIAGNOSTICS_PASSED_ONLY |
| c0_I02 | 20.3988194 ± 0.549 | -6.14392286 ± 2.27 | CHAIN_DIAGNOSTICS_PASSED_ONLY |
| c0_B | 20.29333304 ± 0.423 | -3.892490047 ± 3.06 | CHAIN_DIAGNOSTICS_PASSED_ONLY |
| c0_R | 21.62454694 ± 0.53 | 3.345381271 ± 3.04 | CHAIN_DIAGNOSTICS_PASSED_ONLY |
| c1_I01 | 21.63477774 ± 0.559 | -2.858406378 ± 3.14 | CHAIN_DIAGNOSTICS_PASSED_ONLY |
| c1_I02 | 20.24484685 ± 0.496 | -2.723935174 ± 3.35 | CHAIN_DIAGNOSTICS_PASSED_ONLY |
| c1_B | 20.87698751 ± 0.643 | -9.020520762 ± 2.87 | CHAIN_DIAGNOSTICS_PASSED_ONLY |
| c1_R | 19.71935161 ± 0.389 | -5.260053168 ± 3.18 | CHAIN_DIAGNOSTICS_PASSED_ONLY |
| c2_I01 | 40.69583744 ± 1.09 | -11.55434184 ± 7.76 | MIXING_UNQUALIFIED |
| c2_I02 | 41.97270442 ± 1.31 | -33.06760806 ± 9.57 | MIXING_UNQUALIFIED |
| c2_B | 42.92399549 ± 1.2 | -18.42543163 ± 10.2 | CHAIN_DIAGNOSTICS_PASSED_ONLY |
| c2_R | 39.4334572 ± 1.24 | -4.998488639 ± 7.78 | MIXING_UNQUALIFIED |
| c3_I01 | 45.80730771 ± 1.32 | 0.1183754061 ± 9.66 | CHAIN_DIAGNOSTICS_PASSED_ONLY |
| c3_I02 | 41.34980375 ± 1.4 | -19.56351924 ± 8.57 | MIXING_UNQUALIFIED |
| c3_B | 42.20894159 ± 1.56 | -21.40284752 ± 10.7 | MIXING_UNQUALIFIED |
| c3_R | 40.04094795 ± 1.26 | -9.701448953 ± 8.54 | MIXING_UNQUALIFIED |
| condition0 | 20.80093703 ± 0.265 | -2.720054354 ± 1.39 | FINITE_GRID_PILOT_DIAGNOSTICS_PASSED |
| condition1 | 20.64139476 ± 0.268 | -4.986664955 ± 1.56 | FINITE_GRID_PILOT_DIAGNOSTICS_PASSED |
| condition2 | 41.43326633 ± 0.607 | -17.069818 ± 4.43 | MIXING_UNQUALIFIED |
| condition3 | 42.68097982 ± 0.711 | -14.58339288 ± 4.73 | MIXING_UNQUALIFIED |

K_A is the per-A-cell normalized query mode. The equal-port all-node convention has the separately retained factor 2. The source derivative is clamped and finite-M; inherited mixing qualifications, all signed tensors and component errors remain unchanged. This audit supplies no continuum, SLD/QFI, inverse, physical metric or gravity qualification.

The first audit-only attempt stopped before statistics at a filename-expression typo; its session and error are retained in the audit JSON. The producer and all sealed inputs/outputs were never changed.
