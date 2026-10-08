# Differential baryon calibration required by the lensing contrast

2026-10-04. Pre-execution specification. Data and preceding type-contrast
results are exposed. This is an inverse diagnostic, not a withheld prediction
or an accepted refit. Keep the galaxy-calibrated force and photon interface
fixed. Use both colour and Sersic classifications, seven primary bins each.

For the existing forward ESD function P(gbar), infer

    ghat_i=P^-1(ESD_i), b_i=log10(ghat_i/gbar_i),
    delta_i=b_high,i-b_low,i.

At fixed radius these are required total-baryon mass-scale shifts. They are
not measurements of individual galaxy masses: inverse-of-stack is not the
mean inverse, source-pair weights are missing and gbar itself has uncertainty.
The adopted compact-source/common-exterior geometry and stationary Phi=Psi
bridge remain conditional. Nothing is added to the original force law.

Select the paired 14-by-14 ESD covariance from the released 30-by-30 matrix,
including cross-type blocks and dividing its product bias once. With
s_i=d ln P/d ln g evaluated at ghat_i,

    db_i/dESD_i = 1/[ln(10) ESD_i s_i],
    J=[-diag(k_low),+diag(k_high)], C_delta=J C_14 J^T.

Report all fourteen required offsets and their seven differential values.
Use generalized least squares to summarize delta by one constant per split,
with its first-order statistical standard error and residual shape Q. This
is ONE fitted diagnostic constant per classification, not zero fitted
quantities and not fourteen newly accepted model freedoms. The two splits
overlap and must not be combined as independent evidence. Delta-method
uncertainties/shape Q are descriptive, not a calibrated rejection test.

No extrapolation: invert monotone log-ESD tables on g=10^-17..10^-9 SI at
2049 and4097 log-spaced points using the existing64-angle forward projection.
Check recovered logg agreement <=1e-6 dex, forward roundtrip <=1e-6 relative,
slope agreement <=1e-5 and propagated C_delta relative agreement <=1e-4.
Use symmetric logarithmic derivative steps 1e-4 and5e-5 and require agreement
<=1e-6. All checks precede the final diagnostic summary; preserve failures.
Controls include P_deep(g)=sqrt(a0*g)/(4G): its inverse is quadratic and
delta=2log10(ESD_high/ESD_low) for the matched coordinates. Use same bin edges
to report offset brackets [log10(ghat/gupper),log10(ghat/glower)], conditional
on a monotone true within-bin relation and a uniform scale shift per sample.
These are not statistical intervals or full catalogue recalibrations.

Compare the required TOTAL-baryon shift cautiously with the paper's separate
stellar-calibration checks: colour .14dex cross-method plus .027 estimated
selection bias; Sersic .12 plus .021. These are estimates within the study,
not independent hard bounds or guaranteed transferable priors. For the
published cold-gas estimator f_cold proportional to Mstar^(-.69),
Mbar=Mstar(1+f_cold) implies dlnMbar/dlnMstar=(1+.31f)/(1+f), between .31 and1.
Thus an assumed stellar offset is not identically a total-baryon offset.
Extended gas, differing stellar populations and catalog selection still need
independent evidence; do not assume they have been excluded.

Source: https://arxiv.org/html/2106.11677v1 sections3.3 and5.4, and the intact
official archive already recorded by EFFECTIVE_ESD_FORWARD_V001_REPORT.md.
One small local worker; no fit to a0/r, no new catalogue/installation, no old
galaxy rerun. Preserve the original lensing tension and evidence ceilings.
