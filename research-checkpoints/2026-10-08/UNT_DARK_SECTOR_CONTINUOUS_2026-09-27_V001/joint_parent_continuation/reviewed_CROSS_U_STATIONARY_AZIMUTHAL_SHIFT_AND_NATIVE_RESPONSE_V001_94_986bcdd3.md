# S_cross stationary azimuthal shift and native response V001

2026-10-06 UTC. AUTHOR_DRAFT=True. Guarded analytical companion, awaiting root and independent FULL text/pin review. No scientific function, field, orbit, operator, numerical action or trajectory has been evaluated. This derives a concrete stationary odd sector of the SAME uncompressed V003 Eq(5), retaining the existing even metric, ordinary mass annuli and mode family; it does not declare a full stationary galaxy or select incoming modes, a temporal spectrum, exterior data or a physical preparation.

## 1. Circular geometry and the independent vector

Use c_p=1 for action/current formulas and proper inverse-time/length units consistently. In ds^2=-N^2dt^2+h_AB dx^A dx^B+rho^2(dphi+beta dt)^2, rho=sqrt(h_phiphi), n=(partial_t-beta partial_phi)/N and e=partial_phi/rho. Let U=c n+s e and E=s n+c e, c=cosh chi,s=sinh chi. Native z_j are stationary axisymmetric meridional covectors, U.z_j=0. The admitted phase is phi_phase=omega t with spatial winding absent; its invariant X=Q=omega/N is independent of U and remains so for this circular shift.

Let D be the proper meridional covariant derivative, a=D lnN, b=D lnrho, d=b-a, t=(rho/N)D beta, k=M^2 KB, g=M^2 C=2M_N^2 and C=2-KB. Use the actual positive native weights w_j, quartic k_j=gc^2 xi_j^4, ell and temporal inertias 1/omega_j^2. Define Z=sum_j w_j z_j and T=k a+g Z. No extra physical G or .99 multiplier is supplied to the shift. The static spatial calibration does not by itself determine omega_j; actual dynamic parameters, or an explicitly declared existing benchmark, remain necessary.

The meridional connection identities for the displayed +beta convention are nabla_n n=a, nabla_e e=-b and nabla_n e=nabla_e n=-t/2. They give the exact first-derivative stationary jets

    A_U=c^2 a-s^2 b-cs t,
    F_AE=D chi+cs d+s^2 t,
    V_j=(P_U nabla_U z_j)_E=[cs d+(c^2+s^2)t/2].z_j,
    B_j=(Dcal_E z_j)_E=[c^2 b-s^2 a+cs t].z_j.                (1)

Here F=2nabla_[mu U_nu], its spatial magnetic norm is 2|F_AE|^2, and the remaining mode gradient is G_j,AB=D_A z_j,B. A stationary coordinate mode generally has V_j=(t.z_j)/2 even at chi=0. Y=|P_U dphi_phase|^2=Q^2s^2. The ADM extrinsic-curvature entries are K_A,hatphi=-t_A/2 and K=0, so K_ij K^ij=|t|^2/2.

Up to the actual Einstein boundary term, the exact meridional-sector stationary restriction has measure N sqrt(h)dt d^3x and integrand

    L_st=M^2 R_3/2+M^2|t|^2/4
       +k(|A_U|^2-|F_AE|^2)/2+P(Q)-g Q^2s^2/2
       +g sum_j w_j[V_j^2/(2omega_j^2)-U_j(z_j)
           -ell^2(|G_j,AB|^2+B_j^2)/2+A_U.z_j],
    U_j(z)=|z|^2/2+|z|^4/(4k_j).                             (2)

Ordinary minimally coupled matter and all native unit/projection reactions are retained. This restriction follows their full variation; fixing chi=0 before the projected-U equation would lose a source row. No S_dual multiplier or phase/mode holonomy has been inserted.

## 2. Quadratic shift/tilt action and its two source rows

Hold the leading even N,h_AB,rho,z_j and expand small beta,chi through second order. Let v_j=chi(d.z_j)+(t.z_j)/2 and W_chi=Dchi+chi d. After subtracting the even static integrand, the entire odd quadratic integrand is

    L_2=M^2|t|^2/4-k|W_chi|^2/2
       -T.(chi^2 d+chi t)-gQ^2chi^2/2
       +g sum_j w_j[v_j^2/(2omega_j^2)
          -ell^2(b.z_j){chi^2(d.z_j)+chi(t.z_j)}].            (3)

All contractions and volume/divergence in (3) use the proper held spatial metric. The negative Maxwell magnetic gradient, phase-relative term, modal inertia, angular-gradient contacts and Einstein shift term are separate literal action terms, not an added force or energy inventory.

Set P_t=partial L_2/partial t. Variation of beta and the ordinary action gives

    P_t=(M^2/2)t-chi T+(g/2)sum_j w_j(v_j/omega_j^2)z_j
                         -g ell^2 chi sum_j w_j(b.z_j)z_j,
    div_3(rho P_t)=j_phi,o,  j_phi,o=rho j_hatphi,o.          (4)

The RHS is the covariant coordinate angular momentum density, including its proper sheet delta; it is not j_hatphi,o alone. Indeed delta S_o=integral sqrt(h)j_phi,o delta beta, while the field variation is integral sqrt(h)rho P_t.Ddelta beta. In the pure Einstein flat check, (4) becomes (M^2/2)[R^-1 partial_R(R^3 beta_R)+partial_Z(R^2 beta_Z)]=j_phi,o, equivalently Delta(R beta e_phi)=2j_hatphi,o e_phi/M^2. This fixes the sign; a positive prograde source has negative beta for the usual zero-wall particular inverse. That check does not choose a physical wall.

Let div_N W=(N sqrt(h))^-1 partial_A[N sqrt(h)W^A]. The projected-U equation obtained from varying chi is

    k[div_N W_chi-d.W_chi]-T.(2chi d+t)-gQ^2chi
       +g sum_j w_j[(v_j/omega_j^2)(d.z_j)
           -ell^2(b.z_j){2chi(d.z_j)+(t.z_j)}]=0.            (5)

The gradient and local terms retain their action signs. Neither uniform coercivity, uniqueness, a bounded inverse nor full dynamical stability is inferred. The actual modal frequencies are retained; replacing them by the static susceptibility would change this equation. Variation of beta at fixed chi changes U's coordinate components; therefore the restricted momentum row is the full Hilbert momentum equation together with (5), not a stand-alone metric row after deleting the independent-vector Euler equation.

## 3. ADM alignment, phase current and azimuthal native modes

At chi=0, (5) requires

    t.[-T+g sum_j w_j z_j{(d.z_j)/(2omega_j^2)
                                      -ell^2(b.z_j)}]=0.     (6)

A nonzero ordinary angular momentum generally produces varying beta and does not generically preserve ADM alignment. Equation(6) is a testable cancellation condition; exceptional orthogonality or cancellation is possible. Rigid coordinate rotation D beta=0 has t=0 but is not a sourced rotating-disk solution. No theorem excluding all rotating native states follows.

The SAME action's phase Noether current, n_phi=P_X(Q), is exactly

    r=Q(s^2 n+cs e),
    J_phi=n_phi n-g r=(n_phi-gQ s^2)n-gQcs e.                 (7)

Thus the first-order normal-spatial phase current is -gQchi e; its normal charge changes at second order. Stationarity and axisymmetry with no meridional flux make div J_phi=0 directly, without assigning an extra current. At chi=0 its normal-spatial flux vanishes but coordinate J_phi^phi=-n_phi beta/N remains. This Noether current is not automatically an ordinary positive particle flow; such a physical registration and its timelike/charge conditions remain separate. Phase integrability and the global omega/outer-charge state are still required.

For an admitted azimuthal perturbation z_j -> z_j+zeta_j E, at the linear odd order Dcal_A(zeta E)=(D_A zeta)E and Dcal_E(zeta E)=-zeta b in the meridional plane. These occupy tensor components orthogonal to the retained meridional gradient; its projected time perturbation is meridional, orthogonal to V_j E. The potential and acceleration coupling have no linear cross term. Hence beta,chi do not linearly source zeta_j in this restricted sector. Homogeneous zeta_j=0 is consistent with the inherited zero/parity/outer data; supplied azimuthal modes or incoming packets are not excluded, and their homogeneous equation, state and stability cannot be erased by this observation.

## 4. Ordinary source, weak ports and the accountable next calculation

Use the accepted fixed-rest-mass-annulus cold-circular benchmark: D_Sigma sqrt(H_sheet)=R Sigma_input, Gamma_b=(1-v_ZAMO^2/c_p^2)^-1/2, E_Sigma=D_Sigma c_p^2 Gamma_b, j_hatphi,Sigma=E_Sigma v_ZAMO/c_p, and azimuthal stress E_Sigma v_ZAMO^2/c_p^2. Multiply by the SAME proper delta(l_Z); combine components once. The velocity is the predicted admitted timelike circular branch, not Vobs. Its ordinary momentum is therefore fixed by that benchmark and the actual metric, rather than appended as a fitted rotation source. Unknown pressure/distribution-function data are not silently supplied.

Equations(3)-(5) are first-derivative weak equations. Interior/sheet jumps and outer fluxes follow from the same N sqrt(h) action: the weak jump of rho P_t's normal component carries the admitted j_phi,o sheet, and the chi equation retains its Maxwell flux k N W_chi. There is no direct ordinary-U sheet force. Actual lapse/spatial Einstein and native boundary ports, angular-momentum matching and any cosmological extrinsic/background terms remain required. A zero outer beta or chi can be a disclosed finite-box benchmark but is not established physical exterior data.

At a regular axis rho=0, smooth azimuthal U requires chi=O(rho); beta is finite and radially even, and meridional z_R=O(rho). Contractions b.z then have regular limits. The action is treated in its weighted weak form, not by evaluating 1/rho on the axis. Under reflection through the sheet beta and chi are even, meridional z_R even and z_Z odd, preserving the inherited parity. Smooth-sheet/mean junction and actual outer data must be registered before deriving an orbital force.

The shortest concrete continuation is to admit the predicted cold circular source, solve (4),(5) with the retained proper mode inertias and compatible ports, retain (7), and then include the resulting shift in the accepted exact orbit formula. Hold the even metric only for this odd linearization; solve its normal/spatial/scalar-slip/TT/background corrections and the ordinary/full native source conservation separately. The usual beta~Phi^(3/2) weak-order estimate presumes a controlled spectrum and inverse; neither a source envelope nor this action supplies it. No ten-percent force claim, assigned phase flow, halo amplitude, exterior, temporal spectrum or physical formation history has been chosen.

## Actual protected inputs

- INVARIANT_CLOCK_GRADIENT_SHARED_ACTION_BUDGET_DOMAIN_AND_NORMAL_V003.md — e08b7166892ec59c863539d59b8d4b89c654081776d8870239ecc2c382572da0
- CROSS_U_STATIC_HILBERT_STRESS_AND_LEADING_LENSING_INTERFACE_V001.md — 6844c982d0c017350d85731f3f58bf8b4167c860ee52f8bdd238ceef1fdcd68b
- CROSS_U_CONFORMAL_COLD_CIRCULAR_NEXT_ORDER_SOURCE_CLOSURE_V001.md — f8365d7bff3f420efe7d30746fd8fe3983a88e62dda1442c00ad73329e087979
- CROSS_U_STATIONARY_AXISYMMETRIC_ORBIT_AND_ORDINARY_MATTER_REGISTRATION_V001.md — b962a4e6cc2583033f66b5194b50d47e1553456feda4147624d9f246bc86ebd5
- CROSS_U_NEXT_ORDER_ORBITAL_METRIC_AND_PHASE_CURRENT_CLOSURE_V001.md — 055e9707fd403e2059e8076e7a8fe070234deef807bdca2a0713b7bbaa2ec422
- cross_u_ngc3198_nonlinear_disk_v001.py — ae4285fc9c19cdf2d8efa176ac3d770b7eaf379a75fa3b9627bc9d3f6f3179e1

All six protected input bytes and readonly permissions were checked before and after exclusive creation. These equations were derived by static action/geometry analysis; no scientific expression was numerically evaluated. The draft remains unaccepted pending FULL root and independent text/pin review. Existing fields, source fixtures, operators, failures and qualifications are unchanged.
