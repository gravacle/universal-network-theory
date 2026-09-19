# L12 Stage-6R3 record-flow supplemental adjudication

This packet evaluates the sealed L12 record-flow bridge under two distinct
aggregation laws. It is an owner-once, read-only supplement. Stage-6R2 and all
earlier evidence remain unchanged.

## Audited outcome

Classification:
`STAGE6R3_RECORD_FLOW_OBSERVED__ORIGINAL_Z1_GATE_REMAINS_REJECTED`

### Whole-sector connectivity rule

- Deduplicated q4+q5+q6 mass: `0.56956498393327842`
- Arithmetic `>= 0.50`: pass
- Admissible under the frozen Stage-6 protocol: **no**

The frozen protocol groups adjacent atoms only after each atom passes the full
Stage-6 conjunction. A011 and A016 pass the exploratory z/y window but fail the
full conjunction. No q5 atom passes. Record-flow sector connectivity is not a
preregistered replacement for these requirements.

### Conservative flow-support rule

- q4+q6 endpoint-sector mass: `0.36652893665484882`
- q5 mass required to reach 0.50: `0.13347106334515118`
- Certified common-lineage q5 mass: absent
- Disposition: `UNRESOLVED_FAIL_CLOSED`

`pbar_q` is the arithmetic mean of complete sector weights over events 6--12.
The sidecar flow values are source-sector component norms transferred at event
12. No authenticated theorem converts between those measures, and no preserved
lineage intersection proves that the same q5 support participates in both
q4->q5 and q5->q6 components.

For orientation only, assuming commensurability and using the smaller terminal
flow would give `0.45457010492111312`, still `0.04542989507888688` short. This
number is explicitly not a gate value.

## Decision

Stage 7 is not authorized from Stage-6R3. Closure requires one of:

1. an independently audited theorem adopting whole-sector record membership
   and replacing the original endpoint/full-conjunction rule;
2. event-6--12 lineage-resolved q5 support on the same `pbar` measure; or
3. a preregistered next-size scout seeking fully passing bridge atoms.

## Artifacts

- `STAGE6R3_SUPPLEMENTAL_ADJUDICATION_V001.json`
  - SHA-256: `7fa2062f18be3c90c9167e917974d1cc609273da623966e4068f1c0d1133e2b4`
- `stage6r3_supplemental_adjudicator.py`
  - SHA-256: `c46b7511bcab4a99ea180b4390293cd92d1ec1ccf614cbb05475adbb4db31393`
- `test_stage6r3_supplemental_adjudicator.py`
  - SHA-256: `c4edef64774fd74257610685854d95d2679725f953638ce4e73962d35746569e`
- `verify_stage6r3.py`
  - SHA-256: `f75cbdcf24a4f10927e1b6d29912dd26d8494bab54d4f466f498ec0b1d01dea5`

## Reproduction

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_stage6r3_supplemental_adjudicator.py
PYTHONDONTWRITEBYTECODE=1 python3 stage6r3_supplemental_adjudicator.py
PYTHONDONTWRITEBYTECODE=1 python3 verify_stage6r3.py
```

