# Native retained-record excess: exact work condition V001

2026-09-27. Analytical result only. No numerical run, new Hamiltonian,
physical deformation, state preparation or parent transfer is adopted.

Resident inputs are the revised plan (SHA256
`6b2a8bee520e828f4ccc583db920f289fe0c0a9eefd85fd78c22b6db90da2ccc`),
the I0 allocation and energy-elasticity notes, `TWO_BAND_ANALYTICAL_BRIDGE.md`
section 1, `NATIVE_BRIDGE_LEMMAS.md`, and `SCIENTIFIC_NEXT_CONSTRUCT.md`
(SHA256 `68fe8aa680290b6d9aef23487e9f77fca40bc72d0e655d0806cb9d5db997437a`).
The original `compute_join.py`, BS `MICRO_ACTION.md` and old accounting draft
are dataless and were not reopened. The inherited equations below are read
from the resident analytical notes, not a fresh source replay.

## 1. Necessary and sufficient condition for constant complete excess

For any declared common control u(t), let H_q(u) be the complete native
Hamiltonian in conserved occupation sector q=0,1 on the same background
state space. Let rho_q(t) follow its own unitary dynamics, with arbitrary
normalized initial states fixed by the comparison protocol. Define

    E_q=Tr(rho_q H_q),        M=E_1-E_0.

The commutator term cancels exactly in each total energy derivative:

    dot M = dot u [Tr(rho_1 partial_u H_1)
                 -Tr(rho_0 partial_u H_0)].                 (1)

Thus M is constant on an interval **if and only if** its excess parameter-work
rate vanishes throughout that interval (almost everywhere for absolutely
continuous paths). Control jumps require their jump-work terms as well.
Multiple controls add their corresponding terms. Matching
the initial record counts, bare storage energies or mean background energies
does not replace this condition. At fixed controls both complete sector
energies are constant, even when an assigned record–link interaction energy
exchanges with the background.

For an open region, add the difference of its complete non-parameter supply
and boundary-flux powers to (1). If a controller or geometry is included in
the closed total Hamiltonian, do not also count its transfer as a second
external supply. The same region, reference preparation and interaction
ownership must be fixed before calling M a material excess.

Only with an independently supplied material volume V is

    dot(M/V)+(dot V/V)(M/V)=dot M/V.

Consequently M/V has dust's inverse-volume scaling exactly when the right
side vanishes. Under a closed, volume-only work interface, its mechanical
excess pressure is minus the difference of the two volume-force expectations;
for dot V!=0, zero pressure is then equivalent to dot M=0. Neither a volume
nor that physical interface has been established by this identity. Exchanges
can mimic a density slope without establishing dust stress or perturbations.

## 2. A concrete native test direction, not an invented b(V)

At fixed carrier-X label s, the inherited one-link block has the form

    H_q(b)=C I+epsilon_r q I-hX+(b-lambda_R q)n,
    n=(I-Z)/2.

Here b is the existing q=0 detuning including the fixed carrier contribution;
the inherited values give h=1, epsilon_r=1, lambda_R=1/2 and
b=9/4-s/2. Treating b as a mathematical control with the other coefficients
held fixed specializes (1) to

    dot M = dot b (<n>_1-<n>_0).                           (2)

This identifies the exact observable a proposed detuning deformation must
control. It does not identify b with length or volume. A physical deformation
may change other couplings too; all their force differences must then enter.

As a separate **static eigenbranch diagnostic**, define

    f(b)=(b-sqrt(b^2+4h^2))/2,
    M_lower(b)=epsilon_r+f(b-lambda_R)-f(b).

Because f''(b)=-2h^2/(b^2+4h^2)^(3/2)<0,

    dM_lower/db=f'(b-lambda_R)-f'(b)>0                    (3)

for h,lambda_R>0. A constant bare record energy therefore does not make
the lower-link-eigenbranch insertion cost rigid under this native
parameter direction. The corresponding upper-branch derivative has the
opposite sign. No ground-state replacement, cooling or adiabatic formation
is licensed: the actual formed state retains its upper-band population and
coherences, and must use (1)–(2) with its actual sector states. Equation (3)
is a counterexample to an all-state rigidity claim, not that state's pressure.

The feedback-off control gives a useful sufficiency check. With lambda_R=0,
constant epsilon_r and the **same initial background state** in both sectors,
H_1=H_0+epsilon_r I, so both background histories agree and M=epsilon_r under
any common background drive. That control removes this lambda-mediated
record/active response; it does not remove every possible record interaction
from a wider parent. Conversely nonzero feedback does not prohibit constant
M for special states or other deformation directions; for example matching
maximally mixed link states keep <n>_1=<n>_0=1/2 in this block.

## Changed next action and remaining dependency

The next load-bearing item is the **same-parent deformation generator and
its excess work**, not another demonstration of record retention or a bare
energy-per-record assignment. Once that generator is specified, (1) supplies
an exact finite test using the actual formed state, without fitting a dark
abundance or first deriving all gravity.

No actual native joint active/maintenance dust-plus-vacuum law was found in
these scoped resident inputs. The native source-off hold needs no occupation
refresh; it supplies neither a compulsory maintenance power nor the missing
physical volume/work law. That is a precise current dependency, not a claim
that the joint network program is impossible. This retained-defect control
does not replace the primary allocation construct or borrow q4, FY,
induced-spectrum or owner-once geometry.
