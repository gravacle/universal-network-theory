# Finite-slice V002: reuse identical dust controls, not alter the experiment

2026-09-29. Additive technical wrapper. V001's source, freeze, benchmark,
physical census, integrator and every numerical threshold remain unchanged.
No producer is run by the author. Root owns all execution/publication.

## Exact physical quotient behind the reuse

In the pressureless comparator, w_H=cI2_H=0. Its two material species obey

    (delta_H-delta_b)'=-(theta_H-theta_b),
    (theta_H-theta_b)'=-Hc(theta_H-theta_b).

The declared initial data have zero differences, so both remain zero. The
metric and background then contain E_H+E_b, depending on Omega_m rather
than its arbitrary partition into the two pressureless labels. Initial
common d,v and the radiation distribution likewise depend only on total
matter. Radiation, shear, time units, the preferred clock and both metric
columns are unchanged by this quotient. The absolute hard/baryon density
perturbations still use their own component densities; their abundances are
NOT exchanged or fitted. The finite-pressure candidate never uses this
quotient unless its inherited Delta=0 state is exactly the dust limit.

The cache identity is the V001 source/configuration, Hcal, Omega_m,
Omega_Lambda, Omega_gamma/ordinary-radiation convention, initial basis,
initial epoch, output epochs and k/angle/time controls. Retain the origin
and target Omega_b/Omega_exc and verify their sums. Floating-point split
arithmetic need not be bit-identical: check full initial vectors against the
old arithmetic tolerance and reweight the saved constraint/moment outputs
with the new component split. Do not call those arithmetic checks a new
time-integration qualification.

## Five existing-census anchors; one new freeze

The first finite state in each original background/record order is fixed:
case8,75,142,209,276 (point8 in backgrounds0..4). Case8 is the already passed
V001 benchmark and MUST NOT be rerun. Root runs the other four using V001's
existing run-case mode and unchanged frozen source. These are four required
census histories, not extra calibration/preparation or a second cache
producer. Each contains its own complete candidate, dust and EdS controls.

Fixed receipt paths:

    FINITE_SLICE_GROWTH_TRANSFER_V001_BENCHMARK.json
    FINITE_SLICE_GROWTH_TRANSFER_V001_CASE_075.json
    FINITE_SLICE_GROWTH_TRANSFER_V001_CASE_142.json
    FINITE_SLICE_GROWTH_TRANSFER_V001_CASE_209.json
    FINITE_SLICE_GROWTH_TRANSFER_V001_CASE_276.json

Before V002's freeze, authenticate their raw/payload/freeze hashes, exact
case/background/source-record/configuration identities, four k values,
three resolutions, all output epochs and passing controls. The freeze then
includes all five receipts, their unchanged V001 ancestry and the V002
source/protocol. There is no mutable cache, outside folder, network call,
installation, result overwrite or implicit dependency on a future file.

## Execution and retained evidence

V002 imports V001 only after its fixed source hash authenticates. It does
not monkeypatch a function, call V001 main/run_case, or change its CONFIG.
Modes are freeze and run-case0..334; each output has an explicit single-case
status. All335 still define the full census.

- For the five anchors, reference their original candidate/dust arrays and
  comparisons. This promotes no benchmark into whole-census completion;
  it merely counts its already completed single history once.
- The40 inherited Delta=0 histories use the exact dust identity and refer
  to their background's qualified dust result. No new ODE is claimed.
- Every other finite-gap history runs the unchanged V001 Model/propagate
  and compare_runs candidate branches for all four k, both initial columns
  and three numerical resolutions:12 new ODE propagations per history.
  Its dust arrays and universal EdS control are immutable references.

JSON references include the exact root-relative file, raw SHA, freeze SHA,
payload SHA and JSON pointer. They are not synthetic copied observations.
For a newly propagated history retain its complete candidate initial vectors,
samples/refinements and signed candidate-minus-dust arrays as before.
For a pure reuse retain references, not duplicate the original arrays.
Keep original per-history state/abundance and all1,340-label provenance.

Every rebinding checks the dust species equality, original initial vectors,
unchanged H(a), reconstructed comoving contrasts and shear, and the newly
reweighted Hamiltonian constraint. Compare the new-minus-old raw constraint
at the original2e-11 arithmetic tolerance; the actual normalized constraint
still must satisfy the original2e-7 control. No threshold is relaxed.

The universal EdS evidence is referenced from the original benchmark; it is
not rerun or counted afresh for every case. New check counts are separate
from referenced evidence. Runtime/self RSS and number of actually new ODE
runs are reported; the anchor runtimes are not relabeled as current work.
Any fatal invocation is retained unfinished, as in V001. This wrapper does
not add a full-state intermediate restart capability.

This preserves the scientific comparison exactly while avoiding repeated
control propagation. It does not change the finite-slice preparation into
a primordial mode, establish a CMB spectrum, or turn growth transfer into
observational success.
