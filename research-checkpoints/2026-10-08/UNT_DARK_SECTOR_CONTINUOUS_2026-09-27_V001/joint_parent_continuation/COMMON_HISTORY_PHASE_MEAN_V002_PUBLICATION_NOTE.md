# V002 result published; console summary failed afterward

2026-09-28. V002 successfully normalized and atomically published
`COMMON_HISTORY_PHASE_MEAN_V002_RESULTS.json`. The subsequent optional console
summary still used V001's ordinary `json.dumps` on the in-memory NumPy boolean
and exited 1. This happened AFTER the result publication; it is not a clean
whole-process success. No numerical rerun or overwrite was performed.

A separate read-only check loaded the published JSON, authenticated its freeze
and canonical payload hashes, and confirmed its all-row scientific checks.
All 36 phase means and mode-level results are present. The console defect
affects only the unnormalized print summary, not the normalized saved artifact.
The V001 failure, both sources and freezes remain unchanged. Future use should
read the saved result; any driver repair must additionally normalize the final
console output before claiming a clean command exit.
