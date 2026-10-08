# Independent review: a nonvanishing native record-phase clock candidate

2026-09-28. The proposed observable, source orientation, three actual stored
preparations and full hold window were fixed before this calculation. This
review introduced no native state, physical parameter, source pulse or new
formation run.

## Outcome

The native formed state has a nonzero, forward-advancing writer-referenced
record phase on the **entire inherited interval [0,2]**, under the declared
1e-10 numerical allowance. The conservative 1,024-interval bounds are

    amplitude >= 0.9163300022,
    phase numerator >= 0.6597295250,
    0.6699443734 <= phase rate <= 0.9724973277.

The total continuous phase advance at age 2 is 1.7483061546 radians, in the
inherited epsilon_r=hbar=1 convention. Both grid resolutions independently
certify the same orientation; there was no time-window or sign selection.

| Actual preparation | Full-window outcome |
|---|---|
| Native formed | Nonvanishing signal and strictly advancing phase |
| Feedback off | Constant amplitude and exactly unit phase rate |
| Copying off | Exactly zero raising coherence; phase undefined |

Record **count** is conserved during the hold. Record **coherence phase** is
not: A raises record count and does not commute with the held Hamiltonian.
The result therefore supplies a concrete native temporal readout without
requiring new records to be written continuously. The feedback-off control
also shows that the existence of a phase signal alone is not evidence that
record–link feedback is necessary; feedback changes the native state's rate.

## Mathematical assessment

For A=A_L+A_R and z=mean(n A), the independently reconstructed held matrix
obeys [H,A]=(epsilon_r−lambda_R n)A. Thus

    a_dot=i(epsilon_r a−lambda_R z),
    phi_dot=epsilon_r−lambda_R Re(z/a),
    d|a|²/dt=2 lambda_R Im(conj(a) z).

All signs agree with the inherited minus-Pauli-Y convention and saved K/Y
pulse readouts. The complex ratio z/a is not an occupation probability.
The explicit counterexample to universal positive phase rate is valid, so
the actual-state test is substantive rather than a consequence of positive
onsite energy alone.

All 12 full energy-sector projectors and 16 adjacent-count lines are retained,
including both link bands and the count-one degeneracy. The line orientation
exp[i(E_final−E_initial)t] is correct for this raising observable.

The continuous certificate is analytically sound. With N=Im(conj(a) a_dot),
N_dot=Im(conj(a) a_ddot); the omitted |a_dot|² term is real. Hence
|a_dot|<=M1 and |N_dot|<=M0 M2. Endpoint grids with 512 and 1,024 intervals
have maximum nearest-node distance Delta_t/2. The stated subtraction terms
therefore cover the unsampled times. Signed rate bounds correctly use both
denominator endpoints. The native no-hidden-winding bound is only
0.00201322 radians per fine-grid interval, well below pi, and the stored
continuous phase lifts were independently reproduced.

The allowance is explicit numerical-error control corroborated by matrix
checks, not directed-rounding interval arithmetic. The reported continuous
claim must retain that qualification. It is not merely positivity at five
selected ages.

## Independent saved-data and matrix audit

The frozen source/note/protocol and both ancestral result/freeze pairs were
authenticated, including their canonical payload hashes. All original 518
checks pass; the largest original residual is 2.66454e-15.

The independent script rebuilt the 16-dimensional matrices directly with
Kronecker products, aggregated full numerical energy eigenspaces rather than
choosing vectors inside degeneracies, and checked every spectral coefficient.
A separately coded fixed-degree, centered-H scaled Taylor propagator checked
A, its first and second derivatives, nA, and the previously saved K/Y at every
inherited age. It did not import the production matrix or propagator module.
All 279 saved independent checks pass, with maximum absolute residual
7.32748e-15. The bounds and scientific decisions were independently rebuilt
from the authenticated coefficients. Additional read-only arithmetic also
checked every signed rate interval and stored phase lift.

Reproducible audit: `native_phase_clock_independent_audit.py` and
`NATIVE_PHASE_CLOCK_INDEPENDENT_REVIEW_DATA.json`.

- Production source SHA-256:
  `d06799742d7a800bf415f27b556761817b9044861e94143a535aa965a151bd62`.
- Production freeze SHA-256:
  `e01ceac78343ea49d29cebc8b555d77509427d172439339380e6e80c4a4eb70f`.
- Production result SHA-256:
  `5992e6daf072b3873670d22c280f4f1592e95a0f250eb703d919d6d548f21206`.
- Independent audit source SHA-256:
  `1922cb84632129a7eba6724bc23d6454e532d65dc483c4ab3a4c1c0d0a1b6e0f`.
- Independent audit result SHA-256:
  `7336c6809191bdf16fd8382c3e315768437bd769f45e903ae86c0b334e7a1414`.

## What this establishes next

The same native records already used in the source-response studies now have
a specified, state-dependent local phase reference that passes an oriented
continuous-window test. Its pulse-based quadrature access and switching work
can therefore be carried into a concrete calibration study.

This does not yet map the native evolution parameter to physical seconds or
identify the phase with the covariant clock field. A spacetime clock additionally
requires compatible spatial phases, a smooth timelike gradient, and the common
source/metric/energy constraints. Nothing here derives a native clock kinetic
term, a gravity law, an irreversible arrow, or behavior beyond age 2. These
are precise next interfaces to test, not reasons to discard the demonstrated
local phase reference.
