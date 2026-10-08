# Independent review: finite creation-work implementation

2026-09-29. Accepted within its declared clamped-coordinate scope. I read
the complete protocol and implementation, authenticated the five frozen
inputs and saved result, checked the operator algebra independently, and
recomputed census and ledger identities from all saved rows. I did not
run another propagator or simulate a quantum piston. No frozen file changed.

## Custody and complete census

All five SHA-256 entries in `CREATION_WORK_V001_FROZEN.json` match the
resident source, protocol, controller candidate, volume-increment note and
BS microscopic action. The saved configuration equals the frozen one.

- Freeze SHA-256:
  `7b5c94906a5d22569ccdd0131b4ddd4573684d7f785027df47d4941ed7e9769b`.
- Result file SHA-256:
  `4df2603a83a5f1febd297bc20eae802794c9fbb12bfde423c8d41024ea7c0b97`.
- Independently reconstructed canonical payload SHA-256:
  `a9a4046f9183dfbc1ac229dfbd52e579d66c2cd60ae239b0e0cbdd746452d257`.

The result's freeze and payload identities agree. Status is COMPLETE;
5,985 individual consistency checks have no recorded failure. Many checks
are repeated numerical/expectation checks, not independent physical tests.

The exact Cartesian product is present once each: four clamped `(g,V)`
points, three old-link states, four preparations and five times, giving
240 unique rows and 48 initial-energy records. No time or sign was dropped.
Reported runtime is 0.058205958 seconds and peak self RSS is 34,308,096
bytes; this is process self memory, not a measured whole-job bound.

## Operator and physical ledger checks

### The charge test really uses all 36 states

The native direct sum has dimensions 2+16=18 and is tensored with both
supply states. The full charge `n+supply_occupation` has eigenvalues
1, 2 and 3 with multiplicities 2, 18 and 16. Thus its full 36-dimensional
commutator with H is not the tautological commutator with a constant
18-dimensional identity. It vanishes for every clamped point. The actual
preparations lie in the conserved charge-two subspace, as specified.

The raising block includes the old bit and three genuinely blank new
links. Its adjoint annihilates configurations with occupied new links;
the reverse term does not silently delete those occupied links. The
occupation insertion intertwines through that isometry, so the source
term and creation operator commute, as required for the native double
commutator to survive unchanged.

### Creation energy is not pressure alone

With `d=1/2`, the target-minus-source elastic energy is
`d*p_source+K_V*d^2/2`; the quadratic term is `3/8`. Supply loses energy
3, the native degree baseline adds 2, and weakening the retained old
flip supplies `X_old/2`. The independently derived compressed detuning
is therefore `d0*I+X_old/2`, with

| g | V | p_source | p_target | d0 |
|---:|---:|---:|---:|---:|
| 0 | 0.5 | 0 | 1.5 | -0.625 |
| 0 | 0.8 | -0.9 | 0.6 | -1.075 |
| 0.4 | 0.5 | -0.2 | 1.3 | -0.725 |
| 0.4 | 0.8 | -1.1 | 0.4 | -1.175 |

The pressure jump is exactly 1.5, including when initial pressure is zero.
The three new-link leakage channels each have amplitude `-1/2` and
orthogonal images, giving both singular values `sqrt(3)/2`. Compression
is not the complete transition operator and does not establish a sharp
resonance. The implementation retains the full leakage defect.

The saved initial target-minus-source total energies reproduce this
detuning for all 12 old-state/clamped-point choices to
`8.89e-16`: the plus state has `<X>=1`, while blank and phase states have
`<X>=0`. This independently confirms that old-link coherence work, source
energy, supply energy and elastic displacement were not conflated.

The Hamiltonian is separately assembled at displaced clamped coordinates
for its derivative tests. Its exact quadratic contacts are `K_g=2`,
`K_V=3`, `C=1/2`; the positive bare determinant is 5.75. The maximum
recorded discrepancy, `4.5475e-13`, occurs in second finite differences,
well below the frozen `1e-10` allowance. The fixed implementation uses
the declared `hbar=1`; no claim of a general arbitrary-hbar library is made.

### Forward and reverse currents retain their signs

For `T` taking source to target, the exact current is
`2 epsilon Im<T>` in the frozen units. The state `(S+iT_state)/sqrt(2)`
has `<T>=-i/2`, so its initial current is **-0.2**. The opposite phase
has initial current **+0.2**. All 24 corresponding saved checks retain
these signs. Pure source and pure target preparations start at zero
current. For pure source the first three size derivatives are
`0, 0.08, 0`, consistent with probability `epsilon^2 t^2+O(t^4)`.

Currents can subsequently reverse: across retained times the plus-phase
preparations reach positive 0.167734, and the minus-phase preparations
reach negative -0.148254. The result does not impose monotonic growth or
remove a Hermitian reverse channel.

### All component energies remain in the ledger

The component order is native, source, elastic, supply, creation. Using
the saved target probability P and size current J, I independently checked
all 240 rows against

    E_supply = 3*(1-P),          I_supply = -3*J,
    E_elastic = U1*(1-P)+U2*P,  I_elastic = (U2-U1)*J.

Maximum errors are respectively `8.44e-14`, `2.23e-16`, `6.33e-15` and
`2.78e-17`. Source energy/current vanish exactly at g=0. The creation
component is not discarded: its saved energy ranges from -0.165418 to
+0.154733. Its energy and size current also satisfy the independent
coherence bound `E_creation^2+J^2 <= (2 epsilon)^2 P(1-P)` in every row.

Recomputed total-energy conservation error is `1.7054e-13`, and summed
component-current error is `8.05e-16`. The production checks additionally
report charge error `5.62e-14`, full propagator disagreement `4.22e-14`
between eigensystem and scaled Taylor methods, and unitarity error
`4.42e-14`. These are fixed-parameter conservation/implementation checks.
Because g and V are clamped, this run has no piston displacement or
external path work `dg,dV`; internal component exchanges still occur.

## Connectivity is separate from size change

The graph observable is the projector onto connectivity of the underlying
undirected bipartite graph in each size sector. I independently enumerated
the possible disconnection cuts: the connected N=1 bit pattern is 1;
the connected N=2 patterns are exactly 7, 11, 13, 14 and 15. Thus the
implementation's breadth-first connectivity rule agrees with the exact
four-vertex census, rather than treating node count as geometry.

`connected_probability` mixes connectivity in both size sectors and must
not be reported as a newly connected larger graph. The distinct
`larger_connected_probability` projects jointly onto size two and actual
four-node connection. Initially every blank-included target is disconnected.

For pure-source preparations, at time 2 the target-size probabilities
range from 0.0791596 to 0.121904. At that same time, the joint connected
probabilities range from `4.12135e-5` to `1.59139e-4`, and conditional
connection fractions from 0.000338639 to 0.00188722. These independently
recomputed ranges agree with `SOURCE_VOLUME_CREATION_RESULT_2026-09-29.md`.
Across all their retained times, the
largest joint probability of a larger connected graph is only
`1.59139e-4`. Conditional on being in the target sector, the largest
sampled connection fraction is 0.00320987, occurring at time 1, not at
the maximum size probability. These are outcomes of this deliberately
small blank-register preparation, not a general bound on all native
connected preparations. They substantiate the distinction between
creating blank factors and incorporating them into a connected network.

## Scientific disposition

No blocking mathematical, census, custody or numerical-consistency defect
was found. The test establishes an internally consistent **conditional
finite supply/source-work implementation**, retaining pressure jumps,
coherent creation and reversal, and connectedness as separate quantities.
It does not select the added controller constants, simulate the continuous
quantum piston, derive physical volume or a gravitational stress tensor,
or establish cosmological expansion. All inherited native matrices remain
unchanged; the port constants are the declared engineering examples, not
newly measured UNT parameters.
