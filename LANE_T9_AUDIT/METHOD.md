# T-9 CARRIER AUDIT — METHOD

Six range-partitioned probes audited all 146 FORMAL/PROVED/MEASURED rows against the canonical
carrier taxonomy (toric-2x2 family, steane-713, DD4, bouquet, chamon-fcc, rank2-abelian, spin-chain,
macrospin-CoCrPt, NAND-floating-gate, azobenzene, alanine, perfect-513), with STRUCTURALLY DIFFERENT
meaning different algebra/mechanism, never the same model at another size or parameter set. Probes
defaulted to SINGLE-CARRIER; every TWO-CARRIER claim was attacked by an adversarial refuter checking
the cited evidence exists, concerns the row's actual result, and the carriers genuinely differ —
refuted claims were demoted with the refutation reason kept in the evidence column. Withdrawn
evidence does not count (the azobenzene/alanine rows withdrawn under C-70 support nothing).

Initial coverage: 146/146, no duplicates, no misses. Initial verdicts: SINGLE-CARRIER 111,
TWO-CARRIER 21, NOT-CARRIER-SHAPED 14 (rows whose content is not a computation on a carrier —
meta-classifications, literature statements, definitional consequences; used sparingly per
instruction). The append-only table now contains 157 verdict rows: 116 SINGLE-CARRIER, 22
TWO-CARRIER, and 19 NOT-CARRIER-SHAPED, again with no duplicate IDs. It covers all 156 currently
in-scope `FORMAL`, `PROVED`, and `MEASURED` ledger rows; the additional retained verdict is `C-72`,
which was `PROVED` when audited and later moved to `PARTIAL`. The finite-relational-accumulation
computations are one carrier family across sizes; target, blind, and hostile implementations are
independent reconstructions of that same carrier, not additional carriers.
At the initial audit, the two `PROVED` rows were `C-71` and `C-72`, both TWO-CARRIER
(NAND-floating-gate; macrospin-CoCrPt). `C-72`'s later status change does not rewrite its historical
carrier verdict.

## THE AT-REGISTRATION RULE (T-52, 2026-08-21)

**A newly registered row at status `FORMAL`, `PROVED`, or `MEASURED` is audited AT REGISTRATION** —
its verdict row appended to `T9_carrier_audit.tsv` in the same landing that registers it, under this
method unchanged (default `SINGLE-CARRIER`; a refuter confirms every `TWO-CARRIER` claim on
structurally different carriers; a dimension discriminator or spot-check never counts). The debt this
rule closes accumulated once — `C-90`, `C-91` and `A-PR` sat unaudited at the head of the emergence
chain — and may not re-accumulate. `replicate/check_proof.py`'s R5 reads this table as the record,
so an unaudited new row surfaces as `UNAUDITED` in the proof until its verdict lands.

The 2026-09-15 reconciliation repaired a later breach of that rule by appending `H-8`, `URFT-1`,
`A-AL2`, `GFT-1`, and `RA-1`--`RA-3`. The first four are theorem/scope statements whose own content
is not a carrier computation. The three `RA-*` rows are numerical or gate results on the single
finite-relational-accumulation carrier family; changing size or independently reconstructing the
same mathematical carrier does not create a second carrier.
