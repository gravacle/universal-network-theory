# Constrained-U early adiabatic hierarchy and new thermal transfer V001

Prospective derivation; precise authorship and freeze times are recorded by file metadata and root ownership journals; root owns subsequent numerical execution. This joins ordinary linear Thomson photons/polarization and collisionless massless neutrinos to the NEW constrained-U/physical-phase/one-gradient action. It does not transplant an old-action transfer, select a late subhorizon mixture, claim thermal generation, or supply an angular-data likelihood. The inherited finite thermal preparation and positive curvature convention are disclosed premises.

## 1. Physical normalization and background

Set tau=Hstar*t_proper, h=H/Hstar, q=k*c_p/(a*Hstar), r_i=rho_i/(2 M_bare^2 Hstar^2), and every velocity u_i=Hstar*v_i. Hstar=67.49711988577813 km/s/Mpc is fixed as a unit. KB=.02, C=1.98, Mbar=.5 and Cbar=.99; G_bare=.99 GN. The complete selected V003 physical inventory is unchanged, so H_new(a)=sqrt(.99/.98) H_old(a), not the old .98 Friedmann law. The old density entries divide by rG=.98/.99 in the new bare unit. No vacuum endpoint or A/I0 charge is reset.

The NEW default/half HYREC pair has been accepted by root, with newly evolved xe/Tm and identical physical omega_b/T0/YHe. Its lossless output/receipt hashes below are the transfer's inputs. Above z=8000, fully ionized hydrogen/helium and Tm=T0/a are a declared finite high-temperature thermal fixture. Neff=3.0439772985579183 and YHe=.24356210948040835 remain the inherited preparation in this packet, not NEW BBN predictions. Root's separate new-background BBN test may later give a distinct parent. No old xe table is used as new-action evidence.

Write b for baryons, r_gamma/r_nu for radiation, w for the clock enthalpy, c=cs^2>0, Q for the background phase rate in Hstar units. The exact same P derivatives give Q'/Q=-3hc, w'=-3h(1+c)w and h'=-b-4(r_gamma+r_nu)/3-w. Ordinary radiation obeys r_i'=-4hr_i. All derivatives below are proper-time tau derivatives, not conformal derivatives.

## 2. Closed ordinary hierarchy

State Psi is the spatial Newtonian potential; Phi is the lapse. Let F_gamma,l/F_nu,l be brightness moments with F_2=2*sigma_MB, and G_l photon polarization. Photon/neutrino first moments are F_i1=4q*u_i/3. The exact linear shear and momentum rows are

    Phi=Psi-2(r_gamma F_gamma2+r_nu F_nu2)/q^2,
    Psi'=b*u_b+4*r_gamma*u_gamma/3+4*r_nu*u_nu/3+w*V-h*Phi.

The factor two follows the NEW density unit and must not be copied from an old M^2-unit source. Cold baryons use delta_b'=3Psi'-q^2 u_b and u_b'=Phi+(g/Rb)(u_gamma-u_b), with Rb=3b/(4r_gamma), g=n_e*sigma_T*c_p/Hstar. Ordinary baryon thermal pressure is omitted in this bounded cold-baryon fixture; Tm and a pressure-size diagnostic remain available, not a precision baryon-temperature perturbation closure.

Photons obey delta_gamma'=4Psi'-4q^2u_gamma/3 and u_gamma'=h*u_gamma+Phi+delta_gamma/4-F_gamma2/2+g(u_b-u_gamma). For Pi=F_gamma2+G_0+G_2,

    F_gamma2'=q(2F_gamma1-3F_gamma3)/5-g(F_gamma2-Pi/10),
    F_l'=q[l F_(l-1)-(l+1)F_(l+1)]/(2l+1)-g F_l, l>=3,
    G_l'=q[l G_(l-1)-(l+1)G_(l+1)]/(2l+1)
            -g[G_l-Pi/2*(delta_l0+delta_l2/5)].

For G_0 the stream is -q*G_1. Neutrinos have the same unscattered brightness streaming, delta_nu'=4Psi'-4q^2u_nu/3 and u_nu'=h*u_nu+Phi+delta_nu/4-F_nu2/2. Their anisotropic stress is retained. A finite hierarchy is a Galerkin angular truncation with the next moment set to zero; hierarchy-refinement and its full saved tails remain numerical controls, not claimed exact angular completion.

## 3. Same constrained physical phase and dynamical modes

Use retained mode nodes s_i>0, weights w_i>0 summing to one, omega_i=omega_max*s_i, Z=sum w_i z_i and Zd=sum w_i zd_i. No static susceptibility replaces their dynamics. Define

    L=Q*q, L'=-h(1+3c)L,
    L''=[h^2(1+3c)^2-h'(1+3c)-3h*c']L,
    v=Z/L, vd=(Zd-L'v)/L, Gamma=d+3h*V,
    n_U=vd-c*Gamma, pi_U=V-v,
    P=(KB/2)*q*n_U+Cbar*Z,
    V'=Phi+c*Gamma,
    d'=3Psi'-q^2*V-Cbar*Q*q*sigma/w,
    z_i'=zd_i,
    zd_i'=-3h*zd_i-omega_i^2[(1+ell^2q^2)z_i-q*n_U-sigma].

The full same-action reaction uses alpha=sum w_i omega_i^2, R1=sum w_i omega_i^2 z_i, D=w/c,

    n0'=-h*n_U-C*(Zd+2hZ)/(KB*q),
    d0'=3Psi'-q^2V,
    vd0'=n0'+c'*Gamma+c*d0'+3c*h'*V+3c*h*V',
    Delta=alpha+C*Q^2/KB+Cbar*Q^2*q^2/D>0,
    sigma=[L*vd0'+2L'*vd+L''*v+3h*Zd+(1+ell^2q^2)*R1-alpha*q*n_U]/Delta.

This is the full-Hubble reduced chart with the only ordinary-radiation change being its actual Psi'/Phi sources. n_U and sigma may be introduced as stage algebraic coordinates for an implicit solve; eliminating those coordinates or solving its dynamic block Schur complement does not remove a mode, pole or kinetic term. The full omitted P Euler row is independently testable from individual mode accelerations and the chain-derived n_U': P'+2hP+Cbar*Q*sigma=0.

## 4. Einstein/Thomson Ward controls

The normal residual is

    R=q^2Psi+3h(b*u_b+4*r_gamma*u_gamma/3+4*r_nu*u_nu/3+w*V)
      +b*delta_b+r_gamma*delta_gamma+r_nu*delta_nu+w*d-q*P.

Using ordinary collision cancellation and phase/polarization power exchange gives R'=-3hR. The trace is

    Psi''+h(Phi'+3Psi')+(2h'+3h^2)Phi+q^2(Psi-Phi)/3
      =c*w*d+(r_gamma*delta_gamma+r_nu*delta_nu)/3.

The coefficient three is the proper-time conversion; the conformal-time coefficient two is not applicable. These identities retain photon/neutrino shear and all phase/mode source contacts. Mode polarization has no independent linear pressure, momentum or shear about the stipulated zero-mode background. This does not assert those contacts vanish on a populated/nonlinear sector. One total calibrated GN is counted once.

## 5. Regular adiabatic leading branch and exact finite-start constraint

In radiation domination let Rnu=r_nu/(r_gamma+r_nu). The bounded no-extra-entropy/no-extra-mode branch has

    Psi=(1+2Rnu/5)Phi, V=u_b=u_gamma=u_nu=Phi/(2h),
    delta_b=d=-3Phi/2, delta_gamma=delta_nu=-2Phi,
    F_nu2=(2/15)(q/h)^2Phi,
    Rstar=Psi+hV=(3/2+2Rnu/5)Phi=1e-5.

Rstar's positive sign is the inherited resident convention; it is not silently renamed the opposite common zeta sign. The leading bounded modes have z~a^6, zd~a^4, v~a^7 because the first gradient forcing sigma~a^2. Thus z=zd=0 is leading-order data, not an exact all-orders regular seed. The action's real finite-start approximation must be tested by transporting an earlier start, without reseeding at a=.01.

For a finite start with retarded z=zd=0, define B=b+4(r_gamma+r_nu)/3+w. Choose common V and set exactly

    d=-q^2Psi/[B+(KB/2)q^2c]-3hV,
    delta_b=d, delta_gamma=delta_nu=4d/3,
    pi_U=V, n_U=-c(d+3hV), P=(KB/2)q*n_U.

This makes R=0 exactly; using the old same-T denominator B would violate the NEW hard constraint. A leading tight-coupling photon quadrupole F_gamma2=32*q^2*V/(45g), with G0=5F_gamma2/4 and G2=F_gamma2/4, may be retained. Together with leading F_nu2 its exact finite shear sets A_slip=1+4r_nu/(15h^2)+32r_gamma/(45hg), Phi=Rstar/(A_slip+1/2), Psi=A_slip*Phi, V=Phi/(2h). Higher neutrino leading moments recurse F_l=(q/h)F_(l-1)/(2l+1); photon/polarization tight-coupling higher moments recurse q*l*F_(l-1)/[(2l+1)g]. These are explicit finite approximations, not a favorable phase/primordial fit. The seed/start-refinement, normal, shear, first-jet and omitted-Euler checks must all be retained.

## 6. Bounded executable discriminator

The next source will retain k=.01 Mpc^-1, all omega_max/Hstar=.1,1,10,100, Rstar=1e-5, a=1e-7 through one, the fixed new default/half atomic pair and all full mode/hierarchy states. A half-start a=5e-8 will be transported to the common start. Distinct time, mode, hierarchy, start, atomic and thinning trials are prospective numerical controls. An implicit two-stage Radau IIA stage solve uses the authenticated resident coefficient implementation but no old module or calibration is imported. Dynamic block solves are appropriate to its tridiagonal radiation tails and independent modal kinetic blocks; no static infimum enters.

Readouts include signed photon monopole+Phi, velocities, Weyl Phi+Psi, F2/Pi, comoving baryon/clock/radiation density, polarization and hard/soft source pieces, normal acceleration q*n_U, all constraint/Euler residual terms and phase-domain heads. The inherited Rstar is an input, not a NEW measured primordial spectrum. Any linear-domain violation/refinement failure is exposed. This packet provides a conditional early-to-late transfer; angular C_l, sigma8, merger history, reionization, survey likelihood and data superiority require their actual additional sources/observables. The stationary aligned-galaxy span failures and previous action failures remain intact.

Ordinary conventions are supported by [Ma and Bertschinger 1995](https://arxiv.org/abs/astro-ph/9506072); the equations here are derived in the declared new units and are not an old-action prediction.

| Direct input | SHA256 |
|---|---|
| constrained_u_clock_gradient_flrw_reduced_chart_v002.py | 6d9878bb854bc7147aefcdcd358c6cecd16087a9577960f10686f5c4d17094b9 |
| CONSTRAINED_U_CLOCK_GRADIENT_FLRW_REDUCED_CHART_V002.md | 5d644d9d07d6d2dbf4f44a20e329e30965ef0c558a052359bda102dc0b5aba1b |
| INVARIANT_CLOCK_GRADIENT_CONSTRAINED_U_REDUCED_CHART_AND_RETARDED_RESPONSE_V001.md | 0a15eee6701a4a9230202141422e428e772d57dbfb395a386721f8ea289e0a54 |
| INVARIANT_CLOCK_GRADIENT_SHARED_ACTION_BUDGET_DOMAIN_AND_NORMAL_V003.md | e08b7166892ec59c863539d59b8d4b89c654081776d8870239ecc2c382572da0 |
| INVARIANT_CLOCK_JOINT_CALIBRATION_V003_RESULT.json | c92eb0ce131a61009361f2ead3f4db7522d3eabb22f7e3d472f0e4e0c116c24f |
| constrained_u_clock_gradient_recombination_pair_v002.py | 3cf9dbb9c68a1a1495e255de68cc399a2c2242a4edaa1acfc8bb870dd1cb29f4 |
| CONSTRAINED_U_CLOCK_GRADIENT_RECOMBINATION_PAIR_V002.md | 09c2ee0071903b262c702cd8c91e1a9050d99f813c0a085ca042d630a537b54e |
| CONSTRAINED_U_CLOCK_GRADIENT_RECOMBINATION_PAIR_V002_RESULT.json | 008d86b296fc7c5856b5827b4cb3c0a7646e4cbe526cc0d7cd9013f02fbfeed4 |
| CONSTRAINED_U_CLOCK_GRADIENT_RECOMBINATION_PAIR_V002_RECEIPT.json | 1f210c196856d56294c13c35d7630e88f986015892df4f2856b5d2ce95dedcb4 |
| CONSTRAINED_U_CLOCK_GRADIENT_RECOMBINATION_PAIR_V002_DEFAULT_OUTPUT.json | 058ec2622e89bfd57c11c965444feabc0b3228b566373341b3d2b95836c168ba |
| CONSTRAINED_U_CLOCK_GRADIENT_RECOMBINATION_PAIR_V002_HALF_OUTPUT.json | 58e5aafe79d42c88d14359c66f90372192d298a3a7d7d370c84daa38dacbfc57 |
| invariant_clock_plasma_v001.py | 08cfd9e54759db07683bf652e32ad5aa69ec3006090f548e5d82b5678e8a6a28 |
| invariant_clock_recombination_transfer_v002.py | 54674a431945eb7e17fc2b39af2324c923d8cfc5e991dc87a8cf96465dd1fa45 |
| FINITE_SLICE_CMB_PREPARATION_AND_BOLTZMANN_ROUTE_V001.md | 7b9a4952f279d9a32b6a6d5de9338f01b50bd3cbd6a1eab8cced8bad5f593cd4 |
