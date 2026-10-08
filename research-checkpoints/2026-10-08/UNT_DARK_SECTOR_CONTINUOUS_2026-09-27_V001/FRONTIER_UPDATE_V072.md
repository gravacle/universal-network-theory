# Frontier V072 — thermal convergence failure localized; native completion gap

2026-09-30. Actual latest state after V071. Continue autonomously; all eleven
scientific lanes remain OPEN in ledger V013. No numerical worker is live at
this checkpoint. Root alone runs bounded numerical jobs, serially.

## Thermal packet complete, qualification failed

All eight fixed full-table acquisitions completed: states0/8, quarter
smoke64/smoke128/smoke128_offset2, half smoke128. Each preserves every original
deterministic V005 field except runtime. Native table counts are28333 coarse
and53333 refined, each with4097 common-log-a probes. Executable invocation
times0.629–1.171seconds, sampled process-group peak RSS40.6–72.7MB, no stderr
or process/monitor error. These times exclude controller preparation/custody.
Inputs, tolerances, upstream objects and physical histories were unchanged.

The independent saved-only auditor was source-reviewed by root and the
collector author, then sealed BEFORE the first acquisition intent. It ran once
under an external120second wall limit and its CPU/RSS guards. It authenticated
449 input artifacts and evaluated5,503,855 numerical checks. Exactly2 fail.
All8 individual unit controls pass;4/6 comparison pairs pass. No required unit
or pair was unavailable. Optional cb2 derivatives remain separately unavailable
and unqualified, as prospectively permitted.

Only history0's D2_K=Ksecond/(aH)^3 fails:

| Comparison | Probe; z | Signed difference | Allowance | Absolute difference/allowance |
| --- | --- | ---: | ---: | ---: |
| quarter coarse minus quarter refined | 726;1625.773896926712 | +441.2940451362299 |257.1532707120595|1.716074012647333|
| quarter refined minus half refined |470;2851.8156745887045|-1240.513482909199|257.1532707120595|4.824023740682772|

The norm is global pair amplitude, not pointwise fractional error or an
observational tolerance. All other pair controls pass, including visibility
second derivative, both origin checks and all history8 comparisons. The
history8 resolution D2_K margin is not large (~0.886 of allowance). Native
algebra/integral successes cannot cancel the failed convergence controls.
No threshold, probe, tail or comparison norm has been changed.

- K/CLASS_THERMAL_SAVED_AUDIT_V001_RESULTS.json SHA256:
  `3a032659cf3f2090255b94e7d01e5f64b60bf440f8a61ec9f93ecb6d0114cddb`.
- Root independently verified canonical payload:
  `27a24d8100cf2364a611261248f58cc33d0ee5910efef12df11bb7a30c857af8`.
- Audit seal: `52fb224871b7fe493d05d90415472ed69f18f2af892765f8648e21f707c3bd17`.
- Auditor source: `d67092bf3abb445f7977295caf809d53a650c209865c82a3bb1f37338af251c7`.
- Audit protocol: `50215dc897266d8507015d64821188381c95506b5b5ec36affc0773dda053df3`.
- Independent outcome review by an author of neither collector nor auditor:
  K/CLASS_THERMAL_SAVED_AUDIT_RESULT_INDEPENDENT_V001.md,
  `113aa2f13fd8e73a1faa7a885cd63352e0411c91be82b31f2a0d4f443cd11ed9`.

Audit analysis-phase resource snapshot14.1275seconds/359,940,096bytes excludes
result serialization/publication. All8 raw receipt identities and exact build/
input ancestry are retained in its449-input census. Do not rerun this packet
or auditor; their exclusive intents and failed status remain immutable.

## Cause discrimination now in progress, not a repair claim

Source review identifies the chain: FULL sliding cubic output -> fixed dz=.5
xe rows -> shape-preserving cubic Hermite xe(log(1+z)), C1 but not C2 -> CLASS
resampling on different conformal-time grids -> spline Ksecond -> interpolation
of that derivative column onto common probes. The resolution failure uses an
identical atomic input, so differing recombination physics cannot explain that
pair. Which representation link dominates still requires local diagnosis.
HYREC has approximation switches, but no saved event-location log assigns the
two redshifts to particular switches. Neither is near z=4000 or z=8000 edges.

Root-authored, peer-reviewed saved witness extraction is complete. It copies
5probe/13native/13actual input rows around each of the two fixed failed points
for the three history0 receipts; no new interpolation/evolution/derivatives or
qualification. Actual constants and original background packet are copied.
Exclusive intent, source/input hashes and caught-failure publication are owned.

- K/CLASS_THERMAL_CURVATURE_WITNESS_V001.json:
  `48d91fd06ab892d573a0ded8feef18405035ea52a5afda521ec52a514e74f6a6`.
- Witness source:
  `fd69fa0e9444b5f8a93d2a5a57dc57240ba32db1d2385444a37e538bee94d994`.
- Analysis2.703seconds, self RSS454,705,152bytes; external30second/CPU30/35
  and1GiB guards. No failure. No worker remains.

Exact next: short_path_adversarial is authoring a saved-only analytic PCHIP
curvature discriminator from this small witness. Derive one-sided knot jumps
and chain-rule Ksecond at the two failure locations; authenticate the dust
background parameters and retain both ordinary radiation and vacuum. Root and
peer must read/review before one bounded execution. This is attribution, not a
post-hoc pass test. Then choose a justified separately frozen numerical repair
if supported, retaining V001 failure and its original criteria. Changing only
the diagnostic readout cannot repair the runtime thermal interpolator.

## Prepared next-mode source, still locked

critical_path_native finished inert ABI-correct diagnostics_v004, hooks_v002,
typed output_v001 and emit_class_evolved_sources_v001.py with
CLASS_EVOLVED_SOURCE_ADAPTATION_PROTOCOL_V001.md. The independent source reader
reported PASS, but root has not yet fully read the complete new packet. No
emitter execution, controller, source freeze, compilation or mode run exists.
Current failed thermal audit cannot unlock it. Actual repaired ancestry must
be owned first. Common refined background/thermal stays fixed as mode64/128
changes only perturbation controls. Exactk=.001 and V002 criteria stay unchanged.

## Native mechanism result and honest local input gap

J/NATIVE_COHERENT_WRITER_UNITALITY_V001.md,
`882da1d5745a7b67dd16ed4c4b370f01fb590279ad00e801d1109d76ed01cfef`,
extends the previous zero-gap blank-fragment theorem to the actually owned
coherent writer preparation. Conserved writer blocks each see one target
operator; the accessible identity is preserved even though actual writer
coherences are retained. This is a symbolic extension, not a reservoir added
to the old experiment. It neither proves mixing nor forbids transient
passivation or new physical completions. Root read the note and cited generator,
BS state contract and contact-identifiability argument; analytic peer check
is recorded separately from numerical reproduction.

The current seed leaves the mission state, port supply, source/volume contacts
and relevant physical completion unspecified. Existing retain/copy/average
tests do not derive them. A new mechanism may be explored only as explicitly
new physical content, not silently selected for its desired sign. This local
native-model input gap does not halt useful independent Stage3 work. Prior
negative spectral result stays unchanged; no duplicate eigensolve is needed.

FULL125/335(next125), growth105/335(next105), ordinaryPRIMAT/halo/two-current
results and URM immutableV008 candidate snapshot are unchanged. HeartbeatACTIVE;
historical Goal untouched. Sole local UNT root, no otherMac, installs, settings/
security change, L8/heavyremote, publication or credits. Continue beyond this
checkpoint; no acknowledgment is required and Stage3 is not complete.
