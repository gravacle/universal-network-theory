# Shared galaxy-response and cosmic-potential clock test V001

2026-10-06 UTC. New bounded application of the existing linear-source,
constant-inertia gradient parent. This is not a restart, a refit, a new
vacuum offset, or a native-law adoption. Existing galaxy predictions and all
previous failures remain. Root owns the sole numerical launch.

## Fixed question and normalization

The same positive constant inertia gives omega_max=sqrt(kappa/m)*Lambda.
Use the already varied homogeneous action with C=2M^2/Kb, Kb=kappa*A*Lambda^2/2,
and the inherited static gc=(3*pi/8)*a0. Homogeneous spatial gradients vanish.
No old finite DeltaU is restored after changing to the linear source.

The existing permissive slow-curvature subset has longitudinal curvature
kappa*delta^2+3*u4*q^2 <= m*(chi*H)^2, with chi=3. Its maximum potential is
Uslow/(Kb*gc^2) <= B(alpha), alpha=chi*H/omega_max,

    B(alpha)=alpha^6/27                         (alpha<=1),
             alpha^4/36+alpha^2/18-5/108       (alpha>1).

Converting gc from acceleration to c=1 units, the SAME action therefore gives

    rho_slow_potential/rho_critical
       <= (2/3)*(gc/(c_light*H))^2*B(alpha),
    rho_critical=3*M^2*H^2.

This is an optimistic ceiling on potential energy in the DE-like slow subset,
not a predicted occupation, a universal acceleration criterion, or total
energy. Positive kinetic energy cannot improve its negative-pressure budget.
Adopt H=70km/s/Mpc and a required potential fraction0.7 as EXPLICIT SCALE
ILLUSTRATIONS, not a fit or assertion of a current measured parameter.
Use a0=1.0059833281731022e-10m/s^2 unchanged. Solve the monotone ceiling equality
for alpha_min: it is the FASTEST clock that could meet this specified budget,
even if every allowed slow mode were filled to its curvature ceiling.

## New finite-age galaxy-response application

For s=delta/Lambda in(0,1), x=q/[sqrt(kappa/u4)*Lambda],
beta=g/gc and theta=omega_max*t, the zero-gradient fixed-source equations are

    x''+s^2*x+x^3=s*beta,
    x(0)=x'(0)=0,
    mu_age=D/g=1-(2/beta)*integral_0^1 s^2*x(s,theta) ds.

Hold beta at0.01,0.1,1 after one source step and evaluate ages1,5,10Gyr
using that fastest budget-compatible clock. This is a declared local,
initially unexcited, conservative preparation. The source contact and actual
switching/excitation energy remain; no damping, phase reset or equilibrium
substitution. In a coupled galaxy g need not be externally held; this
constitutive diagnostic is not a self-consistent galaxy or disk evolution.
The full100pc spatial solve is not replaced by these local readouts.
Slower clocks need their own history; no theorem of monotonic finite-age
force over every conservative trajectory is assumed.

There is also a no-scan bound for ALL slower budget-compatible clocks in this
particular preparation. Each step-held mode conserves
x'^2/2+s^2*x^2/2+x^4/4-s*beta*x=0. Thus x cannot become negative for beta>0.
Its equation gives x''<=s*beta, hence x<=s*beta*theta^2/2 and

    0 <= 1-mu_age <= theta^2/4
                      <= (omega_max_allowed*T)^2/4.

This is not a monotonic-response assumption or an equilibrium certificate.
The numerical rows test this independent bound. Nonzero incoming mode energy
or a different source history changes its premises.

Compute the same static positive cubic root s^2*x+x^3=s*beta and its mu_static
for comparison. Neither quantity is a new observed galaxy score. Pre-existing
formation, incoming excitation, variable inertia/spectrum, birth/work or a
different physical clock law can change this comparison and must be retained
and tested as distinct physical inputs.

## Numerical controls fixed before execution

One small single-thread NumPy worker, no installation. Fixed (nodes,steps)
arms are(48,512),(96,256),(96,512),(96,1024),(192,1024), separating
positive Gauss-Legendre spectral and RK4 time refinement at each fixed age.
All9 physical cases retained at all5 arms. Numerical gates: age mu and
full normalized mode position/velocity changes <=1e-8, spectral mu changes
<=1e-8, complete fixed-source energy drift relative to beta^2/2 <=1e-8,
static cubic residual <=1e-12 scaled and96/192 static mu <=1e-8.
An independent weak-source control beta=1e-7 tests the exact linear result
mu=2[sin(theta)/theta+(cos(theta)-1)/theta^2] within1e-10 absolute.
No scientific score threshold, searched coefficient or dropped failed row.
Result and readable report use exclusive creation; source/protocol and three
antecedent hashes are recorded. --execute required; no work on import.

Antecedents: GRADIENT_PARENT_CLOCK_SCREEN_V001.md,
EXPLICIT_MODE_COSMOLOGY_PATHWAY.md and LINEAR_SOURCE_GALAXY_REFERENCE_V001.md.
The last old action used bounded sourcing; its homogeneous oscillator
normalization is retained here, while its finite endpoint vacuum is not.
An internal numerical pass qualifies only the declared cross-domain screen.
All Stage3 lanes remain open.
