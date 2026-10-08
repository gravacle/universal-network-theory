# Explicit same-action spherical ADM sources and canonical evolution V001

2026-10-06 UTC. STATIC continuation of the protected 78-line spherical S_dual reduction. No field/operator/helper, coefficient, matrix, state, inversion or trajectory is evaluated; no action or physical input is changed. These elementary jet formulas remove the unspecified functional-stress step from that reduction. Signature(-+++), c_p=1, per factored4pi; primes mean radial coordinate derivatives. Centre formulas use their smooth weighted limits rather than division at R=0.

## 1. The existing nonlinear calibration has a normalized chart

Retain z_delta=delta*f_delta, xi=delta/Lambda>0 and normalized positive weights w(delta)=nu(delta)/integral nu. The owned nu=A_mode*delta gives w ddelta=2xi dxi before finite quadrature. The existing physical-potential combination is gc²=kappa*Lambda^4/u4, with the inherited effective gc=3pi*a0/8 and geometric a0=a0_SI/c_p². Therefore u4/(kappa*delta^4)=1/(gc²*xi^4). Together with C_m Kb_mode=M²C and omega_delta²=kappa*delta²/m_delta, the unchanged constituent action becomes
    L_D=M²KB A_U²/2+P(X)
       +M²C sum_or_integral w[(Uz)²/(2omega²)-z²/2-z^4/(4gc²xi^4)
              -ell²((Ez)²+2z²b_R²)/2+A_U*z]
       +g_sigma*sigma(Z-p), Z=sum_or_integral w*z, g_sigma=M²C.          (1)
This normalized quartic is already fixed by the retained proper potential/amplitude registration; it is not a new quartic choice. That static calibration fixes neither the separate kappa,A_mode,Lambda nor omega(delta), which belongs to the independently declared temporal spectrum. A finite regulator retains its actual positive nodes/weights and all modes. The old source prefactor2M²/Kb is not copied: current C_m=M²C/Kb uses one Gbare=.99GN. Keeping gc does not transfer an old force fit through the new phase constraint. The early quadratic omega/weights alone would not determine gc, but the resident nonlinear spatial calibration supplies this combination as an effective input without a microscopic-origin prerequisite. No radius-dependent calibration or new phase abundance is introduced.

## 2. Elementary ADM jets and material momenta

Use ds²=-N²dt²+L²(dr+beta dt)²+R²dOmega², c=cosh(chi), s=sinh(chi). For any scalar psi write q_psi=(psi_dot-beta*psi')/N, p_psi=psi'/L; these p_psi are SPATIAL JETS, not canonical momenta. Define
    a_n=N'/(NL), k_L=[L_dot-(beta*L)']/(NL), k_R=q_R/R,
    Upsi=c*q_psi+s*p_psi, Epsi=s*q_psi+c*p_psi,
    A_U=c(q_chi+a_n)+s(p_chi+k_L),
    a_R=(c*q_R+s*p_R)/R, b_R=(s*q_R+c*p_R)/R,
    Q=Uphi, p=Ephi, X=sqrt(q_phi²-p_phi²), n=P_X,
    T=M²KB A_U+g_sigma Z, G=g_sigma*ell²*sum w*z², E_b=-2G*b_R.          (2)
For finite nodes define u_j=Uz_j, e_j=Ez_j, and the exact material jet derivatives
    A_phi=n*q_phi/X-g_sigma*sigma*s, B_phi=-n*p_phi/X-g_sigma*sigma*c,
    A_j=g_sigma*w_j[(c/omega_j²)*u_j-ell²*s*e_j],
    B_j=g_sigma*w_j[(s/omega_j²)*u_j-ell²*c*e_j].                       (3)
Canonical material momenta are Pi_phi=LR²*A_phi, Pi_j=LR²*A_j, Pi_chi=LR²*c*T. The metric receives the compulsory mixed momenta
    P_L=P_L^g+R²*s*T, P_R=P_R^g+LR*s*E_b,
    P_L^g=-2M²R²*k_R, P_R^g=-2M²LR(k_L+k_R).                          (4)
N,beta,sigma have zero momenta. Omitting either metric shift in (4) loses the acceleration or angular-vector-gradient contact. The full conserved phase density is Pi_phi/(LR²); the shifted constituent density is A_phi+g_sigma*sigma*s=n*q_phi/X.

## 3. Explicit complete ADM energy, flux and pressures

Let L_D denote the full material density (1), including its multiplier before on-shell substitution. Direct variations of lnN, beta, lnL and lnR at held chi/z/phi give
    F_N=-n*q_phi²/X-T(c*q_chi+s*k_L)
       +sum_j g_sigma*w_j[-(c/omega_j²)*u_j*q_j+ell²*s*e_j*q_j
                              +2ell²*z_j²*b_R*s*q_R/R]
       +g_sigma*sigma*s*q_phi,
    F_L=n*p_phi²/X-T(c*a_n+s*p_chi)
       +sum_j g_sigma*w_j[-(s/omega_j²)*u_j*p_j+ell²*c*e_j*p_j
                              +2ell²*z_j²*b_R*c*p_R/R]
       +g_sigma*sigma*c*p_phi.                                        (5)
The complete once-only source projections on the ADM normal/radial unit are
    rho=-L_D-F_N+[partial_r(NR²*c*T)]/(NLR²),
    j_e=-A_phi*p_phi-sum_j A_j*p_j-s*E_b*p_R/R
                              +s[e(T)+2(p_R/R)*T],
    p_r=L_D+F_L-[partial_t(LR²*s*T)-partial_r(beta*LR²*s*T)]/(NLR²),
    p_perp=L_D-Div_R(E*E_b)/2=L_D+Div_R(E*G*b_R).                       (6)
Here e(T)=T'/L and Div_R is the weighted two-divergence of the preceding proof. The source convention is j_e=-T_mu_nu n_ADM^mu e^nu. Ordinary species add their actual rho,j,p_r,p_perp once. The time derivatives in (6) are the mixed canonical contacts, not a new EOS: the first-order equations below supply them. In the flat, static, aligned limit these mode pressures reproduce p_r=-V+J f'^2/2+J f²/R² and p_perp=-V+kappa*delta*A_U*f+J(2ff'/R-f'^2/2), summed with the original weights/prefactor. This independent limit checks the angular connection rather than discarding it.

## 4. An explicit first-order constrained canonical system

Recover k_R from P_L^g in (4), then b_R and E_b, subtract the material P_R term and recover k_L. T=Pi_chi/(LR²*c), A_U=(T-g_sigma Z)/(M²KB), so
    q_R=R*k_R, L_dot=(beta*L)'+NL*k_L,
    q_chi=[A_U-s(p_chi+k_L)]/c-a_n,
    q_j=[Pi_j/(g_sigma*w_j*LR²)
                  -(1/omega_j²-ell²)*s*c*p_j]/[c²/omega_j²-ell²*s²].   (7)
The mode denominator must be nonzero on the declared noncharacteristic slice; its positivity is a sufficient local Legendre condition, not full coupled hyperbolicity. The phase q_phi is obtained from the owned positive shifted-charge constituent chart at HELD sigma, without changing its domain. The constraint Z=s*q_phi+c*p_phi and its preservation determine sigma jointly with the actual state; keep these equations undivided at s=0. This is not a proof of a globally monotone nonlinear reaction inverse or permission to pick sigma.
Every scalar position evolves psi_dot=beta*psi'+N*q_psi. Define V_j'=z_j+z_j³/(gc²*xi_j^4), and K_U=s(q_chi+a_n)+c(p_chi+k_L). The material momentum equations contain only explicit jets:
    Pi_phi_dot=partial_r(beta*Pi_phi-NR²*B_phi),
    Pi_j_dot=partial_r(beta*Pi_j-NR²*B_j)
       +NLR²*g_sigma*w_j[-V_j'-2ell²*z_j*b_R²+A_U+sigma],
    Pi_chi_dot=partial_r(beta*Pi_chi-NR²*s*T)
       +NLR²{T*K_U+sum_j g_sigma*w_j(1/omega_j²-ell²)*u_j*e_j
                         -2G*a_R*b_R-g_sigma*sigma*Q}.                 (8)
With k_R,k_L and EH-only momenta from (4), the COMPLETE metric momentum equations are
    P_L_dot=beta*P_L' -N(P_L^g)²/(4M²R²)
       +M²N(1-R'^2/L²)-2M²N'RR'/L²
       +NR²(L_D+F_L)-N*k_L*R²*s*T,
    P_R_dot=partial_r(beta*P_R)
       +N[L(P_L^g)²/(2M²R³)-P_L^g*P_R^g/(2M²R²)]
       +2M²N'R'/L-2M²*partial_r[(NR'+N'R)/L]
       +2NLR*L_D-N*k_R*LR*s*E_b-partial_r(NR²*c*E_b)/R.               (9)
These rows follow by combining EH evolution with (6) and converting to the TOTAL momenta (4); no functional derivative of an unknown stress remains. Gauge lapse/shift choices follow after their equations and must preserve centre/exterior matching, not fix U or phase velocities independently.
For clarity define rho_0=-L_D+A_phi*q_phi+sum_j A_j*q_j+T(A_U-s*p_chi)+s*E_b*q_R/R. Then the lapse derivative contacts cancel explicitly to give the canonical form rho=rho_0+(R²*c*T)'/(LR²). The two independent gravitational constraints are
    H_g+LR²*rho=0,
    H_r=P_R R'-L P_L'+Pi_chi chi'+Pi_phi phi'+sum_j Pi_j z_j'=0,
    H_g=L(P_L^g)²/(4M²R²)-P_L^g P_R^g/(2M²R)
                           -(M²/2)LR²*(3-curvature).                   (10)
The curvature is 2/R²[1-R'^2/L²-2R(R'/L)'/L]. Ordinary canonical terms/sources are included in both constraints. Equivalently H_r^g-L²R²*j_e=0; this independently checks the shift/source sign. Retain the EH radial boundary term or integrate its curvature density into -M²[NL+NR'^2/L+2N'RR'/L] with the same endpoint term. The latter involves only first spatial jets and makes each canonical row elementary local differentiation.

## 5. Implementation scope

Equations (7)-(10), baryon/ordinary transport, the undivided multiplier consistency and inherited FLRW incoming data give a finite-regulator first-order DAE/PDE to implement. Test charged FLRW, total-current flux, both geometric constraints, exact radial Ward/angular work and the owned quadratic all-mode limit before a nonlinear compensated source. Regular-centre and noncharacteristic conditions are those of the protected reduction. The characteristic/constraint solve must report singular or incompatible branches rather than insert an unowned inverse, damping, reflected halo or fitted phase profile. No scientific solve, pressure-reference shift, new preparation, microscopic chi-to-fluid map or observed galaxy result follows from this static system.

## Protected actual inputs

| Input relative to J | SHA256 |
|---|---|
| CONSTRAINED_U_SPHERICAL_FLRW_CURRENT_MODE_AND_HILBERT_SYSTEM_V001.md | 110b2f23ae79c808090f79c60655b7c64c7b38e2edd7773e6aa4965ed4e399b1 |
| INVARIANT_CLOCK_GRADIENT_SHARED_ACTION_BUDGET_DOMAIN_AND_NORMAL_V003.md | e08b7166892ec59c863539d59b8d4b89c654081776d8870239ecc2c382572da0 |
| CONSTRAINED_U_NONLINEAR_ADM_PHASE_CHARGE_INVERSION_AND_SOURCE_CONTACTS_V001.md | c5cf5f19f6a7333d4f807a771bf7033b694924b28f5624980c5050fd8b7d5b82 |
| SPHERICAL_GRADIENT_COMMON_LENSING_CLOSURE_V001.md | a4221d6ed0d5b0fed266e9fc8e27fa190b3f911e39cc7d218912418d1cc69b57 |
| CONSTRAINED_U_GALAXY_WORLDTUBE_AND_STATIC_BOUNDARY_DISCRIMINATOR_V002.md | a7598cc79c7e3bdaa83ad31f32826e7cf439b0f28c6f79fda9a09ea98c5ab90b |
