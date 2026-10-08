# Original-spectrum shared calibration: prospective arithmetic census

2026-09-29. Inert source/protocol before execution. This is a conditional
parameter elimination, not a fit, propagation, galaxy prediction or independent
cosmological validation. The root owns the sole worker and publishes stdout.

Keep all36 authenticated `PREPARED_ACTION_RETURN_V001_RESULTS.json` rows and
their exact inherited positive delta/weight arrays from the common-history
result. Keep all18 rows of `COSMOLOGY_CLOSURE_ARITHMETIC.json`, including
duplicated H0/Omega_Lambda cases with different historical acceleration inputs.
Those old acceleration inputs are provenance only, NOT calibration targets.
The census is exactly648 rows; no row, template, cutoff, resolution or BBN
alternative is selected by its outcome. The36 include12 physical histories
and three numerical-resolution controls each, not36 independent populations.

For each template use its unchanged weighted E,P and I0=sum(weights). For each
late-flat reference use Omega_b=omega_b/(H0/100)^2 and
Omega_exc=1-Omega_Lambda-Omega_b. Positive E,H0,Omega_exc,Omega_Lambda give

    g*_SI=c H0 sqrt[3 I0 Omega_exc/(2E)],
    Q(S)=E Omega_Lambda/Omega_exc,
    Q=sum w[delta^2 y^2/2+3y^4/4], y^3+delta^2 y=delta S.

H0 is converted using exactly3.085677581491367e19 km/Mpc, c=299792458 m/s.
The same finite-spectrum endpoint matching rule supplies the vacuum; there is
no adjustable constant, abundance or new high-gap component. Nonpositive-domain
rows would be retained with an explicit status, never silently repaired.

Numerics fixed before outcomes: analytic hyperbolic cubic roots; an initial
lower estimate sqrt(2Qtarget/I0), at most128 upper-bracket doublings, then80
bisections in S. Independently evaluate every final modal root using80 scalar
bisections on [0,min(S/delta,(delta*S)^(1/3))]. Relative numerical gates are
2e-11 for root closure, bracket width, modal cubic/equilibrium comparisons,
positive-energy/contact identities and reconstructed density fractions. Ratios
are normalized to their positive exact target, not a chosen favorable output.
Inherited aggregate E,P and action sums are checked against their actual saved
mode arrays at the same relative tolerance. These are arithmetic controls,
not precision claims about preparation, observations or continuum truncation.

Retain each row's g*, S, gs, target Q, d=2W_el/(I0 S^2), the exact discrete
trial bound, the separately labeled continuum-only d bound, pressure ratio and
Delta q0=3Omega_exc(P/E)/2. Reconstruct both density fractions and the exact
identity gs=cH0 sqrt[3Omega_Lambda/(1-d)]. The positive trial energy is
W_el=sum w[(S-delta*y)^2/2+y^4/4]; its bound is
sum w min(S^2/2,S^4/(4delta^4)). The continuum bound
pi*S/[4(1-epsilon^2)] is NOT imposed as a gate on finite quadrature.

Store the inherited relaxed acceleration reference and the quadratic-window
diagnostic S^2/(2a0_dim), a0_dim=16I0/(3pi), as explicitly non-observational
diagnostics. Changing S changes the bounded source map and actual fixed-action
response; neither the old galaxy fields nor the old seven-source fixed-I
readout can be rescaled into this new prediction. No source-response or action
evolution is run here. Pressure/E is unchanged; matching present densities
does not establish the past expansion, rapid averaging or a cold population.

The result contains36 compact template metadata rows,18 reference rows and648
keyed calibration rows, with full modal ancestors referenced by hash rather
than duplicated. Compact JSON must remain below1MiB. Record all numeric gate
failures in the payload. Source authentication failure stops before arithmetic.
`freeze` prints a full byte snapshot, `run` requires it and prints a complete
result wrapper. Both are stdout-only; neither writes files or starts another
worker. Frozen sources remain unchanged. The inherited standard-BBN and
model-calibrated late-time reference assumptions remain explicit.
