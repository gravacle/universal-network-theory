# Independent method: Intrinsic Admission Parent L4 V001

The hostile implementation reconstructs the 256-dimensional retained L4
Hamiltonian as a dense matrix and diagonalizes it completely. This is
independent of the target's matrix-free Taylor propagator and Simpson current
integration.

It retains the complete 16 by 256 reachable loaded/spent and carrier state,
rebuilds each local admission rotation, and applies the dense spectral
transport exponential after every admission. It independently evaluates the
`ALLOW`, blocked, reverse-support, null-state, content, bandwidth, lineage,
and final-charge observables.

The comparison fails closed unless the target passes every frozen check and
the two methods agree within `1e-9` on the promoted admission observables.
The audit must also confirm that the target's node-ledger, norm, and number
guards pass and that at least one blocked component is dynamically nonzero.

The method tests a finite one-pass trace only. It does not promote modal
predicates into generators and cannot certify generic accumulation,
background independence, a continuum sector, emergence, or gravity.
