# Independent preflight: same-state central static response

2026-09-29. **Accepted for the declared 42-state census.** Read in full:
producer, protocol, `POLARIZED_STATIC_RADIAL_REDUCTION_V001.md` and
`FIXED_ACTION_SUSCEPTIBILITY_CONSTRAINT_V001.md`. No producer was imported or
executed; no orbit quadrature, action inversion, radial integration or new fit
was performed by this reviewer.

Reviewed source SHA-256:
`123e3112da0bf57029c78cb00ae3d2a44550abad6dc06b2d9bf48097e63082ca`.
Reviewed protocol SHA-256:
`240f85237481e74a47e7091d4247a1740523fc355d17a4540c4e04987c6b4f2d`.

## Independent mathematical checks

For k=delta², the positive angle integral j has
`dj/d(b²) = -u*l/4`, while
`dI/d(b²) = (k+u*b²)/(2*omega)`. Therefore

    e_II = omega²*u*l/[2*j*(k+u*b²)]

is the correct positive scalar fixed-action curvature. The actual census
uses u=1; the separate u=0 control correctly gives zero curvature without
attempting to divide by it. The positive energy root, frequency, action,
second moment and pressure integrands all have the stated normalizations.
The pure-quartic action beta function and J=8e identities provide controls
independent of any desired static result.

The source is b_source=delta in these units, so the per-mode response is
`chi_B = delta²*chi_y`, not chi_y itself. The virial relation gives
`1-chi_B = 3(e+p)/(delta⁴+4e)`; summing these positive deficits is a
cancellation-safe evaluation of Kcal. At zero source, parity removes the
mixed B_I term from the phase-equilibrium derivative. Thus the scalar
fixed-action susceptibility is the appropriate central Jacobian even though
the finite-source phase-equilibrium derivative is different.

On an occupied branch `N*omega=constant`,
`dI/d ln N=-omega/e_II` and `p_I=I*e_II`. Consequently
`d(E+3Pi)/d ln N = -sum w*(omega²/e_II+3I*omega)` exactly. The positive
J/Kcal is a local static differential-operator coefficient, not a measured
length, selected halo boundary or time-growth eigenvalue.

For the six owned finite-spectrum baselines, the displayed a1 and s2 imply

    E+DeltaU+3*(Kb-Kcal)*a1 = -3*Kb*s2.

This agrees with the reconstructed central mass constraint, including the
polarization density. The code checks that identity and retains both signs
of the active center source rather than imposing attraction.

## State, numerical and scope checks

The source binds the exact complete 36 returned states by gap, quadrature,
preparation step, duration and amplitude. Their susceptibility/compression
rows are matched by the same identities; all six pulse states use the actual
fine-endpoint modal data. All 42 are separately matched to the A=1 dilution
records. No original action is replaced by a minimizer or silently dropped.
Read-only hashing verified the pinned input files, their payload digests and
all recursively named ancestral manifest members.

GL64/128 and separately constructed Simpson1024 rules evaluate the positive,
endpoint-safe integrals. Original saved frequencies, actions, pressures,
deficits and the 36 saved compression curvatures supply distinct inherited
checks. The declared energy normalization for tiny-pressure errors and the
relative curvature/deficit comparisons are appropriate; no outcome-dependent
gate or source selection is present.

All actual stored actions are positive. The synthetic b=0 limit has
`e_II=3/(4*delta²)`, but it is not used to populate an exactly empty branch:
an empty copy has no occupied-phase repopulation J. Conversely a positive
occupied action is not deleted merely because it is very small.

Only the six pulse states own the numeric same-finite-spectrum DeltaU used
here. The original 36 center coefficients therefore remain null with an
explicit reason. No infinite-gap matching value, cosmic density, baryon
profile, physical scale or microscopic vector-center regularity is inserted.
The calculation is a conditional averaged radial-scalar diagnostic; it does
not certify the full isotropic-vector transport, global static boundary
solution or its clock stability. No source change was requested.
