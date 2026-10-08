# Frozen-ready formed-state response diagnostic

2026-09-27. Analytical specification only; no execution by its author.
Root owns the single numerical worker and its source/protocol freeze.
This does not modify any earlier frozen source or result. Two deliberately
distinct fixtures are used: an already verified exact one-link preparation
calibrates signs, operator order, noise, and preparation dependence; the
already verified full native N=2 formation history instantiates the common
local/homogeneous response in a shared-record graph. They are not one
fixed-coefficient scaling family or two fits to observations.

Inputs, checked resident before reading:

- `record_paid_formation/PROTOCOL.md`, `RESULTS.json`;
- `fixed_coefficient_formation/PROTOCOL.md`, `compute.py`, and the resident
  `FROZEN.json`, `full_native_N2.json`, `RESULTS.json`;
- `NATIVE_FORMED_NETWORK_RESPONSE_BRIDGE_V001.md`;
- `NATIVE_FORMED_RESPONSE_NOISE_AND_PROBE_V001.md`;
- the recovered native BS action and connected-carrier note.

## 1. Exact one-link calibration from actual formation

Reuse the old s=3, eta=1/6 fixture, not a newly optimized member:

    hbar=U=1, Delta=4, lambda_R=1/2,
    h=g=sqrt(10)/12,
    a=(sqrt(21)-3)/12, epsilon=(sqrt(21)+3)/12,
    d_star=3/2+a/4, epsilon_w=0, T_star=6pi.

Build the native 18-dimensional formation Hamiltonian, with explicit
tensor order (link, writer, active record), dimensions (2,3,3), qutrit
order (B,0,1). The initial state is
|link=0> tensor (|writer=0>+|writer=1>)/sqrt(2) tensor |record=B>.
All other registers are in their stated invariant blank/fixed sectors.
Evolve to T_star; retain the calculated endpoint, not a manually reset
|n=1> vector. Verify the old exact endpoint and then switch copying off.
The reduced link state and the full 18-dimensional expectations must agree
under H_hold=(C+epsilon)I-epsilon n-hX, C=2d_star^2. In particular, check
the partial trace independently of the analytic endpoint construction.

Define R=sqrt(epsilon^2+4h^2), omega_0=R, L=4h^2/R^2. Use four waiting
phases phi=0,pi/2,pi,3pi/2 with w=phi/R and four lag phases of the same
values with u=phase/R. No age is chosen using its response. Predictions:

    m(w)=1-L sin^2(Rw/2),
    chi(w+u,w)=2h^2 epsilon/R^3
       *{[1-cos(Rw)]sin(Ru)+sin(Rw)[1-cos(Ru)]},             (1)
    S(w+u,w)=1/4{1-L+L cos(Ru)-z(w+u)z(w)},
    z(t)=1-L+L cos(Rt).                                    (2)

### Source sign and initial-operator order

The diagnostic source is -f(t)n. Its dimensionless pulse area theta gives
U_kick=exp(+i theta n), not exp(-i theta n). For rho_w and
n(u)=exp(+iH_hold u)n exp(-iH_hold u), form

    Q_conn=Tr[rho_w n(u)n]-m(w+u)m(w).

The rightmost n acts first. This is an unordered correlation, not a
normalized conditional/projective measurement. Directly compare

    Re Q_conn=S,       -2 Im Q_conn=chi,
    i Tr[rho_w(n(u)n-n n(u))]=chi.                         (3)

Independently propagate the two kicked states with theta=+/-0.001 and
measure m_+(u),m_-(u). Since n is a projector, exactly,

    [m_+(u)-m_-(u)]/[2 sin(0.001)]=chi(w+u,w).              (4)

There is no finite-pulse truncation error in (4). In general units its
right side is hbar*chi. The zero response at w=0 concerns an endpoint
impulse; it does not assert zero response to a detuning left on later.

### Noise asymmetry and the stationary comparator

The uniform mixture of these four actual age states is exactly the
energy-dephased two-level state; no numerical dephasing bath is applied.
Check that mixture against the two energy projectors. Its predictions are

    m_bar=1-L/2,
    p_g,e=[1+/-sqrt(1-L)]/2,
    Q_bar(u)=W_0+W_+ exp(-iRu)+W_- exp(iRu),
    W_0=L(1-L)/4,       W_+=L p_g/4,       W_-=L p_e/4.     (5)

Extract these three weights independently both from energy-projector
matrix elements and the four-point discrete Fourier transform of the
direct unordered correlation. With Q(omega)=integral exp(i omega u)Q(u)du,
W_+ is the positive-frequency weight. Check

    W_-/W_+=[1-sqrt(1-L)]/[1+sqrt(1-L)],
    chi_bar(0)=2(W_+-W_-)/R,
    R chi_bar(0)=(L/2)sqrt(1-L).                            (6)

The static susceptibility can separately be assembled by the spectral
Kubo sum. Also check the nonzero below-gap frequency omega=R/2 against
2h^2 epsilon/{R^2[R^2-omega^2]}. Do not infer static response by changing
the preparation populations. Distinguish the directly mixed connected
noise from the average of individually connected pure-state noises:

    S_bar(u)-average_w S(w+u,w)=(L^2/8)cos(Ru).             (7)

### Preparation derivative is not fixed-population susceptibility

This comparison leaves the original formation pulse and actual endpoint
unchanged. For each post-formation detuning x=epsilon+f, phase-average the
hold starting from that same endpoint using its own period. This prepares
a different mixture; it is not a rerun of a detuned formation protocol.
Its mean is 1-2h^2/(x^2+4h^2), so

    d m_bar(x)/dx|epsilon=4h^2 epsilon/R^4=2 chi_bar(0).     (8)

An independent derivative check uses the eigenprojectors P_a of H_hold:

    P_a'=sum_(b!=a)[P_b(-n)P_a+P_a(-n)P_b]/(E_a-E_b),
    p_a=Tr(P_a rho_F),       n_a=Tr(P_a n),
    d m_bar/dx=sum_a [Tr(P_a' rho_F)n_a+p_a Tr(P_a'n)].     (9)

For the actual formed endpoint, each of the two sums in (9) separately
equals chi_bar(0): population redistribution supplies exactly the extra
factor. Keeping p_a fixed and changing only eigenprojectors is the
adiabatic fixed-population protocol. This avoids differentiating two
nearly equal scalar probabilities. An optional finite-change cross-check
at delta=R/16 and R/32 has the exact central quotient

    [m_bar(epsilon+delta)-m_bar(epsilon-delta)]/(2delta)
      =4h^2 epsilon/{[(epsilon+delta)^2+4h^2]
                                    *[(epsilon-delta)^2+4h^2]}. (10)

Use the exact finite expression, not an arbitrary finite-difference error
tolerance against the zero-step derivative.

## 2. Actual full N=2 state: no ideal endpoint or fixed-background row

Reuse every coefficient from `fixed_coefficient_formation/PROTOCOL.md`:

    hbar=U=1, Delta=6, lambda_R=2, epsilon_r=1,
    d_star=7/4, g=1/10, Omega=1/20, N=2, h=1/40,
    t_hop=1/2, lambda_J=0, epsilon_w=0.

Four edge bits are (x,y,u,v)=(a0-b0,a0-b1,a1-b0,a1-b1).
The active record is q=q_a1; q_b0=1 and q_a0=q_b1=0.
Index the active basis by 2*mask+q with x,y,u,v the successive
least-significant bits. Initial state is index 2: x=1,y=u=v=q=0.
All four flips remain active. The diagonal energy is

    E=6(x+y+u+v)+sum_d(d-7/4)^2+(1+q)
                         -2[x+(1+q)u+qv],
    d=(x+y,u+v,x+u,y+v),                                  (11)

and off-diagonals are -h per link flip, +g per active-record flip.
The complete initial energy is C2=49/4. Assemble this Hamiltonian directly
from both bit energies and native tensor operators; do not import an
isolated four-state or frozen-row Hamiltonian.

Use the already declared N=2 isolated timing solely to specify three
formation durations, not as a success claim about the full graph:

    R_plus=sqrt(1+4(g-h)^2), R_minus=sqrt(1+4(g+h)^2),
    Rbar=(R_plus+R_minus)/2, DeltaR=8gh/Rbar,
    k=floor(Rbar/DeltaR), T=pi(2k+1)/Rbar,
    t_form in {T/2,T,2T}.                                  (12)

Compute T from (12), not its rounded reported decimal. For EACH duration
retain its complete actual 32-component state. Switch copying off, with

    H_hold=H_form-g X_q,
    W_stop=-g<X_q>_formation,
    <H_hold>=C2+W_stop.                                    (13)

W_stop need not be nonnegative in this full graph. The positivity proved
for the isolated channel must not be copied here. Keep q coherences and
all record sectors; replacing q by its expectation is not an exact hold.
Use fixed waiting times w=0,1,4 and lags u=1/2,2 in these native units.
No timing, graph outcome, source vertex, or record sector is optimized.

## 3. Same kernel tested by local sources, uniform sources, and carriers

At every declared (t_form,w,u), calculate the actual matrix

    chi_ef=i Tr rho_w[n_e(u),n_f],                          (14)

for all 16 edge pairs. Keep the signed entries, not their absolute values.
No stationarity, passivity, reciprocity chi_ef=chi_fe, or positivity is
assumed. Compare (14) to all four exact projector source kicks (4), using
each n_e as the readout. Compute connected Q_ef independently and verify
chi_ef=-2 Im Q_ef. Check equal-time occupation covariance is positive
semidefinite within roundoff; this does not make the retarded matrix PSD.

With vertex order (a0,a1,b0,b1), use the independently assembled incidence
matrix

    C=[[1,1,0,0],[0,0,1,1],[1,0,1,0],[0,1,0,1]].

For a record-equivalent source -lambda_R j D_v, D_v=sum_e C_ve n_e,
the fixed source prediction is Phi=C chi C^T, with

    delta mu_v^op/delta j_w=-lambda_R^2 Phi_vw,
    delta kappa_v^out/delta j_w=t_hop^2 lambda_R Phi_vw.    (15)

Here mu_v^op=epsilon_r-lambda_R<d_v>, and the curvature is measured
by a newly injected localized carrier after the source history.
The occupation-cost reading is an actual blank-register insertion-work
coefficient at a0,b1. At a1,b0 it is only the stated coefficient field;
an additional blank-register insertion is not available in every outcome.

Uniform edge source -F M, M=x+y+u+v, predicts

    chi_MM=sum_ef chi_ef,
    mu_bar^op=epsilon_r-(lambda_R/2)<M>,
    kappa_bar^out=(t_hop^2/2)<M>.                          (16)

Uniform vertex source j corresponds to F=2lambda_R j, not F=lambda_R j.
Compare these projections with independent finite uniform-M and vertex-D
kicks. M and D are NOT projectors: do not divide their central responses
by 2sin(theta). For generator G=M or D use

    D(theta)=[O(+theta)-O(-theta)]/(2theta),
    D_R=[4D(theta/2)-D(theta)]/3,
    theta=0.0002, theta/2=0.0001.                          (17)

The source is -fG; multiply by lambda_R only when converting the D
response to the record-equivalent j source. If G has spectrum in [0,m],
the Richardson truncation obeys

    |D_R-i<[O(u),G]>| <= m^5 ||O|| theta^4/288.             (18)

Indeed shifting G by m/2 leaves its commutators unchanged and bounds
the fifth derivative by m^5||O||; a fourth-order Taylor remainder in
the two central differences gives (18). Here m<=4 and ||O||<=4.
Roundoff is checked separately against the frozen 1e-8 tolerance.
Optionally an exact discrete Fourier derivative uses 2m+1 kick phases;
it is not needed for the minimum worker.

Independently build the full native one-carrier Hamiltonian of dimension
32*4=128, with carrier order (a0,a1,b0,b1), epsilon_psi=0, t_hop=1/2,
lambda_J=0, and no formation couplings. Do not propagate a guessed
mean graph. For an initial fresh carrier at a and a different site b,
evaluate the projected first-order amplitude B_ba=<b|H_carrier|a> on the
32-dimensional state and score

    kappa_(a->b)=Tr(B_ba rho_w B_ba^dagger)
                 =t_hop^2<n_(ab)>                         (19)

for adjacent-layer sites, zero for other distinct sites. This is the
exact quadratic coefficient with every native flip retained, not a
finite-time approximation or a division by a small transfer probability.
Sum over b for the vertex curvature and check (15)-(16), including after
the declared source kicks. Source/injection work is not discarded:
record Tr[H_hold(rho_kick-rho_w)] for the kicks; the declared localized
carrier has zero mean injection energy for epsilon_psi=lambda_J=0.
That is not a claim of a free preparation/controller.

## 4. Inclusive connectivity and honest interpretation

At each formation duration and each held time w=0,1,4, score all outcomes
without postselection. The Boolean connection indicators are

    C_source=u+(1-u)xyv,
    C_other =v+(1-v)xyu,
    q(C_source-C_other)=q(u-v)(1-xy).                       (20)

C_source connects a1 to b0 either directly or through the three-edge
alternative path; C_other similarly connects a1 to b1. Report
<q C_source>, <q C_other>, their contrast, <q>, <M>, all four occupations,
and the existing exclusive path/seed basis probabilities. Verify (20)
as an exact bit identity before taking expectations. Do not divide by
<q>, discard failed outcomes, equate exclusive target probability with
connectivity, or call q=1 a completed semantic-record certification.

Check held <q> and full energy C2+W_stop at every age, but allow graph
connectivity and kernel signs to evolve. Neither more source connectivity
nor positive/passive response is a predeclared success requirement.
The measured common kernel is a prediction of this actual shared-record
history, not evidence of a universal metric, physical expansion, or
successful macroscopic graph growth.

## Numerical check separation

Freeze source and protocol before launching one root-owned worker. Keep
previous frozen evidence unchanged. The following are separate gates:

1. Native Hamiltonian/basis construction, actual formation, partial trace,
   and complete switch/hold energy ledger.
2. One-link analytic age kernel versus commutator versus exact source kick.
3. Unordered noise order, spectral/DFT asymmetry, connected-subtraction
   distinction, and the two independently differentiated preparation terms.
4. Full32 actual kernel versus projector, vertex, and uniform sources.
5. Full128 projected carrier amplitudes versus occupations and the common
   insertion-cost/transport projections.
6. Inclusive connectivity bit identity and unconditioned time readouts.

Use absolute identity tolerance 1e-8 throughout this prospective worker;
exact bit identities remain exact. This is numerical verification tolerance,
not an observational acceptance threshold. Emit per-gate residuals and
per-formation receipts so a failure is attributable and retained. Do not
reinterpret an unexpected physical sign or low formation probability as a
numerical failure. No sweep, fitting, new parameters per N, or second
numerical worker is requested by this specification.
