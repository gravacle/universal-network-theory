# REVIEW — verify_consistency_2 (pointer)

The full verification of lens C finding L-C02 is in `VERIFY.md` in this folder.

**Verdict: REFUTED as stated. Severity is NOTE; the lens gave SHOULD_FIX. The proposed fix is not sufficient as written; VERIFY.md §4 gives a smaller fix.**

- **The precedence the finding says is missing is already in the r2 bytes:**
  - PREREG [C-3] L169: "stays OPEN, whatever the score shows";
  - ROOT_ITEMS M-4 L89;
  - PREREG L201, L207, L284, L363 and L366;
  - for R-DRIFT, the deciding-test cell at L199.
- **The 110 events come from the lens classifier, which applies none of these clauses.** Under the text's own clauses:
  - 94 of the 110 have a unique status;
  - 2 are a lens input error (R-GRID, whose test has run);
  - 5 belong to L-C01 (2) and L-C08 (d) (3);
  - 9 depend on DT-T1a timing, which the finding does not raise.
- Evidence: `PRECEDENCE_REAPPLY_LC02.json`, from `tools/reapply_precedence_lc02.py`.
