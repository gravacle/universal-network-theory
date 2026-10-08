# A small high-gap component: cold capacity, force cost, and actual preparation

2026-09-29. New named **conditional spectral extension**, not a modification
of the frozen soft-band parent or its results. Analytical calculation only;
no fit, worker, native-origin assertion, or observational success. This reads
the complete `SHARED_MODE_INFERENCE_AND_STATIC_CLOSURE_V001.md` and the actual
saved-preparation source `common_history_mechanism_v001.py`.

## 1. One spectrum and one matching rule

In the existing dimensionless units set kappa=u4=1 and retain one common
positive inertia m. Replace only the declared measure by

    dnu=A delta ddelta on [epsilon,1] + wH at delta=R>1,
    Ws=A(1-epsilon^2)/2, Kb=Ws+wH, f=wH/Kb,
    C=2M^2/Kb, h(g)=g/sqrt(1+g^2/gs^2).                 (1)

Here f and R are TWO new spectral parameters. An overall change of A and
wH together cancels through C; it is not an independent cosmic abundance.
The complete clamped Hamiltonian is still

    W=Kb*g^2/2+integral dnu [m v^2/2+delta^2 y^2/2
                                     +y^4/4-delta h(g)y].

The covariant interface retains its existing contact bookkeeping and the
same absolute matching RULE; it must not count the contact twice. The hard
energy, force, pressure and endpoint all follow from this same measure.
For an isotropic vector use |y|^2 and its square. Scalar pulse/phase-response
formulas below concern the collinear invariant subspace, not automatic
transport of an isotropic cosmological ensemble into radial scalar modes.

## 2. Cold capacity grows as f R^4, not as a free dust abundance

Let E,P be the total unnormalized zero-source, rapidly orbit-averaged
excitation energy and pressure. Define ebar=E/Kb, pbar=P/Kb. The exact
virial/Jensen bound from the preceding note becomes

    mu4=[A(1-epsilon^6)/6+wH*R^4]/Kb,
    pbar >= ebar^2/[sqrt(mu4+3ebar)+sqrt(mu4)]^2.          (2)

This applies also to bounded vector orbits. It is the SAME positive parent,
not an independently appended pressureless fluid. A small f can substantially
increase mu4 by taking R large. The physical excess density is 2M^2 ebar.

For a scalar hard orbit with energy eH per unit atom weight, let
chi=eH/R^4. The harmonic regime chi<<1 gives

    (P/E)_H = 3eH/(8R^4)+O(chi^2),
    ebar_H=f eH.                                        (3)

Thus cold storage at a fixed ebar_H requires ebar_H<<f R^4, not merely
large R or a small weight. Different vector angular actions change detailed
coefficients, not the exact distribution-independent bound (2). Rapid
averaging itself requires the relevant frequencies to exceed the actual
background variation rate. Instantaneous coherent stress is not dust.

## 3. Exact relaxed force and the coupled vacuum change

The hard minimum is the unique positive root

    R^2 yH+yH^3=R h.

For |h|<<R^2,

    R yH=h-h^3/R^4+3h^5/R^8+O(h^7/R^12).

Let Bs(h) be the soft-band minimum polarization and Fs(h)=Ws*h-Bs(h).
The exact normalized relaxed force of the NEW spectrum is

    D(g)=g-h'[Bs(h)+wH R yH]/Kb
        =g-hh'+h'[Fs(h)+wH(h-RyH)]/Kb.                 (4)

Equivalently D=(1-f)Dsoft+f Dhard with each component normalized by its
own contact. In the soft continuum window epsilon^2<<h<<1, g<<gs,
Fs(h)=(3pi A/16)h^2 plus the already known cutoff corrections. Hence

    D(g)~g^2/a0_new,  a0_new=16Kb/(3pi A).              (5)

At unchanged units this raises the zero-atom coefficient with the SAME
finite cutoff/contact, `16Ws/(3pi A)`, by exactly 1/(1-f). Relative to the
old zero-cutoff reference `8/(3pi)`, the factor is instead
`(1-epsilon^2)/(1-f)`, approaching 1/(1-f) in the ordered epsilon->0 limit.
For epsilon>0 this is an intermediate-window coefficient, not the strict
g->0 asymptote. The hard relaxed correction is order f h' h^3/R^4;
the existing bounded-source term g-hh' remains compulsory. Recalibrating
g* after adding f is possible in a NEW shared inference, not retention of
an unchanged old galaxy prediction.

The owned endpoint baseline also changes. Write ds=DeltaUsoft/Ws and

    dH=-emin,H(gs)=R^2 ys^2/2+3ys^4/4,
    DeltaU=DeltaUsoft+wH dH,
    rho_vac=2M^2[(1-f)ds+f dH],                        (6)

where R^2 ys+ys^3=R gs. In the hard limit R^2>>gs,

    dH=gs^2/2-gs^4/(4R^4)+gs^6/(2R^8)+O(gs^8/R^12).

Increasing R increases cold capacity without making this endpoint grow
as R^4, but the O(f) shift cannot be discarded. If preserving the old
background approximately is desired, require f|dH-ds|<<ds. Otherwise solve
the changed SAME force/vacuum relation jointly. There is no extra vacuum
constant to restore the old background independently.

## 4. Exciting the hard band also changes its response

Cold is not identical to dynamically invisible. For a scalar hard mode,
fixed-action perturbation theory at |h|/R^2<<1 and chi<<1 gives

    e(I,h)=R I/sqrt(m)+3I^2/(8mR^2)-h^2/2
              +3I h^2/(2sqrt(m)R^3)+h^4/(4R^4)+... .  (7)

The first h^2 correction follows by averaging the quartic potential about
the shifted harmonic center h/R. Differentiating at FIXED I gives

    R<y>=-e_h=h[1-3eH/R^4+O(chi^2)]-h^3/R^4+... .

Thus an orbit-averaged excited hard band contributes a leading linear
residual approximately

    DeltaD_H=3 f(eH/R^4)g=3 ebar_H g/R^4,              (8)

not just the small relaxed cubic term. To leave a soft quadratic response
dominant down to a specified positive gmin, a sufficient scale separation
is 3ebar_H/R^4 << gmin/a0_new. This is a finite-window statement, not an
assertion of a quadratic law arbitrarily near zero. In a vector ensemble
the susceptibility requires its actual angular actions and transport;
one cannot silently reuse the scalar coefficient 3.

There is also an exact scalar check, independently obtained in the parallel
susceptibility derivation. For the zero-source hard orbit, with turning
amplitude b and fixed action, the weak-source polarization coefficient is

    d[R<y>]/dh = R^2(R^2+<y^2>)/(R^4+4eH).

Indeed the response to a source -F y is
`xi=(R^2+y(t)^2)/(R^4+4eH)`; substitution into the linearized orbit
equation gives unit forcing, and its turning-point value has the fixed-action
normalization. If z=b^2/R^2, the exact contact deficit obeys

    z/(1+z) <= 1-d[R<y>]/dh <= z(2+z)/(1+z)^2.

It is strictly positive for an excited orbit, independently of the small-chi
expansion. This does not assign a scalar susceptibility to an untransported
vector ensemble.

Before averaging, the hard polarization oscillation instead has amplitude
of order f sqrt(2eH)=sqrt(2f ebar_H), which does not decrease with R at
fixed f,ebar_H. Large R raises its frequency. Its effect on the constrained
metric/clock system must be calculated, not removed by verbal averaging.

## 5. A common pulse must pay for the population

For a mode starting at rest, the linear equation

    m yddot+delta^2 y=delta h(t), omega_delta=delta/sqrt(m)

gives, after a pulse whose source returns to zero,

    e_delta=omega_delta^2/2
                  *|integral_0^T h(t) exp(i omega_delta t) dt|^2. (9)

For a ramp from zero to held hf, the residual harmonic excitation instead
is `|integral hdot exp(i omega_delta t)dt|^2/2`. These are Fourier selection
rules, not a new interaction or a population parameter. The actual inherited
duration-8 ramp uses the normalized derivative exp[-1/(s(1-s))], zero
outside (0,1); its source code is C-infinity flat at the endpoints, not a
quintic smoothstep. Bounded h(g) preserves that regularity. Repeated
integration by parts therefore suppresses hard residual excitation faster
than any inverse power of omega_H*T as that product grows. This conclusion
is specific to that smooth history. No atom was present in the saved run,
and no hard population can be assigned to it retrospectively.

A constructive NEW single common pulse, without mode-specific forcing, is

    h(t)=Hp sin^2(pi t/T) cos(Omega t), 0<=t<=T,
    Omega=R/sqrt(m), T=2pi n/Omega, integer n>=2.        (10)

It is zero outside the pulse. Require |Hp|<gs, so the same bounded source
is realized by `g=h/sqrt(1-h^2/gs^2)`. It is a signed, fixed-direction drive;
an autonomous cosmological or network source producing it is NOT supplied
by this formula. Hp and n are new global preparation choices; T and frequency
are then fixed by R and the already declared inertia, not by galaxy residuals.
The pulse phase is fixed as written. Its epoch/observation age and any later
phase or orientation ensemble must also be fixed independently; if inferred,
they count as additional state parameters. In this zero-rest pulse experiment
there is no independently assigned hard action or abundance parameter.

In the harmonic limit the resonant integral is exactly Hp*T/4, so

    eH=pi^2 n^2 Hp^2/8.                                (11)

There is also an explicit off-resonant bound. Put Rminus=R(1-1/n)>1 and
S4soft=A(1-epsilon^6)/6. Resolving (10) into its three cosine frequencies
gives

    Esoft <= 2Hp^2 S4soft/(Rminus^2-1)^2,
    Esoft/Ehard <=16 S4soft/
                         [wH pi^2 n^2 (Rminus^2-1)^2].  (12)

For example the Fourier factor for frequency omega is proportional to
`(exp(i omega T)-1) omega` times the weighted sum of inverse squared-frequency
denominators. Bounding each denominator below by
`(Rminus^2-delta^2)/m` proves (12). The same linear solution obeys, during
the pulse, `|y_delta|<=2 delta |Hp|/(Rminus^2-delta^2)` for soft delta.
Thus |Hp|/R^2<<1 controls their quartic displacement. For the hard mode,
the additional conditions chi<<1 AND n*chi<<1 keep nonlinear frequency
shift and accumulated resonance detuning perturbative. Equations (9)-(12)
are not claimed exact for an arbitrarily strong nonlinear pulse; a prospective
full Hamiltonian run must test the approximation and energy transfer.

The exact source work, including the compulsory contact, is

    Wsource=integral [Kb*g-B(t)h'(g)] gdot dt,
    B(t)=integral dnu delta y_delta(t).                  (13)

For the closed zero-rest pulse its endpoint energy is precisely Esoft+Ehard,
so Wsource equals that positive retained energy. No energy is obtained from
the matched constant DeltaU. The controller or formation process must supply
this work. This is the opposite of assigning a hidden hard population freely.

All identical atom copies driven from rest remain coherently phased. A single
common pulse does NOT generate a phase-isotropic ensemble or a static halo.
If phase mixing requires a finite hard-band width, that width and its actual
evolution are further named model inputs. Finite-time averaging likewise
requires a justified separation from metric, source and expansion times.

## 6. A nonempty parametric target and its first discriminating test

For a desired positive ebar_H and a positive galaxy interval, the algebra
admits simultaneously: small f; R^2>>max(1,gs,|Hp|); ebar_H<<fR^4;
`3ebar_H/R^4 << gmin/a0_new`; a small endpoint change if required by (6);
and resonant work with `ebar_H~f pi^2 n^2 Hp^2/8`, `n ebar_H/(fR^4)<<1`.
Taking R sufficiently large can meet these inequalities. It demands a faster
source with a real energy budget; it does not demonstrate that native UNT
contains the spectrum, inertia, source or preparation. Raising R also cannot
by itself suppress the unaveraged polarization amplitude.

The smallest informative future test is one prospectively fixed common pulse
on the full soft-plus-hard Hamiltonian, starting from one explicitly declared
state. Record actual signed coordinates/velocities, work, hard and soft energy,
nonlinear detuning and subsequent force response of that SAME retained state.
Do not insert an arbitrary atom energy or append a phase-mean mu to a static
gravity equation. Even small soft residual energy is not automatically proof
of unchanged deep response; use its actual distribution in that response test.
The matched DeltaU and Kb must be recomputed once for the enlarged spectrum,
with no compensating fitted constant. This decides whether spectral separation
can actually produce cold storage at tolerable force/vacuum cost before any
galaxy or cosmological fit.
