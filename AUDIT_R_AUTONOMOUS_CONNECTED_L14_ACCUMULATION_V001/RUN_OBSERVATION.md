# Independent run observation

Command:

```sh
PYTHONWARNINGS=error python3 -B AUDIT_R_AUTONOMOUS_CONNECTED_L14_ACCUMULATION_V001/independent_reconstruction.py
```

Terminal result:

```text
AUDIT_PHASE__{"aggregated_entries": 201326276, "elapsed_seconds": 8.311788541, "max_rss_bytes": 4706172928, "orbit_histogram": {"1": 4, "14": 41742, "2": 6, "28": 9566046, "7": 252}, "phase": "L14_GENERATOR_BFS_AND_AGGREGATED_CSR_COMPLETE"}
AUDIT_PHASE__{"csr_bytes": 3096758548, "elapsed_seconds": 8.925307250000001, "hermitian_bilinear_error": 8.179139557482623e-17, "max_rss_bytes": 5744263168, "phase": "L14_STRUCTURAL_NUMERICAL_PROBES_PASS", "source_current_linf": 0.0, "source_energy_imag": 0.0, "source_norm_error": 0.0}
AUDIT_PHASE__{"elapsed_seconds": 1297.891833708, "max_rss_bytes": 5746900992, "phase": "FINE_RK4_PROGRESS", "step": 2048, "steps": 2048}
AUDIT_PHASE__{"checks": "29/29", "elapsed_seconds": 1299.5159334999998, "max_rss_bytes": 5746900992, "phase": "AUDIT_COMPLETE", "verdict": "PASS__INDEPENDENT_L14_NUMERICAL_RECONSTRUCTION"}
PASS__HOSTILE_L14_INDEPENDENT_NUMERICAL_AUDIT__29/29
```

This is the successful hostile run. The two earlier unsafe lift proposals were
rejected without execution and the earlier audit verdict remained fail-closed
until this run completed. Runtime and RSS are single-run engineering
observations, not complexity claims.
