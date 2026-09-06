# Bounded independent-backend repair

The pre-output independent method was frozen at commit
`877c0da69cafd0eee41ec35c538351fb4eaf82ac`. Its first execution failed before
writing `INDEPENDENT_TRACE_L4.json` for two implementation-only reasons:

1. the environment uses Python 3.9, which does not provide `int.bit_count()`;
2. the installed NumPy/BLAS backend emitted divide-by-zero, overflow, and
   invalid warnings while multiplying finite complex spectral matrices.

The bounded repair replaces `int.bit_count()` with the equivalent
`bin(value).count("1")` and replaces complex BLAS matrix products with explicit
`numpy.einsum(..., optimize=False)` contractions. The dense Hamiltonian,
eigensystem, spectral phase, admission map, thresholds, compared observables,
decision rule, and claim boundary are unchanged.

No independent audit output existed when this repair was made. The target
output existed but was not read to choose or tune either repair. Any warning,
nonfinite value, threshold failure, or target disagreement after this one
repair remains `FAIL_CLOSED`.
