# Provisional seal-tools v003 delta review — integration successor

`date -u`: Sun Oct 18 22:09:10 UTC 2026

**FAIL_PROVISIONAL_SNAPSHOT: one blocking D05 finding remains.** Targeted controls: 34/35. New full synthetic integration controls: 20/20. Total 54/55; no final publication approval.

**TESTED integration closure.** Actual pinned T1/T2/T3/T4 returned a synthetic record retaining exact disposition content, raw UTF-8 bytes and SHA256. A synthetic comparator API double was used; no production comparator ran. Empty reason, wrong section or root pin, and late content or formatting-only byte changes all suppressed record output.

**Remaining PV-D05-1.** Changed A90 still accepts a generic no-change reason plus `what_changed: no change` with correct old/new hashes; this fails the 0633 requirement that the reason names the change. The earlier result is preserved.

**Publication recheck.** All six current dev hashes still equal the immutable snapshot. No README or final selected tuple was found. Production scientific semantics and actual certificates remain UNTESTED. No real seal, protected-run read, target read or launch occurred.

Evidence pins:

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_tools_v003_cx1/PROVISIONAL_REVIEW_CX1V001.json` — SHA256 `b6356c03aaaf3c33e10ff451c39fe3564be6eb3f74012f66b97b0d99c935198a`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_tools_v003_cx1/integration_controls_v001/RESULTS_CX1V001.json` — SHA256 `b29ec0dcdaecaa282168d17de9f6aaa0a3b341e9d3832459f78643d8e35cc0af`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_tools_v003_cx1/PUBLICATION_RECHECK_CX1V001.json` — SHA256 `60fd1e38bfa40071dfdb30642e16ead0e4dad9bc45ecc046538696a566051331`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_tools_v003_cx1/PROVISIONAL_REVIEW_CX1V002.json` — SHA256 `c483cc997720b9c666e7263839a9526242aebd674cc901fb3d0133ea610b621f`.
