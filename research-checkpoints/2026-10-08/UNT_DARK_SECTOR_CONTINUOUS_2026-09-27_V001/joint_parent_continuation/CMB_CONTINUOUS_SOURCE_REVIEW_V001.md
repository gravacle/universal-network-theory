# Independent root review — continuous radiation source screen

2026-09-29. Accepted within its explicitly adopted photon/metric interface.
Root read the complete 300-line analytical note, independently checked its
equations and added a bookkeeping clarification before this final review.
No numerical propagation or observational fit was needed or performed.

Reviewed final note SHA-256:
`b4cb12de9a11767f91b6441d860711e09f4f8e64ec7d1517c5065e7ffbe50ad4`.

## Independent checks

- Along a freely redshifting ray, Dx=-u*x, so Df_P=u*G with
  G=-x*f_P'. Integration by parts gives the factors three and four for
  photon-number and energy moments. No equilibrium repopulation is assumed.
- Grey thermal exchange has moment discrepancy
  kappa*(3*r^4-4*r^3+1)/3. Direct factorization yields exactly
  kappa*(r-1)^2*(3*r^2+2*r+1)/3, nonzero for positive r different from one
  and nonzero kappa. This excludes exact Planck preservation for that source,
  not observationally acceptable approximate spectra or other source laws.
- Pure thermal injection requires r=4/3 and u=64*j/81 from its two moments.
  Its Rayleigh--Jeans coefficient is instead 4*j/3; its Wien ratio to G
  grows exponentially. It therefore fails the full spectrum despite those
  moments matching. This is an exact counterexample, not a data fit.
- Positive birth/death rates A=kappa*f_N and B=kappa*(1+f_N) have the stated
  detailed-balance ratio and collision term. Solving the Planck tangent for
  kappa gives the claimed positive frequency law for r>1,u>0. Taylor expansion
  near r=1 and the low/high frequency limits verify its stated asymptotics.
  The required functional form is inverse-designed; it has not been derived
  from the native record model, and positivity alone does not prove spectral
  stability or a native Markov approximation.
- Summing the network/radiation continuity equations cancels Q. With the
  separately adopted radiation-like donor, direct logarithmic differentiation
  gives the temperature-ratio evolution and conserved a^4-weighted total
  radiation energy. The equilibrium endpoint follows by setting r=1 in that
  conserved expression. The donor carries energy and pressure and is not
  permitted to disappear from the gravitational ledger by renaming it.
- L integrates d log(a*T). Thus inherited radiation redshifted to the final
  epoch supplies fractions exp(-4L) of energy and exp(-3L) of photon number.
  I clarified the note's use of "comoving energy": the energy calculation uses
  a^4*rho, whereas true comoving-volume energy a^3*rho also changes through
  pressure work. The formulas were correct; the clarification prevents a
  misleading conservation interpretation. Both original and clarified notes
  are analytical drafts, not overwritten frozen experimental input.
- Isotropic birth/death exchange damps angular occupation perturbations by
  -kappa_nu*delta f. Using delta f=G*Theta and Dx=-u*x gives
  DTheta=(-kappa_nu+u*x*G'/G)*Theta, including the sign of the second term.
  Its Rayleigh--Jeans and Wien limits are different, so monopole preservation
  does not preserve a frequency-independent temperature anisotropy. The
  same bath does not supply correlated polarization. Extra network perturbation
  sources would require their own derived correlations and transfer terms.

## Scientific interpretation

This finishes the first cheap analytic CMB screen for two specified simple
sources and supplies an explicit conditional alternative. It neither excludes
the user's broader network hypothesis nor confirms a continuously generated
CMB. An exact Planck failure is not yet a quantified FIRAS exclusion: finite
spectral residuals and the actual data/covariance would still need evaluation.

The next meaningful calculation needs one owned network-to-photon coupling,
its emission/absorption spectrum, complete energy/momentum debit and perturbation
law. These must predict the observables together; frequency-by-frequency fitting
to the necessary law would not independently test UNT. Balanced maintenance
and a network-generated primordial state remain separate constructs. All
galaxy/expansion and broader Stage 3 obligations remain in force.
