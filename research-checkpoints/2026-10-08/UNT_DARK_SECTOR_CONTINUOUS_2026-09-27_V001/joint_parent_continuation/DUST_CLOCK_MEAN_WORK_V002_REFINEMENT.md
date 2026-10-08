# Mean-work V002: preserve and resolve the five V001 control failures

2026-10-05 UTC. Written before V002 execution. V001 remains FAILED76/81.
Its work identities and independent volume equations passed. Do not erase
the five failed controls or represent the original aggregate as qualified.

1. The exact initial-volume gate compared differently associated products:
   initializer -.75*Z**2 and readout +.75*Z*Z. Their roundoff difference was
   1.3235e-23 in amplitude-normalized units at k=.01,1.6156e-27 at k=.1.
   Use the same square expression in both places; retain tolerance1e-30.
   This changes no physical initial condition or parameter.
2. Centered derivative step1e-5 had truncation errors at k=.1,1 above the
   original2e-5 criterion. Recheck at1e-6 and5e-7 and compare both estimates,
   all with the same2e-5 tolerance. Complex-step action derivatives are
   unchanged; the finite-difference audit is being refined.
3. Cubic Hermite interpolation of the saved65-point k=1 trajectory had
   differential defect6.1925e-5, above2e-5. Upgrade interpolation to quintic
   Hermite using the exact endpoint second derivative of the SAME linear
   equations. No original source integration or harmonic sum is rerun.
   Keep the65-vs33-point and all original time/identity criteria unchanged.

Reuse the frozen V001 engine for physics and the complete original linear
receipt. Report derivatives of mean coordinates in Href time units, not
SI seconds. Proper-volume domain q is not observed redshift acceleration.
The2k response, nonlinear closure and observer optics remain unfinished.
