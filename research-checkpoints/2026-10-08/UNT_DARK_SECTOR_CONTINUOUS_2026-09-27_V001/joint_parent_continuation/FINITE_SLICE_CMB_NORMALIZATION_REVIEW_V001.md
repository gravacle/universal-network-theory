# Finite-slice CMB normalization: independent review

2026-09-29. Full-read analytical acceptance of
`FINITE_SLICE_CMB_PREPARATION_AND_BOLTZMANN_ROUTE_V001.md`, SHA256
`7b9a4952f279d9a32b6a6d5de9338f01b50bd3cbd6a1eab8cced8bad5f593cd4`.
No source import, numerical producer, code receipt, build or observational fit.

## Brightness, scattering and the finite boundary

With the stated `(-i)^l(2l+1)` expansion, the photon collision source
`-Pi P2/2` has quadrupole coefficient `+Pi/10`. The polarization multipole
source `Pi(delta_l0+delta_l2/5)/2` reconstructs

    Pi(1-P2(mu))/2 = 3 Pi(1-mu^2)/4.

Thus equation (4) and the angular source in equation (8) agree. Adding
`4 Phi` to brightness cancels the angular gravitational gradient, leaving
`4(Psi'+Phi')`. The integrating factor gives exactly the written initial
term `exp(-tau_i-ik mu chi_i) B_i`; it does not disappear by changing the
name of the initial slice. Dividing brightness by four gives temperature
and polarization-temperature normalization consistently.

For the standard scalar E convention, the spin-two projection therefore
has source coefficient `3 Pi/16`, times the stated factorial and Bessel
kernel in equation (9). This is consistent with the temperature-normalized
coefficient `3 Pi_T/4`, where `Pi_T=Pi/4`. The Stokes basis and E sign must
still be bound to the implementation for a signed TE comparison; EE alone
cannot detect an overall E sign error. The primary normalization check is
[Zaldarriaga--Seljak, equations (14)--(19)](https://arxiv.org/html/astro-ph/9609170v2).

## Regular-series and curvature normalization

In the qualified leading radiation regime, choose the conformal origin
so `mathcal H=1/eta` for the leading solution; this does not assert a
physical initial singularity. Constant Phi gives `theta=k^2 Phi eta/2`.
The neutrino shear equation
then yields `sigma_nu=k^2 Phi eta^2/15`. Inserting this into the slip
constraint gives `Psi-Phi=2 Rnu Phi/5`. A perfect hard radiation fluid
enters the total radiation density but not that shear numerator. These
checks reproduce equation (7); the imported ordinary conventions match
[Ma--Bertschinger, equation (98)](https://arxiv.org/html/astro-ph/9506072v1).

The stated finite-slice curvature is

    zeta=-Psi+delta_rho_tot/[3(rho_tot+p_tot)].

In the leading radiation solution only, this becomes

    zeta=-(3/2+2 Rnu/5) Phi,
    Phi=-10 zeta/(15+4 Rnu).

This is a useful explicit transfer-normalization control, not permission
to replace the exact finite-slice species sum by its asymptotic limit.
Higher-order series, finite hard transition, baryon loading, finite opacity
and constraint projection retain their own errors. Initial-slice refinement
must transport the SAME declared state rather than reset its random field.

## Scope verdict

The exact material/current interface, separate collisional photons and free
ordinary neutrinos, background-H0 conversion, finite boundary term and
single shared covariance make a coherent conditional linear-scalar design.
No loading of an existing Boltzmann code was tested by this review. The
review does not establish a likelihood pass, a native temperature/clock,
an initial-spectrum mechanism, or an inflationary/Big-Bang premise. The
present normalization algebra is accepted without a correction to the
reviewed source note.
