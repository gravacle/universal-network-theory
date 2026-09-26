# L10/L12 owner-once joint-witness recognition packet V001

Status: `RECOGNIZED_WITH_DISCLOSED_PROCEDURAL_DEVIATION`

This packet records the completed exact L10/L12 calculation without modifying
any frozen protocol, sealed result, source freeze, receipt, or historical
artifact. It separates three conclusions that must not be conflated:

1. **Computational result.** The source-isolated target and hostile programs
   produced independently agreeing finite L10/L12 values. Their final atomic
   JSON files authenticate at SHA-256
   `804b3dda5ebed693ceee26afdedc754602b02a3e8eb7482539f64016d2b54b4b`
   and
   `7e1d1c68dfc50fade4acbe3d39ef04b22394872832ce0475847a1098cfc045f9`.
   Recomputed numerical and control diagnostics pass, and the original
   two-sided statistic is far above one at both sizes.
2. **Strict protocol status.** This packet does not claim that the original
   held-out protocol formally passed. The observed branch-release gap was
   `10,748 s`, not the frozen maximum `60 s`; that deviation is disclosed.
3. **Secondary persistence prediction.** The later signed criterion frozen at
   `f = D8 = 0.001963064475535806` fails at both sizes. The witness reverses
   sign and its magnitude is much smaller than at L8.

## Why the timing deviation does not erase the computation

The 60-second rule was an anti-contamination and blinding safeguard. It was an
operational custody rule, not part of the deterministic equations. Read-only
filesystem chronology records:

| event | UTC |
|---|---|
| target scratch born | `2026-09-23T14:45:33Z` |
| hostile scratch born | `2026-09-23T17:44:41Z` |
| hostile atomic result born | `2026-09-25T04:36:49Z` |
| target atomic result born | `2026-09-25T16:13:29Z` |

Thus neither final result existed at either launch; the target calculation was
already deterministic and running before the hostile launch; the hostile
result declares that it read no target code, arrays, matrices, or values; and
the independently written atomic results agree at approximately `10^-17` in
`D_L`. The wall-clock gap therefore does not bias the numerical answer.

Future protocols should gate on actual value access and implementation
independence, bind launch receipts to both roles, and treat wall-clock skew as
metadata unless a scientific reason for simultaneity is stated in advance.
That prospective policy does not rewrite the old freeze.

## Reproduction

From the repository root:

```text
python3 DEVELOPMENT_R_OWNER_ONCE_JOINT_LINEAGE_CARRIER_HELDOUT_RECOGNITION_V001/recognize_heldout_witness.py
python3 DEVELOPMENT_R_OWNER_ONCE_JOINT_LINEAGE_CARRIER_HELDOUT_RECOGNITION_V001/validate_recognition.py
python3 -m unittest -v DEVELOPMENT_R_OWNER_ONCE_JOINT_LINEAGE_CARRIER_HELDOUT_RECOGNITION_V001/test_recognition.py
```

These commands read the two final atomic JSON files. They do not open or use
partial arrays, rerun the expensive physics, or alter historical artifacts.

## Claim boundary

The recognized result is finite exact computational evidence for a nonzero,
two-sided owner-once joint lineage--carrier association at L10 and L12. It is
not evidence for positive no-decline persistence, an all-L or thermodynamic
limit, the Gate, RGRL/WTC response, alpha, record curvature, continuum
geometry, Einstein dynamics, or gravity.
