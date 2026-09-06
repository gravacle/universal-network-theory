# Frozen post-output comparison and classification method

## Scope

This method is applied after the target and independent L10/L12 raw rows have
been written.  It reads JSON records only.  It does not import or execute the
target module and does not construct any native spacetime algebra.

The independent centerline sequence is formed from the sealed L4q2, L6q3,
and L8q4 reference rows plus the independently generated L10q5 and L12q6
rows.  A separate target sequence uses the same sealed reference rows plus
the target L10q5 and L12q6 rows.  Both are classified from scratch.

## Raw comparison

For both new rows, require exact agreement of `(L,q,rho)`, sector and momentum
block dimensions, sparse nonzero counts, and owner-once structural censuses.
Require relative agreement at the protocol limits:

```text
ground energy and Delta_act  2e-8
chi_tau                      5e-7
R_low                        5e-6
```

Also compare response norm/weight and weight floor at `2e-8`.  Residual,
Hermiticity, orthogonality, projection, covariance, matvec, memory, and wall
telemetry are audited against their absolute guards rather than compared as
physical observables.  Independent lowest-five Ritz lists must exist, be
finite and ordered, and their first ground/response entries must reconstruct
the reported ground and active-pole energies within `1e-9`.

## Independent classification

For lengths `(4,6,8,10,12)`, construct

```text
X_Delta = L Delta_act
X_chi   = chi_tau/L.
```

Independently implement the three frozen families:

```text
fixed-z1:      a/L + b/L^2
free-gapless:  a L^(-z)
positive-gap:  Delta_inf + a L^(-z)
```

The free exponents are searched on the exact frozen 15,001-point grid from
`0.25` to `4.0`.  Linear coefficients are solved from explicit scalar normal
equations, not by importing the target fitting functions.  All three models
are scored by five leave-one-size-out squared relative prediction errors.
The log-power exponents of the gap and `chi_tau` are reconstructed by explicit
mean-centered regression.

Apply every frozen Boolean check literally.  All must pass for
`CENTERLINE_Z1_COMPATIBLE_L4_L12`; any failed check yields
`CENTERLINE_Z1_REJECTED_L4_L12`, unless a required row is unresolved.

## Halt and claim boundary

`CENTERLINE_Z1_REJECTED_L4_L12` mandates a halt of this algebraic-scaling
route.  It does not prove that the true exponent differs from one, prove a
positive thermodynamic gap, or close the larger emergence program.  No native
operator-algebra or anomaly calculation is authorized on rejection.
