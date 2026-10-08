# Native incidence response can be read on the records' own phase

2026-09-28. Exact saved-state short-delay derivative census; all 284 checks
pass. No new formation, finite impulse, new hold age, fitted mass or physical
time conversion was performed.

## Result

The qualified native record phase provides a consistent relational readout
of the SAME incidence-source response. The leading response is positive at
all five inherited ages. The clock's own response to this source begins at
quadratic order in delay, so it does not change that leading sign. Its
state-dependent timing correction is calculable rather than assumed away.

The native phase-normalized strength varies from 0.442793656 to 1.171450854.
Thus the records' own clock does not turn this actual-state response into
a single state-independent source moment. That is a concrete matching
requirement: retain the changing native coherence, rather than fit one
constant mechanical inertia or choose a time rescaling to hide it.

## Complete inherited age census

The impulse convention is H-eta*n*delta(t-w), with eta the integrated
native-time Hamiltonian impulse. In inherited hbar=h=epsilon_r=1 units,
the native-time slope is <X_a>; the equal-record-phase slope is <X_a>/nu.
Each entry below uses its own saved state and held Hamiltonian.

| Age | Native-time slope, native | Equal-phase slope, native | Feedback-off slope, either clock | Blank native-time slope |
|---:|---:|---:|---:|---:|
| 0 | 0.884513623 | 1.152468520 | 0.934864704 | 0.934864704 |
| .25 | 0.886906098 | 1.171450854 | 0.835393822 | 0.835393822 |
| .5 | 0.761131411 | 0.962830452 | 0.560124383 | 0.560124383 |
| 1 | 0.404500862 | 0.442793656 | 0.138476502 | 0.138476502 |
| 2 | 0.581719125 | 0.647721098 | 0.684646748 | 0.684646748 |

The blank record state has no defined phase, so its equal-phase values remain
null. Its incidence response is still measurable in the native evolution
parameter. The feedback-off and blank incidence values coincide because
their incidence/carrier dynamics decouple from record feedback in these
controls; their record coherences are different. Feedback-off is a changed
Hamiltonian, not another state silently pooled with native dynamics.

Within each fixed preparation, the slope variation is resolved by many
orders of magnitude compared with the prospective 2e-11 comparison allowance.
The native equal-phase spread is 0.728657198; the feedback-off spread is
0.796388201. No constant was fitted to either series. Positivity at these five
ages is not asserted as a new continuous-window incidence-slope certificate.

## The measured clock-backreaction coefficient

For a=<A_L+A_R>, the exact complex response obeys

    chi_An(0)=chi_An'(0)=0,
    chi_An''(0)=-i*lambda_R*h*<X_a A>/hbar³.

At fixed readout phase the incidence kernel is

    chi_rel=chi_nn-(m_dot/nu)*Im(chi_An/a),

with the drift, rate and amplitude evaluated at the unperturbed readout
endpoint. The first slope per phase is therefore h<X_a>/(hbar² nu), not a
formula with two inverse clock rates. A consistent change of time variable
keeps the integrated impulse eta unchanged.

For a positive small native impulse, the coefficients of eta*tau² in the
required readout-time shift are, in age order,

    0.295850756, 0.301294588, 0.246444818,
    0.112151965, 0.181153959.

The corresponding incidence timing corrections are

    +0.085559246, -0.022798272, -0.093890962,
    -0.050135785, +0.059410961.

These are Taylor coefficients, not a simulated finite kick. Their signs
change with the actual incidence drift. Feedback-off has zero clock
backreaction at all delays by an exact operator identity. Blank phase
corrections are undefined, not zero-valued substitute clocks.

## Scope, checks and custody

Full original-matrix nested commutators verify every first/second-delay
coefficient, including complex quadratures and all factors of two. The
laboratory strength independently matches the older saved incidence-flip
energy, and the phase rate/readout matches the qualified phase-clock result.
The maximum worker residual is 2.78e-15. Execution took 0.0215837 seconds
and 37,437,440 bytes peak self RSS.

The prospective derivation is NATIVE_RELATIONAL_RESPONSE_DERIVATION_V001.md;
it and the protocol/source remain frozen. Independent mathematical/source
preflight accepted the signs and conventions before execution. The saved
result is available for the separate independent result audit.

- Result: native_relational_slope_v001_results.json, SHA-256
  `95d51edcf1b2738bb815c5876ba2e80355feea58c4ed6e837bab2e85f404b6e6`.
- Freeze: native_relational_slope_v001_frozen.json, SHA-256
  `d8a0e6853ba409e1f6465ee09d22ed4bb0a048f73d5e70e26afdaffbfe09251f`.

This establishes an actual-state relational response with a definite source
and clock-backreaction ledger. It is not yet a calibrated gravitational
source, native continuum inertia or physical spacetime clock. Those mappings
must preserve the state dependence just measured; positive finite-cell
response alone cannot supply their missing source/volume normalizations.
