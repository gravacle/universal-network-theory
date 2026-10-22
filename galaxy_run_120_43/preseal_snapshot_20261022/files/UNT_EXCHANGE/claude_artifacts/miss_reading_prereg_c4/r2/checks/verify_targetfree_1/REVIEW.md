# REVIEW: verify_targetfree_1, the adversarial verification of targetfree finding B-1

Written 2026-10-18T19:36:03Z (`date -u`). The full record is in `VERIFY.md`, in this folder.

- **Finding:** B-1 (SHOULD_FIX). The seal and every root ruling of the miss-reading prereg r2 are bounded only by "before any NGC3198 target is opened". So they can come after the step-5 NGC predictions exist.
- **Result: NOT REFUTED.**
  - The quotes are verbatim: r2 L12; ROOT_ITEMS M-6 item 1 (L117); r2 L369-372.
  - Each piece of cited evidence is confirmed from bytes: V005 L513 (A60); L739 and L848 for the step numbering; RUNBOOK L7-L15; V004 L747 (A41) and L28 (A15); V005 L24 (A47 I3); 0594 L3.
  - Step 5 has still not launched: A93 at 19:31Z keeps its items "before any step-5 launch".
- **Further evidence, beyond what the finding cited:**
  - 0606 L5/L11 sets the prereg adoption deadline "before step 6".
  - ROOT_ITEMS L226 has the classifier sealed with the text "off the critical path until step 6".
  - Codex3's step-5 root item R12 decides the radial support "before freezing flags".
  - V005 L189 (A51): C5H model outputs stayed blinded until the V007 seal.
  - 0522 L9: root expects outer misses from the known flat curve.
  - The band width and the E1(b) comparison are both visible from step-5 outputs alone.
- **Reproduction:** a dimensionless synthetic toy. Once predictions are seen, the M-1/M-3 option choice moves P(P1) from about 0.07 to about 0.82 in a marginal case.
- **Imprecisions (minor):**
  - "C-Status" is not an r2 tag: the Status/Seal block is untagged and unmapped, and T6 cannot see it.
  - Not every prediction exists before the freeze: the sensitivity and STAGE0 runs come later. The headline predictions do exist, which is enough for the finding.
- **Severity: SHOULD_FIX, agreed.**
  - The window is planned (0606, M-12, R12), and there is precedent for blinding model outputs before a seal.
  - Not BLOCKING: no r2 sentence is false, and sealing now, before step 5, would be safe.
- **Fix: right in direction, insufficient as worded.**
  - "Produced or read" contradicts the validity-only sentence, and read literally it gates step 5 on the seal.
  - The fallback covers only the M rulings, not wording changes in r3 or the M-12 classifier.
  - "Exactly as written" cannot be carried out for M-7 (a point support flags no row) and is conditional for M-11.
  - It does not say who stays blind.
  - It names M-1..M-12 rather than every root item.
  - The amended fix is in VERIFY.md §4.2:
    - a reading-bound seal, preferably before step 5, with step 5 never delayed;
    - status-only handling until the seal, as for C5H, with an attestation;
    - a pre-prediction sha, dual reporting, and EXPLORATORY for post-prediction-only results;
    - the same bound for the radial support and the STAGE0 adoption;
    - a C-9 row, and a tag and map row for the seal clause.
