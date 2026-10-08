# A universal deep-response coefficient for conservative prepared orbit means

2026-09-28. New analytical result for the already specified **scalar clamped
mechanical parent**. No galaxy data, response-law fit, physical clock calibration,
thermalization, damping, state reset or native UNT identification enters it.

## Result

For a zero-rest preparation followed by any nonnegative, monotone source ramp
of uniformly bounded physical duration, the infinite-time held-force mean has
a common deep-continuum coefficient. It retains the quadratic force law but
differs from the relaxed-ground-state coefficient:

`C_quench = 0.951821896774068...`,
`C_relaxed = 3*pi/16 = 0.589048622548086...`,
`C_quench/C_relaxed = 1.61586303802343...`.

The corresponding leading scalar force-scale ratio is
`a0_mean/a0_relaxed = C_relaxed/C_quench = 0.618864332229065...`.
This is a conditional Hamiltonian prediction, not a newly fitted acceleration
scale. It does not authorize recalibrating the galaxy law or substituting this
mean into a stationary gravity equation.

There is also an exact finite-band statement, not just an asymptotic or
numerical observation: every such monotone-from-rest preparation has
`Dbar >= D_relaxed`, strictly when a positively weighted mode is excited.
The proof below uses the actual nonnegative orbit and Jensen's inequality.
It does not assert that the instantaneous force stays above its relaxed value.

An exact, data-independent bound already shows that the mean coefficient must
be larger than the relaxed one:

`sqrt(2) < C_quench/C_relaxed < 5*sqrt(2)/4`.

Crucially, the order of limits is the held infinite-time mean at each nonzero
source, followed by the soft-continuum/deep-source limit. At fixed finite time,
the earlier linear weak-source response remains valid; there is no contradiction.

## 1. Parent, normalizations and exact mean force

Fix a direction and positive constants kappa,u4,A,m,Lambda. Take constant
positive mode inertia m, positive lower cutoff delta_min initially, measure
`nu(delta)=A*delta`, and its **matching** contact

`Kb = A*kappa*(Lambda²-delta_min²)/2`.

The source map is the same bounded map as before:

`H=h(G)=G/sqrt(1+(G/gs)²)`, with fixed `gs>0`.

Each mode obeys

`m*y_ddot + kappa*delta²*y + u4*y³ = kappa*delta*h(g(t))`.

The full energy retains the contact and interaction:

`E = Kb*g²/2 + integral nu*(m*y_dot²/2+kappa*delta²*y²/2+u4*y⁴/4)
     - h(g)*B`,
`B = integral nu*kappa*delta*y`,
`D = (partial_g E)/Kb = g-h′(g)*B/Kb`.

During a hold, the individually conserved **tilted** mode energy is

`e_delta = m*y_dot²/2 + kappa*delta²*y²/2 + u4*y⁴/4 - kappa*delta*H*y`.

It is distinct from the nonnegative excitation above that potential's minimum.
Negative e_delta does not mean negative excitation; a quench has e_delta=0
and generally positive excitation. Its energy was supplied by source work,
not erased or manufactured by the later mean.

Set

`delta_H=(u4/kappa)^(1/4)*sqrt(H)`,
`omega_H²=sqrt(kappa*u4)*H/m`,
`s=delta/delta_H`, `y=(H/delta_H)*Y`, `tau=omega_H*t`.

At the final held source the dimensionless potential is

`V_s(Y)=s²*Y²/2+Y⁴/4-s*Y`.

For any bounded periodic orbit, or the constant minimum,

`s²*mean(Y)+mean(Y³)=s`.

Consequently the exact finite-band mean force is

`Dbar = G-H*h′(G)
      + [A*sqrt(kappa*u4)/Kb]*H²*h′(G)
        * integral_(delta_min/delta_H)^(Lambda/delta_H) mean(Y³) ds`.   (1)

No cancellation-prone subtraction of a large polarization term is required
to evaluate the final integral. The identity is a force average at fixed
source, not a claim that a whole family of prepared actions is one vacuum
energy function.

## 2. Sudden-step orbit and convergence

A step from rest at zero source to H leaves Y=Y_tau=0 immediately after the
step, hence dimensionless tilted energy zero. Its turning points are 0 and
the unique positive root b(s) of

`b³+2*s²*b=4*s`.

The complete orbit lies in [0,b]. Thus

`s*(1-s*mean(Y)) = mean(Y³) > 0`,
`mean(Y³) <= b³ <= min(4*s,8/s³)`.                           (2)

The last inequality follows separately from b³<=4s and b<=2/s. Its right
side is integrable on (0,infinity). The parameter-free coefficient

`C_quench = integral_0^infinity mean_(energy=0)(Y³) ds`       (3)

therefore exists and is strictly positive.

For hard modes, put Y=Z/s and use oscillator phase s*tau. The equation becomes
`Z_phasephase+Z+s^-4*Z³=1`; at leading order Z=1-cos(phase). Therefore

`mean(Y³) = (5/2)*s^-3 + O(s^-7)`,
`1-s*mean(Y) = (5/2)*s^-4 + O(s^-8)`.

For soft modes b~(4s)^(1/3), and the normalized cubic moment tends to 1/4
as shown below, giving `mean(Y³)~s`. Neither end requires a regulator chosen
from an observed residual.

## 3. Compact integral and exact bounds

Introduce a new compact parameter `z=s*b/2` in (0,1), distinct from the
oscillator position. Then

`b⁴=8*z*(1-z)`,
`s=2^(1/4)*z^(3/4)*(1-z)^(-1/4)`.

With position x=Y/b in [0,1], the normalized orbit-time weight is

`w_z(x) proportional to
 [x*(1-x)*(1+(1-z)*(x+x²))]^(-1/2)`.

Define `R3(z)=mean_(w_z)(x³)`. Straight substitution in (3) gives

`C_quench = sqrt(2)*integral_0^1
 sqrt(z)*(3-2*z)/sqrt(1-z) * R3(z) dz`.                    (4)

Equivalently z=sin²(phi) removes the remaining endpoint weight:

`C_quench = 2*sqrt(2)*integral_0^(pi/2)
 sin²(phi)*(3-2*sin²(phi))*R3(sin²(phi)) dphi`.             (5)

The inner orbit endpoint singularities disappear with
`x=(1-cos(theta))/2`. These two smooth angle integrals supply a direct,
well-conditioned numerical definition; no elementary closed form is claimed.

At z=0 the weight reduces to `[x*(1-x³)]^-1/2`, so beta-function recursion gives

`R3(0)=Beta(7/6,1/2)/Beta(1/6,1/2)=1/4`.

At z=1 it is the arcsine weight, giving

`R3(1)=Beta(7/2,1/2)/Beta(1/2,1/2)=5/16`.

Moreover

`d R3/dz = (1/2)*Cov_z[x³,(x+x²)/(1+(1-z)*(x+x²))] > 0`,

because both functions of x are strictly increasing and the measure is
nondegenerate. Thus 1/4<R3(z)<5/16 in the interior. Since

`integral_0^1 sqrt(z)*(3-2*z)/sqrt(1-z) dz = 3*pi/4`,

equation (4) implies

`3*pi*sqrt(2)/16 < C_quench < 15*pi*sqrt(2)/64`.            (6)

For comparison, the relaxed cubic root satisfies `Y_*³+s²Y_*=s`.
Substitution t=s*Y_* gives
`Y_*³ ds = sqrt(t)*(3-2*t)/(4*sqrt(1-t)) dt`, so
`C_relaxed=integral Y_*³ ds=3*pi/16`. Dividing (6) proves the
stated exact ratio bound without any numerical trajectory or galaxy input.

## 4. Why every finite monotone common ramp has this deep mean limit

Assume the internal source h(t) is nonnegative and nondecreasing from zero
to H, and each mode initially has y=y_dot=0. Its instantaneous tilted energy
satisfies

`e_dot = -kappa*delta*y*h_dot`.

First establish y>=0, rather than assuming it. Until a possible first negative
crossing, y>=0 makes e nonincreasing from zero. At the first y=0,
`e=m*y_dot²/2>=0`, hence e=0 and y_dot=0. If h>0 there, positive
`y_ddot=kappa*delta*h/m` makes the point a tangent minimum, not a crossing.
If h=0, monotonicity implies no earlier forcing. Local uniqueness gives the
same nonnegative continuation. For an upward jump in h, unchanged coordinates
give `e_after-e_before=-kappa*delta*y*Delta h<=0`, so the argument also permits
steps and monotone piecewise-smooth histories.

At the end of any such ramp,

`V_min(H) <= e_delta <= 0`.

Every subsequent held orbit is therefore contained in the same [0,b_step]
interval as the zero-energy step orbit. Bound (2) holds uniformly over the
entire family of monotone preparations. The exact held mean, not a transient
sample, is used here.

### Finite-band mean-polarization suppression theorem

The nonnegative orbit domain proves an additional result before taking any
continuum or small-source limit. Since y³ is strictly convex on the
nonnegative axis, the exact averaged mode equation gives

`kappa*delta²*mean(y)+u4*mean(y)³
 <= kappa*delta²*mean(y)+u4*mean(y³)=kappa*delta*H`.

The left cubic is strictly increasing for mean(y)>=0, and its equality root
is y_star. Therefore `mean(y)<=y_star`, with strict inequality for a
nonconstant orbit. Positive weights and h′(G)>0 imply

`Dbar-D_relaxed = h′(G)/Kb * integral nu*kappa*delta
                 *[y_star-mean(y)] >= 0`.                 (J)

It is strictly positive when a nonzero measure of weighted modes has nonzero
excitation (or at least one in a finite sum). Thus the six positive mean
departures have a general conservative explanation within this preparation
class. No claim of monotonicity with duration or pointwise relaxation follows.
The proof does not apply unchanged to an arbitrary already-active state whose
orbits cross negative y, to vector-source rotations or to a source that reverses.

Now let H tend to zero with constant positive inertia and physical ramp
durations bounded by a fixed finite T_max. For each fixed s>0 the scaled ramp
duration obeys `eta=omega_H*T <= omega_H*T_max -> 0`. The normalized internal
drive lies between zero and one. Positivity and the equation give
`0<=Y_end<=s*eta²/2`, and integration of the equation gives
`Y_tau,end=O_s(eta)`. Hence the final dimensionless energy tends to zero.
Continuity of the orbit mean at energy zero for each fixed s yields the step
mean in (3). The bound `min(4s,8/s³)` permits dominated convergence.

Therefore if simultaneously

`delta_min/delta_H -> 0`, `Lambda/delta_H -> infinity`,      (7)

the finite-band mean integral in (1) tends to C_quench for every such common
ramp. A fixed upper cutoff Lambda>0 satisfies the second condition. One may
take the zero-lower-cutoff continuum first, or a positive-cutoff sequence
satisfying the first condition. **Holding a nonzero delta_min fixed while
H tends to zero does not satisfy (7)** and does not prove a quadratic law.

The statement requires constant positive m (or a separately justified inertia
law with the same vanishing scaled duration). It is not claimed for arbitrary
native m(delta), an active initial state, transverse rotations, nonmonotone
source paths, a thermal/quantum state or source histories whose duration grows
as the soft period. Initial excitations or a duration scaling like H^-1/2 can
retain a different scaled orbit-energy distribution.

## 5. Force law, bounds and order of limits

For the bounded source,

`G-H*h′(G)=G*[1-(1+(G/gs)²)^(-2)]
          =2*G³/gs²+O(G⁵/gs⁴)`.

This is subleading to G²; H=G+O(G³/gs²) and h′=1+O(G²/gs²).
With Kb approaching its matched continuum value, equation (1) gives

`Dbar = [A*sqrt(kappa*u4)/Kb]*C_quench*G² + o(G²)`.

The relaxed coefficient has C_relaxed in place of C_quench, establishing
the quoted ratio of leading a0 scales at **unchanged parent parameters**.
The mass m cancels individual orbit averages; its presence still controls
which finite duration/observation regime reaches or approximates that mean.

For every finite positive band, the infinite-time Cesaro mean of the summed
held force equals the sum of periodic mode means, with no independent-phase
or thermalization premise. In a continuum at fixed H, an integrable bound on
the mode polarization is needed to interchange the average and integral;
the nonnegative orbit interval supplies one for the finite upper band here.
Then take the deep limit using (2) and (7). Nothing here supplies a finite
averaging-time guarantee or pointwise relaxation of a discrete bath.

In particular, the already derived strict finite-time small-G result
`D_actual=G*mu_age(t)+O(G³)` remains unchanged. Its oscillatory coefficient
cannot be replaced by the infinite-time result just because the latter is
positive. Long-ramp relaxation at fixed G is also a different order of limits.

## 6. Numerical coefficient and independent audit

The original `quench_mean_coefficient_v001.py` uses both the compact formula
(5) and an independently changed variable s=tan(phi), at orders 32/64/128/256.
It checks the cubic turning point, both beta/harmonic endpoint moments and
the analytical bounds. Full read of its source finds the transformations and
normalizations correct. Its complete saved result is authenticated.

`quench_mean_independent_audit.py` uses uniform midpoint rules instead of
Gauss-Legendre, including a full periodic inner angle. At 64/128/256/512 points
per angle it independently obtains

`C_quench = 0.9518218967740684`,
`C_quench/C_relaxed = 1.6158630380234318`,
`C_relaxed/C_quench = 0.6188643322290653`.

Its relative difference from the original value is 6.662e-16. This agreement
supports numerical evaluation of a proved definite integral, not empirical
confirmation of a galaxy response. The coefficient was not selected from the
approximately 1.6 ratio noticed in earlier finite-amplitude orbit means.

## 7. Physical meaning and strict scope

The constructive result is that the specified conservative preparation can
retain the same deep quadratic response **without being the relaxed minimum**,
and predicts a different coefficient from its actual history. No arbitrary
per-radius age or fitted law function is needed for this asymptotic statement.
All excitation and source work remain accounted for.

A prepared family is not automatically a single equilibrium action. The
derivative of its energy must retain changes of the orbital actions and the
work of preparation; integrating mean forces while discarding that term would
not establish a new absolute vacuum energy or force–volume relation.

The theorem remains about a scalar externally clamped parent. It neither
calibrates the native source/contact/clock/volume, proves which initial state
the native network forms, supplies cosmological mode abundance, nor solves
the simultaneous matter/metric/clock constraints. No existing galaxy result
has been rescaled or refitted, and no stationary mean-field substitution is
authorized by this mathematical coefficient alone.

## Reproducible identities

- Original coefficient script SHA-256:
  `428da77db4629d943a0ad65a6df62a82d2be19bfd6cff3c4e5bd66c72676015c`.
- Original coefficient result SHA-256:
  `52252d655e366dde098072285b5673a680f44e98e9b551b9a827dc2ce005e749`.
- Original flat payload SHA-256:
  `3f314c7585e465400c5cc93233f9a20393af08975e26c192b81c76a289fb6c1e`.
- Independent audit script SHA-256:
  `552d7309ee0bd4a81d0c1546e8f42f4bab3dec367d2353f8c15b870763186858`.
- Independent full output: `QUENCH_MEAN_INDEPENDENT_REVIEW_DATA.json`.

This analytical note and independent arithmetic are additive. No frozen
calculation, input, observational score or physical parameter was modified.
