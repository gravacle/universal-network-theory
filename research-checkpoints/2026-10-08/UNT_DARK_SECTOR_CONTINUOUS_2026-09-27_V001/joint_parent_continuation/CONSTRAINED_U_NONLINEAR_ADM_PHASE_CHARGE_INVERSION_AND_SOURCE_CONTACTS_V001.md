# Nonlinear ADM phase-charge inversion and complete-source boundary V001

2026-10-06 UTC. Root-requested STATIC theorem for the owned positive bounded-pressure branch and constrained action. No state, coefficient, operator, source helper, inversion or trajectory is evaluated. Existing parameters, absolute energy, clocks, microscopic/macroscopic preparations and every failed flag remain unchanged. Signature(-+++), c_p=1; physical charges and stresses are used, not normalized weak-row w.

## Exact global constituent chart

Set Nrm=1/eps-ln(1+1/eps)>0, q(s)=sqrt(1+eps*s/(1+s)), X=Q0*q(s), n=P_X=K*s*q(s), K=2A/(Q0*eps*Nrm)>0, s>=0. Then X(n) is unique on Q0<=X<Qcap=Q0*sqrt(1+eps), with n in[0,infinity). This selected branch, not an extension of P to another phase domain, is the theorem's premise.
    c_s²=n X_n/X=s q_s/(q+s q_s)
        =eps*s/[2+(4+3eps)s+2(1+eps)s²] in[0,1),
    c_s²<=c*=eps/[4+3eps+4sqrt(1+eps)].                                     (1)
The maximum follows from 2/s+2(1+eps)s>=4sqrt(1+eps); c_s²=0 at n=0 and tends to0 as n→infinity. No transcendental approximation or evaluated constant is used.

For positive ADM lapse N and positive spatial metric gamma, hold p_i=partial_i phi, p²=gamma^(ij)p_i p_j finite, geometry, U and the projected reaction fixed. In the pinned normalization g_sigma=M²C=C_m Kb_mode and sigma=P_U sigma_phys/C_m. Define
    Gamma=sqrt(1+p²/X(n)²), F(n)=n Gamma,
    qtilde=Pi_phi/sqrt(gamma)+g_sigma N sigma^t,
    phi_dot=beta^i p_i+N X(n)Gamma.                                          (2)
The FULL canonical Noether density is Pi_phi/sqrt(gamma)=qtilde-g_sigma N sigma^t. It is not the constituent qtilde or bare n.
    F'(n)=[1+(1-c_s²)p²/X²]/Gamma>0,
    1/Gamma0<=F'(n)<=Gamma0, Gamma0=sqrt(1+p²/Q0²).                           (3)
F is continuous from0 toinfinity, so every finite qtilde>0 has exactly one finite n>0. An explicit global bracket is qtilde/Gamma0<=n<=qtilde/Gammacap, Gammacap=sqrt(1+p²/Qcap²). At p=0, n=qtilde. At qtilde=0, the selected boundary is n=0,X=Q0; negative qtilde has no solution on this future branch. A reaction can give nonzero Pi_phi at that boundary. Neither full-current timelikeness nor coupled constraint solvability follows.

## Exact finite tilt energy and stress at fixed qtilde

Write lambda=p², Y=sqrt(X(n(lambda))²+lambda), and retain P(Q0)=-A. The bare pressure-constituent normal energy is rho_P=qtilde*Y-P(X), with rho_P(0)=e_req(qtilde), e_req(n)=nX-P and e_req(0)=A. Because n=qtilde*X/Y, all X_n*n_lambda terms cancel:
    partial_lambda rho_P=qtilde/(2Y)=n/(2X)>0.                              (4)
Consequently, with Delta rho_P=rho_P(p)-rho_P(0),
    qtilde[sqrt(Qcap²+p²)-Qcap]<=Delta rho_P
       <=qtilde[sqrt(Q0²+p²)-Q0]<=qtilde*p²/(2Q0).                           (5)
There is no inverse chemical-gap factor Qcap-X. This is a held-charge/reaction constituent completion, not an evaluated correction to any saved state or total gravitational energy bound.
    -partial_lambda P/partial_lambda rho_P
          =c_s² X²/[X²+(1-c_s²)lambda]<=c*,
    0<=P(qtilde)-P(n(p))<=c*Delta rho_P,
    j_P,i=-qtilde p_i, S_P,ij=qtilde p_i p_j/Y+P gamma_ij.                   (6)
Here P(qtilde) means P(X(n=qtilde)) at p=0. The nonisotropic streaming stress is retained. The gradient-energy Hessian at fixed qtilde is (qtilde/Y)[gamma^(ij)-(1-c_s²)p^i p^j/(X²+(1-c_s²)lambda)]; its transverse and longitudinal eigenvalues in an orthonormal frame are qtilde/Y and qtilde X²/[Y(X²+(1-c_s²)lambda)], both positive. This is not a Gibbs, perfect-fluid or full-action stability theorem.

## Reaction, Hamiltonian and normal contacts still required

For the HELD-variable phase portion L_phi=N sqrt(gamma)[P(X)-g_sigma sigma^mu partial_mu phi], its exact canonical momentum is (2) and its partial Legendre transform is
    H_phi=N sqrt(gamma)rho_P+beta^i Pi_phi p_i
                +N sqrt(gamma)g_sigma(sigma^i+beta^i sigma^t)p_i.             (7)
The full constraint also contains +C_m sigma.B in the action, giving -N sqrt(gamma)C_m sigma.B in this held Hamiltonian allocation. The owned C_m a.B vertex, mode/vector mixed momenta, unit/vector reactions, gradients and boundaries remain. Setting B=Kb_mode P_U dphi or making the multiplier action zero on shell does not erase its metric/U/current derivatives or justify identifying rho_P with the complete Hilbert normal source.
For an arbitrary source variation at this constituent chart,
    delta n=[delta qtilde-n delta(p²)/(2Gamma X²)]/F'(n),
    delta qtilde=delta(Pi_phi/sqrt(gamma))+g_sigma delta(N sigma^t),
    delta[X Gamma]=(X_n/Gamma)delta n+delta(p²)/(2X Gamma).                   (8)
Volume/metric/shift and the actual physical-multiplier projection must be differentiated, including delta(P_U), not silently held after eliminating the reaction. Sigma determined by a coupled normal/modal system is not an independently fixed function of n, so (3) alone is not a monotonicity theorem for that coupled solve.
A full ADM state additionally requires unit-U and transverse-mode constraints, B=Kb_mode r and its first jet, actual mode/U momenta and Euler equations, total phase charge continuity, and the Einstein lapse/shift constraints using the COMPLETE once-only Hilbert stress and sources. Ordinary species/Maxwell/support/material-map contacts and admitted boundary data remain. No Einstein, modal or material equation is replaced by this inversion; no pressure reference is reset.

The running macroscopic continuation uses a supplied post-annihilation effective background/ordinary inventory and derived finite regular jets. The separate native photon-onset t^4 correlation result is a microscopic mechanism, not the joint density matrix, charge/volume/stress registration or controlled memory reduction for that macroscopic preparation. Existing deterministic phase/reactive contacts already remain in the macro action. This theorem neither derives microscopic origin nor inserts a chi source, temperature, late fraction or new EOS.

## Exact bytes, checked before and after exclusive creation

| Input relative to J | SHA256 |
|---|---|
| NATIVE_LOCAL_PROPER_MATERIAL_NORMAL_AND_PHASE_SOURCE_MATCHING_V001.md | 40978c4874ea478c1ce03c7bfcaee0e8304f8bd1c80aebf0742282266209b64b |
| NATIVE_CARRIER_LINK_PHOTON_UNIFIED_CURRENT_MATCHING_V001.md | 7b215502059b680391554346d6adc8d4c74138819ddaf6f4bc69755f9d406ecf |
| NATIVE_CARRIER_LINK_PHOTON_UNIFIED_CURRENT_MATCHING_UNITS_ADDENDUM_V001.md | 80c26b94eb4a2d310a8742cd88474d39c50c3a47e390cfe46ea125aa0ad58f6e |
| INVARIANT_CLOCK_GRADIENT_SHARED_ACTION_BUDGET_DOMAIN_AND_NORMAL_V003.md | e08b7166892ec59c863539d59b8d4b89c654081776d8870239ecc2c382572da0 |
| NATIVE_UNIFIED_PARENT_PHOTON_ONSET_AND_MEANFIELD_DISCRIMINATOR_V001.md | 8185f9d938c328731d5ff8caaf0597ea7a8844d5fbf37450e8c2a75b854d7f6a |
| constrained_u_k10_derived_full_common_continuation_v001.py | 90125e5ee7773dab985b3c3d9f26aafff4e56651752aed4fe733a582edf291d3 |
| CONSTRAINED_U_K10_DERIVED_FULL_COMMON_CONTINUATION_V001.md | eed23fb57ed87d5c245283d01ba6ba34f7837c9ce2b3e3206e1c8e73c9ffcfb3 |
