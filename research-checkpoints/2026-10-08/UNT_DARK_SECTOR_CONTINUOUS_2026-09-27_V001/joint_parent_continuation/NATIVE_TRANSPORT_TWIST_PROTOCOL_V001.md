# Native saved-state transport contact and current V001

2026-09-29. Prospective stdout-only arithmetic over the actual retained 16D
native preparations. No formation, eigensolve, larger lattice, physical
strain identification or new source history. The parent is the sole runner.

## Exact retained evidence and useful limit of this test

`RECORD_ADDITION_RESULTS.json` retains three full complex formed vectors:
native, feedback-off and copying-off. Each has the inherited held ages
0,.25,.5,1,2, its own Hamiltonian, twelve analytic spectral sectors, full energy
ledger and hopping energy. All 15 states are retained. Thus the transport
contact t<nT> is already minus the saved hopping energy. The vectors and
projectors also determine the actual current t<nJ> without a formation rerun.

The native and feedback-off preparations are NOT energy/Hamiltonian-matched
histories. Formal total-record dephasing preserves this entire held
incidence/carrier twist channel, including both readouts; it is a matched
null control, not a promised history contrast. It does not preserve the
separate writer cross-response or record-phase clock.

For a later loop test the retained N2/N3 carrier-ruler result has all edge
currents and total hopping energy, but not the individual real edge coherences
or full evolved vectors. A fresh old64D N2 held-state reconstruction would
be required for a complete plaquette-flux Hessian; the declared states there
also have blank records, not a newly authenticated matched formation pair.
That separate calculation is NOT part of this protocol.

## Operators and source conventions

Use basis (left record,right record,incidence,carrier L/R). The current
convention is BS07: A=|R><L|, T=A+A†=X_C,
J=i(A-A†)=conventional Pauli Y_C. The old saved `YC` uses the opposite sign.
The original held action is

    H=3I+R-X_a+n(9/4-lambda_R R-t T),
    R=q_L+q_R, t=1/2, lambda_R=1/2 (or zero in that control).

All original degree, record, carrier and current-square energies are retained.
The prospective dimensionless edge phase is a diagnostic source:

    H(phi)=H+t n[T(1-cos(phi))-J sin(phi)],
    j(phi)=-H_phi=t n[J cos(phi)-T sin(phi)],
    D(phi)=H_phiphi=t n[T cos(phi)+J sin(phi)].

At zero source D=t<nT> and j=t<nJ>; the particle transfer rate is j/hbar.
The fixed-state source work is exactly

    E(phi)-E(0)=D(1-cos(phi))-j sin(phi).

This is a Hamiltonian source at a fixed state. A state-only twist
psi->G(phi)psi at fixed H instead has work D(1-cos(phi))+j sin(phi).
The two are checked separately; their opposite current signs are not mixed.

Keep BOTH the correlated expectations and their factorized counterfactuals
t<n><T>, t<n><J>. No mean-incidence substitution is used in the actual readout.
No sign, positivity or history-difference gate is imposed.

For P=carrier-right projector, the exact operator controls are

    i[H,P]=j(0) (hbar=1),
    [P,[H,P]]=D(0),
    H(phi)=G(phi) H G(phi)†, G(phi)=exp(i phi P).

Also J(phi)^2=J^2=I in this one-carrier restriction, so the native
lambda_J*n*J^2 term is unchanged under the consistent twist. The same holds
for all other retained nonhopping terms. The last similarity proves full
equilibrium-spectrum invariance WITHOUT a new diagonalization. A single
edge has no gauge-invariant loop flux. Accordingly D is an instantaneous
fixed-state contact, NOT a relaxed helicity modulus or a derived continuum
phase-gradient coefficient alpha. The state-response/current kernel must
accompany it before any dynamical transport matching; adding it again to
the same microscopic Hamiltonian would double-count the source response.

## Frozen census and numerical controls

All three saved preparations, all five ages and angles
{0,-.001,+.001,-pi/2,+pi/2,pi}, fixed before outcomes. Reconstruct each held
state with its original analytic projectors, independently check the compact
two-by-two block exponential, and compare all saved held energies, incidence,
carrier and record means. No eigensolver or formation exponential is used.

At each angle compare direct Peierls matrix, exact gauge similarity, unrotated
state energy/work, current continuity, analytic first/second derivatives and
gauge-transformed-state energy invariance. Also retain the separately labeled
fixed-H state-twist work and its opposite current sign. At the small angles use stable
interaction work, not subtraction of two large complete energies, to check
the centered sine derivative and second derivative. Keep full complete energy
and the separate interaction work in the output.

Six synthetic operator controls, explicitly not formed states: incidence on
with carrier X+,X-,Y+,Y-,L; and incidence off with carrier X+. Records blank.
They establish expected positive/negative/zero contacts and currents and exact
source work. Formal total-R-dephased controls retain the same state energy
and both transport expectations; their channel invariance follows from the
commutation with R, not an assumed physical dephasing process.

Absolute matrix/expectation tolerance 2e-11. Stable small-angle derivative
checks use 2e-9 absolute tolerance, fixed before outcomes. This is floating
arithmetic qualification, not interval certification. All signs/outcomes and
failures are retained. Maximum matrices are 16 by 16; no checkpoint or long
job is required. Output is below 1 MiB and contains no physical length/time
conversion or fitted effective stiffness.

Authenticate the result/payload/freeze, all original five manifest members,
the exact BS source and this prospective source/protocol. `freeze` prints the
snapshot only; `run` requires the saved identical snapshot and prints the
complete result. The worker never writes files or imports producer modules.
