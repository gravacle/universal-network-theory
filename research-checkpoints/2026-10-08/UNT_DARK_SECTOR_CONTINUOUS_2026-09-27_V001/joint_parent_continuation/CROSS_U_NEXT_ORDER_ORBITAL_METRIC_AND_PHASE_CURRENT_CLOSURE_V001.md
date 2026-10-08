# S_cross next-order orbital metric and phase-current closure V001

2026-10-06 UTC. Accepted analytical companion after root and independent readonly FULL96/eight-input reviews. No field, Green kernel, numerical operator, metric, force or current has been evaluated. The static source and all old qualifications remain their evidence. This packet adds a concrete lapse-source and modal correction to the accepted Hilbert/orbit interface, with a distributional route to force; it does not select a dynamic state, boundary metric or favorable source.

## 1. What the actual saved branch contains

Use original V003 Eq(5), signature(-,+,+,+), g=M^2 C=2M_N^2, C=2-KB, and ordinary minimal metric coupling. On the declared zero-shift aligned static branch, ds^2=-N^2 dt^2+h_ij dx^i dx^j, U=N^-1 partial_t, phi=omega t. Thus X=omega/N, r=P_U dphi=0 and

    J_phi^mu=P_X v_phi^mu-g r^mu=n U^mu,
    v_phi^mu=-partial^mu phi/X, J_phi^i=0.                         (1)

The positive charged P family supplies n=P_X(X). Its inhomogeneous rho_phi=XP_X-P and pressure P are already included as delta rho_phi+3delta P in core.Model.clock/residual (lines123,138). Neither P nor a native stress tensor is an additional force on ordinary matter. Static phase conservation is compatible with (1); it does not provide an independently chosen spatial current or microscopic particle registration.

Saved native mode coordinates have zero declared time-projected velocity on this branch. They contain quadratic spatial/connection stress and polarization in the lapse source, but do not supply independent modal momenta, phase gradients, a tilt or an ordinary rotating-matter current. A dynamic continuation must solve them jointly: div J_phi=0, phase integrability, the projected U/mode rows and all Einstein constraints. Assigning J_phi^i from the saved density alone changes the state and, through X and Y, its Hilbert sources. No such state is earned by a converged static lapse.

## 2. The computable omitted native active source

Let x be the existing1kpc spatial chart, B0=a0 L0/c_p^2, Phi0=B0 psi, a_*=grad_x psi and u_j=z_j/(a0/c_p^2). The code stores sqrt(w_j)u_j, with the same32 positive weights/labels. Write G_j,ki=D_k u_j,i with the full cylindrical connection; for meridional vectors G_phi,phi=u_R/R. Define

    A_*=KB|a_*|^2/C+sum_j w_j[
          |u_j|^4/(2 gc_*^2 xi_j^4)+ell_*^2|D u_j|^2+a_*.u_j],
    F_kij=sum_j w_j[u_j,k S_j,ij-u_j,i S_j,jk-u_j,j S_j,ik],
    S_j,ij=(G_j,ij+G_j,ji)/2, J_*,k=F_kii,
    Q_*=A_*+ell_*^2 div_x J_*+B0 ell_*^2 a_*.J_*.                (2)

Here gc_*=3pi/8 and ell_*=ell/L0 in the inherited a0 chart. The native quadratic rho+spatial-trace source is g B0^2 Q_*/L0^2; its linear M^2 KB div a+g div Z terms were already used in the leading lapse equation. The flux divergence in (2) is distributional for the Q1 fields, including their interior and reflected sheet contacts.

The saved meter point/volume_order (lines169,227) independently constructs A_*=rho_quadratic+trace(bulk), J_*=traceflux, and its complete weak load. For any admissible scalar test eta over the reflected finite domain D,

    Q_*[eta]=integral_D[A_* eta-ell_*^2 J_*.grad eta
                 +B0 ell_*^2(a_*.J_*)eta]d^3x
               +ell_*^2 integral_outerD(n.J_*)eta dS.            (3)

Use actual R dR dZ volume measures, azimuth and midplane reflection, and actual outer face measures. The original mode mask makes the saved outer native improvement zero, but its signed port must remain authenticated. Do not add sheet/internal deltas again to (3). Isotropic phase pressure is absent from the tracefree slip projection; it is present in the independent lapse/trace budget.

## 3. Lapse correction and the omitted mode equation contact

The exact static lapse identity is 2M^2 Delta_h N/N=rho+T^i_i. Even in a fixed flat coframe, Delta N/N=Delta Phi+|grad Phi|^2. After the already included linear Maxwell/polarization contacts are moved to the left, the extra dimensionless original Gauss source is

    B0 [Q_*-2|a_*|^2/C].                                       (4)

It is exactly the saved native_plus_flat_geometry_load=B0*(active+geom) (meter line283), with the actual outer port retained. The core residual uses positive source plus weak gradients: its ADDITIONAL residual is +B0 weak[Q_*-2|a_*|^2/C], and a linear correction solves H_original delta=-that residual. The signs of the two statements differ; the physical Hessian retains its negative clock mass.

There is also a mode contact absent from the leading flat solver. Varying the pulled action integral N sqrt(h)[-U_j-ell^2|D z_j|^2/2+a.z_j] gives, in this fixed flat coframe,

    f_j u_j-ell_*^2[roughDelta u_j+B0 a_*.D u_j]=a_*,
    f_j=1+|u_j|^2/(gc_*^2 xi_j^4).                              (5)

The drift is -B0 ell_*^2 a_*.D u_j in the strong mode residual. It is of the same correction order and is not a scalar Laplacian for u_R. Spatial-metric changes add their proper inverse-metric/connection and source contacts. Thus the next static response must use the signed coupled scalar/native operator, including the actual D_phi+3W clock susceptibility, plus (4),(5) and the spatial metric contacts. Bare Poisson inversion alone is not that response; its inverse can be strongly affected by the retained clock/native block or a static near-null branch.

## 4. Two defined finite-domain potential contributions, not a closed metric

Put H_y(x)=1/|x-y| and use (3) at eta=H_y(x). The isolated native quadratic contribution to the LINEAR Einstein lapse operator is the particular potential

    Phi_native,E(x)=-C B0^2 Q_*[H_y(x)]/(8pi).                   (6)

The different held-source particular correction of the original Gauss equation, with Z and the clock frozen, is

    Phi_frozen,G(x)=-B0^2[Q_*[H_y(x)]
                         -(2/C) integral_D |a_*|^2 H_y(x)d^3y]
                        /(4pi).                                (7)

The C/2 distinction follows from 2M^2 versus the already reduced g=M^2 C contact. Equations(6),(7) are separately named diagnostic contributions; they are not to be added together. Both keep absolute signs/uncanceled envelopes, and separate all unknown exterior/homogeneous/ordinary/background contributions. Equation(7) still omits the coupled response and (5). No zero boundary potential or empty exterior is physically selected by either particular integral.

The spatial metric uses the accepted interface: Delta^2(Psi-Phi)=3 partial_i partial_j Pi_eff,ij/(2M^2) and Delta gamma_TT=-2 Pi_eff,TT/M^2, with Pi_eff=[T_total-M^2 G_beyond_linear]^TF after the actual background split. Native bulk+full F are available; ordinary stress, nonlinear geometric/background source, static vector compatibility and inherited boundary modes are not supplied by that availability. The ordinary momentum/shift row G_0i=T_0i/M^2 is also required. The zero-shift saved branch is not an ordinary rotating disk's full stationary metric.

## 5. From metric values to orbital force

For a minimally coupled circular orbit, partial_R g_tt+2Omega partial_R g_tphi+Omega^2 partial_R g_phiphi=0 and v_ZAMO=sqrt(g_phiphi)(Omega+beta^phi)/N (coordinate t in the same proper-time convention). In the scalar static chart h_phiphi=R^2 exp(-2Psi),

    v^2/c_p^2=R Phi_R/(1-R Psi_R).                              (8)

The finite potential value in (6) or the scalar-slip value alone therefore cannot establish a force correction. Holding the numerator, a10percent speed increase requires R Psi_R=21/121 relative to the leading code denominator; alternatively it requires a21percent numerator increase when the denominator is negligible. These are requirements on derivatives, not on native tensor/load ratios or tiny potential values. TT changes g_phiphi and shift changes the full orbit equation; neither is determined by the scalar particular solution.

Differentiate the same weak kernels with their distributions, rather than finite-differencing small projected potentials. For n=(x-y)/d,

    partial_xa partial_yb(1/d)
      =-PV[(3 n_a n_b-delta_ab)/d^3]
                       +(4pi/3)delta_ab delta^3(x-y).           (9)

The gradient of the improvement term in (3) needs this local contact; a smooth volume pointwise derivative omits it. Actual Q1 jumps and the mirrored sheet require their same one-sided/PV registration. Differentiated tracefree K/F kernels similarly require their distributional contacts. Strictly positive distances in a finite saved Gauss-point potential calculation avoid point singularities, but do not certify the continuum derivative, sheet limit or a force error. The concrete next force check is a singular-cell/face weak derivative with analytic local subtraction/contact, exact constant/linear source controls and independent spatial/angular convergence under the same original wall. It supplies a derivative of a named native contribution; full orbital closure still requires (4),(5) and all metric/current rows.

No computed source envelope bounds its inverse by itself. No full phase current, ordinary support history, TT/shift/exterior metric,10percent correction or observational success is inferred. The shortest accountable continuation is the authentic active-source potential plus differentiated weak source/contact controls, followed by a same-action coupled metric response with explicit boundary/current data; it does not append an extra stress force to the old readout.

## Protected actual inputs

- INVARIANT_CLOCK_GRADIENT_SHARED_ACTION_BUDGET_DOMAIN_AND_NORMAL_V003.md — e08b7166892ec59c863539d59b8d4b89c654081776d8870239ecc2c382572da0
- CROSS_U_STATIC_HILBERT_STRESS_AND_LEADING_LENSING_INTERFACE_V001.md — 6844c982d0c017350d85731f3f58bf8b4167c860ee52f8bdd238ceef1fdcd68b
- CROSS_U_STATIONARY_AXISYMMETRIC_ORBIT_AND_ORDINARY_MATTER_REGISTRATION_V001.md — b962a4e6cc2583033f66b5194b50d47e1553456feda4147624d9f246bc86ebd5
- cross_u_ngc3198_nonlinear_disk_v001.py — ae4285fc9c19cdf2d8efa176ac3d770b7eaf379a75fa3b9627bc9d3f6f3179e1
- cross_u_ngc3198_saved_weak_stress_meter_v002.py — af1c2f0826380c714220e090f755fc20773c76804f2b0952e1f6400f9cd6eee6
- CROSS_U_NGC3198_SAVED_WEAK_STRESS_METER_V002.md — be14d5467450d17f0cd0d5b2b310d1a21db1cbcb2890859807d7a27ccd101202
- CROSS_U_NGC3198_SAVED_WEAK_STRESS_METER_V002_RESULT.json — d8d7de0d9f2faf7545c400230d116ad1dc2fe3488471982e3c1c01d3aac582c1
- CROSS_U_NGC3198_SAVED_WEAK_STRESS_METER_V002_RECEIPT.json — 12d150e67f3da4f36714e52480d5c7e90f7b7b0fd3dac919787e021503312018

All eight direct input bytes were verified before and after acceptance. Guarded96-line draft063adc97900af4f63e30f4bd5557f8ca4d350be0a0f9085f5de8ffdc59f6b95c is preserved byte-for-byte0444 as reviewed_CROSS_U_NEXT_ORDER_ORBITAL_METRIC_AND_PHASE_CURRENT_CLOSURE_V001_96_063adc97.md. Only acceptance text changed; no numerical or physical qualification.
