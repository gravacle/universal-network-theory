# Native/coupled kinetic factorization and original-row precision V001
AUTHOR_DRAFT=True; analytical definitions only. No arrays, kinetic action, operator, inverse, solver, or evolution evaluated. No physical state or normal-constraint admission follows.

## 1. Exact local matrix identity
Use the admitted point densities D_j, M0, mixing L_j and signed blocks B=(Bu,Bz_1,…,Bz_32),T; u,v_j,k denote the three U rates, three rates per mode, and six metric rates in the authentic covector chart. All quantities here use the existing coordinate-density normalization and symmetric metric basis.
Define C=Bu−Σ_j L_jᵀBz_j and m_j=v_j+L_j u. The exact algebraic action of the SAVED coefficient matrices is

    pz_j = D_j m_j + Bz_j k,
    pu = M0 u + Σ_j L_jᵀ pz_j + C k,
    ph = Σ_j Bz_jᵀ m_j + Cᵀ u + T k.                 (1)

This expands to precisely the admitted native M and coupled B,T, without a D inverse. C is a retained discrepancy, not a new parameter. The present action evaluates native M first and adds Bk afterward; (1) instead combines the complete modal momentum before the U contraction, avoiding a subtraction between separately accumulated modal and metric U terms. Its metric row uses the algebraic adjoint of the same retained C.

## 2. What the exact action implies, and what stored rounding does not imply
Let S=[Jzz;I] be the transverse modal covector embedding and e0 the temporal covector. At fixed geometry, U·S=0 and P e0=S(U⁰ u_cov), where P projects covectors orthogonally to U and u_cov is the stored spatial covector U_i. The admitted L_j=(U⁰u_cov)JzU_j therefore gives

    δV_j[U-rate u]=δV_j[mode-rate L_j u],
    δD_j[U-rate u]=δD_j[mode-rate L_j u].            (2)

These are kinetic tangent identities, with the configuration held; changes of the projector caused by changing the configuration belong to other derivatives. They follow by inserting δnz_ab=δa0 δb0 JzU_j u into the two projected modal derivatives.
For Maxwell F=d(U_flat), a pure hdot variation at fixed N,β,U_i has δ(∂t U_i)=0. ∂t U_0 never enters the antisymmetric F_0i. Thus its pure-metric-rate kinetic tangent is zero even though individual metric/connection and constrained-U pieces need not vanish. The acceleration·Z term is affine in velocities and contributes no kinetic Hessian.
Consequently the exact same-action mixed Hessian obeys Bu=Σ_j L_jᵀBz_j. Independently constructed binary64 B and L need not satisfy this identity bitwise. Neither (2) nor an implementation control licenses discarding their actual C. Preserve C and its bound E_C=E_Bu+Σ_j E_LjᵀE_Bzj; certify the decomposition with compensated products/sums before any simplification. No signed block is symmetrized or clipped here.

## 3. Optional local completed square and its finite-element restriction
Conceptually set W_j=D_j⁻¹Bz_j and w_j=m_j+W_j k. Positive D_j gives

    pz_j=D_j w_j,
    pu=M0 u+Σ_j L_jᵀD_j w_j+Ck,
    ph=Σ_j Bz_jᵀw_j+Cᵀu+G0 k,
    G0=T−Σ_j Bz_jᵀD_j⁻¹Bz_j.                    (3)

G0 is signed; no positivity, uniqueness, or invertibility is inferred. (3) is an algebraic alternative, not a permission to assign free pointwise w_j. Authentic native Q1 and metric F bases, axis/parity lifts and incidence scatter remain fixed.
Let E_U,E_j,E_h denote these exact point evaluation maps; let Wq=diag(reference_volume/R), because D,M0,B,T already contain the coordinate density. Define the weighted modal projection Π_j=E_j(E_jᵀWqD_jE_j)⁻¹E_jᵀWqD_j. All inverses in this paragraph are symbolic only.
For R_Uj=(I−Π_j)L_jE_U and R_hj=(I−Π_j)W_jE_h, exact elimination of the GLOBAL modal coordinates leaves

    HUU=E_UᵀWqM0E_U+Σ_j R_UjᵀWqD_jR_Uj,
    HUh=E_UᵀWqCE_h+Σ_j R_UjᵀWqD_jR_hj,
    Hhh=E_hᵀWqG0E_h+Σ_j R_hjᵀWqD_jR_hj.        (4)

The projection terms survive when L_j or W_j varies through a cell. Dropping them would change the admitted global FE system even if C=0 exactly. A collocated point Schur is therefore insufficient for canonical nodal admission. Constant-coefficient closure or vanishing projection defects must be proved, not presumed from local Gram identities.

## 4. An offset representation that retains the original right-hand side
For x=x0+δ and the fixed saved global linear system A x=f, the exact original residual is r=(f−A x0)−Aδ. Neither the original binary64 f nor the original target norms/1e−10 certificates may be regenerated or replaced by a correction-relative test.
Retain the authenticated saved seed residual r_saved and disclose ε0=r_saved−(f−A x0). Reusing r_saved without ε0 after changing arithmetic can preserve an old rounding offset. A fresh certificate must evaluate the unchanged original rows; stable evaluation of f−A x0 is a precision operation, not a new source or canonical target.
An implementable bounded next instrument is (1) with compensated construction of C, mixed/modal products, inclusive pz, and incidence sums, plus an offset residual with compensated original-row contractions. Error-free two-sum/product expansions or explicitly verified wider arithmetic can carry low parts; platform long-double width must not be assumed. Preserve all signed matrices, original masks/bases, RHS, caps and admission tolerances.
First save a representation certificate against the original expanded coefficient polynomial using its existing uncancelled positive operation bounds, including C and all FE scatter terms. Then retain fresh original raw/scaled residual and actual-target ratios. Compensation reduces arithmetic cancellation; it does not establish intrinsic conditioning, solve the CMC incompatibility, select a history, or justify more iteration caps.

## 5. Disposition and actual inputs
CLOSED V002 owner41181 remains ORIGINAL_CANONICAL_ROWS_NOT_ADMITTED after its bounded corrections; 21 implementation controls do not supply RATE_JETS or an admitted normal-constraint seed. Earlier V001 failure/nonadmission and all qualifications remain unchanged. The reported actual-Pn ratio passing while the affine-row ratio fails is compatible with cancellation in a much smaller RHS; it is not itself proof that (1) will meet the original affine certificate.
These inputs are byte-bound; their old arrays have not been read or evaluated for this analytical addition:

- cross_u_weak_nodal_native_legendre_v001.py: e7b06d179d89b69c6136964266825c36b77425292f723fa65c134efa254cbe70
- cross_u_weak_nodal_metric_temporal_cmc_v001.py: e11bb7ec123971998fbdd64d1e2171627aae9202804d1c625202f412b5f85b6c
- cross_u_weak_canonical_spatial_euler_loads_v003.py: 4f239074b5345709f493b3633f7dd376fa7ac97dbb23bf20825eabde2ed56b79
- cross_u_canonical_nodal_metric_rate_solve_v001.py: f84b8a9bea9d45ac1370985401172621d93d59dc814bedda785206188b3c2c4b
- root_held_canonical_nodal_rate_solve_v002_731_3312f1c0.py: 3312f1c02b0d366e77542bd1338b5a82575703997619f6b840b961193cdb270d
- CROSS_U_CANONICAL_NODAL_METRIC_RATE_SOLVE_V002_RESULT.json: 6759a9c44574bfd75865d1867c4467df18deca79a162979b89f1546ba9e417b7
- CROSS_U_CANONICAL_NODAL_METRIC_RATE_SOLVE_V002_RECEIPT.json: 2b6603b36ef3596c419d76e2ce82ac9c50dae31d150fb850f2d4179a56e3ff70
