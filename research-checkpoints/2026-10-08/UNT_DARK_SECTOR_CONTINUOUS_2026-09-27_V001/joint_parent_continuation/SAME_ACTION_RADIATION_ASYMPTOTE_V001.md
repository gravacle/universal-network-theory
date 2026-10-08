# The same present action fixes an early radiation coefficient

2026-09-29. Analytical consequence of the adopted positive mode parent and
I_j(A)=A^3 I_j(1), A=a^-1. No new state, gap, abundance, preparation or numerical
worker is introduced. This strengthens the already completed dilution census
with a closed coefficient and a finite-A error certificate.

## 1. Exact quartic coefficient, including normalization

For one mode with

    H=p^2/(2m)+k y^2/2+u y^4/4,       m,u>0, k>=0,

use the same I=(1/(2pi))oint p dy. At k=0, b0=(4e0/u)^(1/4), and direct
integration gives

    I=[sqrt(m)/(pi u^(1/4))] B(1/4,3/2) e0^(3/4),
    e0(I)=C I^(4/3),
    C=[pi/B(1/4,3/2)]^(4/3) u^(1/3)/m^(2/3)
     =[(3sqrt(pi)/2) Gamma(3/4)/Gamma(1/4)]^(4/3)
                                      u^(1/3)/m^(2/3).          (1)

There is no extra factor of two from the signed orbit versus a nonnegative
radial coordinate. All42 retained templates use m=u=1, so the bracketed Gamma
constant alone is their C. For each saved mode define

    q_j=C I_j(1)^(4/3),
    Q=sum_j w_j q_j,
    D=sum_j w_j k_j sqrt(q_j/u).                              (2)

Q is a fixed functional of the actual saved actions, not a new radiation
population or adjustable normalization.

## 2. A finite-gap bound proves convergence without an asymptotic guess

At fixed action, adding the positive quadratic potential raises the energy:
e_k(I)>=e0(I). Also compare actions at the trial energy

    e_trial=e0+k b0^2/2.

For every |y|<=b0 its kinetic radicand is
(e0-u y^4/4)+k(b0^2-y^2)/2, no smaller than the pure quartic one. Its turning
point is exactly b0. Therefore its action is at least I, and monotonic I_e>0
implies the upper bound

    e0(I)<=e_k(I)<=e0(I)+k sqrt(e0(I)/u).                      (3)

Independently, the positive angle formula for I_k(b) increases with k at
fixed b, so the actual b_k(I)<=b0(I). The exact virial relation is

    e_k-3p_k=k<y^2>,
    0<=e_k-3p_k<=k b0^2=2k sqrt(e0/u).                       (4)

Substitute I_j(A)=A^3 I_j(1). Summing the positive weights proves

    A^4 Q <= E(A) <= A^4 Q+A^2 D,
    0 <= E(A)-3P(A) <= 2A^2 D.                              (5)

In particular,

    E(A)/A^4 -> Q,
    P(A)/A^4 -> Q/3,
    0 <= E(A)/(A^4 Q)-1 <= D/(A^2 Q),
    0 <= 1/3-P(A)/E(A) <= 2D/(3A^2 Q).                      (6)

These bounds are exact for the specified action-scaled states, not fitted
remainders. To certify fractional energy error at most epsilon_rad, it is
sufficient that A>=sqrt[D/(epsilon_rad Q)]. No sharpness is claimed. For the
saved finite sums Q,D are finite. A continuous or unbounded-gap extension
must separately establish their convergence before reusing this certificate.

For common u, Cauchy-Schwarz also gives
D^2<=Q*sum_j w_j k_j^2/u. This links the radiation convergence scale to the
previous S4 capacity bound, but the direct sum D is sharper and already known
from each saved state. No new turning-point solve is required.

## 3. The present calibration fixes its radiation normalization

Let the SAME stress normalization be Nstress, with present excitation
rho_exc,1=Nstress E1 and E1=sum w e_j(I_j(1),0). The unchanged matched constant
has separate rho_vac=Nstress DeltaU. Then

    rho_exc(A)=rho_exc,1 E(A)/E1,
    rho_exc(A)/A^4 -> rho_exc,1 Q/E1.                         (7)

If a declared present reference calibrates rho_exc,1/ rho_crit,1=Omega_exc,1,
the resulting extrapolated radiation coefficient is

    Omega_extra_rad,asympt = Omega_exc,1 Q/E1,                (8)
    0<=rho_exc(A)/(rho_crit,1 A^4)-Omega_extra_rad,asympt
                          <=Omega_exc,1 D/(E1 A^2).

This is an asymptotic coefficient in PRESENT critical-density units, not a
claim that today's modes already have radiation pressure. Their actual present
pressure remains the saved P1/E1. Nor is it an independently fitted extra
radiation abundance. The dimensional stress factor, Kb and g_star cancel only
because the same state and same present calibration are used on both sides.

For all36 original templates, apply (8) to ALL18 already-declared reference/
BBN alternatives from the original-spectrum calibration. Its late-time flat
reference omitted radiation and is conditional, not a new cosmological fit.
For each of the six extended pulse spectra, Q/E1 is equally definite, but an
assigned Omega_exc,1 remains an explicitly conditional present normalization:
the soft-only matching cannot be silently reused as a completed calibration
of its changed spectrum. The same-parent DeltaU must remain intact.

An independently specified ordinary-radiation normalization Omega_rad,ref would
give the dimensionless early ratio Omega_extra_rad,asympt/Omega_rad,ref in the
shared A^-4 epoch. No photon temperature, neutrino conversion or observational
limit is inserted here. If this extra density is material in a standard-BBN
epoch, the baryon benchmark inferred using standard expansion must be checked
again; it cannot simultaneously be treated as an independent native output.
Radiation-like mode pressure does not establish photon production, a blackbody
spectrum, the observed CMB or its angular/acoustic statistics.

## 4. How a hard gap changes the coefficient at fixed owned present energy

For one hard gap R with fixed weight beta and fixed present weighted energy
E_H1=beta e1, the harmonic present regime e1/R^4<<1 gives

    I1=e1/R [1-3e1/(8R^4)+O(e1^2/R^8)],
    Q_H=C beta I1^(4/3),
    Q_H/E_H1=C [E_H1/(beta R^4)]^(1/3)
                          [1+O(E_H1/(beta R^4))].             (9)

The reduction with R is not just a harmonic approximation. At fixed e1,
I_R=-R<y^2>/omega. Since I omega=e1+p1 and R^2<y^2>=e1-3p1,

    d ln Q_H/d ln R = -(4/3)(1-3w1)/(1+w1),   w1=p1/e1.      (10)

It lies between -4/3 and zero. Thus a higher gap can reduce the radiation
coefficient while retaining a specified present energy; in the cold present
limit it scales as R^(-4/3), not R^(-4). This is a prospective design relation,
not permission to alter any of the six stored states. An actually changed
gap needs a new preparation/work and matched-baseline ledger. Adding spectral
weight also changes Kb; moving fixed weight between gaps does not.

The earlier cold-history result makes the tradeoff explicit. Let r=b^2/R^2,
epsilon(r)=r/2+r^2/4, I=R^3 f(r), and r_c solve w(r_c)=w_c. Define
r_req=f^-1[f(r_c)/A^3]. Then remaining cold through A requires r1<=r_req,
and

    Q_H/E_H1=C f(r1)^(4/3)/epsilon(r1)
             <=C f(r_req)^(4/3)/epsilon(r_req).              (11)

The monotonicity used here is exact:
d ln[e0(I)/e(I)]/d ln I=1/3-w>0. In the cold-threshold, large-A regime,

    Q_H/E_H1 <= approximately C (8w_c/3)^(1/3)/A.            (12)

Equation (11), rather than its expansion, controls a finite specified case.
The complete pulse state must also include its retained soft-mode contribution
to Q; small present soft energy is not a license to delete it from this sum.

## 5. The action/clock domain remains a physical condition

The coefficient Q is mathematically exact under the stated action scaling.
Using it as an actual early-universe prediction additionally needs the owned
isotropic/triad state, physical volume/clock mapping and rapid-mode/adiabatic
conditions already recorded by the dilution census. Neither a low present
pressure nor large R alone proves those conditions at every earlier epoch.

For example, IF the conditional solution is radiation dominated,
H(A) is proportional to A^2, whereas each quartic mode frequency approaches

    omega_j(A)=A*(4C/3) I_j(1)^(1/3)

in internal time units. Thus H*tau_star/omega_j grows proportionally to A for
fixed tau_star. Taking the formal A->infinity limit is not proof that the
adiabatic physical history remains valid to infinity. At any proposed finite
A use the actual clock-rate bounds; no late-time radiation-omitted H0 history
is inserted at A=1101, and no new extreme-BBN extrapolation is authorized here.

## 6. Minimal complete numerical application, with no new dynamics

The parent can calculate only Gamma functions and positive sums for each of
the36 `PREPARED_ACTION_RETURN_V001_RESULTS.json` rows and all six
`HIGH_GAP_PULSE_V001_RESULTS.json` fine states. Read their actual actions,
delta and weights, use k=delta^2, and retain E1,Q,D,Q/E1 and soft/hard splits
where applicable. Compare the already saved252 dilution rows to the two
certificates in (5), retaining all original resolutions and every case.

For the original calibration, pair ALL36 states with all18 old reference rows;
do not infer new Omega_exc values from the radiation result. For the six pulse
states, label the same18 normalizations as conditional reference comparisons,
not existing completed extended-spectrum fits. This gives a cheap exact early
density consequence and a stated finite-gap error without a new ODE, action
root, new parameter, selected source or galaxy/CMB residual fitting.
