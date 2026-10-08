# Prospective consistent inertia two current experiment

This freezes a minimal numerical experiment for the already specified spherical ordinary and hard currents. Its only mechanical change from the old finite-R solver is the reviewed exact consistent inertia and its required canonical geometric term. It does not choose a new physical source, formation rule, bath, metric or parameter fit. The source was written inertly; root alone may execute it after full source and independent preflight review.

## Scope and fixed cases

Use the sole root `/Users/bgm/Documents/ChatGPT/Universal Network Theory`, with all new files in `UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation`.

The two cases, in fixed serial order, are `(R,L,dx,N)=(128,8,1/16,128)` and `(8192,8,1/16,128)`. Preserve the ancestral physical inputs and units from the pinned dust-shadow and release-certificate receipts, `A=1`, zero physical initial momenta, fixed cell masses, source normalization, compact seed, background, material EOS and readout times `[0,1/64,1/32,1/16]`. No `L=16` or spatial refinement case is implied in this packet. Failure of case zero does not scientifically waive the independent case-one diagnostic.

The source-authored configuration, all physical ancestry files from the pinned old two-current freeze, kernel, maps, design, prerequisite result and new producer/protocol/supervisor bytes enter a new runtime freeze. The old freeze has SHA256 `0c698bc6c9867d7afdb32f2dc51f9b776a14f6512a5e302ec8b28aa0c9057c82`. Its old case census is historical, not this experiment's census. The exact kernel prerequisite result has SHA256 `738dd1f841cfa1648f178c4dcbc556f5333b0e560ab3daae82908cd3f715250b`; its successful finite arithmetic controls do not qualify the new evolution.

The producer imports authenticated old definitions under a non-main module name. It reuses only `EOS`, `gravity`, `seed_mass`, `Checks`, `Stop`, the initial-state layout, material/source controls and the physical-force/work `Model.rhs` method. The new initializer never calls the lumped-mass initializer. The new `read` supplies consistent velocities and kinetic energies to the old force/work formulas; the new `rhs` then adds the exact geometric canonical kick. No old `main`, `inputs`, `run_case`, integrator or snapshot is invoked. The state-map and kernel hashes are pinned literally in the producer; a method-name guard is not treated as source authentication.

## Mechanics and output meaning

For each species use `p=A M(x)v`, `xdot=v/A`, `K=vᵀMv/2`, `pdot=g+f` and `g_j=vᵀM_,j v/2`. Preserve `f_gravity=-gradW0/A`, the hard pressure kick including outer traction, and the same finite-R action, gravity energy and EOS quadrature. The ten physical work ledgers are unchanged. The kinetic chain is `Kdot=xdot·pdot−g·xdot−2HK=xdot·f−2HK`: geometry is not an extra physical work input.

Snapshots save canonical momenta, the exact tridiagonal inertia, geometric kicks, coupled force responses and

`vdot=M^-1(f+g)/A−M^-1(Mdot v)−H v`, with `Mdot=M'[xdot]`.

This is the derivative of peculiar velocity in the old dimensionless units. It is **not** the total acceleration of the physical radius `A x`. Isolated gravity and pressure responses are also not complete accelerations. Save signed full profiles, including the origin face and seed edge; do not crop an unfavorable region or call geometric acceleration new modified gravity.

## Integrators and unchanged criteria

Set `h0=min(1/1024,0.15 dx/speed_cap)` using the old formal material/velocity expression. Its only adopted role is a **legacy work ceiling**, not a certified consistent-inertia CFL bound. Run RK4 at `h0`, `h0/2`, `h0/4`, and independent DOPRI 5(4), with the same ceiling. The quarter-step is the designated comparison reference; all coarse and half-step outputs remain mandatory, even if they fail. Integrators start from the identical physical initial state.

DOPRI compares the complete charts `Φ=[A,xb,vb(xb,pb,A),xh,vh(xh,ph,A),scaled ledgers]` of its actual high- and low-order endpoints. Only the final three hard-specific ledgers are divided by total hard mass. Keep `rtol=2e-11`, `atol=2e-13` and the denominator specified by `SPHERICAL_CONSISTENT_SOLVER_INTEGRATION_DESIGN_V001.md`. Guard both embedded endpoints before an accuracy accept/reject; an invalid endpoint is a retained domain failure, not a hidden smaller-step retry.

Preserve all old scalar criteria: arithmetic `2e-11`, EOS/material `2e-10`, complete physical-chart state `2e-8`, velocity/volume/action and work budgets `2e-7`, directional derivatives `2e-6`. Pointwise maximum norms and hard per-rest-mass checks remain; no new weighted average may hide a small hard current or central discrepancy. The old `Checks` normalization is retained: absent an explicit physical scale, compare `|a-b|/max(1,|a|,|b|)`. New per-species actual-mesh derivative/work controls divide both sides by the same fixed total species mass before this rule. Matrix-entry controls likewise divide by fixed species mass; they do not claim a componentwise relative error certificate for tiny entries.

## Required controls and retained data

Run the unchanged actual-mesh homogeneous gravity/pressure, compact seed, rest-action normalization, signed gravity energy derivatives jointly and per species, nonuniform pressure/internal-energy derivative, and saved material controls. Then test the new mechanics on the actual 128-cell initial meshes using **test-only** `v_b=.17 x/(1+x)`, `v_h=−.11 x/(1+x)` and `p=A Mv`. These vectors are never the physical trajectory initial state.

Use the existing derivative steps `[1e-4,5e-5]`, with the same old sine direction `.1 sin(πx/L)`. Retain and check both centered estimates and their fixed Richardson combination for fixed-p kinetic derivatives and `M'[direction]`; do not select a preferred step. Check `vᵀMdot v/2=xdot·g` with the independent derivative assembly and complete kinetic work cancellation with the actual physical kicks. The original pressure-gradient control still uses its explicitly nonuniform synthetic mesh; the new kinematic test does not replace it. No tiny-matrix oracle or quadrature study is rerun.

Prerequisite failure stops that case before trajectory. Its check counts, failed groups and already assembled controls remain saved. Separate prerequisite diagnostic maxima from the actual pressure-on method maxima. Velocity/material-energy/volume extrema pool the four methods' sampled RHS stages; the EOS root-error maximum additionally includes other material reads, including snapshots. These are sampled quantities, not interval bounds.

For completed pressure-on methods, save raw canonical states at every readout and compare all other methods to quarter-step RK4 in the nonlinear chart. Preserve separate velocity, volume, action, EOS order-128, enthalpy, recovered action, sound bound, total/mechanical/ordinary/hard-specific energy budgets and fixed-mass checks. Snapshot solve residuals use `max(||p/A||∞,||diag(M)v||∞,tiny_binary64)` as normalization and the unchanged arithmetic criterion; this is a numerical residual diagnostic, not a condition-number or backward-error theorem.

Finally run pressure-off RK4 at `h0/4`, removing **only** the pressure kick. Keep the same background, EOS and consistent inertia including `g`. Save raw pressure-off states and signed pressure-on/off face, velocity and density differences, together with the inherited shadow comparison at the same labels. Its work budget is not used to qualify the physical fluid. If a preceding numerical comparison failed but the state/domain remains evaluable and resources permit, this control still runs and its outcome is retained.

Each active method has a partial journal of completed readouts, most recent accepted state, attempts and counters. On caught failure, retain the failed stage/endpoint state when available, including nonfinite-safe little-endian binary64 bytes, traceback and reason. A cooperative resource failure retains the active method's last RHS state. Abrupt process termination may prevent a scientific JSON result; the supervisor preserves the raw capture and invocation receipt instead and marks the case incomplete. No failed method is silently replaced or resumed under the same identity.

## Resources and publication

The producer is NumPy-only with all five thread controls set to one before import. Per process: CPU soft/hard limits `150/155` seconds, cooperative/alarm wall limit `165` seconds, self-RSS guard `512 MiB`, each input file at most `64 MiB`, and output JSON at most `16 MiB`. Resource fields labeled `resources_analysis_phase` are sampled before final JSON serialization. The source sets these bounds only when root actually invokes it.

The serial supervisor uses the pinned no-overwrite publication definitions and pinned resource-invocation definitions, never their old entry points. It gives each child a fresh private process group, with a `180`-second wall limit, group-RSS samples every `.2` seconds against `512 MiB`, and a `3`-second termination grace. RSS is sampled, not a hard allocation cap. Capture sizes are validated after invocation (`16 MiB+1` stdout and `1 MiB` stderr); these are not instantaneous pipe monitors. The trusted producer separately limits normal scientific JSON output. Supervisor receipts are capped at `32 MiB`, and the serial launch window at `390` seconds; no third case exists.

Root invokes only the new supervisor with `freeze`, then `run-all`, from the sole root using its existing Python runtime. Freeze is custody-only. Execution emits one exclusive serial intent and one exclusive intent per case before starting the child. Existing intents or outputs refuse automatic retry. Each invocation's raw stdout/stderr, their hashes, return code, resource sampling, stop reason and validation result are retained. Valid scientific failures are published too. A failed case does not allow overlapping execution; the second child starts only after the first group has finished or been terminated. New freezes, intents and results use fsync plus atomic no-overwrite publication. No historical source or receipt is edited.

The supervisor accepts return code `2` only as a potentially valid retained failed case, never as success. A numerical success requires completed producer status, no failed groups, successful invocation/resource custody and unchanged inputs at the end. The new two-case serial summary does not itself perform an independent saved-state arithmetic audit; that review remains a separate step after root execution.

## Interpretation and exact next action

Consistent inertia has a generally dense inverse. The old formal sound/travel expression remains a conditional continuum diagnostic; no strict finite-grid causal domain, CFL theorem or interstage no-crossing proof is inherited. All trajectory qualification, spatial continuum, certified CFL, certified no-crossing, full metric, physical source/formation, observational and Stage 3 completion flags remain false, even if all finite controls pass. All 11 mandatory program lanes remain OPEN.

Root and an independent reviewer must inspect the actual producer, state maps, protocol and supervisor before any invocation. If the two cases resolve the prospective numerical checks, inspect their full origin/edge and pressure-on/off readouts before extending to the already defined refinement/interface grid. If they fail, preserve the exact failure and diagnose it. The purpose is to advance the specified shared-state dynamics, not to manufacture a favorable halo, change the accepted tolerances, or promote stable numerical evolution into a physical explanation of dark matter and dark energy.
