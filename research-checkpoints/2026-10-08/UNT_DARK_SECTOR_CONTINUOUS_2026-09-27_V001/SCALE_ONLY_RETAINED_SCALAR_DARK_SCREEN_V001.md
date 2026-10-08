# Scale-only retained scalar: conditional joint dark-sector screen

2026-09-27. Exact algebra for an explicitly conditional leading action; no numerical run, new adopted field, fitted coefficient, or claim of a same-parent scalar derivation.

## 1. Read evidence and the additional interface

The following resident files were read in full after flag checks:

- ADOPTED_ACTION_DARK_CONSEQUENCES_V001.md, SHA256 beadea3fea04397df1cc768bcde8ede5b994128eb936294f44c3a7db7e57d64e.
- program-worktree/LANE_CROSS_RFT_MGFT_INDUCED_EH_BACKREACTION_V001/THEOREM.md (RIEHB), SHA256 e73c077d1402ebab9a6061b060b9b24e9ac323b25809cccc706f4365da7a5e2f.

RIEHB supplies the conditional common-metric finite-shell calculation (IBP.1–3, IB06–IB10), permits pre/matching terms (IBP.4), and requires all independent collective forces to be varied rather than discarded (IB15a). It does not identify its crossover with a retained scalar or derive that scalar's gradient action.

For this screen only, suppose a physical retained scalar χ controls κ = κ(χ) > 0, with fixed shell ratio x = μ/κ in (0,1), fixed complete signed spectral sums A_0 and A_1 in the IB06 convention, and no mass/potential threshold at these leading orders. Assume no preterms, matching terms, additional retained vacuum potential or Jordan kinetic term. These omissions are physical restrictions, not a subtraction justified by the desired result. Use the metric, Levi-Civita variational formalism in four dimensions with signature (−+++), independent metric and χ variations, and owned boundary conditions.

χ is not thereby a conserved record density, operation rate, or physical clock. Promoting a Wilsonian bookkeeping scale to a field is not this construction. For a spacetime-varying physical crossover, the actual retained derivative operators must be computed: the constant-endpoint shell calculation does not prove their absence. Metric/collective tangent completeness also remains required if g is composite.

## 2. Exact shell coefficient and sign ledger

With L = (4π)² and the explicit ħ convention of IB06,

\[
 C_R=-\frac{\hbar A_1}{2L}(1-x^2)\kappa^2,
 \qquad C_0=-\frac{\hbar A_0}{4L}(1-x^4)\kappa^4.
\]

Healthy positive stiffness and positive vacuum density require A_1 < 0 and A_0 > 0 separately. Set F = 2C_R > 0 and V = −C_0 > 0. Then

\[
 V=\beta F^2,\qquad
 \boxed{\beta=\frac{V}{F^2}
 =-\frac{C_0}{4C_R^2}
 =\frac{L}{4\hbar}\frac{A_0}{A_1^2}
                    \frac{1+x^2}{1-x^2}>0.}          \tag{1}
\]

β has inverse-action units when ħ is explicit; ħβ is dimensionless. The absolute κ cancels. The A_i here are the convention-matched complete signed shell sums, not an unconverted field-count supertrace.

For the remainder of the field-theory derivation set **ħ = c = 1** consistently. Write M² for a fixed positive Einstein-frame normalization, conventionally the reduced Planck mass squared in these units. Choosing this reference does not derive a physical Planck scale, and restoring units in (1) does not change the scale-free conclusion.

## 3. Einstein-frame field, potential, and matter coupling

The conditional Jordan action is

\[
 S_J=\int d^4x\sqrt{-g_J}\,[F(\chi)R_J/2-V(\chi)]
               +S_m[g_J,\psi].                       \tag{2}
\]

The displayed matter premise is Jordan-minimal coupling with no further explicit χ dependence. On a regular F > 0 patch with F_χ ≠ 0, define

\[
 g^E_{\mu\nu}=\frac{F}{M^2}g^J_{\mu\nu},\quad
 y=\ln(F/M^2),\quad
 \phi=\sqrt{\frac32}\,M y.                            \tag{3}
\]

Using R_J = (F/M²)[R_E + 3□_E y − (3/2)(∂y)²_E], the volume factor cancels the variable Ricci coefficient. Removing only the admitted total derivative gives

\[
 S_E=\int d^4x\sqrt{-g_E}
 \left[\frac{M^2}{2}R_E-\frac12(\partial\phi)^2_E-U(\phi)\right]
           +S_m[A^2(\phi)g_E,\psi],
\]
\[
 \boxed{U=M^4\frac{V}{F^2}=\beta M^4,\quad
 A^2=\frac{M^2}{F},\quad
 A=e^{-\phi/(\sqrt6 M)},\quad
 \alpha:=\frac{d\ln A}{d\phi}=-\frac1{\sqrt6 M}.}      \tag{4}
\]

The transformation and metric R²/constant-potential connection have an explicit primary-literature cross-check in Edery and Nakayama, [Generating Einstein gravity, cosmological constant and Higgs mass from restricted Weyl invariance](https://arxiv.org/pdf/1502.05932), §2–2.1, equations (2)–(6). Only that mathematical check is used; their Higgs sector, parameter choices and symmetry claims are not imported into UNT.

For constant shell sums, φ = √6 M ln(κ/κ_*). Nonzero spacetime gradients of κ therefore generate the displayed positive kinetic term; they cannot be dropped while retaining a varying coefficient. A constant background κ does not remove scalar perturbations if F_χ ≠ 0. If F is instead independent of χ on the field domain, (3) is not an invertible scalar redefinition and no additional scalar follows from this calculation.

In the truncated action (4), U_φφ = 0: there is no vacuum restoring mass or preferred finite value of F. With Jordan-minimal matter the scalar is not generally uncoupled:

\[
 \Box_E\phi=U_\phi-\alpha T_E=-\alpha T_E,
 \qquad \nabla^E_\mu T_{m,E}^{\mu\nu}
                       =\alpha T_E\nabla_E^\nu\phi.  \tag{5}
\]

The scalar stress has the compensating divergence. This universal conformal coupling is fixed by (2), not an independent dark charge. Pure-metric calibration of C_R to a measured Newton constant does not automatically survive the addition of an unsuppressed scalar exchange; the full operational gravity interface must be checked. No numerical observational exclusion is asserted here.

In vacuum or with T_E = 0, a homogeneous scalar in an assumed expanding FLRW Einstein-frame solution obeys

\[
 \ddot\phi+3H_E\dot\phi=0,\quad
 K=\dot\phi^2/2\propto a_E^{-6},\quad
 \rho_\phi=K+U_0,\quad p_\phi=K-U_0.                 \tag{6}
\]

Thus the homogeneous kinetic component has w = 1, while the constant potential has w = −1. The canonical scalar's propagation speed is the common metric light speed; it is not a massive, rapidly oscillating cold-matter mode. This is an Einstein-frame component statement, not a license to equate frame-dependent fluid decompositions. With nonzero matter trace, (5) replaces the free a_E^{-6} scaling. The result excludes the proposed *vacuum plus cold scalar matter* realization from this scale-only degree of freedom; it does not exclude every modified-gravity mimic of a dark-matter observation or another retained matter sector.

## 4. No Jordan kinetic term does not remove the scalar dynamics

Varying independent F in (2), equivalently varying χ when F_χ ≠ 0, gives

\[
 R_J=4\beta F.
\]

Eliminating this auxiliary variable on the regular positive-F branch yields the classically equivalent metric action

\[
 S_{\rm grav}=\int d^4x\sqrt{-g_J}\,
                                  \frac{R_J^2}{16\beta}.        \tag{7}
\]

It is not a nondynamical matter variable. The metric equation and its trace are

\[
 F G^J_{\mu\nu}=T^J_{\mu\nu}-\beta F^2g^J_{\mu\nu}
       +\nabla_\mu\nabla_\nu F-g^J_{\mu\nu}\Box_JF,
 \qquad \boxed{3\Box_JF=T_J.}                       \tag{8}
\]

The scalar dynamics reside in the metric mixing. An exactly constant F in this varied model requires T_J = 0; it is not the generic GR solution with arbitrary traceful matter. By contrast, fixing κ as an external constant and not varying any scalar leaves the ordinary constant-coefficient Einstein–Hilbert plus vacuum action, with no scalar equation. These are different completions.

Equation (7) is not the separately generated curvature-squared coefficient of IB07; it is a rewriting of (2). Omitted shell higher-curvature operators must still be bounded. Nor does the metric result transfer to a separately varied Palatini connection, whose scalar content differs: Edery and Nakayama's primary paper [Palatini formulation of pure R² gravity yields Einstein gravity with no massless scalar](https://arxiv.org/pdf/1902.07876) explicitly distinguishes the two formulations. No quantum path-integral measure equivalence is claimed by the classical substitution here.

There is an additional source-validity test. Combining the scalar equation with (1), at a constant-field vacuum or locally wherever that equation is used, gives

\[
 \frac{R_J}{\mu^2}
 =-\frac{A_0}{A_1}\frac{1+x^2}{x^2}.                 \tag{9}
\]

RIEHB IBP.3 requires curvature small relative to μ². Therefore |A_0/A_1|(1+x²)/x² ≪ 1 is necessary for this on-shell shell truncation, independently of absolute κ. A Weyl change of variables cannot repair a failed derivative expansion. Tensor curvature, retained momenta, gradients and the other IB11 remainders must also pass; (9) alone is not sufficient.

## 5. Minimal constructive departure and a joint acceptance criterion

For any future **owned matched** functions F > 0 and V, retain the same conditional zero-Jordan-kinetic, monotone-F interface and define

\[
 B(y)=\frac{V}{F^2},\qquad y=\ln(F/M^2).
\]

A stationary constant-field vacuum requires B_y = 0. At such a point,

\[
 U_0=M^4B,\quad
 m_\phi^2=\frac{2M^2}{3}B_{yy},\quad
 H_{\rm vac}^2=\frac{M^2}{3}B,\quad
 \boxed{\frac{m_\phi^2}{H_{\rm vac}^2}=2\frac{B_{yy}}B.}        \tag{10}
\]

Here H_vac is the flat-slicing Einstein-frame de Sitter expansion scale of the constant-field vacuum, not the instantaneous H of an arbitrary curved or matter-filled FLRW solution. Positive vacuum energy and a locally stable scalar mass require B > 0, B_y = 0, and B_yy > 0. A candidate cold-oscillation regime further needs 2B_yy/B ≫ 1, as well as a supplied oscillation amplitude/history, suitable wavelengths and matter-coupling/decay checks. These inequalities do not by themselves establish dust, abundance or viability. Scale-only B = β fails the mass gate at every κ.

The smallest new spectral/matching datum is thus a same-parent, nonconstant B with an actual positive, nondegenerate minimum—not an independently chosen scalar mass. Existing RIEHB slots capable of changing the ratio include owned mass thresholds (IB09), a state-dependent dimensionless spectral/threshold ratio or crossover profile, and physically fixed pre/matching contributions (IB04a, IB10). Each must be computed with its associated forces and derivatives. None is shown in the read sources to supply the required χ-dependent minimum; writing a desired function is not that derivation.

If the actual retained action has −Z_J(χ)(∂χ)²/2, the canonical metric becomes

\[
 \left(\frac{d\phi}{d\chi}\right)^2
 =M^2\left[\frac{Z_J}{F}
             +\frac32\left(\frac{F_\chi}{F}\right)^2\right].   \tag{11}
\]

Its positivity and normalization must be checked and the mass test recomputed; (10) is then not the general formula. A healthy two-derivative kinetic term alone does not turn a constant B into a massive vacuum excitation. Explicit matter dependence, a conserved-current interpretation of χ, higher derivatives or nonlocal terms likewise change the stated screen and require their own owned variation.

Next bounded calculation: obtain the first actual same-parent spectral or matching departure and evaluate B, B_y and B_yy at its stationary point, together with the derivative-expansion bounds. This tests whether a scale-related field can supply both a positive vacuum term and a cold-matter candidate without fitting either dark-density target. Until then, the scale-only action gives a vacuum-form constant plus a massless scalar, not the requested complete joint mechanism; this is not a no-go for the primary active/maintenance explanation or for UNT.
