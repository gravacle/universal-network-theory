# Fixed-source radial-shape audit V001

The frozen Leroy/Begeman source and the SPARC mass-model columns describe different radial baryon reconstructions and stellar bands. The same G=4.30091e-6 kpc (km/s)^2/Msun is used by the stored pure-Newtonian run and the current S_cross disk surface load. The older nonlinear action and its nominal a0 are not transferred: only the saved physical pure-Newtonian source forces are compared. Their finite-grid/255kpc-boundary diagnostics remain their own scope.

For the illustrative SPARC 3.6-micron mass-to-light value0.5, v_baryon^2=v_gas*abs(v_gas)+0.5v_disk,ML1^2+0.5v_bulge,ML1^2. Signed central gas contributions are retained. This0.5 is not the frozen Leroy K-band0.5 calibration; no physical source replacement, new fit or nonlinear response is selected.

| Radius (kpc) | illustrative SPARC/current-source Newtonian v² ratio |
|---:|---:|
| 2.89 | 0.954850 |
| 5.78 | 1.144406 |
| 6.43 | 1.156923 |
| 10.04 | 1.099105 |
| 14.05 | 1.152590 |
| 28.16 | 1.060973 |
| 44.08 | 1.022006 |

The source difference is radially structured, rather than a common mass multiplier: roughly10–16percent in v² at several middle radii and2percent at the outermost point in this illustrative comparison. This warrants a physical photometric/source reconciliation before interpreting the entire native residual as constitutive-law failure. It does not demonstrate that a different source fixes the nonlinear galaxy prediction; no replacement S_cross solution was computed. The current original-source mismatch remains a failed observational diagnostic.

Every43 original observed radii/velocities/errors matches exactly. Input hashes and complete frozen Newtonian ancestry were verified before and after this saved-table arithmetic. Full43 descriptive rows and all source pins are retained in the companion JSON. No numerical worker, operator, density reconstruction or observational optimization was launched.
