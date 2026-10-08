# k10 density, relative-current and finite angular completion V001

2026-10-06. Exclusive static continuation of the two pinned regular-jet proofs. Root, readonly and observer independently counterchecked the equations; no coefficient, background, series, source/helper, operator, matrix or trajectory is evaluated here. The prior metric reader supplies saved context only. No seed, parameter, source, failed flag or original run is changed. This is the SAME k10 post-annihilation cold/fully-ionized effective fixture, not physical parent emergence or a complete finite Cauchy certificate.

## 1. Exact current identity and the pressure background

Use all units/lower coefficients of the pinned parents: dot=d/dtau with tau=Hstar*t_proper; D=d/dlog(a) acts on coefficient polynomials. Write t=fgamma=1-r, q=q0/a, h=hr*a^-2*H, b=b3*a^-3, beta=b3/(2hr²*t), gTh=g0*a^-3 and cs=c3*a³+O(a⁶), c3=1/(qinf*Nrm*d0). The actual absolute-pressure background is

    H=1+h1*a+h2*a²+h3*a³+h4(log a)*a⁴+...,
    F=H²=1+2h1*a+F4(log a)*a⁴+O(a⁷),
    F4=2h4+2h1*h3+h2²
       =(OA/OR)*[1-logB/Nrm+3log(a)/Nrm].                (1)

The same h4 constant and logarithm must remain. Define GammaBar=t*Gamma_gamma+r*Gamma_nu, Fbar=t*p+r*N, C=cs*Gamma_phi and S=b*wb+4rho_gamma*wg/3+4rho_nu*wn/3. The correctly signed baryon Euler row and Thomson cancellation give the exact transport identity

    Sdot+3h*S=(hr²/2)*a^-4*GammaBar-hr²*a^-4*Fbar
                                      -(b+2hr²*a^-4)*C,
    S=Rdot-h*C,
    F*D(D+1)R+(DF/2)*DR=GammaBar/2-Fbar
                 +F*(D+1)C+(DF/2)*C-2C-(b3/hr²)*a*C.   (2)

Here hdot/(hr²*a^-4)=DF/2-2F. Equation(2) retains the pressure/current sources, changing weights and all background contacts; a small spatial scale is not used to remove them. The known opposite baryon-drag sign in the old source's separate diagnostics is not imported into this proof.

## 2. R5 and the linear-log R6

Let e_l be H^-1 coefficients through order4: e0=1, e1=-h1, e2=h1²-h2, e3=-h1³+2h1*h2-h3, e4=h1⁴-3h1²*h2+h2²+2h1*h3-h4(log a). Define

    Kbar_j=[H^-1*(V+t*wg+r*wn)]_j,
    Kbar5=v5+e1*v4+e2*v3+e3*v2
                      +t*(U5+e1*U4)+r*(wn5+e1*wn4),
    Kbar6=v6+e1*v5+e2*v4+e3*v3+e4*v2
          +t*(U6+e1*U5+e2*U4)+r*(wn6+e1*wn5+e2*wn4).

From GammaBar_j=4R_j-(4q0²/(3hr))*(D+j)^-1*Kbar_j, the retained curvature operator is (D+j)(D+j+1)-2=(D+j-1)(D+j+2). With the owned lower coefficients this yields

    28R5=-2q0²*Kbar5/(15hr)-Fbar5-44h1*R4+4c3*Gamma_phi2,
    (D+5)(D+8)R6=-(2q0²/(3hr))*(D+6)^-1*Kbar6-Fbar6
             -65h1*R5-(10F4+DF4)*R2+5c3*Gamma_phi3
                          +(13h1-b3/hr²)*c3*Gamma_phi2.  (3)

R5 is constant; R6 is degree at most1 in log(a). The terms 44h1,65h1 and 10F4+DF4 arise from the full weighted-current/background equation, not an assumed radiation-only model. For a linear-log RHS f0+f1*log(a), R6=r0+r1*log(a) is fixed by r1=f1/40, r0=(f0-13r1)/40. Also (D+k)^-1(u0+u1*log a)=(u0-u1/k)/k+(u1/k)*log a. These coefficient-polynomial inverses do not choose an incoming homogeneous mode.

## 3. All density contrasts through order6

Set I_j=(1/hr)*(D+j)^-1*[H^-1 V]_j for j=5,6. Define JU5=(U5-h1*U4)/(5hr), JU6=(U6-h1*U5+e2*U4)/(6hr), and Jnu5/Jnu6 by replacing U with wn. The inherited W6 and native sigma2 coefficient give

    eta6=Cbar*Qc*q0*sigma2/(6hr*w3),
    Gamma_phi5=3R5-q0²*I5,
    Gamma_phi6=3R6-q0²*I6-eta6,
    Gamma_gamma,j=4Rj-(4q0²/3)*(Ij+JUj),
    Gamma_nu,j=4Rj-(4q0²/3)*(Ij+Jnuj),                 j=5,6,
    Gamma_b5=3R5-q0²*(I5+JU5),
    Gamma_b6=3R6-q0²*(I6+JU6-W6/(6hr)).                (4)

The sigma sign follows the literal Gamma_phi source -Cbar*Q*q*sigma/w; Qc and w3 are its normalized producer quantities. Consequently Sb_gamma6=q0²*W6/(6hr), Sb_phi6=-q0²*JU6+q0²*W6/(6hr)+eta6. The reaction first changes Gamma_phi6 and does not directly feed R<=6: the pressure drivers in (3) use only Gamma_phi2/3. No lower bound on total physical current or a new charge partition follows from this coefficient statement.

## 4. Relative U,wn through order8 and the slip companions

Multiplying the exact U row by 1+beta*a gives (1+beta*a)*Udot=hU+Gamma_gamma/4-p/2-(1+beta*a)*cs*Gamma_phi. Define lower contacts

    CU5=(5h1+6beta)U6+(4h2+5beta*h1)U5+(3h3+4beta*h2)U4,
    Cnu5=5h1*wn6+4h2*wn5+3h3*wn4,
    CU6=(6h1+7beta)U7+(5h2+6beta*h1)U6
                        +(4h3+5beta*h2)U5+(3h4+4beta*h3)U4,
    Cnu6=6h1*wn7+5h2*wn6+4h3*wn5+3h4*wn4.

Then the next exact coefficient rows are

    6hr*U7=Gamma_gamma5/4-p5/2-c3*Gamma_phi2-hr*CU5,
    6hr*wn7=Gamma_nu5/4-N5/2-c3*Gamma_phi2-hr*Cnu5,
    hr*(D+7)U8=Gamma_gamma6/4-p6/2-c3*Gamma_phi3
                                       -beta*c3*Gamma_phi2-hr*CU6,
    hr*(D+7)wn8=Gamma_nu6/4-N6/2-c3*Gamma_phi3-hr*Cnu6. (5)

U7,wn7 are constant; U8,wn8 are linear-log and use the same polynomial inverse above with k=7. The beta pressure term and h4 contacts are indispensable. The W equation yields

    W7=(beta/g0)*[hr*(U5+h1*U4)+Gamma_gamma3/4-p3/2-g0*W6],
    W8=(beta/g0)*[hr*(U6+h1*U5+h2*U4)+Gamma_gamma4/4
                                      -p4/2-g0*W7-6hr*W6].

Thus wb7=U7-W7+beta*W6, wg7=U7+beta*W6; wb8=U8-W8+beta*W7-beta²*W6, wg8=U8+beta*W7-beta²*W6. All signs follow W=wg-wb and the positive baryon drag. No imposed velocity locking or entropy reset enters these equations.

## 5. Finite lmax4 angular companions and remaining scope

For the literal lmax4 hierarchy, the missing order6 companions are

    G1,6=q0*(G0,4-2G2,4)/(3g0)-5hr*G1,5/g0,
    F_gamma3,6=3q0*p4/(7g0)-5hr*F_gamma3,5/g0,
    G3,6=3q0*G2,4/(7g0)-5hr*G3,5/g0,
    J6=[3q0*N5/(7hr)-4q0*F_nu4,5/(7hr)
                                  -5h1*J5-4h2*J4-3h3*J3]/6,
    F_nu4,5=[4q0*J4/(9hr)-4h1*F_nu4,4]/5,
    F_nu4,6=[4q0*J5/(9hr)-5h1*F_nu4,5-4h2*F_nu4,4]/6. (6)

Here G1,5=q0*p3/(4g0), F_gamma3,5=3q0*p3/(7g0), G3,5=3q0*G2,3/(7g0). Photon F4/G4 begin at a7, so vanish through a6; their derivative h1 contacts also first enter these companion rows at a7. Equation(6) sets F_nu5=0 solely as the declared finite cut. An infinite hierarchy adds -5q0*F_nu5,5/(9hr) inside the last bracket, hence -5q0*F_nu5,5/(54hr) to F_nu4,6; that difference first feeds J7/N8. No exact all-angular history is certified.

Equations(3)-(6) add specific source-led jets without constructing or adopting a physical initial state. Native z7/z8/later reactions, higher Phi/V coefficients, raw pressure/Hilbert and full finite normal/shear/trace/momentum/current constraints, complete incoming history and an all-order remainder remain separate requirements. The raw phase pressure is not zero. A finite-start normal repair or agreeing coefficient residuals cannot replace those tests. No START success, nonlinear galaxy solution, fluid decoupling, microscopic birth or thermal/cosmological origin is inferred.

## Exact resident inputs

| Input | SHA256 |
|---|---|
| CONSTRAINED_U_K10_COMMON_DENSITY_AND_CURRENT_REGULAR_JETS_V001.md | dcfdf786cd6cdc80ff6182db84d4562a1b0a16150b329fcda8bc5e866fc38282 |
| CONSTRAINED_U_K10_REGULAR_METRIC_COMPLETION_V001.md | e5d638570320830f5edbdc7390af23819a930474733e6441c70f0536a2752d5f |
| constrained_u_galaxy_horizon_stable_y_gauss_v002.py | f70826091d11c38715c00b3a572e08c48a41252018477ac4cf3a20b2ded9f531 |
| CONSTRAINED_U_GALAXY_HORIZON_STABLE_Y_GAUSS_V002_MANIFEST.json | 1def78ccec871fc95e9099b17ee4f05079f95804e51769b9cf3d37fb75904d94 |
| CONSTRAINED_U_CLOCK_GRADIENT_BBN_HELIUM_RECOMBINATION_PAIR_V002_DEFAULT_OUTPUT.json | 07e8e4e7fe524fd9d1f1a19422f293f11a49573f6ee6d1bf016b17c80ec70437 |
| CONSTRAINED_U_K10_SAVED_METRIC_COMPLETION_V001_RESULT.json | 04b48d6da753c2cca3b1d95d653a0b34d1c4a8e20a0da3a93bbc1193881bfa81 |
| CONSTRAINED_U_K10_SAVED_METRIC_COMPLETION_V001_RECEIPT.json | 42b7a05641f420dea5dea06d36d03a60b485c3de32e6496b51f151e8997203d3 |
