# Independent analytical finite-time response review

The finite-time pathway is mathematically sound under its explicit classical,
separable, source-clamped assumptions. No mode trajectory or new native
measurement was calculated here. It supplies a constructive preparation and
response criterion; it does not establish that the existing native formed
state occupies the required mechanical minima.

## Force band and limits

From `1-z=z^3/s^4`, the omitted relaxed integral below epsilon is bounded by
`epsilon^(alpha+1)/(alpha+1)` and above S by
`S^(alpha-3)/(3-alpha)`. For alpha=1 the complete integral is 3pi/16, giving
the stated `8/(3pi)*(epsilon^2+S^-2)` relative bound. Positive weights and
nonnegative relaxed contributions make this a genuine bound, not a fitted
cancellation. It cannot alone bound an arbitrary excited omitted state.

The strict finite-cutoff small-source limit follows directly from
`y_*=g/delta-u*g^3/(kappa*delta^5)+...`; each net force begins
`u*g^3/delta^4`. Restricting contact and response to the same modes is
essential. The quadratic continuum force requires the intermediate interval,
not merely a small minimum gap.

The zero-initial-state step has linear trajectory
`y=(g/delta)*(1-cos(sqrt(kappa/m)*delta*t))`. Integrating the remaining
contact force against A delta gives exactly the stated sine/cosine expression.
Its t=0 limit is K_b*g. For fixed finite t its small-g expansion is odd and
analytic, with the next term cubic; it is not static minimization. Decay of
a continuum's oscillatory linear coefficient does not erase stored energy.

## Source inertia

Differentiating the stationarity equation gives
`dy_*/dg=z/[delta*(3-2z)]`. Radial and transverse tangent stiffnesses are
respectively `kappa*delta^2*(3-2z)/z` and `kappa*delta^2/z`, both positive.
The driven-oscillator response includes the compulsory kappa contact and
retains its resonant denominator; no damping is implicit.

An independent substitution uses

    d ln(delta) = (3-2z) dz/[4z(1-z)].

It reduces the radial mass integral to
`(A*m/4) integral z/[(3-2z)(1-z)] dz`, whose primitive is exactly
`-ln(1-z)+(3/2)ln((3-2z)/3)`. The transverse integral has integrand
`(A*m/4)*z*(3-2z)/(1-z)` and primitive `z^2-z-ln(1-z)`.
Their large-separation logarithms and radial constant term follow as stated.
The exact positive integrals, not an extrapolated logarithm, determine signs.

Pulling back mode kinetic energy gives `M(g)*g_dot^2/2`. Its Euler–Lagrange
force is `M*g_ddot+M'*g_dot^2/2`, also obtained by the leading displacement
`-m*y_*ddot/k_rad`. For an external saturated source it transforms with h'^2;
the complete static compensation/contact energy remains separate and intact.
The frequency-expansion bound requires a uniformly controlled positive-gap
band. An integrable mass at zero gap is not uniform permission to expand
through arbitrarily small resonances.

## Conservative finite-band preparation

For the quartic mode potential, its Bregman relative energy around y_trial
has the derivative stated in the note. Explicit g derivatives cancel because
V_g is affine in y. The remaining drift term is exactly

    (3*u*y_trial*w^2+u*w^3)*y_trial_dot.

On a fixed positive-cutoff bounded band, uniform convexity controls w^2 by
the relative energy. A smooth ramp on scale T has y_trial_dot=O(T^-1).
The trial correction `-m*y_*ddot/k_rad` cancels the O(T^-2) equation residual;
its acceleration and quadratic Taylor remainder are O(T^-4). Thus
`d sqrt(E_w)/dt <= O(T^-4)+O(T^-1)*sqrt(E_w)` on the small-error interval.
Gronwall integration over time O(T), with initially zero error, gives
sqrt(E_w)=O(T^-3). Flat endpoint derivatives make the trial equal the final
minimum with zero velocity, so the actual endpoint excitation is O(T^-6).
The bootstrap and constants are fixed-band statements, not uniform in a
gapless limit. Subsequent error oscillates rather than dissipates.

Convexity also gives the actual-state certificate
`E_ex >= integral nu*kappa*delta^2*(y-y_*)^2/2`.
Cauchy–Schwarz with `K_b=integral nu*kappa` proves
`|Delta F|^2<=2*K_b*E_ex`, with any positive kinetic excitation included in
E_ex. The one-step soft-band bound follows from its zero initial coordinates
and conserved energy; other histories require their own work ledger.

## Scope clarifications conveyed to the author

When an entire soft band is omitted, add its relaxed contribution and its
actual-state lag error. The two separately bounded terms may each contribute
`8*epsilon^2/(3pi)`; neither alone is the total omitted-state error.
The `T^2 >> M/F_*'` screen describes controlled, low-frequency small radial
modulations (plus the band-frequency restriction). It is not an unconditional
requirement for every stationary or specially correlated source history.
These are budget/wording clarifications, not defects in the displayed proofs.

No analytical blocker was found. The native source/contact, weighted spectrum,
mode inertias, physical time normalization and actual preparation still need
to be owned together. The prior writer-pulse test is an example of measuring
an actual native source response, not an identification of that source with
the passive mechanical spatial deformation.
