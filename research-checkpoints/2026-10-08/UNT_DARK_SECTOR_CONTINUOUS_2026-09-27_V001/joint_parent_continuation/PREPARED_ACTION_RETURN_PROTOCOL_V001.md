# Retained actions: conditional return to zero source

2026-09-28. A small saved-state continuation of all 36 end-ramp cases, not a
new preparation, galaxy fit, real cosmological history or timed unloading run.
For every mode compute its canonical action from its actual held orbit. At
fixed physical volume, define an ideal adiabatic return of the same positive-gap
mode to h=0, conserving that action. Predict its final energy and pressure;
do not choose a temperature or new mode population.

Use both 64- and 128-node angle quadratures. The general turning-point
factorization gives I=r^2/(sqrt(2)*pi)*integral sin^2(theta)*sqrt(Q) dtheta
in m=1 units. At zero source, with positive turning point b,

    I0(b)=(2/pi)*b^2*integral_0^(pi/2)
        cos^2(theta)*sqrt(delta^2+b^2*(1+sin^2(theta))/2) dtheta,
    e0=delta^2*b^2/2+b^4/4,
    T0=4*integral_0^(pi/2) dtheta/sqrt(delta^2+b^2*(1+sin^2(theta))/2),
    p0=I*2*pi/T0-e0.

Solve the strictly increasing I0(b)=I_saved by bracketed bisection, using
the harmonic bound sqrt(2*I/delta). Check action conservation, original
I*omega=2<kinetic>, p0=<y^4>/4, and 0<=p0<=e0/3. A zero action has zero
energy and pressure by continuity. Cross-quadrature relative differences
and modal identities must be <=2e-8 in their relevant positive action or
energy units. Do not clip negative numerical pressure; retain its value and
the stated absolute-in-energy tolerance.

The unchanged baseline cancels from the complete cycle ledger. Original
preparation work is Kb*G^2/2+sum weights*e_h. Return work is sum weights*e0
minus that value. Total cycle work equals the remaining positive mode energy.
Retain every mode, both gaps, both durations, every numerical resolution and
all three amplitudes. The result predicts an ideal state map; finite-duration
adiabaticity, source-controller realization, native matching and the cosmic
normalization remain separate physical questions. Publish without overwrite.
