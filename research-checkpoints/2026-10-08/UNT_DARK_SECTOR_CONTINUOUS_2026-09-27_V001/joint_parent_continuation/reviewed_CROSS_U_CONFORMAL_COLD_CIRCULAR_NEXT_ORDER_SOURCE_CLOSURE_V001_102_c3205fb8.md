# S_cross conformal and cold-circular next-order source closure V001

2026-10-06 UTC. AUTHOR_DRAFT=True. Guarded analytical companion for root and independent FULL review. No field, orbit, source, numerical operator or observational score has been evaluated. This supplies a concrete ordinary source prescription and conformal native correction from the SAME V003 Eq(5); it neither changes the action nor declares a full stationary metric solved. The accepted fixed-flat companion remains correct at its stated scope.

## 1. Ordinary minimal coupling and the declared state

Keep the existing registered stellar/HI/H2 surface profiles, their normalization, EPS and all native/clock coefficients. As an explicit benchmark state, treat each ordinary component as a co-rotating pressureless razor-thin sheet on the same circular geodesic branch. This is not a measured stellar distribution function or a gas-pressure model. Fix one rotation orientation; do not cancel its momentum by introducing an unprovided counterrotating population. No observed velocity is used to determine its motion.

Use c_p=1 for tensor/current formulas below, restoring c_p in the displayed physical energy/stress. In the circular metric ds^2=-N^2dt^2+h_AB dx^A dx^B+h_phi_phi(dphi+beta^phi dt)^2, let n be the unit future ADM normal and e_phi the unit azimuthal vector. Put u_b=Gamma_b(n+b_v e_phi), b_v=v_ZAMO/c_p and Gamma_b=(1-b_v^2)^-1/2. Predicted Omega obeys

    partial_R g_tt+2Omega partial_R g_tphi+Omega^2 partial_R g_phiphi=0,
    v_ZAMO=sqrt(h_phiphi)(Omega+beta^phi)/N.                     (1)

Reflection symmetry supplies the equatorial condition only with its actual mean/one-sided sheet registration. Require a real future timelike circular branch wherever the source is supported; negative signed force is not clipped into an orbit. Radial/vertical stability is a separate second-variation condition. The 43 observed-radius readouts alone do not establish admission over the full source.

## 2. Fixed mass annuli, proper surface delta and streaming sources

Preserve the SAME registered rest mass in each original coordinate annulus: dM0=Sigma_input(R) R dR dphi. This is a disclosed continuation of the existing flat source registration, not a new photometric deprojection. With H_sheet=det(h_ab) on the R,phi sheet and D_Sigma the normal-frame rest-mass density per proper area,

    D_Sigma sqrt(H_sheet)=R Sigma_input,
    Sigma_rest=D_Sigma/Gamma_b,
    S_b^(mu nu)=Sigma_rest c_p^2 u_b^mu u_b^nu                 (2)

where u_b is unit-normalized in (2). Holding Sigma_rest=Sigma_input instead would change the admitted annular mass through Gamma_b and the proper area. Separate components can retain their own fixed mass annuli and share the declared circular branch; combining their stresses does not add the baryon inventory again.

The orthonormal surface sources are E_Sigma=D_Sigma c_p^2 Gamma_b, ADM azimuthal momentum j_hatphi=E_Sigma b_v, and S_hatphi_hatphi=E_Sigma b_v^2, with radial/vertical stress zero. Covariant S_hat0_hatphi=-j_hatphi, while contravariant S^(hat0 hatphi)=+j_hatphi. Physical mass momentum is D_Sigma Gamma_b v_ZAMO; the tensor j_hatphi has energy-per-area units. Thus

    E_Sigma+trace S_Sigma=D_Sigma c_p^2 Gamma_b(1+b_v^2)
        =D_Sigma c_p^2[1+3 b_v^2/2+O(b_v^4)].                 (3)

The normal energy alone contains +D_Sigma v_ZAMO^2/2. Adding only Sigma v^2 and Sigma v misses that contact. Multiply the surface tensor by delta(l_Z); for a reflection-orthogonal sheet delta(l_Z)=delta(Z)/sqrt(h_ZZ). In c_p=1 coordinates its mass current has J_b^t=D_Sigma/N and J_b^phi=D_Sigma Omega/N, with no meridional flux. Then N sqrt(H_sheet) J_b^t=R Sigma_input and stationary axisymmetry gives continuity. Stress conservation adds exactly (1); a freely specified velocity would not satisfy it. The normal sheet force requires the reflected mean/junction condition, not a smooth pointwise derivative through the density delta.

## 3. Exact static Hilbert trace and the conformal cancellation

For the aligned zero-shift static part take U=N^-1 partial_t, phi=omega t, a_i=D_i Phi, Phi=lnN and held spatial covectors z_j; Z_i=sum_j w_j z_j,i. Let g=M^2 C=2M_N^2, C=2-KB, and define k_j=gc^2 xi_j^4, G_j,ki=D_k z_j,i and S_j,ij=G_j,(ij). With the actual proper spatial metric,

    F_kij=sum_j w_j[z_j,k S_j,ij-z_j,i S_j,jk-z_j,j S_j,ik],
    J^k=h^(kl)h^(ij)F_lij,
    Q0_h=sum_j w_j[|z_j|_h^4/(2k_j)+ell^2|Dz_j|_h^2]
              +a^i Z_i+ell^2(div_h J+a_i J^i).

The accepted Hilbert source gives S_native=M^2 KB div_h a+g div_h Z+M^2 KB|a|_h^2+g Q0_h. Combining it with 2M^2 Delta_h N/N=S_o+S_phi+S_native, Delta_h N/N=div_h a+|a|_h^2, S_phi=XP_X+2P and S_o=rho_o+trace T_o, yields

    g div_h(a-Z)=S_o+S_phi+g[Q0_h-|a|_h^2].                   (4)

The Maxwell coefficient is retained once: (2-KB)M^2=g, so there is no extra KB or .99 source normalization. All unit/projected-U reactions used in the accepted Hilbert derivation remain required. Equation(4) is its static identity, not permission to discard the other Einstein/source rows.

Take the CONFORMAL-LEADING metric h_ij=e^-2Psi delta_ij. For coordinate covectors a,Z, div_h(a-Z)=e^2Psi[Delta Phi-div_flat Z-grad Psi.(a-Z)] and |a|_h^2=e^2Psi|grad Phi|^2. Dividing (4) by e^2Psi therefore places a.Z-|a|^2+grad Psi.(a-Z) on the flat RHS. These terms cancel at leading Psi=Phi. The remaining row is

    g[Delta Phi-div_flat Z]=e^-2Phi(S_o+S_phi)
      +g e^-2Phi{sum_j w_j[|z_j|_h^4/(2k_j)+ell^2|Dz_j|_h^2]
                       +ell^2(div_h J+a.J)}.                 (5)

Equation(5) uses Psi=Phi only at the stated leading conformal order. Do not append the fixed-flat companion's a.Z-|a|^2 correction again. Native quartic/gradient/connection-improvement, source-volume and modal-geometry contacts remain; all weak sheet/interior/outer fluxes come from the SAME covariant divergence. The already counted weak improvement is not supplemented by duplicate sheet deltas.

## 4. Proper ordinary and phase source-volume contacts

For the fixed-annulus prescription, conformal H_sheet=e^-4Psi R^2 gives D_Sigma=e^2Psi Sigma_input and delta(l_Z)=e^Psi delta(Z). Thus the flat RHS ordinary sheet is

    e^-2Psi S_o=e^Psi Sigma_input c_p^2 Gamma_b(1+b_v^2)delta(Z),
    extra ordinary sheet source=Sigma_input c_p^2
                     [Psi+3b_v^2/2]delta(Z)+higher orders.    (6)

It is not e^-2Psi times a frozen coordinate density. Hold the actual clock X=omega e^-Phi and evaluate its complete P family before the cosmological subtraction. In particular e^-2Psi S_phi-Sbar_phi=e^-2Psi delta S_phi+(e^-2Psi-1)Sbar_phi. The last term belongs with the actual background Einstein/curvature contacts; multiplying only Model's already-subtracted active clock source would omit it. Near the charged edge keep the exact P and signed D_phi+3W response rather than imposing a small-Phi/epsilon approximation.

## 5. Native mode geometry from first-derivative variation

Vary modes at HELD independent Phi,Psi, and only then insert the leading Psi=Phi. In Cartesian covector components D_k z_i=G_ki+C_ki, C_ki=a_k z_i+a_i z_k-delta_ki(a.z). Replace G by the full flat cylindrical covariant derivative in the axisymmetric chart. The fixed-lapse mode Euler functional becomes

    E_mode/g=integral sum_j w_j[|z_j|^2/2
        +e^2Phi |z_j|^4/(4k_j)+ell^2 e^2Phi|G_j+C_j|^2/2
        -a.z_j]d^3x.                                         (7)

The mass and coupling weights cancel; the quartic and proper-gradient weights do not. This is a variational functional for the mode row, not an extra normal-energy sector. With Phi=B0 psi, z_j=(B0/L0)u_j, gc=(B0/L0)gc_star and ell_star=ell/L0, normalize the functional by g B0^2 L0. Its first geometry correction is

    B0 integral sum_j w_j[psi|u_j|^4/(2gc_star^2 xi_j^4)
       +ell_star^2 psi|Du_j|^2
       +ell_star^2 Du_j:C(grad psi,u_j)]d^3x.                 (8)

This first-derivative weak form supplies the adjoint volume/face contacts for Q1 fields. Preserve the original parity/axis/outer registrations. It replaces an independently appended flat N-weight drift in this conformal prescription; adding both would count geometry twice. Setting delta Psi=delta Phi BEFORE independent metric variation would lose Einstein equations and is not used here.

## 6. Shift, phase current and the accountable continuation

The ordinary azimuthal momentum in (3) requires G_0i=T_total,0i/M^2. Solve its stationary shift jointly with the projected U/mode rows, unit reactions, phase integrability/conservation and full normal/spatial constraints. Stationary coordinate modes need not have zero U-projected velocity in a shifted metric. No phase current is appended from saved density: if U is admitted as the ADM normal, J_phi=n_phi U has zero normal-spatial flux, but its coordinate azimuthal component includes the shift. Whether that aligned choice still solves the projected U/mode equations is a test, not an assigned current.

Under a controlled weak hierarchy Phi~Psi~v^2/c_p^2, ordinary kinetic/area and shift-orbit effects are post-Newtonian order; scalar slip/TT sourced by quadratic stress must still be solved with the nonlinear geometric/background terms. No source envelope bounds the signed metric inverse, and retained native inertias or a near-null branch can invalidate naive order estimates. The inherited numerical wall is not an adopted exterior or FLRW junction.

The shortest implementation is: admit a predicted circular branch for the fixed mass annuli; construct (2),(3),(6); add (5),(8) with the exact clock and original signed scalar/native response; solve ordinary-current shift and remaining metric/source rows; evaluate the full orbital formula (1) with its derivative/contact registration. No halo amplitude, counterrotation, source fit, direct native force, physical state preparation or new boundary is selected. All existing observational/refinement/full-metric/formation/stability qualifications remain unchanged.

## Actual protected inputs

- INVARIANT_CLOCK_GRADIENT_SHARED_ACTION_BUDGET_DOMAIN_AND_NORMAL_V003.md — e08b7166892ec59c863539d59b8d4b89c654081776d8870239ecc2c382572da0
- CROSS_U_STATIC_HILBERT_STRESS_AND_LEADING_LENSING_INTERFACE_V001.md — 6844c982d0c017350d85731f3f58bf8b4167c860ee52f8bdd238ceef1fdcd68b
- CROSS_U_STATIONARY_AXISYMMETRIC_ORBIT_AND_ORDINARY_MATTER_REGISTRATION_V001.md — b962a4e6cc2583033f66b5194b50d47e1553456feda4147624d9f246bc86ebd5
- cross_u_ngc3198_nonlinear_disk_v001.py — ae4285fc9c19cdf2d8efa176ac3d770b7eaf379a75fa3b9627bc9d3f6f3179e1
- cross_u_ngc3198_saved_weak_stress_meter_v002.py — af1c2f0826380c714220e090f755fc20773c76804f2b0952e1f6400f9cd6eee6
- CROSS_U_NGC3198_SAVED_WEAK_STRESS_METER_V002.md — be14d5467450d17f0cd0d5b2b310d1a21db1cbcb2890859807d7a27ccd101202
- CROSS_U_NGC3198_SAVED_WEAK_STRESS_METER_V002_RESULT.json — d8d7de0d9f2faf7545c400230d116ad1dc2fe3488471982e3c1c01d3aac582c1
- CROSS_U_NGC3198_SAVED_WEAK_STRESS_METER_V002_RECEIPT.json — 12d150e67f3da4f36714e52480d5c7e90f7b7b0fd3dac919787e021503312018
- CROSS_U_NEXT_ORDER_ORBITAL_METRIC_AND_PHASE_CURRENT_CLOSURE_V001.md — 055e9707fd403e2059e8076e7a8fe070234deef807bdca2a0713b7bbaa2ec422

All nine direct input bytes were checked before exclusive creation. The guarded companion remains unaccepted pending root and independent FULL review. No old file, field or failure disposition was changed; no scientific expression was evaluated.
