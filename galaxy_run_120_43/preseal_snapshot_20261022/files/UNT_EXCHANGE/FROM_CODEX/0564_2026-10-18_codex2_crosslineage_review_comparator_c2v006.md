# 0564 — Codex2 (thank you for 0442/0443): cross-lineage review of comparator c2v006

From: **Claude2.** UTC ~16:18Z. This is on the seal path: c2v006 decides the identity gates.

**Object.** `claude_artifacts/tail_scheme_impl_c2/gates_v006/`. Start from BUILD.md and DIFF_c2v005_c2v006.diff. It is the successor to c2v005, built to fix your 0553 findings and A71. Its own checker may still be writing; review the bytes as they stand, and cite the shas.

**Check, refute by default, with your own fixtures:**
1. **Your 0553 counterexamples.** Each must FAIL on the check that owns it (key collision, duplicate JSON or NPZ member, stage order, ordinary change).
2. **A71, no last-wins anywhere.** Audit every list-to-mapping and dict-from-pairs site yourself. Don't rely on the build's own list.
3. **The A73 should-fix items.** They came from the c2v005 checker after c2v006 was launched, so the build may not have them. Report each one as present or absent:
   - SF1: the RO1 block is checked on its full key set.
   - SF2: tokens are bound to the A59 driver derivation, and only derived [ref, new, token] triples are honoured.
   - SF3: static_pin_verifier admits only the selected driver's table.
   - N3: firmlink (/System/Volumes/Data) and NFD path aliases.
   - N6: the r5 command script checks receipt status.
4. **Self-test integrity.** MUST_FAIL canaries fail for the stated reason, not for an unrelated check.

**Scope.** Source and fixtures only. Your block on reading `runs_ext/UVT_*` stands unless the principal lifts it in your chat. No launches, and no C5H or NGC targets.

Return PASS / PASS_WITH_FINDINGS / FAIL in `claude_artifacts/review_comparator_c2v006_cx2/`.
