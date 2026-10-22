# 0349 adversarial review record

**Audit:** CLAUDE2 helper 0349-audit; files listed in FILE_MANIFEST_0349_V001.json.
**Reviewer:** CLAUDE2 helper 0349-review, a separate Claude helper.
- It read bytes 1–41 only, worked from aggregates and masks, displayed no geometry values, and ran with no network.

**Verdict:** CONFIRMED_WITH_CAVEATS. The audit's answer to root holds. Six corrections, K1–K6, are recorded in AUDIT_CORRECTION_0349_V001.json:
- **K1:** a missed T↔f_D transposition, giving the new assumption A1b for NGC3198.
- **K2:** C9 is load-bearing.
- **K3:** A1 and A2 are plausible, not excluded.
- **K4:** item P8 should be labelled OBSERVED.
- **K5:** the separator search touches whole data lines.
- **K6:** A3 is load-bearing.

**Re-runs:** the audit tests, fixtures and document reconciliation reproduced byte-identically, and an independent census matches.
