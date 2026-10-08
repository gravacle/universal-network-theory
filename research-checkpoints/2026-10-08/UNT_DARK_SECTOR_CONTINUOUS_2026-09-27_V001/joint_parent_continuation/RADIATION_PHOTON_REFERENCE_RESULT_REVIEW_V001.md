# Independent photon-reference code and saved-result review

2026-09-29. **Accepted.** This reviewer fully read the final dimensional note
and producer, then independently checked saved-output arithmetic using Python
stdlib and 60-digit Decimal constants. No producer was imported or rerun; no
mode evolution, quadrature, action solve, fit or source preparation occurred.
Primary-source number verification is separately recorded in
`RADIATION_PHOTON_REFERENCE_REVIEW_V001.md`.

Authenticated SHA-256 identities:

- Result `RADIATION_PHOTON_REFERENCE_V001_RESULTS.json`:
  `45d4353256d15b87bf57df3f67a6b581a8f6d347fc42f8eb022f3c43713e7b41`
- Producer `radiation_photon_reference_v001.py`:
  `8aa6d49318ccb0f89a0169dbcab83ea70c676264cfa6f137b19340afc8b5582a`
- Note `RADIATION_PHOTON_REFERENCE_V001.md`:
  `07c0a0d0dc47c69b6e30648d4c4b70cdaa12fceecee10df0c9673bd2ce3cec2f`
- Input `SAME_ACTION_RADIATION_V001_RESULTS.json`:
  `b01ba51bcfb8793fbaed3a3626e797a6b24b4d86c98bc15f9e6bef92a66a39f5`

The source input's canonical payload hash, complete status and empty failure
list were checked. Its deeper mode/input audit is separate; this review does
not claim to duplicate that calculation. The producer and note hashes in the
output match the actual reviewed files. An initial preflight scope mismatch
(only A1101 emitted while the note promised every saved A) was corrected
before this final version: all six values are retained.

## Dimensional and census checks

The two-polarization Planck integral is
`u=8*pi^5*(k_B*T)^4/(15*h_P^3*c^3)` in J/m3. The photon mass density is
`u/c^2`; division by `3*H0^2/(8*pi*G)` gives dimensionless Omega. The
ordinary/reduced Planck-constant conversion, polarization count and c powers
are correct. Each row uses its saved H0 in inverse seconds, without repeating
or changing the inherited Mpc conversion.

Independent arithmetic gives:

- photon energy density `4.1746783808003755e-14 J/m3`;
- photon mass density `4.644956134403367e-31 kg/m3`;
- fixed-H0 independent linearized T/G fractional uncertainty
  `0.0008368517280240154` (about 0.0837%).

All 18 reference records match their source metadata exactly. There are 648
original-template mappings and 108 explicitly conditional extended-spectrum
mappings, with 756 unique `(template_index,reference)` keys. Every mapping
retains all six A values `(1,2,4,11,101,1101)`: 4,536 finite-A coefficient
rows, their upper-error intervals, and the asymptotic ratio. Every scalar
ratio was independently recomputed, and all stated finite-gap intervals were
checked with the unchanged inherited allowance. The audit made 23,512
identity/arithmetic checks; maximum relative discrepancy was
`6.557565844122518e-16`.

| Complete family | Asymptotic coefficient / photons | Saved A1101 coefficient / photons |
| --- | ---: | ---: |
| Original, all 648 mappings | 223.962055–1640.159100 | 224.051566–1640.175087 |
| Conditional extended, all 108 mappings | 33.522395–651.708974 | 33.828586–651.732279 |

These are complete-family extrema, not chosen favorable states or a likelihood.
The output compares the already-normalized excitation coefficient with a
photon density reference. It neither equates the modes with photons nor
proves that the adiabatic action, rapid averaging, isotropic state and volume
clock assumptions hold at A1101 or at the formal asymptote. Its early-epoch
interpretation also requires ordinary photon A^4 scaling. No neutrino number,
free-streaming prediction, acoustic spectrum, N_eff constraint or all-UNT
exclusion was inferred. The imported standard-BBN baryon alternatives require
reanalysis if this extra early density changes the expansion history.
