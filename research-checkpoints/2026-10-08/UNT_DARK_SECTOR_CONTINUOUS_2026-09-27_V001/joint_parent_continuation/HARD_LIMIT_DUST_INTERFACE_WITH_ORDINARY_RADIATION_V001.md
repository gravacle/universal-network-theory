# The same linear hard sector with ordinary radiation and baryon pressure

2026-09-29. Analytical extension of
HARD_LIMIT_NONVACUUM_SCALAR_INTERFACE_V001.md, read at SHA-256
`c501fc2aeebe0cf389ad9c21c5c7fdd3240209a1d9dd0ae710ed45d67bb8003d`.
No numerical evolution, new calibration, radiation data or likelihood.

## Result and assumptions

Within the explicitly declared hard-limit averaged state, the TOTAL hard
excitation plus linear polarization stress obeys exactly the scalar equations
of one pressureless gravitational component on any flat FLRW background.
This remains true in the presence of separately included ordinary radiation,
baryon pressure and anisotropic stress. It is not necessary to set those
sources to zero or replace G by a static effective constant.

The additional internal clock/polarization sector remains and must be
admissible for this linear equivalence to apply. The inherited assumptions
are essential: the large hard gap and finite owned energy; the counted
balanced/antipodal preparation and phase average, not the old coherent pulse
by declaration; the same surviving hard contact; zero soft background; the
same DeltaU; and ordinary matter minimally coupled to the metric, with no
new direct coupling to the network modes. No uniform averaging or nonlinear
stability theorem is added here.

## 1. Background and variables

Let Mpl2=1/(8 pi G), C=2Mpl2/Kb, KH the hard contact, and
rhoLambda=C DeltaU. Denote the nonzero averaged hard energy density by rho.
The background equations now read

    3Mpl2 H^2=rho+rhoLambda+rho_o,
    -2Mpl2 Hdot=rho+rho_o+p_o,
    rho_dot=-3H rho.                                      (1)

Ordinary components may exchange energy among themselves according to their
specified interaction equations; their total stress is separately conserved.
Their pressure and perturbations are not discarded. The normalization of
rho is the owned hard-state energy, not an additional abundance fit here.

Use Newtonian gauge

    ds^2=-(1+2Phi)dt^2+a^2(1-2Psi)dx^2,
    T=t+pi,     phi=t+V,
    p=k/a,      v=V-pi,
    ell=p(Phi-pi_dot).

Phi need not equal Psi when ordinary anisotropic stress is present. The
soft mode matrices Ms,Ks and source vector b retain their definitions in
the parent note, with S=b^T x and

    Pcal=C[S+KH ell].                                    (2)

## 2. Full stress at linear order

The density part of the limiting action is rho(u.partial phi-1), with
normalized u=-dT/|dT|, not a freely varied fluid velocity. Its exact
on-shell stress is rho u_mu u_nu-2rho u_(mu s_nu), where
s_mu=P_mu^nu partial_nu phi. Therefore its linear mixed components are

    delta T_H^0_0=-delta rho_H,
    delta T_H^0_i=-rho partial_i V,
    delta T_H^i_j=0.                                    (3)

In particular the -rho grad(pi) normal momentum and the
-rho grad(V-pi) relative phase momentum combine into -rho grad(V).
The hard energy current conserved by the phi equation is nevertheless
rho u, not a current with velocity potential V by itself.

The linear polarization stress is

    delta rho_pol=-p Pcal,
    delta T_pol^0_i=0,
    delta p_pol=0,       delta anisotropic stress_pol=0.   (4)

This does not assume the empty-de-Sitter equations. To check it directly,
in unitary clock gauge the relevant quadratic terms on any FLRW are

    C a^3 [x_dot^T Ms x_dot/2-x^T Ks x/2
                    +p n S+KH p^2 n^2/2].               (5)

The lapse derivative gives (4). There is no shift or spatial-metric
perturbation in (5), hence no first-order momentum or spatial stress from
this zero-background sector. Those enter at higher perturbative order.
Its background stress is zero, so these linear momentum/spatial-stress
statements are unchanged by the transformation to Newtonian gauge.
The already separated constant rhoLambda contributes only its usual
background metric stress, not an extra excitation perturbation.

## 3. Exact cancellation gives the pressureless interface

The density and phase variations, normalized-clock equation and soft modes
give, without using any special Hdot relation,

    V_dot=Phi,
    delta_H_dot=3Psi_dot-p^2 pi,
       delta_H=delta rho_H/rho,
    Pcal_dot+2H Pcal=rho p(V-pi),
    Ms(x_ddot+3H x_dot)+Ks x=b p(Phi-pi_dot).             (6)

Because p_dot=-Hp and rho_dot=-3Hrho, the polarization contrast obeys

    d[(delta rho_pol)/rho]/dt=-p^2(V-pi).                 (7)

Define the TOTAL effective contrast, without a second abundance,

    delta_d=(delta rho_H+delta rho_pol)/rho.

Equations (3)-(7) imply exactly

    delta_d_dot=3Psi_dot-p^2 V,
    V_dot=Phi,
    delta T_d^0_i=-rho partial_i V,
    delta p_d=0,        delta anisotropic stress_d=0.      (8)

These are the pressureless scalar conservation/stress equations in the
stated sign convention. Combined with (1), the ordinary stress and the
linear Einstein equations, they are a closed metric interface. For example

    delta rho_total=-2Mpl2[p^2 Psi+3H(Psi_dot+H Phi)]      (9)

uses delta rho_total=rho delta_d+delta rho_o; the momentum and
anisotropic-stress equations retain ALL ordinary contributions. No equation
sets Phi=Psi when the ordinary sector supplies anisotropic stress.

The cancellation is a consequence of the same clock variation and stress,
not an algebraic fit or deletion of the polarization. It works at arbitrary
nonzero k in this linear limiting theory; no subhorizon Poisson shortcut
has been used. The homogeneous k=0 constraints remain separate.

## 4. The independent internal condition still has to hold

Since Phi-pi_dot=v_dot by (6), the internal equations remain

    KH(v_ddot+H v_dot)+(S_dot+2HS)/p-(rho/C)v=0,
    Ms(x_ddot+3H x_dot)+Ks x=b p v_dot.                  (10)

The metric response is closed by (8), while (10) fixes the relative clock
and the split between hard energy and signed polarization. The expansion
H now includes the ordinary components. In the finite-band slow-response
limit, (10) reduces to

    v_ddot+H v_dot-rho v/(2Mpl2)=0.                      (11)

It is NOT generally d(v_dot+Hv)/dt=0: instead that derivative equals
-(rho_o+p_o)v/(2Mpl2). The earlier simplification used a background
containing only hard pressureless energy and a constant vacuum.

For an illustrative pressureless era with constant hard fraction F of the
total pressureless background, a proportional to t^(2/3) and (11) has

    v proportional to t^s,       s=[1 +/- sqrt(1+24F)]/6.

The corresponding compensated physical tilt p v grows on the plus branch
when F>1/3. This is an analytical property of the stated slow-response
limit, not a fitted cosmological result or proof that a preparation excites
that branch. Slow soft modes require the full equation (10). Setting the
metric perturbation of such a compensated sector to zero does not remove
its internal physical fields or certify their nonlinear evolution.

## 5. What can and cannot be passed to an acoustic calculation

The interface (8) can be supplied to a linear Einstein/matter solver as the
same pressureless component, with rho fixed by the network-state ledger.
If the background densities, primordial/initial perturbations and ordinary
microphysics are also chosen identical to a reference pressureless model,
then its metric/ordinary linear equations are identical in this ideal limit.
That is a conditional equation-level equivalence, not a computed CMB spectrum,
likelihood, independent prediction or observed preference for UNT.

Ordinary photon transport, recombination, scattering, baryon pressure and
any chosen radiation production/initial condition would be imported explicitly
for that comparison. This note does NOT derive photons as network hum or
replace a primordial-radiation explanation. A distinct continuous photon
source proposal must supply its own energy, spectrum and perturbation terms;
one cannot use the ordinary-photon interface while silently changing those
terms.

The constructive gain is that a nonzero network excitation now has a complete
linear gravitational stress/continuity interface, including radiation-era
backgrounds, rather than only w=0 or a static susceptibility. Its realization,
finite-gap/phase corrections and internal-clock admissibility are still
separate physical requirements of the SAME candidate parent.
