# L8 lineage-order Ollivier--Ricci packet V001

This packet records a prospective, inexpensive postprocessing test on the
already completed L8 owner-once state.  It introduced no new evolution and no
checkpoint/restart machinery.

Artifacts:

- `PROTOCOL.md` freezes the graph, curvature convention, observable,
  statistic, null, thresholds, and claim ceiling.
- `FREEZE.json` gives the machine-readable freeze and authenticated inputs.
- `SOURCE_HASHES.sha256` preserves the pre-output protocol, freeze, and
  implementation hashes.
- `compute_lineage_order_curvature.py` is the explicitly guarded frozen
  implementation.
- `RESULT.json` is the atomic output.
- `RESULT.md` gives the scientific disposition and boundary.
- `validate_result.py` is a strict independent result validator.
- `test_validate_result.py` exercises the accepted record and fail-closed
  mutations.
- `MANIFEST.sha256` authenticates the complete packet except itself.

The result is a resolved null for the formation-order path:

`NO_RESOLVED_LINEAGE_ORDER_CURVATURE_RECORD_ASSOCIATION_L8`.

It is not a no-go theorem for all lineage graphs and says neither that graph
curvature is spacetime curvature nor that gravity is absent.

Validation from the audited repository root:

```bash
python3 DEVELOPMENT_R_L8_LINEAGE_ORDER_OLLIVIER_RICCI_V001/validate_result.py
(cd DEVELOPMENT_R_L8_LINEAGE_ORDER_OLLIVIER_RICCI_V001 && python3 -m unittest -v test_validate_result.py)
shasum -a 256 -c DEVELOPMENT_R_L8_LINEAGE_ORDER_OLLIVIER_RICCI_V001/MANIFEST.sha256
```
