# Independent hard-limit clock and ordinary-matter interface review

2026-09-29. Analytical review and additional transfer bounds. No numerical
producer, new state preparation, data fit or modification of frozen evidence.

## Decision and exact scope

The two reviewed scalar interfaces pass the independent algebraic checks below.
They retain a pressureless total gravitational stress **and** a separate physical
clock/polarization sector. The latter is not certified stable merely because the
metric equations agree with a pressureless reference model. Its controlled
slow-response limit has a compensated, growing relative tilt during sufficiently
hard-excitation-dominated matter expansion. Positive vacuum expansion eventually
arrests that particular growth. No wave-number-divergent rate appears in the
displayed finite-band linear internal system.

These conclusions concern the explicitly adopted balanced, rapid, phase-averaged
hard-limit state, with the retained hard contact and a finite positive soft band.
They do not reclassify the old coherent pulse, prove a native BS dictionary,
establish nonlinear stability, or establish a CMB spectrum or observational fit.

## 1. Independent action, stress and sign checks

Write the gravitational coefficient as M2, C Kb=2M2, KH>0, and
Ksoft=b^T Ks^-1 b=Kb-KH. All soft masses and frequencies are positive. The
unitary-clock variables are those of the reviewed note: T=t, phi=t+v,
N=1+n, N_i=partial_i beta, gamma_ij=a^2 exp(2 zeta) delta_ij,
p=k/a and q=zeta_dot-Hn, with k nonzero.

Independently expanding the homogeneous Einstein-plus-vacuum action gives

    -3M2 a^3 exp(3zeta)(H+zeta_dot)^2/(1+n)
       -rhoLambda a^3 exp(3zeta)(1+n).

Its quadratic zeta^2 coefficient vanishes after the zeta*zeta_dot integration
by parts on the hard-dust-plus-vacuum background. The remaining n*zeta term
is +3rho n zeta. The exact hard phase action contributes
3rho zeta(v_dot-n), so these n*zeta terms cancel. This reproduces equation
(8) of the first reviewed note, including the easily missed +3rho zeta v_dot
term. Variation gives n=v_dot and q=H_dot v, hence zeta-Hv is conserved.

After applying the constraints and removing endpoint terms, the internal action
is exactly the stated one:

    Lint/a^3 = C[ x_dot^T Ms x_dot/2 - x^T Ks x/2
                   +p v_dot b^T x + KH p^2 v_dot^2/2]
                    +rho p^2 v^2/2.                         (1)

The last term is positive in the Lagrangian: it is a negative potential
direction, not a negative kinetic norm. The velocity Hessian is positive for
KH>0 and Ms>0. In canonical variables the v momentum is shifted by C a^3 p S;
the corresponding square remains positive, while -a^3 rho p^2 v^2/2 remains
in the Hamiltonian. A positive-energy conclusion is therefore unavailable.

A separate covariant check uses the hard density stress

    T_H,mu nu=rho u_mu u_nu-2rho u_(mu D_nu)phi.

In Newtonian gauge T=t+pi, phi=t+V, it gives T_H^0_i=-rho partial_i V,
not -rho partial_i pi. The density current is still rho u. The polarization
stress at linear order has delta rho_pol=-p Pcal and zero momentum, pressure
and anisotropic stress, where

    Pcal=C[S+KH p(Phi-pi_dot)].

The gauge map Phi=n+beta_dot, Psi=-zeta-Hbeta, pi=beta, V=v+beta and
delta rho_N=delta rho_U-3Hrho beta checks against both Einstein constraints.
It is essential to transform the density as well as the potentials.

## 2. Exact finite-band wave-number cancellation

The actual internal equations of the reviewed leading action are

    KH(v_ddot+H v_dot)+(S_dot+2HS)/p-(rho/C)v=0,
    Ms(x_ddot+3H x_dot)+Ks x=b p v_dot.                    (2)

They also hold with separately coupled ordinary components; then H contains
those components. Define X=x/p, possible for each nonzero k. Since p_dot=-Hp,
equation (2) is equivalent to

    Ms[X_ddot+H X_dot-(2H^2+H_dot)X]+Ks X=b v_dot,
    KH(v_ddot+H v_dot)+b^T(X_dot+HX)-(rho/C)v=0.          (3)

All k dependence has disappeared from the temporal generator. Thus arbitrary
wave number does not create an arbitrarily fast growing rate **within this
leading finite-band linear system**. Initial data and the conversion to physical
tilt/density still contain k. This is not a statement that all UV modes satisfy
the hard-gap averaging assumptions, nor a proof of causality or hyperbolicity
for the full covariant parent. The limiting action was derived at fixed physical
wave number, not by interchanging k to infinity with the hard-gap limit.

## 3. Exact frozen-coefficient rate bounds and mode count

As a diagnostic only, suppress H and freeze rho>0 and the other coefficients.
An exponential solution with y=s^2 obeys

    F(y)=KH y + sum_j a_j y/(Omega_j^2+y) - rho/C=0,
    a_j=b_j^2/(Ms)_jj,   Omega_j^2=(Ks)_jj/(Ms)_jj.       (4)

For y>0, F'(y)=KH+sum a_j Omega_j^2/(Omega_j^2+y)^2>0.
There is exactly one positive root, and it obeys

    rho/(C Kb) <= s^2 <= rho/(C KH).                     (5)

For a nonempty coupled soft band both inequalities are strict. In a background
containing only the hard density and constant vacuum, (5) is

    -H_dot <= s^2 <= (-H_dot)/f,     f=KH/Kb.

With ordinary components, rho/(2M2), not -H_dot, is the lower expression.
Small f can increase this local response rate; static susceptibility alone is
insufficient to decide whether the soft band follows it.

There is also a complete frozen-mode count. Group equal coupled Omega values.
F is strictly increasing between all negative poles, tends from -infinity to
+infinity on every intervening interval, has one negative root below the
leftmost pole, and its remaining root is the positive root in (4). Thus for
r distinct coupled poles there are r negative y roots and one positive y root.
Source-orthogonal combinations in a repeated-frequency group supply the
remaining stable, bare-frequency modes. There is no hidden complex-y pair in
this rational frozen diagnostic. This count does not replace the expanding
equations when their rates are comparable to H.

## 4. Physical compensated tilt and the slow-response condition

When H and all pertinent envelope rates are small compared with the controlled
soft frequencies, and their fast homogeneous transients are retained or bounded,
x approximately equals Ks^-1 b p v_dot. Equation (2) then becomes

    v_ddot+H v_dot-rho v/(2M2)=0.                         (6)

For the single hard-density-plus-vacuum background, rho/(2M2)=-H_dot, giving

    v=(C1+C2 integral^t a(t') dt')/a.                    (7)

Taking the compensated metric branch Rc=V=Phi=Psi=0 gives beta=pi=-v.
The preferred normal has a physical velocity relative to the hard phase with
magnitude p|v|. This is a relative physical tilt, not a removable coordinate
lapse. In matter domination its growing branch is v proportional to t, so
p v is proportional to t^(1/3)=a^(1/2). Its hard density and polarization
density cancel exactly at this order. Their separate fractional contrasts
grow proportional to a; they must not be counted as independent abundances.
The acceleration p v_dot can decay while the tilt grows.

The finite positive soft frequencies do not by themselves remove this slow
branch. For example, in the matter regime the leading x0=Ks^-1 b p v_dot
has x0_ddot+3H x0_dot=-2x0/(9t^2). Its first derivative-expansion correction
is (2/9)Ks^-1 Ms x0/t^2. This is small for Omega_min t much greater than one.
It demonstrates consistency of the slow expansion, not an exact finite-time
solution or an averaging theorem for a gapless band.

## 5. Analytic dust-plus-vacuum transfer and a finite peak

For H(a)=H0 sqrt(Omega_m a^-3+Omega_Lambda), both density parameters positive,
define Hm=H0 sqrt(Omega_m), HL=H0 sqrt(Omega_Lambda). Select the solution of
(7) regular at the early dust endpoint. Its physical tilt transfer is

    tilt(a) proportional to Ftilt(a)=I(a)/a^2,
    I(a)=integral_0^a da'/H(a')
        =2 a^(5/2)/(5Hm) * 2F1(1/2,5/6;11/6;
                              -Omega_Lambda a^3/Omega_m).     (8)

The hypergeometric expression follows by integrating a'^(3/2) times
(1+Omega_Lambda a'^3/Omega_m)^(-1/2); it is not an observational fit.
For a specified initial a_i>0 the exact slow-limit amplification is
Ftilt(a)/Ftilt(a_i). Selecting the regular branch is an explicit initial-data
choice; arbitrary data also include the C1/a mode in v.

The peak condition is a/H=2I. It has exactly one positive solution: the
derivative of a/H-2I is [3Omega_m(a)/2-1]/H, initially positive and eventually
negative; a/H-2I starts positive and tends to -infinity. The tilt therefore
peaks after acceleration begins and then decays as a^-1. This growth is not
unbounded for all future time when the matched vacuum is positive.

Two useful bounds, requiring no numerical evaluation, are

    -1 <= d ln Ftilt/d ln a <= 1/2,
    Ftilt(a) <= min[2 sqrt(a)/(5Hm), 1/(HL a)],
    sup_a Ftilt(a) <= (2/(5Hm))^(2/3) HL^(-1/3).         (9)

The first follows from 2a/(5H(a)) <= I(a) <= a/H(a).
Accordingly, over a_f>=a_i the regular-branch amplification lies between
(a_f/a_i)^(-1) and (a_f/a_i)^(1/2). These are properties of (6) in its
controlled slow band, not unconditional bounds on arbitrary finite-band
solutions, nonlinear amplitudes or a differently prepared clock.

## 6. Independent ordinary-radiation interface check

The second reviewed note correctly avoids substituting H_dot=-rho/(2M2)
once ordinary species are present. Its result can be checked without any
background Einstein relation. Direct clock variation gives

    partial_t(a^3 p Pcal)=a^3 rho p^2(V-pi).

Together with rho_dot=-3Hrho and p_dot=-Hp, this implies

    partial_t(delta rho_pol/rho)=-p^2(V-pi).

The hard current gives delta_H_dot=3Psi_dot-p^2 pi, while its momentum is
-rho grad V and V_dot=Phi. Adding the polarization yields exactly

    delta_d_dot=3Psi_dot-p^2 V,   V_dot=Phi,
    delta p_d=0,   delta anisotropic stress_d=0.          (10)

This proves the displayed total pressureless stress/conservation interface
on arbitrary flat FLRW backgrounds, including ordinary pressure and radiation.
It does not impose Phi=Psi in the presence of ordinary anisotropic stress.
No static G/mu factor, subhorizon shortcut or borrowed dust abundance enters.

The independent internal equation remains (6) in the slow limit, but generally
d(v_dot+Hv)/dt=-(rho_o+p_o)v/(2M2). In a pressureless era with a constant hard
fraction Fh, its exponents are [1 +/- sqrt(1+24Fh)]/6. The physical tilt grows
on the plus branch exactly when Fh>1/3, as stated in the reviewed note.

Equation-level metric equivalence allows an explicitly imported ordinary
photon/baryon calculation to use this limiting component. It is not already
a computed acoustic spectrum, an origin for photons, a native-derived state,
or a demonstration that the extra compensated sector is acceptably prepared.

## Reviewed byte identities

* HARD_LIMIT_NONVACUUM_SCALAR_INTERFACE_V001.md:
  `c501fc2aeebe0cf389ad9c21c5c7fdd3240209a1d9dd0ae710ed45d67bb8003d`.
* HARD_LIMIT_DUST_INTERFACE_WITH_ORDINARY_RADIATION_V001.md:
  `41111a6ed3d0e69114ad36c19d1790e11a57fb2195d395aea88259b67083d522`.
* PAIRED_HARD_MODE_STATE_V001.md:
  `7461324e5c40de23f796c9e438a9d1cbecd88ffcc9bdb2c21c8e05fd54a38c91`.
* FINITE_MODE_CONSTRAINED_RESPONSE.md:
  `5f6116f2f803fda9c0cd7d60e18c3392e346bab4944ea2fdaef3175756245db3`.
* EXPLICIT_MODE_COSMOLOGY_PATHWAY.md:
  `5a99341c9abb3a35f3f6b59f54bf07cdc5f623016f8bdc9b1c2327f749d52067`.

These identify reviewed mathematical inputs. No new physical parameters,
formation history, coefficient fit or numerical stability outcome was added.
