# Independent review — coherent source/volume V002

2026-09-29. Read-only source/evidence audit and independent analytical check.
I did not implement or execute the production worker and did not repeat its
propagations. The audit read the complete prospective protocol, V002 source,
imported native helper, V001 failure note and exact V001/V002 source diff;
it authenticated saved inputs/results and independently checked every saved
row's phase formula and the full factorial census. No frozen file was edited.

## Disposition

**Accepted within its declared diagnostic scope.** All 72 cases and 1,246
reported numerical checks are present, with no failures. The construction
distinguishes branch-relative identity energies in a coherently controlled
extension. It does not infer a physical coefficient, derive volume, or close
the native-to-gravity bridge.

## Analytical and implementation checks

For arm a, write `phi_a=U_a psi` and `psi_a=exp(-i e_a t) phi_a`.
The worker's controller reduction is
`rho_ab=<psi_b|psi_a>/4`, giving the required **negative** phase
`exp[-i(e_a-e_b)t]`. Its native reduction is the sum of the four arm density
matrices; every scalar phase cancels. The reshape/conjugation conventions in
both reductions implement those formulas, not their complex conjugates.

The source decoder uses arm (g,0) relative to (0,0), divided by the zero-contact
reference at the same g. Its phase is `-c*g^2*t/2`, hence the implemented
`-2*arg(ratio)/(g^2*t)` has the correct sign and normalization. At fixed g,
the two volume arms have exactly the same native Hamiltonian; their contrast
is `exp(-i*alpha*dv*t)` with unit visibility. Both fixed-g volume differences
are checked. The tested phases are safely unaliased: maximum absolute source
phase 0.048 radians, volume phase 0.135 radians.

The native Hamiltonian is assembled from the authenticated original helper
and separately checked against its compact held form. The stored prepared
vectors are used unchanged, including the copying-off blank-record control.
The full 64-state scaled-Taylor propagation is compared with independent
16-state eigensystem propagation, arm by arm. The Taylor stopping expression
is a valid exact-arithmetic exponential remainder bound at the scaled norm;
the protocol correctly does not claim it is a rigorous floating-point error
certificate after squaring. Norm/unitarity/energy/cross-method tests supply
the actual numerical evidence.

Full initial controller dephasing leaves the final controller I/4 because
the Hamiltonian is block diagonal. The global +0.31 identity shift cancels
from the complete density matrix. These controls correctly distinguish
branch-relative energy from an unobservable common energy origin. Retaining
the entire native reduced density also retains its record-clock coherence;
the clock check is not a replacement of the coherent records by occupations.

## Saved evidence independently authenticated

The nine V002 freeze members all match their files. The result's freeze link
and canonical payload hash match. The parent result's status, checks, payload
hash and source-freeze link also authenticate; its five source members are
included in the current freeze. The 72 row tuples are exactly three
preparations x three ages x two durations x four declared (c,alpha) pairs,
with no duplicate or omitted tuple. Every saved phase and decoded coefficient
satisfies the independently evaluated algebraic formula.

Selected maxima from the complete saved census:

| Quantity | Maximum absolute error |
| --- | ---: |
| Full Taylor versus block eigensystem state | 9.30e-16 |
| Unitarity | 6.00e-15 |
| Total held energy | 6.22e-15 |
| Native reduced density | 2.00e-15 |
| Record-clock expectation | 9.93e-16 |
| Decoded c | 2.04e-14 |
| Decoded alpha | 4.78e-15 |

Source-reference visibility is 0.9906766490–0.9991642995, comfortably above
the frozen Duhamel floor of 0.7; volume visibility differs from one only by
roundoff. Reported cost is 0.102899 seconds and 36,323,328 bytes peak self RSS,
not a whole-process-tree memory cap.

Authenticated SHA-256 identities:

    protocol  7e72d36edbf49a17297b2fa46b48c02177007d21215945539bb00ea48c8fe6d9
    source    4d253803a7603b0cad159bf1d2c3b1817548cfba952b4ef8dd37710568494218
    freeze    8711164434c73226b00e5da874283430ced9a82dc4fdee82ea953a3be0cf6572
    result    4024af67d572cb2ee74ca0adf975c140d6f6137668b3228e5bace5cf14e99653

## Technical retry and interpretation boundaries

The exact source diff changes only the freeze filename and its comparison
from encoded JSON to parsed structural equality. V001 and V002 configurations
and all other input identities are identical. This correctly accommodates
0 versus 0.0 serialization without changing the scientific census, equations
or tolerances. The worker executes its own authenticated constants rather
than importing arbitrary executable settings from the freeze. V001's failed
startup and original files remain preserved.

Four qualifications are necessary for interpreting the pass:

1. "State preserving" means invariant **across c/alpha completions at the
   same source arms**. The g-dependent controlled interaction can disturb
   the native state relative to source-free evolution; that is not denied
   or canceled by this test.
2. Two g values identify c only within the already specified quadratic
   family, using its known source-only reference. They do not independently
   establish a quadratic source law or measure an arbitrary local second
   derivative. Similarly, two volume labels test the specified linear
   alpha family, not a general pressure-versus-volume function.
3. Unknown controller self energies, readout phase offsets or an uncalibrated
   source-only reference are confounded with the decoded phases. A physical
   experiment must own them. The protocol explicitly acknowledges this;
   no observed c or alpha has been supplied by the simulation.
4. The four arm labels are adopted operational controls, not dynamical
   geometry, node creation or a cosmological volume. No controller hopping,
   source preparation cost, ruler emergence or GR stress is demonstrated.
   The time-independent hold conserves its declared total energy; that is
   not a complete preparation-and-readout apparatus energy audit.

These are scope limits, not hidden failed controls. The genuine result is an
implemented coherent-channel discriminator that defeats the normalized-native
state ambiguity once extra controller information is available. Predicting
that controller's physical coupling remains the next model-building task.
