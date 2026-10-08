# Curved shared geometry: a bounded exposed grid

Source-only prospective protocol, 2026-10-04. Execution requires the root's
review and release. This changes the previously flat homogeneous premise;
it is not another execution of the flat stability bound.

## Question and retained physics

Use the SAME normalized constant-trace action and odd continuation of the
relaxed galaxy constitutive law in SHARED_GEOMETRY_CONSTANT_SHEAR_REPAIR_V001.md.
Retain physical metric clocks, minimally coupled conserved ordinary baryons
and radiation, and constant negative spatial curvature. Set

    nu0 = (a0/c) in km/s/Mpc, x0=(H0/nu0)^2, y0=eta*x0,
    G(y)=F(y)-2y F'(y), G_y=-F'(y)-2y F''(y),
    kappa=Omega_b0+Omega_r0+Omega_K0+G(y0)/(3x0),
    lambda_b=(2kappa+1)/3,
    E(y)=3kappa*y/eta-G(y).

The present constraint determines kappa; it is not fitted to the BAO vector.
The background equation is

    E(y(z))=3[100^2 wb(1+z)^3+100^2 wr(1+z)^4
                    +H0^2 Omega_K0(1+z)^2]/nu0^2.

Follow the increasing root from y0. The requested still-open candidate has
kappa>1 and E'>3/eta, equivalently lambda_eff>1. Positive kinetic sign is a
necessary local principal screen, NOT full gradient stability, nonlinear
completion, branch formation, or existence of the required EFT window.
The proof excluding acceleration for kappa<=1 is not extended to this grid.

## Inputs, exposure, and counted freedoms

Freeze the Cartesian product H0={60,70,73.6} km/s/Mpc,
Omega_K0={.5,.75,1,1.5}, eta={100,1000,10000}: exactly 36 cases.
These are exposed development choices, not a continuous fit or a probability
distribution. Fix wb=.02235 and wr=4.18e-5 in measured-G_N density units.
The baryon benchmark is conditional on the stated ordinary BBN assumptions;
radiation assumes its stated standard thermodynamic inventory. Neither is
re-estimated here.

Read a0=1.0059833281731022e-10 m/s^2 from the saved SPARC calibration, and
retain r=25.51664211557329 from the old shape result. That r was originally
calibrated using exposed cosmological information, not galaxy-only data.
No force scale, absolute offset, extra matter, curvature profile, or source
history is changed per case. H0, curvature and eta label the three-dimensional
sampled family; kappa is eliminated by its present constraint. The only
within-case fit is ONE common BAO amplitude. Any later selection from these
36 shapes must be disclosed as development selection, not a prediction.

DESI's complete exposed 13-vector and covariance are pinned, including the
last DH-then-DM pair. These are survey-inferred metric distances, not raw
photons. The earlier KiDS mass/lensing reductions assumed their own distance
cosmology and cannot be transferred unchanged to these strongly curved cases.
No KiDS score is computed here.

## Distances and score

With EH=H/H0=sqrt(y/y0), chi=integral_0^z dz/EH and Omega_K0>0,

    dM=sinh(sqrt(Omega_K0)*chi)/sqrt(Omega_K0),
    dH=1/EH, dV=(z*dM^2*dH)^(1/3).

The predictions DM/rd,DH/rd,DV/rd are A times their corresponding d values,
where A=c/(H0*rd)>0. Profile this ONE common A analytically using the full
13x13 covariance. Report its implied rd, not a predicted acoustic ruler.
No H0, eta, curvature or force parameter is fitted to these distances. Save
all cases in declared order, without ranking, score acceptance thresholds,
significance claims, or discarding poor scores.

## Numerical specification and custody

Import only the inert definitions of shared_geometry_prediction_v001.py;
use Law.sample(sqrt(y),r), not Law.sample(y,r). Compare force quadratures
64 and 128 and distance Gauss orders 64 and 128 independently. At each
force order first continue 257 equally spaced z nodes from 0 to 2.33 using
the preceding root as lower bracket. Bracket upper roots using |G|<=F(infinity)
and kappa>0. Distance-node roots stay between their neighboring continued
roots. Also check 257 uniformly spaced y nodes between the endpoint roots.
These are sampled branch checks, not a proof between nodes.

Require 0<F'<1 and E'>3/eta at the dense z, dense y, and actual distance
nodes. Require relative/scaled root and present-constraint residual <=1e-9;
solve to an internal 2e-13 target with at most 40 safeguarded Newton/bisection
iterations. Require monotone continued y, force F/F'/G_y and expansion
64/128 agreement <=1e-7, distance-shape agreement <=1e-7, and amplitude/score
agreement <=1e-6 (scaled by max(1,abs(value)) for score). Test covariance
symmetry/Cholesky, direct versus whitened scoring, synthetic amplitude,
flat-distance limit and analytic Milne distances. No threshold is adjusted
after results. A sign-disagreeing force refinement is unresolved, not passed.

Failed-domain, failed-control, exception, and budget-unreached cases are kept
with reasons; BAO scores are withheld for those cases. Invalid cases do not
constitute a software-control failure by themselves. A 55-second wall-clock
calculation budget is checked between bounded root iterations; remaining
cases are recorded unevaluated. Single process, one BLAS thread, no installs,
no ancestral producer execution, no pycache. This is not a global branch or
global numerical-roundoff certificate.

After reading both files, root runs `curved_shared_geometry_v001.py freeze`
to atomically save all source/protocol/input hashes before executing without
arguments. Freeze is custody-only, not a scientific run. Publication is atomic
and refuses overwrite. The result retains inputs, controls, all 36 case
records, 257-node histories where available, resource use, and hashes; stdout
is compact. All prior flat failures remain intact. No native UNT derivation,
all-stage completion, or superiority claim follows from this diagnostic.
