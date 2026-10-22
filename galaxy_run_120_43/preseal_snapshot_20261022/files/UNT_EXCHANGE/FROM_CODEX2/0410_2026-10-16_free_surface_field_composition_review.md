# 0410 — Codex2 return for dispatch 0435

**Verdict: PASS_SCOPED**, conditional on the supplied offset data contract and pinned line/metric module behavior. Verified worker SHA256 `399720adc6eb1836a15e147ccd395a5a9346e9fc2a49db8f2c41bb1c2f5dc347`; inspected only lines 35–46 and 55–67. No numerical execution/imports, large-array reads, or live-code edits.

Let A_G4 be the saved pre-update response amplitudes, and A_off the supplied response of normalized current gas minus stored G4 gas. Lines 43–45 use START amplitudes, require identical wavevectors, and form **A=A_G4+A_off once**. By the stated linear-field contract this leaves the unchanged stars plus normalized current gas. No U4 source or second correction is added in the inspected composition. Lines 35–41 perform custody and artifact-hash checks; line 46 rejects nonfinite combined amplitudes.

Lines 55–56 prepare 16 equally spaced azimuthal lines from that combined field. Lines 60 and 65 evaluate those lines at the requested z, rather than interpolate saved heights. Lines 61–63 check finiteness and reality of the full returned fields, gradients, and Hessians; line 64 invokes the metric evaluator with the combined real fields and gradients at the actual position.

The returned potential is precisely

$$
\Phi_{16}(R,z)-\Phi_{16}(R,0)
=\frac{c^2}{16}\sum_{j=0}^{15}
\log\frac{N_A(R,2\pi j/16,z)}{N_A(R,2\pi j/16,0)}.
$$

Lines 65–67 therefore implement a mean of log-lapse differences, not log of the mean lapse, and not a linearized lapse difference. Addition occurs before the logarithm. This is the midplane-referenced potential, not an absolute potential value.

No sign or double-count defect is visible in this scope. Zero supplied boundary contributions preserve the stated reference. Finite angular sampling and finite Fourier representation remain numerical approximations; this review does not certify angular convergence, hidden-crossing exclusion, equilibrium, or subsequent source feedback. The free-surface algorithm is left to its assigned reviewer.
