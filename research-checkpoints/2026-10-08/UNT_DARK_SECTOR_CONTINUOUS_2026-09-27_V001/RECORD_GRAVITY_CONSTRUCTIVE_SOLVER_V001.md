# Native records change operational propagation: an exact bridge

2026-09-27. Analytical derivation from `F3-QIRN-V001`; no numerical run,
additional interaction, continuum metric, physical distance, or formation
protocol has been inserted. Resident flags were checked before reading
`NATIVE_SHARED_LINK_RECORD_BINDING_V001.md`,
`DYNAMICAL_SHARED_RESPONSE_DISPERSION_V001.md`,
`NATIVE_STIFFNESS_TO_FLAT_ROTATION_SCREEN_V001.md`, and the complete recovered
`recovered_sources/BS_MICRO_ACTION.md`.

**Result.** The same native link response that gives negative record binding
also changes the propagation of a transported carrier. Its positive static
stiffness and finite response rate can both be derived exactly. This earns a
small operational and dynamical bridge from records to network structure;
identifying that structure with a universal spacetime geometry still requires
an infrared restriction and a common clock response. A spectator-energy
counterexample identifies precisely why the unrestricted microscopic theory
does not already supply that universality.

## 1. Source-owned variables and complete vacuum-link energy

Use the source-off N=1 hold sector of the shared-link note, with formation and
ports switched off as already declared there. For fixed record occupation
sum s=q_L^r+q_R^r, define

    C_s = 2U_d d_*² + ε_r s,
    a = Δ + 2U_d(1−2d_*),
    z_s = a−λ_R s,
    R_s = √(z_s²+4Ω²),
    F(z) = [z−√(z²+4Ω²)]/2.

The carrier-vacuum link Hamiltonian, ground energy and occupation are

    H_s^0 = C_s I−ΩX+z_s n,
    e(s) = C_s+F(z_s),
    m_s = F′(z_s) = (1−z_s/R_s)/2.                    (1)

All common constants and storage costs remain in e(s). The ground is
conditional on this invariant sector. Smooth s derivatives below use the
same external-bias interpolation as the predecessor; physical s remains
0, 1 or 2. For Ω,λ_R>0,

    e″(s) = −2λ_R²Ω²/R_s³ < 0.                       (2)

This is the previously established negative-binding mechanism, not a new
pair interaction. The next sections derive further consequences of (1).

## 2. Native finite-rate response: D and Z_t are calculable

Add a small diagnostic energy bias −f(τ)n to the link. Time τ is the
microscopic operational boundary-clock parameter of BS05; it has not been
renamed a spacetime coordinate. With the link initially in its conditional
ground, the only excitation has gap R_s and

    |〈1|n|0〉|² = Ω²/R_s².

Consequently its exact linear retarded susceptibility is

    χ_nn(τ) = θ(τ) [2Ω²/(ℏR_s²)] sin(R_sτ/ℏ),
    χ_nn(ω) = 2Ω² / {R_s[R_s²−ℏ²(ω+i0)²]}.          (3)

Here δm(ω)=χ_nn(ω)f(ω), with Fourier convention exp(−iωτ).
Writing ζ=δm, its inverse kernel is exactly

    χ_nn(ω)^−1 = D_s−Z_t,s(ω+i0)²,
    D_s = R_s³/(2Ω²) > 0,
    Z_t,s = ℏ²R_s/(2Ω²) > 0.                         (4)

The corresponding quadratic response action is

    L_2 = (Z_t,s/2) ζ̇²−(D_s/2)ζ²+fζ.

Its oscillation frequency is R_s/ℏ. This is an exact linear-response
representation for the chosen ground, not a damping or thermalization law.
For a source fluctuation δs, f=λ_R δs; therefore the mixed energy coefficient
is B=−λ_R and

    e″(s) = −λ_R²/D_s,
    ∂m_s/∂s = λ_R/D_s.                               (5)

These are native one-link counterparts of the response note's D, Z_t and B.
They do not determine its spatial Z_s, a continuum density, or a volume
conversion. In particular, no Yukawa range follows from this one-link
calculation.

The static energy underlying (4) is also explicit. At fixed 〈n〉=m,
0<m<1, minimizing over link states gives

    V_s(m)=C_s+z_s m−2Ω√[m(1−m)].                    (6)

Its second derivative at m_s is D_s. To check the kinetic coefficient
without importing an oscillator, write the normalized link state as
√(1−m)|0〉+exp(iφ)√m|1〉. The native variational action, up to a total
derivative, has Berry term ℏφ ṁ and energy
C_s+z_s m−2Ω√[m(1−m)]cosφ. Eliminating φ to quadratic order gives
Z_t,s=ℏ²/[2Ω√(m_s(1−m_s))], equal to (4).

## 3. The same link changes a probe's actual propagation

Keep the source records fixed during the hold and introduce exactly one
transported carrier of either content x=0 or 1. Let |L,x〉 and |R,x〉 denote
its two positions. Within each content sector, BS07 gives

    T^ψ = |L〉〈R|+|R〉〈L|,    (J^ψ)²=I.

Thus the full Hamiltonian in this invariant one-carrier sector is

    H_s^1 = (C_s+ε_ψ)I−ΩX+(z_s+λ_J)n−t n T^ψ.       (7)

The native current feedback is retained. In transfer-parity states
|±〉=(|L〉±|R〉)/√2, it becomes two exact link Hamiltonians

    H_s,± = (C_s+ε_ψ)I−ΩX+(z_s+λ_J∓t)n.             (8)

No replacement of n by its mean is needed. For an initially left-localized
carrier and arbitrary normalized link state ρ_s, set
U_±(τ)=exp[−iH_s,±τ/ℏ]. Inclusive right-arrival probability is exactly

    P_R(τ;s,ρ_s)
      = ½{1−Re Tr[U_+(τ)ρ_s U_−(τ)†]}.              (9)

This retains probe backreaction and unobserved link entanglement. Both
carrier contents have precisely the same response by native content
covariance. Its short-time expansion is

    P_R(τ;s,ρ_s) = (t²τ²/ℏ²)Tr(ρ_s n)+O(τ³).       (10)

On the conditional vacuum-ground family ρ_s=|0_s〉〈0_s|, the coefficient
κ_s=lim_(τ→0)P_R/τ² therefore satisfies

    κ_s = t²m_s/ℏ²,
    ∂κ_s/∂s = t²λ_R/(ℏ²D_s)
             = −t²e″(s)/(λ_Rℏ²) > 0.                (11)

Equation (11) is the short exact bridge: the response giving record binding
also changes an observable propagation probability, with no separate
propagation coupling or chosen metric. Enhanced transfer alone has no
gravitational sign: no proper distance is held fixed and no local proper
clock has been identified.

Finite-time propagation generally cannot be inferred just from m_s. For
example, ρ=(I+r_xX+r_zZ)/2 has fixed m=(1−r_z)/2 while varying r_x changes
its evolution under the two Hamiltonians in (8). The complete influence
overlap in (9), rather than an instantaneous edge mean, determines arrival.

The conditional ground energies of the two parity sectors are also exact:

    E_s,±^1 = C_s+ε_ψ+F(z_s+λ_J∓t).

For t>0 the parity splitting

    Δ_p(s)=F(z_s+λ_J+t)−F(z_s+λ_J−t)>0

increases with s. When the parity-ground pair is an isolated low-energy
band and t is small relative to its link gaps, its effective transfer
coefficient is

    t_eff=Δ_p/2=t F′(z_s+λ_J)+O(t³).                 (12)

The exact band eigenstates have different link dressings; (12) is not a
claim that an initially localized bare carrier undergoes a pure sinusoidal
two-level transfer. Equation (9) remains the inclusive answer.

## 4. What prevents immediate identification with universal gravity?

There are two concrete, finite obstructions; neither is an infrared no-go.

First, a source-off writer excitation costs exactly ε_w and has no effect
on (1), (3), (7) or (9). Tensoring in an occupied decoupled writer can add
positive total energy while leaving the complete link/carrier dynamics
identical. The source supplies independent ε_w and ε_r coefficients, while
incidence responds directly only to q^r and carrier currents. A universal
response to arbitrary microscopic total energy is therefore not an
identity of V001.

Equivalently, the response cannot be a nontrivial common multiplication of
every microscopic energy gap: Δ_p(s) changes while ε_w does not. If the
writer blank/occupied transition is an admissible local clock, it defeats
that universal multiplication. If physical clocks are instead necessarily
network composites, that must be established by the accessible infrared
sector; the decoupled writer is then only a formal spectator. A spatial
metric can also change an extended transfer clock without changing a local
proper clock, so this spectral observation alone does not exclude spatial
geometry.

Second, record binding does not even fix the sign of every carrier addition
energy. Relative to the SAME vacuum ground, define

    M_±(s)=ε_ψ+F(z_s+λ_J∓t)−F(z_s).

Then exactly

    ∂M_±/∂s
      = −λ_R[F′(z_s+λ_J∓t)−F′(z_s)].                (13)

Because F′ decreases, λ_J>t>0 makes both derivatives positive, even while
record insertion becomes less expensive and binding stays negative. This
is an allowed native parameter choice, not a universal attracting geometry.

A minimal promising native restriction is λ_J=0, t>0, retaining the bonding
low-energy carrier branch. Then ∂M_+/∂s<0, so a carrier's dressed addition
energy and a record's insertion energy both decrease in the same response
background, while propagation increases. The sufficient conditions
ε_ψ>t and ε_r>λ_R keep both costs positive and can coexist with BS13.
This restriction introduces no interaction. It supplies a compatible sign
domain, not universal gravitational mass, inertia, or a metric.

## 5. A constrained inverse solution, with a held-out prediction

Inverse solving need not insert a desired geometry. Suppose conditional
ground occupations m_0,m_1 and spectral energy gaps R_0,R_1 are supplied as
calibration data. Equations (1) invert exactly:

    z_s=R_s(1−2m_s),
    Ω_s=R_s√[m_s(1−m_s)],
    a=z_0,    λ_R=z_0−z_1.                           (14)

Same-parent consistency requires Ω_0=Ω_1>0 and λ_R≥0. These two source
settings then predict the third without another response parameter:

    z_2=2z_1−z_0,
    R_2=√(z_2²+4Ω²),
    m_2=(1−z_2/R_2)/2,
    e(2)−2e(1)+e(0)=−½(R_2−2R_1+R_0).              (15)

The inferred Ω also predicts every D_s and Z_t,s in (4). A separately
calibrated native transfer coefficient t predicts κ_s=t²m_s/ℏ². One
measured insertion energy fixes ε_r if needed. This is an overconstrained
native inverse problem: failure of the held-out s=2 response or binding
rejects this branch rather than demanding an independent gravity fit.
The absolute spectator energy, the decomposition of a into Δ,U_d,d_*, and
any continuum gravitational units remain unidentified by these data.

## 6. Formed states and the next decisive calculation

Ground response need not describe a formed record. During the hold the
record number operators commute with H, so an arbitrary actual postformation
record/link state decomposes for inclusive propagation into occupation
sectors with weights p_s and conditional link states ρ_s. Record-sector
coherences disappear from this inclusive trace because those sectors are
orthogonal; no postselection is required. For a freshly introduced carrier
initially independent of that state,

    P_R^formed(τ)=Σ_s p_s P_R(τ;s,ρ_s),
    lim_(τ→0)P_R^formed/τ²
      = (t²/ℏ²)Tr(ρ_formed n).                       (16)

Thus the operational bridge itself survives arbitrary formed-state
entanglement. The monotonicity (11), the passivity of (3), and the static
binding interpretation do not automatically survive replacing its ground
state by that formed state. Formation or readout that overlaps the probe
requires the corresponding full mission propagator instead of this hold
factorization.

The next decisive calculation is small and exact: take the actual,
unrepinned postformation density matrix from the same blank-to-record
mission, retain its record/link correlations, and insert its ρ_s directly
into (9). In the SAME source backgrounds extract all admissible local-clock
transition responses. This asks whether the operational change is present
in a formed state and whether different physical clocks agree, without
first defining a geometric field.

The finite algebraic target for a common lapse is especially concrete. If
an isolated retained block represents internal clocks and χ is the same
collective response variable, all of its energy gaps scale together only if
their logarithmic derivatives agree. Identify the retained spaces smoothly
with one fixed reference space by an isometry W(χ), and let
K(χ)=W(χ)†H_eff(χ)W(χ). A sufficient operator condition is

    ∂_χ K = α(χ)K + β(χ)I.                          (17)

The derivative includes the dependence of W. This is stronger than needed:
common scaling of nondegenerate gaps only requires the corresponding
Hellmann–Feynman diagonal condition in K's eigenbasis. Gap ratios then
remain fixed and α=∂_χ log N supplies the common clock factor N. The
identity term β cannot determine that clock factor. The unrestricted
microscopic writer example fails this condition for nonzero α. Restricting
to actual accessible, gapped composites is the smallest defensible escape;
its success is testable by finite matrix elements, not a metric definition.

Only after a common clock factor is found should the same retained
propagation kernel determine the spatial response. The native shared-link
result already supplies a response oscillator, source coupling, and an
operational probe affected by that source. Equations (9), (16), and (17)
are the concrete next bridge to solve; no independent gravitational
potential or metric has been fitted into the Hamiltonian.
