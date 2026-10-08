# Fixed-parameter forward lensing comparison

2026-10-04. A new observational check of the older conditional stationary
response, not a claim that the current K(X)/compression model has formed it.
All previous failures remain unchanged. No fitted halo, slip or lensing scale.

## Question and inputs

Does the galaxy-calibrated force law also predict the published excess
surface-density (ESD) profile, without converting ESD into acceleration via
an assumed isothermal profile? Use the unbinned isolated KiDS-bright profile
`Fig-4-5-C1_RAR-KiDS-isolated_Nobins.txt` and corresponding covariance from
the official 2.3 MB Brouwer et al. (2021) release:

- https://kids.strw.leidenuniv.nl/sciencedata.php
- https://kids.strw.leidenuniv.nl/sci_data/brouwer2021_rar.tar
- https://kids.strw.leidenuniv.nl/sci_data/brouwer2021_rar_README.txt
- https://arxiv.org/html/2106.11677v1 (sections 2, 3 and appendix A).

The downloaded archive remains intact in `external_brouwer2021_v001`.
Read only named members; no archive-wide extraction or additional services.
The sandbox's first network request failed DNS. A separately approved,
bounded public download succeeded; this was not a software installation.

All 15 target data values and the paper's qualitative conclusions have been
seen before this protocol. This is a no-refit cross-probe check, not a blind
discovery. The Mistele2024 reduced-acceleration check uses overlapping KiDS
observations and is NOT an independent dataset to multiply into a likelihood.

Hold a0 at `SPARC_EFFECTIVE_TRANSFER_V001_RESULT.json` values:
network 1.0059833281731022e-10 and empirical RAR 1.0022739170327795e-10 m/s^2.
Hold inherited shape r=25.51664211557329. Universal calibration is legitimate,
but the shape and metric bridge are adopted assumptions, not native proofs.
Compare baryons-only gravity and the separately galaxy-calibrated empirical
RAR on exactly the same projection, bins and covariance.

## Forward equation (source-only independent derivation checked)

For a spherical compact source, y=GM/(a0 R^2)=gbar/a0, F=f^{-1} and
g(r)=a0 F[GM/(a0 r^2)]. Adopt the older stationary Phi=Psi, minimally coupled
weak-field photon interface, not an unproved transplant from dynamical K(X).

    alpha(R) = 4 a0 R/c^2 integral_0^(pi/2) F(y cos^2(theta))/cos(theta) dtheta
    DeltaSigma = c^2/(8 pi G) [alpha/R - d(alpha)/dR]
               = sqrt(a0 gbar)/(pi G) integral_0^(pi/2) T(y cos^2(theta)) dtheta
    T(x) = sqrt(x) F'(x) = sqrt(x)/f'(F(x)).

T(0)=1/2 for the inherited low-field normalization. The mass cancels exactly
at a common gbar. This avoids nonlinear averaging over a mean galaxy mass
ONLY for this universal spherical compact-source family and common exterior.
Finite source extent, angular structure, external fields and mass-dependent
cosmological matching may break it. The convergent integral does not justify
an isolated logarithmic potential extending physically to infinity.

Independent projection identity, with u=sin(theta) for endpoint regularity:

    DeltaSigma = a0/(2 pi G) {F(y) + integral_0^1
                             [F(y)-F(y(1-u^2))]/u^2 du}.

Newtonian F(y)=y gives gbar/(pi G); deep F(y)=sqrt(y) gives
sqrt(a0 gbar)/(4G). Thus g=4G DeltaSigma is NOT universal. Use the exact
analytic derivative of the inherited flux, with a finite-difference check.

## Data conventions, fixed range and limitations

Apply ESD_t/bias and error/bias. Divide covariance column 5 by column 7
ONCE: column 7 already contains the product of two calibration factors.
Validate bin matching, symmetry, positive definiteness, correlation entries
and agreement of diagonal errors to the precision of the printed profile.
Use full covariance within each selected subset, not the corresponding
sub-block of an already inverted full matrix. Use h70=1, H0=70 and the
authors' flat distance cosmology Omega_m=.2793, Omega_Lambda=.7207. This is
an imported distance reduction, not elimination of DE from cosmology.
Use G=6.67430e-11 SI, parsec=3.085677581491367e16 m and Msun=1.98847e30 kg.
ESD is physical, not a comoving surface density.

Primary range gbar >= 1e-13 m/s^2 (seven published bins), chosen from the
authors' isolation warning, not the candidate residuals. Retain all 15 and
the eight lower-acceleration bins separately as flagged diagnostics. The
catalogue's isolation is no >10%-stellar-mass neighbour inside 3 h70^-1 Mpc;
photometric-redshift errors can contaminate profiles beyond about .3 Mpc.
The conservative threshold is not an exact per-object isolation guarantee.

gbar uses stars plus an empirical cold-gas estimate as a compact source;
uncertain extended hot/circumgalactic gas is not silently counted as dark
matter or freely fit. The stellar masses use Chabrier/Bruzual-Charlot/GAMA
calibration, not exactly the SPARC 3.6-micron mass-to-light prescription.
Published statistical covariance is not a complete systematic-error budget.

The 15 bins have published logarithmic edges from 1e-15 to 5e-12 SI. The
listed acceleration is approximately their arithmetic centre, not enough
to reconstruct individual source-pair weights. Report centre evaluation,
uniform-log average and uniform-annular-area average (weight dg/g^2), all
unfitted. Also retain predictions at both bin edges as an envelope, NOT a
best-fit choice or a guarantee under uncertain masses. No exact stack claim.

Unfitted total-baryonic-mass scale sensitivities: gbar times 10^(+/- .2).
These bracket a simplified fixed-catalogue mass normalization change; they
are NOT a full stellar-only perturbation with recomputed cold gas, selection
and weights. Do not select the best shift as the central answer or add the
same uncertainty independently in both axes. Preserve the central score.

## Frozen checks, reporting and execution

One small NumPy worker; no scipy, fitting, installs or other Mac. Freeze the
protocol, script, archive, galaxy-calibration receipt and inherited flux/shape
hashes before execution. Controls: Newton/deep analytic projection relative
error <=1e-11; 64/128 angular quadrature agreement <=1e-8 on target and
control range; inverse/flux agreement <=1e-10; analytic/finite-difference
flux derivative <=1e-6; alternate projection identity <=1e-6. Check positive
monotone predictions over all bin edges and mass shifts. Covariance symmetry
and reported correlation consistency <=1e-10; rounded profile/covariance
diagonal error and calibration consistency <=2e-4. No tolerance fitting.

Report Q=(prediction-data)^T C^-1 (prediction-data), Q/n and residuals as
statistical-covariance diagnostics. No calibrated p-value, global rejection,
Bayes factor or UNT-superiority claim: exact within-bin weights, complete
systematics and independent method-specific calibrations are unavailable.
No CDM-halo likelihood is constructed here; Newtonian baryons alone is not
the full standard cosmological model. Any tension is retained and directs
the next measurement-interface investigation rather than an automatic refit.

Stage 3 stays open, as do shared expansion, formation, growth, mergers,
BBN/recombination, CMB perturbations and the separate thermal-origin question.
