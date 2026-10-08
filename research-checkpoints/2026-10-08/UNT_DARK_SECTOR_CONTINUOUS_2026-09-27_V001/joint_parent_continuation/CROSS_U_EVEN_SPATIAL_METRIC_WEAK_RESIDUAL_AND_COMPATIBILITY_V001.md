# S_cross remaining even spatial metric: weak residual and compatibility V001

2026-10-06 UTC. AUTHOR_DRAFT=True; guarded analytical companion pending full root/peer review. New static hand derivation; no source/operator/field/kernel has been evaluated. It defines a conditional operator and finite-field tests, not a physically completed constitutive or normalization match. Native graph-to-physical mapping, temporal inertias, source preparation and exterior remain unregistered. All four already declared sigma=.1,1,10,100 and the same fixed stellar/gas/clock/source inventory are preserved; no source, EOS, unit, inertia, boundary or force is fitted.

## 1. Remaining exact geometry in the inherited circular sector

Use c_p=1, signature -+++, and the accepted +beta convention:

    ds^2=-N^2dt^2+h_AB dx^A dx^B+rho^2(dphi+beta dt)^2,
    n=N^-1(partial_t-beta partial_phi), e=rho^-1 partial_phi,
    t_A=(rho/N)D_A beta, K_A,hatphi=-t_A/2, K=0.

A,B are meridional; D_2 and R_2 belong to h_AB. This is the existing stationary circular benchmark, not a theorem that every native rotating state is circular. Its unretained meridional momentum/mixed angular rows remain compatibility conditions.

    R_3=R_2-2rho^-1 D_2^2rho,
    R^(4)_AB=R^(2)_AB-(D_A D_Brho)/rho-(D_A D_BN)/N+t_A t_B/2,
    R^(4)_phiphi/rho^2=-D_2^2rho/rho-Dlnrho.DlnN-|t|^2/2.      (1)

The spatial Ricci sources are [S_ij+h_ij(E-S)/2]/M^2, E=T_nn and S=h^ij S_ij. Independent normal and lapse/trace rows are

    R_3/2-|t|^2/4=E/M^2,
    Delta_3N/N=|t|^2/2+(E+S)/(2M^2).                         (2)

The signs in (1),(2) follow the accepted K convention; the axial spacelike reduction gives opposite shift signs in meridional and angular Ricci. Holding Psi=Phi cannot supply these remaining rows.

## 2. First-derivative gravity and native tensor ports

After the actual Einstein boundary term, the exact stationary gravitational action per azimuth is

    S_EH=(M^2/2)integral dt sqrt(h_2)
       [N rho R_2+2 DN.Drho+N rho |t|^2/2].                   (3)

Vary h_AB and rho INDEPENDENTLY, with N,beta,chi and native variables held as declared before source/equation elimination. Equivalently use ADM N sqrt(h)(R_3+K_ijK^ij)/2. Compactly supported metric tests remove an unchosen outer metric traction, not the genuine sheet/internal contacts. Curvature weak forms must retain the Einstein boundary reduction; pointwise cell Hessians omit Q1 derivative jumps.

For zero shift/aligned U, the held-covector material action and tensor are exactly Hilbert106 Eq(1),(2), including P, both inverse metrics of |Dz|^2 and its connection. Put C_j,ij=D_(i z_j,j) and

    F^k_ij=sum_j w_j[z_j^k C_j,ij-2z_j,(i C_j,j)^k].

For a symmetric metric test q_ij, q^ij=h^ik h^jl q_kl, the connection improvement is

    integral N sqrt(h) T_improvement,ij q^ij
      =-g ell^2 integral N sqrt(h) F^k_ij D_k q^ij
         +g ell^2 integral_boundary N n_k F^k_ij q^ij.         (4)

Add the literal algebraic Hilbert tensor, not two scalar-gradient surrogates. Cylindrical angular connection, sheet reflection, axis regularity, Q1 jumps and outer ports remain. A global weak derivative includes interior jumps; do not append duplicate deltas. At retained odd order add the metric variation of the ENTIRE accepted L_2, including Einstein shift, Maxwell magnetic gradient, relative phase, inertias and mode angular contacts. All four frequencies are benchmarks, not matched microscopic frequencies.

## 3. Off-shell frame and variable bookkeeping

The uncompressed parent varies independent U, modes, phase and metric with their constraints. Parametrizing U=cosh(chi)n+sinh(chi)e solves its normalization, but a restricted metric derivative also moves U. Recover the unit reaction from the longitudinal U equation; retain its stress. A pullback metric derivative is Hilbert only after its projected-U/modal chain terms are accounted for, not by declaring the saved fields on shell.

At held chi, with c=cosh(chi),s=sinh(chi), the projected frame changes are

    (delta U)_E=cs delta lnN-cs delta lnrho
                    -c^2(rho/N)delta beta.                   (5)

Thus the weak reduced metric variation contains E_chi times (5). Subtract this chain to isolate the normalized-U Hilbert row. For the accepted quadratic odd truncation use cs=chi and c^2=1 at the relevant order; higher odd powers are not silently certified. Equivalently include delta chi=-chi delta lnN+chi delta lnrho+(rho/N)delta beta in a compensated derivative and retain the uncompensated projected-U test separately.

Held covectors also differ off shell from held contravariant native vectors. If z_i=h_ij y^j, a metric test q at held y gives delta z_i=q_ij y^j. Hence

    delta S_metric|y=delta S_metric|z+delta S_z[q.y].          (6)

The modal weak Euler term in (6) vanishes only when that full mode row and its ports hold. Save raw covector variation, modal chain and U chain separately. No mode minimum, normal reaction or physical phase flux is inferred from a lapse residual or from a passed odd linear solve. The SAME phase remains phi=omega t, X=omega/N, with its full P family evaluated BEFORE any background subtraction.

## 4. Fixed material labels and normalization

Use the already admitted fixed rest mass dM0=Sigma_input R dR dphi. D_Sigma sqrt(H_sheet)=R Sigma_input, b_v=v_ZAMO/c_p, Gamma=(1-b_v^2)^-1/2. Proper sources are

    E=D_Sigma c_p^2 Gamma delta(l_Z),
    j_hatphi=E b_v, S_hatphi_hatphi=E b_v^2,
    S_hatRhatR=S_hatZhatZ=0.                                 (7)

Vary the minimally coupled worldline action -dM0 c_p^2 integral d tau at held labels and coordinate Omega, THEN impose the predicted circular condition. Substituting Omega(h) before variation adds an unowned angular-momentum chain. Reflection/junction supplies the normal sheet meaning. No Vobs is a source, no direct native force is appended, and E and S are not a second baryon inventory.

Restore g_energy=c_p^4/(4pi G_N)=M^2 C, C=1.98, M^2=g_energy/C, B0=a0 L0/c_p^2. With x*=x/L0, z*=L0 z and Ehat=L0^2 E/g_energy, the Ricci source is C[Shat_ij+h_ij(Ehat-Shat)/2]; no extra .99 factor. The upper-half azimuth-factored angular test lambda=delta lnrho has source B0 times the OLD scalar annular integrand times N Gamma b_v^2 lambda INSIDE the same quadrature. Its old half-sheet factor remains; no new 2pi or half is inserted.

## 5. Bounded saved-field test and exact remaining qualification

A defined first test uses compactly supported meridional/angular trace-free metric variations on the authentic saved conformal h0, retaining all four CLOSED beta,chi arms and every source/current/state. Use (3),(4) or a first-derivative connection-difference gravity action; record gravity, even native, odd native, matter, U chain and modal chain independently. Test projected-U, modal and normal compatibility separately. No metric inverse or boundary/homogeneous mode is selected.

An off-shell conditional weak residual is not a full Einstein certificate: keep the actual background/extrinsic contributions as uncomputed labelled terms unless registered. At next weak order Pi_eff=[T_total-M^2 G_beyond_linear]^TF; retain scalar, TT, spatial-vector compatibility, trace and normal equations together. A signed residual or small scalar potential does not bound an orbital force or a near-null inverse.

The action defines the conditional metric/source functional, but actual graph-to-field normalization, physical temporal spectrum, state/ordinary closure, exterior homogeneous metric modes and FLRW/extrinsic matching are not thereby registered. The finite-box native/lapse/odd walls do not supply a physical spatial metric boundary. A prospective compact residual packet may compute registered pieces only and preserve unknown background/exterior terms as None; it cannot claim full metric, stability, formation or observed success.

## Actual protected inputs

- INVARIANT_CLOCK_GRADIENT_SHARED_ACTION_BUDGET_DOMAIN_AND_NORMAL_V003.md — e08b7166892ec59c863539d59b8d4b89c654081776d8870239ecc2c382572da0
- CROSS_U_STATIC_HILBERT_STRESS_AND_LEADING_LENSING_INTERFACE_V001.md — 6844c982d0c017350d85731f3f58bf8b4167c860ee52f8bdd238ceef1fdcd68b
- CROSS_U_CONFORMAL_COLD_CIRCULAR_NEXT_ORDER_SOURCE_CLOSURE_V001.md — f8365d7bff3f420efe7d30746fd8fe3983a88e62dda1442c00ad73329e087979
- CROSS_U_NEXT_ORDER_ORBITAL_METRIC_AND_PHASE_CURRENT_CLOSURE_V001.md — 055e9707fd403e2059e8076e7a8fe070234deef807bdca2a0713b7bbaa2ec422
- CROSS_U_STATIONARY_AZIMUTHAL_SHIFT_AND_NATIVE_RESPONSE_V001.md — 048b224899adf28c6924fa02c06a2e2d42fced7f086a139ed8a6981e0dc20fe2
- CROSS_U_STATIONARY_AXISYMMETRIC_ORBIT_AND_ORDINARY_MATTER_REGISTRATION_V001.md — b962a4e6cc2583033f66b5194b50d47e1553456feda4147624d9f246bc86ebd5
- cross_u_ngc3198_odd_banded_correction_v001.py — a22931b8f9b8a0a1cca663a459892c634b0f484791a61495567bff33f14bc913
- CROSS_U_NGC3198_ODD_BANDED_CORRECTION_V001.md — 0f7b501037a0f0e65359435825b9d48f49d1249efc6c39a4549e285bdf88423b
- CROSS_U_NGC3198_ODD_BANDED_CORRECTION_V001_RESULT.json — fc54d032172c901d288d7f845c077b7f4114199183190e3c0b7eb2c8a1420e85
- CROSS_U_NGC3198_ODD_BANDED_CORRECTION_V001_RECEIPT.json — 41a22374c9747d5b64bf4894290433af8a2cdb92f345f64f6de89f8cc175ea0f
