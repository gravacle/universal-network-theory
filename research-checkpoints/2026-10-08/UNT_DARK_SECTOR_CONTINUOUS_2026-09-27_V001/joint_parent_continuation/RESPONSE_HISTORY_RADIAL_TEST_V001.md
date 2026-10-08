# One common source history: a finite-age radial-shape discriminator

2026-09-28. Analytical and prospective only. No numerical propagation,
galaxy fit, new halo, dissipation, gradient operator, or frozen-law edit.

## Result

The same positive mechanical parent permits a concrete finite-age test:
apply ONE independently specified growth history to different final source
amplitudes, with the same spectrum, inertia, initial-state prescription and
observation times. For constant mode inertia, the modes carrying the relaxed
cubic response become slower as the source weakens. Their controlling
dimensionless age scales as T*sqrt(g), not as a freely selected age at each
radius. A finite-age linear-response coefficient and a source-work bound
give directly falsifiable checks on this proposal.

The attractive stronger narrative—outer response is always delayed, always
smaller, and converges monotonically—is false for this conservative parent.
A valid early positive-response window exists, but subsequent ringing can
overshoot the relaxed response and even reverse a clamped force. The bounded
source supplies a separate exact result: for a monotone ramp from rest,
finite-age force error is uniformly suppressed as g^-3 at high field.

These are CLAMPED-SOURCE predictions. They must not be inserted as a fitted
mu_age into the stationary galaxy equation. FINITE_MODE_CONSTRAINED_RESPONSE.md
shows why: the lapse, shift, clock and collective polarization constraints
alter the actual gravitational evolution. The test here identifies a local
constitutive memory channel; a physical galaxy history must subsequently
satisfy that complete coupled problem.

## 1. Specify the history and keep the complete work ledger

Use the existing fixed-direction bounded mechanical parent. Write G for
the final external acceleration source, H=h(G) for its final internal
amplitude, and u4 for the quartic coefficient:

    h(g)=g/sqrt(1+g²/g_s²),
    V0_delta(y)=kappa*delta²*y²/2+u4*y^4/4,
    m(delta)*y_ddot+kappa*delta²*y+u4*y³
                                  =kappa*delta*h(g(t)),
    nu(delta)=A*delta,   delta_min<=delta<=Lambda,
    K_b=kappa*integral nu ddelta.                            (1)

The finite-band contact belongs to the same modes; no absent-mode contact
is silently retained. All amplitudes use the SAME coefficients, band and
state convention. A definite smooth comparison history is

    g_G(t)=G*f(t/T),
    f(s)=0 for s<=0; f(s)=1 for s>=1,
    f(s)= integral_0^s exp[-1/(v*(1-v))] dv
                         / integral_0^1 exp[-1/(v*(1-v))] dv
                         for 0<s<1.                       (2)

This C-infinity monotone shape is fixed for the comparison, not selected
from NGC3198 residuals. A physically measured different common history can
replace it prospectively. T is a physical source-growth time, not the
duration of a computer calculation. Initially y=y_dot=0 is the declared
classical control preparation; section 6 addresses the actual native state.

With B=integral nu*kappa*delta*y ddelta, the full energy and force are

    E=K_b*g²/2+integral nu[m*y_dot²/2+V0_delta(y)]-h(g)*B,
    F_actual=partial_g E=K_b*g-h'(g)*B,
    D_actual=F_actual/K_b,
    E_dot=F_actual*g_dot.                                    (3)

The compulsory bare contact, interaction and kinetic energy are all present.
Let W_b(g) be its relaxed minimum, B_*(h) its equilibrium polarization, and
E_exc=E-W_b(g)>=0. At the end of a ramp from the zero minimum,

    E_exc(T)= integral_0^T F_actual*g_dot dt-W_b(G)
            = integral_0^T (F_actual-F_relaxed)*g_dot dt >=0.  (4)

Thus excess integrated work is nonnegative. It does NOT imply a pointwise
positive lag: conservative motion can return work over portions of a history.
During the hold E_exc is constant, not dissipated into a hidden bath.

## 2. A new exact error bound for any monotone common ramp

The clamped potential is uniformly convex with curvature at least
kappa*delta². The earlier energy certificate therefore gives

    |B-B_*|² <= 2 K_b E_exc,
    E_exc_dot=(B_*-B)*h_dot.                                 (5)

For the zero-excitation initial condition, integration of
d sqrt(E_exc)/dt <= sqrt(K_b/2)*|h_dot|, justified by a positive-energy
regularization at E_exc=0, yields

    sqrt(E_exc(t)) <= sqrt(K_b/2)*total_variation[h;0,t].

For any monotone fixed-direction ramp from zero to H, and at ANY subsequent
hold age,

    E_exc <= K_b*H²/2,
    |D_actual-D_relaxed| <= h'(G)*H
          = G/[1+(G/g_s)²]².                               (6)

No small-oscillation, slow-ramp or equilibrium assumption enters (6).
It holds at finite positive cutoff and positive m(delta), and extends to a
continuum only where the energy integrals and evolution are controlled.
It explains a definite asymmetry: even large conservative lag/overshoot has
an absolute high-field ceiling g_s^4/G³, while the bound is of order G at
low field, much larger than the relaxed deep response of order G²/a0.

This is an error envelope, not a claim that the actual error saturates it or
has a chosen sign. For an initial excitation E0 in the same mechanical
channel the explicit generalization is

    |D_actual-D_relaxed|
          <= h'(G)*[H+sqrt(2E0/K_b)].                        (7)

An actual active native preparation cannot be replaced by E0=0 merely to
obtain the sharper claim. Vector source rotations replace H in this bound
by the path length of the internal source, not its final magnitude alone.

## 3. An exact finite-age floor and its limited sign theorem

At fixed finite time and small G, h(G*f)=G*f+O(G³), and the quartic term
contributes at O(G³). For the initial control state, with
omega_delta²=kappa*delta²/m(delta), linear response gives

    y_delta(t)=(G/delta)*[f(t/T)
        - integral_0^min(t,T) f_dot(s)*cos(omega_delta*(t-s)) ds]
        +O(G³).                                             (8)

Here f_dot(s) means d[f(s/T)]/ds. At any post-ramp observation t>=T,

    D_actual(G,t)=G*mu_age(t)+O(G³),
    mu_age(t)= integral nu(delta) C_delta(t) ddelta
                                      / integral nu(delta) ddelta,
    C_delta(t)= integral_0^T f_dot(s)
                              cos[omega_delta*(t-s)] ds.      (9)

The same mu_age applies to EVERY sufficiently small G under this shared
history; it is not a per-radius parameter. For a finite band, the neglected
terms can be controlled uniformly on a specified finite time interval.
For constant m and fixed finite Lambda this also controls the soft endpoint:
the finite-time Green bound |sin(omega*t)/omega|<=t yields
y_delta=O(delta*G) uniformly on that time interval. The quartic correction
is O(delta³*G³), and the bounded-source correction is O(delta*G³);
their contributions to integral nu*kappa*delta*y are integrable at zero.
The apparent 1/delta in (8) is therefore not a soft divergence in this
constant-m, finite-time limit. A different inertia or unbounded spectrum
requires its own convergence check.
Generic mu_age is not zero, so the strict finite-age low-field response is
linear, not the relaxed quadratic continuum response. For a true finite
lower cutoff the strict relaxed law is cubic force instead; that order of
limits must also remain explicit.

A useful rigorous positive window exists. If f_dot>=0, t>=T, and
omega_max*t<=pi/2, then all cosine phases lie in [0,pi/2], so

    cos(omega_max*t) <= mu_age(t) <= 1.                     (10)

Within its strict positive part, sufficiently weak sources have
D_actual>D_relaxed in a regime where the relaxed force is quadratic or
cubic. For a prescribed external g, this means less polarization than
needed for the relaxed enhancement. Inverting a separate stationary force
relation would suggest less gravitational enhancement, but that inversion
is NOT a solved dynamical gravity prediction.

The condition in (10) involves the hardest retained frequency and may be
very restrictive. It is a proved sign window, not a claim that a galaxy is
inside it. Later ages have no universal positivity or monotonicity theorem.

### Explicit conservative counterexample

For constant m set c=sqrt(kappa/m). The normalized band cosine kernel is

    K_band(tau)= [2/(Lambda²-delta_min²)]
       *[ delta*sin(c*delta*tau)/(c*tau)
                   +cos(c*delta*tau)/(c*tau)² ]_delta_min^Lambda,
    K_band(0)=1,
    mu_age(t)= integral_0^T f_dot(s)*K_band(t-s) ds.          (11)

For delta_min=0 and a step, at tau=pi/(c*Lambda) it is exactly
K_band=-4/pi². A sufficiently short smooth ramp of the fixed shape (2)
also has a negative coefficient near that hold age, by continuity. Thus a
positive bounded Hamiltonian can exhibit a negative clamped instantaneous
force coefficient, while the hold does no work and its total excitation
energy remains positive. Finite positive delta_min sufficiently close to
zero preserves the counterexample; no zero-gap singularity is required.

Consequently 'older always means more relaxed' and 'outer always lags with
the desired sign' are both falsified as universal claims by this parent.
Dephasing of a continuum force is not loss of mode energy, and discrete
finite bands can recur. The actual observation phase must be predicted by
the common history, not selected to improve a curve.

## 4. Why a low-field delay is nevertheless a definite scaling hypothesis

Use the final INTERNAL source H=h(G), and set

    delta_H=(u4/kappa)^(1/4)*sqrt(H),
    omega_H²=sqrt(kappa*u4)*H/m  for constant m,
    s=delta/delta_H,   y=(H/delta_H)*Y,
    tau=omega_H*t,   eta_G=omega_H*T,
    rho_G=G/g_s.

The exact dimensionless driven equation is

    Y_tau_tau+s²*Y+Y³=s*f_rho(tau/eta_G),
    f_rho(v)=f(v)*sqrt(1+rho_G²)
                               /sqrt(1+rho_G²*f(v)²),       (12)

with cutoffs delta_min/delta_H and Lambda/delta_H. The bounded internal
history is therefore NOT falsely assumed to be the same normalized f at
large external G. At the end or during the hold,

    D_actual=G-H*h'(G)
       +h'(G)*[A*kappa*H*delta_H²/K_b]
              *integral_(cutoffs) s*[1-s*Y(s,tau)] ds.       (13)

The first term in (13) is the compulsory bounded-source contact contribution.
In the controlled deep continuum window its relaxed integral tends to
3pi/16, giving the previous relaxed H²/a0 behavior. Equation (13), not a
substituted relaxation ansatz, is the prospective prediction algorithm.

For G<<g_s and a well-resolved continuum window, the dominant modes have
delta about delta_H and respond on omega_H^-1 proportional to G^-1/2.
Thus ONE physical growth time defines the diagnostic crossover scale

    G_T=m/[sqrt(kappa*u4)*T²].                              (14)

The precise onset is set by (12), state/work and finite-band errors, not by
declaring eta=1 an exact boundary. Increasing the common duration by two
shifts this characteristic source scale by four. That is a falsifiable
cross-amplitude/rate relation without per-radius ages.

The relation is not independent of the native inertia law. If
m(delta)=m0*delta^p on the relevant band, the scaled equation instead has
s^p*Y_tau_tau, and omega_H scales as H^((2-p)/4). Low-source modes are
slower only for p<2; p=2 removes this leading trend and p>2 reverses it.
The weighted stiffness spectrum alone therefore cannot establish the sign
of the time-scale trend. An owned spectral response must measure m(delta).
For p>2 an ideal zero-cutoff band has unbounded zero-field frequencies;
the omega_max sign window in (10) then applies only after retaining a
finite band. It cannot be transferred to that full idealized continuum.

Similarly, equal eta does not by itself imply equal response on a finite
physical band: changing G also changes both dimensionless cutoffs and rho_G.
A proposed scaling collapse must carry those explicit dependencies or bound
their actual-state contributions. The relaxed-tail bound alone does not
bound arbitrary excitation in discarded modes.

## 5. Smallest prospective common-history test

This is a fixed symbolic census, not authorization to choose missing native
inputs or to run a new worker. Once independently fixed G_ref and T0 satisfy
the stated physical source/state/band domain, use:

* Three final amplitudes G_ref/4, G_ref, and 4*G_ref.
* The same shape (2), with two globally applied durations T0 and 2*T0.
* At each duration, three observations: immediately after the ramp and
  after common holds T0 and 2*T0. No amplitude-dependent hold or reset.

At every entry retain F_actual, B, kinetic energy, total energy, excess work
and E_exc. Compare with the same parent's relaxed reference, report signed
differences, and check (4)-(7), (9) where the linear approximation is certified,
and the exact rescaled equation (12). The second duration tests the predicted
common rate scaling; the hold census tests ringing instead of concealing it.
Do not select the best phase, discard a low-field sign reversal, or fit a
separate response time to each amplitude.

Before those outputs can represent a native network rather than this
conditional mechanical control, independently fix:

1. The SAME physical source operator, its contact/energy conversion and its
   physical time and volume calibration. The owned bounded map and its
   scale must be part of that match, not inferred from residuals afterward.
2. Weighted stiffness/source overlaps, quartic and cross-mode coefficients,
   finite-size cutoff and m(delta) from actual-state pole/residue response.
   NATIVE_SOURCE_BRIDGE_DECISION.md supplies an exact first-moment check;
   it does not itself determine the whole inertia function.
3. The prepared state and its independently accounted excitation. The
   already measured native copying response is active and reverses sign
   relative to its blank control. It is neither this deformation source
   nor evidence that its state is a passive mechanical minimum.
4. One physical source history and age, including any spatial variation
   actually justified by formation evidence. T0 and G_ref cannot be inferred
   from the feature this test is supposed to predict. A common history is
   itself a testable modeling hypothesis, not a discovered galaxy fact.

For an actual nonstationary native preparation, first compare each perturbed
history with the same unperturbed aged state and its two-time response.
An equilibrium or stationary susceptibility is not an allowed replacement.
If a positive mechanical reduction fails the measured sign or sum rule,
that rejects this identification at that state; it does not authorize
editing its populations to recover the preferred trend.

## 6. What the result would tell us

The useful question is no longer whether a hand-chosen outer delay can
repair a particular galaxy curve. It is whether an independently calibrated
network response, driven by one owned history, predicts the amplitude/rate
dependence and work measured in this small test. A pass would identify a
specific memory correction to test in the full metric/clock equations; a
failure would isolate inertia, source coupling, state or common-history
assumptions without adding a halo or changing the frozen static force law.

No existing NGC3198 force residual, source profile, lensing result or
cosmological fraction has been used to choose any of the inputs above.
