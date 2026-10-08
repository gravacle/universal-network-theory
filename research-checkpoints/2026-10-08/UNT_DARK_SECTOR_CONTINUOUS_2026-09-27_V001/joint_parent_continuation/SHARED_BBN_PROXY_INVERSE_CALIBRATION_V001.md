# A shared baryon/gap inverse calibration, with no extra radiation knob

2026-09-29. Prospective analytical construction; no abundance was scored and
no orbit, mode, BBN or spatial producer was run for this note. This extends
the explicitly adopted scalar alpha-one family, not the native BS action.
The PRIMAT fixed-heating **proxy** remains distinct from the conserved
scalar's unqualified abundance prediction. Earlier frozen states remain intact.

## 1. Two shared parameters and the quantities they must change together

Use x=omega_b and the single global hard gap R>1. The latter is above the
soft band, whose upper endpoint is one. It is a constitutive gap ratio;
identification with a native frequency in seconds remains separate. Keep
beta=.005, exposed a0=1.2e-10 m/s2, and each existing soft spectrum. The
two epsilon alternatives are physical alternatives; their 64/128 quadratures
are numerical controls, not four new adjustable spectra.

At each inherited H0/Omega_m context define

    h100=H0/(100 km/s/Mpc), Omega_b=x/h100^2,
    Omega_exc=Omega_m-Omega_b>0,
    Kb=sum(w_soft)+beta, gstar=a0/[16 Kb/(3 pi)],
    L=3 Kb (c H0)^2/(2 gstar^2),
    E=L Omega_exc, e=E/beta, I=I_R(e,0).                 (1)

The inherited normalization is late-time flat with radiation omitted:
Omega_Lambda=1-Omega_m. It is not silently promoted to an exact early-time
flat solution. All 18 old reference labels and their two exposed standard-BBN
baryon benchmarks are retained as provenance/comparison markers. Their actual
H0/Omega_m values give **five** distinct backgrounds after the later common a0
calibration: the central background and four corners. The old reference cases
5--8 repeat cases 1--4 with ancestral a0 values which the later calibration
already replaced. Deduplication saves work, not reference uncertainty.

The exact finite-R endpoint obeys

    Qsoft(S)+beta [R^2 ys^2/2+3 ys^4/4]=L Omega_Lambda,
    R^2 ys+ys^3=R S.                                    (2)

Its positive solution is unique. In particular S is independent of x at
fixed R/background/spectrum: E Omega_Lambda/Omega_exc=L Omega_Lambda.
This cancellation does NOT permit deleting DeltaU or keeping S fixed while
changing R. The energy, action, cosmic frequency/current, and later galaxy
boundary state must all use (1)--(2).

There is no independently inferred radiation abundance, vacuum offset,
per-galaxy gap, halo radius or radial density function. H0/Omega_m remain
conditional reference alternatives, not separately optimized quantities.

## 2. A unique, cheap inverse map from table coordinates to the same state

Let C4=[pi/B(1/4,3/2)]^(4/3), fnu=(7/8)(4/11)^(4/3), and retain the owned
present photon density Omega_gamma. The same action predicts

    Q=beta C4 I^(4/3),
    Delta_proxy=Q/(L Omega_gamma fnu).                    (3)

The table coordinate Delta is therefore only a convenient reparameterization
of R, not a second radiation fit. For any proposed (x,Delta>0), its action is

    I_target=[Delta L Omega_gamma fnu/(beta C4)]^(3/4).   (4)

At fixed Delta this target is independent of x, while its required energy
e=L(Omega_m-x/h100^2)/beta is not. There is a stable exact inverse which
avoids repeated tilted-orbit or energy solves. Put s=b^2/(2 sqrt(e)):

    R^2=sqrt(e)(1-s^2)/s,              0<s<=1,
    I/e^(3/4)=F(s),
    F(s)=(4/pi)sqrt(s) integral_0^(pi/2)
                     cos^2(theta)sqrt(1+s^2 sin^2(theta)) dtheta. (5)

This follows by inserting the turning-point energy into the action integral.
F is strictly increasing; F(0)=0 and F(1)=C4^(-3/4). Solve once for s,
then recover R. Restrict to R>1; candidates outside that original hard-band
ordering remain explicitly unsupported, not fitted into the soft band.
Delta=0 at E>0 is the singular R->infinity limit, not a finite empty state.
It supplies the matched-standard comparator but not a finite physical gap.

For w=p/e, the exact derivatives are

    partial_lnR ln Delta|x= -4(1-3w)/[3(1+w)]<0,
    partial_x ln Delta|R= -4/[3(1+w) h100^2 Omega_exc],
    partial_x ln R|Delta= -1/[h100^2 Omega_exc(1-3w)].     (6)

They follow from I_e=1/omega, I omega=e+p and R I_R=-(e-3p)/omega.
The last derivative warns about conditioning near a quartic, non-hard
endpoint. For every fixed x the admissible positive radiation coordinate has
a unique finite R. A bounded table interval is not an upper bound on R.

## 3. What the two abundance products can and cannot calibrate

Use exactly the already declared Cooke D/H and Aver YpBBN-convention products,
the pinned PRIMAT 2026 table and the qualified interpolation. The old
standard-BBN omega_b posterior is NOT an additional prior/likelihood here:
the measured D/H replaces it. Both abundances are now calibration information;
helium is no longer an unused validation observable in this inverse exercise.
Two continuous model parameters against two abundance channels cannot by
themselves establish superior explanatory/predictive power.

No helium--deuterium covariance has been supplied. Retain signed marginal
residuals, observation and theory marginal sigmas and interpolation allowances.
The inherited independent observation/theory-source assumption permits the
same marginal sigma_i=hypot(sigma_obs,i,sigma_theory,i); it does not imply
cross-observable independence. Define descriptive bands

    |prediction_i-observation_i| <= k sigma_i + b_interp,i,
    k in {1,2,3}.                                      (7)

Display their intersections and profiles, not a joint Gaussian chi-square,
tail probability or exclusion confidence. They have no assigned simultaneous
coverage. Unknown systematic bias and the retained unprovided He3 convention
correction are not manufactured into a bounded nuisance. Matched Delta=0
values at the same x and the separately one-parameter standard contour remain.
Keep the leading T0/eta-coordinate sensitivity separate from the nominal
inherited physical x convention.

The primary table domain x in [.005,.040], Delta in [0,7] is intersected
with Omega_exc>0 and R>1. No extrapolation. Table nodes are authenticated;
the inherited local interpolation qualification is x in [.020,.024], Delta
in [0,3]. Outside-local-qualification contours must carry that status. The
finite numerical contour census is not a proof that no narrow unsampled
global optimum exists. No outcome-selected background or cut-off is discarded.

## 4. Why this proxy constraint is useful but not exact scalar BBN

The original scalar current a^3 I=constant is exact within the adopted fluid
action. Its E(A) is not the table's prescribed heating history. Reuse the
owned fixed-heating H envelope and finite-gap certificate

    A^4 Q <= E(A) <= A^4 Q+A^2 D,
    D=beta R^2 sqrt(C4) I^(2/3).                         (8)

Every newly inferred state must recalculate D/(A^2 Q), rather than borrowing
the old 360-row maximum. A very large R can leave the asymptotic regime at a
specified finite epoch even though Delta is small. The proxy still has a
defined abundance, but closeness to the conserved finite-gap history then
requires its own qualification. Neither the heating H envelope nor (8) is
an abundance-error estimate; self-consistent changed neutrino heating is
also not supplied. Thus even an empty proxy-compatible region would reject
only these conditional assumptions, not all UNT or an exact uncomputed BBN.

## 5. The linked galaxy cost cannot be hidden by the recalibration

The cosmic static hard reaction is

    J=beta[omega^2/e_II+3 I omega].                       (9)

In the controlled cold regime e/R^4<<1,

    Delta = beta C4 (e/R)^(4/3)/(L Omega_gamma fnu) [1+O(e/R^4)],
    J = (4/3) beta R^4 [1+O(e/R^4)],
    J = (4/3) C4^3 L Omega_exc^4 /
                 [(Omega_gamma fnu)^3 Delta^3] [1+O(e/R^4)]. (10)

At fixed baryon allocation, halving the proxy radiation coordinate increases
this cold reaction by approximately eight, not an independently selectable
amount. Profiling x also changes Omega_exc^4, so that factor must be retained.
The finite-field galaxy K_L/K_T are not the tiny cosmic K0; (10) is not a
galaxy nonexistence theorem or a requirement that excitation remain smooth.

The shortest linked test is to carry EACH retained proxy contour state into
the already owned common-phase material equations N omega(I,h)=omega(I_b,0),
using its new I_b, R, S and unchanged source action, then keep the full hard
energy/reaction in the spatial equation. No rescaling of old galaxy fields,
no independent hard density profile, and no deletion of the reaction that
the clamped attribution control deliberately removed. A source-only spatial
test is useful even before a new observed galaxy score. Cosmic matching,
finite-domain clamps and branch/accessibility remain explicit, as before.

## 6. Proposed immediate calculation

Authenticate the old table-proxy receipt, primary table/observations, all 18
reference mappings and actual four soft quadratures. Compute marginal contour
geometry once in (x,Delta), map its prospectively specified points by (5) for
all five backgrounds and both spectra/resolutions, and return the full state,
vacuum match, energy/history bounds and reaction descriptors. This is a small
shared inverse calibration, not a new propagation/formation calculation.
The companion prospective protocol fixes contour sampling, numerical controls,
and output scope before root executes anything.
