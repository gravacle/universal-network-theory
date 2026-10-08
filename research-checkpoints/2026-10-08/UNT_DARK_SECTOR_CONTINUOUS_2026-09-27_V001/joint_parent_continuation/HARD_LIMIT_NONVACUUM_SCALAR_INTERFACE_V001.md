# The hard excitation with gravity, the preferred clock and soft modes retained

2026-09-29. New analytical conditional interface; no numerical evolution,
observational fit, replacement of a saved pulse state or change to frozen files.

## Result

The large-gap, finite-energy mode sector can supply a pressureless background
and its linear gravitational response in a specified phase-averaged parent.
The resulting metric equations are the pressureless-matter plus matched-vacuum
equations, **not** a substitution of G/mu0 into a static susceptibility. A
separate preferred-clock/polarization sector remains. It has an explicitly
identified compensated growing branch in the slow-soft-mode-response limit.
Thus the calculation supplies useful evolution equations but not an all-sector
stability or cosmological-success claim.

This interface is not yet justified for the old coherent common pulse. A
distinct antipodal-pair preparation makes the leading coherent source cancel
without throwing away its energy; it is an additional counted state assumption.
The clock and phase constraints below must still be solved. The microscopic
preparation, physical time conversion and a uniform coupled averaging error
bound have not been derived.

## 1. Parent, limiting state and a contact that must not disappear

Use the complete covariant action in EXPLICIT_MODE_COSMOLOGY_PATHWAY.md:

    S = integral sqrt(-g) { Mpl2 R/2
          + C [sum w (m v_y^2/2 - V0(y) + kappa delta h(a).y)
                 - DeltaU] },
    u_mu = -partial_mu T/X,  X=sqrt(-partial T squared),
    a_mu = nabla_u u_mu,  v_y=P nabla_u y,  u.y=0,
    V0=kappa delta^2 y^2/2+u4(y^2)^2/4,
    P_mu_nu=g_mu_nu+u_mu u_nu,
    Kb=kappa sum w,  C=2 Mpl2/Kb,  Mpl2=1/(8 pi G).

The bounded source remains h_mu=a_mu/sqrt(1+a^2/gs^2). Here Mpl2 denotes
the gravitational coefficient, not a mode-mass matrix. The explicit formulae
for the hard pair below use the inherited kappa=m=u4=1 units. A general hard
frequency is Omega_H=sqrt(kappa/m_H) R; the acceleration normalization alone
does not determine its physical value.

Let the hard atom have total weight beta, gap R and fixed nonzero total owned
excitation energy. At fixed action its leading harmonic energy is

    e_H(I,h)=Omega_H I-kappa h^2/2 + subleading terms.       (1)

The second term survives as R tends to infinity. With KH=kappa beta and
rho=C beta Omega_H I, theta=Omega_H phi, the leading Whitham action is

    L_H = rho (u.partial phi-1) + C KH h(a)^2/2.            (2)

For multiple balanced copies, rho is their summed energy density; a common
slow phase phi is the scalar adiabatic sector considered here. Independent
relative phases/actions would require additional initial data, not their
silent removal. DeltaU remains the very same matched endpoint. No extra
vacuum term or independent pressureless abundance is inserted.

Equation (2) retains the hard static polarization KH h. Omitting this term
while keeping hard energy loses part of the original contact. Conversely,
adding another bare Kb a^2/2 to this extra action would double-count the
Einstein-sector contact. Around zero acceleration, (2) contributes
C KH a^2/2, because h=a+O(a^3).

The limiting operation requires Omega_H large compared with expansion,
envelope and source-response rates on the interval under consideration,
fixed finite physical perturbation wave number, and controlled hard initial
transients. Finite-R susceptibility corrections at fixed energy are of
relative order R^-4 in the inherited units; dynamic polarization also has
Omega_H^-2 derivative corrections. These are different errors. Neither a
small averaged pressure nor a large numerical R alone establishes the
required coupled metric/clock separation.

### A constructive state prescription, not a relabeling of the pulse

Split the same weight beta into two identical weights beta/2 and set
y_plus=p+q, y_minus=p-q. Their exact local hard terms become

    T=beta (p_dot^2+q_dot^2)/2,
    V2=beta R^2(p^2+q^2)/2,
    V4=beta [(p^2+q^2)^2+4(p.q)^2]/4,
    source=beta R h.p.                                    (3)

At h=0, p=0 is an invariant subspace of the odd unforced equations. The
q excitation carries the same positive energy, while B=beta R p and B_dot
vanish exactly. The q energy is not deleted or assigned a new negative sign.
For fixed q energy, q^2=O(R^-2); its effect on the forced p stiffness,
divided by the leading R^2, is O(R^-4). The slow particular response has
p=h/R at leading order and retains the contact in (2).

This is a NEW pair-prepared sector. A common symmetric source starting both
copies at zero has q=0 for all time and cannot produce it. It needs owned
antisymmetric preparation or independently specified initial data and its
work. Splitting the weight keeps total contact and energy; it does not prove
that the native spectrum contains the necessary pair. At finite source the
trajectories are not origin-antipodal; in the harmonic limit they may instead
be opposite about a common forced particular trajectory.

An isotropic orientation ensemble or a specified equal-axis construction
can supply the homogeneous scalar background. The pair cancels linear fast
polarization but not its oscillatory quadratic stress: that still needs
rapid-phase averaging. The old collinear coherent pulse and its finite B,
B_dot remain unchanged. The resting-annulus incompatibility established in
COHERENT_HIGH_GAP_CLOCK_COMPATIBILITY_V001.md is not evaded by declaring
that state averaged. No general nonlinear averaging theorem with lapse and
clock constraints is asserted here. The equations below are exact equations
of the declared leading averaged action, whose realization is conditional.

## 2. A normalized-gradient clock is not an independently varied dust velocity

Variation of the rho and phi fields in (2) gives

    u.partial phi=1,              nabla_mu(rho u^mu)=0.     (4)

But u is determined by T, not a freely varied timelike vector. Since
delta u^mu=-P^mu_nu nabla^nu(delta T)/X, its density term contributes

    nabla_nu[(rho/X) P^{mu nu} partial_mu phi]              (5)

to the clock equation, together with the soft and hard polarization terms.
Dropping (5) would describe another theory.

For s_mu=P_mu^nu partial_nu phi, the on-shell hard density stress is

    T_H,mu nu = rho u_mu u_nu - 2 rho u_(mu s_nu).          (6)

Its spatial pressure vanishes at this order; relative to u its energy flux
is -rho s_mu. Only the s_mu=0 subbranch is ordinary dust comoving with this
preferred normal. At first order the combined metric response will still
be dust-like, but the hard density current, clock and polarization must be
kept to see how that occurs.

## 3. Nonzero hard background and the complete scalar quadratic action

First use the minimal flat background with no other matter, soft y=0,
phi=T=t and positive hard density rhobar. Define rhoLambda=C DeltaU.

    3 Mpl2 H^2=rhobar+rhoLambda,
    Hdot=-rhobar/(2 Mpl2),     rhobar_dot=-3H rhobar.       (7)

Its rhobar normalization must be inherited from the declared preparation,
not fitted again in this perturbation calculation. The common-pulse limiting
energy is one possible energy ledger, but it does not by itself create the
pair state (3).

In unitary clock gauge T=t, use N=1+n, N_i=partial_i beta,
gamma_ij=a^2 exp(2zeta) delta_ij, phi=t+v and rho=rhobar+delta_rho.
Use a nonzero comoving Fourier wave number k, p=k/a and

    q=zeta_dot-H n,    f=KH/Kb,
    Ms=diag(w_j m_j),  Ks=diag(w_j kappa delta_j^2),
    b_j=w_j kappa delta_j,  S=b^T x,

where x are physical soft longitudinal components. Real Fourier phases are
chosen so that the source coupling is +p n S, and the divergence of this
polarization is -p S. Spatial surface terms vanish under periodic or suitable
decaying boundary conditions. The k=0 problem is separate.

Up to time endpoint terms, the quadratic Lagrangian per a^3 is

    L2/a^3 = Mpl2[-3q^2+p^2 zeta^2+2p^2 n zeta
                     -2p^2 q beta+f p^2 n^2]
             +delta_rho(v_dot-n)+3rhobar zeta v_dot
                     -rhobar p^2 beta v
             +C[x_dot^T Ms x_dot/2-x^T Ks x/2+p n S].     (8)

This retains the density, lapse, shift and clock; it is not a frozen-source
response action. A useful off-shell check is the background contribution
which differs from the empty-de-Sitter calculation. The homogeneous ADM
kinetic term is -3Mpl2 a^3 exp(3zeta)(H+zeta_dot)^2/(1+n),
and the vacuum term is -rhoLambda a^3 exp(3zeta)(1+n).
Their second-order n*zeta coefficient is +3rhobar. Their zeta^2 term cancels
after integration by parts using (7). Meanwhile the exact hard phase action
is sqrt(gamma) rho[phi_dot-N-N^i partial_i phi], which contributes
3rhobar zeta(v_dot-n). Its -3rhobar zeta n cancels that ADM term, giving
precisely (8). Using a densitized density instead is permissible only if
the corresponding variable change is made throughout.

## 4. A closed finite-band evolution/constraint system

Variation of (8) gives

    n=v_dot,
    q=Hdot v,               zeta-Hv=Rc(k),               (9)
    delta_dot+3zeta_dot+p^2 beta=0,
       delta=delta_rho/rhobar,
    delta_rho=2Mpl2[3Hq+p^2(zeta+H beta+f n)]+C p S,
    beta_dot+H beta+zeta+n=0,
    Ms(x_ddot+3H x_dot)+Ks x=b p n.                     (10)

The zeta equation in (10) uses the constraints and rhobar continuity, rather
than importing the vacuum equation without its background terms. The same
clock equation follows either from (5) or preservation of these constraints:

    Pcal=C[S+KH p n],
    Pcal_dot+2H Pcal=rhobar p v,
    delta_rho_pol=-p Pcal,
    (partial_t+3H)delta_rho_pol=-rhobar p^2 v.            (11)

Equivalently, with KH>0, the clock equation and soft mode equations are

    KH(v_ddot+H v_dot)+(S_dot+2H S)/p-(rhobar/C)v=0,
    Ms(x_ddot+3H x_dot)+Ks x=b p v_dot.                 (12)

These are a usable finite system with its constraints retained. The zero
density limit of (11) recovers the conserved comoving polarization charge
of the de-Sitter calculation, now including the retained hard contact.
There is no G/mu0 in these equations. Frequencies, source weights, density
and initial clock data determine the response.

## 5. What the metric actually does

Transform to Newtonian gauge by the time shift -beta. Define

    Phi=n+beta_dot,       Psi=-zeta-H beta,
    pi=beta,             V=v+beta,
    delta_rho_N=delta_rho-3H rhobar beta.                (13)

Here T=t+pi, phi=t+V in that gauge. The physical preferred-normal velocity
is -grad(pi)/a; the physical acceleration amplitude is
ell=p(Phi-pi_dot)=p n. Thus a large unitary lapse alone is not a physical
instability diagnosis. The equations imply

    Phi=Psi,
    V_dot=Phi,
    Psi_dot+H Phi=rhobar V/(2Mpl2),
    Rc=-Psi-HV=constant,       V_dot+HV=-Rc.             (14)

The total linear density sourcing the metric is

    delta_rho_tot=delta_rho_N+delta_rho_pol
       =-2Mpl2[p^2 Psi+3H(Psi_dot+H Phi)].              (15)

This is the pressureless-plus-vacuum metric system. The separate hard
density obeys delta_N_dot=3Psi_dot-p^2 pi, whereas the combined hard plus
polarization density divided by rhobar obeys

    delta_tot_dot=3Psi_dot-p^2 V.                       (16)

Equation (11) supplies exactly their difference. It is therefore wrong both
to discard polarization and to count its signed density again as another
independent positive cosmic abundance. The geodesic subbranch v=n=x=0
has pi=V and zero polarization and reproduces the usual pressureless
response with the inherited rhobar. This is a consistent subbranch, not
an explanation of why formation selects it.

Separately conserved ordinary pressureless matter can be retained without
new model parameters: add its background rhobar_b to (7), its density to
(15), and replace the momentum source in (14) by
(rhobar V+rhobar_b V_b)/(2Mpl2), with V_b_dot=Phi and
delta_b_dot=3Psi_dot-p^2 V_b. The hard equations in Newtonian variables
remain (11) with v=V-pi and the soft equation sourced by p(Phi-pi_dot).
The simple single-component invariant Rc and the particular reduced action
below are not reused unchanged for arbitrary relative matter modes.
Photons, baryon pressure, anisotropic stresses and their interaction terms
require their own owned matter equations before an acoustic/CMB calculation.

## 6. The extra clock sector has not disappeared: a compensated growth mode

For the single hard-density background, impose (9) in (8), keeping Rc fixed,
and integrate by parts. Rc-dependent linear terms cancel by (7); its remaining
field-independent term is irrelevant to the internal equations. The reduced
internal Lagrangian is

    Lclock/a^3=C[x_dot^T Ms x_dot/2-x^T Ks x/2
                   +p v_dot S+KH p^2 v_dot^2/2]
                     +rhobar p^2 v^2/2.                (17)

In particular the last sign is PLUS in the Lagrangian. There is positive
kinetic energy for KH>0 and the finite soft band, but a negative potential
direction, not an all-sector positive-energy theorem. The mixed v_dot*S
term is linear in velocities and does not turn the kinetic Hessian negative.

In a separately stated slow-response regime, all relevant H and solution
rates are much smaller than the retained soft frequencies. Then
S approximately Ksoft p v_dot, Ksoft=b^T Ks^-1 b=Kb-KH, and (12) becomes

    v_ddot+H v_dot+Hdot v=0,
    d(v_dot+Hv)/dt=0.                                   (18)

During pressureless domination a proportional to t^(2/3), its two solutions
are proportional to t and t^(-2/3). For the compensated choice
Rc=V=Phi=Psi=0, beta=pi=-v. The growing solution therefore has physical
preferred-normal tilt magnitude p|v| proportional to t^(1/3)=a^(1/2).
Its hard density +2Mpl2 p^2 v_dot is compensated by the polarization density
-2Mpl2 p^2 v_dot, so the metric perturbation is zero at this order. This is
not merely the ordinary growing metric-density mode described by (14).
It is a genuine additional relative clock/polarization growth channel in
the stated approximation, until its amplitude invalidates linearization.

No claim is made that every preparation excites it, that it grows
exponentially on the expanding background, or that its approximate exponent
applies when soft modes are too slow. Excluding it would require an actual
initial-state selection or a changed parent, not setting its integration
constant to zero without accounting for that choice. In the late de-Sitter
limit the solutions of (18) tend to a constant or decay, so their physical
tilt decays as a^-1; the matter-era statement is not unbounded-time growth.

For orientation only, freezing the background coefficients and ignoring H
gives the positive-real-rate equation

    s^2[KH+b^T(Ks+s^2 Ms)^-1 b]=rhobar/C.               (19)

Its left side strictly increases from zero to infinity for KH>0, so there
is one positive real root. This is a local frozen-background diagnostic,
not a substitute for (12) at rates of order H. A small KH or slow soft band
can change the clock response; it cannot be certified from the static
zero-frequency susceptibility alone.

## 7. What is now available, and what this does not establish

Equations (7), (10)-(12) and (13)-(16) provide the requested nonvacuum scalar
interface for the declared hard-limit state. They keep the actual excitation
background, the already matched vacuum, the hard contact, explicit soft
memory and the clock/lapse/shift constraints. No new force law, density fit,
cosmological spectrum or photon mechanism has been supplied.

The constructive next mathematical discriminator is the finite-band clock
system (12) with an owned balanced preparation and physical time scales,
including its compensated mode. The metric branch already shows why a
matter-like network excitation can gravitate rather than merely possess
an averaged w=0. Its leading metric equivalence to pressureless matter is
not a new observational distinction by itself. Actual perturbation initial
data, finite-gap corrections, phase preparation and the preferred-clock
mode decide additional predictions and admissibility.

This conditional continuum is still not the native BS source/volume
dictionary. Nor does the pair construction prove that the completed coherent
pulse can be converted to it autonomously or without preparation work.
These are separate substantive questions, not routine approval gates.

## Read-source identities

The complete source notes read for this derivation had SHA-256:

* EXPLICIT_MODE_COSMOLOGY_PATHWAY.md:
  `5a99341c9abb3a35f3f6b59f54bf07cdc5f623016f8bdc9b1c2327f749d52067`.
* FINITE_MODE_CONSTRAINED_RESPONSE.md:
  `5f6116f2f803fda9c0cd7d60e18c3392e346bab4944ea2fdaef3175756245db3`.
* COHERENT_HIGH_GAP_CLOCK_COMPATIBILITY_V001.md:
  `222f2894f08a6c6f1781d6f5e7a4bcc66e6909ce88d28131ac7ba301f80593f7`.
* GLOBAL_HARD_GAP_SHARED_FEASIBILITY_V001.md:
  `683bf955a6f70b39cb4a247c01c309db0580faae5b8b06acdd742ca9510bb08d`.

These hashes identify derivation inputs; they are not an observational or
native-state authentication of the newly adopted pair/averaging assumptions.
