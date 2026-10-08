# Scale-only induced action: independent conditional review

2026-09-27. Analytic review only: no numerical work, microscopic rule
adoption, new physical spectrum, observational fit, or claim of a derived
dark-matter abundance.

## 1. Resident basis and explicit extra hypotheses

The review read the resident `ADOPTED_ACTION_DARK_CONSEQUENCES_V001.md`
and the relevant resident RIEHB theorem sections IB03--IB15a at
`../program-worktree/LANE_CROSS_RFT_MGFT_INDUCED_EH_BACKREACTION_V001/THEOREM.md`.
Their flags were checked before reading. RIEHB owns a conditional shell
calculation, the complete stress convention, the preterm/matching ledger,
and an explicit retained-field force obligation. It does not automatically
turn a running scale into a cosmological field.

The following calculation assumes all of these additional restrictions:

- Four-dimensional **metric** variation, with the Levi-Civita connection and
  signature (-+++); the effective metric and retained scalar are independent
  variables, with appropriate boundary terms/conditions.
- A sharp massless shell, fixed x=mu/kappa in (0,1), and fixed signed sums
  A_0 and A_1, including the admitted species, measure and constraint terms.
- No pre-existing/matching contributions to the two coefficients below,
  no additional scalar potential or explicit scalar kinetic term, and a
  controlled omitted-operator/loop remainder. These omissions require
  physical justification, not a convenient renormalization convention.
- kappa(chi) is a **physical retained scalar dependence**, not merely a
  Wilsonian bookkeeping scale; F(chi)>0 and F'(chi) is nonzero on the patch.
- Where matter is included in the displayed field equations, its action is
  minimally coupled to the Jordan metric and has no explicit chi dependence.

Promoting the cutoff and neglecting additional scalar derivative terms is a
new conditional closure. It is not already established by the metric-only
action. In particular, scalar derivative operators can occur at the same
derivative order as the Ricci term and need their own ownership/control.

## 2. Shell relation and signs

Write L=(4 pi)^2. The previously derived shell coefficients give

\[
 F=2C_R=-\frac{\hbar A_1}{L}(1-x^2)\kappa^2,
 \qquad
 V=-C_0=\frac{\hbar A_0}{4L}(1-x^4)\kappa^4
       =\beta F^2,
\]
\[
 \boxed{\beta=-\frac{C_0}{4C_R^2}
 =\frac{L}{4\hbar}\frac{A_0}{A_1^2}
                  \frac{1+x^2}{1-x^2}.}                 \tag{1}
\]

Positive stiffness requires A_1<0; positive vacuum potential additionally
requires A_0>0. Beta has inverse-action units when hbar is retained;
hbar beta is dimensionless. The absolute cutoff cancels from (1).
For a fixed positive A_0/A_1^2, choosing x cannot make beta smaller than
its x->0 limiting value L A_0/(4 hbar A_1^2). This is not a universal lower
bound across unowned spectra or cancellations.

## 3. Scalar variation, metric equation and the constant-field distinction

For the conditional Jordan action

\[
 S_J=\int\sqrt{-g}\,[FR/2-\beta F^2]+S_m[g,\Psi],
\]

the independent chi variation gives

\[
 F'(\chi)(R/2-2\beta F)=0.
\]

On the stipulated invertible patch,

\[
 R=4\beta F,\qquad
 FG_{\mu\nu}=T_{\mu\nu}-\beta F^2g_{\mu\nu}
     +\nabla_\mu\nabla_\nu F-g_{\mu\nu}\Box F.
                                                               \tag{2}
\]

Taking the metric trace and using the scalar equation gives

\[
 3\Box F=T,\qquad T=g^{\mu\nu}T_{\mu\nu}.             \tag{3}
\]

Jordan matter is conserved on shell under the stated coupling. Equation
(3) is compatible with that conservation, not permission to omit the scalar
variation or its exchange in another frame.

For beta nonzero, eliminating F gives

\[
 F=\frac{R}{4\beta},\qquad
 S_J=\int\sqrt{-g}\,\frac{R^2}{16\beta}+S_m.           \tag{4}
\]

This equivalence is restricted to the F>0 patch. In particular, the R=0
boundary is not part of that patch when beta is nonzero. For beta=0,
division by beta is invalid: the scalar equation instead requires R=0.
Zeros of F'(chi) also require separate treatment and cannot be passed
through by the displayed field redefinition.

In the genuinely varied model, a constant F requires T=0 pointwise.
Ordinary pressureless matter with nonzero trace therefore does not coexist
with constant F under this closed set of assumptions. For beta nonzero,
constant **Jordan** R also implies constant F. Vacuum permits constant-F
Einstein solutions with Lambda_J=beta F, but does not fix their overall
F value from (2)--(3).

By contrast, a constant externally prescribed cutoff which is **not varied**
gives fixed-coefficient Einstein gravity plus a cosmological constant, with
no added scalar equation and no added T=0 condition. An auxiliary scalar
that is varied is not the same thing as a prescribed parameter. Absence of
an explicit Jordan kinetic term does not make the former nondynamical:
the metric mixing supplies a scalar degree of freedom.

## 4. Einstein frame, matter exchange and the kinetic equation of state

Choose a positive constant reference F_*, and set

\[
 g^E_{\mu\nu}=\frac{F}{F_*}g_{\mu\nu},\qquad
 \phi=\sqrt{\frac{3F_*}{2}}\ln\frac{F}{F_*}.
\]

Up to the properly handled boundary term, the same action is

\[
 S_E=\int\sqrt{-g_E}
 \left[\frac{F_*}{2}R_E-\frac12(\partial\phi)^2-\beta F_*^2\right]
 +S_m[A^2(\phi)g_E,\Psi],
\]
\[
 A(\phi)=e^{-\phi/\sqrt{6F_*}},\qquad
 \alpha=\frac{d\ln A}{d\phi}=-\frac1{\sqrt{6F_*}}.
                                                               \tag{5}
\]

The potential is constant and the scalar is massless. This is the metric
R^2 equivalence, not its Palatini counterpart; changing the variational
formalism would change the model. The distinction is explicit in the
primary treatment by [Edery and Nakayama](https://arxiv.org/html/1902.07876v2).
The Jordan action has Brans--Dicke parameter omega_BD=0, as in the metric
scalar-tensor equivalence discussed by
[Chiba](https://arxiv.org/abs/astro-ph/0307338).
Neither reference supplies the missing UNT spectrum or authorizes this
physical cutoff promotion.

With the matter assumptions in Section 1, the Einstein-frame equations are

\[
 \Box_E\phi=-\alpha T_E,\qquad
 \nabla^E_\mu T_{m,E}^{\mu\nu}
       =\alpha T_E\nabla_E^\nu\phi.                   \tag{6}
\]

Scalar stress has the opposite divergence. For a homogeneous scalar,
K=dot(phi)^2/2 gives rho_phi=K+beta F_*^2 and
p_phi=K-beta F_*^2. The kinetic contribution has w_K=1 when K>0.
Only in the source-free homogeneous evolution does K scale as a_E^(-6).
Matter exchange in (6) generally changes that dilution law. Inhomogeneous
gradient stress need not have the homogeneous stiff-fluid form, and this
Einstein-frame decomposition is not a frame-independent Jordan dark-fluid
assignment.

There is no massive oscillatory mode in (5), and no derived cold component
with pressureless dilution and clustering. An instantaneous total w_phi=0
does not establish such a component. Nor may the original metric-only
calibration of C_R to an observed force coefficient be reused silently:
the added matter-coupled scalar requires the force-law calibration to be
checked. No observational exclusion is asserted here.

## 5. The scalar mass/curvature gate for a genuinely derived extension

For comparison, retain the same kinetic and matter assumptions but suppose
an actual spectral/matching calculation supplies a nonconstant

\[
 B(y)=\frac{V(F)}{F^2},\qquad y=\ln(F/F_*),\qquad
 U_E(\phi)=F_*^2B(y).
\]

At a stationary vacuum y_0, a positive vacuum and a stable scalar minimum
require

\[
 B(y_0)>0,\qquad B_y(y_0)=0,\qquad B_{yy}(y_0)>0.
\]

Canonical differentiation gives

\[
 m_{\rm eff}^2=\frac{2F_*}{3}B_{yy}(y_0),\qquad
 H_{\rm vac}^2=\frac{F_*}{3}B(y_0),\qquad
 \boxed{\frac{m_{\rm eff}^2}{H_{\rm vac}^2}
       =\frac{2B_{yy}(y_0)}{B(y_0)}.}                  \tag{7}
\]

Here c=1, and m_eff^2 is the inverse-length-squared coefficient of the
canonical Klein--Gordon equation; a rest energy would include hbar.
H_vac is the vacuum de Sitter curvature scale, not the Hubble rate of an
arbitrary matter-filled solution. Rapid small scalar oscillations would
require m_eff^2 much greater than the relevant H^2, as well as control of
matter coupling, amplitudes and gradients. This is a necessary candidate
screen, not a derived abundance or clustering result. The strict scale-only
case has B=beta and B_yy=0, so it does not pass the positive-mass gate.
Nonzero B_yy must come from owned physical content, not from fitting a
new potential to a desired dark component.

## 6. The shell expansion must hold on the resulting branch

Combining (1)--(2) gives a scale-independent on-shell check:

\[
 \frac{R}{\kappa^2}=-\frac{A_0}{A_1}(1+x^2),\qquad
 \frac{R}{\mu^2}=-\frac{A_0}{A_1}\frac{1+x^2}{x^2}.    \tag{8}
\]

RIEHB IB03 assumes small curvature relative to mu^2. Therefore a necessary
condition for this branch to stay in the expansion used to derive it is

\[
 \left|\frac{A_0}{A_1}\right|\frac{1+x^2}{x^2}\ll1.    \tag{9}
\]

Small Ricci scalar alone is not sufficient: the other curvature invariants,
retained momenta, scalar derivatives and omitted terms must also be
controlled. Changing absolute kappa cannot improve (9). The R^2 expression
in (4) is an algebraic representation of this restricted closure, not a
license to ignore the separate curvature-squared terms and remainder
already present in the original shell expansion.

## Verdict

The conditional equations are consistent and sharply testable. They give
a constant Einstein-frame potential plus a massless scalar, not a joint
derived cold-matter/vacuum allocation. They remove an adjustable vacuum
coefficient only if A_0, A_1, x, the zero preterms and the matching closure
are independently fixed. Otherwise the freedom has merely moved into beta.
Changing or rolling the absolute cutoff does not relax the constant
Einstein-frame potential. The additional field, its allowed variations,
derivative terms, matter couplings and validity window must be earned by
the same parent before this comparison can be adopted physically.

Same-family independent algebra checking agreed on the coefficient factor,
Jordan trace sign, Einstein-frame exchange signs, R^2 coefficient and
mass/Hubble ratio. That agreement is not independent empirical validation
and supplies none of the missing physical premises.
