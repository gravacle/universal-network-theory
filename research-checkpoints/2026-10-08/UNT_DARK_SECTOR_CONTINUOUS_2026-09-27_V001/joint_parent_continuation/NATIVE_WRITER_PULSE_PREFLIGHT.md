# Independent writer-pulse preflight

Accepted before execution. This review read the complete proposed code and
protocol and the inherited operator/propagator definitions, checked source
bytes and saved preparation census, and parsed syntax without importing the
worker. No pulse, formation or other physical calculation was executed here.

Reviewed final SHA-256 identities:

- `native_writer_pulse_compute.py`:
  `28476303e45da4bd186e972addd8c49b0fcc91b2dda3a8db408c4687c0b0fb99`
- `NATIVE_WRITER_PULSE_PROTOCOL.md`:
  `943c79be9380ab9e12acfc01c47bfd8eca581a62dcaeb75c0935e67275934318`
- Old result:
  `2b9b19954f137aaf0b60173481fdb9059cda3892ee3c71bd9a6884cbb4b6350a`
- Old freeze:
  `4d22da45549f2de78fc0477be6b5f23bc0f58b3598a312e2aa76d8f729ac9ff3`

The old source members match their manifest. Its three preparation identities,
five saved ages and 1,042 successful checks match the proposed input census.
The new source refuses altered old results, sources or coefficient/age
identities before propagation. The experiment is 3 preparations x 5 ages x
4 durations x 4 signed amplitudes = 240 pulses. Every trial starts from the
same corresponding complex aged vector, without a new formation or a
stationary-population replacement.

## Independent mathematics check

For the explicit plus source `H_epsilon=H+epsilon K`, differentiating the
propagator gives `-i integral exp[-iH(t-s)] K exp[-iHs] ds`. Its energy-basis
divided difference is exactly the implemented continuous sinc kernel,
including degenerate energies. The coupled Taylor recurrence is the upper
block of the exponential of `[[a,b],[0,a]]`; the stated infinity-norm block
tail is a valid exact-arithmetic truncation bound.

The Heisenberg response is `i integral [K(s),O(t)] ds`. The code retains the
full matrices and actual nonstationary state; the 8/16-node quadratures are
checks against the exact spectral derivative, not a diagonal Lehmann
approximation. The source derivative of nested commutators follows
`D_n=[H,D_(n-1)]+[K,ad_H^(n-1) O]`, as implemented. In particular K has zero
first coefficient and second coefficient `-[K,[H,K]]/2`; R has first
coefficient `i[K,R]=Y_L+Y_R` in the inherited minus-Pauli-Y convention.

With L the held spectral width, shifting H by the center of its spectrum
gives `||ad_H||<=L`. There are n source-insertion positions in the nth term.
Summing n>=9 therefore yields the declared remainder
`2||K||||O|| t exp(Lt)(Lt)^8/8!`. Lower time coefficients are not assumed
nonzero; duration ratios remain diagnostics only.

For real epsilon, the nth source derivative has the uniform norm bound
`||O||(2||K||t)^n`. Taylor's theorem gives the central-derivative error
`||O||(2||K||t)^3 epsilon^2/6`. The Richardson combination cancels the common
cubic derivative. Bounding its two fifth-order remainders independently
gives `(4/3)/16/120+1/3/120=1/288`, exactly the conservative coefficient used.
The raw numerical allowance is explicitly divided by epsilon and propagated
through Richardson; no derivative precision is inferred just from a small
change in an order-one expectation.

The finite-copy source is the existing writer source with either sign. Held
record counts commute with H. Their density self-response remains zero,
while writer-copy response need not vanish. For the blank state the linear R
response is zero, but its even finite-amplitude record response need not be.
The prepared-state double-commutator sign is not a claim of negative norm or
a ghost in this finite unitary Hamiltonian.

## Work, scope and correction

During a pulse `H+epsilon K` is constant. Turning it on and off requires
`epsilon<K>_initial` and `-epsilon<K>_final`; their sum equals the change in
held energy. The code checks both pulse-energy conservation and this complete
work ledger. The cancellation-stable unpulsed reference has the same held
energy, so it does not erase a work term.

The only review request was to align the finite positive-pulse sign promise
with code that initially checked only the central odd response. Before any
freeze/run, the author added explicit sign and >10-times-raw-allowance checks
for the actual +.005 pulse at the shortest duration, alongside the central
checks, and aligned the protocol. Those exact changes were re-read.

No remaining preflight blocker was found. A successful run will test an owned
native copying response and its full work/phase dependence. It will not by
itself derive a cosmological clock kinetic term, passive soft spectrum,
autonomous population selection, damping, physical volume stress or a gravity
interface. Input/source custody and exact small-matrix consistency remain
distinct from observational evidence.
