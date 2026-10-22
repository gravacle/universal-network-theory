# PARTIAL — verify_newdefects_2 (adversarial verification of R2B-02)

Started: 2026-10-18T20:31:18Z (date -u)

Status: IN PROGRESS.

- Object hashes verified from bytes against HASHES_R2.txt: all 10 listed files MATCH (PREREG 97d5ce33..., CLAUSE_SOURCE_MAP 38cd6852..., ROOT_ITEMS 4907cf01..., NUMBER_PROVENANCE ff6ca9b8..., TARGET_FREE_CHECK 624f278e..., MUTATION 4445a9bf..., INDEX 0d24b8fe..., check tool 4ae4f705..., test tool dc812342..., make tool 2132078f...). HASHES_R2.txt itself: 2e3cf0c6...
- Next: read PREREG L1-L60, L100-L160, L330-L380, L470-L520; compare with round-1 L-C13 text and the closure table.

## Progress at 2026-10-18T20:38:06Z (date -u)

- Quotes verified in PREREG r2 (97d5ce33): L130-134 (C-1.1 post-target clause), L496 (C-9 row), L357 (C-5.3 "One line, always reported"), L25 (C-P "Every outcome registers"). NOT_READ occurs only at L132 and L496; it is defined nowhere in PREREG, ROOT_ITEMS, CSM, INDEX, tools, provenance or check JSON.
- History: round-1 r2 L93 "Root then rules before any reading is reported" (conditioned on a fail-closed stop, unconstrained content). Round-1 L-C13 fix text (consistency/REVIEW.md L321) proposed the NOT_READ wording verbatim; round-1 B-5 fix (targetfree/REVIEW.md L165) proposed "post-defect rulings ... NOT_AVAILABLE for the affected rows". Round-2 closure table B-5 row says "post-defect rulings limited (C-1.1)", but the binding L130 text has no post-defect trigger.
- Sources: V004 A15 E3 (487d4449, L43-44) is "binding": an outer-row failure "would be TESTED-NEGATIVE". V005 now 7f552858 (read 20:33:39Z); A48 section (L30-36) "A failure reading that does not rest on an unresolved or flagged input is still read"; A48 ruling 18 (L55) NOT_READ is a registered outcome with listed triggers, values reportable "labelled 'not read'".
- Codex2 0490 (3a922168) and REVIEW_CX2V001 (7e3b6211) do not raise this item. Rehearsal rough edges (19807bb3) do not either.
- Next: synthetic check that the v003g stop inputs are target-independent (functions extracted by ast; no module import), then VERIFY.md.

## Final status at 2026-10-18T20:44:14Z (date -u)

- DONE. VERIFY.md and REVIEW.md written; HASHES.txt follows.
- Verdict: NOT REFUTED; SHOULD_FIX confirmed; the fix's direction is right but its wording is insufficient (F1–F4; better fix in VERIFY §5).
- Reproduction: STOP_INPUTS_TARGET_INDEPENDENCE_VND2.json (0 fence events).
- V005 grew during the review: 7f552858 (20:33:39Z), then 5a996e97 (20:43:20Z, new A101 on B2 only). The A48 pin is unchanged. The object still matches HASHES_R2.txt at 20:43:20Z.
