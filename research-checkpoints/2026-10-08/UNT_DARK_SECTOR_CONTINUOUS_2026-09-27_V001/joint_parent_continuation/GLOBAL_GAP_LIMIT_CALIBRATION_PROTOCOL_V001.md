# Prospective shared calibration of the global-gap limit

2026-09-29. Stdlib-only, stdout-only arithmetic; root owns freeze and execution.
No mode trajectory, fitted radius function, new finite-R population, observed
rotation curve, photon/CMB likelihood or parameter search is included.

## Fixed family and complete census

Use the formal common-pulse R->infinity family in
`GLOBAL_HARD_GAP_SHARED_FEASIBILITY_V001.md`: beta=.005, n=8,
Cp=pi^2*n^2/8, vanishing soft actions, and limiting hard energy
E=beta*Cp*Hp^2. This is neither an old returned-action template nor one of
the six finite-gap pulse outputs. The actual coherent pulse does not thereby
become an isotropic population or a static scalar galactic state.

Retain the four DISTINCT stored soft quadratures epsilon={.001,.002} and
node order={64,128}, with exact existing nodes/weights. Verify that all old
duration/dt copies of each quadrature agree; they are not additional physical
spectra. Combine each with ALL18 inherited H0/vacuum/BBN reference alternatives,
giving72 branches. Keep their original metadata and the late-time-flat,
radiation-omitted reference assumption. No reference is selected by agreement.

The fixed acceleration target a0=1.2e-10 m/s2 is ALREADY EXPOSED historical
input. It calibrates the formal soft-quadratic coefficient, not an unused
prediction or proof that the corresponding asymptotic window exists. With
Kb=sum(weights)+beta and a0dim=16*Kb/(3*pi), compute

    gstar=a0/a0dim,
    Ereq=3*Kb*Omega_exc*(c*H0)^2/(2*gstar^2),
    Hp=sqrt[Ereq/(beta*Cp)],
    Qsoft(S)+beta*S^2/2=Ereq*Omega_Lambda/Omega_exc.

Use c=299792458 m/s and the inherited Mpc conversion. Qsoft is evaluated
from the unique roots delta^2*y+y^3=delta*S at the ACTUAL stored nodes.
There is no independent vacuum adjustment or abundance. The hard endpoint
is exactly beta*S^2/2 only in this specified limit.

## Numerical method and independently checked identities

The positive cubic uses its hyperbolic-sine closed form. At each calibrated
endpoint, source-bound probe Hp and each field probe, compare it against80
independent monotone cubic bisections with the analytic upper bracket
min(h/delta,cuberoot(delta*h)). The S root uses80 bisections and an initial
upper bracket sqrt(2*target/beta), valid because the hard endpoint alone
reaches the target there. No adaptive tolerance/precision choice is allowed.

Check cubic residuals, endpoint reconstruction, weighted contact identity,
physical excitation/vacuum reconstruction, the calibrated acceleration
identity and the exact gs relation. Algebra/control tolerance is2e-11
relative to the positive expression; identities involving an exact zero use
2e-12 times max(1,contribution scales). Fixed synthetic cubic/parity controls
use delta={.001,.2,1} and h={0,.01,1}; they are arithmetic controls only.
All checks and failures are retained. No force-sign, curve-shape, source
realizability or observational-success threshold determines numerical status.

## Required scientific outputs

Report Hp/S, target minus Qlimit(Hp), the exact source-realizability boolean
Hp<S, and the separate sufficient inequality
beta*Cp*Omega_Lambda/Omega_exc>Kb/2. A failed sufficient inequality is not
automatically a failed exact source condition. An unrealizable branch remains
in the output; its algebraic force is labeled conditional/unrealizable.

For each branch report every asymptotic window scale: epsilon^2, actual
smallest-node squared, upper soft scale1, S, saturation-quadratic crossover
S^2/(2*a0dim), and upper-cutoff cubic crossover3*pi/8. Their minimum/ratio
is descriptive, NOT a rigorous tolerance-certified field interval. Retain
the strict finite-quadrature cubic coefficient
2/S^2+sum(w/delta^4)/Kb separately from the ordered continuum quadratic law.

At each fixed physical field g={1e-12,1e-10,1e-8} m/s2, evaluate the SAME
parameters' exact limiting scalar law

    h=G/sqrt[1+(G/S)^2], G=g/gstar,
    D=G-h'[Bsoft(h)+beta*h]/Kb.

Use its cancellation-free equivalent
D=G*z*(2+z)/(1+z)^2+h'*sum(w*y^3/delta)/Kb,
z=(G/S)^2. Cross-check the direct expression and independent cubic roots.
Save gN=gstar*D, mu=D/G, g/gN, actual coefficient-shape ratio
D/(G^2/a0dim), and all individual window ratios. These are field-response
predictions of the limiting conditional scalar model, not disk rotation or
an isotropic-vector result. Compare64/128 results descriptively for every
reference; no quadrature-resolution entry is selected or fitted.

No finite-R cold capacity, radiation coefficient, source work, physical
clock, available gap or actual isotropization is supplied by this limit.
The scalar/metric and finite-R preparation tests remain distinct. Neither
the original galaxy fields nor any old saved state is rescaled or overwritten.

## Custody/publication

`global_gap_limit_calibration_v001.py freeze` authenticates inherited results,
payloads, recursive freezes and the source/protocol/derivation, then prints
the prospective snapshot without solving endpoints or field probes. Root
publishes `GLOBAL_GAP_LIMIT_CALIBRATION_V001_FROZEN.json`. `run` requires exact
source matching, prints a complete wrapper with hashes/checks/all72 branches,
and exits2 on numerical failure. The worker writes no files and disables
bytecode creation. A one-MiB output target is reported, never enforced by
dropping cases. No new software dependency or long-job checkpoint is needed.
