# Independent saved calorimeter audit and source-energy interpretation

## Qualification and identities

Accepted as the explicitly switched two-level calorimeter experiment. All 648 rows, 324 coupling pairs, 12 on-Hamiltonian spectra and 36 independent vector-action comparisons are retained. The producer reports COMPLETE, no failed checks, 6,602 numerical checks, 0.846464459 seconds and 89,014,272 bytes peak process-self RSS. These counts are not independent physics tests and RSS is not whole-machine memory.

| Artifact | SHA-256 |
|---|---|
| `NATIVE_CALORIMETER_PORTS_V001_RESULTS.json` | `0dd6bb4ecc1b4e3875d603755de98e6b0dbe8028a416c7509fa8cca9ce8516ed` |
| `NATIVE_CALORIMETER_PORTS_V001_FROZEN.json` | `dd3eada48d549bfd53663fc362375ef56c9d7a186807719aa0cb5933c55c44fe` |
| Canonical payload | `339d7803e7642b21643d239ebc9a2e81b637cc01d12b6e33815fa72a11623871` |
| Producer | `dd04a76c43d7b649fa1829c678924040651b96a78efa6d78dc105df78b5e40f9` |
| Protocol | `7b343eec0228adc3a1cc4c3de0f4c42bc8c1017b5fd166932def658c22ba006c` |
| Auditor `native_calorimeter_saved_audit_v001.py` | `1cef7aba102e25b65f0debae1b16c6812724ec7c0fb948950104bc140510f170` |
| `NATIVE_CALORIMETER_PORTS_V001_SAVED_AUDIT.json` | `97bba6fddc5c19a7585ab6c07626eb47ae4acbda22b08fe1102db1d0129b56f7` |

The independent saved-array auditor authenticates 22 files, three manifests and 42 member occurrences. **56,324 arithmetic entries pass**, maximum discrepancy (9.443\times10^{-14}). No producer, propagation or eigensolver was run. The complete source/protocol and reused definitions were reviewed before the parent executed this experiment.

## What was independently checked

The full Cartesian row/pair census and source associations; all probe-density Hermiticity/traces and every principal minor; populations, lowering means, K03-oriented cross and connected cross; native/probe energy differences and signed switch work; all inherited emission/absorption diagonals and vacuum coherent/connected predictions; exact parity/Dyson bounds and their saved deviations; every coupling-pair subtraction and method-row association. Independent spectral trace/square identities verify the twelve stored 256-dimensional spectra against the old native spectra and adopted probe/interaction terms. Chebyshev tail/alias certificates are recombined algebraically without computing an action.

The largest reported dual-state difference is (3.495\times10^{-14}), energy conservation error (9.237\times10^{-14}), and complete work-ledger error (9.443\times10^{-14}). All saved weak-response deviations satisfy the prospective Dyson bounds plus their fixed roundoff allowance; maximum population-bound utilization is 0.03271. Maximum absolute normalized flip-coefficient errors are .000443668 at g=.01 and .000110921 at g=.005. No fixed factor-four gate was imposed, and small individual coefficients do not acquire a relative-precision guarantee from these absolute tests.

Final coupled/native state vectors are not saved. Therefore their native-energy expectations and dual-action comparisons remain authenticated producer certificates, not independently reconstructed propagations. Probe observables and the work arithmetic do follow independently from the saved reduced densities/energy ledger.

## Energy comes from both native debit and the actuator

All 216 initially empty-probe rows gain probe energy. In 200 the native system loses energy; in **16 it also gains energy**. The latter are unambiguously actuator-supplied on both sides. Vacuum switch work is positive in 210 rows and negative in six. The exact accounting is

    probe gain = native debit + switch work.

Across all vacuum rows, native debit/probe gain ranges −.0121628 to 1.1335596, and switch work/probe gain ranges 1.0121628 to −.1335596. Fractions outside [0,1] correctly retain native gain or recovered actuator work; they are not efficiencies. No sign lies within the audit's explicitly reported 2e−10 descriptive zero band for these vacuum energy entries.

For the inherited middle window (native age=.5, duration=1, omega=1.5), at the smaller g=.005:

| Preparation | Probe gain | Native debit | Switch work | Native fraction |
|---|---:|---:|---:|---:|
| cycle q0 | 6.0634820e−5 | 3.8775158e−7 | 6.0247069e−5 | .00639487 |
| cycle q1 | 6.0309512e−5 | 9.8424103e−8 | 6.0211088e−5 | .00163198 |
| tree q0 | 5.9668851e−5 | 6.2321485e−7 | 5.9045637e−5 | .0104446 |
| tree q1 | 5.7752022e−5 | 3.5815218e−6 | 5.4170500e−5 | .0620155 |

Thus over 99% of the cycle probe gain in this illustrative window is switching work. The cycle remains the matched-initial-energy comparison; the tree is not. Actual connected-cross magnitudes for these cycle rows are (2.19225\times10^{-10}) and (3.56129\times10^{-9}), respectively. Record occupation changes the correlated response, but this does not turn actuator-supplied excitation into autonomous radiation.

The reverse-input rows also retain both energy-transfer signs, initial probe energy omega, and signed switching work. Total probe gain for a singly occupied pair includes both its absorption and the other probe's excitation; it must not be called an isolated absorption rate.

## Scientific scope

This closes a genuine operational check: independently coupled probes reproduce the actual nonstationary native weak kernels with backreaction and a complete energy/work ledger. The initial source-kick counterexample separately shows why identical local-energy summaries need not determine currents. Neither result establishes thermal equilibration, a Markov bath, physical photons, free radiation, an SI temperature, native-to-spacetime calibration or a cosmological origin. Most gain in the displayed cycle window is actuator-supplied; an origin claim still needs an owned preparation/supply mechanism and the relevant spectrum/correlation tests on that same state. No Big Bang or inflationary premise was introduced to obtain this conclusion.
