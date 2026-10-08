# Independent saved-projector refinement review

2026-09-29. **Accepted as an additive stable arithmetic evaluation on the
unchanged saved projectors.** The full prospective source, protocol and
conditioning finding were read before execution. After root publication,
this reviewer independently recomputed positive block strengths and their
signed moments/derivatives using ordinary Python loops and `math.fsum`.
No eigensolver, producer import, linear solve, propagation or fit was run.

Authenticated SHA-256:

- Producer: `ab88f053eb4417219573d59529f367a5347eedbafc0b0fe5c8bfadeb958efcc0`
- Protocol: `1a0d73348bafe93b94b757825e55272e55139addd567b0d7fbd8646d1253d10b`
- Freeze: `f8c4280959b65af0a6bcaa6b55cd024e87438f249f0eb5132043fc79396f96c6`
- Result: `ec04023f41872c3023005c800ecf20f9fabb358020600d8a7c1b29c54835e8cb`
- Payload: `a4f6fb78a813b25b8e6e9bbf5b293a735d8fe089a9cdbd971274dc4ff3e6c7a8`

All twelve frozen member hashes authenticate. The complete eight-case,
24-space, 191-cluster census is retained. Every old eigenvalue, Hamiltonian,
projector, group field, raw strength, bright collective readout and ground
diagnostic checked against the original output is unchanged. The fixed
source remains H-fM and hbar=1.

For Hermitian orthogonal projectors the positive expression
`||Pa M Pb||_F^2` equals `Tr(Pa M Pb M)`. Independent entrywise compensated
products/sums reproduce the new strengths within `7.11e-15` absolute,
the signed energy-source curvatures within `5.56e-17`, and the signed first
moments within `6.11e-16`. The saved signed denominators, old/new differences,
sensitivity sums and discrepancy flags agree. This independent audit made
5,072 identity/arithmetic checks; the producer reports 400,527 scalar
controls with no failures.

All 24 old/new derivative discrepancies above the original 1e-10 absolute
level remain visible. The largest is `4.658865165325067e-6` in the full-space
q=0, h=.00625 control. This corrects cancellation amplified by a tiny gap in
a secondary weak-flip excited-state derivative. It does not change the
native h=.5 eigenproblem or bright transition-spacing outcome.

The saved residual/gap and spread/gap quantities are correctly labeled
conditioning indicators, not rigorous eigenprojector or relative derivative
error bounds. Positive recombination does not justify arbitrary relative
precision in a nearly forbidden line or nearly degenerate derivative.
The original files remain intact; corrected values have explicit new names
alongside their historical counterparts.
