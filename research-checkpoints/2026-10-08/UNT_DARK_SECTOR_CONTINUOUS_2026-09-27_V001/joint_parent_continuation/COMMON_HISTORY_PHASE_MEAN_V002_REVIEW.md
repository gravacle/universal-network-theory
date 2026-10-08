# Independent retained-energy orbit-mean review

2026-09-28. **All 36 saved phase means are authenticated and independently
reproduced.** Each uses the corresponding actual end-ramp excitation; no
temperature, new occupation, state reset or dissipative energy sink is added.

## Mathematics and independent checks

The code correctly uses the unique minimum of
`V(y)=delta²*y²/2+y⁴/4-delta*H*y` and its cancellation-resistant excess energy.
Both turning roots are bracketed and bisected on monotone sides of that
minimum. The factorization and substitution are correct:

`e-V(y)=(y-a)(b-y)*Q(y)/4`,
`Q=y²+(a+b)y+2delta²+a²+ab+b²`,
`y=(a+b)/2+(b-a)cos(theta)/2`.

Time weighting is `dtheta/sqrt(Q)`, not uniform position weighting; the period
is `2sqrt(2)*integral_0^pi dtheta/sqrt(Q)` for m=1. Kinetic energy is `e-V`,
so the orbit equation, `2<K>=<yV′>` virial and total-energy checks have the
correct signs and factors. The derivative h′ and source contact are retained
when converting the mean polarization to mean D.

`common_history_phase_independent_audit.py` authenticates the V002 freeze,
all member hashes, original trajectory result and canonical result seal. It
checks the complete 36-row census and reuses no production orbit quadrature.
Independent periodic midpoint rules at 1024/2048 angles reproduce all aggregate
forces to 1.735e-16 in D/G and periods to 5.268e-16 relatively. Endpoint energies
recomputed in the expanded original potential agree to 4.512e-12 relative to
the positive excitation. All original modes, weights, end-ramp energies and
three numerical resolutions remain present.

Additional explicitly synthetic nonzero-source, small-excitation controls test
the frozen phase routine against independently derived limits:
`period -> 2pi/sqrt(k)`, and
`<y>-y_star = -3*y_star*E_exc/k² + O(E_exc²)`, where
`k=delta²+3*y_star²`. As relative displacement decreases .1→.003, relative
period departure decreases from -9.0601e-5 to -8.0887e-8 and the centroid-shift
ratio approaches 0.999999485. These controls are not new states used to alter
the prepared phase means.

## Six main prepared orbit means

| Final G | Relaxed D/G | Mean D/G, ramp 8 | Mean D/G, ramp 16 |
|---|---:|---:|---:|
| .0025 | .00293803 | .00469201 | .00457821 |
| .01 | .01168042 | .01822797 | .01711490 |
| .04 | .04553192 | .06706046 | .05878999 |

All six means exceed the corresponding relaxed value. The longer ramp gives
a smaller mean departure for these six specified preparations; this observed
ordering is not a general monotonic-relaxation theorem. Unlike selecting a
favorable instantaneous phase, these means retain every oscillator's actually
prepared energy. The result demonstrates a history-dependent **mean** clamped
response in addition to transient ringing.

For this finite collection of uncoupled held scalar oscillators, the result
is exactly the infinite-time Cesaro mean of the additive force: each periodic
orbit has its own time mean, and a finite sum commutes with the limit. No
independent-phase or thermalization assumption is needed for that restricted
statement. It is not a finite-time relaxation certificate. The softest main
mode periods are approximately 123–310 uncalibrated time units, while the
stored trajectories end at time 24/32; those samples alone cannot certify
the infinite-time mean has already been reached.

The source remains externally prescribed, the state is the declared classical
control preparation, and the physical clock/inertia/source matching is absent.
The result does not identify the response of the native active record state,
solve coupled metric/clock/matter evolution, or provide a galaxy correction.
It supplies a defined conservative comparison for that next coupled calculation.

## Publication failure and preserved evidence

V001 completed the in-memory calculation but failed JSON publication on a
NumPy boolean. V002 authenticates and reuses its frozen numerical functions,
converting NumPy scalars only at the publication boundary. The complete V002
result was atomically published and its hashes/checks independently verified.
The subsequent optional console summary failed on the still-unnormalized
in-memory boolean. Therefore V002 is a valid saved numerical artifact, **not
a clean whole-process exit**. Both failure notes and both frozen sources remain;
no tolerance, orbit, energy or numerical input was changed to obtain a pass.

## Custody

- V002 freeze: `bc131f9d81730911dfd3ce8afa3bef21807956977a251900c98b9b50c374fae2`.
- V002 result: `44aa651d0f5d2f103d94538dd2dc56c5225667e359ff35c7f641c64636e8837d`.
- Independent audit script: `19bb15827180f78789ae9ac955509319476dc375599603e2f2e061f24e5519b0`.
- Independent output: `COMMON_HISTORY_PHASE_INDEPENDENT_REVIEW_DATA.json`.

No original trajectory, frozen source or result was changed in this review.

## Addendum: clean V003 publication

The additive `common_history_phase_mean_v003.py` additionally normalizes the
optional console JSON. Its full source was read independently; no numerical
function, state, quadrature or threshold changes. The parent reports a clean
exit. Independent read-only checks authenticate the entire V003 source census,
freeze and saved payload, and confirm that **every scientific payload field is
exactly equal to V002 after excluding only the elapsed-seconds field**. All 36
rows and all checks remain identical. V001/V002 failures and evidence remain.

- V003 source: `b95361077b55ac77f99429b95f805ab060eddcc8740e3dd760d4a9630ee1cb10`.
- V003 freeze: `56e1578b1c30e3dbdb2bf9d2cdf30b34d31ea313065e7f8d399553989682badf`.
- V003 result: `95e7deabf64db1570d90ad0d470fb277764088a3f748505b23f6f0d6eca31da3`.

The independent V002 arithmetic/limit controls therefore also validate the
unchanged V003 numerical content; no duplicate physical propagation was needed.
