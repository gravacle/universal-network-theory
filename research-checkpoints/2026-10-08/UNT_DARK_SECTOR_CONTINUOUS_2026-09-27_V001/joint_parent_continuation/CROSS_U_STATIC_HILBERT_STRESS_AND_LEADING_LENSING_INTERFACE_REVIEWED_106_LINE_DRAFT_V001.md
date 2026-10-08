# S_cross static Hilbert stress and leading lensing interface V001

2026-10-06 UTC. NEW unexecuted analytical companion, pending full independent review. This derives a conditional metric interface from ORIGINAL V003 Eq5 and the actual disk equations. No source, field, operator, stress integral or optical prediction has been evaluated. The converged coarse lapse is retained as a numerical result, with its physical/refinement flags unchanged. No AQUAL, K(X), S_dual stress or older fitted lensing score is transferred; all existing science lanes and their failures remain open at their actual scopes.

## 1. Exact aligned static branch and held variables

Use signature (-,+,+,+), c_p=1, M^2=(8pi Gbare)^-1 and g=M^2 C=2M_N^2, C=2-KB>0. Take ds^2=-N^2dt^2+h_ij dx^i dx^j, U=N^-1 partial_t, phi=omega t, and static spatial modes. V003 uses delta_old in (0,Lambda); here delta=delta_old/Lambda in (0,1), z_delta=delta_old y_delta_old and w(delta)d delta=nu(delta_old)d delta_old/integral nu. Define a_i=D_i lnN and Z_i=integral w z_delta,i. The normalized proper mode potential is

    U_delta(z)=z^2/2+(z^2)^2/(4 gc^2 delta^4),
    f_delta=1+z^2/(gc^2 delta^4), B_ij=D_i z_j, C_ij=B_(ij).

Here gc^2=kappa Lambda^4/u4 is the owned normalized-family registration: the original u4/(kappa delta_old^4) equals 1/(gc^2 delta^4). This is the geometric acceleration gc_SI/c_p^2 and ell is a proper length. The current disk convention has gc_SI=3pi a0/8 and ell=100pc; no new scale is chosen. Physical z_i has inverse-length units. The code stores dimensionless sqrt(w_j) z_j/(a0/c_p^2), not a second energy sector.

The time-projected mode velocity and Y=|P_U dphi|^2 vanish with their first variations on this branch. For a spatial metric variation at fixed N and held covectors z_i, unit-U and U.z reaction variations vanish. The stationary U equation must still hold; this restriction is legitimate only on that branch, and is not a prescription for lapse/U variations or a dynamical mode minimum. Up to the Einstein boundary term the pulled-back action is

    S_stat=integral dt N sqrt(h) [M^2 R^(3)/2+L_stat]+S_o,
    L_stat=M^2 KB a^2/2+P(omega/N)
           +g integral w[-U_delta-ell^2 B_ij B^ij/2+a^i z_i].       (1)

In deriving the lapse source, U=N^-1 partial_t follows the lapse variation and retains its unit reaction. The absolute P budget is unchanged. A local cosmological subtraction is applied to the actual source after variation, with its background contacts retained or explicitly bounded.

## 2. Full spatial stress, including the vector connection

Use delta S_stat=+integral N sqrt(h) T^ij delta h_ij/2. The nonordinary spatial Hilbert stress on the branch is

    T_ij=L_stat h_ij-M^2 KB a_i a_j
       +g integral w{f_delta z_i z_j-2a_(i z_j)
           +ell^2[B_ik B_j^k+B_ki B^k_j]
           +(ell^2/N)[D_k(N z^k C_ij)
                       -2D_k(N z_(i C_j)^k)]}.                    (2)

The isotropic L_stat term includes P. Equation(2) comes from varying BOTH inverse metrics in |Dz|^2 and delta(D_i z_j)=-delta Gamma^k_ij z_k. The last two divergences are the connection improvement; replacing the vector gradient by two scalar-gradient stresses loses them. Boundary tractions from the same variation are retained. This is an on-shell held-covector representation of the Hilbert source, not an off-shell deletion of unit/alignment reactions.

In the leading Euclidean spatial chart only, for a meridional disk z=z_R dR+z_Z dZ, |Dz|^2=(partial_R z_R)^2+(partial_Z z_R)^2+(partial_R z_Z)^2+(partial_Z z_Z)^2+z_R^2/R^2. For a spherical radial mode it is (z')^2+2z^2/r^2. These are the actual flat-leading cylindrical/spherical connection terms; the exact curved h_ij requires its proper inverse-metric factors and connection in (1)-(3). Midplane, axis and physical outer face conditions act on the tensor/divergences too. A thin ordinary sheet and piecewise finite-element fields require their weak surface/jump terms; a cellwise second derivative cannot silently replace them.

The lapse variation independently gives, with W=XP_X,

    rho_phi=W-P,
    rho_native=M^2 KB[div a+a^2/2]
              +g integral w[div z+U_delta+ell^2|Dz|^2/2].          (3)

The coupling a.Z cancels against its lapse-divergence contact. The terms div a and div Z contain the linear polarization/unit reaction; they are not additional positive mode energies. Equation(3) and (2) must be used together, counting the same action once.

## 3. The lapse normalization and the independent spatial metric

For an exact static metric R_00/N^2=Delta_h N/N=(rho+T^i_i)/(2M^2). At the leading weak-metric order, a=grad Phi, Phi=lnN+O(Phi^2), and all native spatial stresses in (2) start quadratically about zero fields. The linear native active source is M^2 KB Delta Phi+g div Z. Therefore

    g div(grad Phi-Z)=delta rho_o+delta rho_phi+3delta P
                     +the retained quadratic/background remainder. (4)

Since g=M^2(2-KB)=2M_N^2, the high-response-suppression limit has ONE 4pi G_N source coefficient. In the actual code Phi_0=B0 psi, B0=a0 L0/c_p^2 and L0=1kpc; (4) is its literal kappa/active-clock/surface-load normalization. There is no extra .99 factor multiplying ordinary baryons. The disk solve explicitly omits the full native quadratic Hilbert remainder and the full spatial Einstein equations.

In a weak static local Cartesian chart set

    ds^2=-(1+2Phi)dt^2+[(1-2Psi)delta_ij+gamma_ij^TT]dx^i dx^j,
    (partial_i partial_j-delta_ij Delta/3)(Psi-Phi)
         -Delta gamma_ij^TT/2=Pi_ij/M^2,
    Pi_ij=[T_ij+T_o,ij]^TF.                                      (5)

Scalar and transverse-traceless projections give respectively

    Delta^2(Psi-Phi)=3 partial_i partial_j Pi_ij/(2M^2),
    Delta gamma_ij^TT=-2Pi_ij^TT/M^2.                             (6)

Equations(5)-(6) give the linear spatial Einstein operator, not every nonlinear static metric equation. If quadratic native stress is used for a next-order correction, the same-order nonlinear geometric/background contact must also be included: replace Pi by Pi_eff=[T_total-M^2 G_beyond_linear]^TF after the actual background split, without subtracting the linear part already on the left. In a strictly static zero-shift branch, its spatial vector projection must satisfy P_transverse,i^k partial^j Pi_eff,kj=0, with the actual boundary conditions; scalar+TT inversions cannot discard a nonzero vector source. G_0i=T_0i/M^2, spatial trace, the normal constraint and full source conservation must also be satisfied. Nonzero ordinary angular momentum requires its stationary shift, or a time-dependent/vector metric if that is the supplied state. This is a compatibility condition, not an assumed vanishing stress or a new constitutive law.

For spherical symmetry gamma^TT=0 and (Psi-Phi)''-(Psi-Phi)'/r=(p_r-p_t)/M^2. The disk has a genuine tensor projection as well as the scalar slip. Its full meridional native vectors, their angular connection stress and the actual ordinary stress are needed, not just the 43 midplane forces. Regularity and the inherited exterior metric fix the homogeneous solutions of (6); an arbitrary zero-slip face cannot be called a cosmological junction.

Isotropic P does not source Pi_ij, but its spatial trace and homogeneous curvature contacts still belong to the remaining Einstein rows. A loaded static perturbation on an off-shell flat background cannot retain 3delta P in (4) and thereby claim that all spatial/background constraints have been solved. In the controlled local subhorizon ordering, such contacts are separately small or matched; their actual omission must be bounded.

## 4. When the computed potential is a leading lens potential

The useful nonlinear-acceleration weak-metric ordering holds a/a0 and z_delta/a0 fixed while B0 is small, with finite ell/L and fixed gc/a0. Thus the quartic response can be important in (4) while each dyadic/gradient stress in (2) is quadratic in the geometric field scale a0/c_p^2. This distinguishes a leading native polarization-divergence force from its spatial stress. It supplies an ordering, not a measured remainder certificate: strong derivatives, very small spatial scales, a near pressure-band edge, boundary terms or a poorly conditioned spatial inverse can defeat a naive small-potential estimate.

If the actual omitted active source, scalar slip and tensor optical contribution are bounded at the solved source/wall; ordinary velocity/pressure stresses and local cosmological contacts satisfy the same ordering; and the inherited homogeneous metric modes are controlled, then

    Phi+Psi=2B0 psi+the explicitly bounded correction.             (7)

Current residual convergence alone does not establish those conditions. In particular the core readout's positive native normal-energy estimate and acceleration-coupling estimate are not a bound on the connection improvement or on (6). A first same-action continuation can evaluate (2)-(3) from the already saved full fields with the same measure/parities and independent quadrature/mesh/exterior checks, then solve the linear spatial metric correction with disclosed matching data. It must keep both the correction to Phi from the omitted active source and Psi-Phi; simply declaring Psi=Phi discards the desired check.

At a locally constant environment the positive per-mode static Hessian obeys D_j>=I+ell^2 k^2 I, so 0<=chi_L<=sum_j w_j/(1+ell^2 k^2). The physical lapse Schur symbol is k^2(1-chi_L)-M_clock. If the signed pressure-loading term M_clock/k^2 is small, k ell>>1 suppresses native polarization and restores the same G_N prefactor in (4). This is a static/local/physical-operator envelope, distinct from a numerical preconditioner, retarded resonance, complete Solar-System test or all-boundary stability statement.

## 5. Actual optical readout and preserved observational scope

For the scalar leading metric, the physical unreduced weak bending is alpha_hat=integral grad_perp(Phi+Psi) dl. The reduced lens-map deflection is alpha=(D_ls/D_s)alpha_hat, and kappa_lens=(D_l D_ls/(2D_s)) integral Delta_perp(Phi+Psi) dl. Proper path lengths and angular-diameter distances use the same adopted background. Tensor/frame-dragging/finite-distance corrections require the actual null-geodesic metric if they are not negligible. No older effective ESD force conversion is substituted.

The first closed native-elimination case is E1em05_HI0_H20, with stored residual 1.5412900786380307e-9 and all full-metric/junction/formation/refinement/stability flags false. It does not complete all four source variants or establish an observed lensing score. The official 15-bin KiDS ESD profile and full corrected covariance already exist in EFFECTIVE_ESD_FORWARD_V001_RESULT.json; missing for THIS nonlocal disk family are the individual/stacked baryon profiles and spatial radii, orientations, source-pair weights, external/matched metric state and the appropriate distance/calibration transfer. Its gbar abscissa alone does not determine those inputs. The older compact spherical mass-cancellation projection is action/source-specific, and the overlapping Mistele reduction is not a second independent likelihood.

No growth, merger, primordial normalization, thermal origin or microscopic P/current attribution is inferred here. The fiducial EPS1e-6 FLRW fixture is not transferred to the converged EPS1e-5 galaxy branch. The immediate earned interface is a conditional same-action spatial-stress/metric correction from the full galaxy fields; the subsequent observational projection needs its actual source catalogue and matching data.

## Protected actual inputs

- INVARIANT_CLOCK_GRADIENT_SHARED_ACTION_BUDGET_DOMAIN_AND_NORMAL_V003.md — e08b7166892ec59c863539d59b8d4b89c654081776d8870239ecc2c382572da0
- cross_u_ngc3198_nonlinear_disk_v001.py — ae4285fc9c19cdf2d8efa176ac3d770b7eaf379a75fa3b9627bc9d3f6f3179e1
- CROSS_U_NGC3198_NONLINEAR_DISK_V001.md — a5e7f129c46af6aac63bbec179d98fe8ae9d3ac7178d0598bb23ba21eaf92b76
- CROSS_U_NGC3198_NONLINEAR_DISK_V001_MANIFEST.json — 65cb05b3aba084bde5fe75015e0a546c0c116a5a7906e7f647a5f2232c206683
- CROSS_U_NGC3198_NATIVE_ELIMINATION_RECOVERY_V006_RESULT.json — d470f406ec2279c9631f8e3e3c46a9e0d862f2a1691e1af6851b80aa871f3ff8
- CROSS_U_NGC3198_NATIVE_ELIMINATION_RECOVERY_V006_RECEIPT.json — 581605c923df95b6008ccf0fabe7ce1fc7ce7533e5d7cd2b2b51e36d90899b3f
- EFFECTIVE_ESD_FORWARD_V001.md — 40a540f3c5bbfd27aad5f4ef2033e7fca2c186f290dddd6079e94cf6a7955e9b
- EFFECTIVE_ESD_FORWARD_V001_RESULT.json — ec9a99b80bebf2a634ae4068407e4ee6767614c43d5376eb6e564076f5b5a433

- CROSS_U_STATIC_HILBERT_STRESS_AND_LEADING_LENSING_INTERFACE_REVIEWED_100_LINE_DRAFT_V001.md — bb2558f14ebe70a1ccd4ea123767a49eff3e6a172f7565f20443263841b6398a

- CROSS_U_STATIC_HILBERT_STRESS_AND_LEADING_LENSING_INTERFACE_REVIEWED_102_LINE_DRAFT_V001.md — 39f3b799c105e4b9f3e7ad611009e88509248fa8a68e8bc2afe70f1683f7a09c

All eight scientific input bytes were checked before exclusive creation and after the optical/spectral/vector registration clarifications; the protected 100/102-line reviewed ancestors are two additional seals. The normalized spectral label, flat-leading component convention and full static Einstein compatibility are now explicit. Historical modes are unchanged. This new analytical file is released for independent review, not numerical execution or physical adoption.
