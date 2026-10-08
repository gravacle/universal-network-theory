# Native record-to-ruler response and the exact local mechanical parent

2026-09-29. Analytical, source-selective continuation; no numerical run, new
formation, fit, physical-metric identification or edit of frozen evidence.

Two useful answers are already fixed by the microscopic Hamiltonian. First,
the existing carrier readout has an exact writer-to-carrier response whose
first allowed short-time term measures a record/link/carrier correlation.
Second, the owned single-link incidence mechanics has an EXACT affine
action-energy relation. Its positive quartic coordinate potential cannot be
retained while dropping the equally compulsory momentum terms. This provides
a sharper native matching test than fitting a constant mass to one moment.

## 1. Owned operators, states and operational readout

In the existing16-dimensional held restriction keep BOTH endpoint records,
the incidence qubit and the one-carrier left/right factor. The writers retain
their fixed occupied content; their zero onsite energy is a spectator. The
original coefficients give

    H=3I+R-h X_a+n(9/4-lambda_R R-t X_C),
    R=q_L+q_R, n=(1-Z_a)/2, h=1, t=1/2, lambda_R=1/2.       (1)

This retains the native current-square term lambda_J n= n/4. Copying is off
in H; its owned source operator is K=X_L+X_R with PLUS sign +g(t)K. The
feedback-off preparation uses its own lambda_R=0 held Hamiltonian, not a
replacement of its state by the native state. The copying-off control is the
saved actually blank record state. Keep all complete saved vectors and phases.

The carrier arrival projector is P=(1-Z_C)/2. Its probability, continuity
current and transfer spectrum are an operational ruler candidate using the
declared boundary clock tau of BS05. This does NOT identify a physical photon,
proper length, gravitational potential or relativistic light cone. A metric
dictionary would have to reproduce these source/readout responses as well as
their clock and energy normalization, rather than simply rename incidence.

Conventions matter. X,Z and Y_a,Y_C below use conventional Pauli matrices,
Y=[[0,-i],[i,0]]. The saved native record quadratures use the opposite sign:

    Y_rec=Y_L(saved)+Y_R(saved), [R,K]=i Y_rec.

The old `record_addition_compute.operators()['YC']` ALSO uses the opposite
Pauli sign on its carrier factor. Therefore `Y_C=-o['YC']` here; Y_rec retains
the saved sign. X_C, P and the Hamiltonian are unchanged. This is a readout
convention, not a microscopic parameter change.

## 2. An exact history-to-carrier coefficient with no fitted source

At held age w let rho_w be the actual aged state. For a diagnostic negative
source H-fK define

    chi_PK(tau;w)=(i/hbar) Tr rho_w [P(tau),K],
    P(tau)=exp(iH tau/hbar) P exp(-iH tau/hbar).           (2)

The native plus-copy impulse has integrated strength eta and unitary
exp(-i eta K/hbar). Its derivative of the later arrival probability is

    R_PK(tau;w)=d<P(tau)>/deta|0 = -chi_PK(tau;w).

eta has units of action; it is not a constant source amplitude or an
automatically realizable zero-duration operation. This derivative can be
calculated exactly without applying a finite impulse or approximating a
galaxy source. For a finite-duration source, integrate the FULL nonstationary
two-time kernel against its specified history; do not identify eta with g.

Direct commutators of (1) give

    ad_H P=-i t n Y_C,
    ad_H^2 P=-t h Y_a Y_C-2t^2 n Z_C,
    [ad_H^3 P,K]=-lambda_R t h X_a Y_C Y_rec.            (3)

The first two lines commute with K, as does P. All record-independent terms
in the third commutator commute with K. In particular its record-dependent
piece before that final commutator is +i lambda_R t h R X_a Y_C. Thus

    chi_PK(0)=chi'_PK(0)=chi''_PK(0)=0,
    chi'''_PK(0)=-lambda_R t h <X_a Y_C Y_rec>_w/hbar^4,
    R_PK(tau;w)=lambda_R t h <X_a Y_C Y_rec>_w
                               *tau^3/(6hbar^4)+O(tau^4). (4)

With the saved carrier `o['YC']` the last coefficient has the opposite sign.
No passive-state assumption, phase mixing or low-energy approximation entered.
The state correlation may vanish or change sign; its value is an outcome,
not a positive signal imposed in advance. The first observable effect under
the writer source can therefore depend on a relationship invisible to counts
alone, and is connected directly to a native carrier readout.

There are two EXACT null controls, not approximate expected trends:

* If lambda_R=0, H separates the record and incidence/carrier dynamics, so
  [P(tau),K]=0 for all tau and every initial state, including entangled ones.
* If rho_w is block diagonal in total R, then the same trace is zero for every
  tau. P(tau) preserves R and K changes it by one. The copying-off blank
  state satisfies this condition. Its response to a finite pulse can start
  at quadratic order in pulse strength; a zero linear response does not say
  that records can never change a carrier trajectory.

The matched formal control D_R(rho)=sum_R P_R rho P_R is especially useful.
It preserves all held R populations, held energy, incidence expectations and
unperturbed carrier transfer at EVERY time, but kills this linear cross-channel.
It is a density-matrix counterfactual, not an assertion of free physical
dephasing or information destruction: a real implementation needs its own
environment/work ledger. It also kills the record-raising clock amplitude,
so this comparison must use the inherited external boundary clock, not
pretend that both states possess the same arg<A> clock.

## 3. What a native low-energy oscillator approximation really contains

For each preserved total-record/carrier-X sector (R,s), let w_Rs be its
constant trace weight and sigma its normalized conditional link density
matrix after tracing the R=1 multiplicity. Its Bloch radius r is fixed under
the held dynamics. For positive w and r, set

    x=9/4-lambda_R R-s/2, d=sqrt(x^2+4h^2),
    L=(2h Xbar+x Zbar)/d,
    S1=(x Xbar-2h Zbar)/d, S2=Ybar.

Then H expectation is 3+R+x/2-dL/2. Use the canonical angle
phi=-atan2(S2,S1) and the orbit action

    I=hbar(r-L)/2, 0<=I<=hbar r, {phi,I}=1.

Exactly, on this compact fixed-radius orbit,

    E(I)=3+R+x/2-dr/2+(d/hbar)I,
    omega=E_I=d/hbar, E_II=0.                           (5)

The endpoints have no angle, and r=0 has no oscillating orbit. This is an
exact canonical representation of density-matrix expectation dynamics, not
a replacement of quantum probabilities by a classical ensemble or a bosonic
ladder with arbitrary occupation. For a sector weight w use canonical J=wI;
its total energy is w E_min+(d/hbar)J and capacity J<=w hbar r.

The incidence-source operator is ALSO fixed by this map:

    n(I,phi)=n0+x I/(d hbar)
        +(2h/d)sqrt[(I/hbar)(r-I/hbar)] cos(phi),
    n0=(1-xr/d)/2.                                      (6)

For the source H-f(t)n, keep (5)-(6) in a fixed zero-source frame. An
instantaneously diagonalized frame at changing f would require its canonical
time-dependent connection; omitting it would falsely make every drive
adiabatic. Equation(6), rather than a freely chosen linear oscillator source,
retains the native compactness, longitudinal term and source moment.

Near the lower stationary point a positive harmonic approximation DOES exist.
In the original canonical incidence chart q=m-m0, p=hbar theta, with

    m0=(1-rx/d)/2, Z0=rx/d, Q0=2hr/d,
    H=const+x m-h Q(m)cos(p/hbar),
    Q(m)=sqrt[r^2-(1-2m)^2],

its coefficients are

    k=H_mm=4h r^2/Q0^3,
    1/M=H_pp=h Q0/hbar^2,
    k/M=d^2/hbar^2,
    chi_n(0)=1/k=2h^2 r/d^3,
    1/M=h Xbar_ground/hbar^2.                            (7)

They are derived microscopic coefficients, not a fitted mass. This local
approximation needs small excursions compared with the compact orbit; it does
not replace the actual formed state by its lower stationary direction.

At p=0 the coordinate potential has

    V'''(m0)=-24h r^2 Z0/Q0^5,
    V''''(m0)=48h r^2(r^2+4Z0^2)/Q0^7 >0.                (8)

That positive quartic is correct. But at the SAME order the Hamiltonian has
the compulsory terms

    +h Z0 q p^2/(hbar^2 Q0)
    -h r^2 q^2 p^2/(hbar^2 Q0^3)
    -h Q0 p^4/(24hbar^4),                               (9)

besides the coordinate cubic/quartic and harmonic pieces. Dropping (9) does
not give the native low-energy expansion. For the transparent algebraic
special case x=0, the quartic coefficients are

    (2h/r^3)q^4 -(h/(r hbar^2))q^2p^2
                                      -(hr/(24hbar^4))p^4.

Their harmonic-orbit averages are respectively
`[3/4,-1/2,-1/4] h I^2/(r hbar^2)`, which sum to zero. For biased native
sectors the coordinate cubic also contributes to the normal-form correction;
the exact (5) proves cancellation to every order without truncation. x=0 is
an algebraic illustration, not one of the six inherited sector biases.

## 4. Consequence for the adopted quartic comparison parent

An isolated positive-mass, positive-quartic scalar oscillator has E_II>0 at
zero source. It is therefore NOT this exact held single-link channel, nor
its complete normal form through the first nonlinear action order. The
constant-mass quartic comparison also has unbounded action, while (5) has
a finite capacity. Its pressure/hardening mechanism cannot be inherited from
the positive coordinate V'''' alone.

This does not exclude that comparison as an eventual collective limit of an
interacting network. Multi-link degree penalties and carrier entanglement do
not close into independent Bloch spheres. A genuine collective derivation
must specify the retained low-energy modes/state and show a nonzero positive
action-curvature coefficient after ALL momentum, source and eliminated-mode
terms are included; a mode-count density alone cannot do it. Near one stable
branch the quadratic oscillator in (7) is already a legitimate narrower
native approximation. There is no soft continuum in this finite cell:
with its inherited h=1 and biases, all d are bounded away from zero.

The diagnostic incidence source still has exactly zero bare second contact.
Eliminating states can produce a source-dependent self-energy, but that is
part of the same susceptibility and must not be counted again as a separately
adjustable positive contact. The mechanical square's critical contact and
its physical source/volume interpretation require their own native derivation.
Likewise affine E(I) does NOT already imply cosmological dust: physical volume,
the state weights/Casimirs under growth, the clock and absolute energy/pressure
map have not been supplied by this finite-cell normal form.

## 5. The smallest exact discriminating calculation

No larger lattice or new formation is needed for the next test:

1. Reuse all three saved full16-component preparations at all five inherited
   held ages w={0,.25,.5,1,2}. Construct P,K and all Y matrices with the signs
   above. Keep each preparation's own held Hamiltonian.
2. Check (3) as full operator identities and retain every signed actual-state
   cubic coefficient in (4). Check the sector energy/action/source identities
   (5)-(7) on the occupied conditional blocks, including their actual mixed
   Bloch radii rather than a ground replacement.
3. At inherited positive delays tau={.01,.02,.04,.08}, evaluate the exact
   plus-copy derivative -chi_PK. Independently evolve the tangent vector
   `U(tau)(-iK psi_w/hbar)` and contract it with the unperturbed arrival
   readout; a Taylor propagator can cross-check the spectral propagator.
   The derivative is about one ideal integrated source, not the response of
   the old finite rectangular pulse at the same numeric source amplitude.
4. Retain the exact feedback-off and blank linear nulls. Include the formal
   total-R-dephased density control at each age: its baseline carrier curve
   and held energy are unchanged and its cross-response is exactly zero.
   Do not phase-select a state because its response looks attractive.
5. Keep the source-work derivative. For a finite ideal kick its exact held
   energy change is Tr rho_w[exp(i eta K/hbar)H exp(-i eta K/hbar)-H]; at
   zero strength its derivative is (i/hbar)<[K,H]>. A real finite waveform
   must instead include its explicit on/off and source-work ledger.

This would provide a falsifiable native history-to-carrier source mapping
and a matched-invisible-baseline control, not a gravity result. Any proposed
effective ruler/metric readout with the same physical source must reproduce
this full cross-kernel and its exact short-time coefficients, not only fit
an incidence self-susceptibility. Identifying which controlled native source
corresponds to physical metric strain remains an additional dictionary, not
a conclusion smuggled into this calculation.

## Source identities read for this derivation

All paths are resident in this packet; hashes authenticate bytes, not a claim
that the microscopic candidate is already nature's complete theory.

* `../recovered_sources/BS_MICRO_ACTION.md`:
  `00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec`.
* `record_addition_compute.py`:
  `4df3bbc8b38ad6b602841b7b28a7a59d37e69d60286f7a2ef11c37ddc150ce10`.
* `RECORD_ADDITION_RESULTS.json` (existing input identity, not rerun):
  `2b9b19954f137aaf0b60173481fdb9059cda3892ee3c71bd9a6884cbb4b6350a`.
* `NATIVE_CANONICAL_INCIDENCE_CLOSURE_V001.md`:
  `e6bfa4b392c5131c2367e115866e83a4344dfea73982236ce56fdc090026b56a`.
* `NATIVE_CARRIER_RULER_PATHWAY_V001.md`:
  `4277871cd49f7e45169f3fd7db0b5d49b9b66651f6b4ac257d794a5230254db8`.
* `NATIVE_SOURCE_BRIDGE_DECISION.md`:
  `c82040f7bebbdefcec4e782f8afb86c6c1c3f2367775f5fd2e6dbbe6159c737a`.
* `NATIVE_WRITER_PULSE_RESULT.md`:
  `8b831defe6915834a6d3cdfe79987987ddfdfc2ed0d95bc65a7a3e65c5726188`.
