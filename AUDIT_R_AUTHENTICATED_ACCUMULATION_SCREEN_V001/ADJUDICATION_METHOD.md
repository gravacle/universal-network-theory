# Fail-closed L4 sign adjudication

The repaired blind history agrees with the target trajectory but exceeds its
own frozen `1e-10` norm guard by `3.402301490827995e-11`.  That row remains
`UNRESOLVED_HISTORY_L`; the guard is not relaxed.

The frozen protocol independently requires the first three signed source
terms to be positive before a depletion sector can exist.  Both iterative
implementations place the third term near `W_3=-0.284`.  A third method may
therefore adjudicate only the sign of `W_3` in the complete 256-dimensional L4
space.  It constructs the Hamiltonian directly, diagonalizes it completely,
forms the transport exponential from all eigenpairs, and evaluates exactly
three write/transport events.

The adjudicator may return only:

```text
CONFIRMED_NEGATIVE_W3__FAIL_CLOSED_HISTORY
UNRESOLVED_W3_SIGN
```

It may not rescue a positive classification or authorize L6/L8.  A negative
upper bound below `-1e-6`, with Hermiticity, eigenpair, unitarity, norm, and
target/blind agreement errors each below `1e-10`, proves the prerequisite
Boolean false at L4.  Since a common L4--L8 sector requires an admissible L4
sector, that result halts the complete seed without running larger sizes.

This is a finite numerical sign certificate for the declared conditional
history.  It is not a continuum, emergence, or gravity result.
