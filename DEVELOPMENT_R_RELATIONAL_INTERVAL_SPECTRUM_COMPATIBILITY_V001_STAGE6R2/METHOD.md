# Stage 6 sandbox-telemetry allocation recovery R2

Stage6R1 successfully repaired and authenticated the source-file census, then
entered the first four-sector blind wave.  The sandbox refused the unchanged
read-only `ps` call used by the RSS guard.  The owner-once continuation stopped
the wave.  One small blind row completed before termination; four credentials
were issued.  No blind index, target run, target index, or adjudication was
created.

The Stage6R1 allocation is retained byte-for-byte.  R2 reuses the Stage6R1
source freeze, which was created and validated before any Stage6R1 physical
row.  It uses fresh `..._STAGE6R2` blind and target workspaces and is intended
to execute with permission for the existing process-telemetry guard to query
worker RSS.

No source, Hamiltonian, numerical guard, fit family, predicate, tolerance,
sector census, or result is changed.  The same tested Stage 6 implementation
performs the complete owner-once run.  R2 stops after the audited Stage 6
result and contains no Stage 7 execution path.

