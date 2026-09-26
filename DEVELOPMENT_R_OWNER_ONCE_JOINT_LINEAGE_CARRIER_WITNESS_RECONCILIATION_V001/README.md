# Owner-once joint lineage--carrier witness reconciliation V001

This packet independently reconciles the already sealed L4/L6/L8 target and
hostile results for the frozen owner-once joint lineage--carrier witness.  It
does not rerun either physical calculation and does not read or compute the
held-out L10/L12 witness.

The reconciler authenticates the protocol, both results, both implementations,
tests, source-freeze record, execution record, target seal, hostile checksum
manifests, and historical dependencies against hashes pinned in the
reconciliation source.  It then independently checks:

- the exact frozen parameters, tolerances, mandatory size set, event order,
  primary terminal checkpoint, and output schemas;
- the target and hostile deterministic-rerun seals and byte counts;
- all target and hostile norm, content, probability, marginal, charge,
  row/column, sham, shuffle, and L4 exhaustive controls;
- `w_L`, `w_L^sham`, `D_L`, every `q`-resolved `D_q`, and every `p_(L,q)`
  across the target and hostile fine-resolution terminal records;
- the target 64-versus-128 disagreement and both implementations'
  row-versus-column disagreement;
- `d_L`, `r_L`, `tau_L`, every `T_L`, and the frozen minimum `T_4:8`; and
- the exact three-way classification rule in Section 6 of the protocol.

Any missing file, changed hash, malformed manifest, wrong parameter, missing
size, nonfinite number, altered condition flag, failed control, or schema
mismatch raises a reconciliation error.  The command-line wrapper emits an
`OWNER_ONCE_JOINT_LINEAGE_CARRIER_WITNESS_UNRESOLVED` record and exits nonzero
on such a failure.  It refuses to overwrite a sealed input.

## Reproduce

Run from the `audited-386ee2c` root:

```sh
python3 -W error -B \
  DEVELOPMENT_R_OWNER_ONCE_JOINT_LINEAGE_CARRIER_WITNESS_RECONCILIATION_V001/reconcile_joint_witness.py

python3 -W error -B \
  DEVELOPMENT_R_OWNER_ONCE_JOINT_LINEAGE_CARRIER_WITNESS_RECONCILIATION_V001/test_reconcile_joint_witness.py
```

The first command deterministically rewrites `FINAL_DISPOSITION_V001.json`.
Two independent invocations produce byte-identical JSON.

## Files

- `reconcile_joint_witness.py` -- fail-closed authenticator and adjudicator;
- `test_reconcile_joint_witness.py` -- real-packet, mutation, nonfinite,
  manifest-tamper, classification-boundary, and determinism tests;
- `FINAL_DISPOSITION_V001.json` -- machine-readable final disposition;
- `RESULT.md` -- human-readable scientific and numerical disposition;
- `TEST_LOG_V001.txt` -- commands and clean test summaries; and
- `MANIFEST.sha256` -- SHA-256 inventory of every packet file except itself.

The final classification is
`RESOLVED_OWNER_ONCE_JOINT_LINEAGE_CARRIER_WITNESS_L4_L8`.  Its scope is only
the finite terminal correlation measured by the one frozen observable at
L4/L6/L8 in the existing owner-once engine.  See `RESULT.md` for the exact
claim boundary.
