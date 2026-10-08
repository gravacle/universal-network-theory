# Constrained U/clock/gradient: exact reduced chart and retarded source V001

2026-10-06 UTC. NEW analytical continuation of the unchanged inventory V003. The original constrained response completed with status ARITHMETIC_FAILED:471/567 gates passed,96 holonomic-value/first-jet gates failed, while its Einstein/time/spectral controls passed. Those outputs and thresholds stay sealed. This note derives a different exact coordinate chart; it neither projects old saved states nor relaxes old controls. The effective action remains a prospective uncompressed cTheta=0 hypothesis with full fixed physical P(X) budget, ONE matched G and no extra native remainder. No numerical evolution or field fit is performed here.

## 1. Exact chart on the admitted quadratic-action domain

Use V003 notation, c_p=1, L=Qq>0, s=cs², Gamma=d+3HV, Z=sum w_i z_i, Zd=sum w_i zd_i. On the actual longitudinal quadratic holonomic constraint choose independent state coordinates (Phi,ordinary fluids,d,V,ALL z_i,zd_i) and define

    v=Z/L, pi_U=V-v,
    vd=(Zd-Ld*v)/L,
    n_U=vd-s*Gamma,
    Ptot=M²KB q*n_U+M²C Z.                            (1)

This is the regulated quadratic longitudinal chart; a finite-amplitude covariant constraint needs its actual nonlinear metric/encoder contacts. The Bernoulli row Vdot=Phi+s*Gamma then gives pi_U_dot=Phi-n_U. Thus the two old first-order coordinates pi_U/Ptot were redundant on the constraint and its tangent. The physical relative field is v, evaluated directly from Z/L; it is not reconstructed by subtracting nearly equal V and pi. Reconstruct pi only for output. All finite modes and their initial positions/velocities remain. This is an initial-data/action pullback, not a time-step projection or numerical loss of a physical excitation.

For fixed background, the pulled-back velocity form is

    D_phi*(delta Vdot)²
       +M²KBq²*(delta Vdot-sum w_i delta zd_i/L)²
       +M²C*sum w_i*(delta zd_i)²/omega_i².            (2)

It is strictly positive/full rank for q,Q,D_phi,KB,C,w_i,omega_i positive in the admitted finite regulator. A moving background adds the actual Ld/Ldd contacts in(1), not a new inertia. The original constrained phase-space codimension is two, exactly matching removal of these two first-order coordinates. No infinite-continuum or full-gravity stability theorem follows.

The Euler chain rule makes the equivalence explicit. At fixed L, E_V,reduced=E_V+E_pi and E_zi,reduced=E_zi-w_i E_pi/L. Solving the omitted normal Euler reaction for sigma then restores the original phase and mode equations; it does not minimize their kinetic energy. Actual time/metric variations of L and all unit-normal/multiplier contacts remain.

## 2. Same reaction and independent omitted Euler check

Let alpha=sum w_i omega_i², R1=sum w_i omega_i² z_i and Bq=1+ell²q². The same mode and phase equations give

    Zdd=-3H Zd-Bq R1+alpha*(q*n_U+sigma),
    d_dot=3Psi_dot-q²V-M²C Qq*sigma/W,
    Vdot=Phi+s*Gamma.

Differentiating(1), not subtracting the old redundant variables, yields

    vdd=(Zdd-2Ld*vd-Ldd*v)/L,
    n_dot=vdd-s_dot*Gamma-s*(d_dot+3H_dot*V+3H*Vdot),
    Ptot_dot=M²KBq*(n_dot-H*n_U)+M²C Zd.              (3)

The omitted equation is Ptot_dot+2HPtot+M²C Q*sigma=0. Its sigma coefficient is the same positive V003 denominator

    Delta=alpha+C Q²/KB+M²C Q²q²/D_phi.               (4)

Hence the original full-Hubble sigma formula is exactly the reduced-action reaction; no coefficient, source, initial physical seed or pole changed. Initial zero-mode d/V/fluid seeds reconstruct the original pi/P seeds exactly. The holonomic value and first jet in this chart are construction identities, so passing them is NOT independent evidence of preservation. A NEW implementation must separately evaluate(3) using the actual mode accelerations, phase rows and background derivatives and check the omitted normal Euler with a prospectively fixed natural-term denominator. Einstein conservation and full time/spectrum refinements remain separate controls. Original96 failures retain their classification.

## 3. Exact local H=0 two-source retarded response

Freeze positive Q,W,D_phi, mode coefficients and proper q over a controlled local window. This is the nongravitating material resolvent about the charged background, not a global flat solution with its positive mean stress removed. The actual zero-incoming retarded mode state is specified; arbitrary incoming mode/coherent preparation is a separate forcing term. For real positive Laplace rate lambda define

    F=integral_0^1 2r³/[lambda²/omega_max²+Bq*r²]dr,
    gamma=M²C Q²/W, U=q²Phi-3lambda²Psi,
    T=CQ*(lambda+Q/F),
    Dp=(CQ²/F+KB lambda²)*(lambda²+s*q²)
                       +gamma*s*q²*lambda²*(C+KB/F). (5)

Use the finite quadrature analogue of F when that is the chosen regulator. It retains the actual inertia and ell gradient. Its continuum form is F=1/Bq-A*log(1+Bq/A)/Bq², A=lambda²/omega_max². The exact response is

    n_U=s*T*U/Dp, v=s*(CQ-KB lambda)*U/Dp,
    d=-(CQ²/F+KB lambda²)*U/Dp,
    V=(Phi+s*d)/lambda, pi=(Phi-n_U)/lambda,
    sigma=-s*Qq*lambda*(C+KB/F)*U/Dp,
    Ptot=M²q*s*CQ²*(C+KB/F)*U/Dp.                    (6)

These follow from lambda*v=n_U+s*d, Z=Qqv=F(q*n_U+sigma), the actual normal-current row and the actual 3Psi_dot phase-volume source. Dp>0 for real lambda>0 on this branch. Positivity of this denominator is not a self-gravitating Jeans analysis or a general nonlinear ghost criterion. Retarded Fourier continuation uses lambda=-i omega+0 and the original modes/branch/initial data; a frequency inverse never discards their poles.

For lapse-only forcing Psi=0, the zero-rate fixed-q limit is n_U/Phi=1, v=F(0,q)Phi/Q, d=-Phi/s and V=0. At small positive rate n_U/Phi=1+F(0,q)lambda/Q+o(lambda): a passive driven normal response can exceed one. The cross-removal ceiling is therefore not a bound on this faithful action. More precisely, inventory V003 Eq11 is exact for Psi_dot=0, or a controlled leading subhorizon neglect of the phase-volume term; its full two-source numerator is s*(q²Phi-3lambda²Psi). This precision leaves the old frozen inventory and the full-Psi numerical equations unchanged.

## 4. Energy, actual source contacts and scope

Evaluating the positive SOURCE-FREE quadratic material norm along the forced real-Laplace response gives

    E_free=[(D_phi lambda²+Wq²)V²
       +M²KBq²lambda²*pi²+M²C Q²q²*v²/F]/2.          (7)

The mode term is obtained by summing EVERY mode's kinetic plus potential energy: z_i=omega_i²(q*n_U+sigma)/(lambda²+Bq omega_i²), and sum w_i(lambda²/omega_i²+Bq)z_i²=Q²q²v²/F. This is an exact forced-response identity, NOT a static minimum applied to kinetic energy. The underlying mode state is retained.

Equation(7) is not the complete inclusive Hamiltonian with nonzero imposed metric sources. Those sources have actual contacts/work. For example, in the explicit H=0 chart N=1+Phi,g_ij=(1-2Psi)delta_ij, the pressure block contains

    L_P^(2)=D_phi*(Vdot-Phi)²/2-Wq²V²/2
             -3W*Psi*(Vdot-Phi)
             +P0*(-3Phi*Psi+3Psi²/2),                (8)

with its actual background/linear energy and pressure terms retained. Maxwell supplies M²KBq²(Phi-pi_dot)²/2 and the mode source supplies M²C q(Phi-pi_dot)Z. Their lapse-squared, mean-stress and mixed source contacts cannot be omitted. Different source coordinates carry their own background-stress chain-rule contacts. The inclusive canonical source work is dH_can/dt=-L_Phi*Phi_dot-L_Psi*Psi_dot plus any other explicit source work, using the COMPLETE action. The perturbation frame about physical phase Q also retains its charge/reference contribution and full absolute P energy; no energy zero is chosen. Positive(7) does not establish positive complete gravitational energy or free preparation.

The exact material loading is delta rho=W*d-qPtot, delta p=s*W*d and momentum W*V. A finite-rate common field must solve the actual Einstein/source constraints with these terms and ordinary matter. Setting lambda=0 and adding an unowned background subtraction is not a valid self-gravitating structure calculation. At lambda comparable to H, use the full FLRW equations rather than this frozen-window formula. The new reduced chart permits that same finite calculation without redundant-potential cancellation; it does not repair the separately failed stationary physical-phase domain or earn observational agreement.

## Frozen direct inputs

| Input relative to J | SHA256 |
|---|---|
| INVARIANT_CLOCK_GRADIENT_SHARED_ACTION_BUDGET_DOMAIN_AND_NORMAL_V003.md | e08b7166892ec59c863539d59b8d4b89c654081776d8870239ecc2c382572da0 |
| constrained_u_clock_gradient_flrw_response_v001.py | 0d4961fd3ef20e3994e452a23913cf5956491d027769d171ccc23f78e821378a |
| CONSTRAINED_U_CLOCK_GRADIENT_FLRW_RESPONSE_V001.md | 5d4a7abceca7f005ac9efd95bc2638ae94dd8eb8b0992ea80793193a079c55b2 |
| CONSTRAINED_U_CLOCK_GRADIENT_FLRW_RESPONSE_V001_RESULT.json | 0fbbf7a2dc89231da78f31b76e3325bb62e502adfb34ff916c03e81bb5c653f3 |
| CONSTRAINED_U_CLOCK_GRADIENT_FLRW_RESPONSE_V001_RECEIPT.json | 01c3effb4ea9a793ca2f2cb9e996f39e343cdacb6803258f6fa58f4bd89f3afc |
