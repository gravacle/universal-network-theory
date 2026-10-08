# Independent homogeneous-dilution result review

2026-09-29. Accepted for the declared same-action scalar-orbit readout. All
42 frozen input identities and the complete canonical payload authenticate.
No roots, quadrature, propagation or fits were repeated in this review.

- Result: `779ea9498572dc8bcbd3f9dc40b7610b097427dde9eb534dcb14345e1d8beb58`
- Freeze: `e3b590115929e9f9b1f7defd5a54b132e449e43fadd7e589dcb1cf7008ed7131`
- Payload: `984af603ab561c019ac1022873719b6e6c14843a3b7df777f6faf3ef3aaf8e29`

Producer evidence contains all 252 rows, 27,684 modal frequencies and 144
old-resolution comparisons. All 568,119 numerical checks passed. Runtime was
4.544785 s and peak self RSS 41,353,216 bytes, not aggregate job memory.
The compressed stdout transport preserved the complete JSON. Independent
saved-data audit passed 7,434 arithmetic comparisons: inherited actions times
the saved frequencies reconstruct every aggregate `E+P` with maximum relative
discrepancy 2.30e-15. Present-state energies/pressures/frequencies, energy
envelopes, all residual-resolution comparisons, contact, and the first two
clock coefficients agree.

The scientific result is useful and restrictive: present coldness is not a
guarantee of past coldness. Under `I(A)=A^3 I(1)`, all original soft templates
have excitation `P/E=.333067–.333327` by `A=1101`, with energy 42.44–255.53
times the backward dust extrapolation. The six hard-pulse states also become
quartic-dominated: `P/E=.327312–.333309`, energy/dust 6.407–101.54. No state or
numerical-resolution alternative was discarded.

Examples retain the same actions throughout:

| State | Present P/E | P/E at A=1101 | E/dust at A=1101 |
|---|---:|---:|---:|
| Original template 6 | 0.000609965 | 0.333067 | 42.4368 |
| Hard R=128, pulse amplitude 4 | 0.00000176481 | 0.332374 | 16.0224 |

This identifies a concrete next requirement for an early cold branch: its
spectrum/action capacity or preparation history must support that branch,
rather than assuming a currently cold oscillator remains harmonic backward
indefinitely. It does not rule out all high-gap spectra, network states, or UNT.

The clock coefficients retain every mode. For the R=128/amplitude-4 state,
the all-mode one-period coefficient remains about 17,333, largely reflecting
the extremely weak soft modes. It must be multiplied by a physically owned
`H tau_star`; no averaging-validity conclusion follows without that clock.
An energy-weighted relaxation of the all-mode condition would require its own
error bound, not silently dropping these modes.

`A` is a conditional inverse scale factor, not a derived observed redshift.
These are excitation pressures, excluding the unchanged vacuum baseline.
The pulse's isotropic ensemble/triad interpretation remains an explicit state
assumption; no actual isotropization, full metric solution, spatial sound speed
or observational expansion fit has been established here.

Reproducible evidence: `homogeneous_dilution_saved_audit_v001.py` and
`HOMOGENEOUS_DILUTION_V001_AUDIT_DATA.json`. Individual new modal energies and
pressures are not stored, so the independent audit reconstructs their aggregate
enthalpy, not every new modal orbit. Curvature and the third clock maximum
remain analytically preflighted producer evidence rather than rerun integrals.
