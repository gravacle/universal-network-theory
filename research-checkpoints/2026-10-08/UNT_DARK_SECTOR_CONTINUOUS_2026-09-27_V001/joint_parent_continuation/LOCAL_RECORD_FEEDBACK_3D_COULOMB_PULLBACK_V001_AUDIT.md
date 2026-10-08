# Independent saved-only Coulomb pullback audit V001

PASS: 5601 independent assertions; all 20 datasets and 1024 leave-one-block replicas checked. Producer controls remain 200/200. No producer import, Hamiltonian action, sampler or RNG replay.

Raw query block sums were reconstructed before centering. Every central result, joint 32/128-block real/imaginary jackknife error, changing mean dyad, derived trace error, D mean, DD contraction, checkpoint, input seal and receipt boundary agrees. All parent mixing qualifications remain unchanged.

| Dataset | Trace response ± SE | K_D ± SE | χ_DD density | D density | Parent status |
|---|---:|---:|---:|---:|---|
| condition0 | -0.263328726474 ± 0.00705143 | 0.0146105568435 ± 0.00450973 | 0.174896115203 | 0.0947533360234 | FINITE_GRID_PILOT_DIAGNOSTICS_PASSED |
| condition1 | -0.273568867337 ± 0.00767276 | 0.0113121625995 ± 0.00474571 | 0.178963100304 | 0.0951376314516 | FINITE_GRID_PILOT_DIAGNOSTICS_PASSED |
| condition2 | -0.274982161568 ± 0.0107399 | -0.0530262271771 ± 0.00572867 | 0.180247793836 | 0.0636107833297 | MIXING_UNQUALIFIED |
| condition3 | -0.262821481764 ± 0.00863578 | -0.044652381204 ± 0.0046918 | 0.171021080454 | 0.0631843496252 | MIXING_UNQUALIFIED |

The full electrostatic sector remains symbolic: K_D + 2[alpha + 1/(4(alpha+4))] + Rraw_second/V. Alpha, the absolute-reference derivative and other strain/source/rest terms remain unowned. Neither the measured trace response nor K_D establishes full mechanical stiffness, pressure, a physical metric or cosmic evolution.

Result SHA256: a0ed403a7bbd41ed460605c568a8b57260897d31e0e2218286b649c83c1871d5.
Canonical result SHA256: 64555da51cfa69c41111032fe1468431fd1626b13741cdcf58c5953271aae08b.
Report SHA256: fe6fd129e8948e5208597d8bcf1fff2c4ea98072681cc21456c22477eee6d269.
Receipt SHA256: c1888849fc79daf6ff32c90db2fa558947e204fc2a3d5d98ef42c95e8c6a122c.

Full raw input/checkpoint seals and dataset values are retained in the companion audit JSON.
