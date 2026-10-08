# Exact native finite-memory carrier transport realization V001

2026-09-29. Analytical continuation of the actual held 16D preparations.
No new formation, eigensolver, numerical producer, microscopic coefficient,
physical clock conversion or effective inertia is introduced.

## Result

The owned carrier channel has an exact small realization: **four complex
carrier-coherence coordinates per record-count sector**, driven by two
conditional incidence density matrices. At linear order the latter are
known unforced functions, so the response closes without a fitted mass.
The source-visible free-operator space has four nonzero frequency pairs per
sector, not one oscillator. Its complete nonstationary response and work
can be retained as finite memory in a proposed larger model.

## 1. Exact block variables, source and absolute energy

Keep the original coefficients h=1, t=1/2 and lambda=1/2 (or lambda=0 for
the actual feedback-off preparation). The held Hamiltonian is

    H=3I+R−h X_a+n(9/4−lambda R−t T_C),
    R=q_L+q_R, n=(I−Z_a)/2.                                  (1)

P=(I−Z_C)/2 is the right-carrier occupation. The energy-unit current is
j=t nY_C=i[H,P], with the conventional carrier Pauli Y; D=t nT_C is its
phase contact. All onsite, record, degree and current-square energies are
already included in (1).

R and T_C commute with the *unforced* held H. A carrier density source
preserves R but generally mixes the T_C eigenvalues s=±1. Trace the R=1
record multiplicity without selecting a vector within it. In each R sector,
use the carrier-X basis (|+>,|−>) and incidence matrices

    a_R=9/4−lambda R, x_s=a_R−ts,
    H_s=(3+R)I+x_s n−h X_a,
    H_R=diag(H_+,H_-),
    P_R(carrier)=1/2 [[I,−I],[−I,I]],
    rho_R=[[rho_+,C_R],[C_R†,rho_-]].                          (2)

The subnormalized matrices retain the actual state. Their summed traces
give the constant R weight; the sum over R is one. Cross-R coherences do
not enter this R-preserving transport experiment, but must not be discarded
if a later source/readout changes record count. The R=1 trace is exact even
for a mixed conditional state.

For the diagnostic phase/scalar source of the Ward note, the exact rotating
frame has H+F(t)P, where F=V+ℏ phi_dot. The complete density equations are

    iℏ rho_+dot=[H_+,rho_+]+(F/2)(C_R−C_R†),
    iℏ rho_-dot=[H_-,rho_-]−(F/2)(C_R−C_R†),
    iℏ C_Rdot=H_+ C_R−C_R H_-+(F/2)(rho_+−rho_-).             (3)

The common scalar F/2 in the diagonal blocks cancels in these commutators;
it has not been deleted from the source energy. Equation (3) is an exact
finite-dimensional, bilinear state realization for arbitrary prescribed F.
It preserves the inherited density matrices and quantum readout rules,
not just a classical trajectory with similar frequencies.

The observables and intrinsic energy are

    <P>=1/2−Re Σ_R Tr C_R,
    <j>=2t Im Σ_R Tr(n C_R),
    <D>=t Σ_R Tr[n(rho_+−rho_-)],
    E_int=Σ_R Tr(H_+rho_+ + H_-rho_-).                         (4)

Thus <P>dot=<j>/ℏ and E_int_dot=−F<j>/ℏ. In the original frame the complete
source energy satisfies E_src_dot=−phi_dot<j_phi>+V_dot<P>. The constants
3+R in (2) remain in E_int and its initial value. Frequency differences
cancel these constants, but source/volume bookkeeping may not cancel them.

The actual preparations also have record-exchange symmetry: equal writer
couplings, both records initially blank, and an R-only held interaction.
This explains the unused antisymmetric R=1 record direction; it is not a
connected-only or favorable-state selection. Equations (2)–(4) do not need
that extra pure-state simplification and retain the multiplicity by tracing.

## 2. Four precisely owned transport frequencies per R

Let

    d_s=sqrt(x_s²+4h²),
    p_s,beta=[I−beta(2hX_a+x_s Z_a)/d_s]/2,
    E_s,beta=3+R+(x_s+beta d_s)/2,  beta=±1.                  (5)

P has the constant diagonal part I/2 and cross-s blocks −I/2. It has no
same-s, different-beta transition. Its four cross-s energy differences are

    Delta_beta,beta'=−t+(beta d_+−beta' d_-)/2.                (6)

For the inherited positive biases, the four positive angular frequencies are

    omega_slow,±=[t ± (d_-−d_+)/2]/ℏ,
    omega_fast,±=[(d_++d_-)/2 ± t]/ℏ.                         (7)

They are strictly positive: |d_-−d_+|<2t for h>0, while d_++d_->2t here.
There is no source-visible zero-frequency carrier-transfer mode in this
finite cell. The native lambda=1/2 values are exactly

| R | d_+ | d_- |
|---:|---:|---:|
| 0 | sqrt(113)/4 | sqrt(185)/4 |
| 1 | sqrt(89)/4 | sqrt(145)/4 |
| 2 | sqrt(73)/4 | sqrt(113)/4 |

The feedback-off Hamiltonian uses the R=0 pair for every R. The copying-off
state has only R=0 occupied, although its Hamiltonian retains the other
record sectors. Keep these labels and zero weights; do not silently replace
a record-bearing state by the copying-off state.

Every one of the four operator transitions is nonzero. Indeed, writing

    c_R=(4h²+x_+x_-)/(d_+d_-),   0<c_R<1,
    Tr(p_+,beta p_-,beta')=(1+beta beta' c_R)/2,               (8)

the squared P matrix element per record-multiplicity copy is
(1+beta beta' c_R)/8. A particular state's response coefficient may still
vanish or have either sign. Equation (8) is an operator-visibility result,
not a claim of positive occupied spectral weight in the formed state.

The constant I/2 part, conserved R/s weights, energy populations and record
multiplicity contain zero modes/initial data. They are not missing: they
condition the kernel and energy. They do not become an extra gapless phase
pole just because the total carrier number is conserved and fixed to one.

## 3. Exact linear realization with initial coherences

Under zero source the conditional matrices are known analytically:

    rho_s^0(t)=exp(−iH_s t/ℏ) rho_s(0) exp(+iH_s t/ℏ),
    C_R^0(t)=exp(−iH_+ t/ℏ) C_R(0) exp(+iH_- t/ℏ).           (9)

The source response of C_R to first order satisfies just

    iℏ delta C_Rdot=H_+delta C_R−delta C_R H_-
                       +(F/2)[rho_+^0(t)−rho_-^0(t)].        (10)

The first-order changes of rho_s are unnecessary for delta<P>,delta<j>,
but are fixed by (3) if the complete energy/state response is requested.
They must not be frozen in an exact finite-amplitude experiment.

Resolving (10) with the two link projectors gives four complex equations

    iℏ delta C_beta,beta'dot
       =Delta_beta,beta' delta C_beta,beta'
        +(F/2) p_+,beta[rho_+^0(t)−rho_-^0(t)]p_-,beta',       (11)

where each projected block has one complex coefficient. This is an exact
8-real-coordinate linear realization per R. Its drive coefficients retain
the unforced conditional link coherences, which rotate at d_s/ℏ; they are
not stationary population differences unless the actual state is stationary.

For a fixed physical initial state with phi(t0)=phi0, the rotating frame
initial condition is

    delta C_R(t0)=−i phi0[rho_+(t0)−rho_-(t0)]/2.             (12)

Covariantly twisting that initial state cancels (12). These are the same
boundary rules as the full Ward identity, not an arbitrary homogeneous
solution chosen to suppress a transient. The actual unperturbed C_R is
needed for mean occupation, current and work even though the *linear
self-response* (10) is determined only by rho_±.

This yields a useful exact distinction. Dephasing in R leaves the entire
transport channel unchanged. Dephasing in carrier X also leaves this linear
self-response unchanged, because [P(t),P(s)] is s-diagonal, but it generally
changes the unforced P,current and source work. Neither operation is being
performed physically. The source must use the full retained initial state
when those quantities are part of the experiment.

There is an exact control identity beyond the five measured contact values:
the feedback-off formation factorizes as a record Hamiltonian plus the
R=0 incidence/carrier Hamiltonian. Starting from the same blank incidence
and left carrier, its reduced incidence/carrier formed state equals that
of copying-off. Their entire carrier channel, including (10), therefore
coincides for all held times, although records and total energies differ.
The native feedback case need not coincide with either.

## 4. Finite-order operator closure and explicit memory

For each R choose the four high/low energy pairs with positive frequencies
omega_l from (7), and let Q_l=Pi_high P Pi_low. Define Hermitian operators

    X_l=Q_l+Q_l†,  Y_l=i(Q_l−Q_l†).

Their unforced equations are X_ldot=omega_l Y_l,
Y_ldot=−omega_l X_l. Their sum supplies the dynamic part of P; the constant
part is I/2. All eight signed eigenvalues are distinct within an inherited
R block and (8) makes all projections nonzero. Therefore the dynamic P
operator in that block has the exact, minimal free Krylov annihilator

    product_l (partial_t²+omega_l²) [Q_R P(t) Q_R−Q_R/2]=0.    (13)

Here Q_R is the record-sector projector and P the carrier occupation. The
corresponding expectation subtracts w_R/2, its conserved baseline; the
unshifted occupation does not obey the homogeneous eighth-order equation.
One may instead apply (13) to that sector's evolved carrier Z or current.
Repeated frequencies across record
sectors can be grouped; their state weights must be summed, not selected.
The full native operator has at most 24 dynamic real coordinates plus its
constant part. This is operator minimality within the free source-visible
Krylov space, not a claim that arbitrary density matrices require that many
independent canonical degrees of freedom.

At a source age u, the exact retarded density impulse kernel is

    chi_PP(u+tau,u)=sum_l [A_l(u) cos(omega_l tau)
                              +B_l(u) sin(omega_l tau)],
    A_l(u)=(i/ℏ)<[X_l,P]>_u,
    B_l(u)=(i/ℏ)<[Y_l,P]>_u.                                (14)

The sum includes every R. The initial conditions/sum rules are

    sum_l A_l(u)=0,
    sum_l omega_l B_l(u)=<D(u)>/ℏ².                          (15)

For Re z>0 its one-sided lag transform at that fixed source age is

    chi_tilde(z;u)=sum_l [z A_l(u)+omega_l B_l(u)]
                                      /(z²+omega_l²).        (16)

This is an age-dependent rational impulse response, not a convolution
kernel valid at every source time. With the actual density blocks in (9),
(14) or (10) reconstruct the full two-time response. The current response
is then fixed by the already derived Ward relation

    K_jphi=chi_jj−<D(t)>delta(t−s)
                              =ℏ² partial_t partial_s chi_PP. (17)

Omitting the contact or source-switch boundary violates this exact closure.
All signs and coefficients in (10)–(17) follow from the microscopic H and
state; no constant oscillator mass is needed.

## 5. Eligible reduction and the limit of a single local phase

The exact same-channel realization is not a single autonomous quadratic
phase mode: even one R block has four distinct operator frequency pairs.
The actual response also carries within-block coherences; its short-time
moment <D(u)> changes with age and is negative in the retained native age-2
state. A stationary passive single-oscillator replacement with one positive
oscillator strength cannot reproduce all these source moments and kernels.

Nor can the right-carrier population simply be called the conserved action
I of a local e(I) phase theory: P changes under the unforced native H. The
conserved total carrier count instead has zero relative-density response in
this one-carrier restriction. The previously derived isolated incidence
block has exact affine E(I) and finite action capacity, not positive quartic
hardening. Positive coordinate curvature alone does not change these facts.

These statements do NOT prohibit every nonlinear scalar representation
with specially nonlinear observables and additional retained state. Such a
proposal must exhibit that map and reproduce (10)–(17); pole counting alone
is not a no-go theorem against all nonlinear systems. They do exclude
identifying the currently proposed one local positive-hardening phase
sector with this exact carrier channel merely by matching one contact.

There are two concrete controlled alternatives:

1. **Retain the finite memory exactly.** Equations (3) or (10), with their
   microscopic frequency matrices and actual initial data, already supply
   a closed native transport port. A larger common model can be tested
   against this port without introducing an invented inertia or discarding
   its state. Quantum fluctuation/readout rules remain those of rho.
2. **Derive a state-qualified low-frequency reduction.** If a separately
   justified stationary state is used, A_l=0 and the susceptibility has
   sum_l B_l omega_l/[omega_l²−(nu+i0)²]. For |nu|<omega_min,

       |chi(nu)−chi(0)| <= nu²/(omega_min²−nu²)
                                      *sum_l |B_l|/omega_l.  (18)

   Higher derivative terms and analogous bounds follow from the same finite
   poles. This gives an actual error control, not an assumed instantaneous
   limit. Passivity/positive effective kinetic coefficients need their own
   state check. The actual coherent states cannot be made stationary by
   changing the notation: their conditional matrices rotate at d_s/ℏ.
   A time average or dephased state is a declared different readout/state
   prescription. Without that justification, retain (10) rather than use
   the stationary expansion.

This finite cell supplies no soft continuum. It does supply the exact poles,
state variables and Ward-normalized memory that a collective low-energy
construction must inherit or controllably eliminate. Physical clock/ruler
calibration is needed to interpret a frequency window in external units;
it is not needed to test the microscopic closure itself.

## 6. Smallest prospective arithmetic discriminator, if requested

No new source trajectory or time grid is necessary. Retain all three saved
preparations and five inherited ages. A small stdout-only calculation could
extract the matrices in (2) and coefficients A_l,B_l in (14), with all R
and zero-weight labels, using the existing analytical projectors. Qualify:

- (3)–(4) against the full 16D commutators and original absolute energies;
- all four gaps and overlap strengths per R, the polynomial identity (13),
  and exact projector reconstruction without a new diagonalization;
- (15), and the first eight per-sector lag derivatives against independently
  nested full-matrix commutators; retain signed coefficients and failures;
- equality of the two control channels from their actual reduced states,
  rather than just agreement of sampled contacts;
- the initial boundary (12) and the same contact/current Ward conventions.

This would produce a reproducible **native temporal-memory specification**
for later same-state transport matching, not another phenomenological fit,
new formation test or claim of emergent gravity. It does not alter the
already qualified twist result. No such producer was run for this note.

## Resident evidence

- `NATIVE_NONSTATIONARY_TRANSPORT_WARD_V001.md`:
  `142dc2d1b3bb2c4b3c7d166ebab3aac766950d6bc6183dad39e1add22b092556`.
- `NATIVE_RULER_SOURCE_AND_NORMAL_FORM_V001.md`:
  `335044ff025cfd831f92ed34574098fb7fe42841047c2b657d40962f6439568c`.
- `RECORD_ADDITION_RESULTS.json`:
  `2b9b19954f137aaf0b60173481fdb9059cda3892ee3c71bd9a6884cbb4b6350a`.
- `record_addition_compute.py`:
  `4df3bbc8b38ad6b602841b7b28a7a59d37e69d60286f7a2ef11c37ddc150ce10`.
- `NATIVE_TRANSPORT_TWIST_V001_RESULTS.json`:
  `9f29e3d5083d5a03b2e02dca62c2dd90041fa1303a573c55e5a73ed5545775d3`.
- `../recovered_sources/BS_MICRO_ACTION.md`:
  `00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec`.
