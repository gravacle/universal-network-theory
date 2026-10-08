# Trace regulator: executed result and reciprocal-filter audit

2026-10-05 UTC. No fitted coefficient, no historical calculation repeated.
`trace_regulator_clock_v001.py` completed in 0.000482 s internally; all 26
frozen unit/algebra controls passed. The analytical source, constraints and
group-speed formula were independently reviewed before interpretation.

## Constant, unfiltered trace response

The new trace term can generate spatial clock response from initially zero
response through gradients of expansion. It leaves an aligned K=0 static
force unchanged. It does not decide between uniformly falling and stationary
external-field clocks, generate positive homogeneous dust, or cure the
homogeneous expansion deficit. Its healthy positive-beta branch reduces
G_cosmo at fixed ordinary inventory; its negative-beta enhancement branch
has a scalar ghost in the declared principal window.

If group propagation is required to stay within the matter light cone down
to 10 AU, with ell=100 pc, the instantaneous filtered acceleration plus
UNFILTERED trace term requires:

    beta <= 1.2276850110382013e-26,
    inverse frequency at 1 kpc >= 2.936292849862938e17 years.

Requiring that inverse frequency instead be 10 Gyr needs
beta >= 1.0584873903183676e-11. Within this same dispersion the corresponding
10 AU group speed would be 2.936292849862938e7 c. A revised validity domain
would have to stop at a length at least 0.2627090598 pc for both diagnostic
criteria to hold; that is not a supplied UV completion.

These figures are a conditional linear scale comparison, not a measured
scalar-speed limit or a theorem about all nonlinear galaxy formation.
Preferred-foliation superluminality is not automatically a paradox. The
criterion is explicit so it cannot be silently borrowed or discarded.

## Why a retarded filter cannot just be inserted

For positive local auxiliary quadratic energy
`q^T(M+k²C)q/2-A j^Tq`, M>0, C>=0, the same-source static susceptibility is

    chi(s)=j^T(M+s C)^(-1)j=sum_a w_a/(1+lambda_a s),
    s=k², w_a>=0, lambda_a>=0.

Hence s[chi(s)-chi(infinity)] is nondecreasing. The desired double-pole
response A/(1+ell²s)² violates this property for s>ell^-2. A zero-gradient
mode adds only a constant; a direct constant contact cannot repair the
decaying response. If moments exist, the same class also requires
`chi(0)chi''(0)>=2chi'(0)²`; the double pole already violates this through
order k^4. This is an exact restriction on that reciprocal positive
same-port auxiliary class, not on all constrained/covariant network models.

Introducing a multiplier lambda enforcing
`D b=A`, `D=1-ell²Delta+tau²partial_t²`, in
`L=-W(b)+lambda(D b-A)` produces the mixed kinetic term
`-tau² lambda_dot b_dot`. Generically it has one negative and one positive
kinetic eigenvalue unless genuine additional constraints remove a mode.
Variation of b also requires `D^dagger lambda=W'(b)`; the reciprocal return
filter and its source work cannot be dropped.

A healthy ordinary wave auxiliary instead obeys `Db+W'(b)=A`, changing the
target static functional. Simply substituting a retarded S into W(SA)
returns an advanced adjoint on variation. A causal open-system treatment or
a different constrained local action must be specified rather than claimed.
The two independent analytic reviews support these scoped statements.

## Constructive next alternative

The failed regulator averages acceleration but not clock expansion. A
distinct same-network hypothesis applies the existing filter to BOTH:
`Delta L=-M² beta (S K)²/2`. No second length is introduced. Its zero-field
quadratic dispersion is under independent examination. If it removes the
high-k divergence, that would be a real improvement in this diagnostic,
not an automatic proof of microscopic causality or cosmological success.
The stationary external state, background normalization and full Stage 3
requirements remain open.
