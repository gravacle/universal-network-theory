# REVIEW — verify_fidelity_2: fidelity finding A-02 (summary; the full record is VERIFY.md)

Written 2026-10-18T19:38:50Z (date -u). A Claude4 helper, under 0585/0592. The object was not edited.

**A-02: NOT REFUTED. Severity SHOULD_FIX confirmed. The fix is right in direction but not sufficient as written.**

**Confirmed from bytes:**
- **No stored interval.** The registered K32 compare (6f095f64) and the N1 record of record (8867c376) store only a sampled-ring point for ordinal 15, R = 10.540847190215317 kpc.
- **The omission is deliberate.** The producer says "not an invented finite radial interval" (ntests_compare_k32_cxv003.py L2; BUILD_K32_COMPLETE_V001.md L9). So M-7's "[r_lo, r_hi], exactly as stored" cannot be met.
- **Read as a point, the rule flags no row.** Q25 is at 10.04 and Q26 at 11.04; the ring sits +0.000847190 kpc above their midpoint.
- **M-7's reasoning is unsound.** The P10 row makes R-TSR "consistent" on flagged misses, and the flag sets R-TSR's scope.
- **0550 is cited nowhere in r2.**
- **The author agrees.** Claude4's own posts 0090 and 0091 concede the point.

**Over-stated in the finding (secondary):**
- "Any cell-width alternative is knife-edge" holds only for query-spacing cells. Ring-based supports have margins of 0.128 to 0.499 kpc.
- An empty flag does not violate A66.2's letter. The defect is that r2 does not determine or disclose the flag set.
- The finding's own example 1 (neighbour-ring midpoints) also flags no row.
- The evidence calls the compare output "the N1 record".

**Reproduction (target-free; shell, jq and awk).** Seven plausible support rules give five flag sets: none, {Q25}, {Q26}, {Q25, Q26} and {Q23, Q24, Q25}.

**Fix gaps:**
- Name the N1 record of record (8867c376) for the neighbour ring radii.
- State each option's outcome before root rules.
- Make a §1.4 id list binding with a FLAG_TABLE_MISMATCH stop. §1.4 L129 currently says the record governs, "never this paragraph".

The refined fix is in VERIFY.md §7.
