# k10 common-density and relative-current regular jets V001

2026-10-06. Static source-led derivation, independently counterchecked by readonly. No background, coefficient, matrix, vector, operator, hierarchy, kernel or trajectory is evaluated. This is the literal k=10/Mpc post-annihilation cold/fully-ionized fixture of f708; no k=.01 coefficient is imported. Root alone may evaluate a separately reviewed bounded coefficient calculation. Both live workers, all sources, initial states, numerical thresholds and failed flags remain unchanged. These jets are necessary preparation data, not an adopted complete seed, physical birth or a microscopic/macroscopic identification.

## 1. Units, source and expansion

Dot means d/dtau, tau=Hstar*t_proper. Set r=Rnu=1-fgamma, t=1-r, q=q0/a, hr=sqrt(OR/rG), Rstar=CURVATURE, A=Rstar/(3/2+2r/5). The literal q0=k*c_p/(1000*Hunit) uses k in Mpc^-1 and Hunit in km/s/Mpc. With m=(OB+OA*sqrt(1+eps)*d0)/OR,

    h=hr*a^-2*(1+h1*a+h2*a²+...), h1=m/2, h2=-m²/8,
    b=b3*a^-3, rho_rad=(3/2)*hr²*a^-4,
    beta=b3/[2hr²*t], r_b=beta*a, gTh=g0*a^-3.          (1)

The high-z Thermal.at branch owns constant xe=1+2fHe and g0=c_p*sigma_T*nH0*(1+2fHe)/Hstar_SI, using the accepted BBN-helium HYREC nH0/fHe. This is a post-annihilation extrapolation within the same fixture; no earlier thermal history or gas-pressure equation is added. The absolute pressure background first adds relative-a4 logarithms to h; it cannot be omitted from a complete higher metric preparation.

Use R=Psi+hV, Gamma_phi=d+3hV, Gamma_b=db+3hV, Gamma_gamma/nu=delta_gamma/nu+4hV, U and W=w_gamma-w_b from the literal weighted chart. The exact source rows are Rdot=S+h*cs*Gamma_phi, Vdot=Phi+cs*Gamma_phi and Gammadot_phi=3Rdot-q²V-Cbar*Q*q*sigma/w. Here S=b*w_b+4rho_gamma*w_gamma/3+4rho_nu*w_nu/3. The correct baryon row is w_bdot=+gTh*W/r_b-cs*Gamma_phi; f708's known minus sign in separate diagnostics is not used.

Write V=sum v_j*a^j, R=Rstar+sum R_j*a^j and every other suffix j as its absolute power of a. The actual metric first jets are

    Phi1=m*A*5(8r-3)/[16(15+2r)]-12t*hr*A/[(15+2r)g0],
    Psi1=-m*A*(15+16r)/[16(15+2r)]+4t*hr*A/[(15+2r)g0],
    Phi0=A, Psi0=A*(1+2r/5), Phi1+3Psi1=-m*A/4.
    v2=A/(2hr), v3=(Phi1-m*A/2)/(3hr),
    v4=[Phi2/hr-3h1*v3-2h2*v2]/4,
    R1=0, R2=-A*q0²*(5+4r)/(120hr²),
    U4=-Rstar*q0²/(36hr³), wn4=U4-A*q0²/(45hr³).       (2)

## 2. The required finite-opacity collision lag and second metric coefficient

Let p_j=F_gamma2,j and N_j=F_nu2,j. Directly matching F_gamma2,G0,G2, including their derivatives, gives

    p3=32q0²*v2/(45g0),
    p4=32q0²*v3/(45g0)-(11/2)*(hr/g0)*p3,
    Pi3=5p3/2, G0,3=5p3/4, G2,3=p3/4,
    Pi4=(5/2)*p4-(45/4)*(hr/g0)*p3,
    G0,4=Pi4/2-15hr*p3/(4g0),
    G2,4=Pi4/10-3hr*p3/(4g0).                          (3)

The 11/2 is the first full polarization/collision lag, not a new relaxation coefficient. Angular streaming involving photon l3 or polarization l1/l3 starts too late to change p4. Replacing (3) by instantaneous tight equilibrium discards an owned term.

For neutrinos and shear,

    N2=4q0²*v2/(15hr),
    N3=[8q0²*v3/(15hr)-2h1*N2]/3,
    J3=F_nu3,3=2A*q0³/(105hr³),
    Knu=2q0²*[wn4-3h1*v3/4-h2*v2/2]/(15hr)
         -3q0*J3/(20hr)-3h1*N3/4-h2*N2/2,
    Phi2=[R2-3hr²*(t*p4+r*Knu)/q0²
               -hr*h1*v3/4-hr*h2*v2/2]/(5/4+r/10),
    N4=q0²*Phi2/(30hr²)+Knu,
    Fbar3=t*p3+r*N3, Fbar4=t*p4+r*N4,
    Psi2=Phi2+3hr²*Fbar4/q0².                           (4)

The positive 5/4+r/10 fixes Phi2 by the exact R2 identity and shear; it is not a fitted metric coefficient. Equations(2)-(4) form a sequential symbolic solve. The angular companions already fixed at this order are F_nu3,4=[3q0*N3/(7hr)-3h1*J3]/4, F_nu4,4=q0*J3/(9hr), G1,5=q0*p3/(4g0), F_gamma3,5=3q0*p3/(7g0) and G3,5=3q0*G2,3/(7g0). Higher terms remain separately required; a finite angular polynomial is not a full primordial distribution.

## 3. Common density and momentum jets

Define

    I3=(v3-h1*v2)/(3hr),
    I4=[v4-h1*v3+(h1²-h2)*v2]/(4hr),
    R3=-q0²*I3/15-Fbar3/10-7h1*R2/5,
    R4=-q0²*I4/27-q0²*R2/(108hr²)-Fbar4/18-3h1*R3/2,
    Gamma_phi,2=3R2-q0²*v2/(2hr),
    Gamma_phi,3=3R3-q0²*I3,
    Gamma_phi,4=3R4-q0²*I4.                             (5)

The general curvature recurrence has an additional -4(h1²+2h2)R2/9 in R4; it vanishes for the actual matter+radiation background at this order. With the declared no-incoming relative modes,

    Gamma_gamma,2=Gamma_nu,2=4Gamma_phi,2/3,
    Gamma_gamma,3=Gamma_nu,3=4Gamma_phi,3/3,
    Gamma_gamma,4=4R4-q0²*[v4+U4-h1*v3+(h1²-h2)*v2]/(3hr),
    Gamma_nu,4=4R4-q0²*[v4+wn4-h1*v3+(h1²-h2)*v2]/(3hr),
    Gamma_b,2=Gamma_phi,2, Gamma_b,3=Gamma_phi,3,
    Gamma_b,4=3Gamma_gamma,4/4.                          (6)

The changing photon-baryon momentum weights give

    U5=Gamma_gamma,3/(16hr)-p3/(8hr)-(3h1+4beta)U4/4,
    U6=Gamma_gamma,4/(20hr)-p4/(10hr)
          -(4h1+5beta)U5/5-(3h2+4beta*h1)U4/5,
    wn5=Gamma_nu,3/(16hr)-N3/(8hr)-3h1*wn4/4,
    wn6=Gamma_nu,4/(20hr)-N4/(10hr)-4h1*wn5/5-3h2*wn4/5,
    W6=4beta*hr*U4/g0,
    wb4=wg4=U4, wb5=wg5=U5, wb6=U6-W6, wg6=U6.         (7)

These follow from the literal U/W/neutrino rows; Thomson exchange is retained. The entropy differences recover Sbphi,4=Rstar*q0^4/(144hr^4), Sgammanu,4=-A*q0^4/(135hr^4), and Sb_gamma through a4 is zero. The native sigma2/z6/zd4/n5 first jets remain the actual f708 ones. Since cs=O(a3), h*cs*Gamma starts at proper-rate a3 and first affects R5; Q*q*sigma/w=O(a4) first affects phase entropy at a6. Thus neither contact can replace (3)-(7).

## 4. Normal/shear checks and the finite-start distinction

Independently insert (2)-(7) into q²(Psi)+3hS+b*Gamma_b+rho_gamma*Gamma_gamma+rho_nu*Gamma_nu+w*Gamma_phi-qP=0. The coefficients a^-2,a^-1,a^0 cancel. At a0, reduction by shear and Vdot leaves hr*v2*(h1²+2h2)/3=0. The exact normal reaction P=KB*q*(vd-cs*Gamma_phi)/2+Cbar*Z first enters beyond these orders, and must remain in any finite check. Shear is enforced through a2 here; normal balance at one time is not the remaining evolution/hierarchy history.

In the controlled pure-radiation/infinite-Thomson limiting ablation, let f,g,tgamma,tnu be the literal f708 radiation coefficients and un4=2tnu/15-1/350. Then R4=-A(q0/hr)^4*[(t*tgamma+r*tnu)/108+r*un4/18] and Gamma_phi,4=3R4-A*f*(q0/hr)^4/16. The existing truncated finite seed has R4=V6=0 in that ablation, and its exact normal repair instead inserts a common Gamma4=-A*g*(q0/hr)^4/2. It preserves zero entropies and does not create the missing current/curvature vector. This limiting mismatch is not a complete START prediction for the physical mixed fixture.

More generally, at held R,V,relative velocities,angular,Z,Zd, insert s=Sbphi,4*ai^4 and tS=Sgammanu,4*ai^4 via deltaGamma_phi=lambda, deltaGamma_b=lambda+s, deltaGamma_gamma=4(lambda+s)/3, deltaGamma_nu=4(lambda+s)/3-tS. Since delta ncalc=-cs*lambda, exact normal preservation requires lambda=-[(b+4rho_rad/3)s-rho_nu*tS]/D, D=b+w+4rho_rad/3+KB*q²*cs/2. Recompute sigma and n with the SAME reaction equations. This possible affine constraint insertion is not the regular solution (2)-(7), nor a seed adoption or a derivation of the entire common START defect.

A complete prepared state still needs Phi3/Phi4,Psi3/Psi4,V5/V6 and the relevant photon/neutrino/polarization higher jets, with the absolute-pressure/log background and native higher first-jet reactions. Equations(5)-(7) fix Gamma through a4 and relative currents through a6, while (4) fixes shear through a2; they do not silently supply those remaining metric/angular coefficients. Full normal/shear, momentum/trace, native reaction/Euler and angular-history residuals must be checked before adoption. Physical-origin matching and observed galaxies remain separate from this constructive correction of the existing effective preparation.

## Exact resident inputs

| Input | SHA256 |
|---|---|
| constrained_u_galaxy_horizon_stable_y_gauss_v002.py | f70826091d11c38715c00b3a572e08c48a41252018477ac4cf3a20b2ded9f531 |
| constrained_u_clock_gradient_early_transfer_v004.py | a4e78b6467b0ba5884c8da2081ff580378b4afb839a90cec548fcf30a389fa07 |
| CONSTRAINED_U_GALAXY_HORIZON_STABLE_Y_GAUSS_V002_MANIFEST.json | 1def78ccec871fc95e9099b17ee4f05079f95804e51769b9cf3d37fb75904d94 |
| CONSTRAINED_U_STABLE_ANGULAR_RADIATION_MEMORY_CHART_V001.md | 8471e9d40bb02dca8deed6dfc2bd49e1c4d1f00cd18af456b27df5082e62b04c |
| CONSTRAINED_U_COMOVING_CURVATURE_AND_RELATIVE_VELOCITY_CHART_V002.md | 2e2102548a82167563f6a7b5ff9af558aea4d9cc85f20957daa72c777c5bdb3a |
| CONSTRAINED_U_CLOCK_GRADIENT_BBN_HELIUM_RECOMBINATION_PAIR_V002_DEFAULT_OUTPUT.json | 07e8e4e7fe524fd9d1f1a19422f293f11a49573f6ee6d1bf016b17c80ec70437 |
| CONSTRAINED_U_CLOCK_GRADIENT_BBN_HELIUM_RECOMBINATION_PAIR_V002_RECEIPT.json | 867911256634977adc8a50cdcc9b3b2e2e7aabaed6435de25c8be80acb6253fd |
| CONSTRAINED_U_FINITE_START_FORCED_ENTROPY_DIAGNOSIS_V001.md | 37a552337ca647afb06d0315271badf5c3295828aaa1b5e6675844bd479b0b39 |
| CONSTRAINED_U_FINITE_START_FORCED_ENTROPY_PERCENTAGE_ADDENDUM_V001.md | 43c117506a131004bf372f5fae68eb7b500258283e5a406352582ded936e1e9d |
