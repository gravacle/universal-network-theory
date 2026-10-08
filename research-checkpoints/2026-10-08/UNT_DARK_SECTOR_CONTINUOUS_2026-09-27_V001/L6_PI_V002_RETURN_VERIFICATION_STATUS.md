# L6 pi completion V002: originating-machine verification status

2026-09-27. Current status: internal archive manifest and table verification
completed successfully after the user reattached the ZIP. The initial missing-
clipboard attempt below is preserved; see the successful addendum at the end.
This verifies internal consistency, not independent sender authentication,
physics replay or dark-sector acceptance. No archive content was executed.

## Observed before disappearance

- ZIP supplied at `/Users/bgm/Library/Group Containers/group.com.apple.coreservices.useractivityd/shared-pasteboard/items/E29126DE-CC04-4F35-A323-C7E7735E3F2E/UNT_L6_PI_TRANSPORT_COMPLETION_RESULT_V002.zip`.
- Resident size 8,999,942 bytes; SHA256 measured by originating machine:
  `8d61b5e934896ec290cab03b6206ab1b2343577f9a402afea3032c7160be6523`.
  No independently supplied sender digest was available.
- ZIP directory census: 3,257 entries, 27,254,327 expanded bytes including
  manifest. Manifest claims 3,256 other members / 26,474,518 bytes.
  These counts were inspected, not all member hashes verified.
- The separately attached 18,680-byte SCIENTIFIC_REPORT.md was read fully.
  Its supplied clipboard path was under item
  `64AA4180-A07F-473F-9B71-A6DC3230D73D`.
- README, included verifier SOURCE (not executed), manifest metadata,
  scientific-summary keys and three CSV headers/initial rows were inspected.
- Independent agent reviewed the phase facade, protocol, capture and source
  reviews, dephasing proposal and prior algebra directly from the archive.
  Facade SHA256 independently matches
  `2feebea605534842d9494189bea0e1b1e71800c848b3093d92d3f36450f4a63e`.
  See `L6_PI_COMPLETION_V002_INDEPENDENT_INTERPRETATION.md` for the precise
  source-review and causal-interpretation limits.

The report states the fresh pi census completed q=0..6 in both lanes and
both numerical settings, while preserving earlier pi/4 and six-event tests.
It reports 66 accepted covariance predictions and a maximum pi occupation
contrast +0.0018498697129894328 (site 0), with largest absolute pair contrast
-0.0006187511915883186 (3,5). These remain reported values pending the root
table check; they have not been independently replayed here.

## Preserved failed verification attempt

`verify_l6_pi_v002_return.py` was written locally using the standard library.
It executes no payload scripts, extracts nothing, bounds ZIP/input sizes,
checks exact member coverage/hashes and plans to cross-check table arithmetic.
It pins the locally measured ZIP hash, not an independent sender identity.

The first invocation failed before opening the archive at `path.stat()`:

    FileNotFoundError: [Errno 2] No such file or directory
    .../E29126DE-CC04-4F35-A323-C7E7735E3F2E/UNT_L6_PI_TRANSPORT_COMPLETION_RESULT_V002.zip

Subsequent read-only `ls -ldO` / `ls -lO` checks confirmed that BOTH the ZIP
item directory and separate report path no longer existed. Other read-only
commands in the same shell invocation completed, so the shell's combined
exit code was zero; this does NOT mean the Python verification succeeded.
No member hash or table-arithmetic pass is claimed from that attempt.

The user was asked to reattach from a permanent folder or supply a saved
path. With the same ZIP bytes, rerun this read-only verification against the
new path. That is an input-check retry, not a production-physics retry.
If bytes differ, inspect the new identity rather than silently changing the pin.

## Remote state and scientific next step

The user supplied a fresh explicit report that the authorized queue is
complete and idle, workers/caffeinate are stopped, dephasing has not begun
and L8 remains locked. No live remote handle is available here; no remote
dispatch or power assertion was made.

Matched occupation dephasing is a useful proposed correlation/coherence
discriminator. It preserves diagonal covariance and sector weights but can
change full marginals, energy and factor rank. It is not itself a dark-sector
prediction, proof of entanglement, or an energy-matched intervention.
Prospective costs and authority must be resolved before execution. The
attachment's suggested successor is not treated as a user instruction.

## Successful reattachment and verification addendum

The user reattached the ZIP under clipboard item
`C1F75AE2-35FE-476E-BA00-E72844BB3706`. After resident-flag and target-absence
checks, it was copied without overwrite to this project folder as
`UNT_L6_PI_TRANSPORT_COMPLETION_RESULT_V002.zip` (8,999,942 bytes). Its hash
exactly matches the earlier measured ZIP; no pin was changed.

Executed read-only:

    /usr/bin/python3 -B UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/verify_l6_pi_v002_return.py UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/UNT_L6_PI_TRANSPORT_COMPLETION_RESULT_V002.zip

Exit code 0; observed execution wall time about 0.21 seconds. Full output
is preserved in `L6_PI_V002_RETURN_VERIFICATION_RESULT.json`.

- All 3,256 manifest-listed members matched size and SHA256, with exact
  coverage, canonical unique regular-file paths and no special/link objects.
  Manifest excluded from its own hash census as required; 26,474,518 listed
  bytes. Manifest hash `e7eefc64de69b36e543d567b33c0f42149fce6b9345bcc86904c19c0de70d2c1`.
- All 9,984 main table rows have complete, unique expected axes and observable
  coverage: two dwells, two lanes, two settings, before/after, seven sectors
  plus aggregate, and 78 observables. Aggregates equal sector sums exactly
  in this returned-table arithmetic. Signed differences agree to 4.73e-17.
- Independent dwell starts have identical returned initial readouts. The
  78-row signed table agrees exactly with the main table's final aggregates.
- The 132 prediction rows cover 66 event/partner predictions in both settings;
  the covariance formula is reproduced from the returned inputs with zero
  difference. Maximum prediction residual is 5.2909066017292616e-17 and maximum
  lane difference 5.551115123125783e-17. Signs are 36 positive / 30 negative.
- The reported largest pi occupation and pair contrasts are reproduced.

Table-only cross/refinement maxima are smaller than the report's maxima
which also include arm traces; no discrepancy is inferred from the different
scopes. This audit did not independently replay traces, conserved controls,
qualification runs, formation histories, cleanup evidence or full forward
error. It does not claim independent physics regeneration. The separate
report file had disappeared and was not byte-compared on the successful
invocation; the archive's own report is covered by its verified manifest.

Root additionally read the prospective dephasing proposal, complete V002
protocol and phase facade from the preserved ZIP. The attached successor
explicitly lacks an execution budget/cost estimate and authorizes no run.
No new remote calculation or successor was launched.
