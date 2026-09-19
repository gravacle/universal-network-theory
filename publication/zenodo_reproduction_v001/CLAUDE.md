# Claude Code Review Guide

## Purpose

This is a deterministic review and reproduction packet for the completed
finite Universal Network Theory proof surface through `L = 12`. Review the
packet as evidence. Do not redesign the theory or rewrite provenance records.

This archive is a **prepublication preparation packet**, not a Zenodo deposit.
`CAPSULE_BUILD.json` records that status as `draft_not_for_publication: true`.

## Start here

1. `README.md`
2. `UNIVERSAL_NETWORK_THEORY_CLOSURE_THEOREM_V001.md`
3. `UNIVERSAL_NETWORK_THEORY_MAJOR_PROOF_INDEX.md`
4. `PUBLICATION_CLAIM_MAP.tsv`
5. For each claim: governing theorem -> listed supporting check or audit ->
   executable validator, when its closure is included -> stated claim boundary

`PUBLICATION_CLAIM_MAP.tsv` contains **15 claim records plus one header row**.
Its `supporting_check_or_audit` column does not, by itself, assert independent
authorship or an independent implementation. Treat a check as independent only
when the cited artifact states and substantiates that relationship. Otherwise
classify it as an executable verifier, same-packet adversarial review, or
self-consistency check, as applicable.

The Markdown Closure Theorem and Major Proof Index are the content authorities.
Their `.docx` files are the publication renderings.

## Verify first

From the extracted packet root, run:

```bash
python3 -B tools/verify_extracted_capsule.py .
```

Treat `SHA256SUMS` and `CAPSULE_BUILD.json` as the archive-integrity record.
If verification fails, report the exact command and artifact. Do not
substitute fixtures, alter hashes, or relax a check.

## Governing terminology

- **RFT**: Record Formation Theory.
- **ARGER**: `ALLOW -> REQUIRE -> GATE -> EM -> RECORD`.
- **GATE** is the single ARGER Gate. Numbered labels preserved in sealed
  evidence are archival implementation identifiers, not multiple theoretical
  gates.
- **GFT**: Gravity Formation Theory -- what follows when eligible record
  structure satisfies the Gate.
- `L` is finite-domain size and one-pass horizon, not a proof level or software
  version.
- `q` is retained-carrier/spent-lineage rank.
- `n` is event-prefix depth.

## Principal finite claim

The authenticated `A009--A016` block has:

- exact audited bounded membership at `L = 4, 6, 8, 10, 12`;
- deduplicated mass greater than `0.50` at every authenticated size;
- positive finite visibility in all 13 selected `(L,q)` rows; and
- minimum `R_low = 0.4280947078156539`.

Under the adopted single ARGER Gate, these premises establish the finite GFT
`z=1` classification through `L = 12`.

## Important distinctions

- The final `L = 12` adjudication and the strict common-lineage diagnostic are
  separate results with separate evidence. `EXACT_ADJUDICATION_V003R1.json`
  supports the `1156/1156` finite history/state adjudication. It does not
  contain the strict-lineage values.
- The strict common-lineage sequence
  `0.0244800482 -> 0.0687369678 -> 0.1157085222` is supported in the capsule by
  `evidence/STRICT_COMMON_LINEAGE_PROGRESSION_V001.json`. It is a secondary
  diagnostic, not the Gate mass and not a Gate premise.
- The capsule reruns the `L = 8` and `L = 10` strict-lineage extraction. The
  `L = 12` Target/Hostile values are authenticated outputs of the full
  repository workflow, not estimates or unexecuted constants. A 2026-09-18
  review rerun reproduced both values and generated a report byte-identical to
  the sealed report. The complete audited workspace is approximately 59 GB;
  the minimum runnable `L = 12` reconstruction set alone contains 86 files and
  13,485,786,130 bytes (12.559617 GiB). The focused capsule therefore preserves
  the method, result, and cryptographic custody without duplicating the bulk
  generated input arrays. It makes no claim that the compact archive itself
  replays that 13.49-GB calculation.
- The `L = 12` complete block mass is `0.56956498393327842`.
- The separately sealed dynamical-exponent `z=1` theorem is conditional on
  its named LL-P premise; do not merge it with the finite Gate classification.
- Alpha is typed as construction-scoped `ALLOW` plus governing-domain
  `REQUIRE`: within a domain satisfying `SAI1--SAI8`, its measured alpha and RG
  trajectory are constitutive for every coefficient-preserving same-sector
  record.
- The incomplete `L = 14` attempt supplies no premise or result.
- **Git-only** means an item is documentary in this packet and its execution
  path is defined by the immutable repository release. It does not imply that
  large generated caches or workspaces are committed to Git; named generated
  inputs must be rebuilt by the documented construction path when required.

## Review boundaries

- Do not edit dated, sealed, hash-pinned, audited, or evidentiary artifacts.
- Do not normalize historical terminology inside those artifacts.
- Do not alter hashes, manifests, expected counts, thresholds, or fixtures.
- Do not publish, upload, create a DOI, push Git, invoke AWS, or run paid
  computation.
- Do not treat preparation placeholders as release metadata.
- Propose corrections to current navigation or publication prose separately
  from historical evidence.
- Classify findings as:
  1. archive-integrity failure;
  2. executable reproduction failure;
  3. claim/evidence mismatch;
  4. navigation or terminology defect; or
  5. optional editorial suggestion.

For every substantive finding, cite the file, line, affected claim ID, and
whether the executable result changes.
