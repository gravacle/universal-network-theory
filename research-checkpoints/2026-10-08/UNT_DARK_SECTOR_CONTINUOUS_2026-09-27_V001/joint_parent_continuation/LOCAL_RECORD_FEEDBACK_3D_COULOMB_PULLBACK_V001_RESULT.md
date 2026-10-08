# Clamped Coulomb offset-sector pullback V001

One declared fixedq1 candidate tangent, with du/da=.5 and df/da=−.5. Full nonlinear derivatives and their block SE are recomputed together, with unchanged inherited mixing statuses.

| Dataset | Average ET trace derivative Re +/- SE | K_D Re +/- SE | Parent status |
|---|---|---|---|
| c0_I01 | -0.2555744661 +/- 0.0138 | 0.01469152172 +/- 0.00983 | CHAIN_DIAGNOSTICS_PASSED_ONLY |
| c0_I02 | -0.2522358921 +/- 0.0145 | 0.01940342625 +/- 0.00824 | CHAIN_DIAGNOSTICS_PASSED_ONLY |
| c0_B | -0.2581104052 +/- 0.0119 | 0.02054074933 +/- 0.00752 | CHAIN_DIAGNOSTICS_PASSED_ONLY |
| c0_R | -0.2811691993 +/- 0.0157 | 0.005171584034 +/- 0.01 | CHAIN_DIAGNOSTICS_PASSED_ONLY |
| c1_I01 | -0.2581468002 +/- 0.0152 | 0.02154968469 +/- 0.00893 | CHAIN_DIAGNOSTICS_PASSED_ONLY |
| c1_I02 | -0.2751202318 +/- 0.0186 | 0.005470689839 +/- 0.0116 | CHAIN_DIAGNOSTICS_PASSED_ONLY |
| c1_B | -0.2611293539 +/- 0.0132 | 0.01941965453 +/- 0.00834 | CHAIN_DIAGNOSTICS_PASSED_ONLY |
| c1_R | -0.2989658675 +/- 0.0135 | 0.0008486481901 +/- 0.00838 | CHAIN_DIAGNOSTICS_PASSED_ONLY |
| c2_I01 | -0.225137126 +/- 0.0202 | -0.02284226904 +/- 0.011 | MIXING_UNQUALIFIED |
| c2_I02 | -0.2891901535 +/- 0.0237 | -0.0641876237 +/- 0.011 | MIXING_UNQUALIFIED |
| c2_B | -0.3128089368 +/- 0.0227 | -0.07002242265 +/- 0.0114 | CHAIN_DIAGNOSTICS_PASSED_ONLY |
| c2_R | -0.2599581748 +/- 0.0224 | -0.05310423402 +/- 0.0111 | MIXING_UNQUALIFIED |
| c3_I01 | -0.2371925215 +/- 0.0163 | -0.0387146814 +/- 0.007 | CHAIN_DIAGNOSTICS_PASSED_ONLY |
| c3_I02 | -0.2479897763 +/- 0.0139 | -0.03468608159 +/- 0.00821 | MIXING_UNQUALIFIED |
| c3_B | -0.273760592 +/- 0.0228 | -0.05487101025 +/- 0.0127 | MIXING_UNQUALIFIED |
| c3_R | -0.260413385 +/- 0.0236 | -0.0437070084 +/- 0.00993 | MIXING_UNQUALIFIED |
| condition0 | -0.2633287265 +/- 0.00705 | 0.01461055684 +/- 0.00451 | FINITE_GRID_PILOT_DIAGNOSTICS_PASSED |
| condition1 | -0.2735688673 +/- 0.00767 | 0.0113121626 +/- 0.00475 | FINITE_GRID_PILOT_DIAGNOSTICS_PASSED |
| condition2 | -0.2749821616 +/- 0.0107 | -0.05302622718 +/- 0.00573 | MIXING_UNQUALIFIED |
| condition3 | -0.2628214818 +/- 0.00864 | -0.0446523812 +/- 0.00469 | MIXING_UNQUALIFIED |

All signed A/B and average matrices, pair/dyad terms, derivative means, raw sufficient sums and Re/Im errors are retained.
Full clamped circuit-sector expression: K_D+2[alpha+1/(4(alpha+4))]+Rraw double-prime/V. Neither alpha nor the reference derivative is selected.
Other strain contacts and mixed operator responses remain unknown. This fixed-beta canonical sector is not complete mechanical stiffness, stability, pressure, volume or expansion evidence.
No physical metric/Fisher/SLD, inverse, selected significance, sampler/RNG/H replay or automatic continuation is inferred.
