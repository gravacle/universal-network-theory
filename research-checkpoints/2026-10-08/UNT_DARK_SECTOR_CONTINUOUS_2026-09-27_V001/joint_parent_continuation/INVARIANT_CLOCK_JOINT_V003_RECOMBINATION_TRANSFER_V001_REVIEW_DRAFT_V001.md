# Joint V003 common-calibration recombination transfer V001

2026-10-06 UTC. Prospective NEW calculation at the already completed two-parameter development calibration. This protocol was designed after inspection of the saved V003 background/BBN/acoustic results and the older transfer results. It changes no fitted parameter or numerical gate. Root alone launches the reviewed worker.

## Frozen physical state and question

Use the SAME invariant-clock K(X) action and pressureless ablation at the final joint V003 tuple: Hunit=67.49711988577813 km/s/Mpc, physical GN-normalized omega_b=0.02166002225093379, OB=0.04659233656879551, Neff=3.0439772985579183 and YHe=0.24356210948040835. The full remaining parameter dictionary is the sealed V003 `fixed` dictionary. Hunit is a unit calibration; Htoday remains the result of the same background, rather than being set equal to it.

The existing joint calibration fitted TWO exposed ordinary observables, D/H=2.527e-5 and 100 theta=1.0411. Its BAO score was subsequently computed without a BAO-ruler fit. This packet fits nothing and does not retroactively turn calibration data into holdout observations. It asks for the photon/baryon/Weyl/clock transfer through recombination at that exact common calibration.

Freeze ONE physical wavenumber k=0.01/Mpc. Use the inherited common primordial curvature seed 1e-5, regular adiabatic initial conditions, zero additional vector/charge/entropy seed, cold baryon stress, massless thermal neutrinos, zero injection and the existing minimally coupled Thomson hierarchy. No primordial power-spectrum amplitude/tilt, reionization, TT/TE/EE spectrum, likelihood, native photon-origin or observational superiority is selected or claimed.

## Owned thermal input and unchanged solver

Reuse the FOUR final V003 candidate/reference default/half HYREC histories. No atomic, BBN, calibration, external executable, build or scan is invoked. Their nH0=0.18389667857584332 /m^3 and fHe=0.08107344068960111 determine n_e=xe*nH and the high-z fully ionized extension xe=1+2 fHe. Above the saved z=8000 endpoint use that existing fully ionized extension. Record its actual join discontinuity. Use the saved final BBN-derived helium and Neff, with RN=(7/8)(4/11)^(4/3) Neff; this is the predetermined joint tuple, not another fit.

The integration, matrix, constraint, initial-state, layout, Radau and error implementations are the pinned existing modules. The driver calls only their pure model/background and integration functions; it blocks the imported atomic invocation entry points. The original sources remain immutable. Authenticate all imported local implementation files before importing them, the joint result and its complete 18-entry input map, and all four claimed atomic-output hashes. Authenticate again before and after public output creation.

The NEW thermal adapter is the same `Thermal.background` implementation with V003 histories and HYREC's own normalization. It does not use the old nH0 approximation or the old one-fit calibration. Construct the inherited model exactly as the V003 driver did and verify every model parameter against V003 `fixed`; verify its measured-temperature radiation and physical baryon normalization against both saved final rows.

## Complete frozen trajectory census and gates

Candidate and reference each retain these SIX trials, with the inherited layout (photon/polarization lmax=16, neutrino lmax=48):

| Trial | Steps | Initial a | Atomic history | Layout / sampling |
|---|---:|---:|---|---|
| COARSE | 4096 | 1e-7 | half | 16/48, full |
| FINE | 8192 | 1e-7 | half | 16/48, full |
| START | 8192 | 5e-8 | half | 16/48, full |
| HIERARCHY | 8192 | 1e-7 | half | 20/64, full |
| ATOMIC | 8192 | 1e-7 | default | 16/48, full |
| THIN | 8192 | 1e-7 | half | 16/48, every second atomic row |

Integrate to a=1/801, with the unchanged 65 logarithmic snapshots, the common candidate visibility peak and z=8000 join. The smaller START extends only the initial prelude. Preserve all evolved fields, signed values and all snapshots. Reference removes only its established absent B/Zh fields from the numerical comparison.

The unchanged gates are: time/start/hierarchy/atomic/interpolation relative error <=1e-4; every trajectory Einstein-constraint residual <=1e-6; algebraic constraint identities and exact physical-background consistency <=1e-10. Time, atomic and thinning comparisons retain every evolved state. Start retains the existing endpoint comparison. Hierarchy compares the established common 11 fields and photon/neutrino/polarization multipoles through l=4. Do not replace a failing full-state result by a stable ratio or omit its limiting field. Save cold-baryon-pressure and linear clock-margin/spatial-gradient screens as descriptive diagnostics, rather than additional success gates.

At the visibility peak, z=800 and every inherited snapshot in 900<z<1500, save candidate/reference transfers per primordial curvature, every signed paired difference, and the five paired/candidate/reference refinement changes. Never divide the difference by a near-zero acoustic readout. This is a conditional linear transfer, not an angular CMB spectrum.

## Checkpoints, custody and closure

Use the exclusive stem `INVARIANT_CLOCK_JOINT_V003_RECOMBINATION_TRANSFER_V001` for source, manifest, journal, checkpoint directory, RESULT.json, REPORT.md, RECEIPT.json and ERROR.json. Numerical execution requires `--execute`. Optional `--resume` reuses only a fully written checkpoint plus matching COMMIT: same complete frozen input map, source/protocol digests, exact branch/trial/steps/layout/start/atomic/thinning/seed metadata and actual payload hash. An orphan, changed hash, duplicate event or mismatched specification is refused. Interrupted in-flight temporary/orphan files are preserved, never silently overwritten or treated as completed trials. No old trajectory checkpoint is reused as the new result.

Create the manifest before any trajectory, append the initial started PID and exact manifest/input-map identity, and journal every committed trial once. Record resumed PIDs explicitly. Recheck all current input seals before reuse and final closure. Public final outputs are exclusive and atomic; completed numerical failures still preserve every row/control under an unqualified status. Exceptional execution preserves exclusive ERROR evidence and completed checkpoints. Final completed outputs cannot be overwritten. Result/report/receipt share one frozen control census, with non-counting final hash guards.

Preserve these inherited facts verbatim in result/report/receipt: old recombination V002 has 76/76 numerical controls passed at Hunit=68.06502010698708; it is a DIFFERENT calibration. Late-lensing V001 has six failed numerical gates and remains unqualified. The earlier HYREC finite-pressure scan retains 207 uncomputed points after its saved panel; it is not resumed here. All old successes, failed attempts, exposed calibration/data and ancestry stay unchanged.

## Frozen direct inputs

Paths are relative to this directory; the source additionally authenticates the entire joint V003 input map.

| Input | SHA256 |
|---|---|
| INVARIANT_CLOCK_JOINT_CALIBRATION_V003_RESULT.json | c92eb0ce131a61009361f2ead3f4db7522d3eabb22f7e3d472f0e4e0c116c24f |
| invariant_clock_joint_calibration_v003.py | 9610ad24604eac4ac674038c97cccc66c354bb9a2f32037a87d62bccb459eeea |
| invariant_clock_recombination_transfer_v001.py | 6619fdc9cffe95703522acb0969ed45a00c483a994eea005907b789e977fb5b6 |
| invariant_clock_recombination_transfer_v002.py | 54674a431945eb7e17fc2b39af2324c923d8cfc5e991dc87a8cf96465dd1fa45 |
| invariant_clock_plasma_v001.py | 08cfd9e54759db07683bf652e32ad5aa69ec3006090f548e5d82b5678e8a6a28 |
| invariant_clock_radiation_v001.py | 0f30f231996feeeb3abe6f6f40326de3a34478adaac11e0520a5e1cf3e8bea3e |
| invariant_clock_transfer_v001.py | fad14451f7658c751a396c660638c5cb59e495b056fcbb5d09b0c8bc5a3415ca |
| invariant_clock_acoustic_v001.py | 9cd21314b29d11cedba04eb6e53799aa7847d40c1280718913d2a392bb3db396 |
| plane_canonical_evolution_v001.py | e2b634317ff0f22c77541a99c615dfcfcfb65e24c59013d8b09b5d322b740907 |
| charged_clock_response_v001.py | b7f539c914d3bf4af31f6b523b2a3c55b88c75fd406528358273f6d4ef95e5ba |
| bounded_clock_shared_prediction_v001.py | dd3d22e143e10b977fb7c0d6a2ce0a7cd260e0ddb077e3a9cf56e9e471f0b896 |
| hyrec_standard_oracle_v001.py | 2b176013f136aafd9495e448c882d1b6860769004be1027c90b5f094880be269 |
| PLANE_CMC_INITIAL_DATA_V002_RESULT.json | 04e6cdeac4c581671dac8afe6cb1229993f7ee5eadc54a560fa5fb79efa8535f |
| INVARIANT_CLOCK_RECOMBINATION_TRANSFER_V002_RESULT.json | 07fd5190198b2cf309b14598bfbae25def98d65b34db64b85dfe7a649da144cc |
| INVARIANT_CLOCK_LATE_LENSING_V001_RESULT.json | 642e2289f9ea2fc2790e3c6abcec823855e8b66810cbcd4864175d6f3f31b8c6 |
| INVARIANT_CLOCK_ACOUSTIC_V001_JOINT3_FINAL_CANDIDATE_DEFAULT_OUTPUT.json | 782bf0351bc99e1d72f9cbf215cec95ae99dd0f571d47574d160300208461274 |
| INVARIANT_CLOCK_ACOUSTIC_V001_JOINT3_FINAL_CANDIDATE_HALF_OUTPUT.json | f1e9312dc9f1f696a7e65d06f345da9daad814e0076456f9986665f51bb997c1 |
| INVARIANT_CLOCK_ACOUSTIC_V001_JOINT3_FINAL_REFERENCE_DEFAULT_OUTPUT.json | 50fe2c2d09b7e4dbc2a3bfac04da53a81d466bf0bd049e93c906c1543d2a779b |
| INVARIANT_CLOCK_ACOUSTIC_V001_JOINT3_FINAL_REFERENCE_HALF_OUTPUT.json | d026fb741fda6cd400d9fdca9e4589ba8d9c76adc06bda4ac737d4153d7ccc11 |
| hyrec_inputs_v001/HYREC_BAO_POINT10_PANEL_V001_RESULTS.json | a43ce0b033b84ddb3f72ed873200e9713e335d6cbc2c54c137807b491a71c623 |
| hyrec_inputs_v001/HYREC_BAO_INTERVAL_SAVED_AUDIT_V003_RESULTS.json | b53c9b477469641d4db082f0583c633c63863f3b134f57e0b097a9cb19487aba |
