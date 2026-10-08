# Independent review: one globally shared hard-gap design

2026-09-29. Complete analytical review of
`GLOBAL_HARD_GAP_SHARED_FEASIBILITY_V001.md`, including a complete reread of
the corrected version at SHA-256
`683bf955a6f70b39cb4a247c01c309db0580faae5b8b06acdd742ca9510bb08d`.
No new state, parameter fit, orbit or propagation was generated.

**The corrected constructive feasible-region argument is accepted.** Two
analytical clarifications were communicated and incorporated before any new
numerical implementation: the weak-field cubic coefficient now includes its
upper-cutoff term, and the declared same-action mixture uses an endpoint-only
coldness test. Their precise content is checked below. The earlier read was
at hash `1891101683cd703a371027c1b06e05910e0d6154d96440beca83c06c71c7300f`;
no frozen numerical output was changed.

## Same-state calibration and budget

The normalization `gstar=cH0 sqrt(3Kb Omega_exc/(2E1))` and the independent
same-parent vacuum equation have the correct factors. At fixed S, stationarity
`RS=R^2 y+y^3` gives exactly `partial_R DeltaU=beta y^4/R>0` by the envelope
theorem. Thus S decreases with R at fixed owned E1 and tends to the specified
soft-plus-harmonic-hard endpoint. Moving fixed weight retains Kb but not the
vacuum baseline; both effects are accounted for.

The fixed-energy logarithmic derivatives of Q_H and E_H(A) are correct.
In particular,
`d ln E_H(A)/d ln R=4(w1-wA)/(1+w1)`; this concerns fixed present energy,
not fixed action. The exact cold-capacity inversion and the radiation
inequality have a common finite-R solution only when the residual hard
budget after retaining Qs is strictly positive. A fixed soft population is
not removed by taking R large.

The finite-epoch total density has the compulsory calibrated dust floor
`Omega_exc/A`. Subtracting that baseline defines a different, nonnegative
excess. Neither photon equality nor the formal quartic coefficient silently
supplies an allowed total early-density threshold. Changed expansion would
also require reconsidering the inherited standard-BBN reference.

## Common preparation and source

Rescaling the hard pulse by `tau=Rt`, `y=Hp Y/R` gives the exact small
nonlinearity `Hp^2/R^4`. Continuous dependence on the fixed dimensionless
duration yields the stated nonzero limiting hard energy. The analogous
soft rescaling gives uniformly vanishing soft excitation on the retained
finite band. These are statements about a **new actual common-pulse family**,
not relabeling the six stored states or freely choosing each mode's action.

The condition `beta Cp Omega_Lambda/Omega_exc>Kb/2` is a valid sufficient,
not necessary, certificate for `S_infinity>Hp`. Strictness provides a margin
at sufficiently large finite R. The inverse bounded-source map is real only
for `|h|<S`. Source work, increasing physical power/bandwidth as duration
shrinks, actual spectral availability, clock mapping and coherent-phase/
orientation preparation remain substantive conditions. The limit is not
uniform in arbitrarily early A, nor an autonomous cosmological production
proof. A phase-averaged scalar force cannot simply replace a coherent state
or the separately qualified vector response.

## Two explicit clarifications

For a finite mixture obeying the same action-scaled dynamics, put
`x_i=E_i/E`. Then
`d w/d ln A=sum x_i d w_i/d ln A+3 Var_x(w_i)>=0`.
Therefore the total coldness condition through a finite A_c needs only its
endpoint, not additional intermediate samples. This uses the already proved
single-mode quartic monotonicity and is not a statement about a driven,
interacting or newly produced population.

At zero lower cutoff but finite upper soft cutoff Lambda, the relaxed
residual force is
`Fsoft=3pi Asoft h^2/16-Asoft h^3/(2Lambda^2)+...`.
An independent derivation subtracts the high-delta tail
`integral_Lambda^infinity Asoft h^3 delta^-3 d delta` from the full continuum.
Consequently the small-G cubic coefficient after bounded-source substitution
is `2/S^2-Asoft/(2Kb Lambda^2)`, not solely `2/S^2`.
The leading quadratic coefficient `1/a0dim=3pi Asoft/(16Kb)` is unchanged.
The revised explicit cubic and its fixed-positive-S remainder are correct.
The removed low band has `0<=F_removed<=Asoft epsilon^2 h/2`, so its
nonpositive contribution to D is bounded by
`Asoft epsilon^2 h h'/(2Kb)`, also as revised. A finite lower cutoff still
requires the stated ordered window; its strict G->0 law is not inferred
from this continuum expression. Keeping both cubic terms small individually
is a valid sufficient criterion and does not assume their cancellation.

These equations specify a useful shared design/calibration problem. They do
not assert observational success, a native unbounded hard spectrum, an
already available controller, a qualified physical early clock, or a solved
galaxy/FLRW field. Legitimate future shared calibration is allowed, provided
all source, vacuum, state and reference consequences are recomputed and its
data use is counted transparently.
