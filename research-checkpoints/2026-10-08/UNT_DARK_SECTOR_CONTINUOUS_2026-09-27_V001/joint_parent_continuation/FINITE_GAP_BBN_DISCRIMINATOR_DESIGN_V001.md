# A cheap, conditional BBN discriminator for the same scalar state

2026-09-29. Analytical continuation of the complete 360-state photon-budget
receipt. No mode propagation, BBN integration, abundance interpolation, fit,
package installation or remote computation was performed. The public primary
sources below were inspected for the proposed forward map and conventions.

## 1. What can be tested now

The new scalar candidate makes an early-expansion prediction without another
microscopic orbit run. Its homogeneous phase current is exactly conserved
within the adopted action. The stored quartic bounds certify when the same
finite-gap state is accurately radiationlike. The smallest useful observation
test is consequently **primordial helium, with deuterium as the shared baryon
calibration/consistency channel**, using a qualified BBN abundance response.
This is not a CMB free-streaming test and does not require assigning the
network excitations a neutrino identity.

The inspected receipt is `FINITE_GAP_PHOTON_BUDGET_V001_RESULTS.json`, raw
SHA256 `23feee802337320fde647fe87ff3ff24b1006c935cc3f31d9cf6a4a9574dba10`,
payload `0a08b471561a46d424efb58158d7adf53eb7506c697a50e66a4240c5074bf8a1`.
All 360 rows and five gap families remain. For R=8192 its **formal high-A**
coefficient relative to present photons is .310161–.402446. At A=1101 the
actual excitation/photon ratio is instead 5.28028–6.41959 and its pressure
ratio is .000116535–.000141661. The latter is predominantly matterlike energy,
not an additional radiation density. Neither number is a BBN result.

## 2. Exact current within the new action, not a microscopic averaging proof

Retain precisely the hard term in `MACROSCOPIC_ALPHA_ONE_GALAXY_BVP_V001.md`:

    L_H = C beta [I X - e_R(I,h)],
    X = sqrt(-g^{mu nu} partial_mu theta partial_nu theta),
    U_theta^mu = -partial^mu theta/X,       X>0.

The sign chooses the future-directed branch. Variation of theta and I gives

    nabla_mu(I U_theta^mu)=0,              X=e_I.          (1)

On homogeneous FLRW, theta=theta(t) and U_theta is the comoving velocity.
For lapse N, sqrt(-g)=N a^3 and U_theta^0=1/N, hence

    partial_t(a^3 I)=0,
    I(A)=A^3 I_1,                         A=a_1/a.        (2)

At h=0 with the declared soft ground background,

    rho_H=C beta e_R(I,0),
    p_H=C beta[I e_I-e_R],
    dot rho_H=-3H(rho_H+p_H).                              (3)

These are exact equations of this separately adopted scalar-fluid model.
They do not require checking H/omega every time (2) is used as a fluid
equation. That check was necessary when deriving an averaged action from
actual fast microscopic oscillators; trusting that derivation at a new epoch
remains a different, unproved physical claim. One must not both adopt the
scalar action as the tested theory and call its exact current merely an
approximate numerical dilution, or conversely promote it to an exact native
BS identity.

The metric/physical-volume dictionary, timelike regular phase, same
constitutive function at high density, ordinary matter microphysics, and
absence of additional exchange/production remain adopted assumptions. The
preferred FLRW normal is geodesic, so h=0 and the soft-zero state is an exact
background branch. This does not demonstrate microscopic phase preparation,
UV validity or perturbation stability. A later photon-exchange construct
must supply its own joint action/current/energy law rather than silently
borrowing this noninteracting history.

## 3. A rigorous route from the saved state to the BBN expansion history

Write E(A)=beta e_R(A^3 I_1,0), with E_1 its saved present value. The existing
Gamma-function result gives, for every retained row,

    Q=beta C4 I_1^(4/3),
    D=beta R^2 sqrt(C4) I_1^(2/3),
    A^4 Q <= E(A) <= A^4 Q+A^2 D,
    0 <= E(A)-3P(A) <= 2 A^2 D.                           (4)

Thus the relative energy correction is at most D/(Q A^2), and
0<=1/3-w<=2D/(3Q A^2). The receipt already supplies the sufficient A for
0.1% accuracy; its largest value across all 360 states is 532567.84. This
is a controlled approximation threshold, not an observed cosmological limit.

With ordinary post-annihilation photon temperature evolution, T=10 keV
corresponds to A approximately 4.3e7 using the already owned T0=2.72548 K.
The corresponding worst bound D/(Q A^2) is below 2e-7. Earlier ordinary BBN
temperatures have still larger A. Hence throughout the standard 10 MeV to
0.01 MeV BBN window, the finite-gap correction is negligible compared with
current abundance errors **conditional on that thermal history and the
fluid's validity**. The temperature interval and the need to evolve plasma,
weak reactions and nuclides are specified in the primary
[PArthENoPE formulation, section II](https://parthenope.na.infn.it/docs/PArthENoPE.pdf).

In physical energy-density units the exact background input is

    u_H(A)=u_crit,0 Omega_exc E(A)/E_1,
    H^2=(8 pi G/3c^2)[u_ordinary+u_H+u_vac],              (5)

with the original matched vacuum unchanged. Do not add a standard cold-dark
matter density on top of the same excitation budget. Homogeneous BBN depends
on (5) and the ordinary kinetic/thermal equations; it does not measure whether
the extra homogeneous stress free-streams or behaves as a perfect fluid.

Let r=Omega_exc Q/(E_1 Omega_gamma,0). This is the **post-reheating photon
reference coefficient**. It is not the ratio to photons at every temperature:

    u_H/u_gamma(T) = r [A T0/T]^4 [1+bounded correction]. (6)

Before electron-positron annihilation, photons are subsequently heated. In
the instantaneous neutrino-decoupling/ideal-plasma approximation, the earlier
ratio is r(11/4)^(4/3), whereas after annihilation it is r. In an accurate
calculation the same relation follows from the evolved plasma entropy and
neutrino energy transfer. Simply holding u_H/u_gamma=r across annihilation
would give the wrong expansion source.

For a BBN table explicitly parameterizing an additional decoupled radiation
component, define the **expansion-equivalent coordinate**, not a species count,

    DeltaN_exp = r / [(7/8)(4/11)^(4/3)].                 (7)

The normalization in (7) defines a conventional ideal late neutrino-temperature
unit. The chosen table's treatment of extra radiation, active-neutrino heating
and weak rates must match it to the required precision; inspect that interface
rather than infer it from the variable name. If its extra component follows a
different thermal convention, match its u_X(T) to (6) explicitly. Extra
electron-neutrino chemical potentials or changes to ordinary weak rates are
not free compensators in this test. No CMB N_eff posterior or neutrino
anisotropic-stress constraint follows from (7).

## 4. A small primary numerical asset exists; no installation is necessary

The [author's PRIMAT page](https://www2.iap.fr/users/pitrou/primat.htm) links
the small, precomputed
[2026 abundance table](https://www2.iap.fr/users/pitrou/primat/PRIMAT_Yp_DH_ErrorMC_1000_2026.dat).
Its header specifies omega_b, DeltaN, two helium conventions, D/H, and marginal
Monte-Carlo nuclear-rate/neutron-lifetime errors. The displayed grid spans
omega_b=.005–.04 and DeltaN=-3–7. The parent subsequently retrieved the
primary bytes into `bbn_inputs_v001/PRIMAT_Yp_DH_ErrorMC_1000_2026.dat`:
156343 ASCII bytes, 1327 lines, SHA256
`48f864ecda028e7c7b4306c777bf694b9d3a214c920736894103d3163f7adec3`.
A metadata-only independent parse finds 1300 eight-column rows, exactly a
complete 52-by-25 Cartesian grid with no duplicated coordinate pair.
Baryon nodes use .001 steps outside .020–.024 and .0002 steps inside it;
DeltaN nodes are -3,-2.5,-2,-1.5,-1,-.75,-.5,-.25,0,.25,.5,.75,1,
1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7. No abundance was scored.
Its header fixes T0=2.7255 K, neutron lifetime 878.4+/-0.5 s and ordinary
baseline N_eff=3.0440; 1000 Monte-Carlo draws vary nuclear rates and lifetime.
Pin this file and its header interpretation in the future calculation's
source manifest, together with the measured-abundance products, exact
column definitions and fixed-versus-inferred baryon treatment.
The
[2024 PRIMAT table in official CAMB](https://raw.githubusercontent.com/cmbant/CAMB/master/camb/PRIMAT_Yp_DH_ErrorMC_2024.dat)
is a separately versioned sensitivity/control asset, not a result-selected
replacement. The 2024 table has not been downloaded and neither table has
been interpolated in this work.

This makes a local interpolation-only abundance screen feasible. Use all
360 labels: the R=8192 rows lie in the displayed expansion-coordinate range;
the larger-radiation families exceed it and must remain explicitly
out-of-domain, not be extrapolated, discarded or automatically counted as
excluded. Extend those with a qualified BBN engine only if needed for their
scientific disposition. No full CMB code, new mode integration or remote GUI
run is needed for the in-domain first comparison.

Use node recovery, withheld-grid interpolation checks and two interpolation
orders to bound interpolation error below the intended abundance error
budget. A table is a compressed forward calculation, not a source of exact
abundances. Its marginal errors do not supply the helium–deuterium theoretical
cross-covariance. Report per-observable standardized residuals first; do not
claim a joint significance by inventing that covariance. The
[PRIMAT methods paper, section VI.2](https://arxiv.org/html/1801.08023v2)
explicitly combines observation and nuclear-rate prediction uncertainty and
distinguishes BBN-only inference from a CMB baryon prior.

A conservative joint-compatibility rule is possible without that covariance,
but its assumptions must be frozen too. Let r_i be each prediction-minus-
observation residual and sigma_i its justified total marginal error; only
independently sourced observational versus theoretical variances may be
added, while a deterministic interpolation bound b_i is added to the band,
not treated as a new Gaussian draw. If finite variances and zero-centred
error models are defensible, the union/Chebyshev bound gives

    Prob(any |r_i| > k sigma_i + b_i) <= 2/k^2.         (8)

It assumes no cross-observable independence. With separately justified
Gaussian marginals one can instead use two Bonferroni marginal bands, each
of coverage 1-alpha/2, to obtain at least 1-alpha simultaneous coverage.
Unknown or unmodelled systematic bias invalidates either nominal-coverage
claim and must be reported, not hidden in a covariance choice. No band level
or Gaussian model has yet been selected for scoring. Reporting the two
marginal residuals without a combined probability remains the minimal
honest output.

## 5. Two convention checks prevent a spurious observation claim

**Abundances rather than BBN-derived baryon parameters.** The already exposed
[Cooke, Pettini and Steidel deuterium result](https://arxiv.org/abs/1710.11129)
is (D/H)_P=(2.527+/-0.030)e-5. Its previously imported standard-BBN omega_b
values cannot be independent confirmations once (5) changes. Initially report
every fixed-reference prediction as an exploratory retest under all 18
retained conditional reference/baryon priors, not 18 independently validated
baryon densities. A proper
subsequent shared inference uses the measured abundance likelihood, updates
omega_b and consequently the SAME Omega_exc/action/vacuum calibration, rather
than varying baryons while leaving their dependent excitation budget frozen.

**Helium's actual definition.** A useful outside-calibration observable is
[Aver et al., section 4.2](https://arxiv.org/html/2010.04180v1):
Y_P=.2453+/- .0034. Their footnote defines
Y=4y[1-20(O/H)]/(1+4y). At the primordial intercept this uses the nucleon-number
convention 4y/(1+4y), despite the phrase “mass fraction.” Compare with the
table's `Yp^BBN`, allowing any explicitly bounded minor-nuclide correction,
not silently with its atomic-mass-corrected `Yp` column. The latter differs
systematically. Keep the observed helium systematic scope and do not combine
overlapping helium regressions as independent measurements. This public data
choice is now exposed; it is not a blinded experiment or claimed latest
consensus.

The table assumes T0=2.7255 K, versus 2.72548 K in the frozen photon reference.
For the simplest declared precision, bound this small difference explicitly.
For an exact eta match use the table's eta column and the candidate's owned
present baryon number/photon density, including its baryon-mass convention;
the leading fixed-mean-baryon-mass conversion is
omega_b,table=omega_b,candidate*(T0,table/T0,candidate)^3.
Do not change the underlying candidate's physical baryon density.

## 6. Concrete next test and what it will decide

1. Freeze the retrieved primary table/header and the two measured abundance
   products/definitions, together with the baryon treatment BEFORE scoring;
   verify its extra-radiation convention and retain the existing 360-state
   labels. Convert each r with (7) only under the checked expansion-only map.
2. Recover an ordinary zero-extra-density reference from the same table, then
   compute helium/D predictions for every in-domain fixed calibration with
   marginal observation, theory and interpolation uncertainties. Retain
   unsupported rows and all signs. No new best-case gap or abundance is picked.
3. The immediate independent discriminator is the helium response of the
   existing reference calibration; D is an exposed consistency channel.
   Report conditional tension/agreement, not a universal cutoff on r.
   If a common recalibration is needed, infer the one shared baryon/energy
   budget from both abundances and propagate it back into the galaxy and
   expansion candidate. A freely fitted radiation amplitude is not allowed:
   Q remains fixed by the same state and spectrum.

This is a small scientific calculation rather than another microscopic
preparation exercise. It tests the adopted scalar continuation with ordinary
BBN microphysics and no photon exchange. A failure would constrain that
construct or require an explicit, retested change of its early history; it
would neither exclude all UNT nor prove the separate continuous-network CMB
source. A success would qualify one early background test, not acoustic
structure, CMB polarization, growth or the origin of the photons.
