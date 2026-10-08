# Finite-slice CMB preparation and an exact-material Boltzmann route V001

Status: analytical implementation design, 2026-09-29. No Boltzmann source receipt, compilation, transfer calculation, data acquisition or fit was performed. This is the conditional macroscopic scalar/Q=0 model, not a native derivation of photons, gravity, a hot origin, or the initial perturbation spectrum. A thermal finite interval is sufficient for this test; neither an initial singularity nor inflation is assumed.

## 1. The actual next calculation

Extend the already owned same-state expansion and recombination histories to **separate collisional photons, baryons, free-streaming ordinary neutrinos and the evolving hard barotropic fluid**, then project the same metric/photon solution into TT, TE, EE and CMB lensing. A small modification of a reviewed Einstein–Boltzmann implementation is preferable to extrapolating the Ai=101 collisionless transfer or substituting dust plus constant extra radiation.

The nonredundant target is the joint acoustic phase, relative peak heights, polarization, damping and Weyl-lensing/growth response of this one material state. A profiled distance/ruler, a homogeneous hard sound horizon, and an effective radiation density alone do not predict these observables.

Input notes fully read, with SHA256 of the reviewed bytes:

- `MACROSCOPIC_ALPHA_ONE_GALAXY_BVP_V001.md`: `64d98fff0681a81edce675049f6d72bb54c58b1d92f463f69fdd09dff8ed7bb3`.
- `ALPHA_ONE_FLRW_ENTROPY_INTERFACE_V001.md`: `48b6ba835fb84d30182bfb2233d17e49ad2b4cd2cb7e5f10def2ff934d94911e`.
- `FINITE_GAP_CMB_PERTURBATION_DISCRIMINATOR_V001.md`: `e0eae5fd62795a3619a402def4549927a44e716a99ed3b5f69203472c297c525`.
- `FINITE_SLICE_GROWTH_TRANSFER_DERIVATION_V001.md`: `3f1cb023a8f3726895eba4c7f99098762c624cdbf4accbc78921934a2c6fb7fe`.
- `FINITE_SLICE_GROWTH_TRANSFER_PROTOCOL_V001.md`: `36a3d0a0b297a48246e2563de30b610130990d82d8a0a8a8d33b3478f1f12800`.

## 2. Same-state material and metric interface

The separately adopted hard action is

\[
 S_H=C\beta\int\sqrt{-g}\,[I\sqrt{-\partial\theta\cdot\partial\theta}-e_R(I,h)]\,d^4x.
\]

On the homogeneous zero-source background, its exact current, not an additional microscopic averaging assumption, gives

\[
 I=I_1a^{-3},\quad \rho_H=C\beta e(I),\quad
 p_H=C\beta(I\omega-e),\quad \omega=e_I,\quad
 c_I^2=I e_{II}/\omega.
 \tag{1}
\]

Here rho is energy density and dimensionless c_I is sound speed divided by c. On the selected conserved polarization-entropy branch Q=0 the linear metric response is exactly that of this barotropic fluid, without hard anisotropic stress. The zero-soft geodesic-clock realization is one member; Q=0 is not permission to fit extra compensated initial functions. A microscopic native interpretation of (1) would separately need its physical clock/averaging qualification; that unresolved derivation must not be confused with the exact current of the explicitly adopted macroscopic action.

Use conformal **length** eta=c integral(dt/a), Newtonian potentials

\[
 ds^2=a^2[-(1+2\Phi)d\eta^2+(1-2\Psi)d\boldsymbol{x}^2],\quad
 \mathcal H=aH/c,\quad E_j=4\pi G a^2\rho_j/c^4.
\]

Primes below mean d/deta, theta is velocity divergence, and k has inverse-length units. The hard equations are

\[
 \delta_H'=-(1+w)(\theta_H-3\Psi')-3\mathcal H(c_I^2-w)\delta_H,
\]
\[
 \theta_H'=-\mathcal H(1-3c_I^2)\theta_H+
 k^2[\Phi+c_I^2\delta_H/(1+w)],\quad
 w'=-3\mathcal H(1+w)(c_I^2-w).
 \tag{2}
\]

No extra rest-frame entropy sound speed is allowed. The Einstein constraints/evolution include **every** species:

\[
 U=\sum_j E_j(1+w_j)\theta_j/k^2,\quad \Psi'=U-\mathcal H\Phi,
\]
\[
 k^2\Psi+3\mathcal H U+\sum_j E_j\delta_j=0,\quad
 k^2(\Psi-\Phi)=3\sum_j E_j(1+w_j)\sigma_j.
 \tag{3}
\]

The matched constant vacuum contributes to the background but not an independently tuned perturbation. The same calibrated hard energy/action is used at every epoch.

## 3. What the Ai=101 transfer must acquire

Let photon brightness be F(mu)=sum_l (-i)^l(2l+1)F_l P_l(mu), with F_0=delta_gamma, F_1=4theta_gamma/(3k), F_2=2sigma_gamma. Let G_l denote scalar linear-polarization brightness in the corresponding conventional Stokes basis, and Pi=F_2+G_0+G_2. Define the **positive** scattering rate Gamma_T=a n_e sigma_T in the chosen length units. Then

\[
 F_0'=-kF_1+4\Psi',\qquad
 F_1'=k(F_0-2F_2)/3+4k\Phi/3-
 \Gamma_T[F_1-4\theta_b/(3k)],
\]
\[
 F_2'=k(2F_1-3F_3)/5-\Gamma_T(F_2-\Pi/10),
\]
\[
 F_l'=k[lF_{l-1}-(l+1)F_{l+1}]/(2l+1)-\Gamma_TF_l\quad(l\ge3),
\]
\[
 G_l'=\mathrm{stream}_l-\Gamma_T[G_l-(\Pi/2)(\delta_{l0}+\delta_{l2}/5)].
 \tag{4}
\]

Ordinary massless neutrinos obey the unscattered brightness hierarchy, with their own initial distribution and shear, not the photon opacity or polarization. The current background's Neff=3.044 massless convention is retained as an explicit imported approximation, not a claim to model neutrino masses or all decoupling spectral corrections. The evolving hard fluid is never counted as additional free-streaming neutrinos.

The leading nonrelativistic baryon equations contain

\[
 \delta_b'=-\theta_b+3\Psi',\qquad
 \theta_b'=-\mathcal H\theta_b+k^2\Phi+
 k^2\delta p_b/\rho_b+\Gamma_T(\theta_\gamma-\theta_b)/R_b,
\quad R_b=3\rho_b/(4\rho_\gamma).
 \tag{5}
\]

The imported ordinary gas temperature/thermal-pressure closure and ionization/reionization history must supply the small baryonic pressure term consistently. Equations (5) state the usual nonrelativistic approximation, not an exact relativistic baryon thermochemistry theory. HYREC's same-H xe and Tm supply recombination, not automatically all perturbative gas/reionization inputs. Photon/neutrino combination used in the late collisionless diagnostic is invalid through Thomson coupling. Controlled tight-coupling and hierarchy/line-of-sight approximations are required; merely retaining a few radiation multipoles is not precision CMB closure. These ordinary conventions are consistent with the primary [Ma–Bertschinger Einstein–Boltzmann framework](https://arxiv.org/abs/astro-ph/9506072); the equations above specify our material substitution explicitly.

## 4. Finite preparation, not a hidden primordial prediction

A useful proposed initial endpoint is A_i=1/a_i=10^7, the already declared thermal-domain endpoint. This is a finite, post-annihilation thermal slice, not an a=0 extrapolation. For each history and intended k interval, the actual k/mathcalH_i, Gamma_T/k and material fractions must be evaluated before using a long-wave/tight-coupling expansion. Fully ionized initial composition above the atomic integration range is a named ordinary high-temperature approximation, not extrapolation of a recombination table. The entire 335-history set remains the input census; an implementation benchmark may be fixed prospectively without scientific selection.

There are two honest preparation choices:

**A: constrained finite-slice transfer.** Declare photon/neutrino angular distributions and polarization, species entropy/velocity relations and metric columns. For example, with zero initial shear, common velocity v and common delta_j/(1+w_j)=d, the exact two-column construction already owned is

\[
 \mathcal A_i=\sum_jE_j(1+w_j),\quad
 v_i=\mathcal H_i(\Psi_i+q_i)/\mathcal A_i,\quad
 d_i=-k^2\Psi_i/\mathcal A_i-3\mathcal H_i v_i,
 \quad q_i=\Psi_i'/\mathcal H_i.
 \tag{6}
\]

It can be applied at the new slice with all actual species. Unit columns are a transfer basis to be multiplied by perturbatively small stochastic amplitudes. They are not automatically the growing adiabatic mode or a native formation result. They also specify only a chosen finite subspace, not every possible photon, neutrino, hard or Q initial perturbation.

**B: regular adiabatic finite-history preparation.** Explicitly select a radiation-era nondecaying branch over a finite preceding interval. When radiation dominance, relativistic hard material and the long-wave limit are qualified, its leading relations in our convention are

\[
 \delta_{\gamma,\nu,H}=-2\Phi_*,\quad \delta_b=-3\Phi_*/2,
 \quad\theta_j=k^2\Phi_*/(2\mathcal H),\quad
 \sigma_\nu=(k/\mathcal H)^2\Phi_*/15,
\]
\[
 \Psi_*=(1+2R_\nu/5)\Phi_*,\qquad
 R_\nu=\rho_\nu/(\rho_\gamma+\rho_\nu+\rho_{H,\mathrm{rel}}).
 \tag{7}
\]

For example sigma_nu'=4theta_nu/15 and (3) give the coefficient 2/5. The hard radiation alters the denominator but contributes no shear. Actual finite-slice initialization needs higher-order material/tight-coupling corrections and exact constraint projection; the strict dust comparator needs its own appropriate regular series. Earlier-slice/series-order checks must agree on the transported state. Decaying-mode suppression can be demonstrated over a specified finite history, but cannot be inferred merely by calling data “primordial.” Neither choice derives the stochastic spectrum from native network dynamics.

With a single selected adiabatic random field, define its finite-slice normalization by zeta_i=-Psi_i+delta_rho_tot/[3(rho_tot+p_tot)], with all the same background species. A minimal explicit spectrum is P_zeta(k)=A_s(k/k_*)^(n_s-1): **two shared new calibration parameters**, not inflation as a premise or a network prediction. Ordinary reionization/foreground nuisance choices are additional and must be counted. Keeping both arbitrary columns instead requires their common covariance, or a specified coherent ratio; allowing an arbitrary function at each k would remove much of the claimed predictive leverage. No separate initial spectra for temperature, polarization, growth or lensing are permitted.

## 5. Exact finite-slice projection and its boundary term

Let tau(eta)=integral_eta^eta0 Gamma_T deta, g=Gamma_T exp(-tau), chi=eta0-eta, and B_gamma=F_gamma+4Phi. The angular form of (4) gives exactly

\[
 B_\gamma'+(ik\mu+\Gamma_T)B_\gamma
 =4(\Psi'+\Phi')+\Gamma_T[F_0+4\Phi-4i\mu\theta_b/k-\Pi P_2(\mu)/2].
\]

Thus the finite-slice observable contains

\[
 B_\gamma(\eta_0,\mu)=e^{-\tau_i-ik\mu\chi_i}B_{\gamma i}(\mu)
 +\int_{\eta_i}^{\eta_0}e^{-\tau-ik\mu\chi}
 \{4(\Psi'+\Phi')+\Gamma_T[F_0+4\Phi-4i\mu\theta_b/k-\Pi P_2/2]\}\,d\eta.
 \tag{8}
\]

Temperature is F/4; the subtracted observer 4Phi_0 affects only its monopole. The initial term may be dropped only with a sufficient optical-depth bound, not by assuming a zero-time origin. Polarization likewise retains any declared initial polarization, attenuated and propagated. For vanishing initial polarization and the conventional scalar E sign, the source term is

\[
 \Delta_l^E=\frac{3}{16}\sqrt{\frac{(l+2)!}{(l-2)!}}
 \int g\Pi\,\frac{j_l(k\chi)}{(k\chi)^2}\,d\eta.
 \tag{9}
\]

The factor 1/4 converts our brightness Pi to temperature normalization; a standard-code comparison must bind the Stokes/E sign used for TE. This expression is a spin-2 projection, not an additional source parameter.

At leading Born order, for a single source distance the lensing potential is

\[
 \varphi(\boldsymbol n)=-\int_0^{\chi_s}
 \frac{\chi_s-\chi}{\chi_s\chi}(\Phi+\Psi)(\eta_0-\chi,\chi\boldsymbol n)\,d\chi.
 \tag{10}
\]

The actual visibility/source distribution and lensing remapping use the same metric transfer. No new lensing amplitude is supplied. Unvalidated nonlinear CDM fitting formulas must not be silently applied to the new pressure fluid.

For an initial covariance P_ab(k), every scalar observable follows from

\[
 C_l^{XY}=4\pi\int d\ln k\sum_{ab}P_{ab}(k)
 \Delta_{l,a}^X(k)\Delta_{l,b}^Y(k).
 \tag{11}
\]

The same covariance predicts density and Weyl transfer/growth. Equations (1)–(11), an owned ordinary thermal/reionization history and a declared finite-slice state close the requested linear scalar calculation without an inflationary origin assertion. They do not explain why those photons or initial correlations exist.

## 6. Concrete CLASS changes, not a dust/Neff substitution

Bounded official source inspection on 2026-09-29 identifies a feasible route. The URLs below use `master` for discovery and are **not a pinned executable receipt**. A later bounded source receipt must pin one revision, enumerate required files and review the actual build; nothing was downloaded or executed here.

1. Add an exact hard-material background provider with rho_H(a), p_H(a), w(a), c_I²(a), their conservation derivative and the retained vacuum. The [background API](https://raw.githubusercontent.com/lesgourg/class_public/master/source/background.c) has a fluid w(a)/derivative/density-integral interface that can be extended. Use the already qualified action-energy map rather than fit a CPL/EDE curve.
2. Replace constant fluid sound speed at **all** stress and evolution sites by the same c_I²(a)=c_a²(a), use the true-fluid branch without PPF, and give the hard species the declared finite-slice data. The inspected [perturbation source](https://raw.githubusercontent.com/lesgourg/class_public/master/source/perturbations.c) uses constant `cs2_fld`; its ordinary fluid initial prescription is unsuitable for dominant early hard radiation. Newtonian gauge avoids its CDM-based synchronous gauge condition. Audit radiation/matter/equality and output-species bookkeeping so no hard density is lost, double-counted or implicitly replaced by CDM.
3. Supply xe, Tm, opacity/derivatives and gas-pressure inputs using the **same** H(a), H'(a), photon temperature, atomic helium and ordinary species conventions. The [thermodynamics module](https://raw.githubusercontent.com/lesgourg/class_public/master/source/thermodynamics.c) is a usable integration interface, but its bundled recombination implementation must not silently replace the reviewed FULL/external-H calculation or apply a standard BBN helium fit. Reionization remains a separately declared ordinary input. A bridge must be independently checked against the saved HYREC histories.
4. Extend initialization/start-time handling and preserve the boundary contribution (8), or certify it negligible. Expose the finite-slice spectrum through a reviewed analytic/table interface, not an automatic inference of inflation from an internal module name. CLASS's [primordial module](https://raw.githubusercontent.com/lesgourg/class_public/master/source/primordial.c) supports analytic spectra; our state normalization and parameter interpretation must be explicit.
5. Reuse photon/polarization projection and metric lensing only after source normalization, scalar constraints, standard dust/radiation limits, time/hierarchy/tight-coupling refinements and the actual same-state material identities pass. Early hard-fluid acoustic oscillations must not be dropped by a dark-energy attractor or fluid approximation.

An exact background normalization conversion is required. The saved convention has Omega_b+Omega_H+Omega_Lambda=1 **and adds** ordinary Omega_r, so its actual present H is H_cal sqrt(1+Omega_r). To enter a flat code whose H0 means actual present expansion, use

\[
 H_{0,\mathrm{code}}=H_{\mathrm{cal}}\sqrt{1+\Omega_r},\qquad
 \Omega_{j,\mathrm{code}}=\Omega_j/(1+\Omega_r)
 \tag{12}
\]

for all densities. Physical omega_b and T0 are unchanged. This preserves the already tested vacuum/density ledger; forcing the old H_cal and closure sum simultaneously would change it.

The official [Makefile](https://raw.githubusercontent.com/lesgourg/class_public/master/Makefile) has a local executable target, but its default `all` includes a Python-wrapper target that invokes pip installation and contains cleanup of an existing Python package. Those targets are **not** the in-scope route. Use only an explicitly reviewed project-local executable/library build with the already installed compiler, no installation/system cleanup, and preserve upstream/derived source separately. The [official README](https://raw.githubusercontent.com/lesgourg/class_public/master/README.md) supplies authorship/citation instructions. Full build safety and exact source pinning are future implementation work, not completed by this bounded inspection.

## 7. A test with real independent leverage

First produce transfer functions and spectra for a prospectively fixed representative history plus the matched ordinary-dust comparator, with the same initial-state freedom and no outcome-selected approximation. The main census remains all retained histories, not just those with a convenient radiation transition. Scientific failure and numerical failure must remain distinct.

Then freeze the data split and common stochastic/nuisance inference before scoring. Primary named targets are the [Planck 2018 TT/TE/EE likelihood products](https://arxiv.org/abs/1907.12875) and [lensing reconstruction](https://arxiv.org/abs/1807.06210), not a constant-free-streaming Neff posterior. For example, an explicitly declared temperature/low-polarization calibration of A_s, n_s and ordinary nuisances can yield correlated conditional TE/EE and lensing tests; their shared sky covariance must be retained. Alternatively a joint TTTEEE calibration can predict lensing/growth without separate amplitude freedom. Public familiarity is not blinding, and the old H0/Omega_m/BBN/Pantheon/DESI exposure remains disclosed.

The minimum new preparation assumption is therefore identifiable: one finite-history scalar initial state plus its common two-parameter power-law spectrum (and named ordinary nuisance inputs). This is a legitimate shared calibration, not evidence that UNT has explained the initial spectrum. Conversely, failure of a fully specified member against the joint peak/polarization/lensing pattern is informative in a way that another profiled ruler is not. The continuous-network thermal-photon origin lane remains a separate energy, spectrum and correlation-generation problem.
