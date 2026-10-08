# EPS5 transverse/axial causal exterior and moving ports V001

2026-10-06 UTC. AUTHOR_DRAFT=True; root and distinct FULL review required. NEW gauge/constraint reduction of the SAME uncompressed S_cross action about its owned zero-mode EPS1e-5 FLRW. No field, background, coefficient, kernel, state, numerical function or trajectory is evaluated. All32 actual positive nodes/weights and sigma=.1,1,10,100 remain conditional. No inertia, incoming state, history, physical exterior, source gain or extra energy is selected.

## 1. Gauge and physical proper-frame variables

Use c_p=1, cosmic proper time t, comoving Cartesian x and the parallel-transported spatial orthonormal frame. In the vector sector write g_ti=a S_i and h_ij=a^2[delta_ij+partial_i F_j+partial_j F_i], with div S=div F=0. Under transverse x relabeling, S changes by -a xi_dot and F by -xi. The invariant shift is B=S-a F_dot. In spatial vector gauge F=0, B=S. Define the independent-U tilt by U_i=a u_i, div u=0; it is invariant and is not ordinary u_M. Each z_j is a projected proper-frame transverse covector. The unit/transverse reactions are varied before reduction.

Retain M^2=(8pi Gbare)^-1, KB=.02, C=1.98, g=M^2 C and the actual background H,Q=phibar_dot,nbar=P_X(Q), a^3 nbar=I0 and Q_dot=-3H c_s^2 Q. The unchanged background satisfies the full P(X)/ordinary Friedmann equations, including actual ordinary pressure. The32 omega_j=sigma xi_j Hstar are proper constants of the declared benchmark, not sigma xi_j H(t). Keep the actual binary weights w_j and their sum without renormalization.

Let D=a^-1 partial_x, K_T=curl curl=-Delta on a transverse field, Z=sum_j w_j z_j and A=u_dot+H u. Direct quadratic variation gives

    L_T^(2)/a^3=M^2 KB[A^2-u.K_T u]/2-g Q^2 u^2/2
       +g sum_j w_j[z_dot_j^2/omega_j^2-z_j^2-ell^2|D z_j|^2]/2
       +g A.Z.                                             (1)

The u.K_T u expression denotes the bulk curl energy with its ACTUAL boundary term retained. Projected nabla_n z_j has proper component z_dot_j, not z_dot_j+H z_j; its spatial projected output removes the background normal connection. Thus no H^2 z_j^2 is appended. In contrast F_n,hat i=A_i contains H u. This distinction follows from the physical coframe, not frozen coordinate components. The quartic derivative vanishes at zbar=0 only; the finite interior action keeps it.

## 2. Retained causal state and vector Einstein constraints

Define P=M^2 KB A+g Z. For each transverse polarization and each of the four sigma arms the exact reduced material rows are

    u_dot=(P-g Z)/(M^2 KB)-H u,
    P_dot=-2H P-(M^2 KB K_T+g Q^2)u,
    z_dot_j=v_j,
    v_dot_j=-3H v_j-omega_j^2(1+ell^2 K_T)z_j+omega_j^2 A.    (2)

This is66 fields per polarization: u,P and32 positions plus32 velocities. All proper temporal and spatial factors remain. In ordinary seconds, set u_SI=c_p u, z_acc=c_p^2 z, P_acc=c_p^2 P, H_SI=c_p H, Q_SI=c_p Q and omega_SI=c_p omega_geom. Then A_acc=u_SI,dot+H_SI u_SI, and the P equation has (M^2 KB c_p^2 K_T+g Q_SI^2)u_SI. The modal equation retains ell^2 K_T. Equivalently use length unit L0 and geometric time c_p t_SI/L0, omega_*=sigma xi_j eta with eta=HstarSI L0/c_p, ell_*=ell/L0. Do not insert another factor1000 in the owned Hunit-to-eta conversion.

Let j_o be the ordinary momentum measured by the ADM normal and Pi_o,ij^V its transverse spatial stress. The independent rotating material/ordinary kinetic equations determine these; neither SFR nor a scalar phase normal supplies them. The EH vector quadratic form is a^3 M^2(D B)^2/4 modulo its boundary term. At held coordinate U components its shift variation also contains the native Euler residual

    E_u=-[P_dot+2H P+(M^2 KB K_T+g Q^2)u],
    M^2 K_T B/2+E_u+j_o=0.                                (3)

After the retained U/mode/reaction rows, the gauge-reduced Einstein vector system is

    K_T B=-2j_o/M^2,
    -M^2 D_(i(B_dot+2H B)_j)=Pi_o,ij^V,
    j_o,dot+4H j_o+D^j Pi_o,ij^V=0.                         (4)

Parentheses mean symmetrization with1/2. Since K_T,dot=-2H K_T in comoving variables, the last two rows propagate the first constraint. No q^-2 division is used on its kernel. Native/phase linear transverse Hilbert momentum vanishes ONLY on these Euler/reaction rows about Fbar=zbar=rbar=0; it is not zero off shell or in the nonlinear galaxy. Its transverse phase current -g Q u is divergence-free, not a new phase-charge source. Ordinary pressure/stress and background metric contacts are retained in (4). No extra vector metric propagation mode is invented; TT/scalar sectors remain their separate equations.

## 3. Axial multipoles and genuine moving conormal momenta

For a normalized divergence-free toroidal vector harmonic X_lm on flat spatial slices, l>=1, write its proper components as u_lm(t,R)X_lm and similarly z_j. Here R=a r is physical radius, not a chosen galaxy boundary. Define

    D_t=partial_t|R+H R partial_R,
    K_l f=-f_RR-2f_R/R+l(l+1)f/R^2.                        (5)

Replace the dots in(2),(4) by D_t and K_T by K_l. The first-order state is identical, with partial_t f=D_t f-HR f_R. The exact background coframe gives U_A=R u X_A,

    F_R,hat A=u_R+u/R, F_n,hat A=D_t u+H u=A,
    (D z_j)_R,hat A=z_j,R, (T z_j)_hat A=D_t z_j.           (6)

For the actual tube R=Rb(t), Vb=Rb_dot-H Rb, |Vb|<1, gamma_b=(1-Vb^2)^-1/2 and outward s=gamma_b(Vb n+e_R), contraction of the literal junction momenta yields

    p_U=s.Pi_U=-gamma_b[M^2 KB(u_R+u/R)+Vb P],
    p_zj=s.Pi_zj=-g w_j gamma_b[Vb D_t z_j/omega_j^2
                                                    +ell^2 z_j,R].       (7)

These are physical proper-frame coefficients multiplying X_lm; no midpoint or scalar-Neumann replacement is made. In particular a fixed proper-radius tube has Vb=-H Rb and temporal flux. The metric vector spatial constraint port is M^2 n^i D_(i B_j); its radial tangential component is M^2(B_R-B/R)/2. This spatial port is NOT the whole timelike EH junction: match the actual induced metric/extrinsic curvature and material connection ports on that same moving tube. The background phase flux -gamma_b nbar Vb remains even when the axial perturbation carries no radial phase charge. Regular gauge kernels and the rotational-frame/angular-momentum homogeneous solutions need their actual registration, not an arbitrary inverse or zero wall.

## 4. Inclusive quadratic work and a small causal exterior operator

With p=P/M^2 and L=l(l+1), define radial harmonic energy/flux per M^2, after angular integration with the stated normalization,

    e=KB[A^2+(u_R+u/R)^2+L u^2/R^2]/2+C Q^2 u^2/2
       +C sum_j w_j[v_j^2/omega_j^2+z_j^2
                              +ell^2(z_j,R^2+L z_j^2/R^2)]/2,
    F=KB A(u_R+u/R)+C ell^2 sum_j w_j v_j z_j,R,
    D_t e-R^-2 partial_R(R^2 F)=W_bg,
    W_bg=-2H A p-2H KB[(u_R+u/R)^2+L u^2/R^2]
       +C(Q Q_dot-H Q^2)u^2-3H C sum_j w_j v_j^2/omega_j^2
       -H C ell^2 sum_j w_j(z_j,R^2+L z_j^2/R^2).           (8)

The acceleration-mode powers cancel inclusively; in particular -2H A p retains its Z contact. W_bg is work with the retained evolving background, not newly assigned birth energy. For a moving radial volume its energy derivative additionally has volume work3H e and surface Rb^2(Vb e+F). This is the quadratic material ledger; the complete background/ordinary/Einstein normal source is not replaced by e.

An actual exterior discretization of(2)-(7), with the ordinary current/stress, has a retained66-field material state per axial harmonic and the constrained metric block. Its boundary-to-momentum map has the form p_Sigma(t)=p_initial(t)+D_sigma(t)b(t)+integral_ti^t K_sigma(t,s)b(s)ds plus the actual ordinary-source-history term. D,K are the variational evolution/trace operator of THESE equations, not adjustable kernels. Use the DAE/constraint-compatible propagator for(4), and keep the actual boundary lifting, motion and ports(7). Prescribing both metric traces and their extrinsic momenta arbitrarily would overdetermine the system.

The no-independent-incoming branch sets only the independent homogeneous exterior perturbation data to its declared retarded value; it does not reset transported inner states, truncate earlier history, or prove a physical initial preparation. At high proper frequency the transverse Maxwell/U principal channel is lightlike and the isolated native branches have ell omega_j; lower-order coupling and Q give the actual mixed dispersion. This is the zero-mode transverse reduction, not the full nonzero-field phase/U/Einstein characteristic theorem.

The existing coefficients suffice to DEFINE this conditional operator without a birth gain or identifying U=u_M. Its numerical evaluation still requires actual boundary/ordinary histories, gauge and exterior domain, and incoming state. Activity support0.3–15.1kpc remains unknown outside that measurement; neither baryons out to44.08kpc nor the128kpc computation are truncated or joined to homogeneous FLRW there. A full rotating galaxy also retains scalar/TT/normal rows, nonlinear interior, the physical inertia/graph-to-field matching and exact full-metric geodesic/observer readout. None is qualified by this derivation.

## Actual input seals

These complete actual bytes were checked before and after exclusive creation; no input was modified or executed. Paths are relative to J.

| Input | SHA256 |
|---|---|
| INVARIANT_CLOCK_GRADIENT_SHARED_ACTION_BUDGET_DOMAIN_AND_NORMAL_V003.md | e08b7166892ec59c863539d59b8d4b89c654081776d8870239ecc2c382572da0 |
| CROSS_U_EPS5_FLRW_GALAXY_JUNCTION_V001.md | baa25990f0b2d4ca925e1a74fb65b40c2968890bd552e9f64541e620e07c6965 |
| CROSS_U_NATIVE_CHARACTERISTIC_SPEED_AND_COUPLED_TRANSPORT_V001.md | 200024fb6cc378bf81f27c93838057239ad63eaba3d5e5306076114505496597 |
| CROSS_U_EPS5_LINEAR_EXTERIOR_PHASE_NATIVE_AND_METRIC_MATCHING_V001.md | a7fc7786b42fa46ca5ec268eaba5ee2e581f3ebcdb48bffb83e8cfc6a5ef54d4 |
| CROSS_U_FULL_FLRW_SOURCE_CONSTRAINT_AND_FINITE_SLICE_TEST_V001.md | c81fa7ed6961f5f0620bbb48dd133ef474543765131ceb738bdcf676f9b9a986 |
| NATIVE_ROTATING_MATERIAL_CLOCK_SOURCE_EXTENSION_V001.md | e8911d59ae25f9d397a57a6dcd6d0ca5c450df82566935c00f8436568f7484ff |
