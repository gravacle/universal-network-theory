# Independent photon-reference dimensional and scope check

2026-09-29. Reviewed the complete `RADIATION_PHOTON_REFERENCE_V001.md`,
SHA-256 `07c0a0d0dc47c69b6e30648d4c4b70cdaa12fceecee10df0c9673bd2ce3cec2f`.
Accepted as a reference-density comparison, not an observational acceptance
test or a derivation of photons from the network.

Integrating the two-polarization Planck energy spectrum gives
`u_gamma=8 pi^5 (k_B T)^4/(15 h_P^3 c^3)` in joules per cubic meter.
Dividing by the **energy** critical density `3 H0^2 c^2/(8 pi G)` gives the
stated dimensionless `Omega_gamma`. No missing `c^2`, polarization factor,
or ordinary/ reduced Planck-constant conversion was found. Each inherited
H0 must retain its original Mpc conversion. The stated independent linear
T/G uncertainty is appropriate only with H0 and inherited calibration held
fixed; it is not a total uncertainty or a covariance-aware likelihood.

The combined temperature and its distinction from the recalibrated FIRAS
value were independently checked against the
[Fixsen 2009 abstract](https://arxiv.org/abs/0911.1955).
Exact c, h and k_B were checked against
[NIST's SI definitions](https://www.nist.gov/pml/special-publication-330/sp-330-section-2).
The cited G value and uncertainty are also available in the
[NIST 2022 CODATA text table](https://physics.nist.gov/cuu/Constants/Table/allascii.txt);
the PDF endpoint did not load in this review.

The proposed ratio compares the already-owned conditional mode energy
coefficient with ordinary photon energy. Its early-epoch interpretation
requires both photon `A^4` scaling and the network action/clock domain.
The note explicitly preserves these assumptions, the independent vacuum
ledger, the six pulse spectra's merely conditional normalizations, and the
need to reconsider standard-BBN inputs if the expansion history changes.
It does not infer a photon spectrum, free streaming, an N_eff likelihood or
CMB acoustic success from an equation-of-state coefficient.
