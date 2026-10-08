# k10 native jets and normal-constraint propagation V001

2026-10-06. Exclusive static continuation of the pinned SAME-action k10 proofs. Root, readonly and observer independently checked the native and normal algebra before creation. No coefficient, background, series, source/helper, operator, matrix or trajectory is evaluated. All original sources, states and failed dispositions remain protected. These are linear effective-fixture preparation identities, not microscopic origin, a corrected seed or a nonlinear physical-state solution.

## 1. Exact native equations and the next two jets

Use the parents' proper dimensionless tau=Hstar*t_proper, D=d/dlog(a), h=hr*a^-2*H and q=q0/a. For a retained mode s let omega_s²=omega_max²*s², Zj=<z_s,j>, R1,6=<omega_s²*z_s,6>, alpha=<omega_s²>, Delta0=alpha+C*Qc²/KB>0. Here brackets use the unchanged positive normalized mode weights; C=2Cbar. The literal equations are

    z_s,dd+3h*z_s,d+omega_s²*(1+ell²*q²)*z_s
                                      =omega_s²*(q*n+sigma),
    v=Z/(Q*q), n=v_dot-cs*Gamma_phi,
    P=(KB/2)*q*n+Cbar*Z, Pdot+2h*P=-Cbar*Q*sigma.       (1)

Q=Qc+O(a³), cs=c3*a³+O(a⁶). Write sigma=sigma2*a²+sigma3*a³+sigma4*a⁴+..., z_s=z_s6*a⁶+z_s7*a⁷+z_s8*a⁸+... and n=n5*a⁵+.... The inherited leading preparation has z_s6=omega_s²*sigma2/(42hr²). Set

    n5=7hr*Z6/(Qc*q0)-c3*Gamma_phi2,
    sigma3=[hr*Qc*q0*c3*(7Gamma_phi3+6h1*Gamma_phi2)
                                             -hr²*h1*Z6]/Delta0,
    z_s7=[omega_s²*sigma3-90hr²*h1*z_s6]/(56hr²),
    sigma4=[hr*Qc*q0*c3*(8Gamma_phi4+7h1*Gamma_phi3+6h2*Gamma_phi2)
            -alpha*q0*n5+ell²*q0²*R1,6-hr²*h1*Z7
                                  -16Cbar*hr*Qc*Z6/KB]/Delta0,
    z_s8=[omega_s²*(sigma4+q0*n5-ell²*q0²*z_s6)
                                      -119hr²*h1*z_s7]/(72hr²). (2)

Thus Z7 is formed before sigma4; no fitted mode profile or global coefficient solve is required. Converting the mode operator gives hr²*a^-4*[F D(D+1)+(DF/2)D] with F=H². At order7 its mode contact90 and P-Euler contact91 leave h1*Z6; at order8 contacts119 and120 leave h1*Z7. The remaining49*(h1²+2h2)*Z6 vanishes for the SAME background. The Cbar*Z6 part of P gives the last sigma4 term and must remain. Rest-frequency omega_s²*z_s6 first enters z_s10; the spatial ell² term already enters z_s8. Q and higher cs corrections occur after the displayed orders.

The necessary tangent data are zd_s4=6hr*z_s6, zd_s5=hr*(7z_s7+6h1*z_s6), zd_s6=hr*(8z_s8+7h1*z_s7+6h2*z_s6). These are derivatives of the same modal position series, not independently chosen velocities or a poststep projection. Serialized old sigma2/z6 may carry their declared binary rounding; it cannot be silently replaced by a newly solved value or treated as exact all-order data.

## 2. Exact normal propagation and independent finite coefficient rows

Let Btot=b+4(rg+rn)/3+w, Cpressure=cs*Gamma_phi, E=b*Gamma_b+rg*Gamma_gamma+rn*Gamma_nu+w*Gamma_phi and

    N=q²*Psi+3h*S+E-q*P,
    (qP)dot=-3h*qP-Cbar*Q*q*sigma,
    Edot=-3h*E-h*(rg*Gamma_gamma+rn*Gamma_nu)-3h*w*Cpressure
           +3Btot*Rdot-q²*Btot*V-q²*S-Cbar*Q*q*sigma.

The same-action identities hdot=-Btot, Rdot=S+h*Cpressure, Vdot=Phi+Cpressure and the correctly signed weighted S transport give

    Ndot+3h*N=h*[q²*(Psi-Phi)-2(rg*p+rn*Nnu)]=0.         (3)

Reaction transfers cancel between E and qP. The final equality is the exact shear constraint, not a discarded pressure term or a scalar-only current assumption. Hence N=constant*a^-3. The declared regular branch has no a^-3 normal-constraint mode, so all formal normal coefficients vanish when every same-order source is retained. This is an exact linear-source propagation identity; it does not bound a finite truncation or binary implementation error.

For independent coefficient checks define S0..S2 as in the first parent, S3=2hr²*(t*U7+r*wn7)+b3*U6, S4=2hr²*(t*U8+r*wn8)+b3*U7, rad4=3hr²/2 and w0=-w3*c3 from the literal pressure background. The additional normal rows are

    N1=q0²*Psi3+3hr*(S3+h1*S2+h2*S1+h3*S0)
              +b3*Gamma_b4+w3*Gamma_phi4
                                +rad4*(t*Gamma_gamma5+r*Gamma_nu5),
    N2=q0²*Psi4+3hr*(S4+h1*S3+h2*S2+h3*S1+h4*S0)
              +b3*Gamma_b5+w3*Gamma_phi5
                    +rad4*(t*Gamma_gamma6+r*Gamma_nu6)+w0*Gamma_phi2.

N2 is linear-log. Native n/Z and w3*eta6 first contribute at normal order a³, so are absent from these two rows. Together with N_-2,N_-1,N0 they must be assembled and reported independently; no numerical zero is forced and no threshold or old failure is changed.

## 3. Finite chart repair and its exact limitation

For chosen chart R,V,angular fields, define Psi=R-hV and Phi=Psi-2(rg*p+rn*Nnu)/q². This enforces shear without forcing a separate Phi-series or changing R. A common density shift (Gamma_phi,Gamma_b,Gamma_gamma,Gamma_nu)→(Gamma_phi+lambda,Gamma_b+lambda,Gamma_gamma+4lambda/3,Gamma_nu+4lambda/3), with lambda=-N/[b+4(rg+rn)/3+w+(KB/2)*q²*cs], enforces the finite normal constraint and preserves relative density entropies, U/wn/W,V and modal positions/velocities. It also changes n by -cs*lambda and P by -(KB/2)*q*cs*lambda; sigma must be reconstructed from the full reaction equation. This is not an exactly current-preserving projection.

If independent N_-2 through N2 coefficient checks cancel, the normal truncation remainder begins at a³ and lambda begins at a⁷, beyond the retained density orders. This formal ordering does not supply a numeric remainder bound. Higher raw Phi/Psi/V jets, complete incoming angular history, full finite source/trace/momentum/domain and phase/native first-jet checks remain required. The finite degree4 initial angular polynomial is not a persistent F5=0 closure under the actual Volterra transport. A separately frozen short two-start test can assess this declared preparation; it cannot promote the original full-run failed flags, microscopic phase birth, physical plasma or observed galaxies. No state or test packet is constructed here.

## Exact resident inputs

| Input | SHA256 |
|---|---|
| CONSTRAINED_U_K10_DENSITY_CURRENT_AND_ANGULAR_COMPLETION_V001.md | c0bb7fc0f58c587fb0182383c894116ff1908533cfa6ad1e754dcf5232edfa4f |
| CONSTRAINED_U_K10_COMMON_DENSITY_AND_CURRENT_REGULAR_JETS_V001.md | dcfdf786cd6cdc80ff6182db84d4562a1b0a16150b329fcda8bc5e866fc38282 |
| CONSTRAINED_U_K10_REGULAR_METRIC_COMPLETION_V001.md | e5d638570320830f5edbdc7390af23819a930474733e6441c70f0536a2752d5f |
| constrained_u_galaxy_horizon_stable_y_gauss_v002.py | f70826091d11c38715c00b3a572e08c48a41252018477ac4cf3a20b2ded9f531 |
| constrained_u_clock_gradient_early_transfer_v004.py | a4e78b6467b0ba5884c8da2081ff580378b4afb839a90cec548fcf30a389fa07 |
| CONSTRAINED_U_GALAXY_HORIZON_STABLE_Y_GAUSS_V002_MANIFEST.json | 1def78ccec871fc95e9099b17ee4f05079f95804e51769b9cf3d37fb75904d94 |
| CONSTRAINED_U_CLOCK_GRADIENT_BBN_HELIUM_RECOMBINATION_PAIR_V002_DEFAULT_OUTPUT.json | 07e8e4e7fe524fd9d1f1a19422f293f11a49573f6ee6d1bf016b17c80ec70437 |
