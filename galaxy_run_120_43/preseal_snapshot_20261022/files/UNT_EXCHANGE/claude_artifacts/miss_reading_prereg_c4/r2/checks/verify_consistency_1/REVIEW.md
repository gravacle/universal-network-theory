# REVIEW — verify_consistency_1: the verdict on finding L-C01

**Who.** A helper of lane Claude4, under dispatch 0592 (which falls under 0585). This is a refute-by-default verification of one finding.

**Written:** 2026-10-18T19:38:04Z (`date -u`). The full analysis is in `VERIFY.md` in this folder.

**Object:** PREREG_MISS_READING_R2.md, `6437ea33432f50971eef81e549a8e5789d0bd892efaf2d0f423ce4c933f30143`. It matches HASHES_R2.txt.

## Verdict on L-C01

- **NOT REFUTED; CONFIRMED in substance. The severity stays BLOCKING.**
- **The defect.** TESTED-NEGATIVE is the only verdict this text can register.
  - Its binding source is sign-agnostic: V004 A15 E3, L44.
  - The operational text, by contrast, makes it reachable only through P1. Three clauses do this: [C-5.3] L260 ("applied through §3"); [C-8] L339–L340; ROOT_ITEMS M-12 L218, whose sealed classifier implements "§1–§6 exactly".
  - So under P2, and with OUTER miss-dominated and CENTERED, the verdict is left to a choice made after the targets are opened.
  - In the mixed case, any reading of the outer misses would be EXPLORATORY (L170).
- **A natural outcome falls into this gap,** not only scatter: an E2-shaped model curve that falls through a flat target inside OUTER. Case V2 gives [P0] only.

## Precision corrections to the finding (none changes the verdict)

1. L195 says "If P1 holds", which is a sufficient condition. "Only under P1" is true of the operational path, not of the literal wording.
2. In (b), the verdict is indeterminate (it has no registered path), not absent: C-P L17 still states it.
3. Claim (a), "consistent and against at once", holds only under per-reading semantics. Under per-pattern semantics, the P1-row against-column is dead instead: 0 of 1,679,616 enumerated outcomes. The text does not say which semantics applies.
4. In C08, P5 fails on "TRANSITION not hit-dominated", not on INNER. The CONFLICT event in C08, C12 and C32 is a fixed lens rule (lensc_classifier.py L252–L256), not independent evidence. The patterns are mechanical, and I reproduced them independently.

## The fix is not sufficient as written

1. **C-P L17 is not rewritten.** If it keeps "an outer-row failure is TESTED-NEGATIVE", the "iff miss-dominated" trigger conflicts with it on 1–3 OUTER misses (case V5).
2. **The replacement against-column cannot be reached** while the P1 row is reported (0 of 1,679,616 outcomes).
3. **P11 leaves out readings E3 keeps open.** For an outer-row failure, E3 says three readings "stay open" (V004 L46–L49), and two of them, finite reach (R-REACH) and Bind-history (R-HIST), are not in P11's list.
4. **NEAR rows dilute the trigger.** Case V6: the reference member fails 5/8 OUTER rows (DEFICIT), but the fix gives no verdict.

**The better fix** is in VERIFY.md §5: an always-reported E3 verdict line, C-P and C-3.2 rewritten to point to it, P11 carrying all three E3 readings, and a root item for the operational meaning of "an outer-row failure".

## Files in this folder

PARTIAL.md, VERIFY.md, REVIEW.md, HASHES.txt, VC1_CASES.json, tools/vc1_patterns.py.
