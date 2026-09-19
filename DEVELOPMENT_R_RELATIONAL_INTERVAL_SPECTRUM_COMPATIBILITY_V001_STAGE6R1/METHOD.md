# Stage 6 source-freeze census repair R1

This bounded repair addresses one pre-computation interface defect in the
Stage 6 V001 compatibility packet.  The runnable implementation requires the
seven-file source census declared by `blind_contract_control.py`, while the
older `SOURCE_FREEZE.json` contains six entries, omits
`blind_adjudication_entrypoint.py`, and carries hashes from before the
September 9 compatibility edits.

The failed `RUN_V002_L12_V003R1` allocation produced only a deterministic
`SECTOR_PLAN.json`.  It produced no runnable blind-method freeze, credential,
physical blind row, blind index, target run, target index, or adjudication.
That allocation remains immutable as failure evidence.

R1 creates a new source freeze before physical Stage 6 work.  It lists exactly
the seven files required by the unchanged validator and retains the unchanged
five dependency bindings.  The current control, worker, publisher, and
adjudication-entrypoint bytes were also independently pinned by both the
Stage4R1 and Stage5R1 pre-output freezes before Stage 5 output existed.

Execution uses fresh `..._STAGE6R1` blind and target workspaces.  It delegates
plan construction, runnable-freeze construction, credential issuance, blind
row execution, blind publication, target execution, and exact adjudication to
the already tested Stage 6 implementation.  No physics definition, numerical
guard, fit family, predicate, tolerance, sector census, or result is changed.

The continuation is owner-once and stops after recording the audited Stage 6
result.  Stage 7 is outside its code path.

