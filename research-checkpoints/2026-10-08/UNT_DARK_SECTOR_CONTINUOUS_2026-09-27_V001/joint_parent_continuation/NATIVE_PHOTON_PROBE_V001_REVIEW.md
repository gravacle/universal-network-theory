# Independent photon-probe review V001

Date: 2026-09-29. Outcome: **accepted within the declared conditional probe model; no implementation or mathematical blocker found.** This review read the complete protocol and source, authenticated saved evidence, and independently recombined saved line weights. It did not rerun a native propagator or simulate photons.

## Custody and numerical census

SHA-256 identities:

| Artifact | SHA-256 |
|---|---|
| `native_photon_probe_v001.py` | `d4956a73c1d8c93bc3f45d9fef63d500ab550edfe9682137a4e34920022cee44` |
| `NATIVE_PHOTON_PROBE_PROTOCOL_V001.md` | `53c92206a2351a45d119fdc80c75e190c27061e2788ff9991495be7ba9477598` |
| `NATIVE_PHOTON_PROBE_V001_FROZEN.json` | `7c21b45e62ac49aafe7acbf2766683f4f7e8279ff1dc859b2a72670c38bbdb2e` |
| `NATIVE_PHOTON_PROBE_V001_RESULTS.json` | `9dc4d27694d313173c6fa80a276ad4068c315d454f59da9dad07e7b586bc1b9a` |
| Canonical result payload | `918d876a15dcddf0be05c9b1ff2fa06ee40014103c5ef74d01bbd71e2557ffd7` |

All nine frozen files match. The result's freeze link, canonical payload hash and configuration match; the parent record-addition result's payload, freeze link and five transitive frozen files also match. These establish byte custody, not a substitute for the mathematical checks below.

The Cartesian census is exactly 162 distinct rows: three preparations, two operators, three ages, three durations and three frequencies. All six stationary diagnostics are present. The saved status is COMPLETE, with 3,731 checks and no failures. The largest numerical residual is `3.8324898810060404e-13` in the rounded allowed-gap comparison; the independent spectral-integral/Taylor-quadrature discrepancy is `1.181968069280949e-14`. Reported runtime is 0.129251458 seconds and peak **self** RSS 37,060,608 bytes, not an aggregate job-memory measurement.

## Independent mathematical checks

For the adopted interaction `eta B(a+a†)` and `hbar=1`, the energy-basis kernel has frequency `E_i-E_j+omega` for vacuum emission. Thus the source correctly uses `F_plus`, with coefficient `||F_plus psi_age||²`. Its negative-frequency counterpart is `F_minus=F_plus†`. Initial one-photon absorption has coefficient `||F_minus psi_age||²`. The calculation retains the actual aged state without adding its age twice to the Heisenberg operator.

Energy dephasing preserves degenerate eigenspaces. It is a separately labelled stationary diagnostic, not an unannounced replacement of the formed state. The analytic incidence transition strength is `1/d²`, with the correct lower/upper populations; the five native positive gaps are `sqrt(73,89,113,145,185)/4`. The feedback-off spectrum has two gaps; copying-off has the same two occupied gaps, with the other structural lines explicitly retained at zero weight. Record count has only zero-frequency weight.

Using only the saved line weights, this review reconstructed every stationary finite-window coefficient with

`K(z,T)=4 sin²(zT/2)/z²`, with its continuous value at zero,

`E_bar=W0 K(omega)+sum_d[W_abs(d) K(omega+d)+W_em(d) K(omega-d)]`,

and the reversed signs for absorption. The maximum difference from the saved values was `5.134781488891349e-14`. Independently resumming `2 sum d(W_abs-W_em)` agrees with the stored stationary double commutator to `4.0523140398818214e-14`. It must not be equated with the nonstationary initial double commutator: the native values are respectively 0.5696679618869833 and 0.8845136230893136.

For all 81 record-count rows, `E=A=K(omega,T)<R²>` agrees to `7.993605777301127e-15`; copying-off gives exactly zero. The nonzero finite-window record coefficient is coherent switching/dressing response. Because `[H,R]=0`, it does not establish stationary energy-conserving radiation from the held record count.

## What the result establishes

The native incidence source is spectrally active and sensitive to record feedback and actual preparation history. For the native preparation, the largest full-state versus stationary emission-coefficient difference is 0.123677429262723. One of its 27 incidence windows has emission greater than absorption; each control has six such windows. These are finite coherent windows, not evidence of a stationary inverted bath or negative opacity.

The native stationary linewise inverse temperatures range from 0.6073917394709404 to 0.8460508590720801. The two occupied control lines give 0.59466256763153 and 0.66073130873799. Hence none of these specified stationary incidence diagnostics satisfies a single-temperature detailed-balance relation across its occupied lines. This is an actual result, not a generic caution: a Planck bath does not follow automatically from these prepared cells.

The constructive next spectral target is therefore an owned many-cell/state mechanism that changes or broadens these discrete, preparation-dependent strengths while preserving the energy debit. No physical microwave frequency, irreversible emission rate, continuum opacity, thermalization or CMB fit is contained in this finite-cell probe. The operator and oscillator coupling are explicit additional hypotheses; the native Hamiltonian and prepared states were not tuned to a radiation target.
