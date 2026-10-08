# Prepared-state compression: prospective saved-state calculation

2026-09-28. Continue the existing common-current, adiabatic scalar closure;
do not introduce a population, temperature, cosmic normalization or new source.
Use all 36 returned-action cases and every mode from
`PREPARED_ACTION_RETURN_V001_RESULTS.json`, whose SHA-256 is
`b8a0efd517e9492aa2546f83eb7cc81bb3a5553e22ff847f5c6f736b545b9678`.
Authenticate that result, its frozen files, payload and original prepared states.

At zero source the potential is V(y)=delta^2*y^2/2+y^4/4, with unit inertia.
For a common infinitesimal compression, all the existing actions scale by
the same factor q. The already adopted current law gives

    E(q)=sum_j w_j e_j(q I_j),
    P(q)=sum_j w_j [q I_j omega_j(q I_j)-e_j(q I_j)],
    c_ad^2 = (dP/dq)/(dE/dq) at q=1
           = sum_j w_j I_j^2 e_j,II / sum_j w_j I_j omega_j.

This dimensionless thermodynamic response is the sound-speed coefficient
only within that common-current, long-wavelength adiabatic closure. It is not
a derivation of microscopic spatial transport, a physical velocity, a cosmic
abundance or an observational clustering result. The unchanged vacuum baseline
has zero derivative and is not included in these excitation sums.

For positive turning amplitude b define

    Q(theta)=delta^2+b^2*(1+sin(theta)^2)/2,
    J=integral_0^(pi/2) Q^(-1/2) dtheta,
    K=integral_0^(pi/2) (1+sin(theta)^2) Q^(-3/2) dtheta.

Then period=4J, omega=2*pi/period, and

    e_II=omega^2*K/[2J*(delta^2+b^2)].

Use independent orders 64 and 128, preserving both complete answers.
Check the saved actions/periods/energies/pressures; compare analytic e_II
against centered logarithmic-amplitude differences with eps=1e-3 and 5e-4
and their Richardson estimate. For almost harmonic modes, evaluate the
frequency excess without subtracting nearly equal numbers: with
t=b^2*(1+sin(theta)^2)/(2delta^2),
omega-delta=omega*(2/pi)*integral t/[sqrt(1+t)*(1+sqrt(1+t))] dtheta.
Difference those excesses, not the full frequencies. Check positive response without choosing or
discarding modes. Report every case, including all original finite-gap,
time-step and mode-quadrature controls. Main rows remain gap=.001, dt=.005.

Also check the independently derived bounds for r=b^2/delta^2 and
zeta=I*e_II/omega:

    r*(r+1)/[(r+2)*(3r+2)] <= zeta
      <= r*(r+2)/[(r+1)*(3r+4)] < 1/3.

These follow by bounding the logarithmic frequency and action-amplitude
derivatives with the range of r*(1+sin^2(theta))/[2+r*(1+sin^2(theta))].
They imply a positive mixture coefficient below 1/3 for these occupied modes.
Use the same 2e-8 absolute comparison allowance, not a fitted physical bound.

The same positive quartic oscillator also obeys I^2*e_II<=2p, from
the period-weighted quartic moment's nonpositive derivative with stiffness
ratio. Therefore check the exact mixture bound
c_ad^2<=2P/(E+P)=2w/(1+w), with the same 2e-8 allowance. This explicitly
tests whether the existing low pressure bounds the compression response.

Cross-quadrature and inherited identities have tolerance 2e-8; the derivative
check has relative tolerance 2e-7. Numerical errors and closure assumptions
are separate. A new source/protocol freeze precedes the sole subsecond-scale
worker. Atomically publish new files only; retain failures if any. No old
source, numerical result, observation, parameter or acceptance limit changes.
