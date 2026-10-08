# Same-T bounded pressure and gradient modes: full FLRW interface V002

2026-10-06 02:46 UTC. NEW narrow clarification of the frozen V001, which remains unchanged. Prospective effective-action test. The physical phase identification in shared-action Eq4 is expressly adopted for this candidate: the pressure phase is the gradient parent's normal T. This replaces the old independent-U spatial sector, rather than relabeling its K(X) implementation. Keep ONE Einstein coefficient with G=GN, the inherited physical A/I0/Q0/eps/ordinary inventory, ell=100pc, positive constant mode inertia and the intrinsic vector gradient. No separately averaged hard sector or hard KH contact is present. Native remainder is absent in this minimal effective hypothesis; this does not derive, cancel or replace the separately retained native count/formation action. No trajectory or numerical outcome was calculated to write this note.

## 1. One background with the inherited absolute inventory

Use c_p=1 temporarily, proper time t, q=k/a, M²=(8pi GN)^(-1), phase norm Qbar, nphi=P_Q, W=Qbar nphi and D=Qbar²P_QQ. On the inherited positive-charge convex branch,

    nphi_dot=-3H nphi, Qbar_dot/Qbar=-3H cs²,
    cs²=W/D, W_dot=-3H(1+cs²)W,
    3M²H²=rho_phi+rho_b+rho_r,
    H_dot=-(W+rho_b+4rho_r/3)/(2M²).                    (1)

Ordinary matter is cold, radiation is a conserved PERFECT radiation fixture. Its anisotropic stress is set to zero as a disclosed late-window approximation, not obtained by deleting a hierarchy in a new CMB prediction. The physical pressure law, including its absolute vacuum A, is the pinned shared-action Eq1. No new vacuum offset, abundance or background mode energy is added. All modes have zero homogeneous coordinates and velocities. The old ratio Gcos/GN=.98 is used only to recover the old physical inventory; the new normal constraint uses GN. Therefore H_new(a)=H_old(a)/sqrt(.98) at fixed physical inventory, not the old H(a) relabeled.

Let H_star=67.49711988577813 km/s/Mpc be the OLD Hunit, converted to inverse proper seconds. Q0=100H_star remains fixed. The latest frozen joint tuple gives eps=1e-6, Omega_A=.7, d0=.35857141419482286, OB=.04659233656879551 and OR=8.996751426107524e-5. The latter is the candidate's conserved photon-plus-neutrino radiation inventory. Define Dnorm=1/eps+ln[eps/(1+eps)], s>0 and qphi=Qbar/Q0 by

    dphase=d0 a^-3=2 qphi s/(eps Dnorm),
    qphi²=1+eps s/(1+s),
    P/A=-1+[ln(1+s)-s/(1+s)]/Dnorm,
    rho_phi/A=1+qphi dphase-[ln(1+s)-s/(1+s)]/Dnorm,
    cs²=eps s/[2+(4+3eps)s+2(1+eps)s²].                 (2)

This is a background charge solve, not a new calibration. The conserved I0 fixes dphase. The same calibrated physical baryon/radiation densities and absolute A are retained, including the previously exposed two fit freedoms; neither is refitted to growth.

## 2. Complete linear matter, normal and metric equations

Write ds²=-(1+2Phi)dt²+a²(1-2Psi)dx² and T=Tbar+Qbar pi, with pi in proper-time units. Set e=delta rho_phi=W d and delta p_phi=cs²e. The preferred-normal acceleration source is grad_phys(Phi-pi_dot). Let z_j be the longitudinal mode acceleration in c_p=1 units, omega_j=omega_max s_j, normalized positive weights w_j approximating 2s ds, sum w_j=1, and Z=sum w_j z_j. The SAME critical conversion C Kb=2M² gives

    rho_pol=-2M² q Z,
    delta p_pol=Qmom_pol=anisotropic_stress_pol=0        (3)

at linear order about zero modes. Potential, kinetic and intrinsic-gradient energies begin at quadratic order; their normal variation already enters the polarization power. The pressure and mode equations are

    pi_dot=Phi+e/D+3H cs²pi,
    e_dot=-3H(1+cs²)e+3W Psi_dot-W q²pi
                                  +2M²q(Z_dot+2H Z),
    z_j_dot=v_j,
    v_j_dot=-3H v_j-omega_j²(1+ell²q²)z_j
                                  +omega_j²q(Phi-pi_dot). (4)

Cold matter and perfect radiation are fully retained:

    delta_b_dot=3Psi_dot-q²v_b, v_b_dot=Phi,
    delta_r_dot=4Psi_dot-4q²v_r/3,
    v_r_dot=H v_r+Phi+delta_r/4.                         (5)

Here velocities are covector velocity potentials in proper-time convention; the radiation H v_r term is required. No anisotropic stress implies Phi=Psi. Define Qmom=W pi+rho_b v_b+4rho_r v_r/3. The Einstein momentum and normal constraints are

    Psi_dot+H Phi=Qmom/(2M²),
    R_N=q²Psi+3H(Psi_dot+H Phi)
       +[e+rho_b delta_b+rho_r delta_r-2M²qZ]/(2M²)=0.   (6)

The spatial trace, independently checkable from the evolved state, is

    Psi_ddot+H(Phi_dot+3Psi_dot)+(2H_dot+3H²)Phi
                      +q²(Psi-Phi)/3=delta p_total/(2M²). (7)

Equations(1),(4),(5) give delta rho_dot+3H(delta rho+delta p)=3Wtot Psi_dot-q²Qmom and Qmom_dot+3HQmom=Wtot Phi+delta p, where Wtot=W+rho_b+4rho_r/3. Consequently R_N_dot=-3H R_N exactly. The +2M²q(Z_dot+2HZ) source in(4) cancels rho_pol_dot+3Hrho_pol. This verifies full normal propagation rather than enforcing the normal equation by projection. A real radiation hierarchy would require its corresponding shear, momentum and Phi-Psi equations; this fixture makes no claim about that replacement.

## 3. Closed dimensionless first-order matrix

Use tau=H_star t, prime=d/dtau, rho*=c_p²H_star²/(4pi GN), h=H/H_star, K=c_p k/(aH_star), L=ell H_star/c_p, b=rho_b/rho*, r=rho_r/rho*, w=W/rho*, Dbar=D/rho*, E=e/rho*. Let u=H_star pi, ub=H_star v_b, ur=H_star v_r, zeta_j=z_j,SI/(c_p H_star) and xi_j=zeta_j'. Thus z_j,SI is physical acceleration, and rho_pol,SI=-c_p²(k/a) Z_SI/(4pi GN); its normalized value is -K Zeta. Set Omega_j=(omega_max/H_star)s_j, Zeta=sum w_j zeta_j, Xi=sum w_j xi_j and c_s=cs² (a squared sound-speed fraction, not c_p).

In the state order Y=(Phi,delta_b,ub,delta_r,ur,u,E,{zeta_j},{xi_j}), the following linear rows specify the entire time-dependent matrix, with no implicit unknown derivative remaining after substitution:

    Q=w u+b ub+4r ur/3,      Phi'=Q-h Phi,
    u'=Phi+E/Dbar+3h c_s u,
    E'=-3h(1+c_s)E+3w(Q-h Phi)-wK²u+K(Xi+2hZeta),
    delta_b'=3(Q-h Phi)-K²ub,      ub'=Phi,
    delta_r'=4(Q-h Phi)-4K²ur/3,
    ur'=h ur+Phi+delta_r/4,
    zeta_j'=xi_j,
    xi_j'=-3h xi_j-Omega_j²(1+L²K²)zeta_j
                     -Omega_j²K[E/Dbar+3h c_s u].       (8)

In particular, the direct Phi terms cancel from each xi row: the freely varied normal source is not an externally clamped gravitational force. For integration in x=ln a use dY/dx=(1/h) times(8), not a different matrix. Background h'=-Btot, Btot=w+b+4r/3, K'=-hK. Equation(2) and the old physical inventory give A/rho*=3Omega_A/(2*.98), b=3OB a^-3/(2*.98), r=3OR a^-4/(2*.98), w=(A/rho*)qphi dphase, Dbar=w/c_s and h²=2[(rho_phi/rho*)+b+r]/3.

The dimensionless normal, trace and signed energy inventory are

    R=K²Phi+3hQ+E+b delta_b+r delta_r-KZeta, R'=-3hR,
    Phi''+4hPhi'+(2h'+3h²)Phi=c_s E+r delta_r/3,
    delta rho_total/rho*=E+b delta_b+r delta_r-KZeta.    (9)

The first-order system evolves the momentum equation and tests the normal/trace independently. No stiffness inverse, static mu replacement or instantaneous metric solve removes an evolved state variable.

## 4. Two exact-constraint basis seeds and fixed prospective census

At ai=.01, use common velocity u=ub=ur=U, modes zeta=xi=0, delta_b=Dseed, delta_r=4Dseed/3, E=w_iDseed. With B_i=w_i+b_i+4r_i/3,

    Dseed=-K_i²Phi_i/B_i-3h_iU,
    Phi'_i=B_iU-h_iPhi_i.                              (10)

Freeze potential seed (Phi_i,U)=(1e-8,0) and velocity seed (0,1e-8/h_i). Both are exact Hamilton/momentum-compatible directions in the instantaneous isentropic/common-velocity subspace. Their amplitude is a numerical basis normalization, not an inferred primordial amplitude or a choice of growing mode. Keep both seed signs and all outcomes. The initial zero modes are a retarded prepared-state premise, not a thermalization result.

The bounded screen is ai=.01 through a=1, k={.01,.1} Mpc^-1 and omega_max/H_star={.1,1,10,100}, all sixteen k/omega/seed cases. Use the frozen ell=100pc, invariant physical pressure inventory and perfect radiation. Root's prospective numerical design uses log-a RK4 16384/32768 steps and spectral 48/96; its source/protocol must freeze actual full-state comparison gates, output/custody/checkpoint rules before execution. Include a mode-off omega=0 reference with the SAME GN background and both seeds. This ablation is not an optimized GR or old K(X) comparison. All failures and signed full-state differences survive; no omega, k, seed or time is selected from results.

Independent controls should retain background charge/Friedmann derivatives; normal propagation, trace and total continuity; full-state time/spectrum refinement; weight normalization and real mode positivity; mode-off limits and no spurious source at zero data. In a nongravitating frozen local patch, the coupled free clock/modes conserve [D pi_dot²+Wq²pi²+C(v^T Ms v+x^T(Ks+Jsq²)x)]/2: coupling powers cancel gyroscopically. This is a free-sector check, not full gravitational stability. The W=0 regular retarded gradient branch is geodesic; clamped growth does not replace it. A static-response value is not a new time-history prediction.

## 5. Physical readouts and a falsifiable domain ceiling

Keep signed ordinary comoving contrast delta_b+3h ub and density b(delta_b+3h ub), clock comoving density E+3h w u, radiation comoving density r(delta_r+4h ur), polarization -KZeta and Weyl potential Phi=Psi. Equation(9) gives -K²Phi as their sum. Report the normal acceleration K(Phi-u'), clock pressure c_sE and all mode/source phases. Transfer ratios with vanishing denominators must retain explicit refusal, rather than become zero or infinity by convention. A k/H or weak-metric diagnostic is separate from arithmetic qualification; the equations themselves retain the full linear constraints, not a subhorizon-only Poisson approximation.

The actual pressure-rate perturbation obeys delta Q/Qbar=c_s E/w. For a real sinusoidal unit-basis transfer, the admissible amplitude must be below inf_a min(Qbar-Q0,Qcap-Qbar)/|Qbar c_s E/w|, with a zero denominator imposing no bound at that time. Keep this ceiling and the fixed 1e-8 arm's domain/linearity status; do not fit frequency, offset, eps or seed normalization after outcomes. Linear transfers may be saved where their physical amplitude fails. The twelve retained static patch violations/passes remain their separate aligned-inheritance test. This full same-T evolution does not yet supply their nonlinear galaxy phase/state solution, a new CMB likelihood or a unified observed galaxy-and-expansion history.

## Frozen direct inputs

Paths are relative to this directory. No antecedent is mutated.

| Input | SHA256 |
|---|---|
| INVARIANT_CLOCK_GRADIENT_SHARED_ACTION_BUDGET_DOMAIN_AND_NORMAL_V001.md | 8359678351bc69f6e58abc6e0355e9b1f7d450138645c8939b944b0769c16e08 |
| GRADIENT_PARENT_LONGITUDINAL_RESPONSE_AND_NORMAL_CONSTRAINT_V001.md | 633d604e5b655d1df096c4bba01c340f25f91460364bf7080df7d1604368560c |
| SPHERICAL_GRADIENT_COMMON_LENSING_CLOSURE_V001.md | a4221d6ed0d5b0fed266e9fc8e27fa190b3f911e39cc7d218912418d1cc69b57 |
| INVARIANT_CLOCK_JOINT_CALIBRATION_V003_RESULT.json | c92eb0ce131a61009361f2ead3f4db7522d3eabb22f7e3d472f0e4e0c116c24f |
| SPHERICAL_GRADIENT_BOUNDED_CLOCK_PATCH_SPAN_V001_RESULT.json | 2f4862ebe1bba0faa5588b7c02d88af7d8233d88c436bc0109e3b7eee206afb0 |
| INVARIANT_CLOCK_GRADIENT_SAME_T_FLRW_INTERFACE_V001.md | 8a2a4e63bfe64586ff1663701ec9fe985ab8ae4c5a16aa5b43123cbe7baf9d3e |
