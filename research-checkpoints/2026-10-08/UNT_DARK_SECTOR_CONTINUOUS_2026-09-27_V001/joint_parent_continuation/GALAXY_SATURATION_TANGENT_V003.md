# Complex step validation of the galaxy tangent

2026-10-03. Preserve V001 and V002 failures and all their bytes. V002 did
not supply higher precision: this ARM runtime aliases longdouble to
float64, both with epsilon2.2204460492503131e-16. Its identical failure is
therefore not a second independent derivative test. No tangent solve or
observational result was obtained in either attempt.

Replace only the field-direction acceptance control with end-to-end
complex-step differentiation of the COMPLETE discrete residual at imaginary
steps1e-20 and1e-24, requiring relative agreement1e-10 with the cached
analytic Jacobian-vector action. The independent residual uses the direct
flux formula and sqrt(n*n+t*t); it does not use mu_g, mu_p or the tangent
action. The positive-real field branch is already checked against the
original code. No abs, real cast, clipping, conjugation or branch decision
may enter the complex residual. Preserve the old centered-difference errors
in every result as arithmetic diagnostics, not physical acceptance gates.

This is a change of numerical derivative-validation method, not a claim
that the original controls passed. It removes cancellation in subtraction
of nearly equal field residuals. It does not widen their old tolerance.
Keep parameter-direction finite differences as acceptance controls, plus
all other V001 controls, frozen physical inputs, algorithm allowances,
1e-8 true solve residual and1e-3 shifted-base diagnostic. There is no
software installation, new empirical fit or change to the model.
