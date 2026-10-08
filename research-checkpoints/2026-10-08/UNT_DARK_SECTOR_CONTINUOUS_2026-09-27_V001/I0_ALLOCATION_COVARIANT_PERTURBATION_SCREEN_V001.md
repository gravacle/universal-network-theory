# I0 active/maintenance allocation: covariant cold-response screen

Date: 2026-09-27. Construct ID: **AM_LOCAL_DENSITY_COLD_SCREEN_V001**.
Conditional analytical acceptance test, not a newly adopted UNT physical rule. No numerical run, cosmological target, new volume law, or parameter choice.

## 1. Scope and established interface

Read in full after resident flag checks:

- I0_ALLOCATION_DERIVATION_V001.md, SHA256 c7302c7f5b22699a3f356dad3b49106655e58984e0f98774c013d3e70f64b10a.
- CONSERVED_RECORD_STRESS_SCREEN_V001.md, SHA256 7e4fbb948014c00e0144b980273317749ea574cacd1640fd2ab1a47c957ccc2a.

The first note leaves a homogeneous energy allocation function unclosed; the second derives the stress of an explicitly conditional conserved-current action. This note imposes the missing momentum/inhomogeneous-response test on that density-only specialization.

The covariant interacting-vacuum framework and the distinction between geodesic and barotropic completions are established, not new discoveries: see Wands, De-Santiago and Wang, [Inhomogeneous vacuum energy](https://arxiv.org/html/1203.6776), sections II, III.3 and IV.2, inspected here. The contribution below is its application to the primary A/M allocation conditions, including exact coldness and fixed-share tests; it is not a microscopic UNT derivation. Our Q is positive into the active component, opposite to that paper's positive-into-vacuum convention.

Adopt only for this screen a differentiable common metric of signature (−+++), an active timelike velocity u with u·u = −1, and independently justified component stresses

\[
 T_A^{\mu\nu}=\rho_Au^\mu u^\nu,\qquad
 T_M^{\mu\nu}=-\rho_Mg^{\mu\nu},\qquad
 \nabla_\mu(T_A^{\mu\nu}+T_M^{\mu\nu})=0.             \tag{1}
\]

Take ρ_A > 0; additionally require ρ_M ≥ 0 when both are claimed to be positive dark components. The vacuum-form term has no independent velocity. The density-only restriction introduced below is an extra constitutive premise. Operation rates, causal capacity and storage counts are not these energy densities without an owned map. No Einstein field equation is required for the conservation algebra, but the common metric and variational stress interpretation are conditional physical imports.

## 2. The exchange is a four-vector, not just a background power

Define dot X = u^μ∇_μX, θ = ∇_μu^μ, a^μ = u^ν∇_νu^μ, h^{μν} = g^{μν}+u^μu^ν, and D^μX = h^{μν}∇_νX. Equation (1) fixes

\[
 \nabla_\mu T_A^{\mu\nu}=\nabla^\nu\rho_M
 =Q u^\nu+D^\nu\rho_M,\qquad Q=-\dot\rho_M.         \tag{2}
\]

Contraction with u and orthogonal projection give, respectively,

\[
 \boxed{\dot\rho_A+\theta\rho_A=-\dot\rho_M=Q,\qquad
          \rho_Aa^\mu=D^\mu\rho_M.}                  \tag{3}
\]

Thus a spatially varying maintenance energy generally forces the active component. A chosen homogeneous Q(t) does not supply its momentum transfer or perturbations. In a closed pair the transfer one-form is a gradient, so a proposed complete Q_μ must also satisfy ∇_[μQ_ν] = 0 locally.

Exactly geodesic active motion requires D^μρ_M = 0, not necessarily dot ρ_M = 0. A time-dependent but comoving-homogeneous vacuum is possible in a more general completion. Geodesic means zero proper acceleration relative to the same metric; it does not mean fixed coordinate position, absence of gravity, or absence of gravitational clustering.

## 3. Conserved density forces exchange and sound response to agree

Now additionally assume a timelike conserved transported current n u^μ, n > 0, with ∇_μ(nu^μ) = 0, and the local isentropic energy law ε(n) from the prior current-action screen. Let ε be C² and ε′ > 0 on the tested density interval. There are no independent entropy, memory, elastic or nonlocal variables in this closure. Its actual variational stress has

\[
 \rho=\epsilon(n),\quad p=n\epsilon'-\epsilon,\quad
 \rho_A=\rho+p=n\epsilon',\quad
 \rho_M=-p=\epsilon-n\epsilon'.                     \tag{4}
\]

The last two equalities are the dust/vacuum decomposition of this stress, not evidence by themselves for a microscopic A/M mechanism. Their derivatives fix both perturbations and exchange:

\[
 D^\mu\rho_M=-n\epsilon''D^\mu n,\qquad
 c_s^2=\frac{dp}{d\rho}=\frac{n\epsilon''}{\epsilon'},\qquad
 \boxed{a^\mu=-c_s^2D^\mu\ln n.}                    \tag{5}
\]

Here c_s is the local adiabatic propagation speed in units of the adopted common cone. It follows from δp = nε″δn and δρ = ε′δn in a local rest frame. This is a constitutive response, not a fixed-metric approximation. In a full perturbation calculation a^μ, D^μ and the field equations include the perturbed metric. Ordinary gravitational Jeans growth is distinct from the short-wavelength fluid gradient instability associated with c_s² < 0.

Since dot n = −θn, the same ε fixes

\[
 \boxed{\dot\rho_M=\theta c_s^2\rho_A,\quad
 Q=-\theta c_s^2\rho_A,\quad
 \frac{d\rho_M}{d\ln n}=-c_s^2\rho_A,\quad
 \frac{d\ln\rho_A}{d\ln n}=1+c_s^2.}                \tag{6}
\]

A background exchange fitted independently of (5) and (6) is not a completion of this density-only action.

### Exact coldness on an interval versus at one point

Require exact geodesicity for admitted inhomogeneous perturbations with nonzero comoving density gradients at every n in a connected open interval I. Equations (5), with nε′ > 0, force ε″ = 0 throughout I. Conversely that condition removes the pressure force there. Hence

\[
 \boxed{\epsilon(n)=mn+\Lambda\quad(n\in I),\qquad
 m>0,\quad\rho_A=mn,\quad\rho_M=\Lambda,\quad Q=0.} \tag{7}
\]

Positive maintenance energy adds Λ ≥ 0. This does not derive m or Λ; the latter must be owned once in the total energy/action ledger, not counted again as a separate geometric volume term. The theorem needs no continuation to n = 0 and makes no statement across an unmodeled phase boundary.

At a single background n_0, vanishing first-order sound response only requires ε″(n_0) = 0. Higher derivatives can restore nonlinear pressure or a nonzero sound response at other densities. A homogeneous background has Dn = 0 for every ε, so its geodesicity alone proves none of (7). If a changing background sweeps an open density interval and arbitrary linear density perturbations must be cold at every point, the interval conclusion does apply.

## 4. Direct A/M consequence: a fixed nontrivial energy share is unstable here

Let f = ρ_A/ε, and suppose 0 < f < 1 so both components are positive. From (4), f = nε′/ε. Differentiation and current conservation give

\[
 \frac{df}{d\ln n}=f(1-f+c_s^2),\qquad
 \boxed{\dot f=-\theta f[(1-f)+c_s^2].}               \tag{8}
\]

This also follows by putting (6) into the earlier I0 identity Q = ε[dot f + θf(1−f)]. For a nonstatic expanding epoch, a constant f = f_* in (0,1) therefore requires

\[
 c_s^2=-(1-f_*)<0,\qquad
 \epsilon(n)=C n^{f_*},\quad C>0,\qquad
 p=(f_*-1)\epsilon.                                 \tag{9}
\]

It fails the barotropic short-wavelength gradient-stability gate wherever that hydrodynamic regime is valid. Equivalently, expansion with stable c_s² ≥ 0 gives Q ≤ 0 (active-to-maintenance), whereas holding a nontrivial f fixed would require Q = θεf(1−f) > 0 (maintenance-to-active).

This rejects a **fixed positive energy-share/ratio claim under this complete density-only closure**, not a fixed operation-rate share. The latter is not f unless the transduction map proves it. A static θ = 0 background gives no such fixed-share constraint. The limits f = 0 or 1, open sources and additional state variables require their own stated domains; dividing by f at zero is not allowed. No measured density ratio was used.

## 5. Quantitative approximate-coldness bound

Specify a density interval [n_−,n_+] with 0 < n_− < n_+, and a prospectively chosen dimensionless ceiling σ on the squared sound speed:

\[
 0\le c_s^2(n)\le\sigma\quad\hbox{throughout the interval}.      \tag{10}
\]

No empirical value is assigned to σ here; a cold-response application requires σ small on its independently stated scales. Integrating the third relation of (6) gives

\[
 0\le\rho_M(n_-)-\rho_M(n_+)
   =\int_{\ln n_-}^{\ln n_+}c_s^2\rho_A\,d\ln n
   \le\sigma[\epsilon(n_+)-\epsilon(n_-)]
   \le\sigma\,\rho_{A,\max}\ln(n_+/n_-).           \tag{11}
\]

Using ε = ρ_A + ρ_M, the middle inequality has the equivalent active-energy form

\[
 \boxed{0\le\rho_M(n_-)-\rho_M(n_+)
 \le\frac{\sigma}{1+\sigma}
                  [\rho_A(n_+)-\rho_A(n_-)].}        \tag{12}
\]

For completeness, (6) also bounds the active scaling:

\[
 \frac{n_+}{n_-}\le
 \frac{\rho_A(n_+)}{\rho_A(n_-)}
 \le\left(\frac{n_+}{n_-}\right)^{1+\sigma}.         \tag{13}
\]

The upper bounds in (12) and (13) are sharp for constant c_s² = σ; their lower bounds are attained at c_s² = 0. They are not merely qualitative statements that vacuum varies slowly. They bound an absolute maintenance-density change. A small σ alone does not guarantee a small *fractional* change in ρ_M if ρ_M is much smaller than ρ_A. If c_s² is allowed negative, the stable-branch ordering in (11)–(13) is lost; calling it cold does not remove its gradient-instability obligation.

## 6. Which departures change the test—and what must be supplied

If the pair is open, let ∇_μ(T_A+T_M)^{μν} = S^ν. The exact replacements are

\[
 \dot\rho_A+\theta\rho_A=-\dot\rho_M-u_\nu S^\nu,
 \qquad \rho_Aa^\mu=D^\mu\rho_M+h^\mu{}_{\nu}S^\nu. \tag{14}
\]

An outside sector can cancel a momentum force only through its owned momentum transfer, not an energy-only adjustment. Its full stress/work ledger must be present.

If records form or disappear, ∇_μ(nu^μ) = Γ changes dot n + θn to Γ. Keeping exactly the same ε(n) and pressure then gives

\[
 \dot\epsilon+(\epsilon+p)\theta=\epsilon'\Gamma.    \tag{15}
\]

With ε′ > 0 this cannot be a closed, isentropic total fluid unless Γ = 0. Nonzero formation needs supplied energy, extra variables/stress or a different action; changing only the counting equation is not a consistent escape.

Independent entropy/history fields, elasticity, relative flows and nonlocal memory can invalidate the single-variable reduction. They may permit geodesic time-dependent vacuum through an independent comoving-homogeneous state variable, but require their own covariant dynamics, interaction force and physical record map. They cannot be omitted in the background fit and restored only to evade its perturbation test. This note does not demand that every UNT parent satisfy ε(n), nor does it disprove those broader routes.

**Next primary acceptance test:** for one candidate actually claiming this conserved density-only A/M realization, derive ε, its first two density derivatives and the independently owned exchange. Check (5)–(6) on admitted inhomogeneous states, and apply (8) plus (11)–(12) over the claimed density interval. A stable cold candidate cannot keep a nontrivial energy share fixed by selecting a compensating background Q. Passing these conditions still does not derive m, Λ, an initial abundance, a physical transport current or the primary active/maintenance mechanism.
