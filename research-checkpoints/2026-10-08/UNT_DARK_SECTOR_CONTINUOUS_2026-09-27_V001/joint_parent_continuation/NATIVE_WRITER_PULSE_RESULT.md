# Native writer-pulse result: formed records retain phase-sensitive response

All 1,631 checks pass for the prescribed 240 pulses, covering all three saved
preparations at all five ages. The actual positive copying pulse has the
predicted opposite K-response sign in both formed states versus the blank
control. The native held record count is unchanged as it ages, but its response
to the same later pulse can reverse sign. That directly demonstrates response
information beyond the record count in this specified native model.

No formation was rerun. The root's measured execution was 0.0825544 seconds
with 39,337,984 bytes peak self RSS. This independent review rechecked hashes,
census, saved scalar arithmetic, source-work closure, finite differences and
bounds without propagating any state. The review implementation and output are
`native_writer_pulse_saved_audit.py` and `NATIVE_WRITER_PULSE_REVIEW_DATA.json`.

## Complete age census and actual short pulses

Every entry below uses duration .01 and the same positive source epsilon .005,
in the inherited hbar=1 units. S is the double-commutator expectation
`<[K,[H_hold,K]]>`; the leading linear K response is `-S*tau^2/2`.
The count is the pre-pulse held count. All four durations and all four signed
amplitudes remain in the full result; the table is the protocol's shortest
pulse diagnostic, not a selected best outcome.

| Preparation | Age | Held R | S | Actual change in K | Actual change in R |
|---|---:|---:|---:|---:|---:|
| Native | 0 | 1.31433676545 | -0.867381853 | +2.16316e-7 | +7.49922e-5 |
| Native | .25 | 1.31433676545 | -0.813079785 | +2.03143e-7 | +6.25765e-5 |
| Native | .5 | 1.31433676545 | -0.825188049 | +2.06623e-7 | +4.78485e-5 |
| Native | 1 | 1.31433676545 | -1.014395843 | +2.54407e-7 | +1.05616e-5 |
| Native | 2 | 1.31433676545 | -1.169355919 | +2.91823e-7 | -6.73927e-5 |
| Feedback off | 0 | 1.29381830117 | -1.175273205 | +2.93839e-7 | +7.00429e-5 |
| Feedback off | .25 | 1.29381830117 | -1.175273205 | +2.93833e-7 | +5.17738e-5 |
| Feedback off | .5 | 1.29381830117 | -1.175273205 | +2.93826e-7 | +3.02856e-5 |
| Feedback off | 1 | 1.29381830117 | -1.175273205 | +2.93810e-7 | -1.68870e-5 |
| Feedback off | 2 | 1.29381830117 | -1.175273205 | +2.93786e-7 | -8.82924e-5 |
| Copying-off blank | 0 | 0 | +3.125975578 | -7.81178e-7 | +4.99997e-9 |
| Copying-off blank | .25 | 0 | +3.188157292 | -7.98153e-7 | +4.99997e-9 |
| Copying-off blank | .5 | 0 | +3.421289128 | -8.57164e-7 | +4.99997e-9 |
| Copying-off blank | 1 | 0 | +3.854686046 | -9.64194e-7 | +4.99996e-9 |
| Copying-off blank | 2 | 0 | +3.386911166 | -8.46173e-7 | +4.99997e-9 |

The blank control's linear R response is exactly zero in the saved computation,
while its finite pulse still produces a small even-amplitude count increase.
Across the entire fixed duration/age grid the exact K linear response is
positive for both formed preparations and negative for the blank control.
The smallest actual shortest-pulse K signal exceeds the fixed raw 1e-12
allowance by 203,142 times.

## Independent arithmetic and numerical agreement

The audit independently reconstructs the central derivatives from the four
signed saved changes, Richardson combinations, leading coefficients, count
and slope formulas from the authenticated older age data, and all 240 work
sums. The maximum scalar arithmetic discrepancy is 1.11e-14. All 120
observable/age/duration response rows and all bounds are retained.

| Check | Maximum absolute discrepancy |
|---|---:|
| Spectral derivative versus coupled Taylor | 1.24127e-16 |
| Full Kubo16 versus exact derivative operator | 9.74239e-17 |
| Kubo8 versus Kubo16 | 4.16356e-17 |
| Held propagator versus inherited Taylor | 5.37886e-15 |
| Pulse energy conservation | 7.10543e-15 |
| Complete switching work versus held-energy change | 7.01739e-15 |
| State norm | 3.55271e-15 |
| Richardson derivative versus exact linear response | 6.39558e-14 |

The largest finite central-derivative error is 6.06151e-8; it is within its
prospective finite-amplitude plus roundoff bound. The tabulated exact/Taylor/
Kubo errors are stored worker comparisons authenticated and reviewed here,
not a new independently propagated trajectory. All 1,631 reported residuals
are finite and satisfy their corresponding fixed tolerances.

## Energy and interpretation

For each pulse, turning the copying source on and off supplies or extracts
`epsilon<K>_initial-epsilon<K>_final`. This equals the actual held-energy
change; no work term is discarded. For the native shortest positive pulse,
net work changes from +5.6137860e-5 at age zero to -6.1951054e-5 at age two.
The corresponding count changes have opposite signs. The copied registers
are reversible under their owned Hermitian source; fixed counts during hold
do not imply that subsequent copying operations can only increase them.
This is not destruction of global unitary information.

The feedback-off formed state has the same qualitative active copying sign
and phase-sensitive count reversal. Consequently the result does not isolate
incidence feedback as the unique cause. It establishes an actual native
prepared-state writer response, not passive ground-state behavior. That is
useful input for a source/state bridge; it is not yet a macroscopic clock
kinetic term, protected active population, damping law, gravity force,
physical volume/pressure map or observational dark-sector success.

## Custody

All ten source/input members match the new freeze. Its SHA-256 is
`9dde274111747690e7cfab23cd6f184ba6a5db6388a00b59f4d658e393564092`.
The result SHA-256 is
`ca023664cd9798999198ff3999b918a95613798d30ce1d434a318669697c49ea`;
its canonical payload hash and freeze link also match. The exact code and
protocol identities are recorded in `NATIVE_WRITER_PULSE_PREFLIGHT.md`.
No source or frozen evidence was changed in this review.
