# R-Gate-C L4+L4 to L8 hostile audit

This packet independently audits the frozen composition-closure protocol. Run:

```sh
python3 -B AUDIT_R_GATE_C_L4_L4_TO_L8_COMPOSITION_CLOSURE_V001/hostile_audit.py
```

The verifier hash-pins the finalized development and adversarial packets plus every pre-comparison frozen record, reconstructs the owner surgery without importing target code, checks conservation and Schmidt-tail agreement, and writes `INDEPENDENT_RESULT.json` reproducibly.

Files:

- `FROZEN_INDEPENDENT.json`: pre-comparison topology, source, spectrum, reconstruction tails, and independent lower-order collision.
- `FROZEN_REFINEMENT.json`: pre-comparison finer Suzuki-Yoshida L8 spectrum.
- `FROZEN_CONSERVATION.json`: pre-comparison owner-once current and conservation ledgers.
- `hostile_audit.py`: final hash-pinned hostile verifier.
- `INDEPENDENT_RESULT.json`: machine-readable audit verdict.
- `AUDIT_REPORT.md`: human-readable claim-bounded verdict.

The pass applies only to the obstruction/mandatory-stop result. Exact D8 remains unresolved in `[251,256]`; no L12 was run and no continuum or gravity claim is authorized.
