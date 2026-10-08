# Independent saved-result audit: ordinary PRIMAT V001

Accepted for the declared **ordinary nuclear-tolerance refinement only**. Both immutable runs and the comparison authenticate, and all 86,558 independent saved-arithmetic checks pass. No PRIMAT/library import, compiler, rate/background interpolation, nuclear integration or physical producer was run by this audit.

## Bound evidence

Paths below are relative to this directory; `B` means `bbn_inputs_v001/primat_c_reference_v001`.

| Artifact | SHA-256 |
| --- | --- |
| `B/build_ordinary_v001/PRIMAT_ORDINARY_SUPERVISOR_V001_FROZEN.json` | `1ef54049931289f2c8715d56f080566e1aecb01e483aada8681fe7b985d7ed00` |
| `B/build_ordinary_v001/PRIMAT_ORDINARY_BUILD_V001.json` | `6a9ef5f2be2cad88e643444c5ec3628815ca2bc351ab9a86028c7df1aa940e74` |
| `B/build_ordinary_v001/receipts/run_default.json` | `1c7031401f5a37450946a270c6503e2e6b1ad27103ba70d477956ec728629e60` |
| `B/build_ordinary_v001/receipts/run_refined.json` | `0c76bc2b05e9a821de3c411b5441cbb8f0b1ba8127d2f90bc4b18444e8320475` |
| `B/build_ordinary_v001/receipts/ordinary_comparison.json` | `23fe82a7fc6e6ce6ea309b78704dad588e43d981f027e14ed37c1561259119a3` |
| `primat_ordinary_saved_audit_v001.py` | `fa912ec1946989315f4ffcd8b8268ba6ed5f07a47d6eda6b6006797ff0cedb04` |
| `PRIMAT_ORDINARY_SAVED_AUDIT_V001.json` | `a4d709b27e350b4bc918cdd0990aee8db895c0e7982c04b520cec1d01748f632` |

The saved-only reproducer authenticates 194 file identities, the full frozen input map, 46 source Git blobs, 24 raw data receipts and their declared CRLF/final-newline normalization, 24 compiler commands/outputs/intents, binary and version receipt, both complete compressed stdout/stderr streams, parsed results and canonical payload hashes. It does not assert reproducibility of unpinned SDK/library bytes. The build's compiler identity is retained; no compiler was invoked to revalidate its version. The source/API arithmetic inspected is the pinned `upstream/primat-c/src/{api,constants,background}.c` and the ordinary adapter.

## Reconstructed numerical result

All 4,674 default and 9,565 refined nuclear rows, 2,761 background rows per profile, and 2,049 HT generator rows per profile remain present. The original producer check counts independently reconstruct to 98,782 and 191,711, respectively, with zero failures. These are numerical entries, not independent physical tests.

| Quantity | Default | Refined | Signed default-minus-refined comparison | Frozen gate |
| --- | ---: | ---: | ---: | ---: |
| D/H | 2.4358767189e-5 | 2.4358703884e-5 | relative +2.5988651e-6 | 5e-5 |
| BBN helium fraction | 0.24699906524 | 0.24699870230 | +3.6294002e-7 | 1e-5 |
| CMB atomic-mass helium fraction | 0.24567275668 | 0.24567239505 | +3.6162698e-7 | 1e-5 |
| Effective neutrino number | 3.04397729856 | 3.04397729856 | relative 0 | 2e-12 |

The final abundance reconstruction uses the saved eight-species row: D/H=Y(H2)/Y(p), helium-BBN=4Y(He4), He3/H includes H3 decay, and Li7/H includes Be7 decay. The CMB helium conversion retains the pinned atomic masses 4.0026032541 and 1.00782503223 rather than identifying the two helium conventions. Neff reconstructs from the three saved final neutrino temperatures using the pinned standard, zero-extra-density convention.

Maximum baryon-number defects are 1.65423e-12 and 1.65734e-12 against the unchanged 1e-8 gate. The refined minimum raw abundance is -3.52738e-19, retained without clipping and within the frozen -1e-12 allowance. Repeated nuclear era endpoints remain present. Background rho_B a^3 is constant to a relative 4.44e-16. Weak-rate nulls above 10 MeV remain null, not extrapolated values.

The backgrounds and HT arrays are byte-equivalent as parsed numbers between profiles. The saved log-time Simpson sums independently give K_2048=798.8511817813236 and K_1024=798.8511817824606, normalized difference 1.42327e-12. This supports the exact fixed two-state HT contraction identity with an approximate integral; it is not a nonlinear final-abundance error bound or a new background refinement.

The controller reports 0.4845 s/default and 0.1130 s/refined, no watchdog/error. Sparse sampled RSS values 32,768 B and 0 B are **not actual peak-memory measurements**; the refined run can finish before the first sample. They must not be reported as the library's memory demand.

## Scientific scope and next step

This is a functioning, source-bound ordinary reference with successful nuclear-tolerance refinement, not a scalar-H calculation or an abundance likelihood. The fixed NEVO/background and rate-table resolution have not been independently refined here. The ordinary H implementation's baryon-rest-density omission is unchanged. No nuclear-rate covariance, observational calibration, or theory-error propagation has been performed. A standard hot-history comparison remains a conditional scientific interface, not an assumption that UNT starts at a Big Bang or requires inflation.

The next meaningful BBN step is an explicitly sourced same-state conserved-scalar contribution to the actual scale-factor H history, retaining thermal/weak-rate conservation and comparing its zero-scalar limit to this ordinary reference. That requires its own prospective source/thermal qualification; this audit does not authorize or execute it. All old table-proxy limits and failures remain separate.
