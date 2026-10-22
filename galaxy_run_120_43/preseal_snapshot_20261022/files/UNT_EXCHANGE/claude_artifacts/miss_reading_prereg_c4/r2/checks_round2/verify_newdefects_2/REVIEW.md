# REVIEW — verify_newdefects_2: R2B-02 (post-target NOT_READ has no condition)

Helper of lane Claude4, under dispatches 0585 and 0606, refute-by-default under 0592. Written 2026-10-18T20:44:14Z (`date -u`). The full report is VERIFY.md.

**Object.** round2, all 10 files match HASHES_R2.txt (PREREG `97d5ce33ffa90e64ac208d36863c776460ad596fded2f376f1090a232e5ce407`). Re-checked at the end: still matching.

**Verdict.**
- **NOT REFUTED.**
- **Severity: SHOULD_FIX, confirmed.**
- **Fix: the direction is right, but the wording is insufficient** (VERIFY §5).

**Why the finding holds.**
- **The grant is real and has no trigger.** PREREG L130–132 lets root "declare the classification NOT_READ" after target access. Every stop runs, and must pass, before target access (L120–129), so the post-target clause never follows a stop.
- **NOT_READ is undefined.** It appears only at L132 and L496.
- **It conflicts with four sources:**
  - C-P L25, "Every outcome registers";
  - §5.3 L357, "One line, always reported";
  - V004 A15 E3 (L43–44, "binding");
  - the pinned A48 governing principle (V005 L34: "A failure reading that does not rest on an unresolved or flagged input is still read").
- **The intended scope was lost.** CSM L102 (B-5: "post-defect rulings limited") shows the author meant a post-defect scope, and the binding text dropped it. The wording comes from round-1 L-C13's proposed fix (consistency REVIEW L321), transcribed without its post-stop context.
- **The reproduction.** On v003g's own helpers, extracted with ast and not imported (0 fence events), every stop input is byte-identical across synthetic target sets, while E3 flips between NOT_NEGATIVE_AT_OUTER and TESTED-NEGATIVE. So in the v003g path no stop can newly fire after targets, and NOT_READ is available exactly when the outcome is known.
- **It is not already carried.** A98.2, 0619 and Codex2 0490 do not cover it, so r3 must carry it explicitly.

**One correction to the finding.** C-9 L496 can also be read as granting the same unconditioned NOT_READ, rather than scoping it to a stop. Either way C-9 calls the risk closed, so the defect stands.

**Gaps in the proposed fix.**
- **F1.** "Allow … only if" keeps a post-trigger choice between a field-map correction and NOT_READ.
- **F2.** "Still computed … the E3 line is printed" cannot be met under a missing-field stop, and under an ids or zone-table stop it would print a verdict resting on a defective input. Conversely, a stop that touches only NEAR should leave E3 read (A48; B-5's "affected rows").
- **F3.** "Target-free output fields byte-identical" does not bind remaps of the fields that decide tiers.
- **F4.** M-6 item 5 (the sha check "before the classifier runs") falls after RUNBOOK step 9, so it is post-target, and the fix gives no response if it fails.

**Better fix.**
- NOT_READ becomes a registered outcome with two fixed triggers:
  - a §1.1 stop re-run on the real score fires;
  - the item-5 sha check fails, with that check moved before RUNBOOK step 9.
- NOT_READ is scoped to the outputs whose inputs are defective. The headline stands, and E3 is read when its inputs are intact. Affected outputs read NOT_READ (<code>), with descriptive values labelled "not read" (A48 ruling 18).
- A field map renames keys only. It is required when a renaming reproduces the sealed M-12 suite byte for byte, and it is pinned before the output is read. Root has no choice.
- C-9 L496, CSM L102/L122 and the M-12 suite are updated to match.
