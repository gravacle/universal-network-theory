# Prospective inherited-reference pressure-bound arithmetic

2026-09-29. No new data, observation fit, optimizer, mode population, force
calculation or physical-time evolution. This is a stdlib-only diagnostic of
the previously exposed and cosmologically calibrated RELAXED reference.

## Fixed inputs and scope

Keep all nine reference combinations and both standard-BBN alternatives in
`COSMOLOGY_CLOSURE_ARITHMETIC.json`, without selection or recombination. Its
plain JSON is identified by SHA-256
`258097f5a80c8cfb4891d93e02a1f6224eb54b73014c276683f05c8b3989f153`.
Authenticate its producer hash and every recorded source hash. Recursively
authenticate the original shape-reference freezes and check the original
shape-result payload/hash and its numerical checks. The new freeze includes
these ancestors, this protocol, the new script, and the completed analytical
shared-mode note and its independent review. Import no scientific code.

Use epsilon=.001, c=299792458 m/s, and the old producer's conversion
1 Mpc=3.085677581491367e19 km. Convert H0 in km/s/Mpc by dividing by that
Mpc-in-km value. For each row retain the original input/baryon metadata and
calculate

    Omega_required=1-Omega_Lambda_ref-10000*omega_b/H0_kmsMpc²,
    gstar_SI=a0_SI/(8/(3pi)),
    S4=(1-epsilon^6)/6,
    factor=(3/4)(1-epsilon²)*(c*H0_SI/gstar_SI)²,
    E_required=factor*Omega_required,
    P_floor=E_required²/[sqrt(S4+3E_required)+sqrt(S4)]²,
    w_floor=P_floor/E_required.

Evaluate the last two only for positive E_required. Keep a nonpositive case
with its signed required density and explicit non-applicability, not a clipped
positive target. There is no scientific pass/fail requirement on its sign or
on the resulting pressure. Cross-check the required coefficient, Omega and
omega against every saved old row and its original shape-reference input.

The three fixed illustrative limits wmax=.001,.01,.1 are definitions for
reporting capacity, NOT independently observed limits:

    E_capacity=4*S4*wmax/(1-3*wmax)²,
    Omega_capacity=E_capacity/factor,
    required_to_capacity=E_required/E_capacity
                        =Omega_required/Omega_capacity.

Retain every capacity for every row. When the required energy is nonpositive,
the positive-required-capacity ratio is null. The signed density remains.

## Numerical controls before the reference table

Use deterministic normalized tolerance 2e-12. Equality checks divide absolute
error by max(abs(left),abs(right)), using one only when both vanish. Inequality
checks use the same scale for the positive violation. Preserve every failure.

Before evaluating reference rows, check:

- the stable pressure-floor formula solves E=2sqrt(S4*P)+3P for E in
  {0,1e-12,1e-6,.01,1,10,1000}, and 0<=P<=E/3;
- inverse-capacity round trips for w in {1e-6,.001,.01,.1,.3};
- Jensen/Cauchy on two declared positive three-mode moment fixtures: one
  saturating both inequalities, one strictly nonuniform, and their resulting
  pressure-floor inequalities;
- the inherited Hubble-unit conversion evaluated by both km and metre routes.

The fixtures test arithmetic/identities, not real periodic trajectories or
physical attainability of equality. The mathematical pressure bound was proved
separately for rapidly averaged zero-source positive quartic modes. The
reference table also checks the exact analytic inverse at every capacity and
the two ways to compute its dimensionless ratio. No qualitative scientific
outcome is part of the numerical qualification.

## Output and interpretation

`pressure_bound_reference_v001.py freeze` emits only a JSON input snapshot to
stdout. The root agent publishes it without overwrite as
`PRESSURE_BOUND_REFERENCE_V001_FROZEN.json`. Running with no arguments requires
that exact parsed snapshot and emits a result wrapper, all 18 rows, all 54
capacity entries, synthetic controls, check failures and payload hash to stdout.
It writes no files and does not launch another worker. Root publishes the
result after source review; this author has not run it.

The prior acceleration scale describes the relaxed curve. A NEW excited-state
joint inference can change gstar and must recompute its actual galaxy response.
Consequently this diagnostic does not exclude all four-parameter shared-state
candidates, prove an observational coldness threshold, or reject UNT. Positive
excitation is real stress in this completion, not absent energy. Nonadiabatic
coherent states lie outside the rapid-virial bound and need their own evolved
stress, not an assigned dust equation of state. No frozen earlier result changes.
