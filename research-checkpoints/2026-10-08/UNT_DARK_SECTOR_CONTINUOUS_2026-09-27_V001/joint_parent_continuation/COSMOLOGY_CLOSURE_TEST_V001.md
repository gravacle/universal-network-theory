# Cosmological closure test: the galaxy law does not yet select the cosmological state

## Result and domain

This is an analytical test of the **adopted explicit mechanical-mode completion**, not a derivation from native UNT. It produces a useful decision, not another fitted example:

1. The relaxed galaxy response and its matched vacuum term admit an exact unexcited, freely falling-clock branch with ordinary GR plus that vacuum term. Baryonic inhomogeneity does not necessarily polarize the network on this branch.
2. On the zero-charge branch, linear cosmological growth is ordinary baryonic GR growth, not the static enhanced-force law with an infinite effective Newton constant.
3. If the previously used flat cosmological reference history and an external standard-BBN baryon benchmark are both retained, the zero-excitation completion has a large, explicit homogeneous energy shortfall. The reference-calibrated vacuum alone cannot close it. The required additional dustlike energy is approximately **7.10–7.35 times the baryonic rest-energy density** at the central inherited reference. This is a conditional energy target, not evidence that particles of an additional kind exist.

The constructive next discriminator is therefore **formation and state selection**: an owned network/clock preparation mechanism must explain why a galaxy enters the relaxed accelerated-clock branch, and whether the same mechanism supplies the cosmological state and energy budget. Replacing that question by a free mode abundance would erase the prediction.

The calculations below use the exact existing action in `EXPLICIT_MODE_COSMOLOGY_PATHWAY.md`, the constraints in `FINITE_MODE_CONSTRAINED_RESPONSE.md`, the force–volume relation in `../joint_parent_dynamics/SAME_PARENT_FORCE_VOLUME_LINK.md`, and the native limitations in `NATIVE_SOURCE_BRIDGE_DECISION.md` and `NATIVE_VOLUME_INCREMENT_PATHWAY.md`. No galaxy parameters, cosmological abundance, or observed velocity was fitted here.

## 1. The action fixes a constitutive relation, not its initial state

Use signature \((-+++)\), \(c=1\), \(M^2=(8\pi G)^{-1}\), and

\[
u_\mu=-\frac{\partial_\mu T}{\sqrt{-\partial T\cdot\partial T}},\quad
a_\mu=u^\nu\nabla_\nu u_\mu,\quad
h_\mu=\frac{a_\mu}{\sqrt{1+a^2/g_s^2}}.
\]

For the spatial modes \(y_{\delta\mu}u^\mu=0\), let \(v_\delta\) be their projected derivative along \(u\). The retained completion is

\[
S=\int\sqrt{-g}\,d^4x\left[\frac{M^2R}{2}
 +C\left\{\int\nu(\delta)d\delta
 \left(\frac{m_\delta v_\delta^2}{2}
 -\frac{\kappa\delta^2y_\delta^2}{2}
 -\frac{u_4(y_\delta^2)^2}{4}
 +\kappa\delta h\cdot y_\delta\right)-\Delta U\right\}\right]+S_b,
\]

where \(m_\delta>0\), \(\nu=A\delta\) on the stipulated interval, \(K_b=\kappa\int\nu d\delta\), and \(C=2M^2/K_b\). These are adopted fields, density and coupling, not an established native source map.

Relaxed static minimization gives the frozen galaxy law. The matching condition gives

\[
\frac{\Delta U}{K_b}=\int_0^\infty g[1-\mu(g)]\,dg,
\qquad H_v^2=\frac{2\Delta U}{3K_b}
\quad(c=1).
\tag{1}
\]

With acceleration in SI units, the last expression is \(H_v^2=2\Delta U/(3K_bc^2)\). Equation (1) is a relative energy difference promoted to an absolute gravitational baseline by the previously declared high-field matching condition. It must not be recounted as an independent measurement of cosmic acceleration; the existing value of \(g_s/a_0\) was calibrated from a cosmological reference.

Neither the static minimum nor (1) fixes \(m_\delta\), initial occupations, the clock congruence, or mode production. For example, changing every \(m_\delta\) by a positive factor leaves the complete static law and \(\Delta U\) unchanged while changing all small-amplitude mode frequencies. This is a genuine dynamical non-identifiability, not a small numerical error.

## 2. Exact zero-excitation branch and what selects a galaxy state

On FLRW, write \(q_\delta\) for physical spatial mode components. Their exact homogeneous equation is

\[
m_\delta(\ddot q_\delta+3H\dot q_\delta)
 +\kappa\delta^2q_\delta+u_4|q_\delta|^2q_\delta=0.
\tag{2}
\]

Thus \(q_\delta=\dot q_\delta=0\) remains zero. Define

\[
\mathcal T=\int\nu\frac{m_\delta|\dot q_\delta|^2}{2}d\delta,
\quad \mathcal V_2=\int\nu\frac{\kappa\delta^2|q_\delta|^2}{2}d\delta,
\quad \mathcal V_4=\int\nu\frac{u_4|q_\delta|^4}{4}d\delta.
\]

The homogeneous density and pressure are

\[
\rho_{\rm modes}=C(\Delta U+\mathcal T+\mathcal V_2+\mathcal V_4),\quad
p_{\rm modes}=C(-\Delta U+\mathcal T-\mathcal V_2-\mathcal V_4).
\tag{3}
\]

Their non-vacuum energy obeys

\[
\dot\rho_{\rm exc}+3H(\rho_{\rm exc}+p_{\rm exc})=0,
\qquad \dot\rho_{\rm exc}=-6HC\mathcal T.
\tag{4}
\]

In an expanding homogeneous universe, this action has no term that creates excitation from the exactly zero state. Fast quadratic oscillations can behave as dust **if excited**; that fact supplies neither their abundance nor their production mechanism. The quartic regime instead has a radiationlike averaged equation of state. A dust abundance cannot be inserted and then attributed to a galaxy-law prediction.

There is also an exact nonlinear observation, independently derived in `COUPLED_SPHERICAL_RESPONSE_PATHWAY_V001.md`. In any local GR solution with the matched vacuum, take a hypersurface-orthogonal geodesic normal and set

\[
a_\mu=0,\qquad y_\delta=0,\qquad v_\delta=0.
\tag{5}
\]

Locally a proper-time solution of \(\partial T\cdot\partial T=-1\) provides such a normal. The mode sources vanish, and every additional metric/clock variation vanishes except the constant \(\Delta U\). Equation (5) is consequently an invariant GR-plus-vacuum branch, including inhomogeneous baryonic solutions wherever the congruence remains regular. It need not survive a caustic, and this construction does not prescribe continuation through one.

The stationary galaxy construction instead chooses an **accelerated** normal aligned with the stationary geometry and modes near their relaxed minimum. The two configurations have physically different \(u_\mu\), acceleration and mode state; this is not merely changing coordinates in one solution. Existence of the attractive static branch does not prove that formation from cosmological initial data selects it. Conversely, existence of (5) does not prohibit another prepared branch. It identifies the missing prediction sharply: an initial-state and formation rule must choose between them without using the resulting rotation curve.

## 3. A curvature-independent background closure invariant

On the unexcited branch, with conserved ordinary baryons and radiation, normalize the present scale factor to one and put \(x=1+z\). Restoring conventional background coefficients gives

\[
H^2(x)=L+B x^3+R x^4+K x^2,\quad
L=H_v^2,\quad B=\frac{8\pi G\rho_{b0}}3,
\quad R=\frac{8\pi G\rho_{r0}}3.
\tag{6}
\]

Here densities are mass-equivalent densities; \(K\) is the present spatial-curvature contribution, with its sign retained. This is a definite conditional prediction once the ordinary species, curvature, and matched vacuum are specified. It does not follow from an assumed large effective \(G/\mu(0)\).

For independently measured \(L\) and \(R\), define

\[
I(x)=\frac{H^2(x)-L-Rx^4}{x^2}.
\]

Then the zero-excitation branch predicts the exact invariant

\[
\boxed{\frac{I(x_2)-I(x_1)}{x_2-x_1}=B}
\tag{7}
\]

for every distinct pair, independent of curvature. For a flat late-time comparison the still simpler quantity \([H^2-L]/x^3\) must be constant and equal to \(B\). Thus changing curvature cannot in general hide a missing dustlike background coefficient.

An eventual observation test should use an independently owned baryon determination and explicit expansion measurements, with their covariance and calibration. A BAO-derived \(H\) or CMB-inferred baryon density imports an early-universe ruler/model; those imports may be legitimate, but must be stated and tested within any alternative early cosmology. No new expansion-data fit was done here.

## 4. Quantitative, authenticated reference-budget test

`cosmology_closure_arithmetic.py` authenticates all ancestors of the saved `SHAPE_REFERENCE_FROZEN.json` and the reference result payload. It retains **all nine** previously declared reference combinations and **both** baryon benchmarks, giving 18 rows in `COSMOLOGY_CLOSURE_ARITHMETIC.json`. This is stdlib arithmetic only, not a new cosmological evolution or an observational fit.

For an external conditional benchmark, Cooke, Pettini and Steidel give \(\omega_b\equiv\Omega_bh^2=0.02166\) with their theoretical nuclear rate, and \(0.02235\) with the empirical alternative, in equations 12 and 14. Both alternatives and their separate measurement/nuclear errors are retained in the JSON. This is a **standard-BBN** inference, not a native UNT baryon derivation or a claim to the latest cosmological estimate. Its assumptions include the early expansion/microphysics and the connection of primordial to present baryon abundance. [Primary paper](https://arxiv.org/pdf/1710.11129)

The inherited central reference is the flat-model \(H_0=73.6\) km s\(^{-1}\) Mpc\(^{-1}\), \(\Omega_{\Lambda}=0.666\) combination from Pantheon+, previously used to set the second force scale. Its \(\Omega_m=0.334\) and expansion history are model-dependent reference quantities, **not an independent new measurement validating this completion**. [Primary paper, Table 3](https://arxiv.org/html/2202.04077v2)

In the inherited units, \(B=10^4\omega_b\) and \(L=3607.69536\) (km s\(^{-1}\) Mpc\(^{-1}\))\(^2\), so \(H_v=60.0641\) km s\(^{-1}\) Mpc\(^{-1}\). Flat, zero-excitation, radiation-neglected arithmetic gives:

| Quantity | BBN theoretical-rate benchmark | BBN empirical-rate benchmark |
|---|---:|---:|
| Predicted zero-excitation \(H_0\), km s\(^{-1}\) Mpc\(^{-1}\) | 61.8409 | 61.8967 |
| Predicted \(H(z=1)\), same units | 73.0787 | 73.4554 |
| Inherited reference \(H(z=1)\), same units | 134.4686 | 134.4686 |
| Required extra dustlike \(\omega_{\rm exc}\), if that reference is adopted | 0.1592665 | 0.1585765 |
| Required \(\rho_{\rm exc}/\rho_b\), same condition | 7.3530 | 7.0951 |

The required coefficient is exactly

\[
E\equiv H_{0,\rm ref}^2-L-B,\qquad
\omega_{\rm exc}=E/10^4,\qquad
\frac{\rho_{\rm exc}}{\rho_b}=\frac EB.
\tag{8}
\]

This ratio is saved for every one of the 18 combinations; it is not a best-fit abundance. If an excited-mode state were proposed to reproduce that reference, its averaged positive energy and pressure would have to supply the corresponding history, with production and conservation accounted for. A field-response enhancement without an added homogeneous stress cannot do that in (2)–(6). This does **not** establish that the missing stress must be a new particle species; network excitations are one possible source, but the current action does not generate them from zero homogeneous modes.

One can set \(K=E\) solely to close the reference value at \(z=0\). Even this illustrative curvature change leaves the exact difference

\[
H_{\rm ref}^2(x)-H_{K=E}^2(x)=E x^2(x-1),
\tag{9}
\]

so it cannot recover the reference shape at other redshifts. The JSON retains this calculation without adopting that curvature or fitting it. Its reported dust-plus-vacuum age is only the mathematical extrapolation of that ideal two-component model, not a full radiation-era age calculation.

The result is a **conditional closure discrepancy**, not a statistical rejection of UNT or an independent fit to expansion data. It prevents the circular assertion that a cosmologically calibrated vacuum plus a successful static galaxy response already predicts a complete baryon-only cosmology.

## 5. Linear growth: conserved charge, not an automatic force multiplier

On a general flat FLRW background, use Newtonian gauge and \(T=t+\pi\), and define

\[
\Upsilon=\Phi-\dot\pi,\qquad
\widehat a_i=\partial_i\Upsilon/a,\qquad
B_i=\int\nu\kappa\delta q_{\delta i}d\delta.
\]

At quadratic order about zero homogeneous modes, the clock-dependent coupling is \(C a^2 B_i\partial_i\Upsilon\). Its variation gives, for arbitrary \(H(t)\),

\[
\partial_t\left[a^2\partial_iB_i\right]=0,
\quad \delta\rho_P=\frac Ca\partial_iB_i,
\quad \delta p_P=\delta T^0{}_{i,P}=\Pi_{ij,P}=0.
\tag{10}
\]

Hence \(\delta\rho_P\propto a^{-3}\), but its sign is unrestricted and its mean is zero for periodic or fluxless boundaries. It is an initial polarization-charge perturbation, not a positive homogeneous dust abundance. Zero initial charge implies zero extra linear metric stress. In particular, the full long-wavelength Einstein constraints are then those of ordinary GR plus the matched vacuum; the static susceptibility cannot be substituted into them as an infinite gravitational coupling. Equation (10) is not to be divided by a zero Fourier wave number; the homogeneous sector is (2)–(6).

For pressureless baryons, negligible radiation/anisotropic stress, and subhorizon modes \(k/a\gg H\), the zero-charge growth equation is

\[
\ddot\delta_b+2H\dot\delta_b-4\pi G\rho_b\delta_b=0,
\]

or, with \(N=\ln a\),

\[
\delta_{b,NN}+\left(2+\frac{d\ln H}{dN}\right)\delta_{b,N}
 -\frac32\Omega_b(a)\delta_b=0.
\tag{11}
\]

For the flat dust-plus-vacuum background only, the growing solution normalized to \(D\sim a\) in its ideal early dust regime is

\[
D(a)=\frac{5B}{2}\,H(a)\int_0^a\frac{da'}{a'^3H^3(a')}.
\tag{12}
\]

This expression is not a radiation-era, recombination, baryonic-pressure or primordial-spectrum calculation. It supplies a definite test once those boundary conditions are owned, not a new claim of a successful structure-formation history.

If the initial charge is nonzero, replace the right side of (11) by \((3/2)\Omega_b s(\mathbf x)\), where \(s=\delta\rho_P/\rho_b\) is time-independent for conserved dust. Equivalently \(\delta_b+s\) obeys the homogeneous growth equation. A chosen \(s\) changes the initial spatial source; it neither changes the homogeneous coefficient \(B\) nor predicts its own amplitude or correlations. Modes outside the subhorizon regime require the complete metric/clock constraints, not this reduced equation.

## 6. What actually advances the program

The surviving useful question is now sufficiently sharp to calculate without an arbitrary extra density:

- Specify native or otherwise independently owned clock and record initial data, evolve a baryonic inhomogeneity, and determine whether it stays on (5) or develops the accelerated, relaxed galaxy branch. The simultaneous clock constraints matter; merely minimizing a static energy answers a different question.
- If record formation transfers energy to modes, derive that source term and its opposite work/energy transfer. The current homogeneous zero state cannot supply the target (8). The target is a diagnostic conditional on the inherited reference, not an abundance to insert by hand.
- Keep fixed-volume native response, absolute volume stress, and creation of new network degrees of freedom separate. The existing native response commutator constrains a spectral moment, not the full volume coupling or population. Along a growth path, energy can be assigned to pressure or chemical work differently until that coupling is specified; a geometry-only relabeling cannot choose it.

This is a stronger position than treating the static law as cosmological closure: it provides an exact null branch, a measurable background invariant, an explicit conditional energy target, and a growth equation. Any proposed network formation mechanism must now overcome or select these precisely stated alternatives while conserving the energy it uses.

## Verification and scope

The small arithmetic ran once, preserved all 18 combinations and authenticated inherited bytes. No field, source profile, law parameter, or frozen evidence was edited. The FLRW charge equation and growth reduction were independently checked by the analytical lane. The exact nonlinear branch has an independent spherical formulation in the named companion note. This document does not claim a native derivation, an observational cosmology fit, a proof of attractor selection, continuation through clock caustics, or completion of the joint dark program.
