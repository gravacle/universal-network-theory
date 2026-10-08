# Phase mean of the actually prepared conservative oscillators

2026-09-28. Additive saved-state test, specified before computing phase means.
Use every end-ramp mode state from every case in
`COMMON_HISTORY_MECHANISM_V001_RESULTS.json`. No new propagation, source
amplitude, time, fit, occupation, heat bath, energy loss or native calibration.

At the fixed final internal source H, each scalar mode has potential
V(y)=delta^2*y^2/2+y^4/4-delta*H*y and its own conserved end-ramp energy.
Find both turning points a<b relative to its exact cubic minimum. Its orbit
mean is the time-weighted, not uniform-coordinate, integral

    <y> = integral_a^b y/sqrt(e-V(y)) dy
                  / integral_a^b 1/sqrt(e-V(y)) dy.

This is a defined stationary phase-ensemble comparator. The calculation
does not assert that any physical galaxy reaches it, replace the actual
finite-time result, discard its excitation, or establish phase mixing of
the constrained gravitational system. In this scalar clamped experiment,
initially zero transverse components stay zero exactly.

For this finite collection of uncoupled held scalar oscillators the same
value is also the exact infinite-time Cesaro mean of the additive force:
each bounded oscillator is periodic, and averaging a finite weighted sum
commutes with the limit. No independent-phase assumption or temperature is
needed for that statement. It does not estimate the finite averaging time
or extend automatically to the coupled metric/clock equations.

Use y=(a+b)/2+(b-a)*cos(theta)/2 to remove endpoint singularities. The exact
factorization is

    e-V(y)=(b-y)(y-a)*Q(y)/4,
    Q(y)=y^2+(a+b)*y+2*delta^2+a^2+a*b+b^2.

Then time weighting is proportional to dtheta/sqrt(Q). Its period in m=1
units is 2*sqrt(2)*integral_0^pi dtheta/sqrt(Q). Determine the roots with
bracketed bisection in x=y-y_star, using the cancellation-resistant excess
potential x^2[(delta^2+3*y_star^2)/2+y_star*x+x^2/4]. Retain every mode's
excitation, both roots, period, coordinate moments, mean kinetic energy and
force. Compare 64/128/256 theta quadratures. Check endpoints, positivity,
the exact orbit equation delta^2*<y>+<y^3>=delta*H, the kinetic virial identity,
and unchanged total energy. Tolerance: 2e-8 relative to the relevant positive
mode energy, force or moment scale; aggregate normalized force quadrature
changes <=2e-8. Report errors and preserve failures. This is a small rerunnable
postprocessor; results are published without overwriting.
