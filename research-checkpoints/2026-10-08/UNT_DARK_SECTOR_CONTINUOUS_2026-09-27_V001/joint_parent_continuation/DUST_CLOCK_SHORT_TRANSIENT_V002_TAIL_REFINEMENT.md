# Resolve only the failed nonlinear harmonic tails

2026-10-05 UTC. Prospective continuation. V001 finished in 6.74 seconds with
91/95 numerical controls passing. Four failures concern the relative tail
of the first correction in density/ordinary velocity for k=.01 and .1.
The k=1 case and all time/Fourier controls passed. V001 source/result remain
unchanged; no existing successful case is rerun and no criterion is relaxed.

Keep all physical parameters, the prepared Delta_i=1e-8 source, log-a
interval .05, equations and physical screens. Refine ONLY k=.01 and .1:

- k=.01: retain odd harmonics through4095, with8192 and16384 time steps.
- k=.1: retain odd harmonics through511, with8192 and16384 time steps.

These extend beyond the independently identified finite-k growth maximum
and its declining high-k side. No new spatial scale or physical cutoff is
chosen; these are numerical summation bounds. As the forced correction
blocks have no mutual feedback, truncating saved blocks exactly reproduces
the same lower harmonic sums and avoids duplicate integrations.

Use unchanged linear time tolerance2e-5, correction time tolerance5e-3 and
relative harmonic-tail tolerance.02. Compare the finer high-m cutoff with
its half-cutoff. Add the stricter time-uniform sum of the omitted coefficients
divided by peak full correction as a separate .02 check; this cannot weaken
the original peak-sum criterion. If still unresolved, preserve that result.

This is still a first constitutive correction, not a full nonlinear metric
calculation or a rigorous all-harmonic remainder theorem. Validity screens
are diagnostics, not observation or whole-program acceptance criteria.
One local single-thread process; no other numerical worker is active.
