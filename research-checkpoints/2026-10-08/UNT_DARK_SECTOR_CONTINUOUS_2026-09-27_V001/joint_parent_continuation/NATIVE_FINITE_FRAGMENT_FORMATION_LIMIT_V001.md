# Formation after the finite-fragment test: the next model decision

2026-09-30. Source-level analytical continuation only. No new propagation,
coefficient calculation, higher-order expansion, state replacement or source
change was made. The exact order-four result remains a separate frozen packet;
its signs and limited coverage are not altered by this note.

The closed 384D extension is useful for testing a paid microscopic exchange
mechanism, but cannot by itself establish asymptotic formation of the required
native state. The shortest next decision is therefore to define an owned
outgoing-region or ordered-layer model, not to scan for a favorable age in
this same finite cell. This note specifies that decision without taking it.

## 1. Exact original-state variance and a reduced-state obstruction

Use each original endpoint/blank/C=1 preparation from the current note and
the complete H'_X, including both controllers, fragment gaps and interactions.
Set f_j=s_j^-1 for A and f_j=1 for B, in the inherited native energy unit.
The five off-diagonal states in H'_X psi0 are mutually orthogonal: one Q
neighbor, one C flip, one incidence flip and the two record flips. Their
amplitudes are respectively -1,-1,-f_j,+f_j,+f_j. Hence

    E0,A=2+3s_j^-1,          Var_0(H'_A)=2+3s_j^-2,
    E0,B=3+2s_j^3,           Var_0(H'_B)=5.              (1)

Restoring the common energy unit E_* multiplies the means by E_* and the
variances by E_*^2. No new calibration is introduced. F_Sigma psi0=0 is
sufficient here: H'psi0=Hpsi0 and <H'^2>=||H'psi0||^2. It was NOT sufficient
on its own for the energy-dipole double-moment identity, which also required
the independent blank-fragment orthogonality argument.

Both variances are positive. The initial pure total state is therefore not
an energy eigenstate or a stationary total density operator. A fixed closed
unitary evolution cannot approach a different full density operator in trace
norm: if a limit existed, its time translates would coincide with it, making
the limit stationary, and unitary invariance of the distance to that stationary
limit would force the original state already to equal it. Distances between
two full initial states are likewise conserved, excluding a common full-state
attractor for distinct preparations.

Partial tracing does permit apparent damping by entanglement. However, for
this fixed finite Hamiltonian every matrix element of the native reduced
state, and every bounded native observable, has the form

    <O>(t)=sum_(E,F) exp[i(E-F)t/hbar] Tr(rho0 Pi_E O Pi_F). (2)

This is a finite frequency sum with complete energy-degeneracy blocks. Such
a sum can have a late-time limit only if all grouped nonzero-frequency
coefficients vanish: multiply its deviation from the proposed limit by each
frequency and take the Cesaro average to isolate that coefficient. It must
then have been constant at every time. Equivalently, finite-dimensional
unitary recurrence supplies arbitrarily close returns, with no asserted
short recurrence-time estimate.

For the actual native record occupation, the already derived blank result is

    <R>(t)=2 f_j^2 (t/hbar)^2+O(t^4),   <R>(0)=0.      (3)

It is nonconstant for both endpoints and both families, so it cannot tend to
a constant as t tends to infinity in this exact closed model. In particular
the whole native reduced state does not converge to a fixed formed state.
This is stronger than simply saying global energy is conserved, but is NOT
a no-go theorem for a larger native universe, approximate finite-window
equilibration, or a restricted observable whose oscillatory coefficients cancel.
It also does not claim that a particular signed response remains negative
at every age. No favorable-age scan establishes the missing asymptotic limit.

## 2. Three different objects must remain distinct

The actual reduced state is Tr_b[U(t)rho0 U(t)^dagger], with its changing
native/fragment correlations. It is not obtained by applying the same
fresh-blank channel repeatedly to reused correlated fragments.

The exact infinite age-average comparator is

    rho_d=sum_E Pi_E rho0 Pi_E.                         (4)

It is stationary but preserves the original energy-block populations and
within-degenerate-block coherences. It is a readout average, not physical
dephasing, cooling or a prepared state. Even an explicitly implemented
dephasing channel would not automatically rearrange populations into passive
order. Restricted-source passivity is a separate test of the complete source
response, not a consequence of stationarity, one positive moment or a reduced
state that looks locally thermal. A driven steady state needs its driven
response and work ledger, not an unforced Kubo formula by substitution.

A finite-window approximation is a third, potentially useful target. It
requires an independently stated physical time/error domain and a bound
uniform over the allowed ages and source probes, not one selected late-time
snapshot. The previous age-average error bounds qualify their particular
readout protocol only. They do not supply a formation mechanism.

## 3. Minimal next completion, before another formation calculation

The BS seed already offers a port completion slot (BS12), finite fragments
(BS10), and an ordered fresh-layer channel (BS14a). It explicitly does not
prove no-backward signalling merely by drawing an oriented edge. None of
these symbols fixes an outgoing physical reservoir or preparation law.

The next concrete model must choose ONE of these scoped targets:

- A larger finite native graph with a specified observation region, actual
  transport/copy Hamiltonian and initial surrounding state. Prove that energy
  and relevant source correlations leave that region with a bounded return
  error throughout a predeclared observation window. A distant boundary or a
  graph arrow alone is not a no-return proof. Finite recurrences remain.
- A specified increasing-graph/layer limit with controlled local observables,
  source assignments and an incoming-state family. An asymptotic relaxation
  claim requires taking/controlling that limit before the late-time limit;
  exchanging them is a mathematical assumption requiring justification.

For the ordered-channel route, the missing data are explicit: each U_j,
the independently supplied target state beta_j, interval/clock, attachment
and decoupling rule, fragment/transport energies, conserved sectors and all
controller actions. The exact finite prefix is

    Phi_j(rho)=Tr_out[U_j(rho tensor beta_j)U_j^dagger]. (5)

An independent fresh beta_j at every step is a physical boundary condition,
not a free reset. Repeated Phi with fixed beta and a chosen gap is a new model
until that supply is derived or independently specified. Its fixed states,
source-visible nondecaying modes and any contraction must follow from those
owned data. A fixed point alone is not passivity or a low-frequency closure.

Both routes must use the SAME microscopic couplings, source/volume dictionary
and preparation rule in the two environments. Local native degree, record
occupation, physical volume and matter density are not interchangeable.
Separate fitted gaps, renewal rates or age choices at each radius would
reintroduce the freedom the program is trying to eliminate.

## 4. Outgoing is not absent: energy, source and volume debit

For a chosen local energy partition, the exact regional balance is

    d<E_R>/dt=<partial_t E_R>+(i/hbar)<[H_tot,E_R]>,
    J_out=-(i/hbar)<[H_tot,E_R]>.                       (6)

Boundary interaction energy must be assigned once and retained; redefining
the partition changes this current accounting. At genuinely decoupled
incoming/outgoing boundaries, a finite-prefix ledger reads

    Delta E_native + Delta E_controller
       +sum_j(E_out,j-E_in,j)=W_external.              (7)

For a closed autonomous parent, controller exchanges belong on the left,
not again as external work. For imposed switching or sources,
W_external=integral sum_theta <partial_theta H_tot> d theta. A zero mean
switch-on energy of a blank target does not establish free preparation,
unlimited low-entropy supply or zero switch-off work. Energy and correlations
carried outside the local region remain part of the universe's accounting.

The lapse, ruler and volume derivatives must act on the same full transport,
fragment, interaction and controller energies: Z_tot=partial_a H_tot,
B_eta=-partial_eta H_tot, with every mixed contact retained. Source-dependent
incoming states, channels and boundaries contribute their own derivatives.
Deleting their energies after tracing a fragment would invalidate precisely
the gravitational/absolute-work comparison being pursued. No symmetric
c(V)I, physical gap/clock calibration or emergent metric has been fixed here.

## Decision and evidence boundary

The finite 384D result is a controlled microscopic/source discriminator, not
an autonomous formation completion. The next useful action is to specify
and analytically audit one outgoing-region/layer completion and its complete
energy/source/preparation ledger. There is no authorized automatic bath,
reset, higher-order expansion or time scan in this note. If the required
boundary choice is unavailable, that formation lane has a precise model-input
gap; useful independent program lanes remain open.

Inputs read for this deduction include the existing reservoir/channel,
autonomous-controller, age-average and current notes, and BS08--14a. Key
identities, with all predecessors unchanged:

- `NATIVE_FINITE_FRAGMENT_SOURCE_CURRENT_V001.md`:
  `1116b37f9cbd35a10abc55632f4d21230cdee5a27c5122e0d70d138881b4324b`.
- Completed exact packet (root-owned execution, not rerun or reinterpreted
  here), `NATIVE_FINITE_FRAGMENT_SOURCE_EXACT_V001_RESULTS.json`:
  `8c35b7b7e987113dc82577b5e496bc5bf690e49fb70fe1ffde05e64476b39ae5`.
- `NATIVE_RESERVOIR_FORMATION_CHANNEL_V001.md`:
  `6db32da99d6d346736e193b34b34cb270c242821051296de1be3bf7d86031a39`.
- `NATIVE_ENERGY_SOURCE_AGE_AVERAGE_V001.md`:
  `764bb3f333aab4750fcb564c043ad715343dfaf15a5519e9fafa3b7cb18cf4d6`.
- `NATIVE_AUTONOMOUS_CONTROLLER_CANDIDATE_V001.md`:
  `69dc91bbc08550481759b8b1646124a249c4386e3484fab8b7982b49bd77adfa`.
- `../recovered_sources/BS_MICRO_ACTION.md`:
  `00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec`.
