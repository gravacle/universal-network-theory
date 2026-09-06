# Independent extended-centerline readiness report

**Verdict:** `PASS_READY_FOR_SEMANTIC_GATE__NO_L10_L12_EXECUTED`  
**Audit:** `107/107` checks passed

The frozen independent implementation reconstructed the owner-once prism,
translation orbits, sparse momentum blocks, positive-overlap ground Krylov
sequence, and response-cyclic Krylov sequence without importing the target
extended-phase module or its outputs.  Only the sealed centerline controls
`L4q2`, `L6q3`, and `L8q4` were executed.  The independent output was written
before the comparison verifier read the sealed L4/L6/L8 reference result.

| L | q | `Delta_act` | `chi_tau` | `R_low` | matvecs | wall seconds |
|---:|---:|---:|---:|---:|---:|---:|
| 4 | 2 | 2.463075497382996 | 0.341638044263196 | 0.428094707815654 | 11 | 0.001230 |
| 6 | 3 | 1.667371519018324 | 0.520382482559258 | 0.632801772065040 | 64 | 0.010486 |
| 8 | 4 | 1.266065438740814 | 0.702672515154985 | 0.732829820693634 | 64 | 0.064843 |

Maximum relative disagreements with the sealed reference were

```text
ground_energy  1.679e-15
Delta_act      4.794e-15
chi_tau        4.480e-15
R_low          8.484e-15
```

The complete validation used `0.078175` wall seconds and peaked at
`28,590,080` bytes RSS.  Every row satisfied the Hermiticity, orthogonality,
actual Ritz-residual, response-projection, momentum-covariance, threshold,
matvec, wall, and memory guards.  Each final ground and response checkpoint
reports its lowest five Ritz values in `INDEPENDENT_VALIDATION.json` and the
per-row raw files.

The executable has explicit future-row support for `L10q5` and `L12q6`, but
refuses those rows without the literal token
`ALLOW_REQUIRE_SEMANTIC_GATE_PASSED`.  No L10/L12 raw output exists in this
packet.

## Frozen and result hashes

```text
d6b18172ad6728affa1b9d86a949e5375f66329d2a121153854648b6b05d76d0  FROZEN_METHOD.json
dbe28ec72e64cea10b9e974213277c284ffd20596877a06fdca4ee66ba4075a4  METHODOLOGY.md
79aec7d5a773f8a7268ae98c6c343201a331e628274a3d225432059dee6b7fa7  independent_centerline.py
db8dcdff56b24a1cdfce850b090e9c1e3f2cccbe4c882d52b30e06fd92c81c28  verify_validation.py
1e812fc5668fd0f75d547bb81f5b1cfaa76c1f6776c0803ab93c7a206ea4adfd  INDEPENDENT_VALIDATION.json
8f2e4b74ddfbcff56c256a9633bb5ff06427a3afabee3a2d45c7de88a6aaf365  VALIDATION_AUDIT.json
```

This is solver readiness only.  It supplies no L10/L12 result, `z=1`
classification, gapless limit, continuum algebra, anomaly, emergence, or
gravity claim.
