# Bounded blind-integrator repair before the seed wave

The first L4 target/blind control was run after pre-output commit
`af54315da9d97f8ba436946d7e97822411bbd655`.  The target resolved, while the
blind order-four RK4 method returned `UNRESOLVED_HISTORY_L`: its 256/512-step
projective coarse/fine difference was `6.441413836127106e-05`, above the frozen
`2e-7` requirement.  The two methods nevertheless agreed on every promoted L4
trajectory quantity at the expected RK4 error scale and both found no bounded
depletion window.

The initial raw hashes are preserved in `FROZEN_NUMERICAL_REPAIR.json`.  The
repair changes only the blind propagation algorithm: each step now uses one
full RK4 step and two half RK4 steps, combined by Richardson extrapolation.
The target implementation, physical operators, event chronology, capacity and
sector definitions, tolerances, and claim boundary are unchanged.  The blind
grid is reset to 128/256 because the extrapolated step has higher order and
triple RK4 cost.

No L6 or L8 target or blind history existed when this repair was frozen.  The
L4 blind row must be replayed, and the complete L4/L6/L8 wave remains subject
to the unchanged post-output comparison.  Failure after this repair closes the
route rather than authorizing another numerical expansion.
