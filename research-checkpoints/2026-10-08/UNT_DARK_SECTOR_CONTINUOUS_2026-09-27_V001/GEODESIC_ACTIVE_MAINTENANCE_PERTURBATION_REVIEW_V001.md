# Active/maintenance perturbations: exact geodesic screen and integrable escape

2026-09-27. Independent analytic review; no numerical execution or fitted
cosmology. Comparison construct: `AM_GEODESIC_CLOCK_COMPARISON_V001`.
The effective counterexample below is **not an adopted UNT
mechanism**. Its role is to identify the additional structure a physical
network explanation would actually need.

Resident sources read after flag checks: `I0_ALLOCATION_DERIVATION_V001.md`,
`CONSERVED_RECORD_STRESS_SCREEN_V001.md`, and
`CONSERVED_RECORD_STRESS_REVIEW_V001.md`. The older
`I0_ALLOCATION_ADVERSARIAL_V001.md` was compressed,dataless and was skipped
without hydration. The present review extends the homogeneous accounting
and conserved-current screen to a covariant perturbation-level test.

## 1. Stress assumptions and conservation

Assume the same adopted metric with signature (-+++), a normalized timelike
velocity u, and a closed pair whose *complete* assigned stresses really are

\[
 T_A^{\mu\nu}=\rho_Au^\mu u^\nu,\qquad
 T_M^{\mu\nu}=-Vg^{\mu\nu},\qquad \rho_A>0.
\]

Interaction, boundary and other stresses cannot be omitted to obtain this
form. Define h_mu^nu=delta_mu^nu+u_mu u^nu, D_mu=h_mu^nu nabla_nu,
dot f=u^mu nabla_mu f, theta=nabla_mu u^mu, and
a_mu=u^nu nabla_nu u_mu. Conservation gives exactly

\[
 \dot\rho_A+\theta\rho_A=-\dot V=:Q,
 \qquad \rho_Aa_\mu=D_\mu V.                         \tag{1}
\]

Q is positive for energy transfer into A. These are necessary equations,
not a derivation of either stress or a microscopic allocation law. No
Einstein background equation is needed to derive them.

## 2. Density-only closure: what the exact theorem actually requires

Add the conserved current nabla_mu(n u^mu)=0, n>0, and a differentiable
isentropic local energy density epsilon(n), without independent entropy,
clock, elastic or history variables. Its pressure is n epsilon'-epsilon,
so the proposed split is forced to be

\[
 \rho_A=n\epsilon',\qquad V=\epsilon-n\epsilon',\qquad
 D_\mu V=-n\epsilon''D_\mu n,
 \qquad c_s^2=\frac{n\epsilon''}{\epsilon'}.
                                                               \tag{2}
\]

Positive rho_A entails epsilon'>0. Equations (1)--(2) imply

\[
 a_\mu=-c_s^2D_\mu\ln n,\qquad
 Q=-\theta c_s^2\rho_A.                              \tag{3}
\]

If **exact geodesicity is required for general admitted inhomogeneous
density perturbations throughout an open density interval**, (2) forces
epsilon''=0 on that interval. Equivalently, exact c_s^2=0 there does so.
Therefore

\[
 \boxed{\epsilon(n)=mn+\Lambda,\quad m>0,\quad
 \rho_A=mn,\quad V=\Lambda,\quad Q=0.}                \tag{4}
\]

Positive maintenance density additionally requires Lambda>=0; neither
constant is numerically selected by this theorem. Conversely (4) supplies
the stated dust-plus-constant-vacuum stress and geodesic dust motion while
the regular single-stream description remains valid.

**Important restrictions:** a homogeneous solution has Dn=0 and does not
force epsilon''=0. Nor does one exceptional perturbation, a single density,
or a restricted family with no independent density gradients establish an
interval theorem. A function may be affine only on the tested interval.

Conventional coldness is not identical to exact c_s^2=0. For example, if
0<=c_s^2<=eta on [n_1,n_2], with n_2>n_1>0, then

\[
 0\le\ln\frac{\epsilon'(n_2)}{\epsilon'(n_1)}
   =\int_{n_1}^{n_2}c_s^2\,d\ln n
   \le\eta\ln\frac{n_2}{n_1}.                       \tag{5}
\]

Small positive pressure response over a finite density/scale range does
not imply exact affine energy. Conversely, absence of the fluid gradient
instability does not prove full microscopic, gravitational or nonlinear
stability.

There is also a sharp allocation consequence within this density-only
closure. Define the **energy** fraction f=rho_A/epsilon, with positive
epsilon and 0<f<1. Combining (1)--(3) gives

\[
 \dot f=-\theta f\big[(1-f)+c_s^2\big].               \tag{5a}
\]

An exactly fixed nontrivial fraction throughout an epoch with theta nonzero
therefore requires c_s^2=f-1<0. This is a conditional hydrodynamic gradient
failure in the stated one-variable isentropic regime. It is not a no-go
for all allocation histories, nonadiabatic exchange, extra fields or
elastic stresses, and f is not an operation-rate fraction by definition.

## 3. New integrability test for an exactly geodesic interacting pair

Without assuming epsilon(n), exact a_mu=0 in (1) requires D_mu V=0. Thus

\[
 \nabla_\mu V=Q u_\mu,\qquad Q=-\dot V.              \tag{6}
\]

This one-form must be exact, not merely a selected homogeneous exchange
history. Antisymmetrize its derivative:

\[
 0=\nabla_\mu(Qu_\nu)-\nabla_\nu(Qu_\mu).
                                                               \tag{7}
\]

Let omega_mu_nu=h_mu^alpha h_nu^beta nabla_[alpha u_beta] be the vorticity.
Spatial projection of (7), and contraction with u^mu, respectively give

\[
 Q\omega_{\mu\nu}=0,\qquad D_\mu Q+Qa_\mu=0.
                                                               \tag{8}
\]

Consequently, on an open regular region with geodesic flow and Q nonzero,

\[
 \omega_{\mu\nu}=0,\qquad D_\mu Q=0.                 \tag{9}
\]

Zero acceleration and zero vorticity imply that u_mu is locally a closed
one-form. On a suitable simply connected patch, write
u_mu=-partial_mu tau, with (partial tau)^2=-1 and dot tau=1. Then

\[
 V=V(\tau),\qquad Q=-V'(\tau).                        \tag{10}
\]

This is an integrability statement, not a choice of coordinate time or a
derived function V. Regions where Q vanishes need not have zero vorticity.
Global proper-time coordinates can also fail at caustics or through
topology; the statement is local and assumes a regular velocity field.

In particular, a proposed local Q=Q(rho_A) generally violates (9) in an
inhomogeneous geodesic regime unless its spatial gradients vanish or
additional owned variables supply the necessary dependence. Selecting a
background Q(t) is not a perturbation closure.

The covariant interacting-vacuum and gauge distinction has a primary
precedent in [Wands, De-Santiago and Wang (2012)](https://arxiv.org/abs/1203.6776).
The displayed integrability projections are derived here with the sign
convention Q positive into A.

## 4. Explicit effective counterexample: constrained proper-time field

To disprove an overstrong claim that *all* geodesic matter forces constant
vacuum, consider the following effective action, with a fixed potential
specified before solving it:

\[
 S_{AM}=\int d^4x\sqrt{-g}
 \left[-\frac{\ell}{2}
 (g^{\mu\nu}\partial_\mu\tau\partial_\nu\tau+1)-V(\tau)\right].
                                                               \tag{11}
\]

Here ell is a Lagrange multiplier, not an extra independently chosen
exchange history. Its variation imposes (partial tau)^2=-1. With
u_mu=-partial_mu tau, normalized gradient flow is geodesic. Metric variation
on the constraint surface gives

\[
 T^{\mu\nu}=\ell u^\mu u^\nu-Vg^{\mu\nu}.
\]

The tau equation gives

\[
 \nabla_\mu(\ell\nabla^\mu\tau)=V'(\tau),\qquad
 \nabla_\mu(\ell u^\mu)=-V'(\tau).                   \tag{12}
\]

Thus rho_A=ell and Q=-V' follow from the same action. Equations (1) and
(6)--(10) are satisfied, with a genuinely time-varying vacuum whenever
V' is nonzero. Positive ell must be imposed on the claimed solution branch.
For example, a specified V=V_0 exp(-gamma tau), V_0,gamma>0, gives
Q=gamma V>0; initially positive ell stays positive along any regular
flow with finite expansion. This example fixes a potential for the
counterexample, not a UNT law or an empirical fit.

The constrained-dust/potential construction is a known effective mechanism;
see [Chamseddine, Mukhanov and Vikman (2014), section 2](https://arxiv.org/html/1403.3961v2#S2),
with conventions translated to (-+++). Neither that literature nor the
algebra earns its application to UNT. An arbitrary potential remains an
unowned function unless its shape, parameters and physical clock are
derived from the parent. Its integration constants also leave abundance
unselected. This is a counterexample to an overbroad no-go, not a new
adoption or a stability/formation theorem.

## 5. Conserved records plus common energy per record close this escape

Impose in addition a conserved record current n u and the identification

\[
 \rho_A=m(\tau)n,
\]

where the same m applies across each proper-time slice. Equations (1),
(10), and current conservation then require

\[
 \boxed{n\,m'(\tau)=-V'(\tau).}                      \tag{13}
\]

Taking a spatial derivative gives m' D_mu n=0. If nonuniform n is admitted
on a slice, m'=0 there, and then V'=0 as well. The same obstruction appears
at linear order: common m and a nonzero exchange disallow a freely varying
comoving density perturbation. A homogeneous background can conceal this
problem because it only fixes n to one value at each time.

A nontrivial geodesic exchange therefore needs a genuinely different
closure: record formation/deletion with its complete stress and supply,
an energy-per-record variable that varies by flow line/history, or other
owned internal dynamics. Merely adding an entropy label is insufficient.
For a separately conserved n, an algebraic history reconstruction would
obey dot m=Q/n; in an inhomogeneous medium this is not a common m(tau).
That reconstruction alone does not derive a microscopic variable-mass
action or prove that its missing interaction forces cancel.

Likewise, replacing current conservation by nabla_mu(nu^mu)=Gamma while
retaining only epsilon(n) and its old stress produces a total energy
residual epsilon' Gamma. Formation does not repair the closed theory
unless its supplying dynamics or additional stress is included.

## 6. Gauge, sound speed and the practical next test

The invariant requirements are D_mu V=0 and D_mu Q=0, not vanishing
coordinate-space derivatives in every gauge. In a comoving proper-time
slicing, delta tau=0 gives delta V=delta Q=0. In another slicing,
delta V=V' delta tau need not vanish. Dropping that perturbation while
retaining a different velocity gauge can manufacture an incorrect force
or conservation equation.

The proper-time construction has zero rest-frame pressure perturbation,
delta p_rest=-delta V_rest=0, despite a generally nonzero background
adiabatic derivative. Where theta rho_A is nonzero,

\[
 c_a^2=\frac{\dot p}{\dot\rho_{\rm total}}
       =-\frac{Q}{\theta\rho_A}.                     \tag{14}
\]

This is not the rest-frame sound speed: the perturbations are nonadiabatic.
A negative (14) by itself is therefore not the density-only gradient
instability of Section 2. Zero rest-frame pressure response still does not
prove absence of caustics, nonlinear instabilities, extra modes or an
acceptable complete cosmology.

For a primary network candidate the next small test is to supply its
same-parent density/internal-variable/exchange law and test the exact
momentum equation and the curl condition (7) on admitted inhomogeneous
perturbations. If it claims conserved records with common per-record
energy, also test (13). Passing homogeneous allocation identities alone
does not pass these tests; adding a free V(tau) or Q after choosing a target
history does not constitute a prediction.
