# Native transport twist: independent preflight V001

2026-09-29. Accepted before inspecting numerical outcomes. This review read
the complete source and protocol; it did not import or execute the producer,
re-form a state, or diagonalize a Hamiltonian.

Reviewed SHA-256 identities:

- `native_transport_twist_v001.py`: `7defe0dea2425aee64a8f490d79d4c14f83fb284f4f97da03f27f7a3bdcbad75`.
- `NATIVE_TRANSPORT_TWIST_PROTOCOL_V001.md`: `247b9227c7ef9ab731f56759a8dd741481a0efbaf03f54fc1316bbe8c5f4e0c6`.
- Associated analytical note `NATIVE_RELATIVE_PHASE_TRANSPORT_TEST_V001.md`: `6e9cc504ae81841c55d73c84f91239ce407e84455f11efc10a32ed8724d4b45a`.

## Independent checks

For the stated orientation, `J=i(|R><L|-|L><R|)` is conventional Pauli Y.
With `H=H_nonhop-t nT`, the exact identities are `i[H,P]=t nJ` and
`[P,[H,P]]=t nT`. Conjugation by `G=exp(i phi P)` gives the implemented
Peierls source, current and contact. Its fixed-state work is
`D(1-cos phi)-j sin phi`; twisting the state at fixed H gives the opposite
current sign. The gauge-transformed-state energy is unchanged. All of these
identities agree with the code, including the unchanged current-square
feedback and complete nonhopping energy.

The analytic record/carrier projectors resolve the original held Hamiltonian.
The separately assembled two-by-two block exponential has the correct sign
and eigenvalue center. The producer restores all three actual formed vectors
at their five original ages and compares their original energy, link, record,
carrier, and hopping-energy readouts. It does not replace the actual state
with its ground state or with a stationary dephased state. Total-record
dephasing is an explicitly separate invariant-channel check.

Both correlated contact/current expectations and their factorized
counterfactuals are retained. Six labeled synthetic states exercise positive,
negative and zero contact/current without turning any of those signs into an
outcome gate. Stable interaction work, rather than a difference of large
complete energies, is used for the small-angle checks.

The input logic pins the original result, manifest, source and BS action;
authenticates the five old manifest members and old payload; verifies the
three preparation names, five ages, dimension and coefficients; and requires
an identical prospective source/protocol snapshot. No scientific inputs or
tolerances are adjusted by the worker.

## Meaning of a pass

A pass qualifies this finite-cell fixed-state source response and its saved
state restoration. A positive contact is not, by itself, a relaxed stiffness:
the single-edge source is a pure gauge and its equilibrium spectrum is
unchanged. The actual state-response kernel, boundary/loop/source ownership,
and canonical/physical normalization remain necessary before identifying a
continuum relative-phase coefficient. Conversely, the fixed-H state twist
has genuine preparation work; gauge equivalence does not make that work
vanish.

No load-bearing implementation or sign defect was found. Numerical results
require a separate saved-result audit. The producer's output-size flag is
only a transport diagnostic, not a scientific test or permission to omit
rows.
