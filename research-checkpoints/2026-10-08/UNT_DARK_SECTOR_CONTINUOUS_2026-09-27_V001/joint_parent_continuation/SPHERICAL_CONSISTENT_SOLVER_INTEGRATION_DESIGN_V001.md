# Consistent inertia integration for the spherical two current solver

This is a prospective implementation and verification design, not a trajectory result. It replaces the old solver's lumped face masses with the separately tested exact finite-shell inertia while preserving its action, material law, physical forces, fixed shell masses, cosmological background and physical initial data. The companion `spherical_consistent_state_maps_v001.py` supplies inert kinematic maps only. It contains no trajectory driver or new step selector and has not been imported, compiled or numerically executed by its author.

The shortest useful next step is a separately frozen, bounded exploratory evolution of the existing initial state with these canonical equations and explicit time refinement. A global nonlinear stability theorem is not a prerequisite for that experiment. The experiment must not inherit the old local CFL or exterior domain-of-dependence interpretation, and an operationally successful finite run would not establish the physical formation of the shared galaxy and cosmic state.

## Inspected sources and unchanged evidence

Paths below are relative to `UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation` under the sole project root `/Users/bgm/Documents/ChatGPT/Universal Network Theory`.

| Source | SHA256 |
| --- | --- |
| `spherical_two_current_v001.py` | `0349740de7d0b4173f634eaf8fd52c7e5eb4ea9ea196f95a5b882024f6dd95df` |
| `SPHERICAL_TWO_CURRENT_PROTOCOL_V001.md` | `c124a0e0a361a33860ec4e0470b0380758405740bdb8b7d9f45783b0bf9a5ba2` |
| `SPHERICAL_TWO_CURRENT_FINITE_R_DESIGN_V001.md` | `4733e51a4bf5646861ec3123ab5799b3b3e5662faf8a449b8eb54f7cd4f661c1` |
| `SPHERICAL_TWO_CURRENT_RESULT_AUDIT_V001.md` | `33eb42c0f30a644b69580e43a17abc77ef5f3394786a2bc70e5055b2764367f5` |
| `SPHERICAL_CONSISTENT_KINETIC_REPAIR_V001.md` | `24309d3602ee4724a975ad61ffaca1903cdb3a73d6a5149b8a10b7e73e711353` |
| `SPHERICAL_EXACT_INERTIA_DERIVATION_V001.md` | `3a60f43ea5e666e23bac8e478df74f38aeaac77f0cc4a86c15cae593a622a431` |
| `spherical_exact_kinetic_v001.py` | `78765ef0e2d29c044642b1d944682a81ff5d48b22de9d0cb16b7bc47b9c7e11a` |

The original two-current results, failed low-order quadrature oracle and separately versioned exact-inertia oracle remain separate evidence. Nothing here changes their thresholds, output bytes or scientific status. The exact-inertia kernel is used as a dependency, not silently substituted into an old frozen producer. Its successful small-matrix controls do not themselves qualify a full two-current evolution.

## Canonical equations and units

Use the original dimensionless radius, time, mass, velocity and energy units. For each species with fixed cell masses and constrained origin, let `M(x)` denote the exact free-face mass matrix. It depends on comoving face geometry only, not explicitly on the scale factor or time. Define

\[
v=A\dot x,\qquad p=A M(x)v=A^2M(x)\dot x,
\qquad K={p^TM^{-1}p\over2A^2}={v^TMv\over2}.
\]

At fixed canonical momentum,

\[
g_j={1\over2}v^TM_{,j}v,\quad K_{,x_j}|_p=-g_j,
\quad\dot x={M^{-1}p\over A^2},
\quad\dot p=g+f.
\]

Preserve the old physical kicks exactly: both species have `f_gravity=-gradW0/A`; the hard species additionally has `f_pressure=4π x_face²(P_left-P_right)`, with the outer `P_right=Pbar`. A kick is a canonical force, not an acceleration. Do not divide `g` by a face mass, omit it because the initial velocities vanish, or add a separate Hubble drag to `pdot`.

Differentiation of `p=A M v` gives the complete peculiar acceleration

\[
\dot v={M^{-1}f\over A}+{M^{-1}g\over A}
          -M^{-1}\dot M v-Hv,
\qquad \dot M=M'[\dot x].
\]

For clarity, the coordinate acceleration is
`xddot=M^-1(f+g)/A²-M^-1 Mdot xdot-2H xdot`.
The isolated gravity and pressure responses are respectively `-M^-1 gradW0/A²` and `M^-1 f_pressure/A`; neither is the total trajectory acceleration. If a future model adds explicit `A` or time dependence to `M`, these formulas require the corresponding extra derivatives and energy work. No such change is adopted here.

For each non-origin shell, with `q=L/R` and `M_shell=mF(q)`, the exact directional derivative needed for acceleration output is

\[
\delta M_{\rm shell}=mF'(q){\delta L-q\delta R\over R}.
\]

The origin contribution is the constant free entry `3m/5`, so its directional derivative is zero. The companion implements this formula using the reviewed rational-polynomial `F'`, not a finite-difference approximation.

## Every lumped mass dependency to replace

Line anchors refer to the pinned old producer above.

| Old location | Required new behavior |
| --- | --- |
| `Model.__init__`, lines 153–176, `face_masses` | Remove the lumped array from dynamics. Preserve cell masses, material calibration, meshes and physical initial `p=0`. Build each `M` from its own current mesh. |
| Initial `error_units`, lines 169–173 | Remove fixed momentum scaling by inverse face masses. Retain only the declared hard-ledger normalization in the nonlinear chart below. |
| `Model.read`, lines 177–203 | Solve `M v=p/A`; use `K_s=v_s^T M_s v_s/2`. Preserve material, gravity and action/volume guards. Cache each species' diagonal, off-diagonal, velocity and geometric force for the same state. |
| `Model.rhs`, lines 204–229 | Use `xdot=v/A`, `pdot=g+f`. Apply the exact same gravity, pressure and outer traction as before. Geometry is not a new physical force law. |
| DOPRI error, lines 244–265 | Compare the full nonlinear charts of the actual fifth- and fourth-order solutions. Do not apply a fixed linear scale to the embedded momentum error. |
| Snapshots, lines 268–285 | Replace both local acceleration divisions with coupled solves. Save physical force responses separately from geometric, inertia-motion, Hubble and complete peculiar acceleration. |
| Controls, lines 288–340 | Retain existing source/material/force controls and add a small actual-mesh nonzero-momentum chain-rule test. Zero-velocity initial tests alone cannot exercise the new term. |
| `run_case`, lines 343–408 | Compare time-integrator states in the new chart, use consistent `K` in unchanged work ledgers, preserve raw canonical vectors, and relabel travel/margin as conditional continuum diagnostics. |
| Pressure-off control, lines 387–398 | Remove only the pressure kick. Keep exact `M`, `g`, background and all kinematics. It remains an artificial numerical control, not an energy-qualified fluid or the original shadow discretization. |

Mass conservation still follows from fixed cell masses. The old density, action and volume formulas and their finite-R material omissions are not changed. Existing gravity accumulation precision and EOS quadrature order are retained. A future separately reviewed use of cancellation-safe volumes must be reported as its own arithmetic change; it is not necessary to bundle it into this inertia adaptation.

## Energy and work remain the same physical accounting

For each species,

\[
\dot K=\dot x^T\dot p-g^T\dot x-2HK
       =\dot x^Tf-2HK.
\]

Thus the geometric kick does not add a new work reservoir. Its canonical work cancels the geometry derivative of kinetic energy. The ten old ledger meanings remain unchanged: mechanical gravity; outer traction; expansion of `K+U`; expansion of `W`; total predicted energy change; formal characteristic travel; pressure-kick work; hard gravity; hard expansion of `K+U`; and complete hard mechanical work. Use the new `K_s` and new `xdot` throughout. Keep `W=W0/A`, the hard internal energy and their old forces unchanged.

The old total, mechanical, hard-per-rest-mass and ordinary mechanical budget equations therefore remain the appropriate tests. Keep arithmetic `2e-11`, material `2e-10`, state `2e-8`, readout/work `2e-7`, derivative `2e-6`, DOPRI `rtol=2e-11`, `atol=2e-13` exactly. These are finite numerical criteria, not observational tolerances. A failed budget remains failed; do not erase it by recording `g` as extra physical work.

## Error measurement and inert component boundary

The state remains `[A, xb, pb, xh, ph, ten ledgers]`. Replace its fixed linear error scale with

\[
\Phi(y)=[A,x_b,v_b(x_b,p_b,A),x_h,v_h(x_h,p_h,A),\widetilde L].
\]

Here only the last three hard-specific ledgers are divided by total hard mass, just as in the old producer. Positions and velocities are in the original dimensionless physical units. Preserve pointwise maximum norms, so a small hard mass or an origin cell cannot hide a velocity error in a weighted average.

For the actual embedded states `y5` and `y4`, use

\[
e=\max_i{|\Phi_i(y5)-\Phi_i(y4)|\over
  2\times10^{-13}+2\times10^{-11}
          \max(|\Phi_i(y)|,|\Phi_i(y5)|)}.
\]

Each chart evaluation uses that state's own two meshes and scale factor. In particular, a changed position changes the velocity conversion even at fixed momentum. Inter-method state comparisons use `Φ` with the old `2e-8` criterion; preserve the separate old `2e-7` velocity, volume and action comparisons. Raw momenta remain in saved method vectors and are not misrepresented as physical velocities.

The companion exposes `canonical_species_rhs`, `mass_matrix_directional_derivative`, `peculiar_acceleration_decomposition`, `physical_error_chart` and `embedded_error_norm`. It accepts an explicitly supplied kernel module; its method-name check is only an API guard. The eventual producer must verify the pinned kernel file before import and bind both source hashes in a new freeze. The companion has no file or publication interface, source loader, integrator or numerical certification claim.

Invalid kinematic charts fail closed. The eventual driver must retain the attempted embedded state and all guard failures, not hide an invalid lower-order state as an ordinary accuracy rejection. Existing DOPRI accuracy rejection remains legitimate when every attempted state is inside the prospective domain; changing that policy requires a separately reported protocol, not an implicit exception workaround.

## Nonlocal inertia and what the old CFL rule does not establish

`M` is tridiagonal but `M^-1` is generally dense. At the semidiscrete ODE level an outer force can immediately induce an interior acceleration through the coupled solve. This is a numerical property of the chosen finite-element coordinates, not evidence of physical superluminal propagation. The old `0.15 dx/speed_cap` is not thereby a proved stability limit, and a physical acoustic travel estimate does not prove a strict finite-grid domain of dependence.

The unchanged shell interpolation has nonnegative velocity shape functions `J_L,J_R`, with
`J_L+J_R=((1-s)L²+sR²)/((1-s)L³+sR³)^(2/3) ≤ 1`.
Thus the old face-velocity guard bounds the interpolated shell speed. It does not localize `M^-1`. Likewise, exterior spherical potential cancellation at the physical force-gradient level does not make the entire inverse-inertia evolution independent of outer numerical forces.

Continue recording the old formal material sound bound and integrated travel quantity, labeled as conditional continuum diagnostics under the sampled action/velocity guards. Preserve matching-width `L=8` and `L=16` comparisons before any exterior-insensitivity claim. The old source audit's origin and resolution problem is a primary readout, not a region to mask after seeing the new trajectory.

For a useful optional numerical conditioning diagnostic, let `S` alternate signs and `B=S M S`. Positive-off-diagonal SPD `M` gives a Stieltjes tridiagonal `B`, so `|M^-1|=B^-1`. Consequently one tridiagonal solve `Bz=1` gives the exact-matrix identity `||M^-1||∞=max z`. If a positive computed vector has rigorously bounded residual `η=||1-B zhat||∞<1`, then `||M^-1||∞≤max(zhat)/(1-η)`. An ordinary floating-point residual and positive computed LDL pivots are numerical diagnostics, not that rigorous certificate. No new inverse-norm implementation is required before the first exploratory run.

Even a rigorous inertia bound alone would not prove nonlinear time stability: the full RHS also contains geometry derivatives, pressure and gravity derivatives and evolving cell widths. Do not use a frozen initial oscillation estimate as a whole-trajectory theorem. Stage and endpoint crossing guards likewise do not rule out every interstage crossing. A separate rigorous no-crossing claim would need interval/dense-output bounds; it is not conferred by this design or required for an explicitly exploratory sampled trajectory.

## Minimal prospective experiment and decisive readouts

After root and independent source review, implement a new inert producer with the mapping above. Use a new freeze, one exclusive intent per run, atomic no-overwrite result publication, source/input digests and retained failure states. Do not modify or resume old case outputs under a changed Hamiltonian. The run protocol must cap CPU, wall time, memory and output before execution, retain partial progress on limits, and use one local numerical worker. No enlarged grid or physical parameter scan is implied.

The proposed first experiment uses the existing coarsest `L=8`, `dx=1/16` state for `R=128`, followed serially by the existing `R=8192` state. Preserve the old initial `A=1`, both zero momenta, source, material parameters and readout times `0,1/64,1/32,1/16`. This is a prospective numerical selection, not selection on favorable outcomes. A failure in one state is retained and does not waive the other state's independent diagnostic value if resources permit.

Use the old `h0=min(1/1024,0.15 dx/speed_cap)` only as a **legacy work ceiling**, explicitly without certified CFL status. Compare fixed-step RK4 at `h0`, `h0/2`, `h0/4`, and the independent DOPRI pair using the new error chart and ceiling. Predeclare all three RK4 resolutions and retain them all; the extra quarter-step is a new prospective refinement, not a result-tuned tolerance change. Accuracy disagreement, monitored crossing, nonpositive volumes, unresolved solves, action/velocity guards or resource exhaustion are retained outcomes. Do not silently replace a failing run with a more favorable step or method.

Only the following additional controls are needed before or alongside that first evolution; the completed tiny-matrix oracle need not be rerun:

1. At the actual initial mesh and fixed masses, exercise nonzero test momenta generated by `v_b=0.17 x/(1+x)`, `v_h=-0.11 x/(1+x)` and `p_s=A M_s v_s`. These are **test-only vectors**, not new physical initial data. Compare the full fixed-p kinetic directional derivative, actual pressure/gravity energy gradient and complete instantaneous work cancellation. Use the already frozen derivative ladder and criteria; preserve every step. Check the companion `M'[direction]` against that same analytical/finite-difference chain. Include the constrained origin.
2. For attempted trajectory stages, keep the existing action, volume, velocity and finite-state guards, and fail on nonpositive/nonfinite LDL pivots. Save solve residual diagnostics at the already requested snapshots; do not turn an unproved condition estimate into an acceptance guarantee. Save canonical `p`, geometric kicks and the complete acceleration decomposition at those snapshots so an apparent force change cannot be caused by a mislabeled local division.
3. Compare the refined physical charts, material readouts and unchanged work budgets using the preserved criteria. Record origin and seed-edge discrepancies pointwise, not only a global average. Quantify the signed hard and ordinary density/velocity changes and pressure-on/off differences; they are the first discriminators of whether this kinematic repair changes the previous finite-grid formation diagnostic.

If these bounded cases are numerically unresolved, retain that finding and diagnose the actual failure before a wider run. If they are resolved, the next useful extension is the original refinement/interface grid, not additional repetitions of already passed kernel algebra. Compare the same initial Lagrangian labels, hard action, both densities and velocities, and radius-dependent enclosed source mass across widths and `L=8,16`. A single unit outer-face kick response `M^-1 e_outer/A`, saved as an optional snapshot diagnostic without evolving a new physical state, can expose the size of the semidiscrete inverse tail; it cannot prove a causal cutoff.

The decisive target is improved, controlled same-state evolution of the specified matter and hard current, including whether the previous origin/edge discrepancy persists. Stable integration alone is not a galaxy fit, a native formation rule, shared cosmic-source derivation, lensing prediction or elimination of dark matter and dark energy. All physical, continuum, observational, state-formation, certified-CFL and certified-no-crossing flags remain false. All 11 program lanes remain OPEN.

## Review and next action

This document and its inert companion are source-only work. The algebra for canonical acceleration and geometric work cancellation was also checked analytically by `critical_path_native`; that is not a numerical reproduction or a review of a completed trajectory. Root must read the actual companion and this design before assigning a new versioned full producer. The next implementation should be the smallest bounded exploratory driver that applies these replacements, preserves custody and reports the shared-state readouts above, not an unbounded campaign to certify all nonlinear stability first.
