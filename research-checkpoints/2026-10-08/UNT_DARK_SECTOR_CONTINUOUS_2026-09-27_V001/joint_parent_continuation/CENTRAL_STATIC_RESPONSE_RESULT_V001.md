# Stored state fixes static response; coldness is not weak response

2026-09-29. Completed42-state scalar diagnostic, independently reviewed.
All114773 numerical controls and18942 saved-arithmetic checks pass. These
are the actual36 returned states and six high-gap pulse states; no new
trajectory, halo fit, population or empirical radius was introduced.

The phase-equilibrium condition N*omega=constant fixes
Kcal=Kb-partial_a F and J_static=sum w*(omega^2/e_II+3I*omega).
All4614 modes are retained. Kcal is accumulated as positive susceptibility
deficits. J/Kcal is a STATIC local coefficient, not a time-growth rate or
inferred halo radius. For the36 soft states Kcal=.00186250--.02707549 and
J=.2222244--.2238090. For the six pulses Kcal=4.41218e-9--1.80029e-5 and
J=6993.82--1.78962e6. Hard modes dominate both pulse responses, consistently
with J_hard~(4/3)*beta*R^4 and Kcal_hard~3*E_H/R^4.

Increasing the gap makes the excitation cold while making occupied action
highly sensitive to lapse. These are linked consequences of the oscillator,
not separately adjustable halo ingredients. Tiny occupied soft actions are
retained; their nonzero derivative is not additional stored energy.

The six pulse records own finite-spectrum DeltaU≈13.952. Their ACTUAL
E+3Pi-2DeltaU values are all negative (−27.5094 to−21.5777), so their regular
averaged-scalar center slopes are outward. Effective central density includes
polarization divergence and is also negative. The full mass identity passes.
No old pulse was rematched to a newer cosmological/infinite-gap baseline.
The original36 center values remain null because the selected inputs do
not supply their numeric same-spectrum absolute baseline.

This is a local test of the polarized static equations, not an attractive
halo solution, smooth microscopic vector center or FLRW embedding. On FLRW,
the matched vacuum enters the background equations; deleting it from a static
answer is not that embedding. The next derivation retains finite-gap pressure
and clock on the expanding background before interpreting a static scale as
a galaxy prediction.

Read CENTRAL_STATIC_RESPONSE_V001_RESULTS_REVIEW.md for full results/scope.
Raw CENTRAL_STATIC_RESPONSE_V001_RESULTS.json SHA-256:
7a930081b22bd902ab8f2e4d8cf3547899901cdfe3597416fa6595576a9c9abf.
All52 frozen members match. The one worker exited after.206816seconds,
with44,040,192bytes peak self RSS. No new physical scale was inferred.
