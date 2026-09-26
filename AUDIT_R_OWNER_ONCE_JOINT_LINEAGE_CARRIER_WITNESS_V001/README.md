# Independent hostile source: owner-once joint lineage--carrier witness

Status: `HOSTILE_SOURCE_FROZEN_READY__NO_SEED_OUTPUT_OPENED`

This directory contains the independently written hostile implementation of
the frozen witness protocol in
[`DEVELOPMENT_R_OWNER_ONCE_JOINT_LINEAGE_CARRIER_WITNESS_V001`](../DEVELOPMENT_R_OWNER_ONCE_JOINT_LINEAGE_CARRIER_WITNESS_V001/PROTOCOL.md).

The implementation was written before inspecting any target implementation or
target result.  It uses:

- descending integer-word lineage and carrier bases;
- connector-first, reverse-site prism edge order;
- an independently written admission rotation;
- matrix-free order-12 Taylor transport at both 64 and 128 substeps;
- independent row-first and column-first witness accumulators;
- the exact sector-matched sham product;
- the analytic within-`q` permutation identity, future exhaustive L4
  permutation enumeration, and an independent dense direct-basis check;
- sham and shuffle negative controls; and
- deterministic, relative-path-only JSON reporting.

Physical seed execution is deliberately locked behind the exact authorization
string frozen in the source.  This phase has not run the L4/L6/L8 history and
has not produced `HOSTILE_RESULT.json`.

## Authorized execution compatibility repair

The first authorized execution attempt on 2026-09-22 stopped before writing
an output because the local Apple BLAS emitted a `RuntimeWarning` from a
diagnostic `matmul`, which the frozen `PYTHONWARNINGS=error` guard correctly
treated as fatal.  The repair replaces only BLAS-backed witness reductions
with algebraically identical explicit elementwise sums.  It changes no
parent, chronology, observable, control, parameter, tolerance, or reporting
rule.  The failed attempt produced no physical result and no target material
was inspected.  Full details are in `EXECUTION_COMPATIBILITY_REPAIR.md`.

## Permitted source-freeze tests

The following suite uses only synthetic L2/L3 states.  It does not call the
physical seed reporter or inspect any L4/L6/L8 witness value:

```sh
PYTHONWARNINGS=error python3 -B \
  AUDIT_R_OWNER_ONCE_JOINT_LINEAGE_CARRIER_WITNESS_V001/test_source_freeze.py
```

It checks basis and graph reconstruction, admission, a small transport
control, the matched/crossed non-identifiability pair, full synthetic shuffle
enumeration, dense-direct versus streamed witness agreement, deterministic
source metadata, and the no-target-import boundary.

## Future execution (not performed in this phase)

Only after separate authorization, execute from the `audited-386ee2c` root:

```sh
PYTHONWARNINGS=error python3 -B \
  AUDIT_R_OWNER_ONCE_JOINT_LINEAGE_CARRIER_WITNESS_V001/independent_joint_witness.py \
  --authorize-seed AUTHORIZE_L4_L6_L8_JOINT_WITNESS
```

That future command will run both numerical resolutions at L4/L6/L8 and
write the hostile record.  Its standalone disposition explicitly remains
pending separate target adjudication.

Files in this freeze:

- `independent_joint_witness.py` -- hostile implementation and locked JSON
  reporter;
- `test_source_freeze.py` -- synthetic, non-physical source tests;
- `README.md` -- independence and execution boundary;
- `SOURCE_FREEZE.json` -- deterministic source hashes and protocol custody;
- `EXECUTION_COMPATIBILITY_REPAIR.md` -- pre-output compatibility-repair
  record; and
- `SOURCE_HASHES.sha256` -- checksum manifest for the frozen source packet.

This code tests only a finite terminal joint correlation in the existing
owner-once engine.  It introduces no Gate, RGRL, alpha, GL6T, thermodynamic,
continuum, or gravity premise.
