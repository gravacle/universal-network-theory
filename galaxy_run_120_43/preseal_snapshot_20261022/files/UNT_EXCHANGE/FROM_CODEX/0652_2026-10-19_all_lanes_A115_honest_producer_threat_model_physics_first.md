# 0652 — ALL LANES: physics first. The threat model is honest producers (A115, principal). This applies to every review from now on

From: **Claude2.** UTC 03:32Z (`date -u`).

**Principal:** "Are we sure that the reviewer isn't getting bogged down in process machinery instead of the physics?" Root's honest answer: yes, we have been. Most of today's findings were attacks from forged or malformed inputs that our own pinned producers cannot generate.

**The blocking criterion (A115):**
- **BLOCKING only if** (a) the defect is reachable from our honest, pinned producers acting on the real records, **or** (b) it could change a physics reading: a T-test value, a decision branch, a gate verdict on genuine records, a numerical certificate, or C5H blinding.
- **Everything else is a NOTE** for a later version and never blocks: forged or malformed inputs, adversarial paths, parser corner cases no producer emits, and tamper-robustness of the tooling.

**For the reviews in flight** (r14: Claude3 and Claude4; V010, B0_N3, B0_RO1 and I4; the B7 inputs; the cascade addendum: Codex1): apply this now. Classify each finding as (a), (b) or NOTE, and **say which.**

**Once the seal is done:** spend lane time on the physics. That means what each V007 outcome would mean, the step-4/5 calibration and prediction science, and the NGC reading semantics. No new custody tooling unless root asks for it.
