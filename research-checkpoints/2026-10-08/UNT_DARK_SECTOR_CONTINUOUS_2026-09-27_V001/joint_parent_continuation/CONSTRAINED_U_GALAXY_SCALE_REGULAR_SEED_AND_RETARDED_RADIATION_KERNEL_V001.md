# Same-action regular galaxy-scale seed and retarded radiation kernel V001

Prospective 2026-10-06 04:46 UTC. This is an analytical parent for a new transport method. No new trajectory, seed normalization, kernel quadrature or native operator was evaluated by the author. Root alone executes reviewed workers. The running k=.01 full-tower packet is an independent-method reference only after its complete result and receipt close; it is not rerun here. The current physical action, absolute A/I0, one-G normalization, inherited curvature input and new BBN/HYREC helium are retained.

## 1. Conventions and regular amplitude

Use conformal **length** eta=integral c_p dt/a in Mpc, x=k eta, and the proper dimensionless time tau=H_* t. H_* is the fixed old calibration unit, not H(a). q=q0/a with q0=k c_p/H_* in compatible Mpc units. Let h=H/H_*, h_r=sqrt(Omega_R/r_G), r_G=.98/.99, R=the fixed ideal-radiation neutrino fraction. The physical .99 bare-G background is retained; the old .98 H(a) is not imported as the new history.

The incoming lapse amplitude A is fixed **before** varying the start by the asymptotic regular curvature:

    A = R_* /(3/2+2R/5),                 R_*=1e-5.             (1)

Finite-start Psi+h V_clock differs from this limit at order x^2; renormalizing it independently at each start changes the incoming growing amplitude. This input is not a measured primordial spectrum or a best fit.

## 2. Radiation regular terms

In the radiation-dominant, tightly coupled photon/baryon limit, write Phi/A=1+f x^2 and Psi/A=1+2R/5+g x^2. The independently derived coefficients are

    f=(56R^2+10R-525)/[630(25+2R)],
    g=-(56R^2+580R+525)/[630(25+2R)],
    t_gamma=(f+g)/3-1/36,  t_nu=t_gamma-1/45,
    delta_gamma=delta_nu=A[-2+(4g-1/3)x^2],
    delta_b=d_clock=(3/4)delta_gamma,
    theta_gamma/k=theta_b/k=A[x/2+t_gamma x^3],
    theta_nu/k=A[x/2+t_nu x^3],
    theta_clock/k=A[x/2+(f/4)x^3],
    F_nu2=A[2x^2/15+(2t_nu/15-1/350)x^4],
    F_nu3=2A x^3/105,  F_nu4=2A x^4/945.                 (2)

They satisfy f+4g=-1/6-2R/15 and g-f=(2R/15)(f+g)-R/35; R=0 gives f=g=-1/30. Baryons follow the photon velocity through the x^3 term while Thomson locking applies. Their velocity cannot be replaced by the cold phase velocity at this order. The finite curvature is A[3/2+2R/5+(g+f/4)x^2+...], with -A x^2/24 correction at R=0.

The first matter correction has m=(Omega_b+Omega_A q_inf d0)/Omega_R and q_inf=sqrt(1+epsilon). At k=0,

    Phi=A+Phi1 a, Psi=A(1+2R/5)+Psi1 a,
    Phi1=m A*5(8R-3)/[16(15+2R)],
    Psi1=-m A*(15+16R)/[16(15+2R)],
    V_clock=A a^2/(2h_r)+(Phi1-m A/2)a^3/(3h_r),
    delta_rad=-2A+4Psi1 a, delta_cold=-3A/2+3Psi1 a,
    H_* eta/c_p=(a/h_r)(1-m a/4)+... .                    (3)

This obeys Phi1+3Psi1=-m A/4. Mixed a x^2 terms, baryon loading, finite opacity and thermal changes are distinct remainder sources; equations (2)-(3) are not an exact finite-start solution. START refinement must compare the same asymptotic A, full transported state and actual signed sources.

## 3. Genuine regular native kinetic terms and finite constraint

For the declared constrained-U action, c_s^2=c3 a^3+..., c3=1/[sqrt(1+epsilon)*norm*d0], norm=1/epsilon-log1p(1/epsilon), Q_c=Q0/H_* sqrt(1+epsilon). Let Gamma=d+3hV=Gamma2 a^2+..., Gamma2=A(3g-1/4+3f/4)(q0/h_r)^2. For the retained mode quadrature define alpha=sum w_i omega_i^2 and Delta0=alpha+C Q_c^2/K_B. The regular branch has

    sigma2=6h_r Q_c q0 c3 Gamma2/Delta0,
    sigma=sigma2 a^2+..., z_i=omega_i^2 sigma2 a^6/(42h_r^2)+...,
    z_i_dot=6h_r z_i6 a^4+...,
    v=alpha sigma2 a^7/(42h_r^2 Q_c q0)+...,
    n_U=-[C Q_c^2/(K_B Delta0)]c3 Gamma2 a^5+... .          (4)

Here dot is d/dtau. The factor42 follows z_ddot+3h z_dot=42h_r^2 z_i6 a^2. The q n_U and spatial-gradient terms start later, at order a^4 in the modal force. No homogeneous incoming mode or favorable transient is selected.

At a finite start construct the regular series and fix A. Impose the actual shear Psi=Phi+2(r_gamma F_gamma2+r_nu F_nu2)/q^2. For a raw normal residual R00, shift delta_b,d by t and delta_gamma,delta_nu by 4t/3 while preserving velocities, modes and lapse. In the retained finite chart,

    t=-R00/[b+4r/3+w+(K_B/2)q^2 c_s^2].                    (5)

Reconstruct n_U, P and sigma literally. This projection satisfies the instantaneous normal/shear/holonomic constraints and adds no relative density entropy, but may add higher-order transients. Its validity is earned through START controls, not its exact constraint residual alone.

## 4. Exact collisionless memory, without a huge tower

For j_l the spherical Bessel function, derivatives below are with respect to its argument. The exact collisionless solution is

    F_l(eta)=I_l(eta)-4Phi(eta)delta_l0+4Phi_i j_l(k Deltaeta)
             +4 integral_(eta_i)^eta (Phi'+Psi')(s)j_l[k(eta-s)]ds. (6)

I_l transports the **actual** initial angular distribution. Through its first four moments,

    I_l=F0i j_l+3F1i j_l'
       +(5F2i/2)(3j_l''+j_l)
       +(7F3i/2)(5j_l'''+3j_l')+higher supplied moments.      (7)

This is not a monopole reset. The equivalent forcing is 4 integral[Psi' j_l+k Phi j_l']. These follow the primary [Ma--Bertschinger equations](https://arxiv.org/pdf/astro-ph/9506072) with their spatial phi=our Psi and lapse psi=our Phi; the integral strategy is the [line-of-sight formulation](https://arxiv.org/pdf/astro-ph/9603033). They preserve the entire collisionless tower through its memory instead of imposing an artificial top boundary at L~k eta.

For an omitted old forcing tail with k(eta-s)>=X>=1, a conservative absolute low-moment error is 4 M_l(X) Var_tail(Phi+Psi), where M0=1/X, M1=1/X+1/X^2, M2=1/X+3/X^2+3/X^3. Keep I_l analytically. This becomes a useful small error only after an actual source total-variation bound is available.

## 5. Finite Thomson visibility and gas

With Gamma=a n_e sigma_T in inverse Mpc, the photon intensity source for l=0,1,2 is

    4Psi' j_l+4kPhi j_l'
    +Gamma[F0 j_l+(4theta_b/k)j_l'+(Pi/4)(j_l+3j_l'')],
    polarization source=Gamma*(3Pi/4)(j_l+j_l''),
    Pi=F2+G0+G2.                                             (8)

Multiply by exp[-integral_s^eta Gamma] and retain the attenuated true initial intensity/polarization. At zero separation the quadrupole sources are Pi/10, G0 gets Pi/2, G2 gets Pi/10, and the photon monopole has no quadrupole collision source. The leading tight seed uses G0=5F2/4, G2=F2/4 and G1=kF2/(4Gamma); its l=1 equation contains G0-2G2 and cannot use a one-sided higher-l recursion. F0,F1,F2,G0,G2 and the ordinary baryon/metric/native state must be solved **together**. Fixed-source LOS postprocessing does not constitute a coupled transfer solution.

On an explicitly fully ionized, fixed-chemistry interval, xe=1+2fHe and kappa_T=k_B T_b(1+fHe+xe)/[m_p c_p^2(1+4fHe)]. The monatomic covariant first law yields

    D_t T_b+(2/3)T_b Theta_b=Gamma_C(T_gamma-T_b),
    tau_b_dot=(2/3)delta_b_dot+Gamma_C[(5R_T-4)tau_gamma
                       -R_T tau_b+(R_T-1)Phi],
    delta p_b/(rho_b_rest c_p^2)=kappa_T(delta_b+tau_b),       (9)

where tau_b=delta T_b/T_b, tau_gamma=delta_gamma/4, R_T=T_gamma/T_b and Gamma_C=8sigma_T a_rad T_gamma^4 xe/[3m_e c_p(1+fHe+xe)]. T_b=T0/a is a tight-temperature approximation; the finite Compton lag R_T-1~H/Gamma_C must be evolved or bounded. Tight adiabatic locking gives tau_b~delta_b/3 and 4kappa_T/3 pressure, not an automatic5kappa_T/3. Baryon thermal energy/enthalpy contacts are of the same order as R_b kappa_T and must be retained or bounded together. A small local sound speed alone proves no global transfer-error bound. Recombination adds actual chemistry/temperature perturbation data beyond this fixed-ionization fixture.

## 6. Actual thermal domain and executable discrimination

The accepted new BBN saved background covers a=4.200102152213733e-12 through2.3486369459311376e-7, photon40MeV through1keV. Its saved brackets place a~1e-8 at T_gamma~23.5keV and a~5e-9 at~46.9keV. At a~1e-9 the photons are~190keV and the annihilation thermal history is active. A late fixed-Neff a^-4 source cannot be extrapolated through that region. The BBN background is owned; a full through-annihilation ordinary perturbation/weak-heating EOS has not thereby been supplied.

The immediate bounded calculation tests the exact finite-opacity polynomial-panel kernels against independent angular transport and primitive identities. This validates reusable integrals, not a field solution. A following coupled worker must retain actual metric forcing, variable visibility, gas and thermal controls, the regular amplitude/native coefficients, and start/time/source-panel refinements. The completed k=.01 full-tower state can then test the independent method without rerunning it; k=10/Mpc has a distinct forcing scale and cannot inherit its convergence. An interval or control that fails remains failed. No galaxy halo, nonlinear collapse, observational superiority or joint primordial fit follows from this construction.

## Frozen resident parents

| Parent | SHA256 |
|---|---|
| CONSTRAINED_U_CLOCK_GRADIENT_EARLY_ADIABATIC_HIERARCHY_V001.md | 1014e8689d23c35b47c2e47b7e4bed2b2b3f0f329aca061b5df3586c249fc7d2 |
| constrained_u_clock_gradient_early_transfer_v004.py | a4e78b6467b0ba5884c8da2081ff580378b4afb839a90cec548fcf30a389fa07 |
| CONSTRAINED_U_CLOCK_GRADIENT_BBN_PAIR_V001_RESULT.json | 64e55eefc0079b75994dc749f5e8853835cd3bc72a2566e9627f8b98851fdc36 |
| CONSTRAINED_U_CLOCK_GRADIENT_BBN_PAIR_V001_RECEIPT.json | e7a9cc7d8f3b59e3b9351a7a3253d5ad4e806a49340908b067600d71783d6685 |
| CONSTRAINED_U_CLOCK_GRADIENT_BBN_PAIR_V001_REFINED_STDOUT.txt | d0ec0ef40b5202420b1f064bb42b5101eb6008936cfafe8ab69b2862ca44d225 |
| CONSTRAINED_U_CLOCK_GRADIENT_BBN_HELIUM_RECOMBINATION_PAIR_V002_RESULT.json | 8edf04b504f89b0e378823c2b5eda6547138361bb5ad13f6858bd0e34ce5be20 |
| CONSTRAINED_U_CLOCK_GRADIENT_BBN_HELIUM_RECOMBINATION_PAIR_V002_RECEIPT.json | 867911256634977adc8a50cdcc9b3b2e2e7aabaed6435de25c8be80acb6253fd |
| CONSTRAINED_U_CLOCK_GRADIENT_BBN_HELIUM_RECOMBINATION_PAIR_V002_DEFAULT_OUTPUT.json | 07e8e4e7fe524fd9d1f1a19422f293f11a49573f6ee6d1bf016b17c80ec70437 |
| CONSTRAINED_U_CLOCK_GRADIENT_BBN_HELIUM_RECOMBINATION_PAIR_V002_HALF_OUTPUT.json | 1df474629eb706d1315f090de228059c59db3ad58c127be2b614c005dc471386 |
