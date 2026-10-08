# Cold high-gap energy is not yet a quasistatic radial state

2026-09-29. Analytical follow-up to the completed six-case nonlinear pulse;
no new integration, fit, rephasing or altered initial state. Read the saved
`HIGH_GAP_PULSE_V001_RESULTS.json` (outer SHA-256
`3ff381351716259c36d3ef1cca01431e40a73c3deeabcf0bb24df27696617140`,
payload `8e4c812d8a8b84e99a65b492f4899cd263cb6fdd490d9d3f0e7bcf21e788fca1`),
the full uniform-annulus release derivation, and the explicit covariant
mode/cosmology action. The pulse completed all276 computational checks in
3.285752 seconds; these checks do not replace a gravitational release test.

## 1. What the actual state contains

The source returned to h=0. The modes retain real positive energy and a
definite coherent phase, not a mixture of stationary orbit averages.
For the stronger Hp=4 control the saved fine states give:

| Hard gap | B=sum w delta y | V_B=sum w delta v | Averaged P/E |
|---:|---:|---:|---:|
|32|0.003952371874|8.0420699505|4.50682e-4|
|64|0.0002476355474|16.0850240731|2.82328e-5|
|128|0.00001548006905|32.1699184340|1.76481e-6|

The Hp=1 cases have the same qualitative behavior and remain in the argument
below. Increasing the gap lowered the averaged pressure; it did NOT erase
the signed source or its time derivative. In the nearly harmonic hard mode,

    B_H(t)≈wH sqrt(2eH) sin(Omega_H t+phase),
    V_B,H(t)≈Omega_H wH sqrt(2eH) cos(Omega_H t+phase).

At fixed energy and weight, B amplitude stays finite while its derivative
grows with frequency. The selected pulse ends close to a displacement zero,
not near a turning point. At exactly h=0 its instantaneous clamped source
force is -B/Kb, whereas its orbit-average B is zero. These are different
readouts of the same state.

## 2. An exact energy-only crossing theorem for the held state

Continue the saved state under its original CLAMPED h=0 Hamiltonian, only
for this analytical argument. Every modal energy is then separately constant.
Let Es be the soft energy, Ws=sum_soft w, S2s=sum_soft w delta^2, and eH
the hard energy per unit atom weight. Cauchy-Schwarz and positivity give

    |Bs(t)| <= Bsmax=sqrt(2Ws Es),
    |V_B,s(t)| <= Vsmax=sqrt(2S2s Es).                    (1)

Let b>0 be the hard turning amplitude, eH=R^2 b^2/2+b^4/4. If

    wH R b > Bsmax,                                      (2)

then the total B is positive at each positive hard turning point and negative
at each negative one. It therefore has a zero in every intervening half-orbit,
independently of the soft phases. At any such zero define
ymax=Bsmax/(wH R). The derivative obeys the lower bound

    |V_B| >= wH R sqrt(2eH-R^2 ymax^2-ymax^4/2)-Vsmax.   (3)

If this is positive, each crossing is simple. This does not assume harmonic
hard motion or use an uncomputed trajectory.

All six saved cases satisfy these conditions by a wide conservative margin:
Es<1.16e-9, Ws<.5, S2s<.5, eH>78.95 and eH/R^4<.00121.
Consequently Bsmax,Vsmax<3.41e-5, wH R b>0.0627, and the right side of (3)
is greater than2 in the saved time convention. These are rounded outward
bounds on saved energies, not a new numerical propagation or phase selection.

Crucial scope: these guaranteed zeros belong to the continued CLAMPED orbit.
They are not established times visited by a released gravitational solution.
They supply exact candidate states on which to test a proposed release.

## 3. Exact obstruction for one explicitly specified radial embedding

Take the same initial-data class as `UNIFORM_PREPARED_ANNULUS_RELEASE_V001.md`:
R_areal=r, beta=0, p_L=p_R=0, ordinary matter instantaneously at rest,
uniform PHYSICAL modal coordinates and velocities, and an initial metric
solving the full lapse constraint. Canonical momenta are not spatially uniform.
Write f=L^-2, a=sqrt(f)(ln N)', eta=Ndot/N. Exact constraint preservation is

    [D eta'+A]'=0,
    D=N r^2 B h''(a)sqrt(f),
    A=N^2 r^2 V_B h'(a).                                 (4)

This retains the absolute matched baseline, source stress and the actual
mode velocities. It is not a fluid pressure argument.

There is an immediate test at the pulse's actual h=0 endpoint. If one attempts
an unforced resting annulus with constant lapse, a=0 and h''(0)=0. Thus D=0
everywhere, and (4) requires

    (N^2 r^2 V_B)'=0.

For constant N and uniform nonzero saved V_B this is impossible. All six
states have nonzero V_B. They therefore CANNOT be inserted unchanged into
this unforced/momentarily-static uniform radial class, even if the initial
metric constraint itself can be solved. No lapse time derivative repairs
the missing compatibility because its coefficient has vanished.

One may instead declare a nonzero initial a, but that changes the local
interaction energy by -B h(a) relative to this pulse endpoint and must be
included in the preparation ledger. At a candidate held state with B=0,
V_B nonzero, D again vanishes identically; now compatibility requires

    (N^2 r^2 V_B h'(a))'=0.                               (5)

It is generically false for the inherited exponential-lapse weak annulus.
A specially compatible lapse/source profile is a different initial-data
choice, not an automatic consequence of cold pressure. If D has an isolated
spatial zero rather than vanishing everywhere, a finite eta' requires the
integration constant K to equal A at that zero; multiple zeros impose
additional compatibility conditions. The fixed-sign invertibility proof
cannot be continued through a sign change by dividing by D.

This is a specific release-class exclusion, not a proof of a singular metric
trajectory, instability of every coupled state, or failure of UNT. General
time-dependent geometry, nonuniform mode profiles, matter currents and clock
data change the constraint-preservation source and must be retained.

## 4. A genuine time-separation test, not pressure alone

For the same weak-field annulus at nonzero fixed a≈gc, N,f≈1, the exact
initial-release formula reduces to

    eta'_r=(V_B/B)[h'(gc)/h''(gc)] Q(r),
    Q(r)=r_in*r_out/r^2-1.

The bounded source has the exact identity

    h'^2/(h h'')=-gs^2/(3a^2).

Hence the source's fractional change in one hard-frequency time is

    dot(h)/(Omega_H h)
      ≈-[gs^2/(3gc^2)] [V_B/(Omega_H B)] Q(r).           (6)

An adiabatic orbit average needs the absolute value of this expression much
less than one, as well as slow metric/expansion coefficients. Away from a
turning point, a coherent dominant hard mode has V_B/(Omega_H B) of order
cot(phase), not of order1/Omega_H. Raising R alone therefore does not create
this separation. Near a simple B zero the ratio diverges and the exact
compatibility test (5), rather than an averaged force, applies.

For the inherited diagnostic gc=.0025, gs=21.65919852693508, the prefactor
gs^2/(3gc^2) is about2.5e7. The small radius of an annulus reduces eta itself
but not (6) at a fixed radius ratio. The old prepared-annulus result already
demonstrated that distinction; the new high-gap coherent state intensifies it.
This estimate is an initial weak-geometry diagnostic, not an evolved metric.

If a separately owned positive mean polarization B0 dominates a coherent
fluctuation deltaB, a necessary generic small-modulation screen from this
same class is

    |deltaB|/|B0| << 3gc^2/gs^2                           (7)

away from Q=0, since V_B≈Omega_H deltaB. A large frequency does not substitute
for a small amplitude ratio. This is not claimed sufficient for complete
coupled stability or an observational bound.

## 5. Why homogeneous cosmology remains a distinct constructive route

The adopted action has a homogeneous aligned branch with a_mu=0. Under an
explicitly homogeneous/isotropic stress prescription (for example an owned
isotropic ensemble or triad), its equations are

    yddot+3H ydot+R^2 y+y^3=0,
    edot=-3H ydot^2,
    rho_exc=C integral w e,
    p_exc=C integral w(ydot^2/2-V0).

Spatial clock-source divergences vanish on that branch. This alone does not
certify isotropic stress for an arbitrary fixed-direction pulse state: the
chosen vector/metric stress and ensemble must actually be specified and
checked. The saved synthetic pulse is collinear and coherently phased; it is
not already an evolved isotropic FLRW solution. The earlier homogeneous
stress derivation supplies a conditional route, not permission to drop this
state-to-geometry requirement or claim photon/clock identification.

Once that state prescription holds, rapid averaging does not require random
phases. Positivity gives |edot|<=6|H|e, so Omega_H>>|H| is a concrete energy
drift screen over an orbit. One also needs slowly varying background/source
coefficients and negligible inhomogeneous momentum/clock response over the
averaging interval. In the illustrative flat, no-ordinary-matter branch,

    H^2=2(DeltaU+E)/(3Kb),  |Hdot|<=2E/Kb.

These supply additional actual-background separation tests; H is not silently
set to zero. At fixed pulse energy and spectral weight, H stays finite as
R grows while Omega_H grows, so a homogeneous rapid-mode limit can exist.
The available R values have not been evolved through that coupled background
here. Homogeneous viability would not by itself establish radial clustering.

## 6. What a real change of state would mean

An antipodal pair (y,v) and(-y,-v), with normalized weights preserving total
energy, cancels B and V_B at h=0 and remains antipodal under the unforced
even potential. An isotropic orientation distribution can likewise cancel a
vector polarization. Neither is produced by the one common zero-rest scalar
pulse: identical atom copies retain the same phase and orientation. Such
choices are NEW counted preparation assumptions, not evidence of dephasing.

Nor is cancellation a universal cure. Under a common nonzero h, the forcing
has the same sign in both pair members and their antipodal relation is not
invariant. At an exactly cancelled B=V_B=0 initial slice, (4) becomes a
compatibility identity rather than a unique lapse-rate equation; higher-order
constraint evolution and the full mode equations still decide the state.
No damping, phase resets or freely chosen per-radius phases have been added.

The cheapest next discriminator is therefore not another clamped pulse:
retain the full mode/clock initial data and test a clearly specified homogeneous
isotropic branch or a boundary-compatible radial state. The exact algebra above
already rules out a tempting resting radial insertion of these actual coherent
states, while leaving a precise homogeneous averaging route and independently
counted alternative preparations open. A valid low-pressure energy mechanism
and a valid galaxy state must be supplied by the SAME complete action/history,
not joined by replacing a signed source with its orbit mean.
