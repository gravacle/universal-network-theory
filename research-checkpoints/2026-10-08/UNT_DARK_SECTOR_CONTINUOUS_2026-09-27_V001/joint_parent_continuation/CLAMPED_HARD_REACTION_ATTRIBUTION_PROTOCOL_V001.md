# Hard-reaction attribution: prospective protocol V001

2026-09-29. Inert new worker only; root is the sole numerical producer.
No physical solve/import was performed during authoring. The original
clamped material, driver, protocol, freeze and all outcomes remain unchanged.

## Fixed intervention and complete census

Run only the declared lambda=0 counterfactual of
`CLAMPED_HARD_REACTION_COUNTERFACTUAL_V001.md`:

    div(D_normalized)=epsilon*deltaT_soft/Kb,
    T=E+3Pi.

Keep the SAME phase-solved material, hard action/frequency relation,
polarization, hard/soft energy and pressure, finite DeltaU, source, clamps,
gap, calibration and two fixed seeds. Only the hard contribution to the
lapse volume source is disabled. This violates the original common-action
source relation deliberately; it is an attribution control, not a viable
second action, no-energy interpretation, or an empirical model repair.

Four cases map to original physical indices [0,2,4,6], namely both gaps
[128,8192] and boxes [1,2] at N16. Each retains BOTH original seed multipliers
[1,2]. Saved physical lambda=1 fields are comparison data, never initial
guesses. Every failed seed and every numerical qualification is retained.
No lambda scan, continuation or fit is performed. A later grid/physical
interpretation would need its own finer comparison; this N16 attribution
does not certify spatial resolution or remove the known mixed clamp corner.

## Exact implementation and controls

Reuse the authenticated frozen `clamped_common_phase_patch_v001.py` geometry,
Newton/line-search algorithm, original controls and full outcome construction,
plus `clamped_phase_material_v001.py`. A sole-worker try/finally temporarily
dispatches the original algorithm to the explicitly named counterfactual
evaluator in memory, then restores the original function. No module source,
configuration, constant, tolerance or file is modified. There is no hidden
physical recomputation of a saved lambda=1 solution.

The counterfactual evaluator calls the unchanged physical evaluator for
flux, material and physical residual, then assembles its own residual from
the same flux minus only the soft source. This avoids cancellation between
large cold hard-reaction terms. Its Jacobian is likewise assembled from the
unchanged flux tensor, F_Phi coupling and ONLY the soft reaction derivative
2Fsoft; no large J diagonal is added and subtracted in the production solve.

For independent final-state checks, the original evaluator also constructs
its complete physical Jacobian. Exact identities are

    R_counter-R_physical=epsilon*deltaT_hard/Kb,
    J_counter=J_physical-epsilon^2*Jstatic*identity/Kb
              +epsilon*(2Fhard-F_Phi)*n.grad/Kb.

The global flux balance has the corresponding removed volume integral.
These controls use the inherited arithmetic tolerance2e-11. Residual and
flux identities are integrated with the same annular volumes and normalized
by max(sheet_flux,abs(counter_volume),abs(physical_volume)). The independent
Jacobian difference uses Frobenius norm divided by max(1,counter_J_norm).
No gate is imposed on the size/sign of the intentionally omitted source or
on the difference between the two solutions.

All other numerical controls are inherited unchanged: Newton40 iterations,
18 line halvings, integrated residual1e-9, global flux2e-8, GL128 primary
versus GL64 residual control2e-8, both fixed directional perturbations at
1e-5 and5e-6 with error2e-5, same-state identities2e-11 and the independent
Newtonian geometry test. All four directional comparisons must actually be
checked and pass to qualify a Jacobian; active-set switching remains visible.
Prerequisite failure leaves both seeds explicitly unstarted.

## What is saved and what a comparison means

Retain all original fields, phase states, absolute energies/pressures,
minimum/excitation split, DeltaU, residual histories, branch flags,
ellipticity, local lengths, sheet inversion and omitted-term diagnostics.
Rename the originally computed full hard volume source to
`recorded_but_removed_hard_volume_source`; its applied contribution is exactly
zero. Also save the original physical residual field, its norm, physical
volume source and physical flux balance evaluated on each retained
counterfactual state. Thus its defect as a solution of the original action
is explicit, not accidentally labeled a passing original field equation.

Compare each same-seed saved physical counterpart with the counterfactual
at identical centers: u, radial/vertical G and physical acceleration, I,
I/Ib, hard/soft/total reaction, hard energy and pressure. Record weighted RMS,
symmetric relative RMS, maximum absolute and signed differences. Differences
are counterfactual minus physical; no interpolation or pass threshold is
needed. A comparison is equilibrium-qualified only if both solves converge,
both Jacobians qualify and both cases' numerical controls pass. Otherwise
it is a descriptive comparison of retained iterates, not evidence for the
size of an equilibrium effect. Even a qualified pair is only this clamped
weak-lapse attribution experiment, not full metric/formation evidence.

## Custody and execution

The worker emits stdout only: `freeze` or `run-case 0..3`. The freeze verifies
the complete original prospective input lineage and binds the new worker,
this protocol, the analytical counterfactual note, and the exact four saved
physical result transports. Each saved transport authenticates its raw and
payload hashes, original freeze, labels, configuration and full seed census.
The root publishes the new snapshot before any run and captures/publishes
the complete compressed wrapper with apply_patch. No producer file writes,
bytecode, subprocess, installation, network or concurrent worker is used.

`COMPLETE_RETAINED_OUTCOMES` means all required outputs and controls are
present; inspect individual seed and pairing qualifications. Numerical
failures exit nonzero, while nonconvergence with passing executed controls
remains an explicitly retained scientific/numerical outcome. The original
failed branches are neither overwritten nor retrospectively reclassified.
